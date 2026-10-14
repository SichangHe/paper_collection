                                              ProsaBuddy: Assisting Mechanized Real-Time
                                             Schedulability Analysis with LLM-based Agents
                                                           Junyi Liu1,2 , Tianchi Ren1 , Fei Guan3 , Xu Jiang4 , Zhe Jiang5 , Wang Yi6 , Nan Guan1
                                                       1
                                                        City University of Hong Kong, 2 Northeastern University (China), 3 Northeast Forestry University,
                                                    4
                                                      University of Electronic Science and Technology of China, 5 Southeast University, 6 Uppsala University


                                           Abstract—Rigorous schedulability analysis is essential for the   time-consuming. Although Prosa has features that enhance its
                                        design of hard real-time systems, yet errors in pen-and-paper       accessibility to real-time systems researchers, such as prioritiz-
                                        proofs threaten the safety of critical applications. The Prosa      ing readability and adhering to established proof conventions
                                        initiative addresses this by offering a foundation for building
arXiv:2610.03796v1 [cs.LO] 1 Oct 2026




                                        machine-checkable schedulability analysis proofs in the Rocq        within the community, the overhead of proof development
                                        proof assistant. However, the substantial time and expertise re-    remains substantial. According to our own experience, proving
                                        quired to construct such proofs remain a major barrier for wider    lemmas in a real-time scheduling paper in Rocq based on
                                        adoption of Prosa. This work presents ProsaBuddy, an LLM-           Prosa may require several weeks, even for those with moderate
                                        based agent system designed to lower the effort needed to develop   familiarity with Prosa and Rocq. For newcomers without
                                        mechanized real-time schedulability proofs. ProsaBuddy employs
                                        a ReAct loop with retrieval over the Prosa codebase, access to      prior experience, it is even more demanding. This substantial
                                        Rocq tools and optional human-written hints. It uses a subgoal-     effort is likely a primary factor discouraging researchers from
                                        delegation architecture, decomposing a lemma into subgoals and      adopting the Prosa approach in their own work.
                                        dispatches them to subagents for proof. We evaluate ProsaBuddy         In this work, we present ProsaBuddy, an LLM-based agent
                                        on a mini benchmark drawn from real-time scheduling literature.     system designed to lower the effort barrier to adopting the
                                        Experiment results show that ProsaBuddy significantly outper-
                                        forms state-of-the-art LLM-based Rocq automated proving agent       Prosa approach for developing mechanized schedulability
                                        systems and a general coding agent OpenCode.                        proofs. While LLMs have demonstrated impressive automated
                                                                                                            theorem proving capabilities in domains such as pure math-
                                                                I. I NTRODUCTION                            ematics, their application to theorem proving in real-time
                                           In hard real-time systems, rigorous real-time performance        scheduling remains entirely unexplored. Although real-time
                                        analysis is essential to guarantee the system’s timing behav-       scheduling lemmas can broadly be regarded as mathematical
                                        ior to consistently meet specified constraints. Researchers in      problems, they exhibit unique features that make them signifi-
                                        this field typically develop schedulability analysis theorems       cantly more challenging to formalize and prove automatically
                                        that provide efficient methods for evaluating real-time perfor-     than the pure-math problems in standard automated theorem
                                        mance. The development of such analyses has traditionally           proving benchmarks, as will be discussed in Section III-A.
                                        relied on human effort and has been conducted in a pen-and-            We build ProsaBuddy as an agent system that relies on
                                        paper manner. However, numerous recent reports have revealed        inference-time scaling through an intensive ReAct (Reasoning
                                        errors in schedulability analyses documented in literatures [1]–    & Acting) loop [7]. It combines retrieval over the Prosa
                                        [4]. Since real-time systems underpin safety-critical applica-      codebase to supply necessary definitions and proof patterns,
                                        tions, such analysis errors can lead to disastrous consequences.    access to various Rocq tools which provide rich feedback in-
                                           Prosa [5] is an initiative that aims to fundamentally ad-        formation, and optional human-written proof hints that provide
                                        dress this problem. Prosa provides a repository of definitions      high-level guidance. ProsaBuddy adopts a subgoal-delegation
                                        and proofs for mechanized (i.e., machine-checkable) real-time       architecture: a primary agent decomposes the lemma into
                                        schedulability analysis. It is built and verified using Rocq        smaller subgoals and dispatches them to subagents, each
                                        (formerly known as Coq) [6], a mature interactive theorem           receiving a structured task bundle that includes the subgoal,
                                        prover. Prosa builds dedicated infrastructure and methodolog-       context, and a proof state snapshot. We enhance the agents
                                        ical frameworks to enable detailed, reliable, yet readable real-    with decomposition guidelines and domain-specific proving
                                        time schedulability analysis. Widespread adoption of the Prosa      skills, improving their ability to navigate the deep proof chains.
                                        approach within the real-time systems research community               We conducted experiments to evaluate the performance of
                                        would significantly elevate the rigor, credibility, and founda-     ProsaBuddy, comparing it with state-of-the-art LLM-based
                                        tional robustness of theoretical developments in the field.         Rocq automated theorem proving systems, as well as a
                                                                                                            general-purpose coding agent OpenCode [8]. The comparison
                                           Despite its potential, a practical barrier prevents Prosa from
                                                                                                            is conducted on a mini-benchmark of 24 lemmas that we built
                                        achieving broader adoption: developing proofs in Rocq is very
                                                                                                            from the real-time scheduling literature; none of them appear
                                          Junyi Liu and Tianchi Ren contributed equally to this work.       in the existing Prosa library. Experimental results show that
                                        Corresponding author: Nan Guan <nanguan@cityu.edu.hk>               ProsaBuddy significantly outperforms all competing systems.
We further extend the evaluation to a larger set of lemmas          1   Context {Job: eqType}.
taken directly from the Prosa library, and the results confirm      2   Variable job_arrival: Job → time.
                                                                    3   Variable job_cost: Job → time.
the superiority of ProsaBuddy. Ablation studies reveal that         4   Variable sched: schedule Job.
                                                                    5   Context {Task: eqType}.
these gains arise from the combined effect of several design        6   Variable job_task: Job → Task.
                                                                    7   Definition scheduled_at (j: Job) (t: time) := sched t == Some j.
choices in ProsaBuddy. Additionally, we assess the impact of        8   Definition service (j: Job) (t: time) :=
different backbone LLMs on the performance of ProsaBuddy.           9   \sum_(0 <= t’ < t) scheduled_at j t’.
                                                                   10   Definition completed_by (j: Job) (t: time) :=
   Overall, ProsaBuddy successfully proves non-trivial schedu-     11           job_cost j <= service j t.
                                                                   12   Hypothesis H_service_leq_job_cost:
lability analysis lemmas, including some whose Rocq proofs         13     forall j t, service j t <= job_cost j.
require hundreds of tactics. Nevertheless, we do not currently     14
                                                                   15
                                                                        Lemma scheduled_implies_not_completed:
                                                                          forall j t, scheduled_at j t → ˜˜ completed_by j t.
position ProsaBuddy as a replacement for human researchers         16   Proof.
                                                                   17     move => j t.
or as capable of proving such lemmas entirely independently.       18     rewrite /completed_by. move=> H_sched. rewrite -ltnNge.
                                                                   19     have H_comp := H_service_leq_job_cost j (t + 1).
Instead, ProsaBuddy is designed to liberate researchers from       20     rewrite /service in H_comp. rewrite addn1 in H_comp.
the tedious low-level details of lengthy Rocq proofs, saving       21     rewrite big_nat_recr //= in H_comp.
                                                                   22     rewrite H_sched /= in H_comp. rewrite /service.
them time to focus on developing high-level proof ideas.           23     by rewrite addn1 in H_comp.
                                                                   24   Qed.
However, given the rapid development of LLMs, a vast open
space remains for exploring whether ProsaBuddy could, in the
future, assist real-time scheduling research in more advanced           Fig. 1. Example of a simple schedulability analysis lemma in Rocq
ways, for instance, by independently proving open problems
or even automatically developing new theories.
                                                                   B. Prosa
          II. BACKGROUND AND R ELATED W ORK                           Prosa [5] is a Rocq-based foundation for verified real-
A. Rocq                                                            time scheduling theory. It emphasizes readable specifications,
   Rocq (formerly known as Coq) is a proof assistant based on      explicit assumptions, and proof reuse. Following the SS-
dependent type theory, allowing users to write mathematical        Reflect methodology [10], Prosa encodes its specifications
definitions, executable algorithms, and prove properties about     as computable boolean predicates, which effectively enables
them interactively. Following the project’s renaming, we will      proof automation via reflection. This clarity also makes Prosa
refer to Rocq exclusively when introducing ProsaBuddy. One         well-suited for LLM-based proof automation, as its good
key difference between human-written and Rocq proofs is the        readability is informative not only to human users but also
level of detail: a simple intuition often requires many explicit   to LLM. Prosa has been extended to verified scheduling
steps. For example, in the example of Figure 1, the lemma          infrastructure in several directions in follow-up work, e.g.,
states that a job scheduled at time t cannot be completed by t.    sustainability theory and weak sustainability [11], Abstract
For humans, this is trivial. In Rocq, however, the proof needs     Response-Time Analysis (ARTA) based on the busy-window
many steps. So developing Rocq proofs is effort-demanding.         principle [12], FIFO response-time analysis with arbitrary
   Rocq does not draw a fundamental distinction between            deadlines and arrival curves [13], and connections between
Lemma, Theorem, Fact, or similar keywords – they all               response-time analysis and network calculus [14]. Further-
introduce a goal to be proved. In this paper, we will use the      more, Prosa serves as the certificate generator for POET [15],
term lemma uniformly for any such goal to prove, regardless of     the first foundational response-time analysis tool that produces
which keyword was used in its declaration. A lemma statement       fully machine-checkable Coq/Rocq certificates. Another re-
in Rocq typically introduces variables, definitions, hypotheses,   cent work integrates Prosa with RefinedC [16], connecting
and a lemma statement. The proof is enclosed by Proof.             Prosa’s verified response-time analysis with C implementa-
and Qed., and the user guides the proof by applying tactics,       tion verification, thereby enabling end-to-end certification of
which are commands that transform the current proof state          interrupt-free real-time schedulers implemented in low-level
(e.g., those marked in blue in Figure 1). Rocq provides a          code. Together, these works make Prosa a useful infrastructure
rich set of tactics, ranging from basic, primitive tactics that    for verified real-time systems. Nevertheless, Prosa currently
manipulate the proof state directly (e.g., move, rewrite,          focuses on a core subset of real-time scheduling theory.
apply, exact) to powerful automation tactics that can
search for proofs or solve decidable fragments automatically       C. Automated Theorem Proving
(e.g., auto, eauto, lia, ring).                                       Mechanized proofs are inherently hard to construct. Before
   In the presentation of this paper, we deliberately minimize     the emergence of LLMs, many efforts sought to improve au-
