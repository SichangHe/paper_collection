                                                  Proc. VMCAI 2016, (c) Springer
                                            Program Analysis with Local Policy Iteration⋆

                                               Egor George Karpenkov1, David Monniaux1 , and Philipp Wendler2
                                                    1
                                                        Univ. Grenoble Alpes, VERIMAG, F-38000 Grenoble, France
arXiv:1509.03424v3 [cs.LO] 3 Nov 2015




                                                              CNRS, VERIMAG, F-38000 Grenoble, France
                                                                2
                                                                  University of Passau, Passau, Germany



                                                Abstract. We present local policy iteration (LPI), a new algorithm for
                                                deriving numerical invariants that combines the precision of max-policy
                                                iteration with the flexibility and scalability of conventional Kleene itera-
                                                tions. It is defined in the Configurable Program Analysis (CPA) frame-
                                                work, thus allowing inter-analysis communication.
                                                LPI uses adjustable-block encoding in order to traverse loop-free pro-
                                                gram sections, possibly containing branching, without introducing extra
                                                abstraction. Our technique operates over any template linear constraint
                                                domain, including the interval and octagon domains; templates can also
                                                be derived from the program source.
                                                The implementation is evaluated on a set of benchmarks from the Inter-
                                                national Competition on Software Verification (SV-COMP). It competes
                                                favorably with state-of-the-art analyzers.


                                        1     Introduction
                                        Program analysis by abstract interpretation [1] derives facts about the execution
                                        of programs that are always true regardless of the inputs. These facts are proved
                                        using inductive invariants, which satisfy both the initial condition and the transi-
                                        tion relation, and thus always hold. Such invariants are found within an abstract
                                        domain, which specifies what properties of the program can be tracked. Classic
                                        abstract domains for numeric properties include [products of] intervals and oc-
                                        tagons [2], both of which are instances of template linear constraint domains [3].
                                             Consider classic abstract interpretation with intervals over the program int
                                        i=0; while(i < 1000000) i++; After the first instruction, the analyzer has a
                                        candidate invariant i ∈ [0, 0]. Going through the loop body it gets i ∈ [1, 1],
                                        thus by least upper bound with the previous state [0, 0] the new candidate in-
                                        variant is i ∈ [0, 1]. Subsequent Kleene iterations yield [0, 2], [0, 3] etc. In order
                                        to enforce the convergence within a reasonable time, a widening operator is used,
                                        which extrapolates this sequence to [0, +∞). Then, a narrowing iteration yields
                                        [0, 100000]. In this case, the invariant finally obtained is the best possible, but the
                                        same approach yields the suboptimal invariant [0, +∞) if an unrelated nested
                                        ⋆
                                            The research leading to these results has received funding from the European
                                            Research Council under the European Union’s Seventh Framework Programme
                                            (FP/2007-2013) / ERC Grant Agreement nr. 306595 “STATOR”.
2

loop is added to the program: while(i<100000)while(unknown()) i++;. This
happens because the candidate invariant obtained with widening is its own post-
image under the nested loop, hence narrowing cannot shrink the invariant.
   In general, widenings and narrowings are brittle: a small program change may
result in a different analysis behavior. Their result is non-monotone: a locally
more precise invariant at one point may result in a less precise one elsewhere.
Max-policy iteration In contrast, max-policy iteration [4] is guaranteed to
compute the least inductive invariant in the given abstract domain.3 To compute
the bound h of the invariant i ≤ h for the initial example above, it considers that
h must satisfy h = max i′ s.t. (i′ = 0) ∨ (i′ = i + 1 ∧ i < 10000000 ∧ i ≤ h) and
computes the least inductive solution of this equation by successively considering
separate cases:
   (i) h = (max i′ s.t. i′ = 0) = 0, which is not inductive, since one can iterate
       from i = 0 to i = 1.
  (ii) h = max i′ s.t. i′ = i + 1 ∧ i < 1000000 ∧ i ≤ h, which has two solutions
       over R ∪ {∞, −∞}: h = −∞ (representing unreachable state, discarded)
       and h = 1000000, which is finally inductive.
     Earlier presentations of policy iteration solve a sequence of global convex op-
timization problems whose unknowns are the bounds (here h) at every program
location. Further refinements [5] allowed restricting abstraction to a cut-set [6]
of program locations (a set of program points such that the control-flow graph
contains no cycle once these points are removed), through a combination with
satisfiability modulo theory (SMT) solving. Nevertheless, a global view of the
program was needed, hampering scalability and combinations with other analy-
ses.
Contribution We present the new local-policy-iteration algorithm (LPI) for
computing inductive invariants using policy iteration. Our implementation is
integrated inside the open-source CPAchecker [7] framework for software verifi-
cation and uses the maximization-modulo-theory solver νZ [8]. To the best of
our knowledge, this is the first policy-iteration implementation that is capable of
dealing with C code. We evaluate LPI and show its competitiveness with state-
of-the-art analyzers using benchmarks from the International Competition on
Software Verification (SV-COMP).
    Our solution improves on earlier max-policy approaches:
(i) Scalability LPI constructs optimization queries that are at most of the size
of the largest loop in the program. At every step we only solve the optimization
problem necessary for deriving the local candidate invariant.
(ii) Ability to cooperate with other analyses LPI is defined within the Con-
figurable Program Analysis (CPA) [9] framework, which is designed to allow easy
inter-analysis collaboration. Expressing policy iteration as a fixpoint-propagation
algorithm establishes a common ground with other approaches (lazy abstraction,
bounded model checking) and allows communicating with other analyses.
3
    It does not, however, necessarily output the strongest (potentially non-inductive)
    invariant in an abstract domain, which in general entails solving the halting problem.
                                                                                         3

(iii) Precision LPI uses adjustable-block encoding [10], and thus benefits from
the precision offered by SMT solvers, effectively checking executions of loop-free
program segments without the need for over-approximation. Path focusing [5]
has the same advantage, but at the cost of pre-processing the control-flow graph,
which significantly hinders inter-analysis communication.
Related Work Policy iteration is not as widely used as classic abstract inter-
pretation and (bounded) model checking. Roux and Garoche [11] addressed a
similar problem of embedding the policy-iteration procedure inside an abstract
interpreter, however their work has a different focus (finding quadratic invari-
ants on relatively small programs) and the policy-iteration algorithm remains
fundamentally un-altered. The tool ReaVer [12] also performs policy iteration,
but focuses on efficiently dealing with logico-numerical abstract domains; it only
operates on Lustre programs. The ability to apply policy iteration on strongly
connected components one by one was (briefly) mentioned before [13]. Our pa-
per takes the approach significantly further, as our value-determination problem
is more succinct, we apply the principle of locality to the policy-improvement
phase, and we formulate policy iteration as a classic fixpoint-iteration algorithm,
enabling communication with other analyses. Finally, it is possible to express the
search for an inductive invariant as a nonlinear constraint solving problem [14] or
as a quantifier elimination problem [15], but both these approaches scale poorly.

