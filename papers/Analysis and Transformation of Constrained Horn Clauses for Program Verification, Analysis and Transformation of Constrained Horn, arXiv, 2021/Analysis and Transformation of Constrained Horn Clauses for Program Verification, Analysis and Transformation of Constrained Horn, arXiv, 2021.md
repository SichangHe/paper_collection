                                                 Under consideration for publication in Theory and Practice of Logic Programming                    1




                                                  Analysis and Transformation of Constrained Horn
                                                          Clauses for Program Verification∗
arXiv:2108.00739v1 [cs.LO] 2 Aug 2021




                                                  EMANUELE DE ANGELIS,1 FABIO FIORAVANTI,2 JOHN P. GALLAGHER,3,4
                                                       (e-mail: emanuele.deangelis@iasi.cnr.it, fioravanti@unich.it, jpg@ruc.dk)

                                             MANUEL V. HERMENEGILDO,4,5 ALBERTO PETTOROSSI,6,1 MAURIZIO PROIETTI 1
                                        (e-mail: manuel.hermenegildo@imdea.org, pettorossi@info.uniroma2.it, maurizio.proietti@iasi.cnr.it)

                                                       1 CNR-IASI, Rome, Italy, 2 DEC, University ‘G. d’Annunzio’, Chieti-Pescara, Italy
                                                          3 Roskilde University, Denmark, 4 IMDEA Software Institute, Madrid, Spain,
                                               5 Universidad Politécnica de Madrid (UPM), Spain, 6 DICII, University of Rome ‘Tor Vergata’, Italy


                                                             submitted 1 January 2003; revised 1 January 2003; accepted 1 January 2003



                                                                                             Abstract
                                                 This paper surveys recent work on applying analysis and transformation techniques that orig-
                                                 inate in the field of constraint logic programming (CLP) to the problem of verifying software
                                                 systems. We present specialisation-based techniques for translating verification problems for dif-
                                                 ferent programming languages, and in general software systems, into satisfiability problems for
                                                 constrained Horn clauses (CHCs), a term that has become popular in the verification field to re-
                                                 fer to CLP programs. Then, we describe static analysis techniques for CHCs that may be used for
                                                 inferring relevant program properties, such as loop invariants. We also give an overview of some
                                                 transformation techniques based on specialisation and fold/unfold rules, which are useful for
                                                 improving the effectiveness of CHC satisfiability tools. Finally, we discuss future developments
                                                 in applying these techniques.
                                                 Under consideration in Theory and Practice of Logic Programming (TPLP).

                                                 KEYWORDS: Program verification, program analysis, program transformation, constrained
                                                 Horn clauses, constraint logic programming.




                                                                                             Contents
                                                 1 Introduction                                                                                      2
                                                 2 Constrained Horn Clauses                                                                          4
                                                   2.1 Constraint Domains                                                                            5
                                                   2.2 Syntax of CHCs                                                                                9
                                                   2.3 Models of CHCs                                                                                9
                                                   2.4 Satisﬁability                                                                                10
                                                        2.4.1 Bottom-up procedures                                                                  11
                                                        2.4.2 Top-down procedures                                                                   12

                                                 ∗ Research partially funded by Spanish MICINN 2019-108528RB-C21 ProCode project, the Madrid
                                                   M141047003 N-GREENS and P2018/TCS-4339 BLOQUES-CM programs, and the Tezos Foundation.
2   E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

3 Semantics Preserving Transformations                                          16
  3.1 Fold/Unfold Transformations                                               16
  3.2 CHC Specialisation                                                        19
  3.3 Redundant Argument Removal                                                21
  3.4 Query-Answer Transformations                                              22
4 From Programs to Constrained Horn Clauses                                     23
  4.1 Semantics-driven Translation of Imperative Languages                      23
      4.1.1 Small-step speciﬁcation                                             23
      4.1.2 Big-step speciﬁcation                                               24
      4.1.3 Translation by specialisation                                       25
      4.1.4 Generating veriﬁcation conditions from semantics-based interpreters 26
  4.2 Translation via Proof Rules                                               27
  4.3 Abstract Compilation                                                      28
  4.4 Compiler-based Translation                                                28
  4.5 Translation of Source Language Annotations                                28
5 Analysis for Verification                                                     29
  5.1 Bottom-up Semantics-based Analysis                                        30
  5.2 Top-down Semantics-based Analysis                                         31
  5.3 Abstraction Reﬁnement                                                     37
6 Transformation for Verification                                               40
  6.1 Constraint Propagation by Specialisation                                  41
  6.2 Predicate Pairing                                                         46
      6.2.1 Relational veriﬁcation                                              46
      6.2.2 Solving CHCs over Algebraic Data Types                              49
  6.3 Other Transformation-based Techniques                                     51
      6.3.1 Reﬁnement based on tree automata                                    51
      6.3.2 Control-ﬂow reﬁnement by specialisation                             52
7 Related CHC-based Techniques                                                  53
8 Future Directions                                                             56




                                   1 Introduction
Program analysis and transformation has been an active research area since the early
days of logic programming. The attention to the topic in logic programming was origi-
nally due to the fact that program speciﬁcations are usually written as logical formulas
and from those formulas one can derive logic programs that are correct ‘by construction.’
When the implementation of eﬃcient Prolog programming systems became a central is-
sue, the main focus of program analysis and transformation shifted towards the discovery
of program properties based on program semantics and their use for optimising program
execution. Indeed, in many cases, logic programs can be transformed into new, eﬃcient
ones, by exploiting suitable program analyses, as done by some advanced logic program-
ming systems. However, it was realised early on that analysis and transformation were
Analysis and Transformation of Constrained Horn Clauses for Program Verification           3

useful also in program veriﬁcation and static debugging, as illustrated by the Ciao Prolog
system1 .
   During the past two decades, the application of these techniques to veriﬁcation has
expanded beyond logic programming to a large variety of other programming languages,
including imperative, functional, object-oriented, and concurrent ones. The main reason
is that logic programming, and more speciﬁcally Constraint Logic Programming (CLP),
is eﬀective as a language for specifying program semantics and program properties.
   For veriﬁcation applications, the term Constrained Horn Clauses (CHCs) is often used
in the literature instead of CLP when dealing with clauses that encode veriﬁcation prob-
lems, but are not intended to be directly executed as programs. Despite this pragmatic
diﬀerence, CHCs are syntactically and semantically the same as constraint logic pro-
grams. The underlying constraint theories of CHCs are typically those that axiomatize
data structures used in programming, such as booleans, integer numbers, real numbers,
bit vectors, arrays, heaps, and recursively deﬁned data structures such as lists and trees.
Eﬀective solvers for checking satisﬁability of sets of CHCs have been developed during
the last years. These solvers focus on constructing models in the theory of constraints;
however, proof-theoretic notions from CLP such as derivation trees, resolution, and refu-
tation are still applicable to CHCs.
   The ﬁrst step in CHC-based software veriﬁcation is the encoding of a veriﬁcation
problem in CHC form. Consider, for instance, the program fragment consisting of the
function deﬁnition in Figure 1. After the assignment sum = sum_upto(m), the location
sum will store the sum of the integers in the interval [0,m], if m≥0, and 0, if m<0:

                    int sum_upto(int x) {
                      int r = 0;
                      while (x > 0) {
                        r = r + x; x = x - 1; }
                      return r;
                    }
Figure 1. The function sum_upto.

Suppose that we want to prove the validity of the Hoare triple {m≥0} sum = sum_upto(m)
{sum≥m}, stating that, if m≥0 and the assignment sum = sum_upto(m) terminates, then
sum is assigned a value larger than or equal to m. This triple is valid if and only if the
following set of clauses, collectively called the verification conditions, is satisﬁable.
  1. false :- M>Sum, M>=0, sum_upto(M,Sum).
  2. sum_upto(X,R) :- R0=0, while(X,R0,R).
  3. while(X1,R1,R) :- X1>0, R2=R1+X1, X2=X1-1, while(X2,R2,R).
  4. while(X1,R1,R) :- X1=<0, R=R1.
Note that, in clause 1 above, we have that: (i) M>=0 is the precondition of the Hoare triple,
(ii) sum_upto(M,Sum) holds if and only if the evaluation of the function sum_upto on
the input integer M terminates and returns the integer Sum, and (iii) the constraint M>Sum
is the negation of the postcondition of the triple. As we will show later, CHC solvers can
show that this set of CHCs is indeed satisﬁable and hence the validity of the Hoare triple
is proven.

1 https://ciao-lang.org/ (Hermenegildo et al. 2012)
4   E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

  In this paper, we survey and discuss various aspects of this scenario, including the
derivation of the CHCs from imperative programs and Hoare triples, and techniques for
automatically checking their satisﬁability. Since satisﬁability of CHCs is undecidable,
a terminating automatic solver yields one of three answers: satisfiable, unsatisfiable or
unknown. An important goal of the techniques we discuss is to return a deﬁnite answer
(satisﬁable or unsatisﬁable) in as many cases as possible. We will show that many well-
established analysis and transformation techniques developed for CLP, as well as new
CHC-based approaches proposed in recent years to address veriﬁcation problems, are
eﬀective for achieving this goal.

   The paper is structured as follows. In Section 2 we present preliminary notions about
constraints, CHCs, their models, and some basic techniques for checking their satisﬁa-
bility, relating these techniques to the proof-theoretic and model-theoretic semantics of
CHCs. Much of this background was established in the ﬁeld of CLP.
   In Section 3, we present various CHC semantics-preserving transformation techniques,
based on CHC fold/unfold rules and specialisation transformations. Fold/unfold trans-
formations have been extensively studied in logic programming, and speciﬁcally in CLP.
They play an important role in veriﬁcation due to the fact that such transformations
preserve satisﬁability. Specialisation is a transformation that preserves satisﬁability with
respect to a particular goal.
   In Section 4, we present techniques for generating CHCs that encode veriﬁcation prob-
lems in other languages, focussing on imperative programming languages. We describe an
approach based on specialisation of semantics-based interpreters, and also survey other
approaches that have been applied in CHC solving tools.
   In Section 5, we describe techniques for CHC analysis applied to veriﬁcation. These
are derived mainly from the CLP literature, and in some cases directly yield a proof
of satisﬁability or unsatisﬁability; in other cases, analyses help with inferring relevant
program properties such as loop invariants. Static analysis also plays an important role
in guiding some CHC transformations, especially specialisation.
   Section 6 covers particular applications of transformation for veriﬁcation. These include
constraint propagation and strengthening. The section also presents transformations for
predicate pairing, with application to relational veriﬁcation and veriﬁcation problems
for abstract data types. We also summarise other transformation techniques such as
tree-automata based reﬁnement, and control-ﬂow reﬁnement.
   In Section 7, we give a brief overview of the use of analysis and transformation tech-
niques in some areas related to software veriﬁcation, such as model checking of inﬁnite
state systems and constraint-based automated testing.
   Finally, in Section 8 we discuss some developments in the area of CHC analysis and
transformation, which we believe worthy of future investigation.


                            2 Constrained Horn Clauses
Constrained Horn clauses are a class of ﬁrst-order logic formulas where the Horn clause
format is extended by the use of formulas of an arbitrary, possibly non-Horn, constraint
theory. A set of CHCs is also known as a program in CLP (Jaﬀar and Lassez 1987,
Jaﬀar and Maher 1994). As already mentioned, the term constrained Horn clauses is
Analysis and Transformation of Constrained Horn Clauses for Program Verification                         5

often used in the veriﬁcation context (Bjørner et al. 2015), where the focus is mainly
on the logical meaning, and in particular, on the construction of models for the clauses,
while the term CLP program refers additionally to the notion of execution which is based
on the procedural semantics of the clauses. In this survey, we will adhere to the CHC
terminology, although we will occasionally make use of the CLP terminology, especially
when referring to techniques that have been proposed in the CLP ﬁeld.
  In this section, we will recall the basic notions of constraints (Section 2.1), CHCs
(Section 2.2), and their models (Section 2.3). We will also present some techniques for
checking CHC satisﬁability (Section 2.4). We assume some familiarity with the elemen-
tary concepts of ﬁrst-order predicate logic (Enderton 1972, Mendelson 1997). For logic
programming notions not deﬁned here, we refer to standard publications (Apt 1990,
Lloyd 1987).


                                    2.1 Constraint Domains
Let L be a ﬁrst-order language with equality. Let the set of terms and formulas in L, be
denoted by T and F , respectively. They are constructed, as usual, starting from a set V
of variables, a set of function and predicate symbols (with arity), the logical connectives,
and the quantiﬁers. A function symbol of arity 0 is also called a constant. Given a formula
ϕ ∈ F, by vars(ϕ) we denote the set of the free variables occurring in ϕ. If vars(ϕ) = ∅,
we say that ϕ is a closed formula. If all variables occurring in ϕ are free, we say that ϕ
is a quantifier-free formula. We denote by ∃(ϕ) the existential closure of ϕ, and by ∀(ϕ)
the universal closure of ϕ. Let a substitution be a ﬁnite mapping from a set of variables
{X1 , . . . , Xm } ⊆ V to a set of terms {t1 , . . . , tm } ⊆ T , written as {X1 /t1 , . . . , Xm /tm }. We
assume that, for i = 1, . . . , m, Xi is diﬀerent from ti .
   A constraint domain D consists of the following components (Jaﬀar and Maher 1994).
(1) A signature Σ, that is, the subset of the function and predicate symbols of L used
     in D. We assume that the signature of any constraint domain D includes the predicate
     symbols true, false, and the equality symbol =. The terms of L using function symbols
     in Σ and variables are called Σ-terms. The formulas of L using symbols in Σ, variables,
     logical connectives, and quantiﬁers, are called Σ-formulas. Here we will omit the
     association of sorts to the symbols of Σ, as this issue is not relevant for the topics
     addressed in this paper. However, in some contexts, the use of many-sorted signatures
     is the standard (Barrett and Tinelli 2018).
(2) A subset C of Σ-formulas, called constraints. We assume that the atomic constraints
     true, false, and equalities between terms are in C. We also assume that C is closed
     under conjunction and existential quantiﬁcation.
(3) A constraint theory A, that is, a set of closed Σ-formulas, called axioms.
(4) A ﬁxed constraint interpretation D for the symbols in the signature Σ. As usual, D
     consists of a set U, called universe, together with functions and relations (with suit-
     able arities) on U that interpret the function and predicate symbols of Σ, respectively.
     The equality symbol is always interpreted as the identity on U. We assume that D
     is a model for A, and thus, for every closed Σ-formula ϕ, if A |= ϕ, then D |= ϕ. In
     many constraint domains, we will also have that, if D |= ϕ, then A |= ϕ (and hence
     A is a complete, decidable theory).
6   E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

(5) Functions for constraint satisfiability, entailment, and projection, deﬁned as follows.
   − A constraint solver, that is, a computable partial function, call it solv, which tests
      satisﬁability of any constraint c in D, that is, solv tells us whether or not D |= ∃(c)
      holds. We assume that solv is a total function whenever satisﬁability is decidable.
   − An entailment function, that is, a computable partial function, called entail, which
      tests whether or not, for any two constraints c1 and c2 , D |= ∀(c1 → c2 ) holds.
   − A projection function, that is, a computable partial function, called proj, which,
      given a constraint c and a ﬁnite set V ⊆ V of variables, computes the new constraint
      proj(c, V ), called the projection of c onto V , such that D |= ∀((∃X1 , . . . , Xm .c) ↔
      proj(c, V )), where {X1 , , . . . , Xm } = vars(c)\V . We assume that proj(c, V ) is a quan-
      tiﬁer-free formula whenever the constraint domain D admits quantifier elimination.
Now we present some of the constraint domains which are used in practice. In the liter-
ature one can ﬁnd slightly diﬀerent, yet equivalent, presentations of those domains. As
already stated, we assume that the signature Σ of every constraint domain includes the
predicate symbols true, false, and =.
Example 1
The constraint domain Bool of the Boolean constraints is deﬁned as follows. The signa-
ture Σ includes the function symbols 0, 1, ∼, ∗, +. For instance, ∼ 1 = x+0 is an atomic
constraint. The axioms of Bool are those of the Boolean algebra freely generated by 0
and 1. For instance, ∀x, y. x∗y = y∗x is the commutativity axiom for ∗. The constraint
interpretation B of Bool has the universe U = {false, true}. The symbols 0, 1, ∼, ∗, and +
are interpreted as false, true, negation, conjunction and disjunction, respectively. Satis-
ﬁability and entailment are decidable and they are tested as usual in Boolean algebras.
Projection is a total function. For instance, we have that B |= ∃x. (∼ 1 = x+0) holds, and
proj(∼ y = x+1, {y}) is the constraint y = 0.
Example 2
The constraint domain Integer of integer arithmetic is as follows. The signature Σ in-
cludes the following function symbols: all integer numbers, +, −, ×, and the predicate
symbols 6= and ≤. The axioms of Integer are Σ-formulas that can be derived from the ax-
ioms of Peano arithmetic (see, for instance, the paper by Wybraniec-Skardowska (2019))
and the references therein). The interpretation of the symbols of Integer is deﬁned as
expected over the universe Z of the integer numbers. Satisﬁability of constraints is un-
decidable, as they include the Diophantine equations (Matiyasevich 1970).
   The constraint domain LIA of linear integer arithmetic is derived from the domain
Integer by requiring that at least one of the two operands of × is an integer constant. The
fully quantiﬁed Σ-formulas of LIA are decidable, by extending Presburger’s algorithm.
The time complexity of the decision procedure is super-exponential with respect to the
size of the formula. The problem of checking satisﬁability of quantiﬁer-free formulas of
LIA is an NP-complete problem (Bradley and Manna 2007).
Example 3
The constraint domain F D of finite domains is related to the constraint domain LIA
and is deﬁned as follows (Jaﬀar and Maher 1994). The signature Σ of F D includes all
integer numbers, the binary function symbols +, −, the inﬁnitely many unary predicate
symbols ‘∈ [m, n]’ (one for each pair hm, ni of integers, with m at most n), and the binary
Analysis and Transformation of Constrained Horn Clauses for Program Verification               7

predicate symbols 6= and ≤. The interpretation of the atomic constraint x ∈ [m, n] over
the universe Z is x ∈ {m, m+1, . . . , n}. For instance, x6= 4 ∧ x∈[2, 5] is a constraint in F D.
As for LIA, we have that for F D the fully quantiﬁed Σ-formulas are decidable and
satisﬁability of the quantiﬁer-free Σ-formulas is NP-complete.

Example 4
The constraint domain Real of real arithmetic is deﬁned as follows. The signature Σ
includes the following function symbols: all rational numbers, +, −, ×, and the predicate
symbols < and ≤. The axioms of Real are those of an ordered, real closed ﬁeld (Shoenﬁeld
1967). The interpretation of the function and predicate symbols of Real is the expected
one over the universe R of the real numbers. Satisﬁability is decidable and there exists a
constraint solver for Real (Jaﬀar et al. 1992, Barrett and Tinelli 2018).
   The constraint domain LRA of linear real arithmetic is derived from the domain Real
by requiring that at least one of the two operands of × is a rational constant. Satisﬁability
of LRA constraints can be computed using Fourier-Motzkin elimination (Schrijver 1998).
If we consider the universe Q of the rational numbers, instead of R, from the domain
Real we get the domain Q of rational arithmetic, and from the domain LRA we get the
domain LQA of linear rational arithmetic. LRA and LQA are two elementary equivalent
structures (Shoenﬁeld 1967), and thus a solver for LRA is also a solver for LQA, and
vice versa.

Example 5
The constraint domain EUF of Equality of Uninterpreted Functions is a domain deﬁned as
follows. The signature Σ includes a set {f0 , . . . , fk } of function symbols and the predicate
symbol 6= 2. The axioms are those for =, that is, reﬂexivity, symmetry, transitivity, and
function congruence (that is, ∀x, y. x = y → f (x) = f (y)), together with the axiom for 6= :
∀x, y. x 6= y ↔ ¬(x = y). The universe of the interpretation is the set T of finite trees.
The 0-ary function symbol a is interpreted as a tree made out of the single node a,
and the n-ary (with n > 0) function symbol f is interpreted as the mapping that, given
the trees that are the interpretations of the n arguments of f , returns a tree having f
as root and the n trees as children of the root. The satisﬁability of conjunctions of
quantiﬁer-free Σ-formulas of EUF can be decided in polynomial time by congruence
closure algorithms (Jaﬀar and Maher 1994, Bradley and Manna 2007). For instance, we
have that T 6|= f (f (f (a))) = a ∧ f (f (a)) = a ∧ f (a) 6= a. Indeed, the ﬁrst two conjuncts
imply f (a) = a.

Example 6
The constraint domain Term is deﬁned as follows. The signature Σ includes a given set of
function symbols. The axioms of Term are the usual ones for = (see Example 5), together
with the axioms speciﬁc of the Clark Equality Theory (Clark 1978)). In particular, (i) for
all distinct function symbols f and g, for all tuples u and v of terms, ¬ (f (u)= g(v)), and
(ii) for all terms t and t′ , if t is a proper subterm of t′ , then ¬(t = t′ ). As for EUF, the
universe of the interpretation is the set of finite trees. The unification algorithm deﬁnes
a total constraint solver for quantiﬁer-free formulas in the domain Term (Apt 1990).

2 We  can do without extra predicate symbols in favour of new function symbols as indicated
  by Barrett and Tinelli (2018).
8   E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

  There is a variant of the constraint domain Term that takes as universe, instead of the
set of ﬁnite trees, the set of rational trees, that is, the set of all (ﬁnite or inﬁnite) trees, each
tree having a finite set of (ﬁnite or inﬁnite) subtrees (Colmerauer 1982). This extension
of the domain Term from ﬁnite trees to rational trees, call it TermRat , has been the
ﬁrst step made towards the integration of a constraint domain into logic programming.
Indeed, when performing uniﬁcation between atoms, the equalities between rational trees
are manipulated as constraints in CHCs. In TermRat , satisﬁability of quantiﬁer-free
formulas is decidable and a constraint solver is a uniﬁcation algorithm that does not
perform the occur-check (Jaﬀar 1984). In particular, the uniﬁcation between a variable x
and a non-variable term containing x always succeeds.

Example 7
The constraint domain Array is the domain of the arrays as commonly used in program-
ming. The signature of Array includes the read and write function symbols for denoting,
respectively, the reading of an array at an index position, and the writing of an element
in an array at an index position. The axioms of Array are the usual ones for equality
between indexes and equality between elements, together with the following two axioms:
for all arrays a, elements v, indexes i and j,
(1) i = j → read(write(a, i, v), j) = v, and (2) i 6= j → read(write(a, i, v), j) = read(a, j)
Satisﬁability of fully quantiﬁed formulas in the Array domain is undecidable. However,
there are suitably restricted classes of Array formulas in which it is decidable (Bradley and Manna
2007, Alberti et al. 2015).

   Since in practice many veriﬁcation problems deal with programs that manipulate
diﬀerent data types, an important theoretical and practical aspect of the use of con-
straint domains is the combination of solvers relative to diﬀerent constraint domains
(Nelson and Oppen 1979, Barrett and Tinelli 2018)
   Many Prolog systems support constraint solving by including selectable solvers as li-
braries, in the CLP(X ) spirit, such as F D (B-Prolog, Ciao, ECLiPSe, GNU, SICStus,
and SWI), Bool (B-Prolog, GNU, SICStus, SWI), Q and Real (Ciao, ECLiPSe, SIC-
Stus, SWI, XSB), and Sets (B-Prolog, ECLiPSe), among others. Also, many Prolog
systems (e.g., Ciao, ECLiPSe, SICStus, SWI, XSB, YAP) support Constraint Handling
Rules (CHR), a committed-choice rule-based language designed for writing constraint
solvers (Frühwirth 1998). This brings support for additional constraint domains or al-
ternative implementations. Finally, the Parma Polyhedral Library (Bagnara et al. 2008)
provides several Prolog systems (Ciao, GNU, SICStus, SWI, XSB, Yap) with the imple-
mentation of primitives, such as widening and convex-hull, for constraint manipulation
over various subdomains of the domain Real, including boxes, bounded diﬀerences, oc-
tagons, and convex polyhedra.
   Constraint solvers for several constraint domains have also been developed using tech-
niques of Satisfiability Modulo Theories (SMT), which build upon various decision pro-
cedures for ﬁrst-order theories and very eﬃcient algorithms for propositional satisﬁa-
bility (Barrett and Tinelli 2018). Constraint solvers based on that approach are called
SMT solvers, and have their main applications in the ﬁeld of program veriﬁcation. For
that reason they focus on constraint domains that formalise data types often used
in programming, such as Booleans, integer and ﬂoating point numbers, bit vectors,
Analysis and Transformation of Constrained Horn Clauses for Program Verification                   9

and arrays. Among other SMT solvers, we have CVC4 (Barrett et al. 2011), Eldar-
ica (Hojjat and Rümmer 2018), MathSAT (Cimatti et al. 2013), Yices (Dutertre 2014),
and Z3 (de Moura and Bjørner 2008, Komuravelli et al. 2013). An important initiative
is SMT-LIB (Barrett et al. 2016), which has the goals of proposing common languages
and interfaces for SMT solvers and constructing a library of benchmarks.


                                        2.2 Syntax of CHCs
Let D be a constraint domain with signature Σ, subset of the ﬁrst-order language L. Let
Predu be a set of the predicate symbols of L which do not belong to Σ. Predu is called the
set of the user-defined predicate symbols. Let C be the set of constraints of D. An atom is
an atomic formula p(t1 , . . . , tm ), where p is a predicate symbol in Predu and t1 , . . . , tm are
Σ-terms. Let Atom be the set of all atoms. A constrained Horn clause (CHC) (or simply, a
clause) is a universally quantiﬁed implication of the form: ∀(c ∧ A1 ∧ . . . ∧ An → H) whose
premise (or body) is the conjunction of a constraint c and n (≥ 0) atoms A1 , . . . , An ,
and whose conclusion (or head) H is either an atom or false. We will use the logic
programming notation and we will write a clause as H ← c, A1 , . . . , An . In the examples
we will also adopt the usual Prolog notation and, in particular, the symbol ‘←’ will be
replaced by ‘:-’.
   A constrained goal (or simply, a goal) is a clause of the form: false ← c, A1 , . . . , An .
A definite clause is a clause whose conclusion is an atom. A constrained fact (or simply,
a fact) is a deﬁnite clause of the form: H ← c. A clause D (or a set P of clauses) is said
to be over C in case we want to stress that the constraints occurring in D (or in P )
belong to the set C of constraints. A clause H ← c, A1 , . . . , An is said to be linear if n ≤ 1,
and nonlinear otherwise. Given a set P of clauses, we say that predicate p immediately
depends on a predicate q if in P there is a clause of the form: p(...) ← c, A1 , . . . , An such
that q occurs in one of the atoms A1 , . . . , An . The relation depends on between predicates
is the transitive closure of the relation immediately depends on.


                                        2.3 Models of CHCs
Let D be a constraint domain, where D is the ﬁxed interpretation for the constraint
signature Σ and U is the universe of D. Without loss of generality, we assume that
for every element in U there is a corresponding constant in the signature Σ and in L
(indeed, we can always extend Σ and L by adding new constants). A valuation σ for D is
a mapping from V to U, and its extension that maps terms to U and formulas to closed
formulas, based on the replacement of every free variable occurrence X by σ(X). The
D-base for L, denoted BD , is the set {σ(A) | A ∈ Atom and σ is a valuation for D}.
   A D-interpretation is an interpretation of L that agrees with the interpretation D on
the symbols of Σ. A D-interpretation I can be identiﬁed with the following subset of BD :
  {p(a1 , . . . , am ) ∈ BD | pI (a1 , . . . , am ) holds in I}
where pI denotes the m-ary relation on Um that interprets the symbol p in I. Given any
set F of formulas, a D-interpretation M is a D-model of F , written M |= F , if, for all
formulas ϕ ∈ F , M |= ϕ holds, that is, ϕ is true in M. F is D-satisfiable if it has a D-
model. We will often say satisfiable, instead of D-satisfiable, when the speciﬁc constraint
10 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

domain D is irrelevant or understood from the context. We write D |= F if, for every
D-interpretation M, M |= F holds.
  Every set P of deﬁnite CHCs is D-satisﬁable and has a least (with respect to set
inclusion) D-model, denoted lm(P, D) (Jaﬀar and Maher 1994). Thus, if Q is any set of
constrained goals, then P ∪ Q is D-satisﬁable if and only if lm(P, D) |= Q.
  When presenting satisﬁability procedures, it will be convenient to consider false as a
user-deﬁned predicate, so that P ∪ Q is a set of deﬁnite CHCs, and hence lm(P ∪ Q, D)
exists. Thus, we will say, with a slight abuse of language, that P ∪ Q is satisﬁable if and
only if false does not belong to lm(P ∪ Q, D), written false 6∈ lm(P ∪ Q, D).
  If the constraint theory A of D is complete, we also have that P ∪ Q is D-satisﬁable if
and only if P ∪ Q ∪ A 6⊢ false.
  A D-interpretation I is represented by a set bI of constrained facts if, for all predicates
p∈Pred u , p(a1 , . . . , am ) ∈ I if and only if, for some constrained fact p(X1 , . . . , Xm ) ← c in bI,
we have that D |= σ(proj(c, {X1 , . . . , Xm })), where σ is a valuation that maps X1 , . . . , Xm
to a1 , . . . , am . In general, a D-interpretation may be represented by more than one (ﬁnite
or inﬁnite) set of constrained facts. On the other hand, a set of constrained facts rep-
resents a unique D-interpretation. We will extend the terminology and notation deﬁned
for D-interpretations to their representation as sets of constrained facts. In particular,
we deﬁne bI ⊆ b      J if I ⊆ J.
  For instance, given the following CHCs over LIA :
  p(X) :- X=0.
  p(X) :- X=Y+1, p(Y).