the reader’s dependence on understanding the syntax and            tomation for different theorem provers, for instance, via pow-
semantics of Rocq. Our goal is to let readers who are not          erful tactics that search for proofs or solve decidable fragments
familiar with Rocq still grasp the key ideas, even if they skip    automatically. For Coq/Rocq, SSReflect [10], Mathematical
some details. For some places that are key to understanding        Components [17] and CoqEAL [18] enable reuse of recurring
our methodology, we will introduce some tactics locally. For a     proof patterns through reflection and proof-oriented compu-
comprehensive introduction to tactics mentioned in this paper,     tation; SMTCoq [19], smt4coq [20] and CoqHammer [21]
we refer the reader to the Rocq reference manual [9].              connect Rocq goals to external solvers and reconstruct their
                          TABLE I                                   combines proof-tree context, Rocq feedback, and previous
  LLM- BASED AUTOMATED C OQ /ROCQ THEOREM PROVING SYSTEMS           proof attempts for software verification. Table I lists existing
                                                                    LLM-based automated Coq/Rocq theorem proving systems.
              Name        Source Year Prover Availability
                                                                       Overall, this body of work shows a shift from isolated
            CoqPilot       [32]   2024   Coq      Yes               tactic prediction to systems combining proof synthesis, re-
             PALM          [33]   2024   Coq      Yes
             COPRA         [34]   2024   Coq      Yes               trieval, prover feedback, repair and agentic control. However,
             Liu etc.      [35]   2024   Coq      No                proofs in real-time scheduling often rely on recurring semantic
             Lu etc.       [36]   2025   Coq      No
              Rango        [37]   2025   Coq      Yes               structures, including scheduling assumptions, workload and
             ADAPT         [38]   2025   Coq      No                processor models, invariants, response-time bounds, rewriting
            RocqStar       [39]   2026   Rocq     Yes               conventions, and sequences of lemmas. Existing methods treat
           Cobblestone     [40]   2026   Coq      Yes
            AutoRocq       [41]   2026   Rocq     Yes               reusable knowledge as retrieved premises, similar proofs, or
          ReCent-Prover    [42]   2026   Rocq     No                short-term proof-state contexts. They do not make domain-
            QUARRY         [43]   2026   Rocq     No
                                                                    specific proof procedures explicit as reusable skills with appli-
                                                                    cability conditions, required assumptions, expected effects and
                                                                    adaptation strategies. This leaves a gap between general LLM-
proofs inside the kernel; Ltac/Ltac2 [22], Mtac/Mtac2 [23],         based proof generation and domain-aware proof automation.
[24], Coq-Elpi [25] and MetaCoq [26] support domain-specific
tactics and reusable proof infrastructure. ML4PG [27], Coq-                               III. P ROSA B UDDY
Gym [28], Tactician [29], Proverbot9001 [30], TacTok [31]           A. Overview
and ASTactic [28] explored proof-pattern mining, tactic pre-           Before presenting our approach, we first discuss the major
diction, local proof search, and proof-step prediction. These       differences between the problem tackled in this paper, auto-
techniques substantially reduce routine proof effort, but they      mated theorem proving for real-time schedulability analysis,
do not fully eliminate the high demand for expert intervention.     and the more commonly studied application of LLM-based
Large mechanized developments still require experts to de-          automated theorem proving to pure mathematics.
compose complex goals, formulate auxiliary lemmas, choose              The theorem-proving capability of LLMs is obtained via
suitable abstractions, and coordinate induction arguments.          pre-training on large-scale corpora such as Mathlib [60]. In
   LLMs have recently been used for automated theorem               contrast, public data for mechanized schedulability analysis is
proving across several proof assistants. Existing work has been     very limited. The Prosa library is the main available resource,
done for different theorem provers, including Coq/Rocq [32]–        but its volume is orders of magnitude smaller than the cor-
[34], [37], [39], [42], Lean [44]–[54] and Isabelle/HOL [55]–       pora for mathematics. This scarcity fundamentally constrains
[57]. In the following, we focus on the work for Coq/Rocq,          the ability of LLMs to learn proof patterns specific to the
and refer to recent survey papers [58], [59] for a more             schedulability analysis domain.
comprehensive overview of the field. CoqPilot [32] provides            The schedulability analysis lemmas are substantially more
a Coq-oriented assistant implemented as a VS Code exten-            complex than those found in mathematics benchmarks. They
sion, where users mark proof holes with admit, configure            are built upon a complex hierarchy of concepts, requiring
completion services, and invoke the tool inside an open Coq         many intricate definitions that often recursively depend on one
file to generate, check, and substitute candidate proofs through    another across multiple levels, along with numerous hypothe-
coq-lsp during interactive editing. COPRA [34] formulates           ses. For example, in the PutnamBench suite [61] for evaluating
proof search as an in-context interactive process where the         LLM-based mathematics theorem proving, the description
model proposes tactics and observes proof-state feedback.           of a lemma spans no more than 20 lines. In contrast, the
PALM [33] uses a generate-then-repair architecture to analyze       complete description of a schedulability analysis lemma in
and repair low-level proof errors. More recent systems com-         Prosa, including all definitions, variables, assumptions, and
bine proof generation with retrieval and multi-step interaction.    the lemma itself, often extends to several hundred lines. This
Rango [37] retrieves relevant premises and similar proofs           increased length and conceptual depth impose a significantly
from the current Coq project. RocqStar [39] and ReCent-             heavier burden on LLM’s context handling and reasoning
Prover [42] further introduce planning, reflection, and strategy-   capabilities. Beyond the complexity of individual lemmas,
aware retrieval into Rocq proof generation. Recent systems          Prosa has a highly structured architecture that promotes lemma
also enrich proof context and refine failed proof attempts. Lu      reuse across different task models. Whether an existing lemma
et al. [36] use selective concept unfolding and separate proof      can be applied to prove a target lemma depends on whether its
planning from tactic generation. Liu et al. [35] explain terms      preconditions hold, and those preconditions, in turn, rely on
in proof obligations and repair incomplete tactic parameters.       further preconditions, ultimately tracing back to the specific
ADAPT [38] selects among different refinement strategies            assumptions of the task model under consideration. This
after a failed proof attempt. QUARRY [43] ranks candidate           unique feature has introduced extra difficulty in the proving.
sublemma decompositions by their estimated CoqHammer                We will further elaborate on this point in Section III-C.
solvability. Cobblestone [40] retains Coq-accepted subproofs           To address the above challenges, ProsaBuddy adopts several
and recursively processes failed parts, while AutoRocq [41]         complementary strategies. First, because pre-training cannot
supply sufficient domain knowledge, we rely on inference-                  Lemma in Rocq
                                                                                                     Human-written
                                                                                                                               Proof in Rocq
                                                                                                      Proof Hints
time scaling: the LLM repeatedly attempts the proof, using
feedback from external tools. Second, we leverage the existing
Prosa library to retrieve relevant definitions and lemmas, and
                                                                                                             Subagent     Prosa Codebase
to learn proving techniques by imitating how Prosa handles
similar problems. This demands a powerful retrieval capability                                               Subagent     External Tools
capable of accurately locating useful information within Prosa.              Primary Agent
Third, we incorporate optional human-provided proof hints,                                                                Proving Skills

which help the agent navigate deep proof chains that would                  Decomposition
                                                                             Guidelines                      Subagent         Auditing
otherwise be difficult to resolve automatically.
   For these considerations, we build ProsaBuddy on top of
OpenCode [8] rather than constructing an agent system from
                                                                                             Fig. 2. Overview of ProsaBuddy
scratch. OpenCode provides a solid foundation that satisfies
the requirements outlined above. In OpenCode, an agent
follows an iterative ReAct (Reasoning & Acting) loop [7]:
it queries the LLM, uses the reasoning in the model’s output
to execute external tools, and then appends the feedback to
the conversation context for the next query, repeating this
process until the task is resolved. OpenCode offers powerful
code search capabilities well-suited for retrieval over the Prosa
library and allows users to inject human-written proof hints
into the agent’s prompt easily. By building on OpenCode, we
inherit a mature agent foundation and can focus our efforts             Fig. 3. An example of the decomposition-based proving procedure
on developing high-level capabilities tailored to the needs of
schedulability analysis lemma proving.
   Figure 2 shows the major components of ProsaBuddy. The            to be proven by itself; if so, it attempts to complete the proof
system takes as input a lemma formalized in Rocq, along with         directly. If the lemma is complex, it performs lemma decom-
optional human-written proof hints. The output is a verified         position, i.e., breaks the target lemma into several subgoals.
proof in Rocq, or a failure declaration. For proof construction,     Each subgoal is then delegated to a subagent for proof. After
ProsaBuddy uses LLM-based agents in a subgoal-delegation             launching a subagent, the primary agent suspends and waits for
architecture. The primary agent decomposes the lemma into            that subagent to return. The subagent returns to the primary
smaller, independent subgoals and dispatches them to special-        agent with either a success or a failure, accompanied by a
ized subagents. The subagent leverages OpenCode’s existing           failure report that explains why it failed and what important
infrastructure, which already supports launching subagents.          piece of information is missing for it to complete the proof of
When launching a subagent, the system does not simply                that subgoal. Upon receiving a failure return from a subagent,
forward the original prompt. Instead, it builds a structured         the primary agent attempts to refine the decomposition. When
task bundle that includes the subgoal to prove, the necessary        the primary agent refines the decomposition, all subgoals
context, and a snapshot of the current proof state, for the          that have already been proved will be kept. Figure 3 shows
subagent to solve the assigned subgoal independently. We             an illustrative example of the proving process. The primary
detail the lemma decomposition process in Section III-B. The         agent first decomposes the target lemma into two subgoals,
agents retrieve relevant information from the Prosa codebase         A and B. The subagent proving A returns with a success,
using OpenCode’s standard file-reading and code-search tools,        but the one proving B returns with a failure. The primary
such as file browsing and grep-like search. Beyond these             agent then analyzes the failed subgoal, redo the decomposition,
standard capabilities, we enable ProsaBuddy to invoke Rocq           further divides subgoal B into smaller subgoals C and D, and
tools directly to get rich feedback information for its ReAct        dispatches them to subagents for proof. Once both C and D
loop. We elaborate on these external tools in Section III-D.         are successfully proved, the primary agent performs a final
We also equip the agents with a collection of proving skills         recheck to ensure that all generated proofs returned from the
that target common challenges in the proving procedure, which        subagents compose into a valid proof of the original lemma.
will be elaborated in Section III-C. Last but not least, the proof      The decomposition by the primary agent is mechanically
submitted by the agents must go through auditing before it is        checked for structural correctness: it guarantees that the orig-
finally accepted as a valid proof of the target lemma, which         inal lemma follows from the conjunction of the subgoals.
will be introduced in Section III-E.                                 Concretely, the agent constructs a proof skeleton in which
                                                                     each subgoal is replaced by admit, and then verifies that
