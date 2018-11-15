from flask import Flask #Importa o flask
from flask_sqlalchemy import SQLAlchemy #Importa o SQLAlchemy

app = Flask(__name__) #Cria uma instância do flask
app.config.from_pyfile('config.py') #Configura, através de um arquivo Externo

database = SQLAlchemy(app) #Configura o SQLAlchemy conforme as configurações

# A Importação é realizada aqui, pois primeiro o objeto precisa ser instanciado
# para que models funcionem
from medical_system.catalog.views import catalog #Importa BluePrint
from medical_system.catalog import models

app.register_blueprint(catalog) #Registra o BluePrint
database.create_all() #Permite a criação das tabelas no Banco.
