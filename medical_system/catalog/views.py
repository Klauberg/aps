# Importa do Flask as Bibliotecas de Request, Jsonify(Para comunicação JSON),
# e Blueprint, que servirá para permitir a modularização do sistema.
# Abort é para tratamento de erro, em requisições (Erro 404, por exemplo.)
import datetime
from flask import request, jsonify, Blueprint, abort, session
from flask import render_template
from flask import redirect, url_for
# Permite gerenciar os metodos GET, POST, PUT e DELETE através de métodos
from flask.views import MethodView
from medical_system import app, database, admin, login_manager #Importa do __init__ as variáveis app e database
#Importa os Modelos no arquivo models.py
#from medical_system.catalog.models import Produtos
from medical_system.catalog.forms import LoginForm, PacienteForm, VisitaForm #Formulário de Login
from medical_system.catalog.controllers import LoginControl, LogoutControl, Doctor, Pacientes, ViewPaciente, CadastroPaciente, VerificaAutorizacao, EditarPaciente, Visitas, ViewVisita, CadastroVisita, DeletaVisita, EditarVisita
from flask_admin.contrib.sqla import ModelView
from medical_system.catalog.models import Login, Medico, Endereco, Especialidade, Formacao, Contato, Paciente, Pessoa, Estadia, Quarto
from flask_login import current_user

catalog = Blueprint('catalog', __name__)

#Metodos de Tratamento#
@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=20)
    session.modified = True
######################

######## Metodos de Paciente ########
@catalog.route('/paciente/cadastrar', methods=['GET', 'POST'])
def cadastro_paciente():
    if not current_user.is_authenticated: abort(404)
    paciente_form = PacienteForm(request.form)
    if request.method == 'POST':
        response = CadastroPaciente(request.method, request.form).auth_methods()
        return response
    return render_template('forms/criar_paciente.html', form=paciente_form)

