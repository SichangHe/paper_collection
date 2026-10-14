                                                             Satisﬁability Modulo
                                                          Extensional Constant Arrays

                                                  Mathias Preiner(B)      , Aina Niemetz      , and Clark Barrett

                                                                Stanford University, Stanford, USA
                                                           {preiner,niemetz,barrett}@cs.stanford.edu




                                               Abstract. Reasoning about array data structures is a key requirement
                                               for many applications in hardware and software veriﬁcation, especially in
                                               combination with machine integers. The Satisﬁability Modulo Theories
                                               (SMT) theory of extensional arrays provides array read and write oper-
                                               ators and allows extensionality over arrays. This is suﬃcient to express
arXiv:2605.16820v3 [cs.LO] 20 Jul 2026




                                               many aspects of computer-aided veriﬁcation, but lacks succinctness to
                                               eﬃciently deal with arrays that are initialized with a default value. Exist-
                                               ing procedures for extending the SMT-LIB theory of arrays with support
                                               for constant arrays are limited to arrays with inﬁnite index domains, and
                                               existing implementations in SMT solvers only support a fragment of the
                                               theory for ﬁnite index domains. In this paper, we present a novel decision
                                               procedure for the theory of arrays with constant arrays that supports ar-
                                               bitrary index domains and is not limited to the inﬁnite case. We present
                                               our procedure as an abstract calculus and show its refutational and sat-
                                               isﬁability soundness. We implement a decision procedure based on our
                                               calculus in the state-of-the-art SMT solver Bitwuzla and evaluate its
                                               performance on a diverse collection of benchmarks and use cases.



                                         1   Introduction

                                         Arrays are an essential data structure in programming languages, and are com-
                                         monly used to model memory in hardware. The ability to eﬃciently reason about
                                         arrays, especially in combination with machine integers, is therefore a core re-
                                         quirement for many applications of computer-aided veriﬁcation [6, 15, 28]. Sat-
                                         isﬁability Modulo Theories (SMT) solvers for the theory of arrays provide such
                                         reasoning and serve as the back end engine for a wide range of applications.
                                             The SMT-LIB standard [8] deﬁnes a theory of arrays with extensionality
                                         as originally axiomatized by McCarthy [23]. This theory provides array read
                                         (select) and write (store) operators and allows extensionality (equality) over
                                         arrays. While this is suﬃcient to express many aspects of modeling memory
                                         and array data structures in hardware and software, the theory lacks the ability
                                         to succinctly express operations over multiple indices and memory initialization.
                                         When modeling an array initialized with a default value, e.g., to represent a zero-
                                         initialized chunk of memory, this initialization must be expressed via a nested
                                         store expression that explicitly writes the default value to all relevant indices.
This leads to inaccuracies in the modeling as indices can only be explicitly over-
written, and to ineﬃciencies in solving procedures as the nesting depth of such
store chains can become very deep, depending on the number of relevant indices.
    Extending the SMT-LIB theory of arrays with so-called constant arrays, i.e.,
arrays that store a single element at every index, provides a succinct way to
model array initialization with a default value (which may be an arbitrary term).
Existing procedures for this extended theory of extensional constant arrays,
however, are all restricted to inﬁnite index domains [20, 26, 34].
    In this paper, we present a novel decision procedure for the theory of exten-
sional constant arrays that is not restricted to inﬁnite index sorts. Our procedure
is presented as an abstract calculus and is a generalization and extension of the
Lemmas on Demand (LOD) procedure for the extensional theory of arrays pre-
sented in [12]. In particular, we make the following contributions:

 – We generalize the LOD procedure for the extensional theory of arrays with
   ﬁxed-size bit-vectors presented in [12] to arbitrary index and element sorts.
 – We present this generalization as an abstract calculus AEXT, which serves
   as the core calculus of our new decision procedure and is decoupled from the
   LOD solving paradigm [9, 24].
 – We then extend this core calculus with support for extensional constant
   arrays, and prove refutational and satisﬁability soundness of our resulting
   calculus CAEXT for the theory of extensional constant arrays.
 – We implemented our procedure in the state-of-the-art SMT solver Bitwu-
   zla [27]. We evaluate it on a diverse collection of benchmarks and use cases,
   including applications in hardware model checking and smart contract ver-
   iﬁcation of the Ethereum virtual machine. Our evaluation shows that our
   new procedure signiﬁcantly expands the solving capabilities of Bitwuzla.

Related Work. The extension of the theory of arrays with constant arrays is
not yet standardized in SMT-LIB [8]. Over the years, several array procedures
incorporated support for constant arrays to some extent, with limitations [20,26,
31, 34]. Several state-of-the-art SMT solvers [7, 13, 14, 16, 25, 27, 28] have limited
support for constant arrays. To the best of our knowledge, none provide full
support for extensional constant arrays with ﬁnite index domains.
    In 2001, Stump et al. [34] axiomatized the extensional theory of arrays with
constant arrays and presented a sound and complete decision procedure for the
extensional theory of arrays. The authors also proposed an extension of the
procedure with support for constant arrays over inﬁnite index domains, which
is not implemented in any state-of-the-art SMT solver.
    In 2009, de Moura and Bjørner [26] proposed a procedure for the so-called
combinatory array logic (CAL) extension of the extensional array theory, which is
implemented by the SMT solver Z3 [25]. The CAL extension includes constant
arrays, and the procedure is, again, limited to inﬁnite index domains. While
Z3 accepts problems that use constant arrays with ﬁnite index domains, in our
experiments, we encountered cases where it reported wrong answers. All of these
instances involved extensionality over constant arrays with ﬁnite index domains.
We faced a similar issue with MathSAT5 [14], which supports constant arrays
and accepts input problems over extensional constant arrays with ﬁnite index
domains but reported wrong answers for some instances involving extensionality.
    cvc5 [7] implements a procedure based on [26], restricting support for con-
stant arrays to the non-extensional case, and to interpreted constants as elements
(arbitrary terms are not allowed). SMTInterpol [13] supports satisﬁability and
interpolation queries for the extensional theory of arrays with constant arrays
as presented by Hoenicke and Schindler [20] in 2019, also limited to the inﬁnite
index domain case. Yices2 [16] does not have native support for constant arrays,
but has limited support for non-extensional constant arrays by means of encoding
them as lambda terms. However, Yices2 gives up if the lambda terms cannot be
eliminated via beta reduction. Boolector [28] generalizes the lemmas on demand
procedure for extensional arrays described in [12] to non-recursive ﬁrst-order
lambda terms [30, 31] and allows reasoning about constant arrays (modeled as
lambda terms) for the non-extensional theory of arrays with constant arrays.
    Bitwuzla [27] implements and extends the array procedure from [12] with
support for (extensional) nested arrays and non-extensional constant arrays.
Until now, extensionality over constant arrays was not supported.


2   Preliminaries

We assume and brieﬂy review the usual notions and terminology of many-sorted
ﬁrst-order logic with equality (see, e.g., [18,22] for a more detailed introduction).
    Let S be a set of sort symbols, and let Σ be a signature containing a set
Σ s ⊆ S of sort symbols and a set Σ f of function symbols f s1 ···sn s with arity
n ≥ 0 and s1 , ..., sn , s ∈ Σ s . We usually omit the superscript from function
symbols and refer to 0-arity function symbols as constants.
    We assume that Σ includes a designated sort Bool, Boolean constants ⊤ (true)
and ⊥ (false), Boolean connectives {∧, ¬ } deﬁned as usual, equality and dise-
quality symbols {≈, 6≈} of sort s × s → Bool for every s ∈ Σ s , and an if-then-else
operator ite of sort Bool × s × s → s for every s ∈ Σ s .
    Let I be a Σ-interpretation that maps each s ∈ Σ s to a non-empty set sI
(the domain of I), with BoolI = {⊤, ⊥}; and each f s1 ···sn s ∈ Σ f to a total
function f I : sI1 × ... × sIn → sI if n > 0, and to an element in sI if n = 0.
We denote the domain size of a sort s ∈ Σ s as |sI |, e.g., |BoolI | = 2. The
interpretation of Boolean connectives, Boolean constants, equality symbols and
ite symbols is ﬁxed and standard. We use the usual inductive deﬁnition of the
satisﬁability relation |= between Σ-interpretations and Σ-formulas.
    A theory is a pair (Σ, I) where Σ is some signature, and I is a class of
Σ-interpretations. A Σ-formula is T -satisﬁable (resp. T -unsatisﬁable) if it is
satisﬁed by some (resp. no) interpretation in I; it is T -valid if it is satisﬁed
by all interpretations in I. We assume the usual deﬁnition of well-sorted terms,
literals, and formulas, and call Σ-formulas T -formulas and Σ-literals T -literals.
We sometimes refer to standard ﬁrst-order logic as the empty theory TE .
               Table 1. Signature for the theory of constant arrays ThAi .

    Syntax     SMT-LIB           Arity                              Comment
    ·[·]       select            (σ → τ ) × σ → τ                   Array access (read)
    ·h· ⊳ ·i   store             (σ → τ ) × σ × τ → (σ → τ )        Array update (write)
    h·iσ                         τ → (σ → τ )                       Constant array



     A literal is ﬂat if it is of the form ⊥, p(x1 , . . . , xn ), ¬p(x1 , . . . , xn ), x ≈ y,
x 6≈ y, or x ≈ f (x1 , . . . , xn ), where p and f are function symbols and x, y, and
x1 , . . . , xn are uninterpreted constants.


3       A Theory of Extensional Constant Arrays

The SMT-LIB theory of extensional arrays TA deﬁnes a parameterized sort
(σ → τ ) for arrays with index sort σ and element sort τ . Its signature contains
two interpreted function symbols for accessing (select) and writing (store) to
arrays as axiomatized by McCarthy in [23].
    In the following, we use symbol σ for array index sorts, symbol τ for array
element sorts, symbols a, b, c, d, e for arrays of sort (σ → τ ), symbols i, j, k for
indices of sort σ, and symbols u, v, w for elements of sort τ .
    We deﬁne the theory of extensional constant arrays ThAi = (ΣhAi , IhAi ) as
an extension of TA with an additional interpreted function symbol for construct-
ing constant arrays. The signature ΣhAi of theory ThAi is shown in Table 1.
Array access function a[i] reads an element from array a at index i (select),
and array update function ahi ⊳ ui constructs a new array that is identical to ar-
ray a except for index i where it stores element u (store). Further, as originally
proposed by Stump et al. in [34], ΣhAi includes a constant array constructor
operator hviσ . This operator creates an array of sort (σ → τ ) that stores a single
element v at all indices and is currently not deﬁned in SMT-LIB. The majority
of SMT solvers that support constant arrays, however, support the ((as const
(Array IndexSort ElementSort)) v) SMT-LIB construct as a constant array
constructor. We omit σ from hviσ if the index sort is clear from the context.


3.1       Axiomatization of ThAi

The theory of extensional constant arrays ThAi is axiomatized by the following
four axioms. Array access and update are deﬁned by McCarthy’s read-over-write
axioms row-eq and row-ne [23]. Note that the axiomatization scheme for the non-
extensional theory of arrays only includes these two axioms.
    Axiom row-eq states that if array ahi⊳ui, which results from storing element u
at index i in array a, is accessed at that index, the accessed element must be u.

                          ∀ a, i, j, u . i ≈ j =⇒ ahi ⊳ ui[j] ≈ u                   (row-eq)
Axiom row-ne covers the symmetric opposite case and states that all elements
that were not overwritten by store ahi ⊳ ui remain unchanged.

                       ∀ a, i, j, u . i 6≈ j =⇒ ahi ⊳ ui[j] ≈ a[j]                    (row-ne)

   The extensionality axiom ext states that two arrays are equal if and only if
both store the same element on each index. The axiomatization scheme for the
extensional theory of arrays TA consists of this and the previous two axioms.

                           ∀ a, b . a ≈ b ⇐⇒ ∀ i . a[i] ≈ b[i]                           (ext)

The axiomatization scheme for the extensional theory of constant arrays ThAi
extends the scheme for TA with the read-over-constant-array axiom roc [34].
This axiom states that accessing a constant array at any arbitrary index always
yields its default value (the value it was constructed with).

                                     ∀ i, v . hvi[i] ≈ v                                 (roc)

3.2   Inﬁnite vs. Finite Constant Arrays
A major limitation of previous work on extensionality of constant arrays [20,26,
34] is its restriction to inﬁnite index domains. In the following, we illustrate why
the restriction to inﬁnite constant arrays signiﬁcantly simpliﬁes procedures for
extensional constant arrays.
     Given two constant arrays hvi and hwi, from axioms ext and roc it follows
that hvi and hwi are equal if and only if their default values v and w are equal,
i.e., ∀v, w . hvi ≈ hwi ⇐⇒ v ≈ w. For constant arrays with inﬁnite index
domain, the same also holds for equality over array stores on constant arrays,
e.g., hvihi ⊳ wihj ⊳ wihk ⊳ wi ≈ hwi. Intuitively, inﬁnite constant arrays with
diﬀerent default values cannot be “made” equal since this requires an inﬁnite
number of array stores, which cannot be expressed in the array theory. Thus, for
inﬁnite constant arrays hvi and hwi, an equality over update sequences on hvi
and hwi cannot hold if v ≈ w does not hold.
     For ﬁnite index domains, however, two constant arrays with diﬀerent default
