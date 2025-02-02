from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# Predefined facts for specific numbers
PREDEFINED_FACTS = {
    371: "371 is an Armstrong number because 3³ + 7³ + 1³ = 371",
}

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(abs(n) ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number."""
    return sum(i for i in range(1, abs(n)) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(abs(n))]
    return sum(d ** len(digits) for d in digits) == abs(n)

def get_fun_fact(number: int) -> str:
    """Get a fun fact from NumbersAPI or predefined facts."""
    if number in PREDEFINED_FACTS:
        return PREDEFINED_FACTS[number]
    
    url = f"http://numbersapi.com/{number}"
    response = requests.get(url)
    
    if "missing a fact" in response.text.lower():
        return f"Sorry, no fun fact found for {number}."
    
    return response.text

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
        number = float(number)  # Allow floating-point numbers
        if number.is_integer():
            number = int(number)  # Convert float to int if it's a whole number
        else:
            raise ValueError("Floating-point numbers are not supported.")
    except ValueError:
        raise HTTPException(status_code=400, detail="Input should be a valid integer.")

    digit_sum = sum(int(digit) for digit in str(abs(number)))
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
        "fun_fact": get_fun_fact(number),
    }