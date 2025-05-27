# - **Activity Selection Problem/Interval Scheduling (Maximize Number of Non-Overlapping Jobs)**
#   - **Description**: A special case of interval scheduling where you have a single CPU/resource and need to maximize the number of tasks completed.
#   - **Key Concept**: Greedy approach. Sort by end time and pick the earliest-ending job that doesn’t conflict.
#   - **Example**: Input: activities = [[1,2], [3,4], [0,6], [5,7]]. Output: 3.
#   - **Difficulty**: Easy
#   - **Practice**: GeeksforGeeks Activity Selection Problem.

def activity_selection(activities):
    # Sort activities by end time
    activities.sort(key=lambda x: x[1])
    count = 0
    last_end = -float('inf')
    
    # Greedily select non-overlapping activities
    for start, end in activities:
        if start >= last_end:
            count += 1
            last_end = end
    
    return count

# Example usage
# activities = [[1,2], [3,4], [0,6], [5,7]]
# print(activity_selection(activities))  # Output: 3

# - **Job Scheduling with Deadlines**
#   - **Description**: Given jobs with durations and deadlines, maximize the number of jobs completed by their deadlines on a single CPU.
#   - **Key Concept**: Greedy. Sort jobs by deadline or duration and schedule them in a feasible order.
#   - **Example**: Input: jobs = [(1,4), (2,3), (1,2)] (duration, deadline). Output: 2 jobs.
#   - **Difficulty**: Easy
#   - **Practice**: GeeksforGeeks Job Sequencing Problem.

def job_scheduling_deadlines(jobs):
    # Sort jobs by deadline
    jobs.sort(key=lambda x: x[1])
    current_time = 0
    count = 0
    
    # Schedule jobs if they can be completed by deadline
    for duration, deadline in jobs:
        if current_time + duration <= deadline:
            current_time += duration
            count += 1
    
    return count

# Example usage
# jobs = [(1,4), (2,3), (1,2)]
# print(job_scheduling_deadlines(jobs))  # Output: 2

### 2. Weighted Job Scheduling
# These problems add weights or profits to jobs, requiring optimization of total profit rather than just the number of jobs.

# - **Weighted Interval Scheduling**
#   - **Description**: Given jobs with start times, end times, and weights (profits), find the maximum profit from a non-overlapping subset of jobs.
#   - **Key Concept**: Dynamic Programming (DP). Use a DP array where dp[i] represents the maximum profit up to job i, considering compatible jobs.
#   - **Example**: Input: jobs = [[1,4,3], [2,5,4], [4,6,2]] (start, end, profit). Output: 5 (select [1,4,3] and [4,6,2]).
#   - **Difficulty**: Medium
#   - **Practice**: LeetCode #1235 (Maximum Profit in Job Scheduling).
from bisect import bisect_right

def weighted_interval_scheduling(jobs):
    # Sort jobs by end time
    jobs.sort(key=lambda x: x[1])
    n = len(jobs)
    # dp[i] is max profit up to job i
    dp = [0] * (n + 1)
    
    # Store end times for binary search
    end_times = [job[1] for job in jobs]
    
    for i in range(n):
        # Option 1: Exclude current job
        dp[i + 1] = dp[i]
        # Option 2: Include current job
        # Find latest non-overlapping job using binary search
        j = bisect_right(end_times, jobs[i][0], 0, i) - 1
        dp[i + 1] = max(dp[i + 1], dp[j + 1] + jobs[i][2])
    
    return dp[n]

# Example usage
# jobs = [[1,4,3], [2,5,4], [4,6,2]]
# print(weighted_interval_scheduling(jobs))  # Output: 5

# - **Job Scheduling with Profit and Deadlines**
#   - **Description**: Given jobs with durations, deadlines, and profits, maximize total profit by scheduling jobs on a single CPU within deadlines.
#   - **Key Concept**: Greedy or DP. Sort by profit-to-duration ratio or use DP for optimal selection.
#   - **Example**: Input: jobs = [(2,5,50), (1,2,20), (3,5,30)]. Output: 70.
#   - **Difficulty**: Medium
#   - **Practice**: GeeksforGeeks Job Sequencing with Deadlines.
from bisect import bisect_right

