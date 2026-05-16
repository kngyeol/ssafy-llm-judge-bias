#!/usr/bin/env python3
"""
Human baseline 채점 CLI — 본인이 직접 50개 라운드를 모델 라벨 가린 채 평가.
나중에 각 LLM 심판과의 일치율을 계산해서 "어느 심판이 가장 인간스러운가" 정량화.

특징:
  - 매 라운드 A/B 순서를 랜덤화 (위치 편향 통제)
  - 모델 이름 노출 안 함 (스타일 인식만 가능)
  - 진행 상황 자동 저장 (중간에 끊어도 이어서)
  - 평가 후 LLM 심판들과 자동 비교

사용:
  python3 human_baseline.py                    # 채점 시작/이어하기
  python3 human_baseline.py --compare          # 결과 LLM 심판들과 비교
  python3 human_baseline.py --reset            # 진행상황 초기화 (주의)
"""
import argparse, json, random, sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from replay_judge import load_battle, RESULTS_DIR
ROOT = Path(__file__).parent

# 원본 배틀 (답변 소스 — 다 동일하므로 아무거나)
SOURCE_BATTLE = RESULTS_DIR / "battle_20260516_134437_judge-gpt5"
PROGRESS_FILE = RESULTS_DIR / "human_baseline" / "progress.json"

# 비교 대상 LLM 심판 결과들
LLM_JUDGE_BATTLES = {
    "GPT-5": "battle_20260516_134437_judge-gpt5",
    "Claude-Sonnet": "battle_20260516_134439_judge-claude",
    "Gemini-Flash": "battle_20260516_134440_judge-gemini",
}

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"started_at": datetime.now().isoformat(), "scores": {}}

def save_progress(progress: dict):
    PROGRESS_FILE.parent.mkdir(exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2),
                             encoding="utf-8")

def truncate(s: str, n: int = 1500) -> str:
    return s if len(s) <= n else s[:n] + f"\n[...잘림 ({len(s)-n}자 더)]"

def score_one(challenge: dict, progress: dict, idx: int, total: int) -> bool:
    """한 라운드 채점. 사용자 입력 받음. 종료/스킵 처리."""
    cid = challenge["id"]

    if cid in progress["scores"]:
        return True  # 이미 채점됨

    # 랜덤 순서로 표시 (left/right 라벨은 X/Y로 사용, A/B 혼동 방지)
    rng = random.Random(cid)  # id 기반 deterministic
    swap = rng.random() < 0.5
    left = challenge["ans_b"] if swap else challenge["ans_a"]
    right = challenge["ans_a"] if swap else challenge["ans_b"]
    left_orig = "B" if swap else "A"
    right_orig = "A" if swap else "B"

    print("\n" + "═" * 70)
    print(f"  [{idx}/{total}]  {cid}  ({challenge['category']})  —  {challenge['name']}")
    print("═" * 70)
    print(f"\n📋 문제\n{challenge['prompt']}\n")
    print("─" * 70)
    print(f"\n🅧  답변 X\n{truncate(left)}\n")
    print("─" * 70)
    print(f"\n🅨  답변 Y\n{truncate(right)}\n")
    print("─" * 70)
    print("\n🗳️  당신의 판정")
    print("   x = X가 더 나음     y = Y가 더 나음     t = 무승부")
    print("   s = 스킵 (나중에)   q = 종료")

    while True:
        ans = input("선택: ").strip().lower()
        if ans in ("x", "y", "t"):
            # 원본 라벨로 변환
            pick_map = {"x": left_orig, "y": right_orig, "t": "TIE"}
            picked = pick_map[ans]
            progress["scores"][cid] = {
                "human_pick": picked,
                "shown_left": left_orig,
                "shown_right": right_orig,
                "shown_pick": "X" if ans == "x" else ("Y" if ans == "y" else "TIE"),
                "scored_at": datetime.now().isoformat(),
                "category": challenge["category"],
            }
            save_progress(progress)
            print(f"  ✓ 저장: 원본 라벨 기준 → {picked}")
            return True
        if ans == "s":
            print("  (스킵)")
            return True
        if ans == "q":
            return False
        print("  ?? 다시 입력: x / y / t / s / q")

def cmd_score(args):
    rounds = load_battle(SOURCE_BATTLE)
    progress = load_progress()
    print(f"\n총 {len(rounds)}개 챌린지. 이미 채점된: {len(progress['scores'])}")
    print(f"진행 상황: {PROGRESS_FILE}\n")
    if args.limit:
        rounds = rounds[:args.limit]
    for i, r in enumerate(rounds, 1):
        ok = score_one(r, progress, i, len(rounds))
        if not ok:
            print(f"\n👋 종료. {len(progress['scores'])}/{len(rounds)} 채점 완료.")
            return
    print(f"\n🎉 전체 채점 완료! {len(progress['scores'])}개")
    print(f"→ 비교 실행: python3 {Path(__file__).name} --compare")

