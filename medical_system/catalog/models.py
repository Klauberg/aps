from medical_system import database #Importa a Database do módulo medical_system (pasta)
from flask_login import UserMixin

'''
IMPORTANTE

Neste documento estão mapeadas as tabelas do Banco.
Caso não existam, serão criadas de forma automática.
Se fizer alguma modificação nesse arquivo,
as tabelas serão substituidas (Reescritas) sem permissão.

Portanto, !!! PELO AMOR DE DEUS, NÃO MEXA EM NADA !!!
'''

class Contato(database.Model):
    __tablename__ = 'contato'
    id_contato = database.Column(database.Integer, primary_key=True)
    nr_telefone = database.Column(database.String(20), nullable=False)
    nr_emergencia = database.Column(database.String(20), nullable=False)
    email = database.Column(database.String(260))

    def __init__(self, nr_telefone, nr_emergencia, email):
        self.nr_emergencia = nr_telefone
        self.nr_emergencia = nr_emergencia
        self.email = email

    def __repr__(self):
        return f"<Contato : {self.id_contato}>"

class Pessoa(database.Model):
    __tablename__ = 'pessoa'
    id_pessoa = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(260), nullable=False)
    cpf = database.Column(database.String(15))
    rg = database.Column(database.String(10), nullable=False)
    nascimento = database.Column(database.Date, nullable=False)
    id_endereco = database.Column(database.Integer, database.ForeignKey('endereco.id_endereco'), nullable=False)
    id_contato = database.Column(database.Integer, database.ForeignKey('contato.id_contato'),  nullable=False)
    endereco = database.relationship('Endereco', foreign_keys=id_endereco)
    contato = database.relationship('Contato', foreign_keys=id_contato)

    def __init__(self, nome, cpf, rg, nascimento, endereco, contato):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.nascimento = nascimento
        self.id_endereco = endereco
        self.id_contato = contato

    def __repr__(self):
        return f"<Pessoa : {self.id_pessoa}>"

class Medico(database.Model):
    __tablename__ = 'medico'
    id_medico = database.Column(database.Integer, primary_key=True)
    crm = database.Column(database.String(20), nullable=False)
    salario = database.Column(database.Float(asdecimal=True), nullable=False)
    id_pessoa = database.Column(database.Integer, database.ForeignKey('pessoa.id_pessoa'), nullable=False)
    bl_atividade = database.Column(database.Boolean, nullable=False)
    id_login = database.Column(database.Integer, database.ForeignKey('login.id_login'), nullable=False)
    pessoa = database.relationship('Pessoa', foreign_keys=id_pessoa)
    login = database.relationship('Login', foreign_keys=id_login)

    def __init__(self, crm, salario, id_pessoa, bl_atividade, id_login):
        self.crm = crm
        self.salario = salario
        self.id_pessoa = id_pessoa
        bl_atividade = bl_atividade
        id_login = id_login

    def __repr__(self):
        return f"<Medico : {self.id_medico}>"

class Formacao(database.Model):
    __tablename__ = 'formacao'
    id_medico = database.Column(database.Integer, database.ForeignKey('medico.id_medico'), primary_key=True, autoincrement=False)
    codigo = database.Column(database.String(50), database.ForeignKey('especialidade.codigo'), primary_key=True, autoincrement=False)
    bl_exercicio = database.Column(database.Boolean, nullable=False)
    cd = database.relationship('Especialidade', foreign_keys=codigo)
    medico = database.relationship('Medico', foreign_keys=id_medico)

    def __init__(self, id_medico, codigo, bl_exercicio):
        self.id_medico = id_medico
        self.codigo = codigo
        self.bl_exercicio = bl_exercicio

    def __repr__(self):
        return f"ID : {self.id_medico} | Codigo : {self.id_medico}"

class Especialidade(database.Model):
    __tablename__ = 'especialidade'
    codigo = database.Column(database.String(50), primary_key=True, autoincrement=False)
    nome = database.Column(database.String(200), nullable=False)

    def __init__(self, codigo, nome):
        self.codigo = codigo
        self.nome = nome

    def __repr__(self):
        return f"<Código : {self.codigo}>"

class Paciente(database.Model):
    __tablename__ = 'paciente'
    id_paciente = database.Column(database.Integer, primary_key=True)
    id_pessoa = database.Column(database.Integer, database.ForeignKey('pessoa.id_pessoa'), nullable=False)
    id_medico = database.Column(database.Integer, database.ForeignKey('medico.id_medico'), nullable=False)
    medico = database.relationship('Medico', foreign_keys=id_medico)
    pessoa = database.relationship('Pessoa', foreign_keys=id_pessoa)

    def __init__(self, id_pessoa, id_medico):
        self.id_pessoa = id_pessoa
        self.id_medico = id_medico

    def __repr__(self):
        return f"<Paciente : {self.id_paciente}>"

