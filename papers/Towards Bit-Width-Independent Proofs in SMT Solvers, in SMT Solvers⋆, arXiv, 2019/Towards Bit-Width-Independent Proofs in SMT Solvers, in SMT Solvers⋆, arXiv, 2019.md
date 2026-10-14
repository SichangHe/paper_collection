                                                       Towards Bit-Width-Independent Proofs
                                                                 in SMT Solvers⋆

                                                   Aina Niemetz1 , Mathias Preiner1 , Andrew Reynolds2 , Yoni Zohar1,
                                                                   Clark Barrett1 , and Cesare Tinelli2
arXiv:1905.10434v3 [cs.LO] 28 Jun 2019




                                                                        1
                                                                          Stanford University, Stanford, USA
                                                                    2
                                                                        The University of Iowa, Iowa City, USA



                                                 Abstract. Many SMT solvers implement efficient SAT-based procedures for solv-
                                                 ing fixed-size bit-vector formulas. These approaches, however, cannot be used di-
                                                 rectly to reason about bit-vectors of symbolic bit-width. To address this shortcom-
                                                 ing, we propose a translation from bit-vector formulas with parametric bit-width
                                                 to formulas in a logic supported by SMT solvers that includes non-linear inte-
                                                 ger arithmetic, uninterpreted functions, and universal quantification. While this
                                                 logic is undecidable, this approach can still solve many formulas by capitalizing
                                                 on advances in SMT solving for non-linear arithmetic and universally quantified
                                                 formulas. We provide several case studies in which we have applied this approach
                                                 with promising results, including the bit-width independent verification of invert-
                                                 ibility conditions, compiler optimizations, and bit-vector rewrites.


                                         1 Introduction

                                         Satisfiability Modulo Theories (SMT) solving for the theory of fixed-size bit-vectors
                                         has received a lot of interest in recent years. Many applications rely on bit-precise rea-
                                         soning as provided by SMT solvers, and the number of solvers that participate in the
                                         corresponding divisions of the annual SMT competition is high and increasing. Al-
                                         though theoretically difficult (e.g., [14]), bit-vector solvers are in practice highly effi-
                                         cient and typically implement SAT-based procedures. Reasoning about fixed-size bit-
                                         vectors suffices for many applications. In hardware verification, the size of a circuit is
                                         usually known in advance, and in software verification, machine integers are treated
                                         as fixed-size bit-vectors, where the width depends on the underlying architecture. Cur-
                                         rent solving approaches, however, do not generalize beyond this limitation, i.e., they
                                         cannot reason about parametric circuits or machine integers of arbitrary size. This is a
                                         serious limitation when one wants to prove properties that are bit-width independent.
                                         Further, when reasoning about machine integers of a fixed but large size, as employed,
                                         for example, in smart contract languages such as Solidity [28], current approaches do
                                         not perform as well in the presence of expensive operations such as multiplication [15].
                                             To address this limitation we propose a general method for reasoning about bit-
                                         vector formulas with parametric bit-width. The essence of the method is to replace the
                                         ⋆
                                             This work was supported in part by DARPA (awards N66001-18-C-4012 and FA8650-18-2-
                                             7861), ONR (award N68335-17-C-0558), NSF (award 1656926), and the Stanford Center for
                                             Blockchain Research.
translation from fixed-size bit-vectors to propositional logic (which is at the core of
state-of-the-art bit-vector solvers) with a translation to the quantified theories of integer
arithmetic and uninterpreted functions. We obtain a fully automated verification process
by capitalizing on recent advances in SMT solving for these theories.
    The reliability of our approach depends on the correctness of the SMT solvers in
use. Interactive theorem provers, or proof assistants, such as Isabelle and Coq [20,29],
on the other hand, target applications where trust is of higher importance than automa-
tion, although substantial progress towards increasing the latter has been made in recent
years [5]. Our long-term goal is an efficient automated framework for proving bit-width
independent properties within a trusted proof assistant, which requires both a formal-
ization of such properties in the language of the proof assistant and the development of
efficient automated techniques to reason about these properties. This work shows that
state-of-the-art SMT solving combined with our encoding techniques make the latter
feasible. The next steps towards this goal are described in the final section of this paper.
    Translating a formula from the theory of fixed-size bit-vectors to the theory of in-
teger arithmetic is not straightforward. This is due to the fact that the semantics of
bit-vector operators are defined modulo the bit-width n, which must be expressed using
exponentiation terms 2n . Most SMT solvers, however, do not support unrestricted ex-
ponentiation. Furthermore, operators such as bit-wise and and or do not have a natural
representation in integer arithmetic. While they are definable in the theory of integer
arithmetic using β-function encodings (e.g., [10]), such a translation is expensive as it
requires an encoding of sequences into natural numbers. Instead, we introduce an unin-
terpreted function (UF) for each of the problematic operators and axiomatize them with
quantified formulas, which shifts some of the burden from arithmetic to UF reasoning.
We consider two alternative axiomatizations: a complete one relaying on induction, and
a partial (hand-crafted) one that can be understood as an under-approximation.
    To evaluate the potential of our approach, we examine three case studies that arise
from real applications where reasoning about bit-width independent properties is es-
sential. Niemetz et al. [19] defined invertibility conditions for bit-vector operators,
which they then used to solve quantified bit-vector formulas. However, correctness of
the conditions was only checked for specific bit-widths: from 1 to 65. As a first case
study, we consider the bit-width independent verification of these invertibility condi-
tions, which [19] left to future work. As a second case study, we examine the bit-width
independent verification of compiler optimizations in LLVM. For that, we use the Alive
tool [17], which generates verification conditions for such optimizations in the theory
of fixed-size bit-vectors. Proving the correctness of these optimizations for arbitrary
bit-widths would ensure their correctness for any language and underlying architecture
rather than specific ones. As a third case study, we consider the bit-width independent
verification of rewrite rules for the theory of fixed-size bit-vectors. SMT solvers for this
theory heavily rely on such rules to simplify the input. Verifying their correctness is
essential and is typically done by hand, which is both tedious and error-prone.
    To summarize, this paper makes the following contributions.

 – In Section 3, we study complete and incomplete encodings of bit-vector formulas
   with parametric bit-width into integer arithmetic.
 – In Section 4, we evaluate the effectiveness of both encodings in three case studies.
  Symbol                          SMT-LIB Syntax                    Sort
  ≈, 6≈                           =, distinct                       σ[n] × σ[n] → Bool
  <uBV , >uBV , <BV
                 s , >s
                       BV
                                  bvult, bvugt, bvslt, bvsgt        σ[n] × σ[n] → Bool
  ≤u , ≥u , ≤s , ≥BV
    BV      BV   BV
                       s          bvule, bvuge, bvsle, bvsge        σ[n] × σ[n] → Bool
  ∼ BV , −BV                      bvnot, bvneg                      σ[n] → σ[n]
  &BV , |BV , ⊕BV                 bvand, bvor, bvxor                σ[n] × σ[n] → σ[n]
  <<BV , >>BV , >>BVa             bvshl, bvlshr, bvashr             σ[n] × σ[n] → σ[n]
  +BV , ·BV , mod BV , div BV     bvadd, bvmul, bvurem, bvudiv      σ[n] × σ[n] → σ[n]
  [u : l]BV                       extract (0 ≤ l ≤ u < n)           σ[n] → σ[u−l+1]
  ◦BV                             concatenation                     σ[n] × σ[m] → σ[n+m]
               Table 1. Considered bit-vector operators with SMT-LIB 2 syntax.


 – As part of the invertibility conditions case study, we introduce conditional inverses
   for bit-vector constraints, thus augmenting [19] with concrete parametric solutions.


Related Work Bit-width independent bit-vector formulas were studied by Picora [22],
who introduced a formal language for bit-vectors of parametric width, along with a
semantics and a decision procedure. The language we use here is a simplified vari-
ant of that language. A unification-based algorithm for bit-vectors of symbolic lengths
is discussed by Bjørner and Picora [4]. Bit-width independent formulas are related to
parametric Boolean functions and circuits. An inductive approach for reasoning about
such formalisms was developed by Gupta and Fisher [12,11] by considering a Boolean
function for the base case of a circuit and another one for its inductive step. Reasoning
about equivalence of such circuits can be embedded in the framework of [22].


2 Preliminaries

We briefly review the usual notions and terminology of many-sorted first-order logic
with equality (denoted by ≈). See [10,30] for more detailed information. Let S be a set
of sort symbols, and for every sort σ ∈ S, let Xσ be an infinite set of variables of sort σ.
We assume that sets Xσ are pairwise disjoint and define X as the union of sets Xσ . A
signature Σ consists of a set Σ s ⊆ S of sort symbols and a set Σ f of function symbols.
Arities of function symbols are defined in the usual way. Constants are treated as 0-ary
functions. We assume that Σ includes a Boolean sort Bool and the Boolean constants
⊤ (true) and ⊥ (false). Functions returning Bool are also called predicates.
    We assume the usual definitions of well-sorted terms, literals, and formulas, and
refer to them as Σ-terms, Σ-literals, and Σ-formulas, respectively. We define x =
(x1 , ..., xn ) as a tuple of variables and write Qxϕ with Q ∈ {∀, ∃} for a quantified
formula Qx1 · · · Qxn ϕ. For a Σ-term or Σ-formula e, we denote the free variables of e
(defined as usual) as FV(e) and use e[x] to denote that the variables in x occur free in e.
For a tuple of Σ-terms t = (t1 , ..., tn ) and a tuple of Σ-variables x = (x1 , . . . , xn ), we
write e {x 7→ t} for the term or formula obtained from e by simultaneously replacing
each occurrence of xi in e by ti .
    A Σ-interpretation I maps: each σ ∈ Σ s to a distinct non-empty set of values σ I
