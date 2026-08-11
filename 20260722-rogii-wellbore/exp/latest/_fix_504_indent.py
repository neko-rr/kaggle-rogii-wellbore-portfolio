# -*- coding: utf-8 -*-
"""Fix corrupted TIP_CV_MODE if-line in tip-cv-chk504 cell 57."""
from __future__ import annotations

import json
import re
from pathlib import Path

NB = Path(__file__).resolve().parents[2] / "my-notebook/tip-cv-chk504-468-gated-h20/tip-cv-chk504-468-gated-h20.ipynb"

FIXED_BLOCK = """    # tip-cv: train 側でも id 集合一致を強制
    if bool(globals().get('TIP_CV_MODE', False)):
        sub = sub[sub['id'].isin(set(sample['id']))].drop_duplicates('id', keep='last')
        sample = sample[sample['id'].isin(set(sub['id']))].drop_duplicates('id', keep='last')
        sub = sample[['id']].merge(sub, on='id', how='left')
"""


def main() -> None:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    c = nb["cells"][57]
    src = "".join(c.get("source", []))
    # Match broken comment+if mashed into one line, plus the following indented body
    pat = re.compile(
        r"# tip-cv:[^\n]*\n?\s*if bool\(globals\(\)\.get\('TIP_CV_MODE', False\)\):\n"
        r"\s*sub = sub\[sub\['id'\]\.isin\(set\(sample\['id'\]\)\)\]\.drop_duplicates\('id', keep='last'\)\n"
        r"\s*sample = sample\[sample\['id'\]\.isin\(set\(sub\['id'\]\)\)\]\.drop_duplicates\('id', keep='last'\)\n"
        r"\s*sub = sample\[\['id'\]\]\.merge\(sub, on='id', how='left'\)\n",
        flags=re.MULTILINE,
    )
    # Also match when if is stuck inside the comment (no real newline before if)
    pat2 = re.compile(
        r"# tip-cv:.*?if bool\(globals\(\)\.get\('TIP_CV_MODE', False\)\):\n"
        r"\s*sub = sub\[sub\['id'\]\.isin\(set\(sample\['id'\]\)\)\]\.drop_duplicates\('id', keep='last'\)\n"
        r"\s*sample = sample\[sample\['id'\]\.isin\(set\(sub\['id'\]\)\)\]\.drop_duplicates\('id', keep='last'\)\n"
        r"\s*sub = sample\[\['id'\]\]\.merge\(sub, on='id', how='left'\)\n",
        flags=re.DOTALL,
    )
    new_src, n = pat.subn(FIXED_BLOCK, src, count=1)
    if n == 0:
        new_src, n = pat2.subn(FIXED_BLOCK, src, count=1)
    if n == 0:
        # manual locate
        idx = src.find("drop_duplicates('id', keep='last')")
        print("AUTO FAIL; context:\n", repr(src[idx - 200 : idx + 250]))
        raise SystemExit(1)
    try:
        compile(new_src, "cell_57", "exec")
        print("compile OK")
    except SyntaxError as e:
        print("compile still fail", e)
        # show line
        lines = new_src.splitlines()
        ln = (e.lineno or 1) - 1
        for j in range(max(0, ln - 5), min(len(lines), ln + 5)):
            print((">>" if j == ln else "  "), j + 1, lines[j])
        raise SystemExit(2)
    c["source"] = [line + "\n" for line in new_src.split("\n")]
    # avoid double newline at end only if original didn't care
    if new_src.endswith("\n") and c["source"] and c["source"][-1] == "\n":
        c["source"].pop()
    NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", NB)


if __name__ == "__main__":
    main()
