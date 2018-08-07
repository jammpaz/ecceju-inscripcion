import unittest
import uuid
from app import create_app, db, feature
from domain.models import Inscripcion
from app.repositories import InscripcionRepository, ParticipanteRepository
from builders import InscripcionBuilder, ParticipanteBuilder
from decimal import Decimal


class InscripcionRepositoryTestCase(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.inscripcion_repository = InscripcionRepository(db.session)
        self.participante_repository = ParticipanteRepository(db.session)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_find_all_by_admin(self):
        inscripcion_1 = Inscripcion(
            id=uuid.uuid1(),
            localidad='Quito Norte',
            servidor='Conny Riera',
            fecha='2018-08-01',
            administradores=['usuario_1', 'usuario_3'])

        inscripcion_2 = Inscripcion(
            id=uuid.uuid1(),
            localidad='Quito Sur',
            servidor='Raul Riera',
            fecha='2018-08-01',
            administradores=['usuario_1', 'usuario_2'])

        inscripcion_3 = Inscripcion(
            id=uuid.uuid1(),
            localidad='Quito Centro',
            servidor='Isa',
            fecha='2018-08-01',
            administradores=['usuario_2', 'usuario_3'])
        self.inscripcion_repository.add(inscripcion_1)
        self.inscripcion_repository.add(inscripcion_2)
        self.inscripcion_repository.add(inscripcion_3)

        response = self.inscripcion_repository.find_all_by_admin('usuario_2')

        self.assertEqual(
            [str(inscripcion_2.id), str(inscripcion_3.id)],
            list(map(lambda i: i.id, response))
        )

    def test_find_all_with_no_administradores(self):
        inscripcion = Inscripcion(
            id=uuid.uuid1(),
            localidad='Quito Norte',
            servidor='Conny Riera',
            fecha='2018-08-01',
            administradores=None)

        self.inscripcion_repository.add(inscripcion)

        response = self.inscripcion_repository.find_all()

        self.assertEqual(
            [str(inscripcion.id)],
            list(map(lambda i: i.id, response))
        )

    def test_get_number_of_registered_people_and_total_amount_per_localidad(
            self):
        inscripcion = InscripcionBuilder().build()
        self.inscripcion_repository.add(inscripcion)
        participante_1 = ParticipanteBuilder(id=uuid.uuid1()).build()
        self.participante_repository.add(participante_1, inscripcion.id)
        participante_2 = ParticipanteBuilder(id=uuid.uuid1()).build()
        self.participante_repository.add(participante_2, inscripcion.id)

        self.assertEqual(
            self.inscripcion_repository.get_total_amount(
                inscripcion.id), Decimal('50.00'))
        self.assertEqual(
            self.inscripcion_repository.get_total_participantes(
                inscripcion.id), 2)

    def test_error_if_inscripcion_id_is_nil_during_get_total_amount(
            self):
        with self.assertRaises(Exception) as context:
            self.inscripcion_repository.get_total_amount(inscripcion_id=None)
        self.assertTrue(
            'Inscripcion id is not valid' in str(
                context.exception))

    def test_error_if_inscripcion_id_is_nil_during_get_total_participantes(
            self):
        with self.assertRaises(Exception) as context:
            self.inscripcion_repository.get_total_participantes(
                inscripcion_id=None)
        self.assertTrue(
            'Inscripcion id is not valid' in str(
                context.exception))

    def test_zero_if_there_is_no_participantes_while_getting_total_amount(
            self):
        inscripcion = InscripcionBuilder().build()
        self.inscripcion_repository.add(inscripcion)

        self.assertEqual(
            self.inscripcion_repository.get_total_amount(
                inscripcion.id), Decimal('0.00'))
