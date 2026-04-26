#!/usr/bin/env python3
"""
trigger_scanner.py v3.5 — 결정주의 트리거 스캐너

stdin/argv → stdout: 헤더 1줄 또는 빈 문자열.
LLM 판단 0%. 모든 결정은 이 스크립트가.

Usage:
    python3 trigger_scanner.py "사용자 메시지"
    echo "사용자 메시지" | python3 trigger_scanner.py -
"""

import re
import sys

# ===== 28 정식명 =====
TRIGGERS = [
    "홈즈","오컴","제1원리","베이지안","엄브렐러","아날로지","연역수렴",
    "외과적","수정4","백본","스켈레톤","SHE","엘베피치","타임스톤",
    "맥가이버","넛지","프리모르템","트리아지","줌","절대자","틀밖",
    "부작업","주작업","제출청소","작업설계자","핑퐁","리허설","작업계획",
]

# 정식명 변형 (조사·표기·영문)
VARIANTS = {
    "제1원리": ["제1원리","제일원리"],
    "베이지안": ["베이지안","베이즈"],
    "수정4": ["수정4","수정레벨","EDIT4"],
    "틀밖": ["틀밖","틀 밖"],
    "핑퐁": ["핑퐁","ping pong","ping-pong","pingpong"],
    "리허설": ["리허설","rehearsal","dry run","dry-run"],
    "작업계획": ["작업계획","작업 계획"],
}
def variants_of(name):
    return VARIANTS.get(name, [name])

# ===== 유사 트리거 사전 (헤더 우측) =====
SIMILAR = {
    "홈즈":["트리아지","프리모르템","오컴"],
    "오컴":["홈즈","제1원리","연역수렴"],
    "제1원리":["백본","틀밖","연역수렴"],
    "베이지안":["홈즈","오컴","연역수렴"],
    "엄브렐러":["줌","절대자","아날로지"],
    "아날로지":["엄브렐러","줌","틀밖"],
    "연역수렴":["줌","홈즈","제1원리"],
    "외과적":["수정4","백본","스켈레톤"],
    "수정4":["외과적","백본","제출청소"],
    "백본":["제1원리","스켈레톤","엘베피치"],
    "스켈레톤":["제출청소","백본","엘베피치"],
    "SHE":["백본","스켈레톤","엘베피치"],
    "엘베피치":["스켈레톤","백본","SHE"],
    "타임스톤":["작업계획","백본","엘베피치"],
    "맥가이버":["트리아지","넛지","외과적"],
    "넛지":["맥가이버","SHE","작업설계자"],
    "제출청소":["스켈레톤","외과적","수정4"],
    "작업설계자":["작업계획","부작업","SHE"],
    "프리모르템":["홈즈","트리아지","리허설"],
    "트리아지":["홈즈","프리모르템","맥가이버"],
    "핑퐁":["리허설","트리아지","작업계획"],
    "리허설":["프리모르템","핑퐁","제출청소"],
    "작업계획":["작업설계자","타임스톤","트리아지"],
    "줌":["절대자","엄브렐러","연역수렴"],
    "절대자":["줌","엄브렐러","틀밖"],
    "틀밖":["제1원리","아날로지","절대자"],
    "부작업":["주작업","작업계획","작업설계자"],
    "주작업":["부작업","작업계획","타임스톤"],
}

# ===== 9 콤보 (일상어 + 정식 멤버) =====
COMBOS = [
    # (콤보명, [정식 멤버], [일상어 트리거 표현 + 콤보명 단독], [유사 콤보])
    ("미궁", ["백본","제1원리"], ["미궁","근본원리","근본적","본질적"], ["박스","복잡계"]),
    ("마비", ["트리아지","홈즈"], ["마비"], ["장밋빛폭주","카드없음"]),  # 선택 결합 룰도 유지
    ("시야", ["줌","절대자","엄브렐러"], ["시야","MECE"], ["복잡계","박스"]),
    ("벽", ["triz","오컴"], ["벽","혼돈"], ["카드없음","미궁"]),
    ("카드없음", ["맥가이버","triz"], ["카드없음","방법없음","방법없어","방법이 없"], ["마비","벽"]),
    ("장밋빛폭주", ["프리모르템","홈즈"], ["장밋빛폭주","실패의 핵심","실패의핵심"], ["마비","제출직전"]),
    ("제출직전", ["스켈레톤","제출청소"], ["제출직전","심플하게 제출","심플하게제출"], ["미궁","장밋빛폭주"]),
    ("복잡계", ["연역수렴","줌"], ["복잡계"], ["시야","미궁"]),
    ("박스", ["틀밖","제1원리"], ["박스","다시 생각","다시생각","처음부터 다시"], ["미궁","시야"]),
]

# ===== NOT 라우팅 =====
NOT_TERMS = ["TRIZ","triz","트리즈","이쁘니"]

# ===== 컨텍스트 마스킹 (오발동 차단) =====
def mask_quoted(s: str) -> str:
    """따옴표·백틱·홑따옴표 안의 내용을 공백으로 마스킹"""
    # "..." '...' `...` 「...」 『...』
    patterns = [
        r'"[^"]*"',
        r"'[^']*'",
        r'`[^`]*`',
        r'「[^」]*」',
        r'『[^』]*』',
    ]
    for p in patterns:
        s = re.sub(p, lambda m: ' ' * len(m.group(0)), s)
    return s

def mask_negation(s: str) -> str:
    """X 말고 / X 아니고 / X 빼고 / X 제외 → 직전 토큰 마스킹"""
    # 한국어: "백본 말고", "백본은 말고", "X말고"
    return re.sub(
        r'(\S+?)(\s*(?:은|는|이|가)?\s*(?:말고|아니고|빼고|제외하고|제외|말구))',
        lambda m: ' ' * len(m.group(1)) + m.group(2),
        s
    )

