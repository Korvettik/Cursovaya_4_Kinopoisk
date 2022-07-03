import pytest
from dao.genre import GenreDAO
from dao.model.genre import Genre
from setup_db import db
from unittest.mock import MagicMock
from service.genre import GenreService

# --------------   ВАРИАНТ КАК В test_director.py НЕ РАБОТАЕТ   --------------
#
# # Шаг 5. Создаем фикстуру с моком для GenreDAO.
# @pytest.fixture()
# def genre_dao():
#     genre_dao = GenreDAO(db.session)
#
#     jonh = Genre(id=1, name='jonh')
#     kate = Genre(id=2, name='kate')
#     max = Genre(id=3, name='max')
#
#     genre_dao.get_one = MagicMock(return_value=jonh)
#     genre_dao.get_all = MagicMock(return_value=[jonh, kate, max])
#     genre_dao.create = MagicMock(return_value=Genre(id=3))
#     genre_dao.delete = MagicMock()
#     genre_dao.update = MagicMock()
#     return genre_dao
#
# # Шаг 6. Пишем класс с тестами для GenreService.
# class TestGenreService:
#     @pytest.fixture(autouse=True)
#     def genre_service(self, genre_dao):
#         self.genre_dao = GenreService(dao=genre_dao)
#
#     def test_get_one(self):
#         genre = self.genre_service.get_one(1)
#         assert genre != None
#         assert genre.id != None
#
#     def test_get_all(self):
#         genres = self.genre_service.get_all()
#         assert len(genres) > 0
#
#     def test_create(self):
#         genre_d = {
#             "name": "Ivan"
#         }
#         genre = self.genre_service.create(genre_d)
#         assert genre.id != None
#
#     def test_delete(self):
#         self.genre_service.delete(1)
#
#     def test_update(self):
#         genre_d = {
#             "id": 3,
#             "name": "Ivan"
#         }
#         self.genre_service.update(genre_d)





# --------------   ВАРИАНТ КАК В test_movie.py РАБОТАЕТ   --------------

# Шаг 5. Создаем фикстуру с моком для  GenreDAO.
@pytest.fixture()
def genres_dao():
    dao = GenreDAO(None)

    dao.get_one = MagicMock()
    dao.get_all = MagicMock()
    dao.create = MagicMock()
    dao.delete = MagicMock()
    dao.update = MagicMock()
    return dao

# Шаг 6. Пишем класс с тестами для GenreService.
class TestGenreService:
    @pytest.fixture(autouse=True)
    def genres_service(self, genres_dao):
        self.genres_service = GenreService(dao=genres_dao)

    parameters = (
        (
            1,
            {
                'id': 1,
                'name': 'Noname',
            }
        ),
        (
            2,
            {
                'id': 2,
                'name': 'TestName',
            }
        )

                )

    @pytest.mark.parametrize("mig, genre", parameters)
    def test_get_one(self, mig, genre):
        self.genres_service.dao.get_one.return_value = genre
        assert self.genres_service.get_one(mig) == genre, "BAD"


    parameters = (
        (
            [
                {
                    'id': 1,
                    'name': 'Noname',
                },
                {
                    'id': 2,
                    'name': 'TestName',
                }
            ]
        ),
    )
    @pytest.mark.parametrize('genres', parameters)
    def test_get_all(self, genres):
        self.genres_service.dao.get_all.return_value = genres
        assert self.genres_service.get_all() == genres, 'BAD'



    parameters = (
        (
            {
                'id': 1,
                'name': 'Noname',
            }
        ),
        (
            {
                'id': 2,
                'name': 'TestName',
            }
        )

                )

    @pytest.mark.parametrize("genre", parameters)
    def test_create(self, genre):
        self.genres_service.dao.create.return_value = genre
        assert self.genres_service.create(genre) == genre, "BAD"

    parameters = (
        (
            {
                'id': 1,
                'name': 'Noname',
            },
            {
                'id': 1,
                'name': 'TestName',
            }
        )

                )

    @pytest.mark.parametrize("genre_original, genre_new", parameters)
    def test_update(self, genre_original, genre_new):
        self.genres_service.dao.update.return_value = genre_new
        assert self.genres_service.update(genre_new) == genre_new
        self.genres_service.dao.update.assert_called_once_with(genre_new)


    def test_delete(self):
        self.genres_service.delete(1)
        self.genres_service.dao.delete.assert_called_once_with(1)