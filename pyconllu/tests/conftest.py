# -*- coding: utf-8 -*-
import pytest
from collections import OrderedDict
from pyconllu.HeadDep import HeadDep
from pyconllu.Sentence import Sentence
from pyconllu.Token import Token


@pytest.fixture
def conllu_string():
    return """1	O	o	DET	DET	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	2	det	_	_
2	objetivo	objetivo	NOUN	NOUN	Gender=Masc|Number=Sing	0	root	_	_
3-4	dos	_	_	_	_	_	_	_	_
3	de	de	ADP	ADP	_	6	case	_	_
4	os	o	DET	DET	Definite=Def|Gender=Masc|Number=Plur|PronType=Art	6	det	_	_
5	principais	principal	ADJ	ADJ	Gender=Masc|Number=Plur	6	amod	_	_
6	hotéis	hotél	NOUN	NOUN	Gender=Masc|Number=Plur	2	nmod	_	_
7-8	da	_	_	_	_	_	_	_	_
7	de	de	ADP	ADP	_	9	case	_	_
8	a	o	DET	DET	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	9	det	_	_
9	cidade	cidade	NOUN	NOUN	Gender=Fem|Number=Sing	6	nmod	_	_
10	.	.	PUNCT	.	_	2	punct	_	_
"""


@pytest.fixture
def conllu_multiple_strings():
    return """# sent_id = train-s1
# text = O cantor só precisou vê - la nadar para passar a acreditar na nadadora.
1	O	o	DET	DET	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	2	det	_	_
2	cantor	cantor	NOUN	NOUN	Gender=Masc|Number=Sing	4	nsubj	_	_
3	só	só	ADV	ADV	_	4	advmod	_	_
4	precisou	precisar	VERB	VERB	Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin	0	root	_	_
5	vê	ver	VERB	VERB	VerbForm=Inf	4	xcomp	_	_
6	-	-	PUNCT	.	_	5	punct	_	_
7	la	ela	PRON	PRON	Case=Acc|Gender=Fem|Number=Sing|Person=3|PronType=Prs	5	obj	_	_
8	nadar	nadar	VERB	VERB	VerbForm=Inf	5	ccomp	_	_
9	para	para	ADP	ADP	_	12	mark	_	_
10	passar	passar	AUX	AUX	VerbForm=Inf	12	aux	_	_
11	a	a	ADP	ADP	_	12	mark	_	_
12	acreditar	acreditar	VERB	VERB	VerbForm=Inf	4	nmod	_	_
13-14	na	_	_	_	_	_	_	_	_
13	em	em	ADP	ADP	_	15	case	_	_
14	a	o	DET	DET	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	15	det	_	_
15	nadadora	nadadora	NOUN	NOUN	Gender=Fem|Number=Sing	12	nmod	SpaceAfter=No	_
16	.	.	PUNCT	.	_	4	punct	_	_



# sent_id = train-s2
# text = A Gol comprou a Webjet e, em novembro, decidiu fechá - la.
1	A	o	DET	DET	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	2	det	_	_
2	Gol	gol	PROPN	PNOUN	Gender=Masc|Number=Sing	3	nsubj	_	_
3	comprou	comprar	VERB	VERB	Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin	0	root	_	_
4	a	o	DET	DET	_	5	det	_	_
5	Webjet	Webjet	PROPN	PNOUN	Gender=Masc|Number=Sing	3	obj	_	_
6	e	e	CCONJ	CONJ	_	11	cc	SpaceAfter=No	_
7	,	,	PUNCT	.	_	9	punct	_	_
8	em	em	ADP	ADP	_	9	case	_	_
9	novembro	novembro	PROPN	PNOUN	Gender=Masc|Number=Sing	11	nmod	SpaceAfter=No	_
10	,	,	PUNCT	.	_	9	punct	_	_
11	decidiu	decidir	VERB	VERB	Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin	3	conj	_	_
12	fechá	fechar	VERB	VERB	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	11	xcomp	_	_
13	-	-	PUNCT	.	_	12	punct	_	_
14	la	ela	PRON	PRON	Case=Acc|Gender=Fem|Number=Sing|Person=3|PronType=Prs	12	obj	SpaceAfter=No	_
15	.	.	PUNCT	.	_	3	punct	_	_


# sent_id = train-s3
# text = O terramoto de 1755 também acarretou extensos danos ao conjunto defensivo.
1	O	o	DET	DET	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	2	det	_	_
2	terramoto	terramoto	NOUN	NOUN	Gender=Masc|Number=Sing	6	nsubj	_	_
3	de	de	ADP	ADP	_	4	case	_	_
4	1755	1755	NUM	NUM	NumType=Card	2	nmod	_	_
5	também	também	ADV	ADV	_	6	advmod	_	_
6	acarretou	acarretar	VERB	VERB	Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin	0	root	_	_
7	extensos	extenso	ADJ	ADJ	Gender=Masc|Number=Plur	8	amod	_	_
8	danos	dano	NOUN	NOUN	Gender=Masc|Number=Plur	6	obj	_	_
9-10	ao	_	_	_	_	_	_	_	_
9	a	a	ADP	ADP	_	11	case	_	_
10	o	o	DET	DET	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	11	det	_	_
11	conjunto	conjunto	NOUN	NOUN	Gender=Masc|Number=Sing	6	iobj	_	_
12	defensivo	defensivo	ADJ	ADJ	Gender=Masc|Number=Sing	11	amod	SpaceAfter=No	_
13	.	.	PUNCT	.	_	6	punct	_	_


"""  # noqa


