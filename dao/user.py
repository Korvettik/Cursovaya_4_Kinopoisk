from dao.model.users import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def find_user(self, email):
        select = self.session.query(User).filter(User.email == email).one()
        return select

    def rewrite_user(self, user):
        self.session.add(user)
        self.session.commit()
        return "", 204
