import os
from app import create_app, db
from flask_migrate import Migrate, upgrade

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
    upgrade()
