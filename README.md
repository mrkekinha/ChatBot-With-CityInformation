# ChatBot-With-CityInformation
# Chatbot de Informações sobre Cidades do Brasil

## 📌 Introdução
Este projeto consiste em um chatbot que responde a perguntas sobre cidades do Brasil. Ele consegue identificar a cidade mencionada pelo usuário e retorna informações relevantes, como população, pontos turísticos e universidades. O chatbot mantém um histórico de conversas para lembrar interações anteriores.

Este README detalha cada parte do código, explicando de forma acessível.

---

## 📖 Sumário
1. [Tecnologias Utilizadas](#tecnologias-utilizadas)
2. [Dicionário de Funções](#dicionário-de-funções)
3. [Explicação do Código](#explicação-do-código)
   - [Importação de Bibliotecas](#1-importação-de-bibliotecas)
   - [Configuração do Modelo de IA](#2-configuração-do-modelo-de-ia)
   - [Banco de Dados das Cidades](#3-banco-de-dados-das-cidades)
   - [Gerenciamento do Histórico](#4-gerenciamento-do-histórico)
   - [Busca de Informações da Cidade](#5-busca-de-informações-da-cidade)
   - [Estrutura do Chatbot](#6-estrutura-do-chatbot)
   - [Execução do Chatbot](#7-execução-do-chatbot)
4. [Como Rodar o Projeto](#como-rodar-o-projeto)

---

## 🛠 Tecnologias Utilizadas
- **Python** → Linguagem principal do projeto
- **LangChain** → Gerencia interações com o modelo de IA
- **Dotenv** → Gerencia variáveis de ambiente
- **Groq API** → Modelo de IA utilizado no chatbot

---

## 📚 Dicionário de Funções

### 📌 Bibliotecas Utilizadas
- `os.getenv("VARIAVEL")`: Obtém uma variável de ambiente.
- `load_dotenv()`: Carrega variáveis do arquivo `.env`.
- `ChatGroq()`: Inicializa o modelo de IA.
- `ChatMessageHistory()`: Gerencia o histórico das conversas.
- `RunnableWithMessageHistory()`: Executa o modelo mantendo o histórico.

### 📌 Funções Criadas
- `get_session_history(session_id)`: Cria ou recupera o histórico de conversas para cada usuário.
- `get_city_info(city)`: Busca informações sobre uma cidade no banco de dados.
- `chatbot(session_id, user_message)`: Processa a mensagem do usuário e retorna uma resposta.

---

## 🔍 Explicação do Código

### 1️⃣ Importação de Bibliotecas
```python
import os
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from operator import itemgetter
```
- Importamos bibliotecas essenciais para:
  - Manipular variáveis de ambiente (`dotenv`)
  - Interagir com IA (`langchain_groq`)
  - Gerenciar histórico de mensagens (`ChatMessageHistory`)

### 2️⃣ Configuração do Modelo de IA
```python
load_dotenv(find_dotenv())
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
model = ChatGroq(model="gemma-2b-it", groq_api_key=GROQ_API_KEY)
```
- Carregamos a chave da API do arquivo `.env`.
- Inicializamos o modelo de IA `gemma-2b-it`.

### 3️⃣ Banco de Dados das Cidades   (Resumido)
```python
city_data = {
    "São Paulo": {
        "população": "12,33 milhões",
        "pontos_turisticos": ["Parque Ibirapuera", "Avenida Paulista", "Mercado Municipal"],
        "universidade": "Universidade de São Paulo (USP)"
    },
    "Rio de Janeiro": {
        "população": "6,7 milhões",
        "pontos_turisticos": ["Cristo Redentor", "Pão de Açúcar", "Praia de Copacabana"],
        "universidade": "Universidade Federal do Rio de Janeiro (UFRJ)"
    }
}
```
- Criamos um dicionário `city_data` contendo informações de cidades brasileiras.

### 4️⃣ Gerenciamento do Histórico
```python
store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
```
- `store`: Dicionário para armazenar histórico de cada usuário.
- `get_session_history()`: Retorna o histórico da sessão ou cria um novo.

### 5️⃣ Busca de Informações da Cidade
```python
def get_city_info(city: str) -> str:
    for nome_cidade in city_data.keys():
        if nome_cidade.lower() in city.lower():
            info = city_data[nome_cidade]
            return (
                f"A cidade de {nome_cidade} tem uma população de {info['população']}. "
                f"Seus principais pontos turísticos são {', '.join(info['pontos_turisticos'])}. "
                f"A principal universidade da cidade é {info['universidade']}."
            )
    return "Desculpe, eu não tenho informações sobre essa cidade."
```
- Percorre o dicionário `city_data` e verifica se a cidade mencionada está na lista.

### 6️⃣ Estrutura do Chatbot
```python
def chatbot(session_id: str, user_message: str) -> str:
    history = get_session_history(session_id)
    history.add_user_message(user_message)
    response_text = get_city_info(user_message)
    history.add_ai_message(response_text)
    return response_text
```
- Obtém o histórico da sessão.
- Adiciona a mensagem do usuário.
- Busca informações da cidade.
- Retorna a resposta gerada.

### 7️⃣ Execução do Chatbot
```python
if __name__ == "__main__":
    session_id = "chat1"
    print("Bem-vindo ao Chatbot sobre cidades do Brasil! Digite 'sair' para encerrar.")
    while True:
        user_input = input("Você: ")
        if user_input.lower() == "sair":
            print("Chatbot encerrado. Até mais!")
            break
        resposta = chatbot(session_id, user_input)
        print("Chatbot:", resposta)
```
- Inicia um chat interativo no terminal.
- O usuário digita perguntas e recebe respostas sobre cidades.
- O chat continua até o usuário digitar "sair".

---

## ▶️ Como Rodar o Projeto
1. Instale as dependências:
   ```bash
   pip install langchain langchain_groq python-dotenv
   ```
2. Crie um arquivo `.env` com sua chave da API:
   ```bash
   GROQ_API_KEY=your_api_key_here
   ```
3. Execute o código:
   ```bash
   python chatbot.py
   ```

Agora você pode conversar com o chatbot e obter informações sobre cidades brasileiras! 🚀