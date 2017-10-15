"""Includes the main library module."""
from freespeak import freespeak


def alloc_size_lea(paramlen, size="8", reg="rdi"):
    """LEA Opcode meant for quick size allocation to register."""
    return "lea " + reg + ", [" + str(paramlen) + " * " + size + "/"


def lea_op(*params, reg="rdi"):
    """Load Effective Address Opcode."""
    op_str = "lea " + reg + ", [" + str(params[0])
    for param in params:
        op_str += " + " + str(param)
    op_str += "]"
    return op_str


def nl_to_nasm(labeled):
    """NASM Assembly language pack for Freespeak NLP Engine."""
    nasmcode = ""
    externed = []

    for event in labeled:
        params = []
        task = []
        structure = []
        for action in event:
            if action[1] == "PARAMETER":
                params.append(int(action[0]))
            elif action[1] == "TASK":
                task.append(action[0])
            elif action[1] == "STRUCTURE":
                structure.append(action[0])

        for proc in range(0, len(task)):
            if task[proc] == "make":
                nasmcode += "extern malloc\nextern free\n"
                if structure[proc] == "array":
                    nasmcode += "lea rdi, [" + str(len(params)) + " * 8]\ncall malloc\n"
                    for val in range(0, len(params)):
                        nasmcode += "mov QWORD[rax + " + str(val) + " * 8], " + str(params[val]) + "\n"
                nasmcode += "mov rdi, rax\ncall free\n"
    nasmcode += "ret\n"
    return nasmcode
