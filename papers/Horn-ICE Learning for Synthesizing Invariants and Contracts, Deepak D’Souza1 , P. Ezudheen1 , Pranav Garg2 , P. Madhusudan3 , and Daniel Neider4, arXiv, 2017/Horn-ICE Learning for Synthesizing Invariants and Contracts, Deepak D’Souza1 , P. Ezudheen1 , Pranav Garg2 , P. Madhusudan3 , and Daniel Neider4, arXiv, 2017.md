                                             Horn-ICE Learning for Synthesizing Invariants and Contracts

                                                    Deepak D’Souza1 , P. Ezudheen1 , Pranav Garg2 , P. Madhusudan3 , and Daniel Neider4
                                                                  1
                                                                  CSA Department, Indian Institute of Science, Bangalore, India
                                                                               2
                                                                                 Amazon India, Bangalore, India
                                                       3
                                                         Department of Computer Science, University of Illinois, Urbana-Champaign, IL, USA
                                                              4
                                                                Max Planck Institute for Software Systems, Kaiserslautern, Germany
arXiv:1712.09418v1 [cs.LO] 26 Dec 2017




                                                Abstract. We design learning algorithms for synthesizing invariants using Horn implication coun-
                                                terexamples (Horn-ICE), extending the ICE-learning model. In particular, we describe a decision-tree
                                                learning algorithm that learns from Horn-ICE samples, works in polynomial time, and uses statistical
                                                heuristics to learn small trees that satisfy the samples. Since most verification proofs can be modeled
                                                using Horn clauses, Horn-ICE learning is a more robust technique to learn inductive annotations that
                                                prove programs correct. Our experiments show that an implementation of our algorithm is able to
                                                learn adequate inductive invariants and contracts efficiently for a variety of sequential and concurrent
                                                programs.


                                         1    Introduction

                                         Synthesizing inductive invariants, including loop invariants, pre/post contracts for functions, and rely-
                                         guarantee contracts for concurrent programs, is one of the most important problems in program verification.
                                         In deductive verification, this is often done by the verification engineer, and automating invariant synthesis
                                         can significantly reduce the burden of building verified software, allowing the engineer to focus on the more
                                         complex specification and design aspects of the code. In completely automated verification, where verification
                                         is typically deployed for simple specifications, checking the validity of verification conditions of recursion-free
                                         code has been mostly automated using constraint logic solving, and coupled with invariant synthesis gives
                                         completely automated verification.
                                             There are several techniques for finding inductive invariants, including abstract interpretation [9], pred-
                                         icate abstraction [1], interpolation [26,23], and IC3 [6]. These techniques are typically white-box techniques
                                         that carefully examine the program, evaluating it symbolically or extracting unsatisfiable cores from proofs
                                         of unreachability of error states in a bounded number of steps in order to synthesize an inductive invariant
                                         that can prove the program correct.
                                             A new class of black-box techniques based on learning has emerged in recent years to synthesize inductive
                                         invariants [16,17]. In this technique, there are two distinct agents, the Learner and the Teacher. In each round
                                         the Learner proposes an invariant for the program, and the Teacher, with access to a verification engine,
                                         checks whether the invariant proves the program correct. If not, it synthesizes concrete counterexamples that
                                         witness why the invariant is inadequate and sends it back to the learner. The learner takes all such samples
                                         the teacher has given in all the rounds to synthesize the next proposal for the invariant. The salient difference
                                         in the black-box approach is that the Learner synthesizes invariants from concrete sample configurations of
                                         the program, and is otherwise oblivious to the program or its semantics.
                                             It is tempting to think that the learner can learn invariants using positively and negatively labeled
                                         configurations, similar to machine learning. However, Garg et al [16] argued that we need a richer notion of
                                         samples for robust learning of inductive invariants. Let us recall this simple argument.
                                             Consider a system with variables x, with initial states captured by a predicate Init(x), and a transition
                                         relation captured by a predicate Trans(x, x′ ), and assume we want to prove that the system does not reach
                                         a set of bad/unsafe states captured by the predicate Bad(x). An inductive invariant I(s) that proves this
                                         property needs to satisfy three constraints:

                                          – ∀x.Init(x) ⇒ I(x);
 – ∀x. ¬(I(x) ∧ Bad(x)); and
 – ∀x, x′ .I(x) ∧ Trans(x, x′ ) ⇒ I(x′ ).

    When a proposed invariant fails to satisfy the first two conditions, the verification engine can indeed
come up with configurations labeled positive and negative to indicate ways to correct the invariant. However,
when the third property above fails, it cannot come up with a single configuration labeled positive/negative;
and the most natural counterexample is a pair of configurations c and c′ , with the instruction to the learner
that if I(c) holds, then I(c′ ) must also hold. These are called implication counterexamples and the ICE
(Implication Counter-Example) learning framework developed by Garg et al. is a robust learning framework
for synthesizing invariants [16]. Garg et al. define several learning algorithms for learning invariant synthesis,
in particular learning algorithms based on decision trees that can learn Boolean combinations of Boolean
predicates and inqualities that compare numerical predicates to arbitrary thresholds [17].
    Despite the argument above, it turns out that implication counterexamples are not sufficient for learning
invariants in program verification settings. This is because reasoning in program verification is more stylized,
to deal compositionally with the program. In particular, programs with function calls and/or concurrency
are not amenable to the above form of reasoning. In fact, it turns out that most reasoning in program
verification can be expressed in terms of Horn clauses, where the Horn clauses have some formulas that need
to be synthesized.
    For example, consider the imperative program snippet:

                                 Ipre (x, y) S(mod x); y := foo(x); Ipost (x, y)

