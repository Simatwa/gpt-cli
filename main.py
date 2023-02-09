#!/usr/bin/python
__version__ = "1.0"
__author__ = "Smartwa Caleb"
from colorama import Fore, Back
from os import getlogin


class config_handler:
    def __init__(self):
        self.sample = """
          { 
             "model":"text-davinci-003",
             "prompt":"How to scan for SMB vulnerability using NMAP?",
             "temperature":0.7,
             "max_tokens":256,
             "top_p":1,
             "frequency_penalty":0,
             "presence_penalty":0
        }"""
        self.color_dict = {
            "cyan": Fore.CYAN,
            "red": Fore.RED,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "black": Fore.BLACK,
            "reset": Fore.RESET,
        }
        self.bcolor_dict = {
            "cyan": Back.CYAN,
            "red": Back.RED,
            "green": Back.GREEN,
            "yellow": Back.YELLOW,
            "blue": Back.BLUE,
            "magenta": Back.MAGENTA,
            "black": Back.BLACK,
            "reset": Back.RESET,
        }
        self.float_range = self.generate_floats()
        self.colors = list(self.color_dict.keys())

    def generate_floats(self):
        """Generates floats in range (0-2)"""
        from numpy import arange

        resp = []
        for val in map(lambda a: round(float(a), 1), arange(0.1, 2.1, 0.1)):
            resp.append(val)
        return resp

    def get_args(self):
        """Gets args parsed"""
        import argparse

        parser = argparse.ArgumentParser(
            description="Interact with GPT3 at the terminal"
        )
        parser.add_argument(
            "-v", "--version", action="version", version=f"%(prog)s v{__version__}"
        )
        parser.add_argument("message", help="Message to be send.", nargs="*")
        models = [
            "text-davinci-001",
            "text-davinci-002",
            "text-davinci-003",
            "text-curie-001",
            "text-babbage-001",
            "text-ada-001",
            "babbage",
            "davinci",
            "ada",
            "text-ada",
            "curie",
            "curie-instruct-beta",
            "davinci-instruct-beta",
            "code-davinci-002",
            "code-cushman-001",
        ]
        parser.add_argument(
            "-m",
            "--model",
            help="Model to be used",
            choices=models,
            metavar="davinci|curie|babbage",
        )
        parser.add_argument(
            "-t",
            "--temperature",
            help="Charge of the generated text's randomness",
            type=float,
            choices=self.float_range[0:10],
            metavar="[0.1-1]",
        )
        parser.add_argument(
            "-mt",
            "--max-tokens",
            help="Maximum number of tokens to be generated upon completion",
            type=int,
            dest="max_tokens",
            choices=range(1, 4001),
            metavar="[1-4000]",
        )
        parser.add_argument(
            "-tp",
            "--top-p",
            help="Sampling threshold during inference time",
            type=float,
            dest="top_p",
            choices=self.float_range[0:10],
            metavar="[0.1-1]",
        )
        parser.add_argument(
            "-f",
            "--frequency-penalty",
            help="Chances of word being repeated",
            type=float,
            dest="frequency_penalty",
            choices=self.float_range,
            metavar="[0.1-2]",
        )
        parser.add_argument(
            "-p",
            "--presence-frequency",
            help="Chances of topic being repeated",
            type=float,
            dest="presence_frequency",
            choices=self.float_range,
            metavar="[0.1-2]",
        )
        parser.add_argument("-k", "--key", help="GPT-API key")
        parser.add_argument(
            "-kp",
            "--key-path",
            help="Path to text-file containing GPT-api key",
            dest="key_path",
        )
        parser.add_argument(
            "-c", "--config", help="Use json-formatted configurations in path"
        )
        parser.add_argument(
            "-ic",
            "--input-color",
            help="Font color for inputs",
            default="reset",
            dest="input_color",
            metavar="[cyan|green|yellow|red]",
            choices=self.colors,
        )
        parser.add_argument(
            "-oc",
            "--output-color",
            help="Font color for outputs",
            default="cyan",
            dest="output_color",
            metavar="[cyan|green|yellow|red]",
            choices=self.colors,
        )
        parser.add_argument(
            "-bc",
            "--background-color",
            help="Console's background-color",
            default="reset",
            dest="background_color",
            metavar="[blue,magenta,black,reset]",
            choices=self.colors,
        )
        parser.add_argument(
            "-pc",
            "--prompt-color",
            help="Prompt's display color",
            default="yellow",
            dest="prompt_color",
            metavar="[cyan|green|yellow|red]",
            choices=self.colors,
        )
        parser.add_argument(
            "--prompt",
            help="Customizes the prompt display",
            default=f"┌─[{getlogin().capitalize()}@chatgpt3]─(%H:%M:%S)",
            dest="settings",
            nargs="*",
        )
        parser.add_argument(
            "--response",
            help="Holds the last response from remote-API",
            required=False,
            action="store_true",
        )
        return parser.parse_args()

    def set_log(self):
        """Configs logging"""
        import logging

        logging.basicConfig(
            format="%(levelname)s - %(message)s : %(asctime)s",
            datefmt="%d-%b-%Y %H:%M:%S",
            level=logging.INFO,
        )
        return logging

    def main(self):
        return self.get_args(), self.set_log()


