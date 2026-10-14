                                                      From Dependency to Compositionality:
                                             A Neurosymbolic Lifting of LLM Outputs via Combinatory
                                                              Categorial Grammar
                                                                                     Remo Pareschi
                                                                  STAKE Lab, University of Molise, Campobasso, Italy
                                                                   Corresponding author: remo.pareschi@unimol.it
                                                                            ORCID: 0000-0002-4912-582X


                                                                                         Abstract
                                                   Large language models (LLMs) generate fluent text by incrementally predicting the
                                               next token from a prefix. Critics in the generative tradition argue that such systems lack
                                               genuine grammar; influential replies from the dependency-grammar perspective hold that
arXiv:2607.18961v2 [cs.AI] 22 Jul 2026




                                               LLM behavior is well described by local head–dependent structure built word by word. We
                                               argue that a sharper observation has been overlooked: the prefix-driven, type-completing
                                               dynamics of autoregressive generation align closely with the incremental processing model
                                               that Combinatory Categorial Grammar (CCG) was originally designed to support. On this
                                               basis we propose a neurosymbolic framework in which LLM outputs are lifted into typed
                                               compositional derivations — not claiming that LLMs implement CCG internally, but that
                                               their outputs admit a principled, incremental, and auditable CCG reconstruction. Two
                                               consequences follow. First, through the Curry–Howard correspondence the lifting extends
                                               beyond natural language to the formal languages LLMs also produce — programming
                                               languages such as Solidity, description-logic and query languages such as OWL and SQL —
                                               with the type system varying and the architecture held fixed. Second, the lifting supports
                                               two layers of checking: a compositional layer that catches structural failures directly, and a
                                               content layer that checks the lifted structure against external knowledge sources, enabling the
                                               earliest possible flagging of hallucinated content. The account thereby requires of a producer
                                               not cognition but a prefix-driven generative profile. We close with a sketch of synchronous
                                               LLM–CCG coupling as one direction the framework opens.

                                         Keywords: large language models; Combinatory Categorial Grammar; neurosymbolic AI;
                                         compositional semantics; hallucination detection; smart contracts


                                         1    Introduction
                                         The success of large language models (LLMs) has reopened, in an unexpected form, a number of
                                         classical disputes of theoretical linguistics. The fluency and broad syntactic competence of these
                                         systems have led many observers to regard them as evidence that grammatical regularities can
                                         emerge from large-scale statistical learning. Critics in the generative tradition have replied that
                                         such systems remain fundamentally grammarless: that they manipulate word sequences without
                                         possessing structured principles of the kind that underwrite genuine linguistic knowledge.
                                             A recent and influential reply to this critique has come from psycholinguistic work in the
                                         dependency-grammar tradition, most prominently associated with Edward Gibson. On this view,
                                         the surface behavior of LLMs is well described by local head–dependent relations that are formed
                                         incrementally as words are processed, and many of the empirical regularities observed both in
                                         human comprehension and in LLM behavior follow from a single principle of dependency locality
                                         (Gibson, 1998; Futrell et al., 2020; Gibson, 2025). This shifts the debate away from the binary
                                         question of whether LLMs “have grammar,” toward the more precise question of whether their

                                                                                             1
observable behavior admits a recoverable grammatical organization. In that respect, dependency
grammar offers a compelling first layer of interpretation.
     The present paper begins with the observation that, while this dependency-based reply is well
taken, it leaves an even more interesting convergence unstated. Autoregressive LLMs operate
prefix by prefix: at each step they maintain a representation of what has been produced so far and
predict what could come next. Combinatory Categorial Grammar (CCG), as developed by Mark
Steedman and colleagues, was designed precisely to support such a left-to-right, prefix-driven,
type-completing notion of processing (Ades and Steedman, 1982; Steedman, 2000, 2011). In
CCG, partial expressions receive principled syntactic and semantic types — “John loves” is not
an ill-formed fragment but a category S/N P with an associated lambda term — and well-defined
combinatory rules govern how those types extend as new material arrives. The same incremental,
predictive, prefix-completing dynamic that LLMs realize statistically is one that CCG was built
to describe formally.
     This convergence is, we believe, the more productive locus for understanding what LLMs
do and what one can do with their output. Dependency grammar describes which words have
been linked to which; CCG describes, in addition, what is still missing, with what type, and
how meaning will compose when it arrives. Where dependency analysis recovers local structure,
CCG recovers the predictive scaffolding of a compositional interpretation. For an autoregressive
system whose entire operational character is predictive, this is not a marginal difference.
     We exploit this convergence in a specific way. Rather than claiming that LLMs internally
implement CCG — a strong empirical claim we do not undertake to defend — we treat CCG as
a lifting mechanism applied to LLM outputs. The idea is post hoc but principled. A sentence
produced by an LLM is parsed into a CCG derivation by an existing CCG semantic parser of
the kind exemplified by ccg2lambda (Martínez-Gómez et al., 2016; Mineshima et al., 2015); the
derivation yields a lambda-style logical form. The result is a pipeline that maps fluent-generated
text into typed, compositional symbolic objects whose internal structure is transparent and
auditable.
     This framing carries three commitments worth stating up front. First, the framework is
layered and modest: dependency grammar gives a lightweight description of observable structure,
and CCG gives a reconstructive layer that supports compositional interpretation. We do not
claim that any one layer suffices, nor that the LLM “contains” any of them. Second, the
framework is conservative: nothing in it requires modifying the LLM, retraining it, or accessing
its internals. The lifting operates on observable outputs. Third, the framework is coherent under
alternative derivations: a property we will return to in section 2.2, because it is what makes the
lifting well-defined in the presence of CCG’s well-known proliferation of semantically equivalent
surface analyses.
     Although the paper enters through a debate about natural-language grammar, the framework
it proposes does not stay there. Once the lifting is in place, two things follow. The operation
it performs — assigning a typed compositional structure to an incrementally produced expres-
sion — is, through the Curry–Howard correspondence, the same operation as type-checking in
programming languages; the framework therefore extends to the formal languages an LLM also
produces, with the type system varying and the architecture held fixed. And the lifted structure,
once available, supports checking at two levels: a compositional level, internal to the structure,
and a content level that refers the structure outward to an external source of knowledge. These
two developments — the cross-domain reach and the two layers of checking — are the substance
of the paper’s middle sections, and together they de-anchor the account from the cognitive
assumptions that the dependency-grammar reply inherits. We take them up after first setting
out the framework in its natural-language form.
     The remainder of the paper is organized as follows. Section 2 reviews the relevant background
on dependency grammar, CCG, CCG-based semantic parsing, and neurosymbolic AI. Section 3
presents the two-layer lifting framework in its natural-language form. Section 4 sets out the


                                                2
framework’s foundational commitments: the architectural rather than cognitive character of the
stance, the distinction between compositional and content checking, and the role of external
knowledge sources. Section 5 develops the cross-domain extension to formal languages, with
the Curry–Howard correspondence as its warrant and smart-contract code as its principal
worked case. Section 6 sketches a tighter, synchronous LLM–CCG coupling as one direction
the framework opens. Section 7 discusses what the framework claims and does not claim, its
relation to existing work, and its limitations, and section 8 concludes.


2        Background
2.1        Dependency grammar as a descriptive layer for LLM behavior
Dependency grammar represents syntactic organization through asymmetric head–dependent
relations between lexical items, without an intervening layer of phrasal nodes. In its modern
form it is associated with Tesnière and with subsequent work in computational and cognitive
linguistics, and it has become the dominant representational scheme in cross-linguistic corpus
annotation through Universal Dependencies (de Marneffe et al., 2021). The cognitive arm of
this tradition, developed by Gibson and collaborators, emphasizes that dependencies impose a
memory cost that scales with their length, yielding the empirical principle of dependency locality:
across languages and across constructions, word orders that minimize dependency length are
preferred (Gibson, 1998; Futrell et al., 2020).
    This framework has proved attractive as a descriptive lens on LLM behavior. The left-to-right
realization of dependencies aligns naturally with autoregressive generation; many local syntactic
regularities exhibited by LLMs can be characterized as the construction of head–dependent links
one word at a time; and dependency-locality effects appear to be reproduced in the surprisal
profiles of language models. We take this body of work as a well-motivated first-order account of
what LLMs visibly do. We do not contest it. We will argue, however, that it is not the deepest
account available because it captures relations already realized in surface text without explicit
machinery for the predictive completion that drives generation.

2.2        Combinatory Categorial Grammar
Combinatory Categorial Grammar (Steedman, 2000, 2011) occupies a distinctive position among
lexicalized grammatical formalisms. Its core intuition is that syntactic categories are semantic
types: every lexical item carries both a syntactic category and an associated lambda term, and
a small set of combinatory rules — forward and backward application, forward and backward
composition, and type-raising — determines both how categories combine and how meanings
combine. Syntactic derivation and semantic composition proceed in lockstep. The classical
warrant for this lockstep is Montague’s algebraic conception of grammar, on which meaning
assignment is a homomorphism from a syntactic algebra to a semantic algebra (Montague, 1970a);
CCG can be seen as realizing that homomorphism in an incremental, surface-compositional
form.
    For present purposes, the crucial feature of CCG is its treatment of partial expressions.
A sequence such as “John loves” is not a fragment without grammatical status; it has the
category S/N P (a sentence missing a noun phrase to its right) together with a partial lambda
term λx. love(john, x) awaiting an argument. This is not a footnote to the formalism: it is
the formalism’s most distinctive commitment. Type-raising and composition were harnessed
by Steedman and colleagues precisely to give a principled account of incremental, left-to-right
interpretation, in which every prefix of a sentence carries a well-defined type and a well-defined
partial meaning (Ades and Steedman, 1982; Steedman, 2000).1 In this respect CCG is unusually
    1
        Type-raising itself has a dual ancestry worth recording. As a syntactic rule it is derivable as a theorem of



                                                           3
well aligned with the operational character of autoregressive language models, whose entire
computation is predictive: at every position they implicitly carry a representation of how the
prefix-so-far might be completed.
     One feature of the formalism is worth highlighting, as it recurs. The combinatory rules of
