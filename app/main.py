from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Predefined facts for specific numbers
PREDEFINED_FACTS = {
    371: "371 is an Armstrong number because 3³ + 7³ + 1³ = 371",
}

def is_prime(n: float) -> bool:
    """Check if a number is prime (only applies to integers)."""
    if n < 2 or not n.is_integer():
        return False
    n = int(n)
    for i in range(2, int(abs(n) ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: float) -> bool:
    """Check if a number is a perfect number (only applies to integers)."""
    if not n.is_integer():
        return False
    n = int(n)
    return sum(i for i in range(1, abs(n)) if n % i == 0) == n

def is_armstrong(n: float) -> bool:
    """Check if a number is an Armstrong number (only applies to integers)."""
    if not n.is_integer():
        return False
    n = int(n)
    digits = [int(d) for d in str(abs(n))]
    return sum(d ** len(digits) for d in digits) == abs(n)

def get_fun_fact(number: float) -> str:
    """Get a fun fact from NumbersAPI or predefined facts."""
    if number in PREDEFINED_FACTS:
        return PREDEFINED_FACTS[number]
    
    url = f"http://numbersapi.com/{int(number)}"  # Convert to integer for API
    response = requests.get(url)

    if response.status_code != 200 or "missing a fact" in response.text.lower():
        return f"Sorry, no fun fact found for {number}."
    
    return response.text

@app.route("/classify", methods=["GET"])
def classify_number():
    """Classify the number and return mathematical properties."""
    
    number = request.args.get("number")

    if number is None:
        return jsonify({"error": "Number parameter is required"}), 400

    try:
        number = float(number)  # Convert input to float
    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400

    digit_sum = sum(int(digit) for digit in str(abs(int(number))))  # Only for integer part
    properties = []

    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    if is_armstrong(number):
        properties.append("armstrong")

    return jsonify({
        "number": number,
        "is_integer": number.is_integer(),
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": get_fun_fact(number),
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)