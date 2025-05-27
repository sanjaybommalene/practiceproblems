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

# Word Pattern
# Given a pattern and a string s, find if s follows the same pattern.
# Here follow means a full match, such that there is a bijection between a letter in pattern and a non-empty word in s. Specifically:
# Each letter in pattern maps to exactly one unique word in s.
# Each unique word in s maps to exactly one letter in pattern.
# No two letters map to the same word, and no two words map to the same letter.
# A bijection is both onto and one-to-one. 
class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:

        s = s.split()

        return (len(set(pattern)) ==
                len(set(s)) ==
                len(set(zip_longest(pattern,s))))

# Subarray Sum Equals K O(N)
# Iterate through nums:
# Update prefix_sum += nums[i].
# If prefix_sum - k exists in sum_map, add sum_map[prefix_sum - k] to count.
# Increment sum_map[prefix_sum] by 1.
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        sub_num = {0:1}
        prefix_sum = count = 0

        for n in nums:
            prefix_sum+=n

            if prefix_sum - k in sub_num:
                count+=sub_num[prefix_sum-k]
            
            sub_num[prefix_sum] = 1+sub_num.get(prefix_sum, 0)
        return count
# Input: nums = [1,1,1], k = 2
# Output: 2
# Input: nums = [1,2,3], k = 3
# Output: 2

# Subarray Sum Equals K O(N^2),O(N) Return SubArray
def subarraySum(nums, k):
    prefix_sum = 0
    sum_map = {}
    sum_map[0] = [-1]  # Base case for subarrays starting at index 0
    result = []

    for i, num in enumerate(nums):
        prefix_sum += num
        # Check if (prefix_sum - k) exists in the map
        if prefix_sum - k in sum_map:
            for start in sum_map[prefix_sum - k]:
                result.append(nums[start + 1 : i + 1])
        # Update the map with the current prefix_sum
        if prefix_sum in sum_map:
            sum_map[prefix_sum].append(i)
        else:
            sum_map[prefix_sum] = [i]
    
    return result
