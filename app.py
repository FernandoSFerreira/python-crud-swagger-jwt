import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger import swagger
from dotenv import load_dotenv
from controllers.user import UserResource, UserListResource
from controllers.auth import AuthResource
from models.database import db
from seed import create_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['JWT_SECRET_KEY'] = 'seu_jwt_secret_key_aqui'

# Inicializar o objeto db com a instância do Flask
db.init_app(app)
# Criar a tabela "user" no banco de dados
@app.before_request
def create_tables():
    db.create_all()
    create_user()  # Chama a função para criar o usuário inicial

jwt = JWTManager(app)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do Swagger
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': os.getenv('APP_NAME', 'User CRUD API')
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
api = Api(app)# Configurar o Swagger

# Adicione os recursos de usuário à API
api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(UserListResource, '/user')
api.add_resource(AuthResource, '/auth/login')

@app.route("/swagger.json")
def swagger_json():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = os.getenv('INFO_VERSION', '1.0')
    swag['info']['title'] = os.getenv('INFO_TITLE', 'User CRUD API')
    swag['info']['description'] = os.getenv('INFO_DESCRIPTION', 'Descrição')
    swag['security'] = [{'Bearer': []}]
    # Incluindo a autorização JWT no Swagger
    swag['securityDefinitions'] = {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
    # Adicionando a propriedade "security" vazia para as rotas específicas
    no_auth_required_paths = ['/auth/login']
    for path in no_auth_required_paths:
        if path in swag['paths']:
            for method, method_data in swag['paths'][path].items():
                method_data['security'] = []

    return jsonify(swag)

if __name__ == '__main__':
    host_x = os.getenv('HOST', '127.0.0.1')
    port_x=int(os.getenv('PORT', 5000))
    debug_x=bool(os.getenv('DEBUG', True))
    app.run(host=host_x, port=port_x, debug=debug_x)
