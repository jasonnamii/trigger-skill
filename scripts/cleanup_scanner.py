#!/usr/bin/env python3
"""
cleanup_scanner.py v2.0 — 제출청소 14축 결정주의 스캐너

trigger_scanner.py의 자매 모듈. 외부 제출 문서를 14축 + 7서브슬롯으로 일괄 스캔.
LLM 판단 0% (오탐 제외·치환 생성은 Claude 수동). 모든 grep/regex 매칭은 본 스크립트가.

Usage:
    python3 cleanup_scanner.py <대상파일.md>          # 14축 전체 스캔
    python3 cleanup_scanner.py <대상파일.md> --axis 14 # 축14만
    python3 cleanup_scanner.py <대상파일.md> --json    # JSON 출력
"""

import re
import sys
import json
import os
from collections import OrderedDict

# ===== 축 1~13 패턴 (기존 protocol-cleanup.md verbatim) =====
AXES_1_TO_13 = OrderedDict([
    ("1_헤더메타", r"changelog|변경이력|revision history|작성자:|author:|검토자:|승인자:|문서번호|doc.?id|draft|검토중|승인대기|내부용|대외비|confidential|internal.?only"),
    ("2_체인지로그", r"변경이력|변경사항|수정이력|수정내역|[Cc]hange.?[Ll]og|[Rr]evision|[Hh]istory|[Rr]elease.?[Nn]otes|이전\s*버전|기존안\s*대비|v\d+.*에서\s*(수정|변경|추가)"),
    ("3_내부언어", r"확신도|MECE|스파인|spine|트리아지|갭렌즈|절대자|C8C|DC\b|OK\b|UP\b|SHE\b|엄브렐러|홈즈|오컴|제1원리|베이지안|모순기술|아날로지|연역수렴|외과적|백본|스켈레톤|엘베피치|엘리베이터\s*피치|타임스톤|맥가이버|넛지|프리모르템|줌\b|부작업|주작업|제출청소|이쁘니|작업설계자|모래시계|렌즈6|ceo-pipeline|policy-planning|bp-guide|financial-model|UP\s*§|§[A-H]\b|§AI\b|§A-[0-9]|§[A-Z]+-?[0-9]*|샤워효과|[0-9]+(축|건|대|종|개|차원|영역|항목)|축별|축\s*[0-9]|다축|수렴축|N대\s*(동인|요인|원칙|패턴|원리)|[0-9]+건\s*(수정|보강|채택|삭제|추가)|대조판정|교차검증|독립\s*리서치|보강\s*리서치|팩트시트|팩트\s*베이스|Phase\s*[0-9]|P[0-9]\b|MUST\b|SHOULD\b|MAY\b|SCOPE_OUT|자체검사|자체점검|연역수렴\s*도출|제약\s*역전|자원\s*재조합|[0-9]+층|[Ll]ayer\s*[0-9]|레이어\s*[0-9]|[0-9]+[대개종]?\s*(패턴|원리|원칙|공식|렌즈|도메인|시나리오|메타원리|매트릭스)|축별\s*(조사|분석|통찰)|L[0-4]\s*(교차|통찰|연역)|공식[①-⑥]|스크리닝|게이트\s*(통과|판정)|폴백|스포크\s*(로드|로딩)|허브\s*스포크|LIGHT\b|DEEP\b|TURBO\b|낙관.?기본.?비관|도메인\s*(라우팅|어댑터|판별)|TRIZ|트리즈|인물\s*동학|조직\s*동학|시장\s*동학|DNA\b|경력\s*DNA"),
    ("4_AI흔적_모델명만", r"Python검증|확신도\s*\d|Co-Authored|Claude|GPT|LLM|서브에이전트|sub-agent|Anthropic|Copilot|ChatGPT|OpenAI|AI\s*생성|generated.?by|AI.?assisted|검증\s*완료|QC\s*통과|클로드|인공지능\s*생성"),
    ("5_작업마커", r"TODO|FIXME|TBD|WIP|⚠️|❓|\[ \]|HACK|PENDING|BLOCKED|미완|미정|확인\s*필요|검토\s*필요|보류|작성중|🚧|\[/\]|\[-\]"),
    ("6_플레이스홀더", r"\[여기에|\(추후|XXX|TBA|삽입\]|INSERT.?HERE|PLACEHOLDER|FILL.?IN|작성\s*예정|추가\s*예정|확인\s*후\s*기재|\{\{|\}\}|\[OO|lorem ipsum"),
    ("7_톤격식", r"~해\b|~야\b|~거든|~잖아|ㅋㅋ|ㅎㅎ|근데\b|걍\b|도움이\s*되셨|우리가\b|내부적으로|FYI\b|BTW\b"),
    ("8_코드주석", r"<!--|-->|%%|console\.(log|warn|error|debug|info|table|dir)|alert\(|debugger\b|dataview|templater|<%|%>"),
    ("9_프론트매터", r"^---|tags:|aliases:"),
    ("10_버전흔적", r"_draft|_old|_backup|_사본|_검토용|_내부용|_temp|_test|_sample|Draft\s*\d|이전\s*버전\s*대비|기존안\s*대비"),
    ("11_내부경로", r"/Users/|/sessions/|/mnt/|C:\\\\|D:\\\\|/home/|/tmp/|localhost|127\.0\.0\.1|192\.168\.|10\.0\.|\.internal\b"),
    ("12_포맷정합", None),  # 수동
    ("13_숫자정합", r"\d+[,.]?\d*\s*(원|만|억|조|달러|위안|RMB|USD|EUR|JPY|%)"),
])

