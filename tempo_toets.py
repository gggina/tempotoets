from functools import wraps
import time
import random
import os

try_agains = {}
current_top_time = 0
total_lists_this_session = 0
lists_this_session = {}


def generate_questions(total_questions, up_to_table):
    question_list = {}
    global lists_this_session
    global total_lists_this_session
    for q in range(0, total_questions):
        a = random.randint(2, (up_to_table))
        b = random.randint(2, (up_to_table))
        c = a*b
        multi_or_divi = random.randint(1,5)
        if multi_or_divi ==2:
            question_list[q] = [(str(c) + ":" + str(b) + "="), a]
        elif multi_or_divi == 3:
            question_list[q] = [(str(c) + ":" + str(a) + "="), b]
        else:
            question_list[q] = [(str(a) + "x" + str(b) + "="), c]
    total_lists_this_session +=1
    lists_this_session[total_lists_this_session]= question_list
    return question_list

def print_question_list(question_list):
    for q in question_list:
        print("question", q+1, " >> ", question_list[q][0], question_list[q][1], end="")
        if len(question_list[q]) >= 2:
            print("  <<  ...you answered", question_list[q][-1])

def answer_question(question_list, q):
    global try_agains
    print("question", q+1, "> ", end="")
    answer = input(question_list[q][0])
    try:
        answer = int(answer)
        if answer == 0:
            print("you're wasting time - enter a number higher than 0")
            answer_question(question_list,q)
        elif answer == question_list[q][1]:
            result = "correct"
            return result
        else:
#            print("not quite...")
            result = "incorrect"
            try_agains[q]= question_list[q]
            try_agains[q].append(answer)
            return result
    except ValueError:
        print("you're wasting time - enter a number higher than 0")
        answer_question(question_list,q)

def ask_question(question_list):
    os.system('cls||clear')
    global lists_this_session
    print("<><><><><><><><><><><><><><>")
    print("<>      TEMPO TOETS       <>")
    print("<><><><><><><><><><><><><><>\n")
    print("STARTING THE TIMER...\n")
    start = time.time()
    correct = 0
    incorrect = 0
    global try_agains
    try_agains={}
#    print(question_list)
    for q in range(len(question_list)):
        result = answer_question(question_list, q)
#        print(try_agains)
        if result == "correct":
            correct +=1
        elif result == "incorrect":
            incorrect +=1
    print("\nSTOPPING THE TIMER...")
    end = time.time()
    total_time = round((end-start),2)
    print("Total time spent:", total_time, "seconds")
    print("incorrect total:", incorrect)
    if incorrect == 0:
        print("-- -- -- -- -- --")
        print("ALL CORRECT!!!")
        print("-- -- -- -- -- --")
    elif correct == 0:
        print("-- -- -- -- -- --")
        print("you got every single answer wrong...")
        print_question_list(try_agains)
        print("-- -- -- -- -- --")
    else:
        print("-- -- -- -- -- --")
        print("you got ", incorrect, " answer(s) wrong:")
        print_question_list(try_agains)
        print("-- -- -- -- -- --")
    return try_agains

def do_the_tempo_toets():
    os.system('cls||clear')
    correct = 0
    incorrect = 0
    global try_agains
    question_list = generate_questions(1000,10)
    print("<><><><><><><><><><><><><><>")
    print("<>      TEMPO TOETS       <>")
    print("<><><><><><><><><><><><><><>")
    print("\n\n")
    print("This is it - you get 1 minute...\nSee how many questions you can answer!")
    print("\n\n")
    input("hit [ENTER] to start")
    print("GO!")
    start = time.time()
#    print(question_list)
    for q in question_list:
        result = answer_question(question_list, q)
        if result == "correct":
            correct +=1
        elif result == "incorrect":
            incorrect +=1
        total_time = time.time()-start
        if total_time > 60:
            break
    print("STOP!!")
    print("time's up.")
    print("...............")
    print("You answered >>", (correct + incorrect), "<< questions in", round(total_time,2), "seconds")
    print("\n\n")
    input("hit [ENTER] to see your results")
    print("GOOD ANSWERS:", correct)
    print("INCORRECT answers: ", incorrect)
    if incorrect > 0:
        print("-- -- -- -- -- --")
        print_question_list(try_agains)
        print("-- -- -- -- -- --")
        print(type(try_agains))
        print(try_agains)
        return try_agains



def main_menu(try_agains = {}, **kwargs):
    print(len(kwargs))
    if 'question_list' in kwargs:
        question_list=kwargs['question_list']
    if 'try_agains' in kwargs:
        try_agains = kwargs['try_agains']
    os.system('cls||clear')
    print("<><><><><><><><><><><><><><>")
    print("<>      TEMPO TOETS       <>")
    print("<><><><><><><><><><><><><><>")
    print("\n\n")
    print("1 - Practice with a new question list")
    print("\n\n")
    if "question_list" in kwargs:
        print("2 - Practice again with same question list")
        print("\n\n")
    print("3 - DO THE TEMPO TOETS!!!")
    if len(try_agains) >0:
            print("4 - Practice the questions you got wrong last time")
    print("\n\n")
    print("9 - view high scores")
    print("\n\n")
    print("q - quit this game")
    print("\n\n")
    user_action = input("What do you want to do?")
    if user_action == "1":
        top_table = int(input("What's the top table you want to practice?"))
        number_of_questions = int(input("how many questions do you want?"))
        question_list = generate_questions(number_of_questions,top_table)
        try_agains = ask_question(question_list)
        input("Press [ENTER] to continue...")
        if try_agains:
            main_menu(question_list=question_list, try_agains=try_agains)
        else:
            main_menu(question_list=question_list)
    elif user_action == "2":
        num_list = list(range(len(kwargs['question_list'])))
        random.shuffle(num_list)
        new_question_list = {}
        for i in range(len(num_list)):
            new_question = num_list[i]
            new_question_list[i] = question_list[new_question]
        try_agains = ask_question(new_question_list)
        input("Press [ENTER] to continue...")
        main_menu(question_list=question_list, try_agains=try_agains)
    elif user_action == "3":
        try_agains = do_the_tempo_toets()
        input("Press [ENTER] to continue...")
        if try_agains and len(try_agains) > 0:
            main_menu(try_agains = try_agains)
        else:
            main_menu()
    elif user_action == "4":
        try_agains = ask_question(kwargs['try_agains'])
        input("Press [ENTER] to continue...")
        print(len(try_agains))
        if try_agains and len(try_agains) > 0:
            main_menu(try_agains = try_agains)
        else:
            main_menu()
    elif user_action == "9":
        print("can't do that just yet")
    elif user_action == "q":
        print ("...goodbye")
        raise SystemExit


main_menu()
