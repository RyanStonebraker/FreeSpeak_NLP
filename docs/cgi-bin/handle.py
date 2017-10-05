#!/Users/Ryan/Documents/Programming/ML/Anaconda3/bin/python3
# -- USE THIS FOR UBUNTU MACHINES -- #!/usr/bin/env python3
# -*- coding: UTF-8 -*-# enable debugging
import cgi, cgitb
import sys
import os

currDIR = os.path.dirname(os.path.realpath(__file__))
freeDir = currDIR.replace("/docs/cgi-bin", "/backend")
sys.path.append(freeDir)
from freespeak import freespeak

cgitb.enable()

form = cgi.FieldStorage()

nlraw = ""

if 'nlcode' in form:
    nlraw = form.getvalue('nlcode').rstrip()

print("Content-Type: text/html;charset=utf-8\n")

with open("index.html", "r") as saveState:
    for line in saveState:
        print(line, sep="")

print("<textarea name=\"nlcode\" id  = \"sCde\" autofocus placeholder=\"Start Typing Here...\">", sep="")

print(nlraw, sep='')

print("</textarea><input type=\"submit\" name=\"intrnl\" value=\"Interpret\"></form> </section>")
print ("<footer><h3>Ryan Stonebraker &copy; 2017</h3></footer></body></html>")

if len(nlraw) > 0:
    print("<section class=\"output\"><h4>OUTPUT:</h4>")
    print(freespeak.identify(nlraw, debug = True))
    print ("</section>")
