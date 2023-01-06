from automata import Automata
from http import HTTPStatus
from .states import logged_out, logged_in

my_machine = Automata(
    name="myMachine",
)

@my_machine.create_endpoint('/health')
async def health_handler(request_headers):
    print(request_headers)
    return HTTPStatus.OK, [], b"OK\n"

my_machine.register_state(logged_out)
my_machine.register_state(logged_in)

def run_machine():
    my_machine.run('localhost', 8080)

