import re

# Dados extraídos
nomes_placas_mae = [
   'Placa Mãe MSI A520M-A PRO, AMD AM4, mATX, DDR4',
    'Placa Mãe Gigabyte B550M Aorus Elite, AMD AM4, Micro ATX, DDR4',
    'Placa Mãe MSI B560M PRO-E, Intel LGA 1200, mATX, DDR4',
    'Placa Mãe Asus TUF GAMING A520M-PLUS II, AMD AM4, mATX, DDR4',
    'Placa Mãe ASRock B450M Steel Legend, AMD AM4, mATX, DDR4',
    'Placa Mãe ASRock B450M-HDV R4.0, AMD AM4, Micro ATX, DDR4',
    'Placa-Mãe MSI MPG B550 Gaming Plus, AMD AM4, ATX',
    'Placa Mãe Gigabyte B450M DS3H V2, AMD B450, mATX, DDR4, (rev. 1.0)',
    'Placa Mãe Asus TUF Gaming B550M-Plus, AMD AM4, mATX, DDR4',
    'Placa Mãe Gigabyte H610M (rev. 1.0), Intel LGA1700, H610, DDR4, mATX - H610M H DDR4',
    'Placa-Mãe Asus TUF Gaming B450M-Plus II, AMD AM4, mATX, DDR4',
    'Placa Mãe MSI B450M-A Pro Max, AMD AM4, Micro-ATX, DDR4',
    'Placa-Mãe MSI B450M Pro-VDH Max p/ AMD AM4, m-ATX, DDR4',
    'Placa Mãe Gigabyte A520M DS3H V2, AMD, Micro ATX, DDR4 - A520M DS3H V2',
    'Placa Mãe Gigabyte Aorus B450 Elite V2, AMD B450, ATX, DDR4, (rev. 1.0)',
    'Placa Mãe ASRock B660M Phantom Gaming 4, Intel, M-ATX, DDR4, Socket, LGA 1700',
    'Placa Mãe Gigabyte B760M AORUS ELITE (rev. 1.0), LGA 1700, DDR5',
    'Placa Mãe Asus Prime A520M-E, AMD AM4, mATX, DDR4',
    'Placa Mãe MSI H310M PRO-VDH, Intel 1151, m-ATX, DDR4 - H310M PRO-VDH',
    'Placa Mãe Asus Prime H610M-E D4, Intel LGA 1700, mATX, DDR4'
]
precos_placas_mae = [379.99, 849.99, 479.99, 599.99, 659.99, 359.99, 999.99, 529.99, 929.99, 529.99, 649.99, 379.99, 499.99, 449.99, 729.99, 739.99, 1369.99, 429.99, 299.99, 614.99]
urls_imagens = ['https://images.kabum.com.br/produtos/fotos/280890/placa-mae-msi-a520m-a-pro-amd-am4-matx-ddr4_1646852577_m.jpg', 'https://images.kabum.com.br/produtos/fotos/114781/placa-mae-gigabyte-b550m-aorus-elite-amd-am4-micro-atx-ddr4_1594908595_m.jpg', 'https://images.kabum.com.br/produtos/fotos/280944/placa-mae-msi-b560m-pro-e-lga-1200-matx-ddr4_1646832447_m.jpg', 'https://images.kabum.com.br/produtos/fotos/165133/placa-mae-asus-tuf-gaming-a520m-plus-ii-amd-am4-matx-ddr4-90mb17g0-m0eay0_1632513548_m.jpg', 'https://images.kabum.com.br/produtos/fotos/100672/placa-mae-asrock-b450m-steel-legend-amd-am4-matx-ddr4-90-mxb9y0-a0uayz_placa-mae-asrock-b450m-steel-legend-amd-am4-matx-ddr4-90-mxb9y0-a0uayz_1552586908_m.jpg', 'https://images.kabum.com.br/produtos/fotos/111107/placa-mae-asrock-b450m-hdv-r4-0-amd-am4-micro-atx-ddr4-_1590689801_m.jpg', 'https://images.kabum.com.br/produtos/fotos/114335/placa-mae-msi-mpg-b550-gaming-plus-amd-am4-atx_1594999681_m.jpg', 'https://images.kabum.com.br/produtos/fotos/127869/placa-mae-gigabyte-b450m-ds3h-v2-amd-b450-matx-ddr4-rev-1-0-_1642601501_m.jpg', 'https://images.kabum.com.br/produtos/fotos/115216/placa-mae-asus-tuf-gaming-b550m-plus-amd-am4-matx-ddr4_1689958846_m.jpg', 'https://images.kabum.com.br/produtos/fotos/315273/placa-mae-gigabyte-h610m-rev-1-0-intel-lga1700-h610-ddr4-matx-h610m-h-ddr4_1647527046_m.jpg', 'https://images.kabum.com.br/produtos/fotos/128437/placa-mae-asus-tuf-b450m-plus-ii_1601898339_m.jpg', 'https://images.kabum.com.br/produtos/fotos/458886/placa-mae-msi-b450m-a-pro-max-amd-am4-micro-atx-ddr4_1699991851_m.jpg', 'https://images.kabum.com.br/produtos/fotos/108499/placa-mae-msi-b450m-pro-vdh-max-p-amd-am4-m-atx-ddr4-_1576079415_m.jpg', 'https://images.kabum.com.br/produtos/fotos/457818/placa-mae-gigabyte-a520m-ds3h-v2-amd-micro-atx-ddr4-a520m-ds3h-v2_1689160432_m.jpg', 'https://images.kabum.com.br/produtos/fotos/127868/placa-mae-gigabyte-aorus-b450-elite-v2-amd-b450-atx-ddr4-rev-1-0-_1599763669_m.jpg', 'https://images.kabum.com.br/produtos/fotos/495982/placa-mae-asrock-b660m-phantom-gaming-4-intel-m-atx-ddr4-socket-lga-1700_1698090845_m.jpg', 'https://images.kabum.com.br/produtos/fotos/419108/placa-mae-gigabyte-b760m-aorus-elite_1677686877_m.jpg', 'https://images.kabum.com.br/produtos/fotos/129653/placa-mae-asus-prime-a520-e-amd-am4-matx-ddr4_1602791074_m.jpg', 'https://images.kabum.com.br/produtos/fotos/430926/placa-mae-msi-h310m-pro-vdh-intel-1151-m-atx-ddr4-h310m-pro-vdh_1686063371_m.jpg', 'https://images.kabum.com.br/produtos/fotos/321070/placa-mae-asus-prime-h610m-e-d4-intel-lga-1700-h610-matx-ddr4-90mb19n0-c1bay0_1648577141_m.jpg']

