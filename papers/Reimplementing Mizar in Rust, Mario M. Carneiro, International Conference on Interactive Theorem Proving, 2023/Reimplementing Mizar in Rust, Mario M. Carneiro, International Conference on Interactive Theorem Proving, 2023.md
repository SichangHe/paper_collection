                                                           Reimplementing Mizar in Rust

                                                                             Mario Carneiro
                                            Hoskinson Center for Formal Mathematics, Carnegie Mellon University,
                                                      5000 Forbes Avenue, Pittsburgh, PA 15213, USA.
arXiv:2304.08391v2 [cs.PL] 23 Dec 2024




                                                Corresponding author(s). E-mail(s): mcarneir@andrew.cmu.edu;


                                                                                  Abstract
                                              This paper describes a new open-source proof processing tool, mizar-rs, a whole-
                                              sale reimplementation of the Mizar proof system, written in Rust. In particular,
                                              the main Mizar processing tool verifier is implemented, which can be used to
                                              verify the Mizar Mathematical Library (MML). This is to our knowledge the first
                                              and only external implementation of the system. We have used this to verify the
                                              entire MML in 11.8 minutes on 8 cores, a 4.8× speedup over the original Pascal
                                              implementation. Since Mizar is not designed to have a small trusted core, check-
                                              ing Mizar proofs entails following Mizar closely, so our ability to detect bugs is
                                              limited. Nevertheless, we were able to find multiple memory errors, four sound-
                                              ness bugs in the original (which were not being exploited in MML), in addition to
                                              one non-critical bug which was being exploited in 46 different MML articles. We
                                              hope to use this checker as a base for proof export tooling, as well as revitalizing
                                              development of the language.

                                              Keywords: Mizar, proof checker, software, Rust




                                         1 Introduction
                                         The Mizar language [1] is a proof language designed by Andrzej Trybulec in 1973 for
                                         writing and checking proofs in a block structured natural deduction style. The Mizar
                                         project more broadly has been devoted to the development of the language and tooling,
                                         in addition to the Mizar Mathematical Library (MML) [2], a compendium of “articles”
                                         on a variety of mathematical topics written in the Mizar language. The MML is one of
                                         the largest and oldest formal mathematical libraries in existence, containing (at time
                                         of writing) 1434 articles and over 65,000 theorems.




                                                                                       1
    The “Mizar system” is a collection of tools for manipulating Mizar articles, used
by authors to develop and check articles for correctness, and maintained by the Asso-
ciation of Mizar Users (SUM). Arguably the most important tool in the toolbox is
verifier, which reads a Mizar article and checks it for logical correctness. The start-
ing point for this work is the goal of extracting formal proofs from the verifier which
can be checked by a tool not directly connected to Mizar. This turned out to be quite
challenging, and this paper will explain how we achieved a slightly diﬀerent goal –
to build mizar-rs, a Rust program which checks proofs in the same manner as the
verifier, with an eye for proof generation.

Why hasn’t this been done before?
The ﬁrst challenge is that there is no “spec” for the Mizar language: a Mizar proof is
one that verifier accepts. Some of it is “obvious” things which users can ﬁgure out
by playing with the language, and there are reference works at varying levels of detail
[3, 4], but if we want to check the entire MML then approximations aren’t going to
cut it. There are some writings online which give the general sense of the algorithm,
but there is nowhere to look for details except the source code.
    This leads to the second challenge, which is that the source code for the Mizar
system is not publicly available, or at least was not while this project was under
development.1 It was only made available to members of the SUM. Luckily, it is
possible to obtain a membership, but the price of admission is that one has to write a
Mizar article ﬁrst. Thus, for this project the author contributed an article regarding
the divergence of the sum of prime reciprocals [5].
    The third challenge is that Mizar does not have a “small trusted kernel” in any
reasonable sense. The main components that perform trusted activities are the “ana-
lyzer” and the “checker”, and most of the code of the veriﬁer is contained in these
modules. Moreover, the code is written in Pascal and Polish (two languages that the
author is not very good at), and is 50 years old, meaning that there is a huge amount
of technical debt in the code.2 To get a good sense of what everything is doing and
why it is correct (or not), we estimated the best option would simply be to rewrite it
and closely follow what the original code is doing. Rust was chosen as the implementa-
tion language because it is well suited to writing console applications with a focus on
correctness, performance, and refactoring, all of which were important for something
that could play the role of verifier.
    We are not the ﬁrst to present aspects of Mizar from an outsider’s perspective. J.
Harrison’s Mizar mode in HOL Light [7] is a simulation of large parts of the Mizar
frontend, with the MESON prover used in place of the Mizar checker. J. Urban’s
MPTP [8] project exports the statements of checker goals and sends them to ATPs.
And most recently, Kaliszyk and Pąk presented a model of Mizar as encoded in Isabelle
[9], but stop short of a fully automatic proof export mechanism.
    One may reasonably ask why the MPTP export is not already everything you could
wish regarding proof export. There are two problems: (1) Because it is using external

   1
     A happy after-effect of this project is that the Mizar source code itself has been made public! It is now
available at https://github.com/MizarProject/system.
   2
     Technically the current incarnation of Mizar (“PC Mizar”) only dates to 1986. See [6] for the early history
of Mizar.


                                                       2
ATPs rather than Mizar’s own code, it does not and cannot reasonably be expected
to achieve 100% success on the MML, and even when it works the Mizar checker often
outperforms the external ATP, because the MML is signiﬁcantly overﬁt to the Mizar
checker. (2) Because it instruments the “checker inference” level, we verify “ by” steps
but not the skeleton steps that glue them together, and some signiﬁcant type reasoning
happens in the analyzer.
    In this paper, we will try to give an implementer’s perspective of Mizar: how it
works under the hood, and some things we discovered while trying to replicate the
functionality. The reader should be aware that this paper is focused on internal details
and implementation correctness of the Mizar system, not the abstract theory of Mizar
(that is, Tarski–Grothendieck set theory and the soft type system). See [3, 9] for
information on these aspects of the language.
    (This is an expanded version of a paper presented at ITP 2023. This paper includes
major revisions of section 2 and section 8, and new sections 5 and 6.)

2 Mizar internals: A (determined) user’s perspective
When one runs the verifier on a Mizar ﬁle, say tarski.miz, one will see something
like this:
Verifier based on More Strict Mizar Processor, Mizar Ver. 8.1.11 (Linux/FPC)
Copyright (c) 1990-2022 Association of Mizar Users
Processing: mizshare/mml/tarski.miz

Parser   [ 138]   0:00
MSM      [ 132]   0:00
Analyzer [ 137]   0:00
Checker [ 137]    0:00
Time of mizaring: 0:00
This refers to modules named Parser, MSM, Analyzer, Checker, so one can reasonably
guess that the code is split up into multiple passes and these are the names of the
modules.
• Parser reads the text and converts it into an abstract syntax tree.
• MSM stands for “More Strict Mizar”, which is a slightly more elaborated version of
  the syntax tree. Notably, this pass does (some kinds of) name resolution, as well as
  resolving and auto-binding reserved variables.
• Analyzer is responsible for processing the large scale logical structure of a Mizar
  document. It resolves symbol overloading and checks types, as well as tracking the
  “thesis” as it is transformed by Mizar proof steps.
• Checker is called by the analyzer whenever there are atomic proof obligations. It is
  sometimes referred to as the “ by” proof automation because it is called whenever
  there is a step proved using the by keyword.
   Both the analyzer and the checker are soundness-critical components. Clearly the
checker is important because it actually checks proofs – a bug here will mean that an
incorrect proof is accepted – but the analyzer is also important because it determines



                                           3
the proof obligations that will be sent to the checker. If the analyzer sends the wrong
assertion to the checker or simply doesn’t call the checker at all, then it might assert
a theorem that hasn’t been properly checked.


                                                        global data       main verifier
       in prel/
                                                         mml.ini               .miz
                                                         mml.vct
        dep .dre
                                                        mizar.dct

        dep .dcl                                                              parser           .idx
        dep .dco                                          accom
        dep .def
        dep .did          .aco    .cho      .atr   .dfe    .epr    .dfs        .frx            .err
        dep .dno          .ano    .prf      .ecl   .dfx            .eno                        .log
        dep .dpr                                                               .wsx
                          .dct    .sgl      .ere   .eid
        dep .drd          .dcx    .vcl             .erd
        dep .sch          .evl                     .esh                        MSM             .msx
        dep .the          .fil                     .eth
                          .frm
                                                               .ref            .par
                          .nol
          .dfr
                                                                             analyzer

                                                                               .xml


                                 exporter                                     checker

                       MPTP proof export           .fex    .bex                  X
