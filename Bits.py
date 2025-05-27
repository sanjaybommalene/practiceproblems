
# Bit Manipulation

# Add Binary
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        carry = 0
        res = []
        
        idxA, idxB = len(a) - 1, len(b) - 1
        
        while idxA >= 0 or idxB >= 0 or carry == 1:
            if idxA >= 0:
                carry += int(a[idxA])
                idxA -= 1            
            if idxB >= 0:
                carry += int(b[idxB])
                idxB -= 1            

            res.append(str(carry % 2))
            carry = carry // 2
            
        return "".join(res[::-1])
    
# Reverse Bits
class Solution:
    def reverseBits(self, n: int) -> int:
        result = 0
        for _ in range(32):
            bit = n & 1            # Extract the least significant bit
            result = (result << 1) | bit # Append the bit to the result
            n >>= 1                # Right-shift n to process the next bit
        return result

# Number of 1 Bits in a number   
class Solution:
    def hammingWeight(self, n: int) -> int:
        res = 0

        for i in range(32):
            if (n >> i) & 1:
                res += 1

        return res
    
# Single number in array
# If already in ones, it gets removed (XOR toggles the bit).
# A Bitwise Approach to find a unique number.
class Solution :
    def singleNumber(self, nums: list[int]) -> int:
        res =0
        for num in nums:
            res ^= num
        return res
    
# Single Number II
# Given an integer array nums where every element appears three times except for one, which appears exactly once. Find the single element and return it.
class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        ones, twos = 0, 0

        for num in nums:
            # first appearance:
            # add it to ones if it's not there in twos
            ones = (ones ^ num) & ~twos
            
            # second appearance:
            # add it to twos if it's not there in ones
            twos = (twos ^ num) & ~ones

        return ones
# Breakdown:
# ones ^ num:
# This toggles bits: if a bit in num is 1 and not in ones, it's added to ones.
# If it's already in ones, it gets removed (XOR toggles the bit).
# & ~twos:
# This ensures that bits already in twos are not kept in ones.
# If a bit is in twos, we zero it out from ones.

# Single Number III
# Given an array where every element appears twice except two unique numbers
# O(n) time and O(1) space.    

# XOR all numbers to get xor = a ^ b (the two unique numbers).
# Find the rightmost set bit in xor to partition the array into two groups.
# XOR numbers in each group to isolate a and b.
# Partitioning by a set bit ensures a and b are in different groups.
# Input: [1, 2, 1, 3, 2, 5]
# Step 1: Compute xor = 1 ^ 2 ^ 1 ^ 3 ^ 2 ^ 5 = 3 ^ 5 = 6 (110 in binary).
# Step 2: diff_bit = 6 & -6 = 2 (010 in binary).
# Step 3: Partition:

# Group 1 (bit 010 set): [2, 2, 3] → 2 ^ 2 ^ 3 = 3 (a).
# Group 2 (bit 010 not set): [1, 1, 5] → 1 ^ 1 ^ 5 = 5 (b).
# Output: [3, 5].
def singleNumber(nums):
    xor = 0
    for num in nums:
        xor ^= num  # Get a ^ b
    
    # Find rightmost set bit 2's complement
    diff_bit = xor & -xor
    
    a, b = 0, 0
    for num in nums:
        # Partitioning by a set bit ensures a and b are in different groups.
        if num & diff_bit:
            a ^= num  # Group with bit set
        else:
            b ^= num  # Group with bit not set
    
    return [a, b]