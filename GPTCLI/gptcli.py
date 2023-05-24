#!/usr/bin/python
from . import __version__, __author__, __repo__, __info__
from colorama import Fore, Back
from os import getlogin, getcwd, path
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich import print as rich_print
import argparse


class config_handler:
    def __init__(self):
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
        self.v4models = [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-32k",
            "gpt-3.5-turbo-0301",
            "gpt-4-0314",
            "gpt-4-32k-031",
        ]
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
        disp = f"""
            Repo : {__repo__}
            By   : {__author__}"""
        gstyle = Style(color="cyan", frame="double")
        intro = Panel(disp, title=f"gpt-cli v{__version__}", style=gstyle)
        rich_print(intro)

        parser = argparse.ArgumentParser(description=__info__)
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
            help="ChatGPT model to be used",
            choices=models + self.v4models,
            metavar="|".join(self.v4models[0:3]),
        )
        parser.add_argument(
            "-t",
            "--temperature",
            help="Charge of the generated text's randomness",
            type=float,
            choices=self.float_range[0:10],
            metavar="[0.1-1]",
            default=0.1,
        )
        parser.add_argument(
            "-mt",
            "--max-tokens",
            help="Maximum number of tokens to be generated upon completion",
            type=int,
            choices=range(1, 7001),
            metavar="[1-7000]",
            default=4000,
        )
        parser.add_argument(
            "-tp",
            "--top-p",
            help="Sampling threshold during inference time",
            type=float,
            choices=self.float_range[0:10],
            metavar="[0.1-1]",
            default=0.0,
        )
        parser.add_argument(
            "-f",
            "--frequency-penalty",
            help="Chances of word being repeated",
            type=float,
            choices=self.float_range,
            metavar="[0.1-2]",
            default=0.0,
        )
        parser.add_argument(
            "-p",
            "--presence-frequency",
            help="Chances of topic being repeated",
            type=float,
            choices=self.float_range,
            default=0.0,
            metavar="[0.1-2]",
        )
        parser.add_argument("-k", "--key", help="OPENAI-API-KEY")
        parser.add_argument(
            "-kp",
            "--key-path",
            help="Path to text-file containing GPT-api key",
            metavar="path",
        )
        parser.add_argument(
            "-ic",
            "--input-color",
            help="Font color for inputs",
            default="green",
            metavar="[cyan|green|yellow|red]",
            choices=self.colors,
        )
        parser.add_argument(
            "-oc",
            "--output-color",
            help="Font color for outputs",
            default="cyan",
            metavar="[cyan|green|yellow|red]",
            choices=self.colors,
        )
        parser.add_argument(
            "-bc",
            "--background-color",
            help="Console's background-color",
            default="reset",
            metavar="[blue,magenta,black,reset]",
            choices=self.colors,
        )
        parser.add_argument(
            "-pc",
            "--prompt-color",
            help="Prompt's display color",
            default="yellow",
            metavar="[cyan|green|yellow|red]",
            choices=self.colors,
        )
        parser.add_argument(
            "--prompt",
            help="Customizes the prompt display",
            default=f"┌─[{getlogin().capitalize()}@GPT-CLI]─(%H:%M:%S)",
            dest="settings",
            nargs="*",
        )
        parser.add_argument(
            "-tm",
            "--timeout",
            help="Request timeout while making request - (Soon)",
            metavar="value",
        )
        parser.add_argument("-pr", "--proxy", help="Pivot request through this proxy")
        parser.add_argument(
            "-rc",
            "--reply-count",
            help="Number of responses to be received",
            default=1,
            type=int,
            metavar="value",
        )
        parser.add_argument(
            "-g",
            "--gpt",
            help="ChatGPT version to be used ",
            choices=["1", "4"],
            metavar="|".join(["1,4"]),
            default="4",
        )
        parser.add_argument(
            "-sp",
            "--system-prompt",
            nargs="*",
            help="Text to train ChatGPT at the start",
            default="You are ChatGPT, a large language model trained by OpenAI. Respond conversationally",
            metavar="text",
        )
        parser.add_argument(
            "-fp",
            "--file-path",
            help="Path to .csv file containing role and prompt - [act,prompt]",
            metavar="path",
        )
        parser.add_argument(
            "-o",
            "--output",
            help=f"Filepath for saving the chats - default [{getcwd()}/.chatgpt-history.txt]",
            default=path.join(getcwd(), ".chatgpt-history.txt"),
            metavar="path",
        )
        parser.add_argument(
            "-pp",
            "--prompt-prefix",
            help="Text to append before saving each prompt - default [>>> timestamp]",
            metavar="prefix",
            default=">>> (%d-%b %H:%M:%S) : ",
        )
        parser.add_argument(
            "-rp",
            "--response-prefix",
            help="Text to append before saving each response - default [None]",
            metavar="prefix",
            default="",
        )
        parser.add_argument(
            "-dm",
            "--dump",
            help="Stdout [keys,values]; Save all prompts in json format to a file",
            metavar="|".join(["keys", "values", "show", "{fnm}"]),
        )
        parser.add_argument(
            "-dl",
            "--delimiter",
            help="Delimeter for the .CSV file - [act,prompt]",
            metavar="symbol",
        )
        parser.add_argument(
            "-cf",
            "--cookie-file",
            help="Path to Bing's cookies - for Edge Image Generation",
            metavar="path",
        )
        parser.add_argument(
            "-bk", "--bard-key", dest="bkey", metavar="KEY", help="Bard's session value"
        )
        parser.add_argument(
            "-bkp",
            "--bard-key-path",
            dest="bkey_path",
            metavar="PATH",
            help="Path to Bard's key path",
        )
        parser.add_argument(
            "-bcf",
            "--bard-cookie-file",
            dest="bcookie_file",
            metavar="PATH",
            help="Path to Bard's cookie file",
        )
        parser.add_argument(
            "-si",
            "--stream-interval",
            metavar="TIME",
            help="Interval for printing responses in (s)",
            type=float,
            default=0.01,
        )
        parser.add_argument(
            "-spin",
            "--spinner",
            choices=[1, 2],
            type=int,
            help="Busy bar indicator",
            metavar="1|2",
            default=2,
        )
        parser.add_argument(
            "--disable-stream",
            help="Specifies not to stream responses from ChatGPT",
            action="store_true",
        )
        parser.add_argument(
            "--new-record",
            help="Override previous chats under the filepath",
            action="store_true",
        )
        parser.add_argument(
            "--disable-recording",
            help="Disable saving prompts and responses",
            action="store_true",
        )
        parser.add_argument(
            "--zero-show",
            help="Specifies not to stdout prompt of the act parsed",
            action="store_true",
        )
        parser.add_argument(
            "--bard", help="Make Bard the default GPT", action="store_true"
        )
        parser.add_argument(
            "--markdown",
            help="Stdout responses in markdown-format - disables streaming",
            action="store_true",
        )
        parser.add_argument(
            "--update",
            help="Download latest prompts - [awesome-chatgpt-prompts]",
            action="store_true",
        )
        parser.add_argument(
            "--sudo",
            help="Run commands against system with sudo privileges",
            action="store_true",
        )
        return parser.parse_args()

    def main(self):
        return self.get_args()


