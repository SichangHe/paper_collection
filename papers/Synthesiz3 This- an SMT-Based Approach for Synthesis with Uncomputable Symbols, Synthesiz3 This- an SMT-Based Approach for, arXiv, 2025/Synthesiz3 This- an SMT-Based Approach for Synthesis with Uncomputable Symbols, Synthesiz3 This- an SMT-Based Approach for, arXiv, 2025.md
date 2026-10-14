                                          Formal Methods in Computer-Aided Design 2025



       Synthesiz3 This: an SMT-Based Approach for
          Synthesis with Uncomputable Symbols
                                          Petra Hozzová∗        and Nikolaj Bjørner†
                                      ∗ Czech Technical University, Prague, Czech Republic
                                                    † Microsoft, Redmond, USA



   Abstract—Program synthesis is the task of automatically con-      the uncomputable symbols, we integrate them directly into the
structing a program conforming to a given specification. In this     specification, expressed as a logical formula, by using second-
paper we focus on synthesis of single-invocation recursion-free      order quantification. The challenges we then solve are how to
functions conforming to a specification given as a logical formula
in the presence of uncomputable symbols (i.e., symbols used in       project away these symbols from the formulas, and how to find
the specification but not allowed in the resulting function). We     witnesses capturing the solutions. To solve these challenges,
approach the problem via SMT-solving methods: we present a           we take an SMT-based route: we present an algorithm based
quantifier elimination algorithm using model-based projections       on quantifier elimination games [7], [13], using and extending
for both total and partial function synthesis, working with          model-based projections [27], [6].
theories of uninterpreted functions and linear arithmetic and
their combination. For this purpose we also extend model-based            Contributions: In this work we synthesize recursion-free
projection to produce witnesses for these theories. Further, we      functions for first-order specifications using uncomputables
present procedures tailored for the case of uniquely determined      and theories. Our main contributions are:
solutions. We implemented a prototype of the algorithms using          1) An algorithm for function synthesis in the presence of
the SMT-solver Z3, demonstrating their practical efficiency
compared to the state of the art.                                         uncomputable symbols (Section III). In contrast to prior
                                                                          work [21], we use quantifiers to handle the scope of un-
                        I. I NTRODUCTION                                  computables. We present tailored model-based projection
                                                                          procedures (Section IV) used for quantifier elimination.
   Program synthesis is the task of finding a function satisfying      2) Our approach works directly for partial function synthesis
the given specification. In this paper we focus on synthesis              (see Section III-C). That is, for specifications that are not
of recursion-free functions and require the solution to be                realizable on all inputs, our approach identifies necessary
guaranteed to be correct. To this end we lean on automated                and sufficient pre-conditions when solutions exist.
reasoning methods and do not consider machine learning.                3) We introduce directed inferences exploiting the case when
As synthesis subsumes verification, it is an inherently hard              specifications have unique solutions (Section V).
problem. Yet, recent developments in this area showed that             4) We implemented a prototype of our method using the
fragments of the problem are tractable [15], [41], [39], [21].            SMT-solver Z3 and compared it to the state of the art
   There are many flavors of synthesis specifications. We con-            (Section VI).
sider specifications expressed as logical formulas capturing re-
lational constraints on symbolically represented inputs/outputs,                           II. P RELIMINARIES
recently addressed by an SMT-based approach [39] and de-                 We assume multi-sorted first-order and second-order logics
ductive synthesis in saturation [21]. Such specifications can        and use standard definitions of their syntax and semantics.
use additional syntactic constraints: in [39] (and in the SyGuS      When discussing validity, we consider all formulas implicitly
paradigm in general [2]), the resulting function must syntacti-      universally quantified. We work with theories as defined in
cally conform to the provided grammar, while [21] introduces         SMT-LIB [5], in particular with the theories of equality and
so-called uncomputable symbols which are not allowed to              uninterpreted functions (EUF), and of linear integer and real
occur in the solution. However, while [21] uses uncomputable         arithmetic (LIA and LRA).
symbols, it does not formally characterize them. That moti-              By E[t] we signify that the term or formula E contains
vated this work: we explore the semantics of specifications          the term t, and by E[t/y] we denote the term or formula we
with uncomputable symbols, and we present an algorithm               obtain from E by replacing every occurrence of the variable
solving such specifications modulo (combinations of) theories.       y by the term t. By ≃ we denote the equality predicate, by
   Uncomputable symbols are a powerful tool allowing to              := assignment, by t the tuple of terms (or variables/symbols)
make the specification more expressive, e.g. by (i) requir-          t1 , . . . , tn , and by TΣ the set of terms over the set of symbols
ing the solution to be maximal, (ii) assuming the necessary          Σ. We recall known notions we use in the paper: negation
condition for the existence of a total solution, or (iii) forcing    normal form (NNF) of a formula F , denoted NNF (F ),
the solution to discover properties of functions or predicates       is any formula equivalent to F , consisting only of literals,
used in the specification, but not allowed in the output.            conjunctions, and disjunctions; disjunction normal form (DNF)
While [21] introduces specialized inference rules to handle          is an NNF which is a disjunction of conjunctions of literals. We



     https://doi.org/                                                                         This article is licensed under a Creative
                                                                                              Commons Attribution 4.0 International License
use the abbreviations sat/unsat for satisfiable/unsatisfiable. We       In the rest of the paper, we use specifications like (2),
abuse the notation and by ⊤, ⊥ we denote the logical constants       formalized as follows:
for true and false, as well as their values, and in our algorithms   Definition 1 (Total Function Synthesis). Let Σ be a signature,
we also denote the undefined value by ⊥. We reduce predicates        let u ⊆ Σ be the set of uncomputable symbols, let y ∈ Σ \ u,
into functions by replacing each atom p(t) by fp (t) ≃ ⊤,            and let c = Σ \ ({y} ∪ u). A synthesis problem is a tuple
where fp is a fresh function symbol with the domain {⊥, ⊤}.
We write ℓ̄ for the complement       of the literal ℓ. When C is                                ⟨Φ[y], u, y⟩,
                            ⋀︁
a conjunction of literals ℓ∈L ℓ, we interchangeably refer to         where Φ[y] = φ[y, c, u] is a quantifier-free formula called
it as a set of its literals L. Given a set of literals L and a       a synthesis specification, containing the variable y, which
formula F , where L ∧ F is unsat, we write Core(L, F ) for           represents the function to be synthesized. A solution for the
C ⊆ L such that C ∧ F is unsat.                                      problem is a term R ∈ Tc , such that Φ[R/y] holds, called
   We use “program” and “function” in the context of objects
                                                                     a realizer for y. As R defines a total function, we call this
we synthesize as synonyms. By ϵ we denote the empty list
                                                                     problem total function synthesis.
and we use | to denote list construction. We write C → r for
                                                                        We consider theory-defined functions computable. In the
the pair of a condition C and a term r used as one case of
                                                                     following we always use y to represent the function to be
a program, and we represent the (possibly partial) program in
                                                                     synthesized, and sometimes write Φ for Φ[y], and when t does
the synthesis process as a list C1 → r1 | . . . | Cn → rn .
                                                                     not contain y, we write Φ[t] for Φ[t/y].
We construct the whole program from the list using the case
constructor,                                                         Example 1 (2-knapsack). We encode the well-known problem:
                                                                     Given 2 items of weights w1 , w2 and a capacity c, which of the
     case C1 : r1 ; . . . case Cn−1 : rn−1 ; default : rn ,          items should we choose so that the total weight of the chosen
                                                     ⋀︁i−1
which evaluates to the value ri for 1 ≤ i < n if Ci ∧ j=1 ¬Cj        items is maximal but at most c? First, we define a formula
is true, and to the value rn otherwise. Since a list of pairs        specifying that y1 , y2 form a valid pick from the two items,
of conditions and terms uniquely defines a program, we               i.e., that the value of yi is either 0 or wi (for i = 1, 2), and
sometimes abuse the notation and use the list in place of its        that y1 + y2 is at most c:
corresponding program. Finally, we use _ to denote any value            φ[y1 , y2 ] := (y1 ≃ 0 ∨ y1 ≃ w1 ) ∧ (y2 ≃ 0 ∨ y2 ≃ w2 )
in the function – i.e., the case when any value of the correct
                                                                                        ∧ y1 + y2 ≤ c
sort satisfies the specification, and we use _ when there exists
at least one computable term of that sort.                           Then the following synthesis problem specifies, assuming that
   III. S YNTHESIS OF T OTAL AND PARTIAL F UNCTIONS                  c, w1 , w2 are non-negative, that y is a valid pick from the
                                                                     two items, such that all valid picks u have lesser or equal
A. Specifications and Realizers
                                                                     combined weight than y:
   We focus on the class of synthesis specifications given as            (︁                      )︁
