                                            Finite countermodels for safety verification of
                                                     parameterized tree systems

                                                                           Alexei Lisitsa

                                                                  Department of Computer Science
                                                                      University of Liverpool
arXiv:1107.5142v1 [cs.LO] 26 Jul 2011




                                                                   a.lisitsa@liverpool.ac.uk



                                              Abstract. In this paper we deal with verification of safety properties
                                              of parameterized systems with a tree topology. The verification problem
                                              is translated to a purely logical problem of finding a finite countermodel
                                              for a first-order formula, which further resolved by a generic finite model
                                              finding procedure. A finite countermodel method is shown is at least as
                                              powerful as regular tree model checking and as the methods based on
                                              monotonic abstraction and backwards symbolic reachability. The prac-
                                              tical efficiency of the method is illustrated on a set of examples taken
                                              from the literature.


                                        1    Finite Countermodel Method
                                        The development of general automated methods for the verification of infinite-
                                        state and parameterized systems poses a major challenge. In general, such prob-
                                        lems are undecidable, so one cannot hope for the ultimate solution and the
                                        development should focus on the restricted classes of systems and properties.
                                            In this paper we deal with a very general method for verification of safety
                                        properties of infinite-state systems which is based on a simple idea. If an evolu-
                                        tion of a computational system is faithfully modeled by a derivation in a classical
                                        first-order logic then safety verification (non-reachability of unsafe states) can
                                        be reduced to the disproving of a first-order formula. The latter task can be
                                        (partially, at least) tackled by generic automated procedures searching for finite
                                        countermodels.
                                            Such an approach to verification was originated in the research on formal ver-
                                        ification of security protocols ([23,22,9,11,10]) and later has been extended to the
                                        wider classes of infinite-state and parameterized verification tasks. Completeness
                                        of the approach for particular classes of systems (lossy channel systems) and rel-
                                        ative completeness with respect to general method of regular model checking has
                                        been established in [17] and [18] respectively. The method has also been applied
                                        to the verification of safety properties of general term rewriting systems and its
                                        relative completeness with respect to the tree completion techniques has been
                                        shown in [19].
                                            In this paper we continue investigation of applicability of the method and
                                        show its power in the context of verification of safety properties of parameter-
                                        ized tree-like systems. We show the relative completeness of FMC methods with
respect to regular tree model checking [3] and with respect to the methods based
on monotonic abstraction and symbolic backwards reachability analysis [5].


1.1   Preliminaries

 We assume that the reader is familiar with the basics of first-order logic. In par-
ticular, we use without definitions the following concepts: first-order predicate
logic, first-order models, interpretations of relational, functional and constant
symbols, satisfaction M |= ϕ of a formula ϕ in a model M , semantical con-
sequence ϕ |= ψ, deducibility (derivability) ⊢ in first-order logic. We denote
interpretations by square brackets, so, for example, [f ] denotes an interpretation
of a functional symbol f in a model. We also use the existence of complete finite
model finding procedures for the first-order predicate logic [7,20], which given
a first-order sentence ϕ eventually produce a finite model for ϕ if such a model
exists.


2     Regular Tree Model Checking

Regular Tree Model Checking (RTMC) is a general method for the verification
of parameterized systems that have tree topology [3,6]. The definitions of this
section are largely borrowed from [3].


2.1   Trees

A ranked alphabet is a pair (Σ, ρ), where Σ is a finite set of symbols and ρ :
Σ → N at is an arity mapping. Let Σp denote the set of symbols in Σ of arity
p. Intuitively, each node of a tree is a labeled with a symbol from Σ and the
out-degree of the node is the same as the arity of the symbol.

Definition 1. A tree T over a ranked alphabet (Σ, ρ) is a pair (S, λ), where

 – S, called tree structure, is a finite set of finite sequences over N at. Each
   sequence n in S is called a node of T . S is prefix-closed set, that is, if S con-
   tains a node n = b1 b2 . . . bk , then S also contains the node n′ = b1 b2 . . . bk−1
   and the nodes nr = b1 b2 . . . bk−1 r, for r : 0 ≤ r < bk . We say that n′ is a
   parent of n, and that n is a child of n′ . A leaf of T is a node n which does
   not have any child.
 – λ is a a mapping from S to Σ. the number of children of n is equal to ρ(λ(n)).
   In particular, if n is a leaf then λ(n) ∈ Σ0 .

    We use T (Σ) to denote the set of all trees over Σ. We write n ∈ T when
n ∈ S and f ∈ T denotes that λ(n) = f for some n ∈ T . For a tree T = (S, λ)
and a node n ∈ T , a subtree of T rooted at n is a tree T ′ = (S ′ , λn ), where
S ′ ⊆ {b | nb ∈ S} and λn (b) = λ(nb). Notice, that according to this definition a
subtree of a tree T consists not necessarily all descendants of some node in T.
    For a ranked alphabet Σ let Σ • (m) be the ranked alphabet which contains
all tuples (f1 , . . . , fm ) such that m ≥ 1 and f1 , . . . , fm ∈ Σp for some p. We put
ρ((f1 , . . . , fm )) = ρ(f1 ).
    For trees T1 = (S1 , λ1 ) and T2 = (S2 , λ2 ) we say that T1 and T2 are struc-
turally equivalent, if S1 = S2 .
    Let T1 = (S, λ1 ), . . . , Tm = (S, λm ) are structurally equivalent trees. Then
T1 × . . . × Tm denotes the tree T = (S, λ) where λ(n) = (λ1 (n), . . . , λm (n)).

2.2   Tree Automata and Transducers
A tree language is a set of trees.
Definition 2. A tree automaton over a ranked alphabet Σ is a triple A =
(Q, F, δ), where Q is a finite set of states, F ⊆ Q is a set of final states,
and δ is a transition relation, represented by a finite set of rules of the form
(q1 , . . . , qp ) →f q, where f ∈ Σp and q1 , . . . qp , q ∈ Q.
    A run r of A on a tree T = (S, λ) ∈ T (Σ) is a mapping from S to Q such that
for each node n ∈ T with children n1 , . . . , nk : (r(n1 , . . . , r(nk )) →λ(n) r(n)) ∈ δ.
    For a state q ∈ S we denote by T ⇒rA q that r ia run of A on T such that
