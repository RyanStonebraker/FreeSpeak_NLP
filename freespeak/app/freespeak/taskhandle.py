import numpy
import collections
# import pdb


# a function that returns the "purpose" of each command, this was made modular
# just in case it was decided more information was needed
def structure_output(task="", structure="", params=[], paramtype=""):
    if task == "":
        return
    return {"TASK": task, "STRUCTURE": structure, "PARAMETERS": params, "TYPE": paramtype}


# tries to cast a string to an integer and if fails, then casts to a float and
# if THAT fails, then it gives up
def to_num(strNum):
    try:
        return int(strNum)
    except:
        try:
            return float(strNum)
        except:
            raise ValueError("to_num parameter:" + str(strNum) + " not a number!")


# The definition of pythonic programming... if to_num doesn't throw, then
# that is returned, else whatever was passed is just returned unaffected
def maybe_num(param):
    try:
        return to_num(param)
    except:
        return param


# necessary to implement a sort of lazy rounding function in python
def roundCutOff(num):
    return ('%f' % num).rstrip('0').rstrip('.')


# rounds the numbers returned between begin and end incrementing by inc
# uses maybe_num just to make extra sure this doesn't throw
def through_mod(begin, end, inc=1):
    strthrough = [roundCutOff(num) for num in numpy.arange(begin + inc, end + inc, inc)]
    return [maybe_num(num) for num in strthrough]


# converts any word to a specified ctype
def convertParam(param, ctype):
    if ctype == "integer":
        try:
            return int(param)
        except:
            return int(float(param))
    elif ctype == "float":
        return float(param)
    elif ctype == "string":
        return str(param)
    elif ctype == "boolean":
        return bool(param)
    else:
        return param


# converts a list of params to a ctype canonically using convertParam
def convertParams(params, ctype):
    new_params = []
    for param in params:
        new_params.append(convertParam(param, ctype))
    return new_params


# checks type of each word in list and converts every word in list to whatever
# word has the highest type precedence
def autoConvert(params):
    auto_type = "string"
    if not isinstance(params, collections.Iterable):
        params = [params]
    for param in params:
        if isinstance(param, str):
            auto_type = "string"
            break
        elif isinstance(param, bool):
            auto_type = "boolean"
            continue
        elif isinstance(param, float) and auto_type != "bool":
            auto_type = "float"
            continue
        elif isinstance(param, int) and auto_type != "float" and auto_type != "bool":
            auto_type = "integer"
            continue
    return (convertParams(params, auto_type), auto_type)


