           An Overview of the HFL Model Checking Project

                                                Naoki Kobayashi
                                               The University of Tokyo
                                                    Tokyo, Japan
                                             koba@is.s.u-tokyo.ac.jp



       In this article, we give an overview of our project on higher-order program verification based on HFL
       (higher-order fixpoint logic) model checking. After a brief introduction to HFL, we explain how it
       can be applied to program verification, and summarize the current status of the project.


1     Introduction
In this article, we give a brief overview of our project on automated verification of higher-order programs
based on (a variation of) Viswanathan and Viswanathan’s higher-order fixpoint logic (HFL) [43]. HFL
is a higher-order extension of the modal µ-calculus and is strictly more expressive than the modal µ-
calculus, but the HFL model checking problem for finite state systems remains decidable.
    In Section 2, we first review HFL, and HFL(Z), an extension of HFL with integer arithmetic, and
show that HFL(Z) may also be viewed as an extension of Constrained Horn Clauses (CHC) [3,12,19,36]
with higher-order predicates and fixpoint alternations.
    In Section 3, we show how various program verification problems can naturally be reduced to HFL(Z)
model/validity checking problems. Our program verification framework based on HFL(Z) can be con-
sidered a generalization of CHC-based program verification framework [3, 12, 19, 36]. In Section 4, we
summarize our methods for automatically solving the HFL(Z) model/validity checking problems, using
higher-order model checkers and CHC solvers as backends.
    This article is intended to be a non-exhaustive survey of HFL-based approaches to program verifica-
tion. The main objective is to provide references to technical papers and clarify how they are connected
with each other; the explanation of each topic is admittedly short and cryptic.


2     Higher-Order Fixpoint Logic and its Relationship with CHC
2.1    Higher-Order Fixpoint Logic
The syntax of HFL(Z) formulas and types is given as follows.
                                                                                          
                   ϕ (formulas) ::= xτ | ϕ1 ∨ ϕ2 | ϕ1 ∧ ϕ2                                
                                                                                          
                                  | haiϕ | [a]ϕ        (modal operators)
                                                                                          
                                                                                            pure HFL
                                  | µxκ .ϕ | νxκ .ϕ (fixpoint operators)                  
                                                                                          
                                  | ϕ1 ϕ2 | λ xτ .ϕ    (λ -abstractions and applications)
                                                                                          
                                  | ϕ e | e1 ≤ e2      (extension with integers)
        e (integer expressions) ::= n | xint | e1 + e2
                      τ (types) ::= int | κ
             κ (predicate types) ::= o | τ → κ

Hossein Hojjat and Bishoksan Kafle (Eds.): 8th Workshop on                   © N. Kobayashi
Horn Clauses for Verification and Synthesis (HCVS 2021)                      This work is licensed under the
EPTCS 344, 2021, pp. 1–12, doi:10.4204/EPTCS.344.1                           Creative Commons Attribution License.
2                                                                               HFL Model Checking Project


     Here, each variable (denoted by the metavariable x, y, . . .) has its own type (specified as a superscript),
and we consider only well-typed formulas and expressions; for example, in ϕ1 ∨ ϕ2 , both ϕ1 and ϕ2 must
have the type o of propositions. We often omit the type annotation of a variable. Each formula must have
a predicate type, and integer expression must have type int. See [27] for typing rules.
     The first three lines of the definition of formulas correspond to the syntax of the modal µ-calculus [15,
30] in negation normal form (if the types κ and τ are restricted to the type o of propositions), and the
first four lines correspond to the syntax of pure HFL [43]. Each formula of type o describes a property of
labeled transition systems. The formula haiϕ means that there exists a transition labeled a after which the
proposition ϕ holds, while the formula [a]ϕ means that, after any transition labeled a, the proposition ϕ
holds. The formulas µxκ .ϕ and νxκ .ϕ respectively denote the least and greatest predicates x such that x =
ϕ. For example, µxo .xo and νxo .xo respectively denote the least and greatest propositions such that x = x,
i.e., false and true respectively; henceforth, we treat false and true as propositional constants. The
fifth line is for the extension with integers. We have only constants, additions, and inequality constraints
on integers, but other predicates and operations, as well as quantifiers, are definable, as shown below.
Example 1. Let ϕ be a formula of type int → o, and ψ be νx.λ n.ϕ(n) ∨ x(n + 1). Then we have

                 ψ(0) ≡       (λ n.ϕ(n) ∨ ψ(n + 1))0                        (by unfolding ψ)
                      ≡       ϕ(0) ∨ ψ(1)                                   (by β -reduction)
                      ≡       ϕ(0) ∨ (λ n.ϕ(n) ∨ ψ(n + 1))(1)               (by unfolding ψ)
                      ≡       ϕ(0) ∨ ϕ(1) ∨ (λ n.ϕ(n) ∨ ψ(n + 1))(2)        (by β -reduction)
                      ≡       ϕ(0) ∨ ϕ(1) ∨ ϕ(2) ∨ · · · .

Thus, ψ(0) denotes ∃x ≥ 0.ϕ(x). Similarly, ∀x ≥ 0.ϕ(x) can be expressed by (νx.λ n.ϕ(n) ∧ x(n + 1))0,
and ∀x ∈ Z.ϕ(x) (where Z is the set of integers) can be expressed by (νx.λ n.ϕ(n) ∧ x(n − 1) ∧ x(n + 1))0.
The multiplication can be expressed as a ternary predicate mult(x, y, z) (which means x × y = z), e.g., by:

      mult := µu.λ (x, y, z).y = z = 0 ∨ (1 ≤ y ∧ u(x, y − 1, z − x)) ∨ (y + 1 ≤ 0 ∧ u(x, y + 1, z + x)).

