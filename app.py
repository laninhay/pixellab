import streamlit as st

st.set_page_config(
    page_title="PixelLab",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 PixelLab")

st.write(
    "Laboratório de processamento de imagens em escala de cinza."
)

st.info(
    "Escolha uma operação para começar."
)

operacao = st.selectbox(
    "Qual operação você deseja estudar?",
    ["Negativo", "Limiarização", "Gamma"]
)

st.write("Operação selecionada:", operacao)

if st.button("Ver minha escolha"):
    st.success(f"Você escolheu: {operacao}")