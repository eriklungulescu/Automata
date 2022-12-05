class StateChangePayload(object):
    def __init__(self, state: str, events: list[str]):
        self.state = state 
        self.events = events

class EventPayload:
    def __init__(self, event: str, data: str):
        self.event = event 
        self.data = data