Fig. 1 Data flow between Mizar components. Files with only an extension like .miz correspond to
files named after the input art .miz file. Files in red are in XML format. For example, art .atr is created
by the accommodator and read by the checker and the exporter. Files like dep .dcl are produced for
the current article by the exporter and aggregated by the accommodator in articles importing that
dependency.


    Another visible eﬀect of running verifier on a .miz ﬁle is that a huge number of
other ﬁles are generated with bespoke extensions, which reveals another implemen-
tation quirk of the Mizar system, which is that the four components above are very
loosely coupled and communicate only via the ﬁle system (see Figure 1). The parser
reads the .miz ﬁle and produces a .wsx ﬁle, which is read by MSM to produce .msx,
which is read by the transfer2analyzer module (not mentioned above) to produce
.par, which is read by Analyzer to produce .xml, which is read by Checker and veriﬁed.
    The general data ﬂow of a Mizar veriﬁcation looks like this:
• The ﬁrst tool to process the article is the “accommodator,” accom. This is the only
  tool which reads data from articles other than the current one; it is responsible
  for aggregating data from imports and collecting them for the current article. The


                                                    4
  many ﬁles produced in this pass are consumed as needed by later stages in the
  pipeline, to provide information about the extant declarations of various kinds in
  the environment.
• The next pass is the parser, which parses the body of the art .miz article and pro-
  duces a art .wsx ﬁle (Weakly Strict Mizar) containing the AST, along with art .frx
  containing the formats declared in the article.
• The MSM pass reads art .wsx and writes art .msx, performing name resolution and
  ﬁlling in the types of reservation variables in statements.
• The transfer2analyzer pass appears to be for backward compatibility reasons, as
  it reads art .msx and translates it to art .par, which is the same thing but in a less
  extensible format. It also resolves format references.
• The analyzer pass reads art .par and writes art .xml, which is the article AST again
  but using fully elaborated and typechecked terms, and with all the statements of
  checker subgoals explicitly annotated.
• The checker is the last pass. It reads art .xml and veriﬁes the theorems.
    Thanks to the eﬀorts of J. Urban in 2004 [10], most of these internal ﬁles between
the components are in XML format, highlighted in red. Of the non-XML ﬁles, most of
them have a simple format, with the notable exception of art .miz (see section 6) and
art .par (which we managed to avoid reading or writing by using art .msx instead).
    (mizar-rs has a signiﬁcantly diﬀerent architecture. One can ﬁnd identiﬁable compo-
nents corresponding to “accom”, “parser”, “MSM + analyzer”, “checker”, and “exporter”,
and for each PC Mizar component one can either enable it in mizar-rs, in which case
it will read the input ﬁles of that component and perform the work, or disable it in
which case it will read the output of that component. This allows mixing and match-
ing between the two implementations, for example running accom to generate all the
intermediate ﬁles, and then running only the “checker” component of mizar-rs, which
will expect e.g. art .eth to exist. If all components are enabled, only the dep .dre ﬁles,
the global ﬁles mml.ini, mml.vct, mizar.dct, and the article source ﬁles art .miz are
used, all of which are human-written input ﬁles.)
    If one opens one of these ﬁles, one is presented with the next major challenge, which
is that terms are pervasively indexed and hence reading the expressions can be quite
diﬃcult. Moreover, there are many distinct index classes which are diﬀerentiated only
by the context in which they appear, so without knowing how the program processes
the indices or what array is being accessed it is hard as an outsider to follow the
references. In the Rust implementation this issue is addressed by using “newtypes”
to wrap each integer to help distinguish diﬀerent indexing sets. There are currently
36 of these newtypes deﬁned: for example there are numbers for functors, selectors,
predicates, attributes, formats, notations, functor symbols (not the same!), left bracket
symbols, reserved identiﬁers, etc.
    After parsing these, one ends up with an expression such as
∀_ : M1 , R4 (K1 (B1 , K2 (N2 )), N1 ), which means something like “for all x of the ﬁrst
type, fourth relation holds of the ﬁrst function applied to x and the second function
applied to 2, and 1”. For many purposes, this is suﬃcient for debugging, but one
tends to go cross-eyed staring at these expressions for too long. Ideally we would
be able to reverse this indexiﬁcation to obtain the much more readable expression


                                            5
∀x : Nat, x · (−2) ≤ 1. However, the code to do this does not exist anywhere in Mizar,
because the Mizar checker never prints expressions. The only output of the checker is
a list of (line, col, err_code) triples, which are conventionally postprocessed by the
errflag tool to insert markers like the following in the text:

for x being Nat holds x = x
proof
  let x be Nat;
end;
::>,70
::>
::> 70: Something remains to be proved

This error message is pointing at the end keyword, but notably it does not say what
remains to be proved, here x = x. A debug build of Mizar will actually print out
expressions to the art .inf ﬁle, but they are similar to the R4 (K1 (. . . )) style.
    Luckily, this issue has been addressed outside the main Mizar codebase: J. Urban’s
HTMLizer is an XSLT stylesheet which can transform the XML intermediate ﬁles into
fully marked up reconstructed Mizar documents, and which we adapted to design the
formatter.
    With the present version of the formatter, and with appropriate debugging enabled,
an input like the following:
for x,y being Nat holds x = 1 & y = 2 implies x + y = 3;

yields this debugging trace:
input: ∃ b0: natural set, b1: natural set st
  (b0 = 1) ∧ (b1 = 2) ∧ ¬((b0 + b1) = 3)
refuting 0 @ TEST:28:33:
  ∃ b0: natural set, b1: natural set st
    (b0 = 1) ∧
      (b0 c= 1) ∧
      (1 c= b0) ∧
      (b1 = 2) ∧
      (b1 c= 2) ∧
      (2 c= b1) ∧
      ¬((b0 + b1) = 3) ∧
      (((b0 + b1) c= 3) → ¬(3 c= (b0 + b1)))
In addition to showing some of the formatting and indentation behavior of the recon-
structed expression, this also reveals some aspects of the checker, like how the goal
theorem has been negated and the deﬁnitional theorem x = y ↔ x ⊆ y ∧ y ⊆ x has
been eagerly applied during preprocessing.
    One other feature that is demonstrated here is “negation desugaring”, which
requires some more explanation. Internally, Mizar represents all expressions using only
¬, ∀ and n-ary ∧. So P → Q is mere syntax for ¬(P ∧ ¬Q) and ∃x, P (x) is actually
¬∀x, ¬P (x). (Even P ↔ Q is desugared, to ¬(P ∧ ¬Q) ∧ ¬(Q ∧ ¬P ), so too much
recursive use of ↔ can cause a blowup in formula size.) This normalization ensures
that diﬀerent spellings of the same formula are not distinguished, for example if the


                                          6
goal is P ∨ Q then one may prove it by assume not P; thus Q;. Double negations are
also cancelled eagerly. In the formatter, we try to recover a natural-looking form for
the expression by pushing negations to the leaves of an expression, and also writing
A ∧ B → C ∨ D if after pushing negations we get a disjunction such that the ﬁrst
few disjuncts have an explicit negation. (Mizar actually carries some annotations on
formulas to help reconstruct whether the user wrote not A or B or A implies B, but
we chose not to use this information as it is often not available for expressions deep
in the checker so we wanted a heuristic that works well in the absence of annotation.)

3 The checker
Mizar is broadly based on ﬁrst order logic, with the non-logical axioms of Tarski–
Grothendieck set theory, with a type system layered on top. While types can depend
on terms, so one may call it a dependent type theory, this is not a type system in
the sense of Martin-Löf type theory: types are essentially just predicates over terms
in an untyped base logic, and the language allows typing assertions to be treated as
predicates.

3.1 Core syntax
The core syntax of Mizar uses the following grammar:

                 a, b, c, d, e, F, G, H, K, U, V, P, R, S, TM , TG ::= ident

  t ::= a, b, c, d, e        variable               ϕ ::= ⊤              true
       |n                    numeral                     | ¬ϕ            negation
                          →
                          −                                V−
       | {F, G, K, U }( ti ) function application        |     →
                                                               ϕ         conjunction
             →
             −                                             Vt′
                                                                 i
       | H( ti ) := t′       local function app.         | b=t ϕ         ﬂex conjunction
       | the τ               choice
              −−−→                                       | ∀ b : τ. ϕ    for all
       | {t | bi : τi | ϕ}   Fraenkel                                →
                                                                     −
                                                         | {P, R}( ti ) predicate
                   →
                   −
 τ ::= − →
         χ i T M ( ti )      mode                              →
                                                               −
                                                         | S( ti ) := t′ local pred.
         →
         −        →
                  −
       | χ i T G ( ti )      struct type                 | t is χ        attribute
               →
               −                                         | t : τ         qualiﬁcation
 χ ::= ±V ( ti )             attribute
     Broadly speaking, terms are ﬁrst order, meaning applications of function symbols
                                                               −−−→
