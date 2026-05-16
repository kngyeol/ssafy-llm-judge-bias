# Two Sum  (code)

**문제**
> Python으로 'Two Sum' 문제를 풀어라. 입력: 정수 배열 nums와 target. 출력: nums[i] + nums[j] == target 인 (i, j) 인덱스. 한 번만 풀고 코드만, 시간복잡도도 함께 한 줄로.

## 🅰️  GPT-5.2
```python
def twoSum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        y = target - x
        if y in seen:
            return (seen[y], i)
        seen[x] = i

# Time Complexity: O(n)
```

## 🅱️  Claude-Opus-4.5
```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
```

**시간복잡도: O(n)**

## ⚖️  심판 (CLAUDE_SONNET_4_5)
WINNER: TIE

REASON: 두 답변 모두 해시맵을 이용한 O(n) 솔루션을 정확히 구현했으며, 시간복잡도도 명시했다. A는 튜플 반환, B는 리스트 반환이라는 사소한 차이만 있을 뿐 알고리즘 품질과 요구사항 충족도가 동등하다.