@pytest.fixture
def conllu_file_contents():
    return """# sent_id = 1
# text = El objetivo de este trabajo ha sido conocer si los valores de \
homocisteína influyen en la evolución del GIM carotídeo en pacientes con \
enfermedad coronaria.
1	El	el	DET	DA0MS0	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	2	det	_	_
2	objetivo	objetivo	NOUN	NCMS000	Gender=Masc|Number=Sing	8	nsubj:pass	_	_
3	de	de	ADP	SP	AdpType=Prep	5	case	_	_
4	este	este	DET	DD0MS0	Definite=Def|Gender=Masc|Number=Sing|PronType=Dem	5	det	_	_
5	trabajo	trabajo	NOUN	NCMS000	Gender=Masc|Number=Sing	2	nmod	_	_
6	ha	haber	AUX	VSIP3S0	Mood=Ind|Number=Sing|Person=3|Tense=Pres	8	aux	_	_
7	sido	ser	AUX	VSP00SM	Gender=Masc|Number=Sing|VerbForm=Part	8	aux:pass	_	_
8	conocer	conocer	VERB	VMN0000	VerbForm=Inf	0	root	_	_
9	si	si	SCONJ	CS	_	14	mark	_	_
10	los	el	DET	DA0MP0	Definite=Def|Gender=Masc|Number=Plur|PronType=Art	11	det	_	_
11	valores	valor	NOUN	NCMP000	Gender=Masc|Number=Plur	14	nsubj	_	_
12	de	de	ADP	SP	AdpType=Prep	13	case	_	_
13	homocisteína	homocisteína	NOUN	NCFS000	Gender=Fem|Number=Sing	11	nmod	_	_
14	influyen	influir	VERB	VMIP3P0	Mood=Ind|Number=Plur|Person=3|Tense=Pres	8	advcl	_	_
15	en	en	ADP	SP	AdpType=Prep	17	case	_	_
16	la	el	DET	DA0FS0	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	17	det	_	_
17	evolución	evolución	NOUN	NCFS000	Gender=Fem|Number=Sing	14	obl	_	_
18-19	del	_	_	_	_	_	_	_	_
18	de	de	ADP	SP	AdpType=Prep	20	case	_	_
19	el	el	DET	DA0MS0	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	20	det	_	_
20	GIM	gim	PROPN	NP00000	_	17	nmod	_	_
21	carotídeo	carotídeo	ADJ	AQ0MS0	Gender=Masc|Number=Sing	20	amod	_	_
22	en	en	ADP	SP	AdpType=Prep	23	case	_	_
23	pacientes	paciente	NOUN	NCCP000	Gender=Com|Number=Plur	8	obl	_	_
24	con	con	ADP	SP	AdpType=Prep	25	case	_	_
25	enfermedad	enfermedad	NOUN	NCFS000	Gender=Fem|Number=Sing	8	obl	_	_
26	coronaria	coronario	ADJ	AQ0FS0	Gender=Fem|Number=Sing	25	amod	_	_
27	.	.	PUNCT	Fp	_	8	punct	_	_

# sent_id = 2
# text = La angiografía coronaria se realizó a 164 pacientes.
1	La	el	DET	DA0FS0	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	2	det	_	_
2	angiografía	angiografía	NOUN	NCFS000	Gender=Fem|Number=Sing	5	nsubj	_	_
3	coronaria	coronario	ADJ	AQ0FS0	Gender=Fem|Number=Sing	2	amod	_	_
4	se	se	PRON	P00CN000	_	5	iobj	_	_
5	realizó	realizar	VERB	VMIS3S0	Mood=Ind|Number=Sing|Person=3|Tense=Past	0	root	_	_
6	a	a	ADP	SP	AdpType=Prep	8	case	_	_
7	164	164	NUM	Z	NumType=Card	8	nummod	_	_
8	pacientes	paciente	NOUN	NCCP000	Gender=Com|Number=Plur	5	obl	_	_
9	.	.	PUNCT	Fp	_	5	punct	_	_

# sent_id = 3
# text = Ningún paciente recibió tratamiento vitamínico durante el estudio.
1	Ningún	ninguno	DET	DI0MS0	Definite=Ind|Gender=Masc|Number=Sing|PronType=Art	2	det	_	_
2	paciente	paciente	NOUN	NCCS000	Gender=Com|Number=Sing	3	nsubj	_	_
3	recibió	recibir	VERB	VMIS3S0	Mood=Ind|Number=Sing|Person=3|Tense=Past	0	root	_	_
4	tratamiento	tratamiento	NOUN	NCMS000	Gender=Masc|Number=Sing	3	obj	_	_
5	vitamínico	vitamínico	ADJ	AQ0MS0	Gender=Masc|Number=Sing	4	amod	_	_
6	durante	durante	ADP	SP	AdpType=Prep	8	case	_	_
7	el	el	DET	DA0MS0	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	8	det	_	_
8	estudio	estudio	NOUN	NCMS000	Gender=Masc|Number=Sing	3	obl	_	_
9	.	.	PUNCT	Fp	_	3	punct	_	_
"""  # noqa


