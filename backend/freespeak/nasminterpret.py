from freespeak import freespeak

def nl_to_nasm(nltext):
    nasmcode = ""
    labeled = freespeak.identify(nltext)

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

        for proc in range(0,len(task)):
            if task[proc] == "make":
                nasmcode += "extern malloc\nextern free\n"
                if structure[proc] == "array":
                    nasmcode += "lea rdi, [" + str(len(params)) + " * 8]\ncall malloc\n"
                    for val in range(0,len(params)):
                        nasmcode += "mov QWORD[rax + " + str(val) + " * 8], " + str(params[val]) + "\n"
                nasmcode += "mov rdi, rax\ncall free\n"
    nasmcode += "ret\n"
    return nasmcode