def job_scheduling_profit_deadlines(jobs):
    # Sort jobs by deadline
    jobs.sort(key=lambda x: x[1])
    # Find maximum deadline
    max_deadline = max(job[1] for job in jobs)
    # DP array: max profit up to time t
    dp = [0] * (max_deadline + 1)
    # Store jobs ending at each time for processing
    time_slots = [[] for _ in range(max_deadline + 1)]
    
    # Group jobs by deadline
    for duration, deadline, profit in jobs:
        if duration <= deadline:
            time_slots[deadline].append((duration, profit))
    
    # Process each time point
    for t in range(1, max_deadline + 1):
        dp[t] = dp[t-1]  # Carry forward max profit
        for duration, profit in time_slots[t]:
            # Check if job can be scheduled ending at t
            if duration <= t:
                dp[t] = max(dp[t], dp[t - duration] + profit)
    
    return dp[max_deadline]

# Example usage
# jobs = [(2,5,50), (1,2,20), (3,5,30)]
# print(job_scheduling_profit_deadlines(jobs))  # Output: 70

### 3. Multi-CPU/Multi-Resource Scheduling
# These problems involve multiple CPUs or resources, adding complexity with resource constraints.

# - **Task Scheduling with Multiple CPUs**
#   - **Description**: Given n tasks with processing times and k CPUs, minimize the total completion time (makespan) by assigning tasks to CPUs.
#   - **Key Concept**: Greedy or Binary Search. Assign tasks to the CPU with the earliest finish time (min-heap) or use binary search to find the minimum makespan.
#   - **Example**: Input: tasks = [1,2,3,4], k = 2 CPUs. Output: 5 (CPU1: [1,4], CPU2: [2,3]).
#   - **Difficulty**: Medium
#   - **Practice**: LeetCode #1834 (Single-Threaded CPU, adapted for multi-CPU).

from heapq import heappush, heappop

def task_scheduling_multicpu(tasks, k):
    # Sort tasks in descending order
    tasks = sorted(tasks, reverse=True)
    # Min-heap to track CPU loads
    cpu_loads = [(0, i) for i in range(k)]  # (load, cpu_id)
    
    # Assign each task to CPU with minimum load
    for task in tasks:
        load, cpu_id = heappop(cpu_loads)
        heappush(cpu_loads, (load + task, cpu_id))
    
    # Makespan is the maximum load across CPUs
    return max(load for load, _ in cpu_loads)

# Example usage
# tasks = [1,2,3,4]
# k = 2
# print(task_scheduling_multicpu(tasks, k))  # Output: 5

# - **Interval Scheduling with k Resources**
#   - **Description**: Given jobs with start and end times and k CPUs, maximize the number of jobs scheduled without conflicts.
#   - **Key Concept**: Greedy or Min-Heap. Sort by start time and use a min-heap to track the earliest available CPU.
#   - **Example**: Input: jobs = [[1,3], [2,4], [3,5]], k = 2. Output: 3.
#   - **Difficulty**: Medium
#   - **Practice**: Codeforces or LeetCode #253 (Meeting Rooms II).

import heapq

def maxJobs(jobs, k):
    # Sort jobs by start time
    jobs.sort(key=lambda x: x[0])
    
    # Min-heap to store end times of jobs on each CPU
    heap = []
    count = 0  # Number of scheduled jobs
    
    for start, end in jobs:
        # Remove CPUs that are free (end time <= current job's start time)
        while heap and heap[0] <= start:
            heapq.heappop(heap)
        
        # If there's an available CPU or we can use a new CPU
        if len(heap) < k:
            heapq.heappush(heap, end)
            count += 1
    
    return count

# Example test case
# jobs = [[1, 3], [2, 4], [3, 5]]
# k = 2
# print(maxJobs(jobs, k))  # Output: 3

# - **Minimum Number of CPUs Required**
#   - **Description**: Given jobs with start and end times, find the minimum number of CPUs needed to schedule all jobs without conflicts.
#   - **Key Concept**: Sweep Line Algorithm. Track the maximum overlap of intervals to determine the minimum CPUs.
#   - **Example**: Input: jobs = [[1,3], [2,4], [2,5]]. Output: 3 CPUs.
#   - **Difficulty**: Medium
#   - **Practice**: LeetCode #253 (Meeting Rooms II).

### 4. Advanced Scheduling Problems
# These involve additional constraints like dependencies, priorities, or variable resources.

