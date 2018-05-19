import unittest
import uuid
from flask import current_app
from app import create_app, db, feature
from domain.models import Inscripcion, Participante
from app.repositories import InscripcionRepository, ParticipanteRepository
from app.models import Usuario
from utils.security import PasswordManager

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
        self._login()
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                monto = '150.00',
                fecha = '2018-08-01')
        self.inscripcion_repository.add(inscripcion)

        participante = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Raul Riera',
                sexo = 'H',
                telefono_contacto = '9999999999')
        self.participante_repository.add(participante, inscripcion.id)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/participantes/{participante.id}")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(participante.id) in response.get_data(as_text = True))
        self.assertTrue(participante.nombres_completos in response.get_data(as_text = True))
        self.assertTrue(participante.sexo in response.get_data(as_text = True))
        self.assertTrue(participante.telefono_contacto in response.get_data(as_text = True))


    def test_index_of_participantes(self):
        self._login()
        inscripcion_1 = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                monto = '280.00',
                fecha = '2018-09-01')

        inscripcion_2 = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Santo Domingo',
                servidor = 'Maria Isabel ',
                monto = '2408.57',
                fecha = '2018-08-31')

        participante_1 = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Raul Riera',
                sexo = 'H',
                telefono_contacto = '9999999999')

        participante_2 = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Gustavo de las Mercedes Riera',
                sexo = 'H',
                telefono_contacto = '8888888888')

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


    def test_new_participante(self):
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                monto = '150.00',
                fecha = '2018-08-01')
        self.inscripcion_repository.add(inscripcion)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/participantes/new")

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Nombres completos' in response.get_data(as_text = True))
        self.assertTrue('Sexo' in response.get_data(as_text = True))
        self.assertTrue('Telefono de contacto' in response.get_data(as_text = True))


    def test_create_a_participante(self):
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                monto = '150.00',
                fecha = '2018-08-01')
        self.inscripcion_repository.add(inscripcion)

        participante_data = {
                        'nombres_completos': 'Nayeli Chiriboga',
                        'sexo': 'M',
                        'telefono_contacto': '9999999999'
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

    def test_should_return_form_for_edit_a_participante(self):
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                monto = '150.00',
                fecha = '2018-08-01')

        self.inscripcion_repository.add(inscripcion)

        participante = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Raul Riera',
                sexo = 'H',
                telefono_contacto = '9999999999')
        self.participante_repository.add(participante, inscripcion.id)

        response = self.client.get(f"/inscripciones/{inscripcion.id}/participantes/{participante.id}/edit")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(participante.nombres_completos in response.get_data(as_text = True))
        self.assertTrue(participante.sexo in response.get_data(as_text = True))
        self.assertTrue(participante.telefono_contacto in response.get_data(as_text = True))


    def test_should_edit_a_participante(self):
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                monto = '150.00',
                fecha = '2018-08-01')
        self.inscripcion_repository.add(inscripcion)

        participante = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Raul Riera',
                sexo = 'H',
                telefono_contacto = '9999999999')
        self.participante_repository.add(participante, inscripcion.id)

        participante_data = {
                        'nombres_completos': 'Nayeli Chiriboga',
                        'sexo': 'M',
                        'telefono_contacto': '9999999999'
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


    def _assert_static_text(self, static_text, response):
        self.assertTrue(static_text in response.get_data(as_text = True))

    def _new_usuario(self, nombre_usuario, clave):
        usuario = Usuario(
                nombre_usuario = nombre_usuario,
                hashed_password = PasswordManager(clave).hash())
        db.session.add(usuario)
        db.session.commit()
        return usuario

    def _login(self):
        nombre_usuario = 'usuario_1'
        clave = 'secreto'
        self._new_usuario(nombre_usuario, clave)
        login_data = {
                'nombre_usuario': nombre_usuario,
                'clave': clave
                }
        return self.client.post(
                '/auth/login',
                data = login_data,
                follow_redirects = True)