closed second-order logical formulas of the form                        ⟨ c ≥ 0 ∧ w1 ≥ 0 ∧ w2 ≥ 0
                                                                                 (︁                                  )︁
                                                                            =⇒ φ[y] ∧ (φ[u] =⇒ u1 +u2 ≤ y1 +y2 ) , {u}, y⟩
                    ∃f.∀c, u. φ[f (c), c, u],                 (1)
                                                                                                                               (3)
where f is the recursion-free function we want to synthesize,
                                                                     A realizer for (y1 , y2 ) of (3) is:
c are all symbols the function can depend on, and u are the
symbols f should be independent of. Following the termi-                     case w1 + w2 ≤ c : (w1 , w2 );
nology of [21], we call c computable and u uncomputable
                                                                             case w1 ≤ c ∧ (w1 ≥ w2 ∨ w2 > c) : (w1 , 0);
symbols. The computable symbols include all symbols which
are allowed in the solution for f : f ’s inputs, as well as                  case w2 ≤ c ∧ (w2 > w1 ∨ w1 > c) : (0, w2 );
constants, functions, and predicates. We call the terms and for-             default : (0, 0)
mulas over c computable terms/formulas, the terms/formulas
containing symbols from u uncomputable terms/formulas, and           B. The Expressivity of the Uncomputable Symbols
the uncomputable symbols themselves also uncomputables.                 We define the scope of uncomputable symbols directly in
   Note that (1) specifies a single single-invocation function:      the specification, by using explicit (and possibly second-order)
f always occurs in φ with the same arguments c. Thus, spec-          quantification. This is in contrast with [21], which introduced
ification (1) can be equivalently expressed in “unskolemized”        uncomputable symbols, but forbade their use in the sought
(yet still possibly second-order) form as                            solution as an additional syntactic constraint, thus allowing
                                                                     the specifications to stay within first-order logic. These two
                     ∀c.∃y.∀u. φ[y, c, u],                    (2)
                                                                     methods of restricting the uncomputable symbols are, however,
where the task is to find a witness for the first-order variable     equivalent in what they allow to express.
y. We can also allow y to be a tuple of variables, effectively          The use of uncomputable symbols allows for more expres-
specifying multiple functions, all depending on the same             sive specifications, which in turn leads to more interesting
computable symbols/inputs.                                           synthesis tasks. As in Example 1, with uncomputables we can
require that the solution is optimal by changing the specifica-                 {u}, c = {p, a, b}, the strongest C ∈ Tc implied by ∀u.Φ is
tion φ[y, c] into φ[y, c]∧(φ[u, c] =⇒ is_better (y, u)), using                  ⊤, so while ⟨a ≃ b, a⟩ satisfies (4), it does not satisfy (5).
a fresh uncomputable symbol u and some suitable definition                          Finite quantifier-free uniform interpolants do not always
of the predicate is_better . We can also use uncomputable                       exist for combinations of theories:
symbols to ensure that a specification φ[y, c] has a solution by                Example 4. Let Φ := a ≃ y ∧ Ψ, where Ψ does not have
adding an assumption φ[u, c], allowing to turn partial function                 a uniform quantifier-free interpolant. For example, let Ψ be
specifications into total ones. For example, there is no total                  ¬(p(u)∧a < u < b) for integers u, a, b, where u = {u}. Then
solution for the specification ⟨2y ≃ x, ∅, y⟩ over integers, but                there is no finite maximal   solution to ⋀︁
                                                                                                                         the synthesis problem,
there is one for ⟨2u ≃ x =⇒ 2y ≃ x, {u}, y⟩.1
                                                                                                        ⋁︁
                                                                                only an infinite one: ⟨ k>1 (a+k ≃ b∧ 0<i<k ¬p(i+a)), a⟩.
   Further, u can include also function and predicate symbols.                      Thus, we cannot develop complete algorithms in general.
With those, synthesis can require discovering properties of                     Yet, for theories admittig uniform interpolation, or even quan-
uninterpreted functions or predicates:                                          tifier elimination, computing the strongest C satisfying (5) is
Example 2 (Workshop [37], [19]). Consider the synthesis                         possible. Our synthesis algorithm, presented next, finds partial
problem ⟨Φ, {w}, y⟩, where:                                                     solutions to (4) and uses (5) as a criterion for termination.
      (︁                                                        )︁
Φ := (Mon ∨Sun) ∧ (Mon =⇒ w(V )) ∧ (Sun =⇒ w(A))                                D. A Synthesis Algorithm
          =⇒ w(y)                                                                  We present an algorithm for partial function synthesis. It
The example models a situation at a conference: given that it                                                 ⋀︁ R := C1 → r1 | . . . | Cn →
                                                                                iteratively builds a list of pairs
is Monday or Sunday today, and given that the workshop A is                     rn , stopping when ∀u.Φ ∧ 1≤i≤n ¬Ci becomes unsatisfiable
taking place on Sunday and the workshop V on Monday, the                        (step 2) – i.e., when the conditions ⋁︁ C1 , . . . , Cn cover all pos-
task is to synthesize a function that tells us which workshop                   sible cases. Then the solution is ⟨ 1≤i≤n Ci , R⟩. To compute
is taking place. Additionally, the solution is not allowed to                   one pair Cj → rj , we first find a formula π ∀ [y]     ⋀︁ not contain-
use the workshop predicate w – if we were able to evaluate                      ing symbols from u, which implies ∀u.Φ ∧ 1≤i≤j−1 ¬Ci
w(·) ourselves, we arguably would not need to use any tools                     (step 3). This π ∀ [y] corresponds to a condition under which the
to synthesize the solution.                                                     specification holds, yet none of the other conditions found so
                                                                                far apply. Next we look for a witness r and a formula π ∃ , both
C. Partial Function Synthesis                                                   only containing symbols from c, such that π ∃ implies π ∀ [r]
   We further consider partial function synthesis: a variation on               (step 4). If we find such r and π ∃ , we set Cj := π ∃ , rj := r
the synthesis problem where the specification is not required to                and add Cj → rj to the list of pairs R (step 6). Otherwise
be satisfiable on all evaluations of computable symbols. Thus,                  we find a formula π ∃ which implies ∃y.π ∀ [y], and refine the
the sought function is not required to be total.                                specification by adding ¬π ∃ to it (step
                                                                                                                       ⋀︁ 5). Then we continue
Definition 2 (Partial Function Synthesis). Let Φ[y] be a                        with the next iteration: if ∀u.Φ ∧ 1≤i≤j ¬Ci is satisfiable,
specification, where ∀c.∃y.∀u.Φ[y] is not necessarily valid.                    we look for Cj+1 → rj+1 . Computation of π ∀ and π ∃ (steps
Then ⟨Φ[y], u, y⟩ is a partial (function) synthesis problem.                    3 and 4) is addressed in Section IV.
A solution for the problem is a pair ⟨C, R⟩, where C is a                          The algorithm can also be used for total function synthesis
quantifier-free formula and R is a realizer for y, both over c,                 by checking that the returned condition C is equivalent to ⊤.
such that:
                                                                                Algorithm 1 Partial Function Synthesis
                                 C     =⇒       Φ[R]                     (4)
                                                                                Given a partial function synthesis task ⟨Φ, u, y⟩, return a
                      (∃y.∀u.Φ)        =⇒       C                        (5)    solution ⟨C, R⟩.
   The first condition ensures that Φ[R] holds under C, and the                   1) Initialize C := ⊥ and R := ϵ.
second condition ensures that ⟨C, R⟩ is a maximal solution for                    2) If ∀u . Φ ∧ ¬C is unsat then return ⟨C, R⟩.
partial function synthesis.                                                       3) Find a satisfiable π ∀ [y] over c∪{y}, such that π ∀ [y] =⇒
   While solutions ⟨C, R⟩ are recursively enumerable for first-                      ∀u . Φ ∧ ¬C. (See Algorithm 3 in Section IV-B.)
order specifications, we note that they are in the undecidable                    4) Find ⟨π ∃ , r⟩ such that π ∃ is satisfiable and over c and
∀∃∀-fragment [24]. The process of finding C that satisfies                           either π ∃ =⇒ π ∀ [r] with r ∈ Tc , or r = ⊥ and there is
condition (5) relates to synthesizing uniform quantifier-free                        no realizer over c for π ∀ [y] and π ∃ =⇒ ∃y.π ∀ [y].
interpolants [42].                                                                   (See Algorithm 2 in Section IV-A.)
Example 3. Let Φ := q(y) ∨ a ≃ b ≃ y with u = {q}, c =                            5) If r = ⊥, update Φ := Φ ∧ ¬π ∃ and go to step 2.
{a, b}. Then the weakest quantifier-free formula that implies                     6) Otherwise, update C := C ∨ π ∃ , R := R | (π ∃ → r) and
∀u.Φ is a ≃ b ≃ y, producing the partial solution ⟨a ≃ b, a⟩.                        go to step 2.
On the other hand, for Φ := p(u) ∨ a ≃ b ≃ y, with u =
  1 This trick does not work if φ already uses some uncomputable symbols.
                                                                                   Correctness of Algorithm 1 is straightforward:
However, our synthesis algorithm (Section III-D) works for partial functions,   Proposition 3. Assume Algorithm 1 terminates with ⟨C, R⟩. If
as defined in Section III-C.                                                    it never produced r = ⊥ in step 4, then ⟨C, R⟩ is a maximal
solution for the given partial synthesis problem. Otherwise        to π ∀ . For step 4 of Algorithm 1, we use existential projection
⟨C, R⟩ is a program satisfying condition (4) but there is no       with witness extraction for the appropriate theory (for EUF,
solution to (5).                                                   see Algorithm 2), which takes π ∀ and an arbitrary model of
Proof. Each step preserves (4) C =⇒ Φ[R]. The termination          it, and returns a suitable pair ⟨π ∃ , r⟩.
condition ensures (5) ∃y.∀u.Φ =⇒ C ∨ C ⊥ , where C ⊥ is
the disjunction of projections for r = ⊥.                          A. Existential Projection
Remark 4. Algorithm 1 is complete for theories that admit             To compute realizers, we use existential model-based pro-
quantifier elimination for computing π ∀ , π ∃ in steps 3 and 4.   jection.
Example 5. Our algorithm solves the workshop problem from          Definition 5 (∃MBP and ∃MBPR [27]). Let Φ be a quantifier-
Example 2. In the first iteration, ∀w.Φ is sat. We find            free formula and assume M |= Φ. Then existential model-
π ∀ [y] = ¬Mon ∧ ¬Sun (see Example 9 for details). Then            based projection ∃MBP(M, x, Φ) is a quantifier-free formula
a corresponding ⟨π ∃ , r⟩ is ⟨¬Mon ∧ ¬Sun, _⟩, where _ is the      π ∃ over symbols not in x, such that M |= π ∃ and π ∃ =⇒
“any” realizer. We add ¬Mon ∧ ¬Sun to C. As ∀w.Φ ∧ ¬C              ∃x.Φ.
is satisfiable, we continue. We find π ∀ [y] = A ≃ y ∧ Sun, and    Further, when y is a symbol in Φ, a model-based projection
then a corresponding ⟨π ∃ , r⟩ = ⟨Sun, A⟩ (see Example 7). We      with realizer ∃MBPR(M, y, Φ) is a pair ⟨π ∃ , r⟩ such that π ∃
add ¬Sun to C. The formula ∀w.Φ ∧ ¬C is still satisfiable,         is quantifier-free and satisfiable, π ∃ =⇒ Φ[r/y], and y ̸∈
so we continue. In the next iteration, π ∀ = V ≃ y ∧ Mon and       π ∃ , r.
⟨π ∃ , r⟩ = ⟨Mon, V ⟩. Then finally ∀w.Φ ∧ ¬C is unsat, and in        Various algorithms for model-based projection have been
fact, C ≡ ⊤. We thus return                                        integrated into Z3. We will use ∃MBP to project uncomputable
  ⟨⊤, (¬Mon ∧ ¬Sun → _) | (Sun → A) | (Mon → V )⟩.                 symbols in Section IV-B. We also introduce an algorithm for
                                                                   computing ∃MBPR(M, y, L) for EUF given a set of literals
Since the first case in the realizer list uses _, we can choose    L. Prior works [6], [26] develop projection algorithms that
to return V in that case. Further, since its condition ¬Mon ∧      apply to combinations with arrays [25], integer arithmetic, and
¬Sun is the complement of the disjunction of the other two         algebraic data-types [7]. However, they do not cover extract-
conditions (Sun or Mon), we can move it to the end of the list     ing computable realizers from projections. For example, [6]
and then unite into a default case with the condition Mon,         defines projections of first-order functions that can be defined
which also returns V , obtaining the final program:                without getting into notions of computable realizers. On the
                                                                   other hand, we can rely on witness extraction algorithms for
             ⟨⊤, case Sun : A; default : V ⟩                       LIA [31] for a combination with EUF.
E. Unique Realizers                                                Definition 6 (Congruence Preserving Partition). Let T be a
   A useful special case in step 4 of Algorithm 1 is when          set of terms closed under sub-terms. A congruence preserving
a solution to the variable y is uniquely determined. For           partition of T is a set P that partitions T , such that for every
example, for a simplified 1-item version of knapsack, given        f (s), f (t) ∈ T , whenever ∀i ∈ {1, . . . , n}.∃P ∈ P.si , ti ∈
by c < 0 ∨ w1 < 0 ∨ ((y1 = 0 ∨ y1 = w1 ) ∧ y1 ≤                    P , then ∃P ′ ∈ P.f (s), f (t) ∈ P ′ .
c ∧ ((u1 ̸= 0 ∧ u1 ̸= w1 ) ∨ u1 > c ∨ u ≤ y)), and under           Definition 7 (E-graph, E). An E-graph, E, is a data structure
the case c ≥ 0, w1 ≥ 0, u1 = w1 , u1 > c, there is a unique        that provides access to a congruence preserving partition. It
solution to y given by 0. In Section V, we show how to read        maps each term t ∈ T to its partition by root(t).
out unique solutions from a combination of the E-graph (a             Every interpretation M induces a congruence preserving
data structure capturing congruences, see Definitions 6 and 7)     partition. Conversely, for a set of equalities over EUF, there
and arithmetical constraints. Our approach can be considered       is a unique congruence preserving partition P such that for
a generalization of E-graph saturation, where we consider also     each equality s ≃ t, s, t belong to the same class in P, and
the theory of linear real arithmetic.                              every other partition with that property is obtained by taking
                                                                   unions of classes in P. When a solver constructs an E-graph
               IV. Q UANTIFIER P ROJECTION                         E, then every equality that is added to E is justified by a
   Our synthesis algorithm (Algorithm 1) uses two flavors          set of literals. Justification extends to every implied equality
of quantifier projection methods, one for existential and one      and can be represented as a proof tree that uses axioms for
for universal quantifiers. Prior work [6] explores projection      EUF. Thus, when root(t) = root(t′ ), then the function J (t, t′ )
operators for EUFLIA, but side-steps some requirements we          returns the set of equality literals used to establish the equality
have for the resulting formulas and realizers. We therefore        between t, t′ in E. We use the partition to find a computable
introduce heuristics suitable for our setting. We describe         term t′ ∈ Tc equal to a given term t. To this end, we define a
methods for existential projection in Section IV-A, and Sec-       so-called representative function repc , returning a suitable t′
tion IV-B presents an approach for universal projection. We        for the given t, as well as for the class t belongs to in P.
then plug these methods into Algorithm 1. For step 3 of            Definition 8 (repc (P ) [6], [14]). Given a congruence preserv-
Algorithm 1, we use universal projection (Algorithm 3), which      ing partition P, a representative, overloaded as: repc : 2T →
takes Φ ∧ ¬C and returns a set of literals L, which we assign      Tc ∪ {⊥}, repc : T → Tc ∪ {⊥}, is a function satisfying:
 1) repc (t) = repc (P ) for each P ∈ P, t ∈ P .                                   Extending MBP from LIA to EUFLIA requires enforcing
 2) repc (P ) = ⊥ or repc (P ) = f (repc (t1 ), . . . , repc (tn )) ∈            Ackermann axioms. We derive a recipe from [6].
    Tc such that f (t) ∈ P, repc (ti ) ̸= ⊥ for each ti .                        Definition 11 (∃MBPR for LIA + EUF). Let M |= L
 3) Maximality: for every P ∈ P, repc (P ) = ⊥ implies that                      over LIA + EUF, and assume L is closed under Ackermann
    every term f (t) in P either has f ̸∈ c, or repc (ti ) = ⊥                   reductions with respect to y. That is, for every occurrence f (s)
    for some i.                                                                  and f (t), where f is uninterpreted, s, t are arithmetic terms
  Searching for a realizer of y for L[y] can be performed by                     that contain y: either (s ̸≃ t) ∈ L or (f (s) ≃ f (t)) ∈ L.
Algorithm 2.2                                                                    Then ∃MBPR(M, y, L) is defined by LIA projection where
                                                                                 only occurrences of y within arithmetic terms are considered.
