import os
import click
from app import create_app, db
from flask_migrate import Migrate, upgrade
from app.models import Usuario, InscripcionData, ParticipanteData
from utils.security import PasswordManager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity = 2).run(tests)

@app.cli.command()
def deploy():
    """Run database migrations"""
    upgrade()

@app.cli.command()
@click.argument('name')
@click.password_option()
def create_user(name, password):
    """Create a new persistent user"""
    hashed_password = PasswordManager(password).hash()
    usuario = Usuario(nombre_usuario = name,
            hashed_password = hashed_password)
    db.session.add(usuario)
    db.session.commit()


@app.shell_context_processor
def make_shell_context():
    return dict(
                db = db,
                PasswordManager = PasswordManager,
                Usuario=Usuario,
                InscripcionData=InscripcionData,
                ParticipanteData=ParticipanteData
            )
