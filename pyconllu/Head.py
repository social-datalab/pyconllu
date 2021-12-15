# -*- coding: utf-8 -*-
from .Token import Token


class Head(Token):
    """A class that represents a Head in a CoNLL-U sentence."""
    def __init__(self, dependents=[], **kwargs):
        self.dependents = dependents
        super(Head, self).__init__(**kwargs)

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
                self.dependents == other.dependents
            )
        return NotImplemented

    def __ne__(self, other):
        if self.__eq__(other) is NotImplemented:
            return NotImplemented
        return not self.__eq__(other)

    def __repr__(self):
        return (
            '{}(id={}, form={}, lemma={}, upostag={}, xpostag={}, feats={}, '
            'head={}, deprel={}, deps={}, misc={}, dependents={})'.format(
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
                self.misc,
                self.dependents,
            )
        )
