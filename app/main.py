from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["GET"],  # Allow only GET requests
    allow_headers=["*"],  # Allow all headers
)

def is_prime(n: int) -> bool:
    """Check if a number is prime (only applies to positive integers)."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number (only applies to positive integers)."""
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number (only applies to integers)."""
    digits = [int(d) for d in str(abs(n))]
    return sum(d ** len(digits) for d in digits) == abs(n)

def get_fun_fact(number: int) -> str:
    """Get a fun fact from NumbersAPI using the 'math' type."""
    url = f"http://numbersapi.com/{number}/math"
    try:
        response = requests.get(url)
        response.raise_for_status()
        if "missing a fact" in response.text.lower():
            return f"Sorry, no fun fact found for {number}."
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Sorry, unable to retrieve a fun fact for {number} due to an error: {str(e)}"

@app.get("/api/classify-number", response_class=JSONResponse)
def classify_number(number: str = Query(..., description="The number to classify")):
    """Classify the number and return mathematical properties."""
    
    try:
        parsed_number = int(number)  # Convert input to integer
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={
                "number": number,
                "error": True
            }
        )
    
    # Properties to calculate
    properties = []
    digit_sum = sum(int(digit) for digit in str(abs(parsed_number)))  # Sum of digits

    # Check if the number is even or odd
    if parsed_number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    # Check if the number is an Armstrong number
    if is_armstrong(parsed_number):
        properties.append("armstrong")

    return JSONResponse(
        status_code=200,
        content={
            "number": parsed_number,
            "is_prime": is_prime(parsed_number),
            "is_perfect": is_perfect(parsed_number),
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": get_fun_fact(parsed_number),
        }
    )