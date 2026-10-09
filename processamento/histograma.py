import numpy as np


def calcular_histograma(imagem):
    contagens = [0] * 256
    altura, largura = imagem.shape

    for linha in range(altura):
        for coluna in range(largura):
            nivel = int(imagem[linha, coluna])
            contagens[nivel] += 1

    return contagens


def expandir_histograma(imagem):
    altura, largura = imagem.shape
    menor = int(imagem[0, 0])
    maior = menor

    for linha in range(altura):
        for coluna in range(largura):
            r = int(imagem[linha, coluna])
            if r < menor:
                menor = r
            if r > maior:
                maior = r

    if maior == menor:
        return imagem.copy()

    resultado = np.zeros((altura, largura), dtype=np.uint8)

    for linha in range(altura):
        for coluna in range(largura):
            r = int(imagem[linha, coluna])
            s = 255.0 * (r - menor) / (maior - menor)
            resultado[linha, coluna] = round(s)

    return resultado


def equalizar_histograma(imagem):
    contagens = calcular_histograma(imagem)
    altura, largura = imagem.shape
    total = altura * largura
    acumulado = 0
    tabela = [0] * 256

    for nivel in range(256):
        acumulado += contagens[nivel]
        tabela[nivel] = round(255.0 * acumulado / total)

    resultado = np.zeros((altura, largura), dtype=np.uint8)

    for linha in range(altura):
        for coluna in range(largura):
            r = int(imagem[linha, coluna])
            resultado[linha, coluna] = tabela[r]

    return resultado