B. Lemma Decomposition                                               this proof is accepted by the Rocq compiler, as illustrated in
   The proving process starts with the primary agent, which          Figure 4. Nested decomposition is permitted (e.g., introducing
first decides whether the lemma to be proved is simple enough        a have tactic within another have, provided it reflects a
                                                                              TABLE II
                                                               S UMMARY OF D ECOMPOSITION G UIDELINES

       Name                                                                              Brief Description

     Reshaping   If an expression is mathematically useful but its exact form does not match what a downstream lemma requires, we should create a subgoal dedicated to
                 reshaping the expression into the exact needed form. Example: If the context contains size (filter P xs) ≤ 1, a useful subgoal is to reshape it into
                 count P xs ≤ 1, so that a counting lemma can be applied directly.

 Witnessing      An object may already be known to exist, but it is still hidden inside an existential statement or an informal paper description. Then the proof should create a
                 subgoal to make that object explicit and record the facts that come with it before using it in later steps. Example: When the context contains an existential fact
                 about a job arriving in an interval I and belonging to task tsk, a useful subgoal is to extract a concrete witness j together with facts such as arrives_in
                 j I and job_task j = tsk.

     Library     Prosa, MathComp, or local lemma may already be the right tool, but the current proof state is not ready for applying it. Then the proof should create a subgoal
     Matching    dedicated to preparing that lemma application: specializing general hypotheses to the current case, and writing out the required premises as explicit subgoals to
                 be proved. Example: Suppose a Prosa lemma can prove the desired conclusion once it is given premises such as job_task j = tsk and arrives_in j
                 I. A useful low-level decomposition is to create separate subgoals for these premises, prove them first, and then apply the library lemma directly.

      Case       A proof may need to be split into cases, but each branch should not be packed into one big proof region. Then the proof should create a subgoal to make the
     Splitting   case split explicit: write out the branch condition, and leave the rest of the branch proof to later subgoals. Example: We already know that the next step depends
                 on whether a job j belongs to the set of jobs arriving in interval I, but we should have a subgoal dedicated to splitting j ∈ jobs_arrived_during I, so
                 that one branch explicitly carries the fact j ∈ jobs_arrived_during I, and the other branch explicitly carries the fact j ∈        / jobs_arrived_during
                 I. Then the latter proof can handle the two branches separately, instead of hiding the whole case analysis inside one large proof step.

      Lifting    When a goal concerns an set (e.g., counting, cardinality, or aggregation) but only per-element implications are available, introduce a subgoal to lift them to the
                 set level. Example: If each job j that receives service in an interval I must have arrived before the end of I, a useful subgoal is to lift this fact to a counting
                 inequality: count (fun j => receives_service_in I j) jobs ≤ count (fun j => arrived_before (end_of I) j) jobs.




 1     Lemma T (a b c d e : nat) :                                                          thus the resulting subgoals are difficult for the subagent to
 2
 3
         a + c <= b + d.
       Proof.
                                                                                            prove. To solve this problem, we further augment the agent
 4       have H1 : a <= b.                                                                  with extra guiding principles that are extracted manually from
 5       {
 6         have S1 : a <= e.                                                                our experience in using Rocq for theorem proving. These
 7         { admit. }
 8         have S2 : e <= b.
                                                                                            principles provide instructions tailored to situations where low-
 9         { admit. }                                                                       level decomposition is effective (summarized in Table II).
10         exact: leq_trans S1 S2.
11       }                                                                                  Specifically, they target highly localized sub-problems that are
12       have H2 : c <= d.
13       { admit. }                                                                         largely independent of the surrounding proof, making them
14
15
         exact: leq_add H1 H2.
       Admitted.
                                                                                            ideal for a subagent to solve in a clean, isolated context. The
                                                                                            guiding principles are embedded in the main agent’s prompt.
                                                                                            The full prompt is considerably more detailed, and Table II
       Fig. 4. An example of the proof script for lemma decomposition
                                                                                            gives only a brief overview.
                                                                                            C. Proving Skills
genuine sub-step or a structural refinement of the reasoning).                                 We develop proving skills to enhance the subagent’s ability
Intermediate subgoals (those that are further decomposed) are                               to prove delegated subgoals. These skills are generated by us-
not delegated to subagents; only terminal subgoals (those that                              ing the LLM to analyze the proving traces, using the following
are not further decomposed) are delegated to subagents for                                  process. First, we select 65 lemmas from Prosa (only a small
proof. In Figure 4, the original lemma T is decomposed into                                 fraction of Prosa) as training lemmas1 . The selection criteria
H1 and H2, where H1 is an intermediate subgoal and H2 is                                    aim for diversity: we choose lemmas with proofs that vary
terminal. H1 is further decomposed into the terminal subgoals                               in tactic count (i.e., difficulty), and we sample from different
S1 and S2. The terminal subgoals S1, S2 and H2 are then                                     files and, whenever possible, different subdirectories within the
dispatched to subagents for proof.                                                          Prosa codebase. We use a preliminary version of our system
   The primary agent performs lemma decomposition in two                                    (equipped with external Rocq tools and the Prosa codebase) to
stages. First, a high-level decomposition stage reasons about                               attempt to prove these lemmas, and we collect the full traces of
the current context (incorporating any human-written proof                                  the proving procedure. Each trace captures the agent’s iterative
hint, if given) to extract fundamental steps that can genuinely                             attempts, including failures, error messages, and proof states,
advance the proof. Second, a low-level decomposition stage                                  until success. We then fed these traces to an LLM to analyze
transforms those high-level steps into a proof skeleton di-                                 failure reasons and generate skills. Concretely:
rectly provable in Rocq. It turns out that the agent is doing                                 1) We use LLM to divide each trace into segments, each
relatively well with the high-level decomposition, especially                                     handling a local task (e.g., fixing an error in the proof).
when human-written proof hints are given. However, the                                        2) For each segment, we use the LLM to identify the
agent struggles in the second stage. Because the low-level                                        problem being solved, analyze its cause, and generate
decomposition relies on the backbone LLM’s inherent rea-                                      1 For detailed information on the training lemmas, see the ProsaBuddy
soning capability, it is usually not fine-grained enough, and                               Github repository ⟨https://github.com/ProsaBuddy/RTSS2026⟩.
                                                                                TABLE III
                                                                        S UMMARY OF P ROVING S KILLS

            Name                                                                                Brief Description

    Small-step & inspect    Write one tactic at a time and inspect the resulting goal state after each step. This avoids writing long proof scripts without checking intermediate
                            goals, and it helps keep the actual proof state in view.

    Error priority          Resolve errors in priority order: syntax or parse errors first, then ill-typed terms, then unsolved goals or tactic failures, since later diagnostics are
                            often consequences of earlier failures.

    Tactic selection        Use simpler and more direct tactics before heavier or more search-based ones, such as reflexivity, lia, ring, tauto, congruence,
                            auto/eauto, and decide/native_decide. For composite goals, decompose the goal first and automate each component separately.

    Rewrite discipline      When rewrite fails because the rewritten term appears in dependent types, reorganize context with commands like generalize dependent
                            or subst. Also, name small helper results with assert, pose proof, or set instead of packing too many steps into one long tactic chain.

    Cleanup & final         After a proof compiles, clean it up, choose deliberately between Qed and Defined, and then actually compile the file with a command such as
    check                   coqc to make sure everything still works. A proof is not complete until temporary holes such as admit or Admitted. have been removed.

    Syntax-driven rewrite   Before each rewrite, check whether the pattern required by the lemma already appears exactly in the current goal. If it does not, first transform the
                            goal into that form instead of forcing the rewrite just because it seems mathematically correct.

    Local bridge lemmas     Use a small local bridge lemma when the mismatch is specific to the current branch or to a fixed local expression. Extract a generic lemma only
                            when the same normalization gap recurs across proofs.

    Minimal expansion       When a by fails, remove by and keep the rest exactly the same. Re-run immediately and record both the first revealed error message and the
                            number of focused goals. If expansion produces multiple goals, the primary issue is proof structure. If it reveals a rewrite mismatch, the issue is the
                            current goal shape. If it reveals Cannot apply or No assumption, the issue lies in the lemma preconditions or the local context.

    Expand “by” patterns    Expand compressed forms such as by rewrite, by apply:, have ...by ..., and case ...; by ... into ordinary proof scripts so
                            that you can see exactly which step fails or which branch is still open. After expanding one by step, fix only that step. Do not guess new tactics
                            before reading the first real error, and shorten it back to by only after the expanded version is confirmed to close the proof correctly.

    Bool/Prop boundary      If the remaining reasoning is easier to carry out in Prop than in Boolean form, convert the comparison once and finish the branch in Prop, reflecting
                            back only if the final goal is Boolean.

    Normal form &           First decide what form the final result should have: a count expression or a big-operator expression. After choosing that target form, rewrite in one
    bridge order            direction: indicator sum -> filtered big operator -> count. Do not switch back and forth between forms.

    Big-op normalization    First simplify the innermost sums that are easy to evaluate, such as constant sums or sums of Boolean tests. Then reorganize the outer sum if
    order                   needed. Only after that should you rewrite repeated addition as multiplication. Try to keep the whole branch in one consistent form instead of
                            repeatedly switching between sums, iter, and multiplication.

    Count before min        First rewrite the main counting fact into a clear bound on count, such as count P s <= k. Only after that should you handle Nat.min, minn,
                            or the final arithmetic inequality. Do not start the final arithmetic steps while the same quantity is still written in several different counting forms.

    Failure signals         If big_mkcond or sum1_count does not apply, the expression is usually still in the wrong form. A common mistake is to skip the intermediate
                            normalization steps and jump straight from an indicator sum to count or even to a min inequality, which makes both the rewrites and the later
                            arithmetic harder to control.

    Failure signatures      When rewrites such as mul1n, mulnC, or big_ord_recr fail, the expression is usually still in the wrong form. If the branch has become a
                            counting problem involving count, sum1_count, or Nat.min, switch to the count-normalization skill instead of continuing with generic
                            big-operator rewrites.

    Goal management         Use this skill when a Coq or Ssreflect proof has drifted into a multi-goal state after a branching tactic or local sublemma, especially when coqc
                            reports “Expected a single focused goal but 2 goals are focused,” and the next step should be structural recovery with
                            bullets, braces, and explicit branch closure rather than further mathematical reasoning.1

    Goal-driven lemma       This skill helps distinguish between ordinary subgoals that can be proved later and early parameters or prerequisites that Coq must know
    instantiation           immediately. It recommends using apply or eapply to let the current goal expose the real remaining obligations, and, if necessary, supplying only the
                            first missing parameter or preconditions instead of writing a long, fully explicit exact term.
1
  Goal-management errors were the most frequent failures in our experiments. This is likely because Rocq and newer SSReflect proof modes enforce goal focusing and subproof
bookkeeping more explicitly, so compressed proof scripts that worked in older Coq settings may fail in Rocq. We hypothesize that current LLMs have seen more older Coq scripts
than Rocq 9.x scripts, and therefore often generate fragile goal-management patterns that lead to these errors.



       a skill to avoid or resolve it. This produces a pool of                                detailed explanation of the goal-driven lemma instantiation
       proving skill candidates.                                                              proving skill (the last row in Table III), which addresses a
    3) We use the LLM to merge proving skill candidates that                                  problem specific to schedulability analysis using Prosa. As
       address the same or similar problems.                                                  mentioned in Section III-A, Prosa has a highly structured hier-
    4) Finally, we manually review the remaining candidates,                                  archy that facilitates lemma reuse across different task models.
       discarding those that are too general, vague, or lacking                               Applying such a lemma requires satisfying its preconditions,
       useful information, and enhance some of them with                                      which themselves depend on further preconditions, eventually
       human expertise. This results in the final 17 proving skills                           reaching the specific assumptions of the chosen task model.
       as summarized in Table III.                                                            In these cases, the agent tends to use the exact tactic when
                                                                                              applying such lemmas, which requires all preconditions and
  Due to space limitations, we cannot elaborate on every
                                                                                              parameters to be explicitly supplied. The upper part of Figure