# - **Task Scheduling with Dependencies**
#   - **Description**: Given tasks with durations and dependencies (e.g., task A must finish before B), schedule them on k CPUs to minimize completion time.
#   - **Key Concept**: Topological Sort + Scheduling. Use topological sort to order tasks and assign them to CPUs using a min-heap.
#   - **Example**: Input: tasks = [1,2,3], dependencies = [(1,2), (2,3)], k = 2. Output: 4.
#   - **Difficulty**: Hard
#   - **Practice**: LeetCode #207/#210 (Course Schedule I/II, adapted for scheduling).

import heapq
from collections import defaultdict, deque

def task_scheduling_dependencies(tasks, dependencies, k):
    # Build adjacency list and in-degree
    n = len(tasks)
    graph = defaultdict(list)
    in_degree = [0] * n
    for u, v in dependencies:
        graph[u].append(v)
        in_degree[v] += 1
    
    # Topological sort using queue
    queue = deque([i for i in xrange(n) if in_degree[i] == 0])
    topo_order = []
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Schedule tasks on k CPUs
    heap = [(0, i) for i in xrange(k)]  # (end_time, cpu_id)
    heapq.heapify(heap)
    max_time = 0
    
    for task in topo_order:
        end_time, cpu_id = heapq.heappop(heap)
        new_end = max(end_time, tasks[task][0]) + tasks[task][1]  # start_time + duration
        max_time = max(max_time, new_end)
        heapq.heappush(heap, (new_end, cpu_id))
    
    return max_time

# Example usage
# tasks = [(0, 1), (0, 2), (0, 3)]  # (start_time, duration)
# dependencies = [(0, 1), (1, 2)]  # Task 0 -> 1, 1 -> 2
# k = 2
# print task_scheduling_dependencies(tasks, dependencies, k)  # Output: 6

# - **Earliest Finish Time with Priorities**
#   - **Description**: Given tasks with start times, durations, and priorities, schedule them on a single CPU to minimize completion time while respecting priorities.
#   - **Key Concept**: Priority Queue. Use a max-heap for priorities within the available time window.
#   - **Example**: Input: tasks = [(1,3,5), (2,4,3)] (start, duration, priority). Output: Optimal schedule.
#   - **Difficulty**: Hard
#   - **Practice**: LeetCode #1834 (Single-Threaded CPU).

import heapq

def earliest_finish_priorities(tasks):
    # Sort tasks by start time
    tasks.sort()  # tasks = [(start, duration, priority)]
    n = len(tasks)
    heap = []  # Max-heap for (priority, index) (negate priority for max-heap)
    result = []
    current_time = 0
    i = 0
    
    while i < n or heap:
        # Add all tasks that can start by current_time to heap
        while i < n and tasks[i][0] <= current_time:
            # Push (negative priority, index) for max-heap
            heapq.heappush(heap, (-tasks[i][2], i))
            i += 1
        
        if heap:
            # Pop task with highest priority
            priority, index = heapq.heappop(heap)
            result.append(index)
            current_time += tasks[index][1]  # Add duration
        else:
            # No tasks available, jump to next task's start time
            if i < n:
                current_time = tasks[i][0]
    
    return result

# Example usage
# tasks = [(1, 3, 5), (2, 4, 3)]  # (start, duration, priority)
# print earliest_finish_priorities(tasks)  # Output: [0, 1]

# - **Multi-Resource Scheduling with Constraints**
#   - **Description**: Schedule jobs requiring multiple resources (e.g., CPUs, memory) with start/end times and resource limits.
#   - **Key Concept**: Greedy or Constraint Optimization. Use a min-heap for resource availability or model as a graph problem.
#   - **Example**: Input: jobs = [(1,3,2 CPUs), (2,5,1 CPU)], total CPUs = 3. Output: Feasible schedule.
#   - **Difficulty**: Hard
#   - **Practice**: Custom problems on competitive programming platforms like Codeforces.

def multi_resource_scheduling(jobs, total_cpus):
    # Create events: (time, cpu_change, is_start)
    events = []
    for i, (start, end, cpus) in enumerate(jobs):
        events.append((start, cpus, True))
        events.append((end, -cpus, False))
    
    # Sort events by time; if times are equal, process end events first
    events.sort(key=lambda x: (x[0], x[2]))
    
    current_cpus = 0
    for time, cpu_change, is_start in events:
        current_cpus += cpu_change
        if current_cpus > total_cpus:
            return False  # Infeasible schedule
    return True

