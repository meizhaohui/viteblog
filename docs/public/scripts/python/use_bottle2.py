# filename: use_bottle2.py
from bottle import route, run, static_file

@route('/')
def index():
    return static_file('use_bottle2_index.html', root='.')

run(host='localhost', port=8080)