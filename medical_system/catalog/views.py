import json # Importa o Modulo de JSON do Python [Nativa].
# Importa do Flask as Bibliotecas de Request, Jsonify(Para comunicação JSON),
# e Blueprint, que servirá para permitir a modularização do sistema.
# Abort é para tratamento de erro, em requisições (Erro 404, por exemplo.)
from flask import request, jsonify, Blueprint, abort
from flask import render_template
from flask import redirect, url_for
# Permite gerenciar os metodos GET, POST, PUT e DELETE através de métodos
from flask.views import MethodView
from medical_system import app, database, admin, login_manager #Importa do __init__ as variáveis app e database
#Importa os Modelos no arquivo models.py
#from medical_system.catalog.models import Produtos
from medical_system.catalog.forms import LoginForm #Formulário de Login
from medical_system.catalog.controllers import LoginControl, LogoutControl
from flask_admin.contrib.sqla import ModelView
from medical_system.catalog.models import Login, Medico, Endereco, Especialidade, Formacao, Contato
from flask_login import current_user

catalog = Blueprint('catalog', __name__)

@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404

@catalog.route('/sistema/', methods= ['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        doctor_name = "Dr. Josemar"
        return render_template('index.html', doctor_name= doctor_name)
    return redirect(url_for('catalog.login')), 302

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

@catalog.route('/sistema/logout/')
@catalog.route('/logout/')
def logout():
    if current_user.is_authenticated:
        LogoutControl()
    return redirect(url_for('catalog.login')), 302

@catalog.route('/ajax-login', methods=['POST'])
def ajax_login()

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
