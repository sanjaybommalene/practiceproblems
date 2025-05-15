# Graph Valid Tree / Detech Cycles Undirected Graphs
# Approach:
# Union-Find to detect cycles.
# Ensure all nodes are connected (edges == n-1).
def validTree(n, edges):
    if len(edges) != n - 1:
        return False
    
    parent = [i for i in range(n)]
    
    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u
    
    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu == pv:
            return False
        parent[pv] = pu
    
    return True
# Time: O(N α(N))

# Detect Cycles in Graph - Directed O(V + E), O(V) (recursion stack)
# Represent the Graph using an adjacency list.
# Track Node States:
#   0 = Unvisited
#   1 = Visiting (in current DFS stack)
#   2 = Visited (fully processed)
# Perform DFS:
#   If a node is encountered while it's still 1 (Visiting), a cycle exists.
#   After processing all neighbors, mark the node as 2 (Visited).
# DFS
def has_cycle(num_nodes, edges):
    # Build adjacency list
    adj = [[] for _ in range(num_nodes)]
    for u, v in edges:
        adj[u].append(v)
    
    visited = [0] * num_nodes  # 0=unvisited, 1=visiting, 2=visited

    def dfs(u):
        if visited[u] == 1:  # Cycle detected (back edge)
            return True
        if visited[u] == 2:  # Already processed
            return False
        
        visited[u] = 1  # Mark as visiting
        for v in adj[u]:
            if dfs(v):
                return True
        visited[u] = 2  # Mark as visited
        return False

    for i in range(num_nodes):
        if visited[i] == 0 and dfs(i):
            return True  # Cycle found
    return False  # No cycle
# edges = [[0, 1], [1, 2], [2, 0]]  # Contains a cycle (0 → 1 → 2 → 0)
# print(has_cycle(3, edges))  # Output: True

def has_cycle_undirected(num_nodes, edges):
    adj = [[] for _ in range(num_nodes)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)  # Undirected graph
    
    visited = [False] * num_nodes

    def dfs(u, parent):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                if dfs(v, u):
                    return True
            elif v != parent:  # Cycle detected
                return True
        return False

    for i in range(num_nodes):
        if not visited[i] and dfs(i, -1):
            return True
    return False


# Course Schedule I
# There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. 
# You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.
# For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
# Return true if you can finish all courses. Otherwise, return false.
# Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
# Output: false
# Explanation: There are a total of 2 courses to take. 
# To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.
def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:

    pre = [[] for _ in range(numCourses)]

    for course, p in prerequisites:
        pre[course].append(p)
    
    taken = set()

    def dfs(course):
        if not pre[course]:  # If no prerequisites, the course can be taken
            return True
        
        if course in taken:  # Cycle detected → return False
            return False
        
        taken.add(course)  # Mark the course as being visited

        for p in pre[course]:  # Check all prerequisites recursively
            if not dfs(p):
                return False
        
        pre[course] = []  # Mark course as completed (memorization)
        return True
    
    for course in range(numCourses):
        if not dfs(course):
            return False

    return True

# Kahn's Algorithm - BFS
# Kahn's Algorithm
# Graph:
# 0 → 1 → 3  
# 0 → 2 → 3  
# In-Degree:
# 0: 0, 1: 1, 2: 1, 3: 2
# BFS Traversal (Process Nodes)

# Dequeue a course (u) and add it to the result.
# For each dependent course (v):
# Reduce in_degree[v] by 1 (since u is now taken).
# If in_degree[v] == 0, enqueue v.
def canFinish(numCourses, prerequisites):
    # Step 1: Initialize adjacency list and in-degree array
    adj = [[] for _ in range(numCourses)]  # Adjacency list to represent the graph
    in_degree = [0] * numCourses          # Tracks the number of prerequisites for each course

    # Step 2: Build the graph and in-degree counts
    for a, b in prerequisites:
        adj[b].append(a)    # Course `b` is a prerequisite for course `a` (directed edge b → a)
        in_degree[a] += 1   # Increment in-degree of course `a`

    # Step 3: Initialize a queue with courses having no prerequisites (in-degree = 0)
    q = deque([i for i in range(numCourses) if in_degree[i] == 0])
    courses_taken = 0  # Tracks the number of courses processed

    # Step 4: Process courses using BFS (Kahn's Algorithm for Topological Sort)
    while q:
        u = q.popleft()     # Take a course with no remaining prerequisites
        courses_taken += 1          # Increment the courses_taken of completed courses

        # Step 5: Reduce in-degree of neighbors (courses dependent on `u`)
        for v in adj[u]:
            in_degree[v] -= 1           # Remove the dependency on `u`
            if in_degree[v] == 0:       # If no more prerequisites, add to queue
                q.append(v)

    # Step 6: If all courses were processed, return True (no cycle)
    return courses_taken == numCourses
