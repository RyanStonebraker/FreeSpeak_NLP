"""Includes the main library module."""
import freespeak
import taskhandle
import math
import ast
import random

# Made this a function just in case the structure externs are stored changes
# in the future
def load_module(modul):
    return "extern " + str(modul) + "\n"


# Defines the structure type "box"
def make_box(params):
    retstr = ""
    paramstr = str(params[0])
    colwidth = 70
    rowheight = 5
    for param in params[1:]:
        paramstr += " " + str(param)
    if len(paramstr) + 4 < colwidth:
        colwidth = len(paramstr) + 4
    if math.ceil(len(paramstr) / colwidth) + 4 > rowheight:
        rowheight = math.ceil(len(paramstr) / colwidth) + 4
    for row in range(0, rowheight):
        retstr += "\\n"
        if row == 0 or row == rowheight - 1:
            retstr += "*" * colwidth
            continue
        if row == 1 or row == rowheight - 2:
            retstr += "*" + "~" * (colwidth - 2) + "*"
            continue
        if len(paramstr) > 0:
            segmnt = paramstr[:colwidth - 4]
            retstr += "* " + segmnt + "~" * (colwidth - len(segmnt) - 3) + "*"
            paramstr = paramstr[colwidth - 4:]
    return retstr + "\\n"


def alloc_size_lea(paramlen, size="8", reg="rdi"):
    """LEA Opcode meant for quick size allocation to register."""
    return "lea " + reg + ", [" + str(paramlen) + " * " + size + "]\n"


def lea_op(*params, reg="rdi", stype="QWORD"):
    """Load Effective Address Opcode."""
    op_str = "lea " + reg + ", " + stype + "[" + str(params[0])
    for param in params[1:]:
        op_str += " + " + str(param)
    op_str += "]"
    return op_str + "\n"


# mov opcode
def mov_op(dest, src, stype=" "):
    if stype != " ":
        dest += " "
        stype += " "
    return "mov " + dest + "," + stype + src + "\n"


# specialized mov opcode that formats with brackets and a type
def mov_bracket_op(*dest, src, stype="QWORD"):
    mv_str = "mov " + stype + "[" + str(dest[0])
    for d_add in dest[1:]:
        mv_str += " + " + str(d_add)
    mv_str += "], " + str(src)
    return mv_str + "\n"


# handles arrays of any type and utilizes open registers if needed or malloc
# in the case of integer arrays
def instantiate_array(params, p_type, open_registers, index=0):
    total_registers = ["rax", "rdi", "rcx", "rdx", "r15", "r14", "r13", "r12", "r11", "r10", "r9", "r8"]
    busy_registers = []
    for reg in total_registers:
        if reg not in open_registers:
            busy_registers.append(reg)
    array_str = ""
    loc = "label"
    lbl = "arr_struct" + str(index)
    flag = "c_loc"
    if p_type == "integer":
        p_size = 8
        for reg in busy_registers:
            array_str += "push " + reg + "\n"
        array_str += alloc_size_lea(len(params))
        array_str += "call malloc\n"
        for reg in reversed(busy_registers):
            array_str += "pop " + reg + "\n"
        for count, param in enumerate(params):
            array_str += mov_bracket_op("rax", count * p_size, src=param)
        loc = "register"
        lbl = open_registers[len(open_registers) - 1]
        array_str += mov_op(lbl, "rax")
        del open_registers[len(open_registers) - 1]
    elif p_type == "float":
        flag = "end"
        array_str += lbl + ":\n"
        array_str += "dd " + str(params[0])
        for param in params[1:]:
            array_str += ", " + str(param)
        array_str += "\n"
    elif p_type == "boolean":
        p_size = 1
        swap_str = 0
        array_str += alloc_size_lea(len(params))
        array_str += "call malloc\n"
        for count, param in enumerate(params):
            if param == "True" or taskhandle.to_num(param) >= 1 or taskhandle.to_num(param) < 0:
                swap_str = 1
            elif param == "False" or taskhandle.to_num(param) == 0:
                swap_str = 0
            array_str += mov_bracket_op("rax", count * p_size, src=swap_str)
        loc = "register"
        lbl = open_registers[len(open_registers) - 1]
        array_str += mov_op(lbl, "rax")
    elif p_type == "string":
        flag = "end"
        array_str += lbl + ":\n"
        for param in params:
            for index in range(0, math.ceil(len(param) / 40)-1):
                array_str += "db `" + str(param)[:40] + "`\n"
                param = param[40:]
            array_str += "db `" + str(param)[:40] + "`, 0\n"

    return (array_str, flag, [loc, lbl, "array", p_type], open_registers)