(the domain of σ in I); each x ∈ Xσ to an element xI ∈ σ I ; and each f σ1 ···σn σ ∈ Σ f
to a total function f I : σ1I × ... × σnI → σ I if n > 0, and to an element in σ I if
n = 0. We use the usual inductive definition of a satisfiability relation |= between
Σ-interpretations and Σ-formulas.
    A theory T is a pair (Σ, I), where Σ is a signature and I is a non-empty class of Σ-
interpretations that is closed under variable reassignment, i.e., if interpretation I ′ only
differs from an I ∈ I in how it interprets variables, then also I ′ ∈ I. A Σ-formula ϕ
is T -satisfiable (resp. T -unsatisfiable) if it is satisfied by some (resp. no) interpretation
in I; it is T -valid if it is satisfied by all interpretations in I. We will sometimes omit T
when the theory is understood from context.
    The theory TBV = (ΣBV , IBV ) of fixed-size bit-vectors as defined in the SMT-
LIB 2 standard [3] consists of the class of interpretations IBV and signature ΣBV , which
includes a unique sort for each positive integer n (representing the bit-vector width), de-
noted here as σ[n] . For a given positive integer n, the domain σ[n] I of sort σ[n] in I is
the set of all bit-vectors of size n. We assume that ΣBV includes all bit-vector constants
of sort σ[n] for each n, represented as bit-strings. However, to simplify the notation we
will sometimes denote them by the corresponding natural number in {0, . . . , 2n − 1}.
All interpretations I ∈ IBV are identical except for the value they assign to variables.
They interpret sort and function symbols as specified in SMT-LIB 2. All function sym-
                                    f                                               s
bols (of non-zero arity) in ΣBV         are overloaded for every σ[n] ∈ ΣBV            . We denote a
ΣBV -term (or bit-vector term) t of width n as t[n] when we want to specify its bit-width
explicitly. We refer to the i-th bit of t[n] as t[i] with 0 ≤ i < n. We interpret t[0] as the
least significant bit (LSB), and t[n − 1] as the most significant bit (MSB), and denote
bit ranges over k from index j down to i as t[j : i]. The unsigned interpretation of
                                                                      n−1
a bit-vector t[n] as a natural number is given by [t]N = Σi=0             t [i] · 2i , and its signed
                                                                      n−1
interpretation as an integer is given by [t]Z = −t [n − 1] · 2            + [t[n − 2 : 0]BV ]N .
    Without loss of generality, we consider a restricted set of bit-vector function and
predicate symbols (or bit-vector operators) as listed in Table 1. The selection of op-
erators in this set is arbitrary but complete in the sense that it suffices to express all
                                                                            BV
bit-vector operators defined in SMT-LIB 2. We use maxBV          s [k] (mins [k] ) for the maximum
or minimum signed value of width k, e.g., maxs [4] = 0111 and minBV
                                                      BV
                                                                                s [4] = 1000.
    The theory TIA = (ΣIA , IIA ) of integer arithmetic is also defined as in the SMT-
LIB 2 standard. The signature ΣIA includes a single sort Int, function and predicate
symbols {+, −, ·, div, mod, |...|, <, ≤, >, ≥}, and a constant symbol for every integer
value. We further extend ΣIA to include exponentiation, denoted in the usual way as ab .
All interpretations I ∈ IIA are identical except for the values they assign to variables.
We write TUFIA to denote the (combined) theory of uninterpreted functions with integer
arithmetic. Its signature is the union of the signature of TIA with a signature containing
a set of (freely interpreted) function symbols, called uninterpreted functions.

2.1 Parametric Bit-Vector Formulas
We are interested in reasoning about (classes of) ΣBV -formulas that hold independently
of the sorts assigned to their variables or terms. We formalize the notion of parametric
ΣBV -formulas in the following.
     We fix two sets X ∗ and Z ∗ of variable and constant symbols, respectively, of bit-
vector sort of undetermined bit-width. The bit-width is provided by the first component
of a separate function pair ω = (ω b , ω N ) which maps symbols x ∈ X ∗ ∪ Z ∗ to ΣIA -
terms. We refer to ω b (x) as the symbolic bit-width assigned by ω to x. The second
component of ω is a map ω N from symbols z ∈ Z ∗ to ΣIA -terms. We call ω N (z) the
symbolic value assigned by ω to z. Let v = FV(ω) be the set of (integer) free variables
occurring in the range of either ω b or ω N . We say that ω is admissible if for every
interpretation I ∈ IIA that interprets each variable in v as a positive integer, and for
every x ∈ X ∗ ∪ Z ∗ , I also interprets ω b (x) as a positive integer.
     Let ϕ be a formula built from the function symbols of ΣBV and X ∗ ∪ Z ∗ , ignoring
their sorts. We refer to ϕ as a parametric ΣBV -formula. One can interpret ϕ as a class of
fixed-size bit-vector formulas as follows. For each symbol x ∈ X ∗ and integer n > 0,
we associate a unique variable xn of (fixed) bit-vector sort σ[n] . Given an admissible ω
with v = FV(ω) and an interpretation I that maps each variable in v to a positive inte-
ger, let ϕ|ω[I] be the result of replacing all symbols x ∈ X ∗ in ϕ by the corresponding
bit-vector variable xk and all symbols x ∈ Z ∗ in ϕ by the bit-vector constant of sort
σ[k] corresponding to ω N (x)I mod 2k , where in both cases k is the value of ω b (x)I .
We say a formula ϕ is well sorted under ω if ω is admissible and ϕ|ω[I] is a well-sorted
ΣBV -formula for all I that map variables in v to positive integers.

Example 1. Let X ∗ be the set {x} and Z ∗ be the set {z0 , z1 }, where ω N (z0 ) = 0 and
ω N (z1 ) = 1. Let ϕ be the formula (x +BVx) +BVz1 6≈ z0 . We have that ϕ is well sorted
under (ω b , ω N ) with ω b = {x 7→ a, z0 7→ a, z1 7→ a} or ω b = {x 7→ 3, z0 7→ 3, z1 7→
3}. It is not well sorted when ω b = {x 7→ a1 , z0 7→ a1 , z1 7→ a2 } since ϕ|ω[I] is not a
well sorted ΣBV -formula whenever aI1 6= aI2 . Note that an ω where ω b (x) = a1 − a2 is
not admissible, since (a1 − a2 )I ≤ 0 is possible even when aI1 > 0 and aI2 > 0.

    Notice that symbolic constants such as the maximum unsigned constant of a sym-
bolic length w can be represented by introducing z ∈ Z ∗ with ω b (z) = w and ω N (z) =
2w − 1. Furthermore, recall that signature ΣBV includes the bit-vector extract operator,
which is parameterized by two natural numbers u and l. We do not lift the above defini-
tions to handle extract operations having symbolic ranges, e.g., where u and l are ΣIA -
terms. This is for simplicity and comes at no loss of expressive power, since constraints
involving extract can be equivalently expressed using constraints involving concatena-
tion. For example, showing that every instance of a constraint s ≈ t[u : l]BV holds,
where 0 < l ≤ u < n − 1, is equivalent to showing that t ≈ y1 ◦BV(y2 ◦BVy3 ) ⇒ s ≈ y2
holds for all y1 , y2 , y3 , where y1 , y2 , y3 have sorts σ[n−1−u] , σ[u−l+1] , σ[l] , respectively.
We may reason about a formula involving a symbolic range {l, . . . , u} of t by consid-
ering a parametric bit-vector formula that encodes a formula of the latter form, where
the appropriate symbolic bit-widths are assigned to symbols introduced for y1 , y2 , y3 .
    We assume the above definitions for parametric ΣBV -formulas are applied to para-
metric ΣBV -terms as well. Furthermore, for any admissible ω, we assume ω can be
extended to terms t of bit-vector sort that are well sorted under ω such that t|ω[I] has
sort σ[ωb (t)I ] for all I that map variables in FV(ω) to positive integers. Such an exten-
sion of ω to terms can be easily computed in a bottom-up fashion by computing ω for
each child and then applying the typing rules of the operators in ΣBV . For example, we
may assume ω b (t) = ω b (t2 ) if t is of the form t1 +BVt2 and is well sorted under ω, and
ω b (t) = ω b (t1 ) + ω b (t2 ) if t is of the form t1 ◦BVt2 .
     Finally, we extend the notion of validity to parametric bit-vector formulas. Given
a formula ϕ that is well sorted under ω, we say ϕ is TBV -valid under ω if ϕ|ω[I] is
TBV -valid for all I that that map variables in FV(ω) to positive integers.


