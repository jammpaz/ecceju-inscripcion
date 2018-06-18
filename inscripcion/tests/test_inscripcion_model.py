import unittest
import uuid
from domain.models import Inscripcion, Participante

class InscripcionTestCase(unittest.TestCase):

    def test_adds_new_participante_and_calculate_total_amount(self):
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01',
                comprobante_uri = 'https://s3.aws.com/comprobante.jpg')

        participante_1 = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Isabel de las Mercedes',
                sexo = "Mujer",
                telefono_contacto = '5252525',
                monto = 25.25,
                numero_deposito = '123455')

        participante_2 = Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Conny Riera',
                sexo = "Mujer",
                telefono_contacto = '5252525',
                monto = 25.50,
                numero_deposito = '123456')

        inscripcion.add_participante(participante_1)
        inscripcion.add_participante(participante_2)

        self.assertEqual([ participante_1, participante_2 ],  inscripcion.participantes)
        self.assertEqual(inscripcion.total_amount(), 50.75)

    def test_total_amount_is_zero_if_participantes_are_emtpy(self):
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = 'Quito',
                servidor = 'Conny Riera',
                fecha = '2018-08-01')

        self.assertEqual(inscripcion.total_amount(), 0.00)
