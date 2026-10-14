                                         An Efficient VCGen-based Modular Verification
                                                    of Relational Properties ⋆

                                                 Lionel Blatter1,2 , Nikolai Kosmatov3,4, Virgile Prevosto3, and
                                                                          Pascale Le Gall5
arXiv:2401.08385v1 [cs.SE] 16 Jan 2024




                                                   1
                                                     Karlsruhe Institute of Technology, 76131, Karlsruhe, Germany
                                                                    firstname.lastname@kit.edu
                                             2
                                               Max Planck Institute for Security and Privacy, 44799, Bochum, Germany
                                                   3
                                                      Université Paris-Saclay, CEA, List, 91120, Palaiseau, France
                                                                     firstname.lastname@cea.fr
                                                     4
                                                       Thales Research & Technology, 91120, Palaiseau, France
                                               5
                                                 CentraleSupélec, Université Paris-Saclay, 91190 Gif-sur-Yvette France
                                                             firstname.lastname@centralesupelec.fr

                                               Abstract Deductive verification typically relies on function contracts
                                               that specify the behavior of each function for a single function call. Re-
                                               lational properties link several function calls together within a single
                                               specification. They can express more advanced properties of a given
                                               function, such as non-interference, continuity, or monotonicity, or relate
                                               calls to different functions, possibly run in parallel, for instance, to show
                                               the equivalence of two implementations. However, relational properties
                                               cannot be expressed and verified directly in the traditional setting of
                                               modular deductive verification. Recent work proposed a new technique
                                               for relational property verification that relies on a verification condition
                                               generator to produce logical formulas that must be verified to ensure a
                                               given relational property. This paper presents an overview of this ap-
                                               proach and proposes important enhancements. We integrate an optim-
                                               ized verification condition generator and extend the underlying theory
                                               to show how relational properties can be proved in a modular way, where
                                               one relational property can be used to prove another one, like in modular
                                               verification of function contracts. Our results have been fully formalized
                                               and proved sound in the Coq proof assistant.



                                         1   Introduction
                                         Modular deductive verification [19] is used to prove that every function f of a
                                         given program respects its contract. Such a contract is, basically, an implication:
                                         if the given precondition is true before a call to f and the call terminates6 , the
                                         given postcondition is true when f returns control to the caller. However, some
                                         ⋆
                                           This version of the contribution has been accepted for publication, after peer re-
                                           view (when applicable) but is not the Version of Record and does not reflect post-
                                           acceptance improvements, or any corrections. The Version of Record is available
                                           online at: https://doi.org/10.1007/978-3-031-19849-6 28.
                                         6
                                           Termination can be either assumed (partial correctness) or proved separately (full
                                           correctness) in a classical way [16]; for the purpose of this paper we can assume it.
//Command csum :       Relational property R1 between commands c1ω and c2ω :
if x1 < x2 then {
     x3 := x3 + x1 ;                        // c1ω :          // c2ω :
     x1 := x1 + 1;                         x1 := 1;          x1 := 0;       
                           x2 h1i= x2 h2i               h1i ∼             h2i x3 h1i= x3 h2i
     call(ysum )                            x3 := 0;          x3 := 0;
} else { skip }                             call(ysum )       call(ysum )
Figure 1: Recursive command csum , associated as a body with procedure name
ysum , and relational property R1 between two commands, denoted c1ω and c2ω ,
involving a call to this procedure.

kinds of properties are not easily reducible to a single function call. Indeed, it
is often necessary to express a property that involves several functions, possibly
executed in parallel, or relates the results of several calls to the same function
for different arguments. Such properties are known as relational properties [6].
    Examples of such relational properties include monotonicity (i.e. x ≤ y ⇒
f (x) ≤ f (y)), involving 2 calls, or transitivity (cmp(x, y) ≥ 0 ∧ cmp(y, z) ≥ 0 ⇒
cmp(x, z) ≥ 0), involving 3 calls. In secure information flow [3], non-interference
is also a relational property. Namely, given a partition of program variables
between high-security variables and low-security variables, a program is said to
be non-interferent if any two executions starting from states in which the low-
security variables have the same initial values will end up in a final state where
the low-security variables have the same values. In other words, high-security
variables cannot interfere with low-security ones.

Motivation. Lack of support for relational properties in verification tools was
already faced by industrial users (e.g. in [8] for C programs). The usual way to
deal with this limitation is to use self-composition [3,30,9], product programs [2]
or other self-composition variants [31]. Those techniques are based on code trans-
formations that are relatively tedious and error-prone. Moreover, they are hardly
applicable in practice to real-life programs with pointers like in C. Namely, self-
composition requires that the compared executions operate on completely sep-
arated (i.e. disjoint) memory areas, which might be extremely difficult to ensure
for complex programs with pointers. Modular verification of relational proper-
ties is another important feature: the user may want to rely on some relational
properties in order to verify some other ones.
Example 1 (relational property). Figure 1 shows an example of a recursive com-
mand (that is, program) csum . We clearly distinguish the name and the body of
a procedure. The procedure named ysum is assumed to have command csum as
its body, so that csum recursively calls itself. Given three global integer variables
x1 , x2 and x3 , command csum adds to x3 (used as an accumulator) the sum
x1 + (x1 + 1) + · · · + (x2 − 1) if x1 < x2 , and has no effect otherwise.
    Figure 1 also shows an example of a relational property R1 (inspired by [2])
stating the equivalence of two commands c1ω and c2ω (assumed to be run on sep-
arate memory states), which assign x1 and x3 before calling ysum . The relational
property is written here in Benton’s notation [6]: tags h1i and h2i are used to
distinguish the programs linked by the property. When variables of the linked

                                               2
programs have the same names, such a tag after a variable name also helps to
distinguish the instance of the variable used in the relational precondition and
postcondition (written in curly braces, resp., on the left and on the right). Prop-
erty R1 states that if x2 has the same value before the execution of c1ω and before
the execution of c2ω , then x3 will have the same value after their executions. In-
deed, c1ω will compute in x3 the sum 1 + 2 + · · · + (x2 − 1), while c2ω will compute
in x3 the sum 0 + 1 + 2 + · · · + (x2 − 1).
    In this paper, we will show how relational property R1 can be verified using
another relational property R3 linking two runs of csum rather than using a full
functional contract of csum . More precisely, R3 (that will be formally defined
below in Fig. 5) generalizes the situation of R1 and states that the resulting
value of x3 after two runs of csum will be the same if the initial state of the
second run is exactly one iteration of csum behind that of the first run.          ⊓
                                                                                   ⊔


Approach. Our recent work [11] proposed an alternative to self-composition that
is not based on code transformation or relational rules. It directly relies on a
standard verification condition generator (VCGen) to produce logical formulas
to be verified (typically, with an automated prover) to ensure a given relational
property. This approach requires no extra code processing (such as sequential
composition of programs or variable renaming). Moreover, no additional separ-
ation hypotheses are required. The locations of each program are separated by
construction: each program has its own memory state. This approach has been
formalized on a minimal language L, representative of the main issues relevant
for relational property verification. L is a standard While language extended
with annotations, procedures and pointers. Notably, the presence of dereferences
and address-of operations makes it representative of various aliasing problems
with (possibly, multiple) pointer dereferences of a real-life language like C. An
example of a relational property for programs with pointers was given in [11].
We formalize the proposed approach and prove its soundness in the Coq proof
assistant [33]. Our Coq development7 contains about 3700 lines.

