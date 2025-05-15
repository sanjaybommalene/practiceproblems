# 1. Detect Duplicates in Linked List
# Problem: Check if a linked list has duplicates.
# Algorithm:
# Traverse the linked list while storing seen values in a hash set.
# If a value is encountered again, return True.
# If traversal completes without duplicates, return False.
# Time Complexity: O(n)
# Space Complexity: O(n)
def has_duplicates(head):
    seen = set()
    current = head
    while current:
        if current.val in seen:
            return True
        seen.add(current.val)
        current = current.next
    return False

# 2. Count Primes (LeetCode 204)
# Problem: Count primes less than n.
# Algorithm (Sieve of Eratosthenes):
# Initialize a boolean array sieve of size n, marking all entries as True.
# Mark 0 and 1 as non-prime.
# For each number i from 2 to sqrt(n), if i is prime, mark all its multiples as non-prime.
# Count remaining True values in sieve.
# Time Complexity: O(n log log n)
# Space Complexity: O(n)
def countPrimes(n):
    if n <= 2:
        return 0
    sieve = [True] * n
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i*i : n : i] = [False] * len(sieve[i*i : n : i])
    return sum(sieve)

# 3. Valid Perfect Square (LeetCode 367)
# Problem: Check if num is a perfect square without sqrt.
# Algorithm (Binary Search):
# Use binary search to find if there exists an integer x such that x * x == num.
# If found, return True; else, False.
# Time Complexity: O(log n)
# Space Complexity: O(1)
def isPerfectSquare(num):
    if num < 2:
        return True
    left, right = 2, num // 2
    while left <= right:
        mid = left + (right - left) // 2
        square = mid * mid
        if square == num:
            return True
        elif square < num:
            left = mid + 1
        else:
            right = mid - 1
    return False

# 4. Add Digits (LeetCode 258)
# Problem: Repeatedly add digits until a single digit is obtained.
# Algorithm (Digital Root Formula):
# If num == 0, return 0.
# Else, use the formula 1 + (num - 1) % 9.
# Time Complexity: O(1)
# Space Complexity: O(1)
def addDigits(num):
    if num == 0:
        return 0
    return 1 + (num - 1) % 9

# 5. Missing Number (LeetCode 268)
# Problem: Find the missing number in [0, n].
# Algorithm (Gauss' Formula):
# Compute expected sum of 0 to n as n * (n + 1) // 2.
# Subtract the sum of nums to find the missing number.
# Time Complexity: O(n)
# Space Complexity: O(1)
def missingNumber(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)

# 6. GCD of Strings (LeetCode 1071) (Without math.gcd)
# Problem: Find the largest string that divides both str1 and str2.
# Algorithm:
# Check if str1 + str2 == str2 + str1 (necessary condition).
# If true, compute GCD of lengths using Euclidean algorithm.
# Return the substring of length GCD(len(str1), len(str2)).
# Time Complexity: O(m + n)
# Space Complexity: O(m + n)
def gcdOfStrings(str1, str2):
    if str1 + str2 != str2 + str1:
        return ""
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    return str1[:gcd(len(str1), len(str2))]

# 7. Rotate Function (LeetCode 396)
# Problem: Compute max F(k) where F(k) = sum(i * nums[(i + k) % n]).
# Algorithm:
# Compute F(0) and sum(nums).
# Use the recurrence relation:
# F(k) = F(k-1) + sum(nums) - n * nums[-k].
# Track the maximum F(k).
# Time Complexity: O(n)
# Space Complexity: O(1)
def maxRotateFunction(nums):
    n = len(nums)
    total_sum = sum(nums)
    F = sum(i * num for i, num in enumerate(nums))
    max_F = F
    for k in range(1, n):
        F += total_sum - n * nums[-k]
        max_F = max(max_F, F)
    return max_F

# 8. Water and Jug Problem (LeetCode 365)
# Problem: Measure target using jugs of capacities x and y.
# Algorithm:
# If target > x + y, return False.
# If target is a multiple of GCD(x, y), return True.
# Time Complexity: O(log(min(x, y)))
# Space Complexity: O(1)
def canMeasureWater(x, y, target):
    if x + y < target:
        return False
    if target == 0:
        return True
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    return target % gcd(x, y) == 0

# 9. Smallest Integer Divisible by K (LeetCode 1015)
# Problem: Find smallest n (made of 1s) divisible by K.
# Algorithm:
# If K is divisible by 2 or 5, return -1 (no solution).
# Use modular arithmetic to track remainders.
# If remainder becomes 0, return the length.
# Time Complexity: O(K)
# Space Complexity: O(1)
def smallestRepunitDivByK(K):
    if K % 2 == 0 or K % 5 == 0:
        return -1
    remainder = 0
    for length in range(1, K + 1):
        remainder = (remainder * 10 + 1) % K
        if remainder == 0:
            return length
    return -1

# 10. Sum of Two Integers (LeetCode 371)
# Problem: Compute a + b without + or -.
# Algorithm (Bit Manipulation):
# Use XOR for sum without carry.
# Use AND and left shift for carry.
# Repeat until carry is 0.
# Time Complexity: O(1)
# Space Complexity: O(1)
def getSum(a, b):
    mask = 0xFFFFFFFF
    while b != 0:
        carry = (a & b) & mask
        a = (a ^ b) & mask
        b = (carry << 1) & mask
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)

# 11. Number of Good Pairs (LeetCode 1512)
# Problem: Count pairs (i, j) where nums[i] == nums[j] and i < j.
# Algorithm:
# Use a hash map to count frequencies.
# For each occurrence, add its current count to the result.
# Time Complexity: O(n)
# Space Complexity: O(n)
def numIdenticalPairs(nums):
    from collections import defaultdict
    freq = defaultdict(int)
    count = 0
    for num in nums:
        count += freq[num]
        freq[num] += 1
    return count

# 12. Wiggle Subsequence (LeetCode 376)
# Problem: Find the longest wiggle subsequence (alternating nums[i] < nums[i+1] and nums[i] > nums[i+1]).
# Algorithm (Greedy):
# Track up and down lengths.
# If nums[i] > nums[i-1], up = down + 1.
# If nums[i] < nums[i-1], down = up + 1.
# Time Complexity: O(n)
# Space Complexity: O(1)
def wiggleMaxLength(nums):
    if len(nums) < 2:
        return len(nums)
    up = down = 1
    for i in range(1, len(nums)):
        if nums[i] > nums[i-1]:
            up = down + 1
        elif nums[i] < nums[i-1]:
            down = up + 1
    return max(up, down)

# 13. Minimal Spanning Tree (Kruskal's Algorithm)
# Problem: Find the MST of a connected, undirected graph.
# Algorithm:
# Sort edges by weight.
# Use Union-Find to add edges without cycles.
# Sum weights of selected edges.
# Time Complexity: O(E log E)
# Space Complexity: O(E + V)
def minCostConnectPoints(points):
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            edges.append((dist, i, j))
    edges.sort()
    
    parent = list(range(n))
    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u
    
    mst_cost = 0
    for dist, u, v in edges:
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            parent[root_v] = root_u
            mst_cost += dist
    return mst_cost