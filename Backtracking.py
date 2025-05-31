######## BACKTRACKING ##########

# Combination Sum on array elements equal to target O(2^n)
# Explore at one combination then
# Backtrack to explore other combinations, trying 3 and 7 in turn.
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []

        def backtrack(start: int, path: List[int], total: int):
            if total == target:
                result.append(path[:])  # Found a valid combination
                return
            if total > target:
                return  # Prune the branch if total exceeds target

            for i in range(start, len(candidates)):
                path.append(candidates[i])
                backtrack(i, path, total + candidates[i])  # i (not i+1) because we can reuse the same element
                path.pop()  # Undo the choice

        backtrack(0, [], 0)
        return result
# Input: candidates = [2,3,6,7], target = 7
# Output: [[2,2,3],[7]]

# # Combination Sum II  # May contain duplicate and each number can used only once
# Input: candidates = [10,1,2,7,6,1,5], target = 8
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []
        candidates.sort()

        def backtrack(start: int, path: List[int], total: int):
            if total == target:
                result.append(path[:])  # Found valid combination
                return
            if total > target:
                return  # Exceeded target

            for i in range(start, len(candidates)):
                # Skip duplicates
                if i > start and candidates[i] == candidates[i-1]:
                    continue
                path.append(candidates[i])
                backtrack(i+1, path, total + candidates[i])  # Move to i+1 to use each element once
                path.pop()  # Backtrack

        backtrack(0, [], 0)
        return result
# Output: [[1,1,6],[1,2,5],[1,7],[2,6]]
# O(nlogn+k*2^n)
# n log n from Sorting
# k is number of valid combinations
# The DFS algorithm has a worst-case time complexity of O(2^n)

# Combination Sum III
# Find all valid combinations of k numbers that sum up to n 
def combinationSum3(k: int, n: int) -> List[List[int]]:
    def backtrack(start, path, remaining_k, target):
        if remaining_k == 0 and target == 0:
            return res.append(path[:])
        if remaining_k == 0 or target <= 0:
            return
        for num in range(start, 10):
            path.append(num)
            backtrack(num + 1, path, remaining_k - 1, target - num)
            path.pop()  # Backtrack

    res = []
    backtrack(1, [], k, n)
    return res
# Time: O(C(9,k)), = O(2^9 . k) where C(9,k) is the number of combinations of k numbers from 1 to 9 (worst case).
# Space: O(k) for the recursion stack (excluding the result storage).
# Input: k = 3, n = 7
# Output: [[1,2,4]]
# Explanation:
# 1 + 2 + 4 = 7
# There are no other valid combinations.
# Example 2:
# Input: k = 3, n = 9
# Output: [[1,2,6],[1,3,5],[2,3,4]]
# Explanation:
# 1 + 2 + 6 = 9
# 1 + 3 + 5 = 9
# 2 + 3 + 4 = 9

# combination Sum k O(n^k)	O(k) (auxiliary)
# Combinations with Exactly k Elements Summing to Target
def combinationSumK(nums, k, target):
    def backtrack(start, path, remaining_target, count):
        if remaining_target == 0 and count == k:
            result.append(path[:])
            return
        if remaining_target < 0 or count >= k:
            return
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path, remaining_target - nums[i], count + 1)
            path.pop()
    
    result = []
    nums.sort()  # Sort to avoid duplicate combinations in different orders
    backtrack(0, [], target, 0)
    return result    
# nums = [1,2,7,6,3,4,2,6,5,4,3]
# target = 11
# [[4, 7], [4, 7], [5, 6], [5, 6]]
# print(combinationSumK(nums,2,target))

# Generate Unique Subsets
class Solution:
    def subsets(nums: List[int]) -> List[List[int]]:
        result = []

        def backtrack(start: int, path: List[int]):
            result.append(path[:])  # Add the current subset to result

            for i in range(start, len(nums)):
                path.append(nums[i])          # Choose
                backtrack(i + 1, path)         # Explore
                path.pop()                     # Un-choose (backtrack)

        backtrack(0, [])
        return result
# Input: nums = [1,2,3]
# Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

# Subset II
# Given an integer array nums that may contain duplicates
class Solution(object):
    def subsetsWithDup(self, nums):

        def backtrack(start, subset):
            result.append(subset[:])
            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i - 1]: # Skip duplicates if i > start i.e # we are not at the first element of the current subset
                    continue
                subset.append(nums[i])
                backtrack(i + 1, subset)
                subset.pop()

        nums.sort()
        result = []
        backtrack(0, [])
        return result
# Input: nums = [1,2,2]
# Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]

# Permutations of numbers in array O(n×n!), O(n!) where n! is the number of permutations, and each permutation takes O(n)O(n) time to copy.
class Solution:
    def permute(self, nums):

        def backtrack(start):
            if start == len(nums):
                res.append(nums[:])
                return
            
            for i in range(start, len(nums)):
                nums[start], nums[i] = nums[i], nums[start]  # Swap
                backtrack(start + 1)                          # Recurse, Using start + 1 
                nums[start], nums[i] = nums[i], nums[start]  # Undo swap (backtrack)

        res = []
        backtrack(0)
        return res
