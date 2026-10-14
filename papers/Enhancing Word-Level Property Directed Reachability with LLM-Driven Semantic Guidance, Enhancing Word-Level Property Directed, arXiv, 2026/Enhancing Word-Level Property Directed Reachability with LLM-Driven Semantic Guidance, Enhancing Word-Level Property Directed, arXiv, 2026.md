                                                                                                                                                                                                                                       1




                                              Enhancing Word-Level Property Directed
                                          Reachability with LLM-Driven Semantic Guidance
                                                       Guangyu Hu * , Mingkai Miao * , Student Member, IEEE, Zhiyuan Yan , Member, IEEE,
                                                         Xiaofeng Zhou , Graduate Student Member, IEEE, Wei Zhang , Fellow, IEEE, and
                                                                                Hongce Zhang † , Member, IEEE



                                            Abstract—Property Directed Reachability (PDR) is a promi-                            Conventional IC3/PDR                                 Helper-Guided IC3/PDR
                                         nent algorithm for hardware formal verification. However, bit-                                                                                                        Helpers
arXiv:2609.30131v1 [cs.AR] 24 Sep 2026




                                         level PDR often struggles with datapath-heavy designs because                      Model                      IC3/PDR                  Model             Predicates   Clauses    Assertions

                                         bit-blasting obscures high-level semantics. While word-level PDR
                                         addresses this by reasoning over bit-vector and array theories,
                                                                                                                                                                                                Guided IC3/PDR
                                         its performance remains bottlenecked by discovering proof-
                                         relevant word-level relations. We propose LLM4PDR, a framework                 CTIs
                                                                                                                                                                 Large
                                                                                                                                                                 Search
                                         leveraging Large Language Models (LLMs) to guide word-                                                                  Space         CTIs                                      Focused
                                                                                                                                                                                                                          Search
                                         level PDR search through three mechanisms: (1) Predicate
                                         Generation, extracting state relationships as candidate predicates
                                         during inductive generalization; (2) Clause Generation, produc-                solver feedback only                              semantic guidance
                                                                                                                                                                            + sound checks
                                         ing candidate frame lemmas to accelerate convergence after                                            SAFE / UNSAFE                                  SAFE / UNSAFE
                                         formal validation; and (3) Assertion Generation, synthesizing
                                         helper assertions that strengthen the target property under                   Fig. 1: Motivation for helper-guided PDR. Conventional PDR
                                         counterexample-guided refinement. We implement LLM4PDR in                     learns blocking clauses mainly from solver feedback during
                                         the Pono model checker and evaluate it on arithmetic micro-
                                                                                                                       the proof search. LLM4PDR adds verifier-checked semantic
                                         benchmarks, HLS-generated pipelines, open-source RTL com-
                                         ponents, and hardware model checking competition (HWMCC)                      helpers at the predicate, clause, and assertion levels, guiding
                                         instances. Results show LLM-generated guidance improves both                  the same proof search toward word-level relations while pre-
                                         solved instances and runtime on datapath-heavy and control-                   serving soundness through model-checker-side checks.
                                         plus-datapath designs. The strongest configuration solves 28 of
                                         33 arithmetic benchmarks, compared to 13 for vanilla Pono and
                                         11 for AVR. On HLS pipelines and open-source RTL, different
                                         modes provide complementary speedups: clause guidance is                      of these systems by exhaustively exploring possible behav-
                                         effective for deep pipelines and predicate guidance for bus and               iors. Among model checking techniques, Property Directed
                                         memory-controller designs. On HWMCC benchmarks, benefits                      Reachability (PDR), also known as IC3 [1], is a leading
                                         are instance-dependent, demonstrating notable speedups and                    algorithm for hardware formal verification. Traditional bit-
                                         timeout avoidance on hard cases. These results suggest that LLM-
                                                                                                                       level PDR is highly effective for many control-centric de-
                                         generated, verifier-checked semantic hints can serve as a practical
                                         complement to conventional word-level PDR.                                    signs, but modern designs often combine control logic with
                                                                                                                       wide datapaths, arithmetic operations, and on-chip memories.
                                            Index Terms—Hardware formal verification, property directed
                                                                                                                       Bit-blasting these word-level structures can break compact
                                         reachability, word-level model checking, large language models,
                                         invariant generation, inductive generalization.                               arithmetic and relational facts into many low-level Boolean
                                                                                                                       constraints, obscuring the design intent that would otherwise
                                                                                                                       guide the proof search.
                                                                  I. I NTRODUCTION                                        Word-level PDR addresses this limitation by reasoning
                                           The ever-increasing complexity of modern hardware designs                   directly over word-level theories, such as bit-vectors and
                                         poses significant challenges to functional verification. For-                 arrays. A simple arithmetic relationship between two variables,
                                         mal verification, particularly automated model checking, has                  which may require a long chain of Boolean clauses after bit-
                                         emerged as a critical technology for ensuring the correctness                 blasting, can be represented as a single word-level formula.
                                                                                                                       This compact representation gives word-level PDR a natural
                                           * Guangyu Hu and Mingkai Miao contributed equally to this work.             advantage on datapath-heavy designs. At the same time, the
                                            Guangyu Hu and Xiaofeng Zhou are with The Hong Kong Uni-                   verifier may operate on an intermediate transition-system
                                         versity of Science and Technology, Hong Kong SAR, China (e-mail:
                                         ghuae@connect.ust.hk; xzhoubu@connect.ust.hk).                                representation such as BTOR2 [2], where source-level cues
                                            Mingkai Miao, Zhiyuan Yan, and Hongce Zhang are with the                   such as module boundaries, naming conventions, structural
                                         Microelectronics Thrust, Function Hub, Hong Kong University of                intent, and comments are reduced or absent. A relation that is
                                         Science and Technology (Guangzhou), Guangzhou 511458, China
                                         (e-mail: mmiao815@connect.hkust-gz.edu.cn; zyan760@connect.hkust-             otherwise apparent in the RTL can become hard for the proof
                                         gz.edu.cn; hongcezh@hkust-gz.edu.cn).                                         engine to discover.
                                            Wei Zhang is with the Department of Electronic and Computer Engineering,      This information loss creates a concrete obstacle for PDR.
                                         The Hong Kong University of Science and Technology, Hong Kong, China
                                         (e-mail: eeweiz@ust.hk).                                                      During the proof search, PDR learns blocking clauses from
                                            † Hongce Zhang is the corresponding author.                                solver feedback and then tries to generalize them so that each
                                                                                                                                                   2



learned clause rules out a number of unreachable states at                             tion, clause-level guidance for frame strengthening, and
once. However, the feedback available to the engine typically                          assertion-level guidance for property strengthening.
expose only flat bit-vector terms or local signal assignments.                      • Unified helper interface and validation pipeline. To
For example, the proof may need the relation that two counters                         support these mechanisms uniformly, we design a re-
advance with a fixed offset, while the solver only exposes pairs                       stricted SMT-LIB2 [3] helper interface and a verifier-side
of allowed values and it is difficult to discover a higher-level                       pipeline that parses, type-checks, validates, and refines
relation from such low-level value pairs. As a result, the engine                      LLM-generated artifacts before they can affect the proof
may learn many weak local clauses instead of a compact word-                           search.
level lemma.                                                                        • Implementation       and evaluation. We implement
   In this paper, we study the following research question:                            LLM4PDR in Pono [4] and evaluate it on arithmetic,
can external semantic insight of the hardware design guide                             HLS-generated, open-source RTL, and HWMCC
the PDR engine toward useful word-level facts without                                  benchmarks. The results show complementary benefits
compromising the soundness of the algorithm? Today’s Large                             across different structural classes, including a higher
Language Models (LLMs) are well suited for generating                                  number of solved arithmetic cases and large speedups or
such semantic hints because they have been trained on                                  timeout avoidance on several hard word-level instances.
large corpora of source-level hardware artifacts, including                         The remainder of this paper is organized as follows. Sec-
digital logic circuits modeled in hardware description                           tion II reviews the IC3/PDR algorithm and problem formula-
languages, generator-produced hardware code, and formal                          tion. Section III motivates the need for LLM-guided reasoning
specifications. They can recognize recurring design idioms                       with a concrete example. Section IV presents the three LLM-
(such as counters, pipeline stages, and handshake protocols),                    guided mechanisms and their integration into the PDR engine.
and propose candidate relations that those idioms suggest.                       Section V reports experimental results across four benchmark
However, these suggestions must not be trusted as proofs. To                     suites, including ablation studies that isolate the contribution
preserve soundness, the LLM can only act as a hint generator;                    of each mechanism. Finally, Section VI concludes the paper.
the model checker remains responsible for accepting,
rejecting, or refining every generated artifact.                                     II. P RELIMINARIES AND P ROBLEM F ORMULATION
   This paper introduces LLM4PDR, a framework that uses
LLM-generated semantic hints to guide word-level PDR while                       A. Symbolic Transition Systems
leaving all proof decisions inside the verifier. Figure 1 illus-                    A finite-state transition system S is defined by a tuple
trates this shift: conventional PDR relies on solver feedback                    (X, Y, I, T ), where X is a set of state variables, Y is a set
to discover blocking clauses, whereas LLM4PDR augments the                       of primary input variables, I(X) is a formula representing
same proof search with verifier-checked semantic helpers. The                    the initial states, and T (X, Y, X ′ ) is the transition relation,
key observation is that semantic guidance can be useful at three                 mapping current states and inputs to next states. A state
verifier-side interfaces in the PDR workflow. First, before a                    can be regarded as an assignment to all variables in X,
bad-state proof obligation is generalized, a helper predicate                    often represented as a cube (a conjunction of literals). A
can add a word-level atom to the vocabulary from which PDR                       safety property P (X) asserts that only P -states (those whose
builds blocking lemmas. Second, before the main blocking                         assignments make P evaluate to true) are reachable. The
loop starts, a helper clause can be checked as a candidate                       model checking problem asks whether all reachable states of
frame lemma. Third, during property checking, a helper as-                       S satisfy P . For a formula φ , we use the form φ′ to denote
sertion can temporarily strengthen the target property and then                  the case when each of its variable x ∈ X is replaced by the
be removed if counterexamples show that it is invalid. These                     primed version x′ ∈ X ′ .
three roles correspond to predicate, clause, and assertion1
guidance, instantiated as LLM-guided predicate generation,                       B. The PDR Algorithm
clause generation, and assertion generation, respectively. In
                                                                                    PDR (a.k.a. IC3) [1], [5] is a SAT-based algorithm that