config_h = config_handler()
args, logging = config_h.main()
from sys import exit
import openai
import json
import cmd
from re import sub
from datetime import datetime
from colorama import Fore
from os import system


class gpt3_interactor:
    def __init__(self):
        self.params = self.get_filters()
        try:
            openai.api_key = self.params["api_key"]
        except KeyError:
            logging.debug(f"API-key not found in config")
        else:
            logging.debug("Getting rid of key from params")
            self.params.pop("api_key")
        if not openai.api_key:
            self.get_api_key()

    def get_api_key(self):
        openai.api_key = args.key
        if not openai.api_key:
            openai.api_key_path = args.key_path
        if not openai.api_key and not openai.api_key_path:
            exit(logging.critical("API-Key not found!"))

    def get_filters(self):
        """Loads the configurations"""
        if args.config:
            try:
                with open(args.config) as file:
                    return json.loads(file.read())
            except Exception as e:
                exit(logging.critical(str(e)))
        else:
            return self.partial_filters(json.loads(config_handler().sample))

    def partial_filters(self, sample: dict):
        """Loads partial configurations parsed"""
        from_args = {
            "prompt": args.message,
            "model": args.model,
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "top_p": args.top_p,
            "frequency_penalty": args.frequency_penalty,
            "presence_frequency": args.presence_frequency,
        }
        for key, value in from_args.items():
            if value:
                sample[key] = value
        return sample

    def main(self):
        """Main Function"""
        try:
            self.params["prompt"] = args.message
            resp = openai.Completion.create(**self.params)
        except Exception as e:
            rp = (False, e)
        else:
            args.response = dict(resp)
            rp = (True, args.response["choices"][0])
        finally:
            return rp


gpt3 = gpt3_interactor()