@pytest.fixture
def conllu_string_with_empty_node():
    return """# source_sent_id = . . email-enronsent28_01-0019
# text = By late 1974 investors were dizzy, they were desperate, they were wrung-out, they had left Wall Street, many for good.
1	By	by	ADP	IN	_	3	case	_	_
2	late	late	ADJ	JJ	Degree=Pos	3	amod	_	_
3	1974	1974	NUM	CD	NumType=Card	6	obl	_	_
4	investors	investor	NOUN	NNS	Number=Plur	6	nsubj	_	_
5	were	be	AUX	VBD	Mood=Ind|Tense=Past|VerbForm=Fin	6	cop	_	_
6	dizzy	dizzy	ADJ	JJ	Degree=Pos	0	root	SpaceAfter=No	_
7	,	,	PUNCT	,	_	10	punct	_|CheckAttachment=6	_
8	they	they	PRON	PRP	Case=Nom|Number=Plur|Person=3|PronType=Prs	10	nsubj	_	_
9	were	be	AUX	VBD	Mood=Ind|Tense=Past|VerbForm=Fin	10	cop	_	_
10	desperate	desperate	ADJ	JJ	Degree=Pos	6	conj	SpaceAfter=No|CheckReln=parataxis	_
11	,	,	PUNCT	,	_	14	punct	_|CheckAttachment=10	_
12	they	they	PRON	PRP	Case=Nom|Number=Plur|Person=3|PronType=Prs	14	nsubj:pass	_	_
13	were	be	AUX	VBD	Mood=Ind|Tense=Past|VerbForm=Fin	14	aux:pass	_	_
14	wrung	wring	VERB	VBN	Tense=Past|VerbForm=Part|Voice=Pass	6	conj	SpaceAfter=No|CheckReln=parataxis	_
15	-	-	PUNCT	HYPH	_	14	punct	SpaceAfter=No	_
16	out	out	ADP	RP	_	14	compound:prt	SpaceAfter=No	_
17	,	,	PUNCT	,	_	20	punct	_|CheckAttachment=6	_
18	they	they	PRON	PRP	Case=Nom|Number=Plur|Person=3|PronType=Prs	20	nsubj	_	_
19	had	have	AUX	VBD	Mood=Ind|Tense=Past|VerbForm=Fin	20	aux	_	_
20	left	leave	VERB	VBN	Tense=Past|VerbForm=Part	6	conj	_|CheckReln=parataxis	_
21	Wall	Wall	PROPN	NNP	Number=Sing	22	compound	_	_
22	Street	Street	PROPN	NNP	Number=Sing	20	obj	SpaceAfter=No	_
23	,	,	PUNCT	,	_	20	punct	_|CheckAttachment=22	_
24	many	many	ADJ	JJ	Degree=Pos	6	parataxis	_|CheckAttachment=22|CheckReln=appos	_
24.1	left	left	VERB	VBN	Tense=Past|VerbForm=Part	_	_	CopyOf=6	_
25	for	for	ADP	IN	_	26	case	_	_
26	good	good	ADJ	JJ	Degree=Pos	24	orphan	SpaceAfter=No|CheckReln=nmod	_
27	.	.	PUNCT	.	_	6	punct	_	_
"""  # noqa


@pytest.fixture()
def token_string():
    return ("12	defensivo	defensivo	ADJ	ADJ	"
            "Gender=Masc|Number=Sing	11	amod	SpaceAfter=No	_")


@pytest.fixture()
def parsed_token_from_string():
    return Token(
        id="12", form="defensivo", lemma="defensivo", upostag="ADJ",
        xpostag="ADJ", feats=OrderedDict([
            ('Gender', 'Masc'), ('Number', 'Sing')]),
        head=11, deprel="amod", deps="SpaceAfter=No", misc=None)


