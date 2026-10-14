                                         Incremental Symbolic Bounded Model Checking of
                                          Software Using Interval Methods via Contractors
                                                Mohannad Aldughaim, Kaled Alshmrany, Rafael Menezes, Alexandru Stancu, and Lucas C. Cordeiro
                                                                                      University of Manchester, Manchester, UK


                                            Abstract—Bounded model checking (BMC) is vital for finding         best suited for concurrent systems as it takes advantage of the
                                         program property violations. For unsafe programs, BMC can             commutative transitions that result in the same state. Another
                                         quickly find an execution path from an initial state to the           successful attempt was Counterexample-Guided Abstraction
                                         violated state that refutes a given safety property. However,
                                         BMC techniques struggle to falsify programs that contain loops.       Refinement (CEGAR) made by Clarke et al. [7]. This method
                                                                                                               converts the code to be verified into an abstract model. Then
arXiv:2012.11245v3 [cs.SE] 21 Sep 2022




                                         BMC needs to incrementally unfold the program loops up to the
                                         bound k, exposing the property violation, which can thus lead         it refines this model according to the property being verified.
                                         to exploring a considerable state space. Here, we describe and        This method keeps the state space small using abstraction
                                         evaluate the first verification method based on interval methods      functions that determine each variable’s level of abstraction.
                                         via contractors to reduce the domains of variables representing
                                         the search space. This reduction is based on the specified property      Biere et al. in 1999 [8] introduced Bounded Model Check-
                                         modeled as functions representing the contractor constraints.         ing (BMC), which uses Boolean Satisfiability (SAT) or Sat-
                                         In particular, we exploit interval methods via contractors to         isfiability Modulo Theories (SMT) solvers’ speed to find a
                                         incrementally analyze the program loop variables and contract         counterexample of a fixed length, reducing the state-space
                                         the domain where the property is guaranteed to hold to prune          size exploration. BMC aims to find errors rather than prove
                                         the search exploration, thus reducing resource consumption
                                         aggressively. Experimental results demonstrate the efficiency and     the absence of them [9]. Some approaches aim to under-
                                         efficacy of our proposed approach over a large set of benchmarks,     approximate and widen the system’s model based on the proof
                                         including 7044 verification tasks, compared with state-of-the-art     of unsatisfiability extracted from SMT solvers [10]. And some
                                         BMC tools. Our proposed method can reduce memory usage up             approaches over-approximate and then narrow the search,
                                         to 75% while verifying 1% more verification tasks.                    such as property-directed reachability (PDR) [11]. PDR is a
                                            Index Terms—Interval methods, constraint satisfaction prob-
                                         lem, software verification, model checking.
                                                                                                               derivative of the IC3 algorithm that has been used successfully
                                                                                                               to verify hardware [12].
                                                                                                                  Here, we advance the state-of-the-art in software model
                                                                 I. Introduction
                                                                                                               checking and introduce a novel verification method to re-
                                            Software model checking prevents software errors that              duce the search space exploration using interval methods via
                                         could cause financial losses or risk individuals’ well-being          contractors [13]. Abstract interpretation techniques exist to
                                         [1]. Developed originally by Clarke and Emerson [2] and               compute intervals [14]. If we compare interval analysis and
                                         by Queille and Sifakis [3], Model Checking models the                 methods with abstract interpretation techniques, they share
                                         software into states that will be explored exhaustively; it is        the same formal definitions and operations over intervals.
                                         considered one of the most successful methods for its use in          However, they differ regarding interval methods since we
                                         research and industry [1]. Model-checking started with mainly         can use forward and backward operations to “contract” the
                                         hardware verification in mind, and over the years, researchers        search space exploration from the program’s entry point to the
                                         developed the technique to include many aspects of software           property being verified and vice-versa. Therefore, contractors
                                         verification. However, one of the critical problems is the state-     make interval methods more practical by reducing the domain
                                         space explosion problem [1]. The growth rate of states is             of the program variables using off-the-shelf solvers targeted at
                                         exponential in the number of variables and processes. With            constraint satisfaction problems (CSP) [15]. Interval methods
                                         fairly complex software systems, the number of states it will         applications in robotics, medicine, and finance, showed that
                                         produce can grow out of proportion, which, in turn, will take         it could prove the existence of a solution while taking into
                                         a substantial amount of memory and time to perform the                account all sources of uncertainty [16].
                                         verification process automatically.                                      Intuitively, our approach works as follows: first, we model
                                            There exist studies that tackled the state explosion problem       the software properties as constraints. Second, we analyze
                                         using various efficient data structures to represent the system’s     the intervals for each variable. Third, we apply contractors
                                         states [4]–[8]. One of the first techniques is Symbolic Model         to analyze those variables’ search space, identify where a
                                         Checking with Binary Decision Diagrams (BDDs) [4] [5],                property is guaranteed to hold, and remove the states as-
                                         which is performed using a fixed-point algorithm. Here, rather        sociated with identified values. What remains is a smaller
                                         than listing each state individually, the states are represented      upper bound region where constraints are satisfied. Finally, we
                                         using a BDD, exponentially smaller than explicitly enumerat-          provide those regions with the BMC procedure to perform the
                                         ing the entire state-space and performing explicit-state model        automated symbolic verification. Experimental results show
                                         checking. Peled [6] introduced Partial Order Reduction (POR)          how our approach improved verification tasks’ scores while
                                         techniques to reduce state-space exploration. This technique is       lowering resource consumption. This work significantly ex-
tends our technical report [17], which now considers the full           encodes all the changes in variables and pc from si to si+1 .
implementation and extensive experimental evaluation of our             Next is to compute a Verification Condition (VC) denoted by
proposed method.                                                        Ψ, a quantifier-free formula in a decidable subset of first-order
Contributions. The main original contributions of this paper            logic. Given a transition system M , a property φ, and a bound
can be summarised as follows:                                           k, BMC unrolls the system k times to produce Ψ such that Ψ
   • We develop and evaluate a novel verification method                is satisfiable iff φ has a counterexample of length k or less.
     based on interval methods via contractors, which con-
     tracts the domains of variables representing the search                                      k i−1
                                                                                                  _ ^
     space. This contraction is based on the specified property                   Ψk = I(s0 ) ∧             γ(sj , sj+1 ) ∧ ¬φ(si )    (3)
     modelled as functions representing the contractor con-                                       i=0 j=0
     straints.
   • We prune the search space not to include the verified                 In the logical formula (3), I denotes the set of initial
     property region, which will always hold, thus reducing             states of M , γ(sj , sj+1 ) denotes the relation between two
     time and memory usage. We perform this step using                  states in M . φ denotes the safety   Vi−1properties that should
     the contractor to reduce the guaranteed area inside the            not be violated. Hence, I(s0 ) ∧ j=0 γ(sj , sj+1 ) represents
     solution.                                                          the execution of M of length i and if there exists some
   • Experimental results demonstrate the efficiency and ef-            i ≤ k such that it satisfies Ψk at time-step i there exists
     ficacy of our proposed approach over a large set of                a state in which φ is violated. Then Ψk is given to an
     benchmarks compared with state-of-the-art BMC tools,               SMT solver to be checked for satisfiability. If it is satisfiable,
     where we can reduce memory usage up to 75% while                   then the SMT solver will provide an assignment that satisfies
     verifying 1% more verification tasks.                              Ψk . With this assignment, the counterexample is constructed
                                                                        using the values extracted from the program variables. For a
                       II. Preliminaries                                property φ, a counterexample consists of a sequence of states