3 Encoding Parametric Bit-Vector Formulas in SMT
Current SMT solvers do not support reasoning about parametric bit-vector formulas.
In this section, we present a technique for encoding such formulas as formulas involv-
ing non-linear integer arithmetic, uninterpreted functions, and universal quantifiers. In
SMT parlance, these are formulas in the UFNIA logic. Given a formula ϕ that is well
sorted under some mapping ω, we describe this encoding in terms of a translation T ,
which returns a formula ψ that is valid in the theory of uninterpreted functions with
integer arithmetic only if ϕ is TBV -valid under ω. We describe several variations on this
translation and discuss their relative strengths and weaknesses.
Overall Approach At a high level, our translation produces an implication whose an-
tecedent requires the integer variables to be in the correct ranges (e.g., k > 0 for every
bit-width variable k), and whose conclusion is the result of converting each (parametric)
bit-vector term of bit-width k to an integer term. Operations on parametric bit-vector
terms are converted to operations on the integers modulo 2k , where k can be a symbolic
constant. We first introduce uninterpreted functions that will be used in our translation.
Note that SMT solvers may not support the full set of functions in our extended signa-
ture ΣIA , since they typically do not support exponentiation. Since translation requires
a limited form of exponentiation we introduce an uninterpreted function symbol pow2
of sort Int → Int, whose intended semantics is the function λx.2x when the argument
x is non-negative. Second, for each (non-predicate) n-ary (with n > 0) function f BV
of sort σ1 × . . . × σn → σ in the signature of fixed-size bit-vectors ΣBV (excluding
bit-vector extraction), we introduce an uninterpreted function f N of arity n + 1 and
sort Int × Int × . . . × Int → Int, where the extra argument is used to specify the bit-
width. For example, for +BV with sort σ[n] × σ[n] → σ[n] , we introduce +N of sort
Int × Int × Int → Int. In its intended semantics, this function adds the second and third
arguments, both integers, and returns the result modulo 2k , where k is the first argu-
ment. The signature ΣBV contains one function, bit-vector concatenation ◦BV , whose
two arguments may have different sorts. For this case, the first argument of ◦N indicates
the bit-width of the third argument, i.e., ◦N (k, x, y) is interpreted as the concatenation of
x and y, where y is an integer that encodes a bit-vector of bit-width k; the bit-width for
x is not specified by an argument, as it is not needed for the elimination of this opera-
tor we perform later. We introduce uninterpreted functions for each bit-vector predicate
in a similar fashion. For instance, ≥u N has sort Int × Int × Int → Bool and encodes
whether its second argument is greater than or equal to its third argument, when these
two arguments are interpreted as unsigned bit-vector values whose bit-width is given by
its first argument. Depending on the variation of the encoding, our translation will either
introduce quantified formulas that fully axiomatize the behavior of these uninterpreted
functions or add (quantified) lemmas that state key properties about them, or both.
  TA (ϕ, ω):
       Return AXA (ϕ, ω) ⇒ C ONV(ϕ, ω).
  C ONV (e, ω):
       Match e:
       x                       → χ(x)                                                         if x ∈ X ∗
                                   N                      b
       z                       → ω (z) mod pow2(ω (z))                                        if z ∈ Z ∗
       t1 ≈ t2                 → C ONV(t1 , ω) ≈ C ONV(t2 , ω)
       f BV (t1 , . . . , tn ) → E LIM(f N (ω b (tn ), C ONV(t1 , ω), . . . , C ONV(tn , ω)))
       ⊲⊳(ϕ1 , . . . , ϕn ) → ⊲⊳(C ONV(ϕ1 , ω), . . . , C ONV(ϕn , ω)) ⊲⊳ ∈ {∧, ∨, ⇒, ¬, ⇔}
  E LIM (e):
       Match e:
       +N (k, x, y)    → (x + y) mod pow2(k)
       −N (k, x, y)    → (x − y) mod pow2(k)
       ·N (k, x, y)    → (x · y) mod pow2(k)
       div N (k, x, y) → ite(y ≈ 0, pow2(k) − 1, x div y)
       mod N (k, x, y) → ite(y ≈ 0, pow2(k) − 1, x mod y)
       ∼ N (k, x)      → pow2(k) − (x + 1)
       −N (k, x)       → (pow2(k) − x) mod pow2(k)
       <<N (k, x, y) → (x · pow2(y)) mod pow2(k)
       >>N (k, x, y) → (x div pow2(y)) mod pow2(k)
       ◦N (k, x, y)    → x · pow2(k) + y
       ⊲⊳Nu (k, x, y)  → x ⊲⊳ y                           ⊲⊳ ∈ {<, ≤, >, ≥}
       ⊲⊳Ns (k, x, y)  → utsk (x) ⊲⊳ utsk (y)             ⊲⊳ ∈ {<, ≤, >, ≥}
       e               →e                                 otherwise

Fig. 1. Translation TA for parametric bit-vector formulas, parametrized by axiomatization
mode A. We use utsk (x) as shorthand for 2 · (x mod pow2(k − 1)) − x.


Translation Function Figure 1 defines our translation function TA , which is parame-
terized by an axiomatization mode A. Given an input formula ϕ that is well sorted under
ω, it returns the implication whose antecedant is an axiomatization formula AXA (ϕ, σ)
and whose conclusion is the result of converting ϕ to its encoded version via the conver-
sion function C ONV . The former is dependent upon the axiomatization mode A which
we discuss later. We assume without loss of generality that ϕ contains no applications
of bit-vector extract, which can be eliminated as described in the previous section, nor
does it contain concrete bit-vector constants, since these can be equivalently represented
by introducing a symbol in Z ∗ with the appropriate concrete mappings in ω b and ω N .
    In the translation, we use an auxiliary function C ONV which converts parametric bit-
vector expressions into integer expressions with uninterpreted functions. Parametric bit-
vector variables x (that is, symbols from X ∗ ) are replaced by unique integer variables of
type Int, where we assume a mapping χ maintains this correspondence, such that range
of χ does not include any variable that occurs in FV(ω). Parametric bit-vector constants
z (that is, symbols from set Z ∗ ) are replaced by the term ω N (z) mod pow2(ω b (z)). The
ranges of the maps in ω may contain arbitrary ΣIA -terms. In practice, our translation
handles only cases where these terms contain symbols supported by the SMT solver,
as well as terms of the form 2t , which we assume are replaced by pow2(t) during this
translation. For instance, if ω b (z) = w + v and ω N (z) = 2w − 1, then C ONV (z) returns
(pow2(w) − 1) mod pow2(w + v). Equalities are processed by recursively running
the translation on both sides. The next case handles symbols from the signature ΣBV ,
where symbols f BV are replaced with the corresponding uninterpreted function f N . We
take as the first argument ω b (tn ), indicating the symbolic bit-width of the last argument
of e, and recursively call C ONV on t1 , . . . , tn . In all cases, ω b (tn ) corresponds to the
bit-width that the uninterpreted function f N expects based on its intended semantics
(the bit-width of the second argument for bit-vector concatenation, or of an arbitrary
argument for all other functions and predicates). Finally, if the top symbol of e is a
Boolean connective we apply the conversion function recursively to all its children.
    We run E LIM for all applications of uninterpreted functions f N introduced during
the conversion, which eliminates functions that correspond to a majority of the bit-
vector operators. These functions can be equivalently expressed using integer arithmetic
and pow2. The ternary addition operation +N , that represents addition of two bit-vectors
with their width k specified as the first argument, is translated to integer addition mod-
ulo pow2(k). Similar considerations are applied for −N and ·N . For div N and mod N ,
our translation handles the special case where the second argument is zero, where the
return value in this case is the maximum value for the given bit-width, i.e. pow2(k) − 1.
The integer operators corresponding to unary (arithmetic) negation and bit-wise nega-
tion can be eliminated in a straightforward way. The semantics of various bitwise shift
operators can be defined arithmetically using division and multiplication with pow2(k).
Concatenation can be eliminated by multiplying its first argument x by pow2(k), where
recall k is the bit-width of the second arugment y. In other words, it has the effect of
shifting x left by k bits, as expected. The unsigned relation symbols can be directly
converted to the corresponding integer relation. For the elimination of signed relation
symbols we use an auxiliary helper uts (unsigned to signed), defined in Figure 1, which
returns the interpretation of its argument when seen as a signed value. The definition
of uts can be derived based on the semantics for signed and unsigned bit-vector values
in the SMT LIB standard. Based on this definition, we have that integers v and u that
encode bit-vectors of bit-width k satisfy <s N (k, u, v) if and only if utsk (u) < utsk (v).
    As an example of our translation, let ϕ = (x +BVx) +BVz1 6≈ z0 , ω N (z0 ) = 0,
ω (z1 ) = 1, and ω b (x) = ω b (z0 ) = ω b (z1 ) = a from Example 1. C ONV (ϕ, (ω b , ω N ))
  N

is E LIM(+N (a, E LIM (+N (a, χ(x), χ(x))), 1 mod pow2(a))) 6≈ 0 mod pow2(a). After
applying E LIM and simplifying, we get (χ(x) + χ(x) + 1) mod pow2(a) 6≈ 0.
    Thanks to E LIM, we can assume that all formulas generated by C ONV contain only
uninterpreted function symbols in the set {pow2, &N, |N , ⊕N }. Thus, we restrict our at-
tention to these symbols only in our axiomatization AXA , described next.

Axiomatization Modes We consider four different axiomatization modes A, which we
call full, partial, combined, and qf (quantifier-free). For each of these axiomatizations,
we define AXA (ϕ, ω) as the conjunction:
                                                                        N     |N       ⊕N
   ^                                   ^
        0 ≤ χ(x) < pow2(ω b (x)) ∧ (       w > 0) ∧ AXpow2 A   ∧ AX&  A ∧ AXA ∧ AXA
x∈FV(ϕ)                               w∈FV(ω)

