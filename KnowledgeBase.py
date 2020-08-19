# a4.py Gergely Sajdik 301142046

# returns True if, and only if, string s is a valid variable name
def is_atom(s):
    if not isinstance(s, str):
        return False
    if s == "":
        return False
    return is_letter(s[0]) and all(is_letter(c) or c.isdigit() for c in s[1:])

def is_letter(s):
    return len(s) == 1 and s.lower() in "_abcdefghijklmnopqrstuvwxyz"


#Runs the program until a user exits. Takes user input and performs either load, tell, or infer.
def runKB():
    theKnowledgeBase = []
    global theInOutBase
    theInOutBase = []
    global inferredAtoms
    inferredAtoms = {}
    global isRunning
    isRunning = True
    global tellCounter
    tellCounter = 0
    while isRunning == True:
        userInput = input("\n" + "kb>")
        theInput = userInput.split()
        fixedInput = theInput[0].lower()
        if fixedInput == "load":
            if len(theInput) > 1:
                theKnowledgeBase = runLoader(theInput)
                inferredAtoms = {}
            else:
                print("Error: specify a file to open")
        elif fixedInput == "tell":
            theKnowledgeBase = runTeller(theInput, theKnowledgeBase)
        elif fixedInput == "infer_all":
            if len(theKnowledgeBase) == 0:
                print("Error: must load a valid KB first")
            elif tellCounter == 0:
                print("Error: no atoms can be inferred until at least one tell command is called")
            else:
                newlyInferredAtoms = runInferer(theKnowledgeBase)
                print("  Newly inferred atoms:")
                if bool(newlyInferredAtoms) == False:
                    print("     <none>")
                else:
                    printDict(newlyInferredAtoms, True)
                print("  Atoms already known to be true:")
                printDict(inferredAtoms, False)
                if len(newlyInferredAtoms) > 0:
                    for key, value in newlyInferredAtoms.items():
                        tempDictionary = {key: value}
                        inferredAtoms.update(tempDictionary)
        elif fixedInput == "exit":
            isRunning = False
        else:
            print("Error: unknown command " + "\"" + theInput[0] + "\"")


#Displays and formats the contents of a dictionary
def printDict(theDict, newlyInferred):
    if len(theDict) == 1:
        result = "     " + next(iter(theDict.values()))
        print(result)
    else:
        tempCounter = 0
        result = "     "
        for key, value in theDict.items():
            if tempCounter == (len(theDict)-1):
                result = result + str(value)
            else:
                if newlyInferred == True:
                    result = result + str(value) + " "
                else:
                    result = result + str(value) + ", "
                tempCounter += 1
        print(result)


#Loads text file and populates the KB and InOut list
def runLoader(theInput):
    fileToLoad = theInput[1]
    fileExists = True
    validFormat = True
    rulesAdded = 0
    global theInOutBase
    global tellCounter
    theInOutBase = []
    theKnowledgeBase = []

    try:
        f = open(fileToLoad, "r")
    except FileNotFoundError:
        fileExists = False
        print('File does not exist.')

    if fileExists == True:
        f = open(fileToLoad, "r")
        fileContents = f.read()
        for line in fileContents.splitlines():
            tempArrayKB = []
            tempArrayInOut = []
            rulesAdded += 1
            currentTextLine = line.split()
            if len(currentTextLine) < 3:
                validFormat = False
            else:
                for i in range(len(currentTextLine)):
                    if i == 0:
                        if is_atom(currentTextLine[i]) == False:
                            validFormat = False
                        else:
                            tempArrayKB.append(currentTextLine[i])
                            tempArrayInOut.append("out")
                    elif i == 1:
                        if currentTextLine[i] != "<--":
                            validFormat = False
                    elif currentTextLine[i] != "&":
                        if is_atom(currentTextLine[i]) == False:
                            validFormat = False
                        else:
                            tempArrayKB.append(currentTextLine[i])
                            tempArrayInOut.append("out")
            theKnowledgeBase.append(tempArrayKB)
            theInOutBase.append(tempArrayInOut)
        if validFormat == False:
            print("Error: " + fileToLoad + " is not a valid knowledge base")
        else:
            tellCounter = 0
            print(fileContents)
            print(str(rulesAdded) + " new rule(s) added")
    return theKnowledgeBase