The least LIA-model of these CHCs is the inﬁnite set {p(0), p(1),...}, which is
represented by the set {p(X) :- X>=0.} of one constrained fact only.
  Most of the satisﬁability techniques work on D-interpretations that can be repre-
sented by finite sets of constrained facts. Such interpretations are said to be D-definable
(Bjørner et al. 2015). If a set S of CHCs has a D-deﬁnable model, then S is said to be
solvable, and the model is said to be a solution for S. Clearly, if S is solvable, then S is
D-satisﬁable. In general, the converse does not hold: there exist sets of CHCs that are
D-satisﬁable, and yet they do not have any D-deﬁnable models (see Section 6.2 for an
example).




                                         2.4 Satisfiability

The reasoning task for CHCs which is most relevant to program veriﬁcation applications is
checking their satisﬁability. We call CHC solvers the tools implementing methods for solv-
ing this task. Unfortunately, as a consequence of classical computability results (Tärnlund
1977), the problem of checking the satisﬁability of a set of CHCs is undecidable, and hence
only incomplete methods can be found. Here we will brieﬂy present two kinds of pro-
cedures which are the basis of many methods for checking satisﬁability: (i) bottom-up
procedures, and (ii) top-down procedures.
Analysis and Transformation of Constrained Horn Clauses for Program Verification 11

                                2.4.1 Bottom-up procedures
Given a constraint domain D, a set P of deﬁnite CHCs over D, and a set Q of constrained
goals over D, we have that P ∪ Q is D-satisﬁable if and only if the set Q of constrained
goals holds in the least D-model lm(P, D) (see Section 2.3).
   Bottom-up procedures for checking the satisﬁability of P ∪ Q are based on the least
ﬁxpoint characterisation of the least D-model of P , which allows us to construct lm(P, D)
as the least upper bound of a sequence of D-interpretations that under-approximate
lm(P, D), starting from the empty set, by making forward inferences (that is, using clauses
as implications for inferring new atoms to be added to the current D-interpretation).
   Indeed, the least D-model lm(P, D) can be computed as the least ﬁxpoint of a func-
tion, denoted TPD , which given a D-interpretation returns a new D-interpretation. This
function is called the immediate consequence operator for P , and it is deﬁned as follows:
     TPD (I) = {σ(H) | H ← c, A1 , . . . , An ∈ P ∧ σ is a valuation for D ∧ D |= σ(c) ∧
                       ∧ {σ(A1 ), . . . , σ(An )} ⊆ I}
Since TPD is a continuous function on the complete partial order (2BD , ⊆), it has a least
                                                                            S
ﬁxpoint lfp(TPD ) (Tarski 1955). This ﬁxpoint is the least upper bound i≥0 TPD ↑ i of the
sequence TPD ↑0 ⊆ TPD ↑1 ⊆ TPD ↑2 ⊆ . . . of D-interpretations, also called a Kleene sequence,
where TPD ↑ i stand for (TPD )i (∅), for all i ≥ 0.
  It can be shown that lfp(TPD ) = lm(P, D) (Jaﬀar et al. 1998).
Example 8
Let D be the constraint domain Integer and let P be the following set of clauses over D:
  C1.       p(X+3,X) :- X<3.
  C2.       p(X+3,Y) :- X>3, p(X,Y).
It can be shown by induction that the bottom-up computation of lfp(TPD ) constructs the
following Kleene sequence of D-interpretations:
  TPD ↑ 0      = ∅
  TPD ↑ 1      = {p(X+3,X) | X<3}
  TPD ↑(k+1)= {p(X+3(k+1),X) | 0<X<3} ∪ TPD ↑ k              for all k>0
whose least upper bound is:
                                    S
  lfp(TPD ) = {p(X+3,X) | X<3} ∪        k>0 {p(X+3(k+1),X) | 0<X<3} = lm(P, D).
   The construction of lfp(TPD ) can be used as the basis for checking the satisﬁability of
P ∪ Q. By the continuity of TPD , any goal in Q is false in lfp(TPD ) if and only if it is
false in TPD ↑ i, for some i ≥ 0. Thus, a bottom-up procedure which computes lfp(TPD ) by
constructing the Kleene sequence, is sound and complete for showing the unsatisﬁability
of P ∪ Q. However, if P ∪ Q is satisﬁable, then the construction of the Kleene sequence
may not terminate (recall that satisﬁability is not even semidecidable). In this case, in
order to prove satisﬁability, one should prove that Q is true in TPD ↑ i, for i ≥ 0, by some
method diﬀerent from direct inspection of lfp(TPD ), e.g., by the abstract interpretation
methods presented in Section 5, which compute an over-approximation of lfp(TPD ). In the
next example we use a method based on induction on i.
Example 9
Let D be the constraint domain Integer. Let us consider the following CHCs over D we
have introduced in Section 1:
12 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

  1. false :- M>Sum, M>=0, sum_upto(M,Sum).
  2. sum_upto(X,R) :- R0=0, while(X,R0,R).
  3. while(X1,R1,R) :- X1>0, R2=R1+X1, X2=X1-1, while(X2,R2,R).
  4. while(X1,R1,R) :- X1=<0, R=R1.
As already mentioned, (i) these clauses encode the veriﬁcation problem for the program
fragment of Figure 1 in the sense that the triple {m≥0} sum = sum_upto(m) {sum≥m}
holds if and only if they are D-satisﬁable, and (ii) these clauses are D-satisﬁable if and
only if goal 1 holds in lfp(TPD ), where P is the set made out of clauses 2–4.
   It can be shown by induction that the bottom-up computation of lfp(TPD ) constructs
the following Kleene sequence of D-interpretations:
  TPD ↑ 0 = ∅
  TPD ↑ 1 = {while(X,R1,R) | X=<0, R=R1}
  TPD ↑ 2 = {while(X,R1,R) | X=1, R=R1+1} ∪ {sum_upto(X,R) | X=<0, R=0} ∪ TPD ↑ 1
  TPD ↑(k+1) = {while(X,R1,R) | X=k, R=R1+(k(k+1)/2)}
                ∪ {sum_upto(X,R) | X=k-1, R=(k-1)k/2} ∪ TPD ↑ k                  for all k>1
                                                                           S
Now, in order to check that goal 1 holds in lfp(TPD ) (which is equal to            D
                                                                               k≥0 TP ↑ k), we
reason as follows. First, we have that lfp(TPD ) is equal to:
    {while(X,R1,R) | X=<0,R=R1} ∪ {while(X,R1,R) | X=1, R=R1+1}
    S
  ∪ k>1 {while(X,R1,R) | X=k, R=R1+(k(k+1)/2)}
  ∪ {sum_upto(X,R) | X=<0, R=0}
    S
  ∪ k>1 {sum_upto(X,R) | X=k-1, R=(k-1)k/2}                                               (†)
(Note that for all integers k>1, we have that k(k+1)/2 and (k-1)k/2 are integer numbers,
and thus the constraints in the above expression of lfp(TPD ) are all in the domain Integer.)
Then, with reference to the constraint X=k-1, R=(k-1)k/2 in Expression (†), we can
show by induction that, for all k≥1, we have that k-1 ≤ (k-1)k/2, which implies that
X ≤ R. Thus, no atom in lfp(TPD ) with predicate sum_upto(M,Sum) satisﬁes the constraint
M>Sum, M>=0 in goal 1, and we get that goal 1 is true in lfp(TPD ). Hence, P ∪ {goal 1} is
D-satisﬁable and the validity of the Hoare triple is proved.


                                2.4.2 Top-down procedures
The top-down approach to check satisﬁability is based on the extension of SLD-resolution
(Kowalski and Kuehner 1971, Lloyd 1987, Apt 1990) to CHCs, which is used to deﬁne
the operational semantics of CLP languages (Jaﬀar and Lassez 1987, Jaﬀar et al. 1998).
The core of this approach is the proof-theoretic notion of a top-down derivation. In a
derivation of that kind, in order to check whether or not the atom false can be derived
from a given initial constrained goal and a given set of deﬁnite CHCs, one proceeds
by making backward inferences, that is, replacing an atom which is uniﬁable (modulo
satisﬁability of constraints) with the head of a clause by the corresponding body of the
clause.
   Similarly to the bottom-up case, given a set Q of constrained goals and a set P of
deﬁnite CHCs over a constraint domain D, we will present a top-down procedure which
is sound and complete for showing unsatisﬁability, but it may not terminate if P ∪ Q is
satisﬁable.
Analysis and Transformation of Constrained Horn Clauses for Program Verification 13

   Without loss of generality, we may assume that Q consists of a single goal G, as P ∪ Q
is satisﬁable if and only if for every constrained goal G∈Q, P ∪ {G} is satisﬁable. Let us
also assume that goal G is of the form: false ← d, A1 , . . . , An .
   In this case, a top-down procedure for satisﬁability checking can be formalised by ﬁrst
deﬁning a rewriting system (a similar approach is followed by Jaﬀar and Maher (1994)).
At every rewriting step, a pair of the form hB, ei, where B is a multiset of atoms and e
is a constraint in D, is rewritten into either a new pair hB ′ , e′ i or fail, as we now specify.
   There are two kinds of rewritings: (i) the r-rewriting, which makes use of a computation
rule and a search rule, and (ii) the c-rewriting. They are deﬁned as follows, starting from
a given pair hB, ei.
(i) The r-rewriting, denoted −→r . Assume that B 6= ∅ and e is a satisﬁable constraint.
    Let p(u1 , . . . , uk ) be an atom which is selected among those in B by the computation
    rule. Then, the search rule selects in P a (renamed apart) clause, if any, of the form:
    p(v1 , . . . , vk ) ← f, C. If that clause exists, then we have the following r-rewriting:
                   hB, ei −→r hB ′ , e ∧ u1 = v1 ∧ . . . ∧ uk = vk ∧ f i                                   (1)
    where B ′ is the multiset of atoms obtained from B by deleting the atom p(u1 , . . . , uk )
    and adding the atoms in C.
    If that clause does not exist, we have the rewriting:
                   hB, ei −→r fail                                                                         (2)
(ii) The c-rewriting, denoted −→c . Assume that e is an unsatisﬁable constraint. (B may
    be ∅ or not.) We have the rewriting:
                   hB, ei −→c fail                                                                         (3)
For all i ≥ 0, by −→ir we denote the i-fold composition of −→r . As usual, by −→+
                                                                                r and
   ∗
                             S               S
−→r we denote the relation i>0 −→r and i≥0 −→r , respectively.
                                       i              i

   A top-down derivation (or simply, a derivation) for the goal false ← d, A1 , . . . , An and
the set P of deﬁnite CHCs, is a (ﬁnite or inﬁnite) maximally extended sequence of
r-rewritings or c-rewritings that starts from the pair h{A1 , . . . , An }, d i.
   A derivation is successful if it is ﬁnite and its last pair is of the form h∅, ei, where e is a
satisﬁable constraint, and it is failed if it is ﬁnite and its last element is fail. A derivation is
fair if either it is failed or every atom which occurs in a pair of the derivation is rewritten
in some later rewriting. A computation rule is fair if it gives rise to fair derivations only.
A goal G is finitely failed if every derivation from G which uses a fair computation rule,
is failed.
   The choices made by the search rule give rise to the notion of derivation tree for a
goal G: false ← d, A1 , . . . , An , a set P of deﬁnite CHCs, and a computation rule. The root
of the derivation tree is h{A1 , . . . , An }, di, and every path starting from the root is a
derivation for G and P , according to the given computation rule.
   In a derivation tree, every node hB, ei, where e is a satisﬁable constraint, has the chil-
dren hB 1 , e1 i, . . . , hB k , ek i, if, for i = 1, . . ., k, there exists the rewriting hB, ei −→r hB i , ei i
for any search rule. Every node hB, ei such that hB, ei −→r fail or hB, ei −→c fail has
the single child fail.
   A derivation tree for a goal G: false ← d, A1 , . . . , An and a set P of deﬁnite CHCs is
fair if all its paths from the root are fair derivations. It is finitely failed if it is fair and
all its paths from the root are failed derivations.
14 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

   In order to know whether or not a constraint is satisﬁable (and thus, to know whether
we will perform an r-rewriting or a c-rewriting), we use the function solv associated
with the constraint domain at hand. We may assume that, if the constraint e is satisﬁ-
able, solv(e) returns a constraint equivalent to e presented in a suitably deﬁned normal
form (such as the solved form for a set of equations (Apt 1990)). Moreover, during an
r-rewriting step (see (1) above), after the modiﬁcation of the current constraint, one
could invoke solv and, if the modiﬁed constraint is unsatisﬁable, one could immediately
derive fail without performing a successive c-rewriting. We will not discuss further these
issues concerning the application of the function solv, as they are not relevant for the
topic of the present paper.
Example 10
Let P be the set of clauses over the Integer domain we have considered in Example 8 of
Section 2.4.1. Those clauses are:
  C1.    p(X+3,X) :- X<3.
  C2.    p(X+3,Y) :- X>3, p(X,Y).
In Figure 2 we have depicted the derivation tree for the goal false :- p(5,X) and P .
The constraint X<3, 5=X+3 in the left child of the root can be replaced by the equivalent
constraint X=2 by an application of a suitable version of the function solv.
                                      h{p(5,X)}, truei
                 (using clause C1)                   (using clause C2)
                                 r                    r
                      h∅, {X<3, 5=X+3}i       h{p(X,Y)}, {X>3, 5=X+3}i

                                                         c
                                                          fail
Figure 2. Derivation tree for the goal false :- p(5,X) and the set {C1, C2} of CHCs.

   The success set of a set P of deﬁnite CHCs over the constraint domain D is the set of
all elements of the D-base BD , each of which occurs in the starting pair of a successful
derivation, that is:
   SS(P )D = {p(a1 , . . . , an ) ∈ BD | hp(a1 , . . . , an ), truei −→+r h∅, di ∧ d is satisﬁable}
Recall that in our case by Predu we denote the set of the predicates symbols occurring
in the heads of the clauses of P . A representation of SS(P )D as a set of constrained facts
is as follows:
   SS(P )D = {p(X1 , . . . , Xn ) ← d | p ∈ Predu ∧ hp(X1 , . . . , Xn ), truei −→+             ′
                                                                                         r h∅, d i ∧
                                             ′                                    ′
                                          ∧ d is satisﬁable ∧ d = proj(d , {X1 , . . . , Xn })}
The fundamental result for top-down procedures is that the success set coincides with the
least D-model, that is, SS(P )D = lm(P, D) (Jaﬀar and Maher 1994, Jaﬀar et al. 1998).
   Given a set P of deﬁnite CHCs over a constraint domain D, a basic top-down procedure
for the computation of SS(P )D can be deﬁned as follows. First, we introduce the success
set up to depth k for P , denoted SS(P )kD , as follows:
   SS(P )kD = {p(a1 , . . . , an ) ∈ BD | hp(a1 , . . . , an ), truei −→ir h∅, di ∧ d is satisﬁable ∧
                                           ∧ 0 < i ≤ k}
                        0
We have that SS(P )D = ∅. A top-down procedure computes SS(P )D as the least upper
        S
bound k≥0 SS(P )kD of the sequence SS(P )0D ⊆ SS (P )1D ⊆ SS (P )2D ⊆ . . .
Analysis and Transformation of Constrained Horn Clauses for Program Verification 15

Example 11
Let D be the constraint domain Integer. Let us consider the set P = {C1, C2} of clauses
considered in Example 10 and the goal false :- p(A,X). It can be shown by induction
that the top-down procedure constructs the following sequence of sets of atoms:
  SS(P )0D   =∅
  SS(P )1D   = {p(A,X) | A=X+3, X<3}
  SS(P )k+1
        D   = {p(A,X) | A=X+3(k+1), 0<X<3} ∪ SS (P )k
                                                    D              for all k>0
Thus, we have that:
                                        S
  SS(P )D = {p(A,X) | A=X+3, X<3} ∪       k>0 {p(A,X) | A=X+3(k+1), 0<X<3} = lm(P, D).
   Let us consider a derivation tree for goal G: false ← d, A1 , . . . , An and a set P of
deﬁnite CHCs. We have that P ∪ {G} is satisﬁable if and only if no successful derivation
for G exists in that tree. Thus, in the case where the satisﬁability of constraints in D
is decidable, a sound and complete method for showing unsatisﬁability is to search for
a successful derivation for G. On the contrary, in order to show satisﬁability one should
prove that no such a derivation exists. In the particular case where the derivation tree
for G and P is ﬁnitely failed, then P ∪{G} is satisﬁable. However, when the derivation tree
is inﬁnite, more sophisticated techniques for showing the absence of successful derivations
should be used. For instance, one can apply memoization (or tabling) (Warren 1992,
Cui and Warren 2000) or top-down techniques for CHC analysis, which construct suitable
over-approximations of SS (P )D (see Section 5.2).
   Now we present an example of program veriﬁcation based on the construction of
SS(P )D .
Example 12
Let D be the constraint domain Integer and let P be the set of deﬁnite CHCs over D
that we have considered in Example 9. It can be shown by induction that the top-down
procedure computes the following sequence of sets of atoms:
  SS(P )0D = ∅
  SS(P )1D = {while(X,R1,R) | X=<0, R=R1}
  SS(P )2D = {while(X,R1,R) | X=1, R=R1+1} ∪ {sum_upto(X,R) | X=<0, R=0} ∪ SS (P )1D
  SS(P )k+1
        D   = {while(X,R1,R) | X=k, R=R1+(k(k+1)/2)}
               ∪ {sum_upto(X,R) | X=k-1, R=(k-1)k/2} ∪ SS (P )k
                                                              D            for all k>1
Thus, the set of the sum_upto atoms in SS (P )D is equal to:
                                  S
  {sum_upto(X,R) | X=<0,R=0} ∪ k>1 {sum_upto(X,R) | X=k-1, R=(k-1)k/2}
as expected from the value of lm(P, D) shown in Example 9. Now we have that in SS (P )D
there is no atom of the form sum_upto(M,Sum) that satisﬁes the constraint M>Sum, M>=0
occurring in goal 1. Hence, by using the top-down procedure, we have that there is no
successful derivation for goal 1. We conclude that goal 1 is true in SS(P )D and the
validity of the Hoare triple is proved.
  In practical veriﬁcation systems, one can use the atom false ‘with arguments’, and
instead of the clause 1, one might consider the clause:
  1’. false(M,Sum) :- M>Sum, M>=0, sum_upto(M,Sum).
In this case, if a successful derivation starting from the pair hfalse(M,Sum), truei is
found, then one could know the values of M and Sum which invalidate the triple.
16 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

                     3 Semantics Preserving Transformations
Program transformation is a technique that modiﬁes the text of a program while pre-
serving its semantics. Various programming languages and formal semantics can be con-
sidered, and also the notion of preservation can be deﬁned depending on the applica-
tions. The transformation-based approach we will consider in this paper derives from
two main streams of work that gained popularity starting from the 1970s. The ﬁrst
stream of work is on rule-based program transformation, which has been ﬁrst proposed in
the ﬁeld of functional programming (Burstall and Darlington 1977) and later extended
to logic programming (Tamaki and Sato 1984) and CLP (Etalle and Gabbrielli 1996). A
second stream of work is on program specialisation techniques, such as partial evaluation
and, in the case of (constraint) logic programming, partial deduction. Various surveys
of early developments can be found in the literature (Jones et al. 1993, Gallagher 1993,
Leuschel and Bruynooghe 2002).
   The transformation techniques developed for CLP, with respect to its logical semantics,
can also be applied to CHCs. In this paper we will survey a number of these transforma-
tion techniques, whose objective is to transform a set of CHCs into a new set for which
satisﬁability may be easier to check.
   A transformation of a set S of CHCs into a new set S ′ is a pair, denoted S 7→ S ′ .
Often, the CHC transformation S 7→ S ′ is obtained in several steps, by constructing a
transformation sequence S0 7→ S1 7→ . . . 7→ Sn , such that S0 =S and Sn =S ′ . The semantics
of interest is deﬁned in terms of D-models (see Section 2.3), and we are mainly interested
in the preservation of D-satisﬁability.

Definition 1
A CHC transformation S 7→ S ′ is said to be: (i) sound if the D-satisﬁability of S ′ im-
plies the D-satisﬁability of S, and (ii) complete if the D-satisﬁability of S implies the
D-satisﬁability of S ′ .

  Note that in the above deﬁnition, S and S ′ may contain constrained goals, and these
goals may be modiﬁed by the transformation.


                         3.1 Fold/Unfold Transformations
CHC transformation rules, such as fold/unfold rules, can be used to perform a se-
quence of small modiﬁcations at clause level, which may result in a radical restruc-
turing of the whole set of clauses by changing their pattern of recursion. In the context
of logic programming and CLP, many papers have addressed the problem of showing
that the transformation rules preserve a large variety of semantics deﬁned in terms of
least Herbrand models, ﬁnite failure, computed answers (Pettorossi and Proietti 1994,
Tamaki and Sato 1984), least D-models (Etalle and Gabbrielli 1996), and many others,
by taking into consideration also extra language features, such as negation as (finite
or infinite) failure (Fioravanti et al. 2004, Roychoudhury et al. 2002, Seki 1991) and co-
induction (Seki 2012).
   We now present some transformation rules usually considered in the literature, with
the help of an example, which also motivates their usefulness for program veriﬁcation.
Let us consider the following set S of CHCs over a particular instance of the constraint
Analysis and Transformation of Constrained Horn Clauses for Program Verification 17

domain Array in which the array indexes and the array elements are assumed to be
integers (see Section 2.1).
  1. all_pos(A,I,N) :- I=N.
  2. all_pos(A,I,N) :- 0=<I, I<N, X>0, J=I+1, X=read(A,I), all_pos(A,J,N).
  3. asum(A,I,N,S) :- I=N, S=0.
  4. asum(A,I,N,S) :- 0=<I, I<N, J=I+1, S=S1+X, X=read(A,I), asum(A,J,N,S1).
  5. false :- S<N-I, I>=0, asum(A,I,N,S), all_pos(A,I,N).
The predicate all_pos(A,I,N) holds iﬀ either I=N or, if I<N, all elements of array A
from index I to index N-1 are positive integers. The predicate asum(A,I,N,S) holds if
and only if either (I=N and S=0) or, if I<N, S is the sum of the elements of A from I to
N-1. The constrained goal, i.e., clause 5, states the property that if all elements of A from
I (≥0) to N-1 are positive, then their sum is not smaller than N-I. We may assume that,
similarly to the example in the introduction, these clauses have been generated from an
imperative program acting on arrays that deﬁnes a function asum, and the speciﬁcation
is given by the Hoare triple {all_pos(a,i,n)} s=asum(a,i,n) {s≥n-i}. In order to
construct a model of clauses 1–5 that is deﬁnable in the constraint domain, a CHC
solver needs to extend the Array constraint domain by array formulas with quantiﬁers
over index variables (Bradley and Manna 2007). We will transform clauses 1–5 in such
a way that this type of quantiﬁed constraints is no longer needed.
   The transformation sequence starts oﬀ by applying the definition rule, which allows
us to introduce a new predicate deﬁned in terms of already existing predicates. In our
example, the new predicate newa is deﬁned as the body of clause 5:
  6. newa(A,I,N,S) :- S<N-I, I>=0, asum(A,I,N,S), all_pos(A,I,N).
The objective of the subsequent transformation steps is to derive a recursive deﬁnition
of newa. First, we apply the unfolding rule which, given a set Si of CHCs and a clause
C: H ← c, B1 , A, B2 in Si , where A is any selected atom in the body and B1 , B2 are
conjunctions of atoms, replaces C by the set of all resolvents (with respect to A) of C
and the clauses in Si whose head is uniﬁable with A (modulo the theory of constraints).
In our example, we unfold clause 6 selecting the atom asum(A,I,N,S), and by resolving
that clause with respect to clauses 3 and 4, we get the following two clauses:
  7. newa(A,I,N,S) :- S<N-I, I>=0, I=N, S=0, all_pos(A,I,N).
  8. newa(A,I,N,S) :- S<N-I, I>=0, I<N, J=I+1, S=S1+X, X=read(A,I),
        asum(A,J,N,S1), all_pos(A,I,N).
The constraint in the body of clause 7 is unsatisﬁable, and hence, by applying the clause
deletion rule, we may remove that clause, which is true in all Array-interpretations. Now,
we unfold clause 8 selecting all_pos(A,I,N) and, by applying again the clause deletion
rule and replacing constraints by equivalent ones, we get the new clause:
  9. newa(A,I,N,S) :- S<N-I, I>=0, I<N, X>0, J=I+1, S=S1+X, X=read(A,I),
        asum(A,J,N,S1), all_pos(A,J,N).
Now, we apply the folding rule, which consists in using a clause H ← d, B (where B
is a conjunction of atoms) introduced by the deﬁnition rule, and replacing a clause
K ← c, B1 , B ρ, B2 , where ρ is a variable renaming, by the new clause K ← c, B1 , H ρ, B2 ,
provided that c entails d ρ in the constraint domain at hand (some extra conditions on ρ
are needed if vars(H) ⊂ vars(B)). Since the constraint S<N-I, I>=0, I<N, X>0, J=I+1,
S=S1+X in the body of clause 9 entails the constraint S1<N-J, J>=0, which is a variant
18 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

of the constraint occurring in the body of the deﬁnition clause 6, we fold clause 9 using
clause 6, and we derive:
  10. newa(A,I,N,S) :- S<N-I, I>=0, I<N, X>0, J=I+1, S=S1+X, X=read(A,I),
        newa(A,J,N,S1).
We can also fold clause 5 using clause 6, and derive the new constrained goal:
  11. false :- S<N-I, I>=0, newa(A,I,N,S).
Finally, we apply another instance of the clause deletion rule, which consists in deleting
any clause C from a set Si when no predicate in the constrained goals of Si depends on the
head predicate of C. By this rule we can delete clauses 1–4, as the predicate newa depends
on neither asum nor all_pos. The ﬁnal set of clauses is S ′ = {clause 10, clause 11}. It is
trivially satisﬁable in the constraint domain Array because it does not contain any con-
strained fact for newa, and its least Array-model is the empty Array-interpretation. The
following general result (De Angelis et al. 2018a, Etalle and Gabbrielli 1996) guarantees
that also the initial set S of CHCs is satisﬁable in the domain Array.

Theorem 1 (Soundness and Completeness of Fold/Unfold Transformations)
Let S0 7→ S1 7→ . . . 7→ Sn be a transformation sequence of CHCs over a constraint do-
main D. Suppose that, for i = 0, . . . , n−1, Si+1 is derived from Si by an application of
one of the following rules: deﬁnition, unfolding, folding, clause deletion and replacement
of constraints which are equivalent in D. Suppose also that each clause used for folding
has been unfolded in a previous step of the sequence. Then,
   (i) S0 is D-satisﬁable if and only if Sn is D-satisﬁable; and
  (ii) if S0 has a D-deﬁnable model, then Sn has a D-deﬁnable model.

   Note that, in the case where both S0 and Sn are satisﬁable, they may have diﬀerent
D-models, simply because they may contain diﬀerent predicate symbols. However, their
least D-models agree on common predicates (Etalle and Gabbrielli 1996). Point (ii) of
Theorem 1 is important because, as already mentioned, many CHC solvers work by look-
ing for D-deﬁnable models, and fold/unfold transformations guarantee the preservation
of the existence of such models (De Angelis et al. 2018a). However, by the fold/unfold
rules we may derive, from a set S0 of satisﬁable CHCs that do not have any D-deﬁnable
model, for a given constraint domain D, a new set Sn with a D-deﬁnable model that can
be computed by a CHC solver (see also an example of this transformation in Section 6.2.1
where a set of satisﬁable clauses with no LIA-deﬁnable model are transformed into a set
of clauses with a LIA-deﬁnable model).
   To understand why the condition on folding in Theorem 1 is indeed needed, let us
observe that, in particular, it disallows self-folding. For instance, consider the following
unsatisﬁable set of clauses:
  1. p.           2. false :- p.
By introducing the new predicate
  3. q :- p.
and then folding clauses 2 and 3 using clause 3 itself, we get the following set of clauses:
  1. p.           4. false :- q.            5. q :- q.
which is satisﬁable.
  Besides semantics preservation, a very relevant issue for fold/unfold transformations
Analysis and Transformation of Constrained Horn Clauses for Program Verification 19

is the design of strategies that guide the application of the transformation rules for the
achievement of a speciﬁc objective. In particular, the introduction of new predicates via
the deﬁnition rule (see, for instance, the introduction of predicate newa in the example
above), also known as eureka step in the transformation literature (Burstall and Darlington
1977), often needs ingenious techniques to achieve automation. In the context of CHC
veriﬁcation, several fully automated strategies have been designed with the objective
of deriving clauses whose satisﬁability can be checked in a more eﬃcient, eﬀective way
by CHC solvers. In Section 6, we will present some of those strategies through appli-
cation examples, and we will point to the relevant literature for the detailed technical
presentations.


                               3.2 CHC Specialisation
Program specialisation is a transformation that customises a program with respect to
its context of use, often identiﬁed by a set of partially known input data (Jones et al.
1993). In the ﬁeld of logic programming, program specialisation (and in particular, partial
evaluation, also called partial deduction) has been formalised in a proof-theoretic way,
by building upon the notion of incomplete SLD(NF )-tree (Lloyd and Shepherdson 1991).
Such tree represents a set of partial computations starting from an atomic goal that
constitutes the context of use of the program. From a set of incomplete SLD(NF)-trees,
one can extract new clauses specialised to the atomic goals of interest. A similar approach
has been extended to CLP (Leuschel and De Schreye 1998).
   An alternative, equivalent presentation, which we will follow here for CHCs, is based