2      Background
We represent a program P as a control flow automaton (CFA) (nodes, X, edges),
where nodes is a set of control states, and X = {x1 , . . . , xn } are the variables of P .
Each edge e ∈ edges is a tuple (A, τ (X, X ′ ), B), where A and B are nodes, and
τ (X, X ′ ) is a transition relation: a formula defining the semantics of a transition
over the set of input variables X and fresh output variables X ′ . A concrete state
of the program P is a map X → Q from variables to rationals4 . A set C of
concrete states is represented using a first-order formula φ with free variables
from X, such that for all c ∈ C we have c |= φ.
Template Linear Constraint Domains A template linear constraint is a
linear inequality t · X ≤ b where t is a vector of constants (template), and b is an
unknown. A template linear constraint domain [3] (TCD) is an abstract domain
defined by a matrix of coefficients aij , which determines what template linear
constraints are expressible within the domain: each row t of the matrix is a tem-
plate (the word “template” also refers to the symbolic product t · X, e.g. i + 2j).
An abstract
        Vm state in a TCD is defined by a vector (d1 , . . . , dm ) and represents
the set i=1 ti · X ≤ di of concrete states. The di ’s range over extended rationals
(R ∪ {∞, −∞}), where positive infinity represents unbounded templates and neg-
ative infinity represents unreachable abstract states. The domain of products of
intervals is one instance of TCD, where the templates are ±xi ≤ ci for program
variables xi . The domain of octagons [2] is another, with templates ±xi ± xj and
±xi . Any template linear constraint domain is a subset of the domain of convex
polyhedra [16].
 4
     We support integers as well, as explained in Sec. 4.
4

                                                                  I
      i n t i =0;
      i n t j =0;                                                     i′ = 0 ∧ j ′ = 0

      w h i l e ( i <10)                                          A        i < 10 ∧ i′ = i + 1
              i ++;
                                                                      ¬(i < 10)
      w h i l e ( j <10)
              j ++;                             C
                                                      ¬(j < 10)
                                                                  B        j < 10 ∧ j ′ = j + 1



       Fig. 1: Running example – C program and the corresponding CFA

    The strongest abstract postcondition in a TCD is defined by optimization:
maximizing all templates subject to the constraints introduced by the semantics
of the transition and the previous abstract state. For the edge e = (A, τ (X, X ′ ), B),
previous abstract state D = (d1 , . . . , dm ), and a set {t1 , . . . , tm } of templates,
the output abstract state is D′ = (d′1 , . . . , d′m ) with
                                          V
                  d′i = (max ti · X ′ s.t. i ti · X ≤ di ∧ τ (X, X ′ ))
    For example, for the abstract state i ≤ 0 ∧ j ≤ 0 under the transition i′ =
i + 1 ∧ i ≤ 10 the new abstract state is i ≤ di ∧ y ≤ dj , where di = max i′ s.t. i ≤
0 ∧ j ≤ 0 ∧ i′ = i + 1 ∧ i < 10 ∧ j ′ = j and dj is the result of maximizing j ′
subject to the same constraints. This gets simplified to i ≤ 1 ∧ j ≤ 0.
    Kleene iterations in a TCD (known as value iterations) may fail to converge in
finite time, thus the use of widenings, which result in hard-to-control imprecision.
Policy Iteration Policy iteration addresses the convergence problem of value-
iteration algorithms by operating on an equation system that an inductive in-
variant has to satisfy. Consider the running example shown in Fig. 1. Suppose we
analyze this program with the templates {i, j}, and look for the least inductive
invariant D = (diA , djA , diB , djB ) that satisfies the following for all possible execu-
tions of the program (xN denotes the value of the variable x at the node N ):
                      iA ≤ diA ∧ iB ≤ diB ∧ jA ≤ djA ∧ jB ≤ djB
To find it, we solve for the smallest D that satisfies the fixpoint equation [system]
for the running example, stating that the set of abstract states represented by
D is equal to its strongest postcondition within the abstract domain:
             diA = sup i′ s. t. (i′ = 0 ∧ j ′ = 0)
                 ∨(i ≤ diA ∧ j ≤ djA ∧ i < 10 ∧ i′ = i + 1 ∧ j ′ = j) ∨ ⊥
             djA = sup j ′ s. t. (i′ = 0 ∧ j ′ = 0)
                 ∨(i ≤ diA ∧ j ≤ djA ∧ i < 10 ∧ i′ = i + 1 ∧ j ′ = j) ∨ ⊥
             diB = sup i′ s. t. (¬(i < 10) ∧ i ≤ diA ∧ j ′ ≤ djA ∧ i′ = i)
                 ∨(i ≤ diB ∧ j ≤ djB ∧ j < 10 ∧ j ′ = j + 1 ∧ i′ = i) ∨ ⊥
             djB = sup j ′ s. t. (¬(i < 10) ∧ i ≤ diA ∧ j ′ ≤ djA ∧ i′ = i)
                 ∨(i ≤ diB ∧ j ≤ djB ∧ j < 10 ∧ j ′ = j + 1 ∧ i′ = i) ∨ ⊥
Note the equation structure: (i) Disjunctions represent non-deterministic choice
for a new value. (ii) The argument ⊥ is added to all disjunctions, representing
                                                                                       5

infeasible choice, corresponding to the bound value −∞. (iii) Supremum is taken
because the bound must be higher than all the possible options, and it has to
be −∞ if no choice is feasible.
    A simplified equation system with each disjunction replaced by one of its
arguments is called a policy. The least solution of the whole equation system
is the least solution of at least one policy (obtained by taking the solution,
and picking one argument for each disjunction, such that the solution remains
unchanged). Policy iteration finds the least tuple of unknowns (d’s) satisfying
the fixpoint equation by iterating over possible policies, and finding a solution
for each one.
    For program semantics consisting of linear assignments and possibly non-
deterministic guards it is possible to find a fixpoint of each policy using one
linear programming step. This is based on the result that for a monotone and
concave function5 f and x0 such that f (x0 ) > x0 , the least fixpoint of f greater
than x0 can be computed in a single step6 .
    It is possible to solve the global equation system by solving all (exponen-
tially many) policies one by one. Instead, policy iteration [4] computes solutions
for a sequence of policies; each solution is guaranteed to be less than the least
solution of the original equation system, and the solutions form an ascending
sequence. The iteration starts with the policy having least possible value (⊥ for
each disjunction, the solution is −∞ assignment to all unknowns), and eventually
terminates when a solution of the original equation system (an inductive invari-
ant) is found. The termination is guaranteed as there is only a finite number of
solutions.
    For each policy the algorithm finds a global value: the least fixpoint in the
template constraints domain of the reduced equation system. For instance, in
the running example, for the policy diA = sup i′ s. t. i′ = 0 ∧ j ′ = 0 (only one
unknown is shown for brevity) the global value is diA = 0. This step is called value
determination. After the global value is computed the algorithm checks whether
the policy can be improved : that is, whether we can find another policy that
will yield a larger value than the previously obtained global value. In the running
example we want to test the following policy for the possibility of improvement:
          diA = sup i′ s. t. (i ≤ diA ∧ j ≤ diA ∧ i < 10 ∧ i′ = i + 1 ∧ j ′ = j)