config_h = config_handler()
args = config_h.main()
from sys import exit, stderr
import json
import openai
import cmd
from . import logging, getExc, error_handler
from .image import imager
from .emage import emager
from re import sub
from datetime import datetime
from os import system, remove, path, environ, makedirs
from threading import Thread as thr
from appdirs import AppDirs
from rich.markdown import Markdown
from .addons import file_parser, system_control, progress
from .bard import Bard
from time import sleep

app_dir = AppDirs(
    "gpt-cli",
    "smartwa",
).user_data_dir

first_time_run = False

date_stamp = lambda text: datetime.today().strftime(text)

if not path.isdir(app_dir):
    first_time_run = True
    try:
        makedirs(app_dir)
    except Exception as e:
        logging.error(getExc(e))


class gpt3_interactor:
    def __init__(self):
        self.out = (
            lambda rp: rich_print(Markdown(rp, style=Style(color=args.output_color)))
            if args.markdown
            else print(rp)
        )

    def gpt_v1(self, rp: str = None):
        """Utilises GPTv1"""
        if not args.disable_stream:
            for data in chatbot.ask_stream(
                args.message, args.temperature, user=args.role
            ):
                progress.stop_spinning()
                print(data, end="", flush=True)
                rp = "".join([rp, data])
        else:
            rp = chatbot.ask(args.message, user=args.role)
            progress.stop_spinning()
            self.out(rp)
        return rp

    def gpt_v4(self, rp: str = None):
        """Utilises GPTv4"""
        if not args.disable_stream:
            for data in chatbot.ask_stream(args.message, role=args.role):
                progress.stop_spinning()
                print(data, end="", flush=True)
                rp = "".join([rp, data])
        else:
            rp = chatbot.ask(args.message, role=args.role)
            progress.stop_spinning()
            self.out(rp)
        return rp

    def main(self):
        """Main Method"""
        try:
            if args.gpt in ("4"):
                return (True, self.gpt_v4(""))
            else:
                return (True, self.gpt_v1(""))
        except Exception as e:
            # logging.exception(e)
            info = getExc(e)
            return (False, info)


