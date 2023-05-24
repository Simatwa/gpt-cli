<h1 align="center">gpt-cli</h1>
<p align="center">
<a href="https://github.com/Simatwa/gpt-cli"><img src="https://img.shields.io/static/v1?logo=Github&label=Github&message=Passing&color=lime" alt="Gihtub"/></a>
<a href="https://pypi.org/project/chatgpt4-cli/"><img src="https://img.shields.io/static/v1?label=Pypi&message=v1.5.7&color=green&logo=pypi" alt="Pypi"/>
<a href="https://wakatime.com/badge/github/Simatwa/gpt-cli"><img src="https://wakatime.com/badge/github/Simatwa/gpt-cli.svg" alt="wakatime"/></a>
<a href="#"><img src="https://img.shields.io/static/v1?label=License&message=MIT&color=green&logo=MIT" alt="license"/></a>
<a href="#"><img src="https://img.shields.io/static/v1?label=Development&message=Beta&color=Orange&logo=progress" alt="Progress"/></a>
<a href="#"><img src="https://img.shields.io/static/v1?label=Code Style&message=Black&color=black&logo=Black" alt="Code-style"/></a>
<a href="#"><img src="https://img.shields.io/static/v1?label=Coverage&message=80%&color=green" alt="Coverage"/></a>
<a href="https://pepy.tech/project/chatgpt4-cli"><img src="https://static.pepy.tech/badge/chatgpt4-cli" alt="Downloads"/></a>
</p>

