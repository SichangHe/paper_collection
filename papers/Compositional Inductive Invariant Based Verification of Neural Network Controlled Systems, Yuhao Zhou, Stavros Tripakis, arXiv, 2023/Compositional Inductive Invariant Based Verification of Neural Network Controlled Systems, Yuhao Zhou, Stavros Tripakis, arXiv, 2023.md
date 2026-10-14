                                              Compositional Inductive Invariant Based
                                              Verification of Neural Network Controlled
                                                               Systems

                                                             Yuhao Zhou        and Stavros Tripakis
arXiv:2312.10842v2 [cs.LO] 26 Mar 2024




                                                             Northeastern University, Boston, MA, USA
                                                             {zhou.yuhao, stavros}@northeastern.edu



                                               Abstract. The integration of neural networks into safety-critical sys-
                                               tems has shown great potential in recent years. However, the challenge
                                               of effectively verifying the safety of Neural Network Controlled Systems
                                               (NNCS) persists. This paper introduces a novel approach to NNCS safety
                                               verification, leveraging the inductive invariant method. Verifying the in-
                                               ductiveness of a candidate inductive invariant in the context of NNCS
                                               is hard because of the scale and nonlinearity of neural networks. Our
                                               compositional method makes this verification process manageable by de-
                                               composing the inductiveness proof obligation into smaller, more tractable
                                               subproblems. Alongside the high-level method, we present an algorithm
                                               capable of automatically verifying the inductiveness of given candidates
                                               by automatically inferring the necessary decomposition predicates. The
                                               algorithm significantly outperforms the baseline method and shows re-
                                               markable reductions in execution time in our case studies, shortening the
                                               verification time from hours (or timeout) to seconds.


                                         Keywords: Formal Verification · Inductive Invariant · Neural Networks ·
                                         Neural Network Controlled Systems


                                         1   Introduction

                                         Neural Network Controlled Systems (NNCSs) are closed-loop systems that con-
                                         sist of an environment controlled by a neural network (NN). Advancements in
                                         machine learning have made NNCSs more widespread in safety-critical applica-
                                         tions, such as autonomous cars, industrial control, and healthcare [47]. While
                                         many methods exist for the formal verification of standard closed-loop sys-
                                         tems [8], the scale and nonlinearity of NNs makes the direct application of these
                                         methods to NNCSs a challenging task.
                                             In this paper, we study formal verification of safety properties of NNCSs,
                                         using the inductive invariant method [28]. In a nutshell, the method consists in
                                         coming up with a state predicate IndInv which is inductive, an invariant, and
                                         implies safety (see Section 2, Conditions (4), (5) and (6)). The most important
                                         property, and often the most difficult to check, is inductiveness. In the case of
2      Y. Zhou and S. Tripakis

NNCSs, checking inductiveness amounts to checking the validity of the follow-
ing formula, where NextNNC and NextENV are the transition relation predicates
of the NN controller and of the environment, respectively, and ϕ′ is the state
predicate ϕ applied to the next-state (primed) variables:

                  (IndInv ∧ NextNNC ∧ NextENV ) =⇒ IndInv′                     (1)

The problem that motivates our work is that checking formula (1) is infeasible
in practice using state-of-the-art tools. On the one hand, generic tools such as
SMT solvers [9] cannot handle formula 1 directly, typically due to the size and
complexity of the NN and corresponding NextNNC predicate. On the other hand,
specialized NN verification tools [45, 46] also cannot handle formula (1) directly,
typically due to limitations in being able to deal with closed-loop systems and
the environment transition relation NextENV (which, for example, might be non-
deterministic).
    This paper proposes a compositional method to deal with this problem. The
key idea is the following: instead of checking formula (1) monolithically, we
propose to break it up into two separate conditions:

                       (IndInv ∧ NextNNC ) =⇒ Bridge                           (2)
                       (Bridge ∧ NextENV ) =⇒ IndInv′                          (3)

where Bridge is a new state predicate that needs to be invented (we propose
a technique to do this automatically). Not only are each of the formulas (2)
and (3) smaller than the monolithic formula (1) they can also be handled by the
corresponding specialized tool: formula (2) by a NN verifier, and formula (3) by
an SMT solver.
    In Section 3 we elaborate our approach. We propose a technique to construct
Bridge predicates automatically, and show how this technique can also be used
to establish the validity of Condition (2) by construction. We also present a
heuristic that can falsify inductiveness compositionally in some cases when for-
mula (1) is not valid. We incorporate these techniques into an algorithm that
checks inductiveness of candidate IndInv predicates for NNCSs.
    Our experimental results (Section 4) indicate that our algorithm consistently
terminates, effectively verifying or falsifying the inductiveness of the given can-
didate in both deterministic and non-deterministic environment setups, for NNs
of sizes up to 2 × 1024 neurons, in a matter of seconds. This is in contrast to the
monolithic method, which times out after one hour for all our experiments with
NNs larger than 2 × 56 neurons.


2   Preliminaries and Problem Statement
Symbolic Transition Systems: The systems considered in this paper can be
modeled as symbolic transition systems (STSs), like the ones shown in Figure 1.
An STS is defined by: (1) a set of state variables, each of appropriate type; (2)
a predicate Init over the state variables, specifying the set of possible initial
               Compositional Inductive Invariant Based Verification of NNCSs            3


                                                 State variable : s ∈ Z
                                                 Init : s = 0
                                                 NN function : fNN : Z → R
State variable : s ∈ Z                           NextNNC : a = fNN (s)
Init : s = 0                                     NextENV : (a ≥ 0 =⇒ s′ = 0) ∧
Next : (s = 3 =⇒ s′ = 0) ∧                                  (a < 0 =⇒ s′ = s + 1)
                    ′
      (s ̸= 3 =⇒ s = s + 1)                      Next : NextNNC ∧ NextENV
Safe : 0 ≤ s ≤ 3                                 Safe : 0 ≤ s ≤ 3

      (a) Mod-4 counter                        (b) Mod-4 counter with NN controller

Fig. 1: Two STSs. The one in Fig. 1b is a NNCS: function fNN (defined elsewhere)
models a neural network controller.



states; and (3) a predicate Next over current and next (primed) state variables,
specifying the transition relation of the system. For example, the STS shown in
Figure 1a models a counter modulo-4. This system has one state variable s of
type integer (Z). Its Init predicate specifies that s is initially 0. Next specifies
that at each transition, s is incremented by one until we reach s = 3, upon which
s is reset to 0 (primed variable s′ denotes the value of state variable s at the
next state). The Safe predicate defines the set of safe states (used later).
    A state is an assignment of values to all state variables. We use the notation
x |= P to denote that state x satisfies state predicate P , i.e., that P evaluates
to true once we replace all state variables in P by their values as given by x.
A transition is a pair of states (x, x′ ) that satisfies the predicate Next, denoted
(x, x′ ) |= Next. We also use notation x → x′ instead of (x, x′ ) |= Next, when Next
is clear from context. A trace is an infinite sequence of states x0 , x1 , · · · such that
x0 |= Init and xi → xi+1 for all i ≥ 0. A state x is reachable if there exists a
trace x0 , x1 , · · · , such that x = xi for some i. We use Reach(M ) to denote the
set of all reachable states of an STS M .


