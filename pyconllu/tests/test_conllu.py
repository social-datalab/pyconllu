# -*- coding: utf-8 -*-
import os
from collections import OrderedDict
from types import GeneratorType
import pytest
from pyconllu import CoNLLU
from pyconllu.HeadDep import HeadDep
from pyconllu.Token import Token
from pyconllu.Sentence import Sentence


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
def parse_file_with_sentences(conllu, conllu_filename, conllu_file_contents):
    filename = conllu_filename(conllu_file_contents)
    return conllu.parse_file(filename)


def test_read_conllu_from_file(conllu, conllu_filename, conllu_file_contents):
    filename = conllu_filename(conllu_file_contents)
    sentences = [
        sentence for sentence in conllu.read_sentences_from_file(
            filename)]
    assert "\n".join(sentences) == conllu_file_contents
    assert len(sentences) == 3


def test_read_conllu_from_file_with_multiple_separators(
        conllu, conllu_filename, conllu_multiple_strings):
    filename = conllu_filename(conllu_multiple_strings)
    sentences = [
        sentence for sentence in conllu.read_sentences_from_file(
            filename)]
    assert len(sentences) == 3


def test_parse_sentence_returns_sentence(conllu, conllu_string):
    assert isinstance(conllu.parse_sentence(conllu_string), Sentence) is True


def test_parse_sentence_from_string(
        conllu, conllu_string, parsed_sentence_from_string):
    assert conllu.parse_sentence(conllu_string) == parsed_sentence_from_string


def test_parse_sentence_from_file(
        parse_file_with_sentences, parsed_sentences):
    sentences = [sentence for sentence in parse_file_with_sentences]

    assert sentences == parsed_sentences


def test_parse_empty_sentence(conllu):
    assert (conllu.parse_sentence("") == Sentence())


def test_parse_sentence_with_errors_raises_exception(conllu):
    sentence = "O o DET\nobjetivo objetivo NOUN\nde de ADP\no o DET\n"\
               "principais principal ADJ\nhotéis hotél NOUN"
    with pytest.raises(Exception) as exc:
        conllu.parse_sentence(sentence)
    assert (str(exc.value) ==
            "Invalid format, line must contain ten fields separated "
            "by tabs.")


def test_parse_sentence_with_empty_node(
        conllu,
        conllu_string_with_empty_node,
        parsed_sentence_with_empty_node):
    assert (conllu.parse_sentence(conllu_string_with_empty_node) ==
            parsed_sentence_with_empty_node)


def test_parse_file_returns_iterator(parse_file_with_sentences):
    assert isinstance(parse_file_with_sentences, GeneratorType)


def test_parse_file_output_contains_sentences(parse_file_with_sentences):
    for sentence in parse_file_with_sentences:
        assert (isinstance(sentence, Sentence) and
                all(isinstance(s, Token) for s in sentence.tokens))


def test_generate_conllu_returns_string(
        conllu, parsed_sentence_from_string, conllu_string):
    assert (isinstance(
        conllu.generate_conllu_sentence(parsed_sentence_from_string), str
    ))


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
        conllu, parsed_sentences, conllu_file_contents):
    assert (conllu.generate_conllu_file(parsed_sentences) ==
            conllu_file_contents)


def test_convert_tokens_to_conllu_line(
        conllu, parsed_sentence_from_string, conllu_string):
    expected = "\n".join(conllu_string.split("\n")[3:7]) + "\n"

    assert conllu._convert_tokens_to_conllu(
        parsed_sentence_from_string.tokens[2:6]) == expected


def test_get_lemmas_from_sentence(conllu, parsed_sentence_from_string):
    lemmas = [
        "o", "objetivo", "de", "o", "principal", "hotél", "de", "o", "cidade",
        "."
    ]

    assert conllu.get_lemmas(parsed_sentence_from_string) == lemmas


def test_get_wordforms_from_sentence(conllu, parsed_sentence_from_string):
    wordforms = [
        "O", "objetivo", "de", "os", "principais", "hotéis", "de", "a",
        "cidade", "."
    ]

    assert (conllu.get_wordforms(parsed_sentence_from_string.tokens) ==
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
        conllu, parsed_sentences, idx, expected):
    assert conllu._get_comments(
        parsed_sentences[idx].comments) == expected


def test_get_root_from_sentence(conllu, parsed_sentence_from_string):
    root = Token(
        id="2", form="objetivo", lemma="objetivo", upostag="NOUN",
        xpostag="NOUN", feats=OrderedDict([
            ("Gender", "Masc"), ("Number", "Sing")]),
        head=0, deprel="root", deps=None, misc=None)

    assert conllu.get_root(parsed_sentence_from_string.tokens) == root


