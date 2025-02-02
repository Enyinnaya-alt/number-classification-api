from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# Predefined facts for specific numbers
PREDEFINED_FACTS = {
    371: "371 is an Armstrong number because 3³ + 7³ + 1³ = 371",
    42: "42 is the Answer to the Ultimate Question of Life, the Universe, and Everything.",
}

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

def get_fun_fact(number: float) -> str:
    """Get a fun fact from NumbersAPI or predefined facts."""
    if number in PREDEFINED_FACTS:
        return PREDEFINED_FACTS[number]
    
    url = f"http://numbersapi.com/{number}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        if "missing a fact" in response.text.lower():
            return f"Sorry, no fun fact found for {number}."
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Sorry, unable to retrieve a fun fact for {number} due to an error: {str(e)}"

@app.exception_handler(HTTPException)
async def invalid_number_exception_handler(request: Request, exc: HTTPException):
    """Return a 400 response for invalid number input."""
    return JSONResponse(
        status_code=400,
        content={
            "number": request.query_params.get("number", "unknown"),
            "error": True,
            "message": exc.detail
        },
    )

@app.get("/api/classify-number", response_class=JSONResponse)
def classify_number(number: str = Query(..., description="The number to classify")):
    """Classify the number and return mathematical properties."""
    
    try:
        parsed_number = float(number)  # Convert input to float
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={
                "number": number,
                "error": True,
                "message": "Input should be a valid number."
            }
        )
    
    # Handle invalid inputs (infinity)
    if parsed_number == float("inf") or parsed_number == float("-inf"):
        return JSONResponse(
            status_code=400,
            content={
                "number": number,
                "error": True,
                "message": "Input should be a valid finite number."
            }
        )
    
    # Properties to calculate
    properties = []
    digit_sum = sum(int(digit) for digit in str(abs(int(parsed_number))) if digit.isdigit())  # Only integer part

    # Check if the number is even or odd (only for integers)
    if parsed_number.is_integer():
        if int(parsed_number) % 2 == 0:
            properties.append("even")
        else:
            properties.append("odd")

        # Check for prime, perfect, and Armstrong (only for positive integers)
        if parsed_number > 0:
            if is_prime(int(parsed_number)):
                properties.append("prime")
            if is_perfect(int(parsed_number)):
                properties.append("perfect")
            if is_armstrong(int(parsed_number)):
                properties.append("armstrong")

    return JSONResponse(
        status_code=200,
        content={
            "number": parsed_number,
            "is_integer": parsed_number.is_integer(),
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": get_fun_fact(parsed_number),
        }
    )