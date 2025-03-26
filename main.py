# IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS
#bibliotecas responsáveis por gerenciar as variáveis do ambiente:
import os                                                                          # interação com o sistema operacional                                                           
from dotenv import load_dotenv, find_dotenv                                        # carregamento e procura das variáveis de ambiente no .env

#integra o langchain com o modelo de linguagem do GROQ
from langchain_groq import ChatGroq                                                #vai permitir o uso do modelo gemma 2-9b-It

#gerenciam o historico de mensagens 
from langchain_community.chat_message_histories import ChatMessageHistory           #gerencia o historico de mensagens para armazenar interações
from langchain_core.chat_history import BaseChatMessageHistory                      #classe base para históricos de chat no LangChain
from langchain_core.runnables.history import RunnableWithMessageHistory             #Envolve um modelo de chat para manter o histórico de interações.

#responsável pelo uso de prompt de template
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  #estruturação de mensagens enviadas ao modelo de ia - chatprompt cria template de mensagens pre definidas e messagesplaceholder define um espaço reservado para as mensagens dinamicas

# Manipula diferentes tipos de mensagens usadas pelo chatbot
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages #human representa a mensagem do use, ai do modelo e system define regras gerais para o chatbot

#Cria fluxos de execução personalizados dentro do LangChain.
from langchain_core.runnables import RunnablePassthrough # Aplica transformações no histórico de mensagens antes de enviá-las ao modelo

#Facilita operações com dicionários e listas.
from operator import itemgetter #Obtém o valor da chave "messages" de um dicionário.

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



# Cria armazenamento para os históricos de conversa
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory: #classe base para manipulação do historico de mensagens
    """Recupera ou cria um histórico de mensagens para um usuário específico."""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()   #cria um historico de mensagens para armazenar interações
    return store[session_id]

"""O código acima define um dicionário store para armazenar históricos de mensagens. 
A função get_session_history recupera ou inicializa um histórico de mensagens para uma sessão específica."""

# Função para buscar informações da cidade
def get_city_info(city: str) -> str:
    """Retorna informações sobre a cidade se disponível."""
    for nome_cidade in city_data.keys():  
        if nome_cidade.lower() in city.lower():  # Verifica se a cidade está no input do usuário
            info = city_data[nome_cidade]
            return (
                f"A cidade de {nome_cidade} tem uma população de {info['população']}. "
                f"Seus principais pontos turísticos são {', '.join(info['pontos_turisticos'])}. "
                f"A principal universidade da cidade é {info['universidade']}."
            )
    return "Desculpe, eu não tenho informações sobre essa cidade."

# Criar um prompt template para estruturar as mensagens do chatbot
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente que fornece informações sobre cidades do Brasil."),
        MessagesPlaceholder(variable_name="messages") 
    ]
)

# Conectar o modelo ao prompt template
chain = prompt | model

# Criar um pipeline de execução
pipeline = (
    RunnableWithMessageHistory(model, get_session_history)
)

def chatbot(session_id: str, user_message: str) -> str:
    """Processa a entrada do usuário e retorna a resposta do chatbot."""
    history = get_session_history(session_id)
    
    # Adicionar a nova mensagem ao histórico
    history.add_user_message(user_message)

    # Identificar a cidade mencionada
    response_text = get_city_info(user_message)

    # Adicionar a resposta do chatbot ao histórico
    history.add_ai_message(response_text)

    return response_text

