                                                      Program Synthesis in Saturation

                                             Petra Hozzová1     ( ), Laura Kovács1 , Chase Norman2 , and Andrei
                                                                           Voronkov3,4
                                                                  petra.hozzova@tuwien.ac.at
arXiv:2402.18962v1 [cs.LO] 29 Feb 2024




                                                                                1
                                                                               TU Wien
                                                                            2
                                                                              UC Berkeley
                                                                      3
                                                                        University of Manchester
                                                                            4
                                                                               EasyChair



                                               Abstract. We present an automated reasoning framework for synthe-
                                               sizing recursion-free programs using saturation-based theorem proving.
                                               Given a functional specification encoded as a first-order logical formula,
                                               we use a first-order theorem prover to both establish validity of this for-
                                               mula and discover program fragments satisfying the specification. As a
                                               result, when deriving a proof of program correctness, we also synthesize
                                               a program that is correct with respect to the given specification. We de-
                                               scribe properties of the calculus that a saturation-based prover capable
                                               of synthesis should employ, and extend the superposition calculus in a
                                               corresponding way. We implemented our work in the first-order prover
                                               Vampire, extending the successful applicability of first-order proving to
                                               program synthesis.
                                               This is an extended version of an Automated Deduction – CADE 29
                                               paper with the same title and the same authors.

                                               Keywords: Program Synthesis · Saturation · Superposition · Theorem
                                               Proving.


                                         1   Introduction
                                         Program synthesis constructs code from a given specification. In this work we
                                         focus on synthesis using functional specifications summarized by valid first-order
                                         formulas [13,1], ensuring that our programs are provably correct. While being a
                                         powerful alternative to formal verification [19], synthesis faces intrinsic compu-
                                         tational challenges. One of these challenges is posed to the reasoning backend
                                         used for handling program specifications, as the latter typically include first-
                                         order quantifier alternations and interpreted theory symbols. As such, efficient
                                         reasoning with both theories and quantifiers is imperative for any effort towards
                                         program synthesis.
                                             In this paper we address this demand for recursion-free programs. We advo-
                                         cate the use of first-order theorem proving for extracting code from correctness
                                         proofs of functional specifications given as first-order formulas ∀x.∃y.F [x, y].
                                         These formulas state that “for all (program) inputs x there exists an output
                                         y such that the input-output relation (program computation) F [x, y] is valid”.
2        Hozzová et al.

Given such a specification, we synthesize a recursion-free program while also
deriving a proof certifying that the program satisfies the specification.
    The programs we synthesize are built using first-order theory terms extended
with if−then−else constructors. To ensure that our programs yield computa-
tional models, i.e., that they can be evaluated for given values of input variables
x, we restrict the programs we synthesize to only contain computable symbols.

Our approach in a nutshell. In order to synthesize a recursion-free pro-
gram, we prove its functional specification using saturation-based theorem prov-
ing [14,10]. We extend saturation-based proof search with answer literals [5],
allowing us to track substitutions into the output variable y of the specification.
These substitutions correspond to the sought program fragments and are condi-
tioned on clauses they are associated with in the proof. When we derive a clause
corresponding to a program branch if C then r, where C is a condition and
r a term and both C, r are computable, we store it and continue proof search
assuming that ¬C holds; we refer to such conditions C as (program) branch
conditions. The saturation process for both proof search and code construction
terminates when the conjunction of negations of the collected branch conditions
becomes unsatisfiable. Then we synthesize the final program satisfying the given
(and proved) specification by assembling the recorded program branches (see
e.g. Examples 1-3).
    The main challenges of making our approach effective come with (i) inte-
grating the construction of the programs with if − then− else into the proof
search, turning thus proof search into program search/synthesis, and (ii) guiding
program synthesis to only computable branch conditions and programs.

Contributions. We bring the next contributions solving the above challenges:5

• We formalize the semantics for clauses with answer literals and introduce a
 saturation-based algorithm for program synthesis based on this semantics. We
 prove that, given a sound inference system, our saturation algorithm derives
 correct and computable programs (Section 4).
• We define properties of a sound inference calculus in order to make the cal-
 culus suitable for our saturation-based algorithm for program synthesis. We
 accordingly extend the superposition calculus and define a class of substitu-
 tions to be used within the extended calculus; we refer to these substitutions
 as computable unifiers (Section 5).
• We extend a first-order unification algorithm to find computable unifiers (Sec-
 tion 6) to be further used in saturation-based program synthesis.
• We implement our work in the Vampire prover [10] and evaluate our synthesis
 approach on a number of examples, complementing other techniques in the area
 (Section 7). For example, our results demonstrate the applicability of our work
 on synthesizing programs for specifications that cannot be even encoded in the
 SyGuS syntax [15].

5
    proofs of our results are given in Appendix A
                                            Program Synthesis in Saturation        3

2     Preliminaries

We assume familiarity with standard multi-sorted first-order logic with equality.
We denote variables by x, y, terms by s, t, atoms by A, literals by L, clauses
by C, D, formulas by F, G, all possibly with indices. Further, we write σ for
Skolem constants. We reserve the symbol  for the empty clause which is log-
ically equivalent to ⊥. Formulas and clauses with free variables are considered
implicitly universally quantified (i.e. we consider closed formulas). By ≃ we de-
note the equality predicate and write t 6≃ s as a shorthand for ¬t ≃ s. We
use a distinguished integer sort, denoted by Z. When we use standard integer
predicates <, ≤, >, ≥, functions +, −, . . . and constants 0, 1, . . . , we assume
that they denote the corresponding interpreted integer predicates and functions
with their standard interpretations. Additionally, we include a conditional term
constructor if−then−else in the language, as follows: given a formula F and
terms s, t of the same sort, we write if F then s else t to denote the term s if
F is valid and t otherwise.
    An expression is a term, literal, clause or formula. We write E[t] to denote
that the expression E contains the term t. For simplicity, E[s] denotes the ex-
pression E where all occurrences of t are replaced by the term s. A substitution
θ is a mapping from variables to terms. A substitution θ is a unifier of two ex-
pressions E and E ′ if Eθ = E ′ θ, and is a most general unifier (mgu) if for every
unifier η of E and E ′ , there exists substitution µ such that η = θµ. We denote
the mgu of E and E ′ with mgu(E, E ′ ). We write F1 , . . . , Fn ⊢ G1 , . . . , Gm to
denote that F1 ∧ . . . ∧ Fn → G1 ∨ . . . ∨ Gm is valid, and extend the notation also
to validity modulo a theory T . Symbols occurring in a theory T are interpreted
and all other symbols are uninterpreted.


2.1    Computable Symbols and Programs

We distinguish between computable and uncomputable symbols in the signature.
The set of computable symbols is given as part of the specification. Intuitively,
a symbol is computable if it can be evaluated and hence is allowed to occur
in a synthesized program. A term or a literal is computable if all symbols it
contains are computable. A symbol, term or literal is uncomputable if it is not
computable.
   A functional specification, or simply just a specification, is a formula

                                   ∀x.∃y.F [x, y].                               (1)

The variables x of a specification (1) are called input variables. Note that while
we use specifications with a single variable y, our work can analogously be used
with a tuple of variables y in (1).
   Let σ denote a tuple of Skolem constants. Consider a computable term r[σ]
such that the instance F [σ, r[σ]] of (1) holds. Since σ are fresh Skolem constants,
the formula ∀x.F [x, r[x]] also holds; we call such r[x] a program for (1) and say
that the program r[x] computes a witness of (1).
4         Hozzová et al.


                                               Superposition:

    s ≃ t∨C         L[s′ ] ∨ C ′      s≃t∨C           u[s′ ] 6≃ u′ ∨ C ′    s≃t∨C     u[s′ ] ≃ u′ ∨ C ′
       (L[t] ∨ C ∨ C ′ )θ                (u[t] 6≃ u′ ∨ C ∨ C ′ )θ            (u[t] ≃ u′ ∨ C ∨ C ′ )θ

    where θ := mgu(s, s′ ); tθ 6 sθ; (first rule only) L[s′ ] is not an equality literal; and
    (second and third rules only) u′ θ 6 u[s′ ]θ.
