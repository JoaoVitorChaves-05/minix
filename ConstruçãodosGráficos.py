import math
import matplotlib.pyplot as plt
import numpy as np
import os

def estatisticas(vetor):
    if not vetor:
        return {"media": 0, "mediana": 0, "maximo": 0, "desvio_padrao": 0}
    n = len(vetor)
    media = sum(vetor) / n
    vetor_ordenado = sorted(vetor)
    if n % 2 == 0:
        mediana = (vetor_ordenado[n // 2 - 1] + vetor_ordenado[n // 2]) / 2
    else:
        mediana = vetor_ordenado[n // 2]
    variancia = sum((v - media) ** 2 for v in vetor) / n
    desvio_padrao = math.sqrt(variancia)
    return {
        "media": media,
        "mediana": mediana,
        "maximo": max(vetor),
        "desvio_padrao": desvio_padrao
    }

BASE = "."

algoritmos = {#aqui baseia no nome do arquivo fonte utilizado para as medias, esses arquvios estão no git, esses nomes
    #que estão aqui são do momento em que gerei os gráficos, posteriormente, mudei seus nomes no git.
    "Padrao": [
        f"{BASE}/resultados/padrao/v2/resultados_01.txt",
        f"{BASE}/resultados/padrao/v2/resultados_02.txt",
        f"{BASE}/resultados/padrao/v2/resultados_03.txt",
        f"{BASE}/resultados/padrao/v2/resultados_04.txt",
    ],
    "FCFS v2": [
        f"{BASE}/resultados/fcfs/v2/resultados_01.txt",
        f"{BASE}/resultados/fcfs/v2/resultados_02.txt",
        f"{BASE}/resultados/fcfs/v2/resultados_03.txt",
        f"{BASE}/resultados/fcfs/v2/resultados_04.txt",
    ],
    "Round Robin": [
        f"{BASE}/resultados/round_robin/v2/resultados_01.txt",
        f"{BASE}/resultados/round_robin/v2/resultados_02.txt",
        f"{BASE}/resultados/round_robin/v2/resultados_03.txt",
        f"{BASE}/resultados/round_robin/v2/resultados_04.txt",
    ],
    "Lottery": [
        f"{BASE}/resultados/lottery/v2/resultados_01.txt",
        f"{BASE}/resultados/lottery/v2/resultados_02.txt",
        f"{BASE}/resultados/lottery/v2/resultados_03.txt",
        f"{BASE}/resultados/lottery/v2/resultados_04.txt",
    ],
}

cenarios = [10, 50, 100, 200]

dados_cpu_media    = {}
dados_cpu_mediana  = {}
dados_cpu_maximo   = {}
dados_cpu_desvio   = {}
dados_io_media     = {}
dados_io_mediana   = {}
dados_io_maximo    = {}
dados_io_desvio    = {}

for nome, arquivos in algoritmos.items():
    medias_cpu = []; medianas_cpu = []; maximos_cpu = []; desvios_cpu = []
    medias_io  = []; medianas_io  = []; maximos_io  = []; desvios_io  = []

    for arquivo in arquivos:
        cpu_tempos = []
        io_tempos  = []

        if not os.path.exists(arquivo):
            print(f"AVISO: arquivo nao encontrado: {arquivo}")
            medias_cpu.append(0); medianas_cpu.append(0)
            maximos_cpu.append(0); desvios_cpu.append(0)
            medias_io.append(0);  medianas_io.append(0)
            maximos_io.append(0); desvios_io.append(0)
            continue

        with open(arquivo, "r") as f:
            for linha in f:
                partes = linha.split()
                if len(partes) != 3:
                    continue
                tipo, pid, tempo = partes
                tempo = float(tempo)
                if tipo == "CPU":
                    cpu_tempos.append(tempo)
                elif tipo == "IO":
                    io_tempos.append(tempo)

        est_cpu = estatisticas(cpu_tempos)
        est_io  = estatisticas(io_tempos)

        medias_cpu.append(est_cpu["media"])
        medianas_cpu.append(est_cpu["mediana"])
        maximos_cpu.append(est_cpu["maximo"])
        desvios_cpu.append(est_cpu["desvio_padrao"])

        medias_io.append(est_io["media"])
        medianas_io.append(est_io["mediana"])
        maximos_io.append(est_io["maximo"])
        desvios_io.append(est_io["desvio_padrao"])

    dados_cpu_media[nome]   = medias_cpu
    dados_cpu_mediana[nome] = medianas_cpu
    dados_cpu_maximo[nome]  = maximos_cpu
    dados_cpu_desvio[nome]  = desvios_cpu
    dados_io_media[nome]    = medias_io
    dados_io_mediana[nome]  = medianas_io
    dados_io_maximo[nome]   = maximos_io
    dados_io_desvio[nome]   = desvios_io

def plotar_grafico(titulo, ylabel, dados, limite_y=None, salvar=None):
    x = np.arange(len(cenarios))
    nomes = list(dados.keys())
    largura = 0.8 / len(nomes)
    cores = ["#2563EB", "#16A34A", "#DC2626", "#7C3AED"]

    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F1F5F9")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#CBD5E1", linewidth=0.6, linestyle="--", alpha=0.7)

    for i, (nome, cor) in enumerate(zip(nomes, cores)):
        deslocamento = (i - len(nomes) / 2) * largura + largura / 2
        ax.bar(x + deslocamento, dados[nome], largura, label=nome,
               color=cor, alpha=0.88, edgecolor="white")

    if limite_y:
        ax.set_ylim(limite_y)
    else:
        maior = max(max(v) for v in dados.values())
        ax.set_ylim(0, maior * 1.15)

    ax.set_title(titulo, fontweight="bold", fontsize=12)
    ax.set_xlabel("Numero de processos", fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(cenarios)
    ax.legend(fontsize=9)
    plt.tight_layout()
    if salvar:
        plt.savefig(salvar, dpi=150, bbox_inches="tight")
        print(f"Salvo: {salvar}")
    plt.show()

def plotar_grafico_geral(titulo, dados_cpu, dados_io, salvar=None):
    cores = ["#2563EB", "#16A34A", "#DC2626", "#7C3AED"]
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F1F5F9")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color="#CBD5E1", linewidth=0.6, linestyle="--", alpha=0.7)

    for nome, cor in zip(dados_cpu.keys(), cores):
        ax.plot(cenarios, dados_cpu[nome], marker="o", linestyle="-",
                color=cor, label=f"{nome} CPU")
        ax.plot(cenarios, dados_io[nome], marker="s", linestyle="--",
                color=cor, alpha=0.6, label=f"{nome} IO")

    ax.set_title(titulo, fontweight="bold", fontsize=12)
    ax.set_xlabel("Numero de processos", fontsize=10)
    ax.set_ylabel("Tempo medio (s)", fontsize=10)
    ax.set_xticks(cenarios)
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    if salvar:
        plt.savefig(salvar, dpi=150, bbox_inches="tight")
        print(f"Salvo: {salvar}")
    plt.show()

plotar_grafico("CPU-bound (Media)",        "Tempo medio CPU (s)",   dados_cpu_media,   salvar="cpu_media.png")
plotar_grafico("CPU-bound (Mediana)",      "Tempo mediano CPU (s)", dados_cpu_mediana, salvar="cpu_mediana.png")
plotar_grafico("CPU-bound (Maximo)",       "Tempo maximo CPU (s)",  dados_cpu_maximo,  salvar="cpu_maximo.png")
plotar_grafico("CPU-bound (Desvio Padrao)","Desvio padrao CPU",     dados_cpu_desvio,  salvar="cpu_desvio.png")

plotar_grafico("IO-bound (Media)",         "Tempo medio IO (s)",    dados_io_media,    salvar="io_media.png")
plotar_grafico("IO-bound (Mediana)",       "Tempo mediano IO (s)",  dados_io_mediana,  salvar="io_mediana.png")
plotar_grafico("IO-bound (Maximo)",        "Tempo maximo IO (s)",   dados_io_maximo,   salvar="io_maximo.png")
plotar_grafico("IO-bound (Desvio Padrao)", "Desvio padrao IO",      dados_io_desvio,   salvar="io_desvio.png")

plotar_grafico_geral("Comparacao Geral - Media",        dados_cpu_media,   dados_io_media,   salvar="geral_media.png")
plotar_grafico_geral("Comparacao Geral - Mediana",      dados_cpu_mediana, dados_io_mediana, salvar="geral_mediana.png")
plotar_grafico_geral("Comparacao Geral - Maximo",       dados_cpu_maximo,  dados_io_maximo,  salvar="geral_maximo.png")
plotar_grafico_geral("Comparacao Geral - Desvio Padrao",dados_cpu_desvio,  dados_io_desvio,  salvar="geral_desvio.png")

print("\nTodos os graficos gerados!")
