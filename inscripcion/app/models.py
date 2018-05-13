from . import db

class InscripcionData(db.Model):
    __tablename__ = 'inscripciones'
    id = db.Column(db.String, primary_key = True)
    localidad = db.Column(db.String(200), nullable = False)
    servidor = db.Column(db.String(200), nullable = False)
    monto = db.Column(db.Numeric(8,2))
    fecha = db.Column(db.Date)
    comprobante_uri = db.Column(db.String(500))

class ParticipanteData(db.Model):
    __tablename__ = 'participantes'
    id = db.Column(db.String, primary_key = True)
    nombres_completos = db.Column(db.String(200), nullable = False)
    sexo = db.Column(db.String(1), nullable = False)
    telefono_contacto = db.Column(db.String(15))
    inscripcion_id = db.Column(db.String, db.ForeignKey('inscripciones.id'))
