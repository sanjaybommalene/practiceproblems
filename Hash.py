# Minimum Deletions to Make Character Frequencies Unique Time: O(n); note that the second loop will not have more than 26 * 26 total operations.
class Solution:
    def minDeletions(self, s: str) -> int:
        count,res,used = collections.Counter(s),0,set()
        for ch, freq in count.items():
            while freq>0 and freq in used:
                freq-=1
                res+=1
            used.add(freq)
        return res
    
# Group Anagrams O(N * K log K), O(N * K)
class Solution:
    def groupAnagrams(strs):
        anagram_map = {}
        
        for s in strs:
            # Sort the string to use as key
            sorted_str = ''.join(sorted(s))
            
            # Add to dictionary with sorted string as key
            if sorted_str not in anagram_map:
                anagram_map[sorted_str] = []
            anagram_map[sorted_str].append(s)
        
        # Return list of anagram groups
        return list(anagram_map.values())
# Input: strs = ["eat","tea","tan","ate","nat","bat"]
# Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

# Valid Anagram
# Count all characters in each string
# Given two strings s and t, return true if t is an anagram of s, and false otherwise.
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:  
        if len(s) != len(t):
            return False

        counter = {}

        for char in s:
            counter[char] = counter.get(char, 0) + 1

        for char in t:
            if char not in counter or counter[char] == 0:
                return False
            counter[char] -= 1

        return True
# Example 1:
# Input: s = "anagram", t = "nagaram"
# Output: true

# Longest Consecutive Sequence O(N),O(N)
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        longest = 0
        num_set = set(nums)
        for n in num_set:
            if (n-1) not in num_set:
                length = 1
                while (n+length) in num_set:
                    length+=1
                longest = max(longest, length)
        return longest
# Input: nums = [100,4,200,1,3,2]
# Output: 4
# Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.

# Ransom Note
# Given two strings ransomNote and magazine, return true if ransomNote can be constructed by using the letters from magazine and false otherwise.
# Counting each character.
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        maga_hash = {}

        for c in magazine:
            maga_hash[c] = 1 + maga_hash.get(c, 0)

        for c in ransomNote:
            if c not in maga_hash or maga_hash[c] <= 0:
                return False
            maga_hash[c] -= 1
        
        return True

# Isomorphic Strings
# Given two strings s and t, determine if they are isomorphic.
# Two strings s and t are isomorphic if the characters in s can be replaced to get t.
class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        char_index_s = {}
        char_index_t = {}

        for i in range(len(s)):
            if s[i] not in char_index_s:
                char_index_s[s[i]] = i

            if t[i] not in char_index_t:
                char_index_t[t[i]] = i
            
            if char_index_s[s[i]] != char_index_t[t[i]]:
                return False

        return True
# Input: s = "egg", t = "add"
# Output: true
# Explanation:
# The strings s and t can be made identical by:
# Mapping 'e' to 'a'.
# Mapping 'g' to 'd'.

# Write an algorithm to determine if a number n is happy.
# A happy number is a number defined by the following process:
# Starting with any positive integer, replace the number by the sum of the squares of its digits.
# Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
# Those numbers for which this process ends in 1 are happy.
# Using remainder.
class Solution:
    def isHappy(self, n: int) -> bool:    
        visit = set()
        
        def get_next_number(n):    
            output = 0
            
            while n:
                digit = n % 10
                output += digit ** 2
                n = n // 10
            
            return output

        while n not in visit:
            visit.add(n)
            n = get_next_number(n)
            if n == 1:
                return True
        
        return False
    
# Contains Duplicate II
# Given an integer array nums and an integer k, return true if there are two distinct indices i and j in the array such that nums[i] == nums[j] and abs(i - j) <= k.
class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        seen = {}

        for i, val in enumerate(nums):
            if val in seen and i - seen[val] <= k:
                return True
            else:
                seen[val] = i
        
        return False
# Input: nums = [1,0,1,1], k = 1
# Output: true
# Input: nums = [1,2,3,1], k = 3
# Output: true
# Input: nums = [1,2,3,1,2,3], k = 2
# Output: false

