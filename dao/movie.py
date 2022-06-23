from sqlalchemy import desc
from constants import POST_PER_PAGE
from dao.model.movie import Movie


class MovieDAO:  # --- класс с функциями для работы с базой данных
    def __init__(self, session):  # --- подвязка будущего курсора, оюозначим в implemented.py  (db.session)
        self.session = session

    def get_one(self, mid):
        return self.session.query(Movie).get(mid)

    def get_all(self):
        return self.session.query(Movie).all()

    def get_all_with_stat_and_pag(self, page):
        # return self.session.query(Movie).order_by(desc(Movie.year)).paginate(int(page), POST_PER_PAGE, False).items()
        offset_page = (int(page) - 1) * POST_PER_PAGE
        return self.session.query(Movie).order_by(desc(Movie.year)).limit(POST_PER_PAGE).offset(offset_page).all()

    def get_all_with_pag(self, page):
        offset_page = (int(page) - 1) * POST_PER_PAGE
        return self.session.query(Movie).limit(POST_PER_PAGE).offset(offset_page).all()

    def get_all_with_stat(self):
        return self.session.query(Movie).order_by(desc(Movie.year)).all()
