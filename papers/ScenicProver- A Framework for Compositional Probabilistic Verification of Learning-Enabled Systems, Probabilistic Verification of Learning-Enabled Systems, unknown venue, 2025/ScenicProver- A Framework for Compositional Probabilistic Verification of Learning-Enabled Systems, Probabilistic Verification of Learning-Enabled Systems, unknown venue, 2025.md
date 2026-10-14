                                            ScenicProver: A Framework for Compositional
                                         Probabilistic Verification of Learning-Enabled Systems

                                                              Eric Vin1 , Kyle A. Miller1 , Inigo Incer2 ,
                                                              Sanjit A. Seshia3 , and Daniel J. Fremont1
                                                     1
                                                         University of California, Santa Cruz, Santa Cruz CA 95064, USA
                                                               {evin, kymiller, dfremont}@ucsc.edu
arXiv:2511.02164v1 [cs.LO] 4 Nov 2025




                                                             2
                                                                University of Michigan, Ann Arbor MI 48109, USA
                                                                               iir@umich.edu
                                                         3
                                                           University of California, Berkeley, Berkeley CA 94720, USA
                                                                          sseshia@berkeley.edu



                                               Abstract. Full verification of learning-enabled cyber-physical systems (CPS)
                                               has long been intractable due to challenges including black-box components and
                                               complex real-world environments. Existing tools either provide formal guaran-
                                               tees for limited types of systems or test the system as a monolith, but no gen-
                                               eral framework exists for compositional analysis of learning-enabled CPS using
                                               varied verification techniques over complex real-world environments. This paper
                                               introduces ScenicProver, a verification framework that aims to fill this gap. Built
                                               upon the Scenic probabilistic programming language, the framework supports:
                                               (1) compositional system description with clear component interfaces, ranging
                                               from interpretable code to black boxes; (2) assume-guarantee contracts over those
                                               components using an extension of Linear Temporal Logic containing arbitrary
                                               Scenic expressions; (3) evidence generation through testing, formal proofs via
                                               Lean 4 integration, and importing external assumptions; (4) systematic combi-
                                               nation of generated evidence using contract operators; and (5) automatic gen-
                                               eration of assurance cases tracking the provenance of system-level guarantees.
                                               We demonstrate the framework’s effectiveness through a case study on an au-
                                               tonomous vehicle’s automatic emergency braking system with sensor fusion. By
                                               leveraging manufacturer guarantees for radar and laser sensors and focusing test-
                                               ing efforts on uncertain conditions, our approach enables stronger probabilistic
                                               guarantees than monolithic testing with the same computational budget.

                                               Keywords: Compositional Verification · Cyber-Physical Systems · Probabilistic
                                               Programming · Simulation-Based Verification · Interactive Theorem Proving


                                        1   Introduction
                                        Full verification of learning-enabled cyber-physical systems (LE-CPS) has long been
                                        a goal of the formal methods community, but historically has proven intractable for a
                                        variety of reasons. First and foremost is the difficulty in reasoning about black-box or
                                        unstructured components such as machine learning (ML) models [34]. It is also difficult
                                        to model diverse real-world environments in a format that is conducive to existing veri-
                                        fication techniques. Finally, small changes to the system, such as those occurring when
2         E. Vin et al.

an ML component is trained or fine-tuned, can invalidate all analysis done so far [17].
However, these problems primarily arise when treating the system as a monolith, with
the goal of a proof that a specification is satisfied under all possible environments. If one
is willing to relax these assumptions, the problem becomes somewhat more feasible.
    One route is to settle for a weaker guarantee: rather than prove correctness in all
possible environments, we can systematically test the system via falsification [11,22],
obtain a probabilistic guarantee from simulations as in statistical model checking [23],
or even make a reasonable assumption based on manufacturer specifications or real-
world testing [32]. While such evidence of correctness is not as ironclad as a formal
proof, it can still be useful: in fact, such reasoning is commonplace in certification
processes for civil aviation, defense, and safety-critical infrastructure (e.g., FAA DO-
178C [32]). In this context, it is important to reason about the strengths and weaknesses
of the evidence and to present this information clearly to stakeholders.
    Another route is to analyze the system compositionally instead of treating it as a
black box [2,10]. Consider a system being analyzed as a whole via simulation testing to
acquire a probabilistic guarantee of correctness, a potentially expensive and time con-
suming task. Analyzing these results, the developers could make changes to improve
the performance of the system, but these changes could have unknown effect. Con-
sider instead if one analyzed the system compositionally by breaking the system into
components, which would require us only to re-test or verify the components that have
changed. This is especially relevant for learning-enabled components, which may un-
dergo frequent changes (from evolving training data or perhaps learning while active).
Compositional verification still requires creation of the component-level specifications,
either manually (a non-trivial task) or automatically synthesized.
    While many of the techniques above have been applied in isolation, to our knowl-
edge there is no general framework enabling compositional analysis of learning-enabled
CPS using a variety of techniques, from explicit proofs to probabilistic testing, over
complex real-world environments.
    To address this gap, we propose ScenicProver, a verification framework and ac-
companying theory which is capable of all of the above. ScenicProver is implemented
as a tool built on top of the Scenic probabilistic programming language [12,13,40],
leveraging its ability to represent complex environments and test black-box systems,
and supports:

    – Compositionally describing systems with clear interfaces between system com-
      ponents and the outside world. Components can range from fully-interpretable code
      to opaque black boxes.
    – Assume-guarantee contracts for components, using an extension of Linear Tem-
      poral Logic (LTL) [28] with predicates containing arbitrary Scenic expressions that
      can also compare values over time.
    – Generating testing-based evidence that a component satisfies a contract using
      Scenic and a compatible simulator.
    – Using proofs, provided by a user, that a component satisfies a given contract or
      that a contract refines another. We provide an interface to Lean 4 [26], and our
      framework is general enough to add support for other tools in the future.
                                                                     ScenicProver        3

 – Combining contract-evidence pairs to obtain new contracts while tracking what
   evidence supports the new guarantees and how, culminating in the ability to gener-
   ate an overall assurance case for the system.
 – An underlying theory describing how to soundly combine the probabilistic results
   of verifying contracts using contract operators.

    In Section 6, we present a case study of our framework applied to a simplified
automatic emergency braking (AEB) system on an autonomous vehicle with a sensor
fusion system combining surrogates for a radar, laser, and camera. We describe the
whole system inside our framework, and use reasonable assumptions on the radar and
laser system representing manufacturer guarantees to avoid testing a portion of the input
space. We then combine these results, along with a Lean 4 proof of the safety of our
controller and simplified physics assumptions, to show that with high probability, our
system will not get closer than a minimum distance to the car in front of it. We obtain a
stronger result than testing the system as a monolith, for the same computational budget.
This example illustrates that by utilizing designer knowledge of how to split the space
compositionally and leveraging known guarantees, one can significantly outperform
existing techniques for verification of learning-enabled cyber-physical systems in our
framework while still ensuring a sound result.
    The rest of the paper is structured as follows. In Section 2 we introduce a motivating
example that we use throughout the remainder of the paper. In Section 3 we discuss
existing concepts that our framework builds on. In Section 4 we discuss the different
methods of verifying contracts in our framework, leading to a theory of how to soundly
combine those results in Section 5. Finally in Section 6 we return to our motivating
example as a case study, and demonstrate that using our framework provides a stronger
result faster than what is achieved by testing the system as a monolith. Throughout the
paper, proofs are omitted for space, and can be found in the appendices.

Related Work. Our work builds off existing theory and tools for verification of CPS,
compositional verification, contract-based design, and assurance case generation.
    Much existing work has applied testing/falsification-based techniques to the veri-
fication of CPS (see [7] for a survey); almost all of these approaches, including those
based on Scenic [12,11], treat the system as a monolith. Tools like KeYmaera X [14]
and Verse [24] allow the user to explicitly prove properties about hybrid systems by
modeling the controls and physical behavior of a system, but they have limited ability
to represent complicated real-world environments and learning-enabled components.
    Other approaches to verification include runtime enforcement techniques which are
designed to detect and correct invalid behavior, such as shields [3] and the Simplex
architecture [35,36]. There has been significant work on creating and synthesizing run-
time monitors that enforce a given safety property [9,38,44,37]. These techniques are
generally applied to specific portions of a system and it is not trivial to extract system-
level guarantees from them. Instead they are complementary to our approach, and can
be used inside a system being verified by our framework (as we show in Sec. 6).
    Contract-based design [2,20] is a framework that allows for compositional construc-
tion, abstraction, analysis, and verification of systems. In contract-based design, com-
ponents define the behavior and data-flow of a system, and contracts define properties
4       E. Vin et al.

on individual components. Various tools, such as OCRA [5] and Pacti [19], exist for rea-
soning about and manipulating contracts themselves, though they do not have the ability
to reason about whether or not contracts hold over complex learning-enabled systems in
realistic environments. Recent papers describe probabilistic contracts [18,4], extending
existing theory to the probabilistic case in a similar way to our formulation, but concern
themselves primarily with the abstract theory and not the additional elements that our
framework encompasses, such as methods of contract verification, proofs of contract
refinement, heuristics for combining probabilistic contracts, etc.
     Existing work has applied compositional analysis to falsification [10] and verifica-
