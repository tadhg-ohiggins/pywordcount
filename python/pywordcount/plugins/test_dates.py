#! /usr/bin/python
# -*- coding: utf-8 -*-

import dates

def test_adjust_for_uris():
    cases = [
        (
            "\n".join([
                "12/12/2008",
                "2008-12-12",
                "12/12/75",
                "05/06"
            ]),
            "date\ndate\ndate\ndate"
        ),
    ]

    for inp, outp in cases:
        print("Expected: %s" % outp)
        print("Input:    %s" % inp)
        print("Output:   %s" % dates.pywordcountplugin(inp))
        assert dates.pywordcountplugin(inp) == outp
