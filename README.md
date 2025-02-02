# Number Classification API

## Description
This API takes a number and returns interesting mathematical properties about it, such as whether the number is prime, perfect, or Armstrong. Additionally, the API provides a fun fact about the number.

## API Endpoint
- **GET /api/classify-number?number={number}**

### Query Parameters:
- `number`: An integer to classify.

### Response Example (200 OK):
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}

For an invalid request, we get this response:
{
    "number": "abc",
    "error": true,
}