on fold/unfold transformations (Proietti and Pettorossi 1993, Sahlin 1993). Indeed, CHC
specialisation can be viewed as a strategy for applying the transformation rules we have
introduced in Section 3.1. The deﬁnition of a sound and complete CHC specialisation will
be an instance of Deﬁnition 1 in the following sense. Given a set P of deﬁnite CHCs and
an atomic goal false ← c, A, where A is an atom, a sound and complete CHC specialisation
yields a set P ′ of clauses and an atomic goal false ← c′ , A′ such that P ∪ {false ← c, A}
is D-satisﬁable if and only if P ′ ∪ {false ← c′ , A′ } is D-satisﬁable.
   From a technical point of view, the main restriction of CHC specialisation with respect
to general fold/unfold transformations, is that the new predicates introduced by speciali-
sation are deﬁned by clauses whose body has a single atom, and not a conjunction of two
or more atoms. Thus, each new deﬁnition introduces a specialised version of a given pred-
icate, and in particular, a specialised version of the predicate occurring in the atom A.
However, this characterisation of CHC specialisation should be taken with some ﬂexi-
bility, as there are techniques like conjunctive partial deduction (De Schreye et al. 1999),
which similarly to the general fold/unfold rules, transform logic programs by producing
specialised predicates that correspond to conjunctions of atoms.
   Let us show how specialisation works with the help of an example. Let us consider the
following set of CHCs over the constraint domain LIA:
  1. false :- X=0, p(X,[0]).
  2. p(X,C) :- X=Y+1, p(Y,C).
  3. p(X,[N|T]) :- X>N.
  4. p(X,[N|T]) :- N>0, q(X,T).
where predicate q is deﬁned by a set of clauses not shown here. We want to specialise
20 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

the clauses with respect to derivations of the atom false. Thus, by looking at goal 1,
we use the deﬁnition rule and we introduce a specialised predicate sp(X) for the atom
p(X,[0]).
  5. sp(X) :- p(X,[0]).
In this ﬁrst step, we might have introduced a diﬀerent specialised predicate, e.g., by
taking into account the constraint X=0. The key issue of controlling the introduction of
new predicates will be discussed later. Now, by unfolding clause 5, we explore all possible
one-step derivations from p(X,[0]).
  6. sp(X) :- X=Y+1, p(Y,[0]).
  7. sp(X) :- X>0.
  8. sp(X) :- 0>0, q(X,[]).
Clause 8 can be deleted because the constraint in its body is unsatisﬁable. By folding
clauses 1 and 6 using clause 5, which deﬁnes the specialised predicate sp, we derive our
ﬁnal set of clauses:
  1f. false :- X=0, sp(X).
  6f. sp(X) :- X=Y+1, sp(Y).
  8. sp(X) :- X>0.
It is easy to see that this set of clauses is satisﬁable. Indeed, its least LIA-model is
{sp(X) :- X>0.}, which can be computed in two iterations of the immediate conse-
quence operator.
   This example suggests some of the potential advantages of CHC specialisation. First
of all, specialisation computes a portion of the CHCs that is relevant to the goal of
interest. For instance, the predicate q, which might require a complex computation when
checking satisﬁability, has been discarded. Another interesting eﬀect is that lists have
been removed, and hence the specialised CHCs can be solved on the LIA domain, instead
of the more complex domain that combines Term and LIA.
   Two main control issues must be tackled for automating CHC specialisation (Leuschel and Bruynooghe
2002). The ﬁrst one is local control, that is, the control of the unfolding process starting
from a given deﬁnition of a specialised predicate. The specialisation algorithm should:
(i) select an atom in the body of a clause to be unfolded (trivial in our example be-
cause all clauses are linear), and (ii) decide when to stop unfolding (after one step in our
example).
   The second issue is global control (Martens and Gallagher 1995), that is, the introduc-
tion of suitable deﬁnitions of specialised predicates. When we stop unfolding, we may
want to replace (by folding) a constrained atom by a specialised predicate, as done in
the above example by folding clause 6 using clause 5. To perform this folding we may
need to introduce a new specialised predicate deﬁnition, which in turn must be unfolded,
thus generating new constrained atoms to be folded. In order to terminate the whole
process, we need to introduce a ﬁnite number of new deﬁnitions by which we are able
to fold all atoms in the body of the clauses derived by unfolding (this is related to
the closedness and coveredness conditions introduced by Lloyd and Shepherdson (1991)
and Leuschel and De Schreye (1998), respectively). In most specialisation algorithms
for CLP and CHCs, this set of deﬁnitions is constructed via suitable generalisation tech-
niques (Peralta and Gallagher 2003, Fioravanti et al. 2013a), which compare the various
specialised versions of the same predicate introduced during transformation, and com-
pute a ﬁnite set that generalises them all by using, for instance, widening operators on
Analysis and Transformation of Constrained Horn Clauses for Program Verification 21

constraints derived from the ﬁeld of abstract interpretation (Cousot and Cousot 1977,
Cousot and Halbwachs 1978). More details on widening and generalisation will be given
in Sections 5 and 6.

                           3.3 Redundant Argument Removal
Redundant argument removal in a set of clauses P with respect to a goal G is a pro-
gram transformation that removes an argument from a predicate in all its occurrences
in P ∪ {G}. Let us call the resulting clauses and goal, after deleting the argument, P ′
and G′ , respectively. Algorithms, called RAF (Redundant Argument Filtering, for top-
down elimination with respect to a goal) and FAR (for bottom-up goal-independent
elimination), which remove redundant arguments, were formulated by Leuschel and
Sørensen (1996). The RAF and FAR algorithms determine sound and complete transfor-
mations from P ∪ {G} to P ′ ∪ {G′ }. Similar algorithms for CLP have been presented by
De Angelis et al. (2017b). Removing redundant arguments can be a useful pre-processing
step since removing variables leads to the elimination of constraints, and can greatly re-
duce the complexity of constraint solving operations. The RAF and FAR algorithms are
related to classical liveness analysis, as shown by Henriksen and Gallagher (2006), while
the relation to the well-known notion of slicing was discussed by Leuschel and Vidal
(2005).
   Consider the following simple example (Leuschel and Sørensen 1996, adapted from Ex-
ample 8), which illustrates how the combination of argument removal and constraint sim-
pliﬁcation can result in the removal of constraints. It is common for veriﬁcation conditions
to include a goal of the form false ← c, p(X1 , . . . , Xn ), where p(X1 , . . . , Xn ) represents the
state of the computation at some program point, and c is a constraint on a small subset
of the state variables X1 , . . . , Xn . In such cases, redundant argument removal can often
lead to the elimination of constraints involving the remaining variables of the predicate p
in other clauses, whose values do not aﬀect c.
Example 13
Let us consider the clauses:
  false :- X>0, q(X,Y).
  q(X,Y) :- X<Y.
Applying the algorithm RAF with respect to the goal false :- X>0, q(X,Y) results
in the following clauses in which the second argument of q is removed. Intuitively, the
argument Y is not ‘used’ in the goal.
  false :- X>0, q1(X).
  q1(X) :- X<Y.
The constraint X<Y can then be replaced in the clause body by true. Applying the FAR
algorithm to the resulting clauses further eliminates the remaining argument of q1, after
which the constraint X>0 can be replaced by true and we are left with the clauses
  false :- q2.
  q2 :- true.
Note that the RAF algorithm can be reconstructed as an application of the fold/unfold
transformation rules (by introducing a new predicate deﬁned by q1(X) :- q(X,Y), in
our example), while, in general, FAR cannot, in a straightforward way, as it exploits
information derived from the constrained facts, rather than from the clause where the
predicate we want to transform occurs.
22 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

                        3.4 Query-Answer Transformations
Query-answer transformations were originally inspired by the magic-set transformation
from deductive databases and the language Datalog (Bancilhon et al. 1986, Rohmer et al.
1986). The typical form of the query-answer (QA) transformation is as follows: given a
set P of deﬁnite clauses and an atom A, let {p1 , . . . , pn } be the predicates occurring in
P ∪ {A}. For each predicate pi , with 1 ≤ i ≤ n, deﬁne an answer predicate pai and a query
predicate pqi . Let the atom Aa (resp. Aq ) be the same as atom A with the predicate p
replaced by pa (resp. pq ). The transformed clauses consist of the union of two sets of
clauses, called the answer clauses P a and the query clauses P q (Kaﬂe and Gallagher
2017a). Given a set P of deﬁnite clauses and a goal false ← c, A, then for each clause
H ← c, A1 , . . . , An (n ≥ 0) in P , we have that:
 (i) P a contains the answer clause H a ← c, H q , Aa1 , . . . , Aan , and
(ii) P q contains the query clauses Aqj ← c, H q , Aa1 , . . . , Aaj−1 , for 1 ≤ j ≤ n.
In addition to the above clauses, P q contains the query clause Aq ← c.
   The relevant correctness property of the transformation is that P ∪ {false ← c, A}
is satisﬁable if and only if P a ∪ P q ∪ {false ← c, Aa } is satisﬁable. The purpose of the
QA transformation is to simulate a top-down derivation (see Section 2.4.2) with left-to-
right computation rule; the query predicates capture the calls in a top-down, left-to-right
derivation of A, and the answer predicates represent the result of successful calls within
the derivation.
Example 14
Let D be the constraint domain Integer. Consider the following goal and deﬁnite clauses
over D:
  1. false :- X=0, p(X).
  2. p(X) :- X=1.
  3. p(X) :- X>1, Y=X+1, p(Y).
Applying the QA transformation with respect to p(X) results in the following goal 4 and
set R = {5,6,7,8} of deﬁnite clauses:
  4. false :- X=0, p_a(X).
  5. p_a(X) :- X=1, p_q(X).
  6. p_a(X) :- X>1, Y=X+1, p_q(X), p_a(Y).
  7. p_q(Y) :- X>1, Y=X+1, p_q(X).
  8. p_q(X) :- X=0.
The bottom-up procedure for the set R of CHCs (see Section 2.4.1) yields the following
sequence of two interpretations TRD ↑0 ⊆ TRD ↑1, where TRD ↑0 = ∅ and TRD ↑1 = {p_q(0)} =
lfp(TRD ). We have that the ﬁnite D-interpretation {p_q(0)} satisﬁes R ∪ {4}, and hence
the original set {1,2,3} of clauses is satisﬁable. However, note that the least model of the
set of the original set of clauses {2,3} is inﬁnite. Furthermore, the top-down derivation
from goal 1 in the original clauses yields a ﬁnite computation, failing after a call to p(0).
   Applying the QA transformation to linear clauses yields clauses in which the an-
swer predicates depend on the query predicates, but not vice versa. However, in the
case of non-linear CHCs, QA transformation gives clauses in which answer predicates
and query predicates are mutually dependent. For example, for a clause of the form
p(X) ← c, r(Y ), p(Z) (with a left-to-right computation rule), pq depends on ra (via query
clause pq (Z) ← c, pq (X), ra (Y )), which depends on rq (via answer clause of the form
ra (X) ← rq (X), . . .), which in turn depends on pq (via query clause rq (Y ) ← c, pq (X)).
Analysis and Transformation of Constrained Horn Clauses for Program Verification 23

   The use of QA transformations is entirely pragmatic; they allow bottom-up analy-
sis tools (see Section 5.1) to achieve the constraint propagation and thereby analysis
precision that would otherwise require top-down analysis frameworks (see the paper
by Codish et al. (1997) for a related discussion on the precision of goal-dependent anal-
yses versus goal-independent analyses). Frameworks for goal-dependent analyses making
use of such transformations were developed (Kanamori 1993, Debray and Ramakrishnan
1994, Nilsson 1995). Examples of practical implementations of logic program analysis
using QA transformations include the work of Codish and Demoen (1995) for modes and
simple types and Gallagher and de Waal (1994) for regular approximations.


                 4 From Programs to Constrained Horn Clauses
Constrained Horn clauses have been used to represent a wide variety of systems and
programs in other languages. These include imperative, functional and object-oriented
programs (at diﬀerent compilation levels, including bytecode, LLVM-IR, or machine in-
structions) (Peralta et al. 1998, Henriksen and Gallagher 2006, Méndez-Lojo et al. 2007,
Navas et al. 2008, Gómez-Zamalloa et al. 2009, Grebenshchikov et al. 2012, Liqat et al.
2016, Gurﬁnkel et al. 2015, De Angelis et al. 2015, Kahsai et al. 2016, López-García et al.
2018, Pérez-Carrasco et al. 2020). Apart from programming languages, Section 7 men-
tions other formalisms that have been translated into CHCs for the purpose of veriﬁca-
tion.
   In this section we summarise diﬀerent approaches to translating programs, focussing
on the translation of imperative programs, together with properties to be proved, into a
set of CHCs to be tested for satisﬁability.


          4.1 Semantics-driven Translation of Imperative Languages
An imperative program deﬁnes a relation hs, σ0 i =⇒ σ1 , which means that if statement s
is executed in initial state σ0 , then σ1 is the state after execution of s, assuming that
the execution halts. In this discussion, a program state is just a mapping from variables
to values; see examples later in the section. The relation =⇒, closely related to the well-
known notion of a Hoare triple (Hoare 1969), can be speciﬁed by Horn clauses, using
the operational semantics of the language of s, in two main styles: small-step (structural
operational semantics) (Plotkin 1981) or big-step (natural semantics) (Kahn 1987), or a
mixture of the two. Let the predicate exec(S,St0,St1) represent the relation, where S,
St0 and St1 are ﬁrst-order terms representing s, σ0 and σ1 , respectively.


                               4.1.1 Small-step specification
In the small-step style the exec relation is speciﬁed as a chain of steps. In a single step
hs0 , σ0 i ⇒ hs1 , σ1 i, s0 is executed in state σ0 , leaving the remaining statement s1 to be
executed in state σ1 ; this is represented by the relation step(S0,St0,S1,St1) in which
S0, St0, S1 and St1 are representations of s0 , σ0 , s1 and σ1 respectively, The chain of
steps, or run, is deﬁned by the recursively deﬁned relation run(S0,St0,S1,St1), which
speciﬁes the reﬂexive, transitive closure ⇒∗ . A complete execution is a run that reaches
24 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

   hs1 , σ0 i ⇒ hhalt, σ1 i           hs1 , σ0 i ⇒ hs′1 , σ1 i         hs1 , σ0 i =⇒ σ1 hs2 , σ1 i =⇒ σ2
   hs1 ; s2 , σ0 i ⇒ hs2 , σ1 i   hs1 ; s2 , σ0 i ⇒ hs′1 ; s2 , σ1 i             hs1 ; s2 , σ0 i =⇒ σ2

Figure 3. Small-step (left) and big-step (right) rules for statement composition.


a halt statement (from which no steps are possible); i.e., hs0 , σ0 i =⇒ σn if and only if
hs0 , σ0 i ⇒∗ hhalt, σn i.
  exec(S,St0,St1) :- run(S,St0,halt,St1).
  run(S,St,S,St) :- true.
  run(S0,St0,S2,St2) :- step(S0,St0,S1,St1), run(S1,St1,S2,St2).
The small step for a simple statement such as an assignment of the form x := e, repre-
sented asg(var(X),E), evaluates the expression e in state σ0 (using predicate eval),
computes state σ1 by replacing the value of x with the result of the evaluation (using
predicate replace) and moves to the halt statement.
  step(asg(var(X),E),S0,halt,S1):- eval(E,S0,V), replace(X,V,S0,S1).
   Let the term seq(S1,S2) represent the compound statement s1 ; s2 , where S1 and S2
represent the component statements s1 and s2 , respectively. Then a small step on s1 ; s2
is speciﬁed as follows.
 step(seq(S1,S2),St0,S2,St1):- step(S1,St0,halt,St1).
 step(seq(S1,S2),St0,seq(S11,S2),St1):- step(S1,St0,S11,St1), S116=halt.
For program analysis and transformation, both big-step and small-step styles have ad-
vantages and disadvantages. Clauses derived using small-step semantics are often simpler,
and essentially represent transition systems; thus they are amenable to well established
model-checking techniques. Big-step predicates allow compositional analysis since each
program component is represented by an input-output predicate; however, this means
that predicates have a greater number of arguments than small-step predicates, which
can increase the complexity of analysis algorithms.


                                        4.1.2 Big-step specification
In the big-step style, the exec relation is deﬁned by structural decomposition of state-
ments. For instance, the complete execution of x := e and s1 ; s2 are speciﬁed as follows.
  exec(asg(var(X),E),St0,St1) :- eval(E,St0,V), replace(X,V,St0,St1).
  exec(seq(S1,S2),St0,St2) :- exec(S1,St0,St1), exec(S2,St1,St2).
  These logical formulations of big- and small-step semantics are direct translations of the
semantic rules to be found in textbooks, e.g., (Nielson and Nielson 1992) (see Figure 3).
The close connection between semantic judgements and Horn clauses was ﬁrst noted by
Kahn and exploited in semantics-based tools (Kahn 1987, Donzeau-Gouge et al. 1984).
More complex semantic rules than the simple ones considered above can be represented,
such as the Clight big-step speciﬁcations for a subset of the language C (Blazy and Leroy
2009).
  Derivation of small-step CHCs from big-step CHCs, and vice versa, can also be deﬁned
(Gallagher et al. 2020). Big-step and small-step styles can be mixed; for example, a pro-
cedure call in the small-step style can be deﬁned as a single step that completely executes
the procedure body, such as is done in (De Angelis et al. 2017b). The following clause
Analysis and Transformation of Constrained Horn Clauses for Program Verification 25

omits parameter passing, for simplicity, and we assume that def(F,FDef) encodes the
relation between the procedure name F and its deﬁnition.
  step(call(F),St0,halt,St1) :- def(F,FDef), run(FDef,St0,halt,St1).


                              4.1.3 Translation by specialisation
Let I be the set of CHCs deﬁning the exec relation, introduced in Section 4.1.1, for the
language of statement (or program) s, that is, exec(S,St0,St1) holds iﬀ hs, σ0 i =⇒ σ1 .
Then, we can apply CLP specialisation (Section 3.2) to I ∪ {false :- exec(S,St0,St1)},
yielding a specialised version of the exec relation for S. This is an instance of the ﬁrst
Futamura projection (Futamura 1971); an interpreter specialised (by partial evaluation)
with respect to a source program P can be seen as a compilation of P into the language
of the interpreter, which in our case is the language of constrained Horn clauses. By
suitable choice of renaming deﬁnitions, the syntactic structure of P and the state rep-
resentations can be removed, leaving predicates whose arguments are the values of the
program variables.
Example 15
Let the source program consist of the assignment sum = sum_upto(m), together with the
function in Figure 1. Using a big-step semantics speciﬁcation of exec, we obtain by
partial evaluation the following CHCs3 :
  asg1(M,Sum1) :- sum_upto(M,E), Sum1=E.
  sum_upto(A,C) :- D=A, E=0, while4(D,E,F,C).
  while4(A,B,E,F) :- A>0, H=B+A, I=A-1, while4(I,H,E,F).
  while4(A,B,A,B) :- A=<0.
The predicate asg1(M,Sum1) is a renamed version of the goal which was specialised,
using the following new deﬁnition:
 asg1(M,Sum1) :- exec(asg(var(sum),call(sum_upto,[var(m)])),
                        [(m,M),(sum,Sum)], [(m,M1),(sum,Sum1)]).
The term asg(var(sum),call(sum_upto,[var(m)])) is the representation of the state-
ment sum = sum_upto(m), whereas [(m,M),(sum,Sum)] and [(m,M1),(sum,Sum1)] rep-
resent the states before and after execution; the states are lists of pairs relating program
variables to their values, but the renaming version retains only the values. Furthermore
the variable Sum is a redundant argument (Leuschel and Sørensen 1996) (see Section 3.3),
and M1 is detected during specialisation to be equal to M. After partial evaluation, ev-
ery statement of the source program results in a corresponding call to exec; trivial
calls to exec are then unfolded. These clauses can be run as a logic program with goal
asg1(M,Sum1) (assuming standard procedures for evaluating arithmetic predicates) with
some speciﬁc input value of M, simulating the execution of the given source program and
returning the result Sum1.
A similar translation based on a small-step semantics can also be performed. Variations
of this are described in the literature (Peralta et al. 1998, Henriksen and Gallagher 2006,
De Angelis et al. 2015). Calls to the step predicate can be completely unfolded, leaving
linear clauses of the form:

3 The big-step interpreter is available at https://github.com/jpgallagher/Semantics4PE and
  the partial evaluation was performed using Logen (Leuschel et al. 2006)
26 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

  run(s0,st0,S2,St2) :- c, run(s1,st1,S2,St2).
where s0, st0, s1, st1 are terms and c is a constraint on the variables occurring in
those terms. The predicate run can then be renamed as in the big-step translation.
   The main advantage of translation by specialisation of a semantics-based interpreter
is that the correctness of translation follows from the correctness of the interpreter and
of the partial evaluator. The correctness of semantics-based interpreters is established
by reference to the formal semantic rules of which the interpreter is composed. The
correctness of the partial evaluator can be demonstrated once and for all, and can then
be applied to many diﬀerent interpreters.


       4.1.4 Generating verification conditions from semantics-based interpreters
Consider a Hoare triple {Pre} s {Post}, where we have predicates on states pre(St)
and post(St) deﬁning Pre and Post, respectively, and error(St) deﬁning the negation
of Post. We also assume that the statement s is given using a fact prog(S). The Hoare
triple is expressed by a goal:
  false :- pre(St0), prog(S), exec(S,St0,St1), error(St1).
For instance, the veriﬁcation problem presented in Section 1 is to show that the Hoare
triple {m≥0} sum = sum_upto(m) {sum≥m} is valid. Let pre, post, and error be deﬁned
as follows:
  pre([(m,M),(sum,Sum)]) :- M>=0.
  post([(m,M),(sum,Sum)]) :- Sum>=M.
  error([(m,M),(sum,Sum)]) :- M>Sum.
The Hoare triple is then expressed by the implication:
 pre(St0)∧ exec(asg(var(sum),call(sum_upto,[var(m)])),St0,St1) → post(St1)
which is equivalent to the following goal g:
  false :- pre(St0), error(St1),                                      (g)
            exec(asg(var(sum),call(sum_upto,[var(m)])),St0,St1).
Specialisation of T ∪ {g}, where T denotes the set of clauses deﬁning pre, exec, and
error, yields the set of clauses T ′ ∪ {g’}, where the goal g’ is:
  false :- M>Sum, M>=0, asg1(M,Sum).                                                  (g’)
and T ′ is the set of clauses shown in Example 15, which is essentially the same set of
veriﬁcation conditions (see clauses 1–4) shown in Section 1. (Note, in fact, that the third
argument of predicate while4 in T ′ is redundant.)

Reachability-style verification conditions. Assume now that the exec predicate is spec-
iﬁed using small-step semantics, using the clauses for exec, run, and step shown in
Section 4.1.1. We derive reachability-style veriﬁcation conditions by an unfold-fold trans-
formation of the semantics-based formulation of the veriﬁcation of a Hoare triple. By
unfolding exec, we obtain the following clauses whose satisﬁability has to be checked
(together with the clauses deﬁning step):
  false :- pre(St0), prog(S), run(S,St0,halt,St1), error(St1).
  run(S,St,S,St) :- true.
  run(S0,St0,S2,St2) :- step(S0,St0,S1,St1), run(S1,St1,S2,St2).
Introduce the following new deﬁnition:
  error_reach(S0,St0) :- run(S0,St0,halt,St1), error(St1).
Analysis and Transformation of Constrained Horn Clauses for Program Verification 27

Unfolding the deﬁnition of error_reach and folding twice, we obtain the following
clauses:
  false :- pre(St), prog(S), error_reach(S,St).
  error_reach(halt,St) :- error(St).
  error_reach(S0,St0) :- step(S0,St0,S1,St1), error_reach(S1,St1).