Here we have used tuple notations and subtractions (−) for readability; as usual, subtractions can be
defined by using additions and existential quantifiers.
    As shown in the example below, pure HFL is already strictly more expressive than the modal µ-
calculus.
Example 2. Consider ϕ be the formula νx.λ y.y ∨ haix(hbiy). Then, we have:

 ϕ(hcitrue) ≡        (λ y.y ∨ haiϕ(hbiy))(hcitrue)                                 (unfolding of ϕ)
            ≡        hcitrue ∨ haiϕ(hbihcitrue)                                    (β -reduction)
            ≡        hcitrue ∨ hai(hbihcitrue ∨ haihaiϕ(hbihbihcitrue))            (unfolding, followed by β )
            ≡        hcitrue ∨ haihbihcitrue ∨ hai2 hbi2 hcitrue ∨ · · ·

Thus, ϕ(hcitrue) means that there exists a transition sequence of the form an bn after which a c-transition
is enabled.
    We write M |= ϕ when a labeled transition system M satisfies ϕ. We omit the formal semantics
of HFL(Z) [27]. The model checking problem for HFL(Z) is the problem of checking whether M |= ϕ
holds, given a finite labeled transition system M and a HFL(Z) formula ϕ of type o. The validity
checking problem is a special case: it is the problem of checking whether M0 |= ϕ holds, where ϕ is
a HFL(Z) formula of type o without modal operators (hai, [a]), and M0 is a trivial model consisting
N. Kobayashi                                                                                              3


of a single state without transitions. We often just write |= ϕ for M0 |= ϕ and say “ϕ is valid” when
|= ϕ holds. For pure HFL, the model checking problem (hence also the validity checking problem) is
decidable [43] and k-EXPTIME complete for the order-k fragment [1]. Here, the order of the model
checking problem is defined as the the largest order of types that occur in the HFL formula, and the order
of a type τ, written ord(τ), is defined by:

                 ord(o) = ord(int) = 0            ord(τ → κ) = max(ord(τ) + 1, ord(κ)).

For example, the order of the formula in Example 2 is 1. For HFL(Z), both the model and validity
checking problems are undecidable due to Gödel’s incompleteness theorem (recall that quantifiers and
multiplications can be expressed, as discussed in Example 1).

2.2   Relationship with CHC
We now explain the connection between the HFL(Z) validity checking problem and the CHC satisfiability
problem, through examples. A little formal discussion on the correspondence between HFL(Z) and CHC
is found in [25]. We assume that the reader is familiar with Constrained Horn Clauses (CHCs); those
not familiar with CHCs may wish to consult [3], which is a good survey CHCs and their applications to
program verification.
    Let us consider the following system S of CHCs.

                                                   ∀x, y, r. y = 0 ∧ r = 0 =⇒ mult(x, y, r)
                    ∀x, y, r, s. y 6= 0 ∧ mult(x, y − 1, s) ∧ r = s + x =⇒ mult(x, y, r)
                                          ∀x, y, r. mult(x, y, r) ∧ x > 0 =⇒ r ≥ y.
The satisfiability of CHCs above (i.e., the existence of an assignment of a predicate to the predicate vari-
able mult) is equivalent to the safety property of the following OCaml program (that assertion failures
never occur):
      let rec mult(x,y) =
        if y=0 then 0
        else let s = mult(x, y-1) in s+x
      let main x y = if x>0 then assert(mult(x,y)>=y)
Here, the ternary predicate mult(x, y, r) in the CHCs intuitively means that the return value of mult(x, y)
in the program is r.
    Let us now convert the satisfiability problem for the CHCs above to the validity checking problem
for a HFL(Z) formula. First, note that the first two clauses are equivalent to:

           ∀x, y, r.(y = 0 ∧ r = 0) ∨ ∃s.(y 6= 0 ∧ mult(x, y − 1, s) ∧ r = s + x) =⇒ mult(x, y, r).

The least predicate ϕ that satisfies the condition above is expressed by:

                   µu.λ (x, y, r).(y = 0 ∧ r = 0) ∨ ∃s.(y 6= 0 ∧ u(x, y − 1, s) ∧ r = s + x).

Thus, the satisfiability of S is equivalent to:

                                     ∀x, y, r. ϕ(x, y, r) ∧ x > 0 =⇒ r ≥ y,

which is also equivalent to:
                                       ∀x, y, r. ϕ(x, y, r) ∨ x ≤ 0 ∨ r ≥ y,
4                                                                                           HFL Model Checking Project


where ϕ is the de Morgan dual of ϕ, given as:
                       νu.λ (x, y, r).(y 6= 0 ∨ r 6= 0) ∧ ∀s.(y = 0 ∨ u(x, y − 1, s) ∨ r 6= s + x).
In this manner, the satisfiability problem for any CHCs on integer arithmetic can be converted to the
validity checking problem for a formula of the first-order, ν-only fragment (i.e. the fragment without
µ) of HFL(Z); recall that universal quantifiers can be expressed by using ν. Conversely, the validity
checking problem for any formula of the first-order, ν-only fragment where the types of fixpoint variables
are restricted to those of the form int → · · · → int → o can be reduced to the satisfiability problem for
CHCs on integer arithmetic [25]. In this sense, the HFL(Z) validity checking problem can be considered a
generalization of the CHC satisfiability problem, where higher-order predicates and fixpoint alternations
between µ and ν are allowed.
    Burn et al. [5, 35] recently studied a higher-order extension of CHCs called HoCHC. The HFL(Z)