gpt3 = gpt3_interactor()


class local_interactor:
    def __init__(self):
        self.special_input = {}
        self.run = lambda key: self.special_input[key]()


class tracker:
    """Keeps track of the prompts & responses"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.feedback = None
        self.failed_to_record = False

    def save_record(self) -> None:
        """Write prompts and responses in a file"""
        info_to_write = f"\n\n{date_stamp(args.prompt_prefix)}{args.message}\n\n{date_stamp(args.response_prefix)}{self.feedback}"
        try:
            with open(self.filepath, "a", encoding="utf-8") as fp:
                fp.write(info_to_write)
        except Exception as e:
            logging.error(f"Failed to keep record - {getExc(e)}")
            self.failed_to_record = True

    def main(self, response: str) -> None:
        """Main method"""
        if any([self.failed_to_record, args.disable_recording]):
            return
        if isinstance(response, list):
            self.feedback = "\n".join(response)
        else:
            self.feedback = sub("\n", "", response, 1)
        thr(target=self.save_record).start()


class intro_prompt_handler:
    """Fetches prompts"""

    def __init__(self, filename: str = path.join(app_dir, "awesome_prompts")):
        self.fnm = filename
        self.links = {
            "prompts": "https://raw.githubusercontent.com/f/awesome-chatgpt-prompts/main/prompts.csv",
            "prompts1": "https://raw.githubusercontent.com/Simatwa/gpt-cli/main/assets/prompts.csv",
        }

    def update(self) -> list:
        from requests import get

        try:
            logging.info("Updating acts and prompts")

            for key, value in self.links.items():
                resp = get(value, timeout=15)
                if resp.status_code == 200:
                    with open(path.join(app_dir, key), "w", encoding="utf-8") as fh:
                        fh.write(resp.text)
                else:
                    logging.error(
                        f'Failed to get prompts from "{value}" - [{resp.status_code} : {resp.reason}]'
                    )
        except Exception as e:
            logging.error(getExc(e))

    def read_contents(
        self, filename: str = None, delimiter: str = ",", resp: dict = {}
    ):
        """Read prompts and return in dict {act:prompt}"""
        import csv

        with open(filename or self.fnm, encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter=delimiter):
                resp[row["act"]] = row["prompt"]
        return resp

    def display_info(self, resp: dict) -> None:
        """Displays acts and roles"""
        x = 0
        if args.dump:
            # with open(args.dump, "w") as fh:
            if args.dump in ("keys", "roles", "acts", "act", "role"):
                from tabulate import tabulate

                data = []
                for key in resp.keys():
                    data.append([key])

                print(
                    tabulate(
                        data,
                        headers=["Prompt Keys"],
                        tablefmt="fancy_grid",
                        showindex=True,
                    )
                )
            elif args.dump in ("values", "prompts", "value", "prompt"):
                for prompt in resp.values():
                    print(x, ">>", prompt, end="\n\n")
                    x += 1
            elif args.dump in ("show", "pretty", "prettify"):
                for key, value in resp.items():
                    print(
                        f"{config_h.color_dict[args.input_color]}>>[{x}] {key} : {config_h.color_dict[args.output_color]}{value}{Fore.RESET}",
                        end="\n\n",
                    )
                    x += 1
            elif args.dump in ("pdf"):
                from .addons import prompts_to_pdf

                prompts_to_pdf().main()

            else:
                with open(args.dump, "w", encoding="utf-8") as fh:
                    from json import dumps

                    data = json.dumps(resp, indent=4)
                    fh.write(data)
                    print(data)
            exit(0)

    def main(self, filepath: str = None):
        resp = {}
        try:
            if any(
                [
                    args.update,
                    first_time_run,
                    not path.isfile(path.join(app_dir, "prompts")),
                ]
            ):
                self.update()
            if filepath:
                resp = self.read_contents(filepath, args.delimiter or ",")
                self.display_info(resp)
            else:
                tpath = lambda fp: path.join(app_dir, fp)
                resp = self.read_contents(tpath("prompts"))
                resp = self.read_contents(tpath("prompts1"), "~", resp)
                self.display_info(resp)
            return resp

        except Exception as e:
            logging.error(getExc(e))
            return resp


time_now_format = lambda v: str(
    f"{config_h.color_dict[args.prompt_color]}{date_stamp(v)}{config_h.color_dict[args.input_color]}\r\n└──╼ ❯❯❯"
)
join_list = lambda line: "_".join(
    line.split(" ") if len(line.split(" ")) > 1 else [line]
)


class main_gpt(cmd.Cmd):
    prompt_disp = (
        " ".join(args.settings) if isinstance(args.settings, list) else args.settings
    )
    prompt = time_now_format(prompt_disp)
    config_handler = config_handler()
    color_dict = config_handler.color_dict
    bcolor_dict = config_handler.bcolor_dict
    interactive = local_interactor()
    parser = lambda self, line: file_parser(line).parse()
    if any([args.bkey, args.bkey_path, args.bcookie_file, environ.get("BARD_SESSION")]):
        bard = Bard(args)
    elif args.bard:
        exit(logging.critical("Bard's cookie file is required"))
    elif not any([args.dump, args.update]):
        logging.warning("Cannot use Bard, since cookie file is missing.")

    def apply_color(self):
        print(
            self.bcolor_dict[args.background_color] + self.color_dict[args.input_color]
        )

    def prompt_is_error_free(self, prompt, resp=True) -> bool:
        """Checks if prompt contains [sorry]"""
        if isinstance(prompt, list):
            if len(prompt) >= 2 and prompt[0:2] == ["I'm", "sorry"]:
                resp = False
        else:
            if prompt.startswith("I'm sorry"):
                resp = False
        return resp

    @progress.run()
    def default(self, raw, return_fb=False, no_check=False):
        raw = self.parser(raw)
        run_against_system = False
        if not raw:
            self.do__prompt(self.prompt_disp)
            return
        # out = lambda b: print(self.color_dict[args.output_color] + b + Fore.RESET)
        if raw[0:2] == "./":
            system((raw[2:]).strip())
        else:
            progress.display_bar(args)
            if "--system" in raw:
                run_against_system = True
                raw = raw.replace("--system", "")
            if any(["--bard" in raw, args.bard]) and not no_check:
                return self.do_bard(raw.replace("--bard", ""))
            args.message = raw
            print(self.color_dict[args.output_color], end="")
            rp = gpt3.main()
            if rp[0]:
                feedback = sub("\n\n", "\n", rp[1], 1)
                if return_fb:
                    return feedback.strip()
                record_keeper.main(feedback)
                if run_against_system:
                    system_control(feedback).execute(args.sudo)

            else:
                progress.stop_spinning()
                logging.error(str(rp[1]))
            print(Fore.RESET)
        self.do__prompt(self.prompt_disp)

    def do_gpt4(self, line):
        """Interact with ChatGPT4"""
        self.default(line, no_check=True)

    @progress.run()
    def do_bard(self, line, return_fb=False, chat=False):
        """Interact with Google's bard"""
        progress.display_bar(args)
        if "--gpt4" in line:
            return self.default(line.replace("--gpt4", ""), no_check=True)

        args.message = line
        if chat:
            print(self.color_dict[args.input_color], end="")
        else:
            print(self.color_dict[args.output_color], end="")
        if args.disable_stream:
            inf, info = self.bard.chat(line, False), ""
            for value in inf:
                progress.stop_spinning()
                info = info + value
            gpt3.out(info)
        else:
            info = ""
            for val in self.bard.chat(line):
                progress.stop_spinning()
                print(val, end="", flush=True)
                info = info + val
        if not chat:
            record_keeper.main(info)
        print(self.color_dict[args.input_color])
        self.do__prompt(self.prompt_disp)
        if return_fb:
            return info

    @error_handler(False)
    def do__botchat(self, line):
        rich_print("Let the bots talk:")

        def get_value(msg: str, type1: object = str) -> str:
            while True:
                val = input(f"[*] " + msg + " >>")
                if val:
                    if type1 == int:
                        if val.isdigit():
                            return int(val)
                    else:
                        return val

        def gpt_chat(msg):
            print(">>[ChatGPT]")
            return self.default(msg, return_fb=True)

        def bard_chat(msg):
            print("\n<<[Bard]")
            return self.do_bard(msg, return_fb=True, chat=True)

        gpt_ = get_value("Enter prompt for ChatGPT")
        bard_ = get_value("Enter prompt for Bard")
        amount = get_value("Enter amount of chat cycles [0 - infinity]", int)
        interval = get_value("Enter sleep interval in each chat (s) - preferred 0", int)
        gpt = gpt_chat(gpt_)
        bard = bard_chat(bard_)
        while amount if amount else True:
            args.message = gpt
            record_keeper.main(bard)
            gpt = gpt_chat(bard)
            bard = bard_chat(gpt)
            if interval:
                sleep_duration = 0
                print()
                while sleep_duration != interval:
                    sleep_duration += 1
                    print(f">[{interval}]<{sleep_duration}", end="\r")
                    sleep(1)

    def do_txt2img(self, line):
        """Generate images based on GPT description"""
        line = self.parser(line)
        if not line:
            self.do__prompt(self.prompt_disp)
            return
        print(
            self.color_dict[args.output_color] + ">>[*] Querying description from GPT",
            end="\r",
        )
        imagiser = imager(line.split(" "))
        description = self.default(imagiser.args.prompt, return_fb=True)
        if description and self.prompt_is_error_free(description):
            print(self.color_dict[args.input_color])
            imagiser.args.prompt = description.strip()
            if imagiser.args.emg:
                self.do_emg(imagiser.args.prompt, imagiser.args)
            else:
                rp = imagiser.main()
                if isinstance(rp, dict):
                    record_keeper.main(rp["url"])

        else:
            print("")
            if not description:
                logging.error("Failed to generate description.")
        self.do__prompt(self.prompt_disp)

    def do_img(self, line):
        line = self.parser(line)
        if not line:
            return
        """Text-to-Image handler"""
        print(self.color_dict[args.output_color], end="\r")
        resp = imager(line.split(" ")).main()
        if isinstance(resp, dict):
            args.message = line
            record_keeper.main(resp["url"])
        self.do__prompt(self.prompt_disp)

    def do_emg(self, line, args_parsed=False):
        line = self.parser(line)
        if not line:
            return
        print(
            self.color_dict[args.input_color if args_parsed else args.output_color],
            end="\r",
        )
        try:
            if args.cookie_file:
                emg_args = args_parsed if args_parsed else imager(line.split(" ")).args
                emg_args.__setattr__("cookie_file", args.cookie_file)
                download = emager(emg_args)
                download.main()
                args.message = line
                if isinstance(download.urls, list):
                    record_keeper.main(download.urls)
            else:
                logging.warning(
                    "Cookie file is required at launch [--cookie-file {path}]"
                )
        except Exception as e:
            logging.error(getExc(e))
        self.do__prompt(self.prompt_disp)

    def do__prompt(self, line):
        progress.querying = False
        line = self.parser(line)
        if not line:
            return
        """Modify prompts"""
        self.prompt_disp = line
        self.prompt = time_now_format(line)

    def do__font_color(self, line):
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
                self.do__prompt(self.prompt_disp)
        except Exception as e:
            logging.error(getExc(e))
        else:
            self.apply_color()
        self.do__prompt(self.prompt_disp)
    
    @error_handler()
    def do__background_color(self, line):
        """Sets background-color"""
        self.bcolor_dict[line.lower()]
        args.background_color = line.lower()
        self.apply_color()
        self.do__prompt(self.prompt_disp)
    
    @error_handler()
    def do__save(self, line):
        if gpt4:
            all = (
                "engine",
                "session",
                "api_key",
                "system_prompt",
                "max_tokens",
                "temperature",
                "top_p",
                "presence_penalty",
                "frequency_penalty",
                "reply_count",
                )
            chatbot.save(join_list(line), *all)
        else:
            chatbot.save_conversation(join_list(line))
        self.do__prompt(self.prompt_disp)
    
    @error_handler()
    def do__load(self, line):
        if gpt4:
            chatbot.load(join_list(line))
        else:
            chatbot.load_conversation(join_list(line))
        self.do__prompt(self.prompt_disp)
    
    @error_handler()
    def do__rollback(self, line):
        if line.isdigit():
            chatbot.rollback(int(line))
        self.do__prompt(self.prompt_disp)
    
    @error_handler()
    def do__reset(self, line):
        if any([args.bard,'--bard' in line]) and not '--gpt4' in line:
            self.bard.reset()
            chat_gpt = 'Bard'
        else:
            if gpt4:
                chatbot.reset(system_prompt=args.system_prompt)
            else:
                chatbot.reset()
            chat_gpt = 'GPT'
        logging.info(f'Chat reset successfully - {chat_gpt}')
        self.do__prompt(self.prompt_disp)

    def do__help(self, line):
        from .helper import help

        rich_print(
            Panel(Markdown(help),title='Help Info')
            )
        self.do__prompt(self.prompt_disp)

    def do__exit(self, line):
        return True


