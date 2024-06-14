from selenium import webdriver
from bs4 import BeautifulSoup
import mysql.connector
import re

# Conexão com o banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="comp"
)

def extrair_atributos_processador(nome_processador):
    # Padronizando o nome do processador
    nome_processador = nome_processador.lower().replace('-', ' ').replace(',', '')

    # Definindo padrões para extrair os atributos
    padrao_marca = r'(amd|intel)' 
    padrao_cores_threads = r'(\d+)(?:[\s-]*core)(?:s)?(?:[\s-]+(\d+)(?:[\s-]*thread)(?:s)?)?'
    padrao_frequencia = r'(\d+(?:\.\d+)?)ghz(?:[\s-]*\(?(?:base|turbo)?(?:clock)?\)?(?:[\s-]*(\d+(?:\.\d+)?)ghz)?)?'
    padrao_cache = r'(\d+mb)(?:[\s-]*cache)?'
    padrao_soquete = r'(lga|am|fm)?\d{3,4}'
    
    # Procurando por padrões no nome do processador
    match_marca = re.search(padrao_marca, nome_processador)
    match_cores_threads = re.search(padrao_cores_threads, nome_processador)
    match_frequencia = re.search(padrao_frequencia, nome_processador)
    match_cache = re.search(padrao_cache, nome_processador)
    match_soquete = re.search(padrao_soquete, nome_processador)

    # Extraindo os atributos
    marca = match_marca.group(1).capitalize() if match_marca else ''
    num_cores = int(match_cores_threads.group(1)) if match_cores_threads and match_cores_threads.group(1) else 0
    num_threads = int(match_cores_threads.group(2)) if match_cores_threads and match_cores_threads.group(2) else 0
    frequencia_base = float(match_frequencia.group(1)) if match_frequencia and match_frequencia.group(1) else 0.0
    frequencia_turbo = float(match_frequencia.group(2)) if match_frequencia and match_frequencia.group(2) else None
    cache = int(match_cache.group(1).replace('mb', '')) if match_cache else 0
    soquete = match_soquete.group() if match_soquete else ''

    return marca, num_cores, num_threads, frequencia_base, frequencia_turbo, cache, soquete

# Conectando com o site 
driver = webdriver.Chrome()
driver.get("https://www.terabyteshop.com.br/hardware/processadores")

html = driver.page_source
site = BeautifulSoup(html, 'html.parser')

# Pegando os valores
imagens_processador = site.find_all("div", class_="commerce_columns_item_image text-center" )
precos_processador = site.find_all("div", class_="prod-new-price")
nomes_processador = site.find_all("a", class_="prod-name")

Precos_processador = []
Nomes_processador = []
urls_imagens = []

# Adicionando à lista 
for span in nomes_processador:
    Nomes_processador.append(span.text.strip())

for span in precos_processador:
    Precos_processador.append(span.text.strip())

# Extrair URLs das imagens e adicionar à lista
for div in imagens_processador:
    img_tag = div.find("img")
    if img_tag:
        src_attr = img_tag.get("src")
        if src_attr:
            urls_imagens.append(src_attr)

# Fecha a página 
driver.quit()

# Limpa o preço
def limpar_e_converter(valor_str):
    valor_str = ''.join(caracter for caracter in valor_str if caracter.isdigit() or caracter == ',').replace(',', '.')
    return float(valor_str)

precos_limpos = []

for valor in Precos_processador:
    preco_convertido = limpar_e_converter(valor)
    precos_limpos.append(preco_convertido)

# Exibir os dados da lista de processadores e preços
for nome, preco, imagem_url in zip(Nomes_processador, precos_limpos, urls_imagens):
    # Usando a função extrair_atributos_processador para dividir o nome do processador em outros atributos
    marca, num_cores, num_threads, frequencia_base, frequencia_turbo, cache, soquete = extrair_atributos_processador(nome)
    
    # Exibindo os atributos e o preço
    # print("Nome do Processador:", nome)
    # print("Marca:", marca)
    # print("Número de Cores:", num_cores)
    # print("Número de Threads:", num_threads)
    # print("Frequência Base:", frequencia_base)
    # print("Frequência Turbo:", frequencia_turbo)
    # print("Cache:", cache)
    # print("Soquete:", soquete)
    # print("Preço:", preco)
    # print("URL da Imagem:", imagem_url)
    # print()

    
# Adiciona uma linha em branco entre os processadores

cursor = mydb.cursor()

# Inserindo os produtos e detalhes do processador no banco de dados
for nome, preco, imagem_url in zip(Nomes_processador, precos_limpos, urls_imagens):
    # Usando a função extrair_atributos_processador para dividir o nome do processador em outros atributos
    marca, num_cores, num_threads, frequencia_base, frequencia_turbo, cache, soquete = extrair_atributos_processador(nome)
    
    # Inserindo o produto na tabela 'produto'
    cursor.execute("INSERT INTO produto (Nome, Marca, Preco, Site, Imagem) VALUES (%s, %s, %s, %s, %s)", (nome, marca, preco, 'Terrabyte', imagem_url))
    mydb.commit()

    # Obtendo o ID do produto recém-inserido
    idProduto = cursor.lastrowid

    # Inserindo os detalhes do processador na tabela 'processador' e vinculando-o ao produto
    cursor.execute("INSERT INTO processador (Produto_idProduto, Qtd_Nucleos, Qtd_Threads, Clock_Base, Clock_Turbo, Cache, Soquete) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (idProduto, num_cores, num_threads, frequencia_base, frequencia_turbo, cache, soquete))
    mydb.commit()

cursor.close()
mydb.close()