values can be made equal if suﬃciently many stores ensure that they are equal
on every index. For example, formula hvihi ⊳ wihj ⊳ wi ≈ hwi ∧ v 6≈ w is satisﬁable
for constant arrays with an index domain of size two, since it is possible to ﬁnd
an interpretation for i and j such that all indices of hvi are updated to w.
     More generally, two ﬁnite constant arrays hviσ and hwiσ with diﬀerent default
values v and w diﬀer on a ﬁnite number of indices n = |σ I |. Consider the
following equality over array update sequences on hvi and hwi:

            hvihi1 ⊳ wih. . . ⊳ . . .ihil ⊳ wi ≈ hwihj1 ⊳ vih. . . ⊳ . . .ihjk ⊳ vi

      If v 6≈ w, this equality only holds if the indices not updated in array update
sequence sv := hvihi1 ⊳ wih. . . ⊳ . . .ihil ⊳ wi are updated in sw := hwihj1 ⊳ vih. . . ⊳
. . .ihjk ⊳ vi, i.e., sv and sw must perform at least n array updates, on n distinct
                            ≈                                                            ≈

      hvihi1 ⊳ u1 i                  ahj1 ⊳ u2 i                       ahi2 ⊳ u3 i               hwihj2 ⊳ u4 i

  ⊤     ⊥         ⊥    ⊥         ⊤    ⊥     ⊥      ⊥               ⊤    ⊤     ⊤      ⊥       ⊤     ⊤         ⊤   ⊥


       h00 ⊳ ⊤i                               h10 ⊳ ⊥i         h01 ⊳ ⊤i                            h11 ⊳ ⊥i



  ⊥     ⊥         ⊥    ⊥                           ⊤   ⊥       ⊤   ⊥                         ⊤     ⊤         ⊤   ⊤

            hvi                                            a                                           hwi


Fig. 1. Visualization of the interpretation satisfying formula ϕ∧v 6≈ w from Example 2.


indices. In other words, interpretation I satisﬁes formula sv ≈ sw ∧ v 6≈ w if and
only if σ I = {iI1 , . . . , iIl , j1I , . . . , jkI }. For any number of array stores l + k < n,
the equality does not hold since sv and sw diﬀer on at least n − (l + k) indices.
   Thus, the main challenge of deciding the equality of two store sequences over
diﬀerent ﬁnite constant arrays is to check whether there exists an arrangement of
n = |σ I | unique array updates such that the resulting updated arrays are equal.
Example 1. Consider formula ϕ over inﬁnite constant arrays, and assume that
arrays hvi, a, and hwi are indexed by integers and store Booleans as elements.
                      ϕ := hvihi1 ⊳ u1 i ≈ ahj1 ⊳ u2 i ∧ ahi2 ⊳ u3 i ≈ hwihj2 ⊳ u4 i
Formula ϕ ∧ v ≈ w is satisﬁable and satisﬁed, e.g., by interpretation
         {a = h⊥i, v = w = u1 = u2 = u3 = u4 = ⊥, i1 = i2 = j1 = j2 = 0}.
Formula ϕ ∧ v 6≈ w, however, is unsatisﬁable since hvi and hwi store diﬀerent
elements at inﬁnitely many indices. Thus, there exists no arrangement for array
updates at indices i1 , i2 , j1 , and j2 to make the array update sequences equal.
                                                                                 ⊓
                                                                                 ⊔

Example 2. Now, for formula ϕ from Example 1 above, assume that arrays hvi,
a, and hwi are indexed by bit-vectors of size two, i.e., by a ﬁnite index sort.
Formula ϕ ∧ v ≈ w is still satisﬁable and satisﬁed, e.g., by interpretation
         {a = h⊥i, v = w = u1 = u2 = u3 = u4 = ⊥, i1 = i2 = j1 = j2 = 00}.
Interestingly, formula ϕ ∧ v 6≈ w is now also satisﬁable since the array stores on
indices i1 , i2 , j1 , and j2 can be arranged in a way such that each equality holds.
One possible interpretation satisfying this formula, as illustrated by Figure 1, is
                             {a = {00 7→ ⊤, 01 7→ ⊥, 10 7→ ⊤, 11 7→ ⊥},
                               v = u2 = u4 = ⊥, w = u1 = u3 = ⊤,
                              i1 = 00, i2 = 01, j1 = 10, j2 = 11}.
    On the other hand, formula ϕ∧v 6≈ w∧i1 ≈ j1 is unsatisﬁable since constraint
i1 ≈ j1 decreases the number of updates on distinct indices to three, but |σ I | = 4
unique updates are required to satisfy both equalities. Similarly, formula ϕ ∧ v 6≈
w ∧i1 6≈ j1 ∧u1 ≈ u2 is also unsatisﬁable. While the array stores can be arranged
to update four distinct indices, the additional constraint u1 ≈ u2 results in array
store hvihi1 ⊳ u1 i to update index i1 to u2 . However, since i1 6≈ j1 , we have that
u2 ≈ v and thus, the array update on i1 leaves hvi unchanged while the remaining
three array updates are not suﬃcient to satisfy both equalities.                   ⊓
                                                                                   ⊔


4   Calculus

In this section, we ﬁrst generalize and formalize the decision procedure for the
extensional theory of arrays presented in [12], which we refer to as DPA , as an
abstract base calculus AEXT. We then extend AEXT with a set of new rules to
handle extensional ﬁnite and inﬁnite constant arrays, yielding a new calculus
CAEXT, which maintains full generality with respect to the ﬁniteness of the
index domain of constant arrays. Finally, we prove that CAEXT is sound and
complete for the theory of extensional constant arrays ThAi .
    In the following, we brieﬂy introduce common assumptions, deﬁnitions and
notation used to deﬁne our base calculus and its extension.

Assumption 1 Whenever we refer to a set of ΣA -formulas A, we assume that
all literals in A are ﬂat.                                             ⊓
                                                                       ⊔

    This assumption is without loss of generality as any set of ΣA -formulas can be
easily transformed into a TA -equisatisﬁable set by the addition of fresh variables
and equalities. Note that some of the derivation rules we introduce later intro-
duce non-ﬂat literals in A. In such cases, we assume that similar transformations
maintain the invariant that all literals in A are ﬂat.

Deﬁnition 1 (Conﬁguration). A conﬁguration is either the distinguished con-
ﬁguration unsat or a tuple hA, I, πi, where A is a set of ΣA -formulas, I is an
interpretation in the empty theory TE that satisﬁes A, and π is a map of propa-
gation steps (as deﬁned in Deﬁnition 2).                                      ⊓
                                                                              ⊔

    Calculus rules modify conﬁgurations and are given in guarded assignment
form, where the rule premises describe the conditions on the current conﬁgu-
ration under which the rule can be applied. The conclusion of a rule is either
unsat or otherwise describes the resulting modiﬁcations to the conﬁguration. An
application of a rule is redundant if it has a conclusion where each component of
the derived conﬁguration is equal to the corresponding component in the premise
conﬁguration, i.e., it remains unchanged. A conﬁguration is saturated with re-
spect to a set of rules if every possible application of each rule is redundant.
    In the following, we use T (A) to denote the set of all terms in formulas A, and
TA (A) to denote all array terms in A. Further, we assume that array disequalities
a 6≈ c ∈ A are represented as ¬(a ≈ c).
4.1   Base Calculus

In this section, we generalize and formalize the LOD decision procedure DPA
for the extensional theory of arrays of [12] as our base calculus AEXT.
    The main concept of DPA as presented in [12] is based on a ﬁxed point al-
gorithm for propagating and congruence checking array reads. The algorithm
produces lemmas that are derived from McCarthy’s array axioms without intro-
ducing new array reads. In [12], procedure DPA assumes that TA is combined
with a single, decidable theory for array indices and elements, and is presented
in the context of combining TA with the theory of ﬁxed-size bit-vectors TBV .
It is based on the lemmas on demand paradigm [9, 24], but with a bit-vector
abstraction at its core, and relies on necessary formula transformations during
preprocessing that introduce virtual reads for array equalities and writes. The
authors show that for this combination of theories, DPA is sound and complete.
    We generalize DPA to combinations of TA with arbitrary theories for array
indices and elements and decouple it from the LOD paradigm. Our generalized
procedure for the theory of extensional arrays TA does not rely on necessary
formula transformations during preprocessing, does not assume that array index
and element sorts belong to the same theory, and does not rely on the existence
of a decision procedure for index and element theories. Instead, it assumes an
interpretation of index and element terms in the empty theory TE .
    We formalize our generalized procedure in terms of our base calculus AEXT.
Given a set of ΣA -formulas A and a current interpretation I |= A, the derivation
rules of our base calculus aim to propagate information about array indices and
elements from one array to another, based on the axioms of TA . For example, for
an array access ahj ⊳ ui[i], if I |= i 6≈ j, from axiom row-ne it follows that ahj ⊳
ui[i] ≈ a[i]. We can therefore propagate the information that reading from ahj⊳ui
at index i yields the same element as reading from a at index i. Our calculus
explores propagations under the current interpretation until unsatisﬁability is
derived, or all possible propagations have been explored.
    Calculus AEXT consists of the set of derivation rules given in Figures 2 and 3.
Figure 2 lists all rules required for the non-extensional theory of arrays, while
Figure 3 shows the supplemental rules to handle the extensional theory of arrays.

Deﬁnition 2 (Propagation Step). A propagation step π(a, t) := (r, c) maps
a propagated term t and its destination array a to a tuple (r, c), where r deﬁnes
the reason for propagating t from source array c to the destination array a. ⊓ ⊔

    Given a conﬁguration hA, I, πi, the propagation path of a read b[i] to destina-
tion array a can be constructed as a sequence of propagation steps by following
the steps in reverse order. That is, starting from π(a, b[i]), we reach π(b, b[i])
via the propagation path {π(a, b[i]) := (rn , cn ), π(cn , b[i]) := (rn−1 , cn−1 ), . . . ,
π(c1 , b[i]) := (r1 , b), π(b, b[i]) := (⊤, b)}. The reason R(a, b[i]) for propagating b[i]
from b to a along this path is deﬁned as follows.

Deﬁnition 3 (Propagation Reason). For a propagation step π(a, t) := (r, c),
R(a, t) deﬁnes the reason for propagating t from its initial source array to des-
tination array a as follows.
                      
                      ()
                                     if π(a, t) = ()
            R(a, t) = ⊤               if t = a or t = a[i] for some i
                      
                      
                        R(c, t) ∧ r   otherwise, where π(a, t) = (r, c)

                                                                                  ⊓
                                                                                  ⊔

    Note that in the context of our base calculus AEXT, we only propagate
reads b[i] to destination arrays a, i.e., propagated term t in Deﬁnitions 2 and 3
is always a read. Thus, the second case of Deﬁnition 3 for t = a does not apply
and propagation reasons are only deﬁned as R(a, b[i]). When extending AEXT
with support for constant arrays to CAEXT, we also propagate default values of
constant arrays which we represent with case t = a, as we will explain later.

Start. Our calculus starts with the initial conﬁguration hA, I0 , π0 i with an empty
interpretation I0 := none and an empty map of propagation steps π0 := λx, y . ().
From this initial conﬁguration, it explores possible propagation steps π under a
current interpretation I for formulas A in the empty theory TE , as deﬁned by
rule Interp, while modifying the conﬁguration. If A is TE -unsatisﬁable, rule Conf
derives conﬁguration unsat. Else, if the conﬁguration is saturated, i.e., each rule
application is redundant and conﬁguration unsat was not derived, for each array
a ∈ TA (A), propagation steps π(a, ·) represent a partial model of a, which can
be extended to an interpretation IA that satisﬁes ΣA -formulas A.

Propagation. In addition to rules Interp and Conf , we distinguish propagation
rules that modify the map of propagation steps π (Init*, Row*, Eq*), and conﬂict
rules that modify the set of formulas A (CongR, DisEq).
    Rules InitR and InitW initialize map π for each direct read a[i] ∈ T (A) and
virtual read ahi ⊳ ui[i] for each write ahi ⊳ ui ∈ T (A), respectively. The purpose
of these virtual reads is to represent the written element u in terms of a read
ahi ⊳ ui[i], which allows for uniform handling of array read and write terms in
the calculus. This is similar to the approach of DPA , where virtual reads are
conceptually added to the formula via top-level equalities ahi ⊳ ui[i] ≈ u as a
preprocessing step. In our calculus, however, the congruence of ahi ⊳ ui[i] and u
is ensured by rules Interp and Conf .
    Rule RowD is based on a rule of DPA which applies read-over-write ax-
iom row-ne. Given a read ahj ⊳ ui[i], if i 6≈ j, by axiom row-ne we have that
ahj ⊳ ui[i] ≈ a[i]. However, instead of creating a (potentially) fresh read a[i],
we can use the existing read ahj ⊳ ui[i] as representative of a[i] under the cur-
rent interpretation I, and propagate ahj ⊳ ui[i] from source array ahj ⊳ ui down
to destination a, which is recorded in the conclusion of rule RowD by adding
propagation step π(a, ahj ⊳ ui[i]) := (i 6≈ j, ahj ⊳ ui) to the conﬁguration.

