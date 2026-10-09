import math
import numpy as np


def negativo(imagem):
    altura, largura = imagem.shape
    resultado = np.zeros((altura, largura), dtype=np.uint8)

    for linha in range(altura):
        for coluna in range(largura):
            r = int(imagem[linha, coluna])
            resultado[linha, coluna] = 255 - r

    return resultado


def limiarizar(imagem, limiar):
    altura, largura = imagem.shape
    resultado = np.zeros((altura, largura), dtype=np.uint8)

    for linha in range(altura):
        for coluna in range(largura):
            r = int(imagem[linha, coluna])

            if r < limiar:
                resultado[linha, coluna] = 0
            else:
                resultado[linha, coluna] = 255

    return resultado


def transformar_gamma(imagem, gamma):
    if gamma <= 0:
        raise ValueError("Gamma deve ser maior que zero.")

    altura, largura = imagem.shape
    resultado = np.zeros((altura, largura), dtype=np.uint8)

    for linha in range(altura):
        for coluna in range(largura):
            r = int(imagem[linha, coluna])
            normalizado = r / 255.0
            s = 255.0 * (normalizado ** gamma)
            resultado[linha, coluna] = round(s)

    return resultado


def transformar_log(imagem):
    altura, largura = imagem.shape
    resultado = np.zeros((altura, largura), dtype=np.uint8)
    c = 255.0 / math.log(256.0)

    for linha in range(altura):
        for coluna in range(largura):
            r = int(imagem[linha, coluna])
            s = c * math.log(1.0 + r)
            resultado[linha, coluna] = round(s)

    return resultado