Algorithm 2 ∃MBPR(M, y, L) for EUF                                               Remark 12. We established complete ∃MBP and ∃MBPR
Given L[y] over c ∪ {y}, and M such that M |= L[y], return                       methods for EUF and EUFLIA. ∃MBP for combinations
⟨π ∃ , r⟩ over c such that either π ∃ =⇒ L[r], or r = ⊥ and                      of theories that include arrays and algebraic datatypes are
π ∃ =⇒ ∃y.L[y].                                                                  implemented in Z3.
  1) Let P be a congruence preserving partition, based on M,
       satisfying L.                                                             B. Universal Projection
  2) Let C := {repc (P ) | P ∈ P, repc (P ) ̸= ⊥}                                     Universal projection for EUFLRA was addressed in dif-
                  ∪ {f (t) | f ∈ c, ti = repc (Pi ) ̸= ⊥}.                       ferent guises. Covering algorithms by [16] can be used to
  3) If there is r ∈ C such that L[y] ∧ y ≃ r is satisfiable,                    compute projections for EUFLRA. They provide a strongest Ψ
       return ⟨L[r], r⟩.                                                         such that (∃u.¬Φ) =⇒ Ψ. Equivalently, ¬Ψ =⇒ ∀u.Φ. We
  4) Otherwise, there is no computable r such that L[r]                          would like to unfold ¬Φ incrementally as a DNF so that we
       does not contradict equalities following from M. Return                   can compute implicants of ∀u.Φ incrementally and terminate
       ⟨∃MBP(M, y, L), ⊥⟩.                                                       once we find a suitable projection.
                                                                                      We here outline a method that produces a DNF of im-
Proposition 9 (Correctness and Completeness of Algo-                             plicants. It can be used for ground formulas and combina-
rithm 2). Algorithm 2 produces ∃MBPR(M, y, L) iff one                            tions of theories where ∃MBP applies. It derives from the
exists, and returns ⟨∃MBP(M, y, L), ⊥⟩ otherwise.                                MARCO algorithm [32] for core enumeration, where our
Proof. The goal is to establish if there exists a term r ∈ Tc                    twist is to apply projection to cores during enumeration and
such that L[r] ≡ L[y] ∧ y ≃ r is satisfiable. For this purpose                   to terminate early when a suitable satisfying assignment is
we enumerate a subset of Tc that is necessary and sufficient.                    found. Let Φ be a ground formula and L be all the literals
In particular, it is sufficient to check the set of terms in P                   that occur in the negation normal form of ¬Φ. The set of
that are already represented by computable terms, and terms                      cores over L with respect to Φ can be enumerated using
immediately obtained from these terms by using the signature                     core enumeration techniques. Each core C is such that C ∧ Φ
c. Suppose there is a term r ∈ Tc such that L[r] is satisfiable.                 is unsatisfiable, which means Φ =⇒ ¬C. We can filter
Then either it is congruent to a term in repc (P ), P ∈ P, or                    out cores that are unsatisfiable by themselves. It remains to
we can trim it down to a term with immediate children in                         eliminate u from each core, or in other words, find C ′ , such
repc (P ). Suppose r = f (t) is a solution, but ti for some i                    that (∀u.¬C) =⇒ ¬C ′ . This question is equivalent to finding
is not congruent within P. Then we could use ti in place of                      C ′ , such that C ′ =⇒ ∃u.C. We can use ∃MBP to establish
r because we can produce a model of L[ti ] by setting the                        C ′ based on a model for C. Thus,
interpretation of ti the same as f (t). Note that it is possible
                                                                                                                     ⋀︁
                                                                                                 ∀u.Φ ≡ ∀u.(Φ ∧ ⋀︁i ¬Ci )
that M enforces congruences not in P so it is not necessarily                                            ≡ (∀u.Φ) ∧ ⋀︁i ∀u.¬Ci
the case that M |= L[r].                                                                                 ≡ (∀u.Φ) ∧ i ¬Ci′
Remark 10. Single invocations of ∃MBPR do not necessarily
                                                                                 We have found a sufficient set of cores when (if) the formula
produce formulas that are equivalent to ∃y.L[y]. Thus, L[y] ∧
¬L[r] is not necessarily unsatisfiable. However, ∃MBPR for
                                                                                                      ⋀︂
                                                                                                     ( ¬Ci′ ) ∧ ¬∀u.Φ
EUF+LIA finitely eliminates all models of L.                                                              i
Example 6. In the following constraints, there are no solutions                  is unsat. But we do not need to compute the full set of cores
for y using Tc . (1) Let c = {a} and L = y ̸≃ a. (2) Let                         before we can extract candidates for π ∀ . We can return a
c = {f, a} and L = f (a) ≃ a ∧ y ̸≃ a.                                           propositional   model π ∀ of the current partial set of projections
Example 7. We compute ⟨π ∃ , r⟩ for L[y] = {A ≃ y, Sun},                         ⋀︁      ′               ∀
                                                                                    i ¬Ci , whenever π ∧ ¬∀u.Φ  ⋀︁ is′ unsat. In other words, it
requested in Example 5. A partition P based on L is                              suffices to  extract a DNF of    i ¬Ci on demand without having
{{A, y}, {Sun, ⊤}}. Then C = {A, Sun}. Since A is of the                         the full i ¬Ci′ =⇒ ∀u.Φ.
                                                                                           ⋀︁
suitable sort and L[A] ∧ y ≃ A is satisfiable, the result is                         This discussion motivates Algorithm 3. It enumerates propo-
⟨Sun ∧ A ≃ A, A⟩, equivalent to ⟨Sun, A⟩.                                        sitional models of literals in Φ, using additional constraints O
  2 We describe the practical optimizations for Algorithm 2, including finding   (blocking implicants of ¬Φ) and S (blocking implicants of
the “any” realizer _, in Section VI.                                             Φ which use uncomputable symbols), both initialized to ⊤.
The models are constructed by first finding a subset U of          model such that L ∧ Φ is unsat then L′ := L \ {ℓ ∈ L | ℓ ̸∈
uncomputable literals in ¬Φ consistent with O ∧ S, and then        Lu , ℓ ∈ Lu } also satisfies L′ ∧ Φ is unsat. The symmetric
finding a model for U ∧ Φ. If this model satisfies a set of        claim is: If L is a propositional model such that L ∧ ¬Φ is
literals L⊤                                  ⊤
           c not using uncomputables, and Lc =⇒ Φ, we are          unsat, then L′ := L \ {ℓ ∈ L | ℓ ̸∈ Lc , ℓ ∈ Lc } also satisfies
done (step 7). If U ∧ Φ is unsat, we block this model in future    L ∧ ¬Φ is unsat. Justification (for the last claim): If ℓ occurs
enumeration: we project u from⋁︁ the unsat core Core(U, Φ),        positive in Φ, but ℓ does not occur in Φ at all, then ℓ does
negate the projection obtaining ℓ∈C̄ ℓ (corresponding to ¬Ci′      not occur negatively in ¬Φ and therefore doesn’t contribute to
from the discussion above), add this clause to O, and add          L ∧ ¬Φ being unsat.
                                                                      Claim: All propositional models of i ¬Ci′ are covered by
                                                                                                            ⋀︁
the new literals from C̄ to all clauses in S (step 4). The last
case is when the propositional model implies Φ, but using an       step 7. Here, Ci′ is a projection of Ci and Ci is a propositional
implicant which includes uncomputable literals. To block this      model of Φ. It follows as step 4 prunes literal combinations
model in future enumeration iterations, we add a clause over       that are propositional  models of ¬Φ, while step 7 identifies the
                                                                   models for i ¬Ci′ , and step 8 forces enumeration of propo-
                                                                                ⋀︁
literals that are false in this model to S (step 8). In contrast
to MARCO, the set of literals that is used to enumerate cores      sitional models to contain literals that belong to a correction
grows (in step 4). To allow models using the new literals, the     set of non-models of Φ.
algorithm weakens S by including new literals from C̄. The            Put together, if the underlying theory allows to finitely
algorithm⋁︁is resumable after returning in step 7 by supplying     eliminate the propositional models (in step 4 by quantifier
a clause ℓ∈C̄ ℓ implied by ¬π ∀ to step 4(a).                      elimination), we eventually reach the model corresponding to
                                                                   the implicant of ∀u.Φ.
                                                                   Example 8. Let Φ := f (u) ≃ a =⇒ f (u) ≃ y where
Algorithm 3 Universal projection using cores, correction sets
                                                                   c = {f, a}, u = {u}. Let U := {f (u) ≃ a, f (u) ̸≃ y}. Then
and ∃MBP
                                                                   U ∧ Φ is unsat and the core C := f (u) ≃ a ∧ f (u) ̸≃ y with
