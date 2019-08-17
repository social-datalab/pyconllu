# -*- coding: utf-8 -*-
import os
import pytest
from types import GeneratorType
from collections import OrderedDict
from pyconllu import CoNLLU
from pyconllu.exceptions import ParseException
from pyconllu.Sentence import Sentence
from pyconllu.Token import Token


@pytest.fixture(scope="session")
def conllu():
    return CoNLLU()


@pytest.fixture()
def conllu_filename(tmpdir):
    def _build_conllu_file(contents):
        filename = os.path.join(tmpdir.strpath, 'sample.conllu')
        with open(filename, "w") as fh:
            fh.write(contents)

        return filename

    return _build_conllu_file


@pytest.fixture()
def sentences_parsed_from_file(conllu, conllu_filename, conllu_file_contents):
    filename = conllu_filename(conllu_file_contents)
    return conllu.parse_file(filename)


def test_read_conllu_from_file(conllu, conllu_filename, conllu_file_contents):
    filename = conllu_filename(conllu_file_contents)
    concat_sentence = [
        sentence for sentence in conllu._read_sentences_from_file(
            filename)]
    assert "\n".join(concat_sentence) == conllu_file_contents


def test_read_conllu_with_multiple_separators(
        conllu, conllu_filename, conllu_multiple_strings):
    filename = conllu_filename(conllu_multiple_strings)
    sentences = [
        sentence for sentence in conllu._read_sentences_from_file(
            filename)]

    assert len(sentences) == 3


def test_parse_sentence_from_string(
        conllu, conllu_string, parsed_sentence_from_string):
    assert conllu.parse_sentence(conllu_string) == parsed_sentence_from_string


def test_parse_last_sentence_from_file(
        sentences_parsed_from_file, parsed_sentence_from_file):
    while True:
        try:
            sentence = next(sentences_parsed_from_file)
        except StopIteration:
            break

    assert sentence == parsed_sentence_from_file[-1]


def test_parse_file_returns_iterator(sentences_parsed_from_file):
    assert isinstance(sentences_parsed_from_file, GeneratorType)


def test_parse_file_output_is_list_of_ordereddicts(sentences_parsed_from_file):
    sent = next(sentences_parsed_from_file)
    assert (isinstance(sent, Sentence) and
            all(isinstance(s, Token) for s in sent.tokens))


def test_parse_empty_sentence(conllu, empty_sentence):
    assert (conllu.parse_sentence(empty_sentence) ==
            Sentence(
                comments=None, tokens=[], contractions=[], empty_nodes=[]))


def test_parse_sentence_with_errors(conllu, sentence_with_errors):
    with pytest.raises(ParseException) as pexc:
        conllu.parse_sentence(sentence_with_errors)
    assert (str(pexc.value) ==
            "Invalid format, line must contain ten fields separated "
            "by tabs.")


def test_parse_sentence_with_empty_node(
        conllu,
        conllu_string_with_empty_node,
        parsed_sentence_with_empty_node):
    assert (conllu.parse_sentence(conllu_string_with_empty_node) ==
            parsed_sentence_with_empty_node)


def test_generate_conllu_from_sentence(
        conllu, parsed_sentence_from_string, conllu_string):
    assert (conllu.generate_conllu_sentence(parsed_sentence_from_string) ==
            conllu_string)


def test_generate_conllu_with_empty_node(
        conllu, parsed_sentence_with_empty_node,
        conllu_string_with_empty_node):
    assert (conllu.generate_conllu_sentence(parsed_sentence_with_empty_node) ==
            conllu_string_with_empty_node)


def test_generate_conllu_from_file(
        conllu, sentences_parsed_from_file, conllu_file_contents):
    assert (conllu.generate_conllu_file(sentences_parsed_from_file) ==
            conllu_file_contents)


def test_convert_tokens_to_conllu_line(
        conllu, parsed_sentence_from_string, conllu_string):
    expected = "\n".join(conllu_string.split("\n")[:2]) + "\n"
    assert conllu._convert_tokens_to_conllu(
        parsed_sentence_from_string.tokens[:2]) == expected


def test_get_lemmas_from_sentence(
        conllu, parsed_sentence_from_string, lemmas):
    assert conllu.get_lemmas(parsed_sentence_from_string) == lemmas


def test_get_wordforms_from_sentence(
        conllu, parsed_sentence_from_string, wordforms):
    assert (conllu.get_wordforms(parsed_sentence_from_string) ==
            wordforms)


@pytest.mark.parametrize('idx,expected', [
    (
        0,
        """# sent_id = 1
# text = El objetivo de este trabajo ha sido conocer si los valores de \
homocisteína influyen en la evolución del GIM carotídeo en pacientes con \
enfermedad coronaria.
"""
    ),
    (
        1,
        """# sent_id = 2
# text = La angiografía coronaria se realizó a 164 pacientes.
"""
    ),
    (
        2,
        """# sent_id = 3
# text = Ningún paciente recibió tratamiento vitamínico durante el estudio.
"""
    )
])
def test_get_comments_from_parsed_file(
        conllu, parsed_sentence_from_file, idx, expected):
    assert conllu._get_comments(
        parsed_sentence_from_file[idx].comments) == expected


def test_get_root_from_sentence(conllu, parsed_sentence_from_string, root):
    assert conllu.get_root(parsed_sentence_from_string) == root


def test_get_sentence_text_from_wordforms(
        conllu,
        parsed_sentence_from_string,
        sentence_from_wordforms):
    assert (conllu.get_sentence_text(parsed_sentence_from_string) ==
            sentence_from_wordforms)


