                                             Certified Verification of Relational Properties⋆

                                                    Lionel Blatter1 , Nikolai Kosmatov2,3(0000−0003−1557−2813) ,
                                                           Virgile Prevosto2(0000−0002−7203−0968) , and
                                                              Pascale Le Gall4(0000−0002−8955−6835)
arXiv:2202.10349v3 [cs.SE] 17 May 2022




                                                                 1
                                                                   Karlsruhe Institute of Technology
                                                                    firstname.lastname@kit.edu
                                                   2
                                                     Université Paris-Saclay, CEA, List, 91120, Palaiseau, France
                                                                     firstname.lastname@cea.fr
                                                     3
                                                       Thales Research & Technology, 91120, Palaiseau, France
                                               4
                                                 CentraleSupélec, Université Paris-Saclay, 91190 Gif-sur-Yvette France
                                                            firstname.lastname@centralesupelec.fr


                                               Abstract The use of function contracts to specify the behavior of func-
                                               tions often remains limited to the scope of a single function call. Re-
                                               lational properties link several function calls together within a single
                                               specification. They can express more advanced properties of a given func-
                                               tion, such as non-interference, continuity, or monotonicity. They can also
                                               relate calls to different functions, for instance, to show that an optim-
                                               ized implementation is equivalent to its original counterpart. However,
                                               relational properties cannot be expressed and verified directly in the tra-
                                               ditional setting of modular deductive verification. Self-composition has
                                               been proposed to overcome this limitation, but it requires complex trans-
                                               formations and additional separation hypotheses for real-life languages
                                               with pointers. We propose a novel approach that is not based on code
                                               transformation and avoids those drawbacks. It directly applies a veri-
                                               fication condition generator to produce logical formulas that must be
                                               verified to ensure a given relational property. The approach has been
                                               fully formalized and proved sound in the Coq proof assistant.


                                         1    Introduction
                                         Modular deductive verification [18] allows the user to prove that a function
                                         respects its formal specification. More precisely, for a given function f , any indi-
                                         vidual call to f can be proved to respect the contract of f , that is, basically an
                                         implication: if the given precondition is true before the call and the call termin-
                                         ates5 , the given postcondition is true after it. However, some kinds of properties
                                         are not easily reducible to a single function call. Indeed, it is frequently neces-
                                         sary to express a property that involves several functions or relates the results
                                         of several calls to the same function for different arguments. Such properties are
                                         known as relational properties [6].
                                         ⋆
                                           Part of this work was funded by the AESC project supported by the Ministry of
                                           Science, Research and Arts Baden-Württemberg (Ref: 33-7533.-9-10/20/1).
                                         5
                                           Termination can be assumed (partial correctness) or proved separately (full correct-
                                           ness) in a well-known way [15]; for the purpose of this paper we can assume it.
//C program Csw1 :      //Composed C program Csw3 :
x3 = * x1 ;             x3_1 = * x1_1 ;                    x3 := ∗x1 ;
* x1 = * x2 ;           * x1_1 = * x2_1 ;           csw1 , ∗x1 := ∗x2 ;
* x2 = x3 ;             * x2_1 = x3_1 ;                    ∗x2 := x3 ;
//C program Csw2 :
* x1 = * x1 + * x2 ;    * x1_2 = * x1_2 + * x2_2 ;              ∗x1 := ∗x1 + ∗x2 ;
* x2 = * x1 - * x2 ;    * x2_2 = * x1_2 - * x2_2 ;       csw2 , ∗x2 := ∗x1 − ∗x2 ;
* x1 = * x1 - * x2 ;    * x1_2 = * x1_2 - * x2_2 ;              ∗x1 := ∗x1 − ∗x2

Figure 1: Two C programs Csw1 and Csw2 swapping *x1 and *x2, their composition
Csw3 , and their counterparts csw1 and csw2 in language L (defined below).


    Examples of such relational properties include monotonicity (i.e. x ≤ y ⇒
f (x) ≤ f (y)), involving two calls, or transitivity (cmp(x, y) ≥ 0 ∧ cmp(y, z) ≥
0 ⇒ cmp(x, z) ≥ 0), involving three calls. In secure information flow [3], non-
interference is also a relational property. Namely, given a partition of program
variables between high-security variables and low-security variables, a program
is said to be non-interferent if any two executions starting from states in which
the low-security variables have the same initial values will end up in a final
state where the low-security variables have the same values. In other words,
high-security variables cannot interfere with low-security ones.
    Relational properties can also relate calls to different functions. For instance,
in the verification of voting rules [5], relational properties are used for defining
specific properties (such as monotonicity, anonymity or consistency). Notably,
applying the voting rule to a sequence of ballots and a permutation of the same
sequence of ballots must lead to the same result, i.e. the order in which the
ballots are passed to the voting function should not have any impact on the
outcome.
Motivation. Lack of support for relational properties in verification tools was
already faced by industrial users (e.g. in [8] for C programs). The usual way to
deal with this limitation is to use self-composition [3,30,9], product program [2]
or other self-composition optimizations [31]. Those techniques are based on code
transformations that are relatively tedious and error-prone. Moreover, they are
hardly applicable in practice to real-life programs with pointers like in C. Namely,
self-composition requires that the compared executions operate on completely
separated (i.e. disjoint) memory areas, which might be extremely difficult to
ensure for complex programs with pointers.

Example 1 (Motivating Example). Figure 1 shows an example of two simple C
programs performing a swap of the values referred to by pointers x1 and x2 (of
type int*). Program Csw1 uses an auxiliary variable x3 (of type int), while Csw2
performs an in-place swap using arithmetic operations. As usual in that case, to
work correctly, each of these programs needs some separation hypotheses: point-
ers x1 and x2 should be separated (that is, point to disjoint memory locations)
and must not point to x1, x2 themselves and, for Csw1 , to x3.

                                         2
    Consider a relational property, denoted Rsw , stating that both programs,
executed from two states in which each of *x1 and *x2 has the same value, will
end up in two states also having the same values in these locations. To prove this
relational property using self-composition, one typically has to generate a new C
program Csw3 (see Fig. 1) composing Csw1 and Csw2 . To avoid name conflicts, we
rename their variables by adding, resp., suffixes “_1” and “_2”. The relational
property Rsw is then expressed by a contract of Csw3 with a precondition P
and a postcondition Q. Obviously, both P and Q must include the equalities:
*x1_1==*x1_2 and *x2_1==*x2_2, and P must also require the aforementioned sep-
aration hypotheses necessary for each function. But for programs with pointers
and aliasing, this is not sufficient: the user also has to specify additional separa-
tion hypotheses6 between variables coming from the different programs, that is,
in our example, that each of x1_1 and x2_1 is separated from each of x1_2 and
x2_2. Without such hypotheses, a deductive verification tool cannot show, for
example, that a modification of *x1_1 does not impact *x1_2 in the composed
program Csw3 , and is thus unable to deduce the required property. For real-life
programs, such separation hypotheses can be hard to specify or generate. It can
become even more complicated for programs with double or multiple indirec-
tions.                                                                             ⊓
                                                                                   ⊔

