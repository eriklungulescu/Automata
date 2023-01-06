'''
    Automata Design Errors
    - Occurs when a user attempts to create an invalid state machine design
'''

class DuplicateInputIdentifierBaseError(Exception):
    """
        Base error type when we try to initialize a the members of an Automata with duplicate identifiers
    """
    pass
    def __str__(self):
        return "Duplicate identifiers are not allowed"
    

class DuplicateEventError(DuplicateInputIdentifierBaseError):
    """
        Occurs when we try to add duplicate events to a single state
    """
    def __init__(self, state: str, event: str):
        self._state = state 
        self._event = event

    def __str__(self):
        return super().__str__() + f" -> tried adding duplicate event {self._event} to state {self._state}" 

class DuplicateStateError(DuplicateInputIdentifierBaseError):
    """
        Occurs when we try to add duplicate states to a machine
    """
    def __init__(self, machine: str, state: str):
        self._machine = machine 
        self._state = state

    def __str__(self):
        return super().__str__() + f" -> tried adding duplicate state {self._state} to machine {self._machine}" 

class DuplicateEndpointError(DuplicateInputIdentifierBaseError):
    """
        Occurs when we try to create a duplicate endpoint handler
    """
    def __init__(self, endpoint: str):
        self._endpoint = endpoint

    def __str__(self):
        return super().__str__() + f" -> tried creating duplicate endpoint {self._endpoint}" 

'''
    Client Runtime Errors
    - Errors that occur when a client request is invalid
'''

class InvalidStateTransition(Exception):
    def __init__(self, state: str, target: str):
        self._state = state
        self._target = target 

    def __str__(self):
        return f"Tried an invalid state transition from {self._state} to {self._target}"

class InvalidPayload(Exception):
    def __init__(self, payload: str):
        self._invalid_payload = payload 

    def __str__(self):
        return f"Tried to process an invalid payload: {self._invalid_payload}"

class InvalidEvent(Exception):
    def __init__(self, current_state: str, invalid_event: str, allowed_events: str):
        self._current_state = current_state
        self._invalid_event = invalid_event
        self._allowed_events = allowed_events

    def __str__(self):
        return f"Tried to call an invalid event: {self._invalid_event}. The allowed events for the state {self._current_state} are {self._allowed_events}"