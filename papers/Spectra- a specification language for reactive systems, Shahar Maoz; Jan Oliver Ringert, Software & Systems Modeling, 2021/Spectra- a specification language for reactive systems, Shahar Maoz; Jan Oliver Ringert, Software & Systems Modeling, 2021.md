Software and Systems Modeling (2021) 20:1553–1586
https://doi.org/10.1007/s10270-021-00868-z

    REGULAR PAPER



Spectra: a specification language for reactive systems
Shahar Maoz1          · Jan Oliver Ringert2

Received: 16 February 2020 / Revised: 23 September 2020 / Accepted: 14 December 2020 / Published online: 14 April 2021
© The Author(s) 2021


Abstract
We introduce Spectra, a new specification language for reactive systems, specifically tailored for the context of reactive
synthesis. The meaning of Spectra is defined by a translation to a kernel language. Spectra comes with the Spectra Tools,
a set of analyses, including a synthesizer to obtain a correct-by-construction implementation, several means for executing
the resulting controller, and additional analyses aimed at helping engineers write higher-quality specifications. We present
the language in detail and give an overview of its tool set. Together with the language and its tool set, we present four
collections of many, non-trivial, large specifications, written by undergraduate computer science students for the development
of autonomous Lego robots and additional example reactive systems. The collected specifications can serve as benchmarks for
future studies on reactive synthesis. We present the specifications, with observations and lessons learned about the potential
use of reactive synthesis by software engineers.

Keywords Reactive synthesis · GR(1) · Specification language


1 Introduction                                                              such as RATSY [6], and Slugs [22], to list a few. Still, major
                                                                            challenges remain on the way to bringing the correct-by-
Reactive synthesis is an automated procedure to obtain a                    construction promise to software engineering practice.
correct-by-construction reactive system from its temporal                      Some of these challenges are at the level of the specifica-
logic specification [66]. Rather than manually constructing                 tion language, i.e., the syntax, semantics, and expressiveness
an implementation and using model-checking or testing to                    of reactive specifications. First, the language should have
verify it against a specification, see Fig. 1 top, synthesis offers         features that are specific to its use in the context of reactive
an approach where a correct implementation of the system                    synthesis, such as the explicit distinction between system and
is automatically obtained for a given specification, see Fig. 1             environment variables, and the explicit distinction between
bottom, if such an implementation exists.                                   guarantees and assumptions. Second, careful balance should
    As the correct-by-construction promise is attractive, much              be found between the language’s usability to engineers, in
research effort has been invested and much progress has                     writing and reading, on the one hand, and its formal expres-
been achieved over the last two decades on reactive synthesis               sive power, on the other hand. Finally, the language alone may
theory, algorithms, and tools. These include, e.g., the identi-             not be enough to address all challenges. Rather, a set of analy-
fication of expressive fragments of temporal logics that have               ses and tools, beyond synthesis itself, specifically tailored for
efficient, symbolic synthesis solutions [10,41,42], various                 the new language and its use in an end-to-end reactive syn-
kinds of compositional synthesis [46], controller synthesis                 thesis environment, is required, for example, in debugging
for probabilistic systems [20,44], support for the addition of              specifications and in executing the synthesized controllers.
quantitative criteria [5], bounded synthesis [26], and tools                In this paper we describe the results of our research efforts
                                                                            over the last five years, to start developing such language and
Communicated by Antonio Vallecillo.                                         tool set.
                                                                               We introduce Spectra, a new specification language for
B Shahar Maoz                                                               reactive systems, specifically tailored for the context of
     maoz@cs.tau.ac.il
                                                                            reactive synthesis. The meaning of Spectra is defined by
1    School of Computer Science, Tel Aviv University, Tel                   a translation to a kernel language. Importantly, beyond the
     Aviv-Yafo, Israel                                                      kernel, Spectra includes advanced language features like
2    School of Informatics, University of Leicester, Leicester, UK


                                                                                                                                  123
1554                                                                                                                         S. Maoz, J. O. Ringert


                                                                               ing languages for code generation and the deployment of
                                                                               synthesized controller on robots [50,52], but, as already
                                                                               demonstrated in the SYNTECH collection of specifications,
                                                                               this is only one of the use cases of Spectra.
                                                                                   Finally, currently, Spectra is not about specifications that
                                                                               cover probabilistic, timed, or other quantitative requirements.
                                                                               Many other works, including some by the authors of the
                                                                               present paper, have discussed various extensions of synthesis
                                                                               to handle specifications with these objectives [2,5,11,16,36,
                                                                               48]. We believe that adding language elements for expressing
                                                                               these and similar objectives, and extending Spectra Tools to
                                                                               support them, is possible; however, it is outside the scope of
                                                                               our current work.
                                                                                   A number of logics and languages exist for the spec-
Fig. 1 A high-level contrast of inputs (left) and outputs (right) for tradi-
tional verification or testing (top) and the synthesis approach (bottom)       ification of reactive systems. These include linear tem-
                                                                               poral logic (LTL) [65], Property Specification Language
                                                                               (PSL) [23], SMV—the input language of the NuSMV
                                                                               tool [15], TLA+ [45] (Temporal Logic of Actions), and the
parametric predicates, monitors, bounded integers and arith-                   Temporal Logic Synthesis Format (TLSF) [35]. Moreover, a
metic operations, a library of patterns and means to define                    number of specification languages for reactive synthesis have
new patterns, bounded counters, and quantified arrays. These                   been developed on top of GR(1), with related synthesis tools,
advanced language features, some of which are unique to                        including ApsectLTL [54], LTLMop (Linear Temporal Logic
Spectra, are meant to enable and encourage reuse and support                   MissiOn Planning) [27], SGR(1) [12,17], Slugs (SmalL bUt
specifications’ readability and maintainability by engineers.                  Complete GROne Synthesizer) [22], Open Promela [25],
   Spectra comes with the Spectra Tools, a set of analyses,                    Tulip [24,76], and RATSY [6]. As we show, Spectra has
including not only a synthesizer to obtain a correct-by-                       unique language features, unique supporting analyses and
construction implementation, but also several means for exe-                   execution mechanisms, and a large set of benchmark spec-
cuting the resulting controller. It further includes additional                ifications, not available for these other languages and tools.
analyses aimed at helping engineers write higher-quality                       We discuss the above languages and tools and compare them
specifications, including, e.g., several means to dealing with                 to Spectra in Sect. 8.
unrealizable and non-well-separated specifications.                                The contributions of this paper are as follows:
   To date, Spectra has been used by small teams of under-
graduate computer science students for the development of
autonomous Lego robots and additional example reactive                          – We present the Spectra language definition, including
systems in four-semester long project classes we have taught                      formal syntax and semantics of its unique constructs.
at Tel Aviv University, in 2015, 2017, 2019, and 2020. From                       While a few previous papers have already used small
these classes, we have collected over 320 versions of speci-                      example specifications written in Spectra, in the lim-
fications of about 10 different Lego robots and 14 additional                     ited context of presenting a specific new analysis (e.g.,
systems, all written by these students as they worked on                          for non-well-separation [51], for unrealizability [43,53],
their projects for several months. Thus, together with the lan-                   for vacuity [57]), the syntax and semantics of the lan-
guage and the tool set, we present four collections of many,                      guage were not presented before. Moreover, several of
non-trivial, large specifications. The collections can serve                      the unique and powerful constructs of the language,
as benchmarks for future studies on reactive synthesis. We                        beyond the kernel, including monitors, PastLTL oper-
present the specifications the students wrote, with observa-                      ators, bounded counters, and quantified arrays, did not
tions and lessons learned about the potential use of reactive                     appear in any previous publication.
synthesis by software engineers.                                                – We present an overview of Spectra Tools. While specific
   It is important to note that Spectra is designed for gen-                      tools have been individually presented in previous pub-
eral purpose reactive systems specifications rather than for                      lications (e.g., for dealing with unrealizability [43]), an
the particular domain of robotics (as, e.g., in the case of                       overview of the Spectra Tools architecture and tool set did
LTLMop [27]). Spectra is also not to be confused for an                           not appear before. All tools we report on in our overview
architecture modeling language for robotic systems (as,                           have been implemented and already used by the under-
e.g., RoboChart [60] or MontiArcAutomaton [69]). Spectra                          graduate students who participated in our project classes
can and has been used in combination with C&C model-                              and created the specifications in the four collections.


123
Spectra: a specification language for reactive systems                                                                         1555


 – We present four collections of specifications, all writ-        2 Background
   ten by undergraduate students in project classes we have
   taught. Together, the collections include over 320 ver-         We provide background on linear temporal logic and syn-
   sions of specifications of about 10 different Lego robots       thesis, which is required for the definition of Spectra syntax
   and 14 additional systems. The collections are larger and       and semantics. We continue with the notation that we use to
   more complex than all previous collections of reactive          define the grammar of Spectra.
   systems specifications published in the context of syn-
   thesis, and can thus serve as new benchmarks for future         2.1 Linear temporal logic and synthesis
   studies in the field.
 – We present a discussion of design decisions, observa-           We repeat some of the standard definitions of linear temporal
   tions, and lessons we have learned from the development         logic (LTL), e.g., as found in [10], a modal temporal logic
   of Spectra and Spectra Tools and from our experience            with modalities referring to time [65]. The syntax of LTL for-
   with it so far. The discussion covers topics such as the dif-   mulas is typically defined over a set of atomic propositions
   ficulty of writing specifications, the necessity of internal    AP with the future temporal operators X (next) and U (until).
   symbolic representations, the fundamental design deci-          Intuitively, an atomic proposition is similar to a Boolean vari-
   sion of choosing GR(1) as kernel for Spectra, the decision      able. If the variable is true, the atomic proposition is present;
   to implement our own synthesizer, and the decision to           if the variable is false, the atomic proposition is absent.
   make Spectra domain agnostic.
                                                                   Definition 1 The syntax of LTL formulas over AP is
                                                                   ϕ ::= p | ¬ϕ | ϕ ∨ ϕ | Xϕ | ϕUϕ for p ∈ AP.
   Spectra and Spectra Tools aim to advance the state of the
                                                                       For  = 2AP , a computation u = u 0 u 1 .. ∈  ω is a
art in reactive synthesis. For engineers who develop reac-
                                                                   sequence where u i is the set of atomic propositions that hold
tive systems, they provide a novel and friendly language
                                                                   at the i-th position. For position i we use u, i | ϕ to denote
and environment to experience writing formal specifications,
                                                                   that ϕ holds at position i, inductively defined as:
examine the idea of reactive synthesis, and start considering
whether and how it may be applicable to the systems they
                                                                    – u, i | p iff p ∈ u i ;
develop. For researchers, they provide a testbed and bench-
                                                                    – u, i | ¬ϕ iff u, i | ϕ;
mark data for future research on specification languages
                                                                    – u, i | ϕ1 ∨ ϕ2 iff u, i | ϕ1 or u, i | ϕ2 ;
and reactive synthesis development environments. We make
                                                                    – u, i | Xϕ iff u, i+1 | ϕ;
Spectra, Spectra Tools, and all specifications we report about
                                                                    – u, i | ϕ1 Uϕ2 iff ∃k ≥ i: u, k | ϕ2 and ∀ j, i ≤ j <
publicly available for inspection and further use by engineers
                                                                      k: u, j | ϕ1 .
and researchers.
                                                                     We denote u, 0 | ϕ by u | ϕ. We use additional LTL
1.1 Paper structure                                                operators F (finally) where Fϕ := true U ϕ and G (globally),
                                                                   where Gϕ := ¬F¬ϕ.
The paper is structured as follows. Section 2 provides nec-          Finally, we also use PastLTL [29] operators Y (previously,
essary background on linear temporal logic and its GR(1)           dual of X) and S (since, dual of U):
fragment, which are required for the formal definition of
Spectra semantics. Section 3 introduces a small language            • u, i | Yϕ iff i > 0 ∧ u, (i − 1) | ϕ;
kernel of Spectra and defines the semantics of a specification      • u, i | ϕ1 Sϕ2 iff ∃k ≤ i: u, k | ϕ2 and ∀ j, k < j ≤
as a GR(1) synthesis problem. This section also introduces            i: u, j | ϕ1 .
an example specification that serves as a running example
throughout the paper. Section 4 covers the language elements           We use additional PastLTL operators O (once), where
Spectra provides and defines their semantics via translations      Oϕ := true S ϕ, and H (historically), where Hϕ := ¬O¬ϕ.
to the kernel. In Sect. 5 we give an overview of Spectra               LTL formulas can be used as specifications of reactive sys-
Tools. We describe our preliminary experience with Spectra         tems where atomic propositions are represented by Boolean
in Sect. 6, which is mainly based on observations from the         variables. The set of variables representing atomic propo-
project classes we have taught over the five years where stu-      sitions is partitioned into Boolean environment (input) and
dents have used Spectra and Spectra Tools to develop about         system (output) variables. An assignment to all variables is
10 different autonomous Lego robots and several additional         called a state.
systems. In Sect. 7 we discuss lessons learned about Spectra,          A strategy for an LTL specification ϕ prescribes the
Spectra Tools, and our design decisions. We discuss related        outputs of a system that from its winning states for all
work in Sect. 8 and conclude in Sect. 9.                           environment choices lead to computations that satisfy ϕ. A


                                                                                                                         123
1556                                                                                                                       S. Maoz, J. O. Ringert


specification ϕ is called realizable if a strategy exists such
                                                                              ϕ sr = (θ e → θ s ) ∧
that for all initial environment choices the initial states are
winning states. The goal of LTL synthesis is, given an LTL                        (θ e → G((Hρ e ) → ρ s )) ∧
                                                                                                                
specification, to find a strategy that realizes it, if one exists.                  (θ e ∧ Gρ e → (      GFJie →   GFJ js ))
   To illustrate the difference between LTL model-checking                                            i∈1..n          j∈1..m
and LTL synthesis in Fig. 1, we could replace specification
by LTL formula and implementation by controller (a formal-                       Specifications for GR(1) synthesis have to be expressible
ization of a strategy).                                                      in the above structure and thus do not cover the complete
                                                                             LTL. Efficient symbolic algorithms for GR(1) realizability
2.2 Generalized reactivity of rank 1 (GR(1))                                 checking and controller synthesis have been presented in [10,
                                                                             64].
LTL synthesis is computationally expensive. Thus, authors                        As an example, consider a GR(1) synthesis problem to
have suggested fragments of LTL that have efficient synthesis                synthesize the controller for the traffic light of a simple junc-
algorithms.                                                                  tion with a main street and a side street (this example is
   GR(1) is a fragment of LTL that has an efficient symbolic                 illustrated in Fig. 3 and further explained in Sect. 3.1):
synthesis algorithm [10,64] and whose expressive power cov-
ers most of the well-known LTL specification patterns of                      • X = {cm, cs} represents information about a car on the
Dwyer et al. [21,49]. GR(1) specifications include assump-                      main street (cm) and on the side street (cs);
tions and guarantees about what needs to hold on all initial                  • Y = {gm, gs} represents control over a green light on
states, on all states and transitions (safety), and infinitely                  the main street (gm) and on the side street (gs);
often on every run (justice). A GR(1) synthesis problem con-                  • θ e = ¬cm ∧¬cs, i.e., initially there is no car on the main
sists of the following elements [10]:                                           street nor the side street;
                                                                              • θ s = , i.e., no restriction on initial outputs;
 – X is a set of Boolean input variables controlled by the                    • ρ e = , i.e., no safety assumptions;
   environment;                                                               • ρ s = ¬(gm ∧ gs), i.e., the main street and side street
 – Y is a set of Boolean output variables controlled by the                     never have a green light at the same time;
   system;                                                                    • J e = {cm, cs}, i.e., cars are always eventually appearing
 – θ e is an assertion, i.e., a propositional logic formula, over               on the main street and on the side street;
   X characterizing initial environment states;                               • J s = {gm, gs}, i.e., the light must always eventually turn
 – θ s is an assertion over X ∪Y characterizing initial system                  green on the main street and on the side street.
   states;
 – ρ e (X , Y, X ) represents constraints on the transition                  This example GR(1) synthesis problem is realizable iff this
   relation of the environment, where X denotes a primed                     LTL formula is realizable:
   copy of variables X , i.e., given a current state, ρ e restricts
   the next input;                                                            ((¬cm ∧ ¬cs) → ) ∧
 – ρ s (X , Y, X , Y ) represents constraints on the transition                   ((¬cm ∧ ¬cs) → G(H() → ¬(gm ∧ gs))) ∧
   relation of the system, where X and Y denote primed                                 ((¬cm ∧ ¬cs) ∧ G() →
   copies of variables X and Y, i.e., given a current state
                                                                                           ((GF(cm) ∧ GF(cs)) → (GF(gm) ∧ GF(gs))))
   and next input, ρ s restricts the next output;
     e
 – Ji∈1..n  is a set of assertions over X ∪Y for the environment
                                                                                An example strategy that satisfies this GR(1) synthesis
   to satisfy infinitely often (called justice assumptions);
                                                                             problem could alternate between output gs ∧¬gm and output
     s
 – J j∈1..m  is a set of assertions over X ∪ Y for the system
                                                                             ¬gs ∧ gm, which ensures that the lights are never green
   to satisfy infinitely often (called justice guarantees).
                                                                             at the same time and that always eventually each light will
                                                                             turn green. The goal of reactive synthesis is to compute such
   A GR(1) synthesis problem is strictly realizable1 iff the
                                                                             strategies automatically.
following LTL formula is realizable:
                                                                                GR(1) synthesis has been used and extended in differ-
                                                                             ent contexts and for different application domains, includ-
                                                                             ing robotics [40,47,52], scenario-based specifications [55],
1 Note that many authors, including us, sometime present the simpler         aspect languages [54], event-based behavior models [18],
and more intuitive formula for implication realizability rather than the     hybrid systems [24], and device drivers [74], to name a few.
one for strict realizability. For a comparison of strict realizability and
implication realizability and a reduction between the two, see [10,38].
Spectra supports strict realizability.


123
Spectra: a specification language for reactive systems                                                                          1557


2.3 Extended notation for context-free grammars                     level keyword replaces to denote that a new production
                                                                    rule replaces an existing production rule. As an example,
The Spectra language is defined by a context-free grammar.          the production specWithImports replaces spec in
We now describe the grammar notation that we use through-           Sect. 4.10, Fig. 13, l. 1. As a result of the replacement, the
out this paper. Our notation is based on common concepts            symbol specWithImports replaces any occurrence of
known from language workbenches, e.g., MontiCore [33]               the symbol spec.
and XText [77]. An excerpt of the Spectra grammar is shown
                                                                    Special productions We make use of three standard, prim-
in Fig. 2.
                                                                    itive productions that we do not define in any production
    Production rules are enclosed in brackets and printed bold.
                                                                    rule. These are file for file names, name for names of
As an example, the production rule for symbol specElem
                                                                    elements, and int for integers.
