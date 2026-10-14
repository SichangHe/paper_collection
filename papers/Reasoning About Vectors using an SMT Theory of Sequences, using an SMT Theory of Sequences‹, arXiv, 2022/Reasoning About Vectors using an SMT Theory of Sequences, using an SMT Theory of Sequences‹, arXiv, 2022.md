                                                                   Reasoning About Vectors
                                                              using an SMT Theory of Sequences‹

                                             Ying Sheng1 , Andres Nötzli1 , Andrew Reynolds2 , Yoni Zohar3 , David Dill4 ,
                                         Wolfgang Grieskamp4 , Junkil Park4 , Shaz Qadeer4 , Clark Barrett1 , and Cesare Tinelli2
                                                  1
                                                      Stanford University 2 The University of Iowa 3 Bar-Ilan University 4 Meta Novi
arXiv:2205.08095v2 [cs.LO] 21 May 2022




                                                  Abstract. Dynamic arrays, also referred to as vectors, are fundamental data
                                                  structures used in many programs. Modeling their semantics efficiently is crucial
                                                  when reasoning about such programs. The theory of arrays is widely supported
                                                  but is not ideal, because the number of elements is fixed (determined by its index
                                                  sort) and cannot be adjusted, which is a problem, given that the length of vectors
                                                  often plays an important role when reasoning about vector programs. In this paper,
                                                  we propose reasoning about vectors using a theory of sequences. We introduce
                                                  the theory, propose a basic calculus adapted from one for the theory of strings,
                                                  and extend it to efficiently handle common vector operations. We prove that our
                                                  calculus is sound and show how to construct a model when it terminates with a
                                                  saturated configuration. Finally, we describe an implementation of the calculus in
                                                  cvc5 and demonstrate its efficacy by evaluating it on verification conditions for
                                                  smart contracts and benchmarks derived from existing array benchmarks.


                                         1      Introduction
                                         Generic vectors are used in many programming languages. For example, in C++’s stan-
                                         dard library, they are provided by std::vector. Automated verification of software
                                         systems that manipulate vectors requires an efficient and automated way of reasoning
                                         about them. Desirable characteristics of any approach for reasoning about vectors in-
                                         clude: piq expressiveness—operations that are commonly performed on vectors should
                                         be supported; piiq generality—vectors are always “vectors of” some type (e.g., vectors of
                                         integers), and so it is desirable that vector reasoning be integrated within a more general
                                         framework; solvers for satisfiability modulo theories (SMT) provide such a framework
                                         and are widely used in verification tools (see [5] for a recent survey); piiiq efficiency—
                                         fast and efficient reasoning is essential for usability, especially as verification tools are
                                         increasingly used by non-experts and in continuous integration.
                                             Despite the ubiquity of vectors in software on the one hand and the effectiveness of
                                         SMT solvers for software verification on the other hand, there is not currently a clean
                                         way to represent vectors using operators from the SMT-LIB standard [3]. While the theory
                                         of arrays can be used, it is not a great fit because arrays have a fixed size determined
                                         by their index type. Representing a dynamic array thus requires additional modeling
                                         work. Moreover, to reach an acceptable level of expressivity, quantifiers are needed,
                                         which often makes the reasoning engine less efficient and robust. Indeed, part of the
                                          ‹
                                              This work was funded in part by the Stanford Center for Blockchain Research, NSF-BSF grant
                                              numbers 2110397 (NSF) and 2020704 (BSF), and Meta Novi. Part of the work was done when
                                              the first author was an intern at Meta Novi.
motivation for this work was frustration with array-based modeling in the Move Prover,
a verification framework for smart contracts [24] (see Section 6 for more information
about the Move Prover and its use of vectors). The current paper bridges this gap by
studying and implementing a native theory of sequences in the SMT framework, which
satisfies the desirable properties for vector reasoning listed above.
     We present two SMT-based calculi for determining satisfiability in the theory of
sequences. Since the decidability of even weaker theories is unknown (see, e.g., [9, 16]),
we do not aim for a decision procedure. Rather, we prove model and solution soundness
(that is, when our procedure terminates, the answer is correct). Our first calculus leverages
techniques for the theory of strings. We generalize these techniques, lifting rules specific
to string characters to more general rules for arbitrary element types. By itself, this base
calculus is already quite effective. However, it misses opportunities to perform high-level
vector-based reasoning. For example, both reading from and updating a vector are very
common operations in programming, and reasoning efficiently about the corresponding
sequence operators is thus crucial. Our second calculus addresses this gap by integrating
reasoning methods from array solvers (which handle reads and updates efficiently) into
the first procedure. Notice, however, that this integration is not trivial, as it must handle
novel combinations of operators (such as the combination of update and read operators
with concatenation) as well as out-of-bounds cases that do not occur with ordinary arrays.
We have implemented both variants of our calculus in the cvc5 SMT solver [2] and
evaluated them on benchmarks originating from the Move prover, as well as benchmarks
that were translated from SMT-LIB array benchmarks.
     As is typical, both of our calculi are agnostic to the sort of the elements in the
sequence. Reasoning about sequences of elements from a particular theory can then be
done via theory combination methods such as Nelson-Oppen [19] or polite combination
[17, 21]. The former can be done for stably infinite theories (and the theory of sequences
that we present here is stably infinite), while the latter requires investigating the politeness
of the theory, which we expect to do in future work.
     The rest of the paper is organized as follows. Section 2 includes basic notions from
first-order logic. Section 3 introduces the theory of sequences and shows how it can
be used to model vectors. Section 4 presents calculi for this theory and discusses their
correctness. Section 5 describes the implementation of these calculi in cvc5. Section 6
presents an evaluation comparing several variations of the sequence solver in cvc5 and
Z3. We conclude in Section 7 with directions for further research.
Related work: Our work crucially builds on a proposal by Bjørner et al. [8], but extends
it in several key ways. First, their implementation (for a logic they call QF_BVRE)
restricts the generality of the theory by allowing only bit-vector elements (representing
characters) and assuming that sequences are bounded. In contrast, our calculus maintains
full generality, allowing unbounded sequences and elements of arbitrary types. Second,
while our core calculus focuses only on a subset of the operators in [8], our implementa-
tion supports the remaining operators by reducing them to the core operators, and also
adds native support for the update operator, which is not included in [8].
     The base calculus that we present for sequences builds on similar work for the theory
of strings [6, 18]. We extend our base calculus to support array-like reasoning based on
the weak-equivalence approach [10]. Though there exists some prior work on extending


                                               2
the theory of arrays with more operators and reasoning about length [1, 13, 15], this
work does not include support for most of the of the sequence operators we consider
here.
    The SMT-solver Z3 [11] also provides a solver for sequences. However, its documen-
tation is limited [7], it does not support update directly, and its internal algorithms are
not described in the literature. Furthermore, as we show in Section 6, the performance of
the Z3 implementation is generally inferior to our implementation in cvc5.


2    Preliminaries
We assume the usual notions and terminology of many-sorted first-order logic with
equality (see, e.g., [14] for a complete presentation). We consider many-sorted signatures
Σ, each containing a set of sort symbols (including a Boolean sort Bool), a family of
logical symbols « for equality, with sort σˆσ Ñ Bool for all sorts σ in Σ and interpreted
as the identity relation, and a set of interpreted (and sorted) function symbols. We assume
the usual definitions of well-sorted terms, literals, and formulas as terms of sort Bool.
A literal is flat if it has the form K, ppx1 , . . . , xn q, ppx1 , . . . , xn q, x « y, x « y,
or x « f px1 , . . . , xn q, where p and f are function symbols and x, y, and x1 , . . . , xn
are variables. A Σ-interpretation M is defined as usual, satisfying MpKq “ false
and assigns: a set Mpσq to every sort σ of Σ, a function Mpf q : Mpσ1 q ˆ . . . ˆ
Mpσn q Ñ Mpσq to any function symbol f of Σ with arity σ1 ˆ . . . ˆ σn Ñ σ, and an
element Mpxq P Mpσq to any variable x of sort σ. The satisfaction relation between
interpretations and formulas is defined as usual and is denoted by |ù.
    A theory is a pair T “ pΣ, Iq, in which Σ is a signature and I is a class of Σ-
interpretations, closed under variable reassignment. The models of T are the inter-
pretations in I without any variable assignments. A Σ-formula ϕ is satisfiable (resp.,
unsatisfiable) in T if it is satisfied by some (resp., no) interpretation in I. Given a (set of)
terms S, we write T pSq to denote the set of all subterms of S. For a theory T “ pΣ, Iq,
a set S of Σ-formulas and a Σ-formula ϕ, we write S |ùT ϕ if every interpretation
M P I that satisfies S also satisfies ϕ. By convention and unless otherwise stated, we
use letters w, x, y, z to denote variables and s, t, u, v to denote terms.
    The theory TLIA “ pΣLIA , ITLIA q of linear integer arithmetic is based on the signature
ΣLIA that includes a single sort Int, all natural numbers as constant symbols, the unary
´ symbol, the binary ` symbol and the binary ď relation. When k P N, we use the
notation k ¨ x, inductively defined by 0 ¨ x “ 0 and pm ` 1q ¨ x “ x ` m ¨ x. In turn,
ITLIA consists of all structures M for ΣLIA in which the domain MpIntq of Int is the set
of integer numbers, for every constant symbol n P N, Mpnq “ n, and `, ´, and ď are
interpreted as usual. We use standard notation for integer intervals (e.g., ra, bs for the set
of integers i, where a ď i ď b and ra, bq for the set where a ď i ă b).


3    A Theory of Sequences
We define the theory TSeq of sequences. Its signature ΣSeq is given in Figure 1. It includes
the sorts Seq, Elem, Int, and Bool, intuitively denoting sequences, elements, integers, and
Booleans, respectively. The first four lines include symbols of ΣLIA . We write t1 ’ t2 ,


                                               3
      Symbol          Arity                      SMT-LIB            Description
      n               Int                        n                  All constants n P N
      `               Int ˆ Int Ñ Int            +                  Integer addition
      ´               Int Ñ Int                  -                  Unary Integer minus
      ď               Int ˆ Int Ñ Bool           <=                 Integer inequality
                     Seq                        seq.empty          The empty sequence
      unit            Elem Ñ Seq                 seq.unit           Sequence constructor
      ||              Seq Ñ Int                  seq.len            Sequence length
      nth             Seq ˆ Int Ñ Elem           seq.nth            Element access
      update          Seq ˆ Int ˆ Elem Ñ Seq     seq.update         Element update
      extract         Seq ˆ Int ˆ Int Ñ Seq      seq.extract        Extraction (subsequence)
        `` ¨ ¨ ¨ ``   Seq ˆ ¨ ¨ ¨ ˆ Seq Ñ Seq    seq.concat         Concatenation


                         Fig. 1: Signature for the theory of sequences.


with ’ P tą, ă, ďu, as syntactic sugar for the equivalent literal expressed using ď (and
possibly ). The sequence symbols are given on the remaining lines. Their arities are
also given in Figure 1. Notice that `` ¨ ¨ ¨ `` is a variadic function symbol.
    Interpretations M of TSeq interpret: Int as the set of integers; Elem as some set; Seq
as the set of finite sequences whose elements are from Elem;  as the empty sequence;
unit as a function that takes an element from MpElemq and returns the sequence that
contains only that element; nth as a function that takes an element s from MpSeqq and
an integer i and returns the ith element of s, in case i is non-negative and is smaller than
the length of s (we take the first element of a sequence to have index 0). Otherwise, the
function has no restrictions; update as a function that takes an element s from MpSeqq,
an integer i, and an element a from MpElemq and returns the sequence obtained from s
by replacing its ith element by a, in case i is non-negative and smaller than the length of
s. Otherwise, the returned value is s itself; extract as a function that takes a sequence
s and integers i and j, and returns the maximal sub-sequence of s that starts at index i
and has length at most j, in case both i and j are non-negative and i is smaller than the
length of s. Otherwise, the returned value is the empty sequence;1 | | as a function that
takes a sequence and returns its length; and `` ¨ ¨ ¨ `` as a function that takes some
number of sequences (at least 2) and returns their concatenation.
    Notice that the interpretations of Elem and nth are not completely fixed by the theory:
Elem can be set arbitrarily, and nth is only defined by the theory for some values of its
second argument. For the rest, it can be set arbitrarily.

3.1       Vectors as Sequences
We show the applicability of TSeq by using it for a simple verification task. Consider
the C++ function swap at the top of Figure 2. This function swaps two elements in a
 1
     In [8], the second argument j denotes the end index, while here it denotes the length of the
     sub-sequence, in order to be consistent with the theory of strings in the SMT-LIB standard.


                                                4
vector. The comments above the function include a partial specification for it: if both
indexes are in-bounds and the indexed elements are equal, then the function should not
change the vector (this is expressed by s_out==s). We now consider how to encode the
verification condition induced by the code and the specification. The function variables
a, b, i, and j can be encoded as variables of sort Int with the same names. We include
two copies of s: s for its value at the beginning, and sout for its value at the end. But
what should be the sorts of s and sout ? In Figure 2 we consider two options: one is based
on arrays and the other on sequences.
Example 1 (Arrays). The theory of arrays includes three sorts: index, element (in this
case, both are Int), and an array sort Arr, as well as two operators: xris, interpreted as
the ith element of x; and xri Ð as, interpreted as the array obtained from x by setting
the element at index i to a. We declare s and sout as variables of an uninterpreted sort V
and declare two functions ` and c, which, given v of sort V , return its length (of sort Int)
and content (of sort Arr), respectively.2
    Next, we introduce functions to model vector operations: «A for comparing vectors,
nthA for reading from them, and updateA for updating them. These functions need
to be axiomatized. We include two axioms (bottom of Figure 2): Ax1 states that two
vectors are equal iff they have the same length and the same contents. Ax2 axiomatizes
the update operator; the result has the same length, and if the updated index is in bounds,
then the corresponding element is updated. These axioms are not meant to be complete,
but are rather just strong enough for the example.
    The first two lines of the swap function are encoded as equalities using nthA ,
and the last two lines are combined into one nested constraint that involves updateA .
The precondition of the specification is naturally modeled using nthA , and the post-
condition is negated, so that the unsatisfiability of the formula entails the correctness
of the function w.r.t. the specification. Indeed, the conjunction of all formulas in this
encoding is unsatisfiable in the combined theories of arrays, integers, and uninterpreted
functions.
     The above encoding has two main shortcomings: It introduces auxiliary symbols, and
it uses quantifiers, thus reducing clarity and efficiency. In the next example, we see how
using the theory of sequences allows for a much more natural and succinct encoding.
Example 2 (Sequences). In the sequences encoding, s and sout have sort Seq. No
auxiliary sorts or functions are needed, as the theory symbols can be used directly.
Further, these symbols do not need to be axiomatized as their semantics is fixed by the
theory. The resulting formula, much shorter than in Example 2 and with no quantifiers,
is unsatisfiable in TSeq .


