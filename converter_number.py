# Python program to print a given number in
# words. The program handles numbers
# from 0 to 9999

# A function that prints
# given number in words

from log_managment import create_logger

logger = create_logger('{}.log'.format(__name__))


def convert_to_words(num) -> str:
    # Get number of digits
    # in given number
    l = len(num)

    # Base cases
    if l == 0:
        logger.error('Number is empty')
        return

    if l > 4:
        logger.error('Number is too big')
        return

    # The first string is not used,
    # it is to make array indexing simple
    single_digits = ["zero", "one", "two", "three",
                     "four", "five", "six", "seven",
                     "eight", "nine"]

    # The first string is not used,
    # it is to make array indexing simple
    two_digits = ["", "ten", "eleven", "twelve",
                  "thirteen", "fourteen", "fifteen",
                  "sixteen", "seventeen", "eighteen",
                  "nineteen"]

    # The first two string are not used,
    # they are to make array indexing simple
    tens_multiple = ["", "", "twenty", "thirty", "forty",
                     "fifty", "sixty", "seventy", "eighty",
                     "ninety"]

    tens_power = ["hundred", "thousand"]

    # Used for debugging purpose only
    logger.debug('Number is {}'.format(num))
    print(num, ":", end=" ")

    # For single digit number
    if l == 1:
        return single_digits[ord(num[0]) - 48]

    # Iterate while num is not '\0'
    x = 0
    while x < len(num):

        # Code path for first 2 digits
        if l >= 3:
            if ord(num[x]) - 48 != 0:
                print(single_digits[ord(num[x]) - 48],
                      end=" ")
                print(tens_power[l - 3], end=" ")
            # here len can be 3 or 4

            l -= 1

        # Code path for last 2 digits
        else:

            # Need to explicitly handle
            # 10-19. Sum of the two digits
            # is used as index of "two_digits"
            # array of strings
            if ord(num[x]) - 48 == 1:
                sum_ = (ord(num[x]) - 48 +
                        ord(num[x + 1]) - 48)
                return two_digits[sum_]

            # Need to explicitly handle 20
            elif (ord(num[x]) - 48 == 2 and
                  ord(num[x + 1]) - 48 == 0):
                return "twenty"

            # Rest of the two digit
            # numbers i.e., 21 to 99
            else:
                i = ord(num[x]) - 48
                if i > 0:
                    print(tens_multiple[i], end=" ")
                else:
                    print("", end="")
                x += 1
                if ord(num[x]) - 48 != 0:
                    return single_digits[ord(num[x]) - 48]
        x += 1
