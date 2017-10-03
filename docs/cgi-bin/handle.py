#!/Users/Ryan/Documents/Programming/ML/Anaconda3/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
import cgi, cgitb
import sys
sys.path.append("/Users/Ryan/Documents/College-UAF/Classwork/Assembly/NLP_interpretted_NASM/FreeSpeak_NLP/backend")
from freespeak import freespeak


form = cgi.FieldStorage()
nlraw = form.getvalue('nlcode').rstrip('\n')

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

print(freespeak.handle(nlraw))

# print(nlraw.replace("\n", "</br>"))

if len(nlraw) > 0:
    print ("</section>")
