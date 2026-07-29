'''
Problem: LeetCode 125 - Valid Palindrome

Description:
A phrase is a palindrome if, after converting all uppercase letters into lowercase 
letters and removing all non-alphanumeric characters, it reads the same forward 
and backward. Alphanumeric characters include letters and numbers.

Given a string `s`, return `True` if it is a palindrome, or `False` otherwise.

Examples:
1. Input: s = "A man, a plan, a canal: Panama"
   Output: True
   Explanation: "amanaplanacanalpanama" is a palindrome.

2. Input: s = "race a car"
   Output: False
   Explanation: "raceacar" is not a palindrome.

3. Input: s = " "
   Output: True
   Explanation: s is an empty string "" after removing non-alphanumeric characters.
                Since an empty string reads the same forward and backward, it is a palindrome.

Key Observations & Approaches:
- Preprocessing Approach: Filter non-alphanumeric characters, lowercase them, and check `s == s[::-1]`. (O(n) time, O(n) space)
- Two Pointers Approach (Optimal): Use `left` and `right` pointers moving inwards, skipping non-alphanumeric characters using `.isalnum()`. (O(n) time, O(1) space)
'''

def is_palindrome(s: str) -> bool:
    # Write your solution here
    clean_list = [ch for ch in s.lower() if ch.isalnum()]
    clean_s = "".join(clean_list)

    left = 0
    right = len(clean_s) - 1

    while left < right :
        if clean_s[left] != clean_s[right]:
            return False
        left += 1
        right -= 1
    return True

# Test cases
print(is_palindrome("A man, a plan, a canal: Panama"))  # Expected: True
print(is_palindrome("race a car"))                      # Expected: False
print(is_palindrome(" "))                               # Expected: True
