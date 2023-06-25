# python-crud-swagger-jwt
## _Demonstration of a Basic DB operations using swagger with JWT authentucation._
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/downloads/release/python-380/)
[![Python Version](https://img.shields.io/badge/Python-3.8-blue.svg?logo=python)](https://www.python.org/downloads/release/python-380/) [![Docker Images](https://img.shields.io/badge/Docker-Images-blue.svg?logo=docker)](https://www.docker.com/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![SQLite](https://img.shields.io/badge/SQLite-Database-blue.svg?logo=sqlite)](https://www.sqlite.org/)

Simples projeto de API para demonstração de operações CRUD, com swagger para simples testes e autenticação JWT (Bearer Token).
Pode ser usado como  start para outros projetos.

## Features

- Login
- List All Users
- Create a new User
- Get User by ID
- Delete User by ID

Projeto desenvolvido por [Fernando S Ferreira].
> O encontro da preparação com a oportunidade gera o rebento que chamamos sorte.

## Tech

Esse projeto usa as seguintes bibliotecas:

- [Flask 2.3.2] - Flask==2.3.2
- [Flask-JWT-Extended 4.5.2] - Flask_JWT_Extended==4.5.2
- [Flask-RESTful 0.3.10] - Flask_RESTful==0.3.10
- [Flask-SQLAlchemy 3.0.5] - flask_sqlalchemy==3.0.5
- [flask-swagger 0.2.14] - flask_swagger==0.2.14
- [flask-swagger-ui 4.11.1] - flask_swagger_ui==4.11.1
- [python-dotenv 1.0.0] - python-dotenv==1.0.0

## Installation and run

Criar virtual environment.
```sh
py -m venv venv
```
Ativar virtual environment.
```sh
venv\Scripts\activate
```
Instalar dependências.
```sh
py -m pip install -r requirements.txt
```
Executar.
```sh
py app.py
```

> Ao executar o projeto, o arquivo seed.py é chamado para a criação de um usuário inicial:
> username = "Ferreira"
> password = "q1w2e3r4"

## Docker
Esse projeto tem um arquivo `Dockerfile` e um arquivo `docker-compose.yml`, dessa forma é possível executar no docker com apenas `01` comando.
```sh
docker-compose up -d
```
> Note: - Por padrão o projeto execua em [localhost:5000](http://localhost:5000)
> O swagger para teste da api pode ser acessado em [localhost:5000/swagger](http://localhost:5000/swagger/#/)

## License

MIT

**Free Software, Hell Yeah!**

   [Fernando S Ferreira]: <https://github.com/FernandoSFerreira/>
   [Flask 2.3.2]: <https://pypi.org/project/Flask/2.3.2/>
   [Flask-JWT-Extended 4.5.2]: <https://pypi.org/project/Flask-JWT-Extended/4.5.2/>
   [Flask-RESTful 0.3.10]: <https://pypi.org/project/Flask-RESTful/0.3.10/>
   [Flask-SQLAlchemy 3.0.5]: <https://pypi.org/project/Flask-SQLAlchemy/3.0.5/>
   [flask-swagger 0.2.14]: <https://pypi.org/project/flask-swagger/0.2.14/>
   [flask-swagger-ui 4.11.1]: <https://pypi.org/project/flask-swagger-ui/4.11.1/>
   [python-dotenv 1.0.0]: <https://pypi.org/project/python-dotenv/1.0.0/>
