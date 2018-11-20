from wtforms import Form
from wtforms import StringField
from wtforms import validators
from wtforms import HiddenField
from wtforms import PasswordField

class LoginForm(Form):
    usuario = StringField('Usuário',
            [
                validators.length(min=5, max=15, message="Usuário ou Senha Inválido(a)")
            ]
            )
    senha = PasswordField('Senha')
