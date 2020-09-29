import os
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.dialects.postgresql import ARRAY
from flask_cors import CORS
from models import setup_db, Movies, Actors


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


# def create_app(test_config=None):
  # create and configure the app
app = Flask(__name__)
app.config.from_object('config')
setup_db(app)
CORS(app, resources={"/": {"origins": "*"}})
db = SQLAlchemy(app)

# CORS Headers 
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


# Default port:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime



@app.route('/')
def index():
  return "hello world"

'''
GET /movies
'''
@app.route('/movies', methods=['GET'])
def get_all_movies():
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
      abort(404)   
  return jsonify({
      'success': True,
      'movies': movie_data
  }), 200

'''
GET /actors
'''
@app.route('/actors', methods=['GET'])
def get_all_actors():
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
  except:
    print('error') 
  return jsonify({
      'success': True,
      'actors': actor_data
  }), 200

'''
GET /movies/id
'''
@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
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
      'movies': movie_data
  }), 200

'''
GET /actors/id
'''
@app.route('/actors/<int:id>', methods=['GET'])
def get_actor(id):
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
      'actors': actor_data
  }), 200

'''
DELETE /movies/id
'''
@app.route('/movies/<int:id>', methods=['DELETE'])
def remove_movie(id):
  try:
    movie = Movies.query.get(id)
    movie.delete()

  
  except BaseException:
      abort(404)   
  return jsonify({
      'success': True,
      'id': id
  }), 200

'''
DELETE /actors/id
'''
@app.route('/actors/<int:id>', methods=['DELETE'])
def remove_actor(id):
  try:
    actor = Actors.query.filter(Actors.id == id).one_or_none()
    actor.delete()

  
  except BaseException:
      abort(404)   
  return jsonify({
      'success': True,
      'id': id
  }), 200


'''
POST /movies
'''
@app.route('/movies', methods=['POST'])
def add_movies():
  body = request.get_json()
  new_title = body.get('title')
  new_release_date = body.get('release_date')
  print(body)
  try:
    movie = Movies(title=new_title, release_date=new_release_date )
    
    movie.insert()

  except BaseException:
      abort(404)   
  return jsonify({
      'success': True
  }), 200

'''
POST /actors
'''
@app.route('/actors', methods=['POST'])
def add_actors():
  body = request.get_json()
  print(body)

  try:
    actor = Actors()
    actor.name = body['name']
    actor.gender = body['gender']
    actor.age = body['age']
    
    actor.insert()

  except:
    print('error')
  return jsonify({
      'success': True
  }), 200


'''
PATCH /movies/id
'''
@app.route('/movies/<int:id>', methods=['PATCH'])
def update_movies(id):
  body = request.get_json()
  new_title = body.get('title')
  print(body)
  try:
    movie = Movies.query.get(id)
    movie.title = new_title
    
    movie.update()

  except:
    print('error')  
  return jsonify({
      'success': True
  }), 200