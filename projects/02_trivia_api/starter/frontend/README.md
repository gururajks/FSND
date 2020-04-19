# Full Stack Trivia API  Frontend

## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you stand up the backend first, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

## Required Tasks

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Request Formatting

The frontend should be fairly straightforward and disgestible. You'll primarily work within the ```components``` folder in order to edit the endpoints utilized by the components. While working on your backend request handling and response formatting, you can reference the frontend to view how it parses the responses. 

After you complete your endpoints, ensure you return to and update the frontend to make request and handle responses appropriately: 
- Correct endpoints
- Update response body handling 

## Optional: Styling

In addition, you may want to customize and style the frontend by editing the CSS in the ```stylesheets``` folder. 

## Optional: Game Play Mechanics

Currently, when a user plays the game they play up to five questions of the chosen category. If there are fewer than five questions in a category, the game will end when there are no more questions in that category. 

You can optionally update this game play to increase the number of questions or whatever other game mechanics you decide. Make sure to specify the new mechanics of the game in the README of the repo you submit so the reviewers are aware that the behavior is correct.


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
Gets all the questions that are available and is paginated. 
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

Eg: `curl -X DELETE http://localhost:3000/questions?1`

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
| Answer |  string |
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
Searches 

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

