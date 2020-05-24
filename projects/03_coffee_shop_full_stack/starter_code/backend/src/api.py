import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
db = setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''

# db_drop_and_create_all()

# ROUTES
'''
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def drinks():
    all_drinks = Drink.query.all()
    formatted_drinks = [drink.short() for drink in all_drinks]
    return jsonify({
        "success": True,
        "drinks": formatted_drinks
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details():
    drinks = Drink.query.all()
    formatted_drinks = [drink.long() for drink in drinks]
    return jsonify({
        "success": True,
        "drinks": formatted_drinks
    })


'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks():
    body = request.get_json()
    try:
        new_drink = Drink(title=body['title'],
                          recipe=json.dumps(body['recipe']))
        new_drink.insert()
    except Exception as e:
        abort(500)
    return jsonify({
        "success": True,
        "drinks": new_drink.long()
    })


'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth("patch:drinks")
def update_drinks(drink_id):
    body = request.get_json()
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if not drink:
            return jsonify({
                "success": True,
                "drinks": "No drink was found"
            })
        if 'title' in body:
            drink.title = body['title']
        if 'recipe' in body:
            drink.recipe = json.dumps(body['recipe'])
        drink.update()
    except KeyError, ValueError as e:
        abort(400)
    except Exception as e:
        abort(500)
    return jsonify({
        "success": True,
        "drinks": drink.long()
    })


'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        drink.delete()
    except Exception as e:
        abort(500, "who knows what happened")
    return jsonify({
        "success": True,
        "drinks": drink_id
    })


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request, could be a bad formed json"
    }), 400


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "something went wrong"
    }), 500


@app.errorhandler(AuthError)
def not_authorized(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error.get('description')
    }), error.status_code
