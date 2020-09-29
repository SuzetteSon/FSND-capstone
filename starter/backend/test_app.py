
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors


class HollywoodTestCase(unittest.TestCase):
    """This class represents the hollywood test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "hollywood"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'title': "Happy Gilmore",
            'release date': '2010'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        """Test get movies success"""

        response = self.client().get('/movies')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    # def test_get_paginated_questions(self):
    #     """Test get paginated questions success"""

    #     response = self.client().get('/questions')

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(len(data['questions']))
    #     self.assertTrue(data['categories'])

    # def test_404_get_paginated_questions_beyond_valid_page(self):
    #     """Test get paginated questions failure"""

    #     response = self.client().get('/questions?page=1000')

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'No matching request found.')

    # def test_get_categories(self):
    #     """Test get categories success"""

    #     response = self.client().get('/categories')

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['categories'])

    # def test_post_question(self):
    #     """Test add question success"""

    #     response = self.client().post('/questions', json={'question': "Who is the prime minister of Sweden?",
    #     'answer': 'Stephan Luwren', 'difficulty': 5, 'category': 2})

    #     data = json.loads(response.data)

    #     question = Question.query.filter(Question.question == "Who is the prime minister of Sweden?").one_or_none()

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(len(data['questions']))
    #     self.assertTrue(data['categories'])
    #     self.assertEqual(question.format()['question'], "Who is the prime minister of Sweden?")
    #     self.assertTrue(data['categories'])


    # def test_400_post_question_failed (self):
    #     """Test add question failed - missing information provided"""

    #     response = self.client().post('/questions', json={})

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Unable to process the contained instructions.')
        
    # def test_search_question (self):
    #     """Test search question success"""

    #     response = self.client().post('/questions/search', json={'searchTerm': 'Anne'})

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(len(data['questions']), 1)
    #     self.assertEqual(data['questions'][0]['id'], 4)
    #     self.assertTrue(data['total_questions'])

    # def test_404_search_question (self):
    #     """Test search question failure searchTerm not provided"""

    #     response = self.client().post('/questions/search', json={})

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'No matching request found.')
    
    # def test_delete_question(self):
    #     """Test delete question success"""

    #     response = self.client().delete('/questions/5')

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(len(data['questions']))
    #     self.assertTrue(data['categories'])

    # def test_404_delete_question_not_found(self):
    #     """Test delete question not found"""

    #     response = self.client().delete('/questions/1000')

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'No matching request found.')

    # def test_get_specific_category_questions(self):
    #     """Test get specificcategories questions success"""

    #     response = self.client().get('/categories/6/questions')

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['questions']), 2)
    #     self.assertTrue(data['total_questions'])


    # def test_get_specific_category_questions_fail(self):
    #     """Test get specific categories questions failure"""

    #     response = self.client().get('/categories/1000/questions')

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'No matching request found.')

    # def test_post_quizzes(self):
    #     """Test post quizzes success"""

    #     response = self.client().post('/quizzes', json={'quiz_category': {'type': 'Science', 'id': '1'}, 'previous_questions':  [1, 22]})

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['question'])
    #     self.assertTrue(data['previousQuestions'])

    # def test_post_quizzes_failure(self):
    #     """Test post quizzes failure"""

    #     response = self.client().post('/quizzes', json={})

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'No matching request found.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()