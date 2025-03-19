# DEPENDENCIES: Python 3.4, tomlkit, questionary, rich, pyfiglet

from rich.align import Align
from rich import print
import subprocess             # run console comands
from pathlib import Path      # ↓ (line 3)
home = Path.home()            # path to USERHOME
import questionary            # interactive terminal option selection
from tomlkit import document  # create TOML 'files'
from tomlkit import dumps     # convert output of 'document' to a string
from tomlkit import parse     # parse TOML files
import os

import getopt, sys            # option parser
argumentList = sys.argv[1:]
options = "chv"
long_options = ["config", "help", "verbose"]
arguments, values = getopt.getopt(argumentList, options, long_options)

argConfig = False
argHelp = False
argVerbose = False

try:
    for currentArgument, currentValue in arguments:    
        if currentArgument in ("-c", "--config"):
            argConfig = True
        if currentArgument in ("-h", "--help"):
            argHelp = True
        if currentArgument in ("-v", "--verbose"):
            argVerbose = True
except:
    pass

if argHelp:
    print('''[red]komo-load[/]

    [red]usage:[/]
     python main.py [bright_green]--arg[/]

    [red]arguments:[/]
     help: [bright_green]-h[/] or [bright_green]--help[/] -> prints this message
     verbose: [bright_green]-v[/] or [bright_green]--verbose[/] -> shows the output of run commands
     config: [bright_green]-c[/] or [bright_green]-config[/] -> allows you to run the startup configuration
    ''')
    quit()

def getProcesses():
    global proc_dict
    output = subprocess.check_output(('TASKLIST', '/FO', 'CSV')).decode()
    # get rid of extra " and split into lines
    output = output.replace('"', '').split('\r\n')
    keys = output[0].split(',')
    proc_list = [i.split(',') for i in output[1:] if i]
    # make dict with proc names as keys and dicts with the extra nfo as values
    proc_dict = dict((i[0], dict(zip(keys[1:], i[1:]))) for i in proc_list)

title = Align.center('''
 [bold red]____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____
||k |||o |||m |||o |||- |||l |||a |||u |||n |||c |||h ||
||__|||__|||__|||__|||__|||__|||__|||__|||__|||__|||__||
|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|
''', vertical="middle")

customStyle = questionary.Style([
    ('qmark', 'fg:#eb6f92'),
    ('answer', 'fg:#eb6f92')
])

def configure():
    global bar
    global hotkey
    global masir

    bar = questionary.select(
        "What bar do you use?", 
        choices=['YASB', 'komorebi-bar'],
        style=customStyle,
        qmark='🍉'
        ).ask()
    hotkey = questionary.select(
        "What is your preffered hotkey daemon?",
        choices=['whkd', 'ahk'],
        style=customStyle,
        qmark='🍉'
        ).ask()
    masir = questionary.confirm(
        "Do you use masir?",
        style=customStyle,
        qmark='🍉'
        ).ask()
    special = questionary.confirm(
        "Would you like to add another command?",
        default=False,
        style=customStyle,
        qmark='🍉'
        ).ask()
    specialCommandString = questionary.text(
        "Type the special command here:",
        style=customStyle,
        qmark='🍉'
        ).skip_if(special == False, default=False).ask()
    tomlFile = document()
    tomlFile.add("bar", bar)
    tomlFile.add("hotkey", hotkey)
    tomlFile.add("masir", masir)
    tomlFile.add("special", specialCommandString)
    configFile = open(home / "komo-launch.toml", "w")
    configFile.write(dumps(tomlFile))
    configFile.close()
    print("[bold red]Setup done!")

barCommand = []
komorebiCommand = []
specialCommand = []

def buildCommand():
    global barCommand
    global komorebiCommand
    global ParsedFile
    global specialCommand
    ParsedFile = parse(open(home / "komo-launch.toml").read())
    komorebiCommand = ["komorebic", "start"]
    if ParsedFile["hotkey"] == "whkd":
        komorebiCommand.append("--whkd")
    elif ParsedFile["hotkey"] == "ahk":
        komorebiCommand.append("--ahk")
    if ParsedFile["masir"] == True:
        komorebiCommand.append("--masir")
    if ParsedFile["bar"] == "komorebi-bar":
        komorebiCommand.append("--bar")
    if ParsedFile["bar"] == "YASB":
        barCommand = ["yasbc", "start"]
    if ParsedFile["special"] != False:
        specialCommand = ParsedFile["special"].split()


def start():
    buildCommand()
    print("Starting [bold red]Komorebi...")
    if argVerbose:
        subprocess.call(komorebiCommand)
        print("")
    else:
        subprocess.call(komorebiCommand,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT)
    if barCommand:
        print(f'Starting [bold red]{ParsedFile["bar"]}...')
    if argVerbose:
        subprocess.call(barCommand)
        print("")
    else:
        subprocess.call(barCommand,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT)
    if specialCommand:
        print("Running [bold red]your command...")
        if argVerbose:
            subprocess.call(specialCommand, shell=True)
            print("")
        else:
            subprocess.call(specialCommand, shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)

    print("[bold red]DONE!\n")

try:
    configFile = open(home / "komo-launch.toml")
except:
    configFile = open(home / "komo-launch.toml", "x")
    print(title)
    configure()
    print("")
    start()
else:
    print(title)  
    if argConfig == True or os.stat(home / "komo-launch.toml").st_size == 0:
        configure()
        print("")
    getProcesses()
    if 'komorebi.exe' in proc_dict:
        if argVerbose:
            subprocess.call(["komorebic", "stop", "--whkd", "--masir", "--ahk"])
            print("")
        else:
            subprocess.call(["komorebic", "stop", "--whkd", "--masir", "--ahk"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
    if 'yasb.exe' in proc_dict:
        if argVerbose:
            subprocess.call(["yasbc", "reload"])
            print("")
        else:
            subprocess.call(["yasbc", "reload"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
        start()