After specialising these clauses for the instances of pre, error, and S from Section 1 (in
particular, S is asg(var(sum),call(sum_upto,[var(m)])), we obtain the following
diﬀerent set of veriﬁcation conditions than the ones shown previously:
  false :- M>=0, assign_error(M).
  assign_error(M) :- X=M, Sum=0, while_error(X,M,Sum).
  while_error(X,M,Sum) :- X=<0, M>Sum.
  while_error(X,M,Sum) :- X>0, Sum1=Sum+X, X1=X-1, while_error(X1,M,Sum1).
This set of conditions has some potential advantages over the previous ones. The predicate
arguments relate to only one state at a time, rather than both an initial and a ﬁnal state
as encoded in the exec or run predicates. Secondly, small-step semantics gives linear
clauses that are closely related to the transition systems handled by model checkers and
techniques for reachability analysis.
   The above clauses encode backwards reachability; the base case of the error_reach
relation is the error state and the goal is the initial state. A similar unfold-fold trans-
formation can be performed to yield veriﬁcation conditions based on forwards reachabil-
ity, or else the Reversal transformation discussed in Section 6.1 can be applied to the
backwards reachability clauses shown above. The resulting set of clauses (shown in the
following subsection) is essentially the same as the schema for proving safety properties
of transition systems given by Grebenshchikov et al. (2012).


                          4.2 Translation via Proof Rules
Although the semantics-based approach provides a comprehensive framework for deriving
CHCs and veriﬁcation conditions from imperative programs, other techniques are often
used in the literature. Rather than translating the source language, some works translate
a veriﬁcation problem for some source language into CHCs indirectly, by encoding the
proof rules and semantic model of the system as CHCs.
   A comprehensive presentation of CHC-based veriﬁcation was given by Grebenshchikov et al.
(2012); in that work, it is assumed that imperative procedures are represented as transi-
tion systems, and CHCs are then constructed from the transitions themselves and from
CHC schemata for proof rules from the literature on program veriﬁcation, such as rely-
guarantee rules, procedure summarisation rules (Reps et al. 1995), and termination proof
rules. For instance, the following scheme is used to formulate proofs of safety of a tran-
sition system, where tr(St0,St1) represents a transition from state St0 to state St1,
init(St) states that St is the initial state, reach(St) states that St is reachable from
the initial state, and error(St) states that St is an error state.
  false :- reach(St), error(St).
  reach(St) :- init(St).
  reach(St1) :- reach(St), tr(St,St1).
Essentially the same scheme was derived in the previous section from semantic deﬁnitions
and unfold-fold transformations. Other proof-based approaches are brieﬂy presented in
Section 7.
28 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

                               4.3 Abstract Compilation
A variation on the approach described above is obtained when the semantics-based in-
terpreter is an abstract interpreter written as a set of CHCs, which is then specialised
with respect to a given source program. The resulting CHCs represent an abstraction of
the original source program. This technique, and its application to program analysis, is
called abstract compilation (Warren et al. 1988, Hermenegildo et al. 1992). The aim is to
generate from an original source program P an abstract set of clauses P ′ whose execution
yields the analysis results corresponding to the abstraction encoded in the interpreter.
An example is the generation of size-change transitions for termination analysis, where
the abstract interpreter computes the size of data structures rather than their values
(Verschaetse and De Schreye 1992).


                           4.4 Compiler-based Translation
Translating from general-purpose programming languages such as C or Java to CHCs
is a challenge due to the complexity of the source language. A pragmatic approach is
to rely on a compiler from the source language into an intermediate language such as
three-address code, LLVM, or Java bytecode, and then translate from there into CHCs.
   Indeed, it has been argued that constrained Horn clauses provide many advantages as
an intermediate compiler representation language (Méndez-Lojo et al. 2007, Gange et al.
2015), naturally incorporating features such as SSA form, reduction of all iterative con-
structs to a single one (recursion), clariﬁcation of variable scope, built-in capture and rep-
resentation of alternative executions paths and non-determinism, and so on. A CHC rep-
resentation facilitates analysis and optimisation of compiled code using solvers, analysers,
and transformation tools available for CHCs. These arguments apply to all CHC-based
representations of imperative code, not only those intended for compilation.
   SeaHorn, a veriﬁcation framework for C based on CHCs, uses a compiler front-end
and then “takes as input the optimized LLVM bitcode and emits veriﬁcation conditions
as Constrained Horn Clauses (CHC)” (Gurﬁnkel et al. 2015). JayHorn, a translator for
Java, follows a similar approach (Kahsai et al. 2016); the description of the translation
to CHCs states that “most steps of the translation from Java into logic are implemented
as bytecode transformations, with the implication that their soundness can be tested
easily”. Thus, it is argued that the translation from intermediate languages is simpler
than translating the source program. Neither of the above cited works provides a formal
proof of correctness of the translation, relying on the correctness of the compiler to reduce
the source to a form where the translation is relatively straightforward.


                4.5 Translation of Source Language Annotations
Some programming languages and systems provide facilities for adding annotations to the
source code, supporting software engineering methods such as design by contract (Meyer
1988, Leavens et al. 2006), or as a part of an advanced program development environment
integrating debugging, analysis, and static and dynamic veriﬁcation (Hermenegildo et al.
1999, 2005; Puebla et al. 2000).
  Such languages and systems include assertions such as assume(A) and check(A). For
example, a procedure contract in Eiﬀel or JML might contain in the procedure body the
Analysis and Transformation of Constrained Horn Clauses for Program Verification 29

precondition assume(x > 0), where x is a parameter of the procedure, meaning that the
procedure call is assumed to satisfy that condition. Similarly, at the end of the procedure
the assertion check(x < w) means that if the precondition holds when the procedure starts,
and the procedure terminates, then at termination we should have x < w. In a constraint
logic programming language with assertions, such as Ciao (Hermenegildo et al. 2012),
similar check-style literals can be used at any program point, but there is also a speciﬁc
form for stating conditions on the execution of an atom. For instance, we may have:
   :- check calls        p(X,W) : X>0.                                                  (1)
   :- check success p(X,W) : X>0 => X<W.                                                (2)
where assertion (1) is a condition X>0 on the call constraints for the atom p(X,W) and
assertion (2) is a condition X<W on the success (answer) constraints for the same atom,
for calls that meet the call constraint X>0. There may be several of these assertions for
a given atom.
   In general, veriﬁcation conditions for such procedure contracts are essentially the same
as for a Hoare triple, and can be generated from the language semantics as discussed
above.
   Conditions to be checked may be inserted at arbitrary program points, and a general
scheme for generating CHC veriﬁcation conditions is to assume that for each program
point k there is a predicate reachk (St), such that St is the state when point k is reached.
Then, the veriﬁcation condition for some property ϕ that should hold at point k is the
goal false ← reachk (St), error(St), where error(St) is a predicate deﬁning the negation
of the desired property ϕ on state St.
   As we will see in Section 5.2, static analyses can produce information directly at
all program points k, without explicitly generating predicates reachk (St), for each k.
Program point assertions can be checked directly against this inferred information.
   An additional proof requirement in the above precondition/postcondition scenario may
consist in checking that all calls to a procedure satisfy a given precondition. For example,
the Ciao calls assertion as (1) above, does require this. If this precondition cannot be
proved statically, before running the program (and this may always happen because of un-
decidability limitations), then a dynamic, run-time check will be introduced for it, issuing
a warning or calling an exception handling routine if the check fails (Hermenegildo et al.
1999, Puebla et al. 2000).


                              5 Analysis for Verification
In this section we review techniques for CHC analysis applied to veriﬁcation. These
techniques, derived mainly from the CLP literature, in some cases directly yield a proof
of satisﬁability (or unsatisﬁability), while in others, they help with inferring relevant
program properties such as loop invariants. Static analysis also plays an important role
in guiding some CHC transformations, especially specialisation.
   The main technique used in these approaches is Abstract Interpretation (Cousot and Cousot
1977), a technique for static program analysis in which execution of the program is simu-
lated on an abstract domain (Dα ) which is simpler than the concrete domain (D). Values
in the abstract domain and values in the concrete domain are related via a pair of mono-
tonic mappings hα, γi: the abstraction α : D → Dα , and the concretisation γ : Dα → D,
which form a Galois connection. An abstract value d ∈ Dα approximates a concrete value
30 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

c ∈ D if α(c) ⊑ d, where ⊑ is the partial ordering on Dα . We refer to these abstract val-
ues also as descriptions. The correctness of abstract interpretation guarantees that the
descriptions inferred (by computing a ﬁxpoint through a Kleene sequence (Tarski 1955))
approximate all the actual values which occur during any possible execution of the pro-
gram, and that this ﬁxpoint computation process will terminate given some conditions on
the abstract domains (such as being ﬁnite, or of ﬁnite height, or without inﬁnite ascending
chains) or by the use of a widening operator (Cousot and Cousot 1977). Guaranteed ter-
mination implies one of the fundamental characteristics of abstract interpretation-based
analyses: automation. Given an abstract domain and, if needed, a widening operator,
analysis does not require user intervention. This comes at the price of some loss in preci-
sion, determined by the abstraction used. Abstraction also brings about scalability, since
it makes it possible to trade oﬀ precision for eﬃciency. These two characteristics enable
the use of abstract interpretation in practical automated tools.
   In the following we review the two main techniques used for CHC analysis applied to
veriﬁcation, which are based on abstracting respectively the bottom-up and top-down
satisﬁability procedures of Section 2.4.


                     5.1 Bottom-up Semantics-based Analysis
The bottom-up approach to logic program analysis was ﬁrst proposed by Marriott and Søndergaard
(1988) and further elaborated by Codish et al. (1994). The approach is based on the
bottom-up semantics discussed in Section 2.4.1, in which the least model of a set P of
clauses is computed as the least ﬁxpoint of the function TPD : 2BD → 2BD , that is, the
least upper bound of the sequence ∅ ⊆ TPD ↑ 1 ⊆ TPD ↑ 2 ⊆ . . .
   Bottom-up analysis using abstract interpretation involves approximating the func-
tion TPD by a new continuous function UP : A → A, where the abstract domain A is
a complete lattice with bottom element ⊥, partial order ⊑, and concretisation func-
tion γ : A → 2BD . The condition TPD ◦ γ ⊆ γ ◦ UP ensures that the sequence ⊥ ⊑ UP (⊥) ⊑
UP2 (⊥) ⊑ . . . converges to an over-approximation of lfp(TPD ), that is, lfp(TPD ) ⊆ γ(lfp(UP )).
If the lattice A has no inﬁnite ascending chain, lfp(UP ) is reached in a ﬁnite number of
steps; otherwise a widening (Cousot and Cousot 1992) is used to construct a sequence
⊥ ⊑ M1 ⊑ M2 ⊑ . . ., such that for all i ≥ 1, UPi (⊥) ⊑ Mi and the sequence is ultimately
stationary; that is, for some ﬁnite k, Mk = Mk+1 = Mk+2 = . . . In both cases we obtain
in a ﬁnite number of steps some over-approximation L of lfp(UP ). Thus, information
about the least model of P can be inferred and hence satisﬁability can be checked; in
particular, if a goal false ← c, B1 , . . . , Bn is true in γ(L), then it is also true in lfp(TPD ) and
hence P ∪ {false ← c, B1 , . . . , Bn } is satisﬁable. An early example of bottom-up analysis
was the type analysis by Barbuti and Giacobazzi (1992). Mode analyses using a bottom-
up analysis framework were also developed by Corsini et al. (1994) and Gallagher et
al. (1995).
Example 16
Consider again the clauses of Example 9 on the constraint domain Integer. They are:
  1. false :- M>Sum, M>=0, sum_upto(M,Sum).
  2. sum_upto(X,R) :- R0=0, while(X,R0,R).
  3. while(X1,R1,R) :- X1>0, R2=R1+X1, X2=X1-1, while(X2,R2,R).
  4. while(X1,R1,R) :- X1=<0, R=R1.
Analysis and Transformation of Constrained Horn Clauses for Program Verification 31

A bottom-up analysis using the abstract domain of convex polyhedra over real num-
bers (Cousot and Halbwachs 1978) is applied to these clauses. This kind of analysis was
ﬁrst introduced into logic programming by Benoy and King (1997). For each predicate
p(X1 , . . . , Xn ), where X1 , . . . , Xn range over reals, a convex polyhedron is represented by
a constrained fact p(X1 , . . . , Xn ) ← c, where c is a linear constraint over X1 , . . . , Xn rep-
resenting a convex polyhedron. An element of the abstract domain for the set of CHCs at
hand is thus a set of constrained facts, one for each predicate. The concretisation func-
tion maps a set of constrained facts to the set of atoms p(d1 , . . . , dn ) such that the point
(d1 , . . . , dn ) is inside the polyhedron for p. The function UP is deﬁned as any function on
the tuple of polyhedra for the predicates, satisfying TPD ◦ γ ⊆ γ ◦ UP ; a suitable implemen-
tation of UP makes use of well-established libraries for manipulating convex polyhedra
such as the Parma Polyhedra Library (Bagnara et al. 2008). The abstract domain has
inﬁnite ascending chains and so, in general, a widening operation on polyhedra is needed
to force convergence of the sequence ⊥ ⊑ UP (⊥) ⊑ UP2 (⊥) ⊑ . . .
   In the following sequence of approximations, we ﬁrst compute the approximation of
the model of the recursive predicate while; this is reached in Step 4 after applying a
widening from Step 3 to Step 4, which (in particular) discards the potentially inﬁnite
sequence of constraints X=<1, X=<2, . . . In Step 5, the approximation of the model of the
non-recursive predicate sum_upto is obtained in one step.
  1. {while(X,R1,R) | X=<0, R=R1}
  2. {while(X,R1,R) | R>=R1, X=<1, R>=X+R1}
  3. {while(X,R1,R) | R>=R1, X=<2, R>=X+R1}
  4. {while(X,R1,R) | R>=R1, R>=X+R1}
  5. {while(X,R1,R) | R>=R1, R>=X+R1} ∪ {sum_upto(X,R) | R>=X, R>=0}
The goal false :- M>Sum, M>=0, sum_upto(M,Sum) is true in the concretisation of the
model computed at Step 5, and hence we can conclude that clauses 1-4 are satisﬁable.


                       5.2 Top-down Semantics-based Analysis
Top-down analyses represent another class of CHC-based program analyses, and were ﬁrst
used in analysers such as MA3 and Ms (Warren et al. 1988), PLAI (Muthukumar and Hermenegildo
1990, 1992, García de la Banda et al. 1996), GAIA (Le Charlier and Van Hentenryck 1994),
or the CLP(R) analyser (Kelly et al. 1998). This style of analysis was extended early on
to CLP/CHCs by García de la Banda and Hermenegildo (1993) and García de la Banda
et al. (1996). These techniques have also been applied to the analysis of functional,
imperative, and object-oriented programs (Méndez-Lojo et al. 2007, Albert et al. 2007,
Navas et al. 2008, 2009, Liqat et al. 2014, 2016, López-García et al. 2018, Pérez-Carrasco et al.
2020), by transforming the original program into CHCs as explained in Section 4. Such
transformations often use the big-step semantics approach.

Basic top-down analysis. Top-down analyses are based on the top-down semantics of
CHCs presented in Section 2.4.2 or variations thereof.
  A basic top-down analysis using abstract interpretation can be derived from this se-
mantics, in a similar way to the bottom-up analysis, as we now specify. Recall that
the top-down semantics is given by a rewriting system on a set S, whose elements
are the pairs hB, ei, where B is a multiset of atoms and e is a constraint on a given
constraint domain D, together with the distinguished element fail. Every element of
32 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

S can be viewed as a constrained goal, being fail any unsatisﬁable goal. A rewriting
step on S, denoted −→, is either an r-rewriting (−→r ) or a c-rewriting (−→r ). Given a
set Q of goals in S, we deﬁne the one-step top-down function td Q : 2S → 2S , as follows:
td Q (T ) = Q ∪ {G′ | G ∈ T, G −→ G′ }. Then, we have that the set of goals reachable by
a (possibly inﬁnite) sequence of rewritings from Q is equal to lfp(tdQ ).
   To construct an abstract interpretation, we assume as before an abstract domain A
which is a complete lattice with bottom element ⊥ and concretisation function: γ : A → 2S .
Thus, an element of A denotes a set of goals. Let I in A be an abstract goal. An abstract
top-down function is a function tdαI : A → A, satisfying tdγ(I) ◦ γ ⊆ γ ◦ tdI . This condition
                                                                            α

ensures that tdα I has a least ﬁxpoint and lfp(tdγ(I) ) ⊆ γ(lfp(tdI )).
                                                                  α


And-trees and call-success semantics. For top-down analysis, it is useful to structure
derivations as trees, rather than sequences of rewritings. This will allow us to identify
the call and (possibly) success constraints for each atom occurring in a derivation, and
this information that can be directly related to atoms in the CHCs. First, we need the
following notion. Given a set P of CHCs, an and-tree for P is deﬁned as follows.
1. Each node is a triple hA, c, Ci, where A is an atom (possibly the atom true), c is a
   constraint whose free variables are a subset of vars(A), and C is a clause in P . The
   component C is empty for leaf nodes.
2. In each non-leaf node, the C component is a clause A ← c′ , B1 , ..., Bk (with k ≥ 1) in P
   which is renamed so that: (i) the head A is identical to the atom of the node, and
   (ii) the variables which occur in the body of the clause and not in the head, do not
   occur outside the subtree at that node. Constrained facts are written as A ← c′ , true.
3. A non-leaf node hA, c, A ← c′ , B1 , . . . , Bk i has k ≥ 1 ordered children,
       hB1 , proj(c ∧ c′ , vars(B1 )), C1 i, · · · , hBk , proj(c ∧ c′ , vars(Bk )), Ck i
   with possibly empty clauses components C1 , . . . , Ck .
Let t be an and-tree and constr(t) be the set of all constraint components of the nodes
of t. Then t is feasible if constr(t) is satisﬁable; t is successful if it is feasible and all
leaf nodes have atom true; t is failed if it has a leaf node with constraint false. When
understood from the context we will feel free to say ‘tree’, instead of ‘and-tree’.

Call constraints and answer constraints in an and-tree. For each successful and-tree t
with root hA, c, Ci, the answer constraint of the root is proj(constr(t), vars(A)). Non-
successful and-trees have no answer constraint of the root. We can also compute call
constraints for nodes of an and-tree, corresponding to the leftmost selection rule. A node
N = hA, c, Ci has a call constraint if the subtrees t1 , . . . , tj (j ≥ 0) rooted at the sibling
nodes to the left of N are successful, and have answer constraints c1 , . . . , cj , respectively.
In this case the call constraint is proj(c ∧ c1 ∧ . . . ∧ cj , vars(A)).

The analysis graph approach. Many practical top-down abstract interpreters adopt a
particular approach that is based on computing an analysis graph. This approach was ﬁrst
proposed in PLAI and is followed in other analysers, like GAIA, or the CLP(R) analyser.
The graph inferred is a ﬁnite, abstract object whose concretisation approximates the
(possibly inﬁnite) set of (possibly inﬁnite) maximal and-trees of the concrete semantics.
  This approach separates the abstraction of the structure of the trees (i.e., the paths in
the concrete trees) from the abstraction of the constraints at the nodes in the concrete
trees. Thus, the abstract domain is made out of two abstractions. The ﬁrst one, called Tα ,
Analysis and Transformation of Constrained Horn Clauses for Program Verification 33

is typically built-in (even if there may be several choices for it), and is the abstract domain
of the analysis graph, which ﬁnitely approximates the shapes of the concrete and-trees,
independently of the contents of the nodes.
   The Tα abstraction is parametric on a second abstraction domain, called Dα . Elements
of Dα are used as labels in the nodes of the analysis graph, and represent the sets of call
constraints and success constraints of the nodes of the concrete and-trees. Using the same
Tα abstraction, many Dα domains have been developed to use Tα for inferring modes,
sharing (variable aliasing), types, numerical constraints, arrays, deﬁniteness, determi-
nacy, non-failure, resources, etc. Each such Dα domain has its concretisation function γ
and its basic operations on the domain lattice (such as least upper bound, greatest lower
bound, and, optionally, widening), a few additional instrumental operations such as pro-
jection and extension, and the semantics (transfer functions) of any built-ins (basic oper-
ations) of the language (see, e.g., the papers by Muthukumar and Hermenegildo (1992),
García de la Banda et al. (1996), and Hermenegildo et al. (2000)).
   The input to the analysis is a set P of CHCs, an abstract domain Dα , and a set Qα
of abstract goals 4 hAi , λi i, where each Ai is an atom with variables as arguments and
λi ∈ Dα . The set Qα deﬁnes the (possibly inﬁnite) set of concrete goals for which that
the analysis should be performed: Q = {hA, d i | d ∈ γ(λ) ∧ hA, λi ∈ Qα }. The concrete
semantics to be safely approximated is then the set of all and-trees that have an element
of Q as root. The result of the analysis is an analysis graph, where every node is of the
form hA, λc , λs i, where {λc , λs } ⊆ Dα (note that the component λ of a node has been
split into a call component λc and a success component λs ).
   Correctness of the analysis requires that if there are one or more nodes in the concrete
trees of the form hA, dc , ds i (also for concrete nodes the constraint components is split
into two), then there exists a node hA, λc , λs i in the analysis graph such that dc ∈ γ(λc )
and ds ∈ γ(λs ). This means that the analysis graph must capture all the call–success
pairs in all the nodes of the and-trees of the concrete semantics. For a given predicate A,
the analysis graph can contain more than one node, with diﬀerent call descriptions.
A node hA, λc , ⊥i indicates that calls to predicate A with description d ∈ γ(λc ) either fail
or do not terminate. An edge in the analysis graph hA, λc , λs i 7→ hB, µc , µs i represents
that calling A with calling description λc generates an atom B to be called with calling
description µc . Correctness requires that if in any concrete tree there is a node hA, dc i
with a child hB, ec i, then there exists an edge hA, λc , λs i 7→ hB, µc , µs i in the graph such
that dc ∈ γ(λc ) and ec ∈ γ(µc ).
   Generating the analysis graph consists essentially in following the construction of the
and-tree with two main diﬀerences: (i) instead of the concrete operations for the con-
straints, the operations from Dα should be used, and (ii) in the construction of the
graph, call descriptions are tabulated so that, if the abstract call constraint of a node
is equal to (or, optionally, subsumed by) that of a node already present, the graph is
not extended and, instead, an edge is introduced pointing to that node (see, node C in
Figure 4). The success label is initialised to ⊥ and the iteration for constructing a ﬁx-
point for the labels is started. For domains with inﬁnite ascending chains the widening
operator is applied to limit the number of call and success descriptions considered. Ad-

4 For reasons of simplicity, in what follows, we will feel free not to write the third component, i.e., the
  clause, of the nodes of and-trees. That clause is common to the abstract and concrete nodes.
34 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

ditional details and optimisations of the particular algorithms used can be found in the
references given above. Also, many variants have been proposed and among them, let us
mention the incremental analyses (Puebla and Hermenegildo 1996, Hermenegildo et al.
2000, García-Contreras et al. 2020a,b). In all cases by the fundamental results of abstract
interpretation one has that (i) termination is guaranteed, and (ii) the concretisation of
the analysis graph is a safe over-approximation of the and-trees generated by the concrete
semantics.
Example 17
Figure 4 (García-Contreras et al. 2020a) shows a possible analysis graph (center of ﬁgure)
for a set of CHCs (left of ﬁgure) that encodes the computation of the parity of a binary
message using the exclusive or, denoted xor. For instance, the parity of the message
[1,0,1] is 0. We take the abstract domain (right of ﬁgure) with the following abstract
values: (i) ⊥ such that γ(⊥) = ∅, (ii) z (for zero) such that γ(z) = {0}, (iii) o (for one) such
that γ(o) = {1}, (iv) b (for bit) such that γ(b) = {0, 1}, and (v) ⊤ such that γ(⊤) is the
set of all concrete values, and initial abstract goal Gα = h main(Msg,P), (Msg/⊤, P/⊤) i,
i.e, where the arguments of main can be bound to any concrete value (see node A in the
ﬁgure). Node B = (h par(Msg,X,P), (Msg/⊤, X/z, P/⊤), (Msg/⊤, X/z, P/b) i) captures
the fact that par may be called with X bound to 0 in γ(z) and, if par succeeds, the third
argument P will be bound to any value in γ(b) = {0, 1}. Note that node C captures the
fact that, after this call, there are other calls to par where X/b. Edges in the graph
stem from the hA, λc , λs i 7→ hB, µc , µs i relation. For example, two such edges exist from
node B, denoting that par may call xor (edge from B to D) or par itself with a diﬀerent
call description (edge from B to C). In this example we have used a simple, non-relational
abstract domain. In the following example we will use a relational domain over the
integers.

                                h main(Msg,P),
                           A:     (Msg/⊤, P/⊤),
main(Msg,P) :-                    (Msg/⊤, P/b) i
     par(Msg,0,P).

par([ ],P,P).                                                                           ⊤
par([C|Cs],P0,P) :-         h par(Msg,X,P),                h xor(C,P0,P1),
     xor(C,P0,P1),        B: (Msg/⊤, X/z, P/⊤),          D: (C/⊤, P0/z, P1/⊤),
     par(Cs,P1,P).           (Msg/⊤, X/z, P/b) i            (C/b, P0/z, P1/b) i         b

xor(0,0,0).                                                                        z         o
xor(0,1,1).
xor(1,0,1).
xor(1,1,0).                 h par(Msg,X,P),                h xor(C,P0,P1),              ⊥
                          C: (Msg/⊤, X/b, P/⊤),          E: (C/⊤, P0/b, P1/⊤),
                             (Msg/⊤, X/b, P/b) i            (C/b, P0/b, P1/b) i


Figure 4. A set of CHCs for computing parity (left) and a possible analysis graph (right).


Example 18
The following is an encoding of the sum_upto example in Ciao 5

5 Modulo the syntax convention adopted in the paper. For instance, for constraints we use > and =,
  instead of .>. and .=., respectively.
Analysis and Transformation of Constrained Horn Clauses for Program Verification 35

  :- module(_,[sum_upto/2],[assertions,nativeprops]).
  :- check calls         sum_upto(M,Sum) : M>=0.
  :- check success sum_upto(M,Sum) : M>=0 => Sum>=M.
  sum_upto(X,R) :- R0=0, while(X,R0,R).
  while(X1,R1,R) :- X1>0, R2=R1+X1, X2=X1-1, while(X2,R2,R).
  while(X1,R1,R) :- X1=<0, R=R1.
The check calls assertion instructs the system to check that M>=0 holds for calls to
sum_upto and, similarly, check success asks for a check that Sum>=M holds after suc-
cessful derivations starting from h{sum_upto(M,Sum)}, M>=0i (see also Section 4.5).
  The output from (top-down) analysis in Ciao for this module, taken in isolation, with
the domain of convex polyhedra (Cousot and Halbwachs 1978), using the Parma Poly-
hedra Library (Bagnara et al. 2008), yields:6
  :- module(_,[sum_upto/2],[assertions,nativeprops]).
  :- check   calls   sum_upto(M,Sum) : M>=0.
  :- checked success sum_upto(M,Sum) : M>=0 => Sum>=M.
  :- true    success sum_upto(M,Sum) : M>=0 =>
             (M>=0, Sum>=M, Sum>=2*M-1, Sum>=3*M-3, Sum>=4*M-6).
  sum_upto(X,R) :- R0=0, while(X,R0,R).
  :- true pred while(X1,R1,R) : (X1>-1, R1>=0) => (X1>-1, R1>=0,
          R>=R1, R>=X1+R1, R>=2*X1-1, R>=3*X1-R1-3, R>=4*X1-2*R1-6).
  while(X1,R1,R) :- X1=<0, R=R1.
  while(X1,R1,R) :- X1>0, R2=R1+X1, X2=X1-1, while(X2,R2,R).
The true assertions contain (part of) the information inferred (i.e., the abstract values)
for each of the two predicates. They represent as assertions the nodes of the analysis graph
and the call and success constraints in each of those nodes. The (true) pred assertion
is a shorthand for a pair of assertions consisting of an identical success assertion and a
calls assertion with the same precondition as the pred, i.e.:
  :- true calls   while(X1,R1,R) : (X1>-1, R1>=0).
  :- true success while(X1,R1,R) : (X1>-1, R1>=0) => (X1>-1, R1>=0,
          R>=R1, R>=X1+R1, R>=2*X1-1, R>=3*X1-R1-3, R>=4*X1-2*R1-6).
The checked success assertion for sum_upto is the result of comparing (reducing,
using abstract specialisation) the original check success and the true assertion in-
ferred, and it indicates that the postcondition Sum>=M has been proven for the assump-
tion M>=0 (Bueno et al. 1997, Puebla et al. 2000). However, since this assumption cannot
be proven to hold without context information (i.e., without knowing how this module
will be called), the check calls assertion remains in check status and a run-time test
will be generated for it. If this module is analysed in the context of other modules that
call it, perhaps inter-modular analysis allows this condition to be discharged and the
run-time test eliminated.
   The analysis graph also contains abstract information at all points in the bodies of the
CHCs, which can also be printed out as assertions, e.g., for the sum_upto predicate:
  sum_upto(X,R) :- true(X>=0), R0=0, true((X>=0,R0=0)), while(X,R0,R),
      true((X>=0, R0=0, R>=X, R>=2*X-1, R>=3*X-3, R>=4*X-6)).

where the true literals are program point assertions which state properties that hold at
those points (for a left-to-right computation rule).

6 This output is a simplification of the information inferred by the analyser: it combines, using the least
  upper bound operator, the information contained in the different versions inferred (see later).
36 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

Polyvariance (context- and path-sensitivity). The analysis graph approach allows repre-
senting the diﬀerent call descriptions encountered during the execution, separating the
cases in which such calls diﬀer, even if some of them subsume others. This feature is tra-
ditionally referred to as polyvariance (or multivariance) in the context of logic program
analysis, and, in our context, it serves two purposes:
1. Precision: Diﬀerent calling descriptions for the same predicate can be recorded de-
   pending on which exact clause and literal this predicate is called from and with
   which call description. This idea of storing multiple calling contexts in this way is
   used in recent implementations of context sensitivity in imperative program analy-
   ses (Khedker and Karkare 2008, Thakur and Nandivada 2020) where it is referred to
   as keeping multiple value contexts.
2. Efficiency: For the same literal and clause in the CHCs, storing diﬀerent calling de-
   scriptions allows keeping the ﬁxpoint computation localised to only those descriptions
   that change.
In addition, the diﬀerent call descriptions for and paths to a given predicate that the anal-
ysis graph encodes in a compact way are really representing diﬀerent possible versions of
that predicate. These versions, which are implicit in the analysis graph, can be materi-
alised in a process called polyvariant specialisation (Bulyonkov 1984, Jacobs et al. 1990,
Giannotti and Hermenegildo 1991, Jones et al. 1993, Puebla and Hermenegildo 1999),
which is essentially the abstract version of traditional predicate specialisation (see Sec-
tions 3.2 and 6.1), allowing additional optimisations. An instrumental concept for the lat-
ter is abstract executability (Giannotti and Hermenegildo 1991, Puebla and Hermenegildo
1999), i.e., the partial evaluation of concrete code with respect to abstract values.
Example 19
As an example of polyvariant specialisation, the graph in Figure 4 contains the two
versions par_1 and par_2 for predicate par and the two versions xor_1 and xor_2 for
xor. Invoking version materialisation produces the following specialisation:
  main(Msg,P) :- par_1(Msg,0,P).
  par_1([],P,P).
  par_1([C|Cs],P0,P) :- xor_1(C,P0,P1), par_2(Cs,P1,P).
  par_2([],P,P).
  par_2([C|Cs],P0,P) :- xor_2(C,P0,P1), par_2(Cs,P1,P).
  xor_1(0,0,0).      xor_1(0,1,1).     xor_1(1,0,1).                       xor_1(1,1,0).
  xor_2(0,0,0).      xor_2(0,1,1).     xor_2(1,0,1).                       xor_2(1,1,0).

Example 20
The following are all the versions (the abstract polyvariant specialisation) generated
during analysis by the Ciao analyser for the sum_upto example, assuming as before the
precondition M>=0, and using again the domain of convex polyhedra:
  :- module(_,[sum_upto/2],[assertions,nativeprops]).
  :- check calls sum_upto(M,Sum) : M>=0.
  :- checked success sum_upto(M,Sum) : M>=0 => Sum>=M.

  :- true pred sum_upto(M,Sum) : M>=0
     => (M>=0, Sum>=M, Sum>=2*M-1, Sum>=3*M-3, Sum>=4*M-6).
  sum_upto(X,R) :- R0=0, while_1(X,R0,R).

  :- true pred while_1(X1,R1,R) : (X1>=0, R1=0)
Analysis and Transformation of Constrained Horn Clauses for Program Verification 37

     => (X1>=0, R1=0, R>=X1, R>=2*X1-1, R>=3*X1-3, R>=4*X1-6).
  while_1(X1,R1,R) :- X1=<0, R=R1.
  while_1(X1,R1,R) :- X1>0, R2=R1+X1, X2=X1-1, while_2(X2,R2,R).

  :- true pred while_2(X1,R1,R) : (X1>-1, R1=X1+1)
     => (X1>-1, R1=X1+1, R>=X1+1, R>=2*X1+1, R>=3*X1, R>=4*X1-2).
  while_2(X1,R1,R) :- X1=<0, R=R1.
  while_2(X1,R1,R) :- X1>0, R2=R1+X1, X2=X1-1, while_3(X2,R2,R).

  :- true pred while_3(X1,R1,R) : (X1>-1, R1>=X1+1, R1=<2*X1+3)
     => (X1>-1, R1>=X1+1, R1=<2*X1+3, R>=R1, R>=X1+R1,R>=2*X1+R1-1).
  while_3(X1,R1,R) :- X1=<0, R=R1.
  while_3(X1,R1,R) :- X1>0, R2=R1+X1, X2=X1-1, while_4(X2,R2,R).

  :- true pred while_4(X1,R1,R) : (X1>-1, R1>=X1)
     => (X1>-1, R1>=X1+1, R>=R1, R>=X1+R1).
  while_4(X1,R1,R) :- X1=<0, R=R1.
  while_4(X1,R1,R) :- X1>0, R2=R1+X1, X2=X1-1, while_4(X2,R2,R).

The last version, predicate while_4, is obtained after a widening step, reaching a ﬁx-
point expressed by the constraint X1>-1, R1>=X1+1, R>=R1, R>=X1+R1, which holds for
call description X1>-1, R1>=X1. Note that this ﬁxpoint denotes a subset of the model
computed at Step 4 of Example 16 in which a bottom-up analysis is performed.
   In addition to polyvariant specialisation, other, more powerful combinations of top-
down analysis and partial evaluation have been proposed (Puebla et al. 1999, 2006). In
particular, the interleaving method of combining top-down analysis and partial evaluation
of Puebla et al. (2006) has been proved to be strictly more powerful than any bounded
sequence of applications of abstract interpretation and partial evaluation procedures.

  Finally, note that the analysis graph, through the hA, λc , λs i 7→ hB, µc , µs i relation,
provides an abstraction of the paths followed by the concrete executions represented by
the concrete trees. The analysis graph generalises the way in which the call-stack is repre-
sented in the popular call-strings method by Sharir and Pnueli (1981) (this method has
been used in recent work (Khedker and Karkare 2008, Thakur and Nandivada 2020)).
Indeed, the call-string method only keeps track of the callers of the abstracted call,
whereas the analysis graph allows us to infer, as a tree all the procedures executed before
that call and not only its direct callers or a limited-depth sequence.


                             5.3 Abstraction Refinement
Previous sections have shown how abstraction (Cousot and Cousot 1977, Jhala and Majumdar
2009) can be eﬀectively used within bottom-up and top-down procedures to check satis-
ﬁability of CHCs and infer useful properties from them.
   Abstraction also enables the design of hybrid approaches that combine bottom-up and
top-down procedures to compute an over-approximation of the least D-model of a set P
of CHCs. Indeed, in some cases, such an over-approximation S, where S ⊇ lm(P, D), can
be computed in a ﬁnite number of steps as a D-deﬁnable interpretation by using these
procedures enhanced with abstraction (Sections 5.1 and 5.2 present two eﬀective ways for
computing S). If a constrained goal G is true in S ⊇ lm(P, D), then G is true in lm(P, D)
and hence P ∪{G} is satisﬁable. However, if G is false in S, a derivation for G may or may
38 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

not exist. If such a derivation can be constructed, then P ∪ {G} is indeed unsatisﬁable.
Otherwise, a spurious counterexample is used to reﬁne the over-approximation S.
   Predicate abstraction (Graf and Saïdi 1997) with Counterexample Guided Abstraction
Refinement (CEGAR) (Clarke et al. 2003), and Property Directed Reachability (PDR) (Een et al.
2011) (we use this terminology to refer to all those veriﬁcation methods originated from
the hardware model checking algorithm IC3 (Bradley 2011)), represent the mainstream
(software) model checking approaches, based on abstraction and its reﬁnements, that
have been successfully applied to the problem of checking satisﬁability of CHCs (see, for
instance, the CHC-COMP-20 report (Rümmer 2020)).
   The well-established combination of predicate abstraction and CEGAR reﬁnement is
implemented by Eldarica (Hojjat and Rümmer 2018) and HSF-QARMC (Grebenshchikov et al.
2012). Speciﬁcally, given a predicate symbol p occurring in a set of CHCs and a set Pred
of predicates, predicate abstraction maps p into a boolean combination of the predicates
in Pred. Starting from a possibly empty set Pred, this approach makes use of spurious
counterexamples to extend Pred with additional predicates, and thereby obtain more
precise over-approximations. Craig interpolation (Craig 1957) is widely used as a tool
for deriving additional predicates from spurious counterexamples (Jhala and Majumdar
2009, McMillan and Rybalchenko 2013, Demyanova et al. 2017).
   Interpolation is also used as a generalisation technique to improve eﬃciency of tabling
(Jaﬀar et al. 2009) for CLP programs and to enhance program veriﬁcation techniques.
In particular, interpolants are computed as generalisations of the constraints encoun-
tered during the construction of the derivation trees. The computed interpolants avoid
redundant exploration of subtrees rooted at constraints that are subsumed by the cor-
responding tabled interpolant. Improvements and extensions of this approach have been
eﬀectively used to perform program veriﬁcation (Jaﬀar et al. 2012, Gange et al. 2013).
   Abstraction and reﬁnement are also the basic building blocks of PDR. In presenting
this approach, we build upon Hoder and Bjørner (2012) as a basis to recast the PDR
algorithm in terms of the deﬁnitions introduced in the previous sections and the following
additional technical notions.
   The index of an atom in a derivation is inductively deﬁned as follows. All atoms in
the initial pair of the derivation have index 0. If in the derivation there is a rewriting
hB, ei −→r hB ′ , e′ i, where B ′ is the multiset of atoms obtained from B by replacing an
atom A with index k by a multiset of atoms C, then the index of the atoms in C is k + 1
and the index of all other atoms in B ′ is the same as their index in B. Given a (successful
or failed) derivation hA, ci −→∗r hB, di −→x L (where x is either r or c and L is either
h∅, ei or fail), the depth of the derivation is m+1, where m is the maximal index of an
atom in B.
   Given a set P ∪ {G} of CHCs, where P is a set of deﬁnite CHCs and G is a con-
strained goal, PDR incrementally constructs, by extension and reﬁnement, a sequence σ
of interpretations of the form: h I0 , ..., In−1 , In i, such that I0 = TPD (∅), where TPD is the im-
mediate consequence operator deﬁned in Section 2.4.1, and for k = 0, . . . , n−1, (i) Ik |= G,
(ii) Ik ⊆ Ik+1 and (iii) TPD (Ik ) ⊆ Ik+1 (that is, Ik+1 is an over-approximation of TPD (Ik )).
   PDR terminates the construction of σ at the smallest n where we have In ⊆ In−1 (in
which case TPD (In ) ⊆ In and therefore lm(P, D) ⊆ In ), or a successful derivation of G is
found. Hence, upon termination we have that either In |= G, in which case P ∪ {G} is
satisﬁable, or there exists a derivation of G, in which case P ∪ {G} is unsatisﬁable.
Analysis and Transformation of Constrained Horn Clauses for Program Verification 39

   Now we present a high-level account of the mechanism for extending σ = h I0 , ..., Ik i
by appending a new interpretation Ik+1 or reﬁning σ. This process starts by gener-
ating any Ik+1 that satisﬁes TPD (Ik ) ⊆ Ik+1 . In the case where Ik+1 6|= G, PDR pro-
ceeds by attempting to construct a successful derivation of depth k + 1 for G. If such
a derivation is found, then PDR terminates reporting that P ∪ {G} is unsatisﬁable.
Otherwise, assuming that G is false ← c, A1 , . . . , Aq , there exists a failed derivation
h{A1 , . . . , Aq }, ci −→∗r hB, di −→∗r . . . −→c fail of depth 1 ≤ j ≤ k, and there is
an atom A in B such that Ij |= ∃(A ∧ d) and TPD (Ij−1 ) 6|= ∃(A ∧ d) (meaning that Ij repre-
sents a too coarse over-approximation of TPD (Ij−1 )). This failed derivation is also called
a spurious counterexample. In this last case, PDR reﬁnes σ by replacing Ij by a diﬀerent
one, say eIj , such that eIj 6|= ∃(A ∧ d); then the construction of σ resumes from eIj .
   PDR guarantees that whenever a new over-approximation Ik+1 is added to σ, all spuri-
ous counterexamples of depth k+1 have been removed (that is, Ik+1 |= G), making PDR
a complete procedure for showing unsatisﬁability. Of course, the eﬀectiveness of PDR-
based algorithms highly relies on the underlying strategy for searching for (successful
or failed) derivations of G, and the interpolation procedure used to get rid of spurious
counterexamples.
   The PDR solving approach presented in Hoder and Bjørner (2012) has been imple-
mented on top of Z3 (de Moura and Bjørner 2008), and called Generalized PDR (GPDR)
to stress the fact that it can deal with general, non-linear CHCs clauses. Indeed, the IC3
algorithm, which gave rise to the PDR solving approaches, has been introduced for per-
forming model checking of transition systems, which correspond to linear CHCs.
   Currently, Z3 provides the SPACER solving engine (Komuravelli et al. 2016) that fur-
ther extends GPDR by computing under-approximations to improve the strategy for
deriving counterexamples.

Example 21
Now we show how a PDR-based algorithm works for checking the satisﬁability of the
clauses 1–4 presented in Section 1. Recall that the satisﬁability of these clauses shows that
the Hoare triple {m ≥ 0} sum = sum_upto(m) {sum ≥ m} holds for the program fragment of
Figure 1. Note that the computation of TPLIA without abstraction does not terminate (see
Example 9). For reasons of simplicity, we consider a simpliﬁed version of those clauses,
where we have unfolded the atom sum_upto(M,Sum) occurring in goal 1, thereby deriving
the following set of clauses:
  5. while(X,R1,R2) :- X>0, R=R1+X, X1=X-1, while(X1,R,R2).
  6. while(X,R1,R2) :- X=<0, R2=R1.
  7. false :- X>R2, X>=0, R1=0, while(X,R1,R2).
Let P be the set {clause 5, clause 6} and G be goal 7.
   The algorithm starts oﬀ by setting the ﬁrst interpretation I0 to TPLIA (∅), that is,
I0 = {while(X,R1,R2) :- X=<0, R1=R2}. I0 |= G. PDR proceeds by introducing a new
interpretation I1 = {while(X,R1,R2) :- true} (speciﬁcally, the whole BLIA ), which is
the coarsest over-approximation of TPLIA (I0 ).
   Now I1 6|= G, so PDR attempts to construct a derivation for G and discovers that
TP (I0 ) = I0 ∪ {while(X,R1,R2) :- X=1, R2=R1+X } and TPLIA (I0 ) |= G. Hence, I1 rep-
  LIA

resents a too coarse over-approximation of TPLIA (I0 ), and PDR proceeds by reﬁning it.
This process essentially requires ﬁnding a constraint F to restrain the current interpre-
40 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

tation for the predicate while in I1 , that is, ﬁnding a clause while(X,R1,R2) :- F,
such that the following two properties hold: (a) TPLIA (I0 ) ⊆ {while(X,R1,R2) :- F},
and (b) {while(X,R1,R2) :- F} |= G. This task easily translates into solving an inter-
polation problem over LIA. Indeed, property (a) requires that (X=<0, R1=R2) → F and
(X=1, R2=R1+X) → F, while property (b) requires that the conjunction of F and the con-
straint ‘X>R2, X>=0, R1=0’ is unsatisﬁable.
   Note that there is some freedom in choosing such a constraint F and, in particular, we
can take F as (X=<0, R1=R2)∨(X=1, R2=R1+X), which is equivalent to TPLIA (I0 ). However,
by doing so, the reﬁnement process would produce an inﬁnite sequence σ of interpreta-
tions. Indeed, in order to help the convergence of σ to In ⊆ In−1 , PDR reﬁnes I1 in a
more gradual manner by trying to ﬁnd a constraint that satisﬁes these additional two
conditions: (c) all constraints occurring in constrained facts in P entail F, and (d) the
interpretation I|F reﬁned using F is a subset of TPD (I|F ). A constraint enjoying these prop-
erties is R2>=R1+X. Hence, we can use R2>=R1+X to reﬁne the current over-approximation
of the predicate while in I1 , thereby getting I1 = {while(X,R1,R2):- R2>=R1+X}.
   Now I1 satisﬁes goal 7. Hence, PDR keeps going on by introducing a new interpreta-
tion I2 , that is, {while(X,R1,R2) :- true}. Now, the algorithm performs exactly the
same steps performed from the introduction of I1 . This process leads to the reﬁnement
of I2 and we get I2 = I1 , and thus PDR terminates computing an over-approximation of
lm(P, LIA). Since I1 satisﬁes goal 7, we conclude, as desired, that the Hoare triple is
valid. Note that in Example 9 the proof of validity of the Hoare triple makes use of an
induction principle.


                          6 Transformation for Verification
We recall from Section 4 that a program veriﬁcation problem can often be reduced to
the problem of checking the satisﬁability of a set P ∪ Q of CHCs, called the veriﬁcation
conditions. The set P consists of clauses whose heads are atoms with user-deﬁned predi-
cate symbols (that is, deﬁnite clauses) and Q consists of clauses whose head is false (that
is, constrained goals). In Section 4, we have also surveyed some techniques, based on the
specialisation of interpreters, by which P ∪ Q can be generated from: (i) a program text
written in a language whose semantics is speciﬁed by an interpreter, and (ii) a property
to be veriﬁed for that program.
   More transformations can be applied to the set P ∪ Q of CHCs, with the objective of
easing the satisﬁability check. That is, we can transform P ∪ Q to a new set P ′ ∪ Q′ , and
then attempt to check satisﬁability of P ′ ∪ Q′ using any of the techniques summarised
in previous sections such as those based on bottom-up, or top-down, or abstraction-
reﬁnement approaches. Transformations can be sound and/or complete (see Deﬁnition 1).
Using a sound transformation P ∪ Q 7→ P ′ ∪ Q′ , a proof of satisﬁability of P ′ ∪ Q′ implies
the satisﬁability of P ∪ Q. Using a complete transformation, a proof of satisﬁability of
P ∪ Q implies the satisﬁability of P ′ ∪ Q′ . By contraposition, this means that, if a coun-
terexample to satisﬁability exists in P ′ ∪ Q′ obtained by a complete transformation, a
counterexample to satisﬁability also exists in P ∪ Q. Transformations that are sound and
complete preserve both satisﬁability and unsatisﬁability.
   CHC transformations can often take advantage of the analysis techniques described in
Section 5, which may help infer over- and under-approximations of the least D-model
Analysis and Transformation of Constrained Horn Clauses for Program Verification 41

of P . These combinations of CHC analysis and transformation can be applied as a pre-
processing step, with the aim of enhancing the eﬀectiveness of subsequent applications
of CHC solvers, but they can also be part of the satisﬁability checking algorithm itself.
   In the rest of the section, we will ﬁrst focus on the use of CHC specialisation, and other
supporting analysis and transformation techniques, for propagating the constraints ap-
pearing in P ∪ Q and deriving a set of more speciﬁc clauses. We will show that this
specialisation often aids the veriﬁcation of satisﬁability. Then, we will present techniques
based on fold/unfold transformation rules, which extend CHC specialisation by allowing
the introduction of new predicates deﬁned as constrained conjunctions of atoms, instead
of constrained atoms only (see Section 3). This extended ability is very helpful for rela-
tional verification and for the veriﬁcation of programs manipulating inductively defined
data structures. Finally, we will brieﬂy recall various reﬁnements and applications of the
above mentioned techniques.


                  6.1 Constraint Propagation by Specialisation
In order to check the satisﬁability of the set P ∪ Q of CHCs, diﬀerent approaches have
been proposed in the literature (see Section 2.4). Among these, CHC solvers based on
abstraction reﬁnement implement a hybrid bottom-up and top-down approach. They
try to compute an over-approximation of lm(P, D) where all goals in Q are true (that
is, the bodies of the goals Q are all false). This over-approximation is constructed in a
bottom-up fashion, by applying some abstraction operator to the TPD immediate conse-
quence operator. The search for such over-approximation is guided, through reﬁnement,
by looking at the goals in Q, and by interleaving the bottom-up procedure with the
attempt to construct a successful top-down derivation of one of those goals which would
show the unsatisﬁability of P ∪ Q.
   A weakness of this family of satisﬁability procedures is that they may fail to derive
from Q a reﬁnement that is inductive, i.e., that is preserved by an application of TPD .
In many cases we may mitigate this weakness by preprocessing the set of clauses and
propagating constraints from Q into the clauses of P , so that information about the
goals can be carried over during the bottom-up construction. Constraint propagation
from goals can be achieved by CHC specialisation, as we explain with the help of an
example.
   Let us consider the following clauses with constraints in the domain LRA of Linear
Real Arithmetic:
  1. false :- X=0, Y=0, p(X,Y,N).
  2. p(X,Y,N) :- X>=N, X>Y.
  3. p(X,Y,N) :- X<N, X1=X+1, Y1=X1+Y, p(X1,Y1,N).
The clauses are satisﬁable, but the CHC solvers Eldarica and Spacer/Z3 (with default set-
tings) fail to terminate on this simple example. A specialisation of the above clauses can
be obtained by applying the fold/unfold transformation rules as described in Section 3.2.
We introduce a specialised predicate
  4. sp(X,Y,N) :- X>=0, Y>=0, p(X,Y,N).
whose constraint is a generalisation of the one occurring in the body of the goal clause 1.
Then, by unfolding clause 4, we get
  5. sp(X,Y,N) :- X>=0, Y>=0, X>=N, X>Y.
  6. sp(X,Y,N) :- X>=0, Y>=0, X<N, X1=X+1, Y1=X1+Y, p(X1,Y1,N).
42 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

   The constraint in the body of clause 6 implies X1>=0, Y1>=0, and hence we can
fold this clause using clause 4. By also folding the goal clause 1 and simplifying the
constraints, we derive the following specialised set of clauses
  7. false :- X=0, Y=0, sp(X,Y,N).
  8. sp(X,Y,N) :- Y>=0, X>=N, X>Y.
  9. sp(X,Y,N) :- X>=0, Y>=0, X<N, X1=X+1, Y1=X1+Y, sp(X1,Y1,N).
Thus, the eﬀect of specialisation has been to add the constraint X>=0,Y>=0 to both
the recursive clause 9 and the constrained fact 8. Now, Eldarica (and Spacer/Z3) easily
computes the following model for the derived specialised clauses 7–9:
      sp(X,Y,N) :- X>=Y+1, Y>=0.
   Several algorithms have been proposed to mechanise CHC specialisation (Craig and Leuschel
2003, Fioravanti et al. 2001a, Peralta and Gallagher 2003). As already mentioned in Sec-
tion 3.2, these algorithms control the application of the unfolding rule (local control)
and, more crucially, the introduction of suitable specialised predicates (global control).
We refer to the original papers for a detailed presentation of those algorithms. Here we
will only discuss the role of constraint generalisation for global control.
   Some specialisation algorithms manage the global control by maintaining a set Defs
(possibly structured as a tree that records the various transformation paths) of specialised
predicate definitions, that is, a set of clauses of the form sp(X) ← c, A(X), where: (i) sp
is a new predicate symbol not occurring in P ∪ Q ∪ Defs, (ii) X is a tuple of variables,
and (iii) A(X) denotes an atom whose variables are the components of the tuple X.
   New predicate deﬁnitions are introduced by means of generalisation functions acting
on clauses. These functions use generalisation operators acting on constraints as we now
indicate.
Definition 2 (Generalisation)
Given two constraints c and d in D, we say that d is more general than c, written c ⊑D d,
if D |= ∀(c → d), where D is the constraint interpretation of D. A generalisation of two
constraints c1 and c2 is a constraint, denoted ω(c1 , c2 ), such that: (i) c1 ⊑D ω(c1 , c2 ), and
(ii) c2 ⊑D ω(c1 , c2 ). The function ω is called a generalisation operator on D. (In general,
ω may be non-commutative.)
   We say that an inﬁnite sequence g0 ⊑D g1 ⊑D . . . of constraints stabilises if there exists
n > 0 such that gn ⊑D gn−1 . The generalisation operator ω is a widening operator if,
for every inﬁnite sequence c0 , c1 , . . . of constraints, the inﬁnite sequence g0 , g1 , . . ., where:
(1) g0 = c0 , and (2) for all i ≥ 0, gi+1 = ω(gi , ci+1 ), stabilises.
   Given two clauses C: sp1(X) ← c, A(X) and D: sp2(X) ← d, A(X) (modulo the order
of the variables in the tuple X), a generalisation of C and D, denoted gen(C, D), is the
clause sp-gen(X) ← ω(proj(c, X), proj(d, X)), A(X), and gen is called a generalisation
function.
   Widening operators on the LRA constraint domain have been ﬁrst introduced in
the ﬁeld of abstract interpretation (Cousot and Cousot 1977) (see also Section 5) and
later used for the specialisation of constraint logic programs (Fioravanti et al. 2001a,
Craig and Leuschel 2003, Peralta and Gallagher 2003). Widening is often combined with
the computation of the convex-hull of a disjunction of linear constraints (Cousot and Halbwachs
1978), which may help discover relations among variables.
   Many specialisation algorithms achieve termination by using a generalisation operator
Analysis and Transformation of Constrained Horn Clauses for Program Verification 43

that is based on a widening operator on constraints. Indeed, any sequence of clauses
obtained by repeatedly applying such an operator is necessarily ﬁnite.
   A simple example of a widening operator in the LRA constraint domain, is deﬁned as
follows. Let c1 = a1 ∧ . . . ∧ an be a constraint, where a1 , . . . , an are atomic constraints of
the form p ≥ 0 or p > 0, and p is a linear polynomial. Given a constraint c2 , the widening
                                              V
of c1 with respect to c2 , denoted c1 ∇c2 , is ni=1 {ai | c2 ⊑LRA ai }. This widening operator
can also be extended to the case when some of the ai ’s are equalities, by ﬁrst splitting
them into conjunctions of inequalities.
   Now, we see how, in our example, the generalisation operator based on the widening ∇,
determines the introduction of the predicate sp. We start oﬀ from the goal clause 1, and
we deﬁne a new predicate whose body is exactly the body of that goal:
     10. sp1(X,Y,N) :- X=0, Y=0, p(X,Y,N).
Then, by unfolding clause 10, we get
     11. sp1(X,Y,N) :- X=0, Y=0, X>=N, X>Y.
     12. sp1(X,Y,N) :- X=0, Y=0, X<N, X1=X+1, Y1=X1+Y, p(X1,Y1,N).
Clause 11 has an unsatisﬁable body and is deleted. Clause 12 is simpliﬁed as follows:
     13. sp1(X,Y,N) :- X=0, Y=0, 0<N, X1=1, Y1=1, p(X1,Y1,N).
Thus, we introduce a new specialised predicate deﬁned as follow:
     14. sp2(X,Y,N) :- 0<N, X=1, Y=1, p(X,Y,N).
whose body has a constraint that is the projection of the constraint of clause 13 onto
the variables of atom p(X1,Y1,N) (we have renamed the variables). The comparison of
clauses 10 and 14 shows that, by iterating the unfolding and projection operations, the
specialisation would generate an inﬁnite sequence of specialised predicate deﬁnitions.
   Some specialisation algorithms avoid nontermination by applying the generalisation
function gen to pairs of clauses (C, D), where C is an ancestor of D in the tree Defs
of specialised predicate deﬁnitions, and the two clauses have the same atom in their
body. In our example, clause 10 is the parent of clause 14 in Defs. Thus, we apply the
generalisation function gen based on the widening operator ∇ to the pair (clause 10,
clause 14). The value of gen is computed by applying the operator ∇ to the constraints
appearing in the two clauses, as follows:
                                                         
    (X>=0, X=<0, Y>=0, Y=<0) ∇ (0<N, X=1, Y=1) = (X>=0, Y>=0)
where the left operand has been obtained by splitting the equalities of clause 10 into
conjunctions of inequalities. Thus, the result of applying gen to (clause 10, clause 14) is
clause 4, which deﬁnes predicate sp.
   In some cases, in order to verify the satisﬁability of P ∪ Q, it is useful to specialise the
clauses by propagating constraints occurring in the constrained facts of P . Various ap-
proaches can be followed. In the case where all clauses in P ∪Q are linear, we can apply the
Reversal transformation (De Angelis et al. 2014a), which, for each clause, interchanges its
head with its body. The Reversal transformation is related to the transformation of regu-
lar grammars from right recursive to left recursive (and vice versa) (Brough and Hogger
1991). For instance, the clauses for reachability presented in Section 4.2 can be trans-
formed from:
     reach(St) :- init(St).
     reach(St1) :- reach(St), tr(St,St1).
     false :- reach(St), error(St).
to
44 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

  false :- init(St), reach(St).
  reach(St) :- tr(St,St1), reach(St1).
  reach(St) :- error(St).
and vice versa. Note that in the original set of clauses the predicate reach holds for
the states that are reachable from the initial ones, while in the clauses obtained after
Reversal reach holds for the states from which error states are reachable. Reversal is
a sound and complete transformation. After Reversal we can specialise the clauses with
respect to the constrained goal and propagate the constraint deﬁning init(St).
   As mentioned above, also the QA transformation has the eﬀect of simulating bottom-
up evaluation through standard top-down execution. Thus, a technique for propagating
constraints from constrained facts is to specialise a set of clauses with respect to the
constrained goals, after applying the QA transformation to the original clauses. An ad-
vantage of the QA transformation over Reversal is that it can be applied to non-linear
clauses. However, the QA transformation may transform a linear clause into a non-linear
one, while Reversal preserves linearity.
   Constraint strengthening is another transformation technique that has been proposed
for propagating constraints from constrained goals and constrained facts (Kaﬂe and Gallagher
2017a). A strengthening of a clause H ← c, A1 , . . . , An is a clause H ← c′ , A1 , . . . , An , such
that c′ ⊑D c. Note that replacing c′ by false is strengthening. Constraint strengthening
of clauses is a complete transformation in the sense of Deﬁnition 1, and thus can be used
to check unsatisﬁability. However, in general, constraint strengthening is not sound, as it
can transform a set of unsatisﬁable clauses into a set of satisﬁable clauses (for example,
{false :- p., p.} can be transformed into {false :- false, p., p.}).
   One way to achieve a sound and complete constraint strengthening of a set P ∪ Q of
CHCs is to add constraints that are a consequence of the body of the clause where the
strengthening is realised. Let us see how we can obtain such a constraint strengthening.
Consider a predicate p in P , and suppose that lm(P, D) |= ∀(p(X) → d). Then, every clause
in P of the form p(X) ← c, B, can be replaced by p(X) ← c, d, B, and every clause in P ∪Q
of the form H ← c, p(X), B, where H may be false, can be replaced by H ← c, d, p(X), B.
If P ′ ∪ Q′ is obtained by all these applications of constraint strengthening, then P ∪ Q is
satisﬁable if and only if P ′ ∪ Q′ is satisﬁable.
   Properties of the form lm(P, D) |= ∀(p(X) → d) to be used for strengthening P ∪ Q, can
be discovered by applying abstract interpretation techniques (see Section 5). A strategy
proposed by Kaﬂe and Gallagher (2017a) consists in transforming P ∪ Q by the following
three steps, where, without loss of generality, we assume that Q consists of a single goal
false ← e, A (we can always get to this case by introducing a new predicate deﬁned in
terms of the goals in Q).
Step (1). Apply the QA transformation to P ∪ {false ← e, A}, and derive a new set of
clauses P a ∪ P q ∪ {false ← e, Aa } (see Section 3.4);
Step (2). Apply Convex Polyhedral Analysis (CPA) (Cousot and Halbwachs 1978, Benoy and King
1997) to construct an over-approximation M of lm(P a ∪ P q , D).
Step (3). Since CPA computes a convex over-approximation for each predicate, without
loss of generality, we may assume that M has a single constrained fact pa (X) ← g, for the
answer predicate pa , and by the soundness and completeness of the QA transformation,
p(X) ← g is also an over-approximation of the atoms for p that are true in lm(P, D),
that is, {p(a) | p(a) ∈ lm(P, D)} ⊆ {p(a) | D |= ∃(g{X/a})}. Thus, lm(P, D) |= ∀(p(X) →
Analysis and Transformation of Constrained Horn Clauses for Program Verification 45

proj(g, X)). The QA transformation at Step (1), enforces that the CPA bottom-up con-
struction performed at Step (2) simulates top-down, goal-directed constraint propagation.
  For example, consider again clauses 1-3 above. We rewrite them here for the reader’s
convenience.
  1. false :- X=0, Y=0, p(X,Y,N).
  2. p(X,Y,N) :- X>=N, X>Y.
  3. p(X,Y,N) :- X<N, X1=X+1, Y1=X1+Y, p(X1,Y1,N).

At Step (1) the QA transformation derives the following new set of clauses, which is
satisﬁable if and only if clauses 1-3 are satisﬁable:
  false :- X=0, Y=0, p_a(X,Y,N).
  p_a(X,Y,N) :- p_q(X,Y,N), X>=N, X>Y.
  p_a(X,Y,N) :- p_q(X,Y,N), X<N, X1=X+1, Y1=X1+Y, p_a(X1,Y1,N).
  p_q(X,Y,N) :- X>=N, X>Y.
  p_q(X1,Y1,N) :- X<N, X1=X+1, Y1=X1+Y, p_q(X,Y,N).

At Step (2) CPA derives the following model:
  p_q(X,Y,N) :- X>=N, X>Y.
  p_a(X,Y,N) :- X>=N, X>Y.
which allows us to infer that lm({2,3}, LRA) |= ∀X,Y,N. p(X,Y,N) → X>=N, X>Y.
At Step (3), by constraint strengthening, we get:
  1’. false :- X=0, Y=0, X>=N, X>Y, p(X,Y,N).
  2’. p(X,Y,N) :- X>=N, X>Y, X>=N, X>Y.
  3’. p(X,Y,N) :- X>=N, X>Y, X<N, X1=X+1, Y1=X1+Y,
                  X1>=N, X1>Y1, p(X1,Y1,N).
where we have underlined the added constraints. Now, the constraint appearing in the
body of clause 1’ is unsatisﬁable, and hence the set {1’,2’,3’} of clauses is trivially
satisﬁable.
  The dual transformation to constraint strengthening is constraint weakening, that is,
the replacement of the clause constraint c by c′ such that c ⊑D c′ . Constraint weakening
applied to the clauses of P ∪Q is a sound transformation but, in general, it is not complete.
Thus, if the weakened set P ′ ∪ Q′ of CHCs is satisﬁable, so is the original set. Constraint
weakening is related to abstraction techniques, as every D-model of P ′ ∪Q′ (where false is
considered as a user-deﬁned predicate symbol) is an over-approximation of lm(P ∪ Q, D).
   Finally, we point out that, as long as CHC transformations are sound and complete,
we can compose any number of them while preserving both satisﬁability and unsatisﬁ-
ability. This opens the way to the design of (un)satisﬁability checking algorithms that
incorporate CHC transformations as building blocks. Some of these transformation-based
algorithms are implemented in the CHC solvers VeriMAP (De Angelis et al. 2014b) and
RAHFT (Kaﬂe et al. 2016).
   VeriMAP generates veriﬁcation conditions by specialising an interpreter for the small-
step semantics of (a fragment of) the C language with respect to a given program, a
precondition, and an error property (see Section 4). The tool generates linear CHCs.
Then VeriMAP iterates the following three steps. (i) The specialisation of the CHCs
with respect to constrained goals. (ii) The analysis of the specialised CHCs, based on
unfolding and clause deletion, to determine whether or not there is a derivation of false.
If such a derivation is found, then the clauses are unsatisﬁable, else if the analysis is able
46 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

to discover that such a derivation is impossible, because false does not depend on any
predicate with constrained facts, then the clauses are satisﬁable. Otherwise, the analysis
is inconclusive. (iii) The reversal of the CHCs, in the case when the analysis at Step (2) is
inconclusive. Reversal enables us to alternate the propagation of the constraints occurring
in the goals with the propagation of those occurring in the facts.
   RAHFT (Reﬁnement of Abstraction in Horn clauses using Finite Tree automata) com-
bines: (1) the preprocessing of the input CHCs by constraint strengthening, as recalled
above, (2) the construction of an over-approximation of the least model of the clauses,
based on Convex Polyhedral Analysis, and (3) the CHC reﬁnement based on Finite Tree
Automata (FTA) techniques (Kaﬂe and Gallagher 2017a), which in the case where the
over-approximation computed at Step (2) allows for unfeasible derivations of false (i.e.,
spurious counterexamples), transforms the CHCs in such a way that the new clauses
avoid those unfeasible derivations (see Section 6.3 for more details). Steps (1)–(3) can be
iterated until a conclusive result is reported.


                                 6.2 Predicate Pairing
CHC specialisation is able to produce specialised versions of an existing predicate by
introducing a new predicate deﬁned in terms of a constrained atom. In some applications
it is very useful to exploit the full power of fold/unfold transformations, which allow us to
introduce a new predicate deﬁned as a constrained conjunction of atoms (see Section 3).
This technique is called predicate pairing (De Angelis et al. 2018a), and is an adapta-
tion to CHC veriﬁcation of fold/unfold transformation strategies previously proposed for
combining two or more predicates with similar recursive deﬁnitions into a single new
predicate (Burstall and Darlington 1977, Pettorossi and Proietti 1994). In essence, pred-
icate pairing is also equivalent to conjunctive partial deduction (De Schreye et al. 1999),
which indeed extends partial deduction by enabling the specialisation of conjunctions of
atoms.
   Algorithms and implementations of predicate pairing, also enhanced with constraint
propagation techniques such as the ones described in Section 6.1, have been presented
in the literature (De Angelis et al. 2016, 2017a, 2018a). In particular, we refer to those
papers for the issue of introducing in a fully automated way the new predicate deﬁnitions
needed for fold/unfold transformations. Here, we will show through examples two appli-
cations of predicate pairing for relational verification and for the veriﬁcation of properties
of programs that compute on Algebraic Data Types.


                               6.2.1 Relational verification
Relational program properties are properties that relate two diﬀerent programs or two
executions of the same program. The veriﬁcation of relational program properties, also
called relational veriﬁcation, is useful during the process of software development, where
the programmer often produces several versions of the same program, and may want to
formally prove relations between old and new program versions. Relational properties
that have been studied in the literature include various forms of program equivalence,
relational cost analysis (in terms of computation time or any other resource consumption),
non-interference for software security, and relative correctness (Barthe et al. 2011, Benton
Analysis and Transformation of Constrained Horn Clauses for Program Verification 47

2004, Churchill et al. 2019, Çiçek et al. 2017, Godlin and Strichman 2008, Lahiri et al.
2013, Lopes and Monteiro 2016, Zaks and Pnueli 2008).
   Many relational program properties can be speciﬁed by extending pre/postconditions
in the style of Hoare triples to pairs of programs, rather than a single program (Barthe et al.
2011). Given two imperative programs P and Q, with disjoint tuples, say x and y, re-
spectively, of global variables and two formulas ϕ(x, y), ψ(x, y), the relational property
{ϕ(x, y)} P ∼ Q {ψ(x, y)} holds if the following holds: if the inputs of P and Q satisfy the
pre-relation ϕ(x, y) and P and Q both terminate, then the outputs of P and Q satisfy
the post-relation ψ(x, y).
   Several papers have advocated the formalisation of relational veriﬁcation problems
in CHCs and the use of a CHC solver, possibly enhanced by ad hoc solving tech-
niques (Chen et al. 2019, De Angelis et al. 2016, 2018a, Felsing et al. 2014, Mordvinov and Fedyukovich
2017, 2019, Shemer et al. 2019, Zhou et al. 2019).
   The relational property {ϕ(x, y)} P ∼ Q {ψ(x, y)} has the following straightforward
translation into CHCs:
  false ← notpost(X2, Y 2), pre(X1, Y 1), p(X1, X2), q(Y 1, Y 2)               (RelProp)
where: (i) X1 and Y 1 are the values of x and y, respectively, before execution of P
and Q, (ii) X2 and Y 2 are the values of x and y, respectively, after execution of P and Q,
(iii) pre(X1, Y 1) is the translation of ϕ(x, y) into a CHC predicate, (iv) notpost(X2, Y 2)
is the translation of ¬ψ(x, y) into a CHC predicate, (v) p(X1, X2) and q(Y 1, Y 2) are the
input/output relations of programs P and Q, respectively, derived by one of the methods
described in Section 4 (for instance, by specialising the interpreter of the imperative
language with respect to the two programs). The order of the constraints and atoms in
the body of (RelProp) is not signiﬁcant from a logical point of view but, as usual, we
write constraints before atoms. The relational property {ϕ(x, y)} P ∼ Q {ψ(x, y)} holds if
and only if the set of CHCs consisting of (RelProp) together with the clauses for notpost,
pre, p, and q, is satisﬁable.
   Many relational properties can be deﬁned by using constraints as pre/postconditions.
For instance, program equivalence is simply translated as
  false ← X2 6= Y 2, X1 = Y 1, p(X1, X2), q(Y 1, Y 2)                            (Equiv)
Non-interference, a property that guarantees information-ﬂow security (Goguen and Meseguer
1982), is another relational property that can be easily expressed in CHCs. Let us con-
sider a program P whose variables are partitioned into a set of public variables (or low
security variables) and a set of private variables (or high security variables). We say that
P satisﬁes the non-interference property if any two terminating executions of P , starting
with the same initial values of the public variables, but possibly with diﬀerent values of
the private variables, compute the same values of the public variables. Thus, if a program
satisﬁes the non-interference property, an attacker cannot acquire information about the
private variables by observing the input/output relation between the public variables,
which are functionally dependent on the public input variables only.
   The non-interference property for program P is translated into the following goal:
  false ← OutL6= OutL1, L = L1, p(L, H, OutL), p(L1, H1, OutL1)                 (NonInt)
where: (i) the predicate p(L, H, OutL) is the input/output relation of P , (ii) L and H are
the tuples of values of the public and private variables, respectively, before the execution
of P , and (iii) OutL is the tuple of values of the public variables upon termination of P .
48 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

   Unfortunately, it is often the case that the straightforward translation of relational
properties into CHCs is not suﬃcient to allow veriﬁcation using state-of-the-art solvers.
Indeed, the strategies for checking satisﬁability employed by those solvers deal with the
sets of clauses encoding the semantics of each of the two programs in an independent
way, thereby failing to take full advantage of the interrelations between the two sets of
clauses. Let us illustrate this limitation through an example.
   Let us consider the two programs of Figure 5. Program Sum_upto_rec computes the
sum of the ﬁrst x1 positive integers and program Prod computes the product of x2 by y2
by summing up x2 times the value of y2.
   /* Program Sum_upto_rec */                        /* Program Prod */

   int x1, z1;                                       int x2, y2, z2;
   int f(int n1){                                    int g(int n2, int m2){
    int r1;                                            int r2 = 0;
                                                       while (n2 > 0) {
    if (n1 <= 0) {r1 = 0;}                               r2 += m2;
    else {r1 = f(n1-1)+n1; }                             n2--;
    return r1;                                           }
    }                                                  return r2;
                                                       }
   void sum_upto_rec() {
    z1 = f(x1);                                      void prod() {
    }                                                  z2 = g(x2,y2);
                                                       }
Figure 5. The programs Sum_upto_rec and Prod.

  We want to verify that the following relational property holds:
  {x1=x2, x2 ≤ y2} Sum_upto_rec ∼ Prod {z1 ≤ z2}                               (Leq)
meaning that, if x1=x2, x2 ≤ y2 holds before the execution of Sum_upto_rec and Prod,
then z1 ≤ z2 holds after their execution. Property Leq cannot directly be proved using
techniques based on structural similarity of programs (Barthe et al. 2011, Felsing et al.
2014), because Sum_upto_rec is a (non-tail) recursive program and Prod is an iterative
program.
  By interpreter specialisation (see Section 4) and constraint propagation, the relational
property Leq is translated into the set of CHCs over LIA shown in Figure 6.

  false :- Z1>Z2, X1=X2, X2=<Y2, sur(X1,Z1), pr(X2,Y2,Z2).
  sur(X,Z) :- f(X,Z).                         \* for sum_upto_rec *\
  f(N,Z) :- N=<0, Z=0.
  f(N,Z) :- N>=1, N1=N-1, Z=R+N, f(N1,R).
  pr(X,Y,Z) :- W=0, X=<Y, g(X,Y,W,Z).         \* for prod *\
  g(N,P,R,R2) :- N=<0, N=<P, R>=0, R2=R.
  g(N,P,R,R2) :- N>=1, N=<P, R>=0, N1=N-1, R1=P+R, g(N1,P,R1,R2).
Figure 6. LeqCHCs: Translation into CHCs of the relational property Leq.

   As mentioned above, CHCs solvers using linear integer arithmetic are unable to prove
the satisﬁability of the set of clauses in Figure 6. This is due to the fact that those solvers
look for a LIA-deﬁnable model, and no such a model exists.
   In order to deal with this limitation one could consider CHCs with solvers for the theory
of non-linear integer arithmetic constraints (Borralleras et al. 2012). Indeed, one way to
prove that LeqCHCs is satisﬁable is to discover quadratic relations among predicate
Analysis and Transformation of Constrained Horn Clauses for Program Verification 49

variables, such as (X1=<0, Z1=0) ∨ (X1>=1, Z1=X1×(X1-1)/2) for sur(X1,Z1), and
(X2=<0, Z2=0) ∨ (X2>=1, Z2=X2×Y2) for pr(X2,Y2,Z2). However, this extension has to
cope with the additional problem that the satisﬁability problem for non-linear constraints
is, in general, undecidable (Matiyasevich 1970) (see also Section 2).
   An alternative approach is based on applying fold/unfold transformations according
to the predicate pairing strategy (De Angelis et al. 2016, 2018a). This transformation
strategy introduces new predicates deﬁned as conjunctions of already existing predicates,
and then derives (possibly recursive) clauses for the new predicates by applying the
unfolding and folding rules, along with clause deletion and constraint replacement.
   In our example, by predicate pairing, we introduce a new predicate fg, deﬁned as the
conjunction of f and g as follows:
  fg(X1,Z1,Y2,W,Z2) :- f(X1,Z1), g(X1,Y2,W,Z2).
and then, by unfolding and folding, the clauses of Figure 6 are transformed into the ones
shown in Figure 7.
  false :- Z1>Z2, X1=<Y2, W=0, fg(X1,Z1,Y2,W,Z2).
  fg(N,Z1,Y,W,Z2) :- N=<0, N=<Y, W>=0, Z1=0, Z2=W.
  fg(N,Z1,Y,W,Z2) :- N>=1, N=<Y, W>=0, N1=N-1, Z1=R+N, M=Y+W,
        fg(N1,R,Y,M,Z2).

Figure 7. LeqPP: Clauses derived from LeqCHCs by predicate pairing.

   The eﬀect of predicate pairing is that it often enables the inference of linear relations
among the variables occurring in conjunctions of predicates in a direct way, without hav-
ing to derive non-linear relations with other variables as an intermediate step. Indeed, in
our example, state-of-the-art solvers for CHCs with LIA are able to prove the satisﬁa-
bility of the clauses of Figure 7 obtained by predicate pairing, and hence the validity of
the relational property Leq. In particular, Eldarica computes the following model:
  fg(X1,Z1,Y2,W,Z2) :- Z2-W>=Z1, Z1>=0, W>=0.


                     6.2.2 Solving CHCs over Algebraic Data Types
Constraint solving techniques have been applied to the veriﬁcation of programs manipu-
lating recursively deﬁned data structures, such as lists and trees and, in general, algebraic
data types (ADTs). In most applications, constraint solvers (and, in particular, SMT
solvers), are used as a back-end by program veriﬁers, such as Boogie (Barnett et al.
2006), Leon (Suter et al. 2011), Why3 (Filliâtre and Paskevich 2013), Dafny (Leino
2013), and Stainless (Hamza et al. 2019), to translate and check program assertions
provided by the programmer.
   Many constraint solvers implement techniques for checking the satisﬁability of con-
straints on ADTs (see, for instance, https://rise4fun.com/Z3/tutorial/guide for
Z3). However, when we consider CHCs over ADTs with user-deﬁned predicates, similarly
to the case of CHCs on other domains, the satisﬁability problem becomes undecidable and
we need to develop incomplete solving methods. While methods based on resolution work
well for proving unsatisﬁability (indeed, they are sound and complete for unsatisﬁability,
as mentioned in Section 2), they are not as eﬀective for proving satisﬁability.
   One recent line of research has proposed the extension of CHC (and SMT) solv-
ing over ADTs with inductive reasoning (Reynolds and Kunčak 2015, Suter et al. 2011,
50 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

Unno et al. 2017) by incorporating methods derived from the ﬁeld of automated theorem
proving (Bundy 2001).
   An alternative approach to the extension of CHC solvers with induction is based on the
application of fold/unfold transformations with the objective of removing data structures
while preserving satisﬁability. The transformation-based approach is related to techniques
for improving the eﬃciency of execution of functional and logic programs, such as defor-
estation (Wadler 1990), unnecessary variable elimination (Proietti and Pettorossi 1995),
and conjunctive partial deduction with redundant argument ﬁltering (De Schreye et al.
1999).
   Recent work has shown that methods for removing data structures are also very eﬀec-
tive for improving CHC solvers (De Angelis et al. 2018b). The advantage of this approach
is that it allows us to separate the reasoning on inductively deﬁned data structures from
the reasoning on clause satisﬁability over basic types, such as booleans or integers. For
instance, when dealing with CHCs over trees of integers, the transformation attempts to
derive an equisatisﬁable set of clauses with constraints on integers only, which can then
be solved by using, for instance, the approximation-based methods of Section 5.
   As an example of application of the transformation-based approach to the veriﬁcation
of call-by-value functional programs, we consider the following Tree-Processing program,
which we write according to the OCaml syntax (Leroy et al. 2017).
  type tree = Leaf | Node of int ∗ tree ∗ tree ;;
  let min x y = if x < y then x else y ;;
  let rec min -leafdepth t = match t with
                   | Leaf –> 0
                   | Node(x, l, r) –> 1 + min (min -leafdepth l) (min -leafdepth r) ;;
  let rec left -drop n t = match t with
                   | Leaf –> Leaf
                   | Node(x, l, r) –> if n <= 0 then Node(x, l, r) else left -drop (n−1) l ;;
In this program: (i) tree is the type of the binary trees with integers at the internal nodes,
(ii) (min -leafdepth t) returns the length of a shortest path from the root of the tree t
to a leaf node, and (iii) (left -drop n t) returns the subtree of t rooted at the n-th node
along the leftmost path from the root of t, if the length of that path is at least n, and
Leaf otherwise. For instance, we have that:
   min -leafdepth (Node(5,(Node(8,Leaf,Leaf)),Leaf)) = 1, and
   left -drop 1 Node(5,(Node(8,Leaf,Leaf)),Leaf)) = Node(8,Leaf,Leaf).
