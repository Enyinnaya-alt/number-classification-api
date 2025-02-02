from fastapi import FastAPI, Query
import requests

app = FastAPI()

# Predefined facts for specific numbers
PREDEFINED_FACTS = {
    371: "371 is an Armstrong number because 3³ + 7³ + 1³ = 371",
}

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is a perfect number."""
    return n > 0 and sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def get_fun_fact(number):
    """Get a fun fact from NumbersAPI or use predefined facts."""
    if number in PREDEFINED_FACTS:
        return PREDEFINED_FACTS[number]
    
    url = f"http://numbersapi.com/{number}"
    response = requests.get(url)
    
    if "missing a fact" in response.text.lower():
        return f"Sorry, no fun fact found for {number}."
    
    return response.text

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="The number to classify")):
    """Classify the number and return mathematical properties."""
    
    digit_sum = sum(int(digit) for digit in str(number))
    properties = []
    
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    if is_armstrong(number):
        properties.append("armstrong")
    
    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": get_fun_fact(number)
    }