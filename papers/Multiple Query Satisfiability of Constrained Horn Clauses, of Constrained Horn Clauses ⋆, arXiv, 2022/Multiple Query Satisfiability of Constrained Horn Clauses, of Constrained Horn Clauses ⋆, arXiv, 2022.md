                                                           Multiple Query Satisfiability
                                                          of Constrained Horn Clauses ⋆

                                                             Emanuele De Angelis1[0000−0002−7319−8439] ,
                                                               Fabio Fioravanti2[0000−0002−1268−7829] ,
                                                            Alberto Pettorossi1,3[0000−0001−7858−4032] , and
arXiv:2211.15207v2 [cs.LO] 11 Jan 2024




                                                               Maurizio Proietti1[0000−0003−3835−4931]
                                         1
                                             IASI-CNR, Rome, Italy {emanuele.deangelis,maurizio.proietti}@iasi.cnr.it
                                         2
                                             DEc, University ‘G. d’Annunzio’, Chieti-Pescara, Italy fabio.fioravanti@unich.it
                                             3
                                               DICII, University of Rome ‘Tor Vergata’, Italy pettorossi@info.uniroma2.it

                                                 Abstract. We address the problem of checking the satisfiability of a set
                                                 of constrained Horn clauses (CHCs) possibly including more than one
                                                 query. We propose a transformation technique that takes as input a set
                                                 of CHCs, including a set of queries, and returns as output a new set
                                                 of CHCs, such that the transformed CHCs are satisfiable if and only if
                                                 so are the original ones, and the transformed CHCs incorporate in each
                                                 new query suitable information coming from the other ones so that the
                                                 CHC satisfiability algorithm is able to exploit the relationships among all
                                                 queries. We show that our proposed technique is effective on a non trivial
                                                 benchmark of sets of CHCs that encode many verification problems for
                                                 programs manipulating algebraic data types such as lists and trees.


                                         1     Introduction
                                         Constrained Horn Clauses (CHCs) have been advocated as a logical formalism
                                         very well suited for automatic program verification [3, 6]. Indeed, many verifica-
                                         tion problems can be reduced to problems of checking satisfiability of CHCs [13],
                                         and several effective CHC solvers are currently available as back-end tools for
                                         program verification purposes [4, 7, 16, 18, 19].
                                             Following the CHC-based verification approach, a program is translated into
                                         a set of definite CHCs (that is, clauses whose head is different from false), which
                                         capture the semantics of the program, together with a set of queries (that is,
                                         clauses whose head is false), which specify the program properties to be verified.
                                         Very often the CHC translation of the verification problem generates several
                                         queries. In particular, this is the case when the program includes several func-
                                         tions, each one having its own contract (that is, a pair of a pre-condition and a
                                         post-condition).
                                             CHC solvers try to show the satisfiability of a set of CHCs of the form:
                                         P ∪ {false ← G1 , . . . , false ← Gn }, where P is a set of definite CHCs, and
                                         ⋆
                                             The Version of Record of this contribution will be published in the Proceedings
                                             of PADL 2023, Boston, MA, USA, January 16–17, 2023: The 25th International
                                             Symposium on “Practical Aspects of Declarative Languages” as a volume of the
                                             Lecture Notes of Computer Science (LNCS) series of Springer Nature.
2                         E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti

false ← G1 , . . . , false ← Gn are queries, by trying to show in a separate way
the satisfiability of each set P ∪ {false ← Gi }, for i = 1, . . . , n. This approach
may not be always quite effective, as the solver may not be able to exploit the,
possibly mutual, dependencies among the various queries. There is a simple way
of combining all queries into one (as done, for instance, in the CHC solver com-
petition [10]): we introduce a new predicate f , and from the above mentioned set
of CHCs we get P ∪ {false ← f, f ← G1 , . . . , f ← Gn }. However, also in this case,
existing solvers will handle each query separately and then combine the results.
       In this paper we propose, instead, a technique that, given a set P ∪{false ← G1 ,
. . . , false ← Gn } of CHCs, derives an equisatisfiable set P ′ ∪ {false ← G′1 , . . . ,
false ← G′n }, for whose satisfiability proof a CHC solver may exploit the mutual
interactions among the n satisfiability proofs, one for each query.
       Our technique builds upon the transformation approach for verifying con-
tracts that we presented in previous work and implemented in the VeriCaT
tool [8]. The algorithm of VeriCaT takes as input a set of CHCs that manipulate
algebraic data types (ADTs) such as lists and trees, and a set of CHCs defining
contracts by means of catamorphisms [20], and returns as output a set of CHCs
without ADT variables such that the original set is satisfiable if the new set is
satisfiable. For CHCs without ADT variables state-of-the-art solvers are more
effective in proving satisfiability, and hence validity of contracts.
       The objective of the transformation algorithm presented in this paper, which
we call Tmq , is not to eliminate ADT variables, rather, it is to incorporate into
the clauses relative to a particular query some additional constraints that are
derived from other queries. These additional constraints are often very beneficial
to the CHC solvers when trying to check the satisfiability of a given set of clauses,
thereby enhancing their ability to verify program properties. Algorithm Tmq is
both sound and complete, that is, the transformed clauses are satisfiable if and
only if so are the original ones. The completeness of Tmq is very important
because if a property does not hold, it allows us to infer the unsatisfiability of
the original clauses. Thus, whenever the solver shows the unsatisfiability of the
transformed clauses, we deduce the invalidity of the property to be verified.

2    Preliminary Notions

We consider constrained Horn clauses that are defined in a many-sorted first
order language L with equality (=) whose constraints are expressed using lin-
ear integer arithmetic (LIA) and boolean (Bool) expressions. A constraint is a
quantifier-free formula c, where the LIA constraints may occur as subexpressions
of boolean constraints, according to the SMT approach [2]:
  c ::= d | B | true | false | ∼ c | c1 & c2 | c1∨c2 | c1 ⇒ c2 | c1 = c2 |
         ite(c, c1 , c2 ) | t = ite(c, t1 , t2 )
  d ::= t1= t2 | t1< t2 | t1≤ t2 | t1≥ t2 | t1> t2
where: (i) B is a boolean variable, (ii) ∼, &, ∨, and ⇒ denote negation, con-
junction, disjunction, and implication, respectively, (iii) the ternary function ite
denotes the if-then-else operator, and (iv) t is a LIA term of the form a0 +
                                           Multiple Query Satisfiability of CHCs            3

a1 X1 + · · · + an Xn with integer coefficients a0 , . . . , an and variables X1 , ..., Xn .
The equality symbol will be used both for integers and booleans. We will often
write B = true (or B = false) as B (or ∼B). The theory of LIA and boolean
constraints will be denoted by LIA ∪ Bool . The integer and boolean sorts are
said to be basic sorts. A recursively defined sort (such as the sort of lists and
trees) is said to be an algebraic data type (ADT, for short).
    An atom is a formula of the form p(t1 , . . . , tm ), where p is a predicate symbol
not occurring in LIA ∪ Bool, and t1 , . . . , tm are first order terms in L. A con-
strained Horn clause (CHC), or simply, a clause, is an implication of the form
H ← c, G. The conclusion H, called the head, is either an atom or false, and the
premise, called the body, is the conjunction of a constraint c and a conjunction G
of zero or more atoms. A clause is said to be a query if its head is false, and a
definite clause, otherwise. Without loss of generality, we assume that every atom
of the body of a clause has distinct variables (of any sort) as arguments. The set
of all variables occurring in an expression e is denoted by vars(e). By bvars(e)
(or adt -vars(e)) we denote the set of variables in e whose sort is a basic sort (or
an ADT sort). The universal closure of a formula ϕ is denoted by ∀(ϕ).
    Let D be the usual interpretation for the symbols of theory LIA ∪ Bool. By
