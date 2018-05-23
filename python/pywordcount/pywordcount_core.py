#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Script for word count.
TODO: check for mode (filetype) and adjust file accordingly.
TODO: strip dates and other strings consisting only of numerals and /
"""
import argparse
import re
import sys
import os
import codecs
try:
    import configparser
except:  # pragma: no cover  # Don't need to test this.
    import ConfigParser as configparser


base_dir = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, base_dir)
import plugins


LINE_SEPS = (
    "\r",
    "\n"
)

WORD_SEPS = (
    " ",        # space
    "\n",       # linebreak
    "\t",       # tab
    "/",        # slash
    "&",        # ampersand
    '"',        # double quotation mark, straight
    "\u201C",  # double quotation mark, left
    "\u201D",  # double quotation mark, right
    "\u2018",  # single quotation mark, left
    "\u2013",  # en dash
    "\u2014",  # em dash
    "\xa0",  # non-breaking space
    ">",        # greater than symbol
    "<",        # less than symbol
    "*",        # asterisk
    "+",        # plus
    "=",        # equals
    "(",        # left parenthesis
    ")",        # right parenthesis
    "[",        # left bracket
    "]",        # right bracket
    "{",        # left curly bracket
    "}",        # right curly bracket
    "|",        # bar
    ":",        # colon; URL handling normally makes this irrelevant
    ";",        # semicolon
    #Multichar separators:
    "--",
    "--",
    "..",
    "...",
)

IGNORE = (
#Not separators per se, but should not be treated as word content
    "'",        # single quotation mark, straight
    "\u2019",  # single quotation mark, right
    "-",        # hyphen
    "#",        # hash mark
    ".",        # period
    "_",        # underscore
    "`",        # backtick
    "\\",        # backslash
)


def setup_cli_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        "-f",
        dest="file",
        help="read from FILE",
        metavar="FILE",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--type",
        "-t",
        dest="type",
        help="set TYPE",
        metavar="TYPE",
        action="append",
        default=[],
    )
    return parser


def cli_options(args, parser):
    options = parser.parse_args(args)
    return options


#  path: str -> configparser.ConfigParser
def read_config(path):  # pragma: no cover
    cp = configparser.ConfigParser()
    cp.read("%s/config.ini" % path)
    return cp


def handle_config(cp):
    """
    Here we want to:

    + Read the config file and parse it.
    + Set the list of modes where we want to run WordCount().
    + Load any modules necessary for supporting the modes.
    + Set what gets run in what order for each mode.

    """
    # cp = read_config(base_dir)
    # cp = configparser.ConfigParser()
    # cp.read("%s/config.ini" % base_dir)

    #Parse the config data so that we end up with a list of processes for
    #each filetype, or None for those filetypes without specified processes
    types = [ft.strip() for ft in cp.get("filetypes", "types").split(",")]
    procs = dict([(t, None) for t in types] + cp.items("preprocesses"))
    def tolist(v): return v and [i.strip() for i in v.split(",")] or v
    procs = dict([(k, tolist(procs[k])) for k in procs])

    #Get a unique list of the processes and import them
    proc_funcs = {}
    for proc in set(sum([v for v in list(procs.values()) if v], [])):
        dotname = "plugins.%s" % proc
        proc_funcs[proc] = __import__(
            dotname, globals(), locals(),
            ["pywordcountplugin"]).pywordcountplugin

    #Replace the string names with the actual functions:
    for ft in procs:
        procs[ft] = procs[ft] and [proc_funcs[p] for p in procs[ft]] or []

    return procs


def handle_filetypes(filetypes, cfg_filetypes):
    processes = []
    for filetype in filetypes:
        if filetype not in cfg_filetypes:
            print("%s is an unsupported filetype." % filetype)
            raise Exception
        for proc in cfg_filetypes.get(filetype, []):
            if proc not in processes:
                processes.append(proc)
    return processes


def handle_input(files):  # pragma: no cover
    if not files:
        files = [sys.stdin.read()]
        return files

    def read(f): return codecs.open(f, mode="r",encoding="utf-8").read()
    files = [read(f) for f in files]
    return files


def handle_command_line(args, cfg_filetypes):
    parser = setup_cli_parser()
    options = cli_options(args, parser)
    processes = handle_filetypes(options.type, cfg_filetypes)
    files = handle_input(options.file)
    return (processes, files)

def count_input(texts, processes):
    return ["c: %s w: %s l: %s" % count_text(t, processes) for t in texts]


def count_text(text, processes):
    chars = len(text)
    for process in processes:
        text = process(text)
    words, lines = count_words(text)
    return (chars, words, lines)


def count_words(text):
    def ors(l): return r"|".join([re.escape(c) for c in l])
    def retext(text, chars, sub):
        return re.compile(ors(chars)).sub(sub, text)

    lns = text and len(re.compile(ors(LINE_SEPS)).findall(text)) or 0

    text = retext(text, WORD_SEPS + LINE_SEPS, " ").strip()
    text = retext(text.strip(), IGNORE, "").strip()
    words = text.strip() and len(re.compile(r"[ ]+").split(text)) or 0

    return (words, lns)


class PyWordCounter(object):

    LINE_SEPS = (
        "\r",
        "\n"
    )

    WORD_SEPS = (
        " ",        # space
        "\n",       # linebreak
        "\t",       # tab
        "/",        # slash
        "&",        # ampersand
        '"',        # double quotation mark, straight
        "\u201C",  # double quotation mark, left
        "\u201D",  # double quotation mark, right
        "\u2018",  # single quotation mark, left
        "\u2013",  # en dash
        "\u2014",  # em dash
        "\xa0",  # non-breaking space
        ">",        # greater than symbol
        "<",        # less than symbol
        "*",        # asterisk
        "+",        # plus
        "=",        # equals
        "(",        # left parenthesis
        ")",        # right parenthesis
        "[",        # left bracket
        "]",        # right bracket
        "{",        # left curly bracket
        "}",        # right curly bracket
        "|",        # bar
        ":",        # colon; URL handling normally makes this irrelevant
        ";",        # semicolon
        #Multichar separators:
        "--",
        "--",
        "..",
        "...",
    )

    IGNORE = (
    #Not separators per se, but should not be treated as word content
        "'",        # single quotation mark, straight
        "\u2019",  # single quotation mark, right
        "-",        # hyphen
        "#",        # hash mark
        ".",        # period
        "_",        # underscore
        "`",        # backtick
        "\\",        # backslash
    )

def cli_main():
    """
    TODO: count more than one file.
    """
    config = read_config(base_dir)
    cfg_filetypes = handle_config(config)
    processes, files = handle_command_line(sys.argv[1:], cfg_filetypes)
    output = count_input(files, processes)
    print("\n".join(output))



if __name__ == "__main__":  # pragma: no cover
    cli_main()
