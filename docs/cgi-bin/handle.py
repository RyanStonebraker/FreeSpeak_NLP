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

if len(nlraw) > 0:
    identified_lang = freespeak.identify(nlraw)
    print("""<section class="output"><h4>NASM INTERPRETATION:</h4><div class="line-sep"></div>""")
    print("<p style = \"text-align: left;\">", nasminterpret.nl_to_nasm(identified_lang).replace("\n", "</br></br>").replace("~", "&nbsp;"), "</p>")
    print("</section></body></html>")
