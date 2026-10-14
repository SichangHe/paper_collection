                                                           Precondition Inference via
                                                          Partitioning of Initial States

                                                       Bishoksan Kafle1 , Graeme Gange2 , Peter Schachte1 ,
                                                           Harald Søndergaard1 , and Peter J. Stuckey2
                                                                   1
                                                                       The University of Melbourne
arXiv:1811.06771v1 [cs.LO] 16 Nov 2018




                                                                         2
                                                                           Monash university



                                               Abstract. Precondition inference is a non-trivial task with several ap-
                                               plications in program analysis and verification. We present a novel itera-
                                               tive method for automatically deriving sufficient preconditions for safety
                                               and unsafety of programs which introduces a new dimension of modular-
                                               ity. Each iteration maintains over-approximations of the set of safe and
                                               unsafe initial states. Then we repeatedly use the current abstractions to
                                               partition the program’s initial states into those known to be safe, known
                                               to be unsafe and unknown, and construct a revised program focusing
                                               on those initial states that are not yet known to be safe or unsafe. An
                                               experimental evaluation of the method on a set of software verification
                                               benchmarks shows that it can solve problems which are not solvable
                                               using previous methods.


                                         1   Introduction
                                         Precondition analysis infers conditions (on the initial states of a program) that
                                         establish runtime properties of interest. For example, a sufficient precondition
                                         for safety is a set of initial states, each of which is guaranteed to be safe with
                                         respect to given safety properties (assertions). Preconditions have several im-
                                         portant applications and shed light on the following questions: (i) which inputs
                                         ensure safe program execution? (program analysis); (ii) which inputs can or can-
                                         not cause an error? (program debugging); (iii) what are the valid inputs for a
                                         program? (program understanding); and (iv) which library functions need to be
                                         modified to ensure valid outputs? (program specialisation).
                                             However, the problem is undecidable in general, hence approaches to finding
                                         preconditions use approximations. Preconditions derived by over-approximations
                                         are usually too weak, while under-approximations are usually too strong to be
                                         useful in practice. Unfortunately, for reasons of computability, we cannot hope to
                                         obtain an exact (optimal) precondition (though such preconditions enable their
                                         re-use, for example, under different calling contexts), so we must instead look for
                                         a (weaker) precondition that is useful. This work builds upon the transformation-
                                         guided framework of Kafle et al. [23]. Additionally, we model the set of safe
                                         terminating states so that we can iteratively refine the approximations of the set
                                         of safe states as well (as in [23]). We also partition initial states guided by the
                                         over-approximations of the safe and unsafe states to derive more precise sufficient
        int main(int a, int b) {       c1 . init(A, B).
          while (a ≥ 1) {              c2 . wh(A, B) ← init(A, B).
            a = a − 1; b = b − 1;      c3 . wh(A, B) ← A0 ≥ 1, A = A0 − 1,
          }                                             B = B0 − 1, wh(A0 , B0 ).
          assert (b ≥ 0);              c4 . unsafe ← A < 1, B < 0, wh(A, B).
        }                              c5 . safe ← A < 1, B ≥ 0, wh(A, B).


 Fig. 1: Running example: (left) original program, (right) translation to CHCs

preconditions, and in some cases precise necessary and sufficient preconditions
(optimal).
    We use constrained Horn clauses (CHCs) to encode the computation of C
programs. CHCs can conveniently be used to represent big- and small-step se-
mantics, transition systems, imperative programs and other models of compu-
tation. The use of CHCs allows decoupling programming language syntax and
semantics from the analysis. We use two special predicates, safe and unsafe re-
spectively to encode the set of safe and the set of unsafe (error) states. A safe
state is reached in all paths without error (return statements are encoded by safe
predicate). The predicate init encodes the set of initial states. We assume that
the users specify all the states of interest by an appropriate construct provided
by the language (for example, assert(c), return hni of the C language). States
not specified by the user (for example, buffer-overflow, floating point exceptions)
are not taken into account while generating CHCs. Hence the correctness of the
preconditions depends on the user specified set of states.
Running example. Before formally presenting our approach, we illustrate the
main steps via the example program in Figure 1. The left side shows a C program
fragment, and the right its CHC representation, encoding the reachable states
of the computation. Program variables in C are represented by logical variables
(Prolog style capital letters) in CHC. The clause c1 specifies the initial states
of the program via the predicate init which is always reachable. Similarly, the
clauses c2 and c3 encode the reachability of the while loop via the predicate
wh. c2 states that the loop is reachable if init is reachable while c3 states that
the loop is reachable if it is already in the loop and the loop guard is satisfied
(recursive case). The first three clauses on the right define the behaviour of the
program in Figure 1 (left) and the last two clauses represent the properties of
the program. The clause c4 states that an “unsafe” state is reached if B < 0
after exiting the loop whereas the clause c5 states that the program terminates
gracefully if B ≥ 0. Note that the semantics of assert(c) is if(c) SKIP else ERROR.
CHCs can be obtained from an imperative program using various approaches
[27,14,16,10]. Henceforth whenever we refer to a program, we refer to its CHC
representation.
    Observe that the assertion is violated if the initial conditions on a and b en-
tail (b < 0 ∧ a ≤ 0) ∨ (a ≥ 1 ∧ a > b), and the program terminates gracefully if
(b ≥ 0 ∧ a ≤ 0) ∨ (a ≥ 1 ∧ b ≥ a). Automatic derivation of these preconditions
is challenging for the following reasons: (i) the desired result is a disjunction of

                                         2
linear constraints—so we need a domain that can express disjunctions; (ii) infor-
mation has to be propagated forwards and backwards because we lose informa-
tion on b and a in the forward and in the backward direction respectively; (iii) we
need to reason simultaneously about the safe and unsafe states; one cannot sim-
ply be obtained by complementing the other. Existing methods [18,2,26,25,23]
cannot infer the desired preconditions.
    Let ϕN         N
          s and ϕu represent the over-approximations of safe and unsafe initial
states, that is, necessary preconditions (NPs) for safety and unsafety, respec-
tively. From the program in Figure 1, we get ϕN          N
                                                  s = ϕu = true (the set of initial
states). Thus the sufficient preconditions (SPs) for: (i) safety ϕSs = ϕN   s ∧ ¬ϕu
                                                                                    N
                    S      N      N
and (ii) unsafety ϕu = ϕu ∧ ¬ϕs are both false. These SPs, although valid, are
uninteresting. So, we transform the program with respect to the predicates safe
and unsafe using CHC transformations described in Section 3 (with the aim of
strengthening NPs) and derive ϕN   s ≡ (B ≥ 0 ∧ A ≤ 0) ∨ (A ≥ 1 ∧ B ≥ 0) ≡ B ≥ 0
and ϕN u ≡  (B < 0 ∧ A ≤  0) ∨ A ≥ 1 ≡ B ≤ 0 ∨ A ≥ 1 from the resulting programs.
The SPs from this iteration are ϕSs ≡ B ≥ 0 ∧ A ≤ 0 and ϕSu ≡ B < 0. These
NPs are more precise than the one obtained in the previous step. However fur-
ther refinement is possible since the NPs for safety and unsafety overlap, that
is, ϕN      N                                                          N
     s ∧ ϕu = B ≥ 0 ∧ A ≥ 1 is satisfiable. Since the formulae ϕs ∧ ¬ϕu and
                                                                                N
  N      N