Contributions. We give an overview of the VCGen-based approach for relational
property verification (presented in [11]) and enhance the underlying theory with
several new features. The new technical contributions of this paper include:

 – a Coq formalization and proof of soundness of an optimized VCGen for
   language L, and its extension to the verification of relational properties;
 – an extension of the framework allowing not only to prove relational proper-
   ties, but also to use them as hypotheses in the following proofs;
 – a Coq formalization of the extended theory.

We also provide an illustrative example and, as another minor extension, add
the capacity to refer to old values of variables in postconditions.
7
    Available at https://github.com/lyonel2017/Relational-Spec/.


                                         3
Outline. Section 2 introduces the imperative language L used in this work. Func-
tional correctness is defined in Section 3. The extension of functional correctness
to relational properties is presented in Section 4. Then, we prove the soundness
of an optimized VCGen in Section 5, and show how it can be soundly extended
to verify relational properties in Section 6. Finally, we present related work in
Section 7 and concluding remarks in Section 8.

2     Syntax and Semantics of the Considered Language L
2.1   Locations, States, and Procedure Contracts
We denote by N = {0, 1, 2, . . . } the set of natural numbers, by N∗ = {1, 2, . . . }
the set of nonzero natural numbers, and by B = {True, False} the set of Boolean
values. Let X be the set of program locations and Y the set of program (procedure)
names, and let x, x′ , x1 , ... and y, y ′ , y1 , ... denote metavariables ranging over
those respective sets. We assume that there exists a bijective function N → X,
so that X = {xi | i ∈ N}. Intuitively, we can see i as the address of location xi .
    Let Σ be the set of functions σ : N → N, called memory states, and let
σ, σ ′ , σ1 , ... denote metavariables ranging over Σ. A state σ maps a location to
a value using its address: location xi has value σ(i).
    We define the update operation of a memory state set(σ, i, n), also denoted
by σ[i/n], as the memory state σ ′ mapping each address to the same value as σ,
except for i, bound to n. Formally, set(σ, i, n) is defined by the following rules:

              ∀σ ∈ Σ, xi ∈ X, n ∈ N, xj ∈ X. i = j ⇒ σ[i/n](j) = n,                (1)
            ∀σ ∈ Σ, xi ∈ X, n ∈ N, xj ∈ X. i 6= j ⇒ σ[i/n](j) = σ(j).              (2)

    Let Ψ be the set of functions ψ : Y → C, called procedure environments,
mapping program names to commands (defined below), and let ψ, ψ1 , ... denote
metavariables ranging over Ψ . We write bodyψ (y) to refer to ψ(y), the commands
(or body) of procedure y in a given procedure environment ψ. An example of a
procedure environment ψsum is given in Fig. 5, where bodyψsum (ysum ) = csum .
    Preconditions (or assertions) are predicates of arity one, taking as para-
meter a memory state and returning an equational first-order logic formula. Let
metavariables P, P1 , ... range over the set P of preconditions. For instance, us-
ing λ-notation, precondition P assessing that location x3 is bound to 2 can be
defined by P , λσ.σ(3) = 2. This form will be more convenient for relational
properties (than e.g. x3 = 2) as it makes explicit the memory states on which a
property is evaluated.
    Postconditions are predicates of arity two, taking as parameters two memory
states and returning an equational first-order logic formula. Its two arguments
refer to the initial and the final state. For instance, postcondition Q assessing
that location x1 was incremented (that is, x1 = old(x1 ) + 1) can be defined in
λ-notation by Q , λσσ ′ . σ ′ (1) = σ(1) + 1. Let metavariables Q, Q2 , ... range over
the set Q of postconditions.
    Finally, we define the set Φ of contract environments φ : Y → P × Q, and
metavariables φ, φ1 , ... to range over Φ. More precisely, φ maps a procedure name

                                          4
a : := n         natural const.
                                           c : := skip                         do nothing
  |x                      location
                                             | x := a                 direct assignment
  | ∗x                 dereference
                                             | ∗ x := a             indirect assignment
  | &x                    address
                                             | c1 ; c2                           sequence
  | a1 op a a2    arithm. oper.
                                             | assert(P )                        assertion
                                             | if b then {c1 } else {c2 }       condition
b : := true | f alse    Boolean const.
                                             | while b inv P do {c1 }                loop
  | a1 op b a2              comparison
                                             | call(y)                      procedure call
  | b1 op l b2 | ¬b1         logic oper.

 Figure 2: Syntax of arithmetic and Boolean expressions and commands in L.

y to the associated (procedure) contract φ(y) = (preφ (y), postφ (y)), composed
of a pre- and a postcondition for procedure y. As usual, a procedure contract
will allow us to specify the behavior of a single procedure call, that is, if we start
executing y in a memory state satisfying preφ (y), and the evaluation terminates,
the pair composed of the initial and final states will satisfy postφ (y).

2.2    Syntax for Expressions and Commands
Let Ea , Eb and C denote respectively the sets of arithmetic expressions, Boolean
expressions and commands. We denote by a, a1 , ...; b, b1 , ... and c, c1 , ... metav-
ariables ranging, respectively, over those sets. Syntax of arithmetic and Boolean
expressions is given in Fig. 2. Constants are natural numbers or Boolean values.
Expressions use standard arithmetic, comparison and logic binary operators, de-
noted respectively op a ::= {+, ×, −}, op b ::= {6, =, . . . }, op l ::= {∨, ∧}.
Since we use natural values, the subtraction is bounded by 0, as in Coq: if
n′ > n, the result of n − n′ is considered to be 0. Expressions also include
locations, possibly with a dereference or address operators.
    Figure 2 also presents the syntax of commands in L. Sequences, skip and con-
ditions are standard. An assignment can be done to a location directly or after
a dereference. Recall that a location xi contains as a value a natural number,
say v, that can be seen in turn as the address of a location, namely xv , so the
assignment ∗xi := a writes the value of expression a to the location xv , while
the address operation &xi computes the address i of xi . An assertion command
assert(P ) indicates that an assertion P should be valid at the point where the
command occurs. The loop command while b inv P do {c1 } is always annot-
ated with an invariant P . As usual, this invariant should hold when we reach the
command and be preserved by each loop step. Command call(y) is a procedure
call. All annotations (assertions, loop invariants and procedure contracts) will
be ignored during the program execution and will be relevant only for program
verification in Section 5. Procedures do not have explicit parameters and return
values (hence we use the term procedure call rather than function call ). Instead,
as in assembly code [23], parameters and return value(s) are shared implicitly
between the caller and the callee through memory locations: the caller must

                                            5
      ξa JnKσ , n         ξa Jxi Kσ , σ(i)      ξa J∗xi Kσ , σ(σ(i))      ξa J&xi Kσ , i
               Figure 3: Evaluation of expressions in L (selected rules).
                                                                                            ψ
                          ξa JaKσ = n               ξa JaKσ = n           hbodyψ (y), σ1 i → σ2
               ψ
hassert(P ), σi → σ               ψ                        ψ                            ψ
                      hxi := a, σi → σ[i/n]   h∗xi := a, σi → σ[σ(i)/n]    hcall(y), σ1 i → σ2
         Figure 4: Operational semantics of commands in L (selected rules).

put/read the right values at the right locations before/after the call. Finally, to
avoid ambiguity, we regroup sequences of commands with { }.
2.3      Operational Semantics
Evaluation of arithmetic and Boolean expressions in L is defined by functions ξa
and ξb . Selected evaluation rules for arithmetic expressions are shown in Fig. 3.
Operations ∗xi and &xi have a semantics similar to the C language, i.e. derefer-
encing and address-of. Semantics of Boolean expressions is standard [36].
    Based on these evaluation functions, we can define the operational semantics