def test_get_sentence_text_from_comments(
        conllu,
        parsed_sentence_from_file,
        sentence_from_comments):
    assert (conllu.get_sentence_text(parsed_sentence_from_file[0]) ==
            sentence_from_comments)


def test_get_head_deps_from_sentence(
        conllu, parsed_sentence_from_string, headdeps):
    assert (conllu.get_headdep_pairs(parsed_sentence_from_string) ==
            headdeps)


def test_get_head_deps_in_deprel(
        conllu, parsed_sentence_from_string, headdeps_nmod):
    assert (conllu.get_headdep_pairs_in_deprel(
        "nmod", parsed_sentence_from_string) == headdeps_nmod)


def test_get_heads_from_sentence(conllu, parsed_sentence_from_string, heads):
    assert conllu.get_heads(parsed_sentence_from_string) == heads


def test_get_deps_from_head(conllu, parsed_sentence_from_string, deps):
    head = conllu.get_heads(parsed_sentence_from_string)[2]
    assert (
        conllu.get_deps_from_head(
            head["id"], parsed_sentence_from_string) == deps)


@pytest.mark.parametrize("line,expected", [
    ("18-19\tdel\t_\t_\t_\t_\t_\t_\t_\t_", True),
    ("25\tfor\tfor\tADP\tIN\t_\t26\tcase\t_\t_", False),
    ("24.1\tleft\tleft\tVERB\tVBN\tVerbForm=Part\t_\t_\tCopyOf=6\t_", False),
])
def test_conllu_line_contains_contraction(conllu, line, expected):
    assert conllu._is_contraction(line) == expected


@pytest.mark.parametrize("line,expected", [
    ("24.1\tleft\tleft\tVERB\tVBN\tVerbForm=Part\t_\t_\tCopyOf=6\t_", True),
    ("25\tfor\tfor\tADP\tIN\t_\t26\tcase\t_\t_", False),
    ("18-19\tdel\t_\t_\t_\t_\t_\t_\t_\t_", False),
])
def test_conllu_line_contains_empty_node(conllu, line, expected):
    assert conllu._is_empty_node(line) == expected


@pytest.mark.parametrize("line,expected", [
    (
        "5\tprincipais\tprincipal\tADJ\tADJ\tGender=Masc|Number=Plur\t6\tamod\
\t_\t_",
        Token(
            id="5", form="principais", lemma="principal", upostag="ADJ",
            xpostag="ADJ", feats=OrderedDict([
                ('Gender', 'Masc'), ('Number', 'Plur')]),
            head=6, deprel="amod", deps=None, misc=None)
    ),
    (
        "3-4\tdos\t_\t_\t_\t_\t_\t_\t_\t_",
        Token(
            id="3-4", form="dos", lemma="_", upostag="_", xpostag=None,
            feats=None, head=None, deprel="_", deps=None, misc=None)
    )
])
def test_parse_conllu_rawline(conllu, line, expected):
    assert conllu._parse_line(line) == expected


@pytest.mark.parametrize("value,expected", [
    ("NOUN", "NOUN"), ("_", None), ("", None)
])
def test_parse_nullable_values(conllu, value, expected):
    assert conllu._parse_nullable_value(value) == expected


@pytest.mark.parametrize("value,expected", [
    ("5-6", None), ("_", None), ("10", 10)
])
def test_parse_int_value(conllu, value, expected):
    assert conllu._parse_int_value(value) == expected


@pytest.mark.parametrize("value,expected", [
    ("Mood=Ind|Number=Plur|Person=3|Tense=Pres", OrderedDict([
        ('Mood', 'Ind'), ('Number', 'Plur'),
        ('Person', '3'), ('Tense', 'Pres')])),
    ("_", None), ("10", "10"), ("", None),
    ("SpaceAfter=No|Gloss=.", OrderedDict([
        ('SpaceAfter', 'No'), ('Gloss', '.')]))])
def test_parse_dict_value(conllu, value, expected):
    assert conllu._parse_dict_value(value) == expected


@pytest.mark.parametrize("value,expected", [
    ("2:obj|4:obj", [('obj', 2), ('obj', 4)]), ("_", None)
])
def test_parse_paired_list_value(conllu, value, expected):
    assert conllu._parse_paired_list_value(value) == expected


@pytest.mark.parametrize("features,expanded_features", [
    (
        OrderedDict([
            ("Mood", "Ind"), ("Number", "Plur"),
            ("Person", "3"), ("Tense", "Pres")]),
        "Mood=Ind|Number=Plur|Person=3|Tense=Pres"
    ),
    (
        None, "_"
    ),
    (
        OrderedDict([
            ("Gender", "Masc"), ("Number", "Sing")]),
        "Gender=Masc|Number=Sing"
    ),
])
def test_expand_features(conllu, features, expanded_features):
    token = Token()
    assert token._expand_features(features) == expanded_features


@pytest.mark.parametrize("tag,expected", [
    ("PNOUN", True), ("NOUN", False),
    ("NCFS000", False), ("PROPN", True),
    ("DET", False), ("NP00000", True),
])
def test_tag_is_propername(conllu, tag, expected):
    assert conllu._is_propername(tag) == expected


@pytest.mark.parametrize("token,lemma", [
    (
        Token(
            id="7", form="de", lemma="de", upostag="ADP", xpostag="ADP",
            feats=None, head=9, deprel="case", deps=None, misc=None),
        "de"
    ),
    (
        Token(
            id="20", form="GIM", lemma="gim", upostag="PROPN",
            xpostag="NP00000", feats=None, head=17, deprel="nmod", deps=None,
            misc=None),
        "GIM"
    )
])
def test_get_lemma(conllu, token, lemma):
    assert conllu._get_lemma(token) == lemma