def test_get_sentence_text_from_wordforms(conllu, parsed_sentence_from_string):
    raw_sentence = "O objetivo de os principais hotéis de a cidade ."

    assert (conllu.get_sentence_text(parsed_sentence_from_string) ==
            raw_sentence)


def test_get_sentence_text_from_comments(conllu, parsed_sentences):
    raw_sentence = "El objetivo de este trabajo ha sido conocer si los "\
                   "valores de homocisteína influyen en la evolución del "\
                   "GIM carotídeo en pacientes con enfermedad coronaria."

    assert (conllu.get_sentence_text(parsed_sentences[0]) == raw_sentence)


def test_get_head_deps_from_sentence(conllu, parsed_sentence_from_string):
    headdeps = [
        HeadDep(head="objetivo", dep="o", relation="det", position=(1, 0)),
        HeadDep(head="hotél", dep="de", relation="case", position=(5, 2)),
        HeadDep(head="hotél", dep="o", relation="det", position=(5, 3)),
        HeadDep(
            head="hotél", dep="principal", relation="amod", position=(5, 4)
        ),
        HeadDep(
            head="objetivo", dep="hotél", relation="nmod", position=(1, 5)
        ),
        HeadDep(head="cidade", dep="de", relation="case", position=(8, 6)),
        HeadDep(head="cidade", dep="o", relation="det", position=(8, 7)),
        HeadDep(head="hotél", dep="cidade", relation="nmod", position=(5, 8)),
        HeadDep(head="objetivo", dep=".", relation="punct", position=(1, 9))
    ]

    assert (conllu.get_headdep_pairs(parsed_sentence_from_string) ==
            headdeps)


def test_get_head_deps_in_deprel(conllu, parsed_sentence_from_string):
    headdeps_nmod = [
        HeadDep(
            head="objetivo", dep="hotél", relation="nmod", position=(1, 5)
        ),
        HeadDep(head="hotél", dep="cidade", relation="nmod", position=(5, 8))
    ]

    assert (conllu.get_headdep_pairs_in_deprel(
        "nmod", parsed_sentence_from_string) == headdeps_nmod)


def test_get_heads_from_sentence(conllu, parsed_sentence_from_string, heads):
    assert conllu.get_heads(parsed_sentence_from_string.tokens) == heads


def test_get_deps_from_head(conllu, parsed_sentence_from_string, heads):
    head = heads[2].id
    tokens = parsed_sentence_from_string.tokens
    deps = heads[2].dependents

    assert (conllu.get_deps_from_head(head, tokens) == deps)


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
            id="3-4", form="dos", lemma=None, upostag=None, xpostag=None,
            feats=None, head=None, deprel=None, deps=None, misc=None)
    ),
    (
        "24.1\tleft\tleft\tVERB\tVBN\tTense=Past|VerbForm=Part\t_\t_\tCopyOf=6\t_",  # noqa
        Token(
            id="24.1", form="left", lemma="left", upostag="VERB",
            xpostag="VBN", feats=OrderedDict([
                 ('Tense', 'Past'), ('VerbForm', 'Part')]),
            head=None, deprel="_", deps="CopyOf=6", misc=None)
    ),
])
def test_parse_line_from_token_string(conllu, line, expected):
    assert conllu._parse_line(line) == expected


def test_parse_line_returns_token(conllu, conllu_string):
    raw_token = conllu_string.partition('\n')[0]

    assert isinstance(conllu._parse_line(raw_token), Token) is True


def test_parse_line_with_errors_returns_exception(conllu):
    line = "5\tprincipais\tprincipal\tADJ\n"
    with pytest.raises(Exception) as exc:
        conllu._parse_line(line)
    assert (str(exc.value) ==
            "Invalid format, line must contain ten fields separated "
            "by tabs.")


@pytest.mark.parametrize("value,expected", [
    ("NOUN", "NOUN"), ("_", None), ("", None)
])
def test_parse_nullable_values(conllu, value, expected):
    assert conllu._parse_nullable_value(value) == expected


@pytest.mark.parametrize("value,expected", [
    ("5-6", None), ("_", None), ("10", 10), ("24.1", None)
])
def test_parse_int_value(conllu, value, expected):
    assert conllu._parse_int_value(value) == expected


@pytest.mark.parametrize("value,expected", [
    ("5-6", "5-6"), ("10", "10"), ("24.1", "24.1"),
])
def test_parse_id_value(conllu, value, expected):
    assert conllu._parse_id_value(value) == expected


@pytest.mark.parametrize("value", ["_", "", "NOUN"])
def test_parse_id_raises_exception_with_wrong_values(conllu, value):
    with pytest.raises(Exception) as exc:
        conllu._parse_id_value(value)
    assert (str(exc.value) ==
            "Incorrect ID field in CoNLL-U: {}".format(value))


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
