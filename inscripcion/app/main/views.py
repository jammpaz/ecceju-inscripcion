from flask import render_template
from . import main

@main.route('/formulario', methods = ['GET'])
def formulario():
    return render_template('formulario.html'), 200
