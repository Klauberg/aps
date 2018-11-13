from medical_system import database #Importa a Database do módulo medical_system (pasta)

'''
IMPORTANTE

Neste documento estão mapeadas as tabelas do Banco.
Caso não existam, serão criadas de forma automática.
Se fizer alguma modificação nesse arquivo,
as tabelas serão substituidas (Reescritas) sem permissão.

Portanto, !!! PELO AMOR DE DEUS, NÃO MEXA EM NADA !!!
'''

#Tabela Produtos
class Produtos(database.Model): #Cria um "Objeto", herdando o Model do SQLAlchemy
    id = database.Column(database.Integer, primary_key=True) #Coluna de ID
    name = database.Column(database.String(255)) #Coluna de Nome
    price = database.Column(database.Float(asdecimal=True)) #Coluna de Preço

    def __init__(self, price, name):
        self.price = price
        self.name = name

    def __repr__(self):
        return f"<Produto {self.id}>"