Approach. This paper proposes an alternative approach that is not based on
code transformation or relational rules. It directly uses a verification condition
generator (VCGen) to produce logical formulas to be verified (typically, with
an automated prover) to ensure a given relational property. It requires no extra
code processing (such as sequential composition of programs or variable renam-
ing). Moreover, no additional separation hypotheses—in addition to those that
are anyway needed for each function to work—are required. The locations of
each program are separated by construction: each program has its own memory
state. The language L considered in this work was chosen as a minimal language
representative of the main issues relevant for relational property verification: it is
a standard While language enriched with annotations, procedures and pointers
(see programs csw1 and csw2 in Fig. 1 for examples; we use a lower-case letter
c for L programs and a capital letter C for C programs). Notably, the presence
of dereferencing and address-of operations makes it representative of various
aliasing problems with (possibly, multiple) pointer dereferences of a real-life lan-
guage like C. We formalize the proposed approach and prove7 its soundness in
the Coq proof assistant [33]. Our Coq development contains about 3400 lines.
Contributions. The contributions of this paper include:

 – a Coq formalization and proof of soundness of recursive Hoare triple veri-
   fication with a verification condition generator on a representative language
   with procedures and aliasing;
6
    For convenience of the reader, P and Q are defined in detail in Appendix A.
7
    The Coq development is at https://github.com/lyonel2017/Relational-Spec,
    where the version corresponding to this paper is tagged iFM2022.


                                          3
 – a novel method for verifying relational properties using a verification condi-
   tion generator, without relying on code transformation (such as self-composi-
   tion) or making additional separation hypotheses in case of aliasing;
 – a Coq formalization and proof of soundness of the proposed method of
   relational property verification for the considered language.
Outline. Section 2 introduces an imperative language L used in this work. Func-
tional correctness is defined in Section 3, and relational properties in Section 4.
Then, we prove the soundness of a VCGen in Section 5, and show how it can be
soundly extended to verify relational properties in Section 6. Finally, we present
related work in Section 7 and concluding remarks in Section 8.

2     Syntax and Semantics of the L Language
2.1   Notation for Locations, States, and Procedure Contracts
We denote by N = {0, 1, 2, . . . } the set of natural numbers, by N∗ = {1, 2, . . . }
the set of nonzero natural numbers, and by B = {True, False} the set of Boolean
values. Let X be the set of program locations and Y the set of program (procedure)
names, and let x, x′ , x1 , ... and y, y ′ , y1 , ... denote metavariables ranging over
those respective sets. We assume that there exists a bijective function N → X,
so that X = {xi | i ∈ N}. Intuitively, we can see i as the address of location xi .
    Let Σ be the set of functions σ : N → N, called memory states, and let
σ, σ ′ , σ1 , ... denote metavariables ranging over the set. A state σ maps a location
to a value using its address: location xi has value σ(i).
    We define the update operation of a memory state set(σ, i, n), also denoted
by σ[i/n], as the memory state σ ′ mapping each address to the same value as σ,
except for i, bound to n. Formally, set(σ, i, n) is defined by the following rules:
              ∀σ ∈ Σ, xi ∈ X, n ∈ N, xj ∈ X. i = j ⇒ σ[i/n](j) = n,                (1)
            ∀σ ∈ Σ, xi ∈ X, n ∈ N, xj ∈ X. i 6= j ⇒ σ[i/n](j) = σ(j).              (2)
    Let Ψ be the set of functions ψ : Y → C, called procedure environments,
mapping program names to commands (defined below), and let ψ, ψ1 , ... denote
metavariables ranging over Ψ . We write bodyψ (y) to refer to ψ(y), the commands
(or body) of procedure y for a given procedure environment ψ.
    Assertions are predicates of arity one, taking as parameter a memory state
and returning an equational first-order logic formula. Let metavariables P, Q, ...
range over the set A of assertions. For instance, using λ-notation, assertion P
assessing that location x3 is bound to 2 can be defined by P , λσ.σ(3) = 2.
This form will be more convenient for relational properties (than e.g. x3 = 2) as
it makes explicit the memory states on which a property is evaluated.
    Finally, we define the set Φ of contract environments φ : Y → A × A, and
metavariables φ, φ1 , ... to range over Φ. More precisely, φ maps a procedure name
y to the associated (procedure) contract φ(y) = (preφ (y), postφ (y)), composed
of a pre- and a postcondition for procedure y. As usual, a procedure contract
will allow us to specify the behavior of a single procedure call, that is, if we start
executing y in a memory state satisfying preφ (y), and the evaluation terminates,
the final state satisfies postφ (y).

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


2.2    Syntax for Expressions and Commands
Let Ea , Eb and C denote respectively the sets of arithmetic expressions, Boolean
expressions and commands. We denote by a, a1 , ...; b, b1 , ... and c, c1 , ... metav-
ariables ranging, respectively, over those sets. Syntax of arithmetic and Boolean
expressions is given in Fig. 2. Constants are natural numbers or Boolean values.
Expressions use standard arithmetic, comparison and logic binary operators, de-
noted respectively op a ::= {+, ×, −}, op b ::= {<=, =}, op l ::= {∨, ∧}. Since
we use natural values, the subtraction is bounded by 0, as in Coq: if n′ > n, the
result of n − n′ is considered to be 0. Expressions also include locations, possibly
with a dereference or address operators.
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
as in assembly code [22], parameters and return value(s) are shared implicitly
between the caller and the callee through memory locations: the caller must
put/read the right values at the right locations before/after the call. Finally, to
avoid ambiguity, we delimit sequences of commands with { }.

Example 2. Figure 3 shows an example of a command crec and a procedure
environment ψ where procedure y1 points to a recursive command, called in crec .

                                            5
                                                                             
                                            
                                                  if x1 > 0 then {           
                                                                              
                                            
                                            
                                            
                                                       x2 := x2 + x3 ;       
                                                                              
                                                                              
                                                                              
           x1 := x4 ;                                   x1 := x1 − 1;
                                            
                                                                             
                                                                              
                                                                             
    crec , x2 := 0;                ψ=      y1 →         call(y1 )       , ...
           call(y1 )                               } else {
                                        
                                                                             
                                                                              
                                        
                                                                             
                                                                              
                                                        skip
                                        
                                                                             
                                                                              
                                        
                                                                             
                                                                              
                                                   }
                                                                             
                                                                             
               λσ.σ(2) = σ(3) × (σ(4) − σ(1)) ∧ 0 ≤ σ(1) ∧ σ(1) ≤ σ(4),
 φ = y1 →                                                                  , ... .
                               λσ.σ(2) = σ(3) × σ(4)

          Figure 3: Example of an L program crec with its environments.


     ξa JnKσ , n        ξa Jxi Kσ , σ(i)    ξa J∗xi Kσ , σ(σ(i))     ξa J&xi Kσ , i
              Figure 4: Evaluation of expressions in L (selected rules).


With the semantics of Sec. 2.3, from any initial state, the command will return
a state in which x2 = x3 × x4 . Procedure y1 returns a state where x2 = x3 × x4
if the initial state satisfies x2 = x3 × (x4 − x1 ) ∧ 0 ≤ x1 ∧ x1 ≤ x4 . This can be
expressed by the contract environment φ given (in λ-notation) in Fig. 3.           ⊓
                                                                                   ⊔

2.3 Operational Semantics
Evaluation of arithmetic and Boolean expressions in L is defined by functions ξa
and ξb . Selected evaluation rules for arithmetic expressions are shown in Fig. 4.
Operations ∗xi and &xi have a semantics similar to the C language, i.e. derefer-
encing and address-of. Semantics of Boolean expressions is standard [36].
    Based on these evaluation functions, we can define the operational semantics
