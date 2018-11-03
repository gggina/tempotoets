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
ids_for_each_table = {}


def set_highscore_questionlog ():
    global high_scores
    global question_log
    global ids_for_each_table
    # high_scores = {quiz_time:{total_correct: [{success_percentage_1: [player_1, player_2...]}, {success_percentage_2: [player_3, player_4...]}]}}
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

    #ids_for_each_table = {table:[q_id, q_id, ...]}
    try:
        file = open('ids_for_each_table', 'rb')
        ids_for_each_table = pickle.load(file)
        file.close()
    except FileNotFoundError:
        generate_question_log()


def generate_question_log():
    global question_log
    global ids_for_each_table
    print("generating new question log")

    #change the below values to generate a larger/smaller question log
    all_tables = 12
    top_table = 12

    #counter is used to generate a unique ID for each question in the question log (the dictionary key)
    counter = 1

    for x in range(2, (top_table+1)):
        for y in range (2, (all_tables+1)):
            multi_sum = str(x) + "x" + str(y)+ "= "
            multi_ans = x*y
            question_log[counter] = [multi_sum, multi_ans, 0, 0, 0]
            if y in ids_for_each_table:
                ids_for_each_table[y].append(counter)
            else:
                ids_for_each_table[y] = [counter]
            counter +=1
            div_sum =  str(x*y) + ":" + str(x) + "= "
            div_ans = y
            question_log[counter] = [div_sum, div_ans, 0, 0,0]
            if x in ids_for_each_table:
                ids_for_each_table[x].append(counter)
            else:
                ids_for_each_table[x] = [counter]
            counter +=1

    for table in ids_for_each_table:
        ids_for_each_table[table]= sorted(ids_for_each_table[table])

    file = open('question_log', 'wb')
    pickle.dump(question_log, file)
    file.close()
    file = open('ids_for_each_table', 'wb')
    pickle.dump(ids_for_each_table, file)
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
        question_number = str(ids_guesses[q][0])
        question = question_log[q][0]
        correct_answer = str(question_log[q][1])
        player_answer = str(ids_guesses[q][-1])
        while len(question_number) < 2:
            question_number = question_number + " "
        while len(question) <8:
            question = question + " "
        while len(player_answer) <4:
            player_answer = player_answer + " "
        while len(question_log[q][0]+ correct_answer) < 11:
            correct_answer = correct_answer + " "
        print("question {0} > {1}your answer: {2} correct answer:  >> {3}{4} <<".format(question_number, question, player_answer, question_log[q][0], correct_answer))


def generate_walkthrough_question_list(tafel):
    global question_log
    global ids_for_each_table
    new_question_list = {}
    for q_id in ids_for_each_table[tafel]:
        new_question_list[q_id] = question_log[q_id]
    return new_question_list


