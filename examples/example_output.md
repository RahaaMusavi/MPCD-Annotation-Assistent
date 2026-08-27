## Q: How to annotate xcomp?

## A: MPCD Annotation Assistant
### xcomp (open clausal complement): How to Annotate
#### Definition and Annotation Protocol

**MPCD** Annotation Assistant xcomp (open clausal complement): How to Annotate Definition and Annotation Protocol *xcomp* (open clausal complement) is used for a predicative or clausal complement that does not have its own overt subject. The subject of the xcomp is controlled by an argument of the main verb (either the subject or object). Typical examples include infinitival complements of modal verbs, causatives, and verbs of perception.

Key annotation points:

The xcomp is a core argument of the main verb, not an adjunct. The dependent verb or predicative element is annotated as *xcomp* and is directly dependent on the main verb. The subject of the xcomp is not overtly expressed within the xcomp clause; it is controlled by the matrix clause. In modal constructions, the infinitive is annotated as *xcomp* to the modal verb. Supporting quotation: "open clausal complement: predicative or clausal complement without its own subject".

### Middle Persian Examples

## Modal verb with infinitive (MX 2.103) čē=t pad frazām hamāg abāyēd hištan *because in the end you must leave all (behind)*

word	ID	head	**DEPREL**
čē	1	6	cc
=t	2	6	nsubj
pad	3	4	case
frazām	4	7	obl
hamāg	5	7	obj
abāyēd	6	0	root
hištan	7	6	xcomp
Here, hištan (*to leave*) is annotated as xcomp to the modal verb abāyēd (*must*).

## Modal verb with infinitive and negation (Dk6 1.89)

ka amā tis pad=iš nē tuwān būd kirdan *if we could not do something for him*

word	ID	head	**DEPREL**
ka	1	7	mark
amā	2	7	nsubj
tis	3	9	obj
pad	4	5	case
=iš	5	9	obl
nē	6	7	advmod
tuwān	7		advcl
būd	8	7	aux
kirdan	9	7	xcomp
Here, kirdan (*to do*) is annotated as xcomp to tuwān (*could*).

### Additional Details

"The infinitive clause is set in 'xcomp'-relation to the modal verb that forms the root of its clause*. *Modal verbs are treated as full verbs. Thus, if they are modified by temporal auxiliaries (e.g. tuwān būd), the temporal auxiliary is related to the modal auxiliary. The infinitive clause is set in 'xcomp'-relation to the modal verb that forms the root of its clause*. *obligatory subject & object predicatives: She looked fantastic. She became angry. This made me angry. optional resultative predicatives: She painted the house blue. The dog barked the neighbors awake." (all xcomp). Summary of Steps Identify the main verb (often a modal or causative). Identify the dependent verb or predicative element that lacks its own subject. Annotate the dependent as *xcomp* to the main verb. Ensure the subject of the xcomp is controlled by the matrix clause. References "open clausal complement: predicative or clausal complement without its own subject* *The infinitive clause is set in 'xcomp'-relation to the modal verb that forms the root of its clause" Modal verb example: MX 2.**103** Modal verb with negation: Dk6 1.89 Full sentence context (from corpus) AŌD-**K20** 92

Surface text: čē awēšān kē nēst pad ārzōg xwāhēnd ud pad awištāb

Translation: [deu] [TJ] Denn diejenigen, die (es) nicht haben, sehnen (es) begierig herbei und unter Druck.

ID	**FORM**	**LEMMA**	**UPOS**	**HEAD**	**DEPREL**	**DEPS**	**SENSE**
1	čē	čē	**CCONJ**	7	cc	_	because, for
2	awēšān	awēšān	**PRON**	7	nsubj	[('obl', 4)]	those
3	kē	kē	**SCONJ**	4	mark	[('ref', 2)]	who
4	nēst	h	**VERB**	2	acl:relcl	_	to be there
5	pad	pad	**ADP**	6	case	_	in
6	ārzōg	ārzōg	**NOUN**	7	obl	_	desire
7	xwāhēnd	xwāstan	**VERB**	0	root	_	to seek, aspire to, search for
8	ud	ud	**CCONJ**	10	cc	_	and
9	pad	pad	**ADP**	10	case	_	in
10	awištāb	aweštāb	**NOUN**	6	conj	[('obl', 7)]	oppression
GBd-**TD1** 51