class local_interactor:
    def __init__(self):
        self.special_input = {
            ":check": self.check,
            ":set": self.edit_config,
            ":response": self.response,
            ":configurations": self.configurations,
            ":help": self.help,
        }
        self.run = lambda key: self.special_input[key]()

    def help(self):
        return f"""
gpt-cli v{__version__} 

Special character is `:`  
[#] Special commands have a predefined function as shown:

╒═════════════════╤══════════════════════════════════════════════════════╕
│ Command         │ Function                                             │
╞═════════════════╪══════════════════════════════════════════════════════╡
│ :check          │ Gives a shallow display of the response from the API │
├─────────────────┼──────────────────────────────────────────────────────┤
│ :set            │ Configures api request parameters                    │
├─────────────────┼──────────────────────────────────────────────────────┤
│ :response       │ Shows whole feedback from the last request           │
├─────────────────┼──────────────────────────────────────────────────────┤
│ :configurations │ Shows api request parameters                         │
├─────────────────┼──────────────────────────────────────────────────────┤
│ :help           │ Outputs this help info                               │
╘═════════════════╧══════════════════════════════════════════════════════╛

[#] Inputs without special character interacts with the CHAT-GPT3 except:

    (a). font_color : modifies font-color
          e.g 'font_color input red'

    (b). background_color : modifies background_color
          e.g 'background_color cyan'

[#] Use single `:` (full-colon) to interact with the special commands
      e.g ':configurations'

[#] Use double `::` (full-colon) to interact with the system commands
      e.g '::ifconfig'

[NOTE] special characters must occupy the first indexes

[#] Modify the chat-gpt parameters by introducing `:set` command
  e.g ':set model curie'
        """

    def response(self):
        return json.dumps(args.response, indent=4)

    def configurations(self):
        return json.dumps(gpt3.params, indent=4)

    def edit_config(self):
        new_conf = args.settings.split(" ")
        reference = {
            "model": str,
            "prompt": str,
            "temperature": float,
            "max_tokens": int,
            "top_p": int,
            "frequency_penalty": float,
            "presence_penalty": float,
        }
        if new_conf[1] in tuple(reference.keys()):
            try:
                gpt3.params[new_conf[1]] = reference[new_conf[1]](new_conf[2])
                return "ok"
            except Exception as e:
                logging.error(e)
        else:
            logging.error(f"'{new_conf[1]}' NOT in {list(reference.keys())}")

    def check(self):
        if isinstance(args.response, dict):
            rp = args.response["choices"][0]
            try:
                rp.pop("text")
            except KeyError:
                pass
            return rp


time_now_format = lambda v: str(
    f"{config_h.color_dict[args.prompt_color]}{datetime.today().strftime(v)}{config_h.color_dict[args.input_color]}\r\n└──╼ ❯❯❯"
)


class main_gpt(cmd.Cmd):
    prompt_disp = (
        " ".join(args.settings) if isinstance(args.settings, list) else args.settings
    )
    prompt = time_now_format(prompt_disp)
    config_handler = config_handler()
    color_dict = config_handler.color_dict
    bcolor_dict = config_handler.bcolor_dict

    def apply_color(self):
        print(
            self.bcolor_dict[args.background_color] + self.color_dict[args.input_color]
        )

    def default(self, raw):
        interactive = local_interactor()
        out = lambda b: print(self.color_dict[args.output_color] + b + Fore.RESET)
        if raw.split(" ")[0] in tuple(interactive.special_input.keys()):
            args.settings = raw
            out(str(interactive.run(raw.split(" ")[0])))
        elif raw[0:2] == "::":
            system((raw[2:]).strip())
        elif bool(raw):
            args.message = raw
            rp = gpt3.main()
            if rp[0]:
                out(sub("\n\n", "\n", rp[1]["text"], 1))
            else:
                logging.error(str(rp[1]))
        self.do_prompt(self.prompt_disp)

    def do_prompt(self, line):
        """Modify prompts"""
        self.prompt_disp = line
        self.prompt = time_now_format(line)

    def do_font_color(self, line):
        """Sets font color"""
        line = line.lower().split(" ")
        try:
            self.color_dict[line[1]]
            if line[0] in ("input"):
                args.input_color = line[1]
            elif line[0] in ("output"):
                args.output_color = line[1]

            else:
                args.prompt_color = line[1]
                self.do_prompt(self.prompt_disp)
        except Exception as e:
            logging.error(str(e))
        else:
            self.apply_color()

    def do_background_color(self, line):
        """Sets background-color"""
        from colorama import Back

        try:
            self.bcolor_dict[line.lower()]
            args.background_color = line.lower()
            self.apply_color()
        except Exception as e:
            logging.error(str(e))


if __name__ == "__main__":
    try:
        run = main_gpt()
        if args.message:
            run.default(" ".join(args.message))
        run.cmdloop()
    except (KeyboardInterrupt, EOFError):
        exit(logging.info("Stopping program"))
    except Exception as e:
        logging.error(str(e))
