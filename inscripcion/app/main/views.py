from flask import render_template, redirect, url_for, session
from flask_login import login_required
from . import main
from .forms import InscripcionForm, ParticipanteForm
from domain.models import Inscripcion, Participante
from app.repositories import InscripcionRepository, ParticipanteRepository
from app import db, feature
import uuid

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

inscripcion_repository = InscripcionRepository(db.session)
participante_repository = ParticipanteRepository(db.session)

@main.route('/inscripciones/<id>')
@login_required
def show_inscripcion(id):
    return render_template('show_inscripcion.html',
            feature = feature,
            inscripcion = inscripcion_repository.find_by(id),
            site = site)

@main.route('/inscripciones')
@login_required
def index_inscripcion():
    return render_template('index_inscripcion.html',
            inscripciones = inscripcion_repository.find_all(),
            site = site)


@main.route('/inscripciones/new', methods = ['GET', 'POST'])
@login_required
def create_inscripcion():
    form = InscripcionForm()
    if form.validate_on_submit():
        inscripcion = Inscripcion(
                id = uuid.uuid1(),
                localidad = form.localidad.data,
                servidor = form.servidor.data,
                monto = form.monto.data,
                fecha = form.fecha.data)

        if feature.is_enabled("COMPROBANTE_PAGO"):
            inscripcion.comprobante_uri = form.comprobante_uri.data.filename

        inscripcion_repository.add(inscripcion)
        return redirect(url_for('main.index_inscripcion'))

    return render_template('save_inscripcion.html',
            feature = feature,
            site = site,
            form = form)

@main.route('/inscripciones/<id>/edit' , methods = ['GET', 'POST'])
@login_required
def edit_inscripcion(id):
    form = InscripcionForm()
    if form.validate_on_submit():
        inscripcion = Inscripcion(
                id = id,
                localidad = form.localidad.data,
                servidor = form.servidor.data,
                monto = form.monto.data,
                fecha = form.fecha.data)

        if feature.is_enabled("COMPROBANTE_PAGO"):
            inscripcion.comprobante_uri = form.comprobante_uri.data.filename

        inscripcion_repository.update(inscripcion)
        return redirect(url_for('main.index_inscripcion'))

    inscripcion = inscripcion_repository.find_by(id)
    form.localidad.data = inscripcion.localidad
    form.servidor.data = inscripcion.servidor
    form.monto.data = inscripcion.monto
    form.fecha.data = inscripcion.fecha

    # TODO: create a google drive client to fetch file
    if feature.is_enabled("COMPROBANTE_PAGO"):
        comprobante_file = open("comprobante.jpg", "w+")
        comprobante_file.close()
        form.comprobante_uri.data = comprobante_file

    return render_template('save_inscripcion.html',
            feature = feature,
            form = form,
            site = site)

@main.route('/inscripciones/<inscripcion_id>/participantes')
@login_required
def index_participante(inscripcion_id):
    return render_template('index_participante.html',
            inscripcion_id = inscripcion_id,
            participantes = participante_repository.find_all(inscripcion_id),
            site = site)

@main.route('/inscripciones/<inscripcion_id>/participantes/<participante_id>')
@login_required
def show_participante(inscripcion_id, participante_id):
    return render_template('show_participante.html',
            inscripcion_id = inscripcion_id,
            participante = participante_repository.find_by(participante_id),
            site = site)

@main.route('/inscripciones/<inscripcion_id>/participantes/new', methods=['GET', 'POST'])
@login_required
def create_participante(inscripcion_id):
    form = ParticipanteForm()
    if form.validate_on_submit():
        participante = Participante(
                id = uuid.uuid1(),
                nombres_completos = form.nombres_completos.data,
                sexo = form.sexo.data,
                telefono_contacto = form.telefono_contacto.data)

        participante_repository.add(participante, inscripcion_id)
        return redirect(url_for(
            'main.index_participante',
            inscripcion_id = inscripcion_id))

    return render_template('save_participante.html',
            form = form,
            site = site)

@main.route('/inscripciones/<inscripcion_id>/participantes/<participante_id>/edit' , methods = ['GET', 'POST'])
@login_required
def edit_participante(inscripcion_id, participante_id):
    form = ParticipanteForm()
    if form.validate_on_submit():
        participante = Participante(
                id = participante_id,
                nombres_completos = form.nombres_completos.data,
                sexo = form.sexo.data,
                telefono_contacto = form.telefono_contacto.data)

        participante_repository.update(participante)
        return redirect(url_for('main.index_participante',
            inscripcion_id = inscripcion_id))

    participante = participante_repository.find_by(participante_id)
    form.nombres_completos.data = participante.nombres_completos
    form.sexo.data = participante.sexo
    form.telefono_contacto.data = participante.telefono_contacto

    return render_template('save_participante.html',
            form = form,
            site = site)
