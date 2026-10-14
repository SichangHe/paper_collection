    Linear Invariant Generation Using Non-linear
                  Constraint Solving

      Michael A. Colón, Sriram Sankaranarayanan, and Henny B. Sipma 

                           Computer Science Department
                                 Stanford University
                              Stanford, CA 94305-9045
                      {colon,srirams,sipma}@cs.stanford.edu



        Abstract. We present a new method for the generation of linear in-
        variants which reduces the problem to a non-linear constraint solving
        problem. Our method, based on Farkas’ Lemma, synthesizes linear in-
        variants by extracting non-linear constraints on the coeﬃcients of a
        target invariant from a program. These constraints guarantee that the
        linear invariant is inductive. We then apply existing techniques, including
        specialized quantiﬁer elimination methods over the reals, to solve these
        non-linear constraints. Our method has the advantage of being complete
        for inductive invariants. To our knowledge, this is the ﬁrst sound and
        complete technique for generating inductive invariants of this form. We
        illustrate the practicality of our method on several examples, including
        cases in which traditional methods based on abstract interpretation with
        widening fail to generate suﬃciently strong invariants.


1     Introduction

An invariant assertion of a program at a location is an assertion over the pro-
gram variables that remains true whenever the location is reached. Invariants
are essential for verifying the correctness of programs. The automatic generation
of invariants is useful both as a direct means of checking program speciﬁcations
and as an indirect means of obtaining intermediate assertions that can be used
as lemmas for proving other safety and liveness properties [16].
    An assertion is said to be inductive at a program location if it holds the
ﬁrst time the location is reached and is preserved under every cycle back to
the location. It has been established that all inductive assertions are invariant.
Furthermore, the standard method for proving a given assertion invariant is to
ﬁnd an inductive assertion that strengthens it [16]. Thus invariant generation
methods are, normally, methods for generating inductive assertions.
    The dominant invariant generation technique is abstract interpretation [6].
The main idea behind this approach is to perform an approximate symbolic

    This research was supported in part by NSF(ITR) grant CCR-01-21403, by NSF
    grant CCR-99-00984-001, by ARO grant DAAD19-01-1-0723, and by ARPA/AF
    contracts F33615-00-C-1693 and F33615-99-C-3014.

W.A. Hunt, Jr. and F. Somenzi (Eds.): CAV 2003, LNCS 2725, pp. 420–432, 2003.

c Springer-Verlag Berlin Heidelberg 2003
             Linear Invariant Generation Using Non-linear Constraint Solving            421

execution of the program until an assertion is reached that remains unchanged by
further executions of the program. This assertion can be shown to be inductive,
and hence invariant. However, in order to guarantee termination, the method
introduces imprecision by use of an extrapolation operator called widening. This
operator often causes the technique to produce weak invariants. The design of a
widening operator with some guarantee of completeness remains a key challenge
for abstract interpretation based techniques [7,1]. In fact, tools like HyTech [12]
have given up widening in favor of extrapolation heuristics with no convergence
guarantees and have reported good results.
    In this paper, we generate linear invariants for linear transition systems,
a class of programs that is widely studied [7,1,11]. A large number of reac-
tive systems may be modeled directly or approximately as linear transition
systems [13]. Rather than perform a least ﬁxed point computation by itera-
tion, we solve constraints on the coeﬃcients c1 , . . . , cn , d of a target invariant
c1 x1 + · · · + cn xn + d ≤ 0. The constraints encode the conditions for inductive-
ness of the inequality. The solution method is exact, thus guaranteeing that all
inductive invariants of this form can be found. The main advantage is that there
is no heuristic widening operation, and thus the method does not suﬀer from
the problem of overshooting invariants. On the other hand, the method gener-
ates non-linear constraints that can be solved only for small or medium size
problem instances using current techniques. This disadvantage notwithstanding,
we demonstrate our approach on some examples drawn from the literature. We
show that in many cases, our method generates invariants that forward propa-
gation with widening misses. Non-linear constraint solving is an active area of
research, and our approach will become increasingly practical as more eﬀective
techniques for solving these constraints are developed.
    The rest of the paper is organized as follows: Section 2 presents some prelim-
inary deﬁnitions. In Section 3, we present a method for generating constraints
using Farkas’ Lemma. Techniques for solving non-linear constraints are brieﬂy
described in Section 4. Section 5 illustrates the method on several examples, and
ﬁnally, Section 6 concludes with a discussion of the advantages and drawbacks
of the approach.

