# Longest Palindrome Subsequence
class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""
        
        longest = ""

        for i in range(len(s)):
            odd = self.expandAroundCenter(s, i, i)
            even = self.expandAroundCenter(s, i, i + 1)

            if len(odd) > len(longest):
                longest = odd
            if len(even) > len(longest):
                longest = even

        return longest

    def expandAroundCenter(self, s: str, left: int, right: int) -> str:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

# Longest Common Subsequence   
# Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.
# 2D Array O(mxn), O(mxn)
def lcs_string(text1, text2):
    m, n = len(text1), len(text2)

    # Step 1: Build DP table
    dp = [[0] * (n+1) for _ in range(m+1)]
    for i in range(m):
        for j in range(n):
            if text1[i] == text2[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])

    # Step 2: Backtrack to reconstruct the LCS string
    i, j = m, n
    lcs_chars = []

    while i > 0 and j > 0:
        if text1[i-1] == text2[j-1]:
            lcs_chars.append(text1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] >= dp[i][j-1]:
            i -= 1
        else:
            j -= 1

    # Step 3: Reverse because we collected characters from end to start
    lcs_chars.reverse()
    return "".join(lcs_chars)
# You can trace back diagonally (where characters matched) to reconstruct the LCS itself ("ace").
#     ""  a  c  e
# ""  0  0  0  0
#  a  0  1  1  1
#  b  0  1  1  1
#  c  0  1  2  2
#  d  0  1  2  2
#  e  0  1  2  3

# 1D Array O(mxn), O(min(m,n)
# Use a 1D array dp where dp[j] represents the LCS length for subproblems.
# Track the previous diagonal value (prev) to avoid overwriting needed values.
def longestCommonSubsequence(text1: str, text2: str) -> int:
    if len(text1) < len(text2):
        text1, text2 = text2, text1 

    m, n = len(text1), len(text2)
    dp = [0] * (n + 1)
    
    for i in range(1, m + 1):
        prev = 0  # Tracks dp[i-1][j-1]
        for j in range(1, n + 1):
            curr = dp[j]
            if text1[i-1] == text2[j-1]: # Match → dp[2] = dp[1] + 1 = 2
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j-1]) # No match → carry forward max(dp[2], dp[3]) = 2
            prev = curr
    
    return dp[n]
# Input: text1 = "abcde", text2 = "ace" 
# Output: 3  
# Explanation: The longest common subsequence is "ace" and its length is 3.

# Unique Paths from start to end of 2D Matrix O(mn),O(n)
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        aboveRow = [1] * n

        for _ in range(m - 1):
            currentRow = [1] * n
            for i in range(1, n):
                currentRow[i] = currentRow[i-1] + aboveRow[i]
            aboveRow = currentRow
            
        return aboveRow[-1]
#   0   1   2
# 0	1	1	1
# 1	1	2	3
# 2	1	3	6


# Minimum Sum Path from start to end O(mn), O(1)
# summate 1st col and 1row, sum of (min of row-1 and col-1), last grid[-1][-1]
# [1, 3, 1]
# [1, 5, 1]
# [4, 2, 1]

# After Row, Column Computation
# [1, 4, 5]
# [2, 5, 1]
# [6, 2, 1]

# [1, 4, 5]
# [2, 7, 6]
# [6, 8, 7]
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        for i in range(1, m): # summate 1st col
            grid[i][0] += grid[i-1][0]
        
        for i in range(1, n): # summate 1st row
            grid[0][i] += grid[0][i-1]
        for i in range(1, m):
            for j in range(1, n):
                grid[i][j] += min(grid[i-1][j], grid[i][j-1])
        return grid[-1][-1]

# if grid modification is not allowed
def min_path_sum_dp(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]

    dp[0][0] = grid[0][0]

    # Fill first row
    for col in range(1, cols):
        dp[0][col] = dp[0][col - 1] + grid[0][col]

    # Fill first column
    for row in range(1, rows):
        dp[row][0] = dp[row - 1][0] + grid[row][0]

    # Fill rest of dp table
    for row in range(1, rows):
        for col in range(1, cols):
            dp[row][col] = min(dp[row - 1][col], dp[row][col - 1]) + grid[row][col]

    return dp[-1][-1]

def minPathSum(grid):
    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = grid[0][0]
    
    # Initialize first row
    for j in range(1, n):
        dp[j] = dp[j-1] + grid[0][j]
    
    for i in range(1, m):
        dp[0] += grid[i][0]  # Update first column
        for j in range(1, n):
            dp[j] = min(dp[j-1], dp[j]) + grid[i][j]
    
    return dp[-1]

