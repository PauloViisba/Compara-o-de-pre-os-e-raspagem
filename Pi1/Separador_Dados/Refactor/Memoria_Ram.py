def extrair_atributos_memoria(memoria_str):
    # Divide a string da memória em partes usando ', ' como delimitador
    atributos = memoria_str.split(', ')
    
    # Extrai o nome e a marca da primeira parte da string
    nome_marca = atributos[0].split('MEMORIA ')[1].split(', ')[0]
    nome = nome_marca.split(' ')[1]
    marca = nome_marca.split(' ')[0]

    # Extrai a quantidade de módulos, capacidade, tipo, frequência, latência e cor das partes correspondentes
    quantidade_modulos = atributos[1].split()[1][1:-1]  # A quantidade de módulos é o segundo número após o parêntese
    capacidade = atributos[1].split()[0]
    tipo = atributos[3]
    frequencia = atributos[4].split()[1]
    latencia = atributos[5]
    cor = atributos[6].split(' E ')[0]

    return nome, marca, quantidade_modulos, capacidade, tipo, frequencia, latencia, cor

def exibir_informacoes_memoria(memoria_str):
    atributos = extrair_atributos_memoria(memoria_str)
    
    # Exibe as informações formatadas
    print("Nome:", atributos[0])
    print("Marca:", atributos[1])
    print("Quantidade de módulos:", atributos[2])
    print("Capacidade:", atributos[3])
    print("Tipo:", atributos[4])
    print("Frequência:", atributos[5])
    print("Latência:", atributos[6])
    print("Cor:", atributos[7])

# Testando com a entrada do usuário
entrada_memoria = "MEMORIA REDRAGON SOLAR, RGB, 8GB (1X8GB), DDR4, 3600MHZ, C16, PRETA E DOURADA, GM-805"
exibir_informacoes_memoria(entrada_memoria)