2    Preliminaries
In this section, we provide some key deﬁnitions and present Farkas’ Lemma, the
basis of our approach.

Transition Systems and Invariants
Deﬁnition 1 (Transition System) A transition system P : V, L, l0 , Θ, T 
consists of a set of variables V , a set of locations L, an initial location l0 , an initial
assertion Θ over the variables V , and a set of transitions T . Each transition
τ ∈ T is a tuple l, l , ρτ , where l, l ∈ L are the pre and post locations, and ρτ is
the transition relation, an assertion over V ∪V  , where V represents current-state
variables and its primed version V  represents the next-state variables.
422     Michael A. Colón, Sriram Sankaranarayanan, and Henny B. Sipma

Throughout the paper, unless otherwise stated, we assume that the set of vari-
ables V = {x1 , . . . , xn } is ﬁxed. Furthermore, given an assertion ψ over the
variables V of a transition system, ψ  denotes the assertion obtained by replac-
ing each variable x ∈ V by x ∈ V  .
    The control-ﬂow graph (CFG) of a transition system is a graph whose vertices
are the locations and whose edges are the transitions. A path π of the transition
system is a path through its CFG, and the relation ρπ associated with the path
is the composition of the corresponding transition relations.
    A cutset C of a transition system P is a subset of the locations of P with
the property that every cyclic path in P passes through some location in C. A
location inside a cutset is called a cutpoint. A basic path π between two cutpoints
li and lj is a simple path that does not go through any cutpoint, other than the
end points.

Deﬁnition 2 (Inductive Assertion Map) Given a program P with a cutset
C and an assertion ηc (l), for each cutpoint l, we say that ηc is an inductive
assertion map for C if it satisﬁes the following conditions for all cutpoints l, l :

Initiation For each basic path π from l0 to l, Θ ∧ ρπ |= ηc (l) .
Consecution For each basic path π from l to l , ηc (l) ∧ ρπ |= ηc (l ) .

   Any such partial map may be extended in a natural way to a total map,
provided a computable post image operator is available. If the cutset C is obvious
from the context, we drop the subscript from the map.


Linear and Non-linear Constraints

A linear constraint over V is an inequality of the form a1 x1 + · · · + an xn + b ≤ 0,
where a1 , · · · , an , b denote known real-valued coeﬃcients. The constraint is said
to be homogeneous if b = 0 and inhomogeneous otherwise. A linear assertion
over a set of variables V is a conjunction of linear constraints over V . A linear
assertion consisting of k inequalities is said to be k-linear. Geometrically, the set
of points satisfying a linear assertion forms a polyhedron. Linear assertions have
been thoroughly studied; problems like satisﬁability and projection are known
to be decidable [17].
    Given a set of vectors S, the cone generated by S, denoted by cone(S), is
the set of all the vectors of the form λ1 s1 + · · · + λm sm , where s1 , . . . , sm ∈ S
and λ1 , . . . , λm ≥ 0. A cone is said to be ﬁnitely generated if it is cone(S)
for some ﬁnite S. Polyhedral cones are cones that can be characterized as the
solution spaces of homogeneous linear assertions. A fundamental result states
that a cone is ﬁnitely generated iﬀ it is polyhedral [17].
    A non-linear constraint is an inequality of the form P ≤ 0, where P is a
polynomial on x1 , . . . , xn . The degree of the constraint is deﬁned as the degree
of the polynomial P . A non-linear assertion is a conjunction of non-linear con-
straints. A polynomial P is said to be reducible if P = P1 P2 , where P1 and
P2 are polynomials of strictly lower degree than P . The set of points satisfying
             Linear Invariant Generation Using Non-linear Constraint Solving                       423

      integer i, j where i = 2 ∧ j = 0               L = {l0 , l1 }, V = {i, j},
         : while true do
      l0                                           Θ : (i = 2 ∧ j = 0), T = {τ0 , τ1 , τ2 },
                i := i + 4                           τ0 : l0 , l1 , true
          l1 :      or                             τ1 : l1 , l0 , (i = i + 4 ∧ j  = j)
                (i, j) := (i + 2, j + 1)             τ2 : l1 , l0 , (i = i + 2 ∧ j  = j + 1)


 Fig. 1. A simple program fragment and the corresponding transition system