proving skill in Table III. In the following, we only give a
 1   exact (@uniprocessor_response_time_bound_restricted_supply_seq               should be refined. Moreover, while proving skills are stored
 2
 3
         Task H (@limited_preemptions_rtc_threshold Task H H1)
         Job H2 H4 H3 (@limited_preemptive_job_model Job H5)
                                                                                  in skill files and loaded on demand, decomposition guidelines
 4       PState H_uniprocessor_proc_model H_unit_supply_proc_model                are placed directly in the agent’s prompt. The current set of
 5       H_consumed_supply_proc_model arr_seq VALID_ARRIVALS
 6       sched JOBS_FROM_ARRIVAL_SEQUENCE JOBS_MUST_ARRIVE                        decomposition guidelines is small, so the benefit of making
 7       COMPLETED_JOBS_DONT_EXECUTE VALID_COSTS ts tsk H_tsk_in_ts
 8       VALID_PREEMPTION_MODEL VALID_RTCT H0 VALID_ARRIVAL_CURVE
                                                                                  them load-on-demand is limited, but nothing prevents users
 9       RESPECTS_MAX_ARRIVALS                                                    from packaging them as on-demand skill files.
10         (rs_jlfp_interference arr_seq sched)
11         (rs_jlfp_interfering_workload arr_seq sched)
12       ABSTRACT_WORK_CONSERVING H_sequential_tasks                              D. Tools
13       I_AND_W_SEQUENTIAL
14
15
         L BUSY_INTERVALS_BOUNDED (arm_sbf Π Θν)
         INTRA_BOUNDED R SOL_SEQ_RS
                                                                                     In addition to the standard built-in tools in OpenCode, such
16       j ARR TSK).                                                              as file reading and code search, we develop several extra tools
                                                                                  to assist the proof construction.
 1
 2
     apply : uniprocessor_response_time_bound_restricted_supply_seq;
       try done.
                                                                                     We integrate a suite of Rocq tools that supply fine-grained,
                                                                                  context-aware feedback based on the current proof state. Rocq
                                                                                  provides a batch compiler and an interactive toplevel, i.e., a
Fig. 5. Example illustrating the goal-driven lemma instantiation proving skill.
The upper part shows the proof script using exact, i.e., explicitly providing
                                                                                  REPL (read–eval–print loop). rocq-lsp is a separate lan-
all the needed preconditions and parameters. The lower part shows the proof       guage server/plugin for Rocq. Our tools wrap these underlying
script using apply combined with try done.                                        interfaces. We develop a compiler-backed tool that checks
                                                                                  whole .v files and reports compilation status and errors,
                                                                                  a toplevel-backed tool that answers queries about library
5 shows a real example we take from the traces for generating                     objects, lemma types, assumptions, and definitions, and a
the proving skills. In this example, the lemma requires a long                    rocq-lsp-backed tool that provides incremental diagnostics,
list of preconditions and parameters (lines 2 - 16) if using                      current goals and local hypotheses. Our integration follows
exact to apply this lemma. It is very difficult for the LLM                       OpenCode’s standard way of providing tools. Each tool is a
to precisely provide all the required preconditions and parame-                   module with a call name, a brief description, and an input
ters. Even if the agent repeatedly guesses parameters, receives                   schema. The agent does not run Rocq directly. It selects
error messages from Rocq tools, and tries again, in most                          a tool and supplies arguments, and the OpenCode runtime
cases, it still can never find the correct combination. However,                  dispatches the call, using session configuration such as file
a simple solution exists for this problem: instead of using                       paths and project roots. The output is written to files, which
exact with all parameters, one can use the apply tactic with                      the OpenCode harness parses into structured results such as
the lemma. This turns the preconditions and parameters into                       error locations, goals, and hypotheses. This gives the agent
explicit goals, which are typically much easier to prove (many                    fine-grained proof-state feedback while avoiding fragile raw
can be resolved automatically by built-in tactics). For instance,                 command-line handling.
the lower part of Figure 5 shows the proof script that applies                       We developed a structured proof-planning tool that enables
the lemma using apply, without providing the preconditions,                       the primary agent to externalize its decomposition as an
and then using try done can close all the generated goals.                        explicit DAG before constructing a proof sketch that can be
This insight becomes a reusable proving skill.                                    compiled by Rocq. Each node in the DAG records a Rocq
   Why does analyzing proof traces enable the LLM to gen-                         subgoal, its dependencies, and optionally proposed library
erate useful skills? The traces contain rich diagnostic infor-                    lemmas; terminal delegation candidates are materialized as
mation: they show iterative attempts to solve a local problem,                    annotated proof regions. The tool mechanically checks target-
with clear success/failure outcomes, error messages, and the                      lemma consistency, acyclicity, and lemma applicability, and
current proof state at each step. The LLM can observe how                         compiles the resulting sketch to ensure the subgoals can be
the agent fails repeatedly and how it eventually succeeds. The                    combined. It also assigns each delegated subgoal a unique
resulting proving skill thus encodes a practical solution that                    proof region, so a subagent can edit only its assigned region
the LLM alone would not produce.                                                  while preserving the surrounding proof and local context. This
   It is worth comparing proving skills with the decomposi-                       tool is useful since, if a decomposition remains only in the
tion guidelines. Both serve the same purpose: adding extra                        primary agent’s free-form reasoning, invalid decompositions
information to the LLM’s prompt to improve its problem-                           may go unnoticed until subagents fail.
solving ability. The differences lie in how they are obtained                        We also developed a tool to detect stagnation in proof
and used. Decomposition guidelines are crafted manually by                        construction. Since the Rocq compiler reports only the cur-
human experts, while proving skills are generated by having                       rent proof state, it cannot determine whether repeated agent
the LLM analyze proof traces, followed by human review. We                        actions are advancing the proof or reproducing the same
also attempted to use a similar trace-driven process to extract                   failure; without an independent progress assessment, the agent
decomposition guidelines, but the results were poor. This is                      may keep calling the same tools, launching subagents on
probably because the impact of a decomposition is non-local                       unchanged proof regions, or making superficial edits while
and diffuse; the LLM struggles to connect later proof failures                    wasting computation and tokens. At proof milestones, such as
to decomposition choices and infer how the decomposition                          after the primary agent writes or substantively revises a proof
                                                                        TABLE IV
                                                             ROCQ COMMAND CLASSIFICATIONS [62].

Classification   Operational role                                                            Representative commands                                        Decision

VtProofStep      Advances or organizes the current proof state.                              Tactic sentences, bullets, focusing commands and delimiters.   Allowed
VtQuery          Queries without modifying the interpretation state.                         Check, Print, Search, Locate, and Show.                        Allowed
VtStartProof     Initiates an interactive proof.                                             Lemma, Theorem, and proof-style Definition.                    Forbidden
VtQed            Terminates or discards the current interactive proof.                       Qed, Defined, Admitted, and Abort.                             Forbidden
VtProofMode      Changes the proof mode used for subsequent proof commands.                  Proof-mode switching commands, e.g., Proof Mode "Ltac2".       Forbidden
VtMeta           Represents STM, history-management, or proof-control commands.              Back, Undo, Restart, and reset commands.                       Forbidden
VtSideff         May modify the global environment, parser state, or interpretation state.   Axiom, Parameter, Definition, Require, Notation,               Forbidden
                                                                                             Set/Unset, Hint, Instance, and Declare ML Module.




sketch, after a proof region is updated, or after a subagent                            of the .v file and check whether there is an AST node
returns, the tool invokes Rocq, compares the new state with                             corresponding to a command in a forbidden class within the
the previously recorded one, and records verified, structural,                          proof body. If so, the check fails at this step.
or diagnostic progress. It then uses these records to detect                               Third, we verify that nothing outside the proof body has
stagnation: if repeated tool calls or subagent attempts on an                           been changed, except for imports from trusted libraries at the
unchanged region produce no new evidence, it warns the agent                            very beginning. Specifically, before the agent starts working,
and may temporarily block further attempts until new compiler                           we store a copy of the original .v file containing the target
evidence appears or the region’s subgoal, dependencies, or                              lemma. After the agent submits its .v file, we compare the
proof commands are substantively revised.                                               ASTs of the two files to ensure that any changes outside the
E. Proof Auditing                                                                       proof body are limited to imports from trusted libraries at the
                                                                                        very beginning; otherwise, the check fails. Currently, we treat
   When an agent declares a proof complete, we cannot
                                                                                        only MathComp and Prosa as trusted libraries and assume
treat that declaration, or even a successful compilation, as
                                                                                        that importing them at the beginning of the .v file does not
evidence that the proof has actually been written, since the
                                                                                        introduce risks of altering the lemma to be proved or enabling
agent may “cheat” during proof construction. For example, an
                                                                                        the agent to bypass the proof.
agent might silently change the theorem statement, weaken a
definition, or introduce an unproven axiom. This could still                               A proof submitted by the agent is deemed valid only if
result in a successful compilation, yet not give a valid proof                          it passes all the steps above. Otherwise, the submitted proof
of the intended lemma. We therefore need an independent                                 is rejected and returned to the agent for reconstruction. Note
auditing step to decide whether the proof is valid.                                     that the audit is performed in a different OS process, so any
   The goal of proof auditing is to ensure two things: (1)                              changes to the Rocq environment state made by the proving
the lemma to be proved is unchanged, and (2) the generated                              agents cannot affect the Rocq environment state used in the
proof indeed proves the lemma rather than bypassing its proof.                          audit. The above auditing procedure is conservative in the
ProsaBuddy runs in a sandbox, an isolated workspace that                                sense that a proof file submitted by the agent is not necessarily
limits which files the agent can read and write. We place the                           invalid just because it failed the audit. Nevertheless, the sound-
libraries the agent is allowed to use in its read-only scope,                           ness of our proof auditing, both its design and implementation,
so that the agent can import from them but cannot modify or                             has not yet been formally verified. Establishing a formally
recompile the libraries themselves. Based on this, the auditing                         verified proof auditing procedure will be our future work.
consists of the following steps.                                                           Besides our proof-auditing script itself, we rely on several
   First, we check whether the submitted .v file, which con-                            trusted bases to declare a proof valid. The scope of the trusted
tains the lemma to be proved and its proof script, is accepted                          base depends on the property being checked. For kernel-level
by Rocq. Concretely, this means that when the Rocq compiler                             proof validity, the trusted base is the Rocq kernel: it is the
processes the file, it is parsed and elaborated without errors,                         component that actually checks proof terms, and Rocq is
and the proof terms produced by the tactics are accepted by the                         designed so that nothing else needs to be trusted for soundness.
Rocq kernel. In particular, if the proof script contains tactics                        ProsaBuddy’s proof-auditing procedure, however, relies on
that leave unfinished goals, such as admit or give_up, the                              additional components. Our assumed trusted base for auditing
check fails at this step.                                                               consists of the Rocq kernel, the Rocq compiler, the tactics
   Second, we check that the proof body, i.e., the part after                           allowed to be used, the trusted libraries, the astdump plugin,
