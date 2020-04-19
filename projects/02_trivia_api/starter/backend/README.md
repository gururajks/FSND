# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


## API Documentation

### `GET /categories`

Gets all the categories that are available
##### Request
Eg: `curl http://localhost:3000/categories`

##### Response
```
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    }
  ],
  "success" : True
}
```

### `GET /questions`
Gets all the questions that are available and is paginated. It is restricted to 10 questions per page
Use page parameter for the page
##### Request

Parameters: `page`

Eg: `curl -v http://localhost:3000/questions?page=1`

##### Response
```
{
    "categories": [
        {
        "id": 1,
        "type": "Science"
        }
    ],
    "current_category": "Sports",
    "questions": [
        {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 21
}
```


### `DELETE /questions/<int:question_id>`

Delete a specific question given its question id

##### Request

Eg: `curl -X DELETE http://localhost:3000/questions`

##### Response
```
{
    "message": "Deleted"
    "success": True
}
```

### `POST /questions`

Create a new question with the given details as part of the body
##### Request

Required Fields:
| Fields   |      Type      |
|----------|:-------------:|
| answer |  string |
| category |    integer   |
| difficulty | integer |
| question | string |

```
{
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
}
```

##### Response
Eg:
```
{
    "id": 1,
    "message" : "Added",
    "success": True
}
```

### `POST /search`

It searches and displays all the questions that have a substring equal to the given string
##### Request

Required Fields:
| Fields   |      Type      |
|----------|:-------------:|
| searchTerm |  string |

```
{
    "searchTerm" : "country"
}
```

##### Response
Eg:
```
{
  "current_category": "Sports", 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }
  ], 
  "total_questions": 1
}

```
Errors:
400 for bad request


### `GET /categories/<int:category_id>/questions`
Get all the questions for a particular category
##### Request

Eg: `curl http://localhost:3000/categories/1/questions`

##### Response
```
{
  "currentCategory": 1, 
  "questions": [
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "totalQuestions": 1
}

```

### `POST /quizzes`

This is the trivia quiz which gives the next question for a particular category. The next question is randomized and does not repeat. 
##### Request

Provide the previous question id so that we know which questions were asked and they are not repeated. 
`quiz_category` is a category object. 

Required Fields:
| Fields   |      Type      |
|----------|:-------------:|
| previous_questions |  List |
| quiz_category |  object |
```
{
    "previous_questions":[],
    "quiz_category":{
        "type":"Science",
        "id":1
    }
}
```

##### Response
Eg:
```
{
  "question": {
    "answer": "Mona Lisa", 
    "category": 2, 
    "difficulty": 3, 
    "id": 17, 
    "question": "La Giaconda is better known as what?"
  }
}
``` 


### Errors

##### `400 - Bad Request`

Response
```
{
  "error": 400,
  "message": "Bad Request, please check the body and the url",
  "success": false
}
```

##### `500 - Server Error`

Response
```
{
    "success": False,
    "error": 500,
    "message": "Server Error"
}
```


##### `404 - Resource not found`

Response
```
{
  "error": 404,
  "message": "Resouce not Found!"
  "success": false
}
```

