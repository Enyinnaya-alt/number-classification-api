
from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

def is_prime(n):
    if n < 2 or not n.is_integer():  # Prime numbers must be whole and ≥ 2
        return False
    n = int(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if not n.is_integer():  # Only whole numbers can be perfect
        return False
    n = int(n)
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    if not n.is_integer():  # Armstrong numbers are whole numbers
        return False
    digits = [int(d) for d in str(abs(int(n)))]  # Convert to integer before checking
    return sum(d**len(digits) for d in digits) == int(n)

@app.route('/')
def home():
    return "Welcome to the Number Classification API! Use /api/classify-number?number=<your_number> to classify a number."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    # Ensure number is included in the error response
    try:
        number = float(number)  # Accept both integers and floats
    except (ValueError, TypeError):
        return jsonify({"number": number, "error": "Invalid input. Please provide a valid number."}), 400

    properties = []
    
    # Classify the number based on various properties
    classifications = {
        "prime": is_prime(number),
        "perfect": is_perfect(number),
        "armstrong": is_armstrong(number),
        "even": number % 2 == 0,
        "odd": number % 2 != 0
    }

    # Dynamically construct the properties list based on classifications
    for prop, is_valid in classifications.items():
        if is_valid:
            properties.append(prop)

    digit_sum = sum(int(digit) for digit in str(abs(int(number))))

    # Generate the fun fact dynamically for Armstrong numbers
    fun_fact = None
    if classifications["armstrong"]:
        fun_fact = f"{int(number)} is an Armstrong number because " + " + ".join(
            [f"{d}^{len(str(int(number)))}" for d in str(abs(int(number)))]
        ) + f" = {int(number)}"

    # Build the response dynamically
    response = {
        "number": number,
        "is_prime": classifications["prime"],
        "is_perfect": classifications["perfect"],
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact if fun_fact else "No fact found."
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)