# Combination Sum 4 [four integers == target] O(target * len(nums)), O(target)
# Given an array of distinct integers nums and a target integer target, return the number of possible combinations that add up to target.
# The test cases are generated so that the answer can fit in a 32-bit integer.
# Example 1:
# Input: nums = [1,2,3], target = 4
# Output: 7
def combinationSum4(nums, target):
    dp = [0] * (target + 1)
    dp[0] = 1  # Base case: one way to make sum (using no numbers)
    
    for i in range(1, target + 1):
        for num in nums:
            if i >= num:
                dp[i] += dp[i - num]
    
    return dp[target]   
# i	dp[i] (Before Update)	Updates (dp[i] += dp[i - num])	                dp[i] (After Update)
# 1 	0	        dp[1] += dp[0] (via num=1)	                               1
# 2	    0	        dp[2] += dp[1] (via num=1), dp[2] += dp[0] (via num=2)	1 + 1 = 2
# 3 	0	        dp[3] += dp[2] (via num=1), dp[3] += dp[1] (via num=2), dp[3] += dp[0] (via num=3)	2 + 1 + 1 = 4
# 4	    0	        dp[4] += dp[3] (via num=1), dp[4] += dp[2] (via num=2), dp[4] += dp[1] (via num=3)	4 + 2 + 1 = 7

# Climb Stairs O(n),O(1)
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 3: return n

        prev1 = 3
        prev2 = 2

        for _ in range(3, n):
            cur = prev1 + prev2
            prev2 = prev1
            prev1 = cur
        
        return cur
   
# Word Break O(n³)	O(n)
def wordBreak(s, wordDict):
    word_set = set(wordDict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[-1]
# Input: s = "leetcode", wordDict = ["leet","code"]
# Output: true
# Explanation: Return true because "leetcode" can be segmented as "leet code".
# Visualization (s = "leetcode", wordDict = ["leet", "code"])**

# Initialize dp = [True, False, ..., False] (length 9).
# dp[4] = True ("leet" found).
# dp[8] = True ("code" found and dp[4] is True).

 
# Coins Change, fewest number of coins O(amount * len(coins)), O(amount)
def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins for amount 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1) # For each coin, update dp[i] if using that coin reduces the count:
    
    return dp[amount] if dp[amount] != float('inf') else -1
# Coin = 1:
# dp[i]	0	1	2	3	4	5	6	7	8	9	10	11
# Coin = 2:
# dp[i]	0	1	1	2	2	3	3	4	4	5	5	6
# Coin = 5:
# dp[i]	0	1	1	2	2	1	2	2	3	3	2	3
# dp[11] = 3 → Minimum coins needed: [5, 5, 1]

# Perfect squares O(n√n)	O(n)
# Given an integer n, return the least number of perfect square numbers that sum to n
# dp[i - square] gives the minimum number of perfect squares required to sum up to i - square.
# By adding 1 (+1), we're including the current square in the total.
import math
def numSquares(n: int) -> int:
    # Create a list to store the least number of perfect squares for each number up to n
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # base case: 0 can be represented by 0 squares

    # Precompute all perfect squares <= n
    squares = [i * i for i in range(1, int(math.sqrt(n)) + 1)]

    for i in range(1, n + 1):
        for square in squares:
            if square > i:
                break
            dp[i] = min(dp[i], dp[i - square] + 1)
    
    return dp[n]

# Partition Equal Subset Sum O(n * target)	O(target)
class Solution:
    def canPartition(nums):
        total = sum(nums)
        if total % 2 != 0:
            return False
        target = total // 2
        dp = [False] * (target + 1)
        dp[0] = True
        for num in nums:
            for j in range(target, num - 1, -1):
                dp[j] = dp[j] or dp[j - num]
        return dp[target]
# Input: nums = [1,5,11,5]
# Output: true
# Explanation: The array can be partitioned as [1, 5, 5] and [11].
# Visualization (nums = [1, 5, 11, 5])

# Total Sum: 22 → Target: 11.
# DP Table (1D):
# Initialize dp = [True, False, ..., False] (size 12).
# For num = 5:
# dp[6] = dp[1] → True (1 + 5 = 6).
# dp[11] = dp[6] → True (6 + 5 = 11).

# Pascal Triangle O(numRows²)	O(numRows²)
def generate(numRows):
    triangle = []
    for i in range(numRows):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = triangle[i-1][j-1] + triangle[i-1][j]
        triangle.append(row)
    return triangle
