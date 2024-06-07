# TP10 - Full Stack Development

Este projeto é a implementação de uma aplicação web completa que consiste em um sistema de gerenciamento de Hamburguers. O objetivo deste projeto é treinar as habilidades de desenvolvimento web, desde o backend (utilizando Python com Flask) até o frontend (utilizando Kivy com Python), passando pelo banco de dados (utilizando SQLite).

## Instalação

1. Crie uma máquina virtual com o `venv` utilizando o comando `python3 -m venv .myvenv` no terminal.
2. Reinicie o VSCode e ative a máquina virtual com o comando `activate` no terminal.
3. Instale as dependências com o comando `pip install -r requirements.txt` no terminal.
4. Preencha o banco de dados com o comando `python3 populate.py` no terminal.
5. Inicie o servidor com o comando `python3 app.py` no terminal.
6. Inicie o frontend com o comando `python main.py` no terminal.

## Execução

Esta aplicação web consiste em um sistema de gerenciamento de hamburguers. O backend utiliza o Flask para expor as funcionalidades da aplicação por meio de rotas (API). O frontend utiliza o Kivy para fornecer uma interface gráfica para o usuário. A comunicação entre o backend e o frontend é realizada por meio de requisições HTTP (GET, POST, DELETE, etc) que são realizadas através da biblioteca requests.

