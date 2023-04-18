from Bard import Chatbot
from . import logging, error_handler
from sys import exit
from os import environ
from json import loads
from time import sleep


class Bard:
    def __init__(self, args: object):
        self.args = args
        self.session = environ.get("BARD_SESSION") or self.__get_sess()
        self.active_link = Chatbot(self.session)

    @error_handler(exit)
    def __get_sess(self):
        """Gets Bard's session"""
        if any([self.args.bkey, self.args.bkey_path, self.args.bcookie_file]):
            if self.args.bkey:
                resp = self.args.bkey
            elif self.args.bkey_path:
                with open(self.args.bkey_path) as fh:
                    resp = fh.read()
            else:
                resp = None
                with open(self.args.bcookie_file) as fh:
                    entries = loads(fh)
                for entry in entries:
                    if entry["name"] == "__Secure-1PSID":
                        resp = entry["value"]
            return resp
        else:
            logging.error("Bard's session not found!")

    @error_handler("Error while communicating with Bard")
    def chat(self, prompt: str, stream: bool = True) -> str:
        """Interact with Bard

        Args:
            prompt (str): Text to Bard
            stream (bool) : Stream responses . Default to True

        Returns:
            str: Bard's Response
        """
        if not self.session:
            return logging.error("Bard's session not found!")
        resp = self.active_link.ask(prompt)["content"]
        if stream:
            for value in resp:
                yield value
                sleep(self.args.stream_interval)
        else:
            return resp["content"]
