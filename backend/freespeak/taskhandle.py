

def getcontext(snt):
    for index, word in enumerate(snt):
        if index == 0:
            continue
        if word[1] == "NUMBER" and (snt[index-1][1] == "MODIFIER" or snt[index-1][1] == "NUMBER" or snt[index-1][1] == "PARAMETER"):
            snt[index] = (word[0],"PARAMETER")
        elif word[1] == "NUMBER" and (snt[index+1][1] == "NUMBER" or snt[index+1][1] == "MODIFIER"):
            snt[index] = (word[0], "PARAMETER")
        if word[1] == "SUPERFLUOUS":
            snt.pop(index)

        if snt[index][1] == "NUMBER":
            snt.pop(index)
    return snt
