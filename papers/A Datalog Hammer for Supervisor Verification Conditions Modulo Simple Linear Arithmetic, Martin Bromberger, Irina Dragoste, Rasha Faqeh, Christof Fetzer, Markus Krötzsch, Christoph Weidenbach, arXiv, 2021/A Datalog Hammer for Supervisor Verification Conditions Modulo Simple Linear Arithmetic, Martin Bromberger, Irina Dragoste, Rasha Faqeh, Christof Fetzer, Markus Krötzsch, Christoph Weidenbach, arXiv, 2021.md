                                        A Datalog Hammer for Supervisor Verification
                                        Conditions Modulo Simple Linear Arithmetic
                                                               Martin Bromberger
                                                       Max Planck Institute for Informatics
                                               Saarland Informatics Campus, Saarbrücken, Germany
arXiv:2107.03189v1 [cs.LO] 7 Jul 2021




                                                                     Irina Dragoste
                                                              TU Dresden, Dresden, Germany

                                                                      Rasha Faqeh
                                                              TU Dresden, Dresden, Germany

                                                                     Christof Fetzer
                                                              TU Dresden, Dresden, Germany

                                                                    Markus Krötzsch
                                                              TU Dresden, Dresden, Germany

                                                              Christoph Weidenbach
                                                       Max Planck Institute for Informatics
                                               Saarland Informatics Campus, Saarbrücken, Germany
                                                                            July 8, 2021


                                                                               Abstract
                                              The Bernays-Schönfinkel first-order logic fragment over simple linear real arith-
                                          metic constraints BS(SLR) is known to be decidable. We prove that BS(SLR) clause
                                          sets with both universally and existentially quantified verification conditions (con-
                                          jectures) can be translated into BS(SLR) clause sets over a finite set of first-order
                                          constants. For the Horn case, we provide a Datalog hammer preserving validity and
                                          satisfiability. A toolchain from the BS(LRA) prover SPASS-SPL to the Datalog
                                          reasoner VLog establishes an effective way of deciding verification conditions in
                                          the Horn fragment. This is exemplified by the verification of supervisor code for a
                                          lane change assistant in a car and of an electronic control unit for a supercharged
                                          combustion engine.




                                                                                   1
                                                         Environment

                                           Processing
                 Sensors                                                                                     Actuators
                                              units




                                                                                                                         Execute Action
                                              P1                           Reasoner                             A1
    Raw Data




                                                                                   Facts + Rules
                                                                       New Facts
                           Observations                 Suggest                                    Request
                                                        Actions




                                                                                                               ...
                                              ...
                                                                                                   Action
                  ...




                                                        & provide
                                                        Explications
                                                                         Supervisor
                                              Pn                                                                Am




                                          Figure 1: The supervisor architecture.



1              Introduction
Modern dynamic dependable systems (e.g., autonomous driving) continuously update
software components to fix bugs and to introduce new features. However, the safety re-
quirement of such systems demands software to be safety certified before it can be used,
which is typically a lengthy process that hinders the dynamic update of software. We
adapt the continuous certification approach [17] of variants of safety critical software
components using a supervisor that guarantees important aspects through challenging,
see Fig. 1. Specifically, multiple processing units run in parallel – certified and updated
not-certified variants that produce output as suggestions and explications. The supervi-
sor compares the behavior of variants and analyses their explications. The supervisor
itself consists of a rather small set of rules that can be automatically verified and run
by a reasoner. The reasoner helps the supervisor to check if the output of an updated
variant is in agreement with the output of a respective certified variant. The absence of
discrepancy between the two variants for a long-enough period of running both variants
in parallel allows to dynamically certify it as a safe software variant.
     While supervisor safety conditions formalized as existentially quantified properties
can often already be automatically verified, conjectures about invariants formalized as
universally quantified properties are a further challenge. In this paper we show that
supervisor safety conditions and invariants can be automatically proven by a Datalog
hammer. Analogous to the Sledgehammer project [7] of Isabelle [30] translating higher-
order logic conjectures to first-order logic (modulo theories) conjectures, our Datalog
hammer translates first-order Horn logic modulo arithmetic conjectures into pure Dat-
alog programs, equivalent to Horn Bernays-Schönfinkel clause fragment, called HBS.
     More concretely, the underlying logic for both formalizing supervisor behavior
and formulating conjectures is the hierarchic combination of the Bernays-Schönfinkel
first-order fragment with real linear arithmetic, BS(LRA), also called Superlog for
Supervisor Effective Reasoning Logics [17]. Satisfiability of BS(LRA) clause sets is
undecidable [15, 23], in general, however, the restriction to simple linear real arithmetic
BS(SLR) yields a decidable fragment [19, 22]. Our first contribution is decidability of
BS(SLR) with respect to universally quantified conjectures, Section 3, Lemma 12.
     Inspired by the test point method for quantifier elimination in arithmetic [27] we


                                                                2
show that instantiation with a finite number of first-order constants is sufficient to decide
whether a universal/existential conjecture is a consequence of a BS(SLR) clause set.
     For our experiments of the test point approach we consider two case studies: veri-
fication conditions for a supervisor taking care of multiple software variants of a lane
change assistant in a car and a supervisor for a supercharged combustion engine, also
called an ECU for Electronical Control Unit. The supervisors in both cases are formu-
lated by BS(SLR) Horn clauses, the HBS(SLR) fragment. Via our test point technique
they are translated together with the verification conditions to Datalog [1] (HBS). The
translation is implemented in our Superlog reasoner SPASS-SPL. The resulting Datalog
clause set is eventually explored by the Datalog engine VLog [11]. This hammer con-
stitutes a decision procedure for both universal and existential conjectures. The results
of our experiments show that we can verify non-trivial existential and universal conjec-
tures in the range of seconds while state-of-the-art solvers cannot solve all problems in
reasonable time. This constitutes our second contribution, Section 5.
Related Work: Reasoning about BS(LRA) clause sets is supported by SMT (Satisfi-
ability Modulo Theories) [29, 14]. In general, SMT comprises the combination of a
number of theories beyond LRA such as arrays, lists, strings, or bit vectors. While SMT
is a decision procedure for the BS(LRA) ground case, universally quantified variables
can be considered by instantiation [34]. Reasoning by instantiation does result in a refu-
tationally complete procedure for BS(SLR), but not in a decision procedure. The Horn
fragment HBS(LRA) out of BS(LRA) is receiving additional attention [20, 6], because
it is well-suited for software analysis and verification. Research in this direction also
goes beyond the theory of LRA and considers minimal model semantics in addition, but
is restricted to existential conjectures. Other research focuses on universal conjectures,
but over non-arithmetic theories, e.g., invariant checking for array-based systems [12]
or considers abstract dedidability criteria incomparable with the HBS(LRA) class [33].
Hierarchic superposition [2] and Simple Clause Learning over Theories [9] (SCL(T))
are both refutationally complete for BS(LRA). While SCL(T) can be immediately
turned into a decision procedure for even larger fragments than BS(SLR) [9], hierar-
chic superposition needs to be refined by specific strategies or rules to become a decision
procedure already because of the Bernays-Schönfinkel part [21]. Our Datalog hammer
translates HBS(SLR) clause sets with both existential and universal conjectures into
HBS clause sets which are also subject to first-order theorem proving. Instance generat-
ing approaches such as iProver [25] are a decision procedure for this fragment, whereas
superposition-based [2] first-order provers such as E [37], SPASS [41], Vampire [35],
have additional mechanisms implemented to decide HBS. In our experiments, Section 5,
we will discuss the differences between all these approaches on a number of benchmark
examples in more detail.
     The paper is organized as follows: after a section on preliminaries, Section 2, we
present the theory of our new Datalog hammer in Section 3. Section 4 introduces
our two case studies followed by experiments on respective verification conditions,
Section 5. The paper ends with a discussion of the obtained results and directions
for future work, Section 6. This paper is an extended version of [8]. Binaries of our
tools, and all benchmark problems, can be found under https://github.com/knowsys/
eval-datalog-arithmetic.




                                             3
2     Preliminaries
We briefly recall the basic logical formalisms and notations we build upon. We use
a standard first-order language with constants (denoted 𝑎, 𝑏, 𝑐), without non-constant
function symbols, variables (denoted 𝑤, 𝑥, 𝑦, 𝑧), and predicates (denoted 𝑃, 𝑄, 𝑅) of
some fixed arity. Terms (denoted 𝑡, 𝑠) are variables or constants. We write 𝑥¯ for a
vector of variables, 𝑎¯ for a vector of constants, and so on. An atom (denoted 𝐴, 𝐵) is an
expression 𝑃( 𝑡¯) for a predicate 𝑃 of arity 𝑛 and a term list 𝑡¯ of length 𝑛. A positive literal
is an atom 𝐴 and a negative literal is a negated atom ¬𝐴. We define comp( 𝐴) = ¬𝐴,
comp(¬𝐴) = 𝐴, | 𝐴| = 𝐴 and |¬𝐴| = 𝐴. Literals are usually denoted 𝐿, 𝐾, 𝐻.
    A clause is a disjunction of literals, where all variables are assumed to be universally
quantified. 𝐶, 𝐷 denote clauses, and 𝑁 denotes a clause set. We write atoms(𝑋) for the
set of atoms in a clause or clause set 𝑋. A clause is Horn if it contains at most one
positive literal, and a unit clause if it has exactly one literal. A clause 𝐴1 ∨ . . . ∨ 𝐴𝑛 ∨
¬𝐵1 ∨ . . . ∨ ¬𝐵𝑚 can be written as an implication 𝐴1 ∧ . . . ∧ 𝐴𝑛 → 𝐵1 ∨ . . . ∨ 𝐵𝑚 , still
omitting universal quantifiers. If 𝑌 is a term, formula, or a set thereof, vars(𝑌 ) denotes
the set of all variables in 𝑌 , and 𝑌 is ground if vars(𝑌 ) = ∅. A fact is a ground unit
clause with a positive literal.
Datalog and the Bernays-Schönfinkel Fragment: The Bernays-Schönfinkel fragment
(BS) comprises all sets of clauses. The more general form of BS in first-order logic
allows arbitrary formulas over atoms, i.e., arbitrary Boolean connectives and leading
existential quantifiers. However, both can be polynomially removed with common syn-
tactic transformations while preserving satisfiability and all entailments that do not refer
to auxiliary constants and predicates introduced in the transformation [31]. Sometimes,
we still refer explicitly to formulas when it is more beneficial to apply these transfor-
mations after some other processing steps. BS theories in our sense are also known
as disjunctive Datalog programs [16], specifically when written as implications. A set
of Horn clauses is also called a Datalog program. (Datalog is sometimes viewed as a
second-order language. We are only interested in query answering, which can equiva-
lently be viewed as first-order entailment or second-order model checking [1].) Again,
it is common to write clauses as implications in this case.
     Two types of conjectures, i.e., formulas we want to prove as consequences of a clause
set, are of particular interest: universal conjectures ∀𝑥𝜙
                                                         ¯ and existential conjectures ∃𝑥𝜙,
                                                                                          ¯
where 𝜙 is any Boolean combination of BS atoms that only uses variables in 𝑥.       ¯
     A substitution 𝜎 is a function from variables to terms with a finite domain dom(𝜎) =
{𝑥 | 𝑥𝜎 ≠ 𝑥} and codomain codom(𝜎) = {𝑥𝜎 | 𝑥 ∈ dom(𝜎)}. We denote substitutions
by 𝜎, 𝛿, 𝜌. The application of substitutions is often written postfix, as in 𝑥𝜎, and
is homomorphically extended to terms, atoms, literals, clauses, and quantifier-free
formulas. A substitution 𝜎 is ground if codom(𝜎) is ground. Let 𝑌 denote some term,
literal, clause, or clause set. 𝜎 is a grounding for 𝑌 if 𝑌 𝜎 is ground, and 𝑌 𝜎 is a ground
instance of 𝑌 in this case. We denote by gnd(𝑌 ) the set of all ground instances of 𝑌 , and
by gnd 𝐵 (𝑌 ) the set of all ground instances over a given set of constants 𝐵. The most
general unifier mgu(𝑍1 , 𝑍2 ) of two terms/atoms/literals 𝑍1 and 𝑍2 is defined as usual,
and we assume that it does not introduce fresh variables and is idempotent.
     We assume a standard first-order logic model theory, and write A |= 𝜙 if an
interpretation A satisfies a first-order formula 𝜙. A formula 𝜓 is a logical consequence
of 𝜙, written 𝜙 |= 𝜓, if A |= 𝜓 for all A such that A |= 𝜙. Sets of clauses are semantically
treated as conjunctions of clauses with all variables quantified universally.
BS with Linear Arithmetic: The extension of BS with linear arithmetic over real


                                               4
numbers, BS(LRA), is the basis for the formalisms studied in this paper. For simplicity,
we assume a one-sorted extension where all terms in BS(LRA) are of arithmetic sort
LA, i.e., represent numbers. The language includes free first-order logic constants that
are eventually interpreted by real numbers, but we only consider initial clause sets
without such constants, called pure clause sets. Satisfiability of pure BS(LRA) clause
sets is semi-decidable, e.g., using hierarchic superposition [2] or SCL(T) [9]. Impure
BS(LRA) is no longer compact and satisfiability becomes undecidable, but it can be
made decidable when restricting to ground clause sets [18], which is the result of our
grounding hammer.
Example 1. The following BS(LRA) clause from our ECU case study compares the
values of speed (Rpm) and pressure (KPa) with entries in an ignition table (IgnTable)
to derive the basis of the current ignition value (IgnDeg1):
   𝑥1 < 0 ∨ 𝑥 1 ≥ 13 ∨ 𝑥 2 < 880 ∨ 𝑥 2 ≥ 1100 ∨ ¬KPa(𝑥3 , 𝑥1 ) ∨
                                                                                        (1)
   ¬Rpm(𝑥4 , 𝑥2 ) ∨ ¬IgnTable(0, 13, 880, 1100, 𝑧) ∨ IgnDeg1(𝑥3 , 𝑥4 , 𝑥1 , 𝑥2 , 𝑧)
     Terms of sort LA are constructed from a set X of variables, a set of first-order
arithmetic constants, the set of integer constants 𝑐 ∈ Z, and binary function sym-
bols + and − (written infix). Atoms in BS(LRA) are either first-order atoms (e.g.,
IgnTable(0, 13, 880, 1100, 𝑧)) or (linear) arithmetic atoms (e.g., 𝑥2 < 880). Arithmetic
atoms may use the predicates ≤, <, ≠, =, >, ≥, which are written infix and have the
expected fixed interpretation. Predicates used in first-order atoms are called free. First-
order literals and related notation is defined as before. Arithmetic literals coincide
with arithmetic atoms, since the arithmetic predicates are closed under negation, e.g.,
comp(𝑥2 ≥ 1100) = 𝑥2 < 1100.
     BS(LRA) clauses and conjectures are defined as for BS but using BS(LRA) atoms.
We often write clauses in the form Λ k 𝐶 where 𝐶 is a clause solely built of free
first-order literals and Λ is a multiset of LRA atoms. The semantics of k is implication
where Λ denotes a conjunction, e.g., the clause 𝑥 > 1 ∨ 𝑦 ≠ 5 ∨ ¬𝑄(𝑥) ∨ 𝑅(𝑥, 𝑦) is also
written 𝑥 ≤ 1, 𝑦 = 5||¬𝑄(𝑥) ∨ 𝑅(𝑥, 𝑦). For 𝑌 a term, literal, or clause, we write ints(𝑌 )
for the set of all integers that occur in 𝑌 .
     A clause or clause set is pure if it does not contain first-order arithmetic constants,