CCG admit multiple derivation orders for the same string: a sentence such as “John loves Mary”
can be derived either canonically, by first combining the verb with its object and then with its
subject, or non-canonically, by type-raising the subject and composing it with the verb before
applying to the object. The resulting surface derivations are distinct, but the lambda terms they
produce coincide: composition is associative, and the two derivations yield equivalent terms in the
underlying combinatory logic. This property, sometimes called derivational equivalence modulo
composition, was studied in detail in early work on efficient parsing of CCG, where it underwrites
the design of chart-based parsers that can deliver all semantically distinct analyses without
enumerating spurious ones (Pareschi and Steedman, 1987). The same line has been pursued more
recently in the design of fully incremental CCG parsers using tree-rotation operations (Stanojević
and Steedman, 2019, 2020), which maintain a fully connected, semantically interpretable structure
at every word and which, in current implementations, use a neural supertagger as a front end.
The supertagger’s role deserves accurate statement, because it is easy to understate: beyond
disambiguating among the known categories of seen words, modern supertaggers reliably predict
categories for unseen words from context, and the corresponding semantic category can then be
supplied by rule. This generalization to unseen vocabulary is a powerful effect — demonstrated
when wide-coverage CCG parsing was ported to biomedical text (Rimell and Clark, 2009) — and
it is a substantial part of what makes current CCG parsers usable for practical semantic tasks,
such as the construction of entailment graphs, on input far from their training distribution. We
note these properties here because they are the formal facts that make a CCG lifting of an LLM
prefix well defined: alternative incremental derivations of the same prefix converge on the same
typed semantic object, so the lifting does not inherit the prefix’s derivational arbitrariness; and
existing incremental parsers demonstrate that the symbolic substrate required to support such a
lifting is implementable in practice.

2.3    CCG-based semantic parsing
CCG has served as the substrate for a substantial body of work on mapping natural language
to logical form. Bos and collaborators developed the Boxer system, which combines a wide-
coverage CCG parser with semantics in the style of Discourse Representation Theory (Bos,
2008). Zettlemoyer and Collins introduced statistical CCG-based semantic parsers learned
from logical-form annotations, thereby opening a long line of subsequent work on data-driven
semantic parsing (Zettlemoyer and Collins, 2005). More recent CCG parsers, such as EasyCCG
and depCCG, provide fast and accurate wide-coverage analyses that are suitable as front-ends
to logical interpretation (Lewis and Steedman, 2014; Yoshikawa et al., 2017). The system
most directly relevant to our pipeline is ccg2lambda, which composes lambda terms over CCG
derivations using a template-based mapping from categories to semantic combinators, producing
higher-order logical forms suitable for inference (Martínez-Gómez et al., 2016; Mineshima et al.,
2015).
    These systems share a presupposition: they operate on curated sentences as input, and their
output is a logical form, typically used for natural-language inference, textual entailment, or
knowledge-base population. We adopt their machinery but reposition it. The input we care
about is LLM-generated text, and the question is what is gained by treating the output of such a
parser not as a final product but as a typed compositional representation of a generator’s output
the Lambek calculus (Lambek, 1958); as a semantic operation it entered the field with Montague’s lifting of
individuals to generalized quantifiers, which renders proper names and quantified noun phrases combinatorially
uniform (Montague, 1973). CCG’s distinctive contribution was to put the operation, together with composition,
in the service of incremental derivation — the point at which the logical and the semantic lineages converge.


                                                      4
— a representation aligned, in its incremental structure, with the way the text was produced in
the first place.
    A parallel tradition in categorial semantics has pursued a quite different downstream object.
Beginning with the distributional compositional categorical (DisCoCat) framework, and con-
tinuing through related work on the Lambek and Lambek–Grishin calculi, this line uses the
categorial-grammar derivation as a recipe for composing distributional vector representations
of word meaning into representations of phrase and sentence meaning, with grammatical types
determining the tensor structure of the composition (Wijnholds et al., 2020). The contrast is
clarifying. DisCoCat-style approaches use the categorial skeleton to combine learned distribu-
tional representations and remain in vector space; the framework proposed here uses the same
skeleton to lift LLM-generated text into symbolic lambda terms and exit vector space at the
parser’s output. Both routes exploit the same compositional logic, but to opposite ends. A
long-standing concern for the vector-space route is the combinatorial blow-up of higher-order
tensors required to type-match elements such as relative pronouns or quantifiers; this difficulty
does not arise on the symbolic route taken here, which is one of its attractions in the present
setting.

2.4    CCG, neural language models, and incremental processing
The combination of CCG and large language models has recently been pursued in cognitive
neuroscience, where the incremental parser of Stanojević and Steedman (2019) has been combined
with Transformer-based next-word predictability estimates to model neural signals during human
sentence comprehension (Stanojević et al., 2023). The aim of that work is different from ours —
to evaluate which grammatical formalism better predicts brain responses to naturalistic speech
— but it is a useful demonstration that incremental CCG parsers can be productively coupled
with language-model machinery, and that the resulting structure-building measures contain
information not captured by the language model alone. We see the present paper as taking
a complementary direction: rather than using CCG-derived measures alongside an LLM to
model an external phenomenon, we use a CCG parser as a symbolic lifting layer applied to the
LLM’s own outputs, with the aim of producing typed compositional representations of generated
content.

2.5    Neurosymbolic AI and representational lifting
Neurosymbolic AI is often presented as a broad family of approaches that integrate the flexibility
of neural systems with the interpretability and inferential control of symbolic models. In practice,
such integration can occur at very different levels of intimacy. Some approaches hybridize model
internals, embedding symbolic constraints into training objectives or into the forward pass;
others maintain a strict separation of layers, with a neural component producing material that a
symbolic component then processes. The framework proposed here belongs to the second family.
We do not modify the LLM. We treat it as a probabilistic generator whose outputs admit a
grammatically informed symbolic reconstruction. In this sense, the CCG layer is best understood
as a lifting mechanism, as familiar in program analysis: a mapping from a less-structured
representation to a more-structured one, preserving the information relevant to subsequent
symbolic operations.


3     A Two-Layer Lifting Framework
We propose interpreting LLM outputs using two cooperating layers of analysis, applied post hoc
to generated text.




                                                 5
  1. Neural generation. An LLM produces a token sequence w1:n probabilistically, conditioned
     on a prompt and on its learned distribution. We make no commitment about what occurs
     inside the model; we observe only its outputs.

  2. Compositional CCG layer. A CCG semantic parser assigns lexical categories and
     combinators to the generated text, yielding a derivation and an associated lambda term.
     This layer answers two questions that surface text does not: how does meaning compose,
     and what is the type of what has been combined?

3.1     Example: Incremental Lifting in Lockstep with Generation
To make the convergence between autoregressive generation and CCG’s predictive dynamics
concrete, consider an LLM emitting the tokens John, loves, Mary one at a time. The example
is small by design: John loves Mary is the canonical CCG derivation that every reader knows,
which lets attention fall on what is novel here — the temporal alignment between two systems
running in lockstep.
    At each generation step, two things happen in parallel. The LLM emits a token and updates
its conditioning prefix; its next-token distribution then favors continuations compatible with
that prefix. Independently, the CCG layer, taking the same prefix as input, resolves it to a typed
category with a partial lambda term — an object that makes explicit what kind of completion
the prefix grammatically requires. The two systems are not communicating, but their forward
expectations agree.2

       Step   LLM emits        LLM next-token expectation                        CCG state for prefix

       t=1    John             a verbal continuation is highly likely            N P , john
       t=2    loves            a noun-phrase continuation is highly likely       S/N P , λy. love(john, y)
       t=3    Mary             sentence is complete; punctuation expected        S, love(john, mary)

    The crucial step is t=2. Once loves has been emitted, the LLM is conditioning on the prefix
John loves and assigning high probability to noun-phrase continuations. At the same moment,
the CCG layer has resolved the prefix to the type S/N P with the partial term λy. love(john, y)
— a category that, by definition, denotes a sentence missing an N P on the right. The LLM’s
distributional expectation and the CCG’s typed expectation agree about what the prefix requires
next, but for entirely different reasons: the LLM has learned the regularity statistically, while
the CCG layer has derived it from lexical types and combinatory rules.
    The CCG side of this alignment is built by type-raising (>T) and forward composition (>B),
which together support a strictly left-to-right derivation that mirrors the order of emission. The
static derivation is:
   2
    A granularity caveat applies throughout. LLMs condition on subword tokens, while the CCG layer assigns
categories to words. In the example each word is a single token, so the two systems align step by step; in general
the alignment holds at word boundaries, with the lifting updating once per completed word rather than once per
token. The distinction is immaterial for post hoc lifting, but it becomes operational in the synchronous regime of
section 6, which requires a buffering layer between token-level decoding and word-level typed state.




                                                        6
                                  John            loves           Mary
                                  NP           (S\N P )/N P       NP
                                  john        λyλx. love(x, y)    mary
                                         >T

                               S/(S\N P )
                               λp. p(john)
                                                             >B

                                           S/N P
                                      λy. love(john, y)
                                                                         >

                                                  S
                                          love(john, mary)

     Two observations follow. First, by the derivational-equivalence property recalled in section 2.2,
this left-to-right derivation yields the same final lambda term as any other CCG derivation of
the same sentence, including the canonical bottom-up application-only derivation. The post-hoc
lifting is well-defined regardless of which derivation order the parser internally follows. Second
— and this is the point that the parallel table is meant to bring out — the prefix-by-prefix
structure of the left-to-right derivation is not merely available in CCG; it is aligned with the
temporal order in which the LLM produced the text. The lifting is not only consistent with
generation; it is operationally aligned with it, recovering at each prefix exactly the typed object
whose unsaturated argument matches what the LLM’s distribution expects to come next.
     A dependency analysis can be inserted as a descriptive intermediate to identify the local
head–dependent organization of the generated string. We treat it here as informative scaffolding
rather than as a separate computational layer of the pipeline; the substantive lifting is performed
by the CCG analysis.
     The architecture is intentionally modest in its ontological commitments. It does not claim that
LLMs internally store symbolic grammatical rules, nor that the agreement between distributional
and typed expectations exhibited in the table above reflects a shared mechanism — only that
the two expectations coincide at each prefix, for reasons that the formal alignment between
CCG and prefix-driven processing explains. It does not require that every fluent output admit
an unproblematic compositional reconstruction; sentences may be ambiguous, underspecified,
or pragmatically dependent, and the CCG layer will fail or yield multiple analyses in such
cases just as it does for human-authored text. What it does claim is that, for an interesting
class of outputs — in particular, declarative and argumentatively organized statements — the
lifting yields typed compositional representations that are stable, transparent, and available for
downstream symbolic processing.
     Two properties of the resulting representation deserve emphasis. First, the lifting is coherent:
by the derivational-equivalence property just recalled, the lambda term assigned to a sentence
does not depend on which of the (potentially many) CCG derivations the parser follows. Second,
the lifting is auditable: every component of the resulting term traces back either to a lexical
entry or to a CCG combinatory step, with no opaque inference between the surface string and
its compositional reading.
     A distinction should be drawn, however, between the ambiguity the coherence property
