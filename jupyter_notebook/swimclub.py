import statistics

FOLDER = "swimdata/"

def read_swim_data(filename):
    # 1. Desestrutura o nome do arquivo
    nome, categoria, distancia, estilo = filename.removesuffix(".txt").split("-")

    # 2. Lê os tempos do arquivo
    with open(FOLDER + filename, "r") as arquivo: #O "r" nessa linha é para indicar que o arquivo será apenas lido(read) e não modificado
        linhas = arquivo.readlines()
        tempos = linhas[0].strip().split(",")

    # 3. Converte os tempos para centésimos de segundo (inteiros)
    convercoes = []
    for t in tempos:
        minutos, resto = t.split(":")
        segundos, centesimos = resto.split(".")
        int_conversao = (
            (int(minutos) * 60 * 100) + (int(segundos) * 100) + (int(centesimos))
        )
        convercoes.append(int_conversao)

    # 4. Calcula a média (mantendo em centésimos como inteiro)
    media_centesimos = round(statistics.mean(convercoes))

    # 5. Reconverte de centésimos para o formato MM:SS.hh de forma segura
    minutos = media_centesimos // 6000
    resto_segundos = media_centesimos % 6000
    segundos = resto_segundos // 100
    centesimos = resto_segundos % 100

    # O formato :02d garante que números menores que 10 ganhem um zero à esquerda (ex: 05)
    media_formatada = f"{minutos}:{segundos:02d}.{centesimos:02d}"

    #Comando de retorno de valores da função
    return nome, categoria, distancia, estilo, tempos, media_formatada