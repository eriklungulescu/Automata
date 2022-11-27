from flask import Flask
from controllers.controller import session
from automata.testing import test

app = Flask(__name__)
app.register_blueprint(session)
 
app._json_decoder

@app.route('/health')
def hello_name():
    return "Server is healthy!"
 
if __name__ == '__main__':
    test()
    # app.run()