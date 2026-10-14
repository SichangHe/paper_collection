                                         Property-based Polynomial Invariant Generation
                                              using Sums-of-Squares Optimization

                                                Assalé Adjé1,a and Pierre-Loïc Garoche1,a and Victor Magron2,b
                                                             1
                                                              Onera, the French Aerospace Lab, France.
                                                          Université de Toulouse, F-31400 Toulouse, France.
arXiv:1503.07025v1 [cs.LO] 24 Mar 2015




                                                                   firstname.lastname@onera.fr
                                         2
                                           Circuits and Systems Group, Department of Electrical and Electronic Engineering,
                                            Imperial College London, South Kensington Campus, London SW7 2AZ, UK.
                                                                      v.magron@imperial.ac.uk



                                               Abstract. While abstract interpretation is not theoretically restricted
                                               to specific kinds of properties, it is, in practice, mainly developed to
                                               compute linear over-approximations of reachable sets, aka. the collecting
                                               semantics of the program. The verification of user-provided properties is
                                               not easily compatible with the usual forward fixpoint computation using
                                               numerical abstract domains.
                                               We propose here to rely on sums-of-squares programming to characterize
                                               a property-driven polynomial invariant. This invariant generation can be
                                               guided by either boundedness, or in contrary, a given zone of the state
                                               space to avoid.
                                               While the target property is not necessarily inductive with respect to
                                               the program semantics, our method identifies a stronger inductive poly-
                                               nomial invariant using numerical optimization. Our method applies to a
                                               wide set of programs: a main while loop composed of a disjunction (if-
                                               then-else) of polynomial updates e.g. piecewise polynomial controllers.
                                               It has been evaluated on various programs.


                                         1   Introduction
                                         With the increased need for confidence in software, it becomes more than ever im-
                                         portant to provide means to support the verification of specification of software.
                                         Among the various formal verification methods to support these analysis, a first
                                         line of approaches, such as deductive methods or SMT-based model checking,
                                         provide rich languages to support the expression of the specification and then try
                                         to discharge the associate proof obligation using automatic solvers. The current
                                         state of the art of these solvers is able to manipulate satisfiability problems over
                                         linear arithmetics or restricted fragments of non linear arithmetics. Another line
                                         of approaches, such as static analysis also known as abstract interpretation, re-
                                         stricts, a priori, the kind of properties considered during the computation: these
                                         a
                                           The author is supported by the RTRA /STAE Project BRIEFCASE and the ANR
                                           ASTRID VORACE Project.
                                         b
                                           The author is supported by EPSRC (EP/I020457/1) Challenging Engineering Grant.
methods typically perform interval arithmetic analysis or rely on convex poly-
hedra computations. In practice this second line of work seems more capable of
manipulating and generating numerical invariants through the computation of
inductive invariants, while the first line of approaches hardly synthesize these
required invariants through satisfiability checks.
    However, when it comes to more than linear properties, the state of the art
is not well developed. In the early 2000s, ellipsoid analyses [Fer04], similar to
restricted cases of Lyapunov functions, were designed to support the study of a
family of Airbus controllers. This exciting result was used to provide the analysis
of absence of runtime errors but could hardly be adapted to handle more general
user provided specifications for polynomial programs.
    However proving polynomial inequalities is NP-hard and boils down to show
that the infimum of a given polynomial is nonnegative. Still, one can obtain lower
bounds of such infima by decomposing certain nonnegative polynomials into
sums-of-squares (SOS). This actually leads to solve hierarchies of semidefinite
relaxations, introduced by Lasserre in [Las01]. Recent advances in semidefinite
programming allowed to extensively apply these relaxations to various fields,
including parametric polynomial optimization, optimal control, combinatorial
optimization, etc. (see e.g. [Par03,Lau09] for more details).
    While these approaches were mentioned a decade ago in [Cou05] and mainly
applied to termination analysis, they hardly made their way through the software
verification community to address more general properties.


Contributions. Our contribution allows to analyze high level properties defined
as a sublevel set of polynomials functions, i.e. basic semialgebraic sets. This
class of properties is rather large: it ranges from boundedness properties to the
definition of a bad region of the state space to avoid. While these properties,
when they hold, are meant to be invariant, i.e. they hold in each reachable state,
they are not necessarily inductive. Our approach rely on the computation of
a stronger inductive property using SOS programming. This stronger property
is proved inductive on the complete system and, by construction, implies the
target property specified by the user. We develop our analysis on discrete-time
piecewise polynomial systems, capturing a wide class of critical programs, as
typically found in current embedded systems such as aircrafts.


Organization of the paper. The paper is organized as follows. In Section 2, we
present the programs that we want to analyze and their representation as piece-
wise polynomial discrete-time systems. Next, we recall in Section 3 the collect-
ing semantics that we use and introduce the polynomial optimization problem
providing inductive invariants based on target polynomial properties. Section 4
contains the main contribution of the paper, namely how to compute effectively
such invariants with SOS programming. Practical computation examples are
provided in Section 5. Finally, we explain in Section 6 how to derive template
bases from generated invariants.
2    Polynomial programs and piecewise polynomial
     discrete-time systems

In this section, we describe the programs which are considered in this paper
and we explain how to analyze them through their representation as piecewise
polynomial discrete-time dynamical systems.
    We focus on programs composed of a single loop with a possibly complicated
switch-case type loop body. Moreover we suppose without loss of generality that
the analyzed programs are written in Static Single Assignment (SSA) form, that
is each variable is initialized at most once.

Definitions. We recall that a function f from Rd to R is a polynomial if and only
if there exists k ∈ N, a family {cα | P  α = (α1 , . . . , αd ) ∈ Nd , |α| = α1 + . . . + αd ≤
                                                                   αd
k} such that for all x ∈ R , f (x) = |α|≤k cα xα
                             d
                                                          1 . . . xd . By extension a function
                                                           1


f : Rd 7→ Rd is a polynomial if and only if all its coordinate functions are
polynomials. Let R[x] stands for the set of d-variate polynomials.
    In this paper, we consider assignments of variables using only parallel polyno-
