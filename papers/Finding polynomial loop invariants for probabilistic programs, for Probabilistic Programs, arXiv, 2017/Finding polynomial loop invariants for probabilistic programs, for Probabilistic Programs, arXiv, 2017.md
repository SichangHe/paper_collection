                                                         Finding Polynomial Loop Invariants
                                                             for Probabilistic Programs

                                          Yijun Feng1 , Lijun Zhang2 , David N. Jansen2 (0000-0002-6636-3301), Naijun
                                                                    Zhan2 , and Bican Xia1
arXiv:1707.02690v1 [cs.LO] 10 Jul 2017




                                              1
                                                   LMAM & School of Mathematical Sciences, Peking University, Beijing, China
                                          2
                                                  State Key Laboratory of Computer Science, Institute of Software, CAS, Beijing,
                                                                                   China



                                                     Abstract. Quantitative loop invariants are an essential element in the
                                                     verification of probabilistic programs. Recently, multivariate Lagrange
                                                     interpolation has been applied to synthesizing polynomial invariants. In
                                                     this paper, we propose an alternative approach. First, we fix a polyno-
                                                     mial template as a candidate of a loop invariant. Using Stengle’s Posi-
                                                     tivstellensatz and a transformation to a sum-of-squares problem, we find
                                                     sufficient conditions on the coefficients. Then, we solve a semidefinite
                                                     programming feasibility problem to synthesize the loop invariants. If the
                                                     semidefinite program is unfeasible, we backtrack after increasing the de-
                                                     gree of the template. Our approach is semi-complete in the sense that it
                                                     will always lead us to a feasible solution if one exists and numerical errors
                                                     are small. Experimental results show the efficiency of our approach.


                                         1         Introduction
                                         Probabilistic programs extend standard programs with probabilistic choices and
                                         are widely used in protocols, randomized algorithms, stochastic games, etc. In
                                         such situations, the program may report incorrect results with a certain proba-
                                         bility, rendering classical program specification methods [11,18] inadequate. As a
                                         result, formal reasoning about the correctness needs to be based on quantitative
                                         specifications. Typically, a probabilistic program consists of steps that choose
                                         probabilistically between several states. and the specification of a probabilistic
                                         program contains constraints on the probability distribution of final states, e. g.
                                         through the expected value of a random variable. Therefore the expected value
                                         is often the object of correctness verification [23,21,14].
                                             To reason about correctness for probabilistic programs, quantitative anno-
                                         tations are needed. Most importantly, correctness of while loops can be proved
                                         by inferring special bounds on expectations, usually called quantitative loop in-
                                         variants [23]. As in the classical setting, finding such invariants is the bottle-
                                         neck of proving program correctness. For some restricted classes, such as linear
                                         loop invariants, some techniques have been established [25,21,3]. To use them
                                         to synthesize polynomial loop invariants, so-called linearization can be used [1],
                                         a technique widely applied in linear algebra. It views higher-degree monomi-
                                         als as new variables, establishes their relationship with existing variables, and
then exploits linear loop invariant generation techniques. However, the number
of monomials grows exponentially when the degree increases. Kapur et al. [29]
introduce solvable mappings, which are a generalization of affine mappings, to
avoid non-polynomial effects generated by polynomial programs. Recently, Chen
et al. [6] applied multivariate Lagrange interpolation to synthesize polynomial
loop invariants directly.
    Another important problem for probabilistic programs is the almost-sure
termination problem, answering whether the program terminates almost surely.
In [13], Fioriti and Hermanns argued that Lyapunov ranking functions, used
in non-probabilistic termination analysis, cannot be extended to probabilistic
programs. Instead, they extended the ranking supermartingale approach [2] to
the bounded probabilistic case, and provided a compositional and sound proof
method for the almost-sure termination problem. In [20], Kaminski and Katoen
investigated the computational complexity of computing expected outcomes (in-
cluding lower bounds, upper bounds and exact expected outcomes) and of de-
ciding almost-sure termination of probabilistic programs. In [5], Chatterjee et
al. further investigated termination problems for affine probabilistic programs.
Recently, they also presented a method [4] to efficiently synthesize ranking su-
permartingales through Putinar’s Positivstellensatz [28] and used it to prove the
termination of probabilistic programs. Their method is sound and semi-complete
over a large class of programs.
    In this paper, we develop a technique exploiting semidefinite programming
through another Positivstellensatz to synthesize the quantitative loop invariants.
Positivstellensätze are essential theorems in real algebra to describe the structure
of polynomials that are positive (or non-negative) on a semialgebraic set. While
our approach shares some similarities with the one in [4], the difference to the
termination problem requires a variation of the theorem. In detail, Putinar’s Pos-
itivstellensatz deals with the situation when the polynomial is strictly positive on
a quadratic module, which is not enough for quantitative loop invariants. In the
program correctness problem, equality constraints are taken into consideration
as well as inequalities. Therefore in our method, Stengle’s Positivstellensatz [30]
dealing with general real semi-algebraic sets is being used.
    As previous results [21,15,6], our approach is constraint-based [9]. We fix
a polynomial template for the invariants with a fixed degree and generate con-
straints from the program. The constraints can be transformed into an emptiness
problem of a semialgebraic set. By Stengle’s Positivstellensatz [30], it suffices to
solve a semidefinite programming feasibility problem, for which efficient solvers
exist. From a feasible solution (which may not be the tightest one) we can then
obtain the corresponding coefficients of the template. We verify the correctness
of the template. If the solver does not provide a feasible solution or if the coeffi-
cients are not correct, we refine the analysis by adding constraints to block the
undesired solutions and get a tighter invariant or increasing the degree of the
template, which will always lead us to a feasible solution if one exists.
    The method is applied to several case studies taken from [6]. The technique
usually solves the problem within one second, which is about one tenth of the
time taken by the tool described in [6]. Our tool supports real variables rather
than discrete ones, and supports programs that require polynomial invariants.
We illustrate these features by analyzing a non-linear perceptron program and a
model for airplane delay with continuous distributions. Moreover, we conduct a
sequence of trials on parameterized probabilistic programs to show that the main
influence factor on the running time of our method is the degree of the invariant
template. We compare our results on these examples with the Lagrange Inter-
polation Prototype (LIP) in [6], Prinsys [15] and the tool for super-martingales
(TM) [2].


2     Preliminaries

In this section we introduce some notations. We use Xn to denote an n-tuple
of variables (X1 , . . . , Xn ). For a vector
                                       P      α = (α1 , . . . , αn ) ∈ Nn , Xα
                                                                             n denotes the
              α1         αn
monomial X1 · · · Xn , and d = i αi is its degree.

Definition 1. A polynomial
                        P f in variables X1 , . . . , Xn is a finite linear combi-
nation of monomials: f = α cα Xα
                               n where finitely many cα ∈ R are non-zero.

The degree of a polynomial is the highest degree of its component monomials.
Extending the notation, for a sequence of polynomials Q        F = (f1 , . . . , fs ) and a
vector α = (α1 , . . . , αs ) ∈ Rs , we let F α denote si=1 fiαi . The polynomial ring
with n variables is denoted with R[Xn ], and the set of polynomials of degree at
most d is denoted with R≤d [Xn ]. For f ∈ R[Xn ] and zn = (z1 , . . . , zn ) ∈ Rn ,
f (zn ) ∈ R is the value of f at zn .
    A constraint is a quantifier-free formula constructed from (in)equalities of
