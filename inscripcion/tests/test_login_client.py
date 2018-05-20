import unittest
import uuid
from flask import current_app
from app import create_app, db
from app.models import Usuario
from utils.security import PasswordManager

class LoginIntTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies = True)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_show_login_in(self):
        response = self.client.get('/auth/login')

        self._assert_login_form(response)

    def test_begin_login_in_session(self):
        nombre_usuario = 'conny'
        clave = 'secreto'
        usuario = self._new_usuario(nombre_usuario, clave)
        login_data = {
                'nombre_usuario': nombre_usuario,
                'clave': clave
                }

        response = self.client.post(
                '/auth/login',
                data = login_data,
                follow_redirects = True)

        self.assertEqual(response.status_code, 200)
        self._assert_static_text('inscripciones/new', response)

    def test_begin_login_in_session_wrong_password(self):
        nombre_usuario = 'conny'
        clave = 'secreto'
        usuario = self._new_usuario(nombre_usuario, clave)
        login_data = {
                'nombre_usuario': nombre_usuario,
                'clave': 'wrong pass'
                }

        response = self.client.post(
                '/auth/login',
                data = login_data,
                follow_redirects = True)

        self._assert_login_form(response)
        self._assert_static_text('Credenciales incorrectas', response)

    def test_begin_login_in_session_wrong_username(self):
        nombre_usuario = 'conny'
        clave = 'secreto'
        usuario = self._new_usuario(nombre_usuario, clave)
        login_data = {
                'nombre_usuario': 'wrong username',
                'clave': clave
                }

        response = self.client.post(
                '/auth/login',
                data = login_data,
                follow_redirects = True)

        self._assert_login_form(response)
        self._assert_static_text('Credenciales incorrectas', response)

    def test_login_first_before_get_a_resource(self):
        protected_urls = [
                'inscripciones',
                'inscripciones/new',
                'inscripciones/<inscripcion_id>',
                'inscripciones/<inscripcion_id>/edit',
                'inscripciones/<inscripcion_id>/participantes',
                'inscripciones/<inscripcion_id>/participantes/new',
                'inscripciones/<inscripcion_id>/participantes/<participante_id>',
                'inscripciones/<inscripcion_id>/participantes/<participante_id>/edit',
                ]
        for url in protected_urls:
            response = self.client.get(url, follow_redirects = True)
            self._assert_login_form(response)

    def test_show_logout(self):
        response = self.client.get('/auth/logout', follow_redirects = True)

        self._assert_login_form(response)

    def _new_usuario(self, nombre_usuario, clave):
        usuario = Usuario(
                nombre_usuario = nombre_usuario,
                hashed_password = PasswordManager(clave).hash())
        db.session.add(usuario)
        db.session.commit()
        return usuario

    def _assert_static_text(self, static_text, response):
        self.assertTrue(static_text in response.get_data(as_text = True))

    def _assert_login_form(self, response):
        self.assertEqual(response.status_code, 200)
        self._assert_static_text('Nombre de usuario', response)
        self._assert_static_text('Clave', response)