@catalog.route('/paciente/editar/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id=None):
    if id == None or not current_user.is_authenticated: abort(404)
    paciente_form = PacienteForm(request.form)
    paciente_info = ViewPaciente(id)
    if request.method == 'POST':
        response = EditarPaciente(id,request.method, request.form).auth_methods()
        return response
    return render_template('forms/editar_paciente.html', form=paciente_form, paciente=paciente_info, id=id)

@catalog.route('/paciente/deletar/<int:id>')
def deletar_paciente(id=None):
    if id == None or not current_user.is_authenticated: abort(404)
    if VerificaAutorizacao(id) == False:
        abort(404)
    else:
        return redirect(url_for('catalog.index'))

@catalog.route('/paciente/<int:id>', methods=['GET', 'POST'])
def detalhes_paciente(id=None):
    if id==None or not current_user.is_authenticated: abort(404)
    paciente = ViewPaciente(id)
    if paciente.medico == int(current_user.get_id()):
        return render_template('forms/details_paciente.html',
                               nome_paciente=paciente.nome,
                               cpf_paciente=paciente.cpf,
                               rg_paciente=paciente.rg,
                               nascimento_paciente=paciente.nascimento,
                               cep_paciente=paciente.cep,
                               cidade_paciente=paciente.cidade,
                               estado_paciente=paciente.estado,
                               pais_paciente=paciente.pais,
                               telefone_paciente=paciente.telefone,
                               telefone2_paciente=paciente.emergencia,
                               email_paciente=paciente.email), 200
    else:
        abort(404)
#########################

######## Metodos de Visita ########
@catalog.route('/visita/cadastrar', methods=['GET', 'POST'])
def cadastro_visita():
    if not current_user.is_authenticated: abort(404)
    visita_form = VisitaForm(request.form)
    pessoas = []
    estadia = []
    pacientes = Paciente.query.filter_by(id_medico=int(current_user.get_id())).all()
    for p in pacientes:
        pessoas.append(Pessoa.query.filter_by(id_pessoa=p.id_pessoa).first())
    visita_form.paciente.choices = [(pessoa.id_pessoa, pessoa.nome) for pessoa in pessoas]
    visita_form.quarto.choices = [(estadias.id_quarto, estadias.id_quarto) for estadias in Quarto.query.all()]
    if request.method == 'POST':
        response = CadastroVisita(request.method, request.form).auth_methods()
        return response
    return render_template('forms/criar_visita.html', form=visita_form)

@catalog.route('/visita/editar/<int:id>', methods=['GET', 'POST'])
def editar_visita(id=None):
    if id == None or not current_user.is_authenticated: abort(404)
    visita_form = VisitaForm(request.form)
    visita_info = ViewVisita(id)
    pessoas = []
    estadia = []
    pacientes = Paciente.query.filter_by(id_medico=int(current_user.get_id())).all()
    for p in pacientes:
        pessoas.append(Pessoa.query.filter_by(id_pessoa=p.id_pessoa).first())
    visita_form.paciente.choices = [(pessoa.id_pessoa, pessoa.nome) for pessoa in pessoas]
    visita_form.quarto.choices = [(estadias.id_quarto, estadias.id_quarto) for estadias in Quarto.query.all()]
    if request.method == 'POST':
        response = EditarVisita(id,request.method, request.form).auth_methods()
        return response
    return render_template('forms/editar_visita.html', form=visita_form, visita=visita_info, id=id)

@catalog.route('/visita/deletar/<int:id>')
def deletar_visita(id=None):
    if id == None or not current_user.is_authenticated: abort(404)
    if DeletaVisita(id) == False:
        abort(404)
    else:
        return redirect(url_for('catalog.index'))

@catalog.route('/visita/<int:id>', methods=['GET', 'POST'])
def detalhes_visita(id=None):
    if id==None or not current_user.is_authenticated: abort(404)
    visita = ViewVisita(id)
    if visita.medico == int(current_user.get_id()):
        return render_template('forms/details_visita.html',
                               nome_paciente=visita.nome,
                               temperatura=visita.temperatura,
                               pressao=visita.pressao,
                               de_estado=visita.de_estado,
                               dt_visita=visita.dt_visita,
                               bl_infeccao=visita.bl_infeccao,
                               de_sintomas=visita.de_sintomas,
                               dt_estadia=visita.dt_estadia), 200
    else:
        abort(404)
#########################

#######Método Sistema########
@catalog.route('/sistema/', methods= ['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        doctor_name = f'Dr. {Doctor().name}'
        paciente = Pacientes()
        visita = Visitas()
        return render_template('index.html', doctor_name=doctor_name, paciente=paciente.paciente, visita=visita.visitas), 200
    return redirect(url_for('catalog.login')), 302
##############################

#### Método de Login  e Logout ####
@catalog.route('/', methods = ['GET', 'POST'])
@catalog.route('/login/', methods = ['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        login_form = LoginForm(request.form)
        if LoginControl(request.method, login_form).auth_methods() == True:
            return redirect(url_for('catalog.index')), 302
    else:
        return redirect(url_for('catalog.index')), 302
    return render_template('login.html', form = login_form), 200

@catalog.route('/logout/')
def logout():
    if current_user.is_authenticated:
        LogoutControl()
    return redirect(url_for('catalog.login')), 302
##############################


@login_manager.user_loader
def load_user(user_id):
    return Login.query.get(int(user_id))

class LoginView(ModelView):
    can_delete = False
    can_edit = True
    can_create = False
    page_size = 10
    column_exclude_list=['password']
    column_searchable_list = ['login']
    form_excluded_columns = ['password']
    edit_modal = True

#Database View (Para Login de ADMIN)
admin.add_view(LoginView(Login, database.session))
admin.add_view(ModelView(Medico, database.session))
admin.add_view(ModelView(Endereco, database.session))
admin.add_view(ModelView(Especialidade, database.session))
admin.add_view(ModelView(Formacao, database.session))
admin.add_view(ModelView(Contato, database.session))
#
