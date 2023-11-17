from typing import List

class Solution:
    def maxProduct(self, words: List[str]) -> int:
        mp = {}
        for word in words:
            x = 0
            for c in word:
                x |= 1 << (ord(c) - ord('a'))
            mp[word] = x

        n = len(words)
        ans = 0
        for i in range(n):
            for j in range(i + 1, n):
                if not mp[words[i]] & mp[words[j]]:
                    # ans = max(ans, len(words[i] * len(words[j])))
                    ans = max(ans, len(words[i]) * len(words[j]))
        return ans

words = ["abcw","baz","foo","bar","xtfn","abcdef"]
# abcw
# x=0
# a-a=0 1<< =>0
#

# b-a=1 x|1*2 => ?
# 00000000
# 00000010
# 00000010  => 2
# b-a=1 x|1*2 => 2

# c-a=2 x|2*2 => ?
# 00000010
# 00000100
# 00000110  => 6
# c-a=2 x|2*2 => 6

# w-a=23 x|23*2 => ?
# 00000110
# 00010111
# 00010111  =>
s = Solution()
ans = s.maxProduct(words)
print(ans)