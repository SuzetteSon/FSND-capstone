import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_name = "hollywood"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

#migrate = Migrate(app, db)

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)
  db.create_all()
    

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Movies(db.Model):
  __tablename__ = 'movies'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable=False)
  release_date = db.Column(db.DateTime, nullable=False)
  
  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def __repr__(self): 
    return json.dumps(self)

class Actors(db.Model):
  __tablename__ = 'actors'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  age = db.Column(db.Integer, nullable=False)
  gender = db.Column(db.String, nullable=False)

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()
    
  def __repr__(self): 
    return json.dumps(self)

# class Show(db.Model):
#   __tablename__ = 'Show'

#   id = db.Column(db.Integer, primary_key=True)
#   artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
#   venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
#   start_time = db.Column(db.DateTime, nullable=False)

#   def __repr__(self): 
#     return f'<Show {self.id} {self.artist_id, self.venue_id}>'