polynomials. It is linear if it contains only linear expressions. A semialgebraic
set is a set described by a constraint:

Definition 2. A semialgebraic
                   V          set in Rk is a finite union of sets of the form
       k
{x ∈ R |f (x) = 0 ∧ g∈G g > 0}, where f is a polynomial and G is a finite set
of polynomials.
    A polynomial p(Xn ) ∈ R[Xn ] is a sum of squares (or SOS, for short),
                                                                    P     if there
exist polynomials f1 (x), . . . , fm (x) ∈ R[Xn ] such that p(Xn ) = m     2
                                                                      i=1 i (Xn ).
                                                                         f
Chapters 2 and 3 of [?] introduce a way to transform the problem whether a
given polynomial is an SOS into a semidefinite programming problem (or SDP, for
short), which is a generalization of linear programming problem. We introduce
the transformation and SDP problems briefly in Appendices A and B.


2.1    Probabilistic Programs

We use a simple probabilistic guarded-command language to construct probabilis-
tic programs with the grammar:

P ::= skip | abort | x := E | P ; P | P [p] P | if (G) then {P } else {P } | while(G){P }
where G is a Boolean expression and E is a real-valued expression defined by
the grammar:

      E ::= c | xn | r |                constant/variable/random variable
           E+E |E ·E |                  arithmetic
      G ::= E < E | G ∧ G | ¬G          guards

Random variable r follows a given probability distribution, discrete or continu-
ous. For p ∈ [0, 1], the probabilistic choice command P0 [p] P1 executes P0 with
probability p and P1 with probability 1 − p.


Example 3. The following probabilistic program P describes a simple game:

        z := 0; while(0 < x < y) {x := x + 1[0.5]x := x − 1; z := z + 1}.

The program models a game where a player has x dollars at the beginning and
keeps tossing a coin with probability 0.5. The player wins one dollar if he tosses
a head and loses one dollar for a tail. The game ends when the player loses all
his money, or he wins y − x dollars for a predetermined y. The variable z records
the number of tosses made by the player during this game.

    We assume that the reader is familiar with the basic concepts of probability
theory and in particular expectations, see e. g. [12] for details. Expectations are
typically functions from program states (i. e. the real-valued program variables)
to R. An expectation is called a post-expectation when it is to be evaluated on the
final distribution, and it is called a pre-expectation when it is to be evaluated on
the initial distribution. Let preE , postE be expectations and prog a probabilistic
program. We say that the sentence hpreE i prog hpostE i holds if the expected
value of postE after executing prog is equal to or greater than the expected
value of preE . When postE and preE are functions, the comparison is executed
pointwise.
    Classical programs can be viewed as special probabilistic programs in the
following sense. For classical precondition pre and postcondition post , let the
characteristic function χpre equal 1 if the precondition is true and 0 otherwise,
and define χpost similarly. If one considers a Hoare triple {pre} prog {post } where
prog is a classical program, then it holds if and only if hχpre i prog hχpost i holds
in the probabilistic sense.



2.2   Probabilistic Predicate Transformers


Let P0 , P1 be probabilistic programs, E an expression, post a post-expectation,
pre a pre-expectation, G a Boolean expression, and p ∈ (0, 1). The probabilistic
predicate transformer wp can be defined as follows [16]:

  wp(skip, post ) = post
  wp(abort, post ) = 0
  wp(x := E, post ) = post [x/ES (E)]
  wp(P ; Q, post) = wp(P, wp(Q, post ))
  wp(if(G) then(P ) else(Q), post ) = χG · wp(P, post ) + (1 − χG ) · wp(Q, post)
  wp(P [p] Q, post ) = p · wp(P, post ) + (1 − p) · wp(Q, post )
  wp(while(G) {P }, post) = µX.(χG · wp(P, X) + (1 − χG ) · post )

Here post [x/ES (E)] denotes the formula obtained by replacing free occurrences
of x in post by the expectation of expression E over the state space S. The least
fixed point operator µ is defined over the domain of expectations [25,23], and it
can be shown that hprei P hpost i holds if and only if pre ≤ wp(P, post ). Thus,
wp(P, post ) is the greatest lower bound of precondition expectation of P with
respect to post , and we say wp(P, post ) is the weakest pre-expectation of P w. r. t.
post.


2.3   Positivstellensatz

Hilbert’s Nullstellensatz is very important in algebra, and its real version, known
as Positivstellensatz, is crucial to our method. First, some concepts are needed
to introduce the theorem.

 – The set P ⊆ R[Xn ] is a positive cone if it satisfies: (i) If a ∈ R[Xn ], then
   a2 ∈ P , and (ii) P is closed under addition and multiplication.
 – The set M ⊆ R[Xn ] is a multiplicative monoid with 0 if it satisfies: (i)
   0, 1 ∈ M , and (ii) M is closed under multiplication.
 – The set I ⊆ R[Xn ] is an ideal if it satisfies: (i) 0 ∈ I, (ii) I is closed under
   addition, and (iii) If a ∈ I and b ∈ R[Xn ], then a · b ∈ I.

We are interested in finitely generated positive cones, multiplicative monoids
with 0, and ideals. Let F = {f1 , . . . , fs } be a finite set of polynomials. We recall
that

 – Any element in the positive cone generated by F (i. e., the smallest positive
   cone containing F ) is of the form
             X
                      kα F α   where kα is a sum of squares for all α ∈ {0, 1}s
           α∈{0,1}s


   In the sum, α denotes an s-length vector with each element 0 or 1.
 – Any nonzero element in the multiplicative monoid with 0 generated by F is
   of the form F α , where α = (α1 , . . . , αs ) ∈ Ns .
 – Any element in the ideal generated by F is of the form k1 f1 +k2 f2 +· · ·+ks fs ,
   where k1 , . . . , ks ∈ R[Xn ].
    The Positivstellensatz due to Stengle states that for a system of real polyno-
mial equalities and inequalities, either there exists a solution, or there exists a
certain polynomial which guarantees that no solution exists.
Theorem 4 (Stengle’s Positivstellensatz [30]). Let (fj )sj=1 , (gk )tk=1 , (hl )w
                                                                                l=1
be finite families of polynomials in R[Xn ]. Denote by P the positive cone gen-
erated by (fj )sj=1 , by M the multiplicative monoid with 0 generated by (gk )tk=1 ,
and by I the ideal generated by (hl )wl=1 . Then the following are equivalent:

1. The set                                                       
                                 fj (zn ) ≥ 0, j = 1, . . . , s 
                          zn ∈ Rn gk (zn ) 6= 0, k = 1, . . . , t               (1)
                                                                 
                                  hl (zn ) = 0, l = 1, . . . , w
   is empty.
2. There exist f ∈ P, g ∈ M, h ∈ I such that f + g 2 + h = 0.


3   Problem formulation

The question that concerns us here is to verify whether the loop sentence

                         hpreE i while(G) {body} hpostE i

holds, when given the pre-expectation preE , post-expectation postE , a Boolean
expression G, and a loop-free probabilistic program body. One way to solve
this problem is to calculate the weakest pre-expectation wp(while(G, {body}),
postE ) and to check whether it is not smaller than preE . However, the weakest
pre-expectation of a while statement requires a fixed-point computation, which
is not trivial. To avoid the fixed point, the problem can be solved through a
quantitative loop invariant.

