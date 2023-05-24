__version__ = "1.5.7"
__author__ = "Smartwa Caleb"
__repo__ = "https://github.com/Simatwa/gpt-cli"
__info__ = "Interact with ChatGPT and Bard at the terminal."

import logging

logging.basicConfig(
    format="%(levelname)s - %(message)s - (%(asctime)s) ",  # [%(module)s,%(lineno)s]",
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
        def main(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(getExc(e))
                return resp() if callable(resp) else resp

        return main

    return wrapper