disposes of and the ambiguity it does not. Derivational equivalence guarantees that spurious
ambiguity — alternative derivation orders of the same analysis — leaves the lifting well-defined.
Genuine ambiguity — lexical category choice, attachment, quantifier scope — is another matter:
distinct analyses yield genuinely distinct lambda terms, and the lifting of an ambiguous sentence
is a set of typed candidates rather than a single term. This is not a defect of the formalism (the

                                                  7
sentence is ambiguous), but it obliges the architecture to state a policy, particularly for the
checking layers developed in section 4: content checks should fire only on predications that are
stable across the parser’s n-best analyses, or on the supertagger-disambiguated analysis weighted
by its confidence, with hard interventions — in the synchronous regime of section 6 — reserved
for flags that survive this discipline. We record the policy here because it is what prevents
a mid-sentence misattachment from producing a false flag with downstream consequences for
generation.

3.2   Why LLM-generated text, and not just any text
A natural question is whether anything in the framework above is specific to LLM-generated
text, or whether it is simply semantic parsing applied to a particular input distribution. The
machinery is indeed the same as that used for human-authored text. What is different is the
failure mode the input distribution exhibits, and what an auditable compositional lifting offers
in response to it.
    LLM-generated text exhibits a characteristic pathology: the confident production of content
that is not entailed by anything the system has access to, including its own prior context. Human
text is not free of confident unsupported assertion, but the failure differs in distribution and
in detectability: in LLM output it is systematic rather than exceptional, arises across every
register, and arrives unmarked by the hedges, sourcing behaviors, and stylistic tells that often
accompany it in human prose. This pathology — variously labelled hallucination, confabulation,
or false-positive generation — is the principal obstacle to the use of LLM output in settings
where the cost of an unverified claim is high. Purely distributional methods for detecting it
have so far made limited progress, in part because the relevant defect is not an aberrant surface
feature but the absence of any verifiable compositional support for what is being said. The
output is locally well-formed; it is in its global semantic dependencies that it fails to cohere.
    This is the setting in which an auditable compositional lifting earns its keep. A typed
lambda term derived from generated text exposes precisely the dependencies that hallucination
obscures: which entities are bound, which predicates are applied to them, and which propositional
commitments follow. Successive lifted representations, taken across a passage, can in principle
be checked for compositional coherence, and — as we develop in section 4 — the same lifted
structure is what makes a further check against external knowledge sources possible at all. We
do not develop a hallucination-detection method here; we note only that lifting LLM output into
typed compositional form is one of the few moves that opens such a method to construction, and
that the case for it is significantly stronger in the LLM-as-input setting than in the human-text
setting where compositional parsing was originally developed.


4     Foundations
The framework, as developed so far, takes natural language as input and CCG as a typed
compositional standard. But nothing prevents us from going further and fully embracing the
generative capabilities of LLMs. The cross-domain extension we develop in the next section —
including programming languages, description logics, query languages, and even the languages
of formal mathematics — raises the question of which theory of language is at play. The
dependency-grammar perspective we used as a starting point in section 1 is located within
cognitive linguistics and, while elegant and compelling, is anchored in human processing: it
is imbued with the assumption that dependency-locality effects exist because human memory
imposes costs on long-range dependencies, and that the empirical regularities follow from this
cognitive constraint. The framework we develop here, however, will apply equally to programming
languages — as in the Solidity case exemplified below — and to description logics such as OWL:
in both cases, artefacts whose “processing” has nothing to do with human memory. Paradoxical


                                               8
as it may seem at first glance, leveraging the methodological approach proposed thus far to its
full capabilities implies a lightening, rather than a burdening, of the foundational assumptions
on which it rests.

4.1    An architectural stance, not a cognitive one
The framework’s central commitment is to a specific architectural pattern: a probabilistic
prefix-driven generator whose output is checked, prefix by prefix, by a typed compositional
analyzer.3 The privileged producer in this pattern is the large language model. The framework
exists because LLMs generate text token by token, conditioned on the prefix produced so
far, and because this mode of generation is both powerful and fallible in characteristic ways.
Compositional incoherence, content drift, and the particular kind of confident-sounding error we
call hallucination are all symptoms of probabilistic prefix-driven production. The framework’s
claim is that CCG-style typed lifting is architecturally well suited to checking the output of
such a producer, because it operates at the same granularity — the prefix — and in the same
direction as the production.
    The cross-domain reach of the framework, developed in section 5, is not about parallel
producers but about parallel output languages. The same LLM can produce English, Solidity,
OWL, or SQL; in each case it produces prefix by prefix; in each case its output is subject to the
same kind of probabilistic compositional failure. What differs across these cases is the type system
against which the output is to be checked, and the body of external knowledge that informs the
content layer of the check. The producer is held constant; the output language varies. This is the
genuinely interesting locus of the framework’s cross-domain claim, and it is sharper than a claim
about parallel producers would be. A deterministic Solidity compiler does not need this kind of
checking architecture, because its output is by construction type-correct; an LLM producing
Solidity does need it, because its output is type-correct only probabilistically. The framework is
about LLMs as producers across output domains, not about any typed compositional producer
whatsoever.
    This re-anchoring also clarifies the relationship to the cognitive-linguistic perspective that
opened the paper. The Gibsonian story is an account of human prefix-driven production, and
it has been our entry point precisely because human language production exhibits the same
prefix-by-prefix character that LLMs exhibit by other means. The framework here generalizes
not by abstracting away from the LLM but by holding the LLM as the producer and varying the
output language. Gibson’s account survives as a complementary cognitive-linguistic description
of one specific producer — the human speaker — whose generative profile is structurally similar
to the LLM’s. The framework does not depend on this similarity being more than structural,
and it does not depend on any further theory of human cognition.4 What it does depend on is
the prefix-driven character of the producer.
    The stance has a deliberately cooling consequence for a debate that currently runs hot. Much
discussion treats LLM linguistic fluency as a proxy battlefield for the question of mind — either
as evidence that these systems understand, or as an occasion to insist that, lacking minds, they
cannot genuinely be doing language at all. The framework declines both inferences, and in
   3
      We use prefix-driven rather than left-to-right as the framework’s primary technical vocabulary, because the
architectural commitment is to the conditioning relation by which each successive output is determined by the
prefix so far, not to any particular writing direction. Left-to-right is the writing-system-specific instance for
English, Solidity, and the other languages we predominantly engage with; right-to-left, vertical, and non-sequential
writing systems realize the same prefix-driven structure differently. The framework is indifferent to the realization
and depends only on the structure.
    4
      This methodological posture has a recognizable precedent in Dennett’s intentional stance (Dennett, 1987), on
which a system may be characterized by the stance that is analytically useful toward it — there, treating it as
having beliefs and desires for predictive purposes — without commitment to claims about its intrinsic nature.
The stance we adopt here is architectural rather than intentional, but the licensing move is the same: a producer
is characterized by its generative profile, not by claims about whether it has a mind.



                                                         9
doing so recovers two older postures at once. It recovers Montague’s anti-psychologism — the
insistence that the theory of language, natural or formal, is a branch of mathematics rather
than of psychology (Montague, 1970a) — and extends it from the theory of meaning to the
characterization of producers: what the framework requires of a producer, human or artificial,
is a generative profile, not a mind. And it echoes Turing’s deflationary gesture of replacing a
metaphysical question he judged “too meaningless to deserve discussion” with an operational
one (Turing, 1950) — while going a step further in one respect: where Turing retained linguistic
behavior as the criterial proxy for intelligence, the present account removes language production
from that battlefield altogether. On this view, fluent production neither requires a mind nor
evidences one; it requires a prefix-driven generative profile, which humans and LLMs realize by
different means.
    This last point deserves to be stated positively rather than left as a silent assumption. The
framework’s architectural choice is not universal across all conceivable producers. A producer
that emits language in a non-sequential mode — as a complete graph, as a one-shot semantic
structure, as a globally optimized whole — would not be an instance of the pattern, and
the framework would not apply to its output in the form developed here. The framework is
bounded to producers whose generative profile is prefix-driven, and within that bound, it makes
a precise architectural claim. Current LLMs fit the bound; future systems that depart from
prefix-driven generation would require a different checking architecture. The framework’s reach is
therefore historically situated rather than metaphysically grounded: it is a claim about a specific
architectural fit between a class of producers we presently have and a class of compositional
analyzers that match their generative profile.
    Because the architectural stance disclaims commitments about model internals, it is worth
noting that recent interpretability evidence supports the abstention rather than merely tolerating
it. Gurnee et al. (2026) present causal evidence that LLMs maintain a small, privileged set of
internal representations — a “global workspace” of word-linked, verbalizable patterns — that
mediates deliberate multi-step reasoning: intermediate concepts appearing in neither prompt
nor output can be identified in this space and swapped, with the swap propagating coherently
to the several downstream computations that read from the same representation. Two aspects
of these findings bear on the present framework, in opposite directions. On one side, ablating
the workspace leaves fluent generation and shallow classification largely intact while collapsing
multi-step reasoning — a mechanistic dissociation between surface fluency and compositional
coherence that is precisely the premise of section 3.2: the characteristic pathology of confident
generation is not an aberrant surface feature but a failure at the level of semantic dependencies
that fluency alone does not carry. On the other side, the representations in question are
atomic and untyped — word-linked patterns without categories, without lambda terms, without
combinatory structure — so nothing in the findings suggests that the model internally realizes
the typed composition our lifting recovers. We draw the moral accordingly: on current evidence,
the internal workspace holds word-like atoms, and the compositional algebra over those atoms
is exactly what an external typed lifting supplies. The evidence thus locates the framework’s
contribution rather than licensing a stronger claim, and it gives empirical texture to a division
of labor that the architectural stance had adopted on principle.

4.2   Production and knowledge of appropriate use
The architectural pattern has two components. There is the production of expressions, performed
by the LLM in the role established above, and there is knowledge of appropriate use against which
the produced expressions can be checked. The production component is held constant across
our cases of interest: it is the LLM, generating prefix by prefix, fallibly, and across whichever
output language it has been prompted to produce. What varies is the body of knowledge against
which the output is checked. When the LLM produces natural language, the relevant knowledge
of appropriate use comprises grammatical, semantic, and pragmatic constraints, together with

                                                10
whatever world-knowledge is needed to evaluate referential content. When it produces a program
in a typed language, the relevant knowledge comprises the language’s type system and execution
semantics, together with the body of practical and security knowledge that experts in that
language maintain. When it produces an expression in a description logic, the relevant knowledge
comprises the ontology’s formal axioms together with the external content — lexical, taxonomic,
factual — that fixes what the concepts in the ontology actually denote.
    This bipartite structure is not a coincidence. Any language whose expressions are meant to
bear a determinate relationship to a domain — whether the domain is the world, the state of a
blockchain, or the structure of a knowledge graph — requires both the production of expressions
and the standard against which their appropriateness is judged. The novelty of the present
framework is not the recognition of this bipartite structure, which is ancient, but the specific
computational realization it proposes: production is a probabilistic neural process operating
prefix by prefix, and knowledge of appropriate use is implemented by a typed compositional
analyzer running on the produced output — post hoc in the conservative version, in parallel
with generation in the synchronous variant of section 6.

