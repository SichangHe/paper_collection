                                                        Verification as an Architectural Layer for LLM Agents
                                                                            A V-Model Design, and a Pilot Study of Its Deterministic Core
                                                                             Ali Afoud∗                                                                       Jie JW Wu
                                                                     Independent Researcher                                                     Michigan Technological University
                                                                            Canada                                                                      Houghton, USA

                                         Abstract                                                                                        The practical problem is not primarily accuracy but the ab-
                                         Large language model (LLM) agents built on the ReAct pattern con-                           sence of a mechanism for declining. A ReAct loop that cannot make
                                         centrate four responsibilities in a single model: selecting a strategy,                     progress does not report failure; it continues to emit actions until
                                         choosing each action, formatting it, and judging whether the result                         an externally imposed budget intervenes or, absent a budget, until
                                                                                                                                     the serving infrastructure refuses further requests. Such an agent
arXiv:2609.31937v1 [cs.SE] 25 Sep 2026




                                         is adequate. No component outside the generative loop can reject
                                         the loop’s output, so an agent that cannot make progress does not                           cannot be composed into a larger system, because a caller receives
                                         report failure; it continues until an externally imposed budget ter-                        either a plausible answer or nothing and cannot distinguish the
                                         minates it. We propose treating verification as an architectural layer                      two. The literature documents the underlying mechanics: turn-
                                         for agent systems by adapting the V-model from software engineer-                           by-turn action selection is a greedy policy that can be arbitrarily
                                         ing: specification levels descend from requirements to individual                           suboptimal over long horizons, with reported myopic-trap rates
                                         steps, each level is paired with a dedicated verifier, a deterministic                      above 50% and post-error recovery near 5% [10]; agents abandon
                                         controller enforces every verdict, and memory is written only by                            plans they produced, repeat executed steps, and act inconsistently
                                         verification outcomes, so that a rejection localizes the level that                         with the preceding thought [22]; and token consumption grows
                                         introduced the fault and an agent halts by declining rather than                            quadratically because the full history is resubmitted each turn [7]. A
                                         by exhaustion. Each verifier separates a zero-cost deterministic                            larger budget does not help: the agent commits to an unproductive
                                         gate from an optional LLM judge, allowing the contribution and                              trajectory early [8].
                                         cost of each to be measured independently. We report a pilot study                              Existing work addresses the symptoms rather than the structure.
                                         implementing the acceptance-level and unit-level verifier pairs,                            Planning and efficiency methods change what the agent reads or
                                         comparing five configurations that share one executor, tool set, and                        how far ahead it looks [7–10], and prompting strategies improve
                                         scorer and differ only in their verification components, on the four-                       how it reasons [3, 4], but neither inspects the result. Where checking
                                         hop stratum of MuSiQue with an 8B-parameter backbone. Across                                does exist, it is the agent checking itself [11, 12], which is the
                                         47 executions, the two unverified configurations answered none                              configuration that Huang et al. [14] report to fail and that Zheng et
                                         of ten questions, every run ending at a step cap or provider token                          al. [15] report to be biased. Table 1 summarizes the four gaps that
                                         limit; the verified configuration without a planner answered eight                          remain and how this work addresses each; the pilot closes G3 and
                                         of ten and abstained on the rest. Deterministic gates produced eight                        makes partial progress on two others.
                                         of the nine observed corrections at zero marginal cost, and planning                            Our response is architectural: we argue that the missing struc-
                                         degraded performance once verification was present. These results                           ture is a verification layer, and that software engineering already
                                         characterize termination behavior rather than accuracy at scale; we                         provides its template. Software engineering separated construction
                                         outline a twelve-month plan for completing and evaluating the full                          from certification decades ago, and the V-model pairs each design
                                         architecture, including the integration-level pair the pilot omits.                         stage with a test stage of matching scope. We transfer that structure
                                                                                                                                     to LLM agents. It is the architecture, rather than the pilot study,
                                                                                                                                     that this line of work ultimately seeks to establish.
                                         1    Introduction
                                         An LLM agent is a language model in a control loop: it receives a
                                         goal, invokes tools, and continues until it decides it has finished.                        1.1   What “verification” means here
                                         The prevailing design is ReAct [1], which extends chain-of-thought                          The term verification is used loosely in the agent literature, covering
                                         prompting [2] to an interactive setting by alternating a Thought,                           self-critique, self-consistency, confidence estimation, reranking, and
                                         which modifies only the model’s context, with an Action, whose                              formal proof; in LLM training it now also names reward models
                                         Observation is appended to that context. Most deployed frameworks                           scoring reasoning steps [16]. We use it in neither sense but in the
                                         are this loop with a tool registry attached [5, 6], and the pattern is                      software-engineering one [41], and we claim no formal guarantees:
                                         now common in software engineering [36, 37]. The design concen-                             our checks decide predicates on one artifact of one execution, as
                                         trates four responsibilities in one model and one prompt: selecting                         in runtime verification [42], not properties over all executions. A
                                         the overall strategy, selecting each action, formatting that action,                        verification act satisfies four conditions.
                                         and judging whether the resulting observation is sufficient. No
                                         component outside the loop can reject the loop’s output.
                                                                                                                                           • V1, externality: the verdict comes from a component distinct
                                         ∗ Ali Afoud completed a B.Sc. at the University of British Columbia (Okanagan campus,
                                                                                                                                             from the one that produced the artifact: a restricted-input
                                         Kelowna) and conducted this work as an independent researcher. Ali is currently                     invocation, ordinary program logic, or, preferably, a sepa-
                                         seeking opportunities for graduate study.                                                           rate model.
                                                                                                                                 1
                                                                                                                                         Ali Afoud and Jie JW Wu


                                                          Table 1: The four gaps this work addresses.

           What the literature does                          The gap                                         Our fix
 G1        The model that produced the output also           No agent has a checker outside the loop         Verifiers are separate components. The controller
           checks it [11, 12].                               whose verdict it must obey. Self-checking       enforces their verdicts, so the agent cannot pro-
                                                             without external feedback degrades accu-        ceed past a rejection.
                                                             racy [14, 15].
 G2        External checks exist, but for one artifact       None pairs checks to the levels of a specifi-   One verifier per level. A rejection names the level
           type: a reasoning step [16], a program [17].      cation, so a rejection cannot say which stage   that failed, and only that level is redone.
                                                             broke, and recovery means starting over.
 G3        Systems mix free structural checks with LLM       Nobody has measured what each half con-         Gates and judges are separate stages, and every
           judgement and report the combined effect.         tributes, so the layer cannot be priced.        correction is attributed to one of them.
 G4        Context is trimmed to fit a budget [7, 8].        Nothing decides what deserves to be carried     Only verdicts write memory. Accepted results
                                                             forward: verified and failed work are resub-    go to a ledger, rejections to an index keyed by
                                                             mitted alike.                                   component and cause.

      • V2, authority: the verdict is binding and enforced by the                  a test layer is not an optimization adopted when time permits; it
        controller; it is not returned as advice the generator may                 is structural, and its absence is a defect in the process. We argue
        ignore.                                                                    that agent systems are in that state now. Concretely, an agent built
      • V3, pairing: each verifier inspects artifacts at exactly one               to this proposal returns exactly one of two things: an answer that
        specification level, so the level at which a rejection fires               named verifiers accepted, or an abstention naming the level that
        identifies where the fault was introduced and scopes the                   refused and the evidence it saw—never an answer no component
        retry.                                                                     but its author has inspected, and never a stop forced by a token limit.
      • V4, bounded termination: each level’s rejection budget is                  The V-model pairing is what provides these guarantees: specifica-
        finite, and exhausting it yields an abstention naming the                  tion levels, a verifier paired with each level, deterministic control of
        level that failed, not a degraded answer.                                  every transition, and memory written only by verdicts. The target
                                                                                   regime is the one in which agents are simultaneously least reliable
    Three terms recur. A gate is a deterministic verifier written as
                                                                                   and most in demand: long-horizon tasks with many interdependent
