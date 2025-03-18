# DEPENDENCIES: Python 3.4, tomlkit, questionary, rich, pyfiglet

from rich import print
import subprocess             # run console comands
from pathlib import Path      # ↓ (line 3)
home = Path.home()            # path to USERHOME
import questionary            # interactive terminal option selection
from tomlkit import document  # create TOML 'files'
from tomlkit import dumps     # convert output of 'document' to a string
from tomlkit import parse     # parse TOML files
import os
import pyfiglet               # title text

import getopt, sys            # option parser
argumentList = sys.argv[1:]
options = "c"
long_options = ["config"]
arguments, values = getopt.getopt(argumentList, options, long_options)

title = pyfiglet.figlet_format("komo-launch", font="smkeyboard", justify="center")

customStyle = questionary.Style([
    ('qmark', 'fg:#eb6f92'),
    ('answer', 'fg:#eb6f92')
])

def configure():
    global bar
    global whkd
    global masir

    bar = questionary.select(
        "what bar do you use?", 
        choices=['YASB', 'Zebar', 'komorebi-bar'],
        style=customStyle,
        qmark='🍉'
        ).ask()
    whkd = questionary.confirm(
        "do you use whkd?",
        style=customStyle,
        qmark='🍉'
        ).ask()
    masir = questionary.confirm(
        "do you use masir?",
        style=customStyle,
        qmark='🍉'
        ).ask()

    tomlFile = document()
    tomlFile.add("bar", bar)
    tomlFile.add("whkd", whkd)
    tomlFile.add("masir", masir)
    configFile = open(home / "komo-launch.toml", "w")
    configFile.write(dumps(tomlFile))
    configFile.close()

barCommand = []
komorebiCommand = []

def buildCommand():
    global barCommand
    global komorebiCommand
    global ParsedFile
    ParsedFile = parse(open(home / "komo-launch.toml").read())
    komorebiCommand = ["komorebic", "start"]
    if ParsedFile["whkd"] == True:
        komorebiCommand.append("--whkd")
    if ParsedFile["masir"] == True:
        komorebiCommand.append("--masir")
    if ParsedFile["bar"] == "komorebi-bar":
        komorebiCommand.append("--bar")
    if ParsedFile["bar"] == "Zebar":
        barCommand = ["zebar"]
    if ParsedFile["bar"] == "YASB":
        barCommand = ["yasbc", "start"]


def start():
    buildCommand()
    print("Starting [bold red]Komorebi...")
    subprocess.call(komorebiCommand, 
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT)
    if barCommand:
        print(f'Starting [bold red]{ParsedFile["bar"]}...')
        subprocess.call(barCommand, 
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT)
    print("[bold red]DONE!\n")

try:
    configFile = open(home / "komo-launch.toml")
except:
    configFile = open(home / "komo-launch.toml", "x")
    print("\n", f'[bold red]{title}')
    configure()
    print("")
    start()
else:
    print("\n", f'[bold red]{title}')
    for currentArgument, currentValue in arguments:    
        if currentArgument in ("-c", "--config"):
            configure()
            print("")
    start()