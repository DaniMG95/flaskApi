import sqlite3
from werkzeug.security import safe_str_cmp
from flask_restful import Resource,reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token,get_jwt_identity, jwt_required, get_jwt
from blacklist import BLACKLIST


_parser_user = reqparse.RequestParser()
_parser_user.add_argument('username', type=str, help='username is necesary')
_parser_user.add_argument('password', type=str, help='password is necesary')

class UserRegister(Resource):

    def post(self):
        data = _parser_user.parse_args()

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



class UserLogin(Resource):


    def post(self):
        data = _parser_user.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message', 'Invalid credentials'}, 401


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        print(BLACKLIST)
        return {'message': 'Successfully logged out'}, 200