mial assignments (x1 , . . . , xd ) = T (x1 , . . . , xd ) where (x1 , . . . , xd ) is the vector of
the program variables. Tests are either weak polynomial inequalities r(x1 , . . . , xd ) ≤
0 or strict polynomial inequalities r(x1 , . . . , xd ) < 0. We assume that assignments
are polynomials from Rd to Rd and test functions are polynomials from Rd to
R. In the program syntax, the notation  will be either <= or <. The form of
the analyzed program is described in Figure 1.


          x ∈ X in ;
          w h i l e ( r10 ( x ) 0 and . . . and rn0 0 ( x )  0 ) {
             c a s e ( r11 ( x ) 0 and . . . and rn1 1 ( x )  0 ) : x = T 1 ( x ) ;
             case . . .
             c a s e ( ri1 ( x ) 0 and . . . and rn1 i ( x )  0 ) : x = T i ( x ) ;
          }


              Fig. 1. One-loop programs with nested conditional branches



    A set C ⊆ Rd is said to be a basic semialgebraic set if there exist g1 , . . . , gm ∈
R[x] such that C = {x ∈ Rd | gj (x)  0, ∀ j = 1, . . . , m}, where  is used to
encode either a strict or a weak inequality.
    As depicted in Figure 1, an update T i : Rd → Rd of the i-th condition branch
is executed if and only if the conjunction of tests rji (x)  0 holds. In other words,
the variable x is updated by T i (x) if the current value of x belongs to the basic
semialgebraic set

                     X i := {x ∈ Rd | ∀j = 1, . . . , ni , rji (x)  0} .                    (1)
Piecewise Polynomial Systems. Consequently, we interpret programs as con-
strained piecewise polynomial discrete-time dynamical systems (PPS for short).
The term piecewise means that there exists a partition {X i , i ∈ I} of Rd such
that for all i ∈ I, the dynamics of the system is represented by the following
relation, for k ∈ N:
                           if xk ∈ X i ∩ X 0 , xk+1 = T i (xk ) .                         (2)
    We assume that I is finite and that the initial condition x0 belongs to some
compact basic semialgebraic set X in . For the program, X in is the set where
the variables are supposed to be initialized in. Since the test entry for the loop
condition can be nontrivial, we add the term constrained and X 0 denotes the
set representing the conjunctions of tests for the loop condition. The iterates of
the PPS are constrained to live in X 0 : if for some step k ∈ N, xk ∈ / X 0 then the
PPS is stopped at this iterate with the terminal value xk .
    We define a partition as a family of nonempty sets such that:
                   [
                      X i = Rd , ∀ i, j ∈ I, i 6= j, X i ∩ X j 6= ∅ .            (3)
                     i∈I

From Equation (3), for all k ∈ N∗ there exists a unique i ∈ I such that xk ∈ X i .
A set X i can contain both strict and weak polynomial inequalities and character-
izes the set of the ni conjunctions of tests polynomials rji . Let ri = (r1i , . . . , rni i )
stands for the vector of tests functions associated to the set X i . We suppose that
the basic semialgebraic sets X in and X 0 also admits the representation given by
Equation (1) and we denote by r0 the vector of tests polynomials (r10 , . . . , rn0 0 )
and by rin the vector of test polynomials (r1in , . . . , rninin ). To sum up, we give a
formal definition of PPS.
Definition 1 (PPS). A constrained polynomial piecewise discrete-time dynam-
ical system (PPS) is the quadruple (X in , X 0 , X , L) with:
 – X in ⊆ Rd is the compact basic semialgebraic set of the possible initial con-
   ditions;
 – X 0 ⊆ Rd is the basic semialgebraic set where the state variable lives;
 – X := {X i , i ∈ I} is a partition as defined in Equation (3);
 – L := {T i , i ∈ I} is the family of the polynomials from Rd to Rd , w.r.t. the
   partition X satisfying Equation (2).
    From now on, we associate a PPS representation to each program of the form
described at Figure 1. Since a program admits several PPS representations, we
choose one of them, but this arbitrary choice does not change the results provided
in this paper. In the sequel, we will often refer to the running example described
in Example 1.
Example 1 (Running example). The program below involves four variables and
contains an infinite loop with a conditional branch in the loop body. The update
of each branch is polynomial. The parameters cij (resp. dij ) are given parameters.
During the analysis, we only keep the variables x1 and x2 since oldx1 and oldx2
are just memories.
                x1 , x2 ∈ [a1 , a2 ] × [b1 , b2 ] ;
                oldx1 = x1 ;
                oldx2 = x2 ;
                w h i l e (−1 <= 0 ) {
                    oldx1 = x1 ;
                    oldx2 = x2 ;
                    c a s e : oldx1 ^2 + oldx2 ^2 <= 1 :
                           x1 = c11 ∗ oldx1 ^2 + c11 ∗ oldx2 ^ 3 ;
                           x2 = c21 ∗ oldx1 ^3 + c22 ∗ oldx2 ^ 2 ;
                    c a s e : −oldx1 ^2 − oldx2 ^2 < −1
                           x1 = d11 ∗ oldx1 ^3 + d12 ∗ oldx2 ^ 2 ;
                           x2 = d21 ∗ oldx1 ^2 + d22 ∗ oldx2 ^ 2 ;
                    }
                }
The associated PPS corresponds to the quadruple (X in , X 0 , {X 1 , X 2 }, {T 1 , T 2 }),
where the set of initial conditions is:
                               X in = [a1 , a2 ] × [b1 , b2 ] ,
the system is not globally constrained, i.e. the set X 0 in which the variable
x = (x1 , x2 ) lies is:
                                  X 0 = Rd ,
the partition verifying Equation (3) is:
       X 1 = {x ∈ R2 | x21 + x22 ≤ 1},        X 2 = {x ∈ R2 | −x21 − x22 < −1} ,
and the polynomials relative to the partition {X 1 , X 2 } are:
                     c11 x21 + c12 x32                   d11 x31 + d12 x22
                                                                        
         T 1 (x) =                       and T 2
                                                 (x) =                       .
                     c21 x31 + c22 x22                   d21 x21 + d22 x22