validity checking problem can also be considered an extension of the satisfiability problem for HoCHC
with fixpoint alternations.


3     From Program Verification to HFL(Z) Model Checking
This section explains how HFL(Z) model/validity checking can be applied to program verification. As
seen at the end of the last section, HFL(Z) validity checking subsumes CHC solving, which already
have a plenty of applications to program verification [3], but how can we exploit the additional power of
HFL(Z) model/validity checking for program verification?
    A standard approach to applying model checking to program verification is to model a program as a
transition system, and a property of the program to be checked as a specification; that is indeed the case
for applications of finite-state model checking [7], pushdown model checking [2], and HORS model
checking (which is another kind of higher-order extension of model checking) [21, 34]. In applying
HFL(Z) model checking to higher-order program verification, we actually switch the roles of systems
and specifications: a program is mapped to a HFL(Z) formula, and a property is mapped to a finite
state system, where the HFL(Z) formula is a kind of “characteristic formula” of the program. This has
been partially inspired by the correspondence between HFL model checking and HORS model checking,
where we also need to switch the roles of systems and specifications [24].
    Let us consider the following file-accessing program, taken from [27].
   let x = open "foo" in (read(x); read(x); close(x))
This program opens the file “foo”, and then reads and closes the file. Suppose we wish to check that
the file “foo” is indeed accessed as a read-only file. To this end, we express the valid access protocol
for a read-only file pointer as a labeled transition system, as shown in Figure 1. The LTS corresponds
to a deterministic automaton that accepts the valid traces read∗ · close · end. Here, end denotes the
termination of a program. In the state q0 (which is the initial state immediately after a file is opened),
both read and close operations are allowed, but after the close operation, only the end operation is
allowed. The program can be converted to the HFL(Z) formula:
                                           hreadihreadihcloseihenditrue,
which intuitively means that the program follows the access protocol represented by the LTS. It is ob-
tained by just replacing each of the read, close, and end operations with the corresponding modal opera-
tors that say “those actions are allowed in the current state.”1 It is easy to see that the program accesses
    1 Please ignore the open operation here; it matters when more than one file is used in a program, as in [21].
N. Kobayashi                                                                                              5


                                          read
                                                 close         end
                                         q0              q1            q2


                         Figure 1: An LTS Mfile expressing the valid file access protocol


the file “foo” just if
                                   Mfile |= hreadihreadihcloseihenditrue.
   The same idea applies to more complex programs that contain recursion and conditionals. Let us
consider the following program:
    let x = open "foo" in
    let rec f n = if n<=0 then close x else (read x; f (n-1) x) in
    f 10
To make the reduction clearer, let us write it in the continuation passing style.
    let x = open "foo" in
    let rec f n k = if n<=0 then close x k else read x (f (n-1) x k) in
    f 10 ()
Here, read and close now take an additional continuation parameter, which is invoked after the read/close
operations. Then, the property that the program accesses the file “foo” as a read-only file just if:

      Mfile |= (µ f .λ n.λ k.(n ≤ 0 ⇒ hcloseik) ∧ (n > 0 ⇒ hreadi( f (n − 1) k)))10 (henditrue).

Here, the formula contains integers and order-1 fixpoint operators. As before, the formula has been
obtained by just replacing each of the read/close operations, and program termination (represented by
()) with the corresponding modal operator. The conditional “if n<=0 then ... else ...” has
been replaced by the corresponding logical formula (n ≤ 0 ⇒ · · ·) ∧ (n > 0 ⇒ · · ·), and the recursion has
been replaced by the fixpoint operator µ (here, by using µ, we require that the program terminates).
     We have given above just order-1 examples, but it should be clear that the idea of the translation
should work for higher-order programs. A general translation for linear-time properties is found in [27],
a translation for arbitrary ω-regular properties (including both linear-time and branching time properties)
is found in [44]. For linear-time properties of first-order recursive programs, a more optimized translation
is given in [25]. In those general translations, program verification problems are actually reduced to the
validity checking problem for HFL(Z) formulas, by using a kind of product construction.


4    Solving HFL(Z) Model Checking Problems
In this section, we discuss how to solve instances of the HFL(Z) model checking problem obtained from
program verification problems. For the sake of simplicity, we actually focus on the validity checking
problem (which is a special case of the model checking problem where the formula contains no modal
operators; recall Section 2.1), but most of the techniques apply to the model checking problem as well.
Some of our tools and benchmark sets mentioned below are available from https://github.com/
hopv. For the other tools, please consult each paper cited below.
6                                                                                        HFL Model Checking Project



                                                HFL(Z) formula
                                                                        Simplification
                                                         Removal of µ
                                                 νHFL(Z) formula
                                     Predicate
                                     abstraction              Refinement types
                                         νHFL formula        CHC
                              Higher-order                       CHC Solving
                              model checking
                                                Yes/No/Unknown



                  Figure 2: An overview of our method for HFL(Z) validity checking


    Our overall method for HFL(Z) validity checking is summarized in Figure 2. In the figure, a