@pytest.fixture
def parsed_sentence_from_string():
    return Sentence(
        comments="",
        tokens=[
            Token(id="1", form="O", lemma="o", upostag="DET", xpostag="DET",
                  feats=OrderedDict([
                      ("Definite", "Def"), ("Gender", "Masc"),
                      ("Number", "Sing"), ("PronType", "Art")]),
                  head=2, deprel="det", deps=None, misc=None),
            Token(id="2", form="objetivo", lemma="objetivo", upostag="NOUN",
                  xpostag="NOUN", feats=OrderedDict([
                      ("Gender", "Masc"), ("Number", "Sing")]),
                  head=0, deprel="root", deps=None, misc=None),
            Token(id="3", form="de", lemma="de", upostag="ADP", xpostag="ADP",
                  feats=None, head=6, deprel="case", deps=None, misc=None),
            Token(id="4", form="os", lemma="o", upostag="DET", xpostag="DET",
                  feats=OrderedDict([
                      ("Definite", "Def"), ("Gender", "Masc"),
                      ("Number", "Plur"), ("PronType", "Art")]),
                  head=6, deprel="det", deps=None, misc=None),
            Token(id="5", form="principais", lemma="principal",
                  upostag="ADJ", xpostag="ADJ", feats=OrderedDict([
                      ("Gender", "Masc"), ("Number", "Plur")]),
                  head=6, deprel="amod", deps=None, misc=None),
            Token(id="6", form="hotéis", lemma="hotél",
                  upostag="NOUN", xpostag="NOUN", feats=OrderedDict([
                      ("Gender", "Masc"), ("Number", "Plur")]),
                  head=2, deprel="nmod", deps=None, misc=None),
            Token(id="7", form="de", lemma="de", upostag="ADP", xpostag="ADP",
                  feats=None, head=9, deprel="case", deps=None, misc=None),
            Token(id="8", form="a", lemma="o", upostag="DET", xpostag="DET",
                  feats=OrderedDict([
                     ("Definite", "Def"), ("Gender", "Fem"),
                     ("Number", "Sing"), ("PronType", "Art")]),
                  head=9, deprel="det", deps=None, misc=None),
            Token(id="9", form="cidade", lemma="cidade",
                  upostag="NOUN", xpostag="NOUN", feats=OrderedDict([
                     ("Gender", "Fem"), ("Number", "Sing")]),
                  head=6, deprel="nmod", deps=None, misc=None),
            Token(id="10", form=".", lemma=".", upostag="PUNCT", xpostag=".",
                  feats=None, head=2, deprel="punct", deps=None, misc=None)
        ],
        contractions=[
            (
                Token(id="3-4", form="dos", lemma="_", upostag="_",
                      xpostag=None, feats=None, head=None, deprel="_",
                      deps=None, misc=None),
                2
            ),
            (
                Token(id="7-8", form="da", lemma="_", upostag="_",
                      xpostag=None, feats=None, head=None, deprel="_",
                      deps=None, misc=None),
                6
            )
        ],
        empty_nodes=[]
    )


