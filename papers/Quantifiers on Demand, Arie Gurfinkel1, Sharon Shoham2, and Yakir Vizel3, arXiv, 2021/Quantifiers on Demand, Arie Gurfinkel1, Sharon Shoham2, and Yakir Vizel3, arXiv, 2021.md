                                                                   Quantifiers on Demand

                                                          Arie Gurfinkel1, Sharon Shoham2, and Yakir Vizel3
                                                                           1
                                                                               University of Waterloo
                                                                               2
                                                                                Tel Aviv University
                                                                                3
                                                                                   The Technion
arXiv:2106.00664v1 [cs.LO] 1 Jun 2021




                                               Abstract. Automated program verification is a difficult problem. It is undecid-
                                               able even for transition systems over Linear Integer Arithmetic (LIA). Extending
                                               the transition system with theory of Arrays, further complicates the problem by
                                               requiring inference and reasoning with universally quantified formulas. In this
                                               paper, we present a new algorithm, Q UIC 3, that extends IC3 to infer universally
                                               quantified invariants over the combined theory of LIA and Arrays. Unlike other
                                               approaches that use either IC3 or an SMT solver as a black box, Q UIC 3 carefully
                                               manages quantified generalization (to construct quantified invariants) and quan-
                                               tifier instantiation (to detect convergence in the presence of quantifiers). While
                                               Q UIC 3 is not guaranteed to converge, it is guaranteed to make progress by ex-
                                               ploring longer and longer executions. We have implemented Q UIC 3 within the
                                               Constrained Horn Clause solver engine of Z3 and experimented with it by apply-
                                               ing Q UIC 3 to verifying a variety of public benchmarks of array manipulating C
                                               programs.


                                        1 Introduction

                                        Algorithmic logic-based verification (ALV) is one of the most prominent approaches for
                                        automated verification of software. ALV approaches use SAT and SMT solvers to rea-
                                        son about bounded program executions; and generalization techniques, such as interpo-
                                        lation, to lift the reasoning to unbounded executions. In recent years, IC3 [8] (originally
                                        proposed for hardware model checking) and its extensions to Constrained Horn Clauses
                                        (CHC) over SMT theories [21,24] has emerged as the most dominant ALV technique.
                                        The efficiency of the IC3 framework is demonstrated by success of such verification
                                        tools as S EA H ORN [19].
                                            The IC3 framework has been successfully extended to deal with arithmetic [21],
                                        arithmetic and arrays [24], and universal quantifiers [23]. However, no extension sup-
                                        ports the combination of all three. Extending IC3 to Linear Integer Arithmetic (LIA),
                                        Arrays, and Quantifiers is the subject of this paper. Namely, we present a technique
                                        to discover universally quantified solutions to CHC over the theories of LIA and Ar-
                                        rays. These solutions correspond to universally quantified inductive invariants of array
                                        manipulating programs.
                                            For convenience of presentation, we present our approach over a transition system
                                        modelled using the theories of Linear Integer Arithmetic (LIA) and Arrays, and not the
                                        more general, but less intuitive, setting of CHCs. Inductive invariants of such transition
                                        systems are typically quantified, which introduces two major challenges: (i) quantifiers
tremendously increase the search space for a candidate inductive invariant, and (ii) they
require deciding satisfiability of quantified formulas – itself an undecidable problem.
     Existing ALV techniques for inferring universally quantified arithmetic invariants
either restrict the shape of the quantifiers and reduce to quantifier free inference [7,29,20],
or guess quantified invariants from bounded executions [1].
     In this paper, we introduce Q UIC 3 – an extension of IC3 [8,21,25] to universally
quantified invariants. Rather than fixing the shape of the invariant, or discovering quan-
tifiers as a post-processing phase, Q UIC 3 computes the necessary quantifiers on demand
by taking quantifiers into account during the search for invariants. The key ideas are to
allow existential quantifiers in proof obligations (or, counterexamples to induction) so
that they are blocked by universally quantified lemmas, and to extend lemma general-
ization to add quantifiers.
     Generating quantifiers on demand gives more control over the inductiveness checks.
These checks (i.e., pushing in IC3) require deciding satisfiability of universally quan-
tified formulas over the combined theory of Arrays and LIA. This is undecidable, and
is typically addressed in SMT solvers by quantifier instantiation in which a universally
quantified formula ∀x · ϕ(x) is approximated by a finite set of ground instances of
ϕ. SMT solvers, such as Z3 [12], employ sophisticated heuristics (e.g., [15]) to find
a sufficient set of instantiations. However, the heuristics are only complete in limited
situations (recall, the problem is undecidable in general), and it is typical for the solver
to return unknown, or, even worse, diverge in an infinite set of instantiations.
     Instead of using an SMT solver as a black-box, Q UIC 3 generates and maintains a
set of instantiations on demand. This ensures that Q UIC 3 always makes progress and is
never stuck in a single inductiveness check. The generation of instances is driven by the
blocking phase of IC3 and is supplemented by traditional pattern-based triggers. Gener-
ating both universally quantified lemmas and their instantiations on demand, driven by
the property, offers additional flexibility compared to the eager quantifier instantiation
approach of [7,29,20].
     Combining the search for all of the ingredients (quantified and quantifier-free for-
mulas, and instantiations) in a single procedure improves the control over the verifi-
cation process. For example, even though there is no guarantee of convergence (the
problem is, after all, undecidable), we guarantee that Q UIC 3 makes progress, exploring
more of the program, and discovering a counter-example (even the shortest one) if it
exists.
     While our intended target is program verification, we have implemented Q UIC 3 in a
more general setting of Constrained Horn Clauses (CHC). We build on the Generalized
PDR engines [21,25] in Z3. The input is a set of CHC in SMT-LIB format, and the
output is a universally quantified inductive invariant, or a counter-example. To evaluate
Q UIC 3, we have used array manipulating C programs from SV-COMP. We show that
our implementation is competitive and can automatically discover non-trivial quantified
invariants.
     In summary, the paper makes the following contributions: (a) extends IC3 frame-
work to support quantifiers; (b) develops quantifier generalization techniques; (c) de-
velops techniques for discovering quantifier instantiations during verification; and (d)
reports on our implementation for software verification.
2 Preliminaries
Logic. We consider First Order Logic modulo the combined theory of Linear Integer
Arithmetic (LIA) and Arrays. We denote the theory by T and the logic by F OL(T ).
We assume that the reader is familiar with the basic notions of F OL(T ) and provide
only a brief description to set the notation. Formulas in F OL(T ) are defined over a
signature Σ which includes sorts int and array, where sort int is also used as the sort
of the array indices and data. We assume that the signature Σ includes equality (=),
interpreted functions, predicates, and constants of arithmetic (i.e., the functions +, −,
∗, the predicates <, ≤, and the constants 1, 2, etc.) and of arrays (i.e., the functions sel
and store).
    In addition, Σ may be extended with uninterpreted constants. In particular, we as-
sume that Σ includes special Skolem uninterpreted constants SK = {ski } of sort int
for i in natural numbers.
    We denote by ΣT the interpreted part of Σ, and by X ⊆ Σ the set of uninterpreted