ϕu ∧¬ϕs are already proven to be safe and unsafe initial states respectively, we
can focus our attention on ϕN      N
                              s ∧ϕu , which is yet to be classified as safe or unsafe.
To perform further classification, we constrain the initial states of the program in
Figure 1 to B ≥ 0 ∧ A ≥ 1 and restart the analysis by specialising the programs
with respect to safe and unsafe. As a result, we derive ϕN      s ≡ (B ≥ A ∧ A ≥ 1)
and ϕN u  ≡  (B ≥ 0 ∧ A >  B) as NPs.  Since ϕ N
                                               s  ∧ ϕ N
                                                      u  ≡  false, the preconditions
are optimal (they are both sufficient and necessary for the validity of assertions)
and the algorithm terminates. The final SPs are given (as the disjunction of SPs
over the iterations) as follows (after simplifications):

    ϕSs ≡ (B ≥ 0 ∧ A ≤ 0) ∨ (B ≥ A ∧ A ≥ 1).      ϕSu ≡ B < 0 ∨ (B ≥ 0 ∧ A > B).

The key contributions of the paper are as follows.

 – We extend the transformation-guided framework of Kafle et al. [23] which
   can now be used to derive SPs not only for safety but also for unsafety using
   over-approximation techniques. This is enabled by the encoding of the safe
   set of states together with the unsafe set of states and their simultaneous
   over-approximations. It also allows detecting optimality as well as controlling
   precision of the derived preconditions. In addition, it allows us to derive
   precondition for non-termination.
 – We partition the initial states of the program (guided by over-approximations)
   into those known to be safe, known to be unsafe, and whose safety are un-
   known. This enables us to reason incrementally on the new partition that is
   yet to be proven safe or unsafe. The precondition for the original program
   can then be derived by composing preconditions of each partitions.

                                          3
Paper outline. After preliminaries in Section 2, we describe preconditions, CHC
transformations and their relationships in Section 3. Section 4 presents our al-
gorithm for precondition inference, and Section 5 is an account of experimental
evaluation. Section 6 places the work in context and Section 7 concludes.


2    Preliminaries
An atomic formula (simply atom), is a formula p(x) where p is a predicate symbol
and x a tuple of arguments. A constrained Horn clause (CHC) is a first-order
formula written as p0 (x0 ) ← ϕ, p1 (x1 ), . . . , pk (xk ) following Constraint Logic
Programming (CLP) standard, where ϕ is a finite conjunction of quantifier-free
constraints on variables xi with respect to some constraint theory T, pi (xi ) are
atoms and p0 (x0 ) and ϕ, p1 (x1 ), . . . , pk (xk ) are respectively called the head and
the body of the clause.
    In textual form, we use Prolog-like syntax and typewriter font, with capital
letters for variable names and linear arithmetic constraints. A constrained fact is
a clause of the form p0 (x0 ) ← ϕ, where ϕ ∈ T. A clause of the form unsafe ← . . .
is called an integrity constraint where the predicate unsafe is always interpreted
as false. A set of CHCs is usually called a program.

CHC semantics. The semantics of CHCs is derived from the semantics of predi-
cate logic. An interpretation assigns to each predicate a relation over the domain
of the constraint theory T. An interpretation that satisfies each clause in the set
is called a model of a set of CHCs. Note that the set of CHCs without any
integrity constraint always has a model (an interpretation that assigns true to
each atom on the head of a clause). When modelling safety properties of systems
using CHCs, we also refer to CHCs as being safe or unsafe when they have a
model, or do not have a model, respectively. We assume that the theory T is
equipped with a decision procedure and a projection operator, and that it is
closed under negation. We use notation ϕ|V to represent the constraint formula
ϕ projected onto variables V .
Definition 1 (AND-tree or derivation tree, adapted from [13]). An
AND-tree for a set of CHCs is a labelled tree whose nodes are labelled as follows.
1. each non-leaf node corresponds to a clause (with variables suitably renamed)
   of the form A ← ϕ, A1 , . . . , Ak and is labelled by an atom A, ϕ, and has
   children labelled by A1 , . . . , Ak ,
2. each leaf node corresponds to a clause of the form A ← ϕ (with variables
   suitably renamed) and is labelled by an atom A and ϕ, and
Given a derivation tree t, constr(t) represents the conjunction of its constraints.
The tree t is feasible if and only if constr(t) is satisfiable over T.

Definition 2 (Initial clauses and nodes). Let P be a set of CHCs, with a
distinguished predicate pI in P which we call the initial predicate. The con-
strained facts {(pI (x) ← θ) | (pI (x) ← θ) ∈ P and θ ∈ T} are called the initial


                                           4
clauses of P . Let t be an AND-tree for P . A node labelled by pI (x) ← θ is an
initial node of t. We extend the term “initial predicate” and use the symbol pI
to refer also to renamed versions of the initial predicate that arise during clause
transformations.


3    Preconditions and CHC transformations

We limit our attention to the sets of clauses for which every derivation tree for
safe and unsafe (whether feasible or infeasible) has at least one initial node.
Definition 3 (Transforming CHCs by replacing initial states). Let P
be a set of CHCs and ϕ be a constraint over T. Let P 0 be the set of clauses
obtained from P by replacing the initial clauses {(pI (x) ← θi ) | 1 ≤ i ≤ k} by
{(pI (x) ← ϕ)}. This operation is denoted by init replace(P, ϕ).

Definition 4 (NP and SP for safety). Let P be a set of CHCs and ϕ be a
constraint over T. Then

 – ϕ is an NP for safety of P (ϕN s (P )) if P `T safe entails init replace(P, ϕ) `T
   safe. In other words, ϕ (possibly true) is an over-approximation of the set of
   initial states of P that can reach safe.
 – ϕ is an SP for safety of P (ϕSs (P )) if init replace(P, ϕ) 6`T unsafe. In other
   words, ϕ (possibly false) represents an under-approximation of the set of
   initial states of P that cannot reach unsafe.

Thus an SP for safety is a constraint that is sufficient to block derivations of
unsafe (given that we assume clauses for which pI is essential for any derivation
of unsafe). However in practice, we would like to consider SP for safety as a
constraint that is sufficient to allow derivations of safe and block derivations
of unsafe. Analogously, we can define both NP (ϕN                      S
                                                     u (P )) and SP (ϕu (P )) for
unsafety. In the following, we show how an NP and an SP can be derived from
a set of clauses.

Lemma 1 (NP extracted from clauses). Let P be a setWof clauses encoding
reachable states of a program. Then the formula ϕN
                                                 s (P ) = {θ | (pI (x) ← θ) ∈
P } is an NP for safety.

Proof (sketch). Let P 0 = init replace(P, ϕN     s (P )). To show: P `T safe entails
P 0 `T safe.
Let P `T safe. Then there exists a derivation tree t rooted at safe such that
constr(t) is satisfiable in T. From our assumption, t uses some initial nodes at its
leaves. Since all constraints from initial nodes of P are in ϕN     s (P ) and are used
in constructing initial clauses of P 0 , t is a feasible derivation of P 0 as well. Then
we have P 0 `T safe.                                                                   t
                                                                                       u

An NP for unsafety can be obtained analogously. Given NPs, we can compute
sufficient preconditions for safety and unsafety as follows. ϕSs (P ) = ϕN
                                                                         s (P ) ∧


                                           5
¬ϕN                       S          N         N
   u (P ) and similarly ϕu (P ) = ϕu (P ) ∧ ¬ϕs (P ). A precondition is optimal
if ϕs (P ) ∧ ϕu (P ) is unsatisfiable. Then we have ϕSs (P ) = ϕN
    N         N
                                                                 s (P ), that is,
the necessary and the sufficient conditions are the same for the validity of the
assertion. Next, we show how a given set of SPs can be combined to derive a
new SPs for a program.

Proposition 1 (Composing Preconditions). Let ϕ1 , ϕ2 , . . . be a (possibly
infinite) set of formulas
                   W      such that each ϕi is an SP for (un)safety of P . Then
their disjunction i ϕi is also an SP for (un)safety of P .

Proof (sketch). Consider the case for safety, that is, each ϕi (i = 1, 2, . . .) is an
SP for safety of P . Let Pi0 = init replace(P, ϕi ). For each ϕi , we have Pi0 6`T W
                                                                                   unsafe.