A. Soundness and Completeness                                           {s0 , s1 , .., sk }|s0 ∈ S0 and si ∈ S|0 ≤ i < k and γ(si , si+1 ).
                                                                        If Ψk is unsatisfiable, no error state is reachable in k steps or
Definition 1 (Soundness). For a verifier to be considered
                                                                        less; therefore, no property was violated. Tools that implement
sound, it must reason about all program executions. Thus,
                                                                        BMC for software [20] produce two quantifier-free formulae,
if the verifier result concludes that there are no bugs, i.e.,
                                                                        represented by C and P , which encode the constraints and
the verification outcome is TRUE, then the program is safe
concerning the specified property. Formally, we can define
                                                                        properties, resp. W        Vi−1C serves as the first part of Ψk ,
                                                                                               Formula
                                                                                                k
                                                                        which is I(s0 ) ∧ i=0 j=0 γ(sj , sj+1 ). As for ¬P , it serves
soundness with the following equation:                                                                       Wk
                                                                        as the second part of Ψk which is i=0 ¬φ(si ). Then the SMT
 ∀ p ∈ L, verifier(p) = TRUE =⇒ p satisfies P (1)                       solver checks C |=T P in the form of C ∧ ¬P .
where L is the set of all programs, the program verifier                   BMC can also be used for soundness (cf. Definition 1)
is sound with respect to property P [18]                                under certain conditions. A completion threshold (CT ) is used
                                                                        to provide soundness [9]. This threshold checks whether k
Definition 2 (Completeness). For a verifier to be considered            reaches all reachable states of M . This means a path of size k
complete, it must have a concrete program execution that                that can reach the program’s last state starting from the initial
results in a property violation. Thus, if the verifier reports          state. CTk can be defined as:
a bug, then the program is unsafe concerning the specified
property. Similar to soundness 1, we can define completeness                                      k
                                                                                                  ^
with the following equation:                                                     CTk = I(s0 ) ∧         γ(si , si+1 ) ∧ ¬(sk = sn )    (4)
                                                                                                  i=0
 ∀ p ∈ L, verifier(p) = TRUE ⇐= p satisfies P (2)
                                                                        where n is the last reachable state of M . In BMC, if Ψk ∨CTk
B. Incremental Bounded Model Checking (BMC) of Software                 is UNSAT for a given k, then the program can be considered
   In BMC, the program is modeled as a state transition system          safe. Finding the optimal value for k is not always possible
(TS), which is derived from its control-flow graph [19], and            due to unbounded loops (i) or limited system resources (ii).
then converted to a Static Single Alignment form (SSA). Each            Considering these limitations, two approaches can be used:
control graph node will be converted to either an assignment            k-induction (for i) and incremental (for ii).
or a conditional statement converted to a guard. Each edge
represents a change in the program’s control location [20].             Definition 3 (Incremental-BMC). In this approach, the value
When modeling the program, a Kripke structure [21] is used as           of k is incremented interactively until all states are reached (or
TS M = (S, T, S0 ), which is an abstract machine that has a set         resources are exhausted) [22]. We can define the incremental-
of states S, initial states S0 ⊆ S, and transition relation T ⊆         BMC for a program P and bound k as Inc(P, k):
S × S. The set of states S = {s0 , s1 , ...sn } : n ∈ N contains                       
all the states. Each state has the value of each variable in the                       P is unsafe,
                                                                                                           Ψk is SAT
program and a program counter pc. Each transition is denoted              Inc(P, k) = P is correct,         Ψk ∨ CTk is UNSAT (5)
by γ(si , si+1 ) ∈ T , where it represents a logical formula that
                                                                                       
                                                                                       Inc(P, k + 1), otherwise.



                                                                    2
C. Interval Analysis and Methods
Definition 4 (Interval). An interval is a connected, closed
subset of R denoted by [x]. It has a lower and an upper limits
that are scalars denoted by x and x, respectively, where x, x ∈
R. An interval is defined as [x] = [x, x] ∈ IR, where IR is
the set of all intervals of R [23].
    Here, we assume that x ≤ x, nonetheless, in the field of             Fig. 1: CSP with x ∈ R2 , initial box√[x] = [0.5, 1.2]×[0.4, 0.6],
Model Interval Analysis [23] it is possible to have x > x.               and two constraints: y ≥ x2 , y ≤ x. Inner contractor versus
However, this case is outside this paper’s scope, which does             an outer contractor. Sout and Sin are the remainder of Cout
not mean that the opposite is invalid as it is used in the field         and Cin actions [24].
of Model Interval Analysis [23]. Each interval has a width
and center, which are respectively defined as: w([x]) = x −
x and c([x]) = x+x   2 , where width and center are w and c,             estimated solution such that Sout ∩Sx = ∅ color-coded in blue.
respectively. An interval is considered degenerate or punctual           Sboundary is the boundary set that represents the area that both
if its width is 0, i.e., w = 0. Intervals can be extended to             include the solution and its inverse such that Sboundary ∩ Sx 6=
multiple dimensions. An interval in n dimensions is a vector             ∅ and Sboundary 6⊂ Sx color-coded in orange.
of intervals for each dimension. Such as [x] = [x1 ] × [x2 ] ×
                                                                            For different CSPs, there are many types of contractors [26],
... × [xn ], where [x] is called a box and [x] ∈ IRn . A box is
                                                                         [27]. However, in this paper, we will use Forward-backward
an axis-aligned hyperrectangle in Rn .
                                                                         Contractor [28] for its simplicity and efficiency.
    1) Set Operations and Arithmetic: Every interval is a set,
but not vice-versa [24]. For a set to be an interval, it has to be       Definition 7 (Forward-backward Contractor). Forward-
closed, connected and defined in real numbers. Set operations            backward Contractor is a contractor (cf. Definition 6) that is
include intersection, union and difference. Set operations can           applied to a CSP with one single constraint; it contracts in two
also be extended to multiple dimensions.                                 steps: forward propagation and backward propagation [24];
    Intervals also have arithmetic and functions that are applied        they are illustrated in Algorithm 1.
extensively [25]. That includes addition and multiplication at
a basic level. Division and subtraction are best described as
interval functions [24].                                                 Algorithm 1 Forward-backward Contractor C↑↓ .
Definition 5 (Constraint Satisfaction Problem). A constraint              1: function C↑↓ ([x], f (x), [I]) do
satisfaction problem (CSP), in the context of interval analysis,          2:   [y] = [I] ∩ [f ]([x])
is defined as the triple (x, [x], f (x) ≤ 0), where x ∈ Rn is a           3:   for all [xi ] ∈ [x] : i ∈ {1, ..., n} do
set of n variables, [x] ∈ IRn is box representing the interval            4:      [xi ] = [xi ] ∩ [fx−1
                                                                                                      i
                                                                                                        ]([y], [x])
domain of each variable (cf. Definition 4), and f (x) ≤ 0                 5:   end for
are the set of constraints such that f : Rn → Rm is a vector              6:   return [x]
function whose coordinates are fj , ∀j ∈ {1, . . . , m} [24]. The         7: end function
solution set of the CSP is defined as:
                   Sx = {x ∈ [x] | f(x) ≤ 0}.                 (6)           Generally, a CSP can have multiple constraints; to handle
                                                                         such a situation, we can use Outer Contractor, which applies
                                                                         forward-backward contractor on each constraint independently
  2) Interval Methods: Given a CSP, interval methods are                 as shown in Algorithm 2 [24].
