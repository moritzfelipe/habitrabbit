from flask import request
from flask_restful import Resource, reqparse
from models.habit import HabitModel
from models.user import UserModel
from datetime import datetime

from content.habit_texts import response_already_created_habit_with_this_name, response_habit_created, response_habit_deleted, response_error

#class for creating habits
class CreateHabit(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('messenger user id',
        type=str,
        required=False,
        location='form',
        help="This field cannot be left blank!"
    )    
    parser.add_argument('habit_name',
        type=str,
        required=False,
        location='form',
        help="Need habit_name"
    )
    #just for testing
    parser.add_argument('habit_points',
        type=int,
        required=False,
        help="This field cannot be left blank!"
    )
    
    def post(self):

        data = CreateHabit.parser.parse_args()
        habit_user_id = UserModel.find_by_msg_id(data['messenger user id'])

        if HabitModel.find_by_name(data['habit_name']):
            old_habit = HabitModel.find_by_name(data['habit_name'])
            if old_habit.user_id == habit_user_id.user_id:
                return response_already_created_habit_with_this_name(data['habit_name'])

        habit = HabitModel(habit_user_id.user_id, data['habit_name'].upper(), 00.00)

        try:
            habit.save_to_db()
        except:
            return response_error(), 500

        return response_habit_created(data['habit_name'])

    #used for testing        
    def put(self):
        data = CreateHabit.parser.parse_args()
        habit_user_id = UserModel.find_by_msg_id(data['messenger user id'])
        habit = HabitModel.find_by_name(data['habit_name'])
        
        date = datetime.utcnow()
        date = date.date()
        date = datetime(2017, 4, 11, 15, 8, 24, 78915)
        
        habit.habit_update_date = date
        habit.habit_points = data['habit_points']
        habit.save_to_db()

        return habit.json()

#class for deleting habits
class DeleteHabit(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('messenger user id',
        type=str,
        required=False,
    )    
    parser.add_argument('habit_name',
        type=str,
        required=False,
        location='form',
    )
    parser.add_argument('Delete_Habit',
        type=str,
        required=False,
        location='form',
    )

    def post(self):
        data = DeleteHabit.parser.parse_args()
        
        habit_user_id = UserModel.find_by_msg_id(data['messenger user id'])
        habit = HabitModel.find_by_name_and_id(data['Delete_Habit'],habit_user_id.user_id)
        
        try:
            habit.delete_from_db()
            return response_habit_deleted(data['Delete_Habit'])
                
        except:
            return response_error(), 500
            

    def get(self):
        msg_id = request.args.get("messenger user id","error")
        habit_user_id = UserModel.find_by_msg_id(msg_id)
        return {'messages': list(map(lambda x: x.json_get_habits_for_delete(), HabitModel.query.filter_by(user_id=habit_user_id.user_id).all()))}


#classs for updating habits
class UpdateHabit(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('messenger user id',
        type=str,
        required=False,
        location='form',        
    )    
    parser.add_argument('Update_Habit',
        type=str,
        required=False,
        location='form',
    )
    parser.add_argument('habits_trained',
        type=str,
        required=False,
        location='form',
    )   


    def post(self):
        data = UpdateHabit.parser.parse_args()
        habit_user_id = UserModel.find_by_msg_id(data['messenger user id'])
        
        #update all habits as trained
        if data['habits_trained']=="all":
            return {'messages': list(map(lambda x: x.update_habits_done(), HabitModel.query.filter_by(user_id=habit_user_id.user_id).all()))}

        #update all habits as not trained
        if data['habits_trained']=="none":
            return {'messages': list(map(lambda x: x.update_habits_not_done(), HabitModel.query.filter_by(user_id=habit_user_id.user_id).all()))}            

        #get habits to update some habits as trained
        if data['habits_trained']=="some":
            return {'messages': list(map(lambda x: x.json_get_habits_for_update(), HabitModel.query.filter_by(user_id=habit_user_id.user_id).all()))}            

        #update habit as trained
        if data['Update_Habit']:
            habit = HabitModel.find_by_name_and_id(data['Update_Habit'],habit_user_id.user_id)
            return {'messages': list(map(lambda x: x.update_habits_done(), HabitModel.query.filter_by(user_id=habit_user_id.user_id,habit_name=habit.habit_name).all()))}            