We do so by computing the local value: substituting the unknown (diA ) on the
right hand side with the value from the previously obtained global value, and
checking whether the result is greater than the previously obtained bound. In
our example we get the local value diA = 1, which is indeed an improvement
over diA = 0 (policy-improvement step). After the policy is selected, we go back
to the value-determination step, obtaining diA = 10, and we repeat the process
until convergence (reaching a step where no policy can be further improved).
    Under the assumption that the operations on the edges can be expressed
as conjunctions of linear (in)equalities, it can be shown [4] that: (i) The value-
determination step can be performed with linear programming. (ii) The resulting
5
    Order-concave in the presence of multiple templates, see [4] for detailed discussion
6
    Over rationals, we discuss the applicability to integers in Sec. 4
6

value is an under-approximation of the least inductive invariant. (iii) Each pol-
icy is selected at most once and the final fixed point yields the least inductive
invariant in the domain.

Example 1 (Policy-Iteration Trace on the Running Example). We solve for the
unknowns (diA , djA , diB , djB ), defining a (global) abstract value v.
    In our example, disjunctions arise from multiple incoming edges to a single
node, hence a policy is defined by a choice of an incoming edge per node per
template, or ⊥ if no such choice is feasible. We represent a policy symbolically as
a 4-tuple of predecessor nodes (or ⊥), as there are two nodes, with two policies
to be chosen per node. The order corresponds to the order of the tuple of the
unknowns. The initial policy s is (⊥, ⊥, ⊥, ⊥). The trace on the example is:
 1. Policy improvement: s = (I, I, ⊥, ⊥), obtained with a local value (0, 0, −∞, −∞).
 2. Value determination: corresponds to the initial condition v = (0, 0, −∞, −∞).
 3. Policy improvement: s = (A, I, ⊥, ⊥), selecting the looping edge, local value
    is (1, 0, −∞, −∞).
 4. Value determination: accelerates the loop convergence to v = (10, 0, −∞, −∞).
 5. Policy improvement: s = (A, I, A, A), with a local value (10, 0, 10, 0) finally
    there is a feasible policy for the templates associated with the node B.
 6. Value determination: does not affect the result v = (10, 0, 10, 0).
 7. Policy improvement: select the second looping edge: s = (A, I, A, B) obtain-
    ing a local value (10, 0, 10, 1).
 8. Value determination: accelerate the second loop to v = (10, 0, 10, 10).
 9. Finally, the policy cannot be improved any further and we terminate.
    On this example we could have obtained the same result by Kleene iteration,
but in general the latter might fail to converge within finite time. The usual
workaround is to use heuristic widening, with possible and hard-to-control im-
precision. Our value-determination step can be seen as a widening that provides
an under-approximation to the least fixed point.
    Each policy improvement requires at least four (small) linear programming
(LP) queries, and each value determination requires one (rather large) LP query.


Path Focusing and Large-Block Encoding In traditional abstract inter-
pretation and policy iteration, the obtained invariant is expressed as an abstract
state at each CFA node. This can lead to a significant loss in precision: for
instance, since most abstract domains only express convex properties, it is im-
possible to express |x| ≥ 1, which is necessary to prove this assertion: if (abs(x)
>= 1) assert(x != 0);
     This loss can be recovered by reducing the number of “intermediate” abstract
states by allowing more expressive formulas associated with edges. Formally,
two consecutive edges (A, τ1 (X, X ′ ), B) and (B, τ2 (X, X ′ ), C), with no other
edges incoming or outgoing to B can be merged into one edge (A, τ1 (X, X̂) ∧
τ2 (X̂, X ′ ), C). Similarly, two parallel edges (A, τ1 (X, X ′ ), B) and (A, τ2 (X, X ′ ), B),
with no other edges incoming to B can be replaced by a new edge (A, τ1 (X, X ′ )∨
τ2 (X, X ′ ), B). For a well-structured CFA, repeating this transformation in a fix-
                                                                                  7

point manner (until no more edges can be merged) will lead to a new CFA where
the only remaining nodes are loop heads.
    Such a transformation was shown to increase both precision and performance
for model checking [17]. Adjustable block encoding [10] gets the same advan-
tages without the need for CFA pre-processing. Independently, the approach
was applied with the same result to Kleene iterations [18] and to max-policy
iterations [5]. In fact, the CFA in Fig. 1 was already reduced in this manner for
the ease of demonstration.
    On the reduced CFA the number of possible policies associated with a single
edge becomes exponential, and explicitly iterating over them is no longer feasible.
Instead, the path focusing approach uses a satisfiability modulo theory (SMT)
solver to select an improved policy.
Configurable Program Analysis CPA [9] is a framework for expressing
algorithms performing program analysis. It uses a generic fixpoint-computation
algorithm, which is configured by a given analysis. We formulate LPI as a CPA.
    The CPA framework makes no assumptions on the performed analysis, thus
many analyses were successfully expressed and implemented within it, such as
bounded model checking, abstract interpretation and k-induction (note that an
analysis defined within the framework is also referred to as a CPA).
    Each CPA configures the fixpoint algorithm by providing an initial abstract
state, a transfer relation (specifying how to produce successors), a merge opera-
tor (specifying whether and how to merge abstract states), and a stop operator
(specifying whether a newly produced abstract state is covered). The algorithm
keeps a set of reached abstract states and a list of “frontier” abstract states, and
at each step produces successor states from the frontier states using the transfer
relation, and then tries to merge the new states with existing states using the
merge operator. If a new state is covered by the set of reached states according
to the stop operator, it is discarded, otherwise it is added to the set of reached
states and the list of frontier states. We show the CPA algorithm as Alg. 1.

3    Local Policy Iteration (LPI)
The running example presented in the background (Ex. 1) has four value-determination
steps and five policy-improvement steps. Each policy-improvement step corre-
sponds to at most #policies × #templates × #nodes LP queries, and each
value-determination step requires solving an LP problem with at least #policies
× #templates × #nodes variables. Most of these queries are redundant, as the
updates propagate only locally through the CFA: there is no need to re-compute
the policy if no new information is available.
    We develop a new policy-iteration-based algorithm, based on the principle of
locality, which aims to address the scalability issues and the problem of commu-
nicating invariants with other analyses. We call it local policy iteration or LPI.
To make it scalable, we consider the structure of a CFA being analyzed, and we
aim to exploit its sparsity.
    A large majority of (non-recursive) programs are well-structured: they con-
sist of statements and possibly nested loops. Consider checking a program P
8

Algorithm 1 CPA Algorithm (taken from [9])
 1: Input: a CPA (D, transfer-relation, merge, stop), an initial abstract state e0 ∈ E
    (let E denote the set of elements of the semi-lattice of D)
 2: Output: a set of reachable abstract states
 3: Variables: a set reached of elements of E, a set waitlist of elements of E
 4: waitlist ← {e0 }
 5: reached ← {e0 }
 6: while waitlist 6= ∅ do
 7:     Pop e from waitlist
 8:     for all e′ ∈ transfer-relation(e) do
 9:         for all e′′ ∈ reached do
