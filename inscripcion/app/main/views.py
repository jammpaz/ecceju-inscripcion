from flask import render_template, redirect, url_for, session
from . import main
from .forms import InscripcionForm

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

@main.route('/formulario', methods = ['GET', 'POST'])
def formulario():
    form = InscripcionForm()
    print("{}".format(form.localidad.data))
    if form.validate_on_submit():
        return redirect(url_for('main.formulario'))
    return render_template('formulario.html',
            site = site,
            form = form)
