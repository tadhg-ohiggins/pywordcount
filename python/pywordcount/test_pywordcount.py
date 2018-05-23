#! /usr/env python
# -*- coding: utf-8 -*-
from pathlib import Path
import pytest
from pywordcount.pywordcount_core import (
    configparser,
    count_input,
    count_text,
    count_words,
    handle_config,
    PyWordCounter,
)



wc = PyWordCounter()


def test_handle_config():
    cp = configparser.ConfigParser()
    fp = str(Path(Path(__file__).parent, "test-config.ini").resolve())
    cp.read(fp)
    result = handle_config(cp)
    keys = [k for k in result]
    expected_keys = ["rest", "mpage", "blog", "mail"]
    assert keys == expected_keys
    for k in expected_keys:
        assert all(callable(_) for _ in result[k])


@pytest.mark.parametrize("line,words", (
    ("This should be five words.", 5),
    ("This shouldn't be six words.", 5),
    ("This should be—five words", 5),
    ("This should be\u2014five words", 5),
    ("This should be--five words", 5),
    ("Six–four Federer means six words.", 6)
), ids=repr)
def test_count_words(line, words):
    assert count_words(line)[0] == words


@pytest.mark.parametrize("text,processes,result", (
    ("This should be five words.", [], (26, 5, 0)),
    (
        "This should not fnord be five words.",
        [lambda x: x.replace("fnord", "")],
        (36, 6, 0)
    ),
    # ("This should be five words.", [], "c: 25, w: 5, l: 1"),
), ids=repr)
def test_count_text(text, processes, result):
    assert count_text(text, processes) == result


@pytest.mark.parametrize("texts,processes,result", (
    (["This should be five words."], [], ["c: 26 w: 5 l: 0"]),
    (
        ["This should not fnord be five words."],
        [lambda x: x.replace("fnord", "")],
        ["c: 36 w: 6 l: 0"],
    ),
), ids=repr)
def test_count_input(texts, processes, result):
    assert count_input(texts, processes) == result


single_char_separators = (
    " ",        # space
    "\t",       # tab
    "/",        # slash
    "&",        # ampersand
    '"',        # double quotation mark, straight
    "\u201C",  # double quotation mark, left
    "\u201D",  # double quotation mark, right
    "\u2018",  # single quotation mark, left
    "\u2013",  # en dash
    "\u2014",  # em dash
    ">",        # greater than symbol
    "<",        # less than symbol
    "+",        # plus
    "=",        # equals
    "(",        # left parenthesis
    ")",        # right parenthesis
    "[",        # left bracket
    "]",        # right bracket
    "{",        # left curly bracket
    "}",        # right curly bracket
    "|",        # bar
)
ignore_list = (
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
repeaters = (
    #These are only separators if they're present consecutively, e.g. -- or ..
    "-",
    "."
)
line_endings = (
    "\r",
    "\n"
)


@pytest.mark.parametrize("separator", single_char_separators, ids=repr)
def test_single_separators(separator):
    text = "one%stwo" % separator
    assert count_words(text)[0] == 2


@pytest.mark.parametrize("char", ignore_list, ids=repr)
def test_ignore_list(char):
    text = "one%stwo" % char
    assert count_words(text)[0] == 1


@pytest.mark.parametrize("char", repeaters, ids=repr)
def test_repeaters(char):
    nonrepeat = "one%sone" % char
    repeat = "one%stwo" % (char * 2)
    assert count_words(nonrepeat)[0] == 1
    assert count_words(repeat)[0] == 2


@pytest.mark.parametrize("char", line_endings, ids=repr)
def test_line_endings(char):
    text = "one%stwo" % char
    assert count_words(text)[0] == 2


@pytest.mark.parametrize("text,cwl", (
    ("\n".join([
        "The quick brown fox",
        "jumped over the lazy",
        "dog"
    ]), (44, 9, 2)),
    ("\n".join([
        "The quick brown “fox”",
        "jumped over the lazy",
        "dog"
    ]), (46, 9, 2)),
    ("\n".join([
        "The quick brown “fox”",
        "didn’t jump over the lazy",
        "dog"
    ]), (46, 10, 2)),
    ("\n", (0, 0, 1)),
    ("", (0, 0, 0)),
    ("one two three five words\n", (24, 5, 1)),
    ("one\two\three five words\n", (24, 5, 1)),
    ("one/two/three five words\n", (24, 5, 1)),
    ("one&two&three five words\n", (24, 5, 1)),
    ("one\"two\"three five words\n", (24, 5, 1)),
    ("one“two“three five words\n", (24, 5, 1)),
    ("one“two”three five words\n", (24, 5, 1)),
    ("one‘two‘three five words\n", (24, 5, 1)),
    ("one–two–three five words\n", (24, 5, 1)),
    ("one—two—three five words\n", (24, 5, 1)),
    ("one\xa0two\xa0three five words\n", (24, 5, 1)),
    ("one>two>three five words\n", (24, 5, 1)),
    ("one<two<three five words\n", (24, 5, 1)),
    ("one+two+three five words\n", (24, 5, 1)),
    ("one=two=three five words\n", (24, 5, 1)),
    ("one(two)three five words\n", (24, 5, 1)),
    ("one (two) three five words\n", (26, 5, 1)),
    ("one ( two ) three five words\n", (28, 5, 1)),
    ("one[two]three five words\n", (24, 5, 1)),
    ("one [two] three five words\n", (26, 5, 1)),
    ("one [ two ] three five words\n", (28, 5, 1)),
    ("one\{two\}three five words\n", (24, 5, 1)),
    ("one \{two\} three five words\n", (26, 5, 1)),
    ("one { two } three five words\n", (28, 5, 1)),
    ("one|two|three five words\n", (24, 5, 1)),
    ("one |two| three five words\n", (26, 5, 1)),
    ("one | two | three five words\n", (28, 5, 1)),
    ("one--two--three five words\n", (24, 5, 1)),
    ("one...two..three five words\n", (24, 5, 1)),
    ("one: two three five words\n", (24, 5, 1)),
    ("one;two three five words\n", (24, 5, 1)),
    ("one two three five (words).\n", (24, 5, 1)),
    ("one two . . .     . three five (words).\n", (24, 5, 1)),
), ids=repr)
def test_count_words_two(text, cwl):
    chars, words, lines = cwl
    c_chars, c_words, c_lines = count_text(text, [])
    assert c_words == words
    assert c_lines == lines