# Used to more easily identify x86 sections
def add_section(sect):
    return "section ." + str(sect) + "\n"


# Takes the simplified commands and converts to x86
def nl_to_nasm(labeled):
    """x86 Assembly language pack for Freespeak NLP Engine."""
    nasmcode = ""
    loaded_externs = add_section("text")
    data_section = ""
    deconstruct = ""
    task_stack = []
    save_stack = []
    variables = {}

    # (register|label, name)
    storage_history = []
    open_registers = ["rax", "rdi", "rcx", "rdx", "r15", "r14", "r13", "r12", "r11", "r10", "r9", "r8"]

    for idx, sent in enumerate(labeled):
        if len(labeled) > 0:
            for tsk in sent:
                task_stack.append((tsk, idx))

    for index, exectask in enumerate(task_stack):
        # Store what sentence the task is in
        tsk_snt = exectask[1]
        exectask = exectask[0]
        # make == allocate space for some structure
        if exectask["TASK"] == "make":
            if exectask["STRUCTURE"] == "array":
                auto_arr = instantiate_array(exectask["PARAMETERS"], exectask["TYPE"], open_registers, index)
                if auto_arr[1] == "c_loc":
                    if "malloc" not in loaded_externs:
                        loaded_externs += load_module("malloc")
                    if "free" not in loaded_externs:
                        loaded_externs += load_module("free")
                    nasmcode += auto_arr[0]
                elif auto_arr[1] == "end":
                    if len(data_section) == 0:
                        data_section += add_section("data")
                    data_section += auto_arr[0]
                storage_history.append(auto_arr[2])

            elif exectask["STRUCTURE"] == "box":
                local_params = exectask["PARAMETERS"]
                if len(exectask["PARAMETERS"]) < 1:
                    continue
                if len(exectask["PARAMETERS"]) >= 1 and "VARIABLE" in exectask["PARAMETERS"][0]:
                    vr_assign = ast.literal_eval(exectask["PARAMETERS"][0])
                    local_params = variables[str(vr_assign[1])]

                auto_arr = instantiate_array([make_box(local_params)], "string", open_registers, index)
                if auto_arr[1] == "c_loc":
                    if "malloc" not in loaded_externs:
                        loaded_externs += load_module("malloc")
                    if "free" not in loaded_externs:
                        loaded_externs += load_module("free")
                    nasmcode += auto_arr[0]
                elif auto_arr[1] == "end":
                    if len(data_section) == 0:
                        data_section += add_section("data")
                    data_section += auto_arr[0]
                storage_history.append([auto_arr[2][0], auto_arr[2][1], "box", "string"])

        elif exectask["TASK"] == "print":
            if load_module("printf") not in loaded_externs:
                loaded_externs += load_module("printf")
            source = []
            p_count = 1
            p_struct = exectask["STRUCTURE"]
            try:
                sourceNum = taskhandle.to_num(exectask["PARAMETERS"][0])
            except:
                sourceNum = 0
            if str(p_struct) == "this":
                source = storage_history[len(storage_history) - 1]
            else:
                for struct_info in storage_history:
                    if sourceNum == p_count and str(struct_info[2]) == str(p_struct):
                        source = struct_info
                    p_count += 1

            if len(source) > 3 and source[3] == "string":
                nmlbl = str(p_struct) + str(p_count) + str(index) + "str"
                data_section += nmlbl + ":\n"
                data_section += "db '%s', 0\n"
                nasmcode += "push rdi\npush rsi\n"
                nasmcode += "mov rdi, " + nmlbl + "\n"
                nasmcode += "mov rsi, " + source[1] + "\n"
                nasmcode += "mov al, 0\n"
                for store in storage_history:
                    if store[0] == "register":
                        nasmcode += "push " + store[1] + "\n"
                nasmcode += "call printf\n"
                for store in reversed(storage_history):
                    if store[0] == "register":
                        nasmcode += "pop " + store[1] + "\n"
                nasmcode += "pop rsi\npop rdi\n"

        elif exectask["TASK"] == "show":
            if exectask["STRUCTURE"] == "deconstruction":
                deconstruct = """<h4>DECONSTRUCTION:</h4><div class="line-sep"></div>""" + str(task_stack)

        elif exectask["TASK"] == "repeat":
            try:
                repeat_amount = taskhandle.to_num(exectask["PARAMETERS"][0])
            except:
                repeat_amount = 1
            if exectask["STRUCTURE"] == "this":
                for i in range(1, repeat_amount + 1):
                    for prev_task in labeled[tsk_snt - 1]:
                        if prev_task != '':
                            task_stack.insert(index + 1, (prev_task, tsk_snt))
                del task_stack[index]

        elif exectask["TASK"] == "store":
            try:
                exectask["PARAMETERS"][0] = ast.literal_eval(exectask["PARAMETERS"][0])
            except:
                exectask["PARAMETERS"][0] = exectask["PARAMETERS"][0]
            if len(exectask["PARAMETERS"]) >= 2 and exectask["PARAMETERS"][0][0] == "VARIABLE":
                # Store a key-value pair of variable and contents in "variables"
                variables[exectask["PARAMETERS"][0][1]] = exectask["PARAMETERS"][1:]
                for idx, value in enumerate(variables[exectask["PARAMETERS"][0][1]]):
                    if "VARIABLE" in value:
                        replace_var = ast.literal_eval(value)[1]
                        variables[exectask["PARAMETERS"][0][1]][idx] = variables[replace_var][0]

        elif exectask["TASK"] == "add":
            if "VARIABLE" in exectask["PARAMETERS"][1]:
                var_str = ast.literal_eval(exectask["PARAMETERS"][1])[1]
                try:
                    variables[var_str] = str(int(variables[var_str][0]) + int(exectask["PARAMETERS"][0]))
                except:
                    variables[var_str] = str(variables[var_str][0]) + str(exectask["PARAMETERS"][0])
        elif exectask["TASK"] == "subtract":
            if "VARIABLE" in exectask["PARAMETERS"][1]:
                var_str = ast.literal_eval(exectask["PARAMETERS"][1])[1]
                try:
                    variables[var_str] = str(int(variables[var_str][0]) - int(exectask["PARAMETERS"][0]))
                except:
                    variables[var_str] = str(variables[var_str][0]) + str(exectask["PARAMETERS"][0])

    for index, dealloc in enumerate(reversed(storage_history)):
        if dealloc[0] == "register":
            if index < len(storage_history) - 1:
                for store in storage_history:
                    if store[0] == "register":
                        nasmcode += "push " + store[1] + "\n"
                nasmcode += "mov rdi, " + str(dealloc[1]) + "\n"
                nasmcode += "call free\n"
                for store in reversed(storage_history):
                    if store[0] == "register":
                        nasmcode += "pop " + store[1] + "\n"
                storage_history.pop(len(storage_history) - 1 - index)
            else:
                nasmcode += "mov rdi, " + str(dealloc[1]) + "\n"
                nasmcode += "call free\n"

    for pop_task in reversed(save_stack):
        nasmcode += pop_task[0]
    nasmcode += "ret\n"

    return (str(task_stack), loaded_externs + nasmcode + data_section + "\n" + deconstruct)