4.3   Two layers of checking: compositional and content
Knowledge of appropriate use, in this framework, has two layers, and being clear about the
distinction between them is essential to avoiding overclaim. The typed compositional lifting
catches compositional failures: cases where the parts of an expression do not combine into a
coherent whole, where required arguments are missing, where the types of subexpressions do not
match the types their context demands. This is the kind of checking that proceeds entirely from
the structure of the expression and the formal type system it is judged against. The Solidity
example we develop in the next section illustrates this layer: a function that omits a required
require statement produces a lifted type whose effect component is strictly weaker than the
contract demands, and the discrepancy is visible at the level of type-comparison alone.
    The lifting does not, however, catch content failures: cases where an expression is compo-
sitionally well-formed but factually wrong about the domain. The sentence “The Aztec god
Zeus loved Europa” is a case in point: a CCG derivation proceeds without difficulty, and the
resulting lambda term is well-typed, yet the sentence is wrong, and wrong in a way that a
structurally identical lifting of “The Greek god Zeus loved Europa” is not. The wrongness lives
in the lexicon — in the fact that Zeus belongs to the Greek pantheon, not the Aztec one —
which is to say, in an external knowledge source that the typed lifting alone cannot access. A
CCG parser equipped only with syntactic categories and types of standard generality cannot
make this distinction: current wide-coverage CCG parsers are limited in their access to lexical
semantics, and supertaggers trained on category disambiguation do not by themselves carry the
kind of lexical-semantic content that would resolve cases of this type (M. Steedman, personal
communication, May 2026). We work this example through in detail at the end of the subsection.
    The same distinction appears in formal languages. A Solidity function — Solidity being the
principal language for the programs, known as smart contracts, that run on blockchains such as
Ethereum — may type-check cleanly while exhibiting a reentrancy pattern: it makes an external
call before updating its own internal state, so that the called party can call back into the original
function and act on state that has not yet been updated. This is a famous failure mode, and the
one behind the 2016 collapse of “The DAO,” an Ethereum investment fund whose contract was
drained of roughly a third of its holdings through exactly this mechanism. Crucially, reentrancy
is not visible at the level of types alone: the function compiles, the values flow through the type
system without contradiction, and the lifted lambda term is well-formed. The failure is about
the ordering of effects, against a body of security knowledge about Solidity that is external
to its type system. Similarly, an OWL class expression asserting that cows are carnivores is
syntactically well-formed and may pass description-logic consistency checking depending on the
ontology in scope, but is wrong against any plausible biological ontology — against external

                                                 11
knowledge of what cows actually are.
     In each case, the typed compositional lifting does not directly catch the failure. What it
does is more modest and more interesting: it produces a structured object — a typed lambda
term, a categorial derivation, an explicit representation of compositional dependencies — against
which a content check, performed against an external knowledge source, becomes operationally
available. The lifting does not perform the check; it produces the substrate on which the check
can be formulated.
     We now work through the Zeus example, both to see the two layers operating together and to
see precisely where the CCG layer earns its place. The two sentences “The Aztec god Zeus loved
Europa” and “The Greek god Zeus loved Europa” differ in a single modifier. The compositional
lifting proceeds identically for both, prefix by prefix. We show the incremental categories and
partial logical forms; the combinatory steps are as in section 3.1 and are elided for compactness.
Two lexical entries deserve explicit statement. The modifier Aztec carries the standard adnominal
category N/N , with term λP λx. aztec(x) ∧ P (x); its forward composition with the determiner’s
NP/N yields the NP/N prefix category of the second row. And the fourth row treats the bare
proper name as an identificational nominal modifier — an entry of category NP\NP contributing
the conjunct x = zeus — which selects the restrictive reading of the construction; an appositive
reading would require a different entry. Nothing downstream depends on either choice, but both
should be visible.

                       prefix      category    partial logical form

                          The      NP/N        λP. ιx. P (x)
                   The Aztec       NP/N        λP. ιx. aztec(x) ∧ P (x)
               The Aztec god       NP          ιx. aztec(x) ∧ god(x)
          The Aztec god Zeus       NP          ιx. aztec(x) ∧ god(x) ∧ x = zeus

                     . . . loved   (S\NP)/NP   λyλx. love(x, y)
             . . . loved Europa    S\NP        λx. love(x, europa)
                   (complete)      S           love(ιx.[aztec(x) ∧ god(x) ∧ x=zeus], europa)

    The type-check succeeds for both sentences: each is compositionally well-formed, and the
only difference between the two derivations is the substitution of greek for aztec in one conjunct.
Compositional checking cannot distinguish them; that is the point. The content check operates
on the structure the lifting has exposed. At the fourth row — the prefix The Aztec god Zeus,
before the verb has been read — the partial logical form already contains the conjunction
aztec(zeus) ∧ god(zeus). This conjunction is a queryable proposition. Mapping it to a query
against a lexical ontology — itself a step a full implementation must specify, not one the lifting
                                                                      ?
performs automatically — yields the lookup pantheon(zeus) = aztec, against which the
ontology returns pantheon(zeus) = greek. The asserted modifier and the retrieved fact are
inconsistent, and the content layer raises a flag. For the second sentence, the same lookup returns
a match and the prefix is cleared. The flag is raised by the ontology, not by the type-checker:
the lifting produced the queryable atom; the external source supplied the fact; the inconsistency
is the conjunction of the two.
    Two things in this example are worth drawing out. First, the flag is available at the fourth
prefix — the moment Zeus is combined with The Aztec god — not at the end of the sentence.
It is the incremental, type-driven character of CCG that makes this early flagging possible:
because every prefix carries a typed, semantically interpreted category, the predication aztec(zeus)
becomes available for content-checking as soon as it is composed, before the predicate and object
are even read. A non-incremental parser would lift the completed sentence and query afterwards;
CCG lets the query fire mid-generation, which in the synchronous regime of section 6 is the
difference between detecting an error and preventing its completion. The content check requires

                                                 12
an external source, but the timing of the check — its availability at the earliest structurally
meaningful point — is a contribution of the CCG layer that no mere superposition of a parser
and a knowledge base would deliver.
    Second, and more speculatively, the example invites a shift in how we regard the types
themselves. In standard CCG a category such as NP or N/N is a combinatory instruction:
it determines how an expression composes with its neighbours and what lambda term results.
Here the type of a composed predication does something further. The compositional structure
isolates a predication — aztec(zeus) — and the type of that predication determines what kind
of external source could adjudicate it: a one-place property over a named entity is the kind of
thing a lexical ontology can be queried about. In this sense the type functions not only as a
combinatory instruction but as an interface to content-level checking: it specifies not just how
the expression combines, but what external knowledge bears on its correctness and how that
knowledge is to be addressed. This is the natural point of unification between the two extensions
this section has developed — the move beyond natural language and the plugging-in of external
sources — since what travels across both is the type. The reframing is not without formal kin:
in the theory of higher-order contracts in programming languages (Findler and Felleisen, 2002),
behavioral specifications attach to typed interfaces and blame assignment identifies which party
violated which obligation — exactly the discipline an architecture of checks against external
sources will need when a check fails and responsibility must be located. We offer this as an
interpretive reframing rather than a formal result: a worked-out semantics of types-as-interfaces,
and its interaction with the combinatory rules, is beyond the present paper, and we note it as a
direction the framework opens rather than one it closes.

4.4   The contract-and-oracle pattern
This substrate-versus-content distinction has a familiar realization in deployed systems, under
two names that are worth bringing into contact with each other.
    In smart-contract design, on-chain verification — the checking that the blockchain network
itself performs as it executes a contract — handles what is intrinsic to the contract: the type-
correctness of values, the well-formedness of state transitions, the consistency of arithmetic.
Anything that requires knowledge external to the chain — the price of an asset, the outcome of
an event in the physical world — is supplied by an oracle: a designated external source whose
output the contract trusts. The contract verifies what it can verify internally; the oracle supplies
what cannot be verified from on-chain state alone. The trustworthiness of any particular oracle
is a meta-question that the contract architecture does not by itself answer, but the architectural
separation is clear and operational.
    In retrieval-augmented generation, the structurally identical pattern appears in natural
language. A system such as Perplexity generates text using a language model and conditions
the generation on documents retrieved from a trusted corpus, with citations exposed to the user.
The retrieval layer plays the same role as the oracle in the smart-contract case: it supplies what
the language model cannot reliably produce from its parametric memory alone, namely accurate
content about the world. RAG systems contain hallucination substantially because they ground
generation in retrieved context, and the practical effectiveness of this pattern is by now well
established in deployed systems.
    The framework we propose can be seen as articulating, at the architectural level, what these
two patterns have in common, and as identifying what a typed compositional lifting adds to both.
In the smart-contract case, on-chain verification operates at the compositional level (typing
and state-transition consistency), and the oracle supplies external content; in the RAG case,
the language model operates at the production level, and the retrieval layer supplies external
content. What is missing in current RAG implementations is the compositional layer: the
retrieved content is fed back into generation as conditioning context, where its influence is
statistical rather than compositional. The framework proposes that a typed compositional lifting

                                                13
of generated text would produce the structured object against which retrieved content could be
checked compositionally rather than distributionally — the lambda term for “The Aztec god
Zeus . . . ” makes the binding aztec(zeus) explicit and queryable, in a way that the surface text
fed back to the model as conditioning does not. The architecture is the same; the lifting is what
would let the check operate at the right level.
    This framing has a final virtue worth flagging. The trustworthiness of any particular
knowledge source — a lexical ontology, a corpus of vetted Solidity patterns, a domain knowledge
base — is a meta-question that the framework recognizes but does not resolve. The framework’s
claim is that, given access to a trustworthy source, the typed lifting produces the substrate
against which content from that source can be checked compositionally and incrementally.
The selection and curation of knowledge sources is itself a substantial undertaking and is left,
appropriately, to subsequent work.

4.5       Incrementality and the earliest possible flagging
A final foundational point concerns when the checking happens. CCG’s incrementality is not
just an elegant theoretical feature aligned with the prefix-driven character of autoregressive
generation; it is operationally significant for the contract-and-oracle architecture we have just
described. Compositional checking can flag a structural problem as soon as the structure
becomes incoherent: the moment a prefix carries a type that cannot be extended to a well-formed
continuation, the lifting fails. Content checking, given access to the relevant knowledge source,
can flag a content problem as soon as the lifted prefix carries enough structure to be queried
against the source.
    Consider the sentence “The Aztec god Zeus . . . ” unfolding token by token. After The, no
