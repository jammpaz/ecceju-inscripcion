from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import LoginForm
from app.models import Usuario
from utils.security import PasswordManager

site = {
        'title': 'Inscripciones ECCEJU 2018',
        'description': 'XXXII Encuentro Carismático Católico Ecuatoriano Juvenil Quito 2018',
        'facebook': 'https://www.facebook.com/eccejuquito2018',
        'instagram': 'https://www.instagram.com/eccejuquito',
        'formulario': {
            'name': 'Inscripciones',
            'url': '/inscripciones'
            },
        'home': {
            'name': 'Inicio',
            'url': '/'
            }
        }


@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(
                nombre_usuario = form.nombre_usuario.data
                ).first()

        if usuario is not None and PasswordManager(
                form.clave.data).check_with(usuario.hashed_password):
            remember_session = False
            login_user(usuario, remember_session)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index_inscripcion')
            return redirect(next)

        flash('Credenciales incorrectas')
    return render_template(
            'auth/login.html',
            site = site,
            form = form)

@auth.route('/logout')
@login_required #TODO: test this requirement
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
