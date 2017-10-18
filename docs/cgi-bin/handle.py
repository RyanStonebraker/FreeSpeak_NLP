#!/Users/Ryan/Documents/Programming/ML/Anaconda3/bin/python3
# -- USE THIS FOR UBUNTU MACHINES -- #!/usr/bin/env python3
# -*- coding: UTF-8 -*-# enable debugging
import cgi
import cgitb
import sys
import os

currDIR = os.path.dirname(os.path.realpath(__file__))
freeDir = currDIR.replace("/docs/cgi-bin", "/backend")
sys.path.append(freeDir)
from freespeak import freespeak
from freespeak import nasminterpret

# TURN OFF FOR FINAL *******************************************************
# cgitb.enable()

form = cgi.FieldStorage()

nlraw = ""

if 'nlcode' in form:
    nlraw = form.getvalue('nlcode').rstrip()

print("Content-Type: text/html;charset=utf-8\n")

with open("index.html", "r") as saveState:
    for line in saveState:
        print(line, sep="")

print("""<textarea name="nlcode" id  = "sCde" autofocus placeholder="Start Typing Here...">
""" + nlraw + """</textarea>""")

print("""
<input type="submit" name="intrnl" value="Interpret"></form>
</section>
<footer><h3>Ryan Stonebraker &copy; 2017</h3></footer>
""")

# deconstruct = False

if len(nlraw) > 0:
    identified_lang = freespeak.identify(nlraw)
    print("""<section class="output"><h4>NASM INTERPRETATION:</h4><div class="line-sep"></div>""")
    print("<p style = \"text-align: left;\">", nasminterpret.nl_to_nasm(identified_lang).replace("\n", "</br></br>").replace("~", "&nbsp;"), "</p>")
    # if deconstruct:
        # print("""<h4>DECONSTRUCTION:</h4><div class="line-sep"></div>""")
        # task_str = """<div class = "line-sep" style = "margin-bottom: 0;"></div>"""
        # struct_str = """<div class = "line-sep" style = "margin-bottom: 0;"></div>"""
        # mod_str = """<div class = "line-sep" style = "margin-bottom: 0;"></div>"""
        # sup_str = """<div class = "line-sep" style = "margin-bottom: 0;"></div>"""
        # type_str = """<div class = "line-sep" style = "margin-bottom: 0;"></div>"""
        # param_str = """<div class = "line-sep" style = "margin-bottom: 0;"></div>"""
        #
        # for count, sent in enumerate(identified_lang):
        #     task_out = [category for category in sent if category[1] == "TASK"]
        #     for task_raw in task_out:
        #         task_str += str(task_raw[0]) + " : #" + str(count+1) + "</br>"
        #     struct_out = [category for category in sent if category[1] == "STRUCTURE"]
        #     for struct_raw in struct_out:
        #         struct_str += str(struct_raw[0]) + " : #" + str(count+1) + "</br>"
        #     mod_out = [category for category in sent if category[1] == "MODIFIER"]
        #     for mod_raw in mod_out:
        #         mod_str += str(mod_raw[0]) + " : #" + str(count+1) + "</br>"
        #     sup_out = [category for category in sent if category[1] == "SUPERFLUOUS"]
        #     for sup_raw in sup_out:
        #         sup_str += str(sup_raw[0]) + " : #" + str(count+1) + "</br>"
        #     type_out = [category for category in sent if category[1] == "TYPE"]
        #     for type_raw in type_out:
        #         type_str += str(type_raw[0]) + " : #" + str(count+1) + "</br>"
        #     param_out = [category for category in sent if category[1] == "PARAMETER"]
        #     for param_raw in param_out:
        #         param_str += str(param_raw[0]) + " : #" + str(count+1) + "</br>"
        #
        # print("""
        #   <span style = "float: left; text-align: center; width: 16.66%;">TASK:</br>""" + str(task_str) + """</span>
        #   <span style = "float: left; text-align: center; width: 16.66%;">STRUCTURE:</br>""" + str(struct_str) + """</span>
        #   <span style = "float: left; text-align: center; width: 16.66%;">MODIFIER:</br>""" + str(mod_str) + """</span>
        #   <span style = "float: right; text-align: center; width: 16.66%;">SUPERFLUOUS:</br>""" + str(sup_str) + """</span>
        #   <span style = "float: right; text-align: center; width: 16.66%;">TYPE:""" + str(type_str) + """</span>
        #   <span style = "float: right; text-align: center; width: 16.66%;">PARAMETERS:</br>""" + str(param_str) + """</span>
        #   <div style = "clear: both;"></div>
        #       """)
    print("</section></body></html>")
