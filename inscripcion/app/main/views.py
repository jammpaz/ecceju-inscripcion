from flask import render_template, redirect, url_for, session
from flask_login import login_required, current_user
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
        'logout': {
            'name': 'Salir',
            },
        'inscripciones': {
            'name': 'Inscripciones',
            },
        'home': {
            'url': '/'
            },
        'ecceju-urls': {
                'programacion': 'https://ecceju.rccec.org/programacion',
                'ministerios': 'https://ecceju.rccec.org/ministerios',
                'musica': 'https://ecceju.rccec.org/musica',
                'inscripciones': 'https://inscripciones.ecceju.rccec.org',
                'acerca-de': 'https://ecceju.rccec.org/about/',
            }
        }

inscripcion_repository = InscripcionRepository(db.session)
participante_repository = ParticipanteRepository(db.session)


@main.route('/')
def index():
    return redirect(url_for('auth.login'))


@main.route('/inscripciones/<id>')
@login_required
def show_inscripcion(id):
    inscripcion = inscripcion_repository.find_by(id)
    if not inscripcion.is_managed_by(current_user.nombre_usuario):
        return render_template('401.html', site = site), 401

    return render_template('show_inscripcion.html',
            feature = feature,
            inscripcion = inscripcion,
            site = site)

@main.route('/inscripciones')
@login_required
def index_inscripcion():
    inscripciones = inscripcion_repository.find_all_by_admin(current_user.nombre_usuario)
    if not inscripciones:
        return render_template('401.html', site = site), 401

    return render_template('index_inscripcion.html',
            inscripciones = inscripciones,
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
                fecha = form.fecha.data)

        if feature.is_enabled("COMPROBANTE_PAGO"):
            inscripcion.comprobante_uri = form.comprobante_uri.data.filename

        inscripcion_repository.update(inscripcion)
        return redirect(url_for('main.index_inscripcion'))

    inscripcion = inscripcion_repository.find_by(id)
    if not inscripcion.is_managed_by(current_user.nombre_usuario):
        return render_template('401.html', site = site), 401

    form.localidad.data = inscripcion.localidad
    form.servidor.data = inscripcion.servidor
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
    inscripcion = inscripcion_repository.find_by(inscripcion_id)
    if not inscripcion.is_managed_by(current_user.nombre_usuario):
        return render_template('401.html', site = site), 401
    participantes = participante_repository.find_all(inscripcion_id)
    inscripcion = inscripcion_repository.find_by(inscripcion_id)
    inscripcion.participantes = participantes

    return render_template('index_participante.html',
            inscripcion_id = inscripcion_id,
            participantes = participantes,
            monto_total = inscripcion.total_amount(),
            site = site)

@main.route('/inscripciones/<inscripcion_id>/participantes/<participante_id>')
@login_required
def show_participante(inscripcion_id, participante_id):
    inscripcion = inscripcion_repository.find_by(inscripcion_id)
    if not inscripcion.is_managed_by(current_user.nombre_usuario):
        return render_template('401.html', site = site), 401

    return render_template('show_participante.html',
            inscripcion_id = inscripcion_id,
            participante = participante_repository.find_by(participante_id),
            site = site)

@main.route('/inscripciones/<inscripcion_id>/participantes/new', methods=['GET', 'POST'])
@login_required
def create_participante(inscripcion_id):
    inscripcion = inscripcion_repository.find_by(inscripcion_id)
    if not inscripcion.is_managed_by(current_user.nombre_usuario):
        return render_template('401.html', site = site), 401

    form = ParticipanteForm()
    if form.validate_on_submit():
        participante = Participante(
                id = uuid.uuid1(),
                nombres_completos = form.nombres_completos.data,
                sexo = form.sexo.data,
                telefono_contacto = form.telefono_contacto.data,
                monto = form.monto.data,
                numero_deposito = form.numero_deposito.data)

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
    inscripcion = inscripcion_repository.find_by(inscripcion_id)
    if not inscripcion.is_managed_by(current_user.nombre_usuario):
        return render_template('401.html', site = site), 401

    form = ParticipanteForm()
    if form.validate_on_submit():
        participante = Participante(
                id = participante_id,
                nombres_completos = form.nombres_completos.data,
                sexo = form.sexo.data,
                telefono_contacto = form.telefono_contacto.data,
                monto = form.monto.data,
                numero_deposito = form.numero_deposito.data)

        participante_repository.update(participante)
        return redirect(url_for('main.index_participante',
            inscripcion_id = inscripcion_id))

    participante = participante_repository.find_by(participante_id)

    form.nombres_completos.data = participante.nombres_completos
    form.sexo.data = participante.sexo
    form.telefono_contacto.data = participante.telefono_contacto
    form.monto.data = float('0.00') if participante.monto is None else float(participante.monto)
    form.numero_deposito.data = participante.numero_deposito

    return render_template('save_participante.html',
            form = form,
            site = site)
