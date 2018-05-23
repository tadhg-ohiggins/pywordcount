#! /usr/bin/python
# -*- coding: utf-8 -*-

import mail

def test_adjust_for_mail():
    cases = [
        (
            "\n".join([
                "Subject: one",
                "To: two",
                "From: three"
            ]),
            ""
        ),
        (
            "\n".join([
                "Subject: one",
                "From: main",
                "three",
            ]),
            "three"
        ),
        (
            "\n".join([
                "Subject: one",
                "From: main",
                "three",
                "four",
            ]),
            "three\nfour"
        ),
        (
            "\n".join([
                "Subject: one",
                "From: main",
                "three",
                "four",
                ".. whatever",
                "five",
                "> container:: affirmations",
                ">six",
            ]),
            "three\nfour\n.. whatever\nfive"
        ),
        (
            "\n".join([
                "Subject: one",
                "From: main",
                "three",
                "four",
                ".. whatever",
                "five",
                "> container:: affirmations",
                ">six",
                "",
                "Furthermore: ",

            ]),
            "\n".join([
                "three",
                "four",
                ".. whatever",
                "five",
                "",
                "Furthermore: ",
            ]),
        ),
    ]

    for inp, outp in cases:
        assert mail.pywordcountplugin(inp) == outp