all cases, the LLM output is untrusted: generated artifacts are
                                                                                 proves safety properties by incrementally constructing an
parsed, type-checked, validated, and either used or discarded
                                                                                 inductive invariant. The algorithm maintains a sequence of
by the model checker.
                                                                                 over-approximating frames F0 , F1 , . . . , Fk . Each frame Fi is
   Our contributions are summarized as follows.
                                                                                 a formula (a set of clauses that are conjuncted) whose models
   • Semantic-guided word-level PDR framework. We pro-
                                                                                 over-approximate the set of states reachable in at most i steps.
      pose LLM4PDR, a framework that utilizes LLM-generated                      The frame sequence satisfies the following invariants:
      semantic hints to guide word-level PDR without trusting
                                                                                    • F0 = I.                                           (initiation)
      the LLM as a proof oracle.
                                                                                    • For all 0 ≤ i < k:
   • Three verifier-side guidance mechanisms. We identify
      three natural injection points in PDR and instantiate                          1) Fi |= Fi+1 .                                (monotonicity)
                                                                                                     ′
      them as predicate-level guidance for inductive generaliza-                     2) Fi ∧ T |= Fi+1  .                            (consecution)
                                                                                     3) Fi |= P .                                          (safety)
  1 Informally speaking, a predicate is a Boolean condition over state vari-
                                                                                    A counterexample to induction (CTI) is a state that is
ables, such as x < y; a clause is a disjunction of such conditions or their
negations, often learned by PDR as a lemma; an assertion is a safety property,   admitted by the current over-approximation but violates the
or an auxiliary fact conjoined with it, that the verifier attempts to prove.     target property. When a CTI is checked to be unreachable, a
                                                                                                                                      3



Algorithm 1 High-level IC3/PDR Algorithm                              Algorithm 2 Recursive Blocking and Minimal Inductive
 1: procedure PDR(I, T, P )                                           Clause (MIC) Generalization
 2:    if IsSat(I ∧ ¬P ) then return false                             1: procedure B LOCK (s, i)
 3:     F0 ← I; k ← 1; Fk ← P                                          2:    if i = 0 then return false
 4:     while true do                                                  3:     while SAT(Fi−1 ∧ ¬s ∧ T ∧ s′ ) do
 5:        while IsSat(Fk ∧ T ∧ ¬P ′ ) do ▷ Blocking Phase             4:         p ← GetPredecessor() ▷ Extract predecessor state
 6:            s ← GetState(Fk ∧ T ∧ ¬P ′ )                            5:         if not B LOCK(p, i − 1) then return false
 7:            if not B LOCK(s, k) then return false                   6:     c ← MIC(¬s, i)               ▷ Inductive Generalization
 8:        k ← k + 1; Fk ← P              ▷ Propagation Phase          7:     for j ← 1 to i do
 9:        for i ← 1 to k − 1 do                                       8:         Fj ← Fj ∪ {c}
10:            for each clause c ∈ Fi do                               9:     return true
11:                if not IsSat(Fi ∧ c ∧ T ∧ ¬c′ ) then               10: procedure MIC(c, i)
12:                    Fi+1 ← Fi+1 ∪ {c}                              11:     req ← ∅              ▷ Literals that cannot be dropped
13:            if Fi = Fi+1 then return true                          12:     for each literal l ∈ c do
                                                                      13:         g ← c \ {l}
                                                                      14:         if D OWN(g, i, req) then
lemma will be conjuncted to the frame where the CTI was               15:             c←g
found. The structure of the frame gives the proof object a            16:         else
simple hierarchy. A predicate is a Boolean atom over state            17:             req ← req ∪ {l}
variables, such as y = x + 2. A literal is a predicate or its         18:     return c
negation, and a clause is a disjunction of literals. Since each       19: procedure D OWN(g, i, req)
frame is in the conjunctive normal form (CNF), a frame is,            20:     while true do
therefore, a conjunction of clauses. A proof is built gradually       21:         if SAT(I ∧ ¬g) then return false
by adding clauses to frames; each clause may contain one or           22:         if not SAT(Fi−1 ∧ T ∧ g ∧ ¬g ′ ) then       ▷ Check
more predicates, with a unit clause being the special case that           consecution
contains a single predicate.                                          23:             core ← UnsatCore()
   The algorithm operates by alternating between a blocking           24:             gcore ← {literal m | ¬m′ ∈ core}
phase and a propagation phase. Algorithm 1 outlines the high-         25:             while SAT(I ∧ ¬gcore ) do ▷ Ensure initiation
level procedure. In the blocking phase, PDR searches for a            26:                 pick l ∈ g \ gcore ; gcore ← gcore ∪ {l}
CTI, namely a predecessor s of ¬P in Fk , i.e., Fk ∧ T ∧ ¬P ′
                                                                      27:             g ← gcore ▷ Drop literals not in UNSAT core
is satisfiable (Line 5). If such a state exists, the algorithm
                                                                      28:             return true
attempts to block it by recursively proving it unreachable
                                                                      29:         else
from previous frames (Line 6). If the backward search reaches
                                                                      30:             s ← GetPredecessor() ▷ Extract predecessor
an initial state (Line 7), the property is violated. Otherwise,
                                                                          state
the propagation phase pushes clauses forward to subsequent
                                                                      31:             if (g \ ¬s) ∩ req ̸= ∅ then return false
frames (Line 8-12). If two consecutive frames become identi-
cal (Fi = Fi+1 ), a fixpoint is reached, and Fi constitutes an        32:             g ← g ∩ ¬s             ▷ Join operation to cover
inductive invariant proving the property (Line 13).                       predecessor

C. Proof Obligation Handling and Inductive Generalization
   When PDR identifies a CTI s at frame i, it generates a             same predecessor p from being extracted again. The D OWN
proof obligation (s, i) and attempts to block it. Algorithm 2         procedure is the workhorse of MIC. It checks if g satisfies
illustrates this recursive blocking process. The B LOCK proce-        consecution relative to Fi−1 using a SAT query. If the query
dure checks if s has a predecessor in Fi−1 . If a predecessor p       is unsatisfiable (UNSAT), the SAT solver returns an UNSAT
exists, it recursively blocks p at frame i − 1. If no predecessor     core, namely a subset of the assumptions sufficient to cause
exists, ¬s is inductive relative to Fi−1 .                            the conflict. D OWN uses this core to simultaneously drop
   At this point, PDR performs inductive generalization to            multiple unnecessary literals from g, significantly speeding up
strengthen ¬s into a smaller clause c ⊆ ¬s that remains in-           generalization. If the query is satisfiable (SAT), the solver has
ductive relative to Fi−1 . This step is critical: a stronger clause   found a predecessor state s. To make the clause inductive,
(containing fewer literals) blocks a larger set of unreachable        D OWN performs a join operation (g ← g ∩ ¬s), which drops
states, accelerating convergence. The minimal inductive clause        literals from g to ensure the generalized cube covers the
(MIC) generalization [6] procedure iteratively attempts to drop       predecessor s.
literals from ¬s. For each candidate subclause g, the algorithm          The effectiveness of PDR heavily relies on the quality of
calls the DOWN subprocedure to verify and further minimize.           the generalized clauses. As shown in Algorithm 2, MIC’s
   The B LOCK procedure’s while loop eventually terminates            literal-dropping order is determined either by an arbitrary
because each successful recursive call to B LOCK adds a new           fixed order or by the SAT solver’s UNSAT core extraction
clause to Fi−1 , strengthening the frame and preventing the           (Line 23), with no semantic understanding of the literals’ roles
                                                                                                                                             4



in the design. This reliance on SAT solver heuristics can result           module top(input clk, input rst, input lden,
in generalizations that capture only local bit-level patterns,                        input ps, input [15:0] ia,
                                                                                      input [15:0] ib);
forcing the algorithm to explicitly enumerate and block many                   reg [15:0] ra, rb, rai, rbi;
individual states, leading to deep backward searches and                       always @(posedge clk) begin
                                                                               if (rst) begin
performance degradation [7], [8]. The same issue also appears                      ra <= 0; rb <= 0;
at the representation level: a compact word-level fact may                         rai <= 0; rbi <= 0;
                                                                               end else begin
require a large number of bit-level clauses, making it difficult                   if (lden) begin
for PDR to discover and exploit the underlying word-level                          ra <= ia; rb <= ib;
                                                                                   rai <= ia; rbi <= ib;
semantics.                                                                         end else begin
                                                                                   if (~ps) begin
                                                                                       rai <= rai + 1; rbi <= rbi + 1;
D. Clause and Literal Explosion in PDR                                         end end end end
   Bit-level PDR represents each frame as a CNF formula                        assert property (!(ra == 16’h1357 &&
                                                                                 rai == 16’h9356 && rb == 16’h2468
over Boolean literals. This representation is sound and solver-                  && rbi == 16’h2467));
friendly, but its size can grow significantly when the proof                   // rai-ra = 16’h7fff, rbi-rb = 16’hffff
                                                                           endmodule
