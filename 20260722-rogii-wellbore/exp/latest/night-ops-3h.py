# -*- coding: utf-8 -*-
"""Night ops ~3h: harvest GPU jobs, push next, leave 2 submit-ready kernels.

User sleep window. Does NOT competitions submit. Does NOT Final-swap.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COMP = ROOT / "20260722-rogii-wellbore"
EXP = COMP / "exp"
LATEST = EXP / "latest"
WORK = EXP / "work" / "wave31-neural-proposal"
VENV_KAGGLE = ROOT / ".venv" / "Scripts" / "kaggle.exe"
PS1 = ROOT / "scripts" / "kaggle-cli.ps1"
ASSERT = ROOT / "scripts" / "assert-kaggle-private.ps1"

WINDOW_SEC = int(os.environ.get("NIGHT_OPS_WINDOW_SEC", str(3 * 3600)))
# 提出候補が RUNNING のまま窓終了した場合、完走待ちを延長（新規 push はしない）
DRAIN_SEC = int(os.environ.get("NIGHT_OPS_DRAIN_SEC", str(6 * 3600)))
POLL_SEC = int(os.environ.get("NIGHT_OPS_POLL_SEC", "90"))
LOG = LATEST / "night-ops-3h.log"
STATE = LATEST / "night-ops-3h-state.json"
WAKE = LATEST / "wake-submit-ready-2026-08-03.md"

TRACK = [
    {
        "chk": "CHK-504",
        "slug": "tip-cv-chk504-468-gated-h20",
        "role": "tip-cv",
        "out": WORK / "out-504-tip-cv",
        "local": COMP / "my-notebook" / "tip-cv-chk504-468-gated-h20",
        "retry_on_error": True,
        "priority": 3,
    },
    {
        "chk": "CHK-492b",
        "slug": "tip-cv-chk492b-ess1p0-h20",
        "role": "tip-cv",
        "out": WORK / "out-492b-tip-cv",
    },
    {
        "chk": "CHK-492",
        "slug": "tip-cv-chk492-490b-h20",
        "role": "tip-cv",
        "out": WORK / "out-492-tip-cv",
        "push_after": "CHK-492b",
        "local": COMP / "my-notebook" / "tip-cv-chk492-490b-h20",
    },
    {
        "chk": "CHK-514",
        "slug": "tip-submit-chk514-hd-fracSpos07",
        "role": "submit-candidate",
        "out": WORK / "out-514-submit",
        "local": COMP / "my-notebook" / "tip-submit-chk514-hd-fracSpos07",
        "priority": 1,
    },
    {
        "chk": "CHK-515",
        "slug": "tip-submit-chk515-row-signed-or-absd2",
        "role": "submit-candidate",
        "out": WORK / "out-515-submit",
        "local": COMP / "my-notebook" / "tip-submit-chk515-row-signed-or-absd2",
        "priority": 2,
    },
]


def log(msg: str) -> None:
    line = f"{datetime.now(timezone.utc).isoformat()} {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {
        "started": datetime.now(timezone.utc).isoformat(),
        "harvested": {},
        "pushed": {},
        "submit_ready": [],
        "errors": [],
    }


def save_state(st: dict) -> None:
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        shell=False,
    )


def ps(args: list[str], cwd: Path | None = None, timeout: int = 600) -> subprocess.CompletedProcess:
    cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(PS1), *args]
    return run(cmd, cwd=cwd, timeout=timeout)


def _norm_status(text: str) -> str:
    u = (text or "").upper()
    for key in ("COMPLETE", "RUNNING", "ERROR", "CANCELLED", "CANCELED", "QUEUED", "PENDING"):
        if key in u:
            return "CANCELLED" if key in ("CANCELLED", "CANCELED") else key
    return "UNKNOWN"


def kernel_status(slug: str) -> dict | None:
    if not VENV_KAGGLE.exists():
        return None
    r = run(
        [str(VENV_KAGGLE), "kernels", "status", f"kazeneko77/{slug}"],
        timeout=120,
    )
    text = (r.stdout or "") + (r.stderr or "")
    try:
        data = json.loads(r.stdout or "{}")
        if isinstance(data, dict) and data:
            raw = str(data.get("status") or data.get("hasStatus") or "")
            data["status"] = _norm_status(raw or text)
            return data
    except Exception:
        pass
    return {"status": _norm_status(text), "raw": text[-500:]}


def free_gpu_slots() -> int:
    # Kaggle GPU max 2 — count RUNNING among tracked + known GPU slugs
    known = {t["slug"] for t in TRACK} | {
        "chk496-297-dual-e2e-gpu",
        "tip-cv-chk504-468-gated-h20",
        "tip-cv-chk492b-ess1p0-h20",
        "tip-cv-chk492-490b-h20",
    }
    n = 0
    for slug in sorted(known):
        st = kernel_status(slug)
        if st and st.get("status") == "RUNNING":
            n += 1
    return max(0, 2 - min(n, 2))


def harvest(slug: str, out_dir: Path) -> bool:
    out_dir.mkdir(parents=True, exist_ok=True)
    # pull output
    r = ps(
        ["kernels", "output", f"kazeneko77/{slug}", "-p", str(out_dir), "-q"],
        timeout=900,
    )
    ok = r.returncode == 0
    log(f"harvest {slug} rc={r.returncode} out={out_dir}")
    if not ok:
        log(f"harvest stderr: {(r.stderr or '')[-400:]}")
    # also status json
    st = kernel_status(slug)
    (out_dir / "kernel-status.json").write_text(json.dumps(st, indent=2), encoding="utf-8")
    return ok


def assert_private(folder: Path) -> bool:
    r = run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ASSERT),
            "-KernelDir",
            str(folder),
        ],
        timeout=120,
    )
    if r.returncode != 0:
        log(f"assert-private FAIL {folder}: {(r.stderr or r.stdout or '')[-300:]}")
        return False
    return True


def push_kernel(folder: Path, slug: str) -> bool:
    if not folder.exists():
        log(f"push skip missing {folder}")
        return False
    if not assert_private(folder):
        return False
    r = ps(["kernels", "push", "-p", str(folder)], cwd=ROOT, timeout=900)
    log(f"push {slug} rc={r.returncode}")
    if r.returncode != 0:
        log(f"push err: {(r.stderr or r.stdout or '')[-500:]}")
        return False
    return True


def ban_gate(chk: str, hypo: str, action: str = "T3") -> bool:
    script = ROOT / "scripts" / "run-hypothesis-ban-gate.ps1"
    if not script.exists():
        log("ban-gate script missing — skip")
        return True
    r = run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script),
            "-ChkId",
            chk,
            "-ActionType",
            action,
            "-Hypothesis",
            hypo,
            "-Phase",
            "pre",
            "-Mechanism",
            "tip E2E then row/well gate on 468 before_hedge; not full mid FINAL",
            "-ExpDir",
            str(EXP),
        ],
        timeout=180,
    )
    log(f"ban-gate {chk} rc={r.returncode}")
    if r.returncode != 0:
        log((r.stdout or "")[-400:] + (r.stderr or "")[-200:])
    return r.returncode == 0


def write_wake(st: dict) -> None:
    ready = st.get("submit_ready", [])
    lines = [
        "# 起床時 — 提出待機（夜間オーケストレータ）",
        "",
        f"- 開始: `{st.get('started')}`",
        f"- 更新: `{datetime.now(timezone.utc).isoformat()}`",
        f"- 窓: {WINDOW_SEC // 3600}h",
        "",
        "## 提出候補（ユーザー確認後に Submit · Agent は提出しない）",
        "",
    ]
    if len(ready) >= 2:
        for i, item in enumerate(ready[:2], 1):
            lines.append(f"{i}. **{item.get('chk')}** `{item.get('slug')}` status={item.get('status')} tipdist≈{item.get('tipdist')}")
            lines.append(f"   - URL: https://www.kaggle.com/code/kazeneko77/{item.get('slug')}")
            lines.append(f"   - out: `{item.get('out')}`")
    else:
        lines.append(f"- COMPLETE {len(ready)}/2 · 状態は `night-ops-3h-state.json` 参照")
        for item in ready:
            lines.append(f"  - ready: {item}")
        for chk in ("CHK-514", "CHK-515"):
            pu = st.get("pushed", {}).get(chk, {})
            hs = st.get("harvested", {}).get(chk, {})
            if pu.get("ok") and hs.get("status") != "COMPLETE":
                slug = pu.get("slug", "")
                lines.append(f"  - running/pending: **{chk}** `{slug}` harvest={hs.get('status', 'pending')}")
                lines.append(f"    URL: https://www.kaggle.com/code/kazeneko77/{slug}")
    lines += [
        "",
        "## Final 2（変更しない）",
        "",
        "- 枠1: SUB-14",
        "- 枠2: farvol 0.95/0.05",
        "",
        "## 禁止",
        "",
        "- Soft / F041 · raw before FINAL · full mid≠tip FINAL (F042)",
        "- 同一提出の二重 Submit",
        "- Agent による `competitions submit`",
        "",
        "## harvest 済み tip-cv",
        "",
    ]
    for k, v in st.get("harvested", {}).items():
        lines.append(f"- {k}: {v}")
    WAKE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"wrote {WAKE}")


def scan_tipdist(out_dir: Path) -> float | None:
    for name in (
        "submission_chk514_hd.csv",
        "submission_chk515_row.csv",
        "submission.csv",
        "submission_tip_before_gate.csv",
    ):
        p = out_dir / name
        if p.exists() and name.startswith("submission_chk"):
            # need tip before for distance — skip if alone
            pass
    tip = out_dir / "submission_tip_before_gate.csv"
    sub = out_dir / "submission.csv"
    if tip.exists() and sub.exists():
        try:
            import pandas as pd
            import numpy as np

            a = pd.read_csv(tip).sort_values("id")
            b = pd.read_csv(sub).sort_values("id")
            m = a.merge(b, on="id", suffixes=("_t", "_p"))
            return float(np.sqrt(np.mean((m["tvt_p"] - m["tvt_t"]) ** 2)))
        except Exception as e:
            log(f"tipdist err: {e}")
    return None


def maybe_push_queue(st: dict) -> None:
    slots = free_gpu_slots()
    log(f"free_gpu_slots≈{slots}")
    if slots <= 0:
        return
    # order: 514, 515, then 504 retry, then 492 if 492b harvested
    queue = []
    for t in TRACK:
        if t.get("role") != "submit-candidate":
            continue
        if t["chk"] in st["pushed"] and st["pushed"][t["chk"]].get("ok"):
            # allow re-push only if later ERROR and retry flag — handled below for tip-cv
            continue
        if t["chk"] in st.get("harvested", {}) and st["harvested"][t["chk"]].get("status") == "COMPLETE":
            continue
        queue.append(t)
    # tip-cv retries (e.g. 504 IndentationError fix)
    for t in TRACK:
        if not t.get("retry_on_error"):
            continue
        hs = st.get("harvested", {}).get(t["chk"], {})
        if hs.get("status") != "ERROR":
            continue
        # already re-pushed after this error?
        if st.get("pushed", {}).get(t["chk"], {}).get("retry_after_error"):
            continue
        if t.get("local"):
            queue.append(t)
    queue.sort(key=lambda x: x.get("priority", 99))
    # 492 after 492b complete
    t492 = next(x for x in TRACK if x["chk"] == "CHK-492")
    if (
        st.get("harvested", {}).get("CHK-492b", {}).get("status") == "COMPLETE"
        and "CHK-492" not in st["pushed"]
        and t492.get("local")
    ):
        queue.append(t492)

    for t in queue:
        if slots <= 0:
            break
        hypo = (
            "H-D well+row gate tip×468 before_hedge E2E submit candidate"
            if t["chk"] == "CHK-514"
            else "row-only signed∨absd2 tip×468 before_hedge E2E submit candidate"
            if t["chk"] == "CHK-515"
            else "tip-cv CHK-492 after 492b"
        )
        action = "T3" if t["chk"].startswith("CHK-51") else "T0"
        if not ban_gate(t["chk"], hypo, action):
            st["errors"].append({"chk": t["chk"], "err": "ban-gate"})
            save_state(st)
            continue
        local = t.get("local")
        if not local or not Path(local).exists():
            log(f"no local for {t['chk']}")
            continue
        ok = push_kernel(Path(local), t["slug"])
        entry = {
            "ok": ok,
            "slug": t["slug"],
            "at": datetime.now(timezone.utc).isoformat(),
        }
        if t.get("retry_on_error") and st.get("harvested", {}).get(t["chk"], {}).get("status") == "ERROR":
            entry["retry_after_error"] = True
            if ok:
                # clear ERROR so poll tracks new run
                st["harvested"].pop(t["chk"], None)
        st["pushed"][t["chk"]] = entry
        save_state(st)
        if ok:
            slots -= 1
            time.sleep(15)


def poll_once(st: dict) -> None:
    for t in TRACK:
        chk = t["chk"]
        slug = t["slug"]
        # skip if already harvested complete
        prev = st.get("harvested", {}).get(chk, {})
        if prev.get("status") == "COMPLETE" and prev.get("harvest_ok"):
            continue
        if prev.get("status") == "ERROR":
            continue
        st_k = kernel_status(slug)
        if not st_k:
            continue
        status = str(st_k.get("status") or st_k.get("hasStatus") or "").upper()
        if not status or status == "UNKNOWN":
            # try nested
            for k, v in st_k.items():
                if isinstance(v, str) and v.upper() in ("COMPLETE", "RUNNING", "ERROR"):
                    status = v.upper()
                    break
        log(f"status {chk} {slug}={status}")
        if status == "COMPLETE":
            ok = harvest(slug, Path(t["out"]))
            tipd = scan_tipdist(Path(t["out"]))
            st.setdefault("harvested", {})[chk] = {
                "status": "COMPLETE",
                "harvest_ok": ok,
                "tipdist": tipd,
                "at": datetime.now(timezone.utc).isoformat(),
            }
            if t.get("role") == "submit-candidate" and ok:
                item = {
                    "chk": chk,
                    "slug": slug,
                    "status": "COMPLETE",
                    "tipdist": tipd,
                    "out": str(t["out"]),
                }
                # replace or append
                st["submit_ready"] = [x for x in st.get("submit_ready", []) if x.get("chk") != chk]
                st["submit_ready"].append(item)
            save_state(st)
            write_wake(st)
        elif status == "ERROR":
            st.setdefault("harvested", {})[chk] = {
                "status": "ERROR",
                "at": datetime.now(timezone.utc).isoformat(),
            }
            st["errors"].append({"chk": chk, "status": "ERROR"})
            save_state(st)
            # pull logs anyway
            harvest(slug, Path(t["out"]))


def ensure_nbs() -> None:
    builder = LATEST / "_build_night_submit_nbs.py"
    r = run([sys.executable, str(builder)], timeout=120)
    log(f"build nbs rc={r.returncode}")
    if r.returncode != 0:
        log((r.stderr or r.stdout or "")[-500:])


def main() -> int:
    LOG.write_text("", encoding="utf-8")
    log(f"night-ops start window={WINDOW_SEC}s drain={DRAIN_SEC}s")
    ensure_nbs()
    st = load_state()
    st["started"] = st.get("started") or datetime.now(timezone.utc).isoformat()
    save_state(st)
    write_wake(st)
    t0 = time.time()
    while time.time() - t0 < WINDOW_SEC:
        try:
            poll_once(st)
            maybe_push_queue(st)
            write_wake(st)
        except Exception as e:
            log(f"loop err: {e}")
            st["errors"].append({"err": str(e), "at": datetime.now(timezone.utc).isoformat()})
            save_state(st)
        ready = [x for x in st.get("submit_ready", []) if x.get("status") == "COMPLETE"]
        if len(ready) >= 2:
            tip_done = all(
                st.get("harvested", {}).get(c, {}).get("status") in ("COMPLETE", "ERROR")
                for c in ("CHK-504", "CHK-492b")
            )
            if tip_done:
                log("early exit: tip-cv settled + 2 submit-ready")
                break
        time.sleep(POLL_SEC)

    # drain: 既に push した提出候補の完走のみ待つ（新規 push なし）
    log("active window end — drain phase (no new push)")
    t1 = time.time()
    while time.time() - t1 < DRAIN_SEC:
        try:
            poll_once(st)
            write_wake(st)
        except Exception as e:
            log(f"drain err: {e}")
        ready = [x for x in st.get("submit_ready", []) if x.get("status") == "COMPLETE"]
        pending_push = [
            c
            for c in ("CHK-514", "CHK-515")
            if st.get("pushed", {}).get(c, {}).get("ok")
            and st.get("harvested", {}).get(c, {}).get("status") not in ("COMPLETE", "ERROR")
        ]
        if len(ready) >= 2 and not pending_push:
            log("drain complete: 2 submit-ready")
            break
        if not pending_push and len(ready) < 2:
            # まだ push できていない — 枠待ちを続ける（drain 中も push 許可）
            maybe_push_queue(st)
        time.sleep(POLL_SEC)

    write_wake(st)
    log("night-ops end")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