def get_api_key() -> str:
    """Gets API from Key_path or args.key"""
    if any([args.key, environ.get("OPENAI_API_KEY")]):
        return args.key or environ.get("OPENAI_API_KEY")
    if args.key_path:
        try:
            with open(args.key_path, encoding="utf-8") as fh:
                return fh.readlines()[0].replace("\n", "")
        except Exception as e:
            exit(logging.critical("While opening Key_Path " + getExc(e)))


def intro_train(
    error_msg: str = "Initializing default configurations - Kindly Wait",
) -> None:
    prompt_dict = intro_prompt_handler().main(args.file_path or None)
    args.__setattr__("role", "User")
    args.message = (
        " ".join(args.message) if isinstance(args.message, list) else args.message
    )
    keys = list(prompt_dict.keys())

    def show_role():
        info = Panel(
            args.message,
            title=args.role,
            style=Style(
                color=args.input_color if args.input_color != "reset" else "yellow",
                frame=True,
            ),
        )
        rich_print(info)
        logging.info("Initializing Chat - Kindly Wait")

    if str(args.message).isdigit() and (len(keys) - 1) >= int(args.message):
        try:
            role = keys[int(args.message)]
            args.message = prompt_dict[role]
            args.role = role
            if not args.zero_show:
                show_role()
            return True
        except KeyError:
            logging.warning(error_msg)

    elif args.message in keys:
        try:
            role = args.message
            args.message = prompt_dict[args.message]
            args.role = role
            if not args.zero_show:
                show_role()
            return True
        except KeyError:
            logging.warning(error_msg)
    else:
        logging.warning(error_msg)
    del prompt_dict, keys