and it is abstracted if its first-order literals contain only variables. Every clause 𝐶 is
equivalent to an abstracted clause that is obtained by replacing each non-variable term
𝑡 that occurs in a first-order atom by a fresh variable 𝑥 while adding an arithmetic
atom 𝑥 ≠ 𝑡 to 𝐶. We asssume abstracted clauses for theory development, but we prefer
non-abstracted clauses in examples for readability,e.g., a fact 𝑃(3, 5) is considered in
the development of the theory as the clause 𝑥 = 3, 𝑥 = 5||𝑃(𝑥, 𝑦), this is important when
collecting the necessary test points.
     The semantics of BS(LRA) is based on the standard model ALRA of linear arith-
metic, which has the domain LAA = R and which interprets all arithmetic predicates
                                     LRA


and functions in the usual way. An interpretation of BS(LRA) coincides with ALRA on
arithmetic predicates and functions, and freely interprets free predicates and first-order
arithmetic constants. For pure clause sets this is well-defined [2]. Logical satisfaction
and entailment is defined as usual, and uses similar notation as for BS.
Simpler Forms of Linear Arithmetic: The main logic studied in this paper is obtained
by restricting BS(LRA) to a simpler form of linear arithmetic. We first introduce a
simpler logic BS(SLR) as a well-known fragment of BS(LRA) for which satisfiability
is decidable [19, 22], and then present the generalization BS(LRA) PP of this formalism
that we will use.


                                             5
Definition 2. The Bernays-Schönfinkel fragment over simple linear arithmetic, BS(SLR),
is a subset of BS(LRA) where all arithmetic atoms are of form 𝑥 ⊳ 𝑐 or 𝑑 ⊳ 𝑐, such that
𝑐 ∈ Z, 𝑑 is a (possibly free) constant, 𝑥 ∈ X , and ⊳ ∈ {≤, <, ≠, =, >, ≥}.

Example 3. The ECU use case leads to BS(LRA) clauses such as

    𝑥1 < 𝑦 1 ∨ 𝑥1 ≥ 𝑦 2 ∨ 𝑥2 < 𝑦 3 ∨ 𝑥2 ≥ 𝑦 4 ∨ ¬KPa(𝑥3 , 𝑥1 ) ∨
                                                                                               (2)
    ¬Rpm(𝑥4 , 𝑥2 ) ∨ ¬IgnTable(𝑦 1 , 𝑦 2 , 𝑦 3 , 𝑦 4 , 𝑧) ∨ IgnDeg1(𝑥 3 , 𝑥4 , 𝑥1 , 𝑥2 , 𝑧).

This clause is not in BS(SLR), e.g., since 𝑥1 > 𝑥5 is not allowed in BS(SLR). However,
clause (1) of Example 1 is a BS(SLR) clause that is an instance of (2), obtained by
the substitution {𝑦 1 ↦→ 0, 𝑦 2 ↦→ 13, 𝑦 3 ↦→ 880, 𝑦 4 ↦→ 1100}. This grounding will
eventually be obtained by resolution on the IgnTable predicate, because it occurs only
positively in ground unit facts.

     Example 3 shows that BS(SLR) clauses can sometimes be obtained by instantiation.
Relevant instantiations can be found by resolution, in our case by hierarchic resolution,
which supports arithmetic constraints: given clauses Λ1 k 𝐿 ∨ 𝐶1 and Λ2 k 𝐾 ∨ 𝐶2 with
𝜎 = mgu(𝐿, comp(𝐾)), their hierarchic resolvent is (Λ1 , Λ2 k 𝐶1 ∨ 𝐶2 )𝜎. A refutation
is the sequence of resolution steps that produces a clause Λ k ⊥ with ALRA |= Λ𝛿 for
some grounding 𝛿. Hierarchic resolution is sound and refutationally complete for pure
BS(LRA), since every set 𝑁 of pure BS(LRA) clauses 𝑁 is sufficiently complete [2],
and hence hierarchic superposition is sound and refutationally complete for 𝑁 [2, 5].
Resolution can be used to eliminate predicates that do not occur recursively:
Definition 4 (Positively Grounded Predicate). Let 𝑁 be a set of BS(LRA) clauses.
A free first-order predicate 𝑃 is a positively grounded predicate in 𝑁 if all positive
occurrences of 𝑃 in 𝑁 are in ground unit clauses (also called facts).
     For a positively grounded predicate 𝑃 in a clause set 𝑁, let elim(𝑃, 𝑁) be the clause
set obtained from 𝑁 by resolving away all negative occurrences of 𝑃 in 𝑁 and finally
eliminating all clauses where 𝑃 occurs negatively. We need to keep the 𝑃 facts for the
generation of test points. Then 𝑁 is satisfiable iff elim(𝑃, 𝑁) is satisfiable. We can extend
elim to sets of positively grounded predicates in the obvious way. If 𝑛 is the number of
𝑃 unit clauses in 𝑁, 𝑚 the maximal number of negative 𝑃 literals in a clause in 𝑁, and
𝑘 the number of clauses in 𝑁 with a negative 𝑃 literal, then | elim(𝑃, 𝑁)| ≤ |𝑁 | + 𝑘 · 𝑛𝑚 ,
i.e., elim(𝑃, 𝑁) is exponential in the worst case.
     We further assume that elim simplifies LRA atoms until they contain at most
one integer number and that LRA atoms that can be evaluated are reduced to true
and false and the respective clause simplified. For example, given the pure and ab-
stracted BS(LRA) clause set 𝑁 = {IgnTable(0, 13, 880, 1100, 2200), 𝑥 1 ≤ 𝑥2 ∨
𝑧2 ≥ 𝑧 1 k ¬IgnTable(𝑥1 , 𝑥2 , 𝑦 1 , 𝑦 2 , 𝑧1 ) ∨ R(𝑧 2 )}, the predicate IgnTable is posi-
tively grounded. Then elim(IgnTable, 𝑁) = {𝑧 2 ≥ 2200 k R(𝑧 2 )} where the unifier
𝜎 = {𝑥1 ↦→ 0, 𝑥2 ↦→ 13, 𝑦 1 ↦→ 880, 𝑦 2 ↦→ 110, 𝑧1 ↦→ 2200} is used to eliminate the
literal ¬IgnTable(𝑥1 , 𝑥2 , 𝑦 1 , 𝑦 2 , 𝑧1 ) and (𝑥1 ≤ 𝑥 2 )𝜎 becomes true and can be removed.
Definition 5 (Positively Grounded BS(SLR): BS(SLR) P). A clause set 𝑁 is out of
the fragment positively grounded BS(SLR), BS(SLR) P if elim(𝑆, 𝑁) is out of the
BS(SLR) fragment, where 𝑆 is the set of all positively grounded predicates in 𝑁.

    Pure BS(SLR) P clause sets are called BS(SLR) PP and are the starting point for
our Datalog hammer.


                                                 6
Lemma 6. Let A be an interpretation satisfying the clause set elim(𝑆, 𝑁). Then we can
                                                           0
construct a satisfying interpretation A0 for 𝑁 such that 𝑃A = { 𝑎¯ ∈ R𝑛 | 𝑃( 𝑎)
                                                                             ¯ ∈ 𝑁 } if
                         0
𝑃 ∈ 𝑆 and otherwise 𝑃A = 𝑃A .

Proof. By contradiction. Assume that A0 2 𝑁. Then there must exist a clause (Λ k
𝐶) ∈ 𝑁 and a grounding 𝜏 : 𝑋 → R such that A0 2 (Λ k 𝐶)𝜏. We can split the
clause 𝐶 = 𝐷 ∨ 𝐷 0 into two clauses 𝐷 and 𝐷 0 such that 𝐷 contains all literals ¬𝑃( 𝑡¯)
from 𝐶 with 𝑃 ∈ 𝑆. The clause 𝐷 0 does not contain any positive literals 𝑃( 𝑡¯) with
𝑃 ∈ 𝑆 or else Λ k 𝐶 would simplify to a fact 𝑃( 𝑎)¯ ∈ 𝑁 that is satisfied by A0. Since
  A0
𝑃 = { 𝑎¯ ∈ R | 𝑃( 𝑎)
              𝑛       ¯ ∈ 𝑁 } for 𝑃 ∈ 𝑆, we can also assume that any literal ¬𝑃( 𝑎)¯ in
                                                                              0
𝐷𝜎 must correspond to a fact 𝑃( 𝑎)  ¯ ∈ 𝑁 or 𝐷 would be satisfied by 𝑃A . This set
of facts can be defined as 𝑆 0 = {𝑃( 𝑎)
                                      ¯ | ¬𝑃( 𝑎)
                                               ¯ ∈ 𝐷𝜎}. As a result, there exists a
clause (Λ0 k 𝐶 0) ∈ elim(𝑆, 𝑁) such that (Λ0 k 𝐶 0) is the result of resolving (Λ k 𝐷 0)
with 𝑆 0; which also means that (Λ0 k 𝐶 0)𝜏 is equivalent to (Λ k 𝐷 0)𝜏. Moreover,
A0  (Λ0 k 𝐶 0) · 𝜏 because A0 behaves the same as A on all clauses without any literal
over a 𝑃 ∈ 𝑆. Hence, A0  (Λ k 𝐶)𝜏 which is a contradiction to our initial assumption,
so A0  𝑁.                                                                            
Lemma 7. Every interpretation A that satisfies the clause set 𝑁 also satisfies elim(𝑆, 𝑁).
Proof. By soundness of hierarchic resolution.                                            


3    The Theory of the Hammer
We define two hammers that help us solve BS(SLR) PP clause sets with both universally
and existentially quantified conjectures. Both are equisatisfiability preserving and allow
us to abstract BS(SLR) PP formulas into less complicated logics with efficient and
complete decision procedures.
    The first hammer, also called grounding hammer, translates any BS(SLR) PP clause
set 𝑁 with a universally/existentially quantified conjecture into an equisatisfiable ground
and no longer pure BS(SLR) clause set over a finite set of first-order constants called
test points. This means we reduce a quantified problem over an infinite domain into a
ground problem over a finite domain. The size of the ground problem grows worst-case
exponentially in the number of variables and the number of numeric constants in 𝑁 and
the conjecture. For the Horn case, HBS(SLR) PP, we define a Datalog hammer, i.e. a
transformation into an equisatisfiable Datalog program that is based on the same set
of test points but does not require an overall grounding. It keeps the original clauses
almost one-to-one instead of greedily computing all ground instances of those clauses
over the test points. The Datalog hammer adds instead a finite set of Datalog facts
that correspond to all theory atoms over the given set of test points. With the help
of these facts and the original rules, the Datalog reasoner can then derive the same
conclusions as it could have done with the ground HBS(SLR) clause set, however, all
groundings that do not lead to new ground facts are neglected. Therefore, the Datalog
approach is much faster in practice because the Datalog reasoner wastes no time (and
space) on trivially satisfied ground rules that would have been part of the greedily
computed ground HBS(SLR) clause set. Moreover, Datalog reasoners are well suited
to the resulting structure of the problem, i.e. many facts but a small set of rules.
    Note that we never compute or work on elim(𝑆, 𝑁) although the discussed clause sets
are positively grounded. We only refer to elim(𝑆, 𝑁) because it allows us to formulate
our theoretical results more concisely. We avoid working on elim(𝑆, 𝑁) because it often


                                            7
increases the number of non-fact clauses (by orders of magnitude) in order to simplify the
positively grounded theory atoms to variable bounds. This is bad in practice because the
number of non-fact clauses has a high impact on the performance of Datalog reasoners.
Our Datalog hammer resolves this problem by dealing with the positively grounded
theory atoms in a different way that only introduces more facts instead of non-fact
clauses. This is better in practice because Datalog reasoners are well suited to handling
a large number of facts. Since the grounding hammer is meant primarily as a stepping
stone towards the Datalog hammer, we also defined it in such a way that it avoids
computing and working on elim(𝑆, 𝑁).

3.0.1   Hammering BS(SLR) Clause Sets with a Universal Conjecture:
Our first hammer, takes a BS(SLR) PP clause set 𝑁 and a universal conjecture ∀𝑦¯ .𝜙
as input and translates it into a ground BS(SLR) formula. We will later show that the
cases for no conjecture and for an existential conjecture can be seen as special cases
of the universal conjecture. Since 𝜙 is a universal conjecture, we assume that 𝜙 is a
quantifier-free pure BS(SLR) formula and vars(𝜙) = vars( 𝑦¯ ). Moreover, we denote by
𝑆 the set of positively grounded predicates in 𝑁 and assume that none of the positively
grounded predicates from 𝑆 appear in 𝜙. There is not much difference developing the
hammer for the Horn or the non-Horn case. Therefore, we present it for the general
non-Horn case, although our second Datalog hammer is restricted to Horn. Note that
a conjecture ∀𝑦¯ .𝜙 is a consequence of 𝑁, i.e. 𝑁 |= ∀𝑦¯ .𝜙, if ∀𝑦¯ .𝜙 is satisfied by every
interpretation A that also satisfies 𝑁, i.e. ∀A.(A |= 𝑁 → ∀𝑦¯ .𝜙). Conversely, ∀𝑦¯ .𝜙 is
not a consequence of 𝑁 if there exists a counter example, i.e. one interpretation A that
satisfies 𝑁 but does not satisfy ∀𝑦¯ .𝜙, or formally: ∃A.(A |= 𝑁 ∧ ∃ 𝑦¯ .¬𝜙).
     Our hammer is going to abstract the counter example formulation into a ground
BS(SLR) formula. This means the hammered formula will be unsatisfiable if and only
if the conjecture is a consequence of 𝑁. The abstraction to the ground case works
because we can restrict our solution space from the infinite reals to a finite set of test
points and still preserve satisfiability. To be more precise, we partition R into intervals
such that any variable bound in elim(𝑆, 𝑁) and 𝜙 either satisfies all points in one such
interval 𝐼 or none. Then we pick 𝑚 = max(1, | vars(𝜙)|) test points from each of those
intervals because any counter example, i.e. any assignment for ¬𝜙, contains at most 𝑚
different points per interval.
     We get the interval partitioning by first determining the necessary set of interval