depends on a word-level relation. A simple relation, such as
a = b + c or x − y = 2, is a single atom at the word level, but     Fig. 2: An example of a hard-to-prove property for existing
after bit-blasting, the same relation is now over the bit slices    SAT-based model checking algorithms.
of the word-level variables, and PDR faces two kinds of blow-
up. First, no single clause captures such a relation, so PDR
has to learn many clauses, each ruling out only a small set of                                III. M OTIVATION
states; this is the clause explosion. Second, each such clause         This section demonstrates a concrete example that remains
can also contain many literals, which is the literal explosion.     challenging for the existing bit-level and word-level PDR
Both effects make the proof larger and slow down every SAT          engines.
query in PDR.
                                                                       One recurring challenge in hardware model checking is the
   Existing engines address this bottleneck mainly in two ways.
                                                                    discovery of effective, high-level inductive invariants required
One possibility is to remain at the bit level, exemplified by
                                                                    to prove a property. PDR provides a robust framework for
the work from the Luka and Vizel, who proposed the PdrER
                                                                    formal proof, yet prior work has shown that its performance
algorithm [9] that adds auxiliary variables and definitions
                                                                    depends heavily on the quality of inductive generalization
to shorten the proof. On one buffer-allocation benchmark,
                                                                    and on the auxiliary predicates or lemmas available to the
ordinary PDR needs more than 65,000 invariant clauses, while
                                                                    engine [6]–[10]. Existing approaches derive such informa-
the proof with auxiliary definitions is far smaller. However,
                                                                    tion through pre-coded rules, fixed templates, solver-feedback
PdrER generates these definitions according to fixed patterns
                                                                    heuristics, or artifacts such as Craig interpolants [13]–[15]. But
rather than deriving them from the design semantics. The
                                                                    this strategy exposes a practical bottleneck: when the necessary
second approach reasons directly at the word level, as exem-
                                                                    arithmetic relationship is implicit in the update logic and does
plified by AVR [10]. Instead of bit-blasting the design, AVR
                                                                    not match the engine’s built-in generation patterns, the search
derives additional terms and predicates from the transition
                                                                    for an inductive invariant can stagnate. Consider the property
system, symbolic post-images, interpolants, and predefined
                                                                    checking problem in Figure 2 as an example. The design
deduction rules. Although this approach can potentially avoid
                                                                    contains four 16-bit state variables (ra, rai, rb, rbi) and a
bit-level blow-up, its terms and predicates are still generated
                                                                    safety property asserting that a particular state assignment is
by hand-crafted rules and built-in heuristics. Consequently,
                                                                    unreachable. Observe that rai and rbi are both incremented
both approaches may fail to discover relations unique to a
                                                                    under identical guard conditions; consequently, the invariant
particular design: an engine may explore many irrelevant terms
                                                                    rai − ra = rbi − rb holds across all reachable states. A
before finding the crucial relation, or may never find it at all.
                                                                    human designer recognizes this word-level relationship almost
Section III illustrates such a case.
                                                                    immediately. Yet at the bit level the subtraction rai − ra
   On the other hand, LLM4PDR takes a different approach.
                                                                    alone expands into a chain of full-adder carry propagation
Instead of generating candidate facts from fixed rules, it uses
                                                                    across all 16 bits, producing an exponential blowup in the
an external LLM to read the static design (the RTL when
                                                                    Boolean representation. A SAT-based engine must rediscover
it is available, and otherwise the BTOR2 transition system)
and to propose helper predicates, clauses, or assertions in a
strict SMT-LIB2 format. These suggestions are not trusted as        TABLE I: Results of different model checkers on the motivat-
invariants or assumptions. A helper predicate is used only          ing example for word widths from 16 to 20 bits.
as a candidate atom during generalization; a helper clause
                                                                              Model checker          Result on 16–20-bit instances
must pass frame-consistency checks before it is added to
a frame; and a helper assertion is kept only if it survives                   Berkeley-ABC [11]            TO on all widths
                                                                              rIC3 [12]                    TO on all widths
counterexample-guided refinement. In this way, a relation that                AVR [10]a                    TO on all widths
would otherwise need many bit-level clauses can enter the                     PdrER [9]                    TO on all widths
proof as one compact suggestion, while the verifier still makes        TO: runtime exceeded the 3600-second limit for every tested width.
                                                                       a The better result of the SA and SA+UF configurations is reported.
every decision that affects soundness.
                                                                                                                                                   5




                                                                                                            Helper
                        Hardware                                                    SMT-LIB2
                                                        LLM                                                 Parser
                         Model                                                       Helpers
                 RTL                      AI                                f                            binds arguments
                                                 proposes helpers                    define-fun
                       BTOR2 / RTL                                                                          to system
                                                                                     declarations
                                                                                                            variables




                                     Purpose                             Two-Phase MIC
                       Predicates         fragment of               • freeze helper predicates
                                            lemmas                  • remove redundant predicates                                 Verification
                                                                                                                                    Result

                                     Purpose                           F1 Clause Injection                                           SAFE
                       Clauses           candidate F1               • init-cover check                                               + invariant
                                           lemmas                   • one-step induction check            IC3/PDR Engine
                                                                                                                                     UNSAFE
                                                                                                                                     + CEX
                                     Purpose                          Assertion Refinement
                       Assertions           property                • check augmented property
                                         strengthening              • drop falsified assertions




Fig. 3: Overview of LLM4PDR. A hardware model is analyzed by an LLM or external tool to produce restricted SMT-LIB2
helper declarations. After parsing and binding helper terms to system variables, the verifier consumes predicates through two-
phase MIC, clauses through F1 injection, and assertions through property-strengthening refinement before returning a safe
proof with an invariant or an unsafe counterexample.


this arithmetic structure and express it using the propositional                     ; helper predicate: extra MIC predicates
logic, whose formula size scales poorly with word width. As                          (define-fun |predicate.k| ((v1 S1) ... (vn Sn)) Bool
                                                                                       <SMT-LIB2 Boolean term>)
table I shows, Berkeley-ABC [11], rIC3 [12], AVR [10], and
PdrER [9] all fail to solve the instance within the one-hour                         ; helper clause: candidate frame lemma
                                                                                     (define-fun |clause.k| ((v1 S1) ... (vn Sn)) Bool
timeout for every width from 16 to 20 bits.                                            <SMT-LIB2 Boolean term>)

                                                                                     ; helper assertion: tentative property strengthening
   Once a relation such as rai − ra = rbi − rb is proposed, the                      (define-fun |assertion.k| ((v1 S1) ... (vn Sn)) Bool
verifier can check it using ordinary initiation and consecution                        <SMT-LIB2 Boolean term>)

queries. The hard part is that existing engines often do
                                                                                   Fig. 4: Restricted SMT-LIB2 helper format. Each entry is an
not synthesize this relation from the low-level encoding by
                                                                                   SMT-LIB2 define-fun; the reserved prefix determines how
themselves. This disparity calls for formal reasoning at a
                                                                                   the PDR engine may consume the term.
higher level.

   This limitation motivates augmenting rule-based lemma
                                                                                                       IV. M ETHODOLOGY
generation with externally proposed semantic hints. In this
paper, we use large language models (LLMs) as semantic hint                           Our framework, LLM4PDR, enhances Property Directed
generators: given a static hardware description, the LLM can                       Reachability by integrating LLM guidance at three stages of
suggest proof-relevant relationships among state variables and                     the verification workflow. As shown in Figure 3, an LLM
emit candidate helper artifacts in a restricted SMT-LIB2 format                    extracts high-level insights from the RTL description and emits
that the verification engine can consume. This also differs                        them as restricted SMT-LIB2 [3] helper declarations (when
from our prior work DreamMiner [16], which learns property                         RTL is not available, BTOR2 transition-system input is used
augmentations from simulation traces and dynamic execution                         instead). These insights become formal artifacts (predicates,
data, while LLM4PDR uses just the static design information.                       clauses, and assertions), steering the PDR engine toward a
                                                                                   more efficient proof search.
   LLM4PDR differs from fixed-rule word-level engines as the
LLM is not limited to a pre-coded set of term-construction
templates. It can use naming, structural context, and recurring                    A. Restricted SMT-LIB2 Helper Interface
RTL idioms to propose predicates, clauses, or assertions that                        Before discussing individual mechanisms, we first describe
are apparent to a designer but difficult for a heuristic term                      the interface, through which the helper information enters the
generator to synthesize. Importantly, this approach positions                      model checker. LLM4PDR uses a helper interface based on
the LLM strictly as a semantic guide rather than a trusted                         a restricted SMT-LIB2 file, rather than a separate domain-
proof oracle. Because the verifier independently checks every                      specific language. The LLM is expected to generate typed
generated candidate using its mathematical proof obligations,                      SMT-LIB2 definitions, where the reserved name prefixes tell
our framework can accelerate the proof search while preserv-                       the verifier the desired use cases of the hints. The interface
ing the soundness of the verification process.                                     bares no guarantee that the hints are useful and it does not
                                                                                                                                                                                   6




          Hardware Context                                                                        COI-Aware Prompt
                    module example (                                                        Prompt Builder                                                       Mode-specific
                            input …,
                            input …,
                                                              [SYSTEM ROLE] You are an expert on Verilog, BTOR2, SMT-LIB v2 and IC3/PDR                         Helper Artifacts
                                                              verification. Your task is to craft helper artifacts.
                            …
                            output …);                        [FEW-SHOT EXAMPLE]                       [TASK DESCRIPTION]
                                                 Cone of      Verilog/BTOR2 snippet: …                 Given a target Verilog/BTOR2 …                            Predicate
                        wire …;

               …                                                                                                                                       LLM
                                                                                                       Given COI filtered variables …
                        reg …;                  Influence     COI filtered Var…
                                                              Example predicate/clause/assertion: …    Generate <= 5 linear helper
                        always … begin
                                                              [COI ANALYSIS]
                                                                                                       predicates/clauses/assertions …                Backend      Clause
                        …                                     Input vars: … state vars: …
                                                                                                       [STRICT OUTPUT FORMAT]
                        end                                                                            Only ;comments+(define-fun ...) declarations
                        assert property (…);   COI filtered
                                                              COI analysis: …
                                                              COI analysis completed                   No set-logic, check-sat, exit …                           Assertion
                                                                                                       Exact BTOR names & bit-widths …
                                                              - Found COI statevar x …
                        endmodule
                                                context