Theorem 5 ([15]). Let preE be a pre-expectation, postE a post-expectation, G
a Boolean expression, and body a loop-free probabilistic program. To show

                        hpreE i while(G) {body} hpostE i,

it suffices to find a loop invariant I which is an expectation such that


1. (boundary) preE ≤ I and I · (1 − χG ) ≤ postE ;
2. (invariant) I · χG ≤ wp(body, I);
3. (soundness) the loop terminates with probability 1 from any state that satis-
   fies G, and
   (a) the number of iterations is finite, or
   (b) I is bounded from above by some fixed constant, or
   (c) the expected value of I ·χG tends to zero as the number of iterations tends
        to infinity.
Since soundness of a loop invariant is not related to pre- and postconditions and
can be verified from its type before any specific invariants are found, we focus on
the boundary and invariant conditions in Theorem 5. The soundness property
is left to be verified manually in case studies.
    For pre-expectation preE and post-expectation postE , the boundary and in-
variant conditions in Theorem 5 provide the following requirements for a loop
invariant I:
                                   preE ≤ I
                              I · (1 − χG ) ≤ postE                                         (2)
                                     I · χG ≤ wp(body, I).

    The inequalities induced by the boundary and invariant conditions contain
indicator functions, which we find difficult to analyze if they appear on both
sides. So first we rewrite the expectations to a standard form. For a Boolean
expression F , we use [F ] to represent its integer value, i. e. [F ] = 1 if F is true,
and [F ] = 0 otherwise. An expectation is in disjoint normal form (DNF) if it is
of the form
                             f = [F1 ] · f1 + · · · + [Fk ] · fk

where the Fi are disjoint expressions, which means any two of the expressions
cannot be true simultaneously, and the fi are polynomials.

Lemma 6 ([21]). Suppose f = [F1 ] · f1 + · · · + [Fk ] · fk and g = [G1 ] · g1 + · · · +
[Gl ] · gl are expectations over Xn in DNF. Then, f ≤ g if and only if (pointwise)

   k ^
     l
            "                      #
   ^
            Fi ∧ Gj ⇒ fi ≤ gj
  i=1 j=1
                             k
                                   "      ^
                                           l                           #
                             ^
                         ∧         Fi ∧         ¬Gj        ⇒ fi ≤ 0
                             i=1          j=1
                                                 l
                                                   " k                                #
                                                 ^   ^
                                             ∧                    ¬Fi       ∧ Gj ⇒ 0 ≤ gj . (3)
                                                 j=1        i=1


Example 7. Consider the following loop sentence for our running example:

hxy − x2 i z := 0; while(0 < x < y){x := x + 1 [0.5] x := x − 1; z := z + 1; } hzi

For this case, the following must hold for any loop invariant I.

                  xy − x2 ≤ I
       I · [x ≤ 0 ∨ y ≤ x] ≤ z
            I · [0 < x < y] ≤ 0.5 · I(x + 1, y, z + 1) + 0.5 · I(x − 1, y, z + 1)
By Lemma 6, these requirements can be written as

              xy − x2 ≤ I ∧                                                       (4)
      x≤0∨y≤x⇒I ≤z∧                                                               (5)
          0<x<y⇒0≤z∧                                                              (6)
          0 < x < y ⇒ I ≤ 0.5 · I(x + 1, y, z + 1) + 0.5 · I(x − 1, y, z + 1) ∧   (7)
      x ≤ 0 ∨ y ≤ x ⇒ 0 ≤ 0.5 · I(x + 1, y, z + 1) + 0.5 · I(x − 1, y, z + 1)     (8)

The program in this example originally served as a running example in [6]. There,
after transforming the constraints into the form above, Lagrange interpolation
is applied to synthesize the coefficients in the template. In our approach, we
check the correctness of each conjunct in (4–8) by checking the nonnegativity of
the polynomial on the right side over a semialgebraic set related to polynomials
on the left side. In this way, we can use the Positivstellensatz to synthesize the
coefficients.


4      Constraint Solving by Semidefinite Programming

Our aim is to synthesize coefficients for the fixed invariant template for simple
(Subsection 4.1) and nested (Subsection 4.2) programs. Checking the validity of
constraints can be transformed into checking the emptiness of a semialgebraic
set. Then, we show that the emptiness problem can be turned into sum-of-squares
constraints using Stengle’s Positivstellensatz.

Our Approach in a Nutshell. For a given polynomial template as a candidate
quantitative loop invariant, it needs to satisfy boundary and invariant condi-
tions. Our goal is to synthesize the coefficients in the template. These conditions
describe a semialgebraic set, and the satisfiability of the constraints is equivalent
to the non-emptiness of the corresponding semialgebraic set. Applying the Posi-
tivstellensatz (see Section 2.3), we will transform the problem to an equivalent
semidefinite programming problem using Lemma 8. Existing efficient solvers can
be used to solve the problem. A more efficient yet sufficient way is to transform
the problem into a sum-of-squares problem (see Appendix A) using Lemma 9
and then to solve it by semidefinite programming. After having synthesized the
coefficients of the template, we verify whether they are valid. In case of a neg-
ative answer, which may happen due to floating-point errors, some refinements
can be made by adding further constraints, which is described in Section 4.3. If
the problem is still unsolved, we try raising the maximum degree of the template
and reiterate the procedure.


4.1     Synthesis Algorithm for Simple Loop Programs

Now we are ready for the transformation method. Each conjunct obtained in
Lemma 6 is of the form F ⇒ G, where F is a quantifier-free formula constructed
from (in)equalities between polynomials in R≤d [Xn ], and G is of the form f ≤ g,
f ≤ 0 or 0 ≤ g, with f, g ∈ R≤d [Xn ]. If F contains negations, we use De Morgan’s
laws to eliminate them. If there is a disjunction in F , we split the constraints
into sub-constraints as ϕ ∨ ψ ⇒ χ is equivalent to (ϕ ⇒ V     χ) ∧ (ψ ⇒ χ). After
these simplifications, F ⇒ G can be written in    V the  form   i (fi Di 0) ⇒ g ≥ 0
where Di ∈ {≥, =}. Observe that a constraint i (fi Di 0) ⇒ g ≥ 0 is satisfied if
and only if the set {x|fi (x) Di 0 for all i; −g(x) ≥ 0; and g(x) 6= 0} is empty. In
this way, we transform our constraint into the form required by Theorem 4.
    Summarizing, Constraint (2) (the boundary and invariant conditions of The-
orem 5) is satisfied if and only if all semialgebraic sets created using the proce-
dure above are empty. Now we are ready to transform this constraint to an SDP
problem.

Lemma 8 ([26,10]). The emptiness of (1) is equivalent to the feasibility of an
SDP problem.

   See Appendix C.1 for a constructive proof. Although the transformation in
Lemma 8 is effective, it is complicated in practice. In the following lemma we
present a simpler yet sufficient procedure.

Lemma 9. The following statements hold (with Di ∈ {≥, =}):
1. f (Xn ) ≥ 0 ⇒ g(Xn ) ≥ 0 holds if g(Xn ) − u · f (Xn ) is a sum of squares for
   some u ∈ R≥0 .
2. f (Xn ) = 0 ⇒ g(Xn ) ≥ 0 holds if g(Xn ) − v · f (Xn ) is a sum of squares for
   some v ∈ R.
