# Definition for a binary tree node.
class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinarySearchTree:
    def __init__(self):
        self.root = None

    # --- Insert (Add) ---
    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert_recursive(self.root, val)

    def _insert_recursive(self, node, val):
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
            else:
                self._insert_recursive(node.left, val)
        else:
            if node.right is None:
                node.right = TreeNode(val)
            else:
                self._insert_recursive(node.right, val)

    # --- Remove ---
    def remove(self, val):
        self.root = self._remove_recursive(self.root, val)

    def _remove_recursive(self, node, val):
        if not node:
            return None
        if val < node.val:
            node.left = self._remove_recursive(node.left, val)
        elif val > node.val:
            node.right = self._remove_recursive(node.right, val)
        else:
            # Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            # Node with two children: Replace with inorder successor (smallest in right subtree)
            temp = self._find_min(node.right)
            node.val = temp.val
            node.right = self._remove_recursive(node.right, temp.val)
        return node

    # --- Search (Get) ---
    def search(self, val):
        return self._search_recursive(self.root, val)

    def _search_recursive(self, node, val):
        if not node:
            return False
        if node.val == val:
            return True
        elif val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)

    # --- Helper Methods ---
    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    def _find_max(self, node):
        while node.right:
            node = node.right
        return node

    # --- Traversals ---
    def inorder(self):
        return self._inorder_recursive(self.root, [])

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.val)
            self._inorder_recursive(node.right, result)
        return result

    def preorder(self):
        return self._preorder_recursive(self.root, [])

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.val)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
        return result

    def postorder(self):
        return self._postorder_recursive(self.root, [])

    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.val)
        return result
# Operation	Average Case	Worst Case (Unbalanced Tree)
# Insert	O(log n)	O(n)
# Remove	O(log n)	O(n)
# Search	O(log n)	O(n)
# Traversals	O(n)	O(n)   