Proof. and before Qed., contains only commands for                                      and our proof-auditing script. Trust to these components is
advancing or querying the proof state. Table IV shows the                               needed because our audit does not inspect the proof term
classification of Rocq commands. Among these classes, only                              directly. It inspects the AST and checks whether the AST
the VtProofStep and VtQuery classes are allowed in                                      contains forbidden commands. The absence of such commands
the proof body; all other classes are forbidden. We use the                             in the AST, however, does not by itself guarantee that the
astdump plugin (part of rocq-lsp) to extract the AST                                    proof term submitted to the kernel is free of them. The AST
is extracted from the source file by the astdump plugin, and       come from manually splitting a single lemma into separate
the proof term is obtained by compiling the source file, during    smaller lemmas. We do this when the original lemma states
which the tactics are executed. To infer from the absence          multiple independent results at once. This does not change
of forbidden commands in the AST that the proof term is            the mathematical content of the original result. There is a
also free of them, we have to trust the astdump plugin, the        compatibility issue: Prosa 0.4 includes foundations for global
compiler, the tactics and the imported libraries, as well as       multiprocessor scheduling, but the latest version, Prosa 0.6,
our proof-auditing script. A bug in any of these components        does not have this part. Prosa 0.6 is based on Rocq, whereas
might cause our auditing procedure to overlook an invalid          Prosa 0.4 is based on Coq, and Rocq and Coq have subtle
proof, even though the Rocq kernel itself remains sound.           syntactic differences. Therefore, we manually ported the global
However, the tools that agents use while generating proofs         multiprocessor scheduling part in Prosa 0.4 from Coq to Rocq.
need not be trusted: they are used only to provide information        We use the relevant portion of the corresponding research
guiding agents to construct proofs, and the correctness of this    paper as the human-written proof hint input. Specifically, this
information does not affect the auditing procedure.                input includes the target theorem or lemma itself, its full
                                                                   human-written proof, as well as any supporting definitions, no-
                      IV. E VALUATION
                                                                   tation, and variables that are referenced within the proof. Au-
A. Comparison with State-of-the-Art                                toRocq, OpenCode and ProsaBuddy accept this input through
   We compare ProsaBuddy with four recent LLM-based au-            their existing interfaces. However, PALM, Cobblestone, and
tomated theorem proving systems for Coq/Rocq: PALM [33],           RocqStar do not originally provide such an interface. PALM
AutoRocq [41], Cobblestone [40] and RocqStar [39]. The             and Cobblestone operate through their generate-and-repair
interaction layer with Coq of PALM and Cobblestone relies          workflows, which take the formal lemma and the current
on coq-serapi, which has only been maintained up to Coq            proof state as inputs and iteratively attempt to construct a
8.20. This dependency prevents PALM from being directly            valid proof. Neither PALM nor Cobblestone accepts additional
applied to the Rocq environment. Since our experiments             text inputs. RocqStar retrieves formal definitions and theorems
use Rocq 9.0 for RocqStar and ProsaBuddy, we ported the            from a structured Rocq library, but it does not accept free-
subset of coq-serapi interaction functionality used by PALM        text descriptions as input. To provide the same human-written
to Rocq 9.0 for a fair comparison. We also attempted to            proof hint to all systems, we augmented PALM, Cobblestone,
evaluate COPRA [34], another recent LLM-based Coq/Rocq             and RocqStar to prepend the corresponding hint to their
proving agent, but COPRA failed on all benchmark tasks in          system prompts. All comparison results reported for PALM,
our environment; therefore, we do not include its results in       Cobblestone, and RocqStar are obtained from their augmented
Table VI. We investigated the failures and found that, although    version with human-written hints.
COPRA claims support for both Lean and Coq, the released              Table VI shows the comparison results. Each column in
GitHub implementation leaves several Coq-environment con-          the table is the lemma index in the benchmark. In each cell,
nection functions unimplemented. We did not compare with           ✔ represents that the lemma is successfully proved, while ✘
Rango [37] because RocqStar has already included a direct          represents the agent declares a failure to prove this lemma
comparison with Rango and reported better performance [39].        and stops. The number under ✔ represents the total amount
Therefore, we only choose the better one as the representative     of token consumption proving this lemma in the unit of 1K
baseline in our experiments. We did not compare with CoqPi-        tokens (counting both input tokens and output tokens). ∞
lot because RocqStar is a follow-up system that extends the        represents that the agent has not yet proved the lemma before
CoqPilot pipeline with a more advanced agentic architecture        reaching the timeout threshold. In our experiments, we set
[32], [39]. We did not compare with ADAPT [38], QUARRY             the timeout threshold to be 50, 000K tokens. The timeout is
[43], ReCent-Prover [42] and the work in [35] and [36]             measured by the number of tokens consumed rather than by
because they are not yet publicly available. Moreover, we          actual time consumption, since variations in time delay depend
also include the original OpenCode in the comparison. For all      heavily on many factors unrelated to the model inference, such
systems, we use GPT-5.4 as the backbone LLM. All compared          as network latency, server load, or local hardware restrictions.
systems have access to the full Prosa library.                     In contrast, the token count provides a more stable metric that
   The evaluation is conducted on a benchmark that we cre-         better reflects the amount of LLM inference performed. To
ated. The benchmark contains 24 lemma formalizations in            give readers a rough sense of scale, in most cases ProsaBuddy
Rocq, which are not included in the existing Prosa library.        takes between 3 and 5 hours to reach the 50, 000K-token
These lemmas are drawn from five research papers [63]–[66],        threshold. Besides the total token consumption, the KV-cache
[68] and one book [67] in real-time scheduling theory, and         hit rate is also a key factor determines the proving efficiency
we manually formalized them in Rocq. This ensures that the         and cost. The KV-cache hit rate of ProsaBuddy is on average
benchmark has no overlap with the “training” lemmas used to        about 90% in our experiments2 .
automatically generate the proving skills, as introduced in Sec-
                                                                      2 The KV-cache hit rate also depends on the LLM serving provider’s KV-
tion III-C. The sources of these lemmas are listed in Table V.
                                                                   cache resource allocation policy. For example, the KV-cache hit rate will drop
All lemmas concern global multiprocessor scheduling. Note          if less KV-cache space is allocated to each request session. Therefore, this
that, in Table V, case #10 and #11 (and also #12 and #13)          KV-cache hit rate result may not be reproducible.
                                                                                              TABLE V
                                                                            I NFORMATION OF THE L EMMA IN OUR B ENCHMARK

    Index        #1      #2       #3        #4       #5      #6      #7      #8      #9      #10       #11        #12      #13      #14       #15    #16   #17      #18       #19    #20   #21    #22     #23     #24

                [63]    [63]      [63]     [64]      [64]  [64]  [64]  [65]  [65]   [65]    [65]    [65]    [65]                    [65]      [65]  [65]  [65]      [65]      [66]  [66]  [66]   [67]     [67]    [68]
   Source
               Lem 3   Lem 4     Thm 6    Thm 1     Thm 2 Thm 3 Thm 4 Lem 1 Thm 1 Lem 1-1 Lem 1-2 Lem 2-1 Lem 2-2                  Lem 3     Lem 4 Lem 5 Thm 1     Thm 2     Thm 3 Lem 4 Lem 5 Lem 18.1 Lem 18.6 Lem 8

 Dependency      -       #1      #1, #2      -        -      #3       -       -      #8        -         -      #10, #11 #10, #11 #12, #13    #14     -    #15      #16       #21     -    #20     -      #22      -

num. of Tactics 70-110 160-200     -      180-300   10-40   70-90   10-40   60-80   30-70   200-220   150-200    40-60      -        -       15-30    -    10-20   100-150   20-80    -     -    15-90     -     60-80

Note: “Dependency” represents which other lemma in this table are prerequisites for this lemma. “# of Tactics” represents the range of the number of tactics in the proof
generated by different systems in the following evaluation experiments (different systems often generate proofs with different numbers of tactics). For those lemmas/theorems
which are not proved by any system, the number is denoted by “-”.



   To reduce time and cost, we omit some experiments, which                                                             x/5 indicates that the system succeeds x times out of the
are denoted by “–” in Table VI. This is because ProsaBuddy                                                              five runs. For n = 5 runs    with x successes, we compute
shows much better performance than all the compared systems,                                                            pass@k = 1 − n−x     k   / n
                                                                                                                                                    k . Token counts are also reported
so we infer that for the cases where ProsaBuddy failed, all the                                                         in thousands. The numbers in the ‘Range’ and ‘Average’ rows
other compared system will also very likely fail, so we omit                                                            represents the token consumption range and the average token
these experiments.                                                                                                      consumption of the 5 runs.
   The experiment results show that ProsaBuddy significantly                                                               The results in Table VII show that, across the 6 selected
outperforms the compared systems. Out of 24 lemmas, PALM                                                                cases, ProsaBuddy achieves 27 successful proofs out of 30
and Cobblestone only succeed 1 lemma, AutoRocq succeeds                                                                 total runs. It succeeds in all 5 runs on Cases #8, #15, and #17,
2, RocqStar and OpenCode succeed 3, while ProsaBuddy                                                                    and in 4 of 5 runs on Cases #1, #2, and #22. These repeated
succeed 17. For the one lemma PALM and Cobblestone                                                                      runs confirm that both proof outcomes and token consumption
succeed, they use many fewer tokens. This is because of the                                                             vary to some extent across individual executions. However,
way they work: they invoke the LLM for a specific number of                                                             this variation does not alter the main comparative picture:
times, and detailed error corrections rely on automated proof                                                           ProsaBuddy attains at least four successes out of five runs on
generation tools such as CoqHammer [21]. This differs from                                                              every selected case, whereas PALM yields no successful runs
other agent-based systems, which conduct iterative dialogues                                                            and OpenCode succeeds in only 2 of its 30 runs. Furthermore,
with the LLM for both proof generation and error correction.                                                            the estimated pass@3 for ProsaBuddy is 1.0 for all 6 cases.
   Our benchmark targets lemmas that are not yet included in                                                               We further conduct evaluations using more lemmas selected
Prosa but are closely connected to the foundations provided                                                             from Prosa. These lemmas are categorized into seven levels
by Prosa. Their proofs rely on existing Prosa definitions and                                                           (L1–L7) based on proof length, measured by the number of
basic lemmas. This selection is intentional: lemmas that are                                                            tactics used in the proof. Each level contains 10 lemmas,
largely unrelated to the current Prosa foundation would require                                                         except L7: Prosa has 12 L7 lemmas in total, among which
ProsaBuddy to invent new definitions and many intermediate                                                              we selected 5 as training lemmas and 5 as evaluation lemmas
lemmas from scratch, which is beyond its current capability.                                                            for this evaluation, with the evaluation lemmas strictly distinct
Accordingly, the experimental results should not be interpreted                                                         from the training lemmas used in Section III-C. Unlike the
as showing that ProsaBuddy can prove real-time scheduling                                                               our build benchmark, this experiment does not provide the
theorems in full generality. They instead evaluate whether                                                              agent with human-written proof hints. This is because many
ProsaBuddy can extend an existing mechanized library by                                                                 lemmas in Prosa are library-internal results and do not have
proving new lemmas when the relevant definitions and many                                                               corresponding human-written proofs in the literature.
auxiliary results are already available. This reflects the positive                                                        We observe that Prosa contains many families of similar
feedback loop we aim to support: as Prosa grows to cover more                                                           proofs. For example, the same lemma is established under
real-time scheduling topics, ProsaBuddy can benefit from the                                                            several related scheduling models, such as fixed-priority pre-
richer foundation and help prove further lemmas.                                                                        emptive, non-preemptive, and limited-preemptive scheduling.
   The results in Table VI report only a single run for each case                                                       Although these are technically different lemmas, their state-