The first conjunction states that all integer variables introduced for parametric bit-vector
variables x reside in the range specified by their bit-width. The second conjunction states
        ⋄ AX⋄full
      pow2 pow2(0) ≈ 1 ∧ ∀k. k > 0 ⇒ pow2(k) ≈ 2 · pow2(k − 1)
           ∀k, x, y. &N(k, x, y) ≈
         N
       &     ite(k > 1, &N (k − 1, x mod pow2(k − 1), y mod pow2(k − 1)), 0) +
             pow2(k − 1) · min(exk−1 (x), exk−1 (y))
           ∀k, x, y. ⊕N (k, x, y) ≈
       ⊕N    ite(k > 1, ⊕N (k − 1, x mod pow2(k − 1), y mod pow2(k − 1)), 0) +
             pow2(k − 1) · |exk−1 (x) − exk−1 (y)|
Table 2. Full axiomatization of pow2, &N, and ⊕N . The axiomatization of |N is omitted, and is
dual to that of &N. We use exi (x) for (x div pow2(i)) mod 2.


that all free variables in ω (denoting bit-widths) are positive. The remaining four con-
juncts denote the axiomatizations for the four uninterpreted functions that may occur
in the output of the conversion function. The definitions of these formulas are given in
Tables 2 and 3 for full and partial respectively. For each axiom, i, j, k denote bit-widths
and x, y denote integers that encode bit-vectors of size k. We assume guards on all quan-
tified formulas (omitted for brevity) that constrain i, j, k to be positive and x, y to be
in the range {0, . . . , pow2(k) − 1}. Each table entry lists a set of formulas (interpreted
conjunctively) that state properties about the intended semantics of these operators. The
formulas for axiomatization mode full assert the intended semantics of these operators,
whereas those for partial assert several properties of them. Mode combined asserts
both, and mode qf takes only the formulas in partial that are quantifier-free. In par-
ticular, AXpow2
             qf   corresponds to the base cases listed in partial, and AX⋄qf for the other
operators is simply ⊤. The partial axiomatization of these operations mainly includes
natural properties of them. For example, we include some base cases for each operation,
and also the ranges of its inputs and output. For some proofs, these are sufficient. For
      N
&N, | and ⊕N , we also included their behavior for specific cases, e.g., &N (k, a, 0) = 0
and its variants. Other axioms (e.g., “never even”) were added after analyzing specific
benchmarks to identify sufficient axioms for their proofs.
     Our translation satisfies the following key properties.

Theorem 2. Let ϕ be a parameteric bit-vector formula that is well sorted under ω and
has no occurrences of bit-vector extract or concrete bit-vector constants. Then:

 1. ϕ is TBV -valid under ω if and only if Tfull (ϕ, ω) is TUFIA -valid.
 2. ϕ is TBV -valid under ω if and only if Tcombined(ϕ, ω) is TUFIA -valid.
 3. ϕ is TBV -valid under ω if Tpartial (ϕ, ω) is TUFIA -valid.
 4. ϕ is TBV -valid under ω if Tqf (ϕ, ω) is TUFIA -valid.

    The proof of Property 1 is carried out by translating every interpretation I BV of
TBV into a corresponding interpretation I N of TUFIA such that I BV satisfies ϕ iff I N
satisfies Tfull (ϕ). The converse translation can be achieved similarly, where appropriate
bit-widths are determined by the range axioms 0 ≤ χ(x) < pow2(ω b (x)) that occur
in Tfull (ϕ, ω). The rest of the properties follow from Property 1, by showing that the
axioms in Table 3 are valid in every interpretation of TUFIA that satisfies AXfull (ϕ, ω).
  ⋄    axiom               AX⋄partial
       base cases          pow2(0) ≈ 1 ∧ pow2(1) ≈ 2 ∧ pow2(2) ≈ 4 ∧ pow2(3) ≈ 8
       weak monotonicity ∀i∀j. i ≤ j ⇒ pow2(i) ≤ pow2(j)
  pow2 strong monotonicity ∀i∀j. i < j ⇒ pow2(i) < pow2(j)
       modularity          ∀i∀j∀x. (x · pow2(i)) mod pow2(j) 6≈ 0 ⇒ i < j
       never even          ∀i∀x. pow2(i) − 1 6≈ 2 · x
       always positive     ∀i. pow2(i) ≥ 1
       div 0               ∀i. i div pow2(i) ≈ 0
       base case           ∀x∀y. &N(1, x, y) ≈ min(ex0 (x), ex0 (y))
       max                 ∀k∀x. &N(k, x, maxNk ) ≈ x
       min                 ∀k∀x. &N(k, x, 0) ≈ 0
    N
  &    idempotence         ∀k∀x. &N(k, x, x) ≈ x
       contradiction       ∀k∀x. &N(k, x, ∼ N (k, x)) ≈ 0
       symmetry            ∀k∀x∀y. &N(k, x, y) ≈&N(k, y, x)
       difference          ∀k∀x∀y∀z. x 6≈ y ⇒&N(k, x, z) 6≈ y∨ &N (k, y, z) 6≈ x
       range               ∀k∀x∀y. 0 ≤&N(k, x, y) ≤ min(x, y)
       base case           ∀x∀y. ⊕N (1, x, y) ≈ ite(ex0 (x) ≈ ex0 (y), 0, 1)
       zero                ∀k∀x. ⊕N (k, x, x) ≈ 0
  ⊕N one                   ∀k∀x. ⊕N (k, x, ∼ N (k, x)) ≈ maxNk
       symmetry            ∀k∀x∀y. ⊕N (k, x, y) ≈ ⊕N (k, y, x)
       range               ∀k∀x∀y. 0 ≤ ⊕N (k, x, y) ≤ maxNk
Table 3. Partial axiomatization of pow2, &N, and ⊕N . The axioms for |N are omitted, and are dual
to those for &N. We use maxNk for pow2(k) − 1.



4 Case Studies

We apply the techniques from Section 3 to three case studies: (i) verification of invert-
ibility conditions from Niemetz et al. [19]; (ii) verification of compiler optimizations
as generated by Alive [17]; and (iii) verification of rewrite rules that are used in SMT
solvers. For these case studies, we consider a set of verification conditions that origi-
nally use fixed-size bit-vectors, and exclude formulas involving multiple bit-widths.
     For each formula φ, we first extract a parametric version ϕ by replacing each vari-
able in φ by a fresh x ∈ X ∗ and each (concrete) bit-vector constant by a fresh z ∈ Z ∗ .
We define ω b (x) = ω b (z) = k for a fresh integer variable k, and let ω N (z) be the
integer value corresponding to the bit-vector constant it replaced. Notice that, although
omitted from the presentation, our translation can be easily extended to handle quan-
tified bit-vector formulas, which appear in some of the case studies. We then define
ω = (ω b , ω N ) and invoke our translation from Section 3 on the parametric bit-vector
formula ϕ. If the resulting formula is valid, the original verification condition holds in-
dependent of the original bit-width. In each case study, we report on the success rates
of determining the validity of these formulas for axiomatization modes full, partial,
combined, and qf. Overall, axiomatization mode combined yields the best results.
     All experiments described below require tools with support for the SMT logic UF-
NIA. We used all three participants in the UFNIA division of the 2018 SMT competi-
tion: CVC4 [2] (GitHub master 6eb492f6), Z3 [8] (version 4.8.4), and Vampire [13]
(GitHub master d0ea236). Z3 and CVC4 use various strategies and techniques for
quantifier instantiation including E-matching [18], and enumerative [24] and conflict-
based [27] instantiation. For non-linear integer arithmetic, CVC4 uses an approach
based on incremental linearization [7,6,26]. Vampire is a superposition-based theorem
prover for first-order logic based on the AVATAR framework [31], which has been ex-
tended also to support some theories including integer arithmetic [23]. We performed
all experiments on a cluster with Intel Xeon E5-2637 CPUs with 3.5GHz and 32GB
of memory and used a time limit of 300 seconds (wallclock) and a memory limit of
4GB for each solver/benchmark pair. We consider a bit-width independent property to
be proved if at least one solver proved it for at least one of the axiomatization modes.3

4.1 Verifying Invertibility Conditions
Niemetz et al. [19] present a technique for solving quantified bit-vector formulas that
utilizes invertibility conditions to generate symbolic instantiations. Intuitively, an in-
vertibility condition φc for a literal ℓ[x] is the exact condition under which ℓ[x] has a
solution for x, i.e., φc ⇔ ∃x.ℓ[x]. For example, consider bit-vector literal x &BV s ≈ t
with x 6∈ FV(s) ∪ FV(t); then, the invertibility condition for x is t &BVs ≈ t.
     The authors define invertibility conditions for a representative set of literals having
a single occurrence of x, that involve the bit-vector operators listed in Table 1, exclud-
ing extraction, as the invertibility condition for the latter is trivially ⊤. A considerable
number of these conditions were determined by leveraging syntax-guided synthesis (Sy-
GuS) techniques [1]. The authors further verified the correctness of all conditions for
bit-widths 1 to 65. However, a bit-width-independent formal proof of correctness of
these conditions was left to future work. In the following, we apply the techniques of
Section 3 to tackle this problem. Note that for this case study, we exclude operators
involving multiple bit-widths, namely bit-vector extraction and concatenation. For the
former, all invertibility conditions are ⊤, and for the latter a hand-written proof of the
correctness of its invertibility conditions can be achieved easily.

Proving Invertibility Conditions Let ℓ[x] be a bit-vector literal of the form ⋄x ⊲⊳ t or
x ⋄ s ⊲⊳ t (dually, s ⋄ x ⊲⊳ t) with operators ⋄ and relations ⊲⊳ as defined in Table 1. To
prove the correctness of an invertibility condition φc for x independent of the bit-width,
we have to prove the validity of the formula:
                                       φc ⇔ ∃x.ℓ[x]                                       (1)
