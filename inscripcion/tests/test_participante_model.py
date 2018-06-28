import unittest
import uuid
import datetime
from decimal import Decimal
from domain.models import Participante, InvalidMonto

class ParticipanteTestCase(unittest.TestCase):

    @unittest.skip("TODO: move this to participante form")
    def test_error_if_monto_is_not_25_at_15_aug(self):
        with self.assertRaises(InvalidMonto) as context:
            Participante(
                id = uuid.uuid1(),
                nombres_completos = 'Isabel de las Mercedes',
                sexo = "Mujer",
                telefono_contacto = '5252525',
                fecha_inscripcion = datetime.date(2018, 8, 14),
                monto = Decimal('15.25'),
                numero_deposito = '123455')

        self.assertTrue('El valor del monto debe ser 25.00 USD' in str(context.exception))
