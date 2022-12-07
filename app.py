import logging
from flask import Flask
from controllers.controller import session
from example import run_machine

app = Flask(__name__)
app.register_blueprint(session)
 
app._json_decoder

@app.route('/health')
def hello_name():
    return "Server is healthy!"
 
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)s] :: %(message)s ', level=logging.DEBUG)
    logging.getLogger("websockets").setLevel(logging.CRITICAL)
    run_machine()
    # app.run()