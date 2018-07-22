from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, FileField, DateField, SelectField
from wtforms.validators import DataRequired

class InscripcionForm(FlaskForm):
    localidad = StringField('Nombre de la Localidad')
    servidor = StringField('Nombre del servidor/a')
    fecha = StringField('Fecha de pago')
    comprobante_uri = FileField('Comprobante de pago')

class ParticipanteForm(FlaskForm):
    nombres_completos = StringField('Nombres completos', validators = [DataRequired()])
    sexo = SelectField('Sexo', choices = [( 'H', 'Hombre' ), ( 'M', 'Mujer' )])
    telefono_contacto = StringField('Telefono de contacto')
    monto = DecimalField('Monto cancelado (USD)', validators = [DataRequired()])
    fecha_inscripcion = StringField('Fecha de inscripcion')
    numero_deposito = StringField('Número de depósito', validators = [DataRequired()])