# ===== 축 14 — 7서브슬롯 (ai-not-canon.md verbatim 패턴) =====

AXIS_14_SLOTS = OrderedDict([
    # 14a. 미사여구·컨설팅투
    ("14a_미사여구_컨설팅투", [
        # 미사여구
        r"혁신적\b", r"차세대\b", r"포용적\b", r"전사적\b", r"윈윈\b", r"유기적\b", r"역동적\b",
        r"다각도로\b", r"다층적으로\b", r"전례\s*없는", r"지속\s*가능한", r"차별화된\b",
        # 컨설팅투
        r"솔루션\s*기반", r"전략적\s*파트너", r"고객\s*중심", r"체계적이고\b", r"필수적인\b", r"선도적인\b",
        # 관계UX
        r"원활한\b", r"긴밀히\b", r"적극적인\b", r"종합적인\b", r"건설적\b", r"지속적인\b", r"효과적인\b",
        r"사용자\s*친화적", r"직관적이고\b", r"최적화된\b", r"사용자\s*경험을\s*향상",
        # 형식주의 부사
        r"본질적으로\b", r"근본적으로\b", r"구체적으로\b", r"전반적으로\b", r"점진적으로\b",
        r"효과적으로\b", r"효율적으로\b", r"전략적으로\b", r"혁신적으로\b", r"지속적으로\b",
    ]),
    # 14b. 한자투·번역투
    ("14b_한자투_번역투", [
        r"에\s*대한\b", r"에\s*대해\b", r"에\s*대하여\b",
        r"을\s*통[해하]", r"를\s*통[해하]", r"통하여\b",
        r"로\s*인[해하]\b", r"으로\s*인[해하]\b", r"인하여\b",
        r"에\s*의[해하]\b", r"에\s*의하여\b",
        r"함으로써\b", r"음으로써\b",
        r"에\s*있어서\b", r"함에\s*있어\b", r"음에\s*있어\b",
        r"로부터\b", r"으로부터\b",
        r"되어진다\b", r"되어졌다\b", r"될\s*수\s*있다", r"어져야\s*한다", r"아져야\s*한다",
        r"에\s*다름\s*아니다",
        r"이루어지고\s*있는", r"탑승하고\s*있던", r"작용하기엔\b",
        r"현\s*상황\s*속에서",
    ]),
    # 14c. 자신없는 어미
    ("14c_자신없는어미", [
        r"같다\b", r"같습니다\b", r"같아요\b",
        r"인\s*듯\b", r"인\s*듯하다\b",
        r"지\s*않을까\b",
        r"수도\s*있다\b", r"수\s*있을\s*것", r"수\s*있을지", 
        r"로\s*보인다\b", r"로\s*보입니다\b",
        r"인\s*것\s*같다", r"라고\s*한다\b", r"인\s*것이다\b",
        r"이\s*아닌가\s*싶다",
        r"할\s*것인\s*것\s*같다", r"인지도\s*모른다\b",
        r"언젠가\b", r"어디선가\b",
    ]),
    # 14d. 것·도·등 남용
    ("14d_것남용", [
        r"것이다\b", r"것입니다\b",
        r"것은\b", r"것을\b", r"것이\b",
        r"것으로\s*보인다", r"수\s*있는\s*것이\s*있다",
        r"수\s*있다고\s*본다", r"할\s*필요가\s*있다",
        r"하는\s*것이\s*중요하다",
        r"라는\s*점에서\b", r"를\s*통하여\b",
        r"하는\s*것이다\b", r"한다는\s*것은\b",
        r"이라는\s*것\b", r"라는\s*것\b",
    ]),
    # 14e. 강조부사 BAN
    ("14e_강조부사", [
        r"매우\b", r"너무\b", r"정말로\b", r"꽤\b", r"완전\b", 
        r"대단히\b", r"아주\b", r"진짜로\b", r"상당히\b",
        r"너무나\b", r"굉장히\b", r"엄청나게\b", r"무척\b",
    ]),
    # 14f. AI 메타·관계 어휘
    ("14f_AI메타_관계어휘", [
        # AI 메타
        r"박제\b", r"박다\b", r"박혀\b", r"박힌\b", r"새기다\b",
        # 약 BAN (hit≥2 = 재작성)
        r"여러분의\b", r"진정한\b", r"또한\b", r"그러므로\b", r"한편\b",
        r"유연하게\b", r"다양한\b", r"여러\b",
        # 동의어 나열
        r"각종\b", r"다채로운\b",
        # 작업라벨 (산출물 잔존 시)
        r"[0-9]+축\b", r"[0-9]+레이어\b", r"[0-9]+트랙\b",
        r"Phase\s*[0-9]+", r"페이즈\s*[0-9]+", r"레이어\s*[0-9]+",
        r"축별\b", r"다축\b", r"수렴축\b",
        r"차원이\b", r"차원에서\b", r"영역에서\b", r"관점에서\b", r"측면에서\b",
        r"종류로\b", r"범주로\b", r"항목으로\b", r"구분으로\b",
        # 메타코드
        r"\bP[0-9]\b", r"\bMUST\b", r"\bSHOULD\b", r"\bMAY\b",
        r"\bSCOPE_OUT\b", r"\bSCOPE_IN\b",
        r"\bLIGHT\b", r"\bDEEP\b", r"\bTURBO\b",
        # 동학어휘
        r"인물\s*동학", r"조직\s*동학", r"시장\s*동학",
        r"경력\s*DNA", r"조직\s*DNA",
        # 자체언급
        r"자체검사\b", r"자체점검\b",
        # 숫자카운터
        r"[0-9]+\s*(축|건|대|종|개|차원|영역|항목|측면|관점|종류|범주|갈래|방면|국면|요소|구분)\b",
    ]),
    # 14g. AI 사족·과잉공손
    ("14g_AI사족_과잉공손", [
        # 결론 사족
        r"결론적으로\b", r"요약하면\b", r"정리하면\b", r"요컨대\b", r"한마디로\b",
        # 우회 단정
        r"라고\s*할\s*수\s*있다", r"라고\s*볼\s*수\s*있다", r"할\s*수\s*있다고\s*본다",
        # 강조 사족
        r"주목할\s*만한", r"강조할\s*필요가\s*있다", r"다시\s*한번\s*강조하면",
        # 접속 비대
        r"더욱이\b", r"게다가\b", r"나아가\b",
        r"이에\s*따라", r"이를\s*통해", r"이러한\s*점에서", r"이와\s*관련하여",
        r"따라서\b",
        # AI 공손 사족
        r"도움이\s*되셨", r"추가\s*질문이", r"이해하기\s*쉽게", r"말씀드리자면",
        # 자가합리화
        r"프레임이라\s*유지", r"숫자\s*없으니\s*OK", r"이번엔\s*예외",
        r"일상어\b", r"의미상\s*OK", r"메타라\s*OK",
        # 과잉감정
        r"제일\s*먼저", r"것은\s*물론", r"할\s*정도로", r"심지어\b", r"마치\s*.{1,5}처럼",
    ]),
])