3    Program invariants as sublevel sets
The main goal of the paper is to decide automatically if a given property holds
for the analyzed program, i.e. for all its reachable states. We are interested in
numerical properties and more precisely in properties on the values taken by the
d-uplet of the variables of the program. Hence, in our point-of-view, a property
is just the membership of some set P ⊆ Rd . In particular, we study properties
which are valid after an arbitrary number of loop iterates. Such properties are
called loop invariants of the program. Formally, we use the PPS representation
of a given program and we say that P is a loop invariant of this program if:
                                   ∀ k ∈ N, xk ∈ P ,
where xk is defined at Equation (2) as the state variable at step k ∈ N of the PPS
representation of the program. Our approach addresses any property expressible
as a polynomial level set property. This section defines formally these notions
and develop our approach: synthesize a property-driven inductive invariant.
3.1   Collecting Semantics as postfixpoint characterization
Now, let us consider a program of the form described in Figure 1 and let us
denote by S the PPS representation of this program. The set R of reachable
values is the set of all possible values taken by the state variable along the
running of S. We define R as follows:
                                    [
                               R=       T|kX 0 (X in )                     (4)
                                      k∈N

where T|X 0 is the restriction of T on X 0 and T|X 0 is not defined outside X 0 . To
prove that a set P is a loop invariant of the program is equivalent to prove that
R ⊆ P . We can rewrite R inductively:
                                    [
                         R = X in ∪    T i R ∩ Xi ∩ X0 .
                                                         
                                                                                  (5)
                                    i∈I

Let us denote by ℘(Rd ) the set of subsets of Rd and introduce the map F :
℘(Rd ) → ℘(Rd ) defined by:
                                     [
                      F (C) = X in ∪   T i C ∩ Xi ∩ X0
                                                       
                                                                       (6)
                                       i∈I
               d
We equip ℘(R ) with the partial order of inclusion. The infimum is understood
in this sense i.e. as the greatest lower bound with respect to this order. The
smallest fixed point problem is:
                          inf C ∈ ℘(Rd ) | C = F (C) .
                             

It is well-known from Tarski’s theorem that the solution of this problem exists,
is unique and in this case, it corresponds to R. Tarski’s theorem also states that
R is the smallest solution of the following Problem:
                          inf C ∈ ℘(Rd ) | F (C) ⊆ C .
                              

    Note also that the map F corresponds to a standard transfer function (or
collecting semantics functional) applied to the PPS representation of a program.
We refer the reader to [CC77] for a seminal presentation of this approach.
    To prove that a subset P is a loop invariant, it suffices to show that P satisfies
F (P ) ⊆ P . In this case, such P is called inductive invariant.

3.2   Considered properties: sublevel properties Pκ,α
In this paper, we consider special properties: those that are encoded with sublevel
sets of a given polynomial function.
Definition 2 (Sublevel property). Given a polynomial function κ ∈ R[x] and
α ∈ R ∪ {+∞}, we define the sublevel property Pκ,α as follows:
                          Pκ,α := {x ∈ Rd | κ(x)  α} .
where  denotes ≤ when α ∈ R and denotes < for +∞. The expression κ(x) <
+∞ expresses the boundedness of κ(x) without providing a specific bound α.
Example 2 (Sublevel property examples).
Boundedness. When one wants to bound the reachable values of a system, we
can try to bound the l2 -norm of the system: Pk·k22 ,∞ with κ(x) = kxk22 . The use
of α = ∞ does not impose any bound on κ(x).
Safe set. Similarly, it is possible to check whether a specific bound is matched.
Either globally using the l2 -norm and a specific α: Pk·k22 ,α , or bounding the
reachable values of each variable: Pκi ,αi with κi : x 7→ xi and αi ∈ R.
Avoiding bad regions. If the bad region can be encoded as a sublevel property
k(x) ≤ 0 then its negation −k(x) ≤ 0 characterize the avoidance of that bad
zone. Eg. if one wants to prove that the square norm of the program variables
is always greater than 1, then we can consider the property Pκ,α with κ(x) =
1 − kxk22 and α = 0.

   A sublevel property is called sublevel invariant when this property is a
loop invariant. This turns out to be difficult to prove loop invariant properties
while considering directly R, thus we propose to find a more tractable over-
approximation of R for which such properties hold.


3.3   Approach: compute a Pκ,α -driven inductive invariant P

In this subsection, we explain how to compute a d-variate polynomial p ∈ R[x]
and a bound w ∈ R, such that the polynomial sublevel sets P := {x ∈ Rd |
p(x) ≤ 0} and Pκ,w satisfy:

                              R ⊆ P ⊆ Pκ,w ⊆ Pκ,α .                           (7)

The first (from the left) inclusion forces P to be valid for the whole reachable
values set. The second inclusion constraints all elements of P to satisfy the
given sublevel property for a certain bound w. The last inclusion requires that
the bound w is smaller than the desired level α. When α = ∞, any bound w
ensures the sublevel property.
    Now, we derive sufficient conditions on p and w to satisfy Equation (7). We
decompose the problem in two parts. To satisfy the first inclusion, i.e. ensure
that P is a loop invariant, it suffices to guarantee that F (P ) ⊆ P , namely that
P is an inductive invariant. Using Equation (5), P is an inductive invariant if
and only if:                   [
                        X in ∪     T i P ∩ Xi ∩ X0 ⊆ P ,
                                                    

                               i∈I

or equivalently:
                           X in ⊆ P ,
                       
                                                                              (8)
                           ∀ i ∈ I, T i P ∩ X i ∩ X 0 ⊆ P .
                                                     

Thus, we obtain:

                                               ∀x ∈ X in ,
               
                                  p(x) ≤ 0 ,
                                i                                             (9)
                   ∀ i ∈ I , p (T (x)) ≤ 0 ,   ∀x ∈ P ∩ X i ∩ X 0 .
Now, we are interested in the second and third inclusions at Equation (7) that
is the sublevel property satisfaction. The condition P ⊆ Pκ,w ⊆ Pκ,α can be
formulated as follows:
                           κ(x) ≤ w ≤ α , ∀x ∈ P .                        (10)
We recall that we have supposed that P is written as {x ∈ Rd | p(x) ≤ 0} where
p ∈ R[x]. Finally, we provide sufficient conditions to satisfy both (9) and (10).
Consider the following optimization problem:
         
           inf             w,
          p∈R[x],w∈R
         
         
                     s.t. p(x) ≤ 0 ,                    ∀x ∈ X in ,
                                                                             (11)
         
                          ∀ i ∈ I , p (T (x)) ≤ p(x) , ∀x ∈ X i ∩ X 0 ,
                                         i
                                                                d
                           κ(x) ≤ w + p(x) ,            ∀x ∈ R .
         

    We remark that α is not present in Problem (11). Indeed, since we mini-
mize w, either there exists a feasible w such that w ≤ α and we can exploit
this solution or such w is not available and we cannot conclude. However, from
Problem (11), we can extract (p, w) and in the case where the optimal bound w
is greater than α, we could use this solution with another method such as policy
iteration [AGM15].

Lemma 1. Let (p, w) be any feasible solution of Problem (11) with w ≤ α or
w < ∞ in the case of α = ∞. Then (p, w) satisfies both (9) and (10) with
P := {x ∈ Rd | p(x) ≤ 0}. Finally, P and Pκ,w satisfy Equation (7).

In practice, we rely on sum-of-squares programming to solve a relaxed version
of Problem (11).


4    Sums-of-Squares Programming for Invariant
     Generation

We first recall some basic background about sums-of-squares certificates for poly-
nomial optimization. Let R[x]2m stands for the set of polynomials of degree at
most 2m and Σ[x]  P ⊂ R[x] be the cone of sums-of-squares (SOS) polynomials,
that is Σ[x] := { i qi2 , with qi ∈ R[x] }. Our work will use the simple fact that
for all p ∈ Σ[x], then p(x) ≥ 0 for all x ∈ Rd i.e. Σ[x] is a restriction of the
set of theP nonnegative polynomials. For q ∈ R[x]2m , finding a SOS decomposi-
tion q = i qi2 valid over Rd is equivalent to solve the following matrix linear
feasibility problem:

                         q(x) = bm (x)T Q bm (x) ,      ∀x ∈ Rd ,                       (12)

where bm (x) := (1, x1 , . . . , xd , x21 , x1 x2 , . . . , xm
                                                             d ) (the vector of all monomials
in x up to degree m) and Q being a semidefinite positive matrix (i.e. all the
eigenvalues of Q are nonnegative). The size of Q (as well as the length of bm ) is
 d+m
     
   d   .
Example 3. consider the bi-variate polynomial q(x) := 1 + x21 − 2x1 x2 + x22 . With
b1 (x) = (1, x1 , x2 ), one looks for a semidefinite positive matrix Q such that the
polynomial equality q(x) = b1 (x)T Q b1 (x) holds for all x ∈ R2 . The matrix
                                                   
                                           1 0 0
                                    Q = 0 1 −1
                                           0 −1 1

satisfies this equality and has three nonnegative eigenvalues, which are 0, 1, and
2, respectively associated to the three eigenvectors e0 := (0, 1, 1)| , e1 := (1,0, 0)|
                                                                            1 0 0
and e2 := (0, 1, −1)| . Defining the matrices L := (e1 e2 e0 ) = 0 1 1 and
     1 0 0                                                     0 −1 1
                                                      |
D = 0 2 0 , one obtains the decomposition Q = L D L and the equality
        000
q(x) = (L b1 (x))T D (L b1 (x)) = σ(x) = 1 + (x1 − x2 )2 , for all x ∈ R2 . The
polynomial σ is called a SOS certificate and guarantees that q is nonnegative.

In practice, one can solve the general problem (12) by using semidefinite pro-
gramming (SDP) solvers (e.g. Mosek [AA00], SDPA [YFN+ 10]). For more de-
tails about SDP, we refer the interested reader to [VB94].
    One way to strengthen the three nonnegativity constraints of Problem (11) is
to consider the following hierarchy of SOS programs, parametrized by the integer
m representing the half of the degree of p:

       inf        w ,


  p∈R[x]2m ,w∈R

                                nin
                                X
                                     σj rjin ,

              s.t. −   p = σ   −

                             0





                                j=1

                                                   ni         n0


                                                 X          X
                                       i      i        i i
                                                                 γji rj0 ,




                  ∀ i ∈ I,  p − p ◦ T   =  σ   −     µ r
                                                       j j −
                                                  j=1        j=1




                   w+p−κ=ψ ,





                  ∀ j = 1, . . . , nin , σj ∈ Σ[x] , deg(σj rjin ) ≤ 2m ,






                  σ0 ∈ Σ[x] , deg(σ0 ) ≤ 2m ,





                  ∀ i ∈ I , σ i ∈ Σ[x] , deg(σ i ) ≤ 2m deg T i ,






                  ∀ i ∈ I , ∀ j = 1, . . . , ni , µij ∈ Σ[x] , deg(µij rji ) ≤ 2m deg T i ,





                  ∀ i ∈ I , ∀ j = 1, . . . , n0 , γ i ∈ Σ[x] , deg(γji rj0 ) ≤ 2m deg T i ,






                  ψ ∈ Σ[x] , deg(ψ) ≤ 2m .

                                                                                     (13)

Proposition 1. For a given m ∈ N, let (pm , wm ) be any feasible solution of
Problem (13). Then (pm , wm ) is also a feasible solution of Problem (11). More-
over, if wm ≤ α then both Pm := {x ∈ Rd | pm (x) ≤ 0} and Pκ,wm satisfy
Equation (7).
Proof. The feasible solution (pm , wm ) is associated with SOS certificates ensur-
ing that the three equality constraints of Problem (13) hold: {σ0 , σj } is associated
to the first one, {σ i , µij , γji } is associated to the second one and ψ is associated
to the third one. The first equality constraint, namely
                                             nin
                                             X
                     −pm (x) = σ0 (x) −            σj (x)rjin (x) ,   ∀x ∈ Rd ,
                                             j=1


implies that ∀x ∈ X in , pm (x) ≤ 0. Similarly, one has ∀i ∈ I, ∀x ∈ X i ∩
X 0 , pm (T i (x)) ≤ pm (x) and ∀x ∈ Rd , κ(x) ≤ wm + pm (x). Then (pm , wm )
is a feasible solution of Problem (11). The second statement comes directly from
Lemma 1.

Computational considerations. Define t := max{deg T i , i ∈ I}. At step                        m of
this hierarchy, the number of SDP variables is proportional to d+2mt
                                                                                        
                                                                                    d      and     the
                                                      d+mt
                                                            
number of SDP constraints is proportional to             d    . Thus, one expects tractable
approximations when the number d of variables (resp. the degree 2m of the
template p) is small. However, one can handle bigger instances of Problem (13) by
taking into account the system properties. For instance one could exploit sparsity
as in [WKKM06] by considering the variable sparsity correlation pattern of the
polynomials {T i , i ∈ I}, {rji , i ∈ I, j = 1, . . . , ni }, {rj0 , j = 1, . . . , n0 }, {rjin , j =
1, . . . , nin } and κ.


5     Benchmarks
Here, we perform some numerical experiments while solving Problem (13) (given
in Section 4) on several examples. In Section 5.1, we verify that the program
of Example 1 satisfies some boundedness property. We also provide examples
involving higher dimensional cases. Then, Section 5.2 focuses on other properties,
such as checking that the set of variable values avoids an unsafe region. Numerical
experiments are performed on an Intel Core i5 CPU (2.40 GHz) with Yalmip
being interfaced with the SDP solver Mosek.

5.1    Checking boundedness of the set of variables values
Example 4. Following Example 1, we consider the constrained piecewise discrete-
time dynamical system S = (X in , X 0 , {X 1 , X 2 }, {T 1 , T 2 }) with X in = [0.9, 1.1]×
[0, 0.2], X 0 = {x ∈ R2 | r0 (x) ≤ 0} with r0 : x 7→ −1, X 1 = {x ∈ R2 | r1 (x) ≤ 0}
                              2
with r1 : x 7→ kxk − 1, X 2 = {x ∈ R2 | r2 (x) < 0} with r2 = −r1
and T : (x1 , x2 ) 7→ (c11 x21 + c12 x32 , c21 x31 + c22 x22 ), T 2 : (x1 , x2 ) 7→ (d11 x31 +
          1

d12 x22 , d21 x21 + d22 x22 ). We are interested in showing that the boundedness prop-
erty Pk·k22 ,α holds for some positive α.

Here we illustrate the method by instantiating the program of Example 1 with
the following input: a1 = 0.9, a2 = 1.1, b1 = 0, b2 = 0.2, c11 = c12 = c21 = c22 =
          (a) m = 3                       (b) m = 4                       (c) m = 5

                 Fig. 2. A hierarchy of sublevel sets Pm for Example 4


1, d11 = 0.5, d12 = 0.4, d21 = −0.6 and d22 = 0.3. We represent the possible
initial values taken by the program variables (x1 , x2 ) by picking uniformly N
          (i)   (i)
points (x1 , x2 ) (i = 1, . . . , N ) inside the box X in = [0.9, 1.1] × [0, 0.2] (see the
corresponding square of dots on Figure 2). The other dots are obtained after
                                          (i) (i)
successive updates of each point (x1 , x2 ) by the program of Example 1. The
sets of dots in Figure 2 are obtained with N = 100 and six successive iterations.
    At step m = 3, Program (13) yields a solution (p3 , w3 ) ∈ R6 [x] × R together
with SOS certificates, which guarantee the boundedness property, that is x ∈
R =⇒ x ∈ P3 := {p3 (x) ≤ 0} ⊆ Pk·k22 ,w3 =⇒ kxk22 ≤ w3 . One has p3 (x) :=
−2.510902467−0.0050x1 −0.0148x2 +3.0998x21 −0.8037x32 −3.0297x31 +2.5924x22 +
1.5266x1 x2 − 1.9133x21 x2 − 1.8122x1 x22 + 1.6042x41 + 0.0512x31 x2 − 4.4430x21 x22 −
1.8926x1 x32 + 0.5464x42 − 0.2084x51 + 0.5866x41 x2 + 2.2410x31 x22 + 1.5714x21 x32 −
0.0890x1 x42 − 0.9656x52 + 0.0098x61 − 0.0320x51 x2 − 0.0232x41 x22 + 0.2660x31 x32 +
0.7746x21 x42 +0.9200x1 x52 +0.6411x62 (for the sake of conciseness, we do not display
p4 and p5 ).
    Figure 2 displays in light gray outer approximations of the set of possible
values X1 taken by the program of Example 4 as follows: (a) the degree six
sublevel set P3 , (b) the degree eight sublevel set P4 and (c) the degree ten
sublevel set P5 . The outer approximation P3 is coarse as it contains the box
[−1.5, 1.5]2 . However, solving Problem (13) at higher steps yields tighter outer
approximations of R together with more precise bounds w4 and w5 (see the
corresponding row in Table 2).
    We also succeeded to certify that the same property holds for higher di-
mensional programs, described in Example 5 (d = 3) and Example 6 (d = 4).


Example 5. Here we consider X in = [0.9, 1.1] × [0, 0.2]2 , r0 : x 7→ −1, r1 :
x 7→ kxk22 − 1, r2 = −r1 , T 1 : (x1 , x2 , x3 ) 7→ 1/4(0.8x21 + 1.4x2 − 0.5x23 , 1.3x1 +
0.5x23 , 1.4x2 +0.8x23 ), T 2 : (x1 , x2 , x3 ) 7→ 1/4(0.5x1 +0.4x22 , −0.6x22 +0.3x23 , 0.5x3 +
0.4x21 ) and κ : x 7→ kxk22 .

Example 6. Here we consider X in = [0.9, 1.1] × [0, 0.2]3 , r0 : x 7→ −1, r1 : x 7→
kxk22 − 1, r2 = −r1 , T 1 : (x1 , x2 , x3 , x4 ) 7→ 0.25(0.8x21 + 1.4x2 − 0.5x23 , 1.3x1 +
0.5, x22 − 0.8x24 , 0.8x23 + 1.4x4 , 1.3x3 + 0.5x24 ), T 2 : (x1 , x2 , x3 , x4 ) 7→ 0.25(0.5x1 +
0.4x22 , −0.6x21 + 0.3x22 , 0.5x3 + 0.4x24 , −0.6x3 + 0.3x24 ) and κ : x 7→ kxk22 .
Table 1 reports several data obtained while solving Problem (13) at step m,
(2 ≤ m ≤ 5), either for Example 4, Example 5 or Example 6. Each instance of
Problem (13) is recast as a SDP program, involving a total number of “Nb. vars”
SDP variables, with a SDP matrix of size “Mat. size”. We indicate the CPU time
required to compute the optimal solution of each SDP program with Mosek.
    The symbol “−” means that the corresponding SOS program could not be
solved within one day of computation. These benchmarks illustrate the com-
putational considerations mentioned in Section 4 as it takes more CPU time
to analyze higher dimensional programs. Note that it is not possible to solve
Problem (13) at step 5 for Example 6. A possible workaround to limit this com-
putational blow-up would be to exploit the sparsity of the system.


            Table 1. Comparison of timing results for Example 4, 5 and 6

            Degree 2m                       4            6             8            10
                    Nb. vars              1513         5740          15705        35212
      Example 4
                    Mat. size              368         802            1404        2174
       (d = 2)        Time                0.82 s      1.35 s         4.00 s       9.86 s
                    Nb. vars              2115        11950         46461        141612
      Example 5
                    Mat. size              628        1860           4132          7764
       (d = 3)        Time                0.84 s      2.98 s         21.4 s       109 s
                    Nb. vars              7202        65306         18480           −
      Example 6
                    Mat. size             1670         6622         373057          −
       (d = 4)        Time                2.85 s      57.3 s        1534 s          −




            Table 2. Hierarchies of bounds obtained for various properties

        Benchmark                   κ                w2      w3        w4          w5
        Example 4                 k · k22           639     17.4      2.44        2.02
        Example 7       x 7→ 0.25 − kx + 0.5k22     0.25    0.249    0.0993     -0.0777
                                  k · k22           10.2    2.84      2.84        2.84
        Example 8
                        x 7→ kT (x) − T 2 (x)k22
                                1
                                                    5.66    2.81      2.78        2.78




5.2    Other properties
Here we consider the program given in Example 7. One is interested in showing
that the set X1 of possible values taken by the variables of this program does
not meet the ball B of center (−0.5, −0.5) and radius 0.5.
Example 7. Let consider the PPS S = (X in , X 0 , {X 1 , X 2 }, {T 1 , T 2 }) with X in =
[0.5, 0.7] × [0.5, 0.7], X 0 = {x ∈ R2 | r0 (x) ≤ 0} with r0 : x 7→ −1, X 1 = {x ∈
R2 | r1 (x) ≤ 0} with r1 : x 7→ kxk22 − 1, X 2 = {x ∈ R2 | r2 (x) ≤ 0} with
r2 = −r1 and T 1 : (x1 , x2 ) 7→ (x21 + x32 , x31 + x22 ), T 2 : (x, y) 7→ (0.5x31 +
0.4x22 , −0.6x21 + 0.3x22 ). With κ : (x1 , x2 ) 7→ 0.25 − (x1 + 0.5)2 − (x2 + 0.5)2 , one
has B := {x ∈ R2 | 0 ≤ κ(x)}. Here, one shall prove x ∈ R =⇒ κ(x) < 0 while
computing some negative α such that R ⊆ Pκ,α . Note that κ is not a norm, by
contrast with the previous examples.

At step m = 3 (resp.m = 4), Program (13) yields a nonnegative solution w3
(resp. w4 ). Hence, it does not allow to certify that R ∩ B is empty. This is
illustrated in both Figure 3 (a) and Figure 3 (b), where the light grey region
does not avoid the ball B. However, solving Program (13) at step m = 5 yields
a negative bound w5 together with a certificate that R avoids the ball B (see
Figure 3 (c)). The corresponding values of wm (m = 3, 4, 5) are given in Table 2.




          (a) m = 3                      (b) m = 4                      (c) m = 5

                 Fig. 3. A hierarchy of sublevel sets Pm for Example 7



    Finally, one analyzes the program given in Example 8.

Example 8. (adapted from Example 3 in [AJ13])
    Let S be the PPS (X in , X 0 , {X 1 , X 2 }, {T 1 , T 2 }) with X in = [−1, 1] × [−1, 1],
X = {x ∈ R2 | r0 (x) ≤ 0} with r0 : x 7→ −1, X 1 = {x ∈ R2 | r1 (x) ≤ 0} with
  0

r1 : x 7→ x2 − x1 , X 2 = {x ∈ R2 | r2 (x) ≤ 0} with r2 = −r1 and T 1 : (x1 , x2 ) 7→
(0.687x1 + 0.558x2 − 0.0001 ∗ x1 x2 , −0.292x1 + 0.773x2 ), T 2 : (x, y) 7→ (0.369x1 +
0.532x2 −0.0001x21 , −1.27x1 +0.12x2 −0.0001x1 x2 ). We consider the boundedness
property κ1 := k · k22 as well as κ2 (x) := kT 1 (x) − T 2 (x)k22 . The function κ2 can
be viewed as the absolute error made by updating the variable x after a possibly
“wrong” branching. Such behaviors could occur while computing wrong values
for the conditionals (e.g. r1 ) using floating-point arithmetics. Table 2 indicates
the hierarchy of bounds obtained after solving Problem (13) with m = 3, 4, 5, for
both properties. The bound w5 = 2.84 (for κ1 ) implies that the set of reachable
values may not be included in the initial set X in . A valid upper bound of the
error function κ2 is given by w5 = 2.78.
6    Templates bases
We finally present further use of the set P defined at Equation (7). This sub-
level set can be viewed as a template abstraction, following from the definition
in [AGG11], with a fixed template basis p and an associated 0 bound. This rep-
resentation allows to develop a policy iteration algorithm [AGM15] to obtain
more precise inductive invariants.
    We now give some simple method to complete this template basis to improve
the precision of the bound w found with Problem (13).
Proposition 2 (Template basis completions). Let (p, w) be a solution of
Problem (13) and Q be a finite subset of R[x] such that for all q ∈ Q, p−q ∈ Σ[x].
Then R ⊆ {x ∈ Rd | p(x) ≤ 0, q(x) ≤ 0, ∀ q ∈ Q} ⊆ Pκ,w ⊆ Pκ,α and
{x ∈ Rd | p(x) ≤ 0, q(x) ≤ 0, ∀ q ∈ Q} is an inductive invariant.
Proof. Let Q be the set {x ∈ Rd | p(x) ≤ 0, q(x) ≤ 0, ∀ q ∈ Q}. It is obvious
that Q ⊆ P = {x ∈ Rd | p(x) ≤ 0} and hence Q ⊆ Pκ,w . Now let us prove that
Q is an inductive invariant. We have to prove that Q satisfies Equation (8) that
is: (i) For all x ∈ X in , q(x) ≤ 0; (ii) For all i ∈ I, for all x ∈ Q ∩ X i ∩ X 0 ,
q(T i (x)) ≤ 0. For all q ∈ Q, we denote by ψq the element of Σ[x] such that
p − q = ψq . Let us show (i) and let x ∈ X in . We have q(x) = p(x) − ψq (x) and
since ψq ∈ Σ[x], we obtain, q(x) ≤ p(x). Now from Proposition 1 and Lemma 1
and since (p, w) is a solution of Problem (13), we conclude that q(x) ≤ p(x) ≤ 0.
    Now let us prove (ii) and let i ∈ I and x ∈ Q ∩ X i ∩ X 0 . We get q(T i (x)) =
p(T i (x)) − ψq (T i (x)) and since ψq ∈ Σ[x], we obtain q(T i (x)) ≤ p(T i (x)). Using
the fact that (p, w) is a solution of Problem (13) and using Proposition 1 and
Lemma 1, we obtain q(T i (x)) ≤ p(T i (x)) ≤ p(x). Since x ∈ Q ⊆ P = {y ∈ Rd |
p(y) ≤ 0}, we conclude that q(T i (x)) ≤ 0.
Actually, we can weaken the hypothesis of Proposition 2 to construct an in-
ductive invariant. Indeed, after the computation of p following Problem (13), it
suffices to take a polynomial q such that p − q ≥ 0. Nevertheless, we cannot com-
pute easily such a polynomial q. By using the hypothesis p − q ∈ Σ[x], we can
compute q by sum-of-squares. Proposition 2 allows to define a simple method to
construct a basic semialgebraic inductive invariant set. Then the polynomials de-
scribing this basic semialgebraic set defines a new templates basis and this basic
semialgebraic set can be used as initialisation of the policy iteration algorithm
developed in [AGM15]. Note that the link between the templates generation and
the initialisation of policy iteration has been addressed in [Adj14].
Example 9. Let us consider the property Pk·k22 ,∞ and let (p, w) be a solution of
Problem (13). We have κ(x) = 1≤j≤k x2j and w + p − κ = ψ where ψ ∈ Σ[x].
                                P
In [RJGF12], the templates basis used to compute bounds on the reachable
values set consists in the square variables plus a Lyapunov function. Let us
prove that, in our setting, Q = {x2k − w, k = 1, . . . , d} can complete {p} in the
                                        . , d} and let x ∈ Rd , p(x) − (x2k − w) =
                   P 2. Let2 k ∈ {1, . .P
sense of Proposition
p(x) − κ(x) + w + j6=k xj = ψ(x) + j6=k x2j ∈ Σ[x].
7     Related works and conclusion

Roux et al. [RJGF12] provide an automatic method to compute floating-point
certified Lyapunov functions of perturbed affine loop body updates. They use
Lyapunov functions with squares of coordinate functions as quadratic invariants
in case of single loop programs written in affine arithmetic. In the context of
hybrid systems, certified inductive invariants can be computed by using SOS
approximations of parametric polynomial optimization problems [LWYZ14]. In
[PJ04], the authors develop a SOS-based methodology to certify that the trajec-
tories of hybrid systems avoid an unsafe region.
    In the context of static analysis for semialgebraic programs, the approach
developed in [Cou05] focuses on inferring valid loop/conditional invariants for
semialgebraic programsc . This approach relaxes an invariant generation prob-
lem into the resolution of nonlinear matrix inequalities, handled with semidef-
inite programming. Our method bears similarities with this approach but we
generate a hierarchy of invariants (of increasing degree) with respect to target
polynomial properties and restrict ourselves to linear matrix inequality formula-
tions. In [BRCZ05], invariants are given by polynomial inequalities (of bounded
degree) but the method relies on a reduction to linear inequalities (the polyhedra
domain). Template polyhedra domains allow to analyze reachability for polyno-
mial systems: in [STDG12], the authors propose a method that computes linear
templates to improve the accuracy of reachable set approximations, whereas the
procedure in [DT12] relies on Bernstein polynomials and linear programming,
with linear templates being fixed in advance. Bernstein polynomials also appear
in [RG13] as polynomial templates but they are not generated automatically.
In [SG09], the authors use SMT-based techniques to automatically generate
templates which are defined as formulas built with arbitrary logical structures
and predicate conjunctions. Other reductions to systems of polynomial equalities
(by contrast with polynomial inequalities, as we consider here) were studied in
[MOS04,RCK07] and more recently in [CJJK14].
    In this paper, we give a formal framework to relate the invariant generation
problem to the property to prove on analyzed program. We proposed a prac-
tical method to compute such invariants in the case of polynomial arithmetic
using sums-of-squares programming. This method is able to handle non trivial
examples, as illustrated through the numerical experiments. Topics of further
investigation include refining the invariant bounds generated for a specific sub-
level property, by applying the policy iteration algorithm. Such a refinement
would be of particular interest if one can not decide whether the set of variable
values avoids an unsafe region when the bound of the corresponding sums-of-
squares program is not accurate enough. For the case of boundedness property,
it would allow to decrease the value of the bounds on the variables. Finally,
our method could be generalized to a larger class of programs, involving semi-
algebraic or transcendental assignments, while applying the same polynomial
reduction techniques as in [MAGW14].
c
    This approach also handles semialgebraic program termination
References
AA00.     Erling D. Andersen and Knud D. Andersen. The mosek interior point opti-
          mizer for linear programming: An implementation of the homogeneous al-
          gorithm. In Hans Frenk, Kees Roos, Tamás Terlaky, and Shuzhong Zhang,
          editors, High Performance Optimization, volume 33 of Applied Optimiza-
          tion, pages 197–232. Springer US, 2000.
Adj14.    A. Adjé. Policy iteration in finite templates domain. In 7th International
          Workshop on Numerical Software Verification (NSV’12), July 2014.
AGG11.    A. Adjé, S. Gaubert, and E. Goubault. Coupling policy iteration with
          semi-definite relaxation to compute accurate numerical invariants in static
          analysis. Logical Methods in Computer Science, 8(1), 2011.
AGM15.    Assalé Adjé, Pierre-Loïc Garoche, and Victor Magron. A Sums-of-Squares
          Extension of Policy Iterations, 2015. Technial report.
AJ13.     Amir Ali Ahmadi and Raphael M. Jungers. Switched stability of nonlinear
          systems via sos-convex lyapunov functions and semidefinite programming.
          In CDC’13, pages 727–732, 2013.
BRCZ05.   R. Bagnara, E. Rodríguez-Carbonell, and E. Zaffanella. Generation of
          basic semi-algebraic invariants using convex polyhedra. In C. Hankin,
          editor, Static Analysis: Proceedings of the 12th International Symposium,
          volume 3672 of LNCS, pages 19–34. Springer, 2005.
CC77.     P. Cousot and R. Cousot. Abstract interpretation: a unified lattice model
          for static analysis of programs by construction or approximation of fix-
          points. In Conference Record of the Fourth Annual ACM SIGPLAN-
          SIGACT Symposium on Principles of Programming Languages, pages 238–
          252, Los Angeles, California, 1977. ACM Press, New York, NY.
CJJK14.   David Cachera, Thomas Jensen, Arnaud Jobin, and Florent Kirchner. In-
          ference of polynomial invariants for imperative programs: A farewell to
          gröbner bases. Science of Computer Programming, 2014.
Cou05.    Patrick Cousot. Proving Program Invariance and Termination by Paramet-
          ric Abstraction, Lagrangian Relaxation and Semidefinite Programming. In
          Radhia Cousot, editor, Verification, Model Checking, and Abstract Inter-
          pretation, volume 3385 of Lecture Notes in Computer Science, pages 1–24.
          Springer Berlin Heidelberg, 2005.
DT12.     Thao Dang and Romain Testylier. Reachability analysis for polynomial
          dynamical systems using the bernstein expansion. Reliable Computing,
          17(2):128–152, 2012.
Fer04.    Jérôme Feret. Static analysis of digital filters. In David A. Schmidt, editor,
          Programming Languages and Systems, 13th European Symposium on Pro-
          gramming, ESOP 2004, Held as Part of the Joint European Conferences on
          Theory and Practice of Software, ETAPS 2004, Barcelona, Spain, March
          29 - April 2, 2004, Proceedings, volume 2986 of Lecture Notes in Computer
          Science, pages 33–48. Springer, 2004.
Las01.    Jean B. Lasserre. Global optimization with polynomials and the problem
          of moments. SIAM Journal on Optimization, 11(3):796–817, 2001.
Lau09.    Monique Laurent. Sums of squares, moment matrices and optimization
          over polynomials. In Mihai Putinar and Seth Sullivant, editors, Emerg-
          ing Applications of Algebraic Geometry, volume 149 of The IMA Volumes
          in Mathematics and its Applications, pages 157–270. Springer New York,
          2009.
LWYZ14.  Wang Lin, Min Wu, ZhengFeng Yang, and ZhenBing Zeng. Exact safety
         verification of hybrid systems using sums-of-squares representation. Sci-
         ence China Information Sciences, 57(5):1–13, 2014.
MAGW14. Victor Magron, Xavier Allamigeon, Stéphane Gaubert, and Benjamin
         Werner. Certification of Real Inequalities – Templates and Sums of
         Squares. Mathematical Programming SERIES B, pages 1–30, 2014. Volume
         on Polynomial Optimization.
MOS04.   M. Müller-Olm and H. Seidl. Computing polynomial program invariants.
         Inf. Process. Lett., 91(5):233–244, 2004.
Par03.   Pablo A. Parrilo. Semidefinite programming relaxations for semialgebraic
         problems. Mathematical Programming, 96(2):293–320, 2003.
PJ04.    Stephen Prajna and Ali Jadbabaie. Safety verification of hybrid systems
         using barrier certificates. In Rajeev Alur and GeorgeJ. Pappas, editors,
         Hybrid Systems: Computation and Control, volume 2993 of Lecture Notes
         in Computer Science, pages 477–492. Springer Berlin Heidelberg, 2004.
RCK07.   E. Rodríguez-Carbonell and D. Kapur. Automatic generation of poly-
         nomial invariants of bounded degree using abstract interpretation. Sci.
         Comput. Program., 64(1):54–75, 2007.
RG13.    Pierre Roux and Pierre-Loïc Garoche. A polynomial template abstract
         domain based on bernstein polynomials. In Sixth International Workshop
         on Numerical Software Verification (NSV’13), 2013.
RJGF12. P. Roux, R. Jobredeaux, P-L. Garoche, and E. Feron. A generic ellipsoid
         abstract domain for linear time invariant systems. In T. Dang and I. M.
         Mitchell, editors, HSCC, pages 105–114. ACM, 2012.
SG09.    Saurabh Srivastava and Sumit Gulwani. Program verification using tem-
         plates over predicate abstraction. SIGPLAN Not., 44(6):223–234, June
         2009.
STDG12. Mohamed Amin Ben Sassi, Romain Testylier, Thao Dang, and Antoine
         Girard. Reachability analysis of polynomial systems using linear program-
         ming relaxations. In Automated Technology for Verification and Analysis,
         pages 137–151. Springer, 2012.
VB94.    Lieven Vandenberghe and Stephen Boyd. Semidefinite programming.
         SIAM Review, 38(1):49–95, 1994.
WKKM06. Hayato Waki, Sunyoung Kim, Masakazu Kojima, and Masakazu Mura-
         matsu. Sums of squares and semidefinite programming relaxations for
         polynomial optimization problems with structured sparsity. SIAM Jour-
         nal on Optimization, 17(1):218–242, 2006.
YFN+ 10. M. Yamashita, K. Fujisawa, K. Nakata, M. Nakata, M. Fukuda,
         K. Kobayashi, and K. Goto. A high-performance software package for
         semidefinite programs : Sdpa7. Technical report, Dept. of Information
         Sciences, Tokyo Institute of Technology, Tokyo, Japan, 2010.
