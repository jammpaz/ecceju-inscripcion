from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired

class PreventaCamisetaForm(FlaskForm):
    nombres_completos = StringField('Nombres completos', validators = [DataRequired()])
    localidad = StringField('Localidad', validators = [DataRequired()])
    color = SelectField('Color', choices = [( 'blanco', 'Blanco' ), ( 'negro', 'Negro' )])
    talla = SelectField('Talla', choices = [('34', 'Talla 34'), ('36', 'Talla 36'), ('38', 'Talla 38'), ('40', 'Talla 40')])
    cantidad = IntegerField('Cantidad')
    fecha_deposito = DateField('Fecha de depósito')
    numero_deposito = StringField('Número de depósito', validators = [DataRequired()])
