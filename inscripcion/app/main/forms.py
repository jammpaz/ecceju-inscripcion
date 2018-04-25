from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, FileField

class InscripcionForm(FlaskForm):
    localidad = StringField('Nombre de la Localidad')
    servidor = StringField('Nombre del servidor/a')
    monto = DecimalField('Monto cancelado (USD)')
    comprobante_uri = FileField('Comprobante de pago')
    guardar = SubmitField('Guardar')
    enviar = SubmitField('Enviar')

