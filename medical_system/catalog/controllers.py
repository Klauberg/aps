from medical_system.catalog.models import Login
from flask_login import login_user, logout_user
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

class LogoutControl():
    def __init__ (self):
        logout_user()
