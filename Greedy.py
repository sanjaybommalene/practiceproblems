# Jump Game
# Start from last but one element and check jump
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        goal = len(nums) - 1

        for i in range(len(nums)-2,-1,-1):
            if i + nums[i]>=goal:
                goal = i

        return True if goal==0 else False
    
# Input: nums = [2,3,1,1,4]
# Output: true
# Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.

# Jump Game - Find Minimum Jumps required
# Keep nearest and farthest points
class Solution:
    def jump(self, nums: List[int]) -> int:
        near = far = jumps = 0

        while far < len(nums)-1:
            farthest = 0
            for i in range(near,far+1):
                farthest = max(farthest,i+nums[i])
            near = far+1
            far = farthest
            jumps+=1
        return jumps
# Input: nums = [2,3,1,1,4]
# Output: 2
# Explanation: The minimum number of jumps to reach the last index is 2. Jump 1 step from index 0 to 1, 
# then 3 steps to the last index.


# Best Time to buy and sell a stock
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        buy_price = prices[0]
        profit = 0

        for p in prices[1:]:
            if buy_price > p:
                buy_price = p
            
            profit = max(profit, p - buy_price)
        
        return profit
# Input: prices = [7,1,5,3,6,4]
# Output: 5 (1,6)

# Best Time to buy and sell a stock - Single Day Buy and Sell
# sell immediately if bigger number found - 4 + 3 = 7
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        profit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                profit+= prices[i] - prices[i-1]
        return profit
    
# Partition Labels
class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        last_occurrence = {}
        
        for i , c in enumerate(s):
            last_occurrence[c]=i
        
        start = end = 0
        result = []

        for i, c in enumerate(s):
            end = max(end,last_occurrence[c])

            if i == end:
                result.append(end-start+1)
                start=i+1
        return result 
# Input: s = "ababcbacadefegdehijhklij"
# Output: [9,7,8]
# Explanation:
# The partition is "ababcbaca", "defegde", "hijhklij".
# This is a partition so that each letter appears in at most one part.