Binary resolution:                 Factoring:         Equality resolution: Equality factoring:

    A ∨ C ¬A ∨ C′        ′
                                    A∨A ∨C′                    s 6≃ t ∨ C         s ≃ t ∨ s′ ≃ t′ ∨ C
       (C ∨ C ′ )θ                  (A ∨ C)θ                       Cθ            (s ≃ t ∨ t 6≃ t′ ∨ C)θ

          where                         where           where θ := mgu(s, t).    where θ := mgu(s, s′ );
     θ := mgu(A, A′ ).             θ := mgu(A, A′).                              tθ 6 sθ; and t′ θ 6 tθ.


                               Fig. 1. The superposition calculus Sup.


     Further, if ∀x.(F1 ∧ . .V   . ∧ Fn → F [x, r[x]]) holds for computable formulas
F1 , . . . , Fn , we write hr[x], ni=1 Fi i to refer to a program with conditions F1 , . . . ,
Fn for (1). In the sequel, we refer to (parts of) programs with conditions also
as conditional branches. In Section 4 we show how to build programs for (1) by
composing programs with conditions for (1) (see Corollary 3).


2.2     Saturation and Superposition

Saturation-based proof search implements proving by refutation [10]: to prove
validity of F , a saturation algorithm establishes unsatisfiability of ¬F . First-
order theorem provers work with clauses, rather than with arbitrary formulas. To
prove a formula F , first-order provers negate F which is further skolemized and
converted to clausal normal form (CNF). The CNF of ¬F is denoted by cnf(¬F )
and represents a set S of initial clauses. First-order provers then saturate S by
computing logical consequences of S with respect to a sound inference system
I. The saturated set of S is called the closure of S and the process of computing
the closure of S is called saturation. If the closure of S contains the empty clause
, the original set S of clauses is unsatisfiable, and hence the formula F is valid.
    We may extend the set S of initial clauses with additional clauses C1 , . . . , Cn .
If C is derived by saturating this extended set, we say C is derived from S under
additional assumptions C1 , . . . , Cn .
    The superposition calculus, denoted as Sup and given in Figure 1, is the
most common inference system used by saturation-based provers for first-order
logic with equality [14]. The Sup calculus is parametrized by a simplification
ordering ≻ on terms and a selection function, which selects in each non-empty
clause a non-empty subset of literals (possibly also positive literals). We denote
selected literals by underlining them. An inference rule can be applied on the
given premise(s) if the literals that are underlined in the rule are also selected
                                               Program Synthesis in Saturation           5

in the premise(s). For a certain class of selection functions, the superposition
calculus Sup is sound (if  is derived from F , then F is unsatisfiable) and
refutationally complete (if F is unsatisfiable, then  can be derived from it).

2.3    Answer Literals
Answer literals [5] provide a question answering technique for tracking substi-
tutions into given variables throughout the proof. Suppose we want to find a
witness for the validity of the formula

                                        ∃y.F [y].                                      (2)

Within saturation-based proving, we first derive the skolemized negation of (2)
and add an answer literal using a fresh predicate ans with argument y, yielding

                                 ∀y.(¬F [y] ∨ ans(y)).                                 (3)

We then saturate the CNF of (3), while ensuring that answer literals are not
selected for performing inferences. If the clause ans(t1 ) ∨ . . . ∨ ans(tm ) is derived
during saturation, note that this clause contains only answer literals in addition
to the empty clause; hence, in this case we proved unsatisfiability of ∀y.¬F [y],
implying validity of (2). Moreover, t1 , . . . , tm provides a disjuntive answer, i.e.
witness, for the validity of (2); that is, F [t1 ]∨. . .∨F [tm ] holds [11]. In particular,
if we derive the clause ans(t) during saturation, we found a definite answer t
for (2), namely F [t] is valid.
Answer literals with if−then−else. The derivation of disjunctive answers
can be avoided by modifying the inference rules to only derive clauses containing
at most one answer literal. One such modification is given within the A(R)-
calculus for binary resolution [21], where R is a so-called strongly liftable term
restriction. The A(R)-calculus replaces the binary resolution rule when both
premises contain an answer literal by the following A-resolution rule:
               A ∨ C ∨ ans(r) ¬A′ ∨ C ′ ∨ ans(r′ )
                                                    (A-resolution),
              (C ∨ C ′ ∨ ans(if A then r′ else r))θ
where θ := mgu(A, A′ ) and the restriction R(if A then r′ else r) holds.
    In our work we go beyond the A-resolution rule and modify both the super-
position calculus and the saturation algorithm to reason not only about answer
literals but also about their use of if−then−else terms (see Sections 4–5).


3     Illustrative Example
Let us illustrate our approach to program synthesis. We use answer literals in sat-
uration to construct programs with conditions while proving specifications (1).
By adding an answer literal to the skolemized negation of (1), we obtain

                                ∀y.(¬F [σ, y] ∨ ans(y)),                               (4)
6         Hozzová et al.


    ∀x. i(x) ∗ x ≃ e (A1)     ∀x. e ∗ x ≃ x (A2)       ∀x, y, z. x∗(y∗z) ≃ (x∗y)∗z (A3)

Fig. 2. Axioms defining a group. Uninterpreted function symbols i(·), e, ∗ represent the
inverse, the identity element, and the group operation, respectively.



where σ are the skolemized input variables x. When we derive a unit clause
ans(r[σ]) during saturation, where r[σ] is a computable term, we construct a
program for (1) from the definite answer r[σ] by replacing σ with the input
variables x, obtaining the program r[x]. Hence, deriving computable definite
answers by saturation allows us to synthesize programs for specifications.

Example 1. Consider the group theory axioms (A1)–(A3) of Figure 2. We are
interested in synthesizing a program for the following specification:

                                    ∀x.∃y. x ∗ y ≃ e                                  (5)

In this example we assume that all symbols are computable. To synthesize a
program for (5), we add an answer literal to the skolemized negation of (5) and
convert the resulting formula to CNF (preprocessing). We consider the set S of
clauses containing the obtained CNF and the axioms (A1)-(A3). We saturate S
using Sup and obtain the following derivation:6

 1. σ ∗ y 6≃ e ∨ ans(y)                                    [preprocessed specification]
 2. i(x) ∗ (x ∗ y) ≃ e ∗ y                                               [Sup A1, A3]
 3. i(x) ∗ (x ∗ y) ≃ y                                                    [Sup A2, 2.]
 4. x ∗ y ≃ i(i(x)) ∗ y                                                    [Sup 3., 3.]
 5. e ≃ x ∗ i(x)                                                          [Sup 4., A1]
 6. ans(i(σ))                                                               [BR 5., 1.]

Using the above derivation, we construct a program for the functional specifi-
cation (5) as follows: we replace σ in the definite answer i(σ) by x, yielding the
program i(x). Note that for each input x, our synthesized program computes the
inverse i(x) of x as an output. In other words, our synthesized program for (5)
ensures that each group element x has a right inverse i(x).

    While Example 1 yields a definite answer within saturation-based proof
search, our work supports the synthesis of more complex recursion-free programs
(see Examples 2–3) by composing program fragments derived in the program
search (Section 4) as well as by using answer literals with if − then− else to
effectively handle disjunctive answers (Section 5).
6
    For each formula in the derivation, we also list how the formula has been derived. For
    example, formula 5 is the result of superposition (Sup) with formula 4 and axiom A1,
    whereas binary resolution (BR) has been used to derive formula 6 from 5 and 1.
                                                  Program Synthesis in Saturation       7

4     Program Synthesis with Answer Literals

We now introduce our approach to saturation-based program synthesis using
answer literals (Algorithm 1). We focus on recursion-free program synthesis and
present our work in a more general setting. Namely, we consider functional spec-
ifications whose validity may depend on additional assumptions (e.g. additional
program requirements) A1 , . . . , An , where each Ai is a closed formula:

                            A1 ∧ . . . ∧ An → ∀x.∃y.F [x, y]                          (6)

Note that specification (1) is a special case of (6). However, since A1 , . . . , An are
closed formulas, (6) is equivalent to ∀x.∃y.(A1 ∧ . . . ∧ An → F [x, y]), which is a
special case of (1).
    Given a functional specification (6), we use answer literals to synthesize pro-
grams with conditions (Section 4.1) and extend saturation-based proof search
to reason about answer literals (Section 4.2). For doing so, we add the answer
literal ans(y) to the skolemized negation of (6) and obtain

                      A1 ∧ . . . ∧ An ∧ ∀y.(¬F [σ, y] ∨ ans(y)).                      (7)

We saturate the CNF of (7), while ensuring that answer literals are not selected
within the inference rules used in saturation. We guide saturation-based proof
search to derive clauses C[σ] ∨ ans(r[σ]), where C[σ] and r[σ] are computable.


