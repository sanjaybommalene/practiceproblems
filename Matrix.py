# Rotate a Matrix
# Vertical Reversal & Transpose
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        edge_length = len(matrix)

        top = 0
        bottom = edge_length - 1

        while top < bottom:
            for col in range(edge_length):
                temp = matrix[top][col]
                matrix[top][col] = matrix[bottom][col]
                matrix[bottom][col] = temp
            top += 1
            bottom -= 1

        for row in range(edge_length):
            for col in range(row+1, edge_length):
                temp = matrix[row][col]
                matrix[row][col] = matrix[col][row]
                matrix[col][row] = temp
        
        return matrix
        
# Print Matrix in spiral order O(m × n), O(1)
# Layer-by-Layer Traversal:
# 1 Define boundaries (top, bottom, left, right).
# 2 Traverse the matrix in four directions:
#   Left to Right (top row).
#   Top to Bottom (right column).
#   Right to Left (bottom row, if top < bottom).
#   Bottom to Top (left column, if left < right).
# 3 Adjust boundaries after each full loop.
# 4 Termination:
# 5 Stop when top > bottom or left > right.
def spiralOrder(matrix):
    if not matrix:
        return []
    
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    result = []
    
    while top <= bottom and left <= right:
        # Traverse Left to Right (top row)
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1
        
        # Traverse Top to Bottom (right column)
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        
        if top <= bottom:  # Check if rows are left
            # Traverse Right to Left (bottom row)
            for i in range(right, left - 1, -1):
                result.append(matrix[bottom][i])
            bottom -= 1
        
        if left <= right:  # Check if columns are left
            # Traverse Bottom to Top (left column)
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    
    return result

# Diagonal Traversal O(mxn), O(mxn)
# We iterate over each diagonal (d from 0 to m+n-2).
# For each diagonal:
# We find the starting point (row, col).
# We collect all elements along that diagonal.
# Depending on the parity (even/odd) of the diagonal, we reverse the elements before adding to the result.
def findDiagonalOrder(mat):
    if not mat or not mat[0]:
        return []
    
    m, n = len(mat), len(mat[0])
    res = []
    
    for d in range(m + n - 1):
        intermediate = []
        
        # Determine the starting row and column
        if d < n:
            row = 0
            col = d
        else:
            row = d - n + 1
            col = n - 1
        
        # Collect all elements along this diagonal
        while row < m and col >= 0:
            intermediate.append(mat[row][col])
            row += 1
            col -= 1
        
        # If the current diagonal is even-numbered, reverse it
        if d % 2 == 0:
            res.extend(intermediate[::-1])
        else:
            res.extend(intermediate)
    
    return res

# Set Matrix Zeros O(m × n), O(1)
# Given an m x n integer matrix matrix, if an element is 0, set its entire row and column to 0'
# Use First Row and Column as Markers:
# Traverse the matrix and mark rows/columns to be zeroed using the first row and column.
# Handle the first row and column separately to avoid overlap.
# Algorithm Steps:
# 1. Check if the first row/column needs to be zeroed.
# 2. Use the first row/column to mark zero positions.
# 3. Zero out marked rows/columns (except first row/column).
# 4. Zero out the first row/column if needed.
class Solution:
    def setZeroes(matrix):
        m, n = len(matrix), len(matrix[0])
        first_row_zero = any(matrix[0][j] == 0 for j in range(n))
        first_col_zero = any(matrix[i][0] == 0 for i in range(m))
        
        # Use first row/column to mark zero positions
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0
        
        # Zero out marked rows/columns
        for i in range(1, m):
            if matrix[i][0] == 0:
                for j in range(1, n):
                    matrix[i][j] = 0
        
        for j in range(1, n):
            if matrix[0][j] == 0:
                for i in range(1, m):
                    matrix[i][j] = 0
        
        # Zero out first row/column if needed
        if first_row_zero:
            for j in range(n):
                matrix[0][j] = 0
        
        if first_col_zero:
            for i in range(m):
                matrix[i][0] = 0
    