That is, unsafe is not derivable from any of Pi0 . Let P 0 = init replace(P, i ϕi ).
The initial clauses of P 0 are the union of all the initial clauses of each Pi0 while
the rest of the clauses are the same. From our assumption, any derivation of
unsafe need to use at least one of the initial clauses, our hypothesis under this
condition ensures that such a derivation either does not exist or is infeasible.
Then obviously, unsafe is not derivable from P 0 . The proof for unsafety can be
done analogously.                                                                       t
                                                                                        u

Next, we present a special kind of under-approximation of CHCs by restricting
their initial states which is useful in partitioning the set of CHCs. We say a set
of CHCs P 0 is an under-approximation of P if for an atom A, we have P 0 `T A
entails P `T A (the reverse is not necessarily true).
Definition 5 (Under-approximating CHCs by restricting initial states).
Let P be a set of CHCs and ϕ be a constraint over T. Let P 0 be the set of clauses
obtained from P by replacing the initial clauses {(pI (x) ← θi ) | 1 ≤ i ≤ k} by
{(pI (x) ← θi ∧ϕ) | 1 ≤ i ≤ k}. This operation is denoted by u approximate(P, ϕ).

Proposition 2. Let P be a set of CHCs, ϕ be any constraint over T and P 0 =
u approximate(P, ϕ). Then P 0 is an under-approximation of P .

Proof (sketch). This is obvious since P 0 is initial clauses restricted version of
P.                                                                              t
                                                                                u

    Note that u approximate(P, ϕ) only restricts the initial clauses of P while
keeping others intact. Then Definition 4 implies that an SP of u approximate(P, ϕ)
is also an SP of P . Formally,
Proposition 3. Let P be a set of CHCs, ϕ be any constraint over T and P 0 =
u approximate(P, ϕ). Let ψ be an SP for (un)safety of P 0 then ψ is also a SP for
(un)safety of P .

Proof (sketch). Consider the case for safety. Let ψ be an SP for safety of P 0 .
Since P and P 0 differ only in the set of initial clauses, both the constructions
init replace(P, ϕ) and init replace(P 0 , ϕ) yield the same set of clauses. So ψ is
an SP for safety of P as well. The proof for the case of unsafety can be done
analogously.                                                                     t
                                                                                 u


                                            6
 unsafe ← B < 0, A ≤ 0, wh 2(A, B).             safe ← B ≥ 0, A ≤ 0, wh 2(A, B).
 wh 2(A, B) ← B < 0, A ≤ 0, init 2(A, B).       wh 2(A, B) ← B ≥ 0, A ≤ 0, init 2(A, B).
 wh 2(A, B) ← B < 0, A = 0, C = 1,              wh 2(A, B) ← B ≥ 0, A = 0, C = 1,
               B − D = −1, wh 1(C, D).                        B − D = −1, wh 1(C, D).
 wh 1(A, B) ← A ≥ 1, init 1(A, B).              wh 1(A, B) ← A ≥ 1, B ≥ 0, init 1(A, B).
 wh 1(A, B) ← A ≥ 1, A − C = −1,                wh 1(A, B) ← B ≥ 0, A ≥ 1, A − C = −1,
               B − D = −1, wh 1(C, D).                        B − D = −1, wh 1(C, D).
 init 1(A, B) ← A ≥ 1.                          init 1(A, B) ← A ≥ 1, B ≥ 0.
 init 2(A, B) ← A ≤ 0, B ≥ 0.                   init 2(A, B) ← B ≥ 0, A ≤ 0.

 Fig. 2: Partially evaluated programs: wrt unsafe (left) and wrt safe (right).

We now present some CHC transformations, taken from the literature on CLP
and Horn clause verification. These are well known transformations and we refer
to [23] for details.


Partial Evaluation (PE). Partial evaluation [20] with respect to a goal spe-
cialises a program for the given goal; preserving only those derivations that are
relevant for deriving the goal. PE algorithm we apply here [12,23] produces a
polyvariant specialisation, that is, a finite number of versions of each predicate,
which is essential for deriving disjunctive information.
    The result of applying PE to the example program in Figure 1 with respect
to unsafe and safe is shown in Figure 2. The algorithm is a bit involved, so we
do not provide details here and ask the readers to refer to [23]. However a key
point to note is that due to polyvariant specialisation the predicates init and
wh are split, leading to a more precise approximations as shown below. But all
the feasible derivations of safe and unsafe are preserved. We derive the following
NPs from these programs:

    ϕN
     s ≡ (B ≥ 0 ∧ A ≤ 0) ∨ (A ≥ 1 ∧ B ≥ 0) ≡ B ≥ 0.
    ϕN
     u ≡ (B < 0 ∧ A ≤ 0) ∨ A ≥ 1 ≡ B < 0 ∨ A ≥ 1.



Constraint Specialisation (CS) [21]. CS strengthens constraints in the
clauses, while preserving derivations of a given atom (goal). The transforma-
tion prunes those paths that are not relevant for deriving the given atom. Next
we explain the transformation with an example.
    Figure 3 (left) shows an example program and Figure 3 (right) its constraint
specialised version preserving the derivation of unsafe. The strengthened con-
straints are obtained by recursively propagating B ≥ A top-down from the goal
unsafe and A = 1, B = 1 bottom-up from the constrained fact. An invariant
A ≥ B, B ≥ 0 for the recursive predicate p(A,B) in derivations of unsafe is com-
puted and conjoined to each call to p in the clauses (underlined in the clauses
in Figure 4 (right)).
    The result of applying CS to the program in Figure 2 (left) with respect
