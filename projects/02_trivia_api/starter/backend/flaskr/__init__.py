import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = setup_db(app)    
    CORS(app)
    
    @app.after_request
    def after_request_response(response):
        response.headers.add('Access-Control-Allow-Headers', 'Authorization,Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
        return response
    
    def _get_all_categories():
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]
        return formatted_categories
    
    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        formatted_categories = _get_all_categories()
        return jsonify({
            "categories": formatted_categories,
            "success" : True
        })

    @app.route('/questions')
    def get_all_questions():
        questions = Question.query.all()
        formatted_categories = _get_all_categories()
        page = int(request.args.get('page'))
        start = (page - 1) * 10
        end = start + 10
        formatted_questions = [question.format() for question in questions]
        return jsonify({
            "questions": formatted_questions[start: end],
            "total_questions": len(formatted_questions),
            "categories": formatted_categories,
            "current_category": "Sports",
            "success": True
        }) 


    @app.route('/questions/<int:question_id>', methods=['Delete'])
    def delete_question(question_id):
        try:
            Question.query.filter_by(id=question_id).delete()
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.close()
            abort(500)
        finally:
            db.session.close()
            
        return jsonify({
            "message": "Deleted",
            "success": True
        })

    
    @app.route('/questions', methods=['POST'])
    def create_new_question():
        id = None
        try:
            body = request.get_json()
            question = Question(question=body["question"],
                                difficulty=body["difficulty"],
                                answer=body["answer"],
                                category=body["category"])
            db.session.add(question)
            db.session.commit()
            id = question.id
        except KeyError as e:
            db.session.close()
            abort(400)
        except Exception as e:
            db.session.rollback()
            db.session.close()
            abort(500)
        db.session.close()
        return jsonify({
            "id": id,
            "message" : "Added",
            "success": True
        })
        
    @app.route('/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        search_term = "%{}%".format(body["searchTerm"])
        questions = Question.query.filter(Question.question.ilike(search_term)).all()
        formatted_questions = [question.format() for question in questions]
        return jsonify({
            "questions": formatted_questions,
            "total_questions": len(formatted_questions),
            "current_category": "Sports"
        })
    
    @app.route('/categories/<int:category_id>/questions')
    def get_question_by_category(category_id):
        questions = Question.query.filter_by(category=category_id).all()
        formatted_questions = [question.format() for question in questions]
        formatted_categories = _get_all_categories()
        return jsonify({
            "questions": formatted_questions,
            "totalQuestions": len(formatted_questions),
            "currentCategory": category_id,
            "success": True
        }) 


    @app.route('/quizzes', methods=['POST'])
    def play():
        try:
            body = request.get_json()
            if body["quiz_category"]["id"]==0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(category=body["quiz_category"]["id"]).all()
            previous_questions = body["previous_questions"]
            total_questions_in_category = len(questions)
            random_question_id = None
            while True:
                if len(previous_questions) == total_questions_in_category:
                    break
                random_question_id = random.randint(0, total_questions_in_category - 1)
                if questions[random_question_id].id not in previous_questions:
                    break
            
            if random_question_id is not None:
                return jsonify({
                    "question": questions[random_question_id].format()
                })
            return jsonify({})
        except KeyError as e:
            print(e)
            abort(400)
        
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request, please check the body and the url"
        }), 400 

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resouce not Found!"
        }), 404

    @app.errorhandler(422)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Processing error!"
        }), 422

    return app

    