# 6. Connected Components in a Matrix (e.g., Number of Islands)
def count_components(grid):
    rows, cols = len(grid), len(grid[0])
    
    def dfs(r, c):
        if 0 <= r < rows and 0 <= c < cols and grid[r][c] == '1':
            grid[r][c] = '0'
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                dfs(r+dx, c+dy)
            return 1
        return 0

    return sum(dfs(i, j) for i in range(rows) for j in range(cols))
# Time Complexity: O(N*M)
# Space Complexity: O(N*M) (call stack)

# Number of Islands
# Traverse the grid, and whenever a '1' (land) is found, perform DFS/BFS to mark all connected '1's as visited (converting them to '0').
# Each DFS/BFS call counts as one island.
# Using BFS O(m*n),O(min(m,n))
from collections import deque
class Solution:
    def numIslands(grid):
        if not grid:
            return 0
        
        count = 0
        rows, cols = len(grid), len(grid[0])
        
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == '1':
                    count += 1
                    queue = deque([(i, j)])
                    grid[i][j] = '0'  # Mark as visited
                    # Perform BFS
                    while queue:
                        x, y = queue.popleft()
                        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '1':
                                grid[nx][ny] = '0'
                                queue.append((nx, ny))
        return count

# Using DFS O(m*n), O(m*n)
class Solution:
    def numIslands(grid):
        if not grid:
            return 0
        
        count = 0
        rows, cols = len(grid), len(grid[0])
        
        def dfs(i, j):
            if i < 0 or i >= rows or j < 0 or j >= cols or grid[i][j] != '1':
                return
            grid[i][j] = '0'  # Mark as visited
            # Explore neighbors (up, down, left, right)
            dfs(i+1, j)
            dfs(i-1, j)
            dfs(i, j+1)
            dfs(i, j-1)
        
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == '1':
                    count += 1
                    dfs(i, j)  # Sink the island
        
        return count

# Surround Regions 
# Using BFS O(mxn),O(1)
# Enqueue border 'O's and mark them as 'T'
# BFS to mark all connected 'O's
# Flip remaining 'O's and revert 'T's
def solve(board):
    if not board:
        return
    
    rows, cols = len(board), len(board[0])
    queue = deque()
    
    # Step 1: Enqueue border 'O's and mark them as 'T'
    for i in range(rows):
        for j in range(cols):
            if (i in [0, rows-1] or j in [0, cols-1]) and board[i][j] == 'O':
                queue.append((i, j))
                board[i][j] = 'T'
    
    # BFS to mark all connected 'O's and mark them as 'T'
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and board[nx][ny] == 'O':
                board[nx][ny] = 'T'
                queue.append((nx, ny))
    
    # Step 2: Flip remaining 'O's and revert 'T's
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 'O':
                board[i][j] = 'X'
            elif board[i][j] == 'T':
                board[i][j] = 'O'
# Using DFS O(mxn),O(mxn)
#  Traverse the border cells (first/last row/column). If a cell is 'O', perform DFS/BFS to mark all connected 'O's as 'T'.
#  Iterate through the entire board. Flip all 'O's (now surrounded) to 'X' and revert 'T' to 'O'.
class Solution:
    def solve(board):
        if not board:
            return
        
        rows, cols = len(board), len(board[0])
        
        def dfs(i, j):
            if i < 0 or i >= rows or j < 0 or j >= cols or board[i][j] != 'O':
                return
            board[i][j] = 'T'  # Mark as temporarily safe
            # Explore neighbors (up, down, left, right)
            dfs(i+1, j)
            dfs(i-1, j)
            dfs(i, j+1)
            dfs(i, j-1)
        
        # Step 1: Mark border-connected 'O's as 'T'
        for i in range(rows):
            for j in range(cols):
                if (i in [0, rows-1] or j in [0, cols-1]) and board[i][j] == 'O':
                    dfs(i, j)
        
        # Step 2: Flip remaining 'O's to 'X' and revert 'T' to 'O'
        for i in range(rows):
            for j in range(cols):
                if board[i][j] == 'O':
                    board[i][j] = 'X'
                elif board[i][j] == 'T':
                    board[i][j] = 'O'

