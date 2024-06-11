from flask import Flask
from project.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.school_details_blueprint import school_details_blueprint

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
app.register_blueprint(school_details_blueprint)

from app import routes