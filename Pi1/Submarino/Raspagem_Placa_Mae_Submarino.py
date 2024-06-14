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

def extrair_atributos_placa_mae(nome_placa_mae):
    # Padronizando o nome da placa-mãe
    nome_placa_mae = nome_placa_mae.lower().replace('-', ' ').replace(',', '')

    # Definindo padrões para extrair os atributos
    padrao_qtd_slots_memoria = r'(\d+)x[\s-]*dimms?'
    padrao_qtd_slots_pci = r'(\d+)x[\s-]*pc[i-e][\s-]*e?[\s-]*x?[\s-]*\d'
    padrao_chipset = r'(?:intel|amd)[\s-]*(\w+(?:\s*\w+)*)'
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
    formato = match_formato.group(1).upper() if match_formato else ''
    soquete = match_soquete.group() if match_soquete else ''

    return qtd_slots_memoria, qtd_slots_pci, chipset, formato, soquete


# Conectando com o site 
driver = webdriver.Chrome()
driver.get("https://www.submarino.com.br/busca/componentes-gamer?content=componentes+gamer&filter=%7B%22id%22%3A%22wit%22%2C%22value%22%3A%22placa+m%C3%A3e%22%2C%22fixed%22%3Afalse%7D&sortBy=relevance&source=nanook&testab=searchTestAB%3Dout")

html = driver.page_source
site = BeautifulSoup(html, 'html.parser')

# Pegando os valores
imagens_placa_mae = site.find_all("picture", class_="src__Picture-sc-xr9q25-2 ghIIuE" )

precos_placa_mae = site.find_all("span", class_="src__Text-sc-154pg0p-0 styles__PromotionalPrice-sc-yl2rbe-0 dthYGD list-price")

nomes_placa_mae =  site.find_all("h3", class_="product-name")

link_processador = site.find_all("a", class_="inStockCard__Link-sc-1ngt5zo-1 JOEpk")

Precos_placa_mae = []
Nomes_placa_mae = []
urls_imagens = []
Links_processador = []
Links_Limpos = []

# Adicionando à lista 
for span in nomes_placa_mae:
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

precos_limpos = []

for valor in Precos_placa_mae:
    preco_convertido = limpar_e_converter(valor)
    precos_limpos.append(preco_convertido)

# Adiciona "https://www.submarino.com.br/" ao início de cada link
for link in Links_processador:
    Links_Limpos.append(f"https://www.submarino.com.br{link}")


print(Nomes_placa_mae)
print("---------")
print(precos_limpos)
print("---------")
print(urls_imagens)
print("---------")
print(Links_Limpos)



