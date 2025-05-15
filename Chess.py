# 1. Check if Two Bishops Threaten Each Other
# Problem: Determine if two bishops on a chessboard threaten each other.
def bishops_attack(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) == abs(y1 - y2)
# Time Complexity: O(1)
# Space Complexity: O(1)

# 2. Valid Moves for Knight/Bishop/King
# Knight:
def knight_moves(x, y, n=8):
    directions = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                  (-2, -1), (-1, -2), (1, -2), (2, -1)]
    return [(x+dx, y+dy) for dx, dy in directions if 0 <= x+dx < n and 0 <= y+dy < n]
# Bishop:
def bishop_moves(x, y, n=8):
    moves = []
    for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
        i, j = x+dx, y+dy
        while 0 <= i < n and 0 <= j < n:
            moves.append((i, j))
            i += dx
            j += dy
    return moves
# King:
def king_moves(x, y, n=8):
    return [(x+dx, y+dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]
            if (dx != 0 or dy != 0) and 0 <= x+dx < n and 0 <= y+dy < n]
# Time Complexity: O(1) per piece
# Space Complexity: O(1)

# 3. Bishop or King Moves from A to B (Min Steps)
def bishop_steps(start, end):
    x1, y1 = start
    x2, y2 = end
    if (x1 + y1) % 2 != (x2 + y2) % 2:
        return -1  # unreachable
    return 1 if abs(x1 - x2) == abs(y1 - y2) else 2

def king_steps(start, end):
    x1, y1 = start
    x2, y2 = end
    return max(abs(x1 - x2), abs(y1 - y2))
# Time Complexity: O(1)
# Space Complexity: O(1)

# 🟡 MEDIUM

# 4. Minimum Steps for Knight to Reach Target
from collections import deque

def min_knight_moves(N, src, dest):
    directions = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                  (-2, -1), (-1, -2), (1, -2), (2, -1)]
    visited = [[False]*N for _ in range(N)]
    q = deque([(src[0], src[1], 0)])

    while q:
        x, y, d = q.popleft()
        if (x, y) == dest:
            return d
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny, d+1))
# Time Complexity: O(N²)
# Space Complexity: O(N²)

# 7. Chessboard Coloring Problem (Bipartite Check)
def is_bipartite_chessboard(n):
    color = [[-1]*n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if color[i][j] == -1:
                queue = [(i, j)]
                color[i][j] = 0
                while queue:
                    x, y = queue.pop()
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < n and 0 <= ny < n:
                            if color[nx][ny] == -1:
                                color[nx][ny] = 1 - color[x][y]
                                queue.append((nx, ny))
                            elif color[nx][ny] == color[x][y]:
                                return False
    return True
# Time Complexity: O(N^2)
# Space Complexity: O(N^2)

# 8. Knight Probability in Chessboard
def knight_probability(N, K, r, c):
    memo = {}

    def dp(k, x, y):
        if x < 0 or x >= N or y < 0 or y >= N:
            return 0
        if k == 0:
            return 1
        if (k, x, y) in memo:
            return memo[(k, x, y)]

        prob = 0
        for dx, dy in [(2, 1), (1, 2), (-1, 2), (-2, 1),
                       (-2, -1), (-1, -2), (1, -2), (2, -1)]:
            prob += dp(k-1, x+dx, y+dy) / 8
        memo[(k, x, y)] = prob
        return prob

    return dp(K, r, c)
# Time Complexity: O(K * N²)
# Space Complexity: O(K * N²)

# 🔴 HARD

# 9. N-Queens Problem
def solve_n_queens(n):
    res = []
    board = [['.'] * n for _ in range(n)]

    def backtrack(r, cols, diag1, diag2):
        if r == n:
            res.append(["".join(row) for row in board])
            return
        for c in range(n):
            if c in cols or (r + c) in diag1 or (r - c) in diag2:
                continue
            board[r][c] = 'Q'
            backtrack(r + 1, cols | {c}, diag1 | {r + c}, diag2 | {r - c})
            board[r][c] = '.'

    backtrack(0, set(), set(), set())
    return res
# Time Complexity: O(N!)
# Space Complexity: O(N²)

# 10. Knight’s Tour Problem
def knights_tour(n):
    board = [[-1]*n for _ in range(n)]
    moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
             (-2, -1), (-1, -2), (1, -2), (2, -1)]

    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n and board[x][y] == -1

    def dfs(x, y, movei):
        if movei == n*n:
            return True
        for dx, dy in moves:
            nx, ny = x+dx, y+dy
            if is_valid(nx, ny):
                board[nx][ny] = movei
                if dfs(nx, ny, movei+1):
                    return True
                board[nx][ny] = -1
        return False

    board[0][0] = 0
    if dfs(0, 0, 1):
        return board
    return None
# Time Complexity: O(8^(N²)) (exponential)
# Space Complexity: O(N²)