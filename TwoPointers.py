# Two Pointer Technique
# Given a sorted array arr (sorted in ascending order) and a target, find if there exists any pair of elements (arr[i], arr[j]) such 
# that their sum is equal to the target.
# Input: arr[] = {10, 20, 35, 50}, target=70
# Output:  Yes
# Explanation : There is a pair (20, 50) with given target.

# Naive Method: O(n^2) Time and O(1) Space

# The very basic approach is to generate all the possible pairs and check if any of them add up to the target value. To generate all pairs, 
# we simply run two nested loops.
# arr = [0, -1, 2, -3, 1]
# target = -4

def two_sum(arr, target):
    for i in range(0, len(arr)-1):
        for j in range (i+1, len(arr)-1):
            if arr[i]+arr[j]==target:
                return True
    return False

# Recursive Binary Search Algorithm:  O(n*log(n)), O(1)

# Create a recursive function and compare the mid of the search space with the key. 
# And based on the result either return the index where the key is found or call the recursive function for the next search space.

def two_sum(arr, target):
    arr.sort()
    left, right = 0, len(arr)-1
    while left<right:
        sum = arr[left] + arr[right]
        if sum == target:
            return True
        elif sum < target: 
            left += 1  # Move left pointer to the right
        else:
            right -= 1 # Move right pointer to the left
    return False

## To print the pairs
def two_sum(arr, target):
    s = {}
    arr.sort()
    left, right = 0, len(arr)-1
    while left<right:
        sum = arr[left] + arr[right]
        if sum == target:
            s[arr[left]]=arr[right]
            left+=1
        elif sum < target: 
            left += 1  # Move left pointer to the right
        else:
            right -= 1 # Move right pointer to the left
    return s

# Using Hash Set – O(n) time and O(n) space
# Rather than checking every possible pair, we store each number in an unordered set during iterating over the array’s elements. 
# For each number, we calculate its complement (i.e., target – current number) and check if this complement exists in the set. 
# If it does, we have successfully found the pair that sums to the target. This approach significantly reduces the time complexity and
#  allowing us to solve the problem in linear time O(n).
# Algorithm
# 1. Create an empty Hash Set or Unordered Set
# 2. Iterate through the array and for each number in the array:
#     a. Calculate the complement (target – current number).
#     b. Check if the complement exists in the set:
#         * If it is, then pair found.
#         * If it isn’t, add the current number to the set.
# If the loop completes without finding a pair, return that no pair exists.
def two_sum(arr, target):
    # Create a set to store the elements
    s = {}

    # Iterate through each element in the array
    for i, num in enumerate(arr):
      
        # Calculate the complement that added to
        # num, equals the target
        complement = target - num

        # Check if the complement exists in the set
        if complement in s:
            return True #return [s[complement],i]

        # Add the current element to the set
        s[num]=i

    # If no pair is found
    return False
# Output
# {0}
# {0, -1}
# {0, 2, -1}
# {0, 2, -3, -1}
# {0, 1, 2, -3, -1}
# false

# 3Sum such that sum of them is zero, dont use duplictes # O(n^2), O(1)
# For each number, perform two pointer with next and last element
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        nums.sort() # O(nlogn)

        for i in range(len(nums)): # O(n^2)
            if i > 0 and nums[i] == nums[i-1]: # Same Numbers, skip
                continue
            
            j = i + 1
            k = len(nums) - 1

            while j < k:
                total = nums[i] + nums[j] + nums[k]

                if total > 0:
                    k -= 1
                elif total < 0:
                    j += 1
                else:
                    res.append([nums[i], nums[j], nums[k]])
                    j += 1

                    while nums[j] == nums[j-1] and j < k: #Same Numbers, skip
                        j += 1
        
        return res

# Valid Palindrome
class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = "".join( c.lower() for c in s if c.isalnum())
        l,r=0,len(s)-1
        while l<r:
            if s[l]!=s[r]:
                return False
            l+=1
            r-=1
        return True
# Input: s = "A man, a plan, a canal: Panama"
# Output: true
# Explanation: "amanaplanacanalpanama" is a palindrome.


# Trapping Rain water O(n), O(1)
class Solution:
    def trap(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        left_max = height[left]
        right_max = height[right]
        water = 0

        while left < right: # Add water between adjacent height
            if left_max < right_max:
                left += 1
                left_max = max(left_max, height[left])
                water += left_max - height[left]
            else:
                right -= 1
                right_max = max(right_max, height[right])
                water += right_max - height[right]
        
        return water

# Container with most water (Two-pointer) O(n), O(1)
# area=max(area,min(height[i],height[j])*(j-i))
class Solution(object):
    def maxArea(self, height):
        area = 0
        i,j=0,len(height)-1
        while i<j:
            area=max(area,min(height[i],height[j])*(j-i))
            if height[i]<height[j]:
                i+=1
            else:
                j-=1
        return area

# Move Zeros to End (Two-pointer) O(n), O(1)
# Using two pointer to swap two numbers.
# [1,1,0,1,0,1] -> [1, 1, 1, 1, 0, 0]
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        left = 0

        for right in range(len(nums)):
            if nums[right] != 0:
                nums[right], nums[left] = nums[left], nums[right]
                left += 1
        
        return nums
    
# Is Subsequence
# Problem: Given two strings s and t, check if s is a subsequence of t.
# A subsequence is formed by deleting zero or more characters from t without changing the order of the remaining characters.
# Examples:
# s = "abc", t = "ahbgdc" → True ("a", "b", "c" appear in order in t).
# s = "axc", t = "ahbgdc" → False ("a" and "c" appear, but "x" is missing).
def isSubsequence(s,t):
    i, j = 0, 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1  # Move to next character in `s`
        j += 1      # Always move in `t`
    return i == len(s)  # Did we match all of `s`?