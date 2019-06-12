# -*- coding: utf-8 -*-
from collections import namedtuple


headdep = namedtuple(
    'headdep', 'head dep rel pos')

sentence = namedtuple(
    'sentence', 'comments tokens contractions empty_nodes')