# ===== ALLOW (BAN 면제·형 시그니처) =====
ALLOW_TOKENS = set([
    # 형 시그니처 부사
    "정말", "확실히", "진짜", "딱", "솔직히", "사실", "근데", "그냥", "왜", "어떻게",
    # 형 시그니처 명사
    "이유", "기준", "핵심", "방식", "차이", "요소", "역할", "방법", "조건",
    # 업계 표준
    "BEP", "KPI", "MECE", "MVP",
    # 마케팅 업계어
    "패러다임", "최적화", "플랫폼", "콘텐츠", "캠페인", "브랜드", "타겟팅", "다이렉트", "퍼포먼스",
])

# ===== 스캔 함수 =====

def scan_axis(text: str, pattern: str):
    """단일 정규식으로 라인·컬럼 매칭 추출"""
    if pattern is None:
        return []
    hits = []
    try:
        regex = re.compile(pattern, re.MULTILINE)
    except re.error as e:
        return [{"error": str(e)}]
    for line_no, line in enumerate(text.splitlines(), start=1):
        for m in regex.finditer(line):
            matched = m.group(0)
            # ALLOW 면제 검사
            if matched.strip() in ALLOW_TOKENS:
                continue
            hits.append({
                "line": line_no,
                "col": m.start() + 1,
                "match": matched,
                "context": line.strip()[:80],
            })
    return hits

