import json
from automata import Automata, State, transition, transmit, EventStatus

logged_out = State('logged_out')

class UserInfo(object):
    def __init__(self, token: str):
        self.token = token
class Outer(object):
    def __init__(self, test, userInfo: UserInfo):
        self.test = test
        self.user = userInfo


@logged_out.event('log_in')
async def handler(automata: Automata, data):
    print(data['test'])
    await transition(automata, 'logged_in', EventStatus.OK, "some data")