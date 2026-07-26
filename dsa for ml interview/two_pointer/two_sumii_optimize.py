
'''
LeetCode 167: Two Sum II – Input Array Is Sorted
Key Observations
The array is sorted in non-decreasing order.
We need to return the 1-indexed positions of the two numbers.
Exactly one valid answer exists.
We cannot use the same element twice.
Intuition (Two Pointers)

Since the array is sorted:

If the current sum is too small, move the left pointer right to increase the sum.
If the current sum is too large, move the right pointer left to decrease the sum.

This works because moving pointers in a sorted array changes the sum predictably.

Algorithm
Initialize:
left = 0
right = len(numbers) - 1
While left < right:
Compute current_sum = numbers[left] + numbers[right]
If current_sum == target:
Return [left + 1, right + 1] (convert to 1-indexed)
If current_sum < target:
Move left += 1
Otherwise:
Move right -= 1
Why +1?

Python uses 0-based indexing, but the problem expects 1-based indexing.
Time complexity: O(n)
Space complexity: O(1)
'''

arr = [1, 2, 3, 4, 5]

#task : return two number whose sum is equal to 6

def find(numbers, target):
    left = 0
    right = len(numbers) - 1

    while left<right:
        sum = numbers[left] + numbers[right] 
        if sum == target:
            return left, right
        
        elif sum < target:
            left += 1
        
        else:
            right -= 1
    
  
values = find(arr, target=3)
print(values)
