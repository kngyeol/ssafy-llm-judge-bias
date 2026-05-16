#!/usr/bin/env python3
"""
기존 배틀 답변을 재사용해서 새 심판/A·B 위치 교체로 재채점.
파이터 호출 안 함 → 비용 저렴.

용도:
  - Position bias 검증: --swap-ab 로 A/B 위치 교체
  - Self-judge: --judge gpt-5.2  /  --judge claude-opus-4-5
  - 임의 심판 추가: --judge gemini-2.5-pro
"""
import argparse, json, re, sys
from datetime import datetime
from pathlib import Path

# gladiator.py 의 호출 함수와 cost/alias를 그대로 재사용
sys.path.insert(0, str(Path(__file__).parent))
from gladiator import (
    call, _kind_of, COST, JUDGE_ALIASES, JUDGE_SYSTEM,
    FIGHTER_A as ORIG_A, FIGHTER_B as ORIG_B,
    RESULTS_DIR,
)

# ── 기존 배틀에서 답변 파싱 ────────────────────────
def parse_round_md(md_path: Path) -> dict:
    """battle_*/<id>.md 한 개 파싱해서 {prompt, ans_a, ans_b, category, name} 반환"""
    text = md_path.read_text(encoding="utf-8")
    # 첫 줄: # 이름 (카테고리)
    m_title = re.match(r"#\s+(.+?)\s+\((\w+)\)", text)
    name = m_title.group(1) if m_title else md_path.stem
    category = m_title.group(2) if m_title else "?"
    # 프롬프트: > ... (첫 인용)
    m_prompt = re.search(r"\n> (.+?)\n\n## 🅰️", text, re.DOTALL)
    prompt = m_prompt.group(1).strip() if m_prompt else ""
    # 답변: ## 🅰️ ... \n(내용)\n## 🅱️
    m_a = re.search(r"## 🅰️[^\n]*\n(.+?)\n\n## 🅱️", text, re.DOTALL)
    m_b = re.search(r"## 🅱️[^\n]*\n(.+?)\n\n## ⚖️", text, re.DOTALL)
    return {
        "id": md_path.stem,
        "name": name,
        "category": category,
        "prompt": prompt,
        "ans_a": m_a.group(1).strip() if m_a else "",
        "ans_b": m_b.group(1).strip() if m_b else "",
    }

def load_battle(battle_dir: Path) -> list:
    rounds = []
    for md in sorted(battle_dir.glob("*.md")):
        if md.stem.startswith("_"):
            continue
        r = parse_round_md(md)
        if r["ans_a"] and r["ans_b"]:
            rounds.append(r)
    return rounds