4.1   From Answer Literals to Programs

Our next result ensures that, if we derive the clause C[σ] ∨ ans(r[σ]), the term
r[σ] is a definite answer under the assumption ¬C[σ] (Theorem 1). We note that
we do not terminate saturation-based program synthesis once a clause C[σ] ∨
ans(r[σ]) is derived. We rather record the program r[x] with condition ¬C[x]
(and possibly also other conditions), replace clause C[σ] ∨ ans(r[σ]) by C[σ], and
continue saturation (Corollary 2). As a result, upon establishing validity of (6),
we synthesized a program for (6) (Corollary 3).

Theorem 1 [Semantics of Clauses with Answer Literals] Let C be a
clause not containing an answer literal. Assume that, using a saturation algo-
rithm based on a sound inference system I, the clause C ∨ ans(r[σ]) is derived
from the set of clauses consisting of initial assumptions A1 , . . . , An , the clausified
formula cnf(¬F [σ, y] ∨ ans(y)) and additional assumptions C1 , . . . , Cm . Then,

                       A1 , . . . , An , C1 , . . . , Cm ⊢ C, F [σ, r[σ]].

That is, under the assumptions C1 , . . . , Cm , ¬C, the computable term r[σ] pro-
vides a definite answer to (6).

We further use Theorem 1 to synthesize programs with conditions for (6).
8       Hozzová et al.

Corollary 2 [Programs with Conditions] Let r[σ] be a computable term
and C[σ] a ground computable clause not containing an answer literal. Assume
that clause C[σ] ∨ ans(r[σ]) is derived from the set of initial clauses A1 , . . . , An ,
the clausified formula cnf(¬F [σ, y] ∨ ans(y)) and additional ground computable
assumptions C1 [σ], . . . , Cm [σ], by using saturation based on a sound inference
system I. Then,
                                       m
                                       ^
                                hr[x],   Cj [x] ∧ ¬C[x]i
                                     j=1

is a program with conditions for (6).
                                                 Vm
    Note that a program with conditions hr[x], j=1 Cj [x] ∧ ¬C[x]i corresponds
                                          Vm
to a conditional (program) branch if j=1 Cj [x] ∧ ¬C[x] then r[x]: only if the
          Vm
condition j=1 Cj [x] ∧ ¬C[x] is valid, then r[x] is computed for (6).
                                             Vm
    We use programs with conditions hr[x], j=1 Cj [x] ∧ ¬C[x]i to finally synthe-
size a program for (6). To this end, we use Corollary 2 to derive programs with
conditions, and once their conditions cover all possible cases given the initial
assumptions A1 , . . . , An , we compose them into a program for (6).

Corollary 3 [From Programs with Conditions to Programs for (6)] Let
                                               Vi−1
P1 [x], . . . , Pk [x], where Pi [x] = hri [x], j=1 Cj [x] ∧ ¬Ci [x]i, be programs with
                                     Vn         Vk
conditions for (6), such that i=1 Ai ∧ i=1 Ci [x] is unsatisfiable. Then P [x],
given by

                      P [x] := if ¬C1 [x] then r1 [x]
                               else if ¬C2 [x] then r2 [x]
                                   ...                                               (8)
                               else if ¬Ck−1 [x] then rk−1 [x]
                               else rk [x],

is a program for (6).

Note that since the conditional branches of (8) cover all possible cases to be
considered
    Vn     over x, we do not need the condition if ¬Ck . In particular, if k = 1,
i.e. i=1 Ai ∧ C1 [x] is unsatisfiable, then the synthesized program for (6) is r1 [x].


4.2   Saturation-Based Program Synthesis

Our program synthesis results from Theorem 1, Corollary 2 and Corollary 3
rely upon a saturation algorithm using a sound (but not necessarily complete)
inference system I. In this section, we present our modifications to extend state-
of-the-art saturation algorithms with answer literal reasoning, allowing to derive
clauses C[σ]∨ans(r[σ]), where both C[σ] and r[σ] are computable. In Sections 5–
6 we then describe modifications of the inference system I to implement rules
over clauses with answer literals.
                                               Program Synthesis in Saturation           9

Algorithm 1 Saturation Loop for Recursion-Free Program Synthesis
1    initial set of clauses S := {cnf(A1 ∧ . . . ∧ An ∧ ∀y.(¬F [σ, y] ∨ ans(y)))}
2    initial sets of additional assumptions C := ∅ and programs P := ∅
3    repeat
4       Select clause G ∈ S
5       Derive consequences C1 , . . . , Cn of G and formulas from S using rules of I
6       for each Ci do
7         if Ci = (C[σ] ∨ ans(r[σ]))
                                  V      and C[σ] is ground and computable then
8            P := P ∪ {hr[x], C ′ ∈C C ′ ∧ ¬C[x]i}                        /* Corollary 2 */
9            C := C ∪ {C[x]}
10           Ci := C[σ]
11      S := S ∪ {C1 , . . . , Cn }
12      if  ∈ S then
13        return program (8) for specification (6), derived from P /* Corollary 3 */



    Our saturation algorithm is given in Algorithm 1. In a nutshell, we use Corol-
lary 2 to construct programs from clauses C[σ] ∨ ans(r[σ]) and replace clauses
C[σ] ∨ ans(r[σ]) by C[σ] (lines 7–10 of Algorithm 1). The newly added com-
putable assumptions C[σ] are used to guide saturation towards deriving pro-
grams with conditions where the conditions contain C[x]; these programs with
conditions are used for synthesizing programs for (6), as given in Corollary 3.
    Compared to a standard saturation algorithm used in first-order theorem
proving (e.g. lines 4–5 of Algorithm 1), Algorithm 1 implements additional steps
for processing newly derived clauses C[σ] ∨ ans(r[σ]) with answer literals (lines
6-10). As a result, Algorithm 1 establishes not only the validity of the specifica-
tion (6) but also synthesizes a program (lines 12-13). Throughout the algorithm,
we maintain a set P of programs with conditions derived so far and a set C of
additional assumptions. For each new clause Ci , we check if it is in the form
C[σ] ∨ ans(r[σ]) where C[σ] is ground and        V computable (line 7). If yes, we con-
struct a program with conditions hr[x], C ′ ∈C C ′ ∧ ¬C[x]i, extend C with the
additional assumption C[x], and replace Ci by C[σ] (lines 8-10). Then, when
we derive the empty clause, we construct the final program as follows. We first
collect all clauses that participated in the derivation of . We use this clause
collection to filter the programs in P – we only keep a program originating from
a clause C[σ] ∨ ans(r[σ]) if the condition C[σ] was used in the proof, obtaining
programs P1 , . . . , Pk . From P1 , . . . , Pk we then synthesize the final program P
using the construction (8) from Corollary 3.

Remark 1. Compared to [21] where potentially large programs (with conditions)
are tracked in answer literals, Algorithm 1 removes answer literals from clauses
and constructs the final program only after saturation found a refutation of the
negated (6). Our approach has two advantages: first, we do not have to keep
track of potentially many large terms using if−then−else, which might slow
down saturation-based program synthesis. Second, our work can naturally be
integrated with clause splitting techniques within saturation (see Section 7).
10      Hozzová et al.

5    Superposition with Answer Literals
We note that our saturation-based program synthesis approach is not restricted
to a specific calculus. Algorithm 1 can thus be used with any sound set of
inference rules, including theory-specific inference rules, e.g. [9], as long as the
rules allow derivation of clauses in the form C∨ans(r), where C, r are computable
and C is ground. I.e., the rules should only derive clauses with at most one answer
literal, and should not introduce uncomputable symbols into answer literals.
    In this section we present changes tailored to the superposition calculus Sup,
