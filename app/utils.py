def classify_number(number: int):
    if number % 2 == 0:
        classification = "Even"
        fact = "Even numbers are divisible by 2."
    else:
        classification = "Odd"
        fact = "Odd numbers are not divisible by 2."

    if number > 1 and all(number % i != 0 for i in range(2, int(number ** 0.5) + 1)):
        classification += " & Prime"
        fact += " Also, prime numbers have only two factors: 1 and themselves."

    return classification, fact
