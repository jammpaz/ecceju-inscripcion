import unittest
import uuid
import datetime
from decimal import Decimal
from domain.models import Participante, InvalidMonto


class ParticipanteTestCase(unittest.TestCase):

    def test_error_if_monto_is_not_25_at_15_aug(self):
        with self.assertRaises(InvalidMonto) as context:
            Participante(
                id=uuid.uuid1(),
                nombres_completos='Isabel de las Mercedes',
                sexo="Mujer",
                telefono_contacto='5252525',
                fecha_inscripcion=datetime.date(2018, 8, 15),
                monto=Decimal('15.25'),
                numero_deposito='123455'
            ).validate_fecha_inscripcion_and_monto()

        self.assertTrue(
            'El valor del monto debe ser 25.00 USD' in str(
                context.exception))

    def test_error_if_monto_is_not_30_bucks_from_16th_aug_to_30th_aug(self):
        with self.assertRaises(InvalidMonto) as context:
            Participante(
                id=uuid.uuid1(),
                nombres_completos='Isabel de las Mercedes',
                sexo="Mujer",
                telefono_contacto='5252525',
                fecha_inscripcion=datetime.date(2018, 8, 16),
                monto=Decimal('25.00'),
                numero_deposito='123455'
            ).validate_fecha_inscripcion_and_monto()

        self.assertTrue(
            'El valor del monto debe ser 30.00 USD' in str(
                context.exception))

    def test_error_if_monto_is_not_20_bucks_from_31st_aug(self):
        with self.assertRaises(InvalidMonto) as context:
            Participante(
                id=uuid.uuid1(),
                nombres_completos='Isabel de las Mercedes',
                sexo="Mujer",
                telefono_contacto='5252525',
                fecha_inscripcion=datetime.date(2018, 8, 31),
                monto=Decimal('30.00'),
                numero_deposito='123455'
            ).validate_fecha_inscripcion_and_monto()

        self.assertTrue(
            'El valor del monto debe ser 20.00 USD' in str(
                context.exception))

    def test_error_if_fecha_inscripcion_is_after_1st_sept(self):
        with self.assertRaises(InvalidMonto) as context:
            Participante(
                id=uuid.uuid1(),
                nombres_completos='Isabel de las Mercedes',
                sexo="Mujer",
                telefono_contacto='5252525',
                fecha_inscripcion=datetime.date(2018, 9, 2),
                monto=Decimal('20.00'),
                numero_deposito='123455'
            ).validate_fecha_inscripcion_and_monto()

        self.assertTrue(
            'Ya no es posible inscribir personas después del evento' in str(
                context.exception))
