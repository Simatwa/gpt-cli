import re
from . import logging, getExc

class file_parser:
    def __init__(self,prompt):
        self.prompt=prompt
    def get_match(self):
        matches = re.findall("{[f]\.(\w+((\.\w+)|(\b))*)}",self.prompt,flags=re.IGNORECASE)
        return [match[0] for match in matches]
    def get_file_content(self,file_path:str) -> str:
        with open(file_path) as fh:
            return fh.read()
    def parse(self):
        """Replace all filepaths with their contents"""
        try:
            for file_path in self.get_match():
               self.prompt = self.prompt.replace(f"{{f.{file_path}}}",'\n'+self.get_file_content(file_path))
        except Exception as e:
            logging.error(getExc(e))
            return
        else:
            return self.prompt

if __name__=="__main__":
    st=file_parser("I want youn to debug this python code {f.test.py}")
    print(st.parse())