10:           ⊲ Combine with existing abstract state
11:           enew ← merge(e′ , e′′ )
12:           if enew 6= e′′ then
13:               waitlist ← (waitlist ∪ {enew }) \ {e′′ }
14:               reached ← (reached ∪ {enew }) \ {e′′ }
15:       ⊲ Whether e′ is already covered by existing states
16:       if ¬stop(e′ , reached) then
17:           waitlist ← waitlist ∪ {e′ }
18:           reached ← reached ∪ {e′ }
19: return reached

against an error property E. If P has no loops, it can be converted into a sin-
gle formula Ψ (X ′ ), and an SMT solver can be queried for the satisfiability of
Ψ (X ′ ) ∧ E(X ′ ), obtaining either a counter-example or a proof of unreachability
of E. However, in the presence of loops, representing all concrete states reach-
able by a program as a formula over concrete states in a decidable first-order
logic is impossible, and abstraction is required. For example, bounded model
checkers unroll the loop, lazy-abstraction-based approaches partially unroll the
loop and use the predicates from Craig interpolants to “cover” future unrollings,
and abstract interpretation relies on abstraction within an abstract domain.
    In LPI, we use the value-determination step to “close” the loop and compute
the fixpoint value for the given policy. Multiple iterations through the loop might
be necessary to find the optimal policy and reach the global fixpoint. In the
presence of nested loops, the process is repeated in a fixpoint manner: we “close”
the inner loop, “close” the outer loop with the new information from the inner
loop available, and repeat the process until convergence. Each iteration selects
a new policy, thus the number of possible iterations is bounded.
    Formally, we state LPI as a Configurable Program Analysis (CPA), which
requires defining the lattice of abstract states, the transfer relation, the merge
operator, and the stop operator. The CPA for LPI is intended to be used in
combination with other CPAs such as a CPA for tracking location information
(the program counter), and thus does not need to keep track of this information
itself. To avoid losing precision, we do not express the invariant as an abstract
state at every node: instead the transfer relation operates on formulas and we
only perform over-approximation at certain abstraction points (which correspond
                                                                                   9

to loop heads in a well-structured CFA). This approach is inspired by adjustable-
block encoding [10], which performs the same operation for predicate abstraction.
One difference to path focusing [18] is that we still traverse intermediate nodes,
which facilitates inter-analysis communication.
    We introduce two lattices: abstracted states (not to be confused with abstract
states in general: both intermediate and abstracted states are abstract ) for states
associated with abstraction points (which can only express abstract states in the
template constraints domain) and intermediate states for all others (which can
express arbitrary concrete state spaces using decidable SMT formulas).
    An abstracted state is an element of a template constraints domain with
meta-information added to record the policy being used.

Definition 1 (Abstracted State). An abstracted state is a mapping from the
externally given set T of templates to tuples (d, policy, backpointer), where d ∈ R
is a bound for the associated template t (the represented property is t · X ≤ d),
policy is a formula representing the policy that was used for deriving d (policy
has to be monotone and concave, and in particular contain no disjunctions), and
backpointer is an abstracted state that is a starting point for the policy (base
case is an empty mapping).

    The preorder on abstracted states is defined by component-wise comparison
of bounds associated with respective templates (lack of a bound corresponds to
an unbounded template). The concretization is given by the conjunction of rep-
resented template linear constraints, disregarding policy and backpointer meta-
information. For example, an abstracted state {x : (10, , )} (underscores repre-
sent meta-information irrelevant to the example) concretizes to {c | c[x] ≤ 10},
and the initial abstracted state {} concretizes to all concrete states.
    Intermediate states represent reachable state-spaces using formulas directly,
again with meta-information added to record the “used” policy.

Definition 2 (Intermediate State). An intermediate state is a tuple (a0 , φ),
where a0 is a starting abstracted state, and φ(X, X ′ ) is a formula over a set of
input variables X and output variables X ′ .

    The preorder on intermediate states is defined by syntactic comparison only:
states with identical starting states and identical formulas are deemed equal, and
incomparable otherwise. The concretization is given by satisfiable assignments
to X ′ subject to φ(X, X ′ ) and the constraints derived from a0 applied to in-
put variables X. For example, an intermediate state ({x : (10, , )}, x′ = x + 1)
concretizes to the set {c | c[x] ≤ 11} of concrete states.
    Abstraction (Alg. 2) is the conversion of an intermediate state (a0 , φ) to an
abstracted state, by maximizing all templates t ∈ T subject to constraints intro-
duced by a0 and φ, and obtaining a backpointer and a policy from the produced
model M. This amounts to selecting the appropriate disjuncts in each disjunc-
tion of φ. To do so, we annotate φ with marking variables: each disjunction τ1 ∨τ2
in φ is replaced by (m ∧ τ1 ) ∨ (¬m ∧ τ2 ) where m is a fresh propositional variable.
A policy associated to a bound is then identified by the values of the marking
10

Algorithm 2 LPI Abstraction
 1: Input: intermediate state (a0 , φ), set T of templates
 2: Output: generated abstracted state new
 3: new ← empty abstracted state
 4: for all template t ∈ T do
 5:    φ̂ ← φ with disjunctions annotated using a set of marking variables M
 6:      ⊲ Maximize subject to the constraints introduced by the formula
 7:      ⊲ and the starting abstracted state.
 8:      d ← max t · X ′ subject to φ̂(X, X ′ ) ∧ a0
 9:      M ← model at the optimal
10:    ⊲ Replace marking variables M in φ̂ with their value from the model M,
11:    ⊲ generating a concave formula that represents the policy.
12:    Policy ψ ← φ̂[M/M]
13:    new [t] ← (d, ψ, a0 )
14: return new

variables at the optimum (subject to the constraints introduced by φ and a0 ),
and is obtained by replacing the marking variables in φ with their values from M.
Thus the abstraction operation effectively performs the policy-improvement op-
eration for the given node, as only the policies which are feasible with respect to
the current candidate invariant (given by previous abstracted state) are selected.

Example 2 (LPI Propagation and Abstraction). Let us start with an abstracted
state a = {x : (100, , )} (which concretizes to {c | c[x] ≤ 100}, underscores
stand for some policy and some starting abstracted state) and a set {x} of
templates.
    After traversing a section of code if(x <= 10)x += 1; else x = 0; we get
an intermediate state (a, φ) with φ = (x ≤ 10 ∧ x′ = x + 1 ∨ x > 10 ∧ x′ = 0)
and a backpointer to the starting abstracted state a. Suppose in our example the
given C code fragment ends with a loop head. Then we use abstraction (Alg. 2)
to convert the intermediate state (a, φ) into a new abstracted state.
    Firstly, we annotate φ with marking variables, which are used to identify the