3. f1 (Xn ) D1 0 ∧ f2 (Xn ) D2 0 ⇒ g(Xn ) ≥ 0 holds if g(Xn ) − r1 · f1 (Xn ) − r2 ·
   f2 (Xn ) is a sum of squares for some r1 , r2 ∈ R; if Di is ≥, it is additionally
   required that ri ≥ 0.

The proof is in Appendix C.2. Note that Item (3) is one of the possible sufficient
relaxations; more general relaxations can be obtained by adding a cross product
r12 f1 (Xn )f2 (Xn ) and squares of the fi (Xn ).

Example 10. Applying the above procedure, Constraint (5) in Example 7 is split
into (x ≤ 0 ⇒ I ≤ z) ∧ (y ≤ x ⇒ I ≤ z) and then normalized to (−x ≥ 0 ⇒
z − I ≥ 0) ∧ (x − y ≥ 0 ⇒ z − I ≥ 0). This holds if z − I + u1 x is a SOS for
some u1 ∈ R≥0 and z − I + u2 (y − x) is a SOS for some u2 ∈ R≥0 . The other
constraints can be handled in a similar way.

   After applying the Positivstellensatz and Lemma 8, template coefficients for
the loop invariant can be synthesized efficiently by semidefinite programming.
The corresponding technique is introduced in Appendix B.
   We summarize our approach in Algorithm 1. The aim is to synthesize the
coefficients of template I. The terms in I are all terms with degree ≤ d in the
multiplicative monoid generated by Xn . Algorithm 1 is semi-complete in the
sense that it will generate an invariant if there exists one. Its termination is
guaranteed in principle by Theorem 4 and the equivalence between SOS and
Algorithm 1 Loop Invariant Generation with Refinement
Input: sentence := hpreE i while(G){body } hpostE i with program variables Xn
Output: a loop invariant satisfying the boundary and invariant conditions
 1: loop
 2:   d := 2
 3:   Choose a template for I ∈ R≤d [Xn ]
 4:   Let f be Constraint (2), i. e. the boundary and invariant conditions from Theo-
      rem 5, for sentence
 5:   Let constraints be the SDP problem equivalent to f according to Lemma 8
 6:   while constraints is feasible do
 7:      Set the coefficients in the template for I
 8:      Round the coefficients of I into rational numbers
 9:      if I satisfies the boundary and invariant conditions then
10:         Output I and terminate
11:      end if
12:      Refine constraints
13:   end while
14:   d := d + 2
15: end loop



SDP in lemma 8, though due to numerical errors, the algorithm may fail to find
I in practice.
    In practice, Lemma 9 is often used instead of Lemma 8 for efficiency. Step 5
in Algorithm 1 is replaced by: “Let constraints be the relaxation of f to an SOS
problem according to Lemma 9”; this can be translated to an equivalent SDP
problem, which is simpler than the direct translation of Lemma 8, using the
technique of Appendix A.

Example 11. We extend Example 7 using Lemma 9. To illustrate our solution
method, we choose Constraints (4), (5), and (7). The initial condition z = 0 is not
included in these constraints, so (4) needs to be refined to z = 0 ⇒ xy − x2 ≤ I.
    First, we set a template for I. Assume I as a quadratic polynomial with three
variables x, y, z:

   I = c0 + c1 x + c2 y + c3 z + c11 x2 + c12 xy + c13 xz + c22 y 2 + c23 yz + c33 z 2

where c0 , . . . , c33 ∈ R are coefficients that remains to be determined.
   For Constraint (4) with initial constraint z = 0, we get the following corre-
sponding constraint:
                                 I − (xy − x2 ) − v · z ≥ 0                 (4′ )
    For (5), the antecedens is a conjunction of two constraints. As in Example 10,
(5) is split into two constraints and transformed into

                                 z − I + u1 · x ≥ 0      and
                           z − I − u2 · (x − y) ≥ 0                                  (5′ )
   For (7), the constraint 0 < x < y needs to be split into two inequalities
x > 0 ∧ y − x > 0. Similarly to (5), we transform (7) to

 0.5 · I(x + 1, y, z + 1) + 0.5 · I(x − 1, y, z + 1) − I − u3 · x − u4 · (y − x) ≥ 0 (7′ )

In this way the example can be transformed into an SDP problem with con-
straints (4′ ), (5′ ), and (7′ ), and positivity constraints on the multipliers u1 ≥
0, . . . , u4 ≥ 0. (For v, an arbitrary real value is allowed.) Then the resulting SDP
problem can be submitted to any SOS solver.
     The result using solver SeDuMi [31] is shown below.

  I = −7.1097 · 10−10 − 3.8818 · 10−10 x − 0.4939 · 10−10 y + z − x2 + xy+
  2.7965 · 10−10 xz + 0.97208 · 10−10 y 2 + 4.4656 · 10−10 yz − 0.28694 · 10−10 z 2

If we ignore the amounts smaller than the order of magnitude of 10−6 , we get
I = z − x2 + xy. This I satisfies all constraints including (6) and (8), so it is
correct.


4.2   Synthesis Algorithm for Nested Loop Programs

We are now turning to programs containing nested loops. To simplify our dis-
cussion, we assume the program only contains a single, terminating inner loop,
i. e. it can be written as

               P = while(G){body }
                  = while(G){body1 ; while(Ginn ){body inn }; body2 }

where body1 , body inn , and body2 are loop-free program fragments. (If the in-
ner loop is placed within an if statement, one can transform it to the above
form by strengthening G.) For a given preE and postE , we need to verify
whether there exists an invariant I that satisfies Constraint (2) (the bound-
ary and invariant conditions of Theorem 5). We denote the inner loop by Pinn =
while(Ginn ){bodyinn }.
   For such a program, the main difficulty is how to deal with wp(body, I) in
Constraint (2). We propose a method here that takes the inner and outer it-
eration into consideration together and uses the verified pre-expectation of the
inner loop to relax the constraint.
   Fix templates for the polynomial invariants: I for the outer loop and Iinn for
the inner loop Pinn , both with degree d. Since body2 is loop-free, it is easy to
obtain I˜ := wp(body2 , I). We use I˜ as post-expectation postE inn for the inner
loop. Note that (2) for the inner loop requires preE inn ≤ Iinn , so we can use
the template Iinn also as template for preE inn . Then the constraints for loop
invariant I are
                            preE ≤ I
                    I · [1 − χG ] ≤ postE
                          I · χG ≤ wp(body,
                                   f        I) = wp(body1 , preEinn )
                                                                                  (9)
                        preE inn = Iinn
               Iinn · [1 − χGinn ] ≤ postE inn = wp(body2 , I)
                    Iinn · χGinn ≤ wp(body inn , Iinn )
The first three equations are almost Constraint (2) for the outer loop, except
that wpf is the strengthening of the weakest pre-expectation using preE inn =
                                                ˜ The last three equations are
Iinn in the wp-calculation instead of wp(Pinn , I).
Constraint (2) for the inner loop, except that we require equality in preE inn ≤
Iinn .
    Then we have the following lemma.
Lemma 12. An invariant I that satisfies Constraint (9) also satisfies (2), there-
fore it is a loop invariant for program P .
See Appendix C.3 for the proof.

4.3   Handling Numerical Error
In practice, it sometimes happens that numerical errors lead to wrong or trivial
coefficients in the templates. We suggest several methods to refine the constraints
and avoid these errors.
     Due to the inaccuracy of floating-point calculations, it is hard for a software
