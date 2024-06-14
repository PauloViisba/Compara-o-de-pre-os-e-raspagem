def extrair_atributos(texto):
    atributos = {}

    # Dividindo o texto em partes separadas por vírgula e espaço
    partes = texto.split(", ")

    for parte in partes:
        # Dividindo cada parte em chave e valor separados por ": "
        chave, valor = parte.split(": ")

        # Armazenando os atributos no dicionário
        atributos[chave.capitalize()] = valor

    return atributos


# Exemplo de utilização
if __name__ == "__main__":
    texto_gabinete = "GABINETE GAMER THERMALTAKE CERES 330 TG SNOW ARGB, MID-TOWER, LATERAL DE VIDRO, COM 3 FANS, BRANCO, CA-1Y2-00M6WN-01"
    atributos = extrair_atributos(texto_gabinete)

    print("Saída:")
    for atributo, valor in atributos.items():
        print(f"{atributo}: {valor}")