# Example usage
# jobs = [(1, 3, 2), (2, 5, 1)]  # (start, end, cpus_required)
# total_cpus = 3
# print multi_resource_scheduling(jobs, total_cpus)  # Output: True

# ### 5. Real-World Inspired Scheduling Problems
# These mimic real-world scenarios and often appear in system design or advanced interviews.

# - **Task Scheduler with Cooldown**
#   - **Description**: Given tasks and a cooldown period (e.g., same task can’t run within n time units), schedule on a single CPU to minimize total time.
#   - **Key Concept**: Greedy + Priority Queue. Use a frequency-based approach to schedule high-frequency tasks first.
#   - **Example**: Input: tasks = [A,A,B,B], cooldown = 2. Output: 7 (A -> B -> idle -> A -> B).
#   - **Difficulty**: Medium
#   - **Practice**: LeetCode #621 (Task Scheduler).

import heapq
from collections import Counter

def task_scheduler(tasks, cooldown):
    # Count frequency of each task
    freq = Counter(tasks)
    # Max-heap of frequencies (use negative for max-heap in Python)
    heap = [-f for f in freq.values()]
    heapq.heapify(heap)
    
    time = 0
    while heap:
        temp = []
        count = min(cooldown + 1, len(heap))  # Tasks in one cycle
        for _ in xrange(count):
            freq = -heapq.heappop(heap)
            if freq > 1:
                temp.append(-(freq - 1))
        # Add back tasks with remaining frequency
        for f in temp:
            heapq.heappush(heap, f)
        # If heap is empty, no idle time needed
        time += 1 if not heap else cooldown + 1
    
    return time

# Example usage
# tasks = ['A', 'A', 'B', 'B']
# cooldown = 2
# print task_scheduler(tasks, cooldown)  # Output: 7

# - **Shortest Job First with Arrival Times**
#   - **Description**: Given tasks with arrival times and durations, schedule on a single CPU to minimize average waiting time.
#   - **Key Concept**: Shortest Job First (SJF). Use a priority queue to pick the shortest job available at the current time.
#   - **Example**: Input: tasks = [(1,3), (2,2), (3,1)] (arrival, duration). Output: Schedule to minimize wait.
#   - **Difficulty**: Medium
#   - **Practice**: GeeksforGeeks Shortest Job First Scheduling.

import heapq

def shortest_job_first(tasks):
    # Sort tasks by arrival time
    tasks.sort()  # tasks = [(arrival, duration)]
    n = len(tasks)
    heap = []  # Min-heap for (duration, index)
    current_time = 0
    i = 0
    total_waiting_time = 0
    completed = [0] * n  # Store completion times
    
    while i < n or heap:
        # Add tasks that have arrived by current_time
        while i < n and tasks[i][0] <= current_time:
            heapq.heappush(heap, (tasks[i][1], i))  # (duration, index)
            i += 1
        
        if heap:
            # Process shortest job
            duration, index = heapq.heappop(heap)
            current_time += duration
            completed[index] = current_time
        else:
            # No tasks available, jump to next arrival
            if i < n:
                current_time = tasks[i][0]
    
    # Calculate average waiting time
    for i in xrange(n):
        waiting_time = completed[i] - tasks[i][0] - tasks[i][1]
        total_waiting_time += waiting_time
    
    return total_waiting_time / float(n)

# Example usage
# tasks = [(1, 3), (2, 2), (3, 1)]  # (arrival, duration)
# print shortest_job_first(tasks)  # Output: 1.0

# - **Job Scheduling with Preemption**
#   - **Description**: Schedule jobs with start times, durations, and the ability to preempt (pause/resume) on a single CPU to maximize profit or minimize completion time.
#   - **Key Concept**: Priority Queue or Segment Tree. Track preemptions and prioritize based on profit or deadlines.
#   - **Example**: Input: jobs = [(1,4,20), (2,3,10)] (start, end, profit). Output: Optimal schedule with preemption.
#   - **Difficulty**: Hard
#   - **Practice**: Advanced problems on HackerRank or Codeforces.

import heapq

