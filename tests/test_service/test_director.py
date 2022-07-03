import pytest
from dao.director import DirectorDAO
from dao.model.director import Director
from setup_db import db
from unittest.mock import MagicMock
from service.director import DirectorService

# Шаг 3. Создаем фикстуру с моком для DirectorDAO.
@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)

    jonh = Director(id=1, name='jonh')
    kate = Director(id=2, name='kate')
    max = Director(id=3, name='max')

    director_dao.get_one = MagicMock(return_value=jonh)
    director_dao.get_all = MagicMock(return_value=[jonh, kate, max])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()
    return director_dao

# Шаг 4. Пишем класс с тестами для DirectorService.
class TestDirectorService:
    @pytest.fixture(autouse=True)
    def user_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director != None
        assert director.id != None

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        director_d = {
            "name": "Ivan"
        }
        director = self.director_service.create(director_d)
        assert director.id != None

    def test_delete(self):
        self.director_service.delete(1)

    def test_update(self):
        director_d = {
            "id": 3,
            "name": "Ivan"
        }
        self.director_service.update(director_d)







