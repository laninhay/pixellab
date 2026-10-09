from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError

from processamento.imagem import converter_para_cinza
from processamento.intensidade import (
    negativo,
    limiarizar,
    transformar_gamma,
    transformar_log,
)
from processamento.histograma import (
    calcular_histograma,
    expandir_histograma,
    equalizar_histograma,
)

st.set_page_config(page_title="PixelLab", page_icon="🔬", layout="wide")
st.title("🔬 PixelLab")
st.write("Laboratório de processamento de imagens em escala de cinza.")

origem = st.sidebar.radio(
    "Imagem de entrada",
    ["Matriz de exemplo", "Enviar imagem"],
)

if origem == "Matriz de exemplo":
    imagem = np.array([[0, 64], [128, 255]], dtype=np.uint8)
    st.info("Exemplo com 2 linhas e 2 colunas, para conferir os cálculos.")
else:
    arquivo = st.sidebar.file_uploader(
        "Escolha uma imagem",
        type=["png", "jpg", "jpeg", "bmp"],
    )

    if arquivo is None:
        st.info("Envie uma imagem pelo menu lateral.")
        st.stop()

    try:
        imagem_pil = Image.open(arquivo)
        imagem_pil = ImageOps.exif_transpose(imagem_pil)
        imagem = converter_para_cinza(imagem_pil)
    except (UnidentifiedImageError, OSError):
        st.error("Não foi possível abrir esse arquivo como imagem.")
        st.stop()

operacao = st.sidebar.selectbox(
    "Operação",
    [
        "Original",
        "Negativo",
        "Limiarização",
        "Gamma",
        "Logaritmo",
        "Expansão de histograma",
        "Equalização de histograma",
    ],
)

parametros = "Sem parâmetros ajustáveis."

if operacao == "Original":
    resultado = imagem.copy()
elif operacao == "Negativo":
    resultado = negativo(imagem)
elif operacao == "Limiarização":
    limiar = st.sidebar.slider("Limiar T", 0, 255, 128)
    resultado = limiarizar(imagem, limiar)
    parametros = f"T = {limiar}; valores iguais a T tornam-se brancos."
elif operacao == "Gamma":
    gamma = st.sidebar.slider("Gamma", 0.1, 3.0, 1.0, 0.1)
    resultado = transformar_gamma(imagem, gamma)
    parametros = f"Gamma = {gamma:.1f}; entrada normalizada para [0, 1]."
elif operacao == "Logaritmo":
    resultado = transformar_log(imagem)
    parametros = "s = 255 × ln(1 + r) / ln(256)."
elif operacao == "Expansão de histograma":
    resultado = expandir_histograma(imagem)
    parametros = "Mínimo → 0; máximo → 255. Imagem constante é preservada."
else:
    resultado = equalizar_histograma(imagem)
    parametros = "s = arredondar(255 × frequência acumulada relativa)."

st.caption(f"Operação: {operacao}. {parametros}")
altura, largura = imagem.shape
st.caption(f"Dimensões: {largura} × {altura} pixels. Escala de cinza de 8 bits.")

coluna_original, coluna_resultado = st.columns(2)
with coluna_original:
    st.image(imagem, caption="Original em cinza", width="stretch", output_format="PNG")
with coluna_resultado:
    st.image(resultado, caption="Resultado", width="stretch", output_format="PNG")

with st.expander("Ver valores dos pixels (até 8 × 8)"):
    st.write("Original: linhas e colunas começam em zero.")
    st.dataframe(imagem[:8, :8])
    st.write("Resultado:")
    st.dataframe(resultado[:8, :8])

hist_original = calcular_histograma(imagem)
hist_resultado = calcular_histograma(resultado)
figura, eixos = plt.subplots(1, 2, figsize=(10, 3))
pico = max(max(hist_original), max(hist_resultado))

for eixo, titulo, contagens in [
    (eixos[0], "Histograma original", hist_original),
    (eixos[1], "Histograma do resultado", hist_resultado),
]:
    eixo.bar(range(256), contagens, width=1.0)
    eixo.set_title(titulo)
    eixo.set_xlabel("Intensidade")
    eixo.set_ylabel("Quantidade de pixels")
    eixo.set_xlim(-0.5, 255.5)
    eixo.set_ylim(0, pico * 1.1)

figura.tight_layout()
st.pyplot(figura)
plt.close(figura)

buffer = BytesIO()
Image.fromarray(resultado).save(buffer, format="PNG")
st.download_button(
    "Baixar resultado em PNG",
    data=buffer.getvalue(),
    file_name="resultado_pixellab.png",
    mime="image/png",
)