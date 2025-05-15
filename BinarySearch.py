#Search in Rotated Sorted Array
#Find a sorted part in ascending order.
class Solution(object):
    def search(self, nums, target):

        left=0
        right=len(nums)-1
        while left<=right:
            mid=left+(right-left)//2
            if nums[mid]==target:
                return mid
            elif nums[mid] >= nums[left]:
                if nums[left] <= target <= nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] <= target <= nums[right]:
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
class Solution:
    def findMin(nums):
        low, high = 0, len(nums) - 1
        
        while low < high:
            mid = low + (high - low) // 2
            
            if nums[mid] < nums[high]:
                high = mid  # Minimum is in the left half (including mid)
            elif nums[mid] > nums[high]:
                low = mid + 1  # Minimum is in the right half (excluding mid)
            else:
                high -= 1  # Handle duplicates (cannot decide left/right)
        
        return nums[low]  # or nums[high], since low == high
# Best/Average Case: O(log n) (when duplicates are sparse).
# Worst Case: O(n) (when all elements are duplicates, e.g., [2,2,2,2]).


#Search a 2D Matrix
#Using binary search twice.
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
class BestSolution(object):
    def searchMatrix(self, matrix, target):

        m=len(matrix)
        n=len(matrix[0])
        
        i=m-1
        j=0
        
        while i>=0 and j<n:
            if matrix[i][j]==target:
                return True
            elif matrix[i][j]<target:
                j+=1
            else:
                i-=1
                
        return False
        
# Single Binary Search
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:        
        rows, cols = len(matrix), len(matrix[0])
        left, right = 0, rows * cols - 1

        while left <= right:
            mid = (left + right) // 2
            row, col = mid // cols, mid % cols
            guess = matrix[row][col]

            if guess == target:
                return True
            elif guess < target:
                left = mid + 1
            else:
                right = mid - 1

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