Conﬂict. Rule CongR is based on the congruence rule of DPA , which handles the
case where two reads b[i] and c[k] read diﬀerent elements from the same array a
                      I ′ |= A ∪ {ahi ⊳ ui[i] ≈ u | ahi ⊳ ui ∈ T (A)}               I = I0
             Interp
                                                I := I ′


                                                  a[i] ∈ T (A)
                                       InitR
                                               π(a, a[i]) := (⊤, a)


                                                ahi ⊳ ui ∈ T (A)
                          InitW
                                  π(ahi ⊳ ui, ahi ⊳ ui[i]) := (⊤, ahi ⊳ ui)


                         I |= i 6≈ j      π(ahj ⊳ ui, b[i]) 6= ()         π(a, b[i]) = ()
                RowD
                                        π(a, b[i]) := (i 6≈ j, ahj ⊳ ui)


                I |= i ≈ k        π(a, b[i]) 6= ()       π(a, c[k]) 6= ()         I |= b[i] 6≈ c[k]
 CongR
          A := A, (R(a, b[i]) ∧ R(a, c[k]) ∧ i ≈ k =⇒ b[i] ≈ c[k])                   (I, π) := (I0 , π0 )


                             A ∪ {ahi ⊳ ui[i] ≈ u | ahi ⊳ ui ∈ T (A)} |= ⊥
                      Conf
                                                      unsat


                      Fig. 2. AEXT rules for non-extensional arrays.



           I |= i 6≈ j       ahj ⊳ ui ∈ T (A)        π(a, b[i]) 6= ()          π(ahj ⊳ ui, b[i]) = ()
  RowU
                                        π(ahj ⊳ ui, b[i]) := (i 6≈ j, a)


      I |= a ≈ c       a, c ∈ TA (A)           a ≈ c ∈ T (A)          π(a, b[i]) 6= ()      π(c, b[i]) = ()
EqR
                                           π(c, b[i]) := (a ≈ c, a)


      I |= a ≈ c       a, c ∈ TA (A)           a ≈ c ∈ T (A)          π(c, b[i]) 6= ()      π(a, b[i]) = ()
EqL
                                           π(a, b[i]) := (a ≈ c, c)


                I |= a 6≈ c    a, c ∈ TA (A)     a ≈ c ∈ T (A)     k{a,c} 6∈ T (A)
        DisEq
                 A := A, (a 6≈ c =⇒ a[k{a,c} ] 6≈ c[k{a,c} ])  (I, π) := (I0 , π0 )


                         Fig. 3. AEXT rules for extensional arrays.
                                     π(hvi, b[i]) 6= ()        I |= b[i] 6≈ v
                  Roc
                        A := A, R(hvi, b[i]) =⇒ b[i] ≈ v              (I, π) := (I0 , π0 )


                 Fig. 4. CAEXT rule for non-extensional constant arrays.



                                                   hvi ∈ T (A)
                                   InitC
                                           π(hvi, hvi) := (⊤, hvi)

                                                                                        ^
                     π(ahj ⊳ ui, hvi) 6= ()       π(a, hvi) = ()        I |= ∃i : σ.        i 6≈ k
                                                                                k∈I(ahj⊳ui,hvi)∪{j}
            CowD
                                            π(a, hvi) := (⊤, ahj ⊳ ui)

                                                                                                     ^
          π(a, hvi) 6= ()      π(ahj ⊳ ui, hvi) = ()      ahj ⊳ ui ∈ T (A)            I |= ∃i : σ.       i 6≈ k
                                                                                             k∈I(a,hvi)∪{j}
   CowU
                                            π(ahj ⊳ ui, hvi) := (⊤, a)


          I |= a ≈ c        a, c ∈ TA (A)       a ≈ c ∈ T (A)         π(a, hvi) 6= ()           π(c, hvi) = ()
   CEqR
                                              π(c, hvi) := (a ≈ c, a)


          I |= a ≈ c        a, c ∈ TA (A)       a ≈ c ∈ T (A)         π(c, hvi) 6= ()        π(a, hvi) = ()
   CEqL
                                              π(a, hvi) := (a ≈ c, c)

                                                                                                ^
                π(a, hvi) 6= ()      π(a, hwi) 6= ()          I |= v 6≈ w        I |= ∃i : σ.       i 6≈ k
                                                                                     k∈I(a,hvi)∪I(a,hwi)
  CongC                                                   ^
          A := A, (R(a, hvi) ∧ R(a, hwi) ∧ ∃i : σ.            i 6≈ k) =⇒ v ≈ w            (I, π) := (I0 , π0 )
                                                k∈I(a,hvi)∪I(a,hwi)




                   Fig. 5. CAEXT rules for extensional constant arrays.


at the same index. Recall that with π(a, b[i]) 6= () and π(a, c[k]) 6= (), we have
that b[i] is a representative of a[i] and c[k] is a representative of a[k] under the
current interpretation I. However, if I |= i ≈ k ∧ b[i] 6≈ c[k], the congruence
axiom of TE is violated since i ≈ k ∧ b[i] ≈ a[i] ∧ c[k] ≈ a[k] =⇒ b[i] ≈ c[k]. As a
result, CongR adds a lemma to A to rule out the current spurious interpretation I.
Note that by modifying A, conﬁguration components π and I are reset to their
initial values π0 and I0 since π is dependent on the current interpretation I,
which does not satisfy the modiﬁed formulas A anymore.

Extensionality. The derivation rules given in Figure 3 are only required if A
contains extensionality over array terms. Similarly to rule RowD, if I |= i 6≈ j,
rule RowU applies axiom row-ne but propagates a[i] to ahj ⊳ ui, since the element
of a at index i remains unchanged after the update operation. Rules EqR and
EqL apply the extensionality axiom ext and propagate reads on arrays a and c
over equalities a ≈ c ∈ T (A) from left to right and vice versa.
    For array equalities a ≈ c for which I |= a 6≈ c, rule DisEq adds an instance of
axiom ext to A. This rule is the only rule that introduces fresh reads (on a fresh
index k{a,c} ), however, limited to at most two reads per equality. The added
lemma ensures that there exists at least one witness index k{a,c} at which arrays
a and c diﬀer. In contrast, DPA relies on a preprocessing step that eagerly adds
this lemma for each a ≈ c ∈ T (A), independent of whether I |= a 6≈ c.

4.2   Constant Array Extension
In this section, we extend our base calculus AEXT with a set of new rules to sup-
port extensional constant arrays. The new rules for our extended calculus CAEXT
are given in Figures 4 and 5. Figure 4 shows the additional conﬂict rule Roc re-
quired for handling reads over constant arrays, while Figure 5 lists the new rules
to handle extensional constant arrays.
    The main challenge of determining satisﬁability of equalities between store
sequences over diﬀerent ﬁnite constant arrays is that we have to reason about
default values for indices that have not been updated by array stores. A straight-
forward extension of AEXT would be the introduction of virtual reads for all
indices of a constant array, i.e., adding hviσ [i] ≈ v for all i ∈ σ I . However, this is
not feasible in general, neither for inﬁnite nor for ﬁnite index domains. For the
inﬁnite case, we would never reach a saturated conﬁguration due to inﬁnitely
many virtual reads. And while it may be feasible for reasonably small ﬁnite index
domains, large domains would require a potentially unfeasibly large number of
derivations to reach a saturated conﬁguration.
    Our extended calculus CAEXT avoids the introduction of virtual reads on
constant arrays. Instead, it propagates the default value v of a constant array hvi
to array a while keeping track of updated indices I(a, hvi) between a and hvi.

Deﬁnition 4 (Updated Indices). Given a propagation step π(a, hvi) := (r, c),
the set of updated indices I(a, hvi) consists of all indices updated while propa-
gating the default value of hvi to array a, and is deﬁned as follows.
              
              
              
               ()                if π(a, hvi) = ()
              
              
              
               ∅                 if a = hvi
   I(a, hvi) = I(b, hvi) ∪ {j} if π(a, hvi) = (⊤, b) with
              
              
              
              
                                        b = ahj ⊳ ui or a = bhj ⊳ ui for some u
              
              I(c, hvi)          otherwise, where π(a, hvi) = (r, c)

                                                                                       ⊓
                                                                                       ⊔

   Propagating the default value of hvi to array a is denoted as π(a, hvi), and
the reason for this propagation is denoted as R(a, hvi). If a default value v is
propagated to array a, indices of a that are not updated along the propagation
path store this default value.
Deﬁnition 5 (Array Default Value). Given array a and constant array hvi,
if π(a, hvi) 6= (), the default value of array a at indices i 6∈ I(a, hvi) is v, i.e.,
∀i : σ. i 6∈ I(a, hvi) =⇒ a[i] ≈ v. Otherwise, it is uninterpreted.                 ⊓
                                                                                    ⊔

    Figure 5 lists the rules for propagating array default values by modifying π
(rules InitC, Cow*, CEq*), and conﬂict rule CongC for extending A with a new
constant array congruence lemma.
    Rule InitC initializes map π for each constant array hvi ∈ T (A) with its default
value. Rules CowD and CowU propagate default values over array stores ahj ⊳ ui.
These two rules are only applied if there exists an index i that has not been
updated on the propagation path from hvi to array store ahj ⊳ ui and is diﬀerent
from j. For inﬁnite index domains, there always exists such an index i. Rules
CEqR and CEqL propagate default values over array equalities a ≈ c ∈ T (A)
from left to right and vice versa. Rule CongC handles the case when two default
values v and w with I |= v 6≈ w are propagated to the same indices of array a.

