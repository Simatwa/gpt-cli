__version__ = "1.5.0"
__author__ = "Smartwa Caleb"
__repo__ = "https://github.com/Simatwa/gpt-cli"

import logging

logging.basicConfig(
    format="%(levelname)s - %(message)s - (%(asctime)s)",
    datefmt="%d-%b-%Y %H:%M:%S",
    level=logging.INFO,
)

getExc = lambda e: e.args[1] if isinstance(e.args, list) else str(e)

def error_handler(resp=None):
    """Handle exceptions

    Args:
        resp (Any, optional): Value to be returned incase of exception. Defaults to None.
    """
    def wrapper(func):
        def main(*args,**kwargs):
            try:
                rp = func(*args,**kwargs)
            except Exception as e:
                logging.error(getExc(e))
                rp = resp() if callable(resp) else resp
            finally:
                return rp
        return main
    return wrapper