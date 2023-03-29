from setuptools import setup
from GPTCLI import __version__,__author__,__repo__

def get_file(fnm:str,lst:bool=False):
    with open(fnm) as fh:
        if lst:
            return fh.readlines()
        return fh.read()

setup(
    name="chatgpt4-cli",
    packages=["GPTCLI"],
    version=__version__,
    license="MIT",
    author=__author__,
    maintainer=__author__,
    author_email="smartwacaleb@gmail.com",
    description="Terminal for ChatGPT",
    url=__repo__,
    project_urls={"Bug Report": f"{__repo__}/issues/new"},
    install_requires=get_file('requirements.txt',True),
    long_description=get_file('README.md'),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        'console_scripts':[
            ('gpt-cli = GPTCLI.gptcli:main'),
            ('gpt-cli-image = GPTCLI.image:main'),
            ('gpt-cli-emage = GPTCLI.emage:main'),
        ]
    }
)