Surface text: u =š guft ohrmazd kū nē harwispkirdār hā gannāgmēnōy kū =t man nē tuwān murnǰēnīdan u =š dām ī =z man ēdōn nē tuwān kirdan kū abāz ō xwēšīh man nē rasēnd

Translation: (Du) mögest nicht allmächtig sein, Übler Geist, sodass du mich nicht vernichten kannst und [wörtl.: er, ev. Fehler für du] kannst auch nicht meine Schöpfung so machen, dass (sie) nicht zu mir selbst zurückkommen!

ID	**FORM**	**LEMMA**	**UPOS**	**HEAD**	**DEPREL**	**DEPS**	**SENSE**
1	u	ud	**CCONJ**	3	cc	_	and
2	=š	ōy	**PRON**	3	nsubj	_	he
3	guft	guftan	**VERB**	0	root	_	say
4	ohrmazd	ohrmazd	**PROPN**	3	dislocated:topic	_	Ohrmazd (god)
5	kū	kū	**SCONJ**	7	mark	_	that
6	nē	nē	**PART**	7	advmod	_	not
7	harwispkirdār	harwispkirdār	**ADJ**	3	ccomp	_	allmighty
8	hā	h	**AUX**	7	cop	_	be
9	gannāgmēnōy	gannāgmēnōy	**PROPN**	7	vocative	_	Foul Spirit
10	kū	kū	**SCONJ**	14	mark	_	so that
11	=t	tō	**PRON**	14	nsubj	[('nsubj:xsubj', 15)]	you
12	man	man	**PRON**	15	obj	_	I
13	nē	nē	**PART**	14	advmod	_	not
14	tuwān	tuwān	**VERB**	7	advcl	_	be able
15	murnǰēnīdan	murnǰēnīdan	**VERB**	14	xcomp	_	to destroy, wreck
16	u	ud	**CCONJ**	24	cc	_	and
17	=š	ōy	**PRON**	24	nsubj	[('nsubj:xsubj', 25)]	he
18	dām	dām1	**NOUN**	25	obj	_	creature
19	ī	ī	**DET**	21	det	_	ezafe
20	=z	=iz	**ADV**	18	advmod	_	also
21	man	man	**PRON**	18	nmod	_	I
22	ēdōn	ēdōn	**ADV**	25	advmod	_	thus
23	nē	nē	**PART**	24	advmod	_	not
24	tuwān	tuwān	**VERB**	14	conj	[('advcl', 7)]	be able
25	kirdan	kirdan	**VERB**	24	xcomp	_	to make
26	kū	kū	**SCONJ**	32	mark	_	so that
27	abāz	abāz	**ADV**	28	advmod	_	back
28	ō	ō	**ADP**	29	case	_	to
29	xwēšīh	xwēšīh	**NOUN**	32	obl	_	ownness
30	man	man	**PRON**	29	nmod	_	I
31	nē	nē	**PART**	32	advmod	_	not
32	rasēnd	rasīdan	**VERB**	25	xcomp	_	to arrive, get to
AŌD-**K20** 1

Surface text: pursīd hašāgird ōšnar ī dānāg kū ēk tā hazār harw mārīg ē rāy saxwan =ē pad frahang be gōw

Translation: "Da uno a mille, per ogni parola pronuncia discorsi ricchi di insegnamenti [...]".

ID	**FORM**	**LEMMA**	**UPOS**	**HEAD**	**DEPREL**	**DEPS**	**SENSE**
1	pursīd	pursīdan	**VERB**	0	root	_	to ask
2	hašāgird	hašāgird	**NOUN**	1	nsubj	_	disciple
3	ōšnar	ōšnar	**PROPN**	1	iobj	_	Ōšnar
4	ī	ī	**DET**	5	det	_	ezafe
5	dānāg	dānāg	**ADJ**	3	amod	_	wise
6	kū	kū	**SCONJ**	19	mark	_	that
7	ēk	ēk	**NUM**	19	obl	_	one
8	tā	tā	**ADP**	9	case	_	up to, until
9	hazār	hazār	**NUM**	7	conj	_	thousand
10	harw	harw	**DET**	11	det	_	every
11	mārīg	mārīg2	**NOUN**	19	obl	_	saying
12	ē	ēw1	**NUM**	11	nummod	_	single
13	rāy	rāy1	**ADP**	11	case	_	for (the sake of), in order to
14	saxwan	saxwan	**NOUN**	19	obj	_	discourse
15	=ē	ēw1	**NUM**	14	nummod	_	one
16	pad	pad	**ADP**	17	case	_	as to, regarding, concerning
17	frahang	frahang	**NOUN**	19	obl	_	education
18	be	be	**PART**	19	advmod	_	**PFV**, **SBJV**
19	gōw	guftan	**VERB**	1	ccomp	_	to utter, speak, mention
**DMX**-K43a **140**

