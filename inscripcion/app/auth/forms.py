from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class LoginForm(FlaskForm):
    nombre_usuario = StringField('Nombre de usuario')
    clave = PasswordField('Clave')
    iniciar = SubmitField('Iniciar')
