def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    # Merge two sorted arrays
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left

        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    
    return arr

def counting_sort(arr):
    max_val = max(arr)
    count = [0] * (max_val + 1)
    output = [0] * len(arr)
    
    for num in arr:
        count[num] += 1
    
    for i in range(1, len(count)):
        count[i] += count[i-1]
    
    for num in reversed(arr):
        output[count[num] - 1] = num
        count[num] -= 1
    
    return output

def radix_sort(arr):
    def counting_sort_for_digit(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = arr[i] // exp
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            i -= 1

        for i in range(n):
            arr[i] = output[i]

    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_for_digit(arr, exp)
        exp *= 10
    
    return arr

# Example usage
if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]
    
    print("Original array:", arr)
    
    # Merge Sort
    print("Merge Sort:", merge_sort(arr.copy()))
    
    # Heap Sort
    print("Heap Sort:", heap_sort(arr.copy()))
    
    # Counting Sort (works with non-negative integers)
    print("Counting Sort:", counting_sort(arr.copy()))
    
    # Radix Sort (works with non-negative integers)
    print("Radix Sort:", radix_sort(arr.copy()))