# Input Errors

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

# Automata Errors

class InvalidStateTransition:
    def __init__(self, state: str, target: str):
        self._state = state
        self._target = target 

    def __str__(self):
        return f"Tried an invalid state transition from {self._state} to {self._target}"