yet, without changing the underlying saturation process of Algorithm 1. We first
introduce the notion of an abstract unifier [16] and define a computable unifier –
a mechanism for dealing with the uncomputable symbols in the reasoning instead
of introducing them into the programs. The use of such a unifier in any sound
calculus is explained, with particular focus on the Sup calculus.
Definition 1 (Abstract unifier [16]). An abstract unifier of two expressions
E1 , E2 is a pair (θ, D) such that:
1. θ is a substitution and D is a (possibly empty) disjunction of disequalities,
2. (D ∨ E1 ≃ E2 )θ is valid in the underlying theory.
Intuitively speaking, an abstract unifier combines disequality constraints D with
a substitution θ such that the substitution is a unifier of E1 , E2 if the constraints
D are not satisfied.
Definition 2 (Computable unifier). A computable unifier of two expressions
E1 , E2 with respect to an expression E3 is an abstract unifier (θ, D) of E1 , E2
such that the expression E3 θ is computable.
    For example, let f be computable and g uncomputable. Then ({y 7→ f (z)},
z 6≃ g(x)) is a computable unifier of the terms f (g(x)), y with respect to f (y).
Further, ({y 7→ f (g(x))}, ∅) is an abstract unifier of the same terms, but not a
computable unifier with respect to f (y).
Ensuring computability of answer literal arguments. We modify the rules
of a sound inference system I to use computable unifiers with respect to the
answer literal argument instead of unifiers. Since a computable unifier may entail
disequality constraints D, we add D to the conclusions of the inference rules.
That is, for an inference rule of I as below
                                  C1    ···    Cn ,
                                        Cθ                                        (9)
where θ is a substitution such that Eθ ≃ E ′ θ holds for some expressions E, E ′ ,
we extend I with the following n inference rules with computable unifiers:
     C1 ∨ ans(r) C2 · · · Cn                  C1    C2 · · · Cn ∨ ans(r) ,
         (D ∨ C ∨ ans(r))θ′            ···         (D ∨ C ∨ ans(r))θ′            (10)
where (θ′ , D) is a computable unifier of E, E ′ with respect to r and none of
C1 , . . . , Cn contains an answer literal. We obtain the following result.
                                                            Program Synthesis in Saturation                     11


                                        Superposition (Sup):

       s ≃ t ∨ C ∨ ans(r)    L[s′ ] ∨ C ′ ∨ ans(r ′ )         s ≃ t ∨ C ∨ ans(r)    L[s′ ] ∨ C ′ ∨ ans(r ′ )
  (D ∨ L[t] ∨ C ∨ C ′ ∨ ans(if s ≃ t then r ′ else r))θ        (D ∨ r 6≃ r ′ ∨ L[t] ∨ C ∨ C ′ ∨ ans(r))θ
                              ′     ′       ′           ′
    s ≃ t ∨ C ∨ ans(r)     u[s ] 6≃ u ∨ C ∨ ans(r )           s ≃ t∨C ∨ans(r)    u[s′ ] ≃ u′ ∨C ′ ∨ans(r ′ )
              ′        ′                        ′
  (D∨u[t] 6≃ u ∨C ∨C ∨ans(if s ≃ t then r else r))θ            (D∨r 6≃ r ∨u[t] ≃ u′ ∨C ∨C ′ ∨ans(r))θ
                                                                         ′

                              ′     ′       ′           ′
    s ≃ t ∨ C ∨ ans(r)     u[s ] ≃ u ∨ C ∨ ans(r )            s ≃ t∨C ∨ans(r)    u[s′ ] 6≃ u′ ∨C ′ ∨ans(r ′ )
  (D∨u[t] ≃ u′ ∨C ∨C ′ ∨ans(if s ≃ t then r ′ else r))θ        (D∨r 6≃ r ′ ∨u[t] 6≃ u′ ∨C ∨C ′ ∨ans(r))θ

  where (θ, D) is a computable unifier of s, s′ w.r.t. the argument of the answer
  literal in the rule conclusion (i.e. if s ≃ t then r ′ else r for the left-column rules,
  and r for the others); (rules on the first line only) L[s′ ] is not an equality literal;
  and (rules on the second and third line only) u′ θ 6 u[s′ ]θ.
                                   Binary resolution (BR):

     A ∨ C ∨ ans(r)        ¬A′ ∨ C ′ ∨ ans(r ′ )            A ∨ C ∨ ans(r)       ¬A′ ∨ C ′ ∨ ans(r ′ )
              ′                         ′
  (D∨C ∨C ∨ans(if A then r else r))θ                           (D ∨ r 6≃ r ∨ C ∨ C ′ ∨ ans(r))θ
                                                                             ′


  where (θ, D) is a computable unifier of A, A′ w.r.t. (first rule) if A then r ′ else r
  or (second rule) r.
   Factoring (F):           Equality resolution (ER):                  Equality factoring (EF):

 A ∨ A′ ∨ C ∨ ans(r)              s 6≃ t ∨ C ∨ ans(r)                 s ≃ t ∨ s′ ≃ t′ ∨ C ∨ ans(r)
 (D∨A∨C ∨ans(r))θ                 (D ∨ C ∨ ans(r))θ                  (D∨s ≃ t∨t 6≃ t′ ∨C ∨ans(r))θ

   where (θ, D) is a               where (θ, D) is a                  where (θ, D) is a computable
  computable unifier              computable unifier                     unifier of s, s′ w.r.t. r;
   of A, A′ w.r.t. r.               of s, t w.r.t. r.                    tθ 6 sθ; and t′ θ 6 tθ.


Fig. 3. Selected rules of the extended superposition calculus Sup for reasoning with
answer literals, with underlined literals being selected.


Lemma 4 [Soundness of Inferences with Answer Literals] If the rule (9)
is sound, the rules (10) are sound as well.
    We note that we keep the original rule (9) in I, but impose that none of its
premises C1 , . . . , Cn contains an answer literal. Clearly, neither the such modified
rule (9) nor the new rules (10) introduce uncomputable symbols into answer
literals. Rather, these rules add disequality constraints D into their conclusions
and immediately select D for further applications of inference rules. Such a
selection guides the saturation process in Algorithm 1 to first discharge the
constraints D containing uncomputable symbols with the aim of deriving a clause
C ′ ∨ ans(r′ ) where C ′ is computable. The clause C ′ ∨ ans(r′ ) is then converted
into a program with conditions using Corollary 2.
Superposition with answer literals. We make the inference rule modifica-
tions (9), together with the addition of new rules (10), for each inference rule of
12        Hozzová et al.

the Sup calculus from Figure 1. Further, we also ensure that rules with multi-
ple premises, when applied on several premises containing answer literals, derive
clauses with at most one answer literal. We therefore introduce the following
two rule modifications. (i) We use the if−then−else constructor to combine
answer literals of premises, by adapting the use of if−then−else within binary
resolution [12,13,21] to superposition rules. (ii) We use an answer literal from
only one of the rule premises in the rule conclusion and add new disequality
constraint r 6≃ r′ between the premises’ answer literal arguments, similar to the
constraints D of the computable unifier. Analogously to the computable unifier
constraints, we immediately select this disequality constraint r 6≃ r′ .
    The resulting extension of the Sup calculus with answer literals is given in
Figure 3. In addition to the rules of Figure 3, the extended calculus contains rules
constructed as (10) for superposition and binary resolution rules of Figure 1.
Using Lemma 4, we conclude the following.

Lemma 5 [Soundness of Sup with Answer Literals] The inference rules
from Figure 3 of the extended Sup calculus with answer literals are sound.

   By the soundness results of Lemmas 4–5, Corollaries 2–3 imply that, when
applying the calculus of Figure 3 in the saturation-based program synthesis
approach of Algorithm 1, we construct correct programs.

Example 2. We illustrate the use of Algorithm 1 with the extended Sup calculus
of Figure 3, strengthening our motivation from Section 3 with if−then−else
reasoning. To this end, consider the functional specification over group theory:

                            ∀x, y.∃z.(x ∗ y 6≃ y ∗ x → z ∗ z 6≃ e),                (11)

asserting that, if the group is not commutative, there is an element whose square
is not e. In addition to the axioms (A1)-(A3) of Figure 2, we also use the right
identity axiom (A2’) ∀x. x ∗ e ≃ x.7 Based on Algorithm 1, we obtain the
following derivation of the program for (11):

 1. σ1 ∗ σ2 6≃ σ2 ∗ σ1 ∨ ans(z)                          [preprocessed specification]
 2. e ≃ z ∗ z ∨ ans(z)                                   [preprocessed specification]
 3. σ1 ∗ σ2 6≃ σ2 ∗ σ1           [answer literal removal 1. (Algorithm 1, line 10)]
 4. x ∗ (x ∗ y) ≃ e ∗ y ∨ ans(x)                                        [Sup 2., A3]
 5. e ≃ x ∗ (y ∗ (x ∗ y)) ∨ ans(x ∗ y)                                  [Sup A3, 2.]
 6. x ∗ (x ∗ y) ≃ y ∨ ans(x)                                            [Sup 4., A2]
 7. x ∗ e ≃ y ∗ (x ∗ y) ∨ ans(if e ≃ x ∗ (y ∗ (x ∗ y)) then x else x ∗ y) [Sup 6., 5.]
 8. y ∗ (x ∗ y) ≃ x ∨ ans(if e ≃ x ∗ (y ∗ (x ∗ y)) then x else x ∗ y) [Sup 7., A2’]
 9. x ∗ y ≃ y ∗ x ∨ ans(if x ∗ (y ∗ x) ≃ y then x else if e ≃ x ∗ (y ∗ (x ∗
    y)) then x else x ∗ y)                                                [Sup 6., 8.]
