

#Processador
def extrair_atributos_processador(processador_str):
    atributos = processador_str.split(', ')

    nome = atributos[0]
    marca = nome.split()[1]  # A marca é a segunda palavra do nome do processador
    num_cores = int(atributos[1].split()[0].split('-')[0])
    num_threads = int(atributos[2].split()[0].split('-')[0])
    
    # Encontrar a frequência de clock base
    frequencia_base = None
    for atributo in atributos[3].split():
        if 'GHZ' in atributo:
            frequencia_base = atributo
            break
            
    # Encontrar a frequência de clock turbo
    frequencia_turbo = None
    for atributo in atributos[3].split():
        if 'GHZ' in atributo and atributo != frequencia_base:
            frequencia_turbo = atributo.replace('(', '').replace(')', '')
            break
            
    cache = atributos[4].split()[1]
    soquete = atributos[5]

    return nome, marca, num_cores, num_threads, frequencia_base, frequencia_turbo, cache, soquete

def exibir_informacoes_processador(processador_str):
    nome, marca, num_cores, num_threads, frequencia_base,frequencia_turbo, cache, soquete = extrair_atributos_processador(processador_str)

    print("Nome:", nome)
    print("Marca:", marca)
    print("Número de núcleos:", num_cores)
    print("Número de threads:", num_threads)
    print("Frequência de clock base:", frequencia_base)
    print("Frequência de clock turbo:", frequencia_turbo)
    print("Cache:", cache)
    print("Soquete:", soquete)

#Placa_Mae
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


def processar_entrada(entrada):
    if entrada.startswith("PLACA MAE"):
        exibir_informacoes_placa_mae(entrada)
    elif entrada.startswith("PROCESSADOR"):
        exibir_informacoes_processador(entrada)
    else:
        print("Entrada inválida")

# Testando com a entrada do usuário
entrada_processador = "Processador AMD Ryzen 5 5500, 3.6GHz, Cache 16MB, Hexa Core, 12 Threads, AM4 - 100-100000457BOX"
entrada_placa_mae = "PLACA MAE ASUS PRIME H770-PLUS, DDR5, LGA 1700, ATX, CHIPSET INTEL H770, PRIME-H770-PLUS"

processar_entrada(entrada_processador)
processar_entrada(entrada_placa_mae)
