from flask import render_template
from . import main

site = {
        'title': 'Inscripciones ECCEJU 2018',
        'description': 'XXXII Encuentro Carismático Católico Ecuatoriano Juvenil Quito 2018',
        'facebook': 'https://www.facebook.com/eccejuquito2018',
        'instagram': 'https://www.instagram.com/eccejuquito',
        'formulario': {
            'name': 'Inscripciones',
            'url': '/formulario'
            },
        'home': {
            'name': 'Inicio',
            'url': '/'
            }
        }

@main.route('/formulario', methods = ['GET'])
def formulario():
    return render_template('formulario.html', site = site), 200
