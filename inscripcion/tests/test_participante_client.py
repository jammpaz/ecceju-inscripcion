import unittest
import uuid
from flask import current_app
from app import create_app, db, feature
from domain.models import Inscripcion, Participante
from app.repositories import InscripcionRepository, ParticipanteRepository
from app.models import Usuario
from utils.security import PasswordManager
from decimal import Decimal
from builders import ParticipanteBuilder, InscripcionBuilder

class ParticipanteIntTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies = True)
        self.inscripcion_repository = InscripcionRepository(db.session)
        self.participante_repository = ParticipanteRepository(db.session)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_show_a_participante(self):
        self._login('usuario_1', 'secreto')
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['admin_1', 'usuario_1'])
        self.inscripcion_repository.add(inscripcion)

        participante = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Raul Riera',
                sexo = 'H',
                telefono_contacto = '9999999999',
                numero_deposito = '12312',
                monto = 25.00 )
        self.participante_repository.add(participante, inscripcion.id)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/participantes/{participante.id}")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(participante.id) in response.get_data(as_text = True))
        self.assertTrue(participante.nombres_completos in response.get_data(as_text = True))
        self.assertTrue(participante.sexo in response.get_data(as_text = True))
        self.assertTrue(participante.telefono_contacto in response.get_data(as_text = True))
        self.assertTrue(str(participante.monto) in response.get_data(as_text = True))
        self.assertTrue(participante.numero_deposito in response.get_data(as_text = True))

    def test_should_not_show_a_participante_if_current_user_is_not_admin(self):
        self._login('usuario_1', 'secreto')
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['usuario_2', 'admin'])
        self.inscripcion_repository.add(inscripcion)

        participante = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Raul Riera',
                sexo = 'H',
                telefono_contacto = '9999999999',
                numero_deposito = '12312',
                monto = 25.00 )
        self.participante_repository.add(participante, inscripcion.id)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/participantes/{participante.id}")

        self.assertEqual(response.status_code, 401)


    def test_index_of_participantes(self):
        self._login()
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

        participante_1 = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Raul Riera',
                sexo = 'H',
                telefono_contacto = '9999999999',
                monto = Decimal('25.00'),
                numero_deposito = '123456')

        participante_2 = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Gustavo de las Mercedes Riera',
                sexo = 'H',
                telefono_contacto = '8888888888',
                monto = Decimal('25.00'),
                numero_deposito = '12457')

        self.inscripcion_repository.add(inscripcion_1)
        self.inscripcion_repository.add(inscripcion_2)
        self.participante_repository.add(participante_1, inscripcion_2.id)
        self.participante_repository.add(participante_2, inscripcion_2.id)

        response = self.client.get(f"/inscripciones/{inscripcion_2.id}/participantes")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(participante_1.id) in response.get_data(as_text = True))
        self.assertTrue(participante_1.nombres_completos in response.get_data(as_text = True))
        self.assertTrue(str(participante_2.id) in response.get_data(as_text = True))
        self.assertTrue(participante_2.nombres_completos in response.get_data(as_text = True))
        self.assertTrue('50' in response.get_data(as_text = True))


    def test_should_not_show_index_of_participantes_if_current_user_is_not_admin(self):
        self._login()
        inscripcion_1 = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-09-01',
                administradores = ['usuario_2', 'admin'])


        participante_1 = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Raul Riera',
                sexo = 'H',
                telefono_contacto = '9999999999',
                monto = Decimal('25.00'),
                numero_deposito = '123456')


        self.inscripcion_repository.add(inscripcion_1)
        self.participante_repository.add(participante_1, inscripcion_1.id)

        response = self.client.get(f"/inscripciones/{inscripcion_1.id}/participantes")

        self.assertEqual(response.status_code, 401)


    def test_new_participante(self):
        self._login()
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['usuario_1', 'admin'])
        self.inscripcion_repository.add(inscripcion)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/participantes/new")

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Nombres completos' in response.get_data(as_text = True))
        self.assertTrue('Sexo' in response.get_data(as_text = True))
        self.assertTrue('Telefono de contacto' in response.get_data(as_text = True))
        self.assertTrue('Monto' in response.get_data(as_text = True))
        self.assertTrue('Número de depósito' in response.get_data(as_text = True))


    def test_should_not_allow_new_participante_if_current_user_is_not_admin(self):
        self._login()
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['admin', 'usuario_2'])
        self.inscripcion_repository.add(inscripcion)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/participantes/new")

        self.assertEqual(response.status_code, 401)


    def test_create_a_participante(self):
        self._login()
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['usuario_1', 'admin'])
        self.inscripcion_repository.add(inscripcion)

        participante_data = {
                        'nombres_completos': 'Nayeli Chiriboga',
                        'sexo': 'M',
                        'telefono_contacto': '9999999999',
                        'monto': 25.00,
                        'numero_deposito': 'ABCD-1111'
                       }

        response = self.client.post(
                f'/inscripciones/{inscripcion.id}/participantes/new',
                data = participante_data)

        participantes = self.participante_repository.find_all(inscripcion.id)
        filtered_participante = list(filter(lambda i:
                i.nombres_completos == 'Nayeli Chiriboga' and
                i.sexo == 'M' and
                i.telefono_contacto == '9999999999',
                participantes))
        self.assertTrue(len(filtered_participante) == 1)
        self.assertEqual(response.status_code, 302)

    def test_should_return_error_if_required_fields_are_not_present_during_participante_creation(self):
        self._login()
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['usuario_1', 'admin'])
        self.inscripcion_repository.add(inscripcion)

        participante_data = {
                        'sexo': 'M',
                        'telefono_contacto': '9999999999',
                       }

        response = self.client.post(
                f'/inscripciones/{inscripcion.id}/participantes/new',
                data = participante_data)

        participantes = self.participante_repository.find_all(inscripcion.id)
        filtered_participante = list(filter(lambda i:
                i.nombres_completos == 'Nayeli Chiriboga' and
                i.sexo == 'M' and
                i.telefono_contacto == '9999999999',
                participantes))
        self.assertTrue(len(filtered_participante) == 0)
        self._assert_static_text('Error en el campo: Monto cancelado (USD) - This field is required', response)
        self._assert_static_text('Error en el campo: Nombres completos - This field is required', response)
        self._assert_static_text('Error en el campo: Número de depósito - This field is required', response)


    def test_should_return_error_if_monto_is_invalid(self):
        self._login()
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['usuario_1', 'admin'])
        self.inscripcion_repository.add(inscripcion)

        participante_data = {
                        'nombres_completos': 'Nayeli Chiriboga',
                        'sexo': 'M',
                        'telefono_contacto': '9999999999',
                        'monto': 20.00,
                        'fecha_inscripcion': '2018-08-30',
                        'numero_deposito': 'ABCD-1111'
                       }

        response = self.client.post(
                f'/inscripciones/{inscripcion.id}/participantes/new',
                data = participante_data)

        participantes = self.participante_repository.find_all(inscripcion.id)
        filtered_participante = list(filter(lambda i:
                i.nombres_completos == 'Nayeli Chiriboga' and
                i.sexo == 'M' and
                i.telefono_contacto == '9999999999',
                participantes))
        self.assertTrue(len(filtered_participante) == 0)
        self._assert_static_text('El valor del monto debe ser 25.00 USD', response)


    def test_should_return_form_for_edit_a_participante(self):
        self._login()
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['usuario_1', 'admin'])

        self.inscripcion_repository.add(inscripcion)

        participante = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Raul Riera',
                sexo = 'H',
                telefono_contacto = '9999999999',
                monto = Decimal('25.00'),
                numero_deposito = '14566185')
        self.participante_repository.add(participante, inscripcion.id)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/participantes/{participante.id}/edit")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(participante.nombres_completos in response.get_data(as_text = True))
        self.assertTrue(participante.sexo in response.get_data(as_text = True))
        self.assertTrue(participante.telefono_contacto in response.get_data(as_text = True))

    def test_should_not_return_form_for_edit_a_participante_if_current_user_is_not_admin(self):
        self._login()
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['usuario_2', 'admin'])

        self.inscripcion_repository.add(inscripcion)

        participante = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Raul Riera',
                sexo = 'H',
                telefono_contacto = '9999999999',
                monto = Decimal('25.00'),
                numero_deposito = '14566185')
        self.participante_repository.add(participante, inscripcion.id)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/participantes/{participante.id}/edit")

        self.assertEqual(response.status_code, 401)


    def test_should_edit_a_participante(self):
        self._login()
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                administradores = ['usuario_1', 'admin'])
        self.inscripcion_repository.add(inscripcion)

        participante = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Raul Riera',
                sexo = 'H',
                telefono_contacto = '9999999999',
                monto = Decimal('25.00'),
                numero_deposito = '14587')
        self.participante_repository.add(participante, inscripcion.id)

        participante_data = {
                        'nombres_completos': 'Nayeli Chiriboga',
                        'sexo': 'M',
                        'telefono_contacto': '9999999999',
                        'monto': 25.00,
                        'numero_deposito': 'xxxxx'
                       }

        response = self.client.post(
                f'/inscripciones/{inscripcion.id}/participantes/{participante.id}/edit',
                data = participante_data)

        participantes = self.participante_repository.find_all(inscripcion.id)
        filtered_participante = list(filter(lambda i:
                i.nombres_completos == 'Nayeli Chiriboga' and
                i.sexo == 'M' and
                i.telefono_contacto == '9999999999',
                participantes))
        self.assertTrue(len(filtered_participante) == 1)
        self.assertEqual(response.status_code, 302)


    def test_should_return_200_showing_participantes_page_after_deleting_one(self):
        self._login()
        inscripcion = InscripcionBuilder().build()
        self.inscripcion_repository.add(inscripcion)

        participante = ParticipanteBuilder().build()
        self.participante_repository.add(participante, inscripcion.id)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/participantes/{participante.id}/destroy",
                follow_redirects = True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(participante.nombres_completos in response.get_data(as_text = True))

    def test_should_return_not_found_while_deleting_a_participante(self):
        self._login()
        inscripcion = InscripcionBuilder().build()
        self.inscripcion_repository.add(inscripcion)

        participante = ParticipanteBuilder().build()
        self.participante_repository.add(participante, inscripcion.id)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/participantes/non-existing-participante/destroy",
                follow_redirects = True)

        self.assertEqual(response.status_code, 404)


    def test_should_return_403_while_deleting_a_participante(self):
        self._login()
        inscripcion = InscripcionBuilder(administradores = ['usuario_2', 'admin']).build()
        self.inscripcion_repository.add(inscripcion)
        participante = ParticipanteBuilder().build()
        self.participante_repository.add(participante, inscripcion.id)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/participantes/{participante.id}/destroy",
                follow_redirects = True)

        self.assertEqual(response.status_code, 401)


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