Invariants: In this paper we are interested in the verification of safety prop-
erties, and in particular invariants, which are state predicates that hold at all
reachable states. Formally, for an STS M , an invariant is a state predicate Inv
such that Reach(M ) ⊆ {s | s |= Inv}. Predicates s ≥ 0 and 0 ≤ s ≤ 3 are both
invariants of the STS of Figure 1a.


Inductive Invariants: A standard technique for checking whether a given state
predicate Safe is an invariant of a given STS is to come up with an inductive
invariant stronger than Safe, that is, with a state predicate IndInv which satisfies
4       Y. Zhou and S. Tripakis

the following conditions [28]:
                                            Init =⇒ IndInv                       (4)
                                                                ′
                            (IndInv ∧ Next) =⇒ IndInv                            (5)
                                           IndInv =⇒ Safe                        (6)
              ′
where IndInv denotes the predicate IndInv where state variables are replaced
by their primed, next-state versions. Condition (4) states that IndInv holds at
all initial states. Condition (5) states that IndInv is inductive, that is, if IndInv
holds at a state s, then it also holds at any successor of s. We call Condition (5)
the inductiveness condition. Condition (6) states that IndInv is stronger than
Safe. Conditions (4) and (5) imply that all reachable states satisfy IndInv, which
together with Condition (6) implies that they also satisfy Safe.

Neural Networks: At its core, a neural network (NN) is a function, receiving
inputs and producing outputs. Mathematically, the output z (i) of each layer in
a feed-forward NN with L layers can be expressed as:
                  z (i) = σi (W (i) z (i−1) + b(i) ),   i = 1, 2, · · · , L,
where W (i) and b(i) represent the weight matrix and bias vector for the i-th layer,
respectively, and σi is the activation function for that layer. Our paper considers
feed-forward NNs with ReLU activation functions, where ReLU(x) = max(0, x).

Neural Network Controlled Systems: In this paper, we are interested in
safety verification for neural network controlled systems (NNCSs). A NNCS is a
STS consisting of a neural network controller and an environment, in closed-loop
configuration. Formally, a NNCS is a STS whose transition relation predicate
Next is of the form NextNNC ∧ NextENV , where NextNNC is a predicate capturing
the NN controller, and NextENV is a predicate capturing the transition relation
of the environment. We assume that NextNNC is always of the form a = fNN (s),
where fNN is the function modeling the NN controller, s is the vector of state
variables of the environment (which are the inputs to the NN controller), and
a is the vector of outputs of the NN controller (which are the inputs to the
environment). Then, NextENV is a predicate on s, s′ , and a. Note that the only
state variables in the NNCS are s. Variables a are not state variables, but just
temporary variables that can be eliminated and replaced by fNN (s), according
to the equation a = fNN (s). We assume that for any assignment of s and a,
there always exists an assignment of s′ such that NextENV is satisfied; that is,
the system is deadlock-free.
    An example NNCS is shown in Figure 1b. In this simple example, the output
a of the NN controller controls the environment to either reset the state variable
s to 0 (if a ≥ 0) or increment it by 1 (if a < 0).

Safety Verification Problem for NNCS: The problem we study in this
paper is the safety verification problem for NNCS, namely: given a NNCS M
and a safety predicate Safe, check whether Safe is an invariant of M .
             Compositional Inductive Invariant Based Verification of NNCSs        5

3     Our Approach
To solve the safety verification problem for NNCSs, we will use the inductive in-
variant method described in Section 2. In particular, our approach assumes that
a candidate inductive invariant is given, and our focus is to check whether this
candidate is indeed a valid inductive invariant stronger than Safe, i.e., whether
it satisfies Conditions (4), (5), and (6). Specifically, we focus on checking induc-
tiveness, i.e., Condition (5), because this is the most challenging condition to
check.
    In the case of NNCS, Condition (5) instantiates to:

                  (IndInv ∧ NextNNC ∧ NextENV ) =⇒ IndInv′ .                    (7)

A naive approach is to attempt to check Condition (7) directly: we call this the
monolithic method. Unfortunately, as we will show in Section 4, the monolithic
method does not scale. This is typically because of the size of the NextNNC part
of the formula, which encodes the NN controller, and tends to be very large.
To address this challenge, we introduce a compositional method for checking
inductiveness, described next.

3.1   Our Approach: Compositional Method
Our compositional method is centered around two key ideas: (i) automatically
construct a bridge predicate, denoted Bridge; and (ii) replace the monolithic
inductiveness Condition (7) by two separate conditions:

                       (IndInv ∧ NextNNC ) =⇒ Bridge                            (8)
                                                         ′
                       (Bridge ∧ NextENV ) =⇒ IndInv                            (9)

By transitivity of logical implication, it is easy to show the following:
Theorem 1 (Soundness). If Conditions (8) and (9) hold then Condition (7)
holds.
   The completeness of our method follows from the fact that in the worst case
we can set Bridge to be equal to IndInv ∧ NextNNC .
Theorem 2 (Completeness). If Condition (7) holds then we can find Bridge
such that Conditions (8) and (9) hold.
    As it turns out (c.f. Section 4) checking Conditions (8) and (9) separately
scales much better than checking Condition (7) monolithically. However, this
relies on finding a “good” bridge precidate. Setting Bridge to IndInv ∧ NextNNC
is not helpful, because then Condition (9) becomes identical to the monolithic
Condition (7). Thus, a necessary step is finding a bridge predicate that satisfies
Conditions (8) and (9), while remaining manageable. In Section 3.2, we present
an automatic technique for doing so. But first, we examine bridge predicates in
more depth.
6         Y. Zhou and S. Tripakis

Naive Bridge Predicates are Incomplete: A natural starting point for
constructing the bridge predicate is to define it only over the output variables a
of the NN controller. We call this a naive bridge predicate. Unfortunately, naive
bridge predicates might be insufficient, as we show next. Consider the system
shown in Figure 1b. Suppose we set NextNNC to:

((0 ≤ s ≤ 2) ∧ a = −1) ∨ (s = 3 ∧ a = 1) ∨ ((s < 0 ∨ s > 3) ∧ (a = −1 ∨ a = 1))

It can be checked that the set of reachable states of this system is 0 ≤ s ≤ 3.
Therefore, 0 ≤ s ≤ 3 is also an inductive invariant of this system. A naive
bridge predicate that satisfies Condition (8) could be a = 1 ∨ a = −1. This is,
in fact, the strongest naive bridge predicate that satisfies Condition (8), as it
captures all the possible values of a. Therefore, if this naive bridge predicate
does not satisfy Condition (9), then no naive bridge predicate that satisfies both
Conditions (8) and (9) exists. Indeed, Condition (9) is violated by this naive
bridge, as it becomes

         ((a = 1 ∨ a = −1) ∧ (a ≥ 0 =⇒ s′ = 0) ∧ (a < 0 =⇒ s′ = s + 1))
                                                         =⇒ (0 ≤ s′ ≤ 3)