def answer_question(question_id, q):
    """
    asks the question_id from the question_log (question number q in the current quiz)
    used by all quiz options
    """
    global question_log
    question_log[question_id][4] +=1
    question = question_log[question_id][0]
    answer = input("question {0} > {1}".format(q, question))
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
#            main_menu(try_agains)
            main_menu()
        q +=1
    print("\nSTOPPING THE TIMER... ")
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
        print("You answered {} question(s) incorrectly:\n".format(len(try_agains)))
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
    while len(player)>12:
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
#            main_menu(try_agains)
            main_menu()
        q +=1
        total_time = round((time.time()-start),2)
    print("STOP!!")
    print("time's up.")
    print("............... ")
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
    Checks if the results of a tempotoets warrant adding to the high_scores list
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
                answered_correctly_string = str(answered_correctly)
                success_ratio_keys = sorted(list(current_high_scores[answered_correctly].keys()), reverse =True)
                for s_r in success_ratio_keys:
                    top_scoring_names = []
                    current_rank = str(rank)
                    if len(current_rank) <2:
                        current_rank = " " + current_rank
                    current_success_ratio = "(" + str(s_r) + "%)"
                    while len(current_success_ratio) <6:
                        current_success_ratio = current_success_ratio + " "
                    for name in current_high_scores[answered_correctly][s_r]:
                        top_scoring_names.append(name)
                    top_scoring_names = top_scoring_names[::-1]
                    name_num=1
                    high_scorer_names = ""
                    for tsn in top_scoring_names:
                        if name_num <= 4:
                            high_scorer_names = high_scorer_names+" ["+  tsn + "]"
                            name_num +=1
                    print("{0} >  {1} correct {2} -{3}".format(current_rank, answered_correctly_string, current_success_ratio, high_scorer_names))
                    rank +=1
            except IndexError:
                current_rank = str(top_score+1)
                if len(current_rank) <2:
                    current_rank = " " + current_rank
                while len(current_rank) <2:
                    current_rank = current_rank + " "
                print("{} >  ... ".format(current_rank))
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
    print(">         TEMPOTOETS           <")
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
    #paging info - number of pages of 1o items required
    total_pages = 1
    if len(tricky_ones) > 10:
        total_pages = round((len(tricky_ones)+1)/10)
        if (len(tricky_ones)+1)%10 > 0:
            total_pages +=1

    if len(fails) > 0:
        tricky_rank = 1
        page_number = 1
        counter = 1
        print("Questions with fail rate of 20% or more:\n")
        print("Page {0} of {1} \n".format(page_number,total_pages))
        for fail_perc in fails:
            for tricky_q in tricky_ones:
                if tricky_ones[tricky_q][0] == fail_perc:
                    tricky_q_id = tricky_ones[tricky_q][1]
                    tricky_question = question_log[tricky_q_id][0]
                    tricky_answer = str(question_log[tricky_q_id][1]) + " "
                    while len(tricky_question) + len(tricky_answer) < 13:
                        tricky_answer = tricky_answer + "."
                    current_tricky_rank = str(tricky_rank)
                    if len(current_tricky_rank) < 2:
                        current_tricky_rank = " " + current_tricky_rank
                    success_rate = str(100-fail_perc) + "%"
                    for n in range (4-len(success_rate)):
                        tricky_answer = tricky_answer + "."
                    total_attempts = str(question_log[tricky_q_id][4])
                    print("{0} >  {1}{2} {3} correct ({4} attempts)".format(current_tricky_rank,tricky_question,tricky_answer, success_rate, total_attempts))
                    tough_list[tricky_q_id] = question_log[tricky_q_id]
                    tricky_rank +=1
                    counter += 1
                    if counter == 11:
                        counter = 1
                        page_number += 1
                        input("\nPress [ENTER] for next page... ")
                        header()
                        print("Questions with fail rate of 20% or more:\n")
                        print("Page {0} of {1}\n".format(page_number,total_pages))

    else:
        if len(fails) == len(question_log):
            print("No questions answered yet.\n")
        else:
            print("All questions have been successfully answered at least 80% of the time.\n")


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


