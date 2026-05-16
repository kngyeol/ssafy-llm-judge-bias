#!/usr/bin/env python3
"""
LogicKor fight 결과를 받아 턴별로 채점.

각 entry는 2턴 평가:
  - turn 1: A1 vs B1 (Q1 단독)
  - turn 2: A2 vs B2 (Q1+A?+Q2 컨텍스트에서의 최종 답변)

Output: results/logickor_judge_<tag>/_results.json + per-entry markdown
"""
import argparse, json, sys, time
from datetime import datetime
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from gladiator import call, COST, JUDGE_ALIASES, JUDGE_SYSTEM, _kind_of

ROOT = Path(__file__).parent

def judge_turn(judge_spec: dict, q: str, ans_a: str, ans_b: str,
               turn_idx: int, prior_context: str = None) -> dict:
    if prior_context:
        prompt = f"""[Multi-turn LogicKor 평가 — Turn {turn_idx+1}]

[이전 컨텍스트]
{prior_context}

[현재 턴 질문]
{q}

[A의 답변]
{ans_a}

[B의 답변]
{ans_b}

이전 컨텍스트를 고려해서 현재 턴의 두 답변을 비교 판정해라."""
    else:
        prompt = f"""[Multi-turn LogicKor 평가 — Turn {turn_idx+1}]

[질문]
{q}

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

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fights-dir", default="results/logickor_fights")
    p.add_argument("--judge", required=True)
    p.add_argument("--tag", required=True)
    p.add_argument("--budget", type=int, default=5000)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    fights_dir = ROOT / args.fights_dir
    fights = [json.loads(f.read_text()) for f in sorted(fights_dir.glob("*.json"))]
    if not fights:
        sys.exit(f"❌ {fights_dir} 비어있음")

    judge_model = JUDGE_ALIASES.get(args.judge, args.judge)
    judge_spec = {
        "name": args.judge.upper().replace("-", "_").replace(".", "_"),
        "model": judge_model,
        "kind": _kind_of(judge_model),
    }
    j_cost = COST.get(judge_model, 30)
    total = len(fights) * 2 * j_cost  # 2턴
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Fights      : {len(fights)} entries (각 2턴 = {len(fights)*2} 판정)")
    print(f"심판        : {judge_spec['name']} ({judge_model})")
    print(f"예상 비용   : {total:,} credit")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    if total > args.budget:
        sys.exit("❌ 예산 초과")
    if args.dry_run:
        print("(dry-run)")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = ROOT / "results" / f"logickor_judge_{timestamp}_{args.tag}"
    out_dir.mkdir()

    results = []
    for i, f in enumerate(fights, 1):
        print(f"\n[{i}/{len(fights)}] id={f['id']}  {f['category']}")
        entry_results = {"id": f["id"], "category": f["category"], "turns": []}
        # Turn 1
        try:
            print(f"  → Turn 1 채점...", flush=True, end="")
            j1 = judge_turn(judge_spec, f["questions"][0],
                            f["a"]["answers"][0], f["b"]["answers"][0], 0)
            print(f"  → {j1['winner']}", flush=True)
            entry_results["turns"].append({"turn": 1, "winner": j1["winner"], "raw": j1["raw"]})
        except Exception as e:
            print(f"  ❌ T1 에러: {e}")
            entry_results["turns"].append({"turn": 1, "winner": "ERROR", "error": str(e)})

        # Turn 2 — 이전 컨텍스트 일부 포함
        try:
            print(f"  → Turn 2 채점...", flush=True, end="")
            prior = f"질문: {f['questions'][0]}\n(A는 자기 답을, B는 자기 답을 가지고 다음 턴 진행)"
            j2 = judge_turn(judge_spec, f["questions"][1],
                            f["a"]["answers"][1], f["b"]["answers"][1], 1, prior_context=prior)
            print(f"  → {j2['winner']}", flush=True)
            entry_results["turns"].append({"turn": 2, "winner": j2["winner"], "raw": j2["raw"]})
        except Exception as e:
            print(f"  ❌ T2 에러: {e}")
            entry_results["turns"].append({"turn": 2, "winner": "ERROR", "error": str(e)})

        results.append(entry_results)

        # 라운드 md
        md_parts = [f"# LogicKor #{f['id']:02d} ({f['category']})\n"]
        for t in range(2):
            q = f["questions"][t]
            a = f["a"]["answers"][t]
            b = f["b"]["answers"][t]
            j = entry_results["turns"][t]
            md_parts.append(f"\n## Turn {t+1}\n\n**질문**\n> {q}\n\n### 🅰️ {f['a']['name']}\n{a}\n\n### 🅱️ {f['b']['name']}\n{b}\n\n### ⚖️ 심판 ({judge_spec['name']})\n{j.get('raw', j.get('error', ''))}\n")
        (out_dir / f"{f['id']:02d}.md").write_text("\n".join(md_parts), encoding="utf-8")

    # 집계
    totals = {"A": 0, "B": 0, "TIE": 0, "ERROR": 0}
    by_turn = {1: defaultdict(int), 2: defaultdict(int)}
    by_cat = defaultdict(lambda: {"A": 0, "B": 0, "TIE": 0, "ERROR": 0})

    for r in results:
        for t in r["turns"]:
            totals[t["winner"]] += 1
            by_turn[t["turn"]][t["winner"]] += 1
            by_cat[r["category"]][t["winner"]] += 1

    summary = {
        "timestamp": timestamp,
        "tag": args.tag,
        "judge": {"name": judge_spec["name"], "model": judge_model, "kind": judge_spec["kind"]},
        "n_entries": len(fights),
        "n_turns": len(fights) * 2,
        "totals": dict(totals),
        "by_turn": {str(k): dict(v) for k, v in by_turn.items()},
        "by_category": {k: dict(v) for k, v in by_cat.items()},
        "results": results,
    }
    (out_dir / "_results.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                                           encoding="utf-8")

    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✓ {out_dir}")
    print(f"  전체  A:{totals['A']} B:{totals['B']} TIE:{totals['TIE']} ERR:{totals['ERROR']}")
    print(f"  Turn1 A:{by_turn[1]['A']} B:{by_turn[1]['B']} TIE:{by_turn[1]['TIE']}")
    print(f"  Turn2 A:{by_turn[2]['A']} B:{by_turn[2]['B']} TIE:{by_turn[2]['TIE']}")

if __name__ == "__main__":
    main()
