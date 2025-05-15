# Stack
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.is_empty():
            return None  # or raise an error
        return self.stack.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

# Valid Parenthesis ((())()
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        bracket_map = {')': '(', '}': '{', ']': '['}
        
        for char in s:
            if char in bracket_map.values():  # Opening bracket
                stack.append(char)
            elif char in bracket_map:         # Closing bracket
                if not stack or stack.pop() != bracket_map[char]:
                    return False
            else:                             # Invalid character
                return False
        
        return not stack  # Stack must be empty at the end
    
# Longest Valid Parenthesis -  O(n), O(n)
# Append index of "(" in stack, pop and minus with present i
# ()(())(((
def longestValidParentheses(s: str) -> int:
    stack = [-1]  # Initialize stack with base index
    max_len = 0

    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        else:
            print(stack)
            stack.pop()  # Pop the matching '(' or base index
            if not stack:
                stack.append(i)  # New base for future substrings
            else:
                print(stack[-1],i)
                max_len = max(max_len, i - stack[-1])

    return max_len
# s = "()()((()))()((())"
# [-1, 0]
# -1 1
# [-1, 2, 3, 4]
# 3 5
# [-1, 2, 3]
# 2 6
# [-1, 2]
# -1 7
# [-1, 8]
# -1 9 = 10

# Min Stack operations in O(1)
# use dual stack
class MinStack:

    def __init__(self):
        self.st = []

    def push(self, val: int) -> None:
        min_val = self.getMin()
        if min_val == None or min_val > val:
            min_val = val
        self.st.append([val, min_val])

    def pop(self) -> None:
        self.st.pop()

    def top(self) -> int:
        return self.st[-1][0] if self.st else None

    def getMin(self) -> int:
        return self.st[-1][1] if self.st else None

# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()

# Daily Temperatures - Wait days for warmer temperature
# For each item, if warmer found, res[idx]=i-idx
# Stack will keep indices of days.
# It will be monotonically decreasing (top has the day with the highest temp so far).
# When current temperature is greater than temperature at index on top of stack:
# We found the "next warmer day" for that index!

# Create an empty stack (stores indices).
# Create a result array res initialized to all 0s.
# Loop through each day's temperature:
#   While stack is not empty and current temp > temp at top of stack:
#       Pop the index from stack.
#       res[popped_index] = current_index - popped_index
#   Push current index onto the stack.
# After loop, remaining indices have 0 (no warmer day).
class Solution:
    def dailyTemperatures(temperatures):
        n = len(temperatures)
        res = [0] * n
        stack = []  # stores indices

        for i in range(n):
            # While current temperature > temperature at index stored at top of stack
            while stack and temperatures[i] > temperatures[stack[-1]]:
                popped_index = stack.pop()
                res[popped_index] = i - popped_index
            stack.append(i)

        return res
# Time - O(N)
# Space - O(N) (stack + result array)
# Input: temperatures = [73,74,75,71,72,69,76,73]
# [0, 0, 0, 0, 0, 0, 0, 0]
# [1, 0, 0, 0, 0, 0, 0, 0]
# [1, 1, 0, 0, 0, 0, 0, 0]
# [1, 1, 0, 0, 0, 0, 0, 0]
# [1, 1, 0, 1, 0, 0, 0, 0]
# [1, 1, 0, 1, 0, 0, 0, 0]
# [1, 1, 4, 1, 2, 1, 0, 0]
# [1, 1, 4, 1, 2, 1, 0, 0]
# [1, 1, 4, 1, 2, 1, 0, 0]
# Output: [1,1,4,2,1,1,0,0]

# Decode String - "3[a]2[bc]"
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        for char in s:
            if char != "]": 
                stack.append(char) 
            else: 
                text = "" 
                while stack and stack[-1] != "[": 
                    text += stack.pop()
                stack.pop() 
                num = "" 
                while stack and stack[-1].isdigit(): 
                    num += stack.pop() 
                stack.append(text * int(num))# we multiply both curr and convert num to int so that we get the total amount of decode strings
        return "".join(stack)