selected policy, obtaining x ≤ 10 ∧ x′ = x + 1 ∧ m1 ∨ x > 10 ∧ x′ = 0 ∧ ¬m1 .
Afterwards, we optimize the obtained formula (together with the constraints
from the starting abstracted state a) for the highest values of templates. This
amounts to a single OPT-SMT query:
      sup x′ s.t. x ≤ 100 ∧ (x ≤ 10 ∧ x′ = x + 1 ∧ m1 ∨ x > 10 ∧ x′ = 0 ∧ ¬m1 )
    The query is satisfiable with a maximum of 11, and an SMT model M :
{x′ : 11, m1 : true, x : 10}. Replacing the marking variable m1 in φ with its value
in M gives us a disjunction-free formula x ≤ 10 ∧ x′ = x + 1, which we store as a
policy. Finally, the newly created abstracted state is {x : (11, x ≤ 10 ∧ x′ = x + 1, a)}.

   The local value-determination step (Alg. 3) computes the least fixpoint for
the chosen policy across the entire strongly connected component where the cur-
rent node n lies. The algorithm starts with a map influencing from nodes to
                                                                                      11

abstracted states, which is generated by transitively following policy backpoint-
ers, and converting the resulting set of abstracted states to a map7 . From this
map, we generate a global optimization problem, where the set of fresh variables
dtni represents the maximal value a template t can obtain at the node ni using
the policies selected. Variable dtni is made equal to the namespaced8 output value
of the policy ψ(X, X ′ ) chosen for t at ni (line 13). For each policy ψ and the
associated backpointer a0 , we constrain the input variables of ψ using a set of
variables dtn00 representing bounds at the node n0 associated with a0 (line 16).
This set of “input constraints” for value determination results in a quadratic
number of constraints in terms of the number of selected policies. Finally, for
each template t we maximize for dtn (line 20), which is the maximum possible
value for t at node n under the current policy, and we record the bound in the
generated abstracted state (line 21), keeping the old policy and backpointer.
    The local-value-determination algorithm is almost identical to max-strategy
evaluation [5], except for two changes: we only add potentially relevant con-
straints from the “closed” loop (found by traversing backpointers associated
with policies), and we maximize objectives one by one, not for their sum (which
avoids special casing infinities, and enables optimizations outlined in Sec. 4). Un-
like classic policy iteration, we only run local value determination after merges
on loop heads, because in other cases the value obtained by abstraction is the
same as the value which could be obtained by value determination.
Formulation as a CPA The initial state is the abstracted state {} (empty
map), representing ⊤ of the template constraints domain. The stop operator
checks whether a newly created abstracted state is covered by one of the exist-
ing abstracted states using the preorder described above. The transfer relation
finds the successor state for a given CFA edge. It operates only on intermedi-
ate states – an abstracted state a0 is firstly converted to the intermediate state
(a0 , true). Then, the transfer-relation operator runs symbolic execution: the suc-
cessor of an intermediate state (a, φ(X, X ′ )) under the edge (A, τ (X, X ′ ), B) is
the intermediate state (a, φ′ (X, X ′ )) with φ′ (X, X ′ ) ≡ ∃X̂.φ(X, X̂) ∧ τ (X̂, X ′ ).
If the successor node is a loop head, then abstraction (Alg. 2) is performed on
the resulting state.
     The merge operator has two operation modes, depending on whether we are
dealing with abstracted states or with intermediate states.
     For two abstracted states, we perform the join: for each template, we pick
the largest bound out of the two possible, and we keep the corresponding policy
and the backpointer. If the merge “closes” the loop (that is, we merge at the
loop head, and one of the updated policies has a backpointer to a state inside the
loop), we find the map influencing by recursively following the backpointers of
the joined state, and run local value determination (Alg. 3). For two intermediate
states (a1 , φ1 ) and (a2 , φ2 ) with a1 identical to a2 the merge operator returns
the disjunction (a1 , φ1 ∨ φ2 ). Otherwise, we keep the states separate.
 7
     The are no collisions as abstracted states are joined at nodes.
 8
     Namespacing means creating fresh copies by attaching a certain prefix to variable
     names.
12

Algorithm 3 Local Value Determination
 1: Input: node n, map influencing from nodes to abstracted states, set T of templates
 2: Output: generated abstracted state new
 3: constraints ← ∅
 4: for all node ni ∈ influencing do
 5:    state s ← influencing[ni ]
 6:    for all template t ∈ s do
 7:        (bound d, policy ψ, backpointer a0 ) ← s[t]
 8:        Generate a unique string namespace
 9:        ⊲ Prefix all variables in ψ.
               ′
10:        ⊲ Xnamespace  , Xnamespace is a set of namespaced output/input variables for
      ψ.                               
11:        constraints ← constraints ∪ ψ[X/Xnamespace ][X ′ /Xnamespace
                                                                ′
                                                                        ]
            t
12:        dni ← fresh variable (upper bound on t at n)
13:        constraints ← constraints ∪ dtni = t · Xnamespace
                                                   ′

14:        n0 ← location associated with a0
15:        for all t0 ∈ a0 do
              constraints ← constraints ∪ t0 · Xnamespace ≤ dtn00
                                          
16:
17: new ← empty abstracted state
18: for all templates t ∈ T do
19:    (d0 , ψ, a0 ) ← influencing[n]
20:    d ← max dtn subject to constraints
21:    new [t] ← (d, ψ, a0 )
22: return new


    The local-value-determination problem only contains the constraints result-
ing from policies of the abstracted states associated with nodes in the current
loop. This optimization does not affect the invariant as only the nodes dominat-
ing the loop head can change it. Of those, only the invariants of the nodes reach-
able from the loop head can be affected by the computation: i.e., the strongly
connected component of n.
Properties of LPI
Soundness LPI, like any configurable program analysis, terminates when no
more updates can be performed, and newly produced abstract states are sub-
sumed (in the preorder defined by the lattice) by the already discovered ones.
Thus, it is an inductive invariant: the produced abstract states satisfy the initial
condition and all successor states are subsumed by the existing invariant. Hence
the obtained invariant is sound.
Termination An infinite sequence of produced abstract states must contain in-
finitely many abstracted states, as they are associated with loop heads. However,
each subsequent abstraction on the same node must choose a different policy
to obtain a successively higher value, but the number of policies is finite. An
infinite sequence is thus impossible, hence termination.
Optimality In the absence of integers, LPI terminates with the same invariant
as classical policy iteration with SMT [5]. The outline of the proof is that LPI
can be seen as an efficient oracle for selecting the next policy to update (note
                                                                                       13

that policies selected by LPI are always feasible with respect to the current in-
variant candidate). Skipping value-determination steps when they have no effect,
and attempting to include only relevant constraints in the value-determination
problem do not alter the values of obtained fixed points.

