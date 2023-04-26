import re
from os import remove, system
from time import sleep
from . import logging, getExc, __repo__, __author__, error_handler
from threading import Thread as thr
from sys import exit
from fpdf import FPDF
from json import loads
import requests
from datetime import datetime


class file_parser:
    """Handles contents from text file"""

    def __init__(self, prompt):
        self.prompt = prompt

    def get_match(self):
        matches = re.findall(
            "{[f]\.(\w+((\.\w+)|(\b))*)}", self.prompt, flags=re.IGNORECASE
        )
        return [match[0] for match in matches]

    def get_file_content(self, file_path: str) -> str:
        with open(file_path) as fh:
            return fh.read()

    def parse(self):
        """Replace all filepaths with their contents"""
        try:
            for file_path in self.get_match():
                self.prompt = self.prompt.replace(
                    f"{{f.{file_path}}}", "\n" + self.get_file_content(file_path)
                )
        except Exception as e:
            logging.error(getExc(e))
            return
        else:
            return self.prompt


class system_control:
    """Retrieves bash commands/script from response"""

    def __init__(self, prompt, interpreter: str = "bash", filename="gpt-run.sc"):
        self.prompt = prompt
        self.file_name = filename
        self.interpreter = interpreter
        self.all_interpreters = ["bash", "python", "java", "php", "node"]

    def get_interpreter(self, commands: list) -> list:
        st = commands[0]
        for inter in self.all_interpreters:
            if st.startswith(inter):
                commands.remove(st)
                commands.insert(0, st.replace(inter, ""))
                self.interpreter = inter
                break

        return list(set(commands))

    def get_command(self, raw: bool = False):
        """Extracts commands from raw text

        Args:
            raw (bool, optional): Remove newline or not. Defaults to False.

        Returns:
            str: commands to be run
        """
        commands = re.findall(r"```(.*?)```", self.prompt, re.DOTALL)
        if commands:
            if raw:
                resp = "".join(self.get_interpreter(commands))
            else:
                resp = []
                for cmd in commands:
                    resp.append(re.sub("\n", "", cmd))
                resp = ";".join(self.get_interpreter(resp))
        else:
            return ";".join(list(set(re.findall(r"`(.*?)`", self.prompt, re.DOTALL))))

        return resp

    def execute(self, sudo: bool = False):
        """Get commands and run them against system"""
        fnm = self.save(self.get_command(True))
        if fnm:
            print()
            cmd = (
                "sudo " + self.interpreter + " " + fnm
                if sudo
                else self.interpreter + " " + fnm
            )
            system(cmd)
            sleep(0.5)
            self.delete_file()

    def save(self, script: str):
        """Saves the bash script"""
        try:
            with open(self.file_name, "w") as fh:
                fh.write(script)
        except Exception as e:
            logging.error(getExc(e))
            return
        else:
            return self.file_name

    def delete_file(self):
        """Deletes the bash script file"""
        try:
            remove(self.file_name)
        except Exception as e:
            logging.error(getExc(e))


class progress:
    querying = None
    __spinner = (("-", "\\", "|", "/"), ("█■■■■", "■█■■■", "■■█■■", "■■■█■", "■■■■█"))
    sleep_time = 0.1

    @classmethod
    def __action(cls, index):
        while cls.querying:
            for spin in cls.__spinner[index]:
                print(" " + spin, end="\r", flush=True)
                if not cls.querying:
                    break
                sleep(cls.sleep_time)

    @classmethod
    def display_bar(cls, args):
        try:
            cls.querying = True
            t1 = thr(
                target=cls.__action,
                args=(args.spinner - 1,),
            )
            t1.start()
        except Exception as e:
            cls.querying = False
            logging.debug(getExc(e))

    @classmethod
    def stop_spinning(cls):
        """Stop displaying busy-bar"""
        if cls.querying:
            cls.querying = False
            sleep(cls.sleep_time)

    @classmethod
    def run(cls):
        """Handles GPT querying functions"""

        def decorator(func):
            def main(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except KeyboardInterrupt:
                    cls.stop_spinning()
                    return
                except EOFError:
                    cls.querying = False
                    exit(logging.info("Stopping program"))
                except Exception as e:
                    cls.stop_spinning()
                    logging.error(getExc(e))

            return main

        return decorator


class prompts_to_pdf:
    def __init__(self):
        self.contents = self.get_contents()
        self.pdf = FPDF()
        self.pdf.add_page()

    @error_handler()
    def get_contents(self):
        resp = requests.get(__repo__ + "/raw/main/assets/all-acts.json", timeout=15)
        if resp.ok:
            return loads(resp.text)
        raise Exception("Prompts NOT found in path.")

    @error_handler()
    def main(self) -> None:
        if not self.contents:
            return
        x = 0
        self.pdf.set_text_color(255, 0, 0)
        self.pdf.set_font("Helvetica", size=18)
        self.pdf.cell(
            0,
            10,
            "Prompts for ChatGPT and Bard",
            align="C",
        )
        self.pdf.ln()
        for key, value in self.contents.items():
            key = f"{x}. {key}"
            value = f"  {value}"
            self.pdf.set_text_color(0, 0, 255)
            self.pdf.set_font("Arial", size=14)
            text_width = self.pdf.get_string_width(key)
            self.pdf.set_x((210 - text_width) / 2)
            self.pdf.cell(0, 10, key)
            self.pdf.cell(0, 10, "")
            self.pdf.ln()
            self.pdf.set_x(0)
            self.pdf.set_font("Courier", size=12)
            self.pdf.set_text_color(0, 0, 128)
            self.pdf.multi_cell(0, 10, value.encode("utf-8").decode("latin-1"))
            x += 1
        self.pdf.ln()
        self.pdf.set_author(__author__)
        self.pdf.set_text_color(255, 0, 0)
        msg = "Click here to visit project's official repo."
        self.pdf.set_x((210 - self.pdf.get_string_width(msg)) / 2)
        self.pdf.add_link()
        self.pdf.cell(0, 10, msg, link=__repo__)

        self.pdf.ln()
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_x((210 - self.pdf.get_string_width(__repo__)) / 2)
        self.pdf.cell(0, 10, __repo__)
        self.pdf.ln()
        self.pdf.set_font('Symbol',size=8)
        time_stamp = f'Lastly auto-edited : {datetime.today().strftime("%d-%b-%Y %H:%M:%S %s")}'
        self.pdf.set_x((210 - self.pdf.get_string_width(time_stamp)) / 2)
        self.pdf.cell(0,10,time_stamp)
        self.pdf.output("all-acts.pdf")
        logging.info("Contents saved to 'all-acts.pdf'")


if __name__ == "__main__":
    st = file_parser("I want you to debug this python code {f.test.py}")
    print(st.parse)
