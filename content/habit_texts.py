#responses from the rabit

#update habit
def response_habit_already_reported(habit):
    return { "text": "No no, training for '{}' already reported today.".format(habit.habit_name)}
    
def response_habit_not_done_at_least_friday(habit):
    return {
              "messages": 
                [   
                    {
                      "attachment": {
                        "type": "image",
                        "payload": {
                          "url": "https://media.giphy.com/media/3ohzdDT6bBBnQyeEwM/giphy.gif"
                        }
                      }
                    },
                    {"text": "You not do training on friday. Will have to start training for '{}' with last obi from beginning with {} point.".format(habit.habit_name,habit.habit_points)}
                ]
            }

def response_habit_not_done_yesterday(habit):
    return {
              "messages": 
                [   
                    {
                      "attachment": {
                        "type": "image",
                        "payload": {
                          "url": "https://media.giphy.com/media/3ohzdDT6bBBnQyeEwM/giphy.gif"
                        }
                      }
                    },
                    {"text": "You not do training on yesterday. Will have to start training for '{}' with last obi from beginning with {} point.".format(habit.habit_name,habit.habit_points)}
                ]
            }


def response_habit_not_done_today(habit):
    return { "text": "You not do training today. Will have to start training for '{}' with ".format(habit.habit_name)+"{}".format(habit.obi_level())+" obi from beginning with {} point.".format(habit.habit_points)}

def response_habit_done(habit, habit_user_first_name):
    return { "text": "Good work {}-san".format(habit_user_first_name)+"! You improved with training for '{}'. ".format(habit.habit_name)+"You got {} point and ".format(habit.habit_points)+"{} obi.".format(habit.obi_level())}

def response_habit_done_level_up(habit, habit_user_first_name):
        obi = ""
        url = ""
        if habit.habit_points == 10:
            obi = "yellow"
            url = "https://media.giphy.com/media/3o7budjTkaG1PfnXFe/giphy.gif"

        if habit.habit_points == 20:
            obi = "orange"
            url = "https://media.giphy.com/media/3ohzdFYlkD7XrxhCoM/giphy.gif"

        if habit.habit_points == 30:
            obi = "green"
            url = "https://media.giphy.com/media/xUPGcxVmfNXUf6esgw/giphy.gif"

        if habit.habit_points == 40:
            obi = "violette"
            url = "https://media.giphy.com/media/3ohze4j13u4DFfEOZy/giphy.gif"

        if habit.habit_points == 50:
            obi = "blue"
            url = "https://media.giphy.com/media/3ohzdZFcb9eb0C9GTK/giphy.gif"

        if habit.habit_points == 60:
            obi = "brown"
            url = "https://media.giphy.com/media/3oKIPb2gELZkfugrDy/giphy.gif"

        if habit.habit_points == 70:
            obi = "brown 2"
            url = "https://media.giphy.com/media/3oKIPb2gELZkfugrDy/giphy.gif"

        if habit.habit_points == 80:
            obi = "brown 3"
            url = "https://media.giphy.com/media/3oKIPb2gELZkfugrDy/giphy.gif"

        if habit.habit_points == 90:
            obi = "black"
            url = "https://media.giphy.com/media/l4FGxGJZg9UiCzoxq/giphy.gif"

        if habit.habit_points == 100:
            obi = "red-white"
            url = "XXX"


        return {
                    "messages": 
                        [   
                            {"text": "Im proud of you {}-san".format(habit_user_first_name)+"! You reach next skill level for training '{}'. You earn {} obi with {} points".format(habit.habit_name,obi,habit.habit_points)},
                            {
                              "attachment": {
                                "type": "image",
                                "payload": {
                                  "url": url
                                }
                              }
                            }
                        ]
                }   
    

def response_habit_done_first_point(habit, habit_user_first_name):
    return {
              "messages": 
                [   
                    {"text": "Good work {}-san! You earned first point for training '{}'.".format(habit_user_first_name,habit.habit_name)},
                    {
                      "attachment": {
                        "type": "image",
                        "payload": {
                          "url": "https://media.giphy.com/media/xUA7bhadLgD4BBrcac/giphy.gif"
                        }
                      }
                    }
                ]
            }

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