a non-linear assertion is called a semi-algebraic set. Problems such as satisﬁa-
bility, projection, intersection and union, though still decidable, have a higher
complexity than for linear constraints [2].
    We say that a transition system is linear if its initial assertion Θ is linear
over V and its transition relations ρτ are linear assertions over V ∪ V  . Conse-
quently, for every simple path π, the relation ρπ is a linear assertion. The rest of
this paper deals with linear transition systems. Corresponding to an inductive
assertion map, a k-linear inductive assertion map (k > 0) is deﬁned to be an
assertion map, wherein each assertion is k-linear.

Example. Figure 1 shows a simple program fragment over the variables i and
j, taken from [7]. As a transition system, it has a two locations l0 and l1 , and
three transitions τ0 , τ1 and τ2 .

Farkas’ Lemma
Farkas’ lemma provides a sound and complete method for reasoning about sys-
tems of linear inequalities.
Theorem 1 (Farkas’ Lemma). Consider the following system of linear in-
equalities over real-valued variables x1 , . . . , xn ,
                                                            
                            a11 x1 + · · · + a1n xn + b1 ≤ 0
                                ..                    .. .. 
                     S:          .                     .  . 
                                    am1 x1 + · · · + amn xn + bm ≤ 0
When S is satisﬁable, it entails a given linear inequality
                                   ψ : c1 x1 + · · · + cn xn + d ≤ 0
if and only if there exist non-negative real numbers λ0 , λ1 , . . . , λm , such that
                  
                  m                                  
                                                     m                   m
           c1 =         λi ai1 ,     ...    , cn =         λi ain , d = (   λi bi ) − λ0
                  i=1                                i=1                 i=1

Furthermore, S is unsatisﬁable if and only if the inequality 1 ≤ 0 can be derived
as shown above.
We represent applications of the lemma using a tabular notation:
424         Michael A. Colón, Sriram Sankaranarayanan, and Henny B. Sipma

                       λ0                          −1 ≤ 0 
                       λ1 a11 x1 + · · · + a1n xn + b1 ≤ 0 
                        ..     ..               ..   ..        S
                         .      .                .    .     
                                                            
                      λm am1 x1 + · · · + amn xn + bm ≤ 0
                           c1 x1 + · · · + cn xn + d ≤ 0 ← ψ
                                                      1 ≤ 0 ← false
The antecedents are placed above the line and the consequences below. For each
column, the sum of the column entries above the line, with the appropriate
multipliers, must be equal to the entry below the line. If a row corresponds to
an inequality, the corresponding multiplier is required to be non-negative. This
requirement is dropped for rows corresponding to equalities.

3     Generating Invariants
We now present our approach to linear invariant generation. We represent the
invariant
                         c1 x1 + · · · cn xn + d ≤ 0
in terms of its coeﬃcients c1 , . . . , cn , d. The main idea behind our technique is to
treat these coeﬃcients as unknowns and generate constraints on the coeﬃcients
such that any solution corresponds to an inductive assertion. The key to this
approach is Farkas’ Lemma.
    Given a transition system and a cutset, we generate a (partial) inductive
assertion map η over the cutpoints by encoding initiation and consecution. Let
η(l) be represented by the assertion cl1 x1 + · · · + cln xn + dl ≤ 0, where each cli
and each dl is an unknown.1 The two conditions for the map to be inductive are
encoded as follows:

Initiation: For each cutpoint l and each basic path π from l0 to l, the path
may be an enabled path, in which case Θ ∧ ρπ is satisﬁable, or the path may be
disabled, in which case, Θ ∧ ρπ is unsatisﬁable. Initiation can thus be represented
by the following table,
      λ0                                                                −1 ≤ 0 
      λ1    a11 x1 + · · · +    a1n xn                               + b1 ≤ 0    
       ..        ..                  ..                                   ..         Θ
        .         .                   .                                    .      
                                                                                  
    λj−1 aj−1,1 x1 + · · · + aj−1,n xn                               + bj−1 ≤ 0 
      λj    aj1 x1 + · · · +    ajn xn + aj1 x1 + · · · + ajn xn + bj ≤ 0    
       ..         ..                  ..       ..                 ..       ..        ρπ
        .          .                   .        .                  .        .     
                                                                                  
                                                                
     λm am1 x1 + · · · + amn xn + am1 x1 + · · · + amn xn + bm ≤ 0
                                         cl1 x1 + · · · + cln xn + dl ≤ 0 ← η(l)
                                                                            1 ≤ 0 ← disabled
