// Arrays, Multi Arrays, Accessing, Looping, Length and Copying
import java.util.*;  // (Optional) If you plan to extend functionality with collections.

public class LearningPrograms {
    public static int sum( int[][] array) {
        int sum = 0;
        for(int[] a : array){
            for(int b : a){
                sum+=b;
            }
        }
        return sum;
    }
    public static double average( int[][] array) {
        return sum (array)/(array.length*array[0].length);
    }
    
    public static int[][] copyArray(int[][] original) {
        int[][] copied = new int[original.length][];
        for(int i=0; i<original.length;++i){
            copied[i]=new int [original[0].length];
            for(int j=0; j<original[i].length;++j){
                copied[i][j]=original[i][j];
            }
            System.arraycopy(original[i], 0, copied[i], 0, original[i].length); //Using arraycopy 
        }
        return copied;
    }
    
    public static void main(String[] args) {
        int[][] array = {{1,2},{3,4},{5,6},{7,8}};
        System.out.println(sum(array)); // true
        System.out.println(average(array)); // false
        System.out.println(copyArray(array));
    }
}

// System.arraycopy(Object src, int srcPos,Object dest, int destPos, int length) - > length how many to copy

// Problem-1: Sorted Array 
class MySolution {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        int[] buf = new int[m+n];
        int first = 0;
        int second = 0;
        if (nums2.length>0){
            for(int i=0;i<m+n;i++){
                if(second<nums2.length){
                    if(nums1.length>i+(nums2.length-second)) 
                        buf[i]=(nums1[first]<=nums2[second]) ? (nums1[first++]):(nums2[second++]);
                    else 
                        buf[i]=nums2[second++];
                }
                else 
                    buf[i]=nums1[first++];
            }
        System.arraycopy(buf,0,nums1,0,m+n);
        }  
    }
}
class Solution1 {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        for(int i=0;i<n;i++){
            nums1[m+i]=nums2[i];
        }
        Arrays.sort(nums1);
    }
}
class BestSolution {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        int i = m-1;
        int j = n-1;
        int k = m+n-1;
        while(j>=0){
            if (i>=0 && nums1[i]>nums2[j])
                nums1[k--]=nums1[i--];
            else nums1[k--]=nums2[j--];
        }
    }
}

// Problem-2 Remove Element in Array
class Solution {
    public int removeElement(int[] nums, int val) {
        int k=0;
        for(int i=0; i<nums.length;i++)
        {   
            if(nums[i]!=val)
                nums[k++]=nums[i];
        }
        return k;
    }
}

// Problem-3 Remove Duplicates from Sorted Array
class Solution {
    public int removeDuplicates(int[] nums) {
       int j=1;
       for(int i=1;i<nums.length;i++){
            if(nums[i]!=nums[j-1]){
                nums[j++]=nums[i];
            }
       }
       return j;
    }
}

// Problem-4 Remove II Duplicates from Sorted Array
class Solution {
    public int removeDuplicates(int[] nums) {
       int j=2;
       for(int i=2;i<nums.length;i++){
            if(nums[i]!=nums[j-2]){
                nums[j++]=nums[i];
            }
       }
       return j;
    }
}

// Problem 5 - Majority in Array/ Voting Problem
class Solution {
    public int majorityElement(int[] nums) {
        Arrays.sort(nums);
        return nums[nums.length/2];
    }
}
//Using More Voting approach
class Solution {
    public int majorityElement(int[] nums) {
        int count = 0;
        int candidate = 0;
        
        for (int num : nums) {
            if (count == 0) {
                candidate = num;
            }
            count = (num == candidate) ? ++count : --count;
        }
        return candidate;
    }
}

//Problem-6 Rotate array by K steps O(n),O(1)
class BestSolution {
    public void rotate(int[] nums, int k) {
        k %= nums.length;

        reverse(nums, 0, nums.length - 1);
        reverse(nums, 0, k - 1);
        reverse(nums, k, nums.length - 1);
    }

    private void reverse(int[] nums, int left, int right) {
        while (left < right) {
            int temp = nums[left];
            nums[left] = nums[right];
            nums[right] = temp;
            left++;
            right--;
        }
    }    
}


// #Given an array of integers nums and an integer target, return indices of the two numbers 
// #such that they add up to target.
class BestSolution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> numMap = new HashMap<>();
        int n = nums.length;

        for (int i = 0; i < n; i++) {
            int complement = target - nums[i];
            if (numMap.containsKey(complement)) {
                return new int[]{numMap.get(complement), i};
            }
            numMap.put(nums[i], i);
        }

        return new int[]{}; // No solution found
    }
}