def job_scheduling_preemption(jobs):
    # Sort jobs by start time
    jobs.sort()  # jobs = [(start, end, profit)]
    n = len(jobs)
    heap = []  # Min-heap for (end_time, profit, index)
    result = []  # Store (start, end, index) for scheduled segments
    total_profit = 0
    i = 0
    current_time = 0
    
    while i < n or heap:
        # Add jobs that start by current_time
        while i < n and jobs[i][0] <= current_time:
            heapq.heappush(heap, (jobs[i][1], jobs[i][2], i))  # (end, profit, index)
            i += 1
        
        # Remove jobs that have ended
        while heap and heap[0][0] <= current_time:
            heapq.heappop(heap)
        
        if heap:
            # Schedule job with highest profit
            end, profit, index = heap[0]
            result.append((current_time, min(end, current_time + 1), index))
            total_profit += profit * (min(end, current_time + 1) - current_time)
            current_time += 1
        else:
            # No jobs available, jump to next start time
            if i < n:
                current_time = jobs[i][0]
    
    return total_profit, result

# Example usage
# jobs = [(1, 4, 20), (2, 3, 10)]  # (start, end, profit)
# profit, schedule = job_scheduling_preemption(jobs)
# print profit  # Output: 30
# print schedule  # Output: [(1, 2, 0), (2, 3, 1), (3, 4, 0)]

# Here’s a **curated list of DSA problems** focused on **Task/Job Scheduling** with constraints like CPUs, start/end times, deadlines, and optimization goals (e.g., minimize CPUs, maximize throughput). These are essential for interview prep:

# ---

# ### **1. Basic Scheduling Problems**
# | **[Maximum Number of Events (LeetCode 1353)](https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended/)** | Events with `[start, last]` days | Attend **max # events** | Greedy + Min-Heap |
import heapq

def maxEvents(events):
    events.sort()  # Sort by start day
    heap = []  # Min-heap of end days
    count = 0  # Number of events attended
    i = 0  # Index for events
    day = 1  # Current day
    
    while heap or i < len(events):
        # Add events that can start on or before the current day
        while i < len(events) and events[i][0] <= day:
            heapq.heappush(heap, events[i][1])
            i += 1
        
        # Remove events that have expired
        while heap and heap[0] < day:
            heapq.heappop(heap)
        
        # Attend the event that ends earliest
        if heap:
            heapq.heappop(heap)
            count += 1
            day += 1
        elif i < len(events):
            # Jump to the next event's start day
            day = events[i][0]
        else:
            break
    
    return count

# Example
# events = [[1,2],[2,3],[3,4],[1,2]]
# print(maxEvents(events))  # Output: 4

# ### **2. CPU/Task Scheduling**
# | **[Minimum Number of CPUs (Custom Variant)](https://www.geeksforgeeks.org/minimize-number-of-platforms-required-for-railway-station/)** | Tasks with `[start, end]` | **Minimize CPUs** (similar to Meeting Rooms II) | Min-Heap |
import heapq

def minCPUsHeap(jobs):
    if not jobs:
        return 0
    # Sort jobs by start time
    jobs.sort(key=lambda x: x[0])
    
    # Min-heap to store end times of active jobs
    heap = []
    max_cpus = 0
    
    for start, end in jobs:
        # Remove jobs that have ended
        while heap and heap[0] <= start:
            heapq.heappop(heap)
        # Add current job's end time
        heapq.heappush(heap, end)
        # Update max CPUs needed
        max_cpus = max(max_cpus, len(heap))
    
    return max_cpus

# Example test case
# jobs = [[1, 3], [2, 4], [2, 5]]
# print(minCPUsHeap(jobs))  # Output: 3
# How It Works:

# Sort events by start day to process them chronologically.
# For each day, add all events that can start on or before the current day to a min-heap (by end day).
# Remove expired events (end day < current day).
# Attend the event with the earliest end day, increment the day, and repeat.
# If no events are available, jump to the next event’s start day.
# Complexity:

# Time: O(n log n + d log n), where n is the number of events and d is the range of days (due to sorting and heap operations).
# Space: O(n) for the heap.
# Example Explanation:

# Events: [[1,2], [1,2], [2,3], [3,4]].
# Day 1: Attend [1,2], heap = [2].
# Day 2: Attend [1,2], heap = [3].
# Day 3: Attend [2,3], heap = [4].
# Day 4: Attend [3,4], heap = [].
# Output: 4 events attended.


# | **[Employee Free Time (LeetCode 759)](https://leetcode.com/problems/employee-free-time/)** | Intervals from multiple employees | Find **common free time** | Merge Intervals + Min-Heap |
def employeeFreeTime(schedule):
    # Flatten all intervals into a single list
    intervals = []
    for emp in schedule:
        intervals.extend(emp)
    
    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])
    
    # Find gaps between intervals
    result = []
    prev_end = intervals[0][1]
    
    for start, end in intervals[1:]:
        if start > prev_end:
            result.append([prev_end, start])
        prev_end = max(prev_end, end)
    
    return result

