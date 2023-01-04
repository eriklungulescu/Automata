import unittest
from automata import Automata, State

test_automata = Automata(
    name="test"
)

initial_state = State(
    name="initial"
)

@initial_state.event('test_event1')
def handler(automata: Automata, data):
    pass

@initial_state.event('test_event2')
def some_handler(automata: Automata, data):
    pass

secondary_state = State(
    name="secondary"
)

tertiary_state = State(
    name="tertiary"
)

class TestValidAutomataSetup(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        test_automata.register_state(initial_state)
        test_automata.register_state(secondary_state)
        test_automata.register_state(tertiary_state)

    def test_check_initial_state(self):
        self.assertEqual(test_automata._current_state, initial_state, f"{initial_state.name} should be the initial state instead of {test_automata._current_state.name}...")

    def test_check_all_states(self):
        states = [initial_state, secondary_state, tertiary_state]
        for state in states:
            self.assertIn(state, test_automata._states.values(), f"{state.name} should exist in our list of states...")

        for state_name in test_automata._states.keys():
            self.assertEqual(state_name, test_automata._states[state_name].name, f"{state_name} should map to the appropriate state...")
    
    def test_check_state_events(self):
        self.assertIn("test_event1", initial_state._events.keys(), "test_event1 is not present in initial_state events")
        self.assertIn("test_event2", initial_state._events.keys(), "test_event1 is not present in initial_state events")