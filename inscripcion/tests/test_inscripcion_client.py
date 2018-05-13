import unittest
import uuid
from flask import current_app
from app import create_app, db, feature
from io import BytesIO
from domain.models import Inscripcion
from app.repositories import InscripcionRepository

class InscripcionTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies = True)
        self.inscripcion_repository = InscripcionRepository(db.session)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_show_an_inscripcion(self):
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                monto = '150.00',
                fecha = '2018-08-01')
        if feature.is_enabled("COMPROBANTE_PAGO"):
            inscripcion.comprobante_uri = 'https://s3.aws.com/comprobante.jpg'

        self.inscripcion_repository.add(inscripcion)

        response = self.client.get(f"/inscripciones/{inscripcion.id}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(inscripcion.id) in response.get_data(as_text = True))
        self.assertTrue(inscripcion.localidad in response.get_data(as_text = True))
        self.assertTrue(inscripcion.servidor in response.get_data(as_text = True))
        self.assertTrue(inscripcion.monto in response.get_data(as_text = True))
        self.assertTrue(inscripcion.fecha in response.get_data(as_text = True))
        if feature.is_enabled("COMPROBANTE_PAGO"):
            self.assertTrue(inscripcion.comprobante_uri in response.get_data(as_text = True))


    def test_index_of_inscripcion(self):
        inscripcion_1 = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                monto = '280.00',
                fecha = '2018-09-01')
        if feature.is_enabled("COMPROBANTE_PAGO"):
            inscripcion_1.comprobante_uri = 'comprobante.jpg'

        inscripcion_2 = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Santo Domingo',
                servidor = 'Maria Isabel ',
                monto = '2408.57',
                fecha = '2018-08-31')
        if feature.is_enabled("COMPROBANTE_PAGO"):
            inscripcion_2.comprobante_uri = 'comprobante.jpg'

        self.inscripcion_repository.add(inscripcion_1)
        self.inscripcion_repository.add(inscripcion_2)

        response = self.client.get(f"/inscripciones")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(inscripcion_1.id) in response.get_data(as_text = True))
        self.assertTrue(str(inscripcion_2.id) in response.get_data(as_text = True))
        self.assertTrue(inscripcion_1.localidad in response.get_data(as_text = True))
        self.assertTrue(inscripcion_2.localidad in response.get_data(as_text = True))
        self.assertTrue(inscripcion_1.monto in response.get_data(as_text = True))
        self.assertTrue(inscripcion_2.monto in response.get_data(as_text = True))


    def test_new_inscripcion(self):
        response = self.client.get("/inscripciones/new")

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Nombre de la Localidad' in response.get_data(as_text = True))
        self.assertTrue('Nombre del servidor/a' in response.get_data(as_text = True))
        self.assertTrue('Monto cancelado (USD)' in response.get_data(as_text = True))
        self.assertTrue('Fecha de pago' in response.get_data(as_text = True))
        if feature.is_enabled("COMPROBANTE_PAGO"):
            self.assertTrue('Comprobante de pago' in response.get_data(as_text = True))


    def test_create_an_inscripcion(self):
        inscripcion_data = {
                        'localidad': 'Quito',
                        'servidor': 'Conny Riera',
                        'monto': '150.00',
                        'fecha': '2018-08-01'
                       }

        if feature.is_enabled("COMPROBANTE_PAGO"):
            inscripcion_data = {
                    'localidad': 'Quito',
                    'servidor': 'Conny Riera',
                    'monto': '150.00',
                    'fecha': '2018-08-01',
                    'comprobante_uri': (
                        BytesIO('Comprobante sample content'.encode('utf-8')),
                        'comprobante.jpg'
                        )
                    }

        response = self.client.post(
                '/inscripciones/new',
                content_type = 'multipart/form-data',
                buffered = True,
                data = inscripcion_data)

        inscripciones = self.inscripcion_repository.find_all()
        filtered_inscripcion = list(filter(lambda i:
                i.localidad == 'Quito' and
                i.servidor == 'Conny Riera',
                inscripciones))
        self.assertTrue(len(filtered_inscripcion) == 1)
        self.assertEqual(response.status_code, 302)

    def test_should_return_form_for_edit_an_inscripcion(self):
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                monto = '150.00',
                fecha = '2018-08-01')

        if feature.is_enabled("COMPROBANTE_PAGO"):
            inscripcion.comprobante_uri = 'comprobante.jpg'

        self.inscripcion_repository.add(inscripcion)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/edit")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(inscripcion.localidad in response.get_data(as_text = True))
        self.assertTrue(inscripcion.servidor in response.get_data(as_text = True))
        self.assertTrue(inscripcion.monto in response.get_data(as_text = True))
        self.assertTrue(inscripcion.fecha in response.get_data(as_text = True))

    def test_should_edit_an_inscripcion(self):
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                monto = '150.00',
                fecha = '2018-08-01')

        if feature.is_enabled("COMPROBANTE_PAGO"):
            inscripcion.comprobante_uri = 'comprobante.jpg'

        self.inscripcion_repository.add(inscripcion)

        inscripcion_data = {
                        'localidad': 'Quito Norte',
                        'servidor': 'Raul Riera',
                        'monto': '450.00',
                        'fecha': '2018-09-01'
                       }

        if feature.is_enabled('COMPROBANTE_PAGO'):
            inscripcion_data = {
                        'localidad': 'Quito Norte',
                        'servidor': 'Raul Riera',
                        'monto': '450.00',
                        'fecha': '2018-09-01',
                        'comprobante_uri': (
                            BytesIO('Comprobante sample content'.encode('utf-8')),
                            'comprobante.jpg'
                            )
                       }

        response = self.client.post(
                f'/inscripciones/{inscripcion.id}/edit',
                content_type = 'multipart/form-data',
                buffered = True,
                data = inscripcion_data)

        inscripciones = self.inscripcion_repository.find_all()
        filtered_inscripcion = list(filter(lambda i:
                i.localidad == 'Quito Norte' and
                i.servidor == 'Raul Riera',
                inscripciones))
        self.assertTrue(len(filtered_inscripcion) == 1)
        self.assertEqual(response.status_code, 302)
