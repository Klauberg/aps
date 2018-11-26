from medical_system.database_connection import Connection

#CONFIGURAÇÕES
DEBUG = True
SQLALCHEMY_DATABASE_URI = Connection.url()
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "apsdumal"
