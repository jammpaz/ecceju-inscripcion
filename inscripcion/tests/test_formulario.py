import unittest
from flask import current_app
from app import create_app

class FormularioTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies = True)

    def tearDown(self):
        self.app_context.pop()

    def test_muestra_formulario(self):
        response = self.client.get('/formulario')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Formulario de inscripción' in response.get_data(as_text = True))

    def test_guarda_informacion_formulario(self):
        response = self.client.post('/formulario',
                data = {
                    'localidad': 'Quito',
                    'servidor': 'Conny Riera',
                    'monto': '150.00',
                    'fecha': '2018-08-01',
                    'comprobante_uri': 'https://s3.aws.com/comprobante.jpg'
                    })
        self.assertEqual(response.status_code, 302)
        # self.assertTrue('Quito' in response.get_data(as_text=True))

