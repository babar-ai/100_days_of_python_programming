
'''
problem : Two Sum II  (brute force approach)


You're tasked with figuring out the pair of elements where arr[p] + arr[q] add up to a certain number. (To try this problem out, check the Two Sum and Sorted Two Sum problems here.)

The brute force solution is to compare each element with every other number, but that's a time complexity of O(n²). We can do better!

'''

arr = [1, 2, 3, 4, 5]

#task : return two number whose sum is equal to 6

def find(numbers, target):
    for i, i_value in enumerate(numbers, start=1):              #start from 1 because of problem statement 1-based indexing
        for j, j_value in enumerate(numbers[i:], start=i+1): 
            if  i_value + j_value == target:
                return i,j

values = find(arr, target=3)
print(values)