@pytest.fixture
def parsed_sentence_with_empty_node():
    return Sentence(
        comments="# source_sent_id = . . email-enronsent28_01-0019\n# text = "
                 "By late 1974 investors were dizzy, they were desperate, "
                 "they were wrung-out, they had left Wall Street, many for "
                 "good.",
        tokens=[
            Token(
                id="1", form="By", lemma="by", upostag="ADP", xpostag="IN",
                feats=None, head=3, deprel="case", deps=None, misc=None),
            Token(
                id="2", form="late", lemma="late", upostag="ADJ",
                xpostag="JJ", feats=OrderedDict([
                    ('Degree', 'Pos')]),
                head=3, deprel="amod", deps=None, misc=None),
            Token(
                id="3", form="1974", lemma="1974", upostag="NUM",
                xpostag="CD", feats=OrderedDict([
                    ('NumType', 'Card')]),
                head=6, deprel="obl", deps=None, misc=None),
            Token(
                id="4", form="investors", lemma="investor", upostag="NOUN",
                xpostag="NNS", feats=OrderedDict([
                    ('Number', 'Plur')]),
                head=6, deprel="nsubj", deps=None, misc=None),
            Token(
                id="5", form="were", lemma="be", upostag="AUX", xpostag="VBD",
                feats=OrderedDict([
                    ('Mood', 'Ind'), ('Tense', 'Past'), ('VerbForm', 'Fin')]),
                head=6, deprel="cop", deps=None, misc=None),
            Token(
                id="6", form="dizzy", lemma="dizzy", upostag="ADJ",
                xpostag="JJ", feats=OrderedDict([
                    ('Degree', 'Pos')]),
                head=0, deprel="root", deps="SpaceAfter=No", misc=None),
            Token(
                id="7", form=",", lemma=",", upostag="PUNCT", xpostag=",",
                feats=None, head=10, deprel="punct",
                deps="_|CheckAttachment=6", misc=None),
            Token(
                id="8", form="they", lemma="they", upostag="PRON",
                xpostag="PRP", feats=OrderedDict([
                    ('Case', 'Nom'), ('Number', 'Plur'), ('Person', '3'),
                    ('PronType', 'Prs')]),
                head=10, deprel="nsubj", deps=None, misc=None),
            Token(
                id="9", form="were", lemma="be", upostag="AUX", xpostag="VBD",
                feats=OrderedDict([
                    ('Mood', 'Ind'), ('Tense', 'Past'), ('VerbForm', 'Fin')]),
                head=10, deprel="cop", deps=None, misc=None),
            Token(
                id="10", form="desperate", lemma="desperate", upostag="ADJ",
                xpostag="JJ", feats=OrderedDict([
                    ('Degree', 'Pos')]),
                head=6, deprel="conj",
                deps="SpaceAfter=No|CheckReln=parataxis", misc=None),
            Token(
                id="11", form=",", lemma=",", upostag="PUNCT", xpostag=",",
                feats=None, head=14, deprel="punct",
                deps="_|CheckAttachment=10", misc=None),
            Token(
                id="12", form="they", lemma="they", upostag="PRON",
                xpostag="PRP", feats=OrderedDict([
                    ('Case', 'Nom'), ('Number', 'Plur'), ('Person', '3'),
                    ('PronType', 'Prs')]),
                head=14, deprel="nsubj:pass", deps=None, misc=None),
            Token(
                id="13", form="were", lemma="be",
                upostag="AUX", xpostag="VBD",
                feats=OrderedDict([
                    ('Mood', 'Ind'), ('Tense', 'Past'), ('VerbForm', 'Fin')]),
                head=14, deprel="aux:pass", deps=None, misc=None),
            Token(
                id="14", form="wrung", lemma="wring", upostag="VERB",
                xpostag="VBN", feats=OrderedDict([
                    ('Tense', 'Past'), ('VerbForm', 'Part'),
                    ('Voice', 'Pass')]),
                head=6, deprel="conj",
                deps="SpaceAfter=No|CheckReln=parataxis", misc=None),
            Token(
                id="15", form="-", lemma="-", upostag="PUNCT", xpostag="HYPH",
                feats=None, head=14, deprel="punct", deps="SpaceAfter=No",
                misc=None),
            Token(
                id="16", form="out", lemma="out", upostag="ADP",
                xpostag="RP", feats=None, head=14, deprel="compound:prt",
                deps="SpaceAfter=No", misc=None),
            Token(
                id="17", form=",", lemma=",", upostag="PUNCT", xpostag=",",
                feats=None, head=20, deprel="punct",
                deps="_|CheckAttachment=6", misc=None),
            Token(
                id="18", form="they", lemma="they", upostag="PRON",
                xpostag="PRP", feats=OrderedDict([
                    ('Case', 'Nom'), ('Number', 'Plur'), ('Person', '3'),
                    ('PronType', 'Prs')]),
                head=20, deprel="nsubj", deps=None, misc=None),
            Token(
                id="19", form="had", lemma="have", upostag="AUX",
                xpostag="VBD", feats=OrderedDict([
                    ('Mood', 'Ind'), ('Tense', 'Past'), ('VerbForm', 'Fin')]),
                head=20, deprel="aux", deps=None, misc=None),
            Token(
                id="20", form="left", lemma="leave", upostag="VERB",
                xpostag="VBN", feats=OrderedDict([
                    ('Tense', 'Past'), ('VerbForm', 'Part')]),
                head=6, deprel="conj", deps="_|CheckReln=parataxis",
                misc=None),
            Token(
                id="21", form="Wall", lemma="Wall", upostag="PROPN",
                xpostag="NNP", feats=OrderedDict([
                    ('Number', 'Sing')]),
                head=22, deprel="compound", deps=None, misc=None),
            Token(
                id="22", form="Street", lemma="Street", upostag="PROPN",
                xpostag="NNP", feats=OrderedDict([
                    ('Number', 'Sing')]),
                head=20, deprel="obj", deps="SpaceAfter=No", misc=None),
            Token(
                id="23", form=",", lemma=",", upostag="PUNCT", xpostag=",",
                feats=None, head=20, deprel="punct",
                deps="_|CheckAttachment=22", misc=None),
            Token(
                id="24", form="many", lemma="many", upostag="ADJ",
                xpostag="JJ", feats=OrderedDict([
                    ('Degree', 'Pos')]),
                head=6, deprel="parataxis",
                deps="_|CheckAttachment=22|CheckReln=appos", misc=None),
            Token(
                id="25", form="for", lemma="for", upostag="ADP", xpostag="IN",
                feats=None, head=26, deprel="case", deps=None, misc=None),
            Token(
                id="26", form="good", lemma="good", upostag="ADJ",
                xpostag="JJ", feats=OrderedDict([
                    ('Degree', 'Pos')]),
                head=24, deprel="orphan", deps="SpaceAfter=No|CheckReln=nmod",
                misc=None),
            Token(
                id="27", form=".", lemma=".", upostag="PUNCT", xpostag=".",
                feats=None, head=6, deprel="punct", deps=None, misc=None)],
        contractions=[],
        empty_nodes=[(Token(
            id="24.1", form="left", lemma="left", upostag="VERB",
            xpostag="VBN", feats=OrderedDict([
                 ('Tense', 'Past'), ('VerbForm', 'Part')]),
            head=None, deprel="_", deps="CopyOf=6", misc=None), 23)])


