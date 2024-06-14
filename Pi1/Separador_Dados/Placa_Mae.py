def extrair_atributos_placa_mae(placa_mae_str):
    atributos = placa_mae_str.split(', ')

    nome = atributos[0]
    marca = nome.split()[2]  # A marca é a terceira palavra do nome da placa mãe
    memoria = atributos[1]
    soquete = atributos[2]
    formato = atributos[3]
    chipset = atributos[4]

    return nome, marca, memoria, soquete, formato, chipset

def exibir_informacoes_placa_mae(placa_mae_str):
    nome, marca, memoria, soquete, formato, chipset = extrair_atributos_placa_mae(placa_mae_str)

    print("Nome:", nome)
    print("Marca:", marca)
    print("Memória:", memoria)
    print("Soquete:", soquete)
    print("Formato:", formato)
    print("Chipset:", chipset)

# Testando com a entrada do usuário
entrada = "PLACA MAE ASUS PRIME B550-PLUS, DDR4, SOCKET AMD AM4, ATX, CHIPSET AMD B550, PRIME-B550-PLUS"
exibir_informacoes_placa_mae(entrada)