is defined in Fig. 2, l. 5 and referenced in l. 3 inside the def-
inition of the production rule for symbol spec. We use            Simplification The parts of the Spectra grammar we show in
common multiplicity symbols for defining the number of              Sects. 3 and 4, present a simplified version of the grammar
repetitions of elements, where ∗ denotes zero or more repeti-       that we use in the implementation of Spectra Tools, described
tions, + denotes at least one repetition, and ? denotes zero or     in Sect. 5. For the purpose of presentation, we have simplified
one repetitions, i.e., the element is optional. As an example,      the production rules. As an example, it is common to encode
the declaration of specification elements (specElem, l. 3)        operator precedence directly into production rules in order to
is repeated at least once. Terminals of the grammar that are        simplify the parsing of specifications. This implementation
also keywords of Spectra are printed in blue, e.g., the key-        related formulation blows up the grammar of expressions as
words spec, sys, and env. Other terminals are printed in gray,      every operator might require a separate production rule. We
e.g., the semicolon (;, l. 7) after a variable declaration.         present a simplified version of the grammar and define oper-
Grammar extensions For readability and modular language             ator precedence when we describe each language element.
definition, we introduce two extensions to the grammar
notation. First, we introduce internal names for produced
symbols, e.g., the name elems for the list of specElem            3 Spectra kernel
in Fig. 2, l. 3. We refer to these internal names when we
describe well-formedness rules of Spectra documents. Sec-           Spectra is based on a small kernel language for writing spec-
ond, we introduce the grammar-level keyword extends to              ifications. The Spectra kernel contains only the essential
denote the extension of production rules. As an example, the        elements to formulate GR(1) synthesis problems. Specif-
production monitor extends specElem in Fig. 2, l. 9.            ically, these language elements are Boolean environment
As a result of the extension, the symbol monitor can              variable declarations, Boolean system variable declarations,
replace any occurrence of the symbol specElem. Note               assumptions, and guarantees. We now introduce the syntax
the difference between varDec and monitor which                 of the Spectra kernel and then give the semantics of speci-
are both alternatives for specElem. The difference is that        fications as GR(1) synthesis problems. We will extend and
production rule varDec was included in the definition of          modify the example as we introduce new language elements
specElem, while the production rule monitor was                 throughout Sect. 4.
added later. We use this extension mechanism when we add
new language features. Finally, we introduce the grammar-           3.1 Example

                                                                    Consider a traffic light on a simple junction as shown in Fig. 3.
                                                                    A team of engineers specified this system in Lst. 1 using only
                                                                    language elements of the Spectra kernel.
                                                                       As a first step, the engineers identify the environment and
                                                                    system controlled variables by determining the inputs and
                                                                    outputs of the system. Two Boolean environment variables
                                                                    carMain and carSide (Lst. 1, ll. 3–4) model sensors
                                                                    to notify whether there is traffic on the main street or on
                                                                    the side street, respectively. The system controls two traf-
                                                                    fic lights through the Boolean variables greenMain and
                                                                    greenSide (Lst. 1, ll. 6–7).
                                                                       Next, the engineers define assumptions, which character-
Fig. 2 Excerpt of the Spectra grammar to demonstrate our extended   ize environment behavior, and guarantees, which express the
notation for context-free grammars                                  required system behavior. The team assumes that initially


                                                                                                                          123
1558                                                                                                                         S. Maoz, J. O. Ringert




Fig. 3 A junction of a side street connecting to a main street. The figure
shows the environment controlled variables carMain and carSide
representing sensors for detecting traffic on each street, and the system
controlled variables greenMain and greenSide for controlling the
traffic lights


there is no traffic and that always eventually there is traf-
fic on each of the streets (Lst. 1, ll. 9–11). The system has
to guarantee that traffic passage at the same time on both
streets never occurs (Lst. 1, l. 13). In addition, the system
has to guarantee to always eventually allow traffic passage
on each of the streets (Lst. 1, ll. 14–15).
    Finally, the engineers check whether the specification
is realizable and synthesize an implementation. In case
an implementation cannot be found, the engineers update
the specification by weakening guarantees or strengthening
assumptions. The Spectra specification shown in Lst. 1 is
                                                                             Fig. 4 Grammar of the Spectra kernel
realizable. A simple, possible implementation keeps one traf-
fic light green until a car arrives and passes, and then repeats
the same for the other street.                                               3.2 Syntax
                                                               Spectra
                                                                             A grammar of the Spectra kernel is shown in Fig. 4. Every
 1   spec T r a f f i c L i g h t                                            valid specification can be produced from the production rule
 2
                                                                             spec of the kernel grammar (and its extensions we present
 3   env b o o l e a n c a r M a i n ;
 4   env b o o l e a n c a r S i d e ;                                       in Sect. 4).
 5                                                                              Every specification starts with the keyword spec and a
 6   sys b o o l e a n g r e e n M a i n ;                                   name. The name of a specification is only informative and has
 7   sys b o o l e a n g r e e n S i d e ;                                   no technical meaning. A specification contains one or more
                                                                             specification elements specElem. Specification elements
 8

 9 asm ini c a r M a i n = f a l s e & c a r S i d e = f a l s e ;
10 asm a l w E v c a r M a i n ;                                             of the Spectra kernel are variable declarations (Fig. 4, l. 7),
11 asm a l w E v carSide ;                                                   assumptions (Fig. 4, l. 11), and guarantees (Fig. 4, l. 16).
12                                                                              Variable declarations introduce variables controlled by the
13 gar alw !( g r e e n M a i n & g r e e n S i d e ) ;
                                                                             environment (keyword env) or by the system (keyword sys).
14 gar a l w E v c a r M a i n & g r e e n M a i n ;
15 gar a l w E v carSide & greenSide ;                                       Variables have a type and a name. The only type available in
                                                                             the kernel is boolean (Fig. 4, l. 9).
Listing 1 A specification –expressed in the Spectra kernel language–            Assumptions have an optional name and can be of three
for a simple traffic light controller consisting of environment variables
env, system variables sys, environment assumptions asm, and system           kinds. They are either initial assumptions (keyword ini),
guarantees gar.                                                              safety assumptions (keyword alw), or justice assumptions
                                                                             (keyword alwEv).2 All assumption kinds are formulated by

                                                                             2 Other GR(1)-based specification languages use the LTL operator G

                                                                             for alw and GF for alwEv. This leads to confusion as their semantics


123
Spectra: a specification language for reactive systems                                                                           1559


expressions exp (Fig. 4, l. 21). Expressions follow standard             To obtain the semantics of assumptions and guarantees, we
definitions of propositional expressions. The unary operators          translate their expression exp to assertions in the GR(1)
of expressions are negation and next, the binary operators             synthesis problem. This translation is straightforward on
are standard Boolean operators and equality, and the pri-              the structures of exp. The symbols of Boolean opera-
mary expressions are true, false, and references to variables          tors of unaryOp and binaryOp are translated to their
(Fig. 4, l. 30). The precedence of operators in expressions            counterparts in assertions. The keywords false and true of
from strongest binding to weakest is !, next, =, &, |, <->,            primExp are translated to a contradiction and a tautology,
->. As usual, binary operators associate from left to right.           respectively. A variable reference of primExp is trans-
   Guarantees are defined analogously to assumptions, with             lated to an assertion over a Boolean variable from X and Y
the exceptions of the keyword gar instead of asm and dif-              with the referenced name. Finally, the unary operator next
ferences in well-formedness rules.                                     substitutes all variables from X and Y in its scope with cor-
Well-formedness rules The names of variables, assumptions,             responding primed variables from X and Y .
and guarantees have to be unique. An initial assumption can-               To illustrate the semantics, note that the specification
not reference system variables. A safety assumption cannot             shown in Lst. 1 corresponds to the GR(1) synthesis prob-
nest references to system variables in the scope of the next           lem example presented at the end of Sect. 2.2. The envi-
operator. A next operator cannot be (transitively) nested              ronment variables carMain and carSide correspond
inside a next operator.                                                to atomic propositions cm and cs. The assumption ini
Scopes The Spectra kernel contains three kinds of named                carMain=false & carSide=false from Lst. 1, l. 9
elements: variables, assumptions, and guarantees. The scope            is translated to θ e = ¬cm ∧ ¬cs in Sect. 2.2.
of variable names is global, i.e., the names of variables have
to be unique and variables can be referenced from anywhere
in the specification. The scope of names of assumptions and            4 Spectra language elements
guarantees is also global but they cannot be referenced from
anywhere inside the specification.                                     We now present the Spectra language elements beyond
                                                                       the kernel language. The language elements we present
3.3 Semantics                                                          include enumerations and bounded integers (Sect. 4.1),
                                                                       defines and type definitions with arrays (Sect. 4.2), state
The semantic domain of the Spectra kernel language is GR(1)            invariants (Sect. 4.3), PastLTL operators (Sect. 4.4), pred-
synthesis problems. We define the semantics of the Spectra             icates (Sect. 4.5), monitors (Sect. 4.6), counters (Sect. 4.7),
kernel by translating every well-formed specification to a             patterns (Sect. 4.8), quantification (Sect. 4.9), and imports
GR(1) synthesis problem.                                               (Sect. 4.10).
   Given a Spectra specification m, its semantics is defined              For each language element we (1) discuss the motivation
by the following GR(1) synthesis problem:                              to have it in the language (including an example in the context
                                                                       of the junction from Lst. 1 – a complete example of most lan-
 – X is the set of all variables declared in m with the keyword        guage elements in one specification is shown in App. B), (2)
   env;                                                                present its syntax as a grammar that extends the Spectra ker-
 – Y is the set of all variables declared in m with the keyword        nel, (3) list well-formedness rules of the extended language,
   sys;                                                                (4) discuss the scope of newly introduced named elements,
 – θ e is the conjunction of the semantics of all initial              and finally (5) present the semantics of new elements.
   assumptions (with keyword ini);                                        Note that we define the semantics of Spectra language ele-
 – θ s is the conjunction of the semantics of all initial guar-        ments by a translation to Spectra without the new language
   antees (with keyword ini);                                          element. A direct translation to the Spectra kernel would be
 – ρ e (X ∪ Y, X ) is the conjunction of the semantics of all          possible but often more complicated because all combina-
   safety assumptions (with keyword alw);                              tions of language elements would have to be considered in the
 – ρ s (X ∪ Y, X ∪ Y ) is the conjunction of the semantics             translation, e.g., references to defines can appear in param-
   of all safety guarantees (with keyword alw);                        eters of predicates. Instead, we present modular translations
     e
 – Ji∈1..n  is the set of the semantics of all justice assumptions     that allow for the combination of any subset of Spectra lan-
   (with keyword alwEv);                                               guage elements. The application of all semantics defining
     s
 – J j∈1..m  is the set of the semantics of all justice guarantees     translations will result in a specification in the Spectra ker-
   (with keyword alwEv).                                               nel language. This design also ensures that extensions of the

usually does not match the LTL semantics. We discuss this further in
Sect. 7.3.


                                                                                                                           123
 1560                                                                                                                  S. Maoz, J. O. Ringert


 Spectra kernel beyond GR(1) will directly support the new
 Spectra language elements.3

 4.1 Enumerations and bounded integers

 4.1.1 Motivation

 The Spectra kernel contains only Boolean variables. How-
 ever, in many cases it is more convenient to use enumerations
 of values to define the type of a multi-valued variable. As an
 example, system variable go in Lst. 2, l. 6 has values MAIN,
 SIDE, and NONE. In expressions, these values can be used
 and compared to each other and to variables of the same type.
    Similarly, some values are best modeled using integers.
 Spectra supports a bounded integer type with lower and upper
 bounds. An example appears in Lst. 2 where the variables
 carsMain and carsSide are of integer type with values
 from 0 to 10 and 0 to 6, respectively. Bounded integers can
 be compared to integer literals, arithmetic expressions, and          Fig. 5 Syntax of enumeration types and bounded integers
 other integer variables (see Lst. 2, ll. 9-11) even when their
 bounds are different.
                                                                       stronger than all previously introduced operators. Finally,
                                                                       we add arithmetic negation as a unary operator and integer
                                                            Spectra
                                                                       constants as primary expressions in Fig. 5, ll. 15–19.
 1   spec T r a f f i c L i g h t E n u m I n t e g e r s              Well-formedness rules The names of enumeration values
 2
 3   env Int ( 0 . . 1 0 ) c a r s M a i n ;                           must be unique and different from variable names. Equal-
 4   env Int ( 0 . . 6 ) c a r s S i d e ;                             ity is the only comparison allowed for enumeration values
 5                                                                     and variables of enumeration type and Boolean type. The
 6   sys { MAIN , SIDE , NONE } go ;
                                                                       upper bound upper of a bounded integer must be strictly
 7
 8   gar ini go = NONE ;                                               greater than its lower bound lower . The new operators
 9   gar alw c a r s M a i n >= c a r s S i d e ->                     intBinaryOp and intUnaryOp can only be used
10                                           next ( go = MAIN ) ;      in arithmetic expressions constructed from these operators,
     gar alw c a r s S i d e > c a r s M a i n ->
                                                                       primitive values intVal, and references to integer vari-
11
12                                           next ( go = SIDE ) ;
                                                                       ables (alternative var Re f of primRef).
 Listing 2 An example of declaring an enumeration variable go and
 integer variables for comparing numbers of cars in a guarantee.
                                                                       4.1.3 Semantics

 4.1.2 Syntax                                                          We define the semantics of enumerations and bounded inte-
                                                                       gers by a translation into Spectra without enumerations and
 The syntax of enumerations and bounded integers is shown              bounded integers. We translate every variable of an enumer-
 in Fig. 5. Enumerations are defined by production rule                ation type with n = |vals| values to log2 (n) Boolean
 enumType and consist of a list of names enclosed in curly           variables. To every value in vals, we assign one combina-
 brackets {, }. Names of enumeration values can be referenced          tion of values of the new variables. We add initial and safety
 as primary expressions (Fig. 5, ll. 5–6), e.g., they can also be      constraints to the specification so that the new variables repre-
 used in expressions.                                                  sent one of the defined values (important for 2log2 (n)  > n).
    Bounded integer types in Spectra start with Int, followed          We translate every equality expression involving enumera-
 by lower and upper bounds in parenthesis (Fig. 5, ll. 9–10).          tions to equivalent expressions over the Boolean variables
 We also add arithmetic operators for addition, subtraction,           that encode them.
 multiplication, division, and modulo to Spectra, together with           Similarly, we translate every bounded integer variable to
 inequalities in Fig. 5, l. 12–13. The inequalities bind with the      log2 (upper − lower ) Boolean variables. For the trans-
 same priority as equality, and the arithmetic operators bind          lation of bounded arithmetic expressions, we employ an
                                                                       encoding inspired by Bartzis and Bultan [4].
 3 Examples of extensions are GR(k) specifications [63], cooperative

 synthesis [7], or GR(1)* [3].


 123
    Spectra: a specification language for reactive systems                                                                              1561


    4.2 Defines and type definitions with arrays                           4.2.2 Syntax

    4.2.1 Motivation                                                       The syntax of defines and type definitions is shown in Fig. 6.
                                                                           Defines are specification elements and thus appear as top
    Specifications often contain sub-expressions that reoccur              level elements inside specifications. Defines have a name and
    multiple times. In the example of the traffic light, one might         an expression. References to defines defRef are primary
    expect that many constraints refer to empty streets, for-              expressions (Fig. 6, l. 4).
    mally carSide=false & carMain=false. If these                             Type definitions (Fig. 6, l. 8) are also specification
    reoccurring expressions get longer and more complicated,               elements and thus appear as top level elements inside speci-
    the overall specification becomes harder to read and diffi-            fications. Type definitions have a name and a type.
    cult to maintain, e.g., when updating a condition. To support             References to type definitions typeRef are treated as
    more concise specifications and to simplify the maintenance            types (Fig. 6, l. 13). We introduce array declarations in the
    of reoccurring sub-expressions, Spectra introduces defines.            same rule as references to type definitions. Array declarations
    In the traffic light example, we might introduce the name              reference a type definition and define any number of dimen-
    streetsEmpty for the expression carSide=false &                        sions of the array. Array fields are accessed in the same way
    carMain=false shown in Lst. 3, ll. 1-2. Assumptions and                as any other variable (Fig. 6, l. 17): a variable reference is
    guarantees may then use streetsEmpty as a reference to                 followed by the coordinates of the specific field.
    the define (ll. 4-6).                                                  Well-formedness rules The names of defines and type defini-
                                                          Spectra          tions must be unique names of elements of the specification.
     1   d e f i n e s t r e e t s E m p t y :=                            Defines with the operator next may not be used in expres-
     2              carSide = false & carMain = false ;                    sions where next is not allowed, e.g., defines with the
     3                                                                     operator next may not be nested inside the operator next.
     4 asm ini s t r e e t s E m p t y ;
                                                                           Note that the expression of a define is not required to evaluate
     5 gar alw s t r e e t s E m p t y ->
     6       ! greenMain & ! greenSide ;                                   to a Boolean value. However, the semantics of a specifica-
                                                                           tion with defines and type definitions has to be a well-formed
    Listing 3 An example of a define that is used in an assumption and a
                                                                           specification.
    guarantee.
       Similarly, several variables in a specification may be of
    the same type. Here, to support more concise specifications
    and to simplify the maintenance of reoccurring types, Spectra
    introduces type definitions. In Lst. 4, the enumeration type
    Item is defined by a type definition in l. 1 and referenced as
    the type of a system variable in l. 4.
       Finally, the readability of some specifications benefits
    from using array types rather than many individual variables.
    As an example, we define a two-dimensional array of type
    Item in Lst. 4, l. 4 with both dimensions of size 10, i.e., an
    array with 100 fields. The initial guarantee in Lst. 4, l. 6 ref-
    erences a field of the array and states that its value is ROBOT
    of the array’s type Item.
                                                             Spectra
1   type { EMPTY , OBSTACLE , BASE , ROBOT } Item ;
2
3   // 10 by 10 map of a w o r k s p a ce of items
4   sys Item [ 1 0 ] [ 1 0 ] map ;
5
6   gar ini map [ 0 ] [ 0 ] = R O B O T ;

    Listing 4 An example definition of type Item and a two-dimensional
    (e.g., x and y coordinates) array of items.
                                                                           Fig. 6 Syntax of defines and type definitions with arrays




                                                                                                                                       123
1562                                                                                                                    S. Maoz, J. O. Ringert


   Finally, each dimension of an array needs to be positive.              not a state invariant and will directly be interpreted as part of
All references to array fields need to have the same number               the GR(1) kernel.
of coordinates as the referenced array has dimensions.4 All                  Note that this language extension does not add new syntax
coordinates in a field reference need to be smaller than the              to Spectra and is implemented on the level of the semantics
corresponding dimension of that array.                                    of operator alw, see Sect. 7.3.
Scopes The names of defines and type definitions have the                 Well-formedness rules The expression exp of a state invari-
same scope as the names of environment and system variables               ant may not contain the operator next. A state invariant of
defined in the Spectra kernel. The names of defines are visible           the environment, i.e., used in an assumption, may not contain
to other defines.                                                         system variables.

4.2.3 Semantics                                                           4.3.3 Semantics