by each system. Since LLM generation is inherently stochastic,                                                          ments and proof structures can be very similar. In such cases,
repeating the evaluation multiple times per case would yield                                                            an agent with access to the full library may solve the target
more robust conclusions. However, conducting such repeated                                                              lemma largely by copying or lightly adapting an existing
runs for all cases would incur prohibitive time and costs.                                                              proof, rather than by generating the proof from the target
As a compromise, we select 6 cases to further conduct                                                                   statement and local context. This would make the evaluation
multi-run evaluations. These cases are selected based on the                                                            less interesting. To solve this problem, for each lemma, we
token consumption of ProsaBuddy in the above experiments,                                                               provide only the minimal Prosa slice required to compile the
covering different difficult levels: #15 and #17 as the low-                                                            target file, computed from the transitive dependency closure of
difficulty group, #8 and #22 as the medium-difficulty group,                                                            its required modules. In this way, the agent has enough formal
and #1 and #2 as the high-difficulty group. For each case,                                                              context to prove the benchmark lemma, but it cannot search
we run each system 5 times under the same configuration.                                                                other parts of Prosa for the original proof or a similar proof.
                                                                                         TABLE VI
                                                  R ESULTS OF THE C OMPARISON E XPERIMENTS AND A BLATION S TUDY WITH OUR B UILT B ENCHMARK

                                                                                                                                                                                                                                                       num. of
                Index           #1           #2           #3    #4      #5          #6              #7    #8          #9           #10         #11      #12     #13   #14    #15     #16   #17     #18     #19     #20   #21    #22     #23    #24
                                                                                                                                                                                                                                                       success

                                                                         ✔
               PALM              ✘            ✘            -     ✘                  ✘               ✘      ✘          ✘             ✘           ✘        ✘       -     -      ✘       -     ✘       ✘       ✘       -     -      ✘       -      ✘        1
                                                                         3
                                                                         ✔                                                                                                                  ✔                ✔
              RocqStar           ✘            ✘            -     ✘                  ✘               ✘      ✘          ✘             ✘           ✘        ✘       -     -      ✘       -             ✘               -     -      ✘       -      ✘        3
                                                                        23                                                                                                                 587             1,486
                                                                         ✔                                                                                                   ✔
              AutoRocq           ✘            ✘            -     ✘                  ✘               ✘      ✘          ✘             ✘           ✘        ✘       -     -              -     ✘       ✘       ✘       -     -      ✘       -      ✘        2
                                                                         6                                                                                                  1176
                                                                         ✔
             Cobblestone         ✘            ✘            -     ✘                  ✘               ✘      ✘          ✘             ✘           ✘        ✘       -     -      ✘       -     ✘       ✘       ✘       -     -      ✘       -      ✘        1
                                                                         2
                                                                         ✔                                             ✔                                                                    ✔
              OpenCode           ✘            ✘            -     ✘                  ✘               ✘      ✘                        ✘           ✘        ✘       -     -      ✘       -             ✘       ✘       -     -      ✘       -      ✘        3
                                                                        247                                          1,083                                                                 500

                                 ✔                               ✔       ✔          ✔                      ✔           ✔                        ✔                             ✔              ✔       ✔       ✔                   ✔
              PB-w/o-S                       ∞             -                                    ∞                                   ✘                   ∞        -     -              -                             -     -              -      ✘        12
                               25,410                          23,440   206       3,760                  21,540       535                     45,185                        4,084           601    2,398    896                29,129
                                 ✔            ✔                  ✔       ✔          ✔            ✔                     ✔                        ✔                             ✔              ✔       ✔       ✔                   ✔              ✔
              PB-w/o-D                                     -                                               ✘                       ∞                    ∞        -     -              -                             -     -              -               14
                               23,056       20,858             11,296   186       11,481       2,617                  456                     30,334                        11,095          616    8,798    479                8,680          29,137
                                 ✔                                       ✔          ✔            ✔                     ✔        ✔               ✔                             ✔              ✔       ✔       ✔                   ✔
              PB-w/o-P                        ✘            -     ✘                                         ✘                                             ✘       -     -              -                             -     -              -      ✘        12
                               37,125                                   205       30,139       47,333                6,511    35,156          24,619                        3,317          2,177   9,354   1,625               27,604
                                 ✔                               ✔       ✔          ✔            ✔         ✔           ✔        ✔               ✔                             ✔              ✔       ✔       ✔                   ✔              ✔
              PB-w/o-H                       ∞             -                                                                                             ✘       -     -              -                             -     -              -               15
                               36,340                          11,238   358       3,501        1,257     16,550      1,398    41,562          31,716                        23,906         1,321   5,096   1,833               21,157         9,278

                                 ✔            ✔                  ✔       ✔           ✔            ✔        ✔           ✔        ✔               ✔        ✔                    ✔              ✔       ✔      ✔                    ✔              ✔
             ProsaBuddy                                ∞                                                                                                        ✘     ✘              ✘                             ✘     ∞              ✘                17
                               48,819       42,027             13,332   281        1,295        2,077    13,077      1,888    24,330          36,004   38,749               6,736          3,908   2,229   307                 31,614         13,557
              Note: The number under each ✔ represents the amount of token consumption to prove this lemma, which is in thousands of tokens.



                                                        TABLE VII                                                                                        B. Ablation Study
                                                  R ESULTS OF F IVE RUNS
                                                                                                                                                            We conduct ablation experiments to evaluate the contri-
Difficulty                       Low                                    Medium                                         High                              bution of different components in ProsaBuddy, the result of
Index                    #15                 #17                 #8                      #22                   #1                        #2              which is also reported in Table VI.
PALM                     0/5                  0/5                0/5                     0/5                   0/5                      0/5
                                                                                                                                                            PB-w/o-S. This variant removes the proving skills from
RocqStar                 0/5                  1/5                0/5                     0/5                   0/5                      0/5              ProsaBuddy. It proves 12 lemmas, fewer than the full Pros-
AutoRocq                 2/5                  0/5                0/5                     0/5                   0/5                      0/5
Cobblestone              0/5                  0/5                0/5                     0/5                   0/5                      0/5              aBuddy does, demonstrating the effectiveness of the proving
OpenCode                 0/5                  2/5                0/5                     0/5                   0/5                      0/5              skills developed in Section III-C.
ProsaBuddy               5/5                  5/5                5/5                     4/5                   4/5                      4/5
                                                                                                                                                            PB-w/o-D. This variant removes the lemma decomposition
pass@1                  1           1             1            0.8           0.8           0.8
pass@3                  1           1             1             1             1             1                                                            mechanism and instead uses only the primary agent to prove
Range
Average
                  6,736–19,087 1,748-6,457 13,077–38,724 22,890–31,614 29,168–54,525 35,546–64,957
                     11,471       3,669        25,220        28,120        44,171        50,630
                                                                                                                                                         a lemma. PB-w/o-D proves 14 lemmas. The gap between PB-
                                                                                                                                                         w/o-D and ProsaBuddy mainly appears on harder cases, i.e.,
                                                                                                                                                         lemmas on which ProsaBuddy spends more tokens. Token
                                     TABLE VIII
                                                                                                                                                         counts reveal a trade-off: ProsaBuddy sometimes spends more
                    R ESULTS WITH L EMMAS S ELECTED FROM P ROSA                                                                                          tokens because planning and delegation introduce extra inter-
                                                                                                                                                         action cost, but this overhead enables proofs that the single-
                                     L1              L2          L3           L4               L5           L6                L7                         agent variant cannot complete.
          num. of tactics            1-20         21-40        41-60      61-80            81-100         101-150            > 150
                                                                                                                                                            PB-w/o-H. This variant removes the human-written proof
               PALM                  1/10           0/10         -            -                 -              -               -
              RocqStar               7/10           2/10         -            -                 -              -               -
                                                                                                                                                         hints from ProsaBuddy, i.e., it does not read the corresponding
              AutoRocq               5/10           1/10         -            -                 -              -               -                         paper content. PB-w/o-H proves 15 lemmas. The two cases
             Cobblestone             1/10           0/10         -            -                 -              -               -                         where ProsaBuddy succeeds but PB-w/o-H does not are both
             OpenCode                4/10           0/10         -            -                 -              -               -
                                                                                                                                                         relatively difficult lemmas. This suggests that for simple cases,
             ProsaBuddy           10/10           10/10         8/10         9/10              9/10        6/10               1/5                        the formal context in Prosa, including definitions, existing
   Note: “# of tactics” represent the number of tactics used in its proof.                                                                               lemmas, and proof states, already provides substantial guid-
                                                                                                                                                         ance for proof construction. However, for difficult lemmas,
                                                                                                                                                         the human-written proof hints play a significant role.
   Similar to above experiments, we omit the experiments in                                                                                                 PB-w/o-P. This variant removes access to the full Prosa
L3-L7 for the compared systems, which are denoted by “–” in                                                                                              library and only provides the minimal dependent files needed
Table VIII. This is because, if a baseline shows poor ability                                                                                            to state the target lemmas. As a result, it can use basic defi-
to solve lemmas in lower-level groups, there is no reason                                                                                                nitions and low-level lemmas (related to the basic properties
to expect better performance on higher levels. As PALM,                                                                                                  of the definitions) included in the dependent files, but cannot
RocqStar, Autorocq, Cobblestone and OpenCode solved zero                                                                                                 directly observe or reuse higher-level auxiliary lemmas in
or only a very small number of lemmas at L2. Therefore,                                                                                                  Prosa. PB-w/o-P proves 12 lemmas. This shows that a full
we did not further evaluate them on L3 and above. The                                                                                                    library context is important for extending an existing mecha-
experiment results with lemmas selected from Prosa confirm                                                                                               nized development. Without it, the agent needs to rediscover
the superiority of ProsaBuddy. The results also show that                                                                                                intermediate facts that are already available in Prosa, which
ProsaBuddy still can successfully prove non-trivial lemmas                                                                                               signiciantly increase the difficulty to complete the proof. For
even without human-written proof hints.                                                                                                                  most cases where PB-w/o-P succeeds, it consumes more token
                                                                                          TABLE IX
                                                                    E XPERIMENT R ESULTS WITH D IFFERENT BACKBONE LLM S

                                                                                                                                                                                                                         num. of
          Index             #1       #2      #3    #4       #5      #6       #7      #8       #9      #10      #11      #12     #13   #14    #15     #16   #17      #18      #19     #20   #21    #22     #23    #24
                                                                                                                                                                                                                         success

                             ✔        ✔             ✔        ✔       ✔        ✔       ✔        ✔       ✔        ✔        ✔                    ✔              ✔        ✔       ✔                    ✔              ✔
         GPT-5.4                             ∞                                                                                  ✘     ✘              ✘                               ✘     ∞              ✘                17
                           48,819   42,027        13,332    281    1,295    2,077   13,077   1,888   24,330   36,004   38,749               6,736          3,908    2,229    307                 31,614         13,557
                                                             ✔       ✔        ✔                ✔                                              ✔              ✔        ✔       ✔                    ✔
    DeepSeek-v4-flash       ∞        ∞       -     ∞                                  ✘               ∞        ∞        ∞        -     -              -                               -     -              -     ∞         9
                                                            959    32,528   7,406            4,013                                          6,205          2,262   18,405   5,624                20,245
                                                             ✔                ✔                ✔                                              ✔              ✔                ✔
    DeepSeek-v4-pro         ∞        ∞       -     ∞                ∞                 ✘                ✘        ✘        ✘       -     -              -              ✘                -     -      ✘       -      ✘        6
                                                           2,201            8,749            4,247                                          20,898          768             4,567
                                                             ✔                                                                                                                ✔
   Gemini-3.1-flash-lite     ✘       ∞       -     ∞                ∞       ∞        ∞        ✘       ∞         ✘        ✘       -     -     ∞        -    ∞         ✘                -     -      ✘       -     ∞         2
                                                           1,889                                                                                                            10,355
                                                             ✔
      GPT-oss-120B           ✘        ✘      -      ✘                ✘       ✘        ✘       ✘        ✘        ✘        ✘       -     -      ✘       -     ✘        ✘        ✘       -     -      ✘       -      ✘        1
                                                           1,192




