import sys
import pickle

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

def makeNewQuestion(wrongLang):
    global Q, tries

    correctLang = askQuestion("Я сдаюсь. Какой правильный ответ?")

    newQuestion = askQuestion("Введи вопрос, который бы отличил {} язык от {} язык".format(correctLang, wrongLang))

    AnswerIsYes = ifYes(askQuestion("Если бы я задал этот вопрос и ты думал про {} язык, то какой был бы ответ".format(correctLang)))

    if AnswerIsYes:
        q = makeQuestion(newQuestion, correctLang, wrongLang)
    else:
        q = makeQuestion(newQuestion, wrongLang, correctLang)

    Q = replaceAns(Q, wrongLang, q)
    tries = 0
    return Q

tries = 0
Q = (makeQuestion('Этот язык является родным для более чем 1 млрд человек?',"китайский","русский"))
q = Q

try:
    while True:
        ans = ifYes(getAnswer(q))
        q = nextQuestion(q, ans)
except KeyboardInterrupt:
    sys.exit(0)
