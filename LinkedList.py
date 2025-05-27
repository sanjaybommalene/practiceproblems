# Definition for singly-linked list.
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # Points to the next node
class LinkedList:
    def __init__(self):
        self.head = None  # Start with an empty list

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, key):
        curr = self.head
        prev = None

        while curr and curr.data != key:
            prev = curr
            curr = curr.next

        if curr is None:
            return  # Key not found

        if prev is None: # Found at beginning
            self.head = curr.next  # Deleting head node
        else:
            prev.next = curr.next  # Bypass the current node

    def search(self, key):
        curr = self.head
        while curr:
            if curr.data == key:
                return True
            curr = curr.next
        return False

    def display(self):
        curr = self.head
        while curr:
            print(curr.data, end=" -> ")
            curr = curr.next
        print("None")


# Detect cycle in a Linked List O(N),O(1)
# Haire-Tortoise solution
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        fast = head
        slow = head

        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast == slow:
                return True
        return False
    
# Detect Cycle - II (Medium) Return Cycle starting Node O(N),O(1)
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                break
        else: return None

        fast = head

        while fast != slow:
            fast = fast.next
            slow = slow.next
        
        return slow
    
#Intersection of Node O(M+N),O(1)
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        lista = headA
        listb = headB
        while lista != listb:
            lista = lista.next if lista else headB #switch it to the head of the other list.
            listb = listb.next if listb else headA #assign other list to this 
        
        return listb
    
#Reverse Linked List O(N),O(1)
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        node = None # Buffer node to hold
        while head: 
            temp = head.next
            head.next = node
            node = head
            head = temp
        return node

# Reverse Between nodes
# tcn,cntn,tnpn,pnt
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:

        if not head or left == right:
            return head

        res = ListNode(0, head)
        prev = res

        for _ in range(left - 1):
            prev = prev.next

        cur = prev.next
        for _ in range(right - left):
            temp = cur.next
            cur.next = temp.next
            temp.next = prev.next
            prev.next = temp

        return res.next
    
# Merge Sorted Linked Lists O(M+N),O(1)
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1:
            return list2
        if not list2:
            return list1
        if list1.val<list2.val:
            result = list1
            result.next = self.mergeTwoLists(list1.next,list2)
        else:
            result = list2
            result.next = self.mergeTwoLists(list1,list2.next)
        return result
    
# Sort a Linked List
# Use Merge Sort, Get Middle(Hare-Tortoise) and Sort left and right
class Solution:
# Function to find the middle of the linked list
    def get_middle(head):
        if not head:
            return head
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    # Merge two sorted linked lists
    def sorted_merge(self,left, right):
        if not left:
            return right
        if not right:
            return left
        if left.data <= right.data:
            result = left
            result.next = self.sorted_merge(left.next, right)
        else:
            result = right
            result.next = self.sorted_merge(left, right.next)
        return result

    # Merge sort for linked list
    def merge_sort(self,head):
        if not head or not head.next:
            return head
        middle = self.get_middle(head)
        next_to_middle = middle.next
        middle.next = None
        left = self.merge_sort(head)
        right = self.merge_sort(next_to_middle)
        sorted_list = self.sorted_merge(left, right)
        return sorted_list

    # Utility function to print linked list
    def print_list(head):
        while head:
            print(head.data, end=" -> ")
            head = head.next
        print("None")

    # Example usage
    head = Node(4)
    head.next = Node(2)
    head.next.next = Node(1)
    head.next.next.next = Node(3)

    print("Original List:")
    print_list(head)

    sorted_head = merge_sort(head)

    print("Sorted List:")
    print_list(sorted_head)

# Palindrome Linked List O(N),O(1)
# using Array 
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        arr = []
        while head:
            arr.append(head.val)
            head=head.next
        l,r=0,len(arr)-1
        while l<r and arr[l]==arr[r]:
            l+=1
            r-=1
        return l>=r

# Using mid-reverse linked list O(N),O(1)
class Solution:
    def reverse(self, head: ListNode) -> ListNode:
        node = None
        while head:
            temp = head.next
            head.next = node
            node = head
            head = temp
        return node

    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        slow=fast=head
        #Find mid
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        rev = self.reverse(slow)
        while rev:
            if head.val!=rev.val:
                return False
            head = head.next
            rev = rev.next
        return True   

# Remove nth-node from linked list O(N),O(1)
def removeNthFromEnd(head, n):
    dummy = ListNode(0)
    dummy.next = head
    fast = slow = dummy
    
    # Move fast n steps ahead
    for _ in range(n):
        fast = fast.next
    
    # Move both until fast reaches the end
    while fast.next:
        fast = fast.next
        slow = slow.next
    
    # Remove the nth node from the end
    slow.next = slow.next.next
    
    return dummy.next
    # [1,2,3,4,5]
    #    d   h
    # r

    # [1,2,3,4,5]
    #      d   h
    #  r

# Add two linked list O(max(N, M)), O(max(N, M))
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        
        dummy = ListNode()
        res = dummy
        
        total = carry = 0

        while l1 or l2 or carry:
            total=carry
            if l1:
                total+=l1.val
                l1= l1.next
            if l2:
                total+=l2.val
                l2=l2.next

            num = total % 10
            carry = total // 10
            dummy.next = ListNode(num)
            dummy=dummy.next
            
        return res.next
    # Input: l1 = [2,4,3], l2 = [5,6,4]
    # Output: [7,0,8]
    # Explanation: 342 + 465 = 807.