Fig. 5: COI-aware prompt construction and helper synthesis in LLM4PDR. Given a verification problem, LLM4PDR uses RTL
when available and otherwise the BTOR2 transition-system input. A cone-of-influence (COI) analysis extracts property-relevant
variables and transition fragments, which are inserted into a fixed prompt template together with the system role, a few-shot
helper example, a mode-specific task description, and strict SMT-LIB2 output constraints. The LLM backend then emits
mode-specific helper artifacts, namely predicate.*, clause.*, or assertion.* declarations, which are later parsed,
type-checked, and validated by the verifier before use.


modify any part of the transition systems. It is rather a side            cates, clauses, and augmented properties all remain subject to
input that carries structured hints into the PDR engine.                  verifier-side checks.
   Figure 4 shows the overall structure of this SMT-LIB2 file.
The SMT-LIB2 format is beneficial, because the terms must
                                                                          B. Prompt Construction and Helper Synthesis
already have precise bit-vector sorts and solver-level semantics
under such format. The only extra convention is the reserved                 The helper interface above defines what the verifier can con-
name prefixes. A predicate.* prefix indicates that the                    sume, while prompt construction determines how LLM4PDR
term follows should be placed in the helper-predicate pool                asks the LLM to produce such helper artifacts. As shown
Pext and can be used as an additional predicate during MIC.               in Figure 5, LLM4PDR builds a COI-aware prompt from a
A clause.* term is placed in the helper-clause pool Cext                  static hardware context and sends the instantiated prompt to
and must respect the initiation, monotonicity and consecution             an LLM backend, which returns mode-specific helper artifacts.
requirements mentioned in Section II-B when it is used to                 For each target property, LLM4PDR starts from the hardware
strengthen a frame. An assertion.* term is placed in                      representation available to the verifier, namely the relevant
the helper-assertion pool Aext and is used as a tentative                 RTL fragment when RTL is available, and otherwise the
strengthening of the target property, with counterexamples                BTOR2 transition-system input. The prompt also includes the
used to remove helpers that turn out to be invalid.                       target property and the state variables that may participate in
   The distinction among helper predicates, helper clauses,               proof-relevant helper declarations.
and helper assertions follows the proof hierarchy from Sec-                  Before assembling the prompt, LLM4PDR applies cone-of-
tion II-B. A helper predicate is an atom that MIC may use                 influence (COI) analysis with respect to the target property.
when it constructs a blocking clause for one proof obligation;            COI identifies the state variables and transition fragments
it serves as a candidate atom for generalization. A helper                whose fan-in can affect the property. Variables and transition
clause is a candidate frame lemma. Before insertion into F1 ,             fragments outside this slice are omitted from the prompt,
it must pass such checks: the initial state predicate must                leaving the COI-filtered design context shown in Figure 5.
imply the clause, and every one-step successor of an initial              This filtering reduces the prompt size and serves as a property-
state must satisfy the primed clause. A helper assertion is a             directed relevance filter, restricting the model context to design
candidate strengthening of the target property and is filtered            elements that can structurally influence the target property. It
by counterexample-guided refinement. Thus the same word-                  will not change the transition system, the target property, or
level fact, such as y = x + 2, can appear in three roles: as              any proof obligation checked by PDR. Empirically speaking,
a predicate atom available to MIC, as a unit clause that can              on representative HWMCC instances, this pruning removes
be checked for F1 insertion, or as an assertion conjoined with            between 52.35% and 82.49% of the state variables from the
the target property.                                                      prompt, reducing both the prompt size and the space of
   The processing path follows three steps. First, the parser             irrelevant candidate helpers the model can propose.
checks that the helper file is syntactically valid SMT-LIB2.                 The prompt builder then instantiates a fixed prompt tem-
Second, elaboration binds every formal argument in a helper               plate, where the system role asks the model to act as a
term to a state variable in the transition system and checks              hardware-verification assistant and to emit helper artifacts
that their bit-vector widths match. Third, the prefix dispatches          in the restricted SMT-LIB2 format. The few-shot example
the term to the corresponding validation path. This structured            provides a small RTL or BTOR2 fragment together with
interface gives the LLM a concrete way to communicate                     correctly typed helper declarations, so the model sees the
word-level information, while keeping soundness inside the                expected types, reserved name prefixes, and the overall output
verifier: helper information can guide search, but the predi-             structure before it generates helpers for the target instance. The
                                                                                                                                      7




               module xp2(clk);
                                                                      Algorithm 3 Helper-Preserving Minimal Inductive Clause
                  input clk;                                          (MIC)
                  reg [5:0] x = 6’d0;
                  reg [5:0] y = 6’d2;                                  1: procedure S YNTHESIZE P REDICATES(D)
                                                                       2:    Praw ← QueryLLM(D)
                  wire      stop;
                  assign stop = (x == 6’d61);                          3:    return {p ∈ Praw | SAT(p) ∧ SAT(¬p)}          ▷ filter out
                                                                            trivial predicates
                  always @(posedge clk) begin
                      if (!stop) begin
                          x <= x + 1;
                          y <= y + 1;                                  4: procedure T WO P HASE MIC(Fi , T, c, Pext )
                      end                                              5:    B ← BitLiterals(c); Vc ← Vars(c)
                  end
                                                                       6:    H←∅             ▷ Helper literals determined by the CTI
                  always @* begin                                      7:    for each p(⃗v ) ∈ Pext with ⃗v ⊆ Vc do
                      x_lt_y: assert(x < y);
                  end                                                  8:        if c |= p then
                                                                       9:            H ← H ∪ {p}
               endmodule // xp2
                                                                      10:        else if c |= ¬p then
Fig. 6: RTL code of the xp2 counter. The useful proof helper          11:            H ← H ∪ {¬p}
                                                                               ⋆
is a word-level relation between x and y, but after translation       12:    B ← M INIMIZE BASE C UBE(Fi , T, H, B) ▷ Phase
into the bit level, the proof obligations expose low-level bit-           1: H is frozen
vector terms rather than the word-level relations.                    13:    for each helper literal h ∈ H do        ▷ Phase 2: Drop
                                                                          redundant helpers
                                                                      14:        Htmp ← H \ {h}
COI analysis supplies the property-directed design context,           15:        Q ← Htmp ∪ B ⋆
including the selected variables and transition fragments. The        16:        Φ ← Cube(Q); Φ′ ← Prime(Φ)
task description selects the guidance mode and asks the model         17:        if SAT(I ∧ Φ) then
to generate helper predicates, helper clauses, or helper asser-       18:            continue ▷ Keep h: cube reaches initial states
tions. Finally, the strict output-format instruction constrains       19:        if SAT(Fi ∧ ¬Φ ∧ T ∧ Φ′ ) then
the requirements for the SMT-LIB2 structure.                          20:            continue         ▷ Keep h: no longer inductive
   In each run, the mode-specific task in Figure 5 asks for up
                                                                      21:        H ← Htmp ▷ Drop redundant word-level helper
to five declarations with one reserved prefix: predicate.*,
clause.*, or assertion.*. The prefix dispatches each                  22:    return ¬Cube(H ∪ B ⋆ )
declaration to the corresponding verifier-side path introduced
in Section IV-A, where it is parsed, type-checked, and val-           23: procedure M INIMIZE BASE C UBE(Fi , T, H, B)
idated before it is used in the PDR procedure. Across all             24:      Φ ← Cube(H ∪ B)
experiments, we use the same prompt template and per-request          25:      Γ ← Fi ∧ ¬Φ ∧ T ∧ Cube(H ′ )        ▷ Hard constraints
cap, so the three settings LLM2Predicate, LLM2Clause,                 26:      B ⋆ ← {b ∈ B | b′ ∈ U NSAT C ORE(Γ; B ′ )} ▷ Only B ′
and LLM2Assert that will be detailed in the next three                27:      return R ESTORE I NITIATION(I, H, B ⋆ , B)
subsections differ only in how the verifier consumes the                         ▷ Restore literals as needed to exclude initial states
generated information.

C. LLM-Guided Predicate Generation                                       As previously stated in Section II-C, inductive generation
                                                                      attempts to find a clause g to block a proof obligation s at
   To help explain how helper predicates are used in our
                                                                      a certain frame Fi when s is shown to be unreachable from
method, we start with a small example as shown by Figure 6.
                                                                      the prior frame Fi−1 . To maintain the requirements of the
It is not hard to find that a word-level inductive invariant
                                                                      frame sequence, the clause g needs to satisfy the following
y = x + 2 holds for x and y within the reachable-state bound
                                                                      requirements:
x ≤ 61 and it should be useful to prove the target property in
this example.                                                                                               I⇒g                     (1)
   However, the bit-level IC3/PDR typically discovers CTIs as                                    g ∧ Fi−1 ∧ T ⇒ g ′                 (2)
bit-level cubes: a state is represented by conjunction of literals,
                                                                                                            g ⇒ ¬s                  (3)
