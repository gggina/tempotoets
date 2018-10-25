import time
import random
import os
import datetime
import pickle

try_agains = {}
file = open('high_scores', 'rb')
high_scores = pickle.load(file)
file.close()

def generate_questions(total_questions, up_to_table):
    question_list = {}
    for q in range(0, total_questions):
        a = random.randint(2, (up_to_table))
        b = random.randint(2, 12)
        c = a*b
        multi_or_divi = random.randint(1,6)
        if multi_or_divi ==2:
            question_list[q] = [(str(b) + "x" + str(a) + "= "), c]
        elif multi_or_divi == 2 or multi_or_divi == 3:
            question_list[q] = [(str(c) + ":" + str(a) + "= "), b]
        else:
            question_list[q] = [(str(a) + "x" + str(b) + "= "), c]
    return question_list

def print_question_list(question_list):
    for q in question_list:
        print("question", q+1, " >> ", str(question_list[q][0]) + str(question_list[q][1]), end="")
        if len(question_list[q]) >= 2:
            print("  <<  ...you answered", question_list[q][-1])

def answer_question(question_list, q):
    print("question", q+1, "> ", end="")
    answer = input(question_list[q][0])
    if answer == "m":
        result = "menu"
        return result
    global try_agains
    try:
        answer = int(answer)
        if answer == 0:
            result = "invalid"
            return result
        elif answer == question_list[q][1]:
            result = "correct"
            return result
        else:
            result = "incorrect"
            this_error = len(try_agains)
            try_agains[this_error]= question_list[q]
            try_agains[this_error].append(answer)
            return result
    except ValueError:
        result = "invalid"
        return result

def ask_question(question_list):
    global try_agains
    header()
    print("[m] - Back to the main menu\n")
    print("STARTING THE TIMER...\n")
    start = time.time()
    correct = 0
    incorrect = 0
    try_agains={}
    for q in question_list:
        result = answer_question(question_list, q)
        if result == "correct":
            correct +=1
        elif result == "incorrect":
            incorrect +=1
        elif result == "invalid":
            print("you're wasting time - enter a number higher than 0")
            answer_question(question_list,q)
        else:
            input("hit [ENTER] to go back to the main menu")
            main_menu(try_agains, question_list)
    print("\nSTOPPING THE TIMER...")
    end = time.time()
    total_time = round((end-start),2)
    print("Total time spent:", total_time, "seconds")
    print("\n")
    input("Hit [ENTER] to see your results")
    if incorrect == 0:
        print("\n-- -- -- -- -- --")
        print("ALL CORRECT!!!")
        print("-- -- -- -- -- --\n")
    elif correct == 0:
        print("\n-- -- -- -- -- --")
        print("0 correct answers...\n")
        print_question_list(try_agains)
        print("-- -- -- -- -- --\n")
    else:
        print("\n-- -- -- -- -- --")
        print_question_list(try_agains)
        print("-- -- -- -- -- --\n")
    return try_agains

def do_the_tempo_toets():
    correct = 0
    incorrect = 0
    global try_agains
    quiz_time = 60
    try_agains = {}
    question_list = generate_questions(1000,10)
    game_time = header()
    player = input("Who's playing? ")
    print("This is it - you get", quiz_time, "seconds...\nSee how many questions you can answer!\n")
    input("Hit [ENTER] to start")
    print("GO!")
    start = time.time()
    for q in question_list:
        result = answer_question(question_list, q)
        if result == "correct":
            correct +=1
        elif result == "incorrect":
            incorrect +=1
        elif result == "invalid":
            print("you're wasting time - enter a number higher than 0")
            answer_question(question_list,q)
        else:
            input("hit [ENTER] to go back to the main menu")
            main_menu(try_agains, question_list)
        total_time = round((time.time()-start),2)
        if total_time > quiz_time:
            break
    print("STOP!!")
    print("time's up.")
    print("...............")
    print("You answered >>", (correct + incorrect), "<< questions in", total_time, "seconds")
    print("\n\n")
    if correct > incorrect:
        high_score_check(correct, incorrect, game_time, player)
    input("hit [ENTER] to see your results")
    print("\nCORRECT answers:", correct)
    print("INCORRECT answers: ", incorrect)
    if incorrect > 0:
        print("-- -- -- -- -- --")
        print_question_list(try_agains)
        print("-- -- -- -- -- --")
        return try_agains
    else:
        print("\n-- -- -- -- -- --")
        print("ALL CORRECT!!!")
        print("-- -- -- -- -- --\n")

