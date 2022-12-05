from collections.abc import Callable
from typing import Generic, Mapping, TypeVar
from types import SimpleNamespace
from .utils.payloads import EventPayload, StateChangePayload
from .utils.errors import DuplicateEventError, DuplicateStateError, InvalidEventPayload
import json
import asyncio
import websockets
from copy import deepcopy
import inspect
from _thread import start_new_thread

class Automata:
    pass

T = TypeVar("T")
class Event(Generic[T]):
    def __init__(self, name: str, handler: Callable[[Automata, T], None]):
        self.name = name
        self._handler = handler

    async def _process_and_handle(self, automata: Automata, event: str):
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

    def event(self, eventName: str):
        if eventName in self._events.keys():
            raise DuplicateEventError(self.name, eventName)

        def decorator(func):
            self._events[eventName] = Event(eventName, func)
        return decorator

"""
    We need a wrapper that maintains every websocket connection and their running handlers

"""

class Automata:
    def __init__(self, name: str, initial: State = None, states: list[State] = []):
        self.name = name
        self._current_state = initial
        self._states: Mapping[str, State] = {}
        for state in states:
            self._states[state.name] = state

    def register_state(self, state: State):
        if state.name in self._states:
            raise DuplicateStateError(self.name, state.name)

        if (len(self._states.keys()) == 0):
            self._current_state = state
        self._states[state.name] = state

    async def handler(self, event: EventPayload | str): # TODO: Add input error checking
        data = event
        if (isinstance(data, str)):
            data: EventPayload  = json.loads(event, object_hook=lambda d: SimpleNamespace(**d))
        
        await self._handler(data.event, data.data)

    async def _handler(self, event_name: str, data: str = None):
        if event_name not in self._states[self._current_state.name]._events.keys():
            raise InvalidEventPayload(self._current_state.name, event_name)
        else:
            await self._states[self._current_state.name]._events[event_name]._process_and_handle(self, data)

    # Websocket Functions
    def _register_websocket(self, websocket):
        self._websocket = websocket
        

    async def _receive(self):
        print(self._websocket.id)

        try:
            async for message in self._websocket:
                await self.handler(message)
        except:
            print('Connection closed') # TODO: add connection closed handler
    
    async def _send(self, data: str):
        await self._websocket.send(data)

    def run(self, uri: str, port: int, path: str):
        clientPoolHandler = AutomataClientConnectionPoolHandler(self)
        clientPoolHandler._serve(uri, port, path)


class AutomataClientConnectionPoolHandler:

    def __init__(self, automata: Automata):
        self._AUTOMATA_IMAGE = automata
        self._connection_pool = {}
    
    def _serve(self, uri: str, port: int, path: str):
        print(f'Running websocket client on: {uri}:{port}{path}')
        self._path = path

        async def serve_server():
            async with websockets.serve(self._manage_client_connections, uri, port):
                await asyncio.Future() # Runs forever
        asyncio.run(serve_server())
    
    async def _manage_client_connections(self, websocket, path):
        if (path != self._path):
            print(f"Request at {path} doesn't match defined path {self.path}")
            return
        
        automata = deepcopy(self._AUTOMATA_IMAGE)
        automata._register_websocket(websocket)
        await automata._receive()
        


# Library Functions

# Will transition to a new state
async def transition(automata: Automata, nextState: str):
    if automata._states[automata._current_state.name]._targets == None or nextState in automata._states[automata._current_state.name]._targets:
        automata._current_state = automata._states[nextState]
        payload = StateChangePayload(automata._current_state.name , list(automata._states[automata._current_state.name]._events.keys()))
        await transmit(automata, payload)
    else:
        raise "Illegal State Transition!"
    # Todo: implement transmission of new state and possible events back

async def transmit(automata: Automata, data: any):
    jsonPayload = json.dumps(data.__dict__)
    await automata._send(jsonPayload)