# Row 0: [1]
# Row 1: [1, 1]
# Row 2: [1, 2, 1]  # 2 = 1 + 1
# Row 3: [1, 3, 3, 1]  # 3 = 1 + 2, 3 = 2 + 1

# Decode Ways O(n),O(n)
# Let dp[i] = number of ways to decode up to s[0...i-1].
# Initialize:
#   dp[0] = 1 → empty string has 1 way (doing nothing).
#   dp[1] = 1 if s[0] != '0', else 0.
# Then, for each i from 2 to len(s):
#   If s[i-1] != '0', add dp[i-1] (decode single digit).
#   If s[i-2:i] in [10,26], add dp[i-2] (decode two digits).
def numDecodings(s: str) -> int:
    if not s or s[0] == '0':
        return 0

    n = len(s)
    dp = [0] * (n + 1)

    dp[0] = 1  # empty string
    dp[1] = 1  # first char (non-zero)

    for i in range(2, n + 1):
        # Single digit decode
        if s[i-1] != '0':
            dp[i] += dp[i-1]
        
        # Two digit decode
        two_digit = int(s[i-2:i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i-2]

    return dp[n]

# O(n),O(1) Since we only need dp[i-1] and dp[i-2] at any time, we can use two variables instead of an array:
def numDecodings(s: str) -> int:
    if not s or s[0] == '0':
        return 0

    prev = 1  # dp[i-2]
    curr = 1  # dp[i-1]

    for i in range(1, len(s)):
        temp = 0
        if s[i] != '0':
            temp = curr
        if 10 <= int(s[i-1:i+1]) <= 26:
            temp += prev
        prev, curr = curr, temp

    return curr
# Input: s = "12"
# Output: 2
# Explanation:
# "12" could be decoded as "AB" (1 2) or "L" (12).


# Minimum Operations to Make Two Words Equal (Edit Distance Problem)
# Key Idea:
#     Use a DP table dp[i][j] where i and j represent prefixes of word1 and word2.
#     dp[i][j] stores the minimum operations to match word1[:i] and word2[:j].
# Transition Cases:
#     Characters match (word1[i-1] == word2[j-1]):
#         No operation needed. Carry forward dp[i-1][j-1].
#     Characters differ:
#         Insert: dp[i][j-1] + 1
#         Delete: dp[i-1][j] + 1
#         Replace: dp[i-1][j-1] + 1
#         Take the minimum of these three options.
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases:
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters in word1
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters from word2
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # No operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i][j-1],    # Insert
                    dp[i-1][j],    # Delete
                    dp[i-1][j-1]   # Replace
                )
    
    return dp[m][n]

# Example Usage:
# word1 = "horse"
# word2 = "ros"
# print(minDistance(word1, word2))  # Output: 3 (horse → rorse → rose → ros)
# Time: O(m × n) (where m and n are the lengths of word1 and word2).
# Space: O(m × n) (can be optimized to O(min(m, n)) using 1D DP).

# (Space: O(min(m, n)))
# Initialization:
#   Let m = len(word1), n = len(word2).
#   If m < n, swap word1 and word2 to ensure word2 is the shorter string.
#   Initialize prev = [0, 1, 2, ..., n] (cost to build word2[:j] from an empty string).
# Fill DP Array:
#   For each character in word1 (index i):
#     Initialize curr[0] = i (cost to convert word1[:i] to an empty string).
#     For each character in word2 (index j):
#       If word1[i-1] == word2[j-1], set curr[j] = prev[j-1].
#       Else, set curr[j] = 1 + min(prev[j], curr[j-1], prev[j-1]).
#     Update prev = curr for the next iteration.
# Result:
#   prev[n] gives the minimum edit distance.
def minDistanceOptimized(word1: str, word2: str) -> int:
    # Initialization
    m, n = len(word1), len(word2)
    if m < n:
        word1, word2 = word2, word1  # Ensure word1 is longer
        m, n = n, m
    
    prev = list(range(n + 1))  # prev[j] = edit distance for word1[0..0] and word2[0..j-1]
    # Fill DP Array for char in word1 
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        curr[0] = i  # Cost to delete all characters in word1[0..i-1]
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                curr[j] = prev[j-1]  # No operation needed
            else:
                curr[j] = 1 + min(
                    prev[j],     # Delete word1[i-1]
                    curr[j-1],   # Insert word2[j-1]
                    prev[j-1]    # Replace word1[i-1] with word2[j-1]
                )
        prev = curr
    
    return prev[n]