which is false when s = 3, a = −1 and s′ = 4. So, no naive bridge predicate can
satisfy both Condition (8) and (9). This suggests that naive bridge predicates
are insufficient. The solution is to allow bridge predicates to refer both to the
inputs and outputs of the NN controller:

Generalized Bridge Predicates are Complete: A generalized bridge predi-
cate is a predicate defined over both the output variables a as well as the input
variables s of the NN controller (the inputs s are the same as the state variables
of the environment). Continuing our example above, a generalized bridge pred-
icate could be: ((0 ≤ s ≤ 2) ∧ a = −1) ∨ (s = 3 ∧ a = 1). Then, Conditions (8)
and (9) become:


((0 ≤ s ≤ 3) ∧
((0 ≤ s ≤ 2) ∧ a = −1) ∨ (s = 3 ∧ a = 1) ∨ ((s < 0 ∨ s > 3) ∧ (a = −1 ∨ a = 1)))
    =⇒ (((0 ≤ s ≤ 2) ∧ a = −1) ∨ (s = 3 ∧ a = 1))                            (10)


          (((0 ≤ s ≤ 2) ∧ a = −1) ∨ (s = 3 ∧ a = 1)) ∧ (a ≥ 0 =⇒ s′ = 0)
          ∧ (a < 0 =⇒ s′ = s + 1))
           =⇒ (0 ≤ s′ ≤ 3).                                                  (11)

and it can be checked that both are valid, which shows that this generalized
bridge predicate is sufficient.
    In general, and according to Theorem 2, a generalized bridge predicate is
sufficient, since we can set Bridge to IndInv ∧ NextNNC , and the latter predicate
             Compositional Inductive Invariant Based Verification of NNCSs           7

is over s and a. But it is important to note that a bridge that works need not
be the “worst-case scenario” predicate IndInv ∧ NextNNC . Indeed, the bridge of
our example is not, and neither are the bridges constructed by our tool for the
case studies in Section 4.

3.2   Automatic Inference of Generalized Bridge Predicates
The key idea of our automatic bridge inference technique is to synthesize a
generalized bridge predicate such that Condition (8) holds by construction (i.e.,
it does not need to be checked). To explain how this works, let us first define,
given a predicate A over both s and a, and predicate B over only s, the set of
postconditions, denoted AllPosts(A, B), to be the set of all predicates C over a
such that (A ∧ B) =⇒ C is valid.
    Then, our algorithm will construct a bridge predicate the has the form:

                Bridge = (p1 ∧ ψ1 ) ∨ (p2 ∧ ψ2 ) ∨ · · · ∨ (pn ∧ ψn )             (12)

where each pi is a predicate over s, and each ψi is a predicate over a, such that
the following conditions hold:

                    (p1 ∨ p2 ∨ · · · ∨ pn ) ⇐⇒ IndInv                             (13)
                    ∀i = 1, ..., n, ψi ∈ AllPosts(NextNNC , pi )                  (14)

Condition (13) ensures that the set of all pi ’s is a decomposition of the candi-
date inductive invariant IndInv, i.e., that their union, viewed as sets, “covers”
IndInv. This decomposition need not be a partition of IndInv, i.e., the pi ’s need
not be disjoint. Condition (14) ensures that each ψi is a postcondition of the
corresponding pi w.r.t. the NN controller (note that ψi is not necessarily the
strongest postcondition).
    Now, from (12) and (13), Condition (8) becomes:

((p1 ∨ p2 ∨ · · · ∨ pn ) ∧ NextNNC ) =⇒ ((p1 ∧ ψ1 ) ∨ (p2 ∧ ψ2 ) ∨ · · · ∨ (pn ∧ ψn ))

which is equivalent to
                                            !                     
                    n
                    _                                  n
                                                       _
                          (pi ∧ NextNNC )       =⇒        (pj ∧ ψj )            (15)
                    i=1                             j=1

which is equivalent to
                                                                  
                   n
                   ^                               n
                                                   _
                         (pi ∧ NextNNC ) =⇒ (           (pj ∧ ψj ))             (16)
                   i=1                             j=1

But observe that (pi ∧ NextNNC ) =⇒ pi trivially holds, for each i = 1, ..., n.
And note that (pi ∧ NextNNC ) =⇒ ψi also holds, since by construction, ψi ∈
AllPosts(NextNNC , pi ). Therefore, (pi ∧ NextNNC ) =⇒ (pi ∧ ψi ) holds for each
i, which implies that (16) holds by construction. Therefore, we have:
8          Y. Zhou and S. Tripakis

Theorem 3 (Condition (8) holds by construction). For any bridge predi-
cate that is in form of Condition (12), if this predicate satisfies Conditions (13)
and (14), then Condition (8) holds by construction.

      Next, consider Condition (9). From (12), Condition (9) becomes:

                                                               
          (p1 ∧ ψ1 ) ∨ (p2 ∧ ψ2 ) ∨ · · · ∨ (pn ∧ ψn ) ∧ NextENV =⇒ IndInv′
                                                      
                                                                                (17)

which is equivalent to:
                         n
                                                  !
                         _
                               (pi ∧ ψi ∧ NextENV )   =⇒ IndInv′                (18)
                         i=1

which is equivalent to:
                        n
                        ^
                               (pi ∧ ψi ∧ NextENV ) =⇒ IndInv′
                                                                 
                                                                                (19)
                        i=1

which means that checking Condition (9) can be replaced by checking n smaller
conditions, namely, (pi ∧ ψi ∧ NextENV ) =⇒ IndInv′ , for i = 1, ..., n.
   The algorithm that we present below (Algorithm 1) starts with n = 1 and
p1 = IndInv. It then computes some ψ1 ∈ AllPosts(NextNNC , p1 ) and checks
whether (p1 ∧ ψ1 ∧ NextENV ) =⇒ IndInv′ is valid. If it is, then p1 ∧ ψ1 is a valid
bridge and inductiveness holds. Otherwise, p1 is split into several pi ’s, and the
process repeats.


3.3       Heuristic for Falsifying Inductiveness

An additional feature of our algorithm is that it is often capable to falsify in-
ductiveness and thereby prove that it does not hold. This allows us to avoid
searching hopelessly for a bridge predicate when none exists, because the candi-
date invariant is not inductive.
    Directly falsifying Condition (7) faces the same scalability issues as trying to
prove this condition monolithically. On the other hand, falsifying Conditions (8)
or (9) is not sufficient to disprove inductiveness. The failure to prove these con-
ditions might simply mean that our chosen bridge predicate does not work.
    Therefore, we propose a practical heuristic which inherits the decomposition
ideas described above. This heuristic involves constructing: (i) a satisfiable falsi-
fying state predicate over s, denoted FState; and (ii) a predicate over the output
of the NN controller a, denoted FPred, such that the following conditions hold:

                                                FState =⇒ IndInv                (20)
                                   (FState ∧ NextNNC ) =⇒ FPred                 (21)
                     (FState ∧ FPred ∧ NextENV ) =⇒ ¬IndInv′                    (22)
             Compositional Inductive Invariant Based Verification of NNCSs       9

