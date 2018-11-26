from flask import Flask #Importa o flask
from flask_sqlalchemy import SQLAlchemy #Importa o SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__) #Cria uma instância do flask
app.config.from_pyfile('config.py') #Configura, através de um arquivo Externo
csrf = CSRFProtect(app)
database = SQLAlchemy(app) #Configura o SQLAlchemy conforme as configurações
admin = Admin(app)
login_manager = LoginManager(app)
login_manager.init_app(app)

# A Importação é realizada aqui, pois primeiro o objeto precisa ser instanciado
# para que models funcionem
from medical_system.catalog.views import catalog #Importa BluePrint
from medical_system.catalog import models

app.register_blueprint(catalog) #Registra o BluePrint
database.create_all() #Permite a criação das tabelas, caso elas não existam no banco