Surface text: čē =t pad frazām hamāg abāyēd hištan

Translation: [deu] Denn zum Ende musst du alles zurücklassen!

ID	**FORM**	**LEMMA**	**UPOS**	**HEAD**	**DEPREL**	**DEPS**	**SENSE**
1	čē	čē	**CCONJ**	6	cc	_	because, for
2	=t	tō	**PRON**	6	obl	[('nsubj:xsubj', 7)]	you
3	pad	pad	**ADP**	4	case	_	in
4	frazām	frazām	**NOUN**	6	obl	_	conclusion
5	hamāg	hamāg	**PRON**	7	obj	_	all
6	abāyēd	abāyistan	**VERB**	0	root	_	must
7	hištan	hištan	**VERB**	6	xcomp	_	to leave behind
Dk5-B **110**

Surface text: xwābar dādār ud hamāg hušnūd zīndag abāz kunēd

Translation: [deu] Der segensreiche Schöpfer wird wieder lebendig machen.

ID	**FORM**	**LEMMA**	**UPOS**	**HEAD**	**DEPREL**	**DEPS**	**SENSE**
1	xwābar	xwābar	**ADJ**	2	amod	_	beneficent
2	dādār	dādār	**NOUN**	8	nsubj	_	creator
3	ud	ud	**CCONJ**	4	cc:nc	_	X
4	hamāg	hamāg	**PRON**	8	obj	_	all
5	hušnūd	hušnūd	**ADJ**	8	xcomp	_	well-satisfied, contented
6	zīndag	zīwandag	**ADJ**	5	conj	[('xcomp', 8)]	alive
7	abāz	abāz	**ADV**	8	advmod	_	again
8	kunēd	kirdan	**VERB**	0	root	_	to make
AŌD-**K20** 19

Surface text: az ēn dō tis šarm nē abāyēd kirdan ēk az wēmārīh ud ud dudīgar az xwēšāwand ī driyōš ,

Translation: one is sickness and the other, a poor relative.

ID	**FORM**	**LEMMA**	**UPOS**	**HEAD**	**DEPREL**	**DEPS**	**SENSE**
1	az	az1	**ADP**	4	case	_	following, out of, due to
2	ēn	ēn	**DET**	4	det	_	this
3	dō	dō	**NUM**	4	nummod	_	two
4	tis	tis1	**NOUN**	8	obl	_	thing
5	šarm	šarm	**NOUN**	8	compound:lvc	_	shame
6	nē	nē	**PART**	7	advmod	_	not
7	abāyēd	abāyistan	**VERB**	0	root	_	shall
8	kirdan	kirdan	**VERB**	7	xcomp	_	to make
9	ēk	ēk	**NUM**	11	advmod	_	one
10	az	az1	**ADP**	11	case	_	following, out of, due to
11	wēmārīh	wēmārīh	**NOUN**	7	advcl	_	illness, sickness
12	ud	ud	**CCONJ**	16	cc	_	and
13	ud	ud	**CCONJ**	12	dep	_	X
14	dudīgar	didīgar	**ADV**	16	advmod	_	other
15	az	az1	**ADP**	16	case	_	following, out of, due to
16	xwēšāwand	xwēšāwand	**NOUN**	11	conj	_	relative
17	ī	ī	**DET**	18	det	_	ezafe
18	driyōš	driyōš	**ADJ**	16	amod	_	poor, needy
19	,	,	**PUNCT**	7	punct	_	,
DD-**K35** 17

Surface text: agar andar ēn zamānag ud šahr X šnāxtag ud āšnāg abar kas agar pad ōy ī dagr wurrōyišnīh dēnpēšōbāy pāzag man xwēš rāy nē ābrōyīg dāram ka ān stāyišn ī sālār =imān ēwāzīg hāzag abar man srawāgīhēd nē =z rāmišnīg , bawam ka =m meh ī az xwēš sālār nāmēnēnd

Translation: [eng] [JD] If at this time and these countries which are known and with which we are acquainted, there is a great person who is the +chief +leader of the religion on account of his steadfast belief; then I do not regard it as honourable for myself when praise as ‘our only proper leader’ is broadcast about me, and I am not pleased when they (i.e. people) call me greater than their own leader.