heuristic search algorithms that estimate an upper bound
solution.
                                                                         Algorithm 2 Outer Contractor Cout .
Definition 6 (Contractor). A contractor is an interval method
that estimates the solution of a given CSP (cf. Definition 5)             1: function Cout ([x], f(x)) do
with the map C : Rn → Rn . Let Sx be the set of solution and              2:   for all fj ∈ f : j ∈ {1, ..., m} do
C : Rn → Rn be a contractor, which is applied to box [x] then             3:     [x] ← C↑↓ ([x], fj (x), (−∞, 0])
C([x]) ⊆ [x] and C([x]) ∩ Sx = [x] ∩ Sx . The former satisfies            4:   end for
the contraction condition and the latter satisfies correctness            5:   return [x]
condition [13].                                                           6: end function

   As illustrated in Fig. 1, we can have inner contractor Cin and
outer contractor Cout , which are complements of each other                 Forward-backward contractor can be used to construct an-
in terms of constraints.                                                 other type of contractor where the complementary CSP is
   After applying the contractor, the result is best described           considered; such contractor is called Inner Contractor, and
as three sets: Sin is the estimated solution of Sx such that             its procedure is defined in Algorithm 3 [24].
Sin ⊂ Sx color-coded in red. Sout is the complement of the



                                                                     3
Algorithm 3 Inner Contractor Cin .                                         1 unsigned int x=nondet_uint();
 1: function Cin ([x], f(x)) do                                            2 unsigned int y=nondet_uint();
                                                                           3 __ESBMC_assume(x <= 20);
 2:   [x̂] ← ∅                                                             4 assert(x >= y);
 3:   for all fj ∈ f : j ∈ {1, ..., m} do
 4:       [x̂] ← [x̂] t C↑↓ ([x], fj (x), (0, ∞))
 5:   end for                                                                           Fig. 3: Outer contractor example.
 6:   return [x̂]
 7: end function                                                                  f (x) ≤ 0              I = (−∞, 0]
                                                                            f (x) : y = x2 − x1     [y] = I ∩ ([x2 ] − [x1 ])      Forward-step
                                                                          f (x)−1
                                                                               x 1 : x1 = x2 − y   [x1 ] = [x1 ] ∩ ([x2 ] − [y])   Backward-step
    III. Incremental Symbolic Bounded Model Checking of                   f (x)−1
                                                                               x 2 : x2 = y + x1   [x2 ] = [x2 ] ∩ ([y] + [x1 ])   Backward-step
      Software Using Interval Methods via Contractors
   Here, we introduce contractors described in Section II-C to              Fig. 4: Outer contractor steps for the example in Fig 3.
BMC of software. In particular, we model the constraints and
properties generated from BMC instances to a CSP [29]. In a
CSP, we have three inputs: variables (dimensions), domain,               property violation since that area is outside the solution Sout .
and constraints. We obtain the domains by analyzing the                  We can visualize the results in Fig. 5, where the left graph
declaration of independent variables, assume statement and               shows our initial domain, the right graph shows the contracted
variable assignment (BMC constraints). The directive assert,             domain in blue, and the area remaining in orange.
which represents the property, will give the contractor con-
straints. Assert statements will also dictate which variables
are included in our defined domains. We apply the contractors
in the intermediate representation (IR) of programs. Our IR is
a GOTO-program that simplifies the program representation
(e.g., replaces switch and while by if and goto statements) [10],
[20]. Fig. 2 shows how contractors can be used in BMC, where
the GOTO-symex component perform the program symbolic
execution.
                                                                                       Fig. 5: Outer Contractors in BMC.

                                                                            However, if we use the inner contractor, which is the
                                                                         complement of our constraint f (x) > 0, we may prune the
                                                                         area inside our solution Sin to possibly prune our search
                                                                         space and only have the Sboundary area to be checked by
                                                                         BMC. Consider the example in Fig. 6, we form our CSP by
                                                                         having our variables: let x be x1 and y be x2 , and domain be
                                                                         [x1 ] = [20, 30] and [x2 ] = [0, 30]. Constraint as x1 ≥ x2 .

                  Fig. 2: Contractors in BMC.
                                                                           1 unsigned int x=nondet_uint();
   As an illustrative example, we consider the code fragment               2 unsigned int y=nondet_uint();
                                                                           3 __ESBMC_assume(x >= 20 && x <= 30);
illustrated in Fig. 3. We model this code into a CSP by having             4 __ESBMC_assume(y <= 30);
our variables x as x1 and y as x2 . Assume the maximum                     5 assert(x >= y);

value that an unsigned integer can hold, defined as Maxuint .
Therefore, we define our intervals for each variable from                                Fig. 6: Inner contractor example.
the declaration of the variables. [x1 ] = [0, Maxuint ], [x2 ] =
[0, Maxuint ]. With the assume directive, variable x1 interval
will be [x1 ] = [0, 20]. With the given assertion x>=y, we                        f (x) > 0               I = [0, ∞)
determine the inequality used being x1 ≥ x2 as our constraint.              f (x) : y = x2 − x1     [y] = I ∩ ([x2 ] − [x1 ])      Forward-step
Now we have our CSP, we model our input as parameters                     f (x)−1
                                                                               x 1 : x1 = x2 − y   [x1 ] = [x1 ] ∩ ([x2 ] − [y])   Backward-step
for a contractor such that: Variables x1 , x2 ; Domains, [x1 ] =
                                                                          f (x)−1
                                                                               x 2 : x2 = y + x1   [x2 ] = [x2 ] ∩ ([y] + [x1 ])   Backward-step
[0, 20], [x2 ] = [0, Maxuint ]; Constraint, x2 − x1 ≤ 0.
   We use the forward-backward contractor [28] mentioned
in Definition 7. After we plug our values in the equations                  Fig. 7: Inner contractor steps for the example in Fig 6.
in Fig. 4, we obtain [y] = [−20, 0], [x1 ] = [0, 20] and [x2 ] =
[0, 20]. We notice that [x2 ] was contracted from [0, Maxuint ] to          For the inner contractor, we list our formulas as illustrated in
[0, 20] because that is where our solution lies. Regarding BMC,          Fig. 7. So we plug our values for [x1 ] and [x2 ]; we obtain [y] =
having the domain contracted by the outer contractor ensures             [0, 10], [x1 ] = [20, 30] and [x2 ] = [20, 30]. Here, [x2 ] was



                                                                     4
contracted from [0, 30] to [20, 30]. To visualize the solution, in       it means that the domain will violate the property(s). There
Fig. 8, the red area is contracted from our domain; it represents        is no need to prune the search space (lines 2 and 3 of
the part of our domain that belongs to Sin . For BMC, this               Algorithm 5). Otherwise, the difference between the result
area is guaranteed to hold the property; therefore, we prune             from the outer contractor [x]0 and the original domain [x]
our search space to the orange area Sboundary only.                      will yield Sout , as demonstrated in line 10 of Algorithm 4.
                                                                         After that, we apply the inner contractor Cin to remove the
                                                                         intervals inside the solution where the property holds. Similar
                                                                         to the outer contractors, the difference between the two sets
                                                                         [x]00 and [x]0 will yield the set inside the solution Sin . Note
                                                                         that box difference will not necessarily yield one single box
                                                                         but rather a finite set of boxes [24]. The resulting domain
                                                                         from the contractor [x]00 will be our boundary area, where
                                                                         [x]00 ⊆ Sboundary . With Sout , Sin and Sboundary , now we can
                                                                         instrument the program for the BMC engine to search for a
              Fig. 8: Inner Contractors in BMC.                          counterexample in Sout and Sboundary while removing Sin
                                                                         from the search-space.
   Algorithms 4 and 5 contain the main steps necessary for                  The instrumentation will be done using the