M (P ) we denote the least D-model of a set P of definite clauses [17].
    Now, in order to characterize the class of queries that can be handled us-
ing our transformation technique, we introduce (see Definition 1 below) a class
of recursive schemata defined by CHCs [8]. That class is related to those of
morphisms, catamorphisms, and paramorphisms considered in functional pro-
gramming [15, 20]. We will not introduce a new terminology here and we will
refer to our schemata as generalized catamorphisms, or catamorphisms, for short.
    Let f be a predicate symbol with m+n arguments (for m ≥ 0 and n ≥ 0) whose
sorts are α1 ,. . ., αm , β1 , . . . , βn , respectively. We say that f is a functional predi-
cate from α1 ×. . .×αm to β1 ×. . .×βn , with respect to a set P of definite clauses,
if M (P ) |= ∀X,Y,Z. f (X,Y ) ∧ f (X,Z) → (Y = Z), where X is an m-tuple of dis-
tinct variables, and Y and Z are n-tuples of distinct variables. Given the atom
f (X, Y ), we say that X and Y are the tuples of the input and output variables
of f , respectively. Predicate f is said to be total if M (P ) |= ∀X∃Y. f (X, Y ). In
what follows, a ‘total, functional predicate’ f from a tuple α of sorts to a tuple β
of sorts will be called a ‘total function’ and denoted by f ∈ [α → β] (the set P
of clauses that define f will be understood from the context).
Definition 1 (Generalized Catamorphisms). A generalized list catamor-
phism, shown in Figure 1 (A), is a total function h ∈ [σ × list (β) → ̺], where :
(i) σ, β, ̺, and τ are (products of ) basic sorts, (ii) list (β) is the sort of lists
of elements of sort β, (iii) base1 is a total function in [σ → ̺], (iv) f is a
catamorphism in [σ × list (β) → τ ] and (v) combine1 is a total function in
[σ × β × ̺ × τ → ̺]. Similarly, a generalized tree catamorphism is a total func-
tion t ∈ [σ × tree(β) → ̺] defined as shown in Figure 1 (B).
Note that the above definition is recursive, that is, the predicates f and g are
defined by instances of schemata (A) and (B), respectively. Examples of cata-
morphisms will be shown in the following section.
4                              E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti

          h(X, [ ], Y ) ← base1(X, Y ).            t(X, leaf , Y ) ← base2(X, Y ).
          h(X, [H|T ], Y ) ←                       t(X, node(L, N, R), Y ) ←
             f (X, T, Rf ),                           g(X, L, RLg), g(X, R, RRg),
             h(X, T, R),                              t(X, L, RL), t(X, R, RR),
             combine1(X, H, R, Rf , Y ).              combine2(X, N, RL, RR, RLg, RRg, Y ).
    (A)                                      (B)
Fig. 1: (A) Generalized list catamorphism. (B) Generalized tree catamorphism.


3     An Introductory Example


Let us consider the clauses of Figure 2, which are the result of translating an
iterative program for Insertion Sort. (Details on how this translation can be
performed are outside the scope of this paper.) The clauses in Figure 2 will be
called program clauses and the predicates defined by those clauses will be called
program predicates.
     We have that ins--sort (Xs, Ys, Zs) holds if Zs is the ordered list of integers
(here and in what follows, the order is with respect to ≤) obtained by inserting
every element of the list Ys in the proper position of the ordered list Xs. Thus,
the result of sorting a list Ys is the list Zs such that ins--sort ([ ], Ys, Zs) holds.
The predicate ins--sort depends (see clause 2) on the predicates empty --list and
ord --ins. We have that empty --list (L) holds if the list L is empty, and
ord --ins(Y , Xs1, Xs2, Ys, Zs) holds if: (i) the concatenation of the lists Xs1 and
Xs2 is ordered, (ii) Y is greater than or equal to the last element of Xs1, and
(iii) ins--sort (Xs ′ , Ys, Zs) holds, where Xs ′ is the concatenation of Xs1 and the
ordered list obtained by inserting (according to the ≤ order) Y into Xs2. As
usual, append (Xs, Ys, Zs) holds if Zs is the concatenation of the lists Xs and
Ys, and snoc(Xs, Y , Zs) holds if append (Xs, [Y ], Zs) holds.
    It is not immediate to see why the above properties for ins--sort and ord --ins
are valid. This is also due to the fact that the predicates ins--sort and ord --ins
are mutually recursive. The goal of this paper is to present a technique based on
CHC transformations that allows us to automatically prove properties expressed
by possibly mutually recursive predicates, using a CHC solver.

    1. ins--sort(Xs, [ ], Xs).                      8. ord --ins(Y , Xs1, [ ], Ys, Zs) ←
    2. ins--sort(Xs, [Y |Ys], S ) ←                      snoc(Xs1, Y , Xs1Y ),
             empty--list(L),                             ins--sort(Xs1Y, Ys, Zs).
             ord --ins(Y , L, Xs, Ys, S ).          9. ord --ins(Y , Xs1, [X |Xs2], Ys, Zs) ←
    3. append ([ ], Ys, Ys).                             Y ≤ X , snoc(Xs1, Y , Xs1Y ),
    4. append ([X |Xs], Ys, [X |Zs]) ←                   snoc(Xs1Y , X , Xs1YX ),
             append (Xs, Ys, Zs).                        append (Xs1YX , Xs2, Xs),
    5. snoc([ ], X , [X ]).                              ins--sort(Xs, Ys, Zs).
    6. snoc([H |T ], X , [H |TX ]) ←               10. ord --ins(Y , Xs1, [X |Xs2], Ys, Zs) ←
             snoc(T , X , TX ).                          Y > X , snoc(Xs1, X , Xs1X ),
    7. empty--list([ ]).                                 ord --ins(Y , Xs1X , Xs2, Ys, Zs).

                        Fig. 2: Program clauses for Insertion Sort.
                                              Multiple Query Satisfiability of CHCs             5

    Now we will present the clauses that formalize the properties we want to show
in our Insertion Sort example. This set of clauses is made out of two subsets:
(A) a set of definite CHCs that define the catamorphisms used in the queries,
and (B) a set of queries that specify the program properties to be shown.
    For (A), in Figure 3 we present the definite CHCs defining the three cata-
morphisms we will use. They are: (i) ordered , which takes as input a list Ls
and returns a boolean B such that if Ls is ordered, then B = true, otherwise
B = false; (ii) first , which takes as input a list Ls and returns a boolean B and
an element F such that if Ls is empty, then B = false and F = 0 (this value
for F is an arbitrary integer and will not be used elsewhere), otherwise B = true
and F is the head of Ls; and (iii) last , which is analogous to first, except that
it returns the last element L, if any, instead of the first element.
    The predicates of these catamorphisms are called property predicates.
11. ordered ([ ], B ) ← B .                    13. first([ ], B , F ) ← ∼B & F = 0.
12. ordered ([H |T ], B ) ←                    14. first([H |T ], B , F ) ← B & F = H .
     B = (B 1 ⇒ (H ≤ F & B 2)),                15. last([ ], B , L) ← ∼B & L = 0.
     first(T , B 1, F ), ordered (T , B 2).    16. last([H |T ], B , L) ←
                                                     B & L = ite(B 1, L1, H ), last(T , B 1, L1).
       Fig. 3: Property clauses for Insertion Sort: (A) the catamorphisms.
     For (B), we present the set of queries that specify the program properties. We
assume that: (i) at most one property is specified for each program predicate, and
(ii) the property related to the program predicate p is expressed as an implication
of the form: p(. . .), cata 1 (. . .), . . . , cata n (. . .) → d, where the cata i (. . .)’s are
catamorphisms and d is a constraint. This implication can be expressed as a
query by adding ∼ d to its premise and changing its conclusion to false. For our
Insertion Sort example, in Figure 4 we specify four properties by introducing a
query for the predicates ins--sort, ord--ins, append , and snoc.
     For ins--sort, query q1 states that given a list of integers Ys, if Xs is ordered
