import unittest
from automata import Automata, State
from automata.utils.errors import DuplicateStateError, DuplicateEventError

test_automata = Automata(
    name="test"
)

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