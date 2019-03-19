import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session, request

from pprint import pprint

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def new_game():

    welcome_msg = "Welcome to memory game. I'm going to say three numbers for you to repeat backwards. Ready?"

    return question(welcome_msg)


@ask.intent("YesIntent")

def next_round():

    numbers = [randint(0, 9) for _ in range(3)]

    round_msg = "Can you repeat the numbers " + ", ".join([str(x) for x in numbers]) + " backwards?" #render_template('round', numbers=numbers)

    session.attributes['numbers'] = numbers[::-1]  # reverse

    return question(round_msg) #question keeps session open


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})

def answer(first, second, third):
    # pprint(session)
    
    # pprint(request)

    winning_numbers = session.attributes['numbers']

    if [first, second, third] == winning_numbers:

        msg = "Good job!"#render_template('win')

    else:

        msg = "Sorry, that's the wrong answer." #render_template('lose')

    return statement(msg) #statement closes session


if __name__ == '__main__':

    app.run(debug=True)
                             