and ins--sort (Xs,Ys, Zs) holds, then Zs is ordered. For ord--ins, query q2 states
that if the concatenation of the lists Xs1 and Xs2 is ordered (that is, Xs1 and
Xs2 are ordered, and the last element of Xs1 is less than or equal to the first
element of Xs2), Y is greater than or equal to the last element of Xs1, and
ord --ins(Y , Xs1, Xs2, Ys, Zs) holds, then Zs is ordered. For append , query q3
states that if Xs1 and Xs2 are ordered, and the last element of Xs1 is less than
or equal to the first element of Xs2 and append (Xs,Ys,Zs) holds, then Zs is
ordered. For snoc, query q4 states that if Xs is ordered, and the last element of
Xs is less than or equal to X , and snoc(Xs, X , XsX ) holds, then XsX is ordered.
    At this point, we can check whether or not the properties expressed by the
queries q1–q4 do hold by checking the satisfiability of the program clauses to-
gether with the property clauses. In order to perform that satisfiability check, we
have used the state-of-the-art CHC solver SPACER, based on Z3 [18]. SPACER
failed to return an answer within five minutes. The weakness of CHC solvers for
examples like the one presented here, motivates our technique based on CHC
transformation. This technique produces an equisatisfiable set of CHCs whose
6                            E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti

(q1)    false ← ∼ (B 1 ⇒ B 2), ordered (Xs, B 1), ordered (Zs, B 2), ins--sort(Xs, Ys, Zs).
(q2)    false ← ∼ ((B 1 & B 2 & ((B 4 & B 5) ⇒ L ≤ F ) & (B 4 ⇒ L ≤ Y )) ⇒ B 3),
          ordered (Xs1, B 1), ordered (Xs2, B 2), ordered (Zs, B 3),
          last(Xs1, B 4, L), first(Xs2, B 5, F ), ord --ins(Y , Xs1, Xs2, Ys, Zs).
(q3)    false ← ∼ ((B 1 & B 2 & ((B 4 & B 5) ⇒ L ≤ F )) ⇒ B 3),
          ordered (Xs, B 1), ordered (Ys, B 2), ordered (Zs, B 3),
          last(Xs, B 4, L), first(Ys, B 5, F ), append (Xs, Ys, Zs).
(q4)    false ← ∼ ((B1 & (B2 ⇒ L ≤ X)) ⇒ B3),
          ordered (Xs, B 1), last(Xs, B 2, L), ordered (XsX , B 3), snoc(Xs, X , XsX ).

            Fig. 4: Property clauses for Insertion Sort: (B) the queries.
satisfiability can be, hopefully, easier to verify. Indeed, in our example, SPACER
succeeds to prove the satisfiability of the new set of CHCs produced by our trans-
formation algorithm. In Section 7, we will show that our technique improves the
effectiveness of state-of-the-art solvers on a non-trivial benchmark.


4      Catamorphism-based Queries
As already mentioned, the translation of a program verification problem to CHCs
usually generates two disjoint sets of clauses: (i) the set of program clauses, and
(ii) the set of property clauses, with the associated sets of program predicates,
and property predicates. Without loss of generality, we will assume that property
predicates may occur in the property clauses only. Moreover, in order to define
a class of CHCs where our transformation technique always terminates, we will
consider property predicates that are catamorphisms (see Definition 1). In the
sequel we need the following definitions. An atom is said to be a program atom
(or a catamorphism atom), if its predicate symbol is a program predicate (or a
catamorphism, respectively). Recall that when writing a catamorphism atom as
cata(X, T, Y ), we stipulate that X is the (tuple of its) input basic variable(s), T
is the input ADT variable, and Y is the (tuple of its) output basic variable(s).
Definition 2. A catamorphism-based query is a query of the form :
            false ← c, cata 1 (X1 , T1 , Y1 ), . . . , cata n (Xn , Tn , Yn ), pred (Z)
where: (i) pred is a program predicate and Z is a tuple of distinct variables,
(ii) c is a constraint such that vars(c) ⊆ {X1 , . . . , Xn , Y1 , . . . , Yn , Z}, (iii) cata 1 ,
. . . , cata n are catamorphism atoms, (iv) Y1 , . . . , Yn are pairwise disjoint tuples
of distinct variables of basic sort not occurring in X1 , . . . , Xn , Z, (v) T1 , . . . , Tn
are ADT variables occurring in Z.
    The queries of Figure 4 are examples of catamorphism-based queries. Many
interesting program properties can be defined as catamorphism-based queries,
although, in general, this might require some ingenuity.

5      Transformation Rules
In this section we present the rules that we use for transforming CHCs. These
rules are variants of the usual transformation rules for CHCs (and CLP pro-
                                        Multiple Query Satisfiability of CHCs         7

grams), specialized to our context where we use catamorphisms. Then, we prove
the soundness and completeness of those rules.
    The goal of the transformation rules is to incorporate catamorphisms into
program predicates, that is, to derive for each program predicate p, a new predi-
cate newp whose definition is given by the conjunction of an atom for p with the
catamorphism atoms needed for showing the satisfiability of the query relative
to p. In this section we will indicate how this can be done referring our Inser-
tion Sort example, while in the next section we will present a transformation
algorithm to perform this task in an automatic way.
    A transformation sequence from S0 to Sn is a sequence S0 Z⇒ S1 Z⇒ . . . Z⇒ Sn
of sets of CHCs such that, for i = 0, . . . , n−1, Si+1 is derived from Si , denoted
Si Z⇒ Si+1 , by performing a transformation step consisting in applying one of
the following rules R1–R4.
(R1) Definition Rule. Let D be a clause of the form newp(X1 , . . . , Xk ) ←
c, Catas, A, where: (1) newp is a predicate symbol not occurring in the sequence
S0 Z⇒ S1 Z⇒ . . . Z⇒ Si constructed so far, (2) {X1 , . . . , Xk } = vars({Catas, A}),
(3) c is a constraint such that vars(c) ⊆ vars({Catas, A}), (4) Catas is a con-
junction of catamorphism atoms, with adt-vars(Catas) ⊆ adt-vars(A), and (5) A
is a program atom. By definition introduction we may add D to Si and get
Si+1 = Si ∪ {D}.
       The case where A is absent is accommodated by considering A to be true(X),
which holds for every X of ADT sort.
       For j = 0, . . . , n, by Defs j we denote the set of clauses, called definitions,
introduced by rule R1 during the construction of the sequence S0 Z⇒ S1 Z⇒
. . . Z⇒ Sj . Thus, Defs 0 = ∅, and for j = 0, . . . , n, Defs j ⊆ Defs j+1 .
   In our Insertion Sort example, the set S0 consists of all the clauses shown in
Figures 2, 3, and 4, and we start off by introducing the following definition (with
constraint true), whose body consists of the atoms in the body of query q1:
D1. new 1(Xs,B 1,Zs,B 2,Ys) ← ordered (Xs,B 1), ordered (Zs,B 2), ins--sort (Xs,Ys,Zs).
Thus, S1 = S0 ∪ {D1}.                                                              
    The clauses for newp are obtained by first (i) unfolding the definition of