to unsafe and Figure 2 (right) with respect to safe is shown in Figure 4. Then
we derive the following NPs: ϕN                                              N
                                s ≡ (B ≥ 0 ∧ A ≤ 0) ∨ (A ≥ 1 ∧ B ≥ A) and ϕu ≡


                                            7
        unsafe ← B > A, p(A, B).         unsafe ← B > A, B ≥ 0, A ≥ B, p(A, B).
        p(A + B, B + 1) ← p(A, B).       p(A + B, B + 1) ← B ≥ 0, A ≥ B, p(A, B).
        p(A, B) ← A = 1, B = 0.          p(A, B) ← A = 1, B = 0, B ≥ 0, A ≥ B.

Fig. 3: Example program (left) and its constraint specialised version preserving
the derivation of unsafe (right).
(B < 0 ∧ A ≤ 0) ∨ (A ≥ 1 ∧ A > B). Since ϕN    N
                                          s ∧ ϕu is unsatisfiable, these precon-
ditions are optimal.

Trace Elimination (TE). TE is a program transformation that eliminates an
AND-tree of P from P while preserving the rest of its AND-trees. We illustrate
the transformation via the program in Figure 5. The program on the right is the
result of eliminating the AND-tree c1 − c3 from the program on the left. Note
that the elimination has caused splitting of the predicate p so that the same
AND-tree is no longer possible to construct while the rest of the AND-trees are
preserved. In summary, the method consists of representing the program and
the trace as finite tree automata, removing the trace using automata difference
construction and reconstructing a program from the result as detailed in [22].


                                                  unsafe ← B > A, p 1(A, B).
            c1 . unsafe ← B > A, p(A, B).
                                                  p 1(A + B, B + 1) ← p(A, B).
            c2 . p(A + B, B + 1) ← p(A, B).
                                                  p(A + B, B + 1) ← p(A, B).
            c3 . p(A, B) ← A = 1, B = 0.
                                                  p(A, B) ← A = 1, B = 0.

Fig. 5: A program (left) and its version after removing the trace c1 − c3 (right).

   TE is a useful transformation since it can act as a refinement or problem
decomposition as we shall see later. Furthermore, the splitting of the predicates
can help derive disjunctive information. While the elimination of infeasible trees
does not have any effect on preconditions, extra care must be taken while elimi-
nating feasible ones. Lemma 2 allows us to derive a safe precondition in this case.
To be consistent with the rest of the transformations, we can define TE which
takes a program P and an atom A and searches for a derivation of P rooted at
A and eliminates it if any.


 unsafe ← B ≤ 0, A < 0, wh 2(B, A).               safe ← B ≥ 0, A ≤ 0, wh 2(A, B).
 wh 2(A, B) ← B < 0, A ≤ 0, init 2(A, B).         wh 2(A, B) ← B ≥ 0, A ≤ 0, init 2(A, B).
 wh 2(A, B) ← B < 0, A = 0, C = 1,                wh 2(A, B) ← B ≥ 0, A = 0, C = 1,
              B − D = −1, wh 1(C, D).                          B − D = −1, wh 1(C, D).
 wh 1(A, B) ← A > B, A ≥ 1, init 1(A, B).         wh 1(A, B) ← A ≥ 1, B ≥ A, init 1(A, B).
 wh 1(A, B) ← A > B, A ≥ 1, A − C = −1,           wh 1(A, B) ← B ≥ 0, A ≥ 1, A − C = −1,
              B − D = −1, wh 1(C, D).                          B − D = −1, wh 1(C, D).
 init 1(A, B) ← A > B, A ≥ 1.                     init 1(A, B) ← A ≥ 1, B ≥ A.
 init 2(A, B) ← B < 0, A ≤ 0.                     init 2(A, B) ← B ≥ 0, A ≤ 0.

Fig. 4: Constraint specialised programs: wrt unsafe (left) and wrt safe (right)
                                              8
Definition 6 (θt ). Let P be a set of CHCs and t be a feasible AND-tree from
P for (un)safe. Let pI (x) be the atom label of an initial node of t then θt =
constr(t)|x .

In other words, θt is basically the result of eliminating all variables but x from
constr(t). Note that θt is necessary condition for t to be feasible.

Lemma 2 ([23]). Let P 0 be the result of eliminating a feasible AND-tree t for
                                                0                      0
safe (unsafe) from P . Then ϕN              N            N         N
                                 s (P ) = ϕs (P ) ∨ θt (ϕu (P ) = ϕu (P ) ∨ θt ),
where θt is a constraint extracted from t (Def. 6).

Transformations such as PE, CS and TE (which removes infeasible trees) not
only preserve the goal but also the initial clauses. This allows us to construct
a sequence of clauses P0 , P1 , . . . , Pm where P = P0 and each element of the
sequence is more specialised than its predecessor with respect to derivations of
safe (unsafe). As a consequence, the NPs are more precise. We write P =⇒A P 0
when P 0 is a goal-preserving transformation of P with respect to an atom A,
that is, P |= A iff P 0 |= A. TE (eliminating feasible trees) is a little different
which does not preserve the goal. We abuse the notation and write P =⇒tA P 0
for transformation of P by eliminating a feasible tree rooted at A, yielding P 0 .
Lemma 2 shows that soundness is ensured in this case.
    Let us now wrap these transformations and their combinations. Let tr and
tr-seq be any functions satisfying the following:
                         0
                         hP , ϕi where P =⇒A P 0
           trA hP, ϕi =     or
                         0 0
                          hP , ϕ i where P =⇒tA P 0 and ϕ0 = ϕ ∨ θtA (Def. 6)

    tr-seqA hP, ϕ, ni = trnA hP, ϕi for n ≥ 1

where f 1 = f and f n = f n−1 ◦ f .
    tr-seq allows us to combine the above transformations in any order and Propo-
sition 4 allows us to derive more precise preconditions from the combination.
Proposition 4 (Adapted from Proposition 2 of [23]). Let P be a set of
CHCs and n ≥ 1. Let hPs , ϕs i = tr-seqsafe hP, false, ni. Then |=T (ϕN   s (Ps )∨ϕs ) →
ϕN
 s  (P ). Similarly, if hP u , ϕu i = tr-seq unsafe hP, false, ni, then |=      N
                                                                           T (ϕu (Pu ) ∨
          N
ϕu ) → ϕu (P ).


4    An algorithm for precondition inference

Given a set of CHC transformations and their relationships with the precondi-
tions, we now state the algorithm for computing SPs for safety and unsafety in
Algorithm 1.
    The algorithm takes a set of CHCs as input (with special predicates encoding
the sets of safe and unsafe states) and a positive number n representing the length
of a sequence of transfomations and returns a pair of SPs for safety and unsafety.


                                           9
Algorithm 1 Algorithm for inferring sufficient preconditions
 1: Input: A set of CHCs P with clauses for safe and unsafeand the length of the
    sequence of transformations n.
 2: Output: Sufficient precondition for safety and unsafety wrt safe and unsafe.
 3: Initialisation: ϕS                     S
                           s ← false; ϕu ← false; Ps ← P ; Pu ← P ;
 4:                   ϕold ← ϕN     s (P ) (Definition 1);
 5: while true do
        hPs , θs i ← tr-seqsafe hPs , false, ni;        hPu , θu i ← tr-sequnsafe hPu , false, ni;
 6:
        ϕs ← ϕN   s (P s ) ∨   θs                       ϕu ← ϕN   u (Pu ) ∨ θu
 7:    ϕnew ← ϕs ∧ ϕu
 8:    if ϕnew ≡ false (optimal condition reached) then
 9:         ϕS        S
               s ← ϕs ∨ ϕs                ϕS      S
                                            u ← ϕu ∨ ϕu