than ProsaBuddy, which witnesses such extra overhead even                                                              ProsaBuddy could not prove alone, a researcher with exper-
if the lemma is still proved.                                                                                          tise in real-time scheduling theory worked interactively with
                                                                                                                       ProsaBuddy, injecting additional human instructions when
C. Different Backbone LLMs                                                                                             ProsaBuddy was stuck or actively requested support. In this
   We further evaluate how the choice of different backbone                                                            way, both lemmas were successfully proved in 2 hours and 3
LLM affects the performance of ProsaBuddy. The results are                                                             hours, respectively. For comparison, a second researcher with a
reported in Table IX. In these experiments, all components                                                             similar background independently proved them fully manually
of ProsaBuddy are held constant except the backbone LLM.                                                               in Rocq, requiring 14 hours and 17 hours, respectively.
From the results we can see that the backbone LLM has a                                                                   A critical issue in automated theorem proving is the formal-
substantial impact on proof success: with the most powerful                                                            ization of the lemmas themselves. This is especially important
model, GPT-5.4, ProsaBuddy proves 17 lemmas, compared to                                                               for schedulability lemmas, whose descriptions are lengthy and
9 with DeepSeek-v4-flash, 6 with DeepSeek-v4-pro, 2 with                                                               involve many definitions and hypotheses. Correct formaliza-
Gemini-3.1-flash-lite, and 1 with GPT-oss-120B. Unexpect-                                                              tion is the foundation for the proof work: if a lemma is
edly, DeepSeek-v4-flash outperforms DeepSeek-v4-pro. We                                                                incorrectly formalized, its proof is meaningless. Therefore, the
currently do not have a clear explanation for this anomaly                                                             lemma must be formalized very carefully, a task that itself
and will investigate its cause in future work. Overall, these                                                          demands considerable effort. Assisting researchers during this
results show that the agent framework, augmented external                                                              formalization phase is thus also valuable. However, while
knowledge, and feedback from Rocq tools are not sufficient                                                             lemma proving benefits from an automatic verifier (Rocq) that
on their own; the reasoning capability of the backbone LLM                                                             can check correctness, formalization lacks such a verifier. It is
is crucial for the performance of ProsaBuddy. We also observe                                                          impossible to fully automate the checking of whether a formal-
that, on the subset of lemmas the weaker models can prove,                                                             ization precisely captures the human’s intended meaning. Our
they tend to consume more tokens on average than GPT-5.4,                                                              future work will investigate how to utilize an LLM-based agent
with a few exceptions. Similar to above, the mark “–” in Table                                                         to assist the formalization of schedulability analysis lemmas.
IX denotes the omitted experiments to save time and cost, as
for the difficult cases GPT-5.4 failed, the other weaker LLMs                                                             The decomposition guidelines and proving skills introduced
likely will also fail.                                                                                                 in Section III are only a small subset of what can be added to
                                                                                                                       improve the agent’s capabilities. We expect that ProsaBuddy
                   V. D ISCUSSIONS AND C ONCLUSIONS                                                                    users will develop their own skills to enhance the agent, and
   In this work, we present ProsaBuddy, an LLM-based agent                                                             we look forward to an ecosystem in which users share their
system designed to lower the effort needed to develop mech-                                                            skills to collectively improve the system. Such an ecosys-
anized real-time schedulability proofs. Evaluations show that                                                          tem would also create a feedback loop in which successful
ProsaBuddy can successfully prove many non-trivial lemmas.                                                             skills are refined, reused, and benchmarked across projects,
However, this is only a preliminary attempt in this direction; it                                                      accelerating collective improvement. On the other hand, these
has many limitations and ample room for further exploration.                                                           guidelines and skills are tailored to the capabilities of today’s
   Although in this paper we introduce and evaluate Pros-                                                              LLMs. Given how rapidly LLMs are advancing, future LLMs
aBuddy as a standalone system that proves lemmas end-to-end,                                                           may have much stronger reasoning abilities, rendering many
our ultimate goal is to build ProsaBuddy as a highly interactive                                                       previously useful skills obsolete.
tool. When a human expert intervenes in the proving process                                                               ProsaBuddy has the potential to be used more broadly.
and provides guidance at points where ProsaBuddy gets stuck,                                                           Proofreader [69] is an agentic system that helps researchers
ProsaBuddy becomes more effective and useful. We did not                                                               and authors find flaws in their own proofs. It actively seeks
systematically evaluate ProsaBuddy with a human in the loop,                                                           counterexamples and errors, without aiming to establish formal
because designing an objective and reproducible evaluation                                                             correctness. Given these complementary strengths, future work
methodology for such interaction would be difficult. Never-                                                            could explore how ProsaBuddy and other tools like Proof-
theless, we conducted some ad-hoc interactive experiments.                                                             reader might jointly accelerate the discovery, refinement, and
For example, for cases #13 and #14 in Table VI, which                                                                  validation of new theorems.
                               R EFERENCES                                              Journal of Functional Programming, vol. 25, pp. 1–59, 2015, Art. no.
                                                                                        e12.
 [1] K. Bletsas, N. C. Audsley, W.-H. Huang, J.-J. Chen, and G. Nelissen,          [24] J.-O. Kaiser, B. Ziliani, R. Krebbers, Y. Régis-Gianas, and D. Dreyer,
     “Errata for three papers (2004-05) on fixed-priority scheduling with self-         “Mtac2: typed tactics for backward reasoning in Coq,” in ACM SIG-
     suspensions,” Leibniz Transactions on Embedded Systems, vol. 5, no. 1,             PLAN International Conference on Functional Programming (ICFP),
     pp. 02:1–02:20, 2018, Art. no. 2.                                                  2018.
 [2] M. Günzel and J.-J. Chen, “Correspondence article: Counterexample for        [25] E. Tassi, “Elpi: an extension language for Coq (Metaprogramming Coq
     suspension-aware schedulability analysis of EDF scheduling,” Real-Time             in the Elpi λProlog dialect),” in International Workshop on Coq for
     Systems, vol. 56, no. 4, pp. 490–493, 2020.                                        Programming Languages (CoqPL), 2018.
 [3] J.-J. Chen, G. Nelissen, W.-H. Huang, M. Yang, B. Brandenburg,                [26] M. Sozeau, S. Boulier, Y. Forster, N. Tabareau, and T. Winterhalter,
     K. Bletsas, C. Liu, P. Richard, F. Ridouard, N. Audsley, R. Rajkumar,              “Coq Coq correct! verification of type checking and erasure for Coq,
     D. Niz, and G. Brüggen, “Many suspensions, many problems: a review                in Coq,” in ACM SIGPLAN Symposium on Principles of Programming
     of self-suspending tasks in real-time systems,” Real-Time Systems,                 Languages (POPL), 2020.
     vol. 55, no. 1, pp. 144–207, 2019.                                            [27] E. Komendantskaya, J. Heras, and G. Grov, “Machine learning in Proof
 [4] K.-H. Chen, M. Günzel, G. von der Brüggen, and J.-J. Chen, “Critical             General: Interfacing interfaces,” Electronic Proceedings in Theoretical
     instant for probabilistic timing guarantees: Refuted and revisited,” in            Computer Science, vol. 118, pp. 15–41, 2013.
     IEEE Real-Time Systems Symposium (RTSS), 2022.                                [28] K. Yang and J. Deng, “Learning to prove theorems via interacting
 [5] F. Cerqueira, F. Stutz, and B. B. Brandenburg, “Prosa: A case for                  with proof assistants,” in International Conference on Machine Learning
     readable mechanized schedulability analysis,” in Euromicro Conference              (ICML), 2019.
     on Real-Time Systems (ECRTS), 2016.                                           [29] L. Blaauwbroek, J. Urban, and H. Geuvers, “The tactician,” in Confer-
 [6] “The coq proof assistant,” project web site, https://coq.inria.fr.                 ence on Intelligent Computer Mathematics (CICM), 2020.
 [7] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao,         [30] A. Sanchez-Stern, Y. Alhessi, L. Saul, and S. Lerner, “Generating cor-
     “ReAct: Synergizing reasoning and acting in language models,” in                   rectness proofs with neural networks,” in ACM SIGPLAN International
     International Conference on Learning Representations (ICLR), 2023.                 Workshop on Machine Learning and Programming Languages (MAPL),
                                                                                        2020.
 [8] Anomaly, “OpenCode: The open source coding agent,” Software, 2026,
     accessed: September 8, 2026. [Online]. Available: https://opencode.ai         [31] E. First, Y. Brun, and A. Guha, “TacTok: semantics-aware proof synthe-
                                                                                        sis,” in ACM SIGPLAN Conference on Object-Oriented Programming,
 [9] The Rocq Development Team, The Rocq Prover Reference Manual,
                                                                                        Systems, Languages, and Applications (OOPSLA), 2020.
     Inria, CNRS, and contributors, 2025, version 9.2. [Online]. Available:
                                                                                   [32] A. Kozyrev, G. Solovev, N. Khramov, and A. Podkopaev, “CoqPilot, a
     https://rocq-prover.org/refman/
                                                                                        plugin for LLM-based generation of proofs,” in IEEE/ACM International
[10] G. Gonthier, A. Mahboubi, and E. Tassi, “A Small Scale Reflection
                                                                                        Conference on Automated Software Engineering (ASE), 2024.
     Extension for the Coq system,” Inria Saclay Ile de France, Research
                                                                                   [33] M. Lu, B. Delaware, and T. Zhang, “Proof automation with large
     Report RR-6455, 2016.
                                                                                        language models,” in IEEE/ACM International Conference on Automated
[11] F. Cerqueira, G. Nelissen, and B. B. Brandenburg, “On strong and weak              Software Engineering (ASE), 2024.
     sustainability, with an application to self-suspending real-time tasks,” in
                                                                                   [34] A. Thakur, G. Tsoukalas, Y. Wen, J. Xin, and S. Chaudhuri, “An in-
     Euromicro Conference on Real-Time Systems (ECRTS), 2018.
                                                                                        context learning agent for formal theorem-proving,” in Conference on
[12] S. Bozhko and B. B. Brandenburg, “Abstract Response-Time Analysis:                 Language Modeling (COLM), 2024.
     A Formal Foundation for the Busy-Window Principle,” in Euromicro              [35] X. Liu, H. Liu, X. Yi, and J. Wang, “LLM-Enhanced Theorem Proving
     Conference on Real-Time Systems (ECRTS), 2020.                                     with Term Explanation and Tactic Parameter Repair,” in Asia-Pacific
[13] K. Bedarkar, M. Vardishvili, S. Bozhko, M. Maida, and B. B. Branden-               Symposium on Internetware (Internetware), 2024.
     burg, “From intuition to Coq: A case study in verified response-time          [36] Y. Lu, H. Yang, X. Wang, G. Zhang, B. Li, C. Fu, C. Li, Y. Yuan, and
     analysis of FIFO scheduling,” in IEEE Real-Time Systems Symposium                  A. C.-C. Yao, “Clarifying before reasoning: A coq prover with structural
     (RTSS), 2022.                                                                      context,” arXiv preprint arXiv:2507.02541, 2025.