# ── 재채점 ────────────────────────────────────────
def judge_pair(judge_spec: dict, challenge: dict, ans_a: str, ans_b: str) -> dict:
    """A, B 라벨로 답변 제시 → 심판 호출 → 결과 dict"""
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

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--from-battle", required=True, help="기존 결과 디렉토리")
    p.add_argument("--judge", required=True, help="심판 모델 alias 또는 id")
    p.add_argument("--swap-ab", action="store_true",
                   help="A/B 위치 교체 (원래 B → A로 표시)")
    p.add_argument("--tag", required=True, help="결과 디렉토리 접미사")
    p.add_argument("--budget", type=int, default=10000)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    battle_dir = Path(args.from_battle)
    if not battle_dir.exists():
        sys.exit(f"❌ 배틀 디렉토리 없음: {battle_dir}")

    rounds = load_battle(battle_dir)
    if not rounds:
        sys.exit(f"❌ 라운드 0개 파싱됨. 디렉토리 확인.")

    judge_model = JUDGE_ALIASES.get(args.judge, args.judge)
    judge_spec = {
        "name": args.judge.upper().replace("-", "_").replace(".", "_"),
        "model": judge_model,
        "kind": _kind_of(judge_model),
    }
    j_cost = COST.get(judge_model, 30)
    total_cost = len(rounds) * j_cost

    print("━" * 50)
    print(f"원본 배틀  : {battle_dir.name}")
    print(f"라운드 수  : {len(rounds)}")
    print(f"새 심판    : {judge_spec['name']} ({judge_model})")
    print(f"A/B 교체   : {'예' if args.swap_ab else '아니오'}")
    print(f"예상 비용  : 약 {total_cost:,} credit (심판 호출만)")
    print(f"예산 한도  : {args.budget:,} credit")
    print("━" * 50)

    if total_cost > args.budget:
        sys.exit(f"❌ 예산 초과")
    if args.dry_run:
        print("(dry-run)")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = RESULTS_DIR / f"replay_{timestamp}_{args.tag}"
    out_dir.mkdir()

    results = []
    for i, r in enumerate(rounds, 1):
        print(f"\n[{i}/{len(rounds)}] {r['id']} — {r['name']}", flush=True)
        # swap-ab: 원래 B를 A로, 원래 A를 B로 제시
        if args.swap_ab:
            shown_a, shown_b = r["ans_b"], r["ans_a"]
            orig_a_label = "B"  # judge가 "A" 골랐다 = 원래 B (= Claude) 손
        else:
            shown_a, shown_b = r["ans_a"], r["ans_b"]
            orig_a_label = "A"
        try:
            j = judge_pair(judge_spec, r, shown_a, shown_b)
        except Exception as e:
            print(f"  ❌ {e}")
            results.append({"id": r["id"], "category": r["category"],
                            "judge_pick": "ERROR", "original_winner": "ERROR"})
            continue
        # original_winner: 원래 라벨 기준 어느 쪽이 이겼나
        if j["winner"] == "TIE":
            original_winner = "TIE"
        elif args.swap_ab:
            # judge가 "A" 골랐다 = 원래 B 답이 이김
            original_winner = "B" if j["winner"] == "A" else "A"
        else:
            original_winner = j["winner"]
        print(f"  판정: shown={j['winner']}  → 원본 라벨 기준: {original_winner}")
        results.append({
            "id": r["id"], "category": r["category"],
            "judge_pick_shown": j["winner"],
            "original_winner": original_winner,
        })

        # 라운드 md
        md = f"""# {r['name']}  ({r['category']})  [replay/{args.tag}]

**문제**
> {r['prompt']}

## 🅰️ (shown as A, originally {'B (Claude-Opus)' if args.swap_ab else 'A (GPT-5.2)'})
{shown_a}

## 🅱️ (shown as B, originally {'A (GPT-5.2)' if args.swap_ab else 'B (Claude-Opus)'})
{shown_b}

## ⚖️ 심판 ({judge_spec['name']})
{j['raw']}

**해석**: 심판이 {j['winner']}를 골랐고, 원본 라벨 기준 **{original_winner}** 손이 올라감.
"""
        (out_dir / f"{r['id']}.md").write_text(md, encoding="utf-8")

    # 집계
    a_wins = sum(1 for r in results if r["original_winner"] == "A")
    b_wins = sum(1 for r in results if r["original_winner"] == "B")
    ties = sum(1 for r in results if r["original_winner"] == "TIE")
    errs = sum(1 for r in results if r["original_winner"] == "ERROR")

    from collections import defaultdict
    by_cat = defaultdict(lambda: {"A": 0, "B": 0, "TIE": 0, "ERROR": 0})
    for r in results:
        by_cat[r["category"]][r["original_winner"]] += 1

    summary = {
        "timestamp": timestamp,
        "tag": args.tag,
        "from_battle": battle_dir.name,
        "judge": {"name": judge_spec["name"], "model": judge_model, "kind": judge_spec["kind"]},
        "swap_ab": args.swap_ab,
        "totals": {"A": a_wins, "B": b_wins, "TIE": ties, "ERROR": errs},
        "by_category": dict(by_cat),
        "results": results,
    }
    (out_dir / "_results.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                                           encoding="utf-8")
    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✓ {out_dir}")
    print(f"  원본 라벨 기준: A {a_wins} - {b_wins} B  (무 {ties}, 에러 {errs})")

if __name__ == "__main__":
    main()