r(ǫ) = q. We say that A accepts T if T ⇒rA q for some run r and some q ∈ F .
The language of trees accepted by an automaton A is defined as L(A) = {T |
T is accepted by A}. The tree language L is called regular iff there is a tree
automaton A such that L = L(A).
    A tree automaton over an alphabet Σ • (2) is called tree transducer.
    Let D be a tree transducer over an alphabet Σ • (2).
    An one-step transition relation RD ⊆ T (Σ) × T (Σ) is defined as RD =
{(T, T ′ ) | T × T ′ is accepted by D}. The reflexive and transitive closure of RD
                   ∗
is denoted by RD     .
    We use ◦ to denote the composition of two binary relations defined in the
standard way. Let Ri denote the ith power of R i.e. i compositions of R. Then
we have R∗ = ∪i≥0 Ri .
    For any L ⊆ T (Σ) and R ⊆ T (Σ) × T (Σ) we denote by L ⋆ R the set
{y | ∃x(x, y) ∈ L × T (Σ) ∩ R}.
    Regular Tree Model Checking deals with the following basic verification task.
Problem 1. Given two tree automata AI and AU over an alphabet Σ and a tree
transducer D over Σ • (2). Does (L(AI ) ⋆ RD
                                           ∗
                                             ) ∩ L(AU ) = ∅ hold?
    In verification scenario, trees over Σ denote states of the system to be verified,
tree automata AI and AU define the sets of trees representing initial, respectively,
unsafe states. Tree transducer D defines the transitions of the system. Under
such assumptions, the positive answer to an instance of Problem 1 means the
safety property is established, namely, none of the unsafe states is reachable
along the system transitions from any of the initial states.
    The verification in RTMC proceeds by producing a tree transducer T R ap-
                 ∗                         ∗
proximating RD     from above, that is RD    ⊆ L(T R), and showing the emptiness
of the set (L(AI ) ⋆ L(T R)) ∩ L(AU )
3     From RTMC to FMC
In this section we show that the generic regular tree model checking question
posed in Problem 1 can be reduced to a purely logical problem of finding a
finite countermodel for a first-order logic formula, which then can be resolved
by application of generic model finding procedure. We show also the relative
completeness of finite countermodel method with respect to RTMC.
    Assume we are given an instance of the basic verification problem (over rank-
ing alphabet Σ), that is

  – a tree automaton AI = (QI , FI , δI ) accepting a regular set of initial states;
  – a tree automaton AU = (QU , FU , δU ) accepting a regular set of unsafe states;
  – a tree transducer D = (QD , FD , δD ) representation one-step transition rela-
    tion RD .

   Now define a set formulae of first-order predicate logic as follows. The vo-
cabulary consists of

  – constants for all elements of QI ⊔ QU ⊔ QD ⊔ Σ0 ;
  – unary predicate symbols Init(1) , U nsaf e(1)
  – binary predicate symbols Init2 , U nsaf e2 , R;
  – a ternary predicate symbol T ;
  – a p-ary functional symbol fθ for every θ ∈ Σp

    Given any tree τ from T (Σ) define its term translation tτ by induction:

  – tτ = c for a tree τ with one node labeled by c ∈ Σ0 ;
  – tτ = fθ (tτ1 , . . . , tτp ) for a tree τ with the root labeled by θ ∈ Σp and children
    τ1 , . . . τp .

   Let Φ be the set of the following formulae, which are all assumed to be
universally closed:

 1. Init(2) (a, q) for every a ∈ Σ0 , q ∈ QI and →a q in δI ;
 2. Init(2) (x1 , q1 ) ∧ . . . ∧ Init(2) (xp , qp ) → Init(2) (fθ (x1 , . . . , xp ), q) for every
    (q1 , . . . , qp ) →θ q in δI ;
 3. ∨q∈FI Init(2) (x, q) → Init(1) (x);
 4. U nsaf e(2) (a, q) for every a ∈ Σ0 , q ∈ QU and →a q in δU ;
 5. U nsaf e(2) (x1 , q1 ) ∧ . . . ∧ U nsaf e(2)(xp , qp ) → U nsaf e(2) (fθ (x1 , . . . , xp ), q)
    for every (q1 , . . . , qp ) →θ q in δU ;
 6. ∨q∈FU U nsaf e(2) (x, q) → U nsaf e(1)(x);
 7. T (a, b, q) for every →(a,b) q in δD ;
 8. T (x1 , y1 , q1 ) ∧ . . . ∧ T (xp , yp , qp ) → T (fθ1 (x1 , . . . , xp ), fθ2 (y1 , . . . , yp ), q) for
    every (q1 , . . . , qp ) →θ1 ,θ2 q in δD ;
 9. ∨q∈FD T (x, y, q) → R(x, y);
10. R(x, x);
11. R(x, y) ∧ R(y, z) → R(x, z).
Proposition 1. (adequacy of Init and Unsafe translations)
  If τ ∈ L(AI ) then Φ ⊢ Init(1) (tτ )
  If τ ∈ L(AU ) then Φ ⊢ U nsaf e(1) (tτ )

Proof. We prove only the first statement, the second one is dealt with in the
same way.

Lemma 1. For any tree τ and any run r if τ ⇒rAI q then Φ ⊢ Init2 (tτ , q).

   Proof of Lemma. By induction on the depth of the trees.

 – Induction Base Case. Assume τ has a depth 0, that is consists of one vertex
   labeled by some a ∈ Σ0 . Let r be a run such that τ ⇒rAI q. It follows (by
   the definition of run) that →a q ∈ δI and then Init(2) (a, q) is in Φ (by clause
   1 of the definition of Φ) and therefore Φ ⊢ Init(2) (a, q) Finally notice that
   term translation tτ of τ is a.
 – Induction Step Case. Assume τ has a root labeled by θ ∈ Σp and τ1 , . . . , tp
   are children of the root. For a run r on τ , assume τ ⇒rAI q and τ1 ⇒rAI
   q1 , . . . , τp ⇒rAI qn . By the definition of a run we have (q1 , . . . , qp ) →θ q
   is in δI . By induction assumption we have Φ ⊢ Init(2) (tτ1 , q1 ), . . . , Φ ⊢
   Init(2) (tτp , qp ). By using clause 2 of the definition of Φ we get
   Φ ⊢ Init(2) (fθ (tτ1 , . . . , tτp ), q) and Φ ⊢ Init2 (tτ , q) ✷

   Returning to the proof of the proposition we notice that if τ ∈ L(AI )