constants (e.g., a or ski , but not 1). In the sequel we write ϕ(X), and say that ϕ is
defined over X, to denote that ϕ is defined over signature Σ = ΣT ∪ X. We write
Const (ϕ) ⊆ X for the set of all uninterpreted constants that appear in ϕ. In the rest of
the paper, whenever we refer to constants, we only refer to the uninterpreted ones.
    We write T for the set of terms of F OL(T ), and V for the set of (sorted) variables.
We assume that int variables in V are of the form vi , where i is a natural number. Thus,
we can refer to all such variables by their numeric name. For a formula ϕ, we write
Terms(ϕ) ⊆ T and FVars(ϕ) ⊆ V for the terms and free variables of ϕ, respectively.
    A substitution σ : V → T is a partial mapping from V to terms in T that pertains
to the sort constraints. We write dom(σ) to denote the domain of σ, and range(σ) to
denote its range. For a formula ϕ, we write ϕσ for the result of applying substitution
σ to ϕ. Abusing notation, we write ∅ for an empty substitution, i.e., a substitution σ
such that dom(σ) = ∅. Given two substitutions σ1 and σ2 , we write (σ1 | σ2 ) for a
composition of substitutions defined such that: (σ1 | σ2 )(x) = σ1 (x) if x ∈ dom(σ1 ),
and σ2 (x), otherwise. We define a special Skolem substitution sk : V → T such that
sk (vi ) = sk i for sk i ∈ SK . Given a formula L, we write Lsk for Lsk , and given a
substitution σ.
    We write abs(U, ϕ) = (ψ, σ) for an abstraction function that given a set of un-
interpreted constants U and a formula ϕ returns an abstraction ψ of ϕ in which the
constants are replaced by free variables, as well as a substitution σ that records the
mapping of variables back to the constants that they abstract. Formally, we require that
abs(U, ϕ) = (ψ, σ) satisfies the following: ψσ = ϕ, dom(σ) = FVars(ψ)\FVars(ϕ),
and U ∩ Terms(ψ) = ∅. The requirements ensure that abs abstracts all uninterpreted
constants in U , and σ maps the newly introduced variables back to the constants. Fur-
thermore, we require that for every skolem constant sk i in U , abs(U, ϕ) abstracts sk i
in ϕ to vi in ψ, and accordingly, σ(vi ) = sk i . This ensures that applying skolemization,
followed by abstraction of SK , reintroduces the same variables and does not result in
variable renaming. That is, abs(SK , ϕsk ) = (ϕ, _).
    We write ∀ϕ for a formula obtained from ϕ by universally quantifying all free vari-
ables of ϕ, and ∃ϕ for a formula obtained by existential quantification, respectively. For
convenience, given a set of constants U and a ground formula ϕ (i.e., a formula where
all terms are ground), we write ∃U · ϕ for ∃ψ, where (ψ, σ) = abs(U, ϕ). We write
ϕ ⇒ ψ do denote the validity of ϕ → ψ.

Model Based Projection. Given a ground formula ϕ, a model M of ϕ, and a set of un-
interpreted constants U ⊆ Const (ϕ), (partial, or incomplete) Model Based Projection,
MBP, is a function P M BP(U, ϕ, M ) = (ψ, W ) such that 1. ψ is a ground monomial
(i.e., conjunction of ground literals), 2. W ⊆ U and Const (ψ) ⊆ Const (ϕ) \ (U \ W ),
3. ψ ⇒ (∃U \ W · ϕ), 4. M |= ψ, 5. P M BP is finite ranging in its third argument: for a
fixed U and ϕ, the set {P M BP(U, ϕ, M ) | M |= ϕ} is finite. Intuitively, the monomial
ψ underapproximates (implies) the result of eliminating the existential quantifiers per-
taining to U \ W from ϕ (where quantifier elimination itself may not even be defined).
It, therefore, represents one of the ways of satisfying the result of quantifier elimination.
The underapproximation ψ is chosen such that it is consistent with the provided model
M . In this paper, MBP is used as a way to underapproximate the pre-image of a set of
states represented implicitly by some formula.
    An MBP is called complete if W is always empty. A complete MBP for Linear
Arithmetic has been presented in [25] and a partial MBP for the theory of arrays has
been presented in [24]. Importantly, in the partial MBP of [24], the remaining set of
constants, W , never contains any constant of sort array. We refer the readers to [25,24]
and to [6] for details. A complete MBP under-approximates quantifier elimination rel-
ative to a given model. Such an MBP can only exist if the underlying theory admits
quantifier elimination. Since the theory of arrays does not admit quantifier elimination
it only admits a partial MBP.
   In the paper, we further require an MBP to eliminate all the constants of sort array
from U , such as the MBP of [24].

Interpolation. Given a ground formula A, and a ground monomial B such that A ⇒
¬B, (partial) interpolation, ITP, is a function P I TP(A, B) = (ϕ, U ), s.t. 1. ϕ is a
ground clause (i.e., a disjunction of ground literals), 2. U ⊆ Const (B) \ Const (A)
and Const (ϕ) ⊆ (Const (A) ∩ Const (B)) ∪ U , 3. A ⇒ ∀U · ϕ, and 4. ϕ ⇒ ¬B. The
set of constants U denotes the constants of ϕ that exceed the set of shared constants
of A and B. An interpolation procedure is complete if for any pair A, B, the returned
set U is always empty. The formula ϕ produced by a complete interpolation procedure
is called an interpolant of A and B. Note that our definitions admit a trivial partial
interpolation procedure defined as P I TPtriv (A, B) = (¬B, Const (B) \ Const (A)).

Safety problem. We represent transition systems via formulas in F OL(T ). The states
of the system correspond to structures over a signature Σ = ΣT ∪ X, where X denotes
the set of (uninterpreted) constants. The constants in X are used to represent program
variables. A transition system is a pair hInit (X), Tr (X, X ′ )i, where Init and Tr are
quantifier-free ground formulas in F OL(T ). Init represents the initial states of the
system and Tr represents the transition relation. We write Tr (X, X ′ ) to denote that Tr
is defined over the signature ΣT ∪ X ∪ X ′ , where X is used to represent the pre-state of
a transition, and X ′ = {a′ | a ∈ X} is used to represent the post-state. A safety problem
is a triple hInit (X), Tr (X, X ′ ), Bad (X)i, where hInit , Tr i is a transition system and
Bad is a quantifier-free ground formula in F OL(T ) representing a set of bad states.
    The safety problem hInit (X), Tr(X, X ′ ), Bad (X)i has a counterexample of length
k if the following formula is satisfiable:

                                                  ^
                                                  k−1
        BMC k (Init , Tr , Bad ) = Init (X0 ) ∧         Tr (Xi , Xi+1 ) ∧ Bad (Xk ),
                                                  i=0

