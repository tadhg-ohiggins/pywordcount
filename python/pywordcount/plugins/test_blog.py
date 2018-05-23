#! /usr/bin/python
# -*- coding: utf-8 -*-

import blog

def test_adjust_for_blog():
    cases = [
        (
            "\n".join([
                "one",
                "two",
                "three"
            ]),
            "three"
        ),
        (
            "\n".join([
                "TITLE",
                "-----",
                "three"
            ]),
            "three"
        ),
        (
            "\n".join([
                "TITLE",
                "-----",
                "three",
                "four",
            ]),
            "three\nfour"
        ),
        (
            "\n".join([
                "TITLE",
                "-----",
                "three",
                "four",
                ".. whatever",
                "five",
                ".. container:: date",
                "six",
            ]),
            "three\nfour\n.. whatever\nfive"
        ),
        (
            "\n".join([
                "TITLE",
                "-----",
                "three",
                "four",
                ".. whatever",
                "five",
                ".. wordcountstop",
                "six",
                ".. container:: date",
                "seven",
            ]),
            "three\nfour\n.. whatever\nfive"
        ),
    ]

    for inp, outp in cases:
        assert blog.pywordcountplugin(inp) == outp
