import statistics
import hfpy_utils

CHARTS = "charts/"
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
        if ":" in t:    
            minutos, resto = t.split(":")
            segundos, centesimos = resto.split(".")
        
        else:
            minutos = 0
            segundos, centesimos = t.split(".")

        int_conversao = ((int(minutos) * 60 * 100) + (int(segundos) * 100) + (int(centesimos)))
        convercoes.append(int_conversao)

    # 4. Calcula a média (mantendo em centésimos como inteiro)
    media_centesimos = round(statistics.mean(convercoes))

    # 5. Reconverte de centésimos para o formato MM:SS.hh de forma segura

    #Centesimos -> Minutos
    minutos = media_centesimos // (60 * 100)

    #Centesimos -> segundos com os min`s inclusos
    resto_segundos = media_centesimos % (60 * 100)

    #Segundos retirando os minutos (ex.: 80 segundos - 1 min = 20 segundos) 
    segundos = resto_segundos // 100
    
    #O resto dos segundos, ou seja o que vem depois da vírgula são os centésimos 
    centesimos = resto_segundos % 100   

    # O formato :02d garante que números menores que 10 ganhem um zero à esquerda (ex: 05)
    media_formatada = f"{minutos}:{segundos:02d}.{centesimos:02d}"

    #Comando de retorno de valores da função
    return nome, categoria, distancia, estilo, tempos, media_formatada, convercoes

def produce_bar_chart(fn):
    #Descompacto as variaveis que vou utilizar
    (swimmer, age, distance, stroke, times, average, converts) = read_swim_data(fn)

    #Uso f'string, uma maneira mais eficiente de declarar variaveis em uma string
    title = f"{swimmer} (Under {age}) {distance} {stroke}"

    header = f"""<!DOCTYPE html>
    <html>
        <head>
            <title>
                {title}
            </title>
         </head>
         <body>
            <h3>{title}</h3>"""
    
    #Crio uma variavel para guardar o maior valor da lista de converções
    from_max = max(converts)

    #Crio uma variavel vazia que irá ser substituida pelo código em HTML
    body = ""

    #Uso o reverse para reverter a ordem dos tempos e das barras do grafico, assim como o projeto é descrito
    times.reverse()
    converts.reverse()

    #Loop para utilizar a função do módulo "hfpy_utils" para a converção dos valores para o intervalo desejado (0 a 400)
    for n,t in enumerate(times):
        bar_windth = hfpy_utils.convert2range(converts[n], 0, from_max, 0, 350)
        body = body + f"""
                        <svg height="30" width="400">
                            <rect height="30" width="{bar_windth}" style="fill:rgb(0,0,255);" />
                        </svg> {t} <br />
                    """
    #Crio uma variavel para escrever o rodapé do código em HTML
    footer = f"""
            <p>Average time: {average}</p>
        </body>
    </html>
    """
    page = header + body + footer

    save_to = f"charts/{fn.removesuffix(".txt")}.html"

    #Uso BIF open para salvar a variavel page no arquivo com nome descrito pela variavel save_to
    #o "w" significa o padrão de gravação de arquivos, e o "a"(não utilizado no momento) é de anexação
    with open(save_to, "w") as sf:
        print(page, file = sf)
    
    return save_to