where λ0 , . . . , λm ≥ 0.
1
    We use c, d with subscripts to denote unknowns and a, b with subscripts to denote
    known values.
            Linear Invariant Generation Using Non-linear Constraint Solving                425

Consecution: For each basic path π from a cutpoint li to a cutpoint lj , we
encode the consecution condition, η(li ) ∧ ρπ |= η(lj ) , using Farkas’ Lemma.
Again there are two cases to consider, one when the path is enabled and the
other when it is disabled. The constraints are represented by the table shown
below:
       µ cli 1 x1 + · · · + cli n xn                                + dli ≤ 0 ← η(li )
      λ0                                                              −1 ≤ 0 
      λ1 a11 x1 + · · · + a1n xn + a11 x1 + · · · + a1n xn + b1 ≤ 0       
       ..       ..                 ..        ..                  ..    ..        ρπ
        .        .                  .         .                   .     .      
                                                                               
                                                               
     λm am1 x1 + · · · + am1 xn + am1 x1 + · · · + amn xn + bm ≤ 0
                                      clj 1 x1 + · · · + clj n xn + dlj ≤ 0, ← η(lj )
                                                                        1 ≤ 0 ← disabled

where µ, λ0 , . . . , λm ≥ 0.
    The constraints corresponding to initiation are linear, as are the constraints
corresponding to the disabled case of consecution. However, the constraints for
the enabled case of consecution are non-linear due to the presence of the mul-
tiplier µ in a row containing unknown coeﬃcients. Methods for solving these
constraints are discussed in Section 4.

Example. Consider the program shown in Figure 1. All cycles of the program
are cut by l0 . Let ϕ : c1 i + c2 j + d ≤ 0 be the target invariant at this cutpoint.
The initial condition, i = 2 ∧ j = 0, generates the constraints

                         λ0                −1 ≤ 0
                         λ1    i           −2 = 0
                         λ2             j     =0
                              c1 i + c2 j + d ≤ 0 ← ϕ
                                            1 ≤ 0 ← disabled

   We can ignore the disabled case since the initial condition is satisﬁable. With
the requirement that λ0 be non-negative, we obtain the following constraints:

                                          c1 = λ1 ∧ c2 = λ2 ∧
                 ψΘ : (∃λ0 , λ1 , λ2 )                                                     (1)
                                          d = −2λ1 − λ0 ∧ λ0 ≥ 0

Two paths cycle back to l0 : path π1 using τ1 and π2 through τ2 . For the path
π1 , the transition relation ρπ1 is given by i − i + 4 = 0 ∧ j − j  = 0. The two
constraints for consecution are given by the table

                  µ c1 i + c2 j                     +d≤0
                  λ0                                −1≤0
                  λ1 i          −      i           +4=0
                  λ2          j            − j         =0
                                    c1 i  + c2 j  + d ≤ 0 ← ϕ
                                                      1 ≤ 0 ← disabled

resulting in the constraints:
426     Michael A. Colón, Sriram Sankaranarayanan, and Henny B. Sipma
                                                                
           0 = µc1 + λ1 ∧                      0 = µc1 + λ1 ∧
          0 = µc2 + λ2 ∧                    0 = µc2 + λ2 ∧      
                                                                
         
 (∃λ, µ)  c1 = −λ1 ∧ c2 = −λ2 ∧  ∨ (∃λ, µ)  0 = −λ1 ∧ 0 = −λ2 ∧ 
                                            
                                                                    (2)
          d = µd + 4λ1 − λ0 ∧               1 = µd + 4λ1 − λ0 ∧ 
           µ, λ0 ≥ 0                           µ, λ0 ≥ 0

Similarly, the constraints corresponding to consecution for π2 are
                                                                       
           0 = µc1 + λ1 ∧                        0 = µc1 + λ1 ∧
          0 = µc2 + λ2 ∧                      0 = µc2 + λ2 ∧           
                                                                       
         
 (∃λ, µ)  c1 = −λ1 ∧ c2 = −λ2 ∧  ∨ (∃λ, µ)  0 = −λ1 ∧ 0 = −λ2 ∧ 
                                              
                                                                           (3)
          d = µd + 2λ1 + λ2 − λ0 ∧            1 = µd + 2λ1 + λ2 − λ0 ∧ 
           µ, λ0 ≥ 0                             µ, λ0 ≥ 0

