# -*- coding: utf-8 -*-
from collections import OrderedDict


class Token(object):
    """A class that represents a Token in a CoNLL-U sentence."""
    def __init__(
            self, id=None, form=None, lemma=None, upostag=None, xpostag=None,
            feats=None, head=None, deprel=None, deps=None, misc=None):
        """
        Constructor of Token.

        :param id: word index in a sentence
        :param form: wordform
        :param lemma: lemma
        :param upostag: universal part-of-speech tag
        :param xpostag: language specific part-of-speech tag
        :param feats: morphological features
        :param head: head of the word
        :param deprel: universal dependency relation to the head
        :param deps: enhanced dependency graph in the form
        :param misc: any other annotation
        """
        self.id = id
        self.form = form
        self.lemma = lemma
        self.upostag = upostag
        self.xpostag = xpostag
        self.feats = feats
        self.head = head
        self.deprel = deprel
        self.deps = deps
        self.misc = misc

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.id == other.id and
                self.form == other.form and
                self.lemma == other.lemma and
                self.upostag == other.upostag and
                self.xpostag == other.xpostag and
                self.feats == other.feats and
                self.head == other.head and
                self.deprel == other.deprel and
                self.deps == other.deps and
                self.misc == other.misc and
                type(self) == type(other)
            )
        return NotImplemented

    def __ne__(self, other):
        if self.__eq__(other) is NotImplemented:
            return NotImplemented
        return not self.__eq__(other)

    def __repr__(self):
        return (
            '{}(id={}, form={}, lemma={}, upostag={}, xpostag={}, feats={}, '
            'head={}, deprel={}, deps={}, misc={})'.format(
                self.__class__.__name__,
                self.id,
                self.form,
                self.lemma,
                self.upostag,
                self.xpostag,
                self.feats,
                self.head,
                self.deprel,
                self.deps,
                self.misc
            )
        )

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
            self.id,
            self.form,
            self._expand_token(self.lemma),
            self._expand_token(self.upostag),
            self._expand_token(self.xpostag),
            self._expand_features(self.feats),
            self._expand_token(self.head),
            self._expand_token(self.deprel),
            self._expand_token(self.deps),
            self._expand_token(self.misc)
        )

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, value):
        self._form = value

    @property
    def lemma(self):
        return self._lemma

    @lemma.setter
    def lemma(self, value):
        self._lemma = value

    @property
    def upostag(self):
        return self._upostag

    @upostag.setter
    def upostag(self, value):
        self._upostag = value

    @property
    def xpostag(self):
        return self._xpostag

    @xpostag.setter
    def xpostag(self, value):
        self._xpostag = value

    @property
    def feats(self):
        return self._feats

    @feats.setter
    def feats(self, value):
        self._feats = value

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, value):
        self._head = value

    @property
    def deprel(self):
        return self._deprel

    @deprel.setter
    def deprel(self, value):
        self._deprel = value

    @property
    def deps(self):
        return self._deps

    @deps.setter
    def deps(self, value):
        self._deps = value

    @property
    def misc(self):
        return self._misc

    @misc.setter
    def misc(self, value):
        self._misc = value

    @staticmethod
    def _expand_token(token):
        if token is None:
            return "_"
        return token

    @staticmethod
    def _expand_features(features):
        if isinstance(features, OrderedDict):
            return "|".join(
                ["=".join([key, features[key]]) for key in features])
        return "_"
