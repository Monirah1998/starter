import imp
import os
import flask 
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import Actors, Movies, setup_db
from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  setup_db(app)
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  # EndPoints 
     
# ROUTES
 # TWO GET REQUEST
  @app.route('/')
  def index():
    return jsonify({
        'success': True,
        'message':'hello'}) 

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies():
   try:
    return jsonify({
       "success": True,
       "movies" : [Movies.short() for movie in Movies.query.all()]
    }) ,200
   except:
       return jsonify({
            'success': False,
            'error': "ERROR !!! "
       })

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors():
   try:
    return jsonify({
       "success": True,
       "actors" : [Actors.short() for actor in Actors.query.all()]
    }) ,200
   except:
       return jsonify({
            'success': False,
            'error': "ERROR !!! "
       })

       # ONE POST REQUEST
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movies():
   try:
    data = request.get_json()
    movie_title = data['movie_title']
    dateMovie = data['title']
    add_movie= Movies(title=movie_title , date=dateMovie)
    add_movie.insert()
    return jsonify({
        'success': True,
        'drinks': [add_movie.long()]
    })
   except:
    return jsonify({
            'success': False,
            'error': "ERROR !!! "
       })

    # ONE PATCH request

  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update(movie,id):
   try:
    check_id = Movies.query.get(id)
    if check_id is None:
        abort(404)
    data = request.get_json()
    if 'movie_title' in data: movie.title = data['movie_title']

    if 'date' in data: movie.date = data['date']

    movie.update()

    return jsonify({
        'success': True,
        'movies': [movie.long()]
    })

   except:
      return jsonify({
            'success': False,
            'error': "ERROR !!! "
       })
# ONE DELETE request
  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete(movie, id):
    check_id = Movies.query.get(id)
    if check_id is None:
        abort(404)
    check_id.delete()
    
    return jsonify({
        'success': True,
        'delete': movie.id
    })

     
# Error Handling



  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422



  @app.errorhandler(404)
  def notfound(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404

  @app.errorhandler(AuthError)
  def auth_error(e):
    return jsonify({
        "success": False,
        "error": e.status_code,
        "message": e.error['description']
    }), e.status_code
  return app


  

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)