“νHFL(Z) formula” refers to a HFL(Z) formula without the least fixpoint operator µ. The overall strat-
egy for solving the validity checking problem is analogous to, and has been inspired by automated
program verification methods. The first phase of removing the least fixpoint operator µ corresponds to
reductions from liveness property verification (such as termination verification) to safety property veri-
fication [8, 32, 37]. The two methods for checking the validity of νHFL(Z) formula correspond to two
major approaches to automated verification of higher-order programs: higher-order model checking [26]
and refinement types [38, 41, 42, 45]. We discuss each step of Figure 2 below.
    Due to underapproximation in various steps (a formula ϕ is replaced by another formula ϕ 0 such that
ϕ ⇒ ϕ, so that the validity of ϕ 0 implies that of ϕ, but not vice versa), the procedure shown in Figure 2
  0

cannot conclude that the original formula ϕ is invalid even if an approximation of the formula is invalid.
Thus, given a HFL(Z) formula ϕ, we also prepare its de Morgan dual ϕ, and apply the whole procedure
in parallel to ϕ and ϕ. If ϕ is valid, then we can conclude that ϕ is invalid.

4.1   Removing µ
In the reductions from program verification problems to HFL(Z) validity checking [25, 27, 44], liveness
and safety properties are respectively turned into µ- and ν-formulas. Thus, following the techniques for
liveness property verification [8,14,32,33,37], it is natural to first remove µ-formulas by using analogous
techniques.
    In [25], we have adopted the technique of Fedyukovich et al. [14] for the first-order fragment of
HFL(Z) formulas. Suppose that we wish to prove the validity of a µ-formula of the form µx.ϕ(x). By
the standard fixpoint theorem, we have

                                           ϕ n (false) ⇒ µx.ϕ(x)

for any natural number n. The formula ϕ n (false) is equivalent to (νx0 .λ z.(z > 0 ∧ ϕ(x0 (z − 1))))n,
which is also equivalent to the following formula ψ:

                              ψ := ∀u ≥ n.(νx0 .λ i.(i > 0 ∧ ϕ(x0 (i − 1))))u.

Thus, it suffices to show that ψ is valid. Here, n can be considered a bound for the number of unfoldings
of the original µ-formula; by gradually increasing n, we can obtain a better approximation of the original
formula.
N. Kobayashi                                                                                                         7


    In the case of the first-order HFL(Z) formulas, the above translation yields order-1 νHFL(Z) formulas
(where all the types are of the form intk → o), whose validity checking problems can be further reduced
to the CHC satisfiability problem, as discussed in Section 2.
Example 3. Let us consider proving the validity of the formula:

                                           ∀i.(µx.λ y.y ≤ 0 ∨ x(y − 1))i.

Based on the above translation, it suffices to show:

                 ∀i.∀u ≥ max(i + 1, 1).(νx0 .λ (z, y).z > 0 ∧ (y ≤ 0 ∨ x0 (z − 1, y − 1)))(u, i).

Here, max(i+1, 1) corresponds to the bound n above; in general, the bound may depend on free variables
as in this example. Note that the resulting formula contains only ν and ∀, where the latter can also be
expressed by ν, as seen in Example 1.
    To translate the formula above to CHCs, observe that the formula is equivalent to:

           ∀i.∀u ≥ max(i + 1, 1).(µx0 .λ (z, y).z ≤ 0 ∨ (y > 0 ∧ x0 (z − 1, y − 1)))(u, i) ⇒ false.

The µ-formula µx0 .λ (z, y).z ≤ 0 ∨ (y > 0 ∧ x0 (z − 1, y − 1))) is the least predicate X that satisfies the
following clauses:
                                                   z ≤ 0 =⇒ X(z, y)
                                 y > 0 ∧ X(z − 1, y − 1) =⇒ X(z, y).
Thus, the validity of the formula above is equivalent to the satisfiability of the two clauses above with
the goal clause:
                               u ≥ i + 1 ∧ u ≥ 1 ∧ X(u, i) =⇒ false.
The above system of CHCs is indeed satisfiable, and has the model: X(z, y) := z ≤ 0 ∧ z ≤ y. We can thus
conclude that the original HFL(Z) formula is valid.
    We have implemented the above method for the first-order fragment of HFL(Z) and applied it to
automated verification of temporal properties [25]. Despite the generality of the approach (which works
for arbitrary ω-regular properties of while-programs), our implementation generally outperformed Cook
and Koskinen’s method specialized for CTL verification [9], probably thanks to the recent advance of
CHC solvers [6, 16, 28] and the streamlined approach. Work is under way to extend the translation above
for HFL(Z) formulas of arbitrary orders.

4.2    Predicate Abstraction for νHFL(Z) Validity Checking
One approach [18] to proving the validity of a νHFL(Z) formula ϕ is to apply predicate abstraction to
obtain a pure νHFL formula ϕ 0 (i.e., a νHFL(Z) formula without integers) as an underapproximation
of ϕ, and then apply an algorithm for pure HFL model checking [17]2 (recall that pure HFL model
checking is decidable; despite its high worst-case complexity, practical algorithms exist, which do not
always suffer from the high complexity). This approach may be viewed as a generalization of the HORS
model checking approach to (un)reachability verification [26] and non-termination verification [31].
   2 In the actual implementation, we actually use a HORS model checker [4, 22] based on the correspondence between HFL

and HORS model checking [24].
8                                                                           HFL Model Checking Project


    Given a set of predicates on integers, a given νHFL(Z) formula can be underapproximated by a pure