We define the semantics of defines and type definitions with              We define the semantics of state invariants by a translation
arrays by a translation into Spectra without defines and type             of state invariants to Spectra without state invariants. Every
definitions. Every reference to a define is replaced by the               state invariant is translated into an initial constraint with the
expression of the define. Then, we expand any variable or                 same expression exp and a safety constraint (with keyword
parameter declarations that include array declarations into               alw) with the expression exp nested inside the operator
multiple variable or parameter declarations that still include            next. Together, the two constraints ensure that the invariant
references to type definitions but no further array declara-              holds in the initial state and in every successor state.
tions, e.g., the array-type variable declaration in Lst. 4, l. 4 is
translated into 100 variable declarations of type Item with               4.4 PastLTL
fresh names (one for each field of the array). All references to
array fields are replaced by a reference to the corresponding,            4.4.1 Motivation
expanded variable or parameter. Finally, every reference to a
type definition is replaced by the type of the type definition.           Assumptions and guarantees define constraints on reactive
                                                                          behavior by relating the inputs and outputs of the current
                                                                          state to those of the next state. However, in some situations
4.3 State invariants
                                                                          the restriction to only current and next inputs and outputs
                                                                          becomes limiting. As an example, consider the assumption
4.3.1 Motivation
                                                                          that a car appears on the side street at least once in every
                                                                          run. This assumption cannot directly be expressed in terms
Some constraints should hold in all states, e.g., the guaran-
                                                                          of current and next inputs and outputs, and also not directly as
tee that green lights on the side and main street never occur
                                                                          a justice assumption that would have to hold infinitely often.
together (Lst. 1, l. 13). These assumptions and guarantees
                                                                          However, this assumption is easily formalized using PastLTL
could be expressed as combinations of initial and safety con-
                                                                          operators supported by Spectra inside a justice assumption:
straints; however, we chose to introduce a special handling
                                                                          alwEv ONCE carSide.
for state invariants to make specifications easier to read and
write.5
                                                                          4.4.2 Syntax

4.3.2 Syntax                                                              We show the syntax of PastLTL expressions in Fig. 7. Spec-
                                                                          tra supports three unary PastLTL operators and one binary
The syntax of state invariants is a subset of safety constraints          PastLTL operator. For all operators Spectra also provides
from the kernel, specifically, the subset of tempConstra-                a one letter abbreviation (preceding the operator name in
int with keyword alw where the following expression                      Fig. 7).
does not contain the operator next. If the following expres-              Well-formedness rules All operands of PastLTL operators
sion includes the operator next, then the safety constraint is            must evaluate to Boolean values (all PastLTL expressions
                                                                          evaluate to Boolean values).
4 Note that this does not allow for partial evaluation of a multi-

dimensional array to a lower-dimensional array. For this task and other   4.4.3 Semantics
use cases Spectra provides quantification, see Sect. 4.9.
5 Note that the common keyword G used for alw in other GR(1) spec-
                                                                          We define the semantics of PastLTL by a translation of
ification languages is often confused for defining state invariants (as
the LTL semantics would suggest), leading to problems we discuss in       PastLTL to Spectra without PastLTL. Recall from the pre-
Sect. 7.3.                                                                liminaries that the two operators PREV and SINCE provide


123
Spectra: a specification language for reactive systems                                                                                       1563


                                                                                                                                        Spectra
                                                                        1   sys b o o l e a n g r e e n M a i n ;
                                                                        2   sys b o o l e a n g r e e n S i d e ;
                                                                        3   sys b o o l e a n g r e e n P e d e s t r i a n ;
                                                                        4
                                                                        5   p r e d i c a t e excl ( b o o l e a n p , b o o l e a n q ) :
                                                                        6       !( p & q ) ;
                                                                        7
                                                                        8   gar alw excl ( greenMain , g r e e n S i d e ) &
                                                                        9           excl ( g r e e n P e d e s t r i a n , g r e e n S i d e ) ;

                                                                        Listing 5 An example of a predicate definition and predicate instances
Fig. 7 PastLTL operators introduced as extensions of unary and binary   in a guarantee.
operators


full expressiveness of PastLTL; all other PastLTL operators             4.5.2 Syntax
can be defined in terms of these two, e.g., the operator ONCE
ϕ used in our example is defined as true SINCE ϕ. We will               We show the syntax of predicate definitions and predicate
show the translation for the operators PREV and SINCE.                  instantiations in Fig. 8. The grammar starts with the syntax
   Given the PastLTL expression PREV ϕ, we create a                     for predicate definitions predicate, which are specifi-
Boolean system variable aux with a fresh name. We then                  cation elements and thus appear as top level elements inside
add the initial guarantee ini !aux and the safety guarantee             specifications. Predicate definitions have a name, followed
alw next(aux) <=> ϕ. Technically, the variable aux                      by a list of typed parameters typedParam. The body of
stores the previous valuation of ϕ. Finally, we replace all             a predicate definition is an expression.
occurrences of PREV ϕ with a reference to the new variable                 Predicate instances predInst (Fig. 8, ll. 11–12) are
aux.                                                                    primary expressions. Instances reference the name of a pred-
   Given a PastLTL expression ϕ SINCE ψ, we create a                    icate and provide expressions for each parameter of the
Boolean system variable aux with a fresh name. We then add              predicate.
the initial guarantee ini aux <=> ψ and the safety guaran-              Well-formedness rules All parameters of predicate instances
tee alw next(aux) <=> (aux & next(ϕ) | next(ψ)).                        must be expressions that evaluate to the type declared in the
The variable aux is true if ψ holds or if aux was true before           predicate definition. The body of the predicate must be an
and ϕ holds, i.e., if ϕ holds since ψ was true in the past.             expression that evaluates to Boolean. The body of a predicate
Finally, we replace all occurrences of ϕ SINCE ψ with a                 cannot (also not transitively, e.g., through predicate instances
reference to the new variable aux.                                      or defines) contain an instance of the predicate itself.

4.5 Predicates

4.5.1 Motivation

Sometimes, repeating parts that appear in specifications dif-
fer in sub-expressions. In these cases, defines from Sect. 4.2
cannot be used to avoid repetition. Instead, for these cases, we
introduce predicates, which can instantiate sub-expressions
with their parameters.
   As an example, consider an extension of the traffic light
with pedestrian crossing, as shown in Lst. 5. Similar to a
green light on the main street, a green light for pedestrians
should also mutually exclude a green light on the side street.
To avoid repetition and manual errors, we can extract the
expression for mutual exclusion into a predicate with two
parameters as shown in Lst. 5, ll. 5-6. The predicate can then
be instantiated, e.g., in a guarantee as shown in l. 8.                 Fig. 8 Syntax of predicates with names, parameters, and a predicate
                                                                        body over parameters




                                                                                                                                      123
1564                                                                                                                       S. Maoz, J. O. Ringert


Scopes The names of predicates have the same scope as the
names of environment and system variables defined in the
Spectra kernel. As a result, the names of predicates are visible
to other predicates. The names of parameters of the predicate
are only visible inside the body of the predicate.

4.5.3 Semantics

We define the semantics of predicate instantiations and pred-
icates by a translation into Spectra without predicates. Every
predicate instance is translated into a Boolean expression.             Fig. 9 Syntax of monitors with types, names, and monitor constraints
Technically, we replace a predicate instance by a copy of the
body of the predicate. In the copy, we replace references to
predicate parameters by the expressions provided for each
parameter.                                                              4.6.2 Syntax

4.6 Monitors                                                            The syntax of monitors is shown in Fig. 9. Monitors are
                                                                        specification elements and thus appear as top level elements
4.6.1 Motivation                                                        inside specifications. Monitors have a type and a name. The
                                                                        body of a monitor consists of initial and safety constraints.
Assumptions and guarantees define constraints on reactive                  References to monitors monRef are primary expres-
behavior by relating the inputs and outputs of the current state        sions (Fig. 9, l. 8), i.e., monitors can be referenced in the
to those of the next state. However, in some situations, the            same way as variables.
restriction of referencing only inputs and outputs becomes              Well-formedness rules The names of monitors must be unique
limiting. As an example, consider an extension of the traffic           names of elements of the specification. The body of a monitor
light with a button for pedestrians to press. The system should         may not contain justice constraints. The expression exp
guarantee that all button presses eventually lead to a green            of an initial constraint may not include the unary operator
light for pedestrians. Yet, in our example, there is no variable        next. The semantics of the constraints in the body of the
indicating whether a request has already been served. As a              monitor must assign a unique value to the monitor in any
solution, Spectra introduces monitors, which come with a                step, and it must not restrict any other variable (when seen
definition of how their value is updated at every execution             as an automaton with the monitor variable as states and all
step. As an example, the monitor needGreenMain (Lst. 6,                 other variables as input, the defined automaton has to be
l. 6–12) is of type boolean and its value is updated on button          deterministic and complete).6
presses not followed by green lights. This monitor is used in           Scopes The names of monitors have the same scope as the
a guarantee (Lst. 6, l. 4) to ensure that requests are always           names of environment and system variables defined in the
eventually handled.                                                     Spectra kernel. Importantly, the name of a monitor is visible
                                                       Spectra          in the constraints of the monitor.
1   env b o o l e a n p e d e s t r i a n B t n ;
2   sys b o o l e a n g r e e n P e d e s t r i a n ;
3
4   gar alwEv ! n e e d G r e e n M a i n ;                             4.6.3 Semantics
5
6  monitor boolean needGreenMain {                                      We define the semantics of monitors by a translation of
7    ini n e e d G r e e n M a i n =
 8     ( pedestrianBtn & ! greenPedestrian );                           monitors to Spectra without monitors. For every monitor def-
 9   alw next ( n e e d G r e e n M a i n ) =                           inition, we create a system variable with the name and type
10     (( n e e d G r e e n M a i n | p e d e s t r i a n B t n ) &     of the monitor. All monitor constraints become guarantees.
11                                   ! greenPedestrian );
                                                                        All references to the monitor become references to the new
12 }
                                                                        system variable with the same name and type.
Listing 6 An example of a monitor and referencing it inside a justice
guarantee.



                                                                        6 This property is difficult to check or ensure syntactically. See also

                                                                        Sect. 7.


 123
Spectra: a specification language for reactive systems                                                                                 1565


4.7 Counters

4.7.1 Motivation

Some constraints require to keep track of number of occur-
rences of cases, events, or actions, e.g., for the traffic light we
might want to limit the number of steps that an ambulance on
the main street has to wait before the light turns green. Spec-
tra provides bounded integers and arithmetic operations (see
Sect. 4.1), which in principle allow one to formulate count-
ing. However, using them for expressing counting, based on
explicit safety constraints, may be tedious and error prone.
    As a solution, Spectra introduces counters, which come
with a definition of how their value is increased, decreased,
or reset at an execution step. For example, Lst. 7 shows              Fig. 10 Syntax of bounded counters with names, and constraints
a bounded counter ambulanceWait from 0 to 5 that
increases when an ambulance waits on the main street (Lst. 7,
l. 2). The counter is reset once the main street light is green. In   Well-formedness rules The names of counters must be unique
case of overflows the counter’s current value is kept (Lst. 7,        names of elements of the specification. The body of a counter
l. 4). The counter in the example is referenced in a guarantee        may not contain justice constraints. The expression exp of
that asserts that the number of steps that an ambulance waits         an initial constraint (ini) may not include the unary operator
is below 5.                                                           next. The semantics of any inc, dec, or reset constraints
    Using a counter, counting is encapsulated in a dedicated          of the counter must be exclusive, i.e., a counter cannot be
specification element, tailored to counting related definitions.      increased, decreased, or reset at the same time. (Spectra Tools
This hides the complexity of using safety constraints to define       checks this and reports relevant problems if found.) Counters
counting, and makes it easier to correctly define and use vari-       may only be referenced in arithmetic expressions.
ables that serve as counters.                                         Scopes The names of counters have the same scope as the
                                                          Spectra     names of environment and system variables defined in the
 1 counter ambulanceWait (0..5) {                                     Spectra kernel. Importantly, the name of a counter is visible
 2   inc : a m b u l a n c e M a i n & ! g r e e n M a i n ;          in the constraints of the counter.
 3   reset : greenMain ;
 4   o v e r f l o w : keep ;
 5 }                                                                  4.7.3 Semantics
 6

 7   gar alw a m b u l a n c e W a i t < 5;
                                                                      We define the semantics of counters by a translation of coun-
Listing 7 An example of a counter to count ambulance wait and a       ters to Spectra without counters. For every counter definition,
guarantee referencing the counter in an arithmetic expression.        we create a system variable of integer type with the size
                                                                      and the name of the counter. The initial counter constraint
                                                                      becomes an initial guarantee. Any inc, dec, or reset con-
                                                                      straint of the counter becomes a safety guarantee that implies
4.7.2 Syntax
                                                                      correct increase, decrease, or reset (to lower bound) of the
                                                                      counter variable value with respect to the chosen overflow
The syntax of counters is shown in Fig. 10. Counters are spec-
                                                                      semantics. The default underflow and overflow methods are
ification elements and thus appear as top level elements inside
                                                                      false.
specifications. Counters have a range and a name. The body
of a counter contains optional initial (ini), increment (inc),
decrement (dec), and reset (reset) constraints. As all counters        – For overflow type false, the guarantees for inc and
are bounded, a counter may declare overflow and underflow                dec constraints are expressed without checking over- or
methods, where false means that an over-/underflow may not               underflows, i.e., these would lead to safety guarantee vio-
happen, keep preserves current counter values, and modulo                lations.
sets the counter to the opposite bound.                                – For overflow type keep, we add a case distinction to the
    References to counters ctrRef are primary expres-                  guarantees for inc and dec constraints to handle over-
sions (Fig. 10, l. 8), i.e., counters can be referenced in the           flows and underflows by preserving the current counter
same way as variables.                                                   values.


                                                                                                                             123
1566                                                                                                                          S. Maoz, J. O. Ringert


 – For overflow type modulo, we add a case distinction to                                                                                Spectra
   the guarantees for inc constraints to set the counter at the         1  /**
   upper bound to its lower bound. Respectively, for dec                2    * Kind : R e s p o n s e : s r e s p o n d s to p
   constraints we set a counter at the lower bound to its                3   * Scope : G l o b a l l y
                                                                         4   * LTL : G ( p -> F s )
   upper bound.                                                          5   *
                                                                         6   * @ p a r a m p t r i g g e r s the r e s p o n s e
   Finally, we add a safety guarantee where the conjunction              7   * @ p a r a m s is the r e s p o n s e
                                                                         8   */
of the negations of all inc, dec, and reset constraints implies          9 pattern pRespondsToS (p , s) {
that the counter variable does not change its value. All ref-           10     var { S0 , S1 } state ;
erences to the counter become references to the new system              11     ini state = S0 ;
                                                                        12     alw (( state = S0 & ((! p ) | ( p & s ) ) &
variable with the same name and bounded integer type.
                                                                        13                                     next ( state = S0 ) ) |
                                                                        14     ( state = S0 & ( p &! s ) & next ( state = S1 ) ) |
4.8 Patterns                                                            15     ( state = S1 & ( s ) &          next ( state = S0 ) ) |
                                                                        16     ( state = S1 & (! s ) &         next ( state = S1 ) ) ) ;
                                                                        17     alwEv ( state = S0 ) ;
4.8.1 Motivation                                                        18 }


                                                                            Listing 8 Definition of the response pattern of Dwyer et al. [21] as
Specifications of reactive systems require engineers to                     instantiated in Lst. 9. This definition was automatically generated as
express complex temporal relations between environment                      described in [49].
and system variables. LTL provides great expressiveness for
temporal relations. However, some relations, if expressed
directly in LTL, lead to long formulas, which might be com-                                                                              Spectra
plicated to read, challenging to write, or simply not within            1    gar p R e s p o n d s T o S ( carMain , g r e e n M a i n ) ;
the restricted syntax of GR(1). As an example, consider the             2    gar p R e s p o n d s T o S ( carSide , g r e e n S i d e ) ;
popular response pattern that a car on the main street even-                Listing 9 An example instantiation of the response pattern of Dwyer et
tually leads to a green light. This guarantee can be expressed              al. [21] as supported by Spectra.
in LTL as follows7 :
                                                                               Note that the response pattern expresses the requirement
G (carMain -> F greenMain)                                                  of letting cars pass much better than the justice guarantee
                                                                            used in Lst. 1, l. 14, as the latter required the now unnecessary
   Note that even this simple LTL formula is not in the GR(1)               assumption in Lst. 1, l. 10, that always eventually cars will
fragment.                                                                   be on the main street.
   Dwyer et al. [21] have identified 55 LTL specification pat-                 Note that Spectra patterns are not limited to the 52 patterns
terns that are common in industrial specifications. They have               defined in the catalog. Spectra provides engineers with means
suggested a classification and natural language descriptions                to define and reference their own patterns.
for the identified patterns. The example above is one of their
patterns and would be transcribed as:
                                                                            4.8.2 Syntax
greenMain responds to carMain
                                                                            The syntax of patterns is shown in Fig. 11. The grammar starts
                                                                            with the syntax for pattern definitions pattern, which are
   We have investigated patterns for GR(1) synthesis in [49].
                                                                            specification elements and thus appear as top level elements
We have shown that 52 of these 55 LTL specification patterns
                                                                            inside specifications. Pattern definitions have a name, fol-
can be supported as assumptions and guarantees for GR(1)
                                                                            lowed by a list of parameter names. The body of a pattern
synthesis.8 In Spectra, the example guarantee is formulated
                                                                            definition can declare variables local to the pattern and tem-
as a pattern definition (Spectra comes with a catalog of pattern
                                                                            poral constraints. A pattern may contain any number of initial
definitions for all 52 supported LTL specification patterns,
                                                                            and safety constraints, but it must contain exactly one justice
e.g., the one shown in Lst. 8) and the pattern instantiation
                                                                            constraint.
shown in Lst. 9, l. 1.
                                                                               Pattern instances patInst (Fig. 11, ll. 12–13) are tem-
7 LTL formula taken from the patterns catalog of Dwyer et al. [21].
                                                                            poral constraints. Instances reference the name of a pattern
There might be multiple ways to express an equivalent guarantee.
                                                                            and provide expressions for each parameter of the pattern.
8 The three patterns that cannot be supported, number 23, 50, and 55,       Well-formedness rules The body of a pattern contains exactly
are among the least frequently used patterns according to the survey        one justice constraint. The expression exp of an initial
reported in [21].                                                           or justice constraint may not include the unary operator


123
Spectra: a specification language for reactive systems                                                                                        1567


                                                                             Instantiated initial pattern constraints become initial guar-
                                                                          antees; instantiated safety pattern constraints become safety
                                                                          guarantees; the instantiated justice constraint becomes a jus-
                                                                          tice assumption if the pattern instance is contained inside an
                                                                          assumption; and the instantiated justice constraint becomes
                                                                          a justice guarantee if the pattern instance is contained inside
                                                                          a guarantee (the formal translation appears in [49]).


                                                                          4.9 Quantification

                                                                          4.9.1 Motivation

                                                                          Arrays, integers, and counters allow for very succinct speci-
                                                                          fications. However, some constraints apply to fields of arrays