Intuitively, FState identifies a set of states which satisfy IndInv but violate
IndInv′ after a transition. FPred captures the outputs of the NN controller when
its inputs satisfy FState. The conjunction of (21) and (22) implies:

                 (FState ∧ NextNNC ∧ NextENV ) =⇒ ¬IndInv′                    (23)

In turn, (23) and (20) together imply that Condition (7) does not hold. This
leads us to the following theorem:

Theorem 4 (Falsifying Inductiveness). If FState is satisfiable, and if Con-
ditions (20), (21), and (22) hold, then Condition (7) does not hold.

    Our falsification approach aligns well with the composite structure of a
NNCS, and is compositional, because it allows to check separately the NN tran-
sition relation NextNNC in (21) and the environment transition relation NextENV
in (22).

3.4   Algorithm
The aforementioned ideas are combined in Algorithm 1, which implements our
compositional inductiveness verification approach for NNCSs. Line 7 ensures
that ψ is a postcondition of p w.r.t. the NN controller. In practice we use a NN
verifier to compute the postcondition (see Section 4). Lines 15 and 16 ensure
Condition (13), together with the fact that the initial p is IndInv (Line 3).
Line 9 ensures that the bridge predicate is in form of Condition (12). Therefore,
by Theorem 3, Algorithm 1 ensures Condition (8) by construction.
    Line 8 corresponds to checking (19) compositionally, i.e., separately for each
i. In practice, we use an SMT solver for this check (see Section 4).
    For falsification, to use Theorem 4, we set FState = p and FPred = ψ.
The splitting process at Line 15 guarantees that p is satisfiable. Condition (20)
then becomes p =⇒ IndInv, which holds by construction because of Condi-
tion (13). Condition (21) becomes p ∧ NextNNC =⇒ ψ, which holds because
ψ ∈ AllPosts(NextNNC , p). Condition (22) becomes (p ∧ ψ ∧ NextENV ) =⇒
¬IndInv′ , which is checked in Line 11.
    If the algorithm can neither prove (p ∧ ψ ∧ NextENV ) =⇒ IndInv′ , nor falsify
inductiveness, then it splits p into a disjunction of satisfiable state predicates,
ensuring Condition (12). Our implementation utilizes various splitting strategies.
The specific splitting strategies employed in our case studies are elaborated in
Section 4. After splitting, all resulting state predicates are added into the queue
Q. Consequently, the queue becomes empty if and only if the validity of every
conjunct in Condition (19) is proved. Therefore, an empty queue indicates that
inductiveness holds.
Termination: the algorithm terminates either upon successfully proving or
upon falsifying inductiveness. However, termination is not guaranteed in all
cases. In infinite state spaces, the algorithm may keep splitting predicates ad
infinitum. In practice, as observed in our case studies, the algorithm consistently
terminated (see Section 4).
10       Y. Zhou and S. Tripakis


    Algorithm 1: Compositional Inductiveness Checking for NNCS
   Input: Transition relations NextNNC , NextENV ; Candidate Inductive Invariant
          IndInv
   Output: Verification result: (True with bridge predicate Bridge) or (False
             with falsifying state predicate)
 1 Function CheckInductiveness(NextNNC , NextENV , IndInv):
 2    Bridge := F alse ;
 3    Q := {IndInv} ;
 4    while Q ̸= ∅ do
 5        Let p ∈ Q ;
 6        Q := Q \ {p} ;
 7        Let ψ ∈ AllPosts(NextNNC , p) ;
 8        if (p ∧ ψ ∧ NextENV ) =⇒ IndInv′ holds then
 9            Bridge := Bridge ∨ (p ∧ ψ) ;
10        end
11        else if (p ∧ ψ ∧ NextENV ) =⇒ ¬IndInv′ holds then
12            return (False, p) ;
13        end
14        else
15            Split p into p1 , p2 , · · · , pk such that p ⇐⇒ (p1 ∨ p2 ∨ · · · ∨ pk );
16            Q := Q ∪ {p1 , p2 , · · · , pk } ;
17        end
18    end
19    return (True, Bridge) ;



4     Evaluation
In the experiments reported below, we evaluate our compositional method by
comparing it against the monolithic method which uses Z3 to check Condition 7
directly. We remark that we also attempted to use specialized NN verifiers such
as [45] to check inductiveness monolithically, but this proved infeasible. Specif-
ically, we tried two ways of encoding checking inductiveness as an NN verifi-
cation problem: (i) Encoding NextENV and Condition (7) into the NN’s input
and output constraints. This approach was impractical for our case studies since
NextENV involves arithmetic applied simultaneously to both the input and out-
put of the NN controller, e.g., (x′ = x + 0.1a). Such constraints are beyond the
capability of existing NN verifiers such as [5, 25, 26, 45]. (ii) Encoding both the
NN controller and the environment into a single NN. Our trials revealed that
current NN verifiers support only a limited range of operators for defining a
NN, restricting this approach as well. Notably, the operators we required, such
as adding the NN’s input to its output, are not typically supported. Although
these limitations might diminish as NN verifiers evolve, an additional compli-
cation arises from the fact that NextENV might be non-deterministic (as in our
second set of case studies). Encoding non-deterministic transition relations into
a NN remains a significant challenge because NNs are typically deterministic
functions.
             Compositional Inductive Invariant Based Verification of NNCSs      11

    In our evaluation, we do not attempt to systematically compare our tool
against NNCS reachability analysis tools, e.g. [16, 23, 35, 41], primarily because
these tools perform verification over a bounded time horizon through reachability
analysis, while our method is based on inductive invariants and enables the
verification of safety properties over an infinite time horizon. However, following
the recommendation of an anonymous Reviewer, we did execute some of the
aforementioned tools on the 2D maze case studies described in Section 4.2 that
follows. In summary, in many of our experiments, tools such as JuliaReach [6]
and NNV [41] have been able to successfully verify safety within a bounded
time horizon. For example, it took NNV a few seconds to perform a 50-step
reachability analysis on the deterministic 2D maze with the largest NN controller
that we used (2 × 1024 neurons). However, both JuliaReach and NNV also failed
to verify safety in some instances, due to the overapproximation of the reach set.
Our experiments with JuliaReach and NNV are reported in Appendix A.

4.1   Implementation and Experimental Setup
We implemented Algorithm 1 in a prototype tool – the source code and models
needed to reproduce our experiments are available at https://github.com/Y
UH-Z/comp-indinv-verif ication-nncs. We use the SMT solver Z3 [9] for the
validity checks of Lines 8 and 11 of Algorithm 1. To compute the postcondition
ψ (Line 7 of Algorithm 1), we use AutoLIRPA [46], which is the core engine of
the NN verifier α-β-CROWN [45]. AutoLIRPA computes a postcondition ψ ∈
AllPosts(NextNNC , p), i.e., guarantees that (p ∧ NextNNC ) =⇒ ψ, but it does
not generally guarantee that ψ is the strongest possible postcondition.
    In our case studies reported below, each candidate inductive invariant is a
