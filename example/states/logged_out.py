import json
from automata import Automata, State, transition, transmit, EventStatus

logged_out = State('logged_out')

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

@logged_out.event('ping')
async def pong(automata: Automata, data):
    print('pong')
    await transmit(automata, EventStatus.OK, 'pong')