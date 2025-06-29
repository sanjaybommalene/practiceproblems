#Find duplicates in array
#Naive Approach O(n)
def findDuplicate(self, nums):
    n = len(nums)
    count = [0] * n
    for num in nums:
        count[num]+=1
        if (count[num]>1):
            return num
    return 0
def findDuplicate(self, nums):
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)
# Hare and Tortoise Algo //Only if all values less than index length
# Loop detection and 2nd phase where they meet is where cycle start
def find_duplicate(nums):
    # Step 1: Initialize slow and fast pointers
    slow = nums[0]
    fast = nums[0]
    
    # Step 2: Move slow by 1 step and fast by 2 steps until they meet
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break  # Cycle detected

    # Step 3: Find entry point of cycle (duplicate number)
    slow = nums[0]  # Reset slow to start
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    
    return slow  # The duplicate number

# Example Usage
nums = [3, 1, 3, 4, 2]
print("Duplicate Number:", find_duplicate(nums))

# Maximum Sum Subarray 
# Kadane's Algo O(n)
def max_subarray(nums):
    if not nums:
        return 0
    
    max_current = max_global = nums[0]
    
    for num in nums[1:]:
        max_current = max(num, max_current + num)
        max_global = max(max_global, max_current)
    
    return max_global
# Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
# Output: 6
# Explanation: The subarray [4,-1,2,1] has the largest sum 6.

# Print those intervals also
def max_subarray(nums):
    if not nums:
        return [], 0  # Handle empty array case
    
    max_current = max_global = nums[0]
    start = end = temp_start = 0
    
    for i in range(1, len(nums)):
        if nums[i] > max_current + nums[i]: # Start i when new current max is found
            max_current = nums[i]
            temp_start = i
        else:
            max_current += nums[i]
        
        if max_current > max_global: # Update start and end when new global max is found
            max_global = max_current
            start = temp_start
            end = i
    
    max_subarray = nums[start : end + 1]
    return max_subarray, max_global

# Merge Intervals O(n),O(n)
# x:x[0] should be sorted
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:        
        if not intervals:
            return []

        # Sort intervals by starting time
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]

        for current in intervals[1:]:
            last = merged[-1]
            if current[0] <= last[1]:  # Overlap detected
                last[1] = max(last[1], current[1])  # Merge
            else:
                merged.append(current)

        return merged
# Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
# Output: [[1,6],[8,10],[15,18]]
# Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

# Sort Color in-place # Count Sort O(n+3)
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        count = {}
        for i in range(len(nums)):
            count[nums[i]] = count.get(nums[i], 0) + 1
        idx = 0
        for color in range(3): # Get Freq and add those no of color to list
            freq = count.get(color, 0)
            nums[idx : idx + freq] = [color] * freq
            idx += freq
    
# Product of Array except self  O(n+n)
# For a given number check multiply from left and then multiply with right elements  
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        output = [1] * len(nums)
        
        left = 1
        for i in range(len(nums)):
            output[i] *= left
            left *= nums[i]
        
        right = 1
        for i in range(len(nums) - 1, -1, -1):
            output[i] *= right
            right *= nums[i]
    
        return output        

# House Robber
class Solution:
    def rob(self, nums: List[int]) -> int:
        prev_rob = max_rob = 0
        # prev_rob: Maximum profit if the thief robs up to house i-2.
        # max_rob: Maximum profit if the thief robs up to house i-1.
        for cur_val in nums:
            temp = max(max_rob, prev_rob + cur_val)
            prev_rob = max_rob
            max_rob = temp
        
        return max_rob
# Input: nums = [1,2,3,1]
# Output: 4
# Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
# Total amount you can rob = 1 + 3 = 4.

# House Robber II
# Approach

# The key insight is that since the houses are circular, we can't rob both the first and last houses. Therefore, we can break the problem into two cases:

