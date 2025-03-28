﻿

```markdown
# Chatbot Cidades do Brasil

## Introdução

Este projeto implementa um chatbot interativo que fornece informações sobre cidades do Brasil. A solução utiliza o modelo `ChatGroq` para processar as perguntas do usuário e retornar dados como população, pontos turísticos e a principal universidade de cada cidade. O chatbot mantém o histórico das conversas para tornar as interações contínuas e personalizadas.

### Objetivo

O objetivo deste projeto é fornecer um assistente virtual que responda perguntas sobre cidades brasileiras com base em um conjunto de dados predefinido. O sistema permite que o usuário pergunte sobre várias cidades e receba informações como:

- **População**: A população estimada da cidade.
- **Pontos turísticos**: Lista de pontos turísticos famosos da cidade.
- **Universidade**: A principal universidade da cidade.

## Sumário

1. [Glossário](#glossário)
2. [Pré-requisitos](#pré-requisitos)
3. [Como usar o projeto](#como-usar-o-projeto)
4. [Explicação dos blocos de código](#explicação-dos-blocos-de-código)
5. [Como instalar as dependências](#como-instalar-as-dependências)
6. [GitHub e Repositório](#github-e-repositório)

## Glossário

- **Chatbot**: Programa que simula uma conversa com o usuário, geralmente utilizando inteligência artificial.
- **API Key**: Chave de autenticação usada para acessar a API do `ChatGroq`.
- **Streamlit**: Framework utilizado para criar interfaces web de forma rápida com Python.
- **Historico de Mensagens**: Armazenamento de mensagens trocadas durante a interação com o chatbot.

## Pré-requisitos

Antes de rodar o projeto, você precisa ter o Python instalado em sua máquina. Você pode verificar se o Python está instalado com o seguinte comando:

```bash
python --version
```

Se não estiver instalado, baixe e instale o Python [aqui](https://www.python.org/downloads/).

Além disso, será necessário ter um editor de código, como o [VS Code](https://code.visualstudio.com/).

## Como usar o projeto

1. **Clone o repositório**:

   Para começar, clone o repositório para sua máquina:

   ```bash
   git clone https://github.com/seu-usuario/chatbot-cidades-do-brasil.git
   cd chatbot-cidades-do-brasil
   ```

2. **Instale o ambiente virtual (venv)**:

   Um ambiente virtual isola as dependências do seu projeto de outras versões de bibliotecas que você possa ter no seu sistema. Para configurar o ambiente virtual, execute os seguintes comandos:

   ```bash
   python -m venv venv
   ```

   Para ativar o ambiente virtual, use o comando:

   - **No Windows**:

     ```bash
     .\venv\Scripts\activate
     ```

   - **No Linux/MacOS**:

     ```bash
     source venv/bin/activate
     ```

3. **Instale as dependências**:

   As dependências do projeto estão listadas no arquivo `requirements.txt`. Para instalá-las, execute:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuração das variáveis de ambiente**:

   O arquivo `.env` contém uma variável importante para o funcionamento do chatbot. Você precisa preencher a chave da API do `ChatGroq`. Substitua `<chave do usuário>` pela sua chave API no arquivo `.env`:

   ```
   GROQ_API_KEY=<chave do usuário>
   ```

5. **Execute o aplicativo**:

   Para rodar o chatbot com a interface gráfica, use o seguinte comando:

   ```bash
   streamlit run app.py
   ```

   Isso abrirá uma interface web local onde você pode interagir com o chatbot.

## Explicação dos blocos de código

### Arquivo `.env`

Este arquivo contém variáveis de ambiente usadas para armazenar informações sensíveis, como a chave da API. Exemplo:

```env
GROQ_API_KEY=<chave do usuário>
```

A chave da API é usada para autenticar o acesso ao serviço do `ChatGroq`.

### Arquivo `.gitignore`

O arquivo `.gitignore` é usado para garantir que arquivos não importantes, como o diretório do ambiente virtual (`venv/`) e o arquivo de variáveis de ambiente (`.env`), não sejam enviados ao repositório Git:

```bash
venv/
.env
```

### Arquivo `requirements.txt`

Este arquivo contém uma lista de bibliotecas que o projeto necessita para rodar corretamente. Aqui estão algumas das bibliotecas listadas:

```txt
absl-py==2.2.0
aiohttp==3.11.14
langchain==0.3.21
streamlit==1.44.0
groq==0.20.0
```

Essas bibliotecas são responsáveis pela execução do chatbot, manipulação de dados e interação com o modelo de IA.

### Arquivo `main.py`

O `main.py` contém a lógica principal do chatbot. Ele carrega a chave da API, configura o modelo `ChatGroq`, define a estrutura das mensagens e mantém o histórico de interações. Exemplo de código relevante:

```python
# Carregar as variáveis de ambiente do arquvo .env
load_dotenv(find_dotenv())

# Obter a chave da API do GROQ armazenada no arquivo .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

### Arquivo `app.py`

O `app.py` é responsável pela interface web utilizando o Streamlit. Ele exibe o chatbot e captura as mensagens do usuário. Exemplo de código relevante:

```python
import streamlit as st
from main import chatbot, get_session_history

st.set_page_config(page_title="Chatbot Cidades do Brasil", layout="wide")

# Recuperar histórico real do chatbot
history = get_session_history(st.session_state.session_id)
```

## Como instalar as dependências

1. **Criar um ambiente virtual**:

   Se você ainda não criou o ambiente virtual, faça isso com o seguinte comando:

   ```bash
   python -m venv venv
   ```

2. **Ativar o ambiente virtual**:

   - **Windows**: `.\\venv\\Scripts\\activate`
   - **Linux/MacOS**: `source venv/bin/activate`

3. **Instalar as dependências**:

   Use o comando abaixo para instalar todas as bibliotecas necessárias:

   ```bash
   pip install -r requirements.txt
   ```

4. **Rodar o aplicativo**:

   Após a instalação das dependências, execute o seguinte comando para iniciar a interface do chatbot:

   ```bash
   streamlit run app.py
   ```

## GitHub e Repositório

O código-fonte completo está disponível no GitHub. Fique à vontade para contribuir, sugerir melhorias ou relatar problemas!

- [Repositório GitHub](https://github.com/mrkekinha/ChatBot-With-CityInformation)
---

Obrigado por usar este chatbot! Se você tiver dúvidas ou sugestões, sinta-se à vontade para abrir uma issue ou enviar um pull request. :)
```

Esse `README.md` oferece uma explicação clara e acessível sobre como utilizar o projeto e o que cada parte do código faz. Além disso, ele fornece uma introdução básica para quem não tem experiência com programação.

Este Projeto foi elaborado pelo grupo 6 "BOT 6" . 
