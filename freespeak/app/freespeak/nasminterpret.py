"""Includes the main library module."""
import freespeak
import taskhandle
import math


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


# Takes advantage of the fact that python is simply injecting text that is
# later interpreted as HTML. Also is used to more easily identify NASM sections
def add_section(sect):
    return "section ." + str(sect) + "\n"


# Takes the simplified commands and converts to NASM
def nl_to_nasm(labeled):
    """NASM Assembly language pack for Freespeak NLP Engine."""
    nasmcode = ""
    loaded_externs = add_section("text")
    data_section = ""
    deconstruct = ""
    task_stack = []
    save_stack = []

    # (register|label, name)
    storage_history = []
    open_registers = ["rax", "rdi", "rcx", "rdx", "r15", "r14", "r13", "r12", "r11", "r10", "r9", "r8"]

    for sent in labeled:
        if len(labeled) > 0:
            for tsk in sent:
                task_stack.append(tsk)

    # loaded_externs = str(task_stack) + "\n" + loaded_externs # DEBUG

    for index, exectask in enumerate(task_stack):

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
                if len(exectask["PARAMETERS"]) < 1:
                    exectask["PARAMETERS"].append("test")
                auto_arr = instantiate_array([make_box(exectask["PARAMETERS"])], "string", open_registers, index)
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
                for i in range(0, repeat_amount):
                    task_stack.insert(index + 1, task_stack[index - 1])

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

    return (str(task_stack) + "\n" + str(labeled),loaded_externs + nasmcode + data_section + "\n" + deconstruct)