def cmd_compare(args):
    progress = load_progress()
    if not progress["scores"]:
        sys.exit("❌ 채점된 라운드 없음. 먼저 채점부터.")

    # LLM 심판 결과 로드
    judge_picks = {}
    for jname, bname in LLM_JUDGE_BATTLES.items():
        bd = RESULTS_DIR / bname
        rj = json.loads((bd / "_results.json").read_text())
        judge_picks[jname] = {r["id"]: r["winner"] for r in rj["results"]}

    # 일치율 계산
    print("\n" + "═" * 70)
    print(f"  Human Baseline 일치율 분석 ({len(progress['scores'])}개 라운드)")
    print("═" * 70)

    rows = []
    for jname, picks in judge_picks.items():
        agreed = 0
        total = 0
        agreed_no_tie = 0
        total_no_tie = 0
        for cid, hscore in progress["scores"].items():
            jpick = picks.get(cid)
            if jpick is None:
                continue
            total += 1
            if jpick == hscore["human_pick"]:
                agreed += 1
            # TIE 제외 일치율 (TIE는 회피 답변일 수도)
            if hscore["human_pick"] != "TIE" and jpick != "TIE":
                total_no_tie += 1
                if jpick == hscore["human_pick"]:
                    agreed_no_tie += 1
        pct = 100 * agreed / total if total else 0
        pct_nt = 100 * agreed_no_tie / total_no_tie if total_no_tie else 0
        rows.append((jname, agreed, total, pct, agreed_no_tie, total_no_tie, pct_nt))

    print(f"\n{'심판':<18} {'일치율':<12} {'(TIE 제외)':<14}")
    print("─" * 50)
    for jname, ag, tot, pct, ag_nt, tot_nt, pct_nt in rows:
        print(f"{jname:<18} {ag:>3}/{tot:<3} ({pct:5.1f}%)  {ag_nt:>3}/{tot_nt:<3} ({pct_nt:5.1f}%)")

    # 카테고리별
    from collections import defaultdict
    by_cat = defaultdict(lambda: defaultdict(lambda: {"agreed": 0, "total": 0}))
    for jname, picks in judge_picks.items():
        for cid, hscore in progress["scores"].items():
            jpick = picks.get(cid)
            if jpick is None:
                continue
            cat = hscore["category"]
            by_cat[cat][jname]["total"] += 1
            if jpick == hscore["human_pick"]:
                by_cat[cat][jname]["agreed"] += 1

    print(f"\n카테고리별 일치율")
    print(f"{'카테고리':<12}", end="")
    for jname in judge_picks:
        print(f"  {jname:<16}", end="")
    print()
    print("─" * (12 + 18 * len(judge_picks)))
    for cat in sorted(by_cat):
        print(f"{cat:<12}", end="")
        for jname in judge_picks:
            s = by_cat[cat][jname]
            pct = 100 * s["agreed"] / s["total"] if s["total"] else 0
            print(f"  {s['agreed']:>2}/{s['total']:<2} ({pct:4.0f}%)    ", end="")
        print()

    # 결과 저장
    out = RESULTS_DIR / "human_baseline" / "comparison.json"
    out.write_text(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "n_scored": len(progress["scores"]),
        "by_judge": {n: {"agreed": ag, "total": tot, "pct": pct,
                         "agreed_no_tie": ag_nt, "total_no_tie": tot_nt, "pct_no_tie": pct_nt}
                     for n, ag, tot, pct, ag_nt, tot_nt, pct_nt in rows},
        "by_category": {cat: {jn: dict(s) for jn, s in d.items()} for cat, d in by_cat.items()},
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✓ 저장: {out}")

def cmd_reset(args):
    if PROGRESS_FILE.exists():
        confirm = input("⚠ 채점 진행상황 전부 삭제할까요? (yes/no): ").strip()
        if confirm.lower() == "yes":
            PROGRESS_FILE.unlink()
            print("✓ 초기화됨")
        else:
            print("취소")
    else:
        print("이미 초기 상태")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--compare", action="store_true", help="채점 결과를 LLM 심판들과 비교")
    p.add_argument("--reset", action="store_true", help="진행상황 초기화")
    p.add_argument("--limit", type=int, help="이번 세션에서 최대 N개만 채점")
    args = p.parse_args()

    if args.reset:
        cmd_reset(args)
    elif args.compare:
        cmd_compare(args)
    else:
        cmd_score(args)

if __name__ == "__main__":
    main()