newp, then (ii) incorporating some catamorphisms and constraints provided by
the queries into the clauses derived by unfolding, and (iii) finally, folding using
suitable new definitions. Now, we introduce an unfolding rule (see R2 below),
which actually is the composition of the unfolding and the application of the
functionality property presented in previous work [8]. Let us first define the
notion of the one-step unfolding which is a step of symbolic evaluation performed
by applying once the resolution rule.
Definition 3 (One-step Unfolding). Let C: H ← c, L, A, R be a clause, where
A is an atom, and let P be a set of definite clauses with vars(C) ∩ vars(P ) = ∅.
Let Cls: {K1 ← c1 , B1 , . . . , Km ← cm , Bm }, with m ≥ 0, be the set of clauses
in P , such that: for j = 1, . . . , m, (i) there exists a most general unifier ϑj of
A and Kj , and (ii) the conjunction of constraints (c, cj )ϑj is satisfiable. The
one-step unfolding produces the following set of CHCs :
8                             E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti

     Unf (C, A, P ) = {(H ← c, cj , L, Bj , R)ϑj | j = 1, . . . , m}.
     In the following Rule R2 and in the sequel, Catas denotes a conjunction of
catamorphism atoms.
(R2) Unfolding Rule. Let D: newp(U ) ← c, Catas, A be a definition in Si ∩ Defsi
and P be the set of definite clauses in Si . We derive a new set UnfCls of clauses
by the following three steps.
Step 1. (One-step unfolding of the program atom) UnfCls := Unf (D, A, P );
Step 2. (Unfolding of the catamorphism atoms)
       while there exists a clause E: H ← d, L, C, R in UnfCls, for some con-
       junctions L and R of atoms, such that C is a catamorphism atom whose
       argument of ADT sort is not a variable do
          UnfCls := (UnfCls \ {E}) ∪ Unf (E , C , P );
Step 3. (Applying Functionality)
       while there exists a clause E: H ← d, L, cata(X, T, Y 1), cata(X, T, Y 2), R
       in UnfCls, for some catamorphism cata do
          UnfCls := (UnfCls − {E}) ∪ {H ← d, Y 1 = Y 2, L, cata(X, T, Y 1), R};
Then, by unfolding D we derive Si+1 = (Si \ {D}) ∪ UnfCls.
For instance, in our Insertion Sort example, by unfolding definition D1, at Step 1
we replace D1 by:
E1. new 1(A, B, A, C, [ ]) ← ordered (A, B), ordered (A, C).
E2. new 1(A, B, C, D, [E|F ]) ← ordered (A, B), ordered (C, D),
                                          empty--list(G), ord--ins(E, G, A, F, C).
Step 2 of the unfolding rule is not performed in this example. At Step 3, clause
E1 is replaced by:
E3. new 1(A, B, A, C, [ ]) ← B = C, ordered (A, B).
Thus, S2 = S0 ∪ {E2, E3}.                                                                       
     The query-based strengthening rule allows us to use the queries occurring
in the set of CHCs whose satisfiability is under verification for strengthening
the body of the other clauses with the addition of catamorphism atoms and
constraints.
(R3) Query-based Strengthening Rule. Let Si = P ∪Q, where P is a set of definite
clauses obtained by applying the unfolding rule, and Q is a set of catamorphism-
based queries, and let C: H ← c, CatasC, A1 , . . . , Am be a clause in P , being
the Ai ’s program atoms. Let E be the clause derived from C as follows:
for k = 1, . . . , m do
 - consider program atom Ak ; let Catas C             k be the conjunction of every catamor-
   phism atom F in CatasC such that adt -vars(Ak ) ∩ adt -vars(F ) 6= ∅;
 - if in Q there exists a query (modulo variable renaming)
   qk : false ← ck , cata 1 (X1 , T1 , Y1 ), . . . , cata n (Xn , Tn , Yn ), Ak
   where Y1 , . . . , Yn do not occur in C, and the conjunction cata 1 (X1 , T1 , Y1 ), . . . ,
   cata n (Xn , Tn , Yn ) can be split into two subconjunctions B1 and B2 such
   that: (i) a variant of B1 is a subconjunction of Catas C                  k , and (ii) for every
   catamorphism atom cata i (Xi , Ti , Yi ) in B2 there is no catamorphism atom
   cata i (V, Ti , W ) in Catas Ck
   then add the conjunction ∼ ck , B2 to the body of C.
                                        Multiple Query Satisfiability of CHCs        9

Then, by query-based strengthening of clause C using queries q1 , . . . , qm (some
of these queries may be absent), we get the new set Si+1 = (Si \ {C}) ∪ {E}.
For instance, from clause E2 by query-based strengthening using q2 (note that
in E2 the program atom empty--list has no associated query), we get:
E4. new1(A, B, C, D, [E|F ]) ←                            
          L & B & ((J &H ) ⇒ K ≤ I ) & (J ⇒ K ≤ E ) ⇒ D ,
         ordered (A, B), ordered (C, D),                                 (B1 )
         ordered (G, L), last (G, J, K), first (A, H, I),                (B2 )
         empty--list(G), ord--ins(E, G, A, F, C).
where the subconjunction B1 mentioned in Rule R3 is in line (B1 ), while the
subconjunction B2 is in line (B2 ). Thus, S3 = S0 ∪ {E3, E4}.                   
   The folding rule allows us to replace a conjunction of a program atom and
catamorphisms by a single atom, whose predicate has been introduced in a pre-
vious application of the Definition Rule.
(R4) Folding Rule. Let C: H ← c, CatasC , A1 , . . . , Am be a clause in Si , where
either H is false or C has been obtained by the unfolding rule, possibly followed
by query-based strengthening. For k = 1, . . . , m,
                                                                              C
 - let Catas C
             k be the conjunction of every catamorphism atom F in Catas such
   that adt -vars(Ak ) ∩ adt -vars(F ) 6= ∅;
 - let Dk : Hk ← dk , Catas D
                            k , Ak be a clause in Defs i (modulo variable renaming)
   such that: (i) D |= ∀(c → dk ), and (ii) Catas C
                                                  k is a subconjunction of Catas k .
                                                                                    D

Then, by folding C using D1 , . . . , Dm , we derive clause E: H ← c, H1 , . . . , Hm ,
and we get Si+1 = (Si \ {C}) ∪ {E}.
    In order to fold clause E4, we introduce two new definitions, one for each
program atom occurring in the body of that clause, as follows (the predicate
names are introduced by our tool):
D2. new 2(A, B, C, D, E, F, G, H, I, J, K, L) ← ordered (A, B), ordered (C, D),
           ordered (E, F ), last (A, G, H), first(C, I, J), ord--ins(K, A, C, L, E).
D3. new 19(A, B, C, D) ← ordered (A, B), last (A, C, D), empty--list(A).
    Thus, S4 = S0 ∪ {E3, E4, D2, D3}.
    Now, we apply Rule R4, and from clause E4 we get:                        
E5. new 1(A,B,C,D,[E|F ]) ← G & B & ((H &I) ⇒ J ≤ K) & (H ⇒ J ≤ E) ⇒ D,
          new 2(L, G, A, B, C, D, H, J, I, K, E, F ), new 19(L, G, H, J).
Then, S5 = S0 ∪ {E3, E5, D2, D3}. Also, query q1 can be folded using defini-
tion D1, and we get:
E6. false ← ∼ (B 1 ⇒ B 2), new 1(Xs, B 1, Zs, B 2, Ys).
    Thus, S6 = (S0 \ {q1})∪{E3, E5, E6, D2, D3}. Then, the transformation will
continue by looking for the clauses relative to the newly introduced predicates
new 2 (see Definition D2) and new 19 (see Definition D3).                         
   The key for understanding our transformation technique is to observe that in
our Insertion Sort example, the query E6 and the clauses E3 and E5 that define
the new predicate new 1, incorporate the program predicate ins--sort together
with the catamorphisms that are used in q1. The advantage of performing this
transformation is that the solver can look for a model of new 1(Xs,B 1,Zs,B 2,Ys)
10                         E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti

where the constraint B1 ⇒B2 holds, instead of looking in a separate way for
models of ordered (Xs,B1), ordered (Zs,B2), and ins--sort (Xs,Ys,Zs) whose con-
junction implies B1 ⇒ B2. Note also that clause E5 has constraints and cata-
morphisms that come from query-based strengthening. Indeed, E5 is obtained
by folding E4 derived by strengthening E2 using query q2.
   The following Theorem 1, whose proof sketch is given in Appendix 1, states