borders based on the variable bounds in elim(𝑆, 𝑁) and 𝜙. Then, we sort and combine
the borders into actual intervals. The interval borders are extracted as follows: We turn
every variable bound 𝑥 ⊳ 𝑐 with ⊳ ∈ {≤, <, >, ≥} in elim(𝑆, 𝑁) and 𝜙 into two interval
borders. One of them is the interval border implied by the bound itself and the other
its negation, e.g., 𝑥 ≥ 5 results in the interval border [5 and the interval border of the
negation 5). Likewise, we turn every variable bound 𝑥 ⊳ 𝑐 with ⊳ ∈ {=, ≠} into all four
possible interval borders for 𝑐, i.e. 𝑐), [𝑐, 𝑐], and (𝑐. The set of interval endpoints C is
then defined as follows:
  C=     {𝑐], (𝑐 | 𝑥 ⊳ 𝑐 ∈ atoms(elim(𝑆, 𝑁)) ∪ atoms(𝜙) where ⊳ ∈ {≤, =, ≠, >}} ∪
         {𝑐), [𝑐 | 𝑥 ⊳ 𝑐 ∈ atoms(elim(𝑆, 𝑁)) ∪ atoms(𝜙) where ⊳ ∈ {≥, =, ≠, <}} ∪
         {(−∞, ∞)}

 It is not necessary to compute elim(𝑆, 𝑁) to compute C. It is enough to iterate over all
theory atoms in 𝑁 and compute all of their instantiations in elim(𝑆, 𝑁) based on the
facts in 𝑁 for predicates in 𝑆. This can be done in 𝑂 (𝑛𝑡 · 𝑛 𝐴 · 𝑛𝑆𝑛𝑣 ), where 𝑛 𝑣 is the


                                             8
maximum number of variables in any theory atom in 𝑁, 𝑛 𝐴 is the number of theory
atoms in 𝑁, 𝑛𝑆 is the number of facts in 𝑁 for predicates in 𝑆, and 𝑛𝑡 is the size of the
largest theory atom in 𝑁 with respect to the number of symbols.
    The intervals themselves can be constructed by sorting C in an ascending order
such that we first order by the border value—i.e. 𝛿 < 𝜖 if 𝛿 ∈ {𝑐), [𝑐, 𝑐], (𝑐}, 𝜖 ∈
{𝑑), [𝑑, 𝑑], (𝑑}, and 𝑐 < 𝑑—and then by the border type—i.e. 𝑐) < [𝑐 < 𝑐] < (𝑐.
The result is a sequence [. . . , 𝛿𝑙 , 𝛿𝑢 , . . .], where we always have one lower border 𝛿𝑙 ,
followed by one upper border 𝛿𝑢 . We can guarantee that an upper border 𝛿𝑢 follows a
lower border 𝛿𝑙 because C always contains 𝑐) together with [𝑐 and 𝑐] together with (𝑐
for 𝑐 ∈ Z, so always two consecutive upper and lower borders. Together with (−∞ and
∞) this guarantees that the sorted C has the desired structure. If we combine every two
subsequent borders 𝛿𝑙 , 𝛿𝑢 in our sorted sequence [. . . , 𝛿𝑙 , 𝛿𝑢 , . . .], then we receive our
partition of intervals I. For instance, if 𝑥 < 5 and 𝑥 = 0 are the only variable bounds
in elim(𝑆, 𝑁) and 𝜙, then C = {5), [5, 0), [0, 0], (0, (−∞, ∞)} and if we sort it we get
{(−∞, 0), [0, 0], (0, 5), [5, ∞)}.
Corollary 8. Let ⊳ ∈ {<, ≤, =, ≠, ≥, >}. For each interval 𝐼 ∈ I, every two points
𝑎, 𝑏 ∈ 𝐼, and every variable bound 𝑥 ⊳ 𝑐 ∈ atoms(elim(𝑆, 𝑁)) ∪ atoms(𝜙), 𝑎 ⊳ 𝑐 if and
only if 𝑏 ⊳ 𝑐.
    The above Corollary states that two points 𝑎, 𝑏 ∈ 𝐼 belonging to the same interval
𝐼 ∈ I satisfy the same theory atoms in elim(𝑆, 𝑁) and 𝜙. However, two points 𝑎, 𝑏 ∈ 𝐼
do not necessarily satisfy the same non-theory atom under an arbitrary interpretation A;
not even if A satisfies 𝑁 ∧ ∃ 𝑦¯ .¬𝜙. E.g., A may evaluate 𝑃(𝑎) to true and 𝑃(𝑏) to false.
Sometimes this is even necessary or we would be unable to find a counter example:
Example 9. Let 𝜙 = (0 ≤ 𝑥, 𝑥 ≤ 1, 0 ≤ 𝑦, 𝑦 ≤ 1||¬𝑃(𝑥) ∨ 𝑃(𝑦)) be our conjecture and
𝑁 = ∅ be our clause set. Informally, the property ∀𝑥, 𝑦.𝜙 states that 𝑃 must be uniform
over the interval [0, 1], i.e. either all points in the interval [0, 1] satisfy 𝑃 or none do.
As a result, all interpretations that are uniform over [0, 1] ∈ I also satisfy ∀𝑥, 𝑦.𝜙.
However, there still exist counter examples that are not uniform, e.g., 𝑃A = {0}, which
satisfies 𝑁 but not ∀𝑥, 𝑦.𝜙 because it evaluates 𝑃(0) to true and 𝑃(𝑎) to false for all
𝑎 ∈ [0, 1] \ {0}.
    To better understand the above example, let us look again at the counter example
formulation 𝑁 ∧ ∃ 𝑦¯ .¬𝜙. This formula is satisfiable, i.e. we have a counter example to
our conjecture ∀𝑦¯ .𝜙 if there exists an interpretation A and a grounding 𝜌 for 𝜙 (also
called an assignment for 𝜙) such that A satisfies 𝑁 and ¬𝜙𝜌. In the worst case, the
assignment 𝜌 maps to 𝑚 = | vars(𝜙)| different points in one of the intervals 𝐼 ∈ I. Each
of those 𝑚 points may "act" differently in the interpretation A although it belongs to the
same interval. On the one hand, this means that we need in the worst case 𝑚 = | vars(𝜙)|
different test points for each interval in I. On the other hand, we will show in the proof of
Lemma 11 that we can always find a counter example, where (i) no more than 𝑚 points
per interval act differently and (ii) the actual value of a point does not matter as long as
it belongs to the same interval 𝐼 ∈ I. This is owed mainly to Corollary 8, i.e. that the
points in an interval act at least the same in the theory atoms. We ensure that a test point
𝑎 belongs to a certain interval 𝐼 by adding a set of variable bounds to our formula. We
define these bounds with the functions ilbd and iubd that turn intervals into lower and
upper bounds: ilbd((−∞, 𝑢), 𝑥) = ∅, ilbd((−∞, 𝑢], 𝑥) = ∅, ilbd((𝑙, 𝑢), 𝑥) = {𝑙 < 𝑥},
ilbd((𝑙, 𝑢], 𝑥) = {𝑙 < 𝑥}, ilbd( [𝑙, 𝑢), 𝑥) = {𝑙 ≤ 𝑥}, ilbd( [𝑙, 𝑢], 𝑥) = {𝑙 ≤ 𝑥} for 𝑙 ≠ −∞;
iubd((𝑙, ∞), 𝑥) = ∅, iubd( [𝑙, ∞), 𝑥) = ∅, iubd((𝑙, 𝑢), 𝑥) = {𝑥 < 𝑢}, iubd((𝑙, 𝑢], 𝑥) =
{𝑥 ≤ 𝑢}, iubd( [𝑙, 𝑢), 𝑥) = {𝑥 < 𝑢}, iubd( [𝑙, 𝑢], 𝑥) = {𝑥 ≤ 𝑢} for 𝑢 ≠ ∞.


                                               9
    Note that this test point scheme would no longer be possible if we were to allow
general inequalities.Even allowing difference constraints, i.e., inequalities of the form 𝑥−
𝑦 ≤ 𝑐, would turn the search for a counter example into an undecidable problem [15, 23],
because variables can now interact both on the first-order and the theory side.
    As a result of these observations, we construct the hammered formula 𝜓, also called
the finite abstraction of 𝑁 ∧∃ 𝑦¯ .¬𝜙, as follows. First we fix the following notations for the
remaining subsection: I is the interval partition for 𝑁 and 𝜙; I= = {𝐼 ∈ I | 𝐼 = [𝑙, 𝑙]}
is the set of all intervals from I that are just points; I∞ = I \ I= is the set of all
intervals that are not just points and therefore contain infinitely many values; 𝑚 =
max(1, | vars(𝜙)|) is the number of test points needed per interval with infinitely many
values; 𝐵 = {𝑎 𝐼 ,1 |𝐼 ∈ I= } ∪ {𝑎 𝐼 , 𝑗 |𝐼 ∈ I∞ and 𝑗 = 1, . . . , 𝑚} is the set of test points for
our abstraction such that we have one test point  Ð per interval 𝐼 ∈ I=Ðand 𝑚 different test
points for each interval 𝐼 ∈ I∞ ; idef(𝐵) = 𝑎𝐼 ,𝑖 ∈𝐵 ilbd(𝐼, 𝑎 𝐼 ,𝑖 ) ∪ 𝑎𝐼 ,𝑖 ∈𝐵 iubd(𝐼, 𝑎 𝐼 ,𝑖 )
is a set of bounds that defines to which interval each constant belongs; and 𝜓 =
                          Ô
gnd 𝐵 (𝑁) ∪ idef (𝐵) ∧ ( 𝜌:vars( 𝜙)→𝐵 ¬𝜙𝜌) is the finite abstraction of 𝑁 ∧ ∃ 𝑦¯ .¬𝜙.
    The hammered formula 𝜓 contains gnd 𝐵 (𝑁), i.e. a ground clause (Λ k 𝐶)𝜎 for
every clause (Λ k 𝐶) ∈ 𝑁 and every assignment 𝜎 : vars(Λ k 𝐶) → 𝐵. This means any
deduction over the tests points 𝐵 we could have performed with theÔ           set of clauses 𝑁 can
also be performed with the set of clauses gnd 𝐵 (𝑁) in 𝜓. Similarly, 𝜌:vars( 𝜙)→𝐵 ¬𝜙𝜌 is
a big disjunction over all assignments of 𝜌 for 𝜙 that assign its variables to test points.
Hence, 𝜓 is satisfiable if there exists a counter example for 𝑁 ∧ ∃ 𝑦¯ .¬𝜙 that just uses the
test points 𝐵. Although the finite abstraction is restricted to the test points 𝐵, it is easy
to extend any of its interpretations to all of R and our original formula. We just have to
interpret all values in an interval that are not test points like one of the test points:
Lemma 10. Let A0 be an interpretation satisfying the finite abstraction 𝜓 of 𝑁 ∧∃ 𝑦¯ .¬𝜙.
Moreover, let 𝜌 : vars(𝜙) → 𝐵 be a substitution such that A0 satisfies ¬𝜙𝜌. Then the
interpretation A satisfies 𝑁 ∧ ∃ 𝑦¯ .¬𝜙 if it is constructed as follows:
                                                                          0
𝑃A = { 𝑎¯ ∈ R𝑛 | 𝑃( 𝑎)  ¯ ∈ 𝑁 } if 𝑃 ∈ 𝑆 and 𝑃A = { 𝑎¯ ∈ R𝑛 | 𝑎𝜎    ¯ ∈ 𝑃A } if 𝑃 ∉ 𝑆 and
                0                           0                0
𝜎 = {𝑎 ↦→ 𝑎 A                            A                A
             𝐼 ,1 | 𝐼 ∈ I and 𝑎 ∈ 𝐼 \ {𝑎 𝐼 ,2 , . . . , 𝑎 𝐼 ,𝑚 }}.
Proof. Before we start with the actual proof, we need to define a second substitution
                                                   0             A0                              A0
𝜎 0 = {𝑎 ↦→ 𝑎 𝐼 ,1 | 𝐼 ∈ I and 𝑎 ∈ 𝐼 \ {𝑎 A     𝐼 ,2 , . . . , 𝑎 𝐼 ,𝑚 }} ∪ {𝑎 ↦→ 𝑎 𝐼 , 𝑗 | 𝑎 = 𝑎 𝐼 , 𝑗 } that
maps any point 𝑎 in one of our intervals 𝐼, either to the test point 𝑎 𝐼 , 𝑗 that is interpreted
                           0
by A0 as 𝑎 (i.e. 𝑎 = 𝑎 A𝐼 , 𝑗 ) or to the default test point for the interval 𝑎 𝐼 ,1 . Then we split
the proof into two parts: 1) we show that A satisfies 𝑁; 2) after that we show that there
exists a 𝜌 0 such that A satisfies ¬𝜙𝜌 0.
1) Instead of directly showing that A satisfies 𝑁, we show that A satisfies elim(𝑆, 𝑁).
Thanks to Lemma 6, we then also know that A satisfies 𝑁. Note that A satisfies
elim(𝑆, 𝑁) is equivalent to A satisfies (Λ k 𝐶)𝜏 for all (Λ k 𝐶) ∈ elim(𝑆, 𝑁) and
all groundings 𝜏 : vars(Λ k 𝐶) → R. However, for any (Λ k 𝐶) ∈ elim(𝑆, 𝑁) and
any grounding 𝜏 : vars(Λ k 𝐶) → R, we can construct an alternative grounding to 𝐵
instead of R
                              𝜏 0 = {𝑥 ↦→ (𝑥𝜏𝜎 0) | 𝑥 ∈ vars(Λ k 𝐶)}
                 0
that applies 𝜎 to the result values of 𝜏, which means we map the result values to their
corresponding values in our set of test points 𝐵. We know that A0 |= (Λ k 𝐶)𝜏 0 because
A0 |= 𝜓 and there exists a (Λ0 k 𝐶 0) ∈ gnd 𝐵 (𝑁) and a set of ground facts 𝑆 0 ∈ gnd 𝐵 (𝑁)
that resolve to (Λ k 𝐶)𝜏 0 by definition of elim(𝑆, 𝑁). Due to the definition of A, we
                                                         0
also know that 𝑎¯ ∈ 𝑃A if and only if 𝑎𝜎   ¯ ∈ 𝑃A . Similarly, Corollary 8 and the definition
of the 𝑎 𝐼 ,𝑖 ∈ 𝐵 imply that 𝑎 ∈ R satisfies a variable bound from elim(𝑆, 𝑁) if and only
if 𝑎𝜎 satisfies it. Therefore, A |= (Λ k 𝐶)𝜏 if and only if A0 |= (Λ k 𝐶)𝜏 0. Hence, A


                                                    10
satisfies elim(𝑆, 𝑁) and by Lemma 6 also 𝑁.
2) We start by constructing a substitution from the variables of 𝜙 to R: 𝜌 0 = {𝑦 𝑖 ↦→
    0
𝑎A                                                        0         0
 𝐼 , 𝑗 | 𝑦 𝑖 𝜌 = 𝑎 𝐼 , 𝑗 }. By definition, A satisfies ¬𝜙𝜌 because A satisfies ¬𝜙𝜌.
Now the two subproofs combined prove that A is satisfying 𝑁 ∧ ∃ 𝑦¯ .¬𝜙.              
     Similarly, we can extend any interpretation A satisfying 𝑁 ∧ ∃ 𝑦¯ .¬𝜙 into an inter-
pretation satisfying 𝜓. We just have to pick one assignment 𝜌 0 : vars(𝜙) → R such that
A satisfies ¬𝜙𝜌 0 and pick one test point 𝐵 for each point in codom(𝜌 0) and interpret it
as its corresponding point in codom(𝜌 0).

Lemma 11. Let A be an interpretation satisfying the formula 𝑁 ∧ ∃ 𝑦¯ .¬𝜙. Then we can
construct an interpretation A0 that satisfies its finite abstraction 𝜓.
Proof. If A satisfies 𝑁 ∧ ∃ 𝑦¯ .¬𝜙, then A satisfies 𝑁 and there exists a 𝜌 0 : vars(𝜙) → R
such that A also satisfies ¬𝜙𝜌 0. We extend the interpretation A so it also satisfies 𝜓
by interpreting some of our test points 𝐵 as points in 𝐵 0 = codom(𝜌 0) and all other
test points as random values 𝑎 𝐼 ∈ 𝐼 \ 𝐵 0 belonging to their corresponding interval 𝐼.
Explicitly this means that we extend the interpretation A to our constants 𝐵 as follows:
𝑎A                       0             0                              A                      0
  𝐼 , 𝑗 := 𝑏 𝑗 if 𝑗 ≤ |𝐵 ∩ 𝐼 | and 𝐵 ∩ 𝐼 = {𝑏 1 , . . . , 𝑏 𝑘 }; 𝑎 𝐼 , 𝑗 := 𝑎 𝐼 if 𝑗 > |𝐵 ∩ 𝐼 |.
                                                                        0      0
This means if 𝑘 points {𝑏 1 , . . . , 𝑏 𝑘 } in the codomain 𝐵 of 𝜌 belong to the interval
𝐼, then the first 𝑘 test points 𝑎 𝐼 ,1 , . . . , 𝑎 𝐼 ,𝑘 are interpreted as 𝑏 1 , . . . , 𝑏 𝑘 and all other
test points 𝑎 𝐼 , 𝑗 as 𝑎 𝐼 . As a result, the extended interpretation A will have one test point
𝑎 𝐼 , 𝑗 ∈ 𝐵 for every 𝑏 ∈ 𝐵 0 that will be interpreted by A as 𝑏. Next, we construct an
assignment 𝜌 ∗ for 𝜙 that ranges into 𝐵 such that A satisfies ¬𝜙𝜌 ∗ . The assignment
𝜌 ∗ := {𝑥 ↦→ 𝑎 𝐼 , 𝑗 | 𝑥 ∈ vars(𝜙) and 𝑥 𝜌 0 = 𝑎 A      𝐼 , 𝑗 } is almost the same as our assignment
𝜌 0 that falsified our conjecture over R, except that the result values of 𝜌 0 are swapped
with their corresponding test points in 𝐵. By definition of the extended A, A satisfies
gnd 𝐵 (𝑁) because A satisfies 𝑁. Due to the way we extended A over the constants 𝐵, A
                                                                      ∗       0                          ∗