HFL formula. For example, suppose that we have decided to abstract every integer with the predicate
λ y.y > 0. Then, the formula φ := (νx.λ y.y ≥ 0 ∧ x(y + 1))1 can be underapproximated by φ 0 :

                                         (νx.λ b.b ∧ x(b))true,

where b is a Boolean variable corresponding to the condition y > 0. Since φ 0 is valid (as can be confirmed
by a pure HFL model checker), we can conclude that the original formula φ is also valid. As in standard
approaches to combining predicate abstraction and model checking, predicates to be used for abstraction
can be found in a counterexample-guided manner. More details can be found in [18].

4.3   Refinement Types for νHFL(Z) Validity Checking
We have also studied another approach to νHFL(Z) validity checking, based on a (sound but incomplete)
reduction to a refinement type inference problem [20]. The approach has been inspired by the refinement
type system of Burn et al. [5] for HoCHC, whose idea can further be traced back to refinement type
systems for functional programs [38, 41, 42, 45].
    The syntax of refinement types for νHFL(Z) is given by:

                                   σ ::= o[ψ] | σ1 → σ2 | x : int → σ .

Here, ψ is a quantifier-free formula of integer arithmetic (which may contain integer variables bound by
x : int → · · ·). The type o[ψ] describes propositions that hold whenever ψ holds. For example, the νHFL
formula x ≥ 0 has type o[x > 0], since x ≥ 0 holds whenever x > 0 holds. A predicate λ p.p(0) has type
(x : int → o[x ≥ 0]) → o[true], because p(0) holds whenever p is a predicate on integers such that p(x)
holds for every x ≥ 0. Based on the intuition, one can construct a refinement type system for νHFL(Z),
such that a νHFL(Z) formula ϕ is valid if ϕ has type o[ψ], and reduce the type inference problem to
a constraint satisfaction problem on predicate variables in a standard manner [5, 6, 41]. Unlike the case
of refinement type systems for (un)reachability verification of functional programs [6, 41], the resulting
constraint satisfaction problem is no longer a CHC problem in general; constraints on predicates may be
of the form:
                           P1 (x̃, ỹ) ∧ · · · ∧ Pk (x̃, ỹ) ∧ ψ(x̃, ỹ) =⇒ Q1 (x̃) ∨ · · · ∨ Q` (x̃),
where disjunction may occur in the head (here, Pi , Q j are unknown predicate variables and ψ(x̃, ỹ) is a
formula of integer arithmetic). Solving this generalized form of constrained clauses [39] is the current
major bottleneck of this approach; work is under way to extend the ICE-based CHC solving approach [6,
13] to deal with the generalized constrained clauses.
    Despite the bottleneck mentioned above, the refinement type-based approach to νHFL(Z) validity
checking is generally faster than the predicate abstraction-based approach, while the latter tends to be
more precise. Thus, the two approaches are complementary to each other.

4.4   Unfold/fold Transformations for Simplification
Inspired by the unfold/fold transformation techniques for CHC solving [10, 11], we have also studied
unfold/fold transformations for the first-order fragment of HFL(Z) [23] to enhance the power of an au-
tomated HFL(Z) validity checker. The transformations are useful for reasoning about relations between
fixpoint formulas.
N. Kobayashi                                                                                                                    9


      For example, consider proving ∀n.Even(n) ⇒ Odd(n + 1), where Even and Odd are defined by:

                                         Even := µx.λ y.(y = 0 ∨ x(y − 2))
                                         Odd := µx.λ y.(y = 1 ∨ x(y − 2)).

It can be expressed as the HFL(Z) formula ∀n.Even(n) ∨ Odd(n + 1), where

                                          Even := νx.λ y.(y 6= 0 ∧ x(y − 2)).

Let Even(y) ∨ Odd(y + 1) be ϕ(y). It can be transformed as follows:

           ϕ(y) ≡        Even(y) ∨ Odd(y + 1)
                ≡        (y 6= 0 ∧ Even(y − 2)) ∨ (y + 1 = 1 ∨ Odd(y − 1)) (unfold Even and Odd)
                ≡        y + 1 = 1 ∨ Even(y − 2) ∨ Odd(y − 1)              (shuffle the formula)
                ≡        y = 0 ∨ ϕ(y − 2)                                  (by the definition of ϕ).

Based on the transformations above, we can replace Even(n)∨Odd(n+1) with (νx.λ y.y = 0∨x(y−2))n,
which is obviously valid (since νx.λ y.y = 0 ∨ x(y − 2) ≡ λ y.true). The above sequence of transfor-
mations are analogous to unfold/fold transformations for CHCs [10], but the soundness of the overall
transformations is more subtle, due to the mixture of the least and greatest fixpoint operators: see [23]
for the conditions of soundness of unfold/fold transformations for the first-order fragment of HFL(Z).

4.5     Semi-Automated Methods
We have so far discussed automated methods for HFL(Z) validity checking. As the HFL(Z) formula
obtained from a program verification problem can be considered a kind of “verification condition,”3 it is
also natural to prove the validity of the formula semi-automatically, possibly using a proof assistant such
as Coq, as exploited in our recent work [29,44]. Integration with the automated methods is left for future
work.


5     Conclusion
We have given an overview of our project on automated program verification based on HFL(Z) model
and validity checking. Our framework can be considered a generalization of the CHC-based program
verification framework and provides a uniform approach to higher-order program verification. One may
wonder whether HFL(Z) is too expressive as the target of reductions from program verification problems.
To answer the question, Tsukada [40] has recently shown that, in a certain sense, HFL(Z) is just as
expressive as needed for encoding higher-order program verification problems. A lot of work is still left
to be done, including a full implementation of the HFL(Z) validity checker and further improvement of
backend solvers for CHCs and generalized constrained clauses.


Acknowledgment
We would like to thank anonymous referees for useful comments. This work was supported by JSPS
KAKENHI Grant Number JP20H00577 and JP20H05703.
    3 Thanks to fixpoint operators, no annotations of loop invariants and pre/post-conditions of recursive functions are required.
10                                                                             HFL Model Checking Project


References
 [1] Roland Axelsson, Martin Lange & Rafal Somla (2007): The Complexity of Model Checking Higher-Order
     Fixpoint Logic. Logical Methods in Computer Science 3(2), doi:10.2168/LMCS-3(2:7)2007.
 [2] Thomas Ball, Byron Cook, Vladimir Levin & Sriram K. Rajamani (2004): SLAM and Static Driver Verifier:
     Technology Transfer of Formal Methods inside Microsoft. In: Integrated Formal Methods 2004, LNCS 2999,
     Springer, pp. 1–20, doi:10.1007/978-3-540-24756-2 1.
 [3] Nikolaj Bjørner, Arie Gurfinkel, Kenneth L. McMillan & Andrey Rybalchenko (2015): Horn Clause Solvers
     for Program Verification. In: Fields of Logic and Computation II - Essays Dedicated to Yuri Gurevich on the
     Occasion of His 75th Birthday, LNCS 9300, Springer, pp. 24–51, doi:10.1007/978-3-319-23534-9 2.
 [4] Christopher H. Broadbent & Naoki Kobayashi (2013): Saturation-Based Model Checking of Higher-Order
     Recursion Schemes. In: CSL 2013, LIPIcs 23, pp. 129–148, doi:10.4230/LIPIcs.CSL.2013.129.
 [5] Toby Cathcart Burn, C.-H. Luke Ong & Steven J. Ramsay (2018): Higher-order constrained horn clauses
     for verification. Proc. ACM Program. Lang. 2(POPL), pp. 11:1–11:28, doi:10.1145/3158099.
 [6] Adrien Champion, Tomoya Chiba, Naoki Kobayashi & Ryosuke Sato (2020): ICE-Based Refinement
     Type Discovery for Higher-Order Functional Programs. J. Autom. Reason. 64(7), pp. 1393–1418,
     doi:10.1007/s10817-020-09571-y.
 [7] Edmund M. Clarke, Orna Grumberg & Doron A. Peled (1999): Model Checking. The MIT Press.
 [8] Byron Cook, Alexey Gotsman, Andreas Podelski, Andrey Rybalchenko & Moshe Y. Vardi (2007): Prov-
     ing That Programs Eventually Do Something Good. In: Proceedings of POPL, ACM Press, pp. 265–276,
     doi:10.1145/1190216.1190257.
 [9] Byron Cook & Eric Koskinen (2013): Reasoning About Nondeterminism in Programs. In: Proceedings of
     PLDI 2013, ACM Press, pp. 219–230, doi:10.1145/2491956.2491969.
[10] Emanuele De Angelis, Fabio Fioravanti, Alberto Pettorossi & Maurizio Proietti (2018): Solving Horn Clauses
     on Inductive Data Types Without Induction. TPLP 18(3-4), pp. 452–469, doi:10.1017/S1471068418000157.
[11] Emanuele De Angelis, Fabio Fioravanti, Alberto Pettorossi & Maurizio Proietti (2020): Removing Alge-
     braic Data Types from Constrained Horn Clauses Using Difference Predicates. In Nicolas Peltier & Viorica
     Sofronie-Stokkermans, editors: Automated Reasoning - 10th International Joint Conference, IJCAR 2020,
     Paris, France, July 1-4, 2020, Proceedings, Part I, Lecture Notes in Computer Science 12166, Springer, pp.
     83–102, doi:10.1007/978-3-030-51074-9 6.
[12] Giorgio Delzanno & Andreas Podelski (2001): Constraint-based deductive model checking. Int. J. Softw.
     Tools Technol. Transf. 3(3), pp. 250–270, doi:10.1007/s100090100049.
[13] P. Ezudheen, Daniel Neider, Deepak D’Souza, Pranav Garg & P. Madhusudan (2018): Horn-ICE learn-
     ing for synthesizing invariants and contracts. Proc. ACM Program. Lang. 2(OOPSLA), pp. 131:1–131:25,
     doi:10.1145/3276501.
[14] Grigory Fedyukovich, Yueling Zhang & Aarti Gupta (2018): Syntax-Guided Termination Analysis. In: Com-
     puter Aided Verification - 30th International Conference, CAV 2018, Held as Part of the Federated Logic
     Conference, FloC 2018, Oxford, UK, July 14-17, 2018, Proceedings, Part I, LNCS 10981, Springer, pp.
     124–143, doi:10.1007/978-3-319-96145-3 7.
[15] Erich Grädel, Wolfgang Thomas & Thomas Wilke, editors (2002): Automata, Logics, and Infinite Games: A
     Guide to Current Research. LNCS 2500, Springer, doi:10.1007/3-540-36387-4.
[16] H. Hojjat & P. Rümmer (2018): The ELDARICA Horn Solver. In: 2018 Formal Methods in Computer Aided
     Design (FMCAD), pp. 1–7, doi:10.23919/FMCAD.2018.8603013.
[17] Youkichi Hosoi, Naoki Kobayashi & Takeshi Tsukada (2019): A Type-Based HFL Model Checking Algo-
     rithm. In Anthony Widjaja Lin, editor: Programming Languages and Systems - 17th Asian Symposium,
     APLAS 2019, Nusa Dua, Bali, Indonesia, December 1-4, 2019, Proceedings, Lecture Notes in Computer
     Science 11893, Springer, pp. 136–155, doi:10.1007/978-3-030-34175-6 8.
N. Kobayashi                                                                                                11


[18] Naoki Iwayama, Naoki Kobayashi, Ryota Suzuki & Takeshi Tsukada (2020): Predicate Abstraction and
     CEGAR for νHFLZ Validity Checking. In David Pichardie & Mihaela Sighireanu, editors: Static Analysis
     - 27th International Symposium, SAS 2020, Virtual Event, November 18-20, 2020, Proceedings, Lecture
     Notes in Computer Science 12389, Springer, pp. 134–155, doi:10.1007/978-3-030-65474-0 7.
[19] Joxan Jaffar, Andrew E. Santosa & Razvan Voicu (2006): A CLP Method for Compositional and Intermittent
     Predicate Abstraction. In: Proceedings of VMCAI 2006, Lecture Notes in Computer Science 3855, Springer,
     pp. 17–32, doi:10.1007/11609773 2.
[20] Hiroyuki Katsura, Naoki Iwayama, Naoki Kobayashi & Takeshi Tsukada (2020): A New Refinement Type
     System for Automated νHFLZ Validity Checking. In Bruno C. d. S. Oliveira, editor: Programming Lan-
     guages and Systems - 18th Asian Symposium, APLAS 2020, Fukuoka, Japan, November 30 - December
     2, 2020, Proceedings, Lecture Notes in Computer Science 12470, Springer, pp. 86–104, doi:10.1007/978-3-
     030-64437-6 5.
[21] Naoki Kobayashi (2013):          Model    Checking    Higher-Order    Programs.        J.   ACM     60(3),
     doi:10.1145/2487241.2487246.
[22] Naoki Kobayashi (2016): HorSat 2: A Saturation-Based Model Checker for Higher-Order Recursion
     Schemes. Available at https://github.com/hopv/horsat2.
[23] Naoki Kobayashi, Grigory Fedyukovich & Aarti Gupta (2020): Fold/Unfold Transformations for Fixpoint
     Logic. In Armin Biere & David Parker, editors: Tools and Algorithms for the Construction and Analysis
     of Systems - 26th International Conference, TACAS 2020, Held as Part of the European Joint Conferences
     on Theory and Practice of Software, ETAPS 2020, Dublin, Ireland, April 25-30, 2020, Proceedings, Part II,
     Lecture Notes in Computer Science 12079, Springer, pp. 195–214, doi:10.1007/978-3-030-45237-7 12.
[24] Naoki Kobayashi, Étienne Lozes & Florian Bruse (2017): On the relationship between higher-order recursion
     schemes and higher-order fixpoint logic. In: POPL 2017, pp. 246–259, doi:10.1145/3009837.3009854.
[25] Naoki Kobayashi, Takeshi Nishikawa, Atsushi Igarashi & Hiroshi Unno (2019): Temporal Verification of
     Programs via First-Order Fixpoint Logic. In Bor-Yuh Evan Chang, editor: Static Analysis - 26th Interna-
     tional Symposium, SAS 2019, Porto, Portugal, October 8-11, 2019, Proceedings, Lecture Notes in Computer
     Science 11822, Springer, pp. 413–436, doi:10.1007/978-3-030-32304-2 20.
[26] Naoki Kobayashi, Ryosuke Sato & Hiroshi Unno (2011): Predicate Abstraction and CEGAR for Higher-
     Order Model Checking. In: PLDI 2011, ACM Press, pp. 222–233, doi:10.1145/1993498.1993525.
[27] Naoki Kobayashi, Takeshi Tsukada & Keiichi Watanabe (2018): Higher-Order Program Verification via
     HFL Model Checking. In Amal Ahmed, editor: Programming Languages and Systems - 27th European
     Symposium on Programming, ESOP 2018, Held as Part of the European Joint Conferences on Theory and
     Practice of Software, ETAPS 2018, Thessaloniki, Greece, April 14-20, 2018, Proceedings, Lecture Notes in
     Computer Science 10801, Springer, pp. 711–738, doi:10.1007/978-3-319-89884-1 25.
[28] Anvesh Komuravelli, Arie Gurfinkel & Sagar Chaki (2016): SMT-based model checking for recursive pro-
     grams. Formal Methods Syst. Des. 48(3), pp. 175–205, doi:10.1007/s10703-016-0249-4.
[29] Mayuko Kori, Takeshi Tsukada & Naoki Kobayashi (2021): A Cyclic Proof System for HFLN . In Christel
     Baier & Jean Goubault-Larrecq, editors: 29th EACSL Annual Conference on Computer Science Logic,
     CSL 2021, January 25-28, 2021, Ljubljana, Slovenia (Virtual Conference), LIPIcs 183, Schloss Dagstuhl -
     Leibniz-Zentrum für Informatik, pp. 29:1–29:22, doi:10.4230/LIPIcs.CSL.2021.29.
[30] Dexter Kozen (1983): Results on the Propositional µ-calculus. Theoretical Computer Science 27, pp. 333–
     354, doi:10.1016/0304-3975(82)90125-6.
[31] Takuya Kuwahara, Ryosuke Sato, Hiroshi Unno & Naoki Kobayashi (2015): Predicate Abstraction and
     CEGAR for Disproving Termination of Higher-Order Functional Programs. In: Proceedings of CAV 2015,
     LNCS 9207, Springer, pp. 287–303, doi:10.1007/978-3-319-21668-3 17.
[32] Takuya Kuwahara, Tachio Terauchi, Hiroshi Unno & Naoki Kobayashi (2014): Automatic Termination Veri-
     fication for Higher-Order Functional Programs. In: Proceedings of ESOP 2014, LNCS 8410, Springer, pp.
     392–411, doi:10.1007/978-3-642-54833-8 21.
12                                                                            HFL Model Checking Project


[33] Akihiro Murase, Tachio Terauchi, Naoki Kobayashi, Ryosuke Sato & Hiroshi Unno (2016): Temporal veri-
     fication of higher-order functional programs. In Rastislav Bodı́k & Rupak Majumdar, editors: Proceedings
     of the 43rd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL
     2016, St. Petersburg, FL, USA, January 20 - 22, 2016, ACM, pp. 57–68, doi:10.1145/2837614.2837667.
[34] C.-H. Luke Ong (2006): On Model-Checking Trees Generated by Higher-Order Recursion Schemes. In:
     LICS 2006, IEEE Computer Society Press, pp. 81–90, doi:10.1109/LICS.2006.38.
[35] C.-H. Luke Ong & Dominik Wagner (2019): HoCHC: A Refutationally Complete and Semantically In-
     variant System of Higher-order Logic Modulo Theories. In: 34th Annual ACM/IEEE Symposium on
     Logic in Computer Science, LICS 2019, Vancouver, BC, Canada, June 24-27, 2019, IEEE, pp. 1–14,
     doi:10.1109/LICS.2019.8785784.
[36] Julio C. Peralta, John P. Gallagher & Hüseyin Saglam (1998): Analysis of Imperative Programs through
     Analysis of Constraint Logic Programs. In: Proceedings of SAS ’98, Lecture Notes in Computer Science
     1503, Springer, pp. 246–261, doi:10.1007/3-540-49727-7 15.
[37] Andreas Podelski & Andrey Rybalchenko (2004): Transition Invariants. In: 19th IEEE Symposium
     on Logic in Computer Science (LICS 2004), 14-17 July 2004, Turku, Finland, Proceedings, pp. 32–41,
     doi:10.1109/LICS.2004.1319598.
[38] Patrick M. Rondon, Ming Kawaguchi & Ranjit Jhala (2008): Liquid types. In: PLDI 2008, pp. 159–169,
     doi:10.1145/1375581.1375602.
[39] Yuki Satake, Hiroshi Unno & Hinata Yanagi (2020): Probabilistic Inference for Predicate Constraint Satis-
     faction. In: The Thirty-Fourth AAAI Conference on Artificial Intelligence, AAAI 2020, The Thirty-Second
     Innovative Applications of Artificial Intelligence Conference, IAAI 2020, The Tenth AAAI Symposium on
     Educational Advances in Artificial Intelligence, EAAI 2020, New York, NY, USA, February 7-12, 2020,
     AAAI Press, pp. 1644–1651, doi:10.1609/aaai.v34i02.5526.
[40] Takeshi Tsukada (2020): On Computability of Logical Approaches to Branching-Time Property Verification
     of Programs. In Holger Hermanns, Lijun Zhang, Naoki Kobayashi & Dale Miller, editors: LICS ’20: 35th
     Annual ACM/IEEE Symposium on Logic in Computer Science, Saarbrücken, Germany, July 8-11, 2020,
     ACM, pp. 886–899, doi:10.1145/3373718.3394766.
[41] Hiroshi Unno & Naoki Kobayashi (2009): Dependent type inference with interpolants. In: Proceedings of
     the 11th International ACM SIGPLAN Conference on Principles and Practice of Declarative Programming,
     September 7-9, 2009, Coimbra, Portugal, ACM, pp. 277–288, doi:10.1145/1599410.1599445.
[42] Hiroshi Unno, Tachio Terauchi & Naoki Kobayashi (2013): Automating relatively complete verification of
     higher-order functional programs. In Roberto Giacobazzi & Radhia Cousot, editors: The 40th Annual ACM
     SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL ’13, Rome, Italy - January
     23 - 25, 2013, ACM, pp. 75–86, doi:10.1145/2429069.2429081.
[43] M. Viswanathan & R. Viswanathan (2004): A Higher Order Modal Fixed Point Logic. In: CONCUR, LNCS
     3170, Springer, pp. 512–528, doi:10.1007/978-3-540-28644-8 33.
[44] Keiichi Watanabe, Takeshi Tsukada, Hiroki Oshikawa & Naoki Kobayashi (2019): Reduction from
     branching-time property verification of higher-order programs to HFL validity checking. In Manuel V.
     Hermenegildo & Atsushi Igarashi, editors: Proceedings of the 2019 ACM SIGPLAN Workshop on Partial
     Evaluation and Program Manipulation, PEPM@POPL 2019, Cascais, Portugal, January 14-15, 2019, ACM,
     pp. 22–34, doi:10.1145/3294032.3294077.
[45] Hongwei Xi & Frank Pfenning (1999): Dependent Types in Practical Programming. In: Proceedings of
     POPL, pp. 214–227, doi:10.1145/292540.292560.