where each literal refer to a single bit in a multi-bit variable
(written as a bit extraction). For example, a proof-obligation        The bit-level IC3/PDR implementation typically invokes the
cube from an actual xp2 run states that all six bits of y are         aforementioned MIC procedure (Algorithm 2) to remove the
one and bit 1 of x is one:                                            literals in B to form the clause g.
          B = {y[j] = 1 | 0 ≤ j ≤ 5} ∪ {x[1] = 1}.                       However, those literals in CTI describe only one corner
                                                                      of the state space, and do not directly model the high-level
Here v[i] denotes a single-bit slice of the bit-vector v, or term     arithmetic relation such as y = x + 2 that we need in the
extract(i, i, v) in the SMT syntax. Here, we use s to refer to        inductive invariant.
                                     def
the corresponding state formula s = (y = 63) ∧ (x[1] = 1),               This is where the LLM is useful. We ask LLM to
and each bit assignment (such as y[5] = 1) is in fact a literal.      read the low-level design representation and generate a
                                                                                                                                                                                                                        8



  IC3/PDR Frames                   Helper predicates
                                    (e.g., from LLM)
                                                                           Two-Phase MiC                                                                Algorithm 4 Helper Clause Side-loading
                                                                          Phase 1: remove bit-level clutter
                                                                force-keep
                                                                helper predicates
                                                                                                    UNSAT core
                                                                                                    prunes extract bits
                                                                                                                                                        Require: Transition system (Init, T ), PDR frames F0 , F1 ,
                   Partial CTl cube
                       bit-level (extracts)                extract(y,5)
                                                                                    y=x+2

                                                                                    x＜y
                                                                                                                                                            Helper clauses Ccand
                        extract(y,5)                       extract(x,1)                                                        Compact blocking lemma
   F0= Init             extract(x,1)                       extract(y,0)
                                                                                    y＜x+3
                                                                                lsb（x）=lsb（y）
                                                                                                                  drop bits       lemma = P1 OR P2      Ensure: F1 strengthened with sanity-checked helper clauses
                        extract(y,0)

                      word-level (helpers)                  Phase 2: remove redundant word-level helpers                           p1：y = x + 2          1: procedure S IDE L OAD C LAUSES(Ccand )
     F1                   y=x+2                             y=x+2             x＜y         y＜x+3       lsb（x）=lsb（y）
                           x＜y                                                                                                     p2：y＜ x + 3           2:    for each clause c ∈ Ccand do
     F2                  y＜x+3                              redundant                             essential

       CTI
                      lsb（x）=lsb（y）
                                                          lsb（x）=lsb（y）        x＜y          y=x+2        y＜x+3
                                                                                                                                                         3:        if c is not Boolean then continue
                                                                                                      inductive test
                                                                                                                                     block CTl/
                                                                                                                                 strengthen frame
                                                                                                                                                         4:        if S AT(Init ∧ ¬c) then continue          ▷ violates
                                                                                                    decide keep/drop

                                                                                                                                                            F0 ⇒ F1
              Without Two-Phase MlC:                       extract(y,5)
              the core may keep a few bits
              and lose the useful word-level structure.    extract(x,1)
                                                                               y=x+2
                                                                                          × y＜x+3             Little word-level info
                                                                                                              → weaker lemma, slower proof
                                                                                                                                                         5:        c′ ← P RIME(c)
                                                                                                                                                         6:        if S AT(Init ∧ T ∧ ¬c′ ) then continue ▷ violates
Fig. 7: Helper-predicate guided two-phase MIC. A CTI cube
                                                                                                                                                            F0 ∧ T ⇒ F1′
initially contains bit-level extract literals and matched word-
level helper predicates. The first phase freezes helper predi-                                                                                           7:        F1 ← F1 ∧ c       ▷ c is a valid first-frame lemma
cates while pruning bit-level clutter; the second phase selec-                                                                                           8:    while true do                        ▷ Main PDR loop
tively removes redundant helper predicates through inductive                                                                                             9:        while Fk ∧ T ∧ ¬P ′ is SAT with witness c do
checks, leaving a compact blocking lemma that preserves                                                                                                 10:            if not B LOCK(c, k) then
useful word-level structure.                                                                                                                            11:                return Unsafe
                                                                                                                                                        12:        ···                   ▷ Main PDR loop continues

restricted SMT-LIB2 helper file with helper predicates
(S YNTHESIZE P REDICATES in Algorithm 3 builds the candi-                                                                                               are asserted, so the core is allowed to explain only which
date pool once for the design). For xp2, the generated helper                                                                                           bit-select literals are still needed.
file contains predicates such as:
                                                                                                                                                           Then in the second phase (Lines 13–21), the helper predi-
          p1 : y = x + 2,                                      p2 : x < y,                                 p3 : x ≤ 61.                                 cates become removable. The engine tries iteratively dropping
                                                                                                                                                        helpers from B ⋆ ∪ Hp . If removing a helper still excludes
These predicates enrich the literal set available to the inductive                                                                                      initial states and remains inductive relative to the current
generalization procedure. Because Formula (3) states that g ⇒                                                                                           frame (both checks remain UNSAT), the helper predicate is
¬s and g is a disjunction of literals, then every literal l in g                                                                                        deemed redundant and can be dropped. This lets MIC keep
should all follow the requirement that s ⇒ ¬l. Therefore, we                                                                                            the generated word-level facts that are actually needed for the
may evaluate each available predicate p under the CTI and use                                                                                           CTI, while discarding generated facts that are merely implied
either p or ¬p as the candidate. If the outcome of the predicate                                                                                        by the remaining cube. The final lemma is therefore compact
is not fixed, then it means the candidate p does not follow the                                                                                         and word-level, instead of being a handful of bit-selects.
above requirement and should be discarded for this inductive                                                                                               Though LLM-generated predicates are used, the soundness
generalization attempt. This selection is described by Lines 7–                                                                                         of the IC3/PDR algorithm is preserved. The LLM never gets
11 in Algorithm 3. In the running example, suppose the CTI                                                                                              to add a fact directly to a frame. All external predicates are
state matches a helper-predicate subset Hp from the generated                                                                                           checked to ensure the resulted clause g follows the require-
file, so the working cube becomes:                                                                                                                      ments stated in Formula (1)–(3).
                                                    C + = B ∪ Hp .
   At first glance, one might simply give C + to ordinary MIC                                                                                           D. LLM-Guided Clause Generation
to select the literals. In practice, however, MIC may only select
a few bit-level literals in B while dropping all matched helper                                                                                            Helper clauses use the same LLM-proposed word-level re-
predicate candidates in Hp entirely. This is because ordinary                                                                                           lations at a different point in the PDR workflow. While helper
MIC sees every element of C + as a removable assumption,                                                                                                predicates wait for a CTI and then give MIC an expanded set
and the UNSAT core extraction in MIC has no direct control                                                                                              of candidate atoms, helper clauses are used earlier and more
on which assumption to keep (it is totally dependent on the                                                                                             directly: before the main blocking loop starts, the verifier asks
internal heuristics of the underlying SAT solver).                                                                                                      whether any generated formula is already strong enough to be
   Our solution is to make MIC work in two phases, as                                                                                                   placed in the first frame F1 . This is referred to as the clause
illustrated by T WO P HASE MIC in Figure 7. In the first                                                                                                side-loading mechanism in the prior work [17]. It gives PDR
phase (corresponding to Line 12 in Algorithm 3), the helper                                                                                             a better initial frame sequence, without any change to either
predicates in Hp are frozen. The solver is allowed to remove                                                                                            the transition system or the target property.
only bit-level literals from B, while the matched helper                                                                                                   The distinction matters in the xp2 example. Without side-
literals remain hard constraints. Consequently, UNSAT-core                                                                                              loaded clauses, F1 in the the initial frame sequence is set
minimization (M INIMIZE BASE C UBE) can shrink B to a                                                                                                   to the target property, namely F1 = P , and the engine has to
smaller set B ⋆ , but does not discard any helper predicates.                                                                                           discover the arithmetic relation between x and y through CTIs.
Operationally, the solver checks the usual initiation and                                                                                               In practice, this produces many local bit-slice lemmas. Clause
consecution conditions while the candidate next-state helpers                                                                                           generation asks the LLM to propose complete frame lemmas
                                                                                                                                                                                        9



(clauses) up front. For xp2, the helper-clause file contains the     Algorithm 5 CEX-Guided Helper Assertion Refinement
desired relation                                                     Require: Transition system (Init, T ), target property P ,
                        c∆ : y = x + 2,                                  helper assertions Acand
as well as other conjectures, such as                                Ensure: Safe for P , or Unsafe with a real counterexample
                                                                      1: procedure C HECK W ITH A SSERTIONS(P, Acand )
cpar : (x & 1) = (y & 1),        ci : (y < x + 3) ∨ (x[2] ̸= 0).      2:     V ← AcandV         ▷ active helpers not yet invalidated
                                                                      3:     P ⋆ ← P ∧ a∈V a
The formula c∆ will be treated as a unit clause after being
                                                                      4:     while true do
loaded, which exposes the whole proof idea: if y = x + 2
                                                                      5:         c ← G ET BAD C UBE(P ⋆ )
is present in the frame, the property x < y is no longer
                                                                      6:         if c ̸= ⊥ then
something PDR must reconstruct from unrelated bit patterns.
                                                                      7:             if not B LOCK(c) then
The other clauses illustrate why clause generation is not
                                                                      8:                 if E VAL(P, c) = false then
merely predicate generation under another name. For example,
                                                                      9:                     return Unsafe
ci is a disjunction-shaped frame lemma: it combines the
                                                                     10:                 V ← {a ∈ V | E VAL(a, c) = true}           ▷
arithmetic predicate y < x + 3 with a bit-level condition on
                                                                         remove falsified helpers V
x[i] and rules out a family of nearby unreachable states. Such
                                                                     11:                 P ⋆ ← P ∧ a∈V a
