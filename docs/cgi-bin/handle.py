#!/Users/Ryan/Documents/Programming/ML/Anaconda3/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
import cgi, cgitb
# import os
form = cgi.FieldStorage()
nlraw = form.getvalue('nlcode')

print("Content-Type: text/html;charset=utf-8\n")

with open("index.html", "r") as saveState:
    for line in saveState:
        print(line)

print ("<footer><h3>Ryan Stonebraker &copy; 2017</h3></footer></body></html>")

if len(nlraw) > 0:
    print("<section class=\"output\"><h4>OUTPUT:</h4>")

print(nlraw.replace("\n", "</br>"))

if len(nlraw) > 0:
    print ("</section>")