# Massive function that attempts to understand what is being asked in each
# sentence. It handles multiple commands in a single sentence by "flushing"
# previous context when a new task word is read.
def getcontext(snt_raw):
    snt = [wrd for wrd in snt_raw if wrd[0] != '' and wrd[1] != "SUPERFLUOUS"]

    # PRE-MAIN PROCESSING LOOP (HANDLES PEMDAS)
    for index, word in enumerate(snt):
        if snt[index][1] == "MODIFIER":
            if snt[index][0] == "multiplied":
                if len(snt) > index + 1 and snt[index - 1][1] == "NUMBER" and snt[index + 1][1] == "NUMBER":
                    snt[index - 1] = (str(roundCutOff(to_num(snt[index - 1][0]) * to_num(snt[index + 1][0]))), "NUMBER")
                    del snt[index]
                    del snt[index]
                elif len(snt) > 0 and snt[index - 1][1] == "NUMBER":
                    snt[index] = snt[index - 1]
                    snt[index - 1] = ("with", "MODIFIER")

            elif snt[index][0] == "divided" and len(snt) > index + 1 and snt[index - 1][1] == "NUMBER" and snt[index + 1][1] == "NUMBER":
                # print("<script>console.log(" + str(((to_num(snt[index - 1][0]) / to_num(snt[index + 1][0])), "NUMBER")[) + ")</script>")
                snt[index - 1] = (str(roundCutOff(to_num(snt[index - 1][0]) / to_num(snt[index + 1][0]))), "NUMBER")
                del snt[index]
                del snt[index]

    ordered_jobs = []
    current_params = []
    start_find = False
    modForwardParams = False
    c_task = ""
    add_to = -1
    c_structure = ""
    c_type = "auto"
    ignore_next = False
    skip_iter = False

    for index, word in enumerate(snt):
        if skip_iter:
            skip_iter = False
            continue
        # Pre Task Modifiers
        if snt[index][1] == "MODIFIER" and not start_find:
            if snt[index][0] == "not":
                ignore_next = True
                continue

        if snt[index][1] == "TASK" and start_find:
            # Inner Pre Task Modifiers
            if snt[index - 1][1] == "MODIFIER":
                if snt[index - 1][0] == "not":
                    start_find = False
                    continue
            if c_type == "auto":
                auto_converted = autoConvert(current_params)
                current_params = auto_converted[0]
                c_type = auto_converted[1]
            else:
                current_params = convertParams(current_params, c_type)

            ordered_jobs.append(structure_output(task=c_task, structure=c_structure, params=current_params, paramtype=c_type))
            current_params = []
            add_to = -1
            c_task = snt[index][0]
            c_structure = ""
            c_type = "auto"
            modForwardParams = False
            continue

        # If not already in a task, starts a context search based on current
        # task word
        if snt[index][1] == "TASK" and not start_find:
            if ignore_next:
                ignore_next = False
                continue
            start_find = True
            c_task = snt[index][0]
            continue

        # resets the mathematical optimization flag
        if snt[index][0] != "plus" and snt[index][0] != "minus":
            add_to = -1

        # If a task was found, then start looking for context
        if start_find:
            if snt[index][1] == "STRUCTURE":
                if index - 1 > 0 and snt[index - 1][1] == "NUMBER":
                    current_params.append(to_num(snt[index - 1][0]))
                c_structure = snt[index][0]
                continue

            # MODIFIER SUBROUTINES
            if snt[index][1] == "MODIFIER":
                if snt[index][0] == "with" or snt[index][0] == "include" or snt[index][0] == "of":
                    modForwardParams = True
                    continue

                if snt[index][0] == "plus" or snt[index][0] == "minus":
                    if (snt[index - 1][1] == "PARAMETER" or snt[index - 1][1] == "NUMBER") and snt[index + 1][1] == "NUMBER":
                        if add_to == -1:
                            add_to = len(current_params) - 1
                        if snt[index][0] == "plus":
                            current_params[add_to] += to_num(snt[index + 1][0])
                            if to_num(snt[index + 1][0]) % 1 != 0:
                                current_params[add_to] = roundCutOff(current_params[add_to])
                        else:
                            current_params[add_to] -= to_num(snt[index + 1][0])
                            if to_num(snt[index + 1][0]) % 1 != 0:
                                current_params[add_to] = roundCutOff(current_params[add_to])
                        skip_iter = True
                        continue

                if snt[index][0] == "through":
                    step = 1
                    start = 0
                    end = 0
                    if snt[index - 1][1] == "PARAMETER" and snt[index + 1][1] == "NUMBER":
                        start = to_num(snt[index - 1][0])
                        end = to_num(snt[index + 1][0])
                        if (index + 2 < len(snt) and snt[index + 2][0] == "by") and snt[index + 3][1] == "NUMBER":
                            step = to_num(snt[index + 3][0])
                        [current_params.append(autoConvert(param)[0][0]) for param in through_mod(start, end, step)]
                        modForwardParams = True

            if modForwardParams and snt[index][1] == "TYPE":
                c_type = snt[index][0]
                continue

            if modForwardParams and (snt[index][1] != "NUMBER" and snt[index][1] != "STRING" and snt[index][1] != "BOOLEAN"):
                modForwardParams = False

            if modForwardParams and (snt[index][1] == "NUMBER" or snt[index][1] == "STRING" or snt[index][1] == "BOOLEAN"):
                current_params.append(maybe_num(snt[index][0]))
                snt[index] = (snt[index][0], "PARAMETER")
                continue

    if c_type == "auto":
        params_auto = autoConvert(current_params)
        current_params = params_auto[0]
        c_type = params_auto[1]
    else:
        current_params = convertParams(current_params, c_type)

    if c_task != "":
        ordered_jobs.append(structure_output(task=c_task, structure=c_structure, params=current_params, paramtype=c_type))

    # Clean up loop, removes numbers/spaces that doesn't know how to deal with
    for index in range(len(snt) - 1, -1, -1):
        if snt[index][1] == "NUMBER" or snt[index][0] == "":
            snt.pop(index)

    return ordered_jobs