# Example (using intervals as [start, end])
# schedule = [[[1,2],[5,6]], [[1,3]], [[4,10]]]
# print(employeeFreeTime(schedule))  # Output: [[3,4]]
# How It Works:

# Flatten all employees’ intervals into one list and sort by start time.
# Track the maximum end time (prev_end) of processed intervals.
# If the current interval’s start time is greater than prev_end, there’s a gap (free time) from prev_end to start.
# Update prev_end to the maximum of current end and prev_end.
# Complexity:

# Time: O(n log n), where n is the total number of intervals (due to sorting).
# Space: O(n) for storing intervals and results.
# Example Explanation:

# Intervals: [1,2], [1,3], [4,10], [5,6].
# Sorted: [1,2], [1,3], [4,10], [5,6].
# Process: prev_end = 2, then 3, gap [3,4] (since 4 > 3), then prev_end = 10.
# Output: [[3,4]] (free time between 3 and 4).

# | **[Process Tasks (LeetCode 1834)](https://leetcode.com/problems/single-threaded-cpu/)** | Tasks with `[enqueueTime, processingTime]` | Schedule in **shortest processing time (SPT)** order | Min-Heap |
import heapq

def getOrder(tasks):
    # Add index to each task and sort by enqueue time
    tasks = sorted((t[0], t[1], i) for i, t in enumerate(tasks))
    
    result = []  # Order of task indices
    heap = []    # Min-heap of (processingTime, index)
    time = tasks[0][0]  # Current time
    i = 0  # Index for tasks
    
    while i < len(tasks) or heap:
        # Add tasks that are available (enqueueTime <= time)
        while i < len(tasks) and tasks[i][0] <= time:
            heapq.heappush(heap, (tasks[i][1], tasks[i][2]))  # (processingTime, index)
            i += 1
        
        if heap:
            # Process task with shortest processing time
            proc_time, idx = heapq.heappop(heap)
            result.append(idx)
            time += proc_time  # Advance time
        else:
            # Jump to next task's enqueue time
            time = tasks[i][0]
    
    return result

# Example
# tasks = [[1,2],[2,4],[3,2],[4,1]]
# print(getOrder(tasks))  # Output: [0,2,3,1]
# How It Works:

# Sort tasks by enqueueTime, including their original index.
# Maintain a min-heap of available tasks, prioritized by processingTime (then index).
# For each step, add all tasks with enqueueTime ≤ current time to the heap.
# Pop the task with the shortest processing time, add its index to the result, and advance time.
# If the heap is empty, jump to the next task’s enqueueTime.
# Complexity:

# Time: O(n log n), where n is the number of tasks (sorting + heap operations).
# Space: O(n) for the heap and result.
# Example Explanation:

# Tasks: [[1,2], [2,4], [3,2], [4,1]].
# Sorted: [(1,2,0), (2,4,1), (3,2,2), (4,1,3)].
# Process: At time 1, process task 0 (time += 2 → 3); at time 3, process task 2 (time += 2 → 5); at time 5, process task 3 (time += 1 → 6); at time 6, process task 1.
# Output: [0,2,3,1].


# | **[Interval Scheduling Maximization](https://www.geeksforgeeks.org/activity-selection-problem-greedy-algo-1/)** | Jobs with `[start, finish]` | **Maximize non-overlapping jobs** | Greedy (Sort by finish time) |
# | **[Job Sequencing Deadline (GfG)](https://www.geeksforgeeks.org/job-sequencing-problem/)** | Jobs with `[deadline, profit]` | **Maximize profit** | Greedy + Union-Find |
# | **[Parallel Courses III (LeetCode 2050)](https://leetcode.com/problems/parallel-courses-iii/)** | DAG with course dependencies | **Minimize completion time** | Topological Sort + DP |
from collections import defaultdict, deque

def minimumTime(n, relations, time):
    # Build adjacency list and in-degree count
    graph = defaultdict(list)
    in_degree = [0] * n
    for prev, next in relations:
        graph[prev - 1].append(next - 1)
        in_degree[next - 1] += 1
    
    # Initialize max time to reach each course
    max_time = [0] * n
    queue = deque()
    
    # Start with courses that have no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
            max_time[i] = time[i]
    
    # Process courses in topological order
    while queue:
        curr = queue.popleft()
        for next_course in graph[curr]:
            # Update max time for next course
            max_time[next_course] = max(max_time[next_course], max_time[curr] + time[next_course])
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return max(max_time)

