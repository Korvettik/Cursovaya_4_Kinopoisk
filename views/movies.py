from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from implemented import movie_service

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        status = request.args.get('status')  # --- получение необходимости сортировки
        page = request.args.get('page')  # --- получение пагинации
        movies = movie_service.get_all(status, page)
        return MovieSchema(many=True).dump(movies), 200


@movie_ns.route('/<int:bid>/')
class MovieView(Resource):
    def get(self, bid):
        movie = movie_service.get_one(bid)
        return MovieSchema(many=True).dump(movie), 200