content check is yet evaluable. After The Aztec god Zeus, the lifted prefix has the binding
aztec(z) ∧ god(z) ∧ z = zeus, which is queryable against a lexical ontology that records pantheon
membership. At this moment — before the sentence’s predicate has even begun — the system
can flag the inconsistency, and downstream behavior (re-prompting, soft constraint, hard mask
in the synchronous variant) can intervene. The same logic applies in formal languages: a Solidity
function that begins an external call before its state update can be flagged at the moment the
external call appears in the lifted structure, against security knowledge that records the safe
ordering. An OWL class expression that begins to assert subsumption of Cow under Carnivore
can be flagged at the moment the subsumption claim becomes queryable against a generalist
ontology such as WordNet.
    What incrementality buys, in this architecture, is the earliest possible flagging. The lifting
and the knowledge-source query proceed in lockstep with generation, and intervention becomes
available at the first prefix at which the check is evaluable.
    The Zeus example is synthetic, constructed for minimal-pair clarity. It is worth seeing the
same machinery applied to a hallucination produced in the wild by a deployed system.5 Queried
for the biblical verse in which Jacob describes his brother (“Esau my brother is a hairy man,”
Genesis 27:11), a current commercial LLM failed to supply the reference and asserted instead
that the brother of Esau was Elijah — apparently through the lexical association that the
prophet Elijah, an unrelated figure from a different period, is also described as hairy (2 Kings
1:8). The error is instructive precisely because of its etiology: it is a distributional slippage along
a shared surface feature, invisible to any check based on fluency or local plausibility, and the
correct answer (Jacob) is a one-step lookup in any encyclopedic knowledge base. The lifting of
the offending assertion proceeds prefix by prefix, in the left-to-right style of section 3.1:
   5
       We owe the episode to Mark Steedman (personal communication, June 2026), who encountered it directly.




                                                      14
                 prefix                  category     partial logical form
                 The                     N P/N        λP. ιx. P (x)
                 The brother             N P/P Pof    λy. ιx. brother(x, y)
                 The brother of Esau     NP           ιx. brother(x, esau)
                 . . . was               S/N P        λy. ιx. brother(x, esau) = y
                 . . . was Elijah        S            ιx. brother(x, esau) = elijah

    Two query moments arise, and they differ in kind from the Zeus case in a way that exercises
the types-as-interfaces reading of section 4.3. At the third prefix, the lifted object is a definite
description over a two-place relation — an individual-denoting term, not a one-place predication
— and its type determines the query form: not a membership check, as with pantheon(zeus),
                                              ?
but referent resolution, ιx. brother(x, esau) = ?, against which an encyclopedic source returns
jacob. At the final step, the equative composes the description with the asserted identity, and
the conjunction of the lifted term with the retrieved referent — elijah = ιx. brother(x, esau)
against jacob = ιx. brother(x, esau), with jacob ̸= elijah — raises the flag at the moment the
word Elijah is emitted, the earliest structurally meaningful point. As in the Zeus case, the flag
is the joint product of the two layers: the lifting supplies the queryable description and the
identity structure; the external source supplies the fact.
    One obligation that a real deployment of this check incurs should be stated, because the
real-world example brings it into focus. The predication brother(x, esau) must trigger the query
only when it occurs in a veridical position — asserted by the producer — and not when it is
embedded under negation, a question, an attitude report (“the system claimed that the brother
of Esau was Elijah”), or fictional framing, where flagging would be a false positive. This gating is
not an additional burden the framework must import from elsewhere; it is information the lifting
already carries. The position of a predication within the lifted term — inside or outside the scope
of a negation, a question operator, or an intensional verb — is exactly what a compositional
derivation makes explicit, and it is what context-free decomposition of text into atomic claims,
as practiced in atomic-fact verification methods such as FActScore (Min et al., 2023), discards.
A worked treatment of veridicality projection is an implementation obligation we flag rather
than discharge here, but it is an obligation the compositional route is structurally equipped to
meet.
    This is what makes the synchronous-coupling architecture of section 6 attractive even as
a future direction: it converts post-hoc detection into prevention. The conservative post-hoc
framework of this paper already exhibits the same structural advantage at a coarser granularity —
it can flag at sentence boundaries or at semantic-unit boundaries rather than at token boundaries
— but the operational character is continuous between the two, and the incrementality of CCG is
what makes both possible.

4.6    What this section commits us to, and what it does not
We close this section by stating its commitments cleanly. The framework is about probabilistic
prefix-driven generation by LLMs and about the architecturally appropriate checking layer for
such generation. It is not about typed compositional production in general. The producer is held
constant — the LLM in its prefix-driven generative profile — and the output language varies
across natural and formal cases. The architecture has two components: production by the LLM,
and knowledge of appropriate use; the latter has two layers, compositional and content. The
typed lifting catches compositional failures and produces the substrate against which content
checks become possible; content checking itself requires external knowledge sources, whose
trustworthiness is a meta-question the framework does not resolve. The contract-and-oracle
pattern from smart-contract design, and retrieval-augmented generation from natural-language
deployment, are recognizable instances of this architecture in operating systems; the framework
proposes that a typed compositional lifting articulates what these patterns have in common

                                                15
and what compositional structure adds to them. The incrementality of CCG-style derivation
makes this architecture deliverable at the granularity of generation itself, supporting the earliest
possible flagging of both compositional and content failures.
    What we are not committing to: any theory of mind, any claim about LLM internals, any
specific implementation of a knowledge source or its curation, any guarantee that a particular
knowledge source will be trustworthy or complete, and any claim about producers whose
generative profile is not prefix-driven. The commitments are architectural and historically
situated. They license the cross-domain extension we develop next — across the output
languages an LLM can produce — and they constrain the kinds of claims that extension can
support.


5     Beyond Natural Language: Lifting Across Typed Domains
The framework as developed so far treats natural language as the input distribution and CCG
as the typed compositional standard against which generated text is lifted. Nothing in the
operational architecture, however, depends on the input being natural language. What it
depends on is something more abstract: that the language produced by the LLM admits a typed
compositional standard with an incremental left-to-right interpretation, and that the production
process itself proceeds left-to-right. Where both conditions hold, the lifting applies.
    This section argues that the conditions hold for a broader class of languages than the natural
ones — and in particular for the formal languages where LLM-based generation has become
consequential: programming languages, description-logic and query languages, and the broad
family of expressions in formal mathematics. The argument is not that these languages are
linguistically similar to English. It is that the operation of lifting incrementally-produced output
into a typed compositional structure has the same formal character in all of them, by virtue of an
identification whose history is older than either CCG or contemporary LLMs. Before giving that
identification its formal statement, it is worth naming its programmatic ancestor. The thesis that
there is no important theoretical difference between natural languages and the artificial languages
of logicians, and that both can be comprehended within a single mathematically precise theory,
is Montague’s (Montague, 1970b): “English as a formal language” was proposed in earnest, not
as a metaphor, and the extension undertaken in this section is that thesis operationalized for
the setting of probabilistic prefix-driven generation.

5.1   The propositions-as-types correspondence
The identification in question is the propositions-as-types correspondence, also known as the
Curry–Howard isomorphism. Discovered independently by Curry in the 1930s and Howard
in the 1960s, and recently surveyed at length by Wadler (2015), it observes that propositions
in intuitionistic logic correspond exactly to types in the simply-typed lambda calculus, and
that proofs of propositions correspond exactly to programs of the corresponding type. The
connective → in logic is the function-type constructor → in programming; modus ponens is
function application; the construction of a proof is the construction of a program. The same
correspondence has been extended to predicate logic (dependent types), second-order logic
(System F and parametric polymorphism), and linear logic (session types). It is, in Wadler’s
phrase, “a notion with depth, breadth, and mystery.”
    The relevance to categorial grammar is direct, and was established early. Beginning with
van Benthem (1983), derivations in Lambek-style categorial calculi were shown to admit a
Curry–Howard interpretation: a categorial proof of a sentence’s grammaticality is also a lambda-
calculus construction of its meaning, with the syntactic category playing the role of the type.
This interpretation became foundational to the type-logical grammar tradition developed by
Moortgat, Morrill, and others, where the syntax–semantics interface is explicitly framed as the


                                                16
Curry–Howard correspondence at work in natural language (Moortgat, 1997; Morrill, 1994).
CCG itself has been given a logical characterization in the same family: Kubota (2014) shows
that CCG can be understood as a substructural logic in which the directional slashes correspond
to substructural implications and the combinatory rules correspond to particular combinator
types.
    What this means for the present paper is that the central operation of the framework —
assigning a typed category and a partial lambda term to a prefix, and updating both incrementally
as new material arrives — is an instance of an operation that has been studied for sixty years
in mathematical logic and forty years in computer science, where it goes by various names
(type-checking, type inference, proof reconstruction) but always refers to the same family of
procedures. The lifting we have been calling “CCG lifting of LLM output” is, viewed through
the Curry–Howard lens, a particular case of a more general operation: incremental type-checking
of left-to-right generated content against a typed compositional standard.

5.2   Implications for cross-domain extension
Once stated in this form, the framework’s potential scope becomes apparent. The same operation
that lifts “A wise lord must keep faith . . . ” into a typed lambda term lifts a program in any
typed programming language into the typed term of its semantics, lifts a description-logic
expression into a typed term in its ambient logic, and lifts a mathematical expression into a
typed computation. In each case, the input is incrementally produced, prefix by prefix, by an
LLM. In each case, a typed compositional standard exists. In each case, the lifting recovers a
structured object that exposes the compositional dependencies of the generated content and
makes them available for symbolic processing.
    What changes across domains is not the operation but the type system and the lexicon.
The CCG types S, N P , N , and the combinatory rules of forward and backward application,
composition, and type-raising are the natural-language-specific instantiation of the more general
apparatus. For a programming language, the analogous instantiation would be the language’s
own type system — primitive types, function types, parameterized types, and the structural rules
by which expressions in the language compose. For a description logic, it would be the types of
concepts and roles and the algebra of class constructors. The framework’s commitment is not
to any particular type system but to the architectural pattern: incremental production from a
probabilistic generator, checked against an incremental compositional analyzer that produces
typed lifted representations.

5.3   Programming languages
The domain in which this cross-extension has the most immediate force is the generation of source
code in typed programming languages. LLM-based code generation has become ubiquitous in
software development, and the failure modes are well-documented: omitted input validation,
incorrect handling of edge cases, control-flow patterns that compile but do not implement the
intended semantics. Surface plausibility and structural similarity to reference implementations
are routinely high, while functional correctness is substantially lower. The failure is compositional:
each line of generated code is locally plausible, but the global semantic structure does not cohere
with the program’s intended specification.
    A Curry–Howard reading of the lifting framework suggests where the leverage lies. If a
