                                         Agentic-IC3: Enabling Semantic Proof Search in
                                                      IC3 Model Checking

                                                   Yu-Wei Fan, SooHyuk Cho, Aarti Gupta, and Sharad Malik

                                                                       Princeton University
                                                           {yf9172,soohyuk.cho,sharad}@princeton.edu
                                                                    aartig@cs.princeton.edu
arXiv:2609.27162v1 [cs.LO] 22 Sep 2026




                                               Abstract. IC3 is a state-of-the-art algorithm for hardware model check-
                                               ing that proves safety properties by incrementally constructing an in-
                                               ductive invariant consisting of a set of lemmas. Its effectiveness depends
                                               on generalization heuristics that identify useful lemmas and guide proof
                                               search. However, many leading IC3 hardware model checkers operate on
                                               lowered, bit-level representations, where high-level design relationships
                                               are difficult to exploit for generalization. Those operating at a higher
                                               level remain limited in exploiting high-level design structure and seman-
                                               tics. We present Agentic-IC3, built on Pono’s word-level model-checking
                                               infrastructure, which integrates a language-model agent into IC3 to guide
                                               semantic proof search using register-transfer-level (RTL) design informa-
                                               tion. The framework exposes an agent-oriented interface to a persistent
                                               IC3 backend, allowing the agent to interact with an explicit, evolving
                                               proof state throughout verification. Across successive proof obligations,
                                               the agent relates intermediate proof states and solver feedback to the
                                               RTL and proposes high-level lemmas through both SAT and UNSAT
                                               generalization. Beyond generalization, the agent can introduce derived
                                               observation signals to express design relationships succinctly and obtain
                                               more informative feedback, and backtrack to revise proposals that lead
                                               to unproductive proof branches. The backend checks proposals before
                                               updating the proof state, preserving soundness and providing feedback
                                               for further reasoning. On a suite of 14 benchmarks spanning security
                                               information-flow verification and functional verification of communication
                                               protocols, processors, and functional units, Agentic-IC3 solves 10 cases
                                               within a one-hour timeout, including four unsolved by all three evaluated
                                               baselines: rIC3, Pono-IC3Bits, and A-IC3.


                                         1   Introduction
                                         Hardware model checking is a widely used approach to hardware formal veri-
                                         fication. Given a hardware design and a property, a model checker determines
                                         whether the property holds for all executions of the design. IC3 [1], also known
                                         as property-directed reachability (PDR) [4], is a state-of-the-art algorithm for
                                         checking safety properties, which require that an undesirable condition never
                                         occurs. It constructs an inductive invariant: a collection of facts, called lemmas,
                                         that holds initially, is preserved by each transition, and implies the property.
2       Y.-W. Fan et al.

   IC3 combines proof-search guidance with solver-based checks. Human-designed
heuristics determine how proof obligations are generalized and which candidate
lemmas the checker attempts to prove, while solvers check the validity of each
proof step. A central task is generalization: turning information about concrete
states into lemmas that cover broader sets of states and help construct the
proof [7,24,18,3]. Useful generalizations depend on the design behavior and the
property being checked. A rule useful in one application may provide little
guidance in another, making a general strategy difficult to develop.
    The design of generalization heuristics also depends on how the model checker
represents the hardware and its lemmas. Bit-level IC3 operates on individual
state bits, where word-level operations in the original design have been lowered
into Boolean logic. This restricted representation supports efficient generalization
through operations such as literal removal, backed by optimized SAT solvers and
compact data structures [4,6]. However, high-level relationships can be difficult to
identify in the lowered design, and expressing them may require multiple bit-level
lemmas. Word-level IC3 retains operations over multi-bit values, allowing lemmas
to express relationships such as equality or arithmetic constraints directly [5,21,26].
The richer representation offers more expressive lemmas, but searching the larger
space requires more resources, and heuristics may miss useful candidates.
   Developing effective generalization strategies therefore requires substantial
expert effort. Existing approaches encode useful proof patterns through heuristics,
synthesis grammars, and abstraction rules [6,5,26]. Other work extends the proof
vocabulary [11] or exploits application-specific structure [20]. Their effectiveness
depends on how well the generalization rules and candidate representations
capture relationships relevant to the target designs and properties, limiting how
well the guidance transfers across applications.
    ML-based approaches offer another way to obtain this guidance, drawing on
data and verification feedback. Within bit-level IC3, NeuroPDR and DeepIC3
use graph neural networks to guide inductive generalization [9,8], while A-IC3
learns to select among generalization strategies during verification [27]. Recent
work also uses language models to generate invariants from design information
and solver feedback. Large Lemma Miners and CIll propose helper invariants for
hardware verification and validate them with formal tools [14,17], while IC3Syn
uses language models for generalization in an IC3-based procedure for distributed
protocols [2]. These efforts motivate a broader role for language-model reasoning
within IC3: using evidence accumulated during proof search to propose lemmas
and revise the decisions that determine subsequent proof obligations.
    We present Agentic-IC3, a framework built on Pono’s word-level model-
checking infrastructure [12] that integrates a language-model agent into IC3 as
a proof-search policy. The interface deliberately keeps the agent’s view of both
the design and the proof state at the register-transfer level (RTL). The agent
examines the RTL, property, proof states, and solver feedback to identify signal
relationships that explain an obligation’s unreachability and express them as
lemmas.
       Agentic-IC3: Enabling Semantic Proof Search in IC3 Model Checking          3

    The backend maintains the ongoing proof state, including admitted lemmas
and proof obligations. Through an agent-oriented interface to a persistent backend
session, the agent uses this evolving context to guide successive generalization
steps. The interaction also supports decisions beyond lemma generation. The
agent can introduce derived observation signals to make useful relationships
easier to recognize and express, and backtrack to earlier proof obligations to
revise proposals that lead to unproductive branches. These actions let the agent
shape both the representation and direction of the continuing proof search. The
backend validates proof updates with SAT/SMT solvers, preserving soundness
and providing feedback for subsequent reasoning.
    We evaluate Agentic-IC3 on 14 benchmarks with applications spanning se-
curity information-flow and functional verification of communication protocols,
processors, and functional units. With a one-hour timeout per benchmark, Agentic-
IC3 solves 10 cases, including four unsolved by all three evaluated baselines:
rIC3 [19], Pono-IC3Bits [12], and A-IC3 [27]. These results demonstrate the
potential of combining model checking algorithms with agent-guided semantic
reasoning on challenging hardware verification tasks.


2    Background
We model a hardware design as a transition system with state variables X, an
initial-state predicate Init(X), and a transition relation T (X, X ′ ), where primed
variables denote the next state. A safety property P (X) requires that every
reachable state satisfy P ; a state satisfying ¬P is a bad state. An inductive
invariant Inv(X) proves the property when

                 Init ⇒ Inv,      Inv ∧ T ⇒ Inv′ ,        Inv ⇒ P.

    IC3 constructs Inv by maintaining a sequence of frames F0 , . . . , Fk . Each
