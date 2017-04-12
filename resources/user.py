from flask_restful import Resource, reqparse
from models.user import UserModel

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('messenger user id',
        type=str,
        required=True,
        location='form',
        help="Every user needs a messenger user id."
    )
    parser.add_argument('first name',
        type=str,
        required=False,
        location='form',
    )    
    parser.add_argument('last name',
        type=str,
        required=False,
        location='form',
    )     
    parser.add_argument('timezone',
        type=str,
        required=False,
        location='form',
    )    

    def post(self):
        data = User.parser.parse_args()
        user = UserModel(data['messenger user id'], data['first name'], data['last name'], data['timezone'])
        
        if UserModel.find_by_msg_id(data['messenger user id']):
            return {'message': "User already with msg_id: '{}' already exists.".format(data['messenger user id'])}, 400
            
        try:
            user.save_to_db()
        except:
            return {"message": "An error occurred creating the user."}, 500
        
#        user = UserModel(data['fb_last_name'], data['fb_timezone'], data['fb_first_name'])

        return user.json(), 201

    def put(self):
        data = User.parser.parse_args()


    def delete(self):
        data = User.parser.parse_args()
        user = UserModel.find_by_msg_id(data['messenger user id'])
        if user:
            user.delete_from_db()

        return {'message': 'User deleted'}
        
class GetUser(Resource):
    def get(self, msg_id):
        user = UserModel.find_by_msg_id(msg_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404        
        

class UserList(Resource):
    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}