where Xi = {ai | a ∈ X} is a copy of the constants used to represent the state of the
system after the execution of i steps. The transition system is safe if the safety problem
has no counterexample, of any length.
Interpolation sequence and inductive invariants. An interpolation sequence of length k
for a safety problem hInit (X), Tr(X, X ′ ), Bad (X)i is a sequence of formulas I1 (X), . . . , Ik (X)
such that (i) Init (X) ⇒ I1 (X), (ii) Ij (X)∧Tr (X, X ′ ) ⇒ Ij+1 (X ′ ) for every 1 ≤ j ≤
k−1, and (iii) Ik (X) ⇒ ¬Bad (X). If an interpolation sequence of length k exists, then
the transition system has no counterexample of length k. An inductive invariant is a for-
mula Inv (X) such that (i) Init(X) ⇒ Inv (X), (ii) Inv (X) ∧ Tr (X, X ′ ) ⇒ Inv (X ′ ),
and (iii) Inv (X) ⇒ ¬Bad (X). If such an inductive invariant exists, then the transition
system is safe.


3 Quantified IC3

In this section, we present Q UIC 3 – a procedure for determining a safety of a transition
system by inferring quantified inductive invariants. Given a safety problem, Q UIC 3
attempts to discover an inductive invariant Inv(X) as a universally-quantified formula
of F OL(T ) (where quantification is restricted to variables of sort int) or produce a
counterexample.
    We first present Q UIC 3 as a set of rules, following the presentation style of [21,25,5,24,18].
We focus on the data structures, the key differences between Q UIC 3 and IC3, and
soundness of the rules. An imperative procedure based on these rules is presented in
Section 4. We assume that the reader is familiar with the basics of IC3. Throughout the
section, we fix a safety problem P = hInit (X), Tr (X, X ′ ), Bad (X)i, and assume that
Init , Tr and Bad are quantifier free ground formulas. For convenience of presentation,
we use the notation F (A) to denote the formula (A(X) ∧ Tr (X, X ′ )) ∨ Init(X ′ ) that
corresponds to the forward image of A over the Tr extended by the initial states.
    The rules of Q UIC 3 are shown in Alg. 1. Similar to IC3, Q UIC 3 maintains a queue
Q of proof obligations (POBs), and a monotone inductive trace T of frames contain-
ing lemmas at different levels. However, both the proof obligations and the lemmas
maintained by Q UIC 3 are quantified.
Quantified Proof Obligations. Each POB in Q is a triple hm, σ, ii, where m is a mono-
mial over X such that FVars(m) are of sort int, σ is a substitution such that FVars(m) ⊆
dom(σ) and range(σ) ⊆ X ′ ∪ SK , and i is a natural number representing the frame
index at which the POB should be either blocked or extended. The POB hm, σ, ii ex-
presses an obligation to show that no state satisfying ∃m is reachable in i steps of Tr .
The substitution σ records the specific instance of the free variables in frame i + 1 that
were abstracted during construction of m. Whenever the POB is blocked, a universally
    Input: A safety problem hInit(X), Tr (X, X ′ ), Bad (X)i.
    Assumptions: Init, Tr and Bad are quantifier free.
    Data: A POB queue Q, where a POB c ∈ Q is a triple hm, σ, ii, m is a conjunction of
          literals over X and free variables, σ is a substitution s.t. mσ is ground, and i ∈ N.
          A level N . A quantified trace T = Q0 , Q1 , . . ., where for every pair (ℓ, σ) ∈ Qi ,
          ℓ is a quantifier-free formula over X and free variables and σ a substitution s.t. ℓσ
          is ground.
    Notation: F(A) = (A(X) ∧ Tr (X, X ′ )) ∨ Init(X ′ ); qi (Q) = {ℓσ | (ℓ, σ) ∈ Q};
     ∀Q = {∀ℓ | (ℓ, σ) ∈ Q}.

    Output: Safe or Cex
    Initially: Q = ∅, N = 0, Q0 = {(Init, ∅)}, ∀i > 0 · Qi = ∅.
    repeat
        Safe If there is an i < N s.t. ∀Qi ⊆ ∀Qi+1 return Safe.
        Cex If there is an m, σ s.t. hm, σ, 0i ∈ Q return Cex.
        Unfold If qi (QN ) ⇒ ¬Bad , then set N ← N + 1.
        Candidate If for some m, m ⇒ qi (QN ) ∧ Bad , then add hm, ∅, N i to Q.
        Predecessor If hm, ξ, i + 1i ∈ Q and there is a model M s.t. M |= qi (Qi ) ∧ Tr ∧ (m′sk ), add
            hψ, σ, ii to Q, where (ψ, σ) = abs(U, ϕ) and (ϕ, U ) = P M BP(X ′ ∪ SK , Tr ∧ m′sk , M ).
        NewLemma For 0 ≤ i < N , given a POB hm, σ, i + 1i ∈ Q s.t. F(qi (Qi )) ∧ m′sk is
           unsatisfiable, and L′ = I TP(F(qi (Qi )), m′sk ), add (ℓ, σ) to Qj for j ≤ i + 1, where
           (ℓ, _) = abs(SK , L).
        Push For 0 ≤ i < N and ((ϕ ∨ ψ), σ) ∈ Qi , if (ϕ, σ) 6∈ Qi+1 , Init ⇒ ∀ϕ and
            (∀ϕ) ∧ ∀Qi ∧ qi (Qi ) ∧ Tr ⇒ ∀ϕ′ , then add (ϕ, σ) to Qj , for all j ≤ i + 1.

    until ∞;         Algorithm 1: The rules of Q UIC 3 procedure.

quantified lemma ∀ℓ is generated in frame i (as a generalization of ∀¬m), and, σ is used
to discover the specific instance of ∀ℓ that is necessary to prevent generating the same
POB again.

Quantified Inductive Trace. A quantified monotone inductive trace T is a sequence of
sets Qi . Each Qi is a set of pairs, where for each pair (ℓ, σ) in Qi , ℓ is a formula over X,
possibly with free variables, such that all free variables FVars(ℓ) are of sort int, and σ
is a substitution such that FVars(ℓ) ⊆ dom(σ) and range(σ) ⊆ X ′ ∪ SK . Intuitively,
a pair (ℓ, σ) corresponds to a universally quantified lemma ∀ℓ and its ground instance
ℓσ. If ℓ has no free variables, it represents a ground lemma (as in the original IC3). We
write ∀Qi = {∀L | (L, σ) ∈ Qi } for the set of all ground and quantified lemmas in Qi ,
and qi (Qi ) = {ℓσ | (ℓ, σ) ∈ Qi } for the set of all instances in Qi .
    Q UIC 3 maintains that the trace T is inductive and monotone. That is, it satisfies the
following conditions, where N is the size of T :

       Init ⇒ ∀Q0            ∀0 ≤ i < N · ∀Qi ∧ Tr ⇒ ∀Qi+1                  ∀Qi+1 ⊆∀Qi

The first two conditions ensure inductiveness and the last ensures syntactic monotonic-
ity. Both are similar to the corresponding conditions in IC3.
The rules. The rules Safe, Cex, Unfold, Candidate are essentially the same as their IC3
counterparts. The only exception is that, whenever the lemmas of frame i are required,
the instances qi (Qi ) of the quantified lemmas in Qi are used (instead of ∀Qi ). This
ensures that the corresponding satisfiability checks are decidable and do not diverge.
Predecessor rule. Predecessor extends a POB hm, ξ, i + 1i ∈ Q from frame i + 1 with
a predecessor POB hψ, σ, ii at frame i. The precondition to the rule is satisfiability of
qi (Qi ) ∧ Tr ∧ (m′sk ). Note that all free variables in the current POB m are skolemized
via the substitution sk (recall that all the free variables are of sort int) and all constants
are primed.
     Predecessor rule extends the corresponding rule of IC3 in two ways. First, POBs