frame Fi (X) is a formula over the state variables that overapproximates the
states reachable within i transitions, with F0 = Init. The nested ovals in Figure 1
illustrate the inclusion between frames, which satisfy
                                                    ′
                         Fi ⇒ Fi+1 ,      Fi ∧ T ⇒ Fi+1 .

IC3 refines these overapproximations by adding lemmas to the frames. A lemma
in Fi holds within the first i transitions but may not hold for arbitrarily many
transitions [1].
    After checking that the property holds initially, IC3 searches for a bad state
satisfying Fk ∧ ¬P . Blocking this state initiates a backward search over proof
obligations. An obligation (q, i) asks IC3 to prove that the states described by
the formula q(X) are unreachable within i transitions. Its predecessor query is

                          Fi−1 (X) ∧ T (X, X ′ ) ∧ q(X ′ ).

In the left panel of Figure 1, a SAT query finds a predecessor pk−1 of the bad
state in Fk−1 . SAT generalization expands pk−1 into a region qk−1 whose states
4       Y.-W. Fan et al.

                   SAT Generalization                                                UNSAT Generalization

                                                     𝐹!       ¬𝑃                                                       𝐹!
                                           𝐹!"#                                                             𝐹!"#            ¬𝑃
                             𝐹$                                                                      𝐹$
                   𝐹%                                                                      𝐹%              𝑞, 𝑘 − 1
                                           𝑞!"# , 𝑘 − 1
                                  𝑞$ , 𝑖

            Init            ?                                                                                         𝑝
                                                  𝑝!"#                              Init
                                     𝑝$
                                                                                                                      ¬ℓ




                   Proof obligation                   Concrete                                       Generalized PO
                                                                        Bad state
                         (PO)                     predecessor state                             (Negation of the Lemma ℓ)




Fig. 1. IC3 proof search and generalization. Left: backward predecessor search creates
proof obligations, with SAT generalization expanding concrete predecessors into regions.
The question mark denotes a pending predecessor query. Right: an UNSAT predecessor
query enables a blocking lemma ℓ that excludes the larger region ¬ℓ.


can reach the parent obligation, creating (qk−1 , k − 1). Repeating this process
produces earlier obligations, such as (qi , i) around pi . These obligations form a
backward search tree; the figure shows one branch, with arrows indicating forward
transitions. A branch reaching an initial state yields a counterexample [4].
    If the predecessor query is UNSAT and q excludes initial states, IC3 can
block (q, i). UNSAT generalization seeks a lemma ℓ satisfying q ⇒ ¬ℓ. The direct
blocking lemma is ¬q; a stronger lemma excludes additional states. To admit ℓ
at frame i, IC3 checks initiation and relative inductiveness:

                                           Init ⇒ ℓ,                  Fi−1 ∧ ℓ ∧ T ⇒ ℓ′ .

The checked lemma is added to F1 , . . . , Fi , strengthening their approximations
and blocking (q, i). The right panel of Figure 1 illustrates this step for (q, k − 1):
the orange region ¬ℓ contains q and is excluded by adding ℓ to Fk−1 . Once all bad
states have been blocked from the frontier, IC3 extends the frame sequence. If
two adjacent frames Fi and Fi+1 become equivalent, Fi is an inductive invariant
proving the property [1].
    The representation of proof obligations and lemmas determines the available
generalizations. In bit-level IC3, an obligation is typically a cube, a conjunction
of Boolean literals, and a blocking lemma is a clause, a disjunction of literals.
Removing literals enlarges the region described by a cube: SAT generalization
obtains a broader predecessor region, while UNSAT generalization obtains a
stronger blocking lemma by negating the enlarged region [4].
    Word-level IC3 can express lemmas over multi-bit values using predicates
such as equality and arithmetic comparisons [26]. For example, equality between
two n-bit registers u and v is expressed by the single word-level lemma u = v.
Its bit-level representation consists of the following 2n clauses:

                   (¬u[j] ∨ v[j])                         and          (u[j] ∨ ¬v[j]),              0 ≤ j < n.
         Agentic-IC3: Enabling Semantic Proof Search in IC3 Model Checking           5

3     Motivating Example

Figure 2 compares generalization in Pono-IC3Bits1 with RTL-guided agent
generalization on an information-flow verification example. Two copies of a
controller share input a and reset, while their b operands may differ when a is
zero and must otherwise agree. The assertion requires both copies to produce
identical finish signals, checking that the permitted differences in b do not
affect completion timing.


module controller (
  input wire clk, rst,
  input wire [7:0] a, b,
  output reg finish
);
  localparam IDLE=2’d0, WORK=2’d2, DONE=2’d3;
  reg [1:0] state;
  reg [7:0] count;
  always @(posedge clk)
    if (rst) begin
      state <= IDLE; count <= 0; finish <= 0;
    end else case (state)
      IDLE: begin
        count <= (a == 0) ? 8’d0 : b;
        state <= WORK;
      end
      WORK: if (count == 0) state <= DONE;
            else count <= count - 1’b1;
      DONE: finish <= 1;
    endcase
endmodule

module duv (
  input wire clk, rst,
  input wire [7:0] a, b1, b2
);
  wire finish1, finish2;
  controller copy1 (clk, rst, a, b1, finish1);
  controller copy2 (clk, rst, a, b2, finish2);
  assume property (a == 0 || b1 == b2);
  assert property (finish1 == finish2);
endmodule

Fig. 2. Two-copy information-flow security verification written in Verilog. Both copies
start from the reset state. a and reset are shared, while b1 and b2 are constrained by
the assumption.
1
    Pono-IC3Bits denotes the IC3Bits engine in the Pono model checker [12], used here
    as a conventional IC3 reference.
6       Y.-W. Fan et al.

   Write sj and fj for the state and finish signals of copy j ∈ {1, 2}. Searching
backward from unequal finish signals, IC3 obtains the predecessor region

                q = ¬f1 ∧ (s1 = DONE) ∧ ¬f2 ∧ (s2 = WORK).

With reset deasserted, the next transition sets f1 and leaves f2 low, reaching a
bad state. The predecessor query against F0 = Init is UNSAT, showing that q
can be blocked at frame 1.
    Pono-IC3Bits greedily removes literals while preserving the blocking condi-
tions [4]. Generalizing q to s1 [0] = 1 yields the blocking lemma

                                ℓlocal ≡ (s1 [0] = 0).

After one transition from initialization, the controller can only be in IDLE or WORK.
The lemma therefore excludes DONE at frame 1, but DONE becomes reachable in
later frames.
    Given the RTL and q, the agent instead proposes

                                 ℓsync ≡ (s1 = s2 ).