CCG-style typed lifting of generated source code produces a lambda term whose type encodes
the function’s behavioral contract, then verification reduces to type-checking: the generated code
is a valid implementation of its intended semantics if and only if the lifted term inhabits the
expected type. This is the same identification that underlies the Curry–Howard correspondence
and that has been exploited in proof assistants such as Coq and Lean for decades. What is
novel here is not the verification idea but the pipeline: an LLM produces the candidate program,


                                                 17
a categorial-style parser produces the typed lambda term, and a type-checker discharges the
verification obligation.

Solidity as a particularly clean instance. For readers outside the area, a brief orientation
is in order. A blockchain is a replicated, append-only ledger maintained by a decentralized
network of nodes that agree, by a consensus protocol, on its contents. A smart contract is a
program stored on such a ledger and executed by the network: it holds state (for instance,
account balances) and exposes functions that external parties invoke through transactions, each
of which deterministically updates the shared state. Solidity is the dominant language for writing
smart contracts on Ethereum, the most widely used programming-capable blockchain, and on
the many compatible platforms. Two properties make this setting consequential. Contract
code, once deployed, is effectively immutable — it cannot be patched in place — so a latent
defect cannot simply be corrected after the fact; and contracts routinely custody economically
significant assets, so a defect that is exploitable is a defect that loses money. These are the
stakes against which the correctness of generated contract code must be judged.
    Solidity is, for our purposes, a particularly clean case, for reasons that go beyond its
relative novelty. It is less widely studied than C or Java but it embeds two features that
make compositional verification both unusually tractable and unusually consequential. First,
Solidity programs are explicitly transactional: each external function call is an atomic unit of
state change, either fully committed to the ledger or fully reverted, with no intermediate state
observable outside the contract. This atomicity disciplines the compositional structure of the
code in ways that align well with typed compositional analysis: the function boundary is also
the verification boundary. Second, Solidity is event-driven in a strong sense: contracts respond
to incoming transactions by emitting events — typed, logged records of what occurred — that
downstream contracts and off-chain systems consume, and the type structure of those events is
part of the contract’s interface. The dependency between a function’s input validation, its state
mutations, and its emitted events is therefore explicit at the language level, in a way that makes
compositional failures particularly visible to a typed lifting.
    These features combine with high stakes to produce a domain where compositional verification
of LLM-generated code is both technically tractable and economically motivated. Recent
empirical work (Salzano et al., 2026) has shown that current LLMs — including ChatGPT-
4o, Gemini, CodeLlama, and DeepSeek-Coder — produce Solidity smart contracts that are
functionally correct only 20–26% of the time in zero-shot generation, and at best 45% with
retrieval augmentation. The failure modes are precisely those that a typed lifting would expose:
omitted require statements that should have validated input, missing access-control modifiers,
and event emissions that do not correspond to the state changes they claim to report. Each
of these is a compositional failure rather than a local one, and each is the kind of failure that
surface similarity metrics will not catch.
    We do not develop the Solidity lifting in detail here; that is a substantial undertaking,
requiring the design of a CCG-style typed lexicon for the language and the engineering of a
parser able to operate on LLM-generated contract code. We note only that the conceptual
framework supports such a development, that the Curry–Howard correspondence provides its
formal warrant, that Solidity’s transactional and event-driven character makes it a particularly
appropriate first target, and that the empirical case for pursuing it is strong: a method that
materially improves on 20–26% functional correctness in smart-contract generation would be a
substantial contribution to a domain where deployed errors are immutable and economically
consequential.

Example: A typed lifting of a Solidity function
To make the type-checking-as-verification claim concrete, we apply the framework to one of the
functions from the empirical study of Salzano et al. (2026). Consider setMinDepositAmount,

                                               18
a function that updates a contract’s minimum-deposit parameter. The ground-truth version,
drawn from a deployed contract, has three coordinated commitments: it is callable only by
the owner, it validates that the new amount exceeds a minimum unit, and it emits an event
recording the update. The lifted form, as a typed lambda term, captures the joint compositional
structure of these commitments.

 (A) Ground-truth Solidity                          Lifted typed term and its type
                                                                                         
 function setMinDepositAmount (                     λa : uint owner(msg.sender) ∧ a > unit .
   uint _amount                                      set(minDeposit, a), emit(MinDepUpd, a)
 ) external onlyOwner {
   require ( _amount > unit () ,                    of type:
       " amount > UNIT ");                          Πa : uint [ φauth ∧ φval (a) ].
   m i n i m u mDepositAmount = _amount ;                                
   emit MinDepositUpdated ( _amount );               State ⊗ EventUpd
 }

 (B) Zero-shot LLM-generated Solidity               Lifted typed term and its type
                                                                                     
 function setMinDepositAmount (                     λa : uint owner(msg.sender) .
   uint256 newAmount                                set(minDeposit, a)
 ) public onlyOwner {
   minDepositAmount = newAmount ;                   of type:
 }                                                  Πa : uint [ φauth ]. State

Figure 1: A Solidity function from Salzano et al. (2026) and its hypothesized typed lifting,
under both the ground-truth implementation (A) and the zero-shot LLM-generated version (B).
The lifted type of (B) is a strict weakening of the lifted type of (A): the precondition omits
the input-validation conjunct φval , and the effect type collapses from a product to a single
component.

    In (A), the term is a dependent function over a precondition combining authorization (φauth )
and input validation (φval ), returning a product of two effects: a state mutation and an event
emission. The type carries the function’s behavioral contract: it states that, given an authorized
caller and a validated input, the function produces both the expected state change and the
expected event. In (B), the LLM-generated version has neither the validation precondition
nor the event-emission effect. Its lifted type is strictly weaker than the expected contract: the
precondition drops φval , and the effect type collapses from a product to a single component.
    The verification step is the type-comparison itself. The expected type for this function —
derived from the contract’s natural-language specification or from a reference implementation —
is the one shown in (A). The LLM’s output has the type shown in (B). The two are inhabitants
of different types, and the latter does not inhabit the former. The compositional failure that the
surface code obscures, and that similarity metrics fail to detect, is visible at the level of type
structure as a strict weakening of the expected contract.
    This is a sketch. A full development would require a CCG-style typed lexicon for Solidity that
produces such lifted terms compositionally from generated source code, rather than presenting
them by hand. It would also require a precise treatment of the refinement annotations φauth
and φval , which we have left informal here. What the example demonstrates is the conceptual
leverage: once the lifting is in place, the failure mode documented empirically by Salzano et
al. (2026) — LLM-generated contracts that compile and pass similarity checks while omitting
validation and event emissions — becomes a type-mismatch that is detectable without execution
and that points directly to the omitted commitments.



                                               19
Sizing the practical problem. Since the development just called for is the natural sequel to
this paper, it is worth setting out, as premises, an honest assessment of what it involves. Four
observations size the undertaking.
    First, the lexicon design is co-extensive with the design of the target type algebra. The base
types of the Solidity lifting are not the language’s surface types — uint, address, mapping
— whose correctness the compiler already polices deterministically. They are the effect-and-
obligation types the example above employs: State, Event Upd , the refinement conditions φauth and
φval , and the product ⊗ on effects. The substantive work is to give this algebra a combinatory,
incrementally composable presentation — a categorial grammar whose derivations build effect-
and-obligation types in lockstep with the traversal of the source. This is also the precise answer
to the question of why the compiler does not already do the job: the compiler checks the surface
types; the lifting checks the behavioral contract.
    Second, the cold-start problem is more tractable than its natural-language analogue. Wide-
coverage CCG parsing of English exists because CCGbank could be converted from an existing
treebank; no SolidityCCGbank exists, and there is no treebank to convert. But the gold standard
in this domain is compiler-checkable: category assignments can be bootstrapped by rule from
deterministic parses of compilable code, and the public corpus of deployed, audited contracts
supplies ground truth at a scale that natural language, where gold categories require human
annotation, has never enjoyed. A large fraction of the supertagger’s training data can therefore
be synthesized rather than hand-labelled.
    Third, the unseen-vocabulary problem is softened by the program itself. Generated contracts
are dense with user-defined identifiers — function names, state variables, custom events — that
are unseen by construction. The supertagger generalization discussed in section 2.2 already
addresses this in natural language, where the semantic category of an unseen word must be
supplied by rule; in Solidity the situation is more favorable still, because the contract’s own
declarations type its identifiers — the source itself states that a given name denotes an event
with a uint parameter. The producer’s output, in other words, carries its own lexicon-extension
information, a resource natural language never supplies.
    Fourth, and this is the boundary to state candidly: the properties that fall out cleanly
and incrementally are the intra-function ones. Missing validation, missing event emission, the
effect-type weakening of the example above — these are visible at the function boundary, which
Solidity’s transactional atomicity makes coincide with the verification boundary. The properties
the security community cares most about, however, with reentrancy foremost among them, are
non-local: as the DAO case of section 4.3 illustrates, reentrancy is not visible at the external call
in isolation, but only relative to whether a state update has already occurred and whether control
can re-enter. The clean way to see this is that a contract is a discourse, its functions are sentences,
and reentrancy is a coreference problem across sentences: the same discourse-level composition
problem flagged for natural language in section 7 recurs here in formal dress, and the incremental
discourse machinery cited there (Grenander et al., 2022) is the natural candidate for lifting into
this setting. Solidity is, if anything, hospitable to the move: its design carries discourse-like
notions — transactions, emitted events, inter-contract calls — that have no counterpart in
traditional languages and that map naturally onto an explicit discourse model.
    These premises are set out here to size the undertaking, not to discharge it. The development
itself — the lexicon, the supertagger, and the evaluation of the resulting checker against the
empirical baseline of Salzano et al. (2026) — is the subject of work in progress.

5.4    Description-logic and query languages
The argument extends to the broad family of description-logic languages, of which two well-known
instances are SQL and OWL. SQL queries generated by LLMs frequently exhibit the same
failure pattern as code: schemas are misremembered, joins are constructed against absent foreign
keys, aggregations are applied to incorrectly grouped relations. The relational algebra is a fully

                                                  20
specified type system, and a categorial-style lifting could in principle catch such failures at the
level of typed composition rather than at the level of execution against a database. OWL exhibits
parallel failures of class subsumption, role composition, and quantifier scope: a generated class
expression may be syntactically well-formed and superficially plausible while denoting a class
that is unsatisfiable, equivalent to an existing class, or in an unintended subsumption relation
with the surrounding ontology. The description-logic reasoning machinery already exists; what
is missing is a lifting pipeline that converts LLM-generated DL expressions into the typed form
that the reasoner can check.
    Beyond SQL and OWL, the same family includes SPARQL for graph databases, the various
