from automata.automata import Event, Automata, State, transition

# Example datatype
class user:
    def __init__(self, name, password):
        self.name = name
        self.password = password
    def __str__(self):
        print('name: ' + self.name)
        print('password: ' + self.password)


async def login(automata: Automata, data: user):
    print(data.name)
    print(data.password)
    if True:
        await transition(automata, "loggedIn")

def test():
    automata = Automata(
        initial="idle",
        states=[
            State(
                name="idle",
                targets=["loggedIn"], #optional and used for transition checking
                events=[
                    Event[user](
                        name='login',
                        handler=login
                    )
                ],
            ),
            State(
                name="loggedIn",
                events=[
                    Event(
                        name="logout",
                        handler= lambda a, _:
                            transition(a, "loggedOut")
                    )
                ]
            ),
            State(
                name="loggedOut",
            )
        ]
    )

    # asyncio.run(main())
    print('here')
    automata.serve('localhost', 8081, '/')