CLI tool for interacting with [ChatGPT](https://openai.com) and [Bard](https://bard.google.com).
> Generate images with BingImageCreator and ChatGPT's DALL-E models.

![screenshot](https://github.com/Simatwa/gpt-cli/raw/main/assets/Screenshot1.png)

### Features

- Chat with ChatGPT and Bard conversationally.
- Let **ChatGPT** and **Bard** chat to each other.
- Generate Images (DALL-E & BingImageCreator)- Based on your prompt or GPT generated description.
- Stream or Non-stream responses.
- Maintain record of the chats.
- Parse [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) easily.
- Fully customizable Commandline Interface.
- Interact with system commands on the fly.

### Prerequisites

- [x] [OPENAI_API_KEY](https://platform.openai.com/account/api-keys)

- [x] [Bard Cookies](https://bard.google.com)

- [x] [Bing cookies](https://bing.com) - *optional*

## Installation

Either of the following ways will get you ready.

1. Using pip

- From pypi

```sh
sudo pip install chatgpt4-cli
```

- Installing from source

```sh
 sudo pip install git+https://github.com/Simatwa/gpt-cli.git
 ```

2. Cloning locally and install

```sh
git clone https://github.com/Simatwa/gpt-cli.git
cd gpt-cli
pip install .
 #or
sudo pip install .
```

## Usage 

- Make OPENAI_API_KEY an environment variable.

`$ export OPENAI_API_KEY=<openai-api-key>`

After that you can launch the script with or without a prompt

> For instance :
```sh 
    #Without a prompt
   $ gpt-cli 
    # With a prompt 
   $ gpt-cli Write a conversation between Sun and Pluto.`
```

- Parsing OPENAI_API_KEY as one of the arguments

Run `$ gpt-cli -k <openai-api-key> <Your query>` at the terminal.

> For instance :

```sh
$ gpt-cli -k xxxxxxxxxxxxxxxxxx How to scan for SMB vulnerability using NMAP?
```

The [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) can be parsed to the script through the following ways:

- Specifying the role - (*case-sensitive*)

    e.g `$ gpt-cli UX/UI Developer`

- Specifying the index of the prompt:

    e.g `$ gpt-cli 29`

Run `$ gpt-cli --dump show` to view the act,prompt and their **indexes**

You can as well generate images using EdgeGPT (DALL-E) or ChatGPT independent of `gpt-cli`, uninteractively at the terminal:

1. EdgeGPT 

```sh
$ gpt-cli-emage --cookie-file <path> <Your prompt>
```  
- Visit [EdgeGPT](https://github.com/acheong08/EdgeGPT#requirements) to learn more on how to get the cookies.

2. ChatGPT 

```sh
  # Make OPENAI_API_KEY environment variable
  $ gpt-cli-image <Your Prompt>
```

For more info run `$gpt-cli-image -h` or `$gpt-cli-emage -h`.

## Highlight
<details>
<summary>
<table>
<thead>
<tr><th style="text-align: right;">  No.</th><th>Command          </th><th>Action                                     </th></tr>
</thead>
<tbody>
<tr><td style="text-align: right;">    0</td><td>./{command}      </td><td>Run command against system                 </td></tr>
<tr><td style="text-align: right;">    1</td><td>img              </td><td>Generate image ChatGPT based on prompt     </td></tr>
<tr><td style="text-align: right;">    2</td><td>emg              </td><td>Generate image with EdgeGPT based on prompt</td></tr>
<tr><td style="text-align: right;">    3</td><td>txt2img          </td><td>Generate image based on GPT description    </td></tr>
<tr><td style="text-align: right;">    4</td><td>_font_color      </td><td>Modify font-color                          </td></tr>
<tr><td style="text-align: right;">    5</td><td>_background_color</td><td>Modify background_color                    </td></tr>
<tr><td style="text-align: right;">    6</td><td>_prompt          </td><td>Modify terminal prompt                     </td></tr>
<tr><td style="text-align: right;">    7</td><td>_save            </td><td>Save current configurations to `.json` file</td></tr>
<tr><td style="text-align: right;">    8</td><td>_load            </td><td>Load configurations from file              </td></tr>
<tr><td style="text-align: right;">    9</td><td>_rollback        </td><td>Rollback Chat by {n} times                 </td></tr>
<tr><td style="text-align: right;">   10</td><td>_reset           </td><td>Reset current chat and start new           </td></tr>
<tr><td style="text-align: right;">   11</td><td>_help            </td><td>Show this help info                        </td></tr>
<tr><td style="text-align: right;">   12</td><td>{Any Other}      </td><td>Chat with ChatGPT                          </td></tr>
</tbody>
</table>
</summary>

1.img : Text-to-Image converter - ChatGPT
 - e.g ```img Toddler cartoon coding in Python```

2.emg : Text-to-Image converter - EdgeGPT
 - e.g ```emg Toddler cartoon coding in Python```

3.txt2img : Generate image based on GPT description
 - e.g ```txt2img Describe phenotype anatomy of ancient dinosaurs```

4._font_color : modifies font-color
 - e.g ```font_color input red```

5._background_color : modifies background_color
 - e.g ```background_color cyan```

6._prompt : Modify CMD prompt
 - e.g ```prompt ┌─[Smartwa@GPT-CLI]─(%H:%M:%S)```

7._load : Load configurations from the json file
 - e.g ```load DAN.json```

8._save : Save the current Chat Configurations
 - e.g ```save DAN.json```

9._rollback : Rollback the Chat by the {n} time(s)
 - e.g ```_rollback 2```

10._reset : Reset current chat and start new
 - e.g ```_reset Chat as if you are a 10 year old child```

11.bard : Specifies to use bard GPT
 - e.g ```bard Explain the composite concept in business```

12.gpt4 : Specifies to use ChatGPT in case `--bard` was made default
 - e.g ```gpt4 How do you make?```

13._help : Show this help info

* Use  `./` (fullstop and forward slash) to interact with **system commands**
 - e.g ```./ifconfig```

 * Use `_botchat` to let the 2 GPTs chat to each other

> **Note** You can further specify the GPT to be used by appending `--gpt4` or `--bard` in the prompt.

* Use *{{f.text-filename}}* to issue prompt contained in the 'text-filename'

</details>

<details>

<summary>

For more info run `gpt-cli -h`.

</summary>

```
╭─────────────────────────────── gpt-cli v1.5.3 ───────────────────────────────╮
│                                                                              │
│             Repo : https://github.com/Simatwa/gpt-cli                        │
│             By   : Smartwa Caleb                                             │
╰──────────────────────────────────────────────────────────────────────────────╯
usage: gpt-cli [-h] [-v] [-m gpt-3.5-turbo|gpt-4|gpt-4-32k] [-t [0.1-1]]
               [-mt [1-7000]] [-tp [0.1-1]] [-f [0.1-2]] [-p [0.1-2]] [-k KEY]
               [-kp path] [-ic [cyan|green|yellow|red]]
               [-oc [cyan|green|yellow|red]] [-bc [blue,magenta,black,reset]]
               [-pc [cyan|green|yellow|red]] [--prompt [SETTINGS ...]]
               [-tm value] [-pr PROXY] [-rc value] [-g 1,4] [-sp [text ...]]
               [-fp path] [-o path] [-pp prefix] [-rp prefix]
               [-dm keys|values|show|{fnm}] [-dl symbol] [-cf path] [-bk KEY]
               [-bkp PATH] [-bcf PATH] [-si TIME] [-spin 1|2]
               [--disable-stream] [--new-record] [--disable-recording]
               [--zero-show] [--bard] [--markdown] [--update] [--sudo]
               [message ...]

Interact with ChatGPT and Bard at the terminal.

positional arguments:
  message               Message to be send.

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -m gpt-3.5-turbo|gpt-4|gpt-4-32k, --model gpt-3.5-turbo|gpt-4|gpt-4-32k
                        ChatGPT model to be used
  -t [0.1-1], --temperature [0.1-1]
                        Charge of the generated text's randomness
  -mt [1-7000], --max-tokens [1-7000]
                        Maximum number of tokens to be generated upon
                        completion
  -tp [0.1-1], --top-p [0.1-1]
                        Sampling threshold during inference time
  -f [0.1-2], --frequency-penalty [0.1-2]
                        Chances of word being repeated
  -p [0.1-2], --presence-frequency [0.1-2]
                        Chances of topic being repeated
  -k KEY, --key KEY     OPENAI-API-KEY
  -kp path, --key-path path
                        Path to text-file containing GPT-api key
  -ic [cyan|green|yellow|red], --input-color [cyan|green|yellow|red]
                        Font color for inputs
  -oc [cyan|green|yellow|red], --output-color [cyan|green|yellow|red]
                        Font color for outputs
  -bc [blue,magenta,black,reset], --background-color [blue,magenta,black,reset]
                        Console's background-color
  -pc [cyan|green|yellow|red], --prompt-color [cyan|green|yellow|red]
                        Prompt's display color
  --prompt [SETTINGS ...]
                        Customizes the prompt display
  -tm value, --timeout value
                        Request timeout while making request - (Soon)
  -pr PROXY, --proxy PROXY
                        Pivot request through this proxy
  -rc value, --reply-count value
                        Number of responses to be received
  -g 1,4, --gpt 1,4     ChatGPT version to be used
  -sp [text ...], --system-prompt [text ...]
                        Text to train ChatGPT at the start
  -fp path, --file-path path
                        Path to .csv file containing role and prompt -
                        [act,prompt]
  -o path, --output path
                        Filepath for saving the chats - default
                        [/home/smartwa/git/gpt-cli/.chatgpt-history.txt]
  -pp prefix, --prompt-prefix prefix
                        Text to append before saving each prompt - default
                        [>>> timestamp]
  -rp prefix, --response-prefix prefix
                        Text to append before saving each response - default
                        [None]
  -dm keys|values|show|{fnm}, --dump keys|values|show|{fnm}
                        Stdout [keys,values]; Save all prompts in json format
                        to a file
  -dl symbol, --delimiter symbol
                        Delimeter for the .CSV file - [act,prompt]
  -cf path, --cookie-file path
                        Path to Bing's cookies - for Edge Image Generation
  -bk KEY, --bard-key KEY
                        Bard's session value
  -bkp PATH, --bard-key-path PATH
                        Path to Bard's key path
  -bcf PATH, --bard-cookie-file PATH
                        Path to Bard's cookie file
  -si TIME, --stream-interval TIME
                        Interval for printing responses in (s)
  -spin 1|2, --spinner 1|2
                        Busy bar indicator
  --disable-stream      Specifies not to stream responses from ChatGPT
  --new-record          Override previous chats under the filepath
  --disable-recording   Disable saving prompts and responses
  --zero-show           Specifies not to stdout prompt of the act parsed
  --bard                Make Bard the default GPT
  --markdown            Stdout responses in markdown-format - disables
                        streaming
  --update              Download latest prompts - [awesome-chatgpt-prompts]
  --sudo                Run commands against system with sudo privileges

```

</details>

> **Note** : **gpt-4** *(model)* supports upto *7000* tokens and others *3000*.

> `$ gpt-cli --dump pdf` will generate `all-acts.pdf` file containing latest acts and prompts as shown [here](https://chatgpt-prompts.tiiny.site). 

Visit [acheong08/Bard](https://github.com/acheong08/Bard) for info on how to get the Bard's cookie file and Sessions.

## Motive

<details>

<summary>

Love for `Terminal` ❤️

</summary>

As a `terminal guy` I used to find it uncomfortable to keep shifting from one window to next in order to access ChatGPT even after trying out the [gpt-login](https://github.com/Simatwa/gpt-login), the rest is [here.](https://github.com/Simatwa/gpt-cli)
</details>

## Contributions

- Anyone is free to [fork](https://github.com/Simatwa/gpt-cli/fork), submit an [issue](https://github.com/Simatwa/gpt-cli/issues) without any **guideline** or submitting a [pull request](https://github.com/Simatwa/gpt-cli/pulls).

### ToDo

- [x] Use dialogue
- [x] Issue prompt from a file
- [x] Busy bar
- [ ] Add prompts to the [prompts.csv](https://github.com/Simatwa/gpt-cli/edit/main/assets/prompts.csv)

  > Review [CHANGELOG](https://github.com/Simatwa/gpt-cli/blob/main/docs/CHANGELOG.md)

## Acknowledgements

1. [remo7777](https://github.com/remo7777/T-Header)

2. [acheong08](https://github.com/acheong08/ChatGPT)

3. [f](https://github.com/f/awesome-chatgpt-prompts)

> **Note** Consider supporting this project by purchasing [Prompts for ChatGPT and Bard](https://payhip.com/b/zxQM0) ebook.
