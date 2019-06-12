CoNLLU
======

It processes a file in CoNLL-U format. If REMOVE\_CONTRACTIONS is set to
True, entries representing contractions will be removed.

**Example**: line starting with "7-8" will be skipped.

::

    7-8 al  _   _   _   (...)
    7   a   a   ADP SP  (...)
    8   el  el  DET DA0MS0  (...)

REMOVE\_CONTRACTIONS is set to True by default. We can change this by
setting this option when we create a class instance.

.. code:: python

    >>> import conllu
    >>> conllu = conllu.CoNLLU(remove_contractions=False)

Parse CoNLL-U file
------------------

We can parse a CoNLL-U file in two ways:

-  By calling ``readSentencesFromFile()``, which returns a generator
   producing raw text sentences.

.. code:: python

    # we get a generator which will iterate over sentences in "sample.conllu"
    >>> sentences = conllu.readSentencesFromFile("sample.conllu")

    # we can iterate over each sentence
    >>> for raw_sentence in sentences:
    ...     print(raw_sentence)
    ... 
    # sent_id = 1
    # text = El método utilizado para desarrollar el modelo ha sido la revisión de literatura y categorización de criterios de usabilidad relevantes.
    1   El  el  DET DA0MS0  Definite=Def|Gender=Masc|Number=Sing|PronType=Art   2   det _   _
    2   método  método  NOUN    NCMS000 Gender=Masc|Number=Sing 0   root    _   _
    3   utilizado   utilizar    VERB    VMP00SM Gender=Masc|Number=Sing|VerbForm=Part   11  acl _   _
    (...)

Each raw sentence can be parsed with ``parseSentence()`` which produces
parsed sentences. A parsed sentence is a list of tokens, where each
token is an OrderedDict containing all the features and information.

.. code:: python

    >>> for raw_sentence in sentences:
    ...     sentence = conllu.parseSentence(raw_sentence)
    ...     print(sentence)
    ... 
    [
        OrderedDict([
            ('id', 1),
            ('form', 'El'),
            ('lemma', 'el'),
            ('upostag', 'DET'),
            ('xpostag', 'DA0MS0'),
            ('feats', OrderedDict([
                ('Definite', 'Def'),
                ('Gender', 'Masc'),
                ('Number', 'Sing'),
                ('PronType', 'Art')])
            ),
            ('head', 2),
            ('deprel', 'det'),
            ('deps', None),
            ('misc', None)
        ]),
        OrderedDict([
            ('id', 2),
            ('form', 'método'),
            ('lemma', 'método'),
            (...)
        ]),
        OrderedDict([
            ('id', 3),
            ('form', 'utilizado'),
            ('lemma', 'utilizar'),
            (...)
        ]),
    (...)
    ]

-  By calling ``parseFile()``, which returns a generator producing
   parsed sentences. This is equivalent to the combination of
   ``readSentencesFromFile()`` and ``parseSentence()``.

.. code:: python

    >>> sentences = conllu.parseFile("sample.conllu")
    >>> for sentence in sentences:
    ...     for token in sentence:
    ...             print("{}\t{}".format(token["lemma"], token["deprel"]))
    ... 
    el  det
    método  root
    utilizar    acl
    para    mark
    desarrollar advcl
    el  det
    modelo  nsubj
    (...)

Other methods
-------------

Once we have the CoNLL-U corpus processed into sentences (raw text or
parsed in individual tokens), we can use other public methods to obtain
more fine-grained information from the corpus.

List of lemmas or wordforms
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The public methods ``getLemmasFromSentence()`` and
``getWordformsFromSentence()`` take a parsed sentence (as returned from
``parseFile()`` and ``parseSentence()``) and produce a list of lemmas
and wordforms, respectively.

.. code:: python

    >>> sentences = conllu.parseFile("sample.conllu")
    >>> for sentence in sentences:
    ...     lemmas = conllu.getLemmasFromSentence(sentence)
    ...     words = conllu.getWordformsFromSentence(sentence)
    ...     print(lemmas)
    ... 
    ['el', 'método', 'utilizar', 'para', 'desarrollar', 'el', 'modelo', (...)]
    (...)
    ...     print(words)
    ... 
    ['El', 'método', 'utilizado', 'para', 'desarrollar', 'el', 'modelo', (...)]
    (...)

Getting dependency information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List of heads in sentence
^^^^^^^^^^^^^^^^^^^^^^^^^

We can obtain a list of heads in a given parsed sentence. Each head is a
dictionary with the following information: id, lemma, tag and the list
of dependencies.

.. code:: python

    >>> for sentence in sentences:
    ...     conllu.getHeadsFromSentence(sentence)
    ... 
    [
        {
            'lemma': 'método',
            'tag': 'NOUN',
            'id': 2,
            'deps': [
                {
                    'lemma': 'el',
                    'tag': 'DET',
                    'form': 'El',
                    'pos': 'DA0MS0',
                    'deprel': 'det'
                },
                {
                    'lemma': 'revisión',
                    'tag': 'NOUN',
                    'form': 'revisión',
                    'pos': 'NCFS000',
                    'deprel': 'appos'
                },
                (...)
            ]
        },
        (...)
    ]