Given Φ and u, return π ∀ such that either π ∀ =⇒ ∀u.Φ, or         respect to Φ has the projection a ̸≃ y. We add a ≃ y to O,
π ∀ = ⊥.                                                           and now O ∧ ¬Φ is unsatisfiable and we can return a ≃ y in
  1) Let O := ⊤, S := ⊤, let Lu be literals in NNF (¬Φ)            step 7. Existential projection computes the pair ⟨⊤, a⟩, which
     that contain symbols from u, and let Lc be the literals       is a solution to the synthesis problem.
     in NNF (Φ) that do not contain symbols from u.                Example 9. We compute π ∀(︁ requested by Algorithm 1 in
  2) If O ∧ S is unsat, then return ⊥.                             Example 5. We have Φ := (Mon            ∨ Sun) ∧ (Mon =⇒
  3) Find a subset U ⊆ Lu ∪ Lc that is satisfiable with model                                        )︁
                                                                   w(V )) ∧ (Sun =⇒ w(A)) =⇒ w(y) and u = {w}.
     M and implies O ∧ S.                                          First let U := {¬Mon, Sun, w(A), w(V ), ¬w(y)}. Then U ∧Φ
  4) If U ∧ Φ is unsat, let C := Core(U, Φ), let C̄ := {ℓ̄ | ℓ ∈   is unsat, with C = Core(U, Φ) = {Sun, w(A), ¬w(y)},
     ∃MBP(M, u, C)}, and                                           projected to {Sun, A ̸≃ y}. We let O := ¬Sun ∨ A ≃ y
             ⋁︁                             ⋁︁
    a) add ℓ∈C̄ ℓ to O, update S := {S ∨ ℓ∈(C̄\Lc ) ℓ | S ∈        and find a new U := {¬Mon, ¬Sun, w(A), w(V ), ¬w(y)}.
        S}, Lc := Lc ∪ C̄, and                                     Then U ∧ Φ is sat, and we find its model M′ = {Sun ↦→
    b) go to step 2.                                               ⊥, Mon ↦→ ⊥, A ↦→ v0 , V ↦→ v1 , y ↦→ v2 , w ↦→ λv.v ̸= v2 }.
  5) Otherwise, let M′ be such that M′ |= U ∧ Φ.                   We get L⊤  c = {¬Mon, ¬Sun}, which implies Φ, and we thus
  6) Let L⊤                   ′
            c := {ℓ ∈ Lc | M (ℓ) = ⊤}
                                                                   return π ∀ = Core(L⊤   c , ¬Φ) = {¬Mon, ¬Sun}.
  7) If Lc ∧¬Φ is unsat, then L⊤
          ⊤
                                c is an implicant of Φ. Return               V. S YNTHESIZING U NIQUE F UNCTIONS
     π ∀ := Core(L⊤ c , ¬Φ).
  8) Let L⊥ := {ℓ ∈ Lc ∪ Lu | M′ (ℓ) = ⊥}, add ℓ∈L⊥ ℓ to
                                                    ⋁︁                When specifications have unique realizers, we can take
     S, and go to step 2.                                          important shortcuts. For synthesis tasks based on Definition 2,
                                                                   there may be unique solutions to y based on implicants π ∀ of
                                                                   Φ. In that case, we can bypass invoking ∃MBPR. It is well-
Proposition 13 (Correctness of Algorithm 3). If Algorithm 3        recognized in QBF solving [36] that there can be a substantial
returns π ∀ ̸= ⊥, then π ∀ =⇒ ∀u.Φ.                                advantage to detecting when a formula entails that there is a
     a) Of Proposition 13:                                         unique solution for an existential variable. Heuristics based on
Proof. Since the algorithm can only return π ∀ from step 7,        unique solutions are also used to significantly aid synthesis
it means π ∀ = Core(L⊤                      ⊤
                          c , ¬Φ) where Lc does not contain        of Boolean functions [1]. We here outline how we leverage
symbols from u, and π =⇒ Φ, which then entails π ∀ =⇒
                        ∀
                                                                   unique function specifications in the case of EUF and LRA.
∀u.Φ.                                                                 The setting we will be discussing is the following: given a
Remark 14. The algorithm provides a way to incrementally           variable y, we introduce inferences that can establish when
compute cases of a partial function. It is complete for theories   a set of constraints Φ entails that y is equal to a term t
that admit quantifier elimination.                                 that does not contain any of the symbols from {y} ∪ u. For
Proof. Claim: the sets Lc obtained from the NNF of Φ and Lu        LRA in isolation, there is a canonical method for inferring
obtained form the NNF of ¬Φ are sufficient for enumerating         equalities from conjunctons of equalities and inequalities:
conflicts with Φ, and ¬Φ, respectively. If L is a propositional    Gaussian elimination. For EUF in isolation, we can consult
repc from Definition 8 if the congruence closure induced by             Let x be an arithmetic variable. It can be reduced to
a conjunction of equalities implies that y is congruent to a         a solution in terms of other variables or constants in the
term without symbols from {y} ∪ u. We summarize these                following ways:
methods in a bit more detail next. Our main observation is             1) x = lo(x), when x is fixed by existing bounds lo(x) =
that the combinination of EUF and LRA is also amenable to                 hi(x).
synthesizing unique solutions. In Section V-C we show how to           2) x = val(x), when the current value for x cannot be
extract unique solutions for y (if they exist) in a combination of        changed, i.e., when (x > val(x) ∨ x < val(x)) ∧ T ∧ B
the two theories. The main claim is that Gaussian elimination             is infeasible.
can be interleaved with congruence closure rules to establish                                                 ′
                                                                                 ∑︁                                   ∑︁
                                                                       3) x =      i ai xi , when x ∈ T and T , x =      i ai xi is
all equalities modulo LRA + EUF under a set of asserted                   obtained from T by pivoting x to a base variable.
literals. It builds on an idea of using Gaussian elimination
to solve for symbols that should be eliminated and use the           C. EUF + LRA
resulting equations to augment the congruence closure for              Suppose there is a term t ∈ Tc such that L entails y ≃ t.
equalities that may have not been surfaced by the LRA solver.        Based on the ingredients for EUF and LRA we establish a
Recall, that it is enough for theory combinations to agree           proof search for t. Represent L as E + T + B, then the search
on equalities with respect to a candidate model [12] and             succeeds by deriving the sequent E, T, B ⊢ y ⇝ t with t ∈ Tc ,
not all implied equalities. So our method extracts implied           using the following rules:
equalities on the fly from LRA and takes them into account
                                                                                      E, T, B ⊢ ti ⇝ si for each i
by augmenting the congruence closure. Beyond experimenting                                     ∑︁          ∑︁
with this method on our benchmarks, this approach also lets                           E, T, B ⊢ i ai ti ⇝ i ai si
Z3 expose equality saturation modulo EUF and LRA.
                                                                                repc (t) ̸= ⊥              t is fixed by T, B
A. EUF                                                                     E, T, B ⊢ t ⇝ repc (t)         E, T, B ⊢ t ⇝ val(t)
   The heart of CDCL(T) solvers is a congruence graph E
for the set of terms in Φ. In a satisfiable state, E maintains                                   E ⊢ t = f (t), f ∈ c
a set of currently implied congruences. If in a satisfiable                                  E, T, B ⊢ ti ⇝ t′i for each i
                                                                             Congruence
state repc (y) ∈ Tc and J (y, repc (y)) has no terms from                                         E, T, B ⊢ t ⇝ f (t′ )
u, then we have a justification that y is equal to a com-
putable term using assumptions that are computable or use                                   T ≡ t = i ai ti , T ′
                                                                                                      ∑︁
y. Assuming the state is consistent for EUF, the justification                                E, T , B ⊢ t ⇝ t′
                                                                                                  ′

J (y, repc (y)) is also EUF-consistent. We then produce the                          Gauss
                                                                                           E, T, B ⊢ i ai ti ⇝ t′
                                                                                                      ∑︁
condition J (y, repc (y))[repc (y)/y] and the realizer repc (y).
By construction, this approach extracts realizers that are forced    Proposition 15. For a real-valued variable y, the search for
by E, but it may fail to detect that a set of constraints have       t ∈ Tc with E, T, B ⊢ y ⇝ t saturates finitely and finds a
only one possible realizer:                                          solution in Tc if and only if it exists.
Example 10. Let Σ = {a, b}, L := y ̸≃ b ∧ a ̸≃ b. Then a is          Proof (Outline). The proof search is finite because every time
a unique realizer for y, but for the congruence class over L,        it solves using T it removes the row for the solved variable
repc (y) = ⊥.                                                        through a Gauss elimination step, and the number of terms
                                                                     in E to check is finite. Assuming arithmetic operations are
B. LRA                                                               computable, the rule that decomposes summations is a special
   It is also possible to solve for variables over LRA. We recall    case of the congruence rule. The proof search is also complete
the dual tableau normal form used by the arithmetic solver.          for arithmetical LRA since if it is invoked with y and finitely
A tableau T maintains a set of basic, B, and non-basic, N ,          saturates without producing a term for y, we can establish a
variables such that each basic variable is in a solved form from     model where y is distinct from every term in Tc : Set val(y) :=
the non-basic variables. The sets B and N are disjoint.              val(y)±ϵ for an infinitesimal ϵ, and inductively, for extensions
                         ⋀︂ (︂       ∑︂         )︂                   t = Σi ai ti there is at least one term ti that cannot be solved
                    T :        xb =      abi xi                      for, so set val(ti ) := val(ti ) ± ϵ/ai . The sign ±ϵ is chosen to
                       b∈B         i∈N                               make sure the new value of y is within the bounds for y in B.