#Adds given atoms to the given KB and updates the InOut list as needed
def runTeller(theInput, theKnowledgeBase):
    global theInOutBase
    global tellCounter
    tellCounter = 0
    if len(theInput) < 2:
        print("Error: tell needs at least one atom")
    elif len(theKnowledgeBase) == 0  or len(theInOutBase) == 0:
        print("Error: must load a valid KB before using \"tell\"")
    else:
        areValidAtoms = True
        for i in range(1,len(theInput)):
            if is_atom(theInput[i]) == False:
                areValidAtoms = False
                print("Error: " + "\"" + theInput[i] + "\"" + " is not a valid atom")
                break
        if areValidAtoms == True:
            iterationLength = len(theKnowledgeBase)
            for i in range(1,len(theInput)):
                for j in range(0,iterationLength):
                    if isinstance(theKnowledgeBase[j], list):
                        if theInput[i] in theKnowledgeBase[j]:
                            theInOutBase[j][theKnowledgeBase[j].index(theInput[i])] = "in"
                if theInput[i] in theKnowledgeBase or theInput[i] in inferredAtoms:
                    print("  atom " + "\"" + theInput[i] + "\"" + " already known to be true")
                    tellCounter += 1
                else:
                    tellCounter += 1
                    theKnowledgeBase.append(theInput[i])
                    theInOutBase.append(["in"])
                    print("  " + "\"" + theInput[i] + "\"" + " added to KB")
    return theKnowledgeBase
        

#Checks for inference and adds atoms to inferred dictionary
def runInferer(theKnowledgeBase):
    global inferredAtoms
    newlyInferredAtoms = {}
    tellCounter = 0
    for i in range(0,len(theKnowledgeBase)):
        if isinstance(theKnowledgeBase[i],str) == True:
            tellCounter += 1
    if tellCounter > 0:
        for i in range(0,len(theKnowledgeBase)):
            if isinstance(theKnowledgeBase[i],list) == True:
                newlyInferredAtoms = testInference(theKnowledgeBase, newlyInferredAtoms)
            else:
                if theKnowledgeBase[i] in inferredAtoms.values():
                    None
                else:
                    tempDictionary = {theKnowledgeBase[i]: theKnowledgeBase[i]}
                    inferredAtoms.update(tempDictionary)
    return newlyInferredAtoms


#Updates the InOut list if a new atom is inferred
def updateInOutBase(theKnowledgeBase, theValue):
    for i in range(0,len(theKnowledgeBase)):
        if isinstance(theKnowledgeBase[i],list) == True:
                if theValue in theKnowledgeBase[i]:
                    theInOutBase[i][theKnowledgeBase[i].index(theValue)] = "in"


#Checks to see if a new atom can be inferred and returns a dictionary
def testInference(theKnowledgeBase, newlyInferredAtoms):
    atomTracker = newlyInferredAtoms
    for i in range(0,len(theKnowledgeBase)):
        if isinstance(theKnowledgeBase[i],list) == True:
            canBeInferred = True
            for j in range(1,len(theKnowledgeBase[i])):
                if theInOutBase[i][j] == "out":
                    canBeInferred = False
            if canBeInferred == True:
                if theKnowledgeBase[i][0] in inferredAtoms.values() or theKnowledgeBase[i][0] in newlyInferredAtoms.values():
                    None
                else:
                    tempDictionary = {theKnowledgeBase[i][0]: theKnowledgeBase[i][0]}
                    atomTracker.update(tempDictionary)
                    updateInOutBase(theKnowledgeBase, theKnowledgeBase[i][0])
                    testInference(theKnowledgeBase,atomTracker)
    return atomTracker
    

#Run the KB--------------------------------------------------------------------------------------

runKB()
