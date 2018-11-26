from medical_system.catalog.models import Login, Paciente, Pessoa, Medico, Estadia, Prioridade, Quarto, Contato, Endereco, Visita
from flask_login import login_user, logout_user, current_user
from medical_system import database
from flask import flash, jsonify
from medical_system.catalog.forms import PacienteForm
from sqlalchemy import func
import json

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
        medico = Medico.query.filter_by(id_login=int(current_user.get_id())).first_or_404()
        paciente_query = database.session.query(Pessoa.nome, Contato.nr_emergencia, Contato.nr_telefone, Paciente.id_paciente, Paciente.id_medico).filter(Pessoa.id_pessoa==Paciente.id_pessoa).filter(Contato.id_contato==Pessoa.id_contato).all()
        self.paciente = []
        for pessoa in paciente_query:
            if pessoa[4] == medico.id_medico:
                self.paciente.append(pessoa)

class Visitas():
    def __init__(self):
        medico = Medico.query.filter_by(id_login=int(current_user.get_id())).first_or_404()
        visita_query = database.session.query(Pessoa.nome, Visita.de_estado, Visita.dt_visita, Visita.id_visita, Paciente.id_medico).filter(Pessoa.id_pessoa==Paciente.id_pessoa).filter(Visita.id_paciente==Paciente.id_paciente).filter(Estadia.id_paciente==Paciente.id_paciente).all()
        self.visitas = []
        for visita in visita_query:
            if visita[4] == medico.id_medico:
                self.visitas.append(visita)

class ViewPaciente():
    def __init__(self, id):
        paciente = Paciente.query.filter_by(id_paciente = id).first()
        pessoa = Pessoa.query.filter_by(id_pessoa=paciente.id_pessoa).first()
        contato = Contato.query.filter_by(id_contato=pessoa.id_contato).first()
        endereco = Endereco.query.filter_by(id_endereco=pessoa.id_endereco).first()
        self.nome = pessoa.nome
        self.cpf = pessoa.cpf
        self.rg = pessoa.rg
        self.nascimento = pessoa.nascimento
        self.telefone = contato.nr_telefone
        self.emergencia = contato.nr_emergencia
        self.email = contato.email
        self.numero = endereco.numero
        self.cep = endereco.cep
        self.cidade = endereco.cidade
        self.estado = endereco.estado
        self.pais = endereco.pais
        self.medico = paciente.id_medico

class ViewVisita():
    def __init__(self, id):
        visita = Visita.query.filter_by(id_visita=id).first()
        paciente = Paciente.query.filter_by(id_paciente = visita.id_paciente).first()
        pessoa = Pessoa.query.filter_by(id_pessoa=paciente.id_pessoa).first()
        estadia = Estadia.query.filter_by(id_paciente=paciente.id_paciente).first()
        self.nome = pessoa.nome
        self.temperatura = visita.temperatura
        self.pressao = visita.pressao
        self.de_estado = visita.de_estado
        self.dt_visita = visita.dt_visita
        self.quarto = estadia.id_quarto
        self.bl_infeccao = estadia.bl_infeccao
        self.de_sintomas = estadia.de_sintomas
        self.dt_estadia = estadia.dt_estadia
        self.medico = visita.id_medico

