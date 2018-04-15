# Task 2 a)

The file CalculatorAPI.py is a simple Calculator REST API using JSON that supports input of
mathematical expressions with the basic operations: +, -, * and /. It allows the
usage of brackets and understands operator precedence.

The API can also retrieve history (Previously queried expressions, along with the calculated answer).

The API is written in Python, utilizing the flask_restful API framework. To test the API, make sure to have Flask installed and simply
run the CalculatorAPI.py file. This starts the server, which can be easily queried using a program like Postman.

Example:
POST /calc
{ “expression”: “-1 * (2 * 6 / 3)” }
Returns:
{ “result”: “-4” }
POST /calc
{ “expression”: “-2 * (4 * 12 / 6)” }
Returns:
{ “result”: “-16” }
POST /calc
{ “expression”: “-4 * (8 * 24 / 12)” }
Returns:
{ “result”: “-64” }


Example
Get /calc/history
Returns:
{
    "-1 * (2 * 6 / 3)": "-4",
    "-2 * (4 * 12 / 6)": "-16",
    "-4 * (8 * 24 / 12)": "-64"
}
