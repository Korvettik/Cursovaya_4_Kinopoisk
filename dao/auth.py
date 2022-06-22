from dao.model.users import User

class AuthDAO:
    def __init__(self, session):
        self.session = session

    def post_new_user(self, data):
        new_user = User(**data)
        with self.session.begin():
            self.session.add(new_user)
        return "", 204

    def get_user(self, email):
        user = self.session.query(User).filter(User.email == email).first()
        return user