# Word Pattern O(n), O(n)
# Given a pattern and a string s, find if s follows the same pattern.
# Here follow means a full match, such that there is a bijection between a letter in pattern and a non-empty word in s. Specifically:
# Each letter in pattern maps to exactly one unique word in s.
# Each unique word in s maps to exactly one letter in pattern.
# No two letters map to the same word, and no two words map to the same letter.
# A bijection is both onto and one-to-one. 
# Example 1:
# Input: pattern = "abba", s = "dog cat cat dog"
# Output: true
# Explanation:
# The bijection can be established as:
# 'a' maps to "dog".
# 'b' maps to "cat".
# Example 2:
# Input: pattern = "abba", s = "dog cat cat fish"
# Output: false
# Example 3:
# Input: pattern = "aaaa", s = "dog cat cat dog"
# Output: false
def word_pattern(pattern: str, s: str) -> bool:
    # Split the string into words
    words = s.split()
    
    # If the lengths are not equal, they can't match
    if len(pattern) != len(words):
        return False

    # Create two dictionaries to track the mappings
    char_to_word = {}
    word_to_char = {}

    for char, word in zip(pattern, words):
        # Check if character was previously mapped
        if char in char_to_word:
            if char_to_word[char] != word:
                return False  # Mapping mismatch
        else:
            char_to_word[char] = word  # New mapping

        # Check if word was previously mapped
        if word in word_to_char:
            if word_to_char[word] != char:
                return False  # Mapping mismatch
        else:
            word_to_char[word] = char  # New reverse mapping

    return True


# Subarray Sum Equals K O(N), O(N)
# Given an array of integers nums and an integer k, return the total number of continuous subarrays whose sum equals to k.
# Iterate through nums:
# Update prefix_sum += nums[i].
# If prefix_sum - k exists in sum_map, add sum_map[prefix_sum - k] to count.
# Increment sum_map[prefix_sum] by 1.
def subarray_sum_count(nums, k):
    count = 0               # To count the number of subarrays summing to k
    current_sum = 0         # To track the prefix sum while iterating
    prefix_sums = {0: 1}    # Hash map to store prefix sum frequencies
                            # Initial entry: sum 0 has occurred once (important base case)

    for num in nums:
        current_sum += num  # Update current prefix sum

        # Check if there's a prefix sum such that current_sum - k == that prefix
        # If yes, it means the subarray between that prefix and current index sums to k
        if (current_sum - k) in prefix_sums:
            count += prefix_sums[current_sum - k]  # Add the number of times that prefix has occurred

        # Update the count of the current prefix sum in the map
        prefix_sums[current_sum] = prefix_sums.get(current_sum, 0) + 1

    return count
# nums = [1, 2, 3], k = 3

# current_sum = 0
# prefix_sums = {0:1}

# i=0: num=1 → current_sum = 1 → 1-3 = -2 → not in map  
#     → update map: {0:1, 1:1}

# i=1: num=2 → current_sum = 3 → 3-3 = 0 → map[0] = 1  
#     → count += 1 → update map: {0:1, 1:1, 3:1}

# i=2: num=3 → current_sum = 6 → 6-3 = 3 → map[3] = 1  
#     → count += 1 → update map: {0:1, 1:1, 3:1, 6:1}

# Return count = 2


# Input: nums = [1,1,1], k = 2
# Output: 2
# Input: nums = [1,2,3], k = 3
# Output: 2

# Subarray Sum Equals K O(N),O(N) Return SubArray
from collections import defaultdict

def subarray_sum_list_optimized(nums, k):
    result = []  # Final list of subarrays
    prefix_sum = 0
    prefix_map = defaultdict(list)  # Map: prefix_sum → list of indices where it occurs

    # Add initial prefix_sum = 0 at index -1 (to handle subarrays starting at index 0)
    prefix_map[0].append(-1)

    for i, num in enumerate(nums):
        prefix_sum += num

        # If current prefix_sum - k exists, collect all starting indices
        if (prefix_sum - k) in prefix_map:
            for start_index in prefix_map[prefix_sum - k]:
                # Add subarray from start_index+1 to i
                result.append(nums[start_index + 1: i + 1])

        # Record current index for current prefix_sum
        prefix_map[prefix_sum].append(i)

    return result
# nums = [1, 2, 1, 3], k = 3

# prefix_sums:
# i=0 → sum=1
# i=1 → sum=3 → sum-k = 0 → map[0] = [-1] → [1,2]
# i=2 → sum=4 → sum-k = 1 → map[1] = [0] → [2,1]
# i=3 → sum=7 → sum-k = 4 → map[4] = [2] → [3]

def subarray_sum_list(nums, k):
    result = []  # List to store all valid subarrays

    # Try every starting index
    for start in range(len(nums)):
        total = 0  # Initialize sum for the subarray starting at `start`

        # Try every ending index from `start` to the end of the array
        for end in range(start, len(nums)):
            total += nums[end]  # Add current element to the running sum

            if total == k:
                # If subarray sum equals k, store the subarray slice
                result.append(nums[start:end + 1])

    return result
# nums = [1, 2, 3]
# k = 3

# start=0:
#   end=0 → total = 1
#   end=1 → total = 3 → [1, 2]
#   end=2 → total = 6

# start=1:
#   end=1 → total = 2
#   end=2 → total = 5

# start=2:
#   end=2 → total = 3 → [3]

# Output: [[1, 2], [3]]

