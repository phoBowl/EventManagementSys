from flask import Flask
from model.client import ems_system, user_manager_system
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'This-is-a-secret-key-6789'

system = ems_system()
user_manager = user_manager_system()
# Login manager stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return user_manager.get_user_by_id(user_id)
