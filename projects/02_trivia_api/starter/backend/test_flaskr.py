import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_category(self):
        res = self.client.get('/categories')
        self.assertEqual(res.status_code, 200)
        expected_response = {
            "categories": [
                {
                "id": 1,
                "type": "Science"
                },
                {
                "id": 2,
                "type": "Art"
                },
                {
                "id": 3,
                "type": "Geography"
                },
                {
                "id": 4,
                "type": "History"
                },
                {
                "id": 5,
                "type": "Entertainment"
                },
                {
                "id": 6,
                "type": "Sports"
                }
            ],
            "success": True
        }
        body = json.loads(res.data)
        self.assertEqual(body, expected_response)

    def test_get_questions(self):
        """
        Test the GET /questions API endpoint which is expected to be paginated at 10 questions / page
        """
        expected_response = {
            "questions": [
                {
                    "answer": "Maya Angelou",
                    "category": 4,
                    "difficulty": 2,
                    "id": 5,
                    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                }
            ],
            "success": True
        }
        res = self.client.get('/questions?page=1')
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertEqual(body["questions"][0]["answer"], expected_response["questions"][0]["answer"])
        self.assertEqual(body["questions"][0]["category"], expected_response["questions"][0]["category"])
        self.assertEqual(body["questions"][0]["id"], expected_response["questions"][0]["id"])
        self.assertEqual(body["questions"][0]["question"], expected_response["questions"][0]["question"])

    def test_get_question_by_category(self):
        """
        Test the GET /category<int:category_id>/questions which gets all the questions for a particular category        
        """
        expected_response = {
            "questions": [
                {
                    "answer": "Maya Angelou",
                    "category": 4,
                    "difficulty": 2,
                    "id": 5,
                    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                }
            ],
            "success": True
        }
        res = self.client.get('/categories/4/questions')
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertEqual(body["questions"][0]["answer"], expected_response["questions"][0]["answer"])
        self.assertEqual(body["questions"][0]["category"], expected_response["questions"][0]["category"])
        self.assertEqual(body["questions"][0]["id"], expected_response["questions"][0]["id"])
        self.assertEqual(body["questions"][0]["question"], expected_response["questions"][0]["question"])

    def test_add_delete_question(self):
        """ 
        Test the DELETE /questions/<question_id> endpoint which deletes a specific question
        """
        expected_response = {
            "message": "Deleted",
            "success": True
        }
        question = {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = self.client.post('/questions', data=json.dumps(question), headers=headers)
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertEqual(body["success"], True)
        self.assertEqual(body["message"], "Added") 
        new_id = body.get("id")
        res = self.client.delete(f'/questions/{new_id}')
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertEqual(body, expected_response) 


    def test_add_question_fail(self):
        """ 
        Test the error condition DELETE /questions/<question_id> endpoint which deletes a specific question
        """        
        question = {            
            "category": 4,
            "difficulty": 2,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = self.client.post('/questions', data=json.dumps(question), headers=headers)
        self.assertEqual(res.status_code, 400)
        body = json.loads(res.data)
        self.assertEqual(body["success"], False)
        self.assertEqual(body["message"], "Bad Request, please check the body and the url") 
        

    def test_delete_question_fail(self):
        res = self.client.delete(f'/questions')
        self.assertEqual(res.status_code, 405)
        body = json.loads(res.data)
        self.assertEqual(body["message"], "Method not allowed. Please check documentation") 

    def test_search(self):
        """
        Test the POST /search endpoint that searches all the questions for the substring provided
        """
        expected_response = {
            "questions": [
                {
                    "answer": "Maya Angelou",
                    "category": 4,
                    "difficulty": 2,
                    "id": 5,
                    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                }
            ],
            "success": True
        }
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            "searchTerm": "auto"
        }
        res = self.client.post('/search', data=json.dumps(body), headers=headers)
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertEqual(body["questions"][0]["answer"], expected_response["questions"][0]["answer"])
        self.assertEqual(body["questions"][0]["category"], expected_response["questions"][0]["category"])
        self.assertEqual(body["questions"][0]["id"], expected_response["questions"][0]["id"])
        self.assertEqual(body["questions"][0]["question"], expected_response["questions"][0]["question"]) 

    def test_fail_search(self):        
        body = {}
        headers = {
            'Content-Type': 'application/json'
        }
        res = self.client.post('/search', data=json.dumps(body), headers=headers)
        # missing body with the "searchTerm"
        self.assertEqual(res.status_code, 400)
        res = self.client.get('/search', data=json.dumps(body), headers=headers)
        # method not allowed
        self.assertEqual(res.status_code, 405)

    def test_play(self):
        """
        Test the POST /quizzes endpoint that plays the trivia game
        it should give a random question and should not repeat questions
        """
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            "previous_questions": [],
            "quiz_category": {
                "type": "Sports",
                "id": '6',
            }
        }
        res = self.client.post('/quizzes', data=json.dumps(body), headers=headers)
        self.assertEqual(res.status_code, 200)


    def test_fail_play(self):
        headers = {
            'Content-Type': 'application/json'
        }
        # missing quiz body in the test
        body = {
            "previous_questions": []
        }
        res = self.client.post('/quizzes', data=json.dumps(body), headers=headers)
        # bad request 
        self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()