that we want to show correct, where S is some straight-line program that modifies x, Ipre and Ipost are some
annotation (like the contract of a function we are synthesizing. Assume that we are synthesizing the contract
for foo as well, and assume the post-condition for foo is P ostF oo(res, x), where res denotes the result it
returns. Then the verification condition that we want to be valid is

                         (Ipre (x, y) ∧ TransS (x, x′ ) ∧ PostFoo(y ′ , x′ )) ⇒ Ipost (x′ , y ′ ),

where TransS captures the logical semantics of the snippet S in terms of how it affects the post-state of x.
    In the above, all three of the predicates Ipre , Ipost and PostFoo need to be synthesized. When a learner
proposes concrete predicates for these, the verifier checking the above logical formula may find it to be invalid,
and find concrete valuations vx , vy , vx′ , vy′ for x, y, x′ , y ′ that makes the above implication false. However,
notice that the above cannot be formulated as a simple implication constraint. The most natural constraint
to return to the learner is
                                                                       
                               Ipre (vx , vvy ) ∧ PostFoo(vy′ , vx′ ) ⇒ Ipost (vx′ , vy′ ),

asking the learner to meet this requirement when coming up with predicates in the future. The above is best
seen as a Horn Implication CounterExample (Horn-ICE).
    The primary goal of this paper is to build Horn-ICE (Horn implication counterexample) learners for
learning predicates that facilitate inductive invariant and contract synthesis for proving safety properties
of programs. It has been observed in the literature that most program verification mechanisms can be
stated in terms of proof rules that resemble Horn clauses [18]; in fact, the formalism of constrained Horn
clauses has emerged as a robust general mechanism for capturing program verification problems in logic [21].
Consequently, whenever a Horn clause fails, it results in a Horn-ICE sample that can be communicated
to the learner, making Horn-ICE learners a much more general mechanism for synthesizing invariants and
contracts.
    Our main technical contribution is to devise a decision-tree based Horn-ICE algorithm. Given a set
of (Boolean) predicates over configurations of programs and numerical functions that map configurations to
integers, the goal of the learning algorithm is to synthesize predicates that are arbitrary Boolean combinations
of the Boolean predicates and atomic predicates of the form n ≤ c, where n denotes a numerical function,
where c is arbitrary. The classical decision-tree learning algorithm learns such predicates from samples labeled

                                                            2
+/− only [34], and the work by Garg et al extends decision-tree learning to learning from ICE-samples [17].
In this work, we extend the latter algorithm to one that learns from Horn-ICE samples.
    Extending decision-tree learning to handle Horn samples turns out to be non-trivial. When a decision
tree algorithm reaches a node that it decides to make a leaf and label it TRUE, in the ICE-learning setting it
can simply propagate the constraints across the implication constraints. However, it turns out that for Horn
constraints, this is much harder. Assume there is a single invariant we are synthesizing and we have a Horn
sample (s1 ∧ s2 ) ⇒ s′ and we decide to label s′ false when building the decision tree. Then we must later turn
at least one of s1 and s2 to false. This choice makes the algorithms and propagation much more complex,
and ensuring that the decision tree algorithm will always construct a correct decision tree (if one exists)
and work in polynomial time becomes much harder. Furthermore, statistical measures based on entropy for
choosing attributes (to split each node) get more complicated as we have to decide on a more complex logical
space of Horn constraints between samples.
    The contributions of this paper are the following:
 1. A robust decision-tree learning algorithm that learns using Horn implication counterexamples, runs in
    polynomial time (in the number of samples) and has a bias towards learning smaller trees (expressions)
    using statistical measures for choosing attributes. The algorithm also guarantees that a decision-tree
    consistent with all samples is created, provided there exists one.
 2. We show that we can use our learning algorithm to learn over an infinite countable set of predicates P,
    and we can ensure learning is complete (i.e., that will find an invariant if one is expressible using the
    predicates P).
 3. An implementation of our algorithm, extending the classical IC3 decision-tree algorithm, and an auto-
    mated verification tool built with our algorithm for synthesizing invariants. We evaluate our algorithm
    for finding loop invariants and summaries for sequential programs and also Rely-Guarantee contracts in
    concurrent programs.
    The paper is structured as follows. In Section 2 we present an overview of Horn ICE invariant synthesis;
in Section 3, we describe the decision tree based algorithm for learning invariant formulas from Horn ICE
samples; in Section 4, we describe the algorithm that propagates the data point classifications across Horn
constraints; we describe the node/attribute selection strategies used in the decision tree based learning
algorithm in Section 5 and the experimental evaluation in Section 6.

Related Work
Invariant synthesis is the central problem in automated program verification and, over the years, several
techniques have been proposed for synthesizing invariants, including abstract interpretation [9], interpola-
tion [26,23], IC3 and PDR [6,25], predicate abstraction [1], abductive inference [10], as well as synthesis
algorithms that rely on constraint solving [19,20,8]. Subsequent to [18], there has been a lot of work to-
wards Horn-clause solving [5,3], using a combination of these techniques. Complementing these techniques
are data driven invariant synthesis techniques, the first ones to be proposed being Daikon [12] that learns
likely program invariants and Houdini [14] that learns conjunctive inductive invariants. Data-driven invari-
ant synthesis has seen renewed interest, lately [39,37,38,15,16,36,41,33,32,30,17,42,7,13]. When the program
manipulates complex data-structures, arrays, pointers, etc., or when one needs to reason over a complicated
memory model and its semantics, the invariant for the correctness of the program might still be simple. In
such a scenario, a black-box, data-driven guess and check approach, guided by a finite set of program con-
figurations, has been shown to be advantageous. However, implication counter-examples proposed by Garg
et al. [16] are not sufficient for learning invariants in general program verification settings. Grebenshchikov
et al. [18] have shown that most reasoning in program verification is expressed in terms of Horn clauses.
Subsequent to [18], there has been a lot of work towards Horn-clause solving [5,3]. SeaHorn [21] is a veri-
fication framework that translates verification conditions of a program to horn clauses that can be solved
using several backend solvers. In the context of data-driven invariant synthesis, our work generalizes the
ICE learning model [16] to Horn counter-examples, and we build a decision-tree based Horn-ICE learner for
learning invariant annotations in this model.

                                                      3
                                         Boogie                                     Horn Solver

                            Annotated             Counter-            Horn constraints      Sat/Unsat
                        Boogie program            examples           Partial evaluation     Forced points
                                                               Data points
                  Program                                    Horn constraints
                                      Teacher                                         Learner

                                                        Conjectured invariants


                         Fig. 1: Architecture of the Horn-ICE invariant synthesis tool


2    Overview

We give an overview of the Horn-ICE invariant synthesis framework in this section. Fig. 1 shows the main
components of our Horn-ICE invariant synthesis framework. The Teacher is given a program along with
a specification, and based on the style of proof the teacher wants to carry out, she determines the kind
of invariants needed (a name for each invariant, and the set of variables or terms it may mention) and the
corresponding verification conditions they must satisfy. The Learner conjectures a concrete invariant for each
invariant name, and communicates these to the Teacher. The Teacher plugs in these conjectured invariants
in the program and asks a verification engine (in this case Boogie, but we could use any suitable program
verifier) to check if the conjectured invariants suffice to prove the specification. If not, Boogie will return a
counter-example showing why the conjectured invariants do not constitute a valid proof. The Teacher passes
these counter-examples to the Learner. The Learner now learns a new invariants that are consistent with
the set of counter-examples given by the Teacher so far. The Learner frequently invokes the Horn Solver
and Horn propagation engine to guide it in the process of building concrete invariants that are consistent
with the set of counter-examples given by the Teacher. The Teacher and Learner go through a number of
such rounds, until the Teacher finds that the concrete invariants supplied by the Learner constitute a correct
proof.
    We illustrate the working of the tool with an example. Fig. 2a shows a concurrent program adapted from
[27], with two threads T1 and T2 that access two shared variables x and y. The precondition says that initially
x = y = 0. The postcondition asserts that when the two threads terminate, the state satisfies x ≤ y. Let
us say the Teacher is interested in proving this specification using Rely-Guarantee style reasoning [24,40].
In this proof technique we need to come up with invariants associated with the program points P 0–P 4 in
T1 and Q0–Q4 in T2 (as in the Floyd-Hoare style proofs of sequential programs), as well as two “two-state”
invariants G1 and G2, which act as the “guarantee” on the interferences caused by each thread respectively.
Symmetrically, G2 and G1 can be thought of as the conditions that the threads T1 and T2 can “rely” on,
respectively, about the interferences from the other thread. Fig. 2b shows a partial list of the verification
conditions that the named invariants need to satisfy, in order to constitute a valid Rely-Guarantee proof of
the program. The VCs are grouped into four categories: “Adequacy” and “Inductiveness” are similar to the
requirements for sequential programs, while “Guarantee” requires that the atomic statements of each thread
satisfy its promised guarantee, and “Stability” requires that the invariants at each point are stable under
interferences from the other thread. We use the notation “[[x:=x+1]]” to denote the two-state (or “before-
after”) predicate describing the semantics of the statement “x:=x+1”, which in this case is the predicate
x′ = x + 1 ∧ y ′ = y. The guarantee invariants G1 and G2 are similar predicates over the variables x, y, x′ , y ′ ,
describing the possible state changes that an atomic statement in a thread can effect. The invariants P 0–P 4
and Q0–Q4 are predicates over the variables x, y. We use the notation P 0′ to denote the predicate P 0 applied
to the variables x′ , y ′ .
    The Teacher asks the Learner to synthesize the invariants P 0–P 4 and Q0–Q4 over the variables x, y, and
G1 and G2 over the variables x, y, x′ , y ′ . As a first cut the Learner conjectures “true” for all these invariants.
The Teacher encodes the VCs in Fig. 2b as annotated procedures in Boogie’s programming language, plugs in
true for each invariant, and asks Boogie if the annotated program verifies. Boogie comes back saying that the

                                                                 4
              Pre: x = y = 0

         T1        ||               T2                           Adequacy                 Inductiveness
                                                              1. (x = 0 ∧ y = 0) → P 0 1. P 0 → P 1 ∧ P 4
    P0   while (*) {           Q0   while (*) {               2. P 4 ∧ Q4 → (x ≤ y)    2. P 1 ∧ (x < y) → P 2
    P1     if (x < y)          Q1     if (y < 10)                                      3. P 2 ∧ [[x := x + 1]] → P 3′
    P2       x := x + 1;       Q2       y := y + 3                                     4. P 3 → P 0
    P3   }                     Q3   }                                                     ···
    P4                         Q4                                Stability                Guarantee
                                                              1. P 0 ∧ G2 → P 0′       1. P 2 ∧ [[x := x + 1]] → G1
               Post: x <= y                                   2. P 1 ∧ G2 → P 1′       2. Q2 ∧ [[y := y + 3]] → G2
                                                                 ···

                (a) The program                                        (b) The verification conditions

  Fig. 2: A concurrent program and the corresponding verification conditions for a Rely-Guarantee proof


ensures clause corresponding to VC Adequacy-1 may fail, and gives a counter-example say hx 7→ 2, y 7→ 1i
which satisfies P 4 and Q4, but does not satisfy x ≤ y. The Teacher conveys this counter-example as a Horn
sample d1 ∧ d2 → false to the Learner, where d1 is the data point hP 4, 2, 1i and d2 is the data point hQ4, 2, 1i.
We use the convention that the data points are vectors in which the first component is the value of a “location”
variable “l” which takes one of the values “P 0”, “P 1”, etc, while the second and third components are values
of x and y respectively. This Horn constraint is represented graphically in the bottom of Fig. 3a.
     To focus on the technique used by the Learner, which is the heart of this work, let us pan to several
rounds ahead, where the Learner has accumulated a set of counter-examples given by the Teacher, as shown
in Fig. 3a. The Learner’s goal is simply to find a small (small in expression size) invariant ϕ (from a finite
class of formulas comprising Boolean combinations of some base predicates), that is consistent with the given
set of Horn constraints. By “consistent”, we mean that for each Horn constraint of the form d1 ∧ · · · ∧ dk → d,
whenever each of d1 , . . . , dk satisfy ϕ, it is the case that d also satisfies ϕ.
     Our Learner uses a decision tree based learning technique. Here the internal nodes of the decision tree
are labelled by the base predicates (or “attributes”) and leaf-nodes are classified as “True”, “False”, or “?”
(for “Unclassified”). Each leaf node in a decision tree represents a logical formula which is the conjunction of
the node labels along the path from the root to the leaf node, and the whole tree represents the disjunction
of the formulas corresponding to the leaf nodes labelled “True”. The Learner builds a decision tree for a
given set of Horn constraints incrementally, starting from the root node. Each leaf node in the tree has a
corresponding subset of the data-points associated with it, namely the set of points that satisfy the formula
associated with that node. In each step the Learner can choose to mark a node as “True”, or “False”, or to
split a node with a chosen attribute and create two child nodes associated with it.
     Before marking a node as “True” or “False” the Learner would like to make sure that this “preserves”
the consistency of the decision tree with respect to the set of Horn constraints. For this he calls the Horn
Solver/Propagation component, which reports whether the proposed extension of the partial valuation is
indeed consistent with the given set of Horn constraints, and if so which are the data-points which are
“forced” to be true or false. For example, let us say the Learner has constructed the partial decision tree
shown in Fig. 3b, where node n4 has already been set to “True” and nodes n2 and n5 are unclassified. He
now asks the Horn Solver if it is okay for him to turn node n2 “True”, to which the Horn Solver replies “Yes”
since this extended valuation would still be consistent with the set of Horn constraints in Fig. 3a. The Horn
Solver also tells him that the extension would force the data-points d12 , d8 , d7 , d5 , d4 , d3 , d1 to be true, and
the point d2 to false.
     The Learner uses this information to go ahead and set n2 to “True”, and also to make note of the fact
that n5 is now a “mixed” node with some points that are forced to be true (like d1 ) and some false (like
d2 ). Based on this information, the Learner may choose to split node n5 next. After completing the decision
tree, the Learner may send the conjecture in which P 0–P 4, G1 and G2 are set to true, and Q1–Q4 are set
to false. The Teacher sends back another counter-example to this conjecture, and the exchanges continue for
several rounds. Finally, our Learner eventually makes a successful conjecture like: x ≤ y for P 0, P 1, P 3, P 4,
and Q0–Q4; x < y for P 2; y = y ′ ∧ x′ ≤ y ′ for G1; and x = x′ ∧ y ≤ y ′ for G2.

                                                          5
                hP 0, 0, 0i11   hP 1, 0, 0i12

                                         hP 0, −1, 0i9

True     hG2, 0, 0 − 1, 0i10

                                hP 1, −1, 0i8                                            n1   l = P0
                 hP 2, 0, 0i7

                                         hP 2, 1, 1i5

            hG2, 0, 0, 1, 1i6                                    3, 9, 11
                                                                            n2                         n3   l = G2
                 hP 0, 2, 1i3    hP 3, 2, 1i4                               ?


                                 hP 4, 2, 1i1                                    6, 10                                    1, 2, 4, . . .
                                                         False                           n4                          n5

                                 hQ4, 2, 1i2                                             +                           ?

          (a) Horn constraints given by the Teacher                (b) A partial decision tree built by the Learner

            Fig. 3: Intermediate results of our Horn-ICE framework on the introductory example.


    The above example illustrates some of the key differences and challenges from the classical ICE framework
in [16,17]. To begin with, the Learner needs to synthesize multiple invariants (in this case 12 different
invariants) rather than a single invariant; adapting decision-tree learning to learn multiple formulas efficiently
is challenging. Secondly, we note that the Teacher needs to use Horn counter-examples rather than simple
implications, as illustrated by the first counter-example d1 ∧ d2 → false, and subsequently d6 ∧ d7 → d5
and d10 ∧ d11 → d9 . Accordingly, the Learner’s decision tree based algorithm needs to be adapted to work
robustly in the presence of Horn constraints.


3      Decision Tree Learning with Horn Constraints

Valuations and Horn constraints We will consider propositional formulas over a fixed set of propositional
variables X, using the usual Boolean connectives ¬, ∧, ∨, →, etc. The data points we introduce later will also
play the role of propositional variables. A valuation for X is a map v : X → {true, false}. A given formula
over X evaluates, in the standard way, to either true or false under a given valuation. We say a valuation v
satisfies a formula ϕ over X, written v  ϕ, if ϕ evaluates to true under v.
    A partial valuation for X is a partial map u : X ⇀ {true, false}. We denote by dom true (u) the set
{x ∈ X | u(x) = true} and dom false (u) the set {x ∈ X | u(x) = false}. We say a partial valuation u is
consistent with a formula ϕ over X, if there exists a full valuation v for X, which extends u (in that for each
x ∈ X, u(x) = v(x) whenever u is defined on x), and v  ϕ.
    Let ϕ be a formula over X, and u a partial valuation over X which is consistent with ϕ. We say a variable
x ∈ X is forced to be true, with respect to ϕ and u, if for all valuations v which extend u, whenever v  ϕ
we have v(x) = true. Similarly we say x is forced to be false, with respect to ϕ and u, if for all valuations v
which extend u, whenever v  ϕ we have v(x) = false. We denote the set of variables forced true (wrt ϕ and
u) by forced-true(ϕ, u), and those forced false by forced-false(ϕ, u).
    Finally, for a partial valuation u over X, and subsets T and F of X, which are disjoint from each other
and from the domain of u, we denote by uTF the partial valuation which extends u by mapping all variables
in T to true, and all variables in F to false.
    A Horn clause (or a Horn constraint) over X is disjunction of literals over X with at most one positive lit-
eral. Without loss of generality, we will write Horn clauses in one of the three forms: (1) true → x, (2) (x1 ∧· · ·∧xk ) → false,
or (3) (x1 ∧ · · · ∧ xl ) → y, where l ≥ 1 and each of the xi ’s and y belong to X.

                                                          6
Data Points Our decision tree learning algorithm is paired with a teacher that refutes incorrect conjectures
with positive data points, negative data points, and, more generally, with Horn constraints over data points.
Roughly speaking, a data point corresponds to a program configuration and contains the values of each
program variable and potentially values that are derived from the program variables, such as x + y, x2 , or
is_list(z). For the sake of a simpler presentation, however, we assume that a data point is an element d ∈ D
of some (potentially infinite) abstract domain of data points D (we encourage the reader to think of programs
over integers where data points correspond to vectors of integers).


Base Predicates and Decision Trees The aim of our learning algorithm is to construct a decision tree
representing a Boolean combination of some base predicates. We assume a set of base predicates, each of
which evaluates to true or false on a data point d ∈ D. More precisely, a decision tree is a binary tree T whose
nodes either have two children (internal nodes) or no children (leaf nodes), whose internal nodes are labeled
with base predicates, and whose leaf W nodes Vare labeled
                                                         with true or false. The formula ψT corresponding to
a decision tree T is defined to be π∈Πtrue ρ∈π ρ where Πtrue is the set of all paths from the root of T to
a leaf node labeled true, and ρ ∈ π denotes that the base predicate ρ occurs as a label of a node on the path
π. Given a set of data points X ⊆ D, a decision tree T induces a valuation vT for X given by vT (d) = true
iff d  ψT . Finally, given aVset of Horn constraints C over a set of data points X, we say a decision tree T is
consistent with C if vT  C. We will also deal with “partial” decision trees, where some of the leaf nodes
are yet unlabeled, and we define a partial valuation uT corresponding to such a tree T , and the notion of
consistency, in the expected way.


Horn Samples In the traditional setting, the learning algorithm collects the information returned by the
teacher as a set of samples, comprising “positive” and “negative” data points. In our case, the set of samples
will take the form of a set of Horn constraints C over a finite set of data points X. We note that a positive
point d (resp. a negative point e) can be represented as a Horn constraint true → d (resp. e → false). We
call such a pair (X, C) a Horn sample.
    In each iteration of the learning process, we require the learning algorithm to construct a decision tree
T that agrees with the information in the current Horn sample S = (X, C), in that T is consistent with C.
The learning task we address then is “given a Horn sample S, construct a decision tree consistent with S”.


The Learning Algorithm Our learning algorithm, shown in Algo. 1, is an extension of Garg et al.’s [17]
learning algorithm, which in turn is based on the classical decision tree learning algorithm of Quinlan [34].
Given a Horn sample (X, C), the algorithm creates an initial (partial) decision tree T which has a single
unlabelled node, whose associated set of data points is X. As an auxiliary data structure, the learning
algorithm maintains a partial valuation u, which is always an extension of the partial valuation induced by
the decision tree. In each step, the algorithm picks an unlabelled leaf node n, and checks if it is “pure” in
that all points in the node are either positive (i.e. true) or unsigned, or similarly neg/unsigned. If so, it
calls the procedure Label which tries to label it positive if all points are positive or unsigned, or negative
otherwise. To label it positive, the procedure first checks whether extending the current partial valuation u
by making all the unsigned data points in n true results in a valuation that is consistent with the given set
of Horn constraints C. It does this by calling the procedure Horn-Solve (described in the next section),
which not only checks whether the proposed extension is consistent with C, but if so, also returns the set
of points forced to be true and false, respectively. In this case, the node n is labelled true and the partial
valuation u is extended with the forced values. If the attempt to label positive fails, it tries to label the
node negative, in a similar way. If both these fail, it “splits” the node using a suitably chosen base predicate
a. The corresponding method Select-Attribute, which aims to (heuristically) obtain a small tree (i.e., a
concise formula), is described in Sec. 5.
    The crucial property of our learning algorithm is that if the given set of constraints C is satisfiable and
if the data points in X are “separable,” it will always construct a decision tree consistent with C. We say
that the points in X are separable if for every pair of points d1 and d2 in X we have a base predicate ρ

                                                       7
Algorithm 1 Decision Tree Learner for Horn Samples
 1: procedure Decision-Tree-Horn
Input: A Horn sample (X, C)
Output: A decision tree T consistent with C, if one exists.
 2:    Initialize tree T with root node r, with r.dat ← X
 3:    Initialize partial valuation u for X, with u ← ∅
 4:    while (∃ an unlabelled leaf in T ) do
 5:        n ← Select-Node( )
 6:        if (pure(n)) then // n.dat ∩ dom true (u) = ∅ or n.dat ∩ dom false (u) = ∅
 7:            result = Label(n)
 8:        if (¬pure(n) ∨ ¬result) then
 9:            if (n.dat is singleton) then
10:                print “Unable to construct decision tree”; return
11:            result ← Split-Node(n)
12:            if (¬result) then
13:                print “Unable to construct decision tree”; return
14:    return T        // decision tree constructed successfully
 1: procedure Label(node n)                    1: procedure Split-Node(node n)
 2:    Y ← n.dat \ dom(u);                     2:    (res, a) ← Select-Attribute(n)
 3:    if (n.dat ∩ dom true (u) 6= ∅) then     3:    if (res) then
          // n contains only pos/unsigned pts 4:         Create new nodes l and r
 4:        (res, T, F ) ← Horn-Solve(u, Y, ∅) 5:         l.dat ← {d ∈ n.dat | d  a}
 5:        if (res) then                       6:        r.dat ← {d ∈ n.dat | d 6 a}
 6:            n.label ← true                  7:        n.left ← l, n.right ← r.
 7:            u ← uYF ∪T                      8:        return true
 8:            return true                     9:    else
 9:        else return false;                 10:        return false
10:    else . . . // try to label neg



which distinguishes them (i.e., either d1  ρ and d2 6 ρ, or vice-versa). This result, together with its time
complexity, is formalized in Theorem 1.

Theorem 1. Let (X, C) be a Horn sample, n = |X|, and h = |C|. If the input set of points X is separable
and the input Horn constraints C are satisfiable, then Algo. 1 runs in time O(h · n3 ) and returns a decision
tree that is consistent with the Horn sample (X, C).

Proof. At each iteration step, the algorithm maintains the invariant that the partial valuation u is an
extension of the partial valuation uT induced by the current (partial) decision tree T , and is consistent
with C. This is because each labelling step is first checked by a call to the horn-solver, which also correctly
identifies the set of forced values, which are then used to update u. It follows that if the algorithm terminates
successfully in Line 14, then uT is a full valuation which coincides with u, and hence satisfies C. The only
way the algorithm can terminate unsuccessfully is in Line 10 or Line 13. The first case is ruled out since if
n.dat is singleton, and by assumption uT is consistent with C, we must be able to label the single data point
with either true or false in a way that is consistent with C. The second case is ruled out, since under the
assumption of separability the Select-Attribute procedure will always return a non-trivial attribute (see
Sec. 5).
    The learning algorithm (Algorithm 1) runs in cubic time in the size n of the input set X of data points
and linear in the number h of Horn constraints. To see this, observe that in each iteration of the loop the
algorithm produces a tree that is either the same as the previous step (but with a leaf node labelled), or splits
a leaf to extend the previous tree. At each step we maintain an invariant that the collection of data points
in the leaf nodes forms a partition of the input set X. Thus the number of leaf nodes is bounded by n, and
hence each tree has a total of at most 2n nodes. When the algorithm returns (successfully or unsucessfully)

                                                          8
each node in the final tree has been processed at most once by calling the labelling/splitting subroutines on
it. Furthermore, the main work in the subroutines is the call to the horn-solver, which takes O(h · n2 ) time
(see Sec. 4). It follows that Algorithm. 1 runs in O(h · n3 ) time.                                         ⊓
                                                                                                            ⊔

    When the points in X are not separable, as done in [17], we add “iff” constraints between every pair
of inseparable points, and if the resulting Horn constraints are satisfiable, our algorithm is guaranteed to
construct a decision tree consistent with the given Horn constraints.
    Furthermore, we can extend our algorithm to work on an infinite enumerable set of predicates P, and
assure that the algorithm will find an invariant if there is one, as done in [17]. We can take some finite set
X ⊆ P , asking whether there is some invariant over X that satisfies P , and if not grow X by taking finitely
more predicates from P \ X. This is clearly guaranteed to converge on an invariant if one is expressible over
P.


4   Algorithm for solving and propagating Horn constraints

In the decision-tree based learning approach, our aim is to construct a decision-tree representing a Boolean
combination of some base predicates, that is consistent with a given set of Horn constraints. A crucial step
in our decision-tree algorithm is to check whether a proposed extension of the current partial valuation
maintained by the Learner, is indeed consistent with the given Horn constraints, and if so to determine the
set of propositional variables that are “forced” to be true or false. In this section we describe an efficient
algorithm to carry out this step. Our algorithm is an adaptation of the “pebbling” algorithm of [11] for
checking satisfiability of Horn formulas, to additionally find the variables that are forced to be true or false.


Algorithm 2
 1: procedure Horn-Solve
Input: Horn constraints C over X, partial valuation u over X, and T, F ⊆ X.
Output: “Unsat” if uTF is inconsistent with C; “Sat”, forced-true(C, uTF ), forced-false(C, uTF ) otherwise.
 2:    Add two new variables True and False to X. Let X ′ = X ∪ {True, False}.
 3:    C ′ ← C + clauses true → x for each x such that u(x) = true or x ∈ T , and x → false for each x such that
    u(x) = false or x ∈ F .
 4:    Mark variable True with “∗”, and each variable x ∈ X with “∗x”.
 5:    repeat
 6:        For each constraint x1 ∧ · · · ∧ xl → y in C ′ :
 7:        if x1 , . . . , xl are all marked “∗” then mark y with “∗”
 8:        if ∃z ∈ X s.t. x1 , . . . , xl are all marked “∗z” or “∗” then mark y with “∗z”
 9:    until no new marks can be added
10:    P ← {x ∈ X | x is marked “ ∗ ”}, N ← {x ∈ X | False is marked “ ∗x”}
11:    P ′ ← P − (T ∪ dom true (u)), N ′ ← N − (F ∪ dom false (u))
12:    if (False is marked “∗”) then return “Unsat”
13:    else return “Sat”, P ′ , N ′



    Procedure Horn-Solve in Algorithm 2 shows our procedure for checking consistency of a partial valua-
tion with respect to a given set of Horn constraints C, as well as identifying the subset of variables forced to
true or false. Intuitively, the standard linear-time algorithm for Horn satisfiability in fact already identifies
the minimal M set of variables that are forced to be true in any satisfying valuation, and assures us that
the others M can be set to false. However, the other variables are not forced to be false. Our algorithm
essentially runs another set of SAT problems where each of the other variables are set to true (this is modeled
by the variable being marked ∗ in the algorithm); this returns SAT iff the variable is not forced to be false.
The following example illustrates Algorithm 2.

                                                       9
                                    (+)       ∗, ∗y, ∗x                   (-)       ∗b, ∗a
                                          y                                     b
                                                              (+)
                                                               z                             False
                                                          ∗, ∗z, ∗x, ∗y                      ∗a, ∗b
                           True           x                                     a
                             ∗       +        ∗, ∗x                       (-)       ∗a, ∗b


Fig. 4: Example illustrating Algorithm 2. The given set of Horn constraints is C = {x → y, x ∧ y → z, a →
b, b → a, a ∧ b → False}, T = {x}, F = ∅, and the partial valuation is empty. The algorithm outputs “Sat”
together with P = {y, z} and N = {a, b}.


Example 1. Fig. 4 illustrates the working of procedure Horn-Solve on an example set of Horn constraints
C = {x → y, x∧y → z, a → b, b → a, a∧b → False}. The given partial valuation is empty, the set of variables
T initially set to true is {x}, and the set of variables F set to false is ∅. The final marking computed by the
procedure is shown below each variable. Variables set to true in the partial assignment or in the input set
T , are shown with a “+” above them. Variables forced to true (respectively false) are shown with a “(+)”
(respectively “(-)”) above them.

     For the remainer of this section, let us fix X, C, u, T , and F to be the inputs to the procedure, and let
X ′ , C ′ , P , N , P ′ and N ′ be as described in the algorithm. It is clear that there exists an extension of uTF
satisfying C ifand only if C ′ is satisfiable. Furthermore, the set of variables forced true by C with respect to
uTF coincides with those forced true in C ′ , less the variables in dom true (u) ∪ T . A similar claim holds for the
variables forced to false. In total, we obtain the following result.

Theorem 2. Let (X, C) be a Horn sample, n = |X|, and h = |C|. The procedure Horn-Solve runs in time
O(h · n2 ) and outputs

 – “Sat” and the set of variables forced to be true (in P ) and false (in N ), respectively, if the given extended
   valuation uTF is consistent with the Horn constraints C; and
 – “Unsat” otherwise.

    To prove Theorem 2, we first introduce the notion of pebblings (adapted from [11]) and state several
straight-forward propositions. Let x be a variable in X ′ . A C ′ -pebbling of (x, m) from True is a sequence of
markings (x0 , m0 ), . . . , (xk , mk ), such that xk = x and mk = m, and each xi and mi satisfy:

 – xi ∈ X ′ and mi ∈ {∗} ∪ {∗x | x ∈ X}, and
 – one of the following:
    • xi = True and mi = “ ∗ ”, or
    • mi = “ ∗ xi ”, or
    • ∃i1 , . . . , il < i such that each mik = “ ∗ ”, and mi = “ ∗ ”, and xi1 ∧ · · · ∧ xil → xi ∈ C ′ , or
    • ∃z ∈ X and ∃i1 , . . . , il < i such that each mik = “ ∗ ” or “∗z”, and mi = “ ∗z”, and xi1 ∧ · · · ∧ xil →
       xi ∈ C ′ .

A C ′ -pebbling is complete if the sequence cannot be extended to add a new mark.
   It is easy to see that each time the procedure Horn-Solve marks a variable x with a mark m, the
sequence of markings till this point forms a valid C ′ -pebbling of (x, m) from True, and the final sequence of
markings produced does indeed constitute a complete pebbling.

Proposition 1. Consider a C ′ -pebbling of (x, “ ∗”) from True. Let v be a valuation such that v  C ′ . Then
v(x) = true.

Proposition 2. Consider a C ′ -pebbling of (y, “ ∗ x”) from True. Let v be a valuation such that v(x) = true
and v  C ′ . Then v(y) = true.

                                                                   10
Proposition 3. Consider a complete C ′ -pebbling from True, in which False is not marked “∗”. Let v be the
valuation given by                     (
                                         true if x is marked “∗”; and
                              v(x) =
                                         false otherwise.

Then v  C ′ .

Proposition 4. Let y ∈ X. Consider a complete C ′ -pebbling from True, in which False is not marked “∗y”.
Let v be the valuation given by
                                     (
                                       true if x is marked “∗” or “∗y”; and
                              v(x) =
                                       false otherwise.

Then v  C ′ .

    Given Propositions 1 to 4, we can now prove Theorem 2.

Proof (of Theorem 2). We first observe that the procedure Horn-Solve clearly terminates since there is a
finite number of variables in X (say n) and each variable can only be marked n + 1 times. In fact, if h is the
number of clauses in C, the running time of the procedure is bounded by O(h · n2 ).
     We return now to the correctness of the procedure Horn-Solve. Firstly, the procedure outputs “Unsat”
if and only if C ′ is unsatisfiable. Suppose the procedure outputs “Unsat”. Then, False must be marked “∗”
by the algo. But this means we have a C ′ -pebbling of False from True. Now, since we don’t have a clause
True → False in C ′ , we must have a clause c ∈ C ′ of the form x1 ∧ · · · ∧ xl → False and a pebbling (by “∗”)
of each xi from True. Now, suppose to the contrary that there exists a valuation v such that v  C ′ . By
Prop. 1, v must set each xi to true. But this means that v does not satisfy clause c, which contradicts the
assumption that v  C ′ .
     Conversely, suppose the procedure outputs “Sat”. Then, we have have a complete pebbling in which False
is not labelled “∗”. By Prop. 3, we can construct a valuation v which satisfies C ′ , and hence C ′ is satisfiable.
     We further need to argue that in the latter case (when the algorithm outputs “Sat”), the P and N sets
are computed correctly as the set of variables forced to true and false respectively, in C ′ . We begin with the
P set. Recall that P is the set of variables that are marked “∗” at the end of the procedure, and hence in
a complete pebbling. It follows from Prop. 1 that all the variables in P are indeed forced true. Conversely,
suppose there is a variable x that is not marked “∗” by the algorithm. Then, by Prop. 3 there is a valuation
v which satisfies C ′ , in which x is set to false. Hence x is not forced to true by C ′ .
     Regarding the N set, recall that it is the set of variables x such that False is marked “∗x”. Let x ∈ N ,
and let v be a valuation that sets x to true, and satisfies C ′ . Then there must be a clause c of the form
x1 ∧ · · · ∧ xl → false in C ′ , and each xi is marked “∗” or “∗x”. By Props. 1 and 2, v must set each of the
xi ’s to true. But then v does not satisfy clause c, and this contradicts the assumption that v  C ′ . Hence
every variable in N is forced false. Conversely, suppose x 6∈ N . Hence False is not marked “∗x”. Then, by
Prop. 4, there is a valuation v which sets x to true and satisfies C ′ . Hence, x is not forced to false by C ′ .
This completes the proof of the correctness of the procedure.                                                   ⊓
                                                                                                                ⊔


5    Node and Attribute Selection

The decision tree algorithm in Section 3 returns a consistent tree irrespective of the order in which nodes of
the tree are processed or the heuristic used to choose the best attribute to split nodes in the tree. If one is
not careful while selecting the next node to process or one ignores the Horn constraints while choosing the
attribute to split the node, seemingly good splits can turn into bad ones as data points involved in the Horn
constraints get classified during the construction of the tree. We experimented with the following strategies
for node and attribute selection:

                                                        11
Node selection: breadth-first-search; depth-first-search; random selection; selecting nodes with the maxi-
   mum/minimum entropy
Attribute selection: based on a new information gain metric that penalizes node splits that cut Horn
   constraints; based on entropy for Horn samples obtained by assigning probabilistic likelihood values to
   unlabeled datapoints using model counting.

    So as to clutter the paper not too much, we here only describe the best performing combination of
strategies in detail. The experiments reported in Section 6 have been conducted with this combination.


Choosing the next node to expand the decision tree We select nodes in a breadth-first search (BFS)
order for building the decision tree. BFS ordering ensures that while learning multiple invariant annotations,
the subtree for all invariants gets constructed simultaneously. In comparison, in depth-first ordering of the
nodes, subtrees for the multiple invariants are constructed one after the other. In this case, learning a simple
invariant, for e.g. true, for an annotation usually forces the invariant for a different annotation to become
very complex.


Choosing attributes for splitting the given node Similar to [17], we observed that if one chooses
attribute splits based on the entropy of the node that ignores Horn constraints, the invariant learning algo-
rithm tends to produce large trees. In the same spirit as [17], we penalize the information gain for attribute
splits that cut Horn constraints, and choose the attribute with the highest corresponding information gain.
For a sample S = (X, C) that is split with respect to attribute a into subsamples Sa and S¬a , we say that
the corresponding attribute split cuts a Horn constraint ψ ∈ C if and only if

 – x ∈ premise(ψ) and x ∈ Sa and conclusion(ψ) ∈ S¬a ; or
 – x ∈ premise(ψ) and x ∈ S¬a and conclusion(ψ) ∈ Sa .

The penalized information gain is defined as

                       Gainpen (S, Sa , S¬a ) = Gain(S, Sa , S¬a ) − Penalty(S, Sa , S¬a , C),

where the penalty is proportional to the number of Horn constraints cut by the attribute split. However,
we do not penalize a split when it cuts a Horn constraint such that the premise of the constraint is labeled
negative and the conclusion is labeled positive. We incorporate this in the penalty function by formally
defining it as
                                       X                                X                           
        Penalty(S, Sa , S¬a , H) =               1 − f (Sa , S¬a ) +                1 − f (S¬a , Sa ) ,
                                       ψ∈H,x∈Sa                              ψ∈H,x∈S¬a
                                     x∈premise(ψ)                           x∈premise(ψ)
                                   conclusion(ψ)∈S¬a                      conclusion(ψ)∈Sa


where, for subsamples S1 and S2 , f (S1 , S2 ) is the likelihood of S1 being labeled negative and S2 being labeled
positive (i.e., f (S1 , S2 ) = P1N+N
                                   1
                                      . P2 ). Here, Pi and Ni is the number of positive and negative datapoints
                                     1 P2 +N2
respectively in the sample Si .


6   Experimental Evaluation

We have implemented a prototype, named Horn-DT to evaluate the proposed learning framework. The
decision tree learning algorithm and the Horn solver are fresh implementations, consisting of roughly 6000
lines of C++ code. The teacher, on the other hand, is implemented on top of Microsoft’s program verifier
Boogie [2] and reuses much of the code originally developed by Garg et al. [17] for their ICE learning tool.
Via C-to-Boogie conversion tools such as Smack [35], our prototype becomes a fully automatic program
verifier for C programs.

                                                         12
    We have evaluated our prototype on two suits of benchmarks. The first suite consists of 56 sequential pro-
grams of varying complexity, mainly taken the Software Verification Competition (SV-Comp) [4]. The second
benchmark suite consists of 24 concurrent and recursive programs and includes popular concurrent protocols
like Peterson’s algorithm, a producer-consumer problem and complex recursive programs like McCarthy91.
    A natural choice to compare Horn-DT to is Seahorn [21]. Seahorn is a fully automated analysis framework
for LLVM-based languages, which compiles C and C++ code via the LLVM intermediate language into
verification conditions in form of constrained Horn clauses. These Horn clauses can then be solved by any
suitable solver. For our experimental evaluation, we used the PDR engine [22] implemented in Z3 [29], which
is offered as the standard option in Seahorn.
    Unfortunately, Seahorn cannot reason about concurrent programs and, thus, we can only compare to
Seahorn on sequential programs (we are not aware of any other Horn-based invariant synthesis tool to which
we could compare on this benchmark suite). Moreover, it is important to emphasize that our evaluation is
not a like-to-like comparison due to the following two reasons:
 – Boogie and Seahorn produce different verification conditions: as Boogie allows very rich specifications
   (e.g., including quantifiers), the verification conditions produced by it are typically larger and more
   complex compared to those produced by Seahorn.
 – The PDR engine does not require invariant templates while Horn-DT does. More precisely, Horn-DT
   learns invariants that are arbitrary Boolean combinations of Boolean program variables and predicates
   of the form x ± y ≤ c where x, y are numeric program variables and c is a constant determined by the
   decision tree learner. (Note, however, that this particular choice of template is not a general restriction
   of our framework and can easily be changed should the specific domain require it.)
As a consequence of these differences, our general expectation was that Seahorn with PDR to performs
slightly better than Horn-DT on “simple” programs that do not require the overhead introduced by Boogie
and permit simple invariants. Conversely, we expected a superior performance of Horn-DT on complex
programs (e.g., programs working over arrays or performing nonlinear computations) due to its black box
nature and the use of templates.


                                                                                   TO
                                                            Horn-DT (time in s)




           Seahorn
                                                                                   101
          Horn-DT
                                                                                   100
                     0       20       40    56
                         Number of programs                                       10−1

                           Verified
                           Timeout (300 s)                                               10−1   100     101    TO
                           Error / false positive
                                                                                         Seahorn (time in s)

Fig. 5: Experimental comparison of Horn-DT with Seahorn on the the sequential programs benchmark suite.
TO indicates a time out after 300 s or a false positive.


    The remainder of this section presents our empirical evaluation on both benchmark suites in detail. All
experiments were conducted on a Intel Core i3-4005U 4x1.70GHz CPU with 4 GB of RAM running Ubuntu
16.04 LTS 64 bit. The reported results were obtained using the split and node selection strategies described
in Sec. 5.

Sequential Programs The first benchmark suite consists of 56 sequential programs taken SV-Comp as well
as Garg et al.’s ICE tool [17]. These programs vary in complexity and range from simple integer manipulating

                                                     13
Table 1: Results of Horn-DT on concurrent and recursive programs. Columns show the number of invariants
to be synthesized (“Inv”), total number of terms used (“Dim”), number of iterations between teacher and
learner (“Rounds”), number of each kind of counter-examples generated (“Pos”, “Neg”, and “Horn”), and
the time taken (“Time”). Benchmarks with the suffix -RG and -OG indicate Rely-Guarantee-style proofs
and Owicki-Gries-style proofs, respectively.

                     Benchmark                     Inv Dim Rounds Pos Neg Horn Time (s)
                     Ackermann02                 2        5    13   4    1     8    0.89
                     Addition03                  2        5    31   2    5    29    1.00
                     afterrec_2calls             2        4     0   0    0     0    0.04
                     BallRajamani-SPIN2000-Fig1 2         5    32   5    0    30    1.58
                     fib_bench-OG                6       18     7   2    0     5    1.52
                     fibo_2calls_5               4        6   105   1    3   105    3.65
                     Fibo_5                      2        3    71   1    3    67    2.43
                     id2_b3_o2                   4        6    48   1    5    45    1.40
                     id2_i5_o5                   4        6    10   1    1    10    0.72
                     McCarthy91                  1        2    98   5   91     2    2.77
                     peterson-OG                 8       32   370   3   91   277   65.31
                     qw2004-OG                  13       20    24   2    1    23    3.33
                     stateful01-OG               6       12   220   2    0   218    9.56
                     sum_2x3                     2        5    36   1    2    36    0.99
                     sum_non_eq                  2        4     8   3    1     4    0.58
                     sum_non                     2        4     6   4    1     1    0.57
                     18_read_write_lock-OG       8       16    16   2    1    13    2.42
                     Mine_Fig_1-OG [28]            10    20    35   2   0     41    2.00
                     Mine_Fig_1-RG [28]            12    28    43   2   0     48    3.13
                     Mine_Fig_4-OG [28]            13    28    51   3   0     65    6.03
                     Mine_Fig_4-RG [28]            15    44   123   3   0    159   38.59
                     pro_cons_atomic-OG             8    16    32   2   0     30    2.11
                     pro_cons_queue-OG              8    16    31   2   0     29    2.09
                     12_hour_clock_serialization    1     3     6   1   1      4    1.59



programs to programs involving nonlinear computations to programs with complex array manipulations. The
task for each of the benchmark programs is to find a single inductive invariant or adequate contract for a
method call. We refer the reader to SV-Comp [4] as well as Garg et al. [17] for further details.
    Figure 5 summarizes the results of our experimental evaluation on the sequential programs benchmark
suite (see Appendix A for details). As shown on the left, Horn-DT is able to synthesize invariants and verify
all 56 programs in the benchmarks suite. Seahorn, on the other hand, is able to verify 43 programs (77 %)
and times out on 3 further programs (5 %). Surprisingly, Seahorn produced false positives (i.e., it reported
an assertion violation) for 10 programs (18 %)—these programs predominantly involve arrays or nonlinear
computations. After corresponding with the authors of SeaHorn, it turned out that these false positives were
in fact caused by bugs in Seahorn and are now being investigated.
    The right-hand-side of Figure 5 shows a comparison of the runtimes of Horn-DT and Seahorn. As expected,
Seahorn requires slightly less time to verify programs but frequently times out (or fails) when the programs
work over arrays or perform nonlinear computations. Horn-DT, on the other hand, is able to verify the
majority of programs in less than 1 s, which demonstrates the effectiveness of our technique.


Concurrent and Recursive Programs The second benchmark suite consists of 17 concurrent and re-
cursive programs selected from SV-Comp15 pthread, pthread-atomic, pthread-ext, pthread-lit, recursive and
recursive-simple benchmarks, as well as popular concurrent programs from the literature [28].

                                                        14
    For concurrent programs we have used both Rely-Guarantee [40] and Owicki-Gries [31] proof techniques
to verify the assertions. For recursive programs we use a modular verification technique, in the form of
function contracts for each procedure. All these programs were manually converted into Boogie programs.
For concurrent programs, we essentially encode the verification conditions for Rely-Guarantee or Owicki-Gries
proofs in Boogie. Invariants inside a loop with an empty loop-body can be removed by over constraining
invariant at the loop entry. This modification will safely under approximate the search space for invariants.
We have adopted this encoding technique to verify Peterson’s algorithm.
    Table 1 shows the results of running our Horn-DT tool on these programs. We note that each of these
programs produce a large number of Horn counter-examples. The Boogie Teacher first tries to produce
positive or negative counter-examples, and produces Horn counter-examples only if these are not possible.
This indicates that Horn counter-examples are predominantly needed for these kinds of program specifications.
Our tool successfully learns invariants for all these programs in reasonable time, with most finishing within
10 seconds. Only one program took more than 50 s to verify.
    Verification using Owicki-Gries proof rules requires adequate invariants at each program point in each
thread. In comparison, Rely-Guarantee additionally requires two-state invariants for each thread for the
Rely/Guarantee conditions. These additional invariants makes learning for Rely-Guarantee proofs more
difficult for the Learner.


References
 1. Ball, T., Majumdar, R., Millstein, T.D., Rajamani, S.K.: Automatic predicate abstraction of C programs. In:
    PLDI, 2001. pp. 203–213 (2001)
 2. Barnett, M., Chang, B.E., DeLine, R., Jacobs, B., Leino, K.R.M.: Boogie: A modular reusable verifier for object-
    oriented programs. In: FMCO 2005. LNCS, vol. 4111, pp. 364–387. Springer (2005)
 3. Beyene, T.A., Popeea, C., Rybalchenko, A.: Solving existentially quantified horn clauses. In: CAV 2013. pp.
    869–882. LNCS, Springer (2013)
 4. Beyer, D.: Software verification with validation of results - (report on SV-COMP 2017). In: TACAS 2017. LNCS,
    vol. 10206, pp. 331–349 (2017)
 5. Bjørner, N., McMillan, K.L., Rybalchenko, A.: On solving universally quantified horn clauses. In: SAS 2013. pp.
    105–125 (2013)
 6. Bradley, A.R.: Sat-based model checking without unrolling. In: VMCAI 2011. LNCS, vol. 6538, pp. 70–87. Springer
    (2011)
 7. Brockschmidt, M., Chen, Y., Kohli, P., Krishna, S., Tarlow, D.: Learning shape analysis. In: SAS 2017. pp. 66–87
    (2017)
 8. Colón, M., Sankaranarayanan, S., Sipma, H.: Linear invariant generation using non-linear constraint solving. In:
    CAV 2003. LNCS, vol. 2725, pp. 420–432. Springer (2003)
 9. Cousot, P., Cousot, R.: Abstract interpretation: A unified lattice model for static analysis of programs by con-
    struction or approximation of fixpoints. In: POPL 1977. pp. 238–252. ACM Press (1977)
10. Dillig, I., Dillig, T., Li, B., McMillan, K.L.: Inductive invariant generation via abductive inference. In: Object
    Oriented Programming Systems Languages & Applications, OOPSLA 2013. pp. 443–456 (2013)
11. Dowling, W.F., Gallier, J.H.: Linear-time algorithms for testing the satisfiability of propositional horn formulae.
    J. Log. Program. 1(3), 267–284 (1984)
12. Ernst, M.D., Czeisler, A., Griswold, W.G., Notkin, D.: Quickly detecting relevant program invariants. In: ICSE
    2000. pp. 449–458. ACM Press (2000)
13. Fedyukovich, G., J Kaufman, S., Bodik, R.: Sampling invariants from frequency distributions (2017)
14. Flanagan, C., Leino, K.R.M.: Houdini, an annotation assistant for esc/java. In: FME 2001. LNCS, vol. 2021, pp.
    500–517. Springer (2001)
15. Garg, P., Löding, C., Madhusudan, P., Neider, D.: Learning universally quantified invariants of linear data
    structures. In: CAV 2013. LNCS, vol. 8044, pp. 813–829. Springer (2013)
16. Garg, P., Löding, C., Madhusudan, P., Neider, D.: ICE: A robust framework for learning invariants. In: CAV
    2014. LNCS, vol. 8559, pp. 69–87. Springer (2014)
17. Garg, P., Neider, D., Madhusudan, P., Roth, D.: Learning invariants using decision trees and implication coun-
    terexamples. In: POPL 2016. pp. 499–512. ACM (2016)
18. Grebenshchikov, S., Lopes, N.P., Popeea, C., Rybalchenko, A.: Synthesizing software verifiers from proof rules.
    In: PLDI 2012. pp. 405–416. ACM (2012)


                                                         15
19. Gulwani, S., Srivastava, S., Venkatesan, R.: Program analysis as constraint solving. In: PLDI 2008. pp. 281–292.
    ACM (2008)
20. Gupta, A., Rybalchenko, A.: Invgen: An efficient invariant generator. In: CAV 2009. LNCS, vol. 5643, pp. 634–640.
    Springer (2009)
21. Gurfinkel, A., Kahsai, T., Komuravelli, A., Navas, J.A.: The seahorn verification framework. In: CAV 2015. LNCS,
    vol. 9206, pp. 343–361. Springer (2015)
22. Hoder, K., Bjørner, N.: Generalized property directed reachability. In: SAT 2012. LNCS, vol. 7317, pp. 157–171.
    Springer (2012)
23. Jhala, R., McMillan, K.L.: A practical and complete approach to predicate refinement. In: TACAS 2006. LNCS,
    vol. 3920, pp. 459–473. Springer (2006)
24. Jones, C.B.: Tentative steps toward a development method for interfering programs. Transactions on Program-
    ming Languages and System 5(4), 596–619 (1983)
25. Karbyshev, A., Bjørner, N., Itzhaky, S., Rinetzky, N., Shoham, S.: Property-directed inference of universal invari-
    ants or proving their absence. In: CAV 2015. LNCS, vol. 9206, pp. 583–602. Springer (2015)
26. McMillan, K.L.: Interpolation and SAT-Based model checking. In: CAV 2003. LNCS, vol. 2725, pp. 1–13. Springer
    (2003)
27. Miné, A.: Relational thread-modular static value analysis by abstract interpretation. In: VMCAI 2014. LNCS,
    vol. 8318, pp. 39–58. Springer (2014)
28. Miné, A.: Relational thread-modular static value analysis by abstract interpretation. In: International Conference
    on Verification, Model Checking, and Abstract Interpretation. pp. 39–58. Springer (2014)
29. de Moura, L.M., Bjørner, N.: Z3: an efficient SMT solver. In: TACAS 2008. LNCS, vol. 4963, pp. 337–340. Springer
    (2008)
30. Nguyen, T., Kapur, D., Weimer, W., Forrest, S.: Using dynamic analysis to discover polynomial and array
    invariants. In: ICSE 2012. pp. 683–693. IEEE (2012)
31. Owicki, S., Gries, D.: Verifying properties of parallel programs: An axiomatic approach. Communications of the
    ACM 19(5), 279–285 (1976)
32. Padhi, S., Sharma, R., Millstein, T.D.: Data-driven precondition inference with learned features. In: Proceedings
    of the 37th ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI 2016. pp.
    42–56 (2016)
33. Pavlinovic, Z., Lal, A., Sharma, R.: Inferring annotations for device drivers from verification histories. In: Pro-
    ceedings of the 31st IEEE/ACM International Conference on Automated Software Engineering, ASE 2016. pp.
    450–460 (2016)
34. Quinlan, J.R.: Induction of decision trees. Machine Learning 1(1), 81–106 (1986)
35. Rakamaric, Z., Emmi, M.: SMACK: decoupling source language details from verifier implementations. In: CAV
    2014. LNCS, vol. 8559, pp. 106–113. Springer (2014)
36. Sharma, R., Aiken, A.: From invariant checking to invariant inference using randomized search. In: CAV 2014.
    LNCS, vol. 8559, pp. 88–105. Springer (2014)
37. Sharma, R., Gupta, S., Hariharan, B., Aiken, A., Liang, P., Nori, A.V.: A data driven approach for algebraic
    loop invariants. In: ESOP 2013. LNCS, vol. 7792, pp. 574–592. Springer (2013)
38. Sharma, R., Gupta, S., Hariharan, B., Aiken, A., Nori, A.V.: Verification as learning geometric concepts. In: SAS
    2013. LNCS, vol. 7935, pp. 388–411 (2013)
39. Sharma, R., Nori, A.V., Aiken, A.: Interpolants as classifiers. In: CAV 2012. LNCS, vol. 7358, pp. 71–87. Springer
    (2012)
40. Xu, Q., de Roever, W.P., He, J.: The rely-guarantee method for verifying shared variable concurrent programs.
    Formal Asp. Comput. 9(2), 149–174 (1997)
41. Zhu, H., Nori, A.V., Jagannathan, S.: Learning refinement types. In: ICFP 2015. pp. 400–411. ACM (2015)
42. Zhu, H., Petri, G., Jagannathan, S.: Automatically learning shape specifications. In: PLDI (2016). pp. 491–507.
    ACM, New York, NY, USA (2016)




                                                         16
A    Details of Experimental Evaluation
The following table lists the results of our experimental evaluation on the sequential programs benchmark
suite.

Table 2: Experimental results of Horn-DT and Seahorn on the sequential programs benchmark suite.
“Rounds” corresponds to the number of rounds of the learning process. “Pos”, “Neg”, and “Horn” refers
to the number of positive, negative, and Horn examples produced during the learning, respectively. “To”
indicates a timout after 300 s, while“FP” indicates a false positive. All times are given in seconds.

               Benchmark                            Horn-DT                      Seahorn
                                Rounds Pos Neg Horn Learner time Total time         Time
               add.bpl                8    1 6    1            0.03        0.8       4.49
               afnp.bpl              13    1 3    9            0.06       0.81       0.35
               array2.bpl             5    3 2    1            0.05       0.43       0.46
               array.bpl             14    4 4    7            0.06       0.99       0.26
               array_diff.bpl         3    2 2    0            0.01       0.34       0.23
               arrayinv1.bpl        134    4 32 100            7.44      11.57       1.34
               arrayinv2.bpl         45    7 12 27             0.38       2.55       0.22
               bool_dec.bpl           3    2 1    0            0.01       0.31        FP
               bool_inc.bpl           3    1 1    1            0.15       0.45        FP
               cegar1.bpl             5    3 1    1            0.02       0.41       0.28
               cegar2.bpl            24    4 7 14              0.28       1.67       0.30
               cggmp.bpl             67    1 13 53             0.69       2.11       0.31
               countud.bpl           25    3 16   8            0.11       0.57       0.27
               dec.bpl                3    1 2    0            0.01       0.32       0.31
               dillig01.bpl           8    2 6    1            0.03       0.37       0.22
               dillig03.bpl           9    2 4    3            0.04       0.38       0.21
               dillig05.bpl          15    3 10   4            0.11        0.5        TO
               dillig07.bpl          12    3 5    5            0.05        0.4       0.28
               dillig15.bpl          12    2 3    7            0.05       0.41       0.26
               dillig17.bpl          39    5 9 31              0.21        0.8       0.36
               dillig19.bpl          12    2 4    7            0.05       0.43       0.31
               dillig24.bpl          15    0 0 17              0.08       0.53       0.44
               dillig25.bpl          47    1 25 36             0.32        1.1        TO
               dillig28.bpl          25    1 0 34              0.12       0.61        TO
               dtuc.bpl              28    6 15 14             0.14       0.74        FP
               ex14.bpl               2    1 1    0            0.01       0.31       0.24
               ex14c.bpl              2    1 1    0            0.01       0.32       0.22
               ex23.bpl              19    2 7 11               0.1       0.58        FP
               ex7.bpl                3    2 2    0            0.01       0.39        FP
               fig1.bpl               5    2 3    1            0.02       0.34       0.24
               fig3.bpl               3    2 2    0            0.01       0.34        FP
               fig9.bpl               2    1 1    0            0.01       0.32       0.20
               formula22.bpl         56    1 9 46              0.44       1.24       0.39
               formula25.bpl         32    1 28   3            0.16       0.76       0.67
               formula27.bpl        116    1 105 10            0.93       2.62       0.89
               inc2.bpl              10    4 3    3            0.05       0.45       0.26
               inc.bpl              102    1 1 100             1.98       3.14       0.21
               loops.bpl             16    3 0 16              0.08       0.53       0.35



                                                   17
                         Table 2: continued

Benchmark                         Horn-DT                     Seahorn
                Rounds Pos Neg Horn Learner time Total time     Time
matrixl1.bpl         8 6 7         1          0.04     0.51      0.21
matrixl1c.bpl        8 5 11        0          0.04      0.5       FP
matrixl2.bpl        24 14 9        6          0.11     0.87      0.21
matrixl2c.bpl       36 15 18       6           0.2     1.31       FP
nc11.bpl             9 2 4         4          0.04     0.39      0.26
nc11c.bpl            8 3 3         3          0.04     0.39      0.27
sqrt.bpl            95 6 49       42          1.29     3.67       FP
square.bpl          18 1 14        3          0.08     0.79       FP
sum1.bpl            22 5 16        4           0.1     0.63      0.30
sum3.bpl             6 1 4         1          0.03     0.38      0.26
sum4.bpl            41 1 7        33          0.21     0.98      0.28
sum4c.bpl           19 5 11        4          0.09     0.59      0.19
tacas.bpl           32 15 9       11          0.17     0.69      0.30
trex1.bpl            4 2 3         0          0.02     0.36      0.25
trex3.bpl           10 4 7         2          0.04     0.46      0.35
vsend.bpl            2 1 1         0          0.01     0.34      0.20
w1.bpl               4 2 1         1          0.02     0.34      0.29
w2.bpl               4 1 2         1          0.02     0.34      0.27




                                 18