program logic—a regular expression, a set-membership test, or, in
                                                                                   components, where one unchecked intermediate result contam-
code, a compiler or test runner; it costs nothing per invocation
                                                                                   inates everything downstream. We do not claim that this paper
and is self-consistent, though determinism buys repeatability, not
                                                                                   establishes O2. We claim that O2 is well posed, that it is a candidate
correctness: a gate passes any artifact wrong in a way its predicate
                                                                                   for a standard rather than one more technique, and that this paper
does not express (§3.5). A judge is a model invocation posed one
                                                                                   provides its first measurement.
question that no gate can answer; its authority derives from the
                                                                                      Three observations make O2 plausible rather than merely appeal-
controller that enforces its verdict, not from any assumed reliability
                                                                                   ing. First, most of the layer is free: the deterministic half produced
of the model (§6.4). A guard is loop control rather than verification:
                                                                                   eight of the nine corrections in our study at zero marginal cost. Sec-
it decides whether an action is re-executed, whether unparseable
                                                                                   ond, the layer does not require a stronger model: the gates worked at
output ends the run, and how much of an observation enters the
                                                                                   the 8B scale, at which the executor itself barely worked. Third, the
transcript, but it evaluates nothing for correctness. The third term
                                                                                   structure is already validated in the discipline it is borrowed from,
matters because guards and gates are easily conflated and, in the
                                                                                   and the evidence against self-correction [14, 15] argues for exter-
pilot, confounded (§5.2).
                                                                                   nalizing the check rather than against checking. The counterweight
                                                                                   is our own planning result (§5.3): adding a decomposition stage
1.2   Objectives                                                                   without the verifier meant to check it made the system markedly
We pursue two objectives of different scope, stated separately be-                 worse, so the structure may be adoptable only as a whole—a cost
cause the evidence for each differs.                                               the plan in §8 must assess.
   O1, near-term: a minimal verification layer is a cheap and
near-universal improvement to ordinary agents on ordinary
tasks. A small set of deterministic checks—costing no model calls                  1.3    The pilot, and its scope
and expressible in a few hundred lines of ordinary code—changes                    The pilot study implements the outer (L1/R3) and inner (L3/R1) pairs
the behavior of a conventional ReAct agent out of proportion to                    of the architecture and compares five configurations that differ by
its cost: primarily by making the agent stop for a stated reason,                  one component at a time, so that every correction can be attributed
and secondarily by making it more accurate. The claim’s scope is                   to the component that caused it. Its research questions test O1
deliberately modest—short tasks, one model tier, one task family—                  directly and bound O2 from below. RQ1: What does a deterministic
and if it holds, the recommendation is unconditional, because the                  verification layer do to task success and to termination behavior?
layer is free at run time and does not depend on model capability.                 RQ2: What does an LLM judge add beyond the gates? RQ3: Does
   O2, long-term: verification should be a standard architec-                      planning still help once verification is present? RQ4: What does
tural commitment for agent systems. In software engineering,                       each component cost?
                                                                               2
Verification as an Architectural Layer for LLM Agents


    We designed the study around silent errors: answers that are              detection methods range from sampling-based consistency [19]
wrong but delivered without any indication that the chain failed.             to attribution against context spans [20], and our deterministic
At the model scale we study, that failure mode did not occur—the              grounding check is the simplest member of that family, testing
unverified configurations never advanced far enough to be confi-              whether the answer occurs in any returned observation. For the
dently wrong, and instead collapsed structurally. The contribution            task domain, MuSiQue [24] was constructed so that single-hop
therefore shifted to termination behavior: whether an agent halts for         shortcuts fail, which is why we adopt it over HotpotQA [23]; agen-
a stated reason or continues until refused externally, a property that        tic approaches to multi-hop retrieval include Self-Ask [26] and
matters comparably for deployment. The silent-error hypothesis                IRCoT [25]. Broader agent benchmarks [30, 31] report that long-
is reported as untested at this scale, with qualitative observations          horizon tasks fail for structural reasons and that single-attempt
at larger scale (§6.2). The evidence base is 47 executions over five          accuracy overstates deployed reliability.
items with one backbone, so all quantitative statements are direc-
tional; the middle pair (§3.4) and the memory schema (§3.3) are               3     The Proposed Architecture: ReAct under the
specified but not built.                                                            V-Model
    In summary, this paper makes the following contributions:
                                                                              3.1    Levels and their paired verifiers
      • an architecture that treats verification as a layer of an agent       Figure 1 shows the motivating frame and Figure 2 the architecture
        system, pairing each specification level with a verifier under        it yields: specification levels descend on the left, verifiers ascend
        a deterministic controller (§3);                                      on the right, and each verifier is paired with exactly one level, so
      • a definition of verification for agents (V1–V4) separating            the level at which a failure is caught identifies the level at which it
        gates, judges, and guards, which makes each half of the               was introduced.
        layer separately measurable (§1.1);                                      L1, requirements: the request plus a machine-usable statement
      • a pilot study of the deterministic core: five configurations,         of what would satisfy it, such as the expected answer type or, in
        47 executions, every correction attributed to its component           code, the failing test that must pass. L2, decomposition: the subtasks,
        (§5);                                                                 their order, the data flow between them, and each one’s completion
      • a twelve-month plan that supplies what the pilot lacks and            condition; this is where most long-horizon failures are introduced,
        moves to a code domain where the integration pair can be              since a decomposition that mis-binds one subtask to another can-
        exercised (§8).                                                       not be repaired downstream. L3, step specification: one tool, one
                                                                              argument, one expected result type; the only level the executor sees
   Workshop positioning, and the feedback we seek. This paper is a            in full.