We will eliminate the quantiﬁers and complete the example in Section 4. The
technique presented in this section can be easily extended to k-linear assertion
maps. Farkas’ Lemma may be used in this case to obtain constraints for initiation
and consecution with few changes.

Theorem 2. For any k > 0, a k−linear assertion map η is inductive iﬀ it is a
solution to the system of constraints generated by our method.

The theorem follows directly from Farkas’ Lemma and our constraint generation
technique. It states that our technique is sound. Furthermore, completeness holds
for those linear invariants that can be proved using linear inductive assertions. A
linear program may have a reachable state-space that is not convex, but induc-
tive linear assertions can only characterize convex sets. Hence, there are linear
programs which satisfy linear invariants that can only be established by resort-
ing to non-linear or non-convex inductive assertions. This result is demonstrated
by the work of Clarke [3].
    In theory, having a conjunction of k > 1 linear inequalities at each cutpoint
is better than a single inequality at each cutpoint. In practice however, we ﬁnd
that the constraints obtained for k > 1 are too complex to solve exactly for
all but the smallest of systems. Nevertheless, as Section 5 illustrates, our tech-
nique with exact solution is powerful even when restricted to 1-linear assertions.
Furthermore, k-linear inductive assertions can be approximated iteratively, by
starting with 1-linear assertions and strengthening each transition relation with
the invariants computed in the previous stage.


4     Solving Constraints
Our method extracts linear and non-linear constraints characterizing inductive
assertions. Any solution to these constraints is thus inductive. These constraints
may be solved by eliminating the quantiﬁed variables. In practice, however, quan-
tiﬁer elimination is a costly process with exponential time complexity. Therefore,
we exploit various techniques like factorization and root ﬁnding to simplify the
constraints, thereby reducing the size of each quantiﬁer elimination instance and
           Linear Invariant Generation Using Non-linear Constraint Solving    427

that of the result after elimination. In some cases, we are able to generate all
the solutions solely by making use of these simpliﬁcation techniques, without
resorting to quantiﬁer elimination. We present some of these techniques and
then apply them to solve the constraints generated for our running example.
The reader is referred to the comprehensive survey by Bockmayr and Weispfen-
ning [2] on constraint solving for more details.


Linear Constraints

Geometrically, the set of points satisfying an inhomogeneous linear assertion
forms a polyhedron, and the set satisfying a homogeneous linear assertion is a
polyhedral cone; elimination of variables corresponds to projection. One approach
to projection is to compute the generators of the polyhedron and then project
these generators on to the free variables. These generators can be computed by
the simplex method [17] or the double description method [9]. In our examples,
presented in the next section, we use an implementation of the double description
method called PolKa [10].
    Alternatively, projection and the computation of generators can be achieved
through a quantiﬁer elimination method called Fourier’s elimination, which elim-
inates variables from the system of constraints incrementally [2]. Due to its sim-
plicity, Fourier’s elimination has been used widely to solve linear constraints,
even though its complexity is exponential.


Non-linear Constraints

Non-linear constraints can be solved by direct quantiﬁer elimination or indirect
methods using techniques such as factorization and polynomial root solving.
    The original breakthrough in quantiﬁer elimination was due to Tarski [18].
However, it was not computationally feasible until Collins introduced Cylindri-
cal Algebraic Decomposition [5]. Recently, there have been many practical im-
plementations based on this technique. Notable among them is qepcad, which
incorporates many improvements to the original CAD algorithm [4]. The time
complexity of the algorithm is exponential in the size of the formula. However,
the running time can be brought down signiﬁcantly for low degree polynomials
using the elimination at test points method due to Weispfenning [19]. After quan-
tiﬁer elimination, simpliﬁcation is carried out using factorization and Gröbner
Bases. This method has been implemented in redlog [8].
    Another approach is to use linear programming and delay processing non-
linear constraints until they can be linearized or simpliﬁed to an extent that
they can be solved directly. This approach, which is at the heart of many clp
based solvers [15], works for a surprisingly large variety of problems. However,
there are problems that require non-linear constraint solving. Thus, non-linear
constraint solvers have been incorporated into the clp paradigm. For instance,
the risc-clp(r) system uses quantiﬁer elimination in the background to solve
constraints [14].
428      Michael A. Colón, Sriram Sankaranarayanan, and Henny B. Sipma

Heuristics

