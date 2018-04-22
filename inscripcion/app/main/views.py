from flask import render_template
from . import main

site = {
        'title': 'Encuentro Carismático Católico Ecuatoriano Juvenil 2018',
        'description': 'XXXII Encuentro Carismático Católico Ecuatoriano Juvenil Quito 2018',
        'facebook': 'https://www.facebook.com/eccejuquito2018',
        'instagram': 'https://www.instagram.com/eccejuquito'
        }

@main.route('/formulario', methods = ['GET'])
def formulario():
    return render_template('formulario.html', site = site), 200
