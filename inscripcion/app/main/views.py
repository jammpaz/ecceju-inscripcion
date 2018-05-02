from flask import render_template, redirect, url_for, session
from . import main
from .forms import InscripcionForm
from domain.models import Inscripcion, Participante

site = {
        'title': 'Inscripciones ECCEJU 2018',
        'description': 'XXXII Encuentro Carismático Católico Ecuatoriano Juvenil Quito 2018',
        'facebook': 'https://www.facebook.com/eccejuquito2018',
        'instagram': 'https://www.instagram.com/eccejuquito',
        'formulario': {
            'name': 'Inscripciones',
            'url': '/inscripcion'
            },
        'home': {
            'name': 'Inicio',
            'url': '/'
            }
        }

@main.route('/inscripciones/<id>')
def show_inscripcion(id):
    inscripcion = Inscripcion(
            id,
            localidad = 'Quito',
            servidor = 'Conny Riera',
            monto = '150.00',
            fecha = '2018-08-01',
            comprobante_uri = 'https://s3.aws.com/comprobante.jpg')

    participante = Participante(nombres_completos = 'Isabel de las Mercedes',
            sexo = "Mujer",
            telefono_contacto = '5252525')

    inscripcion.addParticipante(participante)

    return render_template('show_inscripcion.html',
            inscripcion = inscripcion,
            site = site)

@main.route('/inscripcion', methods = ['POST'])
def edit_inscripcion():
    form = InscripcionForm()
    if form.validate_on_submit():
        return redirect(url_for('main.edit_inscripcion'))
    return render_template('inscripcion.html',
            site = site,
            form = form)