pilot, submitted to JAWs for feedback on experimental design before              R1, unit inspects one observation against the L3 step that re-
the larger study is committed to, and we would value disagreement             quested it. R2, integration inspects the assembled intermediate re-
on three points: (i) gates and guards are confounded (§5.2)—is sepa-          sults against L2: do references resolve, do types compose, do the
rating them the right next controlled condition, or should scaling            parts concern the entities the decomposition assumed. R3, accep-
across model tiers come first? (ii) the judges are the same model that        tance inspects the final answer against L1.
produced the work, and two repairs are available (§6.4)—a stronger
judge above a weaker executor, or a judge restricted to questions             3.2    Runtime properties
the deterministic layer can ground: which makes the better second             Three properties of the architecture are load-bearing. First, the
study? (iii) the integration verifier needs a task family with assem-         controller is the only stateful component: it holds the current level,
bled artifacts, for which we propose SWE-bench—would a smaller                the per-level budget, and the artifact store, and the generative
domain with cheaper ground truth serve better?                                components are called as functions that return content. Second,
                                                                              every verifier is split: the gate half runs first and costs nothing, and
2    Background                                                               the judge half runs only on artifacts the gates have cleared, and only
Verification and validation are distinct activities with distinct ar-         at levels whose failure class is semantic; this split is what makes the
tifacts [41]. In the V-model, each design stage is paired with a              two halves separately priceable. Third, rejection routes to the paired
test stage of matching scope: unit tests examine the detailed de-             level: R1 re-issues one step; R2 returns to L2 and re-decomposes,
sign, integration tests examine the architecture, and acceptance                             L1 Requirements
                                                                                                                                   is checked by
                                                                                                                                                                      R3 Acceptance
                                                                                             what “done” means                                                         answer vs. L1
tests examine the requirements. Falcão et al. [43] report nearly two
decades of its use as a framing device whose stage transitions act
                                                                                                     L2 Architecture                                         R2 Integration
as quality gates, and Wu [44] finds, from practitioner interviews                                    the moving parts                                       parts fit as L2 said


on ML-enabled systems, that layered decomposition, explicit re-
                                                                                                           L3 Detailed design                             R1 Unit
sponsibility boundaries, and consistent verification across levels                                       exact steps & arguments                   result vs. one L3 step

correspond to those systems’ failure modes. Our proposal rests on
the observation that an agent’s control loop is a delivery process of                                              Execution: one Thought, one Action,
                                                                                                                  one observation. The only layer that acts.

this kind—run at inference time and at high frequency—but built
without the corresponding certification structure.                            Figure 1: The motivating frame. Solid arrows show the flow of work; dotted
                                                                              lines show which verifier checks which specification. The pilot implements
   The failure mode that model-based verification targets, a flu-
                                                                              the outer pair (L1/R3) and the inner pair (L3/R1) only.
ent, confident, and unsupported answer, is well characterized [18];
                                                                          3
                                                                                                                                                                                                                                    Ali Afoud and Jie JW Wu


                                                                 Context store: success ledger · failure index                                                    Answer or abstention + failing level
                                                               written only by verifier verdicts; read on assembly                                                    + the evidence inspected




                                                                                                                                                                             R3 Acceptance
                                  L1 Requirements
                                                                                                                                                                      gate: present, typed, grounded
                           the request; what counts as done
                                                                                                                                                                    judge: evidence entails the answer




                                                                                      level · budget · retry · stop
                                                                                       Deterministic controller
                                                                                                                                                                             R2 Integration
                                L2 Decomposition
                                                                                                                                                                 gate: references resolve, types compose
                              subtasks, order, data flow
                                                                                                                                                                  judge: parts concern the same entities




                                                                                                                                                                                R1 Unit
                                     L3 Step spec.
                                                                                                                                                                  gate: non-empty, parses, no tool error
                           one tool, one argument, one type
                                                                                                                                                                   judge: observation answers the step




                                                                             Executor (ReAct)
                                                                  one Thought, one Action, one Observation


Figure 2: The architecture. Dotted lines are the controller’s mediation: no artifact reaches a verifier and no verdict reaches a generator except through it, and
it alone reads and writes the context store (§3.3). Each verifier is a free deterministic gate followed by an optional LLM judge invoked only on what the gate
cleared; a rejection routes to its paired level, and an exhausted budget yields an abstention naming that level. The pilot implements the R3 and R1 rows only.

discarding only what is downstream of the mis-binding; R3 returns                                                         Table 2: The context schema. The executor row is what makes a subtask a
to L1 or, once the budget is exhausted, abstains. The system’s output                                                     new input rather than a continuation.
is therefore a triple: an answer or an abstention, the level of the last                                                   Role                   Reads                                                                   Never reads
rejection, and the evidence inspected.                                                                                     Planner (L2)           L1; inventory of tools and compo-                                       any execution output
    One consequence holds by construction rather than by model be-                                                                                nents
                                                                                                                           Designer (L3)          L2; this component’s slot and con-                                      sibling implementations
havior. Bounded termination with cause: budgets are finite constants                                                                              tract
and every transition is decided by finite program logic, so every run                                                      Executor       (one    its objective; the contract it must                                     L1, L2, sibling code, every earlier
                                                                                                                           subtask)               honor; its checks; its own failure                                      transcript
terminates within bounded steps in one of exactly two states—an                                                                                   entries
                                                                                                                           Gates                  the artifact and the one condition                                      everything else
accepted answer or an abstention naming the failing level—under                                                            Judges R1–R3           the artifact and its paired specifica-                                  every other level, and all transcripts
no assumption about the backbone; the uncapped collapse of §4 is                                                                                  tion level
                                                                                                                           Controller             the whole state                                                         —
what its absence looks like.

                                                                                                                          instead of by trajectory length, and abstention becomes scoped,
3.3   Memory: what each component may remember                                                                            since work banked in the ledger survives a component’s failure.
In a ReAct loop the transcript is the memory: every thought, action,                                                      Neither is implemented in the pilot, which keeps a conventional
observation, and failed attempt is resubmitted on each turn, which                                                        transcript with a truncation guard; §8 schedules the schema as an
is why token consumption grows quadratically [7] and why, late in                                                         ablation.
a task, most of what the model reads concerns steps it has already                                                                                                                 Assembler (controller)
                                                                                                                                                                           builds the context to the role’s schema
finished or already got wrong. Nothing in the loop decides what
belongs there. Our design replaces accumulation with assembly: the                                                                                                             Context for ONE invocation
                                                                                                                                                                                objective · contract · checks
controller owns two stores, a verdict is the only event that writes                                                                                                              · this component’s failures

to either, and each invocation receives a context built to a declared
schema (Table 2, Figure 3).                                                                                                                                                     Agent produces one artifact


    The success ledger is append-only and written only when a ver-
                                                                                                                                                                                    Verifier: gate, then judge
ifier accepts: the subtask, the condition it satisfied, the accepted
output or interface, and a pointer to the evidence; rejected attempts                                                                                                      accept                                reject



and raw transcripts never enter it, so it is by construction the set                                                                                Success ledger                                                            Failure index
                                                                                                                                                 accepted artifacts only                                                   component × condition