10:        return hϕS            S
                           s , ϕu i
11:    else if ϕold → ϕnew (approximation does not get stronger) then
12:         ϕS        S
               s ← ϕs ∨ (ϕs ∧ ¬ϕu )                ϕS      S
                                                     u ← ϕu ∨ (ϕu ∧ ¬ϕs )
                           S     S
13:        return hϕs , ϕu i
14:    else (refine clauses via under-approximation using Def. 5)
15:        ϕold ← ϕnew
            ϕS        S
               s ← ϕs ∨ (ϕs ∧ ¬ϕu );                      ϕS        S
                                                           u ← ϕu ∨ (ϕu ∧ ¬ϕs );
16:
            Ps ← u approximate(Ps , ϕnew )                Pu ← u approximate(Pu , ϕnew )



The SPs ϕSs and ϕSu are initialised to false. The algorithm aims to weaken these
SPs as much as possible. ϕold keeps track of the set of initial states that are
yet to be proven safe or unsafe and is initialised to the set of initial states of
P . Ps and Pu keep track of the transformations of P with respect to safe and
unsafe respectively, and also their under-approximations.



       SafeI          UnsafeI          SafeI          UnsafeI          SafeI           UnsafeI




       Safe           Unsafe           Safe           Unsafe            Safe           Unsafe




Fig. 6: Precondition inference: Reality (left), Initial approximations (middle),
One step refinement of approximations using Algorithm 1 (right). We discard
the regions classified as definitely safe or unsafe considering only the intersection.

    The progress of Algorithm 1 is depicted in Figure 6. The leftmost panel
reflects the reality, that is, it depicts the set of concrete safe and unsafe states
along with the set of initial states leading to them. The set of safe states and
the set of initial states leading to them are respectively marked as Safe and
SafeI and are drawn on the left side of each panel. Similarly, the set of unsafe


                                               10
states and the set of initial states leading to them are respectively marked as
Unsafe and UnsafeI and are shown on the right side of each panel. Given a
program together with the description of the sets of interest (safe and unsafe
states), the precondition analysis infers a set of initial states that leads to these
sets of interest. Due to approximations, it discovers over-approximations of the
initial sets of states. These over-approximations are depicted as ellipses in the
middle panel with the corresponding colours for safe and unsafe initial states.
These approximations may intersect. As a consequence, there are some witness
traces from the left ellipse to Unsafe (shown by dotted arrows) and vice versa.
The algorithm aims to reduce these ellipses progressively towards the optimal
condition, where the left ellipse leads to the set of safe states and the right one
to the set of unsafe states (that is, these ellipses do not overlap anymore). A
single step of refinement is illustrated in the rightmost panel.
    In the algorithm, the following operations are carried out in an iterative man-
ner and possibly in parallel (within the while loop). The instructions on two sides
of the boxes can be executed in parallel. One or more of the transformation of
Ps and Pu with respect to safe and unsafe respectively are carried out and the
NPs are extracted from the resulting programs (line 6 ). The algorithm termi-
nates and returns an SP if the conjunction of these NPs is unsatisfiable (line 10,
optimal ) or it is not stronger (in the sense of implication of formulas) than ϕold
(line 13 ). Otherwise, the algorithm iterates with the new under-approximations
obtained by restricting their initial states with the conjunction (line 16 ). Note
that the conjunction needs to be converted to DNF before applying Definition
5, which may blow up the number of resulting clauses (only the initial ones).
Simulating the algorithm on the example program. We denote the pro-
gram in Figure 1 by P . Initially, ϕold = true, the initial state of P . First, we
choose to apply PE to P with respect to safe and unsafe respectively (call it
the iteration 0 of the algorithm). The resulting set of CHCs are shown in Fig-
ure 2 along with the derived NPs. Since the conjunction of ϕN              N
                                                                  s and ϕu , that
is, B ≥ 0 ∧ A ≥ 1, is satisfiable, the preconditions are not optimal. But the con-
junction is stronger than ϕold (conjunction of previous approximations), so the
algorithm progresses to refinement (line 14-16 ). Before under-approximating the
programs, we update the SPs from this iteration as:

    ϕSs ≡ false ∨ (B ≥ 0 ∧ ¬(B < 0 ∨ A ≥ 1)) ≡ B ≥ 0 ∧ A ≤ 0.
    ϕSu ≡ false ∨ ((B < 0 ∨ A ≥ 1) ∧ ¬B ≥ 0) ≡ B < 0.

The results of under-approximating the programs in Figure 2 by B ≥ 0 ∧ A ≥ 1
following Definition 5 are trivial and are not shown here. In the next iteration
(iteration 1), we apply CS with respect to safe and unsafe respectively to
the under-approximations, obtaining the clauses shown in Figure 7. Then the
NPs are: ϕN                             N                            N
            s ≡ (B ≥ A ∧ A ≥ 1) and ϕu ≡ (B ≥ 0 ∧ A > B). Since ϕs ∧ ϕu ≡
                                                                            N

false, the preconditions are optimal and the algorithm terminates. The final
SPs are given as the disjunction of SPs over the iterations as follows: ϕSs ≡
(B ≥ 0 ∧ A ≤ 0) ∨ (B ≥ A ∧ A ≥ 1) and ϕSu ≡ B < 0 ∨ (B ≥ 0 ∧ A > B).

                                         11
unsafe ← A < 0, B = 0, wh 2(B, A).                safe ← A ≥ 0, B = 0, wh 2(B, A).
wh 2(A, B) ← B < 0, A = 0, C = 1,                 wh 2(A, B) ← B ≥ 0, A = 0, C = 1,
            B − D = −1, wh 1(C, D).                           B − D = −1, wh 1(C, D).
wh 1(A, B) ← A > B, B ≥ 0, A ≥ 1, init(A, B).     wh 1(A, B) ← B ≥ A, A ≥ 1, init(A, B).
wh 1(A, B) ← A > B, A ≥ 1, A − C = −1,            wh 1(A, B) ← B ≥ A, A − C = −1,
            B − D = −1, wh 1(C, D).                      A ≥ 1, B − D = −1, wh 1(C, D).
init(A, B) ← A > B, B ≥ 0.                        init(A, B) ← B ≥ A, A ≥ 1.

Fig. 7: Constraint specialised programs: wrt unsafe (left) and wrt safe (right)

    If instead we apply the sequence CS, P E to the original program, we get
ϕN                                          N
  s ≡ (B ≥ 0 ∧ A ≤ 0) ∨ (A ≥ 1 ∧ B ≥ A), ϕu ≡ (B < 0 ∧ A ≤ 0) ∨ (A ≥ 1 ∧ A > B)
