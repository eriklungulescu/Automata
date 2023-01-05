import unittest
from unittest.mock import patch
from automata import Automata, State, transition, EventStatus
from automata.utils.errors import InvalidPayload, InvalidEvent, InvalidStateTransition

class RandomException(Exception):
    pass

test_automata = Automata(
    name="test"
)

initial_state = State(
    name="initial",
    targets=["secondary"]
)

secondary_state = State(
    name="secondary"
)

tertiary_state = State(
    name="tertiary"
)

@initial_state.event('test_event')
def handler(automata: Automata, data):
    pass

@initial_state.event('cause_random_exception')
def cause_error(automata: Automata, data):
    raise RandomException

@initial_state.event('cause_illegal_state_transition')
async def cause_error(automata: Automata, data):
    await transition(automata, 'tertiary', EventStatus.OK)

class TestInvalidRuntime(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(self):
        test_automata.register_state(initial_state)
        test_automata.register_state(secondary_state)
        test_automata.register_state(tertiary_state)


    @patch('automata.automata._send_data_to_client')
    async def test_invalid_payloads(self, _):
        with self.assertRaises(InvalidPayload):
            await test_automata.handler('{"event":"wrong_event", "daat": "some data"}')
        with self.assertRaises(InvalidPayload):
            await test_automata.handler('{"eve":"wrong_event", "data": null}')
        with self.assertRaises(InvalidPayload):
            await test_automata.handler('{"eev":"wrong_event", "daat": null}')
        with self.assertRaises(InvalidPayload):
            await test_automata.handler('{"event":"wrong_event", "daat": null}')
        with self.assertRaises(InvalidPayload):
            await test_automata.handler('{"event":"wrong_event", "data": null, "something":"not allowed"}')

    @patch('automata.automata._send_data_to_client')
    async def test_invalid_events(self, _):
        with self.assertRaises(InvalidEvent):
            await test_automata.handler('{"event":"wrong_event", "data": "some data"}')
        with self.assertRaises(InvalidEvent):
            await test_automata.handler('{"event":"test-event", "data": "some data"}')

    @patch('automata.automata._send_data_to_client')
    async def test_exception_order(self, _):
        with self.assertRaises(InvalidPayload):
            await test_automata.handler('{"eent":"cause_random_exception", "data": "some data"}')
        with self.assertRaises(InvalidEvent):
            await test_automata.handler('{"event":"cause-random_exception", "data": "some data"}')
        with self.assertRaises(RandomException):
            await test_automata.handler('{"event":"cause_random_exception", "data": "some data"}')
        with self.assertRaises(InvalidStateTransition):
            await test_automata.handler('{"event":"cause_illegal_state_transition", "data": "some data"}')