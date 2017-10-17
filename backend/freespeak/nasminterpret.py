"""Includes the main library module."""
from freespeak import freespeak
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


def mov_op(src, dest, stype=" "):
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


def instantiate_array(params, p_type):
    array_str = ""
    if p_type == "integer":
        p_size = 8
        array_str += alloc_size_lea(len(params))
        array_str += "call malloc\n"
        for count, param in enumerate(params):
            array_str += mov_bracket_op("rax", count * p_size, src=param)
        # array_str += mov_op("rax", sv)
    return array_str


def add_section(sect):
    return "<p style = \"text-align: left; margin-bottom: 0; margin-left: 10%;\">section ." + str(sect) + "</p>\n"


# TODO: go through task stack and perform assembly tasks, implement statements
# like "print this array.", "print the 2nd array.", etc. and "exclude 3,4,5 from 2nd array."
# (exclude is a task)
def nl_to_nasm(labeled):
    # return str(labeled)
    """NASM Assembly language pack for Freespeak NLP Engine."""
    nasmcode = ""
    loaded_externs = add_section("text")
    task_stack = []
    save_stack = []
    for sent in labeled:
        if len(labeled) > 0:
            for tsk in sent:
                task_stack.append(tsk)
    # return str(task_stack)

    for exectask in task_stack:
        # make == allocate space for some structure
        if exectask["TASK"] == "make":
            if "malloc" not in loaded_externs:
                loaded_externs += load_module("malloc")
            if "free" not in loaded_externs:
                loaded_externs += load_module("free")

            if exectask["STRUCTURE"] == "array":
                nasmcode += instantiate_array(exectask["PARAMETERS"], exectask["TYPE"])
                nasmcode += "push rax\n"
                save_stack.append(("pop rdi\ncall free\n", exectask["STRUCTURE"]))
    for pop_task in reversed(save_stack):
        nasmcode += pop_task[0]
    nasmcode += "ret\n"
    return loaded_externs + nasmcode