# Level Order Traversal, Print pairs
# Use BFS
class Solution(object):
    def levelOrder(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: List[List[int]]
        """
        res = []
        if not root:
            return res
        queue = deque([root])
        while queue:
            same_level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                same_level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            res.append(same_level)
        return res

# Sorted Array to Binary Search Tree
class Solution(object):
    def sortedArrayToBST(self, nums):

        total_nums = len(nums)
        if not total_nums:
            return None

        mid_node = total_nums // 2
        return TreeNode(
            nums[mid_node], 
            self.sortedArrayToBST(nums[:mid_node]), self.sortedArrayToBST(nums[mid_node + 1 :])
        ) 
  
# Check BST Validity
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def valid(node, minimum, maximum):
            if not node:
                return True
            
            if not (node.val > minimum and node.val < maximum):
                return False
            
            return valid(node.left, minimum, node.val) and valid(node.right, node.val, maximum)
        
        return valid(root, float("-inf"), float("inf"))


# Check if Tree is Balanced: O(n),O(h)(recursion stack, where h is the tree height)
# Example Usage:
# Balanced Tree:
#     1
#    / \
#   2   3
#  / \
# 4   5
# root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
# print(isBalanced(root))  # Output: True

# Unbalanced Tree:
#     1
#    / 
#   2   
#  / 
# 3
# root = TreeNode(1, TreeNode(2, TreeNode(3)))
# print(isBalanced(root))  # Output: False
# A binary tree is balanced if the heights of the two subtrees of any node never differ by more than 1.
# Calculate the height of each subtree recursively and check the balance condition.
def isBalanced(root):
    def check(node):
        if not node:
            return 0  # Height of empty tree is 0
        left_height = check(node.left)
        right_height = check(node.right)
        # If any subtree is unbalanced, propagate -1
        if left_height == -1 or right_height == -1 or abs(left_height - right_height) > 1:
            return -1
        return max(left_height, right_height) + 1
    
    return check(root) != -1

# Check if BT is complete tree O(n),O(n)
# A binary tree is complete if all levels except possibly the last are fully filled, and all nodes are as far left as possible.
# Example Usage:
# Complete Tree:
#     1
#    / \
#   2   3
#  / \
# 4   5
# root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
# print(isCompleteTree(root))  # Output: True
# Incomplete Tree:
#     1
#    / \
#   2   3
#    \
#     5
# root = TreeNode(1, TreeNode(2, None, TreeNode(5)), TreeNode(3))
# print(isCompleteTree(root))  # Output: False
# Use BFS to traverse the tree. After encountering a null node, no other nodes should exist.
def isCompleteTree(root):
    if not root:
        return True
    queue = deque([root])
    has_null = False  # Flag to detect gaps
    
    while queue:
        node = queue.popleft()
        if not node:
            has_null = True
        else:
            if has_null:  # Non-null node after a null
                return False
            queue.append(node.left)
            queue.append(node.right)
    return True


# Check if tree is Symmetric Tree
# We are going to left side and right side at the same time.
# We have two base cases.
# If both sides are null at the same time, return True because we reach the end of a tree.
# If one of sides is null, return False because it's not symmetric.
class Solution(object):
    def isSymmetric(self, root):
        
        def ismirror(node1,node2):
            if not node1 and not node2:
                return True
            if not node1 or not node2:
                return False
            return node1.val==node2.val and ismirror(node1.left,node2.right) and ismirror(node1.right,node2.left)
        if not root:
            return True
        return ismirror(root.left,root.right)

# Same Tree
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        
        if p and q and p.val == q.val:
            return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        
        return False

# Print Leaves
def get_leaves(root, leaves):
    if root is None:
        return
    if root.left is None and root.right is None:
        leaves.append(root.val)
        return
    get_leaves(root.left, leaves)
    get_leaves(root.right, leaves)
  
# Max Depth of a Binary Tree
# Using DFS
# 1 + max(left, right)
def maxDepth(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """
        if not root:
            return 0
        return 1+max(self.maxDepth(root.left),self.maxDepth(root.right))
#Using BFS
# Take root and check for right and left if it has child, then increase depth
class Solution(object):
    def maxDepth(self, root):
        if not root:
            return 0
        
        queue = deque()
        queue.append(root)
        depth = 0
        
        while queue:
            depth += 1
            
            for _ in range(len(queue)):
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        
        return depth  
 
# Diameter of Binary Tree (O(n)), (O(h))
# The diameter of a Binary Search Tree (BST) (or any binary tree) is defined as the longest path between any two nodes in the tree. This path may or may not pass through the root.
# Explanation of DFS Approach

# Recursive Height Calculation:
#   For each node, compute the height of its left and right subtrees.
# Update Diameter:
#   The diameter passing through the current node is left_height + right_height.
#   Track the maximum diameter encountered.
# Return Height:
#   Each node returns its height (1 + max(left_height, right_height)).
def diameterOfBST(root):
    diameter = 0

    def height(node):
        nonlocal diameter
        if not node:
            return 0
        left_height = height(node.left)
        right_height = height(node.right)
        diameter = max(diameter, left_height + right_height)
        return 1 + max(left_height, right_height)

    height(root)
    return diameter
# Example BST:
#       10
#      /  \
#     5    20
#         /  \
#       15    30
#            /
#          25
# root = TreeNode(10)
# root.left = TreeNode(5)
# root.right = TreeNode(20)
# root.right.left = TreeNode(15)
# root.right.right = TreeNode(30)
# root.right.right.left = TreeNode(25)

# Approach
# Compute Heights & Track Diameter Path:
# For each node, calculate the heights of left and right subtrees.
# If left_height + right_height is greater than the current diameter, update the diameter and store the path.
# Backtrack the Path:
# Once the diameter is found, backtrack from the deepest nodes to reconstruct the path.
def diameterOfBSTWithPath(root):
    if not root:
        return 0, []

    diameter = 0
    path = []

    def height(node):
        nonlocal diameter, path
        if not node:
            return 0, []
        
        left_height, left_path = height(node.left)
        right_height, right_path = height(node.right)
        
        # Update diameter and path if current node's path is longer
        if left_height + right_height > diameter:
            diameter = left_height + right_height
            path = left_path + [node.val] + right_path[::-1]  # Combine left, current, right (reversed)
        
        # Return the longer subtree's height and path
        if left_height > right_height:
            return left_height + 1, left_path + [node.val]
        else:
            return right_height + 1, right_path + [node.val]

    height(root)
    return diameter, path

# Max Sum Path in BST
# Use DFS
class Solution(object):
    def maxPathSum(self, root):
        self.max_sum = float('-inf')
        self.dfs(root)
        return self.max_sum
    
    def dfs(self, node):
        if not node:
            return 0
        
        left_max = max(self.dfs(node.left), 0)  # Ignore negative sums
        right_max = max(self.dfs(node.right), 0)
        
        current_path_sum = node.val + left_max + right_max
        self.max_sum = max(self.max_sum, current_path_sum)
        
        return node.val + max(left_max, right_max)  # Choose left or right path for parent


# Path Sum I equal to target
# If present or not
class Solution:
    def hasPathSum(self, root, targetSum):
        if not root:
            return False
        
        if not root.left and not root.right: # Reached Leaf Node
            return targetSum - root.val == 0
        
        targetSum -= root.val
        
        return self.hasPathSum(root.left, targetSum) or self.hasPathSum(root.right, targetSum)


# Path Sum II DFS + Backtrack Till Leaf
# find all root-to-leaf paths in a binary tree where the sum of the node values along the path equals a given target sum. 
# The solution involves traversing the tree using a depth-first search (DFS) approach, keeping track of the current path and
# the current sum of node values in that path. When we reach a leaf node, we check if the current sum matches the target sum, and if it does, we add the current path to our result list.
# Initialization: The pathSum function initializes the result list and starts the DFS traversal from the root node with an initial current sum of 0 and an empty current path.
# DFS Traversal: The dfs function is called recursively for each node. It adds the node's value to the current path and updates the current sum.
# Leaf Node Check: If the current node is a leaf (both left and right children are None), it checks if the current sum matches the target sum. If they match, the current path is added to the result list.
# Backtracking: After processing both the left and right subtrees, the node's value is removed from the current path to backtrack and explore other paths.
# Result Compilation: The result list, which contains all valid paths, is returned after the DFS traversal completes.
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        def hasPathSum(node, current_sum, current_path, result):
            if not node:
                return
            current_path.append(node.val) # Backtrack
            current_sum += node.val
            if not node.left and not node.right: # Reached Leaf Node
                if current_sum == targetSum:
                    result.append(list(current_path))
            else:
                hasPathSum(node.left, current_sum, current_path, result)
                hasPathSum(node.right, current_sum, current_path, result)
            current_path.pop() # Backtrack
        
        result = []
        hasPathSum(root, 0, [], result)
        return result

# Path sum III equal to Target - return count
# 1. Use a Hash Map (prefixSumCount):
# # Store prefix sums and their counts to track the number of times each sum has appeared.
# 2. Depth-First Search (DFS) Traversal:
# #  Start at the root and maintain a currentSum (prefix sum).
# #  Check how many times currentSum - targetSum has occurred → This gives the count of valid paths ending at the current node.
# #  Add currentSum to the hash map.
# #  Recur for left and right subtrees.
# #  Backtrack: Remove currentSum when returning to the previous node to maintain correctness.
class Solution(object):
    def pathSum(self, root, targetSum):
        prefixSumCount = defaultdict(int)
        prefixSumCount[0] = 1  # To handle cases where the entire path matches targetSum
        return self.dfs(root, 0, targetSum, prefixSumCount)

    def dfs(self, node, currentSum, targetSum, prefixSumCount):
        if not node:
            return 0

        currentSum += node.val
        count = prefixSumCount[currentSum - targetSum]
        
        prefixSumCount[currentSum] += 1
        
        count += self.dfs(node.left, currentSum, targetSum, prefixSumCount)
        count += self.dfs(node.right, currentSum, targetSum, prefixSumCount)
        
        prefixSumCount[currentSum] -= 1
        if prefixSumCount[currentSum] == 0:
            del prefixSumCount[currentSum]
        
        return count

   
# Lowest Common Ancestor of a Binary Tree
# The Lowest Common Ancestor (LCA) of two nodes in a Binary Tree is the deepest node that has both nodes as descendants (where we allow a node to be a descendant of itself).
#      3
#     / \
#    5   1
#   / \ / \
#  6  2 0  8
#    / \
#   7   4
# LCA of 5 and 1 → 3
# LCA of 5 and 4 → 5 (since 5 is an ancestor of 4)
# Approach to Find LCA
# 1. Recursive DFS (Optimal)
#   Traverse the tree recursively.
#   If either p or q is found, return the node.
#   If a node has both left and right subtrees returning non-null, it is the LCA.
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root or root == p or root == q: # If either p or q matches the current root, return the root
            return root
        
        left = self.lowestCommonAncestor(root.left, p, q) # Search for p and q in the left and right subtrees.
        right = self.lowestCommonAncestor(root.right, p, q)

        if left and right: # If both subtrees return non-null, root is the LCA.
            return root
        return left or right  # If only one subtree returns non-null, propagate that result upwards.
   
# Invert Binary Tree
# Swap left child to right child
class Solution(object):
    def invertTree(self, root):
        if not root:
            return
        temp = root.left
        root.left = root.right
        root.right = temp

        self.invertTree(root.left)
        self.invertTree(root.right)
        return root

# Kth Smallest in the BST / For largest, just reverse inorder.left->right
# Convert BST to array by Using Inorder
class Solution(object):
    def kthSmallest(self, root, k):
        values = []
        self.inorder(root, values)
        return values[k - 1]
    def inorder(self,root,values):
        if not root:
            return
        self.inorder(root.left,values)
        values.append(root.val)
        self.inorder(root.right,values)

# BT-Right Side View - Use BFS
#      3
#     / \
#    5   1
#   / \ / \
#  6  2 0  8
#    / \
#   7   4
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        res = []

        q = deque()
        q.append(root)

        while q:
            right_side = None

            for _ in range(len(q)):
                node = q.popleft()
                if node:
                    right_side = node
                    q.append(node.left)
                    q.append(node.right)
            
            if right_side:
                res.append(right_side.val)
        
        return res

# Construct Binary Tree from Preorder and Inorder Traversal
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:

        preorder = deque(preorder)

        def build(preorder, inorder):
            if inorder:
                idx = inorder.index(preorder.popleft())
                root = TreeNode(inorder[idx])

                root.left = build(preorder, inorder[:idx])
                root.right = build(preorder, inorder[idx+1:])

                return root

        return build(preorder, inorder)
    
# Expression Tree
# Post-Order Traversal (DFS):
# Evaluate left subtree
# Evaluate right subtree
# Apply the operator at the current node to the results from left and right
def evaluateExpressionTree(root):
    if not root:
        return 0
    
    # Leaf nodes are numbers
    if not root.left and not root.right:
        return int(root.val)
    
    # Recursively evaluate left and right subtrees
    left_val = evaluateExpressionTree(root.left)
    right_val = evaluateExpressionTree(root.right)
    
    # Apply the operator
    if root.val == '+':
        return left_val + right_val
    elif root.val == '-':
        return left_val - right_val
    elif root.val == '*':
        return left_val * right_val
    elif root.val == '/':
        return left_val // right_val  # Integer division
    
# Example Usage
# root = TreeNode('*')
# root.left = TreeNode('+')
# root.right = TreeNode('3')
# root.left.left = TreeNode('2')
# root.left.right = TreeNode('5')

# print(evaluateExpressionTree(root))  # Output: 21 (which is (2 + 5) * 3)


# Time & Space Complexity Table
# Problem	                 Time 	Space  Approach Used
# Sorted Array to BST	     O(N)	O(log N) (recursion stack)	Divide & Conquer (Mid = Root)
# Check BST Validity	     O(N)	O(H) (height of tree)	Inorder Traversal / DFS
# Check Symmetric Tree	     O(N)	O(H)	DFS (Mirror Comparison)
# Max Depth of Binary Tree	 O(N)	O(H)	DFS / BFS
# Print Leaves	             O(N)   O(H)	DFS
# Path Sum I (Target Exists) O(N)	O(H)	DFS
# Path Sum II (All Paths)	 O(N²)  O(N) 	DFS + Backtracking
# Path Sum III (Count Paths) O(N²) 	O(N)	DFS + Prefix Sum (Optimized)
# Lowest Common Ancestor   	 O(N)	O(H)	DFS (Post-order)
# Max Sum Path in BST	     O(N)	O(H)	DFS (Post-order)
# Invert Binary Tree	     O(N)	O(H)	DFS / BFS
# Kth Smallest in BST	     O(N) 	O(H)	Inorder Traversal
# Right Side View (BFS)	     O(N)	O(W) 	BFS (Level-order)
# Expression Tree Evaluation O(N)	O(H)	Post-order DFS


from collections import deque, defaultdict

def diagonalTraversal(root):
    if not root:
        return []

    # Use a dict to collect nodes at each diagonal level
    diagonal_map = defaultdict(list)
    queue = deque()
    
    # Queue contains pairs of (node, diagonal level)
    queue.append((root, 0))
    
    while queue:
        node, d = queue.popleft()
        
        while node:
            diagonal_map[d].append(node.val)
            if node.left:
                queue.append((node.left, d + 1))
            node = node.right  # stay on the same diagonal

    # Collect results sorted by diagonal level
    result = []
    for key in sorted(diagonal_map.keys()):
        result.append(' '.join(map(str, diagonal_map[key])))
    
    return result
Time: O(N) – each node is visited once.
Space: O(N) – space for queue and map.