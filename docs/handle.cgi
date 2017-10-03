#!/usr/bin/python
import cgi
import cgitb
form = cgi.FieldStorage()

nlRaw = form.getvalue('nlcode')
print nlcode
