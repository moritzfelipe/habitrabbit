#responses from the rabit

#update habit
def response_habit_already_reported(habit):
    return {"text": "No no, training for '{}' already reported today.".format(habit.habit_name)}
    
def response_habit_not_done_at_least_friday(habit):
    return { "text": "You not do training on friday. Will have to start training for '{}' with ".format(habit.habit_name)+"{}".format(habit.obi_level())+" obi from beginning with {} point.".format(habit.habit_points)}

def response_habit_not_done_yesterday(habit):
    return { "text": "You not do training yesterday. Will have to start training for '{}' with ".format(habit.habit_name)+"{}".format(habit.obi_level())+" obi from beginning with {} point.".format(habit.habit_points)}

def response_habit_not_done_today(habit):
    return { "text": "You not do training today. Will have to start training for '{}' with ".format(habit.habit_name)+"{}".format(habit.obi_level())+" obi from beginning with {} point.".format(habit.habit_points)}

def response_habit_done(habit, habit_user_first_name):
    return { "text": "Good work {}-san".format(habit_user_first_name)+"! You improved with training for '{}'. ".format(habit.habit_name)+"You got {} point and ".format(habit.habit_points)+"{} obi.".format(habit.obi_level())}

def response_habit_done_level_up(habit, habit_user_first_name):
    return { "text": "Im proud of you {}-san".format(habit_user_first_name)+"! You reach next skill level for training '{}'. ".format(habit.habit_name)+"You earned your {} obi with ".format(habit.obi_level())+"{} point.".format(habit.habit_points)}

def response_habit_done_first_point(habit, habit_user_first_name):
    #return { "messages": [ {"text": "Good work {}-san! You earned first point for training '{}'.".format(habit_user_first_name,habit.habit_name)}], "redirect_to_blocks": ["first_point"]}
    return { "messages": [ {"text": "Good work Moritz-san! You earned first point for training"}]}
   
#create habit
def response_already_created_habit_with_this_name(habit_name):
    return { "messages": [ {"text": "You already created training for habit named '{}'.".format(habit_name)}]}

def response_habit_created(habit_name):
    return { "messages": [ {"text": "New training for habit '{}' created".format(habit_name.upper())}]}

#delete habit
def response_habit_deleted(habit_name):
    return { "messages": [ {"text": "Training for habit '{}' deleted".format(habit_name)}]}

#global messages
def response_error():
    return { "messages": [ {"text": "An error has occurred please try again or leave feedback."}]}