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


# Maximum Subarray 
# Kadane's Algo O(n)
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:            
        max_sum = current_sum = nums[0]
        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        return max_sum
# Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
# Output: 6
# Explanation: The subarray [4,-1,2,1] has the largest sum 6.

# Print those intervals also
def max_subarray_with_elements(nums):
    max_sum = current_sum = nums[0]
    start = end = temp_start = 0

    for i in range(1, len(nums)):
        if nums[i] > current_sum + nums[i]:
            current_sum = nums[i]
            temp_start = i
        else:
            current_sum += nums[i]
        
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i

    return max_sum, nums[start:end + 1]

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

# Range Minimum Query (RMQ)
# Problem:
# Given an array, answer multiple queries to find the minimum element in a range [L, R] efficiently.
# Precompute minimums for intervals of length 2^k using dynamic programming.
# For a query [L, R], split the range into two overlapping intervals of length 2^j and take the minimum.
# Preprocessing: O(n log n)
# Query Time: O(1)
# Space: O(n log n)
import math
class RMQ:
    def __init__(self, arr):
        self.n = len(arr)
        self.k = math.floor(math.log2(self.n)) + 1
        self.st = [[0] * self.n for _ in range(self.k)]
        
        # Base case: intervals of length 1
        for i in range(self.n):
            self.st[0][i] = arr[i]
        
        # Precompute intervals of length 2^j
        for j in range(1, self.k):
            for i in range(self.n - (1 << j) + 1):
                self.st[j][i] = min(self.st[j-1][i], self.st[j-1][i + (1 << (j-1))])
    
    def query(self, L, R):
        length = R - L + 1
        j = math.floor(math.log2(length))
        return min(self.st[j][L], self.st[j][R - (1 << j) + 1])

# Example Usage:
arr = [2, 5, 1, 8, 3, 7]
rmq = RMQ(arr)
print(rmq.query(1, 4))  # Output: 1 (min in [5, 1, 8, 3])