10. ans(if σ1 ∗(σ2 ∗σ1 ) ≃ σ2 then σ1 else if e ≃ σ1 ∗(σ2 ∗(σ1 ∗σ2 )) then σ1 else
    σ1 ∗ σ2 )                                                              [BR 9., 3.]
7
     We include axiom (A2’) only to shorten the presentation of the obtained derivation.
                                                 Program Synthesis in Saturation        13

11.                                [answer literal removal 11. (Algorithm 1, line 10)]
   The programs with conditions collected during saturation-based program
synthesis, in particular corresponding to steps 3. and 11. above, are:
P1 [x, y] := hz, x ∗ y ≃ y ∗ xi
P2 [x, y] := hif x ∗ (y ∗ x) ≃ y then x else (if e ≃ x ∗ (y ∗ (x ∗ y)) then x else x ∗ y),
             x ∗ y 6≃ y ∗ xi

Note the variable z, representing an arbitrary witness, in P1 [x, y]. An arbitrary
value is a correct witness in case x∗ y ≃ y ∗ x holds, as in this case (11) is trivially
satisfied. Thus, we do not need to consider the case x∗y ≃ y∗x separately. Hence,
we construct the final program P [x, y] only from P2 [x, y] and obtain:
P [x, y] := if x∗(y ∗x) ≃ x then x else (if e ≃ x∗(y ∗(x∗y)) then x else x∗y)

     We conclude this section by illustrating the benefits of computable unifiers.
Example 3. Consider the group theory specification
                               ∀x, y.∃z. z ∗ (i(x) ∗ i(y)) = e,                       (12)

describing the inverse element z of i(x) ∗ i(y). We annotate the inverse i(·) as
uncomputable to disallow the trivial solution i(i(x) ∗ i(y)). Using computable
unifiers, we synthesize8 the program y ∗ x; that is, a program computing y ∗ x as
the inverse of i(x) ∗ i(y).


6     Computable Unification with Abstraction
When compared to the Sup calculus of Figure 1, our extended Sup calculus with
answer literals from Figure 3 uses computable unifiers instead of mgus. To find
computable unifiers, we introduce Algorithm 2 by extending a standard unifica-
tion algorithm [17,7] and an algorithm for unification with abstraction of [16].
Algorithm 2 combines computable unifiers with mgu computation, resulting in
the computable unifier θ := mgucomp(E1 , E2 , E3 ) to be further used in Figure 3.
      Algorithm 2 modifies a standard unification algorithm to ensure computabil-
ity of E3 θ. Changes compared to a standard unification algorithm are high-
lighted. Algorithm 2 does not add s 7→ t to θ if s is a variable in E3 and t is
uncomputable. Instead, if t is f (t1 , . . . , tn ) where f is computable but not all
t1 , . . . , tn are computable, we extend θ by s 7→ f (x1 , . . . , xn ) and then add equa-
tions x1 = t1 , . . . , xn = tn to the set of equations E to be processed. Otherwise,
f is uncomputable and we perform an abstraction: we consider s and t to be uni-
fied under the condition that s ≃ t holds. Therefore we add a constraint s 6≃ t to
the set of literals D which will be added to any clause invoking the computable
unifier. To discharge the literal s 6≃ t, one must prove s ≃ t. While s can be later
substituted for other terms, as long as we use mgucomp, s will never be substituted
for an uncomputable term. Thus, we conclude the following result.
8
    see derivation in Appendix B
14        Hozzová et al.

Algorithm 2 Computable Unification with Abstraction
function mgucomp (E1 , E2 , E3 )
  if E3 is uncomputable then fail
  let E be a set of equations and θ be a substitution; E := {E1 = E2 }; θ := {}
  let D be a set of disequalities; D := ∅
  repeat
     if E is empty then
       return (θ, D) where D is the disjunction of literals in D
     Select an equation s = t in E and remove it from E
     if s coincides with t then do nothing
     else if s is a variable and s does not occur in t then
       if s does not occur in E3 or t is computable then θ := θ◦{s 7→ t}; E = E {s 7→ t}
       else if t = f (t1 , . . . , tn ) and f is computable then
          θ := θ◦{s 7→ f (x1 , . . . , xn )}; E := E {s 7→ f (x1, . . . , xn )}∪{x1 = t1 , . . . , xn = tn }
             where x1 , . . . , xn are fresh variables
       else if t = f (t1 , . . . , tn ) and f is uncomputable then D := D ∪ {s 6≃ t}
     else if s is a variable and s occurs in t then fail
     else if t is a variable then E := E ∪ {t = s}
     else if s and t have different top-level symbols then fail
     else if s = f (s1 , . . . , sn ) and t = f (t1 , . . . , tn ) then E := E ∪{s1 = t1 , . . . , sn = tn }



Theorem 6. Let E1 , E2 , E3 be expressions. Then (θ, D) := mgucomp(E1 , E2 , E3 )
is a computable unifier.


7      Implementation and Experiments

Implementation. We implemented our saturation-based program synthesis ap-
proach in the Vampire prover [10]. We used Algorithm 1 with the extended
Sup calculus of Figure 3. The implementation, consisting of approximately 1100
lines of C++ code, is available at https://github.com/vprover/vampire. The syn-
thesis functionality can be turned on using the option --question answering
synthesis.
    Vampire accepts functional specifications in an extension of the SMT-LIB2
format [4], by using the new command assert-not to mark the specification. We
consider interpreted theory symbols to be computable. Uninterpreted symbols
can be annotated as uncomputable via the command (set-option
:uncomputable (symbol1 ... symbolN)).
    Our implementation also integrates Algorithm 1 with the AVATAR archi-
tecture [25].9 We modified the AVATAR framework to only allow splitting over
ground computable clauses that do not contain answer literals. Further, if we
derive a clause C[σ]∨ans(r[σ]) with AVATAR assertions C1 [σ], . . . ,W
                                                                     Cm [σ], where
                                                                      m
C[σ] is ground and computable, we replace it by the clause C[σ] ∨ i=1 ¬Ci [σ] ∨
ans(r[σ]) without any assertions. We then immediately record a program with
9
     We include a short description of AVATAR in Appendix C.
                                            Program Synthesis in Saturation         15

conditions hr[x], ¬C[x]∧ m
                           V                                             Wm
                             i=1 Ci [x]i, and replace the clause by C[σ]∨ i=1 ¬Ci [σ]
(see lines 7-10 of Algorithm 1), which may be then further split by AVATAR.
    Finally, our implementation simplifies the programs we synthesize. If during
Algorithm 1 we record a program hz, F i where z is a variable, we do not use
this program in the final program construction (line 12 of Algorithm 1) even if
F occurs in the derivation of  (see Example 2).
Examples and experimental setup. The goal of our experimental evaluation
is to showcase the benefits of our approach on problems that are deemed to
be hard, even unsolvable, by state-of-the-art synthesis techniques. We therefore
focused on first–order theory reasoning and evaluated our work on the group
theory problems of Examples 1-3, as well as on integer arithmetic problems.
    As the SMT-LIB2 format can easily be translated into the SyGuS 2.1 syn-