@error_handler()
def main():
    global chatbot, gpt4, record_keeper
    args.disable_stream = True if args.markdown else args.disable_stream
    record_keeper = tracker(args.output)
    args.api_key = get_api_key()
    predefined_prompt_used = intro_train()
    openai.api_key = args.api_key
    try:
        if args.gpt in ("4"):
            from revChatGPT.V3 import Chatbot

            gpt4 = True
            chatbot = Chatbot(
                api_key=args.api_key,
                engine=args.model
                if args.model in config_h.v4models
                else "gpt-3.5-turbo",
                # timeout=args.timeout, #Available as from revChatGPT>=4.0.6.1
                proxy=args.proxy,  #
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                presence_penalty=args.presence_frequency,
                frequency_penalty=args.frequency_penalty,
                reply_count=args.reply_count,
                system_prompt=args.system_prompt
                if args.system_prompt is str
                else " ".join(args.system_prompt),
            )
        else:
            gpt4 = False
            from revChatGPT.V0 import Chatbot

            chatbot = Chatbot(api_key=args.api_key, engine=args.model, proxy=args.proxy)
    except Exception as e:
        exit(logging.critical(getExc(e)))

    try:
        if args.new_record and path.isfile(args.output):
            remove(args.output)
        run = main_gpt()
        if args.message:
            prompt = (
                " ".join(run.parser(args.message))
                if args.message is list
                else args.message
            )
            if args.bard:
                run.do_bard(prompt)
            else:
                run.default(prompt)
        run.cmdloop()
    except (KeyboardInterrupt, EOFError):
        progress.querying = False
        exit(logging.info("Stopping program"))
    except Exception as e:
        progress.querying = False
        logging.error(getExc(e))


if __name__ == "__main__":
    main()
