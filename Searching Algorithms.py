# Binary Search - Sorted Array O(logN), O(1)
def binarySearch(arr, low, high, x):

    while low <= high:
        mid = low + (high - low) // 2

        if arr[mid] == x:
            return mid

        elif arr[mid] < x:
            low = mid + 1

        else:
            high = mid - 1

    # If we reach here, then the element
    # was not present
    return -1

# Recursive Binary Search 
# Returns index of x in arr if present, else -1
def binarySearch(arr, low, high, x):

    # Check base case
    if high >= low:

        mid = low + (high - low) // 2
        if arr[mid] == x:
            return mid
        # If element is smaller than mid, then it can only be present in left subarray
        elif arr[mid] > x:
            return binarySearch(arr, low, mid-1, x)
        # Else the element can only be present in right subarray
        else:
            return binarySearch(arr, mid + 1, high, x)
        
    else:
        return -1

if __name__ == '__main__':
    arr = [2, 3, 4, 10, 40]
    x = 10

    result = binarySearch(arr, 0, len(arr)-1, x)
    if result != -1:
        print("Element is present at index", result)
    else:
        print("Element is not present in array")

# Longest increasing sequence in an Array

# Naive Approach O(n*2)
def longest_increasing_subsequence(arr):
    n = len(arr)
    if n == 0:
        return 0

    dp = [1] * n  # Initialize LIS length for each element as 1

    for i in range(n):
        for j in range(i):
            if arr[i] > arr[j]:  # Check if increasing
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)  # The longest LIS

# Using Binary Search O(nlogn)
from bisect import bisect_left

def longest_increasing_subsequence(arr):
    sub = []  # List to store the LIS

    for num in arr:
        pos = bisect_left(sub, num)  # Find insertion position

        if pos == len(sub):
            sub.append(num)  # Extend LIS
        else:
            sub[pos] = num  # Replace element at found position

    return len(sub)  # LIS length

# Example Usage
arr = [10, 9, 2, 5, 3, 7, 101, 18]
print(longest_increasing_subsequence(arr))  # Output: 4 (LIS: [2, 3, 7, 101])

# Longest increasing sequence by the boundary elements of an Array
def longest_sequence(arr):
    l, r = 0, len(arr) - 1
    prev = float('-inf')  # Using negative infinity instead of sys.maxsize
    count = 0

    while l <= r:
        # Select the element that can be added to LIS while being the smallest
        if arr[l] > prev and arr[r] > prev:
            if arr[l] < arr[r]:
                prev = arr[l]
                l += 1
            else:
                prev = arr[r]
                r -= 1
            count += 1
        elif arr[l] > prev:
            prev = arr[l]
            l += 1
            count += 1
        elif arr[r] > prev:
            prev = arr[r]
            r -= 1
            count += 1
        else:
            break  # Stop if neither element can be added

    return count

# Example Usage
arr = [10, 20, 30, 25, 15, 40, 50]
print(longest_sequence(arr))

def longest_sequence_recursive(arr, left, right, prev):
    # Base case: if pointers cross each other
    if left > right:
        return 0

    count1 = count2 = 0

    # Take the left element if it can be part of LIS
    if arr[left] > prev:
        count1 = 1 + longest_sequence_recursive(arr, left + 1, right, arr[left])

    # Take the right element if it can be part of LIS
    if arr[right] > prev:
        count2 = 1 + longest_sequence_recursive(arr, left, right - 1, arr[right])

    # Return the maximum of both choices
    return max(count1, count2)

# Wrapper function
def longest_sequence(arr):
    return longest_sequence_recursive(arr, 0, len(arr) - 1, float('-inf'))

# Example usage
arr = [10, 20, 30, 25, 15, 40, 50]
print(longest_sequence(arr))  

# Output
# 1. arr[0] = 10 > prev  → Take 10 → Call (left=1, right=6, prev=10)
# 2. arr[1] = 20 > 10  → Take 20 → Call (left=2, right=6, prev=20)
# 3. arr[2] = 30 > 20  → Take 30 → Call (left=3, right=6, prev=30)
# 4. arr[5] = 40 > 30  → Take 40 → Call (left=6, right=6, prev=40)
# 5. arr[6] = 50 > 40  → Take 50 → Call (left=7, right=6, prev=50) → Base case → Return 0


# Count of equal value pairs from given two Arrays such that a[i] equals b[j] using bisect
from bisect import bisect_left, bisect_right

def count_equal_pairs(A, B):
    B.sort()  # Sort array B for binary search
    count = 0

    for num in A:
        # Count occurrences of num in B
        left = bisect_left(B, num)
        right = bisect_right(B, num)
        count += (right - left)  # Number of occurrences of num in B

    return count

# Example Usage
A = [1, 2, 3, 4, 5]
B = [3, 3, 4, 5, 5, 5]
print(count_equal_pairs(A, B))  # Output: 5 (Pairs: (3,3), (3,3), (4,4), (5,5), (5,5))
# Result 
# 0 0
# 0 0
# 0 2
# 2 3
# 3 5
# 5


# Returns counts of 1's in arr[low..high]. 
# The array is assumed to be sorted in 
# non-increasing order
def count_ones(arr):
    n = len(arr)
    low, high = 0, n - 1
    
    # get the middle index
    while low <= high:
        mid = (low + high) // 2

        # If mid element is 0
        if arr[mid] == 0:
            high = mid - 1
            
        # If element is last 1
        elif mid == n - 1 or arr[mid + 1] != 1:
            return mid + 1
            
        # If element is not last 1    
        else:
            low = mid + 1
    return 0

arr = [1, 1, 1, 0, 0, 0, 0, 0]
print(count_ones(arr))


# Function to return largest pair sum. Assumes that
# there are at-least two elements in arr[]
def find_largest_sum_pair(arr):
    n = len(arr)
    if n < 2:
        return -1

    # Initialize first and second largest element
    first, second = (arr[0], arr[1]) if arr[0] > arr[1] else (arr[1], arr[0])

    # Traverse remaining array and find first and second
    # largest elements in overall array
    for i in range(2, n):
      
        # If current element is greater than first then
        # update both first and second
        if arr[i] > first:
            second = first
            first = arr[i]
        elif arr[i] > second:
            # If arr[i] is in between first and second then
            # update second
            second = arr[i]

    return first + second

# Driver program to test above function
arr = [12, 34, 10, 6, 40]
print("Max Pair Sum is", find_largest_sum_pair(arr))
