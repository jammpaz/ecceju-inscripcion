from datetime import date
from decimal import Decimal

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
        if not self.participantes:
            return Decimal('0.00')
        valid_participantes = list(filter(lambda p: isinstance(p.monto, Decimal), self.participantes))
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

    def __repr__(self):
        return f'(id: {self.id}, nombre: {self.nombres_completos})'


class InvalidMonto(Exception):
    pass
