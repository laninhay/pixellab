import numpy as np


def converter_para_cinza(imagem_pil):
    rgb = np.array(imagem_pil.convert("RGB"))
    altura, largura, canais = rgb.shape
    cinza = np.zeros((altura, largura), dtype=np.uint8)

    for linha in range(altura):
        for coluna in range(largura):
            vermelho = int(rgb[linha, coluna, 0])
            verde = int(rgb[linha, coluna, 1])
            azul = int(rgb[linha, coluna, 2])

            valor = 0.299 * vermelho + 0.587 * verde + 0.114 * azul
            cinza[linha, coluna] = round(valor)

    return cinza