Fig. 11 Syntax of patterns with names, parameters, auxiliary variables,   or for specific values of integer variables. Writing these con-
and pattern constraints over auxiliary variables and parameters           straints could become very repetitive. To ensure that this
                                                                          kind of repetitive constraints can be written succinctly in
next. The expression exp of a safety constraint may only                Spectra, we introduce universal and existential quantifica-
include references to pattern variables var s in the scope of             tion. Consider the example shown in Lst. 10. The universal
the operator next. The semantics of the initial and the safety            quantification in l. 5 states that either the current value of
constraints must assign a unique value to all pattern variables           pos is p or active pickup requests at position p stay active.
in any step and must not restrict any other variable (when                                                                               Spectra
seen as an automaton with the pattern variables as states and             1   type P o s i t i o n = Int ( 0 . . 5 ) ;
all other variables as input, the defined automaton has to be             2   env P o s i t i o n pos ; // c u r r e n t p o s i t i o n pos
deterministic and complete).9                                             3   env b o o l e a n [5] r e q P i c k U p ; // pickup
                                                                                  r e q u e s t s at p o s i t i o n s
    The production patInst may only appear exclusively                  4
as a temporal constraint in assumptions or guarantees, i.e., it           5   gar alw f o r a l l p in P o s i t i o n . pos = p | (
can appear neither inside another expression nor in any other                     r e q P i c k U p [ p ] -> next ( r e q P i c k U p [ p ]) ) ;
place in a specification.                                                 Listing 10 An example of a universal quantification over an integer
Scopes The names of pattern parameters params, and the                    type used inside a comparison with another integer variable and for
names of pattern variables var s, areonly visible inside the            addressing the fields of a Boolean array
body of the pattern, delimited by , The names of pat-
terns are visible beyond specification files and thus can be
imported, Sect. 4.10. This is important for the ability to                4.9.2 Syntax
reuse patterns across specifications.
                                                                             The syntax for quantification is shown in Fig. 12. A
4.8.3 Semantics                                                           quantified expression quantExp starts either with the
                                                                          universal quantifier forall or with the existential quantifier
We define the semantics of patterns by a translation of pat-              exists. The quantifier is followed by a variable name and its
tern instances and patterns to Spectra without patterns. For              domain. Finally, a quantified expression contains an expres-
every pattern instance, we create a copy of all pattern vari-             sion exp.
ables as system variables with a fresh name and the same
type. We instantiate pattern constraints by replacing refer-
ences to pattern variables with references to the fresh names
and by replacing references to variable names with copies of
the corresponding expression of the parameter values from
pV als.




                                                                          Fig. 12 Grammar for universal and existential quantification in Spectra
9 This property is difficult to check syntactically. See also Sect. 7.




                                                                                                                                       123
1568                                                                                                                S. Maoz, J. O. Ringert


   We also extend the syntax of references to array fields.       Well-formedness rules The names of patterns and predicates
Array fields can be indexed by names of quantified variables      in all imported and in the current Spectra files must be unique.
in addition to integer literals (as shown in Fig. 6).             The bodies of all (transitively) imported predicates may only
Well-formedness rules Replacing the quantified variable by        contain references to other predicates and their parameters
any literal from its domain makes the quantified expression       (e.g., they may not reference system or environment variables
well-formed. Only quantified variables of integer types may       or defines from other specifications10 ).
index fields of arrays.
Scopes The names of quantified variables are visible inside       4.10.3 Semantics
the quantified expression.
                                                                  We define the semantics of imports by a translation of imports
4.9.3 Semantics                                                   to Spectra without imports. Given a Spectra file with imports,
                                                                  we copy all (transitively) referenced patterns of the imported
We define the semantics of quantification by a translation        files into the current file. We also copy all (transitively) refer-
of quantification to Spectra without quantification. Start-       enced predicates into the current file and remove the import
ing from inner-most quantified expressions, every universal       statements.
quantification is replaced by a conjunction of copies of the
quantified expression, where every occurrence of the quanti-
fied variable is replaced by a different value from its domain.   5 Spectra Tools
Similarly, every existential quantification is replaced by a
disjunction.                                                      Spectra comes with Spectra Tools, a set of analyses and tools
                                                                  packaged as an extensible set of Eclipse plug-ins. A rich
                                                                  Eclipse editor for Spectra is implemented using XText [77].
4.10 Imports
                                                                  All symbolic representations and operations are carried out
                                                                  using a BDD library (several libraries can be used, including,
4.10.1 Motivation
                                                                  e.g., CUDD [72]).
                                                                     Spectra Tools is available from [73], together with a user
We have motivated many language features of Spectra based
                                                                  guide and many example specifications. Beyond the SYN-
on reuse. In all cases, a reuse within a single specification
                                                                  TECH specifications we describe in Sect. 6, the examples on
makes sense. In some cases, a reuse across specifications is
                                                                  the Spectra website include specifications and simulations
also desirable. As an example, patterns, e.g., from the cata-
                                                                  for some classic problems, such as the Towers of Hanoi,
log of Dwyer et al. [21] or domain-specific pattern collections
                                                                  Cinderella and her stepmother, moving obstacle evasion, etc.
for mobile robots [59], are general and should be useful for
                                                                  We encourage the interested reader to try them out.
many different specifications. Thus, to support reuse across
                                                                     We now give an overview of the architecture of Spectra
specifications, we have added an import mechanism to Spec-
                                                                  Tools and how it supports language extensions, including the
tra. A specification can import other specifications and thus
                                                                  ones presented in Sect. 4.
use their patterns and predicate definitions (see Sect. 4.5 and
Sect. 4.8).
                                                                  5.1 Spectra Tools Architecture
4.10.2 Syntax                                                     We have built Spectra Tools in a modular way that supports
                                                                  separation of concerns and reduces technological depen-
The syntax of imports is shown in Fig. 13. We extend specifi-     dencies. The main concerns of Spectra Tools are the input
cations with import statements. Each import statement starts      language syntax, the definition of semantics of language con-
with the keyword import, contains a filename in quotation         structs in terms of the Spectra kernel, a representation of the
marks, and ends with a semicolon.                                 semantics of Spectra at the BDD level, analyses and tools that
                                                                  operate on this BDD-based representation, and a UI layer.
                                                                  These concerns (shown as gray, rounded boxes) are reflected
                                                                  in a set of components shown in Fig. 14.
                                                                     Spectra Tools defines a rich abstract syntax representation
                                                                  of Spectra including its kernel and all language elements

                                                                  10 Note that these references from predicates are allowed in general
Fig. 13 Grammar for imports in Spectra                            (see Sect. 4.5) and are very convenient to use.


123
Spectra: a specification language for reactive systems                                                                                1569


                                                                             Two main advantages of the Spectra Tools architecture,
                                                                          as we show in Fig. 14, are (1) its separation of technolog-
                                                                          ical and representation concerns and (2) its modularity. As
                                                                          an example, the separation of technological concerns allows
                                                                          for replacing XText by other language workbenches or an
                                                                          API-based use of Spectra Tools (indeed, in addition to the
                                                                          Eclipse-based plug-ins, we provide a command line inter-
                                                                          face that is independent of Eclipse). As another example, the
                                                                          modular semantics definition per language element inside
                                                                          component GameInputTrans leads to small and easily
                                                                          testable translations implementing the semantics of each of
                                                                          the language elements described Sect. 4.
                                                                             We now give an overview of the different analyses and
                                                                          tools. All the features described below are implemented in
                                                                          Spectra Tools.



Fig. 14 A component diagram of Spectra Tools showing main compo-
                                                                          5.2 Realizability checking
nents and their  uses  relations
                                                                          First and foremost, Spectra Tools provides means to check
                                                                          whether a specification is realizable, i.e., whether there exists
inside component GameInput. The semantics of all lan-                     a controller that can ensure all guarantees given that all
guage elements as presented in Sect. 4 is defined by transfor-            assumptions hold. The check is implemented as part of
mations of the abstract syntax. All these transformations are             components GR1 and made available through component
implemented in component GameInputTrans, e.g., the                        SpectraToolsUI shown in Fig. 14.
component contains a class CounterTranslator, which                           As an example, Spectra tools returns a positive result when
implements the translation described in Sect. 4.7.3, a class              checking realizability for the specification from Lst. 1. The
QuantifierTranslator, which implements the trans-                         value of checking realizability without construction a con-
lation described in Sect. 4.9.3, etc.11                                   troller is that this check is usually much faster than controller
    Component BddGenerator takes the abstract syntax of                   construction.
the Spectra kernel and translates it into a BDD-based repre-                  The algorithm for realizability checking follows [10], but,
sentation defined by component GameModel. Importantly,                    importantly, incorporates a number of performance heuris-
this representation is completely independent of any con-                 tics from [28]. We have implemented heuristics in two levels.
crete or abstract syntax of Spectra. Together with component              At the BDD and controlled predecessors computation level,
Games, a structure that encodes the Spectra kernel semantics              we use grouping of variables and their primed copies, com-
as described in Sect. 3.3 is provided.                                    bined conjunction and existential abstraction, and the use of
    GR(1) synthesis, implemented in component GR1, and                    a partitioned transition relation. At the algorithmic level, we
additional more advanced analyses, e.g., component                        use early detection of fixed-point, early detection of unreal-
WellSeparation (see Sect. 5.6), rely on the represen-                     izability, and fixed-point recycling.
tation provided by component GameModel. We describe                           As empirically shown in [28], the combination of all these
some of the different analyses and tools in the following sub-            heuristics provides improvements in realizability checking
sections below.                                                           running times. Moreover, the greatest improvement is for
   Finally, Spectra Tools provides a UI integrated into Eclipse           specifications that have slower original running times. This
that enables engineers to apply analyses to specifications. The           is a positive result, as these specifications are the ones it is
component SpectraToolsUI in Fig. 14 implements the                        most important to address in order to make reactive synthesis
UI. It has dependencies that go all the way up to the level of            more useful and applicable in practice.
the input language, as the UI orchestrates the execution of                   Finally, the evaluation in [28] also shows that thanks
the parser, the translations, and the analyses chosen by the              to these heuristics, Spectra outperforms two previously
engineer.                                                                 published tools, RATSY [6] and Slugs [22], on large spec-
                                                                          ifications. While for small specifications, the other tools
11 A single exception is translation of bounded integers and arithmetic   running times for realizability checking are better than Spec-
operations, which is implemented in component BddGenerator for            tra’s, the larger the specification, the faster Spectra becomes
performance considerations following [4].                                 relative to the two other tools.


                                                                                                                                123
1570                                                                                                                   S. Maoz, J. O. Ringert


   For details about these heuristics and their evaluation,               when they are required. JITS itself is symbolic, and takes
including the details of the comparison against RATSY and                 advantage of the symbolic representation of the results of
Slugs on specifications from the literature, we refer the reader          realizability checking.
to [28].
                                                                          5.4 Controller execution
5.3 Synthesis of concrete and symbolic controllers
                                                                          Spectra Tools provides several different means to execute and
Beyond realizability checking, Spectra Tools includes two                 simulate the synthesized controller, concrete or symbolic.
synthesis features, which take the specification as input and             This functionality is implemented as part of components GR1
output a correct-by-construction controller, if one exists.               and ControllerRunner shown in Fig. 14.
After a series of basic checks and translations, synthesis is                 First is code generation from concrete controllers. The
performed symbolically following the algorithms described                 concrete controller is directly translated to a simple imple-
in [10], with performance heuristics adapted from [28] (see               mentation of a state machine. We currently have application-
above in Sect. 5.2).                                                      specific Java code generation tailored to run on Lego NXT
    As an example, for the specification from Lst. 1 Spectra              robots.
Tools computes a controller that waits for a car to appear on                 Second is an execution API for symbolic controllers. The
the side street, gives a green light to that car, waits for a car         symbolic controller is loaded and iteratively called, at run-
to appear on the main street, gives a green light to that car,            time, with the current inputs from the environment, to provide
and repeats this process indefinitely.                                    the next outputs (assignment to system variables). This run-
    The engineer can choose the form of the synthesis output.             time environment requires a BDD library; however, its use
First, the output may be a concrete controller, which is fur-             is limited to single calls to extract a satisfying assignment.
ther presented in the console or used for application-specific            Our students have used this API to execute their Lego robots
code generation. As the concrete controller is complete for               (where the actual execution runs on a Raspberry Pi) and to
the environment and deterministic for the system, i.e., in                develop some small example standalone Java applications.
every state it accepts all inputs from the environment and                    Third is a simulation environment, inside Eclipse, we call
deterministically responds with an assignment to the system               Controller Walker. The Walker uses the execution API for
variables, it allows for straightforward application-specific             symbolic controllers. It shows the engineer the current state
code generation.                                                          of the controller (values of environment and system vari-
    Second, the output may be a symbolic controller, follow-              ables) and allows her to ‘walk’, step by step, forward and
ing ideas from [10]. Roughly, the symbolic controller consists            backward, on its transition system. It serves as the main tool
of two functions, represented using BDDs. The first BDD                   for closely inspecting the behavior of the synthesized con-
describes the set of allowed initial states, while the second             troller.
describes the controller’s allowed transitions. The engineer
can save it and execute it, see below in Sect. 5.4.                       5.5 Analyses of unrealizability
    One advantage of the concrete controller output is that it
enables direct code generation. When it is very small, it is              One of the challenges of writing specifications for synthesis
also simple to read and inspect. In our experience however,               is unrealizability. Spectra Tools provides several means to
the concrete representation does not even scale to systems                deal with unrealizable specifications.
like the autonomous Lego robots we describe in Sect. 6. Its                  As an example for an unrealizable specification, consider
generation is slow, due to the need to enumerate all states, and          the specification from Lst. 1 where the two assumptions
its size is beyond what any engineer can manually inspect.                alwEv carSide and alwEv carMain are replaced by
Moreover, sometimes the size of straightforward generated                 a single, similar assumption:
code prohibits compilation.12 All these disadvantages moti-
vated us to design and implement the symbolic controller.                 alwEv carSide | carMain
    Finally, we have recently presented just-in-time reactive
synthesis (JITS) [58], and implemented it in Spectra Tools.               Identifying unrealizability and computing an unrealizable
JITS accelerates synthesis time significantly, as it skips the            core When synthesis fails due to unrealizability, the engi-
symbolic controller construction all together. Instead, next              neer receives an appropriate message. Then, she can ask to
states are computed at the controller’s execution time, only              compute an unrealizable core, i.e., a locally minimal subset of
                                                                          the specification’s guarantees, which already makes it unre-
12 As an example, a code generator for Java generating if-statements to   alizable. Spectra Tools computes the core using DDmin [79],
check all inputs easily creates methods larger than 64kB, which is the    following ideas described in [39] and with heuristics inves-
size limit for the Java compiler.                                         tigated in [28]. The core guarantees are highlighted on the


123
Spectra: a specification language for reactive systems                                                                              1571


specification (using Eclipse standard editor markers). The        tion is usually undesired. Specifications that allow it are
user guide in [73] includes example screenshots.                  called non-well-separated [38]. In [51] we have shown that
   In the example above, Spectra Tools highlights the guar-       non-well-separation is a common problem in specifications.
antee alwEv carMain & greenMain as an unrealizable                The well-separation check is implemented as part of compo-
core (the other justice guarantee in Lst. 1 equally constitutes   nent WellSeparation shown in Fig. 14, which depends
another unrealizable core).                                       on component GR1.
Computing a concrete counter-strategy Given an unreal-               As an example, consider the specification from Lst. 1 with
izable specification, the engineer can generate a concrete        the additional assumption alwEv carSide & greenSide.
counter-strategy, which specifies one strategy for the envi-      While Spectra Tools confirms that the original specification
ronment to force any system to violate the specification. The     is well-separated, it finds that the modified version is not.
counter-strategy is computed by playing a Rabin game, fol-        The reason for non-well-separation is that the system could
lowing the algorithm from [39,56]. The counter-strategy can       always set greenSide to false and thus force the environ-
be presented in simple textual format on the console. It can      ment to violate the new assumption.13
also be interactively simulated, together with the JVTS, see         Spectra Tools provides means to identify and investigate
next.                                                             non-well-separation. The engineer can check her specifi-
   In the example above, Spectra Tools computes a strat-          cation for well-separation. If the specification is not well-
egy for the environment that satisfies the modified justice       separated, information about the specific type of non-well-
assumption always by setting carSide to true but con-             separation found is displayed. Furthermore, the engineer
stantly setting carMain to false. This makes it impossible        can ask to compute a strategy that shows how the envi-
for any controller to satisfy the justice guarantee alwEv         ronment can be forced to violate its assumptions. Finally, a
carMain & greenMain.                                              non-well-separation core, a minimal set of assumptions that
Computing a JVTS As concrete counter-strategies may be            leads to non-well-separation, can be computed (again, using
very large and difficult to understand, we have recently pre-     DDmin [79]), and highlighted on the specification (using
sented the Justice Violations Transition System (JVTS), a         Eclipse standard editor markers). See [51].
symbolic representation of a counter-strategy [43]. The JVTS
is much smaller and simpler than its corresponding concrete       5.7 Additional analyses
counter-strategy. Moreover, it is annotated with invariants
that explain how the counter-strategy forces the system to        Spectra Tools provides several additional analyses that aim
violate the specification. We compute the JVTS symbolically,      at helping engineers write higher-quality specifications. We
and thus more efficiently, without the expensive enumeration      give some examples below.
of concrete states. We provide the JVTS with an on-demand             First, some assumptions and guarantees may be trivially
interactive concrete and symbolic play. See [43]. The JVTS        false or trivially true. Clearly, such assumptions or guaran-
computation is implemented as part of component JVTS              tees point to a problem in the quality of the specification,
shown in Fig. 14.                                                 even when they are just redundant. We provide a basic anal-
Suggestions of repairs for unrealizable specifications Given      ysis that looks for such trivial assumptions and guarantees
an unrealizable specification, a repair is a set of assumptions   and highlights them to the engineer. Furthermore, we have
that one may add to the original specification in order to        recently presented a more general and comprehensive work
make it realizable. Spectra Tools implements two symbolic         on detecting inherent vacuities [57]. Intuitively, a specifi-
algorithms for computing repairs, one based on the JVTS,          cation is inherently vacuous if one or more of its elements
which may suggest many possible repairs but is incomplete,        is logically redundant, i.e., removing it will not change the
and a second algorithm, which is sound and complete but           semantics of the specification. We define and detect several
only computes a single repair, if one exists. See [53]. This      kinds of vacuities, as well as a vacuity core, which localizes
repair functionality is implemented as part of components         the cause of vacuity. All these analyses are implemented in
Repair and RepairUI shown in Fig. 14, and depends on              Spectra Tools.
component JVTS.                                                       Second, some Spectra language elements are not easy to
   In the example above, Spectra Tools suggests the interest-     write correctly. For example, monitors contain constraints
ing repair alw carMain = carSide.                                 inside their body that should only restrict the monitor variable
                                                                  itself. However, it is easy to mistakenly write constraints that
5.6 Analyses of non-well-separation                               are contradicting or constraining other variables. These mal-

