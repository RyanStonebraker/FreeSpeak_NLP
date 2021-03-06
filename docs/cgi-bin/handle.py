#!/Users/Ryan/Documents/Programming/ML/Anaconda3/bin/python3
# -- USE THIS FOR UBUNTU MACHINES -- #!/usr/bin/env python3
# -*- coding: UTF-8 -*-# enable debugging
import cgi
import cgitb
import sys
import os

# adds location of freespeak library to path
currDIR = os.path.dirname(os.path.realpath(__file__))
freeDir = currDIR.replace("/docs/cgi-bin", "/backend")
sys.path.append(freeDir)
from freespeak import freespeak
from freespeak import nasminterpret

# FOR DEBUGGING *******************************************************
# cgitb.enable()

# gets all posted form data and stores it in a variable
form = cgi.FieldStorage()

nlraw = ""

# If form data includes the natural language input, store it in nlraw
if 'nlcode' in form:
    nlraw = form.getvalue('nlcode').rstrip()

# Required header to display an html page
print("Content-Type: text/html;charset=utf-8\n")

# recreates most of the initial webpage state up to the textarea
with open("index.html", "r") as saveState:
    for line in saveState:
        print(line, sep="")

# includes nlraw so input is saved between submits
print("""<textarea name="nlcode" id  = "sCde" autofocus placeholder="Start Typing Here...">
""" + nlraw + """</textarea>""")

print("""
<input type="submit" name="intrnl" value="Interpret"></form>
</section>
<footer><h3>Ryan Stonebraker &copy; 2017</h3></footer>
""")

# If anything was actually submitted, then print the interpretation section with
# the assembly code
if len(nlraw) > 0:
    identified_lang = freespeak.identify(nlraw)
    print("""<section class="output"><h4>NASM INTERPRETATION:</h4><div class="line-sep"></div>""")
    print("<p style = \"text-align: left;\">", nasminterpret.nl_to_nasm(identified_lang).replace("\n", "</br></br>").replace("~", "&nbsp;"), "</p>")
    print("</section></body></html>")
