from automata import Automata, State, transition

logged_in = State('logged_in')

@logged_in.event('log_out')
async def handler(automata: Automata, data: str):
    print(data)
    await transition(automata, 'logged_out')