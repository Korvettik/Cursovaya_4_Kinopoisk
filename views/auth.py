from flask import request
from flask_restx import Resource, Namespace
from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/register/')
class AuthView_reg(Resource):
    def post(self):
        data = request.get_json()
        post_new_user = auth_service.rewrite_hash_pass(data)
        return post_new_user


@auth_ns.route('/login/')
class AuthView_log(Resource):
    def post(self):
        # функция проверки пользователя, что такой есть
        req_json = request.get_json()
        return auth_service.cheking(req_json)

    def put(self):
        # проверка наличия рефреш токена в теле запроса
        req_json = request.get_json()
        return auth_service.tokens_regeneration(req_json)
