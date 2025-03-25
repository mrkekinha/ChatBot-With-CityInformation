# IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS
#bibliotecas responsáveis por gerenciar as variáveis do ambiente:
import os                                                                       
from dotenv import load_dotenv, find_dotenv

#integra o langchain com o modelo de linguagem do GROQ
from langchain_groq import ChatGroq

#gerenciam o historico de mensagens 
from langchain_community.chat_message_histories import ChatMessageHistory           #Armazenamento de mensagem de chat
from langchain_core.chat_history import BaseChatMessageHistory 
from langchain_core.runnables.history import RunnableWithMessageHistory             #Envolve um modelo de chat para manter o histórico de interações.

#responsável pelo uso de prompt de template
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter

# Carregar as variáveis de ambiente do arquvo .env
load_dotenv(find_dotenv())

# Obter a chave da API do GROQ armazenada no arquivo .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Inicializar o modelo de AI utilizando a API da GROQ
model = ChatGroq(
    model="gemma2-9b-it",
    groq_api_key=GROQ_API_KEY
)

# criando o dicionario de infos das cidades
city_data = {
    "São Paulo": {
        "população": "12,33 milhões",
        "pontos_turisticos": ["Parque Ibirapuera", "Avenida Paulista", "Mercado Municipal", "Catedral da Sé"],
        "universidade": "Universidade de São Paulo (USP)"
    },
    "Rio de Janeiro": {
        "população": "6,7 milhões",
        "pontos_turisticos": ["Cristo Redentor", "Pão de Açúcar", "Praia de Copacabana"],
        "universidade": "Universidade Federal do Rio de Janeiro (UFRJ)"
    },
    "Salvador": {
        "população": "2,9 milhões",
        "pontos_turisticos": ["Pelourinho", "Elevador Lacerda", "Farol da Barra"],
        "universidade": "Universidade Federal da Bahia (UFBA)"
    },
    "Belo Horizonte": {
        "população": "2,5 milhões",
        "pontos_turisticos": ["Praça da Liberdade", "Igreja São José", "Museu de Artes e Ofícios"],
        "universidade": "Universidade Federal de Minas Gerais (UFMG)"
    },
    "Fortaleza": {
        "população": "2,7 milhões",
        "pontos_turisticos": ["Praia do Futuro", "Catedral Metropolitana", "Mercado Central"],
        "universidade": "Universidade Federal do Ceará (UFC)"
    },
    "Brasília": {
        "população": "3,1 milhões",
        "pontos_turisticos": ["Congresso Nacional", "Catedral de Brasília", "Palácio do Planalto"],
        "universidade": "Universidade de Brasília (UnB)"
    },
    "Curitiba": {
        "população": "1,9 milhões",
        "pontos_turisticos": ["Jardim Botânico", "Ópera de Arame", "Rua XV de Novembro"],
        "universidade": "Universidade Federal do Paraná (UFPR)"
    },
    "Porto Alegre": {
        "população": "1,5 milhões",
        "pontos_turisticos": ["Parque Redenção", "Caminho dos Antiquários", "Fundação Ibere Camargo"],
        "universidade": "Universidade Federal do Rio Grande do Sul (UFRGS)"
    },
    "Recife": {
        "população": "1,6 milhões",
        "pontos_turisticos": ["Praia de Boa Viagem", "Instituto Ricardo Brennand", "Marco Zero"],
        "universidade": "Universidade Federal de Pernambuco (UFPE)"
    },
    "Manaus": {
        "população": "2,1 milhões",
        "pontos_turisticos": ["Teatro Amazonas", "Encontro das Águas", "Palácio Rio Negro"],
        "universidade": "Universidade Federal do Amazonas (UFAM)"
    },
    "Natal": {
        "população": "1,4 milhões",
        "pontos_turisticos": ["Forte dos Reis Magos", "Praia de Ponta Negra", "Dunas de Genipabu"],
        "universidade": "Universidade Federal do Rio Grande do Norte (UFRN)"
    },
    "Maceió": {
        "população": "1,0 milhão",
        "pontos_turisticos": ["Praia do Francês", "Palácio Marechal Floriano Peixoto", "Igreja de São Gonçalo do Amarante"],
        "universidade": "Universidade Federal de Alagoas (UFAL)"
    },
    "Cuiabá": {
        "população": "620 mil",
        "pontos_turisticos": ["Parque Nacional de Chapada dos Guimarães", "Catedral Basílica do Senhor Bom Jesus", "Museu do Morro da Caixa D'Água"],
        "universidade": "Universidade Federal de Mato Grosso (UFMT)"
    },
    "Aracaju": {
        "população": "650 mil",
        "pontos_turisticos": ["Praia de Atalaia", "Museu Palácio Marechal Floriano Peixoto", "Mercado Municipal"],
        "universidade": "Universidade Federal de Sergipe (UFS)"
    }
}

#model.invoke([HumanMessage(content="oi, eu moro em belo horizonte")]) #enviando a mensagem humana para processamento do modelo

# Cria armazenamento para os históricos de conversa
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Recupera ou cria um histórico de mensagens para um usuário específico."""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

"""O código acima define um dicionário store para armazenar históricos de mensagens. 
A função get_session_history recupera ou inicializa um histórico de mensagens para uma sessão específica."""

# with_message_history=RunnableWithMessageHistory(model,get_session_history)

"""A classe RunnableWithMessageHistory é usada para associar o histórico de mensagens ao modelo de IA, permitindo conversas com contexto."""

"""
config={"configurable":{"session_id":"chat1"}}
response=with_message_history.invoke(
    [HumanMessage(content="oi, gostaria de saber mais sobre belo horizonte")],
    config=config
)
response.content"""

"""A variável config define a sessão da conversa.
 O método invoke é chamado para enviar uma mensagem e obter uma resposta do modelo, utilizando o histórico armazenado."""

# Criar um prompt template para estruturar as mensagens do chatbot
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente que fornece informações sobre cidades do Brasil."),
        MessagesPlaceholder(variable_name="messages")
    ]
)

# Conectar o modelo ao prompt template
chain = prompt | model


def get_city_info(city: str):
    """Retorna informações sobre a cidade, se disponível."""
    if city in city_data:
        info = city_data[city]
        return f"A cidade de {city} tem uma população de {info['população']}. Seus principais pontos turísticos são {', '.join(info['pontos_turisticos'])}. A principal universidade da cidade é {info['universidade']}."
    else:
        return "Desculpe, eu não tenho informações sobre essa cidade."


# Criar um pipeline de execução otimizado
pipeline = (
    RunnablePassthrough.assign(messages=itemgetter("messages"))
    | prompt
    | model
)

def chatbot(session_id: str, user_message: str):
    """Processa a entrada do usuário e retorna a resposta do chatbot."""
    history = get_session_history(session_id)
    
    # Adicionar a nova mensagem ao histórico
    history.add_user_message(user_message)

    # Identificar a cidade mencionada
    response_text = get_city_info(user_message)

    # Adicionar a resposta do chatbot ao histórico
    history.add_ai_message(response_text)

    return response_text

if __name__ == "__main__":
    session_id = "chat1"  # Simulando uma sessão fixa

    print("Bem-vindo ao Chatbot sobre cidades do Brasil! Digite 'sair' para encerrar.")
    
    while True:
        user_input = input("Você: ")
        if user_input.lower() == "sair":
            print("Chatbot encerrado. Até mais!")
            break
        
        resposta = chatbot(session_id, user_input)
        print("Chatbot:", resposta)