clauses can be inserted and propagated as complete lemmas,
                                                                     12:                 R ESTART W ITH(P ⋆ )
even when they are not single word-level atoms.
   Side-loading is only helpful when the injected clauses are        13:         else
good. A large set of irrelevant clauses can slow every SAT           14:             N EW F RAME
query and steer the search toward unproductive regions. There-       15:             if P ROPAGATE then
fore LLM4PDR treats every formula in Cext as a candidate, not        16:                 return Safe
as a trusted invariant. After parsing and type-checking, the
engine performs the two sanity checks required for a clause              LLM helper assertions              Strengthen property
                                                                                                                                                    IC3/PDR checks P+
                                                                               a1,a2,a3                  P+=P AND a1 AND a2 AND a3
to live in F1 :
                                                                                                                                                                         NO
     UNSAT (Init ∧ ¬c),          UNSAT (Init ∧ T ∧ ¬c′ ).                                                                                Counterexample
                                                                                                                                                             NO
                                                                                                                                                                        SAFE
                                                                                restart with weaker p+                                       to P+ ?                 invariant proves
                                                                                 p+ = p AND a1 AND a3                                                                     P+ => P
The first query checks that adding c preserves F0 ⇒ F1 : no                                                                               YES

initial state may violate the side-loaded clause. The second                                                      YES: replay counterexample trace
                                                                                                                     check original p and each ai
checks that F0 ∧ T ⇒ F1′ : every one-step successor of an                P is true, some ai are false
                                                                         DROP falsified assertions
                                                                                                                     p:          true                                   P is false
                                                                                                                     a1:         true                             REAL counterexample
initial state must satisfy the primed clause.                                    drop a2                             a2:          false    ×                          UNSAFE
                                                                                                                     a3:         true
   Algorithm 4 summarizes such validation path. After a candi-
date passes both checks, the lemma object will be inserted into                               Only assertion consistent with counterexamples survive.
F1 . From that point on, the clause is handled by the ordinary
PDR machinery. If it is relatively inductive at later frames,        Fig. 8: Counterexample-guided refinement for helper asser-
propagation will push it forward; if not, it stays behind and will   tions.V The verifier checks the strengthened property P ⋆ =
not appear in the final inductive invariant. In the xp2 run, the     P ∧ a∈V a. A counterexample to P ⋆ is replayed against the
relation y = x + 2 is side-loaded into F1 and then propagates        original property: if it violates P , it is a real counterexample;
with the proof, while clauses that only satisfy the first-frame      otherwise, only the falsified helper assertions are removed and
checks are naturally filtered by subsequent propagations.            PDR restarts with a weaker strengthened property.
   The soundness boundary is the same as in helper-predicate
generation. The LLM can propose a word-level lemma, but
the verifier decides whether the lemma is legal at F1 , and the      stronger property proves the original one, while giving PDR a
existing propagation checks decide whether it survives beyond        more informative property frame to build from. Algorithm 5
F1 . Thus clause generation gives PDR a head start with the          summarizes this counterexample-guided refinement workflow.
checks to ensure the frame sequence is sound.                        Lines 2–3 initialize the active helper set and construct the
                                                                     strengthened property.
                                                                        The xp2 example shows why this is useful. The target
E. LLM-Guided Assertion Generation
                                                                     property is P : x < y. The LLM may propose the word-level
   Helper assertions use LLM-proposed word-level conjectures         relation
at the property level. While helper predicates and helper                                  a∆ : (y − x) = 2.
clauses do not change the transition system or the target
property, the helper assertion instead attempts to strengthen        This formula is the same design fact that can be used by
the target property temporarily. The verifier asks PDR to prove      the predicate and clause mechanisms, but it is consumed
                                   ^                                 differently when it works as a helper assertion. With helper
                       P⋆ = P ∧        a,                            predicates, (y−x) = 2 is only a candidate atom for MIC. With
                                   a∈V                               helper clauses, (y − x) = 2 must pass frame checks before
where V ⊆ Aext is the set of helper assertions that have             being inserted into F1 . With helper assertions, the verifier
not yet been invalidated. Since P ⋆ ⇒ P , proving the                therefore uses the candidate to form the augmented property
                                                                                                                                     10



P ⋆ = (x < y) ∧ ((y − x) = 2), so the property frame already         B. Arithmetic Benchmarks
exposes the arithmetic relation that explains why x < y holds.
                                                                        Across the suites, we compare against Pono [4] with the
    This direct augmentation is powerful but unsafe if used
                                                                     IC3bits engine (which uses the SMT-Switch backend to in-
blindly, because an LLM may propose a false assertion. We
                                                                     terface with the Bitwuzla SMT solver [19]), AVR [10] (the
therefore follow the counterexample-guided refinement pattern
                                                                     champion of the 2020’s HWMCC), and DreamMiner [16]
in Algorithm 5. Whenever the strengthened property produces
                                                                     (a recent reinforcement-learning-based property mining and
an unblockable bad cube c, the verifier first evaluates the orig-
                                                                     argumentation baseline). As LLM4PDR is built upon a cus-
inal property P on that cube (Line 8). If P itself is false, the
                                                                     tomized IC3 engine (IC3ng) that we implemented in Pono,
cube is a real counterexample and the design is unsafe. Oth-
                                                                     we also include an Ablation configuration that runs Pono with
erwise, the counterexample only shows that the current helper
                                                                     IC3ng but disables all LLM-generated helper artifacts. This
set was too strong. The verifier removes exactly the helper
                                                                     isolates the effect of the proposed guidance from the effect of
assertions falsified by c (Line 10), rebuilds P ⋆ from the re-
                                                                     changing the underlying PDR engine. We report three single-
maining helpers (Line 11), and restarts the ordinary PDR loop.
                                                                     mechanism instantiations of LLM4PDR: LLM2Predicate,
Figure 8 pictorially illustrates how invalid helper assertions are
                                                                     LLM2Clause, and LLM2Assert. They enable predicate
filtered without compromising the original proof obligation.
                                                                     generation, clause generation, and assertion generation, respec-
    For xp2, the assertion a∆ is true on all reachable states, so    tively, as described in Section IV. Runtimes are wall-clock
no refinement is needed. The strengthened property exposes           times; entries marked TO hit the timeout limits described in
the arithmetic reason behind x < y immediately, and the              the corresponding table notes.
proof can converge using the compact relation y − x = 2
                                                                        The arithmetic suite contains 33 micro-benchmarks whose
instead of rediscovering it through many bit-level CTIs. If the
                                                                     safety properties depend on word-level relationships among
LLM had proposed a wrong relation, such as y − x = 3, the
                                                                     datapath signals. These instances are intentionally small, but
first counterexample satisfying x < y but violating that helper
                                                                     difficult for engines that must rediscover arithmetic invariants
would simply delete the helper and continue with the original
                                                                     through bit-level generalization. They therefore provide a
property.
                                                                     focused test of whether LLM-generated helper artifacts can
    The soundness boundary is again kept inside the verifier.        expose the equalities, bounds, and guarded relations that PDR
Helper assertions are not added to the transition relation and       needs for compact inductive invariants.
are not trusted as assumptions. They are tentative property
                                                                        Figure 9 summarizes the result for this set of problems.
augmentations. If they help, they become part of a proof to the
                                                                     Pono and AVR solve 13 and 11 cases, respectively, while
target property; if they are contradicted by a counterexample,
                                                                     DreamMiner solves 19. All three LLM4PDR variants improve
they will be removed. In the worst case, all helper assertions
                                                                     on these baselines: LLM2Predicate and LLM2Clause
are filtered out and Algorithm 5 degenerates to ordinary PDR
                                                                     each solve 23 cases, and LLM2Assert solves 28. The cactus
working on the original property P .
                                                                     plot shows the same pattern in runtime. LLM2Assert solves
                                                                     the most instances and has the lowest curve over most of
              V. E XPERIMENTAL E VALUATION                           the solved range, while LLM2Predicate and LLM2Clause
                                                                     remain consistently below the deductive baselines. The arith-
A. Setup and Baselines                                               metic suite thus confirms that each helper-artifact interface
   We evaluate LLM4PDR on four benchmark suites that ex-             can strengthen word-level PDR, with assertion-guided search
ercise different sources of difficulty in word-level hardware        providing the largest gain when the generated helper facts align
model checking. The arithmetic suite isolates datapath-heavy         closely with the target property.
reasoning over additions, multiplications, shifts, and extracts.
The HWMCC suite contributes larger competition benchmarks
                                                                     C. HWMCC Benchmarks
with mixed control and datapath structure. The HLS–SEC suite
contains fixed-point Kalman-filter kernels generated by high-           To test larger designs, we selected twelve HWMCC in-
level synthesis, where the properties encode bit-exact equiva-       stances [20] spanning accelerators, embedded CPU cores,
lence between independently pipelined implementations. The           a DSP kernel, peripheral/storage controllers, and a video
open-source RTL suite contains formally annotated bus inter-         interface. This mix stresses both arithmetic datapaths and
connects and DDR3 controllers, representing realistic control-       control-dominated state machines. Table II reports the wall-
rich SoC components.                                                 clock runtime.
   For all LLM4PDR runs, we use OpenAI GPT o3 [18] as                   The accelerator family marlann_cp_* shows the benefit
