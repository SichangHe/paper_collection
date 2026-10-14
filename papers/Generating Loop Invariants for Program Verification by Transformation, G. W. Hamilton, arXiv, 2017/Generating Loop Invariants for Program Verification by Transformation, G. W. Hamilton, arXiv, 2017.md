    Generating Loop Invariants for Program Verification by
                      Transformation

                                               G.W. Hamilton
                                             School of Computing
                                             Dublin City University
                                                    Ireland
                                         hamilton@computing.dcu.ie



      Loop invariants play a central role in the verification of imperative programs. However, finding
      these invariants is often a difficult and time-consuming task for the programmer. We have previously
      shown how program transformation can be used to facilitate the verification of functional programs,
      but the verification of imperative programs is more challenging due to the need to discover these loop
      invariants. In this paper, we describe a technique for automatically discovering loop invariants. Our
      approach is similar to the induction-iteration method, but avoids the potentially exponential blow-up
      in clauses that can result when using this and other methods. Our approach makes use of the distil-
      lation program transformation algorithm to transform clauses into a simplified form that facilitates
      the identification of similarities and differences between them and thus help discover invariants. We
      prove that our technique terminates, and demonstrate its successful application to example programs
      that have proven to be problematic using other approaches. We also characterise the situations where
      our technique fails to find an invariant, and show how this can be ameliorated to a certain extent.


1    Introduction
The verification of imperative programs generally involves annotating programs with assertions, and
then using a theorem prover to check these annotations. Central to this annotation process is the use
of loop invariants which are assertions that are true before and after each iteration of a loop. However,
finding these invariants is a difficult and time-consuming task for the programmer, and they are often
reluctant to do this. In previous work [14], we have shown how to make use of program transformation
in the verification of functional programs. However, the verification of imperative programs is not so
straightforward due to the need to discover these invariants prior to verification. In this paper, we describe
a technique for automatically discovering loop invariants, thus relieving the programmer of this burden.
Our technique relies upon the programmer having provided a postcondition for the program; this is much
less onerous than providing loop invariants as it generally forms part of the specification of the program.
    The technique we describe is similar to the induction-iteration method of Suzuki and Ishihata [30],
but we overcome the problems associated with that method which were potential non-termination and
exponential blow-up in the size of clauses. Similarly to the induction-iteration method, our technique
involves working backward through the iterations of a loop and determining the assertions that are true
before each iteration. We use the distillation program transformation [13, 15] to transform assertions into
a simplified form that facilitates the identification of similarities and differences between them. Com-
monalities between these assertions are identified, and they are generalised accordingly to give a putative
loop invariant that can then be verified. We prove that our technique terminates and demonstrate its suc-
cessful application to example programs that have proven to be problematic using other approaches. We
also characterise the situations where our technique fails to find an invariant.

A. Lisitsa, A. Nemytykh, M. Proietti (Eds.):
Verification and Program Transformation (VPT 2017)
EPTCS 253, 2017, pp. 36–53, doi:10.4204/EPTCS.253.5
G.W. Hamilton                                                                                            37


    The remainder of this paper is structured as follows. In Section 2, we describe the simple imperative
language that will be used throughout the paper. In Section 3, we provide some background on the use
of loop invariants in the verification of programs written in this language. In Section 4, we give a brief
overview of the distillation program transformation algorithm which is used to simplify assertions in our
approach. In Section 5, we describe our technique for the automatic generation of loop invariants and
prove that it terminates. In Section 6, we give a number of examples of the application of our technique,
demonstrating where it succeeds on problematic examples and where it does not. In Section 7, we
consider related work and compare these to our own our technique. Section 8 concludes and considers
future work.


2    Language
In this section, we introduce our object language, which is a simple imperative programming language.
Definition 2.1 (Language Syntax) The syntax of our object language is as shown in Figure 1.

                           S    ::=    SKIP                            Do nothing
                                   |   V := E                          Assignment
                                   |   S1 ; S2                         Sequence
                                   |   IF B THEN S1 ELSE S2            Conditional
                                   |   BEGIN VAR V1 . . .Vn S END      Local block
                                   |   WHILE B DO S                    While loop

                                          Figure 1: Language Syntax

E corresponds to natural number expressions which belong to the following datatype:

                                           Nat ::= Zero | Succ Nat
We use the shorthand notation 0, 1, . . . for Zero, Succ Zero, . . .

B corresponds to boolean expressions which belong to the following datatype:

                                             Bool ::= True | False

These expressions are defined in a simple functional language with the following syntax.
Definition 2.2 (Expression Syntax) The syntax of expressions in our language is as shown in Figure 2.
An expression can be a variable, constructor application, λ -abstraction, function call, application, CASE
or WHERE. Variables introduced by λ -abstractions, CASE patterns and WHERE definitions are bound;
all other variables are free. We use f v(E) to denote the free variables of E and write E ≡ E ′ if E and E ′
differ only in the names of bound variables.
     The constructors are those specified above (Zero, Succ, True, False). We assume a number of pre-
defined operators written in this language; the explicit definitions of these operators are unfolded as part
of our transformation rather than appealing to properties such as associativity, etc. For natural num-
ber expressions the operators (+, −, ∗, /, %,∧ ) implement natural number addition, subtraction, mul-
tiplication, division, modulus and exponentiation respectively. For boolean expressions the operators
(∧, ∨, ¬, ⇒) implement conjunction, disjunction, negation and implication respectively. The relational
operators (<, >, ≤, ≥, =, 6=) are also defined.
38                                                                                    Generating Loop Invariants


                E    ::=    V                                          Variable
                        |   C E1 . . . Ek                              Constructor Application
                        |   λ V.E                                      λ -Abstraction
                        |   F                                          Function Call
                        |   E0 E1                                      Application
                        |   CASE E0 of P1 → E1 | · · · | Pk → Ek       Case Expression
                        |   E0 WHERE F1 = E1 . . . Fn = En             Local Function Definitions

                P    ::=    C V1 . . . Vk                              Pattern

                                            Figure 2: Expression Syntax