Datalog dialects used in knowledge representation, and a growing class of domain-specific
languages developed for everything from policy specification to bioinformatics. In each case, the
language has an established compositional semantics, an established type-checking apparatus,
and an emerging body of LLM-generated content whose compositional correctness is currently
checked, when checked at all, by execution rather than by typed lifting. The framework proposed
here is in principle applicable to all of these.

5.5   Mathematical expressions and the unifying view
A smaller-scale but structurally clean illustration is arithmetic and, more generally, the language
of formal mathematical expressions. LLMs are well known to produce chains of mathematical
reasoning whose intermediate steps do not actually compose into the claimed result — a failure
that is precisely the kind of compositional incoherence that a typed lifting would expose. We
note this case mainly as a probe rather than as a serious application target: simpler tool-use
methods (calculator APIs, program-aided language models, dedicated solver invocations) are
often more practical for arithmetic specifically, although the deeper case of formal mathematical
reasoning, including proof-trace verification, is precisely where typed-lifting approaches connect
to the proof-assistant tradition mentioned earlier.
    What unifies all of these domains is not their linguistic structure but their compositional
structure. They are all languages in which the meaning of a complex expression is a function of the
meanings of its parts and the way those parts are combined. The Curry–Howard correspondence
gives this structural fact a formal expression: the meaning is the lambda term, the type is the
proposition the term proves, and the lifting operation is the assignment of type and term to
an incrementally produced expression. Where this combination of properties holds — and it
holds across natural language, programming languages (with Solidity as a particularly clean first
target), description-logic and query languages, and the languages of formal mathematics — the
framework applies.
    We do not claim to have demonstrated this. We have argued for the conceptual scope on
the basis of the formal correspondence and have indicated the empirical domain where the
case is strongest. The development of the framework in any specific formal-language domain
is substantial work in its own right, and we leave it to subsequent papers, our own or others’.
The point of this section is to mark the scope: the lifting framework is not specific to natural
language, and the prefix-driven convergence between LLM generation and CCG-style incremental
processing is the linguistic instance of a more general phenomenon whose formal articulation
has been with us since Curry. Stated as a genealogy: Montague supplied the thesis — natural
language as a formal language, interpreted through a typed homomorphism; CCG supplies its
incremental, surface-compositional realization; and the LLM supplies the prefix-driven producer
whose output that realization can discipline.




                                                21
6    Toward Synchronous LLM–CCG Coupling
The framework above is post hoc: it lifts text after generation. A natural and considerably more
ambitious extension is to couple an incremental CCG parser to the LLM during generation,
so that at every decoding step the symbolic layer maintains a typed syntactic–semantic state
aligned with the current token prefix. Let w1:t be the prefix at step t and let the LLM produce
a distribution p(wt+1 | w1:t ) over next tokens. In parallel, an incremental CCG component
maintains a set of derivational states St together with partial semantic terms Λt . For each
candidate token, the parser predicts admissible category insertions and updates these states.
Information flows in both directions: the LLM proposes tokens, and the parser returns signals of
admissibility, syntactic fit, and semantic consistency that may constrain or reweight generation.
In a soft variant, these signals are combined with the LLM’s log-probabilities; in a hard variant,
inadmissible tokens are masked.
     We mention this here as a future direction rather than as a fully worked-out proposal, but
it is no longer purely speculative — and for formal languages, part of the territory is already
occupied. Constrained-decoding systems mask or reweight inadmissible continuations against
a formal grammar during generation: PICARD does so incrementally for SQL (Scholak et al.,
2021), Synchromesh for several target languages via completion engines (Poesia et al., 2022),
and grammar-guided generation frameworks make the hard-masking regime generic and efficient
(Willard and Louf, 2023). Their practical success is direct evidence for the viability of the
architectural pattern. What none of them maintains, however, is a typed semantic state — a
partial lambda term alongside the syntactic admissibility check — and none addresses natural
language, where the grammar is not given by a language definition but must be supplied by
wide-coverage categorial machinery of the kind discussed above. The unoccupied territory is
therefore twofold: the coupling of semantically interpreted symbolic state with generation, and
its extension from formal languages to natural ones. On the CCG side, the incremental parsers of
Stanojević and Steedman (2019, 2020) provide a symbolic substrate that maintains exactly the
kind of typed prefix-level state St , Λt that the coupling requires, and they already use a neural
supertagger as a front end — so the architectural pattern of a neural component proposing
material and a symbolic component validating and updating typed state is one for which working
CCG-side machinery exists. What remains to be designed for the LLM-coupled variant is the
combination rule between symbolic admissibility signals and statistical decoding scores; the
operating regime in which the symbolic layer constrains rather than merely scores generation; and
a treatment of pragmatic and underspecified expressions that neither tradition has fully resolved.
A specific hazard of the hard variant should also be named: incremental parsers commit and
reanalyze, and a mask derived from the parser’s current analysis may prune continuations that a
later reanalysis would have licensed — a parser-induced garden path, in which the checking layer
rather than the generator becomes the source of error. This consideration favors the soft regime,
with reweighting and deferred commitment, as the default operating point for natural language,
reserving hard masking for formal languages whose grammars do not give rise to reanalysis. The
conservative post hoc lifting framework of the previous section remains, we believe, both more
immediately defensible and more immediately useful, and we do not pretend in this draft that
the synchronous version is more than a sketch.


7    Discussion
What the framework claims, and what it does not. The framework is a contribution to
the conceptual architecture of neurosymbolic language processing rather than an empirical claim
about the internal organization of LLMs. Its principal virtue is layered modesty: dependency
grammar gives a lightweight description of observable structure, and CCG gives a reconstructive
layer that supports compositional interpretation. Neither layer makes claims it cannot support.


                                               22
In particular, we do not claim that LLMs internally implement CCG, nor do we claim that every
fluent output admits a straightforward compositional reconstruction. Ambiguity, underspeci-
fication, anaphora that cannot be resolved from local context, and pragmatic dependence all
remain serious challenges, and they remain challenges for the CCG layer in the same way as for
any other compositional formalism. We would add one point of scope, developed in section 4:
although the paper’s entry point is the reply to a debate about natural-language grammar, the
architectural claim is not confined to natural language. It concerns probabilistic prefix-driven
generation as such, and applies wherever an LLM produces output in a language with a typed
compositional standard — natural or formal — against which that output can be checked.

Relation to existing CCG-semantics work. Our contribution is not the use of CCG for
logical-form extraction — that is well established in the line from Bos and Steedman through
Zettlemoyer and Collins to ccg2lambda and its successors. Our contribution is the repositioning
of this machinery in light of the convergence noted in section 1: the same incremental, prefix-
driven dynamic that CCG was designed to describe is the one that autoregressive language
models realize statistically, which makes a CCG lifting of LLM output not merely a technical
option but a structurally well-motivated one. A second point of contact is with atomic-fact
verification methods such as FActScore (Min et al., 2023), which decompose generated text into
independent claims and check each against a source: the lifting proposed here can be read as
a typed, incremental alternative to LLM-based claim decomposition — one that preserves the
entailment context of each predication (section 4.5) rather than discarding it.

Why the convergence matters. If a single observation deserves to be carried away from
this paper, it is the one developed in section 1: the prefix-driven, type-completing dynamic that
autoregressive LLMs realize statistically is the dynamic that CCG was originally designed to
describe. This is not, we believe, accidental. The character of left-to-right processing imposes a
structure on what can be predicted and how predictions can be completed. Incrementality by
itself, it should be said, is not the distinctive claim: left-corner parsers, incremental dependency
parsers, and neural syntactic models all maintain prefix states of one kind or another. What
CCG — alone among major grammatical formalisms — provides is semantically interpreted
incrementality: every prefix is a first-class typed object carrying a partial meaning, with
a principled combinatory algebra governing how that object extends, rather than a parser
configuration awaiting completion. It is this property, not incrementality as such, that the lifting
exploits. The dependency-grammar reply to the “grammarless” critique is correct as far as it
goes; the CCG observation extends it in a direction where what is gained is not merely a richer
descriptive vocabulary but a principled route to typed compositional meaning.

Two layers, and a view of types. A second strand of the paper concerns what the lifting is
for. We have argued that the typed structure it produces supports checking at two levels — a
compositional level internal to the structure, and a content level that refers the structure to an
external knowledge source — and that this division is what allows the framework to make honest
contact with the problem of hallucination without overstating what compositional analysis alone
can do. The same division underwrites a reading of the framework’s central object that we have
offered tentatively: that a type, in this setting, functions not only as a combinatory instruction
but as an interface specifying what external knowledge bears on an expression’s correctness and
how that knowledge is to be addressed. We regard this as an interpretive reframing rather than
a formal result, but it is the point at which the paper’s two extensions — the move beyond
natural language and the plugging-in of external sources — meet, since what travels across both
is the type.




                                                23
Limitations and next steps. Four limitations of the present draft should be flagged explicitly.
First, while we have provided a sentence-level example of incremental lifting, a fully worked
end-to-end implementation taking a multi-paragraph passage of generated text through a CCG
parser pipeline remains a natural next step. Second, the treatment of multi-sentence discourse,
anaphora, and pragmatic context remains open; the lifting as described operates sentence by
sentence, and the question of how to compose successive lifted representations into a coherent
discourse-level object is substantial. Coreference resolution is the most acute instance of this
gap; it is, however, no longer unaddressed territory. Sentence-incremental neural coreference
resolution over an explicit discourse model has been developed by Grenander, Cohen, and
Steedman (Grenander et al., 2022), with a fuller treatment in Grenander (2025), and the
incrementality of that line is precisely the property a prefix-driven lifting requires of its discourse
layer. Composing such a layer with the sentence-level lifting remains substantial work, but it
is work for which incremental machinery now exists. Third, the robustness of available CCG
parsers must be assessed accurately — which means neither overstating nor understating it.
Wide-coverage CCG parsing has historically been trained on CCGbank, the CCG conversion
of the Wall Street Journal portion of the Penn Treebank, which provides roughly a million
words of newswire English, while LLM-generated text ranges over registers, domains, and
degrees of formality well beyond this distribution. The lexical dimension of this gap, however,
is substantially mitigated by the supertagger generalization discussed in section 2.2: modern
supertaggers predict categories for unseen words from context, with the semantic category
supplied by rule, and this is what allowed wide-coverage CCG parsing to be ported successfully
to domains as lexically remote as biomedical text (Rimell and Clark, 2009). The residual
concern is therefore structural and register-level rather than lexical — constructions, discourse
conventions, and degrees of informality unattested in newswire — and it is most pressing in the
synchronous regime of section 6, where parser failures would directly constrain generation rather
than merely producing an unlifted sentence. Fourth, what one does with the resulting lambda
terms — whether they are used for verification, for hallucination detection, for explanation,
for the extraction of decision-relevant rules, or for the construction of higher-level reasoning
objects — is held back for separate treatment. A companion paper, in preparation, details one
such downstream use.