are generated using partial MBP. The P M BP(X ′ ∪SK , Tr ∧m′sk , M ) is used to construct
a ground monomial ϕ over X ∪ X ′ ∪ SK , describing a predecessor of m′sk . Whenever
ϕ contains constants from X ′ ∪ SK, these are abstracted by fresh free variables to
construct a POB ψ over X. Thus, the newly constructed POB is not ground and its free
variables are implicitly existentially quantified. (Since P M BP is guaranteed to eliminate
all constants of sort array, the free variables are all of sort int). Second, the Predecessor
maintains with the POB ψ the substitution σ that corresponds to the inverse of the
abstraction used to construct ψ from ϕ, i.e., ψσ = ϕ. It is used to introduce a ground
instance that blocks ψ as a predecessor of hm, ξ, i + 1i when the POB is blocked (see
NewLemma).
     The soundness of Predecessor (in the sense that it does not introduce spurious coun-
terexamples) rests on the fact that every state in the generated POB has a Tr successor
in the original POB. This is formalized as follows:
Lemma 1. Let hm, ξ, i+1i ∈ Q and let (ψ, σ, i) be the POB computed by Predecessor.
Then, (∃ψ) ⇒ ∃X ′ · (T r ∧ ∃m′ ).

Proof. From the definition of Predecessor, (ψ, σ) = abs(U, ϕ), where (ϕ, U ) =
P M BP (X ′ ∪ SK , Tr ∧ m′sk , M ). The set U ⊆ X ′ ∪ SK are the constants that were not
eliminated by MBP. Then, by properties of P M BP , ψσ ⇒ ∃(X ′ , SK ) \ U · T r ∧ m′sk .
Note that (∃U ·ϕ) = ∃ψ. By abstracting U in ϕ and existentially quantifying over the re-
sulting variables in both sides of the implication, we get that ∃ψ ⇒ ∃X ′ , SK ·T r∧m′sk .
Since SK does not appear in T r, the existential quantification distributes over Tr :
∃X ′ , SK · T r ∧ m′sk ≡ ∃X ′ · (T r ∧ ∃m′ ).                                          ⊓
                                                                                       ⊔

    By induction and Lemma 1, we get that if hψ, σ, ii is a POB in Q, then every state
satisfying ∃ψ can reach a state in Bad .
NewLemma rule. NewLemma creates a potentially quantified lemma ℓ and a corre-
sponding instance ℓσ to block a quantified POB hm, σ, i + 1i at level i + 1. Note that
if ℓ is quantified, then while the instance ℓσ is guaranteed to be new at level i + 1,
the lemma ℓ might already appear in Qi+1 . The lemma ℓ is first computed as in IC3,
but using a skolemized version of the POB. Second, if any skolem constants remain in
the lemma, then they are re-abstracted into the original variables. The corresponding
instance of ℓ is determined by the substitution σ of the POB. Note that the instance ℓσ
is well defined since abs abstracts skolem constants back into the variables (of sort int)
that introduced them, ensuring that FVars(ℓ) ⊆ dom(σ). Note further that if ℓ has no
void init_arrray(int[] A, int sz) {
  1: for (int i = 0; i < sz; i++) A[i] = 0;
  2: j = nd(); assume(0 <= j && j < sz);
  3: assert(A[j] == 0);}
                           Fig. 1. An array manipulating program.
free variables, then the substitution σ is redundant and could be replaced by an empty
substitution. (In fact, it is always sufficient to project σ to FVars(ℓ).)
    The soundness of NewLemma follows form the fact that every lemma (ℓ, σ) that is
added to the trace T keeps the trace inductive. Formally:

Lemma 2. Let (ℓ, σ) be a quantified lemma added to Qi+1 by NewLemma. Then,
F (∀Qi ) ⇒ (∀ℓ′ ).

Proof. ℓ is abs(SK , L), where L′ = I TP(F (qi (Qi )), m′sk ). Therefore, F (qi (Qi )) ∧
¬L′ is unsatisfiable. Let Ψ be F (∀Qi ) ∧ (¬∀ℓ′ ), and assume, to the contrary, that Ψ
is satisfiable. Since no constants from SK appear in F (∀Qi ) and ℓ is abs(SK , L), Ψ
is equi-satisfiable to F (∀Qi ) ∧ (¬L′ ). Let M be the corresponding model. Then, in
contradiction, M |= F (qi (Qi )) ∧ (¬L′ ).                                             ⊓
                                                                                       ⊔

    Rules Predecessor and NewLemma use m′sk that is skolemized with our special
