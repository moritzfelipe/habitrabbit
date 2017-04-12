from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    msg_id = db.Column(db.String(80))
    fb_first_name = db.Column(db.String(80))
    fb_last_name = db.Column(db.String(80))
    fb_timezone = db.Column(db.String(80))
    

    #UserModel has relationship with HabitModel 
    habits = db.relationship('HabitModel', lazy='dynamic')

    def __init__(self, msg_id, fb_first_name, fb_last_name, fb_timezone):
        self.msg_id = msg_id
        self.fb_first_name = fb_first_name
        self.fb_last_name = fb_last_name
        self.fb_timezone = fb_timezone
        

    def json(self):
        return {'msg_id': self.msg_id, 'fb_first_name': self.fb_first_name, 'fb_last_name': self.fb_last_name, 'fb_timezone': self.fb_timezone,
        'habits': [habit.json() for habit in self.habits.all()]}

    @classmethod
    def find_by_msg_id(cls, msg_id):
        return cls.query.filter_by(msg_id=msg_id).first()
    
    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()