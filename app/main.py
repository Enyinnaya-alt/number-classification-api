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
                "error": True,
                "message": "Input should be a valid integer."
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
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": get_fun_fact(parsed_number),
        }
    )