also satisfies eachÔ bound in idef(𝐵).   By definition of 𝜌 and 𝜌 , A also satisfies ¬𝜙𝜌
and therefore         𝜌:vars( 𝜙)→𝐵 ¬𝜙𝜌 . Hence, the extended A satisfies 𝜓.                             

    If we combine both results, we get that 𝑁 ∧ ∃ 𝑦¯ .¬𝜙 is equisatisfiable to 𝜓:
Lemma 12. 𝑁 ∧ ∃ 𝑦¯ .¬𝜙 has a satisfying interpretation if and only if its finite abstraction
𝜓 has a satisfying interpretation.
Proof. The first part of the equivalence follows from Lemma 10. The second part
follows from Lemma 11.                                                       

    The finite abstraction for the case with a universal conjecture can also be used to
construct a finite abstraction for the case without a conjecture and the case with an
existential conjecture. Let 𝑁 be a BS(SLR) PP clause set and let 𝑆 be the set of all
positively grounded predicates in 𝑁. 𝑁 is satisfiable if and only if 𝑁 6 |= ⊥. Hence,
we get a finite abstraction for 𝑁 if we build one for 𝑁 |= ⊥, which can be treated as a
universal conjecture because all variables in ⊥ are universally quantified. The existential
case works similarly: 𝑁 |= ∃ 𝑦¯ .𝜙 if and only if 𝑁 ∪ 𝑁 0 |= ⊥, where 𝑁 0 is the universal
BS(SLR) clause set we get from applying a CNF transformation [31] to ∀𝑦¯ .¬𝜙.
Example 13. We finish the presentation of our first hammer by applying it to two
examples 𝑁 |= ∀𝑥, 𝑦.𝜙1 and 𝑁 |= ∀𝑥, 𝑦.𝜙2 . For the examples we choose
       𝑁 := {0 ≤ 𝑥, 𝑥 ≤ 2 k ¬𝑃(𝑥) ∨ 𝑄(𝑥), 𝑥 ≤ 1 k 𝑃(𝑥), 𝑥 > 1 k ¬𝑃(𝑥)}
as our set of clauses and check two different conjectures


                                                   11
                              𝜙1 := 0 ≤ 𝑥, 𝑥 ≤ 1, 0 ≤ 𝑦, 𝑦 ≤ 1 k ¬𝑄(𝑥) ∨ 𝑄(𝑦)
      and
                             𝜙2 := 1 < 𝑥, 𝑥 ≤ 2, 1 < 𝑦, 𝑦 ≤ 2 k ¬𝑄(𝑥) ∨ 𝑄(𝑦).
       The conjecture 𝜙1 is true if 𝑄 is always interpreted uniformly over the interval [0, 1],
       i.e. for every interpretation A satisfying 𝑁 either A evaluates 𝑄 to true for all points
       in [0, 1] (𝑄 A = [0, 1]) or to false for all points in [0, 1] (𝑄 A = ∅). The conjec-
       ture 𝜙2 states almost the same property except that 𝑄 has to be interpreted uni-
       formly over the interval (1, 2]. We now construct for both examples their finite ab-
       straction. To this end, we first compute their sets of interval endpoints, which are
       both equivalent because 𝑁 has no positively grounded predicates and all variable
       bounds in our conjectures 𝜙1 and 𝜙2 also appear in 𝑁. The variable bounds in 𝑁 are
       0 ≤ 𝑥, 𝑥 ≤ 2, 𝑥 ≤ 1, 𝑥 > 1. As a result, we get as the set of interval endpoints
       C = {0), [0, 2], (2, 1], (1, (−∞, ∞)}. Next we sort an recombine the endpoints in C, and
       receive the interval partition I = {(−∞, 0), [0, 1], (1, 2], (2, ∞)}. Since our conjec-
       tures contain two variables, we need two test points/constants for each interval. There-
       fore, 𝐵 = {𝑎 (−∞,0) ,1 , 𝑎 (−∞,0),2 , 𝑎 [0,1],1 , 𝑎 [0,1],2 , 𝑎 (1,2],1 ,Ô𝑎 (1,2],2 , 𝑎 (2,∞) ,1 , 𝑎 (2,∞) ,2 }. For
       both finite abstractions Ô    𝜓1 = gnd 𝐵 (𝑁) ∪ idef (𝐵) ∧ ( 𝜌:vars( 𝜙1 )→𝐵 ¬𝜙1 𝜌) and 𝜓2 =
       gnd 𝐵 (𝑁) ∪ idef(𝐵) ∧ ( 𝜌:vars( 𝜙2 )→𝐵 ¬𝜙2 𝜌), gnd 𝐵 (𝑁) and idef(𝐵) are the same. As
       mentioned before, idef(𝐵) formally defines that each 𝑎 𝐼 , 𝑗 must be interpreted as a value
       in its respective interval 𝐼 with the help of variable bounds:
           idef(𝐵) := { 𝑎 (−∞,0),1 < 0, 𝑎 (−∞,0),2 < 0, 0 ≤ 𝑎 [0,1],1 , 𝑎 [0,1],1 ≤ 1, 0 ≤ 𝑎 [0,1],2 ,
                            𝑎 [0,1],2 ≤ 1, 1 < 𝑎 (1,2],1 , 𝑎 (1,2],1 ≤ 2, 1 < 𝑎 (1,2],2 , 𝑎 (1,2],2 ≤ 2,
                            2 < 𝑎 (2,∞) ,1 , 2 < 𝑎 (2,∞) ,2 }
       gnd 𝐵 (𝑁) defines all groundings of the clauses 𝑁 over the set of test points 𝐵, i.e.
          gnd 𝐵 (𝑁) := { 0 ≤ 𝑎 (−∞,0),1 , 𝑎 (−∞,0),1 ≤ 2 k ¬𝑃(𝑎 (−∞,0),1 ) ∨ 𝑄(𝑎 (−∞,0),1 ), . . . ,
                              0 ≤ 𝑎 (2,∞),2 , 𝑎 (2,∞) ,2 ≤ 2 k ¬𝑃(𝑎 (2,∞) ,2 ) ∨ 𝑄(𝑎 (2,∞) ,2 ),
                              𝑎 (−∞,0),1 ≤ 1 k 𝑃(𝑎 (−∞,0),1 ), . . . , 𝑎 (2,∞) ,2 ≤ 1 k 𝑃(𝑎 (2,∞) ,2 ),
                              𝑎 (−∞,0),1 > 1 k ¬𝑃(𝑎 (−∞,0),1 ), . . . , 𝑎 (2,∞) ,2 > 1 k ¬𝑃(𝑎 (2,∞),2 )}
       Note that half of the clauses (Λ k 𝐶) ∈ gnd 𝐵 (𝑁) are trivially satisfied because the in-
       equalities in idef (𝐵) ensure that Λ is not satisfiable, e.g. 𝑎 (−∞,0),1 > 1 k ¬𝑃(𝑎 (−∞,0),1 )
       is trivially satisfied because 𝑎 (−∞,0),1 > 1 and (𝑎 (−∞,0),1 < 0) ∈ idef(𝐵) contradict each
       other. As a result, we can remove those clauses without loss of generality. Similarly, all
       other clauses (Λ k 𝐶) ∈ gnd 𝐵 (𝑁) satisfy their theory atoms Λ if we take the inequalities
       in idef(𝐵) into account, e.g. in 0 ≤ 𝑎 (1,2],1 , 𝑎 (1,2],1 ≤ 2 k ¬𝑃(𝑎 (1,2],1 ) ∨ 𝑄(𝑎 (1,2],1 )
       the inequalities (1 < 𝑎 (1,2],1 ) ∈ idef(𝐵) and (𝑎 (1,2],1 ≤ 2) ∈ idef (𝐵) ensure that
       0 ≤ 𝑎 (1,2],1 and 𝑎 (1,2],1 ≤ 2. Therefore, we can remove their theory atoms without loss
       of generality, i.e. simplify Λ k 𝐶 into 𝐶. So at least for our intuitive understanding, we
       can simplify gnd 𝐵 (𝑁) to
                 𝑁𝐺 = { ¬𝑃(𝑎 [0,1],1 ) ∨ 𝑄(𝑎 [0,1],1 ), ¬𝑃(𝑎 [0,1],2 ) ∨ 𝑄(𝑎 [0,1],2 ),
                           ¬𝑃(𝑎 (1,2],1 ) ∨ 𝑄(𝑎 (1,2],1 ), ¬𝑃(𝑎 (1,2],2 ) ∨ 𝑄(𝑎 (1,2],2 ),
                            𝑃(𝑎 (−∞,0),1 ), 𝑃(𝑎 (−∞,0),2 ), 𝑃(𝑎 [0,1],1 ), 𝑃(𝑎 [0,1],2 ),
                           ¬𝑃(𝑎 (1,2],1 ), ¬𝑃(𝑎 (1,2],2 ), ¬𝑃(𝑎 (2,∞) ,1 ), ¬𝑃(𝑎 (2,∞) ,2 )}
Ô The finite abstractions       ∗
                                   do, however, differ in the groundings of their two conjectures:
    𝜌:vars( 𝜙1 )→𝐵 ¬𝜙1 𝜌 := 𝜙1 :=                                                                                           
¬ 0 ≤ 𝑎 (−∞,0),1 , 𝑎 (−∞,0),1 ≤ 1, 0 ≤ 𝑎 (−∞,0),1 , 𝑎 (−∞,0) ,1 ≤ 1 k ¬𝑄(𝑎 (−∞,0),1 ) ∨ 𝑄(𝑎 (−∞,0),1 )  ∨
¬ 0 ≤ 𝑎 (−∞,0) ,1 , 𝑎 (−∞,0),1 ≤ 1, 0 ≤ 𝑎 (−∞,0),2 , 𝑎 (−∞,0),2 ≤ 1 k ¬𝑄(𝑎 (−∞,0) ,1 ) ∨ 𝑄(𝑎 (−∞,0),2                   ) ∨
¬ 0 ≤ 𝑎 (−∞,0),1 , 𝑎 (−∞,0),1 ≤ 1, 0 ≤ 𝑎 [0,1],1 , 𝑎 [0,1],1 ≤ 1 k ¬𝑄(𝑎 (−∞,0) ,1 ) ∨ 𝑄(𝑎 [0,1],1 ) ∨ 
. . . ∨ ¬ 0 ≤ 𝑎 (2,∞) ,2 , 𝑎 (2,∞) ,2 ≤ 1, 0 ≤ 𝑎 (2,∞) ,2 , 𝑎 (2,∞),2 ≤ 1 k ¬𝑄(𝑎 (2,∞) ,2 ) ∨ 𝑄(𝑎 (2,∞) ,2 )




                                                            12
Ô                            ∗
    𝜌:vars( 𝜙2 )→𝐵 ¬𝜙2 𝜌 := 𝜙2 :=                                                                                
¬ 1 < 𝑎 (−∞,0),1 , 𝑎 (−∞,0),1 ≤ 2, 1 < 𝑎 (−∞,0),1 , 𝑎 (−∞,0),1 ≤ 2 k ¬𝑄(𝑎 (−∞,0),1 ) ∨ 𝑄(𝑎 (−∞,0),1 )  ∨
¬ 1 < 𝑎 (−∞,0),1 , 𝑎 (−∞,0),1 ≤ 2, 1 < 𝑎 (−∞,0),2 , 𝑎 (−∞,0),2 ≤ 2 k ¬𝑄(𝑎 (−∞,0),1 ) ∨ 𝑄(𝑎 (−∞,0),2        ) ∨
¬ 1 < 𝑎 (−∞,0),1 , 𝑎 (−∞,0),1 ≤ 2, 1 < 𝑎 [0,1],1 , 𝑎 [0,1],1 ≤ 2 k ¬𝑄(𝑎 (−∞,0),1 ) ∨ 𝑄(𝑎 [0,1],1 ) ∨ 
. . . ∨ ¬ 1 < 𝑎 (2,∞) ,2 , 𝑎 (2,∞),2 ≤ 2, 1 < 𝑎 (2,∞) ,2 , 𝑎 (2,∞),2 ≤ 2 k ¬𝑄(𝑎 (2,∞) ,2 ) ∨ 𝑄(𝑎 (2,∞),2 )
       But similarly to gnd 𝐵 (𝑁), we can drastically simplify the groundings of our con-
       jectures if we take idef (𝐵) into account (and some other boolean simplifications). For
       instance ¬(1 < 𝑎 (−∞,0),1 , 𝑎 (−∞,0),1 ≤ 2, 1 < 𝑎 (−∞,0),1 , 𝑎 (−∞,0),1 ≤ 2 k ¬𝑄(𝑎 (−∞,0),1 ) ∨
       𝑄(𝑎 (−∞,0),1 )) simplifies to false because the theory atom 1 < 𝑎 (−∞,0),1 must be false ac-
       cording to idef(𝐵) and therefore (1 < 𝑎 (−∞,0),1 , 𝑎 (−∞,0),1 ≤ 2, 1 < 𝑎 (−∞,0),1 , 𝑎 (−∞,0),1 ≤
       2 k ¬𝑄(𝑎 (−∞,0),1 ) ∨ 𝑄(𝑎 (−∞,0),1 )) is trivially true. So at least for our intuitive under-
                                      Ô
       standing, we can simplify 𝜌:vars( 𝜙1 )→𝐵 ¬𝜙1 𝜌 to
             Ô      𝜙10 := (𝑄(𝑎 [0,1],1 ) ∧ ¬𝑄(𝑎 [0,1],2 )) ∨ (𝑄(𝑎 [0,1],2 ) ∧ ¬𝑄(𝑎 [0,1],1 ))
       and 𝜌:vars( 𝜙2 )→𝐵 ¬𝜙2 𝜌 to
                  𝜙20 := (𝑄(𝑎 (1,2],1 ) ∧ ¬𝑄(𝑎 (1,2],0),2 )) ∨ (𝑄(𝑎 (1,2],2 ) ∧ ¬𝑄(𝑎 (1,2],1 )).
       Now based on these simplifications it is relatively easy to show that 𝑁 |= ∀𝑥, 𝑦.𝜙1 and
       𝑁 6 |= ∀𝑥, 𝑦.𝜙2 . The former is true because we can prove by refutation that 𝜓1 is unsatisfi-
       able. To do so, we simply resolve 𝑃(𝑎 [0,1],1 ) ∈ 𝑁𝐺 with (¬𝑃(𝑎 [0,1],1 ) ∨ 𝑄(𝑎 [0,1],1 )) ∈
       𝑁𝐺 and 𝑃(𝑎 [0,1],2 ) ∈ 𝑁𝐺 with (¬𝑃(𝑎 [0,1],2 ) ∨ 𝑄(𝑎 [0,1],2 )) ∈ 𝑁𝐺 to get 𝑄(𝑎 [0,1],1 )
       and 𝑄(𝑎 [0,1],2 ). Hence, (𝑄(𝑎 [0,1],1 ) ∧ ¬𝑄(𝑎 [0,1],2 )) in 𝜙10 simplifies to false because of
       𝑄(𝑎 [0,1],2 ), (𝑄(𝑎 [0,1],2 ) ∧¬𝑄(𝑎 [0,1],1 )) in 𝜙10 simplifies to false because of 𝑄(𝑎 [0,1],1 ),
       and as a result 𝜙10 overall also simplifies to false. Our second conjectures is not a con-
       sequence, i.e. 𝑁 6 |= ∀𝑥, 𝑦.𝜙2 , because 𝜓2 actually has a satisfying interpretation A with
       𝑃A := {𝑎 (−∞,0),1 , 𝑎 (−∞,0),2 , 𝑎 [0,1],1 , 𝑎 [0,1],2 } and 𝑄 A := {𝑎 [0,1],1 , 𝑎 [0,1],2 , 𝑎 (1,2],1 }.
       This assignment satisfies 𝜓2 and constitutes a counter example for 𝑁 |= ∀𝑥, 𝑦.𝜙2 be-
       cause it satisfies 𝑁 although it assigns 𝑄 for one test point (𝑎 (1,2],1 ) in (1, 2] to true and
       for the other (𝑎 (1,2],2 ) to false. Hence, 𝑁 is not uniform in the interval (1, 2].

      3.0.2   A Datalog Hammer for HBS(SLR) PP:
      The set gnd 𝐵 (𝑁) grows exponentially with regard to the maximum number of variables
      𝑛𝐶 in any clause (Λ k 𝐶) ∈ 𝑁, i.e. 𝑂 (| gnd 𝐵 (𝑁)|) = 𝑂 (|𝑁 | · |𝐵| 𝑛𝐶 ). Since 𝐵 is large
      for realistic examples (e.g., in our examples the size of 𝐵 ranges from 15 to 1609
      constants), the finite abstraction is often too large to be solvable in reasonable time.
      As an alternative approach, we propose a Datalog hammer for the Horn fragment of
      BS(SLR) PP clause sets, called HBS(SLR)PP. This hammer exploits the ideas behind
      the finite abstraction and will allow us to make the same ground deductions, but instead
      of grounding everything, we only need to (i) ground the negated conjecture over our
      test points and (ii) provide a set of ground facts that define which theory atoms are
      satisfied by our test points. As a result, the hammered formula is much more concise
      and we need no actual theory reasoning to solve the formula. In fact, we can solve
      the hammered formula by greedily resolving with all facts (from our set of clauses
      and returned as a result of this process) until this produces the empty clause—which
      would mean the conjecture is implied—or no more new facts—which would mean we
      have found a counter example. (In practice, greedily applying resolution is not the best
      strategy and we recommend to use more advanced techniques for instance those used
      by a state-of-the-art Datalog reasoner.)
           The Datalog hammer takes as input (i) a HBS(SLR)PP clause set 𝑁 (where 𝑆 is the
      set of all positively grounded predicates in 𝑁) and (ii) optionally a universal conjecture
      ∀𝑦¯ .𝑃( 𝑦¯ ) where 𝑃 ∉ 𝑆. Restricting the conjecture to a single positive literal may seem


                                                       13
