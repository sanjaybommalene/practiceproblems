# Longest Substring Without Repeating Characters O(n),O(min(m,n))
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_length = left = 0
        count = {}
        for right, c in enumerate(s):
            count[c] = 1 + count.get(c, 0)
            while count[c]>1: # Means Repeated {a:2,b:1,c:1}
                count[s[left]] -= 1
                left+=1
            max_length = max(max_length,right-left+1)
        return max_length

# Subarray Sum  O(N),O(1)
def slidingWindowSubarray(nums, target):
    left = 0
    current_sum = 0
    result = []
    
    for right in range(len(nums)):
        current_sum += nums[right]
        while current_sum > target and left <= right:
            current_sum -= nums[left]
            left += 1
        if current_sum == target:
            result.append(nums[left:right + 1])  # Or return [left, right]
    return result

# Example Usage:
nums = [1, 2, 3, 4, 5]
target = 9
print(slidingWindowSubarray(nums, target))  # Output: [[2, 3, 4]]

# Minimum Size Subarray Sum  O(N),O(1)
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        min_len = float("inf")
        left = 0
        cur_sum = 0
        for right in range(len(nums)):
            cur_sum += nums[right]
            while cur_sum >= target:
                min_len=min(min_len,right-left+1)
                cur_sum -= nums[left]
                left += 1
        return min_len if min_len != float("inf") else 0
# Input: target = 7, nums = [2,3,1,2,4,3]
# Output: 2
# Explanation: The subarray [4,3] has the minimal length under the problem constraint.

# Sliding Window Maximum Number O(N),O(k)
class Solution(object):
    def maxSlidingWindow(self, nums, k):

        res = []
        q = deque()

        for idx, num in enumerate(nums):
            # Maintain the deque in descending order
            while q and q[-1] < num:
                q.pop() # removes elements from the right end of the deque
            q.append(num) # adds to right end of the deque
            
            # Remove an Element That Is Out of the Current Window
            if idx >= k and nums[idx-k]==q[0]:
                q.popleft()
            # Append the maximum of the current window to the result
            if idx >= k - 1:
                res.append(q[0])
        return res
# You are given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. 
# You can only see the k numbers in the window. Each time the sliding window moves right by one position.
# Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
# Output: [3,3,5,5,6,7]

# Find All Anagrams in a String O(N),O(1)
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        count = Counter(p)
        
        ans = []
        left = 0
        for right, c in enumerate(s):
            count[c] -= 1
            while count[c] < 0:  # If number of characters `c` is more than our expectation
                count[s[left]] += 1  # Slide left until count[c] == 0
                left += 1
            if right - left + 1 == len(p):  #  If we already filled enough `p.length()` chars
                ans.append(left)  # Add left index `l` to our result
                
        return ans
    
# Input: s = "cbaebabacd", p = "abc"
# Output: [0,6]
# Explanation:
# The substring with start index = 0 is "cba", which is an anagram of "abc".
# The substring with start index = 6 is "bac", which is an anagram of "abc".

# Sliding Window Rate Limiting Algorithm
from collections import deque
from time import time

class SlidingWindowRateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_log = deque()

    def allow_request(self):
        current_time = time()
        # Remove requests older than the window
        while self.request_log and self.request_log[0] <= current_time - self.window_seconds:
            self.request_log.popleft()
        # Check if within limit
        if len(self.request_log) < self.max_requests:
            self.request_log.append(current_time)
            return True
        return False

# Example: Allow 5 requests per 10 seconds
limiter = SlidingWindowRateLimiter(5, 10)
print(limiter.allow_request())  # True (1st request)
print(limiter.allow_request())  # True (2nd request)
# ... after 5 requests, further calls return False.