The constraints we obtain are of a low degree and hence, redlog is the most
suitable tool. A disadvantage of using quantiﬁer elimination is the size of the
result after elimination. In general, the ﬁnal result after elimination is a boolean
combination of, mostly unfactorized, polynomial equalities and inequalities, con-
taining redundant non-linear inequalities that need to be detected and removed.
It has been our experience so far that the majority of these reduce to linear
factors, and that non-linear irreducible polynomials are rare.
    If the polynomials in the result are linear, then the cone containing all the
solutions is polyhedral, and a minimal set of generators for this cone can be
computed using the double description method. The set of inductive invariants
can be completely characterized by considering each of these generators as a
constraint.
    If there are irredundant and unfactorizable non-linear constraints, the cone
of consequences may or may not be ﬁnitely generated. However, we are unaware
of an eﬃcient method for deciding which case holds. When the cone is not
ﬁnitely generated, it is not possible to characterize all invariants without using
a parametric representation.
    We have found a few heuristics that are eﬀective in dealing with non-linear
factors: If a polynomial P is reducible, it is always possible to reduce the degree of
the constraints by splitting. For instance, the constraint P1 P2 ≤ 0 is equivalent to
the disjunction (P1 ≤ 0 ∧ P2 ≥ 0) ∨ (P1 ≥ 0 ∧ P2 ≤ 0). Further information about
polynomial factorization can be found in standard textbooks on the topic [21].
    Another heuristic, especially eﬀective when the result of the elimination is
too large to be factorized or simpliﬁed, is to set some of the coeﬃcients to zero,
in eﬀect restricting the target invariants to those involving only a subset of the
variables of the program. Furthermore, since any two-dimensional cone is ﬁnitely
generated, setting suﬃciently many variables to zero always yields a polyhedral
cone.
Example. We can now complete our example from the previous section by ap-
plying the techniques mentioned in this section to solve the constraints.
    The initiation constraint shown in (1) is linear and simpliﬁes to 2c1 + d ≤ 0.
The constraints corresponding to consecution for path π1 are shown in (2). It is
possible to solve them using quantiﬁer elimination. However, a simple substitu-
tion on the ﬁrst clause yields −µλ1 + λ1 = 0 ∧ −µλ2 + λ2 = 0, which can be
simpliﬁed to µ = 1 or λ1 = λ2 = 0. Branching on both possibilities, we obtain
c1 ≤ 0 for the former and c1 = c2 = 0, d ≤ 0 for the latter. The other clause can
be similarly solved using substitution, yielding c1 = c2 = 0 ∧ d ≥ 0. Consecution
for path π2 can also be solved using factorization. The ﬁnal result is:
                                                                           
                        (c1 = c2 = 0 ∧ d ≤ 0) ∨       (c1 = c2 = 0 ∧ d ≤ 0) ∨
      (2c1 + d ≤ 0) ∧  (c1 ≤ 0) ∨               ∧  (2c1 + c2 ≤ 0) ∨        
                        (c1 = c2 = 0 ∧ d ≥ 0)         (c1 = c2 = 0 ∧ d ≥ 0)
            Linear Invariant Generation Using Non-linear Constraint Solving      429

                 integer i, j, k where i = 1 ∧ j = 1 ∧ 0 ≤ k ≤ 1
                 l0 : while true do
                   l1 : (i, j, k) := (i + 1, j + k, k − 1)


                                Fig. 2. increment


After converting this into DNF and eliminating unsatisﬁable disjuncts, we obtain
the following generators shown along with the corresponding invariants:
                         c1 c2 d         c1 i + c2 j + d ≤ 0
                          0 0 −1                     −1 ≤ 0
                          0 −1 0                     −j ≤ 0
                         −1 2 2           −i + 2j + 2 ≤ 0
These match the invariants obtained in [7]. Additional inductive assertions, such
as −i + 2 ≤ 0 can be obtained as consequences of the assertions shown above.

5   Applications
We now demonstrate our approach on several examples.

Increment
Consider the program increment shown in Figure 2. With each iteration it
increments i, while manipulating the variables j and k. Surprisingly, the analysis
of Cousot and Halbwachs [7] misses the obvious invariant i ≥ 1. On the other
hand, our method produces the invariants 1 ≤ i + k ≤ 2 and i ≥ 1 in one
iteration. This phenomenon, in which the presence of additional, independent
variables weakens the invariants generated using abstract interpretation, can be
observed in more realistic programs, e.g. the implementation of mergesort
presented by Wirth [20].

