import requests
import os
import time
from flask import Flask
from flask_restful import Api
from datetime import datetime, timedelta

from models.user import UserModel
from models.habit import HabitModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    with app.app_context():
        
        if datetime.utcnow().isoweekday() in range(1, 6):
            bot_id = "57da448b9d5d8a3fd79ce9a7"
            chatfuel_token = os.environ['CHATFUEL_TOKEN']
            chatfuel_block_id = "591f07f2e4b0458b5bdafe4e"
            
            #get timezone where it's 22:00
            utc = datetime.utcnow().hour
            utc = 20
            
            if utc < 12:
                timezone_to_message = -2 - utc
            else:
                timezone_to_message = 22 - utc 
                
            #print(timezone_to_message)
            #habit_update_date=>max_update_date
            
            update_time_22h = datetime.utcnow() - timedelta(hours=22)
            update_time_42h = datetime.utcnow() - timedelta(hours=42)
            
            #get users in the timezone where it's 22:00
            for user in UserModel.query.filter_by(fb_timezone=str(timezone_to_message)).all():

                #get habits of this user
                new_user = UserModel.find_by_msg_id(user.msg_id)
                #check if habits have right time
                habits_list = []
                for habits in HabitModel.query.filter_by(user_id=new_user.user_id).filter(HabitModel.habit_update_date>update_time_42h).filter(HabitModel.habit_update_date<update_time_22h).all():
                    habits_list.append(habits.habit_name)
                
                message = None
                
                if len(habits_list) == 1:
                    message = "押忍 {}-san, you not report your habit {} today, you do it?".format(new_user.fb_first_name,habits_list[0])
                
                if len(habits_list) == 2:
                    message = "押忍 {}-san, you not report your habit {} and {} today, did you train?".format(new_user.fb_first_name,habits_list[0],habits_list[1])
    
                if len(habits_list) > 2:
                    message = "押忍 {}-san, you not report your habit {} and {} today, did you train?".format(new_user.fb_first_name,", ".join(habits_list[:-1]), habits_list[-1])
                
                if message:
                    r = requests.post('https://api.chatfuel.com/bots/{}/users/{}/send?chatfuel_token={}&chatfuel_block_id={}&message_content={}'.format(bot_id,user.msg_id,chatfuel_token,chatfuel_block_id,message), data={})
                    time.sleep(1)
                else:
                    print('no message to send for {} {}'.format(user.fb_first_name, user.fb_last_name))
    
        