class Estadia(database.Model):
    __tablename__ = 'estadia'
    id_paciente = database.Column(database.Integer, database.ForeignKey('paciente.id_paciente'), primary_key=True, autoincrement=False)
    id_quarto = database.Column(database.Integer, database.ForeignKey('quarto.id_quarto'), primary_key=True, autoincrement=False)
    bl_infeccao = database.Column(database.Boolean, nullable=False)
    de_sintomas = database.Column(database.String(360), nullable=False)
    dt_estadia = database.Column(database.Date, nullable=False)
    quarto = database.relationship('Quarto', foreign_keys=id_quarto)
    paciente = database.relationship('Paciente', foreign_keys=id_paciente)

    def __init__ (self, id_paciente, id_quarto, bl_infeccao, de_sintomas, dt_estadia):
        self.bl_infeccao = bl_infeccao
        self.de_sintomas = de_sintomas
        self.dt_estadia = dt_estadia
        self.id_paciente = id_paciente
        self.id_quarto = id_quarto

    def __repr__(self):
        return f"<Estadia -> Paciente: {self.id_paciente} | Quarto: {self.id_quarto}>"

class Quarto(database.Model):
    __tablename__ = 'quarto'
    id_quarto = database.Column(database.Integer, primary_key=True, autoincrement=False)
    nr_capacidade = database.Column(database.Integer, nullable=False)
    nr_andar = database.Column(database.Integer, nullable=False)
    nr_usando = database.Column(database.Integer, nullable=False)

    def __init__ (self, id_quarto, nr_capacidade, nr_andar, nr_usando):
        self.id_quarto = id_quarto
        self.nr_capacidade = nr_capacidade
        self.nr_andar = nr_andar
        self.nr_usando = nr_usando

    def __repr__(self):
        return f"<Quarto : {self.id_quarto}>"

class Login(database.Model, UserMixin):
    __tablename__ = 'login'
    id_login = database.Column(database.Integer, primary_key=True)
    login = database.Column(database.String(100), nullable=False)
    password = database.Column(database.String(20), nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def get_id(self):
        return self.id_login

    def __repr__(self):
        return f"<Login : {self.id_login}>"

class Prioridade(database.Model):
    __tablename__ = 'prioridade'
    id_prioridade = database.Column(database.Integer, primary_key=True, autoincrement=False)
    int_prioridade = database.Column(database.Integer, nullable=False)
    doenca = database.Column(database.String(120), nullable=False)
    sn_fila = database.Column(database.Integer, nullable=False)
    tm_prioridade = database.Column(database.DateTime, server_default=database.text('LOCALTIMESTAMP'), nullable=False)
    bl_paciente = database.Column(database.Boolean, nullable=False)
    id_paciente = database.Column(database.Integer, database.ForeignKey('paciente.id_paciente'), nullable=False)
    paciente = database.relationship('Paciente', foreign_keys=id_paciente)

    def __init__(self, int_prioridade, doenca, sn_fila, tm_prioridade, id_paciente, bl_paciente):
        self.bl_paciente = bl_paciente
        self.doenca = doenca
        self.id_paciente = id_paciente
        self.int_prioridade = int_prioridade
        self.sn_fila = sn_fila

    def __repr__(self):
        return f"<Prioridade : {self.id_prioridade}>"

class Visita(database.Model):
    __tablename__ = 'visita'
    id_visita = database.Column(database.Integer, primary_key=True)
    temperatura = database.Column(database.Integer)
    pressao = database.Column(database.String(10))
    de_estado = database.Column(database.String(360), nullable=False)
    dt_visita = database.Column(database.Date, nullable=False)
    id_paciente = database.Column(database.Integer, database.ForeignKey('paciente.id_paciente'), nullable=False)
    id_medico = database.Column(database.Integer, database.ForeignKey('medico.id_medico'), nullable=False)
    paciente = database.relationship('Paciente', foreign_keys=id_paciente)
    medico = database.relationship('Medico', foreign_keys=id_medico)

    def __init__(self, temperatura, pressao, de_estado, dt_visita, id_paciente, id_medico):
        self.temperatura = temperatura
        self.de_estado = de_estado
        self.dt_visita = dt_visita
        self.id_medico = id_medico
        self.pressao = pressao
        self.id_paciente = id_paciente

    def __repr__(self):
        return f"<Visita : {self.id_visita}>"

class Endereco(database.Model):
    __tablename__ = 'endereco'
    id_endereco = database.Column(database.Integer, primary_key=True)
    numero = database.Column(database.String(45), nullable=False)
    cep = database.Column(database.String(12), nullable=False)
    cidade = database.Column(database.String(100), nullable=False)
    estado = database.Column(database.String(100))
    pais = database.Column(database.String(100), nullable=False)

    def __init__(self, numero, cep, cidade, estado, pais):
        self.cep = cep
        self.cidade = cidade
        self.numero = numero
        self.estado = estado
        self.pais = pais

    def __repr__(self):
        return f"<Endereco : {self.id_endereco}>"