the correctness of the transformation rules.
Theorem 1 (Soundness and Completeness of the Rules). Let S0 Z⇒ S1 Z⇒
. . . Z⇒ Sn be a transformation sequence using rules R1–R4. Then, S0 is satisfiable
if and only if Sn is satisfiable.
       Note that the applicability conditions of R3 disallow the application of the
rule to a query. Otherwise, we could easily get a satisfiable clause from an un-
satisfiable one. Indeed, we could transform false ← c(Y ), cata(X, Y ), p(X) into
false ← ∼ c(Y ) & c(Y ), cata(X, Y ), p(X). Note also that folding a clause using
itself is not allowed, thus avoiding the transformation of H ← c, Catas, A into
the trivially satisfiable clause H ← c, H.
       The applicability conditions of the rules force a sequence of the transforma-
tion rules which is fixed, if the new definitions to be introduced are known. The
algorithm that we will present in the next section shows how these definitions
can be introduced in an automatic way.


6    Transformation Algorithm
In this section we present an algorithm, called Tmq , which given a set P of
definite clauses and a set Q of queries, introduces a set of new predicates and
transforms P ∪ Q into a new set P ′ ∪ Q′ such that: (i) P ∪ Q is satisfiable
if and only if P ′ ∪ Q′ is so, and (ii) each new predicate defined in P ′ ∪ Q′ is
equivalent to the conjunction of a program predicate and some catamorphisms
needed for checking the satisfiability of the queries in Q. As an effect of the
application of the query-based strengthening rule, the transformed clauses also
exploit the interdependencies among the queries in Q. This transformation is
effective, in particular, in the presence of mutually recursive predicates, like in
our Insertion Sort example, where we are able to get new clauses for checking the
satisfiability of the query q1 for ins--sort that take into account the constraints
and catamorphisms of the query q2 for ord--ins, and vice versa.
    The set of new definitions needed by Tmq is computed as the least fixpoint
of an operator τP,Q that transforms a set ∆ of definitions into a new set ∆′ . For
introducing that operator, we need some preliminary definitions and functions.
Definition 4. A generalization of a pair (c1 , c2 ) of constraints is a constraint,
denoted α(c1 , c2 ), such that D |= ∀(c1 → α(c1 , c2 )) and D |= ∀(c2 → α(c1 , c2 )) [11].
The projection of a constraint c onto a tuple V of variables is a constraint π(c, V )
such that: (i) vars(π(c, V )) ⊆ V and (ii) D |= ∀(c → π(c, V )).
   A set ∆ of definitions is monovariant if it contains at most one definition for
each program predicate.
                                           Multiple Query Satisfiability of CHCs           11

Definition 5. Let D1 : newp1(U1 ) ← c1 , Catas 1 , p(Z) and D2 : newp2(U2 ) ←
c2 , Catas 2 , p(Z) be two definitions for the same predicate p. We say that D2 is an
extension of D1 , written D1 ⊑ D2 , if (i) Catas 1 is a subconjunction of Catas 2 ,
and (ii) D |= ∀(c1 → c2 ). Let ∆1 and ∆2 be two monovariant sets of definitions.
We say that ∆2 is an extension of ∆1 , written ∆1 ⊑ ∆2 , if for each D1 in ∆1
there exists D2 in ∆2 such that D1 ⊑ D2 .

    Given a set Cls of clauses and a set ∆ of definitions, the Define function (see
Figure 5) derives a set ∆′ of definitions that can be used for folding all clauses
in Cls. If ∆ is monovariant, then also ∆′ is monovariant. In particular, due to
the (Project) case, ∆′ contains a definition for each program predicate occurring
in the body of clauses in Cls. Due to the (Extend) case, ∆ ⊑ ∆′ .


Function Define(Cls, ∆): a set Cls of clauses; a monovariant set ∆ of definitions.
Define(Cls, ∆) returns a monovariant set ∆′ of new definitions computed as follows.
∆′ := ∆;
for each clause C: H ← c, G in Cls do
  for each program atom A in G do
      let CatasA be the conjunction of every catamorphism atom F in G such that
      adt-vars(A) ∩ adt-vars(F ) 6= ∅
      • (Skip) if in ∆′ there is a clause newp(U ) ← d, B, A, for any conjunction B
      of catamorphism atoms, such that: (i) CatasA is a subconjunction of B, and
      (ii) D |= ∀(c → d), then skip;
      • (Extend) else if the definition for the predicate of A in ∆′ is the clause
      D: newp(U ) ← d, B, A, where B is a conjunction of catamorphism atoms, and
      either (i) CatasA is not a subconjunction of B, or (ii) D 6|= ∀(c → d), then
      introduce definition ExtD : extp(V ) ← α(d, c), A, B ′ , where: (i) extp is a new
      predicate symbol, (ii) V = vars({α(d, c), B ′ , A}), and B ′ is the conjunction of
      the distinct catamorphism atoms occurring either in B or in CatasA ;
      ∆′ := (∆′ \ {D}) ∪ {ExtD };
      • (Project) else if there is no clause in ∆′ of the form K ← d, B, A, for any
      conjunction B of catamorphism atoms,
      then introduce definition D: newp(U ) ← π(c, I), A, CatasA , where: (i) newp
      is a new predicate symbol, (ii) I are the input variables of basic sort in
      {A, CatasA }, and (iii) U = vars({π(c, I), A, CatasA });
      ∆′ := ∆′ ∪ {D};

               S P ): a set ∆ = {D1 ,. . ., Dn } of definitions; a set P of definite clauses.