tion [27,30] of CPS, though not as a general framework that supports arbitrary system
architectures. Existing work has also explored learning contracts over specific portions
of the system [1], or the assumptions for the whole system [33], but again these apply
to specific types of contracts and situations (e.g., contracts over perception components
or assumptions over the whole system).
     Significant work exists on presenting and reasoning about the results of composi-
tional verification [39,29,21,31,43,42], commonly called an assurance or safety case.
Specialized tools such as AdvoCATE [8] have also been used to work with assurance
cases. These are complementary to our work, and could be used to better visualize the
results of our framework.
     To our knowledge no framework has been proposed that supports compositional ver-
ification for CPS with black-box components over complex real-world environments.


2   Motivating Example

We will motivate the utility of our framework with an example which we will refer-
ence throughout the paper and use in our case study. While simplified, this example
includes many elements of real-world systems, including untrusted components, sensor
fusion and robust state estimation for dealing with uncertainty, continuous signals, and
complex dynamics.
    Suppose that we are the manufacturers of an autonomous vehicle that is required by
law to have an Automatic Emergency Braking (AEB) system, for which regulators have
specified minimum standards: the vehicle must never get closer than x meters to the car
in front of it in at least y% of cases with z confidence. We must provide an argument
to regulators for why our system meets this standard (such as an assurance case [32])
before our vehicle is allowed on the road.
    Other manufacturers produce sensors that we plan to use in our system. These sen-
sors have specifications which conform to their own sets of regulations, so we can as-
sume any such specification holds in our argument. In our example, we will utilize two
such sensors whose error is guaranteed to be within a certain bound under certain con-
ditions: a radar distance sensor which has guarantees if the car in front has at least a
certain width, and a laser distance sensor which has guarantees if the atmosphere is
free of occluding particles like rain and snow. Outside of these conditions the sensors
should ideally still provide somewhat reasonable values, but the sensor manufacturers
make no guarantees, so it is our responsibility to ensure the system meets regulator
specifications across actual driving conditions. We also include a third sensor: a ma-
                                                                     ScenicProver       5

chine learning-based camera system which we believe will work well in practice but
for which we have no guarantees.
     We can test our system as a whole in simulation to provide a probabilistic guarantee
of correctness; however, this route does not allow us to make use of the guarantees pro-
vided by the sensor manufacturers, and means that any change to the system invalidates
all of our previous tests. Using our framework, we can do better.
     To begin we will split up our system into discrete components:
 – Perception System: Observes the world using sensors and outputs an estimate of
   the distance to the car in front of us.
 – Control System: Takes in the distance estimate and outputs a throttle signal, indi-
   cating at what level we should accelerate or brake.
 – Vehicle Actuator: Takes in the throttle signal and takes a corresponding action,
   accelerating or braking, in the environment.
Note that each component above might be made of other components. In fact, as a sim-
ple form of sensor fusion we will state that the perception system contains a component
for each sensor listed above and one additional component which returns the median of
their outputs (to reduce noise and errors).
    With this structure in place, we can specify contracts that we want to hold over
each component. Ideally these contracts, when combined, should imply the system-
level specification we care about (i.e., not crashing into the car ahead of us). Logical
contracts for each of our components could be:
 – Perception System: Outputs a distance accurate to within a given error bound.
 – Control System: If the input distance is below a “danger threshold” depending on
   our current speed, the output signal should be to brake fully.
 – Vehicle Actuator: If we brake fully, our speed decreases by a given amount.
We can combine these components to form a component representing the entire car,
with our system-level specification being a contract on this combined component. As-
suming these contracts hold, we can derive an argument showing that we satisfy our
system-level specification of not crashing into the car ahead of us (i.e., the distance is
relatively accurate, so the car brakes, so we slow down, so we don’t hit the lead car).
    At this stage, we must verify that these contracts hold, but we now have more options
than when we viewed the system as a monolith. We may be able to prove the contract on
the control system outright, as it does not depend on the environment. Our contract on
the vehicle actuator corresponds to braking deceleration, a value we may easily be able
to test separately and import into our argument. We could also simply test our contract
on the perception system, but there is a better approach that makes use of the guarantees
we have been provided about the sensors in use. Namely, we could further subdivide
our contract, splitting it into one contract that covers performance under the conditions
our radar and laser sensors are known to work in, and another contract covering all
other conditions. The first contract we can prove, using our sensor assumptions and the
semantics of the median filter, showing that our overall perception system will always
be accurate in those conditions. Therefore, we can avoid testing this contract, and thus
a fraction of the input space, and focus our limited testing budget on the other contract
covering the “unsafe” part of the space. We do exactly this in Section 6, providing a
stronger result than monolithic testing would be able to provide alone.
6       E. Vin et al.

3     Preliminaries: Traces, Components, and Contracts
In this section, we discuss existing concepts that form the backbone of our framework,
and how we have implemented these concepts. These include how we model our system
and the environment, and the ideas underpinning compositional verification including
components and contracts.

3.1   Environment and System Traces
In ScenicProver, values of the system and environment are modeled via traces. A trace
is a finite-length series of states of an environment and system with each value in the
series representing the value at a given discrete timestep.
      A distribution over environments is modeled by the random variable E, which is
defined by a Scenic program (we also refer to E as a scenario). A specific environment
e can be drawn from E with probability P(E = e) (we also refer to e as a scene).
      A component M (discussed in depth in Section 3.2) has a value v, defined to be
the value of all IO and internal state at a given timestep. Note that components are
assumed to be deterministic. A component value v ′ can be retrieved by “running” a
component: v ′ = M(e, v), where v represents the previous state of M and can be
either another component state or null (written ∅), which represents the deterministic
initial state of a component. As we will see later, a component can be composed of
other sub-components, and in this case we recursively define a component value to be
the concatenation of the values of all sub-components.
      To model how the environment changes over time in response to the system’s out-
put, we use a simulator function. The simulator function S is formally defined as a
function that takes an environment e, a component value v, and a simulator state s, re-
turning a distribution over a pair containing a new environment and simulator. Formally
(e′ , s′ ) ← S(e, v, s). The distribution represents the probabilistic nature of e, in that it
defines a distribution over future behaviors of environment agents. The simulator state s
is used to represent the internal state of the simulator and the unobserved world state. To
model the simulation ending (due to meeting criteria specified in the Scenic program),
we allow S to return a special environment value ⊥.
      Given a component M, an environment e0 , and a simulator state s0 , we can sample
a trace τ = ((e0 , v0 ), . . . , (em , vm )) by setting v0 = M(e0 , ∅) and for all i ≥ 1 until
ei−1 = ⊥, sampling (ei , si ) ← S(ei−1 , vi−1 , si−1 ) and assigning vi = M(ei , vi−1 ).
QmWe write T (e0 , s0 , M) for the induced trace distribution, where τ has probability
   i=1 P ((ei , si ) = S(ei−1 , vi−1 , si−1 )). We also overload T to be defined with regards
to a scenario instead of a scene, writing τ ← T (E, s0 , M), where P(T (E, s0 , M) =
τ ) = P(E = e0 ) · P(T (e0 , s0 , M) = τ ). As an abuse of notation, we write ∀ τ ∈ T to
indicate quantifying over all possible traces that can be drawn from T .

3.2   Components
Components define a compartmentalized piece of a system, with well-defined inputs
and outputs. As we will see in this section, components can be combined via composi-
tion, such that the top-level system can also be considered a component.
                                                                          ScenicProver      7




Fig. 1: A ScenicProver snippet defining the throttle controller component of the AEB
example from Sec. 2.


    The interface of a component can be considered a 4-tuple (I, O, S, A), where I is
a set of typed inputs (originating from the output of another component), O is a set
of typed outputs, S is a set of typed sensor values (originating from sensed environ-
ment data), and A is a set of typed actions (essentially a more restricted form of input
representing actions taken in by this component which are then enacted on the envi-
ronment)4 . Components can also have internal state. The concatenated values of all of
these is what determines a component’s value v at a given timestep.
    In Scenic, a system’s implementation is defined by behavior statements, which can
contain arbitrary Python code, take arbitrary input from the world, and have arbitrary
effects on the world. This approach provides significant flexibility to the user, while
allowing black-box testing, but poses a problem for compositional reasoning. We take a
different approach to defining components in our framework that balances expressivity
with providing structure for analysis while preserving the ability to simulate any com-
ponent. Specifically, we add new syntax which restricts how components take input and
affect world state to the defined component interfaces, which aids analysis. The syntax
defining the throttle controller component of our AEB example is shown in Figure 1.


3.3     Contracts

To specify and reason about the behavior of components, we use assume-guarantee
contracts, which we define as follows. A contract C is a pair (A, G) of LTLf Modulo
Theories [15,16] formulas (an extension of Linear Temporal Logic (LTL) [28]), whose
atomic formulas may use any Scenic expressions. Traces as defined above include all
the information necessary to evaluate such expressions and so give a truth value to these
formulas. A given trace τ is said to satisfy a contract C = (A, G), written τ ⊨ C, iff
 4
     Sensors and actions are separated from other forms of IO for implementation reasons.
