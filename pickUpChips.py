

from __future__ import print_function
from random import randint


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if (event['session']['application']['applicationId'] !=
             "amzn1.ask.skill.26e18db1-50b1-46e9-86d1-eb9df427e0bf"):
        raise ValueError("Invalid Application ID")

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


# --------------- Events ------------------


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    card_title = "Pick Up Chips"
    should_end_session = False

    # Dispatch to your skill's intent handlers
    if intent_name == "StartGame":
        return GameSetup(intent, session)
    elif intent_name == "GetNumber":
        if intent["slots"]["Number"]["value"] != "1" and intent["slots"]["Number"]["value"] != "2" and intent["slots"]["Number"]["value"] != "3":
            session_attributes = session["attributes"]
            speech_output = "Sorry, that sounded like an invalid number of chips. You can only take 1, 2, or 3 chips. How many chips do you take?"
            reprompt_text = "Sorry, that sounded like an invalid number of chips. How many chips do you take from the table?"
            return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
        return GameLoop(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },'''
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },'''
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Pick Up Chips. There is a pile of chips on the table. Your objective is to not pick up the last chip. We will pick up 1, 2, or 3 chips in alternating turns. I will go first. What difficulty would you like to play?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please select a difficulty. The options are easy, medium, or hard."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def GameSetup(intent, session):
    """ Sets up the board based on DifficultyValue.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False


    # This should always evaluate to true
    difficulty = intent['slots']['DifficultyValue']['value']
    if difficulty.lower() == "easy" or difficulty.lower() == "medium":
        chipsOnBoard = randint(18, 27)
    elif difficulty.lower() == "hard":
        chipsOnBoard = (4 * randint(5, 7)) + 1 + 2  # Alexa's first move will always be 2
    else:
        speech_output = "Hmm, I don't recognize that difficulty. The options are easy, medium, or hard. What difficulty would you like?"
        reprompt_text = "Hmm, I don't recognize that difficulty. The options are easy, medium, or hard. What difficulty would you like?"
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    speech_output = "Ok, we'll play on " + difficulty + " difficulty. There are " + str(chipsOnBoard) + " chips on the table. I pick up 2 chips. There are now " + str(chipsOnBoard - 2) + " chips on the table. How many chips do you take?"
    chipsOnBoard = int(chipsOnBoard) - 2
    session_attributes = {"chipsOnBoard": str(chipsOnBoard), "difficulty": difficulty}
    reprompt_text = "Sorry, that sounded like an invalid number of chips. How many chips do you take?"
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def GameLoop(intent, session):
    """ The core game loop, keeps going until no more chips left on table. Order of this function: user(input already in intent), then Alexa."""
    # This function should never be entered if chipsOnBoard < 1
    card_title = intent['name']
    should_end_session = False

    chipsOnBoard = session["attributes"]["chipsOnBoard"]
    difficulty = session["attributes"]["difficulty"]

    if int(intent["slots"]["Number"]["value"]) < int(chipsOnBoard):
        chipsOnBoard = int(chipsOnBoard) - int(intent["slots"]["Number"]["value"])  # subtracts the user's selection
    elif int(intent["slots"]["Number"]["value"]) > int(chipsOnBoard):
        speech_output = "You selected more chips than are on the table. There are still " + str(chipsOnBoard) + " chips left on the table. How many do you want to take?"
        reprompt_text = "Sorry, that sounded like an invalid number of chips. There are " + str(chipsOnBoard) + " left on the table. How many do you take?"
        session_attributes = {"chipsOnBoard": str(chipsOnBoard), "difficulty": difficulty}
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
    elif int(intent["slots"]["Number"]["value"]) == int(chipsOnBoard):
        return PlayerLose()

    if difficulty.lower() == "easy" or difficulty.lower() == "medium":
        AlexaSelection = randint(1, 3)
        while AlexaSelection > int(chipsOnBoard):  # Handles the edge cases near the end of the game so chipsOnBoard doesn't go into the negatives.
            AlexaSelection = randint(1,3)
    else:
        AlexaSelection = 4 - int(intent["slots"]["Number"]["value"])

    if AlexaSelection == int(chipsOnBoard):
        return PlayerWin(chipsOnBoard)

    speech_output = "There are now " + str(chipsOnBoard) + " chips on the table. I'll take " + str(AlexaSelection) + " Now there's " + str(chipsOnBoard - AlexaSelection) + " chips left. How many do you want to take away?"
    chipsOnBoard = int(chipsOnBoard) - AlexaSelection
    reprompt_text = "Sorry, that sounded like an invalid number of chips. There are " + str(chipsOnBoard) + " chips left on the table. How many do you take?"
    session_attributes = {"chipsOnBoard": str(chipsOnBoard), "difficulty": difficulty}
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def PlayerLose():
    card_title = "Game Over"
    should_end_session = True
    session_attributes = {}

    speech_output = "You've picked up the last chip on the table. You lose. Better luck next time, thanks for playing!"
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def PlayerWin(chipsOnBoard):
    card_title = "Game Over"
    should_end_session = True
    session_attributes = {}

    speech_output = "There are now " + str(chipsOnBoard) + " chips on the table. I'll take " + str(AlexaSelection) + ". I've taken the last chip, you win! Congratulations, try playing again on a harder difficulty. Thanks for playing."
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



'''
def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        '''

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thanks for playing!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
