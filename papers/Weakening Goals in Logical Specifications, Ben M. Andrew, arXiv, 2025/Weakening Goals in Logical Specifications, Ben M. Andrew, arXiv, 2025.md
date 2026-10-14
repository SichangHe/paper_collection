                                               Weakening Goals in Logical Specifications

                                                                         Ben M. Andrew

                                                             University of Manchester, Manchester, UK
                                                               benjamin.andrew@manchester.ac.uk
arXiv:2510.15718v1 [cs.LO] 17 Oct 2025




                                               Abstract. Logical specifications are widely used to represent software
                                               systems and their desired properties. Under system degradation or en-
                                               vironmental changes, commonly seen in complex real-world robotic sys-
                                               tems, these properties may no longer hold and so traditional verification
                                               methods will simply fail to construct a proof. However, weaker versions
                                               of these properties do still hold and can be useful for understanding the
                                               system’s behaviour in uncertain conditions, as well as aiding composi-
                                               tional verification. We present a counterexample-guided technique for
                                               iteratively weakening properties, apply it to propositional logic specifi-
                                               cations, and discuss planned extensions to state-based representations.


                                         1   Introduction
                                         Software systems, along with properties that we are interested in proving about
                                         them, are often specified in logics such as first-order or temporal logic. Many
                                         verification techniques exist for automatically checking whether desired prop-
                                         erties hold in a system, but in complex systems that interact with the real
                                         world, unexpected environmental conditions or system degradation can cause
                                         these properties to no longer hold [9].
                                              In these cases traditional formal verification techniques will simply report
                                         property violations, leaving us unable to say anything about the system’s be-
                                         haviour. However, for many applications we may be interested in weakened forms
                                         of the property that do hold in the system.
                                              As an example, consider a quadrotor drone that we have proven can only
                                         safely land when the wind speed is below a certain threshold, and now imagine
                                         that this property does not hold when one of the rotors has failed. There may
                                         still be a weaker version of this property, for example with a lower threshold on
                                         the wind speed, that does hold for the degraded drone. Being able to automat-
                                         ically deduce this weakened property may be crucial for regulatory approval or
                                         understanding how the system properties change under uncertain conditions.
                                              To be precise, a weakening of a property P is any property that speci-
                                         fies a superset of the behaviours of P . For example, we can logically spec-
                                         ify the above example as weakening HighW ind ∨ LowW ind → CanLand to
                                         LowW ind → CanLand. (Note that strengthening the antecedent weakens the
                                         implication.)
                                              Automatic deduction of weakened properties is also useful in compositional
                                         assume-guarantee reasoning [8], where our system is an individual component
2         B.M. Andrew

providing guarantees that feed into the assumptions of other components’ spec-
ifications [11], and aid proofs of the composed system’s global properties.
    This PhD project currently aims to answer two core research questions:
    RQ1: How can a system property, normally holding but invalidated by system
     degradation or environmental changes, be automatically weakened so that it
     both holds in the degraded system and is still useful?
    RQ2: In compositional assume-guarantee reasoning, how does the weakening of
     a component’s guaranteed properties affect other components or system-level
     properties?

Related Work. Goal weakening has been explored in requirements engineer-
ing [12]. However, conflicts are only handled between goals because the weaken-
ing is done at requirements engineering-time, whereas our approach is concerned
with inconsistencies between the requirements and the implementation, which
occur at a later stage in the development lifecycle.
    Belief revision [6] is a technique where a belief set is updated when new
information conflicts with existing beliefs, removing those that conflict. However,
this is a coarse approach that does not weaken the individual beliefs themselves,
and so can be overly conservative.
    Counterexample-guided techniques have been applied to areas like abstrac-
tion refinement [3], inductive synthesis [1], and control [7]. However, they have
not yet been applied to the problem of weakening goals in specifications.


2      Counterexample-Guided Weakening
Our approach finds counterexamples that show that the property doesn’t hold
in the system, integrates them into the property, and repeats. By integrating
counterexamples we iteratively weaken the property until it holds in the system.
     Our algorithm, initially applied to propositional logic, is implemented in
OCaml, using the Why3 [5] platform with Alt-Ergo [4], a tableau-based solver.
The code is hosted publicly on GitHub1 .
     Not all weakenings of the desired property are useful, as evidenced by the
