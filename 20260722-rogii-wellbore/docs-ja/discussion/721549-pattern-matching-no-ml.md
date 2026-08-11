# Does pattern matching solutions (no ML) work here?

> Topic ID: **721549** · **Andrey Chankin** · **2026/07/06** · 票 7  
> 最新: **2026/07/20** · 原文: `docs-en/discussion/721549-pattern-matching-no-ML.md`

## 要約

動画のような horizontal GR ↔ typewell GR マッチを試すが、持続的にベース超えできず。**平坦井**で上下に振れすぎる。手合わせでも理由が不明な領域あり。

| 誰 | 内容 |
|---|---|
| Shrey [+3] | 多くの井では効くが、**GR 重なりが悪い井**が多数 |
| Ochir [+2] | 候補パス集合（likpf/pf/beam/formation 等）の **oracle ≈4.5–…**（CLI 途中）。良いパスは存在するが選ぶのが難しい、という含意 |
| Andrey (7/20) | flat 井の悪影響回避は未解決 → writeup を読め |

## 示唆

- 純マッチ単体は不十分。候補生成＋選択（ガード付き）が本命寄り  
- flat 井の過振れ抑制が必須
