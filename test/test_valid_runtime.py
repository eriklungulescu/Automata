import unittest
from unittest.mock import patch
from automata import Automata, State, transition, EventStatus

test_automata = Automata(
    name="test"
)

green_state = State(
    name="green",
    targets=["yellow"]
)

yellow_state = State(
    name="yellow",
    targets=["red"]
)

red_state = State(
    name="red",
    targets=["green"]
)

@green_state.event('go_yellow')
async def handler(automata: Automata, data):
    await transition(automata, 'yellow', EventStatus.OK)

@yellow_state.event('go_red')
async def some_handler(automata: Automata, data):
    await transition(automata, 'red', EventStatus.OK)

@red_state.event('go_green')
async def some_handler(automata: Automata, data):
    await transition(automata, 'green', EventStatus.OK)


class TestValidRuntime(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(self):
        test_automata.register_state(green_state)
        test_automata.register_state(yellow_state)
        test_automata.register_state(red_state)

    @patch('automata.automata._send_data_to_client')
    async def test_state_transition_internal(self, _):
        self.assertEqual(test_automata._current_state, green_state)
        await test_automata._current_state._events['go_yellow']._handler(test_automata, '')
        self.assertEqual(test_automata._current_state, yellow_state)
        await test_automata._current_state._events['go_red']._handler(test_automata, '')
        self.assertEqual(test_automata._current_state, red_state)
        await test_automata._current_state._events['go_green']._handler(test_automata, '')
        self.assertEqual(test_automata._current_state, green_state)

    @patch('automata.automata._send_data_to_client')
    async def test_machine_handler(self, _):
        self.assertEqual(test_automata._current_state, green_state)
        await test_automata.handler(' {"event": "go_yellow", "data": ""}')
        self.assertEqual(test_automata._current_state, yellow_state)
        await test_automata.handler(' {"event": "go_red", "data": ""}')
        self.assertEqual(test_automata._current_state, red_state)
        await test_automata.handler(' {"event": "go_green", "data": ""}')
        self.assertEqual(test_automata._current_state, green_state)
