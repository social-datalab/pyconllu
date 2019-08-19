# -*- coding: utf-8 -*-
class HeadDep(object):
    def __init__(
            self, head=None, dep=None, relation=None, position=None):
        self.head = head
        self.dep = dep
        self.relation = relation
        self.position = position

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.head == other.head and
                self.dep == other.dep and
                self.relation == other.relation and
                self.position == other.position
            )
        return NotImplemented

    def __ne__(self, other):
        if self.__eq__(other) is NotImplemented:
            return NotImplemented
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self):
        return (
            '{}(head={}, dep={}, relation={}, position={})'.format(
                self.__class__.__name__,
                self.head,
                self.dep,
                self.relation,
                self.position
            )
        )

    def __str__(self):
        return (
            ('{},{},{},{},{}').format(
                self.head,
                self.dep,
                self.relation,
                self.position[0],
                self.position[1]
            )
        )

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, value):
        self._head = value

    @property
    def dep(self):
        return self._dep

    @dep.setter
    def dep(self, value):
        self._dep = value

    @property
    def relation(self):
        return self._relation

    @relation.setter
    def relation(self, value):
        self._relation = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