def scan_axis_14(text: str):
    """축14 — 7서브슬롯별 분리 스캔"""
    result = OrderedDict()
    for slot_name, patterns in AXIS_14_SLOTS.items():
        slot_hits = []
        for pat in patterns:
            try:
                regex = re.compile(pat, re.MULTILINE)
            except re.error:
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                for m in regex.finditer(line):
                    matched = m.group(0)
                    if matched.strip() in ALLOW_TOKENS:
                        continue
                    slot_hits.append({
                        "line": line_no,
                        "col": m.start() + 1,
                        "match": matched,
                        "pattern": pat,
                        "context": line.strip()[:80],
                    })
        result[slot_name] = slot_hits
    return result

def scan_full(text: str):
    """14축 전수 스캔"""
    out = OrderedDict()
    for axis_name, pattern in AXES_1_TO_13.items():
        out[axis_name] = scan_axis(text, pattern)
    out["14_AI아님_종합"] = scan_axis_14(text)
    return out

# ===== 출력 포맷 =====

def format_table(scan_result):
    """14행 고정 테이블 출력"""
    lines = []
    lines.append("| # | 축 | grep 건수 | 비고 |")
    lines.append("|---|---|-----------|------|")
    for i, (axis, hits) in enumerate(scan_result.items(), start=1):
        if i == 14:
            # 축14는 서브슬롯 합산
            total = sum(len(v) for v in hits.values())
            note_parts = [f"{k.split('_',1)[1]}={len(v)}" for k, v in hits.items() if v]
            note = " · ".join(note_parts) if note_parts else "all clear"
            mark = "✅" if total == 0 else "⚠️"
            lines.append(f"| {i} | {axis} | {mark} {total}건 | {note} |")
        else:
            n = len(hits)
            mark = "✅" if n == 0 else "⚠️"
            note = "수동 대조" if axis == "12_포맷정합" else ("Python 검증" if axis == "13_숫자정합" else "")
            lines.append(f"| {i} | {axis} | {mark} {n}건 | {note} |")
    return "\n".join(lines)

def format_axis_14_detail(axis_14_hits):
    """축14 서브슬롯 상세"""
    lines = []
    lines.append("\n## 축14 AI아님 종합 — 서브슬롯 상세\n")
    for slot, hits in axis_14_hits.items():
        if not hits:
            continue
        lines.append(f"### {slot} ({len(hits)}건)\n")
        for h in hits[:20]:  # 슬롯당 최대 20건
            lines.append(f"- L{h['line']}:{h['col']} `{h['match']}` — {h['context']}")
        if len(hits) > 20:
            lines.append(f"- ... ({len(hits)-20}건 더)")
        lines.append("")
    return "\n".join(lines)

def format_text_report(scan_result, file_path):
    parts = []
    parts.append(f"# 제출청소 14축 스캔 — {os.path.basename(file_path)}\n")
    parts.append(format_table(scan_result))
    # 축14 상세
    if any(scan_result["14_AI아님_종합"].values()):
        parts.append(format_axis_14_detail(scan_result["14_AI아님_종합"]))
    # 축 1~13 상세 (실건수 ≥ 1)
    for axis, hits in scan_result.items():
        if axis == "14_AI아님_종합":
            continue
        if isinstance(hits, list) and hits:
            parts.append(f"\n### {axis} ({len(hits)}건)\n")
            for h in hits[:15]:
                if "error" in h:
                    parts.append(f"- ERROR: {h['error']}")
                    continue
                parts.append(f"- L{h['line']}:{h['col']} `{h['match']}` — {h['context']}")
            if len(hits) > 15:
                parts.append(f"- ... ({len(hits)-15}건 더)")
    parts.append("\n---\n다음: 오탐 제외 + 변환안 생성 → 형 승인 → 일괄 적용 → 재스캔")
    return "\n".join(parts)

# ===== 메인 =====

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    
    file_path = args[0]
    output_json = "--json" in args
    only_axis = None
    if "--axis" in args:
        idx = args.index("--axis")
        if idx + 1 < len(args):
            only_axis = args[idx + 1]
    
    if not os.path.exists(file_path):
        print(f"ERROR: file not found — {file_path}", file=sys.stderr)
        sys.exit(2)
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    if only_axis == "14":
        result = {"14_AI아님_종합": scan_axis_14(text)}
    else:
        result = scan_full(text)
    
    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text_report(result, file_path))

if __name__ == "__main__":
    main()