# Remove Duplicates in Sorted Linked List
def deleteDuplicates(head):
    current = head
    while current and current.next:
        if current.val == current.next.val:
            current.next = current.next.next
        else:
            current = current.next
    return head
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        res = ListNode(0, head)
        prev = res
        current = head

        while current:
            is_duplicate = False

            while current.next and current.val == current.next.val:
                is_duplicate = True
                current = current.next

            if is_duplicate:
                prev.next = current.next
            else:
                prev = prev.next

            current = current.next

        return res.next

# Rotate Linked List O(N),O(1)
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head or not head.next or k == 0:
            return head

        # Step 1: Count the length of the list
        length = 1
        tail = head
        while tail.next:
            tail = tail.next
            length += 1

        # Step 2: Make the list circular
        tail.next = head

        # Step 3: Find the new tail: (length - k % length - 1)th node
        k = k % length
        steps_to_new_tail = length - k
        new_tail = head
        for _ in range(steps_to_new_tail - 1):
            new_tail = new_tail.next

        # Step 4: Break the circle
        new_head = new_tail.next
        new_tail.next = None

        return new_head
    
# Partition Linked List
# Given the head of a linked list and a value x, partition it such that all nodes less than x come before nodes greater than or equal to x.
def partition(head, x):
    # Dummy nodes to simplify merging
    before_head = ListNode(0)
    after_head = ListNode(0)
    before = before_head
    after = after_head
    
    current = head
    while current:
        if current.val < x:
            before.next = current
            before = before.next
        else:
            after.next = current
            after = after.next
        current = current.next
    
    # Connect the two lists
    before.next = after_head.next
    after.next = None  # Terminate the list
    
    return before_head.next
    
# Swap Node pair
# Keep the second node and next pair node
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        res = ListNode(0,head)
        prev,cur=res,head

        while cur and cur.next:
            third=cur.next.next
            second=cur.next

            second.next = cur
            cur.next = third
            prev.next = second
            # Re-assign prev and cur
            prev = cur
            cur = third
        return res.next
# Input: head = [1,2,3]
# Output: [2,1,3]

# Merge K sort lists: O(Nlogk) O(1)
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists or len(lists) == 0:
            return None
        while len(lists) > 1:
            mergedLists = []
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                l2 = lists[i+1] if i + 1 < len(lists) else None
                mergedLists.append(self.mergeTwoLists(l1, l2))
            lists = mergedLists
        
        return lists[0]
    # re-usable merge two lists
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1:
            return list2
        if not list2:
            return list1
        if list1.val<list2.val:
            result = list1
            result.next = self.mergeTwoLists(list1.next,list2)
        else:
            result = list2
            result.next = self.mergeTwoLists(list1,list2.next)
        return result
    
# Divide and conquer Solution
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        return self.divideAndConquer(lists, 0, len(lists) - 1)

    def divideAndConquer(self, lists: List[Optional[ListNode]], left: int, right: int) -> Optional[ListNode]:
        if left == right:
            return lists[left]

        mid = (right-left) // 2
        l1 = self.divideAndConquer(lists, left, mid)
        l2 = self.divideAndConquer(lists, mid + 1, right)
        return self.mergeTwoLists(l1, l2)

    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1:
            return list2
        if not list2:
            return list1
        if list1.val<list2.val:
            result = list1
            result.next = self.mergeTwoLists(list1.next,list2)
        else:
            result = list2
            result.next = self.mergeTwoLists(list1,list2.next)
        return result
    
# Flatten BT to linked list in-place O(N), O(H)
# Do a reverse preorder: right → left → root.
# Keep track of the previously visited node (prev).
# At each node:
# Set node.right = prev
# Set node.left = None
# Update prev = node
class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        prev = None

        def dfs(node):
            nonlocal prev
            if not node:
                return
            dfs(node.right)   # first flatten right subtree
            dfs(node.left)    # then flatten left subtree
            node.right = prev # set current node's right to previously processed node
            node.left = None  # set left to None
            prev = node       # move prev to current node

        dfs(root)

# Morris Traversal O(N) O(1)
# If left child exists:
#   Find the rightmost node of the left subtree (predecessor).
#   Connect predecessor's right to current node’s right.
#   Move current’s left subtree to the right.
#   Set left to None.
# Move current to current’s right.
def flatten(root):
    current = root

    while current:
        if current.left:
            # Find the rightmost node of the left subtree
            predecessor = current.left
            while predecessor.right:
                predecessor = predecessor.right

            # Connect the predecessor's right to current's right subtree
            predecessor.right = current.right

            # Move left subtree to right
            current.right = current.left
            current.left = None

        # Move to next node (always right child)
        current = current.right

# LRU Cache - O(1) for both get and put (due to hashmap + doubly linked list), O(capacity) (for storing nodes and hashmap).
class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        self.head = Node(0, 0)  # dummy head
        self.tail = Node(0, 0)  # dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Remove a node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node):
        """Add a node right before the tail."""
        last_node = self.tail.prev
        last_node.next = node
        node.prev = last_node
        node.next = self.tail
        self.tail.prev = node

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)  # Remove from current position
            self._add(node)    # Move to most recently used (tail)
            return node.val
        return -1

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])  # Remove existing node
        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add(new_node)  # Add to most recently used (tail)
        
        if len(self.cache) > self.capacity:
            # Evict LRU (head.next is least recently used)
            lru_node = self.head.next
            self._remove(lru_node)
            del self.cache[lru_node.key]

