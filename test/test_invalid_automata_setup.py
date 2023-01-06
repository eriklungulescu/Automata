import unittest
from automata import Automata, State
from automata.utils.errors import DuplicateStateError, DuplicateEventError, DuplicateEndpointError

test_automata = Automata(
    name="test"
)

@test_automata.create_endpoint('/health')
async def some_handler(request_header):
    return 'OK'

initial_state = State(
    name="initial"
)

@initial_state.event('test_event1')
def handler(automata: Automata, data):
    pass

class TestValidAutomataSetup(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        test_automata.register_state(initial_state)

    def test_add_duplicate_state_should_throw_exception(self):
        with self.assertRaises(DuplicateStateError):
            test_automata.register_state(initial_state)

    def test_add_duplicate_event_should_throw_exception(self):
        with self.assertRaises(DuplicateEventError):
            @initial_state.event('test_event1')
            def handler(automata: Automata, data):
                pass

    def test_create_duplicate_http_endpoint_should_throw_exception(self):
        with self.assertRaises(DuplicateEndpointError):
            @test_automata.create_endpoint('/health')
            async def some_duplicate_handler(request_header):
                return 'OK'
