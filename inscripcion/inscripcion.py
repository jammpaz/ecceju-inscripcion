import os
import click
from app import create_app, db, mail
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
@click.argument('email')
@click.password_option()
def create_user(name, email, password):
    """Create a new persistent user"""
    from app.email import send_email
    hashed_password = PasswordManager(password).hash()
    usuario = Usuario(
            nombre_usuario = email,
            readable_name = name,
            hashed_password = hashed_password
            )
    db.session.add(usuario)
    db.session.commit()

    send_email(
            email,
            'Una cuenta a sido creada para ti',
            'email/created_account',
            name = name,
            username = email,
            password = password,
            contact_email = os.getenv('ECCEJU_MAIL_SENDER')
            )


@app.shell_context_processor
def make_shell_context():
    return dict(
                db = db,
                Usuario=Usuario,
                InscripcionData=InscripcionData,
                ParticipanteData=ParticipanteData
            )
