# Capstone Project

## Motivation

Capstone is the final project for the Udacity FullStack Nanodegree.
This project consists of a database, API, Authorisation using Auth0 and deployed to Heroku

The Casting Agency models a company that is responsible for creating, updating, removing and viewing movies and actors. I was assigned Executive Producer within the company and are creating a system to simplify and streamline the process.

## Getting Started

### Heroku Link

[Capestone project link](https://hollywood22.herokuapp.com/)

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I worked within a virtual environment whenever using Python for projects. Instructions for set up can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup

While Postgres is running, restore a database using the file hollywood.psql as provided and run:

```bash
createdb hollywood
psql hollywood < hollywood.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --reload
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Postman Collection

I have uploaded a postman collection called `Capstone.postman_collection.json` in this repo containing the endpoints and jwt's required to test the endpoints.

## Auth0 setup

Set up an [Auth0](https://manage.auth0.com/) account 
Create an application and an API

### Environment variable to set up locally

```bash
export AUTH0_DOMAIN="{your-auth0-domain-here}.auth0.com"
export ALGORITHMS="RS256"
export API_AUDIENCE="{your-api-identifier}"
```

### Roles & Permissions in API to setup in Auth0

Casting Assistant 
- Can view actors and movies 
    - Permissions: (GET '/movies', GET '/actors', GET '/movies/<id>', GET '/actors/<id>')

Casting Director
- Can view actors and movies 
    - Permissions: (GET '/movies', GET '/actors', GET '/movies/<id>', GET '/actors/<id>')
- Add or delete an actor from the database 
    - Permissions: (DELETE '/movies/<id>', DELETE '/actors/<id>', POST '/movies', POST '/actors')
- Modify actors or movies 
    - Permissions: (PATCH '/movies', PATCH '/actors')

### Obtain and set JWT tokens

Enter your detailsi n the following link and require your JWT's

```bash
https://{{auth0-domain-here}}/authorize?audience={{api-identifier}}&response_type=token&client_id={{client-id}}&redirect_uri={{callback_uri}}
```

### Set up the environment variables in the `setup.sh` file by running:

```bash
source ./setup.sh
```

## Testing
To run the tests, run
```
dropdb hollywood_test
createdb hollywood_test
psql hollywood_test < hollywood.psql
python3 test_app.py
```

## Endpoints 

- GET '/movies'
- GET '/actors'
- GET '/movies/<id>'
- GET '/actors/<id>'
- DELETE '/movies/<id>'
- DELETE '/actors/<id>'
- POST '/movies'
- POST '/actors'
- PATCH '/movies'
- PATCH '/actors'


GET '/movies'

- Fetches a tupel with dictionaries of movies
- Request Arguments: None
- Returns: A tupel with objects with key:value pairs for id, release_date and title of the movie.

```
[
    {
        "id": 10,
        "release_date": "Tue, 04 Jul 2019 13:23:55 GMT",
        "title": "Joker"
    },
    {
        "id": 12,
        "release_date": "Wed, 04 Jul 2001 13:23:55 GMT",
        "title": "The Lord of the Rings"
    },
    ... ]

```

GET '/actors'

- Fetches a tupel with dictionaries of actors
- Request Arguments: None
- Returns: A tupel with objects with key:value pairs for id, age, gender and name of the actor.

```
[
    {
        "age": 50,
        "gender": "female",
        "id": 3,
        "name": "Sharon Stone"
    },
    {
        "age": 25,
        "gender": "female",
        "id": 4,
        "name": "Emma Stone"
    },
... ]

```

GET '/movies/<id>'

- Fetches a dictionary of the movie  
- Request Arguments: the movie's ID appended to the URL
- Returns: A tupel with an object with key:value pairs of the movie

```
/movies/10 will return:
{
    "id": 10,
    "release_date": "Tue, 04 Jul 2019 13:23:55 GMT",
    "title": "Joker"
}

```
GET '/actors/<id>'

- Fetches a dictionaries of the actor
- Request Arguments: the actor's ID appended to the URL
- Returns: An object with key:value pairs of the actor

```
/actors/3 will return:
{
    "age": 50,
    "gender": "female",
    "id": 3,
    "name": "Sharon Stone"
}

```

DELETE '/movies/<id>'

- Deletes a specified movie
- Request Arguments: the movie's ID appended to the URL
- Returns: An object with key:value pairs for the id, title and release_date of the deleted movie

```
/movies/15  will return:
{
    "id": 15,
    "release_date": "Wed, 04 Jul 2001 13:23:55 GMT",
    "title": "the hobbit 4"
}

```
DELETE '/actors/<id>'

- Deletes a specified actor
- Request Arguments: the actor's ID appended to the URL
- Returns: An object with key:value pairs for the id, name, gender and age of the deleted actor

```
/actors/4  will return:
{
    "age": 11,
    "gender": "female",
    "id": 4,
    "name": "Emma Stone"
}

```


POST '/movies'

- Creates a new movie
- Request Arguments: an object with the new title and release_date of the new movie
- Returns: An object with key:value pairs for the newly created movie

```
{
    "id": 15,
    "release_date": "Wed, 04 Jul 2001 13:23:55 GMT",
    "title": "the hobbit 4"
}
```

POST '/actors'

- Creates a new actor
- Request Arguments: an object with the new age, gender and name of the new actor
- Returns: An object with key:value pairs for the newly created actor

```
{
    "age": 5,
    "gender": "female",
    "id": 10,
    "name": "Emily Blunt"
}
```

PATCH '/movies/<id>'

- Updates the movie according to the request body
- Request Arguments: the movie's ID appended to the URL
- Returns: An object with key:value pairs for the updated movie

```
/movies/9 will return:
{
    "id": 9,
    "release_date": "Fri, 04 Jul 1988 13:23:55 GMT",
    "title": "Batman Returns"
}
```

PATCH '/actors/<id>'

- Updates the actor according to the request body
- Request Arguments: the actor's ID appended to the URL
- Returns: An object with key:value pairs for the updated actor

```
/actors/9 will return:
{
    "age": 30,
    "gender": "F",
    "id": 3,
    "name": "Zooey Deschanel"
}
```



