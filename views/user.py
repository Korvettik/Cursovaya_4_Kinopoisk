from flask_restx import Resource, Namespace
from implemented import user_service
from flask import request
from required import auth_required

user_ns = Namespace('user')


@user_ns.route('/')
class UserView(Resource):
    @auth_required
    def get(self):
        print('готовлюсь user_service.show_info()')
        return user_service.show_info()

    @auth_required
    def patch(self):
        change_user = request.get_json()
        print(change_user)
        return user_service.change_info(change_user), 204


@user_ns.route('/password')
class UserPasswd(Resource):
    @auth_required
    def put(self):
        passwords = request.get_json()
        return user_service.change_passwords(passwords)
