# Arrays, Multi Arrays, Accessing, Looping, Length and Copying
class Arrays:
    def sum_array(array):
        return sum(sum(row) for row in array)

    def average(array):
        total_elements = sum(len(row) for row in array)
        return sum_array(array) / total_elements if total_elements > 0 else 0

    def copy_array(original):
        copied = []
        for row in original:
            new_row = []
            for element in row:
                new_row.append(element)
            copied.append(new_row)
        return copied
        # return [row[:] for row in original]  # List comprehension for deep copy

    def main():
        array = [[1, 2], [3, 4], [5, 6], [7, 8]]
        print(sum_array(array))  # Should print sum of all elements
        print(average(array))    # Should print average of all elements
        print(copy_array(array)) # Should print copied array

    if __name__ == "__main__":
        main()

# Problem-1: Sorted Array 
class MySolution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        buf = [0] * (m + n)
        first, second = 0, 0

        if nums2:
            for i in range(m + n):
                if second < len(nums2):
                    if len(nums1) > i + (len(nums2) - second):
                        if nums1[first] <= nums2[second]:
                            buf[i] = nums1[first]
                            first += 1
                        else:
                            buf[i] = nums2[second]
                            second += 1
                    else:
                        buf[i] = nums2[second]
                        second += 1
                else:
                    buf[i] = nums1[first]
                    first += 1
            
            nums1[:] = buf  # Copy buffer to nums1

class Solution1:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        nums1[m:] = nums2  # Append nums2 elements at the end
        nums1.sort()  # Sort the entire array

class BestSolution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        i, j, k = m - 1, n - 1, m + n - 1

        while j >= 0:
            if i >= 0 and nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1

# Problem-2 Remove Element in Array
class MySolution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        i = 0
        temp = []
        while (i<len(nums)):
            if nums[i] != val:
                temp.append(nums[i])
            i+=1
        
        nums[:]=temp

class BestSolution(object):
    def removeElement(self, nums, val):
        k=0
        for i in range(len(nums)):
            if nums[i]!= val:
                nums[k]=nums[i]
                k+=1
        return k

# Problem-3 Remove Duplicates from Sorted Array
class Solution(object):
    def removeDuplicates(self, nums):
        j=1
        for i in range(1,len(nums)):
            if nums[i] != nums[j-1]:
                nums[j]=nums[i] 
                j+=1
        return j

# Problem-4 Remove II Duplicates from Sorted Array
class Solution(object):
    def removeDuplicates(self, nums):
        j=2
        for i in range(2,len(nums)):
            if nums[i] != nums[j-2]:
                nums[j]=nums[i] 
                j+=1
        return j
    
# Problem 5 - Majority in Array/ Voting Problem
class Solution(object):
    def majorityElement(self, nums):
        nums.sort()
        n=len(nums)
        return nums[n/2]
class Solution:
    def majorityElement(self, nums):
        count, candidate = 0, None
        for num in nums:
            if count == 0:
                candidate = num
            count += (1 if num == candidate else -1)
        return candidate

# Reverse full array
class Solution(object):
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        buf = 0
        for i in range(0,len(nums)/2):
            buf=nums[i]
            nums[i]=nums[len(nums)-i-1]
            nums[len(nums)-i-1]=buf

#Problem-6 Rotate array by K steps
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        k %= len(nums)

        def reverse(left, right):
            while left < right:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
                right -= 1

        reverse(0, len(nums) - 1)
        reverse(0, k - 1)
        reverse(k, len(nums) - 1)

# O(n),O(n)
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k = k % n
        rotated = [0] * n

        for i in range(n):
            rotated[(i + k) % n] = nums[i]
        
        for i in range(n):
            nums[i] = rotated[i]

#Given an array of integers nums and an integer target, return indices of the two numbers 
#such that they add up to target.
class MySolution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for i, num in enumerate(nums):
            for j in range(i+1,len(nums)):
                if nums[i]+nums[j] == target:
                    return [i,j]      

