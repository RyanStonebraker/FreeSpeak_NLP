"""Includes the main library module."""
from freespeak import freespeak
from freespeak import taskhandle
import math


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
        retstr += "\n"
        if row == 0 or row == rowheight - 1:
            retstr += "*" * colwidth
            continue
        if row == 1 or row == rowheight - 2:
            retstr += "*" + " " * (colwidth - 2) + "*"
            continue
        if len(paramstr) > 0:
            segmnt = paramstr[:colwidth - 4]
            retstr += "* " + segmnt + " " * (colwidth - len(segmnt) - 3) + "*"
            paramstr = paramstr[colwidth - 4:]
    return retstr


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


def mov_op(dest, src, stype=" "):
    if stype != " ":
        dest += " "
        stype += " "
    return "mov " + dest + "," + stype + src + "\n"


def mov_bracket_op(*dest, src, stype="QWORD"):
    mv_str = "mov " + stype + "[" + str(dest[0])
    for d_add in dest[1:]:
        mv_str += " + " + str(d_add)
    mv_str += "], " + str(src)
    return mv_str + "\n"


# def print_array(arr):
#     iarray_print
#     larray_print
#     farray_print


def instantiate_array(params, p_type, index=0):
    array_str = ""
    lbl = "arr_struct" + str(index)
    flag = "c_loc"
    if p_type == "integer":
        p_size = 8
        array_str += alloc_size_lea(len(params))
        array_str += "call malloc\n"
        for count, param in enumerate(params):
            array_str += mov_bracket_op("rax", count * p_size, src=param)
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
            if param == "True" or taskhandle.to_num(param) >= 1:
                swap_str = 1
            elif param == "False" or taskhandle.to_num(param) == 0:
                swap_str = 0
            array_str += mov_bracket_op("rax", count * p_size, src=swap_str)
    elif p_type == "string":
        flag = "end"
        array_str += lbl + ":\n"
        for param in params:
            array_str += "dq \"" + str(param) + "\"\n"
        array_str += "dq 0\n"
    return (array_str, flag, lbl)


def add_section(sect):
    return "<p style = \"text-align: left; margin-bottom: 0; margin-left: 10%;\">section ." + str(sect) + "</p>\n"


# TODO: go through task stack and perform assembly tasks, implement statements
# like "print this array.", "print the 2nd array.", etc. and "exclude 3,4,5 from 2nd array."
# (exclude is a task)
def nl_to_nasm(labeled):
    """NASM Assembly language pack for Freespeak NLP Engine."""
    nasmcode = ""
    loaded_externs = add_section("text")
    data_section = ""
    task_stack = []
    save_stack = []
    for sent in labeled:
        if len(labeled) > 0:
            for tsk in sent:
                task_stack.append(tsk)
    # return str(task_stack)

# TODO: Write a function that writes assembly that realloc (variant of malloc) an array
# to store pointers to data structures so I can call functions

    for index, exectask in enumerate(task_stack):
        # make == allocate space for some structure
        if exectask["TASK"] == "make":
            if exectask["STRUCTURE"] == "array":
                auto_arr = instantiate_array(exectask["PARAMETERS"], exectask["TYPE"], index)
                if auto_arr[1] == "c_loc":
                    if "malloc" not in loaded_externs:
                        loaded_externs += load_module("malloc")
                    if "free" not in loaded_externs:
                        loaded_externs += load_module("free")
                    nasmcode += auto_arr[0]
                    nasmcode += "push rax\n"
                    save_stack.append(("pop rdi\ncall free\n", exectask["STRUCTURE"]))
                elif auto_arr[1] == "end":
                    if len(data_section) == 0:
                        data_section += add_section("data")
                    data_section += auto_arr[0]

    for pop_task in reversed(save_stack):
        nasmcode += pop_task[0]
    nasmcode += "ret\n"
    return loaded_externs + nasmcode + data_section
