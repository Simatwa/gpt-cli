#!/usr/bin/python
__version__ = "1.1.0"
__author__ = "Smartwa Caleb"
from colorama import Fore, Back
from os import getlogin, getcwd, path
import argparse


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
        parser.add_argument(
            "-o",
            "--output",
            help="Filepath for saving the chats - default [$PWD/GPT-CLI-convo.txt]",
            default=path.join(getcwd(), "GPT-CLI-convo.txt"),
        )
        parser.add_argument(
            "-pp",
            "--prompt-prefix",
            help="Text to append before saving each prompt - default [>>timestamp]",
            dest="prompt_prefix",
            metavar="prefix",
            default=">>(%d-%b %H:%M:%S) : ",
        )
        parser.add_argument(
            "-rp",
            "--response-prefix",
            help="Text to append before saving each response - default [None]",
            dest="response_prefix",
            metavar="prefix",
            default="",
        )
        parser.add_argument(
            "--new-record",
            help="Override previous chats under the filepath",
            action="store_true",
            dest="new_record",
        )
        parser.add_argument(
            "--disable-recording",
            dest="disable_recording",
            help="Disable saving prompts and responses",
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
from sys import exit, stderr
import openai
import json
import cmd
from re import sub
from datetime import datetime
from os import system, remove, path
from threading import Thread as thr

date_stamp = lambda text: datetime.today().strftime(text)


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

    (c). img : Text-to-Image converter - (EXPERIMENTAL)
          e.g 'img Toddler cartoon coding in Python'
    (d). txt2img : Generate image based on GPT description
          e.g 'txt2img Describe phenotype anatomy of ancient dinosaur'
          

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
    f"{config_h.color_dict[args.prompt_color]}{date_stamp(v)}{config_h.color_dict[args.input_color]}\r\n└──╼ ❯❯❯"
)