The design and input assumption explain this relationship: both counters load zero
when a is zero and otherwise load equal b operands. Their identical updates keep
the controllers synchronized. The lemma excludes q and captures a relationship
across execution phases that contributes to the inductive invariant proving equal
completion timing.


4     Agentic-IC3 Framework

Agentic-IC3 builds on the separation between proof-search guidance and solver-
checked proof steps described in Section 1. The agent uses the RTL and evidence
from the ongoing search to propose and revise lemmas. In Figure 3, the IC3 proof
kernel comprises a search controller, an evolving proof state, and SAT/SMT
checks. The controller executes IC3 and requests agent guidance at SAT and
UNSAT generalization steps. In response, the agent can Propose lemmas for
generalization, Observe derived expressions whose values augment subsequent
feedback, or Backtrack to an earlier proof obligation to revise a proposal.
We next describe the interface, the motivation for each action, and its backend
support.


4.1   Design and Agent Interface

RTL proof representation. Agentic-IC3 uses Pono’s word-level model-checking
infrastructure [12] to allow lemmas to directly express relationships inferred from
the RTL, such as equality between counters or bounds on arithmetic expressions.
The agent reads the RTL, property, and assumptions, and receives the current-
state variables and their bit widths. The interface presents proof obligations,
       Agentic-IC3: Enabling Semantic Proof Search in IC3 Model Checking                                      7

                                                  RTL design
                       Encode                     + safety property      Read



                                          Agent-oriented interface
            IC3 Proof Kernel                                              Language-model agent

              IC3 search controller            Proof request
              Predecessor search
              Frame refinement               Goal, frame lemmas,
                                             and batched formulas
              Evolving proof state                                              Choose one action
              Frames · lemmas · goals
                                                                                 PROPOSE
              Observation vocabulary
                                                                                 SAT / UNSAT generalization
                                             Action response
                                                                                 OBSERVE
              SAT / SMT checks                                                   Derived state expressions
                                        Lemma proposals, observations,
              Validate proof updates
                                           or a backtrack request                BACKTRACK
                                                                                 Revise a prior proposal



Fig. 3. Agentic-IC3 architecture. The kernel sends proof requests to the agent, which
uses the RTL and accumulated context to Propose, Observe, or Backtrack. The
kernel checks proof updates.


frame lemmas, and solver feedback using RTL signal names and expressions. The
agent proposes lemmas using a subset of Verilog expressions, including arithmetic,
comparisons, bitwise operations, and concatenation. A Verilog-expression frontend
parses and type-checks these proposals and compiles them into quantifier-free
bit-vector SMT formulas used by the kernel.

Persistent proof session. The kernel maintains a persistent proof session in
which frames, admitted lemmas, proof obligations, and registered observations
remain available across requests. Agent actions advance or revise this proof state,
while the agent uses accumulated interaction context to reason across successive
obligations. A long-lived CLI process retains the solver context and exchanges
requests and responses through JSON Lines.
    Each proof request identifies the obligation and its frame level i, and supplies
the active lemmas of Fi−1 . Depending on the generalization task, the request also
contains a batch of predecessor regions or checked blocking lemmas. The backend
collects these lemmas before adding them to the frames, allowing the agent to
combine low-level facts into more informative design relationships through batch
generalization. Each agent response selects one action: Propose, Observe, or
Backtrack.


4.2   Batch Generalization

Conventional IC3 performs generalization on an individual predecessor state or
proof obligation. Directly replacing these generalization steps with agent calls
gives the agent only one example at a time. The agent may then propose a lemma
based on particular register values in that example, without identifying the design
relationships that explain other similar states. IC3Syn addresses this difficulty
8      Y.-W. Fan et al.

Algorithm 1 SAT batch generalization
Input: Proof obligation (q, i), i > 0.
 1: E ← Fi−1 ∧ T ∧ q ′ ; B ← ∅
 2: while |B| < b and SAT(E) do
 3:    p ← predecessor satisfying E
 4:    G ← Generalize(p)
 5:    B ← B ∪ {(p, G)}
 6:    E ← E ∧ ¬G
 7: if B = ∅ then
 8:    return to UNSAT generalization
 9: r ← SAT request for (q, i) with B and active frame lemmas
             . , ℓm ) ← RequestGeneralization(r)