our approach. The first four lines describe each variable we             assume(expr) directive, where we constrain the search
will use throughout the process. We will analyze the variables           space indicated by the expression expr, which the contractors
x and their intervals (or domain) [x] and the properties (or             produced. Note that instrumenting assume(expr) directive
constraints in the context of CSP) f(x) ≤ 0. Then, after call-           is not a trivial task since we need to ensure where the pruned
ing Apply Contractor, we initialize the contractors based                intervals are in the context of the program, especially when
on variables and constraints. The outer contractors Cout are             it comes to loops. If Sin is at the end of the loop, we add
initialised based on the property in the form of f (x) ≤ 0 or            the assume(Sout ∪ Sboundary ) to remove these unnecessary
f (x) = 0, which depends on the property. In contrast, the               loop steps in the loop. However, if Sin is at the beginning or
inner contractor Cin is initialized in the form f (x) > 0 or             middle of the loop, we discussed it further in Section V-E.
f (x) 6= 0.
                                                                            We will use the illustrative example in Fig. 9 to demonstrate
                                                                         the application of the steps of Algorithm 4. Note that we have
Algorithm 4 Proposed method algorithm.
                                                                         two variables in this program x and y, which will be x1 and
Input: Program P                                                         x2 in the CSP space, respectively, where x = {x1 , x2 }. For
 1: x : set of Variables                                                 the domain, after the analysis, they will be x1 = [1, Maxint ]
 2: [x] : domain                                                         and x2 = [0, 1000] with [x] = [1, Maxint ] × [0, 1000], while
 3: f(x) ≤ 0 : set of Constraints                                        the constraint will be x1 ≥ x2 where f(x) ≤ 0 ⇒ f (x) =
 4: f(x) ≤ 0 ← Analyze P roperties(P )                                   x2 − x1 ≤ 0. Therefore, our constraints will be in the form of
 5: [x] ← Analyze Intervals(P )                                          x2 − x1 ≤ 0 for the outer contractor and x2 − x1 > 0 for the
 6: [x] ← Apply Contractor(x, [x], f(x) ≤ 0)                             inner contractor. In this case, however, the outer contractor re-
 7: P 0 ← instrument(P, [x])                                             turned the same domain, which means it cannot be contracted
 8: return P 0                                                           from the outside because there are no values in the domain [x]
                                                                         guaranteed to be outside the solution, thus Sout = ∅. Fig. 10
                                                                         illustrates the outcome of the inner contractor on the program
Algorithm 5 Apply Contractor.                                            (line 12 of Algorithm 4), where the domain were reduced from
Input: Varibles x, Domains [x], Constraints f(x) ≤ 0                     [x]0 = [1, Maxint ] × [0, 1000] to [x]00 = [1, 1000] × [1, 1000]
 1: [x]0 ← Cout ([x], f(x))                                              where Sin = {[1000, Maxint ]×[0, 1000], [0, 1000]×[0, 1]} and
 2: if [x]0 = ∅ then                                                     Sboundary ← [x]00 . An example of the employed instrumenta-
 3:    P0 ← P                                                            tion is shown in Fig. 11. The assume(expr) directive here
 4: else                                                                 is placed in the loop, where the values change for variables.
 5:    Sout ← [x] \ [x]0                                                 It is placed in this location to guide the verifier not to check
 6:    [x]00 ← Cin ([x]0 , f(x))                                         steps further in the loop because these steps represent Sin ,
 7:    Sin ← [x]0 \ [x]00                                                where the property is guaranteed to hold.
 8:    Sboundary ← [x]00
 9: end if
10: return Sboundary ∪ Sout                                                                    IV. Implementation

   With CSP components being set up, we contract our domain                 The implementation of the proposed approach follows the
starting with Cout , where the domain will be reduced to                 Algorithm 4 and goes into the following steps, as described
exclude the region outside the solution, which violates the              below. Though it has limitations, we will discuss them further
property. If the resulting set of the domain [x]0 is empty,              in Section IV-E.



                                                                     5
  1  #include <assert.h>                                                 1  #include <assert.h>
  2  int main() {                                                        2  int main() {
   3     int x = 1, y = 0;                                                3     int x = 1, y = 0;
   4     while (y < 1000                                                  4     while (y < 1000
   5              && __VERIFIER_nondet_int()) {                           5              && __VERIFIER_nondet_int()) {
   6         x = x + y;                                                   6         x = x + y;
   7         y = y + 1;                                                   7         y = y + 1;
   8     }                                                                8         assume(x <= 1000);
   9     assert(x >= y);                                                  9     }
  10     return 0;                                                       10     assert(x >= y);
  11 }                                                                   11     return 0;
                                                                         12 }


Fig. 9: C program extracted from sv-benchmarks/c/loop-
lit/afnp2014.c, where __VERIFIER_nondet_int() returns                         Fig. 11: afnp2014.c after applying contractors.
a non-deterministic integer.
                                                                               n          ∈      V                     scalar values
                                                                               x          ∈      X                     program variable
                                                                                         ::=     + | − | ∗ | ...       binary operator
                                                                               R         ::=     < | ≤ | == | ...      comparison operator
                                                                               E         ::=                           scalar expressions
                                                                                           |     n                     scalar constant
                                                                                           |     x                     variable
                                                                                           |     E      E              binary operation
                                                                               B         ::=                           Boolean expressions
                                                                                           |     E R E                 Compare two expressions
                                                                               L         ::=                           logical expression
                                                                                           |     B
                                                                                           |     B ∧B                  and
                                                                                           |     B ∨B                  or
Fig. 10: afnp2014.c search space before and after contractors.
                                                                                                     Fig. 12: IBEX Syntax.

A. Property Analysis
                                                                          The contractor type used is the forward-backward con-
   In this step, we will analyze the property used as a con-           tractor. With the constraint and the variables parsed from
straint in the CSP. We start with parsing each expression in           the first step, and domains from the second step, we create
the assert directive, which is carried by converting from              the contractor with the constraint complement to reduce the
the syntax of ESBMC GOTO-program to the IBEX syntax.                   intervals inside the solution. As described previously, the
Figures 13and 12 illustrate both syntaxes, where we notice             contractor will need a CSP; at this point, we should have all
that IBEX syntax is more strict in its structure than ESBMC’s          the components to apply it. We have the list of constraints, the
syntax. For example, (x > 1) + 1 is allowed in ESBMC’s                 variables, and their domains. The resulting domains from the
syntax but not IBEX. Furthermore, IBEX syntax does not                 contractor will represent where the property may be violated,
have an operator for ! =, which makes it hard to convert               thus limiting the search space for BMC.
some expressions. While parsing an expression, we build a
list of variables inside the assertions, which we will use later       D. Modify Original Program
to analyze intervals. We have two lists updated from this                 With the resulting intervals, we compare them to the original
procedure: a list of variables and a list of constraints.              and insert the assume directive based on the difference. This
                                                                       is to tell BMC to ignore the instructions (loop iterations),
