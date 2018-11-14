import json # Importa o Modulo de JSON do Python [Nativa].

# Importa do Flask as Bibliotecas de Request, Jsonify(Para comunicação JSON),
# e Blueprint, que servirá para permitir a modularização do sistema.
# Abort é para tratamento de erro, em requisições (Erro 404, por exemplo.)
from flask import request, jsonify, Blueprint, abort

# Permite gerenciar os metodos GET, POST, PUT e DELETE através de métodos
from flask.views import MethodView

from medical_system import app, database #Importa do __init__ as variáveis app e database

#Importa os Modelos no arquivo models.py
from medical_system.catalog.models import Produtos

catalog = Blueprint('catalog', __name__)

@catalog.route('/')
@catalog.route('/login/')
def login():
    return "Bem-Vindo ao Sistema!"

#Classe de Exemplo. Não Mexer no momento.
# class ProdutosView(MethodView):
#
#     def get(self, id=None, pagina=1):
#         if not id:
#             produtos = Produtos.query.paginate(pagina, 10).items
#             resposta = {}
#             for produto in produtos:
#                 resposta[produtos.id] = {
#                     "nome" : produto.name,
#                     "preço" : str(produto.price)
#                 }
#         else:
#             produto = Produtos.query.filter_by(id=id).first()
#             if not produto:
#                 abort(404)
#             resposta = {
#                 "nome" : produto.name,
#                 "preço" : produto.price
#             }
#         return jsonify(resposta)
#
#     def post(self):
#         name = request.form.get('name')
#         price = request.form.get('preco')
#         produto = Produtos(price, name)
#         database.session.add(produto)
#         database.session.commit()
#         return jsonify(
#             {
#                 produto.id:{
#                     "nome":produto.name,
#                     "preço":produto.price
#                 }
#             }
#         )
#
#     def put(self, id):
#         return
#
#     def delete(self, id):
#         return
#
# produtos_view = ProdutosView.as_view('produtos_view')
# app.add_url_rule('/produtos/', view_func=produtos_view, methods=['GET','POST'])
# app.add_url_rule('/produtos/<int:id>', view_func=produtos_view, methods=['GET'])