skolem substitution where sk (vi ) = sk i . We note that while the skolem constants in
m′sk are always a subset of SK and do not overlap with X ∪ X ′ , they may overlap the
existing skolem constants that appear in the rest of the formula (e.g., if the rest of the
formula contains qi (Qi−1 ), where the ground instances result from previously blocked
POBs and, therefore, also contain skolem constants). In this sense, our skolemization
appears non-standard. However, all the claims in this section only rely on the fact that
the range of sk is SK and that SK is disjoint from X ∪ X ′ , which holds for sk .
Push rule. Push is similar to its IC3 counterpart. It propagates a (potentially quantified)
lemma to the next frame. The key difference is the use of quantified formulas ∀Qi (and
their instantiations qi (Qi ) in the pre-condition of the rule. Thus, checking applicability
of Push requires deciding validity of a quantified FOL formula, which is undecidable
in general. In practice„ we use a weaker, but decidable, variant of these rules. In par-
ticular, we use a finite instantiation strategy to instantiate ∀Qi in combination with all
of the instantiations qi (Qi ) discovered by Q UIC 3 before theses rules are applied. This
ensures progress (i.e., Q UIC 3 never gets stuck in an application of a rule) at an ex-
pense of completeness (some lemmas are not pushed as far as possible, which impedes
divergence).
    We illustrate the rules on a simple array-manipulating program init_array shown
in Fig. 1. In the program, assume and assert stand for the usual assume and assert
statements, respectively, and nd returns a non-deterministic value. We assume that the
program is converted into a safety problem as usual. In this problem, a special variable
pc is used to indicate the program counter. The first POB found by Candidate is pc =
3 ∧ sel(A, j) 6= 0. Its predecessor, is pc = 2 ∧ sel(A, v0 ) 6= 0 ∧ 0 ≤ v0 < sz and the
corresponding substitution is (v0 7→ j). Note that since P M BP could not eliminate j,
it was replaced by a free variable. Eventually, this POB is blocked, the lemma that is
added is ∀((pc = 2 ∧ 0 ≤ v0 < sz) ⇒ sel(A, v0 ) = 0).
   N ← 0; Q0 = {(Init, ∅)}
   if Init ∧ Bad then
        return C EX
   while (true) do
        N ← N + 1; QN ← ∅
        if Quic3_MakeSafe (Bad , ∅, N ) = C EX then
             return C EX
        if Quic3_Push () = S AFE then
             return S AFE
   end
      Fig. 2. Main Procedure (Quic3_Main ). Wlog, we assume that Bad is a monomial.
Soundness. We conclude this section by showing that applying Q UIC 3 rules from Alg. 1
in any order is sound:
Lemma 3. If Q UIC 3 returns Cex, then P is not safe (and there exists a counterexam-
ple). Otherwise, if Q UIC 3 returns Safe, then P is safe.

Proof. The first case follows immediately from Lemma 1. The second case follows
from the properties of the inductive trace maintained by Q UIC 3 that ensure that when-
ever Safe is returned (by Safe rule), a safe inductive invariant is obtained. Lemma 2
ensures that these properties are preserved whenever a new quantified lemma is added.
Soundness of all other rules follows the same argument as the corresponding rules of
IC3.                                                                                 ⊓
                                                                                     ⊔

   In fact, Q UIC 3 ensures a stronger soundness guarantee:
Lemma 4. In every step of Q UIC 3, for every k < N , the sequence {∀Qi }ki=1 is an
interpolation sequence of length k for P .
Thus, if Q UIC 3 reaches N > k, then there are no counterexample of length k.


4 Progress and Counterexamples
Safety verification of transition systems described in the theory of LIA and Arrays is
undecidable in general. Thus, there is no expectation that Q UIC 3 always terminates.
None-the-less, it is desirable for such a procedure to have strong progress guarantees
– the longer it runs, the more executions are explored. In this section, we show how to
orchestrate the rules defining Q UIC 3 (shown in Alg. 1) into an effective procedure that
guarantees progress in exploration and produces a shortest counterexample, if it exists.
Realization of Q UIC 3. Fig. 2 depicts procedure Quic3_Main – an instance of Q UIC 3
where each iteration, starting from N = 0, consists of a Quic3_MakeSafe phase fol-
lowed by a Quic3_Push phase. The Quic3_MakeSafe phase, described in Fig. 3,
starts by initializing Q to the POB (Bad , ∅, N ) (this is a degenerate application of
Candidate that is sufficient when Bad is a monomial). It then applies Predecessor
and NewLemma iteratively until either a counterexample is found or Q is emptied.
NewLemma is preceded by an optional generalization procedure (Line 16) that may
introduce additional quantified variables and record the constants that they originated
   Input: (Cube m0 , Substitution σ0 , Level i0 )
   Data: Queue Q of triples hm, σ, ii, where m is a cube, σ is a substitution and i is a level
 1 Q = ∅
   // Apply Candidate rule
 2 Add(Q, hm0 , σ0 , i0 i)
 3 while ¬Empty (Q) do
 4    hm, ξ, ii ← Top(Q)
  5      if i = 0 then
                // Apply Cex rule; Found a counterexample
  6          return C EX
  7      M ← SAT(qi (Qi−1 ) ∧ Tr ∧ (m′sk ))
  8      if M 6= ⊥ then
                // Apply Predecessor rule
  9             (ϕ, U ) ← P M BP(X ′ ∪ SK , Tr ∧ m′sk , M )
 10             (ψ, σ) ← abs(U, ϕ)
 11             Add(Q, hψ, σ, i − 1i)
 12      else
 13             Remove (Q, hm, ξ, ii)
 14             L′ ← I TP(qi (Qi−1 ∧ Tr ), m′sk )
                // Abstract all skolem constants
 15             (ℓ, _) ← abs(SK , L)
                // Optional quantified generalization (see Sec. 5)
 16             (ℓ, ξ) ← QGen(ℓ, hm, ξ, ii)
                // Apply NewLemma rule
 17             forall j ≤ i, Qj ← Qj ∪ {(ℓ, ξ)}
18    end
19    return B LOCKED
                           Fig. 3. Quic3_MakeSafe procedure of Q UIC 3.
from by extending the substitution ξ. We defer discussion of this procedure to Section 5;
in the simplest case, it will return the same lemma with the same substitution ξ. At the
end of Quic3_MakeSafe, the trace (Qi )i is an interpolation sequence of length N . The
Quic3_Push applies Push iteratively from frame i = 1 to i = N . The corresponding
satisfiability queries are restricted to use the existing instances of quantified lemmas
and a finite set of instantiations pre-determined by heuristically chosen triggers. If, as
a result of pushing, two consecutive frames become equal (rule Safe), Quic3_Main
returns Safe.
Progress. Recall that we use a deterministic skolemization procedure. Namely, for a
POB hm, ξ, ii, in every satisfiability check of the form qi (Qi−1 ) ∧ Tr ∧ (m′sk ), the
same skolem substitution (defined by sk (vi ) = sk i ) is used in m′sk , even if the rest of
the formula (i.e., qi (Qi−1 )) changes. The benefit of using a deterministic skolemization
procedure is that it ensures that all applications of P M BP in Predecessor use exactly
the same formula T r ∧ m′sk and exactly the same set of constants. As a result, the
number of predecessors (POBs) generated by applications of Predecessor for each POB
is bounded by the finite range of P M BP in its third (model) argument:
Lemma 5. If a deterministic skolemization is used, then for each POB hm, ξ, ii, the
number of POBs generated by applying Predecessor on hm, ξ, ii is finite.
Proof. For simplicity, we ignore the application of quantified generalization; the proof
extends to handle it as well. After a quantified lemma (ℓ, ξ) is added to Qi−1 , every
model M |= qi (Qi−1 ) ∧ Tr ∧ m′sk that is discovered when applying Predecessor on
hm, ξ, ii will be such that M |= ℓξ. Recall that the lemma was generated by a POB
hϕ, σ, i − 1i that was blocked since qi (Qi−2 ) ∧ Tr ∧ ϕ′sk was unsatisfiable, and (ℓ, _) =
abs(SK , L) where L′ = I TP(qi (Qi−2 ∧ Tr ), ϕ′sk ). Therefore L ∧ ϕsk ≡ ⊥. Since
abs maps each skolem constant back to the variable that introduced it, we have that the
skolems in L are abstracted to the original variables from ϕ. Hence, ℓ ∧ ϕ ≡ ⊥, which
implies that ℓξ∧ϕξ ≡ ⊥. Thus, if M |= qi (Qi−1 )∧Tr ∧m′sk then M 6|= ϕξ. Therefore,
P M BP (X ′ ∪ SK , T r ∧ m′sk , M ) 6= (ϕξ, _). Meaning, once the POB that generated
the lemma was blocked, it cannot be rediscovered as a predecessor of hm, ξ, ii. Since
the first two arguments of P M BP are the same in all applications of Predecessor on
hm, ξ, ii (due to the deterministic skolemization), the finite range of P M BP implies that
only finitely many predecessors are generated for the POB hm, ξ, ii.                      ⊓
                                                                                          ⊔

     Thus, for any value of N , there is only a finite number of POBs that are added to Q
and processed by the rules, resulting in a finite number of rule applications. Moreover,
since Quic3_Push restricts the use of quantified lemmas to existing ground instances
and a finite instantiation scheme, and since the other rules also use only these instances,
all satisfiability queries posed to the solver are of quantifier-free formulas in the com-
bined theories of LIA and Arrays, and as a result guaranteed to terminate. This means
that each rule is terminating. Therefore, Quic3_Main always makes progress in the
following sense:

Lemma 6. For every k ∈ N, Quic3_Main either reaches N = k, returns Safe„ or
finds a counterexample.

Shortest Counterexamples. Quic3_Main increases N only after an interpolation se-
quence of length N is obtained, in which case it is guaranteed that no counterexample
up to this length exists. Combined with Lemma 6 that ensures progress, this implies
that Quic3_Main always find a shortest counterexample, if one exists:

Corollary 1. If there exists a counterexample, then Quic3_Main is guaranteed to ter-
minate and return a shortest counterexample.


5 Quantified Generalization

Q UIC 3 uses quantified POBs to generate quantified lemmas. However, these lemmas are
sometimes too specific, hindering convergence. This is addressed by quantified general-
ization (QGen), a key part of Q UIC 3. The Q UIC 3 rules in Alg. 1 are extended with the
rule QGen shown in Alg. 2, and Quic3_MakeSafe (Figure 3) is extended with a call
to QGen, which implements QGen, before a new lemma is added to its corresponding
frame.
QGen rule. QGen generalizes a (potentially quantified) lemma (ℓ, ξ) ∈ Qi+1 into a
new quantified lemma (g, σ) such that (∀g) → (∀ℓ) is valid, i.e., the new lemma g
    QGen For 0 ≤ i < n and a lemma (ℓ, ξ) ∈ Qi+1 , let g be a formula and σ a substitution such
       that (i) gσ ≡ ℓξ, (ii) FVars(ℓ) ⊆ FVars(g), and (iii) F(qi (Qi )) → ∀g ′ . Then, add (g, σ)
       to Qj for all 0 ≤ j ≤ i + 1.
         Algorithm 2: QGen rule for Quantified Generalization in Q UIC 3.
is stronger than ℓ. The new quantified lemma g and a substitution ρ (s.t. gρ ≡ ℓ) are
constructed by abstracting some terms of ℓ with fresh universally quantified variables.
If the new formula ∀g is a valid lemma, i.e., F (qi (Qi )) → ∀g ′ is valid, then QGen
adds (g, σ) to Qj for 0 ≤ j ≤ i + 1, where σ = ξ|ρ. Note that the check ensures that
the new lemma maintains the interpolation sequence property of the trace. In the rest of
this section, we describe two heuristics to implement QGen that we found useful in our
benchmarks.

Simple QGen abstracts a single term in the input lemma ℓ by introducing one additional
universally quantified variable to ℓ. In the new lemma g, the new variable v appears only
as an index of an array (e.g., sel(A, v)) or as an offset (e.g., sel(A, i + v)). Simple QGen
considers all sel terms in ℓ and identifies sub-terms t of index terms for which ℓ imposes
lower and upper bounds. Each term t is abstracted in turn with bounds used as guards.
For example, if ℓ is 0 < sz → (sel(A, 0) = 42) and t = 0 of sel(A, 0), then a candidate
(g, σ) is 0 ≤ v0 < sz → sel(A, v0 ) = 42, and {v0 7→ 0}, where v0 is universally
quantified.

Arithmetic QGen. Simple QGen does not infer correlations neither between abstracted
terms nor between index and value terms. For example, it is unable to create a lemma
of the form ∀v · 0 ≤ v < sz → (sel(A, v) = exp(v)), where exp(v) is some linear
expression involving v. Arithmetic QGen addresses this limitation by extracting and
generalizing a correlation between interpreted constants in the input lemma ℓ. Arith-
metic QGen works on lemmas ℓ of the form (ψ ∧ φ0 ∧ · · · ∧ φn−1 ) → φn , where
there is a formula p(~v ) with free variables ~v and a set of substitutions {σk }nk=0 s. t.
φk = pσk . For example, ℓ is ((1 < sz) ∧ (sel(A, 0) = 42)) → (sel(A, 1) = 44),
where p(i, j) is sel(A, i) = j, σ0 is {i 7→ 0, j 7→ 42}, and σ1 is {i 7→ 1, j 7→ 44}.
The substitutions can be viewed as data points and generalized by a convex hull, de-
noted ch. For example, ch({σ0 , σ1 }) = 0 ≤ i ≤ 1 ∧ j = 2i + 42. The lemma ℓ
is strengthened by replacing the substitution of φn with the convex hull by rewriting
ℓ into ∀~v · (ch({σ1 , . . . , σn }) ∧ ψ ∧ φ0 · · · ∧ φn−1 ) → p(~v ). In our running example,
this generates ∀i, j · (0 ≤ i ≤ 1 ∧ j = 2i + 42 ∧ 1 < sz) ∧ (sel(A, 0) = 42)) →
(sel(A, i) = j). Note that only φn is generalized, while all other φk , 0 ≤ k < n, pro-
vide the data points. Applying standard generalization might simplify the lemma further
by dropping (sel(A, 0) = 42) and combining i ≤ 1 ∧ 1 < sz into 1 < sz, resulting
in ∀i · (0 ≤ i ≤ sz) → (sel(A, i) = 2i + 42). Note that arithmetic QGen applies to
arbitrary linear arithmetic terms by replacing the convex hull (ch) with the polyhedral
join (⊔).
    These two generalizations are sufficient for our benchmarks. However, the power of
