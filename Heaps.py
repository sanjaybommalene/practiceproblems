# Python program to find the k largest elements in the  
# array using min heap

import heapq

# Function to find the k largest elements in the array 
def kLargest(arr, k):
  
    # Create a min-heap with the first k elements
    minH = arr[:k]
    heapq.heapify(minH)
    
    # Traverse the rest of the array
    for x in arr[k:]:
        if x > minH[0]:
            heapq.heapreplace(minH, x)
    
    res = []

    # Min heap will contain only k 
    # largest element
    while minH:
        res.append(heapq.heappop(minH))

    # Reverse the result array, so that all
    # elements are in decreasing order
    res.reverse()

    return res

if __name__ == "__main__":
    arr = [1, 23, 12, 9, 30, 2, 50]
    k = 3
    res = kLargest(arr, k)
    print(" ".join(map(str, res)))
# Result: 50 30 23


# K most Frequent Words in a File
### Get K most frequent words in a file ?? Try using MinHeap
def process_text(text, k):
    
    # Store Frequencies of all words
    freq_map = Counter(text.split())
    
    # Get the top k frequent items
    res = freq_map.most_common(k)
    print(res)
    for word, freq in res:
        print(f'{word} : {freq}')

if __name__ == '__main__':
    text = 'Welcome to the world of Geeks Geeks for Geeks is great'
    process_text(text, 5)
    # to read from file
    # with open('file.txt', 'r') as file:
    #     text = file.read()
    #     process_text(text, k)

# Using MinHeap    O(nlogk)
from collections import Counter
import heapq

def k_most_frequent_words(text, k):
    # Count word frequencies
    word_counts = Counter(text.split())

    # Min Heap to keep top K elements
    min_heap = []

    for freq, word in word_counts.items():
        heapq.heappush(min_heap, (freq, word))  # Push (frequency, word)
        if len(min_heap) > k:
            heapq.heappop(min_heap)  # Remove the least frequent word

    # Extract results in descending order of frequency
    return sorted(min_heap, key=lambda x: -x[0])

#Using Array-O(n)
from collections import Counter
class Solution(object):
    def k_most_frequent_words(text, k):
        words = Counter(text.split())
        freq = {i:[] for i in range(len(words) + 1)}
        for word, count in words.items():
            freq[count].append(word)
        
        res = []

        for i in range(len(freq) - 1, -1, -1):
            for word in freq[i]:
                res.append(word)
                if len(res) == k:
                    return res
                
# Example Usage
text = 'Welcome to the world of Geeks Geeks for Geeks is great'
k = 3
print(k_most_frequent_words(text, k))

# Kth Largest element in an array using max heap
import heapq

# Function to find the kth smallest array element
def kthSmallest(arr, K):
    # Create a max heap (priority queue)
    max_heap = []

    # Iterate through the array elements
    for num in arr:
        # Push the negative of the current element onto the max heap
        heapq.heappush(max_heap, -num)

        # If the size of the max heap exceeds K, remove the largest element
        if len(max_heap) > K:
            heapq.heappop(max_heap)

    # Return the Kth smallest element (top of the max heap, negated)
    return -max_heap[0]
# Driver's code:
if __name__ == "__main__":
    arr = [10, 5, 4, 3, 48, 6, 2, 33, 53, 10]
    K = 4

    # Function call
    print("Kth Smallest Element is:", kthSmallest(arr, K))
#Result:
# [-10, -5, -4, -3]
# [-6, -5, -4, -3]
# [-5, -3, -4, -2]
# [-5, -3, -4, -2]
# [-5, -3, -4, -2]
# [-5, -3, -4, -2]
# [-5, -3, -4, -2]
# Kth Smallest Element is: 5

# Task Scheduler (Greedy + Max Heap) Time: O(N log N)
# Problem:
# Schedule tasks with cooldown n to minimize total time.
# Approach:
# Max-Heap to schedule most frequent tasks first.
# Queue to manage cooldown periods.
def leastInterval(tasks, n):
    task_counts = Counter(tasks)
    max_heap = [-cnt for cnt in task_counts.values()]
    heapq.heapify(max_heap)

    time = 0

    while max_heap:
        temp = []
        for _ in range(n + 1):
            if max_heap: # During edge case, 2 elements remaining, for loop tries 3 times so use if condition
                temp.append(heapq.heappop(max_heap))
        
        for cnt in temp:
            if cnt + 1 < 0:
                heapq.heappush(max_heap, cnt + 1)
        
        time += n + 1 if max_heap else len(temp)
    
    return time
# Input: tasks = ["A","A","A","A","B","B","C","C","D","D","E"]
# n = 2
# Output
# MaxHeap = [-4, -2, -2, -2, -1]
# [-4, -2, -2]
# [-3, -1, -2, -1, -1]
# [-3, -2, -1]
# [-2, -1, -1, -1]
# [-2, -1, -1]
# [-1, -1]
# [-1, -1]
# 11

# Meeting Rooms I
# Given an array of meeting time intervals [start, end], determine if a person can attend all meetings.
# Time: O(N log N)
# Space: O(1)
def canAttendMeetings(intervals):
    intervals.sort()
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True

# Meeting Rooms II
# Find the minimum number of rooms required to schedule all meetings.
# Sort start/end times and use two pointers or a min-heap.
# Time: O(N log N) (sorting + heap operations).
# Space: O(N) (heap storage).
def minMeetingRooms(intervals):
    intervals.sort()  # Sort by start time
    heap = []
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)  # Reuse the room
        heapq.heappush(heap, end)  # Assign a new room
    return len(heap)

# Meeting Rooms III
# Given n rooms and meetings [start, end], assign meetings to rooms such that delays are minimized.
# Use two heaps (available rooms + ongoing meetings).
# Time: O(M log N) (M = number of meetings)
# Space: O(N)
def mostBooked(n, meetings):
    meetings.sort()
    available = list(range(n))
    busy = []  # (end_time, room)
    count = [0] * n
    
    for start, end in meetings:
        # Free up rooms where meetings end <= start
        while busy and busy[0][0] <= start:
            _, room = heapq.heappop(busy)
            heapq.heappush(available, room)
        
        if available:
            room = heapq.heappop(available)
            heapq.heappush(busy, (end, room))
        else:
            earliest_end, room = heapq.heappop(busy)
            heapq.heappush(busy, (earliest_end + (end - start), room))
        
        count[room] += 1
    
    return count.index(max(count))
