from datetime import date
from decimal import getcontext, Decimal

getcontext().prec = 2

class Inscripcion:
    def __init__(self, id, localidad, servidor, fecha, comprobante_uri = ''):
        self.id = id
        self.localidad = localidad
        self.servidor = servidor
        self.fecha = fecha
        self.comprobante_uri = comprobante_uri
        self.participantes = []

    def add_participante(self, participante):
        self.participantes.append(participante)

    def total_amount(self):
        from functools import reduce
        return reduce(lambda p1, p2: p1.monto + p2.monto, self.participantes)

class Participante:
    def __init__(self,
            id,
            nombres_completos,
            sexo,
            numero_deposito,
            fecha_inscripcion = date.today(),
            telefono_contacto = '',
            monto = Decimal('0.00')):
        if monto is None or monto < Decimal('25.00'):
            raise InvalidMonto('El valor del monto debe ser 25.00 USD')

        self.id = id
        self.nombres_completos = nombres_completos
        self.sexo = sexo
        self.telefono_contacto = telefono_contacto
        self.monto = monto
        self.numero_deposito = numero_deposito
        self.fecha_inscripcion = fecha_inscripcion

class InvalidMonto(Exception):
    pass