class tracker:
    """Keeps track of the prompts & responses"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.feedback = None
        self.failed_to_record = False

    def save_record(self) -> None:
        """Writes the prompt and response in a file"""
        info_to_write = f"\n\n{date_stamp(args.prompt_prefix)}{args.message}\n\n{date_stamp(args.response_prefix)}{self.feedback}"
        try:
            with open(self.filepath, "a") as fp:
                fp.write(info_to_write)
        except Exception as e:
            logging.error(f"Failed to keep record - {e}")
            self.failed_to_record = True

    def main(self, response: str) -> None:
        """Main method"""
        if any([self.failed_to_record, args.disable_recording]):
            return
        self.feedback = sub("\n", "", response, 1)
        thr(target=self.save_record).start()


### Imager


class imager:
    """Handles image generation"""

    def __init__(self, commands: list):
        self.args = self.get_args(commands)
        if type(self.args.prompt) is list:
            self.args.prompt = " ".join(self.args.prompt)
        self.image_buff = self.image_saver(self.args, [])

    def get_args(self, args):
        resolutions = ["256x256", "512x512", "1024x1024"]
        dir = path.join(path.expanduser("~"), "Downloads/GPT")
        parser = argparse.ArgumentParser(description="Text-to-Image Converter")
        parser.add_argument("prompt", help="Description of the image", nargs="*")
        parser.add_argument(
            "-f", "--file", help="Path to text-file containing the description"
        )
        parser.add_argument(
            "-n",
            "--number",
            help="Total images to be generated - def  [1]",
            type=int,
            default=1,
        )
        parser.add_argument(
            "-s",
            "--size",
            help="Image resolution (size) - def [512x512]",
            default="512x512",
            choices=resolutions,
            metavar="|".join(resolutions),
        )
        parser.add_argument("-o", "--output", help="Name for identifying the images")
        parser.add_argument(
            "-d",
            "--dir",
            help=f"Directory for saving the images - def [{dir}]",
            default=dir,
        )
        parser.add_argument(
            "--url", help="Get url for the images only, not images", action="store_true"
        )
        return parser.parse_args(args=args)

    def main(self) -> dict:
        if not self.args:
            return
        try:
            if not bool(self.args.prompt):
                if self.args.file:
                    with open(self.args.file) as fh:
                        self.args.prompt = fh.read()
                else:
                    print("[*] Kindly pass prompt or file-path to a text-file.")
                    return
            if type(self.args.prompt) is list:
                self.args.prompt = " ".join(self.args.prompt)
            print(">>[*] Generating image with GPT", end="\r")
            image_resp = openai.Image.create(
                prompt=self.args.prompt, n=self.args.number, size=self.args.size
            )
            resp = []
            for value in image_resp["data"]:
                resp.append(value["url"])

            self.image_buff.urls = resp
            self.image_buff.save()
            print("", end="\r")
            return {"api_resp": image_resp, "url": resp}

        except Exception as e:
            logging.error(str(e))

    class image_saver:
        """Receives urls, query and save the contents"""

        def __init__(self, args: object, urls: list):
            self.args = args
            self.urls = urls
            self.save_count = 0

        def write_buff(self, data):
            """Saves the image"""
            if not path.isdir(self.args.dir):
                from os import makedirs

                makedirs(self.args.dir)
            cpath = path.join(
                self.args.dir,
                f'{self.args.output}{self.save_count if self.save_count else ""}.png',
            )
            if path.isfile(cpath):
                self.save_count += 1
                return self.write_buff(data)

            with open(cpath, "wb") as fh:
                fh.write(data)
            self.save_count += 1

        def save(self):
            """Queries the image and saves it"""
            if self.args.url:
                return
            if not self.args.output:
                prompt = self.args.prompt.split(" ")
                self.args.output = (
                    "_".join(prompt[:4]) + "..."
                    if len(prompt) > 5
                    else "_".join(prompt)
                )
            from requests import get

            for link in self.urls:
                print(
                    ">>Downloading image" f"[{self.urls.index(link) + 1}]",
                    end="\r",
                )
                try:
                    resp = get(link, timeout=60)
                    if resp.status_code == 200:
                        self.write_buff(resp.content)
                    else:
                        logging.warning(
                            f">>Failed to download image - Code : {resp.status_code} - {resp.reason}"
                        )
                except Exception as e:
                    logging.error(str(e))


### Main class


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

    def default(self, raw, return_fb=False):
        if not bool(raw):
            return
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
                feedback = sub("\n\n", "\n", rp[1]["text"], 1)
                out(feedback)
                record_keeper.main(feedback)
                if return_fb:
                    return feedback.strip()
            else:
                logging.error(str(rp[1]))
        self.do_prompt(self.prompt_disp)

    def do_txt2img(self, line):
        """Generate images based on GPT description"""
        print(">>[*] Querying description from GPT", end="\r")
        imagiser = imager(line.split(" "))
        description = self.default(imagiser.args.prompt, return_fb=True).strip()
        if description:
            imagiser.args.prompt = description
            imagiser.main()

        else:
            logging.error("Failed to generate description.")

    def do_img(self, line):
        """Text-to-Image handler"""
        resp = imager(line.split(" ")).main()
        if isinstance(resp, dict):
            args.message = line
            record_keeper.main(str(resp["url"]))

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
            logging.exception(e)
        else:
            self.apply_color()

    def do_background_color(self, line):
        """Sets background-color"""

        try:
            self.bcolor_dict[line.lower()]
            args.background_color = line.lower()
            self.apply_color()
        except Exception as e:
            logging.exception(e)


if __name__ == "__main__":
    record_keeper = tracker(args.output)
    try:
        if args.new_record and path.isfile(args.output):
            remove(args.output)
        run = main_gpt()
        if args.message:
            run.default(" ".join(args.message))
        run.cmdloop()
    except (KeyboardInterrupt, EOFError):
        exit(logging.info("Stopping program"))
    except Exception as e:
        logging.exception(e)
