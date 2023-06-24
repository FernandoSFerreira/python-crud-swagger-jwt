from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token
from datetime import datetime
from models.user import User, db

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
            'created_at': user.created_at.isoformat(),
            'access_token': create_access_token(identity=user.id)
        }
        return response, 201
