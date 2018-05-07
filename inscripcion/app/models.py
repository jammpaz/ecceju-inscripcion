from . import db

class InscripcionData(db.Model):
    __tablename__ = 'inscripciones'
    id = db.Column(db.String, primary_key = True)
    localidad = db.Column(db.String(200), nullable = False)
    servidor = db.Column(db.String(200), nullable = False)
    monto = db.Column(db.Numeric(8,2))
    fecha = db.Column(db.Date)
    comprobante_uri = db.Column(db.String(500))