# Input: nums = [1,2,3]
# Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
# [[1, 2, 3, 4], [1, 2, 4, 3], [1, 3, 2, 4], [1, 3, 4, 2], [1, 4, 3, 2]..

# Permutations II, O(n×n!), O(n!) input may contain duplicate
def permuteUnique(nums):
    def backtrack(path, used):
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i] or (i > 0 and nums[i] == nums[i-1] and not used[i-1]):
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False

    nums.sort()
    res = []
    backtrack([], [False] * len(nums))
    return res

# Generate Parentheses
# // Intuition
# // Increase number of open parentheses until we reach n at first
# Initialization: We initialize an empty list res to store the valid combinations.
# Define the dfs function. def dfs(openP, closeP, s): This is a helper function that uses depth-first search (DFS) to explore all possible combinations.
# Base Case: If the number of open and close parentheses are equal and the total length of the string is 2 * n, it means we have a valid combination.
# Recursive Case: Adding an Open Parenthesis
# Recursive Case: Adding a Close Parenthesis
# Initial Call to dfs
# Return the Result
class GenerateParentheses:
    def generateParenthesis(self, n: int) -> List[str]:
        res = []

        def dfs(openP, closeP, s):
            if openP == closeP and openP + closeP == n * 2:
                res.append(s)
                return
            
            if openP < n:
                dfs(openP + 1, closeP, s + "(")
            
            if closeP < openP:
                dfs(openP, closeP + 1, s + ")")

        dfs(0, 0, "")

        return res

# Palindrome Partitioning
# Backtracking , IsPalindrome s[::-1]
def partition(s):
    def is_palindrome(sub):
        return sub == sub[::-1]
    
    def backtrack(start, path):
        if start == len(s):
            result.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            prefix = s[start:end]
            if is_palindrome(prefix):
                path.append(prefix)
                backtrack(end, path)
                path.pop()  # Backtrack
    
    result = []
    backtrack(0, [])
    return result
# Input: s = "aab"
# Output: [["a","a","b"],["aa","b"]]

# Letter Combinations of a Phone Number
# Using backtracking to create all possible combinations
# This is based on Python solution. Other might be differnt a bit.
# Initialize an empty list res to store the generated combinations.
# Check if the digits string is empty. If it is, return an empty list since there are no digits to process.
# Create a dictionary digit_to_letters that maps each digit from '2' to '9' to the corresponding letters on a phone keypad.
# Define a recursive function backtrack(idx, comb) that takes two parameters:
# idx: The current index of the digit being processed in the digits string.
# comb: The current combination being formed by appending letters.
# Inside the backtrack function:
# Check if idx is equal to the length of the digits string. If it is, it means a valid combination has been formed, so append the current comb to the res list.
# If not, iterate through each letter corresponding to the digit at digits[idx] using the digit_to_letters dictionary.
# For each letter, recursively call backtrack with idx + 1 to process the next digit and comb + letter to add the current letter to the combination.
# Initialize the res list.
# Start the initial call to backtrack with idx set to 0 and an empty string as comb. This will start the process of generating combinations.
# After the recursive calls have been made, return the res list containing all the generated combinations.
class LetterCombinations(object):
    def letterCombinations(self, digits):
        """
        :type digits: str
        :rtype: List[str]
        """
        digit_to_letters = {
            '2': 'abc',
            '3': 'def',
            '4': 'ghi',
            '5': 'jkl',
            '6': 'mno',
            '7': 'pqrs',
            '8': 'tuv',
            '9': 'wxyz',
        }

        def backtrack(idx,comb):
            if not digits: #Case of 0
                return []

            if idx == len(digits): #Case of Full
                res.append(comb)
                return 

            for letter in digit_to_letters[digits[idx]]:
                backtrack(idx+1,comb+letter)
        
        res = []
        backtrack(0,"")

        return res
# can be extended to dict of words

#  Count Minimum Operations to Make Valid Parentheses O(n) time and O(1) space
def min_operations_to_valid(s):
    openB = 0
    closeB = 0
    
    for char in s:
        if char == '(':
            openB += 1
        elif char == ')':
            if openB > 0:
                openB -= 1
            else:
                closeB += 1
                
    return openB + closeB

# Remove Invalid Parentheses 
# Time Complexity: O(2^n) in worst case where n is string length
# In practice, it's much better because we stop at the first valid level
# Space Complexity: O(2^n) for the queue and visited set
# Again, optimized by stopping early when solutions are found
# Key Idea:
# Use BFS to explore all possible removals level by level (minimum removals first).
# For each candidate, check validity.
# Problem: Remove the minimum number of invalid parentheses to make the input string valid. Return all possible results.
# First, we define a helper function is_valid to check if a string has balanced parentheses.
# We use BFS approach where each level represents strings with one more character removed.
# Start with the original string in the first level.
# For each string in current level, generate new strings by removing each parenthesis.
# If any valid string is found in current level, return all valid strings.
# Otherwise, proceed to next level with one more character removed.
def removeInvalidParentheses(s):
    def is_valid(t):
        balance = 0
        for c in t:
            if c == '(': balance += 1
            elif c == ')': balance -= 1
            if balance < 0: return False
        return balance == 0

    result = []
    visited = set()
    queue = deque()
    queue.append(s)
    visited.add(s)
    found = False  # Flag to stop at minimum level

    while queue:
        current = queue.popleft()

        if is_valid(current):
            result.append(current)
            found = True  # Mark that we've found valid strings at this level
        
        # If we found valid strings at this level, don't process next level
        if found:
            return current
        
        # Generate all possible strings by removing one parenthesis
        for i in range(len(current)):
            if current[i] not in '()':  # Skip non-parenthesis characters
                continue
            
            # Create new string by removing the i-th character
            new_str = current[:i] + current[i+1:]
            if new_str not in visited:
                visited.add(new_str)
                queue.append(new_str)
    
    return result if result else [""]  # Handle empty string case

