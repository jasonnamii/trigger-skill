# trigger-skill

> Hard-fire trigger invocation engine — 28 formal triggers + 9 combos with deterministic substring matching, no judgment, no context evaluation, no fiction-frame exemption.

## What it does

Forces invocation on **every user message** when any of 28 trigger names or 9 combo names appears as a substring (with Korean particle/ending variants). Replaces fuzzy "should I invoke?" reasoning with a hard gate: `if name in message → invoke. else → skip`.

## Why it exists

Five generations of `trigger-dictionary` evolution showed that LLMs systematically under-invoke when description is abstract. This skill encodes the highest-yield techniques from `trigger-dictionary v1.1 HARD-FIRE` (substring matching, FAIL branding, particle variants) and merges the v3.7 glossary-verbatim gate (forced `Read` on hit) — guaranteeing both invocation rate and definition fidelity.

## Triggers (28 + 9)

**28 formal names:** 홈즈 · 오컴 · 제1원리 · 베이지안 · 엄브렐러 · 아날로지 · 연역수렴 · 외과적 · 수정4 · 백본 · 스켈레톤 · SHE · 엘베피치 · 타임스톤 · 맥가이버 · 넛지 · 프리모르템 · 트리아지 · 줌 · 절대자 · 틀밖 · 부작업 · 주작업 · 제출청소 · 작업설계자 · 핑퐁 · 리허설 · 작업계획

**9 combos:** 미궁 · 마비 · 시야 · 벽 · 카드없음 · 장밋빛폭주 · 제출직전 · 복잡계 · 박스

## 6 RULES (HARD-FIRE)

1. **100% invoke** on substring match. Probability = 1.0.
2. **Particle/ending invariant.** `홈즈` = `홈즈를` = `홈즈로` = `홈즈 해줘` — all fire.
3. **Formal names only.** Synonyms, typos, abbreviations don't fire.
4. **Context-blind.** Jokes, irony, fiction, past tense, negation — all fire.
5. **Confirm gate.** `핑퐁`/`리허설`/`작업계획` wait for user confirmation.
6. **Multiple triggers.** N triggers in one message → all fire, in order: perspective → analysis → structure → judgment → execution → switch.

## Installation

```bash
# Clone into Claude Code skills directory
git clone https://github.com/jasonnamii/trigger-skill.git ~/.claude/skills/trigger-skill
```

Or download the `.skill` package and double-click to install in Cowork.

## Validation

40/40 cases pass (100%) on internal eval suite. See `evals/cases.json` and `changelog.md` for autoloop history.

## Heritage

Built on:
- `trigger-dictionary v1.1 HARD-FIRE` — substring matching + FAIL branding + particle variants (the +18.2pt jump from baseline)
- `trigger-dictionary v3.2-enforce` — every-message invoke + asymmetric cost framing
- `trigger-dictionary v3.7` — glossary verbatim gate

## License

Proprietary. See LICENSE.

---

🇰🇷 [한국어 README](README.ko.md)