of commands in a given procedure environment ψ. Selected evaluation rules8 are
shown in Fig. 4. As said above, both assertions and loop invariants can be seen
as program annotations that do not influence the execution of the program itself.
Hence, command assert(P ) is equivalent to a skip. Likewise, loop invariant P
has no influence on the semantics of while b inv P do {c}.
                             ψ                                    ψ
   We write      hc, σi → σ ′ to denote that hc, σi → σ ′ can be derived from
the rules of Fig. 4. Our Coq formalization, inspired by [29], provides a deep
embedding of L, with an associated parser, in files Aexp.v, Bexp.v and Com.v.

3      Functional Correctness
We define functional correctness in a similar way to the original Hoare triple
definition [19], except that we also need a procedure environment ψ, leading to a
quadruple denoted ψ : {P }c{Q}. We will however still refer by the term “Hoare
triple” to the corresponding program property, formally defined as follows.

Definition 1 (Hoare triple). Let c be a command, ψ a procedure environment,
and P and Q two assertions. We define a Hoare triple ψ : {P }c{Q} as follows:
                                                                  ψ
           ψ : {P }c{Q} , ∀σ, σ ′ ∈ Σ. P (σ) ∧ ( hc, σi → σ ′ ) ⇒ Q(σ, σ ′ ).

   Informally, our definition states that, for a given ψ, if a state σ satisfies P
and the execution of c on σ terminates in a state σ ′ , then (σ, σ ′ ) satisfies Q.

Example 2. Figure 5 gives an example of a Hoare triple denoted R2 .                              ⊓
                                                                                                 ⊔

   Next, we introduce notation CV (ψ, φ) to denote the fact that, for the given
φ and ψ, every procedure satisfies its contract.
 8
     For convenience of the reviewers, full versions of Fig. 3, 4 are given in Appendix A.


                                                6
Procedure environment:                              ψsum , {ysum → csum }
                                        
                                            True csum old(x1 ) > old(x2 ) ⇒ old(x3 ) = x3
                                                     
Hoare triple R2 :              ψsum :
                                                    
                           
                            x1 h2i< x2 h2i ∧        
                                                     
Relational                   x2 h1i= x2 h2i ∧
                                                                        
                    ψsum :                             csum h1i ∼ csum h2i x3 h1i= x3 h2i
property R3 :              
                            x 1 h1i= x 1 h2i + 1 ∧  
                                                     
                             x3 h1i= x3 h2i + x1 h2i
                                                    

Figure 5: A procedure environment ψsum associating procedure name ysum with
its body csum (see Fig. 1), a Hoare triple R2 for command csum , and a relational
property R3 linking two runs of csum .

Definition 2 (Contract Validity). Let ψ be a procedure environment and φ
a contract environment. We define contract validity CV (ψ, φ) as follows:

                CV (ψ, φ) , ∀y ∈ Y. ψ : {preφ (y)}call(y){postφ (y)}).

    The notion of contract validity is at the heart of modular verification, since it
allows assuming that the contracts of the callees are satisfied during the verifica-
tion of a Hoare triple. More precisely, to state the validity of procedure contracts
without assuming anything about their bodies in our formalization, we will con-
sider an arbitrary choice of implementations ψ ′ of procedures that satisfy the
contracts, like in the first assumption of Theorem 1 below. This theorem, taken
from [1, Th. 4.2] and reformulated for L in [11], states that ψ : {P }c{Q} holds if
we can prove the contract of (the bodies in ψ of) all procedures in an arbitrary
environment ψ ′ respecting the contracts, and if the validity of contracts of φ for
ψ implies the Hoare triple itself. This theorem is the basis for modular verifica-
tion of Hoare Triples, as done for instance in Hoare Logic [19,36] or verification
condition generation.

Theorem 1 (Recursion). Given a procedure environment ψ and a contract
environment φ such that the following two assumptions hold:

       ∀ψ ′ ∈ Ψ. CV (ψ ′ , φ) ⇒ ∀y ∈ Y, ψ ′ : {preφ (y)}bodyψ (y){postφ (y)},
                              CV (ψ, φ) ⇒ ψ : {P }c{Q},

we have ψ : {P }c{Q}.

   We refer the reader to the Coq development, more precisely the results
recursive_proc and recursive_hoare_triple in file Hoare_Triple.v for a
complete proof of Theorem 1.

4    Relational Functional Correctness
Relational properties can be seen as an extension of Hoare triples. But, instead of
linking one program with two properties, the pre- and postconditions, relational
properties link n programs to two properties, called relational precondition and

                                                7
relational postcondition. A relational precondition or assertion (resp., relational
postcondition) for n programs is a predicate taking a sequence of n (resp., 2n)
memory states and returning a first-order logic formula. Metavariables Pb , P        c′ , . . .
         b Q
(resp., Q, c′ , . . . ) range over the corresponding sets. As a simple example, the
relational postcondition of R1 (written in Fig. 1 in Benton’s notation) can be
stated in λ-notation as follows: λσ1 , σ2 , σ1′ , σ2′ . σ1′ (3) = σ2′ (3).
    A relational property is a property about n programs c1 , ..., cn , stating that if
each program ci starts in a state σi and ends in a state σi′ such that Pb (σ1 , ..., σn )
              b 1 , ..., σn , σ ′ , ..., σ ′ ) holds, where Pb is a relational precondition
