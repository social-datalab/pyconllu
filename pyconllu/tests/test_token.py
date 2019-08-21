# -*- coding: utf-8 -*-
import pytest
from collections import OrderedDict
from pyconllu.Token import Token, Head


@pytest.fixture()
def token():
    return Token(
        id="12", form="defensivo", lemma="defensivo", upostag="ADJ",
        xpostag="ADJ", feats=OrderedDict([
            ('Gender', 'Masc'), ('Number', 'Sing')]),
        head=11, deprel="amod", deps="SpaceAfter=No", misc=None)


def test_token(token):
    assert (token.id == "12" and
            token.form == "defensivo" and
            token.lemma == "defensivo" and
            token.upostag == "ADJ" and
            token.xpostag == "ADJ" and
            token.feats == OrderedDict([
                ('Gender', 'Masc'), ('Number', 'Sing')]) and
            token.head == 11 and
            token.deprel == "amod" and
            token.deps == "SpaceAfter=No" and
            token.misc is None)


def test_empty_token():
    empty_token = Token()

    assert (empty_token.id is None and
            empty_token.form is None and
            empty_token.lemma is None and
            empty_token.upostag is None and
            empty_token.xpostag is None and
            empty_token.feats is None and
            empty_token.head is None and
            empty_token.deprel is None and
            empty_token.deps is None and
            empty_token.misc is None)


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
def test_expand_features(features, expanded_features):
    assert Token._expand_features(features) == expanded_features


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
def test_expand_token(tokens, expanded_tokens):
    assert Token._expand_token(tokens) == expanded_tokens


def test_convert_token_back_to_string(token):
    raw_token = "12	defensivo	defensivo	ADJ	ADJ	Gender=Masc|Number=Sing	"\
                "11	amod	SpaceAfter=No	_"

    assert raw_token == str(token)


def test_head(heads):
    head = heads[0]

    assert (head.id == "9" and
            head.form == "cidade" and
            head.lemma == "cidade" and
            head.upostag == "NOUN" and
            head.xpostag == "NOUN" and
            head.feats == OrderedDict([
                ('Gender', 'Fem'), ('Number', 'Sing')]) and
            head.head == 6 and
            head.deprel == "nmod" and
            head.deps is None and
            head.misc is None and
            head.dependents == [
                Token(id="7", form="de", lemma="de", upostag="ADP",
                      xpostag="ADP", feats=None, head=9, deprel="case",
                      deps=None, misc=None),
                Token(id="8", form="a", lemma="o", upostag="DET",
                      xpostag="DET", feats=OrderedDict([
                        ("Definite", "Def"), ("Gender", "Fem"),
                        ("Number", "Sing"), ("PronType", "Art")]),
                      head=9, deprel="det", deps=None, misc=None),
            ])


def test_empty_head():
    empty_head = Head()

    assert (empty_head.id is None and
            empty_head.form is None and
            empty_head.lemma is None and
            empty_head.upostag is None and
            empty_head.xpostag is None and
            empty_head.feats is None and
            empty_head.head is None and
            empty_head.deprel is None and
            empty_head.deps is None and
            empty_head.misc is None and
            empty_head.dependents == [])
