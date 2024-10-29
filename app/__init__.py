from flask import Flask, g
from .app_factory import create_app
from .db_connect import close_db, get_db

app = create_app()
app.secret_key = 'your-secret'  # Replace with an environment variable

# Register Blueprints
from app.blueprints.loan_amortization import loan_amortization
from app.blueprints.loan_amortization_detail import loan_amortization_detail
from app.blueprints.grades import grades

app.register_blueprint(loan_amortization)
app.register_blueprint(loan_amortization_detail)
app.register_blueprint(grades)

from . import routes

@app.before_request
def before_request():
    g.db = get_db()

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)