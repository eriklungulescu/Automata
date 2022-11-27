from flask import Blueprint
from flask_sock import Sock

session = Blueprint('session', __name__, url_prefix='/session')
sock = Sock(session)

@session.route('/join')
def join():
    return "Websocket blueprint!"

@sock.route('echo')
def echo(ws):
    while True:
        data = ws.receive()
        ws.send(data)