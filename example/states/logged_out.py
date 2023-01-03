import json
from automata import Automata, State, transition, transmit, EventStatus

logged_out = State('logged_out')

class UserInfo(object):
    def __init__(self, token: str):
        self.token = token
class Outer(object):
    def __init__(self, test, user: str):
        self.test = test
        self.user = user


@logged_out.event('log_in')
async def handler(automata: Automata, data):
    print(data)
    send = {
        'test': 'test',
        'test2': {
            'inner': 'value',
            'list': [1,2,3]
        },
        'test3': 5
    }
    await transition(automata, 'logged_in', EventStatus.OK, send)