union of hyperrectangles, which aligns with the constraint types supported by
mainstream NN verifiers such as [5, 25, 26, 45].
    Our splitting strategy (Line 15 of Algorithm 1) follows a binary scheme,
dividing hyperrectangles at their midpoints along each dimension. For example,
the interval [1, 2] would be split into [1, 3/2] and [3/2, 2]. This straightforward
strategy turns out to be effective in our case studies.
    Our experiments were conducted on a machine equipped with a 3.3 GHz
8-core AMD CPU, 16 GB memory, and an Nvidia 3060 GPU. Z3 ran on the
CPU and AutoLIRPA on the GPU with CUDA enabled, both using default
configurations.

4.2   Case Studies and Experimental Results
We ran our experiments on two sets of examples, a deterministic 2D maze, and
a non-deterministic 2D maze, as described below.
    Deterministic 2D maze: In this example, the environment has two state
variables x and y of type real (R), representing an object’s 2D position. The
NN controller fNN : R2 → R2 outputs (a, b) = fNN (x, y), guiding the object’s
horizontal and vertical movement. The initial state is set within 0.3 ≤ x ≤
0.4 and 0.6 ≤ y ≤ 0.7. The transition relation NextENV of the environment is
12     Y. Zhou and S. Tripakis


Table 1: Experimental results: Det and NDet indicate the results for the deter-
ministic and non-deterministic 2D maze case studies, respectively. All execution
times are in seconds. T.O. represents an one-hour timeout. The Verified? col-
umn shows whether the compositional method successfully terminated, either by
proving (T) or by disproving (F) inductiveness. #Splits reports the total number
of splits performed. #SMT and #NNV queries report the total number of calls
made to Z3 and AutoLIRPA, respectively.
                   Monolithic     Compositional           #SMT     #NNV
           Verified?                             #Splits
 NN size           execution time execution time          queries  queries
          Det NDet Det     NDet Det NDet         Det NDet Det NDet Det NDet
 2 × 32 T T        51.59 39.73 0.73 0.83         12 14    61 71    49 57
 2 × 40 T T        113.69 296.61 0.70 0.66       13 13    66 66    53 53
 2 × 48 T T        410.14 3002.20 0.52 0.42      10 8     51 41    41 33
 2 × 56 T T        1203.76 T.O.   0.42 0.46      8 9      41 46    33 37
 2 × 64 T T        T.O.    T.O.   0.76 0.61      15 12    76 61    61 49
 2 × 128 F T       T.O.    T.O.   2.21 1.43      64 28    225 141 160 113
 2 × 256 T T       T.O.    T.O.   1.68 1.18      27 23    136 116 109 93
 2 × 512 T T       T.O.    T.O.   3.04 2.30      60 45    301 226 241 181
 2 × 1024 T T      T.O.    T.O.   1.94 5.23      38 102 191 511 153 409



deterministic and defined by x′ = x + 0.1a and y ′ = y + 0.1b. The controller’s
goal is to navigate the object to (0.8 ≤ x ≤ 0.9 and 0.8 ≤ y ≤ 0.9), while keeping
it within a safe region of (0.22 ≤ x ≤ 0.98 and 0.54 ≤ y ≤ 0.98), which is the
safety property we want to prove.
    As NN controllers, we used two-layer feed-forward NNs with ReLU acti-
vations, trained via PyTorch [31] and Stable-Baselines3 [33]. We trained NN
controllers of various sizes, ranging from 2 × 32 to 2 × 1024 neurons. To stan-
dardize the comparison among the systems containing different NN controllers,
for each system, we check the same candidate inductive invariant, defined as
0.25 ≤ x ≤ 0.95 and 0.55 ≤ y ≤ 0.95. For this candidate and for the Init and
Safe predicates defined above, it is easy to see that Conditions (4) and (6) hold.
So our experiments only check the inductiveness Condition (7).
    The results are reported in Table 1: for this case study, the relevant columns
are those marked as Det. The compositional method successfully terminated in
all cases, and proved inductiveness for all NN configurations, except for 2 × 128,
for which inductiveness does not hold, and in which case the compositional
method managed to falsify it. In terms of performance, the monolithic method
requires around one minute even for the smallest NN configurations, and times
out after one hour for the larger configurations; while the compositional method
terminates in all cases in a couple of seconds. A key metric of the compositional
method is the number of splits, which is determined by the number of times
Line 15 of Algorithm 1 is executed. This metric is crucial as it impacts the
number of queries made to the SMT solver and to the NN verifier, typically the
most time-consuming steps in the algorithm. Additionally, the number of splits
             Compositional Inductive Invariant Based Verification of NNCSs        13

indicates the size of the bridge predicate, where fewer splits suggest smaller
bridge predicates.
    Non-deterministic 2D maze: This case study is similar to the determin-
istic 2D maze, with the difference that the environment’s transition relation is
non-deterministic, specifically, defined as x′ = x + 0.1c · a and y ′ = y + 0.1c · b,
where c is a constant of type real, non-deterministically ranging between 0.5 and
1.0. This non-determinism simulates the noise within the system.
    The NN controllers in this set of experiments, while maintaining the same
architecture and size as in the deterministic case studies, were retrained from
scratch to adapt to the new transition relation. The candidate inductive invari-
ant is the same as in the deterministic case study, ensuring consistency in our
comparative analysis.
    The results are shown in Table 1, columns marked by NDet. As demonstrated
by the results, our compositional method successfully verified inductiveness in
all configurations, in a matter of seconds.


5   Related Work

A large body of research exists on NN verification, including methods that verify
NN input-output relations, using SMT solvers [22, 25, 26] or MILP solvers [40],
as well as methods that employ abstract-interpretation techniques [17, 38], sym-
bolic interval propagation [44], dual optimization [13], linear relaxation [46], and
bound propagation [45]. [29] formally verifies equivalence and adversarial robust-
ness of binarized NNs by SAT solvers. [14] propose an SMT based approach for
checking equivalence and approximate equivalence of NNs.
    These and other techniques and the corresponding tools focus on NN verifi-
cation at the component level, that is, they verify a NN in isolation. In contrast,
we focus on system-level verification, that is, verification of a closed-loop system
consisting of a NN controller and an environment.
    System-level verification approaches have also been proposed in the litera-
ture. A number of methods capture NNCSs as hybrid systems: in [24] the NN is
transformed into a hybrid system and the existing tool Flow* [7] is used to verify
the resulting hybrid system. In [21] the NN is approximated using Bernstein poly-
nomials, while [23] employs Taylor models, and uses various techniques to reduce
error. In [15] NNCSs are modeled as transition systems, and existing NN verifiers
like Marabou [26] are used for bounded model checking. These methods are adept
at proving safety properties within a bounded time horizon. The ARCH-COMP
series of competitions includes categories for verifying continuous and hybrid
systems with neural network components [27]. The tools [2, 6, 12, 16, 20, 24, 41]
that participated in these competitions are designed to verify properties within
a bounded time horizon by reachability analysis. In contrast, our approach is
designed to verify safety properties over an infinite time horizon using inductive
invariants instead of reachability. Also, our approach works for a discrete-time
rather than continuous-time model. In [4], the authors perform time-unbounded
safety verification of NNCS within a conventional reinforcement learning setting
14     Y. Zhou and S. Tripakis