where occurrences of s and t are implicitly universally quantified. We then want to
prove that Equation (1) is TBV -valid under ω. Considering the two directions of (1)
separately, we get:
                               ∃x.ℓ[x, s, t] ⇒ φc [s, t]                        (rtl)
                                  φc [s, t] ⇒ ∃x.ℓ[x, s, t]                              (ltr)
The validity of (rtl) is equivalent to the unsatisfiability of the quantifier-free formula:
                                    ℓ[x, s, t] ∧ ¬φc [s, t]                             (rtl’)
 3
     All benchmarks, results, log files, and solver configurations are available              at
     http://cvc4.cs.stanford.edu/papers/CADE2019-BVPROOF/.
Eliminating the quantifier in (ltr) is much trickier. It typically amounts to finding a
symbolic value for x such that ℓ[x, s, t] holds provided that φc [s, t] holds. We refer to
such a symbolic value as a conditional inverse.

Conditional Inverses Given an invertibility condition φc for x in bit-vector literal
ℓ[x], we say that a term αc is a conditional inverse for x if φc ⇒ ℓ[αc ] is TBV -valid. For
                                                                             BV
example, the term s itself is a conditional inverse for x in the literal (x | s) ≤uBV t: given
                                         BV                               BV
that there exists some x such that (x | s) ≤u t, we have that (s | s)≤uBV t. When a
                                                 BV

conditional inverse αc for x is found, we may replace (ltr) by:

                                        φc ⇒ ℓ[αc ]                                     (ltr’)

Clearly, (ltr’) implies (ltr). However, the converse may not hold, i.e., if (ltr’) is refuted,
(ltr) is not necessarily refuted. Notice that if the invertibility condition for x is ⊤, the
conditional inverse is in fact unconditional. The problem of finding a conditional inverse
for a bit-vector literal x⋄s ⊲⊳ t (dually, s⋄x ⊲⊳ t) can be defined as a SyGuS problem by
asking whether there exists a binary bit-vector function C such that the (second-order)
formula ∃C∀s∀t.φc ⇒ C(s, t) ⋄ s ⊲⊳ t is satisfiable. If such a function C is found,
then it is in fact a conditional inverse for x in ℓ[x]. We synthesized conditional inverses
for x in ℓ[x] for bit-width 4 with variants of the grammars used in [19] to synthesize
invertibility conditions. For each grammar we generated 160 SyGuS problems, one for
each combination of bit-vector operator and relation from Table 1 (excluding extraction
and concatenation), counting commutative cases only once. We used the SyGuS feature
of the SMT solver CVC4 [25] to solve these problems, and out of 160, we were able to
synthesize candidate conditional inverses for 143 invertibility conditions. For 12 out of
these 143, we found that the synthesized terms were not conditional inverses for every
bit-width, by checking (ltr’) for bit-widths up to 64.

Results Table 4 provides detailed information on the results for the axiomatization
                                                                          →
modes full, partial, and qf discussed in Section 3. We use → and to indicate that
only direction left-to-right (ltr or ltr’) or right-to-left (rtl’), respectively, were proved,
and X and ✕ to indicate that both or none, respectively, of the directions were proved.
Additionally, we use →αc (resp. →no αc ) to indicate that for direction left-to-right, for-
mula (ltr’) (resp. (ltr)) was proved with (resp. without) plugging in a conditional inverse.
    Overall, out of 160 invertibility conditions, we were able to fully prove 110, and for
19 (17) conditions we were able to prove only direction rtl’ (ltr’). For direction right-
to-left, 129 formulas (rtl’) overall were successfully proved to be unsatisfiable. Out of
these 129, 32 formulas were actually trivial since the invertibility condition φc was ⊤.
For direction left-to-right, overall, 127 formulas were proved successfully, and out of
these, 102 (94) were proved using (resp. not using) a conditional inverse. Furthermore,
33 formulas could only be proved when using a conditional inverse. Thus, using condi-
tional inverses was helpful for proving the correctness of invertibility conditions.
    Considering the different axiomatization modes, overall, with 104 fully proved and
only 17 unproved instances, combined performed best. Interestingly, even though ax-
iomatization qf only includes some of the base cases of axiomatization partial, it still
performs well. This may be due to the fact that in many cases, the correctness of the
                                         →
         Axiomatization          X              →       ✕         →αc       →no αc
                     full        64      18     22      56         72           51
                partial          76      14     26      44         78           81
                      qf         40      22     22      76         50           51
             combined           104      21     18      17         99           79
             Total (160)        110      19     17      14        102           94
Table 4. Invertibility condition verification using axiomatization modes combined, full, partial,
and qf. Column →αc (→no αc ) counts left-to-right proved with (without) conditional inverse.


invertibility condition does not rely on any particular property of the operators involved.
For example, the invertibility condition φc for literal x &BVs ≈ t is t &BVs ≈ t. Proving
the correctness of φc amounts to coming up with the right substitution for x, without
relying on any particular axiomatization of &N. In contrast, the invertibility condition φc
for literal x &BV s 6≈ t is t 6≈ 0 ∨ s 6≈ 0. Proving the correctness of φc relies on ax-
ioms regarding &BV and ∼ BV . Specifically, we have found that from partial, it suffices
to keep “min” and “idempotence” to prove φc . Overall, from the 2696 problems that
this case study included, CVC4 proved 50.3%, Vampire proved 31.4%, and Z3 proved
33.8%, while 23.5% of the problems were proved by all solvers.

4.2 Verifying Alive Optimizations
Lopes et al. [17] introduces Alive, a tool for proving the correctness of compiler peep-
hole optimizations. Alive has a high-level language for specifying optimizations. The
tool takes as input a description of an optimization in this high-level language and then
automatically verifies that applying the optimization to an arbitrary piece of source
code produces optimized target code that is equivalent under a given precondition. It
can also automatically translate verified optimizations into C++ code that can be linked
into LLVM [16]. For each optimization, Alive generates four constraints that encode
the following properties, assuming that the precondition of the optimization holds:
 1. Memory Source and Target yield the same state of memory after execution.
 2. Definedness The target is well-defined whenever the source is.
 3. Poison The target produces so-called poison values (caused by LLVM’s nsw, nuw,
    and exact attributes) only when the source does.
 4. Equivalence Source and target yield the same result after execution.
From these verification tasks, Alive can generate benchmarks in SMT-LIB 2 format in
the theory of fixed-size bit-vectors, with and without quantifiers. For each task, types
are instantiated with all possible valid type assignments (for integer types up to a default
bound of 64 bits). In the following, we apply our techniques from Section 3 to prove
Alive verification tasks independently from the bit-width. For this, as in the Alive paper,
we consider the set of optimizations from the instcombine optimization pass of LLVM,
provided as Alive translations (433 total).4 Of these 433 optimizations, 113 are depen-
dent on a specific bit-width; thus we focus on the remaining 320. We further exclude
optimizations that do not comply with the following criteria:
 4
     At https://github.com/nunoplopes/alive/tree/master/tests/instcombine
             Family      Considered                            Proved
                                              full   partial     qf   combined      Total
      AddSub (52)                  16           7          7      7          9         9
  MulDivRem (29)                    5           1          2      1          3         3
   AndOrXor (162)                 124          57        55      53         60        60
        Select (51)                26          15        11      11         16        16
         Shifts (17)                9           0          0      0          0         0
LoadStoreAlloca (9)                 0           0          0      0          0         0
        Total (320)               180          80        75      72         88        88
Table 5. Alive optimizations verification using axiomatizations combined, full, partial and qf.


 – In each generated SMT-LIB 2 file, only a single bit-width is used.
 – All SMT-LIB 2 files generated for a property (instantiated for all possible valid
   type assignments) must be identical modulo the bit-width (excluding, e.g., bit-width
   dependent constants other than 0, 1, (un)signed min/max, and the bit-width).
As a useful exception to the first criterion, we included instances where all terms of bit-
width 1 can be interpreted as Boolean terms. Overall, we consider bit-width independent
verification conditions 1–4 for 180 out of 320 optimizations. None of these include
memory operations or poison values, and only some have definedness constraints (and
those are simple). Hence, the generated verification conditions 1–3 are trivial. We thus
only consider the equivalence verification conditions for these 180 optimizations.

Results Table 5 summarizes the results of verifying the equivalence constraints for the
selected 180 optimizations from the instcombine LLVM optimization pass. It first lists
all families, showing the number of bit-width independent optimizations per family
(320 total). The next column indicates how many in each family were in the set of
180 considered optimizations, and the remaining columns show how many of those
considered were proved with each axiomatization mode.
     Overall, out of 180 equivalence verification conditions, we were able to prove 88.
Our techniques were most successful for the AndOrXor family. This is not too surpris-
ing, since many verification conditions of this family require only Boolean reasoning
and basic properties of ordering relations that are already included in the theory TIA .
For example, given bit-vector term a and bit-vector constants C1 and C2 , optimization
AndOrXor:979 essentially rewrites (a <BV                   BV            BV
                                              s C1 ∧ a <s C2 ) to a <s C1 , provided that
                     BV
precondition C1 <s C2 holds. To prove its correctness, it suffices to apply the transi-
tivity of <BV
            s with Boolean reasoning. The same holds when lifting this equivalence to
the integers, deducing the transitivity of <s N from that of the builtin < relation of TIA .
     None of the 9 benchmarks from the Shifts family were proven. These benchmarks