Q UIC 3 comes from the ability to integrate additional generalizations, as required. For
example, arithmetic QGen can be extended to consider not only a single lemma, but
also mine other existing lemmas for potential data points.
6 Experimental Results

We have implemented Q UIC 3 within the CHC engine of Z3 [12,22] and evaluated it on
array manipulating C programs from SV-COMP [4] and from [13]. We have converted
C programs to CHC using S EA H ORN [19]. In most of these examples, array bounds
are fixed constants. We have manually generalized array bounds to be symbolic to en-
sure that the problems require quantified invariants. Note, however, that our approach
is independent of the value of the array bound (concrete or symbolic). We stress that
using S EA H ORN prevents us from using the “best CHC encoding” for a given problem,
which is unfortunately a common evaluation practice. By using S EA H ORN as is, we
show how Q UIC 3 deals with complex realistic intermediate representation. For exam-
ple, S EA H ORN generates constraints supporting memory allocation and pointer arith-
metic. This complicates the necessary inductive invariants even for simple examples.
While we could have used a problem-specific encoding for specially selected bench-
marks, such an encoding does not uniformly extend to all SV-COMP benchmarks.
    Experiments were done on a Linux machine with an Intel E3-1240V2 CPU and a
timeout of 300 seconds. The source code for Q UIC 3 is available in the main Z3 repos-
itory at https://github.com/Z3Prover/z3. The CHC for all the benchmarks are
available at https://github.com/chc-comp/quic3. The results for the safe in-
stances – the most interesting – are shown in Table 1. We compare with the S PACER
engine of Z3. S PACER supports arrays, but not quantifiers. As expected, S PACER times
out on all of the benchmarks. We emphasize the difference in the number of lemmas
discovered by both procedures. Clearly, since Q UIC 3 discovers quantified lemmas, it
generates significantly fewer lemmas than S PACER. Each quantified lemma discovered
by Q UIC 3 represents many ground lemmas that are discovered by S PACER.
    As shown in Table 1, Q UIC 3 times out on some of the instances. This is due to
