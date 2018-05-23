#! /usr/bin/python
# -*- coding: utf-8 -*-

from . import rest

def test_adjust_for_rest():
    cases = [
        (
            "\n".join([
                "one",
                "two",
                "three"
            ]),
            "\n".join([
                "one",
                "two",
                "three"
            ])
        ),
        (
            "\n".join([
                "one",
                ".. container:: main",
                "three"
            ]),
            "\n".join([
                "one",
                "three"
            ])
        ),
        (
            "\n".join([
                "one",
                ".. container:: main",
                "three",
                "four",
            ]),
            "\n".join([
                "one",
                "three",
                "four",
            ])
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
            "\n".join([
                "one",
                "three",
                "four",
                "five",
                "six",
            ]),
        ),
    ]

    for inp, outp in cases:
        assert rest.pywordcountplugin(inp) == outp