Example 3 (LPI Trace on the Running Example). We revisit the running exam-
ple (Fig. 1) with LPI:
 1. We start with the empty abstracted state a0 ≡ {}.
 2. Transfer relation under the edge (I, φ1 , A) produces the new intermediate
    state (a0 , i′ = 0 ∧ j ′ = 0) associated with A. As A is a loop head, we perform
    an abstraction to obtain the abstracted state a1 ≡ {i : (0, , a0 ) , j : (0, , a0 )}
    (corresponding to i ≤ 0 ∧ j ≤ 0) [2 linear programming problems].
 3. Transfer relation explores the edge (A, φ2 , A) and produces the intermediate
    state (a1 , i ≤ 0 ∧ j ′ ≤ 0 ∧ i′ = i + 1). Again we perform an abstraction, ob-
    taining the abstracted state a2 ≡ {i : (1, , a1 ) , j : (0, , a1 )} [2 LP problems].
 4. The merge operator on node A merges the new state a2 with the previous
    state a1 , yielding the abstracted state a3 ≡ {i : (1, , a1 ) , j : (0, , a0 )}. Value
    determination “closes” the loop, producing a4 ≡ {i : (10, , a1 ) , j : (0, , a0 )}.
    [1 LP problem].
 5. Transfer relation explores the edge (A, φ3 , B) and produces the intermediate
    state (a3 , i′ ≤ 10 ∧ (¬i′ < 10) ∧ j ′ ≤ 0), which is abstracted to
    a5 ≡ {i : (10, , a4 ) , j : (0, , a4 )} [2 LP problems].
 6. The edge (B, φ4 , B) is explored, resulting in the intermediate state
    (a4 , i′ ≤ 10 ∧ j ≤ 0 ∧ j ′ = j + 1), which is abstracted into
    a6 ≡ {i : (10, , a5 ) , j : (1, , a5 )} [2 LP problems].
 7. Value determination produces the state a7 ≡ {i : (10, , a4 ) , j : (10, , a5 )},
    and the exploration concludes. [1 LP problem].
    Compared to the original algorithm there are two value-determination prob-
lems instead of four, both on considerably smaller scale. There are also only
ten LP problems, compared to more than twenty in the original version. The
improvement in performance is more than a fixed constant: if the number of
independent loops in the running example was to increase from 2 to N , the in-
crease in the analysis time of classic policy iteration would be quadratic, while
LPI would scale linearly.

4    Extensions and Implementation Aspects
Template Synthesis The template constraints domain requires templates de-
fined for the given program. In LPI, we can simulate the interval and octagon
domains by synthesizing templates of the form ±x, ±x ± y for every numeric
variable x, y in the program alive at the given program node. Moreover, the
templates can be synthesized from error properties: e.g. for assert(x >= 2 *
y) we could generate the templates ±(x − 2y).
    We show the analysis time of LPI (excluding startup and parsing) in the
interval-domain-mode vs. octagon-domain-mode in Fig. 2 (each data point cor-
responds to an analyzed program). The number of octagon templates is quadratic
14




                        Analysis Time with Octagon Domain (s)
                                                                                Timing data
                                                                                  0.94t1.24

                                                                 100




                                                                10−1




                                                                       10−2               10−1              100
                                                                              Analysis Time with Interval Domain (s)

Fig. 2: Octagon vs. Interval LPI Analysis Time (Dataset and Setup as in Sec. 5)

in terms of the number of interval templates, thus we expect a quadratic rise in
analysis time, however in practice we observe a sub-quadratic increase.
    This has motivated us to experiment with simulating a more expressive do-
main. We generate templates ±2x ± y, ±x ± y ± z, and even ±2x ± y ± z, for
every possible combination of live variables x, y, z at the given program location.
Using this new “rich” template generation strategy we achieve a significant pre-
cision improvement as shown by the number of verified programs in the legend
of Fig. 3a.
Dealing With Integers Original publications on max-policy iteration in tem-
plate constraints domain deal exclusively with reals, whereas C programs operate
primarily on integers9 . Excessively naive handling of integers leads to poor re-
sults: with an initial condition x = 0, x ∈ [0, 4] is inductive for the transition
system x′ = x + 1 ∧ x 6= 4 in integers, but not in rationals, due to the possibility
of the transition x = 3.5 to x = 4.5. An obvious workaround is to rewrite each
strict inequality a < b into a ≤ b − 1: on this example, the transition becomes
x = x + 1 ∧ (x ≤ 3 ∨ x ≥ 5) and x ∈ [0, 4] becomes inductive on rationals. How-
ever, to make use of data produced by an additional congruence analysis, we use
optimization modulo theory with integer and real variables for abstraction, and
mixed integer linear programming for value determination.
    Unfortunately, linear relations over the integers are not concave, which is a
requirement for the least fixpoint property of policy iteration. Thus the encoding
described above may still result in an over-approximation. Consider the following
program:
x =0; x new=unknown ( ) ;
w h i l e ( 2 ∗ x new == x+2) {
        x = x new ; x new = unknown ( ) ;
}

LPI terminates with a fixpoint x ≤ 2, yet the least fixpoint is x ≤ 1.
9
     Previous work [19] deals with finding the exact interval invariants for programs
     involving integers, but only for a very restricted program semantics.
                                                                                      15

Congruence A congruence analysis which tracks whether a variable is even
or odd can be run in parallel with LPI (a more general congruence analysis may
be used, but we did not find the need for it on our examples). During the LPI
abstraction step, the congruence information is conjoined to the formula being
maximized, and the bounds from LPI are used for the congruence analysis.
    This combination enhances the precision on our dataset (cf. Fig. 3a), and
demonstrates the usefulness of expressing policy iteration as a typical fixpoint
computation. Furthermore, it provides a strong motivation to use integer formu-
las for integer variables in programs, and not their rational relaxation.
Optimizations In Sec. 3 we describe the local value-determination algorithm
which adds a quadratic number of constraints in terms of policies. In practice this
is often prohibitively expensive. The quadratic blow-up results from the “input”
constraints to each policy, which determine the bounds on the input variables.
We propose multiple optimization heuristics which increase the performance.
    As a motivation example, consider a long trace ending with an assignment x
= 1. If this trace is feasible and chosen as a policy for the template x, the output
bound will be 1, regardless of the input. With that example in mind, consider
the abstraction procedure from which we derive the bound d for the template t.
Let ( , φ(X, X ′ )) be the intermediate state used for the abstraction (Alg. 2). We
check the satisfiability of φ(X, X ′ ) ∧ t · X ′ > d; if the result is unsatisfiable, then
the bound of t is input-independent, that is, it is always d if the trace is feasible.
Thus we do not add the input constraints for the associated policy in the value-
determination stage. Also, when computing the map influencing from nodes
to abstracted states for the value-determination problem, we do not follow the
backpointers for input-independent policies, potentially drastically shrinking the
resulting constraint set. Similarly, if none of the variables of the “input template”
occur in the policy, the initial constraint is irrelevant and can be dropped.
    Furthermore, we limit the size of the value-determination LP by merging
some of the unknowns. This is equivalent to equating these variables, thus
strengthening the constraints. The result thus under-approximates the fixed
point of the selected policy. If it is less than the policy fixed point (not inductive
with respect to the policy), we fall back to the normal value determination.
    During abstraction on the intermediate state (a0 , ψ), we may skip the op-
