
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

import app
from models import setup_db, Movies, Actors


class HollywoodTestCase(unittest.TestCase):
    """This class represents the hollywood test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxMWUZDZGdXQkl2bFQ4NHZmUmNfLSJ9.eyJpc3MiOiJodHRwczovL2Z1bGxzdGFja3VkYWNpdHkuZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTExNjY5MTYyMDA1ODAxNjEyMDE5IiwiYXVkIjpbImhvbGx5d29vZCIsImh0dHBzOi8vZnVsbHN0YWNrdWRhY2l0eS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjAxOTg3Mzk1LCJleHAiOjE2MDIwNzM3OTUsImF6cCI6IldqM3FETWdaMGlOcUg0ZmNZaXFlWDFxVEhqcEJmU3R6Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDphY3RvcnNfaWQiLCJnZXQ6bW92aWVzIiwiZ2V0Om1vdmllc19pZCIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.F941jsuKFsb96-MfNaQ1X0JQoD7Z5-cZn8tAz4_VhLaRiYgFTJwl4cxxmF7UMI6CGdjwAF2AHPRajn2JsEYWnUag-bqMOesJsD3QAkRwspYMbtigORAzgXrHsMEFMmLxH1t4htasCkgaZ1AgMk_1kpPUdYGiqaO7x_c6wXpWdGREOZDTN8m__Biw9HrTMvbFNYuCfoUT33LG6cSGqv1jA0pk5tOsDnFJb8Nrh_FGFTr3SIGMbTP7iuF6A6Y1bSBvA766Ffa6zyC-YvD6OuBtYEZ2nvAq-vyzzwoOhZ9-hEm24FlV8tvvd7VfpKGGteqXxDPlXbEQ3PTOrKACc6GuDQ"
        self.assistant_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxMWUZDZGdXQkl2bFQ4NHZmUmNfLSJ9.eyJpc3MiOiJodHRwczovL2Z1bGxzdGFja3VkYWNpdHkuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNGRmYjFmNTkzNTgwMDA2NzU1MTE4ZiIsImF1ZCI6ImhvbGx5d29vZCIsImlhdCI6MTYwMTk5MjM2MCwiZXhwIjoxNjAyMDc4NzU4LCJhenAiOiJXajNxRE1nWjBpTnFINGZjWWlxZVgxcVRIanBCZlN0eiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDphY3RvcnNfaWQiLCJnZXQ6bW92aWVzIiwiZ2V0Om1vdmllc19pZCJdfQ.q5Yt99gblIec9meY51gspTkQT03gJRydMGiBdQ5UpZzf2yD799o_cfsGnf_GETK414Y93clGAilLbxiIx_lBoHgnPKz4688siUNV2mc1iTK1_yWeEUYjLMZZAGOTa5EA_iGz2blbFFgEak08MH_UtkJ0EvH2ZB_P312UWbPsYZTq3jVnoydMoR24KKNqao-zHpvfJPXYlK4Tz8FqNTKttUI1Qnit4rVLRxO58LFiNnDmgYF70MsZFzq5jAiz89EcR_unMRp_6IsMPVVfhkll3KkC3hcUcDU5olDBxqSWdwydjuXTRW-8rA4M84P7s5YJn9zRbLPhmAdn0wl5k9uM9w"
        self.app = app.create_app()
        self.client = self.app.test_client
        self.database_name = "hollywood_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
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

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()