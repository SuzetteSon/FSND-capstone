import os
import json
import dateutil.parser
import babel
from flask import Flask, request, Response, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.dialects.postgresql import ARRAY
from flask_cors import CORS
from models import setup_db, Movies, Actors
from auth import AuthError, requires_auth

'''
App Config.
'''


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object('config')
    setup_db(app)
    CORS(app, resources={"/": {"origins": "*"}})
    db = SQLAlchemy(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Default port:
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, debug=True)

    '''
    Filters.
    '''

    def format_datetime(value, format='medium'):
        date = dateutil.parser.parse(value)
        if format == 'full':
            format = "EEEE MMMM, d, y 'at' h:mma"
        elif format == 'medium':
            format = "EE MM, dd, y h:mma"
        return babel.dates.format_datetime(date, format)

    app.jinja_env.filters['datetime'] = format_datetime

    @app.route('/')
    def index():
        return "Hello world! Refer to the README of this project to continue."

    '''
    GET /movies
    '''
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_all_movies(jwt):
        try:
            movies = Movies.query.all()
            movie_data = []
            for movie in movies:
                movie_data.append({
                    "id": movie.id,
                    "title": movie.title,
                    "release_date": movie.release_date
                    })
        except BaseException:
            abort(401)
        return jsonify({
            'success': True,
            'movies': movie_data
            }), 200

    '''
    GET /actors
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_all_actors(jwt):
        try:
            actors = Actors.query.all()
            actor_data = []
            for actor in actors:
                actor_data.append({
                    "id": actor.id,
                    "name": actor.name,
                    "age": actor.age,
                    "gender": actor.gender
                    })
        except BaseException:
            abort(401)
        return jsonify({
            'success': True,
            'actors': actor_data
            }), 200

    '''
    GET /movies/id
    '''
    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movies_id')
    def get_movie(jwt, id):
        try:
            movie = Movies.query.get(id)
            movie_data = []

            movie_data.append({
                "id": movie.id,
                "title": movie.title,
                "release_date": movie.release_date
                })
        except BaseException:
            abort(404)
        return jsonify({
            'success': True,
            'movie': movie_data[0]
            }), 200

    '''
    GET /actors/id
    '''
    @app.route('/actors/<int:id>', methods=['GET'])
    @requires_auth('get:actors_id')
    def get_actor(jwt, id):
        try:
            actor = Actors.query.get(id)
            actor_data = []

            actor_data.append({
                "id": actor.id,
                "name": actor.name,
                "age": actor.age,
                "gender": actor.gender
            })
        except BaseException:
            abort(404)
        return jsonify({
            'success': True,
            'actor': actor_data[0]
            }), 200

    '''
    DELETE /movies/id
    '''
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def remove_movie(jwt, id):
        try:
            movie = Movies.query.get(id)
            movie.delete()

            movie_data = []
            movie_data.append({
                "id": movie.id,
                "title": movie.title,
                "release_date": movie.release_date
            })
        except BaseException:
            abort(404)
        return jsonify({
            'success': True,
            'deleted_movie': movie_data[0]
            }), 200

    '''
    DELETE /actors/id
    '''
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def remove_actor(jwt, id):
        try:
            actor = Actors.query.filter(Actors.id == id).one_or_none()
            actor.delete()
            actor_data = []
            actor_data.append({
                "id": actor.id,
                "name": actor.name,
                "age": actor.age,
                "gender": actor.gender
            })
        except BaseException:
            abort(404)
        return jsonify({
            'success': True,
            'deleted_actor': actor_data[0]
            }), 200

    '''
    POST /movies
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movies(jwt):
        body = request.get_json()
        new_title = body.get('title')
        new_release_date = body.get('release_date')

        if ((new_title is None) or (new_release_date is None)):
            abort(422)

        try:
            movie = Movies(title=new_title, release_date=new_release_date)
            movie.insert()
            movie_data = []

            movie_data.append({
                "id": movie.id,
                "title": movie.title,
                "release_date": movie.release_date
                })
        except BaseException:
            abort(404)
        return jsonify({
            'success': True,
            'created_movie': movie_data[0]
            }), 200

    '''
    POST /actors
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actors(jwt):
        body = request.get_json()
        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')

        if ((new_name is None) or (new_age is None) or (new_gender is None)):
            abort(422)

        try:
            actor = Actors()
            actor.name = body['name']
            actor.gender = body['gender']
            actor.age = body['age']
            actor.insert()

            actor_data = []

            actor_data.append({
                "id": actor.id,
                "name": actor.name,
                "age": actor.age,
                "gender": actor.gender
            })
        except BaseException:
            abort(404)
        return jsonify({
            'success': True,
            'created_actor': actor_data[0]
            }), 200

    '''
    PATCH /movies/id
    '''
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies(jwt, id):

        body = request.get_json()
        new_title = body.get('title')
        new_release_date = body.get('release_date')

        if ((new_title is None) or (new_release_date is None)):
            abort(422)

        try:

            movie = Movies.query.get(id)

            if new_title:
                movie.title = new_title

            if new_release_date:
                movie.release_date = new_release_date

            movie.update()

            movie_data = []

            movie_data.append({
                "id": movie.id,
                "title": movie.title,
                "release_date": movie.release_date
                })

        except BaseException:
            abort(404)
        return jsonify({
            'success': True,
            'updated_movie': movie_data[0]
            }), 200

    '''
    PATCH /actors/id
    '''
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(jwt, id):
        body = request.get_json()
        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')

        if ((new_name is None) or (new_age is None) or (new_gender is None)):
            abort(422)

        try:
            actor = Actors.query.get(id)
            actor.name = new_name
            actor.age = new_age
            actor.gender = new_gender
            actor.update()

            actor_data = []

            actor_data.append({
                "id": actor.id,
                "name": actor.name,
                "age": actor.age,
                "gender": actor.gender
            })

        except BaseException:
            abort(404)
        return jsonify({
            'success': True,
            'updated_actor': actor_data[0]
            }), 200

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'message': error.error
            }), error.status_code

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Request not understood due to malformed syntax.'
            }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Request unauthorized.'
            }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'No matching request found.'
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unable to process the contained instructions.'
            }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Unable to complete the request.'
            }), 500

    return app