def main_menu():
    """
    the main menu. hidden option is "clear high scores"
    """
    file = open('question_log', 'wb')
    pickle.dump(question_log, file)
    file.close()
    global question_list
    global tough_list
    global quiz_time
    global try_agains
    qlist = 0
    trylist = 0
    toughlist = 0
    header()
    print("TOETS MODE... ")
    print("[1] - Do the {} second TEMPOTOETS!!!".format(quiz_time))
    print("\n\n")
    print("PRACTICE MODE... ")
    print("[2] - New set of random questions")
    if len(question_list) > 0:
        qlist = 1
        print("[3] - Play the same questions again (random order)")
    else:
        print("[ ] - ... not available yet")
    if len(try_agains) >0:
        trylist = 1
        print("[4] - Retry the questions you got wrong last time")
    else:
        print("[ ] - ... not available yet")
    if len(tough_list) >0:
        toughlist = 1
        print("[5] - ** TRY SOME TRICKY QUESTIONS!!! **")
    else:
        print("[ ] - ... not available yet")
    print("[6] - Pick a table to to practice")
    print("\n")
    print("----------------")
    print("[h] - TEMPOTOETS high scores")
    print("[stats] - find out the tricky questions")
    print("[t] - change the tempotoets timer")
    print("[q] - quit this game")
    print("\n")
    user_action = input("What do you want to do? ")
    if user_action == "2":
        number_of_questions = input("how many questions do you want? ")
        try:
            number_of_questions = int(number_of_questions)
        except ValueError:
            number_of_questions = 10
            print("Not a valid input - will generate a list with 10 questions.")
            input("Press [ENTER] to continue... ")
        question_list = generate_questions(number_of_questions)
        try_agains = ask_question(question_list)
    elif user_action == "3":
        if qlist == 1:
            old_qs = list(question_list.keys())
            random.shuffle(old_qs)
            new_question_list = {}
            for i in range(len(old_qs)):
                new_question = old_qs[i]
                new_question_list[new_question] = question_list[new_question]
            try_agains = ask_question(new_question_list)
        else:
            print("...option not available yet, do the tempotoets or practice with a table or some random questions first")
    elif user_action == "4":
        if trylist == 1:
            try_agains = ask_question(try_agains)
        else:
            print("...option not available yet, do the tempotoets or practice with a table or some random questions first")
    elif user_action == "5":
        if toughlist == 1:
            if len(tough_list) > 10:
                old_qs = list(tough_list.keys())
                random.shuffle(old_qs)
                tough_play_list = {}
                for i in range(10):
                    new_question = old_qs[i]
                    tough_play_list[new_question] = tough_list[new_question]
            else:
                tough_play_list = tough_list
            question_list = tough_play_list
            try_agains = ask_question(tough_play_list)
        else:
            print("...option not available yet, do the tempotoets or practice with some random questions first")
    elif user_action == "1":
        try_agains = do_the_tempo_toets()
    elif user_action == "6":
        table_num = 0
        table_to_practice = input("which number do you want to practice? ")
        while table_num == 0:
            try:
                table_to_practice = int(table_to_practice)
                if table_to_practice < 2 or table_to_practice > 12:
                    print("Not a valid input - enter a number between 2 and 12")
                    table_to_practice = input("which number do you want to practice? ")
                else:
                    table_num = 1
            except ValueError:
                print("Not a valid input - enter a number between 2 and 12")
                table_to_practice = input("which number do you want to practice? ")
        print(table_num, table_to_practice)
        question_list = generate_walkthrough_question_list(table_to_practice)
        try_agains = ask_question(question_list)
    elif user_action == "9" or user_action == "h":
        header()
        read_high_score()
        print("")
    elif user_action == "clear high scores":
        action = input("Clear high scores? (y/n)")
        if action == "y":
            global high_scores
            high_scores = {}
            file = open('high_scores', 'wb')
            pickle.dump(high_scores, file)
            file.close()
            print("High scores cleared - no going back.")
    elif user_action == "stats":
        question_stats()
#        print("")
#        input("Press [ENTER] to list questions that have not yet been asked... ")
#        the_unaskeds()
    elif user_action == "t":
        new_quiz_time = input("Set the tempotoets timer to how many seconds (current {})? ".format(quiz_time))
        new_time_success = 0
        while new_time_success == 0:
            try:
                new_quiz_time = int(new_quiz_time)
                if new_quiz_time >=2 and new_quiz_time <=120:
                    new_time_success += 1
                    quiz_time = new_quiz_time
                else:
                    new_quiz_time = input("Set the tempotoets timer to how many seconds (current {})? ".format(quiz_time))
            except ValueError:
                print("Not a valid input = enter a number between 2 and 120")
                new_quiz_time = input("Set the tempotoets timer to how many seconds (current {})? ".format(quiz_time))
    elif user_action == "q":
        print ("...goodbye")
        sys.exit(2)
    input("\nPress [ENTER] to go back to the menu... ")
    main_menu()

set_highscore_questionlog()
main_menu()
