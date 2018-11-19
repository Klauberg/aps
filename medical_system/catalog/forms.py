from wtforms import Form
from wtforms import StringField
from wtforms import validators
from wtforms import HiddenField
from wtforms import PasswordField

#def length_honeypot (form, field):
#    if len(field.data) > 0:
#        raise validators.ValidationError()

class LoginForm(Form):
    usuario = StringField('Usuário',
            [
                validators.length(min=5, max=15, message="Usuário Inválido")
            ]
            )
    senha = PasswordField('Senha')
