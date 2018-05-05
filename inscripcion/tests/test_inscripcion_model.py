import unittest
import uuid
from domain.models import Inscripcion, Participante

class InscripcionTestCase(unittest.TestCase):

    def test_adds_new_participante(self):
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                monto = '150.00',
                fecha = '2018-08-01',
                comprobante_uri = 'https://s3.aws.com/comprobante.jpg')

        participante = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Isabel de las Mercedes',
                sexo = "Mujer",
                telefono_contacto = '5252525')

        inscripcion.addParticipante(participante)

        self.assertTrue(participante in inscripcion.participantes)
