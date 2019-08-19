# -*- coding: utf-8 -*-
from pyconllu.Sentence import Sentence
from pyconllu.Token import Token


def test_sentence(parsed_sentence_from_string):
    sentence = Sentence(
        comments="# sent-id = 1\n# A cidade.",
        tokens=[
            Token(id="1", form="A", lemma="o", upostag="DET", xpostag="DET",
                  feats=None, head=2, deprel="det", deps=None, misc=None),
            Token(id="2", form="cidade", lemma="cidade", upostag="NOUN",
                  xpostag="NOUN", feats=None, head=0, deprel="root",
                  deps=None, misc=None),
            Token(id="3", form=".", lemma=".", upostag="PUNCT", xpostag=".",
                  feats=None, head=2, deprel="punct", deps=None, misc=None),
        ],
    )

    assert (sentence.contractions == [] and
            sentence.empty_nodes == [] and
            sentence.tokens == [
                Token(
                    id="1", form="A", lemma="o", upostag="DET", xpostag="DET",
                    feats=None, head=2, deprel="det", deps=None, misc=None
                ),
                Token(
                    id="2", form="cidade", lemma="cidade", upostag="NOUN",
                    xpostag="NOUN", feats=None, head=0, deprel="root",
                    deps=None, misc=None
                ),
                Token(
                    id="3", form=".", lemma=".", upostag="PUNCT", xpostag=".",
                    feats=None, head=2, deprel="punct", deps=None, misc=None
                ),
            ] and
            sentence.comments == "# sent-id = 1\n# A cidade.")


def test_empty_sentence():
    empty_sentence = Sentence()

    assert (empty_sentence.comments == "" and
            empty_sentence.tokens == [] and
            empty_sentence.contractions == [] and
            empty_sentence.empty_nodes == [])
