from flask import render_template
from . import auth
from .forms import LoginForm

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

@auth.route('/login')
def login():
    form = LoginForm()
    return render_template(
            'auth/login.html',
            site = site,
            form = form)