to check equations and inequalities like x = 0 or x 6= 0. A common trick to
avoid this problem is to turn the equality constraint into x ≥ 0 ∧ x ≤ 0. As
for inequalities, taking x 6= 0 as an example, a way to solve the problem is
adding a new variable y to transform the constraint into xy ≥ 1, since xy ≥ 1
implies x 6= 0 for any value of y. The new constraints are in the form required
by Theorem 4.
     Numerical errors may also lead to an unsound invariant: we may get some
coefficients with a small magnitude, which often result from floating-point inac-
curacies. A common solution for this problem is to ignore those small numbers,
usually smaller than 10−6 in practice. In Example 11, eliminating the terms
with a small order of magnitude was successful, but we cannot be sure whether
the resulting invariant is correct if the remaining coefficients are approximate.
We propose to check the soundness of such solutions symbolically as follows.
Checking whether the generated invariant satisfies Constraint (2) is a special
case of quantifier elimination ∀xn ∈ Rn , f (xn ) ≥ 0. Such problem can be solved
efficiently using an improved Cylindrical Algebraic Decomposition (CAD) algo-
rithm implemented in [17]. In our experiments in Section 5, the found solutions
are obtained by ignoring small numbers, and we verified they are correct by
running CAD in a separate tool.
     If the invariant still violates some of the constraints, we can try to strengthen
the constraint (e. g., change x ≥ 0 to x ≥ 0.1) and repeat our method.
5     Experimental Results
We have implemented a prototype in Python to test our technique. We call the
MATLAB toolbox YALMIP [22] with the SeDuMi solver [31] to solve the SDP
feasibility problem. We use the math software Maple to verify the correctness of
the constraints through CAD. The experiments were done on a computer with
Intel(R) Core(TM) i7-4710HQ CPU and 16 GiB of RAM. The operating system
is Window 7 (32bit). Constraint refinement cannot be handled automatically in
the current version, but we plan to add it together with projection for rounding
solutions in a future version.
    Our prototype and the detailed experimental results can be found at http://iscasmc.ios.ac.cn/ppsdp.
For each probabilistic program, we give the description of the while loop with
pre- and post-expectations in Table 5 and Appendix D. The annotated pre-
expectation serves as an exact estimate of the annotated post-expectation at
the entrance of the loop. We apply the method to several different types of
examples. A summary of the results is shown in Table 1. The first eleven proba-
bilistic programs are benchmarks taken from paper [6], thus we skip the detailed
descriptions of them. We have further constructed three case studies to illustrate
continuous distributions, polynomial probabilistic programs and nested loop pro-
grams. The details of these examples are included in Appendix D. We ran CAD
in Maple manually to verify the feasability of the generated invariants.
    As we can see from Table 5, the running time of our method is within one
second. There are some notes when calculating the examples. We relax the loop
condition z 6= 0 in example geo2 into z ≥ 0.5. Also in the fair coin example, we
relax the loop condition x 6= y into x − y ≥ 0.5 ∨ y − x ≥ 0.5. Since variables in
those two examples are integers, the relaxation is sound.

5.1   Evaluation
Other approaches to compute loop invariants in probabilistic programs are the
Lagrange Interpolation Prototype (LIP) in [6], the tool for martingales (TM)
in [2] and Prinsys in [15]. The tools are executed on the same computer, LIP
and TM under Linux and the other two under Windows. In Table 2, we compare
the features supported by the four tools.
    We have tested the examples in Table 1 on these four tools. Prinsys takes
the longest time and fails to verify any of non-linear examples presented. LIP
fails to verify any examples that include a continuous variable or have a degree
larger than 3; additionally it is always about 10 times slower than our tool. TM
fails to verify examples ruin, bin3 and geo directly. We observe that it cannot
treats constraints of the form x = y or x 6= y (where x and y might be variables
or constants). However, by transforming x = y into x ≥ y ∧ y ≥ x, TM can
synthesize a supermartingale for the program. Also, it cannot verify the simple
perceptron, as it is a non-linear program. Furthermore, TM cannot deal with
nested loop programs.
    We now consider the parametric linear program in Section D.3. Table 3 gives
a comparison of time consumption of the main technical step in our prototype.
The number of constraints grows with the number of variables in our approach,
similarly with the running time. Some more experiments on the number of vari-
ables and maximum degree of polynomials are included in Appendix D.3.


6   Conclusion

In this paper, we propose a method to synthesize polynomial quantitative in-
variants for recursive probabilistic programs by semialgebraic programming via
a Positivstellensatz. First, a polynomial template is fixed whose coefficients re-
main to be determined. The loop and its pre- and post-expectation can be trans-
formed into a semialgebraic set, of which the emptiness can be decided by finding
a counterexample satisfying the condition of the Positivstellensatz. Semidefinite
programming provides an efficient way to synthesize such a counterexample. The
method can be applied to polynomial programs containing continuous or discrete
variables, including those with nested loops. When numerical errors prevent find-
ing a loop invariant polynomial right away, we currently can correct them ad hoc
(by deleting terms with very small coefficients and sometimes strengthening the
constraints), but we would like to develop a more systematic treatment.
    As future improvements, we are considering improvements in numerical error
handling. A better approximation can be found by projecting I(x)  ˜    onto a ra-
tional subspace defined by SDP constraints [27,19]. There are also acceleration
methods for different types of probabilistic programs: For linear programs, Han-
delman’s Positivstellensatz describes a faster way to synthesize SOS constraints,
and for Archimedean programs, [10] describes a faster way to apply Stengle’s
Positivstellensatz.


References
 1. Barthe, G., Espitau, T., Ferrer Fioriti, L. M., Hsu, J.: Synthesizing probabilistic
    invariants via Doob’s decomposition. arXiv preprint 1605.02765 (2016)
 2. Chakarov, A., Sankaranarayanan, S.: Probabilistic program analysis with martin-
    gales. In: Sharygina, N., Veith, H. (eds.) Computer aided verification: CAV. LNCS,
    vol. 8044, pp. 511–526. Springer, Heidelberg (2013)
 3. Chakarov, A., Sankaranarayanan, S.: Expectation invariants for probabilistic pro-
    gram loops as fixed points. In: Müller-Olm, M., Seidl, H. (eds.) Static analysis:
    SAS. LNCS, vol. 8723, pp. 85–100. Springer, Cham (2014)
 4. Chatterjee, K., Fu, H., Goharshady, A. K.: Termination analysis of probabilistic
    programs through Positivstellensatz’s. In: Chaudhuri, S., Farzan, A. (eds.) Com-
    puter aided verification: CAV. LNCS, vol. 9779, pp. 3–22. Springer, Cham (2016)
 5. Chatterjee, K., Fu, H., Novotný, P., Hasheminezhad, R.: Algorithmic analysis of
    qualitative and quantitative termination problems for affine probabilistic programs.
    In: Bodik, R., Majumdar, R. (eds.) POPL’16. pp. 327–342. ACM, New York (2016)
 6. Chen, Y.-F., Hong, C.-D., Wang, B.-Y., Zhang, L.: Counterexample-guided poly-
    nomial loop invariant generation by Lagrange interpolation. In: Kroening, D.,
    Păsăreanu, C. S. (eds.) Computer aided verification: CAV. LNCS, vol. 9206, pp.
    658–674. Springer, Cham (2015)
 7. Choi, M.-D., Lam, T. Y., Reznick, B.: Sums of squares of real polynomials. In:
    Jacob, B., Rosenberg, A. (eds.) K-Theory and Algebraic Geometry: Connections
    with Quadratic Forms and Division Algebras. Proceedings of Symposia in Pure
    Mathematics, vol. 58, Part 2, pp. 103–126. American Mathematical Society, Prov-
    idence, R. I. (1995)
 8. Civil Aviation Administration of China (CAAC): Statistical com-
    muniqué on the development of aviation in 2015 [in Chinese].
    http://www.caac.gov.cn/XXGK/XXGK/TJSJ/201605/P020160531575434538041.pdf
    (2016)
 9. Colón, M. A., Sankaranarayanan, S., Sipma, H. B.: Linear invariant generation us-
    ing non-linear constraint solving. In: Hunt, Jr., W. A., Somenzi, F. (eds.) Computer
    aided verification: CAV. LNCS, vol. 2725, pp. 420–432. Springer, Berlin (2003)
