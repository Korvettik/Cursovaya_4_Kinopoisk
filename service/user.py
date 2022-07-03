from dao.model.users import UserSchema
from dao.user import UserDAO
from required import generate_password, secret, algo
from flask import request
import jwt

user_schema = UserSchema()


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def show_info(self):
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        data = jwt.decode(jwt=token, key=secret, algorithms=[algo])
        email = data.get("email")
        user = self.dao.find_user(email)
        return user_schema.dump(user), 200

    def change_info(self, change_user):
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        data = jwt.decode(jwt=token, key=secret, algorithms=[algo])
        email = data.get("email")
        user = self.dao.find_user(email)

        print(change_user["surname"])

        if change_user.get("name"):  # ----- только при GET не выдает ошибки
            user.name = change_user["name"]
        if change_user.get("surname"):
            user.surname = change_user["surname"]
        if change_user.get("favorite_genre"):
            user.favorite_genre = change_user["favorite_genre"]

        self.dao.rewrite_user(user)
        return "", 204

    def change_passwords(self, passwords):
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        data = jwt.decode(jwt=token, key=secret, algorithms=[algo])
        email = data.get("email")
        user = self.dao.find_user(email)

        old_password = user.password

        password1 = passwords['old_password']
        password2 = passwords['new_password']

        if old_password == generate_password(password1):
            print(f'{old_password}   {generate_password(password1)}')

            user.password = generate_password(password2)
            self.dao.rewrite_user(user)
            return "", 204
        else:
            return "введен неверный старый пароль", 401