# Example
# n = 3
# relations = [[1,3],[2,3]]
# time = [3,2,5]
# print(minimumTime(n, relations, time))  # Output: 8
# How It Works:

# Build a directed graph and track in-degrees for each course.
# Initialize a queue with courses that have no prerequisites and set their completion time to time[i].
# Process each course, updating the maximum time to complete dependent courses (time to complete prev + time[next]).
# The maximum value in max_time is the minimum time to complete all courses.
# Complexity:

# Time: O(n + m), where n is the number of courses and m is the number of relations (graph construction + topological sort).
# Space: O(n + m) for the graph and queue.
# Example Explanation:

# Courses: 1, 2, 3; Relations: 1→3, 2→3; Time: [3,2,5].
# Course 1 takes 3, course 2 takes 2, course 3 takes 5 but requires 1 and 2.
# Completion times: Course 1 (3), Course 2 (2), Course 3 (max(3,2) + 5 = 8).
# Output: 8.

# | **[Minimum Time to Complete All Tasks (LeetCode 2589)](https://leetcode.com/problems/minimum-time-to-complete-all-tasks/)** | Tasks with `[start, end, duration]` | **Find min total time** | Greedy + Sweep Line |
def findMinimumTime(tasks):
    # Sort tasks by end time
    tasks.sort(key=lambda x: x[1])
    
    # Track which time points are used
    used = [False] * 2001  # Time range is 1 to 2000 per constraints
    total_time = 0
    
    for start, end, duration in tasks:
        # Count how many time points are already used in [start, end]
        used_count = sum(used[start:end + 1])
        remaining = duration - used_count
        
        # Assign remaining duration to unused time points, starting from end
        if remaining > 0:
            for t in range(end, start - 1, -1):
                if not used[t] and remaining > 0:
                    used[t] = True
                    total_time += 1
                    remaining -= 1
    
    return total_time

# Example
# tasks = [[2,3,1],[4,5,1],[1,5,2]]
# print(findMinimumTime(tasks))  # Output: 2
# How It Works:

# Sort tasks by end time to process them greedily.
# For each task, check how many time points in [start, end] are already used.
# Assign the remaining duration to unused time points, starting from the end (to maximize overlap with future tasks).
# Track the total number of used time points.
# Complexity:

# Time: O(n log n + n * T), where n is the number of tasks and T is the maximum time range (2000 per constraints).
# Space: O(T) for the used array.
# Example Explanation:

# Tasks: [[2,3,1], [4,5,1], [1,5,2]].
# Sorted by end: [[2,3,1], [4,5,1], [1,5,2]].
# Task [2,3,1]: Use time 3, total_time = 1.
# Task [4,5,1]: Use time 5, total_time = 2.
# Task [1,5,2]: Need 2, time 3 and 5 are used, so done (2 already satisfied).
# Output: 2.

# ### Key Concepts and Techniques to Master
# - **Greedy Algorithms**: For interval scheduling, activity selection, and profit maximization.
# - **Dynamic Programming**: For weighted interval scheduling and complex constraints.
# - **Priority Queues/Min-Heaps**: For multi-CPU scheduling and task prioritization.
# - **Sweep Line Algorithm**: For determining resource requirements (e.g., minimum CPUs).
# - **Topological Sort**: For scheduling with dependencies.
# - **Binary Search**: For optimizing makespan or resource allocation.
# - **Segment Trees/Fenwick Trees**: For advanced problems with range queries or preemption.

# ### Tips for Interview Preparation
# 1. **Understand Constraints**: Clarify if the problem involves single/multiple CPUs, dependencies, preemption, or deadlines.
# 2. **Choose the Right Approach**: Greedy works for non-overlapping jobs; DP for weighted cases; heaps for resource allocation.
# 3. **Practice Edge Cases**: Empty input, overlapping intervals, tight deadlines, or equal priorities.
# 4. **Optimize Time Complexity**: Aim for O(n log n) solutions using sorting or heaps; avoid brute force.
# 5. **Explain Your Thought Process**: In interviews, walk through your approach (e.g., why you chose greedy over DP).
