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
        self.inscripcion = InscripcionBuilder().build()
        self.inscripcion_repository.add(self.inscripcion)


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    @unittest.skip("Applying validations over monto")
    def test_find_by_with_none_monto(self):
        participante = ParticipanteBuilder(monto = None).build()
        self.participante_repository.add(participante, self.inscripcion.id)

        response = self.participante_repository.find_by(participante.id)

        self.assertEqual(participante.id, response.id)


    @unittest.skip("Applying validations over monto")
    def test_find_all_with_none_monto(self):
        participante = ParticipanteBuilder(monto = None).build()
        self.participante_repository.add(participante, self.inscripcion.id)

        response = self.participante_repository.find_all(self.inscripcion.id)

        self.assertEqual(participante.id, response[0].id)

    def test_delete_by_id(self):
        participante = ParticipanteBuilder().build()
        self.participante_repository.add(participante, self.inscripcion.id)

        self.participante_repository.delete(participante)

        self.assertIsNone(self.participante_repository.find_by(participante.id))
