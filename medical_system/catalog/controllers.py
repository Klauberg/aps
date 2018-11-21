from medical_system.catalog.models import Login, Paciente, Pessoa, Medico, Estadia, Prioridade, Quarto
from flask_login import login_user, logout_user, current_user
from medical_system import database
from flask import flash

class LoginControl():
    def __init__(self, request_method=None, form=None):
        self.method = request_method
        self.form = form

    def auth_methods (self):
        if self.method == 'POST' and self.form.validate():
            user = Login.query.filter_by(login=self.form.usuario.data).first()
            if user and (user.password == self.form.senha.data):
                user_id = Login.query.get(user.id_login)
                login_user(user_id)
                return True
            else:
                flash("Usuário ou Senha Inválido(a)")

class LogoutControl():
    def __init__ (self):
        logout_user()

class Doctor():
    def __init__(self):
            medico = Medico.query.filter_by(id_login=int(current_user.get_id())).first()
            pessoa = Pessoa.query.filter_by(id_pessoa=medico.id_pessoa).first()
            if pessoa:
                self.name = str(pessoa.nome)
            else:
                self.name = "Sem Nome"


class Pacientes():

    def __init__(self):
        self.paciente = database.session.query(Pessoa.nome, Estadia.id_quarto, Prioridade.doenca).filter(Pessoa.id_pessoa == Paciente.id_pessoa)
        print(self.paciente)
