import uuid
from datetime import datetime
from app.models import InscripcionData, ParticipanteData
from domain.models import Inscripcion, Participante

class InscripcionRepository:
    def __init__(self, session):
        self.session = session

    def add(self, inscripcion):
        data = InscripcionData(
                id = str(inscripcion.id),
                localidad = inscripcion.localidad,
                servidor = inscripcion.servidor,
                monto = inscripcion.monto,
                fecha = datetime.strptime(inscripcion.fecha, '%Y-%m-%d'),
                comprobante_uri = inscripcion.comprobante_uri)
        self.session.add(data)
        self.session.commit()

    def update(self, inscripcion):
        data = InscripcionData.query.filter_by(id = str(inscripcion.id)).first()
        data.localidad = inscripcion.localidad
        data.servidor = inscripcion.servidor
        data.monto = inscripcion.monto
        data.fecha = datetime.strptime(inscripcion.fecha, '%Y-%m-%d')
        data.comprobante_uri = inscripcion.comprobante_uri
        self.session.add(data)
        self.session.commit()

    def find_by(self, inscripcion_id):
        data = InscripcionData.query.filter_by(id = str(inscripcion_id)).first()
        return Inscripcion(
                id = data.id,
                localidad = data.localidad,
                servidor = data.servidor,
                monto = data.monto,
                fecha = data.fecha,
                comprobante_uri = data.comprobante_uri)

    def find_all(self):
        data_list = InscripcionData.query.all()
        return list(map(lambda data:
                Inscripcion(id = data.id,
                    localidad = data.localidad,
                    servidor = data.servidor,
                    monto = data.monto,
                    fecha = data.fecha,
                    comprobante_uri = data.comprobante_uri), data_list))


class ParticipanteRepository:
    def __init__(self, session):
        self.session = session


    def add(self, participante, inscripcion_id):
        data = ParticipanteData(
                id = str(participante.id),
                nombres_completos = participante.nombres_completos,
                sexo = participante.sexo,
                telefono_contacto = participante.telefono_contacto,
                monto = participante.monto,
                numero_deposito = participante.numero_deposito,
                inscripcion_id = str(inscripcion_id))
        self.session.add(data)
        self.session.commit()


    def update(self, participante):
        data = ParticipanteData.query.filter_by(id = str(participante.id)).first()
        data.nombres_completos = participante.nombres_completos
        data.sexo = participante.sexo
        data.telefono_contacto = participante.telefono_contacto
        data.monto = participante.monto
        data.numero_deposito = participante.numero_deposito
        self.session.add(data)
        self.session.commit()


    def delete(self, participante):
        data = ParticipanteData.query.filter_by(id = str(participante.id)).first()
        self.session.delete(data)
        self.session.commit()


    def find_by(self, participante_id):
        data = ParticipanteData.query.filter_by(id = str(participante_id)).first()
        return Participante(
                id = uuid.UUID(data.id),
                nombres_completos = data.nombres_completos,
                sexo = data.sexo,
                telefono_contacto = data.telefono_contacto,
                monto = data.monto,
                numero_deposito = data.numero_deposito)


    def find_all(self, inscripcion_id):
        data_list = ParticipanteData.query.filter_by(inscripcion_id = str(inscripcion_id)).all()
        return list(map(lambda data:
                Participante(
                    id = uuid.UUID(data.id),
                    nombres_completos = data.nombres_completos,
                    sexo = data.sexo,
                    telefono_contacto = data.telefono_contacto,
                    monto = data.monto,
                    numero_deposito = data.numero_deposito), data_list))

