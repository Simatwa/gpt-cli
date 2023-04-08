__version__ = "1.4.8"
__author__ = "Smartwa Caleb"
__repo__ = "https://github.com/Simatwa/gpt-cli"

import logging

logging.basicConfig(
    format="%(levelname)s - %(message)s - (%(asctime)s)",
    datefmt="%d-%b-%Y %H:%M:%S",
    level=logging.INFO,
)

getExc = lambda e: e.args[1] if isinstance(e.args, list) else str(e)
