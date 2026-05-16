#!/usr/bin/env python3
"""
GPT vs Claude 격투장 — SSAFY GMS 프록시 사용
==============================================
같은 도전과제를 두 모델에 보내고, 심판 모델이 승패를 가린다.

실행:
  python3 gladiator.py                                     # 기본 (gpt-5 심판)
  python3 gladiator.py --judge claude-sonnet-4-5           # Claude 심판
  python3 gladiator.py --judge gemini-2.5-flash            # Gemini 심판
  python3 gladiator.py --challenges f1.json f2.json        # 여러 파일 합치기
  python3 gladiator.py --tag round2 --budget 20000         # 세션 이름 + 예산
  python3 gladiator.py --only code-1                       # 한 챌린지만
  python3 gladiator.py --dry-run                           # 비용 추산만
"""
import argparse, json, os, sys, time
from datetime import datetime
from pathlib import Path
import httpx

# ── 키 로드 ───────────────────────────────────────
def _load_key() -> str:
    k = os.environ.get("OPENAI_API_KEY", "").strip()
    if k and not k.startswith("PASTE_"):
        return k
    env_path = Path.home() / ".hermes" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("OPENAI_API_KEY="):
                v = line.split("=", 1)[1].strip().strip('"').strip("'")
                if v and not v.startswith("PASTE_"):
                    return v
    sys.exit("❌ OPENAI_API_KEY 미설정. ~/.hermes/.env 확인.")

KEY = _load_key()

# ── 엔드포인트 & 비용표 ───────────────────────────
GMS_OPENAI = "https://gms.ssafy.io/gmsapi/api.openai.com/v1"
GMS_ANTHROPIC = "https://gms.ssafy.io/gmsapi/api.anthropic.com/v1"
GMS_GEMINI = "https://gms.ssafy.io/gmsapi/generativelanguage.googleapis.com/v1beta"

# SSAFY GMS 가이드 기준 평균 credit/call
COST = {
    "gpt-5.2": 20, "gpt-5": 20, "gpt-5-mini": 5, "gpt-5-nano": 1,
    "claude-opus-4-5-20251101": 50,
    "claude-sonnet-4-5-20250929": 30,
    "claude-haiku-4-5-20251001": 10,
    "gemini-2.5-flash": 30, "gemini-2.5-flash-lite": 1, "gemini-2.5-pro": 30,
}

# 모델 ID로 종류 자동 판별
def _kind_of(model_id: str) -> str:
    if model_id.startswith("gpt") or model_id.startswith("o3"):
        return "openai"
    if model_id.startswith("claude"):
        return "anthropic"
    if model_id.startswith("gemini") or model_id.startswith("imagen"):
        return "gemini"
    raise ValueError(f"알 수 없는 모델: {model_id}")

# 심판 alias → 실제 model id
JUDGE_ALIASES = {
    "gpt-5": "gpt-5",
    "claude-sonnet-4-5": "claude-sonnet-4-5-20250929",
    "claude-haiku-4-5": "claude-haiku-4-5-20251001",
    "gemini-2.5-flash": "gemini-2.5-flash",
    "gemini-2.5-flash-lite": "gemini-2.5-flash-lite",
}

# ── 파이터 (고정) ─────────────────────────────────
FIGHTER_A = {"name": "GPT-5.2", "model": "gpt-5.2", "kind": "openai"}
FIGHTER_B = {"name": "Claude-Opus-4.5", "model": "claude-opus-4-5-20251101", "kind": "anthropic"}