as optimal preconditions. This suggests that a sequence of transformations can
potentially avoid the costly DNF conversion (needed during refinement) after
each transformation. Therefore, in our experiments, we apply the sequence of
transformations PE followed by CS followed by TE, rather than a single one.
The rationale behind this particular sequences is that CS is most effective when
performed after PE, which propagates constraints and introduces new versions
of predicates. Trace elimination helps decompose the problem as well as splitting
predicates, which induces a split in the resulting programs.
    In each iteration of the loop, the algorithm either explores a strictly smaller
set of initial states that have not yet been classified as safe or unsafe or, termi-
nates. This property is formalised in Proposition 5.

Proposition 5 (Progress and Termination of Algorithm 1). At each it-
eration of the while loop, Algorithm 1 either progresses (considers a smaller set
of states that is yet to be proven safe or unsafe) or terminates.

Proof (sketch). At each iteration, the algorithm maintains a constraint formula
(representing the initial set of states that is yet to be classified as safe or unsafe).
The algorithm can exit if the formula in the current iteration is the formula false
(line 8-10 ), or is equivalent to the formula in the previous iteration (line 11-13 ).
In other case, the current formula is stronger (representing a smaller set of initial
states, treating constraint formula as a set) than that in the previous iteration,
so it recurses (line 14-16 ). This means the set that is yet to be proven safe or
unsafe gets smaller. In this sense, the algorithm makes progress.

    Proposition 4 establishes the correctness of the combination of transforma-
tions, Proposition 3 ensures that the precondition of an under-approximation of
CHCs is also that of the original and Proposition 1 allows us to combine pre-
conditions derived in each iterations.All these propositions together ensure the
soundness of Algorithm 1, which is formally stated as follows.

Theorem 1 (Soundness of Algorithm 1). Let P be a set of CHCs anno-
tated with the predicates safe (indicating a set of safe terminating states) and
unsafe (indicating a set of unsafe states). If Algorithm 1 returns a tuple hS, U i,
then S and U are the SPs for safety and unsafety of P , respectively, with respect
to the predicates safe and unsafe.

                                           12
Proof (sketch). In each iteration the algorithm essentially computes over ap-
proximations of the set of safe and unsafe states using the sequence of trans-
formations. Proposition 4 establishes the correctness of the sequence. Then it
computes the under-approximations of the original program with the sets of
states that are yet to be classified as safe or unsafe while accumulating those
states (preconditions) that are known to be safe and known to be unsafe. The
under-approximations are fed to the next iteration. Proposition 3 ensures that
the precondition of an under-approximation of CHCs is also that of the origi-
nal. Proposition 1 ensures that the preconditions accumulated (disjunctively) in
each iteration are the preconditions for the original program. These arguments
together ensures the soundness of the algorithm.                               t
                                                                               u

Limitations of our method and non-termination. The SPs derived by our method
may include non-terminating inputs, that neither lead to safe nor unsafe. Popeea
and Chin [28] treat such inputs as unsafe whereas Seghir and Schrammel [30]
ignore them, as do we. However, the modelling of safe and unsafe terminating
states and their over-approximations allow us to reason about a limited form of
non-termination as suggested by Popeea and Chin [28]. That is, any input state
that is neither in the over-approximation of safe nor unsafe is non-terminating
(again assuming that we model all the terminating safe and unsafe states).
    We illustrate this with the example in Figure
8. This program does not terminate if a ∈ [0, 10].     void main(int a) {
We derive ϕN    =   a ≥ 11 and ϕ N
                                   =  a <  0 as NPs.     while (a ≥ 0) {
             s                   u
Thus the condition satisfying ¬(ϕN    ∨ϕ N
                                           ), that is,     if (a ≤ 9) a++;
                                    s    u
¬(a ≥ 11 ∨ a < 0) ≡ a ∈ [0, 10] is a precondition          else if (a == 10)
                                                             a = 5;
for non-termination (which happens to be precise
                                                           else return;
in this case). It is obtained as our method’s side-      }
effect and we leave the primary analysis of non-         assert (false);
termination for future work.                           }

                                                       Fig. 8: Non-termination
5   Experimental evaluation

We implemented Algorithm 1 (a sequential version) in the tool PI-Horn (Pre-
condition Inferrer for Horn clauses), which is available from https://github.
com/bishoksan/PI-Horn. Given 3 different program transformations, the im-
plementation fixes the length of the sequence to 3. The order of their application
is PE followed by CS followed by TE. The tool is written in Ciao Prolog [17] and
makes use of the Parma Polyhedra Library (PPL) [1] and Yices2 SMT solver [11].
The input to our tool is a set of CHCs; with safe, unsafe and init as distinguished
predicates (for technical reasons). It outputs a pair of SPs for safety and un-
safety. The derived SPs are classified as: (i) optimal : the precondition is both
necessary and sufficient (exact); (ii) (un)safe-non-trivial : the SP for (un)safety
is different from false (but not optimal ) and (iii) (un)safe-trivial : the SP for
(un)safety is false.


                                        13
Benchmarks and experimental settings. We tested our approach with 261
integer programs (available from https://github.com/bishoksan/PI-Horn/
tree/master/benchmarks) collected from the following sources which we think
could be the good candidates. (i) 150 programs from the loop (69) and recursive
(81) categories of SV-COMP’18 [4]; (ii) 83 programs from the DAGGER [15]
and TRACER tools [19] and (iii) 28 programs from the literature on precon-
dition inference and backwards analysis [2,25,26,3,5]. Unfortunately, we could
not include all the benchmarks used by Kafle et al. [23] since some of their C
sources were not available, but only their CHCs representations modelling only
the unsafe terminating states. Benchmark set (i) is designed for software verifi-
cation competitions while (ii) and (iii) are designed to demonstrate the strength
of some specific tools and techniques. We adapt these programs written in C for
precondition inference in the following way. They are first translated to CHCs by
specialising an interpreter of C written in Prolog using the tool VeriMap [9]. The
specialisation approach was described by De Angelis et al. [10], and models only
the states leading to an “error” state by the predicate unsafe. The current trans-
lation also models return statements and the initial states of programs by two
special predicates safe and init respectively (again using VeriMap), which allows
us to reason about the safe terminating states and the initial states respectively.
Given a sequence of initial state variables x1 , . . . , xn and the corresponding initial
clause init(x1 , . . . , xn ) ← ϕ(x1 , . . . , xn ) obtained by the translation, we replace
ϕ(x1 , x2 , . . . , xn ) by true obtaining the clause init(x1 , x2 , . . . , xn ) ← true. The
replacement allows the analysis to infer preconditions in terms of these variables
starting from an unrestricted set of initial states.
     Unfortunately, we could not compare our tool against the recent works of
Seghir et al. [29,30] and that of Bakhirkin et al. [2], the first due to some issues
with the tool (discovered together with the authors), and the second due to the
lack of a tool automating their approach (confirmed by the authors via email).
But we do compare to the work of Kafle et al. [23] (represented in the table as
WP-Rahft). Although some of the components used in our tools are the same,
a direct comparison is difficult due to different outcomes. That tool, for example,
cannot detect optimality and does not attempt to do so, unlike ours. Therefore,
it is hard to compare the quality of the generated preconditions.
     Experiments have been carried on a MacBook Pro, running OS X 10.11 in