of steps that moved the task forward. The failure index is keyed by
component and condition, recording which check rejected, why,                                                             Figure 3: The write path. A verdict is the only event that writes memory,
and what the retry did; a retry receives only the entries match-                                                          so a rejected attempt survives as its verdict and not as a transcript, and the
ing its own component and condition, which turns a pile of failed                                                         assembler reads back only what Table 2 permits.
attempts into a line reading rejected twice by the type gate for the
same missing field and makes repetition a stopping condition the
controller can read. Isolation makes both stores usable: the executor                                                     3.4     What is new, and what the pilot omits
is invoked per subtask, and a subtask is a new input rather than                                                          Each ingredient of the architecture has precedent; the arrangement
a continuation, receiving its objective, contract, and checks—and                                                         does not. Deterministic control of traversal appears in EoG [22],
none of the requirements, architecture, sibling implementations, or                                                       external per-step signals appear in process supervision [16] and
earlier transcripts.                                                                                                      interpreter feedback [17], and model-based critique appears in Re-
    Two consequences follow, both design expectations rather than                                                         flexion and Self-Refine [11, 12]. What is absent from all of them is
results: the executor’s context is bounded by the largest subtask                                                         a verification subsystem that is stratified by specification level, so
                                                                                                                      4
Verification as an Architectural Layer for LLM Agents


that rejections localize; external and binding by construction, so                       R1 the patch applies, the file parses, its own tests pass. Free,
that the checked party cannot overrule the check; split into free                           and no model involved.
and paid halves at every level, so that the cost of judging becomes                      R2 the rest of the suite. The fix passes its own test and breaks
an empirical question; and coupled to a memory written only by                              three that parsed the old format: every edit is correct alone,
verdicts. O2 is the claim that this arrangement, not any one part, is                       the assembly is not. Control returns to L2, not to the execu-
what turns an agent into a component other software can call.                               tor, and only the edits downstream of the revised contract
   The pilot omits the middle (L2/R2) pair because multi-hop ques-                          are redone.
tion answering assembles nothing: every subtask is a retrieval re-                       R3 the original failing test, plus the one question no gate can
turning a string, so an integration verifier has nothing to inspect                         answer: does the patch fix the issue, or only the test that
beyond what L3/R1 already compares. This is a property of the                               came with it?
task family, not of the architecture, and it is why §8 moves to code,
where assembled artifacts and executable ground truth both exist.                     If an edit is rejected three times by the same gate, the run stops
§3.5 presents a pilot failure that only an integration verifier could              with failed at R1, edit 2, patch does not apply, keeping what was
have caught.                                                                       already accepted. A monolithic agent emits patches until its budget
                                                                                   ends and returns a transcript in which nothing separates the useful
                                                                                   attempt from the discarded ones.
3.5    Worked example: a four-hop question
The item asks for the son of the Italian navigator who explored,
for England, the eastern coast of the continent on which Ignacio                   3.7    The pilot implementation
Esparza’s birthplace lies; the gold answer is Sebastian Cabot. A                   The implemented pipeline (Figure 4) is Figure 2 without the R2 row
VPG run produced this accepted plan (L2), with what each subtask                   and without the context store. Three principles govern the imple-
returned:                                                                          mentation. First, control resides in program logic: steps, retries, and
         1. Find the region where Ignacio Esparza was born.
            → Guadalajara, Jalisco, Mexico (correct)                               termination are decided in ordinary code bounded by named con-
         2. Find the navigator father of the person whose name is associated       stants. Second, inexpensive checks precede expensive ones, so that
         with the region in the result of subtask 1.                               a judge is paid for only where gates cannot decide. Third, failures
            → Giovanni Battista Caviglia (wrong)
         3. Find the explorer who explored the east coast of the region in         are reported rather than reinterpreted, because silently reformu-
         the result of subtask 2.                                                  lating a step into a weaker objective is the mechanism by which
            → Lieutenant James Cook (wrong, inherited)                             agents come to fabricate values.
         4. Find the navigator whose name is the result of subtask 3.
            → no answer; retrieval continues until the budget ends                    Eleven gates examine the plan: nine structural checks (parseabil-
   Every R1 check passes at every step: each subtask returned a                    ity, length, duplicate subtasks, self-, forward and dangling refer-
non-empty, correctly typed result, free of tool errors and present in              ences, terminal step, typed completion conditions, tool existence)
a retrieved paragraph, and R3 never fires because no final answer is               and two that apply only to arithmetic questions (single-expression
produced. The fault lies at L2 and is invisible to both implemented                form and numeric coverage). Seven examine an answer (presence,
pairs: subtask 3 is defined over the result of subtask 2 rather than               non-emptiness, non-answers, consistency with the alternatives a
over the question, so the distractor matched at step 2 propagates.                 comparison offers, tool errors, type agreement, and optionally oc-
This is an integration failure in the V-model sense—individually                   currence in an observation). The plan judge asks whether the steps,
valid units assembled into an invalid whole. An R2 gate comparing                  assuming each succeeds, would answer the question; the answer
the type subtask 2 produced (a person) with the type subtask 3                     judge asks whether the evidence entails the answer. Three guards
presupposes (a region) would reject the chain at step 3 with no                    operate inside the executor—a repeated action is served from cache
model call and return control to L2 for re-decomposition; the judge                with a warning, unparseable output ends the run after bounded
half would handle the residual case in which types agree but entities              attempts, and observations are truncated before entering the tran-
do not. Whether type-composition gates fire often enough to pay                    script; per §1.1 these are loop control, not verification.
for themselves is an empirical question the plan places first among
the code-domain experiments.                                                       Table 3: The five configurations; internal labels in parentheses match the
                                                                                   released logs. All share one executor, tool set, retriever, scorer and backbone,
3.6    Worked example: fixing a repository issue                                   so adjacent pairs differ by one component.
A SWE-bench task supplies a repository, an issue, a test the patch                 Config.      Composition               Plan      Guards       Gates     Judges
must make pass, and a suite that must keep passing [32]—two                        N (A)        plain ReAct                 –          –           –          –
test sets at different specification levels, precisely the structure the           NP (B)       ReAct + planner            yes         –           –          –
                                                                                   VG (C1)      verified, no planner        –         yes         yes         –
architecture exploits. Consider an issue reporting that timestamps                 VPG (C0)     + planner + plan gates     yes        yes         yes         –
lose their timezone offset:                                                        VPGJ (C)     + LLM judges               yes        yes         yes        yes

      L1 the issue plus its failing test.
      L2 two files change, the serializer and the parser, and their                   Table 3 defines the configurations. VG proves central to the
         contract is that a timestamp carries an offset.                           analysis: it has no planner—the question itself is the single task,
      L3 one edit at a time, each with the tests that cover it. The                carrying a completion condition derived from its interrogative form,
         executor is given one edit, its contract and its tests—not the            so that “Who . . . ” yields a person or organization, not one of their
         issue, not the repository, not the previous edit’s transcript.            attributes. VG is the minimal configuration that retains verification.
                                                                               5
                                                                                                                                                                                                                           Ali Afoud and Jie JW Wu


                                                                        reject
                                           reject: regenerate plan




                                     Planner                         Plan            pass
                                                                                              Plan judge     pass       Executor loop                        Answer            pass
                                                                                                                                                                                      Answer judge   pass
                                                                                                                                                                                                              Answer
                         Question
                                      (LLM)                          gates                      (LLM)                 Thought → Action                        gates                      (LLM)               or abstain
                                                                                                                       → Observation


                                                                                                                                        reject: retry step

                                                                                                                                                                 reject

                                                                             Deterministic controller: owns every transition, budget, retry and stop. Agents propose content only.