Example 3. Consider formula ϕ from Example 2, deﬁned over ﬁnite constant
arrays with bit-vectors of size 2 as indices and Booleans as elements. Our initial
conﬁguration is given as follows.
                       s                s              s                  s
               z    }|1   { z }|2 { z }|3 { z                  }|4   {
         A := hvihi1 ⊳ u1 i ≈ ahj1 ⊳ u2 i ∧ ahi2 ⊳ u3 i ≈ hwihj2 ⊳ u4 i ∧v 6≈ w
         I0 := none
         π0 := λx, y . ()

After applying rules InitW and InitC for all stores and constant arrays, we get

   π(s1 , s1 [i1 ]) := (⊤, s1 ),   π(s3 , s3 [i2 ]) := (⊤, s3 ),      π(hvi, hvi) := (⊤, hvi),
   π(s2 , s2 [j1 ]) := (⊤, s2 ),   π(s4 , s4 [j2 ]) := (⊤, s4 ),     π(hwi, hwi) := (⊤, hwi).

Now, assume rule Interp yields the following interpretation I:

           i1 = j1 = i2 = j2 , u1 = u2 = u3 = u4 , v 6= w, s1 = s2 , s3 = s4 ,
                             s1 [i1 ] = u1 , s2 [j1 ] = u2 , s3 [i2 ] = u3 , s4 [j2 ] = u4 .

We have that π(hvi, hvi) 6= () and π(s1 , hvi) = () for s1 = hvihi1 ⊳u1 i ∈ T (A), and
I(hvi, hvi) = {}. Since there exists an index not in {}∪{iI1 }, we can propagate hvi
to s1 by applying rule CowU, which yields π(s1 , hvi) := (⊤, hvi). Intuitively, after
we propagated the default value of hvi to s1 , all indices of s1 , except the updated
index i1 , have default value v. Next, rule CEqR can be applied and propagates hvi
from s1 to s2 , which yields π(s2 , hvi) := (s1 ≈ s2 , s1 ). Since π(s2 , hvi) 6= () and
π(a, hvi) = () for s2 = ahj1 ⊳ u2 i ∈ T (A) and there still exists an index not
in {iI1 } ∪ {j1I }, we can propagate hvi down to array a via rule CowD, which
yields π(a, hvi) := (⊤, s2 ). Note that under interpretation I, indices i1 and j1
are equal and thus {iI1 } ∪ {j1I } yields a set containing one index. Following the
same reasoning steps, from π(a, hvi) 6= () we can propagate hvi via rule CowU to
s3 , afterwards apply rule CEqR to propagate hvi to s4 , and ﬁnally propagate hvi
down to hwi, which yield the following conﬁguration of π:
  π(s1 , s1 [i1 ]) := (⊤, s1 ),π(s3 , s3 [i2 ]) := (⊤, s3 ),  π(hvi, hvi) := (⊤, hvi),
  π(s2 , s2 [j1 ]) := (⊤, s2 ),π(s4 , s4 [j2 ]) := (⊤, s4 ), π(hwi, hwi) := (⊤, hwi),
   π(s1 , hvi) := (⊤, hvi), π(s2 , hvi) := (s1 ≈ s2 , s1 ),      π(a, hvi) := (⊤, s2 ),
    π(s3 , hvi) := (⊤, a), π(s4 , hvi) := (s3 ≈ s4 , s3 ),     π(hwi, hvi) := (⊤, s4 ).
We now have that π(hwi, hvi) 6= (), π(hwi, hwi) 6= () and I(hwi, hvi) = {i1 , j1 , i2 , j2 },
but indices i1 , j1 , i2 , j2 are all equal under I, and v 6≈ w. This means that all
indices i 6= iI1 need to have the default v and w at the same time, which is not
possible, and thus, rule CongC adds the following lemma to A.
                   R(hwi,hvi)          R(hwi,hwi)
              z       }|      {            z}|{               ^
              s1 ≈ s2 ∧ s3 ≈ s4 ∧           ⊤       ∧ ∃i.           i 6≈ k =⇒ v ≈ w
                                                       k∈{i1 ,j1 ,i2 ,j2 }

After that I and π are reset to I0 and π0 , and we continue with a new inter-
pretation I. In the next interpretation, indices i1 , j1 , i2 , j2 will be forced to be
diﬀerent due to the added lemma, which may yield interpretation I:
       i1 6= j1 6= i2 6= j2 , u1 = u2 = u3 = u4 , u2 6= v, v 6= w, s1 = s2 , s3 = s4 ,
                                   s1 [i1 ] = u1 , s2 [j1 ] = u2 , s3 [i2 ] = u3 , s4 [j2 ] = u4 .
With this interpretation, after applying rules InitW and InitC, read s2 [j1 ] is prop-
agated from s2 to hvi by applying rules RowU, EqR, and RowD. This will result in
a new lemma generated by rule Roc, since π(hvi, s2 [j1 ]) 6= () and I |= s2 [j1 ] 6≈ v
due to I |= s2 [j1 ] ≈ u2 ∧ u2 6≈ v.
     Reads s1 [i1 ], s3 [i2 ], and s4 [j2 ] will be propagated similarly and after all con-
ﬂicts are resolved we can ﬁnally derive a saturated conﬁguration, and thus,
conclude with satisﬁable.
     The following interpretation I that will lead to a saturated conﬁguration,
i.e., by applying all rules until ﬁxed point, will not yield any conﬂict.
      I := {i1 6= j1 6= i2 6= j2 , v = u2 = u4 , w = u1 = u3 , v 6= w,
            s1 = s2 , s3 = s4 , s1 [i1 ] = u1 , s2 [j1 ] = u2 , s3 [i2 ] = u3 , s4 [j2 ] = u4 }.
                                                                                                     ⊓
                                                                                                     ⊔

4.3    Correctness
In this section, we establish the theorems for refutational and satisﬁability sound-
ness of our base calculus presented in Section 4.1, and its extension presented in
Section 4.2. Refutational soundness ensures that the calculus never reports unsat
unless the initial set of constraints is unsatisﬁable. Satisﬁability soundness is the
complementary property: if the calculus does not report unsat, then the initial
set of constraints is satisﬁable. This is often referred to as completeness, but we
ﬁnd the term satisﬁability soundness more precise in this context. We prove the
refutational and satisﬁability soundness of our calculus CAEXT in the appendix.
Theorem 1 (Refutational Soundness). If a derivation starting with an ini-
tial conﬁguration hA, I, πi ends in unsat, then A is TA -unsatisﬁable.

    Refutational soundness holds for arbitrary derivations. For satisﬁability sound-
ness, we need a restriction on the order in which propagations of default values
are recorded. Since rules Cow* and CEq* record at most one propagation step
per pair (a, hvi), the recorded set of updated indices I(a, hvi) is determined by
the ﬁrst recorded propagation path. This may result in an over-approximation
of the indices updated along other derivable propagation paths. For ﬁnite index
domains, this can lead to a conﬂict not detected by CongC if the existential side
condition fails on the union of the over-approximated index sets.
    We therefore restrict derivations to a strategy that records conﬂicting prop-
agations eagerly. That is, whenever rules InitC, Cow*, and CEq* admit sequences
of applications under I that make rule CongC applicable for some a, hvi and
hwi, we record the propagation steps that lead to that conﬂict before any other
propagation step. This strategy is eﬀective since only ﬁnitely many propagation
paths, that visit each each array at most once, need to be considered. Our im-
plementation realizes this strategy by intersecting the updated index sets over
all propagation paths explored under I.

Theorem 2 (Satisﬁability Soundness). If a derivation following the above
strategy, starting with an initial conﬁguration hA, I0 , π0 i, ends in a conﬁguration
other than unsat, and every applicable rule is redundant, then A is TA -satisﬁable.


5   Integration
In Section 4, we presented our new calculus CAEXT for the theory of extensional
constant arrays ThAi as a set of derivation rules that modify conﬁgurations start-
ing from the initial conﬁguration hA, I0 , π0 i. Our calculus is independent of the
underlying solver architecture and only requires the existence of a procedure
that provides an interpretation I in the empty theory TE (rule Interp).
    We integrated a decision procedure for ThAi based on our new calculus CAEXT
in the state-of-the-art SMT solver Bitwuzla [27]. Bitwuzla specializes on theo-
ries relevant for bit-precise reasoning and supports the theories of ﬁxed-size
bit-vectors, ﬂoating-point arithmetic, and combinations with arrays and unin-
terpreted functions. Until now, it implemented a decision procedure for the the-
ory of extensional arrays based on [12], extended with support for nested arrays
and non-extensional constant arrays. We replaced this procedure with a new
decision procedure based on CAEXT, which seamlessly integrates into the LOD
architecture of Bitwuzla. In the context of CAEXT, the bit-vector solver at the
core of its LOD architecture is responsible for providing interpretation I [29].
As implemented in Bitwuzla, our procedure incorporates several optimizations.

distinctN . When a conﬂict between two diﬀerent constant arrays is detected,
i.e., rule CongC applies, we produce a resulting lemma that does not actually
contain a quantiﬁed formula. Instead, the quantiﬁed formula is encoded as a
special variant of distinct , which we call distinctN . While distinct (t1 , . . . , tk ) is
true iﬀ terms t1 , . . . , tk are pairwise diﬀerent, distinctN (n, t1 , . . . , tk ) is true iﬀ at
least n terms are pairwise diﬀerent, i.e., the set of values assigned to t1 , . . . , tk has
at least n elements. If n = k, then distinctN (k, t1 , . . . , tk ) ≡ distinct (t1 , . . . , tk ),
while for n > k, distinctN (n, t1 , . . . , tk ) ≡ ⊥. Given a ﬁnite sort τ for ti and
k > |τ I |, distinct (t1 , . . . , tk ) ≡ ⊥, whereas distinctN (n, t1 , . . . , tk ) for n ≤ k is
not. We encode the quantiﬁed formula in CongC as follows.
                     ^
              ∃i : σ. i 6≈ k ≡ ¬distinctN (|σ I |, I(a, hvi) ∪ I(a, hwi))
             k∈I(a,hvi)∪I(a,hwi)

The intuition here is that this quantiﬁed formula is true if there exists an index i
that has not been updated between hvi and a and hwi and a, and is thus not
included in I∪ := I(a, hvi)∪I(a, hwi). For inﬁnite index domains, this will always
be ⊤. However, for ﬁnite index domains it depends on whether the set of updated
indices I∪ includes all possible indices of index domain σ I , which can be encoded
as distinctN (|σ I |, I(a, hvi) ∪ I(a, hwi)).
    As an additional optimization, we encode a given distinctN (n, t1 , . . . , tk ) con-
straint lazily and use a custom decision heuristic that tries to assign diﬀerent
values to terms t1 , . . . , tk . If our heuristic fails to assign n unique values to the
given terms, we lazily expand the encoding of the constraint until we ﬁnd n
diﬀerent values or conclude that distinctN (n, t1 , . . . , tk ) ≡ ⊥.

Propagation. In order to reduce memory overhead, we do not immediately record
pair (r, c) when constructing π(a, t) while exploring all possible propagations of
reads. Since these pairs are only required for constructing R, we instead replay
the propagation steps to produce the full map π containing (r, c) only for the
array reads involved in a conﬂict. In this replay phase, propagation is performed
in breadth-ﬁrst-search order, which yields the shortest sequence of propagation
steps to the conﬂict under the current interpretation.


6    Evaluation
We evaluate the performance of our procedure for the theory of extensional
constant arrays as implemented in the SMT solver Bitwuzla [27], denoted as
conﬁguration BitwuzlahAi . Bitwuzla supports the (quantiﬁed and quantiﬁer-free)
theories of ﬁxed-size bit-vectors and ﬂoating-point arithmetic, in combination
with arrays and uninterpreted functions. We therefore focus on problems over
ﬁnite constant arrays.
    We compare our conﬁguration BitwuzlahAi against its baseline version Bitwu-
zla (commit 961ccbc5 [3]), and the SMT solvers cvc5 [7] (version 1.3.2), Z3 [25]
(commit 9666915d [5]) and MathSAT5 [14] (version 5.6.16). These four support
diﬀerent fragments of theory ThAi . In particular, our conﬁguration BitwuzlahAi is
the only SMT solver that fully supports ThAi for ﬁnite constant arrays. Note that
Z3 and MathSAT5 allow the use of ﬁnite constant arrays without restrictions,
but we encountered soundness issues that suggest that they only support the
fragment of ThAi without extensionality over ﬁnite constant arrays. We exclude
Boolector [28] and SMTInterpol [13] from the evaluation, since they do not sup-
port extensionality over ﬁnite constant arrays. We further exclude MathSAT5
from quantiﬁed benchmark sets since it does not support quantiﬁer reasoning.
    Support for constant arrays is not yet standardized in the SMT-LIB language.
Thus, the SMT-LIB benchmark library [32, 33] does not include benchmarks
with constant arrays. We therefore evaluated our approach in diﬀerent usage
scenarios: a) on benchmarks without constant arrays but where reasoning about
constant arrays is required internally to Bitwuzla; and b) on a compilation of
diverse sets of benchmarks with constant arrays, one crafted and the others
stemming from diﬀerent applications. We use the following benchmark sets.

smtlib (5,112 benchmarks). The non-incremental benchmarks of the quantiﬁed
logics ABV, ABVFP and ABVFPLRA of the SMT-LIB benchmark library [33]. These
benchmarks do not contain constant arrays but require constant array reasoning
in subsolver queries of the model-based quantiﬁer instantiation (MBQI) [19] en-
gine implemented in Bitwuzla. This is due to the MBQI procedure asserting the
model value of each constant x that occurs in the ground formulas via equalities
of the form x ≈ xI . The model value of an array constant is represented as a
store chain on a constant-initialized array. This inevitably introduces equalities
over constant arrays. We use this set to evaluate how much our new procedure
improves quantiﬁed reasoning with arrays in Bitwuzla.

mbqi (4,147 benchmarks). A set of quantiﬁer-free non-incremental benchmarks
deﬁned over value-initialized and nested extensional constant arrays with ﬁxed-
size bit-vectors. These benchmarks were extracted from subsolver queries of the
MBQI solver of BitwuzlahAi on benchmarks from set smtlib that were unsolved
by baseline conﬁguration Bitwuzla due to subsolver queries with extensional
constant arrays. We included at most one satisﬁable and one unsatisﬁable of
these queries per corresponding smtlib benchmark.

k-ind (41 benchmarks, 2,838 incremental queries). A set of quantiﬁer-free incre-
mental benchmarks over zero-initialized extensional constant arrays with ﬁxed-
size bit-vectors. This set was extracted from all queries with constant arrays
generated by the k-induction engine of the model checker Pono [21] on bench-
marks of the hardware model checking competitions (HWMCC) 2019–2025 [1,
2, 10, 11]. Similarly to Bitwuzla’s MBQI engine, this model-checking engine pro-
duces queries that equate array constants with array model values.

hevm (34 benchmarks). This set contains benchmarks generated by hevm [4,17],
a symbolic execution engine for the Ethereum virtual machine. Benchmarks in
this set are encoded over bit-vectors of size 256 in combination with uninter-
preted functions and zero-initialized extensional constant arrays.

crafted (410 benchmarks). In order to cover a wider range of the encoding ca-
pabilities (and corner cases) of ThAi with ﬁnite constant arrays, we created a set
of benchmarks as the instantiations of parameterizing formula

          hvihi1 ⊳ ei1 ih. . . ⊳ . . .ihin ⊳ ein i ≈ a1 hk1 ⊳ ek1 ih. . . ⊳ . . .ihks ⊳ eks i ≈ . . .
          . . . ≈ az hl1 ⊳ el1 ih. . . ⊳ . . .ihlt ⊳ elt i ≈ hwihj1 ⊳ ej1 ih. . . ⊳ . . .ihjm ⊳ ejm i

over the number of array constants z and the number of array updates n, m, s
and t. Indices {i1 , . . . , in , k1 , . . . , ks , l1 , . . . , lt , j1 , . . . , jm } and elements {ei1 , . . . ,
ein , ek1 , . . . , eks , el1 , . . . , elt , ej1 , . . . , ejm } are uninterpreted constants over ﬁnite sorts
(Bool, bit-vector, ﬂoating-point arithmetic, rounding mode). This benchmark
set is split into the two subsets crafted hAi and crafted ∀ (205 benchmarks each).
Set crafted hAi encodes constant arrays natively via (as const ...), and set
crafted ∀ encodes constant arrays with quantiﬁers via axiom roc. The quantiﬁed
encoding serves two purposes: (1) as a baseline to compare against the native
encoding, i.e., to show whether the native encoding has any advantages over
an axiomatization with quantiﬁers; and (2) if solvers disagree on the native
encoding, we can compare their answers to the results on the quantiﬁed encoding
to determine which solver gave a wrong answer.
      For each solver and benchmark pair, we allocated one CPU core and 8GB of
memory with a time limit of 1200 seconds. If a solver terminated with unknown,
an error or ran into the memory limit on a speciﬁc benchmark, we counted its
runtime on that benchmark as 1200 seconds as a penalty.
      Table 2 summarizes the results of each solver over all benchmark sets. Overall,
BitwuzlahAi signiﬁcantly outperforms all other solvers on each benchmark set.
      On the smtlib set, our new procedure signiﬁcantly improves the performance
of Bitwuzla’s MBQI engine on problems where MBQI subqueries involve reason-
ing over extensional constant arrays. Compared to the baseline version Bitwuzla,
the number of solved benchmarks increases by a factor of 5 (3,545 vs. 717). On
the 636 benchmarks commonly solved by BitwuzlahAi and Bitwuzla, we observe
a 27× speed-up in runtime (22 vs. 594.5 seconds).
      On the mbqi set, BitwuzlahAi solves all queries, including the ones that Bitwu-
