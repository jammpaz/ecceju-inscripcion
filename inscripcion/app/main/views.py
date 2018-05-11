from flask import render_template, redirect, url_for, session
from . import main
from .forms import InscripcionForm
from domain.models import Inscripcion, Participante
from app.repositories import InscripcionRepository
from app import db
import uuid

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

inscripcion_repository = InscripcionRepository(db.session)

@main.route('/inscripciones/<id>')
def show_inscripcion(id):
    inscripcion = inscripcion_repository.find_by(id)

    participante = Participante(
            id = uuid.uuid1(),
            nombres_completos = 'Isabel de las Mercedes',
            sexo = "Mujer",
            telefono_contacto = '5252525')

    inscripcion.add_participante(participante)

    return render_template('show_inscripcion.html',
            inscripcion = inscripcion,
            site = site)

@main.route('/inscripciones')
def index_inscripcion():
    return render_template('index_inscripcion.html',
            inscripciones = inscripcion_repository.find_all(),
            site = site)


@main.route('/inscripciones/<inscripcion_id>/participantes/<participante_id>')
def show_participante(inscripcion_id, participante_id):
    participante = Participante(
            id = participante_id,
            nombres_completos = 'Isabel de las Mercedes',
            sexo = "Mujer",
            telefono_contacto = '5252525')

    return render_template('show_participante.html',
            participante = participante,
            site = site)


@main.route('/inscripciones/new')
def new_inscripcion():
    form = InscripcionForm()

    return render_template('create_inscripcion.html',
            site = site,
            form = form)


@main.route('/inscripciones', methods = ['POST'])
def create_inscripcion():
    form = InscripcionForm()
    if form.validate_on_submit():
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = form.localidad.data,
                servidor = form.servidor.data,
                monto = form.monto.data,
                fecha = form.fecha.data,
                comprobante_uri = form.comprobante_uri.data.filename)
        inscripcion_repository.add(inscripcion)
        return redirect(url_for('main.index_inscripcion'))

    return render_template('create_inscripcion.html',
            site = site,
            form = form)
