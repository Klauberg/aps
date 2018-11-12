# CLASSE DE CONEXÃO
# Aqui, poderá configurar o Banco (Nome, senha, host, porta, Database)
# Apenas substitua os campos no dict. Ele criará a string pra você.
class Connection(object):
    def url():

        db = {
            'user':'aps',
            'password':'aps',
            'host':'127.0.0.1',
            'port':'5432',
            'database':'medical_system'
        }

        url = "postgresql://{}:{}@{}:{}/{}"
        url = url.format(db['user'], db['password'], db['host'], db['port'], db['database'])
        return url