Function Unfold(∆,
Unfold(∆, P ) = n
                i=1 Ci , where Ci is the set of clauses derived by unfolding Di .

Function Strengthen (Cls, Q): a set Cls = {C1 , . . . , Cn } of clauses; a set Q of catamor-
phism-based queries, at most one query for each program predicate in Cls.
Strengthen (Cls, Q) = {Ei | Ei is derived from Ci by query-based strengthening using Q}
Function Fold(Cls, ∆): a set Cls = {C1 , . . . , Cn } of clauses; a monovariant set ∆ of
definitions.
Fold (Cls, ∆) = {Ei | Ei is derived from Ci by folding Ci using definitions in ∆}.

           Fig. 5: The Define, Unfold , Strengthen, and Fold functions.
12                           E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti

   The Unfold and Strengthen functions (see Figure 5) apply the unfolding and
query-based strengthening rules, respectively, to sets of clauses.
   Now, we define the operator τP,Q as follows:
              (
                Define(Q, ∅)                                   if ∆ = ∅
   τP,Q (∆) =
                Define(Strengthen(Unfold (∆, P ), Q), ∆)       otherwise
In the case where ∆ is the empty set of definitions, τP,Q (∆) introduces by the
Define function (Project case), a new definition for each program predicate oc-
curring in a query in Q. In the case where ∆ is not empty, τP,Q (∆) is an extension
of ∆ obtained by first unfolding all clauses in ∆, then applying the query-based
strengthening rule to the clauses derived by unfolding, and finally applying the
Define function.
    The Define function is parametric with respect to the generalization opera-
tor α (see the Extend case). In our implementation we use an operator based on
widening [11] that ensures stabilization, that is, for any infinite sequence c0 , c1 , . . .
of constraints and any sequence defined as (i) d0 = c0 , and (ii) dk+1 = α(dk , ck+1 ),
there exists m ≥ 0 such that dm = dm+1 . The Strengthen function ensures that
there is a bound on the number of catamorphisms that can be present in a def-
inition. Since, as already mentioned, τP,Q is monotonic with respect to ⊑, its
                                       n
least fixpoint lfp(τP,Q ) is equal to τP,Q (∅), for some finite number n of iterations
of τP,Q . Note that, by construction, lfp(τP,Q ) is monovariant.
    Once we have computed the set lfp(τP,Q ) of definitions, we can use them
to fold all clauses derived by unfolding and strengthening by applying the Fold
function (see Figure 5). Thus, the transformation algorithm is defined as follows:
                                                                          
    Tmq (P, Q) = Fold Strengthen Unfold (lfp(τP,Q ), P ), Q , lfp(τP,Q )
Termination of Tmq follows immediately from the fact that lfp(τP,Q ) is computed
in a finite number of steps.
Theorem 2 (Termination of Algorithm Tmq ). Let P be a set of definite
clauses and Q a set of catamorphism-based queries. Then, Algorithm Tmq ter-
minates for P and Q.
   By the soundness and completeness of the transformation rules (see Theo-
rem 1), we also get the following result.
Theorem 3 (Soundness and Completeness of Algorithm Tmq ). For any
set P of definite clauses and Q of catamorphism-based queries, P ∪Q is satisfiable
if and only if Tmq (P, Q) is satisfiable.
    We conclude this section by showing the sequence of definitions for the pro-
gram predicate snoc computed by iterating the applications of τP,Q in the In-
sertion Sort example. The definitions in lfp(τP,Q ) are listed in Appendix 2.
     new 4(A, B, C, D, E, F, G) ← ordered (A, B), last(A, C, D), ordered (E, F ),
            snoc(A, G, E).
     new 5(A, B, C, D, E, F, G, H, I, J, K) ← ordered (E, J), last(E, F, G),
            ordered (A, D), first (E, H, I), first (A, B, C), snoc(E, K, A).
     new 13(A, B, C, D, E, F, G, H, I, J, K, L, M ) ← ordered (A, B), last (A, C, D),
            ordered (E, F ), last (E, G, H), first (E, J, K), first (A, L, M ), snoc(A, I, E).
     Note that these three definitions are in the ⊑ relation.
                                      Multiple Query Satisfiability of CHCs     13

7     Experimental Evaluation

We have implemented algorithm Tmq in a tool, called VeriCaTmq , which extends
VeriCaT [8] by guaranteeing a sound and complete transformation. VeriCaTmq is
based on (i) VeriMAP [7] for transforming CHCs, and (ii) SPACER (with Z3
4.11.2) to check the satisfiability of the transformed CHCs.
    We have considered 170 problems, as sets of CHCs, with 470 queries in total,
equally divided between the class of satisfiable (sat) problems and unsatisfiable
(unsat) ones (85 problems and 235 queries for each class). These problems are
related to programs that manipulate: (i) lists of integers by performing con-
catenation, permutation, reversal and sorting, and (ii) binary search trees, by
inserting and deleting elements. For list manipulating programs, we have con-
sidered properties such as: list length, minimum and maximum element, sum
of elements, list content as sets or multisets of elements, and list sortedness (in
ascending or descending order). For trees, we have considered size, height, min-
imum and maximum element, tree content and the binary search tree property.
    The problems considered here are derived from those of the benchmark set
of previous work [8] with some important differences. We have considered addi-
tional satisfiable problems (for instance, those related to Heapsort). In addition
to satisfiable problems, we have also considered unsatisfiable problems that have
been obtained from their satisfiable counterparts by introducing bugs in the
programs: for instance, by not inserting an element in a list, or adding an ex-
tra constraint, or replacing a non-empty tree by an empty one. Note also that
the transformed CHCs produced by Tmq contain both basic variables and ADT
variables, whereas those produced by the method presented in previous work [8]
contain basic variables only.
    For comparing the effectiveness of our method with that of a state-of-the-art
CHC solver, we have also run SPACER (with Z3 4.11.2) on the original, non-
transformed CHCs, in SMT-LIB format. In Table 1 we summarize the results
of our experiments4. The first three columns report the name of the program,
the total number of problems and queries for each program. The fourth and
fifth columns report the number of satisfiable and unsatisfiable problems proved
by SPACER before transformation, whereas the last two columns report the
number of satisfiable and unsatisfiable problems proved by VeriCaTmq .
    In summary, VeriCaTmq was able to prove all the 170 considered problems
whereas SPACER was able to prove the properties of 84 ‘unsat’ problems out
of 85, and none of the ‘sat’ problems. The total time needed for transforming
the CHCs was 275 seconds (1.62 s per problem, on average), and checking the
satisfiability of the transformed CHCs took about 174 s in total (about 1s average
time, 0.10 s median time). For comparison, SPACER took 30.27 s for checking
the unsatisfiability of 84 problems (0.36 s average time, 0.15 s median time). The
benchmark and the tool are available at https://fmlab.unich.it/vericatmq.

4
    Experiments have been performed on an Intel Xeon CPU E5-2640 2.00GHz with
    64GB RAM under CentOS with a time limit of 300s per problem.
14                      E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti

      Program                  Problems Queries    SPACER       VeriCaTmq
                                                  sat unsat     sat unsat
      List Membership                 2       6     0       1     1       1
      List Permutation                8      24     0       4     4       4
      List Concatenation             18      18     0       8     9       9
      Reverse                        20      40     0      10    10      10
      Double Reverse                  4      12     0       2     2       2
      Reverse w/Accumulator           6      18     0       3     3       3
      Bubblesort                     12      36     0       6     6       6
      Heapsort                        8      48     0       4     4       4
      Insertionsort                  12      24     0       6     6       6
      Mergesort                      18      84     0       9     9       9
      Quicksort (version 1)          12      38     0       6     6       6
      Quicksort (version 2)          12      36     0       6     6       6
      Selectionsort                  14      42     0       7     7       7
      Treesort                        4      20     0       2     2       2
      Binary Search Tree             20      24     0      10    10      10
      Total                         170     470     0      84    85      85
     Table 1: Programs and problems proved by SPACER and VeriCaTmq .

     For instance, for all the considered list sorting programs (Bubblesort, Heap-
sort, Insertionsort, Mergesort, Quicksort, Selectionsort and Treesort), VeriCaTmq
was able to prove properties stating that the output list is sorted and has the
same multiset of elements of the input list. Similarly, VeriCaTmq was able to
prove that those properties do not hold, if extra elements are added to the out-
put list, or some elements are not copied from the input list to the output list,
or a wrong comparison operator is used.
     The results obtained by the VeriCaTmq prototype implementation of our
method are encouraging and show that, when used in combination with state-
of-the-art CHC solvers, it can greatly improve their effectiveness to prove sat-
isfiability of sets of CHCs with multiple queries, while it does not inhibit their
remarkable ability to prove unsatisfiability, although some extra time due to
transformation may be required.


8    Conclusions and Related Work
Many program verification problems can be translated into the satisfiability
problem for sets of CHCs that include more than one query. A notable example is
the case where we want to verify the correctness of programs made out of several
functions, each of which has its pre-/postconditions [13]. We have proposed an
algorithm, called Tmq , for transforming a set of CHCs with multiple queries into
a new, equisatisfiable set of CHCs that incorporate suitable information about
the set of queries contained in the initial set. The advantage gained is that, in
order to prove the satisfiability of the transformed CHCs, the CHC solver may
exploit the mutual interactions among the satisfiability proofs of the various
queries. We have identified a class of queries that specify program properties
using catamorphisms on ADTs, such as lists and trees, for which Tmq terminates.
                                       Multiple Query Satisfiability of CHCs      15

We have implemented algorithm Tmq and shown that it improves the effectiveness
of the state-of-the-art CHC solver SPACER [18] on a non trivial benchmark.
    Algorithm Tmq improves over the transformation algorithm Tcata presented
in a previous paper [8], which works by eliminating ADTs from sets of CHCs.
Instead of the contracts handled by Tcata , algorithm Tmq considers queries, and
thus its input is simply a set of CHCs. More importantly, Tmq is sound and com-
plete, in the sense that the initial and transformed CHCs are equisatisfiable sets,
whereas Tcata is only sound (that is, it can be seen as computing an abstraction
of the initial clauses), and thus if the transformed clauses are unsatisfiable we
cannot infer anything about the satisfiability of the initial CHCs. Completeness
is very important in practice, because proving that a set of clauses is unsatisfiable
and finding a counterexample can help identify a program bug. The experimental
evaluation reported in Section 7 shows that our transformation-based verifica-
tion technique is able to dramatically improve the effectiveness of the SPACER
solver for satisfiable sets of CHCs (where the results of SPACER are very poor),
while retaining the excellent results of the solver for unsatisfiable sets of CHCs
(for which SPACER is, at least in principle, complete).
    Decision procedures for suitable classes of first order formulas defined on
catamorphisms [21, 22] have been used in program verifiers [23]. However, we do
not propose here any specific decision procedure for catamorphisms and, instead,
we transform a set of CHCs with catamorphisms into a new set of CHCs where
catamorphisms are, in a sense, compiled away.
    Type-based norms, which are a special kind of integer-valued catamorphisms,
were used for proving termination of logic programs [5] and for resource analy-
sis [1] via abstract interpretation. Similar abstract interpretation techniques are
also implemented in the CiaoPP preprocessor [14] of the Ciao logic program-
ming system. In our approach we do not need to specify a priory any abstract
domain where to perform the analysis, and instead, by transformation, we gener-
ate new CHCs which incorporate the relations defined by the constraints on the
catamorphisms. The problem of showing the satisfiability of CHCs defined on
ADTs is a very hot topic and various approaches have been proposed in recent
work, including: (i) a proof system that combines inductive theorem proving
with CHC solving [25], (ii) lemma generation based on syntax-guided synthesis
from user-specified templates [26], (iii) invariant discovery based on finite tree
automata [19], and (iv) use of suitable abstractions [12].
    A limitation of our approach is that the effectiveness of the transformation
may depend on the set of properties specified through the queries. For instance,
it may happen that programmers provide partial program specifications (e.g., for
a subset of the program functions), and therefore queries only for some program
predicates, such as the main program predicates (e.g., ins--sort and ord --ins of
our example). In this case, it is essential to have a mechanism that is able to
infer from the queries the unspecified catamorphisms for the remaining program
predicates (e.g., append and snoc which ins--sort and ord --ins depend on). As
future work, we plan to extend Tmq to propagate the catamorphisms specified in
the queries to those program predicates for which no query has been specified.
16                        E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti

References
 1. E. Albert, S. Genaim, R. Gutiérrez, and E. Martin-Martin. A transformational
    approach to resource analysis with typed-norms inference. Theory Pract. Log.
    Program., 20(3):310–357, 2020.
 2. C. W. Barrett, R. Sebastiani, S. A. Seshia, and C. Tinelli. Satisfiability mod-
    ulo theories. In Handbook of Satisfiability, volume 185 of Frontiers in Artificial
    Intelligence and Applications, pages 825–885. IOS Press, 2009.
 3. N. Bjørner, A. Gurfinkel, K. L. McMillan, and A. Rybalchenko. Horn clause solvers
    for program verification. In Fields of Logic and Computation (II), Lecture Notes
    in Computer Science 9300, pages 24–51. Springer, 2015.
 4. M. Blicha, G. Fedyukovich, A. E. J. Hyvärinen, and N. Sharygina. Transition
    power abstractions for deep counterexample detection. In Tools and Algorithms
    for the Construction and Analysis of Systems, TACAS ’22, Part I, Lecture Notes
    in Computer Science 13243, pages 524–542. Springer, 2022.
 5. M. Bruynooghe, M. Codish, J. P. Gallagher, S. Genaim, and W. Vanhoof. Termi-
    nation analysis of logic programs through combination of type-based norms. ACM
    Transactions on Programming Languages and Systems, 29(2):10–es, 2007.
 6. E. De Angelis, F. Fioravanti, J. P. Gallagher, M. V. Hermenegildo, A. Pettorossi,
    and M. Proietti. Analysis and transformation of constrained Horn clauses for
    program verification. Theory and Practice of Logic Programming, 22(6):974–1042,
    2022.
 7. E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti. VeriMAP: A tool
    for verifying programs through transformations. In Tools and Algorithms for the
    Construction and Analysis of Systems, TACAS ’14, Lecture Notes in Computer
    Science 8413, pages 568–574. Springer, 2014.
 8. E. De Angelis, M. Proietti, F. Fioravanti, and A. Pettorossi. Verifying cata-
    morphism-based contracts using constrained Horn clauses. Theory and Practice
    of Logic Programming, 22(4):555–572, 2022.
 9. S. Etalle and M. Gabbrielli. Transformations of CLP modules. Theoretical Com-
    puter Science, 166:101–146, 1996.
10. G. Fedyukovich and P. Rümmer. Competition report: CHC-COMP-21. In 8th
    Workshop on Horn Clauses for Verification and Synthesis, volume 344 of EPTCS,
    pages 91–108. Open Publishing Association, 2021.
11. F. Fioravanti, A. Pettorossi, M. Proietti, and V. Senni. Generalization strategies
    for the verification of infinite state systems. Theory and Practice of Logic Pro-
    gramming, 13(2):175–199, 2013.
12. H. Govind V. K., S. Shoham, and A. Gurfinkel. Solving constrained Horn clauses
    modulo algebraic data types and recursive functions. Proceedings of the ACM on
    Programming Languages, POPL ’22, 6:1–29, 2022.
13. S. Grebenshchikov, N. P. Lopes, C. Popeea, and A. Rybalchenko. Synthesizing
    software verifiers from proof rules. In Conference on Programming Language Design
    and Implementation, PLDI ’12, pages 405–416, 2012.
14. M. V. Hermenegildo, G. Puebla, F. Bueno, and P. López-García. Integrated pro-
    gram debugging, verification, and optimization using abstract interpretation (and
    the Ciao system preprocessor). Science of Computer Programming, 58(1–2):115–
    140, 2005.
15. R. Hinze, N. Wu, and J. Gibbons. Unifying structured recursion schemes. In
    International Conference on Functional Programming, ICFP ’13, pages 209–220.
    ACM, 2013.
                                      Multiple Query Satisfiability of CHCs      17

16. H. Hojjat and P. Rümmer. The ELDARICA Horn solver. In Formal Methods in
    Computer Aided Design, FMCAD ’18, pages 1–7. IEEE, 2018.
17. J. Jaffar and M. Maher. Constraint logic programming: A survey. Journal of Logic
    Programming, 19/20:503–581, 1994.
18. A. Komuravelli, A. Gurfinkel, and S. Chaki. SMT-based model checking for recur-
    sive programs. Formal Methods in System Design, 48(3):175–205, 2016.
19. Y. Kostyukov, D. Mordvinov, and G. Fedyukovich. Beyond the elementary rep-
    resentations of program invariants over algebraic data types. In Conference on
    Programming Language Design and Implementation, PLDI ’21, pages 451–465.
    ACM, 2021.
20. E. Meijer, M. M. Fokkinga, and R. Paterson. Functional programming with ba-
    nanas, lenses, envelopes and barbed wire. In 5th ACM Conference Functional
    Programming Languages and Computer Architecture, Lecture Notes in Computer
    Science 523, pages 124–144. Springer, 1991.
21. T. Pham, A. Gacek, and M. W. Whalen. Reasoning about algebraic data types
    with abstractions. Journal of Automated Reasoning, 57(4):281–318, 2016.
22. P. Suter, M. Dotta, and V. Kuncak. Decision procedures for algebraic data
    types with abstractions. In Symposium on Principles of Programming Languages,
    POPL ’10, pages 199–210. ACM, 2010.
23. P. Suter, A. S. Köksal, and V. Kuncak. Satisfiability modulo recursive programs.
    In Symposium on Static Analysis, SAS ’11, Lecture Notes in Computer Science
    6887, pages 298–315. Springer, 2011.
24. H. Tamaki and T. Sato. A generalized correctness proof of the unfold/fold logic
    program transformation. Technical Report 86-4, Ibaraki University, Japan, 1986.
25. H. Unno, S. Torii, and H. Sakamoto. Automating induction for solving Horn
    clauses. In Computer Aided Verification, CAV ’17, Part II, Lecture Notes in Com-
    puter Science 10427, pages 571–591. Springer, 2017.
26. W. Yang, G. Fedyukovich, and A. Gupta. Lemma synthesis for automating in-
    duction over algebraic data types. In International Conference on Principles and
    Practice of Constraint Programming, CP 2019, Lecture Notes in Computer Science
    11802, pages 600–617. Springer, 2019.
18                       E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti

Appendix 1
In this appendix we present a proof sketch of Theorem 1 that states the soundness
and completeness of the transformation rules.
Proof sketch. The proof of Theorem 1 is based on the correctness of the transfor-
mation rules for (constraint) logic programs [9, 24]. In particular, the addition of
catamorphisms performed by the query-based strengthening rule, is sound and
complete because the catamorphisms are total, functional relations. The cor-
rectness of folding is proved by using a method similar to the one introduced by
Tamaki and Sato [24], which relies on two facts: (i) we can associate predicates
with levels where program predicates have a higher level than catamorphisms,
and (ii) only clauses obtained by unfolding with respect to a program atom are
folded.

Appendix 2
In this appendix let us first show the seven definitions that have been introduced
during the transformation of the given set of CHCs presented in Figures 2, 3,
and 4. Note that in our case, the constraints in these definitions are all true.
D1. new 1(A, B, C, D, E) ← ordered (A, B), ordered (C, D), ins--sort(A, E, C).
D2. new 2(A, B, C, D, E, F, G, H, I, J, K, L) ← ordered (A, B), ordered (C, D),
           ordered (E, F ), last (A, G, H), first(C, I, J), ord--ins(K, A, C, L, E).
     new 6(A, B, C, D) ← ordered (A, B), first(A, C, D).
     new 7(A, B, C, D, E, F, G, H, I, J, K, L, M, N ) ← first (A, B, C),
           ordered (A, D), last (E, F, G), first(H, I, J), ordered (H, K),
           first(E, L, M ), ordered (E, N ), append (E, A, H).
     new 13(A, B, C, D, E, F, G, H, I, J, K, L, M ) ← ordered (A, B),
           last (A, C, D), ordered (E, F ), last (E, G, H), first(E, J, K),
           first(A, L, M ), snoc(A, I, E).
     new 17(A, B) ← ordered (A, B).
D3. new 19(A, B, C, D) ← ordered (A, B), last (A, C, D), empty--list(A).
    Now we list the final set of CHCs which has been derived by our transforma-
tion technique using the above definitions. The first four CHCs are the queries
derived from the queries q1–q4 of Figure 4 denoting the four properties for Inser-
tion Sort we wanted to prove. We have that this final set of clauses is sastisfiable
and thus, the four properties are all valid.
E6. false ← ∼ (A ⇒ B), new 1(C, A, D, B, E).
     false ← ∼ ((A & B & ((C & D) ⇒ E ≤ F ) & (C ⇒ E ≤ G)) ⇒ H),
          new 2(I, A, J, B, K, H, C, E, D, F, G, L).
     false ← ∼ (A & B & ((C & D) ⇒ E ≤ F ) ⇒ G),
          new 7(H, D, F, B, I, C, E, J, K, L, G, M, N, A).
     false ← ∼ ((A & (B ⇒ C ≤ D)) ⇒ E), new 13(F,A,B,C,G,E,H,I,D,J,K,L,M ).
     new 1(A, B, A, B, [ ]) ← new 17(A, B).
E5. new 1(A, B, C, D, [E|F ]) ← (G&B & ((H &I) ⇒ J ≤ K) & (H ⇒ J ≤ E)) ⇒ D,
          new 2(L, G, A, B, C, D, H, J, I, K, E, F ), new 19(L, G, H, J).
                               Multiple Query Satisfiability of CHCs   19

new 2(A, B, [ ], C, D, E, F, G, H, I, J, K) ← C & ∼ H & I = 0 &
    ((B & (F ⇒ G ≤ J)) ⇒ L) & (L ⇒ E), new 1(M, L, D, E, K),
    new 13(A, B, F, G, M, L, N, O, J, P, Q, R, S).
new 2(A, B, [C|D], E, F, G, H, I, J, K, L, M ) ← (L ≤ C) &
    (E = (N ⇒ (C ≤ O & P ))) & J & K = C & ((B & (H ⇒ I ≤ L)) ⇒ Q) &
    ((Q & (R ⇒ S ≤ C)) ⇒ T ) & ((T & P & ((U & N ) ⇒ V ≤ O)) ⇒ W ) &
    (W ⇒ G), new 1(X, W, F, G, M ),
    new 7(D, N, O, P, Y, U, V, X, Z, A1, W, B1, C1, T ),
    new 13(D1, Q, R, S, Y, T, U, V, C, E1, F 1, G1, H1),
    new 13(A, B, H, I, D1, Q, R, S, L, I1, J1, K1, L1).
new 2(A, B, [C|D], E, F, G, H, I, J, K, L, M ) ← (L ≥ C +1) &
    (E = (N ⇒ (C ≤ O & P ))) & J & K = C & ((B & (H ⇒ I ≤ C)) ⇒ Q) &
    ((Q & P & (((R & N ) ⇒ S ≤ O) & (R ⇒ S ≤ L))) ⇒ G),
    new 2(T, Q, D, P, F, G, R, S, N, O, L, M ),
    new 13(A, B, H, I, T, Q, R, S, C, U, V, W, X).
new 6([ ], A, B, C) ← A & ∼ B & C = 0.
new 6([A|B],C,D,E) ← C = (F ⇒ (A ≤ G & H)) & D & E = A, new 6(B,H,F,G).
new 7(A,B,C,D,[ ],E,F,A,B,C,D,G,H,I) ← ∼ E & F = 0 & ∼ G & H = 0 & I,
   new6(A, D, B, C).
new 7(A,B,C,D,[E|F ],G,H,[E|I],J,K,L,M,N,O) ← G & H = ite(P, Q, E) &
   J & K = E & L = (R ⇒ (E ≤ S & T )) & M & N = E &
   O = (U ⇒ (E ≤ V & W )) & ((W & D & ((P & B) ⇒ Q ≤ C)) ⇒ T ),
   new7(A, B, C, D, F, P, Q, I, R, S, T, U, V, W ).
new 13([ ], A, B, C, [D], E, F, G, D, H, I, J, K) ← A & ∼ B & C = 0 &
   E = (L ⇒ (D ≤ M & N )) & F & G = ite(O, P, D) & H & I = D &
    ∼ J & K = 0 & N & ∼ L & M = 0 & ∼ O & P = 0.
new 13([A|B],C,D,E,[A|F ],G,H,I,J,K,L,M,N ) ← C = (O ⇒ (A ≤ P & Q)) &
   D & E = ite(R, S, A) & G = (T ⇒ (A ≤ U & V )) & H & I = ite(W, X, A) &
   K & L = A & M & N = A & ((Q & (R ⇒ S ≤ J)) ⇒ V ),
   new13(B, Q, R, S, F, V, W, X, J, T, U, O, P ).
new 17([ ], A) ← A.
new 17([A|B], C) ← C = (D ⇒ (A ≤ E & F )), new 6(B, F, D, E).
new 19([ ], A, B, C) ← A & ∼ B & C = 0.
