import unittest
import uuid
from app import db
from domain.models import Participante, Inscripcion
from app.repositories import ParticipanteRepository, InscripcionRepository
from builders import ParticipanteBuilder, InscripcionBuilder

class ParticipanteRepositoryTestCase(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.inscripcion_repository = InscripcionRepository(db.session)
        self.participante_repository = ParticipanteRepository(db.session)


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_find_by_with_none_monto(self):
        inscripcion = InscripcionBuilder().build()
        participante = ParticipanteBuilder(monto = None).build()

        self.inscripcion_repository.add(inscripcion)
        self.participante_repository.add(participante, inscripcion.id)

        response = self.participante_repository.find_by(participante.id)

        self.assertEqual(participante.id, response.id)


    def test_find_all_with_none_monto(self):
        inscripcion = InscripcionBuilder().build()
        participante = ParticipanteBuilder(monto = None).build()

        self.inscripcion_repository.add(inscripcion)
        self.participante_repository.add(participante, inscripcion.id)

        response = self.participante_repository.find_all(inscripcion.id)

        self.assertEqual(participante.id, response[0].id)
