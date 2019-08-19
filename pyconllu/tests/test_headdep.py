# -*- coding: utf-8 -*-
from pyconllu.HeadDep import HeadDep


def test_headdep():
    headdep = HeadDep("árbol", "plantar", "obj", (3, 4))

    assert (headdep.head == "árbol" and
            headdep.dep == "plantar" and
            headdep.relation == "obj" and
            headdep.position == (3, 4))


def test_empty_headdep():
    empty_headdep = HeadDep()

    assert (empty_headdep.head is None and
            empty_headdep.dep is None and
            empty_headdep.relation is None and
            empty_headdep.position is None)
