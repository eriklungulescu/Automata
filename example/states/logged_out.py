from automata import Automata, State, transition, transmit

logged_out = State('logged_out')

class userInfo:
    def __init__(self, token):
        self.token = token

@logged_out.event('log_in')
async def handler(automata: Automata, data: str):
    await transition(automata, 'logged_in')
    u = userInfo('oi21jeoi21e897dasdu09q2')
    await transmit(automata, u)
