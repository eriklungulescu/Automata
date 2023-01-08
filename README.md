# Automata 


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#introduction">Introduction</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation-and-setup">Installation and Setup</a></li>
      </ul>
    </li>
    <li><a href="#states-events-state-changes-data-events-and-payloads">States, Events, State Changes, Data Events, and Payloads</a></li>
    <li><a href="#advanced">Advanced</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## Introduction

Automata is a lightweight framework that allows users to define a state machine based websocket server. Each machine has a collection of states, for example, a traffic light state machine has Green, Yellow, and Red states. Each state can have any number of events, these events can be defined by the developer to do whatever they want. They can return data back to the client, transition to a new state, process data, or even do nothing; that is all up the the desired implementation. Overall, the goal of Automata is to provide a unified methodology and doctrine for defining and improving the clarity of websocket communication.

## Getting Started

This is a simple example of how you to set up your Automata instance and run your application.

### Prerequisites
* `python version >= 3.7`

### Installation and Setup

1. Install with `pip install automata-ws`

2. Initialize your Automata (we use app.py)
  ```python3
  from automata import Automata
  
  my_machine = Automata(
    name="myMachine"
  )
  ```

3. Create your states and any events (in any directory you want)
  ```python3
  from automata import State, EventStatus, transition, transmit
  
  red_light = State('red_light')
  
  @red_light.event('change_to_green')
  async def handler(automata, data):
    #do something here...
    run_some_func()
    await transition(automata, 'green', EventStatus.OK) #will change the state of our machine and will report this to the client
    
  green_state = State(
    name="green",
    targets=["yellow"]
  )
  
  @green_light.event('change_to_yellow')
  async def handler(automata, data):
    await transmit(automata, EventStatus.OK, some_data) #will send back data without changing state
    
  #and so on and so on...
  ```

4. Register states in your machine (back in the file you defined the machine)
  ```python3
  my_machine.register_state(red_light) #the first state that is registered will be the initial state for new sessions
  my_machine.register_state(green_light)
  ```

5. Run the machine
  ```python3
  my_machine.run('localhost', 8000)
  ```

## States, Events, State Changes, Data Events, and Payloads 

### 1. States
  - Every state must be unique: there cannot exist two states with the same name
  - A state may have a list of target states: all of the states in which a transition from the referenced state is possible
    - Trying to transition to a state that is not in the target list for the referenced state will raise an exception
    - An undefined target list means that a transition to any state is allowed  
    ###
    
    ```python3
    green_state = State(
      name="green",
      targets=["yellow"] #the target list with all the states that the green_state can transition to
    )
    ```
  - The initial state is the one that is registered first in the `Automata` instance

### 2. Events
  - Events defined for a specific state must be unique
  - All events are identified by their name and defined by their handler
  - Each handler will recieve an `Automata` instance and a `data` instance (either as a `dict` or a `str`)
  ###
  
  ```python3
  @green_state.event('change_to_yellow') #this annotation will create an event for the corresponding state (green_state in this case)
  async def handler(automata: Automata, data):
    run_some_code()
    do_whatever_you_want()
    await transition(automata, 'yellow', EventStatus.OK)
  
  @green_state.event('ping')
  def handler(automata: Automata, data): #the handler doesn't necessarily have to be async
    print('pong')
  
  ```

### 3. State Changes
  - Each state transition has to be relayed to the client: they will receive data about their new state and all events they can call
  - Each state transition has to be accompanied with a status code: these are similar to the 100, 200, 300, 400, 500 status codes defined in HTTP and are found in the `EventStatus` enum
  - A state transition may have data associated with it if needed (data is optional)
  - A state transition is achieved through the `transition` function
    ###
    - ```python3
      await transition(automata, 'logged_in', EventStatus.OK, some_data) #a state transition with some data
      ```

### 4. Data Events
  - It is possible to send data back to the client without changing state: this is achieved through the `transmit` function
  - Each data event must be accompanied with a status code (as mentioned above)
    ###
    - ```python3
      await transmit(automata, EventStatus.OK, some_data) #a data event with no state transition
      ```

### 5. Payloads
  - All client to server payloads must follow the format below
    ###
    - ```json
      {
        "event" : "event_name",
        "data" : data
      }
      ```
  - A state change will be relayed to the client in the following format (occurs when `transition` is called)
    ###
    - ```json
      {
        "state" : "new_state",
        "events" : [
            "event1",
            "event2", //Any number of possible events associated with the new state
        ],
        "status" : 200,
        "data": "some_data" //optional: can be None/Null
      }
      ```
  - Any generic data event will be returned back in the following format (occurs when `transmit` is called)
    ###
    - ```json
      {
        "status" : 200,
        "data": "some_data" //optional
      }
      ```

## Advanced

### 1. Custom HTTP Endpoint(s)
  - As of now all websocket connections are served on `/`
  - It is possible to implement a custom endpoint using the `automata.endpoint('/endpoint')` annotation
  - This is useful if a health check (or something generic) is needed
    ###
    - ```python3
      @my_machine.endpoint('/health')
      async def some_handler(request_headers):
          return 'OK'
      ```
  - **Note**: only `get` requests can be handled 
      
## License 

Apache License 2.0