# Maximal Rectangle in Binary Matrix
def maximalRectangle(matrix):
    if not matrix:
        return 0
    
    rows, cols = len(matrix), len(matrix[0])
    height = [0] * cols
    left = [0] * cols
    right = [cols] * cols
    max_area = 0
    
    for i in range(rows):
        # Update height and left boundary
        current_left = 0
        for j in range(cols):
            if matrix[i][j] == '1':
                height[j] += 1
                left[j] = max(left[j], current_left)
            else:
                height[j] = 0
                left[j] = 0
                current_left = j + 1
        
        # Update right boundary
        current_right = cols
        for j in range(cols - 1, -1, -1):
            if matrix[i][j] == '1':
                right[j] = min(right[j], current_right)
            else:
                right[j] = cols
                current_right = j
        
        # Compute max area
        for j in range(cols):
            max_area = max(max_area, height[j] * (right[j] - left[j]))
    
    return max_area

# Example Usage
matrix = [
    ["1","0","1","0","0"],
    ["1","0","1","1","1"],
    ["1","1","1","1","1"],
    ["1","0","0","1","0"]
]
# Visualization Summary

# Row	height	    left	  right	  Max Area
# 0	[1,0,1,0,0]	[0,0,2,0,0]	[1,5,3,5,5]	1
# 1	[2,0,2,1,1]	[0,0,2,2,2]	[1,5,5,5,5]	6
# 2	[3,1,3,2,2]	[0,0,2,2,2]	[5,5,5,5,5]	6
# 3	[4,0,0,3,0]	[0,0,0,3,0]	[1,5,5,4,5]	6

print(maximalRectangle(matrix))  # Output: 6

# 5. Rat in a Maze (Path Finding)
def rat_maze(maze):
    n = len(maze)
    path = []
    visited = [[False]*n for _ in range(n)]

    def dfs(x, y):
        if x == n-1 and y == n-1:
            path.append((x, y))
            return True
        if 0 <= x < n and 0 <= y < n and maze[x][y] == 1 and not visited[x][y]:
            visited[x][y] = True
            path.append((x, y))
            if dfs(x+1, y) or dfs(x, y+1) or dfs(x-1, y) or dfs(x, y-1):
                return True
            path.pop()
        return False

    return path if dfs(0, 0) else []
# Time Complexity: O(4^N²) worst-case
# Space Complexity: O(N²) recursion stack


# Word Search in 2D Letter Board DFS + Backtrack
class Solution(object):
    def exist(board, word):
        if not board or not word:
            return False
        
        rows, cols = len(board), len(board[0])
        path = []  # Stores (row, col) pairs of the current path
        
        def dfs(r, c, index):
            if index == len(word):
                print("Path found:", path)  # Print the path coordinates
                return True
            
            if (r < 0 or r >= rows or 
                c < 0 or c >= cols or 
                board[r][c] != word[index]):
                return False
            
            # Temporarily mark the cell as visited
            temp = board[r][c]
            board[r][c] = '#'
            path.append((r, c))  # Track the current cell
            
            # Explore all 4 directions
            found = (dfs(r+1, c, index+1) or
                    dfs(r-1, c, index+1) or
                    dfs(r, c+1, index+1) or
                    dfs(r, c-1, index+1))
            
            # Backtrack: restore the cell and remove from path
            board[r][c] = temp
            path.pop()
            
            return found
        
        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True  # Word found
        
        return False  # Word not found