10. Dai, L., Xia, B., Zhan, N.: Generating non-linear interpolants by semidefinite pro-
    gramming. In: Sharygina, N., Veith, H. (eds.) Computer Aided Verification: CAV.
    LNCS, vol. 8044, pp. 364–380. Springer, Berlin (2013)
11. Dijkstra, E.: A Discipline of Programming, vol. 4. Prentice-Hall, Englewood Cliffs
    (1976)
12. Feller, W.: An introduction to probability theory and its applications: volume I,
    vol. 1. Wiley (1968)
13. Ferrer Fioriti, L. M., Hermanns, H.: Probabilistic termination: Soundness, com-
    pleteness, and compositionality. In: POPL’15: principles of programming lan-
    guages. pp. 489–501. ACM, New York (2015)
14. Gordon, A. D., Henzinger, T. A., Nori, A. V., Rajamani, S. K.: Probabilistic pro-
    gramming. In: Dwyer, M. B., Herbsleb, J. (eds.) Future of Software Engineering
    (FOSE 2014). pp. 167–181. ACM, New York (2014)
15. Gretz, F., Katoen, J.-P., McIver, A.: Prinsys: on a quest for probabilistic loop
    invariants. In: Joshi, K., Siegle, M., Stoelinga, M., D’Argenio, P. R. (eds.) Quan-
    titative Evaluation of Systems: QEST. LNCS, vol. 8054, pp. 193–208. Springer,
    Berlin (2013)
16. Gretz, F., Katoen, J.-P., McIver, A.: Operational versus weakest pre-expectation
    semantics for the probabilistic guarded command language. Perf. Eval. 73, 110–132
    (2014)
17. Han, J., Jin, Z., Xia, B.: Proving inequalities and solving global optimization prob-
    lems via simplified cad projection. J. Symb. Comput. 72, 206–230 (2016)
18. Hoare, C. A. R.: An axiomatic basis for computer programming. Commun. ACM
    12(10), 576–580 (1969)
19. Kaltofen, E. L., Li, B., Yang, Z., Zhi, L.: Exact certification in global polynomial
    optimization via sums-of-squares of rational functions with rational coefficients.
    Journal of Symbolic Computation 47(1), 1–15 (2012)
20. Kaminski, B. L., Katoen, J.-P.: On the hardness of almost-sure termination. In:
    Italiano, G. F., Pighizzini, G., Sannella, D. T. (eds.) Mathematical foundations of
    computer science 2015: MFCS. LNCS, vol. 9234, pp. 307–318. Springer, Heidelberg
    (2015)
21. Katoen, J.-P., McIver, A. K., Meinicke, L. A., Morgan, C. C.: Linear-invariant
    generation for probabilistic programs. In: Cousot, R., Martel, M. (eds.) Static
    analysis: SAS. LNCS, vol. 6337, pp. 390–406. Springer, Berlin (2010)
22. Löfberg, J.: YALMIP: A toolbox for modeling and optimization in MATLAB. In:
    2004 IEEE International symposium on computer aided control systems design
    [CACSD]. pp. 284–289. IEEE, Piscataway, NJ (2004)
23. McIver, A., Morgan, C. C.: Abstraction, Refinement and Proof for Probabilistic
    Systems. Springer, New York (2005)
24. Meyer, C. D.: Matrix Analysis and Applied Linear Algebra. SIAM, Philadelphia
    (2000)
25. Morgan, C., McIver, A., Seidel, K.: Probabilistic predicate transformers. ACM
    Trans. Progr. Lang. Syst. 18(3), 325–353 (1996)
26. Parrilo, P. A.: Semidefinite programming relaxations for semialgebraic problems.
    Math. Program., Ser. B 96(2), 293–320 (2003)
27. Peyrl, H., Parrilo, P. A.: Computing sum of squares decompositions with rational
    coefficients. Theoretical Computer Science 409(2), 269–281 (2008)
28. Putinar, M.: Positive polynomials on compact semi-algebraic sets. Indiana Univ.
    Math. J. 42(3), 969–984 (1993)
29. Rodrı́guez-Carbonell, E., Kapur, D.: Generating all polynomial invariants in simple
    loops. J. Symb. Comput. 42(4), 443–476 (2007)
30. Stengle, G.: A nullstellensatz and a positivstellensatz in semialgebraic geometry.
    Math. Ann. 207(2), 87–97 (1974)
31. Sturm, J. F.: Using SeDuMi 1.02, a MATLAB toolbox for optimization over sym-
    metric cones. Optimization Methods and Software 11(1–4), 625–653 (1999)
32. Toh, K. C., Todd, M. J., Tütüncü, R. H.: SDPT3, a MATLAB software package
    for semidefinite programming, version 1.3. Optimization Methods and Software
    11(1–4), 545–581 (1999)
Table 1. The column “Name” shows the name of each experiment. The annotated pre-
and post-expectations are shown in the columns “preE ” and “postE ”. The inferred
quantitative loop invariant for each example is given in the column “Invariant”. The
column “Time” gives the running time needed of our tool: the first one is the total
running time, and the second one is the time used in the SeDuMi solver.

Name         preE             postE                    Invariant                 Time (s)
ruin         xy − x2            z      z + xy − x2                                0.4/0.3
bin1         x + 41 ny          x      x + 14 ny                                  0.4/0.2
             1 2
               n − 81 n +
bin2         8
             3                  x      x + 18 n2 − 18 n + 43 ny                  0.7/0.3
             4
               ny
                                                                  2
             1 2                         x − 0.0057n − 0.0014x + 0.1763xn +
               n − 81 n   +
bin3         8                  x        712.909n2 + 0.0014x2 n + 0.4114xn2 +    0.7/0.3
             3
               ny 2
             4                           0.4188ny 2 − 0.0178n3
geo          x + 3zy               x     x + 3zy                                 0.2/0.2
                                         x + 30.2312y + 3.4699z − 12.6648y 2 −
geo2         x + 15                x                                             0.2/0.1
                  2                      44.6591yz − 35.5112z 2 − 22.8807
             1 2
sum          4
               n + 4n 1
                                   x     x + 41 n2 + 14 n                        0.3/0.1
             1 2
prod         4
               n − 4n 1
                                  xy     − 41 n + xy + 21 xn + 12 yn + 41 n2     0.3/0.1
                                         0.7130−0.5622x+0.3364y+0.8564n−
