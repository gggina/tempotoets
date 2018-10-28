import time
import random
import os
import datetime
import pickle

try_agains = {}

# high_scores = {total_correct: [{success_percentage_1: [player_1, player_2...]}, {success_percentage_2: [player_3, player_4...]}]}
file = open('high_scores', 'rb')
high_scores = pickle.load(file)
file.close()

#question log =  {questionid: [question, answer, correct#, incorrect#, total_asks]
file = open('question_log', 'rb')
question_log = pickle.load(file)
file.close()

question_list = {}
tough_list = {}

def generate_questions(total_questions):
    """
    used in practice mode only. generates a random number (question_id) and uses this to compile a question_list form the question_log.
    """
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
    """
    asks the question_id from the question_log (question number q in the current quiz)
    used by all quiz options
    """
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
    """
    practice mode asks the qs_to_ask
    """
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
        while result == "invalid":
            print("you're wasting time - enter a number higher than 0")
            result = answer_question(n,q)
        if result == "correct":
            correct +=1
        elif result == "incorrect":
            incorrect +=1
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
    """
    The big toets.
    change the quiz_time to make toets longer or shorter
    """
    global try_agains
    global question_log
    correct = 0
    incorrect = 0
    quiz_time =5
    try_agains = {}
    header()
    player = input("Who's playing? ")
    while len(player)<1:
        player = input("you need to enter a name so i can save your score...\n")
    while len(player)>10:
        player = input("try again - this time, keep it a bit shorter (max 10 chars)...\n")
    print("Good to see you", player, "- you get", quiz_time, "seconds...\nSee how many questions you can answer!\n")
    input("Hit [ENTER] to start")
    print("GO!")
    start = time.time()
    q = 1
    total_time = quiz_time-1
    this_quiz = []
    invalid_answers = 0
    while total_time < quiz_time:
        question_id = random.randint(1, (len(question_log)))
        while question_id in this_quiz:
            question_id = random.randint(1, (len(question_log)))
        this_quiz.append(question_id)
        result = answer_question(question_id, q)
        while result == "invalid":
            if invalid_answers <3:
                print("you're wasting time - enter a number higher than 0")
                invalid_answers +=1
                result = answer_question(question_id, q)
            else:
                print("too much time wasting! Goodbye")
                result = "forced exit"
        if result == "correct":
            correct +=1
            question_log[question_id][2] += 1
        elif result == "incorrect":
            incorrect +=1
            question_log[question_id][3] += 1
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
        high_score_check(correct, incorrect, player)
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

def high_score_check(total_correct, total_incorrect, player):
    """
    Checks if the results of a tempo toets warrant adding to the high_scores list
    Persists an updated high_scores list to the high_scores file using pickle
    """
    global high_scores
    success_perecentage = round((total_correct /(total_correct + total_incorrect))*100)
    if total_correct in high_scores:
        if success_perecentage in high_scores[total_correct]:
            high_scores[total_correct][success_perecentage].append(player)
        else:
            high_scores[total_correct][success_perecentage]=[player]
    else:
        high_scores[total_correct] = {success_perecentage: [player]}
    file = open('high_scores', 'wb')
    pickle.dump(high_scores, file)
    file.close()

def read_high_score():
    """
    Prints the top 10 high scores from the high_scores list
    All tempotoets scores/names are stored if there were more correct answers than wrong answers
    high scores are calculated by total correct answers and then success_ratio
    """
    global high_scores
    high_score_keys = list(high_scores.keys())
    top_scores = sorted(high_score_keys, reverse = True)
    rank = 1
    if len(high_scores) > 0:
        for top_score in range(10):
            try:
                answered_correctly = top_scores[top_score]
                success_ratio_keys = sorted(list(high_scores[answered_correctly].keys()), reverse =True)
                for s_r in success_ratio_keys:
                    top_scoring_names = []
                    print(rank, "> ", end="")
                    print(str(answered_correctly), "correct ("+ str(s_r) + "%) -", end = "")
                    for name in high_scores[answered_correctly][s_r]:
                        top_scoring_names.append(name)
                    top_scoring_names = top_scoring_names[::-1]
                    name_num=1
                    for tsn in top_scoring_names:
                        if name_num <= 4:
                            print(" ["+  tsn + "]", end = "")
                            name_num +=1
                    print("")
                    rank +=1
            except IndexError:
                print((top_score+1), "> ...")
    else:
        print("No high scores yet!\n")

