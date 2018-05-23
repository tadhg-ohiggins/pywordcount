#! /usr/bin/python
# -*- coding: utf-8 -*-

def pywordcountplugin(text):
    """
    We want to start on the third line, and end at ..container:: date.
    """
    nothing_below = ".. wordcountstop"
    if not nothing_below in text:
        nothing_below = ".. container:: date"
    lines = text.split("\n")
    if len(lines) > 2:
        lines = lines[2:]
    if len(lines):
        newlines, include = [], True
        for line in lines:
            if line == nothing_below:
                include = False
            if include:
                newlines.append(line)
        text = "\n".join(newlines)
    return text