Let us also consider the following property Prop, which we would like to verify for the
Tree-Processing program:
  ∀n, t. n ≥ 0 ⇒ ((min -leafdepth (left -drop n t)) + n) ≥ (min -leafdepth t). (Prop)
The direct translation into CHCs of a ﬁrst-order functional program with the call-by-
value semantics is straightforward (Unno et al. 2017), although one could also follow the
approach based on interpreter specialisation. We get the following set of clauses:
  false :- N>=0, M+N<K,
     left_drop(N,T,U), min_leafdepth(U,M), min_leafdepth(T,K).
  left_drop(N,leaf,leaf).
  left_drop(N,node(X,L,R),node(X,L,R)) :- N=<0.
  left_drop(N,node(X,L,R),T) :- N>=1, N1=N-1, left_drop(N1,L,T).
Analysis and Transformation of Constrained Horn Clauses for Program Verification 51

  min_leafdepth(leaf,M) :- M=0.
  min_leafdepth(node(X,L,R),M) :- M=M3+1,
     min_leafdepth(L,M1), min_leafdepth(R,M2), min(M1,M2,M3).
  min(X,Y,Z) :- X<Y, Z=X.
  min(X,Y,Z) :- X>=Y, Z=Y.
where a predicate f(X,Y) is the translation of the relation ‘f x evaluates to y’.
  This set of CHCs is satisﬁable iﬀ Prop holds for Tree-Processing. However, CHC solvers
