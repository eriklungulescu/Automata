from automata import Automata
from .states import logged_out, logged_in

my_machine = Automata(
    name="myMachine",
)

my_machine.register_state(logged_out)
my_machine.register_state(logged_in)

def run_machine():
    my_machine.run('localhost', 8080, '/session')