B. Interval Analysis                                                   which will result in holding the property.
  Interval analysis builds intervals for each variable that is
in the assert statements. These intervals will serve as do-            E. limitations
mains for the CSP. The current implementation now utilizes               In property analysis, we only support a limited number
--interval-analysis option in ESBMC and parses                         of conversions, which are one-to-one conversions. However,
each assume statement inserted by it. At each assume, we               some expressions require a more complex conversion. For
check whether the variable used is in our list, and if it is, we       example, IBEX does not support the != operator since a union
update its interval.
                                                                                   E       ::=                       scalar expressions
C. Interval Methods (Apply Contractor)                                                       |       n               scalar constant
                                                                                             |       x               variable
   For contractors, we chose IBEX library.1 IBEX is a C++                                    |       E    E          binary operation
library for constraint processing over real numbers. It started                              |       E R E           Compare two expressions
                                                                                             |       E ∧E            and
in 2007 as an open-source academic project that provides                                     |       E ∨E            or
algorithms for handling non-linear constraints. IBEX is also                                 |       ¬E              not
                                                                                             |       T ypecast(E )   typecast
the only Interval Analysis library that implements contractors.                    ...

  1 http://www.ibex-lib.org/                                                         Fig. 13: ESBMC goto-program Syntax.



                                                                   6
of intervals can represent it. Another example is (x>1)+1,             swapping or turbo during our experiments, and all executed
where it is possible to have in GOTO-program syntax but not            tools were restricted to a single core.
in IBEX’s syntax. That is because IBEX syntax would not
allow adding a logical expression to a scalar or any other             C. Description of the Benchmarks
expression, as illustrated in Fig. 12. So the conversion of               We evaluate our approach using 7044 tasks in
such expressions will be more complex and not a one-to-one             unreach-call benchmarks from SV-COMP 2022 [35],
conversion. Also, we only deal with one constraint per time.           which can be described as verifying whether exists an
Additionally, we will not convert expressions if the property          execution path that can lead a benchmark to an assertion
has an unsupported operator, which includes ! =, ==, &&, ||.           failure. This category contains benchmarks extracted from
   The interval analysis option’s drawback in ESBMC is that            various domains (e.g., linux drivers, recursion, unbounded
the intervals are sometimes too broad to be helpful for the            loops, algorithms, real-world, etc.). Due to massive arithmetic
contractor. Additionally, the lack of floating-point interval          computation within loops, this category can result in many
analysis could hinder the future since IBEX deals exclusively          timeouts (i.e. a tool can not verify it in a given time
with double datatype.                                                  constraint); they fit our approach. All tools, benchmarks,
                                                                       and evaluation results are available on a supplementary web
                 V. Experimental Evaluation
                                                                       page2 .
A. Objectives
   This experiment will compare results from performing                D. Results
incremental-BMC (cf. Definition 3) with and without con-                  ESBMC with contractors had been evaluated on unreach-
tractors in terms of time and memory consumption. This                 call property in 13 subcategories in SV-COMP. Table I
evaluation will answer the following main experimental goals:          shows our comparison results with other BMC state-of-the-
                                                                       art tools. Our approach showed its effectiveness in multiple
   EG1 (Efficiency) Does the contractors prune the search              subcategories regarding score and resource consumption. In
       space to consume less resources when verifying                  detail, we improved ESBMC incremental-BMC in Arrays,
       programs with ESBMC?                                            ControlFlow, ECA, Heap, and Loops. Moreover, Table III
   EG2 (Soundness and completeness) Do the contrac-                    shows how much memory contractors saved during the execu-
       tors and resulting code instrumentation preserve                tion of these benchmarks. Although some categories consumed
       the soundness and completeness when verifying                   more memory with contractors, the total shows a combined
       programs with ESBMC?                                            decrease in memory usage that amount to 75%.
   EG3 (Improve ESBMC in programs with large
       loops) Does our approach improve ESBMC per-
       formance in programs with large loops?                             The experimental results show that our method helped
                                                                          BMC efficiently reduce resource consumption, which
                                                                          includes a reduction of 75% of memory usage while
B. Description of the Setup                                               verifying 1% more benchmarks than our baseline,
                                                                          which thus successfully answers EG1.
   We executed ESBMC with the same set of options of
SV-COMP 2022, differing only on the strategy chosen (i.e.,
k-induction or incremental-bmc). We compare our results                   Our approach had shown its capabilities in these bench-
with state-of-the-art tools from SV-COMP 2022. These tools             marks by scoring the same as ESBMC incremental-BMC or
include CBMC [30] for its success over the years. Veriabs [31],        even higher. We have the lead in subcategories XCSP and
which is the SV-COMP 2022 champion in this category and                AWS-C-Common, and we are a close second in Floats.
the runner-up CPA Checker 2.1 [32] and Verifuzz [33]. SV-              Also, our approach ranked third in our comparison of Loops,
COMP score system consists in: (+2) for correct true, (+1) for         Arrays, and Heap categories. This shows how valuable
correct false, (-32) for incorrect true, and (-16) for incorrect       contractors are in real-world programs because we scored
false.                                                                 higher than other tools and decreased the verification time and
   All experiments were conducted on an Intel(R) Xeon(R)               memory. However, contractors could not improve the score
CPU E5-2620 v4 @ 2.10GHz and 160GB of RAM. We                          in other categories, for it was not applicable in the current
set time and memory limits of 900 seconds and 15GB for                 implementation. The cases where contractors could not be
each benchmark, respectively. Finally, we present the results          applied are due to our naive approach to detecting monotonic-
by showing the verification time and scores. All presented             ity and due to it only supporting a subset of operators (cf.
execution times are CPU times, i.e., only the elapsed periods          Subsection IV-E).
spent in the allocated CPUs. Furthermore, memory consump-                 One of the main issues in BMC is dealing with lengthy
tion is the amount of memory that belongs to the verification          loops. Our approach focuses on dealing with loops and pruning
process and is currently present in RAM (i.e., not swapped or          the unnecessary steps to conclude the verification. Loops cat-
otherwise not-resident). CPU time and memory consumption               egory has 14 subcategories categorized the same as SV-COMP
were measured with the benchexec tool [34] (commands
available on the supplementary page). We did not enable                 2 removed for double-blind review.




                                                                   7