to variables. The exception is the Fraenkel operator {t | bi : τi | ϕ}, which should be
                           →
                           −             −−−→                      →
                                                                   −
read as “the set of t( bi ) where the bi : τi are such that ϕ( bi )”, where the variables
−−−→
bi : τi are quantiﬁed in both t and ϕ.
     All terms t have a type τ , and there is a robust subtyping system – most terms
have many types simultaneously. All types are required to be nonempty, which is
what justiﬁes the the τ constructor for indeﬁnite description. Types are composed
                                                                                      →
                                                                                      −
of a collection of attributes (a.k.a. clusters) χ applied to a base type {TM , TG }( bi ).
Regular types are called “modes”; new modes can be deﬁned by carving out a subset of
an existing mode, and modes need not deﬁne a set (in particular, object is a primitive
mode which is the supertype of everything, and does not constitute a set per Russell’s


                                             7
paradox). Structure types are roughly modeled after partial functions from some set
of “tags”, but they are introduced axiomatically, similarly to how structure types are
treated in a dependent type theory such as Coq or Lean.
Remark 1. Although one can define a mode for any ZFC set or class, modes and
sets are not interchangeable in Mizar because they lie in different syntactic classes.
Modes are types, which go in the type argument of quantifiers such as the Nat in ∀x :
Nat. x ≥ 0, while sets are objects, which can be passed to functions, like |NAT| = ℵ0 . In
the MML, NAT is the set of natural numbers, while Nat and Element of NAT are modes
which describe the type of natural numbers (and in general Element of A can be used
to treat a set as a type).
    Attributes, also known as “adjectives” or “clusters”, are modiﬁers on types, which
may be described as intersection typing in modern terminology, although attributes
do not stand alone as types. For example, “ x is non empty finite set” means
¬(x is empty) ∧ (x is finite) ∧ (x : set). The Mizar system treats the collection of
attributes on a type as an unordered list for equality comparisons.
    Formulas are composed mainly from negation, conjunction and for-all, but there
are some extra formula constructors that deserve attention:
• Not represented in the grammar is that ¬¬ϕ is identiﬁed with ϕ, and internally
  there is an invariant that ¬¬ never appears.
• Similarly, conjunctions are always ﬂattened, so P ∧(Q∧R)∧S becomes P ∧Q∧R∧S.
• Unlike most type theories, typing assertions are reiﬁed into an actual formula, so it
  is possible to say 4/2 : N and ¬(−1 : N).
• There is also a predicate for having an attribute, and (t : χ τ ) ↔ (t is χ) ∧ (t : τ ) is
  provable.
• Flex-conjunction is written with syntax such as P[1] & ... & P[n] (with literal
  “ ...”), and Mizar knows that this expression is equivalent both to ∀x : N. 1 ≤ x ≤
  n → P (x) as well as to an explicit conjunction (when n is a numeral). For example
  P[1] & ... & P[3] will be expanded to P[1] & P[2] & P[3] in the checker.

   The diﬀerent letters for functions, predicates, and variables correspond to the
diﬀerent roles that these can play, although in most situations they are treated
similarly.
• “Locus variables” (a) are used in function declarations to represent the parameters
  of a function, mode, cluster, etc. For example a local function might be declared
  as K(−→
        ai ) : τ := t where τ and t are allowed to depend on the −  →
                                                                    ai , and then when
                                    →
                                    −              −−−−→
  typing it we would have that K( ti ) has type τ [ai 7→ ti ].
• “Bound variables” (b) are de Bruijn levels, used to represent variables in all binding
  syntaxes. So for example, ∀x : N. ∀y : N. x ≤ x + y would be represented as
  ∀ : N. ∀ : N. b0 ≤ b0 + b1 . NB: there are two conventions for locally nameless
  variables, called “de Bruijn indices” (variables are numbered from the inside out)
  and “de Bruijn levels” (variables are numbered from the outside in), and Mizar’s
  choice of convention is the less common one.
• “Constants” (c) are variables that have been introduced by a consider, given, or
  take declaration, as well as Skolem constants introduced in the checker when there
  are existentially quantiﬁed assumptions. Constants may or may not be deﬁned to


                                             8
  equal some term (for example take x = t will introduce a variable x equal to t) and
  the checker will use this in the equalizer if available.
• “Inference constants” (d) are essentially checker-discovered abbreviations for terms.
  This is used to allow for subterm sharing, as terms are otherwise completely
  unshared.
• “Equivalence classes” (e) are used in the equalizer to represent equivalence classes
  of terms up to provable equality. So for example if the equalizer sees a term x + y it
  will introduce an equivalence class e1 for it and keep track of all the things known
  to be in this class, say e1 = x + y = y + x = e1 + 0.
• Functors (K) and predicates (R) are the simplest kind of deﬁnition, they correspond
  to function and relation symbols in traditional FOL.
• Scheme functors (F ) and scheme predicates (P ) are the higher-order analogue of
  constants. They are only valid inside scheme deﬁnitions, which declare these at the
  start and then use them in the statement and proof.
• Local functors (H) and local predicates (S) are function declarations within a local
  scope, declared with the deffunc or defpred keywords. Internally every predicate
  carries the result of substituting its arguments, so if we declare deffunc H1 (x, y) :=
  x + y then an expression like 2 · H1 (x − 1, y) is really stored as 2 · (H1 (x − 1, y) := x −
  1 + y). Some parts of the system treat such an expression like a function application,
  while others treat it like an abbreviation for a term.