# You are given a nested list of integers nestedList. Each element is either an integer or a list whose elements may also be integers or other lists.
# The depth of an integer is the number of lists that it is inside of. For example, the nested list [100, [20,2], [[3], 2],1] has each integer's value set to its depth.
# Return the sum of each integer in nestedList multiplied by its depth. 
# Recursive Approach O(n) O(depth)
def depthSum(nestedList):
    def dfs(nlist, depth):
        total = 0
        for elem in nlist:
            if isinstance(elem, int):
                total += elem * depth
            else:
                total += dfs(elem, depth + 1)
        return total
    
    return dfs(nestedList, 1)

# Stack Approach
def depthSum(nestedList):
    stack = [(nestedList, 1)]
    total = 0

    while stack:
        current_list, depth = stack.pop()
        for elem in current_list:
            if isinstance(elem, int):
                total += elem * depth
            else:
                stack.append((elem, depth + 1))
    
    return total

# Example usage
nestedList = [100, [20, 2], [[3], 2], 1]
# Output should be 100*1 + (20+2)*2 + (3*3 + 2*2) + 1*1

# 843. Evaluate Complex Mathematical Expression String
# Hard
# Create a function that can evaluate a string representation of a mathematical expression with nested functions. The expression will include integers and the operations add, sub, mul, div, and pow corresponding to addition, subtraction, multiplication, division, and exponentiation, respectively. Each operation takes exactly two arguments which may themselves be expressions.

# Requirements:

# Function Definitions:
# add(x, y): Returns the sum of x and y.
# sub(x, y): Returns the difference of x and y.
# mul(x, y): Returns the product of x and y.
# div(x, y): Returns the quotient of x divided by y.
# pow(x, y): Returns x raised to the power of y.
# Input:
# The input is a string representing the expression.
# The input will be correctly formatted, and you can assume there will not be any divide-by-zero situations.
# Output:
# The function should return the result as an integer.
# Recursive
def evaluate_expression(expr: str) -> int:
    def helper(s: str, start: int, end: int) -> int:
        if s[start].isdigit() or (s[start] == '-' and s[start + 1].isdigit()):
            return int(s[start:end + 1])
        
        # Find the function name
        i = start
        while s[i] != '(':
            i += 1
        func = s[start:i]
        
        # Parse the arguments inside the parentheses
        i += 1  # skip '('
        paren_count = 0
        arg_start = i
        for j in range(i, end):
            if s[j] == '(':
                paren_count += 1
            elif s[j] == ')':
                paren_count -= 1
            elif s[j] == ',' and paren_count == 0:
                arg1 = helper(s, i, j - 1)
                arg2 = helper(s, j + 1, end - 1)
                return apply_function(func, arg1, arg2)
    
    def apply_function(func: str, x: int, y: int) -> int:
        if func == 'add':
            return x + y
        elif func == 'sub':
            return x - y
        elif func == 'mul':
            return x * y
        elif func == 'div':
            return x // y
        elif func == 'pow':
            return x ** y
        else:
            raise ValueError(f"Unknown function: {func}")

    return helper(expr, 0, len(expr) - 1)

# Stack Approach
def evaluate_expression_stack(expr: str) -> int:
    def apply_function(func: str, x: int, y: int) -> int:
        if func == 'add':
            return x + y
        elif func == 'sub':
            return x - y
        elif func == 'mul':
            return x * y
        elif func == 'div':
            return x // y
        elif func == 'pow':
            return x ** y
        else:
            raise ValueError(f"Unknown function: {func}")

    import re
    tokens = re.findall(r'\w+|[-]?\d+\.?\d*|[(),]', expr)
    stack = []

    for token in tokens:
        if token == ')':
            # Build arguments for operation
            args = []
            while stack and stack[-1] != '(':
                args.append(stack.pop())
            stack.pop()  # remove '('
            func = stack.pop()
            arg2 = int(args.pop(0))
            arg1 = int(args.pop(0))
            result = apply_function(func, arg1, arg2)
            stack.append(str(result))
        elif token != ',':
            stack.append(token)

    return int(stack[0])

# | Approach    | Time | Space | Pros                         | Cons                        |
# | ----------- | ---- | ----- | ---------------------------- | --------------------------- |
# | Recursive   | O(n) | O(d)  | Cleaner for nested recursion | Risk of stack overflow      |
# | Stack-based | O(n) | O(n)  | Avoids recursion limits      | Slightly more complex logic |
