from collections.abc import Callable
from typing import  Mapping
from types import SimpleNamespace
from uuid import UUID
from .utils.payloads import EventPayload, StateChangePayload
from .utils.errors import DuplicateEventError, DuplicateStateError, InvalidEventPayload, InvalidStateTransition
from urllib.parse import urlsplit, parse_qs
from copy import deepcopy
import json
import asyncio
import websockets
import inspect
import logging
import traceback

class Automata:
    pass

class Event:
    def __init__(self, name: str, handler: Callable[[Automata, any], None]):
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
        self._logger = logging.getLogger(__name__)

    def event(self, eventName: str):
        if eventName in self._events.keys():
            raise DuplicateEventError(self.name, eventName)

        def decorator(func):
            self._events[eventName] = Event(eventName, func)
        return decorator


class Automata:
    def __init__(self, name: str, initial: State = None, states: list[State] = []):
        self.name = name
        self._current_state = initial
        self._states: Mapping[str, State] = {}
        for state in states:
            self._states[state.name] = state
        self._logger = logging.getLogger(__name__)


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
            
    async def _send(self, data: str):
        await self._websocket.send(data)

    def run(self, uri: str, port: int, path: str):
        self._logger.info(f'Starting Automata Websocket server on {uri}:{port}{path}')
        clientPoolHandler = AutomataClientConnectionPoolHandler(self)
        clientPoolHandler._serve(uri, port, path)


class AutomataClientConnectionPoolHandler:

    def __init__(self, automata: Automata):
        self._AUTOMATA_IMAGE = automata
        self._connection_pool: dict[str, dict[UUID, Automata]] = {}
        self._logger = logging.getLogger(__name__)
        self._num_connections = 0
    
    def _serve(self, uri: str, port: int, path: str):
        self._path = path
        self._uri = uri 
        self._port = port

        async def serve_server():
            async with websockets.serve(self._manage_client_connections, uri, port):
                await asyncio.Future() # Runs forever
        asyncio.run(serve_server())
    
    async def _manage_client_connections(self, websocket, path):
        self._num_connections += 1
        self._logger.debug(f'New connection {websocket.id} -> there are {self._num_connections} active connections')

        params = self._parse_path_params(path)
        if (path != self._path and False): # TODO: add path checker...
            print(f"Request at {path} doesn't match defined path {self._path}")
            return
        automata = deepcopy(self._AUTOMATA_IMAGE)
        automata._register_websocket(websocket)

        if "group_id" in params.keys():
            groups = params['group_id']
            for group in groups:
                if group not in self._connection_pool.keys():
                    self._connection_pool[group] = { websocket.id : automata }
                else:
                    self._connection_pool[group][websocket.id] = automata 


        try:
            async for message in websocket:
                await automata.handler(message)
        except websockets.exceptions.ConnectionClosed:
            self._logger.debug(f'Safely closed websocket connection {websocket.id} ')
        except:
            self._logger.error(f'Something went wrong! Forcefully closing websocket connection {websocket.id}')
            self._logger.error(traceback.format_exc())
        finally:
            self._num_connections -= 1
            if "group_id" in params.keys():
                groups = params['group_id']
                for group in groups:
                    del self._connection_pool[group][websocket.id]
                    if len(self._connection_pool[group]) == 0:
                        del self._connection_pool[group]
    
    def _parse_path_params(self, path: str) -> dict[str, any]:
        params = {}
        try:
            url = self._uri + ':' + str(self._port) + path
            params = parse_qs(urlsplit(url).query)
        except:
            self._logger.error("Couldn't parse url params.")
        finally:
            return params


# Library Functions

# Will transition to a new state
async def transition(automata: Automata, target: str):
    if automata._states[automata._current_state.name]._targets == None or target in automata._states[automata._current_state.name]._targets:
        automata._current_state = automata._states[target]
        payload = StateChangePayload(automata._current_state.name , list(automata._states[automata._current_state.name]._events.keys()))
        await transmit(automata, payload)
    else:
        raise InvalidStateTransition(automata._current_state, target)

async def transmit(automata: Automata, data: any):
    jsonPayload = json.dumps(data.__dict__)
    await automata._send(jsonPayload)