Furthermore,     it maintains bounds B on all variables              Whenever ti is congruent to f (t), f ∈ c, there is inductively
⋀︁                                                                   an argument ti which is non-solvable, so the interpretation of f
   i lo(xi ) ≤ xi ≤ hi(xi ), where lower lo(xi ) ∈ {−∞} ∪ R,
hi(xi ) ∈ {∞} ∪ R. Every lower and upper bound that is               can be adjusted to take into account the new value for ti . This
not infinite is justified by a set of literals Jlo (x), Jhi (x). A   produces a non-standard model where the interpretation of all
feasible tableau comes with an evaluation function val(xi ) that     terms in Tc are over the rational numbers while y evaluates
maps every variable into a value from R, such that:                  to a non-standard real. Functions are interpreted over rationals
                    ∑︁                                               if all arguments are rationals, and can otherwise evaluate to a
         val(xb ) = i∈N abi val(xi ) for every b ∈ B                 non-standard real if some argument is not a real number.
  We note that it is straightforward to extend the inference                      Id Benchmark subset description               Count Has u Partial Unique
system to also extract justifications by tracking inequalities                     I  simple if-then-else benchmarks from        3      ✗      ✗        ✓
                                                                                      SyGuS competition [3]
used for fixed bounds and equalities used for congruences.
                                                                                  II k-knapsack (see Example 1)                   5     ✓      ✗        ✓
          VI. I MPLEMENTATION AND E VALUATION                                    III maximum function for n given integers       10     ✗      ✗        ✓
  We implemented our method as a proof of concept, and                           IV lower bound function for n integers          10     ✗      ✗        ✗
compared it with state-of-the-art methods supporting uncom-                       V function finding an integer lower than       10     ✗      ✗        ✗
                                                                                      all n given integers
putables: the synthesis mode of Vampire [21] and the leading
                                                                                 VI function finding an integer between the      4      ✓      ✗        ✗
SyGuS solver cvc5 [39], obtaining encouraging early results.                          given bounds, assuming some exists
A. Implementation                                                                VII function finding an integer between the     4      ✓      ✓        ✗
                                                                                      given bounds, if some exists
   We implemented Algorithms 1, 2, and 3, as well as the                         VIII fuction finding a solution for y in the    3      ✓      ✗        ✓
unique solution finding of Section V, as a stand-alone Python                         given equation, assuming it exists
prototype (available online at [20]) using the Z3 API, which                     IX function finding a solution for y in the     3      ✗      ✓        ✓
we also extended by new features. We use variables of array                           given equation, if it exists
sort for higher-order quantification. The theory of arrays in                     X Examples 2 (and a computable variant         4    ✗+✓      ✗        ✓
                                                                                      thereof) and 8 (and a variant thereof)
Z3 coincides with SMT-LIB 2 [5] for ground formulas, but                         XI the first specification or Example 3         1      ✓      ✓        ✓
not quantified formulas. E.g., the first-order theory of array
select function admits models where select does not include                      TABLE I: Summary of the 57 benchmarks used: set id,
bijections, but with Z3 one can instantiate quantified array                     description, how many benchmarks are in the subset, and
variables by λx.x and select is just a function application.                     whether they use uncomputables, specify a partial function,
   The API already provided functions for computing ∃MBP,                        and a unique function. Benchmark sets I-IX use LIA, X and
an incomplete method for ∃MBPR, and accessing the E-graph.                       XI use UF. In set II we have k ∈ {1, 2, 3, 4, 5}, and in sets
We extended Z3 by exposing E-graph justifications, and by                        III-V we have n ∈ {2, 5, 10, 15, 20, 25, 30, 50, 100, 150}.
a new heuristic for finding witnesses from Tc for EUF in
                                                                                              I II III IV V VI VII VIII IX X XI         sum total & partial
∃MBPR. It searches for an E-match for y that does not lead
                                                                                 Synthesiz3   3 3 9 4 3 4 4         3 3 4 1                   33 & 8
to equating shared sub-terms, and specifically avoids merging                    Vampire      3 0 5 2 0 4 –         0 – 2 –                   16 & –
sub-terms used in disequalities. We also added a method for                      cvc5         3 1 5 5 5 4 –         0 – 4 –                   27 & –
solving variables that is complete for LRA and extends to LIA                    TABLE II: Experimental results: numbers of problems solved
(incompletely, not to deal with non-convexity of LIA).                           by each solver in benchmark sets I-XI. Benchmark sets VII,
   We optimize all our algorithms as follows. In Algorithm 1,
                                                                                 IX, and XI specify partial synthesis problems not supported
step 6, if u = ∅, we use Φ[r/y] as the condition for realizer
                                                                                 by Vampire nor cvc5, which we denote by “–”.
r instead of π ∃ . Further, to compute ∃MBPR(M, y, L) of
Algorithm 2, we first check if L contains y, and if it does not,
we return the “any” realizer (as in Example 5). Otherwise, we                    and extended it with the solvable examples from this paper,
try calling ∃MBPR of the API, and if that does not return a                      as well as additional partial function synthesis problems.
realizer, we iterate over the candidates provided by repc , only                 Table I shows a summary of the benchmarks, organized into
producing a new one if the last did not work out. Finally, in                    11 subsets denoted I-XI. The set contains 57 benchmarks:
Algorithm 3, step 7, we check the unsatisfiability with respect                  18 small, conceptually distinct problems (all 3 problems of
to ¬Φ′ , where Φ′ is (i) initialized to the original specification               subset I, 2 per both VI and VII, 4 in X, and one per all the other
Φ, and (ii) only if Algorithm 3 returns the same π ∀ twice,                      subsets), and 39 scaled-up versions of the small instances.
updated to Φ′ := Φ ∧ ¬C using the current C of Algorithm 1.                         We evaluated the performance of our prototype on this
B. Evaluation                                                                    dataset and for the total synthesis problems also compared
                                                                                 it to Vampire and cvc5.5 We ran each benchmark on a single
   To the best of our knowledge, there was no standard
                                                                                 core of a 1.60GHz CPU with 16 GB RAM, with the time
benchmark set for synthesis with uncomputable symbols as of
                                                                                 limit of 1 minute. We chose 1 minute as it is enough time
writing this paper. However, a dataset based on the benchmarks
                                                                                 to solve the solvable small problems, and show the trend for
from [21] was under development in parallel with this paper,
                                                                                 the scaled-up problem instances, but not solve all the scaled-
and in the meantime it was accepted for publication [18].3
                                                                                 up instances. Table II shows the numbers of solved problems.
We took the subset of this dataset supported by our method,4
                                                                                 Successful solving of the small instances took all solvers less
   3 The dataset was co-developed by one of the authors of this paper.           than 1 second. For the larger instances, the runtimes increased
It is available at https://github.com/vprover/vampire_benchmarks/tree/master/
synthesis. The version that was available shortly before this paper was            5 We used Vampire v4.9, commit dde88d57f, in the configuration
submitted, and which we used for evaluation, is at https://github.com/vprover/   --decode dis+32_1:1_tgt=off:qa=synthesis:ep=off:alasc
vampire_benchmarks/tree/6356e52/synthesis.                                       a=off:drc=ordering:bd=off:nm=0:sos=on:ss=included:si
   4 We excluded problems using (i) theories beyond EUFLIRA, or (ii) more        =on:rawr=on:rtra=on:proof=off:msp=off_600, and cvc5 v1.1.2
complex quantification, or (iii) interpreted uncomputables, or (iv) which were   in the default configuration. For cvc5, we used SyGuS translations of the
too similar to others in the dataset – e.g. we used maximum but not minimum.     problems, encoding uncomputables as non-input variables.
up to the time limit. We note that what makes many scaled-               Projections: The literature on interpolation, includ-
up instances hard is that they encode problems with many           ing [17], develops algorithms based on proof objects. Symbol
symmetries: e.g., each case of the maximum-of-n-integers           elimination in saturation [28] works by deriving clauses that
function has the same structure, but with different variables.     are consequences of ∃u.¬Φ. Negations of these clauses can
   Overall, our approach solves the most total function synthe-    be used as projections. The approach of [28] relies on symbol
sis problems, and also partial synthesis problems which cvc5       orderings to eliminate symbols through rewriting, but does not
and Vampire do not support. Our approach scales as well as or      offer guarantees of complete symbol elimination. Deductive
better than both Vampire and cvc5 for all benchmarks with a        synthesis with uncomputables [21] blocks inferences which
unique solution, and slightly worse than cvc5 on problems with     would lead to uncomputable realizers, but also is not complete.
infinitely many possible solutions (sets IV and V). Notably,       As an example, inferences such as f (y) ̸≃ f (a) ⊢ y ̸≃ a with
within 1 minute, only our approach solves 2- and 3-knapsack,       u = {f } are not part of this methodology.6
and it also finds the maximum-of-n-integers function for              Notably, MCSAT [23] relies on a dual to ∃MBP, called
n up to 100, while cvc5 and Vampire can go only up to              ∀MBP, in a setting where it is used for satisfiability checking
n ≤ 20. Interestingly, both cvc5 and Vampire fail to solve         of quantifier-free formulas. The starting point for ∀MBP is a
all benchmarks of set VIII, including the smallest instance        partial model of a subset of symbols that cannot be completed
⟨2u ≃ x =⇒ 2y ≃ x, {u}, y⟩, “find the half of an even x”.          to a full model of all symbols. A combination of ∀MBP
                                                                   and ∃MBP for quantifier solving for polynomial arithmetic
                    VII. R ELATED W ORK                            is developed in [35], while ∃MBP with cores and strategies
      Synthesis: The field of synthesis encompasses very dif-      are used in [7], [9], [33]