class CadastroVisita():
    def __init__(self, request_method=None, form=None):
        self.method = request_method
        self.form = form

    def auth_methods(self):
        if self.method == 'POST':
            self.paciente = self.form['paciente']
            self.temperatura = self.form['temperatura']
            self.pressao = self.form['pressao']
            self.descricao_estado = self.form['descricao_estado']
            self.data_visita = self.form['visita']
            self.quarto = self.form['quarto']
            self.infeccao = self.form['infeccao']
            self.descricao_sintoma = self.form['descricao_sintoma']
            self.data_estadia = self.form['data_estadia']
            self.response = {}
            print(self.paciente)
            #Definição de Erros
            letraTemperatura = not(self.temperatura.isdigit()) and (self.temperatura != "")
            tamanhoTemperatura =  (len(self.temperatura) > 4) and (self.temperatura != "")
            letraPressao = not(self.pressao.isdigit()) and (self.pressao != "")
            tamanhoPressao =  (len(self.pressao) > 4) and (self.pressao != "")
            tamanhoDescEstado = (len(self.descricao_estado) > 350) or (len(self.descricao_estado) < 10)
            tamanhoDescSintoma = (len(self.descricao_sintoma) > 350) or (len(self.descricao_sintoma) < 10)
            check = tamanhoDescSintoma or tamanhoDescEstado or tamanhoPressao or letraPressao or tamanhoTemperatura or letraTemperatura
            self.response = {'status':'200',
                            'letratemp':letraTemperatura,
                            'tamanhotemp':tamanhoTemperatura,
                            'letrapressao':letraPressao,
                            'tamanhopressao':tamanhoPressao,
                            'tamanhodescestado':tamanhoDescEstado,
                            'tamanhodescsintoma':tamanhoDescSintoma,
                            'check':check}
            if check == False:
                pessoa = Paciente.query.filter_by(id_pessoa=self.paciente).first()
                if Estadia.query.filter_by(id_paciente=pessoa.id_paciente).first() != None:
                    visita = database.session.query(func.criaVisita(self.temperatura, self.pressao, self.descricao_estado, self.data_visita, pessoa.id_paciente, int(current_user.get_id()))).scalar()
                else:
                    estadia = database.session.query(func.criaEstadia(pessoa.id_paciente, self.quarto, self.infeccao, self.descricao_sintoma, self.data_estadia)).scalar()
                    visita = database.session.query(func.criaVisita(self.temperatura, self.pressao, self.descricao_estado, self.data_visita, pessoa.id_paciente, int(current_user.get_id()))).scalar()
                database.session.commit()
            return json.dumps(self.response)

class CadastroPaciente():
    def __init__(self, request_method=None, form=None):
        self.method = request_method
        self.form = form

    def auth_methods(self):
        if self.method == 'POST':
            self.nome = self.form['nome']
            self.cpf = self.form['cpf']
            self.rg = self.form['rg']
            self.nascimento = self.form['nascimento']
            self.telefone = self.form['telefone']
            self.emergencia = self.form['emergencia']
            self.email = self.form['email']
            self.cep = self.form['cep']
            self.numero = self.form['numero']
            self.cidade = self.form['cidade']
            self.estado = self.form['estado']
            self.pais = self.form['pais']
            self.response = {}
            #Definição de Erros
            campoVazio = False
            erroEmail = ("@" and "." not in self.email) and (self.email != "")
            letraCPF = not(self.cpf.isdigit()) and (self.cpf != "")
            letraRG = not(self.rg.isdigit()) and (self.rg != "")
            letraTelefone = not(self.telefone.isdigit())
            letraEmergencia = not(self.emergencia.isdigit())
            letraNumero = not(self.numero.isdigit())
            letraCep = not(self.cep.isdigit())
            tamanhoNome = (len(self.nome) < 4) or (len(self.nome) > 240)
            tamanhoCPF =  (len(self.cpf) != 11) and (self.cpf != "")
            tamanhoRG = (len(self.rg) > 10)
            tamanhoTelefone = (len(self.telefone) < 10) or (len(self.telefone) > 14)
            tamanhoEmergencia = (len(self.emergencia) < 10) or (len(self.emergencia) > 14)
            tamanhoEmail = (len(self.email) > 200)
            tamanhoCep = (len(self.cep) < 8) or (len(self.cep) > 12)
            tamanhoNumero = (len(self.numero) < 1) or (len(self.numero) > 45)
            tamanhoCidade = (len(self.cidade) > 90)
            tamanhoEstado = (len(self.estado) > 90)
            tamanhoPais = (len(self.pais) > 90)
            check = erroEmail or letraCPF or letraRG or letraTelefone or letraEmergencia or letraNumero or letraCep or tamanhoNome or tamanhoCPF or tamanhoRG or tamanhoTelefone or tamanhoEmergencia or tamanhoEmail or tamanhoCep or tamanhoNumero or tamanhoCidade or tamanhoEstado or tamanhoPais
            if (not self.nome) or (not self.nascimento) or (not self.telefone) or (not self.emergencia) or (not self.cep) or (not self.numero) or (not self.cidade) or (not self.pais):
                campoVazio = True
            self.response = {'status':'200',
                            'email':erroEmail,
                            'letracpf':letraCPF,
                            'letrarg':letraRG,
                            'letratel':letraTelefone,
                            'letraemg':letraEmergencia,
                            'letracep':letraCep,
                            'letranum':letraNumero,
                            'tamanhonome':tamanhoNome,
                            'tamanhocpf':tamanhoCPF,
                            'tamanhorg':tamanhoRG,
                            'tamanhotelefone':tamanhoTelefone,
                            'tamanhoemergencia':tamanhoEmergencia,
                            'tamanhoemail':tamanhoEmail,
                            'tamanhocep':tamanhoCep,
                            'tamanhonumero':tamanhoNumero,
                            'tamanhocidade': tamanhoCidade,
                            'tamanhoestado': tamanhoEstado,
                            'tamanhopais': tamanhoPais,
                            'check':check}
            if check == False:
                teste = database.session.query(func.criaPaciente(self.telefone,self.emergencia,self.email,self.numero,self.cep,self.cidade,self.estado,self.pais,self.nome,self.cpf,self.rg,self.nascimento,int(current_user.get_id()))).scalar()
                database.session.commit()
            return json.dumps(self.response)