class BestSolution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        numMap = {} #HashMap
        n = len(nums)

        for i in range(n):
            complement = target - nums[i]
            if complement in numMap:
                return [numMap[complement], i]
            numMap[nums[i]] = i

        return []  # No solution found  
    
# Roman Letters
class Solution:
    def romanToInt(self, s: str) -> int:
        res = 0
        roman = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

        for a, b in zip(s, s[1:]):
            if roman[a] < roman[b]:
                res -= roman[a]
            else:
                res += roman[a]

        return res + roman[s[-1]] 
    
# Longest Common Prefix    
class Solution:
    def longestCommonPrefix(self, v: List[str]) -> str:
        ans=""
        v=sorted(v)
        first=v[0]
        last=v[-1]
        for i in range(min(len(first),len(last))):
            if(first[i]!=last[i]):
                return ans
            ans+=first[i]
        return ans 

# Largest Rectangle in Histogram O(n), O(n)
# Use a stack to track indices of increasing heights.
# For each bar, pop smaller bars and calculate their max area.
# Handle remaining bars in the stack after traversal.
def largestRectangleArea(heights):
    stack = []
    max_area = 0
    heights.append(0)  # Sentinel to force stack pop
    
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    
    return max_area

# Basic Calculator: O(n)
# String Processing: We first remove spaces to simplify parsing the string.
# Stack: We use a stack to store the intermediate results. Each time we encounter a new number, we process it based on the previous operation (+, -, *, /).
# Operators Handling:
#   For + and -, we store the result of the previous number and operation.
#   For * and /, we apply the operation immediately to the last number in the stack and update the stack.
# Final Calculation: The stack holds all intermediate results, so we return the sum of all elements in the stack as the final result.

def basicCalculator(s: str) -> int:
    # Remove all spaces from the input string for easier processing
    s = s.replace(" ", "")
    
    # Initialize a stack to store intermediate results
    stack = []
    # The current number and operation to apply
    num = 0
    sign = 1  # 1 means positive, -1 means negative
    
    # Loop through the characters of the string
    for i in range(len(s)):
        char = s[i]
        
        if char.isdigit():
            # Build the current number digit by digit
            num = num * 10 + int(char)
        
        # If we encounter an operator or the end of the string
        if char in '+-*/' or i == len(s) - 1:
            if char in '+-':
                # Apply the previous number with the current sign
                stack.append(sign * num)
                # Reset the number and set the new sign
                num = 0
                sign = 1 if char == '+' else -1
            elif char in '*/':
                # Apply multiplication or division immediately to the last element in the stack
                prev = stack.pop()
                if char == '*':
                    stack.append(prev * num)
                elif char == '/':
                    stack.append(int(prev / num))  # Use int() for truncation towards 0
                num = 0  # Reset the current number
        elif i == len(s) - 1 and char.isdigit():
            # This handles the last number in the string when no operator follows it
            stack.append(sign * num)
    
    # Return the sum of all numbers in the stack (for the final result)
    return sum(stack)

import json
# Load user data from JSON file
def load_users_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Main logic
def main():
    users = load_users_from_file('users.json')
    
    print("All users:")
    for user in users:
        print(f"{user['name']} ({user['age']} years old) - {user['email']}")

    # List transformation examples:

    # 1. Extract all user names
    names = [user['name'] for user in users]
    print("\nNames:", names)

    # 2. Filter users older than 25
    older_users = [user for user in users if user['age'] > 25]
    print("\nUsers older than 25:", [user['name'] for user in older_users])

    # 3. Sort users by age
    sorted_by_age = sorted(users, key=lambda x: x['age'])
    print("\nUsers sorted by age:")
    for user in sorted_by_age:
        print(f"{user['name']}: {user['age']}")

    # 4. Map users to a simplified format
    simplified = [{"username": user["name"], "contact": user["email"]} for user in users]
    print("\nSimplified user info:")
    print(simplified)