# Time: O(m×n×4^L), where L is the length of word (due to DFS with 4 directions per step).
# Space: O(L) for the recursion stack (worst case when the entire word is traversed).
   
   
# Valid Sudoko O(1),O(1) Box Index
# Whenever we see a number:
# We check if it's already present in the corresponding row, column, or box.
# If yes → ❌ Invalid board.
# Else → ✅ Add it to respective sets.
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)] # 3x3 boxes indexed from 0 to 8
        
        for r in range(9):
            for c in range(9):
                num = board[r][c]
                if num == ".":
                    continue  # Skip empty cells

                # Calculate box index
                box_index = (r // 3) * 3 + (c // 3)
                # Check if number is already in row, column, or box
                if (num in rows[r]) or (num in cols[c]) or (num in boxes[box_index]):
                    return False
                # Add number to corresponding row, column, and box sets
                rows[r].add(num)
                cols[c].add(num)
                boxes[box_index].add(num)

        return True

# Solve Sudoko - BackTrack + DFS
# for each 9x9 elements, if element is "."->for each in 1..9->check if valid num
# if valid, backtrack by adding number to i,j and taking back
from typing import List
class Solution:
    def solveSudoku(board: List[List[str]]) -> None:
        def is_valid(r: int, c: int, ch: str) -> bool:
            # Check row and column
            for i in range(9):
                if board[r][i] == ch or board[i][c] == ch:
                    return False
            
            # Check 3x3 box
            box_row = 3 * (r // 3)
            box_col = 3 * (c // 3)
            for i in range(3):
                for j in range(3):
                    if board[box_row + i][box_col + j] == ch:
                        return False
            return True

        def backtrack() -> bool:
            for i in range(9):
                for j in range(9):
                    if board[i][j] == '.':
                        for ch in '123456789':
                            if is_valid(i, j, ch):
                                board[i][j] = ch
                                if backtrack():
                                    return True
                                board[i][j] = '.'  # backtrack
                        return False  # No valid number found
            return True  # Board completely filled

        backtrack()
# Time: O(9^n), where n is the number of empty cells (worst case), but pruning reduces this significantly.
# Space: O(N) for recursion stack

# Kth Smallest Element in a Sorted Matrix O(n log(max-min)),O(1)
# Range Definition:
#   left = matrix[0][0] (smallest element).
#   right = matrix[-1][-1] (largest element).
# Binary Search:
#   Guess a mid value and count how many elements are ≤ mid (using matrix properties).
#   Adjust left or right based on whether the count is < k or ≥ k.
# Counting Elements ≤ mid:
#   Start from the top-right corner of the matrix.
#   Move left if matrix[i][j] > mid.
#   Move down if matrix[i][j] ≤ mid (add j+1 to count).
def kthSmallest(matrix, k):
    n = len(matrix)
    left, right = matrix[0][0], matrix[-1][-1]
    
    def count_less_equal(mid):
        count = 0
        i, j = 0, n - 1  # Start from top-right corner
        while i < n and j >= 0:
            if matrix[i][j] > mid:
                j -= 1  # Move left
            else:
                count += j + 1  # All elements in this row up to j are ≤ mid
                i += 1  # Move down
        return count
    
    while left < right:
        mid = left + (right - left) // 2
        if count_less_equal(mid) < k:
            left = mid + 1  # Need larger elements
        else:
            right = mid  # Narrow down to left half
    return left

# Game of Life O(mxn), O(1)
# The board is made up of an m x n grid of cells, where each cell has an initial state: live (represented by a 1) or dead (represented by a 0). Each cell interacts with its eight neighbors (horizontal, vertical, diagonal) using the following four rules (taken from the above Wikipedia article):

# Any live cell with fewer than two live neighbors dies as if caused by under-population.
# Any live cell with two or three live neighbors lives on to the next generation.
# Any live cell with more than three live neighbors dies, as if by over-population.
# Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
# The next state of the board is determined by applying the above rules simultaneously to every cell in the current state of the m x n grid board. In this process, births and deaths occur simultaneously.

# Given the current state of the board, update the board to reflect its next state.
class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        m, n = len(board), len(board[0])
        
        def countNeighbors(r, c):
            directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
            count = 0
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    if board[nr][nc] in [1, 2]:  # originally alive
                        count += 1
            return count

        for r in range(m):
            for c in range(n):
                neighbors = countNeighbors(r, c)
                
                if board[r][c] == 1:
                    if neighbors < 2 or neighbors > 3:
                        board[r][c] = 2  # live → dead
                else:
                    if neighbors == 3:
                        board[r][c] = 3  # dead → live

        # Final pass to finalize states
        for r in range(m):
            for c in range(n):
                if board[r][c] == 2:
                    board[r][c] = 0
                elif board[r][c] == 3:
                    board[r][c] = 1