holds, then Q(σ                   1       n
       b
and Q is a relational postcondition. We formally define relational correctness
similarly to functional correctness (cf. Def. 1), except that we now use sequences
of commands and memory states. We abbreviate by (uk )n a sequence of elements
(uk )nk=1 = (u1 , . . . , un ), where k ranges from 1 to n. If n ≤ 0, (uk )n is the empty
sequence denoted [ ]. If n = 1, (u)1 is the singleton sequence (u).
Definition 3 (Relational Hoare Triple). Let ψ be a procedure environment,
(ck )n a sequence of n commands (n ∈ N∗ ), Pb and Q   b relational pre- and post-
condition for n commands. The relational correctness of (ck )n with respect to Pb
and Q,b denoted ψ : {Pb}(ck )n {Q},
                                b is defined as follows:

                                       ψ : {Pb}(ck )n {Q}
                                                        b ,
                                            n
                                            ^               ψ
       ∀(σk )n , (σk′ )n . Pb ((σk )n ) ∧ (                             b k )n , (σ ′ )n ).
                                                 hci , σi i → σ ′ i ) ⇒ Q((σ       k
                                         i=1

   For n = 1, this notion defines a Hoare triple. It also generalizes Benton’s
notation [6] for two commands: ψ : {Pb}c1 ∼ c2 {Q}.
                                                b As Benton’s work mostly
focused on comparing equivalent programs, using symbol ∼ was quite natural.
Example 3. Relational property R3 introduced in Ex. 1 is formalized (in Benton’s
notation) in Fig. 5. Below, we will illustrate modular verification of relational
properties by deducing R1 from R3 and partial contract R2 of csum .            ⊓
                                                                               ⊔
    We will now extend Theorem 1 to relational contract environments. A re-
lational contract environment φb maps a sequence of program names (yk )n to
a relational contract, composed of a relational pre- and postcondition, denoted
b k )n ) = ( pre
φ((y                           d b((yk )n ) ). Practical applications require only a
                c φb((yk )n ), postφ
finite number of properties, so the relational contract can be assumed trivial for
all except a finite number of sequences. A relational contract environment gener-
alizes a contract environment, since a standard procedure contract is a relational
contract (for a sequence of exactly one element). Notice that φb considers only
one relational property for a given sequence (yk )n : this is not a limitation since
several properties can be encoded in one contract. We define the set of relational
contract environments Φ,  b and metavariables φ, b φb0 , φb1 , ... will range over Φ.
                                                                                   b
                                      b
    We introduce notation CVr (ψ, φ) to denote the fact that all procedures
defined in ψ satisfy the relational contracts in which they are involved in φ.        b



                                                8
Definition 4 (Relational Contract Validity). Let ψ be a procedure envir-
onment and φb a relational contract environment. We define CVr (ψ, φ)
                                                                   b as follows:
        b , ∀(yk )n ∈ dom(φ),
CVr (ψ, φ)                b n > 0 ⇒ ψ : {pre                            d b((yk )n )}.
                                         c φb((yk )n )}(call(yk ))nk=1 {postφ

Theorem 2 (Relational Recursion). Given a procedure environment ψ and
a relational contract environment φb such that the following two assumptions hold:
                                           b ⇒
                         ∀ψ ′ ∈ Ψ. CVr (ψ, φ)
            n      b ψ : {pre
      ∀(yk ) ∈ dom(φ),     ′                              d b((yk )n )},
                          c φb((yk ) )}(bodyψ (yk ))nk=1 {post
                                    n
                                                              φ

                                  b ⇒ ψ : {Pb }(ck )n {Q}
                          CVr (ψ, φ)                   b

then we have ψ : {Pb }(ck )n {Q}.
                              b

   The Coq proof (which is a straightforward extension of the proof of The-
orem 1) is available in Rela.v, Theorem recursion relational.

5    Optimized Verification Condition Generator
A standard way [16] for verifying that a Hoare triple holds is to use a verification
condition generator (VCGen). In this section, we formalize a VCGen for Hoare
triples such that if all verification conditions that it generates are valid, then the
Hoare triple is valid according to Def. 1. The VCGen described in this section is
based on optimizations introduced in [15]. Such optimizations allow the VCGen
to return formulas whose size is linear with respect to the size of the program
itself, and are now part of any state-of-the-art deductive verification tool. The
key idea is to avoid splitting verification condition generation into two separ-
ated sub-generation at each conditional. The definition is formalized in Coq in
the file Vcg Opt.v, where we also prove that the verification conditions of this
optimized VCGen imply those of the naive VCGen presented in [11]. This will
allow us to use the optimized VCGen (or more generally any VCGen satisfy-
ing the properties stated in Theorem 3 below) for the verification of relational
properties as well (see Section 6).

5.1 Verification Condition Generator
When defining the naive VCGen in [11], we proposed a modular definition.
Namely, we divided it into three functions Tc , Ta and Tf . Here, we follow the
same approach for the optimized VCGen, using three new functions Tc⊲ , Ta⊲ ,
and Tf⊲ :

 – function Tc⊲ generates the main verification condition, expressing that the
   postcondition holds in the final state, assuming auxiliary annotations hold;
 – function Ta⊲ generates auxiliary verification conditions stemming from as-
   sertions, loop invariants, and preconditions of called procedures;
 – finally, function Tf⊲ generates verification conditions for the auxiliary pro-
   cedures that are called by the main program, to ensure that their bodies
   respect their contracts.

                                          9
                         Tc⊲ JskipK(σ, σ ′ , φ, f ) , f (σ = σ ′ )
                      Tc⊲ Jxi := aK(σ, σ ′ , φ, f ) , f (σ ′ = set(σ, i, ξa JaKσ))
                     Tc⊲ J∗xi := aK(σ, σ ′ , φ, f ) , f (σ ′ = set(σ, σ(i), ξa JaKσ))
                  Tc⊲ Jassert(P )K(σ, σ ′ , φ, f ) , f (P (σ) ∧ σ = σ ′ )
                         Tc⊲ Jc0 ; c1 K(σ, σ ′ , φ, f ) , ∀σ ′′ , Tc⊲ Jc0 K(σ, σ ′′ , φ, λp1 .
                                                      Tc⊲ Jc1 K(σ ′′ , σ ′ , φ, λp2 .f (p1 ∧ p2 )))
 Tc⊲ Jif b then {c0 } else {c1 }K(σ, σ ′ , φ, f ) , Tc⊲ Jc0 K(σ, σ ′ , φ, λp1 .
                                                      Tc⊲ Jc1 K(σ, σ ′ , φ, λp2 .
                                                      f ((b ≡ True ⇒ p1 ) ∧ (b ≡ False ⇒ p2 ))))
                      Tc⊲ Jcall(y)K(σ, σ ′ , φ, f ) , f (preφ (y)(σ) ∧ posty (φ)(σ, σ ′ ))
  Tc⊲ Jwhile b inv inv do {c}K(σ, σ ′ , φ, f ) , f (inv σ ∧ inv σ ′ ∧ ¬(ξb JbKσ ′ ))
Figure 6: Definition of function Tc⊲ generating the main verification condition.
Definition 5 (Function Tc⊲ generating the main verification condition).
Given a command c, two memory states σ and σ ′ , a contract environment φ, and
a function f taking a formula as argument and returning a formula, function
Tc⊲ returns a formula defined by case analysis on c as shown in Fig. 6.
     State σ represents the state before executing the command, while σ ′ rep-
resents the state after it. Intuitively, the argument that gets passed to f is the
formula that relates σ and σ ′ according to c itself. Thus, if f is of the form
λp.p ⇒ Q(σ, σ ′ ), as in Theorem 3 below, the resulting formula is a verification
condition for post-condition Q to hold.
     For skip, which does nothing, both states are identical. For assignments, σ ′
is simply the update of σ. An assertion introduces a hypothesis over σ but leaves
it unchanged. For a sequence, a fresh memory state σ ′′ is introduced, and we
compose the VCGen. For a conditional, if the condition evaluates to True, we
select the condition from the then branch, and otherwise from the else branch.
Note that, contrary to the naive VCGen, we perform a single call to f , ensuring
the linearity of the formula.
     The rule for calls simply assumes that before the call σ satisfies preφ (y)
and after the call σ and σ ′ satisfy postφ (y). Finally, Tc⊲ assumes that, for a
loop, both the initial state σ and the final one σ ′ satisfy the loop invariant.
Additionally, in σ ′ the loop condition evaluates to False. As for an assertion, the
callee’s precondition and the loop invariant are just assumed to be true; function
Ta⊲ , defined below, generates the corresponding proof obligations.
Example 4. For c , if False then {skip} else {x1 := 2} we have:
                   Tc⊲ JcK(σ, σ ′ , φ, λp. p ⇒ σ ′ (1) = 2) ≡
(False ≡ True ⇒ σ = σ ′ ) ∧ (False ≡ False ⇒ σ ′ = set(σ, 1, 2)) ⇒ σ ′ (1) = 2. ⊓
                                                                                ⊔
   Lemma 1 establishes a relation between functions Tc⊲ and Tc : the formulas
generated by Tc⊲ imply the formulas generated by Tc .

                                                    10
                      Ta⊲ JskipK(σ, φ) , True
                    Ta⊲ Jx := aK(σ, φ) , True
                   Ta⊲ J∗x := aK(σ, φ) , True
                Ta⊲ Jassert(P )K(σ, φ) , P (σ)
                     Ta⊲ Jc0 ; c1 K(σ, φ) , Ta⊲ Jc0 K(σ, φ) ∧
                                ∀σ ′ , Tc⊲ Jc0 K(σ, σ ′ , φ, λp. p ⇒ Ta⊲ Jc1 K(σ ′ , φ))
Ta⊲ Jif b then {c0 } else {c1 }K(σ, φ) , (ξb JbKσ ′ ⇒ Ta⊲ Jc0 K(σ, φ)) ∧
                                (¬(ξb JbKσ ′ ) ⇒ Ta⊲ Jc1 K(σ, φ))
                   Ta⊲ Jcall(y)K(σ, φ) , preφ (y)(σ)
 Ta⊲ Jwhile b inv inv do {c}K(σ, φ) , inv(σ) ∧
                                (∀σ ′ , inv(σ ′ ) ⇒ ξb JbKσ ′ ⇒ Ta⊲ JcK(σ ′ , φ)) ∧
                                (∀σ ′ σ ′′ , inv(σ ′ ) ⇒ Tc⊲ JcK(σ ′ , σ ′′ , φ, λp. p ⇒ inv(σ ′′ )))
Figure 7: Definition of function Ta⊲ generating auxiliary verification conditions.

Lemma 1. Given a program c, a procedure contract environment φ, a memory
state σ and an assertion P , if we have ∀σ ′ ∈ Σ, Tc⊲ JcK(σ, σ ′ , φ, λp. p ⇒ P (σ ′ )),
then we have Tc JcK(σ, φ, P ).

Proof. By structural induction over c.                                                              ⊓
                                                                                                    ⊔

Definition 6 (Function Ta⊲ generating the auxiliary verification condi-
tion). Given a command c, a memory state σ representing the state before the
command, and a contract environment φ, function Ta returns a formula defined
by case analysis on c as shown in Fig. 7.

   Basically, Ta⊲ collects all assertions, preconditions of called procedures, as
well as invariant establishment and preservation, and lifts the corresponding
formulas to constraints on the initial state σ through the use of Tc⊲ .
   As for Tc⊲ , the formulas generated by Ta⊲ imply those generated by Ta .

Lemma 2. For a given program c, a procedure contract environment φ, and a
memory state σ, if we have Ta⊲ JcK(σ, φ), then we have Ta JcK(σ, φ).

Proof. By structural induction over c.                                                              ⊓
                                                                                                    ⊔

   Finally, we define the function for generating the conditions for verifying that
the body of each procedure defined in ψ respects its contract defined in φ.

Definition 7 (Function Tf⊲ generating the procedure verification con-
dition). Tf⊲ takes as argument two environments ψ and φ and returns a formula:

 Tf⊲ (φ, ψ) , ∀y, σ, σ ′ . preφ (y)(σ) ⇒
         Ta⊲ Jbodyψ (y)K(σ, φ) ∧ Tc⊲ Jbodyψ (y)K(σ, σ ′ , φ, λp.p ⇒ postφ (y)(σ, σ ′ )).

                                              11
      Finally, the formulas generated by Tf⊲ imply those generated by Tf .
Lemma 3. For a given procedure environment ψ, and a procedure contract en-
vironment φ, if we have Tf⊲ (φ, ψ), then we have Tf (φ, ψ).
Proof. Using Lemmas 1 and 2.                                                                             ⊓
                                                                                                         ⊔
   The definition of the optimized VCGen and its link to the naive version can
be found in file Vcg Opt.v of the Coq development.

5.2       Hoare Triple Verification
Using the VCGen defined in Sec. 5.1, we can state the theorem establishing how
a Hoare Triple can be verified. The proof can be found in file Correct.v of the
Coq development.
Theorem 3 (Soundness of VCGen). Assume that we have Tf⊲ (φ, ψ) and

                                     ∀σ. P (σ) ⇒ Ta⊲ JcK(σ, φ),
                    ∀σ, σ ′ . P (σ) ⇒ Tc⊲ JcK(σ, σ ′ , φ, λp. p ⇒ Q(σ, σ ′ )).

Then we have ψ : {P }c{Q}.
Proof. By soundness of the naive VCGen [11, Th. 3] and Lemmas 1, 2, 3.                                   ⊓
                                                                                                         ⊔

6        Modular Verification of Relational Properties
In this section, we propose a modular verification method for relational proper-
ties (defined in Section 4) using the optimized VCGen defined in Section 5 (or,
more generally, any VCGen respecting Theorem 3). First, we define the function
Tcr⊲ for the recursive call of Tc⊲ on a sequence of commands and memory states.
Definition 8 (Function Tcr⊲ ). Given a sequence of commands (ck )n and a
sequence of memory states (σk )n , a contract environment φ and a function f
taking as argument a formula and returning a formula, function Tcr⊲ is defined
by induction on n for the basis (n = 0) and inductive case (n ∈ N∗ ) as follows:

                                 Tcr⊲ ([ ], [ ], [ ], φ, f ) , f (T rue),
                                 Tcr⊲ ((ck )n , (σk )n , (σk′ )n , φ, f ) ,
Tc⊲ Jcn K(σn , σn′ , φ, λpn . Tcr⊲ ((ck )n−1 , (σk )n−1 , (σk′ )n−1 , φ, λpn−1 . f (pn ∧ pn−1 ))).

   Intuitively, like in Def. 5, the argument that gets passed to f is the formula
that relates the n pre-states (σk )n to the n post-states (σk′ )n when all (ck )n
                                                   b k )n , (σ ′ )n ), the resulting