# Time: O(V + E) (V = numCourses, E = prerequisites)
# Space: O(V + E)

# Course Schedule II usign DFS with prequisite
# edge b → a means b is a prerequisite for a
# numCourses = 4
# prerequisites = [[1,0], [2,0], [3,1], [3,2]]
# Return course order O(V + E), O(V + E)
# Kahn's Algorithm
def findOrder(numCourses, prerequisites):
    adj = [[] for _ in range(numCourses)]
    in_degree = [0] * numCourses
    
    for a, b in prerequisites:
        adj[b].append(a)
        in_degree[a] += 1
    
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    result = []
    
    while queue:
        u = queue.popleft()
        result.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    return result if len(result) == numCourses else []
# DFS
class Solution:
    def findOrder(numCourses, prerequisites):
        adj = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            adj[course].append(prereq)
        
        visited = [0] * numCourses
        topo_order = []
        
        def dfs(node):
            if visited[node] == 1:
                return False
            if visited[node] == 2:
                return True
            
            visited[node] = 1
            for neighbor in adj[node]:
                if not dfs(neighbor):
                    return False
            
            visited[node] = 2
            topo_order.append(node)
            return True
        
        for course in range(numCourses):
            if not dfs(course):
                return []
        
        return topo_order

# Course Schedule III
# Given courses with [duration, lastDay], return the maximum number of courses you can take.
# Approach (Greedy + Max-Heap)
# Sort courses by lastDay (earliest deadlines first).
# Use a max-heap to track durations of selected courses.
# If adding a course exceeds its deadline, replace the longest course in the heap.
def scheduleCourse(courses):
    # Sort courses by lastDay (earliest deadline first)
    courses.sort(key=lambda x: x[1])
    max_heap = []  # Stores durations of selected courses (max-heap using negatives)
    time = 0       # Current time
    
    for duration, lastDay in courses:
        if time + duration <= lastDay:
            heapq.heappush(max_heap, -duration)  # Push negative for max-heap
            time += duration
        elif max_heap and -max_heap[0] > duration:
            # Replace the longest course with the current one
            time += duration + heapq.heappop(max_heap)  # Subtract the removed duration
            heapq.heappush(max_heap, -duration)
    
    return len(max_heap)
# Time: O(N log N) (due to sorting and heap operations)
# Space: O(N)

# Course Schedule IV
# Given numCourses, prerequisites, and queries [u, v], check if u is a prerequisite of v.
# Floyd-Warshall or BFS/DFS to precompute reachability. 
def checkIfPrerequisite(numCourses, prerequisites, queries):
    # Initialize reachability matrix
    reachable = [[False] * numCourses for _ in range(numCourses)]
    for u, v in prerequisites:
        reachable[u][v] = True
    
    # Floyd-Warshall to compute transitive closure
    for k in range(numCourses):
        for i in range(numCourses):
            for j in range(numCourses):
                if reachable[i][k] and reachable[k][j]:
                    reachable[i][j] = True
    
    return [reachable[u][v] for u, v in queries]
# Time: O(N³) (Floyd-Warshall)
# Space: O(N²)
         


# Unweighted Graph (Shortest Path using BFS)
def bfs_shortest_path(graph, start, goal):
    visited = set()
    queue = deque([[start]])

    if start == goal:
        return [start]

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in visited:
            for neighbor in graph[node]:
                new_path = list(path) # Used Traversed path so far 
                new_path.append(neighbor) # Append each neighbour to make new path
                queue.append(new_path)

                if neighbor == goal:
                    return new_path
            visited.add(node)
    return None
# Example graph as adjacency list
graph = defaultdict(list)
graph[0] = [1, 2]
graph[1] = [2]
graph[2] = [3]
graph[3] = [4]
graph[4] = []

print(bfs_shortest_path(graph, 0, 4))  # Output: [0, 2, 3, 4]
# Traverse
# [0]
# deque([[0, 1]])
# deque([[0, 1], [0, 2]])
# [0, 1]
# deque([[0, 2], [0, 1, 2]])
# [0, 2]
# deque([[0, 1, 2], [0, 2, 3]])
# [0, 1, 2]
# [0, 2, 3]
# deque([[0, 2, 3, 4]])
# [0, 2, 3, 4]