ROOT = Path(__file__).parent
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ── API 호출 ──────────────────────────────────────
def call_openai(model: str, prompt: str, system: str = None) -> str:
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": prompt})
    body = {"model": model, "messages": msgs}
    # gpt-5 family는 temperature 커스텀 거부
    r = httpx.post(
        f"{GMS_OPENAI}/chat/completions",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        json=body, timeout=180,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def call_anthropic(model: str, prompt: str, system: str = None) -> str:
    body = {"model": model, "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]}
    if system:
        body["system"] = system
    r = httpx.post(
        f"{GMS_ANTHROPIC}/messages",
        headers={"x-api-key": KEY, "anthropic-version": "2023-06-01",
                 "Content-Type": "application/json"},
        json=body, timeout=180,
    )
    r.raise_for_status()
    return r.json()["content"][0]["text"]

def call_gemini(model: str, prompt: str, system: str = None) -> str:
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    r = httpx.post(
        f"{GMS_GEMINI}/models/{model}:generateContent",
        headers={"x-goog-api-key": KEY, "Content-Type": "application/json"},
        json=body, timeout=180,
    )
    r.raise_for_status()
    data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def call(spec: dict, prompt: str, system: str = None) -> str:
    if spec["kind"] == "openai":
        return call_openai(spec["model"], prompt, system)
    if spec["kind"] == "anthropic":
        return call_anthropic(spec["model"], prompt, system)
    if spec["kind"] == "gemini":
        return call_gemini(spec["model"], prompt, system)
    raise ValueError(f"unknown kind: {spec['kind']}")

# ── 심판 ──────────────────────────────────────────
JUDGE_SYSTEM = """너는 두 LLM 답변을 비교 평가하는 공정한 심판이다.
- 어느 쪽이 더 나은지(A/B/무승부) 판정하고
- 왜 그렇게 판정했는지 1~2문장으로 설명한다
- 감점 요인이 있으면 명시한다
- 중요: 모델 가족/스타일/길이로 편향되지 말고 오직 문제 요구사항 충족도와 품질로 판단
- 출력 형식은 반드시:
  WINNER: A | B | TIE
  REASON: <한 줄 설명>"""

def judge_round(judge_spec: dict, challenge: dict, ans_a: str, ans_b: str) -> dict:
    prompt = f"""[Challenge]
이름: {challenge['name']}
카테고리: {challenge['category']}
문제: {challenge['prompt']}

[A의 답변]
{ans_a}

[B의 답변]
{ans_b}

판정해라."""
    out = call(judge_spec, prompt, system=JUDGE_SYSTEM)
    winner = "TIE"
    for line in out.splitlines():
        if line.upper().startswith("WINNER:"):
            v = line.split(":", 1)[1].strip().upper().rstrip(".")
            if v in ("A", "B", "TIE"):
                winner = v
                break
    return {"winner": winner, "raw": out}

# ── 메인 ──────────────────────────────────────────
def estimate_cost(n: int, judge_model: str) -> int:
    a = COST.get(FIGHTER_A["model"], 30)
    b = COST.get(FIGHTER_B["model"], 50)
    j = COST.get(judge_model, 30)
    return n * (a + b + j)

def run_round(challenge: dict, judge_spec: dict, log_path: Path) -> dict:
    print(f"  → {FIGHTER_A['name']} 응답 중...", flush=True)
    t0 = time.time()
    ans_a = call(FIGHTER_A, challenge["prompt"])
    print(f"    완료 ({time.time()-t0:.1f}s)", flush=True)

    print(f"  → {FIGHTER_B['name']} 응답 중...", flush=True)
    t0 = time.time()
    ans_b = call(FIGHTER_B, challenge["prompt"])
    print(f"    완료 ({time.time()-t0:.1f}s)", flush=True)

    print(f"  → 심판 {judge_spec['name']} 판정 중...", flush=True)
    j = judge_round(judge_spec, challenge, ans_a, ans_b)
    print(f"    승자: {j['winner']}", flush=True)

    md = f"""# {challenge['name']}  ({challenge['category']})

**문제**
> {challenge['prompt']}

## 🅰️  {FIGHTER_A['name']}
{ans_a}

## 🅱️  {FIGHTER_B['name']}
{ans_b}

## ⚖️  심판 ({judge_spec['name']})
{j['raw']}
"""
    log_path.write_text(md, encoding="utf-8")
    return {"id": challenge["id"], "category": challenge["category"], "winner": j["winner"]}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--challenges", nargs="+", default=[str(ROOT / "challenges.json")],
                   help="챌린지 JSON 파일들 (여러 개 가능 — 합쳐짐)")
    p.add_argument("--judge", default="gpt-5",
                   help=f"심판 모델 alias 또는 model id. alias: {list(JUDGE_ALIASES.keys())}")
    p.add_argument("--tag", default=None, help="결과 디렉토리 접미사 (없으면 timestamp만)")
    p.add_argument("--only", help="한 챌린지 ID만 실행")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--budget", type=int, default=10000, help="누적 credit 한도")
    args = p.parse_args()

    # 심판 spec 만들기
    judge_model = JUDGE_ALIASES.get(args.judge, args.judge)
    judge_spec = {
        "name": args.judge.upper().replace("-", "_"),
        "model": judge_model,
        "kind": _kind_of(judge_model),
    }

    # 챌린지 로드 & 합치기
    challenges = []
    for cf in args.challenges:
        path = Path(cf)
        if not path.exists():
            sys.exit(f"❌ 챌린지 파일 없음: {cf}")
        challenges.extend(json.loads(path.read_text()))
    # id 중복 체크
    seen_ids = set()
    dedup = []
    for c in challenges:
        if c["id"] not in seen_ids:
            dedup.append(c)
            seen_ids.add(c["id"])
    challenges = dedup

    if args.only:
        challenges = [c for c in challenges if c["id"] == args.only]
        if not challenges:
            sys.exit(f"❌ ID '{args.only}' 못 찾음")

    cost_estimate = estimate_cost(len(challenges), judge_model)
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"심판 모델  : {judge_spec['name']} ({judge_model})")
    print(f"챌린지 수  : {len(challenges)}")
    print(f"예상 비용  : 약 {cost_estimate:,} credit (라운드당 {cost_estimate//len(challenges):,})")
    print(f"예산 한도  : {args.budget:,} credit")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    if cost_estimate > args.budget:
        sys.exit(f"❌ 예상 비용이 예산을 초과. --budget 올리거나 챌린지 수 줄이기.")

    if args.dry_run:
        print("(dry-run, 실제 호출 없음)")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = f"_{args.tag}" if args.tag else ""
    session_dir = RESULTS_DIR / f"battle_{timestamp}{suffix}"
    session_dir.mkdir()

    results = []
    for i, c in enumerate(challenges, 1):
        print(f"\n[{i}/{len(challenges)}] {c['id']} — {c['name']}")
        try:
            r = run_round(c, judge_spec, session_dir / f"{c['id']}.md")
            results.append(r)
        except Exception as e:
            print(f"  ❌ 에러: {e}")
            results.append({"id": c["id"], "category": c["category"], "winner": "ERROR", "error": str(e)})

    # 요약
    wins_a = sum(1 for r in results if r["winner"] == "A")
    wins_b = sum(1 for r in results if r["winner"] == "B")
    ties = sum(1 for r in results if r["winner"] == "TIE")
    errors = sum(1 for r in results if r["winner"] == "ERROR")

    # 카테고리별 집계
    from collections import defaultdict
    by_cat = defaultdict(lambda: {"A": 0, "B": 0, "TIE": 0, "ERROR": 0})
    for r in results:
        by_cat[r["category"]][r["winner"]] += 1

    summary = f"""# 🏆 GPT vs Claude 격투장 결과

날짜: {timestamp}
모델 A: {FIGHTER_A['name']} ({FIGHTER_A['model']})
모델 B: {FIGHTER_B['name']} ({FIGHTER_B['model']})
심판  : {judge_spec['name']} ({judge_model})

## 최종 스코어
- 🅰️ A 승: **{wins_a}**
- 🅱️ B 승: **{wins_b}**
- 🤝 무승부: {ties}
- ❌ 에러: {errors}

## 카테고리별
| 카테고리 | A | B | TIE | ERR |
|---|---|---|---|---|
"""
    for cat in sorted(by_cat):
        s = by_cat[cat]
        summary += f"| {cat} | {s['A']} | {s['B']} | {s['TIE']} | {s['ERROR']} |\n"

    summary += "\n## 라운드별 결과\n| ID | 카테고리 | 승자 |\n|---|---|---|\n"
    for r in results:
        emoji = {"A": "🅰️ A", "B": "🅱️ B", "TIE": "🤝", "ERROR": "❌"}.get(r["winner"], "?")
        summary += f"| {r['id']} | {r['category']} | {emoji} |\n"

    summary_path = session_dir / "_SUMMARY.md"
    summary_path.write_text(summary, encoding="utf-8")

    # JSON으로도 저장 (분석 sub-agent가 읽기 쉽게)
    json_path = session_dir / "_results.json"
    json_path.write_text(json.dumps({
        "timestamp": timestamp,
        "judge": {"name": judge_spec["name"], "model": judge_model, "kind": judge_spec["kind"]},
        "fighter_a": FIGHTER_A,
        "fighter_b": FIGHTER_B,
        "totals": {"A": wins_a, "B": wins_b, "TIE": ties, "ERROR": errors},
        "by_category": dict(by_cat),
        "results": results,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✓ 완료. 결과: {session_dir}")
    print(f"  최종: A {wins_a} - {wins_b} B  (무 {ties}, 에러 {errors})")

if __name__ == "__main__":
    main()