4      Calculi
After introducing some definitions and assumptions, we describe a basic calculus for the
theory of sequences, which adapts techniques from previous procedures for the theory
 2
     It is possible to obtain a similar encoding using the theory of datatypes; however, here we use
     uninterpreted functions which are simpler and better supported by SMT solvers.


                                                  5
/ / @pre : 0 <= i , j < s . s i z e ( ) and s [ i ] == s [ j ]
/ / @post : s o u t == s
v o i d swap ( s t d : : v e c t o r <i n t>& s , i n t i , i n t j ) {
    int a = s [ i ];
    int b = s [ j ];
    s[ i ] = b;
    s[j] = a;
}

                            Sequences                                     Arrays
 Problem Variables          a, b, i, j : Int     s, sout : Seq            a, b, i, j : Int   s, sout : V
 Auxiliary Variables                                                      ` : V Ñ Int     c : V Ñ Arr
                                                                          «A : V ˆ V Ñ Bool
                                                                          nthA : V ˆ Int Ñ Int
                                                                          updateA : V ˆ Int ˆ Int Ñ V
 Axioms                                                                   Ax1 ^ Ax2
 Program                    a « nthps, iq ^ b « nthps, jq                 a « nthA ps, iq ^ b « nthA ps, jq
                            sout « updatepupdateps, i, bq, j, aq          sout «A updateA pupdateA ps, i, bq, j, aq
 Spec.                      0 ď i, j ă |s| ^ nthps, iq « nthps, jq        0 ď i, j ă `psq ^ nthA ps, iq « nthA ps, jq
                               sout « s                                     sout «A s

                Ax1 :“ @x, y.x «A y Ø p`pxq « `pyq ^ @ 0 ď i ă `pxq.cpxqris « cpyqrisq
 Ax2 :“ @x, y, i, a.y «A updateA px, i, aq Ñ p`pxq « `pyq ^ p0 ď i ă `pxq Ñ cpyq « cpxqri Ð asqq

                                         Fig. 2: An example using TSeq .


of strings. In particular, the basic calculus reduces the operators nth and update by
introducing concatenation terms. We then show how to extend the basic calculus by
introducing additional rules inspired by solvers for the theory of arrays; the modified
calculus can often reason about nth and update terms directly, avoiding the introduction
of concatenation terms (which are typically expensive to reason about).
    Given a vector of sequence terms t “ pt1 , . . . , tn q, we use t to denote the term
corresponding to the concatenation of t1 , . . . , tn . If n “ 0, t denotes , and if n “ 1, t
denotes t1 ; otherwise (when n ą 1), t denotes a concatenation term having n children.
In our calculi, we distinguish between sequence and arithmetic constraints.

Definition 1. A ΣSeq -formula ϕ is a sequence constraint if it has the form s « t or
s ff t; it is an arithmetic constraint if it has the form s « t, s ě t, s ff t, or s ă t where
s, t are terms of sort Int, or if it is a disjunction c1 _ c2 of two arithmetic constraints.

Notice that sequence constraints do not have to contain sequence terms (e.g., x « y
where x, y are Elem-variables). Also, equalities and disequalities between terms of sort
Int are both sequence and arithmetic constraints. In this paper we focus on sequence
constraints and arithmetic constraints. This is justified by the following lemma. (Proofs
of this lemma and later results can be found in the appendix.)

Lemma 1. For every quantifier-free ΣSeq -formula ϕ, there are sets S1 , . . . , Sn of se-
quence constraints and sets A1 , . . . , An of arithmetic constraints such that ϕ is TSeq -
satisfiable iff Si Y Ai is TSeq -satisfiable for some i P r1, ns.


                                                              6
|| Ñ 0                       |unitptq| Ñ 1
|updateps, i, tq| Ñ |s|       |s1 `` ¨ ¨ ¨ `` sn | Ñ |s1 | ` ¨ ¨ ¨ ` |sn |

u ``  `` v Ñ u `` v          u `` ps1 `` ¨ ¨ ¨ `` sn q `` v Ñ u `` s1 `` ¨ ¨ ¨ `` sn `` v
Fig. 3: Rewrite rules for the reduced form tÓ of a term t, obtained from t by applying
these rules to completion.


Throughout the presentation of the calculi, we will make a few simplifying assumptions.

Assumption 1. Whenever we refer to a set S of sequence constraints, we assume:
 1. for every non-variable term t P T pSq, there exists a variable x such that x « t P S;
 2. for every Seq-variable x, there exists a variable `x such that `x « |x| P S;
 3. all literals in S are flat.
Whenever we refer to a set of arithmetic constraints, we assume all its literals are flat.

    These assumptions are without loss of generality as any set can easily be transformed
into an equisatisfiable set satisfying the assumptions by the addition of fresh variables
and equalities. Note that some rules below introduce non-flat literals. In such cases, we
assume that similar transformations are done immediately after applying the rule to
maintain the invariant that all literals in S Y A are flat. Rules may also introduce fresh
variables k of sort Seq. We further assume that in such cases, a corresponding constraint
`k « |k| is added to S with a fresh variable `k .

Definition 2. Let C be a set of constraints. We write C |ù ϕ to denote that C entails
formula ϕ in the empty theory, and write ”C to denote the binary relation over T pCq
such that s ”C t iff C |ù s « t.

Lemma 2. For all set S of sequence constraints, ”S is an equivalence relation; further-
more, every equivalence class of ”S contains at least one variable.

We denote the equivalence class of a term s according to ”S by rss”S and drop the ”S
subscript when it is clear from the context.
    In the presentation of the calculus, it will often be useful to normalize terms to what
will be called a reduced form.

Definition 3. Let t be a ΣSeq -term. The reduced form of t, denoted by tÓ, is the term
obtained by applying the rewrite rules listed in Figure 3 to completion.

Observe that tÓ is well defined because the given rewrite rules form a terminating rewrite
system. This can be seen by noting that each rule reduces the number of applications of
sequence operators in the left-hand side term or keeps that number the same but reduces
the size of the term. It is not difficult to show that |ùTSeq t « tÓ.
    We now introduce some basic definitions related to concatenation terms.

Definition 4. A concatenation term is a term of the form s1 `` ¨ ¨ ¨ `` sn with n ě 2.
If each si is a variable, it is a variable concatenation term. For a set S of sequence
constraints, a variable concatenation term x1 `` ¨ ¨ ¨ `` xn is singular in S if S * xi « 


                                               7
for at most one variable xi with i P r1, ns. A sequence variable x is atomic in S if
S * x «  and for all variable concatenation terms s P T pSq such that S |ù x « s, s is
singular in S.

We lift the concept of atomic variables to atomic representatives of equivalence classes.