# Rob houses from 0 to n-2 (excluding the last house)
# Rob houses from 1 to n-1 (excluding the first house)
def rob(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    def simple_rob(nums):
        prev_max = 0
        curr_max = 0
        for num in nums:
            temp = curr_max
            curr_max = max(prev_max + num, curr_max)
            prev_max = temp
        return curr_max
    
    # Case 1: Rob houses 0 to n-2
    case1 = simple_rob(nums[:-1])
    # Case 2: Rob houses 1 to n-1
    case2 = simple_rob(nums[1:])
    
    return max(case1, case2)

# Palindrome Number
# Using Remainder
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False

        reverse = 0
        xcopy = x

        while x > 0:
            reverse = (reverse * 10) + (x % 10)
            x //= 10
        
        return reverse == xcopy

# Trailing Zeros in factorial
class Solution:
    def trailingZeroes(self, n: int) -> int:
        res = 0
        while n > 0:
            n //= 5 # Count multiples of 5, 25, 125, etc.
            res += n
        return res

# Buildings With an Ocean View O(n), O(k)
def findBuildings(heights):
    n = len(heights)
    res = []
    max_height = float('-inf')
    
    for i in range(n - 1, -1, -1):  # Traverse from right to left
        if heights[i] > max_height:
            res.append(i)  # Current building has ocean view
            max_height = heights[i]  # Update max_height
    
    return res[::-1]  # Reverse to return indices in increasing order
# print(findBuildings([4,2,3,1]))  
# # Output: [0, 2, 3]
# print(findBuildings([1,3,2,4]))  
# # Output: [3]

# We can avoid the reversal altogether by prepending indices into the result list.
def findBuildings(heights):
    n = len(heights)
    res = []
    max_height = float('-inf')
    
    for i in range(n - 1, -1, -1):
        if heights[i] > max_height:
            res.insert(0, i)  # Insert at the beginning
            max_height = heights[i]
    
    return res

# Construct K Palindrome Strings O(n), O(1)
# Character Frequency Analysis:
#   A palindrome can have at most one character with an odd count (for the middle of odd-length palindromes).
#   The minimum number of palindromes (min_palindromes) is determined by the number of characters with odd counts.
#   The maximum number of palindromes (max_palindromes) is the length of the string (each character as a separate palindrome).
# Feasibility Check:
#   If k is between min_palindromes and max_palindromes, it’s possible.
# Input: s = "annabelle", k = 2
# Output: true
# Explanation: You can construct two palindromes using all characters in s.
# Some possible constructions "anna" + "elble", "anbna" + "elle", "anellena" + "b"
class Solution(object):
    def canConstruct(self, s, k):
        if k > len(s):
            return False  # Cannot create more palindromes than characters
        
        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1
        
        odd_count = sum(1 for count in freq.values() if count % 2 != 0)
        
        return odd_count <= k <= len(s)

# Length of Last but one Word
class Solution:
    def lengthOfLastWord(self, s: str) -> int:                
        end = len(s) - 1

        while s[end] == " ":
            end -= 1
        
        start = end
        while start >= 0 and s[start] != " ":
            start -= 1
        
        return end - start
    
# Reverse words in a sentence
class Solution:
    def reverseWords(self, s: str) -> str:
        words = s.split()
        res = []

        for i in range(len(words) - 1, -1, -1):
            res.append(words[i])
            if i != 0:
                res.append(" ")

        return "".join(res)

# Find the Index of the First Occurrence in a String
# Given two strings needle and haystack, return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.
# Input: haystack = "sadbutsad", needle = "sad"
# Output: 0
# Explanation: "sad" occurs at index 0 and 6.
# Slice a string of haystack.
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:

        if len(haystack) < len(needle):
            return -1

        for i in range(len(haystack)):
            if haystack[i:i+len(needle)] == needle:
                return i

        return -1 
         
# Gas Station
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        if sum(gas) < sum(cost):
            return -1
                
        curernt_gas = 0
        start = 0
        for i in range(len(gas)):
            curernt_gas += gas[i] - cost[i]
            if curernt_gas < 0:
                curernt_gas = 0
                start = i + 1

        return start
# Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
# Output: 3
# Explanation:
# Start at station 3 (index 3) and fill up with 4 unit of gas. Your tank = 0 + 4 = 4
# Travel to station 4. Your tank = 4 - 1 + 5 = 8
# Travel to station 0. Your tank = 8 - 2 + 1 = 7
# Travel to station 1. Your tank = 7 - 3 + 2 = 6
# Travel to station 2. Your tank = 6 - 4 + 3 = 5
# Travel to station 3. The cost is 5. Your gas is just enough to travel back to station 3.
# Therefore, return 3 as the starting index.

# ✅ 2. Partition Sorted Array into K Groups Minimizing Total Range

# 🔍 Problem:
# Given a sorted array arr and integer k, divide the array into k contiguous groups such that:
# Cost = sum of (max - min) for each group is minimized.
# 🧠 Intuition:
# Since array is sorted, max - min of a group = arr[end] - arr[start].
# Grouping fewer adjacent elements reduces cost. So split at largest gaps.
# ✅ Approach:
# Compute all consecutive gaps: arr[i+1] - arr[i].
# Select (k-1) largest gaps as split points → reduces (max - min) in each group.
# Total cost = arr[-1] - arr[0] - sum of (k-1) largest gaps.
# ⏱ Time: O(N log N)
# 📦 Space: O(N)
def min_total_range(arr, k):
    if k == 1:
        return arr[-1] - arr[0]
    if k >= len(arr):
        return 0
    
    # Calculate differences between consecutive elements
    gaps = []
    for i in range(1, len(arr)):
        gaps.append(arr[i] - arr[i-1])
    
    # Sort the differences in descending order
    gaps.sort(reverse=True)
    
    # The sum is (total range) - (sum of k-1 largest gaps)
    total_range = arr[-1] - arr[0]
    sum_of_gaps = sum(gaps[:k-1])
    
    return total_range - sum_of_gaps
# For example, with array [1,3,7,10] and k=2:
# Differences: [2,4,3]
# We remove the (k-1) largest gap (4), making groups [1,3] and [7,10]
# Sum is (3-1) + (10-7) = 5, which equals (10-1) - 4 = 5

# Q2. Given a number num, two adjacent digits can be swapped if their parity is the same, that is, both are odd or both are even. For example, (5, 9) have the same parity, but (6,9) do not.
# Find the largest number that can be created. The swap operation can be applied any number of time:
# Example
# Let num = "7596801".
# • Swap 5 and 9 - "7956801"
# • Swap 7 and 9 →> "9756801"
# • Swap 6 and 8 -> "9758601"
# The largest value possible is "9758601"
def largest_num_parity_swap(num_str):
    num = list(num_str)
    n = len(num)
    
    # Separate the digits into even and odd lists while preserving original order
    evens = []
    odds = []
    for digit in num:
        if int(digit) % 2 == 0:
            evens.append(digit)
        else:
            odds.append(digit)
    
    # Sort each group in descending order
    evens.sort(reverse=True)
    odds.sort(reverse=True)
    
    # Reconstruct the number by picking from the appropriate group
    result = []
    even_ptr = 0
    odd_ptr = 0
    for digit in num:
        if int(digit) % 2 == 0:
            result.append(evens[even_ptr])
            even_ptr += 1
        else:
            result.append(odds[odd_ptr])
            odd_ptr += 1
    
    return ''.join(result)
# Explanation
# Separate Parity Groups: The digits of the input number are divided into two lists: one for even digits and one for odd digits. The order of digits in these lists matches their original positions in the input number.
# Sort Groups: Each list (even and odd) is sorted in descending order. This ensures that the largest digits are at the front of their respective lists.
# Reconstruct Number: The original number is reconstructed by iterating through each digit of the input number. For each digit, if it was even, the next largest even digit from the sorted even list is placed in its position; similarly for odd digits. This step ensures that digits are swapped only within their parity groups, adhering to the problem constraints.
# For example, with the input "7596801":
# Even digits extracted in order: 6, 8, 0 → sorted: 8, 6, 0
# Odd digits extracted in order: 7, 5, 9, 1 → sorted: 9, 7, 5, 1
# Reconstructing:
# Original digits: 7(odd),5(odd),9(odd),6(even),8(even),0(even),1(odd)
# Replaced with: 9,7,5,8,6,0,1 → "9758601"


# Given an array of integers, find the maximum possible even sum of its elements.

# Example Testcase: [2,3,6,-5,10,1,1]
# Expected output: 22
def max_even_sum(arr):
    total_sum = sum(num for num in arr if num > 0)
    
    if total_sum % 2 == 0:
        return total_sum
    
    # Find the smallest positive odd and largest negative odd
    smallest_pos_odd = float('inf')
    largest_neg_odd = -float('inf')
    
    for num in arr:
        if num % 2 != 0:
            if num > 0 and num < smallest_pos_odd:
                smallest_pos_odd = num
            elif num < 0 and num > largest_neg_odd:
                largest_neg_odd = num
    
    candidates = []
    if smallest_pos_odd != float('inf'):
        candidates.append(total_sum - smallest_pos_odd)
    if largest_neg_odd != -float('inf'):
        candidates.append(total_sum + largest_neg_odd)
    
    return max(candidates) if candidates else 0

# Example Testcase
arr = [2, 3, 6, -5, 10, 1, 1]
print(max_even_sum(arr))  # Output: 22

# Q2: In an API request optimization system, a sequence of binary request codes represented by requestSeq, consits of '0' and '1'. 
# The system requires the sequence to be divided into non-overlapping, even-length segments, where each segment contains only identical request codes, either all 1's or all 0's. Implement a function to calculate the minimum number of request code flips(changing '0' to '1' or '1' to '0') required to meet the given system requirement.# 
# Constraints:
# 2 <= requestSeq <= 10^5
# The length of requestSeq is even.
# rquestSeq contains only 1's and 0's.
# Example input #1: "11010010" . Output = 2. You can flip two 1's to get "1111000".
# Example input #2: "101011" . Output = 2. You can flip two 0's to get "111111".

def minFlips(requestSeq):
    flips = 0
    # Iterate through the string in steps of 2
    for i in range(0, len(requestSeq), 2):
        # If the pair differs, increment flips
        if requestSeq[i] != requestSeq[i + 1]:
            flips += 1
    return flips
# Since segments must be of even length and contain identical characters, the simplest approach is to assume segments of length 2 (e.g., 00 or 11), as larger even-length segments (e.g., length 4) are combinations of smaller segments.

# Problem Statement
# Given a string s, return the last substring of s in lexicographical order. A substring is a contiguous sequence of characters within the string. 
# The last substring in lexicographical order is the one that would appear last if all possible substrings were sorted alphabetically.
# Constraints:
# 1 <= s.length <= 4 * 10^5
# s contains only lowercase English letters.
# Example 1: Input: s = "abab"
# Output: "bab"
# Explanation: Substrings are ["a", "ab", "aba", "abab", "b", "ba", "bab"]. Sorted lexicographically: ["a", "ab", "aba", "abab", "b", "ba", "bab"]. The last one is "bab".
# Example 2: Input: s = "leetcode"
# Output: "tcode"
# Explanation: The last substring in lexicographical order is "tcode", starting from the letter 't'.
def largest_substring(s):
    max_char = max(s)
    for i in range(len(s)):
        if s[i] == max_char:
            return s[i:]
    return s

def lastSubstring(s: str) -> str:
    # Initialize pointers and max character
    i = 0  # Current candidate for the start of the largest substring
    j = 1  # Next position to compare
    k = 0  # Offset for character comparison
    n = len(s)
    
    while j + k < n:
        if s[i + k] == s[j + k]:
            # Characters match, continue comparing
            k += 1
        elif s[i + k] > s[j + k]:
            # Current substring at i is larger, move j forward
            j = j + k + 1
            k = 0
        else:
            # Substring at j is larger, update i to j
            i = max(i + k + 1, j)
            j = i + 1
            k = 0
    
    return s[i:]

### ✅ **1. First Unique Character in a String**

# **Problem:** Find the index of the first non-repeating character in a string.
# **Input:** `"leetcode"`
# **Output:** `0`
# **Approach:** Count frequency with `Counter`, then find the first character with frequency `1`.
from collections import Counter

def first_uniq_char(s: str) -> int:
    freq = Counter(s)  # Count each character
    for i, ch in enumerate(s):
        if freq[ch] == 1:  # First character with frequency 1
            return i
    return -1


### ✅ **2. Remove All Adjacent Duplicates In String**

# **Problem:** Remove pairs of adjacent duplicates repeatedly.
# **Input:** `"abbaca"`
# **Output:** `"ca"`
# **Approach:** Use a stack to remove adjacent duplicates in one pass.
def remove_adjacent_duplicates(s: str) -> str:
    stack = []
    for ch in s:
        if stack and stack[-1] == ch:  # Remove adjacent duplicate
            stack.pop()
        else:
            stack.append(ch)
    return ''.join(stack)  # Reconstruct string from stack

### ✅ **3. String Compression**

# **Problem:** Compress repeated characters in-place and return new length.
# **Input:** `["a","a","b","b","c","c","c"]`
# **Output:** `6`
# **Resulting Array:** `["a","2","b","2","c","3"]`
# **Approach:** Two pointers (`read`, `write`) with compression count as string.
def compress(chars: list[str]) -> int:
    write = left = right = 0  # Two pointers
    while left < len(chars):
        right = left
        # Count consecutive characters
        while right < len(chars) and chars[right] == chars[left]:
            right += 1
        chars[write] = chars[left]
        write += 1
        count = right - left
        if count > 0:
            chars[write] = str(count)
            write += 1
        left = right
    return write  # New length of array

### ✅ **5. Check If a Word Occurs As a Prefix of Any Word in a Sentence**

# **Input:** `"i love eating burger"`, searchWord: `"burg"`
# **Output:** `4`
# **Approach:** Split sentence and check if any word starts with `searchWord`.
def isPrefixOfWord(sentence: str, searchWord: str) -> int:
    words = sentence.split()
    for i, word in enumerate(words, 1):
        if word.startswith(searchWord):
            return i
    return -1

### ✅ **6. Remove Duplicate Letters**

# **Problem:** Remove duplicate letters so that every letter appears once and the result is smallest lexicographically.
# **Input:** `"cbacdcbc"`
# **Output:** `"acdb"`
# **Approach:** Stack + Greedy + Track last occurrence and seen characters.
def remove_duplicate_letters(s: str) -> str:
    last_occurrence = {ch: i for i, ch in enumerate(s)}  # Last index of each char
    stack = []
    seen = set()

    for i, ch in enumerate(s):
        if ch in seen:
            continue
        # Remove chars that are greater and can appear later
        while stack and ch < stack[-1] and i < last_occurrence[stack[-1]]:
            removed = stack.pop()
            seen.remove(removed)
        stack.append(ch)
        seen.add(ch)
    return ''.join(stack)

# Median of Two Sorted Arrays O(log(min(m, n))) , O(1)
# Median is the middle value in a sorted list.
# If total length is even → median = average of two middle values.
# If total length is odd → median = middle element.
# Ensure nums1 is the smaller array (swap if needed for optimization).
# Binary Search on nums1:
# We want to partition both arrays such that:
# Left part of both arrays has half elements
# All elements in left ≤ all elements in right
#   low = 0, high = m (size of nums1).
#   partitionX = (low + high) // 2 (mid of nums1).
#   partitionY = (m + n + 1) // 2 - partitionX (balancing point in nums2).
# Check Partition Validity:
#   maxLeftX = max element on the left of nums1.
#   minRightX = min element on the right of nums1.
#   maxLeftY = max element on the left of nums2.
#   minRightY = min element on the right of nums2.
#   Valid if: maxLeftX ≤ minRightY and maxLeftY ≤ minRightX.
# Adjust Binary Search:
#   If maxLeftX > minRightY: move high = partitionX - 1.
#   Else: move low = partitionX + 1.
# Compute Median:
#   If (m + n) is even: (max(maxLeftX, maxLeftY) + min(minRightX, minRightY)) / 2.
#   Else: max(maxLeftX, maxLeftY).
def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    low, high = 0, m

    while low <= high:
        i = (low + high) // 2
        j = (m + n + 1) // 2 - i  # because total left half should have (m + n + 1)//2 elements

        maxLeftX = float('-inf') if i == 0 else nums1[i - 1]
        minRightX = float('inf') if i == m else nums1[i]

        maxLeftY = float('-inf') if j == 0 else nums2[j - 1]
        minRightY = float('inf') if j == n else nums2[j]

        if maxLeftX <= minRightY and maxLeftY <= minRightX:
            if (m + n) % 2 == 0:
                return (max(maxLeftX, maxLeftY) + min(minRightX, minRightY)) / 2
            else:
                return max(maxLeftX, maxLeftY)
        elif maxLeftX > minRightY:
            high = i - 1
        else:
            low = i + 1

# Range Minimum Query (RMQ)
# Problem:
# Given an array, answer multiple queries to find the minimum element in a range [L, R] efficiently.
# Precompute minimums for intervals of length 2^k using dynamic programming.
# For a query [L, R], split the range into two overlapping intervals of length 2^j and take the minimum.
# Preprocessing: O(n log n)
# Query Time: O(1)
# Space: O(n log n)
# A Sparse Table is a preprocessing technique used to answer range minimum/maximum/gcd queries in constant time O(1) after a O(n log n) preprocessing step.
# We preprocess the array to answer min(i, j) by storing answers for all ranges of length 2^k starting at every index.
# Let:
# st[i][j] = minimum value in the subarray starting at index i and of length 2^j.
import math

class RMQ:
    def __init__(self, arr):
        self.n = len(arr)
        self.k = int(math.log2(self.n)) + 1  # max power of 2 needed
        self.st = [[0] * self.k for _ in range(self.n)]

        # Initialize st[i][0] with the original array values
        for i in range(self.n):
            self.st[i][0] = arr[i]

        # Build the Sparse Table
        for j in range(1, self.k):  # power of 2: 2^1, 2^2, ..., 2^k
            for i in range(self.n - (1 << j) + 1):  # valid start indices
                # Combine two overlapping intervals of length 2^(j-1)
                self.st[i][j] = min(
                    self.st[i][j - 1],
                    self.st[i + (1 << (j - 1))][j - 1]
                )

    def query(self, l, r):
        j = int(math.log2(r - l + 1)) # max power of 2 in range size
        return min(self.st[l][j], self.st[r - (1 << j) + 1][j])


# Example Usage:
arr = [2, 5, 1, 8, 3, 7]
rmq = RMQ(arr)
print(rmq.query(1, 4))  # Output: 1 (min in [5, 1, 8, 3])