# Word Break II for(n^3)
# Given a string s and a dictionary of strings wordDict, add spaces in s to construct a sentence where each word is a valid dictionary word. Return all such possible sentences in any order.
# Note that the same word in the dictionary may be reused multiple times in the segmentation.
# Approach: Backtracking + Memoization
# Key Idea:
# Partition s into valid prefixes (found in wordDict) and recursively process the remaining substring.
# Use DFS + memoization to explore every possible partition.
# At each index, try all prefixes s[start:end].
# If the prefix is in the dictionary, recurse on the remaining substring.
# Use a memoization map to avoid recomputing results for the same substring.
# Input: s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
# Output: ["cats and dog","cat sand dog"]
from functools import lru_cache

def wordBreak(s,wordDict):
    word_set = set(wordDict)  # Convert to set for O(1) lookups
    max_len = max(len(word) for word in wordDict) if wordDict else 0
    
    @lru_cache(maxsize=None)
    def backtrack(start):
        if start == len(s):
            return [""]  # Base case: empty string
        
        sentences = []
        # Try all possible end positions (up to max word length for optimization) for end in range(start + 1, len(s) + 1):
        for end in range(start + 1, min(start + max_len + 1, len(s) + 1)):
            word = s[start:end]
            if word in word_set:
                # Recursively process the remaining string
                for subsentence in backtrack(end):
                    if subsentence:
                        sentences.append(word + " " + subsentence)
                    else:
                        sentences.append(word)
        return sentences
    
    return backtrack(0)

# Preprocessing:
# Convert wordDict to a set for O(1) lookups
# Calculate max_len to limit our prefix checks (optimization)
# Backtracking with Memoization:
# backtrack(start) returns all valid sentences from s[start:]
# Base case: when start reaches end of string, return [""]
# For each possible prefix s[start:end]:
# If prefix is in dictionary:
# Recursively get sentences from s[end:]
# Combine current word with each subsentence
# @lru_cache memoizes results to avoid recomputation


# N-Queens
# Problem: Place n queens on an n x n chessboard such that no two queens threaten each other. Return all distinct solutions.
# Approach: Backtracking
# Key Idea:
# Try placing a queen in each row, ensuring no conflicts with previously placed queens (same column or diagonal).
# Backtrack if a valid position isn't found.
# Solution Code:
def solveNQueens(n: int) -> List[List[str]]:
    def backtrack(row, cols, diags, anti_diags, path):
        if row == n:
            res.append(["".join(row) for row in path])
            return
        for col in range(n):
            d, ad = row - col, row + col
            if col not in cols and d not in diags and ad not in anti_diags:
                path[row][col] = 'Q'
                backtrack(row + 1, cols | {col}, diags | {d}, anti_diags | {ad}, path)
                path[row][col] = '.'  # Backtrack

    res = []
    backtrack(0, set(), set(), set(), [['.'] * n for _ in range(n)])
    return res
# Time Complexity: O(n!)
# Space Complexity: O(n^2)

# Restore IP Addresses:
class solution:
    def restoreIpAddresses(s: str) -> List[str]:
        def backtrack(start, path):
            if len(path) == 4 and start == len(s):
                res.append(".".join(path))
                return
            if len(path) == 4 or start == len(s):
                return
            for i in range(1, 4):
                if start + i > len(s):
                    break
                segment = s[start:start+i]
                if (segment[0] == '0' and len(segment) > 1) or int(segment) > 255:
                    continue
                backtrack(start + i, path + [segment])
        
        res = []
        backtrack(0, [])
        return res
# Time: O(3^4)=O(81) (since at each of the 4 segments, there are up to 3 choices).
# Space: O(1) (ignoring the space for the result).
# Input: s = "25525511135"
# Output: ["255.255.11.135","255.255.111.35"]
# Input: s = "0000"
# Output: ["0.0.0.0"]

# Zigzag conversion
# The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)
# P   A   H   N
# A P L S I I G
# Y   I   R
# We can move up and down with 1 and -1
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s

        idx, d = 0, 1
        rows = [[] for _ in range(numRows)]

        for char in s:
            rows[idx].append(char)
            if idx == 0:
                d = 1
            elif idx == numRows - 1:
                d = -1
            idx += d

        for i in range(numRows):
            rows[i] = ''.join(rows[i])

        return ''.join(rows)   