# Shortest path of weighted graph using Dijkstra's (Positive  Weights)
# Priority Queue (Min-Heap): Selects the next node with the smallest tentative distance.
# Distance Array: Tracks the shortest known distance from the source to each node.
def dijkstra(graph, start):
    heap = [(start, 0)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    while heap:
        current_node, current_distance = heapq.heappop(heap)

        if current_distance > distances[current_node]:
            continue # Skip if a shorter path already exists

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (neighbor, distance))

    return distances
# Step 2: Process B (Distance = 1)

# Relax neighbors of B:
# B → C: 1 + 2 = 3 (Better than 4(A->C) → Update C).
# B → D: 1 + 5 = 6 (Update D).
# Update Queue: [(C,3), (D,6), (C,4)] (Old C:4 is ignored).
# Visited: {A, B}
# Example weighted graph
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('C', 2), ('D', 5)],
    'C': [('D', 1)],
    'D': []
}
print(dijkstra(graph, 'A'))  # Output: shortest distance from A to every node

# Find the cheapest flight from src to dst with at most K stops.
# Approach:
# Use Priority Queue (Min-Heap) to track (cost, node, stops_used).
# Relax edges only if stops are within K.
def findCheapestPrice(n, flights, src, dst, K):
    # Build adjacency list
    graph = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))
    
    # Min-heap: (current_cost, current_city, remaining_stops)
    heap = [(0, src, K + 1)]  # K stops = K+1 edges
    visited = {}  # Tracks (city, remaining_stops) to avoid reprocessing
    
    while heap:
        cost, city, stops = heapq.heappop(heap)
        if city == dst:
            return cost
        if stops <= 0:
            continue
        if (city, stops) in visited and visited[(city, stops)] <= cost:
            continue
        visited[(city, stops)] = cost
        for neighbor, price in graph[city]:
            heapq.heappush(heap, (cost + price, neighbor, stops - 1))
    
    return -1
# Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, K = 1
# Output: 200 (Path: 0 → 1 → 2 with 1 stop)
# Heap: [(0, 0, 2)] (cost=0, city=0, stops left=2).
# Process (0, 0, 2):
# Push (100, 1, 1) (path 0→1) and (500, 2, 1) (path 0→2).
# Process (100, 1, 1):
# Push (200, 2, 0) (path 0→1→2).
# Process (200, 2, 0):
# Destination reached! Return 200.
# Output: 200 ✅
# Time: O(E + V log V) (Dijkstra’s with heap)

# Network Delay Time (Dijkstra’s)
# You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel times as directed edges times[i] = (ui, vi, wi), 
# where ui is the source node, vi is the target node, and wi is the time it takes for a signal to travel from source to target.
# We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal. If it is impossible for all the n nodes to receive the signal, return -1.
# Approach:
# Build a weighted adjacency list to represent the graph.
# Use Dijkstra's Algorithm to compute the shortest path from k to all other nodes.
# Track the maximum distance from k to any node. If any node is unreachable, return -1.
def networkDelayTime(times, n, k):
    # Step 1: Build adjacency list
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    
    # Step 2: Initialize distance dictionary
    distances = {node: float('inf') for node in range(1, n + 1)}
    distances[k] = 0  # Distance from k to itself is 0
    
    # Step 3: Priority queue (min-heap) to process nodes
    heap = [(0, k)]
    
    while heap:
        current_time, u = heapq.heappop(heap)
        if current_time > distances[u]:
            continue  # Skip if a shorter path already exists
        
        # Step 4: Relax all outgoing edges from u
        for v, w in graph[u]:
            if distances[v] > current_time + w:
                distances[v] = current_time + w
                heapq.heappush(heap, (distances[v], v))
    
    # Step 5: Find the maximum distance
    max_distance = max(distances.values())
    return max_distance if max_distance != float('inf') else -1
# Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
# Output: 2
# Example Usage:
# n = 5
# edges = [[0, 1], [1, 2], [3, 4]]
# print(countComponents(n, edges))  # Output: 2

# Rotting Oranges with BFS
from collections import deque
class Solution:
    def bfs(self, grid, q, cnt):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        made, sec = 0, 0
        m, n = len(grid), len(grid[0])

        while q:
            r, c, sec = q.popleft()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    q.append((nr, nc, sec + 1))
                    grid[nr][nc] = -1
                    made += 1
        
        return sec if made == cnt else -1

    def orangesRotting(self, grid):
        m, n = len(grid), len(grid[0])
        cntFresh = 0
        q = deque()

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    q.append((i, j, 0))
                    grid[i][j] = -1
                elif grid[i][j] == 1:
                    cntFresh += 1

        return self.bfs(grid, q, cntFresh)