that features a finite set of possible actions by computing polyhedral overap-
proximations of the reach set using MILP techniques. In contrast, our method
does not assume a finite action space and uses inductive invariants.
    Our approach can handle non-deterministic environments. While the non-
deterministic case is less studied than deterministic NNCSs, some of the tools
mentioned above, e.g., [2, 41], can also handle non-determinism, albeit with a
fundamentally different technique than ours (reachability instead of inductive
invariants). The verification of non-deterministic NNCSs has also been studied
in [1], which leverages MILP solvers for the verification task.
    In addition to verification, various methods for testing NNCSs have been ex-
plored. Simulation-based approaches for NNCS analysis, including falsification,
fuzz testing, and counterexample analysis, were introduced by [11, 42]. [19] pro-
posed a method to explore the state space of hybrid systems containing neural
networks.
    Our work is also related to research on automatic inductive invariant dis-
covery, which is a hard, generally undecidable, problem [30]. Recently, several
studies have proposed techniques for automatic inductive invariant discovery
for distributed protocols [18, 36], while [34] applies deep learning techniques to
infer loop invariants for programs. [3] proposes a heuristic for inferring simple
inductive invariants in NNCSs, within the context of communication network-
ing systems. Such systems possess unique traits not commonly found in general
NNCSs. These specific traits enable using a NN verifier to check a weaker con-
dition instead of directly verifying the inductiveness condition. In contrast, our
method does not depend on specific properties of specialized NNCSs.
    Our work is also related to barrier certificates, an alternative technique for
verifying continuous-time systems [32, 39]. In [43] the authors synthesize barrier
certificates by solving an optimization problem subject to bilinear matrix in-
equalities. In [10] the authors propose a method that uses barrier certificates to
synthesize neural network controllers which are safe by design. [37] presents an
approach to verifying NNCSs by constructing barrier certificates.


6    Conclusions

We present a compositional, inductive-invariant based method for NNCS veri-
fication. Our method allows to to verify safety properties over an infinite time
horizon. The key idea is to decompose the monolithic inductiveness check (which
is typically not supported by state-of-the-art NN verifiers, and does not scale
with state-of-the-art SMT solvers) into several manageable subproblems, which
can be each individually handled by the corresponding tool. Our case studies
show encouraging results where the verification time is reduced from hours (or
timeout) to seconds.
    Future work includes augmenting our method’s capabilities to suit a broader
range of NNCS applications. We also plan to explore the automatic generation
of candidate inductive invariants (in addition to bridges) for NNCSs.
              Compositional Inductive Invariant Based Verification of NNCSs           15

Acknowledgments

We would like to thank the anonymous Reviewers of the submitted version of
this paper for their helpful feedback. This work has been supported in part by
NSF CCF award #2319500.


References

 1. Akintunde, M.E., Botoeva, E., Kouvaros, P., Lomuscio, A.: Formal verification of
    neural agents in non-deterministic environments. Autonomous Agents and Multi-
    Agent Systems (2022)
 2. Althoff, M.: An introduction to CORA 2015. In: Proc. of the Workshop on Applied
    Verification for Continuous and Hybrid Systems (2015)
 3. Amir, G., Schapira, M., Katz, G.: Towards scalable verification of deep reinforce-
    ment learning. In: Formal Methods in Computer Aided Design (FMCAD) (2021)
 4. Bacci, E., Giacobbe, M., Parker, D.: Verifying reinforcement learning up to infinity.
    In: Proceedings of the International Joint Conference on Artificial Intelligence.
    International Joint Conferences on Artificial Intelligence Organization (2021)
 5. Bak, S.: nnenum: Verification of ReLU neural networks with optimized abstraction
    refinement. In: NASA Formal Methods Symposium (2021)
 6. Bogomolov, S., Forets, M., Frehse, G., Potomkin, K., Schilling, C.: JuliaReach: a
    toolbox for set-based reachability. In: Proceedings of the 22nd ACM International
    Conference on Hybrid Systems: Computation and Control (2019)
 7. Chen, X., Ábrahám, E., Sankaranarayanan, S.: Flow*: An analyzer for non-linear
    hybrid systems. In: Computer Aided Verification (2013)
 8. Clarke, E.M., Henzinger, T.A., Veith, H., Bloem, R. (eds.): Handbook of Model
    Checking. Springer (2018)
 9. De Moura, L., Bjørner, N.: Z3: An efficient smt solver. In: International conference
    on Tools and Algorithms for the Construction and Analysis of Systems (2008)
10. Deshmukh, J.V., Kapinski, J.P., Yamaguchi, T., Prokhorov, D.: Learning deep
    neural network controllers for dynamical systems with safety guarantees. In: 2019
    IEEE/ACM International Conference on Computer-Aided Design (ICCAD). IEEE
    (2019)
11. Dreossi, T., Fremont, D.J., Ghosh, S., Kim, E., Ravanbakhsh, H., Vazquez-
    Chanlatte, M., Seshia, S.A.: VerifAI: A toolkit for the formal design and analysis of
    artificial intelligence-based systems. In: Computer Aided Verification (CAV) (Jul
    2019)
12. Dutta, S., Chen, X., Jha, S., Sankaranarayanan, S., Tiwari, A.: Sherlock-a tool for
    verification of neural network feedback systems: demo abstract. In: Proceedings
    of the 22nd ACM International Conference on Hybrid Systems: Computation and
    Control (2019)
13. Dvijotham, K., Stanforth, R., Gowal, S., Mann, T.A., Kohli, P.: A dual approach
    to scalable verification of deep networks. In: UAI (2018)
14. Eleftheriadis, C., Kekatos, N., Katsaros, P., Tripakis, S.: On neural network equiv-
    alence checking using SMT solvers. In: 20th International Conference on Formal
    Modeling and Analysis of Timed Systems (FORMATS 2022) (2022)
15. Eliyahu, T., Kazak, Y., Katz, G., Schapira, M.: Verifying learning-augmented sys-
    tems. In: Proceedings of the 2021 ACM SIGCOMM 2021 Conference (2021)
16      Y. Zhou and S. Tripakis

16. Fan, J., Huang, C., Chen, X., Li, W., Zhu, Q.: ReachNN*: A Tool for Reachability
    Analysis of Neural-Network Controlled Systems. In: Automated Technology for
    Verification and Analysis (2020)
17. Gehr, T., Mirman, M., Drachsler-Cohen, D., Tsankov, P., Chaudhuri, S., Vechev,
    M.: Ai2: Safety and robustness certification of neural networks with abstract in-
    terpretation. In: 2018 IEEE symposium on security and privacy (SP) (2018)