Figure 4: The implemented pipeline. Diamonds are deterministic checks (no model cost); green rounded boxes are LLM judges, invoked only on gate-cleared
artifacts; dashed arrows are bounded rejection paths. When plan regeneration is exhausted, the system falls back to executing the question as a single task (§5).

4    Experimental Design                                                                                                      cap removed, and all ten of those runs terminated without scoreable
Establishing O2 requires five methodological ingredients, most of                                                             output, each invoking the same tool until the provider’s token limit
which the pilot lacks by design: (i) assembled artifacts, without                                                             ended the process. Second, repeated passes for VG and VPG repro-
which R2 has nothing to inspect; (ii) executable ground truth, with-                                                          duced the first pass exactly—decoding determinism at temperature
out which a verifier’s mistakes cannot be distinguished from the                                                              0, not stability—so the per-run costs in Table 5 are computed over
scorer’s; (iii) several model tiers, because each half of the layer ad-                                                       distinct logged traces. Third, the plan judge in VPGJ rejected every
dresses a failure class that appears at a different scale; (iv) abstention-                                                   plan in all five of its enabled runs, and the two runs with the judge
aware measures, because accuracy alone cannot summarize a system                                                              disabled both returned no answer; this is the smallest cell in the
that is permitted to decline; and (v) a switchable memory schema,                                                             study and is reported separately.
without which context management and verification are measured
together. The plan in §8 is organized around supplying all five. The                                                          5        Results of the Pilot
pilot has the fourth and part of the third: it is a feasibility study,                                                        5.1         Execution outcomes (RQ1)
showing that architectural differences are measurable at all when
every other component is held constant.                                                                                       Table 4: Execution accounting over all 47 runs. No configuration produced
                                                                                                                              a silent error, so that column is omitted.
   Task, tools, model. MuSiQue-Answerable [24], four-hop stratum:
twenty paragraphs per item, of which roughly four support the                                                                 Config.                              exec.              score.          crash               corr.    abst.      cov.
answer and the rest are mined distractors. We use five items, one                                                             N (plain ReAct)                             10                5                5               0         5      0.00
                                                                                                                              NP (+ planner)                              10                5                5               0         5      0.00
of which also appears in a four-paragraph gold-context variant as a                                                           VG (verified)                               10               10                0               8         2      0.80
control of reduced difficulty. Two tools are bound to a single item’s                                                         VPG (+ planner)                             10               10                0               1         9      0.10
paragraphs: retrieve[query], a BM25 [28] index returning three                                                                VPGJ (+ judges)                              7                7                0               4         3      0.57
query-centred excerpts with indices, and read_paragraph[idx]. A                                                               Total                                       47               37               10              13        24        —
single allow-list function is the only path from harness to tool, emit-
ting nothing beyond index, title, and text, so the gold answer and                                                               N and NP answered none of the ten questions: all ten scoreable
the supporting-paragraph annotations cannot reach the retriever.                                                              runs hit the 12-step cap without once invoking finish, all ten
Every role in every configuration runs llama-3.1-8b-instant at                                                                uncapped runs continued until the provider refused them, and the
temperature 0, so differences are attributable to architecture and                                                            study’s entire 21% crash rate falls on these two configurations. VG
not capacity; the executor budget is 12 steps unless stated otherwise,                                                        answered eight of ten, using fewer steps than N (Table 5), and
over two passes.                                                                                                              abstained on the two items it could not resolve instead of guessing.

    Measures. A verified configuration may decline to answer and                                                              5.2         A confound between guards and gates
an unverified one cannot, which a single accuracy figure cannot                                                               One qualification applies to every result below. The verified con-
represent. We therefore report a partition summing to unity: correct;                                                         figurations differ from N and NP in two respects: the gates, which
silent error (an answer was produced and is wrong—the consequen-                                                              are verification, and the three guards, which are loop control. The
tial case, since nothing downstream can distinguish it from a correct                                                         collapse mode of §6.1, in which an agent invokes the same tool
answer); and abstention; plus coverage, the proportion of scoreable                                                           until an external limit intervenes, is plausibly prevented by the
runs that answered. Scoring follows MuSiQue’s SQuAD-style pro-                                                                duplicate-action guard alone, which refuses the second identical
cedure [29]. A correction is a rejection whose retry produced a                                                               invocation without consulting any gate. We therefore cannot at-
different answer that was then accepted; the change requirement                                                               tribute the observed difference to verification as such; separating
matters, since accepting a resubmitted identical answer is the judge                                                          the two is the first ablation in §8.
contradicting itself.
   Execution accounting. The study comprises 47 executions: five                                                              5.3         The effect of planning (RQ3)
items over two passes for four configurations, plus seven for VPGJ,                                                           VPGJ with the plan judge enabled and VG produced identical out-
whose second pass was replaced by two runs with the plan judge                                                                comes: the judge rejected all five plans, so VPGJ fell back to execut-
disabled to observe an executed plan. Of these, 37 were scoreable                                                             ing the question as a single task and became VG with additional
and 10 were not, a distribution that is itself a result (Table 4). Three                                                      overhead. Partitioning every run by whether a plan was executed
points follow. First, the second pass for N and NP ran with the step                                                          makes the effect explicit. Twelve runs executed a plan, of which
                                                                                                                       6
Verification as an Architectural Layer for LLM Agents


Table 5: Mean cost per scoreable run over distinct logged traces. Executor                     about a third of the necessary evidence, because the executor issues
steps are the architecture-neutral comparison; total calls include planner                     sentence-form queries against a lexical index. VG answered eight
and judge overhead.                                                                            of ten while reaching complete evidence in only one run of five, so
Config.               LLM calls        exec. steps         prompt tok.     compl. tok.         several items were resolved from a subset of the annotated evidence.
N                          12.0    12.0 (all at cap)            18,891               598           This ceiling bounds verifier calibration in both directions. The
NP                         13.0    12.0 (all at cap)            11,180               752       judge never sees the gold answer or the supporting-paragraph
VG                         11.8        11.8 (3–21)              19,511             1,150       annotations, so when required evidence is never fetched it can reject
VPG                        15.2        14.2 (8–20)              17,226               840
VPGJ                       14.8        10.0 (4–18)              20,943             1,210       an answer the scorer would have accepted, inflating abstentions.
  judge disabled           23.0                 20.0            28,609             1,464       We observed no such false negative: the three judge rejections
                                                                                               concerned intermediate results the scorer does not evaluate, and
