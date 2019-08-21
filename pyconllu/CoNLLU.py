# -*- coding: utf-8 -*-
import re
import sys
from collections import OrderedDict
from copy import deepcopy
from .HeadDep import HeadDep
from .Sentence import Sentence
from .Token import Head, Token

DEFAULT_FIELDS = (
    'id', 'form', 'lemma', 'upostag', 'xpostag', 'feats',
    'head', 'deprel', 'deps', 'misc')

DEPS_PATTERN = r"\d+:[a-z][a-z_-]*(:[a-z][a-z_-]*)?"
TEXT_PATTERN = r"#\s*text\s*=\s*(.*)$"
TOKEN_SEP_PATTERN = r"\t"
MULTI_DEPS_PATTERN = re.compile(
    r"^{}(\|{})*$".format(DEPS_PATTERN, DEPS_PATTERN))
PNAME_PATTERN = r"(NP|PROPN|PNOUN|NNP)"
CONTRACT_ID_PATTERN = r"^[0-9]+\-[0-9]+$"
EMPTY_NODE_ID_PATTERN = r"^[0-9]+\.[0-9]+$"


class CoNLLU(object):
    """
    It processes a file in CoNNL-U format.

    """
    def __init__(self):
        pass

    def parse_sentence(self, raw_sentence):
        """
        It parses a raw sentence and returns a parsed sentence (list of
        tokens).

        :param raw_sentence: string
        :return: Sentence

        Input:
            "1	O	o	DET (...)
            2	objetivo	objetivo	NOUN (...)
            3-4	dos	_	_	_	_	_	_	_	_
            3	de	de	ADP (...)
            4	os	o	DET (...)
            5	principais	principal	ADJ (...)
            6	hotéis	hotél	NOUN (...)"

        Output:

        Sentence
        (
            comments="",
            tokens=[
                OrderedDict([
                    ("id", "1"), ("form", "O"), ("lemma", "o"),
                    ...
                OrderedDict([
                    ("id", "2"), ("form", "objetivo"),
                    ...
                OrderedDict([
                    ("id", "3"), ("form", "de"), ("lemma", "de"),
                    ...
                OrderedDict([
                    ("id", "4"), ("form", "os"), ("lemma", "o"),
                    ...
                ...
            ],
            contractions=[
                (
                    OrderedDict([
                        ("id", "3-4"), ("form", "dos"), ("lemma", "_"),
                        ("upostag", "_"), ("xpostag", None), ("feats", None),
                        ...
                    2
                ),
                ...
            ],
            empty_nodes=[]
        )
        """
        comments = ""

        if re.search(r"^\s*#", raw_sentence):
            comments = "\n".join(
                re.findall(r"^\s*#.*$", raw_sentence, re.MULTILINE))

        contractions = [
            (self._parse_line(m.group(0)), int(m.group(2))-1)
            for m in re.finditer(
                r"^(([0-9]+)\-[0-9]+\t.*)$", raw_sentence, re.MULTILINE)]

        empty_nodes = [
            (self._parse_line(m.group(0)), int(m.group(2))-1)
            for m in re.finditer(
                r"^(([0-9]+)\.[0-9]+\t.*)$", raw_sentence, re.MULTILINE)]

        return Sentence(
            comments=comments,
            tokens=self._parse_sentence(raw_sentence),
            contractions=contractions,
            empty_nodes=empty_nodes,
        )

    def parse_file(self, ifile):
        """
        (generator)list parse_file(str)

        It transforms a CoNLLU corpus into parsed sentences. A sentence is a
        list of tokens, where each token is an OrderedDict containing all the
        features and information.

        Input:
            ifile = "corpus.conllu"

        Output:
            ToDo
        """
        for raw_sentence in self.read_sentences_from_file(ifile):
            yield self.parse_sentence(raw_sentence)

    def read_sentences_from_file(self, ifile):
        """
        (generator)str read_sentences_from_file(str)

        It reads a CoNLLU corpus from file and returns a generator which
        produces a string containing a raw sentence on each iteration.

        Input:
            ifile = "corpus.conllu"

        Output:
            "# sent_id = 1
            # text = Las unidades sísmicas (...)
            1   Las el  DET DA0FP0  (...)
            2   unidades    unidad  NOUN    NCFP000 (...)
            3   sísmicas    sísmico ADJ AQ0FP0  (...)
            (...)"
        """
        raw_sentence = ""
        try:
            with open(ifile) as f:
                for line in f:
                    line = line.strip(" ")
                    if line == "\n":
                        if raw_sentence is "":
                            continue
                        yield raw_sentence
                        raw_sentence = ""
                        continue

                    if line:
                        raw_sentence += line

            # yield remaining contents if file does not end in '\n\n'
            if raw_sentence:
                yield raw_sentence
        except IOError:
            print("Unable to read file: " + ifile)
            sys.exit()

    def generate_conllu_sentence(self, sentence):
        """

        :param sentence:
        :return: raw_sentence
        """
        tokens = deepcopy(sentence.tokens)

        # Contractions
        for contraction in reversed(sentence.contractions):
            tokens.insert(contraction[1], contraction[0])

        # Empty nodes
        for empty_node in reversed(sentence.empty_nodes):
            tokens.insert(empty_node[1] + 1, empty_node[0])

        return (
            self._get_comments(sentence.comments) +
            self._convert_tokens_to_conllu(tokens)
        )

    def generate_conllu_file(self, sentences):
        return "\n".join([
            self.generate_conllu_sentence(sentence) for sentence in sentences])

    def get_lemmas(self, sentence):
        """
        list get_lemmas(list)

        It returns a list of lemmas in a sentence. A sentence is a list of
        tokens, where each token is an OrderedDict containing all the features
        and information.

        Input:
            Sentence =
            [
                OrderedDict([
                    ('id', 1),
                    ('form', 'Las'),
                    ('lemma', 'el'),
                    ...
                ]),
                OrderedDict([
                    ('id', 2),
                    ('form', 'unidades'),
                    ('lemma', 'unidad'),
                    ...
                ]),
                OrderedDict([
                    ('id', 3),
                    ('form', 'sísmicas'),
                    ('lemma', 'sísmico'),
                    ...
                ]),
                ...
            ]

        Output:
            [
                'el', 'unidad', 'sísmico', 'restante', 'corresponder', 'a' ...
            ]
        """
        return [self._get_lemma(token) for token in sentence.tokens]

    def get_wordforms(self, tokens):
        """
        list get_wordforms(list)

        It returns a list of wordforms in a sentence.

        Input:
            instance of Sentence

        Output:
            [
                'Las', 'unidades', 'sísmicas', 'restantes', 'corresponden' ...
            ]
        """
        return [token.form for token in tokens]

    def get_sentence_text(self, sentence):
        """
        str get_sentence_text(str)

        It returns the sentence as included in the comment 'text = ...' or
        raises Exception if the comment does not exist.
        """
        try:
            return re.search(TEXT_PATTERN, sentence.comments).group(1)
        except:
            pass

        return " ".join(self.get_wordforms(sentence.tokens))

    def get_root(self, tokens):
        """
        dict get_root(list)

        It returns OrderedDict storing data about the sentence head
        (head = 0).

        Input:
            instance of Sentence

        Output:
            OrderedDict([
                ('id', 5),
                ('form', 'corresponden'),
                ('lemma', 'corresponder'),
                ('upostag', 'VERB'),
                ('xpostag', 'VMIP3P0'),
                ('feats', OrderedDict([
                    ('Mood', 'Ind'),
                    ('Number', 'Plur'),
                    ('Person', '3'),
                    ('Tense', 'Pres')
                    ])
                ),
                ('head', 0),
                ('deprel', 'root'),
                ('deps', None),
                ('misc', None)
            ])
        """
        for token in tokens:
            if token.head == 0:
                return token

    def get_heads(self, tokens):
        """
        list get_heads(list)

        It returns a list of heads in a given sentence. Each head is a
        dictionary with information about the head: lemma, tag and its
        list of dependencies.

        Input:
            sentence (list of OrderedDict)

        Output:
            [
                {
                    "lemma", "relleno",
                    "tag", "NOUN",
                    "deps": [
                        {
                            "tag": "ADP",
                            "deprel": "case",
                            "lemma": "a",
                            "form": "a",
                            "pos": "SP"
                        },
                        {
                            "lemma": "el",
                            ...
                        },
                        {
                            "lemma": "sedimentario",
                            ...
                        },
                        {
                            "lemma": "ría",
                            ...
                        }
                    ]
                },
                {
                    "lemma": "unidad",
                    "tag": "NOUN",
                    ...
                },
                {
                    "lemma": "ría",
                    "tag": "NOUN",
                    ...
                },
                {
                    "lemma": "corresponder",
                    "tag": "VERB",
                    ...
                }
            ]
        """
        return [
            Head(
                id=tokens[t - 1].id,
                form=tokens[t - 1].form,
                lemma=tokens[t - 1].lemma,
                upostag=tokens[t - 1].upostag,
                xpostag=tokens[t - 1].xpostag,
                feats=tokens[t - 1].feats,
                head=tokens[t - 1].head,
                deprel=tokens[t - 1].deprel,
                deps=tokens[t - 1].deps,
                misc=tokens[t - 1].misc,
                dependents=self.get_deps_from_head(
                    int(tokens[t - 1].id), tokens)
            ) for t in set([
                token.head for token in tokens
            ]).difference([0])
        ]

    def get_deps_from_head(self, head, tokens):
        """
        list get_deps_from_head(int, list)

        It returns a list of dependencies for a given head. Each dependency
        is a dictionary containing all related information.

        The head provided must be the index of the token in sentence (token
        ID), as returned by get_heads().

        Input:
            head = 1
            sentence (list of OrderedDict)

        Output:
            [
                {
                    "pos": "DA0FP0",
                    "deprel": "det",
                    "lemma": "el",
                    "form": "Las",
                    "tag": "DET"
                },
                {
                    "pos": "AQ0FP0",
                    "deprel": "amod",
                    "lemma": "sísmico",
                    "form": "sísmicas",
                    "tag": "ADJ"
                },
                {
                    "pos": "AQ0CP0",
                    "deprel": "amod",
                    "lemma": "restante",
                    "form": "restantes",
                    "tag": "ADJ"
                }
            ]
        """
        return [
            Token(
                id=token.id,
                form=token.form,
                lemma=token.lemma,
                upostag=token.upostag,
                xpostag=token.xpostag,
                feats=token.feats,
                head=token.head,
                deprel=token.deprel,
                deps=token.deps,
                misc=token.misc,
            ) for token in tokens if token.head == int(head)
        ]

    def get_headdep_pairs(self, sentence):
        """
        list get_headdep_pairs(list)

        It returns a list of Head-Dep relations and their position in the
        sentence. The position is a tuple with the indexes of head and dep
        in the list returned by get_lemmas().

        The 'root' relation is excluded.

        Input: sentence (list of OrderedDict)

        Output:
            [
                headdep(rel='det', head='unidad', dep='el', pos=(1, 0))
                headdep(
                    rel='nsubj', head='corresponder', dep='unidad', pos=(4, 1))
                headdep(rel='amod', head='unidad', dep='sísmico', pos=(1, 2))
                headdep(rel='amod', head='unidad', dep='restante', pos=(1, 3))
                headdep(rel='case', head='relleno', dep='a', pos=(7, 5))
                headdep(rel='det', head='relleno', dep='el', pos=(7, 6))
                headdep(
                    rel='obj', head='corresponder', dep='relleno', pos=(4, 7))
                headdep(
                    rel='amod', head='relleno', dep='sedimentario', pos=(7, 8))
                headdep(rel='case', head='ría', dep='de', pos=(11, 9))
                headdep(rel='det', head='ría', dep='el', pos=(11, 10))
                headdep(rel='nmod', head='relleno', dep='ría', pos=(7, 11))
                headdep(rel='punct', head='corresponder', dep='.', pos=(4, 12))
            ]
        """
        lemmas = self.get_lemmas(sentence)
        return [
            HeadDep(
                head=lemmas[token.head - 1],
                dep=token.lemma,
                relation=token.deprel,
                position=(
                    token.head - 1,
                    idx
                )
            )
            for idx, token in enumerate(sentence.tokens) if token.head > 0
        ]

    def get_headdep_pairs_in_deprel(self, deprel, tokens):
        """
        list get_headdep_pairs_in_deprel(str, list)

        Input:
            deprel = "amod"
            sentence (list of OrderedDict)

        Output:
            [
                headdep(head='unidad', dep='sísmico', rel='amod', pos=(1, 2))
                headdep(head='unidad', dep='restante', rel='amod', pos=(1, 3))
                headdep(
                    head='relleno', dep='sedimentario', rel='amod', pos=(7, 8))
            ]
        """
        return [
            headdep_pair
            for headdep_pair in self.get_headdep_pairs(tokens)
            if headdep_pair.relation == deprel
        ]

    def _get_comments(self, comments):
        if comments:
            if not re.search(r"\n$", comments):
                comments += "\n"
            return comments
        return ""

    def _convert_tokens_to_conllu(self, tokens):
        return "".join([str(token) + "\n" for token in tokens])

    def _is_propername(self, tag):
        """
        bool _is_propername(str)

        It determines if a token is a proper name given its PoS tag.

        Input:
            tag = "DA0FP0"

        Output:
            False
        """
        if re.match(PNAME_PATTERN, tag):
            return True
        return False

    def _get_lemma(self, token):
        """
        str _get_lemma(dict)

        It returns the correct lemma for a token: wordform if the token is a
        proper name, lemma in other cases.

        Input:
            token = OrderedDict([
                ('id', 23),
                ('form', 'UPV'),
                ('lemma', 'upv'),
                ('upostag', 'NOUN'),
                ('xpostag', 'NP00000'),
                ('feats', None),
                ('head', 20),
                ('deprel', 'obl'),
                ('deps', None),
                ('misc', None)
            ])

        Output:
            "UPV"
        """
        return token.form if (
            self._is_propername(token.xpostag) or
            self._is_propername(token.upostag)
        ) else token.lemma

    def _is_contraction(self, line):
        if re.search(
                CONTRACT_ID_PATTERN, re.split(TOKEN_SEP_PATTERN, line)[0]):
            return True
        return False

    def _is_empty_node(selfself, line):
        if re.search(
                EMPTY_NODE_ID_PATTERN, re.split(TOKEN_SEP_PATTERN, line)[0]):
            return True
        return False

    def _parse_file(self, ifile):
        return [
            self._parse_sentence(sentence)
            for sentence in ifile.split("\n\n")
            if sentence
        ]

    def _parse_sentence(self, raw_sentence):
        return [
            self._parse_line(line)
            for line in raw_sentence.split("\n")
            if (line and not line.strip().startswith("#") and
                not self._is_contraction(line) and
                not self._is_empty_node(line))
        ]

    def _parse_line(self, line):
        """
        Parser adapted from conllu package
        https://github.com/EmilStenstrom/conllu
        """
        fields = DEFAULT_FIELDS
        line = re.split(TOKEN_SEP_PATTERN, line)
        if len(line) != 10:
            raise Exception(
                "Invalid format, line must contain ten fields separated "
                "by tabs."
                )

        data = Token()

        for i, field in enumerate(fields):
            if i >= len(line):
                break

            if field == "id":
                data.id = self._parse_id_value(line[i])
            elif field == "form":
                data.form = line[i]
            elif field == "lemma":
                data.lemma = line[i]
            elif field == "upostag":
                data.upostag = line[i]
            elif field == "xpostag":
                data.xpostag = self._parse_nullable_value(line[i])
            elif field == "feats":
                data.feats = self._parse_dict_value(line[i])
            elif field == "head":
                data.head = self._parse_int_value(line[i])
            elif field == "deprel":
                data.deprel = line[i]
            elif field == "deps":
                data.deps = self._parse_paired_list_value(line[i])
            elif field == "misc":
                data.misc = self._parse_dict_value(line[i])

        return data

    def _parse_id_value(selfself, value):
        if re.match(r"^[0-9]+([\-\.][0-9]+)?$", value):
            return value

        raise Exception(
            "Incorrect ID field in CoNLL-U: {}".format(value))

    def _parse_int_value(self, value):
        """
        Parser adapted from conllu package
        https://github.com/EmilStenstrom/conllu
        """
        try:
            return int(value)
        except ValueError:
            return None

    def _parse_paired_list_value(self, value):
        """
        Parser adapted from conllu package
        https://github.com/EmilStenstrom/conllu
        """
        if re.match(MULTI_DEPS_PATTERN, value):
            return [
                (part.split(":", 1)[1], self._parse_int_value(
                    part.split(":", 1)[0]))
                for part in value.split("|")
            ]

        return self._parse_nullable_value(value)

    def _parse_dict_value(self, value):
        """
        Parser adapted from conllu package
        https://github.com/EmilStenstrom/conllu
        """
        if "=" in value:
            return OrderedDict([
                (part.split("=")[0], self._parse_nullable_value(
                    part.split("=")[1]))
                for part in value.split("|") if len(part.split('=')) == 2
            ])

        return self._parse_nullable_value(value)

    def _parse_nullable_value(self, value):
        """
        Parser adapted from conllu package
        https://github.com/EmilStenstrom/conllu
        """
        if not value or value == "_":
            return None

        return value
