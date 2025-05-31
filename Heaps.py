# Python program to find the k largest elements in the  
# array using min heap

import heapq

# Function to find the k largest elements in the array 	O(n log k)	O(k)s
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


# K most Frequent Words in a File O(n + m log k)	O(m + k)
### Get K most frequent words in a file ?? Try using MinHeap
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
# Example Usage
text = 'Welcome to the world of Geeks Geeks for Geeks is great'
k = 3
print(k_most_frequent_words(text, k))

# Kth Largest element in an array using max heap
import heapq

# Function to find the kth smallest array element O(n log K)	O(K)
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
# Driver's code
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
            heapq.heappop(heap)  # Reuse the room - pop
        heapq.heappush(heap, end)  # Assign a new room - push
    return len(heap)

# Meeting Rooms III
# Given n rooms and meetings [start, end], assign meetings to rooms such that delays are minimized.
# Use two heaps (available rooms + ongoing meetings).
# Time: O(M log N) (M = number of meetings)
# Space: O(N)

import heapq

def min_total_delay(n, meetings):
    # Sort meetings by their start times
    meetings.sort()

    # Heap to track current room usage: (end_time, room_index)
    room_heap = []

    # Initially, all rooms are free
    for room in range(n):
        heapq.heappush(room_heap, (0, room))  # (available_time, room_index)

    total_delay = 0

    for start, end in meetings:
        duration = end - start

        # Get the earliest available room
        avail_time, room = heapq.heappop(room_heap)

        if avail_time <= start:
            # Room is free, no delay
            new_end = start + duration
            delay = 0
        else:
            # Room isn't free, delay the meeting
            delay = avail_time - start
            new_end = avail_time + duration
            total_delay += delay

        # Assign meeting and update room availability
        heapq.heappush(room_heap, (new_end, room))

    return total_delay


import heapq

def mostBooked(n, meetings):
    # Sort the meetings by their start time
    meetings.sort()

    # Available rooms stored by index (always use smallest index first)
    available_rooms = list(range(n))
    heapq.heapify(available_rooms)

    # In-use rooms stored as (end_time, room_index)
    used_rooms = []

    # Track how many meetings each room hosted
    meeting_count = [0] * n

    for start, end in meetings:
        # Free up rooms whose meetings ended before this one starts
        while used_rooms and used_rooms[0][0] <= start:
            end_time, room_index = heapq.heappop(used_rooms)
            heapq.heappush(available_rooms, room_index)

        duration = end - start

        if available_rooms:
            # Use the available room with the smallest index
            room = heapq.heappop(available_rooms)
            heapq.heappush(used_rooms, (end, room))
        else:
            # All rooms are busy — delay the meeting to the earliest room available
            earliest_end, room = heapq.heappop(used_rooms)
            new_end = earliest_end + duration
            heapq.heappush(used_rooms, (new_end, room))

        # Increment count for the room used
        meeting_count[room] += 1
    
    # Find the room with maximum meetings
    max_count = max(meeting_count)
    return meeting_count.index(max_count)
# Time: O(m log n) where m = number of meetings, n = number of rooms
# Sorting: O(m log m)
# Each meeting may insert/remove from heap: O(log n)
# Space: O(n) for heaps and room counters