def high_score_check(total_correct, total_incorrect, game_time, player):
    global high_scores
    success_perecentage = round((total_correct /(total_correct + total_incorrect))*100)
    if total_correct in high_scores:
        print("tied with", high_scores[total_correct][0])
    else:
        high_scores[total_correct]=[player,success_perecentage, game_time]
    file = open('high_scores', 'wb')
    pickle.dump(high_scores, file)
    file.close()

def read_high_score():
    global high_scores
    top_scores = list(high_scores.keys())
    top_scores = sorted(top_scores, reverse = True)
    if len(high_scores) > 0:
        for s in range(0,10):
            try:
                score = top_scores[s]
                print((s+1), ">", high_scores[score][0], "-", score, "correct ("+str(high_scores[score][1])+"%)-", high_scores[score][2])
            except IndexError:
                print((s+1), "> ...")
    else:
        header()
        print("\nNo High scores saved yet...")
        print("Play the TEMPO TOETS to set a high score")

def header():
    os.system('cls||clear')
    right_now = datetime.datetime.today()
    pretty_datetime = right_now.ctime()
    print("> ---------------------------- <")
    print(">         TEMPO TOETS          <")
    print(">                              <")
    print(">  ", pretty_datetime, "  <")
    print("> ---------------------------- <")
    print("\n")
    return pretty_datetime

def main_menu(try_agains = {}, question_list = {}):
    qlist = False
    trylist = False
    header()
    print("TOETS MODE...")
    print("[1] - Do the TEMPO TOETS!!!")
    print("\n\n")
    print("PRACTICE MODE...")
    print("[2] - New question list")
    if len(question_list) > 0:
        qlist = True
        print("[3] - Same questions again (random order)")
    if len(try_agains) >0:
        trylist = True
        print("[4] - Just the questions you got wrong last time")
    print("\n")
    print("----------------")
    print("[9] - high scores")
    print("[q] - quit this game")
    print("\n")
    user_action = input("What do you want to do?")
    if user_action == "2":
        top_table = int(input("What's the top table you want to practice?"))
        number_of_questions = int(input("how many questions do you want?"))
        question_list = generate_questions(number_of_questions,top_table)
        try_agains = ask_question(question_list)
        input("Press [ENTER] to continue...")
        main_menu(try_agains, question_list)
    elif user_action == "3" and qlist == True:
        num_list = list(range(len(question_list)))
        random.shuffle(num_list)
        new_question_list = {}
        for i in range(len(num_list)):
            new_question = num_list[i]
            new_question_list[i] = question_list[new_question]
        try_agains = ask_question(new_question_list)
        input("Press [ENTER] to continue...")
        main_menu(try_agains, question_list)
    elif user_action == "4" and trylist == True:
        try_agains = ask_question(try_agains)
        input("Press [ENTER] to continue...")
        print(len(try_agains))
        if try_agains and len(try_agains) > 0:
            main_menu(try_agains)
        else:
            main_menu()
    elif user_action == "1":
        try_agains = do_the_tempo_toets()
        input("Press [ENTER] to continue...")
        if try_agains and len(try_agains) > 0:
            main_menu(try_agains)
        else:
            main_menu()
    elif user_action == "9":
        header()
        read_high_score()
        print("")
        input("Press [ENTER] to go back to the menu...")
        main_menu(try_agains, question_list)
    elif user_action == "clear high scores":
        action = input("Clear high scores? (y/n)")
        if action == "y":
            global high_scores
            high_scores = {}
            file = open('high_scores', 'wb')
            pickle.dump(high_scores, file)
            file.close()
            print("High scores cleared - no going back.")
            input("Press [ENTER] to go back to the menu and start again...")
            main_menu(try_agains, question_list)
        else:
            input("Press [ENTER] to pretend this never happened...")
            main_menu(try_agains, question_list)
    elif user_action == "q":
        print ("...goodbye")
        raise SystemExit
    else:
        main_menu(try_agains, question_list)


main_menu()