are more complicated than others. They combine bit-wise and arithmetical operations
and thus rely on their axiomatization. Solving these benchmarks is an interesting chal-
lenge for future work. Adding specialized axioms to partial is one promising approach.
     Interestingly, for this case study, the results from the different axiomatization modes
are very similar. This can again be explained by the fact that many optimizations rely
on properties of the integers that are already included in TIA , without requiring any
particular property of functions pow2, &N, |N and ⊕N (as in the above example).
    Note that we have also tried using our approach for proving the equivalence verifica-
tion conditions for up to a bit-width of 64. However, all optimizations that were proven
correct this way were already proven correct for arbitrary bit-widths, which suggests
that this restriction did not make the benchmarks easier. Overall, from the 720 prob-
lems in this case study, CVC4 proved 42.6%, Vampire proved 36.2%, and Z3 proved
37.9%, while 32.5% of the problems were proved by all solvers.


4.3 BV Rewriting

SMT solvers for the theory of fixed-size bit-vectors heavily rely on rewriting to reduce
the size of the input formula prior to solving the problem. Since these rewrite rules
are usually implemented independently of the bit-width, verifying that they hold for
any bit-width is crucial for the soundness of the solver. For this case study, we used
a feature of the SyGuS solver in CVC4 that allows us to enumerate equivalent bit-
vector terms/formulas (rewrite candidates) for a certain bit-width up to a certain term
depth (nesting level of operators) [21]. We generated 1575 pairs of equivalent bit-vector
terms of depth three and 431 equivalent pairs of formulas of depth two for bit-width 4
and translated them to integer problems with axiomatization modes full, partial, qf, and
combined, resulting in 6300 + 1724 = 8024 benchmarks in total. Since rewrites that
have been proved can be used to further axiomatize the integer translation, we collected
all proven rewrites after each run, added them as axioms to the initial problems and
reran the experiments. This was repeated until we reached a fixpoint, i.e., no further
rewrites were proved. With this approach, we were able to prove 409 out of the 435
formula equivalences (94%), reaching a fixpoint at the first iteration. For the equivalent
terms, we initially proved 878 out of the 1575 equivalences, which increased to 935
(59%) after adding all axioms from the first run, reaching a fixpoint after two iterations.
Overall, from the 8024 problems, CVC4 proved 64.2%, Vampire proved 66.5%, and Z3
proved 64.2%, while 63.8% of the problems were proved by all solvers.


5 Conclusion and Further Research

We have studied several translations from bit-vector formulas with parametric bit-width
to the theories of integer arithmetic and uninterpreted functions. The translations differ
in the way that the operator 2( ) and bitwise logical operators are axiomatized, namely,
fully (using induction) or partially (using some of their key properties). Our empiri-
cal results show that state-of-the-art SMT solvers are capable of solving the translated
formulas for various benchmarks that originate from the verification of invertibility
conditions, LLVM optimizations, and rewriting rules for fixed-size bit-vectors.
    In future research, we plan to investigate a translation of our results to a proof as-
sistant such as Coq, for which a bit-vector library was recently developed [9]. This will
involve supporting proofs in the SMT solver for non-linear arithmetic and quantifiers.
We believe that our promising experimental results with an integer encoding indicate
that this is a viable approach for automating bit-width independent proofs. We also plan
to explore satisfiable benchmarks, and to extend our approach for translating models.
References
 1. Alur, R., Bodı́k, R., Juniwal, G., Martin, M.M.K., Raghothaman, M., anjit A. Seshia, S.,
    Singh, R., Solar-Lezama, A., Torlak, E., Udupa, A.: Syntax-guided synthesis. In: Formal
    Methods in Computer-Aided Design, FMCAD 2013, Portland, OR, USA, October 20-23,
    2013. pp. 1–8 (2013)
 2. Barrett, C., Conway, C.L., Deters, M., Hadarean, L., Jovanović, D., King, T.,
    Reynolds, A., Tinelli, C.: CVC4. In: Proceedings of the 23rd International Confer-
    ence on Computer Aided Verification. pp. 171–177. CAV’11, Springer-Verlag (2011),
    http://dl.acm.org/citation.cfm?id=2032305.2032319
 3. Barrett, C., Stump, A., Tinelli, C.: The SMT-LIB Standard: Version 2.0. In: Gupta, A., Kroen-
    ing, D. (eds.) Proceedings of the 8th International Workshop on Satisfiability Modulo Theo-
    ries (Edinburgh, UK) (2010)
 4. BjØrner, N.S., Pichora, M.C.: Deciding fixed and non-fixed size bit-vectors. In: Steffen, B.
    (ed.) Tools and Algorithms for the Construction and Analysis of Systems. pp. 376–392.
    Springer Berlin Heidelberg, Berlin, Heidelberg (1998)
 5. Blanchette, J.C., Böhme, S., Paulson, L.C.: Extending sledgehammer with SMT solvers.
    J. Autom. Reasoning 51(1), 109–128 (2013). https://doi.org/10.1007/s10817-013-9278-5,
    https://doi.org/10.1007/s10817-013-9278-5
 6. Cimatti, A., Griggio, A., Irfan, A., Roveri, M., Sebastiani, R.: Experimenting on solving non-
    linear integer arithmetic with incremental linearization. In: SAT. Lecture Notes in Computer
    Science, vol. 10929, pp. 383–398. Springer (2018)
 7. Cimatti, A., Griggio, A., Irfan, A., Roveri, M., Sebastiani, R.: Incremental linearization
    for satisfiability and verification modulo nonlinear arithmetic and transcendental functions.
    ACM Trans. Comput. Log. 19(3), 19:1–19:52 (2018)
 8. De Moura, L., Bjørner, N.: Z3: An efficient smt solver. In: Proceedings of the Theory and
    Practice of Software, 14th International Conference on Tools and Algorithms for the Con-
    struction and Analysis of Systems. pp. 337–340. TACAS’08/ETAPS’08, Springer-Verlag
    (2008), http://dl.acm.org/citation.cfm?id=1792734.1792766
 9. Ekici, B., Mebsout, A., Tinelli, C., Keller, C., Katz, G., Reynolds, A., Barrett, C.: Smtcoq: a
    plug-in for integrating smt solvers into coq. In: International Conference on Computer Aided
    Verification. pp. 126–133. Springer (2017)
10. Enderton, H., Enderton, H.B.: A mathematical introduction to logic. Elsevier (2001)
11. Gupta, A., Fisher, A.L.: Parametric circuit representation using inductive boolean functions.
    In: Courcoubetis, C. (ed.) Computer Aided Verification. pp. 15–28. Springer Berlin Heidel-
    berg, Berlin, Heidelberg (1993)
12. Gupta, A., Fisher, A.L.: Representation and symbolic manipulation of lin-
    early inductive boolean functions. In: Proceedings of the 1993 IEEE/ACM
    International Conference on Computer-aided Design. pp. 192–199. IC-
    CAD ’93, IEEE Computer Society Press, Los Alamitos, CA, USA (1993),
    http://dl.acm.org.stanford.idm.oclc.org/citation.cfm?id=259794.259827
13. Kovács, L., Voronkov, A.: First-order theorem proving and vampire. In: CAV. Lecture Notes
    in Computer Science, vol. 8044, pp. 1–35. Springer (2013)
14. Kovásznai, G., Fröhlich, A., Biere, A.: Complexity of fixed-size bit-vector logics. The-
    ory Comput. Syst. 59(2), 323–376 (2016). https://doi.org/10.1007/s00224-015-9653-1,
    https://doi.org/10.1007/s00224-015-9653-1
15. Kroening, D., Strichman, O.: Decision Procedures - An Algorithmic Point of View, Second
    Edition. Texts in Theoretical Computer Science. An EATCS Series, Springer (2016)
16. Lattner, C., Adve, V.S.: LLVM: A compilation framework for lifelong program anal-
    ysis & transformation. In: 2nd IEEE / ACM International Symposium on Code Gen-
    eration and Optimization (CGO 2004), 20-24 March 2004, San Jose, CA, USA.
    pp. 75–88. IEEE Computer Society (2004). https://doi.org/10.1109/CGO.2004.1281665,
    https://doi.org/10.1109/CGO.2004.1281665
17. Lopes, N.P., Menendez, D., Nagarakatte, S., Regehr, J.: Provably correct peep-
    hole optimizations with alive. In: Proceedings of the 36th ACM SIGPLAN Con-
    ference on Programming Language Design and Implementation. pp. 22–32. PLDI
    ’15, ACM, New York, NY, USA (2015). https://doi.org/10.1145/2737924.2737965,
    http://doi.acm.org/10.1145/2737924.2737965
18. de Moura, L.M., Bjørner, N.: Efficient e-matching for SMT solvers.
    In: Automated Deduction - CADE-21, 21st International Conference on
    Automated       Deduction,     Bremen,      Germany,      July    17-20,   2007,    Proceed-
    ings.      pp.      183–198       (2007).     https://doi.org/10.1007/978-3-540-73595-3 13,
    https://doi.org/10.1007/978-3-540-73595-3_13
19. Niemetz, A., Preiner, M., Reynolds, A., Barrett, C., Tinelli, C.: Solving quan-
    tified bit-vectors using invertibility conditions. In: Chockler, H., Weissenbacher,
    G. (eds.) Computer Aided Verification - 30th International Conference, CAV
    2018, Held as Part of the Federated Logic Conference, FloC 2018, Oxford, UK,
    July 14-17, 2018, Proceedings, Part II. Lecture Notes in Computer Science, vol.
    10982, pp. 236–255. Springer (2018). https://doi.org/10.1007/978-3-319-96142-2 16,
    https://doi.org/10.1007/978-3-319-96142-2_16
20. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL: a proof assistant for higher-order
    logic, vol. 2283. Springer Science & Business Media (2002)
21. Nötzli, A., Reynolds, A., Barbosa, H., Niemetz, A., Preiner, M., Barrett, C., Tinelli, C.:
    Syntax-guided rewrite rule enumeration for smt solvers. To appear at SAT 2019.
22. Pichora, M.C.: Automated Reasoning About Hardware Data Types Using Bit-vectors of
    Symbolic Lengths. Ph.D. thesis, Toronto, Ont., Canada, Canada (2003), aAINQ84686
23. Reger, G., Suda, M., Voronkov, A.: Unification with abstraction and theory in-
    stantiation in saturation-based reasoning. In: Tools and Algorithms for the Con-
    struction and Analysis of Systems - 24th International Conference, TACAS
    2018, Held as Part of the European Joint Conferences on Theory and Prac-
    tice of Software, ETAPS 2018, Thessaloniki, Greece, April 14-20, 2018, Pro-
    ceedings, Part I. pp. 3–22 (2018). https://doi.org/10.1007/978-3-319-89960-2 1,
    https://doi.org/10.1007/978-3-319-89960-2_1
24. Reynolds, A., Barbosa, H., Fontaine, P.: Revisiting enumerative instantiation. In: Tools and
    Algorithms for the Construction and Analysis of Systems - 24th International Conference,
    TACAS 2018, Held as Part of the European Joint Conferences on Theory and Practice of
    Software, ETAPS 2018, Thessaloniki, Greece, April 14-20, 2018, Proceedings, Part II. pp.
    112–131 (2018)
25. Reynolds, A., Deters, M., Kuncak, V., Tinelli, C., Barrett, C.W.: Counterexample-guided
    quantifier instantiation for synthesis in SMT. In: Computer Aided Verification - 27th Inter-
    national Conference, CAV 2015, San Francisco, CA, USA, July 18-24, 2015, Proceedings,
    Part II. pp. 198–216 (2015)
26. Reynolds, A., Tinelli, C., Jovanovic, D., Barrett, C.: Designing theory
    solvers with extensions. In: Frontiers of Combining Systems - 11th Interna-
    tional Symposium, FroCoS 2017, Brası́lia, Brazil, September 27-29, 2017,
    Proceedings.      pp.     22–40     (2017).    https://doi.org/10.1007/978-3-319-66167-4 2,
    https://doi.org/10.1007/978-3-319-66167-4_2
27. Reynolds, A., Tinelli, C., de Moura, L.M.: Finding conflicting in-
    stances of quantified formulas in SMT. In: Formal Methods in Computer-
    Aided      Design,     FMCAD 2014,           Lausanne,      Switzerland,   October    21-24,
    2014.       pp.     195–202      (2014).     https://doi.org/10.1109/FMCAD.2014.6987613,
    https://doi.org/10.1109/FMCAD.2014.6987613
28. Solidity Language Developers: Solidity (2018), https://solidity.readthedocs.io/en/v0.4.25/
29. development team, T.C.: The coq proof assistant reference manual version 8.9 (2019),
    https://coq.inria.fr/distrib/current/refman/
30. Tinelli, C., Zarba, C.G.: Combining decision procedures for sorted theories. In: Alferes, J.J.,
    Leite, J. (eds.) Logics in Artificial Intelligence. pp. 641–653. Springer Berlin Heidelberg,
    Berlin, Heidelberg (2004)
31. Voronkov, A.: AVATAR: the architecture for first-order theorem provers. In: CAV. Lecture
    Notes in Computer Science, vol. 8559, pp. 696–710. Springer (2014)
A    Verified Invertibility Conditions

Table 6 summaries the results of verifying invertibility conditions. For each invertibility
condition, it states whether it was fully proved, only one direction of it was proved, or
none of the directions were proved.


             ℓ[x]     ≈    6≈   <uBV    >uBV    ≤uBV   ≥uBV     <BV
                                                                 s     >BV
                                                                        s      ≤BV
                                                                                s     ≥BV
                                                                                       s

       −BVx ⊲⊳ t      X   X       X      X       X       X        X      X      X       X
       ∼ BVx ⊲⊳ t     X   X       X      X       X       X        X      X      X       X
     x &BVs ⊲⊳ t      →   X       X      X       X       X        →      →      ✕       →
       x |BVs ⊲⊳ t    →   X       X      X       X       X        →      ✕      →       ✕
                           →                                                    →
    x <<BVs ⊲⊳ t      →           X      →       X       →        →      ✕              ✕
                                                                  →             →
    s <<BVx ⊲⊳ t      X   X       X      X       X       X               X              X
    x >>BVs ⊲⊳ t      X   X       X      →       X       X        X      →      X       →
    s >>BVx ⊲⊳ t      X   X       X      X       X       X        X      X      X       X
   x >>BV a s ⊲⊳ t    ✕   X       X      X       X       X        →      X      →       X
                                  →      →       →       →        →             →
   s >>BVa x ⊲⊳ t     X   X                                              ✕              X
     x +BVs ⊲⊳ t      X   X       X      X       X       X        X      X      X       X
                           →                                                    →
       x ·BVs ⊲⊳ t    ✕           X      ✕       X       ✕        ✕      ✕              ✕
                                                         →
   x div BVs ⊲⊳ t     X   X       X      X       X                X      X      X       X
                           →                                             →              →
   s div BVx ⊲⊳ t     X           X      X       X       X        X             X
                                                                                →
  x mod BVs ⊲⊳ t      X   X       X      X       X       X        ✕      X              X
                                                                         →              →
  s mod BVx ⊲⊳ t      →   X       X      X       X       X        X             X

Table 6. Invertibility conditions verification. X means was fully proved, → means only left-to-
             →
right proved, means only right-to-left proved, ✕ means not proved.
B Conditional Inverses
Tables 7 to 11 list all verified conditional inverses that we found. Note that we omitted
superscript BV from all bit-vector symbols for better readability.


                                    Literal     ≈          6≈
                                   −x ⊲⊳ t     −t        ∼t
                                   ∼x ⊲⊳ t     ∼t           t
                                 x + s ⊲⊳ t  t − s ∼(s + t)
                                 x & s ⊲⊳ t      t       ∼t
                               x >>a s ⊲⊳ t              ∼t
                               s >>a x ⊲⊳ t        t >>s − t
                                x >>s ⊲⊳ t t <<s mins <<t
                                s >>x ⊲⊳ t                −t
                                  x · s ⊲⊳ t       maxs <<t
                                  x | s ⊲⊳ t     t       ∼t
                                x <<s ⊲⊳ t t >>s maxs <<t
                                s <<x ⊲⊳ t                  t
                               x div s ⊲⊳ t   s ·t    s >>t
                               s div x ⊲⊳ t         t & mins
                              x mod s ⊲⊳ t       t      −∼t
                              s mod x ⊲⊳ t   s −t           t

                      Table 7. Conditional inverses for relations ≈ and 6≈.




C    Proof of Theorem 2
C.1 Property 1
Given a mapping J of the variables in v = FV(ω) to positive integers, every inter-
pretation I BV of TBV is translated to a corresponding interpretation I N of TUFIA such
that
    (∗) I BV satisfies ϕ iff I N satisfies Tfull (ϕ).
I N is defined as follows:
 – ⋄I N is set to satisfy AXfull                    N N
                                                          N
                             ⋄ for any ⋄ ∈ pow2, & , | , ⊕
 – v I N = v J for every v ∈ v
 – χ(x)I N = xcI BV N , where c = ω b (x)J for any x ∈ X ∗
                       

The converse translation can be achieved similarly, where appropriate bit-widths are
determined by the range axioms 0 ≤ χ(x) < pow2(ω b (x)) that occur in Tfull (ϕ, ω).
We prove (∗) using the following lemmas.
                   Literal             <s            ≤s
                  −x ⊲⊳ t             mins         mins
                  ∼x ⊲⊳ t             maxs         maxs
                x + s ⊲⊳ t        mins − s         t −s
                x & s ⊲⊳ t            mins             t
              x >>a s ⊲⊳ t            mins         mins
              s >>a x ⊲⊳ t     ∼(s | maxs ) ∼(s | maxs )
               x >>s ⊲⊳ t       mins <<s               t
               s >>x ⊲⊳ t      ∼(s | maxs ) ∼(s | maxs )
                 x · s ⊲⊳ t
                 x | s ⊲⊳ t            mins            mins
               x <<s ⊲⊳ t         mins >>s           t >>s
               s <<x ⊲⊳ t
              x div s ⊲⊳ t            ∼ −t                 t
              s div x ⊲⊳ t
             x mod s ⊲⊳ t     ∼(maxs | −s)         t & mins
             s mod x ⊲⊳ t                t             s −t

          Table 8. Conditional inverses for relations <s and ≤s .




      Literal                            >s                          ≥s
     −x ⊲⊳ t                             ∼t                          −t
     ∼x ⊲⊳ t                            mins                       mins
   x + s ⊲⊳ t                       maxs − s                       t −s
   x & s ⊲⊳ t                           maxs                      maxs
 x >>a s ⊲⊳ t                           maxs                      maxs
 s >>a x ⊲⊳ t                       s & mins                  s & mins
  x >>s ⊲⊳ t                      maxs <<s                       t <<s
  s >>x ⊲⊳ t
    x · s ⊲⊳ t
    x | s ⊲⊳ t                         maxs                           t
  x <<s ⊲⊳ t                      maxs >>s                  maxs >>s
  s <<x ⊲⊳ t
 x div s ⊲⊳ t
 s div x ⊲⊳ t
