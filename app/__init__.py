
from flask import Flask
import time

from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change_this_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/ipcm'
# db = SQLAlchemy(app)

login_manager = LoginManager(app)

# Metadata and runtime context
app.config['SERVICE_NAME'] = 'ipcm-orange-offline'
app.config['VERSION'] = '0.1.0'
app.start_time = time.time()

# Utilisateur simulé pour le mode hors-ligne
class FakeUser:
    def __init__(self, username='Invité'):
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
        self.id = 1

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return FakeUser()




from . import routes
# Enregistre les gestionnaires d'erreurs (404/500)
from . import errors

if __name__ == '__main__':
    app.run(debug=True)
