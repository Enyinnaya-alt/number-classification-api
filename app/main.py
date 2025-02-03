from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Predefined facts for specific numbers
PREDEFINED_FACTS = {
    371: "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371",
}

def is_prime(n: int) -> bool:
    """Check if a number is prime (only applies to integers)."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(abs(n) ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number (only applies to integers)."""
    if n < 2:
        return False
    total = 1
    for i in range(2, int(abs(n) ** 0.5) + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
        if total > n:
            return False
    return total == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number (only applies to integers)."""
    digits = [int(d) for d in str(abs(n))]
    return sum(d ** len(digits) for d in digits) == abs(n)

def get_fun_fact(number: int) -> str:
    """Get a fun fact using the 'math' type from Numbers API."""
    if number in PREDEFINED_FACTS:
        return PREDEFINED_FACTS[number]
    
    url = f"http://numbersapi.com/{number}/math"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and "missing a fact" not in response.text.lower():
            return response.text
    except requests.exceptions.RequestException:
        pass
    return f"Sorry, no fun fact found for {number}."

@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    """Classify the number and return mathematical properties."""
    
    number = request.args.get("number")

    if number is None:
        return jsonify({"error": True, "number": "unknown"}), 400

    # Ensure input is a valid integer or float
    if not number.lstrip("-").replace(".", "", 1).isdigit():
        return jsonify({"error": True, "number": number, "message": "Input must be a valid number"}), 400

    number = int(float(number))  # Convert to integer
    digit_sum = sum(int(digit) for digit in str(abs(number)))  # Sum of digits

   
    properties = []

    # Check if the number is natural (positive integer)
    if number > 0 and isinstance(number, int):
        properties.append("natural")

    # Check if the number is whole (non-negative integer)
    if number >= 0 and isinstance(number, int):
        properties.append("whole")

    # Check if the number is integer
    if isinstance(number, int):
        properties.append("integer")

    # Check if the number is rational (can be expressed as a fraction)
    if isinstance(number, (int, float)):
        properties.append("rational")

    # Check if the number is even/odd
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    # Check if the number is prime
    if is_prime(number):
        properties.append("prime")

    # Check if the number is perfect
    if is_perfect(number):
        properties.append("perfect")

    # Check if the number is Armstrong
    if is_armstrong(number):
        properties.append("armstrong")

    # Handle negative numbers
    if number < 0:
        properties.append("negative")
        if "prime" in properties:
            properties.remove("prime")
        if "perfect" in properties:
            properties.remove("perfect")
        if "armstrong" in properties:
            properties.remove("armstrong")

    return jsonify({
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,  
        "digit_sum": digit_sum,
        "fun_fact": get_fun_fact(number),
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)