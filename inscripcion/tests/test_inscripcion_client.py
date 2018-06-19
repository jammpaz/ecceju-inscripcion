import unittest
import uuid
from flask import current_app
from app import create_app, db, feature
from io import BytesIO
from domain.models import Inscripcion
from app.repositories import InscripcionRepository
from app.models import Usuario
from utils.security import PasswordManager

class InscripcionIntTestCase(unittest.TestCase):

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


    def test_show_login_in_main_route(self):
        response = self.client.get('/', follow_redirects = True)

        self.assertEqual(response.status_code, 200)


    def test_show_an_inscripcion(self):
        self._login('usuario_1', 'secreto')
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['usuario_1'])

        if feature.is_enabled("COMPROBANTE_PAGO"):
            inscripcion.comprobante_uri = 'https://s3.aws.com/comprobante.jpg'
        self.inscripcion_repository.add(inscripcion)

        response = self.client.get(f"/inscripciones/{inscripcion.id}")

        self.assertEqual(response.status_code, 200)
        self._assert_static_text(str(inscripcion.id), response)
        self._assert_static_text(inscripcion.localidad, response)
        self._assert_static_text(inscripcion.servidor, response)
        if feature.is_enabled("COMPROBANTE_PAGO"):
            self.assertTrue(inscripcion.comprobante_uri in response.get_data(as_text = True))

    def test_should_not_show_an_inscripcion_if_current_user_does_not_belong_to_admin_group_of_inscripcion(self):
        self._login('usuario_1', 'secreto')
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['usuario_admin', 'usuario_2'])
        self.inscripcion_repository.add(inscripcion)

        response = self.client.get(f"/inscripciones/{inscripcion.id}")

        self.assertEqual(response.status_code, 401)


    def test_index_of_inscripcion(self):
        self._login('usuario_1', 'secreto')
        inscripcion_1 = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-09-01',
                administradores = ['usuario_1', 'admin'])

        inscripcion_2 = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Santo Domingo',
                servidor = 'Maria Isabel ',
                fecha = '2018-08-31',
                administradores = ['usuario_1', 'admin'])

        self.inscripcion_repository.add(inscripcion_1)
        self.inscripcion_repository.add(inscripcion_2)

        response = self.client.get(f"/inscripciones")

        self.assertEqual(response.status_code, 200)
        self._assert_static_text(str(inscripcion_1.id), response)
        self._assert_static_text(str(inscripcion_2.id), response)
        self._assert_static_text(inscripcion_1.localidad, response)
        self._assert_static_text(inscripcion_2.localidad, response)


    def test_new_inscripcion(self):
        self._login()
        response = self.client.get("/inscripciones/new")

        self.assertEqual(response.status_code, 200)

        self._assert_static_text('Nombre de la Localidad', response)
        self._assert_static_text('Nombre del servidor/a', response)
        self._assert_static_text('Fecha de pago', response)
        if feature.is_enabled("COMPROBANTE_PAGO"):
            self.assertTrue('Comprobante de pago' in response.get_data(as_text = True))


    def test_create_an_inscripcion(self):
        self._login()
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
        self._login('conny', 'secreto')
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['conny', 'admin'])

        self.inscripcion_repository.add(inscripcion)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/edit")

        self.assertEqual(response.status_code, 200)
        self._assert_static_text(inscripcion.localidad, response)
        self._assert_static_text(inscripcion.servidor, response)
        self._assert_static_text(inscripcion.fecha, response)

    def test_should_not_to_allow_edit_an_inscripcion_if_current_user_is_not_admin(self):
        self._login('conny', 'secreto')
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['raul', 'admin'])

        self.inscripcion_repository.add(inscripcion)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/edit")

        self.assertEqual(response.status_code, 401)


    def test_should_edit_an_inscripcion(self):
        self._login()
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
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

    def _assert_static_text(self, static_text, response):
        self.assertTrue(static_text in response.get_data(as_text = True))

    def _new_usuario(self, nombre_usuario, clave):
        usuario = Usuario(
                nombre_usuario = nombre_usuario,
                hashed_password = PasswordManager(clave).hash())
        db.session.add(usuario)
        db.session.commit()
        return usuario

    def _login(self, nombre_usuario = 'usuario_1', clave = 'secreto'):
        self._new_usuario(nombre_usuario, clave)
        login_data = {
                'nombre_usuario': nombre_usuario,
                'clave': clave
                }
        return self.client.post(
                '/auth/login',
                data = login_data,
                follow_redirects = True)