Definition 5. Let S be a set of sequence constraints. Assume a choice function α :
T pSq{”S Ñ T pSq that chooses a variable from each equivalence class of ”S . A
sequence variable x is an atomic representative in S if it is atomic in S and x “ αprxs”S q.

Finally, we introduce a relation that is the foundation for reasoning about concatenations.

Definition 6. Let S be a set of sequence constraints. We inductively define a relation
S |ù`` x « s, where x is a sequence variable in S and s is a sequence term whose
variables are in T pSq, as follows:
 1. S |ù`` x « x for all sequence variables x P T pSq.
 2. S |ù`` x « t for all sequence variables x P T pSq and variable concatenation terms
     t, where x « t P S.
 3. If S |ù`` x « pw `` y `` zqÓ and S |ù y « t and t is  or a variable concatena-
     tion term in S that is not singular in S, then S |ù`` x « pw `` t `` zqÓ.
Let α be a choice function for S as defined in Definition 5. We additionally define the
entailment relation S |ù˚`` x « y, where y is of length n ě 0, to hold if each element of
y is an atomic representative in S and there exists z of length n such that S |ù`` x « z
and S |ù yi « zi for i P r1, ns.

In other words, S |ù˚`` x « t holds when t is a concatenation of atomic representatives
and is entailed to be equal to x by S. In practice, t is determined by recursively expanding
concatenations using equalities in S until a fixpoint is reached.

Example 3. Suppose S “ tx « y `` z, y « w `` u, u « vu (we omit the additional
constraints required by Assumption 1, part 2 for brevity). It is easy to see that u, v,
w, and z are atomic in S, but x and y are not. Furthermore, w and z (and one of u or
v) must also be atomic representatives. Clearly, S |ù`` x « x and S |ù x « y `` z.
Moreover, y `` z is a variable concatenation term that is not singular in S. Hence, we
have S |ù`` x « py `` zqÓ, and so S |ù`` x « y `` z (by using either Item 2 or
Item 3 of Definition 6, as in fact x « y `` z P S. ). Now, since S |ù`` x « y `` z,
S |ù y « w `` u, and w `` u is a variable concatenation term not singular in S, we get
that S |ù`` x « ppw `` uq `` zqÓ, and so S |ù`` x « w `` u `` z. Now, assume that
v “ αprvs”S q “ αptv, uuq. Then, S |ù˚`` x « w `` v `` z.

Our calculi can be understood as modeling abstractly a cooperation between an arithmetic
subsolver and a sequence subsolver. Many of the derivation rules lift those in the string
calculus of Liang et al. [18] to sequences of elements of an arbitrary type. We describe
them similarly as rules that modify configurations.

Definition 7. A configuration is either the distinguished configuration unsat or a pair
pS, Aq of a set S of sequence constraints and a set A of arithmetic constraints.


                                             8
The rules are given in guarded assignment form, where the rule premises describe the
conditions on the current configuration under which the rule can be applied, and the
conclusion is either unsat, or otherwise describes the resulting modifications to the
configuration. A rule may have multiple conclusions separated by k. In the rules, some
of the premises have the form S |ù s « t (see Definition 2). Such entailments can be
checked with standard algorithms for congruence closure. Similarly, premises of the
form S |ùLIA s « t can be checked by solvers for linear integer arithmetic.
     An application of a rule is redundant if it has a conclusion where each component
in the derived configuration is a subset of the corresponding component in the premise
configuration. We assume that for rules that introduce fresh variables, the introduced
variables are identical whenever the premises triggering the rule are the same (i.e., we
cannot generate an infinite sequence of rule applications by continuously using the same
premises to introduce fresh variables).3 A configuration other than unsat is saturated
with respect to a set R of derivation rules if every possible application of a rule in R
to it is redundant. A derivation tree is a tree where each node is a configuration whose
children, if any, are obtained by a non-redundant application of a rule of the calculus.
A derivation tree is closed if all of its leaves are unsat. As we show later, a closed
derivation tree with root node pS, Aq is a proof that A Y S is unsatisfiable in TSeq . In
contrast, a derivation tree with root node pS, Aq and a saturated leaf with respect to all
the rules of the calculus is a witness that A Y S is satisfiable in TSeq .

4.1     Basic Calculus
Definition 8. The calculus BASE consists of the derivation rules in Figures 4 and 5.
     Some of the rules are adapted from previous work on string solvers [18, 23]. Com-
pared to that work, our presentation of the rules is noticeably simpler, due to our use of
the relation |ù˚`` from Definition 6. In particular, our configurations consist only of pairs
of sets of formulas, without any auxiliary data-structures.
     Note that judgments of the form S |ù˚`` x « t are used in premises of the calculus.
It is possible to compute whether such a premise holds thanks to the following lemma.
Lemma 3. Let S be a set of sequence constraints and A a set of arithmetic constraints. If
pS, Aq is saturated w.r.t. S-Prop, L-Intro and L-Valid, the problem of determining whether
S |ù˚`` x « s for given x and s is decidable.
Lemma 3 assumes saturation with respect to certain rules. Accordingly, our proof
strategy, described in Section 5, will ensure such saturation before attempting to apply
rules relying on |ù˚`` . The relation |ù˚`` induces a normal form for each equivalence
class of ”S .
Lemma 4. Let S be a set of sequence constraints and A a set of arithmetic constraints.
Suppose pS, Aq is saturated w.r.t. A-Conf, S-Prop, L-Intro, L-Valid, and C-Split. Then, for
every equivalence class e of ”S whose terms are of sort Seq, there exists a unique
(possibly empty) s such that whenever S |ù˚`` x « s1 for x P e, then s1 “ s. In this case,
we call s the normal form of e (and of x).
 3
     In practice, this is implemented by associating each introduced variable with a witness term as
     described in [22].


                                                  9
                                  A |ùLIA K                    A |ùLIA s « t          s, t P T pSq
                        A-Conf                      A-Prop
                                    unsat                               S :“ S, s « t

                        S |ù K                  S |ù s « t          s, t P T pSq       s, t are ΣLIA -terms
             S-Conf                   S-Prop
                        unsat                                         A :“ A, s « t

                                            x, y P T pSq X T pAq         x, y : Int
                                    S-A
                                          A :“ A, x « y        k     A :“ A, x ff y

                        s P T pSq         s : Seq                       x P T pSq         x : Seq
              L-Intro                                L-Valid
                         S :“ S, |s| « p|s|qÓ                  S :“ S, x «        k     A :“ A, `x ą 0

                         S |ù unitpxq « unitpyq                    S |ù˚
                                                                       `` x « z         S |ù˚
                                                                                            `` y « z
                  U-Eq                                  C-Eq
                                S :“ S, x « y                              S :“ S, x « y

                          S |ù˚
                              `` x « pw `` y `` zqÓ                  S |ù˚             1    1
                                                                         `` x « pw `` y `` z qÓ
                C-Split
                                    A :“ A, `y ą `y1   S :“ S, y « y 1 `` k                k
                                    A :“ A, `y ă `y1   S :“ S, y 1 « y `` k                k
                                         A :“ A, `y « `y1    S :“ S, y « y 1

                                                    x ff y P S        x, y : Seq
        Deq-Ext
                                              A :“ A, `x ff `y k
                  A :“ A, `x « `y , 0 ď i ă `x S :“ S, w1 « nthpx, iq, w2 « nthpy, iq, w1 ff w2

Fig. 4: Core derivation rules. The rules use k and i to denote fresh variables of sequence
and integer sort, respectively, and w1 and w2 for fresh element variables.



    We now turn to the description of the rules in Figure 4, which form the core of the
calculus. For greater clarity, some of the conclusions of the rules include terms before
they are flattened. First, either subsolver can report that the current set of constraints is
unsatisfiable by using the rules A-Conf or S-Conf. For the former, the entailment |ùLIA
(which abbreviates |ùTLIA ) can be checked by a standard procedure for linear integer
arithmetic, and the latter corresponds to a situation where congruence closure detects
a conflict between an equality and a disequality. The rules A-Prop, S-Prop, and S-A
correspond to a form of Nelson-Oppen-style theory combination between the two sub-
solvers. The first two communicate equalities between the sub-solvers, while the third
guesses arrangements for shared variables of sort Int. L-Intro ensures that the length
term |s| for each sequence term s is equal to its reduced form p|s|qÓ. L-Valid restricts
sequence lengths to be non-negative, splitting on whether each sequence is empty or
has a length greater than 0. The unit operator is injective, which is captured by U-Eq.
C-Eq concludes that two sequence terms are equal if they have the same normal form. If
two sequence variables have different normal forms, then C-Split takes the first differing
components y and y 1 from the two normal forms and splits on their length relationship.
Note that C-Split is the source for non-termination of the calculus (see, e.g., [18, 23]).
Finally, Deq-Ext handles disequalities between sequences x and y by either asserting
that their lengths are different or by choosing an index i at which they differ.
    Figure 5 includes a set of reduction rules for handling operators that are not directly
handled by the core rules. These reduction rules capture the semantics of these operators
by reduction to concatenation. R-Extract splits into two cases: Either the extraction uses


                                                         10
                                             x « extractpy, i, jq P S
                 R-Extract
                             A :“ A, i ă 0 _ i ě `y _ j ď 0        S :“ S, x «  k
                              A :“ A, 0 ď i ă `y , j ą 0, `k « i, `x « minpj, `y ´ iq
                                            S :“ S, y « k `` x `` k1
                                               x « nthpy, iq P S
                R-Nth
                                       A :“ A, i ă 0 _ i ě `y k
                        A :“ A, 0 ď i ă `y , `k « i  S :“ S, y « k `` unitpxq `` k1

                                              x « updatepy, i, zq P S
                   R-Update
                                 A :“ A, i ă 0 _ i ě `y       S :“ S, x « y k
                                        A :“ A, 0 ď i ă `y , `k « i, `k1 « 1
                               S :“ S, y « k `` k1 `` k2 , x « k `` unitpzq `` k2

Fig. 5: Reduction rules for extract, nth, and update. The rules use k, k 1 , and k 2 to denote
fresh sequence variables. We write s « minpt, uq as an abbreviation for s « t _ s «
u, s ď t, s ď u.


an out-of-bounds index or a non-positive length, in which case the result is the empty
sequence, or the original sequence can be described as a concatenation that includes
the extracted sub-sequence. R-Nth creates an equation between y and a concatenation
term with unitpxq as one of its components, as long as i is not out of bounds. R-Update
considers two cases. If i is out of bounds, then the update term is equal to y. Otherwise,
y is equal to a concatenation, with the middle component (k 1 ) representing the part of y
that is updated. In the update term, k 1 is replaced by unitpzq.

Example 4. Consider a configuration pS, Aq, where S contains the formulas x « y `` z,
z « v `` x `` w, and v « unitpuq, and A is empty. Hence, S |ù |x| « |y `` z|.
By L-Intro, we have S |ù |y `` z| « |y| ` |z|. Together with Assumption 1, we have
S |ù `x « `y ` `z , and then with S-Prop, we have `x « `y ` `z P A. Similarly, we can
derive `z « `v ` `x ` `w , `v « 1 P S, and so p˚q A |ùLIA `z « 1 ` `y ` `z ` `w . Notice
that for any variable k of sort Seq, we can apply L-Valid, L-Intro, and S-Prop to add to A
either `k ą 0 or `k “ 0. Applying this to y, z, w, we have that A |ùLIA K in each branch
thanks to p˚q, and so A-Conf applies and we get unsat.


4.2   Extended Calculus

Definition 9. The calculus EXT is comprised of the derivation rules in Figures 4 and 6,
with the addition of rule R-Extract from Figure 5.

    Our extended calculus combines array reasoning, based on [10] and expressed by the
rules in Figure 6, with the core rules of Figure 4 and the R-Extract rule. Unlike in BASE,
those rules do not reduce nth and update. Instead, they reason about those operators
directly and handle their combination with concatenation. Nth-Concat identifies the ith
element of sequence y with the corresponding element selected from its normal form (see
Lemma 4). Update-Concat operates similarly, applying update to all the components.


                                                  11
Update-Concat-Inv operates similarly on the updated sequence rather than on the original
sequence. Nth-Unit captures the semantics of nth when applied to a unit term. Update-
Unit is similar and distinguishes an update on an out-of-bounds index (different from 0)
from an update within the bound. Nth-Intro is meant to ensure that Nth-Update (explained
below) and Nth-Unit (explained above) are applicable whenever an update term exists in
the constraints. Nth-Update captures the read-over-write axioms of arrays, adapted to
consider their lengths (see, e.g., [10]). It distinguishes three cases: In the first, the update
index is out of bounds. In the second, it is not out of bounds, and the corresponding nth
term accesses the same index that was updated. In the third case, the index used in the
nth term is different from the updated index. Update-Bound considers two cases: either
the update changes the sequence, or the sequence remains the same. Finally, Nth-Split
introduces a case split on the equality between two sequence variables x and x1 whenever
they appear as arguments to nth with equivalent second arguments. This is needed to
ensure that we detect all cases where the arguments of two nth terms must be equal.

4.3   Correctness
In this section we prove the following theorem:
Theorem 1. Let X P tBASE, EXTu and pS0 , A0 q be a configuration, and assume
without loss of generality that A0 contains only arithmetic constraints that are not
sequence constraints. Let T be a derivation tree obtained by applying the rules of X
with pS0 , A0 q as the initial configuration.
 1. If T is closed, then S0 Y A0 is TSeq -unsatisfiable.
 2. If T contains a saturated configuration pS, Aq w.r.t. X, then pS, Aq is TSeq -satisfiable,
    and so is pS0 , A0 q.
The theorem states that the calculi are correct in the following sense: if a closed derivation
tree is obtained for the constraints S0 Y A0 then those constraints are unsatisfiable in
TSeq ; if a tree with a saturated leaf is obtained, then they are satisfiable. It is possible,
however, that neither kind of tree can be derived by the calculi, making them neither
refutation-complete nor terminating. This is not surprising since, as mentioned in the
introduction, the decidability of even weaker theories is still unknown.
    Proving the first claim in Theorem 1 reduces to a local soundness argument for each
of the rules. For the second claim, we sketch below how to construct a satisfying model
M from a saturated configuration for the case of EXT. The case for BASE is similar
and simpler.

Model construction steps The full model construction and its correctness are described
in the appendix together with a proof of the theorem above. Here is a summary of the
steps needed for the model construction.
 1. Sorts: MpElemq is interpreted as some arbitrary countably infinite set. MpSeqq and
     MpIntq are then determined by the theory.
 2. ΣSeq -symbols: TSeq enforces the interpretation of almost all ΣSeq -symbols, except
     for nth when the second input is out of bounds. We cover this case below.
 3. Integer variables: based on the saturation of A-Conf, we know there is some TLIA -
     model satisfying A. We set M to interpret integer variables according to this model.


                                              12
                                x « nthpy, iq P S               S |ù˚
                                                                    `` y « w1 `` ¨ ¨ ¨ `` wn
           Nth-Concat
                                           A :“ A, i ă 0 _ i ě `y k
                          A :“ A, 0 ď i ă `w1     S :“ S, x « nthpw1 , iq k . . . k
                                n´1
                                ÿ              n
                                               ÿ                                   n´1
                                                                                   ÿ
                        A :“ A,     `wj ď i ă    `wj      S :“ S, x « nthpwn , i ´     `wj q
                                j“1               j“1                                               j“1


                               x « updatepy, i, vq P S                S |ù˚
                                                                          `` y « w1 `` ¨ ¨ ¨ `` wn
             Update-Concat
                                                S :“ S, x « z1 `` ¨ ¨ ¨ `` zn ,
                                                                                             n´1
                                                                                             ÿ
                              z1 « updatepw1 , i, vq, . . . , zn « updatepwn , i ´                 `wj , vq
                                                                                             j“1


                                 x « updatepy, i, vq P S                S |ù˚
                                                                            `` x « w1 `` ¨ ¨ ¨ `` wn
           Update-Concat-Inv
                                                   S :“ S, y « z1 `` ¨ ¨ ¨ `` zn ,
                                                                                               n´1
                                                                                               ÿ
                                w1 « updatepz1 , i, vq, . . . , wn « updatepzn , i ´                 `wj , vq
                                                                                               j“1


                                       x « nthpy, iq P S              S |ù y « unitpuq
               Nth-Unit
                          A :“ A, i ă 0 _ i ą 0         k       A :“ A, i « 0           S :“ S, x « u

                                      x « updatepy, i, vq P S             S |ù y « unitpuq
                 Update-Unit
                                A :“ A, i ă 0 _ i ą 0                 S :“ S, x « unitpuq      k
                                       A :“ A, i « 0                 S :“ S, x « unitpvq

                                                s1 « updateps, i, tq P S
                             Nth-Intro
                                         S :“ S, e « nthps, iq, e1 « nthps1 , iq

                     nthpx, jq P T pSq       y « updatepz, i, vq P S             S |ù x « y or S |ù x « z
        Nth-Update
                                             A :“ A, j ă 0 _ j ě `x k
                             A :“ A, i « j, 0 ď j ă `x      S :“ S, nthpy, jq « v k
                             A :“ A, i ff j, 0 ď j ă `x     S :“ S, nthpy, jq « nthpz, jq

                                                   x « updatepy, i, vq P S
          Update-Bound
                           A :“ A, 0 ď i ă `y           S :“ S, nthpy, iq ff v           k   S :“ S, x « y
                                                        1   1                       1
                                      nthpx, iq, nthpx , i q P T pSq          i«i PA
                          Nth-Split
                                         S :“ S, x « x1          k     S :“ S, x ff x1

Fig. 6: Extended derivation rules. The rules use z1 , . . . , zn to denote fresh sequence
variables and e, e1 to denote fresh element variables.

 4. Element variables: these are partitioned into their ”S equivalence classes. Each class
    is assigned a distinct element from MpElemq, which is possible since it is infinite.
 5. Atomic sequence variables: these are assigned interpretations in several sub-steps:
    (a) length: we first use the assignments to variables `x to set the length of Mpxq,
         without assigning its actual value.
    (b) unit variables: for variables x with x ”S unitpzq, we set Mpxq to be rMpzqs.
    (c) non-unit variables: All other sequence variables are assigned values according
         to a weak equivalence graph we construct in a manner similar to [10]. This
         construction takes into account constraints that involve update and nth.
 6. Non-atomic sequence variables: these are first transformed to their unique normal
    form (see Lemma 4), consisting of concatenations of atomic variables. Then, the
    values assigned to these variables are concatenated.


                                                     13
 7. nth-terms: for out-of-bounds indices in nth-terms, we rely on ”S to make sure that
    the assignment is consistent.
We conclude this section with an example of the construction of M.

Example 5. Consider a signature in which Elem is Int, and a saturated configuration
pS˚ , A˚ q w.r.t. EXT that includes the following formulas: y « y1 `` y2 , x « x1 `` x2 ,
y2 « x2 , y1 « updatepx1 , i, aq, |y1 | “ |x1 |, |y2 | “ |x2 |, nthpy, iq « a, nthpy1 , iq « a.
Following the above construction, a satisfying interpretation M can be built as follows:
Step 1 Set both MpIntq and MpElemq to be the set of integer numbers. MpSeqq is
     fixed by the theory.
Step 3, Step 4 First, find an arithmetic model, Mp`x q “ Mp`y q “ 4, Mp`y1 q “
     Mp`x1 q “ 2, Mp`y2 q “ Mp`x2 q “ 2, Mpiq “ 0. Further, set Mpaq “ 0.
Step 5a Start assigning values to sequences. First, set the lengths of Mpxq and Mpyq
     to be 4, and the lengths of Mpx1 q, Mpx2 q, Mpy1 q, Mpy2 q to be 2.
Step 5b is skipped as there are no unit terms.
Step 5c Set the 0th element of Mpy1 q to 0 to satisfy nthpy1 , iq “ a (y1 is atomic, y is
     not). Assign fresh values to the remaining indices of atomic variables. The result
     can be, e.g., Mpy1 q “ r0, 2s, Mpx1 q “ r1, 2s, Mpy2 q “ Mpx2 q “ r3, 4s.
Step 6 Assign non-atomic sequence variables based on equivalent concatenations:
     Mpyq “ r0, 2, 3, 4s, Mpxq “ r1, 2, 3, 4s.
Step 7 No integer variable in the formula was assigned an out-of-bound value, and so
     the interpretation of nth on out-of-bounds cases is set arbitrarily.


5   Implementation

We implemented our procedure for sequences as an extension of a previous theory solver
for strings [18, 23]. This solver is integrated in cvc5, and has been generalized to reason
about both strings and sequences. In this section, we describe how the rules of the
calculus are implemented and the overall strategy for when they are applied.
    Like most SMT solvers, cvc5 is based on the CDCLpT q architecture [20] which
combines several subsolvers, each specialized on a specific theory, with a solver for
propositional satisfiability (SAT). Following that architecture, cvc5 maintains an evolving
set of formulas F. When F starts with quantifier-free formulas over the theory TSeq ,
the case targeted by this work, the SAT solver searches for a satisfying assignment
for F, represented as the set M of literals it satisfies. If none exists, the problem is
unsatisfiable at the propositional level and hence TSeq -unsatisfiable. Otherwise, M is
partitioned into the arithmetic constraints A and the sequence constraints S and checked
for TSeq -satisfiability using the rules of the EXT calculus. Many of those rules, including
all those with multiple conclusions, are implemented by adding new formulas to F
(following the splitting-on-demand approach [4]). This causes the SAT solver to try to
extend its assignment to those formulas, which results in the addition of new literals to
M (and thereby also to A and S).
    In this setting, the rules of the two calculi are implemented as follows. The effect
of rule A-Conf is achieved by invoking cvc5’s theory solver for linear integer arithmetic.
Rule S-Conf is implemented by the congruence closure submodule of the theory solver


                                             14
for sequences. Rules A-Prop and S-Prop are implemented by the standard mechanism
for theory combination. Note that each of these four rules may be applied eagerly, that
is, before constructing a complete satisfying assignment M for F.
     The remaining rules are implemented in the theory solver for sequences. Each time
M is checked for satisfiability, cvc5 follows a strategy to determine which rule to apply
next. If none of the rules apply and the configuration is different from unsat, then it is
saturated, and the solver returns sat. The strategy for EXT prioritizes rules as follows.
Only the first applicable rule is applied (and then control goes back to the SAT solver).
  1. (Add length constraints) For each sequence term in S, apply L-Intro or L-Valid, if not
     already done. We apply L-Intro for non-variables, and L-Valid for variables.
  2. (Mark congruent terms) For each set of update (resp. nth) terms that are congruent
     to one another in the current configuration, mark all but one term and ignore the
     marked terms in the subsequent steps.
  3. (Reduce extract) For extractpy, i, jq in S, apply R-Extract if not already done.
  4. (Construct normal forms) Apply U-Eq or C-Split. We choose how to apply the
     latter rule based on constructing normal forms for equivalence classes in a bottom-
     up fashion, where the equivalence classes of x and y are considered before the
     equivalence class of x `` y. We do this until we find an equivalence class such that
     S |ù˚`` z « u1 and S |ù˚`` z « u2 for distinct u1 , u2 .
  5. (Normal forms) Apply C-Eq if two equivalence classes have the same normal form.
  6. (Extensionality) For each disequality in S, apply Deq-Ext, if not already done.
  7. (Distribute update and nth) For each term updatepx, i, tq (resp. nthpx, jq) such that
     the normal form of x is a concatenation term, apply Update-Concat and Update-
     Concat-Inv (resp. Nth-Concat) if not already done. Alternatively, if the normal form
     of the equivalence class of x is a unit term, apply Update-Unit (resp. Nth-Unit).
  8. (Array reasoning on atomic sequences) Apply Nth-Intro and Update-Bound to update
     terms. For each update term, find the matching nth terms and apply Nth-Update.
     Apply Nth-Split to pairs of nth terms with equivalent indices.
  9. (Theory combination) Apply S-A for all arithmetic terms occurring in both S and A.
Whenever a rule is applied, the strategy will restart from the beginning in the next
iteration. The strategy is designed to apply with higher priority steps that are easy to
compute and are likely to lead to conflicts. Some steps are ordered based on dependencies
from other steps. For instance, Steps 5 and 7 use normal forms, which are computed in
Step 4. The strategy for the BASE calculus is the same, except that Steps 7 and 8 are
replaced by one that applies R-Update and R-Nth to all update and nth terms in S.
     We point out that the C-Split rule may cause non-termination of the proof strategy
described above in the presence of cyclic sequence constraints, for instance, constraints
where sequence variables appear on both sides of an equality. The solver uses methods
for detecting some of these cycles, to restrict when C-Split is applied. In particular, when
S |ù˚`` x « pu `` s `` wqÓ, S |ù˚`` x « pu `` t `` vqÓ, and s occurs in v, then
C-Split is not applied. Instead, other heuristics are used, and in some cases the solver
terminates with a response of “unknown” (see e.g., [18] for details). In addition to the
version shown here, we also use another variation of the C-Split rule where the normal
forms are matched in reverse (starting from the last terms in the concatenations). The
implementation also uses fast entailment tests for length inequalities. These tests may


                                            15
allow us to conclude which branch of C-Split, if any, is feasible, without having to branch
on cases explicitly.
     Although not shown here, the calculus can also accommodate certain extended
sequence constraints, that is, constraints using a signature with additional functions. For
example, our implementation supports sequence containment, replacement, and reverse.
It also supports an extended variant of the update operator, in which the third argument
is a sequence that overrides the sequence being updated starting from the index given
in the second argument. Constraints involving these functions are handled by reduction
rules, similar to those shown in Figure 5. The implementation is further optimized by
using context-dependent simplifications, which may eagerly infer when certain sequence
terms can be simplified to constants based on the current set of assertions [23].


6     Evaluation

We evaluate the performance of our approach, as implemented in cvc5. The evaluation
investigates: (i) whether the use of sequences is a viable option for reasoning about
vectors in programs, (ii) how our approach compares with other sequence solvers, and
(iii) what is the performance impact of our array-style extended rules. As a baseline,
we use Version 4.8.14 of the Z3 SMT solver, which supports a theory of sequences
without updates. For cvc5, we evaluate implementations of both the basic calculus
(denoted cvc5) and the extended array-based calculus (denoted cvc5-a). The benchmarks,
solver configurations, and logs from our runs are available for download.4 We ran all
experiments on a cluster equipped with Intel Xeon E5-2620 v4 CPUs. We allocated one
physical CPU core and 8GB of RAM for each solver-benchmark pair and used a time
limit of 300 seconds. We use the following two sets of benchmarks:
Array Benchmarks (A RRAYS) The first set of benchmarks is derived from the QF_AX
benchmarks in SMT-LIB [3]. To generate these benchmarks, we (i) replace declarations
of arrays with declarations of sequences of uninterpreted sorts, (ii) change the sort of
index terms to integers, and (iii) replace store with update and select with nth. The
resulting benchmarks are quantifier-free and do not contain concatenations. Note that
the original and the derived benchmarks are not equisatisfiable, because sequences take
into account out-of-bounds cases that do not occur in arrays. For the Z3 runs, we add to
the benchmarks a definition of update in terms of extraction and concatenation.
Smart Contract Verification (D IEM) The second set of benchmarks consists of verifi-
cation conditions generated by running the Move Prover [24] on smart contracts written
for the Diem framework. By default, the encoding does not use the sequence update
operation, and so Z3 can be used directly. However, we also modified the Move Prover
encoding to generate benchmarks that do use the update operator, and ran cvc5 on them.
In addition to using the sequence theory, the benchmarks make heavy use of quantifiers
and the SMT-LIB theory of datatypes.
    Figure 7a summarizes the results in terms of number of solved benchmarks and total
time in seconds on commonly solved benchmarks. The configuration that solves the
 4
     http://dx.doi.org/10.5281/zenodo.6146565


                                           16
                                                               sat                                         sat

                    w/ update                       102        unsat
                                                               10x
                                                                                                     102   unsat
                                                                                                           10x
                                                               100x                                        100x
     Set           cvc5 cvc5-a   Z3                            1000x                                       1000x




                                       cvc5-a [s]




                                                                                        cvc5-a [s]
                                                    101                                              101
 A RRAYS Slvd      242     390 170
  (551)  Time      162     303 4329
                                                    100                                              100

    D IEM   Slvd   542     547   443
    (558)   Time   518     440   639        10−1 −1                                          10−1 −1
                                               10                100        101   102           10           100        101   102
                                                                       cvc5 [s]                                    cvc5 [s]


                   (a)                                    (b) A RRAYS                                      (c) D IEM

Fig. 7: Figure 7a lists the number of solved benchmarks and total time on commonly
solved benchmarks. The scatter plots compare the base solver (cvc5) and the extended
solver (cvc5-a) on A RRAY (Figure 7b) and D IEM (Figure 7c) benchmarks.


largest number of benchmarks is the implementation of the extended calculus (cvc5-a).
This approach also successfully solves most of the D IEM benchmarks, which suggests
that sequences are a promising option for encoding vectors in programs. The results
further show that the sequences solver of cvc5 significantly outperforms Z3 on both the
number of solved benchmarks and the solving time on commonly solved benchmarks.
    Figures 7b and 7c show scatter plots comparing cvc5 and cvc5-a on the two bench-
mark sets. We can see a clear trend towards better performance when using the extended
solver. In particular, the table shows that in addition to solving the most benchmarks,
cvc5-a is also fastest on the commonly solved instances from the D IEM benchmark set.
    For the A RRAYS set, we can see that some benchmarks are slower with the extended
solver. This is also reflected in the table, where cvc5-a is slower on the commonly solved
instances. This is not too surprising, as the extra machinery of the extended solver can
sometimes slow down easy problems. As problems get harder, however, the benefit of
the extended solver becomes clear. For example, if we drop Z3 and consider just the
commonly solved instances between cvc5 and cvc5-a (of which there are 242), cvc5-a is
about 2.47ˆ faster (426 vs 1053 seconds). Of course, further improving the performance
of cvc5-a is something we plan to explore in future work.


7     Conclusion

We introduced calculi for checking satisfiability in the theory of sequences, which can
be used to model the vector data type. We described our implementation in cvc5 and pro-
vided an evaluation, showing that the proposed theory is rich enough to naturally express
verification conditions without introducing quantifiers, and that our implementation is
efficient. We believe that verification tools can benefit by changing their encoding of ver-
ification conditions that involve vectors to use the proposed theory and implementation.
     We plan to propose the incorporation of this theory in the SMT-LIB standard and
contribute our benchmarks to SMT-LIB. As future research, we plan to integrate other
approaches for array solving into our basic solver. We also plan to study the polite-
ness [17, 21] and decidability of various fragments of the theory of sequences.


                                                          17
References
 [1] F. Alberti, S. Ghilardi, and E. Pagani. Cardinality constraints for arrays (decidability results
     and applications). Formal Methods Syst. Des., 51(3):545–574, 2017.
 [2] H. Barbosa, C. W. Barrett, M. Brain, G. Kremer, H. Lachnitt, M. Mann, A. Mohamed,
     M. Mohamed, A. Niemetz, A. Nötzli, A. Ozdemir, M. Preiner, A. Reynolds, Y. Sheng,
     C. Tinelli, and Y. Zohar. cvc5: A versatile and industrial-strength SMT solver. In TACAS
     (1), volume 13243 of Lecture Notes in Computer Science, pages 415–442. Springer, 2022.
 [3] C. Barrett, P. Fontaine, and C. Tinelli. The SMT-LIB Standard: Version 2.6. Technical
     report, Department of Computer Science, The University of Iowa, 2017. Available at
     www.SMT-LIB.org.
 [4] C. Barrett, R. Nieuwenhuis, A. Oliveras, and C. Tinelli. Splitting on demand in SAT modulo
     theories. In M. Hermann and A. Voronkov, editors, Proceedings of the 13th International
     Conference on Logic for Programming, Artificial Intelligence and Reasoning (LPAR’06),
     Phnom Penh, Cambodia, volume 4246 of Lecture Notes in Computer Science, pages 512–526.
     Springer, 2006.
 [5] C. W. Barrett and C. Tinelli. Satisfiability modulo theories. In Handbook of Model Checking,
     pages 305–343. Springer, 2018.
 [6] M. Berzish, V. Ganesh, and Y. Zheng. Z3str3: A string solver with theory-aware heuristics.
     In D. Stewart and G. Weissenbacher, editors, 2017 Formal Methods in Computer Aided
     Design, FMCAD 2017, Vienna, Austria, October 2-6, 2017, pages 55–59. IEEE, 2017.
 [7] N. Bjørner, L. de Moura, L. Nachmanson, and C. Wintersteiger. Programming
     Z3. https://theory.stanford.edu/˜nikolaj/programmingz3.html#
     sec-sequences-and-strings, 2018.
 [8] N. Bjørner, V. Ganesh, R. Michel, and M. Veanes. An SMT-LIB format for sequences and
     regular expressions. SMT, 12:76–86, 2012.
 [9] N. Bjørner, N. Tillmann, and A. Voronkov. Path feasibility analysis for string-manipulating
     programs. In S. Kowalewski and A. Philippou, editors, Tools and Algorithms for the
     Construction and Analysis of Systems, 15th International Conference, TACAS 2009, Held as
     Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2009,
     York, UK, March 22-29, 2009. Proceedings, volume 5505 of Lecture Notes in Computer
     Science, pages 307–321. Springer, 2009.
[10] J. Christ and J. Hoenicke. Weakly equivalent arrays. In FroCos, volume 9322 of Lecture
     Notes in Computer Science, pages 119–134. Springer, 2015.
[11] L. M. de Moura and N. Bjørner. Z3: an efficient SMT solver. In TACAS, volume 4963 of
     Lecture Notes in Computer Science, pages 337–340. Springer, 2008.
[12] N. Dershowitz and Z. Manna. Proving termination with multiset orderings. Commun. ACM,
     22(8):465–476, 1979.
[13] N. Elad, S. Rain, N. Immerman, L. Kovács, and M. Sagiv. Summing up smart transitions.
     In CAV (1), volume 12759 of Lecture Notes in Computer Science, pages 317–340. Springer,
     2021.
[14] H. B. Enderton. A mathematical introduction to logic. Academic Press, 2 edition, 2001.
[15] S. Falke, F. Merz, and C. Sinz. Extending the theory of arrays: memset, memcpy, and
     beyond. In VSTTE, volume 8164 of Lecture Notes in Computer Science, pages 108–128.
     Springer, 2013.
[16] V. Ganesh, M. Minnes, A. Solar-Lezama, and M. C. Rinard. Word equations with length
     constraints: What’s decidable? In Haifa Verification Conference, volume 7857 of Lecture
     Notes in Computer Science, pages 209–226. Springer, 2012.
[17] D. Jovanovic and C. W. Barrett. Polite theories revisited. In C. G. Fermüller and A. Voronkov,
     editors, Logic for Programming, Artificial Intelligence, and Reasoning - 17th International


                                                18
     Conference, LPAR-17, Yogyakarta, Indonesia, October 10-15, 2010. Proceedings, volume
     6397 of Lecture Notes in Computer Science, pages 402–416. Springer, 2010.
[18] T. Liang, A. Reynolds, C. Tinelli, C. W. Barrett, and M. Deters. A DPLL(T) theory solver
     for a theory of strings and regular expressions. In A. Biere and R. Bloem, editors, Computer
     Aided Verification - 26th International Conference, CAV 2014, Held as Part of the Vienna
     Summer of Logic, VSL 2014, Vienna, Austria, July 18-22, 2014. Proceedings, volume 8559
     of Lecture Notes in Computer Science, pages 646–662. Springer, 2014.
[19] G. Nelson and D. C. Oppen. Simplification by cooperating decision procedures. ACM Trans.
     Program. Lang. Syst., 1(2):245–257, 1979.
[20] R. Nieuwenhuis, A. Oliveras, and C. Tinelli. Solving SAT and SAT Modulo Theories: from
     an abstract Davis-Putnam-Logemann-Loveland Procedure to DPLL(T). Journal of the ACM,
     53(6):937–977, Nov. 2006.
[21] S. Ranise, C. Ringeissen, and C. G. Zarba. Combining data structures with nonstably infinite
     theories using many-sorted logic. In B. Gramlich, editor, Frontiers of Combining Systems, 5th
     International Workshop, FroCoS 2005, Vienna, Austria, September 19-21, 2005, Proceedings,
     volume 3717 of Lecture Notes in Computer Science, pages 48–64. Springer, 2005. Extended
     technical report is available at https://hal.inria.fr/inria-00070335/.
[22] A. Reynolds, A. Nötzli, C. W. Barrett, and C. Tinelli. Reductions for strings and regular
     expressions revisited. In 2020 Formal Methods in Computer Aided Design, FMCAD 2020,
     Haifa, Israel, September 21-24, 2020, pages 225–235. IEEE, 2020.
[23] A. Reynolds, M. Woo, C. W. Barrett, D. Brumley, T. Liang, and C. Tinelli. Scaling up
     DPLL(T) string solvers using context-dependent simplification. In R. Majumdar and
     V. Kuncak, editors, Computer Aided Verification - 29th International Conference, CAV 2017,
     Heidelberg, Germany, July 24-28, 2017, Proceedings, Part II, volume 10427 of Lecture
     Notes in Computer Science, pages 453–474. Springer, 2017.
[24] J. E. Zhong, K. Cheang, S. Qadeer, W. Grieskamp, S. Blackshear, J. Park, Y. Zohar, C. Barrett,
     and D. L. Dill. The Move prover. In S. K. Lahiri and C. Wang, editors, Proceedings of the
     32nd International Conference on Computer Aided Verification (CAV ’20), volume 12224 of
     Lecture Notes in Computer Science, pages 137–150. Springer International Publishing, July
     2020.




                                               19
A     Appendix
In this appendix, each section presents a proof that was omitted from the main text due
to lack of space. For convenience, the lemma/theorem that is being proved is repeated at
the beginning of each section.
    Below, we make use of the following helper lemma.

Lemma 5. Let S be a set of sequence constraints and A a set of arithmetic constraints.
Suppose pS, Aq is saturated w.r.t. S-Prop, L-Intro and L-Valid. If x1 `` ¨ ¨ ¨ `` xn P T pSq
is a variable concatenation term of size n not singular in S, then
               n
 1. A |ùLIA Σk“1   `xk ě 2; and
                                     n
 2. for each m P r1, ns, A |ùLIA Σk“1   `xk ą `xm .

Proof. Let i, j P r1, ns, i ‰ j, such that S * xi «  and S * xj « . We know that
xi , xj P T pSq, so by saturation of L-Valid, we have A |ù `xi ą 0 and A |ù `xj ą 0.
Also, by saturation of L-Valid, L-Intro, and S-Prop, together with Assumption 1, we know
                                                                n
that A |ùLIA `xk ě 0 for k P r1, ns. It follows that A |ùLIA Σk“1   `xk ě 2. Furthermore,
                                 n
for each m P r1, ns, A |ùLIA Σk“1 `xk ą `xm .

A.1   Proof of Lemma 1
Lemma 1. For every quantifier-free ΣSeq -formula ϕ, there are sets S1 , . . . , Sn of se-
quence constraints and sets A1 , . . . , An of arithmetic constraints such that ϕ is TSeq -
satisfiable iff Si Y Ai is TSeq -satisfiable for some i P r1, ns.

Proof. Using standard transformations, ϕ can be transformed into an equisatisfiable
disjunction ϕ1 “ ϕ1 _ . . . _ ϕn , where for i P r1, ns, ϕi is a conjunction ϕ1i , . . . , ϕni i
of flat literals. Each flat literal in ϕ1 is either a sequence constraint or an arithmetic
constraint. For each i P r1, ns we set Si “ tϕji | such that ϕji is a sequence constraint
u and Ai “ tϕji | such that ϕji is an arithmetic constraint u. Hence, for every TSeq -
interpretation M, M |ù ϕ iff M |ù Si Y Ai for some i P r1, ns.

A.2   Proof of Lemma 3
Lemma 3. Let S be a set of sequence constraints and A a set of arithmetic constraints. If
pS, Aq is saturated w.r.t. S-Prop, L-Intro and L-Valid, the problem of determining whether
S |ù˚`` x « s for given x and s is decidable.

Proof. We show that the set of pairs px, sq for which S |ù`` x « s is finite (it is then
easy to see that the set of pairs py, tq for which S |ù˚`` y « t is also finite). Consider a
tree whose root is obtained by Item 1 or Item 2 of Definition 6 where the children of a
node are all possible results of applying Item 3 of Definition 6. Note that each node can
have only finitely many children as there are only finitely many pairs py, tq where y is a
variable in S and t is  or a variable concatenation term in T pSq. Below, we show that
every path in the tree is finite, from which it follows that the tree is finite. Since there are
only finitely many such trees, it follows that the set of px, sq for which S |ù`` x « s is
finite.


                                              20
     Define a partial order ă over terms of sort Seq in T pSq, by s ă t iff A |ùLIA
`xs ă `xt for some variables xs and xt such that xs ”S s and xt ”S t. We show
that ă is well defined. First, by Assumption 1, such xs and xt exist. Next, if xs ”S s,
xt ”S t, x1s ”S s and x1t ”S t, then A |ùLIA `xs ă `xt iff A |ùLIA `x1s ă `x1t , since
S |ù xs « x1s and S |ù xt « x1t and saturation of S-Prop. Let ă˚ be the (well-founded)
Dershowitz-Manna multiset ordering induced by ă [12], that is, the minimal transitive
relation that satisfies: A ă˚ B whenever A is obtained from B by removing a single
element b, and possibly adding any finite number of elements a such that a ă b for
every such new element. Now, for each term t of sort Seq in T pSq, let mptq be the
multiset of the terms occurring in it (the multiplicity of each element in this multiset
is the number of times it occurs in t). We prove the following claim, which establishes
that every path in the tree mentioned above is finite: if S |ù`` x « pw `` y `` zqÓ,
S |ù y « t and t is  or a variable concatenation term in S that is not singular in S, then
mppw `` y `` zqÓq ą˚ mppw `` t `` zqÓq.
     We consider two cases: t is  or t is a variable concatenation term in T pSq not singular
in S. In the first case, pw `` t `` zqÓ “ pw `` zqÓ. Note that the only role of Ó here
is to flatten nested concatenations. Hence, y is removed from the multiset of sub-terms
and is not replaced by anything, so mppw `` y `` zqÓq ą˚ mppw `` t `` zqÓq.
     In the second case, t is a variable concatenation term in S not singular in S. Let
t “ t1 `` . . . `` tn . Now, pw `` pt1 `` ¨ ¨ ¨ `` tn q `` zqÓ is a flat concatenation in
which y was removed, and t1 , . . . , tn were added. To prove a decrease in ă˚ from
mppw `` y `` zqÓq to mppw `` t `` zqÓq, we show that for every k P r1, ns, tk ă y,
that is, A |ùLIA `tk ă `y (notice that tk and y are variables). By Lemma 5, we know that
                                n
for each k P r1, ns, A |ùLIA Σi“1   `ti ą `tk . Since S |ù y « t, we have S |ù |y| “ |t|. By
                                                                                        n
saturation of L-Intro and S-Prop, and by Assumption 1, it follows that A |ù `y “ Σi“1      `ti .
Thus, A |ùLIA `y ą `tk .



A.3   Proof of Lemma 4

Lemma 4. Let S be a set of sequence constraints and A a set of arithmetic constraints.
Suppose pS, Aq is saturated w.r.t. A-Conf, S-Prop, L-Intro, L-Valid, and C-Split. Then, for
every equivalence class e of ”S whose terms are of sort Seq, there exists a unique
(possibly empty) s such that whenever S |ù˚`` x « s1 for x P e, then s1 “ s. In this case,
we call s the normal form of e (and of x).

Proof. Let e be an equivalence class of ”S whose terms are of sort Seq, and let x P e
(we know every equivalence class has at least one variable by Lemma 2). We show
existence and uniqueness of a normal form for e.
Existence: We show that for some s, S |ù˚`` x « s. Consider the tree construction of
Lemma 3. If we follow some path in the tree, we will reach a node S |ù`` x « t for
which no children can be derived (i.e., Item 3 of Definition 6 doesn’t apply). It is not
hard to see that t “ pt1 , . . . , tn q, where n ě 0 and each ti is a variable for i P r1, ns.
    Let s have the same length as t and let si :“ αpti q for i P r1, ns. We prove that
S |ù˚`` x « s. We know that S |ù`` x « t. If n “ 0, then trivially, S |ù˚`` x « s.


                                              21
Otherwise, for each i P r1, ns, we further know that S |ù ti « si and si “ αprsi sq, so it
only remains to show that si is atomic in S. Assume it is not. Then either S |ù si « 
or there exists a variable concatenation term u P T pSq not singular in S such that
S |ù si « u. In either case, this would imply that Item 3 of Definition 6 is applicable to
S |ù`` x « t, contradicting our assumption.
Uniqueness: By the existence argument above, there exists some s such that S |ù˚``
x « s. Now, suppose S |ù˚`` x « s1 , and assume that s ‰ s1 . Then there must be
w, z, z 1 , y, y 1 , each containing only variables that are atomic representatives, such that
s “ pw `` y `` zqÓ and s1 “ pw `` y 1 `` z 1 qÓ, with y ‰ y 1 . By saturation w.r.t.
C-Split, there are three possibilities: A |ù `y ą `y1 and y « y 1 `` k P S for some k;
A |ù `y ă `y1 and y 1 « y `` k P S for some k; or A |ù `y “ `y1 and y « y 1 P S. In
the first case, notice that since S |ù y « y 1 `` k, it follows that S |ù |y| « |y 1 `` k|.
Also, by saturation of L-Intro, S |ù |y 1 `` k| « |y 1 | ` |k|. So, S |ù |y| « |y 1 | ` |k|.
And, by saturation of S-Prop and Assumption 1 also A |ù `y « `y1 ` `k . It follows
that S * k « ; otherwise, we would have A |ù `k « 0 by L-Intro and S-Prop, which
together with A |ù `y ą `y1 contradicts saturation of A-Conf. Also, y 1 is atomic and
hence, S * y 1 « . Thus, S |ù y « y 1 `` k but y 1 `` k is not singular in S as S * k « 
and S * y 1 « . In particular, this means that y is not atomic, which contradicts our
assumption, so the first case is impossible. The second case is analogous to the first. In
the third case, we have y « y 1 P S, but we know that y and y 1 are both equivalence class
representatives, so it must be that y “ y 1 , which contradicts our assumption that y ‰ y 1 .



A.4   Proof of Theorem 1, Item 1

Theorem 1. Let X P tBASE, EXTu and pS0 , A0 q be a configuration, and assume
without loss of generality that A0 contains only arithmetic constraints that are not
sequence constraints. Let T be a derivation tree obtained by applying the rules of X
with pS0 , A0 q as the initial configuration.
 1. If T is closed, then S0 Y A0 is TSeq -unsatisfiable.
 2. If T contains a saturated configuration pS, Aq w.r.t. X, then pS, Aq is TSeq -satisfiable,
    and so is pS0 , A0 q.

    The proof of Item 1 is routine, and amounts to a local soundness check of each of
the derivation rules. The only non-trivial case is C-Split, which relies on the following
lemma:

Lemma 6. Let S be a set of sequence constraints and A a set of arithmetic constraints.
Suppose pS, Aq is saturated w.r.t. S-Prop, L-Intro and L-Valid. If S |ù˚`` x « s then
S |ùTSeq x « s.

Proof. Suppose S |ù˚`` x « s where s “ ps1 , . . . , sn q. Then, for some s1 “ ps11 , . . . , s1n q,
S |ù`` x « s1 and S |ù si « s1i for i P r1, ns. To show that S |ùTSeq x « s, it thus
suffices to show that S |ùTSeq x « s1 . As shown in Lemma 3, there is a finite number
k of derivation steps in |ù`` that yield x « s1 . We prove the claim by induction on


                                               22
k. For k “ 1, we either apply Item 1 or Item 2. In the former case we get a trivial
identity S |ù`` x « x, and clearly S |ùTSeq x « x. In the latter case, we get an identity
S |ù`` x « t such that S |ù x « t, and so in particular S |ùTSeq x « t. Suppose
k ą 1, and that x « s1 was obtained using Item 3 of Definition 6. Hence, s1 has the
form pw `` t `` zqÓ, where S |ù`` x « pw `` y `` zqÓ with a shorter derivation,
and S |ù y « t. By the induction hypothesis, S |ùTSeq x « pw `` y `` zqÓ. Clearly,
S |ùTSeq y « t. Hence, S |ùTSeq x « s1 .

   Using Lemma 6, since S |ù˚`` x « s implies that x « s follows from S in TSeq ,
we have that every model of the assumptions of C-Split assigns the same values to
pw `` y `` zqÓ and pw `` y 1 `` z 1 qÓ. Assuming that the first two branches of the
conclusion do not hold in some model, we indeed get that the interpretations of y and y 1
must be identical, as they are the sub-sequence of the same sequence, that begins at the
same index and whose length is the same.


A.5   Proof of Theorem 1, Item 2

Theorem 1. Let X P tBASE, EXTu and pS0 , A0 q be a configuration, and assume
without loss of generality that A0 contains only arithmetic constraints that are not
sequence constraints. Let T be a derivation tree obtained by applying the rules of X
with pS0 , A0 q as the initial configuration.
 1. If T is closed, then S0 Y A0 is TSeq -unsatisfiable.
 2. If T contains a saturated configuration pS, Aq w.r.t. X, then pS, Aq is TSeq -satisfiable,
    and so is pS0 , A0 q.

    Consider a saturated configuration pS, Aq. We define an interpretation M. Unless
stated otherwise, by equivalence class we mean an equivalence class w.r.t. ”S and may
drop the subscript when referring to it (e.g., writing rxs for the equivalence class of x).
We also sometimes drop “in S” from “atomic in S” when S is clear from context. We say
that an equivalence class e is atomic if its terms are of sort Seq and all variables in it are
atomic. Note that if e contains any variable that is atomic in S, then all variables in e are
atomic in S.
    The following definitions completely define the model M. Concretely, Definition 10
defines the domains of M; Definition 11 defines the function symbols of ΣSeq . Defini-
tion 12 defines the interpretations of variables of sort Int and Elem; Definition 13 assigns
lengths to the interpretations of variables of sort Seq that are atomic in S (it does not set
their values, but only their lengths); Definition 15 defines the interpretations of variables
of sort Seq that are equivalent to unit terms; Definition 18 defines the interpretations
of variables of sort Seq that are atomic in S but are not equivalent to unit terms; Def-
inition 19 defines the interpretations of variables of sort Seq that are not atomic in S;
Finally, Definition 20 defines the interpretation of the nth symbol in M (note that only a
part of its interpretation is fixed by the theory).
    The definitions are shown to be well-defined in Lemma 10.
    We start by assigning domains to the sorts of TSeq .

Definition 10 (Model construction: domains).


                                             23
 1. MpIntq “ Z, the set of integers.
 2. MpElemq is some countably infinite set.
 3. MpSeqq is the set of finite sequences whose elements are taken from MpElemq.
    The domains for Int and Seq were chosen to be consistent with the requirements
of TSeq . The exact identity of Elem is not important, and so we set its elements to be
arbitrary. In contrast, its cardinality is important, and is set to be infinite.
Definition 11 (Model construction: function symbols). The symbols shown in Fig-
ure 1 are interpreted in such a way that M is both a TLIA -interpretation and a TSeq -
interpretation, as described in Figure 1 and in Sections 2 and 3.
Now we can assign values to variables of sort Int and Elem.
Definition 12 (Model construction: Int and Elem variables).
 1. Let A be a TLIA -interpretation with ApIntq “ Z that satisfies A. Then Mpxq :“
    Apxq for every variable x of sort Int.
 2. Let a1 , a2 , . . . be an enumeration of MpElemq, and let e1 , . . . , en be an enumeration
    of the equivalence classes of ”S whose variables have sort Elem. Then, for every
    i P r1, ns and every variable x P ei , Mpxq :“ ai .
Lemma 7. If y « updatepx, i, zq P S, then Mp`x q “ Mp`y q.
Proof. By congruence, we have that S |ù |y| « |updatepx, i, zq|, and by saturation
of L-Intro and the definition of Ó, we know that S |ù |updatepx, i, zq| « |x|. Thus,
S |ù |x| « |y|. By Assumption 1, S |ù `x « `y , so by saturation of S-Prop, we
have A |ù `x « `y . It follows from Definition 12 that Ap`x q “ Ap`y q, and thus,
Mp`x q « Mp`y q.
   We now turn to assigning values to variables of sort Seq. We will first associate a
sequence value with every sequence equivalence class (we write Mpeq for the value
associated with equivalence class e). Then, for each equivalence class e and for each
x P e, we define Mpxq :“ Mpeq. We start by defining lengths.
Definition 13 (Model construction: length of atomic variables). For each variable
x in an atomic equivalence class e of ”S , we constrain Mpeq to be a sequence of length
Mp`x q. (the elements of Mpeq are not defined yet).
    Note that because every atomic variable is in an atomic equivalence class, Defini-
tion 13 assigns a length to every atomic variable. In what follows, we denote the length
assigned to Mpeq in Definition 13 by `e .
    Next, we define model values for atomic variables. We start with equivalence classes
that contain unit-terms.
Definition 14. An equivalence class e of ”S is called a unit equivalence class if unitpxq P
e for some x.
Definition 15 (Model construction: atomic variables in unit equivalence classes).
For every atomic variable x such that x ”S unitpyq for some y, we set Mprxsq to be a
sequence of length 1 whose only element is set to Mpyq.


                                              24
    Next we turn to atomic equivalence classes that are not unit. We begin by defining
a graph in order to keep track of constraints that originate from the update symbol.
This definition is an adaptation of the weak equivalence graph from [10] to the context
of sequences, where operations are richer. In particular, we take into account not only
whether a constraint of the form y « updatepx, i, aq appears in S, but also whether x
and y are atomic, and whether the interpretation already given to i in Definition 12 is
within the range determined by the length assigned to x and y in Definition 13.

Definition 16 (Weak equivalence graph). Define a graph G “ pV, E, δq as follows.
V is the set of atomic equivalence classes. E Ď V ˆ V is a set of unordered edges,
and δ : E Ñ PpNq is a labeling function on edges, such that pe1 , e2 q P E and
k P δppe1 , e2 qq iff there are x P e1 and y P e2 such that y « updatepx, i, zq P S or
x « updatepy, i, zq P S, where Mpiq “ k and 0 ď k ă Mp`e1 q “ Mp`e2 q.

Definition 17 (Weak equivalence). Given a weak equivalence graph G “ pV, E, δq,
for each i P N, we define a binary relation „i over V as follows: e1 „i e2 iff there exists
a path p between e1 and e2 in G, such that for each edge d in p, δpdqztiu ‰ H.

    It is routine to verify that:

Lemma 8. For each i P N, „i is an equivalence relation over the atomic equivalence
classes of ”S .

Notice that even though „i is defined using update-terms, every atomic equivalence
class e satisfies e „i e, even if it has no update-terms.
      Let ` “ maxeP”S `e be the maximal sequence length assigned in Definition 13. Let
a11 , a21 , . . . , a`1 , a12 , . . . , a`2 , . . . be an enumeration of the elements in MpElemq that were
not assigned to any variable of Elem sort. For each i P r0, `q, let E1i , E2i , . . . , Eni i be an
enumeration of the equivalence classes of „i .
      By Lemma 8, we have:
Lemma 9. For every atomic equivalence class e of ”S , and for each i P r0, `e q, there
exists some j such that e P Eji .

Definition 18 (Model construction: atomic variables in non-unit equivalence classes).
 Let e be an atomic equivalence class of ”S that is not a unit equivalence class. We set
the ith element of Mpeq for every i P r0, `e q as follows. By Lemma 9, there exists some
j such that e P Eji .
 1. If there are e1 P Eji , s P e1 , x, and y such that x ”S nthps, yq and Mpyq “ i, we
     set the ith element of Mpeq to be Mpxq.
 2. Otherwise, the ith element of Mpeq is set to aij .

    Next, we set the interpretation of non-atomic variables of sort Seq.

Definition 19 (Model construction: non-atomic sequence variables). Let x be a
non-atomic variable of sort Seq, and let y be its normal form. Mprxsq is set to be the
concatenation of the interpretations of the variables in y (Mprxsq is the empty sequence
if y is of size 0).


                                                   25
    Finally, we define the interpretation of nth. Mpnthq is a function from MpSeqq ˆ
MpIntq to MpElemq. Given a P MpSeqq and an integer i, if i is non-negative and
smaller than the length of a, the value of Mpnthqpa, iq is fixed by the theory. The
following definition assigns a value to Mpnthqpa, iq when i is out of bounds.
Definition 20 (Model construction: nth terms). For every element a P MpSeqq with
length n and for every i P N such that i ă 0 or i ě n, if there are s, x, and y such that
x ”S nthps, yq, Mpsq “ a, and Mpyq “ i, Mpnthqpa, iq is set to Mpxq. Otherwise, it
is set arbitrarily.
    This concludes the construction of M.
Lemma 10. Definitions 10 to 13, 15 and 18 to 20 are well-defined.
     This lemma is proved in Appendix A.6, below.
     By construction, M is a TSeq -interpretation, and by Lemma 10 it is well-defined. It
is left to show that it satisfies A Y S. The arithmetic constraints are satisfied, by the fact
that A |ù A (see Definitions 11 and 12):
Lemma 11. M satisfies A.
    Showing that M |ù S is more involved. Roughly speaking, each possible shape
of a sequence constraint is considered separately, and for each, M is proved to satisfy
constraints of that shape from S. The cases that include nth and update terms heavily rely
on the construction of the weak equivalence graph. Constraints that include concatenation
are handled by reasoning about |ù`` .
Lemma 12. M satisfies S.
    This lemma will be proved in Appendix A.7.
    We conclude this section by reviewing the earlier example for the construction of M
with a few more details.
Example 6. Consider a signature in which Elem is Int, and a saturated configuration
pS˚ , A˚ q w.r.t. EXT that includes the following formulas: y « y1 `` y2 , x « x1 `` x2 ,
y2 « x2 , y1 « updatepx1 , i, aq, |y1 | “ |x1 |, |y2 | “ |x2 |, nthpy, iq « a, nthpy1 , iq « a.
Following the above construction, a satisfying interpretation M can be built as follows:
Definition 10 Set both MpIntq and MpElemq to be the set of integer numbers. MpSeqq
     is fixed by the theory.
Definition 12 First, find an arithmetic model, Mp`x q “ Mp`y q “ 4, Mp`y1 q “
     Mp`x1 q “ 2, Mp`y2 q “ Mp`x2 q “ 2, Mpiq “ 0. Further, set Mpaq “ 0.
Definition 13 Start assigning values to sequences. First, set the lengths of Mpxq and
     Mpyq to be 4, and the lengths of Mpx1 q, Mpx2 q, Mpy1 q, Mpy2 q to be 2.
Definition 18 Definition 15 is skipped as there are no unit terms. Next, according to
     Item 1, the 0th element of Mpy1 q is set to 0 (y1 is atomic, y is not.). According to
     Item 2, assign fresh values to the remaining indices of atomic variables. The result
     can be, e.g., Mpy1 q “ r0, 2s, Mpx1 q “ r1, 2s, Mpy2 q “ Mpx2 q “ r3, 4s.
Definition 19 Assign non-atomic sequence variables based on equivalent concatena-
     tions: Mpyq “ r0, 2, 3, 4s, Mpxq “ r1, 2, 3, 4s.
Definition 20 No integer variable in the formula was assigned an out-of-bound value,
     and so the interpretation of nth on out-of-bounds cases is set arbitrarily.


                                             26
A.6   Proof of Lemma 10
Lemma 10. Definitions 10 to 13, 15 and 18 to 20 are well-defined.

   Note that Definitions 10 and 11 are trivially well-defined. We now go through the
remaining definitions.

Lemma 13. Definition 12 is well-defined.

Proof. To show that Item 1 is well-defined, it suffices to note that by saturation of
A-Conf, A is TLIA -satisfiable. To show that Item 2 is well-defined, it suffices to establish
an infinite enumeration a1 , a2 , . . . of MpElemq, which is guaranteed to exist due to
Definition 10.

Lemma 14. Definition 13 is well-defined.

Proof. Let x, y P e. We show that Mp`x q “ Mp`y q. Since x ”S y, we have S |ù |x| «
|y|. By Assumption 1, we also have S |ù `x « `y . By saturation of S-Prop, we have
`x « `y P A, and hence, by Definition 12, Mp`x q “ Mp`y q.

Lemma 15. Definition 15 is well-defined.

Proof. We first show that `rxs is 1. To see this, note first that by saturation of L-Intro (and
Figure 3), we have S |ù |unitpyq| « 1. We also have `x « |x| P S by Assumption 1. It
follows that S |ù `x « 1, so `x « 1 P A by saturation of S-Prop. Thus, we must have
Ap`x q “ 1 in Definition 12, and thus Mp`x q “ 1. By Definition 13, we then have that
the length of Mprxsq must be 1.
    Next, suppose unitpyq, unitpzq P rxs. We prove Mpyq “ Mpzq. Since S |ù
unitpyq « unitpzq, we must have y « z P S, by saturation of U-Eq. Hence, y ”S z and
so by Definition 12, we have Mpyq “ Mpzq.

Lemma 16. Definition 18 is well-defined.

Proof. Let e be as in Definition 18. Suppose there are e1 , e2 P Eji , with s1 P e1 , s2 P e2 ,
and x1 , y 1 , x2 , y 2 such that x1 ”S nthps1 , y 1 q and x2 ”S nthps2 , y 2 q and Mpy 1 q “
Mpy 2 q “ i, with i P r0, `e q. We prove that Mpx1 q “ Mpx2 q.
    We first show that y 1 « y 2 P S. Clearly y 1 , y 2 P T pSq. Also, y 1 , y 2 P T pAq since
y « y 1 P A and y 2 « y 2 P A by saturation of S-Prop. It follows by saturation of S-A
 1

that either y 1 « y 2 P A or y 1 ff y 2 P A. Since Mpy 1 q “ Mpy 2 q, the latter cannot hold,
and so the former holds. Then, by saturation of A-Prop, we have y 1 « y 2 P S as well.
    Now, notice that e1 „i e2 . Hence, there exist e1 , . . . , en such that e1 “ e1 , en “ e2
and for k P r1, nq, ek and ek`1 are connected by an edge dk in G where δpdk qztiu ‰ H.
For every such k, we have that sk « updateps1k , yk , zk q P S or s1k « updatepsk , yk , zk q P
S for some sk P ek , s1k P ek`1 , integer variable yk , and Elem-variable zk . By Lemma 7,
Mp`sk q “ Mp`s1k q. And by Definition 13, `ek “ Mp`sk q and `ek`1 “ Mp`s1k q. It
follows that `e1 “ `e1 “ . . . “ `en “ `e2 . By a similar argument, because e „i e1 , we
have `e1 “ `e . We also have: p˚q Mpyk q ‰ i and p˚˚q Mpyk q P r0, `e q. Define s10 to be
an alias for s1 and then notice that for k P r1, nq, sk ”S s1k´1 because sk , s1k´1 are both
in ek .


                                              27
     We prove by induction that for k P r0, nq, nthps1 , y 1 q ”S nthps1k , y 1 q. For the base
case, we simply note that nthps1 , y 1 q and nthps10 , y 1 q are identical and nthps1 , y 1 q P T pSq.
For the induction step, suppose that nthps1 , y 1 q ”S nthps1k , y 1 q, where k P r0, n ´ 1q.
This implies nthps1k , y 1 q P T pSq, and we also know s1k ”S sk`1 . Recalling that sk`1 «
updateps1k`1 , yk`1 , zk`1 q P S or s1k`1 « updatepsk`1 , yk`1 , zk`1 q P S, we see that
the premises of Nth-Update are satisfied. By saturation of Nth-Update, then, there are
three possibilities.
 1. In the first case, A |ù y 1 ă 0 _ y 1 ě `s1k . We know from Definition 12 that Mpy 1 q “
     Apy 1 q and Mp`s1k q “ Ap`s1k q, so we must have Mpy 1 q ă 0 or Mpy 1 q ě Mp`s1k q.
     But Mpy 1 q “ i and i P r0, `e q, and we know that Mp`s1k q “ `ek`1 “ `e , so this
     case is not possible.
 2. In the second case, A |ù y 1 « yk`1 . This is also not possible because we know that
     Apy 1 q “ Mpy 1 q “ i ‰ Mpyk`1 q “ Apyk`1 q.
 3. We are thus left with the third option, in which nthpsk`1 , y 1 q ”S nthps1k`1 , y 1 q. But
     we know that s1k ”S sk`1 , so we also have nthps1k , y 1 q ”S nthps1k`1 , y 1 q. Then,
     by the induction hypothesis, nthps1 , y 1 q ”S nthps1k`1 , y 1 q, which completes the
     induction proof.
Letting k “ n ´ 1, we obtain nthps1 , y 1 q ”S nthps1n´1 , y 1 q. But s1n´1 P en and en “ e2 ,
so s1n´1 ”S s2 and nthps1 , y 1 q ”S nthps2 , y 1 q. Finally, since we showed above that
y 1 « y 2 P S, we have nthps1 , y 1 q ”S nthps2 , y 2 q, and thus x1 ”S x2 , which means that
Mpx1 q “ Mpx2 q by Definition 12.

Lemma 17. Definition 19 is well-defined.

Proof. y exists and is unique by Lemma 4. If y is a variable or a variable-concatenation
term, then uniqueness guarantees well-definedness. Further, each variable that occurs in
y is atomic by Lemma 4, and hence its value in M was already defined in Definitions 15
and 18.

    We prove that Definition 20 is well-defined, but first we prove some helper lemmas.
Recall that we write C |ùLIA ϕ to denote that every model of TLIA satisfying C also
satisfies ϕ. Intuitively, if ϕ can be derived from C using arithmetic reasoning, then
C |ùLIA ϕ.
                                                                 n
Lemma 18. If S |ù`` x « z and z is of size n, then A |ùLIA `x “ Σi“1 `zi .

Proof. The proof is by structural induction using Definition 6. For Item 1, clearly
A |ù `x « `x . For Item 2, we have S |ù`` x « t for some variable concatenation term
t “ t1 `` ¨ ¨ ¨ `` tn such that S |ù x « t. Therefore, S |ù |x| « |t|. By saturation of
                       n                                                             n
L-Intro, S |ù |x| « Σi“1   |ti |, and using Assumption 1, we get S |ù `x « Σi“1         `ti . By
                                      n
saturation of S-Prop, A |ù `x « Σi“1 `ti .
    Now suppose that S |ù`` x « pw `` y `` zqÓ and S |ù y « t, where t is  or
a variable concatenation term in T pSq. Let w “ pw1 , . . . , wm q and z “ pz1 , . . . , zn q,
                                                                                m
with m, n ě 0. By the induction hypothesis, we have that A |ùLIA `x « Σi“1          `wi ` `y `
  n
Σi“1 `zi . We consider two cases. (1) t “ : in this case, S |ù |y| « ||. Also, S |ù || “ 0
by saturation of L-Intro, so S |ù |y| “ 0, and thus A |ù `y “ 0 by saturation of S-Prop
                                                      m            n
and Assumption 1. It follows that A |ùLIA `x « Σi“1       `wi ` Σi“1  `zi . (2) t is a variable


                                                 28
concatenation term in T pSq: let t “ t1 `` . . . `` tk . We have S |ù |y| « |t|. Also,
            k
S |ù |t| “ Σi“1 |ti | by saturation of L-Intro. By saturation of S-Prop and Assumption 1
                              k                                    k
(and assuming wlog that Σi“1      `ti is the result of flattening Σi“1 |ti |), it follows that
            k                                 m            k         n
A |ù `y “ Σi“1 `ti . Thus, A |ùLIA `x « Σi“1 `wi ` Σi“1 `ti ` Σi“1       `zi .

Lemma 19. For every sequence variable x P S, if ` is the length of Mpxq, then
Mp`x q “ `.

Proof. If x is atomic, then ` “ Mp`x q by Definition 13. Suppose that x is non-atomic.
Let y be the normal form of x where y is of size n. Each element of y is atomic, so
                                                                                n
for i P r1, ns, the length of Mpyi q is Mp`yi q by Definition 13. Then, ` “ Σi“1   Mp`yi q
by Definition 19. Let z of length n be such that S |ù`` x « z and S |ù yi « zi for
i P r1, ns, which exists by Definition 6. By Lemma 18, we have that A |ùLIA `x «
  n
Σi“1  `zi . For each i P r1, ns, we know that because S |ù yi « zi , S |ù |yi | « |zi |, and
so by Assumption 1, S |ù `yi « `zi . Therefore, A |ù `yi « `zi by saturation of S-Prop.
                                             n
Then, we can conclude that A |ùLIA `x « Σi“1     `yi . Finally, we have Mp`x q “ Ap`x q “
  n                 n
Σi“1 Ap`yi q “ Σi“1 Mp`yi q “ `.


Lemma 20. Suppose k ”S nthpx, yq. Let i “ Mpyq, e “ rxs, and let `e be the length
of Mpxq. If e is atomic and i P r0, `e q, then the ith element of Mpxq is Mpkq.

Proof. We consider the following cases:
 1. e is a unit equivalence class: then, for some z, unitpzq P e. By Definition 15,
    we have that i “ 0 and Mpxq contains the single element Mpzq. We show that
    Mpzq “ Mpkq. Since nthpx, yq P T pSq and S |ù x « unitpzq, by saturation of
    Nth-Unit, there are two cases. In the first case, A |ù y ă 0 _ y ą 0, which, by
    Definition 12, is not possible since Mpyq “ i “ 0. So, we are left with the second
    case, in which nthpx, yq « z P S. It follows that z ”S k, so by Definition 12,
    Mpzq “ Mpkq.
 2. e is atomic but not a unit equivalence class: let j be such that e P Eji . Then, by
    Item 1 of Definition 18, the ith element of Mpeq must be Mpkq, and thus the ith
    element of Mpxq is Mpkq.


Lemma 21. Suppose k ”S nthpx, yq. Let i “ Mpyq, e “ rxs, and let `e be the length
of Mpxq. If i P r0, `e q, then the ith element of Mpxq is Mpkq.

Proof. If e is atomic, then we have the result by Lemma 20. Suppose e is not atomic.
Let y be the normal form of x.
 1. If y is empty, then by Definition 19, Mpxq is the empty sequence, so i P r0, `e q is
    always false, and the statement holds vacuously.
 2. Suppose y has a single element, y1 . By Definition 6, it’s clear that S |ù˚`` y1 « y1 .
    So, by saturation of C-Eq, we must have x « y1 P S. But y1 is atomic, so this
    contradicts the assumption that e is not atomic.
 3. Otherwise, y “ y1 `` ¨ ¨ ¨ `` yn , with n ě 2. Recall that nthpx, yq P T pSq. Thus,
    by saturation of Nth-Concat, one of its n ` 1 conclusions is applicable. In the first


                                             29
    case, we must have A |ù y ă 0 _ y ě `x . But we also know that Mpyq “ i is
    non-negative and is smaller than the length assigned to M pxq, which leads to a
    contradiction using Lemma 19. For the other cases, we have, for some k P r1, ns,
                k´1              k                                                k´1
    (1) A |ù Σj“1   `yj ď y ă Σj“1   `yj and (2) S |ù nthpx, yq « nthpyk , y ´ Σj“1   `yj q.
                                           k´1                          k
    By Definition 12, this means that Σj“1 Mp`yj q ď Mpyq ă Σj“1            Mp`yj q. Now,
    by Definition 19, Mpxq “ Mpy1 q `` ¨ ¨ ¨ `` Mpyn q, and by Lemma 19, the
                                                                      k´1
    length of Mpyj q is Mp`yj q for j P r1, ns. Let i1 “ Mpyq ´ Σj“1      Mp`yj q. Clearly,
    i1 P r0, Mp`yk qq, and element Mpyq of Mpxq is the same as element i1 of Mpyk q.
                                                      k´1
    Now, revisiting (2), let α be the term y ´ Σj“1       `yj , and let α̂ be the variable
    introduced for α when flattening the term nthpyk , αq. We have k ”S nthpx, yq, so
    k ”S nthpyk , α̂q by (2). Let i2 be Mpα̂q, and recall that yk is atomic and that the
    length of Mpyk q is Mp`yk q. By Lemma 20, we have that if i2 P r0, Mp`yk qq, then
    the i2 th element of Mpyk q is Mpkq. It remains to show that i1 “ i2 . To see this,
    note that S |ù α̂ « α. So, by saturation of S-Prop, we have A |ù α̂ « α. Then, by
                                               k´1
    Definition 12, i2 “ Mpα̂q “ Mpyq ´ Σj“1         Mp`yj q “ i1 .


Lemma 22. For all x, y, with x ff y P S, we have Mpxq ‰ Mpyq.

Proof. By Deq-Ext we have two cases. In the first, A |ù `x ‰ `y . So, by Definition 12,
Mp`x q ‰ Mp`y q. Thus, by Lemma 19, we have that the length of Mpxq is different
from the length of Mpyq, so Mpxq ‰ Mpyq.
    In the second case, we have (1) A |ù `x « `y ^ 0 ď i ă `x and (2) w1 «
nthpx, iq, w2 « nthpy, iq, w1 ff w2 P S, for some i, w1 , w2 . By (2) and saturation
of S-Conf, we know that w1 ıS w2 , so by Definition 12, Mpw1 q ‰ Mpw2 q. Let
n “ Mpiq and let ` be the length of Mpxq. By Definition 12, we have Mp`x q “ Mp`y q
and 0 ď n ă Mp`x q. So, by Lemma 19, we have that the lengths of Mpxq and Mpyq
are both equal to `, and n P r0, `q. Looking again at (2), we can apply Lemma 21 twice
to get that the nth element of Mpxq is Mpw1 q and the nth element of Mpyq is Mpw2 q.
We can then conclude that Mpxq ‰ Mpyq, as we know that Mpw1 q ‰ Mpw2 q.

    We can now show that Definition 20 is well-defined.

Lemma 23. Definition 20 is well-defined.

Proof. Suppose there are x, x1 , s, s1 , y, y 1 such that x ”S nthps, yq, x1 ”S nthps1 , y 1 q,
Mpsq “ Mps1 q “ a, and Mpyq “ Mpy 1 q “ i. We prove Mpxq “ Mpx1 q. Since
y, y 1 P T pSq, and they have sort Int, by saturation of S-Prop, we have that y « y, y 1 «
y 1 P A, and so y, y 1 P T pSq X T pAq. By saturation of S-A, either y ff y 1 P A or
y « y 1 P A. The first case is impossible since Mpyq “ Mpy 1 q. In the second case, we
have y « y 1 P A, and so y « y 1 P S by saturation of A-Prop. Now, by saturation of
Nth-Split, there are two options: either s ff s1 P S or s « s1 P S. The first is impossible
by Lemma 22, as Mpsq “ Mps1 q. On the other hand, if s « s1 P S, then since
x ”S nthps, yq and x1 ”S nthps1 , y 1 q, we also have x ”S x1 . Thus, by Definition 12, we
have Mpxq “ Mpx1 q.



                                             30
A.7     Proof of Lemma 12
Lemma 12. M satisfies S.

      We start with helper lemmas.

Lemma 24. x is atomic in S iff S |ù˚`` x « y for some atomic representative y.

Proof. ñ: Let y be the representative of rxs. By Definition 4, and because x ”S y and
x is atomic, y must also be atomic. We have S |ù`` x « x by Definition 6, and thus,
also by Definition 6, we have S |ù˚`` x « y.
    ð: Since y is atomic and x ”S y, it is easy to see by Definition 4 that x is also
atomic.

Lemma 25. If S |ù˚`` x « y, then Mpxq “ Mpy1 q `` . . . `` Mpyn q, where y has
size n ě 0.

Proof. If x is not atomic, then the result is immediate by Definition 19. If x is atomic,
then by Lemma 24 and uniqueness of normal forms (Lemma 4), n “ 1. Since x ”S y1 ,
and models are assigned by equivalence class in Definitions 15 and 18, it follows that
Mpxq “ Mpy1 q.

Lemma 26. S |ù x «  iff Mpxq has length 0.

Proof. ñ: If S |ù x « , then S |ù |x| « ||. By saturation of L-Intro, S |ù || “ 0. So,
by Assumption 1, S |ù `x « 0, and so, by saturation of S-Prop, we have `x « 0 P A.
Thus, by Definition 12, Mp`x q “ 0, and so the length of x is 0 by Lemma 19. ð: If
Mpxq has length 0, then by Lemma 19, Mp`x q “ 0. By saturation of L-Valid, either
x «  P S or A |ù `x ą 0. But the latter is impossible by Definition 12.

Lemma 27. If x « updatepy, i, vq P S, Mpiq P r0, Mply qq, and S |ù˚`` y « w1 ``
¨ ¨ ¨ `` wn , then:
  1. x « z1 `` ¨ ¨ ¨ `` zn P S for some atomic  z1 , . . . , zn ;
                                              řk´1                     řk
  2. there exists some k P r1, ns, such that j“1 Mp`wj q ď Mpiq ă j“1 Mp`wj q
                                                                  řk´1
       and zk “ updatepwk , αk , vq P S, where A |ù αk « i ´ j“1 `wj ; and
  3. for all j P r1, ns, j ‰ k, zj « wj P S.

Proof. By saturation w.r.t. Update-Concat, there is x « z1 `` ¨ ¨ ¨ `` zn P S, for some
z1 , . . . , zn , such that zm « updatepwm , αm , vq P S for m P r1, ns, where αm is the
                                       řm´1
variable introduced for the term i ´ j“1 `wj when flattening the term updatepwm , i ´
řm´1                                                                      řm´1
  j“1 `wj , vq. Then, zm « updatepwm , αm , vq P S and αm ”S i ´             l“1 `wl . By
                                                      řm´1
saturation of S-Prop, we also have A |ù αm « i ´ j“1 `wj .
      Next we prove that z1 , ..., zn are atomic. Suppose zm is not atomic for some m P
r1, ns. Note that we cannot have S |ù zm « : wm is atomic, so by Lemma 26, Mpwm q
has a nonzero length; then, by Lemma 7, Mpzm q has nonzero length, so S * zm « 
by Lemma 26. Let u be the normal form of zm . u cannot be empty because then, by
Lemma 25, the length of Mpzm q would be 0, so by Lemma 26, we would have zm « .
u cannot be of size 1 as then zm would be atomic by Lemma 24. Thus, u is of size at


                                           31
least 2. Now, by saturation of Update-Concat-Inv applied to zm « updatepwm , αm , vq,
we have wm « z 1 P S, u1 « updatepz11 , αm , vq P S, and u2 « updatepz21 , α1 , vq P S,
for some α1 where S |ù α1 “ αm ´ `u1 . By Lemma 7, we have Mp`u1 q “ Mp`z11 q and
Mp`u2 q « Mp`z21 q. But u1 and u2 are atomic, so by Lemma 26, their lengths cannot be
zero. By Lemma 19, then, the lengths of z11 and z21 are also nonzero. So S * z1 «  and
S * z2 «  by Lemma 26. Thus, z is not singular, which means that wm is not atomic,
which is a contradiction.                                    řk´1             řk
    Now, consider the following n ` 2 constraints: i ă 0, j“1 `wj ď i ă j“1 `wj
                          řn
for k P r1, ns, and i ě j“1 `wj . Exactly one of these holds in M, since it interprets
arithmetic symbols in the usual way by Definition
                                           řn        11.
    Suppose M |ù i ă 0 or M |ù i ě j“1 `wj . We know that Mpiq P r0, Mp`y qq,
so this case is impossible by Lemmas 19 and 25.
                                   řk´1                  řk
    Now, suppose that M |ù            j“1 `wj ď i ă       j“1 `wj for some k P r1, ns.
Clearly, Item 2 holds for this k. We know that Update-Bound is saturated   řw.r.t. zm «
                                                                            m´1
updatepwm , αm , vq P S for m P r1, ns. Recall also that A |ù αm « i ´ j“1 `wj . It
is easy to see that the first branch is inconsistent with M whenever m ‰ k. Thus, we
have zm « wm P S for m P r1, ns, m ‰ k.

Lemma 28. If x ”S unitpyq then x is atomic.

Proof. Note that S |ù |unitpyq| « 1 by saturation of L-Intro, and so we also have (˚)
S |ù |x| « 1. Assume x is not atomic. There are two cases. In the first case, x ”S . But
S |ù || « 0 by saturation of L-Intro, so by (˚) and saturation of S-Prop, this implies A |ù
0 « 1, which contradicts saturation of A-Conf. In the second case, there exists a variable
concatenation term x1 `` ¨ ¨ ¨ `` xn P T pSq such that S |ù x « x1 `` ¨ ¨ ¨ `` xn and
                                                                                 n
x1 `` ¨ ¨ ¨ `` xn is not singular in S. By Lemma 5, we know that A |ùLIA Σi“1       `xn ě 2.
But by (˚) and saturation of S-Prop and L-Intro, together with Assumption 1, we also
              n
have A |ù Σi“1  `xn “ 1, which also contradicts saturation of A-Conf.

Definition 21. Define S |ù1,3
                            `` x « t if there is a derivation of S |ù`` x « t without
using Item 2 of Definition 6.

Lemma 29. If S |ù˚`` x « y, where y has size n, then for some z of size n such that
zi ”S yi , i P r1, ns, S |ù1,3
                           `` x « z.

Proof. Since S |ù˚`` x « y, there is some z 1 such that zi1 ”S yi , i P r1, ns and
S |ù`` x « z 1 . Consider the derivation tree described in Lemma 3, and let D be the path
through the tree corresponding to the derivation of S |ù`` x « z 1 . If D has no application
of Item 2 of Definition 6, then the claim is proved by setting z to be z 1 . Otherwise, the
first node in D must use Item 2 of Definition 6 to derive S |ù`` x « t, where x « t P S.
Suppose that t is not singular. Then, it is possible to derive S |ù1,3
                                                                   `` x « t by starting with
S |ù1,3
      `` x « x and then applying Item 3 of Definition 6, using S |ù x « t. We can then
replace the root of D with this derivation to get a derivation showing S |ù1,3 `` x « z.
     Suppose, on the other hand, that t is singular. Suppose t “ t1 `` . . . `` tm . Without
loss of generality, assume that D eagerly applies Item 3 of Definition 6 m ´ 1 times,
each time using S |ù ti «  for some i P r1, ms, which is possible because t is singular.


                                            32
The resulting node is a derivation of S |ù`` x « tk for some variable tk . We consider
two cases.
 1. Suppose that tk is atomic with atomic representative v. Then, clearly we have
    S |ù˚`` x « v and S |ù˚`` tk « v, so by saturation of C-Eq, x ”S tk . By Lemma 4,
    we also have that y “ v. But then, let z “ x. Clearly, we have S |ù1,3     `` x « z.
    Furthermore, x ”S y, proving the claim.
 2. Suppose that tk is not atomic. Then D must continue after S |ù`` x « tk , and the
    next step must use Item 3 of Definition 6 using S |ù tk « t1 to derive S |ù`` x « t1 ,
    where t1 is  or a variable concatenation term in S that is not singular in S. But
    then, note that we can start with S |ù1,3
                                            `` tk « tk and apply the same step to get
         1,3        1
    S |ù`` tk « t . If we continue using the rest of the steps in derivation D, we can
    show that S |ù1,3          1                     ˚
                      `` tk « z , and therefore, S |ù`` tk « y. By saturation of C-Eq,
    we then have x ”S tk . But, since x ”S tk , this means that x ”S t1 . So, we can
    start with S |ù1,3                                                            1
                     `` x « x and apply Item 3 of Definition 6 using S |ù x « t to get
         1,3
    S |ù`` x « t1 . Using the same steps of that appear in D after tk « t1 , we can show
    S |ù1,3        1
         `` x « z , which proves the claim.



Lemma 30. Let x be a sequence variable. Suppose S |ù1,3
                                                    `` x « t and S |ù`` z «
pu `` x `` vqÓ. Then S |ù`` z « pu `` t `` vqÓ.

Proof. By induction on the number of derivation steps in |ù1,3                    1,3
                                                                `` that yield S |ù`` x « t
(see Definition 6). If this number is 1, then it must be by using Item 1 of Definition 6, so
x “ t and the result follows trivially. If this number is some n ` 1 ą 1, then consider
the first n steps of the derivation. Let S |ù1,3
                                               `` x « s be their result. By the induction
hypothesis, S |ù`` z « pu `` s `` vqÓ. Now, consider the n ` 1 step of the derivation.
It must replace some variable y in s by some term r, which results in t. Performing the
same step on S |ù`` z « pu `` s `` vqÓ results in S |ù`` z « pu `` t `` vqÓ.

Lemma 31. Let x1 , . . . , xk be sequence variables. Suppose S |ù`` x « x1 ``¨ ¨ ¨``xk ,
and for every i P r1, ks, S |ù˚`` xi « x1i `` ¨ ¨ ¨ `` xni i . Then S |ù˚`` x « x11 `` ¨ ¨ ¨ ``
xnk k .

Proof. We have S |ù`` x « x1 `` ¨ ¨ ¨ `` xk . Also, for every i P r1, ks, since S |ù˚``
xi « x1i `` ¨ ¨ ¨ `` xni i , we also have, by Lemma 29, S |ù1,3              1             ni
                                                                   `` xi « yi `` ¨ ¨ ¨ `` yi for
                    n              j        j
some yi1 , . . . , yi i such that yi ”S xi for every j P r1, ni s. Considering the case where
i “ 1, by Lemma 30 we get S |ù`` x « ppy11 `` ¨ ¨ ¨ `` y1n1 q `` x2 `` ¨ ¨ ¨ `` xk qÓ.
Continuing this way until i “ k, and by the properties of Ó, we obtain S |ù`` x «
py11 `` ¨ ¨ ¨ `` yknk qÓ. Since y11 , . . . , yknk are variables, we actually have S |ù`` x «
y11 `` ¨ ¨ ¨ `` yknk . And hence, S |ù˚`` x « x11 `` ¨ ¨ ¨ `` xnk k .

   Finally, we can conclude that M |ù S, by considering each shape of a literal in S
separately.

Proof of Lemma 12. Let ϕ P S. We prove that M |ù ϕ. By Assumption 1, ϕ is a flat
sequence constraint. We consider the possible shapes of ϕ.


                                              33
 1. ϕ is x « y, where x, y have sort Int: using rule S-Prop, x « y P A. By Lemma 11,
    M |ù ϕ.
 2. ϕ is x « y, where x, y have sort Elem: we know that x ”S y, so by Definition 12,
    Mpxq “ Mpyq. Thus, M |ù ϕ.
 3. ϕ is x « y where x, y have sort Seq: Definitions 13, 15, 18 and 19 are defined for
    equivalence classes. Since x and y are in the same equivalence class, M |ù ϕ.
 4. ϕ is x ff y where x, y have sort Int: by saturation of S-Prop, x « x, y « y P A.
    Hence, x, y P T pSq X T pAq. By saturation of S-A, we either have x « y P A or
    x ff y P A. In the first case, by saturation of A-Prop, we also have x « y P S, which
    is impossible by saturation of S-Conf. Hence, we have x ff y P A. By Lemma 11,
    M |ù ϕ.
 5. ϕ is x ff y where x, y have sort Elem: x is not equivalent to y w.r.t. ”S , so
    Definition 12 assigns them different values; thus, Mpxq ‰ Mpyq, and hence,
    M |ù ϕ.
 6. ϕ is x ff y where x, y have sort Seq: M |ù ϕ by Lemma 22.
 7. ϕ is x « y ` z, x « ´y, or x « n for some n P N: by saturation of S-Prop, ϕ P A,
    so M |ù ϕ by Lemma 11.
 8. ϕ is x « : we know that S |ù || “ 0 by saturation of L-Intro. Using Assumption 1,
    we get S |ù `x « 0, and so by saturation of S-Prop we have A |ù `x “ 0. It follows
    by Lemma 19 that Mpxq has length 0 and is thus the empty sequence.
 9. ϕ is x « unitpyq: By Lemma 28, rxs is atomic. Also, rxs is a unit equivalence class.
    Hence Mprxsq was defined in Definition 15 and was set to a sequence of size 1
    whose only element is Mpyq by Lemma 15. Therefore, M |ù x « unitpyq.
10. ϕ is x « |y|: we know that `y « |y| P S by Assumption 1, so `y « x P A by
    saturation of S-Prop. From Definition 12, it follows that Mp`y q “ Mpxq. But by
    Lemma 19, we also have Mp|y|q “ Mp`y q, so Mpxq “ Mp|y|q.
11. ϕ is x « x1 `` ¨ ¨ ¨ `` xn . Suppose that x1 , . . . , xn have the unique (by Lemma 4)
    normal forms S |ù˚`` x1 « u1 `` ¨ ¨ ¨ `` um1 , S |ù˚`` x2 « um1 `1 `` ¨ ¨ ¨ `` um2 ,
    . . ., S |ù˚`` xn « umn´1 `1 `` ¨ ¨ ¨ `` umn . By Item 2 of Definition 6, we know
    S |ù`` x « x1 ``¨ ¨ ¨``xn , so by Lemma 31, we have S |ù˚`` x « u1 ``¨ ¨ ¨``umn .
    By Lemma 25, then Mpxq “ Mpu1 q `` . . . `` Mpumn q. Also, by Lemma 25, for
    each i P r1, ns, Mpxi q “ Mpui q `` . . . `` Mpumi q. So, Mpx1 `` . . . `` xn q “
    Mpx1 q `` . . . `` Mpxn q “ Mpu1 q `` . . . `` Mpumn q “ Mpxq.
12. ϕ is x « nthpy, iq: We consider two cases:

    (a) Mpiq is negative or is not smaller than the length of Mpyq: applying Defini-
        tion 20 with Mpyq for a, Mpiq for i and x for itself, we get that M |ù ϕ.
    (b) Mpiq is non-negative and smaller than the length of Mpyq: By Lemma 21 with
        x for k, y for x and i for y, we have that the Mpiqth element of Mpyq is Mpxq.
        Therefore, M |ù ϕ.

13. ϕ is x « updatepy, i, zq: First, assume Mpiq is negative or not smaller than the
    length of Mpyq. In this case, the interpretation in M of updatepy, i, zq is Mpyq.
    Hence, we prove that Mpxq “ Mpyq. By saturation of Update-Bound, we have that
    either A |ù 0 ď i ă `y or x « y P S. The first case is impossible by Definitions 11
    and 12 and Lemma 19, and hence, the second case holds. We therefore have x ”S y,


                                           34
    and since the definitions of sequence variables are done by equivalence classes (see
    Definitions 15, 18 and 19), we have Mpxq “ Mpyq.
    Next, assume Mpiq is non-negative and smaller than the length of Mpyq (this also
    implies that Mpyq is not an empty sequence). By Lemma 7, we have Mp`x q “
    Mp`y q, and by Lemma 19, Mp|x|q “ Mp`x q and Mp|y|q “ Mp`y q. We consider
    the following cases:
    (a) rxs and rys are atomic in S: We show that for every j P r0, Mp`x qq, the jth
         element of Mpxq is the same as the jth element of Mpupdatepy, i, zqq.
         First, suppose j “ Mpiq. We show that the jth element of Mpxq is Mpzq. By
         saturation of Nth-Intro, we have nthpx, iq P T pSq. Since x « updatepy, i, zq P
         S, rule Nth-Update applies. Notice that its first and last branches are impos-
         sible: the first by our assumption on Mpiq and Definitions 11 and 12 and
         Lemma 19, and the last because it would require A |ù i ‰ i, but we know
         A * K by saturation of A-Conf. Hence, the middle branch applies, which means
         nthpx, iq « z P S. By Lemma 20, then, we know that the jth element of Mpxq
         is Mpzq.
         Suppose, on the other hand, that j ‰ Mpiq. This implies Mp`x q “ Mp`y q ě 2,
         so rxs and rys cannot be unit by Definition 15. Their values are thus set by
         Definition 18. Since x « updatepy, i, zq P S, by Definition 16, there is an edge
         d between rxs and rys with Mpiq P δpdq. It follows, because j ‰ Mpiq, that
         rxs „j rys by Definition 17. But then rxs and rys are in the same equivalence
         class of „j , so in either case of Definition 18, their jth value is set to the same
         value. Finally, because j ‰ Mpiq, the jth element of Mpupdatepy, i, zqq is
         (according to the semantics of update) the jth element of Mpyq.
    (b) Suppose S |ù˚`` y « w1 ``¨ ¨ ¨``wn . By Lemma 27, we have x « z1 ``¨ ¨ ¨``
                                                 řk´1                         řk
         zn P S for some atomic z1 , . . . , zn , j“1 Mp`wj q ď Mpiq ă j“1 Mp`wj q
         and zk “ updatepwk , αk , zq P S for some k P r1, ns, where A |ù αk «
               řk´1
         i ´ j“1 `wj , and for m P r1, ns, m ‰ k, zm « wm P S. Since Definitions 15
         and 18 assign equivalence classes, we also have Mpzm q “ Mpwm q.
         Since zk , wk are atomic, we have Mpzk q “ Mpupdatepwk , αk , zqq by Item 13a
                                                                řk´1
         above. By Lemma 11, we have Mpαk q “ Mpiq ´ j“1 Mp`wj q. By Item 11,
         above, Mpxq « Mpz1 q `` . . . `` Mpzn q. It follows that Mpxq “ Mpw1 q ``
         . . . `` Mpupdatepwk , αk , zqq `` . . . `` Mpwn q. By Lemma 24, we also have
         Mpyq “ Mpw1 q `` . . . `` Mpwn q, so Mpupdatepy, i, zqq “ Mpw1 q ``
                                                 řk´1
         . . .``MpupdateqpMpwk q, Mpiq´ j“1 Mp`wj q, Mpzqq``. . .``Mpwn q.
         It follows that Mpxq “ Mpupdatepy, i, zqq.
14. ϕ is x « extractpy, i, jq: By saturation w.r.t. R-Extract, we have two options.
    In the first, A |ù i ă 0 _ i ě `y _ j ď 0 and x «  P S. By Item 8, above, Mpxq
    is the empty sequence. By Lemmas 11 and 19, Mpiq ă 0 or Mpiq has at least the
    length of Mpyq or Mpjq ď 0. In each of these 3 cases, we get from the semantics of
    extract in TSeq that Mpextractq assigns the empty sequence w.r.t the inputs Mpyq,
    Mpiq and Mpjq. Hence in this case we get M |ù ϕ.
    In the second case, A |ù 0 ď i ă `y ^ j ą 0 ^ `k « i ^ `x « minpj, `y ´
    iq ^ `k1 « `y ´ `x ´ i and y « k `` x `` k 1 P S. We thus have Mpyq “
    Mpkq `` Mpxq `` Mpk 1 q by Item 11, above. Also, M |ù A, by Lemma 11.


                                             35
According to the semantics of extract in TSeq , since Mpiq, Mpjq ě 0, Mpiq is
smaller than the length of Mpyq, the value assigned in M to extractpy, i, jq is the
maximal sub-sequence of Mpyq that starts at index Mpiq and has length at most
Mpjq. Since M |ù y « k `` x `` k 1 with the appropriate length constraints (by
Lemma 19), we have that this sequence value is exactly Mpxq and hence, M |ù ϕ.




                                     36