Definition 2.3 (Substitution) θ = {V1 7→ E1 , . . . ,Vn 7→ En } denotes a substitution. If E is an expres-
sion, then E θ = E{V1 7→ E1 , . . . ,Vn 7→ En } is the result of simultaneously substituting the expressions
E1 , . . . , En for the corresponding variables V1 , . . . ,Vn , respectively, in the expression E while ensuring that
bound variables are renamed appropriately to avoid name capture.
We reason about the behaviour of our imperative programming language using Floyd-Hoare style logic
[9, 17]. Specifications in this logic take the form of a triple {P} S {Q}, where P and Q are boolean
expressions that denote the pre- and post-conditions respectively for imperative program S i.e. if P is
true, then after execution of S, Q will be true. These are therefore partial correctness specifications, and
do not say anything about the termination of programs.
Definition 2.4 (Floyd-Hoare Logic) The rules and axioms of Floyd-Hoare logic for our imperative lan-
guage are as shown in Figure 3.

                            {P} SKIP {P}                           {Q{V := E}} V := E {Q}

                    {P} S1 {Q},      {Q} S2 {R}              {P ∧ B} S1 {Q},  {P ∧ ¬B} S2 {Q}
                          {P} S1 ; S2 {R}                      {P} IF B THEN S1 ELSE S2 {Q}

             {P} S {Q}, V1 . . .Vn ∈
                                   / f v(P), f v(Q)                     {I ∧ B} S {I}
             {P} BEGIN VAR V1 . . .Vn S END {Q}                   {I} WHILE B DO S {I ∧ ¬B}

                      P ⇒ P′ ,  {P′ } S {Q}                          {P} S {Q′ },  Q′ ⇒ Q
                           {P} S {Q}                                       {P} S {Q}

                                            Figure 3: Floyd-Hoare Logic

In the rule for the WHILE loop, the assertion I is called the loop invariant.


3    Loop Invariants
A loop invariant is an assertion that is true before and after each iteration of the loop, and usually needs to
be provided by the programmer. A loop which is annotated in this way is denoted by WHILE B DO {I} S
Definition 3.1 (Requirements of Loop Invariants) The three requirements of the invariant I of the loop
{P} WHILE B DO {I} S {Q} are as follows:
G.W. Hamilton                                                                                              39


    1. P ⇒ I
    2. {I ∧ B} S {I}
    3. (I ∧ ¬B) ⇒ Q
Thus, the precondition P should establish the invariant before executing the loop, the loop body S should
maintain the invariant, and the invariant should be sufficient to establish the postcondition Q after exiting
the loop.
Example 1 Consider the program shown in Figure 4.

                                              {n ≥ 0}
                                              x := 0;
                                              y := 1;
                                              WHILE x < n DO
                                                BEGIN
                                                  x := x + 1;
                                                  y := y ∗ k
                                                END
                                              {y = k∧ n}

                                        Figure 4: Example Program

This program calculates the exponentiation k∧ n. Say we wish to construct an invariant for the loop
in this program which will allow it to be verified. In [10] it is observed that the required invariant is
often a weakening of the postcondition for the loop and can be obtained by mutating this postcondition.
The assertion y = k∧ x is an invariant for this loop which is a mutation of the postcondition. However,
this invariant is not sufficient to allow verification of this program; the additional invariant x ≤ n is also
required. In general, the problem of constructing appropriate invariants which are sufficient to allow
programs to be verified is undecidable. However, in this paper we show how we can automatically
generate invariants which are sufficient to allow a wide range of programs to be verified.
Our approach makes use of the weakest liberal precondition originally proposed by Dijkstra [6].
Definition 3.2 (Weakest Liberal Precondition) We define the weakest liberal precondition for pro-
grams in our language, denoted as W LP(S, Q), where S is a program and Q a postcondition. The
condition P = W LP(S, Q) if Q is true after execution of S, and no condition weaker than P satisfies
this. The key difference of a weakest liberal precondition as opposed to a weakest precondition is that it
does not say anything about the termination of programs. The rules for calculating W LP(S, Q) for our
programming language are as shown in Figure 5.
Note that the weakest liberal precondition calculation for a loop requires that it has already been anno-
tated with its invariant. This implies that we should apply our techniques to inner loops first to determine
their invariant before applying them to outer loops.


4    Distillation
The predicates produced in our approach are simplified using the distillation transformation [13, 15].
Distillation is a fold/unfold program transformation that builds on top of positive supercompilation [29],
40                                                                                         Generating Loop Invariants


                           W LP(SKIP, Q)             =     Q
                        W LP(V := E, Q)              =     Q{V := E}
                           W LP(S1 ; S2 , Q)         =     W LP(S1 ,W LP(S2 , Q))
           W LP(IF B THEN S1 ELSE S2 , Q)            =     (B ⇒ W LP(S1 , Q)) ∧ (¬B ⇒ W LP(S2 , Q))
       W LP(BEGIN VAR V1 . . .Vn S END, Q)           =     W LP(S, Q), where V1 . . .Vn ∈
                                                                                        / f v(Q)
              W LP(WHILE B DO {I} S, Q)              =     I ∧ ((B ∧ I) ⇒ W LP(S, I)) ∧ ((¬B ∧ I) ⇒ Q)

                                 Figure 5: Weakest Liberal Precondition


but is more powerful, thus allowing more simplifications to be performed. The main distinguishing
characteristic between the two algorithms is that in distillation, generalisation and folding are performed
with respect to recursive terms, while in positive supercompilation they are not. In the work described
here, we use distillation to transform predicates into a simplified form that facilitates the identification
of similarities and differences between them. In particular, pre-defined associative operators (such as
+,*,∧,∨), whose explicit definitions are unfolded as part of our transformation, are always transformed
into right-associative form (for example, (x + y) + z is transformed to x + (y + z)).

4.1 Embedding
Generalisation is performed if the predicate obtained from distillation is an embedding of a previously
distilled one. The form of embedding which we use to inform this process is known as homeomor-
phic embedding. The homeomorphic embedding relation was derived from results by Higman [16] and
Kruskal [21] and was defined within term rewriting systems [5] for detecting the possible divergence of
the term rewriting process. Variants of this relation have been used to ensure termination within positive
supercompilation [28], distillation [13, 15], partial evaluation [23] and partial deduction [2, 22].
Definition 4.1 (Expression Embedding) An expression E is embedded in expression E ′ if E E E ′ ,
where the binary relation E is defined as follows.
                               ∃i ∈ {1 . . . n}.E E Ei             ∀i ∈ {1 . . . n}.Ei E Ei′
                 V E V′         E E φ (E1 , . . . , En )       φ (E1 , . . . , En ) E φ (E1′ , . . . , En′ )
The first rule here is for variables, the second is a diving rule and the third is a coupling rule. Diving
detects a sub-expression embedded in a larger expression, and coupling matches all the sub-expressions
of two expressions which have the same top-level functor. Bound variables are handled by this relation
by requiring that they have the same de Bruijn indices. We write E  E ′ if expression E is coupled with
expression E ′ at the top level.

