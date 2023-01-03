import logging
from example import run_machine

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)s] :: %(message)s ', level=logging.DEBUG)
    logging.getLogger("websockets").setLevel(logging.CRITICAL)
    run_machine()
    # app.run()