Heapsort
We applied our method to heapsort, shown in Figure 3 and taken from [7].
Arrays and operations involving arrays were not modeled in the transition sys-
tem, and branches involving array conditions were treated as non-deterministic
choices. All cycles are cut by l3 . There are eight paths that go from l3 back to it-
self. Upon simpliﬁcation, the formula obtained after elimination does not contain
any non-linear constraint, and the following invariants were easily extracted:
                l−1≥0                 r≥2                2l − r ≥ 0
                  n≥3                 r≤n                     j = 2i
Repeating the analysis assuming l ≥ 1, we obtained the additional invariants
2l ≤ j, 2l + 2r ≥ j + 2, matching the invariants generated using abstract inter-
pretation [7].
430    Michael A. Colón, Sriram Sankaranarayanan, and Henny B. Sipma

               integer n, l, r, i, j where l = n2 + 1 ∧ n ≥ 2 ∧ r = n
               realarray T [1 . . . n];
               real k;
               l0 : if l ≥ 2 then
                   l0a : (l, k) := (l − 1, T [l]);
               else
                     l0b : (k, T [r], r) := (T [r], T [1], r − 1);
               end if
               l1 : while r ≥ 2 do
                                                                             
                     l2 : (i, j) := (l, 2l);
                l3 : while j ≤ r do                                          
                                                                           
                           l4 : if j ≤ r − 1 ∧ T [j] < T [j + 1] then 
                                                                             
                                l4a : j := j + 1;                          
                                                                           
                          end if                                           
                                                                           
                          l5 : if k ≥ T [j] then                           
                                                                           
                                l a
                                        :  break;                            
                                  5                                        
                          end if ;                                         
                                                                             
                           l   :    (T   [i], i, j) :=  (T [j], j, 2j);      
                             6                                               
                       end     while                                         
                                                                             
                        l7 : T [i] := k;                                     
                                                                             
                        l8 : if l ≥ 2 then                                   
                                                                             
                               l a
                                      :   (l, k)  :=  (l −  1, T [l]);        
                                 8                                           
                                                                             
                             else                                            
                               l8 : (k, T [r], r) := (T [r], T [1], r − 1);
                                  b                                           
                                                                             
                        end if                                               
                    l9 : T [1] := k;
                 end while


                                  Fig. 3. heapsort


Vagrant Robot

We analyzed a hybrid system modeling the position of a robot over time, taken
from [12], represented as the linear transition system presented in Figure 4.
The robot works in two alternating phases modeled by locations l0 and l1 , each
taking between 1 and 2 seconds. In l0 it moves approximately northeast (both
x and y increase), and in l1 it moves approximately southeast (x increases and
y decreases). The result after quantiﬁer elimination is too large to be factorized
or to be converted into some normal form by redlog. Therefore, we analyzed
the expression with each of the coeﬃcients set to 0, thus looking for invariants
involving at most two variables at a time. The invariants obtained for cutpoint
l0 were: t ≤ x ≤ 2t, and −t ≤ y ≤ t. Taking their post image produces the
following invariants at location l1 : t ≤ x ≤ 2t, −t + 2 ≤ y ≤ t + 2, y ≤ 2t and
t ≥ 1.
    Note that the invariant assertions above are true immediately after a discrete
mode transition is taken. If the continuous evolution is to be taken into account,
as is always the case for a hybrid system, we need to perform an additional post
            Linear Invariant Generation Using Non-linear Constraint Solving             431


                         V = {x, y, t}, L = {l0 , l1 }, T = {τ1 , τ2 }
                            τ1 : l0 , l1 , ρ1  , τ2 : l1 , l0 , ρ2 
                             Θ: x=0 ∧ y=0 ∧ t=0
                                                                                    
        t − t ≤ x − x ≤ 2(t − t) ∧                  t − t ≤ x − x ≤ 2(t − t) ∧
 ρ1 :  t − t ≤ y  − y ≤ 2(t − t) ∧        ρ2 :  −(t − t) ≥ y  − y ≥ −2(t − t) ∧ 
        1 ≤ t − t ≤ 2                                1 ≤ t − t ≤ 2


                  Fig. 4. Transition system for the vagrant robot


image computation at each location to obtain the true invariant from a hybrid
system point of view. In either case, the invariants above suﬃce to establish the
unreachability of the point y = 12, x = 9, which is posed as a challenge to the
reader in [12].