• An aggregate functor (G) is Mizar terminology for a structure constructor {foo :=
  x, bar := y} : MyStruct, and the converse operator is a selector (U ), which is the
  projection t.foo for a ﬁeld. (The Mizar spelling for these operators is MyStruct(#
  x, y #) for the constructor and the foo of t for the projection.)


3.2 Structure of the checker
The checker is called whenever there is a proof such as “ 2 + 2 = 4;” or
“ x <= y by A1,Thm2;”: basically any time there is a by in the proof text, as well as
when propositions just end in a semicolon, this being the nullary case of by. It consists
of three major components, although there is another piece that is used even before
the checker is properly called on a theorem statement:
0. Attribute inference (“rounding-up”) is used on every type −       →
                                                                     χ − τ to prove that
                        →
                        −  +          →
                                      − +                    →
                                                             − −
    it is equivalent to χ τ where χ is a superset of χ . Internally we actually
    keep both versions of the attributes (the “lower cluster” −
                                                              →
                                                              χ − being the one provided
                                           →
                                           − +
    by the user and the “upper cluster” χ being what we can infer by applying all
   inference rules), because it is useful to be able to prove that two clusters are equal
   if −
      →
      χ−    →+
            −         →− −
                      −      →+
        1 ⊆ χ 2 and χ 2 ⊆ χ 1 .
1. The pre-checker takes the list of assumptions, together with the negated conjec-
   ture, and performs a number of normalizations on them, skolemizing existentials,
   removing vacuous quantiﬁers, and expanding some deﬁnitions. Then it converts the
   whole formula into disjunctive normal form (DNF) and tries to refute each clause.
2. The equalizer does most of the “theory reasoning”. It replaces each term in the
   clause with an equivalence class, adding equalities for inference constants and
   deﬁned constants, as well as registered equalities and symmetry declarations, as well


                                              9
   as any equalities in the provided clause. It also evaluates the numeric value (for
   2+2 = 4 proofs) and polynomial value (for (x+1)2 = x2 +2x+1 proofs) of equality
   classes and uses them to union classes together. These classes also have many types
   since many terms are going into the classes, and all of the attributes of these types
   are mixed together into a “supercluster” and rounded-up some more, potentially
   leading to a contradiction. For example if we know that x = y and x is positive and
   y is negative then the supercluster for {x, y} becomes positive negative which is
   inconsistent.
3. The last step is the unifier, which handles instantiation of quantiﬁers. This is rela-
   tively simplistic and non-recursive: for each assumption ∀~b. P (~b) it will instantiate
   P (~v ) (where ~v are metavariables) and then construct the possible assignments (as a
   DNF) to the variables that would make P (~v ) inconsistent with some other assump-
   tion. It tries this for each forall individually, and if it fails, it tries taking forall
   assumptions in pairs and unifying them. If that still fails then it gives up – it does
   not attempt a complete proof method.
Finally, there is one more component which is largely separate from the “ by”
automation:
4. The schematizer is the automation that is called for justiﬁcations starting with
   “ from”. These are scheme instantiations. In this case it is very explicitly given the
   list of hypotheses in the right order, so the only thing it needs to do is to determine
   an assignment of the scheme variables (F, P ) to regular functors and predicates
   (K, R) or local functors and predicates (H, S). Users are often required to introduce
   local predicates in order to apply a scheme. Nullary scheme functors (a.k.a constant
   symbols) can be uniﬁed with arbitrary terms, however.
    Although we cannot go into full detail on the algorithms here, in the following
sections we will go into some of the highlights, with an emphasis on what it takes to
audit the code for logical soundness, through the lens of root-causing some soundness
bugs.

3.3 Requirements
One aspect of the Mizar system that is of particular interest is the concept of “require-
ments”, which are deﬁnitions that the checker has direct knowledge of. For example,
the grammar given above does not make any special reference to equality: it is sim-
ply one of the possible relation symbols Ri (x, y), and the relation number for equality
can vary from one article to the next depending on how the accommodator decides to
order the imported relation symbols. Nevertheless, the checker clearly needs to reason
about equality to construct equality equivalence classes.
    To resolve this, there is a ﬁxed list of “built-in” notions, and one of the ﬁles produced
by the accommodator (art .ere) speciﬁes what the relation/functor/mode/etc. number
of each requirement is. Importantly, if a constructor is identiﬁed in this way as a
requirement, this not only allows the checker to recognize and produce expressions like
x = y, it is also an assertion that this relation behaves as expected. If a requirement is
given a weird deﬁnition, for example if we were to open xcmplx_0.miz and change the


                                             10
deﬁnition of x + y to mean subtraction instead, we would be able to prove false in a
downstream theorem which enables the requirement for +, because we would still be
able to prove 2 + 2 = 4 by evaluation.
   At the surface syntax level, requirements are enabled in groups, using the
requirements directive in the import section. The requirements are, in rough depen-
dency order:
• HIDDEN (introduced after the HIDDEN article) is a requirement that is automatically
  enabled for every Mizar ﬁle. It introduces the modes object and set, as well as
  x = y and x ∈ y. (The article HIDDEN itself is somewhat magical, and cannot be
  processed normally because every ﬁle takes an implicit dependency on HIDDEN.)
• BOOLE (introduced after XBOOLE_0) introduces the adjective x is empty, as well as
  set operators ∅, A ∪ B, A ∩ B, A \ B, A ⊕ B, and A meets B (i.e. A ∩ B 6= ∅).
  These operators have a few extra properties such as A ∪ ∅ = A that are used in the
  equalizer.
• SUBSET (introduced after SUBSET_1) introduces the mode Element of A, along with
  P(A), A ⊆ B, and the mode Subset of A. The checker knows about how these
  notions relate to each other, for example if x ∈ A then x : Element(A). (Because
  types have to be nonempty, x : Element(A) is actually equivalent to x ∈ A ∨ (A =
  ∅ ∧ x = ∅). So the reverse implication used by the checker is (x : Element(A)) ∧
  ¬(A is empty) → x ∈ A.)
• NUMERALS (introduced after ORDINAL1) introduces succ(x), x is natural, the set N
  (spelled NAT or omega), 0, and x is zero. Note that 0 is not considered a numeral in
  the sense of section 3.1, it is a functor symbol Ki (). Numbers other than 0 can be
  written even before the ORDINAL1 article, but they are uninterpreted sets; after this
  requirement is added the system will give numerals like 37 the type Element of NAT
  instead of set.
• REAL (introduced after XXREAL_0) introduces x ≤ y, x is positive, x is negative,
  along with some basic implications of these notions.
                                                            Vb
  – NUMERALS + REAL enables the use of ﬂex-conjunctions i=a ϕ(i), since these
    expand to the expression ∀i : N. a ≤ i ≤ b → ϕ(i) which requires N and ≤ to
    write down.
• ARITHM (introduced after XCMPLX_0) introduces algebraic operators on the complexes:
  x + y, x · y, −x, x−1 , x − y, x/y, i, and x is complex. This also enables the ability to
  do complex rational arithmetic on numerals, as well as polynomial normalization.

3.3.1 Soundness considerations of the requirements
There is a slight mismatch between what the user has to provide in order to enable a
requirement and what the checker gets to assume when a requirement is enabled which
causes a challenge for proof export or other external soundness veriﬁcation. As the list
above might indicate, generally checker modules corresponding to a requirement are
enabled as soon as all of the constructors involved in stating them are available; for
example we can see this with the NUMERALS + REAL prerequisite for ﬂex-conjunctions.


                                            11
(More precisely, ﬂex-conjunctions are enabled exactly when N and ≤ become avail-
able.) However, the checker needs more than that to justify the manipulations it does
with them.                                               V3
    For example the checker exploits the fact that i=1 ϕ(i) is equivalent both to
∀i : N. 1 ≤ i ≤ 3 → ϕ(i) and to ϕ(1) ∧ ϕ(2) ∧ ϕ(3), and so this amounts to an assertion
that a ≤ i ≤ b ↔ i = a ∨ i = a + 1 ∨ · · · ∨ i = b is provable when a and b are numerals
such that a ≤ b. The reverse implication follows from numerical evaluation, and the
forward implication is a metatheorem that can be proven by induction, assuming the
existence of lemma L saying a ≤ i → i = a ∨ succ(a) ≤ i:
Theorem 1. If a and n are numerals and i : N, then

            i : N ⊢ a ≤ i ≤ succn (a) → i = a ∨ i = succ(a) ∨ · · · ∨ i = succn (a)
is provable.
Proof. By induction on n. Applying the induction hypothesis with succ(a) and n − 1,
we get

             i : N ⊢ succ(a) ≤ i ≤ succn (a) → i = succ(a) ∨ · · · ∨ i = succn (a)

so it suﬃces to show a ≤ i → i = a ∨ succ(a) ≤ i, and we appeal to lemma L.
    So ideally, when introducing ≤ or the REAL requirement, one would be required to
supply a proof of lemma L somehow to justify that the checker will be making use of
this fact in the following article. Unfortunately, there is no actual place to inject this
theorem into the system, because there is no concrete syntax for introducing require-
ments. That is, even taking all the .miz ﬁles in the MML together there is nothing
that would indicate that XXREAL_0 is the article which allows the REAL requirement to
be used.3
    The way this actually works is that when the accommodator sees a
requirements REAL; directive, it reads the (hand-written) real.dre XML ﬁle, which
explicitly names the constructor number for ≤ and the fact that it is in article XXREAL_0.
We would like to propose that this ﬁle also contains justifications for involved constants
so that the theorems aren’t smuggled in without proof. (Or even better, requirement
declarations become a part of the language proper, so that they can get correctness
proof blocks like any other justiﬁed property.)
    The case of NUMERALS + REAL enabling ﬂex-conjunctions is especially interesting
because neither of these requirements depends on the other, so neither numerals.dre
nor real.dre can state the compatibility theorem a ≤ i → i = a ∨ succ(a) ≤ i between
them. (This doesn’t require a major reorganization to ﬁx, since of course the article
that introduces REAL, xxreal_0.miz, references the article which introduces NUMERALS,
ordinal1.miz.)

  3
    Note that is also a Mizar article called real.miz, which contains some of the lemmas that are auto-proved
by the REAL requirement, but there is no formal relation between the article and the requirement, and it is
only an incomplete approximation to the lemmas required to justify the requirement, not formally checked.
This should be easy to fix, and will more or less fall out of any attempt at proof export.




                                                     12
4 The analyzer
The analyzer plays an interesting role in Mizar. This is an essentially completely sepa-
rate inference system from the checker, which has much stricter rules about equality of
expressions, and it is what forms the “glue” between diﬀerent lines of proof. It is a large
module only because the language of Mizar is quite expansive, with 109 keywords,
including:
• Diﬀerent kinds of deﬁnitions for modes, functors, predicates; redeﬁnitions;
• Deﬁnitions by case analysis;
• “Notations” (synonym and antonym declarations);
• “Properties” like commutativity, projectivity or involutiveness;
• Cluster registrations (existential, functor, and conditional);
  – Existential clusters assert that −→
                                      χ τ is nonempty and hence a legal type
  – Functor clusters assert that t is −→χ for some term t
  – Conditional clusters assert that χ implies −
                                       →
                                       −          →
                                                  χ′
• “Reductions”, equalities the checker automatically uses for simpliﬁcation;
• “Identiﬁcations”, equalities the checker automatically uses for congruence closure;
• Local declarations;
• Schemes;
• Reservations (variables with types declared in advance);
• Propositions and theorems;
and this is not an exhaustive list.
   This also only covers top-level items. Inside a proof block there is a diﬀerent (over-
lapping but largely disjoint) set of legal items, called skeleton steps, which correspond
to natural deduction rules. Inside a proof there is a variable that holds the current
“thesis”, the goal to prove, and the thesis keyword resolves to it, unless one is in a now
block, where the thesis is not available and is reconstructed from the skeleton steps.
• let x be T; is the forall introduction rule: it transforms the thesis from ∀x : T. ϕ(x)
  to ϕ(x) and introduces a constant x : T .
• assume A; is the implication introduction rule: it transforms the thesis from A → B
  to B and pushes a proposition A, which can be referred to using then.
• thus A; is the conjunction introduction rule: it transforms the thesis from A ∧ B to
  B, and gives A as a goal to the checker.
• take t; is the existential introduction rule: it transforms the thesis from ∃x. ϕ(x) to
  ϕ(t). There is also take x = t; which is the same but introduces x as an abbreviation
  for t; this version can also be used in a now block.
• consider x being T such that A; is existential elimination: it introduces x : T and
  a proposition A(x) that can be labeled, and gives ∃x : T. A(x) as a goal to the
  checker.
• given x being T such that A; is a combination of implication introduction and
  existential elimination: it transforms (∃x : T. A(x)) → B to B and introduces x : T
  and a proposition A(x) that can be labeled.




                                            13
• reconsider x = t as T; introduces x : T as a new local constant known to be equal
  to t, and gives (t : T ) as a proof obligation to the checker. (This is mainly used
  when t : T is not already obvious to the type system, and allows t : T to be proved
  by the user.)
• per cases; is disjunction elimination, and it has two variations:
                                                                       W
  – followed by a sequence of suppose A_i; ... end; blocks, it gives i Ai as a goal
    to the checker and makes Ai available in each block, leaving theWthesis unchanged;
  – followed by a sequence of case A_i;
                                      W    ... end; blocks, it gives i Ai as a goal to
    the checker, and if the thesis is i (Ai ∧ Bi ) then Bi becomes the thesis in each
    block.
    Additionally, the formulas don’t have to exactly match what the skeleton steps say.
For example one can start a proof of ∀x : N. ϕ(x) using let x be set; because set
is a supertype of Nat. Deﬁnitional unfolding can also be forced by a skeleton step, for
example if the thesis is A ⊆ B then let x be set; is a legal step provided the right
definitions directive is supplied.
    The other major role of the analyzer is to elaborate types, terms, and formulas
from their input form to the core grammar shown in section 3.1. There are two things
that make this challenging:
• Mizar heavily uses overloading, where the same function symbol can have several
  deﬁnitions (and redefinitions, which are deﬁnitions which use the same base term
  but can have diﬀerent input and output types). These are resolved by declaration
  order (last declaration wins) and typing. Types are propagated exclusively from the
  inside out, using this type-based overload resolution, although you can use e qua A
  as a type ascription to inﬂuence the selection.
• Many declarations have “invisible arguments”, also known as “implicit arguments” in
  the literature. These are ﬁlled in by a straightforward ﬁrst-order uniﬁcation process.4

5 Name resolution (MSM)
The MSM (more strict Mizar) pass in the veriﬁer is primarily concerned with name res-
olution and the reserve keyword. In mizar-rs this task is done as part of the analyzer,
but in the original Mizar this is a separate pass, converting art .wsx to art .msx.
    Generally speaking, name resolution is a straightforward process that proceeds as
one would expect. A declaration like let x be set; introduces a variable x until the
end of the scope, which is a block such as proof ... end;. Variables are locally bound
by constructs like for x being set holds P[x].
    Where things get interesting is when the top level command reserve x for set;
is used. This has two eﬀects:
  4
    Unfortunately, the unification process does not have completely unique solutions, because attributes
are unordered, and this can lead to overfitting in the MML to the Mizar attribute ordering. For example,
rng(f ) ⊆ B returns the range of a function f : A → B as an element of Subset of B (and rng has hidden
arguments rngA,B (f ) inferred from the types). But the function type is split into separate attributes as
A-defined B-valued Function, so if f is B-valued C-valued Function then it is up to a variety of implementation
details whether you get the type of rng f as Subset of B or Subset of C. This happens in practice for the
empty function, which is registered as NAT-valued, RAT-valued, and a few others.




                                                     14
• The variable x can now be used as a binder without specifying the type:
  for x holds P[x]. This would otherwise be an error. (Unlike some other type theory
  based systems, Mizar performs no type inference for variables based on usage.)
• The variable x will be implicitly quantiﬁed when used as a free variable in theo-
  rems. For example theorem x = x; becomes legal and deﬁnes a theorem which says
  for x being set holds x = x.

   There is more to implicit quantiﬁcation than meets the eye, though, because
implicit quantiﬁcation also occurs in nested positions. For example:
reserve a,b,c,d for Nat;
{{c,a} : a + b < d} = d;

parses as:
for d being Nat holds
  {{c,a} where a,c is Nat : for b being Nat holds a + b < d} = d;

The way we explain this behavior is by deﬁning a tree of nested implicit quantification
scopes as follows:
• The top level of a formula is an implicit quantiﬁcation scope.
• A Fraenkel operator {e | x : T | ϕ} deﬁnes two implicit quantiﬁcation scopes, one
  around the whole {e | x : T | ϕ} expression, and one around ϕ.
These scopes form a tree structure, and given a reserved variable we can mark each
node according to whether it contains a use of the variable which is not in a sub-scope.
For the above example we obtain the following marking structure:

                      {{c,a} : a + b < d} = d                  d

                         {{c,a} : a + b < d}        a      c

                              a + b < d             a b        d

We then place the quantiﬁer for each variable at every node such that none
of its ancestors are marked. This means that d is bound at the top, a and
c are bound in the middle node, and b is bound in the innermost node.
A variable may end up bound more than once if it appears in disjoint
subtrees. For example {0 : b = b} = {1 : b = b} will bind b twice to obtain
{0 : for b being Nat holds b = b} = {1 : for b being Nat holds b = b}.
    Reserved variables can also have dependent types, such as reserve x for set,
y for Element of x;. In this case, a use of variable y causes x to also be considered
as used and may cause it to be pulled in for implicit quantiﬁcation. But this also
interacts with the ﬁrst use of reserved variables (type elision for binders), in that:
for x holds {0 : y = y} = x
:: elaborates to ->
for x being set holds {0 : for y being Element of x holds y = y} = x


                                          15
for z being set holds {0 : y = y} = z
:: elaborates to ->
for z being set holds
  {0 : for x being set, y being Element of x holds y = y} = z
where we note that the binder for y has a type referring to the explicit
for x binder in the ﬁrst example. Because implicit quantiﬁcations always
go ﬁrst, before any explicit quantiﬁers, there are ways to use this to
obtain invalid expressions, for example for x holds y = y would elaborate to
for y being Element of x, x being set holds y = y, where y’s type attempts to
refer to a binder deeper in the expression. Such constructs are rejected by the checker.5

6 The parser
Working from back to front, we ﬁnally end up at the parser, which is the component
which reads the input ﬁle and produces an abstract syntax tree (AST) which is pro-
cessed by the stages we have already seen. Several papers about the Mizar parser have
been written, inlcuding [11–13].

6.1 The scanner
The ﬁrst component in the parser is the scanner, also known in the literature as the
tokenizer. This is responsible for separating the input text into a sequence of “tokens”
which are then built into a tree structure in the parser. This is a fairly standard design
for a programming language, but the Mizar tokenizer makes some unique choices which
have historically make parsing Mizar tricky.
    The top of a Mizar ﬁle is the environment section of the form environ ... begin,
which is pre-parsed with a ﬁxed grammar. The accommodator reads only this part
of the ﬁle, and then loads all the data for the referenced articles, before the parser
can proceed to the rest of the ﬁle. This is important, because the Mizar tokenizer
is extensible. In contrast to some ITP systems (and to the frustration of its users),
tokens are deﬁned by an external art .voc ﬁle, or in the global mizar.voc ﬁle used for
deﬁnitions in the MML, rather than in the art .miz ﬁle itself. This means that:
definition
  let x be Nat;
  func foo x -> Nat equals x+1;
  correctness;
end;
results in some parse errors like Functor symbol expected at the foo token, which are
ﬁxed by adding the line Ofoo to the art .voc ﬁle, where the O means that this is a
functor symbol declaration.
   This usability issue seems relatively easy to ﬁx—the deﬁnition site
func foo x ->... could be taken to deﬁne a new token foo, rather than having to

  5
    At least, mizar-rs rejects these constructs. Original Mizar appears not to be hardened against this, and
gives an assertion violation with this example.


                                                    16
be declared separately (in a not particularly human readable ﬁle). But mizar-rs
currently just follows the same strategy as PC Mizar here.

6.2 The parser
The Mizar language has a rather large grammar, with 115 keywords like assume,
hereby, involutiveness, and reducibility. This derives from Mizar’s origin as a con-
trolled natural language, where Mizar proofs “read like mathematics” and the grammar
does not need to be learned explicitly. On the other hand, Mizar does not have very
many synonyms, in the sense of keywords that can be freely interchanged, so when
writing Mizar one very much does need to know the formal grammar.
    We have already seen the top level constructs of a Mizar ﬁle in section 4. The
formal grammar is also presented in BNF form on the Mizar website6 , so we will not
dwell on it. However, mizar-rs does not (and cannot) simply use a parser generator
applied to the BNF to get a working Mizar parser. There are a few reasons for this:
• This makes it possible to implement the parser without a lot of lookahead: the
  maximum lookahead is two tokens, to diﬀerentiate A: 1 = 1 from A + 1 = 1. Using
  the BNF directly would result in unbounded lookahead.
• There are also some constraints which would bloat the BNF; for example, the term
  former the field is legal only within a structure declaration; outside a structure
  one must instead use the field of struct. One would need to have two copies of
  the term grammar to express this in a context-free way.
• There are some cases of genuine ambiguity in the grammar.
  – The BNF deﬁnes ϕ & ψ or χ without a precedence ordering, which would imply
    two valid parses. In reality there is a precedence ordering here and only one parse
    is valid. There are no user-deﬁned formula operators, so this is a ﬁxed list.
  – Similarly, inﬁx operators in the term grammar have deﬁned precedences, so
    that a + b * c parses as expected. In this case the operators are user-deﬁned,
    so precedence is speciﬁed in the art .voc ﬁle and the parser has to handle a
    dynamic-precedence grammar.
  – One particularly nasty case of ambiguity in the grammar is caused by the fact that
    commas are used for separating between binder groups, and also for separating
    the arguments of a type. For example:
       reserve x for set, y for Element of x, f,g for Function of x,y, w for set;
       We have inserted extra spaces to clarify, but Mizar has to know the “arity” of
       Element and Function here to realize that in “ x, f,g”, the x is part of the type
       of y while f,g are new variable directives, and in “ x,y, w” the ﬁrst two variables
       are arguments because Function of x,y takes two arguments.
       To make things worse, a type operator need not have only one arity. For example
       Relation of X and Relation of X,Y are both deﬁned (meaning subsets of X × X
       and X × Y respectively). Mizar (and mizar-rs) currently uses a heuristic to avoid
       backtracking in this situation, which is to take all arguments up to the maximum
       arity of the type operator.

 6
     https://mizar.uwb.edu.pl/language/


                                            17
    Disambiguating inﬁx expressions in the term grammar turns out to be especially
subtle and a bit mathematically interesting, so we will go into a bit more detail
there. Mizar allows inﬁx functions with more than 2 arguments, by using a tuple-like
notation before or after the symbol. In general, a functor application has the form
(x1 , . . . , xm ) F (y1 , . . . , ym ), where F is a functor symbol, and there are m left and
n right arguments to the function. When m = 1 the parentheses are optional, and
when m = 0 nothing is written. So this generalizes the notion of preﬁx, postﬁx, and
inﬁx functions like F(x,y,z), x + y, and x ^2. But just like with type constructors,
functor symbols can be overloaded, and in fact the parser must disambiguate based
on (F, m, n), that is, it resolves a functor symbol together with its number of left and
right arguments, so you could simultaneously have -y, x-y, and x-(y,z) as independent
operations associated to the functor symbol -.
    In general, the input to precedence resolution is a sequence of operators separated
by arguments, of the form:

              (x01 , . . . , x0k0 ) F1 (x11 , . . . , x1k1 ) F2 . . . Fn (xn1 , . . . , xnkn ).

The goal is to produce a suitable parenthesization of the operators (that is, a binary
tree with Fi on internal nodes and (xij )j≤ki on the leaves) respecting precedence such
that each Fi is applied to the right number of arguments. One might think that we can
just put the operators into a tree such that Fi is a left child of Fj if prec(Fi ) ≤ prec(Fj )
and Fi is a right child of Fj if prec(Fi ) < prec(Fj ) (note, all precedence levels in Mizar
are left-associative), but this produces an incorrect result in practice.
    An example of this is the expression union union X, which we can pre-parse as
() union () union (X). Grouping this only using precedence and left-associativity
results in the parse (() union ()) union (X), where the ﬁrst union operator is applied
to 0 left and right arguments, and the second is applied to 1 left and 1 right argu-
ment. In this case neither operator exists and we give an error, but the alternative
parse () union (() union (X)) would apply both union operators to 0 left and 1 right
argument, which does exist (union X is the union of a set of sets).
    We can formalize this as a constrained optimization problem, where we want to pick
a solution which violates as few precedence ordering constraints as possible, among
solutions that only use operator formats that actually exist. The unconstrained prece-
dence ordering problem can be solved in O(n) in the length of the chain of operators,
but to our knowledge there is no similar O(n) algorithm for constrained precedence
parsing. There does exist an O(n4 ) dynamic programming algorithm, in which we cal-
culate for each 1 ≤ a ≤ i ≤ b ≤ n on the substring Fa , . . . , Fb of the original problem
the minimal cost (or +∞) of a solution having Fi at the root of the tree. (There are
O(n3 ) of these subproblems and they can be calculated from smaller subproblems in
O(n).)
    Original Mizar does not actually use this algorithm, it uses an approximation of it
which is O(n2 ). So (unfortunately) mizar-rs follows suit, since MML is already known
to satisfy it. It would be interesting to see whether there exists a hybrid algorithm
which works in the general case and is still O(n2 ) in the situation where the original
Mizar algorithm works.



                                                    18
7 Mizar soundness bugs
One of the fortuitous side eﬀects of going over each line of code and rewriting it to
something morally equivalent in a diﬀerent language is that one can ﬁnd a lot of bugs.
Bugs can happen even when one takes great eﬀorts to avoid them [14, 15], but external
review can deﬁnitely help. Mizar is a large project with a long history and a small
team, whose source code was not publicly accessible, with many soundness-critical
parts, which is pretty much a worst case scenario for ﬁnding soundness bugs. This
mizar-rs project has been tremendously successful in ferreting out these bugs, with no
less than four proofs of false that will be given below. We reported these bugs to the
Mizar developers, and they have been ﬁxed (and the MML patched) in version 8.1.14.
    While it is unfortunate that the software wasn’t perfect to start with, this is evi-
dence for the usefulness of external checkers, and it is a way for us to improve the
original Mizar. We hope that by telling the story of how these bugs work we can give
some sense of some of the issues that can arise when doing proof checking, as well as
some more internal details whose importance may not have been obvious.

7.1 Exhibit 1: polynomial arithmetic overflow
This is the largest of the contradiction proofs, and we will show only the main part of
it.7 The only non-MML notion used is the adjective a is x-ordered deﬁned as x < a.
theorem contradiction
proof
  consider x being 1-ordered Nat such that not contradiction;
  1 is 0-ordered; then
  A1: x * x is 1-ordered; then
  consider x1 being 0-ordered Nat such that B1: x1 = x * x;
  A2: 1 < x1 by A1,B1; then
  x1 * x1 is x1-ordered by XREAL_1:155; then :: 0 < a & 1 < b -> a < a*b
  consider x2 being x1-ordered Nat such that B2: x2 = x1 * x1;
  ...
  consider x31 being x1-ordered Nat such that B31: x31 = x30 * x30;
  consider x32 being x1-ordered Nat such that B32: x32 = x31 * x31;
  C: x32 * x1 = x1 by
    B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,B11,B12,B13,B14,B15,B16,
    B17,B18,B19,B20,B21,B22,B23,B24,B25,B26,B27,B28,B29,B30,B31,B32;
  x32 is x1-ordered implies x1 < x32;
  then 0 < x1 & 1 < x32 by A2,XXREAL_0:2; :: a <= b & b <= c -> a <= c
  hence contradiction by C,XREAL_1:155;   :: 0 < a & 1 < b -> a < a*b
end;

   As mentioned earlier, there is a module in the equalizer for polynomial evaluation.
This means that each expression which is a complex number will also be expressed as
a polynomial in terms of basic variables, and two expressions which compute to equal

  7
    The full proof can be found at
https://github.com/digama0/mizar-rs/blob/itp2023-2/itp2023/false1/false1.miz.



                                                 19
polynomials will be equated. This is how things like −(a + b) = −a + −b are proved
automatically by the checker.                P Q n
    These polynomials are of the form i ci j xi,ji,j , and the starting point for this
proof was the discovery that the ni,j are represented as signed 32-bit integers and
overﬂow is not checked. Turning this into an exploit is surprisingly diﬃcult however,
                                               32
because one cannot simply write down x2 because the power function is not one of the
requirements (see section 3.3). The best thing we have for creating larger polynomials
                                            32
is multiplication, but we can get to x2 with 32 steps of repeated squaring, which is
what the large block of consider statements is doing.
                                                                                   30
    So the strategy is to construct x1 = x2 , x2 = x4 , all the way up to x30 = x2 . After
                                                31
this things start to get weird: x31 = x−2 because of signed overﬂow, and x32 = x0 .
The system does not recognize x32 = 1 however, because it maintains an invariant of
monomial powers being nonzero, and single powers are also handled specially, so we
have to go up to x32 · x1 = x2 . Since x1 is also x2 , the system will equate x32 · x1 = x1
which is the key step C. After this, we simply need to separately prove that since
                     32
x32 · x1 is really x2 +2 , it is strictly larger than x1 = x2 as long as we choose x > 1.
    To prove this last fact we use the attribute inference mechanism to prove that all
of the intermediates are strictly greater than x1 , since x1 < a implies x1 < a · a as
long as x1 > 1. Hence 1 < x1 < x32 so x1 < x32 · x1 = x1 , which is a contradiction.

7.2 Exhibit 2: negation in the schematizer
This one requires absolutely no imports; we include the complete proof below including
the import section.
environ begin

scheme Foo{P[set,set]}: P[1,1] implies P[1,1]
proof thus thesis; end;

theorem contradiction
proof
  1 = 1 implies 1 <> 1 from Foo;
  hence thesis;
end;

    This deﬁnes a very trivial scheme which just says that P (1, 1) implies P (1, 1).
The interesting part is the instantiation of this scheme in the main proof. In the
schematizer, we do not negate the thesis and try to prove false, we just directly match
the thesis against the goal. It does not attempt any fancy higher-order uniﬁcation: if it
                   → ?
                   −           →
                               −                                                     ?
needs to unify P ( ti ) = ±R( ti ′ ) it will just assign P := ±R and proceed with ti = t′i
for each i. Or at least it should do that, but there is a bug wherein it instead assigns
P := R and ignores the ± part, so we can trick it into unifying P (x, y) := (x = y) and
                          ?
then think that P (x, y) = (x 6= y) is still true. So we use 1 = 1 to prove 1 6= 1 and
then prove a contradiction.




                                            20
7.3 Exhibit 3: flex-and unfolding

theorem contradiction
proof
  (1 = 1 or 1 = 1) & ... & (2 = 1 or 1 = 1);
  hence thesis;
end;

    This one is bewilderingly short. We start by asserting a (true) ﬂex-and statement
V2
  i=1 (i = 1 ∨ 1 = 1). We prove this by using the forall expansion of the ﬂex-and,
∀i : N. 1 ≤ i ≤ 2 → i = 1 ∨ 1 = 1, which is of course true because the 1 = 1 disjunct
is provable.
    The second part is simply hence contradiction
                                             V2      , so we are calling the checker to
disprove the same statement. So we assume i=1 (i = 1 ∨ 1 = 1) and one of the things
the pre-checker does here is to expand out the conjunction, and we would expect it to
produce (1 = 1 ∨ 1 = 1) ∧ (2 = 1 ∨ 1 = 1) from which no contradiction can be found.
However, what it actually produces is 1 = 1 ∧ 2 = 1, which can be disproved.
    To see why this happens, we have to look more speciﬁcally at the forall-expansion
without the negation sugar employed thus far. What Mizar actually sees for the expan-
sion of the ﬂex-and expression is ∀i : N. ¬(1 ≤ i ∧ i ≤ 2 ∧ (i 6= 1 ∧ 1 6= 1)), except
that as mentioned previously conjunctions are always ﬂattened into their parents. The
code for expanding ﬂex-and expects the expansion body to be the third conjunct past
the forall and negation, but after ﬂattening the third conjunct is actually i 6= 1 and
there is an unexpected fourth conjunct 1 6= 1 that is forgotten.

7.4 Exhibit 4: flex-and substitution
This is the most worrisome of the bugs that have been presented, because it is not
simply a bad line of code but rather an issue with the algorithm itself. As a result,
this one survived the translation to Rust and was discovered to aﬀect both versions,
and moreover the ﬁx could not be rolled out without breaking the MML. The MML
maintainers have stepped up and ﬁxed the proofs though after we brought this issue
to their attention, so we were able to successfully excise this bug from both Mizar
implementations.
theorem contradiction
proof
  A: now
    let n be Nat;
    assume n > 3 & (1 + 1 <> 3 & ... & n <> 3);
    hence contradiction;
  end;
  ex n being Nat st n > 3 & (1 + 1 <> 3 & ... & n <> 3)
  proof
    take 2 + 2;
    thus 2 + 2 > 3 & (1 + 1 <> 3 & ... & 2 + 2 <> 3);
  end;



                                          21
  hence thesis by A;
end;

     To explain what is happening here, we have to talk about another aspect of ﬂex-
             Vb which was not mentioned in section 3.1, which is that a ﬂex-and
and expressions
expression i=a ϕ(i) is actually stored as ﬁve pieces of information: the bounds a and
b, the expansion ∀i : N. a ≤ i ≤ b → ϕ(i), from which ϕ(i) can be reconstructed (if
one is careful – see section 7.3), and the bounding expressions ϕ(a) and ϕ(b). As the
reader may have noticed, the syntax of Mizar very much prefers to only discuss the
bounding expressions, since ﬂex-and expressions in the concrete syntax are written as
ϕ(a) ∧ · · · ∧ ϕ(b) with literal dots, and no place to supply a, b or ϕ(i).
     When one writes an expression like P ∧ · · · ∧ Q, Mizar essentially diﬀs the two
expressions to determine what is changing and what the values are on each side. So
if one writes 1 + 1 6= 3 ∧ · · · ∧ n 6= 3 then Mizar infers that the desired expression is
V  n
   i=1+1 i 6= 3.
     The problem is that this operation is not stable under substitution.
                                                               V2+2         If we take that
expression and substitute n := 2 + 2, then we end up with i=1+1 i 6= 3, but if we were
                                                                             V2
to write out 1 + 1 6= 3 ∧ · · · ∧ 2 + 2 6= 3 ourselves we would end up with i=1 i + i 6= 3
instead. This is somewhat annoying, especially if one is trying to write an exploit
example, but it’s not obviously a soundness bugVyet because internally   V2     we are still
                                                         2+2
storing the expansion which has all the details – i=1+1 i 6= 3 and i=1 i + i 6= 3 are
diﬀerent expressions.
     However, the equality check between two ﬂex-and expressions is simply ϕ(a) =
ϕ′ (a) and ϕ(b) = ϕ′ (b)! The example above is crafted to demonstrate that this is not
                          V2+2                         V2
sound in general, since i=1+1 i 6= 3 is false but i=1 i + i 6= 3Vis true.
                                                                     n
     In the ﬁrst part of the proof we show that ∀n. ¬(n > 3 ∧ i=1+1 i 6= 3), which is
true. The interesting partVis the second half, where we take n := 2 + 2. At this point
                               2+2
the thesis is 2 + 2 > 3 ∧ i=1+1 i 6= 3, but we cannot write this expression. What we
write instead is 2 + 2 > 3 ∧ (1 + 1 6= 3 ∧ · · · ∧ 2 + 2 6= 3), which as mentioned will be
                                V
interpreted as 2 + 2 > 3 ∧ 2i=1 i + i 6= 3. This should be rejected for not matching
the thesis, but it has the same endpoints so it is accepted, and the checker is able
to prove it by case analysis. If we were to write thus thesis to let Mizar insert the
unmentionable proposition, then the analyzer will accept it as being the right thesis
but the checker will not be able to prove it.

7.5 Honorable mention: attributes that don’t exist
This is not an exploitable bug to my knowledge, but it is notable for being widespread,
and it is diﬃcult for mizar-rs to support without resulting in very weird behavior.8
Consider the following Mizar article:
environ
  vocabularies ZFMISC_1, SUBSET_1;
  notations ZFMISC_1, SUBSET_1;
  constructors TARSKI, SUBSET_1;

 8
     It is also the only bug among those discussed here which is not fixed in the latest version (8.1.14).



                                                      22
  requirements SUBSET; ::, BOOLE;
begin
for x,B being set, A being Element of bool B st x in A holds x in B;

This checks as one would expect, and it is in fact a true statement (and it is not at
all contrived). However, the reasoning that gets the checker to accept the proof is. . .
somewhat suspicious. It goes as follows:
1. Suppose A : Element(P(B)), x ∈ A and x ∈ / B.
2. Because A : Element(P(B)) and x ∈ A, it follows that B is not empty and x :
   Element(B).
3. Because x ∈
             / B, B is not empty, and x : Element(B), contradiction.
Because the example has been minimized, there is really not much going on in the
proof because these are all essentially primitive inferences. The problem here is “B is
not empty”, because the BOOLE requirement which supplies the B is not empty pred-
icate is not available (note the environment section). The constructor for empty is
actually available in the environment because it has been brought in indirectly via the
constructors SUBSET_1 directive, but without the requirement the checker just sees it
as a normal attribute.
    So what, then, is the checker doing? This seems to be a case of multiple bugs
cancelling each others’ eﬀects. Requirements are internally represented by an integer
index, where zero means that the requirement is not available. Normally any handling
of a requirement involves a check that the requirement is nonzero ﬁrst, but we forget
that in step 2, and as a result we end up adding attribute 0 to B, which is meaningless.
The second bug is in step 3, where we again forget to ask whether the requirement
index is nonzero, and so we ﬁnd attribute 0 and interpret it (correctly) as meaning
that B is not empty.
    This would just be a curious bug, but for the fact that it is exploited all over
the place because when creating articles it is standard to minimize the environment
section by removing anything that keeps the proof valid, and this bug allows one to
remove the BOOLE requirement without breaking the proof. We had to patch 46 articles
that all had this same issue. In all cases we only need to add the BOOLE requirement
to ﬁx the issue.

                                                                     Table 1 Line counts by
8 Results                                                            category in mizar-rs.

The whole project is 28 592 lines of code (see ﬁgure 1), or            category     lines
13 631 if we restrict attention to those ﬁles used in the checker,
which is 1/2 to 1/3 of the equivalent code in Pascal (see              accom.        613
ﬁgure 2). We credit this mainly to the language itself – Rust          parser       2781
is able to express many complex patterns that would be sig-            analyzer     6353
niﬁcantly more verbose to write in Pascal, and PC Mizar is             checker     13631
also written in a fairly OOP-heavy style that necessitates a           general      5214
lot of boilerplate. Furthermore, Pascal is manually memory-            total       28592
managed while Rust uses “smart-pointer” style automatic



                                             23
                       y = 4.93 x                                             1000
                                                                                        y = 4.93 x
           120
                       y =x                                                             y =x

           100                                                                100




verifier




                                                                   verifier
           80
                                                                               10


           60
                                                                                1

           40

                                                                              0.10
           20



            0                                                                 0.01
                 0            5     10          15    20                        0.001    0.010       0.100         1           10      100

                                     mizar-rs                                                                mizar-rs

Fig. 2 Scatter plot of files in the MML based on check time in verifier (vertical axis) vs. in mizar-
rs (horizontal axis), in seconds. The left plot is linear and the right is log-log (including some outliers
not in the left plot). The blue line is the best fit, indicating an average 4.93× speedup, and the gray
dashed line is a 1× reference; there are no points below this line, indicating that mizar-rs was never
slower than verifier on this run.

Table 2 Comparison of the original (Pascal) implementation of Mizar with mizar-rs (Rust). Tests
were performed on a 12 core 12th Gen Intel Core i7-1255U @ 2.20GHz, with 12 threads. The times
are measured in CPU minutes, and the “par.” column gives the observed parallelism as a ratio
between real time and CPU time (e.g. a full mizar-rs run takes 167.58
                                                                   10.1
                                                                         = 16.62 min of real time),
which is roughly constant because all tasks have ample concurrency. (Note that prel/ is
precalculated before the runs, so that all articles can be processed in parallel.)

                                                           PC Mizar                                  mizar-rs

                     Enabled passes                  CPU time                   par.           CPU time                 par.        ratio
        analyzer                                     129.90 min                 9.70         15.34 min                  9.54        8.47×
accom + analyzer                                     141.43 min                 9.35         13.80 min                  10.3        10.2×
                                  checker            698.58 min                 10.2        142.75 min                  9.69        4.89×
                       analyzer + checker            748.40 min                 10.5        165.00 min                  10.2        4.54×
accom + analyzer + checker                           798.38 min                 9.55        167.58 min                  10.1        4.76×


memory management, so all the destructors simply don’t need to be written which
decreases verbosity and eliminates many memory bugs.
    The performance improvements are most striking: we measured almost 5× reduc-
tion in processing time to check the MML. See Figure 2. This is most likely a
combination of characteristics of the LLVM compiler pipeline, along with many small
algorithmic improvements and removing redundant work. (The reduction is even larger
when adding the other phases of the Mizar system – accom, parser, MSM – so that
we can skip the costly I/O and serialization steps of section 2.)

9 Conclusion & Future work
We have implemented a drop-in replacement for the verifier checker of the Mizar
system that is able to check the entire MML, which gets a signiﬁcant performance
improvement. Furthermore, we have improved Mizar by uncovering and reporting some
soundness bugs.


                                                              24
    While this implementation is explicitly trying not to diverge from the Mizar lan-
guage as deﬁned by the PC Mizar implementation and the MML, there are many
possible areas where improvements are possible to remove unintentional or undesirable
restrictions. For example, anyone who has played with Mizar will have undoubtedly
noticed that all the article names are 8 letters or less, for reasons baked deeply into
PC Mizar. Should mizar-rs become the oﬃcial Mizar implementation, it would be
possible to lift this restriction without much diﬃculty.
    This project was also originally started to get proof export from Mizar, and to that
end replacing one large trusted tool with another one does not seem like much of an
improvement. But (bugs notwithstanding) we saw nothing while auditing the checker
that is not proof-checkable or unjustiﬁed, and remain conﬁdent that proof export is
possible.

References
 [1] Bancerek, G., Byliński, C., Grabowski, A., Korniłowicz, A., Matuszewski, R.,
     Naumowicz, A., Pak, K., Urban, J.: Mizar: State-of-the-art and beyond. In: Intelli-
     gent Computer Mathematics: International Conference, CICM 2015, Washington,
     DC, USA, July 13-17, 2015, Proceedings., pp. 261–279 (2015). Springer

 [2] Bancerek, G., Byliński, C., Grabowski, A., Korniłowicz, A., Matuszewski, R.,
     Naumowicz, A., Pąk, K.: The role of the Mizar Mathematical Library for inter-
     active proof development in Mizar. Journal of Automated Reasoning 61, 9–32
     (2018)

 [3] Grabowski, A., Korniłowicz, A., Naumowicz, A.: Mizar in a nutshell. Journal of
     Formalized Reasoning 3(2), 153–245 (2010)

 [4] Muzalewski, M.: An Outline of PC Mizar. Fondation Philippe le Hodey, ???
     (1993)

 [5] Carneiro, M.: The Divergence of the Sum of Prime Reciprocals. Formalized
     Mathematics 30(3), 209–210 (2022) https://doi.org/10.2478/forma-2022-0015

 [6] Matuszewski, R., Rudnicki, P.: Mizar: the ﬁrst 30 years. Mechanized mathematics
     and its applications 4(1), 3–24 (2005)

 [7] Harrison, J.: A Mizar Mode for HOL. In: Wright, J., Grundy, J., Harrison, J.
     (eds.) Theorem Proving in Higher Order Logics: 9th International Conference,
     TPHOLs’96. Lecture Notes in Computer Science, vol. 1125, pp. 203–220. Springer,
     Turku, Finland (1996)

 [8] Urban, J.: MPTP 0.2: Design, implementation, and initial experiments. Journal
     of Automated Reasoning 37, 21–43 (2006)

 [9] Kaliszyk, C., Pąk, K.: Semantics of Mizar as an Isabelle object logic. Journal of
     Automated Reasoning 63, 557–595 (2019)


                                          25
[10] Urban, J.: XML-izing Mizar: Making Semantic Processing and Presentation
     of MML Easy. In: Kohlhase, M. (ed.) Mathematical Knowledge Management,
     4th International Conference, MKM 2005, Bremen, Germany, July 15-17, 2005,
     Revised Selected Papers. Lecture Notes in Computer Science, vol. 3863, pp. 346–
     360. Springer, ??? (2005). https://doi.org/10.1007/11618027_23 . https://doi.
     org/10.1007/11618027_23

[11] Bylinski, C., Alama, J.: New Developments in Parsing Mizar. In: Jeuring, J.,
     Campbell, J.A., Carette, J., Dos Reis, G., Sojka, P., Wenzel, M., Sorge, V. (eds.)
     Intelligent Computer Mathematics, pp. 427–431. Springer, Berlin, Heidelberg
     (2012)

[12] Cairns, P., Gow, J.: Using and parsing the mizar language. Electronic Notes
     in Theoretical Computer Science 93, 60–69 (2004) https://doi.org/10.1016/j.
     entcs.2003.12.028 . Proceedings of the Mathematical Knowledge Management
     Symposium

[13] Nakasho, K.: Development of a Flexible Mizar Tokenizer and Parser for Infor-
     mation Retrieval System. In: 2019 Federated Conference on Computer Science
     and Information Systems (FedCSIS), pp. 77–80 (2019). https://doi.org/10.15439/
     2019F151

[14] Adams, M.M.: Proof auditing formalised mathematics. Journal of Formalized
     Reasoning 9(1), 3–32 (2016)

[15] Kunčar, O., Popescu, A.: A consistent foundation for Isabelle/HOL. In: Interac-
     tive Theorem Proving: 6th International Conference, ITP 2015, Nanjing, China,
     August 24-27, 2015, Proceedings 6, pp. 234–252 (2015). Springer




                                          26
