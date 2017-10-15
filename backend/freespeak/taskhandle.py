def getcontext(snt):
    modFlag = False
    modListFlag = False
    # TODO: make array of tasks and have modifiers correspond to tasks
    for index, word in enumerate(snt):
        if snt[index][1] == "MODIFIER":
            modFlag = True

        if modFlag and snt[index][1] == "NUMBER":
            modListFlag = True
            snt[index] = (snt[index][0], "PARAMETER")

        elif modFlag and modListFlag and snt[index][1] != "NUMBER":
            modFlag = False
            modListFlag = False

    for index in range(len(snt) - 1, -1, -1):
        if snt[index][1] == "NUMBER" or snt[index][0] == "":
            snt.pop(index)

    return snt