4.2 Generalisation
Definition 4.2 (Generalisation of Expressions) The generalisation of expressions E and E ′ (denoted
by E ⊓ E ′ ) is defined as shown below.
                            (φ (E1′′ , . . . , En′′ ), ni=1 θi , ni=1 θi′ ),   if φ = φ ′
                                                     S         S
                         
                         
                         
                         
                         
                               where
                                E = φ (E1 , . . . , En )
                         
               E ⊓ E′ =
                         
                               E ′ = φ ′ (E1′ , . . . , En′ )
                                ∀i ∈ {1 . . . n}.Ei ⊓ Ei′ = (Ei′′ , θi , θi′ )
                         
                         
                         
                         
                            (V, {V 7→ E}, {V 7→ E ′ }),                        otherwise (V is fresh)
                         
G.W. Hamilton                                                                                                  41


The result of this generalisation is a triple (E ′′ , θ , θ ′ ) where E ′′ is the generalised expression and θ and
θ ′ are substitutions s.t. E ′′ θ ≡ E and E ′′ θ ′ ≡ E ′ . Within these rules, if both expressions have the same
functor at the outermost level, this is made the outermost functor of the resulting generalised expression,
and the corresponding sub-expressions within the functor applications are then generalised. Otherwise,
both expressions are replaced by the same variable.

Definition 4.3 (Most Specific Generalisation) A most specific generalisation of expressions E and E ′
is an expression E ′′ such that for every other generalisation E ′′′ of E and E ′ , there is a substitution θ such
that E ′′ θ ≡ E ′′′ . The most specific generalisation, denoted by E△E ′, of expressions E and E ′ is computed
by exhaustively applying the following rewrite rule to the triple obtained from the generalisation E ⊓ E ′ :
                                                                                     
                                             E,                      E{V1 7→ V2 },
                            {V1 7→ E ′ ,V2 7→ E ′ } ∪ θ ,  ⇒  {V2 7→ E ′ } ∪ θ , 
                               {V1 7→ E ′′ ,V2 7→ E ′′ } ∪ θ ′      {V2 7→ E ′′ } ∪ θ ′
This minimises the substitutions by identifying common substitutions which were previously given dif-
ferent names.


5    Automatic Generation of Loop Invariants
5.1 Algorithm
In order to calculate loop invariants, starting from the postcondition, we work our way backwards through
each iteration of the loop generating successive approximations to the loop invariant. If the current
approximation is an embedding of a previous one (coupled at the top level) then these approximations
are generalised with respect to each other. This process is continued until the current approximation is
a renaming of a previous one; this is then the putative invariant for the loop. If there are a number of
different possible paths through the loop, then a number of possible preconditions will be calculated for
it; these are collapsed into a single precondition by being generalised with respect to each other, thus
producing a single approximation for each loop iteration.
     Our algorithm for the automatic generation of an invariant for the loop WHILE B DO S with postcon-