tax [15], we compared our results to cvc5 1.0.4 [3], supporting SyGuS-based syn-
thesis [2]. Our experiments were run on an AMD Epyc 7502, 2.5 GHz CPU with
1 TB RAM, using a 5 minutes time limit per example. Our benchmarks as well as
the     configurations      for      our     experiments       are    available   at:
https://github.com/vprover/vampire benchmarks/tree/master/synthesis
Experimental results with group theory properties. Vampire synthesizes
the solutions of the Examples 1-3 in 0.01, 13, and 0.03 seconds, respectively.
Since these examples use uninterpreted functions, they cannot be encoded in
the SyGuS 2.1 syntax, showcasing the limits of other synthesis tools.
Experimental results with maximum of n ≥ 2 integers. For the maximum
of 2 integers, the specification is ∀x1 , x2 ∈ Z. ∃y ∈ Z. y ≥ x1 ∧ y ≥ x2 ∧ (y =
x1 ∨ y = x2 ) , and the program we synthesize is if x1 < x2 then x2 else x1 .
Both our work and cvc5 are able to synthesize programs choosing the maximal
value for up to n = 23 input variables, as summarized below. For n > 23, both
Vampire and cvc5 time out.
    Number n of variables for
                                   2       5       10     15     20     22     23
    which max is synthesized
                   Vampire       0.03    0.03     0.05     1     13    55      215
                        cvc5     0.01    0.03     0.6     6.8    88    188     257

Experimental results with polynomial equations. Vampire can synthesize
the solution of polynomial equations; for example, for ∀x1 , x2 ∈ Z.∃y ∈ Z.(y 2 =
x21 +2x1 x2 +x22 ), we synthesize x1 +x2 . Vampire finds the corresponding program
in 26 seconds using simple first-order reasoning, while cvc5 fails in our setup.


8     Related Work
Our work builds upon deductive synthesis [13] adapted for the resolution calcu-
lus [12,21]. We extend this line of work with saturation-based program synthesis,
by using adjustments of the superposition calculus.
    Component-based synthesis of recursion-free programs [20] from logical spec-
ifications is addressed in [20,6,23]. The work of [20] uses first-order theorem
16      Hozzová et al.

proving to prove specifications and extract programs from proofs. In [6,23], ∃∀
formulas are produced to capture specifications over component properties and
SMT solving is applied to find a term satisfying the formula, corresponding to a
straight-line program. We complement [20] with saturation-based superposition
proving and avoid template-based SMT solving from [6,23].
    A prominent line of research comes with syntax guided synthesis (SyGuS) [1],
where functional specifications are given using a context-free grammar. This
grammar yields program templates to be synthesized via an enumerative search
procedure based on SMT solving [3,8]. We believe our work is complementary
to SyGuS, by strengthening first-order reasoning for program synthesis, as evi-
denced by Examples 1–3.
    The sketching technique [18,24] synthesizes program assignments to variables,
using an alternative framework to the program synthesis setting we rely upon. In
particular, sketching addresses domains that do not involve input logical formulas
as functional specifications, such as example-guided synthesis [22].


9    Conclusions
We extend saturation-based proof search to saturation-based program synthesis,
aiming to derive recursion-free programs from specifications. We integrate answer
literals with saturation, and modify the superposition calculus and unification to
synthesize computable programs. Our initial experiments show that a first-order
theorem prover becomes an efficient program synthesizer, potentially opening
up interesting avenues toward recursive program synthesis, for example using
saturation-based proving with induction.

Acknowledgements. We thank Haniel Barbosa for support with experiments
with cvc5. This work was partially funded by the ERC CoG ARTIST 101002685,
and the FWF grants LogiCS W1255-N23 and LOCOTES P 35787.


References
 1. Alur, R., Bodı́k, R., Dallal, E., Fisman, D., Garg, P., Juniwal, G., Kress-Gazit,
    H., Madhusudan, P., Martin, M.M.K., Raghothaman, M., Saha, S., Seshia, S.A.,
    Singh, R., Solar-Lezama, A., Torlak, E., Udupa, A.: Syntax-Guided Synthesis. In:
    Dependable Software Systems Engineering, pp. 1–25 (2015)
 2. Alur, R., Fisman, D., Padhi, S., Reynolds, A., Singh, R., Udupa, A.: SyGuS-Comp
    2019. https://sygus.org/comp/2019/ (2019)
 3. Barbosa, H., Barrett, C.W., Brain, M., Kremer, G., Lachnitt, H., Mann, M., Mo-
    hamed, A., Mohamed, M., Niemetz, A., Nötzli, A., Ozdemir, A., Preiner, M.,
    Reynolds, A., Sheng, Y., Tinelli, C., Zohar, Y.: cvc5: A Versatile and Industrial-
    Strength SMT Solver. In: TACAS. pp. 415–442 (2022)
 4. Barrett, C., Fontaine, P., Tinelli, C.: The SMT-LIB Standard Version 2.6.
    www.SMT-LIB.org (2021)
 5. Green, C.: Theorem-Proving by Resolution as a Basis for Question-Answering Sys-
    tems. Machine Intelligence 4, 183–205 (1969)
                                             Program Synthesis in Saturation        17

 6. Gulwani, S., Jha, S., Tiwari, A., Venkatesan, R.: Synthesis of Loop-Free Programs.
    In: PLDI. p. 62–73 (2011)
 7. Hoder, K., Voronkov, A.: Comparing Unification Algorithms in First-Order Theo-
    rem Proving. In: KI. pp. 435–443 (2009)
 8. Jha, S., Seshia, S.A.: A Theory of Formal Synthesis via Inductive Learning. Acta
    Informatica 54(7), 693–726 (2017)
 9. Korovin, K., Kovacs, L., Reger, G., Schoisswohl, J., Voronkov, A.: ALASCA: Rea-
    soning in Quantified Linear Arithmetic. In: TACAS (2023), to appear
10. Kovács, L., Voronkov, A.: First-Order Theorem Proving and Vampire. In: CAV.
    pp. 1–35 (2013)
11. Kunen, K.: The Semantics of Answer Literals. J. of Automated Reasoning 17(1),
    83–95 (1996)
12. Lee, R.C.T., Waldinger, R.J., Chang, C.L.: An Improved Program-Synthesizing
    Algorithm and Its Correctness. Commun. ACM (4), 211–217 (1974)
13. Manna, Z., Waldinger, R.: A Deductive Approach to Program Synthesis. ACM
    Trans. Program. Lang. Syst. 2(1), 90–121 (1980)
14. Nieuwenhuis, R., Rubio, A.: Paramodulation-Based Theorem Proving. In: Hand-
    book of Automated Reasonings, vol. I, pp. 371–443. Elsevier and MIT Press (2001)
15. Padhi, S., Polgreen, E., Raghothaman, M., Reynolds, A., Udupa, A.: The SyGuS
    Language Standard Version 2.1. https://sygus.org/language/ (2021)
16. Reger, G., Suda, M., Voronkov, A.: Unification with Abstraction and Theory In-
    stantiation in Saturation-Based Reasoning. In: TACAS. pp. 3–22 (2018)
17. Robinson, J.A.: A Machine-Oriented Logic Based on the Resolution Principle. J.
    ACM 12(1), 23–41 (1965)
18. Solar-Lezama, A.: The Sketching Approach to Program Synthesis. In: APLAS. pp.
    4–13 (2009)
19. Srivastava, S., Gulwani, S., Foster, J.S.: From Program Verification to Program
    Synthesis. In: POPL. p. 313–326 (2010)
20. Stickel, M., Waldinger, R., Lowry, M., Pressburger, T., Underwood, I.: Deductive
    Composition of Astronomical Software from Subroutine Libraries. In: CADE. pp.
    341–355 (1994)
21. Tammet, T.: Completeness of Resolution for Definite Answers. J. of Logic and
    Computation 5(4), 449–471 (08 1995)
22. Thakkar, A., Naik, A., Sands, N., Alur, R., Naik, M., Raghothaman, M.: Example-
    Guided Synthesis of Relational Queries. In: PLDI. p. 1110–1125 (2021)
23. Tiwari, A., Gascón, A., Dutertre, B.: Program Synthesis Using Dual Interpretation.
    In: CADE. pp. 482–497 (2015)
24. Torlak, E., Bodik, R.: Growing Solver-Aided Languages with Rosette. In: Onward!
    p. 135–152. Onward! 2013 (2013)
25. Voronkov, A.: AVATAR: The Architecture for First-Order Theorem Provers. In:
    CAV. pp. 696–710 (2014)
18        Hozzová et al.

A       Proofs

In the following we use the notion of universal closure of a formula F , which is
the formula ∀z.F , where z are all free variables of F .

Theorem 1 [Semantics of Clauses with Answer Literals] Let C be a
clause not containing an answer literal. Assume that, using a saturation algo-
rithm based on a sound inference system I, the clause C ∨ ans(r[σ]) is derived
from the set of clauses consisting of initial assumptions A1 , . . . , An , the clausified
formula cnf(¬F [σ, y] ∨ ans(y)) and additional assumptions C1 , . . . , Cm . Then,

                        A1 , . . . , An , C1 , . . . , Cm ⊢ C, F [σ, r[σ]].

