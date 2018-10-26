import time
import random
import os
import datetime
import pickle

try_agains = {}
file = open('high_scores', 'rb')
high_scores = pickle.load(file)
file.close()

file = open('question_log', 'rb')
question_log = pickle.load(file)
file.close()

question_list = {}
tough_list = {}

#below is still used for practice mode
def generate_questions(total_questions):
    global question_log
    question_list = {}
    for q in range(1, (total_questions+1)):
        new_q = random.randint(1,len(question_log))
        question_list[new_q] = question_log[new_q]
    return question_list

def print_question_list(ids_guesses):
    global question_log
    for q in ids_guesses:
        print("question", ids_guesses[q][0], " >> ", str(question_log[q][0]) + str(question_log[q][1]), end="")
        print("  <<  ...you answered", ids_guesses[q][-1])

def answer_question(question_id, q):
    global question_log
    question_log[question_id][4] +=1
    print("question", q, "> ", end="")
    answer = input(question_log[question_id][0])
    if answer == "m":
        result = "menu"
        return result
    global try_agains
    try:
        answer = int(answer)
        if answer == 0:
            result = "invalid"
            return result
        elif answer == question_log[question_id][1]:
            result = "correct"
            return result
        else:
            result = "incorrect"
            try_agains[question_id]= [q]
            try_agains[question_id].append(answer)
            return result
    except ValueError:
        result = "invalid"
        return result

def ask_question(qs_to_ask):
    global try_agains
    header()
    print("[m] - Back to the main menu\n")
    print("STARTING THE TIMER...\n")
    start = time.time()
    correct = 0
    incorrect = 0
    try_agains={}
    q = 1
    for n in qs_to_ask:
        result = answer_question(n, q)
        if result == "correct":
            correct +=1
        elif result == "incorrect":
            incorrect +=1
        elif result == "invalid":
            print("you're wasting time - enter a number higher than 0")
            answer_question(n,q)
        else:
            input("hit [ENTER] to go back to the main menu")
            main_menu(try_agains)
        q +=1
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
    global question_log
    quiz_time = 60
    try_agains = {}
    game_time = header()
    player = input("Who's playing? ")
    print("This is it - you get", quiz_time, "seconds...\nSee how many questions you can answer!\n")
    input("Hit [ENTER] to start")
    print("GO!")
    start = time.time()
    q = 1
    total_time = quiz_time-1
    while total_time < quiz_time:
        this_quiz = []
        question_id = random.randint(1, (len(question_log)))
        while question_id in this_quiz:
            question_id = random.randint(1, (len(question_log)))
        this_quiz.append(question_id)
        result = answer_question(question_id, q)
        if result == "correct":
            correct +=1
            question_log[question_id][2] += 1
        elif result == "incorrect":
            incorrect +=1
            question_log[question_id][3] += 1
        elif result == "invalid":
            print("you're wasting time - enter a number higher than 0")
            answer_question(question_id, q)
        else:
            input("hit [ENTER] to go back to the main menu")
            main_menu(try_agains)
        q +=1
        total_time = round((time.time()-start),2)
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

def question_stats():
    header()
    global question_log
    global tough_list
    tough_list = {}
    tricky_ones = {}
    fails = []
    for q in question_log:
        if question_log[q][4] > 0:
            fail_ratio = round(((question_log[q][3])/question_log[q][4])*100)
            if fail_ratio > 19:
                tricky_ones[q] = [fail_ratio, q]
                if fail_ratio not in fails:
                    fails.append(fail_ratio)
    fails = sorted(fails, reverse=True)
    for fail in fails:
        for tricky_q in tricky_ones:
            if tricky_ones[tricky_q][0] == fail:
                tricky_q_id = tricky_ones[tricky_q][1]
                print((100-fail), "% correct answers for:", question_log[tricky_q_id][0], question_log[tricky_q_id][1])
                tough_list[tricky_q_id] = question_log[tricky_q_id]

def main_menu(try_agains = {}):
    file = open('question_log', 'wb')
    pickle.dump(question_log, file)
    file.close()
    global question_list
    global tough_list
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
    if len(tough_list) >0:
        toughlist = True
        print("[5] - ** TRY 10 TRICKY QUESTIONS!!! **")
    print("\n")
    print("----------------")
    print("[9] - high scores")
    print("[stats] - find out the tricky questions")
    print("[q] - quit this game")
    print("\n")
    user_action = input("What do you want to do?")
    if user_action == "2":
        number_of_questions = int(input("how many questions do you want?"))
        question_list = generate_questions(number_of_questions)
        try_agains = ask_question(question_list)
        input("Press [ENTER] to continue...")
        main_menu(try_agains)
    elif user_action == "3" and qlist == True:
        num_list = list(range(len(question_list)))
        old_qs = list(question_list.keys())
        random.shuffle(old_qs)
        new_question_list = {}
        for i in range(len(old_qs)):
            new_question = old_qs[i]
            print(new_question)
            new_question_list[new_question] = question_list[new_question]
        try_agains = ask_question(new_question_list)
        input("Press [ENTER] to continue...")
        main_menu(try_agains)
    elif user_action == "4" and trylist == True:
        try_agains = ask_question(try_agains)
        input("Press [ENTER] to continue...")
        main_menu(try_agains)
    elif user_action == "5" and toughlist == True:
        if len(tough_list) > 10:
            old_qs = list(tough_list.keys())
            random.shuffle(old_qs)
            tough_play_list = {}
            for i in range(10):
                new_question = old_qs[i]
                tough_play_list[new_question] = tough_list[new_question]
            print(len(tough_play_list))
        else:
            tough_play_list = tough_list
        try_agains = ask_question(tough_play_list)
        input("Press [ENTER] to continue...")
        main_menu(try_agains)
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
        main_menu(try_agains)
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
            main_menu(try_agains)
        else:
            input("Press [ENTER] to pretend this never happened...")
            main_menu(try_agains)
    elif user_action == "stats":
        question_stats()
        print("")
        input("Press [ENTER] to go back to the menu...")
        main_menu(try_agains)

    elif user_action == "q":
        print ("...goodbye")
        raise SystemExit
    else:
        main_menu(try_agains)

main_menu()
