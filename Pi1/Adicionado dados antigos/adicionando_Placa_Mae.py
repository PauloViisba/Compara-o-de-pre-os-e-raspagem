import mysql.connector

# Dados de exemplo
dados = [
 (525,2,0,'A520','matx','AM4'),(526,0,0,'H610','mATX','LGA1700')
,(527,0,1,'H61S','Micro atx','LGA1155'),(528,4,0,'B760M Aorus Elite','mATX','Intel 1700'),(529,2,0,'B450M Gaming','mATX','AM4'),
(530,0,0,'X670','Não especificado','Não especificado'),(531,0,0,'Ga-f2a68hm-h','Não especificado','Não especificado'),
(532,0,0,'B550','Matx','Amd Am4'),(533,0,0,'H61 Ih61-ma2','Não especificado','LGA1155'),
(534,0,0,'X99 Gaming','Não especificado','Não especificado'),(535,2,0,'A520M-E','matx','AM4'),
(536,0,0,'Ddr3 Lga 1155','Não especificado','Não especificado'),(537,0,0,'B550M-PLUS','Não especificado','AM4'),
(538,0,0,'A320m','Não especificado','Não especificado'),(539,0,0,'G41','DDR3','L775'),(540,0,0,'H61zg M2 H61','Não especificado','LGA1155'),
(541,0,0,'B250','Não especificado','LGA1151'),(542,0,0,'H61','Não especificado','LGA1155'),(543,0,0,'B660M-Plus D4','Matx','LGA1700'),
(544,0,0,'H61','Não especificado','LGA1155'),(545,0,0,'H110Tn-M','Ddr4 Mini Itx','Lga 1151'),(546,0,0,'9700','Não especificado','Não especificado'),(547,0,0,'B450M K','AM4','matx'),
(548,0,0,'B75M-A','Não especificado','Lga 1155'),(549,0,0,'BPC-H61M.2-T','Não especificado','Lga 1155'),(615,0,0,'B550','mATX','AMD AM4'),(616,0,0,'B450','mATX','AMD AM4'),
(617,0,0,'B450','mATX','AMD AM4'),(618,0,0,'B450','ATX','AMD AM4'),(619,0,0,'A520','mATX','AMD AM4'),(620,0,0,'B550','mATX','AMD AM4'),(621,0,0,'A520','mATX','AMD AM4'),
(622,0,0,'H510','mATX','LGA1200'),(623,0,0,'B550','mATX','AMD AM4'),(624,0,0,'A520','mATX','AMD AM4'),(625,0,0,'A520','mATX','AMD AM4'),(626,0,0,'H510','mATX','LGA1200'),
(627,0,0,'B450','mATX','AMD AM4'),(629,0,0,'H610','mATX','LGA1700'),(630,0,0,'H61','Micro ATX','LGA1155'),(631,0,0,'B760','mATX','Intel 1700'),(632,0,0,'B450','mATX','AMD AM4'),
(633,0,0,'X670','N/A','N/A'),(634,0,0,'F2A68HM-H','Micro ATX','Socket FM2+'),(635,0,0,'B550','mATX','AMD AM4'),(636,0,0,'H61','Micro ATX','LGA1155'),
(637,0,0,'X99','ATX','LGA2011-3'),(638,0,0,'A520','mATX','AMD AM4'),(639,0,0,'H61','Micro ATX','LGA1155'),(640,0,0,'B550','mATX','AMD AM4'),(641,0,0,'A320','Micro ATX','AMD AM4'),
(642,0,0,'G41','Micro ATX','LGA775'),(643,0,0,'H61','Micro ATX','LGA1155'),(644,0,0,'B250','ATX','LGA1151'),(645,0,0,'H61','Micro ATX','LGA1155'),(646,0,0,'B660','mATX','LGA1700'),
(647,0,0,'H61','Micro ATX','LGA1155'),(648,0,0,'H110','Mini ITX','LGA1151'),(649,0,0,'9700','N/A','N/A'),(650,0,0,'B450','mATX','AMD AM4'),(651,0,0,'B75','Micro ATX','LGA1155'),
(652,0,0,'A520','Micro ATX','AMD AM4')

]

# Função para modificar os IDs
def modificar_ids(dados, incremento):
    novos_dados = []
    for registro in dados:
        novo_id = registro[0] + incremento
        novos_dados.append((novo_id,) + registro[1:])
    return novos_dados

# Modificar os IDs adicionando 657
novos_dados = modificar_ids(dados, 649)

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
INSERT INTO placa_mae (Produto_idProduto, Qtd_Slots_Memoria, Qtd_Slots_Pci, Chipset, Formato, Soquete)
VALUES (%s, %s, %s, %s, %s, %s)
''', novos_dados)

# Confirmar as alterações
conexao.commit()

# Fechar a conexão
conexao.close()

print("Dados inseridos com sucesso!")
