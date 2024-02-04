# filename: use_bottle1.py
from bottle import route, run

@route('/')
def index():
    return "Hello Bottle!"

run(host='localhost', port=8080)