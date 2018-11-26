from wtforms import Form
from wtforms import StringField
from wtforms import validators
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import DateField
from wtforms import TextField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms.fields.html5 import EmailField
from datetime import date

class LoginForm(Form):
    usuario = StringField('Usuário',
            [
                validators.length(min=5, max=15, message="Usuário ou Senha Inválido(a)")
            ]
            )
    senha = PasswordField('Senha')

class PacienteForm(Form):
    nome = StringField('Nome Completo',
                       [
                            validators.length(min=5, max=240, message="Erro: Tamanho do campo nome inválido."),
                            validators.Required(message="O campo de nome é requerido.")
                        ])
    cpf = StringField('CPF',
                      [
                            validators.length(min=11, max=11, message="Erro: Tamanho do CPF inválido")
                      ])
    rg = StringField('RG',
                     [
                            validators.length(min=5, max=10, message="Erro: Tamanho do RG é inválido")
                     ])
    nascimento = DateField('Data de Nascimento',
                           [
                                validators.Required(message="O campo de Nascimento é requerido.")
                           ], format="%Y-%m-%d")
    telefone = StringField('Telefone',
                           [
                               validators.length(min=10, max=14, message="Erro: Tamanho do Telefone inválido."),
                               validators.Required(message="O campo de Telefone é requerido.")
                           ])
    emergencia = StringField('Telefone de Emergencia',
                             [
                                 validators.length(min=10, max=14, message="Erro: Tamanho do Telefone de Emegência inválido."),
                                 validators.Required(message="O campo de Telefone de Emegência é requerido.")
                             ])
    email = EmailField('Email',
                       [
                           validators.length(max=200, message="Erro: Tamanho do E-mail inválido.")
                       ])
    cep = StringField('CEP',
                      [
                          validators.length(min=8, max=12, message="Erro: Tamanho do CEP inválido."),
                          validators.Required(message="O campo de CEP é requerido.")
                      ])
    numero = StringField('Numero',
                         [
                             validators.length(min=1, max=45, message="Erro: Tamanho do Número inválido."),
                             validators.Required(message="O campo de Número é requerido")
                         ])
    cidade = StringField('Cidade',
                         [
                             validators.length(max=90, message="Erro: Tamanho do campo Cidade inválido."),
                             validators.Required(message="O campo de Cidade é Requerido.")
                         ])
    estado = StringField('Estado',
                         [
                             validators.length(max=90, message="Erro: Tamanho do campo Estado inválido.")
                         ])
    pais = StringField('Pais',
                       [
                           validators.length(max=90, message="Erro: Tamanho do campo Pais inválido."),
                           validators.Required(message="O campo Pais é requerido.")
                       ])

class VisitaForm(Form):
    temperatura = StringField('Temperatura')
    pressao = StringField('Pressão')
    descricao_estado = TextField('Descrição Estado', [validators.Required()])
    visita = DateField('Data de Visita',[validators.Required()], format="%Y-%m-%d")
    paciente = SelectField('Paciente', [validators.Required()], choices=[])
    quarto = SelectField('Quarto', [validators.Required()], choices=[])
    infeccao = SelectField('Infecção', [validators.Required()], choices=[('t','Sim'),('f','Não')])
    descricao_sintoma = StringField('Descrição Sintoma', [validators.Required()])
    data_estadia = StringField('Data de Estadia', [validators.Required()])