zla was not able to solve due to extensional constant arrays. This observed per-
formance gain directly translates to the improved performance on the smtlib set,
since BitwuzlahAi is now able to eﬃciently solve the MBQI subqueries. On the
4,126 instances commonly solved by Z3 and BitwuzlahAi , BitwuzlahAi achieves a
140× speed-up in solving time over Z3 (37.8 vs. 5,279.6 seconds). Compared to
MathSAT5 , BitwuzlahAi achieves a 1.4× speed-up on the 4,034 commonly solved
instances (44.9 vs. 63.9 seconds).
      On benchmark set k-ind , we observe a similar performance improvement of
BitwuzlahAi over Bitwuzla, where BitwuzlahAi is able to solve all incremental
queries on which Bitwuzla struggled due to extensional constant arrays.
      On the hevm set, both Bitwuzla and BitwuzlahAi solve all benchmarks the
fastest. Note that these benchmarks only make use of non-extensional zero-
initialized constant arrays. Thus, Bitwuzla and BitwuzlahAi are expected to per-
form similarly. The diﬀerence in runtime is due to one benchmark where Bitwu-
zla’s abstraction-reﬁnement approach for bit-vector arithmetic [29] receives dif-
ferent bit-vector models, which helps BitwuzlahAi to converge faster.
Table 2. Number of solved/satisﬁable/unsatisﬁable/unsolved benchmarks/queries
(Solved,Sat,Unsat,Unsolved), and penalized runtime (T), grouped by benchmark set.
Number (x/y) indicates the total number of benchmarks x and satisﬁability queries y
in the set. Numbers marked with * include incorrect answers.

 Benchmarks      Solver        Solved       Sat       Unsat      Unsolved          T [s]
                 BitwuzlahAi    3,545      3,299        246          1,567   1,897,536.4
 smtlib          Z3               846        698        148          4,266   5,125,846.4
 (5,112/5,112)   Bitwuzla         717        700         17          4,395   5,274,616.8
                 cvc5             276        184         92          4,836   5,803,208.3
                 BitwuzlahAi    4,147      2,585       1,562             0          47.3
 mbqi            Z3             4,126      2,564       1,562            21      30,479.6
 (4,147/4,147)   MathSAT5       4,034      2,522       1,512           113     135,663.9
                 cvc5           2,972      2,103         869         1,175   1,410,552.5
                 Bitwuzla           4          4           0         4,143   4,971,600.0
                 BitwuzlahAi    2,838      2,173        665              0     19,368.6
 k-ind           Z3             2,142      1,644        498            696     47,133.4
 (41/2,838)      cvc5           1,230        945        285          1,608     48,651.5
                 MathSAT5         883        682        201          1,955     46,967.0
                 Bitwuzla         372         15        357          2,466     49,200.0
                 BitwuzlahAi         34          1          33          0            0.3
 hevm            Bitwuzla            34          1          33          0            2.6
 (34/34)         MathSAT5            34          1          33          0           53.2
                 cvc5                34          1          33          0           75.9
                 Z3                  32          0          32          2        2,400.7
                 BitwuzlahAi       172         100        72           33      46,752.1
                                 *         *            *
                 Z3                153         115        38           52      67,838.4
 crafted hAi                     *             *        *
 (205/205)       MathSAT5          107           13       94           98     119,363.6
                 cvc5                0            0        0          205     246,000.0
                 Bitwuzla            0            0        0          205     246,000.0
                 BitwuzlahAi         117        89          28         88     109,776.4
                 Bitwuzla            113        85          28         92     116,918.9
 crafted ∀
                 cvc5                 42        27          15        163     195,601.3
 (205/205)
                 Z3                   28        16          12        177     212,833.4




    On the crafted hAi set, BitwuzlahAi solves the highest number of benchmarks.
This benchmark set consists of benchmarks that encode equalities over ﬁnite
constant arrays with diﬀerent default values. Both cvc5 and baseline Bitwuzla do
not support this case and reject the input with an appropriate error message. Z3
and MathSAT5 , on the other hand, accept the input, but report wrong answers
for a signiﬁcant number of benchmarks. In contrast, we did not encounter any
disagreements between any of the solvers on the crafted ∀ set.
    We investigated all of the disagreements on the native encoding and com-
pared the solver results with the results of all solvers on the quantiﬁed encoding
in crafted ∀ . We found that Z3 reports sat (resp. unsat ) on 31 (19) benchmarks
that are known to be unsatisﬁable (resp. satisﬁable) by construction. Further,
on benchmarks commonly solved by Z3 between crafted hAi and crafted ∀ , it dis-
agrees with itself on 1 benchmark with unknown status and 5 benchmarks with
known status. MathSAT5 reports unsat on 29 benchmarks with unknown status
that are determined to be satisﬁable by BitwuzlahAi and Bitwuzla on the quan-
tiﬁed encoding. Further, 17 of these benchmarks are also solved by BitwuzlahAi
on the native encoding and determined to be satisﬁable.
    In an additional experiment, we investigated the models produced by Bitwu-
zlahAi , MathSAT5 , and Z3 on the crafted hAi set for correctness. That is, when
a solver reported sat, we asked the solver to produce a model, which was then
asserted back to the original formula. We ran all three solvers on all result-
ing benchmarks and found that the only solver that did not disagree with its
own models was BitwuzlahAi . Further, BitwuzlahAi rejected 3 (out of 12) Math-
SAT5 models and 69 (out of 84) Z3 models. These ﬁndings suggest that both
MathSAT5 and Z3 , while accepting the input, do not fully support equality
over constant arrays with ﬁnite index domains. We contacted the developers of
MathSAT5 and Z3 and provided the failing test cases.
    Finally, with the native encoding of constant arrays, BitwuzlahAi is able to
solve signiﬁcantly more benchmarks than with the quantiﬁer-based encoding
crafted ∀ . Overall, only 13 benchmarks that could be solved by at least one solver
with the quantiﬁer-based encoding could not be solved by BitwuzlahAi with the
native encoding. In contrast, BitwuzlahAi was able to solve 59 native benchmarks
that none of the solvers was able to solve with the quantiﬁed encoding. On closer
inspection of the behavior of BitwuzlahAi on native benchmarks that were hard
to solve, we found that the majority of the solving time is spent on ﬁnding an
index arrangement via distinctN . We leave improving the lazy expansion scheme
for distinctN to future work.


7   Conclusion
We have presented a new calculus CAEXT for the theory of extensional constant
arrays ThAi without imposing any limitations on the ﬁniteness of the array index
domain. We have shown the refutational and satisﬁability soundness of CAEXT.
We integrated a new decision procedure for ThAi based on CAEXT in the state-
of-the-art SMT solver Bitwuzla and evaluated its performance on a diverse set of
benchmarks. The new decision procedure enables Bitwuzla to solve problems it
was not able to handle before, and thus signiﬁcantly improves over its baseline.
    While the integration into Bitwuzla and its evaluation has focused on arrays
with ﬁnite index domains, our procedure is agnostic to the underlying solver
architecture and fully supports the inﬁnite domain case. As future work, we
plan to integrate a new array solver based on CAEXT in the SMT solver cvc5.

Acknowledgments. This work was supported in part by the Stanford Center for Au-
tomated Reasoning, the Stanford Center for Blockchain Research, Defense Advanced
Research Projects Agency (DARPA) contract FA875024-2-1001, and a gift from Ama-
zon Web Services.

Disclosure of Interests. The authors have no competing interests to declare that
are relevant to the content of this article.
Data Availability Statement. The artifact accompanying this paper is ar-
chived and available in the Zenodo repository at https://zenodo.org/records/19713260.

