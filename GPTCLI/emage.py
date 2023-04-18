import json
import os
import time
import urllib

import regex
import requests
from . import logging, getExc
from .image import imager

BING_URL = "https://www.bing.com"


class ImageGen:
    """
    Image generation by Microsoft Bing
    Parameters:
        auth_cookie: str
    """

    def __init__(self, auth_cookie: str) -> None:
        self.session: requests.Session = requests.Session()
        self.session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "referrer": "https://www.bing.com/images/create/",
            "origin": "https://www.bing.com",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
        }
        self.session.cookies.set("_U", auth_cookie)

    def get_images(self, prompt: str) -> list:
        """
        Fetches image links from Bing
        Parameters:
            prompt: str
        """
        print(">[*] Sending request...", end="\r")
        url_encoded_prompt = urllib.parse.quote(prompt)
        # https://www.bing.com/images/create?q=<PROMPT>&rt=3&FORM=GENCRE
        url = f"{BING_URL}/images/create?q={url_encoded_prompt}&rt=4&FORM=GENCRE"
        response = self.session.post(url, allow_redirects=False)
        if response.status_code != 302:
            # if rt4 fails, try rt3
            url = f"{BING_URL}/images/create?q={url_encoded_prompt}&rt=3&FORM=GENCRE"
            response3 = self.session.post(url, allow_redirects=False, timeout=200)
            if response3.status_code != 302:
                logging.error(response3.text)
            response = response3
        # Get redirect URL
        redirect_url = response.headers["Location"].replace("&nfy=1", "")
        request_id = redirect_url.split("id=")[-1]
        self.session.get(f"{BING_URL}{redirect_url}")
        # https://www.bing.com/images/create/async/results/{ID}?q={PROMPT}
        polling_url = f"{BING_URL}/images/create/async/results/{request_id}?q={url_encoded_prompt}"
        # Poll for results
        print(">[*] Waiting for results...", end="\r")
        start_wait = time.time()
        while True:
            if int(time.time() - start_wait) > 300:
                raise Exception("Timeout error")
            # print(".", end="", flush=True)
            response = self.session.get(polling_url)
            if response.status_code != 200:
                raise Exception("Could not get results")
            if response.text == "":
                time.sleep(1)
                continue
            else:
                break

        # Use regex to search for src=""
        image_links = regex.findall(r'src="([^"]+)"', response.text)
        # Remove size limit
        normal_image_links = [link.split("?w=")[0] for link in image_links]
        # Remove duplicates
        return list(set(normal_image_links))

    def save_images(self, links: list, output_dir: str) -> None:
        """
        Saves images to output directory
        """
        print("\n>[*] Downloading images...", end="\r")
        try:
            os.makedirs(output_dir)
        except FileExistsError:
            pass
        image_num = 0
        try:
            for link in links:
                with self.session.get(link, stream=True) as response:
                    # save response to file
                    response.raise_for_status()
                    with open(f"{output_dir}/{image_num}.jpg", "wb") as output_file:
                        for chunk in response.iter_content(chunk_size=8192):
                            output_file.write(chunk)

                image_num += 1
        except requests.exceptions.MissingSchema as url_exception:
            raise Exception(
                "Inappropriate contents found in the generated images. Please try again or try another prompt."
            ) from url_exception


class emager:
    """Receives args and controls the image gen process"""

    def __init__(self, args: object):
        self.args = args
        self.urls = []

    def main(self):
        # prompt,file,number,size,dir,output, dir, url
        try:
            if self.args.file:
                self.get_prompt_from_file()
            auth = self.get_U()
            if not auth:
                return logging.error("Unable to find auth from cookie")
            imageGen = ImageGen(auth)
            urls = imageGen.get_images(self.args.prompt)
            if isinstance(urls, list):
                self.urls.extend(urls)
                img_handler = imager.image_saver(self.args, urls, imageGen.session)
            else:
                logging.error(f"Failed to get image urls - {urls}")
            if img_handler.save():
                """Recurse the function to meet total number of args"""
                logging.debug("Recursing main function in emager")
                return self.main()
        except Exception as e:
            logging.error(getExc(e))

    def get_prompt_from_file(self):
        try:
            with open(self.args.cookie_file) as fh:
                self.args.prompt = fh.read()
        except Exception as e:
            logging.error("Failed to load prompt from file -" + getExc(e))

    def get_U(self):
        try:
            with open(self.args.cookie_file, encoding="utf-8") as file:
                cookie_json = json.load(file)
                for cookie in cookie_json:
                    if cookie.get("name") == "_U":
                        return cookie.get("value")
        except Exception as e:
            logging.error(getExc(e))


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Text-To-Image Converter - EdgeGPT (DALL-E)"
    )
    parser.add_argument(
        "prompt", help="Prompt to generate images for", type=str, nargs="+"
    )
    parser.add_argument(
        "-U", "--auth", metavar="AUTH", help="Auth cookie from browser", type=str
    )
    parser.add_argument(
        "-cf",
        "--cookie-file",
        metavar="PATH",
        help="File containing auth cookie",
        type=str,
    )
    parser.add_argument(
        "-d",
        "--dir",
        dest="output_dir",
        help="Output directory",
        metavar="PATH",
        type=str,
        default=os.path.join(os.path.expanduser("~"), "Downloads/GPT"),
    )
    args = parser.parse_args()
    # Load auth cookie
    with open(args.cookie_file, encoding="utf-8") as file:
        cookie_json = json.load(file)
        for cookie in cookie_json:
            if cookie.get("name") == "_U":
                args.U = cookie.get("value")
                break

    if args.U is None:
        raise Exception("Could not find auth cookie")

    # Create image generator
    image_generator = ImageGen(args.U)
    image_generator.save_images(
        image_generator.get_images(" ".join(args.prompt)),
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(getExc(e))