are executed. Again, if f is of the form λp.p ⇒ Q((σ          k
formula is a verification condition for the relational postcondition Q   b to hold.
More concretely, for n = 2, and f as above, we obtain:
                                                                   b 1 , σ2 ), (σ ′ , σ ′ ))) ≡
             Tcr⊲ ((c1 , c2 ), (σ1 , σ2 ), (σ1′ , σ2′ ), φ, λp.p ⇒ Q((σ          1     2
                                                                          b 1 , σ2 ), (σ ′ , σ ′ )))).
    T ⊲ Jc2 K(σ2 , σ ′ , φ, λp2 .T ⊲ Jc1 K(σ1 , σ ′ , φ, λp1 .p2 ∧ p1 ⇒ Q((σ
     c              2            c               1                                        1    2



                                                     12
    We similarly define a notation for the auxiliary verification conditions for
a sequence of n commands. Basically, this is the conjunction of the auxiliary
verification conditions generated by Ta⊲ on each individual command.

Definition 9 (Function Tar  ⊲
                              ). Given a sequence of commands (ck )n and a
sequence of memory states (σk )n , we define function Tar
                                                        ⊲
                                                          as follows:
                                                           n
                                                           ^
                           ⊲
                         Tar ((ck )n , (σk )n , φ) ,             Ta⊲ Jci K(σi , φ).
                                                           i=1

    A standard contract over a single procedure y can be used directly whenever
there is a call to y. For a relational contract over (yk )n , things are more com-
plicated: there is not a single program point where we can apply the relational
contract. Instead, we have to somehow track in the generated formulas all the
calls that have been made, and to guard the application of the relational contract
by a constraint stating that all the appropriate calls have indeed taken place. In
order to achieve that, we start by defining a notation for the conjunction of a
sequence of procedure calls and associated memory states:

Definition 10 (Functions Pcall and Ppred ).

                                                                           ψ
                            Pcall (y, σ, σ ′ , ψ) ,   hcall(y), σi → σ ′ ,
                                                         ^n
                 Ppred ((yk )n , (σk )n , (σk′ )n , ψ) ,     Pcall (yi , σi , σi′ , ψ).
                                                             i=1

   Then, we can define function Tpr translating relational contracts into a logical
formula, using Ppred to guard its application with tracked calls.

Definition 11 (Function Tpr ).

                                                  b
                                           Tpr (φ, ψ) ,
              n
        ∀(yk )    , (σk ) , (σk′ )n , n > 0 ⇒ Ppred ((yk )n , (σk )n , (σk′ )n , ψ)
                        n
                                                                                          ⇒
                      c φb((yk )n )(σk )n ⇒ post
                      pre                        d b((yk )n )(σk )n (σk′ )n .
                                                     φ

   We now define function L to lift a relational procedure contract with an
associated tracked call predicate and reduce it to a standard contract.

  b ψ) , λy.(λσ.pre
L(φ,                                     d b((y)1 )(σ)1 (σ ′ )1 ∧ Pcall (y, σ, σ ′ , ψ)).
                c φb((y)1 )(σ)1 , λσσ ′ .postφ


    Finally, using function Tpr and L, we can define function Tf⊲r for generat-
ing the verification condition for verifying that the bodies of each sequence of
                                                       b thanks to L, each call in-
procedures respect the relational contract defined in φ:
struction will result in a corresponding Pcall occurrence in the generated formula,
so that it will be possible to make use of the relational contracts hypotheses in
Tpr when the appropriate sequences of calls occur.

                                                      13
Definition 12 (Function Tf⊲r ).

                                                b ψ) ,
                                          Tf⊲r (φ,
              ∀(yk )n , (σk )n , (σk′ )n , ψ ′ , pre                  b ψ′ ) ⇒
                                                 c φb((yk )n ) ⇒ Tpr (φ,
                           ⊲
                         Tar                                  b ψ ′ )) ∧
                             ((body ψ (yk ))nk=1 , (σk )n , L(φ,
                                                      b ψ ′ ), λp.p ⇒ post
       Tcr⊲ ((bodyψ (yk ))nk=1 , (σk )n , (σk′ )n , L(φ,              d b((yk )n ))).
                                                                          φ

   Using functions Tcr⊲ , Tar ⊲
                                 and Tf⊲r , we can now give the main result of this
paper, i.e. that the verification of relational properties with the VCGen is correct.

Theorem 4 (Soundness of relational VCGen). For any sequence of com-
                                    b procedure environment ψ, and relational
mands (ck )n , contract environment φ,
                         b     b
pre- and postcondition P and Q, if the following three properties hold:
                                                  b ψ),
                                            Tf⊲r (φ,                                            (3)
        ∀(σk )n , ψ ′ , Pb((σk )n ) ∧ Tpr (φ,                                   b ψ ′ )),
                                                b ψ) ⇒ T ⊲ ((ck )n , (σk )n , L(φ,              (4)
                                                             ar
                                                                    b ψ) ⇒
                      ∀(σk )n , (σk′ )n , ψ ′ , Pb ((σk )n ) ∧ Tpr (φ,
                                                b ψ ′ ), λp. p ⇒ Q((σ
            Tcr⊲ ((ck )n , (σk )n , (σk′ )n , L(φ,               b k )n , (σk′ )n )),           (5)

then we have ψ : {Pb }(ck )n {Q}.
                              b
    In other words, a relational property is valid if all relational procedure con-
tracts are valid, and, assuming the relational precondition holds, both the aux-
iliary verification conditions and the main relational verification condition hold.
The corresponding Coq formalization is available in file Rela.v, and the Coq
proof of Theorem 4 is in file Correct Rela.v.
Example 5. Consider ψ = ψsum and φb which encodes R2 and R3 . The relational
property R1 of Fig. 1 can now be proven valid in a modular way, using R2
and R3 , by the proposed technique based on Theorem 4 (see file Examples.v of
the Coq development). For instance, (5) becomes the formula of Fig. 8. There,
the relational precondition is given by (6), while the simplified (instantiated for
                                                                      b ψ) is given
sequence (ysum , ysum )) translation of the relational contracts Tpr (φ,
by (7). Finally, (8) gives the main verification condition:
                                                b ψ ′ ), λp.p ⇒ σ ′ [3] = σ ′ [3]), where L(φ,
Tcr⊲ ((c1ω , c2ω ), (σ1 , σ2 ), (σ1′ , σ2′ ), L(φ,                                           b ψ′ ) =
                                                                 1         2
 {ysum → (λσ. True, λσ, σ . σ[1] > σ[2] ⇒ σ[3] = σ [3] ∧ Pcall (ysum , σ, σ , ψ ′ ))}.
                                      ′                            ′                       ′


Long for a manual proof, such formulas are well-treated by solvers.                               ⊓
                                                                                                  ⊔

7    Related Work
Relational Property Verification. Significant work has been done on relational
program verification (see [27,26] for a detailed state of the art). We discuss below
some of the efforts the most closely related to our work.

                                                14
                                       ∀σ1 , σ2 , σ1′ , σ2′ , ψ.
                                         σ1 (1) = σ2 (1)                                    (6)
                                                  ∧

                                        (∀σ1 , σ2 , σ1′ , σ2′ .
                     Pcall (ysum , σ1 , σ1′ , ψ) ∧ Pcall (ysum , σ2 , σ2′ , ψ)∧
                              σ2 (1) < σ2 (2) ∧ σ1 (2) = σ2 (2)∧
                                                                                            (7)
                       σ1 (1) = σ2 (1) + 1 ∧ σ1 (3) = σ2 (3) + σ2 (1)
                                                 ⇒
                                        σ1′ (3) = σ2′ (3))

                                                 ⇒

                                     ∀σ1′′ , σ1′′′ , σ2′′ , σ2′′′ .
                       σ1′′ = set(σ1 , 1, 1) ∧ σ1′′′ = set(σ1′′ , 3, 0)∧
           ((σ1 (1) > σ1′′′ (2) ⇒ σ1′′′ (3) = σ1′ (3)) ∧ Pcall (ysum , σ1′′′ , σ1′ , ψ))∧
              ′′′


                       σ2′′ = set(σ2 , 1, 0) ∧ σ2′′′ = set(σ2′′ , 3, 0)∧                    (8)
            ((σ2 (1) > σ2′′′ (2) ⇒ σ2′′′ (3) = σ2′ (3)) ∧ Pcall (ysum , σ2′′′ , σ2′ , ψ))
               ′′′


                                                 ⇒
                                         σ1′ (3) = σ2′ (3)

 Figure 8: Assumption (5) of Theorem 4 illustrated for property R1 of Fig. 1.

    Various relational logics have been designed as extensions to Hoare Logic,
such as Relational Hoare Logic [6] and Cartesian Hoare Logic [32]. As our ap-
proach, those logics consider for each command a set of associated memory states
in the very rules of the system, thus avoiding additional separation assumptions.
Limitations of these logics are often the absence of support for aliasing or a
limited form of relational properties. For instance, Relational Hoare Logic sup-
ports only relational properties with two commands and Cartesian Hoare Logic
supports only k-safety properties (relational properties on the same command).
Our method has an advanced support of aliasing and supports a very general
definition of relational properties, possibly between several dissimilar commands.
    Self-compositon [3,30,9] and its derivations [2,31,14] are well-known appro-
aches to deal with relational properties. This is in particular due to their flexibil-
ity: self-composition methods can be applied as a preprocessing step to different
verification approaches. For example, self-composition is used in combination
with symbolic execution and model checking for verification of voting func-
tions [5]. Other examples are the use of self-composition in combination with
verification condition generation in the context of the Java language [13] or the
C language [9,10]. In general, the support of aliasing of C programs in these last
efforts is very limited due the problems mentioned earlier. Compared to these
techniques, where self-composition is applied before the generation of verifica-
tion conditions (and therefore requires taking care about separation of memory

                                                  15
states of the considered programs), our method can be seen as relating the con-
sidered programs’ semantics directly at the level of the verification conditions,
where separation of their memory states is already ensured, thus avoiding the
need to take care of this separation explicitly.
    Finally, another advanced approach for relational verification is the trans-
lation of the relational problem into Horn clauses and their proof using con-
straint solving [22,34]. The benefit of constraint solving lies in the ability to
automatically find relational invariants and complex self-composition deriva-
tions. Moreover, the translation of programs into Horn clauses, done by tools
like Reve9 , results in formulas similar to those generated by our VCGen. There-
fore, like our approach, relational verification with constraint solving requires no
additional separation hypothesis in presence of aliasing.
Certified Verification Condition Generation. In a broad sense, this work contin-
ues previous efforts in formalization and mechanized proof of program language
semantics, analyzers and compilers, such as [29,25,18,7,20,21,35,24,12,28]. Gen-
eration of certificates (in Isabelle) for the Boogie verifier is presented in [28]. The
certified deductive verification tool WhyCert [18] comes with a similar soundness
result for its verification condition generator. Its formalization follows an altern-
ative proof approach, based on co-induction, while our proof relies on induction.
WhyCert is syntactically closer to the C language and the ACSL specification
language [4], while our proof uses a simplified language, but with a richer ali-
asing model. Furthermore, we provide a formalization and a soundness proof for
relational verification, which was not considered in WhyCert or in [28].
    Our previous work [11] presented a method for relational property verification
based on a naive VCGen. To the best of our knowledge, the present work is the
first proposal of modular relational property verification based on an optimized
VCGen for a representative language with procedure calls and aliases with a full
mechanized formalization and proof of soundness in Coq.

8     Conclusion
We have presented in this paper an overview of a method for modular verifica-
tion of relational properties using an optimized verification condition generator,
without relying on code transformations (such as self-composition) or making
additional separation hypotheses in case of aliasing. This method has been fully
formalized in Coq, and the soundness of recursive relational verification using
a verification condition generator (itself formally proved correct) for a simple
language with procedure calls and aliasing has been formally established.
    This work opens the door for interesting future work. Currently, for relational
properties, product programs [2] or other self-composition optimizations [31] are
the standard approach to deal with complex loop constructions. We expect that
user-provided coupling invariants and loop properties can avoid having to rely
on code transformation methods. Showing this in our framework is the next step,
before the investigation of termination and co-termination [17],[34] for extending
the modularity of relational contracts.
9
    https://formal.kastel.kit.edu/projects/improve/reve/


                                          16
References
 1. Apt, K., de Boer, F., Olderog, E.: Verification of Sequential and
    Concurrent Programs. Texts in Computer Science, Springer (2009).
    https://doi.org/10.1007/978-1-84882-745-5
 2. Barthe, G., Crespo, J.M., Kunz, C.: Relational verification using product
    programs. In: Proc. of the 17th International Symposium on Formal
    Methods (FM 2011). LNCS, vol. 6664, pp. 200–214. Springer (2011).
    https://doi.org/10.1007/978-3-642-21437-0 17
 3. Barthe, G., D’Argenio, P.R., Rezk, T.: Secure information flow by self-composition.
    J. of Mathematical Structures in Computer Science 21(6), 1207–1252 (2011).
    https://doi.org/10.1017/S0960129511000193
 4. Baudin, P., Cuoq, P., Filliâtre, J.C., Marché, C., Monate, B., Moy,
    Y., Prevosto, V.: ACSL: ANSI/ISO C Specification Language (2021),
    https://frama-c.com/html/acsl.html
 5. Beckert, B., Bormer, T., Kirsten, M., Neuber, T., Ulbrich, M.: Automated verific-
    ation for functional and relational properties of voting rules. In: Proc. of the 6th
    International Workshop on Computational Social Choice (COMSOC 2016) (2016)
 6. Benton, N.: Simple relational correctness proofs for static analyses and pro-
    gram transformations. In: Proc. of the 31st ACM SIGPLAN-SIGACT Sym-
    posium on of Programming Languages (POPL 2004). pp. 14–25. ACM (2004).
    https://doi.org/10.1145/964001.964003
 7. Beringer, L., Appel, A.W.: Abstraction and subsumption in modular veri-
    fication of C programs. In: Proc. of the Third World Congress on Formal
    Methods - (FM 2019). LNCS, vol. 11800, pp. 573–590. Springer (2019).
    https://doi.org/10.1007/978-3-030-30942-8 34
 8. Bishop, P.G., Bloomfield, R.E., Cyra, L.: Combining testing and proof to gain
    high assurance in software: A case study. In: Proc. of the 24th International Sym-
    posium on Software Reliability Engineering (ISSRE 2013). pp. 248–257. IEEE
    (2013). https://doi.org/10.1109/ISSRE.2013.6698924
 9. Blatter, L., Kosmatov, N., Le Gall, P., Prevosto, V.: RPP: automatic proof
    of relational properties by self-composition. In: Proc. of the 23rd Interna-
    tional Conference on Tools and Algorithms for the Construction and Analysis
    of Systems (TACAS 2017). LNCS, vol. 10205, pp. 391–397. Springer (2017).
    https://doi.org/10.1007/978-3-662-54577-5 22
10. Blatter, L., Kosmatov, N., Le Gall, P., Prevosto, V., Petiot, G.: Static and dynamic
    verification of relational properties on self-composed C code. In: Proc. of the 12th
    International Conference on Tests and Proofs (TAP 2018). LNCS, vol. 10889, pp.
    44–62. Springer (2018). https://doi.org/10.1007/978-3-319-92994-1 3
11. Blatter, L., Kosmatov, N., Prevosto, V., Le Gall, P.: Certified verification of re-
    lational properties. In: Proc. of the 17th International Conference on integrated
    Formal Methods (iFM 2022). LNCS, Springer (Jun 2022), to appear
12. Blazy, S., Maroneze, A., Pichardie, D.: Verified validation of program slicing. In:
    Proc. of the 2015 Conference on Certified Programs and Proofs (CPP 2015). pp.
    109–117. ACM (2015). https://doi.org/10.1145/2676724.2693169
13. Dufay, G., Felty, A.P., Matwin, S.: Privacy-sensitive information flow with JML.
    In: Proc. of the 20th Conference on Automated Deduction (CADE 2005). LNCS,
    vol. 3632, pp. 116–130. Springer (2005). https://doi.org/10.1007/11532231 9
14. Eilers, M., Müller, P., Hitz, S.: Modular product programs. In: Proc. of the 27th
    European Symposium on Programming (ESOP 2018). LNCS, vol. 10801, pp. 502–
    529. Springer (2018). https://doi.org/10.1007/978-3-319-89884-1 18


                                          17
15. Flanagan, C., Saxe, J.B.: Avoiding exponential explosion: generating compact
    verification conditions. In: Proc. of the 28th ACM SIGPLAN Symposium on
    Principles of Programming Languages (POPL 2001). pp. 193–205. ACM (2001).
    https://doi.org/10.1145/360204.360220
16. Floyd, R.W.: Assigning meanings to programs. In: Proc. of Symposia in Ap-
    plied Mathematics. vol. 19 (Mathematical Aspects of Computer Science), p. 19–32
    (1967). https://doi.org/10.1090/psapm/019/0235771
17. Hawblitzel, C., Kawaguchi, M., Lahiri, S.K., Rebêlo, H.: Towards modularly com-
    paring programs using automated theorem provers. In: Proc. of the 24th Interna-
    tional Conference on Automated Deduction (CADE 2013). LNCS, vol. 7898, pp.
    282–299. Springer (2013). https://doi.org/10.1007/978-3-642-38574-2 20
18. Herms, P.: Certification of a Tool Chain for Deductive Program Veri-
    fication. Phd thesis, Université Paris Sud - Paris XI (Jan 2013),
    https://tel.archives-ouvertes.fr/tel-00789543
19. Hoare, C.A.R.: An axiomatic basis for computer programming. Communications
    of the ACM 12(10), 576–580 (1969). https://doi.org/10.1145/363235.363259
20. Jourdan, J., Laporte, V., Blazy, S., Leroy, X., Pichardie, D.: A formally-verified C
    static analyzer. In: Proc. of the 42nd Annual ACM SIGPLAN-SIGACT Symposium
    on Principles of Programming Languages (POPL 2015). pp. 247–259. ACM (2015).
    https://doi.org/10.1145/2676726.2676966
21. Jung, R., Krebbers, R., Jourdan, J., Bizjak, A., Birkedal, L., Dreyer, D.: Iris from
    the ground up: A modular foundation for higher-order concurrent separation logic.
    J. Funct. Program. 28, e20 (2018). https://doi.org/10.1017/S0956796818000151
22. Kiefer, M., Klebanov, V., Ulbrich, M.: Relational program reasoning using compiler
    IR - combining static verification and dynamic analysis. J. of Automated Reasoning
    60(3), 337–363 (2018). https://doi.org/10.1007/s10817-017-9433-5
23. Kip, I.: Assembly Language for x86 Processors. Prentice Hall Press, 7th edn. (2014)
24. Krebbers, R., Leroy, X., Wiedijk, F.: Formal C semantics: CompCert and
    the C standard. In: Proc. of the 5th International Conference on Inter-
    active Theorem Proving (ITP 2014), Held as Part of the Vienna Sum-
    mer of Logic (VSL 2014). LNCS, vol. 8558, pp. 543–548. Springer (2014).
    https://doi.org/10.1007/978-3-319-08970-6 36
25. Leroy, X., Blazy, S.: Formal verification of a C-like memory model and its uses for
    verifying program transformations. Journal of Automated Reasoning 41(1), 1–31
    (2008)
26. Maillard, K., Hritcu, C., Rivas, E., Van Muylder, A.: The next 700 relational
    program logics. In: Proc. of the 47th ACM SIGPLAN Symposium on Prin-
    ciples of Programming Languages (POPL 2020). vol. 4, pp. 4:1–4:33 (2020).
    https://doi.org/10.1145/3371072
27. Naumann, D.A.: Thirty-seven years of relational Hoare logic: Remarks on its prin-
    ciples and history. In: Proc. of the 9th International Symposium on Leveraging
    Applications of Formal Methods (ISoLA 2020). LNCS, vol. 12477, pp. 93–116.
    Springer (2020). https://doi.org/10.1007/978-3-030-61470-6 7
28. Parthasarathy, G., Müller, P., Summers, A.J.: Formally validating a practical veri-
    fication condition generator. In: Proc. of the 33rd International Conference on
    Computer Aided Verification (CAV 2021). LNCS, vol. 12760, pp. 704–727. Springer
    (2021). https://doi.org/10.1007/978-3-030-81688-9 33
29. Pierce, B.C., Azevedo de Amorim, A., Casinghino, C., Gaboardi, M.,
    Greenberg, M., Hriţcu, C., Sjöberg, V., Yorgey, B.: Logical Founda-
    tions. Software Foundations series, volume 1, Electronic textbook (2018),
    http://www.cis.upenn.edu/~ bcpierce/sf


                                          18
30. Scheben, C., Schmitt, P.H.: Efficient self-composition for weakest precon-
    dition calculi. In: Proc. of the 19th International Symposium on Formal
    Methods (FM 2014). LNCS, vol. 8442, pp. 579–594. Springer (2014).
    https://doi.org/10.1007/978-3-319-06410-9 39
31. Shemer, R., Gurfinkel, A., Shoham, S., Vizel, Y.: Property directed self com-
    position. In: Proc. of the 31th International Conference on Computer Aided
    Verification (CAV 2019). LNCS, vol. 11561, pp. 161–179. Springer (2019).
    https://doi.org/10.1007/978-3-030-25540-4 9
32. Sousa, M., Dillig, I.: Cartesian Hoare Logic for Verifying k-safety Prop-
    erties. In: Proc. of the 37th Conference on Programming Language
    Design and Implementation (PLDI 2016). pp. 57–69. ACM (2016).
    https://doi.org/10.1145/2908080.2908092
33. The Coq Development Team: The Coq Proof Assistant (2021),
    https://coq.inria.fr/
34. Unno, H., Terauchi, T., Koskinen, E.: Constraint-based relational verifica-
    tion. In: Proc. of the 33th International Conference on Computer Aided
    Verification (CAV 2021). LNCS, vol. 12759, pp. 742–766. Springer (2021).
    https://doi.org/10.1007/978-3-030-81685-8 35
35. Wils, S., Jacobs, B.: Certifying C program correctness with re-
    spect to compcert with verifast. CoRR abs/2110.11034 (2021),
    https://arxiv.org/abs/2110.11034
36. Winskel, G.: The formal semantics of programming languages - an introduction.
    Foundation of computing series, MIT Press (1993)




                                       19
                                  Appendix
This appendix is provided for convenience of the reviewers, not for publication.


A     Complete Semantics of Language L
A.1    Evaluation of Arithmetic and Boolean Expressions in L
We provide a complete list of rules for evaluation of arithmetic and Boolean
expressions in L in Fig. 9. Evaluation of arithmetic and Boolean expressions
in L is defined by functions ξa and ξb . As mentioned above, the subtraction is
lower-bounded by 0. Operations ∗xi and &xi have a semantics similar to the C
language, i.e. dereferencing and address-of. Semantics of Boolean expressions is
standard [36].



             ξa JnKσ , n                                 ξb JtrueKσ , True
            ξa Jxi Kσ , σ(i)                            ξb Jf alseKσ , False
           ξa J∗xi Kσ , σ(σ(i))                     ξb Ja1 op b a2 Kσ , ξa Ja1 Kσ op a ξa Ja2 Kσ
          ξa J&xi Kσ , i                            ξb Jb1 op l b2 Kσ , ξb Jb1 Kσ op l ξb Jb2 Kσ
    ξa Ja1 op a a2 Kσ , ξa Ja1 Kσ op a ξa Ja2 Kσ            ξb J¬bKσ , ¬ξb JbKσ

        Figure 9: Evaluation of arithmetic and Boolean expressions in L.


A.2    Operational Semantics of Commands in L in L
We provide a complete operational semantics of commands in L in Fig. 10.




                                               20
              ψ
                                     ξa JaKσ = n                     ξa JaKσ = n
 hskip, σi → σ                              ψ                               ψ
                               hxi := a, σi → σ[i/n]          h∗xi := a, σi → σ[σ(i)/n]

                                                                                   ψ
      hassert(P ), σi → σ
                           ψ                       ξb JbKσ = True     hc1 , σ1 i → σ2
                                                                                       ψ
                                                hif b then {c1 } else {c2 }, σ1 i → σ2

         ψ                       ψ                                                 ψ
hc1 , σ1 i → σ2      hc2 , σ2 i → σ3               ξb JbKσ = False    hc2 , σ1 i → σ2
                      ψ                                                                ψ
        hc1 ; c2 , σ1 i → σ3                    hif b then {c1 } else {c2 }, σ1 i → σ2

                                      ψ                                                ψ
 ξb JbKσ1 = True          hc1 , σ1 i → σ2        hwhile b inv P do {c}, σ2 i → σ3
                                                             ψ
                          hwhile b inv P do {c}, σ1 i → σ3

                                                                               ψ
             ξb JbKσ = False                                hbodyψ (y), σ1 i → σ2
                                      ψ                                    ψ
hwhile b inv P do {c}, σi → σ                                hcall(y), σ1 i → σ2

          Figure 10: Operational semantics of commands in L.




                                             21