trivial property ⊥ that any system guarantees. Thus, along with our desired
property we also specify a critical property PC that our system must satisfy, as
the minimum weakening of PD that we allow.
     Our specifications are triples ⟨A, PD , PC ⟩ of propositional formulae, where A
represents the internal structure of the system and the environment, PD repre-
sents the desired property of the system, and PC represents the critical prop-
erty of the system. ⟨A, PD , PC ⟩ is well-formed if and only if PD implies PC ,
i.e. PD → PC . We begin the proof process by checking whether the iterative
algorithm is necessary:
 1. Check that A → PD . If true, then finish successfully with PD as the property;
    otherwise,
1
     https://github.com/benmandrew/prop-goal-weakening
                                           Weakening Goals in Logical Specifications         3

 2. Check that A → PC . If false, then finish unsuccessfully, as our critical prop-
    erty does not hold; otherwise,
 3. Find an intermediate property PI between PD and PC such that A → PI .

(By PI being between PD and PC , we mean that PD → PI and PI → PC ,
considering propositional formulae to be partially ordered by implication.)

Algorithm. The algorithm uses a counterexample-guided approach, iteratively
computing counterexamples using a SAT solver and integrating them back into
the candidate property until it is satisfied. It is detailed below as well as in Fig. 1.
    The i-th candidate property is denoted by PIi , for i ∈ N, and we begin by
initialising PI0 = PD . We then construct a formula F (i) that is a conjunction of
the following:

 1. A → PIi , the candidate property must hold in the system,
 2. PD → PIi , the candidate property must be weaker than or equivalent to the
    desired property, and
 3. PIi → PC , the candidate property must be stronger than or equivalent to the
    critical property.

We check the validity of F (i) using a SAT solver. If F (i) is valid, then PIi
holds in the system and we are finished. Otherwise, the SAT solver gives us
a counterexample model that holds in A but does not in PIi . This model may
contain assignments to hidden variables that occur in A but not in PD or PC .
Including them would expose the inner logical workings of the system which may
sometimes be desirable, but for the purposes of overapproximating the weakened
property, we remove all hidden variables from the counterexample.
    From this overapproximated counterexample we construct a formula Ci which
is a conjunction of positive or negative propositional variables. For example, the
model {X = true, Y = false, Z = false} corresponds to the formula X ∧¬Y ∧¬Z.
    The next iteration of the candidate property is then
                                  PIi+1 = PIi ∨ Ci
and we repeat the loop by constructing and checking F (i + 1).




                       i=0                                                yes
 Initialise PI0 = PD         Construct F (i)            Is F (i) valid?         Return PIi



                                                           no
                                     i++          Integrate overapproximated
                                                   counterexample into PIi+1


Fig. 1. Overview of the algorithm, which iteratively weakens the candidate property
PIi until it is satisfied by the system representation A.
4       B.M. Andrew

   The algorithm is complete for systems with finite numbers of variables. As
each step adds at least one complete interpretation to the candidate property,
the number of iterations is bounded by 2N , where N is the number of unique
propositional variables in PD and PC combined.

Example. We use the example from the introduction concerning a quadrotor
drone. Our propositional variables are R4 , that all four rotors work; R3 , that
only three rotors work; WH , that windspeed is high; WL , that windspeed is low;
and L, that the drone can land.
The system is modelled by three assumptions,
             A = R3 ∧ (R4 ∧ (WH ∨ WL ) → L) ∧ (R3 ∧ WL → L)
                |{z}   |       {z        }     |    {z   }
                   (3a)              (3b)                    (3c)

which specify (3a), that only three rotors work (i.e. one rotor has failed); and (3b,
3c), the conditions for the drone being able to land. Our desired goal property
is PD = (WH ∨ WL ) → L, but this is not satisfied by the assumptions, so we
must weaken it. (For the purposes of demonstration we let our critical property
PC = ⊤.)
    We construct the initial F (0) with PI0 = PD , and check for validity with the
SAT solver, receiving a negative answer with the counterexample ¬L ∧ WH ∧
¬WL ∧ R3 ∧ ¬R4 . This counterexample contains the ‘hidden’ variables R3 and
R4 , and as we would prefer not to expose the inner state of our system, we
remove them, resulting in the overapproximated counterexample ¬L∧WH ∧¬WL .
Integrating this into our candidate property results in
                 PI1 = ((WH ∨ WL ) → L) ∨ (¬L ∧ WH ∧ ¬WL )
                      = WL → L