That is, under the assumptions C1 , . . . , Cm , ¬C, the computable term r[σ] pro-
vides a definite answer to (6).

Proof. We consider the calculus which was used for deriving C ∨ ans(r[σ]), but
with lifted ordering and selection constraints. Since the soundness of the calculus
does not depend on these constraints, the calculus without the constraints is
sound as well. Now, since ans is uninterpreted, we can replace ans(y) by y 6≃ r[σ],
and obtain a derivation of C ∨r[σ] 6≃ r[σ] from A1 , . . . , An , ∀y.cnf(¬F [σ, y]∨y 6≃
r[σ]) using the calculus without the constraints.10
    We want to show that
                            n
                            ^            m
                                         ^
                                  Ai ∧         Ci → C ∨ F [σ, r[σ]]                  (13)
                            i=1          i=1

is valid. Hence, we need to show that in each interpretation, in which the an-
tecedent is true, also the consequent is true. Let us consider such an interpreta-
tion I. We distinguish two cases. First, assume that ∀y.cnf(¬F [σ, y] ∨ y 6≃ r[σ])
is true in I. Then since all assumptions from which we derived C ∨ r[σ] 6≃ r[σ]
are true in I and since the inference system is sound, also C ∨ r[σ] 6≃ r[σ] is true.
That clause is equivalent to C, hence C is true, which makes the consequent
of (13) true. Second, assume that ∀y.cnf(¬F [σ, y] ∨ y 6≃ r[σ]) is false in I. Then
its negation, ¬∀y.cnf(¬F [σ, y] ∨ y 6≃ r[σ]), equivalent to ∃y.(F [σ, y] ∧ y ≃ r[σ]),
equivalent to F [σ, r[σ]] must be true in I. Hence, the consequent of (13) is true
also in this case. Therefore (13) is valid.                                        

Corollary 2 [Programs with Conditions] Let r[σ] be a computable term
and C[σ] a ground computable clause not containing an answer literal. Assume
that clause C[σ] ∨ ans(r[σ]) is derived from the set of initial clauses A1 , . . . , An ,
the clausified formula cnf(¬F [σ, y] ∨ ans(y)) and additional ground computable
10
     The derivation might not have been possible in the calculus with the ordering and
     selection constraints due to replacing the positive literal ans(y) with the negative
     literal y 6≃ r[σ] containing different symbols.
                                                Program Synthesis in Saturation     19

assumptions C1 [σ], . . . , Cm [σ], by using saturation based on a sound inference
system I. Then,
                                       m
                                       ^
                                hr[x],   Cj [x] ∧ ¬C[x]i
                                    j=1

is a program with conditions for (6).
                                          Vn          Vm
Proof. From Theorem 1 follows that i=1 Ai ∧ i=1 Ci [σ] → C[σ] ∨VF [σ, r[σ]]
                                                                             n
holds.
Vm     Since σ are fresh uninterpreted constants, we obtain that V i=1 Ai ∧
                                                                            m
             → C[x]∨F [x, r[x]] is valid as well, and that is equivalent to j=1 Cj [x]∧
  i=1 Ci [x] V
¬C[x] → ( ni=1 Ai → F [x, r[x]]). Therefore hr[x], m
                                                       V
                                                         j=1 Cj [x] ∧ ¬C[x]i is a pro-
gram with conditions for A1 ∧ . . . ∧ An → ∀x.∃y.F [x, y].                          

Corollary 3 [From Programs with Conditions to Programs for (6)] Let
                                               Vi−1
P1 [x], . . . , Pk [x], where Pi [x] = hri [x], j=1 Cj [x] ∧ ¬Ci [x]i, be programs with
                                     Vn         Vk
conditions for (6), such that i=1 Ai ∧ i=1 Ci [x] is unsatisfiable. Then P [x],
given by

                     P [x] := if ¬C1 [x] then r1 [x]
                              else if ¬C2 [x] then r2 [x]
                                  ...                                              (8)
                              else if ¬Ck−1 [x] then rk−1 [x]
                              else rk [x],

is a program for (6).

Proof. For any interpretation I and any variable assignment v, let p be the
smallest index such that ¬Cp [x] holds in I under v, but all ¬Cj [x], where 1 ≤
                                               Vn        Vk
j < p, do not hold in I under v. Since i=1 Ai ∧ i=1 Ci [x] is unsatisfiable,
under the assumptions A1 , . . . , An such a p has to exist. Then in I under v and
under the assumptions A1 , . . . , An , the interpretation of P [x] is the same as the
interpretation of rp [x].
                    Vp−1
    Further, since j=1 Cj [x] ∧ ¬Cp [x] is the condition for Pp [x], from the defi-
nition of a program with conditions we obtain that A1 ∧ · · · ∧ An → F [x, rp [x]]
holds in I under v. Hence also A1 ∧ · · · ∧ An → F [x, P [x]] holds in I under v.
    Finally, since this argument holds for any I and v, and since all A1 , . . . , An
are closed formulas, also A1 ∧ · · · ∧ An → ∀x.F [x, P [x]] holds. Therefore P [x] is
a program for (6).                                                                  

Lemma 4 [Soundness of Inferences with Answer Literals] If the rule (9)
is sound, the rules (10) are sound as well.

Proof. For clarity we repeat the original rule:
                                   C1     ···    Cn ,
                                          Cθ                                       (9)
20      Hozzová et al.

where θ is a substitution such that Eθ ≃ E ′ θ holds for some expressions E, E ′ .
   We will prove the soundness of the new rule

                            C1 ∨ ans(r) C2 · · · Cn
                                (D ∨ C ∨ ans(r))θ′  ,                               (10’)

where (θ′ , D) is a computable unifier of E, E ′ with respect to r, and none of
C1 , . . . , Cn contains an answer literal. The proof of soundness of the other new
rules of (10) is analogous.
    Assume interpretation I to be a model of the universal closures of the premises
of (10’), but not a model of the universal closure of its conclusion. Then Dθ′ , Cθ′
and ans(r)θ′ are false in I. From Dθ′ being false in I and from (θ′ , D) being
an abstract unifier follows that Eθ′ ≃ E ′ θ′ holds. We can therefore set θ := θ′ .
From the soundness of (9) and Cθ′ being false in I then follows that some of
C1 , . . . , Cn is false in I. However, none of C2 , . . . , Cn can be false in I, because
we assumed all premises of (10’) to be true in I. Hence, C1 is false in I. Further,
from ans(r)θ′ being false in I follows that ans(r) is false in I. However, that
means that C1 ∨ ans(r) is false in I, which contradicts the assumption that the
universal closures of all premises of rule (10’) are true in I.
    Hence, the rule (10’) is sound.                                                     

Lemma 5 [Soundness of Sup with Answer Literals] The inference rules
from Figure 3 of the extended Sup calculus with answer literals are sound.

Proof. Soundness of the factoring, equality factoring and equality resolution
rules follows from Lemma 4.
    We will prove soundness for the first superposition rule and the second binary
resolution rule. The proofs for other superposition and binary resolution rules
are analogous.
    For clarity we repeat the first superposition rule of Figure 3:

                    s ≃ t ∨ C ∨ ans(r) L[s′ ] ∨ C ′ ∨ ans(r′ )
               (D ∨ L[t] ∨ C ∨ C ′ ∨ ans(if s ≃ t then r′ else r))θ

Assume interpretation I to be a model of the universal closures of the premises
of the rule, but not a model of the universal closure of its conclusion. Then
there is some variable assignment v such that (D ∨ L[t] ∨ C ∨ C ′ ∨ ans(if s ≃
t then r′ else r))θ is false in I under v. Let v ′ be a variable assignment that
assigns to each variable x the value that xθ has in I under v. Then:

 1. From L[t]θ, Cθ, C ′ θ being false in I under v follows that L[t], C, C ′ are false
    in I under v ′ .
 2. Since Dθ is false in I under v, from (θ, D) being an abstract unifier of s, s′
    follows that sθ ≃ s′ θ is true in I under v, and therefore s, s′ have the same
    interpretation in I under v ′ . Then consider two cases:
    (a) s ≃ t is true in I under v ′ and sθ ≃ tθ is true in I under v. Then
         from ans(if s ≃ t then r′ else r)θ being false in I under v follows that
                                                   Program Synthesis in Saturation              21

        ans(r′ )θ is false in I under v and therefore ans(r′ ) is false in I under v ′ .
        Also from s ≃ t being true in I under v ′ , 1., and 2. follows that L[s′ ] is
        false in I under v ′ . Then the whole second premise of the rule is false
        in I under v ′ , which is a contradiction with the assumption that I is a
        model of its universal closure.
    (b) s ≃ t is false in I under v ′ and sθ ≃ tθ is false in I under v. This case
        leads similarly to the first premise being false, in contradiction with the
        assumption.
