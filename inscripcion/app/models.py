from flask_login import UserMixin
from . import db
from . import login_manager

class InscripcionData(db.Model):
    __tablename__ = 'inscripciones'
    id = db.Column(db.String, primary_key = True)
    localidad = db.Column(db.String(200), nullable = False)
    servidor = db.Column(db.String(200), nullable = False)
    monto = db.Column(db.Numeric(8,2))
    fecha = db.Column(db.Date)
    comprobante_uri = db.Column(db.String(500))
    administradores = db.Column(db.String(500))

class ParticipanteData(db.Model):
    __tablename__ = 'participantes'
    id = db.Column(db.String, primary_key = True)
    nombres_completos = db.Column(db.String(200), nullable = False)
    sexo = db.Column(db.String(1), nullable = False)
    telefono_contacto = db.Column(db.String(15))
    inscripcion_id = db.Column(db.String, db.ForeignKey('inscripciones.id'))
    monto = db.Column(db.Numeric(8,2))
    numero_deposito = db.Column(db.String(64))
    fecha_inscripcion = db.Column(db.Date)

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key = True)
    nombre_usuario = db.Column(db.String(64), unique = True, index = True)
    readable_name = db.Column(db.String(128))
    hashed_password = db.Column(db.String(128))

@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(int(usuario_id))
