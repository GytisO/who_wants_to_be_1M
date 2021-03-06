import requests
import random
import pyfiglet

name = input('Enter your name to begin the game: ')
msg = pyfiglet.figlet_format("who wants to be a millionaire".capitalize())
right = pyfiglet.figlet_format("correct".capitalize())
wrong = pyfiglet.figlet_format("wrong".capitalize())
won = pyfiglet.figlet_format("congratulations!".capitalize())
lost = pyfiglet.figlet_format("game over!".capitalize())

print(msg)
print('****************************************************\n', name,'get ready for the question.\n****************************************************')

current_level = 0
data = {}


def questions_list(level):
    url = 'https://opentdb.com/api.php';

    response = requests.get(
            url,
            headers={'results': 'application/json'},
            params={'amount': '5', 'type': 'multiple', 'difficulty': level}
    )
    global data
    data = response.json()
    # print('DATA lenght',len(data['results']))
    return data


def question():
    global data
    global current_level
    while current_level < 5:
        if current_level == 0:
            load_questions()
        new_question()

    while 5 <= current_level < 10:
        print(current_level)

        if current_level == 5:
            print("NEXT LEVEL")
            load_questions()

        new_question()

    while current_level >= 10:

        if current_level == 10:
            print("NEXT LEVEL")
            load_questions()
        new_question()


def load_questions():
    if 16 > current_level >= 10:
        questions_list('hard')
        print('Level: Hard')
    elif 10 > current_level >= 5:
        questions_list('medium')
        print('Level: Medium')
    else:
        questions_list('easy')
        print('Level: easy')


def new_question():
    global data
    global current_level

    print('Current question',current_level+1, '\n****************************************************')

    current_question = data['results'][-1]['question'].replace('&quot;', '"')

    for repl in (('&quot;', '"'), ("&#039;", "'")):
        current_question = current_question.replace(*repl)

    print(current_question)

    incorrect = data['results'][-1]['incorrect_answers']
    correct = data['results'][-1]['correct_answer']
    answers = incorrect
    answers.insert(random.randint(0, 3), correct)

    choice = [chr(i) for i in range(ord('a'), ord('d') + 1)]
    showing_choices = dict(zip(choice, answers))

    continue_question(showing_choices)

    guess = input("Guess the answer (a/b/c/d) ")
    if guess == "help":
            helps()
    elif showing_choices[guess] == correct:
        current_level += 1
        if current_level == 15:
            print('****************************************************\n', name,'you won the game!\n', won, '\n****************************************************')
            exit()
        print(right)
        del data['results'][-1]
        print(len(data['results']))

    else:
        print(wrong)
        print('****************************************************\n', name,
              'you lost the game.\n****************************************************')
        exit()


def continue_question(showing_choices):
    print('[a]', showing_choices['a'], '\n[b]', showing_choices['b'], '\n[c]', showing_choices['c'], '\n[d]',
          showing_choices['d'])


def helps():
    global current_level
    global right
    print("Help list: \n[a] - 50/50")
    help_decision = input("Enter help: ")
    if help_decision == "a":
        incorrect = data['results'][-1]['incorrect_answers'][0:1]
        correct = data['results'][-1]['correct_answer']
        answers = incorrect
        answers.insert(random.randint(0, 1), correct)
        choice = [chr(i) for i in range(ord('a'), ord('b') + 1)]
        showing_choices = dict(zip(choice, answers))
        print('[a]', showing_choices['a'], '\n[b]', showing_choices['b'])
        input("Guess the answer (a/b) ")
        del data['results'][-1]
        current_level += 1
        print(right)
        new_question()

question()