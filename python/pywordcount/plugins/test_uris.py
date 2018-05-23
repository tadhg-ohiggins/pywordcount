#! /usr/bin/python
# -*- coding: utf-8 -*-

import uris

def test_adjust_for_uris():
    cases = [
        (
            "\n".join([
                "http://tadhg.com/wp/ ",
                "two",
                "three"
            ]),
            "url \ntwo\nthree"
        ),
    ]

    for inp, outp in cases:
        assert uris.pywordcountplugin(inp) == outp
