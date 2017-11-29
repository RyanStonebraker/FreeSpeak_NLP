# views.py

from flask import render_template
from flask import request
from flask import redirect
from app import app

import sys
import os
currDIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currDIR + "/freespeak/")

import freespeak
import nasminterpret


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/interpret", methods=['GET', 'POST'])
def interpret():
    if request.method == "GET":
        return render_template("interpret.html")
    elif request.method == "POST":
        natural_lang = request.form.get("nlcode")
        if not natural_lang:
            return render_template("index.html")
        identified_lang = freespeak.identify(natural_lang)
        identified_lang = nasminterpret.nl_to_nasm(identified_lang).split("\n")
        return render_template("interpret.html", content=identified_lang, raw_text=natural_lang)
