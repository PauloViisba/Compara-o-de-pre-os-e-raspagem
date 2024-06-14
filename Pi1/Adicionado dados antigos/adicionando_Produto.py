import mysql.connector

# Dados de exemplo
dados = [

]

# Função para modificar os IDs e adicionar valores 'None', '2024-04-25', 'None'
def modificar_dados(dados, incremento):
    novos_dados = []
    for registro in dados:
        novo_id = registro[0] + incremento
        novos_dados.append((novo_id,) + registro[1:] + (None, '2024-04-25', None))
    return novos_dados

# Modificar os IDs adicionando 649 e adicionar valores 'null', '2024-04-25', 'null'
novos_dados = modificar_dados(dados, 649)

# Configurações de conexão ao banco de dados MySQL
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'comp'
}

# Conectar ao banco de dados MySQL
conexao = mysql.connector.connect(**config)
cursor = conexao.cursor()

# Inserir os novos dados na tabela
cursor.executemany('''
INSERT INTO produto (idProduto, Nome, Marca, Preco, Site, Imagem, Data, Link)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
''', novos_dados)

# Confirmar as alterações
conexao.commit()

# Fechar a conexão
conexao.close()

print("Dados inseridos com sucesso!")