timization query based on a syntactic check: if we are optimizing for the tem-
plate t, and none of the variables of t occur in ψ, we return the bound associated
with a0 [t].
    Additionally, during maximization we add a redundant lemma to the set of
constraints that specifies that the resultant value has to be strictly larger than
the current bound. This significantly speeds up the maximization by shrinking
the search space.
Iteration Order In our experiments, we have found performance to depend on
the iteration order. Experimentally, we have determined a good iteration order
to be the recursive iteration strategy using the weak topological ordering [20].
This is a strength of LPI: it blends into existing iteration strategies.
16

Unrolling We unroll loops up to depth 2, as some invariants can only be
expressed in the template constraints domain in the presence of unrollings (e.g.,
invariants involving a variable whose initial value is set only inside the loop).
Abstraction Refinement for LPI As a template constraints domain can
be configured by the number of templates present, it is a perfect candidate for
refinement, as templates can be added to increase the precision of the analysis.
    However, a full abstraction-refinement algorithm for LPI would be outside of
the scope of this work, and thus to obtain the results we use a naive algorithm
that iteratively tries progressively more precise and costly configurations until
the program can be verified. The configurations we try are (in that order): (i) In-
tervals (ii) Octagons (iii) Previous + Unrolling (iv) Previous + Rich Templates
(±x ± y ± z) (v) Previous + Congruence Analysis.

5      Experiments
We have evaluated our tool on the benchmarks from the category “Loops” of the
International Competition on Software Verification (SV-COMP’15) [21] consist-
ing of 142 C programs, 93 of which are correct (the error property is unreachable).
We have chosen this category for evaluation because its programs contain nu-
merical assertions about variables modified in loops, whereas other categories of
SV-COMP mostly involve variables with a small finite set of possible values that
can be enumerated effectively. All experiments were performed with the same re-
sources as in SV-COMP’15: an Intel Core i7-4770 quad-core CPU with 3.40 GHz,
and limits of 15 GB RAM and 900 s CPU time per program. The tool is integrated
inside the open-source verification framework CPAchecker [7], used configuration
and detailed experimental results are available at http://lpi.metaworld.me.
    We compare LPI (with abstraction refinement) with three tools representing
different approaches to program analysis: BLAST 2.7.3 (SV-COMP’15) [22],
which uses lazy abstraction, PAGAI (git hash 254c2fc693) [23], which uses ab-
stract interpretation with path focusing, and CPAchecker 1.3.10-svcomp15
(SV-COMP’15) [7], the winner of SV-COMP 2015 category “Overall”, which
uses an ensemble of different techniques: explicit value, k-induction, and lazy
predicate abstraction. For LPI we use CPAchecker in version 1.4.10-lpi-vmcai16.
    Because LPI is an incomplete approach, it can only produce safety proofs (no
counter-examples). Thus in Table 1 we present the statistics on the number of
safety proofs produced by different tools. The first five columns represent differ-
ences between approaches: the cell corresponding to the row A and a column B
(read “A vs. B”) displays the number of programs A could verify and B could not.
In the column Unique we show the number of programs only the given tool could
verify (out of the analyzers included in the comparison). The column Verified
shows the total number of programs a tool could verify. The column Incorrect
shows false positives: programs that contained a bug, yet were deemed correct
by the tool — our current implementation unsoundly ignores integer overflows,
as though the program used mathematical integers.10
10
     It is possible to add sound overflow handling, as done in e.g. Astrée, to our approach,
     at the expense of extra engineering.
                                                                                                                               17

                                        vs. PAGAI LPI BLAST CPAchecker Unique Verified Incorrect
                      PAGAI                               4        13              15         1           52               1
                      LPI                             13           20              20         7           61               1
                      BLAST                            6  4                         8         0           45               1
                      CPAchecker                      21 17        21                        12           58               2
                                  Table 1: Number of verified programs of different tools
                                           (LPI in abstraction-refinement mode)

               103         Intervals (verified: 34)                      103       PAGAI (verified: 52)
                           Above +Octagons (40)                                    LPI-Refinement (61)
                           +Unrolling (46)                                         BLAST (45)
                                                                         102
                           +Rich Templates (48)                                    CPAchecker (58)
CPU Time (s)




               102         +Congruence (55)                                        LPI-Intervals (34)
                                                                         101


                                                                         100
               101
                                                                        10−1


                                                                        10−2
                 0
               10
                      0     20    40     60    80     100   120   140          0    20     40     60   80      100   120   140
                                        Programs                                                  Programs

                     (a) Different LPI Configurations                                   (b) Different Tools
                                             Fig. 3: Quantile Timing Plots.
                            Each data point is an analyzed program, timeouts are excluded.

                    From this table we see that LPI verifies more examples than other tools can,
                including seven programs that others cannot.
               Timing Results In Sec. 4 we have described the various possible configura-
               tions of LPI. As trying all possible combinations of features is exponential, tested
               configurations represent cumulative stacking of features. We present the timing
               comparison across those in the quantile plot in Fig. 3a, and in the legend we re-
               port the number of programs each configuration could verify. Each data point is
               an analyzed program, and the series are sorted separately for each configuration.
                   The quantile plot for timing comparison across different tools is shown in
               Fig. 3b. We have included two LPI configurations in the comparison: fastest
               (LPI-Intervals) and the most precise one (LPI-Refinement, switches to a more
               expensive strategy out of the ones in Fig. 3a if the program cannot be verified).
               From the plot we can see that LPI performance compares favorably with lazy
               abstraction, but that it is considerably outperformed by abstract interpretation.
               The initial difference in the analysis time between the CPAchecker-based tools
               and others is due to JVM start-up time of about 2 seconds.

                6         Conclusion and Future Work
               We have demonstrated that LPI is a viable approach to program analysis, which
               can outperform state-of-the-art competitors either in precision (abstract inter-
18

pretation), or both in precision and scalability (predicate abstraction). However,
much work needs to be done to bring policy-iteration-based approaches to the
level of maturity required for analyzing industrial-scale codebases, in particular:
  – Sound handling of machine integers and floats, and overflow checking in par-
    ticular. The only incorrect result given by LPI on the dataset was due to the
    unsound overflow handling. It is possible to check the obtained invariants for
    inductiveness using bitvectors or overflow checks.
  – Template abstract domains are perfect candidates for refinement : dynam-
    ically adding templates during the analysis. Using counter-examples and
    refining the domain using CEGAR [24] approach is a promising research
    direction.
Acknowledgments The authors wish to thank Tim King for proof-reading
and extremely valuable feedback, Nikolaj Bjørner for improving νZ performance
on our difficult cases, and the anonymous reviewers for their helpful suggestions.

