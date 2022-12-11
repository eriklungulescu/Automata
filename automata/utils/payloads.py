from enum import Enum

class EventStatus(str, Enum):
    # 200's - the success status codes
    OK = 200
    NewContent = 201
    NoContent = 202
    SuccessfulStateChange = 203

    # 400's - the error status codes
    Error = 400
    Unauthorized = 401
    InvalidEvent = 402
    InvalidPayload = 403

class DataPayload(object):
    def __init__(self, status: EventStatus, data: any = None):
        self.status = status
        self.data = data

class StateChangePayload(DataPayload):
    def __init__(self, state: str, events: list[str], status: EventStatus, data: any = None):
        self.state = state 
        self.events = events
        super().__init__(status, data)

class EventPayload(object):
    def __init__(self, event: str, data: str):
        self.event = event 
        self.data = data