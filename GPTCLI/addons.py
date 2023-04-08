import re
from os import remove, system
from time import sleep
from . import logging, getExc
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
                commands.insert(0,st.replace(inter,''))
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


if __name__ == "__main__":
    st = file_parser("I want youn to debug this python code {f.test.py}")
    print(st.parse)
