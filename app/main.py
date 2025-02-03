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
    for i in range(2, int(abs(n) ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number (only applies to integers)."""
    return sum(i for i in range(1, abs(n)) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number (only applies to integers)."""
    digits = [int(d) for d in str(abs(n))]
    return sum(d ** len(digits) for d in digits) == abs(n)

def get_fun_fact(number: int) -> str:
    """Get a fun fact using the 'math' type from Numbers API."""
    if number in PREDEFINED_FACTS:
        return PREDEFINED_FACTS[number]
    
    url = f"http://numbersapi.com/{number}/math"
    response = requests.get(url)

    if response.status_code != 200 or "missing a fact" in response.text.lower():
        return f"Sorry, no fun fact found for {number}."
    
    return response.text

@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    """Classify the number and return mathematical properties."""
    
    number = request.args.get("number")

    if number is None:
        return jsonify({"error": True, "number": "unknown"}), 400

    # Ensure input is a valid integer (no decimals, no words)
    if not number.lstrip("-").isdigit():
        return jsonify({"error": True, "number": number}), 400

    number = int(number)  # Convert to integer
    digit_sum = sum(int(digit) for digit in str(abs(number)))  # Sum of digits
    properties = []

    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    if is_armstrong(number):
        properties.append("armstrong")

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