without induction (e.g., Eldarica and Spacer/Z3) are not able to check satisﬁability,
because of the presence of variables ranging over trees.
  To solve this problem, we can apply the Elimination Algorithm (De Angelis et al.
2018b), which automatically introduces two new predicates:
  new1(N,M,K) :- left_drop(N,T,U), min_leafdepth(U,M),
        min_leafdepth(T,K).
  new2(M) :- min_leafdepth(L,M).
and by applying fold/unfold transformations, derives the following equisatisﬁable set of
clauses without tree variables, whose constraints are in LIA only:
  false:- N>=0, M+N<K, new1(N,M,K).
  new1(N,M,K) :- M=0, K=0.
  new1(N,M,K) :- N=<0, M=M3+1, K=M, new2(M1), new2(M2), min(M1,M2,M3).
  new1(N,M,K) :- N>=1, N1=N-1, K=K3+1,
        new1(N1,M,K1), new2(K2), min(K1,K2,K3).
  new2(M) :- M=0.
  new2(M) :- M=M3+1, new2(M1), new2(M2), min(M1,M2,M3).
Now, state of the art solvers for CHCs on LIA constraints are able to prove the satisﬁ-
ability of these clauses. In particular, Eldarica computes the following model:
  new1(A,B,C) :- A+(B-C)>=0.
  new1(A,B,C) :- B>=C.
  new2(A) :- true.
In some cases, in order to remove inductively deﬁned ADTs from CHCs, fold/unfold
transformations need to be complemented by the discovery of suitable intermediate lem-
mas, which allow the replacement of subconjunctions occurring in the body of a clause
by a new one. This is not surprising, as the need for lemma discovery has long been
recognised as a key factor for the automation of inductive proofs (Bundy 2001). A re-
cent transformation technique uses the idea that lemmas can be generated by means
of the so-called difference predicates, based on the impossibility of applying the folding
rule (De Angelis et al. 2020).

                    6.3 Other Transformation-based Techniques
In this section we summarise other satisﬁability-preserving transformations of CHCs that
have been developed for speciﬁc applications. Their correctness in most cases follows from
the general principles of semantics-preserving transformations presented in Section 3
although the transformation algorithms are not presented in that style.

                         6.3.1 Refinement based on tree automata
Recall that an and-tree represents a top-down derivation (see Section 5.2). The success
set of a set of CHCs P , SS(P )D , can be identiﬁed with the set of successful and-trees
of P . We say that t is a successful and-tree for A if t is successful and has root hA, true, Ci.
52 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

   SS(P )D = {A ← proj(constr(t), vars(A)) | t is a successful and-tree for A}
Kaﬂe and Gallagher (2017b) develop a transformation preserving the set of successful
and-trees for a set of CHCs. The transformation is achieved by associating a tree au-
tomaton AP with a set P of CHCs, such that the set of trees recognised by AP , called
L(AP ), is the set of and-trees (both successful and failed) for P . If a spurious counterex-
ample is discovered while attempting to show satisﬁability of P (such as in abstraction-
reﬁnement procedures, see Section 5.3), then we can construct the corresponding failed
and-tree t. A tree automaton for the diﬀerence language L(AP ) \ {t} is then constructed;
from this a new set P ′ of CHCs can be derived from this tree automaton. The set of
feasible and-trees of P is preserved in P ′ , since only one infeasible tree was removed;
thus P ′ has the same success set as P . Hence the transformation from P to P ′ is sound
and complete.
   That work generalised the approach of reﬁnement by trace abstraction (Heizmann et al.
2009) from string traces to tree traces. Interpolation techniques can be applied to gener-
alise an infeasible and-tree t to a set At of infeasible and-trees (Wang and Jiao 2016),
and the diﬀerence L(AP ) \ At is then computed, instead of L(AP ) \ {t}. Tree-automata
based reﬁnement was applied in the RAHFT CHC veriﬁcation tool (Kaﬂe et al. 2016).


                     6.3.2 Control-flow refinement by specialisation
A useful application of constraint propagation is control-flow refinement (Doménech et al.
2019), which transforms a set of clauses by specialising with respect to internal con-
straints rather than constrained goals or constrained facts. The eﬀect is to produce
diﬀerent specialised versions of predicates arising from diﬀerent instances that are ob-
tained in derivations, and hence control-ﬂow reﬁnement is a form of polyvariant specialisa-
tion (Bulyonkov 1984, Jacobs et al. 1990, Giannotti and Hermenegildo 1991, Jones et al.
1993, Puebla and Hermenegildo 1999), as discussed in Section 5.2 (see Figure 4 and
Example 20). Polyvariant specialisation is often crucial in applications to program ver-
iﬁcation (Gulwani et al. 2009), allowing the inference of disjunctive invariants, which
cannot be discovered, for instance, by a direct application of convex polyhedral analy-
sis (Fioravanti et al. 2012, De Angelis et al. 2014a, Kaﬂe et al. 2018). Control-ﬂow reﬁne-
ment is especially useful for termination and complexity analysis, when it allows complex
loops to be decomposed into simpler ones, thus enabling the discovery of more precise
loop invariants or simpler ranking functions (Doménech et al. 2019). Polyvariant special-
isation introduces the additional issue of controlling the set of specialised versions of the
same predicate so as to achieve maximal precision and, at the same time, avoid the ex-
plosion in size of the transformed set of clauses (Doménech et al. 2019, Fioravanti et al.
2013, Kaﬂe et al. 2018, Puebla and Hermenegildo 1999, Ochoa et al. 2006, Leuschel et al.
1998).
Example 22
Let P be the following set of clauses.
  main :- while(X,Y,M).
  while(X,Y,M) :- X>0, Y<M, Y1=Y+1, while(X,Y1,M).
  while(X,Y,M) :- X>0, Y>=M, X1=X-1, while(X1,Y,M).
  while(X,Y,M) :- X=<0.
These clauses represent a while loop whose body contains a branch. Proof of program
Analysis and Transformation of Constrained Horn Clauses for Program Verification 53

properties, in particular termination of the loop, is hampered by the branch which ne-
cessitates inference of a lexicographical ranking function. After control-ﬂow reﬁnement,
we obtain the following clauses.
  main :- while0(X,Y,M).
  while0(X,Y,M) :- X>0, Y<M, Y1=Y+1, while1(X,Y1,M).
  while0(X,Y,M) :- X>0, Y>=M, X1=X-1, while2(X1,Y,M).
  while0(X,Y,M) :- X=<0.
  while1(X,Y,M) :- X>0, Y<M, Y1=Y+1, while1(X,Y1,M).
  while1(X,Y,M) :- X>0, Y>=M, X1=X-1, while2(X1,Y,M).
  while2(X,Y,M) :- X>0, Y>=M, X1=X-1, while2(X1,Y,M).
  while2(X,Y,M) :- X=<0.
The original while loop has been reﬁned into three versions:
  while0(X,Y,M) :- while(X,Y,M).
  while1(X,Y,M) :- X>0, while(X,Y,M).
  while2(X,Y,M) :- Y>=M, while(X,Y,M).
This yields separate loops (while1 and while2), each of which has a simple ranking
function (and the predicate while0 becomes a simple branch), and thus termination is
easily proved for the transformed clauses.


                        7 Related CHC-based Techniques
As already mentioned in Section 4, constrained Horn clauses have recently been applied
for modelling programs written in many diﬀerent programming languages. Besides pro-
grams, CHCs have also been used for encoding more abstract computational models
of various kinds, including Petri nets (Fribourg and Olsén 1997, Leuschel and Lehmann
2000), timed automata (Jaﬀar et al. 2004), linear hybrid automata (Banda and Gallagher
2009), concurrent systems (Delzanno and Podelski 1999, Fioravanti et al. 2001b, 2013a),
parameterized systems (Roychoudhury et al. 2000), process algebras (Fioravanti et al.
2013b) and business processes (De Angelis et al. 2019).
   Constraints ease the modelling of systems whose state space is inﬁnite, as data or time
values can be represented using variables ranging over inﬁnite domains. Usually, these
systems are represented as transition systems encoded as CHCs, and it is argued that the
CHCs generate the same transition system as the one deﬁned by the source system. The
predicates deﬁning the corresponding transition relation range from a simple collection of
constrained facts to more sophisticated operational semantics (in the latter case program
specialisation can be used for removing intermediate data structures).
  The most common application of CHCs in veriﬁcation is proving (or disproving) safety
properties, i.e., that ‘something bad never happens’ during computation. Notable exam-
ples of safety properties are partial correctness (Hoare triples), deadlock freedom (the
program does not enter a state from which it cannot make progress), and mutual ex-
clusion (no two processes, or threads, are in their critical sections at the same time).
However, CHCs have also been used for modelling other kinds of properties such as live-
ness properties stating that ‘something good will eventually happen’. Among them, there
are program termination and starvation freedom.
  Safety and liveness properties can be speciﬁed using temporal logics such as the
µ-calculus or the Computation Tree Logic (CTL) (Clarke et al. 1999), that can be en-
coded using CHCs. Diﬀerent methods have been developed for proving these properties
54 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

based on explicit ﬁxpoint construction (Delzanno and Podelski 2001), tabled resolution
(Roychoudhury et al. 2000), and co-induction (Gupta et al. 2007).
   A proof-based approach using logic programming is followed by Leuschel and Massart
(2000), where veriﬁcation of CTL properties is performed by combining tabulation and
partial evaluation. An extension to constraint logic programming based on program
specialisation of a CTL interpreter is presented by Fioravanti et al. (2001b, 2013a). In
both cases, the extension of logic programs with negation as (ﬁnite or inﬁnite) fail-
ure (Apt and Bol 1994) plays a central role in the proof procedures. Leuschel and Massart
(2000) handle negation by using under-approximations of the answers of predicate calls
as safe over-approximations of their negation, while Fioravanti et al. (2001b, 2013a) use
transformation rules that preserve the perfect model semantics of clauses with locally
stratiﬁed negation.
   Termination properties constitute a particular class of liveness properties, but they
are often treated separately and proved using specialised techniques. Termination anal-
ysis of Java bytecode programs based on constraint logic programs has been studied by
Albert et al. (2008) and Spoto et al. (2010). Termination properties are also proved by
applying CEGAR techniques on Horn-like clauses with existentially quantiﬁed variables
in their head (Beyene et al. 2013), and by reducing the termination problem to a safety
problem and using syntax-guided synthesis (Fedyukovich et al. 2018).
   Automatic complexity and resource analysis is closely related to CHC veriﬁcation and
has been an important subject of investigation in the CLP context (Debray et al. 1990,
1997, Debray and Lin 1993, Navas et al. 2007, Albert et al. 2011, López-García et al.
2012, 2016, Serrano et al. 2014, Klemen et al. 2018). Some of these analyses have been
developed for analysing CLP/CHC programs directly and also for analysing impera-
tive programs, by translation to CHCs, using diﬀerent representation levels as starting
point, such as source, bytecode, compiler intermediate representations (e.g., LLVM-IR),
or machine code. An area of particular interest in this context has been static analyses
for bounding the energy consumption of programs (Navas et al. 2008, 2009, Liqat et al.
2014, 2016, López-García et al. 2015, 2018).
  Recently, CHCs have been used for modelling the operational semantics of time-aware
business processes (De Angelis et al. 2019), whose activities have durations that are ei-
ther controllable (that is, determined by the organisation that executes the process), or
uncontrollable (determined by the environment). Controllability properties, which guar-
antee process completion independently of the values of the uncontrollable durations, are
encoded using reachability formulas with existential and universal quantiﬁers, and are
veriﬁed by combining resolution and constraint solving in LIA.
  Techniques for the veriﬁcation of higher-order functional programs have been developed
using machine learning (Champion et al. 2020) or extending CHCs to higher-order logic
(Burn et al. 2018). Other extensions of CHCs, such as existential and universal CHCs,
have been studied by Bjørner et al. (2015).
   Further applications of Horn clauses include veriﬁcation of smart contracts and security
protocols. Indeed, several approaches to veriﬁcation and analysis of smart contracts for
the Ethereum cryptocurrency are based on CHCs and use abstraction (Grishchenko et al.
2018, Kalra et al. 2018, Tsankov et al. 2018), possibly combined with partial evalua-
tion (Tsankov et al. 2018, Schneidewind et al. 2020). Moreover, abstract models of secu-
Analysis and Transformation of Constrained Horn Clauses for Program Verification 55

rity protocols are represented through Horn clauses in the automatic symbolic veriﬁer
ProVerif (Blanchet 2016), that uses resolution with free selection for verifying properties
of these protocols, such as secrecy, authentication, and process equivalence.


  Veriﬁcation is not the only validation task that can be conveniently carried out us-