One way a controller may satisfy a specification is by pre-       13 Note though, that in many cases, Spectra Tools does not exploit non-
venting the environment from satisfying the assumptions,          well-separation, e.g., in our example, it again computes the controller
without satisfying the guarantees. Although valid, this solu-     described in Sect. 5.3.


                                                                                                                             123
1572                                                                                                                  S. Maoz, J. O. Ringert


formed monitors might lead to unrealizability of the whole              work of the students in the project class. In total, we have
specification. Spectra Tools implements checks and high-                collected 327 (= 78 + 149 + 27 + 73) specifications. We
lighting for monitors to rule out this reason for unrealizability.      consider these specifications to be the most realistic and rel-
   Finally, as one would expect from an engineer-friendly               evant examples one could find for the purpose of learning
editor for writing and reading specifications, Spectra Tools            about the challenges of using reactive synthesis in practice.
editor provides an outline, syntax coloring, type checks, and           We made them available for download in [73].
specification completion. These are implemented by taking                   It is important to note the background of the students
advantage of the rich XText [77] APIs.                                  and what we have taught them. All students were third-year
                                                                        computer science undergrads at Tel Aviv University. All had
                                                                        learned Python, Java, and C++ in other classes. All have com-
6 Collections of Spectra specifications                                 pleted basic classes on data structures, computer architecture,
                                                                        and algorithms. Some had limited industry experience as
Over the last five years (in 2015, 2017, 2019, and 2020),               software developers. None had knowledge of formal methods
small teams of 3rd year Computer Science undergraduate                  or any experience with formal verification tools. We taught
students from Tel Aviv University, have used Spectra and                them the syntax and semantics of Spectra, while covering
Spectra Tools in four-semester long project classes we have             only the very basic syntax and semantics of LTL required,
taught. In the first two project classes, in 2015 and in 2017, the      i.e., we taught them the semantics of G and GF, but did not
students have developed about 10 different autonomous Lego              teach the syntax and semantics of the LTL U (until) opera-
robots, which they wrote the specifications for, and actually           tor and the fact that temporal operators can be nested. We
built and run.14 In the third and fourth project classes, in            showed them a few example systems that we have created.
2019 and 2020, the students have developed several example              We did not teach them anything about the inner workings of
systems with a PC-based simulation. From these classes, we              GR(1) synthesis, BDDs, fixed-point algorithms, etc.
have collected over 320 versions of specifications, all written             Thus, it is also important to discuss the quality of the
by these students as they worked on their projects for several          specifications in the four collections. All specifications were
months.                                                                 written by teams of 2-5 third-year students. They wrote the
   In the first two instances of the class, our choice of Lego as       specifications in order to get their robots and systems running
the underlying robotics technology for initial experience with          and working correctly—as they did eventually, satisfying an
Spectra was motivated by its relatively low cost and its mod-           initial set of high-level requirements one may expect from
ularity, allowing us to gain experience from several different          such robots and systems. They wrote them neither in order
robots, e.g., a robot sorting Lego pieces by color, an elevator         to make best use of the language features of Spectra, nor
servicing different floors, a self-parking Lego car, each per-          to look for its advantages or challenges, nor to create high-
forming very different tasks. Furthermore, although different           quality examples of great specifications. One team gave up
in detail and scale, the use of the Lego robots provided us with        in the middle of the project, not for any reason related to the
concrete examples of some of the challenges one expects to              project itself (Elevator project in SYNTECH15 collection).
encounter with real-world robotic technologies, such as the             We still include the specifications they wrote in the collection.
inaccuracy of sensor readings, and the limitations in terms                 We consider the above characteristics to be both a strength
of battery, memory, and computation power. In the 2019 and              and a weakness of these specifications. A weakness, because
2020 classes we have decided to extend our experience with              they cannot be used to demonstrate Spectra best-practices,
systems outside the autonomous robots domain, and there-                reusable solutions, etc., they may include all kinds of redun-
fore suggested other target systems for the students to specify         dancies, use of inconsistent or misleading variable and value
and develop simulations for.                                            names, partial or inaccurate documentation, etc. A strength,
   From this experience, we have learned a lot about the                because they provide a first example of specifications, soft-
challenges of writing specifications for synthesis and using it         ware engineers may write when given a synthesis-based
in practice. We developed some of the tools described above             development environment for reactive systems in order to
as a result of what we learned when guiding the students                make the systems they develop work.
through the projects in the four classes.                                   In the remainder of this section, we present the SYNTECH
   Thus, the SYNTECH15, SYNTECH17, SYNTECH19,                           collections with an overview of each collection. We conclude
and SYNTECH20 collections of specifications we describe                 with aggregated statistics that give a rough idea about the size
below, (SYNTECH for short), were not created specifically               and complexity of the specifications that the students wrote.
for the evaluation in our paper but as part of the ordinary

14 More information including short videos are available from http://

smlab.cs.tau.ac.il/syntech/lego.


123
Spectra: a specification language for reactive systems                                                                        1573


6.1 Collection SYNTECH15                                           variants that the students have submitted, and other specifi-
                                                                   cations from the version control of the projects.
In the class we taught in 2015, the students have cre-
ated the following robots: ColorSort—a robot sorting Lego          6.4 Collection SYNTECH20
bricks by color; Elevator—an elevator servicing different
floors (incomplete); Humanoid—a mobile robot of humanoid           Finally, we have re-taught a similar project class in 2020, in
shape; PCar—a self-parking car; Gyro—a robot with self-            which the students were able to use an improved documen-
balancing capabilities; and SPCar—a second project of a            tation and improved set of tools that implemented all of the
self-parking car.                                                  analyses described in Sect. 5.
   We call this set of specifications SYNTECH15. The set              In this class, the students were divided into 8 teams. Three
consists of 78 specifications of which 61 are realizable and       teams chose to develop a smarthome system. The other teams
17 are unrealizable.                                               developed a controller for a smart neighborhood simulation,
                                                                   for an airport control tower, for a parking lot management
                                                                   system, and for an elevator. All wrote a specification and
6.2 Collection SYNTECH17
                                                                   a corresponding Java simulation with interactive GUI that
                                                                   allows one to execute and play with the synthesized (sym-
We have re-taught a similar project class two years later
                                                                   bolic) controller.
with an improved set of tools that implemented some of
                                                                      We call this set of specifications SYNTECH20. The set
the analyses described in Sect. 5 (i.e., including analysis
                                                                   consists of a total of 73 specifications, including the final
of non-well-separation, but excluding JVTS and repair). In
                                                                   version that the students have submitted, some additional
this class, the students have created the following robots:
                                                                   variants that the students have submitted, and other specifi-
APShuttle—a shuttle car that moves passengers between
                                                                   cations from the version control of the projects.
several stations and returns to a designated station for mainte-
nance; ConvoyCar—a robot car driving in a convoy following
                                                                   6.5 Statistics for SYNTECH collections
a line and evading obstacles; Elevator—an elevator with auto-
matic doors and several modes of operation; RobotArm—a
                                                                   Table 1 presents statistics about the specifications in the SYN-
robotic arm that moves objects; and SimpleCar—a self-
                                                                   TECH15, SYNTECH17, SYNTECH19, and SYNTECH20
parking car.
                                                                   collections. The data give a rough idea about the size and
    We call this set of specifications SYNTECH17. The set
                                                                   complexity of the specifications that the students wrote and
consists of 149 specifications of which 123 are realizable
                                                                   actually used to run their systems. While in all collections
and 26 are unrealizable.
                                                                   we have several versions of specifications for each system
                                                                   (between 4 and 45 versions per specification, most realiz-
6.3 Collection SYNTECH19                                           able, some unrealizable), we show here only the statistics for
                                                                   the last specification submitted by each students team, which
