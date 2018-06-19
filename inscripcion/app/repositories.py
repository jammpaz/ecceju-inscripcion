import uuid
from datetime import datetime
from app.models import InscripcionData, ParticipanteData
from domain.models import Inscripcion, Participante

class InscripcionRepository:
    def __init__(self, session):
        self.session = session

    def add(self, inscripcion):
        administradores_string = ','.join(inscripcion.administradores)
        data = InscripcionData(
                id = str(inscripcion.id),
                localidad = inscripcion.localidad,
                servidor = inscripcion.servidor,
                fecha = datetime.strptime(inscripcion.fecha, '%Y-%m-%d'),
                comprobante_uri = inscripcion.comprobante_uri,
                administradores = administradores_string)
        self.session.add(data)
        self.session.commit()

    def update(self, inscripcion):
        data = InscripcionData.query.filter_by(id = str(inscripcion.id)).first()
        data.localidad = inscripcion.localidad
        data.servidor = inscripcion.servidor
        data.fecha = datetime.strptime(inscripcion.fecha, '%Y-%m-%d')
        data.comprobante_uri = inscripcion.comprobante_uri
        self.session.add(data)
        self.session.commit()

    def find_by(self, inscripcion_id):
        data = InscripcionData.query.filter_by(id = str(inscripcion_id)).first()
        administradores = data.administradores.split(',')
        return Inscripcion(
                id = data.id,
                localidad = data.localidad,
                servidor = data.servidor,
                fecha = data.fecha,
                comprobante_uri = data.comprobante_uri,
                administradores = administradores)

    def find_by_id_and_admin(self, inscripcion_id, admin):
        inscripcion = self.find_by(inscripcion_id)
        if admin in inscripcion.administradores:
            return inscripcion
        else:
            return None

    def find_all(self):
        data_list = InscripcionData.query.all()
        return list(map(lambda data:
                Inscripcion(id = data.id,
                    localidad = data.localidad,
                    servidor = data.servidor,
                    fecha = data.fecha,
                    comprobante_uri = data.comprobante_uri,
                    administradores = data.administradores.split(',')), data_list))

    def find_all_by_admin(self, admin):
        inscripciones = self.find_all()
        return list(filter(lambda i: admin in i.administradores, inscripciones))


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
                fecha_inscripcion = participante.fecha_inscripcion,
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
        data.fecha_inscripcion = participante.fecha_inscripcion
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
                fecha_inscripcion = data.fecha_inscripcion,
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
                    fecha_inscripcion = data.fecha_inscripcion,
                    numero_deposito = data.numero_deposito), data_list))

