     Formal Verification of Station Keeping Maneuvers for a
              Planar Autonomous Hybrid System

                              Benjamin Martin                               Khalil Ghorbal
                       LIX, Ecole Polytechnique, CNRS                       INRIA, Rennes,
                    Université Paris-Saclay, 91120 Palaiseau,                 France
                                      France                          khalil.ghorbal@inria.fr
                     bmartin@lix.polytechnique.fr

                           Eric Goubault                                     Sylvie Putot
                   LIX, Ecole Polytechnique, CNRS                   LIX, Ecole Polytechnique, CNRS
                Université Paris-Saclay, 91120 Palaiseau,       Université Paris-Saclay, 91120 Palaiseau,
                                  France                                           France
                 goubault@lix.polytechnique.fr                      putot@lix.polytechnique.fr




       We formally verify a hybrid control law designed to perform a station keeping maneuver for a planar
       vehicle. Such maneuver requires that the vehicle reaches a neighborhood of its station in finite time
       and remains in it while waiting for further instructions. We model the dynamics as well as the control
       law as a hybrid program and formally verify both the reachability and safety properties involved. We
       highlight in particular the automated generation of invariant regions which turns out to be crucial
       in performing such verification. We use the theorem prover Keymaera X to discharge some of the
       generated proof obligations.




1    Introduction

Formal hybrid modelling languages such as hybrid automata [1] or hybrid programs [12] offer a conve-
nient way to describe a wide variety of hybrid systems. In this paper, we consider a piecewise continuous
system where the continuous dynamics are subject to discrete switching. The plant part is modeled as a
Dubins vehicle, that is a vehicle describing planar circular curves at a constant speed. The heading of the
vehicle respects a hybrid control law, here taken from [8], designed for station keeping maneuver. This
means that the vehicle is expected to reach a neighborhood of its station in finite time and remains in it as
long as it is not asked to do differently. Possible applications for such maneuvers are e.g. an autonomous
sailboat that needs to anchor around a GPS position waiting to be picked up, or an autonomous drone
that needs to keep a station at a given position while waiting for further instructions.
    Our goal is to formally verify the given control law while investigating to which extent such verifica-
tion could be automated. In particular, we use recent symbolic computation techniques to automatically
generate algebraic and semialgebraic invariant regions [11, 7]. Such regions are then exploited to for-
mally verify the reachability and safety properties of the station keeping maneuver using the hybrid
theorem prover Keymaera X [4]. We compare our findings with the results from [8] where another proof
is conducted by means of guaranteed numerical methods.

L. Bulwahn, M. Kamali, S. Linker (Eds.): First Workshop on                         c B. Martin et al.
Formal Verification of Autonomous Vehicles (FVAV 2017).                            This work is licensed under the
EPTCS 257, 2017, pp. 91–104, doi:10.4204/EPTCS.257.9                               Creative Commons Attribution License.
92                                                                  Formal Verification of Station Keeping




          Figure 1: Cartesian coordinates (left) and polar coordinates (right). Courtesy to [8].


2    The Station Keeping Maneuver
The Dubins vehicle in Cartesian coordinates is described by the following system:
                                        
                                         ẋ = cos(θ )
                                             ẏ = sin(θ ) ,                                               (1)
                                            θ̇ = u
                                        

where (x, y, θ ) defines the pose of the vehicle composed of its position in the plane (x, y) as well as its
heading angle θ . The vehicle is always moving at a constant speed (here fixed to 1). The variable u
encodes an input control that affects directly the heading’s angular velocity. Following [8], we consider
the above plant model in the polar coordinates (d, ϕ, α) depicted in Figure 1. The above ODE then
becomes:                                  
                                               ˙
                                           d = − cos(ϕ)
                                          
                                              ϕ̇ = sin(ϕ)
                                                        d +u ,                                          (2)
                                           α̇ = − sin(ϕ)
                                          
                                                         d

where radius d is a positive real satisfying d 2 = x2 + y2 and the heading angle θ is linearly related to ϕ
and α: ϕ − θ + α = π. The angle ϕ can be understood as a bearing which measures the angle of the
head of the vehicle with respect to a given position of the plan (here the origin).
     The polar coordinates have in fact numerous advantages over the Cartesian coordinates. On one hand,