16GB Memory and 2.7 GHz Intel Core i5 processor.

Experimental Results. Table 1 presents the results. The columns respectively
show iter (# of refinement iterations (line 14-16 )), opt (# of programs with
optimal preconditions), ntS (Sw) (# of programs with non-trivial SPs for safety
excluding optimal cases, and, in parentheses, the difference with trivial SPs
for unsafety), ntU (Uw) (same, but for unsafety), ntSU (# of programs with
non-trivial SPs for both safety and unsafety), tSU (# of programs with trivial
SPs for both safety and unsafety), total/iter (# of programs with non-trivial
plus optimal SP per iteration), WP-Rahft total/iter (# of programs with non-
trivial SP per iteration for WP-Rahft). For example, the entry 9 (7) in column
3 indicates that there were 9 non-trivial SPs for safety, of which 7 had trivial SPs

                                             14
    iter opt ntS (Sw)     ntU (Uw)    ntSU        tSU      total/iter WP-Rahft
                                                                       total/iter
      0 58       0 (0)        0 (0)           0          0        58            197
      1 87       9 (7)        5 (3)           2         20        99              20
      2 21      20 (15)       7 (2)           5          0        43               0
      3 5        6 (3)        3 (0)           3          0        11               0
      4 2        3 (1)        2 (0)           2          0          5              0
      5 2        0 (0)        0 (0)           0          0          2              1
      6 1        0 (0)        0 (0)           0          0          1              0
 #total 176     38 (26)      17 (5)          12         20       219            218

Table 1: Experimental results on 261 programs, with a timeout of 300 seconds.
for unsafety. Each row contains the number of instances for which the algorithm
terminated after the given number of iterations.
    The results show our tool is able to generate non-trivial preconditions for
83% of the programs while timing out for 9%. The average time taken (ignoring
timeouts) per each instance is 5.94 seconds. Optimal preconditions are inferred
for 67% of the programs whereas for 8% the tool fails to infer any meaningful pre-
conditions. A meaningful SP for safety or unsafety (6= false) apart from optimal
ones is inferred for 16% of the problems (columns 3rd and 4th ). Preprocessing
using partial evaluation and constraint specialisation, as well as refinement by re-
moving program traces and restarting the analysis from unresolved initial states,
increases the precision of the analysis for the following reasons. On the one hand,
partial evaluation brings polyvariant specialisation by creating several versions
of the predicates, which the abstract interpreter in constraint specialisation can
take advantage of. On the other hand, the refinement helps limit the set of initial
states to explore and/or reduces the number of paths to explore. Note that the
tool infers optimal preconditions for 58 programs due to preprocessing alone,
which is indicated by the result along the row iteration 0 in the table, whereas
it infers optimal preconditions for 99 programs after the first refinement. How-
ever, it should be noted that the refinement also hinders the performance of the
analysis by increasing the size of the resulting programs. This explains why we
solve fewer and fewer problems after iteration 2. The number of programs with
non-trivial SPs are almost the same for both the tools (219 vs. 218), but they
differ in the quality (such as optimality) of the generated SPs. The refinement in
our approach allows us to derive optimal or non-trivial preconditions for more
programs, but in case of WP-Rahft it does not yield any better results after
the first refinement iteration (note though that the derived preconditions may be
more general). The average time taken (ignoring the timeouts ) by WP-Rahft
per each instance is 5.59 (first iteration) and 8.34 (sixth iteration) seconds. The
first one is bit lower and the second is bit higher than in our approach. The reason
for this difference is that WP-Rahft does not know when to stop refining since
the termination criterion, the maximum number of iterations, is rather weak.
Another possible reason is that at each iteration an under-approximation of the
original program is analysed by our tool as opposed to WP-Rahft, which can


                                        15
be easier. Though the refinement may help derive a weaker SP, it also consumes
more time.


6   Related work
Given a wide range of applications, there are a handful of techniques in the
literature dealing with precondition inference. We classify them as follows.
Abstract interpretation: Over-approximation techniques (forward and back-
wards abstract interpretations or their combination [6,7,3]) inherently derive
NPs and complementation allows deriving SPs at the cost of precision (due to
approximation of the complement). In order to minimise the loss, we need to
find either a (pseudo) complemented domain [24] or an alternative to comple-
mentation that is less aggressive. Along these lines, Howe et al. [18] utilise the
pseudo-complemented domain Pos to infer SPs whereas Bakhirkin et al. [2] ex-
change an abstract complement operation for abstract logical subtraction. In
contrast to these lines of work, we neither assume an abstract domain to be
complemented nor apply complementation of an abstract element during ab-
stract interpretation. Instead our method applies to any abstract domain, and
the complementation is carried out as a separate process outside the abstract
domain, storing the result as a formula without any loss of precision.
    Little work has been done that inherently computes SPs without comple-
mentation. The notable exception is the work of Miné [25], which designs all
required purpose-built backward transfer functions for intervals, octagons and
convex polyhedra domains. The downside is that the purpose-built operations,
including widening, can be rather intricate and require substantial implemen-
tation effort. Moy [26] employs weakest-precondition reasoning and forward ab-
stract interpretation to attempt to generalise conditions at loop heads to infer
SPs. The derived conditions offer limited use except for a theorem prover. As
opposed to these works, our method makes use of standard tools and techniques
offering simplicity and ease of implementation. Furthermore, our results can be
consumed by other tools in the area of program analysis and verification. Though
formulated in the context of software verification, the dual-analysis approach of
Poppea and Chin [28] uses over-approximations as in our approach to concur-
rently infer NPs for safety and unsafety of each method (and program), from
which SPs can be derived. However, in contrast to our approach, no refinement
of the derived preconditions takes place.
Program transformation: The forward and backward iterative specialisation
approach of De Angelis et al. [8] designed to verify program properties can be
used for deriving preconditions, as in our approach. The transformation approach
uses constraint generalisation method instead of abstract interpretation and can
be adjusted to refine preconditions.
Counterexample-guided abstraction refinement (CEGAR): Seghir et
al. [29,30] use a CEGAR approach to derive exact necessary and sufficient pre-
conditions for safety. Like us, they model safe and unsafe states of a program


                                       16
and refine their approximations until they are disjoint. Their algorithm may di-
verge due to (i) the lack of a suitable generalisation of the counterexamples (an
inherent limitation of CEGAR) and (ii) the termination condition (disjointness)
that is too hard to achieve for realistic programs (due to undecidability). We,
on the other hand, use abstract interpretation and program transformation, so
each step of the algorithm terminates and a sound precondition can be derived
from the resulting programs. In addition, optimality is not the end goal for us
and it is obtained as a by-product of precision refinement.
    The work of Kafle et al. [23] is orthogonal to all of the above; it combines