ferent approaches. We only overview methods similar to ours:          We note that stand-alone projection is not necessarily the
synthesizing functions from scratch based on specifications        most efficient method for solving quantifiers. Templates have
given as logical formulas with some syntactic restrictions.        recently been used successfully for non-linear arithmetic [11],
The general restriction setting in [40] is to integrate a black-   and Z3’s Horn clause solver uses information from several pro-
box function within a solver that determines whether a term        jection invocations to compute more general projections [30].
is computable. We base our specification format on [21].                 Implied equalities: Bromberger and Weidenbach [10]
In contrast with [21], we distinguish uncomputable symbols         present a method for extracting all implied equalities from
directly in the specification formula by using quantification.     a set of linear inequalities over the reals. It is used when
The deductive synthesis methods of [21], [40] are based on         solving over LIA. Z3 [8] uses an incomplete heuristic to detect
theorem proving, and [21] is implemented in Vampire [29].          implied equalities during search. The QEL algorithm [14]
While these methods introduce specialized inference rules to       uses equalities that are consistent with an interpretation, but
filter terms using uncomputable symbols, our approach uses         not necessarily implied by a current assignment to literals, to
quantifier elimination games to remove uncomputables, and          simplify quantifier elimination problems.
thus requires no changes in the underlying search procedures.
    Another related paradigm is SyGuS [2], which supports                                  VIII. C ONCLUSIONS
specifying multiple functions with different inputs, and con-         This paper formally defines and studies the problem of
straining the space of solutions to functions generated by a       synthesis of total and partial functions in the presence of
given grammar. SyGuS solvers include cvc5 [4], [39] and            uncomputable symbols. To solve these problems, we intro-
DryadSynth [22]. Compared to the specification setting we          duced a modular algorithm for synthesis, relying on quantifier
consider, SyGuS allows a more fine-grained syntactic control       projections. We summarized requirements on the projections
over the synthesized function. We note that to solve such          and presented algorithms computing existential projection with
specifications, we could generate candidate terms using the        witnesses for EUFLIA, and universal projection internally
provided grammar instead of using ∃MBPR, or that we                relying on existential projection. Further, we described a
could use grammar-based reconstruction as in [39] on top of        method to circumvent quantifier solving for uniquely defined
∃MBPR. On the other hand, our specifications support the use       functions in EUFLRA. Finally, we implemented a prototype
of uninterpreted symbols, in particular uninterpreted functions    demonstrating that the proposed methods work in practice.
and predicates. This allows us to express e.g. the workshop           Our results prompt future work in multiple directions, such
problem (see Example 2), which is not directly supported           as extending synthesis to functions with different inputs, or
by SyGuS. However, using higher-order logic, uninterpreted         extending the specification with quantified background axioms
functions can be encoded as higher-order variables, and with       to support reasoning with user-defined theories. Moreover,
this encoding cvc5 solves the workshop problem (and some           developing projections for other theories would allow synthesis
other problems, see Section VI). Finally, neither SyGuS nor the    in those theories by plugging them into our algorithm. Last but
deductive synthesis methods support partial function synthesis.    not least, our unique solution approach could be extended to
    We provide some examples where the partial function            infer all implied equalities.
synthesis problem has no solutions. The study of unrealiz-
ability [34] dually establishes methods to show that there are       6 We note that such an inference could be supported by a suitable variation
no solutions to synthesis problems.                                of unification with abstraction [38].
Acknowledgments. We thank Kuldeep Meel for suggesting                            [16] Sumit Gulwani and Madan Musuvathi. Cover algorithms and their
to examine partial function synthesis with unique realiz-                             combination. In Sophia Drossopoulou, editor, Programming Languages
                                                                                      and Systems, 17th European Symposium on Programming, ESOP 2008,
ers. Diego Olivier Fernandez Pons inspired us to explore                              Held as Part of the Joint European Conferences on Theory and Practice
synthesis with Z3. We also thank Mikoláš Janota for dis-                              of Software, ETAPS 2008, Budapest, Hungary, March 29-April 6, 2008.
cussions of examples. Petra Hozzová was funded by the                                 Proceedings, volume 4960 of Lecture Notes in Computer Science, pages
                                                                                      193–207. Springer, 2008.
European Union under the project ROBOPROX (reg. no.                              [17] Ashutosh Gupta, Corneliu Popeea, and Andrey Rybalchenko. Solving
CZ.02.01.01/00/22_008/0004590).                                                       recursion-free horn clauses over LI+UIF. In Hongseok Yang, editor,
                                                                                      Programming Languages and Systems - 9th Asian Symposium, APLAS
                              R EFERENCES                                             2011, Kenting, Taiwan, December 5-7, 2011. Proceedings, volume 7078
 [1] S. Akshay, Supratik Chakraborty, and Shetal Shah. Tractable repre-               of Lecture Notes in Computer Science, pages 188–203. Springer, 2011.
     sentations for boolean functional synthesis. Ann. Math. Artif. Intell.,     [18] Márton      Hajdu,    Petra     Hozzová,    Laura    Kovács,    Andrei
     92(5):1051–1096, 2024.                                                           Voronkov, Eva Maria Wagner, and Richard Steven Žil-
 [2] Rajeev Alur, Rastislav Bodík, Eric Dallal, Dana Fisman, Pranav Garg,             inčík.       Synthesis Benchmarks for Automated Reasoning.
     Garvit Juniwal, Hadas Kress-Gazit, P. Madhusudan, Milo M. K. Martin,             https://arxiv.org/abs/2507.19827, 2025.                     To appear
     Mukund Raghothaman, Shambwaditya Saha, Sanjit A. Seshia, Rishabh                 in proceedings of CICM 2025.
     Singh, Armando Solar-Lezama, Emina Torlak, and Abhishek Udupa.              [19] Petra Hozzová. Integrating Answer Literals with AVATAR for Program
     Syntax-Guided Synthesis. In Dependable Software Systems Engineering,             Synthesis. In Laura Kovács and Michael Rawson, editors, Proc. of the
     pages 1–25. 2015.                                                                7th and 8th Vampire Workshop, volume 99 of EPiC Series in Computing,
 [3] Rajeev Alur, Dana Fisman, Saswat Padhi, Andrew Reynolds,                         pages 13–20. EasyChair, 2024.
     Rishabh Singh, and Abhishek Udupa.                SyGuS-Comp 2019.          [20] Petra Hozzová and Nikolaj Bjørner. Online material for Synthesiz3
     https://sygus.org/comp/2019/, 2019.                                              This! https://doi.org/10.5281/zenodo.16436706 and https://github.com/
 [4] Haniel Barbosa, Clark W. Barrett, Martin Brain, Gereon Kremer, Hanna             Z3Prover/doc/tree/master/synthesiz3/src, 2025.
     Lachnitt, Makai Mann, Abdalrhman Mohamed, Mudathir Mohamed,                 [21] Petra Hozzová, Laura Kovács, Chase Norman, and Andrei Voronkov.
     Aina Niemetz, Andres Nötzli, Alex Ozdemir, Mathias Preiner, Andrew               Program Synthesis in Saturation. In Brigitte Pientka and Cesare Tinelli,
     Reynolds, Ying Sheng, Cesare Tinelli, and Yoni Zohar. cvc5: A Versatile          editors, Proc. of CADE, volume 14132 of LNCS, pages 307–324, Cham,
     and Industrial-Strength SMT Solver. In Proc. of TACAS, pages 415–442,            2023. Springer.
     2022.                                                                       [22] Kangjing Huang, Xiaokang Qiu, Peiyuan Shen, and Yanjun Wang.
 [5] Clark Barrett, Pascal Fontaine, and Cesare Tinelli. The Satisfiability           Reconciling Enumerative and Deductive Program Synthesis. In Proc.
     Modulo Theories Library (SMT-LIB). www.SMT-LIB.org, 2016.                        of PLDI, PLDI 2020, page 1159–1174, New York, NY, USA, 2020.
 [6] Nikolaj Bjørner, Arie Gurfinkel, Sharon Shoham, and Yakir Vizel.                 Association for Computing Machinery.
     Model based interpolation for uninterpreted functions and integer linear    [23] Dejan Jovanovic and Leonardo Mendonça de Moura. Solving non-
     arithmetic. EasyChair Preprint no. 10000, EasyChair, 2023.                       linear arithmetic. In Bernhard Gramlich, Dale Miller, and Uli Sattler,
 [7] Nikolaj S. Bjørner and Mikoláš Janota. Playing with quantified sat-              editors, Automated Reasoning - 6th International Joint Conference,
     isfaction. In Ansgar Fehnker, Annabelle McIver, Geoff Sutcliffe, and             IJCAR 2012, Manchester, UK, June 26-29, 2012. Proceedings, volume
     Andrei Voronkov, editors, 20th International Conferences on Logic for            7364 of Lecture Notes in Computer Science, pages 339–354. Springer,
     Programming, Artificial Intelligence and Reasoning - Short Presenta-             2012.
     tions, LPAR 2015, Suva, Fiji, November 24-28, 2015, volume 35 of            [24] A. S. Kahr, Edward F. Moore, and Hao Wang. Entscheidungsproblem
     EPiC Series in Computing, pages 15–27. EasyChair, 2015.                          reduced to the ∀∃∀ case. Journal of Symbolic Logic, 27(2):225–225,
 [8] Nikolaj S. Bjørner and Lev Nachmanson. Arithmetic solving in Z3. In              1962.
     Arie Gurfinkel and Vijay Ganesh, editors, Computer Aided Verification -     [25] Anvesh Komuravelli, Nikolaj Bjørner, Arie Gurfinkel, and Kenneth
     36th International Conference, CAV 2024, Montreal, QC, Canada, July              Mcmillan. Compositional verification of procedural programs using horn
     24-27, 2024, Proceedings, Part I, volume 14681 of Lecture Notes in               clauses over integers and arrays. In FMCAD, pages 89–96, 09 2015.
     Computer Science, pages 26–41. Springer, 2024.                              [26] Anvesh Komuravelli, Nikolaj Bjørner, Arie Gurfinkel, and Kenneth L.
 [9] Maria Paola Bonacina, Stéphane Graham-Lengrand, and Christophe                   McMillan. Compositional verification of procedural programs using
     Vauthier. QSMA: A new algorithm for quantified satisfiability modulo             horn clauses over integers and arrays. In Proceedings of the 15th
     theory and assignment. In Brigitte Pientka and Cesare Tinelli, editors,          Conference on Formal Methods in Computer-Aided Design, FMCAD
     Automated Deduction - CADE 29 - 29th International Conference on                 ’15, page 89–96, Austin, Texas, 2015. FMCAD Inc.
     Automated Deduction, Rome, Italy, July 1-4, 2023, Proceedings, volume       [27] Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. Smt-based model
     14132 of Lecture Notes in Computer Science, pages 78–95. Springer,               checking for recursive programs. In Armin Biere and Roderick Bloem,
     2023.                                                                            editors, Computer Aided Verification - 26th International Conference,