then there is a run r such that τAr I q for some q ∈ FI . By Lemma 1 Φ ⊢
∨q∈FI Init(2) (tτ , q). By using clause 3 of the definition of Φ we then get Φ ⊢
Init(1) (tτ )

Proposition 2. (adequacy of encoding)
                   ∗
  If τ ∈ L(AI ) ⋆ RD then Φ ⊢ ∃x Init(1) (x) ∧ R(x, tτ )

Proof. Easy induction on the length of transition sequences.

 – Induction Base Case. Let τ ∈ L(AI ) ⊆ L(AI ) ⋆ RD        ∗
                                                              . Then Φ ⊢ Init(1) (tτ )
                                                       (1)
   (by Proposition 1) and, further Φ ⊢ ∃x Init (x) ∧ R(x, tτ ) (using clause
   10).
                                                 n+1
 – Induction Step Case. Let τ ∈ L(AI ) ⋆ RD          . Then there exists τ ′ such that
    ′                n          ′
   τ ∈ L(AI ) ⋆ RD and R(τ , τ ) holds. Further, by the argument analogous to
   the proof of Proposition 1, R(τ ′ , τ ) entails Φ ⊢ ∨q∈FD T (tτ ′ , tτ , q) and further
   Φ ⊢ R(tτ ′ , tτ ) (using clause 9). from this, the clause 11 and the induction
   assumption Φ ⊢ ∃x Init(1) (x) ∧ R(x, tτ ) follows.
                         ∗
   Assume τ ∈ L(AI ) ⋆ RD  then by definition of ⋆ there exists τ0 ∈ L(AI ) such
      ∗
that RD (τ0 , τ ) holds.