fair coin1   1
             2
               −  1
                  2
                    x         1 − x + xy 1.2740x2 + 07610xy − 1.4572xn −         0.2/0.1
                                         1.2208y 2 + 1.4572yn − 0.1366n2
                                         1.1941+1.6157x+0.6387y+7.9774n−
fair coin2   1
             2
               − 21 y           x + xy 14.6705x2 + 9.7904xy − 14.9948xn −        0.3/0.1
                                         14.6457y 2 + 14.9948yn − 1.4058n2
                                         6.0556 + 2.5964x + 3.2468y +
             8
               − 8
                   x −  8
                          y +            39.2052n   − 69.9038x2 + 44.0224xy −
fair coin3   3   3      3         n                                              0.2/0.1
             1
             3
               n                         72.1408xn − 69.8067y 2 + 72.1408yn −
                                         6.7632n2
simple
perceptron −2b                  n      n − 2b                                    0.3/0.1
airplane
delay      106.548x             h      106.548x − 106.548n + h                   0.4/0.2
airplane
delay2     282.507x             h      282.507(x − n) + h                        0.5/0.2
nested
           20(m − x)            k      k + 20(m − x)                             1.6/1.1
loop



             Table 2. Comparison of the features supported by 4 tools

                              Prinsys    LIP       TM       Our tool
        Type of Program        Linear   Cubic     Linear Polynomial
        Type of Invariant      Linear Polynomial Linear Polynomial
        Computation Method Symbolic Symbolic Numerical Numerical
        Distribution of Vari-
                              Discrete Discrete Continuous Continuous
        able
Table 3. Comparison of running time (in seconds) of the parameterized linear example

    Number of variables     n = 15   n = 20   n = 25   n = 30   n = 35   n = 40
    Solver time of our tool 0.41      1.30     2.44     8.30     20.56    46.62
The following appendices are added for the convenience of the reviewers. They
will become part of a technical report accompanying our publication, once ac-
cepted. We appreciate the reviewers’ consideration.—The authors.

A    Sum-of-Squares Problems
 The set of sum-of-squares polynomials is a proper subset of the nonnegative
 polynomials with good algebraic properties, allowing efficient calculations. The
 “Gram matrix” method [7] is a way to decompose a polynomial into a sum of
 squares using semidefinite programming.
                                P                 ≤d
    Consider a polynomial f = |α|≤d cα Xα  n ∈ R     [Xn ] with degree at most d.
fPis a sum of squares if and only if it has a representation f = Xn AXTn =
               α β
   α,β∈∆ aαβ Xn Xn , where the |∆| × |∆| matrix A = (aαβ )α,β∈∆ is positive
semidefinite. So checking whether f is a sum of squares is equivalent to solv-
ing the following constraint problem:
                 
                  c0 = aP 00 ,
                    cγ = α+β=γ aαβ for γ 6= 0                                 (10)
                 
                    and A = (aαβ )α,β∈∆ is positive semidefinite
The above problem can be solved using a semidefinite program; we refer to
Appendix B for details. Semidefinite programs can be efficiently solved both in
theory and in practice and have seen active research in recent years. Some of the
tools being used are SeDuMi [31] and SDPT3 [32].


B    Semidefinite Programming
A semidefinite program can be seen as a generalization of a linear program where
the constraints are described by a cone of positive semidefinite matrices.
    We use S n to denote all real n × n symmetric matrices. Then for a matrix
A ∈ S n , A is positive semidefinite if all eigenvalues of A are ≥ 0 (one can find
more about positive semidefinite matrix in any book about linear algebra such
as [24]). For matrices A and B in S n , we write A  B if and only if A − B is
positive semidefinite.
    We use h · , · i to denote the scalar product of two matrices or vectors, i. e.
for A = (aij ), B = (bij ) ∈ S n and x, y ∈ Rn
                                                    n
                                                    X
                        hA, Bi := T r(AT B) =             aij bij
                                                  i,j=1

                                   hx, yi := xT y
A semidefinite program is defined as follows:
                     minimize hC, Xi
                     subject to hAi , Xi = bi for i = 1, . . . , k            (11)
                                X0
where X ∈ S n is the decision variable, bi ∈ R and C, Ai ∈ S n are given
symmetric matrices.
    Sum-of-squares problem (10) can be transformed into an SDP problem as
follows. Let X = (aαβ )α,β∈∆ , Ai (for i ∈ ∆) be the symmetric matrix whose
(α, β) entry is 1 if α + β = i and 0 otherwise, and let bi = ci . In this way, (10)
is transformed into the form (11) without objective.


C     Proofs of Lemmas
C.1    Proof of Lemma 8
Lemma 8 ([26,10]). The emptiness of (1) is equivalent to the feasibility of an
SDP problem.
Proof. We use the notations from Theorem 4 in this proof. The emptiness of
(1) is equivalent to the existence of a solution for equation f + g 2 + h = 0 with
f ∈ P , g ∈ M , h ∈ I due to Theorem 4.
    Note that f , g and h can be represented as
         P
 – f = α∈{0,1}s uα F α , where uα is a sum of squares for all α ∈ {0, 1}s and
    F = {f1 , . . . , fs }, and
 – g = G α with G = {g1 , . . . , gt }, and
 – h = v1 h1 + v2 h2 + · · · + vw hw , where v1 , . . . , vw ∈ R[Xn ].
Fix a maximal degree d. Then we only consider F α and G α with |α| ≤ d. We
set templates with degree d for uα and v0 , . . . , vw and treat their coefficients
as parameters. Every polynomial vi can be presented as the difference of two
                                2          2                     Pl
SOS polynomials: vi = (vi +1) −(v 4
                                     i −1)
                                             . Then f + g 2 + h = i=1 δi pi , where l is
some integer, pi is one of fi , gi , hi , or −hi , and δi is a SOS. Then the equation
f + g 2 + h = 0 can be transformed into a set of equations by merging coefficients
of each Xα n with maximal degree 2d. One can formulate additional constraints
that δα needs to be a SOS and the coefficient matrix Aα with δα = Xn Aα XTn to
be positive semidefinite. The equation set with constraints can be transformed
into an SDP problem of the form in Appendix B.

C.2    Proof of Lemma 9
Proof. We only prove (1) and (2) here, (3) is a straightforward extension of them
by analogy.
    For (1), assume h(Xn ) = g(Xn ) − u · f (Xn ) is an SOS for some u ∈ R≥0 and
f (Xn ) ≥ 0. Since h(Xn ) ≥ 0, g(Xn ) = h(Xn ) + u · f (Xn ) ≥ 0.
    For (2), assume h(Xn ) = g(Xn ) − v · f (Xn ) is an SOS for arbitrary v ∈ R
and f (Xn ) = 0. Then g(Xn ) = h(Xn ) + v · f (Xn ) = h(Xn ) ≥ 0.
By the method indicated above Lemma 9, one can easily find that a constraint
of the form f1 (Xn ) ≥ 0 ∨ f2 (Xn ) ≥ 0 ⇒ g(Xn ) ≥ 0 can be translated to two
SOS problems.
C.3    Proof of Lemma 12

Lemma 12. An invariant I that satisfies Constraint (9) also satisfies (2),
therefore it is a loop invariant for program P .

