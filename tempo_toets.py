import time
import random
import os
import datetime
import pickle
import sys

quiz_time = 60
if len(sys.argv) > 1:
    try:
        quiz_time = int(sys.argv[1])
    except:
        pass

try_agains = {}
question_list = {}
tough_list = {}
question_log = {}
high_scores= {}

# high_scores = {total_correct: [{success_percentage_1: [player_1, player_2...]}, {success_percentage_2: [player_3, player_4...]}]}

def set_highscore_questionlog ():
    global high_scores
    global question_log
    try:
        file = open('high_scores', 'rb')
        high_scores = pickle.load(file)
        file.close()
    except FileNotFoundError:
        high_scores = {}

    #question log =  {questionid: [question, answer, correct#, incorrect#, total_asks]
    try:
        file = open('question_log', 'rb')
        question_log = pickle.load(file)
        file.close()
    except FileNotFoundError:
        generate_question_log()

def generate_question_log():
    global question_log
    print("generating new question log")

    all_tables = 12
    top_table = 12
    counter = 1

    for x in range(2, (top_table+1)):
        for y in range (2, (all_tables+1)):
            multi_sum = str(x) + "x" + str(y)+ "= "
            multi_ans = x*y
            question_log[counter] = [multi_sum, multi_ans, 0, 0, 0]
            counter +=1
        for z in range (2, (all_tables+1)):
            div_sum =  str(x*z) + ":" + str(x) + "= "
            div_ans = z
            question_log[counter] = [div_sum, div_ans, 0, 0,0]
            counter +=1

    file = open('question_log', 'wb')
    pickle.dump(question_log, file)
    file.close()

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

def generate_walkthrough_question_list(tafel):
    global question_log
    walkthrough_question_lists = {}
    new_question_list = {}
    walkthrough_question_lists[2] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,45,67,89,111,133,155,177,199,221]
    walkthrough_question_lists[3] = [23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,2,46,68,90,112,134,156,178,200,222]
    walkthrough_question_lists[4] = [45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,3,25,69,91,113,135,157,179,201,223]
    walkthrough_question_lists[5] = [67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,4,26,48,92,114,136,158,180,202,224]
    walkthrough_question_lists[6] = [89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,5,27,49,71,115,137,159,181,203,225]
    walkthrough_question_lists[7] = [111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,6,28,50,72,94,138,160,182,204,226]
    walkthrough_question_lists[8] = [133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,7,29,51,73,95,117,161,183,205,227]
    walkthrough_question_lists[9] = [155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,8,30,52,74,96,118,140,184,206,228]
    walkthrough_question_lists[10] = [177,178,179,180,181,182,183,184,185,186,187,188,190,191,192,193,194,195,196,197,198,9,31,53,75,97,119,141,163,207,229]
    walkthrough_question_lists[11] = [199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,10,32,54,76,98,120,142,164,230]
    walkthrough_question_lists[12] = [221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,11,33,55,77,99,121,143,165]
    for q_id in walkthrough_question_lists[tafel]:
        new_question_list[q_id] = question_log[q_id]
    return new_question_list

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
    Specify a quiz time on running script to make toets longer or shorter (default 60 seconds)
    """
    global try_agains
    global question_log
    global quiz_time
    correct = 0
    incorrect = 0
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
    global quiz_time
    if quiz_time in high_scores:
        current_high_scores = high_scores[quiz_time]
    else:
        high_scores[quiz_time] = {}
        current_high_scores = high_scores[quiz_time]
    success_perecentage = round((total_correct /(total_correct + total_incorrect))*100)
    if total_correct in current_high_scores:
        if success_perecentage in current_high_scores[total_correct]:
            current_high_scores[total_correct][success_perecentage].append(player)
        else:
           current_high_scores[total_correct][success_perecentage]=[player]
    else:
        current_high_scores[total_correct] = {success_perecentage: [player]}
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
    global quiz_time
    if quiz_time in high_scores:
        current_high_scores = high_scores[quiz_time]
    else:
        high_scores[quiz_time] = {}
        current_high_scores = high_scores[quiz_time]
    print("High scores for {} second tempotoets\n".format(quiz_time))
    current_high_score_keys = list(current_high_scores.keys())
    top_scores = sorted(current_high_score_keys, reverse = True)
    rank = 1
    if len(current_high_scores) > 0:
        for top_score in range(10):
            try:
                answered_correctly = top_scores[top_score]
                success_ratio_keys = sorted(list(current_high_scores[answered_correctly].keys()), reverse =True)
                for s_r in success_ratio_keys:
                    top_scoring_names = []
                    print(rank, "> ", end="")
                    print(str(answered_correctly), "correct ("+ str(s_r) + "%) -", end = "")
                    for name in current_high_scores[answered_correctly][s_r]:
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
    global quiz_time
    qlist = False
    trylist = False
    toughlist = False
    header()
    print("TOETS MODE...")
    print("[1] - Do the {} second TEMPO TOETS!!!".format(quiz_time))
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
    print("[6] - Pick a table to to practice")
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
    elif user_action == "6":
        table_num = False
        table_to_practice = input("which number do you want to practice?")
        while table_num == False:
            try:
                table_to_practice = int(table_to_practice)
                if table_to_practice < 2 or table_to_practice > 12:
                    print("Not a valid input - enter a number between 2 and 12")
                    table_to_practice = input("which number do you want to practice?")
                else:
                    table_num = True
            except ValueError:
                print("Not a valid input - enter a number between 2 and 12")
                table_to_practice = input("which number do you want to practice?")
        question_list = generate_walkthrough_question_list(table_to_practice)
        try_agains = ask_question(question_list)
        input("Press [ENTER] to continue...")
        main_menu(try_agains)
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

set_highscore_questionlog()
main_menu()
