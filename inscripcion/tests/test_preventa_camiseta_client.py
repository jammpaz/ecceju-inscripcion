import unittest
import uuid
from flask import current_app
from app import create_app, db, feature
from app.repositories import PreventaCamisetaRepository

class PreventaCamisetaIntTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies = True)
        self.preventa_camiseta_repository = PreventaCamisetaRepository(db.session)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_new_preventa_camiseta(self):
        response = self.client.get("/preventa/new")

        self.assertEqual(response.status_code, 200)

        self._assert_static_text('Nombres completos', response)
        self._assert_static_text('Localidad', response)
        self._assert_static_text('Color', response)
        self._assert_static_text('Talla', response)
        self._assert_static_text('Cantidad', response)
        self._assert_static_text('Fecha de depósito', response)
        self._assert_static_text('Número de depósito', response)
        self._assert_static_text('Cédula', response)

    def test_create_preventa_camiseta(self):
        data = {
                'nombres_completos': 'Conny Riera',
                'localidad': 'Quito',
                'color': 'blanco',
                'talla': '34',
                'cantidad': 2,
                'fecha_deposito': '2018-09-01',
                'numero_deposito': 'ABCD-0001',
                'cedula': '0000000001'
                }

        response = self.client.post(
                '/preventa/new',
                content_type = 'multipart/form-data',
                buffered = True,
                data = data)

        preventas = self.preventa_camiseta_repository.find_all()
        self.assertTrue(len(preventas) == 1)
        self.assertEqual(response.status_code, 302)


    def _assert_static_text(self, static_text, response):
        self.assertTrue(static_text in response.get_data(as_text = True))
