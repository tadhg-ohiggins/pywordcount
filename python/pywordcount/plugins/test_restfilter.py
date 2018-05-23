#! /usr/bin/python
# -*- coding: utf-8 -*-

from . import mpage

def test_adjust_for_morning_pages():
    cases = [
        (
            "\n".join([
                "one",
                "two",
                "three"
            ]),
            ""
        ),
        (
            "\n".join([
                "one",
                ".. container:: main",
                "three"
            ]),
            "three"
        ),
        (
            "\n".join([
                "one",
                ".. container:: main",
                "three",
                "four",
            ]),
            "three\nfour"
        ),
        (
            "\n".join([
                "one",
                ".. container:: main",
                "three",
                "four",
                ".. whatever",
                "five",
                ".. container:: affirmations",
                "six",
            ]),
            "three\nfour\n.. whatever\nfive"
        ),
    ]

    for inp, outp in cases:
        assert mpage.pywordcountplugin(inp) == outp
