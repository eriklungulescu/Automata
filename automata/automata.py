from collections.abc import Callable
from typing import Generic, Mapping, TypeVar
from types import SimpleNamespace
from automata.utils.payloads import RequestEventPayload, StateChangePayload
import json
import asyncio
import websockets
import inspect

class Automata:
    pass

T = TypeVar("T")
class Event(Generic[T]):
    def __init__(self, name: str, handler: Callable[[Automata, T], None]):
        self.name = name
        self._handler = handler

    async def _processAndHandle(self, automata: Automata, event: str):
        if inspect.iscoroutinefunction(self._handler):
            await self._handler(automata, event)
        else:
            self._handler(automata, event)

class State:
    def __init__(self, name: str,  targets: list[str] = None, events: list[Event] = []):
        self.name = name
        self._events: Mapping[str, Event] = {}
        for event in events:
            self._events[event.name] = event
        self._targets = targets

class Automata:
    def __init__(self, initial: str, states: list[State]):
        self._currentState = initial
        self._states: Mapping[str, State] = {}
        for state in states:
            self._states[state.name] = state

    async def _handler(self, eventName: str, data: str = None):
        if eventName not in self._states[self._currentState]._events.keys():
            raise "Invalid event " + eventName + " called on current state " + self._currentState
        else:
            await self._states[self._currentState]._events[eventName]._processAndHandle(self, data)

    # Websocket Functions
    def serve(self, uri: str, port: int, path):
        print(f'Running websocket client on: {uri}:{port}{path}')
        self.path = path
        async def serveServer():
            async with websockets.serve(self._receiveRequests, uri, port):
                await asyncio.Future() # Runs forever
        asyncio.run(serveServer())
        

    async def _receiveRequests(self, websocket, path):
        if (path != self.path):
            print(f"Request at {path} doesn't match defined path {self.path}")
            return

        self.websocket = websocket
        async for message in self.websocket:
            data: RequestEventPayload  = json.loads(message, object_hook=lambda d: SimpleNamespace(**d))
            print(data)
            await self._handler(data.event, data.data)
    
    async def _send(self, data: str):
        await self.websocket.send(data)



# Library Functions

# Will transition to a new state
async def transition(automata: Automata, nextState: str):
    if automata._states[automata._currentState]._targets == None or nextState in automata._states[automata._currentState]._targets:
        automata._currentState = nextState
        payload = StateChangePayload(automata._currentState, list(automata._states[automata._currentState]._events.keys()))
        await transmitJSON(automata, payload)
    else:
        raise "Illegal State Transition!"
    # Todo: implement transmission of new state and possible events back



async def transmitJSON(automata: Automata, data: any):
    jsonPayload = json.dumps(data.__dict__)
    await automata._send(jsonPayload)