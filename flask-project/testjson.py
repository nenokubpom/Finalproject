import os
import connectjson
from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    x= connectjson.show()
    z=""
    for i in x:
        if i["Band"] == "BLACKPINK":
            z = i["Band"]
            return z
    return z