links_processadores = ['https://www.kabum.com.br/produto/280890/placa-mae-msi-a520m-a-pro-amd-am4-matx-ddr4', 'https://www.kabum.com.br/produto/114781/placa-mae-gigabyte-b550m-aorus-elite-amd-am4-micro-atx-ddr4', 'https://www.kabum.com.br/produto/280944/placa-mae-msi-b560m-pro-e-intel-lga-1200-matx-ddr4', 'https://www.kabum.com.br/produto/165133/placa-mae-asus-tuf-gaming-a520m-plus-ii-amd-am4-matx-ddr4', 'https://www.kabum.com.br/produto/100672/placa-mae-asrock-b450m-steel-legend-amd-am4-matx-ddr4', 'https://www.kabum.com.br/produto/111107/placa-mae-asrock-b450m-hdv-r4-0-amd-am4-micro-atx-ddr4', 'https://www.kabum.com.br/produto/114335/placa-mae-msi-mpg-b550-gaming-plus-amd-am4-atx', 'https://www.kabum.com.br/produto/127869/placa-mae-gigabyte-b450m-ds3h-v2-amd-b450-matx-ddr4-rev-1-0-', 'https://www.kabum.com.br/produto/115216/placa-mae-asus-tuf-gaming-b550m-plus-amd-am4-matx-ddr4', 'https://www.kabum.com.br/produto/315273/placa-mae-gigabyte-h610m-rev-1-0-intel-lga1700-h610-ddr4-matx-h610m-h-ddr4', 'https://www.kabum.com.br/produto/128437/placa-mae-asus-tuf-gaming-b450m-plus-ii-amd-am4-matx-ddr4', 'https://www.kabum.com.br/produto/458886/placa-mae-msi-b450m-a-pro-max-amd-am4-micro-atx-ddr4', 'https://www.kabum.com.br/produto/108499/placa-mae-msi-b450m-pro-vdh-max-p-amd-am4-m-atx-ddr4-', 'https://www.kabum.com.br/produto/457818/placa-mae-gigabyte-a520m-ds3h-v2-amd-micro-atx-ddr4-a520m-ds3h-v2', 'https://www.kabum.com.br/produto/127868/placa-mae-gigabyte-aorus-b450-elite-v2-amd-b450-atx-ddr4-rev-1-0-', 'https://www.kabum.com.br/produto/495982/placa-mae-asrock-b660m-phantom-gaming-4-intel-m-atx-ddr4-socket-lga-1700', 'https://www.kabum.com.br/produto/419108/placa-mae-gigabyte-b760m-aorus-elite-rev-1-0-lga-1700-ddr5', 'https://www.kabum.com.br/produto/129653/placa-mae-asus-prime-a520m-e-amd-am4-matx-ddr4', 'https://www.kabum.com.br/produto/430926/placa-mae-msi-h310m-pro-vdh-intel-1151-m-atx-ddr4-h310m-pro-vdh', 'https://www.kabum.com.br/produto/321070/placa-mae-asus-prime-h610m-e-d4-intel-lga-1700-matx-ddr4']

# Função para extrair os atributos
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
        formato = match_formato.group(1).upper() if match_formato else ''
        soquete = match_soquete.group() if match_soquete else ''

        return qtd_slots_memoria, qtd_slots_pci, chipset, formato, soquete

    except Exception as e:
        print(f"Erro ao extrair atributos da placa-mãe '{nome_placa_mae}': {e}")
        return 0, 0, '', '', ''

# Gerar os scripts SQL
for i in range(len(nomes_placas_mae)):
    nome = nomes_placas_mae[i]
    preco = precos_placas_mae[i]
    imagem = urls_imagens[i]
    link = links_processadores[i]

    # Extrair atributos
    qtd_slots_memoria, qtd_slots_pci, chipset, formato, soquete = extrair_atributos_placa_mae(nome)

    # Comando SQL para inserir na tabela produto
    sql_produto = f"INSERT INTO produto (Nome, Marca, Preco, Site, Imagem, Data, Link) VALUES ('{nome}', '', {preco}, 'Terabyte Shop', '{imagem}', '2024-05-22', '{link}');"
    
    # Imprimindo o comando SQL para produto
    print(sql_produto)

    # Comando SQL para inserir na tabela placa_mae
    sql_placa_mae = f"INSERT INTO placa_mae (Produto_idProduto, Qtd_Slots_Memoria, Qtd_Slots_Pci, Chipset, Formato, Soquete) VALUES (LAST_INSERT_ID(), {qtd_slots_memoria}, {qtd_slots_pci}, '{chipset}', '{formato}', '{soquete}');"
    
    # Imprimindo o comando SQL para placa_mae
    print(sql_placa_mae)
