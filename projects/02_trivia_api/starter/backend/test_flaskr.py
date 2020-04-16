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

    def test_add_question(self):
        """
        Test the POST /questions/ endpoint which adds a new question
        """
        expected_response = {
            "id": 1,
            "message": "Added",
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
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body["success"], True)
        self.assertEqual(body["message"], "Added")
        self.new_id = body.get("id")

    def test_delete_question(self):
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
        body = json.loads(res.data)
        new_id = body.get("id") 
        res = self.client.delete(f'/questions/{new_id}')
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertEqual(body, expected_response) 




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()