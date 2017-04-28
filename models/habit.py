from db import db
from datetime import datetime
import math
from models.user import UserModel
from content.habit_texts import response_habit_already_reported, response_habit_not_done_at_least_friday, response_habit_not_done_yesterday, response_habit_not_done_today, response_habit_done, response_habit_done_level_up

#database for habits
class HabitModel(db.Model):
    __tablename__ = 'habits'

    habit_id = db.Column(db.Integer, primary_key=True)
    habit_name = db.Column(db.String(80))
    habit_points = db.Column(db.Integer)
    habit_update_date = db.Column(db.DateTime)
    habit_creation_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    #Habit model has now user attribute which matches user model, id
    user = db.relationship('UserModel')

    def __init__(self, user_id, habit_name, habit_points):
        self.user_id = user_id
        self.habit_name = habit_name
        self.habit_points = habit_points
        self.habit_update_date = datetime.utcnow()
        self.habit_creation_date = datetime.utcnow()        


    #just for testing
    def json(self):
        return {'user_id': self.user_id, 'habit_name': self.habit_name, 'habit_points': self.habit_points, 'habit_update_date': str(self.habit_update_date) }
    
    #method for functions reported as done
    def update_habits_done(self):
        #the habit was already repoted this day
        if self.habit_update_date.date() == datetime.today().date():
            #its the first day of training the habit
            if datetime.today().date() == self.habit_creation_date.date() and self.habit_points == 0:
                    self.habit_points = self.habit_points+1
                    self.save_to_db() 
                    habit_user_id = UserModel.find_by_user_id(self.user_id)
                    habit_user_first_name = habit_user_id.fb_first_name
                    return response_habit_done(self,habit_user_first_name)
            else:
                return response_habit_already_reported(self)
            

        #today - date last done habit = days since last done habit
        time_since_update = datetime.today().date()-self.habit_update_date.date()
        time_since_update_days = time_since_update.total_seconds()/86400        

        #if today is sunday or monday and habit was not updated at least on friday, user drops one level
        if (datetime.today().weekday() == 6 and time_since_update_days > 2.0) or (datetime.today().weekday() == 0 and time_since_update_days > 3.0):
            print(time_since_update_days)
            self.calc_habit_not_done()
            return response_habit_not_done_at_least_friday(self)

        #if today is not monday or sunday and habit was done yesterday, user drops one level 
        if datetime.today().weekday() is not 0 and datetime.today().weekday() is not 6 and time_since_update_days > 1.0:
            self.calc_habit_not_done()
            return response_habit_not_done_yesterday(self)

        #habit done calculation 
        level = ""
        self.habit_points = self.habit_points+1
        self.habit_update_date = datetime.utcnow()
        self.save_to_db() 
        habit_user_id = UserModel.find_by_user_id(self.user_id)
        habit_user_first_name = habit_user_id.fb_first_name

        #habit done and level up        
        if self.habit_points % 10 == 0:
            return response_habit_done_level_up(self,habit_user_first_name)

        #habit done response
        return response_habit_done(self,habit_user_first_name)

    #method for updated reported as done
    def update_habits_not_done(self):
        if self.habit_update_date.date() == datetime.today().date():
            return response_habit_already_reported(self)            
        
        self.calc_habit_not_done()
        self.habit_points = self.habit_points-1
        self.save_to_db()
        return response_habit_not_done_today(self)

    #calculation for habits not done
    def calc_habit_not_done(self):
        x = self.habit_points
        x = x/10
        x = math.trunc(x)
        x = x*10
        #habit points get plus a point because when reported it is done one more time should be made nicer in next release
        self.habit_points = x+1
        self.habit_update_date = datetime.utcnow()        
        self.save_to_db()
        return
    
    #calculation of obi level, needs to be replaced as dictionary
    def obi_level(self):
        if self.habit_points >= 0:
            level = "white"
        
        if self.habit_points > 10:
            level = "yellow"

        if self.habit_points > 20:
            level = "orange"

        if self.habit_points > 30:
            level = "green"

        if self.habit_points > 40:
            level = "violett"

        if self.habit_points > 50:
            level = "blue"
            
        if self.habit_points > 60:
            level = "brown"
            
        if self.habit_points > 70:
            level = "brown"

        if self.habit_points > 80:
            level = "brown"
 
        if self.habit_points > 90:
            level = "black"      
            
        if self.habit_points > 100:
            level = "red-white"   

        if self.habit_points > 110:
            level = "red"   
        
        return level
    
    
    #Selection of habits
    
    #Selection of habits to delete
    def json_get_habits_for_delete(self):
        return {
            "attachment": {
                "payload":{
                  "template_type": "button",
                  "text": "Stop training for '{}'?".format(self.habit_name),
                  "buttons": [
                    {
                        "set_attributes": 
                            {
                              "Delete_Habit": "{}".format(self.habit_name),
                            },
                          "block_names": ["delete habit 2"],
                          "type": "show_block",
                          "title": "delete"
                    }
                  ]
                },
                "type": "template"
            }
        }

    #Selection of habits to update
    def json_get_habits_for_update(self):
        return {
            "attachment": {
                "payload":{
                  "template_type": "button",
                  "text": "Habit: '{}' train today?".format(self.habit_name),
                  "buttons": [
                    {
                        "set_attributes": 
                            {
                              "Update_Habit": "{}".format(self.habit_name),
                            },
                          "block_names": ["Habit done"],
                          "type": "show_block",
                          "title": "yes",
                    }
                  ]
                },
                "type": "template"
            }
        }


    @classmethod
    def find_by_name(cls, habit_name):
        return cls.query.filter_by(habit_name=habit_name).first()
        
    @classmethod
    def find_by_name_and_id(cls, habit_name, user_id):
        return cls.query.filter_by(habit_name=habit_name, user_id=user_id).first()        

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    