Table 6: Rejections and corrections across the logged traces; identical re-                    every final-answer abstention came from a gate observing that no
peats are not double-counted. A correction required the retry to produce a                     answer existed. We observed no false positives either, but attach
different answer that was then accepted.                                                       little weight to that, since no configuration produced a confidently
Source                   rejections      corrections           rate      marginal cost         wrong answer for a judge to accept.
Deterministic gates               24                   8       0.33      none
LLM judges                         3                   1       0.33      one call each         6     Discussion
                                                                                               6.1   Unverified agents do not abstain
one was correct (a success rate of 0.08), at a mean of 15.6 executor
                                                                                               No unverified execution ended with a refusal: the recorded ab-
steps; fifteen runs executed no plan, of which twelve were correct
                                                                                               stentions of N and NP in Table 4 are the harness observing that
(0.80), at a mean of 10.9 steps. Planning thus cost 43% more steps
                                                                                               the loop ended without invoking finish once the step cap inter-
for roughly one tenth of the success rate.
                                                                                               vened, and removing the cap—our artifact, not ReAct’s—produced
   Two mechanisms appear in the traces. Budget fragmentation:
                                                                                               the uncapped collapse of §4. The verified configurations differ in
four subtasks under a twelve-step budget allow three steps each,
                                                                                               kind: every termination is a decision with a recorded cause. Inde-
the minimum viable trajectory (retrieve, read, finish), leaving no
                                                                                               pendently of accuracy, halting with a stated reason is what lets a
capacity to reformulate a failed query, and most planned failures
                                                                                               component be composed into a larger system; we therefore regard
end at the first or second subtask. Error propagation: the chain fails
                                                                                               the deterministic half as close to a precondition for unattended
at its first incorrect resolution, as §3.5 shows in full, and no gate in
                                                                                               deployment, subject to the confound of §5.2.
the implemented system can detect it, since each subtask answer is
present, non-empty, typed and grounded and only the composition
is wrong; no configuration solved that item in any run. This is the
                                                                                               6.2   Behavior under a stronger backbone
missing L2/R2 pair appearing as a measured result rather than an                               No confidently wrong answers occurred, so the silent-error hypoth-
argument.                                                                                      esis could not be tested; we report this as a null result. Using the
                                                                                               model on which the judge contributes least was deliberate: the 8B
5.4    Cost (RQ4)                                                                              experiment establishes a lower bound. When reasoning capacity is
                                                                                               identical and low across configurations, whatever separates them is
The distribution matters more than the mean: N and NP sat at the
                                                                                               attributable to guards, gates, and control flow; at 70B the backbone
cap in every scoreable run, having no way to stop earlier, whereas
                                                                                               absorbs the failures the architecture exists to handle, measuring
VG ranged from 3 to 21 steps—resolving one item in three and
                                                                                               the model instead of the design. The cost is that the judge’s target
spending its full allocation plus a retry on the item it declined—the
                                                                                               failure class does not arise.
observable signature of adaptive termination.
                                                                                                  Exploratory runs on two larger backbones (llama-3.3-70b-
                                                                                               versatile and qwen/qwen3.6-27b), outside the controlled set and
5.5    Attribution of corrections (RQ2)
                                                                                               requiring confirmation, indicate where that failure class does arise.
The two halves of the layer show a comparable success rate per                                 With a stronger backbone, N and NP stop collapsing structurally:
rejection but differ by an order of magnitude in volume: gates                                 they hold the action format, terminate, and produce answers. On
fired 24 times, judges three times, with no judge reversal (rejecting                          harder items, however, the loop commits to a plausible intermediate
and then accepting the identical answer). The plan judge behaved                               entity and returns a fluent answer with no indication that the chain
differently from the answer judge: it rejected all five plans with a                           broke. A recurring proportion of these answers were rejected by
recurring objection of the form “the plan does not guarantee that 𝑋 is                         the answer judge and by no gate, for reasons citing exactly what
the same as 𝑌 ”, twice identically across both regeneration attempts.                          gates cannot evaluate: the evidence does not support the answer,
No plan can guarantee what a retrieval will return, so regeneration                            the observation concerns a different entity, or a plausible name
cannot satisfy such an objection, and the fallback to unplanned                                was inferred rather than retrieved—the intrinsically semantic class
execution becomes deterministic.                                                               the hallucination literature [18, 19] targets. The implication is a
                                                                                               division of labor: gates are mandatory, being free and covering the
5.6    Retrieval ceiling                                                                       malformed, empty, mistyped, repeated, and placeholder outputs
The agent reached 67% of the required paragraphs on average,                                   that dominate at every scale we examined; judging should be de-
and all of them in 25% of runs, which bounds every configuration:                              ployed selectively, where unsupported but well-formed output is
architectural differences are measured on a retriever that omits                               the anticipated failure.
                                                                                           7
                                                                                                                                                  Ali Afoud and Jie JW Wu


6.3   Planning and verification are partial substitutes                       in part, the integration row and the memory schema being argued
Also outside the controlled set, on stronger backbones NP consis-             for rather than tested.
tently outperformed N, in line with ReWOO and ADaPT [7, 9]; that                 Conclusion validity. With 37 scoreable runs and cells of 7 to 10,
advantage did not survive verification (8 of 10 versus 1 of 10). A ten-       no statistical inference is performed and none should be drawn;
tative explanation is that a planner’s benefit to an unverified loop is       the absent runs are not missing at random but are the crashes of
structural discipline, which guards and gates supply more cheaply;            Table 4, so N and NP appear in the outcome columns only in their
what remains is the decomposition itself, which on retrieval-shaped           capped configuration.
tasks fragments the budget and propagates the first error. The ar-               Researcher bias. One author implemented all five configurations,
chitectural reading is that a decomposition is an L2 artifact and             and scoring was not blind.
the pilot has no R2 verifier to check one; degradation from adding
L2 without R2 is what the architecture predicts. Whether planning             8      One-Year Research Plan
recovers its value once paired with integration verification is a
                                                                              Four deficiencies drive the plan: insufficient statistical power, a
question for §8.
                                                                              single model tier, a task family that cannot exercise the integration
                                                                              layer, and separate per-configuration directories. Table 7 organizes
6.4   Why self-assessment is structurally limited                             the schedule around them.
We attribute the judge’s weakness at 8B to its configuration, not
                                                                              Table 7: Twelve-month plan; half the schedule goes to code, where deter-
to prompt quality; the prompts were revised repeatedly, and the               ministic verifiers are rich and the L2/R2 row can be exercised.
final failures used the revised rubric’s own vocabulary. The judges
                                                                              Months         Work and rationale
are the same model at the same temperature, examining the same
                                                                              1–2       Consolidation, and the confound. One codebase with the configuration as a pa-
tool outputs and evaluating the same model’s work, so they share                        rameter, removing the divergence risk of §7; a dense retriever [27] to raise the 67%
the actor’s blind spots and are least reliable exactly where the actor                  ceiling. First ablation: guards without gates, gates without guards, and both ends of the
                                                                                        ladder—until those cells exist, the difference in §5 cannot be assigned to verification
