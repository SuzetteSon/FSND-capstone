
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

import app
from models import setup_db, Movies, Actors

DIRECTOR_JWT = os.environ.get('DIRECTOR_JWT')
ASSISTANT_JWT = os.environ.get('ASSISTANT_JWT')
ASSISTANT_JWT = os.environ.get('ASSISTANT_JWT')

class HollywoodTestCase(unittest.TestCase):
    """This class represents the hollywood test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.director_token = DIRECTOR_JWT
        self.assistant_token = ASSISTANT_JWT
        self.app = app.create_app()
        self.client = self.app.test_client
        self.database_name = "hollywood_test"

        self.database_path = "postgres://{}/{}".format(
           'localhost:5432', self.database_name)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies_director(self):
        """Test get movies success"""
        response = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_get_movies_unauth(self):
        """Test RBAC - no token"""
        response = self.client().get('/movies')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], {
            'code': 'authorization_header_missing', 
            'description': 'Authorization header is expected.'
        })

    def test_get_movies_assistant(self):
        """Test get movies success"""
        response = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    # def test_get_movies_unauth_assistant(self):
    #     """Test RBAC for the Casting Assistant - no token"""
    #     response = self.client().get('/movies')

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(data['message'], {
    #         'code': 'authorization_header_missing', 
    #         'description': 'Authorization header is expected.'
    #     })

    def test_get_actors(self):
        """Test get actors success"""
        response = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    def test_get_actors_unauth_director(self):
        """Test RBAC for the Casting Director - no token"""
        response = self.client().get('/actors')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], {
            'code': 'authorization_header_missing', 
            'description': 'Authorization header is expected.'
        })

    def test_get_actors_unauth(self):
        """Test RBAC - no token"""
        response = self.client().get('/actors')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], {
            'code': 'authorization_header_missing', 
            'description': 'Authorization header is expected.'
        })

    # def test_get_movies_unauth_assistant(self):
    #     """Test RBAC for the Casting Assistant - no token"""
    #     response = self.client().get('/movies')

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(data['message'], {
    #         'code': 'authorization_header_missing', 
    #         'description': 'Authorization header is expected.'
    #     })

    def test_get_specific_movie(self):
        """Test get specific movie success"""

        response = self.client().get('/movies/13',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_get_specific_movie_invalid_id_provided(self):
        """Test get specific movie failure - invalid id provided"""

        response = self.client().get('/movies/1000',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No matching request found.')

    def test_get_specific_actor(self):
        """Test get specific actor success"""

        response = self.client().get('/actors/6',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_get_specific_actor_invalid_id_provided(self):
        """Test get specific actor failure - invalid id provided"""

        response = self.client().get('/actors/1000',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No matching request found.')

    def test_post_movie(self):
        """Test add movie success"""

        response = self.client().post('/movies',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}, 
            json={'title': "Joker",
                'release_date': '2019-07-04*13:23:55'}
        )

        data = json.loads(response.data)

        movie = Movies.query.filter(Movies.title == "Joker").one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(movie.title, "Joker")

    def test_post_movie_failed (self):
        """Test add movie failed - missing information provided"""

        response = self.client().post('/movies',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}, 
            json={}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to process the contained instructions.')
        

    def test_post_actor(self):
        """Test add actor success"""

        response = self.client().post('/actors',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}, 
            json={'name': "Blake Lively",
                'age': '35', 'gender': 'female'}
        )

        data = json.loads(response.data)

        actor = Actors.query.filter(Actors.name == "Blake Lively").one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(actor.name, "Blake Lively")

    def test_post_movies_assistant(self):
        """Test RBAC Assistant - not authorised"""
        response = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)}, 
            json={'title': "The Hobbit",
                'release_date': '2019-07-04*13:23:55'}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['message'], {
            'code': 'unauthorized',
            'description': 'Permission not found.'
        })
    
    def test_post_actor_failed (self):
        """Test add actor failed - missing information provided"""

        response = self.client().post('/actors',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}, 
            json={}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to process the contained instructions.')

    def test_patch_movie(self):
        """Test add movie success"""

        response = self.client().patch('/movies/13',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}, 
            json={'title': "The Hobbit II",
                'release_date': '2019-07-04*13:23:55'}
        )

        data = json.loads(response.data)

        movie = Movies.query.filter(Movies.title == "The Hobbit II").one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(movie.title, "The Hobbit II")

    def test_patch_movie_failed (self):
        """Test add movie failed - error in request provided"""

        response = self.client().patch('/movies/3',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}, 
            json={'the title': "The Hobbit II"}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to process the contained instructions.')

    def test_patch_actor(self):
        """Test add actor success"""

        response = self.client().patch('/actors/7',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}, 
            json={'name': "Blake Lively-Reynolds",
                'age': '35', 'gender': 'female'}
        )

        data = json.loads(response.data)

        actor = Actors.query.filter(Actors.name == "Blake Lively-Reynolds").one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(actor.name, "Blake Lively-Reynolds")

    def test_patch_actors_assistant(self):
        """Test RBAC Assistant - not authorised"""
        response = self.client().patch('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)}, 
            json={'name': "Blake Lively",
                'age': '35', 'gender': 'female'}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['message'], {
            'code': 'unauthorized',
            'description': 'Permission not found.'
        })

    def test_patch_actor_failed (self):
        """Test add actor failed - error in request provided"""

        response = self.client().patch('/actors/5',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}, 
            json={'names': "Ben Jeremy Afleck"}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to process the contained instructions.')

    def test_delete_movie(self):
        """Test delete movie success"""

        response = self.client().delete('/movies/12', 
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_movie'])

    def test_delete_movie_invalid_id_provided(self):
        """Test delete movie failure - invalid id provided"""

        response = self.client().get('/movies/1000',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No matching request found.')

    def test_delete_actor(self):
        """Test delete actor success"""

        response = self.client().delete('/actors/5', 
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_actor'])
    
    def test_delete_actor_invalid_id_provided(self):
        """Test delete actor failure - invalid id provided"""

        response = self.client().get('/actors/1000',  
            headers={
                'Authorization': "Bearer {}".format(self.director_token)}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No matching request found.')


if __name__ == "__main__":
    unittest.main()