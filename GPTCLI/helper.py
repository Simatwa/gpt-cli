from . import __version__, __repo__

from os import getlogin

help = f"""
   gpt-cli {__version__}
 Repo : {__repo__}

╒═══════╤═══════════════════╤═════════════════════════════════════════════╕
│   No. │ Command           │ Action                                      │
╞═══════╪═══════════════════╪═════════════════════════════════════════════╡
│     0 │ ./{{command}}       │ Run command against system                  │
├───────┼───────────────────┼─────────────────────────────────────────────┤
│     1 │ img               │ Generate image ChatGPT based on prompt      │
├───────┼───────────────────┼─────────────────────────────────────────────┤
│     2 │ emg               │ Generate image with EdgeGPT based on prompt │
├───────┼───────────────────┼─────────────────────────────────────────────┤
│     3 │ txt2img           │ Generate image based on GPT description     │
├───────┼───────────────────┼─────────────────────────────────────────────┤
│     4 │ _font_color       │ Modify font-color                           │
├───────┼───────────────────┼─────────────────────────────────────────────┤
│     5 │ _background_color │ Modify background_color                     │
├───────┼───────────────────┼─────────────────────────────────────────────┤
│     6 │ _prompt           │ Modify terminal prompt                      │
├───────┼───────────────────┼─────────────────────────────────────────────┤
│     7 │ _save             │ Save current configurations to `.json` file │
├───────┼───────────────────┼─────────────────────────────────────────────┤
│     8 │ _load             │ Load configurations from file               │
├───────┼───────────────────┼─────────────────────────────────────────────┤
│     9 │ _rollback         │ Rollback Chat by {{n}} times                  │
├───────┼───────────────────┼─────────────────────────────────────────────┤
│    10 │ _reset            │ Reset current chat and start new            │
├───────┼───────────────────┼─────────────────────────────────────────────┤
│    11 │ _help             │ Show this help info                         │
├───────┼───────────────────┼─────────────────────────────────────────────┤
│    12 │ {{Any Other}}       │ Chat with ChatGPT                           │
╘═══════╧═══════════════════╧═════════════════════════════════════════════╛

1.  img : Text-to-Image converter - (EXPERIMENTAL)
    e.g 'img Toddler cartoon coding in Python'

2.  txt2img : Generate image based on GPT description
    e.g 'txt2img Describe phenotype anatomy of ancient dinosaurs'

3. _font_color : modifies font-color
    e.g 'font_color input red'

4. _background_color : modifies background_color
    e.g 'background_color cyan'

5. _prompt : Modify CMD prompt
    e.g '_prompt ┌─[{getlogin().capitalize()}@ChatGPT4]─(%H:%M:%S)

6. _load : Load configurations from the json file
    e.g '_load DAN.json'

7. _save : Save the current Chat Configurations
    e.g '_load DAN.json'

8. _rollback : Rollback the Chat by  {{n}} time(s)
    e.g '_rollback 2'

9. _reset : Reset current chat and start new
    e.g '_reset Chat as if you are a 10 year old child'

10. _help : Show this help info

* Use double `./` (fullstop and foward slash) to interact with system commands
      e.g './ifconfig'
* Use {{f.text-filename}} to issue prompt contained in  the 'text-filename'

* _exit or `CTRL+C` : Quits the program.
        """