18. Goel, A., Sakallah, K.: On Symmetry and Quantification: A New Approach to
    Verify Distributed Protocols. In: NASA Formal Methods Symposium (2021)
19. Goyal, M., Duggirala, P.S.: Neuralexplorer: state space exploration of closed loop
    control systems using neural networks. In: Automated Technology for Verification
    and Analysis: 18th International Symposium, ATVA 2020. Springer (2020)
20. Huang, C., Fan, J., Chen, X., Li, W., Zhu, Q.: POLAR: A polynomial arithmetic
    framework for verifying neural-network controlled systems. In: International Sym-
    posium on Automated Technology for Verification and Analysis. Springer (2022)
21. Huang, C., Fan, J., Li, W., Chen, X., Zhu, Q.: ReachNN: Reachability analysis of
    neural-network controlled systems. ACM Transactions on Embedded Computing
    Systems (TECS) (2019)
22. Huang, X., Kwiatkowska, M., Wang, S., Wu, M.: Safety Verification of Deep Neural
    Networks. In: Computer Aided Verification (2017)
23. Ivanov, R., Carpenter, T., Weimer, J., Alur, R., Pappas, G., Lee, I.: Verisig 2.0:
    Verification of neural network controllers using taylor model preconditioning. In:
    Computer Aided Verification (2021)
24. Ivanov, R., Weimer, J., Alur, R., Pappas, G.J., Lee, I.: Verisig: verifying safety
    properties of hybrid systems with neural network controllers. In: Proceedings of
    the 22nd ACM International Conference on Hybrid Systems: Computation and
    Control (2019)
25. Katz, G., Barrett, C., Dill, D.L., Julian, K., Kochenderfer, M.J.: Reluplex: An
    efficient smt solver for verifying deep neural networks. In: Computer Aided Verifi-
    cation (2017)
26. Katz, G., Huang, D.A., Ibeling, D., Julian, K., Lazarus, C., Lim, R., Shah, P.,
    Thakoor, S., Wu, H., Zeljić, A., et al.: The marabou framework for verification and
    analysis of deep neural networks. In: Computer Aided Verification: 31st Interna-
    tional Conference, CAV 2019 (2019)
27. Lopez, D.M., Althoff, M., Forets, M., Johnson, T.T., Ladner, T., Schilling, C.:
    ARCH-COMP23 category report: Artificial intelligence and neural network control
    systems (AINNCS) for continuous and hybrid systems plants. In: Proceedings of
    10th International Workshop on Applied Verification of Continuous and Hybrid
    Systems (ARCH23). EPiC Series in Computing (2023)
28. Manna, Z., Pnueli, A.: Temporal Verification of Reactive Systems: Safety. Springer-
    Verlag, New York (1995)
29. Narodytska, N., Kasiviswanathan, S., Ryzhyk, L., Sagiv, M., Walsh, T.: Verify-
    ing properties of binarized deep neural networks. In: Proceedings of the AAAI
    Conference on Artificial Intelligence (2018)
30. Padon, O., Immerman, N., Shoham, S., Karbyshev, A., Sagiv, M.: Decidability of
    inferring inductive invariants. ACM SIGPLAN Notices (2016)
31. Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., Killeen,
    T., Lin, Z., Gimelshein, N., Antiga, L., et al.: Pytorch: An imperative style, high-
    performance deep learning library. Advances in neural information processing sys-
    tems (2019)
              Compositional Inductive Invariant Based Verification of NNCSs             17

32. Prajna, S., Jadbabaie, A.: Safety verification of hybrid systems using barrier certifi-
    cates. In: International Workshop on Hybrid Systems: Computation and Control.
    Springer (2004)
33. Raffin, A., Hill, A., Gleave, A., Kanervisto, A., Ernestus, M., Dormann, N.: Stable-
    baselines3: Reliable reinforcement learning implementations. Journal of Machine
    Learning Research (2021)
34. Ryan, G., Wong, J., Yao, J., Gu, R., Jana, S.: CLN2INV: learning loop invariants
    with continuous logic networks. arXiv preprint arXiv:1909.11542 (2019)
35. Schilling, C., Forets, M., Guadalupe, S.: Verification of neural-network control
    systems by integrating Taylor models and zonotopes. In: AAAI (2022)
36. Schultz, W., Dardik, I., Tripakis, S.: Plain and simple inductive invariant inference
    for distributed protocols in TLA+. In: Formal Methods in Computer-Aided Design
    (FMCAD) (2022)
37. Sha, M., Chen, X., Ji, Y., Zhao, Q., Yang, Z., Lin, W., Tang, E., Chen, Q., Li, X.:
    Synthesizing barrier certificates of neural network controlled continuous systems
    via approximations. In: ACM/IEEE Design Automation Conference. IEEE (2021)
38. Singh, G., Gehr, T., Mirman, M., Püschel, M., Vechev, M.: Fast and effective
    robustness certification. Advances in neural information processing systems 31
    (2018)
39. Sogokon, A., Ghorbal, K., Tan, Y.K., Platzer, A.: Vector barrier certificates and
    comparison systems. In: International Symposium on Formal Methods. Springer
    (2018)
40. Tjeng, V., Xiao, K.Y., Tedrake, R.: Evaluating robustness of neural networks with
    mixed integer programming. In: ICLR (2019)
41. Tran, H.D., Yang, X., Manzanas Lopez, D., Musau, P., Nguyen, L.V., Xiang, W.,
    Bak, S., Johnson, T.T.: NNV: the neural network verification tool for deep neural
    networks and learning-enabled cyber-physical systems. In: International Confer-
    ence on Computer Aided Verification. Springer (2020)
42. Viswanadha, K., Kim, E., Indaheng, F., Fremont, D.J., Seshia, S.A.: Parallel and
    multi-objective falsification with scenic and verifai. In: Runtime Verification: 21st
    International Conference (2021)
43. Wang, Q., Chen, M., Xue, B., Zhan, N., Katoen, J.P.: Synthesizing invariant barrier
    certificates via difference-of-convex programming. In: International Conference on
    Computer Aided Verification. Springer (2021)
44. Wang, S., Pei, K., Whitehouse, J., Yang, J., Jana, S.: Formal security analysis of
    neural networks using symbolic intervals. In: 27th USENIX Security Symposium
    (USENIX Security 18). USENIX Association (2018)
45. Wang, S., Zhang, H., Xu, K., Lin, X., Jana, S., Hsieh, C.J., Kolter, J.Z.: Beta-
    crown: Efficient bound propagation with per-neuron split constraints for neural
    network robustness verification. Advances in Neural Information Processing Sys-
    tems (2021)
46. Xu, K., Shi, Z., Zhang, H., Wang, Y., Chang, K.W., Huang, M., Kailkhura, B., Lin,
    X., Hsieh, C.J.: Automatic perturbation analysis for scalable certified robustness
    and beyond. Advances in Neural Information Processing Systems (2020)
47. Zhang, J., Li, J.: Testing and verification of neural-network-based safety-critical
    control software: A systematic literature review. Information and Software Tech-
    nology (2020)
