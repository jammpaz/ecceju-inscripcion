import unittest
import uuid
from domain.models import Inscripcion, Participante
from decimal import Decimal


class InscripcionTestCase(unittest.TestCase):

    def test_adds_new_participante_and_calculate_total_amount(self):
        inscripcion = Inscripcion(
            id=uuid.uuid1(),
            localidad='Quito',
            servidor='Conny Riera',
            fecha='2018-08-01',
            comprobante_uri='https://s3.aws.com/comprobante.jpg')

        participante_1 = Participante(
            id=uuid.uuid1(),
            nombres_completos='Isabel de las Mercedes',
            sexo="Mujer",
            telefono_contacto='5252525',
            monto=Decimal('25.00'),
            numero_deposito='123455')

        participante_2 = Participante(
            id=uuid.uuid1(),
            nombres_completos='Conny Riera',
            sexo="Mujer",
            telefono_contacto='5252525',
            monto=Decimal('25.00'),
            numero_deposito='123456')

        inscripcion.participantes = [participante_1, participante_2]

        self.assertEqual([participante_1, participante_2],
                         inscripcion.participantes)
        self.assertEqual(inscripcion.total_amount(), Decimal('50.00'))

    def test_total_amount_is_zero_if_participantes_are_emtpy(self):
        inscripcion = Inscripcion(
            id=uuid.uuid1(),
            localidad='Quito',
            servidor='Conny Riera',
            fecha='2018-08-01')

        self.assertEqual(inscripcion.total_amount(), 0.00)

    @unittest.skip("Applying validations over monto")
    def test_calculate_total_amount_including_none_type(self):
        inscripcion = Inscripcion(
            id=uuid.uuid1(),
            localidad='Quito',
            servidor='Conny Riera',
            fecha='2018-08-01',
            comprobante_uri='https://s3.aws.com/comprobante.jpg')

        participante_1 = Participante(
            id=uuid.uuid1(),
            nombres_completos='Isabel de las Mercedes',
            sexo="Mujer",
            telefono_contacto='5252525',
            monto=None,
            numero_deposito='123455')

        participante_2 = Participante(
            id=uuid.uuid1(),
            nombres_completos='Conny Riera',
            sexo="Mujer",
            telefono_contacto='5252525',
            monto=Decimal('25.50'),
            numero_deposito='123456')

        participante_3 = Participante(
            id=uuid.uuid1(),
            nombres_completos='Conny Riera',
            sexo="Mujer",
            telefono_contacto='5252525',
            monto=Decimal('25'),
            numero_deposito='123456')

        inscripcion.participantes = [
            participante_1, participante_2, participante_3]

        self.assertEqual(inscripcion.total_amount(), Decimal(50.50))

    def test_adds_new_admin(self):
        inscripcion = Inscripcion(
            id=uuid.uuid1(),
            localidad='Quito',
            servidor='Conny Riera',
            fecha='2018-08-01',
            administradores=['conny', 'admin_1'])

        self.assertEqual(['conny', 'admin_1'], inscripcion.administradores)

    def test_return_true_if_user_belongs_admins_group(
            self):
        inscripcion_1 = Inscripcion(
            id=uuid.uuid1(),
            localidad='Quito Norte',
            servidor='Conny Riera',
            fecha='2018-08-01',
            administradores=['usuario_1', 'usuario_3'])

        response = inscripcion_1.is_managed_by('usuario_3')

        self.assertTrue(response)

    def test_false_if_user_does_not_belongs_admins_group(
            self):
        inscripcion_1 = Inscripcion(
            id=uuid.uuid1(),
            localidad='Quito Norte',
            servidor='Conny Riera',
            fecha='2018-08-01',
            administradores=['usuario_1', 'usuario_3'])

        response = inscripcion_1.is_managed_by('non_allowed_user')

        self.assertFalse(response)