of commands in a given procedure environment ψ. Selected evaluation rules8 are
shown in Fig. 5. As said above, both assertions and loop invariants can be seen
as program annotations that do not influence the execution of the program itself.
Hence, command assert(P ) is equivalent to a skip. Likewise, loop invariant P
has no influence on the semantics of while b inv P do {c}.
                           ψ                               ψ
   We write      hc, σi → σ ′ to denote that hc, σi → σ ′ can be derived from
the rules of Fig. 5. Our Coq formalization, inspired by [29], provides a deep
embedding of L, with an associated parser, in files Aexp.v, Bexp.v and Com.v.

3     Functional Correctness
We define functional correctness in a similar way to the original Hoare triple
definition [18], except that we also need a procedure environment ψ, leading to a
quadruple denoted ψ : {P }c{Q}. We will however still refer by the term “Hoare
triple” to the corresponding program property, formally defined as follows.
8
    For convenience of the reader, full versions of Fig. 4, 5 are given in Appendix B.


                                            6
                                     ψ
                                                    ξa JaKσ = n
                  hassert(P ), σi → σ                       ψ
                                                hxi := a, σi → σ[i/n]

                                                                        ψ
                       ξa JaKσ = n                hbodyψ (y), σ1 i → σ2
                             ψ                                      ψ
                h∗xi := a, σi → σ[σ(i)/n]           hcall(y), σ1 i → σ2
      Figure 5: Operational semantics of commands in L (selected rules).


Definition 1 (Hoare triple). Let c be a command, ψ a procedure environment,
and P and Q two assertions. We define a Hoare triple ψ : {P }c{Q} as follows:
                                                                ψ
          ψ : {P }c{Q} , ∀σ, σ ′ ∈ Σ. P (σ) ∧ (         hc, σi → σ ′ ) ⇒ Q(σ ′ ).

   Informally, our definition states that, for a given ψ, if a state σ satisfies P
and the execution of c on σ terminates in a state σ ′ , then σ ′ satisfies Q.
   Next, we introduce notation CV (ψ, φ) to denote the fact that, for the given
φ and ψ, every procedure satisfies its contract.

Definition 2 (Contract Validity). Let ψ be a procedure environment and φ
a contract environment. We define contract validity CV (ψ, φ) as follows:

             CV (ψ, φ) , ∀y ∈ Y. ψ : {preφ (y)}call(y){postφ (y)}).

    The notion of contract validity is at the heart of modular verification, since it
allows assuming that the contracts of the callees are satisfied during the verifica-
tion of a Hoare triple. More precisely, to state the validity of procedure contracts
without assuming anything about their bodies in our formalization, we will con-
sider an arbitrary choice of implementations ψ ′ of procedures that satisfy the
contracts, like in assumption (3) in Lemma 1. This technical lemma, taken from
[1, Equation (4.6)], gives an alternative criterion for validity of procedure con-
tracts: if, under the assumption that the contracts in φ hold, we can prove for
each procedure y that its body satisfies its contract, then the contracts are valid.
Lemma 1 (Adequacy of contracts). Given a procedure environment ψ and
a contract environment φ such that

       ∀ψ ′ ∈ Ψ. CV (ψ ′ , φ) ⇒ ∀y ∈ Y, ψ ′ : {preφ (y)}bodyψ (y){postφ (y)},       (3)

we have CV (ψ, φ).

Proof. Any given terminating execution traverses a finite number of procedure
calls (over all procedures) that can be replaced by inlining the bodies a sufficient
number of times. We first formalize a theory of k-inliners (that inline procedure
bodies a finite number of times k ≥ 0 and replace deeper calls by nonterminating
loops) and prove their properties. Relying on this elegant theory, the proof of
the lemma proceeds by induction on the number of procedure inlinings.             ⊓
                                                                                  ⊔

                                            7
   From that, we can establish the main result of this section. Theorem 1, taken
from [1, Th. 4.2] states that ψ : {P }c{Q} holds if assumption (3) holds and if
the validity of contracts of φ for ψ implies the Hoare triple itself. This theorem is
the basis for modular verification of Hoare Triples, as done for instance in Hoare
Logic [18,36] or verification condition generation.

Theorem 1 (Recursion). Given a procedure environment ψ and a contract
environment φ such that

     ∀ψ ′ ∈ Ψ. CV (ψ ′ , φ) ⇒ ∀y ∈ Y, ψ ′ : {preφ (y)}bodyψ (y){postφ (y)}, and
                             CV (ψ, φ) ⇒ ψ : {P }c{Q},

we have ψ : {P }c{Q}.

Proof. By Lemma 1.                                                                     ⊓
                                                                                       ⊔

    We refer the reader to the Coq development, more precisely the results
recursive_proc and recursive_hoare_triple in file Hoare_Triple.v for com-
plete proofs of Lemma 1 and Theorem 1 for L. To the best of our knowledge,
this is the first mechanized proof of these classical results.
    An interesting corollary can be deduced from Theorem 1.
Corollary 1 (Procedure Recursion) Given a procedure environment ψ and
a contract environment φ such that

       ∀ψ ′ ∈ Ψ. CV (ψ ′ , φ) ⇒ ∀y ∈ Y, ψ ′ : {preφ (y)}bodyψ (y){postφ (y)},

we have ∀y ∈ Y. ψ : {preφ (y)}bodyψ (y){postφ (y)}.


4    Relational Properties
Relational properties can be seen as an extension of Hoare triples. But, instead
of linking one program with two properties, the pre- and postconditions, rela-
tional properties link n programs to two properties, called relational assertions.
We define a relational assertion as a predicate taking a sequence of memory
states and returning a first-order logic formula. We use metavariables Pb , Q, b ... to
                                                         b
range over the set of relational assertions, denoted A. As a simple example of a
relational assertion, we might say that two states bind location x3 to the same
value. This would be stated as follows: λ(σ1 , σ2 ).σ1 (3) = σ2 (3).
    A relational property is a property about n programs c1 , ..., cn , stating that if
each program ci starts in a state σi and ends in a state σi′ such that Pb (σ1 , ..., σn )
holds, then Q(σb ′ , ..., σ ′ ) holds, where Pb and Q
                                                    b are relational assertions over n
                  1        n
memory states.
    We formally define relational correctness similarly to functional correctness
(cf. Def. 1), except that we now use sequences of memory states and commands of
equal length. We denote by (uk )n a sequence of elements (uk )nk=1 = (u1 , . . . , un ),
where k ranges from 1 to n. If n ≤ 0, (uk )n is the empty sequence denoted [ ].

                                           8
                              ψ : {Pb} csw1 ∼ csw2 {Q},
                                                    b

         Pb , λσ1 σ2 . σ1 (σ1 (1)) = σ2 (σ2 (1)) ∧ σ1 (σ1 (2)) = σ2 (σ2 (2))∧
σ1 (1) 6= σ1 (2) ∧ σ2 (1) 6= σ2 (2) ∧ σ1 (1) > 3 ∧ σ1 (2) > 3 ∧ σ2 (1) > 2 ∧ σ2 (2) > 2,

          b , λσ1′ σ2′ . σ1′ (σ1′ (1)) = σ2′ (σ2′ (1)) ∧ σ1′ (σ1′ (2)) = σ2′ (σ2′ (2)).
          Q
    Figure 6: A relational property for L programs csw1 and csw2 of Fig. 1.

Definition 3 (Relational Correctness). Let ψ be a procedure environment,
(ck )n a sequence of n commands (n ∈ N∗ ), and Pb and Q  b two relational assertions
over n states. The relational correctness of (ck ) with respect to Pb and Q,
                                                  n                       b denoted
      b      n b
