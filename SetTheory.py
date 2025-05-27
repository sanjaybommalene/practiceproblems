# Number of Connected Components in an Undirected Graph
# Input: n = 5, edges = [[0, 1], [1, 2], [3, 4]]
# Output: 2 (Connected components: {0, 1, 2} and {3, 4})
# O(E α(N)) — E = number of edges, N = number of nodes.
# α(N) = inverse Ackermann function, practically almost constant.
# Use path compression and union by rank for near-constant time operations.
# Count the number of unique roots (parents) to determine connected components.
# Find with path compression → always compress tree when finding.
# Initially parent[x] = x 
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        self.parent[self.find(x)] = self.find(y)

def countComponents(n, edges):
    dsu = DSU(n)
    for u, v in edges:
        dsu.union(u, v)
    
    return len({dsu.find(i) for i in range(n)})
# Example Usage:
# n = 5
# edges = [[0,1],[1,2],[3,4]]
# print(countComponents(n, edges))  # Output: 2

# Simpler DFS
# O(V + E)(each node and edge is processed once), O(V) (for visited array and recursion stack)
def countComponents(n, edges):
    from collections import defaultdict
    
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = set()
    components = 0
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
    
    for node in range(n):
        if node not in visited:
            dfs(node)
            components += 1
    
    return components

# Redundant Connection (Union-Find) O(N α(N))
# Union-Find (Disjoint Set Union - DSU) to detect cycles.
# If find(u) == find(v), the edge is redundant.
def findRedundantConnection(edges):
    parent = [i for i in range(len(edges)+1)]
    
    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u
    
    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu == pv:
            return [u, v]
        parent[pv] = pu
    return []

# Questions was we have n elements with 3 properties each we need to group the elements. If any one of the property is common those two element should be in same group.
# e.g.:
# elements = {
#             "e1": ['red',   'circle',    'small'],
#             "e2": ['blue',  'square',    'small'],
#             "e3": ['green', 'triangle',  'large'],
#             "e4": ['black',   'triangle',  'large'],            
#             }
# Output: [["e1", "e2"], ["e3", "e4"]]
class DSU:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        self.parent[self.find(x)] = self.find(y)

def group_elements_dsu(elements):
    dsu = DSU()
    property_to_element = {}

    # Union elements that share any property
    for element, props in elements.items():
        for prop in props:
            if prop in property_to_element:
                dsu.union(element, property_to_element[prop])
            else:
                property_to_element[prop] = element

    # Group elements by their root representative
    groups = {}
    for element in elements:
        root = dsu.find(element)
        groups.setdefault(root, []).append(element)

    return list(groups.values())

# O(n * p) where:
# n = number of elements
# p = number of properties per element (in your case, 3)

# Account Merge
# Treat each email as a node.
# If two emails belong to the same person (same account or share emails across accounts), union them.
# After that, group all connected emails together under the account name.
class DSU:
    def __init__(self):
        self.parent = {}
    
    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        self.parent[self.find(x)] = self.find(y)

# Key Idea:
#  Union emails that belong to the same account.
#  Group emails by their root parent.
#  Sort and format the merged accounts.
# Steps:
#  Initialize Union-Find to manage email connections.
#  Map each email to its owner's name (for final output).
#  Union all emails under the same account.
#  Group emails by their root parent using a dictionary.
#  Sort emails and format the result.
def accountsMerge(accounts):
    uf = DSU()
    email_to_name = {}

    # Step 1: Union emails within the same account
    for account in accounts:
        name = account[0]
        first_email = account[1]
        for email in account[1:]:
            uf.union(email, first_email)
            email_to_name[email] = name

        # email_to_name after step 1:
        # johnsmith@mail.com: John
        # john00@mail.com: John
        # johnnybravo@mail.com: John
        # john_newyork@mail.com: John
        # mary@mail.com: Mary

        # ds.parent after step 1:
        # johnsmith@mail.com: john_newyork@mail.com
        # john00@mail.com: johnsmith@mail.com
        # johnnybravo@mail.com: johnnybravo@mail.com
        # john_newyork@mail.com: john_newyork@mail.com
        # mary@mail.com: mary@mail.com

    # Step 2: Group emails by their root parent email
    groups = {}
    for email in email_to_name:
        root = uf.find(email)
        groups.setdefault(root, []).append(email)

    # Step 3: Prepare output
    result = []
    for root_email, emails in groups.items():
        result.append([email_to_name[root_email]] + sorted(emails))
    return result

# Example Usage:
accounts = [
    ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
    ["John", "johnsmith@mail.com", "john00@mail.com"],
    ["Mary", "mary@mail.com"],
    ["John", "johnnybravo@mail.com"]
]

print(accountsMerge(accounts))
# O(E × α(E) + E log E) — almost linear time because of Union-Find optimizations
# Where E = total number of emails.
