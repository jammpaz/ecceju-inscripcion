import uuid
from datetime import date
from domain.models import Participante
from decimal import Decimal

class ParticipanteBuilder:
    def __init__(self,
            id = uuid.uuid1(),
            nombres_completos = 'Conny Riera',
            sexo = 'M',
            numero_deposito = '122344XXX',
            telefono_contacto = '022222222',
            monto = Decimal('25.00'),
            fecha_inscripcion = date.today()):
        self.id = id
        self.nombres_completos = nombres_completos
        self.sexo = sexo
        self.telefono_contacto = telefono_contacto
        self.monto = monto
        self.numero_deposito = numero_deposito
        self.fecha_inscripcion = fecha_inscripcion

    def build(self):
        return Participante(
                id = self.id,
                nombres_completos = self.nombres_completos,
                sexo = self.sexo,
                telefono_contacto = self.telefono_contacto,
                numero_deposito = self.numero_deposito,
                monto = self.monto,
                fecha_inscripcion = self.fecha_inscripcion)