ψ : {P }(ck ) {Q}, is defined as follows:

                                     ψ : {Pb}(ck )n {Q}
                                                     b ,
                                               n
                                               ^              ψ
         ∀(σk )n , (σ ′ k )n . Pb((σk )n ) ∧ (                            b ′ k )n ).
                                                   hci , σi i → σ ′ i ) ⇒ Q((σ
                                             i=1

    This notation generalizes the one proposed by Benton [6] for relational prop-
erties linking two commands: ψ : {Pb }c1 ∼ c2 {Q}. b As Benton’s work mostly
focused on comparing equivalent programs, using symbol ∼ was quite natural.
In particular, Benton’s work would not be practical for verification of relational
properties with several calls such as transitivity mentioned in Sec. 1.
Example 3 (Relational property). Figure 6 formalizes the relational property
Rsw for L programs csw1 and csw2 discussed in Ex. 1. Recall that Rsw (writ-
ten in Fig. 6 in Benton’s notation) states that both programs executed from two
states named σ1 and σ2 having the same values in ∗x1 and ∗x2 will end up in
two states σ1′ and σ2′ also having the same values in these locations. Notice that
the initial state of each program needs separation hypotheses (cf. the second line
of the definition of Pb ). Namely, x1 and x2 must point to different locations and
must not point to x1 , x2 or, for csw1 , to x3 for the property to hold. This rela-
tional property is formalized in the Coq development in file Examples.v.         ⊓
                                                                                 ⊔


5   Verification Condition Generation for Hoare Triples
A standard way [15] for verifying that a Hoare triple holds is to use a verification
condition generator (VCGen). In this section, we formalize a VCGen for Hoare
triples and show that it is correct, in the sense that if all verification conditions
that it generates are valid, then the Hoare triple is valid according to Def. 1.

5.1 Verification Condition Generator
We have chosen to split the VCGen in three steps, as it is commonly done [23]:

 – function Tc generates the main verification condition, expressing that the
   postcondition holds in the final state, assuming auxiliary annotations hold;

                                                9
                        Tc JskipK(σ, φ, f ) , ∀σ ′ . σ ′ = σ ⇒ f (σ ′ )
                      Tc Jxi := aK(σ, φ, f ) , ∀σ ′ . σ ′ = set(σ, i, ξa JaKσ) ⇒ f (σ ′ )
                    Tc J∗xi := aK(σ, φ, f ) , ∀σ ′ . σ ′ = set(σ, σ(i), ξa JaKσ) ⇒ f (σ ′ )
                  Tc Jassert(P )K(σ, φ, f ) , ∀σ ′ . σ ′ = σ ∧ P (σ) ⇒ f (σ ′ )
                        Tc Jc0 ; c1 K(σ, φ, f ) , Tc Jc0 K(σ, φ, λσ ′ . Tc Jc1 K(σ ′ , φ, f ))
  Tc Jif b then {c0 } else {c1 }K(σ, φ, f ) , (ξb JbKσ ⇒ Tc Jc0 K(σ, φ, f ))∧
                                                     (¬ξb JbKσ ⇒ Tc Jc1 K(σ, φ, f ))
                      Tc Jcall(y)K(σ, φ, f ) , preφ (y)(σ) ⇒ (∀σ ′ . postφ (y)(σ ′ ) ⇒ f (σ ′ ))
  Tc Jwhile b inv inv do {c}K(σ, φ, f ) , inv(σ) ⇒
                                                     (∀σ ′ . inv(σ ′ ) ∧ ¬(ξb JbKσ ′ ) ⇒ f (σ ′ ))

 Figure 7: Definition of function Tc generating the main verification condition.


 – function Ta generates auxiliary verification conditions stemming from asser-
   tions, loop invariants, and preconditions of called procedures;
 – finally, function Tf generates verification conditions for the auxiliary proced-
   ures that are called by the main program, to ensure that their bodies respect
   their contracts.


Definition 4 (Function Tc generating the main verification condition).
Given a command c, a memory state σ representing the state before the com-
mand, a contract environment φ, and an assertion f , function Tc returns a
formula defined by case analysis on c as shown in Fig. 7.

    Assertion f represents the postcondition we want to verify after the command
executed from state σ. For each command, except sequence and branch, a fresh
memory state σ ′ is introduced and related to the current memory state σ. The
new memory state is given as parameter to f . For skip, which does nothing, both
states are identical. For assignments, σ ′ is simply the update of σ. An assertion
introduces a hypothesis over σ but leaves it unchanged. For a sequence, we
simply compose the conditions, that is, we check that the final state of c0 is such
that f will be verified after executing c1 . For a conditional, we check that if the
condition evaluates to true, the then branch will ensure the postcondition, and
that otherwise the else branch will ensure the postcondition. The rule for calls
simply assumes that σ ′ verifies postφ (y). Finally, Tc assumes that, after a loop, σ ′
is a state where the loop condition is false and the loop invariant holds. As for an
assertion, the callee’s precondition and the loop invariant are just assumed to be
true; function Ta , defined below, generates the corresponding proof obligations.

Example 4. For c , skip; x1 := 2, and f , λσ. σ(1) = 2, we have:

   Tc JcK(σ, φ, f ) ≡ ∀σ1′ .σ = σ1′ ⇒ (∀σ2′ .σ2′ = set(σ1′ , 1, 2) ⇒ σ2′ (1) = 2).                   ⊓
                                                                                                     ⊔


                                                  10
                         Ta JskipK(σ, φ) , T rue
                       Ta Jxi := aK(σ, φ) , T rue
                      Ta J∗xi := aK(σ, φ) , T rue
                   Ta Jassert(P )K(σ, φ) , P (σ)
                         Ta Jc0 ; c1 K(σ, φ) , Ta Jc0 K(σ, φ)∧
                                          Tc Jc0 K(σ, φ, λσ ′ .(Ta Jc1 K(σ ′ , φ)))
    Ta Jif b then {c0 } else {c1 }K(σ, φ) , ξb JbKσ ⇒ Ta Jc0 K(σ, φ)∧
                                          ¬(ξb JbKσ) ⇒ Ta Jc1 K(σ, φ)
                       Ta Jcall(y)K(σ, φ) , preφ (y)(σ)
    Ta Jwhile b inv inv do {c}K(σ, φ) , inv(σ)∧
                                          (∀σ ′ , inv(σ ′ ) ∧ ξb JbKσ ′ ⇒ Ta JcK(σ ′ , φ))∧
                                          (∀σ ′ , inv(σ ′ ) ∧ ξb JbKσ ′ ⇒ Tc JcK(σ ′ , φ, inv))

Figure 8: Definition of function Ta generating auxiliary verification conditions.


Definition 5 (Function Ta generating the auxiliary verification condi-
tions). Given a command c, a memory state σ representing the state before the
command, and a contract environment φ, function Ta returns a formula defined
by case analysis on c as shown in Fig. 8.
    Basically, Ta collects all assertions, preconditions of called procedures, as well
as invariant establishment and preservation, and lifts the corresponding formulas
to constraints on the initial state σ through the use of Tc .
    Finally, we define the function for generating the conditions for verifying that
the body of each procedure defined in ψ respects its contract defined in φ.
Definition 6 (Function Tf generating the procedure verification con-
dition). Given two environments ψ and φ, Tf returns the following formula:
          Tf (φ, ψ) , ∀y, σ. preφ (y)(σ) ⇒ Ta Jbodyψ (y)K(σ, φ) ∧
                                                  Tc Jbodyψ (y)K(σ, φ, postφ (y)).
   The VCGen is defined in file Vcg.v of the Coq development. Interested
readers will also find a proof (in file Vcg Opt.v) of a VCGen optimization (not
detailed here), which prevents the size of the generated formulas from becoming
exponential in the number of conditions in the program [14], which is a classical
problem for “naive” VCGens.
5.2 Hoare Triple Verification
We can now state the theorems establishing correctness of the VCGen. Their
proof can be found in file Correct.v of the Coq development.
   First, Lemma 2 shows that, under the assumption of the procedure contracts,
a Hoare triple is valid if for all memory states satisfying the precondition, the
main verification condition and the auxiliary verification conditions hold.

                                             11
Lemma 2. Assume the following two properties hold:

                          ∀σ ∈ Σ, P (σ) ⇒ Ta JcK(σ, φ),
                         ∀σ ∈ Σ, P (σ) ⇒ Tc JcK(σ, φ, Q).

Then we have CV (ψ, φ) ⇒ ψ : {P }c{Q}.

Proof. By structural induction over c.                                            ⊓
                                                                                  ⊔

   Next, we prove in Lemma 3 that if Tf (φ, ψ) holds, then for an arbitrary
choice of implementations ψ ′ of procedures respecting the procedure contracts,
the body of each procedure y respects its contract.

Lemma 3. Assume that the formula Tf (φ, ψ) is satisfied. Then we have

       ∀ψ ′ ∈ Ψ. CV (ψ ′ , φ) ⇒ ∀y ∈ Y, ψ ′ : {preφ (y)}bodyψ (y){postφ (y)}.

Proof. By Lemma 2.                                                                ⊓
                                                                                  ⊔

  Finally, we can establish the main theorem of this section, stating that the
VCGen is correct with respect to our definition of Hoare triples.

Theorem 2 (Soundness of VCGen). Assume that we have Tf (φ, ψ) and

                           ∀σ ∈ Σ, P (σ) ⇒ Ta JcK(σ, φ),
                         ∀σ ∈ Σ, P (σ) ⇒ Tc JcK(σ, φ, Q).

Then we have ψ : {P }c{Q}.

Proof. By Theorem 1 and Lemmas 2 and 3.                                           ⊓
                                                                                  ⊔

Example 5. Consider again the command crec , procedure environment ψ, and
contract environment φ of Ex. 2 (presented in Fig. 3). We can apply Theorem 2
to prove its functional correctness expressed by the following Hoare triple:

                  ψ : {λσ.T rue} crec {λσ.σ(2) = σ(4) × σ(3)}

(see command com_rec in file Examples.v).                                         ⊓
                                                                                  ⊔


6   Verification of Relational Properties
In this section, we propose a verification method for relational properties (defined
in Section 4) using the VCGen defined in Section 5 (or, more generally, any
VCGen respecting Theorem 2). First, we define the notation Tcr for the recursive
call of function Tc on a sequence of commands and memory states:

Definition 7 (Function Tcr ). Given a sequence of commands (ck )n and a se-
                                                                          b over
quence of memory states (σk )n , a contract environment φ and a predicate Q
n states, function Tcr is defined by induction on n as follows.

                                         12
 – Basis: n = 0.
                                                       b , Q([
                                     Tcr ([ ], [ ], φ, Q)  b ]).

 – Inductive: n ∈ N∗ .

                                                                b ,
                                      Tcr ((ck )n , (σk )n , φ, Q)
                                                                              b ′ k )n ))).
           Tc Jcn K(σn , φ, λσn′ .Tcr ((ck )n−1 , (σk )n−1 , φ, λ(σ ′ k )n−1 .Q((σ

    Intuitively, for n = 2, Tcr gives the weakest relational condition that σ1 and
σ2 must fulfill in order for Q     b to hold after executing c1 from σ1 and c2 from σ2 :
                                b ≡ Tc Jc2 K(σ2 , φ, λσ ′ .Tc Jc1 K(σ1 , φ, λσ ′ .Q(σ
Tcr ((c1 , c2 ), (σ1 , σ2 ), φ, Q)                                                b ′ , σ ′ ))).
                                                       2                      1      1   2



Remark 1. Assume we have n > 0, a command cn , a sequence of commands
(ck )n−1 , and a sequence of memory states (σk )n−1 . From Def. 1, it follows that

                                                                  ψ
                        ∀σn , σn′ . Pb((σk )n ) ∧ ( hcn , σn i → σn′ ) ⇒
                                                                  b ′ k )n ))
                      Tcr ((ck )n−1 , (σk )n−1 , φ, λ(σ ′ k )n−1 .Q((σ

is equivalent to

   ψ : {λσn .Pb((σk )n )}cn {λσn′ .Tcr ((ck )n−1 , (σk )n−1 , φ, λ(σ ′ k )n−1 .Q((σ
                                                                               b ′ k )n ))}.


Example 6 (Relational verification condition). In order to make things more con-
crete, we can go back to the relational property Rsw between two implement-
ations csw1 and csw2 of swap defined in Ex. 1 and examine what would be the
main verification condition generated by Tcr . Let Pb and Q
                                                          b be defined as in Ex. 3.
In this particular case, we have n = 2, and φ is empty (since we do not have any
function call), thus Def. 7 becomes:

                                    b = Tc Jcsw2 K(σ2 , ∅, λσ ′ .Tc Jcsw1 K(σ1 , ∅, λσ ′ .Q(σ
Tcr ((csw1 , csw2 ), (σ1 , σ2 ), ∅, Q)                                                    b ′ , σ ′ ))).
                                                             2                        1      1   2


We thus start by applying Tc over csw1 , to obtain, using the rules of Def. 4 for
sequence and assignment, the following intermediate formula:

                                                            b =
                        Tcr ((csw1 , csw2 ), (σ1 , σ2 ), ∅, Q)
                           Tc (csw2 , σ2 , ∅,
                              λσ2′ .∀σ3 , σ5 , σ7 .
                                 σ3 = σ1 [3/σ1 (σ1 (1))] ⇒
                                 σ5 = σ3 [σ3 (1)/σ3 (σ3 (2))] ⇒
                                                             b 7 , σ ′ ).
                                 σ7 = σ5 [σ5 (2)/σ5 (3)] ⇒ Q(σ            2



                                                  13
We can then do the same with csw2 to obtain the final formula:
                                                     b =
                 Tcr ((csw1 , csw2 ), (σ1 , σ2 ), ∅, Q)
                         ∀(σk )8 .
                            σ4 = σ2 [σ2 (1)/σ2 (σ2 (1)) + σ2 (σ2 (2))] ⇒
                            σ6 = σ4 [σ4 (2)/σ4 (σ4 (1)) − σ4 (σ4 (2))] ⇒
                            σ8 = σ6 [σ6 (1)/σ6 (σ6 (1)) − σ6 (σ6 (2))] ⇒
                            σ3 = σ1 [3/σ1 (σ1 (1))] ⇒
                            σ5 = σ3 [σ3 (1)/σ3 (σ3 (2))] ⇒
                                                        b 7 , σ8 ).
                            σ7 = σ5 [σ5 (2)/σ5 (3)] ⇒ Q(σ

Here, σk with odd (resp., even) indices result from Tc for csw1 (resp., csw2 ).           ⊓
                                                                                          ⊔

   We similarly define a notation for the auxiliary verification conditions for a
sequence of n commands.
Definition 8 (Function Tar ). Given a sequence of commands (ck )n and a se-
quence of memory states (σk )n , we define function Tar as follows:
                                                     n
                                                     ^
                       Tar ((ck )n , (σk )n , φ) ,         Ta Jci K(σi , φ).
                                                     i=1

Remark 2. For n > 0, it trivially follows from Def. 8 that:

         Tar ((ck )n , (σk )n , φ) ≡ Ta Jcn K(σn , φ) ∧ Tar ((ck )n−1 , (σk )n−1 , φ).

    Using functions Tcr and Tar , we can now give the main result of this paper: it
states that the verification of relational properties using the VCGen is correct.
Theorem 3 (Soundness of relational VCGen). For any sequence of com-
mands (ck )n , contract environment φ, procedure environment ψ, and relational
assertions over n states Pb and Q,
                                b if the following three properties hold:

                                          Tf (φ, ψ),                                     (4)

                      ∀(σk )n , Pb((σk )n ) ⇒ Tar ((ck )n , (σk )n , φ),                 (5)

                     ∀(σk )n , Pb((σk )n ) ⇒ Tcr ((ck )n , (σk )n , φ, Q),
                                                                       b                 (6)
then we have ψ : {Pb }(ck )n {Q}.
                              b

    In other words, a relational property is valid if all procedure contracts are
valid, and, assuming the relational precondition holds, both the auxiliary verific-
ation conditions and the main relational verification condition hold. We give the
main steps of the proof below. The corresponding Coq formalization is available
in file Rela.v, and the Coq proof of Theorem 3 is in file Correct Rela.v.

                                              14
Proof. By induction on the length n of the sequence of commands (ck )n .
 – Induction basis: n = 0. By Def. 3, our goal becomes:

                             ψ : {Pb }(ck )0 {Q}
                                              b ≡ Pb([ ]) ⇒ Q([
                                                            b ]).

   Indeed, by definition of Tcr and Hypothesis (6), Pb ([ ]) ⇒ Q([
                                                                 b ]) holds.
 – Induction step: assuming the result for n, we prove it for n + 1. So, assume
   we have a sequence of commands (ck )n+1 , relational assertions and environ-
   ments respecting (4), (5), (6) (stated for sequences of n + 1 elements). We
   have to prove ψ : {P̂ }(ck )n+1 {Q̂}, which, by Def. 3, is equivalent to:
                                                  n+1
                                                  ^                ψ
     ∀(σk )n+1 , (σ ′ k )n+1 . Pb((σk )n+1 )∧(                                  b ′ k )n+1 ). (7)
                                                         hci , σi i → σ ′ i ) ⇒ Q((σ
                                                  i=1

   First, we can deduce from Hypothesis (5) and Remark 2:

                        ∀(σk )n+1 , Pb((σk )n+1 ) ⇒ Ta Jcn+1 K(σn+1 , φ),                         (8)

                       ∀(σk )n+1 , Pb ((σk )n+1 ) ⇒ Tar ((ck )n , (σk )n , φ).                    (9)
   By Hypothesis (6) and Def. 7, we have

                                    ∀(σk )n+1 , Pb((σk )n+1 ) ⇒
                               ′
        Tc Jcn+1 K(σn+1 , φ, λσn+1                                        b k )n+1 ))). (10)
                                   .Tcr ((ck )n , (σk )n , φ, λ(σ ′ k )n .Q((σ

   Using (4), (8) and (10), we can now apply Theorem 2 (for an arbitrary
   subsequence (σk )n , that we can thus put in an external universal quantifier)
   to obtain:

                                      ∀(σk )n .
   ψ : {λσn+1 . Pb ((σk )n+1 )}cn+1 {λσn+1
                                       ′                                           b ′ k )n+1 ))}. (11)
                                           . Tcr ((ck )n , (σk )n , φ, λ(σ ′ k )n .Q((σ

   Using Remark 1 and by rearranging the quantifiers and implications, we can
   rewrite (11) into:

               ′                           ′ψ
      ∀σn+1 , σn+1 . hcn+1 , σn+1 i → σn+1        ⇒
         ∀(σk )n .Pb ((σk )n+1 ) ⇒ Tcr ((ck )n , (σk )n , φ, λ(σ ′ k )n .Q((σ
                                                                         b ′ k )n+1 )). (12)

                                                                                    ψ
                                   ′
   For arbitrary states σn+1 and σn+1  such that hcn+1 , σn+1 i → σn+1
                                                                    ′
                                                                       , using
   (4), (9) and (12), we can apply the induction hypothesis, and obtain:
               ′                            ψ ′
      ∀σn+1 , σn+1 .       hcn+1 , σn+1 i → σn+1   ⇒
                                          n b                                b ′ k )n+1 )}.
                              ψ : {λ(σk ) .P ((σk )n+1 )}(ck )n {λ(σ ′ k )n .Q((σ

   Finally, by Def. 3 and by rearranging the quantifiers, we deduce (7).                            ⊓
                                                                                                    ⊔

                                                  15
Example 7. The relational property of Ex. 3 is proven valid using the proposed
technique based on Theorem 3 in file Examples.v of the Coq development. For
instance, (6) becomes ∀σ1 , σ2 . Pb(σ1 , σ2 ) ⇒ Tcr ((csw1 , csw2 ), (σ1 , σ2 ), ∅, Q),
                                                                                    b where
the last expression was computed in Ex. 6. Such formulas—long for a manual
proof—are well-treated by automatic solvers.
    Notice that in this example we do not need any code transformations or extra
separation hypotheses in addition to those anyway needed for the swap functions
while both programs manipulate the same locations x1 , x2 , and—even worse—
the unknown locations pointed by them can be any locations xi , i > 3.                   ⊓
                                                                                         ⊔


7    Related Work
Relational Property Verification. Significant work has been done on relational
program verification (see [27,26] for a detailed state of the art). We discuss below
some of the efforts the most closely related to our work.
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
    Self-compositon [3,30,9] and its derivations [2,31,13] are well-known appro-
aches to deal with relational properties. This is in particular due to their flexibil-
ity: self-composition methods can be applied as a preprocessing step to different
verification approaches. For example, self-composition is used in combination
with symbolic execution and model checking for verification of voting func-
tions [5]. Other examples are the use of self-composition in combination with
verification condition generation in the context of the Java language [12] or the
C language [9,10]. In general, the support of aliasing of C programs in these last
efforts is very limited due the problems mentioned earlier. Compared to these
techniques, where self-composition is applied before the generation of verifica-
tion conditions (and therefore requires taking care about separation of memory
states of the considered programs), our method can be seen as relating the con-
sidered programs’ semantics directly at the level of the verification conditions,
where separation of their memory states is already ensured, thus avoiding the
need to take care of this separation explicitly.
    Finally, another advanced approach for relational verification is the trans-
lation of the relational problem into Horn clauses and their proof using con-
straint solving [21,34]. The benefit of constraint solving lies in the ability to
automatically find relational invariants and complex self-composition deriva-
tions. Moreover, the translation of programs into Horn clauses, done by tools

                                            16
like Reve9 , results in formulas similar to those generated by our VCGen. There-
fore, like our approach, relational verification with constraint solving requires no
additional separation hypothesis in presence of aliasing.
Certified Verification Condition Generation. In a broad sense, this work contin-
ues previous efforts in formalization and mechanized proof of program language
semantics, analyzers and compilers, such as [29,25,17,7,19,20,35,24,11,28]. Gen-
eration of certificates (in Isabelle) for the Boogie verifier is presented in [28]. The
certified deductive verification tool WhyCert [17] comes with a similar soundness
result for its verification condition generator. Its formalization follows an altern-
ative proof approach, based on co-induction, while our proof relies on induction.
WhyCert is syntactically closer to the C language and the ACSL specification
language [4], while our proof uses a simplified language, but with a richer ali-
asing model. Furthermore, we provide a formalization and a soundness proof for
relational verification, which was not considered in WhyCert or in [28].
    To the best of our knowledge, the present work is the first proposal of rela-
tional property verification based on verification condition generation realized for
a representative language with procedure calls and aliases with a full mechanized
formalization and proof of soundness in Coq.

8     Conclusion
We have presented in this paper a method for verifying relational properties
using a verification condition generator, without relying on code transformations
(such as self-composition) or making additional separation hypotheses in case of
aliasing. This method has been fully formalized in Coq, and the soundness of
recursive Hoare triple verification using a verification condition generator (itself
formally proved correct) for a simple language with procedure calls and aliasing
has been formally established. Our formalization is well-adapted for proving
possible optimizations of a VCGen and for using optimized VCGen versions for
relational property verification.
    This work sets up a basis for the formalization of modular verification of
relational properties using verification condition generation. We plan to extend
it with more features such as the possibility to refer to the values of variables
before a function call in the postcondition (in order to relate them to the values
after the call) and the capacity to rely on relational properties during the proof of
other properties. Future work also includes an implementation of this technique
inside a tool like RPP [9] in order to integrate it with SMT solvers and to
evaluate it on benchmarks. The final objective would be to obtain a system
similar to the verification of Hoare triples, namely, having relational procedure
contracts, relational assertions, and relational invariants. Currently, for relational
properties, product programs [2] or other self-composition optimizations [31]
are the standard approach to deal with complex loop constructions. We expect
that user-provided coupling invariants and loop properties can avoid having to
rely on code transformation methods. Moreover, we expect termination and co-
termination [16],[34] to be used to extend the modularity of relational contracts.
9
    https://formal.kastel.kit.edu/projects/improve/reve/


                                          17
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
11. Blazy, S., Maroneze, A., Pichardie, D.: Verified validation of program slicing. In:
    Proc. of the 2015 Conference on Certified Programs and Proofs (CPP 2015). pp.
    109–117. ACM (2015). https://doi.org/10.1145/2676724.2693169
12. Dufay, G., Felty, A.P., Matwin, S.: Privacy-sensitive information flow with JML.
    In: Proc. of the 20th Conference on Automated Deduction (CADE 2005). LNCS,
    vol. 3632, pp. 116–130. Springer (2005). https://doi.org/10.1007/11532231 9
13. Eilers, M., Müller, P., Hitz, S.: Modular product programs. In: Proc. of the 27th
    European Symposium on Programming (ESOP 2018). LNCS, vol. 10801, pp. 502–
    529. Springer (2018). https://doi.org/10.1007/978-3-319-89884-1 18
14. Flanagan, C., Saxe, J.B.: Avoiding exponential explosion: generating compact
    verification conditions. In: Proc. of the 28th ACM SIGPLAN Symposium on


                                          18
    Principles of Programming Languages (POPL 2001). pp. 193–205. ACM (2001).
    https://doi.org/10.1145/360204.360220
15. Floyd, R.W.: Assigning meanings to programs. In: Proc. of Symposia in Ap-
    plied Mathematics. vol. 19 (Mathematical Aspects of Computer Science), p. 19–32
    (1967). https://doi.org/10.1090/psapm/019/0235771
16. Hawblitzel, C., Kawaguchi, M., Lahiri, S.K., Rebêlo, H.: Towards modularly com-
    paring programs using automated theorem provers. In: Proc. of the 24th Interna-
    tional Conference on Automated Deduction (CADE 2013). LNCS, vol. 7898, pp.
    282–299. Springer (2013). https://doi.org/10.1007/978-3-642-38574-2 20
17. Herms, P.: Certification of a Tool Chain for Deductive Program Veri-
    fication. Phd thesis, Université Paris Sud - Paris XI (Jan 2013),
    https://tel.archives-ouvertes.fr/tel-00789543
18. Hoare, C.A.R.: An axiomatic basis for computer programming. Communications
    of the ACM 12(10), 576–580 (1969). https://doi.org/10.1145/363235.363259
19. Jourdan, J., Laporte, V., Blazy, S., Leroy, X., Pichardie, D.: A formally-verified C
    static analyzer. In: Proc. of the 42nd Annual ACM SIGPLAN-SIGACT Symposium
    on Principles of Programming Languages (POPL 2015). pp. 247–259. ACM (2015).
    https://doi.org/10.1145/2676726.2676966
20. Jung, R., Krebbers, R., Jourdan, J., Bizjak, A., Birkedal, L., Dreyer, D.: Iris from
    the ground up: A modular foundation for higher-order concurrent separation logic.
    J. Funct. Program. 28, e20 (2018). https://doi.org/10.1017/S0956796818000151
21. Kiefer, M., Klebanov, V., Ulbrich, M.: Relational program reasoning using compiler
    IR - combining static verification and dynamic analysis. J. of Automated Reasoning
    60(3), 337–363 (2018). https://doi.org/10.1007/s10817-017-9433-5
22. Kip, I.: Assembly Language for x86 Processors. Prentice Hall Press, 7th edn. (2014)
23. Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski, B.: Frama-
    C: A software analysis perspective. Formal Aspects of Computing 27(3), 573–609
    (2015). https://doi.org/10.1007/s00165-014-0326-7
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


                                          19
    tions. Software Foundations series, volume 1, Electronic textbook (2018),
    http://www.cis.upenn.edu/~ bcpierce/sf
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




                                       20
                                   Appendix

 A       Detailed Motivating Example

 Figure 9 provides a more detailed version of the motivating example presented
 in Section 1 and Fig. 1. Programs Csw1 and Csw2 contain, resp., C functions sw1
 and sw2, where pointers x1 and x2 are function parameters and variable x3 in
 Csw1 is a local variable. This choice is most natural in C.
     Recall that we consider a relational property Rsw :

Rsw : both programs, executed from two states in which *x1 has the same value
      for both programs and *x2 has the same value for both programs, will end
      up in two states in which each of these locations also has the same value.

     To prove the target relational property, a new composed C program Csw3
 with a C function sw3 is created (see Fig. 9) by composing the code of both
 functions. To distinguish variables of different programs, variables coming from
 Csw1 and Csw1 are marked, resp., with a suffix “_1” or “_2”.
     In the self-composition based approach, the target relational property for
 the composed program Csw3 is proved by the Hoare triple {P } Csw3 {Q}, where
 precondition P and postcondition Q are defined in Fig. 9. The definitions are
 expressed in the ACSL specification language [4]. Lines 5–6 in the definition
 of P state that each of *x1 and *x2 has the same value in the states before
 the execution of sw1 and sw2. Similarly, lines 5–6 in the definition of Q state
 the same properties after the execution of sw1 and sw2. However, the precondi-
 tion must also include additional constraints. Lines 9–11 in the definition of P
 provide usual preconditions for the swap function sw1 to be executed correctly:
 the input pointers must be valid and separated. For instance, validity of pointer
 x1_1 means that *x1_1 can be safely read and written. The separation property
 \separated(x1_1,x2_1) means that the locations *x1_1 and *x2_1 are disjoint,
 that is, do not share any byte10 . Lines 14–16 in the definition of P provide sim-
 ilar preconditions for the swap function sw2. For simplicity, we ignore arithmetic
 overflows in sw2: the specification and verification of properties about the ab-
 sence of arithmetic overflows are straightforward and orthogonal to the purpose
 of this paper.
     Notice that thanks to the choice of having pointers x1 and x2 as function
 parameters and variable x3 in Csw1 as a local variable, for this version we do not
 need to state explicitly other separation hypotheses stating that x1 and x2 do not
 10
      Notice that this separation property is stronger in C than the non-equality constraint
      x1_1 != x2_1, which does not exclude that both locations have some bytes in com-
      mon (if the pointers are not aligned). For simplicity, byte-related data representation
      and alignment constraints are not modeled in L, where the separation can be simply
      represented by non-equality constraints. This does not restrict the representativity
      of L for the purpose of our study.


                                              21
refer to x1, x2 and, for sw1, x3 themselves. Indeed, these separation hypotheses11
are already ensured by the fact that x1, x2 and, for sw1, x3 are allocated during
the call to the C function (and the pointers x1 and x2 are valid before the call).

     The aforementioned parts of P and Q naturally come from the relational
property Rsw and the preconditions of the considered functions: in this sense,
they are expected. However, they are not sufficient: in a real-life language with
possible aliasing like C, to model the behavior of both programs correctly within
the composed program and to prove the expected relational property, additional
separation hypotheses between the variables coming from both programs Csw1
and Csw2 are required. They are expressed by lines 20–23 in the definition of P
in Fig. 9.
     Such additional separation hypotheses become even more complex for real-
life programs, in particular in C, with a greater number of pointers and/or in
the presence of multiple pointers (such as double pointers, for instance, int **p).
Indeed, the required separation hypotheses for the composed program rapidly
become extremely hard to specify (or to generate) in order to ensure a sound
proof of relational properties on the composed program.

   With this definition of precondition P and postcondition Q, the code of Csw3
can be proved to satisfy its contract by the deductive verification plugin Wp of
Frama-C [23].




11
     In L, for simplicity, we consider only global variables, therefore, in the counterparts
     csw1 and csw2 in language L, these additional separation hypotheses must be explicit
     (as we show in Ex. 3 and Fig. 6). This slight difference of modeling is intentional
     in order to show the most natural version of these functions in C with function
     parameters and local variables rather than with global variables only.


                                             22
//C program Csw1 :                            //Composed C program Csw3 :
void sw1 ( int * x1 , int * x2 ) {            void sw3 ( int * x1_1 , int * x2_1
  int x3 ;                                        int * x1_2 , int * x2_2 ) {
  x3 = * x1 ;
  * x1 = * x2 ;                             //Code simulating Csw1 :
  * x2 = x3 ;                                 int x3_1 ;
}                                             x3_1 = * x1_1 ;
                                       {P }   * x1_1 = * x2_1 ;                    {Q}
                                              * x2_1 = x3_1 ;
//C program Csw2 :
void sw2 ( int * x1 , int * x2 ) {            //Code simulating Csw2 :
  * x1 = * x1 + * x2 ;                          * x1_2 = * x1_2 + * x2_2 ;
  * x2 = * x1 - * x2 ;                          * x2_2 = * x1_2 - * x2_2 ;
  * x1 = * x1 - * x2 ;                          * x1_2 = * x1_2 - * x2_2 ;
}                                             }


  1   //P is defined as follows:          1   //Q is defined as follows:
  2                                       2

  3 //Relation between initial            3 //Relation between resulting
  4 //values of Csw1 and Csw2 :           4 //values of Csw1 and Csw2 :
  5 * x1_1 == * x1_2 &&                   5 * x1_1 == * x1_2 &&

  6 * x2_1 == * x2_2 &&                   6 * x1_1 == * x1_2

  7                                       7

  8 //Preconditions for Csw1 :            8

  9 \valid ( x1_1 ) &&                    9

 10 \valid ( x2_1 ) &&                   10

 11 \separated ( x1_1 , x2_1 ) &&        11

 12                                      12

 13 //Preconditions for Csw2 :           13

 14 \valid ( x1_2 ) &&                   14

 15 \valid ( x2_2 ) &&                   15

 16 \separated ( x1_2 , x2_2 ) &&        16

 17                                      17

 18 //Extra hypotheses for               18

 19 //a correct simulation by Csw3 :     19

 20 \separated ( x1_1 , x1_2 ) &&        20

 21 \separated ( x1_1 , x2_2 ) &&        21

 22 \separated ( x2_1 , x1_2 ) &&        22

 23 \separated ( x2_1 , x2_2 )           23


Figure 9: Two C programs Csw1 and Csw2 swapping *x1 and *x2 and the Hoare
triple {P } Csw3 {Q} to prove a relational property between them using their
composition in C program Csw3 , as well as definitions of precondition P and
postcondition Q of Csw3 .



                                        23
             ξa JnKσ , n                                       ξb JtrueKσ , True
            ξa Jxi Kσ , σ(i)                                  ξb Jf alseKσ , False
           ξa J∗xi Kσ , σ(σ(i))                          ξb Ja1 op b a2 Kσ , ξa Ja1 Kσ op a ξa Ja2 Kσ
          ξa J&xi Kσ , i                                  ξb Jb1 op l b2 Kσ , ξb Jb1 Kσ op l ξb Jb2 Kσ
    ξa Ja1 op a a2 Kσ , ξa Ja1 Kσ op a ξa Ja2 Kσ                 ξb J¬bKσ , ¬ξb JbKσ

       Figure 10: Evaluation of arithmetic and Boolean expressions in L.

                    ψ
                                           ξa JaKσ = n                        ξa JaKσ = n
       hskip, σi → σ                              ψ                                   ψ
                                     hxi := a, σi → σ[i/n]           h∗xi := a, σi → σ[σ(i)/n]

                                                                                             ψ
            hassert(P ), σi → σ
                                 ψ                       ξb JbKσ = True        hc1 , σ1 i → σ2
                                                                                                 ψ
                                                      hif b then {c1 } else {c2 }, σ1 i → σ2

               ψ                       ψ                                                     ψ
      hc1 , σ1 i → σ2      hc2 , σ2 i → σ3               ξb JbKσ = False       hc2 , σ1 i → σ2
                            ψ                                                                    ψ
              hc1 ; c2 , σ1 i → σ3                    hif b then {c1 } else {c2 }, σ1 i → σ2

                                            ψ                                                    ψ
       ξb JbKσ1 = True          hc1 , σ1 i → σ2        hwhile b inv P do {c}, σ2 i → σ3
                                                                    ψ
                                hwhile b inv P do {c}, σ1 i → σ3

                                                                                         ψ
                   ξb JbKσ = False                                 hbodyψ (y), σ1 i → σ2
                                            ψ                                        ψ
      hwhile b inv P do {c}, σi → σ                                 hcall(y), σ1 i → σ2

                Figure 11: Operational semantics of commands in L.

B     Complete Semantics of Language L

B.1    Evaluation of Arithmetic and Boolean Expressions in L
We provide a complete list of rules for evaluation of arithmetic and Boolean
expressions in L in Fig. 10. Evaluation of arithmetic and Boolean expressions
in L is defined by functions ξa and ξb . As mentioned above, the subtraction is
lower-bounded by 0. Operations ∗xi and &xi have a semantics similar to the C
language, i.e. dereferencing and address-of. Semantics of Boolean expressions is
standard [36].

B.2    Operational Semantics of Commands in L in L
We provide a complete operational semantics of commands in L in Fig. 11.




                                                   24
