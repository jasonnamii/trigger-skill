# trigger-skill

> 정식명 28 + 콤보 9 부분문자열 hit → 응답 첫 토큰 전 무조건 발동. 판단·맥락평가·픽션면제 ✗.

## 무엇을 하는가

**모든 사용자 메시지**에서 28 정식명·9 콤보가 조사·어미 변주 포함 부분문자열로 등장하면 자동 invoke. "발동할 정도인가?" 판단 회로를 제거하고 `if name in message → invoke`로 결정주의 게이트를 박았다.

## 왜 존재하는가

`trigger-dictionary` 5세대 진화에서 발견된 사실: **description이 추상적일수록 발동률은 떨어진다.** 본 스킬은 가장 효과 컸던 기법 3개(부분문자열 매칭·FAIL 박제·조사변주 — v1.1 HARD-FIRE 핵심)와 v3.7의 glossary 강제 Read 게이트를 결합. 발동률 100% + 정의 활용 verbatim 100%를 동시 보증.

## 트리거 (28 + 9)

**정식명 28종:** 홈즈 · 오컴 · 제1원리 · 베이지안 · 엄브렐러 · 아날로지 · 연역수렴 · 외과적 · 수정4 · 백본 · 스켈레톤 · SHE · 엘베피치 · 타임스톤 · 맥가이버 · 넛지 · 프리모르템 · 트리아지 · 줌 · 절대자 · 틀밖 · 부작업 · 주작업 · 제출청소 · 작업설계자 · 핑퐁 · 리허설 · 작업계획

**콤보 9종:** 미궁 · 마비 · 시야 · 벽 · 카드없음 · 장밋빛폭주 · 제출직전 · 복잡계 · 박스

## 6대 RULE (HARD-FIRE)

1. **100% 발동** — 부분문자열 hit = 무조건. 발동 확률 1.0
2. **조사·어미 불변** — `홈즈` = `홈즈를` = `홈즈로` = `홈즈 해줘` 전부 발동
3. **정식명 전용** — 유사어·오타·약어 ✗
4. **문맥 무시** — 농담·반어·인용·과거형·부정문·픽션 = 무관
5. **컨펌 게이트** — 핑퐁·리허설·작업계획은 컨펌 대기
6. **복수 트리거** — N개 동시 등장 시 전부 발동 (관점→분석→구조→판단→실행→전환 순)

## 설치

```bash
git clone https://github.com/jasonnamii/trigger-skill.git ~/.claude/skills/trigger-skill
```

또는 `.skill` 파일 더블클릭으로 Cowork 설치.

## 검증

내부 eval 40/40 (100%). `evals/cases.json` + `changelog.md` 참조 (autoloop 진화 기록).

## 헤리티지

본 스킬은 다음의 결합:
- `trigger-dictionary v1.1 HARD-FIRE` — 부분문자열 매칭 + FAIL 박제 + 조사변주 (baseline 대비 +18.2pt 점프의 핵심)
- `trigger-dictionary v3.2-enforce` — 매 메시지 invoke + 비대칭 비용 프레이밍
- `trigger-dictionary v3.7` — glossary 강제 Read 게이트

## 라이선스

Proprietary. LICENSE 참조.