TABLE I: Results for each subcategory. Each cell in the table shows two values. The top value represents the score, while the
bottom represents time in seconds.

                                       ESBMC               ESBMC           ESBMC                               CPA
                                                                                        CBMC       Veriabs             Verifuzz
          Subcategory / TScore
                         ime(s)   incremental-BMC     incremental-BMC     k-induction                        Checker
                                   with contractors          v6.9             v6.8       v5.43.0   v1.4.2      v2.1     v1.2.11
                                         159                 151              234           -66      729        77       109
                 Arrays
                                        272607             273123           224050       133708    17449     352273     274219
                                          24                  55               55           41       76         71        15
                BitVectors
                                        13876               14145            12924        8294      6077      9680      28691
                                          58                  55               64           67       128       113        40
               ControlFlow
                                        47384               46727            23883        30696    24763      13987     46734
                                         270                 268             1098          170      1312       930       429
                  ECA
                                        947500             949801           539341       989186    449183    687361     799332
                                         800                 802              779          782       827       749        -64
                  Floats
                                        48147               46768            36501        46743    44156      62876     368963
                                         256                 227              226          292       204       282        57
                  Heap
                                        55180               53887            45732        48786    40801      50371     161308
                                         669                 652              609          637      1044       696       209
                  Loops
                                        296102             294764           273893       236902    170916    292803     492657
                                         -595                -595             783          256       903       903       216
              ProductLines
                                        214485             214554            62777       128144    149945     80606     48716
                                          -64                 -64             109          100       125        92        43
                Recursive
                                        31790               31771            22736        18695    22073      23215     54177
                                         159                 159              158          158       152       153        55
                  XCSP
                                        14306               14334            13273        12087    19869      20442     59186
                                         174                 174              157            6        -         43         0
             AWS-C-Common
                                        32234               33479            19637        5279        -       81193      1999
                                           0                   0                2            0        -         2          0
                BusyBox
                                         2141                1812              10         7755        -       2555       206
                                          66                  66             2020         -3257       -       3114         0
          DeviceDriversLinux64
                                       2133570             2102103          802304      1697560       -      948362     328643
                                         1976                1950            6294          -814     5500      7225       1109
                  total
                                       4109322             4077268         2077061      3363835    945232    2625724   2664831



   With the current scores, we can confirm that we have                     In the loops category, we find our approach shows
   preserved the soundness (cf. Definition 1) and com-                      improvement of ESBMC performance by at least 2%
   pleteness (cf. Definition 2) of the BMC technique. The                   and achieves EG3.
   results show that the number of correct and incorrect
   results were maintained by a margin of 0.01%, thus
   achieving our EG2.

                                                                        the most critical objectives by saving CPU time, decreasing
                                                                        memory consumption and improving the scores. Additionally,
2022 as shown in Table II. In particular, in four of these sub-         we scored reasonably well in most categories, with 2 being
categories, our approach performed better than plain ESBMC.             the lead. However, this version of our approach does not
For example, we looked at the subcategory of loops; we got              apply to some benchmarks, so we see some differences in
remarkable results compared to plain ESBMC. The same ap-                scores. Also, we noticed our approach did not perform well in
plies to loop-new, loop-zilu, loops-crafted-1 and                       one particular benchmark and reported a false negative. The
nla-digbench-scaling. We also got better scores and                     benchmark is in bitvectors, which represents the overflow
time consumption results than the champion tool Veriabs. In             problem. Another issue with the implementation is that we do
particular, in the subcategory loop-simple, verifythis                  not apply the contractors when it comes to an unsupported
and nla-digbench-scaling.                                               operator. This is also a reason for the score not improving
   However, we scored lower in loop-acceleration be-                    in some subcategories. Moreover, the lack of accuracy in the
cause some benchmarks timed out, which cost us 3 scores. We             interval analysis option in ESBMC hindered the performance
also have some shortcomings in our approach: we do not deal             of the contractors. Because the intervals were not accurate and
with multiple lengthy loops in this version. That is why we got         the result of the contractor was not helpful to reduce the search
the same score in some subcategories. In general, we achieved           space. In the future, we will work to overcome this limitation.



                                                                   8
TABLE II: Results for loops category. Each cell in the table shows two values. The top value represents the score, while the
bottom represents time in seconds.

                                        ESBMC               ESBMC           ESBMC                                CPA
                                                                                           CBMC      Veriabs             Verifuzz
          Subcategory / TScore
                         ime(s)    incremental-BMC     incremental-BMC     k-induction                         Checker
                                    with contractors          v6.9             v6.8        v5.43.0    v1.4.2     v2.1    v1.2.11
                                           29                  25                1           52        85         78       28
                   loops
                                         18353               18544            13261         14172     5817      10579    32777
                                           26                  29               28           28        49         32       17
             loop-acceleration
                                         18568               15803            13734         5800      2967      16468    18698
                                            3                   3                8            1        11          5        0
                loop-crafted
                                          3846                3608            1723          1450       459       3306     5403
                                           11                  11               15            3        41         37        1
                loop-invgen
                                         18610               17661            15683         21295     8529      12144    25219
                                           15                  15               13           23        37         21        1
                  loop-lit
                                         12628               12645            11945         10011     4317      11150    18914
                                            8                   4               12           12        16         10        0
                 loop-new
                                          6309                8354            6285          3996      2835       6977     9906
                                           16                  16               28           16        32         36        0
           loop-industry-pattern
                                          9061                9061            2923          8137      2363       1826    16208
                                           -24                 -28             -17            3        96          9        8
              loops-crafted-1
                                         42493               40099            19040         27417     6344      42570    39663
                                            3                   3                3            1        17          7        1
              loop-invariants
                                          7124                7122            6950          6141       144       4914     7208
                                           13                  13               11            9        11          7        1
                loop-simple
                                          961                 920              903           605      1001       2419     6307
                                           20                  14               16           14        42         38        0
                 loop-zilu
                                         10932               13657            12650         13135     1194       4887    19812
                                            2                   2                2            2         0         -30       2
                 verifythis
                                          3631                3634            3618          2069      2392       1939     2883
                                            7                   7                8            5        23          5        4
               nla-digbench
                                         23947               23953            23617         21905     16700     25427    24412
                                          540                 538              481           468       584       441      146
            nla-digbench-scaling
                                        119639              119702           141561        100768    115853    148198    265249
                                          669                 652              609           637      1044       696      209
                   total
                                        296102              294764           273893        236902    170916    292803    492657



E. Threats to the validity
   As mentioned in Section III, we only apply the contractor
if the contracted area is at the end of the loop. For example,
given a variable x = X0 that is incremented inside a non-
deterministic loop x + + up to a max value of Xmax , if the
contractor result (e.g., X = [X0 , Xmax ]) was reduced from
the upper bound (i.e., X < Xn < Xmax , where X < Xn
is the contracted region) we can safely skip the instructions                            Fig. 14: Monotone vs non-monotone.
(iterations) that exceed the upper bound. However, suppose
the contracted area was at the beginning of the loop (i.e.,
the reduced interval from the lower bound). In that case, we
cannot guarantee the correctness of the verification results, as
the method cannot reason about the minimum quantity of loop              the other is not (here, y can increment and decrement at any
iterations. In the previous example, reducing from the lower             state). Dots represent states, and blank lines and grey areas
bound (i.e. X > Xn ∧ X < Xmax ) cannot be contracted as it               represent a property. Assume that we start from the origin
would skip instructions.                                                 point; the first program is safe to use an assume directive to
   Similarly, the program’s monotonicity for variables also              skip the states guaranteed to hold the property. However, that
affects the verification results. For example, given a variable y        is not the case with the second program, and we will end
that may be non-deterministically incremented or decremented             up in the same situation as mentioned before, where the area
cannot be contracted. Illustrated in Figure 14 are two pro-              reduced is at the beginning of the loop. Nevertheless, this time
grams; one is monotone (here, y would always increment), and             it is in the middle.



                                                                    9