def header():
    """
    Printed at the top of every screen
    returns a nicely formatted datetime that could be used for storing data
    """
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
    """
    Checks the question log for questions that have been asked with a fail ratio (incorrect answer/total asks) of 20%
    Prints all matching question/answers with associated stats
    Generates the 'tough_list' which is used to practice with tricky questions
    !! Without running stats there is no tough_list, so the practice with tricky questions option will not be available !!
    """
    header()
    global question_log
    global tough_list
    tough_list = {}
    tricky_ones = {}
    fails = []
    for q_id in question_log:
        if question_log[q_id][4] > 0:
            fail_ratio = round(((question_log[q_id][3])/question_log[q_id][4])*100)
            if fail_ratio > 19:
                tricky_ones[q_id] = [fail_ratio, q_id]
                if fail_ratio not in fails:
                    fails.append(fail_ratio)
    fails = sorted(fails, reverse=True)
    if len(fails) > 0:
        print("Questions with fail rate of 20% or more:\n")
        tricky_rank = 1
        for fail_perc in fails:
            for tricky_q in tricky_ones:
                if tricky_ones[tricky_q][0] == fail_perc:
                    tricky_q_id = tricky_ones[tricky_q][1]
                    print(tricky_rank, ">", question_log[tricky_q_id][0] + str(question_log[tricky_q_id][1]), " -", (100-fail_perc), "% correct", end ="")
                    print(" (" + str(question_log[tricky_q_id][4]) + " attempts)")
                    tough_list[tricky_q_id] = question_log[tricky_q_id]
                    tricky_rank +=1
    else:
        print("All questions are successfully answered at least 80% of the time.\n")


def the_unaskeds():
    header()
    global question_log
    unaskeds = []
    for q_id in question_log:
        if question_log[q_id][4] == 0:
            unaskeds.append(q_id)
    if len(unaskeds) > 0:
        print("Questions with 0 asks:\n")
        for q_id in unaskeds:
            print(">", question_log[q_id][0] + str(question_log[q_id][1]))
    else:
        print("All questions have been asked at least once.")

def main_menu(try_agains = {}):
    """
    the main menu. hidden option is "clear high scores"
    """
    file = open('question_log', 'wb')
    pickle.dump(question_log, file)
    file.close()
    global question_list
    global tough_list
    qlist = False
    trylist = False
    toughlist = False
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
        print("[5] - ** TRY SOME TRICKY QUESTIONS!!! **")
    print("\n")
    print("----------------")
    print("[9] - TEMPO TOETS high scores")
    print("[stats] - find out the tricky questions")
    print("[q] - quit this game")
    print("\n")
    user_action = input("What do you want to do?")
    if user_action == "2":
        number_of_questions = input("how many questions do you want?")
        try:
            number_of_questions = int(number_of_questions)
        except ValueError:
            number_of_questions = 10
            print("Not a valid input - will generate a list with 10 questions.")
            input("Press [ENTER] to continue...")
        question_list = generate_questions(number_of_questions)
        try_agains = ask_question(question_list)
        input("Press [ENTER] to continue...")
        main_menu(try_agains)
    elif user_action == "3" and qlist == True:
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
        input("Press [ENTER] to list questions that have not yet been asked...")
        the_unaskeds()
        print("")
        input("Press [ENTER] to go back to the menu...")
        main_menu(try_agains)

    elif user_action == "q":
        print ("...goodbye")
        raise SystemExit
    else:
        main_menu(try_agains)

main_menu()
