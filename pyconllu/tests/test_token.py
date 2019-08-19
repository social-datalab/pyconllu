# -*- coding: utf-8 -*-
import pytest
from collections import OrderedDict
from pyconllu.Token import Token


@pytest.fixture()
def token():
    return Token()


@pytest.mark.parametrize("features,expanded_features", [
    (
        OrderedDict([
            ("Mood", "Ind"), ("Number", "Plur"),
            ("Person", "3"), ("Tense", "Pres")
        ]),
        "Mood=Ind|Number=Plur|Person=3|Tense=Pres"
    ),
    (
        None, "_"
    ),
    (
        OrderedDict([
            ("Gender", "Masc"), ("Number", "Sing")
        ]),
        "Gender=Masc|Number=Sing"
    ),
])
def test_expand_features(token, features, expanded_features):
    assert token._expand_features(features) == expanded_features


@pytest.mark.parametrize("tokens,expanded_tokens", [
    (
        None, "_"
    ),
    (
        "NOUN", "NOUN"
    ),
    (
        OrderedDict([
            ("Gender", "Masc"), ("Number", "Sing")
        ]),
        OrderedDict([
            ("Gender", "Masc"), ("Number", "Sing")
        ])
    ),
])
def test_expand_token(token, tokens, expanded_tokens):
    assert token._expand_token(tokens) == expanded_tokens


def test_convert_token_back_to_string(
        token, token_string, parsed_token_from_string):
    assert token_string == str(parsed_token_from_string)