x mod s ⊲⊳ t                            −∼t                           t
s mod x ⊲⊳ t (s | mins ) − (maxs & t − maxs ) (s | mins ) − (t & maxs )

          Table 9. Conditional inverses for relations >s and ≥s .
           Literal            <u           ≤u
          −x ⊲⊳ t               0            0
          ∼x ⊲⊳ t              −t          ∼t
        x + s ⊲⊳ t            −s           −s
        x & s ⊲⊳ t              0             t
      x >>a s ⊲⊳ t              0            0
      s >>a x ⊲⊳ t    ∼(s | maxs ) ∼(s | maxs )
       x >>s ⊲⊳ t               s            s
       s >>x ⊲⊳ t               s            s
         x · s ⊲⊳ t             0            0
         x | s ⊲⊳ t             s            s
       x <<s ⊲⊳ t               0            0
       s <<x ⊲⊳ t            mins         mins
      x div s ⊲⊳ t              0             t
      s div x ⊲⊳ t            ∼0           ∼0
     x mod s ⊲⊳ t               s            s
     s mod x ⊲⊳ t               s            s

Table 10. Conditional inverses for relations <u and ≤u .




              Literal      >u       ≥u
             −x ⊲⊳ t       ∼t        −t
             ∼x ⊲⊳ t         0        0
           x + s ⊲⊳ t      ∼s       ∼s
           x & s ⊲⊳ t        s        s
         x >>a s ⊲⊳ t      ∼0       ∼0
         s >>a x ⊲⊳ t s & mins s & mins
          x >>s ⊲⊳ t       ∼s       ∼s
          s >>x ⊲⊳ t         0        0
            x · s ⊲⊳ t
            x | s ⊲⊳ t     ∼s         t
          x <<s ⊲⊳ t       ∼0       ∼0
          s <<x ⊲⊳ t
         x div s ⊲⊳ t      ∼0
         s div x ⊲⊳ t        0        0
        x mod s ⊲⊳ t     ∼ −s         t
        s mod x ⊲⊳ t         0        0

Table 11. Conditional inverses for relations >u and ≥u .
Lemma 3. Let I be an interpretation of TUFIA that satisfies AXpow2
                                                              full . Then, over natu-
ral numbers, pow2I is identical to λx.2x .
Proof. By the usual inductive definition of exponentiation.
Lemma 4. Let I be an interpretation of TUFIA that satisfies AXpow2   full . Let a be a bit-
vector constant of bit-width k and n = [a]N . Then I satisfies the following equations:
 – [i◦BVa]N ≈ pow2(k) · i + [a]N for any 0 ≤ i ≤ 1.
 – n mod pow2(k − 1) ≈ [a[k − 2 : 0]BV ]N
 – n div 2 ≈ [a[k − 1 : 1]BV ]N
Proof. By the definition of [·]N and Lemma 3.

Lemma 5. Let I be an interpretation of TUFIA that satisfies AXpow2
                                                              full , a be a bit-vector
                                                                    I
constant of bit-width k, 0 ≤ i ≤ k − 1 and n = [a]N . Then exi (n) = a [i], where
exi (n) is defined in Table 2.
Proof. We prove the first item by induction on k. The second is proved similarly. If
k = 1 then we must have i = 0. In this case, 0 ≤ n ≤ 1 and exi (n)I = n = [a [0]]N .
Suppose k > 1. If i = 0 then this is shown similarly to the base case. Otherwise, a [i]
is the i − 1 bit of a[1 : k − 1]BV . By the induction hypothesis and Lemma 4, the latter
is equal to exi−1 ([a[1 : k − 1]BV ]N )I = exi−1 ([a]N div 2)I = exi (n)I .
Lemma 6. Let a and b be bit-vector constants of bit-width k, ⋄ ∈ {&, |, ⊕}, and I an
                                                   ⋄
interpretation of TUFIA that satisfies AXpow2                                BV
                                         full ∧ AXfull . Then I satisfies [a⋄ b]N ≈
 N
⋄ (k, [a]N , [b]N ).
Proof. We prove the lemma for the case where ⋄ is & by induction on k. The other
                                                                            I
cases are shown similarly. If k = 1, then by Lemmas 3 and 5 we have [a &BVb]N =
                              N
[min(a, b)]N = min(a, b) =& (1, [a]N , [b]N ). Now suppose k > 1. Then,

            &N(k, [a]N , [b]N )I =
            (&N(k − 1, [a]N mod pow2(k − 1), [b]N mod pow2(k − 1))+
            pow2(k − 1) · min(exk−1 (a), exk−1 (b)))I

   By Lemma 5, we have that

                min(exk−1 (a), exk−1 (b)) = a [k − 1] &BVb [k − 1] N
                                                                 

By the induction hypothesis and Lemma 4, we obtain that &N (k, [a]N , [b]N ) is equal in
I to

     a[k − 2 : 0]BV &BVb[k − 2 : 0]BV N + pow2(k − 1) · a [k − 1] &BVb [k − 1] N
                                                                               

which by Lemma 4 is equal in I to

      a [k − 1] &BVb [k − 1] ◦BVa[k − 2 : 0]BV &BVa[k − 2 : 0]BV N = a &BVb N
                                                                         

                              h          i
                        IN          I BV
Lemma 7. C ONV(t, ω) = t|ω[J ]              for any parametric ΣBV -term t.
                                           N
Proof. First notice that for any x ∈ X ∗ ∪ Z ∗ we have that ω b (x)I N = ω b (x)J and
ω N (x)I N = ω N (x)J . Using induction, the same holds for any parametric ΣBV -term t.
    We prove the lemma by induction on t.

 – If t is x for some x ∈ X ∗ : follows from the definition of I N for this case.
 – If t is z for some z ∈ Z ∗ :
                                                 IN
                                  C ONV (t, ω) =
                                  (ω N (z) mod pow2(ω b (z)))I N =
                                  ω N (z)J mod pow2(ω b (z)J )

   Now, z|ω[J ] is the bit-vector constant of width k = ω b (z)J whose integer value is
   ω N (z)J mod 2k .
 – If t is constructed from an operator other than &BV , |BV , ⊕BV , then this follows by
   the semantics of the various operators as it is defined in the SMT-LIB 2 standard.
   We explicitly show that case where t = t1 +BVt2 . In this case,

             C ONV (t, ω) = (C ONV (t1 , ω) + C ONV (t2 , ω)) mod pow2(ω b (t2 ))

    which by Lemma 3 is interpreted in I N as

                       ((C ONV (t1 , ω))I N + (C ONV (t2 , ω))I N ) mod 2k

    for k = ω b (t2 )J . By the induction hypothesis, the latter is equal to
                           h               i  h               i
                                      I BV               I BV
                          ( t1 |ω[J ]        + t2 |ω[J ]        ) mod 2k
                                             N                  N

   which   by the semantic of +BV as defined in the SMT-LIB 2 standard, is equal to
     ((t1 +BVt2 )|ω[J ] )I BV N .
   

 – The operators &BV , |BV and ⊕BV rely on Lemma 6, rather than on the SMT-LIB 2
   standard. We explicitly show the case where t = t1 &BVt2 . In this case,
                             IN
               C ONV(t, ω)        = (&N(ω b (t2 ), C ONV (t1 , ω), C ONV(t2 , ω)))I N

    which by the induction hypothesis is equal to
                                      h              i h              i
                        (&N(ω b (t2 ), t1 |ω[J ] I BV , t2 |ω[J ] I BV ))I N
                                                       N              N

    By Lemma 6, we obtain

                                         ((t1 &BVt1 )|ω[J ] )I BV N
                                                                


Corollary 8. I BV satisfies ϕ iff I N satisfies Tfull (ϕ).

Proof. By routine induction on ϕ, where the base cases follow from Lemma 7.
C.2 Properties 2 – 4
The rest of the properties follow from Property 1 by showing that the axioms in Table 3
are valid in every interpretation of TUFIA that satisfies AXfull (ϕ, ω). The axioms of
pow2 easily follow from simple properties of exponentiation. As for the bitwise logical
operators, we explicitly prove the validity of “difference” for &N. The rest are shown
similarly. Let k > 0, 0 ≤ x, y, z < 2k , and I an interpretation of TUFIA that satisfies
AXfull (ϕ, ω). Note that k, x, y and z are bound as integers, and are therefore interpreted
as themselves in I. Let a, b and c be bit-vectors of width k such that x = [a]N , y = [b]N
and z = [c]N . Suppose I satisfies x 6≈ y. Then a 6≈ b, and so there exists some
0 ≤ i ≤ k − 1 such that a [i] 6≈ b [i]. First suppose a [i] = 0. Then b [i] = 1 and
(a &BVc) [i] = 0, and hence a &BV c 6≈ b. This means that [a &BVc]N 6≈ [b]N , and thus
by By Lemma 6 we have that I satisfies &N(k, x, z) 6≈ y. Otherwise, a [i] = 1 and
b [i] = 0. If a &BV c ≈ b then c [i] = 0, which means that (b &BVc) [i] = 0 and so
b &BV c 6≈ a. This means that [b &BVc]N 6≈ [a]N , and thus by Lemma 6 we have that I
satisfies &N(k, y, z) 6≈ x.
