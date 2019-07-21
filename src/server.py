from flask import Flask
import time, re

variables = {}
app = Flask(__name__)


def get_time():
    return int(time.time() * 1000)


def match(str1, str2):
    regex = re.compile(str1.replace("*", ".+"))
    return re.match(regex, str2)


@app.route("/")
def _index():
    return "Hello, world!"


@app.route("/set/<name>/<value>/<int:timeout>")
def _set(name, value, timeout):
    """
    name - variable name
    value - variable value
    timeout - after this amount of milliseconds the variable shall disappear!
    """
    global variables

    variables[name] = {
        "value": value,
        "timeout": get_time() + timeout
    }
    
    return "ok"


@app.route("/get/<name>")
def _get(name):
    global variables
    
    if name not in variables.keys():
        return "not found"

    if variables[name]["timeout"] <= get_time():
        del variables[name]
        return "not found"

    return variables[name]["value"]

@app.route("/query/<name>")
def _query(name):
    global variables

    result = []
    for i in (f for f in variables if match(name, f)):
        result.append(i + " " + variables[i]["value"])

    return "\n".join(result)

app.run(port=8080)
