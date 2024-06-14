from selenium import webdriver
from bs4 import BeautifulSoup
import mysql.connector
import re
from datetime import datetime

# Conexão com o banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="comp"
)

# Função para extrair os atributos da placa-mãe
def extrair_atributos_placa_mae(nome_placa_mae):
    try:
        # Padronizando o nome da placa-mãe
        nome_placa_mae = nome_placa_mae.lower().replace('-', ' ').replace(',', '')

        # Definindo padrões para extrair os atributos
        padrao_qtd_slots_memoria = r'(\d+)x[\s-]*dimms?'
        padrao_qtd_slots_pci = r'(\d+)x[\s-]*pci[\s-]*e?[\s-]*x?[\s-]*\d'
        padrao_chipset = r'chipset[\s-]*([\w\s]+)'
        padrao_formato = r'(atx|matx|micro[\s-]*atx|mini[\s-]*itx)'
        padrao_soquete = r'(lga|am|fm)?\d{3,4}'

        # Procurando por padrões no nome da placa-mãe
        match_qtd_slots_memoria = re.search(padrao_qtd_slots_memoria, nome_placa_mae)
        match_qtd_slots_pci = re.search(padrao_qtd_slots_pci, nome_placa_mae)
        match_chipset = re.search(padrao_chipset, nome_placa_mae)
        match_formato = re.search(padrao_formato, nome_placa_mae)
        match_soquete = re.search(padrao_soquete, nome_placa_mae)

        # Extraindo os atributos
        qtd_slots_memoria = int(match_qtd_slots_memoria.group(1)) if match_qtd_slots_memoria else 0
        qtd_slots_pci = int(match_qtd_slots_pci.group(1)) if match_qtd_slots_pci else 0
        chipset = match_chipset.group(1).capitalize() if match_chipset else ''
        formato = match_formato.upper() if match_formato else ''
        soquete = match_soquete.group() if match_soquete else ''

        return qtd_slots_memoria, qtd_slots_pci, chipset, formato, soquete

    except Exception as e:
        print(f"Erro ao extrair atributos da placa-mãe '{nome_placa_mae}': {e}")
        return 0, 0, '', '', ''

# Conectando com o site 
driver = webdriver.Chrome()
driver.get("https://www.terabyteshop.com.br/hardware/placas-mae")

html = driver.page_source
site = BeautifulSoup(html, 'html.parser')

# Pegando os valores
imagens_placa_mae = site.find_all("div", class_="commerce_columns_item_image text-center")
precos_placa_mae = site.find_all("div", class_="prod-new-price")
nomes_placas_mae = site.find_all("a", class_="prod-name")
link_processador = site.find_all("a", class_="commerce_columns_item_image")

precos_limpos = []
Nomes_placa_mae = []
Precos_placa_mae = []
urls_imagens = []
Links_processador = []

# Adicionando à lista 
for span in nomes_placas_mae:
    Nomes_placa_mae.append(span.text.strip())

for span in precos_placa_mae:
    Precos_placa_mae.append(span.text.strip())

for span in link_processador:
    Links_processador.append(span['href'])  

# Extrair URLs das imagens e adicionar à lista
for div in imagens_placa_mae:
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

for valor in Precos_placa_mae:
    preco_convertido = limpar_e_converter(valor)
    precos_limpos.append(preco_convertido)

# Inserindo os produtos e detalhes da placa-mãe no banco de dados
cursor = mydb.cursor()

# Usar a data atual para o campo Data
data_atual = datetime.now().strftime('%Y-%m-%d')

for nome, preco, imagem_url, link in zip(Nomes_placa_mae, precos_limpos, urls_imagens, Links_processador):
    # Usando a função extrair_atributos_placa_mae para dividir o nome da placa-mãe em outros atributos
    qtd_slots_memoria, qtd_slots_pci, chipset, formato, soquete = extrair_atributos_placa_mae(nome)
    
    # Inserindo o produto na tabela 'produto'
    cursor.execute("INSERT INTO produto (Nome, Marca, Preco, Site, Imagem, Data, Link) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (nome, 'Desconhecida', preco, 'Terabyte', imagem_url, data_atual, link))
    mydb.commit()

    # Obtendo o ID do produto recém-inserido
    idProduto = cursor.lastrowid

    # Inserindo os detalhes da placa-mãe na tabela 'placa_mae' e vinculando-o ao produto
    cursor.execute("INSERT INTO placa_mae (Produto_idProduto, Qtd_Slots_Memoria, Qtd_Slots_Pci, Chipset, Formato, Soquete) VALUES (%s, %s, %s, %s, %s, %s)",
                   (idProduto, qtd_slots_memoria, qtd_slots_pci, chipset, formato, soquete))
    mydb.commit()

cursor.close()
mydb.close()