@pytest.fixture
def parsed_sentence_from_file():
    return [
        Sentence
        (
            comments="# sent_id = 1\n# text = El objetivo de este trabajo ha "
                     "sido conocer si los valores de homocisteína influyen "
                     "en la evolución del GIM carotídeo en pacientes con "
                     "enfermedad coronaria.",
            tokens=[
                Token(
                    id="1", form="El", lemma="el", upostag="DET",
                    xpostag="DA0MS0", feats=OrderedDict([
                        ("Definite", "Def"), ("Gender", "Masc"),
                        ("Number", "Sing"), ("PronType", "Art")]),
                    head=2, deprel="det", deps=None, misc=None),
                Token(
                    id="2", form="objetivo", lemma="objetivo",
                    upostag="NOUN", xpostag="NCMS000",
                    feats=OrderedDict([
                        ("Gender", "Masc"), ("Number", "Sing")]), head=8,
                    deprel="nsubj:pass", deps=None, misc=None),
                Token(
                    id="3", form="de", lemma="de", upostag="ADP",
                    xpostag="SP", feats=OrderedDict([
                        ("AdpType", "Prep")]),
                    head=5, deprel="case", deps=None, misc=None),
                Token(
                    id="4", form="este", lemma="este", upostag="DET",
                    xpostag="DD0MS0", feats=OrderedDict([
                        ("Definite", "Def"), ("Gender", "Masc"),
                        ("Number", "Sing"), ("PronType", "Dem")]),
                    head=5, deprel="det", deps=None, misc=None),
                Token(
                    id="5", form="trabajo", lemma="trabajo", upostag="NOUN",
                    xpostag="NCMS000", feats=OrderedDict([
                        ("Gender", "Masc"), ("Number", "Sing")]),
                    head=2, deprel="nmod", deps=None, misc=None),
                Token(
                    id="6", form="ha", lemma="haber", upostag="AUX",
                    xpostag="VSIP3S0", feats=OrderedDict([
                        ("Mood", "Ind"), ("Number", "Sing"),
                        ("Person", "3"), ("Tense", "Pres")]),
                    head=8, deprel="aux", deps=None, misc=None),
                Token(
                    id="7", form="sido", lemma="ser", upostag="AUX",
                    xpostag="VSP00SM", feats=OrderedDict([
                        ("Gender", "Masc"), ("Number", "Sing"),
                        ("VerbForm", "Part")]),
                    head=8, deprel="aux:pass", deps=None, misc=None),
                Token(
                    id="8", form="conocer", lemma="conocer", upostag="VERB",
                    xpostag="VMN0000", feats=OrderedDict([
                        ("VerbForm", "Inf")]),
                    head=0, deprel="root", deps=None, misc=None),
                Token(
                    id="9", form="si", lemma="si", upostag="SCONJ",
                    xpostag="CS", feats=None, head=14, deprel="mark",
                    deps=None, misc=None),
                Token(
                    id="10", form="los", lemma="el", upostag="DET",
                    xpostag="DA0MP0", feats=OrderedDict([
                        ("Definite", "Def"), ("Gender", "Masc"),
                        ("Number", "Plur"), ("PronType", "Art")]),
                    head=11, deprel="det", deps=None, misc=None),
                Token(
                    id="11", form="valores", lemma="valor", upostag="NOUN",
                    xpostag="NCMP000", feats=OrderedDict([
                        ("Gender", "Masc"), ("Number", "Plur")]),
                    head=14, deprel="nsubj", deps=None, misc=None),
                Token(
                    id="12", form="de", lemma="de", upostag="ADP",
                    xpostag="SP", feats=OrderedDict([
                        ("AdpType", "Prep")]),
                    head=13, deprel="case", deps=None, misc=None),
                Token(
                    id="13", form="homocisteína", lemma="homocisteína",
                    upostag="NOUN", xpostag="NCFS000", feats=OrderedDict([
                        ("Gender", "Fem"), ("Number", "Sing")]),
                    head=11, deprel="nmod", deps=None, misc=None),
                Token(
                    id="14", form="influyen", lemma="influir", upostag="VERB",
                    xpostag="VMIP3P0", feats=OrderedDict([
                        ("Mood", "Ind"), ("Number", "Plur"), ("Person", "3"),
                        ("Tense", "Pres")]),
                    head=8, deprel="advcl", deps=None, misc=None),
                Token(
                    id="15", form="en", lemma="en", upostag="ADP",
                    xpostag="SP", feats=OrderedDict([
                        ("AdpType", "Prep")]),
                    head=17, deprel="case", deps=None, misc=None),
                Token(
                    id="16", form="la", lemma="el", upostag="DET",
                    xpostag="DA0FS0", feats=OrderedDict([
                        ("Definite", "Def"), ("Gender", "Fem"),
                        ("Number", "Sing"), ("PronType", "Art")]),
                    head=17, deprel="det", deps=None, misc=None),
                Token(
                    id="17", form="evolución", lemma="evolución",
                    upostag="NOUN", xpostag="NCFS000", feats=OrderedDict([
                        ("Gender", "Fem"), ("Number", "Sing")]),
                    head=14, deprel="obl", deps=None, misc=None),
                Token(
                    id="17-18", form="del", lemma="_", upostag="_",
                    xpostag=None, feats=None, head=None, deprel="_",
                    deps=None, misc=None),
                Token(
                    id="18", form="de", lemma="de", upostag="ADP",
                    xpostag="SP", feats=OrderedDict([
                        ("AdpType", "Prep")]),
                    head=20, deprel="case", deps=None, misc=None),
                Token(
                    id="19", form="el", lemma="el", upostag="DET",
                    xpostag="DA0MS0", feats=OrderedDict([
                        ("Definite", "Def"), ("Gender", "Masc"),
                        ("Number", "Sing"), ("PronType", "Art")]),
                    head=20, deprel="det", deps=None, misc=None),
                Token(
                    id="20", form="GIM", lemma="gim", upostag="PROPN",
                    xpostag="NP00000", feats=None, head=17, deprel="nmod",
                    deps=None, misc=None),
                Token(
                    id="21", form="carotídeo", lemma="carotídeo",
                    upostag="ADJ", xpostag="AQ0MS0", feats=OrderedDict([
                        ("Gender", "Masc"), ("Number", "Sing")]),
                    head=20, deprel="amod", deps=None, misc=None),
                Token(
                    id="22", form="en", lemma="en", upostag="ADP",
                    xpostag="SP", feats=OrderedDict([
                        ("AdpType", "Prep")]),
                    head=23, deprel="case", deps=None, misc=None),
                Token(
                    id="23", form="pacientes", lemma="paciente",
                    upostag="NOUN", xpostag="NCCP000", feats=OrderedDict([
                        ("Gender", "Com"), ("Number", "Plur")]),
                    head=8, deprel="obl", deps=None, misc=None),
                Token(
                    id="24", form="con", lemma="con", upostag="ADP",
                    xpostag="SP", feats=OrderedDict([
                        ("AdpType", "Prep")]),
                    head=25, deprel="case", deps=None, misc=None),
                Token(
                    id="25", form="enfermedad", lemma="enfermedad",
                    upostag="NOUN", xpostag="NCFS000", feats=OrderedDict([
                        ("Gender", "Fem"), ("Number", "Sing")]),
                    head=8, deprel="obl", deps=None, misc=None),
                Token(
                    id="26", form="coronaria", lemma="coronario",
                    upostag="ADJ", xpostag="AQ0FS0", feats=OrderedDict([
                        ("Gender", "Fem"), ("Number", "Sing")]),
                    head=25, deprel="amod", deps=None, misc=None),
                Token(
                    id="27", form=".", lemma=".", upostag="PUNCT",
                    xpostag="Fp", feats=None, head=8, deprel="punct",
                    deps=None, misc=None)
            ],
            contractions=[
                (
                    Token(
                        id="17-18", form="del", lemma="_", upostag="_",
                        xpostag=None, feats=None, head=None, deprel="_",
                        deps=None, misc=None),
                    16
                )
            ],
            empty_nodes=[]
        ),
        Sentence
        (
            comments="# sent_id = 2\n# text = La angiografía coronaria se "
                     "realizó a 164 pacientes.",
            tokens=[
                Token(
                    id="1", form="La", lemma="el", upostag="DET",
                    xpostag="DA0FS0", feats=OrderedDict([
                        ("Definite", "Def"), ("Gender", "Fem"),
                        ("Number", "Sing"), ("PronType", "Art")]),
                    head=2, deprel="det", deps=None, misc=None),
                Token(
                    id="2", form="angiografía", lemma="angiografía",
                    upostag="NOUN", xpostag="NCFS000", feats=OrderedDict([
                        ("Gender", "Fem"), ("Number", "Sing")]),
                    head=5, deprel="nsubj", deps=None, misc=None),
                Token(
                    id="3", form="coronaria", lemma="coronario",
                    upostag="ADJ", xpostag="AQ0FS0", feats=OrderedDict([
                        ("Gender", "Fem"), ("Number", "Sing")]),
                    head=2, deprel="amod", deps=None, misc=None),
                Token(
                    id="4", form="se", lemma="se", upostag="PRON",
                    xpostag="P00CN000", feats=None, head=5, deprel="iobj",
                    deps=None, misc=None),
                Token(
                    id="5", form="realizó", lemma="realizar", upostag="VERB",
                    xpostag="VMIS3S0", feats=OrderedDict([
                        ("Mood", "Ind"), ("Number", "Sing"),
                        ("Person", "3"), ("Tense", "Past")]),
                    head=0, deprel="root", deps=None, misc=None),
                Token(
                    id="6", form="a", lemma="a", upostag="ADP", xpostag="SP",
                    feats=OrderedDict([
                        ("AdpType", "Prep")]),
                    head=8, deprel="case", deps=None, misc=None),
                Token(
                    id="7", form="164", lemma="164", upostag="NUM",
                    xpostag="Z", feats=OrderedDict([
                        ("NumType", "Card")]),
                    head=8, deprel="nummod", deps=None, misc=None),
                Token(
                    id="8", form="pacientes", lemma="paciente",
                    upostag="NOUN", xpostag="NCCP000", feats=OrderedDict([
                        ("Gender", "Com"), ("Number", "Plur")]),
                    head=5, deprel="obl", deps=None, misc=None),
                Token(
                    id="9", form=".", lemma=".", upostag="PUNCT",
                    xpostag="Fp", feats=None, head=5, deprel="punct",
                    deps=None, misc=None)],
            contractions=[],
            empty_nodes=[]
        ),
        Sentence
        (
            comments="# sent_id = 3\n# text = Ningún paciente recibió "
                     "tratamiento vitamínico durante el estudio.",
            tokens=[
                Token(
                    id="1", form="Ningún", lemma="ninguno", upostag="DET",
                    xpostag="DI0MS0", feats=OrderedDict([
                        ("Definite", "Ind"), ("Gender", "Masc"),
                        ("Number", "Sing"), ("PronType", "Art")]),
                    head=2, deprel="det", deps=None, misc=None),
                Token(
                    id="2", form="paciente", lemma="paciente",
                    upostag="NOUN", xpostag="NCCS000", feats=OrderedDict([
                        ("Gender", "Com"), ("Number", "Sing")]),
                    head=3, deprel="nsubj", deps=None, misc=None),
                Token(
                    id="3", form="recibió", lemma="recibir", upostag="VERB",
                    xpostag="VMIS3S0", feats=OrderedDict([
                        ("Mood", "Ind"), ("Number", "Sing"), ("Person", "3"),
                        ("Tense", "Past")]),
                    head=0, deprel="root", deps=None, misc=None),
                Token(
                    id="4", form="tratamiento", lemma="tratamiento",
                    upostag="NOUN", xpostag="NCMS000", feats=OrderedDict([
                        ("Gender", "Masc"), ("Number", "Sing")]),
                    head=3, deprel="obj", deps=None, misc=None),
                Token(
                    id="5", form="vitamínico", lemma="vitamínico",
                    upostag="ADJ", xpostag="AQ0MS0", feats=OrderedDict([
                        ("Gender", "Masc"), ("Number", "Sing")]),
                    head=4, deprel="amod", deps=None, misc=None),
                Token(
                    id="6", form="durante", lemma="durante", upostag="ADP",
                    xpostag="SP", feats=OrderedDict([
                        ("AdpType", "Prep")]),
                    head=8, deprel="case", deps=None, misc=None),
                Token(
                    id="7", form="el", lemma="el", upostag="DET",
                    xpostag="DA0MS0", feats=OrderedDict([
                        ("Definite", "Def"), ("Gender", "Masc"),
                        ("Number", "Sing"), ("PronType", "Art")]),
                    head=8, deprel="det", deps=None, misc=None),
                Token(
                    id="8", form="estudio", lemma="estudio", upostag="NOUN",
                    xpostag="NCMS000", feats=OrderedDict([
                        ("Gender", "Masc"), ("Number", "Sing")]),
                    head=3, deprel="obl", deps=None, misc=None),
                Token(
                    id="9", form=".", lemma=".", upostag="PUNCT",
                    xpostag="Fp", feats=None, head=3, deprel="punct",
                    deps=None, misc=None)],
            contractions=[],
            empty_nodes=[]
        ),
    ]