[14] P. Roux, S. Quinton, and M. Boyer, “A Formal Link Between Response            [37] K. Thompson, N. Saavedra, P. Carrott, K. Fisher, A. Sanchez-Stern,
     Time Analysis and Network Calculus,” in Euromicro Conference on                    Y. Brun, J. F. Ferreira, S. Lerner, and E. First, “Rango: Adaptive
     Real-Time Systems (ECRTS), 2022.                                                   retrieval-augmented proving for automated software verification,” in
[15] M. Maida, S. Bozhko, and B. Brandenburg, “Foundational response-time               IEEE/ACM International Conference on Software Engineering (ICSE),
     analysis as explainable evidence of timeliness,” in Euromicro Conference           2025.
     on Real-Time Systems (ECRTS), 2022.                                           [38] M. Lu, Z. Zhou, D. Xie, S. Jia, B. Delaware, and T. Zhang, “Adaptive
[16] K. Bedarkar, L. Elbeheiry, M. Sammler, L. Gäher, B. Brandenburg,                  proof refinement with llm-guided strategy selection,” arXiv preprint
     D. Dreyer, and D. Garg, “RefinedProsa: Connecting response-time anal-              arXiv:2510.25103, 2025.
     ysis with C verification for interrupt-free schedulers,” in ACM SIGPLAN       [39] A. Kozyrev, N. Khramov, G. Solovev, and A. Podkopaev, “Rocqstar:
     Conference on Programming Language Design and Implementation                       Leveraging similarity-driven retrieval and agentic systems for rocq
     (PLDI), 2025.                                                                      generation,” in International Conference on Autonomous Agents and
[17] A. Mahboubi and E. Tassi, Mathematical Components. Zenodo, Sep.                    Multiagent Systems (AAMAS), 2026.
     2022.                                                                         [40] S. R. Kasibatla, A. Agrawal, Y. Brun, S. Lerner, T. L. Ringer, and
[18] M. Dénès, A. Mörtberg, and V. Siles, “A refinement-based approach               E. First, “Cobblestone: A divide-and-conquer approach for automating
     to computational algebra in COQ,” in International Conference on                   formal verification,” in IEEE/ACM International Conference on Software
     Interactive Theorem Proving (ITP), 2012.                                           Engineering (ICSE), 2026.
[19] B. Ekici, A. Mebsout, C. Tinelli, C. Keller, G. Katz, A. Reynolds, and        [41] H. Tu, H. Zhao, Y. Song, M. Zafar, R. Meng, and A. Roychoudhury,
     C. Barrett, “Smtcoq: A plug-in for integrating smt solvers into coq,” in           “Agentic verification of software systems,” in ACM International Con-
     International Conference on Computer Aided Verification (CAV), 2017.               ference on the Foundations of Software Engineering (FSE), 2026.
[20] B. Ekici, G. Katz, C. Keller, A. Mebsout, A. J. Reynolds, and C. Tinelli,     [42] Y. Sun, C. Shi, H. Lyu, and Y. Xiong, “On reasoning-centric llm-based
     “Extending SMTCoq, a Certified Checker for SMT (Extended Ab-                       automated theorem proving,” arXiv preprint arXiv:2604.19558, 2026.
     stract),” in International Workshop on Hammers for Type Theories              [43] N. Zhang, N. Di, Z. Li, Y. Yao, and X. Ma, “Planning to hammer:
     (HaTT), 2016.                                                                      Difficulty-aware decomposition for automating rocq proofs,” arXiv
[21] Ł. Czajka and C. Kaliszyk, “Hammer for Coq: Automation for depen-                  preprint arXiv:2606.17981, 2026.
     dent type theory,” Journal of Automated Reasoning, vol. 61, no. 1–4,          [44] Y. Wu, A. Q. Jiang, W. Li, M. Rabe, C. Staats, M. Jamnik, and
     pp. 423–453, 2018.                                                                 C. Szegedy, “Autoformalization with large language models,” in Con-
[22] D. Delahaye, “A Tactic Language for the System Coq,” in Interna-                   ference on Neural Information Processing Systems (NeurIPS), 2022.
     tional Conference on Logic for Programming and Automated Reasoning            [45] A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jamnik, T. Lacroix,
     (LPAR), 2000.                                                                      Y. Wu, and G. Lample, “Draft, Sketch, and Prove: Guiding formal
[23] B. Ziliani, D. Dreyer, N. R. Krishnaswami, A. Nanevski, and                        theorem provers with informal proofs,” in International Conference on
     V. Vafeiadis, “Mtac: A monad for typed tactic programming in Coq,”                 Learning Representations (ICLR), 2023.
[46] Q. Liu, X. Zheng, X. Lu, Q. Cao, and J. Yan, “Rethinking and improving          IEEE International Conference on Embedded and Real-Time Computing
     autoformalization: Towards a faithful metric and a dependency retrieval-        Systems and Applications (RTCSA), 2014.
     based approach,” in International Conference on Learning Representa-       [67] S. Baruah, M. Bertogna, and G. Buttazzo, Multiprocessor scheduling for
     tions (ICLR), 2025.                                                             real-time systems. Springer, 2015.
[47] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil,          [68] A. Gujarati, F. Cerqueira, and B. B. Brandenburg, “Outstanding paper
     R. J. Prenger, and A. Anandkumar, “Leandojo: Theorem proving with               award: Schedulability analysis of the linux push and pull scheduler with
     retrieval-augmented language models,” in Conference on Neural Infor-            arbitrary processor affinities,” in Euromicro Conference on Real-Time
     mation Processing Systems (NeurIPS), 2023.                                      Systems (ECRTS), 2013.
[48] Z. Azerbayev, H. Schoelkopf, K. Paster, M. D. Santos, S. M. McAleer,       [69] B. C. Ward, “Proofreader: Informally auditing formal proofs with
     A. Q. Jiang, J. Deng, S. Biderman, and S. Welleck, “Llemma: An                  LLMs,” Manuscript, 2026, college of Connected Computing, Vanderbilt
     open language model for mathematics,” in International Conference on            University. [Online]. Available: https://cdn.vanderbilt.edu/t2-my/my-p
     Learning Representations (ICLR), 2024.                                          rd/wp-content/uploads/sites/3445/2026/06/proofreader.pdf
[49] H. Wang, H. Xin, C. Zheng, L. Li, Z. Liu, Q. Cao, Y. Huang,
     J. Xiong, H. Shi, E. Xie, J. Yin, Z. Li, H. Liao, and X. Liang, “LEGO-
     prover: Neural theorem proving with growing libraries,” in International
     Conference on Learning Representations (ICLR), 2024.
[50] H. Xin, Z. Ren, J. Song, Z. Shao, W. Zhao, H. Wang, B. Liu, L. Zhang,
     X. Lu, Q. Du, W. Gao, H. Zhang, Q. Zhu, D. Yang, Z. Gou, Z. Wu,
     F. Luo, and C. Ruan, “Deepseek-prover-v1.5: Harnessing proof assistant
     feedback for reinforcement learning and monte-carlo tree search,” in
     International Conference on Learning Representations (ICLR), 2025.
[51] H. Lin, Z. Sun, S. Welleck, and Y. Yang, “Lean-STar: Learning to in-
     terleave thinking and proving,” in International Conference on Learning
     Representations (ICLR), 2025.
[52] P. Song, K. Yang, and A. Anandkumar, “Lean copilot: Large language
     models as copilots for theorem proving in lean,” in International
     Conference on Neuro-symbolic Systems (NeuS), 2025.
[53] Y. Lin, S. Tang, B. Lyu, Z. Yang, J.-H. Chung, H. Zhao, L. Jiang,
     Y. Geng, J. Ge, J. Sun, J. Wu, J. Gesi, X. Lu, D. Acuna, K. Yang,
     H. Lin, Y. Choi, D. Chen, S. Arora, and C. Jin, “Goedel-prover-v2:
     Scaling formal theorem proving with scaffolded data synthesis and self-
     correction,” in International Conference on Learning Representations
     (ICLR), 2026.
[54] S. Varambally, T. Voice, Y. Sun, Z. Chen, R. Yu, and K. Ye, “Hilbert:
     Recursively building formal proofs with informal reasoning,” in Inter-
     national Conference on Learning Representations (ICLR), 2026.
[55] A. Q. Jiang, W. Li, S. Tworkowski, K. Czechowski, T. Odrzygóźdź,
     P. Miłoś, Y. Wu, and M. Jamnik, “Thor: Wielding hammers to integrate
     language models and automated theorem provers,” in Conference on
     Neural Information Processing Systems (NeurIPS), 2022.
[56] E. First, M. N. Rabe, T. Ringer, and Y. Brun, “Baldur: Whole-proof
     generation and repair with large language models,” in ACM Joint
     European Software Engineering Conference and Symposium on the
     Foundations of Software Engineering (ESEC/FSE), 2023.
[57] H. Wang, H. Xin, Z. Liu, W. Li, Y. Huang, J. Lu, Z. YANG, J. Tang,
     J. Yin, Z. Li, and X. Liang, “Proving theorems recursively,” in Confer-
     ence on Neural Information Processing Systems (NeurIPS), 2024.
[58] K. Weng, L. Du, S. Li, W. Lu, H. Sun, H. Liu, and T. Zhang,
     “Autoformalization in the era of large language models: A survey,” arXiv
     preprint arXiv:2505.23486, 2025.
[59] N. Giessing, H. Rahkooy, and M. Schubotz, “A survey on llms in
     automated theorem proving,” Zenodo preprint, 2026.
[60] The mathlib Community, “The Lean mathematical library,” in ACM
     SIGPLAN International Conference on Certified Programs and Proofs
     (CPP), 2020.
[61] G. Tsoukalas, J. Lee, J. Jennings, J. Xin, M. Ding, M. Jennings,
     A. Thakur, and S. Chaudhuri, “Putnambench: Evaluating neural
     theorem-provers on the putnam mathematical competition,” in Confer-
     ence on Neural Information Processing Systems, Datasets and Bench-
     marks Track (NeurIPS), 2024.
[62] The Rocq Development Team, “Vernacextend: Rocq runtime api,” https:
     //rocq-prover.org/doc/V9.1.0/api/rocq-runtime/Vernacextend/index.ht
     ml, 2025, rocq version 9.1.0, accessed September 15, 2026.
[63] M. Bertogna, M. Cirinei, and G. Lipari, “Improved schedulability
     analysis of edf on multiprocessor platforms,” in Euromicro Conference
     on Real-Time Systems (ECRTS), 2005.
[64] M. Bertogna and M. Cirinei, “Response-time analysis for globally
     scheduled symmetric multiprocessor platforms,” in IEEE Real-Time
     Systems Symposium (RTSS), 2007.
[65] N. Guan, M. Stigge, W. Yi, and G. Yu, “New response time bounds for
     fixed priority multiprocessor scheduling,” in IEEE Real-Time Systems
     Symposium (RTSS), 2009.
[66] Y. Sun, G. Lipari, N. Guan, and W. Yi, “Improving the response
     time analysis of global fixed-priority multiprocessor scheduling,” in