Corollary 1. (correctness of the verification method)
  If Φ 6⊢ ∃x∃y(Init(1) (x)∧R(x, y)∧U nsaf e(1) (y) then (L(AI )⋆RD
                                                                 ∗
                                                                   )∩L(AU ) = ∅
    The corollary 1 serves as a formal underpinning of the proposed FCM (finite
countermodel) verification method. In order to prove safety, that is (L(AI ) ⋆
RD∗
    ) ∩ L(AU ) = ∅ it is sufficient to demonstrate Φ 6⊢ ∃x∃y(Init(1) (x) ∧ R(x, y) ∧
U nsaf e(1) (y). In the FCM method we delegate this task to the generic finite
model finding procedure, which searches for the finite countermodels for
Φ → ∃x∃y(Init(1) (x) ∧ R(x, y) ∧ U nsaf e(1)(y).

3.1   Relative completeness of FCM with respect to RTMC
In general, searching for finite countermodels to disprove non-valid first-order
formulae may not always lead to success, because for some formulae counter-
models are inevitably infinite. Here we show, however, this is not the case for
the first-order encodings of the problems which can be positively answered by
Regular Tree Model Checking. It follows then that FCM is at least as powerful in
establishing safety as RTMC, provided a complete finite model finding procedure
is used.
Theorem 1. (relative completeness of FCM) Given an instance of the basic
verification problem for RTMC, that is two tree automata AI and AU over an
alphabet Σ and a tree transducer D = (QD , FD , δD ) over Σ • (2). If there exists
                                               ∗
a regular tree language R such that (L(AI ) ⋆ RD ) ⊆ R and R ∩ L(AU ) = ∅ then
there is a finite countermodel for Φ → ∃x∃y(Init(1) (x) ∧ R(x, y) ∧ U nsaf e(1) (y)
Proof. Let A = (Q, F, δ) be a deterministic tree automaton recognizing the tree
language R, i.e. L(A) = R. We take Q ∪ QI ∪ QU ∪ QD ∪ {e} to be domain of
the required finite model. Here e is a distinct element not in Q ∪ QI ∪ QU ∪ QD .
   Define interpretations as follows.
 – For a ∈ Σ0 [a] = q ∈ Q such that →a q is in δ;
 – For θ ∈ Σp [fθ ](q1 , . . . , qp ) = q for any (q1 , . . . , qp ) →θ q in δ, and [fθ ](. . .) =
   e otherwise;
 – Interpretations of Init2 and Init1 are defined inductively, as the least subsets
   of pairs, respectively, elements of the domain, satisfying the formulae (1) -
   (3) (and assuming all interpretations above);
 – Interpretations of U nsaf e2 and U nsaf e1 are defined inductively, as the least
   subsets of pairs, respectively, elements of the domain, satisfying the formulae
   (4) - (6) (and assuming all interpretations above);
 – Interpretation of T is defined inductively, as the least subsets of triples sat-
   isfying the formulae (7) - (8) (and assuming all interpretations above);
 – Interpretation of R and Init1 is defined inductively, as the least subsets of
   pairs, satisfying the formulae (9) - (11) (and assuming all interpretations
   above);

   Such defined a finite model satisfies Φ (by construction). Now we check that
¬∃x∃y(Init(1) (x) ∧ R(x, y) ∧ U nsaf e(1) (y) is satisfied in the model We have
 1. [Init(1) ] ⋆ [R] ⊆ {[t] | t ∈ L(AI ) ⋆ RD
                                            ∗
                                              } (by the minimality condition on
                             (1)
    interpretations of Init and R);
                           ast
 2. {[t] | t ∈ L(AI ) ⋆ RD     } ⊆ F ⊆ Q (by interpretations of terms and condition
                  ∗
    (L(AI ) ⋆ RD ) ⊆ R);
 3. [Init(1) ] ⋆ [R] ⊆ F (by 1 and 2);
 4. [U nsaf e(1) ] = {[t] | t ∈ L(AU )} (by definition of [U nsaf e1 ], in particular by
    the minimality condition);
 5. {[t] | t ∈ L(AU )} ∩ F = ∅ (by condition R ∩ L(AU ) = ∅);
 6. U nsaf e(1) ∩ F = ∅ (by 4 and 5);
 7. [Init(1) ] ⋆ [R] ∩ U nsaf e(1) = ∅ (by 3 and 6);


4    The case study

In this section we illustrate FCM method by applying it to the verification of
Two-way Token protocol. The system consists of finite-state processes connected
to form a binary tree structure. Each process stores a single bit which represents
the fact that the process has a token. During operation of the protocol the token
can be passed up or down the tree. The correctness condition is that no two or
more tokens ever appear. In parameterized verification we would like to establish
correctness for all possible sizes of trees.
    We take RTMC-style specification of Two-way Token from [3]. Let Σ =
{t, n, T, N } be the alphabet. Here t, n ∈ Σ0 label processes on the leaves of a
tree, and T, N ∈ Σ2 label processes on the inner nodes of a tree. Further, t, T
label processes with a token and n, N label processes without tokens.
    The automaton AI = (QI , FI , δI ) accepts the initial configurations of the
protocol, that is the trees with exactly one token. Here QI = {q0 , q1 }, FI = {q1 }
and δI consists of the following transition rules:

                              →n q0            →t q1 (q0 , q0 ) →T q1
                   (q0 , q0 ) →N q0 (q0 , q1 ) →N q1 (q1 , q0 ) →N q1

    The tree transducer D = (QD , FD , δD ) over Σ • (2) represents the transitions
of the protocol. Here QD = {q0 , q1 , q2 , q3 }, F = {q2 } and δD consists of the
following transition rules:

                                  →(n,n) q0              →(t,n) q1
                                    (n,t)
                                   →      q3 (q0 , q0 ) →(N,N ) q0
                                   (N,N )
                       (q0 , q2 ) →       q2 (q2 , q0 ) →(N,N ) q2
                       (q0 , q0 ) →(T,N ) q1 (q3 , q0 ) →(T,N ) q2
                       (q0 , q3 ) →(T,N ) q2 (q0 , q1 ) →(N,T ) q2
                       (q1 , q0 ) →(N,T ) q2 (q0 , q0 ) →(N,T ) q3

   The automaton AU = (QU , FU , δU ) accepts unsafe (bad) configurations of
the protocol, that is the trees with at least two tokens. Here QU = {q0 , q1 , q2 },
FU = {q2 } and δU consists of the following transition rules:
                             →n q0            →t q1 (q0 , q0 ) →N q0
                  (q0 , q0 ) → q1 (q0 , q1 ) →N q1 (q1 , q0 ) →N q1
                              T

                  (q0 , q1 ) →T q2 (q1 , q0 ) →T q2 (q1 , q1 ) →T q2
                  (q0 , q2 ) →T q2 (q2 , q0 ) →T q2 (q1 , q2 ) →T q2
                  (q2 , q1 ) →T q2 (q2 , q2 ) →T q2 (q1 , q1 ) →N q2
                  (q0 , q2 ) →N q2 (q2 , q0 ) →N q2 (q1 , q2 ) →N q2
                  (q2 , q1 ) →N q2 (q2 , q2 ) →N q2
    The set Φ of the following formulae presents a translation of the verification
problem. We use the syntax of first-order logic used in Mace4 finite model finder
[20].




T(n,n,q0).
T(t,n,q1).
T(n,t,q3).
T(x,z,q0) & T(y,v,q0) -> T(fT(x,y),fN(z,v),q1).
T(x,z,q1) & T(y,v,q0) -> T(fN(x,y),fT(z,v),q2).
T(x,z,q0) & T(y,v,q1) -> T(fN(x,y),fT(z,v),q2).
T(x,z,q0) & T(y,v,q0) -> T(fN(x,y),fN(z,v),q0).
T(x,z,q0) & T(y,v,q2) -> T(fN(x,y),fN(z,v),q2).
T(x,z,q2) & T(y,v,q0) -> T(fN(x,y),fN(z,v),q2).
T(x,z,q3) & T(y,v,q0) -> T(fT(x,y),fN(z,v),q2).
T(x,z,q0) & T(y,v,q3) -> T(fT(x,y),fN(z,v),q2).
T(x,z,q0) & T(y,v,q0) -> T(fN(x,y),fT(z,v),q3).

% Initial states automaton

Init(n,q0).
Init(t,q1).
Init(x,q0) & Init(y,q0) -> Init(fT(x,y),q1).
Init(x,q0) & Init(y,q1) -> Init(fN(x,y),q1).
Init(x,q0) & Init(y,q0) -> Init(fN(x,y),q0).
Init(x,q1) & Init(y,q0) -> Init(fN(x,y),q1).

% Bad states automaton

Bad(n,q0).
Bad(t,q1).
Bad(x,q0) & Bad(y,q0) -> Bad(fN(x,y),q0).
Bad(x,q0) & Bad(y,q0) -> Bad(fT(x,y),q1).
Bad(x,q0) & Bad(y,q1) -> Bad(fN(x,y),q1).
Bad(x,q1) & Bad(y,q0) -> Bad(fN(x,y),q0).

Bad(x,q0) & Bad(y,q1) -> Bad(fT(x,y),q2).
Bad(x,q1) & Bad(y,q0) -> Bad(fT(x,y),q2).
Bad(x,q1) & Bad(y,q1) -> Bad(fN(x,y),q2).
Bad(x,q1) & Bad(y,q2) -> Bad(fT(x,y),q2).
Bad(x,q2) & Bad(y,q1) -> Bad(fT(x,y),q2).
Bad(x,q2) & Bad(y,q2) -> Bad(fT(x,y),q2).
Bad(x,q1) & Bad(y,q1) -> Bad(fN(x,y),q2).
Bad(x,q0) & Bad(y,q2) -> Bad(fN(x,y),q2).
Bad(x,q2) & Bad(y,q0) -> Bad(fN(x,y),q2).
Bad(x,q1) & Bad(y,q2) -> Bad(fN(x,y),q2).
Bad(x,q2) & Bad(y,q1) -> Bad(fN(x,y),q2).
Bad(x,q2) & Bad(y,q2) -> Bad(fN(x,y),q2).

T(x,y,q2) -> R(x,y).
R(x,y) & R(y,z) -> R(x,z).

Init(x,q1) -> Init1(x).
Bad(x,q2) -> Bad1(x).




    According to Proposition 2 and Corollary 1 to establish safety for Two-way
Token protocol it does suffice to show Φ 6⊢ ∃x∃y((Init1(x) ∧ R(x, y)) ∧ Bad1(y)).
We delegate this task to Mace4 finite model finder and it finds a countermodel for
Φ → ∃x∃y((Init1(x) ∧ R(x, y)) ∧ Bad1(y)) in 0.03s. The parameterized protocol
is verified. Actual Mace4 input and output can be found in [14].


5     Monotonic abstraction and symbolic reachability vc
      FCM
Regular Tree Model Checking provides with a general method for the verifica-
tion parameterized protocols for tree-shaped architectures. In [5] a lightweight
alternative to RTMC was proposed. It utilizes a generic approach to safety ver-
ification using monotonic abstraction and symbolic reachability applied to tree
rewriting systems. This generic approach has previously been successfully ap-
plied to the verification of parameterized linear system [1] (as an alternative to
standard Regular Model Checking). In this section we demonstrate the flexibility
of the FCM approach and show that one can translate safety verification prob-
lems for parameterized tree-shaped systems formulated using tree rewriting into
the problem of disproving a first-order formulae using the same basic principles
(reachability as FO derivability). For defined translation we show the relative
completeness of the FCM with respect to monotonic abstraction and symbolic
reachability and demonstrate its practical efficiency.

5.1   Parameterized Tree Systems


   The approach of [5] to the verification of parameterized tree systems adopts
the following viewpoint. A configuration of the system is represented by a tree
over a finite alphabet, where elements of the alphabet represent the local states
of the individual processes. The behaviors of the system is specified by a set
of tree rewriting rules, which describe how the processes perform transitions.
Transitions are enabled by the local states of the process together with the
states of children and parent processes.

Definition 3. A tree T over a set of states Q is a pair (S, λ), where

 – S is a tree structure (cf. Definition 1)
 – λ is a a mapping from S to Q.

    Notice that trees over a set of states are similar to the trees over ranked
alphabets (Definition 1) with the only difference is that the same state can label
the vertices with different number of children (e.g. leaves of the tree and internal
vertices).
    In what follows to assume for simplicity of presentation (after [5]) that all
trees are (no more than) binary, that is every node has either one or two children
(internal node) or no children (leaf). It is straightforward to extend all construc-
tions and results to the general case of not necessarily binary trees. Notice that
configurations of the tree systems will be modeled by complete binary trees.
Incomplete binary trees (which may contain nodes with one child) will appear
only in the rewrite rules.

Definition 4. A parameterized tree system P is a tuple (Q, R), where Q is a
finite set of states and R ⊆ T (Q × Q) is a finite set of rewrite rules.

    For each rule r = (S, λ) ∈ R we associate two trees, called left and right trees
of r. We define lhs(r) = (S, lhs(λ)) and rhs(r) = (S, rhs(λ)), where lhs(r) and
rhs(r) are left, respectively right projection of λ.
    We will denote (labeled) binary trees by bracket expressions in a standard
way.

Example 1. Let Q = {q0 , q1 , q2 } then r = hq0 , q1 i(hq1 , q1 i, hq2 , q0 i) ∈ T (Q × Q) is
a rewriting rule. This rule has •(•, •) as it tree structure with one root and two
leaves. The pairs of states hq0 , q1 i, hq1 , q1 i, hq2 , q0 i label the root and two leaves
respectively. We also have lhs(r) = q0 (q1 , q2 ) and rhs(r) = q1 (q1 , q0 ).

Example 2. Let Q be as above then hq1 , q2 i(hq0 , q1 i) is a rewriting rule with the
structure of incomplete binary tree •(•)

    Given a parameterized tree system P = (Q, R) define one step transition
relation ⇒P ⊆ T (Q) × T (Q) as follows: τ1 ⇒P τ2 iff for some r ∈ R τ1 con-
tains lhs(r) as a subtree and τ2 obtained from τ1 by replacing this subtree with
rhs(r). Since lhs(r) and rhs(r) have the same tree structure, the operation of
replacement and one step transition relation are well-defined.

Example 3. Let P = (Q, R) with Q = {q0 , q1 , q2 } and R = {hq0 , q1 i(hq1 , q1 i, hq2 , q0 i)}.
Then we have (with the subtrees refered to in the definition of ⇒P inderlined):
 – q0 (q1 , q2 ) ⇒P q1 (q1 , q0 );
 – q2 (q0 (q1 , q2 ), q1 ) ⇒P q2 (q1 (q1 , q0 ), q1 );
 – q0 (q1 (q1 , q0 ), q2 (q0 , q2 )) ⇒P q1 (q1 (q1 , q0 ), q0 (q0 , q2 ));
Denote transitive and reflexive closure of ⇒P by ⇒∗P .
Definition 5. (embedding) For τ1 = (S1 , λ1 ) and τ2 = (S2 , λ2 ) an injective
function f : S1 → S2 is called embedding iff
 – s · b ∈ S implies f (s) · b ≤ f (s · b) for any s ∈ S
 – λ1 (s) = λ2 (f (s))
     We use τ1 f τ2 to denote that f is embedding of τ1 into τ2 and write τ1  τ2
iff there exists f such that τ1 f τ2 .
     Using embeddability relation ≺ allows to describe infinite families of trees by
finitary means.
     We call a set of trees T ⊆ T (Q) finitely based iff there is a finite set B ⊆ T (Q)
such that T = {τ | ∃τ ′ ∈ Bτ ′  τ }. Notice that finitely based set of trees are
upwards closed with respect to , that is τ ∈ T and τ  τ ′ implies τ ′ ∈ T .
     Many safety verification problems for parameterized tree system can be re-
duced to the following coverability problem.
Problem 2. Given a parameterized tree system P = (Q, R), a regulat tree lan-
guage Init ⊆ T (Q) of initial configurations and finitely based set of unsafe
configurations U nsaf e ⊆ T (Q). Does τ 6⇒∗P τ ′ hold for all τ ∈ Init and all
τ ′ ∈ U nsaf e?
Note 1. We formally defined regular tree languages over ranked alphabets. Reg-
ular tree languages over (unranked) states can be defined in a various ways. We
will fix a particular convention in Assumption 1 below.
    Now we briefly outline the monotonic abstraction approach [5] to verification.
Given the coverability problem above [5] defines the monotonic abstraction ⇒A   P
of the transition relation ⇒P as follows. We have τ1 ⇒A     P τ2 iff there exists
a tree τ ′ such that τ ′  τ1 and τ ′ ⇒P τ2 . It is clear that such defined ⇒A  P
is an over-approximation of ⇒P . To establish the safety property, i.e. to get
a positive answer to the question of Problem 2, [5] proposes using a symbolic
backward reachability algorithm for monotonic abstraction. Starting with an
upwards closed (wrt to ≺) set of unsafe configuration U nsaf e the algorithm
proceeds iteratively with the computation of the set of configurations backwards
reachable along ⇒A P from U nsaf e:
 – U0 = U nsaf e
 – Ui+1 = Ui ∪ P re(Ui )
    where P re(U ) = {τ | ∃τ ′ ∈ U ∧τ ⇒A     ′
                                          P τ }. Since the relation  is a well quasi-
ordering [13] this iterative process is guaranteed to stabilize, i.e. Un+1 = Un = U
for some finite n. During the computation each Ui is represented symbolically
by a finite set of generators. Once the process stabilized on some U the check is
preformed on whether Init∩U = ∅. If this condition is satisfied then the safety is
established, for no bad configuration can be reached from initial configurations
via ⇒ −P A and, a fortiori, via ⇒P .
5.2   Parameterized Tree systems to FCM
Here we show how to translate the coverability problem (Problem 2) into the task
of disproving a first-order formula and demonstrate the relative completeness of
the FCM method with respect to monotonic abstraction approach.
    Assume we are given an instance of the coverability problem, that is
 – a parameterized tree system P = (Q, R),
 – a regular tree language Init of initial configurations, given by a tree automa-
   ton AI = (QI , F, δ), and
 – finitely based set of unsafe configurations U nsaf e given by a finite set of
   generators U n ⊆ T (Q).
                                          (2)
For a set of states Q let FQ = {fq | q ∈ Q} ∪ {e} be the set of corresponding
binary functional symbols extended with a distinct functional symbol e of arity
0 (constant).
    For any complete binary tree τ ∈ T (Q) define its term translation tτ in
vocabulary FQ inductively:
 – tτ = fq (e, e) if τ is a tree with one node labeled by a state q;
 – tτ = fq (tτ1 , tτ2 ) if the root of τ has two children and τ = q(τ1 , τ2 );
For any not necessarily complete binary tree τ ∈ T (Q × Q) define inductively
its translation sτ as a set of pairs of terms in vocabulary FQ :
 – sτ = {hfq1 (e, e), fq2 (e, e)i} if τ is a tree with one node labeled with states
   (q1 , q2 );
 – sτ = {hfq1 (ρ1 , ρ2 ), fq2 (ρ3 , ρ4 )i | hρ1 , ρ3 i ∈ sτ1 , hρ2 , ρ4 i ∈ sτ2 } if the root
   of τ is labeled by (q1 , q2 ) and it has two children τ1 and τ2 , i.e. if τ =
   (q1 , q2 )(τ1 , τ2 );
 – sτ = {hfq1 (ρ1 , e), fq2 (ρ2 , e)i | hρ1 , ρ2 i ∈ sτ1 }∪{hfq1 (e, ρ1 ), fq2 (e, ρ2 )i | hρ1 , ρ2 i ∈
   sτ1 } if the root of τ is labeled by (q1 , q2 ) and it has one child τ1 , i.e. if
   τ = (q1 , q2 )(τ1 ).
For hρ1 , ρ2 i ∈ sτ we denote by ρgen
                                  1   (by ρgen
                                           2 ) a generalized term obtained by re-
placement of all occurences of constant e in ρ1 (in ρ2 , respectively,) with distinct
variables.
   Now we define first-order translation of the set of rules R as the following set
ΦR of first-order formulae, which are all assumed to be universally closed:
 1. R(ρgen   gen
       1 , ρ2 ) for all r ∈ R and hρ1 , ρ2 i ∈ sr              rewriting axioms
 2. R(x, x)                                                    reflexivity axiom
 3. R(x, y) ∧ R(y, z) → R(x, z)                               transitivity axiom
 4. R(x, y) ∧ R(z, v) → R(fq (x, z), fq (y, v)) for all q ∈ Q
                                                              congruence axioms
   In 1) we additionally require that generalizations ρgen
                                                        1    and ρgen
                                                                  2    should be
consistent, that means the variables used in the generalizations are the same in
the same positions.
   Now for simplicity we make the following
Assumption 1 An automaton AI = (QI , FI , δI ) is given over ranked alphabet
FQ .
    We define the translation of AI as the set ΦI of first-order formulae
 5. Iθ (fq (e, e)) for all →e θ′ and (θ′ , θ′ ) →fq θ in δI ;
 6. Iθ1 (x) ∧ Iθ2 (y) → Iθ3 (fq (x, y)) for all (θ1 , θ2 ) →fq θ3 ) in δI .
 7. ∨θ∈FI Iθ (x) → Init(x)
   Let AU = (QU , FU , δU ) is a tree automaton recognizing finitely based set
U nsaf e. Then its translation ΦU defined analogously to the translation of AI :
 8. Uθ (fq (e, e)) for all →e θ′ and (θ′ , θ′ ) →fq θ in δU ;
 9. Uθ1 (x) ∧ Uθ2 (y) → Uθ3 (fq (x, y)) for all (θ1 , θ2 ) →fq θ3 ) in δU .
10. ∨θ∈FU Uθ (x) → U nsaf e(x)
Proposition 3. (Adequacy of encoding) For an instance of the coverability prob-
lem and the translation defined above the following holds true:
 1. For any τ1 , τ2 ∈ T (Q) if τ1 ⇒∗P τ2 then ΦR ⊢ R(tτ1 , tτ2 )
 2. For any τ ∈ Init ΦI ⊢ Init(tτ );
 3. For any τ ∈ U nsaf e ΦU ⊢ U nsaf e(tτ )
Proof. proceeds by straightforward inspection of definitions.
Corollary 2. (safety verification) If ΦR ∪ΦI ∪ΦU 6⊢ ∃x∃yInit(x)∧U nsaf e(y)∧
R(x, y) then the coverability problem has a positive answer, that is τ 6⇒∗P τ ′ holds
for all τ ∈ Init and all τ ′ ∈ U nsaf e.
Theorem 2. (relative completeness) Given a parameterized tree system P =
(Q, R), the tree regular language of initial configurations Init, finitely based set
of unsafe configurations U nsaf e. Assume the backward symbolic reachability al-
gorithm for monotonic abstraction described above terminates with the fixed-point
U = Un+1 = Un for some n and Init ∩ U = ∅. Then there exists a finite model
for ΦR ∧ ΦI ∧ ΦU ∧ ¬(∃x∃yInit(x) ∧ U nsaf e(y) ∧ R(x, y)).
Proof. First we observe that since the fixed-point U has a finite set of generators
it is a regular tree language. Let AU ∗ = (QU ∗ , FU ∗ , δU ∗ ) be a deterministic tree
automaton recognizing U . We take QU ∗ as a domain of the required model.
Interpretations of all functional symbols from FQ are given by δU ∗ :
 – [fq ](θ1 , θ2 ) = θ3 iff (θ1 , θ2 ) →fq θ3 is in δU ∗
 – [e] = θ, where →e θ is in δU ∗ .
Interpretations of predicates R, Iθ , Init, Uθ , U nsaf e are defined inductively as
the least sets of tuples, or elements of the domains satisfying the axioms 1-
4, 5-7, 8-10, respectively. That concludes the definition of the model which we
denote by M. We have M |= ΦR ∧ ΦI ∧ ΦU by construction. Now we check that
M |= ¬(∃x∃yInit(x) ∧ U nsaf e(y) ∧ R(x, y)) is satisfied in the model. We have
 1. [Init] ⋆ [R] ⊆ {[τ ] | ∃τ ′ ∈ Init τ ′ ⇒∗P τ } (by the minimality conditions on
    interpretations of Init and R)
 2. {[τ ] | ∃τ ′ ∈ Init τ ′ ⇒∗P τ } ⊆ F̄U ∗ = Q − FU ∗ (by assumption U ∩ Init = ∅)
 3. [U nsaf e] ⊆ FU ∗ (by U nsaf e ⊆ U );
 4. ([Init] ⋆ [R]) ∩ [U nsaf e] = ∅ (by 1-3).
5.3   The case study, II
In this section we illustrate the discussed variation of the FCM method by ap-
plying it again to the verification of Two-way Token Protocol, but specified
differently. The specification of this protocol using trees over states and tree
rewriting is taken from [5]. The set of states Q = {n, t}, where n and t denote
local states ‘no token’ and ‘token’, respectively. The set of R of rewriting rules
consists of the following rules:
 – ht, ni(hn, ti);
 – hn, ti(ht, ni);
   The set Init of initial configurations consists all complete binary trees over
Q with exactly one token. The set U nsaf e of unsafe configuration consists of all
complete binary trees over Q with at least two tokens. The set of the formulae
Φ below is a first-order translation (in Mace4 syntax) of the verification task.


% rewriting rules

R(ft(fn(y,z),x),fn(ft(y,z),x)).
R(ft(x,fn(y,z)),fn(x,ft(y,z))).
R(fn(ft(y,z),x),ft(fn(y,z),x)).
R(fn(x,ft(y,z)),ft(x,fn(y,z))).

% reflexivity

R(x,x).

%congruence
(R(x,y) & R(z,v)) -> R(fn(x,z),fn(y,v)).
(R(x,y) & R(z,v)) -> R(ft(x,z),ft(y,v)).

% transitivity

(R(x,y) & R(y,z)) -> R(x,z).

% Initial states automaton
I1(fn(e,e)).
(I1(x) & I1(y)) -> I1(fn(x,y)).
(I1(x) & I1(y)) -> Init(ft(x,y)).
(Init(x) & I1(y)) -> Init(fn(x,y)).
(I1(x) & Init(y)) -> Init(fn(x,y)).

% Unsafe states automaton
B1(ft(x,y)).
B1(x) -> B1(fn(x,y)).
B1(y) -> B1(fn(x,y)).
B1(x) -> Unsafe(ft(x,y)).
B1(x) -> Unsafe(ft(y,x)).
B1(x) & B1(y) -> Unsafe(fn(x,y)).
B1(x) & B1(y) -> Unsafe(ft(x,y)).
Unsafe(x) -> Unsafe(fn(x,y)).
Unsafe(x) -> Unsafe(fn(y,x)).
Unsafe(x) -> Unsafe(ft(x,y)).
Unsafe(x) -> Unsafe(ft(y,x)).




   Now, in order to establish safety, it is sufficient to show that Φ 6⊢ ∃x∃yInit(x)∧
R(x, y)∧U nsaf e(y). Finite model finder Mace4 finds a model for Φ∧¬(∃x∃yInit(x)∧
R(x, y) ∧ U nsaf e(y)) in 0.04s.



6         Experimental results

We have applied both presented versions of FMC method to the verification of
several parameterized tree-shaped systems. The tasks specified in RTMC tra-
dition were taken from [3] and the first translation was used. To compare with
monotonic abstraction based methods we used the second translation for the
tasks from [5].
In the experiments we used the finite model finder Mace4[20] within the package
Prover9-Mace4, Version 0.5, December 2007. The system configuration used in
the experiments: Microsoft Windows XP Professional, Version 2002, Intel(R)
Core(TM)2 Duo CPU, T7100 @ 1.8Ghz 1.79Ghz, 1.00 GB of RAM. The time
measurements are done by Mace4 itself, upon completion of the model search it
communicates the CPU time used. The table below lists the parameterized tree
protocols and shows the time it took Mace4 to find a countermodel and verify a
safety property. The time shown is an average of 10 attempts. We also show the
time reported on the verification of the same protocols by alternative methods.


6.1       FCM vs RTMC

                   Protocol      Time Time reported in [6]∗
                   Token         0.02s               0.06s
                   Two-way Token 0.03s               0.09s

      ∗
     the system configuration used in [6] was Intel Centrino 1.6GHZ with 768MB
of RAM
   Notice that [6] discusses different methods for enhancement of RTMC within
the abstract-check-refine paradigm and we included in the table the best times
reported in [6] for each verification problem.
6.2       FCM vs monotonic Abstraction

                   Protocol        Time Time reported in [5]∗
                   Token           0.02s                   1s
                   Two-way Token 0.03s                     1s
                   Percolate       0.02s                   1s
                   Leader Election 0.03s                   1s
                   Tree-arbiter    0.02s                 37s
                   IEEE 1394       0.04s          1h15m25s

      ∗
      the system configuration used in [5] was dual Opteron 2.8 GHZ with 8 GB
of RAM
    All specifications used in the experiments and Mace4 output can be found in
[14].


7         Related work


    As mentioned Section 1 the approach to verification using the modeling of
protocol executions by first-order derivations and together with countermodel
finding for disproving was introduced within the research on the formal analysis
of cryptographic protocols ([23],[22],[9], [11], [10]).
    This work continues the exploration of the FCM approach presented in
[14,15,16,17,18,19]. In [17](which is an extended version of [15]) it was shown
that FCM provides a decision procedure for safety verification for lossy channel
systems, and that FCM can be used for efficient verification of parameterised
cache coherence protocols. The relative completeness of the FCM with respect
to regular model checking and methods based on monotonic abstraction for lin-
ear parameterized systems was established in [18](which is an extended version
of the abstract [16]). The relative completeness of the FCM with respect to
tree completion techniques for general term rewriting systems is shown in [19].
Our treatment of tree rewriting in 5.1 can be seen as a particular case of term
rewriting considered in [19] with slightly different translation of tree automata.
Detailed comparison and/or unified treatment of FCM vs Tree Completion vs
RTMC vs Monotonic Abstraction to be given elsewhere. Here we notice only
that the reason for FCM to succeed in verification of safety of various classess of
infinite-state and parameterized systems is the presence of regular sets of config-
urations (invariants) covering all reachable configurations and disjoint with the
sets of unsafe configurations.
    In a more general context, the work we present in this paper is related to the
concepts of proof by consistency [12], and inductionless induction [8] and can be
seen as an investigation into the power of these concepts in the particular setting
of the verification of parameterized tree systems via finite countermodel finding.
8    Conclusion

We have shown how to apply generic finite model finders in the parameterized
verification of tree-shaped systems, have demonstrated the relative completeness
of the method with respect to regular tree model checking and to the methods
based on monotonic abstraction and have illustrated its practical efficiency. Fu-
ture work includes the investigation of scalability of FCM, and its applications
to software verification.


Acknowledgments

The author is grateful to anonymous referees of FMCAD 2011 conference who
provided with many helpful comments on the previous version of this paper.


References
1. Abdulla, P.A., Delzanno G., Henda, N.B., & Rezine, A., (2009a), Monotonic Ab-
  straction: on Efficient Verification of Parameterized Systems. Int. J. Found. Comput.
  Sci. 20(5): 779-801
2. Abdulla, P.A., Jonsson, B., (1996) Verifying programs with unreliable channels.
  Information and Computation, 127(2):91-101, 1996.
3. Abdulla, Parosh Aziz and Jonsson, Bengt and Mahata, Pritha and d’Orso, Julien,
  Regular Tree Model Checking, in Proceedings of the 14th International Conference
  on Computer Aided Verification, CAV ’02, 2002, 555–568
4. Abdulla, P.A., Jonsson,B., Nilsson, M., & Saksena, M., (2004) A Survey of Regular
  Model Checking, In Proc. of CONCUR’04, volume 3170 of LNCS, pp 35–58, 2004.
5. Parosh Aziz Abdulla, Noomene Ben Henda, Giorgio Delzanno, Frdric Haziza and
  Ahmed Rezine, Parameterized Tree Systems, in FORMAL TECHNIQUES FOR
  NETWORKED AND DISTRIBUTED SYSTEMS FORTE 2008, Lecture Notes in
  Computer Science, 2008, Volume 5048/2008, 69-83.
6. A. Bouajjani, P. Habermehl,A. Rogalewicz, T. Vojnar, Abstract Regular Tree Model
  Checking, Electronic Notes in Theoretical Computer Science, 149, (2006), 37–48.
7. Caferra, R., Leitsch, A., & Peltier, M., (2004) Automated Model Building, Applied
  Logic Series, 31, Kluwer, 2004.
8. Comon, H., (1994), Inductionless induction. In R. David, ed. 2nd Int. Conf. in
  Logic for Computer Science: Automated Deduction. Lecture Notes, Chambery, Uni
  de Savoie, 1994.
9. Goubault-Larrecq, J., (2010), Finite Models for Formal Security Proofs, Journal of
  Computer Security, 6: 1247–1299, 2010.
10. Guttman, J., (2009) Security Theorems via Model Theory, Proceedings 16th In-
  ternational Workshop on Expressiveness in Concurrency, EXPRESS, EPTCS, vol. 8
  (2009)
11. Jurjens, J., & Weber, T., (2009), Finite Models in FOL-Based Crypto-Protocol
  Verification, P. Degano and L. Vigan‘o (Eds.): ARSPA-WITS 2009, LNCS 5511, pp.
  155-172, 2009.
12. Kapur, D., & Musser, D.R., (1987), Proof by consistency. Artificial Intelligence,
  31:125–157, 1987.
13. Kruskal, J.B., (1960), Well-Quasi-Ordering, the Tree Theorem, and Vazsonyi’s
  Conjecture, Transactions of the American Mathematical Society, 95,2:210–225, 1960.
14. Lisitsa, A., (2009a), Verfication via countermodel finding
  http://www.csc.liv.ac.uk/~alexei/countermodel/
15. Lisitsa, A., (2009b), Reachability as deducibility, finite countermodels and verifi-
  cation. In preProceedings of AVOCS 2009, Technical Report of Computer Science,
  Swansea University, CSR-2-2009, pp 241-243.
16. Lisitsa, A., (2010a), Finite countermodels as invariants. A case study in verification
  of parameterized mutual exclusion protocol. In Proceedings of WING 2010, 1pp
17. Lisitsa, A., (2010b), Reachability as deducibility, finite countermodels and verifi-
  cation. In Proceedings of ATVA 2010, LNCS 6252, 233–244
18. Lisitsa, A., (2010c), Finite model finding for parameterized verification, CoRR
  abs/1011.0447: (2010)
19. Lisitsa, A., (2011), Finite models vs tree automata in safety verification, CoRR
  abs/1107.0349: (2011) .
20. McCune, W., Prover9 and Mace4 http://www.cs.unm.edu/~mccune/mace4/
21. Nilsson, M., (2005) Regular Model Checking. Acta Universitatis Upsaliensis. Up-
  psala Dissertations from the Faculty of Science and Technology 60. 149 pp. Uppsala.
  ISBN 91-554-6137-9, 2005.
22. Selinger, P., (2001), Models for an adversary-centric protocol logic. Electr. Notes
  Theor. Comput. Sci. 55(1) (2001)
23. Weidenbach, C., (1999), Towards an Automatic Analysis of Security Protocols in
  First-Order Logic, in H. Ganzinger (Ed.): CADE-16, LNAI 1632, pp. 314–328, 1999.
