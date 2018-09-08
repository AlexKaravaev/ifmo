import sys
import pickle
from graphviz import Digraph

""" Programm for generating quesitons and answers"""

def makeQuestion(question, correctAns, wrongAns):
    return [question, correctAns, wrongAns]

def askQuestion(question):
    print("\r{}".format(question))
    return sys.stdin.readline().strip().lower()

#Проверить является ли вопросом,или ответом на загадку пользователя
def isQuestion(candidate):
    return type(candidate).__name__ == "list"

def getAnswer(question):
    if isQuestion(question):
        return askQuestion(question[0])
    else:
        return askQuestion("Ты думал о {} язык?".format(question))

def ifYes(answer):
    print(answer.lower() == "да")
    return answer.lower() == "да"

def playAgain():
    return True

def correctGuess(msg):
    global tries

    print("Победа! Я использовал {} попыток".format(tries))

    if playAgain():
        tries = 0
        return Q
    else:
        sys.exit(0)

def nextQuestion(question, answer):
    global tries
    tries += 1

    if isQuestion(question):
        if answer:
            return question[1]
        else:
            return question[2]
    else:
        if answer:
            return correctGuess("Это было очевидно...")
        else:
            return makeNewQuestion(question)

def replaceAns(tree, find, replace):
    if not isQuestion(tree):
        if tree == find:
            return replace
        else:
            return tree
    else:
        return makeQuestion(tree[0], replaceAns(tree[1], find, replace), replaceAns(tree[2],find,replace))

def count_available_langs(Q, counter):
    global dot
    if isQuestion(Q):
        for i in range(1,3):
            dot.node(str(Q),str(Q[0]))
            if i == 2:
                dot.edge(str(Q), str(Q[i]), label='нет')
            else:
                dot.edge(str(Q), str(Q[i]), label='да')
            sub_counter = 0
            counter += count_available_langs(Q[i], sub_counter)
    else:
        print(Q)
        dot.node(str(Q),str(Q))
        #dot.edge(str(Q),str(Q[i]))
        return 1
    return counter

def makeNewQuestion(wrongLang):
    global Q, tries, dot

    correctLang = askQuestion("Я сдаюсь. Какой правильный ответ?")

    newQuestion = askQuestion("Введи вопрос, который бы отличил {} язык от {} язык".format(correctLang, wrongLang))

    AnswerIsYes = ifYes(askQuestion("Если бы я задал этот вопрос и ты думал про {} язык, то какой был бы ответ".format(correctLang)))

    if AnswerIsYes:
        q = makeQuestion(newQuestion, correctLang, wrongLang)
    else:
        q = makeQuestion(newQuestion, wrongLang, correctLang)

    Q = replaceAns(Q, wrongLang, q)
    tries = 0
    with open('question_database', 'wb') as f:
        pickle.dump(Q, f)
    return Q

if __name__ == '__main__':

    tries = 0

    try:
        with open('question_database', 'rb') as f:
            Q = pickle.load(f)
    except FileNotFoundError:
        Q = (makeQuestion('Ваш язык произошел от греческого?',"английский","китайский"))
    dot = Digraph(comment = 'Дерево вопросов')
    print("Database: {}".format(Q))
    print("Список доступных языков: ")
    print("На данный момент доступно {} языков".format(count_available_langs(Q, 0)))
    dot.render('test-output/question_tree.gv', view=True)
    q = Q

    try:
        while True:
            ans = ifYes(getAnswer(q))
            q = nextQuestion(q, ans)
    except KeyboardInterrupt:
        sys.exit(0)
