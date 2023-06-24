from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from models.user import User
    
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