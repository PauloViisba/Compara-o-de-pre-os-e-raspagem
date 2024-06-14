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
    nome, marca, num_cores, num_threads, frequencia_base, frequencia_turbo, cache, soquete = extrair_atributos_processador(processador_str)

    print("Nome:", nome)
    print("Marca:", marca)
    print("Número de núcleos:", num_cores)
    print("Número de threads:", num_threads)
    print("Frequência de clock base:", frequencia_base)
    print("Frequência de clock turbo:", frequencia_turbo)
    print("Cache:", cache)
    print("Soquete:", soquete)

# Testando com a entrada do usuário
entrada = "PROCESSADOR INTEL CORE I5-14400F, 10-CORE, 16-THREADS, 3.5GHZ (4.7GHZ TURBO), CACHE 20MB, LGA1700, BX8071514400F"
exibir_informacoes_processador(entrada)
