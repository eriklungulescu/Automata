# Automata 
Automata is a state based websocket manager that allows you to define your states, events, and event handlers. It provides a unified methodology and doctrine for defining and improving the clarity of websocket communication.


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation-and-setup">Installation and Setup</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## Getting Started

This is a simple example of how you to set up your Automata instance and run your application.

### Prerequisites
* `python version 3.11^`

### Installation and Setup
1. Install using PIP `pip install ...` We haven't made the package yet! 
2. Initialize your Automata (we use app.py)
  ```python3
  from automata import Automata
  
  my_machine = Automata(
    name="myMachine"
  )
  ```
3. Create your states and any events (in any directory you want)
  ```python3
  from automata import State
  
  red_light = State('red_light')
  
  @red_light.event('change_to_green')
  async def handler(automata, data):
    #Do something here...
    run_some_func()
    await transition('green_light') #Will change the state of our machine and will report this to the client
    
  green_light = State('green_light')
  
  @green_light.event('change_to_yellow')
  async def handler(automata, data):
    await transition('yellow')
    
  #And so on and so on...
  ```
4. Register states in your machine (back in the file you defined the machine)
  ```python3
  my_machine.register_state(red_light) #The first state that is registered will be the initial state for new sessions
  my_machine.register_state(green_light)
  ```
5. Run the machine
  ```python3
  my_machine.run('localhost', 8000, '/session')
  ```


## License 

Apache License 2.0
