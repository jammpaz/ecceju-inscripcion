import uuid
from domain.models import Participante, Inscripcion
from decimal import Decimal
from datetime import date

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

class InscripcionBuilder:
    def __init__(self,
            id = uuid.uuid1(),
            localidad = 'RCC UIO',
            servidor = 'Conny Riera',
            fecha = '2018-01-01' ,
            comprobante_uri = 'http://google.com',
            administradores = ['admin', 'usuario_1']):
        self.id = id
        self.localidad = localidad
        self.servidor = servidor
        self.fecha = fecha
        self.comprobante_uri = comprobante_uri
        self.administradores = administradores

    def build(self):
        return Inscripcion(
                id = self.id,
                localidad = self.localidad,
                servidor = self.servidor,
                fecha = self.fecha,
                comprobante_uri = self.comprobante_uri,
                administradores = self.administradores)
