from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

csrf = CSRFProtect(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import views, models