ID	**FORM**	**LEMMA**	**UPOS**	**HEAD**	**DEPREL**	**DEPS**	**SENSE**
1	agar	agar	**SCONJ**	8	mark	_	if
2	andar	andar	**ADP**	4	case	_	in
3	ēn	ēn	**DET**	4	det	[('det', 6)]	this
4	zamānag	zamānag	**NOUN**	8	obl	[('obl', 10)]	time
5	ud	ud	**CCONJ**	6	cc	_	and
6	šahr	šahr	**NOUN**	4	conj	[('obl', 8), ('obl', 10)]	land, country
7	X	§	**NOUN**	8	nsubj	[('nsubj', 10)]	§
8	šnāxtag	šnāxtag	**ADJ**	26	advcl	_	popular
9	ud	ud	**CCONJ**	10	cc	_	and
10	āšnāg	āšnāg	**ADJ**	8	conj	[('advcl', 26)]	known (as a fact)
11	abar	abar1	**ADP**	12	case	_	on, about
12	kas	kas	**PRON**	10	obl	_	person
13	agar	agar	**SCONJ**	20	mark	_	if
14	pad	pad	**ADP**	18	case	_	as to, regarding, concerning
15	ōy	ōy	**PRON**	18	det	_	that
16	ī	ī	**DET**	17	det	_	ezafe
17	dagr	dagr	**ADJ**	18	amod	_	steady
18	wurrōyišnīh	wurrawišnīh	**NOUN**	20	obl	_	belief
19	dēnpēšōbāy	dēnpēšōbāy	**NOUN**	20	nsubj	_	Leader of the religion
20	pāzag	pāzag	**ADJ**	26	advcl	_	sincere
21	man	man	**PRON**	26	nsubj	[('nsubj', 42), ('nsubj:xsubj', 40)]	I
22	xwēš	xwēš	**PRON**	25	obl	_	own
23	rāy	rāy1	**ADP**	22	case	_	for
24	nē	nē	**PART**	25	advmod	_	not
25	ābrōyīg	ābrōyīg	**ADJ**	26	xcomp	_	honourable
26	dāram	dāštan	**VERB**	0	root	_	to consider
27	ka	ka	**SCONJ**	37	mark	_	when
28	ān	ān	**DET**	29	det	_	that
29	stāyišn	stāyišn	**NOUN**	37	nsubj	_	praise
30	ī	ī	**DET**	31	det	_	ezafe
31	sālār	sālār	**NOUN**	29	nmod	[('nsubj:xsubj', 33)]	leader
32	=imān	amāh	**PRON**	31	nmod	_	we
33	ēwāzīg	ēwāzīg	**ADJ**	34	advcl	[('acl', 31)]	sole
34	hāzag	hāzag	**ADJ**	31	amod	_	leading
35	abar	abar1	**ADP**	36	case	_	on, about
36	man	man	**PRON**	37	obl	_	I
37	srawāgīhēd	srawāgīhistan	**VERB**	26	advcl	_	to be (loudly) announced, proclaimed
38	nē	nē	**PART**	42	advmod	_	not
39	=z	=iz	**ADV**	38	advmod	_	also
40	rāmišnīg	rāmišnīg	**ADJ**	42	xcomp	[('acl', 21)]	delighted
41	,	,	**PUNCT**	42	punct	_	,
42	bawam	būdan	**VERB**	26	conj	_	become
43	ka	ka	**SCONJ**	50	mark	_	when
44	=m	man	**PRON**	50	obj	[('nsubj:xsubj', 45)]	I
45	meh	meh	**ADJ**	50	xcomp	[('acl', 44)]	greater
46	ī	ī	**DET**	49	det	_	ezafe
47	az	az1	**ADP**	49	case	_	than
48	xwēš	xwēš	**PRON**	49	det	_	own
49	sālār	sālār	**NOUN**	45	nmod	_	leader
50	nāmēnēnd	nāmēnīdan	**VERB**	42	advcl	_	name
GA-**K20** 74

Surface text: ud amā =z pad mēnōyīg kirdārīh be zadan ī druz ī mēnōyīg čiyōn wēmārīh ud tab ud seǰ ud xešm niyāzīg hom ō ātaxš

Translation: [eng] [RM] And (so) we are in need of fire in spiritual activiti(es) for smiting the spritual deceit-demon such as illness, and fever, and danger, and anger.