10: (ℓ1 , . .V
               m
11: L ← j=1 ℓj
12: if UNSAT(Fi−1 ∧ T ∧ q ′ ∧ ¬L) then
13:    Report that no predecessor is excluded
14:    return for revision
15: for each ℓj in proposal order do
16:    Check ℓj with BMC to depth i − 1
17:    if a reachable violation is found then
18:        return counterexample as proposal feedback
19:    else
20:        Recursively block (¬ℓj , i − 1)
21:    if UNSAT(Fi−1 ∧ T ∧ q ′ ) then
22:        return to UNSAT generalization
23: Continue with remaining predecessors



by presenting multiple states together for generalization [2]. Following this idea,
Agentic-IC3 provides batches at both SAT and UNSAT generalization steps. SAT
batches contain predecessor states and their generalized regions, while UNSAT
batches contain blocking lemmas obtained during IC3 search. The agent examines
each batch together with the RTL, frame lemmas, and previous interactions.
    We use b for the maximum batch size and mmax for the maximum number of
lemmas per proposal. A proposal contains ℓ1 , . . . , ℓm , where 1 ≤ m ≤ mmax .
    We first describe SAT and UNSAT batch generalization for responses con-
taining lemma proposals. Both algorithms use RequestGeneralization to
query the agent with a proof request r containing the current batch and proof
context. The following subsections extend this interaction with observation and
backtracking actions.
SAT generalization. For a proof obligation (q, i), IC3 must exclude its pre-
decessors from Fi−1 before it can block q at frame i. Algorithm 1 first collects
up to b predecessors satisfying Fi−1 ∧ T ∧ q ′ . Each predecessor p is expanded
into a region G using conventional SAT generalization [4]. The next enumeration
query excludes G, so subsequent predecessors represent states outside the regions
already collected (line 6). This avoids collecting states already covered by the
same conventional generalization.
        Agentic-IC3: Enabling Semantic Proof Search in IC3 Model Checking             9

Algorithm 2 UNSAT batch generalization
Input: Pending batch B at frame i.
 1: Add newly checked lemmas to B
 2: if |B| < b and collection can continue then
 3:    return to IC3 search
 4: while B ̸= ∅ do
 5:    r ← UNSAT request at frame i with B and active frame lemmas
 6:    (ℓ1 , . . . , ℓm ) ← RequestGeneralization(r)
 7:    for each ℓj in proposal order do
 8:      C ← {B ∈ B | ℓj ⇒ B}
 9:      Check Init ⇒ ℓj
10:       Check Fi−1 ∧ ℓj ∧ T ⇒ ℓ′j
11:       if both checks pass then
12:            Add ℓj to F1 , . . . , Fi
13:            B ←B\C
14:       else
15:            return counterexample as proposal feedback



    The agent uses this batch to propose lemmas ℓ1 , . . . , ℓm for Fi−1 . Each proposal
ℓj expresses a relationship expected to hold within the first i − 1 transitions; its
negation ¬ℓj describes the states to exclude. Different predecessors may require
different lemmas to explain their unreachability. We allow proposals to exclude
only some predecessors, so the agent need not identify every relationship in one
response. The backend     checks whether any predecessor violates the proposed
conjunction L = j ℓj by testing the satisfiability of Fi−1 ∧ T ∧ q ′ ∧ ¬L (line 12).
                  V
If this formula is UNSAT, none of the predecessors would be removed, and the
agent is asked to revise its proposals.
    Conventional SAT generalization requires every state in the generalized
predecessor region to reach q in one transition [4]. Agentic-IC3 relaxes this
requirement, allowing the agent to propose a lemma ℓj whose negation also
includes states that do not lead directly to q. This allows a relationship inferred
from the RTL to exclude more unreachable states than the current predecessor
query identifies. However, the proposed relationship may be too strong and
exclude reachable states as well. Before starting recursive blocking, the backend
therefore uses bounded model checking (BMC) to check whether an execution
from Init, following the original transition relation T , can violate ℓj within i − 1
transitions (line 16). A violating execution is returned to the agent for revision,
avoiding further backward search for a proposal that cannot hold at its target
frame.
    If the BMC check is UNSAT, the proposal holds within the checked bound.
The backend then recursively blocks (¬ℓj , i − 1) to refine the frames through IC3’s
initiation and relative-inductiveness checks (line 20). After these refinements, it
repeats the predecessor query for (q, i). Remaining predecessors lead to further
generalization requests; once the query becomes UNSAT, IC3 proceeds to UNSAT
generalization to block q.
10      Y.-W. Fan et al.

UNSAT generalization. Conventional IC3 blocks an obligation by deriving a
lemma and adding it to the frames. Several such lemmas may express separate
constraints that can be generalized into a simpler or stronger design relationship.
To allow the agent to consider these constraints together, Agentic-IC3 collects
checked blocking lemmas in a batch B before adding them to the frames. These
lemmas may result from blocking individual obligations or from recursively
proving lemmas proposed during SAT generalization.
    Algorithm 2 requests agent generalization when b lemmas have accumulated,
or earlier when the collected lemmas are needed to continue the current search.
The agent examines the batch and the RTL to propose lemmas that replace one
or more of the collected constraints. A proposal ℓ can replace a batch lemma
Bj when ℓ ⇒ Bj . Thus, ¬ℓ contains ¬Bj : the proposal blocks at least the states
excluded by Bj .
    The backend checks initiation, Init ⇒ ℓ, and relative inductiveness, Fi−1 ∧
ℓ ∧ T ⇒ ℓ′ . If both checks pass, it adds ℓ to F1 , . . . , Fi and removes the batch
lemmas implied by ℓ (lines 12–13). Otherwise, it returns the counterexample
from the failed check for revision. Generalization continues for the remaining
batch lemmas until each is covered by an admitted lemma.


4.3   Derived Observation Vocabulary

Batch generalization allows the agent to compare several states, but useful
relationships may not be apparent from individual register values. Identifying
these relationships requires the agent to reason about combinations of signals and
compare the resulting values across states. This requires additional reasoning, and
useful relationships may be overlooked. To provide more informative feedback,
Agentic-IC3 allows the agent to introduce named observations whose values are
included in subsequent proof requests.
    Consider the two four-bit counters cnt1 and cnt2 and the control signal
active in Table 1. Neither counter has a fixed value when active is asserted.
Their sum, however, is 8 in each of these states. The agent can introduce an
observation obs.total = cnt1 + cnt2, adding the last column to the request.
This makes the conditional relationship directly visible: obs.total is 8 when
active is asserted and varies in the other displayed states. The agent can then
propose active ⇒ obs.total == 4’d8 for generalization.
    In RequestGeneralization(r), the agent may respond to the proof request
r with Observe(e) instead of a lemma proposal. The backend checks the expres-
sion e and registers its name, definition, and bit width. It then augments r with
the observation values and queries the agent again. The agent may introduce
further observations before returning lemmas. Registered observations remain
available throughout the session and are evaluated on states returned in later
requests and counterexamples. The agent can thus compare the same derived
value across successive proof obligations and reuse the observation name to
simplify lemma expressions.
       Agentic-IC3: Enabling Semantic Proof Search in IC3 Model Checking           11

Table 1. A derived observation makes a conditional relationship between two counters
explicit.

                         active   cnt1    cnt2    obs.total
                           1        1       7         8
                           1        5       3         8
                           1        6       2         8
                           0        2       3          5
                           0        4       7         11



4.4   Backtracking and Proof Revision

UNSAT generalization adds a proposed lemma to the frames once it passes the
initiation and relative-inductiveness checks. SAT generalization instead creates
a proof obligation that the backend tries to block recursively. The choice of a
SAT proposal therefore determines which obligations the subsequent search must
prove. Even if the proposal holds within the current frame bound, proving it
through recursive blocking may require many intermediate obligations.
    IC3 gains efficiency from local SAT/SMT queries involving only one transition,
without unrolling the transition relation [1]. However, the resulting feedback
describes only the current proof step, making it difficult for the agent to anticipate
the recursive obligations needed to establish a proposed lemma. As backward
search continues, the agent can relate successive predecessor states and learned
lemmas to the RTL and develop a better understanding of the design behavior.
It may then recognize that an earlier proposal describes only a local fact or that
another relationship offers a more effective direction for the proof. Agentic-IC3
therefore allows the agent to backtrack and replace the earlier proposal before
completing its proof attempt.
    For a proposal ℓ made while blocking (q, i), Algorithm 1 recursively attempts
to block (¬ℓ, i − 1) (line 20). When RequestGeneralization(r) is invoked for
SAT generalization of this obligation, the agent may return Backtrack instead
of lemmas. This response ends the recursive attempt to prove ℓ and returns
control to the generalization step for (q, i), skipping the remaining lemmas from
the same proposal response. The backend repeats the query Fi−1 ∧ T ∧ q ′ using
the retained frame lemmas (line 21). If predecessors remain, it collects a new
batch and calls RequestGeneralization with an updated request for (q, i).
Admitted lemmas remain in their validated frames and can prune subsequent
search, since each has passed its own proof checks independently of the abandoned
proposal.


5     Evaluation

We compare agent-guided proof search with conventional and ML-assisted IC3
for hardware verification.
12      Y.-W. Fan et al.

    We implement Agentic-IC3 in Python using Pono’s word-level model-checking
infrastructure [12]. Yosys translates the RTL into a word-level transition system
in BTOR2 format [25], and Bitwuzla handles the backend SMT queries [13]. We
use Codex CLI version 0.153.0 as the agent framework, with GPT-5.6-Sol and
medium reasoning effort. The full Agentic-IC3 configuration uses a maximum
batch size of b = 5 for both SAT and UNSAT generalization and allows at most
mmax = 5 lemmas per proposal.
    Our evaluation comprises 14 benchmarks spanning security information-flow
verification and functional verification of communication protocols, processors,
and functional units. The suite includes cache and arithmetic-unit information-
flow checks adapted from SecIC3 [20]; FIFO, arithmetic-loop, and arbitration
benchmarks from the hard benchmark set of Large Lemma Miners [14]; and
processor-verification benchmarks for NERV, PicoRV32, and SERV from CIll [17].
We also include a buffer-overflow check for the BSG communication protocol,
adapted from the ILA models used by Lu et al. [10]. We primarily select cases
that are difficult for conventional IC3 engines, while retaining a small number of
easier cases to assess the overhead of agent-guided verification.
    Each run starts with a fresh agent conversation and persistent IC3 session.
The full-system runs use the same task prompt and interface documentation
across benchmarks. The agent has read-only access to the RTL, documentation,
and proof history, and writable space for temporary files. It interacts with the
kernel through the shell; backend source code and internal state files remain
outside the sandbox. Shell network access and web search are disabled.
    We compare Agentic-IC3 with Pono-IC3Bits [12], rIC3 [19], and A-IC3 [27].
Pono-IC3Bits provides a conventional IC3 baseline using the same model-checking
infrastructure. rIC3 provides a state-of-the-art bit-level IC3 baseline, while A-IC3
provides an ML-assisted baseline that adaptively selects generalization strategies.
All experiments run on AMD EPYC 7532 processors, with one CPU core and
16 GiB of memory allocated per run and a verification timeout of 3,600 seconds.
We report wall-clock runtimes and additionally distinguish the time spent awaiting
agent responses from work performed by the Agentic-IC3 backend.

5.1   Comparison with IC3 Baselines
Table 2 summarizes the verification results. Agentic-IC3 solves 10 of the 14 bench-
marks within one hour, whereas Pono-IC3Bits times out on all 14. Agentic-IC3
thus solves additional cases using the same model-checking infrastructure. Against
the other baselines, rIC3 and A-IC3 each solve five cases. Agentic-IC3 solves every
case solved by either baseline and four additional cases: lrg_arb_lrg_16_ebmc,
fp_divider, nerv_causal, and picorv32_pc_bwd.
    Agentic-IC3 also improves runtime on cache, fifo_vis, and fp_adder com-
pared with both baselines. Agent interaction introduces overhead, however: on
multiplier, rIC3 and A-IC3 finish in approximately three seconds, compared
with 21.23 seconds for Agentic-IC3. Across the ten completed runs, time spent
awaiting agent responses accounts for 87% of the aggregate runtime. This sug-
gests that reducing agent-response latency could substantially improve end-to-end
       Agentic-IC3: Enabling Semantic Proof Search in IC3 Model Checking           13

Table 2. End-to-end runtimes in seconds. Agent measures time awaiting agent responses;
Backend measures verification work. The remainder is framework and orchestration
overhead. TO: one-hour timeout; OOM: out of memory.

                                                                Agentic-IC3
Test case                Pono-IC3Bits      rIC3 A-IC3
                                                           Total Agent Backend
bsg_link                             TO    TO      407.25 360.57   341.00       2.66
cache                                TO 199.17     135.70 82.40     62.74       5.33
fifo_vis                             TO 239.80     274.79 138.35   125.51       2.30
gulwani_fig1a_2_ebmc                 TO 51.43         TO 175.73    129.49      33.90
lrg_arb_lrg_16_ebmc                  TO    TO         TO 55.47      37.64       8.73
multiplier                           TO   2.93       3.14 21.23     13.17       0.22
fp_adder                             TO 530.81     209.53 153.22   136.54       5.89
fp_divider                           TO    TO         TO 512.71    463.79      38.61
nerv_causal                          TO    TO       OOM 162.34     142.83       9.86
picorv32_insn_mul                    TO    TO         TO     TO         –          –
picorv32_insn_sub                    TO    TO         TO     TO         –          –
picorv32_pc_bwd                      TO    TO         TO 42.10      32.90       1.11
picorv32_reg                         TO    TO         TO     TO         –          –
serv_insn_add                        TO    TO         TO     TO         –          –
Solved                              0/14   5/14     5/14            10/14


performance. One potential direction is to fine-tune smaller models on recorded
IC3 proof traces, aiming to retain effective generalization and action selection
with faster inference.

5.2   Ablation Study of Individual Mechanisms
We evaluate the contribution of batch generalization, observations, and back-
tracking by disabling each mechanism separately on the ten benchmarks solved
by the full system with all mechanisms enabled. Without batching, each SAT
or UNSAT request contains one item, and the agent is asked to propose one
lemma per response. The other two configurations disable the corresponding
action, with the interface documentation adjusted accordingly. Table 3 reports the
outcome and runtime of each run, together with the numbers of generalizations,
backtracks, and registered observations. We examine both proof completion and
generalization counts, since the reasoning required for individual agent responses
varies and runtime alone does not describe the resulting search.

Batch generalization. The full system requires fewer generalizations than the
no-batching configuration on all ten benchmarks. The total decreases from 515
to 137, a reduction of 73%, with the largest reductions on fifo_vis (173 to
7) and cache (22 to 2). Batching lets the agent generalize several predecessors
or blocking lemmas together, reducing the number of generalization calls. Both
configurations solve all ten benchmarks, and batching also reduces runtime on
nine, with speedups of 3.3× on fp_divider and 2.6× on fp_adder.
14          Y.-W. Fan et al.

Table 3. Ablation results on the ten benchmarks solved by the full system. Gen. counts
lemma-proposal responses; BT. counts backtracks; Obs. counts registered observation
definitions. Time is end-to-end wall time in seconds.

                              Full                  No batching          No observations        No backtracking
Test case
                       Gen. BT. Obs.   Time Gen. BT. Obs.         Time Gen. BT. Obs.    Time Gen. BT. Obs.    Time
bsg_link                16    0    6 360.57    28     4    7 384.04      10   0      0 214.41   15   0    7 323.58
cache                    2    0    6 82.40     22     0   13 165.42       4   0      0 67.66    16   0    0 168.17
fifo_vis                 7    0   33 138.35   173     0   18 445.94      14   0      0 132.22   46   0   97 543.00
gulwani_fig1a_2_ebmc     7    0    2 175.73    37     0    1 302.38      41   0      0    TO    10   0    2 358.79
lrg_arb_lrg_16_ebmc      5    0    0 55.47     12     0    0   91.81      6   0      0 67.43     8   0    0   60.01
multiplier               2    0    0 21.23      4     0    0   30.43      4   0      0 47.48     2   0    0   26.00
fp_adder                23    1    0 153.22    79     1    2 397.62      42   0      0 255.46   67   0    0 356.16
fp_divider              62    0    0 512.71   141     1    0 1691.69    109   3      0 710.27   78   0    6 440.06
nerv_causal             11    1    0 162.34    16     1    0 149.61      20   4      0 321.98   43   0    0 1704.11
picorv32_pc_bwd          2    0    0 42.10      3     0    1   46.83      2   0      0 33.32     4   0    0   53.17
Solved                        10/10                   10/10                   9/10                   10/10




Observations. The full system solves one more benchmark than the configuration
without observations. On gulwani_fig1a_2_ebmc, it completes the proof in
175.73 seconds using two observations and seven generalizations, whereas the
no-observations run makes 41 generalizations and times out. On cache and
fifo_vis, the full system also requires half as many generalizations: two rather
than four, and seven rather than fourteen, respectively. On fifo_vis, observations
reduce the number of generalizations even though the two runs take similar time.
The trajectory in Section 5.3 shows how an occupancy observation helps relate
two different FIFO representations. The run without observations is faster on
bsg_link, but this difference may reflect variation between runs; repeated runs
are needed to determine whether it is consistent.

Backtracking. The full-system runs for fp_adder and nerv_causal each back-
track once. Compared with the runs without backtracking, their generalization
counts decrease from 67 to 23 and from 43 to 11, with runtime speedups of 2.3×
and 10.5×, respectively. Although both configurations solve all ten benchmarks,
these cases show substantial differences in the amount of generalization needed
to complete the proof. The adder trajectory in Section 5.3 explains the role of
backtracking: recursive feedback reveals that an earlier proposal requires operand
relationships before the corresponding registers are updated. Backtracking lets
the agent replace that proposal with relationships restricted to the relevant
control states, while retaining previously admitted lemmas.


5.3      Proof-Search Trajectory Analysis

We examine recorded proof-search trajectories to show how the agent uses design
information and solver feedback to propose lemmas, introduce observations,
and revise earlier proposals. We also examine difficulties encountered in both
completed and timed-out runs.


Agent Decisions
        Agentic-IC3: Enabling Semantic Proof Search in IC3 Model Checking            15

Generalization from design semantics. The multiplier benchmark checks
whether two multiplier instances produce their completion signals simultaneously
under an input constraint. For instance j ∈ {1, 2}, let aj and bj denote its stored
operands and busy j its busy flag. Each instance asserts its completion signal on
the next cycle when it is busy on the current cycle and either stored operand is
zero. The initial predecessor batch contains states in which the instances disagree
on these conditions. The agent proposes three relationships:

              a1 = a2 ,      (a1 = 0) ∨ (b1 = b2 ),     busy 1 = busy 2 .

These relationships capture the completion logic: when the shared operand is zero,
the other operands need not agree; otherwise, their equality ensures that both
instances detect zero simultaneously. The backend admits these three relationships
and completes the proof.

Observations connecting different representations. The fifo_vis benchmark
compares a shift-register FIFO (sr) with a ring-buffer FIFO (rb), each containing
sixteen entries. In the shift-register FIFO, the tail index (sr.tail) identifies the
oldest entry, and the empty flag (sr.empty) indicates whether any entries are
present. When nonempty, this FIFO contains sr.tail + 1 entries. The ring-buffer
pointers rb.head and rb.tail identify the next insertion location and oldest
entry, respectively.
    The agent introduces the four-bit observation obs.occupancy = rb.head −
rb.tail, representing ring-buffer occupancy modulo 16. Subsequent feedback
includes this value alongside the original state variables. For example, one prede-
cessor has rb.head = 5 and rb.tail = 4, giving obs.occupancy = 1, while the
nonempty shift-register FIFO has sr.tail = 7, representing eight entries. A pop
therefore exposes inconsistent empty flags.
    The agent proposes a lemma relating the occupancy representations: its
nonempty case requires obs.occupancy = sr.tail + 1, with separate conditions
for initialization and the empty case. All arithmetic in these expressions is four-bit
arithmetic modulo 16; the empty flags distinguish an empty FIFO from a full
FIFO. The backend admits the lemma expressed using this observation.

Backtracking after requiring equality too early. The fp_adder benchmark checks
whether two adder instances assert their completion signals together. For instance
j ∈ {1, 2}, let sj , aj , and bj denote the RTL registers state, a, and b, respectively.
Each instance loads its operands in separate cycles, then decodes them. The
following simplified RTL shows the relevant clocked updates; take_a and take_b
abbreviate the input handshakes, and unrelated assignments are omitted.
    On entering state 1, aj has been updated but bj still holds its old value. The
new bj is available in state 2, and its decoded exponent, mantissa, and sign (b_e,
b_m, b_s) are available in state 3.
    While proving s1 = s2 , the agent initially requires b1 = b2 and equality of
the corresponding decoded fields whenever a1 ̸= 0. The backend admits this
relationship at an early frame. When the agent later tries to establish it at a
16      Y.-W. Fan et al.

case (state)
  0: if (take_a) begin a <= input_a; state <= 1; end
  1: if (take_b) begin b <= input_b; state <= 2; end
  2: begin
       b_e <= b[30:23] - 127; // also update b_m, b_s
       state <= 3;
     end
endcase


              Fig. 4. Code snippet for the fp_adder state transitions.


higher frame, recursive search returns a transition from state 0 to state 1 that
loads a nonzero a1 while leaving unequal b1 and b2 and their decoded fields
unchanged. The proposal therefore requires equality before those registers have
been updated.
   The agent backtracks to the proof of s1 = s2 and replaces the proposal with
two lemmas. The first requires b1 = b2 when s1 ≥ 2 and a1 =      ̸ 0. The second
requires equality of the decoded fields when 3 ≤ s1 ≤ 10 and a1 ̸= 0. The backend
admits the revised lemmas, and the subsequent search completes the proof.

Limitations and Extensions

Quantified lemmas to reduce enumeration. Relationships that hold uniformly
across indexed state components can require many explicit cases in the current
lemma language. Allowing quantified lemmas could let the agent express such
relationships over all relevant indices in a single formula. The fifo_vis trajectory
illustrates this opportunity: one admitted lemma uses sixteen disjuncts to relate
a shift-register word to the corresponding ring-buffer word under each possible
circular address offset, and similar lemmas cover other words. Symbolic array
indexing could remove the explicit address cases, while universal quantification
could express the correspondence across all valid entries. Together, these exten-
sions could make proposals more concise and reduce repeated reasoning about
individual indices. They would also require backend support for checking the
richer formulas; a more compact representation does not by itself guarantee faster
verification.

Stateful observations to capture temporal relationships. Some useful proof relation-
ships connect values from different execution stages, while the current observation
mechanism only defines expressions over the existing state. Extending obser-
vations with persistent state could retain selected past values or summarize
execution history, making these relationships available to lemma generation. The
timed-out picorv32_insn_sub trajectory illustrates this limitation: proposals
repeatedly confuse values belonging to different instructions or assume that a
result has reached the retirement record before the corresponding update. A
stateful observation, such as a shadow register or history monitor, could retain
       Agentic-IC3: Enabling Semantic Proof Search in IC3 Model Checking        17

an instruction’s operands and destination through retirement, providing a stable
reference for expressing the intended correspondence. Such an extension would
require explicit initialization and update rules, with auxiliary state that records
execution history without restricting the original design’s behaviors. The backend
would then check proposed lemmas over the augmented transition system.


6   Discussion

Combining established forms of proof guidance. Agentic-IC3 draws on established
ideas in model checking, including synthesis-based lemma generation [26], ex-
tensions to the proof vocabulary [11], and global guidance based on previously
learned lemmas [22]. Applying these ideas effectively requires deciding which
relationships to express, what evidence to examine, and when to revise the search.
Agentic-IC3 provides a common interface through which a language-model agent
can combine these forms of guidance according to the evolving proof context.
The backend maintains the algorithm’s proof conditions, while the agent selects
and applies the available actions. This suggests a research direction centered on
identifying useful proof-search actions and providing informative feedback that
enables an agent to use them together.

Understanding and debugging proof search. The interaction trace exposes pro-
posed relationships, solver feedback, and the agent’s explanations for revising
earlier decisions. These records help connect proof-search behavior to the RTL.
For example, the floating point adder trajectory in Section 5.3 reveals that
operand equality and equality of decoded fields become relevant at different con-
trol states. Examining such trajectories can reveal missing observations, repeated
unproductive proposals, and opportunities for additional interface actions. This
makes the framework useful for investigating how proof guidance succeeds or fails
and for refining the information exposed to the agent. The resulting insights could
also inform conventional IC3 heuristics, such as recognizing control conditions
under which a proposed relationship becomes useful.

Learning specialized proof-search policies. Recorded proof-search traces provide a
possible basis for fine-tuning smaller models for lemma generation and action
selection. Training examples could associate proof contexts and agent decisions
with solver feedback and subsequent proof progress. Since a valid lemma may
contribute little to the final invariant, useful training signals should account
for the progress and cost of the resulting search. Such training could improve
decisions about when to introduce observations or revise proposals, in addition
to reducing response latency. The same separation between guidance and checked
proof steps could extend to other algorithms. In interpolation-based model
checking, for example, interpolant strength affects the resulting approximations
and verification performance [15]. An agent could guide interpolant construction
or selection, while the backend enforces the interpolation conditions and any
additional requirements of the model-checking algorithm.
18      Y.-W. Fan et al.

Alternative integration and global reflection. Our framework requests agent guid-
ance at designated generalization steps. An alternative could allow conventional
IC3 heuristics to run until repeated obligations or limited frame progress trigger
agent intervention. Such selective intervention could retain access to the internal
proof state while reducing the frequency of agent calls. A complementary direction
is to give the agent an explicit opportunity to review broader proof progress.
Global guidance in IC3-style algorithms already demonstrates the value of con-
sidering learned lemmas collectively to address limitations of local reasoning [22].
Drawing on agent reflection [16] and multi-agent frameworks [23], a periodic re-
view or a separate reviewing agent could examine admitted lemmas, unsuccessful
proposals, and frame progress to suggest revisions to the proof-search policy.
Providing this broader context could help identify patterns that are difficult to
recognize while concentrating on one proof obligation at a time. The benefit of
these designs would need to be evaluated against their additional reasoning and
coordination costs.



7    Related Work

Section 1 reviews conventional and ML-based IC3 generalization. IC3Syn inte-
grates LLM-generated blocking clauses into an IC3 controller for distributed
protocols and identifies an agent-based workflow as future work [2]. Agentic-IC3
provides such an interaction framework for RTL hardware verification and ex-
tends the role of learned guidance beyond lemma generation, allowing an agent
to introduce observations and revise proof obligations within a persistent IC3
session.
    Large Lemma Miners and CIll generate helper invariants using design infor-
mation and verification feedback [14,17]. Agentic-IC3 guides the model checker’s
internal proof search and could serve as a verification backend for these frame-
works.



8    Conclusion

Agentic-IC3 integrates a language-model agent into a persistent IC3 proof ses-
sion. Using RTL information and solver feedback, the agent guides word-level
generalization, introduces observations, and backtracks to revise proposals. The
backend maintains soundness through solver-checked proof updates. Agentic-IC3
solves 10 of 14 benchmarks, including four unsolved by all three baselines. The
ablation study shows fewer generalization interactions with batching and benefits
from observations and backtracking on selected proof searches. Future work will
examine variability across repeated runs, explore additional agent actions, and
extend the framework to other model-checking algorithms.
        Agentic-IC3: Enabling Semantic Proof Search in IC3 Model Checking           19

References
 1. Bradley, A.R.: SAT-based model checking without unrolling. In: Verification, Model
    Checking, and Abstract Interpretation (VMCAI). pp. 70–87. Springer (2011). https:
    //doi.org/10.1007/978-3-642-18275-4_7
 2. Cao, W., Wu, G., Yao, Y., Wei, H., Chen, T., Ma, X.: Synthesizing inductive
    invariants for distributed protocols via IC3 and large language models. arXiv
    preprint arXiv:2605.24619 (2026). https://doi.org/10.48550/arXiv.2605.24619
 3. Chen, Y., Gong, X., Yin, L., Wang, J., Wang, T.: BCCIC3: Batch clause construction
    enhanced generalization in IC3. In: Formal Methods and Software Engineering
    (ICFEM 2025). Lecture Notes in Computer Science, vol. 16229, pp. 134–151. Springer
    (2026). https://doi.org/10.1007/978-981-95-4213-0_8
 4. Eén, N., Mishchenko, A., Brayton, R.: Efficient implementation of property directed
    reachability. In: Formal Methods in Computer-Aided Design (FMCAD). pp. 125–134
    (2011), https://dl.acm.org/doi/10.5555/2157654.2157675
 5. Goel, A., Sakallah, K.: Model checking of Verilog RTL using IC3 with syntax-
    guided abstraction. In: NASA Formal Methods (NFM). pp. 166–185. Springer
    (2019). https://doi.org/10.1007/978-3-030-20652-9_11
 6. Griggio, A., Roveri, M.: Comparing different variants of the IC3 algorithm for hard-
    ware model checking. IEEE Transactions on Computer-Aided Design of Integrated
    Circuits and Systems 35(6), 1026–1039 (2016). https://doi.org/10.1109/TCAD.
    2015.2481869
 7. Hassan, Z., Bradley, A.R., Somenzi, F.: Better generalization in IC3. In: Formal
    Methods in Computer-Aided Design (FMCAD). pp. 157–164 (2013). https://doi.
    org/10.1109/FMCAD.2013.6679405
 8. Hu, G., Tang, J., Yu, C., Zhang, W., Zhang, H.: DeepIC3: Guiding IC3 algorithms
    by graph neural network clause prediction. In: 29th Asia and South Pacific Design
    Automation Conference (ASP-DAC). pp. 262–268 (2024). https://doi.org/10.
    1109/ASP-DAC58780.2024.10473807
 9. Hu, G., Zhang, W., Zhang, H.: NeuroPDR: Integrating neural networks in the
    PDR algorithm for hardware model checking. In: ACM/IEEE 5th Workshop on
    Machine Learning for CAD (MLCAD). pp. 1–6 (2023). https://doi.org/10.1109/
    MLCAD58807.2023.10299875
10. Lu, H., Xing, Y., Gupta, A., Malik, S.: SoC protocol implementation verification
    using instruction-level abstraction specifications. ACM Transactions on Design
    Automation of Electronic Systems 28(6), 89:1–89:24 (2023). https://doi.org/10.
    1145/3610292
11. Luka, A., Vizel, Y.: Property directed reachability with extended resolution. arXiv
    preprint arXiv:2505.18998 (2025). https://doi.org/10.48550/arXiv.2505.18998
12. Mann, M., Irfan, A., Lonsing, F., Yang, Y., Zhang, H., Brown, K., Gupta, A.,
    Barrett, C.: Pono: A flexible and extensible SMT-based model checker. In: Computer
    Aided Verification (CAV). Lecture Notes in Computer Science, vol. 12760, pp. 461–
    474. Springer (2021). https://doi.org/10.1007/978-3-030-81688-9_22, https:
    //hongcezh.people.ust.hk/publication/cav21/cav21.pdf
13. Niemetz, A., Preiner, M.: Bitwuzla. In: Computer Aided Verification (CAV). Lecture
    Notes in Computer Science, vol. 13965, pp. 3–17. Springer (2023). https://doi.
    org/10.1007/978-3-031-37703-7_1
14. Peled, R., Kroening, D., Tautschnig, M., Vizel, Y.: Large lemma miners: Can
    LLMs do induction proofs for hardware? arXiv preprint arXiv:2511.02521 (2025).
    https://doi.org/10.48550/arXiv.2511.02521
20      Y.-W. Fan et al.

15. Rollini, S.F., Sery, O., Sharygina, N.: Leveraging interpolant strength in model
    checking. In: Computer Aided Verification (CAV). Lecture Notes in Computer
    Science, vol. 7358, pp. 193–209. Springer (2012). https://doi.org/10.1007/
    978-3-642-31424-7_18
16. Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., Yao, S.: Reflexion: Language
    agents with verbal reinforcement learning. In: Advances in Neural Information Pro-
    cessing Systems. vol. 36 (2023), https://proceedings.neurips.cc/paper_files/
    paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.
    html
17. Su, Y., Bu, T., Yang, Q., Ci, Y., Tian, E.: CIll: CTI-guided invariant generation
    via LLMs for model checking. arXiv preprint arXiv:2602.23389 (2026). https:
    //doi.org/10.48550/arXiv.2602.23389
18. Su, Y., Yang, Q., Ci, Y.: Predicting lemmas in generalization of IC3. In: 61st
    ACM/IEEE Design Automation Conference (DAC). ACM (2024). https://doi.
    org/10.1145/3649329.3655970
19. Su, Y., Yang, Q., Ci, Y., Bu, T., Huang, Z.: The rIC3 hardware model checker. In:
    Computer Aided Verification (CAV). Lecture Notes in Computer Science, vol. 15931,
    pp. 185–199. Springer (2025). https://doi.org/10.1007/978-3-031-98668-0_9
20. Tan, Q., Gaonkar, A., Fan, Y.W., Gupta, A., Malik, S.: SecIC3: Customizing IC3
    for hardware security verification. In: Design, Automation and Test in Europe
    Conference (DATE) (2026), https://arxiv.org/abs/2601.21353
21. V K, H.G., Fedyukovich, G., Gurfinkel, A.: Word level property directed reachability.
    In: IEEE/ACM International Conference on Computer-Aided Design (ICCAD).
    pp. 1–9. ACM (2020). https://doi.org/10.1145/3400302.3415708
22. Vediramana Krishnan, H.G., Chen, Y., Shoham, S., Gurfinkel, A.: Global guidance
    for local generalization in model checking. In: Computer Aided Verification (CAV).
    Lecture Notes in Computer Science, vol. 12225, pp. 101–125. Springer (2020).
    https://doi.org/10.1007/978-3-030-53291-8_7
23. Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang,
    S., Liu, J., Awadallah, A.H., White, R.W., Burger, D., Wang, C.: AutoGen: Enabling
    next-gen LLM applications via multi-agent conversations. In: Conference on Lan-
    guage Modeling (COLM) (2024), https://openreview.net/forum?id=BAakY1hNKS
24. Xia, Y., Becchi, A., Cimatti, A., Griggio, A., Li, J., Pu, G.: Searching for i-Good
    lemmas to accelerate safety model checking. In: Computer Aided Verification (CAV).
    pp. 288–308. Springer (2023). https://doi.org/10.1007/978-3-031-37703-7_14
25. YosysHQ: Yosys Open SYnthesis Suite. https://yosyshq.net/yosys/about.html,
    accessed September 13, 2026
26. Zhang, H., Gupta, A., Malik, S.: Syntax-guided synthesis for lemma genera-
    tion in hardware model checking. In: Verification, Model Checking, and Ab-
    stract Interpretation (VMCAI). Lecture Notes in Computer Science, vol. 12597,
    pp. 325–349. Springer (2021). https://doi.org/10.1007/978-3-030-67067-2_15,
    https://hongcezh.people.ust.hk/publication/vmcai21/vmcai21.pdf
27. Zhou, X., Hu, G., Zhang, H., Zhang, W.: A-IC3: Learning-guided adaptive inductive
    generalization for hardware model checking. In: Computer Aided Verification (CAV).
    Lecture Notes in Computer Science, vol. 16682, pp. 357–379. Springer (2026).
    https://doi.org/10.1007/978-3-032-32519-8_19
