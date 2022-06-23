from dao.auth import AuthDAO
from required import generate_password, secret, algo
from flask import abort
import datetime
import calendar
import jwt


class AuthService:
    def __init__(self, dao: AuthDAO):
        self.dao = dao

    def rewrite_hash_pass(self, data):
        passwd = data['password']
        data['password'] = generate_password(str(passwd))  # меняем значение поля password на хэш
        return self.dao.post_new_user(data)

    def cheking(self, req_json):
        email = req_json.get("email", None)
        password = req_json.get("password", None)

        if None in [email, password]:
            abort(400)

        # делаем запрос в бд и получаем строку-кортеж (если она есть и соответствует выше), (имя, хэш-пароль, роль)
        user = self.dao.get_user(email)
        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        # если все ок, делаем новый хэш из полученного пароля (с проверкой) - проверка пароля
        user_password = generate_password(password)  # делаем хэш из полученного пароля
        if user.password != user_password:  # сравниваем хэш-пароль пользователя из бд с хэш-паролем введенным
            return {"error": "Неверные учётные данные"}, 401

        # если все ок, формируем данные пользователя (спецсловарь) из базы данных (далее пригодится)
        # в реальности это просто будет информация для работы с бд, она будет храниться в шифрованном виде
        # пароль сюда в чистом виде лучше не сувать

        data = {
            "email": user.email
        }

        # генерим access_token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        # print(access_token)

        # генерим refresh_token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        # print(refresh_token)

        # формируем результат
        tokens = {"access_token": access_token.decode('utf-8'), "refresh_token": refresh_token.decode('utf-8')}
        print(tokens)
        # return jsonify(tokens), 201
        return tokens, 201

    def tokens_regeneration(self, req_json):
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)

        # пробуем расшифровать рефреш токен
        try:
            data = jwt.decode(jwt=refresh_token, key=secret, algorithms=[algo])
        except Exception as e:
            abort(401)

        # из запроса получаем email
        email = data.get("email")

        # получаем модель-строку из базы-данных по email
        user = self.dao.get_user(email)

        # формируем данные пользователя (спецсловарь) из базы данных (далее пригодится)

        data = {
            "email": user.email
        }
        # генерим access_token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)

        # генерим refresh_token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)

        # формируем результат
        tokens = {"access_token": access_token.decode('utf-8'), "refresh_token": refresh_token.decode('utf-8')}

        return tokens, 201