the LLM backend. We use a fixed prompt template across all           of injecting helper artifacts into an already strong PDR engine.
benchmarks and do not perform benchmark-specific prompt              LLM2Assert is fastest on two of the three accelerator
tuning. For each benchmark instance and each guidance mode,          instances, and LLM2Clause is fastest on the third; both
the LLM is asked to generate up to five helper artifacts in          variants consistently improve over Pono, DreamMiner, and the
the restricted SMT-LIB2 helper format: five predicate.*              IC3ng ablation. The DSP instance intersymbol_conv is
declarations for LLM2Predicate, five clause.* declara-               more decisive: Pono, AVR, and DreamMiner time out, the
tions for LLM2Clause, or five assertion.* declarations               IC3ng ablation takes 613.64 s, and LLM2Predicate proves
for LLM2Assert.                                                      the property in 3.06 s. This case indicates that helper predicates
                                                                                                                                                                                11




                                          Fig. 9: Performance comparison on simple arithmetic benchmarks.

         TABLE II: Benchmark sizes and runtime comparison on HWMCC19–24 benchmarks. Runtimes are in seconds.a
                                                                                                                                             LLM2           LLM2            LLM2
Category                     Benchmark                     Sizee         Ponob         AVRc         Ablationd         DreamMiner          Predicate        Assert          Clause

                             marlann_cp_fail1_p2        693 / 1441       26.64       2083.95           25.55              25.63              23.94          13.50           21.48
Accelerator                  marlann_cp_fail2_p0        690 / 1441       23.23        315.02            6.92               9.07               6.46            8.39          6.20
                             marlann_cp_pass_p2         694 / 1441       26.58       2439.43           26.07              35.66              23.21          13.61           20.89

                             picorv32_p01                                 5.99         0.50                2.78           10.11               2.70               4.51         3.52
Embedded CPU core            picorv32_p05              1911 / 1878       18.00         0.64                4.32           17.55               4.21               9.83         5.90
                             picorv32_p06                                25.22         0.71                5.60           75.37               5.53               5.28         6.47

DSP / signal-estimation      intersymbol_conv            308 / 59          TO           TO            613.64              TO                3.06                29.80      3445.22

Peripheral / storage         qspiflash_p164             3100 / 614         TO        2553.76        1310.61               TO               1220.00         859.80            TO
ctrl.                        qspiflash_p078             3098 / 613         TO          TO            299.92               TO                 77.27         100.50           53.89

Display / video
                             vgasim_p89                2003 / 1010         TO         41.60           815.79              TO                110.05          471.30          757.15
interface

                             zipcpu_busdelay_p02        950 / 658          TO        1872.35        1279.06               TO               1243.78        2806.50            TO
Embedded CPU core
                             zipcpu_pfcache_p16        1818 / 3206         TO          3.27         1510.29               TO                359.62          19.20          2404.34
a
  TO: solver hit the time-out limit (≥ 1 h).
b
  Pono: results from the Pono model checker (IC3bits engine).
c
  AVR: best of SA and SA+UF.
d
  Ablation: results from the Pono model checker (IC3ng engine) without LLM assistance.
e
  Size: LoC / state bits. LoC: number of BTOR model records; State bits: total bits in all BTOR state declarations.



can supply a compact word-level explanation that the unguided                             TABLE III: HLS–SEC benchmark sizes and runtimes in
engine does not discover quickly.                                                         seconds.a
                                                                                          Case     Sizec      Pono     AVR        Abl.       DM       Pred.b     Assertb   Clauseb

                                                                                          K1       506/84     24.90     1.49     13.35       3.33      18.41      24.63     1.97
   The HWMCC results are heterogeneous, as expected for                                   K2      491/102     93.57    998.46   1217.89      6.47      20.45      24.64     25.01
competition benchmarks that mix accelerators, CPU cores,                                  K3                   TO       TO        TO       5275.60    9912.86    5112.58   3990.83
                                                                                                   424/83
                                                                                          K4                   TO       TO        TO       5366.69    9741.71    5184.17   3664.56
DSP kernels, storage controllers, and video interfaces, and                               a
                                                                                            K1–K4: Kalman1–4. TO: ≥ 3 h. Abl.: IC3ng without LLM assistance. DM:
therefore LLM guidance is not uniformly best on ev-                                       DreamMiner.
                                                                                          b
ery small instance; for example, AVR remains strong on                                    c
                                                                                            Pred./Assert/Clause: LLM2Predicate, LLM2Assert, and LLM2Clause.
                                                                                            Size: RTL LoC / state bits.
several picorv32 cases. However, the guided configu-
rations provide large gains on several harder instances.
On intersymbol_conv, Pono, AVR, and DreamMiner                                            D. HLS–SEC Safety Kernels
time out, the unguided IC3ng ablation takes 613.64 s,
while LLM2Predicate proves the property in 3.06 s.                                           The HLS–SEC benchmarks are fixed-point Kalman-filter
LLM2Assert and LLM2Clause also lead on different                                          kernels whose top-level wrappers assert equivalence between
qspiflash and zipcpu cases. These results indicate that                                   two independently pipelined implementations. Their multipli-
the proposed helper artifacts are complementary: predicates,                              ers, adders, shifts, and long pipeline dependencies make them
clauses, and assertions each benefit different structural classes                         a stress test for arithmetic-aware verification.
rather than acting as a single universally dominant heuristic.                               Table III shows a clear progression in difficulty. On
                                                                                                                                                         12



TABLE IV: Benchmark sizes and runtime comparison on open-source circuit designs with assertions. Runtimes are in seconds.a
                                                                                                                                  LLM2      LLM2      LLM2
Category                     Benchmark                     Sizeb             Pono          AVR         Ablation   dreamminer   Predicate   Assert    Clause

                             axil2axis                  1043 / 1802          79.18          TO          32.01        80.43      25.37       69.80     29.43
Bus interconnects,
                             wbm2axilite                 391 / 521            TO           2.58         47.01         TO         25.71       TO       36.15
bridges, etc.
                             axildouble                 1257 / 2448         149.25          TO         253.19       155.44      131.60     161.20    193.30

                             multiconfig_ecc                                436.71          TO         293.76       450.28      147.08     300.60    237.89
DDR3 Controller              singleconfig              4136 / 10130         443.23          TO         313.21       441.98      153.03     328.69    255.23
                             multiconfig_default                            600.87          TO         418.60       597.62      124.88     475.10    139.70
a
    TO: solver hit the time-out limit (≥ 1 h).
b
    Size: LoC / state bits. LoC: RTL source code lines; State bits: total bits in all BTOR state declarations.



Kalman1, AVR is fastest and LLM2Clause is close behind.
On Kalman2, DreamMiner achieves the best runtime, while
LLM2Predicate remains much faster than Pono, AVR,
and the ablation. The harder Kalman3 and Kalman4 cases
separate the approaches more clearly: Pono, AVR, and the
ablation time out, while the LLM4PDR variants complete the
proofs. Among our variants, LLM2Clause is fastest on both
hard kernels, completing them in about one hour. These results
suggest that side-loaded clauses are particularly effective for
deep HLS pipelines, where useful arithmetic relations can
be validated early and propagated through the PDR frame
sequence.

E. Open-Source RTL Designs with Assertions
   The open-source suite in Table IV contains two families of
real-world RTL designs. The WB2AXIP cases include fully
pipelined AXI4 and AXI-Lite bridges that allow multiple in-
flight transactions, creating deep handshake logic. The DDR3                                   Fig. 10: Execution-time scatter plot comparing Pono IC3bits
controller cases add rank-bank management, write levelling,                                    with Pono IC3ng without helper artifacts.
read calibration, and optional SEC–DED error correction,
yielding long control pipelines and wide datapaths. These
designs are formally annotated, and their properties are chal-                                 reducing bit-level literals, and eager propagation makes the
lenging for general-purpose model checkers.                                                    resulting lemmas available sooner in subsequent frames. To
   LLM2Predicate is the strongest configuration on this                                        establish that our speedups cannot be explained by these
suite. It obtains the best runtime on five out of six cases and                                engine changes alone, we disable all LLM-generated helpers
remains competitive on wbm2axilite, where AVR is ex-                                           while retaining the underlying IC3ng heuristics. Figure 10
ceptionally fast. On the AXI bridge cases, LLM2Predicate                                       compares this unguided configuration with IC3bits; the Ab-
outperforms Pono, the ablation, DreamMiner, and the other                                      lation columns in the tables compare it with LLM4PDR on the
LLM4PDR modes on axil2axis and axildouble; it also                                             same engine.
solves wbm2axilite while Pono and DreamMiner time out.                                            Without helpers, IC3ng does not consistently outperform
On the DDR3 controllers, AVR times out on all three cases,                                     IC3bits: Figure 10 shows both improvements and regressions.
whereas LLM2Predicate gives roughly 3–5× speedups                                              Thus, the added heuristics alone do not establish a gen-
over Pono and clear improvements over the IC3ng ablation.                                      eral performance advantage. Enabling helpers on the same
This pattern is consistent with the nature of these designs:                                   IC3ng engine yields substantial additional speedups on sev-
predicate guidance is well suited to repeated control/data                                     eral benchmarks; for example, LLM2Predicate reduces
relationships, such as handshake consistency and pipeline-state                                intersymbol_conv from 613.64 s to 3.06 s. These results
correspondence, that become useful during many MIC calls.                                      show that the engine changes alone cannot explain these
                                                                                               gains: the LLM-generated semantic information makes an
                                                                                               additional contribution when used together with the enhanced
F. Ablation: IC3bits vs. IC3ng
                                                                                               generalization and propagation procedures.
  To better exploit LLM-generated helpers, we use IC3ng,
which extends IC3bits with the D OWN/MIC-style inductive
                                                                                                                       VI. C ONCLUSION
generalization [1] and eager lemma propagation during block-
ing, following the rationale of aggressive clause pushing [21].                                  This paper presents LLM4PDR, a framework for injecting
These mechanisms support helper-guided proof search: the                                       LLM-generated semantic guidance into PDR-based hardware
generalizer is extended to retain word-level helpers while                                     model checking. The key idea is to keep the LLM outside
                                                                                                                                                             13