is. Their available behaviors reduce to agreement, which conveys                        rather than loop control.
nothing, and unanchored disagreement, which is noise. This is the             3–4      Scale, and verifier configurations. Roughly 500 items stratified by hop count, three
                                                                                       seeds, three to five model tiers, every repeat retained; paired per-item analysis with
configuration Huang et al. [14] report to fail, and it violates V1 in                  effect sizes [38], hypotheses registered beforehand. Asymmetric and ground-truth-
spirit while satisfying it in letter.                                                  constrained verification (§6.4) as separate conditions. Second ablation: full accumulation
                                                                                       vs. ledger only vs. both stores, with tokens read per step reported alongside accuracy.
    Two designs would constitute a fair test of model-based judg-
                                                                              5–7      Transfer to code. Port to SWE-bench [32] and its agent interfaces [33], with function-
ing. Asymmetric verification places a strictly stronger model in                       level suites under rigorous test augmentation [34, 35] as a cheaper inner loop. In code
                                                                                       the gate layer becomes a compiler, type checker, and test runner, with ground truth
the judge roles above a weaker executor; judges issue one to two                       no question-answering gate can have; we expect the gate/judge balance to shift and
calls per subtask against the executor’s seven to thirteen, so the                     will re-run Table 6.

cost is modest (§6.2 provides indirect evidence in its favor). Ground-        8–10      Debugging, and the integration layer. Fault localization and repair, where a failing
                                                                                        test supplies both trigger and oracle [17]. The L2/R2 pair becomes testable at last:
truth-constrained verification allows the judge only questions whose                    individually correct units forming a broken assembly is a real repository failure
                                                                                        class invisible to unit checks (§3.5). Repository length makes the memory schema
evidence the deterministic layer supplies (e.g., whether a specified                    consequential, so its ablation is repeated with per-component isolation on and off.
span entails the answer [16, 17]); its limit is that it cannot detect a       11–12     Synthesis. Cross-domain comparison of where each half contributes, a replication
failure the deterministic layer did not already suspect.                                package of code, prompts, items, seeds and logs, and submission.

    Finally, what the judge did catch—an executor emitting the lit-
eral placeholder finish[. . . ], admitted by all seven gates—was
syntactic, and expressing it as a gate afterwards took three lines            9      Conclusion
of code. This suggests a practice: run a judge during construction,           This paper argued that LLM agents run a delivery process without
promote each recurring catch into a gate, and reserve run-time                the certification structure such a process needs, transferred the
judging for the semantic class above, which cannot be promoted.               V-model to supply that structure, and measured its deterministic
                                                                              core. The measurement is small—five items, 47 executions, one 8B
                                                                              backbone—but its central contrast is stark: without the layer, no run
7     Threats to Validity                                                     ever terminated by decision; with it, every run ended in an accepted
We follow the threat categories conventional in empirical software            answer or a reasoned abstention, and eight of nine corrections were
engineering [39, 40].                                                         free. Planning, added without its paired verifier, made the system
   Internal validity. The five configurations are implemented as              worse—the architecture’s own prediction, appearing as data.
separate directories; the executor, gates, tools, and scorer are byte-           Three uncertainties bound what this establishes, and they are the
identical across them and every run’s configuration is logged, but            feedback we seek at the workshop: whether the effect belongs to
divergence remains a risk we detected and corrected more than                 verification or to the bundled guards (§5.2); whether judges recover
once during development.                                                      their value once separated from the model they check (§6.4); and
   Construct validity. Exact-match scoring under-credits paraphrases,         whether the integration level, which no question-answering task
and the retrieval ceiling (§5.6) bounds every reported figure and             can exercise, earns its place once the architecture moves to code
may generate false negatives for the judge.                                   (§8). What we ask the field to weigh, meanwhile, is not another
   External validity. The study uses one backbone, one benchmark,             technique for a leaderboard, but whether an agent without an exter-
one task family, and the small sample of §4; §6.2 reports qualitative         nal verification layer is structurally incomplete, in the way untested
patterns, not measurements; and the architecture is evaluated only            software is.
                                                                          8
Verification as an Architectural Layer for LLM Agents


References                                                                                    [22] Jha et al., “Think Locally, Explain Globally: Graph-Guided LLM Investigations
 [1] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao, “ReAct:                 via Local Reasoning and Belief Propagation,” arXiv:2601.17915, 2026.
     Synergizing Reasoning and Acting in Language Models,” in Proc. ICLR, 2023.               [23] Z. Yang, P. Qi, S. Zhang, Y. Bengio, W. W. Cohen, R. Salakhutdinov, and C. D.
     arXiv:2210.03629.                                                                             Manning, “HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question
 [2] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi, Q. Le, and               Answering,” in Proc. EMNLP, 2018.
     D. Zhou, “Chain-of-Thought Prompting Elicits Reasoning in Large Language                 [24] H. Trivedi, N. Balasubramanian, T. Khot, and A. Sabharwal, “MuSiQue: Multihop
     Models,” in NeurIPS, 2022.                                                                    Questions via Single-hop Question Composition,” TACL, vol. 10, pp. 539–554,
 [3] X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdhery, and                   2022.
     D. Zhou, “Self-Consistency Improves Chain of Thought Reasoning in Language               [25] H. Trivedi, N. Balasubramanian, T. Khot, and A. Sabharwal, “Interleaving Re-
     Models,” in Proc. ICLR, 2023. arXiv:2203.11171.                                               trieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step
 [4] S. Yao, D. Yu, J. Zhao, I. Shafran, T. L. Griffiths, Y. Cao, and K. Narasimhan,               Questions,” in Proc. ACL, 2023. arXiv:2212.10509.
     “Tree of Thoughts: Deliberate Problem Solving with Large Language Models,” in            [26] O. Press, M. Zhang, S. Min, L. Schmidt, N. A. Smith, and M. Lewis, “Measuring
     NeurIPS, 2023. arXiv:2305.10601.                                                              and Narrowing the Compositionality Gap in Language Models,” in Findings of
 [5] T. Schick, J. Dwivedi-Yu, R. Dessì, R. Raileanu, M. Lomeli, L. Zettlemoyer, N.                EMNLP, 2023. arXiv:2210.03350.
     Cancedda, and T. Scialom, “Toolformer: Language Models Can Teach Themselves              [27] V. Karpukhin, B. Oğuz, S. Min, P. Lewis, L. Wu, S. Edunov, D. Chen, and W.
     to Use Tools,” in NeurIPS, 2023. arXiv:2302.04761.                                            Yih, “Dense Passage Retrieval for Open-Domain Question Answering,” in Proc.
 [6] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang, X. Zhang, S. Zhang, J.            EMNLP, 2020. arXiv:2004.04906.
     Liu, A. H. Awadallah, R. W. White, D. Burger, and C. Wang, “AutoGen: Enabling            [28] S. Robertson and H. Zaragoza, “The Probabilistic Relevance Framework: BM25
     Next-Gen LLM Applications via Multi-Agent Conversation,” arXiv:2308.08155,                    and Beyond,” Foundations and Trends in Information Retrieval, vol. 3, no. 4, pp.
     2023.                                                                                         333–389, 2009.
 [7] B. Xu, Z. Peng, B. Lei, S. Mukherjee, Y. Liu, and D. Xu, “ReWOO: Decou-                  [29] P. Rajpurkar, J. Zhang, K. Lopyrev, and P. Liang, “SQuAD: 100,000+ Questions
     pling Reasoning from Observations for Efficient Augmented Language Models,”                   for Machine Comprehension of Text,” in Proc. EMNLP, 2016.
     arXiv:2305.18323, 2023.                                                                  [30] X. Liu et al., “AgentBench: Evaluating LLMs as Agents,” in Proc. ICLR, 2024.
 [8] Molinari and Ciravegna, “Reason-Plan-ReAct: A Reasoner-Planner Supervising                    arXiv:2308.03688.
     a ReAct Executor for Complex Enterprise Tasks,” arXiv:2512.03560, 2025.                  [31] S. Yao, N. Shinn, P. Razavi, and K. Narasimhan, “𝜏 -bench: A Benchmark for
 [9] A. Prasad, A. Koller, M. Hartmann, P. Clark, A. Sabharwal, M. Bansal, and T.                  Tool-Agent-User Interaction in Real-World Domains,” arXiv:2406.12045, 2024.
     Khot, “ADaPT: As-Needed Decomposition and Planning with Language Models,”                [32] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan,
     arXiv:2311.05772, 2023.                                                                       “SWE-bench: Can Language Models Resolve Real-World GitHub Issues?” in Proc.