8    Conclusion
We have laid the groundwork for a layered perspective on grammar and meaning in large language
models. Our starting point was dependency grammar, which plausibly explains important aspects
of the observable grammatical organization of LLM outputs, countering the claim that such
systems are entirely grammarless. We have argued that Combinatory Categorial Grammar goes
further: by virtue of its prefix-driven, type-completing design, it aligns with the operational
character of autoregressive generation in a way no other major grammatical formalism does,
and it supports a principled lifting of generated text into typed compositional structures. The
path from dependency to compositionality is, in this sense, a path from observable fluency to
recoverable meaning.
    The perspective this opens brings further scenarios and challenges into view. On the one
hand, the type-checking discipline that CCG naturally imposes on LLM output raises the
question of how far it can actually go in catching hallucinations and the other production defects
characteristic of these models. The answer we have proposed is that it can go a substantial
distance, but only once the notion of “type” is broadened from a purely syntactic category into
a channel, or interface, toward external sources of knowledge — a move that is unsurprising
and even fitting, since it mirrors the evolution of types in their native setting of programming
languages, and so closes a circle with their use in the adjacent setting of natural-language
analysis. On the other hand, it is precisely this move that points to the applicability of the


                                                  24
approach across the full range of LLM output, of which natural-language text is only a part:
programming code of various kinds, structured expressions in domain languages such as SQL
and OWL, and the formal languages of logic and mathematics. As a consequence, the account is
de-anchored from the mind-based theories of language production to which dependency grammar
is inevitably tied.
    Beneath this apparent proliferation of directions lies a single picture. The neural and symbolic
layers of linguistic production rest on a common foundation, the one used creatively, the other
normatively; and it is their pairing — generation disciplined by compositional checking — that
the framework is meant to articulate. If the first phase of generative AI was one of rapid and
largely uncontrolled production, the contribution we have sketched belongs to a second and
more stable phase, in which what is generated can also be checked. This second phase, moreover,
is unlikely to be navigated by any component in isolation. The threats that generative AI poses
and the opportunities it opens call, respectively, for control and for enhancement, and both are
most effectively pursued in a systemic setting — through the interaction of agents, human and
artificial, coordinated within shared communication spaces of the kind formalized in Borghoff et
al. (2025). Within such an architecture, a CCG lifting component has a natural role to play:
alongside its implications for theoretical linguistics, it contributes precisely the auditing and
normative capabilities — typed, incremental, and compositional — that governed generation
requires.


Acknowledgments
This paper resumes a line of inquiry that the author owes to early and recent conversations with
Mark Steedman, whose comments on successive drafts shaped the present version in several
substantive respects: the accurate statement of supertagger generalization to unseen vocabulary,
the pointer to sentence-incremental coreference resolution, and the real-world hallucination
example of section 4.5, which he encountered directly and generously supplied. Errors and
excesses are the author’s own.


Statements and Declarations
Funding. This work was partially supported by the project Ermete (“Extended Reality for
MaintenancE and Training Ecosystem”), funded by the Italian Ministry of Enterprises and Made
in Italy (MIMIT), 2023, Grant number B39J25000400005.

Competing interests. The author is co-founder and shareholder of BB-Smile S.r.l., a univer-
sity spin-off active in blockchain and tokenization applications; the present paper is conceptual
in nature and does not evaluate, employ, or promote any product or service of that company.
The author has no other relevant financial or non-financial interests to disclose.

Data availability.    No datasets were generated or analysed during the current study.

Use of AI-assisted technologies. In preparing this manuscript the author made use of
Claude (Anthropic) as an assistive tool for drafting, revision, literature positioning, and LaTeX
preparation, under the author’s direction and with the author’s review and editing of all content.
The author takes full responsibility for the content of the manuscript.


References
Ades AE, Steedman MJ (1982) On the order of words. Linguist Philos 4(4):517–558


                                                25
Borghoff UM, Bottoni P, Pareschi R (2025) Human–artificial interaction in the age of agentic
 AI: a system-theoretical approach. Front Hum Dyn 7:1579166. https://doi.org/10.3389/
  fhumd.2025.1579166
Bos J (2008) Wide-coverage semantic analysis with Boxer. In: Semantics in Text Processing
 (STEP), pp 277–286
de Marneffe MC, Manning CD, Nivre J, Zeman D (2021) Universal Dependencies. Comput
  Linguist 47(2):255–308
Dennett DC (1987) The Intentional Stance. MIT Press, Cambridge, MA
Findler RB, Felleisen M (2002) Contracts for higher-order functions. In: Proceedings of the
  ACM SIGPLAN International Conference on Functional Programming (ICFP), pp 48–59
Futrell R, Levy RP, Gibson E (2020) Dependency locality as an explanatory principle for word
  order. Language 96(2):371–412
Gibson E (1998) Linguistic complexity: locality of syntactic dependencies. Cognition 68(1):1–76
Gibson E (2025) Syntax: A Cognitive Approach. MIT Press, Cambridge, MA
Grenander M, Cohen S, Steedman M (2022) Sentence-incremental neural coreference resolution.
  In: Proceedings of the Conference on Empirical Methods in Natural Language Processing
 (EMNLP), pp 427–443
Grenander M (2025) Explicit discourse modelling for coreference and summarization. Dissertation,
  University of Edinburgh
Gurnee W, Sofroniew N, Pearce A et al (2026) Verbalizable representations form
 a global workspace in language models. Transformer Circuits Thread. https://
 transformer-circuits.pub/2026/workspace/index.html. Accessed 21 July 2026
Kubota Y (2014) Combinatory categorial grammar as a substructural logic. In: Aizawa M et al
 (eds) New Frontiers in Artificial Intelligence. Springer, pp 25–38
Lambek J (1958) The mathematics of sentence structure. Am Math Mon 65(3):154–170
Lewis M, Steedman M (2014) A* CCG parsing with a supertag-factored model. In: Proceedings
  of the Conference on Empirical Methods in Natural Language Processing (EMNLP), pp
  990–1000
Martínez-Gómez P, Mineshima K, Miyao Y, Bekki D (2016) ccg2lambda: a compositional
 semantics system. In: Proceedings of ACL-2016 System Demonstrations, pp 85–90
Min S, Krishna K, Lyu X et al (2023) FActScore: fine-grained atomic evaluation of factual
 precision in long form text generation. In: Proceedings of the Conference on Empirical Methods
 in Natural Language Processing (EMNLP), pp 12076–12100
Mineshima K, Martínez-Gómez P, Miyao Y, Bekki D (2015) Higher-order logical inference with
 compositional semantics. In: Proceedings of the Conference on Empirical Methods in Natural
 Language Processing (EMNLP), pp 2055–2061
Montague R (1970a) Universal grammar. Theoria 36(3):373–398. Reprinted in: Thomason R
 (ed) Formal Philosophy: Selected Papers of Richard Montague. Yale University Press, 1974
Montague R (1970b) English as a formal language. In: Visentini B et al (eds) Linguaggi nella
 Società e nella Tecnica. Edizioni di Comunità, Milan, pp 189–224. Reprinted in: Thomason R
 (ed) Formal Philosophy: Selected Papers of Richard Montague. Yale University Press, 1974

                                              26
Montague R (1973) The proper treatment of quantification in ordinary English. In: Hintikka J,
 Moravcsik J, Suppes P (eds) Approaches to Natural Language. Reidel, Dordrecht, pp 221–242.
 Reprinted in: Thomason R (ed) Formal Philosophy: Selected Papers of Richard Montague.
 Yale University Press, 1974

Moortgat M (1997) Categorial type logics. In: van Benthem J, ter Meulen A (eds) Handbook of
 Logic and Language. Elsevier, pp 93–177

Morrill GV (1994) Type Logical Grammar: Categorial Logic of Signs. Kluwer, Dordrecht

Pareschi R, Steedman M (1987) A lazy way to chart-parse with categorial grammars. In:
  Proceedings of the 25th Annual Meeting of the Association for Computational Linguistics, pp
  81–88

Poesia G, Polozov A, Le V et al (2022) Synchromesh: reliable code generation from pre-trained
  language models. In: International Conference on Learning Representations (ICLR)

Rimell L, Clark S (2009) Porting a lexicalized-grammar parser to the biomedical domain. J
  Biomed Inform 42(5):852–865

Salzano F, Scalabrino S, Oliveto R, Pareschi R (2026) Beyond code similarity: benchmarking
  the plausibility, efficiency, and complexity of LLM-generated smart contracts. Manuscript
  under review

Scholak T, Schucher N, Bahdanau D (2021) PICARD: parsing incrementally for constrained
  auto-regressive decoding from language models. In: Proceedings of the Conference on Empirical
  Methods in Natural Language Processing (EMNLP), pp 9895–9901

Stanojević M, Steedman M (2019) CCG parsing algorithm with incremental tree rotation. In:
  Proceedings of the 2019 Conference of the North American Chapter of the Association for
  Computational Linguistics: Human Language Technologies (NAACL-HLT), pp 228–239

Stanojević M, Steedman M (2020) Max-margin incremental CCG parsing. In: Proceedings of
  the 58th Annual Meeting of the Association for Computational Linguistics, pp 4111–4122

Stanojević M, Brennan JR, Dunagan D, Steedman M, Hale JT (2023) Modeling structure-building
  in the brain with CCG parsing and large language models. Cogn Sci 47(7):e13312

Steedman M (2000) The Syntactic Process. MIT Press, Cambridge, MA

Steedman M (2011) Taking Scope: The Natural Semantics of Quantifiers. MIT Press, Cambridge,
  MA

Turing AM (1950) Computing machinery and intelligence. Mind 59(236):433–460

van Benthem J (1983) The semantics of variety in categorial grammar. Technical Report 83-29,
  Department of Mathematics, Simon Fraser University

Wadler P (2015) Propositions as types. Commun ACM 58(12):75–84

Wijnholds G, Sadrzadeh M, Clark S (2020) Representation learning for type-driven composition.
 In: Proceedings of the 24th Conference on Computational Natural Language Learning (CoNLL),
 pp 313–324

Willard BT, Louf R (2023) Efficient guided generation for large language models. arXiv preprint
 arXiv:2307.09702



                                              27
Yoshikawa M, Noji H, Matsumoto Y (2017) A* CCG parsing with a supertag and dependency fac-
  tored model. In: Proceedings of the 55th Annual Meeting of the Association for Computational
  Linguistics, pp 277–287

Zettlemoyer LS, Collins M (2005) Learning to map sentences to logical form: structured
  classification with probabilistic categorial grammars. In: Proceedings of the Conference on
  Uncertainty in Artificial Intelligence (UAI), pp 658–666




                                             28
