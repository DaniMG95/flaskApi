import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser_user = reqparse.RequestParser()
    parser_user.add_argument('username', type=str, help='username is necesary')
    parser_user.add_argument('password', type=str, help='password is necesary')

    def post(self):
        data = UserRegister.parser_user.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'msg':'User existed'}, 400

        
        user = UserModel(**data)

        user.save_from_db()

        return {'msg':'User created'}, 201


class User(Resource):
    
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_to_db()
        return {'message': 'User deleted'}, 200