a deficiency of the current implementation of QGen. Currently, QGen only considers
one candidate for abstraction, and generalization fails if that candidate fails. Allowing
QGen to try several candidates should solve this issue.
    Unfortunately, we were unable to compare Q UIC 3 to other related approaches. To
our knowledge, tools that participated in SV-COMP 2018 are not able to discover the
necessary quantified invariants and often use unsound (i.e., bounded) inference. The
closely related tools, including S AFARI [1], B OOSTER [2], and [13] are no longer
available. Based on our understanding of their heuristics, the invariants required in our
benchmarks are outside of the templates supported by these heuristics.


7 Related Work

Universally quantified invariants are necessary for verification of systems with un-
bounded state size (i.e., the size of an individual system state is unbounded) such as
array manipulating programs, programs with dynamic memory allocation, and parame-
terized systems in general. Thus, the problem of universal invariant inference has been
a subject of intense research in a variety of areas of automated verification. In this sec-
tion, we present the related work that is technically closest to ours and is applicable to
the area of software verification.
Table 1. Summary of results. TO is timeout; Depth is the size of inductive trace; Lemmas and Inv
are the number of lemmas discovered overall and in invariant, respectively.
  Benchmark                     Q UIC 3           Z3/S PACER    Benchmark                       Q UIC 3            Z3/S PACER
                      Depth Lemmas Inv Time [s] Depth Lemmas                           Depth Lemmas Inv Time [s] Depth Lemmas
  array-init-const       6     24      7 0.14    130    4,483   std-copy9-tucg          31     538 145 14.74      111    5,078
  array-init-partial     9     45     12 0.34    126    4,224   std-copyInitSum2-tucg 32       511     –  TO      77     2,987
  array-mono-set         6     25      9 0.22     70    2,436   std-copyInitSum3-tucg 14       127     –  TO      76     3,103
  array-mono-tuc         6     25      9 0.21     70    2,422   std-copyInitSum-tucg     9     59     21 0.43     78     3,085
  array-mul-init-tuc   129   8,136     – TO      131    8,393   std-copyInit-tucg       10     69     27 0.59     75     2,851
  array-nd-2-c-true      6     37      – TO       39    1,482   std-find-tucg            8     35      7  0.32    105    2,915
  array-reverse          6     21      5 0.18    144     729    std-init2-tucg           7     29      8  0.14    88     3,662
  array-shadowinit-tuc 30     252      – TO       99    5,005   std-init3-tucg           7     30      8  0.14    95     4,122
  array-swap            13    136     64 6.38     45    2,700   std-init4-tucg           7     31      8  0.14    94     3,898
  array-swap-twice      14    155      – TO       45    2,991   std-init5-tucg           7     32      8  0.14    93     4,152
  sanfoundry-02-tucg    11     89     31 1.57     46    1,986   std-init6-tucg           7     33      8  0.15    95     4,090
  sanfoundry-10-tucg    11     71     23 0.67    109    3,245   std-init7-tucg           7     34      8  0.14    100    4,916
  sanfoundry-27-tucg     6     24      7 0.14    131    4,568   std-init8-tucg           7     35      8  0.15    97     4,604
  std-compMod-tucg      10    120     61 5.48     58    3,871   std-init9-tucg           7     32     11 0.21     100    4,929
  std-copy1-tucg         6     33     14 0.33     89    4,035   std-maxInArray-tucg      7     30      9  0.33    132    4,618
  std-copy2-tucg         9     65     25 0.77     73    2,751   std-minInArray-tucg      7     30     10 0.27     133    4,686
  std-copy3-tucg        13    109     39 1.86     76    2,806   std-palindrome-tucg      5     14      –  TO      64     1,717
  std-copy4-tucg        18    217      – TO       85    3,416   std-part-orig-tucg      10     83     11 11.59    138    5,035
  std-copy5-tucg        19    233     76 5.47     90    3,642   std-part-tucg           13     103    41   1.7    132    4,746
  std-copy6-tucg        22    301      – TO       97    3,991   std-sort-N-nd-assert-L  12     100    15 5.02      5      17
  std-copy7-tucg        25    357      – TO      101    4,321   std-vararg-tucg-tt       9     40     10 0.23     133    4,622
  std-copy8-tucg        27    430 105 8.05       106    4,581   std-vector-diff-tucg    12     112    14 2.94     76     2,964


     Classical predicate abstraction [17,3] has been adapted to quantified invariants by
extending predicates with skolem (fresh) variables [14,26]. This is sufficient for dis-
covering complex loop invariants of array manipulating programs similar to the ones
used in our experiments. These techniques require a decision procedure for satisfiabil-
ity of universally quantified formulas, and, significantly complicate predicate discov-
ery (e.g., [27]). Q UIC 3 extends this work to the IC3 framework in which the predicate
discovery is automated and quantifier instantiation and instance discovery are carefully
managed throughout the procedure.
     Recent work [7,29,20] studies this problem via the perspective of discovering uni-
versally quantified models for CHCs. These works show that fixing the number of ex-
pected quantifiers in an invariant is sufficient to approximate quantified invariants by
discovering a quantifier free invariant of a more complex system. The complexity comes
in a form of transforming linear CHC to non-linear CHC (linear refers to the shape of
CHC, not the theory of constraints). Unlike predicate abstraction, guessing the predi-
cates apriori is not required. However, both the quantifiers and their instantiations are
guessed eagerly based on the syntax of the input problem. In contrast, Q UIC 3 works
directly on linear CHC (i.e., a transition system), and discovers quantifiers and instan-
tiations on demand. Hence, Q UIC 3 is not limited to a fixed number of quantifiers, and,
unlike these techniques, is guaranteed to find the shortest counterexample.
     Model-Checking Modulo Theories (MCMT) [16] extends model checking to array
manipulating programs and has been used for verifying heap manipulating programs
and parameterized systems (e.g., [11]). It uses a combination of quantifier elimina-
tion (QELIM) for computing predecessors of Bad , satisfiability checking of univer-
sally quantified formulas for pruning exploration (and convergence check), and custom
generalization heuristics. In comparison, Q UIC 3 uses MBP instead of QELIM and uses
generalizations based on bounded exploration.
     S AFARI [1] (and later B OOSTER [2]), that extend MCMT with Lazy Abstraction