ID	**FORM**	**LEMMA**	**UPOS**	**HEAD**	**DEPREL**	**DEPS**	**SENSE**
1	ud	ud	**CCONJ**	21	cc	_	and
2	amā	amāh	**PRON**	21	nsubj	_	we
3	=z	=iz	**ADV**	2	advmod	_	also
4	pad	pad	**ADP**	6	case	_	in
5	mēnōyīg	mēnōyīg	**ADJ**	6	amod	_	belonging to the mēnōy world, spiritual
6	kirdārīh	kirdārīh	**NOUN**	21	obl	_	activity
7	be	be	**PART**	8	advmod	_	**PFV**, **SBJV**
8	zadan	zadan	**NOUN**	6	nmod	_	defeating, beating
9	ī	ī	**DET**	10	det	_	ezafe
10	druz	druz	**NOUN**	8	nmod	_	demon, demonic being
11	ī	ī	**DET**	12	det	_	ezafe
12	mēnōyīg	mēnōyīg	**ADJ**	10	amod	_	belonging to the mēnōy world, spiritual
13	čiyōn	čiyōn	**ADP**	14	case	_	like, such as
14	wēmārīh	wēmārīh	**NOUN**	10	nmod	_	illness, sickness
15	ud	ud	**CCONJ**	16	cc	_	and
16	tab	tab	**NOUN**	14	conj	_	fever
17	ud	ud	**CCONJ**	18	cc	_	and
18	seǰ	seǰ	**NOUN**	14	conj	_	danger, peril
19	ud	ud	**CCONJ**	20	cc	_	and
20	xešm	xēšm	**NOUN**	14	conj	_	anger
21	niyāzīg	niyāzīg	**ADJ**	0	root	_	in want, needy
22	hom	h	**AUX**	21	cop	_	be
23	ō	ō	**ADP**	24	case	_	to
24	ātaxš	ātaxš	**NOUN**	21	obl	_	fire
AŌD-**K20** 15

Surface text: dō hēnd kē xwēštan tar nē kunēnd ēk kē X društāwāzīhā saxwan ō kasān nē gōwēd ud dudīgar kē az wattarān tis nē xwāhēd

Translation: one is that one should not address a speech to others with a stern voice and the other is that one should not ask a thing of the wicked.

ID	**FORM**	**LEMMA**	**UPOS**	**HEAD**	**DEPREL**	**DEPS**	**SENSE**
1	dō	dō	**NUM**	0	root	[('nsubj', 7)]	two
2	hēnd	h	**AUX**	1	cop	_	be
3	kē	kē	**SCONJ**	7	mark	[('ref', 1)]	who
4	xwēštan	xwēštan	**PRON**	7	obj	_	oneself
5	tar	tar	**ADV**	7	xcomp	_	adverse, wrong
6	nē	nē	**PART**	7	advmod	_	not
7	kunēnd	kirdan	**VERB**	1	acl:relcl	_	to do
8	ēk	ēk	**NUM**	_	_	_	one
9	kē	kē	**PRON**	_	_	_	who
10	X	$	X	_	_	_	$
11	društāwāzīhā	društāwāzīhā	**ADV**	_	_	_	with a harsh voice
12	saxwan	saxwan	**NOUN**	_	_	_	word
13	ō	ō	**ADP**	14	case	_	to
14	kasān	kas	**PRON**	_	_	_	other
15	nē	nē	**PART**	_	_	_	not
16	gōwēd	§	_	_	_	_	§
17	ud	§	_	_	_	_	§
18	dudīgar	§	_	_	_	_	§
19	kē	§	_	_	_	_	§
20	az	az1	**ADP**	21	case	_	from, out of
21	wattarān	wattar	**NOUN**	24	obl	_	bad person
22	tis	tis1	**PRON**	24	obj	_	something
23	nē	nē	**PART**	24	advmod	_	not
24	xwāhēd	xwāstan	**VERB**	_	_	_	to ask for, request
AŌD-**K20** 7

Surface text: ēk tis az =iš būdan nē šāyēd kunišn ī xwēš

Translation: [eng][BP] [Dhabhar **1930**] One thing is oneˈs own action without which it is impossible to exist.

