import pickle

question_log = {}

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

for q in question_log:
    print(q, question_log[q])

file = open('question_log', 'wb')
pickle.dump(question_log, file)
file.close()