class VerificaAutorizacao():
    def __init__(self, id):
        paciente = Paciente.query.filter_by(id_paciente=id).first()
        pessoa = Pessoa.query.filter_by(id_pessoa=paciente.id_pessoa).first()
        contato = Contato.query.filter_by(id_contato=pessoa.id_contato).first()
        endereco = Endereco.query.filter_by(id_endereco=pessoa.id_endereco).first()
        estadias = Estadia.query.filter_by(id_paciente=id).all()
        prioridades = Prioridade.query.filter_by(id_paciente=id).all()
        visitas = Visita.query.filter_by(id_paciente=id).all()
        if paciente.id_medico == int(current_user.get_id()):
            if estadias != None:
                for estadia in estadias:
                    database.session.delete(estadia)
            if prioridades != None:
                for prioridade in prioridades:
                    database.session.delete(prioridade)
            if visitas != None:
                for visita in visitas:
                    database.session.delete(visita)
            database.session.delete(paciente)
            database.session.delete(pessoa)
            database.session.delete(contato)
            database.session.delete(endereco)
            database.session.commit()
            database.session.close()
        else:
            return False

class DeletaVisita():
    def __init__(self, id):
        visita = Visita.query.filter_by(id_visita=id).first()
        estadias = Estadia.query.filter_by(id_paciente=visita.id_paciente).all()
        visitas = Visita.query.filter_by(id_paciente=visita.id_paciente).all()
        if visita.id_medico == int(current_user.get_id()):
            if estadias != None:
                for estadia in estadias:
                    database.session.delete(estadia)
            if visitas != None:
                for visita in visitas:
                    database.session.delete(visita)
            database.session.commit()
            database.session.close()
        else:
            return False