References
 1. Hardware Model Checking Competition 2019. https://fmv.jku.at/hwmcc19/
    (2019)
 2. Hardware Model Checking Competition 2020. https://hwmcc.github.io/2020/
    (2020)
 3. Bitwuzla on GitHub. https://github.com/bitwuzla/bitwuzla/ (2026)
 4. hevm       symbolic       execution      engine     SMT         queries      (2026),
    https://github.com/SMT-LIB/pending-benchmarks/commit/0a87f2c7581a3df7ad0f2d7b57621b6ecf4637ad
 5. Z3 on GitHub. https://github.com/Z3Prover/z3/ (2026)
 6. Baldoni, R., Coppa, E., D’Elia, D.C., Demetrescu, C., Finocchi, I.: A survey of
    symbolic execution techniques. ACM Comput. Surv. 51(3), 50:1–50:39 (2018).
    https://doi.org/10.1145/3182657
 7. Barbosa, H., Barrett, C.W., Brain, M., Kremer, G., Lachnitt, H., Mann, M., Mo-
    hamed, A., Mohamed, M., Niemetz, A., Nötzli, A., Ozdemir, A., Preiner, M.,
    Reynolds, A., Sheng, Y., Tinelli, C., Zohar, Y.: cvc5: A versatile and industrial-
    strength SMT solver. In: Fisman, D., Rosu, G. (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems - 28th International Conference, TACAS
    2022, Held as Part of the European Joint Conferences on Theory and Practice
    of Software, ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings, Part
    I. Lecture Notes in Computer Science, vol. 13243, pp. 415–442. Springer (2022).
    https://doi.org/10.1007/978-3-030-99524-9 24
 8. Barrett, C., Fontaine, P., Tinelli, C.: The SMT-LIB Standard: Version 2.7. Tech.
    rep., Department of Computer Science, The University of Iowa (2025), available
    at http://smt-lib.org
 9. Barrett, C.W., Dill, D.L., Stump, A.: Checking satisﬁability of ﬁrst-order formulas
    by incremental translation to SAT. In: Brinksma, E., Larsen, K.G. (eds.) Computer
    Aided Veriﬁcation, 14th International Conference, CAV 2002,Copenhagen, Den-
    mark, July 27-31, 2002, Proceedings. Lecture Notes in Computer Science, vol. 2404,
    pp. 236–249. Springer (2002). https://doi.org/10.1007/3-540-45657-0 18
10. Biere, A., Froleyks, N., Preiner, M.: Hardware model checking competition 2024.
    In: Narodytska, N., Rümmer, P. (eds.) Formal Methods in Computer-Aided Design,
    FMCAD 2024, Prague, Czech Republic, October 15-18, 2024. p. 1. IEEE (2024).
    https://doi.org/10.34727/2024/ISBN.978-3-85448-065-5 6
11. Biere, A., Froleyks, N., Preiner, M.: Hardware model checking competition
    2025. In: Irfan, A., Kaufmann, D. (eds.) Proceedings of the 25th Confer-
    ence on Formal Methods in Computer-Aided Design, FMCAD 2025, Menlo
    Park, CA, USA, October 6-10, 2025. TU Wien Academic Press (2025).
    https://doi.org/10.34727/2025/ISBN.978-3-85448-084-6 6
12. Brummayer, R., Biere, A.: Lemmas on demand for the extensional the-
    ory of arrays. J. Satisf. Boolean Model. Comput. 6(1-3), 165–201 (2009).
    https://doi.org/10.3233/SAT190067
13. Christ, J., Hoenicke, J., Nutz, A.: SMTInterpol: An interpolating SMT solver.
    In: Donaldson, A.F., Parker, D. (eds.) Model Checking Software - 19th Inter-
    national Workshop, SPIN 2012, Oxford, UK, July 23-24, 2012. Proceedings.
    Lecture Notes in Computer Science, vol. 7385, pp. 248–254. Springer (2012).
    https://doi.org/10.1007/978-3-642-31759-0 19
14. Cimatti, A., Griggio, A., Schaafsma, B.J., Sebastiani, R.: The mathsat5
    SMT solver. In: Piterman, N., Smolka, S.A. (eds.) Tools and Algorithms for
    the Construction and Analysis of Systems - 19th International Conference,
    TACAS 2013, Held as Part of the European Joint Conferences on Theory
    and Practice of Software, ETAPS 2013, Rome, Italy, March 16-24, 2013. Pro-
    ceedings. pp. 93–107. Lecture Notes in Computer Science, Springer (2013).
    https://doi.org/10.1007/978-3-642-36742-7 7
15. Clarke, E.M., Henzinger, T.A., Veith, H., Bloem, R. (eds.): Handbook of Model
    Checking. Springer (2018). https://doi.org/10.1007/978-3-319-10575-8, ISBN 978-
    3-319-10574-1
16. Dutertre, B.: Yices 2.2. In: Biere, A., Bloem, R. (eds.) Computer Aided Ver-
    iﬁcation - 26th International Conference, CAV 2014, Held as Part of the Vi-
    enna Summer of Logic, VSL 2014, Vienna, Austria, July 18-22, 2014. Pro-
    ceedings. pp. 737–744. Lecture Notes in Computer Science, Springer (2014).
    https://doi.org/10.1007/978-3-319-08867-9 49
17. Dxo, Soos, M., Paraskevopoulou, Z., Lundfall, M., Brockman, M.: Hevm, a fast
    symbolic execution framework for EVM bytecode. In: Gurﬁnkel, A., Ganesh,
    V. (eds.) Computer Aided Veriﬁcation - 36th International Conference, CAV
    2024, Montreal, QC, Canada, July 24-27, 2024, Proceedings, Part I. Lec-
    ture Notes in Computer Science, vol. 14681, pp. 453–465. Springer (2024).
    https://doi.org/10.1007/978-3-031-65627-9 22
18. Enderton, H.B.: A mathematical introduction to logic. Academic Press (1972),
    ISBN 978-0-12-238450-9
19. Ge, Y., de Moura, L.M.: Complete instantiation for quantiﬁed formulas in sat-
    isﬁabiliby modulo theories. In: Bouajjani, A., Maler, O. (eds.) Computer Aided
    Veriﬁcation, 21st International Conference, CAV 2009, Grenoble, France, June 26
    - July 2, 2009. Proceedings. Lecture Notes in Computer Science, vol. 5643, pp.
    306–320. Springer (2009). https://doi.org/10.1007/978-3-642-02658-4 25
20. Hoenicke, J., Schindler, T.: Solving and interpolating constant arrays based
    on weak equivalences. In: Enea, C., Piskac, R. (eds.) Veriﬁcation, Model
    Checking, and Abstract Interpretation - 20th International Conference, VM-
    CAI 2019, Cascais, Portugal, January 13-15, 2019, Proceedings. Lecture
    Notes in Computer Science, vol. 11388, pp. 297–317. Springer (2019).
    https://doi.org/10.1007/978-3-030-11245-5 14
21. Mann, M., Irfan, A., Lonsing, F., Yang, Y., Zhang, H., Brown, K., Gupta, A.,
    Barrett, C.W.: Pono: A ﬂexible and extensible smt-based model checker. In:
    Silva, A., Leino, K.R.M. (eds.) Computer Aided Veriﬁcation - 33rd International
    Conference, CAV 2021, Virtual Event, July 20-23, 2021, Proceedings, Part II.
    Lecture Notes in Computer Science, vol. 12760, pp. 461–474. Springer (2021).
    https://doi.org/10.1007/978-3-030-81688-9 22
22. Manzano, M.: Introduction to many-sorted logic. In: Many-sorted logic and its
    applications, pp. 3–86. John Wiley & Sons, Inc., New York, NY, USA (1993),
    https://dl.acm.org/doi/10.5555/165446.165450, ISBN 0-471-93485-2
23. McCarthy, J.: Towards a mathematical science of computation. In: Information
    Processing, Proceedings of the 2nd IFIP Congress 1962, Munich, Germany, August
    27 - September 1, 1962. pp. 21–28. North-Holland (1962)
24. Moura, L.D., Rueß, H.: Lemmas on demand for satisﬁability solvers. In: The 5th
    International Symposium on the Theory and Applications of Satisﬁability Testing,
    SAT 2002, Cincinnati, USA (2002), https://leodemoura.github.io/ﬁles/sat02.pdf
25. de Moura, L.M., Bjørner, N.S.: Z3: an eﬃcient SMT solver. In: Ramakrish-
    nan, C.R., Rehof, J. (eds.) Tools and Algorithms for the Construction and
    Analysis of Systems, 14th International Conference, TACAS 2008, Held as
    Part of the Joint European Conferences on Theory and Practice of Soft-
    ware, ETAPS 2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings.
    Lecture Notes in Computer Science, vol. 4963, pp. 337–340. Springer (2008).
    https://doi.org/10.1007/978-3-540-78800-3 24
26. de Moura, L.M., Bjørner, N.S.: Generalized, eﬃcient array decision procedures.
    In: Proceedings of 9th International Conference on Formal Methods in Computer-
    Aided Design, FMCAD 2009, 15-18 November 2009, Austin, Texas, USA. pp. 45–
    52. IEEE (2009). https://doi.org/10.1109/FMCAD.2009.5351142
27. Niemetz, A., Preiner, M.: Bitwuzla. In: Enea, C., Lal, A. (eds.) Computer Aided
    Veriﬁcation - 35th International Conference, CAV 2023, Paris, France, July 17-22,
    2023, Proceedings, Part II. Lecture Notes in Computer Science, vol. 13965, pp.
    3–17. Springer (2023). https://doi.org/10.1007/978-3-031-37703-7 1
28. Niemetz, A., Preiner, M., Wolf, C., Biere, A.: Btor2 , BtorMC and Boolec-
    tor 3.0. In: Chockler, H., Weissenbacher, G. (eds.) Computer Aided Veriﬁca-
    tion - 30th International Conference, CAV 2018, Held as Part of the Federated
    Logic Conference, FloC 2018, Oxford, UK, July 14-17, 2018, Proceedings, Part
    I. Lecture Notes in Computer Science, vol. 10981, pp. 587–595. Springer (2018).
    https://doi.org/10.1007/978-3-319-96145-3 32
29. Niemetz, A., Preiner, M., Zohar, Y.: Scalable bit-blasting with abstractions. In:
    Gurﬁnkel, A., Ganesh, V. (eds.) Computer Aided Veriﬁcation - 36th International
    Conference, CAV 2024, Montreal, QC, Canada, July 24-27, 2024, Proceedings, Part
    I. Lecture Notes in Computer Science, vol. 14681, pp. 178–200. Springer (2024).
    https://doi.org/10.1007/978-3-031-65627-9 9
30. Preiner, M.: Lambdas, Arrays and Quantiﬁers. Ph.D. thesis, Informatik, Johannes
    Kepler University Linz (2017), https://resolver.obvsg.at/urn:nbn:at:at-ubl:1-14897
31. Preiner, M., Niemetz, A., Biere, A.: Lemmas on demand for lambdas. In: Ganai,
    M.K., Sen, A. (eds.) Proceedings of the Second International Workshop on De-
    sign and Implementation of Formal Tools and Systems, Portland, OR, USA, Oc-
    tober 19, 2013. CEUR Workshop Proceedings, vol. 1130. CEUR-WS.org (2013),
    https://ceur-ws.org/Vol-1130/paper 7.pdf
32. Preiner, M., Schurr, H., Barrett, C.W., Fontaine, P., Niemetz, A.,
    Tinelli, C.: SMT-LIB release 2025 (incremental benchmarks) (May 2025).
    https://doi.org/10.5281/ZENODO.15493095
33. Preiner, M., Schurr, H., Barrett, C.W., Fontaine, P., Niemetz, A., Tinelli,
    C.: SMT-LIB release 2025 (non-incremental benchmarks) (Aug 2025).
    https://doi.org/10.5281/ZENODO.15493089
34. Stump, A., Barrett, C.W., Dill, D.L., Levitt, J.R.: A decision procedure for an ex-
    tensional theory of arrays. In: 16th Annual IEEE Symposium on Logic in Computer
    Science, Boston, Massachusetts, USA, June 16-19, 2001, Proceedings. pp. 29–37.
    IEEE Computer Society (2001). https://doi.org/10.1109/LICS.2001.932480
Appendix

In this appendix, we prove refutational and satisﬁability soundness of our base
calculus presented in Section 4.1, and its extension presented in Section 4.2.

   We start with several crucial lemmas that are needed to prove the main
theorems. First, we need the following deﬁnition, which assigns a speciﬁc numeric
value indicating the recursion depth necessary to calculate a reason R.

Deﬁnition 6.
                     
                     0
                                        if π(a, t) = ()
          |R(a, t)| = 1                  if t = a or t = a[i] for some i
                     
                     
                       1 + |R(c, t)|     otherwise, where π(a, t) = (r, c)

                                                                                    ⊓
                                                                                    ⊔
   The ﬁrst lemma states that once a reason R has been established, it does
not change unless a conﬂicting rule is applied and the conﬁguration is reset.

Lemma 1. Let D be a derivation ending in conﬁguration C, with C 6= unsat.
The following are true of R in C for all a and t: (i) if C is obtained by applying a
non-conﬂict rule to a conﬁguration C ′ , and R(a, t) 6= () in C ′ , then both R(a, t)
and |R(a, t)| remain unchanged from C ′ to C. (ii) R(a, t) is well deﬁned; (iii)
|R(a, t)| is ﬁnite; and (iv) R(a, t) = () iﬀ π(a, t) = ().

Proof. The proof is by induction over deductions. In an initial conﬁguration (i)
holds trivially, and R and π are always equal to (), so it is easy to see that the
properties hold.
     Now, suppose they hold for conﬁguration C ′ , and let C be obtained from C ′
by the application of a rule other than Conf . Suppose the rule is a conﬂict rule.
Then (i) holds trivially, and as above, R and π are always equal to (), so the
other three properties hold as well.
     Suppose the rule is not a conﬂict rule. We ﬁrst show (i) by considering, in
C ′ , the cases in the deﬁnition of R. Suppose π(a, t) = () in C ′ . By (iv), we also
have R(a, t) = () in C ′ , so the property holds trivially. Suppose t = a or t = a[i]
for some i, then R(a, t) = ⊤ and |R(a, t)| = 1 regardless of the conﬁguration.
Finally, assume we have (in C ′ ) R(a, t) = R(c, t) ∧ r, where (r, c) = π(a, t). And
suppose (i) does not hold. Then we can choose a and t such that R(a, t) 6= () in
C ′ , R(a, t) or |R(a, t)| changes value from C ′ to C, and |R(a, t)| is minimum in
C ′ (possible by property (iii)).
     But π(a, t) cannot have changed from C ′ to C, since all non-conﬂict rules only
modify π(a, t) if its value is (). So, we must also have in C that R(a, t) = R(c, t)∧
r, where (r, c) = π(a, t) and |R(a, t)| = |R(c, t)| + 1. Thus, if R(a, t) or |R(a, t)|
has changed, it must be because either R(c, t) or |R(c, t)| has also changed.
But by deﬁnition, |R(c, t)| = |R(a, t)| − 1, which contradicts the minimality
assumption.
     We now show (ii) and (iii). Suppose R(a, t) 6= () in C ′ . We know by the
induction hypothesis that R(a, t) is well deﬁned and |R(a, t)| is ﬁnite in C ′ . As
we just showed above, R(a, t) and |R(a, t)| remain unchanged in C, meaning that
R(a, t) is well deﬁned and |R(a, t)| is ﬁnite in C. On the other hand, suppose
R(a, t) = () in C ′ . By (iv), we have π(a, t) = () in C ′ as well. If π(a, t) = () still
in C, then it is clear that R(a, t) = () in C as well, and so it is well deﬁned,
and |R(a, t)| = 0. The last case is when π(a, t) = () in C ′ but π(a, t) 6= () in C.
This happens when the rule newly deﬁnes π(a, t). But whenever this happens,
we either have t = a or t = a[i] for some i, in which case R(a, t) is trivially well
deﬁned with |R(a, t)| = 1, or the rule newly deﬁnes π(a, t) to be some (r, a′ ),
where π(a′ , t) 6= () in C ′ . In the latter case, by (iv), R(a′ , t) 6= () in C ′ , so by
(i), R(a′ , t) and |R(a′ , t)| are unchanged from C ′ to C. And by (iii), |R(a′ , t)| is
ﬁnite in C ′ . But, by deﬁnition, R(a, t) = R(a′ , t) ∧ r, which is well deﬁned, and
similarly, |R(a, t)| = |R(a′ , t)| + 1, which is ﬁnite.
     Finally, we show (iv). The if direction follows directly by the deﬁnition
of R(a, t). For the only-if direction, consider the contrapositive. Suppose that
π(a, t) 6= (). Then by deﬁnition, either R(a, t) = ⊤ or R(a, t) = r1 ∧ r2 for some
r1 , r2 . We know that it is well deﬁned by (ii), so in either case, R(a, t) 6= (). ⊓    ⊔

   The next lemma provides the main invariant needed for soundness in the
base calculus AEXT.

Lemma 2. Let D be a derivation ending in conﬁguration C, with C 6= unsat.
The following is true in C for all a, b, i:

              If π(a, b[i]) 6= (), then TA |= R(a, b[i]) =⇒ a[i] ≈ b[i].

Proof. The proof is by induction on the length of a derivation. If C is the initial
conﬁguration, π is empty, so the statement holds vacuously.
    Now, suppose C is obtained by applying a rule to conﬁguration C ′ . We
consider each rule and show that it preserves the property.
    First, if the rule is a conﬂict rule, then π is empty in C, so again, the statement
holds vacuously.
    Second, if π(a, b[i]) 6= () in C ′ , then by Lemma 1, R(a, b[i]) has the same value
in C and C ′ , so, since the property holds in C ′ by the induction hypothesis, the
property must hold also in C.
    The remaining case to consider is when π(a, b[i]) is newly deﬁned by the rule.
We consider all such rules. First note that the InitR and InitW rules deﬁne π for
a pair of arguments of the form (a, a[i]). Since a[i] ≈ a[i] is always true, the
property clearly holds in C.
    Next, consider RowD. The newly deﬁned value of π(a, b[i]) is (i 6≈ j, ahj ⊳ ui).
We also know that π(ahj ⊳ ui, b[i]) 6= () in C ′ , so we also have TA |= R(ahj ⊳
ui, b[i]) =⇒ ahj ⊳ ui[i] ≈ b[i] in C ′ by the induction hypothesis. The same
holds also in C by Lemma 1. Now, by the deﬁnition of R, we have (in C)
R(a, b[i]) = R(ahj ⊳ ui, b[i]) ∧ i 6≈ j. And by the (row-ne) array axiom, we have
TA |= i 6≈ j =⇒ a[i] ≈ ahj ⊳ ui[i]. It follows that (in C) TA |= R(a, b[i]) =⇒
a[i] ≈ b[i].
    The RowU case is similar. Suppose a = a′ hj ⊳ ui. The newly deﬁned value
of π(a′ hj ⊳ ui, b[i]) is (i 6≈ j, a′ ). We also know that π(a′ , b[i]) 6= () in C ′ , so we
also have TA |= R(a′ , b[i]) =⇒ a′ [i] ≈ b[i] in C ′ by the induction hypothesis.
The same holds also in C by Lemma 1. Now, by the deﬁnition of R, we have
(in C) R(a′ hj ⊳ ui, b[i]) = R(a′ , b[i]) ∧ i 6≈ j. And by the (row-ne) array axiom,
we have TA |= i 6≈ j =⇒ a′ [i] ≈ a′ hj ⊳ ui[i]. It follows that (in C) TA |=
R(a′ hj ⊳ ui, b[i]) =⇒ a′ hj ⊳ ui[i] ≈ b[i].
    Consider now EqL. The newly deﬁned value of π(a, b[i]) in C is (a ≈ c, c). We
also know that π(c, b[i]) 6= () in C ′ , so we also have TA |= R(c, b[i]) =⇒ c[i] ≈
b[i] in C ′ by the induction hypothesis. The same holds also in C by Lemma 1.
Now, by the deﬁnition of R, we have (in C) R(a, b[i]) = R(c, b[i]) ∧ a ≈ c. And
by equality reasoning, we have TA |= a ≈ c =⇒ a[i] ≈ c[i]. It follows that
TA |= R(a, b[i]) =⇒ a[i] ≈ b[i]. The EqR case is analogous.
    These are the only rules that add a newly deﬁned value to π of the form
(a, b[i]).                                                                                 ⊓
                                                                                           ⊔

   Next, for our extended calculus CAEXT we need an additional deﬁnition and
a pair of lemmas similar to the AEXT case.

Deﬁnition 7.
               
               
               
                0                   if π(a, hvi) = ()
               
               1
               
                                    if a = hvi
  |I(a, hvi)| = 1 + |I(b, hvi)|      if π(a, hvi) = (⊤, b) with
               
               
               
               
                                          b = ahj ⊳ ui or a = bhj ⊳ ui for some u
               
               1 + |I(c, hvi)|      otherwise, where π(a, hvi) = (r, c)

                                                                                          ⊓
                                                                                          ⊔

Lemma 3. Let D be a derivation ending in conﬁguration C, with C 6= unsat.
The following are true of I in C for all a and t: (i) if C is obtained by applying
a non-conﬂict rule to a conﬁguration C ′ , and I(a, hvi) 6= () in C ′ , then both
I(a, hvi) and |I(a, hvi)| remain unchanged from C ′ to C. (ii) I(a, hvi) is well
deﬁned; (iii) |I(a, hvi)| is ﬁnite; and (iv) I(a, hvi) = () iﬀ π(a, hvi) = ().

Proof. The proof is by induction over deductions. In an initial conﬁguration (i)
holds trivially, and I and π are always equal to (), so it is easy to see that the
properties hold.
     Now, suppose they hold for conﬁguration C ′ , and let C be obtained from C ′
by the application of a rule other than Conf . Suppose the rule is a conﬂict rule.
Then (i) holds trivially, and as above, I and π are always equal to (), so the
other three properties hold as well.
     Suppose the rule is not a conﬂict rule. We ﬁrst show (i) by considering, in
C ′ , the cases in the deﬁnition of I. Suppose π(a, t) = () in C ′ . By (iv), we also
have I(a, hvi) = () in C ′ , so the property holds trivially. Suppose a = hvi; then,
I(a, hvi) = ∅ and |I(a, hvi)| = 1 regardless of the conﬁguration. Finally, assume
we have (in C ′ ) I(a, hvi) = I(b, hvi) ∪ {j} (for some b, j) or I(a, hvi) = I(c, hvi)
(for some c), and suppose (i) does not hold. Then we can choose a and v such
that I(a, hvi) 6= () in C ′ , I(a, hvi) or |I(a, hvi)| changes value from C ′ to C, and
|I(a, hvi)| is minimum in C ′ (possible by (iii)).
    But π(a, hvi) cannot have changed from C ′ to C, since all non-conﬂict rules
only modify π(a, hvi) if its value is (). So, if I(a, hvi) or |I(a, hvi)| has changed, it
must be because of a change in I(b, hvi) or |I(b, hvi)| (in the ﬁrst case) or because
of a change in I(c, hvi) or |I(c, hvi)|(in the second case). But by deﬁnition, we
have |I(b, hvi)| = |I(a, hvi)| − 1 or |I(c, hvi)| = |I(a, hvi)| − 1, which in either case
contradicts the minimality assumption.
    We now show (ii) and (iii). Suppose I(a, hvi) 6= () in C ′ . We know by the
induction hypothesis that I(a, hvi) is well deﬁned and |I(a, hvi)| is ﬁnite in C ′ . As
we just showed above, I(a, hvi) and |I(a, hvi)| remain unchanged in C, meaning
that I(a, hvi) is well deﬁned and |I(a, hvi)| is ﬁnite in C. On the other hand,
suppose I(a, hvi) = () in C ′ . By (iv), we have π(a, hvi) = () in C ′ as well. If
π(a, hvi) = () still in C, then it is clear that I(a, hvi) = () in C as well, and so it
is well deﬁned and |I(a, hvi)| = 0. The last case is when π(a, hvi) = () in C ′ but
π(a, hvi) 6= () in C. This happens when the rule newly deﬁnes π(a, hvi).
    Now, if a = hvi, then I(a, hvi) is trivially well deﬁned and |I(a, hvi)| = 1.
Otherwise, the rule newly deﬁnes π(a, hvi) to be some (r, b), where π(b, hvi) 6= ()
in C ′ . By (iv) and the induction hypothesis, I(b, hvi) 6= () in C ′ , so by (i),
I(b, hvi) and |I(b, hvi)| remain unchanged from C ′ to C. But now, by deﬁnition,
we either have I(a, hvi) = I(b, hvi) ∪ {j} for some j or I(a, hvi) = I(b, hvi), which
in either case is well deﬁned. Similarly, we have, in either case, |I(a, hvi)| =
1 + |I(b, hvi)|, which is ﬁnite.
    Finally, we show (iv). The if direction follows directly by the deﬁnition of
I(a, hvi). For the only-if direction, consider the contrapositive. Suppose that
π(a, hvi) 6= (). Then by deﬁnition, either I(a, hvi) = ∅, I(a, hvi) = I(b, hvi) ∪ {j}
for some b, j, or I(a, hvi) = I(c, hvi) for some c. In each case, we know that it is
well deﬁned by (ii), so in each case, I(a, hvi) 6= ().                                 ⊓
                                                                                       ⊔
Lemma 4. Let D be a derivation ending in conﬁguration C, with C 6= unsat.
The following is true in C for all a, v:
                                                       _
      If π(a, hvi) 6= (), then TA |= R(a, hvi) =⇒ ∀ i.   i ≈ k ∨ a[i] ≈ v.
                                                        k∈I(a,hvi)

Proof. The proof is by induction on the length of a derivation. If C is the initial
conﬁguration, π is empty, so the statement holds vacuously.
    Now, suppose C is obtained by applying a rule other than Conf to conﬁgu-
ration C ′ . We consider each rule and show that it preserves the property.
    First, if the rule is a conﬂict rule, then π is empty in C, so again, the statement
holds vacuously.
    Second, if π(a, hvi) 6= () in C ′ , then by Lemma 1 and Lemma 3, R(a, hvi)
and I(a, hvi) have the same value in C and C ′ , so, since the property holds in
C ′ by the induction hypothesis, the property must hold also in C.
    The remaining case to consider is when π(a, hvi) is newly deﬁned by the rule.
We consider all such rules.
     First note that the InitC rule deﬁnes π for a pair of arguments of the form
(hvi, hvi). Since TA |= hvi[i] ≈ v for every i, the property clearly holds in C.
     Next, consider CowD. The newly deﬁned value of π(a, hvi) is (⊤, ahj ⊳ ui). We
alsoWknow that π(ahj ⊳ ui, hvi) 6= () in C ′ , so we have TA |= R(ahj ⊳ ui, hvi) =⇒
∀ i. k∈I(ahj⊳ui,hvi) i ≈ k ∨ ahj ⊳ ui[i] ≈ v in C ′ by the induction hypothesis.
The same holds also in C by Lemmas 1 and 3. By the deﬁnition of R, we
have (in C) R(a, hvi) = R(ahj ⊳ ui, hvi) ∧ ⊤. And, by the deﬁnition of I, we
have (in C) I(a, hvi) = I(ahj ⊳ ui, hvi) ∪ {j}. Now, to show the property holds
in C, let WI be a TA -interpretation with I |= R(a, hvi). We must show that
I |= ∀ i. k∈I(a,hvi) i ≈ k ∨ a[i] ≈ v. To this end, let ι ∈ σ I be such that
ι 6= k I for every k ∈ I(a, hvi). We must show that aI (ι) = v I . First, note
that by the deﬁnition of R(a, hvi), we have     W I |= R(ahj ⊳ ui, hvi), so by the
induction hypothesis, we also have I |= ∀ i. k∈I(a,hvi) i ≈ k∨ahj⊳ui[i] ≈ v. Since
I(ahj ⊳ ui, hvi) is a subset of I(a, hvi), it must be the case that ahj ⊳ uiI (ι) = v I .
But we also know that j I 6= ι because j ∈ I(a, hvi), so by array axiom (row-ne),
we have aI (ι) = v I .
     The argument for CowU is similar, but we include it for completeness. Let
a = a′ hj ⊳ ui. The newly deﬁned value of π(a, hvi) is (⊤, a′ ). W       We also know
that π(a′ , hvi) 6= () in C ′ , so we have TA |= R(a′ , hvi) =⇒ ∀ i. k∈I(a′ ,hvi) i ≈
k ∨a′ [i] ≈ v in C ′ by the induction hypothesis. The same holds also in C by Lem-
mas 1 and 3. By the deﬁnition of R, we have (in C) R(a, hvi) = R(a′ , hvi) ∧ ⊤.
And, by the deﬁnition of I, we have (in C) I(a, hvi) = I(a′ , hvi) ∪ {j}. Now, to
show the property holds in C,     W let I be a TA -interpretation with I |= R(a, hvi).
We must show that I |= ∀ i. k∈I(a,hvi) i ≈ k ∨ a[i] ≈ v. To this end, let ι ∈ σ I
be such that ι 6= k I for every k ∈ I(a, hvi). We must show that aI (ι) = v I .
First, note that by the deﬁnition of R(a, hvi),Wwe have I |= R(a′ , hvi), so by the
induction hypothesis, we also have I |= ∀ i. k∈I(a′ ,hvi) i ≈ k ∨ a′ [i] ≈ v. Since
I(a′ , hvi) is a subset of I(a, hvi), it must be the case that (a′ )I (ι) = v I . But we
also know that j I 6= ι because j ∈ I(a, hvi), so by array axiom (row-ne), we have
aI (ι) = v I .
     Consider now CEqL. The newly deﬁned value of π(a, b[i]) in C is (a ≈ c, c).
We W also know that π(c, hvi) 6= () in C ′ , so we also have TA |= R(c, hvi) =⇒
∀ i. k∈I(c,hvi) i ≈ k ∨ c[i] ≈ v in C ′ by the induction hypothesis. The same
holds also in C by Lemmas 1 and 3. Now, by the deﬁnition of R, we have (in
C) R(a, hvi) = R(c, hvi) ∧ a ≈ c. And, by the deﬁnition of I, we have (in C)
I(a, hvi) = I(c, hvi). And by equality reasoning,Wwe have TA |= a ≈ c =⇒ a[i] ≈
c[i]. It follows that TA |= R(a, hvi) =⇒ ∀ i. k∈I(a,hvi) i ≈ k ∨ a[i] ≈ v The
CEqR case is analogous.
     These are the only rules that add a newly deﬁned value to π of the form
(a, hvi).                                                                              ⊓
                                                                                       ⊔

   Refutational soundness is stated by the following theorem.

Theorem 3 (Refutational Soundness). If a derivation starting with an ini-
tial conﬁguration hA, I, πi ends in unsat, then A is TA -unsatisﬁable.
Proof. We ﬁrst note that the only rule that derives unsat is the Conf rule, which
applies when A ∪ {ahi ⊳ ui[i] ≈ u | ahi ⊳ ui ∈ T (A)} is unsatisﬁable (in the empty
theory). Clearly, this implies that A ∪ {ahi ⊳ ui[i] ≈ u | ahi ⊳ ui ∈ T (A)} is
also TA -unsatisﬁable which is true iﬀ A is TA -unsatisﬁable, since {ahi ⊳ ui[i] ≈
u | ahi ⊳ ui ∈ T (A)} always holds in TA .
    It thus suﬃces to show that the remaining rules are satisﬁability preserving
with respect to TA , that is, A is TA -satisﬁable iﬀ A′ is TA -satisﬁable, where A
and A′ are the values of A before and after applying the rule, respectively. For
most rules, this is trivially true, as they do not modify A.
    Consider now rule CongR, which adds R(a, b[i])∧R(a, c[k])∧i ≈ k =⇒ b[i] ≈
c[k] to A. By Lemma 2, we know that TA |= R(a, b[i]) =⇒ a[i] ≈ b[i] and also
TA |= R(a, c[k]) =⇒ a[k] ≈ c[k]. It follows that TA |= R(a, b[i])∧R(a, c[k])∧i ≈
k =⇒ b[i] ≈ c[k]. Since the added formula is valid in TA , adding it to A does
not change its TA -satisﬁability.
    Next, consider rule DisEq, which adds the formula a 6≈ c =⇒ a[k{a,c} ] 6≈
c[k{a,c} ]. Call the result A′ . Clearly, if A′ is TA -satisﬁable, then so is A. In the
other direction, suppose A is TA -satisﬁable with interpretation I. If aI = cI ,
then A′ is also satisﬁed by I. Otherwise, if I |= a 6≈ c, then aI (ι) 6= cI (ι) for
some ι. We can then modify I to I ′ where I ′ is identical to I except that it
interprets ka,c as ι. I ′ then satisﬁes A′ .
    We next consider rule Roc, which adds R(hvi, b[i]) =⇒ b[i] ≈ v. By Lemma 2,
we know that TA |= R(hvi, b[i]) =⇒ hvi[i] ≈ b[i]. But by array axiom (roc), we
know that TA |= hvi[i] = v, so TA |= R(hvi, b[i]) =⇒ b[i] ≈ v. Since the added
formula is valid in TA , adding it to A does not change its TA -satisﬁability.
    Finally,
        V       consider rule CongC, which adds R(a, hvi) ∧ R(a, hwi) ∧
∃i : σ. k∈I(a,hvi)∪I(a,hwi) i 6≈ k =⇒ v ≈ w. By Lemma 4, we know that TA |=
                       W
R(a, hvi) =⇒ ∀ i. k∈I(a,hvi) i ≈ k ∨ a[i] ≈ v and also TA |= R(a, hwi) =⇒
    W
∀ i. k∈I(a,hwi) i ≈ k ∨ a[i] ≈ w. It follows that R(a, hvi) ∧ R(a, hwi) ∧ ∃i :
   V
σ. k∈I(a,hvi)∪I(a,hwi) i 6≈ k =⇒ v ≈ w. Since the added formula is valid in TA ,
adding it to A does not change its TA -satisﬁability.
    These are all of the rules that modify A.                                         ⊓
                                                                                      ⊔

   Refutational soundness ensures that the calculus never reports unsat unless
the initial set of constraints is unsatisﬁable. Satisﬁability soundness is the com-
plementary property: if the calculus does not report unsat, then the initial set of
constraints is satisﬁable.1 We need one more lemma.

Lemma 5. Let D be a derivation ending in conﬁguration C, with C 6= unsat.
The following is true in C for all a, t. If I =
                                              6 I0 and R(a, t) 6= (), then I |=
R(a, t).

Proof. The proof is by induction on the length of a derivation. If C is the initial
conﬁguration, I = I0 , so the statement holds vacuously.
1
    This is often referred to as completeness, but we ﬁnd the term satisﬁability soundness
    more precise in this context.
    Now, suppose C is obtained by applying a rule to conﬁguration C ′ . We
consider each rule and show that it preserves the property.
    First, if the rule is a conﬂict rule, then π is empty in C, so again, the statement
holds vacuously. The remaining case to consider is when π(a, t) is newly deﬁned
by the rule. We consider all such rules.
    First note that the InitR, InitW, and InitC rules deﬁne π for a pair of arguments
of the form (a, a[i]) or (a, a). Since R(a, t) = ⊤ in these cases, the property holds.
    For all other rules, if π(a, t) is newly set to (r, c) in C, we have R(a, t) =
R(c, t) ∧ r. By the induction hypothesis and Lemma 1, we have I |= R(c, t), so
we simply have to show I |= r. But in every such rule, either r = ⊤ or I |= r is
a premise.                                                                           ⊓
                                                                                     ⊔

Theorem 4 (Satisﬁability Soundness). If a derivation starting with an ini-
tial conﬁguration hA, I0 , π0 i ends in a conﬁguration other than unsat, and every
applicable rule is redundant, then A is TA -satisﬁable.

Proof. We ﬁrst note that because Conf does not apply, it must be the case that
A∪{ahi⊳ui[i] ≈ u | ahi⊳ui ∈ T (A)} is satisﬁable in the empty theory. Moreover,
because Interp does not apply, a speciﬁc satisfying interpretation I is already
stored in the ﬁnal conﬁguration.
    We will show that A is TA -satisﬁable by using I to construct a TA -interpretation
A that satisﬁes A. We start by deﬁning the domains of A as

                             Aσ = Iσ ,
                           Aτ = Iτ ,
                        A(σ→τ ) = { f | f : Aσ 7→ Aτ } .

    For this proof, it will be convenient to use the SMT-LIB function names for
array reads and writes. In the rest of the proof, we consider a[i] to be syntactic
sugar for select(a, i) and ahi ⊳ ui to be syntactic sugar for store(a, i, u). We
also introduce const(v) and consider hvi syntactic sugar for const(v). We deﬁne
these function symbols in A as follows:

selectA = λ α : A(σ→τ ) . λ ι : Aσ . α(ι) ,
 storeA = λ α : A(σ→τ ) . λ ι : Aσ . λ ǫ : Aτ . (λ κ : Aσ .if ι = κ then ǫ else α(κ)) .
 constA = λ ǫ : Aτ . (λ κ : Aσ .ǫ)

   For all variables v that are not of sort (σ → τ ), we keep their original inter-
pretations in I, i.e., we take v A = v I .
   Let ǫ be some element of Aτ . We interpret each array a : (σ → τ ) as the
corresponding function from I, but in a restricted manner.

              
                     I I I
              select (b , i )
                                     if π(a, b[i]) 6= () and iI = ι
 A
a = λ ι : Aσ . v I                    if π(a, hvi) 6= () and ι 6= k I for every k ∈ I(a, hvi)
              
              
                ǫ                     otherwise
Intuitively, we interpret the elements according to the corresponding interpre-
tations of the reads, we ensure that default elements match with any relevant
constant arrays, and we otherwise pick an arbitrary default element.
     We ﬁrst show that the interpretation is well-deﬁned. To show that the ﬁrst
case above is well deﬁned, suppose that for some variable a, we have both
π(a, b[i]) 6= () and π(a, c[k]) 6= () with iI = k I = ι, and suppose towards a
contradiction that selectI (bI , iI ) 6= selectI (cI , k I ), or, in other words, I |=
b[i] 6≈ c[k]. Then, the premises of rule CongR are satisﬁed, so in order for it to be
redundant, it must mean that R(a, b[i]) ∧ R(a, c[k]) ∧ i ≈ k =⇒ b[i] ≈ c[k] ∈ A.
Now, by Lemma 5, we know that I |= R(a, b[i]) and I |= R(a, c[k]). We also
know that I |= i ≈ k. But this means that we must have I |= b[i] ≈ c[k], which
contradicts our assumption.
    To show that the second case is well deﬁned, suppose that for some vari-
able a, we have both π(a, hvi) 6= () and π(a, hwi) 6= (), and suppose towards
a contradiction that for some element ι : σ, we have ι 6= k I for every k ∈
I(a, hvi) ∪ I(a, hwi) and wI 6= v I . Then, the premises of rule CongC are satisﬁed,
   in order for it to be redundant, it must mean that R(a, hvi) ∧ R(a, hwi) ∧ ∃i :
so V
σ. k∈I(a,hvi)∪I(a,hwi) i 6≈ k =⇒ v ≈ w ∈ A. Now, by Lemma 5, we know that
I |= R(a, hvi) and I |= R(a, hwi). But this means that we must have I |= v ≈ w,
which contradicts our assumption.
    We must also show that the ﬁrst and second cases don’t conﬂict. Suppose
towards a contradiction that for some ι : σ, we have both π(a, b[i]) 6= (), with iI =
ι and π(a, hvi) 6= () with ι 6= k I for every k ∈ I(a, hvi) and selectI (bI , iI ) 6= v I ,
or in other words, I |= b[i] 6≈ v. It is not hard to see that in this case, we must
also have π(hvi, b[i]) 6= (). Then, the premises of rule Roc are satisﬁed, so in order
for it to be redundant, it must mean that R(hvi, b[i]) =⇒ b[i] ≈ v ∈ A. Now,
by Lemma 5, we know that I |= R(hvi, b[i]) But this means that we must have
I |= b[i] ≈ v, which contradicts our assumption.
    It is easy to see that the deﬁnitions of select, store, and const satisfy the
axioms of TA . Now, we proceed to show that A |= A. First, note that by con-
struction, for a variable v not of sort (σ → τ ), we have v A = v I . Next, consider
a term of the form a[i] ∈ T (A). We know by the fact that rule InitR is redundant
that π(a, a[i]) 6= (). Then, by deﬁnition, aA (iA ) = selectI (aI , iI ). Then, by the
deﬁnition of selectA , it’s clear that selectA (aA , iA ) = selectI (aI , iI ). Since
a ﬂat term of a non-array sort can only be a variable or an array read, this shows
that if we have ﬂat terms s, t ∈ T (A) of a non-array sort, sA = sI and tA = tI .
Thus, all equalities s ≈ t and disequalities s 6≈ t between non-array terms must
have the same truth value in A as in I.
    Next, consider equalities and disequalities between variables of sort (σ → τ ).
For a disequality a 6≈ c ∈ A, we know by rule DisEq that a 6≈ c =⇒ a[k{a,c} ] 6≈
c[k{a,c} ] ∈ A. So, since I |= a 6≈ c, we also have I |= a[k{a,c} ] 6≈ c[k{a,c} ]. By
InitR, we have π(a, a[k{a,c} ]) 6= () and π(c, c[k{a,c} ]) 6= (), so by the deﬁnition of
aA and cA , it’s clear that aA (k{a,c}
                                    A
                                        ) = (a[k{a,c} ])I 6= (c[k{a,c} ])I = cA (k{a,c}
                                                                                  A
                                                                                        ).
              A    A
Therefore, a 6= c .
     To see that equalities a ≈ c are satisﬁed, let ι : σ and consider aA (ι). If
π(a, b[i]) 6= () for some b, i with iA = ι, then aA (ι) = selectI (bI , iI ). Now, we
know by the fact that rule EqR is redundant that we must also have π(c, b[i]) 6= ().
It follows then that also cA (ι) = selectI (bI , iI ).
     Suppose now that π(a, b[i]) = () for every b, i with iA = ι. Suppose further
that π(a, hvi) 6= () and ι 6= k I for every k ∈ I(a, hvi) so that aA (ι) = v I . We
know that rule CEqR is redundant, so we must have π(c, hvi) 6= (). If ι 6= k I
for every k ∈ I(c, hvi), then we also have cA (ι) = v I as required. However, if
ι = k I for some k ∈ I(c, hvi), then there must be a write to index k. And the
corresponding read introduced by InitW would have propagated to a contradict-
ing our assumption. A symmetric argument can be made starting with cA (ι).
In the ﬁnal case, where none of the above hold, we have aA (ι) = ǫ = cA (ι).
This concludes the case for equalities and disequalities between variables of sort
(σ → τ ).
     Next, consider an equality of the form c ≈ ahi⊳ui. Let ι : σ and consider cA (ι).
First, suppose ι = iA . We know that π(ahi⊳ui, ahi⊳ui[i]) 6= () by InitW. It follows
from EqL that π(c, ahi ⊳ ui[i]) 6= (). Thus, by deﬁnition, cA (ι) = (ahi ⊳ ui[i])I .
But we know by Interp that I |= ahi ⊳ ui[i] ≈ u, so cA = uI . And by deﬁnition of
selectA and storeA , we also have (ahi ⊳ ui[i])A = uA = uI .
     Otherwise, by the deﬁnition of store, and because iA 6= ι, we have (ahi ⊳
ui) (ι) = aA (ι). So, we must show that cA (ι) = aA (ι). If π(c, b[k]) 6= () for some
    A

b, k with k A = ι, then cA (ι) = selectI (bI , k I ). Now, we know by the fact that
rule EqR cannot be applied that we must also have π(ahi ⊳ ui, b[k]) 6= (). Then,
because iI = iA 6= k A = k I , we also have by RowD that π(a, b[k]) 6= (). So,
aA (ι) = selectI (bI , k I ).
     Next, suppose that π(c, b[k]) = () for every k I = ι but π(c, hvi) 6= () for some
v and ι 6= k I for every k ∈ I(c, hvi) so that cA (ι) = v I . Now, by CEqR, we know
that π(ahi ⊳ ui, hvi) 6= (). But if ι = k I for some k ∈ I(ahi ⊳ ui,), then there must
be a write to index k. And the corresponding read introduced by InitW would
have propagated to c contradicting our assumption. Thus, we must have ι 6= k I
for every k ∈ I(ahi ⊳ ui,). It follows that aA (ι) = v I . A symmetric argument can
be made with ahi ⊳ ui. In the ﬁnal case, where none of the above hold, we have
aA (ι) = ǫ = cA (ι).
     Finally, consider an equality of the form a ≈ hvi. We know by InitC that
π(hvi, hvi) 6= (). So, by CEqL, we also have π(a, hvi) 6= (). Consider aA (ι). We
know that hviA (ι) = v A = v I . If π(a, b[k]) 6= () for some b, k with k A = ι,
then aA (ι) = (b[k])I . But by EqR, we also then have π(hvi, b[k]) 6= (). Sup-
pose I |= b[k] 6= v. Then, the premises of rule Roc are satisﬁed, so we must have
R(hvi, b[k]) =⇒ b[k] ≈ v ∈ A. Now, by Lemma 5, we know that I |= R(hvi, b[k])
But this means that we must have I |= b[k] ≈ v, which contradicts our assump-
tion. Thus, (b[k])I = v I . On the other hand, suppose that π(a, b[k]) = () for every
k I = ι. Suppose further that π(a, hwi) 6= () and ι 6= k I for every k ∈ I(a, hwi)
so that aA (ι) = wI . We know from CEqR that π(hvi, hwi) 6= (). But then if
v I 6= wI , CongC would apply, so we must have v I = wI . A symmetric argument
starting with hvi shows that it must always be the case that aA (ι) = v I .          ⊓
                                                                                     ⊔
