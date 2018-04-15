from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api, reqparse
import urllib
import json
import codecs

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('expression')


HISTORY = dict()

class CalculatorHistory(Resource):
	def get(self): #Returns all previously evaluated expressions
		return HISTORY, 200

api.add_resource(CalculatorHistory, '/calc/history')

class Calculator(Resource):
	def post(self): #posts an expression to history and returns the result.
		args = parser.parse_args()
		expression = args["expression"]
		result = eval(expression)
		if result == int(result): #1.0 ==> 1 and 1.5 ==> 1.5
			result = int(result)
		HISTORY[expression] = str(result)
		return {"result": HISTORY[expression]}, 201 #Returns the result of the expression.

api.add_resource(Calculator, '/calc')

if __name__ == "__main__":
	app.run(debug=True)