ID	**FORM**	**LEMMA**	**UPOS**	**HEAD**	**DEPREL**	**DEPS**	**SENSE**
1	ēk	ēk	**NUM**	8	advmod	_	one
2	tis	tis1	**NOUN**	8	nsubj	[('nsubj', 7), ('nsubj:xsubj', 5)]	aspect
3	az	az1	**ADP**	4	case	_	from
4	=iš	ōy	**PRON**	5	obl	_	it
5	būdan	būdan	**VERB**	7	xcomp	_	to emerge, come into being
6	nē	nē	**PART**	7	advmod	_	not
7	šāyēd	šāyistan	**VERB**	2	acl:relcl	_	be able
8	kunišn	kunišn	**NOUN**	0	root	_	doing
9	ī	ī	**DET**	10	det	_	ezafe
10	xwēš	xwēš	**PRON**	8	nmod	_	own
AŌD-**K20** 3

Surface text: ud ēk pad kirdan be harw kār kē pašēmān nē bawēd kirbag

Translation: [eng][BP] [Dhabhar **1930**] One is a meritorious deed (to be done) while doing every duty, whereof one may not repent.

ID	**FORM**	**LEMMA**	**UPOS**	**HEAD**	**DEPREL**	**DEPS**	**SENSE**
1	ud	ud	**CCONJ**	7	cc	_	and
2	ēk	ēk	**NUM**	7	advmod	_	one
3	pad	pad	**ADP**	4	case	_	in, at (temporal)
4	kirdan	kirdan	**NOUN**	7	obl	_	acting
5	be	pad	**ADP**	7	dep	_	as to, regarding, concerning
6	harw	harw	**DET**	7	det	_	every
7	kār	kār1	**NOUN**	0	root	[('obl', 9)]	deed
8	kē	kē	**SCONJ**	11	mark	[('ref', 7)]	which
9	pašēmān	pašēmān	**ADJ**	11	xcomp	_	repentant
10	nē	nē	**PART**	11	advmod	_	not
11	bawēd	būdan	**VERB**	7	acl:relcl	_	to become, turn to
12	kirbag	kirbag1	**NOUN**	7	nsubj	_	good deed
AŌD-**K20** 95

Surface text: ud xwāstag pad mar ī paymān weh andčand petyārag az tan abāz dāštan tuwān

Translation: [eng] The wealth to be taken into consideration should be acquired with good moderation as much as can keep away calamities from oneˈs person.

ID	**FORM**	**LEMMA**	**UPOS**	**HEAD**	**DEPREL**	**DEPS**	**SENSE**
1	ud	ud	**CCONJ**	7	cc	_	and
2	xwāstag	xwāstag	**NOUN**	7	nsubj	_	property, wealth
3	pad	pad	**ADP**	4	case	_	in
4	mar	mar1	**NOUN**	7	obl	_	amount
5	ī	ī	**DET**	6	det	_	ezafe
6	paymān	paymān	**NOUN**	4	nmod	_	measure
7	weh	weh	**ADJ**	0	root	_	better
8	andčand	andčand	**ADV**	13	advmod	_	as much as
9	petyārag	petyārag	**NOUN**	13	obj	_	misfortune
10	az	az1	**ADP**	11	case	_	from
11	tan	tan	**PRON**	13	obl	_	self
12	abāz	abāz	**ADV**	13	advmod	_	back
13	dāštan	dāštan	**VERB**	14	xcomp	_	to hold, keep
14	tuwān	tuwān	**AUX**	7	advcl	_	be able
DD-**K35** 66

Surface text: ēk abēzag mard gayōmard kē =š fradom menišnīg stāyīdār būd

Translation: [eng] [JD] One is the pure man, Gayōmart, who was the first to praise ... with his +mind.

ID	**FORM**	**LEMMA**	**UPOS**	**HEAD**	**DEPREL**	**DEPS**	**SENSE**
1	ēk	ēk	**NUM**	3	nsubj	_	one
2	abēzag	abēzag	**ADJ**	3	amod	_	pure
3	mard	mard	**NOUN**	0	root	_	man, human
4	gayōmard	gayōmart	**PROPN**	3	appos	[('nsubj', 9)]	Gayōmart
5	kē	kē	**SCONJ**	9	mark	[('ref', 4)]	who
6	=š	ōy	**PRON**	9	obj	_	he
7	fradom	fradom	**ADJ**	9	advmod	_	first
8	menišnīg	menišnīg	**ADJ**	9	advmod	_	mental, in thought
9	stāyīdār	stāyīdār	**NOUN**	3	acl:relcl	_	praiser
10	būd	būdan	**AUX**	9	aux	_	to be
Your message:
Ask a question about syntax or morphology...
Send
Clear
Logout
RunsRuns
- Use via APIlogo
- Built with Gradiologo
- SettingsSettings
