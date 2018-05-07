from datetime import datetime
from app.models import InscripcionData
from domain.models import Inscripcion

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

    def find_by(self, inscripcion_id):
        data = InscripcionData.query.filter_by(id = str(inscripcion_id)).first()
        return Inscripcion(
                id = data.id,
                localidad = data.localidad,
                servidor = data.servidor,
                monto = data.monto,
                fecha = data.fecha,
                comprobante_uri = data.comprobante_uri)



