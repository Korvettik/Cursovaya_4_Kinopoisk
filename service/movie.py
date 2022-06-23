from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self, status, page):  # --- далее реализуем логику работы
        if page is None and status is None:
            return self.dao.get_all()
        elif page is not None and status == 'new':
            return self.dao.get_all_with_stat_and_pag(page)
        elif page is not None:
            return self.dao.get_all_with_pag(page)
        elif status == 'new':
            return self.dao.get_all_with_stat()