48. Zhou, Y., Tripakis, S.: Compositional Inductive Invariant Based Verification of
    Neural Network Controlled Systems. In: 16th NASA Formal Methods Symposium
    (NFM 2024) (2024)
18        Y. Zhou and S. Tripakis

Appendix

A       Experiments with JuliaReach and NNV
As mentioned in Section 4, following the recommendation of an anonymous Re-
viewer of the conference version of this paper [48], we performed some exper-
iments with NNCS reachability analysis tools, specifically, with JuliaReach [6]
and NNV [41]. In this section, we present a summary of these experimental re-
sults. We utilize the deterministic 2D maze case study, as discussed in Section 4,
to assess the performance of these tools. All necessary files and instructions to
reproduce the results are available at https://github.com/YUH-Z/comp-indin
v-verification-nncs.

A.1      Model conversion
Our tool is designed to work with PyTorch models for the controller, with the
environment modeled within a Python file. However, JuliaReach and NNV re-
quire different formats for both the controller and the environment. While the
environment can be manually implemented in Julia and Matlab, converting the
NN controller into a format compatible with JuliaReach and NNV is necessary.
    Figure 2 illustrates the conversion process. The conversion begins by convert-
ing the pretrained PyTorch model into the ONNX format, utilizing PyTorch’s
native ONNX exporter. NNV then employs its ONNX importer to translate
the ONNX model into NNV’s proprietary format. Additionally, NNV offers a
discrete environment model, allowing us to represent our environment directly.
With the model and environment thus prepared, we proceed to perform a 50-step
reachability analysis.
    JuliaReach also offers an ONNX importer capable of converting a limited
subset of ONNX models into JuliaReach’s internal format. Unfortunately, the
ONNX models exported directly from our PyTorch models are incompatible
with this importer. Consequently, we developed a converter to transform the
ONNX files into NNet files, a format compatible with JuliaReach. While the
NNet repository1 does contain an ONNX converter, it does not support our
ONNX models due to the presence of unsupported operators. Our converter
builds upon NNet’s existing ONNX converter, extending its functionality to
support these operators.
    We evaluated the ONNX to NNet converter by comparing the output of the
ONNX model with that of the NNet model converted from the same ONNX
model. To conduct the assessment, we generated one million uniformly dis-
tributed input vectors for each NN controller configuration. Subsequently, we
computed the absolute difference between the outputs of the ONNX and NNet
models for each input vector. The largest difference observed across all NN con-
troller configurations and input vectors was on the order of 10−6 , which we
considered acceptable for our purposes. (The origin of this difference is unclear.
1
     https://github.com/sisl/NNet
              Compositional Inductive Invariant Based Verification of NNCSs     19

Considering that the converter maintains consistent precision in floating-point
representation, it is possible that the difference in the output values arises from
differences in operator implementation between the ONNX and NNet libraries.)
    To model the environment in JuliaReach, which does not natively support
reachability analysis on discrete-time systems, we represented the deterministic
2D maze as a continuous-time system, aligning with the continuous-discrete
conversion strategy used in ARCH-COMP [27]. This continuous-time system
has a time increment of 1.0 and the following dynamics:

                               ẋ = 0.1a,   ẏ = 0.1b,                        (24)

where x and y represent the state variables, and a and b are control inputs
produced by the NN controller. Following a procedure similar to the NNV setup,
we conducted a reachability analysis on this system from time 0 to time 50.



   PyTorch                      PyTorch
    ONNX                         Model
   Exporter                                                      Our Tool

                                       Environment
                                        in Python




                              NNV ONNX
    ONNX                       Importer
    Model                                                       NNV Engine


                                       Environment
                                        in Matlab
    ONNX
   to NNet
  Converter


                               NNet Model
                                                                JuliaReach


                                       Environment
                                         in Julia


Fig. 2: Overview of converting our models into formats compatible with NNV
and JuliaReach.
20      Y. Zhou and S. Tripakis

A.2    Experimental results

The experimental results using NNV and JuliaReach are shown in Figures 3
and 4, respectively. In these figures, the green regions indicate the area deemed
safe, the orange regions indicate the initial states, and the yellow regions rep-
resent the (approximated) reach sets computed by the tools. In every scenario,
both NNV and JuliaReach completed the reachability analysis within a few sec-
onds.
    NNV failed to verify safety for NN controllers with configurations of 2 × 40
and 2 × 512 neurons. Specifically, as shown in Figures 3b and 3h, the reach sets
computed by NNV are not subsets of the safe regions. This is evident in the top
right corners of the figures, where the yellow boxes exceed the boundaries of the
green region. Consequently, NNV cannot prove that all reachable states, within
a maximum of 50 steps from the initial state, satisfy the safety property, even
though this is indeed the case (as the inductive invariant method shows).
    JuliaReach failed to verify safety for NN controllers with configurations of
2 × 512 and 2 × 1024 neurons. In both Figures 4h and 4i, the yellow boxes exceed
the boundaries of the green regions.
    The inability of NNV and JuliaReach to prove safety in some cases is at-
tributed to the over-approximation errors introduced by the reachability analysis
performed by these tools. In contrast, the inductive invariant method is exact. As
detailed in Section 4, our tool managed to verify safety across all tested scenarios
in a few seconds, demonstrating the effectiveness of our proposed method.
            Compositional Inductive Invariant Based Verification of NNCSs   21




                                   (a) 2 × 32




                                   (b) 2 × 40




                                   (c) 2 × 48

Fig. 3: NNV reachability analysis results for deterministic 2D maze, with sub-
captions denoting the number of neurons in the NN controllers.
22     Y. Zhou and S. Tripakis




                                  (d) 2 × 56




                                  (e) 2 × 64




                                  (f) 2 × 128

Fig. 3: NNV reachability analysis results for deterministic 2D maze, with sub-
captions denoting the number of neurons in the NN controllers.
            Compositional Inductive Invariant Based Verification of NNCSs   23




                                  (g) 2 × 256




                                  (h) 2 × 512




                                  (i) 2 × 1024

Fig. 3: NNV reachability analysis results for deterministic 2D maze, with sub-
captions denoting the number of neurons in the NN controllers.
24     Y. Zhou and S. Tripakis




                                   (a) 2 × 32




                                   (b) 2 × 40




                                   (c) 2 × 48

Fig. 4: JuliaReach reachability analysis results for deterministic 2D maze, with
subcaptions denoting the number of neurons in the NN controllers.
            Compositional Inductive Invariant Based Verification of NNCSs    25




                                   (d) 2 × 56




                                   (e) 2 × 64




                                   (f) 2 × 128

Fig. 4: JuliaReach reachability analysis results for deterministic 2D maze, with
subcaptions denoting the number of neurons in the NN controllers.
26     Y. Zhou and S. Tripakis




                                  (g) 2 × 256




                                  (h) 2 × 512




                                  (i) 2 × 1024

Fig. 4: JuliaReach reachability analysis results for deterministic 2D maze, with
subcaptions denoting the number of neurons in the NN controllers.