With Interpolation (LAWI) [28], is closest to Q UIC 3. As in LAWI, interpolation (in
case of S AFARI, for the theory of arrays [10]) is used to construct a quantifier-free
proof π of bounded safety. The proof π is generalized by universally quantifying out
some terms, and a decision procedure for universally quantified formulas is used to de-
termine convergence. The key differences between S AFARI and Q UIC 3 are the same
as between L AWI and IC3. We refer the reader to [30] for an in-depth comparison.
Specifically, Quic3_MakeSafe computes an interpolation sequence that can be used
for S AFARI. However, unlike S AFARI, Q UIC 3 does not rely on an external array in-
terpolation procedure. Moreover, in Q UIC 3, the generalizations are dynamic and the
quantifiers are introduced as early as possible, potentially exponentially simplifying the
bounded proof. Finally, Q UIC 3 manages its quantifier instantiations to avoid relying on
an external (semi) decision procedure. The acceleration techniques used in B OOSTER
are orthogonal to Q UIC 3 and can be combined in a form of pre-processing.
    To our knowledge, UPDR [23] is the only other extension of IC3 to quantified
invariants. The key difference is that UPDR focuses on programs specified using the
Effectively PRopositional (EPR) fragment of uninterpreted first order logic (e.g., with-
out arithmetic) for which quantified satisfiability is decidable. As such, UPDR does
not deal with quantifier instantiation and its mechanism for discovering quantifiers is
different. UPDR is also limited to abstract counterexamples (i.e., counterexamples to
existence of universal inductive invariants, as opposed to counterexamples to safety).
    Interestingly, Q UIC 3 is closely related to algorithms for quantified satisfiability
(e.g., [9,15,6]). Q UIC 3 uses a MBP to construct a complete instantiation, if possible.
However, unlike [9,15], the convergence (of Quic3_MakeSafe) does not rely on any
syntactic feature of the quantified formula.


8 Conclusion

In this paper, we present Q UIC 3, an extension of IC3 to reasoning about array manip-
ulating programs by discovering quantified inductive invariants. While our extension
keeps the basic structure of the IC3 framework, it significantly affects how lemmas and
proof obligations are managed and generalized. In particular, guaranteeing progress in
the presence of quantifiers requires careful management of the necessary instantiations.
Furthermore, discovering quantified lemmas, requires new lemma generalization tech-
niques that are able to infer universally quantified facts based on several examples. Un-
like previous works, our generalizations and instantiations are done on demand guided
by the property and current proof obligations. We have implemented Q UIC 3 in the CHC
engine of Z3 and show that it is competitive for reasoning about C programs.


Acknowledgements. This publication is part of a project that has received funding
from the European Research Council (ERC) under the European Union’s Horizon 2020
research and innovation programme (grant agreement No [759102-SVIS]). The re-
search was partially supported by Len Blavatnik and the Blavatnik Family founda-
tion, the Blavatnik Interdisciplinary Cyber Research Center, Tel Aviv University, and
the United States-Israel Binational Science Foundation (BSF) grants No. 2016260 and
2012259. We acknowledge the support of the Natural Sciences and Engineering Re-
search Council of Canada (NSERC), RGPAS-2017-507912.
References
 1. F. Alberti, R. Bruttomesso, S. Ghilardi, S. Ranise, and N. Sharygina. SAFARI: SMT-based
    abstraction for arrays with interpolants. In CAV, 2012.
 2. F. Alberti, S. Ghilardi, and N. Sharygina. Booster: An acceleration-based verification frame-
    work for array programs. In ATVA, 2014.
 3. T. Ball, A. Podelski, and S. K. Rajamani. Boolean and cartesian abstraction for model check-
    ing C programs. In TACAS, 2001.
 4. D. Beyer. Software verification with validation of results - (report on SV-COMP 2017). In
    TACAS, 2017.
 5. N. Bjørner and A. Gurfinkel. Property directed polyhedral abstraction. In VMCAI’15, 2015.
 6. N. Bjørner and M. Janota. Playing with quantified satisfaction. In LPAR, 2015.
 7. N. Bjørner, K. L. McMillan, and A. Rybalchenko. On solving universally quantified Horn
    clauses. In Static Analysis (SAS), 2013.
 8. A. R. Bradley. SAT-Based Model Checking without Unrolling. In VMCAI, 2011.
 9. A. R. Bradley, Z. Manna, and H. B. Sipma. What’s decidable about arrays? In Verification,
    Model Checking, and Abstract Interpretation (VMCAI), 2006.
10. R. Bruttomesso, S. Ghilardi, and S. Ranise. Quantifier-free interpolation of a theory of arrays.
    Logical Methods in Computer Science, 8(2), 2012.
11. S. Conchon, A. Goel, S. Krstic, A. Mebsout, and F. Zaïdi. Invariants for finite instances and
    beyond. In FMCAD, 2013.
12. L. M. de Moura and N. Bjørner. Z3: an efficient SMT solver. In TACAS, 2008.
13. I. Dillig, T. Dillig, and A. Aiken. Fluid updates: Beyond strong vs. weak updates. In Euro-
    pean Symposium on Programming (ESOP), 2010.
14. C. Flanagan and S. Qadeer. Predicate abstraction for software verification. In POPL, 2002.
15. Y. Ge and L. M. de Moura. Complete instantiation for quantified formulas in satisfiabiliby
    modulo theories. In Computer Aided Verification (CAV), 2009.
16. S. Ghilardi and S. Ranise. MCMT: A model checker modulo theories. In IJCAR’10, 2010.
17. S. Graf and H. Saïdi. Construction of abstract state graphs with PVS. In CAV’97, 1997.
18. A. Gurfinkel and A. Ivrii. Pushing to the top. In FMCAD, 2015.
19. A. Gurfinkel, T. Kahsai, A. Komuravelli, and J. A. Navas. The SeaHorn verification frame-
    work. In Computer Aided Verification (CAV), 2015.
20. A. Gurfinkel, S. Shoham, and Y. Meshman. SMT-based verification of parameterized sys-
    tems. In FSE, 2016.
21. K. Hoder and N. Bjørner. Generalized property directed reachability. In SAT’12, 2012.
22. K. Hoder, N. Bjørner, and L. M. de Moura. µZ- an efficient engine for fixed points with
    constraints. In Computer Aided Verification (CAV), 2011.
23. A. Karbyshev, N. Bjørner, S. Itzhaky, N. Rinetzky, and S. Shoham. Property-directed infer-
    ence of universal invariants or proving their absence. In CAV, 2015.
24. A. Komuravelli, N. Bjørner, A. Gurfinkel, and K. L. McMillan. Compositional verification
    of procedural programs using Horn clauses over integers and arrays. In FMCAD, 2015.
25. A. Komuravelli, A. Gurfinkel, and S. Chaki. SMT-Based Model Checking for Recursive
    Programs. In Computer Aided Verification (CAV), 2014.
26. S. K. Lahiri and R. E. Bryant. Constructing quantified invariants via predicate abstraction.
    In VMCAI, 2004.
27. S. K. Lahiri and R. E. Bryant. Indexed predicate discovery for unbounded system verifica-
    tion. In Computer Aided Verification (CAV), 2004.
28. K. L. McMillan. Lazy abstraction with interpolants. In CAV, 2006.
29. D. Monniaux and L. Gonnord. Cell morphing: From array programs to array-free Horn
    clauses. In Static Analysis (SAS), 2016.
30. Y. Vizel and A. Gurfinkel. Interpolating property directed reachability. In CAV’14, 2014.