ing CHCs. It is well known that constraints can be eﬀectively and eﬃciently used for
software testing (Gotlieb et al. 1998, Godefroid et al. 2005, Meudec 2001), and various
CHC-based techniques have been developed for test case generation (TCG) using diﬀer-
ent approaches.
  White-box TCG has been performed by means of bounded symbolic execution (Gómez-Zamalloa et al.
2010), after applying partial evaluation to derive CHCs from object-oriented or bytecode
programs (Albert et al. 2010). The approach has been extended to TCG for concurrent
programs (Albert et al. 2018) by integrating partial-order reduction techniques for mit-
igating state space explosion. Concolic testing (Godefroid et al. 2005), combining con-
crete and symbolic execution for TCG, has recently been applied to CLP programs
(Mesnard et al. 2020).
  A CLP-based approach exploiting uniﬁcation and constraint solving (Senni and Fioravanti
2012), combined with program transformation (Fioravanti et al. 2015), has been applied
to Bounded-Exhaustive Testing (BET) (Coppit et al. 2005), where the task is that of gen-
erating all input data satisfying a given property, and has shown to be very competitive
with respect to other approaches to BET.
   Some recent papers use CHCs for Property-Based Testing (PBT) (Claessen and Hughes
2000), where inputs are randomly generated so that input and output pairs satisfy some
given properties. The idea of using properties deﬁned by predicates as generators for
testing arises naturally in the CLP/CHC context, since calls to predicates with free
variables will instantiate (or constrain) those variables to values that will eventually
cover all the success set, as shown in Section 2.4.2. In particular, the Ciao assertion
framework (Hermenegildo et al. 1999, 2005, Puebla et al. 2000) implements assertion-
based testing: the properties that appear in assertions are deﬁned using predicates, and
then the preconditions of such assertions act as generators that are used to drive the
run-time testing of those parts of assertions that are not discharged at compile time,
essentially embodying the PBT approach. Recent work (Casso et al. 2019) shows how
this generation process can be performed for complex properties and random values
by executing the predicates deﬁning such properties under diﬀerent search rules (e.g.,
breadth-ﬁrst, iterative deepening, random), available in the Ciao system.
  Other work is aimed more speciﬁcally at PBT, such as PrologCheck (Amaral et al.
2014), which provides custom test data generators and a predicate speciﬁcation language
for PBT of Prolog programs. When the input consists of data structures that must
satisfy complex properties, such as sorted lists or AVL trees, naive generation is not
always suitable and programmers may have to write custom generators. The ProSyT
tool (De Angelis et al. 2019) relieves programmers from writing such generators for PBT
of Erlang programs. Inputs are automatically generated from functional speciﬁcations
by interleaving (via coroutining) symbolic data structure generation, constraint solving,
and random variable instantiation.
56 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

                                 8 Future Directions

The idea that CHCs provide a common logical framework (or lingua franca) for program
veriﬁcation problems has gained traction in recent years (McMillan 2013, Bjørner et al.
2015) and has been boosted by the development of powerful satisﬁability checkers for a
range of constraint domains. The roots of the idea can be traced to the early years of
(constraint) logic programming, and many works in the ﬁeld of CLP in the past three
decades have exploited the expressiveness of CHCs and their model- and proof-theoretic
properties for veriﬁcation problems (see the many references to the work on analysis,
transformation, and veriﬁcation of CLP programs surveyed in this paper). Continued
progress depends on research in several areas.


Transformation of verification problems to CHCs. The translation of a veriﬁcation prob-
lem from a source language into CHCs needs to be scalable to large problems in main-
stream languages, and veriﬁable with respect to the language semantics. Most existing
approaches are lacking in scalability or rigour. One area for research is to exploit ex-
isting logical frameworks and semantic speciﬁcation languages, such as the rewriting-
based K Framework (Rosu and Serbanuta 2010) or constructive logic proof assistants
(Barras et al. 1997, Nipkow et al. 2002), which have previously been used to specify a
variety of languages. An interpretive approach based on semantic rules expressed as
CHCs, combined with CHC specialisation, as discussed in Section 4, is one possible
strategy. Another strategy is compiler-based translation, in which a validated compiler
is applied, leaving a ‘simpler’ intermediate language to translate into CHCs. Eﬀective
and scalable translations to and from SMT-LIB representations to CHCs can also play
an important role in interfacing with existing translation tools and solvers. Translators
from program veriﬁers based on pre/post-condition speciﬁcations (Barnett et al. 2006,
Filliâtre and Paskevich 2013, Hamza et al. 2019, Leino 2013) could also be useful for
generating veriﬁcation conditions in CHC format that can be handled by CHC-based
tools. In addition, research is needed on formalising and translating other languages and
systems to which CHC veriﬁcation has not previously been applied, in particular popu-
lar languages which are not strongly typed (e.g., Javascript, Python), machine learning
systems, and heterogeneous distributed systems.


Advances in CHC solvers. As with veriﬁcation tools in general, CHC solvers face the
challenges of automation and scalability. As regards automation, some techniques, such
as abstract interpretation (see Section 5), are indeed automatic. Moreover, various prac-
tical tools are based on algorithmic strategies for applying the techniques discussed in
this paper and for making the so-called eureka steps (see Section 3.1). Some such strate-
gies were presented through examples in Section 6. Scalability is addressed in two ways:
ﬁrstly, large problems are tackled, whenever possible, by divide-and-conquer approaches,
including, for example, modularity and incrementality (within abstract interpretation,
we refer to the paper by García-Contreras et al. (2020b) and the references therein);
and, secondly, abstract interpretation (as mentioned in Section 5) oﬀers the possibil-
ity of trading oﬀ scalability for precision, less precise analyses being, in general, more
scalable; hence strategies for choosing and reﬁning abstractions are crucial. An annual
Analysis and Transformation of Constrained Horn Clauses for Program Verification 57

