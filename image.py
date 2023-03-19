import openai
import argparse
from os import path
import logging

logging.basicConfig(
    format="%(levelname)s - %(message)s : %(asctime)s",
    datefmt="%d-%b-%Y %H:%M:%S",
    level=logging.INFO,
)


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
        parser = argparse.ArgumentParser(description="Text-to-Image Generator")
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
                    ">>Downloading image",
                    f"[{self.urls.index(link) + 1}]",
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


if __name__ == "__main__":
    from sys import argv

    cmd = [
        "Guy wearing Fawkes mask in a very palatial place with a nice coding-setup, programming in python. Display the codes",
        "-n",
        "2",
    ]
    start = imager(argv[1:])
    # start = imager(cmd)
    # print(start.main())
