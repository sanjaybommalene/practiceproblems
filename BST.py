# Definition for a binary tree node.
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
        
        q = deque()
        q.append(root)
        depth = 0
        
        while q:
            depth += 1
            
            for _ in range(len(q)):
                node = q.popleft()
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
        
        return depth  
 
# Diameter of Binary Tree
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        res = 0 
        def dfs(root):
            if not root:
                return 0
            
            l = dfs(root.left)
            r = dfs(root.right)

            nonlocal res
            res = max(res, l + r)

            return 1 + max(l, r)

        dfs(root)
        return res

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

# Path Sum I equal to target
# If present or not
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False
        
        if not root.left and not root.right:
            return targetSum - root.val == 0
        
        targetSum -= root.val
        
        return self.hasPathSum(root.left, targetSum) or self.hasPathSum(root.right, targetSum)


# Path Sum II
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
        def dfs(node, current_sum, current_path, result):
            if not node:
                return
            current_path.append(node.val)
            current_sum += node.val
            if not node.left and not node.right:
                if current_sum == targetSum:
                    result.append(list(current_path))
            else:
                dfs(node.left, current_sum, current_path, result)
                dfs(node.right, current_sum, current_path, result)
            current_path.pop()
        
        result = []
        dfs(root, 0, [], result)
        return result

# Path sum III equal to Target
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

# Max Sum Path in BST
# Use DFS
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        # res = [float('-inf')] Python 2
        res = root.val 

        def dfs(node):
            nonlocal res # Not Needed in python 2

            if not node:
                return 0
            
            # recursively compute the maximum sum of the left and right subtree paths
            left_sum = max(0, dfs(node.left))
            right_sum = max(0, dfs(node.right))

            # update the maximum path sum encountered so far(with split)
            res = max(res, left_sum + right_sum + node.val)

            # return the maximum sum of the path(without split)
            return max(left_sum, right_sum) + node.val

        dfs(root)
        return res
   
# Lowest Common Ancestor of a Binary Tree
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root or root == p or root == q:
            return root
        
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        if left and right:
            return root
        return left or right  
   
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

#Kth Smallest in the BST / For largest, just reverse inorder.left->right
#Use Inorder
class Solution(object):
    def kthSmallest(self, root, k):
        """
        :type root: Optional[TreeNode]
        :type k: int
        :rtype: int
        """
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
    