@pytest.fixture
def lemmas():
    return [
        "o", "objetivo", "de", "o", "principal", "hotél", "de", "o",
        "cidade", "."
    ]


@pytest.fixture
def wordforms():
    return [
        "O", "objetivo", "de", "os", "principais", "hotéis", "de", "a",
        "cidade", "."
    ]


@pytest.fixture
def root():
    return Token(
        id="2", form="objetivo", lemma="objetivo", upostag="NOUN",
        xpostag="NOUN", feats=OrderedDict([
            ("Gender", "Masc"), ("Number", "Sing")]),
        head=0, deprel="root", deps=None, misc=None)


@pytest.fixture
def sentence_from_wordforms():
    return "O objetivo de os principais hotéis de a cidade ."


@pytest.fixture
def sentence_from_comments():
    return (
        "El objetivo de este trabajo ha sido conocer si los valores de "
        "homocisteína influyen en la evolución del GIM carotídeo en pacientes "
        "con enfermedad coronaria."
    )


@pytest.fixture
def headdeps():
    return [
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


@pytest.fixture
def headdeps_nmod():
    return [
        HeadDep(
            head="objetivo", dep="hotél", relation="nmod", position=(1, 5)
        ),
        HeadDep(head="hotél", dep="cidade", relation="nmod", position=(5, 8))
    ]


@pytest.fixture
def heads():
    return [
        {
            "id": "9", "tag": "NOUN", "lemma": "cidade", "deps": [
                {
                    "pos": "ADP", "form": "de", "tag": "ADP",
                    "lemma": "de", "deprel": "case"
                },
                {
                    "pos": "DET", "form": "a", "tag": "DET",
                    "lemma": "o", "deprel": "det"
                }
            ]
        },
        {
            "id": "2", "tag": "NOUN", "lemma": "objetivo", "deps": [
                {
                    "pos": "DET", "form": "O", "tag": "DET",
                    "lemma": "o", "deprel": "det"
                },
                {
                    "pos": "NOUN", "form": "hotéis", "tag": "NOUN",
                    "lemma": "hotél", "deprel": "nmod"
                },
                {
                    "pos": ".", "form": ".", "tag": "PUNCT",
                    "lemma": ".", "deprel": "punct"
                }
            ]
        },
        {
            "id": "6", "tag": "NOUN", "lemma": "hotél", "deps": [
                {
                    "pos": "ADP", "form": "de", "tag": "ADP",
                    "lemma": "de", "deprel": "case"
                },
                {
                    "pos": "DET", "form": "os", "tag": "DET",
                    "lemma": "o", "deprel": "det"
                },
                {
                    "pos": "ADJ", "form": "principais", "tag": "ADJ",
                    "lemma": "principal", "deprel": "amod"
                },
                {
                    "pos": "NOUN", "form": "cidade", "tag": "NOUN",
                    "lemma": "cidade", "deprel": "nmod"
                }
            ]
        }
    ]


@pytest.fixture
def deps():
    return [
        {
            "tag": "ADP", "form": "de", "deprel": "case",
            "lemma": "de", "pos": "ADP"
        },
        {
            "tag": "DET", "form": "os", "deprel": "det",
            "lemma": "o", "pos": "DET"
        },
        {
            "tag": "ADJ", "form": "principais", "deprel": "amod",
            "lemma": "principal", "pos": "ADJ"
        },
        {
            "tag": "NOUN", "form": "cidade", "deprel": "nmod",
            "lemma": "cidade", "pos": "NOUN"
        }
    ]


@pytest.fixture
def sentence_with_errors():
    return """O o DET
objetivo objetivo NOUN
de de ADP
o o DET
principais principal ADJ
hotéis hotél NOUN
"""


@pytest.fixture
def line_with_errors():
    return "5\tprincipais\tprincipal\tADJ\n"