References
 1. P. Cousot and R. Cousot, “Abstract interpretation: A unified lattice model for
    static analysis of programs by construction or approximation of fixpoints,” in Con-
    ference Record of the Fourth ACM Symposium on Principles of Programming Lan-
    guages, Los Angeles, California, USA, January 1977, pp. 238–252, ACM, 1977.
 2. A. Miné, “The octagon abstract domain,” Higher-Order and Symbolic Computa-
    tion, vol. 19, no. 1, 2006.
 3. S. Sankaranarayanan, H. B. Sipma, and Z. Manna, “Scalable analysis of linear
    systems using mathematical programming,” in Verification, Model Checking, and
    Abstract Interpretation, 6th International Conference, VMCAI 2005, Paris, France,
    January 17-19, 2005, vol. 3385 of Lecture Notes in Computer Science, pp. 25–41,
    Springer, 2005.
 4. T. Gawlitza and H. Seidl, “Precise relational invariants through strategy iteration,”
    in Computer Science Logic, 21st International Workshop, CSL 2007, 16th Annual
    Conference of the EACSL, Lausanne, Switzerland, September 11-15, 2007, vol. 4646
    of Lecture Notes in Computer Science, pp. 23–40, Springer, 2007.
 5. T. M. Gawlitza and D. Monniaux, “Invariant generation through strategy itera-
    tion in succinctly represented control flow graphs,” Logical Methods in Computer
    Science, vol. 8, no. 3, 2012.
 6. A. Shamir, “A linear time algorithm for finding minimum cutsets in reducible
    graphs,” SIAM J. Comput., vol. 8, no. 4, pp. 645–655, 1979.
 7. D. Beyer and M. E. Keremoglu, “CPAchecker: A tool for configurable software ver-
    ification,” in Computer Aided Verification - 23rd International Conference, CAV
    2011, Snowbird, UT, USA, July 14-20, 2011, vol. 6806 of Lecture Notes in Com-
    puter Science, pp. 184–190, Springer, 2011.
 8. N. Bjørner, A. Phan, and L. Fleckenstein, “νZ - an optimizing SMT solver,” in
    Tools and Algorithms for the Construction and Analysis of Systems - 21st Interna-
    tional Conference, TACAS 2015, vol. 9035 of Lecture Notes in Computer Science,
    pp. 194–199, Springer, 2015.
 9. D. Beyer, T. A. Henzinger, and G. Théoduloz, “Configurable software verification:
    Concretizing the convergence of model checking and program analysis,” in Com-
    puter Aided Verification, 19th International Conference, CAV 2007, Berlin, Ger-
    many, July 3-7, 2007, vol. 4590 of Lecture Notes in Computer Science, pp. 504–518,
    Springer, 2007.
                                                                                    19

10. D. Beyer, M. E. Keremoglu, and P. Wendler, “Predicate abstraction with
    adjustable-block encoding,” in 10th International Conference on Formal Methods
    in Computer-Aided Design, FMCAD 2010, Lugano, Switzerland, October 20-23,
    pp. 189–197, IEEE, 2010.
11. P. Roux and P. Garoche, “Integrating policy iterations in abstract interpreters,”
    in Automated Technology for Verification and Analysis - 11th International Sym-
    posium, ATVA 2013, Hanoi, Vietnam, October 15-18, 2013, vol. 8172 of Lecture
    Notes in Computer Science, pp. 240–254, Springer, 2013.
12. D. Monniaux and P. Schrammel, “Speeding up logico-numerical strategy iteration,”
    in Static Analysis - 21st International Symposium, SAS 2014, Munich, Germany,
    September 11-13, 2014, vol. 8723 of Lecture Notes in Computer Science, pp. 253–
    267, Springer, 2014.
13. S. Gaubert, E. Goubault, A. Taly, and S. Zennou, “Static analysis by policy iter-
    ation on relational domains,” in Programming Languages and Systems, 16th Eu-
    ropean Symposium on Programming, ESOP 2007, vol. 4421 of Lecture Notes in
    Computer Science, pp. 237–252, Springer, 2007.
14. M. Colón, S. Sankaranarayanan, and H. Sipma, “Linear invariant generation using
    non-linear constraint solving,” in Computer Aided Verification, 15th International
    Conference, CAV 2003, Boulder, CO, USA, July 8-12, 2003, vol. 2725 of Lecture
    Notes in Computer Science, pp. 420–432, Springer, 2003.
15. D. Monniaux, “Automatic modular abstractions for template numerical con-
    straints,” Logical Methods in Computer Science, June 2010.
16. P. Cousot and N. Halbwachs, “Automatic discovery of linear restraints among
    variables of a program,” in Conference Record of the Fifth Annual ACM Symposium
    on Principles of Programming Languages, Tucson, Arizona, USA, January 1978,
    pp. 84–96, ACM Press, 1978.
17. D. Beyer, A. Cimatti, A. Griggio, M. E. Keremoglu, and R. Sebastiani, “Software
    model checking via large-block encoding,” in 9th International Conference on For-
    mal Methods in Computer-Aided Design, FMCAD 2009, 15-18 November 2009,
    Austin, Texas, USA, pp. 25–32, IEEE, 2009.
18. D. Monniaux and L. Gonnord, “Using bounded model checking to focus fixpoint
    iterations,” in Static Analysis - 18th International Symposium, SAS 2011, Venice,
    Italy, September 14-16, 2011, vol. 6887 of Lecture Notes in Computer Science,
    pp. 369–385, Springer, 2011.
19. T. Gawlitza and H. Seidl, “Precise fixpoint computation through strategy itera-
    tion,” in Programming Languages and Systems, 16th European Symposium on Pro-
    gramming, ESOP 2007, vol. 4421 of Lecture Notes in Computer Science, pp. 300–
    315, Springer, 2007.
20. F. Bourdoncle, “Efficient chaotic iteration strategies with widenings,” in Formal
    Methods in Programming and Their Applications, vol. 735 of Lecture Notes in
    Computer Science, pp. 128–141, Springer Berlin Heidelberg, 1993.
21. D. Beyer, “Software verification and verifiable witnesses - (report on SV-COMP
    2015),” in Tools and Algorithms for the Construction and Analysis of Systems - 21st
    International Conference, TACAS 2015, vol. 9035 of Lecture Notes in Computer
    Science, pp. 401–416, Springer, 2015.
22. P. Shved, M. U. Mandrykin, and V. S. Mutilin, “Predicate analysis with BLAST
    2.7 - (competition contribution),” in Tools and Algorithms for the Construction
    and Analysis of Systems - 18th International Conference, TACAS 2012, vol. 7214
    of Lecture Notes in Computer Science, pp. 525–527, Springer, 2012.
23. J. Henry, D. Monniaux, and M. Moy, “PAGAI: A path sensitive static analyser,”
    Electr. Notes Theor. Comput. Sci., vol. 289, 2012.
20

24. E. M. Clarke, O. Grumberg, S. Jha, Y. Lu, and H. Veith, “Counterexample-guided
    abstraction refinement,” in Computer Aided Verification, 12th International Con-
    ference, CAV 2000, Chicago, IL, USA, July 15-19, 2000, vol. 1855 of Lecture Notes
    in Computer Science, pp. 154–169, Springer, 2000.