[10] “Why Reasoning Fails to Plan: A Planning-Centric Analysis of Long-Horizon                     ICLR, 2024. arXiv:2310.06770.
     Decision Making in LLM Agents,” arXiv:2601.22311, 2026.                                  [33] J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan, and O. Press,
[11] N. Shinn, F. Cassano, E. Berman, A. Gopinath, K. Narasimhan, and S. Yao, “Re-                 “SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineer-
     flexion: Language Agents with Verbal Reinforcement Learning,” in NeurIPS, 2023.               ing,” in NeurIPS, 2024. arXiv:2405.15793.
     arXiv:2303.11366.                                                                        [34] M. Chen et al., “Evaluating Large Language Models Trained on Code,”
[12] A. Madaan et al., “Self-Refine: Iterative Refinement with Self-Feedback,” in                  arXiv:2107.03374, 2021.
     NeurIPS, 2023. arXiv:2303.17651.                                                         [35] J. Liu, C. S. Xia, Y. Wang, and L. Zhang, “Is Your Code Generated by ChatGPT
[13] Y. Bai et al., “Constitutional AI: Harmlessness from AI Feedback,”                            Really Correct? Rigorous Evaluation of Large Language Models for Code Gener-
     arXiv:2212.08073, 2022.                                                                       ation,” in NeurIPS, 2023. arXiv:2305.01210.
[14] J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. W. Yu, X. Song, and D. Zhou,               [36] X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo, J. Grundy, and
     “Large Language Models Cannot Self-Correct Reasoning Yet,” in Proc. ICLR, 2024.               H. Wang, “Large Language Models for Software Engineering: A Systematic
     arXiv:2310.01798.                                                                             Literature Review,” ACM Trans. Softw. Eng. Methodol., 2024. arXiv:2308.10620.
[15] L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D.         [37] A. Fan, B. Gokkaya, M. Harman, M. Lyu, J. Mao, M. Mytkowicz, and S. Yoo,
     Li, E. P. Xing, H. Zhang, J. E. Gonzalez, and I. Stoica, “Judging LLM-as-a-Judge              “Large Language Models for Software Engineering: Survey and Open Problems,”
     with MT-Bench and Chatbot Arena,” in NeurIPS Datasets and Benchmarks, 2023.                   in Proc. ICSE-FoSE, 2023. arXiv:2310.03533.
     arXiv:2306.05685.                                                                        [38] R. Dror, G. Baumer, S. Shlomov, and R. Reichart, “The Hitchhiker’s Guide to
[16] H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J.                Testing Statistical Significance in Natural Language Processing,” in Proc. ACL,
     Schulman, I. Sutskever, and K. Cobbe, “Let’s Verify Step by Step,” in Proc. ICLR,             2018, pp. 1383–1392.
     2024. arXiv:2305.20050.                                                                  [39] C. Wohlin, P. Runeson, M. Höst, M. C. Ohlsson, B. Regnell, and A. Wesslén,
[17] X. Chen, M. Lin, N. Schärli, and D. Zhou, “Teaching Large Language Models to                  Experimentation in Software Engineering. Springer, 2012.
     Self-Debug,” in Proc. ICLR, 2024. arXiv:2304.05128.                                      [40] P. Runeson and M. Höst, “Guidelines for Conducting and Reporting Case Study
[18] Z. Ji, N. Lee, R. Frieske, T. Yu, D. Su, Y. Xu, E. Ishii, Y. J. Bang, A. Madotto,             Research in Software Engineering,” Empirical Software Engineering, vol. 14, no. 2,
     and P. Fung, “Survey of Hallucination in Natural Language Generation,” ACM                    pp. 131–164, 2009.
     Computing Surveys, vol. 55, no. 12, pp. 1–38, 2023.                                      [41] B. W. Boehm, “Guidelines for Verifying and Validating Software Requirements
[19] P. Manakul, A. Liusie, and M. J. F. Gales, “SelfCheckGPT: Zero-Resource Black-                and Design Specifications,” in Proc. Euro IFIP, 1979, pp. 711–719.
     Box Hallucination Detection for Generative Large Language Models,” in Proc.              [42] M. Leucker and C. Schallhart, “A Brief Account of Runtime Verification,” Journal
     EMNLP, 2023. arXiv:2303.08896.                                                                of Logic and Algebraic Programming, vol. 78, no. 5, pp. 293–303, 2009.
[20] Wang et al., “AttnTrace: Contextual Attribution of Prompt Injection and Knowl-           [43] R. Falcão, A. Jedlitschka, F. Elberzhager, and D. Rombach, “Experiences in Using
     edge Corruption,” arXiv:2508.03793, 2025.                                                     the V-Model as a Framework for Applied Doctoral Research,” arXiv:2407.04563,
[21] Liu et al., “QuadSentinel: Sequent Safety for Machine Learning Agents,”                       2024.
     arXiv:2512.16279, 2025.                                                                  [44] J. JW Wu, “An Exploratory Study of V-Model in Building ML-Enabled Software:
                                                                                                   A Systems Engineering Perspective,” in Proc. CAIN, Lisbon, Portugal, 2024, pp.
                                                                                                   1–11. arXiv:2308.05381.




                                                                                          9
