from datetime import datetime
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger import swagger
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['JWT_SECRET_KEY'] = 'seu_jwt_secret_key_aqui'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Criar a tabela "user" no banco de dados
# with app.app_context():
#     db.create_all()
@app.before_request
def create_tables():
    db.create_all()

# Configuração do Swagger
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'User CRUD API'
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        """
        Get user by ID
        ---
        parameters:
          - name: user_id
            in: path
            description: ID of the user to retrieve
            required: true
            schema:
              type: integer
        tags: ['User']
        responses:
          200:
            description: User details
            schema:
              type: object
              properties:
                username:
                  type: string
                created_at:
                  type: string
                  format: date-time
        """
        user = User.query.get_or_404(user_id)
        return {'username': user.username, 'created_at': user.created_at.isoformat()}

    @jwt_required()
    def delete(self, user_id):
        """
        Delete user by ID
        ---
        parameters:
          - name: user_id
            in: path
            description: ID of the user to delete
            required: true
            schema:
              type: integer
        tags: ['User']
        responses:
          200:
            description: Success message
        """
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'Usuário deletado com sucesso'}

class UserListResource(Resource):
    @jwt_required()
    def get(self):
        """
        Get all users
        ---
        tags: ['User']
        responses:
          200:
            description: List of users
            schema:
              type: array
              items:
                type: object
                properties:
                  username:
                    type: string
                  created_at:
                    type: string
                    format: date-time
        """
        users = User.query.all()
        return [{
            'id': user.id,
            'username': user.username,
            'created_at': user.created_at.isoformat()
        } for user in users]

    @jwt_required()
    def post(self):
        """
        Create a new user
        ---
        parameters:
          - name: body
            in: body
            description: User object
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                password:
                  type: string
        tags: ['User']
        responses:
          201:
            description: Access token
            schema:
              type: object
              properties:
                access_token:
                  type: string
        """
        data = request.get_json()
        user = User(username=data['username'], password=data['password'], created_at=datetime.now())
        db.session.add(user)
        db.session.commit()
        response = {
            'id': user.id,
            'username': user.username,
            'created_at': user.created_at.isoformat(),  # Convertendo para string no formato ISO 8601
            'access_token': create_access_token(identity=user.id)
        }
        return response, 201
    
class AuthResource(Resource):
    def post(self):
        """
        User login
        ---
        parameters:
          - name: body
            in: body
            description: User login credentials
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                password:
                  type: string
        tags: ['Auth']
        responses:
          200:
            description: Access token
            schema:
              type: object
              properties:
                access_token:
                  type: string
        """
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200

        return {'message': 'Invalid username or password'}, 401

api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(UserListResource, '/user')
api.add_resource(AuthResource, '/auth/login')

@app.route("/swagger.json")
def swagger_json():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "User CRUD API"
    swag['info']['description'] = "Fernando Ferreira"
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