like a drastic restriction, but we will later show that we can transform any universal
conjecture into this form if it contains only positive atoms. Given this input, the Datalog
hammer first computes the same interval partition I and test point/constant set 𝐵 needed
for the finite abstraction. Then it computes an assignment 𝛽 for the constants in 𝐵 that
corresponds to the interval partition, i.e. 𝑎 𝐼 ,𝑖 𝛽 ∈ 𝐼 and 𝑎 𝐼 ,𝑖 𝛽 ≠ 𝑎 𝐼 , 𝑗 𝛽 if 𝑖 ≠ 𝑗. Next,
it computes three clause sets that will make up the Datalog formula. The first set
tren 𝑁 (𝑁) is computed out of 𝑁 by replacing each theory atom 𝐴 in 𝑁 with a literal
𝑃 𝐴 ( 𝑥),
      ¯ where vars( 𝐴) = vars( 𝑥)   ¯ and 𝑃 𝐴 is a fresh predicate. This is necessary to
eliminate all non-constant function symbols (e.g., +, −) in positively grounded theory
atoms because Datalog does not support non-constant function symbols. (It is possible
to reduce the number of fresh predicates needed, e.g., by reusing the same predicate
for two theory atoms that are equivalent up to variable renaming.) The second set is
empty if we have no universal conjecture or it contains the ground and negated version
𝜙 of our universal conjecture ∀𝑦¯ .𝑃( 𝑦¯ ). Since we restricted the conjecture to a single
positive literal, 𝜙 has the form 𝐶 𝜙 → ⊥, where 𝐶 𝜙 contains all literals 𝑃( 𝑦¯ ) 𝜌 for all
groundings 𝜌 : vars( 𝑦¯ ) → 𝐵. We cannot skip this grounding but the worst-case size of
𝐶 𝜙 is 𝑂 (gnd 𝐵 (𝑁)) = 𝑂 (|𝐵| 𝑛 𝜙 ), where 𝑛 𝜙 = | 𝑦¯ |, which is in our applications typically
much smaller than the maximum number of variables 𝑛𝐶 contained in any clause in 𝑁.
The last set is denoted by tfacts(𝑁, 𝐵) and contains a fact tren 𝑁 ( 𝐴) for every ground
theory atom 𝐴 contained in the theory part Λ of a clause (Λ k 𝐶) ∈ gnd 𝐵 (𝑁) such
that 𝐴𝛽 simplifies to true. (Alternatively, it is also possible to use a set of axioms and
a smaller set of facts and let the Datalog reasoner compute all relevant theory facts
for itself.) The set tfacts(𝑁, 𝐵) can be computed without computing gnd 𝐵 (𝑁) if we
simply iterate over all theory atoms 𝐴 in all constraints Λ of all clauses (Λ k 𝐶) ∈ 𝑁
and compute all groundings 𝜏 : vars( 𝐴) → 𝐵 such that 𝐴𝜏𝛽 simplifies to true. This
can be done in time 𝑂 (𝜇(𝑛 𝑣 ) · 𝑛 𝐿 · |𝐵| 𝑛𝑣 ) and the resulting set tfacts(𝑁, 𝐵) has worst-
case size 𝑂 (𝑛 𝐴 · |𝐵| 𝑛𝑣 ), where 𝑛 𝐿 is the number of literals in 𝑁, 𝑛 𝑣 is the maximum
number of variables | vars( 𝐴)| in any theory atom 𝐴 in 𝑁, 𝑛 𝐴 is the number of different
theory atoms in 𝑁, and 𝜇(𝑥) is the time needed to simplify a theory atom over 𝑥
variables to a variable bound. Please note that already satifiability testing for BS clause is
NEXPTIME-complete in general, and DEXPTIME-complete for the Horn case [26, 32].
So when abstracting to a polynomially decidable clause set (ground HBS) an exponential
factor is unavoidable.
Lemma 14. 𝑁 ∧∃ 𝑦¯ .¬𝑃( 𝑦¯ ) is equisatisfiable to its hammered version 𝑁 𝐷 = tren 𝑁 (𝑁) ∪
tfacts(𝑁, 𝐵) ∪{𝜙}. 𝑁 is equisatisfiable to its hammered version tren 𝑁 (𝑁) ∪tfacts(𝑁, 𝐵).
Proof. Let Π0 be the set of new predicate symbols introduced by tren 𝑁 . We will
prove that 𝜓 = gnd 𝐵 (𝑁) ∪ idef(𝐵) ∪ {𝜙}, the finite abstraction of 𝑁 ∧ ∃ 𝑦¯ .¬𝑃( 𝑦¯ ), is
equisatisfiable to 𝑁 𝐷 = tren 𝑁 (𝑁) ∪ tfacts(𝑁, 𝐵) ∪ {𝜙}. Then we get from Lemma 12
that 𝑁 ∧ ∃ 𝑦¯ .¬𝑃( 𝑦¯ ) is equisatisfiable to its hammered version. (The case for 𝑁 without
conjecture works exactly the same.)
⇒: Let A be an interpretation satisfying 𝜓. Then we can extend A over Π0 so it also
satisfies 𝑁 𝐷 . The extension sets exactly those arguments for 𝑃 𝐴 ∈ Π0 to true that appear
in tfacts(𝑁, 𝐵), i.e. if 𝑃 𝐴 ∈ Π0, then 𝑃A          A
                                                             ¯ ∈ tfacts(𝑁, 𝐵)}. As a result, A
                                            𝐴 = { 𝑎¯ | 𝑃 𝐴 ( 𝑎)
automatically satisfies tfacts(𝑁, 𝐵) and A also trivially satisfies 𝜙 because it also appears
in 𝜓. Moreover, we can proof that A satisfies any clause 𝐷 ∨ 𝐶 ∈ gnd 𝐵 (tren 𝑁 (𝑁)) by
case distinction over the corresponding clause Λ k 𝐶 ∈ gnd 𝐵 (𝑁) with tren 𝑁 (Λ) = ¬𝐷:
since A satisfies Λ k 𝐶 (i) either A satisfies 𝐶 or (ii) A does not satisfy Λ and therefore
one of the atoms 𝑃( 𝑎)    ¯ in tren 𝑁 (Λ) does not appear in tfacts(𝑁, 𝐵) by definition of
tfacts and thus 𝐷 that contains ¬𝑃( 𝑎)   ¯ is satisfied by A. Hence, A satisfies tren 𝑁 (𝑁).


                                               14
⇐: Let A be an interpretation satisfying 𝑁 𝐷 . Let 𝛽 be the assignment for the constants in
𝐵 that was used in the construction of 𝑁 𝐷 such that 𝑎 𝐼 ,𝑖 𝛽 ∈ 𝐼 and 𝑎 𝐼 ,𝑖 𝛽 ≠ 𝑎 𝐼 , 𝑗 𝛽 if 𝑖 ≠ 𝑗.
Then there exists an interpretation A0 that satisfies 𝜓. A0 interprets each constant 𝑎 𝐼 ,𝑖
                                                 0
in 𝐵 as 𝑎 𝐼 ,𝑖 𝛽 and each predicate 𝑃 ∈ Π as 𝑃A = { 𝑎𝛽 ¯ | 𝑎¯ ∈ 𝑃A }. By definition of 𝛽, A0
                                               0
satisfies idef(𝐵). As in the previous case, A satisfies 𝜙 because 𝜙 appears in 𝑁 𝐷 and A
satisfies 𝑁 𝐷 . Moreover, we can proof that A0 satisfies any clause (Λ k 𝐶) ∈ gnd 𝐵 (𝑁)
by case distinction over the corresponding clause (𝐷 ∨ 𝐶) ∈ gnd 𝐵 (tren 𝑁 (𝑁)) with
tren 𝑁 (Λ) = ¬𝐷: since A satisfies 𝐷 ∨ 𝐶 (i) either A satisfies 𝐶 and therefore A0
satisfies 𝐶 or (ii) A satisfies 𝐷 and therefore at least one of the atoms 𝑃( 𝑎) ¯ = tren 𝑁 ( 𝐴)
with 𝐴 ∈ Λ does not appear in tfacts(𝑁, 𝐵), which can only be that case if 𝐴𝛽 simplifies
to false and thus Λ is not satisfied by A0. Hence, A also satisfies gnd 𝐵 (𝑁).                    
    Note that tren 𝑁 (𝑁) ∪ tfacts(𝑁, 𝐵) ∪ {𝜙} is actually a HBS clause set over a finite
set of constants 𝐵 and not yet a Datalog input file. It is well known that such a formula
can be transformed easily into a Datalog problem by adding a nullary predicate Goal
and adding it as a positive literal to any clause without a positive literal. Querying for
the Goal atom returns true if the HBS clause set was unsatisfiable and false otherwise.

3.0.3    Positive Conjectures:
One of the seemingly biggest restrictions of our Datalog hammer is that it only accepts
universal conjectures over a single positive literal ∀𝑦¯ .𝑃( 𝑦¯ ). We made this restriction
because it is the easiest way to guarantee that our negated and finitely abstracted goal
takes the form of a Horn clause. However, there is a way to express any positive universal
conjecture — i.e. any universal conjecture where all atoms have positive polarity —
as a universal conjecture over a single positive literal. (Note that any negative theory
literal can be turned into a positive theory literal by changing the predicate symbol, e.g.,
¬(𝑥 ≤ 5) ≡ (𝑥 > 5).) Similarly as in a typical first-order CNF transformation [31], we
can simply rename all subformulas, i.e. recursively replace all subformulas with some
some fresh predicate symbols and add suitable Horn clause definitions for these new
predicates to our clause set 𝑁.
      Let ∀𝑦¯ .𝜙 0 be a universal conjecture where all atoms have positive polarity. Then
we define the functions rflat(𝜙 0) and pflat(𝜙 0) recursively as follows: pflat(𝜙 0) returns
an atom 𝑃 𝜙0 ( 𝑥)  ¯ over a fresh predicate 𝑃 𝜙0 for any formula 𝜙 0 with vars(𝜙 0) = vars( 𝑥)             ¯
that is not just a free first-order atom and otherwise the atom itself. rflat(𝜙 0) on the
other hand introduces a set of new rules that define the fresh predicates 𝑃 𝜙0 : rflat(𝜙 0) :=
{(pflat(𝜙10 ), . . . , pflat(𝜙 𝑚
                               0 ) → pflat(𝜙 0 ))} ∪ rflat(𝜙 0 ) ∪ . . . ∪ rflat(𝜙 0 ) if 𝜙 0 = 𝜙 0 ∧ . . . ∧
                                                                1                  𝑚             1
𝜙 𝑚 , rflat(𝜙 ) := {(pflat(𝜙10 ) → pflat(𝜙 0)), . . . , (pflat(𝜙 𝑚
   0           0                                                    0 ) → pflat(𝜙 0 ))} ∪ rflat(𝜙 0 ) ∪
                                                                                                       1
. . . ∪ rflat(𝜙 𝑚0 ) if 𝜙 0 = 𝜙 0 ∨ . . . ∨ 𝜙 0 , rflat(𝜙 0 ) := {(Λ k→ pflat(𝜙 0 ))} if 𝜙 0 = Λ is a
                                 1            𝑚
conjunction of theory atoms, and rflat(𝜙 0) := ∅ if 𝜙 0 is a free first-order atom.

Lemma 15. Let A be an interpretation that satisfies 𝑁. Let 𝜏 : vars(𝜙∗ ) → R be a
grounding for 𝜙 0. Then A |= 𝜙 0 𝜏 if and only if (A ∧ rflat(𝜙 0)) |= pflat(𝜙 0)𝜏.
Proof. ⇒: Assume A is an interpretation that satisfies A |= 𝜙 0 𝜏. Then we show
by induction that A ∧ rflat(𝜙 0) |= pflat(𝜙∗ )𝜏 for all subformulas 𝜙∗ of 𝜙 0, where
A |= 𝜙∗ 𝜏. Case 1: if 𝜙∗ is a free first-order atom, then (A ∧ rflat(𝜙 0)) |= pflat(𝜙∗ )𝜏
because pflat(𝜙∗ ) = 𝜙∗ 𝜏. Case 2: if 𝜙∗ = Λ is a conjunction of theory atoms, then
(Λ k→ pflat(𝜙∗ )) ∈ rflat(𝜙 0) and A |= 𝜙∗ 𝜏 entails (A ∧ rflat(𝜙 0)) |= pflat(𝜙∗ )𝜏. Case
3: if 𝜙∗ = 𝜙∗1 ∨ . . . ∨ 𝜙∗𝑚 , then there must exist a 𝜙∗𝑗 with A |= 𝜙∗𝑗 𝜏 and by induction
hypothesis (A ∧ rflat(𝜙 0)) |= pflat(𝜙∗𝑗 )𝜏. Together with (pflat(𝜙∗𝑗 ) → pflat(𝜙∗ )) ∈


                                                    15
rflat(𝜙 0) this means (A ∧ rflat(𝜙 0)) |= pflat(𝜙∗ )𝜏. Case 4: if 𝜙∗ = 𝜙∗1 ∧ . . . ∧ 𝜙∗𝑚 ,
then A |= 𝜙∗𝑗 𝜏 for all 𝜙∗𝑗 and by induction hypothesis (A ∧ rflat(𝜙 0)) |= pflat(𝜙∗𝑗 )𝜏
for all 𝜙∗𝑗 . Together with (pflat(𝜙∗1 ), . . . , pflat(𝜙∗𝑚 ) → pflat(𝜙∗ )) ∈ rflat(𝜙 0) this means
(A ∧ rflat(𝜙 0)) |= pflat(𝜙∗ )𝜏.
⇐: Assume A is an interpretation that satisfies (A ∧ rflat(𝜙 0)) |= rflat(𝜙 0)𝜏. Then we
show by induction that A |= 𝜙∗ 𝜏 for all subformulas 𝜙∗ of 𝜙 0, where (A ∧ rflat(𝜙 0)) |=
pflat(𝜙∗ )𝜏. Case 1: if 𝜙∗ is a free first-order atom, then pflat(𝜙∗ ) = 𝜙∗ only appears as a
negative literal in rflat(𝜙 0). Hence, A |= 𝜙∗ 𝜏. Case 2: if 𝜙∗ = Λ is a conjunction of theory
atoms, then (Λ k→ pflat(𝜙∗ )) ∈ rflat(𝜙 0) is the only clause in 𝑁 ∪ rflat(𝜙 0), where
pflat(𝜙∗ ) appears positively. Hence, A |= 𝜙∗ 𝜏. Case 3: if 𝜙∗ = 𝜙∗1 ∨ . . . ∨ 𝜙∗𝑚 , then there
only exist 𝑚 clauses in rflat(𝜙 0) where pflat(𝜙 0) is positive. This means (A∧rflat(𝜙 0)) |=
pflat(𝜙∗ )𝜏 can only be true if there exist a rule (pflat(𝜙∗𝑗 ) → pflat(𝜙∗ )) ∈ rflat(𝜙 0) with
(A ∧ rflat(𝜙 0)) |= pflat(𝜙∗𝑗 )𝜏 and by induction hypothesis A |= 𝜙∗𝑗 𝜏. However, this also
means A |= 𝜙∗ 𝜏. Case 4: if 𝜙∗ = 𝜙∗1 ∧ . . . ∧ 𝜙∗𝑚 , then (pflat(𝜙∗1 ), . . . , pflat(𝜙∗𝑚 ) →
pflat(𝜙∗ )) ∈ rflat(𝜙 0) is the only clause in rflat(𝜙 0) where pflat(𝜙 0) is positive. This
means (A ∧ rflat(𝜙 0)) |= pflat(𝜙∗ )𝜏 can only be true if (A ∧ rflat(𝜙 0)) |= pflat(𝜙∗𝑗 )𝜏 for
all 𝜙∗𝑗 and by induction hypothesis A |= 𝜙∗𝑗 𝜏. However, this also means A |= 𝜙∗ 𝜏.               
Corollary 16. 𝑁 |= (∀𝑦¯ .𝜙 0) is equivalent to (𝑁 ∪ rflat(𝜙 0)) |= (∀𝑦¯ . pflat(𝜙 0)).
    Using the same technique, we can also express any positive existential conjecture
— i.e. any existential conjecture where all atoms have positive polarity — as additional
clauses in our set of input clauses 𝑁.
Corollary 17. 𝑁 |= (∃ 𝑦¯ .𝜙 0) is equivalent to 𝑁 ∪ rflat(𝜙 0) ∪ (pflat(𝜙 0) → ⊥) is
unsatisfiable.
   As with the first hammer, we also finish the presentation of our second hammer by
applying it to some examples.
Example 18. For our examples, we choose the same set of clauses as in the previous
example
        𝑁 := {0 ≤ 𝑥, 𝑥 ≤ 2 k ¬𝑃(𝑥) ∨ 𝑄(𝑥), 𝑥 ≤ 1 k 𝑃(𝑥), 𝑥 > 1 k ¬𝑃(𝑥)}
Although this set of clauses belongs to the horn fragment, we cannot handle the previous
two conjectures with our Datalog hammer because they are not positive (both contain
the negative literal ¬𝑄(𝑥)). Instead, we will check two different conjectures 𝜙3 :=
0 ≤ 𝑥, 𝑥 ≤ 1 k 𝑄(𝑥) and 𝜙4 := 0 ≤ 𝑥, 𝑥 ≤ 2 k 𝑄(𝑥). 𝑁 |= ∀𝑥.𝜙3 is true if every
interpretation A satisfying 𝑁 interprets 𝑄(𝑎) as true for all 𝑎 ∈ [0, 1]. 𝑁 |= ∀𝑥.𝜙4 is
true if every interpretation A satisfying 𝑁 interprets 𝑄(𝑎) as true for all 𝑎 ∈ [0, 2].
Before we can apply the Datalog hammer, we have to flatten our positive conjectures
to unit clauses. Note that 𝜙3 written via boolean operators instead of our k-notation
looks as follows: 0 > 𝑥 ∨ 𝑥 > 1 ∨ 𝑄(𝑥). Hence, pflat(𝜙3 ) := 𝑅(𝑥) and rflat(𝜙3 ) =
{0 > 𝑥 k 𝑅(𝑥), 𝑥 > 1 k 𝑅(𝑥), 𝑄(𝑥) → 𝑅(𝑥)}. Similarly, pflat(𝜙4 ) := 𝑆(𝑥) and
rflat(𝜙4 ) = {0 > 𝑥 k 𝑆(𝑥), 𝑥 > 2 k 𝑆(𝑥), 𝑄(𝑥) → 𝑆(𝑥)}. Next, we combine
these new clause sets with our initial clause set 𝑁 to get 𝑁3 := 𝑁 ∪ rflat(𝜙3 ) and
𝑁4 := 𝑁 ∪ rflat(𝜙4 ). By Corollary 16, this means that 𝑁 |= ∀𝑥.𝜙3 and 𝑁 |= ∀𝑥.𝜙4 are
equivalent to 𝑁3 |= ∀𝑥.𝑅(𝑥) and 𝑁4 |= ∀𝑥.𝑆(𝑥), respectively. The latter two are now
also in a format to which we can apply the Datalog hammer.
     As the first step of our Datalog hammer, we have to compute the interval par-
tition for both examples. Note, however, that the variable bounds in rflat(𝜙3 ) and
rflat(𝜙4 ) appear in negated form in 𝑁, e.g. 0 > 𝑥 appears in rflat(𝜙3 ) and 0 ≤ 𝑥 ≡


                                                16
¬(0 > 𝑥) appears in 𝑁. This means 𝑁3 and 𝑁4 result in the same interval end-
points as 𝑁 alone. The latter we have already determined in the previous example
as I = {(−∞, 0), [0, 1], (1, 2], (2, ∞)}. In contrast to our previous example, our con-
jectures contain only one variable, so we need only one test point/constant for each
interval. Therefore, 𝐵 = {𝑎 (−∞,0),1 , 𝑎 [0,1],1 , 𝑎 (1,2],1 , 𝑎 (2,∞) ,1 }. As our assignment 𝛽 for
the constants, we can simply pick random points from the respective intervals, e.g.
𝑎 (−∞,0),1 𝛽 = −1, 𝑎 [0,1],1 𝛽 = 0, 𝑎 (1,2],1 𝛽 = 2, and 𝑎 (2,∞) ,1 𝛽 = 3.
      In the next step of the Datalog hammer, we have to replace the inequalities in our
clause sets by fresh predicates. The inequalities in our examples are 0 ≤ 𝑥, 𝑥 ≤ 2,
𝑥 ≤ 1, 𝑥 > 1, 0 > 𝑥, and 𝑥 > 2; we choose as their respective fresh predicates 𝑇0≤𝑥 (𝑥),
𝑇𝑥 ≤2 (𝑥), 𝑇𝑥 ≤1 (𝑥), 𝑇𝑥>1 (𝑥), 𝑇0>𝑥 (𝑥), and 𝑇𝑥>2 (𝑥). As a result, our sets of clauses after
renaming look as follows
       tren 𝑁3 (𝑁3 ) := { ¬𝑇0≤𝑥 (𝑥) ∨ 𝑇𝑥 ≤2 (𝑥) ∨ ¬𝑃(𝑥) ∨ 𝑄(𝑥), ¬𝑇𝑥 ≤1 (𝑥) ∨ 𝑃(𝑥),
                            ¬𝑇𝑥>1 (𝑥) ∨ ¬𝑃(𝑥), ¬𝑇0>𝑥 (𝑥) ∨ 𝑅(𝑥), ¬𝑇𝑥>1 (𝑥) ∨ 𝑅(𝑥),
                            ¬𝑄(𝑥) ∨ 𝑅(𝑥)}
       tren 𝑁4 (𝑁4 ) := { ¬𝑇0≤𝑥 (𝑥) ∨ 𝑇𝑥 ≤2 (𝑥) ∨ ¬𝑃(𝑥) ∨ 𝑄(𝑥), ¬𝑇𝑥 ≤1 (𝑥) ∨ 𝑃(𝑥),
                            ¬𝑇𝑥>1 (𝑥) ∨ ¬𝑃(𝑥), ¬𝑇0>𝑥 (𝑥) ∨ 𝑆(𝑥), ¬𝑇𝑥>2 (𝑥) ∨ 𝑆(𝑥),
                            ¬𝑄(𝑥) ∨ 𝑆(𝑥)}
The groundings of our conjectures are
             𝜙30 := ¬𝑅(𝑎 (−∞,0),1 ) ∨ ¬𝑅(𝑎 [0,1],1 ) ∨ ¬𝑅(𝑎 (1,2],1 ) ∨ ¬𝑅(𝑎 (2,∞) ,1 )
               𝜙40 := ¬𝑆(𝑎 (−∞,0) ,1 ) ∨ ¬𝑆(𝑎 [0,1],1 ) ∨ ¬𝑆(𝑎 (1,2],1 ) ∨ ¬𝑆(𝑎 (2,∞) ,1 )
so simply the disjunction of all negative instances of our conjecture predicate over our
set of test points 𝐵. The sets of theory facts are
    tfacts(𝑁3 , 𝐵) := { 𝑇0≤𝑥 (𝑎 [0,1],1 ), 𝑇0≤𝑥 (𝑎 (1,2],1 ), 𝑇0≤𝑥 (𝑎 (2,∞) ,1 ), 𝑇𝑥 ≤2 (𝑎 (−∞,0),1 ),
                           𝑇𝑥 ≤2 (𝑎 [0,1],1 ), 𝑇𝑥 ≤2 (𝑎 (1,2],1 ), 𝑇𝑥 ≤1 (𝑎 (−∞,0) ,1 ), 𝑇𝑥 ≤1 (𝑎 [0,1],1 ),
                           𝑇𝑥>1 (𝑎 (1,2],1 ), 𝑇𝑥>1 (𝑎 (2,∞),1 ), 𝑇0>𝑥 (𝑎 (−∞,0),1 )}
   tfacts(𝑁4 , 𝐵) := { 𝑇0≤𝑥 (𝑎 [0,1],1 ), 𝑇0≤𝑥 (𝑎 (1,2],1 ), 𝑇0≤𝑥 (𝑎 (2,∞),1 ), 𝑇𝑥 ≤2 (𝑎 (−∞,0),1 ),
                           𝑇𝑥 ≤2 (𝑎 [0,1],1 ), 𝑇𝑥 ≤2 (𝑎 (1,2],1 ), 𝑇𝑥 ≤1 (𝑎 (−∞,0),1 ), 𝑇𝑥 ≤1 (𝑎 [0,1],1 ),
                           𝑇𝑥>1 (𝑎 (1,2],1 ), 𝑇𝑥>1 (𝑎 (2,∞) ,1 ), 𝑇0>𝑥 (𝑎 (−∞,0),1 ), 𝑇𝑥>2 (𝑎 (2,∞) ,1 )}
The last step of our Datalog hammer is to combine these sets of clauses into one big
set of horn clauses for each conjecture: 𝑁 𝐷         3 := tren (𝑁 ) ∪ {𝜙 0 } ∪ tfacts(𝑁 , 𝐵) and
                                                                  𝑁3    3        3                 3
                             0
𝑁 𝐷 := tren 𝑁4 (𝑁4 ) ∪ {𝜙4 } ∪ tfacts(𝑁4 , 𝐵).
   4

      We end this example by proving that (i) the conjecture 𝜙3 is actually a consequence
of 𝑁 and (ii) the conjecture 𝜙4 is not a consequence of 𝑁. We prove that the conjecture
𝜙3 is actually a consequence of 𝑁 by deriving the empty clause from 𝑁 𝐷                            3 , which

proves that 𝑁 𝐷    3 is unsatisfiable (and that there exists no counter example). As our first

resolution step, we will simply resolve with all tfacts. The result will be similar to what
we got, when we simplified the ground clauses in our first hammer with the help of the
inequalities in idef(𝐵) and theory reasoning; we will get rid of all the renamed theory
literals:
             3 := { ¬𝑃(𝑎
           𝑁𝐺                 [0,1],1 ) ∨ 𝑄(𝑎 [0,1],1 ),     ¬𝑃(𝑎 (1,2],1 ) ∨ 𝑄(𝑎 (1,2],1 ),
                        𝑃(𝑎 (−∞,0) ,1 ), 𝑃(𝑎 [0,1],1 ), ¬𝑃(𝑎 (1,2],1 ), ¬𝑃(𝑎 (2,∞) ,1 ),
                        𝑅(𝑎 (−∞,0),1 ), 𝑅(𝑎 (1,2],1 ), 𝑅(𝑎 (2,∞) ,1 )}
Next, we resolve 𝑃(𝑎 [0,1],1 ) with ¬𝑃(𝑎 [0,1],1 ) ∨ 𝑄(𝑎 [0,1],1 ) to get 𝑄(𝑎 [0,1],1 ), followed
by 𝑄(𝑎 [0,1],1 ) with 𝑄(𝑥) ∨ 𝑅(𝑥) to get 𝑅(𝑎 [0,1],1 ). The final step is to resolve 𝜙30 with
𝑅(𝑎 [0,1],1 ) and 𝑅(𝑎 (−∞,0),1 ), 𝑅(𝑎 (1,2],1 ), 𝑅(𝑎 (2,∞) ,1 ) ∈ 𝑁𝐺       3 . The result is the empty

clause.
      Our second conjecture 𝜙4 is not a consequence, i.e. 𝑁 6 |= ∀𝑥.𝜙4 , because 𝑁 𝐷              3 actually
                                                  A                                   A
has a satisfying interpretation A with 𝑃 := {𝑎 (−∞,0),1 , 𝑎 [0,1],1 }, 𝑄 := {𝑎 [0,1],1 } and



                                                    17
𝑅 A := {𝑎 (−∞,0),1 , 𝑎 [0,1],1 , 𝑎 (2,∞),1 }.


4     Two Supervisor Case Studies
We consider two supervisor case studies: a lane change assistant and the ECU of a
supercharged combustion engine; both using the architecture in Fig. 1.
Lane Assistant: This use case focuses on the lane changing maneuver in autonomous
driving scenario i.e., the safe lane selection and the speed. We run two variants of soft-
ware processing units (updated and certified) in parallel with a supervisor. The variants
are connected to different sensors that capture the state of the freeway such as video or
LIDAR signal sensors. The variants process the sensors’ data and suggest the safe lanes
to change to in addition to the evidence that justify the given selection. The supervi-
sor is responsible for the selection of which variant output to forward to other system
components i.e., the execution units (actuators) that perform the maneuver. Variants
categorize the set of available actions for each time frame into safe/unsafe actions and
provide explications. The supervisor collects the variants output and processes them to
reason about (a) if enough evidence is provided by the variants to consider actions safe
(b) find the actions that are considered safe by all variants.
    Variants formulate their explications as facts using first-order predicates. The su-
pervisor uses a set of logical rules formulated in BS(SLR) PP to reason about the
suggestions and the explications (see List. 1). In general, the rules do not belong to the
BS(SLR) PP fragment, e.g., the atom = (𝑥ℎ1, −(𝑥𝑒𝑠, 1)) includes even an arithmetic
calculation. However, after grounding with the facts of the formalization, only simple
bounds remain.
 1 ## Exclude actions per variant if safety disproved or declared unsafe.
 2 SuggestionDisproven(xv, xa), VariantName(xv) -> ExcludedAction(xv, xa).
 3 VariantName(xv), LaneNotSafe(xv, xl, xa)     -> ExcludedAction(xv, xa).
 4 ## Exclude actions for all variants if declared unsafe by the certified

 5 CertifiedVariant(xv1), UpdatedVariant(xv2), LaneNotSafe(xv1, xl, xa)

 6   -> ExcludedAction(xv2,xa).
 7

 8 ## A safe action is disproven
 9 SafeBehindDisproven(xv, xenl, xecl, xecs, xes, xa), LaneSafe(xv, xl, xa),
10   SuggestedAction(xv, xa) -> SuggestionDisproven(xv, xa).
11 SafeFrontDisproven(xv, xenl, xecl, xecs, xes, xa),  LaneSafe(xv, xl, xa),
12   SuggestedAction(xv, xa) -> SuggestionDisproven(xv, xa).
13

14 ## Unsafe left lane: speed decelerated and unsafe distance front
15 >(xh1, xfd), !=(xecl, xenl), =(xh1,-(xes,1)) ||
16   LaneSafe(xv, xenl, adecelerateleft), EgoCar(xv, xecl, xecs, xes),
17   DistanceFront(xv, xenl, xofp, xfd, adecelerateleft),
18   SpeedFront(xv, xenl, xofp, xofs, adecelerateleft)
19   -> SafeFrontDisproven(xv, xenl, xecl, xecs, xes, adecelerateleft).

        List. 1: The rules snippets for the lane changing use case in BS(SLR) PP.

    Variants explications: The SuggestedAction predicate encodes the actions sug-
gested by the variants. LaneSafe and LaneNotSafe specify the lanes that are safe/un-
safe to be used with the different actions. DistanceFront and DistanceBehind pro-
vide the explications related to the obstacle position, while their speeds are SpeedFront


                                                18
and SpeedBehind. EgoCar predicate reports the speed and the position of the ego ve-
hicle.
     Supervisor reasoning: To select a safe action, the supervisor must exclude all unsafe
actions. The supervisor considers actions to be excluded per variant (ExcludedAction)
if (a) SuggestionDisproven; the variant fails to prove that the suggested action is safe
(line 2), or (b) the action is declared unsafe (line 3). The supervisor declares an action
to be excluded cross all variants if the certified variant declares it unsafe (lines 5-6).
To consider an action as SuggestionDisproven, the supervisor must check for each
LaneSafe the existence of unsafe distances between the ego vehicle in the given lane
and the other vehicles approaching either from behind (SafeBehindDisproven) or in
front (SafeFrontDisproven). The rule SafeFrontDisproven (lines 15-19) checks
in the left lane, if using the ego vehicle decelerated speed (=(xh1,-(xes,1))) the
distance between the vehicles is not enough (>(xh1, xfd)). The supervisor checks
ExcludeAction for all variants. If all actions are excluded, the supervisor uses an
emergency action as no safe action exists. Otherwise, selects a safe action from the
not-excluded actions suggested by the updated variant, if not found, by the certified.
ECU: The GM LSJ Ecotec engine (https://en.wikipedia.org/wiki/GM_Ecotec_engine)
is a supercharged combustion engine that was almost exclusively deployed in the US,
still some of those run also in Europe. The main sensor inputs of the LSJ ECU consist
of an inlet air pressure and temperature sensor (in KPa and in degree Celsius), a speed
sensor (in Rpm), a throttle pedal sensor, a throttle sensor, a coolant temperature sensor,
oxygen sensors, a knock sensor, and its main actuators controlling the engine are ignition
and injection timing, and throttle position. For the experiments conducted in this paper
we have taken the routines of the LSJ ECU that compute ignition and injection timings
out of inlet air pressure, inlet air temperature, and engine speed. For this part of the
ECU this is a two stage process where firstly, basic ignition and injection timings are
computed out of engine speed and inlet air pressure and secondly, those are adjusted
with respect to inlet air temperature. The properties we prove are safety properties,
e.g., certain injection timings are never generated and also invariants, e.g., the ECU
computes actuator values for all possible input sensor data and they are unique. Clause 2,
page 6, is an actual clause from the ECU case study computing the base ignition timing.
The adjustments are then done with respect to inlet temperature values. Basically, if the
inlet temperature exceeds a certain value, typically around 80◦ C, then the pre-ignition
is reduced in order to prevent a too early burning of the fuel that might damage the
engine.
    𝑧1 ≥ 𝑦 1 , 𝑥1 ≤ 𝑥, 𝑥 < 𝑥 2 ||¬IgnDeg1(𝑥𝑡 𝑝, 𝑥𝑡𝑟, 𝑥 𝑝, 𝑥𝑟 𝑝𝑚, 𝑧1 ) ∨ ¬Tmp(𝑥, 𝑥) ∨
         ¬TempIgnTabl𝑒(𝑥1 , 𝑥2 , 𝑦 1 , 𝑦 2 ) ∨ IndnDeg2(𝑥𝑡 𝑝, 𝑥𝑡𝑟, 𝑥, 𝑥 𝑝, 𝑥𝑟 𝑝𝑚, 𝑥, 𝑦 2 )
A final third iteration then considers the knock sensor. If knock is detected consistently
over a certain period of time, then the pre-ignition is reduced even further. This iteration
is not yet contained in our formalization.


5    Implementation and Experiments
We have implemented the Datalog hammer into our BS(LRA) system SPASS-SPL and
combined it with the Datalog reasoner Rulewerk. The resulting toolchain is the first
implementation of a decision procedure for HBS(SLR) with positive conjectures.
SPASS-SPL is a new system for BS(LRA) based on some core libraries of the first-order
theorem prover SPASS [41] and including the CDCL(LA) solver SPASS-SATT [10]


                                             19
for mixed linear arithmetic. Eventually, SPASS-SPL will include a family of reasoning
techniques for BS(LRA) including SCL(T) [9], hierarchic superposition [2, 5] and
hammers to various logics. Currently, it comprises the Datalog hammer described
in this paper and hierarchic UR-resolution [28] (Unit Resulting resolution) which is
complete for pure HBS(LRA). The Datalog hammer can produce the clause format
used in the Datalog system Rulewerk (described below), but also the SPASS first-order
logic clause format that can then be translated into the first-order TPTP library [38]
clause format. Moreover, it can be used as a translator from our own input language
into the SMT-LIB 2.6 language [4] and the CHC competition format [36].
    Note that our implementation of the Datalog hammer is of prototypical nature. It
cannot handle positively grounded theory atoms beyond simple bounds, unless they
are variable comparisons (i.e., 𝑥 ⊳ 𝑦 with ⊳ ∈ {≤, <, ≠, =, >, ≥}). Moreover, positive
universal conjectures have to be flattened until they have the form Λ k 𝑃( 𝑥).
                                                                            ¯ On the
other hand, we already added some improvements, e.g., we break/eliminate symmetries
in the hammered conjecture and we exploit the theory atoms Λ in a universal conjecture
Λ k 𝑃( 𝑥)
        ¯ so the hammered conjecture contains only groundings for 𝑃( 𝑥) ¯ that satisfy
Λ.
Rulewerk (formerly VLog4j) is a rule reasoning toolkit that consists of a Java API and
an interactive shell [11]. Its current main reasoning back-end is the rule engine VLog
[39], which supports Datalog and its extensions with stratified negation and existential
quantifiers, respectively. VLog is an in-memory reasoner that is optimized for efficient
use of resources, and has been shown to deliver highly competitive performance in
benchmarks [40].
     We have not specifically optimized VLog or Rulewerk for this work, but we have tried
to select Datalog encodings that exploit the capabilities of these tools. The most notable
impact was observed for the encoding of universal conjectures. A direct encoding of
(grounded) universal claims in Datalog leads to rules with many (hundreds of thousands
in our experiments) ground atoms as their precondition. Datalog reasoners (not just
VLog) are not optimized for such large rules, but for large numbers of facts. An
alternative encoding in plain Datalog would therefore specify the expected atoms as
facts and use some mechanism to iterate over all of them to check for goal. To accomplish
this iteration, the facts that require checking can be endowed with an additional identifier
(given as a parameter), and an auxiliary binary successor relation can be used to specify
the iteration order over the facts. This approach requires only few rules, but the number
of rule applications is proportional to the number of expected facts.
     In Rulewerk/VLog, we can encode this in a simpler way using negation. Universal
conjectures require us to evaluate ground queries of the form entailed( 𝑐¯1 ) ∧ . . . ∧
entailed( 𝑐¯ℓ ), where each entailed( 𝑐¯𝑖 ) represents one grounding of our conjecture over
our set of test points. If we add facts expected( 𝑐¯𝑖 ) for the constant vectors 𝑐¯1 , . . . , 𝑐¯ℓ ,
we can equivalently use a smaller (first-order) query ∀𝑥.(expected(
                                                             ¯              ¯ →
                                                                            𝑥)  entailed( 𝑥)),
                                                                                              ¯
which in turn can be written as ¬ ∃𝑥.(expected(
                                             ¯           ¯ ∧ ¬entailed( 𝑥))
                                                         𝑥)                  ¯ . This can be
expressed in Datalog with negation and the rules expected( 𝑥)    ¯ ∧¬entailed( 𝑥)¯ → missing
and ¬missing → Goal, where Goal encodes that the query matches. This use of negation
is stratified, i.e., not entwined with recursion [1]. Note that stratified negation is a form of
non-monotonic negation, so we can no longer read such rules as first-order formulae over
which we compute entailments. Nevertheless, implementation is simple and stratified
negation is a widely supported feature in Datalog engines, including Rulewerk. The
encoding is particularly efficient since the rules using negation are evaluated only once.
Benchmark Experiments To test the efficiency of our toolchain, we ran benchmark


                                                20
       Problem Q Status 𝑋 𝑌 𝐵    Size   t-time h-time p-time r-time vampire spacer z3        cvc4
       lc_e1   ∃ true 9 3 19      12/30     0.2    0.0    0.1 0.1       0.0    0.0     0.0      0.0
       lc_e2   ∃ false 9 3 17     13/27     0.2    0.0    0.1 0.1       0.0    0.1 timeout timeout
       lc_e3   ∃ false 9 3 15     12/22     0.2    0.0    0.1 0.1       0.0    0.0 timeout timeout
       lc_e4   ∃ true 9 3 21      12/35     0.2    0.0    0.1 0.1       0.0    0.0     0.0      0.1
       lc_u1   ∀ false 9 2 29     12/25     0.2    0.0    0.1 0.1       0.0 N/A timeout timeout
       lc_u2   ∀ false 9 2 26     12/25     0.2    0.0    0.1 0.1       0.0 N/A timeout timeout
       lc_u3   ∀ true 9 2 23      12/22     0.2    0.0    0.1 0.1       0.0 N/A        0.0      0.1
       lc_u4   ∀ false 9 2 32     12/33     0.2    0.0    0.1 0.1       0.0 N/A timeout timeout
       ecu_e1 ∃ false 10 6 311 27/649       1.1    0.1    0.3 0.7       0.5    0.1 timeout timeout
       ecu_e2 ∃ true 10 6 311 27/649        1.1    0.1    0.3 0.7       0.5    0.1     2.4      0.4
       ecu_u1 ∀ true 11 1 310 27/651        1.1    0.1    0.3 0.7      94.6 N/A 145.2           0.3
       ecu_u2 ∀ false 11 1 310 27/651       1.1    0.1    0.3 0.7      80.7 N/A timeout timeout
       ecu_u3 ∀ true 9 2 433 27/1291        1.0    0.1    0.5 0.4      12.0 N/A 209.7           0.1
       ecu_u4 ∀ true 9 2 1609 26/20459 12.4        2.9    3.2 6.3     526.5 N/A 167.7           0.1
       ecu_u5 ∀ true 10 3 629 28/17789 22.6        0.7    2.1 19.8 timeout N/A timeout timeout
       ecu_u6 ∀ false 10 3 618 27/15667 11.6       0.7    1.7 9.1 timeout N/A timeout timeout

                          Figure 2: Benchmark results and statistics


experiments on the two real world HBS(SLR) PP supervisor verification conditions.
The two supervisor use cases are described in Section 4. The names of the problems
are formatted so the lane change assistant examples start with lc and the ECU examples
start with ecu. The lc problems with existential conjectures test whether an action
suggested by an updated variant is contradicted by a certified variant. The lc problems
with universal conjectures test whether an emergency action has to be taken because we
have to exclude all actions for all variants. The ecu problems with existential conjectures
test safety properties, e.g., whether a computed actuator value is never outside of the
allowed safety bounds. The ecu problems with universal conjectures test whether the
ecu computes an actuator value for all possible input sensor data. Our benchmarks are
prototypical for the complexity of HBS(SLR) reasoning in that they cover all abstract
relationships between conjectures and HBS(SLR) clause sets. With respect to our two
case studies we have many more examples showing respective characteristics. We would
have liked to run benchmarks from other sources too, but we could not find any suitable
HBS(SLR) problems in the SMT-LIB or CHC-COMP benchmarks.
     For comparison, we also tested several state-of-the-art theorem provers for related
logics (with the best settings we found): the satisfiability modulo theories (SMT) solver
cvc4-1.8 [3] with settings --multi-trigger-cache --full-saturate-quant; the
SMT solver z3-4.8.10 [13] with its default settings; the constrained horn clause (CHC)
solver spacer [24] with its default settings; and the first-order theorem prover vampire-
4.5.1 [35] with settings --memory_limit 8000 -p off, i.e., with memory extended
to 8GB and without proof output.
     For the experiments, we used a Debian Linux server with 32 Intel Xeon Gold 6144
(3.5 GHz) processors and 754 GB RAM. Our toolchain employs no parallel computing,
except for the java garbage collection. The other tested theorem provers employ no
parallel computing at all. Each tool got a time limit of 40 minutes for each problem.
     The table in Fig. 2 lists for each benchmark problem: the name of the problem
(Problem); the type of conjecture (Q), i.e., whether the conjecture is existential ∃
or universal ∀; the status of the conjecture (Status), i.e., true if the conjecture is a
consequence and false otherwise; the maximum number of variables in any clause
(𝑋); the number of variables in the conjecture (𝑌 ); the number of test points/constants
introduced by the Hammer (𝐵); the size of the formula in kilobyte before and after the
hammering (Size); the total time (in s) needed by our toolchain to solve the problem
(t-time); the time (in s) spent on hammering the input formula (h-time); the time (in s)


                                                   21
spent on parsing the hammered formula by Rulewerk (p-time); the time (in s) Rulewerk
actually spent on reasoning (r-time). The remaining four columns list the time in s
needed by the other tools to solve the benchmark problems. An entry "N/A" means
that the benchmark example cannot be expressed in the tools input format, e.g., it is
not possible to encode a universal conjecture (or, to be more precise, its negation) in
the CHC format. An entry "timeout" means that the tool could not solve the problem
in the given time limit of 40 minutes. Rulewerk is connected to SPASS-SPL via a file
interface. Therefore, we show parsing time separately.
    The experiments show that only our toolchain solves all the problems in reasonable
time. It is also the only solver that can decide in reasonable time whether a universal
conjecture is not a consequence. This is not surprising because to our knowledge
our toolchain is the only theorem prover that implements a decision procedure for
HBS(SLR). On the other types of problems, our toolchain solves all of the problems in
the range of seconds and with comparable times to the best tool for the problem. For
problems with existential conjectures, the CHC solver spacer is the best, but as a trade-
off it is unable to handle universal conjectures. The instantiation techniques employed
by cvc4 are good for proving some universal conjectures, but both SMT solvers seem to
be unable to disprove conjectures. Vampire performed best on the hammered problems
among all first-order theorem provers we tested, including iProver [25], E [37], and
SPASS [41]. We tested all provers in default theorem proving mode, but adjusted the
memory limit of Vampire, because it ran out of memory on ecu_u4 with the default
setting. The experiments with the first-order provers showed that our hammer also works
reasonably well for them, e.g., they can all solve all lane change problems in less than
a second, but they are simply not specialized for the HBS fragment.


6    Conclusion
We have presented several new techniques that allow us to translate BS(SLR) PP clause
sets with both universally and existentially quantified conjectures into logics for which
efficient decision procedures exist. The first set of translations returns a finite abstraction
for our clause set and conjecture, i.e., an equisatisfiable ground BS(LRA) clause set
over a finite set of test points/constants that can be solved in theory by any SMT solver
for linear arithmetic. The abstraction grows exponentially in the maximum number of
variables in any input clause. Realistic supervisor examples have clauses with 10 or
more variables and the basis of the growth exponent is also typically large, e.g., in our
examples it ranges from 15 to 1500, so this leads immediately to very large clause sets.
An exponential growth in grounding is also unavoidable, because the abstraction reduces
a NEXPTIME-hard problem to an NP-complete problem (ground BS, i.e., SAT). As an
alternative, we also present a Datalog hammer, i.e., a translation to an equisatisfiable
HBS clause set without any theory constraints. The hammer is restricted to the Horn
case, i.e., HBS(SLR) PP clauses, and the conjectures to positive universal/existential
conjectures. Its advantage is that the formula grows only exponentially in the number of
variables in the universal conjecture. This is typically much smaller than the maximum
number of variables in any input clause, e.g., in our examples it never exceeds three.
     We have implemented the Datalog hammer into our BS(LRA) system SPASS-SPL
and combined it with the Datalog reasoner Rulewerk. The resulting toolchain is an
effective way of deciding verification conditions for supervisors if the supervisors can
be modeled as HBS(SLR) clause sets and the conditions as positive BS(SLR) con-
jectures. To confirm this, we have presented two use cases for real-world supervisors:


                                              22
(i) the verification of supervisor code for the electrical control unit of a super-charged
combustion engine and (ii) the continuous certification of lane assistants. Our experi-
ments show that for these use cases our toolchain is overall superior to existing solvers.
Over existential conjectures, it is comparable with existing solvers (e.g., CHC solvers).
Moreover, our toolchain is the only solver we are aware of that can proof and disproof
universal conjectures for our use cases.
     For future work, we want to further develop our toolchain in several directions.
First, we want SPASS-SPL to produce explications that prove that its translations are
correct. Second, we plan to exploit specialized Datalog expressions and techniques (e.g.,
aggregation and stratified negation) to increase the efficiency of our toolchain and to
lift some restrictions from our input formulas. Third, we want to optimize the selection
of test points. For instance, we could partition all predicate argument positions into
independent sets, i.e., two argument positions are dependent if they are assigned the
same variable in the same rule. For each of these partitions, we should be able to create
an independent and much smaller set of test points because we only have to consider
theory constraints connected to the argument positions in the respective partition. In
many cases, this would lead to much smaller sets of test points and therefore also to
much smaller hammered and finitely abstracted formulas.
Acknowledgments: This work was funded by DFG grant 389792660 as part of TRR 248
(CPEC), by BMBF in project ScaDS.AI, and by the Center for Advancing Electron-
ics Dresden (cfaed). We thank Pascal Fontaine, Alberto Griggio, Andrew Reynolds,
Stephan Schulz and our anonymous reviewers for discussing various aspects of this
paper.


References
 [1] Abiteboul, S., Hull, R., and Vianu, V. Foundations of Databases. Addison
     Wesley, 1994.
 [2] Bachmair, L., Ganzinger, H., and Waldmann, U. Refutational theorem proving
     for hierarchic first-order theories. Applicable Algebra in Engineering, Communi-
     cation and Computing, AAECC 5, 3/4 (1994), 193–212.
 [3] Barrett, C., Conway, C., Deters, M., Hadarean, L., Jovanović, D., King, T.,
     Reynolds, A., and Tinelli, C. CVC4. In CAV, vol. 6806 of LNCS. 2011.
 [4] Barrett, C., Fontaine, P., and Tinelli, C. The SMT-LIB Standard: Version
     2.6. Tech. rep., Department of Computer Science, The University of Iowa, 2017.
     Available at www.SMT-LIB.org.
 [5] Baumgartner, P., and Waldmann, U. Hierarchic superposition revisited. In
     Description Logic, Theory Combination, and All That - Essays Dedicated to Franz
     Baader on the Occasion of His 60th Birthday (2019), C. Lutz, U. Sattler, C. Tinelli,
     A. Turhan, and F. Wolter, Eds., vol. 11560 of Lecture Notes in Computer Science,
     Springer, pp. 15–56.
 [6] Bjørner, N., Gurfinkel, A., McMillan, K. L., and Rybalchenko, A. Horn
     clause solvers for program verification. In Fields of Logic and Computation II -
     Essays Dedicated to Yuri Gurevich on the Occasion of His 75th Birthday (2015),
     L. D. Beklemishev, A. Blass, N. Dershowitz, B. Finkbeiner, and W. Schulte, Eds.,
     vol. 9300 of Lecture Notes in Computer Science, Springer, pp. 24–51.


                                           23
 [7] Böhme, S., and Nipkow, T. Sledgehammer: Judgement day. In Automated Rea-
     soning, 5th International Joint Conference, ĲCAR 2010, Edinburgh, UK, July
     16-19, 2010. Proceedings (2010), J. Giesl and R. Hähnle, Eds., vol. 6173 of
     Lecture Notes in Computer Science, Springer, pp. 107–121.
 [8] Bromberger, M., Dragoste, I., Faqeh, R., Fetzer, C., Krötzsch, M., and
     Weidenbach, C. A datalog hammer for supervisor verification conditions modulo
     simple linear arithmetic. In Frontiers of Combining Systems - 13th International
     Symposium, FroCoS 2021, Birmingham, United Kongdom, September 8-10, 2021.
     Proceedings (2021), G. Reger and B. Konev, Eds., Lecture Notes in Computer
     Science, Springer. To appear.
 [9] Bromberger, M., Fiori, A., and Weidenbach, C. Deciding the bernays-
     schoenfinkel fragment over bounded difference constraints by simple clause learn-
     ing over theories. In Verification, Model Checking, and Abstract Interpretation
     - 22nd International Conference, VMCAI 2021, Copenhagen, Denmark, January
     17-19, 2021, Proceedings (2021), F. Henglein, S. Shoham, and Y. Vizel, Eds.,
     vol. 12597 of Lecture Notes in Computer Science, Springer, pp. 511–533.
[10] Bromberger, M., Fleury, M., Schwarz, S., and Weidenbach, C. SPASS-SATT
     - A CDCL(LA) solver. In Automated Deduction - CADE 27 - 27th International
     Conference on Automated Deduction, Natal, Brazil, August 27-30, 2019, Proceed-
     ings (2019), P. Fontaine, Ed., vol. 11716 of Lecture Notes in Computer Science,
     Springer, pp. 111–122.
[11] Carral, D., Dragoste, I., González, L., Jacobs, C., Krötzsch, M., and Ur-
     bani, J. VLog: A rule engine for knowledge graphs. In Proc. 18th Int. Semantic
     Web Conf. (ISWC’19, Part II) (2019), C. Ghidini et al., Ed., vol. 11779 of LNCS,
     Springer, pp. 19–35.
[12] Cimatti, A., Griggio, A., and Redondi, G. Universal invariant checking of
     parametric systems with quantifier-free SMT reasoning. In Proc. CADE-28 (2021).
     To appear.

[13] de Moura, L., and Bjørner, N. Z3: An efficient SMT solver. In Tools and
     Algorithms for the Construction and Analysis of Systems, vol. 4963 of LNCS.
     2008.
[14] de Moura, L. M., and Bjørner, N. Satisfiability modulo theories: introduction
     and applications. Communications of the ACM 54, 9 (2011), 69–77.

[15] Downey, P. J. Undecidability of presburger arithmetic with a single monadic
     predicate letter. Tech. rep., Center for Research in Computer Technology, Harvard
     University, 1972.
[16] Eiter, T., Gottlob, G., and Mannila, H. Disjunctive datalog. ACM Trans.
     Database Syst. 22, 3 (1997), 364–418.
[17] Faqeh, R., Fetzer, C., Hermanns, H., Hoffmann, J., Klauck, M., Köhl, M. A.,
     Steinmetz, M., and Weidenbach, C. Towards dynamic dependable systems
     through evidence-based continuous certification. In Leveraging Applications of
     Formal Methods, Verification and Validation: Engineering Principles - 9th Inter-
     national Symposium on Leveraging Applications of Formal Methods, ISoLA 2020,


                                         24
     Rhodes, Greece, October 20-30, 2020, Proceedings, Part II (2020), T. Margaria
     and B. Steffen, Eds., vol. 12477 of Lecture Notes in Computer Science, Springer,
     pp. 416–439.
[18] Fiori, A., and Weidenbach, C.             SCL with theory constraints.     CoRR
     abs/2003.04627 (2020).
[19] Ge, Y., and de Moura, L. M. Complete instantiation for quantified formulas in
     satisfiabiliby modulo theories. In Computer Aided Verification, 21st International
     Conference, CAV 2009, Grenoble, France, June 26 - July 2, 2009. Proceedings
     (2009), vol. 5643 of Lecture Notes in Computer Science, Springer, pp. 306–320.
[20] Grebenshchikov, S., Lopes, N. P., Popeea, C., and Rybalchenko, A. Syn-
     thesizing software verifiers from proof rules. In ACM SIGPLAN Conference on
     Programming Language Design and Implementation, PLDI ’12, Beĳing, China -
     June 11 - 16, 2012 (2012), J. Vitek, H. Lin, and F. Tip, Eds., ACM, pp. 405–416.
[21] Hillenbrand, T., and Weidenbach, C. Superposition for bounded domains. In
     McCune Festschrift (2013), M. P. Bonacina and M. Stickel, Eds., vol. 7788 of
     LNCS, Springer, pp. 68–100.
[22] Horbach, M., Voigt, M., and Weidenbach, C. On the combination of the
     bernays-schönfinkel-ramsey fragment with simple linear integer arithmetic. In
     Automated Deduction - CADE 26 - 26th International Conference on Auto-
     mated Deduction, Gothenburg, Sweden, August 6-11, 2017, Proceedings (2017),
     L. de Moura, Ed., vol. 10395 of Lecture Notes in Computer Science, Springer,
     pp. 77–94.
[23] Horbach, M., Voigt, M., and Weidenbach, C. The universal fragment of
     presburger arithmetic with unary uninterpreted predicates is undecidable. CoRR
     abs/1703.01212 (2017).
[24] Komuravelli, A., Gurfinkel, A., and Chaki, S. SMT-based model checking
     for recursive programs. In CAV (2014), vol. 8559 of Lecture Notes in Computer
     Science, Springer, pp. 17–34.
[25] Korovin, K. iprover - an instantiation-based theorem prover for first-order logic
     (system description). In Automated Reasoning, 4th International Joint Confer-
     ence, ĲCAR 2008, Sydney, Australia, August 12-15, 2008, Proceedings (2008),
     A. Armando, P. Baumgartner, and G. Dowek, Eds., vol. 5195 of Lecture Notes in
     Computer Science, Springer, pp. 292–298.
[26] Lewis, H. R. Complexity results for classes of quantificational formulas. Journal
     of Compututer and System Sciences 21, 3 (1980), 317–353.
[27] Loos, R., and Weispfenning, V. Applying linear quantifier elimination. The
     Computer Journal 36, 5 (1993), 450–462.
[28] McCharen, J., Overbeek, R., and Wos, L. Complexity and related enhancements
     for automated theorem-proving programs. Computers and Mathematics with
     Applications 2 (1976), 1–16.
[29] Nieuwenhuis, R., Oliveras, A., and Tinelli, C. Solving sat and sat modulo
     theories: From an abstract davis–putnam–logemann–loveland procedure to dpll(t).
     Journal of the ACM 53 (November 2006), 937–977.

                                          25
[30] Nipkow, T., Paulson, L. C., and Wenzel, M. Isabelle/HOL — A Proof Assistant
     for Higher-Order Logic, vol. 2283 of LNCS. Springer, 2002.

[31] Nonnengart, A., and Weidenbach, C. Computing small clause normal forms. In
     Handbook of Automated Reasoning. Elsevier and MIT Press, 2001, pp. 335–367.
[32] Plaisted, D. A. Complete problems in the first-order predicate calculus. Journal
     of Computer and System Sciences 29 (1984), 8–35.
[33] Ranise, S. On the verification of security-aware e-services. Journal of Symbolic
     Compututation 47, 9 (2012), 1066–1088.
[34] Reynolds, A., Barbosa, H., and Fontaine, P. Revisiting enumerative instantia-
     tion. In Tools and Algorithms for the Construction and Analysis of Systems - 24th
     International Conference, TACAS 2018, Held as Part of the European Joint Con-
     ferences on Theory and Practice of Software, ETAPS 2018, Thessaloniki, Greece,
     April 14-20, 2018, Proceedings, Part II (2018), D. Beyer and M. Huisman, Eds.,
     vol. 10806 of Lecture Notes in Computer Science, Springer, pp. 112–131.
[35] Riazanov, A., and Voronkov, A. The design and implementation of vampire.
     AI Communications 15, 2-3 (2002), 91–110.

[36] Rümmer, P. Competition report: CHC-COMP-20. In Proceedings 8th Inter-
     national Workshop on Verification and Program Transformation and 7th Work-
     shop on Horn Clauses for Verification and Synthesis, VPT/HCVS@ETAPS 2020,
     Dublin, Ireland, 25-26th April 2020 (2020), L. Fribourg and M. Heizmann, Eds.,
     vol. 320 of EPTCS, pp. 197–219.

[37] Schulz, S., Cruanes, S., and Vukmirović, P. Faster, higher, stronger: E 2.3.
     In Proc. of the 27th CADE, Natal, Brasil (2019), P. Fontaine, Ed., no. 11716 in
     LNAI, Springer, pp. 495–507.
[38] Sutcliffe, G. The TPTP problem library and associated infrastructure - from
     CNF to th0, TPTP v6.4.0. J. Autom. Reason. 59, 4 (2017), 483–502.

[39] Urbani, J., Jacobs, C., and Krötzsch, M. Column-oriented Datalog materi-
     alization for large knowledge graphs. In Proc. 30th AAAI Conf. on Artificial
     Intelligence (AAAI’16) (2016), D. Schuurmans and M. P. Wellman, Eds., AAAI
     Press, pp. 258–264.
[40] Urbani, J., Krötzsch, M., Jacobs, C. J. H., Dragoste, I., and Carral, D. Effi-
     cient model construction for Horn logic with VLog: System description. In Proc.
     9th Int. Joint Conf. on Automated Reasoning (ĲCAR’18) (2018), D. Galmiche,
     S. Schulz, and R. Sebastiani, Eds., vol. 10900 of LNCS, Springer, pp. 680–688.
[41] Weidenbach, C., Dimova, D., Fietzke, A., Suda, M., and Wischnewski, P.
     Spass version 3.5. In 22nd International Conference on Automated Deduction
     (CADE-22) (Montreal, Canada, August 2009), R. A. Schmidt, Ed., vol. 5663 of
     Lecture Notes in Artificial Intelligence, Springer, pp. 140–145.




                                         26
