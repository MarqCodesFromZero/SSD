
# Secure Software Development - Unit 6 Seminar Answers

This document provides answers to the questions from the Unit 6 Seminar activities.

---

## **Question 1: Running `styleLint.py`**

### **What happens when the code is run?**
When running `styleLint.py`, the code raises an `IndentationError` because the `if` and `else` statements are not properly indented. Python relies on indentation to define code blocks, and the lack of proper indentation causes the code to fail.

### **Can you modify this code for a more favorable outcome?**
Yes, the code can be modified to fix the indentation issue.

### **What amendments have you made to the code?**
The corrected version of `styleLint.py` is as follows:

```python
def factorial(n):
    """Return factorial of n."""
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
```
### **What amendments have you made to the code?**
The corrected version of `styleLint.py` is as follows:
The amendments include:
- Properly indenting the if and else blocks.
- Ensuring the return statements are aligned with their respective blocks.
  
## Question 2: Running pylint on pylintTest.py **

### **Review each of the code errors returned.**
Running pylint on pylintTest.py returns several errors and warnings, such as:
1. Missing docstrings for the module and functions.
2. Use of raw_input, which is Python 2 syntax and invalid in Python
3. Inconsistent indentation, especially in the nested if statements.
4. Unused imports (e.g., string module).
5. Logical errors, such as the if choice == "decode" block being incorrectly nested inside the if choice == "encode" block.

### **Can you correct each of the errors identified by pylint?**
The corrected version as follows:

```python
"""Module to encode or decode text using a Caesar cipher."""

import string

def caesar_cipher(choice, word, shift=3):
    """Encode or decode text using a Caesar cipher."""
    letters = string.ascii_letters + string.punctuation + string.digits
    encoded = ''
    
    if choice == "encode":
        for letter in word:
            if letter == ' ':
                encoded += ' '
            else:
                x = letters.index(letter) + shift
                encoded += letters[x]
    elif choice == "decode":
        for letter in word:
            if letter == ' ':
                encoded += ' '
            else:
                x = letters.index(letter) - shift
                encoded += letters[x]
    
    return encoded

if __name__ == "__main__":
    choice = input("Would you like to encode or decode? ")
    word = input("Please enter text: ")
    print(caesar_cipher(choice, word))
```
### **What amendments have you made to the code?**
The amendments include:
- Added docstrings for the module and function.
- Replaced raw_input with input for Python 3 compatibility.
- Fixed the indentation and logical structure of the if blocks.
- Removed unnecessary nesting of the decode block inside the encode block.
- Encapsulated the logic in a function for better reusability.

## Question 3: Running `flake8` on `pylintTest.py` and `metricTest.py` **

### **Review the errors returned. In what way does this error message differ from the error message returned by `pylint`?**
`flake8` focuses on style and syntax issues, such as:
- Missing whitespace around operators.
- Line length violations.
- Unused imports.
- Syntax errors.

Unlike `pylint`, `flake8` does not provide detailed analysis of code structure or logic but is stricter about PEP 8 compliance.

### **Run `flake8` on `metricTest.py`. Can you correct each of the errors returned by `flake8`?**
The corrected version of `metricTest.py` is as follows:

```python
"""Module to demonstrate various functions and classes for testing static checkers."""

import random

def fn(x, y):
    """A function which performs a sum."""
    return x + y

def find_optimal_route_to_my_office_from_home(start_time, expected_time,
                                              favorite_route='SBS1K',
                                              favorite_option='bus'):
    """Determine the optimal route to the office based on time."""
    d = (expected_time - start_time).total_seconds() / 60.0

    if d <= 30:
        return 'car'
    if 30 < d < 45:
        return ('car', 'metro')
    if d > 45:
        if d < 60:
            return ('bus:335E', 'bus:connector')
        if d > 80:
            return random.choice(('bus:330', 'bus:331', ':'.join((favorite_option, favorite_route))))
        if d > 90:
            return ':'.join((favorite_option, favorite_route))
    return None

class C:
    """A class which does almost nothing."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def f(self):
        """Placeholder function."""
        pass

    def g(self, x, y):
        """Perform a conditional sum."""
        if self.x > x:
            return self.x + self.y
        if x > self.x:
            return x + self.y
        return None

class D(C):
    """D class."""

    def __init__(self, x):
        super().__init__(x, 0)

    def f(self, x, y):
        """Perform a conditional subtraction or addition."""
        if x > y:
            return x - y
        return x + y

    def g(self, y):
        """Perform a conditional sum or subtraction."""
        if self.x > y:
            return self.x + y
        return y - self.x
```

Amendments made:
- Added docstrings for all functions and classes.
- Fixed line length issues by breaking long lines.
- Corrected syntax errors (e.g., – to -).
- Added proper spacing around operators and after commas.

## Question 4: Running `mccabe` on `sums.py` and `sums2.py` **

### **Run `mccabe` on `sums.py`. What is the result?**
The result for `sums.py` shows a cyclomatic complexity of 1, as there is only one function (`test_sum`) with no conditional logic.

### **Run `mccabe` on `sums2.py`. What is the result?**
The result for `sums2.py` shows a cyclomatic complexity of 2, as there are two functions (`test_sum` and `test_sum_tuple`), each contributing to the complexity.

### **What are the contributors to the cyclomatic complexity in each piece of code?**
- In `sums.py`, the complexity is solely from the `test_sum` function.
- In `sums2.py`, the complexity comes from both `test_sum` and `test_sum_tuple`. Each function adds a decision point (the assert statement), increasing the complexity.