class EditarPaciente():
    def __init__(self, id, request_method, form):
        self.method = request_method
        self.form = form
        self.id = id

    def auth_methods(self):
        if self.method == 'POST':
            self.nome = self.form['nome']
            self.cpf = self.form['cpf']
            self.rg = self.form['rg']
            self.nascimento = self.form['nascimento']
            self.telefone = self.form['telefone']
            self.emergencia = self.form['emergencia']
            self.email = self.form['email']
            self.cep = self.form['cep']
            self.numero = self.form['numero']
            self.cidade = self.form['cidade']
            self.estado = self.form['estado']
            self.pais = self.form['pais']
            self.response = {}
            #Definição de Erros
            campoVazio = False
            erroEmail = ("@" and "." not in self.email) and (self.email != "")
            letraCPF = not(self.cpf.isdigit()) and (self.cpf != "")
            letraRG = not(self.rg.isdigit()) and (self.rg != "")
            letraTelefone = not(self.telefone.isdigit())
            letraEmergencia = not(self.emergencia.isdigit())
            letraNumero = not(self.numero.isdigit())
            letraCep = not(self.cep.isdigit())
            tamanhoNome = (len(self.nome) < 4) or (len(self.nome) > 240)
            tamanhoCPF =  (len(self.cpf) != 11) and (self.cpf != "")
            tamanhoRG = (len(self.rg) > 10)
            tamanhoTelefone = (len(self.telefone) < 10) or (len(self.telefone) > 14)
            tamanhoEmergencia = (len(self.emergencia) < 10) or (len(self.emergencia) > 14)
            tamanhoEmail = (len(self.email) > 200)
            tamanhoCep = (len(self.cep) < 8) or (len(self.cep) > 12)
            tamanhoNumero = (len(self.numero) < 1) or (len(self.numero) > 45)
            tamanhoCidade = (len(self.cidade) > 90)
            tamanhoEstado = (len(self.estado) > 90)
            tamanhoPais = (len(self.pais) > 90)
            check = erroEmail or letraCPF or letraRG or letraTelefone or letraEmergencia or letraNumero or letraCep or tamanhoNome or tamanhoCPF or tamanhoRG or tamanhoTelefone or tamanhoEmergencia or tamanhoEmail or tamanhoCep or tamanhoNumero or tamanhoCidade or tamanhoEstado or tamanhoPais
            if (not self.nome) or (not self.nascimento) or (not self.telefone) or (not self.emergencia) or (not self.cep) or (not self.numero) or (not self.cidade) or (not self.pais):
                campoVazio = True
            self.response = {'status':'200',
                            'email':erroEmail,
                            'letracpf':letraCPF,
                            'letrarg':letraRG,
                            'letratel':letraTelefone,
                            'letraemg':letraEmergencia,
                            'letracep':letraCep,
                            'letranum':letraNumero,
                            'tamanhonome':tamanhoNome,
                            'tamanhocpf':tamanhoCPF,
                            'tamanhorg':tamanhoRG,
                            'tamanhotelefone':tamanhoTelefone,
                            'tamanhoemergencia':tamanhoEmergencia,
                            'tamanhoemail':tamanhoEmail,
                            'tamanhocep':tamanhoCep,
                            'tamanhonumero':tamanhoNumero,
                            'tamanhocidade': tamanhoCidade,
                            'tamanhoestado': tamanhoEstado,
                            'tamanhopais': tamanhoPais,
                            'check':check}
            if check == False:
                x = database.session.query(func.editaPaciente(self.telefone,self.emergencia,self.email,self.numero,self.cep,self.cidade,self.estado,self.pais,self.nome,self.cpf,self.rg,self.nascimento,self.id)).scalar()
                database.session.commit()
            return json.dumps(self.response)

class EditarVisita():
    def __init__(self, id, request_method, form):
        self.method = request_method
        self.form = form
        self.id = id

    def auth_methods(self):
        if self.method == 'POST':
            self.paciente = self.form['paciente']
            self.temperatura = self.form['temperatura']
            self.pressao = self.form['pressao']
            self.descricao_estado = self.form['descricao_estado']
            self.data_visita = self.form['visita']
            self.quarto = self.form['quarto']
            self.infeccao = self.form['infeccao']
            self.descricao_sintoma = self.form['descricao_sintoma']
            self.data_estadia = self.form['data_estadia']
            self.response = {}
            print(self.paciente)
            #Definição de Erros
            letraTemperatura = not(self.temperatura.isdigit()) and (self.temperatura != "")
            tamanhoTemperatura =  (len(self.temperatura) > 4) and (self.temperatura != "")
            letraPressao = not(self.pressao.isdigit()) and (self.pressao != "")
            tamanhoPressao =  (len(self.pressao) > 4) and (self.pressao != "")
            tamanhoDescEstado = (len(self.descricao_estado) > 350) or (len(self.descricao_estado) < 10)
            tamanhoDescSintoma = (len(self.descricao_sintoma) > 350) or (len(self.descricao_sintoma) < 10)
            check = tamanhoDescSintoma or tamanhoDescEstado or tamanhoPressao or letraPressao or tamanhoTemperatura or letraTemperatura
            self.response = {'status':'200',
                            'letratemp':letraTemperatura,
                            'tamanhotemp':tamanhoTemperatura,
                            'letrapressao':letraPressao,
                            'tamanhopressao':tamanhoPressao,
                            'tamanhodescestado':tamanhoDescEstado,
                            'tamanhodescsintoma':tamanhoDescSintoma,
                            'check':check}
            if check == False:
                visita = Visita.query.filter_by(id_visita=self.id).first()
                estadia = Estadia.query.filter_by(id_paciente=visita.id_paciente,id_quarto=self.quarto)
                if estadia is not None:
                    estadia.bl_infeccao = self.infeccao
                    estadia.de_sintomas = self.descricao_sintoma
                    estadia.dt_estadia = self.data_estadia
                visita.temperatura = self.temperatura
                visita.pressao = self.pressao
                visita.de_estado = self.descricao_estado
                visita.dt_visita = self.data_visita
                database.session.commit()
                database.session.close()
            return json.dumps(self.response)