We have re-taught a similar project class in 2019, in which        is, as one would expect, realizable.
the students were able to use an improved set of tools                 For each specification, the table shows the number of lines
that implemented all of the analyses described in Sect. 5          of specification including comments (lines of spec); number
(except repairing of unrealizable specifications, which we         of environment (# env var decls) and system (# sys var decls)
made available in Spectra Tools only after the class ended)        variable declarations—of variables of any type, e.g., integer
as well as new language features including arrays and counter      or enumeration types (also, an array of any size is counted
definitions. Spectra Tools was also, by then, more stable (with    as one variable declaration); number of environment (# bool
less bugs), faster (already employing some of the heuristics       env vars), system (# bool sys vars), auxiliary (# bool aux
presented in [28]), and better documented for its users.           vars) variables, as well as total number of variables (# bool
    In this class, the students were divided into 6 teams. Two     total vars)—these numbers refer to Boolean variables, i.e.,
teams developed a controller for the traffic lights of a 4-way     the variable count after the translation to the Spectra kernel;
junction. Three teams developed a controller for an automatic      number of initial assumptions and guarantees (# ini asm/gar),
teller machine (ATM). One team developed a controller for an       number of safety assumptions and guarantees (# safety asm/-
irrigation system. All wrote a specification and a correspond-     gar), number of justice assumptions and guarantees (# justice
ing Java simulation with interactive GUI that allows one to        asm/gar)—excluding any assumptions or guarantees created
execute and play with the synthesized (symbolic) controller.       by translations; number of pattern instances (# pattern inst),
    We call this set of specifications SYNTECH19. The set          as well as total number of assumptions and guarantees (# total
consists of a total of 27 specifications, including the final      asm/gar)—including pattern instances; number of PastLTL
version that the students have submitted, some additional          operators (# past operators), number of defines (# defines),


                                                                                                                        123
                                                                                                                                                                                   1574




      Table 1 Statistics for the last specifications submitted by the students in SYNTECH15, SYNTECH17, SYNTECH19, and SYNTECH20 collections




123
      Specification                      # lines of   # env var    # sys var    # bool env   # bool sys   # bool aux   #      bool   # ini asm   # ini gar   # safety   # safety
                                         spec         decls        decls        vars         vars         vars         total vars                            asm        gar

      SYNTECH15       ColorSort          176           8           10           12           14            6           32             0           4           2         28
                      Elevator            32           1            1            2            2            0            4             0           1           1          0
                      Gyro               121           4            2            6            5            4           15             3           2           1          9
                      Humanoid           257           4            7            5           18           10           33             1           4           3         30
                      PCar               226           5            4            8           11           10           29             1           1           3         38
                      SPCar              558           3            6            7           15            8           30             0           1           0         49
                      Median             201           4            5            6.5         12.5          7.0         29.5           0.5         1.5         1.5       29.0
      SYNTECH17       APShuttle          471          15            5           16            6           23           45             1           1           9         17
                      Elevator           414           8            4           12            6           15           33             4           1          12         26
                      RobotArm           602           8            6           24           10           18           52             4           5          14         21
                      SimpleCar          267           7            4           14           12           19           45             1           1          11         42
                      ConvoyCar          106           3            3            6            7           10           23             0           1           0         10
                      Median             414           8            4           14            7           18           45             1           1          11         21
      SYNTECH19       Junction I         228           5            2           25            8           11           44             0           0          13          5
                      Junction II        404          10            8           34           20           22           76             0           0          20         14
                      Irrigation         159           9            2           50            4            2           56             2           0          11         51
                      ATM I              123           6            3            9            3            3           15             1           1          17          9
                      ATM II             130           4            5            7            7            3           17             1           2           9         12
                      ATM III            179           5            8           10           13            5           28             1           1          12         15
                      Median             169           5.5          4           17.5          7.5          4           36             1           0.5        12.5       13
      SYNTECH20       S. Neighborhood    213           5            5           19           14           11           44             3           4          10         24
                      Airtraffic         244           9           17            9           17            9           35             1           3           2         23
                      Parking I           88           4            4            8            8            4           20             0           1           3          7
                      SmartHome I        199           5            8           13           10            2           25             5           0          25         12
                      SmartHome II       220           8           15           12           19           23           54             5          10          19         61
                      SmartHome III      273          16           22           29           45           13           87             1           3          12         37
                      AV                 155           6            4           18            7            1           26             0           0           0         40
                      Elevator           227           6            4           27           16            0           43             6           3           8         32
                      Median             216.5         6            6.5         15.5         15            6.5         39             2           3           9         28
                                                                                                                                                                                   S. Maoz, J. O. Ringert
      Table 1 continued
      Specification                     # justice   # justice   # pattern   #    total   #     past   # defines   # predi-   # monitors   # pattern   # counter   #    array
                                        asm         gar         inst        asm/gar      operators                cates                   defs        defs        defs

      SYNTECH15       ColorSort          3           1           4           42           2            3
                      Elevator           0           3           0            5           0            0
                      Gyro               1           2           4           22           0            3
                      Humanoid           0           1           4           43           7            0
                      PCar               2           1           1           47          14            0
                      SPCar              0           1           7           58           1           22
                      Median             0.5         1.0         4.0         42.5         1.5          1.5
                                                                                                                                                                               Spectra: a specification language for reactive systems




      SYNTECH17       APShuttle          1           5           5           39           1           13          1          15            0
                      Elevator           0           4           5           52           4           29          0           7            0
                      RobotArm           0           4           0           48           0           17          9           0            0
                      SimpleCar          4           1          14           74          10            6          0           0            0
                      ConvoyCar          0           3           4           18           0           21          0           1            0
                      Median             0           4           5           48           1           17          0           1            0
      SYNTECH19       Junction I         6           0           8           32           3            1          4           0            0          0            6
                      Junction II        2           8          12           56           0            6          8          10            0          0           16
                      Irrigation         1           0           1           64           0            6           0          0            0          0            0
                      ATM I              0           0           0           27           0           14          0           1            0          1            0
                      ATM II             0           0           0           23           0            1          0           0            0          1            0
                      ATM III            1           1           1           31           0           26          0           2            0          1            0
                      Median             1           0           1           31.5         0            6          0           1            0          0.5          0
      SYNTECH20       S. Neighborhood   11           8           0           60           0            9          8           0            0          0            4
                      Airtraffic        10           9           2           50           0           12          0           0            0          2            0
                      Parking I          7           0           0           18           0            2          1           0            0          1            2
                      SmartHome I       21           3           0           66           0            0          7           0            0          0            0
                      SmartHome II       4           4           2          105          16            8          0           0            0          2            0
                      SmartHome III      8           0           0           61           0            7          5           0            0          3            0
                      AV                 5           2           1           48           0            2          10          0            0          0            4
                      Elevator           0          17           0           66           0            1          0           0            0          0           10
                      Median             7.5         3.5         0           60.5         0            4.5         3          0            0          0.5          1




123
                                                                                                                                                                               1575
1576                                                                                                                    S. Maoz, J. O. Ringert


number of predicate definitions that are used at least once          and Spectra Tools and from our experience with it so far.15
(# predicates), number of monitors (# monitors), number of           The discussion covers the following topics: the difficulty of
pattern definitions beyond the Dwyer et al. patterns (# pat-         writing specifications, the necessity of internal symbolic rep-
tern defs), number of counter definitions (# counter defs),          resentations, the use of alw vs. G, the fundamental design
and number of array definitions (# array defs).                      decision of choosing GR(1) as kernel for Spectra, the deci-
   We provide the following preliminary observations from            sion to implement our own synthesizer, the decision to make
the data in the table. First, note that the specifications are not   Spectra domain agnostic, and the use of the SYNTECH col-
very small and are not trivial. For example, in SYNTECH15            lections as benchmarks.
to SYNTECH20, number of lines of specification (includ-
ing comments) ranges from 32 to 602 (medians 201, 414,
                                                                     7.1 Difficulty of writing specifications
169, 216.5 resp.). The total number of Boolean variables, i.e.,
the variable count after the translation to the Spectra kernel,
                                                                     Many authors have discussed the difficulty of writing formal
ranges from 4 to 87 (medians 29.5, 45, 36, and 39 resp.).
                                                                     specifications, in particular in LTL, see, e.g., [70]. Indeed,
The total number of assumptions and guarantees, excluding
                                                                     one important lesson we have learned from our preliminary
any assumptions or guarantees created by translations, ranges
                                                                     experience with Spectra is the difficulty of writing specifica-
from 5 to 105 (medians 42.5, 48, 31.5, 60.5 resp.).
                                                                     tions.
   Second, note some use of advanced language features
                                                                        Each assumption and guarantee alone, thanks to the inten-
beyond pure GR(1), e.g., PastLTL, monitors, patterns, coun-
                                                                     tionally limited syntax (e.g., no nesting of LTL operators), is
ters, or arrays; however, the use of these advanced features
                                                                     relatively easy to write and read. The use of enumerations,
varies much between specifications and is not pervasive. A
                                                                     defines, and arrays, further makes it easier to write and read
possible explanation for this phenomenon is that the students
                                                                     specifications.
had not enough documentation and examples available to
                                                                        Yet, at the level of a complete specification, consisting
them (as they were using our language and tool set while we
                                                                     of many assumptions and guarantees, writing and reading is
were developing and documenting it, i.e., they did not have
                                                                     difficult. It is very easy to unintentionally write unrealizable
the complete version of the user guide we now made avail-
                                                                     or non-well-separated specifications, and fixing these prob-
able), resulting in problems in understanding, leading to lack
                                                                     lems is difficult. Spectra Tools support for dealing with these
of confidence in using the more advanced language feature.
                                                                     problems and others, as we described in Sect. 5, helps, but
   Finally, note larger and more complex specifications from
                                                                     there is still much room for improvement in this regard.
SYNTECH17 to SYNTECH20 compared to SYNTECH15.
                                                                        Moreover, some students tended to translate an impera-
We believe this is due to the additional language constructs
                                                                     tive way of thinking, which they are used to from traditional
and better tool set available to the students. Predicates, moni-
                                                                     programming languages they know, into too-detailed safety
tors, and pattern definitions, were not available to the students
                                                                     guarantees, rather than writing higher-level assumptions and
of the SYNTECH15. Moreover, starting from SYNTECH17
                                                                     guarantees, and letting the synthesizer solve the dependen-
our students had faster realizability checking (due in part
                                                                     cies and complete the details.
to the heuristics we described in [28]), faster synthesis (due
                                                                        Consider the following as a negative example for the use of
to ability to output a symbolic rather than a concrete con-
                                                                     an imperative style inspired by the forklift example from [50].
troller), and ability to execute the symbolic controller (and
                                                                     An engineer could specify that a forklift should go forward
not the generated code from the concrete one) on the robots.
                                                                     to find cargo, e.g., alw !cargo -> next(forward).
The slight drop in sizes of specifications from SYNTECH17
                                                                     To ensure that the forklift does not hit obstacles, the engi-
to SYNTECH19 and SYNTECH20 might be due to the
                                                                     neer might add alw obstacle -> next(turn), but
different target of the latter. While specifications of SYN-
                                                                     would also have to add an exception to the previous guar-
TECH15 and SYNTECH17 capture the behavior of robotic
                                                                     antee, e.g., change it to alw !cargo & !obstacle ->
systems, specifications of SYNTECH19 and SYNTECH20
                                                                     next(forward). Finally, adding an emergency stop feature
capture behavior integrated in a software system or simula-
                                                                     would again require updating both guarantees with excep-
tion. Moreover, naturally, the use of defines, predicates, and
                                                                     tions. In contrast, our example specification in [50] shows a
arrays makes it easier to write more concise specifications.
                                                                     declarative way of expressing similar behavior in the guaran-
                                                                     tees. In our experience, the imperative style is more natural to
                                                                     students but often leads to unrealizability, while a declarative
7 Discussion
                                                                     15 In a recent short workshop paper, we listed software engineering
We now discuss more general design decisions, observations,          challenges of applying reactive synthesis to robotics [52]. The discus-
and lessons we have learned from the development of Spectra          sion here is broader and is not limited to the robotics domain.


123
Spectra: a specification language for reactive systems                                                                                         1577


style is less natural to students but is easier to maintain and                                                                          Spectra
evolve.                                                                    1   env Int ( 0 . . 3 ) l o a d e d P a c k a g e s ;
                                                                           2   sys b o o l e a n load ;
                                                                           3
7.2 Necessity of symbolic controller and execution                         4   asm alw load -> next ( l o a d e d P a c k a g e s ) =
    mechanism                                                                      l o a d e d P a c k a g e s + 1;
                                                                           5
                                                                           6   // " G " is not S p e c t r a s y n t a x !! only for
Another lesson one can learn from our experience is the                            illustration
necessity to use a symbolic representation for execution.                  7   gar G ( l o a d e d P a c k a g e s = 3 -> ! load ) ;
   Very soon after the students started writing the specifica-             Listing 11 An example where the operator G, often used in GR(1)
tions for SYNTECH15, the size of the generated concrete                    specifications, has a confusing meaning.
controllers we saw prohibited their use for straightforward                   As an example from another GR(1) synthesis tool, a
code generation. Specifically, synthesis often produced con-               bug/issue18 has been reported for Slugs [22], where G has
trollers with thousands of states, which prohibits straightfor-            the syntax []. In the report, a user writes “the environ-
ward code generation due to size limits of the Java compiler.              ment is seemingly allowed to falsify one of its own safety
Thus, we were forced to quickly implement and let the stu-                 requirements, specifically the mutex statement: [] (s1
dents use the symbolic execution mechanism described in                    <-> !s2)”. The user further notes that “The issue is
Sect. 5. With the symbolic execution mechanism, the students               resolved if the env safety is written in the “next” tense:
were able to execute controllers with up to 270 states.16 Based            [](next(s1) <-> next(!s2))”.
on our experience in the SYNTECH projects, with the use                       An informal discussion with one the authors of RATSY [6]
of the symbolic mechanism, execution of large controllers                  reveals an implementation of the same semantics of G in
becomes feasible.                                                          GR(1), which they, however, reported had not led to problems
                                                                           so far.
7.3 Always versus G                                                           We have decided to address this confusion at the language
                                                                           level and avoid it by replacing the GR(1)-G by the new key-
Spectra, as most other GR(1) tools, has previously used the                word alw.19
keyword G instead of alw for safety constraints in assump-
tions and guarantees. However, this use of the keyword G                   7.4 Choice of GR(1) as kernel
instead of alw is different than LTL-G in most GR(1) tools.
This has lead to some cases of confusion (for ourselves, our               A fundamental language design decision we have made early
students, and users of other tools, see below), specifically in            on was to use GR(1) as a kernel for Spectra. Our choice
the context of non-well-separation and for the execution of                of GR(1) was motivated by its performance and expressive
controllers.                                                               power. In retrospect, five years into the development and use
   As an example, consider the simple specification in Lst. 11             of Spectra, we believe that we have made the right decision.
where the environment maintains a counter of loaded pack-                     From the synthesis performance perspective, given our
ages from 0 to 3. If the system sets variable load to true                 efficient symbolic implementation following [10], with some
when loadedPackages=3, the environment has to vio-                         of the additional heuristics investigated in [28], our experi-
late its assumption as it cannot further increase the bounded              ence shows that synthesis computation time is not negligible
integer. An engineer intended to fix this problem by adding                but at the same time not necessarily the main challenge for
the guarantee G (loadedPackages = 3 -> !load).                             engineers’ effective use of reactive synthesis. In our four
However, this intended fix does not work17 : Although it                   project classes, the students used their own ordinary laptop
uses the confusing operator G, the guarantee is an assertion               computers for synthesis, from within Eclipse. While we did
over current and next state, and so a transition to a state                not systematically collect synthesis performance data, we
with loadedPackages = 3 and load is allowed. The                           have experienced synthesis times ranging from less than five
guarantee only asserts that such a state would not have any                seconds to up to a minute. We did not hear complaints or
possible successors (but at that point the environment already             much negative feedback from the students about the perfor-
had to violate its assumption).                                            mance of checking realizability or synthesizing a symbolic
                                                                           controller.
16 The size of the state-space is estimated based on the number of

Boolean variables after translation to the kernel, as we are not able to   18 See the report and discussion at https://github.com/Verifiable
enumerate the reachable states of controllers this size.                   Robotics/slugs/issues/5.
17 It works neither in the strict nor in the implication semantics of      19 For backward compatibility, we still allow the use of G, and interpret

GR(1) [10].                                                                it as the GR(1)-G.


                                                                                                                                       123
1578                                                                                                            S. Maoz, J. O. Ringert


    From the expressive power perspective, on the one hand,       dent implementation of related algorithms, e.g., for dealing
we have shown that the expressive power of GR(1) synthesis        with non-well-separation and unrealizability (core, counter-
is enough to support most LTL specification patterns [21,49].     strategy, JVTS, repair), see Sect. 5.1. We continue to take
On the other hand, our experience shows that writing specifi-     advantage of this flexibility for additional new analyses that
cations is difficult and using more expressive languages, e.g.,   we are currently developing.
full LTL, with nested temporal operators, might anyways be           Finally, note that while we have implemented our own
very challenging for engineers. Thus, the expressive power        synthesizer, we did not start the implementation from noth-
of GR(1) seems well suited for our purpose.                       ing. Our implementation started from infrastructure provided
    Still, we have work in progress toward enriching Spec-        by JTLV [67]. Moreover, we did not implement our own
tra with additional language constructs and expressiveness,       BDD library but rely on existing ones. Currently, the user of
beyond LTL. As an example, we have work in progress on            Spectra Tools can choose between (our own slightly modi-
adding regular expressions and a variant of the rich triggers     fied versions of) CUDD [72] library and JTLV’s pure Java
operator of PSL [23]. As another example, we have work in         library.
progress on adding a quantitative aspect to Spectra synthesis
using the notion of energy, which corresponds with the accu-      7.6 Decision to make Spectra domain agnostic
mulation and consumption of a finite resource such as power
or memory. There, synthesis becomes the problem of gener-         Another design decision we have made early on was to
ating an implementation that not only meets the pure GR(1)        define Spectra as a general purpose specification language,
specification but also guarantees that the resource is never      not limited or tied to a specific application domain of reactive
over consumed, if such an implementation exists. Finally,         systems. Thus, we kept the language and the analyses domain
on this front of enriching Spectra, we have recently pre-         agnostic, completely separated from the application-specific
sented GR(1)* [3], a fragment of CTL* that extends GR(1)          implementation required for the execution of the synthesized
with existential guarantees that are not expressible in LTL.      controller in specific environments.
Importantly, yet, in comparison to GR(1), GR(1)* remains             We have already taken advantage of this separation, in
efficient, and induces only a minor additional cost in terms      that we have implemented two independent execution envi-
of time complexity, proportional to the extended length of        ronments, for Lego NXT robots and for stand-alone Java
the formula.                                                      applications, as demonstrated in the SYNTECH collections.
                                                                  Thanks to this separation and based on our experience, we
7.5 Implementing our own synthesizer                              expect that in the future one can relatively easily extend the
                                                                  execution end of Spectra Tools to additional domains and
Given the above fundamental choice to use GR(1) as a kernel       execution environments.
for Spectra, one may suggest that we could have implemented
Spectra Tools on top of an existing GR(1) synthesizer. Indeed,    7.7 The SYNTECH collections as benchmarks
several open-source GR(1) synthesizers are available, e.g.,
RATSY [6] and Slugs [22]. Why should we make the invest-          Finally, in Sect. 6 we gave an overview of the four SYNTECH
ment and implement yet another one?                               collections of Spectra specifications. We described how we
   The decision to implement our own new synthesizer was          obtained these collections, and presented an overview of the
due to two main reasons. The first reason is performance.         specifications and various metrics in Table 1, such as the
Our early experience showed that existing synthesizers (then,     number of assumptions and guarantees in each specification,
only RATSY), may not give us the performance required             etc. Finally, we have also discussed their quality character-
for the size of specifications we aimed to handle. Building       istics, their strengths and weaknesses. All these are relevant
our own synthesizer allowed us to optimize the code, use          when considering the use of these collections as benchmarks.
encoding inspired by Bartzis and Bultan [4] for arithmetic            Sim et al. [71] formulated a theory of benchmarking
operations, and further integrate performance heuristics at the   within scientific disciplines and challenge software engi-
BDD level as well as at the fixed-point algorithms level [28].    neering research to become more scientific and cohesive
As we show in [28], these proved to be very effective in          by working as a community to define benchmarks. To date,
improving the performance of GR(1) realizability checking         benchmark specifications for GR(1) synthesis have been very
compared to RATSY and Slugs, specifically for large speci-        limited. Most if not all works used only a handful of specifi-
fications.                                                        cations, mainly the ARM AMBA AHB Arbiter (AMBA) [8]
   The second reason is flexibility in developing analyses        and a Generalized Buffer from an IBM tutorial (GenBuf) [9],
beyond realizability checking and synthesis. Implementing         which were created by researchers for the specific purpose
our own synthesizer allowed us the complete flexibility           of evaluating the performance of GR(1) synthesis tools.
to choose an architecture that will enable the indepen-           One advantage of these two specifications, is that they are


123
Spectra: a specification language for reactive systems                                                                       1579


parametric. This makes them suitable for evaluating scala-            Property Specification Language (PSL) [23] is an exten-
bility. They are, however, very systematic and very carefully     sion of LTL with many operators that were introduced to
designed. They may not adequately represent specifications        help engineers write specifications more concisely. PSL has
that engineers may write in practice.                             become an IEEE standard in 2005. While the expressiveness
   We made Spectra versions of AMBA and GenBuf, as well           of PSL extends the one of LTL (and GR(1)), we believe that
as of additional parametric specifications of some classic        some of its language constructs, e.g., the trigger operator, are
problems (e.g., Towers of Hanoi, Dining Philosophers, Cin-        interesting language features with which to extend Spectra
derella and her stepmother) available on the Spectra website.     in the future. The main use of PSL specifications is verifica-
Since all are parametric, they are indeed suitable for evalu-     tion of reactive systems. PSL has been suggested for reactive
ating scalability, but, as argued above, may not adequately       synthesis in [8], with a case study of synthesizing an AMBA
represent specifications that engineers may write in practice.    AHB bus controller. Importantly, however, despite its title,
   As described in Sect. 6, the SYNTECH specifications are        the PSL language constructs appearing in [8] are limited to
different. In this sense, we believe they provide new valuable    those directly expressible in GR(1), and it is unclear whether
benchmarks for reactive synthesis related research. Indeed,       their translation has been automated. Moreover, support for
we have already used SYNTECH15 and SYNTECH17 as                   the trigger operator is not discussed in [8]. PSL includes nei-
benchmarks to examine the motivation for and the efficiency       ther a distinction between environment and system variables,
and effectiveness of various analyses, e.g., [28,43,51,53].       nor any operators similar to Spectra’s advanced constructs of
Others have also already used them, e.g., [14,59]. As we          monitors, patterns, and counters.
make these collections publicly available, we hope they will          SMV is the input language of the NuSMV tool [15] for
serve to advance reactive synthesis research and its future       symbolic model-checking [13]. The SMV language consists
use in practice.                                                  of a part for declaratively describing finite-state machines
                                                                  from variables and transitions, and of another part for spec-
                                                                  ifications written in LTL or CTL. SMV has influenced the
                                                                  input languages of JTLV [67] and the design of Spectra.
8 Related work
                                                                  The declaration of variables, types, and definitions in Spec-
                                                                  tra is similar to that of SMV. A major difference between
We review work related to Spectra and Spectra Tools from
                                                                  Spectra and SMV is, however, Spectra’s built-in distinction
different perspectives. First, we discuss related specification
                                                                  between environment and system variables. In addition, the
languages. Second, we discuss GR(1) specification lan-
                                                                  advanced language constructs of parametric predicates, mon-
guages and synthesis tools.
                                                                  itors, patterns, counters, and quantified arrays are also unique
                                                                  to Spectra.
8.1 Related specification languages                                   TLA+ [45] (Temporal Logic of Actions) is a versatile
                                                                  specification language for software systems. TLA+ includes
A number of logics and languages exist for the specifica-         language constructs for the structural definition of closed
tion of reactive systems. Most fundamental, linear temporal       and open (reactive) systems. Behavior in TLA+ can be
logic (LTL) [65], a modal temporal logic with modalities          specified using temporal operators. Analyses of TLA+ spec-
referring to time, was introduced for the specification of        ifications are supported by the TLC model-checker [78]. The
reactive behavior and is probably the most commonly used          TLA+ language is too expressive for model-checking to be
specification language for model-checking today. The time         fully automated and only subsets of the language are sup-
complexity of synthesis from LTL is double-exponential in         ported. TLA+ has been successfully applied in industrial
the length of the formula [66]. Nevertheless, some tools pro-     settings [61]. We believe that in the future, Spectra could ben-
vide implementations of LTL synthesis (see an overview            efit from composition mechanisms for specifications, similar
in [34]). These tools either suffer from scalability problems     to the ones provided by TLA+ .
or provide only bounded solutions. We are not aware of any            The Temporal Logic Synthesis Format (TLSF) [35] has
larger LTL specifications successfully used for reactive syn-     been designed as a high-level description language for LTL
thesis. Spectra is based on GR(1), a fragment of LTL with         synthesis problems. TLSF is used as an exchange format
more efficient synthesis algorithms. When teaching Spectra        for LTL specifications in the SYNTCOMP competition [34].
to the undergraduate students who participated in our four        TLSF is not specific to GR(1) and incorporates some fea-
project classes, we have deliberately avoided teaching LTL,       tures similar to the ones of PSL [23] for quantification and
so that the students use Spectra based on the intuitions of       parametrization for the purpose of compact expression of
always and alwaysEventually, instead of the some-                 repetitive constraints. TLSF does not provide advanced lan-
times complicated semantics of LTL formulas with nested           guage features like monitors, counters, or patterns. To the
temporal operators.                                               best of our knowledge, existing specifications written in


                                                                                                                       123
1580                                                                                                            S. Maoz, J. O. Ringert


TLSF have been translated from other languages and thus           and environment communicate via a single event per step,
the experience of developing specifications directly in TLSF      instead of by assigning values to multiple variables. MTSA
is limited.                                                       has been extended with a check for non-well-separation:
                                                                  D’Ippolito et al. [18] (indirectly) refer to non-well-separation
8.2 Related GR(1) specification languages and tools               by characterizing the possible controllers that force assump-
                                                                  tion violations as anomalous. To the best of our knowledge,
A number of specification languages and tools for reactive        non-well-separation is only checked but unlike in Spectra
synthesis have been developed on top of GR(1).                    Tools, no additional well-separation analyses (strategies or
    ApsectLTL [54] is an aspect-oriented specification lan-       cores as in [51], see Sect. 5.6), are provided by MTSA.
guage for reactive synthesis where specifications consist         Moreover, to the best of our knowledge, analyses related
of a base and a set of aspects. An AspectLTL base con-            to unrealizability have not been applied to SGR(1), unlike
sists of variable declarations and guarantees. AspectLTL          Spectra Tools, which provides various means to deal with
aspects define new variables and advice in terms of addi-         unrealizable specifications, see Sect. 5.5. Finally, synthesis of
tional guarantees over variables of aspects and the base. The     SGR(1) follows a concrete rather than a symbolic algorithm,
AspectLTL language provides support for bounded integers,         and has been applied only to very small example systems
arrays, enumeration types, defines, and PastLTL. However, it      designed by the authors of [12,17].
lacks support for assumptions and does not include advanced           Slugs (SmalL bUt Complete GROne Synthesizer) [22] is
language features like monitors, patterns, parametrized pred-     an implementation and extensible tool for GR(1) synthesis.
icates, and counters. AspectLTL comes with rich Eclipse           Slugs comes with plug-ins that implement analyses of unre-
editors and tools for debugging and tracing of specifica-         alizability [68], synthesis for weighted specifications [36],
tions [56]. The available body of AspectLTL specifications        and various modifications of the original GR(1) algorithm
is limited to small examples created by the authors. It might     (see Sect. 3 in [22]). The input format of Slugs is limited
be interesting to consider an aspect language based on Spec-      to Boolean variables and GR(1) constraints. Note that the
tra. However, this would require the identification of suitable   input of Slugs corresponds to the Spectra kernel, and thus
pointcuts for the new language constructs.                        it does not include advanced constructs corresponding to
    LTLMop (Linear Temporal Logic MissiOn Planning) [27]          Spectra’s monitors, parametrized predicates, counters, etc.
is a software for specifying and synthesizing robot missions      Structured Slugs is an alternative format that provides support
on 2D maps. The tool comes with a graphical map editor and        for bounded non-negative integers with comparison and addi-
allows specifications to be expressed in the GR(1) subset of      tion. In contrast, Spectra supports bounded integers (not only
LTL or structured English [37]. LTLMop supports different         non-negative) with more arithmetic operations, including
GR(1) synthesizers (including JTLV [67] and Slugs [22]) and       addition, subtraction, multiplication, division, and modulo
various output formats of synthesized controllers with sup-       (see Sect. 4.1). Structured Slugs can automatically be trans-
port for deployment on the ROS middleware [75]. The tool          lated to Slugs input format. Note, however, that the arithmetic
supports various analyses of unrealizable specifications [68].    translation from Structured Slugs to Slugs input is done at the
Some specifications created by the authors are available for      syntax level, while our translation in Spectra is implemented
examples presented in LTLMop’s research papers. Compared          at the BDD level with potential performance benefits related
to Spectra, LTLMop has a very specialized focus for mission       to variable order [4]. Slugs has been used as a platform for
planning on a 2D map. To the best of our knowledge, the           various research papers. However, we are not aware of doc-
specification language does not provide advanced language         umented experience of using Slugs for synthesis except for
features beyond those contained in the Spectra kernel.            small examples in research papers. Finally, in [28], the per-
    A version of the Modal Transition System Analyzer             formance of realizability checking in Slugs is systematically
(MTSA) [19] has been extended with synthesis for SGR(1)           compared against the performance of realizability checking
[12,17], which is a variant of GR(1) that is specialized to       in Spectra, using two well-known families of specifications
the context of event-based models. MTSA models systems            from the literature. The comparison shows that Spectra, with
as Finite State Processes (FSP), a language for the composi-      all the heuristics of [28] employed, outperforms Slugs on
tional definition of Labeled Transition Systems (LTS) [19],       large specifications. While for small specifications Slugs run-
and expresses specifications in Fluent Linear Temporal Logic      ning times for realizability checking are better than Spectra’s,
(FLTL) [30]. An SGR(1) synthesis problem consists of an           the larger the specification, the faster Spectra becomes rela-
LTS modeled in FSP, and justice assumptions and guarantees        tive to Slugs.
specified as assertions over fluents [17]. A major difference         Open Promela [25] is a multi-paradigm specification lan-
between MTSA and SGR(1), and all other GR(1) languages            guage for synthesis defined as an extension of the syntax
and tools that we review in this section, including Spectra,      of Promela. The semantics of Open Promela is different
is that MTSA and SGR(1) are event-based, i.e., the system         from Promela and is defined by a translation to GR(1).


123
Spectra: a specification language for reactive systems                                                                                 1581


The term “multi-paradigm” refers to the mix of imperative                performance of realizability checking in RATSY is system-
and declarative language elements. In addition to declara-               atically compared against the performance of realizability
tive assertions, the language introduces imperative variables            checking in Spectra, using two well-known families of spec-
and processes. Intuitively, the value of an imperative variable          ifications from the literature. The comparison shows that
remains unchanged unless it appears in an assignment. Pro-               Spectra, with all the heuristics of [28] employed, outperforms
cesses control assignments to variables, e.g., for describing            RATSY on large specifications. While for small specifica-
possible transitions. Synthesis from Open Promela speci-                 tions, RATSY running times for realizability checking are
fications is supported by a translation to the input format              better than Spectra’s, the larger the specification, the faster
of Slugs [22]. Imperative language elements are expressed                Spectra becomes relative to RATSY (similarly to Slugs, see
by adding constraints to variables. The language of Open                 above).
Promela is demonstrated on a variant of the GR(1) AMBA                       Finally, some scenario-based specification languages and
specification [8]. We are not aware of tools for analyzing               tools, as well as event-based modeling tools, make use of a
Open Promela specifications, their unrealizability, or their             translation to GR(1) or variants thereof. These include, e.g.,
non-well-separation. To the best of our knowledge, the body              PlayGo [32], which uses the translation described in [55],
of available Open Promela specifications is limited to few               ScenarioTools [31], and SGR(1) [18] (discussed above).
examples.                                                                Some of these use a visual language while others use a tex-
   Tulip [24,76] is a toolbox for the synthesis of hybrid sys-           tual language. Some of these provide tools for execution
tems. It combines GR(1) synthesis with automated abstrac-                and debugging. None includes support for language features
tions of continuous dynamics. The syntax of Tulip expres-                such as Spectra’s monitors, parametrized predicates, quanti-
sions and operators is inspired by TLA+ [45] while speci-                fied arrays, patterns, and counters. It may be interesting to
fications appear to be built programmatically.20 We are not              extend Spectra with an event-based idiom and scenario-like
aware of Tulip’s support beyond synthesis itself, for analyz-            language constructs.
ing specifications, unrealizability, or non-well-separation. Its
input language does not include advanced constructs similar
to Spectra’s monitors, counters, and patterns. To the best of            9 Conclusion and future work
our knowledge, the collected experience of writing specifi-
cations in Tulip is limited to few examples.                             The definition and development of Spectra and Spectra Tools
   RATSY [6] has been developed as a requirement analysis                are part of the SYNTECH project,22 which aims at bridging
tool that includes GR(1) synthesis. The tool has a graphical             the gap between the theory and algorithms of reactive synthe-
user interface to draw Buchi automata that serve as GR(1)                sis, on the one hand, and software engineering practice, on
assumptions or guarantees. Execution traces are visualized               the other. We use the language and tool set to learn about the
and RATSY implements algorithms for exploring counter-                   challenges in bridging this gap and to develop and evaluate
strategies in case of unrealizability [39]. RATSY does not               possible means to address them. An overview of the SYN-
support constructs similar to Spectra’s advanced language                TECH project was recently presented in an invited keynote
constructs such as monitors, patterns, and counters. Inter-              by the first listed author at FormaliSE’20.23
estingly, RATSY’s user-manual presents an example of how                    In this paper we presented the Spectra language. Spec-
to use RATSY to specify a bounded counter, by listing the                tra provides means to specify assumptions and guarantees
different (safety) requirements one needs to specify.21 One              for a reactive system, using high-level constructs such as
may contrast this with the simplicity of Spectra’s counter               patterns, monitors, and counters. We further presented an
construct, which hides the complexity and encapsulates the               overview of Spectra Tools, a set of analyses and tools provid-
concept of counting into a single specification element. The             ing synthesis into correct-by-construction controllers, means
focus of RATSY on requirements and its graphical user                    to execute and simulate the synthesized controllers, and
interface differs from that of Spectra where the syntax of               additional analyses aimed at helping engineers write higher-
specifications is text-based. However, we believe that some              quality specifications. Finally, we presented statistics and
analyses may benefit from visualizations of transition sys-              observations based on four collections of specifications and
tems and we have integrated some of these into Spectra                   on our early experience with Spectra.
Tools, specifically visualizing both concrete and symbolic                  We consider future work on different fronts. First, on
representations of counter-strategies [43]. Finally, in [28], the        the language front, we are working on enriching Spectra
                                                                         with additional language constructs, e.g., powerful temporal
20 See examples available from https://github.com/tulip-control/tulip-

control/tree/master/examples.                                            22 SYNTECH: http://smlab.cs.tau.ac.il/syntech/.

21 http://rat.fbk.eu/ratsy/uploads/Main/RatsyManual_v2.1.pdf, down-      23 FormaliSE’20    keynote   about   SYNTECH:     https://youtu.be/
loaded July 2019, pages 9 to 13.                                         ig8_PbkGito.


                                                                                                                               123
1582                                                                                                                       S. Maoz, J. O. Ringert


constructs, such as the triggers operator of PSL [23]. We fur-              A Spectra grammar
ther consider the development of additional pattern libraries,
beyond the one covering the patterns of Dwyer et al., which                 We show a combination of the grammars of the Spectra kernel
already comes with the language. For example, a set of spec-                from Fig. 4 and of all extensions from Sect. 4 in Fig. 15. As
ification patterns for robotic missions was presented in [59];              mentioned in Sect. 2.3, this grammar includes simplifications
we have work in progress on adding a library of these patterns              for readability and in order to fit it on a single page.
to Spectra.                                                                    Spectra provides more verbose alternative to most key-
    Second, on the tools front, we have work in progress on                 words shown in Table 2. We have decided to use the shorter
an improved simulation, testing, and debugging environment                  keywords in Sects. 3 and 4 as they seem to be preferred when
for the synthesized controller. This includes, for example,                 writing specifications.
the ability to set breakpoints using propositions, to check
whether a state that satisfies a certain proposition is reachable
from the current state, etc.                                                B Complete extended example
    Third, on the application domain front, we are looking to
expand to other domains beyond autonomous Lego robots                       Listing 12 shows our initial example from Lst. 1 and all its
and the example systems we had so far. We are specifically                  extensions mentioned in Sect. 4. The extensions include enu-
examining case studies in the medical devices and network                   merations and integer variables from Lst. 2, the define and its
protocols domains, together with two industry partner com-                  use from Lst. 3, state invariants as described in Sect. 4.3, the
panies.                                                                     PastLTL example from Sect. 4.4, the predicate from Lst. 5,
    Finally, we are looking into performing broader and more                the monitor from Lst. 6, the counter from Lst. 7, the pattern
systematic evaluations of Spectra and Spectra Tools. We have                instances from Lst. 9, and an import as described in Sect. 4.10
already shared it with colleagues in other universities who                 to import the pattern definition shown in Lst. 8.
may use it in teaching. We have also shared it with potential                  The lines of the different listings are rearranged in Lst. 12
industrial collaborators. To broaden the evaluation, we plan                to define all system and environment variables at the top of
to collect data about the experience in using Spectra in addi-              the specification. The body of the define from Lst. 3 has been
tional application domains. To make it more systematic, we                  extended to include variable ambulanceMain. With this
will consider controlled experiments where, for example, dif-               inclusion the complete specification as shown in Lst. 12 is
ferent teams of students are instructed to do the same project              realizable.
with and without the availability of specific language con-
structs or analyses. We hope all these will generate additional
                                                                            Table 2 Overview of Spectra keywords that have more verbose alter-
data and insights into the potential applicability of reactive              natives (in alphabetical order)
synthesis to software engineering.
                                                                            Keyword                                         Alternative
Acknowledgements We thank the 67 undergraduate students who par-
                                                                            alw                                             always
ticipated in our four project classes. We thank Elizabeth Firman, Aviv
Kuvent, Or Pistiner, Rafi Shalom, Ilia Shevrin, Keren Solodkin, and         alwEv                                           alwaysEventually
Yoni Wolbe for their contribution to the implementation of Spectra          asm                                             assumption
Tools.                                                                      env                                             input
    This project has received funding from the European Research
Council (ERC) under the European Union’s Horizon 2020 research              gar                                             guarantee
and innovation program (grant agreement No 638049, SYNTECH).                H                                               HISTORICALLY
                                                                            ini                                             initially
Open Access This article is licensed under a Creative Commons
Attribution 4.0 International License, which permits use, sharing, adap-    O                                               ONCE
tation, distribution and reproduction in any medium or format, as           S                                               SINCE
long as you give appropriate credit to the original author(s) and the       sys                                             output
source, provide a link to the Creative Commons licence, and indi-
                                                                            Y                                               PREV
cate if changes were made. The images or other third party material
in this article are included in the article’s Creative Commons licence,
unless indicated otherwise in a credit line to the material. If material
is not included in the article’s Creative Commons licence and your
intended use is not permitted by statutory regulation or exceeds the
permitted use, you will need to obtain permission directly from the copy-
right holder. To view a copy of this licence, visit http://creativecomm
ons.org/licenses/by/4.0/.




123
Spectra: a specification language for reactive systems                                                                                           1583


                                                                                                                                          Spectra
                                                                       1   import " DwyerPatterns . spectra "
                                                                       2   spec T r a f f i c L i g h t
                                                                       3
                                                                       4   env    boolean carMain ;
                                                                       5   env    boolean carSide ;
                                                                       6   env    Int ( 0 . . 1 0 ) c a r s M a i n ;
                                                                       7   env    Int ( 0 . . 6 ) c a r s S i d e ;
                                                                       8   env    boolean pedestrianBtn ;
                                                                       9   env    boolean ambulanceMain ;
                                                                      10
                                                                      11   sys    { MAIN , SIDE , NONE } go ;
                                                                      12   sys    boolean greenMain ;
                                                                      13   sys    boolean greenSide ;
                                                                      14   sys    boolean greenPedestrian ;
                                                                      15
                                                                      16   p r e d i c a t e excl ( b o o l e a n p , b o o l e a n q ) :
                                                                      17       !( p & q ) ;
                                                                      18
                                                                      19   gar alw excl ( greenMain , g r e e n S i d e ) &
                                                                      20           excl ( g r e e n P e d e s t r i a n , g r e e n S i d e ) ;
                                                                      21
                                                                      22   d e f i n e s t r e e t s E m p t y :=
                                                                      23       ! carSide & ! carMain & ! ambulanceMain ;
                                                                      24
                                                                      25   asm    ini s t r e e t s E m p t y ;
                                                                      26   asm    ini c a r S i d e = f a l s e & c a r M a i n = f a l s e ;
                                                                      27   asm    alwEv carSide ;
                                                                      28   asm    alwEv carMain ;
                                                                      29   asm    alwEv ONCE c a r S i d e ;
                                                                      30
                                                                      31   gar ini go = NONE ;
                                                                      32   gar alw c a r s M a i n >= c a r s S i d e i m p l i e s
                                                                      33           next ( go = MAIN ) ;
                                                                      34   gar alw c a r s S i d e > c a r s M a i n i m p l i e s
                                                                      35           next ( go = SIDE ) ;
                                                                      36   gar alw s t r e e t s E m p t y i m p l i e s
                                                                      37           ! greenMain & ! greenSide ;
                                                                      38   gar alw !( g r e e n M a i n & g r e e n S i d e ) ;
                                                                      39   gar a l w E v c a r S i d e & g r e e n S i d e ;
                                                                      40   gar a l w E v c a r M a i n & g r e e n M a i n ;
                                                                      41
                                                                      42   monitor boolean needGreenMain {
                                                                      43     ini n e e d G r e e n M a i n =
                                                                      44         ( pedestrianBtn & ! greenPedestrian );
                                                                      45     t r a n s next ( n e e d G r e e n M a i n ) =
                                                                      46         (( n e e d G r e e n M a i n | p e d e s t r i a n B t n ) &
                                                                      47                                       ! greenPedestrian );
                                                                      48   }
                                                                      49   gar a l w E v ! n e e d G r e e n M a i n ;
                                                                      50
                                                                      51   counter ambulanceWait (0..5) {
                                                                      52     inc : a m b u l a n c e M a i n & ! g r e e n M a i n ;
                                                                      53     reset : greenMain ;
                                                                      54     o v e r f l o w : keep ;
                                                                      55   }
                                                                      56   gar alw a m b u l a n c e W a i t < 5;
                                                                      57
                                                                      58   gar p R e s p o n d s T o S ( c a r M a i n , g r e e n M a i n ) ;
                                                                      59   gar p R e s p o n d s T o S ( c a r S i d e , g r e e n S i d e ) ;

                                                                      Listing 12 The example from Lst. 1 with all extensions from Sect. 4.
Fig. 15 Grammar of Spectra including the Spectra kernel from Fig. 4
and all extensions from Sect. 4




                                                                                                                                        123
1584                                                                                                                           S. Maoz, J. O. Ringert


References                                                                 14. Cavezza, D.G., Alrajeh, D., György, A.: Minimal assumptions
                                                                               refinement for GR(1) specifications. CoRR, arXiv:1910.05558
 1. 2013 IEEE/RSJ International Conference on Intelligent Robots and           (2019)
    Systems, Tokyo, Japan, November 3–7, 2013, IEEE (2013)                 15. Cimatti, A., Clarke, E.M., Giunchiglia, E., Giunchiglia, F., Pistore,
 2. Almagor, S., Kupferman, O., Ringert, J.O., Velner, Y.: Quanti-             M., Roveri, M., Sebastiani, R., Tacchella, A.: NuSMV 2: An Open-
    tative assume guarantee synthesis. In: Majumdar, R., Kuncak,               Source Tool for Symbolic Model Checking. In: CAV, volume 2404
    V. (eds.) Computer Aided Verification—29th International Con-              of LNCS, pp. 359–364. Springer (2002)
    ference, CAV 2017, Heidelberg, Germany, July 24–28, 2017,              16. David, A., Jensen, P.G., Larsen, K.G., Mikucionis, M., Taankvist,
    Proceedings, Part II, volume 10427 of Lecture Notes in Computer            J.H.: Uppaal stratego. In: Baier, C., Tinelli, C. (eds.) Tools and
    Science, pp. 353–374, Springer (2017)                                      Algorithms for the Construction and Analysis of Systems - 21st
 3. Amram, G., Maoz, S., Pistiner, O.: GR(1)*: GR(1) specifications            International Conference, TACAS 2015, Held as Part of the Euro-
    extended with existential guarantees. In: ter Beek, M.H., McIver,          pean Joint Conferences on Theory and Practice of Software, ETAPS
    A., Oliveira, J.N. (eds.) Formal Methods—The Next 30 Years—                2015, London, UK, April 11–18, 2015. Proceedings, volume 9035
    Third World Congress, FM 2019, Porto, Portugal, October 7–11,              of Lecture Notes in Computer Science, pp. 206–211. Springer
    2019, Proceedings, volume 11800 of Lecture Notes in Computer               (2015)
    Science, pp. 83–100, Springer (2019)                                   17. D’Ippolito, N., Braberman, V.A., Piterman, N., Uchitel, S.: Syn-
 4. Bartzis, C., Bultan, T.: Efficient BDDs for bounded arithmetic con-        thesis of live behaviour models for fallible domains. In: ICSE, pp.
    straints. STTT 8(1), 26–36 (2006)                                          211–220 (2011)
 5. Bloem, R., Chatterjee, K., Henzinger, T.A., Jobstmann, B.: Better      18. D’Ippolito, N., Braberman, V.A., Piterman, N., Uchitel, S.: Syn-
    quality in synthesis through quantitative objectives. In: Bouajjani,       thesizing nonanomalous event-based controllers for liveness goals.
    A., Maler, O., (eds.) Computer Aided Verification, 21st Interna-           ACM Trans. Softw. Eng. Methodol. 22(1), 9 (2013)
    tional Conference, CAV 2009, Grenoble, France, June 26–July 2,         19. D’Ippolito, N., Fischbein, D., Chechik, M., Uchitel, S.: MTSA:
    2009. Proceedings, volume 5643 of Lecture Notes in Computer                the modal transition system analyser. In: 23rd IEEE/ACM Inter-
    Science, pp. 140–156. Springer (2009)                                      national Conference on Automated Software Engineering (ASE
 6. Bloem, R., Cimatti, A., Greimel, K., Hofferek, G., Könighofer, R.,         2008), 15–19 September 2008, L’Aquila, Italy, pp. 475–476. IEEE
    Roveri, M., Schuppan, V., Seeber, R.: RATSY—a new requirements             Computer Society (2008)
    analysis tool with synthesis. In: CAV, volume 6174 of LNCS, pp.        20. Dräger, K., Forejt, V., Kwiatkowska, M.Z., Parker, D., Ujma,
    425–429. Springer (2010)                                                   M.: Permissive controller synthesis for probabilistic systems. In:
 7. Bloem, R., Ehlers, R., Könighofer, R.: Cooperative reactive syn-           TACAS, volume 8413 of LNCS, pp. 531–546. Springer (2014)
    thesis. In: Finkbeiner, B., Pu, G., Zhang, L. (eds.) Automated         21. Dwyer, M.B., Avrunin, G.S., Corbett, J.C.: Patterns in property
    Technology for Verification and Analysis—13th International                specifications for finite-state verification. In: ICSE, pp. 411–420.
    Symposium, ATVA 2015, Shanghai, China, October 12–15, 2015,                ACM (1999)
    Proceedings, volume 9364 of Lecture Notes in Computer Science,         22. Ehlers, R., Raman, V.: Slugs: Extensible GR(1) synthesis. In: CAV,
    pp. 394–410. Springer (2015)                                               volume 9780 of LNCS, pp. 333–339. Springer (2016)
 8. Bloem, R., Galler, S.J., Jobstmann, B., Piterman, N., Pnueli,          23. Eisner, C., Fisman, D.: A Practical Introduction to PSL. Springer,
    A., Weiglhofer, M.: Interactive presentation: Automatic hardware           Series on Integrated Circuits and Systems (2006)
    synthesis from specifications: a case study. In: Lauwereins, R.,       24. Filippidis, I., Dathathri, S., Livingston, S.C., Ozay, N., Murray,
    Madsen, J. (eds.) 2007 Design. Automation and Test in Europe               R.M.: Control design for hybrid systems with tulip: the tempo-
    Conference and Exposition, DATE 2007, Nice, France, April 16–              ral logic planning toolbox. In: 2016 IEEE Conference on Control
    20, 2007, pp. 1188–1193. EDA Consortium, San Jose, CA, USA                 Applications, CCA 2016, Buenos Aires, Argentina, September 19–
    (2007)                                                                     22, 2016, pp. 1030–1041. IEEE (2016)
 9. Bloem, R., Galler, S.J., Jobstmann, B., Piterman, N., Pnueli, A.,      25. Filippidis, I., Murray, R.M., Holzmann, G.J.: A multi-paradigm
    Weiglhofer, M.: Specify, compile, run: hardware from PSL. Electr.          language for reactive synthesis. In: P. Cerný, V. Kuncak, and P.
    Notes Theor. Comput. Sci. 190(4), 3–16 (2007)                              Madhusudan, editors, Proceedings Fourth Workshop on Synthesis,
10. Bloem, R., Jobstmann, B., Piterman, N., Pnueli, A., Sa’ar, Y.: Syn-        SYNT 2015, San Francisco, CA, USA, 18th July 2015., volume
    thesis of Reactive(1) Designs. J. Comput. Syst. Sci. 78(3), 911–938        202 of EPTCS, pp. 73–97 (2015)
    (2012)                                                                 26. Finkbeiner, B., Schewe, S.: Bounded synthesis. STTT 15(5–6),
11. Bohy, A., Bruyère, V., Filiot, E., Raskin, J.: Synthesis from              519–539 (2013)
    LTL specifications with mean-payoff objectives. In: Piterman, N.,      27. Finucane, C., Jing, G., Kress-Gazit, H.: Ltlmop: Experimenting
    Smolka, S.A. (eds.) Tools and Algorithms for the Construction              with language, temporal logic and robot control. In: 2010 IEEE/RSJ
    and Analysis of Systems—19th International Conference, TACAS               International Conference on Intelligent Robots and Systems, Octo-
    2013, Held as Part of the European Joint Conferences on Theory             ber 18–22, 2010, Taipei, Taiwan, pp. 1988–1993. IEEE (2010)
    and Practice of Software, ETAPS 2013, Rome, Italy, March 16–           28. Firman, E., Maoz, S., Ringert, J.O.: Performance heuristics for
    24, 2013. Proceedings, volume 7795 of Lecture Notes in Computer            GR(1) synthesis and related algorithms. Acta Inform. 57(1–2), 37–
    Science, pp. 169–184. Springer (2013)                                      79 (2020)
12. Braberman, V.A., D’Ippolito, N., Piterman, N., Sykes, D., Uchitel,     29. Gabbay, D.M.: The declarative past and imperative future: Exe-
    S.: Controller synthesis: from modelling to enactment. In: Notkin,         cutable temporal logic for interactive systems. In: Banieqbal, B.,
    D., Cheng, B.H.C., Pohl, K. (eds.) 35th International Conference           Barringer, H., Pnueli, A. (eds.) Temporal Logic in Specification,
    on Software Engineering, ICSE ’13, San Francisco, CA, USA, May             Altrincham, UK, April 8–10, 1987, Proceedings, volume 398 of
    18–26, 2013, pp. 1347–1350. IEEE Computer Society (2013)                   Lecture Notes in Computer Science, pp. 409–448. Springer (1987)
13. Burch, J.R., Clarke, E.M., McMillan, K.L., Dill, D.L., Hwang, L.J.:    30. Giannakopoulou, D., Magee, J.: Fluent model checking for event-
    Symbolic model checking: 10ˆ20 states and beyond. In: Proceed-             based systems. In: Paakki, J., Inverardi, P., (eds.) Proceedings
    ings of the Fifth Annual Symposium on Logic in Computer Science            of the 11th ACM SIGSOFT Symposium on Foundations of
    (LICS ’90), Philadelphia, Pennsylvania, USA, June 4–7, 1990, pp.           Software Engineering 2003 held jointly with 9th European Soft-
    428–439. IEEE Computer Society (1990)                                      ware Engineering Conference, ESEC/FSE 2003, Helsinki, Finland,
                                                                               September 1–5, 2003, pp. 257–266. ACM (2003)


123
Spectra: a specification language for reactive systems                                                                                            1585


31. Greenyer, J., Gritzner, D., Gutjahr, T., König, F., Glade, N., Marron,       humanoid robot. In: Kragic, D., Bicchi, A., Luca, A.D. (eds.)
    A., Katz, G.: Scenariotools—a tool suite for the scenario-based              2016 IEEE International Conference on Robotics and Automation,
    modeling and analysis of reactive systems. Sci. Comput. Program.             ICRA 2016, Stockholm, Sweden, May 16–21, 2016, pp. 4192–
    149, 15–27 (2017)                                                            4199. IEEE (2016)
32. Harel, D., Maoz, S., Szekely, S., Barkan, D.: Playgo: towards a com-     48. Maoz, S., Pistiner, O., Ringert, J.O.: Symbolic BDD and ADD
    prehensive tool for scenario based programming. In: Pecheur, C.,             algorithms for energy games. In: Piskac and Dimitrova [62], pp.
    Andrews, J., Nitto, E.D. (eds.) ASE 2010, 25th IEEE/ACM Interna-             35–54
    tional Conference on Automated Software Engineering, Antwerp,            49. Maoz, S., Ringert, J.O.: GR(1) synthesis for LTL specification pat-
    Belgium, September 20–24, 2010, pp. 359–360. ACM (2010)                      terns. In: ESEC/FSE, pp. 96–106. ACM (2015)
33. Hölldobler, K., Rumpe, B.: MontiCore 5 Language Workbench                50. Maoz, S., Ringert, J.O.: Synthesizing a Lego Forklift Controller
    Edition 2017. Aachener Informatik-Berichte, Software Engineer-               in GR(1): A Case Study. In: Proceedings of the 4th Workshop on
    ing, Band 32. Shaker Verlag, December (2017)                                 Synthesis, SYNT 2015 colocated with CAV 2015, volume 202 of
34. Jacobs, S., Basset, N., Bloem, R., Brenguier, R., Colange, M., Fay-          EPTCS, pp. 58–72 (2015)
    monville, P., Finkbeiner, B., Khalimov, A., Klein, F., Michaud, T.,      51. Maoz, S., Ringert, J.O.: On well-separation of GR(1) specifica-
    Pérez, G.A., Raskin, J., Sankur, O., Tentrup, L.: The 4th reactive           tions. In: FSE, pp. 362–372. ACM (2016)
    synthesis competition (SYNTCOMP 2017): Benchmarks, partic-               52. Maoz, S., Ringert, J.O.: On the Software Engineering Challenges
    ipants & results. In: Fisman, D., Jacobs, S. (eds.) Proceedings              of Applying Reactive Synthesis to Robotics. In: Proceedings of the
    Sixth Workshop on Synthesis, SYNT@CAV 2017, Heidelberg,                      1st Int. Workshop on Robotics Software Engineering, RoSE 2018
    Germany, 22nd July 2017., volume 260 of EPTCS, pp. 116–143                   colocated with ICSE 2018 (2018)
    (2017)                                                                   53. Maoz, S., Ringert, J.O., Shalom, R.: Symbolic repairs for GR(1)
35. Jacobs, S., Klein, F., Schirmer, S.: A high-level LTL synthesis for-         specifications. In: Mussbacher, G., Atlee, J.M., Bultan, T. (eds.)
    mat: TLSF v1.1. In: Piskac and Dimitrova [62], pp. 112–132                   Proceedings of the 41st International Conference on Software Engi-
36. Jing, G., Ehlers, R., Kress-Gazit, H.: Shortcut through an evil              neering, ICSE 2019, Montreal, QC, Canada, May 25–31, 2019, pp.
    door: optimality of correct-by-construction controllers in adver-            1016–1026. IEEE/ACM (2019)
    sarial environments. In: 2013 IEEE/RSJ International Conference          54. Maoz, S., Sa’ar, Y.: AspectLTL: an aspect language for LTL spec-
    on Intelligent Robots and Systems, Tokyo, Japan, November 3–7,               ifications. In: AOSD, pp. 19–30. ACM (2011)
    [1], pp. 4796–4802 (2013)                                                55. Maoz, S., Sa’ar, Y.: Assume-guarantee scenarios: Semantics and
37. Jing, G., Finucane, C., Raman, V., Kress-Gazit, H.: Correct high-            synthesis. In: MODELS, volume 7590 of LNCS, pp. 335–351.
    level robot control from structured english. In: IEEE International          Springer (2012)
    Conference on Robotics and Automation, ICRA 2012, 14-18 May,             56. Maoz, S., Sa’ar, Y.: Two-way traceability and conflict debugging
    2012, St. Paul, Minnesota, USA, pp. 3543–3544. IEEE (2012)                   for aspectltl programs. Trans. Aspect-Oriented Softw. Dev. 10, 39–
38. Klein, U., Pnueli, A.: Revisiting synthesis of GR(1) specifications.         72 (2013)
    In: Haifa Verification Conference (HVC), volume 6504 of LNCS,            57. Maoz, S., Shalom, R.: Inherent vacuity for GR(1) specifications.
    pp. 161–181. Springer (2010)                                                 In: ESEC/FSE, pp. 99–110. ACM (2020)
39. Könighofer, R., Hofferek, G., Bloem, R.: Debugging formal spec-          58. Maoz, S., Shevrin, I.: Just-in-time reactive synthesis. In: ASE, pp.
    ifications: a practical approach using model-based diagnosis and             635–646. IEEE (2020)
    counterstrategies. STTT 15(5–6), 563–583 (2013)                          59. Menghi, C., Tsigkanos, C., Pelliccione, P., Ghezzi, C.,
40. Kress-Gazit, H., Fainekos, G.E., Pappas, G.J.: Temporal-logic-               Berger, T.: Specification patterns for robotic missions. CoRR,
    based reactive mission and motion planning. IEEE Trans. Robot.               arXiv:1901.02077 (2019)
    25(6), 1370–1381 (2009)                                                  60. Miyazawa, A., Ribeiro, P., Li, W., Cavalcanti, A., Timmis, J.,
41. Kupferman, O., Lustig, Y., Vardi, M.Y., Yannakakis, M.: Temporal             Woodcock, J.: Robochart: modelling and verification of the func-
    synthesis for bounded systems and environments. In: Schwentick,              tional behaviour of robotic applications. Softw. Syst. Model. 18(5),
    T., Dürr, C. (eds.) 28th International Symposium on Theoretical              3097–3149 (2019)
    Aspects of Computer Science, STACS 2011, March 10–12, 2011,              61. Newcombe, C., Rath, T., Zhang, F., Munteanu, B., Brooker, M.,
    Dortmund, Germany, volume 9 of LIPIcs, pp. 615–626. Schloss                  Deardeuff, M.: How amazon web services uses formal methods.
    Dagstuhl-Leibniz-Zentrum fuer Informatik (2011)                              Commun. ACM 58(4), 66–73 (2015)
42. Kupferman, O., Vardi, M.Y.: Synthesis of trigger properties. In:         62. Piskac, R., Dimitrova, R., (eds.): Proceedings Fifth Workshop on
    LPAR, volume 6355 of LNCS, pp. 312–331. Springer (2010)                      Synthesis, SYNT@CAV 2016, Toronto, Canada, July 17–18, 2016,
43. Kuvent, A., Maoz, S., Ringert, J.O.: A symbolic justice viola-               volume 229 of EPTCS (2016)
    tions transition system for unrealizable GR(1) specifications. In:       63. Piterman, N., Pnueli, A.: Faster solutions of rabin and streett games.
    Bodden, E., Schäfer, W., van Deursen, A., Zisman, A. (eds.),                 In: 21th IEEE Symposium on Logic in Computer Science (LICS
    Proceedings of the 2017 11th Joint Meeting on Foundations of                 2006), 12–15 August 2006, Seattle, WA, USA, Proceedings, pp.
    Software Engineering, ESEC/FSE 2017, Paderborn, Germany,                     275–284. IEEE Computer Society (2006)
    September 4–8, 2017, pp. 362–372. ACM (2017)                             64. Piterman, N., Pnueli, A., Sa’ar, Y.: Synthesis of reactive(1) designs.
44. Kwiatkowska, M.Z., Parker, D.: Automated verification and strat-             In: VMCAI, volume 3855 of LNCS, pp. 364–380. Springer (2006)
    egy synthesis for probabilistic systems. In: Hung D.V., Ogawa, M.        65. Pnueli, A.: The temporal logic of programs. In: 18th Annual Sym-
    (eds.), Automated Technology for Verification and Analysis—11th              posium on Foundations of Computer Science, Providence, Rhode
    International Symposium, ATVA 2013, Hanoi, Vietnam, October                  Island, USA, 31 October–1 November 1977, pp. 46–57. IEEE Com-
    15-18, 2013. Proceedings, volume 8172 of Lecture Notes in Com-               puter Society (1977)
    puter Science, pp. 5–22. Springer (2013)                                 66. Pnueli, A., Rosner, R.: On the Synthesis of a Reactive Module. In:
45. Lamport, L.: Specifying Systems. Addison–Wesley, The TLA+                    POPL, pp. 179–190. ACM Press (1989)
    Language and Tools for Hardware and Software Engineers (2002)            67. Pnueli, A., Sa’ar, Y., Zuck, L.D.: JTLV: a framework for developing
46. Lustig, Y., Vardi, M.Y.: Synthesis from component libraries. STTT            verification algorithms. In: CAV, volume 6174 of LNCS, pp. 171–
    15(5–6), 603–618 (2013)                                                      174. Springer (2010)
47. Maniatopoulos, S., Schillinger, P., Pong, V., Conner, D.C., Kress-       68. Raman, V.: Kress-Gazit, H.: Analyzing unsynthesizable specifi-
    Gazit, H.: Reactive high-level behavior synthesis for an atlas               cations for high-level robot behavior using ltlmop. In: Gopalakr-


                                                                                                                                          123
1586                                                                                                                           S. Maoz, J. O. Ringert


    ishnan G., Qadeer, S. (eds.) Computer Aided Verification—23rd                                               S. Maoz is an Associate Pro-
    International Conference, CAV 2011, Snowbird, UT, USA, July                                                 fessor at the School of Computer
    14–20, 2011. Proceedings, volume 6806 of Lecture Notes in Com-                                              Science in Tel Aviv University,
    puter Science, pp. 663–668. Springer (2011)                                                                 where he heads the Software Mod-
69. Ringert, J.O., Roth, A., Rumpe, B., Wortmann, A.: Language                                                  eling Laboratory. Shahar has BSc
    and code generator composition for model-driven engineering of                                              and MSc computer science degrees
    robotics component & connector systems. J. Softw. Eng. Robot. 6,                                            from Tel Aviv University, and a
    33–57 (2015)                                                                                                PhD from the Weizmann Insti-
70. Rozier, K.Y.: Specification: the biggest bottleneck in formal meth-                                         tute, Israel. From 2010 to 2012
    ods and autonomy. In: VSTTE, volume 9971 of LNCS, pp. 8–26                                                  he was a postdoc research fel-
    (2016)                                                                                                      low in RWTH Aachen University,
71. Sim, S.E., Easterbrook, S.M., Holt, R.C.: Using benchmarking to                                             Germany, with a fellowship from
    advance research: a challenge to software engineering. In: Clarke,                                          the Minerva Foundation. In 2015–
    L.A., Dillon, L., Tichy, W.F. (eds.) Proceedings of the 25th Inter-                                         2016, he spent a sabbatical at MIT
    national Conference on Software Engineering, May 3–10, 2003,                                                CSAIL. Shahar’s research inter-
    Portland, Oregon, USA, pp. 74–83. IEEE Computer Society (2003)          ests are in software engineering, specifically in the use of models and
72. Somenzi, F.: CUDD: BDD package, University of Colorado, Boul-           formal methods for software evolution, model inference, testing, and
    der. http://vlsi.colorado.edu/~fabio/CUDD/cudd.pdf                      synthesis. His work has been published in top software engineering
73. Spectra Website. http://smlab.cs.tau.ac.il/syntech/spectra/             and modeling conferences and journals. He has served multiple times
74. Walker, A., Ryzhyk, L.: Predicate abstraction for reactive synthesis.   on the program committees of ASE, ESEC/FSE, ICSE, and MoDELS
    In: Formal Methods in Computer-Aided Design, FMCAD 2014,                conferences, and will be PC co-Chair for ASE’22. He is a recipient of
    Lausanne, Switzerland, October 21–24, 2014, pp. 219–226. IEEE           an ERC Starting Grant for the development of synthesis technologies
    (2014)                                                                  (project SYNTECH: http://smlab.cs.tau.ac.il/syntech/).
75. Wong, K.W., Finucane, C., Kress-Gazit, H.: Provably-correct robot
    control with ltlmop, OMPL and ROS. In: 2013 IEEE/RSJ Interna-
    tional Conference on Intelligent Robots and Systems, Tokyo, Japan,                                         J. O. Ringert is a Lecturer at
    November 3–7 [1], p. 2073 (2013)                                                                           the School of Informatics at Uni-
76. Wongpiromsarn, T., Topcu, U., Ozay, N., Xu, H., Murray, R.M.:                                              versity of Leicester. Jan has a
    TuLiP: A Software Toolbox for Receding Horizon Temporal Logic                                              Diploma from Technical Univer-
    Planning. In: Proceedings of the 14th International Conference on                                          sity of Brunswick and a PhD from
    Hybrid Systems: Computation and Control, HSCC ’11, pp. 313–                                                RWTH Aachen University. From
    314. New York, NY, USA, ACM (2011)                                                                         2013 to 2015, he was a postdoc
77. Xtext. Xtext. https://www.eclipse.org/Xtext/                                                               research fellow in Tel Aviv Uni-
78. Yu, Y., Manolios, P., Lamport, L.: Model checking tla+ specifica-                                          versity, with a fellowship from the
    tions. In: L. Pierre and T. Kropf, editors, Correct Hardware Design                                        Minerva Foundation. From 2015
    and Verification Methods, 10th IFIP WG 10.5 Advanced Research                                              to 2018, his postdoc research was
    Working Conference, CHARME ’99, Bad Herrenalb, Germany,                                                    funded through the SYNTECH
    September 27–29, 1999, Proceedings, volume 1703 of Lecture                                                 project. Jan’s research interests are
    Notes in Computer Science, pp. 54–66. Springer (1999)                                                      in using formal methods for model-
79. Zeller, A.: Yesterday, my program worked. today, it does not. why?                                         based software engineering with
    In: ESEC/FSE, volume 1687 of LNCS, pp. 253–267. Springer                applications to autonomous systems. His work has been published in
    (1999)                                                                  top software engineering and modeling conferences and journals. Jan
                                                                            has co-developed and taught classes on synthesis using Spectra at Tel
                                                                            Aviv University. He was lead developer of the Spectra Tools from
                                                                            2014 to 2018. He obtained Fellowship status from the Higher Educa-
Publisher’s Note Springer Nature remains neutral with regard to juris-      tion Academy in 2020.
dictional claims in published maps and institutional affiliations.




123
