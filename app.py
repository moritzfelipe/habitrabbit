import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.habit import CreateHabit, DeleteHabit, UpdateHabit
from resources.user import User, UserList, GetUser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ['HRABBIT_SECRET']
api = Api(app)

api.add_resource(User, '/user/')
api.add_resource(GetUser, '/getuser/<string:msg_id>')
api.add_resource(UserList, '/users/')
api.add_resource(CreateHabit, '/createhabit/')
api.add_resource(UpdateHabit, '/updatehabit/')
api.add_resource(DeleteHabit, '/deletehabit/')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)