TABLE III: Results per category with memory consumption.                  of run-time errors in C programs automatically. It uses an
Each cell shows the score at the top and the memory used in               accurate over-approximation of intervals for variables, whether
MB at the bottom. The decrease in memory usage is shown                   it is a floating-point or an abstract domain. It accounts for
as the percentage of how much less memory was used.                       rounding errors in both domains. The use of interval methods
                                                                          is what distinguishes our work from Astree.
                             ESBMC             ESBMC       memory            There is also PIPS [42] that was first introduced in 1988.
       Subcategory          incremental      incremental    saved         PIPS automatically detects medium- to large-grain parallelism
                          with contractors       v6.9                     in programs using techniques based on convex array regions.
         Arrays
                                159              151
                                                            78%
                                                                          The main drawback of PIPS is that it only supports FORTRAN
                              152018            682100                    and C [43]. Like PIPS, PAGAI [44] is also an automatic static
                                 24               55                      analysis tool that uses the program’s polyhedral abstraction.
        BitVectors                                          -10%
                               5877              5325                     Both tools have been used to infer program invariants [45].
                                 58               55                      APRON is another example of a library employed for static
       ControlFlow                                          -23%
                              129040            104705                    analysis of the program numerical variables using Abstract
                                270              268                      Interpretation [46]. Such analysis aims to infer (inductive)
          ECA                                               -2%
                              3662494          3595599
                                                                          invariants about those variables, such as −2 <= a − b <= c,
                                800              802
          Floats                                            59%           which should hold during any program execution.
                               74664            181319
                                                                             Veriabs [31], [47] is a tool that utilizes BMC, abstraction,
                                256              227
          Heap                                              -16%          and fuzzing to verify programs. Also, it employs a strategy
                               71968            62046
                                669              652
                                                                          selector that utilizes twelve different verification techniques.
          Loops                                             36%           The selector will choose a technique based on code-structural
                              177184            275648
                                -595             -595                     and variable-data properties. Veriabs is the champion of SV-
      ProductLines                                          4%            COMP 22 in Reach safety category. The runner-up in SV-
                              136344            141732
                                 -64              -64                     COMP 22 is CPA Checker [32] which is a tool that has
        Recursive                                           -9%           configurable program analysis (CPA) to continuously improve
                               76335            69961
                                159              159                      with new verification components. CPA Checker is mainly
          XCSP                                              58%
                               12773            30461                     built for researchers to conveniently implement new ideas and
                                174              174                      produce experimental results.
    AWS-C-Common                                            89%
                               68463            622038                       What differentiates our approach from existing methods is
        BusyBox
                                  0                0
                                                            96%
                                                                          the use of interval methods described in the interval analysis
                               2216             54352                     and methods field. All the studies motioned in our related work
                                 66               66                      utilize the interval analysis techniques as described in static
   DeviceDriversLinux64                                     83%
                              7045822         40824348                    analysis. While Interval Analysis and Methods described in
                               1976              1950                     Section II share the same formal definitions and arithmetic,
          total                                             75%
                             11615197         46649636                    they do not share the same methods, in particular contractors.
                                                                                       VII. Conclusions and future work
                        VI. Related Work                                     In Interval Analysis and Methods, contractors made using
   One of the most known software verification frameworks                 Interval Methods more practical in their applications by re-
for static analysis and verification for C/C++, and Java is               ducing the complexity of such methods. We advocate that
CBMC [30], [36]. CBMC is a bounded model checker that                     contractors should have a similar effect for interval analysis
has been developed and maintained for over 18 years. It                   applied to static analysis of programs. In this work, we
implements bit-precise BMC to verify C programs. CBMC is                  extended the application of contractors to prune the search
part of CProver, which has the component Goto-Analyzer [37].              space of BMC techniques; the experimental results show its
It is an abstract interpreter and takes the GOTO-program as               impact on open-source C benchmarks where the score was
an input. It supports three types of abstract domain: constant,           increased in some categories and reduced consumption of
variable sensitivity, and dependency domain. Goto-Analyzer                resources. In particular, interval methods via contractors made
strength lies where it can analyze the interval, where it is              the incremental BMC verification faster and reduced memory
guaranteed to hold and produce results as a success. Another              usage by various orders of magnitude. Once we compare
tool for static analysis is Frama-C [38], [39]. It is a framework         verification with and without the contractor, we can see a
that utilizes several plugins for static analysis of C code. One          difference in the score (32 more benchmarks successfully veri-
of these plugins is Evolved Value Analysis (EVA) [40], which              fied) and resource consumption (75% less memory consumed),
does the breakdown of each possible variable value and thus               especially when we prune the search space of programs that
gives the interval(s) for the variables. It can analyze intervals         contain loops. Furthermore, compared to state-of-the-art tools
accurately and produce a variable’s calculated minimum and                in BMC, it also performed well, where we achieved the lead in
maximum value. Another tool with successful applications in               2 subcategories. It preserved the soundness and completeness
the industry is Astree [41]. Astree is an abstract interpretation-        of the BMC technique by producing the same verification
based static program analyzer. It aims to prove the absence               outcome. However, the approach needs more development to



                                                                     10
cover more cases and improve scores further. Implementing                               [29] J. Little and E. Tsang, Foundations of Constraint Satisfaction. No. 5 in
support for more operators and better interval analysis is top on                            Computation in cognitive science, Academic Press, 1995.
                                                                                        [30] D. Kroening and M. Tautschnig, “Cbmc–c bounded model checker,” in
the list of improvements that would have the highest impact on                               International Conference on Tools and Algorithms for the Construction
verification results in terms of score and resource consumption.                             and Analysis of Systems, pp. 389–391, Springer, 2014.
                                                                                        [31] P. Darke, S. Agrawal, and R. Venkatesh, “Veriabs: A tool for scalable
                                References                                                   verification by abstraction (competition contribution),” in International
                                                                                             Conference on Tools and Algorithms for the Construction and Analysis
 [1] E. M. Clarke, W. Klieber, M. Nováček, and P. Zuliani, “Model checking                 of Systems, pp. 458–462, Springer, 2021.
     and the state explosion problem,” LASER Summer School, vol. 7682                   [32] D. Beyer and M. E. Keremoglu, “Cpachecker: A tool for configurable
     LNCS, no. 2005, pp. 1–30, 2012.                                                         software verification,” in International Conference on Computer Aided
 [2] E. M. Clarke and E. A. Emerson, “Design and Synthesis of Synchroniza-                   Verification, pp. 184–190, Springer, 2011.
     tion Skeletons Using Branching Time Temporal Logic,” in 25 Years of                [33] A. B. Chowdhury, R. K. Medicherla, and R. Venkatesh, “Verifuzz:
     Model Checking (O. Grumberg and H. Veith, eds.), pp. 196–215, 2008.                     Program aware fuzzing,” in International Conference on Tools and
 [3] J. P. Queille and J. Sifakis, “Specification and verification of concurrent             Algorithms for the Construction and Analysis of Systems, pp. 244–249,
     systems in CESAR,” in Lecture Notes in Computer Science (M. Dezani-                     2019.
     Ciancaglini and U. Montanari, eds.), vol. 137 LNCS, (Berlin, Heidel-               [34] D. Beyer, “Reliable and reproducible competition results with benchexec
     berg), pp. 337–351, Springer Berlin Heidelberg, 1982.                                   and witnesses (report on sv-comp 2016),” in International Conference
 [4] K. L. McMillan, “Symbolic Model Checking,” in Symbolic Model                            on Tools and Algorithms for the Construction and Analysis of Systems,
     Checking, pp. 25–60, 1993.                                                              pp. 887–904, Springer, 2016.
 [5] Bryant, “Graph-Based Algorithms for Boolean Function Manipulation,”                [35] D. Beyer, “Progress on software verification: Sv-comp 2022,” in Tools
     IEEE Transactions on Computers, vol. C-35, pp. 677–691, 8 1986.                         and Algorithms for the Construction and Analysis of Systems (D. Fis-
 [6] D. Peled, “All from one, one for all: on model checking using repre-                    man and G. Rosu, eds.), (Cham), pp. 375–402, Springer International
     sentatives,” in CAV, pp. 409–423, 1993.                                                 Publishing, 2022.
                                                                                        [36] E. Clarke, D. Kroening, and F. Lerda, “A tool for checking ANSI-C
 [7] E. Clarke, O. Grumberg, S. Jha, Y. Lu, and H. Veith, “Counterexample-
                                                                                             programs,” in Tools and Algorithms for the Construction and Analysis
     Guided Abstraction Refinement,” in CAV, pp. 154–169, 2000.
                                                                                             of Systems (TACAS 2004) (K. Jensen and A. Podelski, eds.), vol. 2988
 [8] A. Biere, A. Cimatti, E. Clarke, and Y. Zhu, “Symbolic model checking
                                                                                             of Lecture Notes in Computer Science, pp. 168–176, Springer, 2004.
     without BDDs,” in LNCS, vol. 1579, pp. 193–207, 1999.
                                                                                        [37] T. Yamaguchi, M. Brain, C. Ryder, Y. Imai, and Y. Kawamura, Ap-
 [9] A. Biere, A. Cimatti, E. M. Clarke, O. Strichman, and Y. Zhu, “Bounded
                                                                                             plication of abstract interpretation to the automotive electronic control
     Model Checking,” Adv. Comput, vol. 58, no. C, pp. 117–148, 2003.
                                                                                             system, vol. 11388 LNCS. Springer International Publishing, 2019.