dition Q is as shown in Figure 6. Here, P is the current predicate (initially equivalent to ¬B ∧ Q, which

       f (distill(¬B ∧ Q)) 0/
       where
       f P φ = if ∃Q ∈ φ s.t. Q ≡ P (modulo variable renaming)
                then return P
                else if ∃Q ∈ φ s.t. Q  P
                     then f P′ φ where P′ = P△Q
                                     i
                                     n
                     else return f ( {distill(B ∧ Pi )) (φ ∪ {P})
                                      i=1
                                                  n
                                                  ^
                          where W LP(S, P) =            Pi
                                                  i=1


                              Figure 6: Algorithm for Finding Loop Invariants

is true if the loop is exited) and φ is the set of previous approximations to the invariant (initially empty).
42                                                                                                 Generating Loop Invariants


If P is a renaming of a predicate in φ , then P is returned as the putative invariant. If there is a predicate
Q in φ which is embedded in P (coupled at the top level), then P and Q are generalised with respect to
each other, and the algorithm is further applied to this generalisation. Otherwise, the predicate which is
true before the previous execution of the loop body is calculated. The conjuncts of this predicate are then
combined with the loop condition (which must have been true for the loop body to be executed), sim-
plified using distillation and generalised together. The algorithm is then further applied to the resulting
generalised predicate with P added to φ .
     The generated invariant may contain generalisation variables; inductive definitions for these variables
can be determined using the three requirements for loop invariants (Definition 3.1). We try to find values
for these variables that satisfy each of these requirements using our Poitı́n theorem prover [12]1 . If we
are not able to satisfy all three of these requirements, then we have failed in finding a suitable invariant.
     For the loop {P} WHILE B DO {I} S {Q}, the initial value of generalisation variable v can be
obtained by satisfying the following for v0 using the first requirement:
                                                         P ⇒ I{v := v0 }
The inductive definition of v can be obtained by satisfying the following for vi+1 using the second re-
quirement:
                                             {I{v := vi } ∧ B} S {I{v := vi+1 }}
The final value of v can be obtained by satisfying the following for vn using the third requirement:
                                                     (I{v := vn } ∧ ¬B) ⇒ Q

5.2 Example
Example 1 We illustrate this algorithm by applying it to the example program in Figure 4.

Firstly, we calculate the logical assertion which is true if the loop is exited:
                                                      ¬(x < n) ∧ y = k∧ n
This is simplified by distillation to the following2 :

                                                         x ≥ n ∧ y = k∧ n                                                          (1)

Then, we calculate the logical assertion which is true before the final execution of the loop body:
                             WLP(BEGIN x := x + 1; y := y ∗ k END, x ≥ n ∧ y = k∧ n)
This gives the following:
                                                     x + 1 ≥ n ∧ y ∗ k = k∧ n
In conjunction with the loop condition (x < n), this is simplified to the following by distillation:

                                                     x + 1 = n ∧ y ∗ k = k∧ n                                                      (2)

This is not an embedding of (1), so the calculation continues. We next calculate the logical assertion
which is true before the penultimate execution of the loop body:
     1 This could also be done using a SAT solver.
   2 For this and all following examples, the result of distillation is simplified by replacing any instances of the definitions of the

pre-defined operators of our language with a corresponding call of the operator; the results would be too unwieldy otherwise.
G.W. Hamilton                                                                                                                43


                        WLP(BEGIN x := x + 1; y := y ∗ k END, x + 1 = n ∧ y ∗ k = k∧ n)
This gives the following:
                                           (x + 1) + 1 = n ∧ (y ∗ k) ∗ k = k∧ n
In conjunction with the loop condition (x < n), this is simplified to the following by distillation:

                                           x + (1 + 1) = n ∧ y ∗ (k ∗ k) = k∧ n                                              (3)

We can see that (3) is an embedding of (2), so generalisation is performed to produce the following:

                                                 x + v = n ∧ y ∗ w = k∧ n                                                    (4)

This is not an embedding, so the logical assertion which is true before execution of the loop body is now
re-calculated as follows:
                       WLP(BEGIN x := x + 1; y := y ∗ k END, x + v = n ∧ y ∗ w = k∧ n)
This gives the following:
                                           (x + 1) + v = n ∧ (y ∗ k) ∗ w = k∧ n
In conjunction with the loop condition (x < n), this is simplified to the following by distillation:

                                           x + (1 + v) = n ∧ y ∗ (k ∗ w) = k∧ n                                              (5)

We can see that (5) is an embedding of (4), so generalisation is performed to produce the following:

                                                 x + v′ = n ∧ y ∗ w′ = k∧ n                                                  (6)

We can now see that (6) is a renaming of (4), so (6) is our putative invariant We now try to find inductive
definitions for the generalisation variables v′ and w′ from the three requirements of loop invariants given
in Definition 3.1, which we do using our theorem prover Poitı́n.
    The initial values of the generalisation variables, given by v′0 and w′0 can be determined using the first
invariant requirement as follows:
                                 n ≥ 0 ∧ x = 0 ∧ y = 1 ⇒ x + v0′ = n ∧ y ∗ w0′ = k∧ n
The assignments v′0 := n and w′0 := k∧ n satisfy this assertion.
    The inductive values of the generalisation variables, given by v′i+1 and w′i+1 , can be determined using
the second invariant requirement as follows:
                 x + vi′ = n ∧ y ∗ wi′ = k∧ n ∧ x < n ⇒ (x + 1) + vi+1
                                                                   ′                    ′
                                                                       = n ∧ (y ∗ k) ∗ wi+1 = k∧ n
The assignments v′i+1 := v′i − 1 and w′i+1 := w′i /k satisfy this assertion.
    The final values of the generalisation variables, given by v′n and w′n , can be determined using the third
invariant requirement as follows:
                                  x + vn = n ∧ y ∗ wn = k∧ n ∧ ¬(x < n) ⇒ y = k∧ n
The assignments vn := 0 and wn = 1 satisfy this assertion. The discovered invariant is therefore equivalent
to the following3 :
                                                      x ≤ n ∧ y = k∧ x
   3 Our technique does not actually convert the discovered invariant into this simplified form; however the discovered inductive

version is sufficient for the purpose of verifying the program.
44                                                                                 Generating Loop Invariants


5.3 Termination
In order to prove that our loop invariant algorithm always terminates, we firstly need to show that in any
infinite sequence of predicates P0 , P1 , . . . there definitely exists some i < j where Pi  Pj . This amounts
to proving that the embedding relation  is a well-quasi order.
Definition 5.1 (Well-Quasi Order) A well-quasi order on set S is a reflexive, transitive relation ≤ such
that for any infinite sequence s1 , s2 , . . . of elements from S there are numbers i, j with i < j and si ≤ s j .

Lemma 5.2 ( is a Well-Quasi Order) The embedding relation  is a well-quasi order on any se-
quence of predicates.

Proof. The proof is similar to that given in [20]. It involves showing that there are a finite number of
functors (function names and constructors) in the language. Applications of different arities are replaced
with separate constructors; we prove that arities are bounded so there are a finite number of these. We also
replace case expressions with constructors. Since bound variables are defined using de Bruijn indices,
each of these are replaced with separate constructors; we also prove that de Bruijn indices are bounded.
The overall number of functors is therefore finite, so Kruskal’s tree theorem can then be applied to show
that  is a well-quasi-order.                                                                             2

Theorem 5.3 (Termination) The loop invariant algorithm always terminates.
Proof. The proof is by contradiction. If the loop invariant algorithm did not terminate then the set
of invariants generated as successive approximations to the invariant must be infinite. Every new predi-
cate which is added to the set of approximations cannot have any of the previously generated predicates
on this set embedded within it by the homeomorphic embedding relation , since either generalisation
would have been performed or a renaming encountered and the algorithm terminated. However, this
contradicts the fact that  is a well-quasi-order (Lemma 5.2).                                        2



6    Further Examples
In this section, we consider further examples that have been found to be problematic in techniques (in-
cluding our own) for the automatic discovery of invariants.
Example 2 Consider the following example program:

 {n ≥ 0}
 x := n;
 y := 1;
 z := k;
 WHILE x > 0 DO
   BEGIN
     IF x%2 = 1 THEN y := y ∗ z ELSE SKIP;
     x := x/2;
     z := z ∗ z
   END
 {y = k∧ n}
G.W. Hamilton                                                                                            45



This program also calculates the exponentiation k∧ n. This example is problematic using other approaches
(as discussed in Section 7) because of the presence of the conditional inside the loop, which causes an
exponential blow-up in the size of the generated predicates; we show how this blow-up is avoided using
our approach. In the following, we use S to denote the body of the loop in the above program. Firstly,
we calculate the logical assertion which is true if the loop is exited:
                                             ¬(x > 0) ∧ y = k∧ n
This is simplified by distillation to the following:

                                               x ≤ 0 ∧ y = k∧ n                                          (7)

Then, we calculate the logical assertion which is true before the final execution of the loop body:
                                          WLP(S, x ≤ 0 ∧ y = k∧ n)
This gives the following:
               (x%2 = 1 ⇒ x/2 ≤ 0 ∧ y ∗ z = k∧ n) ∧ (¬(x%2 = 1) ⇒ x/2 ≤ 0 ∧ y = k∧ n)
In conjunction with the loop condition (x > 0), the second conjunct is simplified to True by distillation,
but the first conjunct is simplified to the following:

                                             x = 1 ∧ y ∗ z = k∧ n                                        (8)

This is not an embedding, so the calculation continues. We next calculate the logical assertion which is
true before the penultimate execution of the loop body:
                                        WLP(S, x = 1 ∧ y ∗ z = k∧ n)
This gives the following:
      (x%2 = 1 ⇒ x/2 = 1 ∧ (y ∗ z) ∗ (z ∗ z) = k∧ n) ∧ (¬(x%2 = 1) ⇒ x/2 = 1 ∧ y ∗ (z ∗ z) = k∧ n)
In conjunction with the loop condition (x > 0), the first conjunct is simplified to the following by distil-
lation:
                                   x = (2 ∗ 1) + 1 ∧ y ∗ (z ∗ (z ∗ z)) = k∧ n
and the second conjunct is simplified to the following:
                                         x = 2 ∗ 1 ∧ y ∗ (z ∗ z) = k∧ n
These are generalised with respect to each other to give the following:

                                          x = v ∧ y ∗ (z ∗ w) = k∧ n                                     (9)

This is not an embedding, so the logical assertion which is true before execution of the loop body is now
re-calculated as follows:
                                     WLP(S, x = v ∧ y ∗ (z ∗ w) = k∧ n)
This gives the following:
                            (x%2 = 1 ⇒ x/2 = v ∧ (y ∗ z) ∗ ((z ∗ z) ∗ w) = k∧ n) ∧
                              (¬(x%2 = 1) ⇒ x/2 = v ∧ y ∗ ((z ∗ z) ∗ w) = k∧ n)
In conjunction with the loop condition (x > 0), the first conjunct is simplified to the following by distil-
lation:
46                                                                                 Generating Loop Invariants


                                x = (2 ∗ v) + 1 ∧ y ∗ (z ∗ (z ∗ (z ∗ w))) = k∧ n
and the second conjunct is simplified to the following:
                                      x = 2 ∗ v ∧ y ∗ (z ∗ (z ∗ w)) = k∧ n
These are generalised with respect to each other to give the following:

                                       x = v′ ∧ y ∗ (z ∗ (z ∗ w′ )) = k∧ n                                 (10)

We can see that (10) is an embedding of (9), so generalisation is performed to give the following:

                                         x = v′′ ∧ y ∗ (z ∗ w′′ ) = k∧ n                                   (11)

We can now see that (11) is a renaming of (9), so (11) is our putative invariant. We now try to find induc-
tive definitions for the generalisation variables v′′ and w′′ from the three requirements of loop invariants
given in Definition 3.1, which we do using our theorem prover Poitı́n.
     The initial values of the generalisation variables, given by v′′0 and w′′0 can be determined using the
first invariant requirement as follows:
                        n ≥ 0 ∧ x = n ∧ y = 1 ∧ z = k ⇒ x = v0′′ ∧ y ∗ (z ∗ w0′′ ) = k∧ n
The assignments v′′0 := n and w′′0 := k∧ (n − 1) satisfy this assertion.
    The inductive values of the generalisation variables, given by v′′i+1 and w′′i+1 , can be determined using
the second invariant requirement as follows:
                                 x = vi′′ ∧ y ∗ (z ∗ wi′′ ) = k∧ n ∧ x > 0 ⇒
                       ((x%2 = 0 ⇒ x/2 = vi+1 ′′ ∧ (y ∗ z) ∗ ((z ∗ z) ∗ w′′ ) = k∧ n) ∧
                                                                           i+1
                         (¬(x%2 = 1) ⇒ x/2 = vi+1   ′′ ∧ y ∗ ((z ∗ z) ∗ w′′ ) = k∧ n))
                                                                          i+1
If x%2 = 0, the assignments v′′i+1 := v′′i /2 and w′′i+1 := w′′i /(z ∗ z) satisfy this assertion. Otherwise, the
assignments v′′i+1 := v′′i /2 and w′′i+1 := w′′i /z satisfy this assertion.
    The final values of the generalisation variables, given by v′′n and w′′n , can be determined using the third
invariant requirement as follows:
                             x = vn′′ ∧ y ∗ (z ∗ wn′′ ) = k∧ n ∧ ¬(x > 0) ⇒ y = k∧ n
The assignments v′′n := 0 and w′′n = 1/z satisfy this assertion. The discovered invariant is therefore equiv-
alent to the following (again, we do not actually convert the invariant into this simplified form):
                                                 y ∗ z∧ x = k∧ n
Example 3 Consider the following example program:

 {n ≥ 0}
 x := 0;
 y := 1;
 WHILE x < n DO
   BEGIN
     x := x + 1;
     z := 0;
     v := 0;
     WHILE z < k DO
       BEGIN
G.W. Hamilton                                                                                           47


        v := v + y;
        z := z + 1
      END;
    y := v
   END
 {y = k∧ n}

This program also calculates the exponentiation k∧ n, but can be problematic using other approaches
(as discussed in Section 7) because it uses a nested loop. We will assume that the programmer has given
the postcondition of the inner loop as {v = y ∗ k}. Note that our technique could also be applied without
this information, as the postcondition from the weakest liberal precondition calculation for the outer loop
body could be used instead. However, the invariant of the inner loop would have to be re-calculated for
every weakest liberal precondition calculation of the outer loop body. The logical assertion which is true
if the inner loop is exited is as follows:
                                            ¬(z < k) ∧ v = y ∗ k
This is simplified by distillation to the following:

                                              z ≥ k∧v = y∗k                                            (12)

Then, we calculate the logical assertion which is true before the final execution of the inner loop body:
                       WLP(BEGIN v := v + y; z := z + 1 END, z ≥ k ∧ v = y ∗ k)
This gives the following:
                                          z+1 ≥ k∧v+y = y∗k
In conjunction with the loop condition (z < k), this is simplified to the following by distillation:

                                          z+1 = k∧v+y = y∗k                                            (13)

This is not an embedding, so the calculation continues. The logical assertion which is true before the
penultimate execution of the inner loop body is as follows:
                   WLP(BEGIN v := v + y; z := z + 1 END, z + 1 = k ∧ v + y = y ∗ k)
This gives the following:
                                    (z + 1) + 1 = k ∧ (v + y) + y = y ∗ k
In conjunction with the loop condition (z < k), this is simplified to the following by distillation:

                                    z + (1 + 1) = k ∧ v + (y + y) = y ∗ k                              (14)

We can see that (14) is an embedding of (13), so generalisation is performed to produce the following:

                                          z+w = k∧v+u = y∗k                                            (15)

This is not an embedding, so the calculation continues. We next calculate the logical assertion which is
true before the penultimate execution of the inner loop body:
                   WLP(BEGIN v := v + y; z := z + 1 END, z + w = k ∧ v + u = y ∗ k)
This gives the following:
48                                                                              Generating Loop Invariants


                                   (z + 1) + w = k ∧ (v + y) + u = y ∗ k
In conjunction with the loop condition (z < k), this is simplified to the following by distillation:

                                   z + (1 + w) = k ∧ v + (y + u) = y ∗ k                                 (16)

We can now see that (16) is an embedding of (15), so generalisation is performed to produce the follow-
ing:
                                     z + w ′ = k ∧ v + u′ = y ∗ k                                   (17)
We can now see that (17) is a renaming of (15), so (17) is our putative invariant. We now try to find induc-
tive definitions for the generalisation variables w′ and u′ from the three requirements of loop invariants
given in Definition 3.1, which we do using our theorem prover Poitı́n.
     The initial values of the generalisation variables, given by w′0 and u′0 can be determined using the
first invariant requirement as follows:
                       n ≥ 0 ∧ x ≤ n ∧ z = 0 ∧ v = 0 ⇒ z + w0′ = k ∧ v + u′0 = y ∗ k
The assignments w′0 := k and u′0 := y ∗ k satisfy this assertion.
    The inductive values of the generalisation variables, given by w′i and u′i , can be determined using the
second invariant requirement as follows:
             z + wi′ = k ∧ v + u′i = y ∗ k ∧ z < k ⇒ (z + 1) + wi+1
                                                                ′   = k ∧ (v + y) + u′i+1 = y ∗ k
The assignments w′i+1 := w′i − 1 and u′i+1 := u′i − y satisfy this assertion.
    The final values of the generalisation variables, given by w′n and u′n , can be determined using the third
invariant requirement as follows:
                            z + wn′ = k ∧ v + u′n = y ∗ k ∧ ¬(z < k) ⇒ v = y ∗ k
The assignments w′n := 0 and u′n = 0 satisfy this assertion. This is equivalent to the following:
                                              z ≤ k∧v = y∗z
This invariant can then be used to calculate the invariant for the outer loop as shown in Example 1.

Example 4 Consider the following example program:

 {n ≥ 0}
 x := 0;
 y := 1;
 WHILE x < n DO
   BEGIN
     x := x + 1;
     y := k ∗ y
   END
 {y = k∧ n}

This program is very similar to that shown in Figure 4, except that the operands of the final multipli-
cation are swapped. We now show how this program is problematic using our approach. Firstly, we
calculate the logical assertion which is true if the loop is exited:
                                            ¬(x < n) ∧ y = k∧ n
G.W. Hamilton                                                                                           49


This is simplified by distillation to the following:

                                              x ≥ n ∧ y = k∧ n                                         (18)

Then, we calculate the logical assertion which is true before the final execution of the loop body:
                        WLP(BEGIN x := x + 1; y := k ∗ y END, x ≥ n ∧ y = k∧ n)
This gives the following:
                                          x + 1 ≥ n ∧ k ∗ y = k∧ n
In conjunction with the loop condition (x < n), this is simplified to the following by distillation:

                                          x + 1 = n ∧ k ∗ y = k∧ n                                     (19)

This is not an embedding, so the calculation continues. We next calculate the logical assertion which is
true before the penultimate execution of the loop body:
                    WLP(BEGIN x := x + 1; y := k ∗ y END, x + 1 = n ∧ k ∗ y = k∧ n)
This gives the following:
                                     (x + 1) + 1 = n ∧ k ∗ (k ∗ y) = k∧ n
In conjunction with the loop condition (x < n), this is simplified to the following by distillation:

                                     x + (1 + 1) = n ∧ k ∗ (k ∗ y) = k∧ n                              (20)

We can see that (20) is an embedding of (19), so generalisation is performed to produce the following:

                                          x + v = n ∧ k ∗ w = k∧ n                                     (21)

This is not an embedding, so the logical assertion which is true before execution of the loop body is now
re-calculated as follows:
                    WLP(BEGIN x := x + 1; y := y ∗ k END, x + v = n ∧ k ∗ w = k∧ n)
This gives the following:
                                       (x + 1) + v = n ∧ k ∗ w = k∧ n
In conjunction with the loop condition (x < n), this is simplified to the following by distillation:

                                       x + (1 + v) = n ∧ k ∗ w = k∧ n                                  (22)

We can see that (22) is an embedding of (21), so generalisation is performed to produce the following:

                                          x + v′ = n ∧ k ∗ w = k∧ n                                    (23)

We can now see that (23) is a renaming of (21), so (23) is our putative invariant. Using our theorem
prover Poitı́n, we are unable to prove that this invariant satisfies any of the three requirements for the
loop invariant given in Definition 3.1. The problem here is that a variable that is updated in the loop
body (in this case y) has been removed from the calculated invariant by generalisation. This situation
can be avoided to a certain extent by making sure that such variables appear in the left operand of binary
operations (as is the case in Example 1). This is because repeated applications of such operations are
always transformed into right-associative form by distillation, and any mismatches are more likely to
occur in the right operand. However, this may not always be possible if the operation is not commutative
or if both operands contain variables that are updated in the loop body.
50                                                                              Generating Loop Invariants


7    Related Work
The main approaches to the automatic generation of loop invariants include abstract interpretation, proof
planning, dynamic methods, using heuristics and the induction-iteration method. The earliest methods
for the automatic generation of loop invariants involved static analysis. Abstract interpretation is a sym-
bolic execution of programs over abstract domains (such as predicate abstraction domains or polyhedral
abstraction domains) that over-approximates the semantics of loop iteration. Predicate abstraction do-
mains [1, 11, 26, 4, 8] replace predicates with variables, which is similar to the generalisation we perform
in our approach. Constraint-based techniques rely on sophisticated decision procedures over non-trivial
mathematical domains (such as polynomials [27] or convex polyhedra [3]) to represent concisely the
semantics of loops with respect to certain properties. Loop invariants in these forms are extremely useful
but rarely sufficient to prove full functional correctness of programs.
     In [8], Flanagan and Qadeer describe the use of predicate abstraction to generate loop invariants.
Their approach differs from our own in that predicates are obtained by working forwards from the pre-
condition through successive iterations of the loop, as opposed to backwards from the postcondition in
our approach. A strongest postcondition semantics is therefore used in [8] as opposed to our weakest pre-
condition approach. Loop invariants are computed by iterative approximation. The first approximation is
obtained by abstracting the set of reachable states at loop entry. Each successive approximation enlarges
the current approximation to include the states reachable by executing the loop body once from the states
in the current approximation. The iteration terminates in a loop invariant since the abstract domain is
finite. However, this approach does suffer from the drawback that the approximations can grow exponen-
tially as they are a disjunction of the approximations for all the reachable states. This exponential growth
is avoided in our approach. Also, we argue that working forwards from the precondition makes it harder
to find the required invariant since (as observed in [10]), the required invariant is often a weakening of
the postcondition.
     In [19], a proof planning approach is used to synthesise loop invariants. This approach makes use
of failed attempts to prove a putative invariant correct. The proof attempts are applied to the verification
conditions generated for the putative invariant. If these proof attempts fail, the failure is analysed using
proof critics. One such critic is the generalisation critic, which performs generalisation in a similar way
to that described in our work, and is used to update the putative invariant to one which is more likely
to be correct. One drawback of this approach is that the original putative invariant has to be guessed,
although the postcondition is a good first guess. Another drawback is knowing which critics to apply
when, since multiple critics can discover the invariant, but some may do so more efficiently than others.
Also, it is not clear how this method could be applied to nested loops.
     In [7], invariants are discovered dynamically. Using this approach, the program is run over a test suite
of inputs. The corresponding outputs are analysed for patterns and relationships among the variables.
Candidate invariants are guessed by trying out a pre-defined set of user-provided templates (including
comparisons between variables, simple inequalities, and simple list comprehensions). These candidate
invariants are then tested against several program runs; the invariants that are not violated in any of the
runs are retained as likely invariants. This inference is not sound and only gives an educated guess.
However, a prototype tool called Daikon was implemented using these techniques, and has worked well
in practice and many of the guessed invariants are sound.
     In [10], Furia and Meyer describe the use of heuristics to synthesise loop invariants. This work is
based on the observation that the required invariant is often a weakening of the postcondition for the loop
and can be obtained by mutating this postcondition. The core idea is to generate candidate invariants by
mutating postconditions according to a few commonly recurring patterns. Although this idea works well
G.W. Hamilton                                                                                                      51


in many cases, it is not capable of generating the required invariant for the example program in Figure
4, as this requires the addition of an extra clause to the postcondition (y ≤ n), which is not one of the
described heuristics.
    The previous work which is closest to our own is the induction-iteration method of Suzuki and Ishi-
hata [30]. This method works as follows for the program {P} S1 ; WHILE B DO S2 {Q} with precondi-
tion P and postcondition Q. Firstly, the logical assertion which is true if the loop is exited is calculated
in a similar way to our technique:
                                                 P0 = (¬B ⇒ Q)
Then, similarly to our technique, the weakest liberal precondition is used to calculate the logical assertion
which is true before each execution of the loop body (in reverse order):
                                           Pi+1 = (B ⇒ W LP(S2 , Pi ))
                                                               ∞
                                                               V
The weakest liberal precondition of the loop is given by            Pi . In order to calculate this finitely, a number
                                                              i=0
of successive approximations are calculated for it until one is found that is a loop invariant, where the jth
                                   Vj
approximation is given by I j =         Pi. It then has to be shown that this approximation is true on entry to
                                  i=0
the loop and is also a loop invariant:
                                                P ⇒ W LP(S1 , I j )                                               (1)


                                             (I j ∧ B) ⇒ W LP(S2 , I j )                                          (2)
(2) is equivalent to the following:
                                                    I j ⇒ Pj+1                                                    (3)
This therefore suggests an iterative approach to finding the loop invariant. Successive values for I j can
be computed making use of the previous values. If (3) is satisfied for the current value of I j , then we are
done and I j is the required invariant. If (1) is not satisfied for the current value of I j , then we have failed
to find a suitable invariant. Otherwise, we carry on the iteration to I j+1 .
     One problem with this approach is that, unlike our own approach, it is not guaranteed to terminate.
This is avoided by limiting the number of iterations. It is found that in practice, for most of the small
examples tried, very few iterations are actually required. Another problem with this approach is that
there can be an exponential blow-up in clauses into increasingly larger conjunctions. This is particularly
the case for conditionals, and can degrade I j to such an extent that it never converges to a loop invariant.
This problem is avoided in [30] by cleverly designing the theorem prover to avoid this potential expo-
nential blow-up in clauses. In our approach, this problem is avoided by combining the conjuncts using
generalisation. Finally, the seminal work in [30] does not show how to deal with nested loops. However,
an extension to the technique which does this is described by Xu et al. [31]. This approach is very similar
to the way in which we also deal with nested loops.


8    Conclusions and Further Work
In this paper we have described a technique for automatically discovering loop invariants. The technique
we describe is similar to the induction-iteration method of Suzuki and Ishihata [30], but we overcome the
problems associated with that method. One of these problems was the potential non-termination of the
induction-iteration method; our technique is guaranteed to terminate but may not be able to find a suitable
52                                                                               Generating Loop Invariants


invariant. Another problem with the induction-iteration method is the potential exponential blow-up in
clauses into increasingly larger conjunctions. Our technique avoids this through the combination of these
conjuncts using generalisation. We have successfully demonstrated our technique on example imperative
programs that have proven to be problematic using other approaches. We have also characterised the
situations where our technique fails to find an invariant and shown how this can be ameliorated to a
certain extent.
     There are a number of possible directions for further work. Firstly, we need to extend our techniques
to languages with richer features. For example, we could extend the language to manipulate unbounded
data structures such as arrays. For such constructs, the required loop invariants need to be universally
quantified, but this can be handled by our theorem prover Poitı́n, so should not present a problem for
our technique. Another way in which the language could be extended would be to handle pointers.
Separation logic [24, 25] extends Floyd-Hoare logic to be able to handle pointers, so this seems to be
an obvious basis for the extension of our technique. It has already been shown by Ireland [18] how his
approach to invariant generation can be extended to handle pointers by making use of separation logic.
     One other possible direction for further work is extending our technique to deal with the termination
of programs. This would involve calculating the weakest precondition rather than the weakest liberal
precondition as we do here. This would require the generation of a variant in addition to an invariant,
and the refinement of the invariant to show that the variant is decreased on each iteration of the loop.
This appears to be a lot more challenging than the problem which is tackled here.


References
 [1] T. Agerwala & J. Misra (1978): Assertion Graphs for Verifying and Synthesizing Programs. Technical Report
     83, University of Texas, Austin doi:10.1.1.13.1126.
 [2] R. Bol (1993): Loop Checking in Partial Deduction. Journal of Logic Programming 16(1–2), pp. 25–46
     doi:10.1016/0743-1066(93)90022-9.
 [3] P. Cousot & N. Halbwachs (1978): Automatic Discovery of Linear Restraints Among Variables of a Pro-
     gram. In: Proceedings of the ACM Symposium on Principles of Programming Languages, pp. 84–96
     doi:10.1145/512760.512770.
 [4] S. Das, D.L. Dill & S. Park (1999): Experience With Predicate Abstraction. In: International Conference on
     Computer Aided Verification, LNCS, 1633, Springer, pp. 160–171 doi:10.1007/3-540-48683-6 16.
 [5] N. Dershowitz & J.-P. Jouannaud (1990): Rewrite Systems. In J. van Leeuwen, editor: Handbook of Theoret-
     ical Computer Science, Elsevier, pp. 244–320 doi:10.1016/B978-0-444-88074-1.50011-1.
 [6] E.W. Dijkstra (1975): Guarded Commands, Nondeterminacy and Formal Derivation of Programs. Commu-
     nications of the ACM 18, pp. 453–457 doi:10.1145/360933.360975.
 [7] M. Ernst, J. Cockrell, W. Griswold & D. Notkin (2001): Dynamically Discovering Likely Program In-
     variants to Support Program Evolution. IEEE Transactions in Software Engineering 27(2), pp. 1–25
     doi:10.1109/32.908957.
 [8] C. Flanagan & S. Qadeer (2002): Predicate Abstraction for Software Verification. In: Proceedings of the
     29th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, ACM Press,
     pp. 191–202 doi:10.1145/503272.503291.
 [9] R.W. Floyd (1967): Assigning Meanings to Programs. In: Proceedings of the American Mathematical Soci-
     ety Symposia on Applied Mathematics, 19, pp. 19–32 doi:10.1090/psapm/019/0235771.
[10] C.A. Furia & B. Meyer (2010): Inferring Loop Invariants Using Postconditions. In: Fields of Logic and
     Computation, Springer, pp. 277–300 doi:10.1007/978-3-642-15025-8 15.
G.W. Hamilton                                                                                                    53


[11] S. Graf & H. Saidi (1997): Construction of Abstract State Graphs With PVS. In: International Conference on
     Computer Aided Verification, LNCS, 1254, Springer, pp. 72–83 doi:10.1007/3-540-63166-6 10.
[12] G. W. Hamilton (2006): Poitı́n: Distilling Theorems From Conjectures. Electronic Notes in Theoretical
     Computer Science 151(1), pp. 143–160 doi:10.1016/j.entcs.2005.11.028.
[13] G.W. Hamilton (2007): Distillation: Extracting the Essence of Programs. In: Proceedings of the ACM
     SIGPLAN Symposium on Partial Evaluation and Semantics-Based Program Manipulation, pp. 61–70
     doi:10.1145/1244381.1244391.
[14] G.W. Hamilton (2007): Distilling Programs for Verification. Electronic Notes in Theoretical Computer
     Science 190(4), pp. 17–32 doi:10.1016/j.entcs.2007.09.005.
[15] G.W. Hamilton & N.D. Jones (2012): Distillation With Labelled Transition Systems. In: Proceedings of the
     ACM SIGPLAN Symposium on Partial Evaluation and Semantics-Based Program Manipulation, ACM, pp.
     15–24 doi:10.1145/2103746.2103753.
[16] G. Higman (1952): Ordering by Divisibility in Abstract Algebras. Proceedings of the London Mathematical
     Society 2, pp. 326–336 doi:10.1112/plms/s3-2.1.326.
[17] C.A.R. Hoare (1969): An Axiomatic Basis for Computer Programming. Communications of the ACM 12,
     pp. 576–583 doi:10.1145/363235.363259.
[18] A. Ireland (2006): Towards Automatic Assertion Refinement for Separation Logic. In: Proceedings of the
     International Conference on Automated Software Engineering, pp. 209–312 doi:10.1109/ASE.2006.69.
[19] A. Ireland & J. Stark (1997): On the Automatic Discovery of Loop Invariants. In: Fourth Nasa Langley
     Formal Methods Workshop, pp. 137–152 doi:10.1.1.16.9466.
[20] I. Klyuchnikov (2010): Supercompiler HOSC 1.1: Proof of Termination. Preprint 21, Keldysh Institute of
     Applied Mathematics, Moscow doi:10.1.1.182.2914.
[21] J.B. Kruskal (1960): Well-Quasi Ordering, the Tree Theorem, and Vazsonyi’s Conjecture. Transactions of
     the American Mathematical Society 95, pp. 210–225 doi:10.2307/1993287.
[22] M. Leuschel (1998): On the Power of Homeomorphic Embedding for Online Termination. In: Proceedings
     of the International Static Analysis Symposium, Pisa, Italy, pp. 230–245 doi:10.1007/3-540-49727-7 14.
[23] R. Marlet (1994): Vers une Formalisation de l’Évaluation Partielle. Ph.D. thesis, Université de Nice - Sophia
     Antipolis.
[24] P. O’Hearn, J. Reynolds & Y. Hongseok (2001): Local Reasoning About Programs That Alter Data Struc-
     tures. In: Proceedings of Computer Science Logic, Lecture Notes in Computer Science 2142, pp. 1–19
     doi:10.1007/3-540-44802-0 1.
[25] J.C. Reynolds (2002): Separation Logic: A Logic for Shared Mutable Data Structures. In: Proceedings of
     the Symposium on Logic in Computer Science, pp. 55–74 doi:10.1109/LICS.2002.1029817.
[26] H. Saidi & N. Shankar (1999): Abstract and Model Check While You Prove. In: International Confer-
     ence on Computer Aided Verification, Lecture Notes in Computer Science 1633, Springer, pp. 443–454
     doi:10.1007/3-540-48683-6 38.
[27] S. Sankaranarayanan, H. Sipma & Z. Manna (2004): Non-Linear Loop Invariant Generation Using Gr obner
     Bases. In: Proceedings of the ACM Symposium on Principles of Programming Languages, pp. 318–329
     doi:10.1145/964001.964028.
[28] M.H. Sørensen & R. Glück (1994): An Algorithm of Generalization in Positive Supercompilation. Lecture
     Notes in Computer Science 787, pp. 335–351 doi:10.1.1.49.1869.
[29] M.H. Sørensen, R. Glück & N.D. Jones (1996): A Positive Supercompiler. Journal of Functional Program-
     ming 6(6), pp. 811–838 doi:10.1017/S0956796800002008.
[30] N. Suzuki & K. Ishihata (1977): Implementation of an Array Bound Checker. In: 4th ACM Symposium on
     Principles of Programming Languages, ACM Press, pp. 132–143 doi:10.1145/512950.512963.
[31] Z. Xu & B. Reps, T. amd Miller (2000): Safety Checking of Machine Code. In: ACM SIGPLAN Conference
     on Programming Language Design and Implementation, ACM Press, pp. 70–82 doi:10.1145/349299.349313.