Proof. The first two inequalities of (2) are literally the same as the first two of
(9). To prove the remaining inequality of (2), we assume that the inner loop
terminates. (The verification of soundness is not a part of our algorithm.) From
Theorem 5 applied to the last three (in)equalities in (9), we immediately get
that preE inn ≤ wp(Pinn , postE inn ). From this we have:

    I · χG ≤ wp(body
             f       , I) = wp(body1 , preE inn )
                          ≤ wp(body1 , wp(Pinn , postE inn ))
                          ≤ wp(body1 , wp(Pinn , wp(body2 , I)))
                          = wp(body1 ; Pinn ; body2 , I)         = wp(body , I).


D     Experiment Details

D.1    Non-linear Probabilistic Programs

We use a non-linear probabilistic program to model a simple perceptron, which
is an algorithm for supervised learning of binary classifiers in machine learning.
It gives a linear classifier function to decide whether an input belongs to one
class or another based on a set of given data. Assume the training data is the
collection of pairs (xi , yi )i∈I , where yi is the desired output value of xi . We have
to learn the linear function f (x) that maps the data to a single binary value:
                                        
                                            1 if w · xi + b > 0
                            f (xi ) =
                                            0 otherwise

When the outcome does not match yi , the random perceptron updates its clas-
sifier by w ← w + xi yi [η] w and b ← b + yi [η] b where η is a learning rate. When
the input of the perceptron is one data pair (x, y), the algorithm to generate a
simple perceptron can be described as:

                  real x, y;
                  real w, b;
                  int n := 0;
                  while(y (w · x + b) ≤ 0){
                    w := w + y · x, b := b + y [η] skip; n := n + 1
                  }

   In our trial, we further set (x, y) = (1, 1), η = 0.25 and initialize w = 0 and
b < 0. The expected time before the function can correctly classify the input is
E(n) = −2b, as the method shows.
D.2    Probabilistic Program with Real Variables

The figures in this example are based on aviation statistics in 2015, collected by
the Civil Aviation Administration of China [8]. 68.3 % of the scheduled flights
are actually flown. An airplane takes 2 h 15 min from Beijing to Shanghai. The
average delay is 21 min and can be approximated by a normal distribution. As-
sume an airliner is scheduled for this flight x times, then the total flight time (in
minutes) can be calculated by the program:

           h := 0;
           n := 0;
           while(n ≤ x){
              h := h + 135 + NormDist(21, σ) [0.683] skip; n := n + 1
           }

where NormDist(µ, σ) is a normal distribution with average of µ and standard
deviation of σ. (For expectations, the value of σ is of no importance.) Since the
sum of normal distributions is also a normal distribution, we can calculate that
E(h) = 106.548x, which can be proved by our prototype, with the synthesized
invariant loop 106.548x − 106.548n + h.
    Further, we consider a slightly more involved version. A direct flight from
Beijing to Hongkong takes 220 min with an average delay of 40 min. An alterna-
tive two-leg route starts from Beijing, stops in Shanghai, and ends in Hongkong.
The first leg takes 135 min, with an average delay of 21 min. The second leg takes
another 135 min, with an average delay of 40 min. A passenger takes x flights
from Beijing to Hongkong; if the direct flight is cancelled, s/he stops in Shang-
hai. (We assume that at most one of the two routes is cancelled for simplicity.)
The total travel time can be calculated by the program:

           h := 0;
           n := 0;
           while(n ≤ x){
              h := h + 220 + NormDist(40, σ) [0.683] h := h + 270 +
                    NormDist(21, σ) + NormDist(40, σ);
              n := n + 1
           }

   We can see E(h) = 282.507x, which can be verified by our method, with the
synthesized loop invariant 282.507(x − n) + h.


D.3    Parametric Example

In this section we consider some parametric examples such that we can observe
how our approach scales with the number of variables and the degree of the
templates.
Parametric Linear Program. We first consider a linear program with pa-
rameter n ∈ N. The program scheme is

     h := 0;
     while(t > 0){
        h := h + x1 + · · · + xn [0.5] h := h + x1 + · · · + xn + UnifDist(0, 2n)
        t := t − 1
     }

The post-expectation of the program is h and the related pre-expectation is
( n2 + x1 + · · · + xn )t.
     If the degree of the invariant template is chosen to be 2, one gets as the
synthesized invariant of this parameterized program h + ( n2 + x1 + · · · + xn )t. In
Table 4, we observe that the number of coefficients remaining to be determined
by the SDP tool is quadratic to the number of variables. Moreover, curve fitting
shows the running time is approximately cubic in the number of variables.


Table 4. Running time with degree 2 for the parametric linear program. The row
“Number of coefficients” shows the numbers of coefficients in the invariant template
remaining to be determined. The row “solvertime” describes the time SDP solver takes
to solve the constraint solving problem.

   Number of variables        n = 15   n = 20    n = 25   n = 30    n = 35    n = 40
   Number of coefficients      136       231      351      496       741       946
   Solvertime                 0.41 s    1.30 s   2.44 s    8.30 s   20.56 s   46.62 s
   Total time                 1.11 s    2.26 s   4.14 s   12.58 s   22.53 s   78.40 s




Quadratic Program. We consider the quadratic program obtained from the
above program by replacing x1 by x21 . We need a template of degree 4. In Table 5
we observe that the number of coefficients is cubic in the number of variables.
Runtime grows rapidly when variables are being added. Additionally, when we
look at the case with n = 30 in Table 4 and n = 8 in Table 5, we see that
for a similar number of variables the latter solvertime is still 50 % higher; so
the increase in running time is not only due to the number of coefficients in the
invariant template. One reason is that the constraint matrix in the SDP problem
becomes much coarser, which makes it more difficult to solve the problem.


Polynomial Program. Our next trial is to consider the following parameter-
ized version of Example 7.


hxy n − x2 i z := 0; while(0 < x < y n ){x := x + 1 [0.5] x := x − 1; z := z + 1; } hxi
   Table 5. Running time for the parametric polynomial program with degree 4

       Number of variables       n=5      n=6      n=7    n=8     n=9       n = 10
       Number of coefficients     126      210      330    495     715      1001
       Solvertime                0.96 s   1.59 s   4.29 s 12.66 s 29.42 s   96.24 s
       Total time                1.43 s   4.57 s   5.27 s 14.98 s 36.04 s 107.30 s

           Table 6. Running time for parameterized version of Example 7

      Parameter                 n=6       n=7      n=8    n=9     n = 10    n = 11
      Number of coefficients     455      680      969     1330    1771      2300
      Solvertime                19.83 s 64.63 s 182.69 s 470.43 s 1099.2 s 2223.5 s
      Total time                23.19 s 75.02 s 213.90 s 498.52 s 1153.1 s 2431.6 s



with n ∈ N as a parameter. The relevant invariant template has degree 2n.
Table 6 shows the running times dependent on n.
    The number of coefficients grows almost cubic in n, but the running time
grows much faster than in Table 5, which indicates that degree is the major
influence on running time of our method.
    As a conclusion, the main influence on the running time of our method is the
degree of the invariant template. The number of coefficients also has an influence.

D.4    Nested Loop program
We copy an example from [5] for analysis of almost-sure termination. Here we
try to generate a loop invariant for the program.

                          real x, y;
                          int k = 0;
                          while(x ≤ m){
                            y = 0;
                            while(y ≤ n){
                               y = y + UnifDist(−0.1, 0.2)
                            }
                            x = x + UnifDist(−0.1, 0.2);
                            k =k+1
                          }

   Let postE = k, for preE = 20(m − x), we can synthesize an invariant I =
k + 20(m − x) as the method shows.