[10] L. C. Cordeiro, SMT-based bounded model checking of multi-threaded
                                                                                        [38] P. Cuoq, F. Kirchner, N. Kosmatov, V. Prevosto, J. Signoles, and
     software in embedded systems. PhD thesis, University of Southampton,
                                                                                             B. Yakobowski, “Frama-c,” in International conference on software
     UK, 2011.
                                                                                             engineering and formal methods, pp. 233–247, Springer, 2012.
[11] A. Cimatti and A. Griggio, “Software model checking via ic3,” in                   [39] D. Beyer and M. Spiessl, “The static analyzer frama-c in sv-comp
     International Conference on Computer Aided Verification, pp. 277–293,                   (competition contribution),” in International Conference on Tools and
     Springer, 2012.                                                                         Algorithms for the Construction and Analysis of Systems, pp. 429–434,
[12] K. Hoder and N. Bjørner, “Generalized property directed reachability,”                  Springer, 2022.
     in International Conference on Theory and Applications of Satisfiability           [40] D. Bühler, P. Cuoq, B. Y. With, M. Lemerre, A. Maroneze, V. Perrelle,
     Testing, pp. 157–171, Springer, 2012.                                                   and V. Prevosto, “Eva - The Evolved Frama-C Value Analysis Plugin,”
[13] L. Jaulin, M. Kieffer, O. Didrit, and E. Walter, “Applied Interval                      2020.
     Analysis,” in Springer London, 2001.                                               [41] P. Cousot, R. Cousot, J. Feret, L. Mauborgne, A. Miné, D. Monniaux,
[14] P. Cousot and R. Cousot, “Abstract interpretation: a unified lattice model              and X. Rival, “The ASTREÉ Analyzer,” in Programming Languages
     for static analysis of programs by construction or approximation of                     and Systems (M. Sagiv, ed.), (Berlin, Heidelberg), pp. 21–30, Springer
     fixpoints,” in POPL, pp. 238–252, 1977.                                                 Berlin Heidelberg, 2005.
[15] G. Chabert, “ibex-lib.org.”                                                        [42] F. Irigoin, P. Jouvelot, and R. Triolet, “Semantical interprocedural
[16] M. Mustafa, A. Stancu, N. Delanoue, and E. Codres, “Guaranteed                          parallelization: An overview of the PIPS project,” in ACM ICS 25th
     SLAM—An interval approach,” Robotics and Autonomous Systems,                            Anniversary Volume, pp. 143–150, 1991.
     vol. 100, pp. 160–170, 2018.                                                       [43] F. Irigoin, P. Jouvelot, and R. Triolet, “Author Retrospective for Seman-
[17] Omitted for double-blind review, “Bounded model checking of software                    tical Interprocedural Parallelization: An Overview of the PIPS Project,”
     using interval methods via contractors,” CoRR, vol. abs/2012.11245,                     in ACM ICS 25th Anniversary Volume, p. 12–14, 2014.
     2020.                                                                              [44] J. Henry, D. Monniaux, and M. Moy, “Pagai: A path sensitive static
[18] X. Rival and K. Yi, Introduction to Static Analysis: An Abstract                        analyser,” ENTCS, vol. 289, pp. 15–25, 2012.
     Interpretation Perspective. MIT Press, 2020.                                       [45] W. Rocha, H. Rocha, H. Ismail, L. Cordeiro, and B. Fischer, “DepthK:
[19] S. S. Muchnick, Advanced Compiler Design Implementation. Morgan                         A k-induction verifier based on invariant inference for C programs,” in
     Kaufmann Publishers Inc., 1997.                                                         TACAS, vol. 10206 of LNCS, pp. 360–364, 2017.
[20] L. Cordeiro, B. Fischer, and J. Marques-Silva, “SMT-based bounded                  [46] B. Jeannet and A. Miné, “Apron: A library of numerical abstract domains
     model checking for embedded ANSI-C software,” IEEE Transactions                         for static analysis,” in Computer Aided Verification, 21st International
     on Software Engineering, vol. 38, no. 4, pp. 957–974, 2012.                             Conference, CAV 2009, Grenoble, France, June 26 - July 2, 2009.
[21] S. A. Kripke, “Semantical Analysis of Modal Logic I Normal Modal                        Proceedings, vol. 5643 of Lecture Notes in Computer Science, pp. 661–
     Propositional Calculi,” Mathematical Logic Quarterly, vol. 9, no. 5-6,                  667, 2009.
     pp. 67–96, 1963.                                                                   [47] M. Afzal, A. Asia, A. Chauhan, B. Chimdyalwar, P. Darke, A. Datar,
[22] M. R. Gadelha, F. R. Monteiro, J. Morse, L. C. Cordeiro, B. Fischer, and                S. Kumar, and R. Venkatesh, “Veriabs : Verification by abstraction and
     D. A. Nicole, “ESBMC 5.0: An industrial-strength C model checker,”                      test generation,” in 2019 34th IEEE/ACM International Conference on
     in ASE, pp. 888–891, ACM, 2018.                                                         Automated Software Engineering (ASE), pp. 1138–1141, 2019.
[23] M. A. Sainz, J. Armengol, R. Calm, P. Herrero, L. Jorba, and J. Vehi,
     Modal Interval Analysis, vol. 2091. Springer, 2014.
[24] M. M. A. Mustafa, Guaranteed SLAM—An interval approach. PhD
     thesis, Manchester University, 2017.
[25] L. Jaulin, M. Kieffer, O. Didrit, and E. Walter, “Interval Analysis,” in
     Applied Interval Analysis, ch. 2, pp. 11–43, Springer, London, 2001.
[26] E. Hansen and G. W. Walster, Global optimization using interval
     analysis: revised and expanded, vol. 264. CRC Press, 2003.
[27] A. Neumaier and A. Neumaier, Interval methods for systems of equa-
     tions, vol. 37. Cambridge university press, 1990.
[28] L. Granvilliers, “Revising hull and box consistency,” Logic Program-
     ming, pp. 230–244, 1999.




                                                                                   11
