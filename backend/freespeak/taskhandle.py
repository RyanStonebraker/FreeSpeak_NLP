import numpy
import collections
# import pdb


def structure_output(task="make", structure="array", params=[]):
    return {"TASK": task, "STRUCTURE": structure, "PARAMETERS": params}


def to_num(strNum):
    try:
        return int(strNum)
    except:
        try:
            return float(strNum)
        except:
            raise ValueError("to_num parameter not a number!")


def maybe_num(param):
    try:
        return to_num(param)
    except:
        return param


def through_mod(begin, end, inc=1):
    return [maybe_num(('%f' % num).rstrip('0').rstrip('.')) for num in numpy.arange(begin + inc, end, inc)]


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


def convertParams(params, ctype):
    new_params = []
    for param in params:
        new_params.append(convertParam(param, ctype))
    return new_params


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
    return convertParams(params, auto_type)


def getcontext(snt_raw):
    # print(snt_raw)
    snt = [wrd for wrd in snt_raw if wrd[0] != '' and wrd[1] != "SUPERFLUOUS"]
    print(snt)

    ordered_jobs = []
    current_params = []
    start_find = False
    modForwardParams = False
    c_task = ""
    c_structure = ""
    c_type = "auto"
    for index, word in enumerate(snt):
        if snt[index][1] == "TASK" and start_find:
            if c_type == "auto":
                current_params = autoConvert(current_params)
            else:
                current_params = convertParams(current_params, c_type)
            ordered_jobs.append(structure_output(task=c_task, structure=c_structure, params=current_params))
            current_params = []
            c_task = snt[index][0]
            c_structure = ""
            c_type = "auto"
            modForwardParams = False
            continue

        if snt[index][1] == "TASK" and not start_find:
            start_find = True
            c_task = snt[index][0]
            continue

        if start_find:
            if snt[index][1] == "STRUCTURE":
                c_structure = snt[index][0]
                continue

            # MODIFIER SUBROUTINES
            if snt[index][1] == "MODIFIER":
                if snt[index][0] == "with" or snt[index][0] == "include":
                    modForwardParams = True
                    continue

                if snt[index][0] == "through":
                    step = 1
                    start = 0
                    end = 0
                    if snt[index - 1][1] == "PARAMETER" and snt[index + 1][1] == "NUMBER":
                        start = to_num(snt[index - 1][0])
                        end = to_num(snt[index + 1][0])
                        if (snt[index + 2][0] == "by") and snt[index + 3][1] == "NUMBER":
                            step = to_num(snt[index + 3][0])
                        [current_params.append(autoConvert(param)[0]) for param in through_mod(start, end, step)]
                        modForwardParams = True

            if modForwardParams and snt[index][1] == "TYPE":
                c_type = snt[index][0]
                continue

            if modForwardParams and snt[index][1] != "NUMBER":
                modForwardParams = False

            if modForwardParams and snt[index][1] == "NUMBER":
                current_params.append(to_num(snt[index][0]))
                snt[index] = (snt[index][0], "PARAMETER")
                continue

    print (c_type)
    if c_type == "auto":
        current_params = autoConvert(current_params)
    else:
        current_params = convertParams(current_params, c_type)

    ordered_jobs.append(structure_output(task=c_task, structure=c_structure, params=current_params))

    # Clean up loop, removes numbers/spaces that doesn't know how to deal with
    for index in range(len(snt) - 1, -1, -1):
        if snt[index][1] == "NUMBER" or snt[index][0] == "":
            snt.pop(index)

    return ordered_jobs
