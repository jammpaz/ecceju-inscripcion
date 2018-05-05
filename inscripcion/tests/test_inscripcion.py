import unittest
import uuid
from flask import current_app
from app import create_app
from domain.models import Inscripcion

class InscripcionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies = True)

    def tearDown(self):
        self.app_context.pop()

    def test_show_a_inscripcion(self):
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                monto = '150.00',
                fecha = '2018-08-01',
                comprobante_uri = 'https://s3.aws.com/comprobante.jpg')
        response = self.client.get(f"/inscripciones/{inscripcion.id}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(inscripcion.id) in response.get_data(as_text = True))
        self.assertTrue(inscripcion.localidad in response.get_data(as_text = True))
        self.assertTrue(inscripcion.servidor in response.get_data(as_text = True))
        self.assertTrue(inscripcion.monto in response.get_data(as_text = True))
        self.assertTrue(inscripcion.fecha in response.get_data(as_text = True))
        self.assertTrue(inscripcion.comprobante_uri in response.get_data(as_text = True))

    def test_guarda_informacion_inscripcion(self):
        response = self.client.post('/inscripcion',
                data = {
                    'localidad': 'Quito',
                    'servidor': 'Conny Riera',
                    'monto': '150.00',
                    'fecha': '2018-08-01',
                    'comprobante_uri': 'https://s3.aws.com/comprobante.jpg'
                    })
        self.assertEqual(response.status_code, 302)
        # self.assertTrue('Quito' in response.get_data(as_text=True))

