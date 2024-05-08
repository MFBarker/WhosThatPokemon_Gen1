#imports
import PySimpleGUI as sg
import os
import json
import random
"""
Unicode Decoding
' - \u0027
" - \u0022
♀ (female) - \u2640
♂ (male) - \u2642
"""

#CHEAT MODE
cheatMode = True

#load files
dbFileName = "db.json"

sg.theme("LightGrey3")

layout = [
    [sg.Text("Who's That Pok\u00E9mon?")],
    [sg.Text("Press Submit to Start the Game!",key="hints")],
    [sg.Text("Input Guess: "), sg.InputText(key="INPUT",do_not_clear=False),sg.Button("Submit")], #https://stackoverflow.com/questions/68691097/pysimplegui-how-do-you-remove-text-from-input-text-box
    [sg.Text("",key="results")],
    [sg.Text("Hint: For specific gendered Pok\u00E9mon, format input as \u0022[name] [gender]\u0022.")]
]

wordBank = []
alreadydone = []

gotWrong = []
inputted = []

global noneLeft
noneLeft = False

word = None
global score
score = 0


gameStart = False
previousAnswered = False

window = sg.Window("Who's That Pok\u00E9mon? (Gen. 1)", layout)

def loadRecords():
    if os.path.isfile(dbFileName):
        print("db.json found. loading records")
        file = open(dbFileName)
        global wordBank
        wordBank = json.load(file)
    else:
        window["results"].Update("File Not Found. Are you forgetting something?")

def chooseRandomWord():
    i = random.randint(0,len(wordBank["KantoDex"])-1)
    selectedWord = wordBank["KantoDex"][i]
    # print(selectedWord) tst
    if alreadydone.__contains__(selectedWord):
        selectedWord = None
    else:
        alreadydone.append(selectedWord)
        return selectedWord
    
def startGame():
    global word
    word = None
    while word == None:
        word = chooseRandomWord()
    if cheatMode == True:
        print("Pok\u00E9mon:",word["name"])
    if len(alreadydone) == 151:
        global noneLeft
        noneLeft = True
    global hint
    hint = "Type: " + word["type"] + "     Height: " + word["height"] + "     Weight: " + word["weight"]
    window["hints"].print(hint)
    window["results"].print("Question " + str(len(alreadydone)) + " of " + str(len(wordBank["KantoDex"])) + "  -  Score: " + str(score))

def correct():
    global previousAnswered
    global score
    print("Correct!")
    score += 1
    previousAnswered = True
def incorrect(val:str):
    global previousAnswered
    print("Incorrect!")
    previousAnswered = True
    gotWrong.append(str(word["name"]))
    inputted.append(val)

#__________________________________________________________________________________________________
loadRecords()

while (len(alreadydone) <= len(wordBank["KantoDex"])): #needs fixing

    if word != None and previousAnswered == True and noneLeft == False:
        previousAnswered = False
        startGame()
    elif noneLeft == True:
        break
    event, values = window.Read()

    if event == sg.WIN_CLOSED or event == "Cancel":
        break
    elif event == "Submit" and gameStart == False:
        print("Game Start")
        window["hints"].update("")
        startGame()
        gameStart = True
    #main code goes here
    if(str(values["INPUT"]) != ""):
        if(word["name"].__contains__("\u2640")): #female
            substr, substr2 = str(values["INPUT"]).split(" ")
            if(substr2.lower() == "female" and substr.lower() == "nidoran"):
                correct()
            else:
                incorrect(str(values["INPUT"]))
        elif (word["name"].__contains__("\u2642")): #male
            substr, substr2 = str(values["INPUT"]).split(" ")
            if(substr2.lower() == "male" and substr.lower() == "nidoran"):
                correct()
            else:
                incorrect(str(values["INPUT"]))
        elif str(word["name"]) == "Mr. Mime":
            if(str(values["INPUT"]).lower() == "mr.mime" or str(values["INPUT"]).lower() == "mr. mime"):
                correct()
            else:
                incorrect(str(values["INPUT"]))
        else:
            if(str(word["name"]).lower() == str(values["INPUT"]).lower()):
                correct()
            else:
                incorrect(str(values["INPUT"]))
    if(previousAnswered == True):
        window["hints"].update("")
        window["results"].update("")
#
print("All Done! You got", score, "out of", len(alreadydone), "correct!")

if(len(gotWrong) != 0):
    print("Pok\u00E9mon that you got wrong:")
    it = 0
    while it < len(gotWrong):
        print(gotWrong[it] + ": \u0022" + inputted[it] + "\u0022")
        it+=1

window.close()

