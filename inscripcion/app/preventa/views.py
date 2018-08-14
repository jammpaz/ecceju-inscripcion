from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import preventa
from .forms import PreventaCamisetaForm;
from domain.models import PreventaCamiseta
from app.repositories import PreventaCamisetaRepository
from app import db, preventa_camisetas_admin
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
        'preventa': {
            'name': 'Preventa',
            },
        'home': {
            'url': 'https://www.rccec.org',
            'name': 'Inicio'
            },
        'ecceju-urls': {
                'programacion': 'https://ecceju.rccec.org/programacion',
                'ministerios': 'https://ecceju.rccec.org/ministerios',
                'musica': 'https://ecceju.rccec.org/musica',
                'inscripciones': 'https://inscripciones.ecceju.rccec.org',
                'acerca-de': 'https://ecceju.rccec.org/about/',
            }
        }

preventa_camiseta_repository = PreventaCamisetaRepository(db.session)


@preventa.route('/new', methods = ['GET', 'POST'])
def create_preventa_camiseta():
    form = PreventaCamisetaForm()
    if form.validate_on_submit():
        preventa_camiseta = PreventaCamiseta(
                    id = uuid.uuid1(),
                    nombres_completos = form.nombres_completos.data,
                    localidad = form.localidad.data,
                    color = form.color.data,
                    talla = form.talla.data,
                    cantidad = form.cantidad.data,
                    fecha_deposito = form.fecha_deposito.data,
                    numero_deposito = form.numero_deposito.data)
        preventa_camiseta_repository.add(preventa_camiseta)
        flash('Tu pedido de camiseta ha sido enviada satisfactoriamente!', 'green')
        return redirect(url_for('preventa.create_preventa_camiseta'))

    flash_errors(form)
    return render_template(
            'preventa/save_preventa_camiseta.html',
            site = site,
            form = form
            )

@preventa.route('/')
@login_required
def list_preventa_camisetas():
    if not current_user.nombre_usuario in preventa_camisetas_admin['data']:
            return render_template('403.html', site = site), 403

    return render_template(
            'preventa/list_preventa_camiseta.html',
            preventas = preventa_camiseta_repository.find_all(),
            site = site
            )


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error en el campo: %s - %s" % (
                getattr(form, field).label.text,
                error
                ), 'red')
