#!/usr/bin/env python3
"""
LogicKor 멀티턴 fighter 실행기 — 각 entry의 2턴 대화를 두 모델에 시키고 저장.

Output: results/logickor_fights/<id>.json
  {"id":..., "category":..., "questions":[Q1,Q2],
   "a": {"model": "...", "answers":[A1,A2]},
   "b": {"model": "...", "answers":[B1,B2]}}

다음 단계: logickor_judge.py 로 채점
"""
import argparse, json, os, sys, time
from datetime import datetime
from pathlib import Path
import httpx

sys.path.insert(0, str(Path(__file__).parent))
from gladiator import KEY, GMS_OPENAI, GMS_ANTHROPIC, GMS_GEMINI, COST, _kind_of

# ── 멀티턴 호출 ────────────────────────────────────
def call_openai_multi(model: str, messages: list) -> str:
    r = httpx.post(
        f"{GMS_OPENAI}/chat/completions",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        json={"model": model, "messages": messages}, timeout=180,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def call_anthropic_multi(model: str, messages: list) -> str:
    r = httpx.post(
        f"{GMS_ANTHROPIC}/messages",
        headers={"x-api-key": KEY, "anthropic-version": "2023-06-01",
                 "Content-Type": "application/json"},
        json={"model": model, "max_tokens": 4096, "messages": messages},
        timeout=180,
    )
    r.raise_for_status()
    return r.json()["content"][0]["text"]

def call_multi(spec: dict, messages: list) -> str:
    if spec["kind"] == "openai":
        return call_openai_multi(spec["model"], messages)
    if spec["kind"] == "anthropic":
        return call_anthropic_multi(spec["model"], messages)
    raise ValueError(f"멀티턴 미지원: {spec['kind']}")

# ── Fighter spec ──────────────────────────────────
FIGHTER_A = {"name": "GPT-5.2", "model": "gpt-5.2", "kind": "openai"}
FIGHTER_B = {"name": "Claude-Opus-4.5", "model": "claude-opus-4-5-20251101", "kind": "anthropic"}

# ── 한 엔트리 실행 ────────────────────────────────
def run_entry(entry: dict) -> dict:
    """Q1 답변 → Q2 답변 (양 fighter)"""
    q1, q2 = entry["questions"][:2]  # 일부 entry는 3개 — 처음 2개만 사용

    print(f"  → {FIGHTER_A['name']} Q1...", flush=True, end=""); t0 = time.time()
    a1 = call_multi(FIGHTER_A, [{"role": "user", "content": q1}])
    print(f" ({time.time()-t0:.1f}s)  Q2...", flush=True, end=""); t0 = time.time()
    a2 = call_multi(FIGHTER_A, [
        {"role": "user", "content": q1},
        {"role": "assistant", "content": a1},
        {"role": "user", "content": q2},
    ])
    print(f" ({time.time()-t0:.1f}s)", flush=True)

    print(f"  → {FIGHTER_B['name']} Q1...", flush=True, end=""); t0 = time.time()
    b1 = call_multi(FIGHTER_B, [{"role": "user", "content": q1}])
    print(f" ({time.time()-t0:.1f}s)  Q2...", flush=True, end=""); t0 = time.time()
    b2 = call_multi(FIGHTER_B, [
        {"role": "user", "content": q1},
        {"role": "assistant", "content": b1},
        {"role": "user", "content": q2},
    ])
    print(f" ({time.time()-t0:.1f}s)", flush=True)

    return {
        "id": entry["id"],
        "category": entry["category"],
        "questions": entry["questions"],
        "references": entry.get("references"),
        "a": {"model": FIGHTER_A["model"], "name": FIGHTER_A["name"], "answers": [a1, a2]},
        "b": {"model": FIGHTER_B["model"], "name": FIGHTER_B["name"], "answers": [b1, b2]},
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--questions", default="logickor_questions.jsonl")
    p.add_argument("--out", default="results/logickor_fights")
    p.add_argument("--only", type=int, help="특정 id만 실행")
    p.add_argument("--budget", type=int, default=10000)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--resume", action="store_true", help="기존 결과 건너뛰기")
    args = p.parse_args()

    ROOT = Path(__file__).parent
    questions_path = ROOT / args.questions
    entries = [json.loads(l) for l in open(questions_path)]
    if args.only:
        entries = [e for e in entries if e["id"] == args.only]

    a_cost = COST.get(FIGHTER_A["model"], 20)
    b_cost = COST.get(FIGHTER_B["model"], 50)
    per_entry = 2 * (a_cost + b_cost)  # 2턴 × 2 fighter
    total = per_entry * len(entries)

    out_dir = ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    # resume: 이미 있는 id 건너뛰기
    if args.resume:
        existing = {int(f.stem) for f in out_dir.glob("*.json")}
        entries = [e for e in entries if e["id"] not in existing]
        total = per_entry * len(entries)

    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Entry 수    : {len(entries)} (각 2턴)")
    print(f"비용/entry  : {per_entry} credit (A: 2×{a_cost} + B: 2×{b_cost})")
    print(f"예상 총 비용: {total:,} credit")
    print(f"예산 한도   : {args.budget:,} credit")
    print(f"출력        : {out_dir}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    if total > args.budget:
        sys.exit(f"❌ 예산 초과")
    if args.dry_run:
        print("(dry-run)")
        return

    for i, e in enumerate(entries, 1):
        print(f"\n[{i}/{len(entries)}] id={e['id']}  {e['category']}")
        try:
            result = run_entry(e)
            (out_dir / f"{e['id']:02d}.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  ✓ 저장: {e['id']:02d}.json")
        except Exception as ex:
            print(f"  ❌ 에러: {ex}")

    print(f"\n✓ 완료. 다음 단계: python3 logickor_judge.py --judge gpt-5 --tag logickor-gpt5")

if __name__ == "__main__":
    main()