8       E. Vin et al.




Fig. 2: An abbreviated ScenicProver snippet containing syntax for describing the con-
tract over the throttle shield.


τ ⊨ (A =⇒ G). Given a distribution over traces   P T , its probability of satisfying a
contract C is P(T ⊨ C) = P(τ ⊨ C | τ ← T ) = τ ∈T P(τ ⊨ C).
    To be useful, a contract must specify assumptions and/or guarantees. As discussed
above, contracts represent these using LTLfMT in which propositions contain arbitrary
Scenic expressions with access to global variables and contract ports. An example of
such a property, always self.speed <= (next self.speed), would imply
that the linked object never accelerates. An example of the syntax for defining a contract
over our control system is shown in Figure 2.
    In the next sections, we discuss how we verify whether contracts hold and how we
combine them to derive properties of the whole system.


4   Contract Verification

We now turn to methods to quantify to what extent contracts hold, which we call veri-
fication procedures. These procedures allow us to formalize the different types of “ev-
idence” supported by the framework, and allow us to define a calculus for combining
them into an assurance case in the next section.
    We define a verification procedure for a contract as a (possibly randomized) proce-
dure which computes a lower bound for the probability that the contract holds:

Definition 1 (Verification Procedures). A verification procedure V(T , c) is a proba-
bilistic procedure which takes in a distribution over traces T and a confidence c ∈ [0, 1]
and outputs p ∈ [0, 1]. A verification procedure V is sound with respect to a contract C,
written V(T , c) ⊢ C, iff P(V(T , c) ≤ P(T ⊨ C)) ≥ c.

For simplicity, we omit the parameters of verification procedures when not needed.
    In our framework, we assume that all evidence is derived independently. Intuitively,
this means that our confidence in one piece of evidence does not affect our confidence
in another piece of evidence. This concept is formalized in Assumption 1.

Assumption 1 All verification procedures are performed independently. Formally,

      ∀ V1 , V2 , ∀ p1 , p2 , P((p1 ≤ V1 ) ∧ (p2 ≤ V2 )) = P(p1 ≤ V1 )P(p2 ≤ V2 ).
                                                                             ScenicProver         9

4.1     Testing-based Verification Procedures

The most accessible way to verify a potentially black-box system is testing, something
that Scenic is already capable of doing. We begin by defining contract checking proce-
dures, which given a set of traces provide a lower bound on the number of traces in the
set which satisfy a contract.

Definition 2 (Contract Checking Procedure). A contract checking procedure K takes
a set of traces T̂ and returns a count k. A contract checking procedure K is sound with
respect to a contract C, written K(T̂ ) ⊢ C, iff K(T̂ ) ≤ |{τ ∈ T̂ | τ ⊨ C}|

For simplicity, we omit the parameters of contract checking procedures when not needed.
A sound contract checking procedure naturally yields a sound verification procedure5 :

Definition 3 (Testing-based Verification Procedures). The testing-based verification
schema VT takes in a contract checking procedure K and the number of tests to run
n ∈ N, returning a verification procedure as follows:


VT (K, n)(T , c) Definition:
1: τ1 ∼ T , . . . , τn ∼ T
2: T̂ := {τ1 , . . . , τn }
3: k := K(T̂ )
4: p := ClopperPearsonInterval(k, n, c)                   ▷ Compute Clopper-Pearson interval [6].
5: return p



Theorem 2 (Soundness of Testing-based Verification Procedures). If for all T̂ sam-
pled IID from any T , K(T̂ ) is a sound contract checking procedure, then for any con-
tract C and n ∈ N, VT (K, n) ⊢ C.

     The first type of verification procedure available in ScenicProver is an instantiation
of a testing-based verification procedure using the above schema. Recall that Scenic
has the ability to specify environments, sample static scenes from them, and then run
dynamic simulations with the help of a simulator. During a simulation, the assumptions
and guarantees provided by a contract can be evaluated to determine whether or not they
hold. Leveraging these two pieces, we can generate data using Scenic and then use that
to see if a component satisfies a contract, allowing us to implement a sound contract
checking procedure. This technique provides a baseline method to generate evidence for
components that may be difficult or impossible to reason about using other techniques.
     There are several potential methods to actually implement the required contract
checking procedure. The most straightforward method, implemented in ScenicProver,
is to sample a scene from Scenic and run a dynamic simulation, with the linked Scenic
object using the behavior defined by the components in question. Using this method,
 5
     The verification is sound for the simulated system, and we leave addressing the sim-to-real gap
     to future work.
10         E. Vin et al.

each run provides evidence that can be used for all contracts on the components. Note
that using this approach to test the system as a whole is equivalent to what is currently
available using Scenic. We leave other methods to future work.


4.2     Proof-based Verification Procedures

While testing can be generically applied and requires little user effort, the evidence gen-
erated is probabilistic and can take significant computation time to generate. For these
reasons we also provide the ability to explicitly prove contracts correct. The following
proof-based verification schema supports an arbitrary machine-checkable proof format.