the soundness boundary: it proposes predicates, clauses, and                     [14] H. Zhang, A. Gupta, and S. Malik, “Syntax-guided synthesis for lemma
helper assertions, while the verifier parses, type-checks, vali-                      generation in hardware model checking,” in International Conference
                                                                                      on Verification, Model Checking, and Abstract Interpretation. Springer,
dates, and refines those artifacts through ordinary PDR proof                         2021, pp. 325–349.
obligations. This lets the engine benefit from high-level word-                  [15] K. L. McMillan, “Interpolation and SAT-based model checking,” in
level relations without trusting the LLM as an oracle.                                International Conference on Computer Aided Verification. Springer,
                                                                                      2003, pp. 1–13.
   Across arithmetic, HWMCC, HLS–SEC, and open-source                            [16] Z. Yan and H. Zhang, “Word-level augmentation of formal proof by
RTL benchmarks, the three LLM4PDR modes improve differ-                               learning from simulation traces,” in Proceedings of the 43rd IEEE/ACM
ent parts of the proof search. Assertion guidance is strongest                        International Conference on Computer-Aided Design, 2024, pp. 1–9.
                                                                                 [17] G. Hu, J. Tang, C. Yu, W. Zhang, and H. Zhang, “DeepIC3: Guiding IC3
on the arithmetic suite, clause guidance is especially effective                      algorithms by graph neural network clause prediction,” in 2024 29th Asia
on deep HLS pipelines, and predicate guidance performs best                           and South Pacific Design Automation Conference (ASP-DAC). IEEE,
on open-source control-plus-datapath designs. The ablation                            2024, pp. 262–268.
                                                                                 [18] OpenAI, “OpenAI o3,” OpenAI API Documentation, 2025, accessed:
against unguided IC3ng further shows that these gains come                            2026-05-27.
from the generated helper artifacts rather than from an en-                      [19] A. Niemetz and M. Preiner, “Bitwuzla,” in International Conference on
gine swap alone. These results indicate that LLM-generated                            Computer Aided Verification. Springer, 2023, pp. 3–17.
                                                                                 [20] A. Biere, N. Froleyks, and M. Preiner, “Hardware model checking
semantic hints can be a practical and sound complement to                             competition 2024,” in Proceedings of the 24th Conference on Formal
conventional PDR generalization.                                                      Methods in Computer-Aided Design–FMCAD 2024. TU Wien Aca-
                                                                                      demic Press, 2024, pp. 7–7.
                                                                                 [21] A. Ivrii and A. Gurfinkel, “Pushing to the top,” in 2015 Formal Methods
                        ACKNOWLEDGMENTS                                               in Computer-Aided Design (FMCAD). IEEE, 2015, pp. 65–72.
                                                                                 [22] M. Mann, A. Wilson, Y. Zohar, L. Stuntz, A. Irfan, K. Brown,
   The authors used Gemini 3.8 Flash only to improve the                              C. Donovick, A. Guman, C. Tinelli, and C. Barrett, “SMT-Switch: a
language and readability of the manuscript text. It was not used                      solver-agnostic C++ API for SMT solving,” in International Conference
                                                                                      on Theory and Applications of Satisfiability Testing. Springer, 2021,
to generate technical ideas, results and figures. All suggested                       pp. 377–386.
revisions were reviewed and verified by the authors, who take
full responsibility for the final content.                                                                Guangyu Hu received the B.E. degree in soft-
                                                                                                          ware engineering from Xiamen University, Xiamen,
                                                                                                          China, in 2021.
                              R EFERENCES                                                                    He received his PhD degree in Microelectron-
 [1] A. R. Bradley, “SAT-based model checking without unrolling,” in                                      ics, Individualized Interdisciplinary Program (IIP) of
     International Workshop on Verification, Model Checking, and Abstract                                 Hong Kong University of Science and Technology,
     Interpretation. Springer, 2011, pp. 70–87.                                                           Clear Water Bay, Hong Kong SAR. His research
 [2] A. Niemetz, M. Preiner, C. Wolf, and A. Biere, “Btor2, BtorMC                                        interests include hardware model checking and logic
     and Boolector 3.0,” in International Conference on Computer Aided                                    synthesis.
     Verification. Springer, 2018, pp. 587–595.
 [3] C. Barrett, A. Stump, and C. Tinelli, “The SMT-LIB standard – version
     2.0,” in Proceedings of the 8th International Workshop on Satisfiability
     Modulo Theories (SMT ’10), Jul. 2010, edinburgh, Scotland. [Online].                                  Mingkai Miao received the B.Eng. degree in elec-
     Available: http://theory.stanford.edu/~barrett/pubs/BST10.pdf                                         tronic and information engineering from the Uni-
 [4] M. Mann, A. Irfan, F. Lonsing, Y. Yang, H. Zhang, K. Brown, A. Gupta,                                 versity of Electronic Science and Technology of
     and C. Barrett, “Pono: a flexible and extensible SMT-based model                                      China, Chengdu, China, in 2021, and the M.Eng.
     checker,” in International Conference on Computer Aided Verification.                                 degree in electrical and computer engineering from
     Springer, 2021, pp. 461–474.                                                                          the University of Illinois Urbana-Champaign, Ur-
 [5] N. Eén, A. Mishchenko, and R. Brayton, “Efficient implementation of                                   bana, IL, USA, in 2024. He is currently pursu-
     property directed reachability,” in 2011 Formal Methods in Computer-                                  ing the Ph.D. degree in microelectronics with the
     Aided Design (FMCAD). IEEE, 2011, pp. 125–134.                                                        Hong Kong University of Science and Technology
 [6] A. R. Bradley and Z. Manna, “Checking safety by inductive generaliza-                                 (Guangzhou), Guangzhou, China. His research inter-
     tion of counterexamples to induction,” in Formal Methods in Computer                                  ests include hardware formal verification, IC3/PDR
     Aided Design (FMCAD’07). IEEE, 2007, pp. 173–180.                           model checking, and machine learning and large language model techniques
 [7] Z. Hassan, A. R. Bradley, and F. Somenzi, “Better generalization in IC3,”   for electronic design automation.
     in 2013 Formal Methods in Computer-Aided Design. IEEE, 2013, pp.
     157–164.
 [8] A. Griggio and M. Roveri, “Comparing different variants of the                                       Zhiyuan Yan received the B.Sc. degree in Elec-
     IC3 algorithm for hardware model checking,” IEEE Transactions on                                     tronic Information Science and Technology from
     Computer-Aided Design of Integrated Circuits and Systems, vol. 35,                                   Henan University, Kaifeng, China, in 2020, and the
     no. 6, pp. 1026–1039, 2016.                                                                          master’s degree in Microelectronics from Nanyang
 [9] A. Luka and Y. Vizel, “Property directed reachability with extended                                  Technological University, Singapore, in 2022. He
     resolution,” in International Conference on Computer Aided Verification.                             is currently pursuing the Ph.D. degree with the
     Springer, 2025, pp. 258–280.                                                                         Microelectronics Thrust, Hong Kong University of
[10] A. Goel and K. Sakallah, “AVR: Abstractly verifying reachability,” in                                Science and Technology (Guangzhou), Guangzhou,
     International Conference on Tools and Algorithms for the Construction                                China, advised by Prof. Hongce Zhang. His research
     and Analysis of Systems. Springer, 2020, pp. 413–422.                                                lies in AI for EDA, especially machine learning-
[11] R. Brayton and A. Mishchenko, “ABC: An academic industrial-strength                                  guided formal verification and SAT.
     verification tool,” in International Conference on Computer Aided Ver-
     ification. Springer, 2010, pp. 24–40.
[12] Y. Su, Q. Yang, Y. Ci, T. Bu, and Z. Huang, “The rIC3 hardware model
     checker,” in International Conference on Computer Aided Verification.
     Springer, 2025, pp. 185–199.
[13] A. Goel and K. Sakallah, “Model checking of Verilog RTL using IC3
     with syntax-guided abstraction,” in NASA Formal Methods Symposium.
     Springer, 2019, pp. 166–185.
                                                                                14



                         Xiaofeng Zhou received the B.Eng. degree in in-
                         formation science and engineering from Southeast
                         University, Nanjing, China, in 2020, and the Ph.D.
                         degree in electronic and computer engineering from
                         The Hong Kong University of Science and Technol-
                         ogy, Hong Kong, in 2026. His research interests in-
                         clude hardware formal verification, model checking,
                         high-level synthesis, and FPGA-based acceleration.



                        Wei Zhang (Fellow, IEEE) received the Ph.D. de-
                        gree from Princeton University, Princeton, NJ, USA,
                        in 2009.
                           She was an Assistant Professor with the School
                        of Computer Engineering, Nanyang Technological
                        University, Singapore, from 2010 to 2013. She
                        joined The Hong Kong University of Science and
                        Technology, Hong Kong, in 2013, where she is
                        currently a Professor and she established the Re-
                        configurable Computing System Laboratory. Her
                        research interests include reconfigurable systems,
field-programmable gate array-based design, low-power high-performance
multicore systems, electronic design automation, embedded systems, and
emerging technologies.

                       Hongce Zhang (Member, IEEE) received the B.S.
                       degree in microelectronics from Shanghai Jiao Tong
                       University, Shanghai, China, in 2015, and the Ph.D.
                       degree from the Electrical and Computer Engineer-
                       ing Department of Princeton University, NJ, USA,
                       in 2021.
                          He is currently an Assistant Professor with the Mi-
                       croelectronics Thrust, Function Hub of Hong Kong
                       University of Science and Technology (Guangzhou),
                       Guangzhou, China, and is also affiliated with the Di-
                       vision of Emerging Interdisciplinary Areas (EMIA)
of the Hong Kong University of Science and Technology, Clear Water Bay,
Hong Kong SAR. His research interests include formal verification and
hardware model checking.
