from datetime import date
from decimal import Decimal
import uuid
import datetime


class Inscripcion:
    def __init__(
            self,
            id,
            localidad,
            servidor,
            fecha,
            comprobante_uri='',
            administradores=[]):
        self.id = id
        self.localidad = localidad
        self.servidor = servidor
        self.fecha = fecha
        self.comprobante_uri = comprobante_uri
        self.participantes = []
        self.administradores = administradores

    def add_participante(self, participante):
        self.participantes.append(participante)

    def total_amount(self):
        if not self.participantes:
            return Decimal('0.00')
        valid_participantes = list(
            filter(
                lambda p: isinstance(
                    p.monto,
                    Decimal),
                self.participantes))
        suma = sum(list(map(lambda p: float(p.monto), valid_participantes)))
        return Decimal(suma)

    def is_managed_by(self, admin):
        return admin in self.administradores

    def __repr__(self):
        return f'(id: {self.id}, nombre: {self.localidad})'


class Participante:
    def __init__(self,
                 id,
                 nombres_completos,
                 sexo,
                 numero_deposito,
                 fecha_inscripcion=date.today(),
                 telefono_contacto='',
                 monto=Decimal(0.00)):
        self.id = id
        self.nombres_completos = nombres_completos
        self.sexo = sexo
        self.telefono_contacto = telefono_contacto
        self.monto = monto
        self.numero_deposito = numero_deposito
        self.fecha_inscripcion = fecha_inscripcion

    def validate_fecha_inscripcion_and_monto(self):
        if self.fecha_inscripcion <= datetime.date(2018, 8, 15):
            if self.monto is None or self.monto != Decimal('25.00'):
                raise InvalidMonto('El valor del monto debe ser 25.00 USD')

        if datetime.date(
                2018,
                8,
                16) <= self.fecha_inscripcion < datetime.date(
                2018,
                8,
                30):
            if self.monto is None or self.monto != Decimal('30.00'):
                raise InvalidMonto('El valor del monto debe ser 30.00 USD')

        if datetime.date(
                2018,
                8,
                31) <= self.fecha_inscripcion <= datetime.date(
                2018,
                9,
                1):
            if self.monto is None or self.monto != Decimal('20.00'):
                raise InvalidMonto('El valor del monto debe ser 20.00 USD')

        if datetime.date(2018, 9, 2) <= self.fecha_inscripcion:
            raise InvalidMonto(
                'Ya no es posible inscribir personas después del evento')

    def readable_sexo(self):
        if (self.sexo is "M"):
            return "Mujer"
        elif(self.sexo is "H"):
            return "Hombre"
        else:
            return "Desconocido"

    def __repr__(self):
        return f'(id: {self.id}, nombre: {self.nombres_completos})'


class PreventaCamiseta:
    def __init__(self,
                 id=uuid.uuid1(),
                 nombres_completos='Desconocido',
                 localidad='Desconocido',
                 color='blanco',
                 talla='34',
                 cantidad=1,
                 fecha_deposito=date.today(),
                 numero_deposito='Desconocido',
                 cedula='0000000000'):
        self.id = id
        self.nombres_completos = nombres_completos
        self.localidad = localidad
        self.color = color
        self.talla = talla
        self.cantidad = cantidad
        self.fecha_deposito = fecha_deposito
        self.numero_deposito = numero_deposito
        self.cedula = cedula


class InvalidMonto(Exception):
    pass
