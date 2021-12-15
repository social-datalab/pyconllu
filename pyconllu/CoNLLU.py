# -*- coding: utf-8 -*-
import re
import sys
from collections import OrderedDict
from copy import deepcopy
from .HeadDep import HeadDep
from .Sentence import Sentence
from .Token import Token
from .Head import Head

DEFAULT_FIELDS = (
    'id', 'form', 'lemma', 'upostag', 'xpostag', 'feats',
    'head', 'deprel', 'deps', 'misc')

DEPS_PATTERN = r"\d+:[a-z][a-z_-]*(:[a-z][a-z_-]*)?"
TEXT_PATTERN = r"#\s*text\s*=\s*(.*)$"
TOKEN_SEP_PATTERN = r"\t"
MULTI_DEPS_PATTERN = re.compile(
    r"^{arg}(\|{arg})*$".format(arg=DEPS_PATTERN))
PNAME_PATTERN = r"(NP|PROPN|PNOUN|NNP)"
CONTRACT_ID_PATTERN = r"^[0-9]+\-[0-9]+"
EMPTY_NODE_ID_PATTERN = r"^[0-9]+\.[0-9]+"


class CoNLLU:
    """Process a file or string with text in CoNNL-U format."""
    def __init__(self):
        pass

    def parse_sentence(self, raw_sentence):
        """Parse a sentence in CoNLL-U format

        It parses a sentence in CoNLL-U by building a Sentence object with
        the information.

        :example:

        >>> conllu.parse_sentence(conllu_string)
        Sentence
        (
            comments="",
            tokens=[
                Token(id=1, form=O, lemma=o, upostag=DET, xpostag=DET,
                      feats=OrderedDict([
                        ('Definite', 'Def'), ('Gender', 'Masc'),
                        ('Number', 'Sing'), ('PronType', 'Art')]),
                      head=2, deprel=det, deps=None, misc=None),
                Token(id=2, form=objetivo, lemma=objetivo, upostag=NOUN,
                      xpostag=NOUN, feats=OrderedDict([
                        ('Gender', 'Masc'), ('Number', 'Sing')]),
                      head=0, deprel=root, deps=None, misc=None),
                Token(id=3, form=de, lemma=de, upostag=ADP, xpostag=ADP,
                      feats=None, head=6, deprel=case, deps=None, misc=None),
                (...)
            ],
            contractions=[
                (
                    Token(id="3-4", form="dos", lemma="_", upostag="_",
                          xpostag=None, feats=None, head=None, deprel="_",
                          deps=None, misc=None),
                    2
                ), (...)
            ],
            empty_nodes=[]
        )

        :param raw_sentence: CoNLL-U sentence
        :type raw_sentence: str
        :return: CoNLL-U sentence represented as a Sentence object
        :rtype: Sentence
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
        """Parse a file in CoNLL-U format

        It transforms a CoNLLU corpus into parsed sentences. Each sentence
        contains a list of tokens (Sentence.tokens), where each token is an
        instance of Token containing the features and information.

        :example:

        >>> conllu.parse_file("corpus.conllu")
        <generator object CoNLLU.parse_file at 0x7f224cf94728>

        :param ifile: filename
        :type ifile: str
        :return: generator producing sentences represented as Sentence objects
        :rtype: Sentence
        """
        for raw_sentence in self.read_sentences_from_file(ifile):
            yield self.parse_sentence(raw_sentence)

    def read_sentences_from_file(self, ifile):
        """Read CoNLL-U sentences from file, one at a time

        It reads a CoNLLU corpus from file and returns a generator which
        produces a string containing a raw sentence on each iteration.

        :example:

        >>> conllu.read_sentences_from_file("corpus.conllu")
        <generator object CoNLLU.read_sentences_from_file at 0x7f05ad359780>

        >>> next(sentence)
        '# id = 203\n# text = O objetivo dos principais hotéis da cidade.\n
        1\tO\to\tDET\tDET\tDefinite=Def|Gender=Masc|Number=Sing|PronType=Art\t
        2\tdet\t_\t_\n2\tobjetivo\tobjetivo\tNOUN\tNOUN\tGender=Masc|Number=
        Sing\t0\troot\t_\t_\n3-4\tdos\t_\t_\t_\t_\t_\t_\t_\t_\n3\tde\tde\t
        ADP\tADP\t_\t6\tcase\t_\t_\n4\tos\to\tDET\tDET\tDefinite=Def|Gender=
        Masc|Number=Plur|PronType=Art\t6\tdet\t_\t_\n5\tprincipais\tprincipal
        \tADJ\tADJ\tGender=Masc|Number=Plur\t6\tamod\t_\t_\n6\thotéis\thotel\t
        NOUN\tNOUN\tGender=Masc|Number=Plur\t2\tnmod\t_\t_\n7-8\tda\t_\t_\t_\t
        _\t_\t_\t_\t_\n7\tde\tde\tADP\tADP\t_\t9\tcase\t_\t_\n8\ta\to\tDET\t
        DET\tDefinite=Def|Gender=Fem|Number=Sing|PronType=Art\t9\tdet\t_\t_\n
        9\tcidade\tcidade\tNOUN\tNOUN\tGender=Fem|Number=Sing\t6\tnmod\t_\t_\n
        10\t.\t.\tPUNCT\t.\t_\t2\tpunct\t_\t_\n'

        :param ifile: filename to be read, in CoNLL-U format
        :type ifile: str
        :return: generator producing strings with CoNLL-U sentences
        :rtype: str
        """
        raw_sentence = ""
        try:
            with open(ifile) as fhi:
                for line in fhi:
                    line = line.strip(" ")
                    if line == "\n":
                        if raw_sentence == "":
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
        """Produce a CoNLL-U sentence

        It transforms a Sentence object into a string containing a sentence
        in CoNLL-U format.

        :example:

        >>> conllu.generate_conllu_sentence(sentence)
        '# id = 203\n# text = O objetivo dos principais hotéis da cidade.\n
        1\tO\to\tDET\tDET\tDefinite=Def|Gender=Masc|Number=Sing|PronType=Art\t
        2\tdet\t_\t_\n2\tobjetivo\tobjetivo\tNOUN\tNOUN\tGender=Masc|Number=
        Sing\t0\troot\t_\t_\n3-4\tdos\t_\t_\t_\t_\t_\t_\t_\t_\n3\tde\tde\t
        ADP\tADP\t_\t6\tcase\t_\t_\n4\tos\to\tDET\tDET\tDefinite=Def|Gender=
        Masc|Number=Plur|PronType=Art\t6\tdet\t_\t_\n5\tprincipais\tprincipal\t
        ADJ\tADJ\tGender=Masc|Number=Plur\t6\tamod\t_\t_\n6\thotéis\thotel\t
        NOUN\tNOUN\tGender=Masc|Number=Plur\t2\tnmod\t_\t_\n7-8\tda\t_\t_\t
        _\t_\t_\t_\t_\t_\n7\tde\tde\tADP\tADP\t_\t9\tcase\t_\t_\n8\ta\to\t
        DET\tDET\tDefinite=Def|Gender=Fem|Number=Sing|PronType=Art\t9\tdet\t
        _\t_\n9\tcidade\tcidade\tNOUN\tNOUN\tGender=Fem|Number=Sing\t6\tnmod
        \t_\t_\n10\t.\t.\tPUNCT\t.\t_\t2\tpunct\t_\t_\n'

        :param sentence: object with parsed sentence
        :type sentence: Sentence
        :return: sentence in CoNLL-U format
        :rtype: str
        """
        tokens = deepcopy(sentence.tokens)

        # Contractions
        for contraction in reversed(sentence.contractions):
            tokens.insert(contraction[1], contraction[0])

        # Empty nodes
        for empty_node in reversed(sentence.empty_nodes):
            tokens.insert(empty_node[1] + 1, empty_node[0])

        return (
            self._format_comments(sentence.comments) +
            self._convert_tokens_to_conllu(tokens)
        )

    def generate_conllu_file(self, sentences):
        """Produce multiple CoNLL-U sentences

        It transforms a list of Sentence objects into a string containing
        multiple sentences in CoNLL-U format.

        :param sentences: list of sentences
        :type sentences: list
        :return: sentences in CoNLL-U format
        :rtype: str
        """
        return "\n".join([
            self.generate_conllu_sentence(sentence) for sentence in sentences])

    def get_lemmas(self, sentence):
        """Return lemmas in a sentence.

        It returns a list of lemmas contained in a sentence. Each sentence
        contains a list of tokens (Sentence.tokens), where each token is an
        instance of Token containing the features and information.

        :example:

        >>> conllu.get_lemmas(sentence)
        ['o', 'objetivo', 'de', 'o', 'principal', 'hotel', 'de', 'o',
        'cidade', '.']

        :param sentence: object with parsed sentence
        :type sentence: Sentence
        :return: list of lemmas in sentence
        :rtype: list
        """
        return [self._get_lemma(token) for token in sentence.tokens]

    def get_wordforms(self, sentence):
        """Return wordforms in a sentence.

        It returns a list of wordforms in a sentence.

        :example:

        >>> conllu.get_wordforms(sentence)
        ['O', 'objetivo', 'de', 'os', 'principais', 'hotéis', 'de', 'a',
        'cidade', '.']

        :param sentence: object with parsed sentence
        :type sentence: Sentence
        :return: list of wordforms in sentence
        :rtype: list
        """
        return [token.form for token in sentence.tokens]

    def get_sentence_text(self, sentence):
        """Return sentence text.

        It returns the sentence as included in the comment 'text = ...' or
        the list of wordforms joined by blank spaces if the comment does not
        exist.

        :example:

        - Sentence text is built by joining wordforms. In such cases, the
          result may be different from the original because the applied
          tokenisation (affecting contractions, punctuation, etc) is kept.

        >>> conllu.get_sentence_text(sentence)
        'O objetivo de os principais hotéis de a cidade .'

        - Sentence text is extracted from comments, if they are present.

        >>> conllu.get_sentence_text(sentence)
        'O objetivo dos principais hotéis da cidade.'

        :param sentence: object with parsed sentence
        :type sentence: Sentence
        :return: sentence text
        :rtype: str
        """
        try:
            return re.search(TEXT_PATTERN, sentence.comments).group(1)
        except AttributeError:
            pass

        return " ".join(self.get_wordforms(sentence))

    def get_root(self, sentence):
        """Return the root of the sentence.

        It returns the token analyzed as sentence head (head = 0).

        :example:

        >>> conllu.get_root(sentence)
        Token(id=2, form=objetivo, lemma=objetivo, upostag=NOUN, xpostag=NOUN,
        feats=OrderedDict([('Gender', 'Masc'), ('Number', 'Sing')]), head=0,
        deprel=root, deps=None, misc=None)

        :param sentence: object with parsed sentence
        :type sentence: Sentence
        :return: token marked as root (with head = 0)
        :rtype: Token
        """
        for token in sentence.tokens:
            if token.head == 0:
                return token

    def get_heads(self, sentence):
        """Return heads in a sentence

        It returns a list of heads in a given sentence. Each head is a
        Head object, which extends Token class with an extra attribute
        storing its list of dependents.

        :example:

        >>> conllu.get_heads(sentence)
        [Head(id=9, form=cidade, lemma=cidade (...) dependents=[Token(id=7,
        form=de, lemma=de, upostag=ADP, xpostag=ADP, feats=None, head=9,
        deprel=case, deps=None, misc=None), Token(id=8, form=a, lemma=o,
        upostag=DET, xpostag=DET (...)]

        :param sentence: object with parsed sentence
        :type sentence: Sentence
        :return: tokens in sentence which acts as heads
        :rtype: list
        """
        return [
            Head(
                id=sentence.tokens[t - 1].id,
                form=sentence.tokens[t - 1].form,
                lemma=sentence.tokens[t - 1].lemma,
                upostag=sentence.tokens[t - 1].upostag,
                xpostag=sentence.tokens[t - 1].xpostag,
                feats=sentence.tokens[t - 1].feats,
                head=sentence.tokens[t - 1].head,
                deprel=sentence.tokens[t - 1].deprel,
                deps=sentence.tokens[t - 1].deps,
                misc=sentence.tokens[t - 1].misc,
                dependents=self.get_deps_from_head(
                    int(sentence.tokens[t - 1].id), sentence)
            ) for t in set([
                token.head for token in sentence.tokens
            ]).difference([0])
        ]

    def get_deps_from_head(self, head, sentence):
        """Return the list of dependents of a head.

        It returns a list of dependents for a given head. Each dependent is
        an instance of Token. The head provided must be the index of the
        token in sentence (token ID), as returned by get_heads().

        :example:

        >>> conllu.get_deps_from_head(9, sentence)
        [Token(id=7, form=de, lemma=de, upostag=ADP, xpostag=ADP, feats=None,
        head=9, deprel=case, deps=None, misc=None), Token(id=8, form=a,
        lemma=o, upostag=DET, xpostag=DET, feats=OrderedDict([('Definite',
        'Def'), ('Gender', 'Fem'), ('Number', 'Sing'), ('PronType', 'Art')]),
        head=9, deprel=det, deps=None, misc=None)]

        :param head: head id
        :type head: int
        :param sentence: object with parsed sentence
        :type sentence: Sentence
        :return: tokens in sentence that depends on the given head
        :rtype: list
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
            ) for token in sentence.tokens if token.head == int(head)
        ]

    def get_headdep_triples(self, sentence):
        """Return all dependency triples in a sentence

        It returns a list of Head-Dep relations and their position in the
        sentence, represented as an instance of HeadDep. The position is a
        tuple with the indexes of head and dep in the list returned
        by get_lemmas().

        The 'root' relation is excluded.

        :example:

        >>> conllu.get_headdep_triples(sentence)
        [HeadDep(head=objetivo, dep=o, relation=det, position=(1, 0)),
        HeadDep(head=hotel, dep=de, relation=case, position=(5, 2)),
        HeadDep(head=hotel, dep=o, relation=det, position=(5, 3)),
        HeadDep(head=hotel, dep=principal, relation=amod, position=(5, 4)),
        HeadDep(head=objetivo, dep=hotel, relation=nmod, position=(1, 5)),
        HeadDep(head=cidade, dep=de, relation=case, position=(8, 6)),
        HeadDep(head=cidade, dep=o, relation=det, position=(8, 7)),
        HeadDep(head=hotel, dep=cidade, relation=nmod, position=(5, 8)),
        HeadDep(head=objetivo, dep=., relation=punct, position=(1, 9))]

        :param sentence: object with parsed sentence
        :type sentence: Sentence
        :return: list of head-deps in a sentence
        :rtype: list
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

    def get_headdep_triples_in_deprel(self, deprel, sentence):
        """Return dependency triples with a given relation

        It returns a list of Head-Dep triples in a given relation and their
        position in the sentence.

        :example:

        >>> conllu.get_headdep_triples_in_deprel("nmod", sentence)
        [HeadDep(head=objetivo, dep=hotel, relation=nmod, position=(1, 5)),
        HeadDep(head=hotel, dep=cidade, relation=nmod, position=(5, 8))]

        :param deprel: dependency relation
        :type deprel: str
        :param sentence: object with parsed sentence
        :type sentence: Sentence
        :return: list of head-deps in a dependency relacion
        :rtype: list
        """
        return [
            headdep
            for headdep in self.get_headdep_triples(sentence)
            if headdep.relation == deprel
        ]

    def _format_comments(self, comments):
        """
        It adds a newline character to the comments when needed.
        """
        if comments:
            if not re.search(r"\n$", comments):
                comments += "\n"
            return comments
        return ""

    def _convert_tokens_to_conllu(self, tokens):
        """
        It converts Token objects into CoNLL-U tokens.
        """
        return "".join([str(token) + "\n" for token in tokens])

    def _is_propername(self, tag):
        """
        It determines if a token is a proper name given its PoS tag.
        """
        if re.match(PNAME_PATTERN, tag):
            return True
        return False

    def _get_lemma(self, token):
        """
        It returns the correct lemma for a token: wordform if the token is a
        proper name, lemma in other cases.
        """
        return token.form if (
            self._is_propername(token.xpostag) or
            self._is_propername(token.upostag)
        ) else token.lemma

    def _is_contraction(self, line):
        """
        It checks if a string is a contraction ID or not.
        """
        if re.search(
                CONTRACT_ID_PATTERN, re.split(TOKEN_SEP_PATTERN, line)[0]):
            return True
        return False

    def _is_empty_node(self, line):
        """
        It checks if a string is an empty node ID or not.
        """
        if re.search(
                EMPTY_NODE_ID_PATTERN, re.split(TOKEN_SEP_PATTERN, line)[0]):
            return True
        return False

    def _parse_sentence(self, raw_sentence):
        """
        It parses a raw_sentence and produces a list of tokens.
        """
        return [
            self._parse_line(line)
            for line in raw_sentence.split("\n")
            if (line and not line.strip().startswith("#") and
                not self._is_contraction(line) and
                not self._is_empty_node(line))
        ]

    def _parse_line(self, line):
        """
        It parses a CoNLL-U line and produces a Token instance.

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

        if self._is_contraction(line[0]):
            return Token(id=line[0], form=line[1])

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

    def _parse_id_value(self, value):
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
