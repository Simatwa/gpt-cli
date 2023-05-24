from . import __version__, __repo__

from os import getlogin

help = f"""

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
│     7 │ _save             │ Save current configurations to '.json' file │
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

1.  `img` : Text-to-Image converter - *(EXPERIMENTAL)*
    e.g *img Toddler cartoon coding in Python*

2.  `txt2img` : Generate image based on GPT description
    e.g *txt2img Describe phenotype anatomy of ancient dinosaurs*

3. `_font_color` : modifies font-color
    e.g *font_color input red*

4. `_background_color` : modifies background_color
    e.g *background_color cyan*

5. `_prompt` : Modify CMD prompt
    e.g *_prompt ┌─[{getlogin().capitalize()}@ChatGPT4]─(%H:%M:%S)*

6. `_load` : Load configurations from the json file
    e.g *_load DAN.json*

7. `_save` : Save the current Chat Configurations
    e.g *_load DAN.json*

8. `_rollback` : Rollback the Chat by  {{n}} time(s)
    e.g *_rollback 2*

9. `_reset` : Reset current chat and start new
    e.g *_reset Chat as if you are a 10 year old child*

11. `bard` : Specifies to use bard GPT
    e.g *bard Explain the composite concept in business.*

12. `gpt4` : Specifies to use ChatGPT in case `--bard` was made default
    e.g *gpt4 How do you make?*

13. `_help` : Show this help info

* You can further specify the GPT to be used by appending `--gpt4` or `--bard` in the prompt.

* Use `_botchat` to let the 2 GPTs chat to each other

* Use double `./` (fullstop and foward slash) to interact with system commands
      e.g *./ifconfig*
      
* Use `{{f.text-filename}}` to issue prompt contained in  the 'text-filename'

* Use `CTRL+C` to cancel a request 

* `_exit` or `CTRL+C` or `CTRL+Z` : Quits the program.
        """
