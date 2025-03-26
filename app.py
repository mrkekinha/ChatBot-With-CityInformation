import streamlit as st
from main import chatbot, get_session_history

st.set_page_config(page_title="Chatbot Cidades do Brasil", layout="wide")

# Inicializar sessão e histórico
if "session_id" not in st.session_state:
    st.session_state.session_id = "chat1"

if "messages" not in st.session_state:
    st.session_state.messages = []  # Lista para armazenar as mensagens já exibidas

# Recuperar histórico real do chatbot
history = get_session_history(st.session_state.session_id)

st.title("🤖 Chatbot sobre Cidades do Brasil")

# Exibindo histórico de mensagens já armazenadas
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Caixa de entrada do usuário
user_input = st.chat_input("Digite sua mensagem...")

if user_input:
    with st.chat_message("human"):
        st.write(user_input)
    
    # Enviar mensagem para o chatbot
    bot_reply = chatbot(st.session_state.session_id, user_input)
    
    # Adicionar ao histórico do chatbot
    history.add_user_message(user_input)
    history.add_ai_message(bot_reply)
    
    # Atualizando as mensagens para evitar repetição na exibição
    st.session_state.messages.append({"role": "human", "content": user_input})
    st.session_state.messages.append({"role": "ai", "content": bot_reply})
    
    # Exibindo resposta no chat
    with st.chat_message("ai"):
        st.write(bot_reply)