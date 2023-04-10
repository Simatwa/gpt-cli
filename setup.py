from setuptools import setup
from GPTCLI import __version__, __author__, __repo__

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
    install_requires=[
        "numpy>=1.23.4",
        "colorama>=0.4.6",
        "openai>=0.26.4",
        "revChatGPT==4.0.6",
        "appdirs>=1.4.4",
        "requests>=2.28.2",
        "tabulate>=0.9.0",
    ],
    long_description=open("README.md").read(),
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
        "console_scripts": [
            ("gpt-cli = GPTCLI.gptcli:main"),
            ("gpt-cli-image = GPTCLI.image:main"),
            ("gpt-cli-emage = GPTCLI.emage:main"),
        ]
    },
)