Which is a valid property of the system and so we are done.

3   Future Work
To answer RQ1, we are investigating how to extend weakening to properties
expressed in state-based specification languages, such as as Deterministic Finite
Automata (DFAs), Buchi automata (which commonly correspond with LTL for-
mulae), and Abstract State Machines (ASMs). We are currently exploring how
these properties can be automatically weakened, based on the framework of au-
tomata learning with the L∗ algorithm [2].
    Weakening goals is not the only way to weaken a specification: in contract-
based reasoning [11], strengthening the corresponding assumption serves the
same purpose, and may be a more natural solution for changes in the environ-
ment. This will contribute to answering RQ2. It remains to be seen when this
would be appropriate, and how exactly it would be done.
    It may be more suitable to frame weakening as an interpolation problem [10]
— that is, finding a suitable interpolant between the desired and critical prop-
erties, subject to the constraint of being a valid property of the system. This
approach requires investigation.
                                 Weakening Goals in Logical Specifications   5

References

 [1]   R. Alur, R. Bodik, G. Juniwal, M.M.K. Martin, M. Raghothaman, S.A.
       Seshia, R. Singh, A. Solar-Lezama, E. Torlak, and A. Udupa. “Syntax-
       Guided Synthesis”. In: Formal Methods in Computer-Aided Design. IEEE,
       2013, pp. 1–8. doi: 10.1109/FMCAD.2013.6679385.
 [2]   D. Angluin. “Learning Regular Sets from Queries and Counterexamples”.
       In: Information and Computation 75.2 (1987), pp. 87–106. doi: 10.1016/
       0890-5401(87)90052-6.
 [3]   E. Clarke, O. Grumberg, S. Jha, Y. Lu, and H. Veith. “Counterexample-
       Guided Abstraction Refinement”. In: Computer Aided Verification. Springer,
       2000, pp. 154–169. doi: 10.1007/10722167_15.
 [4]   S. Conchon, A. Coquereau, M. Iguernlala, and A. Mebsout. “Alt-Ergo 2.2”.
       In: International Workshop on Satisfiability Modulo Theories. 2018. url:
       https://inria.hal.science/hal-01960203.
 [5]   J. Filliâtre and A. Paskevich. “Why3 — Where Programs Meet Provers”.
       In: Programming Languages and Systems. Vol. 7792. LNCS. Springer, 2013,
       pp. 125–128. doi: 10.1007/978-3-642-37036-6_8.
 [6]   P. Gärdenfors. Belief Revision. Cambridge Tracts in Theoretical Computer
       Science. Cambridge University Press, 1992. doi: 10.1017/CBO9780511526664.
 [7]   T.A. Henzinger, R. Jhala, and R. Majumdar. “Counterexample-Guided
       Control”. In: Automata, Languages and Programming. Springer, 2003, pp. 886–
       902. doi: 10.1007/3-540-45061-0_69.
 [8]   C.B. Jones. “Tentative Steps Toward a Development Method for Inter-
       fering Programs”. In: ACM Transactions on Programming Languages and
       Systems 5.4 (1983), pp. 596–619. doi: 10.1145/69575.69577.
 [9]   M. Luckcuck, M. Farrell, L.A. Dennis, C. Dixon, and M. Fisher. “Formal
       Specification and Verification of Autonomous Robotic Systems: A Survey”.
       In: ACM Computing Surveys 52.5 (2019), 100:1–100:41. doi: 10 . 1145 /
       3342355.
[10]   K.L. McMillan. “Applications of Craig Interpolants in Model Checking”.
       In: Tools and Algorithms for the Construction and Analysis of Systems.
       Vol. 3440. Springer, 2005, pp. 1–12. doi: 10.1007/978-3-540-31980-1_1.
[11]   B. Meyer. “Applying ‘Design by Contract’”. In: Computer 25.10 (1992),
       pp. 40–51. doi: 10.1109/2.161279.
[12]   A. van Lamsweerde and E. Letier. “Handling Obstacles in Goal-Oriented
       Requirements Engineering”. In: IEEE Transactions on Software Engineer-
       ing 26.10 (2000), pp. 978–1005. doi: 10.1109/32.879820.
