import random
import string


# Flips a coin 'n' number of times, records the results, and counts the number of heads and tails
def coin_flip(n):

    record = []
    heads = tails = 0

    for i in range(n):

        result = random.randint(0,1)

        if result == 0:

            record.append('Heads')
            heads += 1

        else:

            record.append('Tails')
            tails += 1

    print('Record: {}'.format(record))
    print('Number of Heads: {}'.format(heads))
    print('Number of Tails: {}'.format(tails))


# Determines whether or not the given number (positive integer) is a 'happy number'
def happy_number(n):

    while not isinstance(n, int) or n <= 0:

        n = input('Invalid entry, please enter a positive integer: ')

    def get_digits(num):

        digits = []
        num_digits = len(str(num))

        for i in range(num_digits):

            ith_digit = num // (10**i) % 10
            digits.append(ith_digit)

        return digits

    previous_numbers = []

    while True:

        curr_digits = get_digits(n)
        ss_digits = 0

        for d in curr_digits:

            ss_digits += (d**2)

        if ss_digits == 1:

            return True

        elif ss_digits in previous_numbers:

            return False

        else:

            n = ss_digits
            previous_numbers.append(n)


# Prints the first 8 happy numbers, starting from the number entered by the user
def print_happy_numbers(n):

    happy_numbers = []
    count = 0

    while count < 8:

        if happy_number(n):

            happy_numbers.append(n)
            count += 1

        n += 1

    return happy_numbers


# Recursive approach to computing the factorial of n
def r_fact(n):

    # Base case, recursion terminates
    if n == 0:

        return 1

    else:

        return n * r_fact(n-1)


# Iterative approach to computing the factorial of n
def i_fact(n):

    if n == 0:

        return 1

    else:

        factorial = n

        for i in range(1, n):

            factorial *= (n-i)

        return factorial


# Recursive approach to computing the nth Fibonacci number
def r_fib(n):

    # Base case, recursion terminates
    if n <= 2:

        return 1

    else:

        return r_fib(n-1) + r_fib(n-2)


# Iterative approach to computing the nth Fibonacci number
def i_fib(n):

    if n <= 2:

        return 1

    else:

        prev = 1
        curr = 1

        for i in range(n-2):

            next = prev + curr
            prev = curr
            curr = next

        return next


# Implements the Luhn algorithm (check sum) to determine whether or not a given credit card number is valid
def credit_card_validator(n):

    n = str(n)
    digits = []

    for digit in n:

        digits.append(int(digit))

    def check_sum(num):

        odd_digits = []
        even_digits = []

        for i, d in enumerate(num):

            if (len(num) - i) % 2 == 0:

                m = int(d) * 2

                if m >= 10:

                    m = (m // 10) + (m % 10)

                even_digits.append(m)

            else:

                odd_digits.append(int(d))

        return sum(odd_digits) + sum(even_digits)

    if check_sum(n) % 10 == 0:

        return True

    else:

        return False


# Computing the result of the collatz conjecture applied to a given positive integer n (n > 1)
def compute_collatz(n):

    while not str(n).isdigit() or int(n) <= 1:

        n = input('Invalid entry, please enter a positive integer (not including 1): ')

    num_steps = 0
    n = int(n)

    while n != 1:

        if n % 2 == 0:

            n = n // 2

        else:

            n = (n * 3) + 1

        num_steps += 1

    return num_steps


# Sorting a given array using the merge sort algorithm
def merge_sort(arr):

    if len(arr) > 1:

        mid = len(arr) // 2
        left_sub = arr[:mid]
        right_sub = arr[mid:]

        merge_sort(left_sub)
        merge_sort(right_sub)

        i = j = k = 0

        while i < len(left_sub) and j < len(right_sub):

            if left_sub[i] < right_sub[j]:

                arr[k] = left_sub[i]
                i += 1
                k += 1

            else:

                arr[k] = right_sub[j]
                j += 1
                k += 1

        while i < len(left_sub):

            arr[k] = left_sub[i]
            i += 1
            k += 1

        while j < len(right_sub):

            arr[k] = right_sub[j]
            j += 1
            k += 1

    return arr


# Sorting a given array using the bubble sort algorithm
def bubble_sort(arr):

    is_sorted = False

    while not is_sorted:

        num_swaps = 0

        for i in range(len(arr) - 1):

            if arr[i] > arr[i + 1]:

                temp = arr[i + 1]
                arr[i + 1] = arr[i]
                arr[i] = temp
                num_swaps += 1

        if num_swaps == 0:

            is_sorted = True

    return arr


# Encoding (or decoding) a given sequence using the caesar cipher with a particular key value
def caesar_cipher(instruction, sequence, key):

    while True:

        if instruction.lower() not in ['encode', 'decode']:

            instruction = input("Please enter a valid instruction: 'encode', or 'decode' ")
            continue

        elif not sequence.isalpha():

            sequence = input('Please enter a valid (alphabetical) sequence: ')
            continue

        elif not str(key).isdigit() or int(key) not in range(1, 26):

            key = input('Please enter a valid integer key between 1 and 25 (inclusive): ')
            continue

        else:

            key = int(key)
            break

    alphabet = string.ascii_lowercase

    if instruction == 'encode':

        encoded_letters = []

        for letter in sequence.lower():

            shifted_ord = ord(letter) + key

            if shifted_ord > ord('z'):

                shifted_ord -= len(alphabet)

            shifted_letter = chr(shifted_ord)
            encoded_letters.append(shifted_letter)

        return ''.join(encoded_letters)

    else:

        decoded_letters = []

        for letter in sequence.lower():

            shifted_ord = ord(letter) - key

            if shifted_ord < ord('a'):

                shifted_ord += len(alphabet)

            shifted_letter = chr(shifted_ord)
            decoded_letters.append(shifted_letter)

        return ''.join(decoded_letters)
