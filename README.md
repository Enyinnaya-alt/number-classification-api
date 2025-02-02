# Number Classification API

This API classifies numbers based on certain mathematical properties.

## Endpoints

- `GET /api/classify-number?number={number}`

## Response Example

```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}

##for an invalid request we get this resonse
{
    "number": "abc",
    "error": true,

}