competition for CHC solvers (https://chc-comp.github.io/) motivates progress and
provides evidence of the increasing eﬀectiveness of the solvers.
   As impressive as recent progress is, much research is still needed on the scalabil-
ity and expressiveness of CHC solvers. On the one hand, as shown in this survey,
most existing techniques are for numerical constraint domains, with extensions for ar-
rays, and ADTs for standard data structures such as lists and trees. On the other,
new domains are being developed to handle strings, heaps, bit-vectors, ﬂoating point
numbers and other such typical constructs that arise in program veriﬁcation applica-
tions (see, for instance, (Brain et al. 2014, Brummayer and Biere 2009, Liang et al. 2016,
Madhusudan et al. 2011)). Furthermore, progress in solving numerical constraint prob-
lems requires techniques for eﬀective handling of non-linear constraints, both through
decision procedures for selected theories (Jovanovic and de Moura 2012), and abstract
domains for safe approximation of non-linear problems (Jeannet and Miné 2009). Apart
from constraint domains themselves, research and experimentation is needed on ver-
iﬁcation strategies combining analysis and transformation with reﬁned techniques for
generalisation and counterexample-based reﬁnement. Novel veriﬁcation strategies such
as Newtonian iteration (Esparza et al. 2010) are also being investigated from the per-
spective of CHC veriﬁcation (Kaﬂe et al. 2018).


Applications. Advances in general CHC solving techniques, as just discussed, will en-
able existing application areas to be addressed more eﬀectively and at larger scale. By
contrast, some applications require conceptual advances to ﬁnd eﬀective ways to ex-
press them as CHC veriﬁcation problems. One such area is the automatic veriﬁcation
of properties of concurrent systems, which has been the subject of intensive research for
many years. Approaches that simultaneously exploit the power of CHC solvers and tech-
niques developed for model checking, such as partial order reduction (Clarke et al. 2003,
Flanagan and Godefroid 2005), are needed. The approach described by Grebenshchikov et al.
(2012), in which proof rules for concurrency properties (such as Owicki-Gries rules and
rely-guarantee rules) are encoded as CHCs, provides a promising direction for future
research. Veriﬁcation of co-inductive program properties, arising in concurrency, type
theory and elsewhere, can exploit the greatest ﬁxpoint semantics of CHCs. The litera-
ture contains initial work in this area (Basold et al. 2019, Gupta et al. 2007, Seki 2012).
   A new challenging ﬁeld of application for CHC-based techniques is the veriﬁcation of
security properties of computations executing in cryptographic currency systems on top
of the highly decentralised and distributed blockchain structure. Indeed, the usefulness
of CHCs for specifying the formal semantics and for the static analysis of smart con-
tracts has been advocated by recent papers (Grishchenko et al. 2018, Kalra et al. 2018,
Tsankov et al. 2018, Schneidewind et al. 2020, Pérez-Carrasco et al. 2020).
   Probabilistic program veriﬁcation problems arise either from probabilistic programs,
which include random choices, or from deterministic programs where a probability dis-
tribution is provided for inputs, and the problem is to verify the probability of reaching
a speciﬁed state. This is becoming an active research topic, with applications in ma-
chine learning and real-time systems among others. CHCs can be given probabilistic
interpretations (Sato and Kameya 1997, Kimmig et al. 2011) which can provide the ba-
sis for probabilistic reasoning. Recent work on probabilistic Horn clause veriﬁcation is
58 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

described by Albarghouthi (2017); probabilistic abstract interpretations have also been
considered (Monniaux 2000, Kirkeby 2019).
  Automatic analysis of the resource consumption of programs is also a very important
and active area, where CHC-based techniques play a very relevant role. Of particular
interest are static (or combined static and dynamic) analyses for bounding the energy con-
sumption of programs (Navas et al. 2008, 2009, Liqat et al. 2014, 2016, López-García et al.
2015, 2018) This application area is of increasing importance as, on one hand, the global
energy consumption of software systems grows rapidly, and on the other hand, wearable,
implantable, and portable systems need to minimize energy consumption in order to
maximize battery life.


                                  Acknowledgments
We would like to thank Isabel García-Contreras, Bishoksan Kaﬂe, and José Francisco
Morales for discussions. We are also grateful to the Editor-in-Chief Mirosław Truszczyński
and the anonymous reviewers for their comments and suggestions, all of which have
contributed to improving our manuscript.
  Emanuele De Angelis, Fabio Fioravanti, Alberto Pettorossi, and Maurizio Proietti are
members of the INdAM Research Group GNCS.

Competing interests: The authors declare none.


                                      References
Albarghouthi, A. 2017. Probabilistic Horn clause veriﬁcation. In SAS ’17. LNCS
 10422. Springer, 1–22.
Albert, E., Arenas, P., Genaim, S., and Puebla, G. 2011. Closed-form upper
 bounds in static cost analysis. J. Autom. Reason. 46, 2, 161–203.
Albert, E., Arenas, P., Genaim, S., Puebla, G., and Zanardini, D. 2007. Cost
 analysis of Java bytecode. In ESOP ’07. LNCS 4421. Springer, 157–172.
Albert, E., Arenas, P., Genaim, S., Puebla, G., and Zanardini, D. 2008. Re-
 moving useless variables in cost analysis of Java bytecode. In ACM SAC - Software
 Verification Track (SV08 ). ACM Press, 368–375.
Albert, E., Arenas, P., and Gómez-Zamalloa, M. 2018. Systematic testing of
 actor systems. Softw. Test. Verification Reliab. 28, 3, e1661.
Albert, E., Gómez-Zamalloa, M., and Puebla, G. 2010. PET: A partial evaluation-
 based test case generation tool for Java bytecode. In PEPM ’10. ACM Press, 25–28.
Alberti, F., Ghilardi, S., and Sharygina, N. 2015. Decision procedures for ﬂat
 array properties. J. Autom. Reasoning 54, 4, 327–352.
Amaral, C., Florido, M., and Costa, V. S. 2014. PrologCheck - Property-based
 testing in Prolog. In 12th FLOPS ’14. LNCS 8475. Springer, 1–17.
Apt, K. R. 1990. Introduction to logic programming. In Handbook of Theoretical
 Computer Science, J. van Leeuwen, Ed. Elsevier, 493–576.
Apt, K. R. and Bol, R. N. 1994. Logic programming and negation: A survey. J. Log.
 Program. 19, 20, 9–71.
Analysis and Transformation of Constrained Horn Clauses for Program Verification 59

Bagnara, R., Hill, P. M., and Zaffanella, E. 2008. The Parma Polyhedra Library:
  Toward a complete set of numerical abstractions for the analysis and veriﬁcation of
  hardware and software systems. Science of Computer Programming 72, 1-2, 3–21.
Bancilhon, F., Maier, D., Sagiv, Y., and Ullman, J. 1986. Magic sets and other
  strange ways to implement logic programs (Extended abstract). In 5th ACM SIGMOD-
  SIGACT Symp. on Principles of Database Systems, 1985. ACM Press, 1–15.
Banda, G. and Gallagher, J. P. 2009. Analysis of linear hybrid systems in CLP. In
  LOPSTR ’08. LNCS 5438. Springer, 55–70.
Barbuti, R. and Giacobazzi, R. 1992. A bottom-up polymorphic type inference in
  logic programming. Science of Computer Programming 19, 281–313.
Barnett, M., Chang, B.-Y. E., De Line, R., Jacobs, B., and Leino, K. R. M.
  2006. Boogie: A modular reusable veriﬁer for object-oriented programs. In Formal
  Methods for Components and Objects. LNCS 4111. Springer, 364–387.
Barras, B., Boutin, S., Cornes, C., Courant, J., Filliâtre, J.-C., Gimenez,
  E., Herbelin, H., Huet, G., Munoz, C., Murthy, C., Parent, C., Paulin-
  Mohring, C., Saibi, A., and Werner, B. 1997. The Coq Proof Assistant Reference
  Manual: Version 6.1. Tech. Rep. RT-0203. https://hal.inria.fr/inria-00069968.
Barrett, C., Conway, C. L., Deters, M., Hadarean, L., Jovanovic, D., King,
  T., Reynolds, A., and Tinelli, C. 2011. CVC4. In CAV ’11. LNCS 6806. Springer,
  171–177.
Barrett, C., Fontaine, P., and Tinelli, C. 2016. The Satisﬁability Modulo Theories
  Library (SMT-LIB). www.SMT-LIB.org.
Barrett, C. W. and Tinelli, C. 2018. Satisﬁability modulo theories. In Handbook
  of Model Checking, E. M. Clarke and al., Eds. Springer, 305–343.
Barthe, G., Crespo, J. M., and Kunz, C. 2011. Relational veriﬁcation using product
  programs. In FM ’11. LNCS 6664. Springer, 200–214.
Basold, H., Komendantskaya, E., and Li, Y. 2019. Coinduction in Uniform: Foun-
  dations for corecursive proof search with Horn clauses. In ESOP ’19. LNCS 11423.
  Springer, 783–813.
Benoy, F. and King, A. 1997. Inferring argument size relationships with CLP(R). In
  LOPSTR ’96. LNCS 1207. Springer, 204–223.
Benton, N. 2004. Simple relational correctness proofs for static analyses and program
  transformations. In POPL ’04. ACM Press, 14–25.
Beyene, T. A., Popeea, C., and Rybalchenko, A. 2013. Solving existentially quan-
  tiﬁed horn clauses. In CAV ’13. LNCS 8044. Springer, 869–882.
Bjørner, N., Gurfinkel, A., McMillan, K. L., and Rybalchenko, A. 2015. Horn
  clause solvers for program veriﬁcation. In Fields of Logic and Computation II – Essays
  dedicated to Yuri Gurevich. LNCS 9300. Springer, 24–51.
Blanchet, B. 2016. Modeling and verifying security protocols with the applied pi
  calculus and ProVerif. Found. Trends Priv. Secur. 1, 1-2, 1–135.
Blazy, S. and Leroy, X. 2009. Mechanized semantics for the Clight subset of the
  C language. J. Autom. Reasoning 43, 3, 263–288.
Borralleras, C., Lucas, S., Oliveras, A., Rodríguez-Carbonell, E., and Ru-
  bio, A. 2012. SAT modulo linear arithmetic for solving polynomial constraints. J.
  Autom. Reasoning 48, 1, 107–131.
Bradley, A. R. 2011. SAT-based model checking without unrolling. In VMCAI ’11.
  LNCS 6538. Springer, 70–87.
60 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

Bradley, A. R. and Manna, Z. 2007. The Calculus of Computation. Springer.
Brain, M., D’Silva, V., Griggio, A., Haller, L., and Kroening, D. 2014. Deciding
  ﬂoating-point logic with abstract conﬂict driven clause learning. Formal Methods in
  System Design 45, 2, 213–245.
Brough, D. R. and Hogger, C. J. 1991. Grammar-related transformations of logic
  programs. New Generation Computing 9, 1, 115–134.
Brummayer, R. and Biere, A. 2009. Boolector: An eﬃcient SMT solver for bit-vectors
  and arrays. In TACAS ’09. LNCS 5505. Springer, 174–177.
Bueno, F., Deransart, P., Drabent, W., Ferrand, G., Hermenegildo, M.,
  Maluszynski, J., and Puebla, G. 1997. On the role of semantic approximations in
  validation and diagnosis of constraint logic programs. In 3rd Workshop on Automated
  Debugging – AADEBUG ’97. Univ. of Linköping Press, Linköping, Sweden, 155–170.
Bulyonkov, M. A. 1984. Polyvariant mixed computation for analyzer programs. Acta
  Informatica 21, 473–484.
Bundy, A. 2001. The automation of proof by mathematical induction. In Handbook of
  Automated Reasoning (I), A. Robinson and A. Voronkov, Eds. North Holland, 845–911.
Burn, T. C., Ong, C. L., and Ramsay, S. J. 2018. Higher-order constrained Horn
  clauses for veriﬁcation. ACM Program. Lang. 2, POPL ’18, 11:1–11:28.
Burstall, R. M. and Darlington, J. 1977. A transformation system for developing
  recursive programs. J. ACM 24, 1, 44–67.
Casso, I., Morales, J. F., López-García, P., and Hermenegildo, M. 2019. An
  integrated approach to assertion-based random testing in Prolog. In LOPSTR ’19.
  LNCS 12042. Springer, 159–176.
Champion, A., Chiba, T., Kobayashi, N., and Sato, R. 2020. ICE-based reﬁnement
  type discovery for higher-order functional programs. J. Autom. Reason.64,7,1393–1418.
Chen, J., Wei, J., Feng, Y., Bastani, O., and Dillig, I. 2019. Relational veriﬁcation
  using reinforcement learning. ACM Program. Lang. 3, OOPSLA, 141:1–141:30.
Churchill, B. R., Padon, O., Sharma, R., and Aiken, A. 2019. Semantic program
  alignment for equivalence checking. In PLDI ’19. ACM Press, 1027–1040.
Çiçek, E., Barthe, G., Gaboardi, M., Garg, D., and Hoffmann, J. 2017. Rela-
  tional cost analysis. In POPL ’17. ACM Press, 316–329.
Cimatti, A., Griggio, A., Schaafsma, B., and Sebastiani, R. 2013. The MathSAT5
  SMT Solver. In TACAS ’13. LNCS 7795. Springer, 93–107.
Claessen, K. and Hughes, J. 2000. QuickCheck: A lightweight tool for random testing
  of Haskell programs. In ICFP ’00. ACM Press, 268–279.
Clark, K. L. 1978. Negation as failure. In Logic and Data Bases, H. Gallaire and
  J. Minker, Eds. Plenum Press, New York, 293–322.
Clarke, E., Grumberg, O., Jha, S., Lu, Y., and Veith, H. 2003. Counterexample-
  guided abstraction reﬁnement for symbolic model checking. J. ACM 50, 5, 752–794.
Clarke, E. M., Grumberg, O., and Peled, D. 1999. Model Checking. MIT Press.
Codish, M., Bruynooghe, M., García de la Banda, M., and Hermenegildo,
  M. 1997. Exploiting goal independence in the analysis of logic programs. J. Log.
  Program. 32, 3, 247–261.
Codish, M., Dams, D., and Yardeni, E. 1994. Bottom-up abstract interpretation of
  logic programs. Journal of Theoretical Computer Science 124, 93–125.
Codish, M. and Demoen, B. 1995. Analyzing logic programs using "PROP"-ositional
  logic programs and a magic wand. J. Log. Program. 25, 3, 249–274.
Analysis and Transformation of Constrained Horn Clauses for Program Verification 61

Colmerauer, A. 1982. Prolog and inﬁnite trees. In Logic Programming, K. L. Clark
 and S.-Å. Tärnlund, Eds. Academic Press, 231–251.
Coppit, D., Le, W., Sullivan, K. J., Khurshid, S., and Yang, J. 2005. Software
 assurance by bounded exhaustive testing. IEEE Trans. Softw. Eng. 31, 4, 328–339.
Corsini, M.-M., Musumbu, K., Rauzy, A., and Le Charlier, B. 1994. Eﬃcient
 bottom-up abstract interpretation of Prolog by means of constraint solving over sym-
 bolic ﬁnite domains. In PLILP ’93. LNCS 714. Springer, 75–91.
Cousot, P. and Cousot, R. 1977. Abstract interpretation: A uniﬁed lattice model for
 static analysis of programs by construction of approximation of ﬁxpoints. In POPL ’77.
 ACM Press, 238–252.
Cousot, P. and Cousot, R. 1992. Comparing the Galois connection and widening/
 narrowing approaches to abstract interpretation. In PLILP ’92. LNCS 631. Springer,
 269–295.
Cousot, P. and Halbwachs, N. 1978. Automatic discovery of linear restraints among
 variables of a program. In POPL ’78. ACM Press, 84–96.
Craig, S.-J. and Leuschel, M. 2003. A compiler generator for constraint logic pro-
 grams. In PSI ’03. LNCS 2890. Springer, 148–161.
Craig, W. 1957. Three uses of the Herbrand-Gentzen theorem in relating model theory
 and proof theory. The Journal of Symbolic Logic 22, 3, 269–285.
Cui, B. and Warren, D. S. 2000. A system for tabled constraint logic programming.
 In Computational Logic ’00. LNCS 1861. Springer, 478–492.
De Angelis, E., Fioravanti, F., Meo, M. C., Pettorossi, A., and Proietti, M.
 2019. Semantics and controllability of time-aware business processes. Fundamenta
 Informaticae 165, 205–244.
De Angelis, E., Fioravanti, F., Palacios, A., Pettorossi, A., and Proietti, M.
 2019. Property-based test case generators for free. In Tests and Proofs - TAP@FM ’19.
 LNCS 11823. Springer, 186–206.
De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2014a. Program
 veriﬁcation via iterated specialization. Sci. Comput. Program. 95, Part 2, 149–175.
De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2014b. Veri-
 MAP: A tool for verifying programs through transformations. In TACAS ’14. LNCS
 8413. Springer, 568–574.
De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2015.
 Semantics-based generation of veriﬁcation conditions by program specialization. In
 PPDP ’15. ACM Press, 91–102.
De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2016. Re-
 lational veriﬁcation through Horn clause transformation. In SAS ’16. LNCS 9837.
 Springer, 147–169.
De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2017a. Predi-
 cate pairing with abstraction for relational veriﬁcation. In LOPSTR ’17. LNCS 10855.
 Springer, 289–305.
De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2017b.
 Semantics-based generation of veriﬁcation conditions via program specialization. Sci.
 Comput. Programm. 147, 78–108.
De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2018a. Predi-
 cate Pairing for program veriﬁcation. Theor. Pract. Logic Program. 18, 2, 126–166.
62 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2018b. Solv-
  ing Horn clauses on inductive data types without induction. Theor. Pract. Logic Pro-
  gram. 18, 3-4, 452–469.
De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2020. Removing
  algebraic data types from constrained Horn clauses using diﬀerence predicates. In
  IJCAR ’20. Lecture Notes in Artiﬁcial Intelligence 12166. Springer, 83–102.
de Moura, L. M. and Bjørner, N. 2008. Z3: An eﬃcient SMT solver. In TACAS ’08.
  LNCS 4963. Springer, 337–340.
De Schreye, D., Glück, R., Jørgensen, J., Leuschel, M., Martens, B., and
  Sørensen, M. H. 1999. Conjunctive partial deduction: Foundations, control, algo-
  rithms, and experiments. J. Log. Program. 41, 2–3, 231–277.
Debray, S. and Ramakrishnan, R. 1994. Abstract interpretation of logic programs
  using magic transformations. J. Log. Program. 18, 149–176.
Debray, S. K. and Lin, N. W. 1993. Cost analysis of logic programs. ACM Transac-
  tions on Programming Languages and Systems 15, 5, 826–875.
Debray, S. K., Lin, N.-W., and Hermenegildo, M. 1990. Task granularity analysis
  in logic programs. In ACM PLDI ’90. ACM Press, 174–188.
Debray, S. K., López-García, P., Hermenegildo, M., and Lin, N.-W. 1997. Lower
  bound cost estimation for logic programs. In Intl. Logic Program. Symp. ’97. MIT Press,
  291–305.
Delzanno, G. and Podelski, A. 1999. Model checking in CLP. In TACAS ’99. LNCS
  1579. Springer, 223–239.
Delzanno, G. and Podelski, A. 2001. Constraint-based deductive model checking.
  Intl. Journal on Software Tools for Technology Transfer 3, 3, 250–270.
Demyanova, Y., Rümmer, P., and Zuleger, F. 2017. Systematic predicate abstrac-
  tion using variable roles. In NASA Formal Methods. Springer Intl. Publishing, 265–281.
Doménech, J. J., Gallagher, J. P., and Genaim, S. 2019. Control-ﬂow reﬁnement
  by partial evaluation, and its application to termination and cost analysis. Theor.
  Pract. Logic Program. 19, 5-6, 990–1005.
Donzeau-Gouge, V., Huet, G., Kahn, G., and Lang, B. 1984. Programming en-
  vironments based on structured editors: The MENTOR experience. In Interactive
  Programming Environments. McGraw-Hill, 128–140.
Dutertre, B. 2014. Yices 2.2. In CAV ’14. LNCS 8559. Springer, 737–744.
Een, N., Mishchenko, A., and Brayton, R. 2011. Eﬃcient implementation of prop-
  erty directed reachability. In Formal Methods in Comput. Aided Des. FMCAD, 125–134.
Enderton, H. 1972. A Mathematical Introduction to Logic. Academic Press, New York.
Esparza, J., Kiefer, S., and Luttenberger, M. 2010. Newtonian program analysis.
  J. ACM 57, 6, 33.
Etalle, S. and Gabbrielli, M. 1996. Transformations of CLP modules. Theoretical
  Computer Science 166, 101–146.
Fedyukovich, G., Zhang, Y., and Gupta, A. 2018. Syntax-guided termination anal-
  ysis. In CAV ’18, Part I. LNCS 10981. Springer, 124–143.
Felsing, D., Grebing, S., Klebanov, V., Rümmer, P., and Ulbrich, M. 2014.
  Automating regression veriﬁcation. In ASE ’14. ACM Press, 349–360.
Filliâtre, J. C. and Paskevich, A. 2013. Why3 — Where programs meet provers.
  In ESOP ’13. LNCS 7792. Springer, 125–128.
Analysis and Transformation of Constrained Horn Clauses for Program Verification 63

Fioravanti, F., Pettorossi, A., Proietti, M., and Senni, V. 2013. Controlling poly-
  variance for specialization-based veriﬁcation.Fundamenta Informaticae 124, 4, 483–502.
Fioravanti, F., Pettorossi, A., and Proietti, M. 2001a. Automated strategies for
  specializing constraint logic programs. In LOPSTR ’00. LNCS 2042. Springer, 125–146.
Fioravanti, F., Pettorossi, A., and Proietti, M. 2001b. Verifying CTL properties
  of inﬁnite state systems by specializing constraint logic programs. In ACM Workshop
  VCL ’01. Technical Report DSSE-TR-2001-3. University of Southampton, UK, 85–96.
Fioravanti, F., Pettorossi, A., and Proietti, M. 2004. Transformation rules for
  locally stratiﬁed constraint logic programs. In Program Development in Computational
  Logic. LNCS 3049. Springer, 292–340.
Fioravanti, F., Pettorossi, A., Proietti, M., and Senni, V. 2012. Improving
  reachability analysis of inﬁnite state systems by specialization. Fundamenta Informa-
  ticae 119, 3-4, 281–300.
Fioravanti, F., Pettorossi, A., Proietti, M., and Senni, V. 2013a. General-
  ization strategies for the veriﬁcation of inﬁnite state systems. Theor. Pract. Log.
  Program. 13, 2, 175–199.
Fioravanti, F., Pettorossi, A., Proietti, M., and Senni, V. 2013b. Proving
  theorems by program transformation. Fundamenta Informaticae 127, 1-4, 115–134.
Fioravanti, F., Proietti, M., and Senni, V. 2015. Eﬃcient generation of test data
  structures using constraint logic programming and program transformation. Journal
  of Logic and Computation 25, 6, 1263–1283.
Flanagan, C. and Godefroid, P. 2005. Dynamic partial-order reduction for model
  checking software. In POPL ’05. ACM Press, 110–121.
Fribourg, L. and Olsén, H. 1997. A decompositional approach for computing least
  ﬁxed-points of Datalog programs with Z-counters. Constraints 2, 3/4, 305–335.
Frühwirth, T. 1998. Theory and practice of constraint handling rules. J. Log. Pro-
  gram. 37, 1, 95–138.
Futamura, Y. 1971. Partial evaluation of computation process - an approach to a
  compiler-compiler. Systems, Computers, Controls 2(5), 45–50.
Gallagher, J. P. 1993. Tutorial on specialisation of logic programs. In PEPM ’93.
  ACM Press, 88–98.
Gallagher, J. P., Boulanger, D., and Sağlam, H. 1995. Practical model-based
  static analysis for deﬁnite logic programs. In Intl. Logic Program. Symp. MIT Press,
  351–365.
Gallagher, J. P. and de Waal, D. A. 1994. Fast and precise regular approximation
  of logic programs. In 11th Intl. Conference on Logic Programming. MIT Press, 599–613.
Gallagher, J. P., Hermenegildo, M., Kafle, B., Klemen, M., López-García,
  P., and Morales, J. F. 2020. From big-step to small-step semantics and back with
  interpreter specialization. In VPT ’20. Elect. Proc. Theor. Comput. Sci. 320 , 50–64.
Gange, G., Navas, J., Schachte, P., Søndergaard, H., and Stuckey, P. 2013.
  Failure tabled constraint logic programming by interpolation. Theor. Pract. Log. Pro-
  gram. 13, 4-5, 593–607.
Gange, G., Navas, J. A., Schachte, P., Søndergaard, H., and Stuckey, P. J.
  2015. Horn clauses as an intermediate representation for program analysis and trans-
  formation. Theor. Pract. Log. Program. 15, 4-5, 526–542.
64 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

García-Contreras, I., Morales, J. F., and Hermenegildo, M. 2020a. Incremental
 analysis of logic programs with assertions and open predicates. In LOPSTR ’19. LNCS
 12042. Springer, 36–56.
García-Contreras, I., Morales, J. F., and Hermenegildo, M. 2020b. Incremen-
 tal and modular context-sensitive analysis. Theor. Pract. Logic Program. (to appear).
García de la Banda, M. and Hermenegildo, M. 1993. A practical approach to the
 global analysis of constraint logic programs. InLogicProgram.Symp.MIT Press,437–455.
García de la Banda, M., Hermenegildo, M., Bruynooghe, M., Dumortier, V.,
 Janssens, G., and Simoens, W. 1996. Global analysis of constraint logic programs.
 ACM Transactions on Programming Languages and Systems 18, 5, 564–615.
Giannotti, F. and Hermenegildo, M. 1991. A technique for recursive invariance
 detection and selective program specialization. In PLILP ’91. LNCS 528. Springer,
 323–335.
Godefroid, P., Klarlund, N., and Sen, K. 2005. DART: Directed automated ran-
 dom testing. In PLDI ’05. ACM Press, 213–223.
Godlin, B. and Strichman, O. 2008. Inference rules for proving the equivalence of
 recursive procedures. Acta Informatica 45, 6, 403–439.
Goguen, J. A. and Meseguer, J. 1982. Security policies and security models. In 1982
 IEEE Symposium on Security and Privacy. 11–20.
Gómez-Zamalloa, M., Albert, E., and Puebla, G. 2009. Decompilation of Java
 bytecode to Prolog by partial evaluation. Inf. Softw. Technol. 51, 10, 1409–1427.
Gómez-Zamalloa, M., Albert, E., and Puebla, G. 2010. Test case generation for
 object-oriented imperative languages in CLP. Theor. Pract. Logic Program. 10, 4–6,
 659–674.
Gotlieb, A., Botella, B., and Rueher, M. 1998. Automatic test data generation
 using constraint solving techniques. In ACM Software Testing and Analysis Symp.
 ACM Press, 53–62.
Graf, S. and Saïdi, H. 1997. Construction of abstract state graphs with PVS. In
 CAV ’97. LNCS 1254. Springer, 72–83.
Grebenshchikov, S., Lopes, N. P., Popeea, C., and Rybalchenko, A. 2012. Syn-
 thesizing software veriﬁers from proof rules. In PLDI ’12. ACM Press, 405–416.
Grishchenko, I., Maffei, M., and Schneidewind, C. 2018. Foundations and tools
 for the static analysis of Ethereum smart contracts. In CAV ’18, Part I. LNCS 10981.
 Springer, 51–78.
Gulwani, S., Jain, S., and Koskinen, E. 2009. Control-ﬂow reﬁnement and progress
 invariants for bound analysis. In PLDI ’09. ACM Press, 375–385.
Gupta, G., Bansal, A., Min, R., Simon, L., and Mallya, A. 2007. Coinductive
 logic programming and its applications. In ICLP ’07. LNCS 4670. Springer, 27–44.
Gurfinkel, A., Kahsai, T., Komuravelli, A., and Navas, J. A. 2015. The SeaHorn
 veriﬁcation framework. In CAV ’15. LNCS 9206. Springer, 343–361.
Hamza, J., Voirol, N., and Kunčak, V. 2019. System FR: Formalized foundations
 for the Stainless veriﬁer. ACM Programming Languages 3, OOPSLA, 166:1–166:30.
Heizmann, M., Hoenicke, J., and Podelski, A. 2009. Reﬁnement of trace abstrac-
 tion. In SAS ’09. LNCS 5673. Springer, 69–85.
Henriksen, K. S. and Gallagher, J. P. 2006. Abstract interpretation of PIC pro-
 grams through logic programming. In SCAM ’06. IEEE Computer Society, 184–196.
Analysis and Transformation of Constrained Horn Clauses for Program Verification 65

Hermenegildo, M., Bueno, F., Carro, M., López-García, P., Mera, E.,
  Morales, J. F., and Puebla, G. 2012. An overview of Ciao and its design phi-
  losophy. Theor. Pract. Logic Program. 12, 1–2, 219–252.
Hermenegildo, M., Puebla, G., and Bueno, F. 1999. Using global analysis, partial
  speciﬁcations, and an extensible assertion language for program validation and debug-
  ging. In The Logic Programming Paradigm: A 25-Year Perspective. Springer, 161–192.
Hermenegildo, M., Puebla, G., Bueno, F., and López-García, P. 2005. Inte-
  grated program debugging, veriﬁcation, and optimization using abstract interpretation
  (and the Ciao system preprocessor). Sci. Comput. Program. 58, 1–2, 115–140.
Hermenegildo, M., Puebla, G., Marriott, K., and Stuckey, P. 2000. Incremen-
  tal analysis of constraint logic programs. ACM TOPLAS 22, 2, 187–223.
Hermenegildo, M., Warren, R., and Debray, S. K. 1992. Global ﬂow analysis as
  a practical compilation tool. J. Log. Program. 13, 4, 349–367.
Hoare, C. A. R. 1969. An axiomatic basis for computer programming. Comm. of the
  ACM 12, 10, 576–580, 583.
Hoder, K. and Bjørner, N. 2012. Generalized property directed reachability. In
  SAT ’12. LNCS 7317. Springer, 157–171.
Hojjat, H. and Rümmer, P. 2018. The ELDARICA Horn solver. In Formal Methods
  in Computer Aided Design ’18. IEEE, 1–7.
Jacobs, D., Langen, A., and Winsborough, W. 1990. Multiple specialization of logic
  programs with run-time tests. In Intl. Conf. on Logic Program. MIT Press, 718–731.
Jaffar, J. 1984. Eﬃcient uniﬁcation over inﬁnite terms. NewGener.Comput.2,3,207–219.
Jaffar, J. and Lassez, J.-L. 1987. Constraint logic programming. In POPL ’87. ACM
  Press, 111–119.
Jaffar, J. and Maher, M. 1994. Constraint logic programming: A survey. J. Log.
  Program. 19/20, 503–581.
Jaffar, J., Maher, M., Marriott, K., and Stuckey, P. 1998. The semantics of
  constraint logic programs. J. Log. Program. 37, 1–46.
Jaffar, J., Michaylov, S., Stuckey, P. J., and Yap, R. H. C. 1992. The CLP(R)
  language and system. ACM Trans. Program. Lang. Syst. 14, 3, 339–395.
Jaffar, J., Murali, V., Navas, J. A., and Santosa, A. E. 2012. TRACER: A
  symbolic execution tool for veriﬁcation. In CAV ’12. LNCS 7358. Springer, 758–766.
Jaffar, J., Santosa, A., and Voicu, R. 2009. An interpolation method for CLP
  traversal. In CP ’09. LNCS 5732. Springer, 454–469.
Jaffar, J., Santosa, A. E., and Voicu, R. 2004. A CLP proof method for timed
  automata. In IEEE Real-Time Systems Symp. IEEE Computer Society, 175–186.
Jeannet, B. and Miné, A. 2009. Apron: A library of numerical abstract domains for
  static analysis. In CAV ’09. LNCS 5643. Springer, 661–667.
Jhala, R. and Majumdar, R. 2009. Software model checking. ACM Computing
  Surveys 41, 4, 21:1–21:54.
Jones, N. D., Gomard, C. K., and Sestoft, P. 1993. Partial Evaluation and Auto-
  matic Program Generation. Prentice Hall.
Jovanovic, D. and de Moura, L. 2012. Solving non-linear arithmetic. In IJCAR ’12.
  LNCS 7364. Springer, 339–354.
Kafle, B. and Gallagher, J. P. 2017a. Constraint specialisation in Horn clause
  veriﬁcation. Sci. Comput. Program. 137, 125–140.
66 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

Kafle, B. and Gallagher, J. P. 2017b. Horn clause veriﬁcation with convex polyhe-
  dral abstraction and tree automata-based reﬁnement. Comput. Lang. Syst. Struct. 47,
  2–18.
Kafle, B., Gallagher, J. P., Gange, G., Schachte, P., Søndergaard, H., and
  Stuckey, P. J. 2018. An iterative approach to precondition inference using con-
  strained Horn clauses. Theor. Pract. Logic Program. 18, 3-4, 553–570.
Kafle, B., Gallagher, J. P., and Ganty, P. 2018. Tree dimension in veriﬁcation
  of constrained Horn clauses. Theor. Pract. Logic Program. 18, 2, 224–251.
Kafle, B., Gallagher, J. P., and Morales, J. F. 2016. RAHFT: A tool for verifying
  Horn clauses using abstract interpretation and ﬁnite tree automata. In CAV ’16, Part I.
  LNCS 9779. Springer, 261–268.
Kahn, G. 1987. Natural semantics. LNCS 247. Springer, 22–39.
Kahsai, T., Rümmer, P., Sanchez, H., and Schäf, M. 2016. JayHorn: A framework
  for verifying Java programs. In CAV ’16, Part I. LNCS 9779. Springer, 352–358.
Kalra, S., Goel, S., Dhawan, M., and Sharma, S. 2018. Zeus: Analyzing safety of
  smart contracts. In 25th Network and Distributed System Security Symp. The Internet
  Society, 1–15.
Kanamori, T. 1993. Abstract interpretation based on Alexander templates. J. Log.
  Program. 15, 1&2, 31–54.
Kelly, A., Marriott, K., Søndergaard, H., and Stuckey, P. 1998. A practical
  object-oriented analysis engine for CLP.Software: Practice and Experience28,2,188–224.
Khedker, U. P. and Karkare, B. 2008. Eﬃciency, precision, simplicity, and generality
  in interprocedural data ﬂow analysis: Resurrecting the classical call strings method.
  In CC ’08. LNCS 4959. Springer, 213–228.
Kimmig, A., Demoen, B., Raedt, L. D., Costa, V. S., and Rocha, R. 2011. On
  the implementation of the probabilistic logic programming language ProbLog. Theor.
  Pract. Logic Program. 11, 2-3, 235–262.
Kirkeby, M. H. 2019. Probabilistic output analyses for deterministic programs - reusing
  existing non-probabilistic analyses. Elect. Proc. Theor. Comput. Sci. 312 , 43–57.
Klemen, M., Stulova, N., López-García, P., Morales, J. F., and
  Hermenegildo, M. 2018. Static performance guarantees for programs with run-time
  checks. In PPDP ’18. ACM Press, 1–13.
Komuravelli, A., Gurfinkel, A., and Chaki, S. 2016. SMT-based model checking
  for recursive programs. Formal Methods Syst. Des. 48, 3, 175–205.
Komuravelli, A., Gurfinkel, A., Chaki, S., and Clarke, E. M. 2013. Automatic
  abstraction in SMT-based unbounded software model checking. In CAV ’13. LNCS
  8044. Springer, 846–862.
Kowalski, R. and Kuehner, D. 1971. Linear resolution with selection function. Ar-
  tificial Intelligence 2, 227–260.
Lahiri, S. K., McMillan, K. L., Sharma, R., and Hawblitzel, C. 2013. Diﬀerential
  assertion checking. In ESEC/FSE ’13. ACM Press, 345–355.
Le Charlier, B. and Van Hentenryck, P. 1994. Experimental evaluation of a
  generic abstract interpretation algorithm for Prolog. ACM TOPLAS 16, 1, 35–101.
Leavens, G. T., Baker, A. L., and Ruby, C. 2006. Preliminary design of JML: A
  behavioral interface speciﬁcation language for Java. Softw. Eng. Notes 31, 3, 1–38.
Leino, K. R. M. 2013. Developing veriﬁed programs with Dafny. In Intl. Conf. on
  Software Engineering ’13. IEEE Press, 1488–1490.
Analysis and Transformation of Constrained Horn Clauses for Program Verification 67

Leroy, X., Doligez, D., Frisch, A., Garrigue, J., Rémy, D., and Vouillon, J.
  2017. The OCaml system, Release 4.06. Documentation and user’s manual, Institut
  National de Recherche en Informatique et en Automatique, France.
Leuschel, M. and Bruynooghe, M. 2002. Logic program specialisation through
  partial deduction: Control issues. Theor. Pract. Log. Program. 2, 4&5, 461–515.
Leuschel, M. and De Schreye, D. 1998. Constrained partial deduction and the
  preservation of characteristic trees. New Gener. Comput. 16, 3, 283–342.
Leuschel, M., Elphick, D., Varea, M., Craig, S., and Fontaine, M. 2006. The
  Ecce and Logen partial evaluators and their web interfaces. In PEPM ’06. ACM Press,
  88–94.
Leuschel, M. and Lehmann, H. 2000. Coverability of reset Petri nets and other
  well-structured transition systems by partial deduction. In CL ’00. Lecture Notes in
  Artiﬁcial Intelligence 1861. Springer, 101–115.
Leuschel, M., Martens, B., and De Schreye, D. 1998. Controlling generalization
  and polyvariance in partial deduction of normal logic programs. ACM Transactions
  on Programming Languages and Systems 20, 1, 208–258.
Leuschel, M. and Massart, T. 2000. Inﬁnite state model checking by abstract inter-
  pretation and program specialisation. In LOPSTR ’99. LNCS 1817. Springer, 63–82.
Leuschel, M. and Sørensen, M. H. 1996. Redundant argument ﬁltering of logic
  programs. In LOPSTR ’96. LNCS 1207. Springer, 83–103.
Leuschel, M. and Vidal, G. 2005. Forward slicing by conjunctive partial deduction
  and argument ﬁltering. In ESOP ’05. LNCS 3444. Springer, 61–76.
Liang, T., Reynolds, A., Tsiskaridze, N., Tinelli, C., Barrett, C. W., and
  Deters, M. 2016. An eﬃcient SMT solver for string constraints. Formal Methods
  Syst. Des. 48, 3, 206–234.
Liqat, U., Georgiou, K., Kerrison, S., López-García, P., Hermenegildo, M.,
  Gallagher, J. P., and Eder, K. 2016. Inferring parametric energy consumption
  functions at diﬀerent software levels: ISA vs. LLVM IR. In FOPARA ’15. LNCS 9964.
  Springer, 81–100.
Liqat, U., Kerrison, S., Serrano, A., Georgiou, K., López-García, P., Grech,
  N., Hermenegildo, M., and Eder, K. 2014. Energy consumption analysis of pro-
  grams based on XMOS ISA-level models. In LOPSTR ’13. LNCS 8901. Springer,
  72–90.
Lloyd, J. 1987. Foundations of Logic Programming. Springer. 2nd Extended Edition.
Lloyd, J. W. and Shepherdson, J. C. 1991. Partial evaluation in logic programming.
  J. Log. Program. 11, 217–242.
Lopes, N. P. and Monteiro, J. 2016. Automatic equivalence checking of programs
  with uninterpreted functions and integer arithmetic. Intl. Journal on Software Tools
  for Technology Transfer 18, 4, 359–374.
López-García, P., Darmawan, L., Bueno, F., and Hermenegildo, M. 2012.
  Interval-based resource usage veriﬁcation: Formalization and prototype.           In
  FOPARA ’11. LNCS 7177. Springer, 54–71.
López-García, P., Darmawan, L., Klemen, M., Liqat, U., Bueno, F., and
  Hermenegildo, M. 2018. Interval-based resource usage veriﬁcation by translation
  into Horn clauses and an application to energy consumption. Theor. Pract. Logic
  Program. 18, 2, 167–223.
68 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

López-García, P., Haemmerlé, R., Klemen, M., Liqat, U., and Hermenegildo,
 M. 2015. Towards energy consumption veriﬁcation via static analysis. In HIP3ES
 Workshop. arXiv:1512.09369.
López-García, P., Klemen, M., Liqat, U., and Hermenegildo, M. 2016. A gen-
 eral framework for static proﬁling of parametric resource usage. Theor. Pract. Logic
 Program. 16, 5–6, 849–865.
Madhusudan, P., Parlato, G., and Qiu, X. 2011. Decidable logics combining heap
 structures and data. In POPL ’11. ACM Press, 611–622.
Marriott, K. and Søndergaard, H. 1988. Bottom-up abstract interpretation of
 logic programs. In Conf. and Symp. on Logic Programming. MIT Press, 733–748.
Martens, B. and Gallagher, J. P. 1995. Ensuring global termination of partial
 deduction while allowing ﬂexible polyvariance. In ICLP ’95. MIT Press, 597–611.
Matiyasevich, J. V. 1970. Enumerable sets are diophantine. Doklady Akademii Nauk
 SSSR 191, 279–282. In English: Soviet Mathematics–Doklady, 11 (1970), 354–357.
McMillan, K. L. 2013. Logic as the lingua franca of software veriﬁcation. Invited talk
 at the VMCAI ’13, Rome, Italy. Slides at https://studylib.net/doc/9889611/.
McMillan, K. L. and Rybalchenko, A. 2013. Solving constrained Horn clauses using
 interpolation. MSR Tech. Rep.t 2013-6, Microsoft Research, Redmond, WA, USA.
Mendelson, E. 1997. Introduction to Mathematical Logic. Chapman&Hall. 4th Edition.
Méndez-Lojo, M., Navas, J., and Hermenegildo, M. 2007. A ﬂexible (C)LP-based
 approach to the analysis of object-oriented programs. In LOPSTR ’07. LNCS 4915.
 Springer, 154–168.
Mesnard, F., Payet, É., and Vidal, G. 2020. Concolic testing in CLP. Theory Pract.
 Log. Program. 20, 5, 671–686.
Meudec, C. 2001. ATGen: Automatic test data generation using constraint logic pro-
 gramming and symbolic execution. Softw. Test. Verification Reliab. 11, 2, 81–96.
Meyer, B. 1988. Object-oriented Software Construction. Prentice Hall.
Monniaux, D. 2000. Abstract interpretation of probabilistic semantics. In SAS ’00.
 LNCS 1824. Springer, 322–339.
Mordvinov, D. and Fedyukovich, G. 2017. Synchronizing constrained Horn clauses.
 In LPAR-21. EPiC Series in Computing, vol. 46. EasyChair, 338–355.
Mordvinov, D. and Fedyukovich, G. 2019. Property directed inference of relational
 invariants. In Formal Methods in Computer Aided Design ’19. IEEE, 152–160.
Muthukumar, K. and Hermenegildo, M. 1990. Deriving a ﬁxpoint computation
 algorithm for top-down abstract interpretation of logic programs. Techn. Rep. ACT-
 DC-153-90, MCC, Austin, TX 78759.
Muthukumar, K. and Hermenegildo, M. 1992. Compile-time derivation of variable
 dependency using abstract interpretation. J. Log. Program. 13, 2/3, 315–347.
Navas, J., Méndez-Lojo, M., and Hermenegildo, M. 2008. Safe upper-bounds
 inference of energy consumption for Java bytecode applications. In NASA Langley
 Formal Methods Workshop. 29–32.
Navas, J., Méndez-Lojo, M., and Hermenegildo, M. 2009. User-deﬁnable resource
 usage bounds analysis for Java bytecode. In BYTECODE ’09 Workshop. Electronic
 Notes in Theoretical Computer Science 253, 5. Elsevier, 65–82.
Navas, J., Mera, E., López-García, P., and Hermenegildo, M. 2007. User-
 deﬁnable resource bounds analysis for logic programs. In ICLP ’07. LNCS 4670.
 Springer, 348–363.
Analysis and Transformation of Constrained Horn Clauses for Program Verification 69

Nelson, G. and Oppen, D. C. 1979. Simpliﬁcation by cooperating decision procedures.
  ACM Transactions on Programming Languages and Systems 1, 2, 245–257.
Nielson, H. R. and Nielson, F. 1992. Semantics With Applications - A Formal
  Introduction. Wiley Professional Computing. Wiley.
Nilsson, U. 1995. Abstract interpretation: A kind of magic. Theor. Comput. Sci. 142, 1,
  125–139.
Nipkow, T., Wenzel, M., and Paulson, L. C. 2002. Isabelle/HOL: A Proof Assistant
  for Higher-Order Logic. Springer.
Ochoa, C., Puebla, G., and Hermenegildo, M. 2006. Removing superﬂuous ver-
  sions in polyvariant specialization of Prolog programs. In LOPSTR ’05. LNCS 3901.
  Springer, 80–97.
Peralta, J. C. and Gallagher, J. P. 2003. Convex hull abstractions in specialization
  of CLP programs. In LOPSTR ’02. LNCS 2664. Springer, 90–108.
Peralta, J. C., Gallagher, J. P., and Saglam, H. 1998. Analysis of imperative
  programs through analysis of constraint logic programs. In SAS ’98. LNCS 1503.
  Springer, 246–261.
Pérez-Carrasco, V., Klemen, M., López-García, P., Morales, J. F., and
  Hermenegildo, M. 2020. Cost analysis of smart contracts via parametric resource
  analysis. In SAS ’20. LNCS 12389. Springer.
Pettorossi, A. and Proietti, M. 1994. Transformation of logic programs: Founda-
  tions and techniques. J. Log. Program. 19–20, 261–320.
Plotkin, G. 1981. A structural approach to operational semantics. Technical report
  DAIMI FN-19, Computer Science Department, Aarhus University, Denmark.
Proietti, M. and Pettorossi, A. 1993. The loop absorption and the generaliza-
  tion strategies for the development of logic programs and partial deduction. J. Log.
  Program. 16, 1–2, 123–161.
Proietti, M. and Pettorossi, A. 1995. Unfolding-deﬁnition-folding, in this order, for
  avoiding unnecessary variables in logic programs. Theor. Comput. Sci. 142, 1, 89–124.
Puebla, G., Albert, E., and Hermenegildo, M. 2006. Abstract interpretation with
  specialized deﬁnitions. In SAS ’06. LNCS 4134. Springer, 107–126.
Puebla, G., Bueno, F., and Hermenegildo, M. 2000. Combined static and dynamic
  assertion-based debugging of constraint logic programs. In LOPSTR ’99. LNCS 1817.
  Springer, 273–292.
Puebla, G. and Hermenegildo, M. 1996. Optimized algorithms for the incremental
  analysis of logic programs. In SAS ’96. LNCS 1145. Springer, 270–284.
Puebla, G. and Hermenegildo, M. 1999. Abstract multiple specialization and its
  application to program parallelization. J. Log. Program. 41, 2&3, 279–316.
Puebla, G., Hermenegildo, M., and Gallagher, J. P. 1999. An integration of
  partial evaluation in a generic abstract interpretation framework. In ACM SIGPLAN
  PEPM ’99. BRISC Series NS-99-1. University of Aarhus, Denmark, 75–85.
Reps, T. W., Horwitz, S., and Sagiv, S. 1995. Precise interprocedural dataﬂow
  analysis via graph reachability. In POPL ’95. ACM Press, 49–61.
Reynolds, A. and Kunčak, V. 2015. Induction for SMT solvers. In VMCAI ’15.
  LNCS 8931. Springer, 80–98.
Rohmer, J., Lescoeur, R., and Kerisit, J. 1986. The Alexander method - A tech-
  nique for the processing of recursive axioms in deductive databases. New Generation
  Computing 4, 3, 273–285.
70 E. De Angelis, F.Fioravanti, J.Gallagher, M.Hermenegildo, A.Pettorossi, M.Proietti

Rosu, G. and Serbanuta, T. 2010. An overview of the K semantic framework. Journal
  of Logic and Algebraic Programming 79, 6, 397–434.
Roychoudhury, A., Kumar, K. N., Ramakrishnan, C. R., and Ramakrishnan,
  I. V. 2002. Beyond Tamaki-Sato style unfold/fold transformations for normal logic
  programs. Intl. Journal on Foundations of Computer Science 13, 3, 387–403.
Roychoudhury, A., Kumar, K. N., Ramakrishnan, C. R., Ramakrishnan, I. V.,
  and Smolka, S. A. 2000. Veriﬁcation of parameterized systems using logic program
  transformations. In TACAS ’00. LNCS 1785. Springer, 172–187.
Rümmer, P. 2020. Competition Report: CHC-COMP-20. Tech. Rep. Available at
  https://chc-comp.github.io/report.pdf.
Sahlin, D. 1993. Mixtus: An automatic partial evaluator for full Prolog. New Generation
  Computing 12, 7–51.
Sato, T. and Kameya, Y. 1997. PRISM: A language for symbolic-statistical modeling.
  In 15th IJCAI ’97. Morgan Kaufmann, 1330–1339.
Schneidewind, C., Grishchenko, I., Scherer, M., and Maffei, M. 2020. eThor:
  Practical and provably sound static analysis of Ethereum smart contracts. In CCS ’20 :
  ACM Conf. on Computer and Communications Security. ACM Press, 621–640.
Schrijver, A. 1998. Theory of Linear and Integer Programming. John Wiley & Sons.
Seki, H. 1991. Unfold/fold transformation of stratiﬁed programs. Theoretical Computer
  Science 86, 107–139.
Seki, H. 2012. Proving properties of co-logic programs by unfold/fold transformations.
  In LOPSTR ’11. LNCS 7225. Springer, 205–220.
Senni, V. and Fioravanti, F. 2012. Generation of test data structures using constraint
  logic programming. In Tests and Proofs. LNCS 7305. Springer, 115–131.
Serrano, A., López-García, P., and Hermenegildo, M. 2014. Resource usage
  analysis of logic programs via abstract interpretation using sized types. Theor. Pract.
  Logic Program. 14, 4-5, 739–754.
Sharir, M. and Pnueli, A. 1981. Two approaches to interprocedural data ﬂow analysis.
  In Program Flow Analysis: Theory and Applications. Prentice-Hall, Chapter 7, 189–233.
Shemer, R., Gurfinkel, A., Shoham, S., and Vizel, Y. 2019. Property directed self
  composition. In CAV ’19, Part I. LNCS 11561. Springer, 161–179.
Shoenfield, J. R. 1967. Mathematical Logic. Addison-Wesley Publishing Company.
Spoto, F., Mesnard, F., and Payet, É. 2010. A termination analyzer for Java
  bytecode based on path-length. ACM Trans. Program. Lang. Syst. 32, 3, 8:1–8:70.
Suter, P., Köksal, A. S., and Kunčak, V. 2011. Satisﬁability modulo recursive
  programs. In SAS ’11. LNCS 6887. Springer, 298–315.
Tamaki, H. and Sato, T. 1984. Unfold/fold transformation of logic programs. In
  ICLP ’84, S.-Å. Tärnlund, Ed. Uppsala University, Uppsala, Sweden, 127–138.
Tärnlund, S. 1977. Horn clause computability. BIT 17, 2, 215–226.
Tarski, A. 1955. A lattice-theoretical ﬁxpoint theorem and its applications. Pacific
  Journal of Mathematics 5, 285–309.
Thakur, M. and Nandivada, V. K. 2020. Mix your contexts well: Opportunities
  unleashed by recent advances in scaling context-sensitivity. In Conf. on Compiler
  Construction. ACM Press, 27–38.
Tsankov, P., Dan, A. M., Drachsler-Cohen, D., Gervais, A., Bünzli, F., and
  Vechev, M. T. 2018. Securify: Practical security analysis of smart contracts. In ACM
  Conf. on Computer and Communications Security. ACM Press, 67–82.
Analysis and Transformation of Constrained Horn Clauses for Program Verification 71

Unno, H., Torii, S., and Sakamoto, H. 2017. Automating induction for solving Horn
  clauses. In CAV ’17, Part II. LNCS 10427. Springer, 571–591.
Verschaetse, K. and De Schreye, D. 1992. Derivation of linear size relations by
  abstract interpretation. In PLILP ’92. LNCS 631. Springer, 296–310.
Wadler, P. L. 1990. Deforestation: Transforming programs to eliminate trees. Theo-
  retical Computer Science 73, 231–248.
Wang, W. and Jiao, L. 2016. Trace abstraction reﬁnement for solving Horn clauses.
  The Computer Journal 59, 8, 1236–1251.
Warren, D. S. 1992. Memoing for logic programs. Comm. of the ACM 35, 3, 93–111.
Warren, R., Hermenegildo, M., and Debray, S. K. 1988. On the practicality of
  global ﬂow analysis of logic programs. In Conf. & Symp. Logic Programming. MIT
  Press, 684–699.
Wybraniec-Skardowska, U. 2019. On certain axiomatizations of arithmetic of nat-
  ural and integer numbers. Axioms 8, 3. doi: 10.3390/axioms8030103.
Zaks, A. and Pnueli, A. 2008. CoVaC: Compiler validation by program analysis of
  the cross-product. In Intl. Symp. on Formal Methods. LNCS 5014. Springer, 35–51.
Zhou, Q., Heath, D., and Harris, W. 2019. Relational veriﬁcation via invariant-
  guided synchronization. In HCVS/PERR@ETAPS 2019. Elect. Proc. Theor. Comput.
  Sci. 296 , 28–41.