List of deps in sentence
^^^^^^^^^^^^^^^^^^^^^^^^

We may obtain a list of dependencies for a given head in a given parsed
sentence. Each dependency is a dictionary containing all related
information.

The head provided must be the index of the token in sentence (token ID),
as returned by ``getHeadsFromSentence()``.

Example: obtaining dependencies of the head with ID 19 (lemma
"usabilidad").

.. code:: python

    >>> sentences = conllu.parseFile("sample.conllu")
    >>> sentence = next(sentences)
    >>> conllu.getDepsFromHead(19, sentence)
    [
        {
            'pos': 'SP',
            'deprel': 'case',
            'tag': 'ADP',
            'form': 'de',
            'lemma': 'de'
        },
        {
            'pos': 'AQ0CP0',
            'deprel': 'amod',
            'tag': 'ADJ',
            'form': 'relevantes',
            'lemma': 'relevante'
        }
    ]

Example: obtaining dependencies from the full list of heads in a
sentence.

.. code:: python

    >>> import conllu
    >>> import json
    >>> conllu = conllu.CoNLLU()
    >>> sentences = conllu.parseFile("sample.conllu")
    >>> sentence = next(sentences)
    >>> for heads in conllu.getHeadsFromSentence(sentence):
    ...     print("ID {}: {}".format(heads["id"], heads["lemma"]))
    ...     deps = conllu.getDepsFromHead(heads["id"], sentence)
    ...     print(json.dumps(deps, indent=4))
    ... 
    ID 2: método
    [
        {
            "pos": "DA0MS0",
            "tag": "DET",
            "lemma": "el",
            "form": "El",
            "deprel": "det"
        },
        {
            "pos": "NCFS000",
            "tag": "NOUN",
            "lemma": "revisión",
            "form": "revisión",
            "deprel": "appos"
        },
        (...)
    ]
    ID 5: desarrollar
    [
        {
            "pos": "SP",
            "tag": "ADP",
            "lemma": "para",
            "form": "para",
            "deprel": "mark"
        }
    ]
    (...)

List of relations Head-Dep in a sentence
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The method ``getHeadDepsFromSentence()`` returns a list of Head-Dep
relations and their position in the sentence. This position is a tuple
with the indexes of head and dep in the list returned by
``getLemmasFromSentence()``.

The 'root' relation is excluded.

Example:

.. code:: python

    >>> sentences = conllu.parseFile("sample.conllu")
    >>> sentence = next(sentences)
    >>> conllu.getHeadDepsFromSentence(sentence)
    [
        headdep(rel='det', head='método', dep='el', pos=(1, 0)),
        headdep(rel='acl', head='revisión', dep='utilizar', pos=(10, 2)),
        headdep(rel='mark', head='desarrollar', dep='para', pos=(4, 3)),
        headdep(rel='advcl', head='revisión', dep='desarrollar', pos=(10, 4)),
        headdep(rel='det', head='modelo', dep='el', pos=(6, 5)),
        headdep(rel='amod', head='usabilidad', dep='relevante', pos=(18, 19))
        (...)
    ]

If we want to restrict the output to a single dependency relation, we
may use ``getHeadDepsFromSentenceInDeprel()`` instead.

.. code:: python

    >>> sentence = next(sentences)
    >>> headdep = conllu.getHeadDepsFromSentenceInDeprel('amod', sentence)
    >>> headdep
    [
        headdep(rel='amod', head='entorno', dep='virtual', pos=(5, 6)),
        headdep(rel='amod', head='usabilidad', dep='relevante', pos=(18, 19))
    ]
    >>> print(headdep[0].head)
    entorno

Obtain the root element from a sentence
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The method ``getRootFromSentence()`` gets a parsed sentence and returns
the root token with its features (as OrderedDict).

.. code:: python

    >>> sentence = next(sentences)
    >>> conllu.getRootFromSentence(sentence)
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
            ('Tense', 'Pres')])
        ),
        ('head', 0),
        ('deprel', 'root'),
        ('deps', None),
        ('misc', None)
    ])

Get sentence text
^^^^^^^^^^^^^^^^^

If the CoNLL-U corpus contains the sentence text included as comments,
we could get it by calling ``getSentenceTextFromRawtext()``. If this
information is not available, ``getSentenceTextFromWordforms()`` can
build a representation of the sentence by joining its wordforms.

.. code:: python

    >>> import conllu
    >>> conllu = conllu.CoNLLU()
    >>> sentences = conllu.readSentencesFromFile("sample.conllu")
    >>> raw_sentence = next(sentences)
    >>> try:
    ...     sentence_text = conllu.getSentenceTextFromRawtext(raw_sentence)
    ... except:
    ...     sentence = conllu.parseSentence(raw_sentence)
    ...     sentence_text = conllu.getSentenceTextFromWordforms(sentence)
    ... 
    >>> print(sentence_text)
    Las unidades sísmicas restantes corresponden al relleno sedimentario de las rías.

