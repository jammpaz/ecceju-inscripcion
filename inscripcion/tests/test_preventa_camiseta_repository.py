import unittest
import uuid
from app import create_app, db
from domain.models import PreventaCamiseta
from app.repositories import PreventaCamisetaRepository

class PreventaCamisetaRepositoryIntTestCase(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.preventa_camiseta_repository = PreventaCamisetaRepository(db.session)


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_should_find_all(self):
        preventa_1 = PreventaCamiseta()
        preventa_2 = PreventaCamiseta(id = uuid.uuid1())
        self.preventa_camiseta_repository.add(preventa_1)
        self.preventa_camiseta_repository.add(preventa_2)

        response = self.preventa_camiseta_repository.find_all()

        self.assertEqual(
                [preventa_1.id, preventa_2.id],
                list(map(lambda i: i.id, response))
                )

    def test_should_return_empty_list_at_finding_all(self):
        response = self.preventa_camiseta_repository.find_all()

        self.assertEqual([], response)
