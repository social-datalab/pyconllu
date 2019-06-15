# -*- coding: utf-8 -*-


class Sentence(object):
    def __init__(self, tokens, comments, contractions, empty_nodes):
        self.tokens = tokens
        self.comments = comments
        self.contractions = contractions
        self.empty_nodes = empty_nodes

    def __repr__(self):
        return (
            ('{}(comments="{}", tokens={}, contractions={}, '
             'empty_nodes={})').format(
                self.__class__.__name__,
                self.comments,
                self.tokens,
                self.contractions,
                self.empty_nodes
            )
        )

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.tokens == other.tokens and
                self.comments == other.comments and
                self.contractions == other.contractions and
                self.empty_nodes == other.empty_nodes
            )
        return NotImplemented

    def __ne__(self, other):
        if self.__eq__(other) is NotImplemented:
            return NotImplemented
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, value):
        self._tokens = value

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, value):
        self._comments = value

    @property
    def contractions(self):
        return self._contractions

    @contractions.setter
    def contractions(self, value):
        self._contractions = value

    @property
    def empty_nodes(self):
        return self._empty_nodes

    @empty_nodes.setter
    def empty_nodes(self, value):
        self._empty_nodes = value