[10] Martin Bromberger and Christoph Weidenbach. Fast cube tests for LIA              CAV 2014, Held as Part of the Vienna Summer of Logic, VSL 2014,
     constraint solving. In IJCAR, 2016.                                              Vienna, Austria, July 18-22, 2014. Proceedings, volume 8559 of Lecture
[11] Krishnendu Chatterjee, Ehsan Kafshdar Goharshady, Mehrdad Karrabi,               Notes in Computer Science, pages 17–34. Springer, 2014.
     Harshit J Motwani, Maximilian Seeliger, and Ðord̄e Žikelić. Quantified     [28] Laura Kovács and Andrei Voronkov. Interpolation and symbol elimi-
     Linear and Polynomial Arithmetic Satisfiability via Template-based               nation. In Renate A. Schmidt, editor, Automated Deduction - CADE-
     Skolemization. In AAAI, 2025.                                                    22, 22nd International Conference on Automated Deduction, Montreal,
[12] Leonardo de Moura and Nikolaj Bjørner. Model-based theory combina-               Canada, August 2-7, 2009. Proceedings, volume 5663 of Lecture Notes
     tion. Electron. Notes Theor. Comput. Sci., 198(2):37–49, May 2008.               in Computer Science, pages 199–213. Springer, 2009.
[13] Azadeh Farzan and Zachary Kincaid. Linear arithmetic satisfiability via     [29] Laura Kovács and Andrei Voronkov. First-Order Theorem Proving and
     strategy improvement. In Subbarao Kambhampati, editor, Proceedings               Vampire. In N. Sharygina and H. Veith, editors, Proc. of CAV, volume
     of the Twenty-Fifth International Joint Conference on Artificial Intelli-        8044 of LNCS, pages 1–35. Springer, 2013.
     gence, IJCAI 2016, New York, NY, USA, 9-15 July 2016, pages 735–743.        [30] Hari Govind Vediramana Krishnan, YuTing Chen, Sharon Shoham, and
     IJCAI/AAAI Press, 2016.                                                          Arie Gurfinkel. Global guidance for local generalization in model
[14] Isabel Garcia-Contreras, Hari Govind V. K., Sharon Shoham, and Arie              checking. Formal Methods Syst. Des., 63(1):81–109, 2024.
     Gurfinkel. Fast approximations of quantifier elimination. In Constantin     [31] Viktor Kuncak, Mikaël Mayer, Ruzica Piskac, and Philippe Suter. Com-
     Enea and Akash Lal, editors, Computer Aided Verification - 35th                  plete functional synthesis. In Benjamin G. Zorn and Alex Aiken, editors,
     International Conference, CAV 2023, Paris, France, July 17-22, 2023,             Proceedings of the 2010 ACM SIGPLAN Conference on Programming
     Proceedings, Part II, volume 13965 of Lecture Notes in Computer                  Language Design and Implementation, PLDI 2010, Toronto, Ontario,
     Science, pages 64–86. Springer, 2023.                                            Canada, June 5-10, 2010, pages 316–329. ACM, 2010.
[15] Sumit Gulwani, Susmit Jha, Ashish Tiwari, and Ramarathnam Venkate-          [32] Mark H. Liffiton, Alessandro Previti, Ammar Malik, and João Marques-
     san. Synthesis of Loop-Free Programs. In Proc. of PLDI, page 62–73,              Silva. Fast, flexible MUS enumeration. Constraints An Int. J.,
     2011.                                                                            21(2):223–250, 2016.
[33] Charlie Murphy and Zachary Kincaid. Quantified linear arithmetic             [37] Giles Reger. Revisiting Question Answering in Vampire. EPiC Series
     satisfiability via fine-grained strategy improvement. In Arie Gurfinkel           in Computing, 53:64–74, 2018.
     and Vijay Ganesh, editors, Computer Aided Verification - 36th Inter-         [38] Giles Reger, Martin Suda, and Andrei Voronkov. Unification with
     national Conference, CAV 2024, Montreal, QC, Canada, July 24-27,                  Abstraction and Theory Instantiation in Saturation-Based Reasoning. In
     2024, Proceedings, Part I, volume 14681 of Lecture Notes in Computer              Proc. of TACAS, pages 3–22, 2018.
     Science, pages 89–109. Springer, 2024.                                       [39] Andrew Reynolds, Viktor Kuncak, Cesare Tinelli, Clark W. Barrett, and
[34] Shaan Nagy, Jinwoo Kim, Thomas W. Reps, and Loris D’Antoni.                       Morgan Deters. Refutation-based synthesis in SMT. Formal Methods
     Automating unrealizability logic: Hoare-style proof synthesis for infinite        Syst. Des., 55(2):73–102, 2019.
     sets of programs. Proc. ACM Program. Lang., 8(OOPSLA2):113–139,              [40] Tanel Tammet. Completeness of resolution for definite answers. J. Log.
     2024.                                                                             Comput., 5(4):449–471, 1995.
[35] Jasper Nalbach and Gereon Kremer. Extensions of the cylindrical              [41] Ashish Tiwari, Adrià Gascón, and Bruno Dutertre. Program Synthesis
     algebraic covering method for quantifiers. CoRR, abs/2411.03070, 2024.            Using Dual Interpretation. In Proc. of CADE, pages 482–497, 2015.
[36] Markus N. Rabe, Leander Tentrup, Cameron Rasmussen, and Sanjit A.            [42] Greta Yorsh and Madanlal Musuvathi. A combination method for
     Seshia. Understanding and extending incremental determinization for               generating interpolants. In Robert Nieuwenhuis, editor, Automated
     2qbf. In Hana Chockler and Georg Weissenbacher, editors, Computer                 Deduction - CADE-20, 20th International Conference on Automated
     Aided Verification - 30th International Conference, CAV 2018, Held as             Deduction, Tallinn, Estonia, July 22-27, 2005, Proceedings, volume
     Part of the Federated Logic Conference, FloC 2018, Oxford, UK, July               3632 of Lecture Notes in Computer Science, pages 353–368. Springer,
     14-17, 2018, Proceedings, Part II, volume 10982 of Lecture Notes in               2005.
     Computer Science, pages 256–274. Springer, 2018.