one gets a decoupling of the state variables for free since the derivatives of ϕ and d are independent of
α calling for a model reduction where only the states (d, ϕ) are considered. On the other hand, since
ϕ appears only as a direct argument of the sine and cosine functions, one can restrict ϕ to [0, 2π) with
no loss of generality: the vector field is invariant under the action of the transitive additive group that
takes ϕ to ϕ + 2kπ. Recall that the polar coordinates transformation presents a singularity at the origin
(x, y) = (0, 0), where d vanishes. We will go back to this issue later. First, we recall the piecewise control
law for u proposed in [8].
                                       (                              √
                                          1             if cos(ϕ) ≤ 22
                                  u=                                       ,                               (3)
                                          − sin(ϕ)      otherwise
B. Martin et al.                                                                                                93


    The intuition is√that the vehicle constantly turns left when it is not pointing towards the origin (mod-
elled by cos(ϕ) ≤ 22 ), otherwise the input is proportional to the bearing ϕ so as to push it towards 0, in
which case the vehicle is moving towards the origin.
    Combining the control law (3) together with the plant in polar coordinates (2), one gets a switched
system where two different dynamics, implied by two different controls, can be applied depending on
the state of the system.
    In the following sections we prove that (i) the vehicle reaches in a finite time a position at a reasonably
short distance from a beacon positioned at the center of the coordinate system, and (ii) stays in that region
for an indefinite time. To do so, we first perform a qualitative analysis of the two continuous dynamics
obtained exhibiting interesting invariant regions.


3    Generating Positive Algebraic Invariants
For convenience, we recall the formal definition of positive invariant sets. Let φ (x0 , .) : R → Rn denote
the solution of the initial value problem ẋ = f (x) for a given ODE f and initial value x0 . Let I ⊂ R
denote the maximal interval on which φ (x0 , .) is defined. Recall that I need not be the entire real line and
that, depending on f , the solution may be defined on a bounded interval. When I is bounded, the system
exhibits a finite time blow-up problem [2], that is in general at least one variable diverges in finite time.
Such problems are intimately related to the singularities of the solutions and are often hard to detect and
characterize. We will carefully discuss and analyze such issues for our case study. Notice, however, that
to the best of our knowledge there are currently no automated methods to detect whether I is bounded or
not where non-linear dynamics are involved (when f is linear, I = R).
Definition 1. A set S ⊆ Rn is positive invariant for f if and only if for any x0 ∈ S, the corresponding
solution φ (x0 , ·) satisfies φ (x0 ,t) ∈ S for all t ∈ [0, +∞) ∩ I, that is for all non-negative time t as long as
the solution is defined.
     In order to verify that a set S is positive invariant for an ODE, it is enough to show that the flow f is
entering, constant or inner tangential on the boundaries of S. When S is semi-algebraic (that is defined by
boolean combinations of polynomial equalities and inequalities), this can be done by checking the sign
of the Lie derivatives (and, if necessary, higher-order Lie derivatives) of the active boundaries of S [9].
     Recently in [11, 5, 9, 14, 7], many effective methods for constructing algebraic and semi-algebraic
positive invariant sets have been proposed. Those methods apply, however, only to polynomial vector
fields. We thus start by transforming the system (2) into a polynomial differential system. This could
be done classically by adding fresh variables corresponding to the transcendental functions. The so
obtained dynamics is a sound approximation (abstraction) of the original dynamics that one could refine
by re-introducing the links between the extra variables and the hidden transcendental functions they
represent [3]. For our dynamics, one obtains the following algebraic system :
                                           
                                           
                                               ġ = −(he + u)h
                                            ḣ = (he + u)g
                                           
                                           
                                                ė = ge2            ,                                      (4)
                                           
                                           
                                               d˙ = −g
                                           
                                               ϕ̇ = he + u
                                           

where the variable g encodes cosine function cos(ϕ), h the sine function sin(ϕ) and e the inverse d1 . For
the abstraction to be precise enough, one has to respect those functions initially, for instance if the initial
94                                                                    Formal Verification of Station Keeping


                           Control          Darboux Polynomial              Cofactor
                                                    e                           ge
                            u=1
                                                 1 + 2eh                       2ge
                                                    e                           ge
                           u = −h
                                                    h                       (e − 1)g

                                 Table 1: Darboux polynomials for Eq. (4).

values of g and h are fixed, then the initial value of φ is entirely determined. Likewise, if d is fixed
initially, then the initial value of e is fixed and is equal to the inverse of d. In this case study, the control
law u, as well as the switching conditions (cf. (3)), are expressible directly with the extra variables g, h,
and e. Therefore, the control law as well as the plant could be rewritten entirely algebraically.

Darboux polynomials and positive invariants Darboux polynomials, and more generally the Dar-
boux criterion, are fundamental building blocks for the qualitative analysis of ODE and hence invariant
generation. They are also at the heart of symbolic integration methods [6, 10].
Definition 2. Let ẋ = f (x) denote an ODE. A polynomial p is Darboux for f if and only if

                                                    ṗ = cp

where c ∈ R[x] is a polynomial, called cofactor and where ṗ denotes the time derivative of the polynomial
p with respect to f .
     The polynomial ṗ is also known as the Lie derivative of p with respect to f and is formally defined
as
                                                   h∇p, f i ,
where ∇p is the gradient of p and h., .i is the standard inner product on Rn .
      Searching for Darboux polynomials, up to a given fixed degree, can be performed algorithmically
[11, 5] by deriving all the constraints that the unknown coefficients of a polynomial (or template) have
to satisfy and then solve the so obtained system.
      We were able to exploit such techniques to automatically generate Darboux polynomials of Eq. (4).
For a better performance, we restricted ourselves to the three dimensional dynamics in (g, h, e) since they
define a closed form ODE on their own. Table 1 summarizes our findings depending on the selected con-
trol. From there, we recovered other Darboux polynomials for the five dimensional system by exploiting
the algebraic invariant de = 1 known to be satisfied by construction.
      From Table 1, in the constant control mode (u = 1), we observe that the cofactors of the two Darboux
polynomials are the same up to a multiplication by the integer 2. This suggests the following rational
invariant function for this mode:
                                                        1 + 2eh
                                              Vcst :=            ,                                            (5)
                                                           e2
obtained by first matching the two cofactors by raising the power of the Darboux polynomial e to match
the multiplicative integer 2 (since the cofactor of e2 is twice the cofactor of e) and then dividing the two
Darboux polynomials with the same cofactor, namely 1 + 2eh and e2 . Such relation between Darboux
polynomials and rational invariant functions is well known in the literature [6]. One can indeed easily
check that the Lie derivative of Vcst vanishes for all t, that is V̇cst = 0, as long as the control input remains
equal to 1. Moreover, since de = 1 by construction of e, we have a polynomial equivalent formula for
Vcst , namely d 2 + 2dh.
B. Martin et al.                                                                                          95


                                              ������������ �������
                       ���




                       ���




                       ���




                       ���
                   �




                       ���




                       ���




                       ���
                               ���      ���     ���      ���      ���     ���      ���

                                                         φ

                              Figure 2: The set Vcst ≤ 0 is depicted in blue.


    For the proportional mode, when u = −h, it turns out that the time derivative of Vcst keeps a constant
sign:
                                                2g(h + 1)
                                      V̇cst = −           ≤0 .
                                                    e
                                                                                  √
This is because h + 1 ≥ 0 (recall that h is defined as a sine function) and g > 22 by definition of g and
the considered control law (3).
     Figure 2 shows the region Vcst ≤ 0 (depicted in blue). Observe in particular that it contains the
equilibrium of the system (d, ϕ) = (1, 3π  2 ) and that d is upper bounded by 2, meaning that the vehicle is
at a fairly close distance to the origin of the Cartesian coordinate system. Thus, the set Vcst ≤ 0 seems to
be a good station keeping candidate for the switched system.
     In the next sections, we formally prove that Vcst ≤ 0 is an invariant set for the switched system and
more importantly that it is reachable from any initial condition of the vehicle provided that initially d > 0
and ϕ 6= 0.


4    Safety Analysis
In this section, we will first model the switched system as a hybrid program, then prove the invariance of
Vcst ≤ 0.
96                                                                          Formal Verification of Station Keeping


Definition 3 (Hybrid Program Model).
                 nn                         √ o n                         √ oo∗
            α :=    Plant|u=1 & d > 0 ∧ 2g ≤ 2 ∪ Plant|u=−h & d > 0 ∧ 2g > 2

where the Plant dynamics are defined as in (4).
     The hybrid program α in Definition 3 shows a piece-wise continuous system that models the behavior
of the vehicle when the control law is applied. The entire feedback loop runs for any non-negative number
of iterations, modeled by the star {}∗ . The loop is made of an non-deterministic choice (modelled by the
operator ∪) between the dynamics induced by the two possible controls (Plant|u=1 and Plant|u=−h ). Any
dynamics are applied as long as the states remains within the evolution domain given by the conditions
after the & symbol. Here, the different conditions on g imposes to follow the control law given by (3).
The condition d > 0, present in both evolution domains, ensures that the polar coordinates rewriting is
valid.
     In the sequel, we will be using ∆ := g2 + h2 = 1 ∧ ed = 1 ∧ d > 0 to encode the fact that the initial
                                                                        

value of the variables (g, h, ϕ, d, e) is coherent, that is once g and h are fixed such that g2 + h2 = 1,
ϕ ∈ [0, 2π[ is known and is such that cos(ϕ) = g and sin(ϕ) = h, although its value is not given explicitly.
The variable e is entirely determined via the equation de = 1 as soon as a positive d is chosen. We are
now ready to formally state the positive invariance of the region Vcst ≤ 0.
Theorem 1 (Vcst ≤ 0 is a Positive Invariant).

                                            Vcst ≤ 0 ∧ ∆ → [α] Vcst ≤ 0

     The box modality around α means that for all runs of the hybrid program, the following post-
condition must be true. When Theorem 1 is written as a hybrid program in Keymaera X1 , we use the
polynomial form of Vcst = d 2 + 2dh, which is a valid rewriting of the rational form if de − 1 = 0 is an
invariant of the hybrid system. If one assumes that de − 1 = 0 holds initially (as this is the case here) then
it is possible to prove that it holds for all time. Indeed the polynomial de − 1 is a Darboux polynomial
for the dynamics defined in (4) for all inputs u. This fact cannot be proved currently within the theorem
prover Keymaera X as a proof rule based on the Darboux criterion is not yet available. Therefore, it
is currently necessary to add the conditions de − 1 = 0 into the evolution domain in order to complete
the proof in Keymaera X. The proof itself then is mostly based on the differential invariant (DI) proof
rule [12], which is essentially a conservative lifting of barrier certificates [13] to the boolean connec-
tives. For convenience, we give in Eq. (6) the conditions required for barrier certificates, or likewise the
premises of the proof rule DI for the simple case of region of the form p ≤ 0.

                                                   ∀x.([x0 := f (x)] ṗ ≤ 0)
                                         (DI)                                                                       (6)
                                                p ≤ 0 → [ẋ = f (x)&H]p ≤ 0

In other words, the invariance of p ≤ 0 can be deduced  √     if its time (Lie) derivative is negative. The
reason (DI) succeeds is due to the fact that when g > 22 and the proportional control is applied, one gets
V̇cst = −2gd(h + 1), which is negative since g is positive, d is positive, and h, as a cosine, is greater or
equal to −1. The set Vcst ≤ 0 is thus not only a positive invariant when the constant control is applied but
also for the proportional control when applied according to the control law Eq. (3). The output obtained
with Keymaera X is shown on Fig. 3.
     1 Source files for this hybrid program are available at the following link http://ben-martin.fr/publications
B. Martin et al.                                                                                        97




           Figure 3: Keymaera X: last window showing the proof of Theorem 1 is concluded.


5     Reachability Analysis
We prove in this section that the region Vcst ≤ 0 is reachable from (almost) anywhere in the phase space.
We use the same hybrid program model given in Definition 3. We first discuss the special case ϕ = 0
(Section 5.1), and then the generic case where ϕ > 0 (Section 5.2).


5.1   The Special Case (ϕ = 0)
When ϕ = 0 initially, then g and h have to be instantiated to 1 and 0 respectively. This configuration sets
the control input u to −h and one can see from Table 1 that h is a Darboux polynomial and therefore
h = 0 is an invariant equation as long as the system evolves following the Plant equations (cf. (4)) with
the domain d > 0. In this particular case, and since h = 0 is invariant, the set of equations simplifies to
                                            
                                            
                                              ġ   =   0
                                             ḣ    =   0
                                            
                                            
                                               ė   =   e2 ,                                           (7)
                                            
                                            
                                             d ˙   =   −1
                                            
                                                    =   0
                                            
                                              ϕ̇
98                                                                  Formal Verification of Station Keeping


meaning that the bearing angle ϕ, as well as its cosine g, will remain constants. Subsequently, this
also means that the control input u will also remain fixed to −h, that is 0. The vehicle shows here an
interesting behavior as the time derivative for d is strictly decreasing: the vehicle is heading straight to
the origin (x, y) = (0, 0). However, because of the evolution domain constraint d > 0, the dynamics will
be followed as long as this constraint is not violated. But then, by design, the system is forced again to
execute the differential equation which only makes d closer and closer to 0 (and thus e closer to infinity
because of ed = 1 is an invariant). We have here in fact a finite time explosion problem: if the system
starts at a distance d0 from the origin, with ϕ0 = 0, the dynamics are only defined for t ∈ [0, d0 [ and the
maximal interval of definition is upper bounded. At t = d0 , the model hits the singularity of the polar
coordinates transformation and it is no longer valid as is. A careful analysis shows that, right after the
singularity, d remains an infinitesimal (and is thus continuous as one expects) and ϕ is discontinuous as
it jumps from 0 to π switching the control input from −h to 1. This discontinuity comes in fact from
switching the direction of the radius vector (of magnitude d) and does affect neither the position nor the
heading of the vehicle. The vehicle follows therefore a new trajectory with d very small but positive and
ϕ = π. This new initial position is part of the generic case discussed in the next section.



5.2   The Generic Case (ϕ > 0)

The phase space is now restricted to (0 < ϕ < 2π). We assume that in this case all trajectories are
defined for all t ≥ 0. Our reachability analysis exploits the recent invariant-based liveness proof rule,
(SP), introduced by Sogokon and Jackson in [15, Proposition 10]. The idea is to use special invariant
sets, so called staging sets, that contains the initial set and from which the system can only escape to go
to the target set one wants to prove reachable. To further prove that the system will eventually leave the
staging set in finite time, a progress function must be also supplied. These two ingredients are sufficient
to prove that any trajectory starting in the staging set will eventually reach the target set in finite time.
The (SP) rule is defined as follows: XT ⊂ Rn is the target set we want to prove reachable in finite time
and X0 ⊂ Rn is the initial set. The premises of the proof rule are sufficient to prove its conclusion under
the assumption that the solution is defined for as long as needed to reach the target set.

                                      ` ∃ε > 0. ∀x. S → (p ≥ 0 ∧ ṗ ≤ −ε)

                       X0 ∧ ¬XT ` S      ` S → [ẋ = f (x) & ¬(H ∧ XT )]S      X0 ∨ S ` H
                (SP)                                                                                     (8)
                                          ` X0 → hẋ = f (x) & HiXT

The diamond modality around the hybrid program means that at least one run leads to satisfying the post-
conditions (liveliness). The proof rule has four premises and relies essentially on a strictly decreasing
progress function p within an invariant set S. The progress of p is proven using the positive real number
ε. The intuition of the proof rule (SP) is that if there exists a bounded from below and decreasing function
along the trajectories in an invariant region with respect to certain evolution domain constraint, then the
flow cannot stay indefinitely inside and must eventually exit the region described by those constraints.
     The aim of this section is to prove that the region defined by Vcst ≤ 0 is reachable from any generic
initial position (i.e. excluding the case ϕ = 0). Doing so with a single application of the (SP) rule
can be cumbersome. Therefore, we suggest to build a chain of staging sets that prove reachability of
intermediate regions, the chain leading to the reachability of Vcst ≤ 0. In what follows, we partition the
B. Martin et al.                                                                                        99


                                                ���������� �������
                       �




                       �


                               1                       2                           3

                       �
                   �




                       �




                       �                                               4




                       �
                           �       �        �          �        �          �        �

                                                           φ

Figure 4: Phase space of the controlled Dubins vehicle in polar coordinates. The black curve shows a
possible trajectory of the vehicle until reaching Vcst ≤ 0 (region Ã). When the vehicle is in regions À or
Â, u = 1; In region Á u = −h.

phase space into 4 regions as shown in Fig. 4:
                                                 π
                                   À := 0 < ϕ <     ∧ d>0
                                                 4
                                        π         7π
                                   Á := ≤ ϕ ≤         ∧ d > 0 ∧ Vcst > 0
                                        4          4                                                   (9)
                                        7π
                                   Â :=      < ϕ < 2π ∧ d > 0 ∧ Vcst > 0
                                         4
                                   Ã := Vcst ≤ 0
 This partition has been found manually by separating the regions with different control and the region
found safe in the previous section. We prove sequentially that Á can be reached from À, Â can be
reached from Á and that Ã can be reached from Â.
Lemma 1.            √                 !                                √       √ !
                     2                                                  2       2
                       < g ∧ h > 0 ∧ ∆ → h Plant|u=−h i             g=    ∧ h=
                    2                                                  2       2
                                                                           √
Proof. Apply the proof rule (SP) with the progress function p := d, ε := 22 and the invariant set S := X0 .
100                                                                 Formal Verification of Station Keeping


All premises can be checked automatically. The first, second and fourth premises can be discharged using
a quantifier elimination procedure over the reals (CAD for instance). The most involved premise is the
third one where one has to prove the invariance of the staging set S. As shown in [9] this can be also
reduced to a universal quantifier elimination problem and can thus be discharged using CAD.

   Prop. 1 exhibits a particular run of the hybrid program α in which it reaches the bearing angle ϕ = π4
from any coherent initial position satisfying ϕ ∈ (0, π4 ).
Proposition 1.                              π            π
                                      0 < ϕ < ∧ ∆ → hαi ϕ =
                                             4              4
                                             √
Proof. When ϕ ∈ (0, π4 ) initially then g > 22 and the control input u is set to −h. According to Lem. 1,
and since d > 0 is a positive invariant, ϕ = π4 is reachable by continuously following the dynamics while
         √ −h. This is allowed by the control law since, as long as the system evolves within the staging
fixing u to
set, g > 22 is satisfied.

      Similarly, we prove that region Â is reachable from Á by exhibiting a run of α that reaches the region
Á.
Lemma 2.                  √                !                         √          !
                           2                                          2
                       g≤    ∧ Vcst > 0 ∧ ∆ → h Plant|u=1 i             <g ∧ h<0
                          2                                          2

Proof. Apply the proof rule (SP) with the progress function p := −ϕ + 7π             1
                                                                            4 , ε := 2 and the invariant set
S := X0 . To prove that S → p ≥ 0, we need to use the fact that (g, h) = (cos(ϕ), sin(ϕ)). The proof is not
involved but has to be done manually as it requires manipulating transcendental functions.

Proposition 2.                                                        
                            π      7π                        7π
                              ≤ϕ ≤    ∧ Vcst > 0 ∧ ∆ → hαi      < ϕ < 2π
                            4       4                         4
      Finally, we prove the reachability of the invariant set Ã from Â.
Lemma 3.                √                            !
                         2
                           < g ∧ h < 0 ∧ Vcst > 0 ∧ ∆ → h Plant|u=−h i (Vcst ≤ 0)
                        2
                                                                              √
Proof. Apply the proof rule (SP) with the progress function p := d, ε := 22 and the invariant set S :=
X0 .

Proposition 3.                                            
                                 7π
                                    < ϕ < 2π ∧ Vcst > 0 ∧ ∆ → hαi (Vcst ≤ 0)
                                  4
      Combined together, Propositions 1, 2 and 3 give:
Theorem 2 (Reachability of Vcst ). The region Vcst ≤ 0 is reachable from any coherent generic position:

                                     (0 < ϕ < 2π ∧ ∆) → hαi (Vcst ≤ 0)
B. Martin et al.                                                                                         101


    The proof rule (SP) is not yet available in Keymaera X. All the premises can be however discharged
using a quantifier elimination procedure, including the invariance of the staging set S. The latter is a
direct consequence of the decidability of the invariance of semialgebraic sets [9]. We used our proper
implementation of the procedure described in [9] together with the Reduce procedure in Wolfram Math-
ematica to discharge all the premises of the (SP) proof rule, except for Lem. 2 where transcendental
functions are involved.
Remark 1. Theorem 2 tells nothing about the time required to reach the target set, only that this time is
finite. The rule (SP) embeds, however, a bounded progress function which can be used to determine an
upper bound on the time required to reach the target region. For example starting at (ϕ0 , d0 ) in region À
(d > 0), and given the upper bound√ on the decrease of the progress function d, we can conclude that the
region Á is entered in at most at 2d0 seconds. The quality of this upper bound depends on the positive
bound used for the progress function and can thus be arbitrarily large (but always finite). Notice that
a finer analysis for the time spent at a given traversed region would benefit from a lower bound of the
progress function, although such bound is not required for proving the reachability itself.
Remark 2. There exists in fact an attractor for the switched system that is inside Vcst ≤ 0, namely
Vcst ≤ − 12 . However, proving its reachability is much more involved than proving the reachability of
Vcst ≤ 0, because a trajectory mayhloop for i some time before reaching it. It also features a sliding
                                                                                                     mode  
                        7π           1                                                               7π √1
at the boundary ϕ = 4 for d in      √
                                      2
                                        , 1  . In fact the only entry to the attractor is the point   4 , 2
which is reached whenever the system enters its sliding mode. Notice also that when the system loops
around this attractor, one has to consider roots of the Lambert W function. We do not carry such proof
in Keymaera X, however, since Vcst ≤ 0 is sufficient to prove that the maneuver reaches a region close to
the origin. (see Fig. 5).


6    Related Work
An interval-based numerical approach has been proposed in [8] to validate the controller. The idea
is to construct a discrete abstraction of the state space of the system and then to build a graph where
nodes correspond to discrete regions and transitions between nodes mean that the system can potentially
move from one region to the other. To actually build such transitions, the author considered guaranteed
numerical tests based on interval analysis. This final graph was then used to show that the vehicle will
be eventually trapped in a limited region of the state space. By construction, such a region is an over-
approximation of the actual attractor of the system. This region is not precisely given in [8] but it can be
approximated by the following set:

                         (0 ≤ d ≤ 2) ∨
                                                                   
                                      π 7π
                              0≤ϕ ≤ ∨        ≤ ϕ ≤ 2π ∧ 0 ≤ d ≤ 7.6 ∨
                                      6    4
                                                                          
                           π         7π                 112
                              ≤ϕ ≤      ∧ 2 ≤ d ≤ 7.6 ∧     ϕ − 25d − 6 ≥ 0 .
                            2         4                  π
In comparison, the zero level set of Vcst describes more accurately the behavior of the system, entailing a
sharper analysis. Fig. 6 depicts the attractor from [8] in comparison to the ones found in this paper. It is
worth noting that the method from [8] does not require the algebraic rewriting. It works directly with the
original system in polar coordinates and uses guaranteed numerical computations to find the invariant
set. As in our approach, however, finding invariant candidates was essentially manual.
102                                                                Formal Verification of Station Keeping


                                               ������� ���������
                      ���



                      ���



                      ���



                      ���
                  �




                      ���



                      ���



                      ���



                      ���
                                      �              �              �               �

                                                         φ

Figure 5: The refined invariant of the controlled vehicle. The red segment shows the sliding mode region
before entering the attractor. The black curve shows a possible looping trajectory around the attractor.
The region Vcst ≤ 0 is shown in purple for convenience.


7     Discussion and Conclusion
We have developed a formal proof for the safety and liveness of an autonomous switched system, corre-
sponding to a planar Dubins car whose goal is to perform a station keeping maneuver around the origin.
This proof can be synthesized in three steps. First, we have used recent algebraic methods to derive
algebraic invariant properties for the switched system. In particular, an algebraic invariant region, corre-
sponding to a station keeping behavior, has been identified and formally checked with the hybrid system
theorem prover Keymaera X. Second, the unbounded time reachability analysis of the system has been
performed. To do so, the phase space was partitioned into subregions, each equipped with a progress
function to prove that the system eventually leaves the region. To complete the proof, we exploited the
invariants we generated to show that a region is only exited at certain locations.
    Although this case study appears simple, this formal proof relies on non-trivial elements in particular
for the reachability analysis. We believe, however, that the current state-of-the-art techniques and tools
are mature enough to handle such the proof obligations for such case study (up to properly implementing
the used proof rules in a theorem prover like Keymaera X). Some questions remain about how far can
the application of these tools be automatized. For example, we were required to decompose the state
space for the proof of reachability. The decomposition is obtained by hand from the autonomous system
B. Martin et al.                                                                                            103


                                                  Comparison of invariants
                        10




                         8




                         6
                    d




                         4




                         2




                         0
                             0      1         2            3           4     5          6

                                                               j


    Figure 6: In gray the invariant region obtained in [8], in purple Vcst ≤ 0 and in green Vcst ≤ − 12 .


itself and the invariant found for the safety proof. We can think that for other applications, such a
decomposition could be partially inferred automatically in a similar manner.
     Another challenging future work avenue we are keen to investigate is the interaction between the
formal proof process and the design of the control law. For instance, how can one derive a feedback for
the designer when the proof fails ? This becomes more intricate when the proof strategy proceeds by
sufficient conditions not by equivalences, as for reachability. A promising direction would be to direct
the design so as to ease the generation of suitable differential variants/invariants sets (e.g. using Darboux
polynomials), like for control Lyapunov functions.


Acknowlegments
This work is partially supported by the DGA / MRIS under the project “Sureté de Fonctionnement des
Systèmes Robotiques Complexes” and by the Academic and Research Chair “Engineering of Complex
Industrial Systems”, sponsored by Thales, Naval Group, Dassault Aviation and DGA.


References
 [1] Rajeev Alur, Costas Courcoubetis, Thomas A Henzinger & Pei-Hsin Ho (1993): Hybrid automata: An
     algorithmic approach to the specification and verification of hybrid systems. In: Hybrid systems, Springer,
104                                                                    Formal Verification of Station Keeping


      pp. 209–229, doi:10.1007/3-540-57318-6 30.
 [2] John M. Ball (1978): Finite Time Blow-Up in Nonlinear Problems. In Michael G. Crandall, editor: Nonlinear
     Evolution Equations, Academic Press, pp. 189 – 205, doi:10.1016/B978-0-12-195250-1.50015-1.
 [3] David C. Carothers, G. Edgar Parker, James S. Sochacki & Paul G. Warne (2005): Some properties of solu-
     tions to polynomial systems of differential equations. Electronic Journal of Differential Equations 2005(40),
     pp. 1–17.
 [4] Nathan Fulton, Stefan Mitsch, Jan-David Quesel, Marcus Völp & André Platzer (2015): KeYmaera X: An
     Axiomatic Tactical Theorem Prover for Hybrid Systems. In Amy P. Felty & Aart Middeldorp, editors: CADE,
     LNCS 9195, Springer, pp. 527–538, doi:10.1007/978-3-319-21401-6 36.
 [5] Khalil Ghorbal & André Platzer (2014): Characterizing Algebraic Invariants by Differential Radical Invari-
     ants. In: TACAS, Springer, pp. 279–294, doi:10.1007/978-3-642-54862-8 19.
 [6] Alain Goriely (2001): Integrability and Nonintegrability of Dynamical Systems. Advanced Series in Nonlin-
     ear Dynamics, World Scientific, doi:10.1142/3846.
 [7] Eric Goubault, Jacques-Henri Jourdan, Sylvie Putot & Sriram Sankaranarayanan (2014): Finding non-
     polynomial positive invariants and Lyapunov functions for polynomial systems through Darboux polyno-
     mials. In: 2014 American Control Conference, pp. 3571–3578, doi:10.1109/ACC.2014.6859330.
 [8] Luc Jaulin (2013): Outer Approximation of Attractors Using an Interval Quantization. Reliable Computing
     19, pp. 261–273.
 [9] Jiang Liu, Naijun Zhan & Hengjun Zhao (2011): Computing semi-algebraic invariants for polynomial dy-
     namical systems. In: EMSOFT, ACM, pp. 97–106, doi:10.1145/2038642.2038659.
[10] Yiu-Kwong Man (1993): Computing Closed Form Solutions of First Order ODEs Using the Prelle-Singer
     Procedure. J. Symb. Comput. 16(5), pp. 423–443, doi:10.1006/jsco.1993.1057.
[11] Nadir Matringe, Arnaldo Vieira Moura & Rachid Rebiha (2010): Generating Invariants for Non-linear Hy-
     brid Systems by Linear Algebraic Methods. In: SAS, LNCS 6337, Springer, pp. 373–389, doi:10.1007/978-
     3-642-15769-1 23.
[12] André Platzer (2008): Differential Dynamic Logic for Hybrid Systems. J. Autom. Reasoning 41(2), pp.
     143–189, doi:10.1007/s10817-008-9103-8.
[13] Stephen Prajna & Ali Jadbabaie (2004): Safety Verification using Barrier Certificates. In: HSCC, LNCS
     2993, Springer, pp. 477–492, doi:10.1007/978-3-540-24743-2 32.
[14] Sriram Sankaranarayanan (2010): Automatic invariant generation for hybrid systems using ideal fixed points.
     In: HSCC, pp. 221–230, doi:10.1145/1755952.1755984.
[15] Andrew Sogokon & Paul B. Jackson (2015): Direct Formal Verification of Liveness Properties in Continuous
     and Hybrid Dynamical Systems. In: FM, LNCS 9109, Springer, pp. 514–531, doi:10.1007/978-3-319-19249-
     9 32.