Definition 4 (Proof-based Verification Procedures). The proof-based verification schema
VP takes in three parameters: a proof r, a proof checker R, and a contract C, return-
ing a verification procedure. We indicate a proof being validated by the checker as
R(r, C) = ⊤, which should occur only when r is a valid proof indicating ∀ τ, τ ⊨
(A =⇒ G). Then we define
                                                 (
                                                  1      R(r, C) = ⊤
                           VP (r, R, C)(T , c) =
                                                  0      otherwise

   Note that T and c are unused in the above definition, as a proof-based verification
procedure is independent of the distribution of traces and the desired confidence.

Theorem 3. If R is a sound checker, in that it only accepts valid proofs of the correct
type, then VP (r, R, C) is a sound verification procedure.

    In our implementation, we enable this functionality by formalizing semantics for
a subset of Scenic in the proof assistant Lean 4 [26] and allowing the user to provide
proofs that a given contract is correct. ScenicProver provides functionality to export as-
sumptions and guarantees from our internal logic to .lean files, along with the trans-
lated component and proof obligations using the LeanLTL [41] library, which provides
structure for reasoning about LTLf modulo theories. ScenicProver checks that the proof
supplied by the user is valid using the Lean 4 REPL [25].
    Providing semantics for Scenic in general is highly non-trivial since it can contain
arbitrary Python. Limiting what can be written in Scenic components in general would
be restrictive to the ability to represent real-life systems. Instead, for Lean-based proofs,
we target a subset of Scenic containing arithmetic and several other useful functions
like ceilings, floors, minimum, maximum, etc. and thus limit which components can be
verified directly.6 However we show in our example that even a small subset of Scenic
is enough to achieve interesting results.
 6
     This subset has some overlap with established theories in LTLf modulo theories [15]. However,
     even in our simple example we encounter nonlinear arithmetic, an undecidable theory. Using
     an interactive theorem prover like Lean 4 sidesteps the problem of decidability.
                                                                     ScenicProver      11

4.3    Assumption-based Verification Procedures

There are cases where the user may have reason for believing a contract to be true
that does not support a formal proof and is not conducive to testing. A user may also
want to complete the structure of their argument before deciding how to generate the
requisite evidence. For such cases, we give users the ability to assume a contract is
correct with a given probability and confidence. From a theory perspective, we model
assumptions by simply assuming that a sound verification procedure has generated the
assumed probability for the given confidence.


5     Combining Verification Procedures

The previous sections describe how to formalize components and contracts, and how
to verify that a given contract holds for a given component. The natural next question
is how to combine these results to translate component-level results to system-level
results, a process we accomplish using contract operators: composition, conjunction,
refinement, strong merging, and weak merging. All of these operations, with the excep-
tion of weak merging, are existing operators from the contract literature [19,20]. For
each contract operator, we provide a formal definition and a judgment rule for deriving
a sound verification procedure for the output of the operator, given sound verification
procedures for the inputs. We provide additional details for the weak merging operator,
as to the best of our knowledge, this is a novel operator proposed here for the purpose
of reducing manual proof burden by weakening the needed contracts.
    ScenicProver computes the required verification procedures directly, using Pacti [19]
to compute the contract outputs of many of the following contract operators. As some
operations can be undecidable [15,41] (namely refinement), we also provide the ability
for the user to input a Lean 4 proof using LeanLTL [41] (similar to how ScenicProver
checks proof-based evidence) if Pacti is unable to compute the operation automatically.


5.1    Refinement

The first contract operator we introduce is the refinement operator, which provides a
partial ordering over contracts. It is useful for translating a “stronger” contract into a
“weaker” contract that has a desired form.

Definition 5 (Refinement Contract Operation [19,20]). Given two contracts C1 =
(A1 , G1 ) and C2 = (A2 , G2 ), refinement (C1 ≤ C2 ) is defined as,

      C1 ≤ C2 ⇐⇒ ∀ τ, τ ⊨ (A2 =⇒ A1 ) ∧ ((A1 =⇒ G1 ) =⇒ (A2 =⇒ G2 ))

Theorem 4 (Refinement Rule).

                                V1 (T , c) ⊢ C1 C1 ≤ C2
                                      V1 (T , c) ⊢ C2
12        E. Vin et al.

5.2    Composition, Conjunction, and Strong Merge

The composition operator allows one to combine contracts over sub-components to ob-
tain a contract over the resulting higher-level component. The conjunction and strong
merge operator allow one to combine contracts over the same component, the first loss-
lessly and the second in a way that assumes both contracts hold. These contract opera-
tors are defined in Definition 6 (see [20] for more information).
Definition 6 (Composition, Conjunction, and Strong Merge Operators [19,20]).
                                               Assumptions
  Operator Name Symbol
                                               Guarantees
                                  (A1 ∧ A2 ) ∨ (A1 ∧ G1 ) ∨ (A2 ∧ G2 )
    Composition       ∥
                             ((A1 =⇒ G1 ) ∧ (A2 =⇒ G2 )) ∨ (¬A1 ∧ ¬A2 )
                                                A1 ∨ A2
    Conjunction       ∧
                             ((A1 =⇒ G1 ) ∧ (A2 =⇒ G2 )) ∨ (¬A1 ∧ ¬A2 )
                                                A1 ∧ A2
   Strong Merge       •
                                         (G1 ∧ G2 ) ∨ ¬A1 ∨ ¬A2
   Our judgment rules deriving verification procedures for these operators, given in
Theorem 5, are derived from a common scheme:

Definition 7 (Union Bound Verification Scheme). The union bound verification pro-
cedure scheme V∪ takes in two other verification procedures and a binary contract
operator, combining the results using the union bound:


V∪ (V1 , V2 , ∗)(C1 ∗ C2 , T , c1 c2 ) Definition:
 1: p1 ← V1 (T , c1 )
 2: p2 ← V2 (T , c2 )
 3: return p1 + p2 − 1



Theorem 5 (Composition, Conjunction, and Strong Merge Rules).

       V1 (T , c1 ) ⊢ C1 V2 (T , c2 ) ⊢ C2                  V1 (T , c1 ) ⊢ C1 V2 (T , c2 ) ⊢ C2
(1)                                                  (2)
      V∪ (V1 , V2 , ∥)(T , c1 c2 ) ⊢ (C1 ∥ C2 )            V∪ (V1 , V2 , ∧)(T , c1 c2 ) ⊢ (C1 ∧ C2 )
                                  V1 (T , c1 ) ⊢ C1 V2 (T , c2 ) ⊢ C2
                           (3)
                                 V∪ (V1 , V2 , •)(T , c1 c2 ) ⊢ (C1 • C2 )

5.3    Weak Merge

The weak merge operator returns a contract that assumes either of the assumptions and
either of the guarantees of the input contracts hold. This contract operator is novel to our
work, because it produces a contract that is more relaxed in the refinement order than
the result of conjunction or strong merging. However, it has useful properties when it
comes to verification procedure combination. Intuitively, if the contract resulting from
                                                                             ScenicProver         13

the weak merge operation is still strong enough for our needs, we can obtain a higher
probability of correctness than using the conjunction or strong merge operator, as we
need only assume that one input contract holds.

Definition 8 (Weak Merge Contract Operation). Given two contracts C1 = (A1 , G1 )
and C2 = (A2 , G2 ), their weak merge C1 ▷◁ C2 is (A1 ∨ A2 , G1 ∨ G2 ∨ ¬(A1 ∨ A2 )).

Theorem 6 (Weak Merge Rule).

                        V1 (T | A1 , c1 ) ⊢ C1 V2 (T | ¬A1 , c2 ) ⊢ C2
                                 V▷◁ (T , c1 c2 ) ⊢ (C1 ▷◁ C2 )



V▷◁ (V1 , V2 )(C1 ▷◁ C2 , T , c1 c2 ) Definition:
 1: p1 ← V1 (T | A1 , c1 )
 2: p2 ← V2 (T | ¬A1 , c2 )
 3: return p1 (P(T ⊨ A1 )) + p2 (1 − P(T ⊨ A1 ))



Note that this verification procedure requires determining P(T ⊨ A1 ). For this reason,
we propose a less general but more practical contract-checking procedure for the case
where a proof for one contract is provided (utilizing VP to check the proof’s validity),
which we implement in ScenicProver. We present it as a sound contract checking pro-
cedure K▷◁T , which as noted above can be converted to a sound verification procedure.

Theorem 7 (Testing-Based Weak Merge Contract Checking Procedure).

                             VP (r, R)(T , 1) ⊢ C1      K1 (TˆT ) ⊢ C2
                            K▷◁T (r, R, K1 , T , n)(T̂ ) ⊢ (C1 ▷◁ C2 )




K▷◁T (r, R, K1 , T , n)(T̂ ) Definition:
 1: p′ ← VP (r, R)(C1 , T , 1)
 2: if p′ < 1 then return 0                                             ▷ Proof of C1 did not check
 3: TˆP := {τ ∈ T̂ | τ ⊨ A1 }                       ▷ C1 applies for these traces; no need to test C2
 4: TˆT := T̂ − TˆP                                               ▷ Test C2 on the remaining traces
 5: k := K1 (C2 , TˆT , c)
 6: return k + |TˆP |



    This procedure provides a speedup over strong merge when some assumptions can
be checked statically, i.e., given an initial state e0 , all traces that start with this state
will either satisfy or violate the assumptions. For example, suppose C1 assumes A and
14        E. Vin et al.

sunny weather, while C2 assumes A and rainy weather. If we have proved C1 , and can
determine that the weather is sunny in a given trace τ just from its initial state, then
we know that τ ⊨ C1 ▷◁ C2 without needing to run a complete simulation. Note that it
is sufficient to be able to check the weather statically, regardless of the complexity of
A. In general, for assumptions A1 and A2 which are conjunctions of other constraints,
only the constraints which are not common to both assumptions need to be checkable
statically. This is because if a constraint is included in both sets of assumptions, then if
it holds, the proof of C1 ensures C1 ▷◁ C2 holds. If instead the constraint does not hold,
then A1 ∨ A2 is violated and so C1 ▷◁ C2 is vacuously true. In Section 6 we will see the
concrete speedup provided by this operator.

5.4     Visualizing Verification Procedure Trees
All contract results generated in ScenicProver can be visualized as a textual assurance
case [32]. The assurance case shows a tree of the rules that generated the top-level
result, down to the proofs, assumptions, and tests that were used in the base verification
procedures. Complete examples are shown in Appendix C. In the future, we hope to
add support for other tools/methods [39,29,21,8] for visualizing assurance cases.


6      Case Study
To illustrate the applicability and utility of our framework, we implement our motivat-
ing AEB example as a case study. Specifically, we use a combination of proofs and
testing to get a stronger result than testing the system as a monolith could provide. For
abbreviated examples of the ScenicProver code defining components and contracts in
this case study, see Figures 1 and 2 (full code is available in our repository).
    The three sensors are, for simplicity, modeled internally as components that take
the true distance to the lead vehicle from the ego and add errors to simulate their real-
world analogues.7 The radar distance sensor has a chance of failure (returning a too-high
value) that increases as the profile of the lead car shrinks, intended to simulate the radar
profile of the lead vehicle being too small to reliably detect. The laser distance sensor
has a chance of failure (returning a too-small value) in weather conditions like rain and
snow, in which atmospheric particles might obstruct the beam. The camera distance
sensor simply adds a small amount of Gaussian noise to the true value. The remainder
of the components and contracts are as described in Section 2.
    We now turn to constructing our assurance case in ScenicProver, which is visualized
in Figure 3. We will reach our overall system safety contract (K EEPS D ISTANCE) by
refining the composition of contracts over the three high-level components of our vehi-
cle: the perception system, control system, and vehicle actuator. The operations shown
in the figure are those explicitly invoked in the ScenicProver file, though ScenicProver
syntax does abstract away some boilerplate.8 All operators with a white background
were computed automatically by Pacti, while operators with a green background were
 7
     ScenicProver supports realistic sensors from any simulator compatible with Scenic.
 8
     For example, the composition to derive C ONTROL S YSTEM S AFETY is over only the S AFE
     T HROTTLE F ILTER, using an implicit vacuous contract for the PID controller.
                                                                                                   ScenicProver            15

                                                                Vehicle


                                  ≤     Refinement
    Testing       Assumption                               Keeps Distance
                                  ||    Composition

     Proof           Rule         ⋈     Weak Merge
                                                                  ≤


                                                                  ||



               Accurate Speed               Accurate Distance                Control System
                                                                                                       Max Braking Force
                                                                                 Safety



                                       ⋈                                             ||


              Accurate Distance             Accurate Distance
                 Unknown                         Known                      Safe Throttle Filter



                                       ≤


                                       ||


    Radar Accurate             Laser Accurate         Median Distance
       Distance                   Distance                 Filter


                            Perception System                                Control System             Vehicle Actuator


         Fig. 3: The structure of the assurance case generated with ScenicProver.



proved manually in Lean 4. Some of these proofs were highly non-trivial (e.g. the proof
of refinement for K EEPS D ISTANCE uses the undecidable theory of nonlinear arith-
metic) and others we hope to automate in future work.
    We begin with the contracts for the control system and vehicle actuator. For the
control system, we prove in Lean 4 that the safety filter (i.e. a shield) will always output
a braking action if we are perceived to be too close to the vehicle ahead of us. This
guarantee is transferred to the control system as a whole automatically via Pacti when
the control system is composed together. For the vehicle actuator, we assume that a
maximal braking action will result in a given slowdown with a probability of at least
99% with 99.9% confidence, with the justification used in Section 2 that this could be
determined by outside testing.
    Turning to the perception system, ACCURATE S PEED is assumed directly (justi-
fied by assuming an accurate speedometer). For showing our ACCURATE D ISTANCE
contract, we begin by importing our manufacturer sensor requirements (R ADAR AC -
CURATE D ISTANCE and L ASER ACCURATE D ISTANCE) and proving a small contract
about the semantics of the median filter (M EDIAN D ISTANCE F ILTER). We compose
16      E. Vin et al.

                                                                       Naive     Optimized
Minutes Naïve     Opt.
                                                      1.00
1       0.2787    0.4912




                            Correctness Probability
5       0.7717    0.8759                              0.75

15      0.8262    0.9327
                                                      0.50
30      0.8708    0.9317
60      0.9049    0.9310                              0.25

120     0.9100    0.9394
                                                      0.00
240     0.9112    0.9411                                     1     5      10                 50     100

480     0.9155    0.9459                                         Verification Runtime (minutes, log scale)


Fig. 4: Probability lower bounds on the overall system contract (K EEPS D ISTANCE)
obtained with ScenicProver, as a function of time spent testing.


and refine these three contracts into a contract over the whole perception system that
shows that when the assumptions of the radar and laser sensors are met, the perception
system will always output an accurate distance (ACCURATE D ISTANCE K NOWN). We
then define another contract over the perception system covering the remaining portion
of the space (ACCURATE D ISTANCE U NKNOWN), which we will test via simulation
with a target confidence of 99.9%. Finally, we perform a weak merge over these two
contracts, resulting in our overall ACCURATE D ISTANCE contract. The end result is
that ACCURATE D ISTANCE K NOWN (which represents 35% of the space in our exam-
ple) need not be tested, and so we are able to allocate all of our testing budget to the
remaining 65% of the space covered by ACCURATE D ISTANCE U NKNOWN.
     The gains achieved by structuring the assurance argument in this way rather than
testing the system as a monolith are shown in Figure 4. We compare the probability
bounds obtained for the top-level contract between using ScenicProver naïvely versus
incorporating the manufacturer guarantees using the weak merge operator. The results
are shown as a function of time spent testing, up to a total of 8 hours. As can be seen
in the figure, the optimized analysis, possible only because of the reasoning abilities of
ScenicProver, results in us being able to show our overall guarantee is true with proba-
bility 94.59%, up from 91.55% with the same time budget and confidence (99.8%). In
fact, ScenicProver is able to provide a stronger result in 15 minutes than what naïvely
testing the system as a monolith can provide in 8 hours. The complete assurance cases
generated by ScenicProver after 8 hours (naïve and optimized) are given in Appendix C.


7     Conclusion

In this paper we introduced ScenicProver, a new framework that builds on the Scenic
probabilistic programming language to allow for compositional verification of cyber-
physical systems with learning-enabled components using a variety of methods from
explicit proofs to testing. We illustrated the value of the system by providing a stronger
                                                                           ScenicProver        17

verification result for the same testing budget on an example system given reasonable
assumptions, something that would not have been possible in Scenic alone.
    In future work we plan to expand on this framework, adding additional methods of
evidence generation such as analysis techniques for neural networks, further integration
with Pacti [19] to automate more complex contract operations, techniques to address the
sim-to-real gap, and support for synthesis of contracts from top-level requirements. We
also plan to apply this framework to a real system in a more in-depth case study paper.

Acknowledgments. This material is based upon work supported by the National Science Foun-
dation under Award No. 2303564.


References
 1. Astorga, A., Hsieh, C., Madhusudan, P., Mitra, S.: Perception Contracts for Safety of ML-
    Enabled Systems. Proceedings of the ACM on Programming Languages 7(OOPSLA2),
    299:2196–299:2223 (Oct 2023). https://doi.org/10.1145/3622875, https://dl.acm.org/doi/10.
    1145/3622875
 2. Benveniste, A., Caillaud, B., Nickovic, D., Passerone, R., Raclet, J.B., Reinkemeier, P.,
    Sangiovanni-Vincentelli, A., Damm, W., Henzinger, T., Larsen, K.: Contracts for Systems
    Design. Now Foundations and Trends (2018), https://ieeexplore.ieee.org/document/8620676
 3. Bloem, R., Könighofer, B., Könighofer, R., Wang, C.: Shield Synthesis: Runtime Enforce-
    ment for Reactive Systems. In: Baier, C., Tinelli, C. (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems, vol. 9035, pp. 533–548. Springer Berlin Heidelberg,
    Berlin, Heidelberg (2015), http://link.springer.com/10.1007/978-3-662-46681-0_51
 4. Blohm, P., Fränzle, M., Herber, P., Kröger, P., Remke, A.: Towards probabilistic contracts
    for intelligent cyber-physical systems. In: Margaria, T., Steffen, B. (eds.) Leveraging Appli-
    cations of Formal Methods, Verification and Validation. Specification and Verification. pp.
    26–47. Springer Nature Switzerland, Cham (2025)
 5. Cimatti, A., Dorigatti, M., Tonetta, S.: OCRA: A tool for checking the refinement of tem-
    poral contracts. In: 2013 28th IEEE/ACM International Conference on Automated Software
    Engineering (ASE). pp. 702–705 (Nov 2013). https://doi.org/10.1109/ASE.2013.6693137,
    https://ieeexplore.ieee.org/document/6693137
 6. CLOPPER, C.J., PEARSON, E.S.: The use of confidence or fiducial limits illustrated in the
    case of the binomial. Biometrika 26(4), 404–413 (Dec 1934). https://doi.org/10.1093/biomet/
    26.4.404, https://doi.org/10.1093/biomet/26.4.404
 7. Corso, A., Moss, R., Koren, M., Lee, R., Kochenderfer, M.: A Survey of Algorithms for
    Black-Box Safety Validation of Cyber-Physical Systems. J. Artif. Int. Res. 72, 377–428 (Jan
    2022). https://doi.org/10.1613/jair.1.12716, https://dl.acm.org/doi/10.1613/jair.1.12716
 8. Denney, E., Pai, G., Pohl, J.: AdvoCATE: An Assurance Case Automation Toolset. In: Ort-
    meier, F., Daniel, P. (eds.) Computer Safety, Reliability, and Security. pp. 8–21. Springer,
    Berlin, Heidelberg (2012). https://doi.org/10.1007/978-3-642-33675-1_2
 9. Desai, A., Ghosh, S., Seshia, S.A., Shankar, N., Tiwari, A.: SOTER: A Runtime Assurance
    Framework for Programming Safe Robotics Systems. In: 2019 49th Annual IEEE/IFIP Inter-
    national Conference on Dependable Systems and Networks (DSN). pp. 138–150 (Jun 2019).
    https://doi.org/10.1109/DSN.2019.00027, https://ieeexplore.ieee.org/document/8809550
10. Dreossi, T., Donzé, A., Seshia, S.A.: Compositional Falsification of Cyber-Physical Sys-
    tems with Machine Learning Components. Journal of Automated Reasoning 63(4), 1031–
    1053 (Dec 2019). https://doi.org/10.1007/s10817-018-09509-5, https://doi.org/10.1007/
    s10817-018-09509-5
18       E. Vin et al.

11. Dreossi, T., Fremont, D.J., Ghosh, S., Kim, E., Ravanbakhsh, H., Vazquez-Chanlatte,
    M., Seshia, S.A.: VerifAI: A Toolkit for the Formal Design and Analysis of Artificial
    Intelligence-Based Systems. In: Dillig, I., Tasiran, S. (eds.) Computer Aided Verifica-
    tion. pp. 432–442. Springer International Publishing, Cham (2019). https://doi.org/10.1007/
    978-3-030-25540-4_25
12. Fremont, D.J., Dreossi, T., Ghosh, S., Yue, X., Sangiovanni-Vincentelli, A.L., Seshia, S.A.:
    Scenic: a language for scenario specification and scene generation. In: Proceedings of
    the 40th ACM SIGPLAN Conference on Programming Language Design and Implemen-
    tation. pp. 63–78. PLDI 2019, Association for Computing Machinery, New York, NY,
    USA (Jun 2019). https://doi.org/10.1145/3314221.3314633, https://dl.acm.org/doi/10.1145/
    3314221.3314633
13. Fremont, D.J., Kim, E., Dreossi, T., Ghosh, S., Yue, X., Sangiovanni-Vincentelli, A.L., Se-
    shia, S.A.: Scenic: a language for scenario specification and data generation. Machine Learn-
    ing 112(10), 3805–3849 (Oct 2023). https://doi.org/10.1007/s10994-021-06120-5, https:
    //doi.org/10.1007/s10994-021-06120-5
14. Fulton, N., Mitsch, S., Quesel, J.D., Völp, M., Platzer, A.: KeYmaera X: An Axiomatic
    Tactical Theorem Prover for Hybrid Systems. In: Felty, A.P., Middeldorp, A. (eds.) Auto-
    mated Deduction - CADE-25. pp. 527–538. Springer International Publishing, Cham (2015).
    https://doi.org/10.1007/978-3-319-21401-6_36
15. Geatti, L., Gianola, A., Gigante, N.: Linear Temporal Logic Modulo Theories over Fi-
    nite Traces. In: Proceedings of the Thirty-First International Joint Conference on Artifi-
    cial Intelligence. vol. 3, pp. 2641–2647 (Jul 2022). https://doi.org/10.24963/ijcai.2022/366,
    https://www.ijcai.org/proceedings/2022/366
16. Geatti, L., Gianola, A., Gigante, N., Winkler, S.: Decidable Fragments of LTLf Modulo The-
    ories. In: ECAI 2023, pp. 811–818. IOS Press (2023), https://ebooks.iospress.nl/doi/10.3233/
    FAIA230348
17. Giannakopoulou, D., Namjoshi, K.S., Păsăreanu, C.S.: Compositional Reasoning. In:
    Clarke, E.M., Henzinger, T.A., Veith, H., Bloem, R. (eds.) Handbook of Model Check-
    ing, pp. 345–383. Springer International Publishing, Cham (2018), https://doi.org/10.1007/
    978-3-319-10575-8_12
18. Hampus, A., Nyberg, M.: A Theory of Probabilistic Contracts. In: Margaria, T., Steffen, B.
    (eds.) Leveraging Applications of Formal Methods, Verification and Validation. Specification
    and Verification. pp. 296–319. Springer Nature Switzerland, Cham (2024). https://doi.org/10.
    1007/978-3-031-75380-0_17
19. Incer, I., Badithela, A., Graebener, J.B., Mallozzi, P., Pandey, A., Rouquette, N., Yu, S.J.,
    Benveniste, A., Caillaud, B., Murray, R.M., Sangiovanni-Vincentelli, A., Seshia, S.A.: Pacti:
    Assume-guarantee contracts for efficient compositional analysis and design. ACM Trans.
    Cyber-Phys. Syst. 9(1) (Jan 2025). https://doi.org/10.1145/3704736, https://doi.org/10.1145/
    3704736
20. Incer, I., Benveniste, A., Sangiovanni-Vincentelli, A.: Some Algebraic Aspects of Assume-
    Guarantee Reasoning, pp. 9–35. Springer Nature Switzerland, Cham (2026). https://doi.org/
    10.1007/978-3-031-97537-0_2, https://doi.org/10.1007/978-3-031-97537-0_2
21. Kelly, T.: The Goal Structuring Notation A Safety Argument Notation. Proceedings of the
    Dependable Systems and Networks 2004 Workshop on Assurance Cases, July (2004), https:
    //cir.nii.ac.jp/crid/1573387449073910656
22. Koren, M., Alsaif, S., Lee, R., Kochenderfer, M.J.: Adaptive Stress Testing for Autonomous
    Vehicles. In: 2018 IEEE Intelligent Vehicles Symposium (IV). pp. 1–7 (Jun 2018). https:
    //doi.org/10.1109/IVS.2018.8500400, https://ieeexplore.ieee.org/document/8500400
23. Legay, A., Delahaye, B., Bensalem, S.: Statistical Model Checking: An Overview. In: Bar-
    ringer, H., Falcone, Y., Finkbeiner, B., Havelund, K., Lee, I., Pace, G., Roşu, G., Sokolsky,
                                                                             ScenicProver         19

    O., Tillmann, N. (eds.) Runtime Verification. pp. 122–135. Lecture Notes in Computer Sci-
    ence, Springer, Berlin, Heidelberg (2010). https://doi.org/10.1007/978-3-642-16612-9_11
24. Li, Y., Zhu, H., Braught, K., Shen, K., Mitra, S.: Verse: A Python Library for Reasoning
    About Multi-agent Hybrid System Scenarios. In: Enea, C., Lal, A. (eds.) Computer Aided
    Verification. pp. 351–364. Springer Nature Switzerland, Cham (2023). https://doi.org/10.
    1007/978-3-031-37706-8_18
25. Morrison,       K.:    leanprover-community/repl        (Sep       2025),     https://github.com/
    leanprover-community/repl
26. Moura, L.d., Ullrich, S.: The Lean 4 Theorem Prover and Programming Language. In:
    Platzer, A., Sutcliffe, G. (eds.) Automated Deduction – CADE 28. pp. 625–635. Springer
    International Publishing, Cham (2021). https://doi.org/10.1007/978-3-030-79876-5_37
27. Pasareanu, C.S., Gopinath, D., Yu, H.: Compositional Verification for Autonomous Systems
    with Deep Learning Components (Oct 2018). https://doi.org/10.48550/arXiv.1810.08303,
    http://arxiv.org/abs/1810.08303
28. Pnueli, A.: The temporal logic of programs. In: 18th Annual Symposium on Foundations of
    Computer Science (sfcs 1977). pp. 46–57 (Oct 1977). https://doi.org/10.1109/SFCS.1977.32,
    https://ieeexplore.ieee.org/document/4567924
29. Polacsek, T., Sharma, S., Cuiller, C., Tuloup, V.: The need of diagrams based on Toul-
    min schema application: an aeronautical case study. EURO Journal on Decision Pro-
    cesses 6(3), 257–282 (Nov 2018). https://doi.org/10.1007/s40070-018-0086-3, https://www.
    sciencedirect.com/science/article/pii/S2193943821000911
30. Păsăreanu, C.S., Mangal, R., Gopinath, D., Getir Yaman, S., Imrie, C., Calinescu, R.,
    Yu, H.: Closed-Loop Analysis of Vision-Based Autonomous Systems: A Case Study. In:
    Enea, C., Lal, A. (eds.) Computer Aided Verification. pp. 289–303. Lecture Notes in
    Computer Science, Springer Nature Switzerland, Cham (2023). https://doi.org/10.1007/
    978-3-031-37706-8_15
31. Rushby, J.: An Evidential Tool Bus. In: Lau, K.K., Banach, R. (eds.) Formal Methods and
    Software Engineering. pp. 36–36. Springer, Berlin, Heidelberg (2005). https://doi.org/10.
    1007/11576280_3
32. Rushby, J., Xu, X., Rangarajan, M., Weaver, T.L.: Understanding and Evaluating Assur-
    ance Cases. Tech. Rep. NF1676L-22111, NASA (Sep 2015), https://ntrs.nasa.gov/citations/
    20160000772
33. Seshia, S.A.: Introspective Environment Modeling. In: Finkbeiner, B., Mariani, L. (eds.)
    Runtime Verification. pp. 15–26. Springer International Publishing, Cham (2019). https://
    doi.org/10.1007/978-3-030-32079-9_2
34. Seshia, S.A., Sadigh, D., Sastry, S.S.: Toward verified artificial intelligence. Communications
    of the ACM 65(7), 46–55 (Jun 2022). https://doi.org/10.1145/3503914, https://dl.acm.org/
    doi/10.1145/3503914
35. Seto, D., Krogh, B., Sha, L., Chutinan, A.: The Simplex architecture for safe online control
    system upgrades. In: Proceedings of the 1998 American Control Conference. ACC (IEEE
    Cat. No.98CH36207). vol. 6, pp. 3504–3508 vol.6 (Jun 1998). https://doi.org/10.1109/ACC.
    1998.703255, https://ieeexplore.ieee.org/document/703255
36. Sha, L.: Using simplicity to control complexity. IEEE Software 18(4), 20–28 (Jul 2001).
    https://doi.org/10.1109/MS.2001.936213, https://ieeexplore.ieee.org/document/936213
37. Torfah, H., Seshia, S.A.: Runtime Monitors for Operational Design Domains of Black-Box
    ML-Models. In: OpenReview (Nov 2022), https://openreview.net/forum?id=6_AtjSBhqx
38. Torfah, H., Xie, C., Junges, S., Vazquez-Chanlatte, M., Seshia, S.A.: Learning Monitorable
    Operational Design Domains for Assured Autonomy. In: Bouajjani, A., Holík, L., Wu, Z.
    (eds.) Automated Technology for Verification and Analysis. pp. 3–22. Springer International
    Publishing, Cham (2022). https://doi.org/10.1007/978-3-031-19992-9_1
20       E. Vin et al.

39. Toulmin, S.E.: The Uses of Argument. Cambridge University Press (Jul 2003)
40. Vin, E., Kashiwa, S., Rhea, M., Fremont, D.J., Kim, E., Dreossi, T., Ghosh, S., Yue,
    X., Sangiovanni-Vincentelli, A.L., Seshia, S.A.: 3D Environment Modeling for Falsifica-
    tion and Beyond with Scenic 3.0. In: Enea, C., Lal, A. (eds.) Computer Aided Verifi-
    cation. pp. 253–265. Springer Nature Switzerland, Cham (2023). https://doi.org/10.1007/
    978-3-031-37706-8_13
41. Vin, E., Miller, K.A., Fremont, D.J.: LeanLTL: A Unifying Framework for Linear Temporal
    Logics in Lean. In: Forster, Y., Keller, C. (eds.) 16th International Conference on Interactive
    Theorem Proving (ITP 2025). Leibniz International Proceedings in Informatics (LIPIcs),
    vol. 352, pp. 37:1–37:9. Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl, Ger-
    many (2025). https://doi.org/10.4230/LIPIcs.ITP.2025.37, https://drops.dagstuhl.de/entities/
    document/10.4230/LIPIcs.ITP.2025.37
42. Wang, T.E., Daw, Z., Nuzzo, P., Pinto, A.: Hierarchical Contract-Based Synthesis for As-
    surance Cases. In: NASA Formal Methods: 14th International Symposium, NFM 2022,
    Pasadena, CA, USA, May 24–27, 2022, Proceedings. pp. 175–192. Springer-Verlag, Berlin,
    Heidelberg (May 2022). https://doi.org/10.1007/978-3-031-06773-0_9, https://doi.org/10.
    1007/978-3-031-06773-0_9
43. Wang, T.E., Oh, C., Low, M., Amundson, I., Daw, Z., Pinto, A., Chiodo, M.L., Wang,
    G., Hasan, S., Melville, R., Nuzzo, P.: Computer-Aided Generation of Assurance Cases.
    In: Computer Safety, Reliability, and Security. SAFECOMP 2023 Workshops: ASSURE,
    DECSoS, SASSUR, SENSEI, SRToITS, and WAISE, Toulouse, France, September 19,
    2023, Proceedings. pp. 135–148. Springer-Verlag, Berlin, Heidelberg (Sep 2023). https:
    //doi.org/10.1007/978-3-031-40953-0_12, https://doi.org/10.1007/978-3-031-40953-0_12
44. Yalcinkaya, B., Torfah, H., Desai, A., Seshia, S.A.: Ulgen: A Runtime Assurance Framework
    for Programming Safe Cyber–Physical Systems. IEEE Transactions on Computer-Aided De-
    sign of Integrated Circuits and Systems 42(11), 3679–3692 (Nov 2023). https://doi.org/10.
    1109/TCAD.2023.3246386, https://ieeexplore.ieee.org/abstract/document/10048006



A    Proofs of Base Verification Procedures

Theorem 2 Proof:

Proof. Given that K is a sound contract checking procedure, we know that k is a lower
bound on the true number of traces in T̂ that satisfy C. Since T̂ is sampled IID from T ,
the rest of the proof follows from the validity of the Clopper-Pearson interval [6].

Theorem 3 Proof:

Proof.
Case (R(r, C) = ⊤):
In this case, we know that C is valid as ∀ T , ∀ τ ∈ T , τ ⊨ (A =⇒ G), so
P(T ⊨ C) = 1. As p is always 1 in this case, and 1 ≤ 1, VP is sound in this case.
Case: (otherwise)
In this case, VP (r, R, C)(T , c) = 0. By definition, P(T ⊨ C) ≥ 0, so VP is trivially
sound in this case.
                                                                   ScenicProver     21

B    Proofs of Contract Operator Verification Procedures
We begin by establishing two lemmas that follow from the existing contract literature.
Lemma 1. Given two contracts C1 and C2 , and a trace distribution T ,
                      P(T ⊨ C1 ∥ C2 ) = P((T ⊨ C1 ) ∧ (T ⊨ C2 ))


Proof. Follows from [19,2].
Lemma 2. Given two contracts C1 and C2 , and a trace distribution T ,
                      P(T ⊨ C1 ∧ C2 ) = P((T ⊨ C1 ) ∧ (T ⊨ C2 ))


Proof. Follows from [19,2].
   We now prove the soundness of the refinement, composition, conjunction, and strong
merge verification procedures.
Theorem 4 Proof:
Proof. As V1 is sound, we know that with probability c, p ≤ P(T ⊨ C1 ). We consider
that case below.

            p ≤ P(T ⊨ C1 )
              = P(τ ⊨ (A1 =⇒ G1 ) | τ ← T )
              ≤ P(τ ⊨ (A2 =⇒ G2 ) | τ ← T )                (From C1 ≤ C2 )
              = P(T ⊨ C2 )


    Thus V1 (T , c) ⊢ C2 .
Theorem 5.1 Proof:
Proof. By the implicit assumption that V1 and V2 are sound validation procedures, we
have P(p1 ≤ P(T ⊨ C1 )) ≥ c1 and P(p1 ≤ P(T ⊨ C2 )) ≥ c2 . As these events are
assumed to be independent, we consider the case where they are both true which occurs
with probability c1 c2 .
 P(T ⊨ C1 ∥ C2 ) = P((T ⊨ C1 ) ∧ (T ⊨ C2 ))                      (Lemma 1)
                   = 1 − P((T ⊨ C1 ) ∨ (T ⊨ C2 ))
                   ≥ 1 − (P(T ⊨ C1 ) + P(T ⊨ C2 ))               (Boole’s Inequality)
                   = 1 − P(T ⊨ C1 ) − P(T ⊨ C2 )
                   = 1 − (1 − P(T ⊨ C1 )) − (1 − P(T ⊨ C2 ))
                   = 1 − 1 + P(T ⊨ C1 ) − 1 + P(T ⊨ C2 )
                   = P(T ⊨ C1 ) + P(T ⊨ C2 ) − 1
                   ≥ p1 + p2 − 1
22       E. Vin et al.

Thus V∪ (V1 , V2 , ∥)(T , c1 c2 ) ⊢ (C1 ∥ C2 ).
Theorem 5.2 Proof:
Proof. By the implicit assumption that V1 and V2 are sound validation procedures, we
have P(p1 ≤ P(T ⊨ C1 )) ≥ c1 and P(p1 ≤ P(T ⊨ C2 )) ≥ c2 . As these events are
assumed to be independent, we consider the case where they are both true which occurs
with probability c1 c2 .

 P(T ⊨ C1 ∧ C2 ) = P((T ⊨ C1 ) ∧ (T ⊨ C2 ))                         (Lemma 2)
                     = 1 − P((T ⊨ C1 ) ∨ (T ⊨ C2 ))
                     ≥ 1 − (P(T ⊨ C1 ) + P(T ⊨ C2 ))                (Boole’s Inequality)
                     = 1 − P(T ⊨ C1 ) − P(T ⊨ C2 )
                     = 1 − (1 − P(T ⊨ C1 )) − (1 − P(T ⊨ C2 ))
                     = 1 − 1 + P(T ⊨ C1 ) − 1 + P(T ⊨ C2 )
                     = P(T ⊨ C1 ) + P(T ⊨ C2 ) − 1
                     ≥ p1 + p2 − 1


Thus V∪ (V1 , V2 , ∧)(T , c1 c2 ) ⊢ (C1 ∧ C2 ).
Theorem 5.3 Proof:
Proof. Using our Theorem 5.2 we have a sound verification procedure over C1 ∧ C2 . We
now show that C1 ∧ C2 ≤ C1 • C2 .
Assumptions:

                    A1 ∧ A2 =⇒ A1 ∨ A2                          (Trivial)

Guarantees:

         ((A1 =⇒ G1 ) ∧ (A2 =⇒ G2 )) =⇒ ((A1 ∧ A2 ) =⇒ (G1 ∧ G2 ))
                                                  ⇐⇒ (G1 ∧ G2 ) ∨ ¬(A1 ∧ A2 )
                                                  ⇐⇒ (G1 ∧ G2 ) ∨ ¬A1 ∨ ¬A2

Using the above and Theorem 4, we can conclude that V∪ (V1 , V2 , •)(T , c1 c2 ) ⊢ (C1 •
C2 ).
Theorem 6 Proof:
Proof. We first show that ∀ τ, (τ ⊨ C1 ∨τ ⊨ C2 ) =⇒ (τ ⊨ C1 ▷◁ C2 ). The assumptions
are trivial, so we focus on the guarantees. If neither A1 or A2 is true, then the contract
is vacuously satisfied. Otherwise, at least one must be true, so either G1 or G2 is true,
satisfying the G1 ∨ G2 portion of the contract.
    We again assume that p1 and p2 are lower bounds on the validity of their respective
contracts (as done in previous proofs), which due to the independence of V1 and V2
                                                                      ScenicProver        23

occurs with confidence c1 c2 .

P(T ⊨ C1 ▷◁ C2 ) ≥ P(T ⊨ C1 ∨ C2 )
                  = P(T ⊨ (C1 ∨ C2 ) ∧ (A1 ∨ ¬A1 ))
                  = P(T ⊨ ((C1 ∨ C2 ) ∧ A1 ) ∨ ((C1 ∨ C2 ) ∧ ¬A1 ))
                  = P(T ⊨ ((C1 ∨ C2 ) ∧ A1 )) + P(T ⊨ ((C1 ∨ C2 ) ∧ ¬A1 ))           (Disjoint Events)
                  ≥ P(T ⊨ C1 ∧ A1 ) + P(T ⊨ C2 ∧ ¬A1 )
                  = P(T ⊨ C1 | T ⊨ A1 )P(T ⊨ A1 )
                    + P(T ⊨ C2 | T ⊨ ¬A1 )P(T ⊨ ¬A1 )
                  = P((T | A1 ) ⊨ C1 )P(T ⊨ A1 )
                    + P((T | ¬A1 ) ⊨ C2 )(1 − P(T ⊨ A1 ))
                  ≥ p1 (P(T ⊨ A1 )) + p2 (1 − P(T ⊨ A1 ))


Theorem 7 Proof:
Proof. The proof for this verification procedure is similar to the proof for VT . First, we
ensure that r is a valid proof, returning 0 if that isn’t the case. By assumption k is the
number of traces in TˆT that satisfy C2 . Furthermore, T̂P is composed entirely of traces
that satisfy C1 , as the set consists entirely of traces that satisfy A1 , and thus C1 as we
have checked that it holds using VP . Therefore we know that in the sample T̂ has at
least k + |TˆP | traces that satisfy C1 or C2 , and thus C1 ▷◁ C2 . Thus K▷◁T is a sound
contract checking procedure.


C    Example Assurance Cases:

In this appendix we include assurance cases generated by ScenicProver, with some
added line breaks (indicated by \) and minor abbreviations for space (indicated by . . .).


Naïve:
Probabilistic Contract Result:
  Component: Car(...)
  Minimum 91.55% Correctness with 99.80% Confidence
  Assumptions:
    always (self._lane is not None)
    always (((0) <= (self.speed)) and ((self.speed) <= (5.4)))
    always (((0) <= (lead_car.speed)) and ((lead_car.speed) <= (5.4)))
    always (((-(0.9)) <= ((next (self.speed)) - (self.speed)))\
        and (((next (self.speed)) - (self.speed)) <= (0.5)))
    always (((-(0.9)) <= ((next (lead_car.speed)) - (lead_car.speed)))\
        and (((next (lead_car.speed)) - (lead_car.speed)) <= (0.5)))
    ((lead_dist) > (buffer_dist)) and ((self.speed) == (0))
    always ((next (lead_dist)) == ((lead_dist) - (true_relative_speed)))
  Guarantees:
    always ((lead_dist) > (5))
  Evidence:
    Refinement Method: LeanProof: (...)
    Probabilistic Contract Result:
24      E. Vin et al.

       Component: PerceptionSystem()
       Minimum 92.55% Correctness with 99.90% Confidence
       Assumptions:
         None
       Guarantees:
         (100.00%) always ((behind_car)\
             implies ((((lead_dist) - (0.1)) <= (dist))\
             and ((dist) <= ((lead_dist) + (0.1)))))
       Evidence:
         Simulation-Based Testing
         Sampled from Scenario ’highway.scenic (Hash=2255290405)
         3374 Verified, 559 Rejected, 0 A-Violated, 220 G-Violated
         4153 Samples, 28804.75 Seconds
         Mean Correctness: 93.88%
         Confidence Gap: 0.0266
     Contract Result:
       Component: Speedometer()
       Assumptions:
         None
       Guarantees:
         always ((speed) == (self.speed))
       Evidence:
         Assumed
     Contract Result:
       Component: ControlSystem(...)
       Assumptions:
         None
       Guarantees:
         always (((next (dist)) <= ((p_buffer_dist) + (0.1)))\
             implies ((next (throttle)) == (-(1))))
       Evidence:
         Contract Result:
           Component: ThrottleSafetyFilter(...)
           Assumptions:
             None
           Guarantees:
             always (((next (dist)) <= ((p_buffer_dist) + (0.1))) implies\
                 ((next (modulated_throttle)) == (-(1))))
           Evidence:
             LeanProof: (...)
     Probabilistic Contract Result:
       Component: CarActionControls()
       Minimum 99.00% Correctness with 99.90% Confidence
       Assumptions:
         None
       Guarantees:
         always (((throttle) == (-(1))) implies\
             (((next (self.speed)) == (0)) or\
             ((next (self.speed)) == ((self.speed) - (0.9)))))
       Evidence:
         Assumed

Optimized:
Probabilistic Contract Result:
  Component: Car(...)
  Minimum 94.59% Correctness with 99.80% Confidence
  Assumptions:
    always (self._lane is not None)
    always (((0) <= (self.speed)) and ((self.speed) <= (5.4)))
    always (((0) <= (lead_car.speed)) and ((lead_car.speed) <= (5.4)))
    always (((-(0.9)) <= ((next (self.speed)) - (self.speed)))\
        and (((next (self.speed)) - (self.speed)) <= (0.5)))
    always (((-(0.9)) <= ((next (lead_car.speed)) - (lead_car.speed)))\
        and (((next (lead_car.speed)) - (lead_car.speed)) <= (0.5)))
    ((lead_dist) > (buffer_dist)) and ((self.speed) == (0))
    always ((next (lead_dist)) == ((lead_dist) - (true_relative_speed)))
  Guarantees:
                                                          ScenicProver   25

  always ((lead_dist) > (5))
Evidence:
  Refinement Method: LeanProof: (...)
  Probabilistic Contract Result:
    Component: PerceptionSystem()
    Minimum 95.59% Correctness with 99.90% Confidence
    Assumptions:
      None
    Guarantees:
      always ((behind_car) implies\
          ((((lead_dist) - (0.1)) <= (dist))\
          and ((dist) <= ((lead_dist) + (0.1)))))
    Evidence:
      Refinement Method: LeanProof: (...)
      Conjunction Result:
      Simulation-Based Testing
          Sampled from Scenario ’NONE (Hash=NONE)
          5322 Verified, 810 Rejected, 0 A-Violated, 197 G-Violated
          6329 Samples, 28803.76 Seconds
          Mean Correctness: 96.43%
          Confidence Gap: 0.0166
      Sub Result (Correctness=1.00):
      Contract Result:
        Component: PerceptionSystem()
        Assumptions:
          (((params[’weather’]) == (0))\
              or ((params[’weather’]) == (1)))\
              and ((params[’lead_car_width’]) >= (1.8))
        Guarantees:
          always ((behind_car) implies\
              ((((lead_dist) - (0.1)) <= (dist))\
              and ((dist) <= ((lead_dist) + (0.1)))))
        Evidence:
          Refinement Method: LeanProof: (...)
          Contract Result:
            Component: RadarDistanceSystem()
            Assumptions:
              (params[’lead_car_width’]) >= (1.8)
            Guarantees:
              always ((behind_car) implies\
                   ((((lead_dist) - (0.1)) <= (dist))\
                   and ((dist) <= ((lead_dist) + (0.1)))))
            Evidence:
              Assumed
          Contract Result:
            Component: LaserDistanceSystem()
            Assumptions:
              ((params[’weather’]) == (0))\
                   or ((params[’weather’]) == (1))
            Guarantees:
              always ((behind_car) implies\
                   ((((lead_dist) - (0.1)) <= (dist))\
                   and ((dist) <= ((lead_dist) + (0.1)))))
            Evidence:
              Assumed
          Contract Result:
            Component: MedianDistanceFilter()
            Assumptions:
              None
            Guarantees:
              always ((out_dist) == \
                   (min((min((max((dist1), (dist2))),\
                   (max((dist1), (dist2))))),\
                   (max((dist2), (dist3))))))
            Evidence:
              LeanProof: (...)
      Sub Result (Correctness=0.93):
      Probabilistic Contract Result:
26      E. Vin et al.

           Component: PerceptionSystem()
           Minimum 93.34% Correctness with 99.90% Confidence
           Assumptions:
             ( 0.00%) not ((((params[’weather’]) == (0))\
                 or ((params[’weather’]) == (1)))\
                 and ((params[’lead_car_width’]) >= (1.8)))
           Guarantees:
             (100.00%) always ((behind_car) implies\
                 ((((lead_dist) - (0.1)) <= (dist))\
                 and ((dist) <= ((lead_dist) + (0.1)))))
           Evidence:
             Simulation-Based Testing
             Sampled from Scenario ’highway.scenic (Hash=2255290405)
             3446 Verified, 534 Rejected, 0 A-Violated, 197 G-Violated
             4177 Samples, 28803.76 Seconds
             Mean Correctness: 94.59%
             Confidence Gap: 0.0250

     Contract Result:
       Component: Speedometer()
       Assumptions:
         None
       Guarantees:
         always ((speed) == (self.speed))
       Evidence:
         Assumed
     Contract Result:
       Component: ControlSystem(...)
       Assumptions:
         None
       Guarantees:
         always (((next (dist)) <= ((p_buffer_dist) + (0.1)))\
             implies ((next (throttle)) == (-(1))))
       Evidence:
         Contract Result:
           Component: ThrottleSafetyFilter(...)
           Assumptions:
             None
           Guarantees:
             always (((next (dist)) <= ((p_buffer_dist) + (0.1)))\
                 implies ((next (modulated_throttle)) == (-(1))))
           Evidence:
             LeanProof: (...)
     Probabilistic Contract Result:
       Component: CarActionControls()
       Minimum 99.00% Correctness with 99.90% Confidence
       Assumptions:
         None
       Guarantees:
         always (((throttle) == (-(1))) implies\
             (((next (self.speed)) == (0))\
             or ((next (self.speed)) == ((self.speed) - (0.9)))))
       Evidence:
         Assumed