Therefore the first superposition rule is sound.
   For clarity we repeat the second binary resolution rule of Figure 3:
                            A∨C ∨ans(r) ¬A′ ∨C ′ ∨ans(r′ )
                             (D ∨ r 6≃ r′ ∨ C ∨ C ′ ∨ ans(r))θ

Assume interpretation I to be a model of the universal closures of the premises
of the rule, but not a model of the universal closure of its conclusion. Then there
is some variable assignment v such that (D ∨ r 6≃ r′ ∨ C ∨ C ′ ∨ ans(r))θ is false
in I under v. Let v ′ be a variable assignment that assigns to each variable x the
value that xθ has in I under v. Then:
 1. From rθ 6≃ r′ θ, Cθ, C ′ θ being false in I under v follows that r 6≃ r′ , C, C ′ are
    false in I under v ′ . Therefore r, r′ have the same interpretation in I under
    v′ .
 2. Since ans(r)θ is false in I under v, also ans(r) is false in I under v ′ . Then
    from 1. follows that ans(r′ ) is also false in I under v ′ .
 3. Since Dθ is false in I under v, from (θ, D) being an abstract unifier of
    A, A′ follows that Aθ, A′ θ have the same interpretation in I under v, and
    therefore A, A′ have the same interpretation in I under v ′ . Therefore, only
    one of A, ¬A′ is true in I under v ′ , which together with C, C ′ , ans(r), ans(r′ )
    being false in I under v ′ forms a contradiction with the assumption that I
    is a model of both premises of the rule.
Therefore the second binary resolution rule is sound as well.                                   

Theorem 6. Let E1 , E2 , E3 be expressions. Then (θ, D) := mgucomp(E1 , E2 , E3 )
is a computable unifier.

Proof. We will denote the subexpression of the expression E at position p by
E|p.
    We first prove that (θ, D) is an abstract unifier of E1 , E2 . If E1 θ|p′ and E2 θ|p′
differ, there has to be a position p, where p′ is a prefix of p, such that the top-level
symbol of E1 θ|p and E2 θ|p differs. From the construction of θ follows that for
any position p, the subexpressions E1 θ|p, E2 θ|p differ in their top-level symbol
only if E1 |p = s and E2 |p = f (t1 , . . . , tn ) (or, symmetrically, E1 |p = f (t1 , . . . , tn )
and E2 |p = s) where s is a variable and f is uncomputable. However, in this case
s 6≃ f (t1 , . . . , tn ) occurs in D. Therefore, for any interpretation I, any variable
assignment v, and any position p′ , the interpretations of E1 θ|p′ , E2 θ|p′ in I under
22        Hozzová et al.

v will either be the same, or sθ 6≃ f (t1 , . . . , tn )θ will be true in I under v. Hence,
(D ∨ E1 ≃ E2 )θ is valid, and therefore (θ, D) is an abstract unifier of E1 , E2 .
   Next, we prove that E3 θ is computable. Since the algorithm successfully
terminated, E3 must have been computable (otherwise it would fail). Further, the
algorithm only extends the substitution θ by s 7→ t where t is uncomputable if s
does not occur in E3 . Thus, E3 θ is computable, and hence (θ, D) is a computable
unifier.


B       Example
A detailed version of Example 3 follows.
Example 3. Consider the group axioms (A1)-(A3) of Figure 2, the additional
axioms (A1’) ∀x. x ∗ i(x) ≃ e for right inverse and (A2’) ∀x. x ∗ e ≃ x for right
identity (symmetric to (A1), (A2)),11 and the following specification

                              ∀x, y.∃z. z ∗ (i(x) ∗ i(y)) = e,                            (14)

describing the inverse element of i(x) ∗ i(y). The trivial program derivation for
this specification would only have three steps:
 1. e 6≃ x ∗ (i(σ1 ) ∗ i(σ2 )) ∨ ans(x)                          [preprocessed specification]
 2. ans(i(i(σ1 ) ∗ i(σ2 )))                                                      [BR A1, 1.]
 3.                                                              [answer literal removal 2.]

    To disallow the trivial solution, i(i(x)∗i(y)), we annotate the function symbol
i as uncomputable. Therefore we do not perform the step 2. from above, but
instead perform binary resolution with the computable unifier ({x 7→ i(i(σ1 ) ∗
i(σ2 ))}, x 6≃ i(i(σ1 ) ∗ i(σ2 ))), leading to the following derivation:
 1. e 6≃ x ∗ (i(σ1 ) ∗ i(σ2 )) ∨ ans(x)                          [preprocessed specification]
 2. i(i(σ1 ) ∗ i(σ2 )) 6≃ x ∨ ans(x)                                               [BR A1, 1.]
 3. i(x) ∗ (x ∗ y) ≃ e ∗ y                                                      [Sup A3, A1]
 4. i(x) ∗ (x ∗ y) ≃ y                                                            [Sup 3., A2]
 5. i(i(x)) ∗ e ≃ x                                                               [Sup 4., A1]
 6. i(i(x)) ≃ x                                                                  [Sup 5., A2’]
 7. e ≃ x ∗ (y ∗ i(x ∗ y))                                                     [Sup A1’, A3]
 8. x ∗ i(y ∗ x) ≃ i(x) ∗ e                                                         [Sup 4., 7.]
 9. i(x) = y ∗ i(x ∗ y)                                                          [Sup 8., A2’]
10. i(x) ∗ i(y) = i(y ∗ x)                                                          [Sup 4., 9.]
11. i(i(σ2 , σ1 )) 6≃ x ∨ ans(x)                                                  [Sup 10., 2.]
12. ans(σ2 ∗ σ1 )                                                                  [BR 6., 11.]
13.                                                             [answer literal removal 12.]

   We synthesize the program P [x, y] := y ∗ x. Note that there exists a differ-
ent derivation only using computable unifiers in the form (θ, ) (i.e., not using
abstraction).
11
     We include the symmetric axioms to shorten the derivation for presentation purposes.
     The derivation would work also without (A1’), (A2’).
                                                     Program Synthesis in Saturation                23

C     Splitting and AVATAR

One of the keys to the efficiency of saturation-based theorem proving is clause
splitting, with the leading approach being the AVATAR architechture [25]. The
main idea of splitting is as follows. Let S be a set of clauses and C1 ∨ C2 a clause
such that C1 , C2 have disjoint sets of variables. We call such clauses C1 , C2 the
components of C1 ∨ C2 . Then S ∪ {C1 ∨ C2 } is unsatisfiable iff both S ∪ {C1 }
and S ∪ {C2 } are unsatisfiable. Therefore, instead of checking satisfiability of a
set of large clauses, we check the satisfiability of multiple sets of smaller clauses.
AVATAR implements this idea by using an interplay between a saturation-based
first-order theorem prover and a SAT/SMT solver. The SAT/SMT solver finds
a set of clause components, satisfiability of which implies satisfiability of all
split clauses. These components, called assertions, are then used by the theorem
prover for further derivations in saturation. All clauses derived using assertions
C1 , . . . , Cn are called clauses with assertion C1 , . . . , Cn .
    However, when using Algorithm 1 for program synthesis with (standard)
AVATAR to saturate a preprocessed specification (7), we may derive a clause
ans(r[σ]) with assertions C1 [σ], . . . , Cm [σ]. By Theorem 1, we then obtain

                          A1 , . . . , An , C1 [σ], . . . , Cm [σ] ⊢ F [σ, r[σ]].

If C1 [σ], . . . , Cm [σ] are computable and ground, then hr[x], m
                                                                                V
                                                                                  i=1 Ci [x]i is a pro-
gram with conditions. However, if not all of the assertions C1 [σ], . . . , Cm [σ] are
computable and ground, then Algorithm 1 should continue reasoning with these
assertions with the aim of reducing them to computable and ground literals.
This, however, is not directly possible in the AVATAR framework. Hence, we
modify AVATAR as described in Section 7.