if __name__ == "__main__":
    main()


# Imagine you’re working on payments team. Customer subscribes to Products and is interested in exploring how much it’ll cost them to keep using the product for the rest of the year.
# Your task is to develop a Cost Explorer that calculates the total cost a customer has to pay in a unit year. This means that at any day of the year they should be able to get a 
# provisional report giving monthly/yearly cost estimates.
# Cost Explorer should be able to provide a report of - Monthly cost (Generate a bill for each month, including bill amount for future months for the unit year) - Yearly cost estimates (for the unit year)
# // Atlassian pricing plans - [{BASIC, 9.99},{STANDARD, 49.99},{PREMIUM, 249.99}]
# // Customer subscription information
# Customer -> C1
# Product ->
# Name -> Jira
# Subscription -> [ "BASIC", "2022-01-01”, "2022-03-31", "PREMIUM" ] // {planId, startDate, endDate, newPlan}

# To solve this problem, we need to develop a Cost Explorer that calculates the total cost a customer has to pay for the rest of the year based on their subscription changes. 
# The solution involves tracking the customer's subscription plans over time and computing the monthly and yearly costs accordingly.
# Approaches
# Parse Subscription Information: Extract the customer's subscription details, including the plan changes and their respective date ranges.
# Calculate Monthly Costs: For each month in the year, determine which plan was active and compute the cost for that month.
# Sum Yearly Cost: Aggregate the monthly costs to get the total yearly cost.
# Generate Report: Format the results into a report showing monthly bills and the total yearly cost.

import datetime
from collections import defaultdict

# Pricing plans
PRICING_PLANS = {
    "BASIC": 9.99,
    "STANDARD": 49.99,
    "PREMIUM": 249.99
}

# Customer subscription information
SUBSCRIPTIONS = [
    {"customer": "C1", "product": "Jira", "plan": "BASIC", "start_date": "2022-01-01", "end_date": "2022-03-31", "new_plan": "PREMIUM"}
]

def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

def get_monthly_costs(subscriptions, year):
    monthly_costs = defaultdict(float)
    for sub in subscriptions:
        start_date = parse_date(sub["start_date"])
        end_date = parse_date(sub["end_date"])
        new_plan = sub["new_plan"]
        current_plan = sub["plan"]
        
        for month in range(1, 13):
            month_start = datetime.date(year, month, 1)
            if month == 12:
                month_end = datetime.date(year, month, 31)
            else:
                month_end = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
            
            # Determine which plan was active during this month
            if start_date <= month_start and month_end <= end_date:
                plan = current_plan
            elif start_date <= month_end and month_start <= end_date:
                # Transition month
                if month_start < start_date:
                    plan = current_plan
                elif month_end > end_date:
                    plan = new_plan
                else:
                    # The entire month is within the transition period
                    # Here, we assume the new plan starts immediately after the end date
                    plan = new_plan if month_start >= end_date else current_plan
            else:
                if month_start > end_date:
                    plan = new_plan
                else:
                    plan = current_plan
            
            monthly_costs[month] += PRICING_PLANS[plan]
    
    return monthly_costs

def generate_report(customer, product, year):
    relevant_subs = [sub for sub in SUBSCRIPTIONS if sub["customer"] == customer and sub["product"] == product]
    if not relevant_subs:
        return {"customer": customer, "product": product, "year": year, "monthly_costs": {}, "yearly_cost": 0.0}
    
    monthly_costs = get_monthly_costs(relevant_subs, year)
    yearly_cost = sum(monthly_costs.values())
    
    report = {
        "customer": customer,
        "product": product,
        "year": year,
        "monthly_costs": {datetime.date(year, month, 1).strftime("%B"): round(cost, 2) for month, cost in monthly_costs.items()},
        "yearly_cost": round(yearly_cost, 2)
    }
    
    return report

# Example usage
# customer = "C1"
# product = "Jira"
# year = 2022
# report = generate_report(customer, product, year)
# print(report)