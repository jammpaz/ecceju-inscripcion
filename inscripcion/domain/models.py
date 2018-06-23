from datetime import date
from decimal import getcontext, Decimal

getcontext().prec = 2

class Inscripcion:
    def __init__(self, id, localidad, servidor, fecha, comprobante_uri = '', administradores = []):
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
        from functools import reduce
        if not self.participantes:
            return Decimal('0.00')
        return reduce(lambda p1, p2: p1.monto + p2.monto, self.participantes)

    def is_managed_by(self, admin):
        return admin in self.administradores

class Participante:
    def __init__(self,
            id,
            nombres_completos,
            sexo,
            numero_deposito,
            fecha_inscripcion = date.today(),
            telefono_contacto = '',
            monto = Decimal(0.00)):
        self.id = id
        self.nombres_completos = nombres_completos
        self.sexo = sexo
        self.telefono_contacto = telefono_contacto
        self.monto = monto
        self.numero_deposito = numero_deposito
        self.fecha_inscripcion = fecha_inscripcion

    def readable_sexo(self):
        if (self.sexo is "M"):
            return "Mujer"
        elif(self.sexo is "H"):
            return "Hombre"
        else:
            return "Desconocido"


class InvalidMonto(Exception):
    pass