6   Conclusions
We have presented a method that generates invariants by solving for their coeﬃ-
cients directly. This is in contrast to traditional methods, which work iteratively
toward a ﬁxed point. The method generates constraints using Farkas’ Lemma.
Theoretically, the method is sound and complete, guaranteeing that any linear
invariant of a linear program which is provable using an inductive linear assertion
can be be found using our approach.
    The main drawback of the method is that it produces non-linear constraints.
As a result, while the technique can be applied to generate subtle invariants for
small systems, its applicability to larger systems is limited. We are conﬁdent
that, as the state of art in non-linear constraint solving advances, our method
will become more and more practical.


References
 1. F. Besson, T. Jensen, and J.-P. Talpin. Polyhedral analysis of synchronous lan-
    guages. In Static Analysis Symposium, SAS’99, Lecture Notes in Computer Science
    1694, pages 51–69, 1999.
 2. A. Bockmayr and V. Weispfenning. Solving numerical constraints. In A. Robinson
    and A. Voronkov, editors, Handbook of Automated Reasoning, volume I, chapter 12,
    pages 751–842. Elsevier Science, 2001.
 3. E.M. Clarke. Synthesis of resource invariants for concurrent programs. In ACM
    Principles of Programming Languages, pages 211–221, January 1979.
 4. G. E. Collins and H. Hong. Partial cylindrical algebraic decomposition for quan-
    tiﬁer elimination. Journal of Symbolic Computation, 12(3):299–328, sep 1991.
 5. G.E. Collins. Quantiﬁer elimination for real closed ﬁelds by cylindrical algebraic
    decomposition. In H.Brakhage, editor, Automata Theory and Formal Languages,
    volume 33 of LNCS, pages 134–183, 1975.
432     Michael A. Colón, Sriram Sankaranarayanan, and Henny B. Sipma

 6. P. Cousot and R. Cousot. Abstract Interpretation: A uniﬁed lattice model for
    static analysis of programs by construction or approximation of ﬁxpoints. In ACM
    Principles of Programming Languages, pages 238–252, 1977.
 7. P. Cousot and N. Halbwachs. Automatic discovery of linear restraints among the
    variables of a program. In ACM Principles of Programming Languages, pages
    84–97, January 1978.
 8. A. Dolzmann and T. Sturm. REDLOG: Computer algebra meets computer logic.
    ACM SIGSAM Bulletin, 31(2):2–9, June 1997.
 9. K. Fukuda and A. Prodon. Double description method revisited. In Combinatorics
    and Computer Science, volume 1120 of LNCS, pages 91–111. Springer-Verlag, 1996.
10. N. Halbwachs and Y.-E. Proy. POLyhedra desK cAlculator (POLKA). VERIMAG,
    Montbonnot, France, September 1995.
11. N. Halbwachs, Y.E. Proy, and P. Roumanoﬀ. Veriﬁcation of real-time systems
    using linear relation analysis. Formal Methods in System Design, 11(2):157–185,
    1997.
12. T.A. Henzinger and P.-H. Ho. Model-checking strategies for hybrid systems. In
    Conference on Industrial and Engineering Applications of AI and Expert Systems,
    1994.
13. T.A. Henzinger and P.-H. Ho. Algorithmic analysis of nonlinear hybrid systems. In
    P. Wolper, editor, Computer-Aided Veriﬁcation, LNCS 939, pages 225–238. 1995.
14. H. Hong. RISC-CLP(Real): Constraint logic programming over real numbers. In
    CLP: Selected Research. MIT Press, 1993.
15. J. Jaﬀar and J.-L. Lassez. Constraint logic programming. In Principles of Pro-
    gramming Languages(popl), pages 111–119, January 1987.
16. Z. Manna and A. Pnueli. Temporal Veriﬁcation of Reactive Systems: Safety.
    Springer-Verlag, New York, 1995.
17. A. Schrijver. Theory of Linear and Integer Programming. Wiley, 1986.
18. A. Tarski. A decision method for elementary algebra and geometry. Univ. of
    California Press, Berkeley, 5, 1951.
19. V. Weispfenning. Quantiﬁer elimination for real algebra—the quadratic case and
    beyond. In Applied Algebra and Error-Correcting Codes (AAECC) 8, pages 85–101,
    1997.
20. N. Wirth. Algorithms + Data Structures = Programs. Prentice-Hall, 1976.
21. R. Zippel. Eﬀective Polynomial Computation. Kluwer Academic Publishers,
    Boston, 1993.