def mask_meta_question(s: str) -> str:
    """X가 뭐야 / X 뜻 / X라는 / X(은/는) ... 누구/어디/언제 → X 마스킹"""
    # 1) X(이/가/은/는)? 뭐야|뜻... — 직후
    s = re.sub(
        r'([가-힣A-Za-z0-9]+)(\s*(?:이|가|은|는)?\s*(?:뭐야|뭐죠|뭐임|뭔지|뭔데|뜻이|뜻은|뜻을|뜻이야|의미가|의미는|의미야))',
        lambda m: ' ' * len(m.group(1)) + m.group(2), s
    )
    # 2) X(이/가)? 라는|이라는 단어/용어/말/개념
    s = re.sub(
        r'([가-힣A-Za-z0-9]+)(\s*(?:이|가)?\s*(?:라는|이라는)\s*(?:단어|용어|말|개념|건|것))',
        lambda m: ' ' * len(m.group(1)) + m.group(2), s
    )
    # 3) X(은/는) ... 누구/어디/언제/왜 (문장 내 어디든)
    s = re.sub(
        r'([가-힣A-Za-z0-9]+)(은|는)(\s+[^?.!]*?(?:누구|어디|언제|왜|어떤|어떻게 생긴|생김))',
        lambda m: ' ' * len(m.group(1)) + m.group(2) + m.group(3), s
    )
    return s

def mask_not_terms(s: str) -> str:
    """NOT 라우팅 단어 마스킹 (다른 스킬로 가야 함)"""
    for t in NOT_TERMS:
        s = s.replace(t, ' ' * len(t))
    return s

def mask_all(s: str) -> str:
    s = mask_quoted(s)
    s = mask_negation(s)
    s = mask_meta_question(s)
    s = mask_not_terms(s)
    return s

# ===== 매칭 =====
def find_trigger_hits(masked: str):
    """마스킹된 텍스트에서 정식명 hit 찾기. 순서 보존."""
    hits = []
    for name in TRIGGERS:
        for v in variants_of(name):
            if v in masked:
                if name not in hits:
                    hits.append(name)
                break
    return hits

def find_combo_hit(masked: str, trigger_hits):
    """콤보 hit 찾기. 일상어 우선, 그 다음 멤버 동시 매칭."""
    # 1) 일상어 직접 매칭
    for cname, members, phrases, similar in COMBOS:
        for ph in phrases:
            if ph in masked:
                return (cname, members, similar)
    # 2) 특수 콤보 (멤버는 정식명 또는 키워드 동시)
    # 마비: "선택" + 막막함 표현 동시
    if "선택" in masked and any(k in masked for k in ["어떻게","어떡해","맞을까","맞나","많아","많은","고민","모르겠","어려워"]):
        for cname, members, phrases, similar in COMBOS:
            if cname == "마비":
                return (cname, members, similar)
    # 시야: "관점" 단독 (작업맥락 포함시만)
    if "관점" in masked and ("정리" not in masked):
        # 작업동사 동반 시
        if any(w in masked for w in ["분석","설계","진단","해결","기획","검토","봐줘","해줘","가자","하자"]):
            for cname, members, phrases, similar in COMBOS:
                if cname == "시야":
                    return (cname, members, similar)
    # 복잡계: "정리" + "관점" 동시
    if "정리" in masked and "관점" in masked:
        for cname, members, phrases, similar in COMBOS:
            if cname == "복잡계":
                return (cname, members, similar)
    # 3) 정식명 멤버 동시 매칭 (예: 백본+제1원리 → 미궁)
    if len(trigger_hits) >= 2:
        for cname, members, phrases, similar in COMBOS:
            # triz는 정식명 아님(NOT) → 멤버에 triz 있으면 스킵
            if "triz" in members:
                continue
            if all(m in trigger_hits for m in members):
                return (cname, members, similar)
    return None

# ===== 헤더 포맷 =====
def format_header(trigger_hits, combo):
    if combo:
        cname, members, similar = combo
        member_str = "+".join(members)
        sim_str = " · ".join(similar[:2])
        return f"🎯 {cname} ({member_str}) · 유사: {sim_str}"
    if len(trigger_hits) == 1:
        t = trigger_hits[0]
        sims = SIMILAR.get(t, [])[:3]
        return f"🎯 {t} · " + " · ".join(sims) if sims else f"🎯 {t}"
    if len(trigger_hits) >= 2:
        # 콤보 매칭 안 된 복수 hit
        head = "+".join(trigger_hits[:2])
        # 첫 트리거의 유사로 채움
        sims = SIMILAR.get(trigger_hits[0], [])[:2]
        sim_str = " · ".join(sims)
        return f"🎯 {head} · 유사: {sim_str}"
    return ""

# ===== 메인 =====
def scan(message: str) -> str:
    """입력 → 헤더 1줄 또는 빈 문자열."""
    if not message or not message.strip():
        return ""
    masked = mask_all(message)
    trigger_hits = find_trigger_hits(masked)
    combo = find_combo_hit(masked, trigger_hits)
    if not trigger_hits and not combo:
        return ""
    return format_header(trigger_hits, combo)

def main():
    if len(sys.argv) < 2:
        print("Usage: trigger_scanner.py <message> | trigger_scanner.py -", file=sys.stderr)
        sys.exit(2)
    arg = sys.argv[1]
    if arg == "-":
        msg = sys.stdin.read()
    else:
        msg = " ".join(sys.argv[1:])
    out = scan(msg)
    if out:
        print(out)

if __name__ == "__main__":
    main()
