# Search in Rotated Sorted Array - checking the sorted half’s range
def search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        # By checking the sorted half’s range, we can decide whether to search there or in the other half.
        # Check if left half is sorted
        if nums[left] <= nums[mid]:
            # Check if target is in the sorted left half
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half must be sorted
        else:
            # Check if target is in the sorted right half
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
        
#Find First and Last Position of Element in Sorted Array
#Using Binary Search twice for left most value and right most value
from bisect import bisect_left,bisect_right
class Solution(object):
    def searchRange(self, nums, target):

        left = bisect_left(nums,target)
        right = bisect_right(nums,target)
        if (right-left>1):
            return[left,right-1]
        elif (right-left==1):
            return [left,left]
        else:
            return [-1,-1]
        
#Find Minimum in Rotated Sorted Array
#Use part of input array to compare numbers.
class Solution:
    def findMin(self, nums: List[int]) -> int:
    
        left = 0
        right = len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            if nums[mid] <= nums[right]:
                right = mid
            else:
                left = mid + 1
        
        return nums[left]

# List may contain duplicates (Hard) 
# With Duplicates:
# If nums[mid] == nums[high], we cannot decide which half to search.
# Solution: Decrement high to eliminate the duplicate.
def findMin(nums):
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = (left + right) // 2
        
        if nums[mid] < nums[right]:
            right = mid
        elif nums[mid] > nums[right]:
            left = mid + 1
        else:
            right -= 1  # Handle duplicates
    
    return nums[left]
# Best/Average Case: O(log n) (when duplicates are sparse).
# Worst Case: O(n) (when all elements are duplicates, e.g., [2,2,2,2]).

# Search a 2D Matrix
# Approach
# Flatten the Matrix Conceptually:
#   Treat the 2D matrix as a 1D sorted array of size m * n.
# Binary Search:
#   Use row-major order to map the 1D index to 2D indices:
#     row = index // n
#     col = index % n
# Perform standard binary search on the virtual 1D array.
def searchMatrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
    
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_val = matrix[mid // n][mid % n]
        
        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False

# Example Usage
matrix = [
    [1, 3, 5, 7],
    [10, 11, 16, 20],
    [23, 30, 34, 60]
]
print(searchMatrix(matrix, 3))   # Output: True
print(searchMatrix(matrix, 13))  # Output: False
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        
        top = 0
        bot = len(matrix) - 1

        while top <= bot:
            mid = (top + bot) // 2

            if matrix[mid][0] < target and matrix[mid][-1] > target:
                break
            elif matrix[mid][0] > target:
                bot = mid - 1
            else:
                top = mid + 1
        
        row = (top + bot) // 2

        left = 0
        right = len(matrix[row]) - 1

        while left <= right:
            mid = (left + right) // 2

            if matrix[row][mid] == target:
                return True
            elif matrix[row][mid] > target:
                right = mid - 1
            else:
                left = mid + 1
        
        return False
    
# Search column-row sorted Matrix  
def searchMatrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
    
    m, n = len(matrix), len(matrix[0])
    row, col = 0, n - 1  # Start from top-right
    
    while row < m and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1  # Move left (eliminate column)
        else:
            row += 1  # Move down (eliminate row)
    
    return False

# Find a peak element index
# A peak element is an element that is strictly greater than its neighbors.
# nums [1,2,1,3,5,6,4]
# output: 5
class Solution:
    def findPeakElement(nums) :
        left = 0
        right = len(nums) - 1

        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[mid + 1]:
                right = mid
            else:
                left = mid + 1

        return left
