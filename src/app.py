import streamlit as st
from pathlib import Path

# Importações dos módulos customizados
from config import MODEL, DOCS_PATH, get_system_prompt
from utils.data_loader import load_files
from services.llm_service import chat_with_llm

st.set_page_config(
    page_title="My first chatbot",
    page_icon="🤖",
)

st.header("Bem-vindo ao ShieldMind!")

# --- Leitura dos arquivos (Contexto) ---
context = load_files(DOCS_PATH)

# --- Geração do System Prompt ---
system_prompt = get_system_prompt(context)

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["context"])

# --- Chat ---
# Campo de input do usuário
if prompt := st.chat_input("Digite sua mensagem:"):

    # Adiciona mensagem do usuário no histórico
    st.session_state.messages.append({"role": "user", "context": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chama o modelo e exibe a resposta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                reply = chat_with_llm(
                    model=MODEL,
                    system_prompt=system_prompt,
                    chat_history=st.session_state.messages
                )
                st.markdown(reply)
                
                # Adiciona resposta ao histórico
                st.session_state.messages.append({"role": "assistant", "context": reply})
            except Exception as e:
                st.error(f"Erro ao obter resposta da LLM: {e}")