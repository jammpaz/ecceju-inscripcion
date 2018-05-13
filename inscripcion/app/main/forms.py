from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, FileField, DateField

class InscripcionForm(FlaskForm):
    localidad = StringField('Nombre de la Localidad')
    servidor = StringField('Nombre del servidor/a')
    monto = DecimalField('Monto cancelado (USD)')
    fecha = StringField('Fecha de pago')
    comprobante_uri = FileField('Comprobante de pago')

class ParticipanteForm(FlaskForm):
    nombres_completos = StringField('Nombres completos')
    sexo = StringField('Sexo')
    telefono_contacto = StringField('Telefono de contacto')