a range of established tools and techniques such as abstract interpretation, CE-
GAR and program transformations in a profitable way. The iterative nature of
their approach allows them to derive more precise preconditions for safety on
demand, however the termination criterion, the maximum number of iterations
supplied by the user, is rather weak. The quality of the preconditions such as
optimality cannot be checked using their approach. The current work offers sev-
eral advantages over that approach. We model both safe and unsafe states of
programs. This allows detecting optimality and also inferring NP and SP for
both safety and unsafety. In addition, it allows reasoning about a limited form
of non-termination and provides more refined termination criteria. Unlike many
methods in the literature [29,30,2], our method can handle not only programs
with procedures, but also recursive programs, in a uniform way.



7    Concluding remarks


We have presented an iterative method for automatically deriving sufficient pre-
conditions for safety and unsafety of programs. It maintains over-approximations
of the set of safe and unsafe initial states. At each iteration, only the set of states
that are common to these over-approximations are considered, as those are yet
to be classified as safe or unsafe. The method terminates when the common
set of states is empty or the common set does not get smaller in successive
iterations. Experimental results show that the method is able to generate op-
timal preconditions in 67% of the cases and also solves some problems which
are otherwise unsolvable using only approximations of the unsafe states (as was
done in previous work). Owing to over-approximation, the sufficient precondi-
tions may include some non-terminating states, which hinders the derivation of
optimal preconditions. In future work we intend to augment our method with
non-termination analysis.


Acknowledgement We thank John Gallagher for comments on an earlier draft
and many useful discussions which has led to many improvements. We thank
Emanuele de Angelis for C to CHC translation, help with the tool VeriMAP,
benchmarks and many stimulating discussions.

                                          17
References
 1. R. Bagnara, P. M. Hill, and E. Zaffanella. The Parma Polyhedra Library: Toward a
    complete set of numerical abstractions for the analysis and verification of hardware
    and software systems. Sci. Comput. Program., 72(1–2):3–21, 2008.
 2. A. Bakhirkin, J. Berdine, and N. Piterman. Backward analysis via over-
    approximate abstraction and under-approximate subtraction. In Static Analysis,
    volume 8723 of LNCS, pages 34–50. Springer, 2014.
 3. A. Bakhirkin and D. Monniaux. Combining forward and backward abstract inter-
    pretation of Horn clauses. In Static Analysis, volume 10422 of LNCS, pages 23–45.
    Springer, 2017.
 4. D. Beyer. Software verification with validation of results (report on SV-COMP
    2017). In Proc. TACAS 2017, volume 10206 of LNCS, pages 331–349, 2017.
 5. F. Cassez, P. G. Jensen, and K. G. Larsen. Refinement of trace abstraction for
    real-time programs. In Reachability Problems, volume 10506 of LNCS, pages 42–58.
    Springer, 2017.
 6. P. Cousot and R. Cousot. Abstract interpretation and application to logic pro-
    grams. J. Log. Program., 13(2&3):103–179, 1992.
 7. P. Cousot, R. Cousot, and F. Logozzo. Precondition inference from intermittent
    assertions and applications to contracts on collections. In VMCAI 2011, volume
    6538 of LNCS, pages 150–168. Springer, 2011.
 8. E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti. Program verification
    via iterated specialization. Sci. Comput. Program., 95:149–175, 2014.
 9. E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti. VeriMAP: A tool
    for verifying programs through transformations. In TACAS 2014, volume 8413 of
    LNCS, pages 568–574. Springer, 2014.
10. E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti. Semantics-based
    generation of verification conditions via program specialization. Sci. Comput. Pro-
    gram., 147:78–108, 2017.
11. B. Dutertre. Yices 2.2. In Proc. CAV 2014, volume 8559 of LNCS, pages 737–744.
    Springer, 2014.
12. J. P. Gallagher. Specialisation of logic programs: A tutorial. In PEPM 1993, pages
    88–98, 1993.
13. J. P. Gallagher and L. Lafave. Regular approximation of computation paths in
    logic and functional languages. In Partial Evaluation, volume 1110 of LNCS, pages
    115–136. Springer, 1996.
14. S. Grebenshchikov, N. P. Lopes, C. Popeea, and A. Rybalchenko. Synthesizing
    software verifiers from proof rules. In PLDI 2012, pages 405–416. ACM, 2012.
15. B. S. Gulavani, S. Chakraborty, A. V. Nori, and S. K. Rajamani. Automatically
    refining abstract interpretations. In TACAS 2008, volume 4963 of LNCS, pages
    443–458. Springer, 2008.
16. A. Gurfinkel, T. Kahsai, A. Komuravelli, and J. A. Navas. The SeaHorn verification
    framework. In CAV 2015, volume 9206 of LNCS, pages 343–361. Springer, 2015.
17. M. V. Hermenegildo, F. Bueno, M. Carro, et al. An overview of Ciao and its design
    philosophy. Theory and Practice of Logic Programming, 12(1-2):219–252, 2012.
18. J. M. Howe, A. King, and L. Lu. Analysing logic programs by reasoning backwards.
    In Program Development in Computational Logic, volume 3049 of LNCS, pages
    152–188. Springer, 2004.
19. J. Jaffar, V. Murali, J. A. Navas, and A. E. Santosa. TRACER: A symbolic
    execution tool for verification. In CAV 2012, volume 7358 of LNCS, pages 758–
    766. Springer, 2012.


                                          18
20. N. Jones, C. Gomard, and P. Sestoft. Partial Evaluation and Automatic Software
    Generation. Prentice Hall, 1993.
21. B. Kafle and J. P. Gallagher. Constraint specialisation in Horn clause verification.
    Sci. Comput. Program., 137:125–140, 2017.
22. B. Kafle and J. P. Gallagher. Horn clause verification with convex polyhedral
    abstraction and tree automata-based refinement. Computer Languages, Systems
    & Structures, 47:2–18, 2017.
23. B. Kafle, J. P. Gallagher, G. Gange, et al. An iterative approach to precondition
    inference using constrained Horn clauses. Theory and Practice of Logic Program-
    ming, 18:553–570, 2018.
24. K. Marriott and H. Søndergaard. Precise and efficient groundness analysis for logic
    programs. ACM LOPLAS, 2(1–4):181–196, 1993.
25. A. Miné.     Inferring sufficient conditions with backward polyhedral under-
    approximations. Electr. Notes Theor. Comput. Sci., 287:89–100, 2012.
26. Y. Moy. Sufficient preconditions for modular assertion checking. In VMCAI 2008,
    volume 4905 of LNCS, pages 188–202. Springer, 2008.
27. J. C. Peralta, J. P. Gallagher, and H. Sağlam. Analysis of imperative programs
    through analysis of constraint logic programs. In Static Analysis, volume 1503 of
    LNCS, pages 246–261, 1998.
28. C. Popeea and W. Chin. Dual analysis for proving safety and finding bugs. Sci.
    Comput. Program., 78(4):390–411, 2013.
29. M. N. Seghir and D. Kroening. Counterexample-guided precondition inference. In
    ESOP 2013, volume 7792 of LNCS, pages 451–471. Springer, 2013.
30. M. N. Seghir and P. Schrammel. Necessary and sufficient preconditions via eager
    abstraction. In APLAS 2014, volume 8858 of LNCS, pages 236–254. Springer,
    2014.




                                          19