// Roman Letters
class Solution {
    public int romanToInt(String s) {
        int res = 0;
        Map<Character, Integer> roman = new HashMap<>();
        roman.put('I', 1);
        roman.put('V', 5);
        roman.put('X', 10);
        roman.put('L', 50);
        roman.put('C', 100);
        roman.put('D', 500);
        roman.put('M', 1000);

        for (int i = 0; i < s.length() - 1; i++) {
            if (roman.get(s.charAt(i)) < roman.get(s.charAt(i + 1))) {
                res -= roman.get(s.charAt(i));
            } else {
                res += roman.get(s.charAt(i));
            }
        }

        return res + roman.get(s.charAt(s.length() - 1));        
    }
}

// Longest Common Prefix
class Solution {
    public String longestCommonPrefix(String[] strs) {
        StringBuilder ans = new StringBuilder();
        Arrays.sort(v);
        String first = v[0];
        String last = v[v.length-1];
        for (int i=0; i<Math.min(first.length(), last.length()); i++) {
            if (first.charAt(i) != last.charAt(i)) {
                return ans.toString();
            }
            ans.append(first.charAt(i));
        }
        return ans.toString();
    }
}

//////// BACKTRACKING ///////////


// Letter Combinations of a Phone Number
// Using backtracking to create all possible combinations
// This is based on Python solution. Other might be differnt a bit.

// Initialize an empty list res to store the generated combinations.

// Check if the digits string is empty. If it is, return an empty list since there are no digits to process.

// Create a dictionary digit_to_letters that maps each digit from '2' to '9' to the corresponding letters on a phone keypad.

// Define a recursive function backtrack(idx, comb) that takes two parameters:

// idx: The current index of the digit being processed in the digits string.
// comb: The current combination being formed by appending letters.
// Inside the backtrack function:

// Check if idx is equal to the length of the digits string. If it is, it means a valid combination has been formed, so append the current comb to the res list.
// If not, iterate through each letter corresponding to the digit at digits[idx] using the digit_to_letters dictionary.
// For each letter, recursively call backtrack with idx + 1 to process the next digit and comb + letter to add the current letter to the combination.
// Initialize the res list.

// Start the initial call to backtrack with idx set to 0 and an empty string as comb. This will start the process of generating combinations.

// After the recursive calls have been made, return the res list containing all the generated combinations.

class LetterCombinations {
    public List<String> letterCombinations(String digits) {
        List<String> res = new ArrayList<>();
        
        if (digits == null || digits.length() == 0) {
            return res;
        }
        
        Map<Character, String> digitToLetters = new HashMap<>();
        digitToLetters.put('2', "abc");
        digitToLetters.put('3', "def");
        digitToLetters.put('4', "ghi");
        digitToLetters.put('5', "jkl");
        digitToLetters.put('6', "mno");
        digitToLetters.put('7', "pqrs");
        digitToLetters.put('8', "tuv");
        digitToLetters.put('9', "wxyz");
        
        backtrack(digits, 0, new StringBuilder(), res, digitToLetters);
        
        return res;        
    }

    private void backtrack(String digits, int idx, StringBuilder comb, List<String> res, Map<Character, String> digitToLetters) {
        if (idx == digits.length()) {
            res.add(comb.toString());
            return;
        }
        
        String letters = digitToLetters.get(digits.charAt(idx));
        for (char letter : letters.toCharArray()) {
            comb.append(letter);
            backtrack(digits, idx + 1, comb, res, digitToLetters);
            comb.deleteCharAt(comb.length() - 1);
        }
    }    
}

// Generate Parentheses
// Intuition

// Increase number of open parentheses until we reach n at first

// Initialization: We initialize an empty list res to store the valid combinations.
// Define the dfs function. def dfs(openP, closeP, s): This is a helper function that uses depth-first search (DFS) to explore all possible combinations.
// Base Case: If the number of open and close parentheses are equal and the total length of the string is 2 * n, it means we have a valid combination.
// Recursive Case: Adding an Open Parenthesis
// Recursive Case: Adding a Close Parenthesis
// Initial Call to dfs
// Return the Result
class GenerateParentheses {
    public List<String> generateParenthesis(int n) {
        List<String> res = new ArrayList<>();

        dfs(0, 0, "", n, res);

        return res;        
    }

    private void dfs(int openP, int closeP, String s, int n, List<String> res) {
        if (openP == closeP && openP + closeP == n * 2) {
            res.add(s);
            return;
        }

        if (openP < n) {
            dfs(openP + 1, closeP, s + "(", n, res);
        }

        if (closeP < openP) {
            dfs(openP, closeP + 1, s + ")", n, res);
        }
    }    
}