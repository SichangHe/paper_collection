                                            From Noisy Traces to Root Causes: Structural Trajectory Analysis and
                                                         Causal Extraction for Agent Optimization

                                                                     Ying Chang1 2 † , Jiahang Xu2 * , Xuan Feng2 ,
                                                                   Chenyuan Yang2 , Peng Cheng2 , Yuqing Yang2
                                                             1
                                                               University of Chinese Academy of Sciences, Beijing, China,
                                                                                  2
                                                                                    Microsoft Research.
                                                                     Correspondence: jiahangxu@microsoft.com


                                                               Abstract
                                             The optimization of long-horizon agents in-
                                             creasingly relies on reflection-based mecha-
                                             nisms, where a large language model (LLM)
                                             acts as an optimizer to diagnose agent failures
                                             and improve agent policies. However, real exe-
                                             cution traces are difficult to use directly for
                                             optimization: large trace collections are of-
arXiv:2607.07702v1 [cs.CL] 8 Jul 2026




                                             ten redundant and heterogeneous, making opti-
                                             mization inefficient and prone to overfitting to
                                             low-value failures; meanwhile, each individual
                                             trajectory also contains many irrelevant steps,
                                             while naive context reduction methods such
                                             as truncation or sliding windows can discard
                                             causally important evidence and produce mis-
                                             leading optimization signals. To resolve this
                                             dilemma, we introduce STRACE (Structural
                                             Trajectory Analysis and Causal Extraction), a
                                             framework that constructs high signal-noise op-
                                             timization contexts for more precise and effec-
                                             tive optimization. At the batch level, STRACE
                                             mines failure patterns to filter redundant traces        Figure 1: Comparison of context construction strate-
                                             and retain representative failures; within each          gies. Existing methods struggle with the context-noise
                                             selected trace, it performs causal localization          trade-off : (a) Full Trajectory introduces noise leading
                                             over a textual dependency graph to remove non-           to spurious correlations, while (b) Short Truncation
                                             causal steps and identify the true root-cause            fails to capture long-range causal dependencies (e.g.,
                                             module for optimization. Empirical results               linking Step 1 to Step 48). In contrast, (c) STRACE
                                             demonstrate that STRACE significantly out-               performs causal context distillation to extract a compact
                                             performs standard context-filtering baselines.           causal slice, providing a high-SNR context for precise
                                             Notably, on a challenging formal verification            optimization.
                                             task (VeruSAGE-Bench), it successfully op-
                                             timizes human-expert designed agents, deliv-             of Computer Use (Anthropic, 2024a,b) and au-
                                             ering 1.4× success-rate improvement (42.5%               tonomous software engineering (Jimenez et al.,
                                             to 58.5%). The code is available at https:               2024; Chen et al., 2021; OpenAI, 2024b), these
                                             //github.com/moomight/STRACE.                            systems are no longer mere chatbots but sophis-
                                                                                                      ticated operational units. They orchestrate com-
                                        1    Introduction
                                                                                                      plex tool usage, manage dynamic memory, and
                                        The field of Artificial Intelligence is undergoing            execute multi-step control flows to solve intricate
                                        a paradigm shift from single-turn interactions to             long-horizon tasks (Wang et al., 2024; Xi et al.,
                                        Compound Agent Systems (Zaharia et al., 2024).                2023; Schick et al., 2023). Meanwhile, the arti-
                                        Powered by reasoning-intensive models capable                 facts generated by these systems have evolved from
                                           †                                                          simple conversational logs into complex execution
                                            Ying Chang did the work during an internship at Mi-
                                        crosoft Research.                                             trajectories with reasoning chains, code execution
                                           *
                                             Corresponding author.                                    environments and state transitions. How to effec-

                                                                                                  1
tively use such trajectory information to further            tematically resolves these dual challenges through
enhance agent systems has become a critical ques-            a decoupled pipeline.
tion.                                                           First, Structural Modeling infers a compact tex-
   A predominant paradigm for optimizing such                tual dependency graph that records data and control
agent systems is reflexive optimization (Pryzant             relations among agent components as dependency
et al., 2023; Shinn et al., 2023; Yang et al., 2024),        priors. Building on this topology, Failure Pattern
which uses an LLM to diagnose agent-system fail-             Mining and Trace Filtering tackles large-scale
ures and evolve agent policies based on historical           trace heterogeneity by summarizing each batch into
feedback derived from agent trajectories. However,           statistical and structural diagnoses, then filtering
when deployed on complex long-horizon tasks,                 redundant or low-value failures using recurrence
these frameworks struggle to process the sheer vol-          and severity signals to retain a compact trace set.
ume and complexity of generated data. In realis-             Within these representative traces, Causal Local-
tic settings, batched execution trajectories contain         ization identifies the true root cause as the optimiza-
heterogeneous failures with different frequencies,           tion target and provides the causal context needed
severities, and causes (Cemri et al., 2026; Barke            for optimization: it traces dependencies backward
et al., 2026). Attempting to optimize the agent from         to discard irrelevant steps, extract a compact causal
every failed trace is computationally intractable            slice, and locate the failure’s logical origin rather
and often leads to brittle, overfitted updates. Conse-       than its manifestation node. Finally, during Induc-
quently, a mechanism is needed to aggregate these            tive Policy Optimization, STRACE uses localized
heterogeneous logs, isolate the most frequent and            failure episodes to synthesize generalized, natural
consequential failure patterns, and distill them into        language heuristics. These preventative guidelines
generalized improvements.                                    are injected exclusively into the instructions of the
   Even after representative failures are selected,          identified root-cause modules, enabling continu-
optimization within an individual trace remains              ous, safe, and cost-effective improvement without
challenging due to the context-noise trade-off (Liu          altering the underlying executable code.
et al., 2023). Existing methods often force a choice
                                                                We validate this capability on HotpotQA (Yang
between two imperfect extremes (illustrated in Fig-
                                                             et al., 2018), WebArena (Zhou et al., 2024), and
ure 1). Feeding the full trajectory (a) overwhelms
                                                             VeruSAGE-Bench (Yang et al., 2025) benchmarks,
the optimizer with irrelevant successful steps and
                                                             where STRACE significantly outperforms state-of-
low-SNR context, inviting spurious correlations
                                                             the-art baselines, notably boosting success rates
and hallucinated prompt patches (Yuksekgonul
                                                             on the rigorous VeruSAGE benchmark by an abso-
et al., 2024; Shi et al., 2023). Conversely, relying
                                                             lute 16.0% (42.5% → 58.5%). In summary, our
on short truncation (b) treats local proximity as
                                                             contributions are:
a signal of causal relevance (Agrawal et al., 2025;
Kang et al., 2025); it risks discarding distant but
causally essential history, severing the link between           • We propose STRACE, an end-to-end agent
a symptom and its origin.                                         optimization framework that treats execution
   This dilemma exposes a fundamental reality                     logs as structured causal evidence rather than
of agentic workflows: the node where an error                     monolithic linear text.
manifests (the downstream symptom) is often not
the node where it originates (the upstream root
                                                                • We introduce a trace filtering and causal local-
cause) (Zhang et al., 2025). For instance, a Code
                                                                  ization mechanism that selects representative
Interpreter crash at Step 50 may be the delayed con-
                                                                  failures, extracts compact causal slices, and
sequence of an incorrect parameter generated by a
                                                                  identifies root-cause modules as optimization
Planner at Step 5. Without a mechanism to bridge
                                                                  targets.
this temporal gap while filtering noise, optimizers
tend to repair symptoms rather than root causes.
   To address these challenges, we introduce                    • We evaluate STRACE on comprehensive
STRACE (Structural Trajectory Analysis and                        benchmarks covering diverse reasoning and
Causal Extraction), an optimization framework that                long-horizon agent settings, showing consis-
treats execution logs not as monolithic linear text,              tent gains over full-trajectory, truncation, and
but as causal graphs (Figure 1(c)). STRACE sys-                   prompt-optimization baselines.

                                                         2
2     Related Work                                          by mitigating reward sparsity via temporal redis-
                                                            tribution mechanisms (Harutyunyan et al., 2019;
2.1    Automated Prompt Optimization
                                                            Arjona-Medina et al., 2019). In modular agent
Automated Prompt Optimization (APO) employs                 systems, the focus shifts to Structural Credit As-
LLMs to iteratively search for superior instruc-            signment (SCA), where recent frameworks utilize
tions. Pioneering works formulate this as a nat-            min-form bottleneck penalties (Cheng et al., 2025)
ural language search problem based on perfor-               or generative critiques (Xie et al., 2025) to refine
mance scores (Zhou et al., 2023; Yang et al.,               reasoning chains. Despite these advancements, es-
2024). To handle complex workflows, recent                  tablishing explicit, causal-based attribution in long-
frameworks leverage reflexive feedback (Shinn               horizon trajectories remains an open challenge.
et al., 2023) or modular textual gradients (Pryzant
et al., 2023; Khattab et al., 2024) to optimize             3     The STRACE Framework
multi-stage pipelines. Furthermore, evolutionary
                                                            3.1   System Overview
strategies have been adopted to enhance explo-
ration through population-based mutation and en-            STRACE is an advanced optimization framework
vironmental feedback, such as EvoPrompt (Guo                designed to maximize the context signal-to-noise
et al., 2025), GEPA (Agrawal et al., 2025), and             ratio (SNR) in the optimization of long-horizon
SCOPE (Pei et al., 2025). However, a critical lim-          agents. Directly placing massive traces into the
itation remains in context management. Existing             agent optimizer’s context window introduces sub-
methods typically rely on scalar rewards or trun-           stantial noise, diluting the LLM’s reasoning sig-
cated summaries to fit context windows. In long-            nal and often trapping optimization in local op-
horizon agentic tasks, this compression obscures            tima. STRACE resolves this context-noise trade-
deep structural dependencies, hindering the diag-           off through a two-pronged approach: first, it per-
nosis of complex, multi-step failures.                      forms trace filtering to retain only highly diverse,
                                                            representative traces; second, it executes rigor-
2.2    Reflexive Agents and Harness Evolution               ous causal localization to explicitly strip away
Distinct from APO, reflexive and self-evolving              non-causal noise. By condensing large execu-
agents improve agent behavior through feedback-             tion batches into high-quality diagnostic evidence,
driven revision, ranging from inference-time re-            STRACE enables precise and stable optimization
finement (Madaan et al., 2023; Sun et al., 2023)            within finite context limits.
and verifier-based reinforcement (Jiang et al., 2025;          As illustrated in Figure 2, the STRACE pro-
Zhou et al., 2025) to code- and architecture-level          cess operates through four integrated phases. First,
evolution (Novikov et al., 2025; Sharma, 2025;              Structural Modeling constructs a textual Execution
Hu et al., 2025; Zhai et al., 2025). Recent                 Dependency Graph (EDG) to serve as the topologi-
harness-level systems, such as Hermes Agent Self-           cal foundation for subsequent trace filtering. Sec-
Evolution (Nous Research, 2026), further use op-            ond, Failure Pattern Mining and Trace Filtering
timizers like GEPA to evolve editable agent com-            compresses massive, heterogeneous trace batches
ponents. However, these methods still largely rely          into a compact, diverse set of representative ex-
on unstructured feedback or trajectory-level reflec-        emplars. Third, Causal Localization distills the
tion to decide what to modify. Without structured           minimal causal context via backward slicing and
failure localization, they may repair downstream            isolates the true root cause node. Finally, Induc-
symptoms or update the wrong component. In                  tive Policy Optimization converts this localized ev-
contrast, STRACE performs dependency-guided                 idence into generalized, persistent prompt updates
diagnosis before optimization, producing localized          for the defective modules.
repair signals that can transfer to skills and other
tunable harness components.                                 3.2   Phase 1: Structural Modeling
                                                            To enable structural analysis, STRACE leverages
2.3    Agent Diagnostics and Credit Assignment              an LLM to read the agent’s source implementation
The Credit Assignment Problem (CAP) fundamen-               and construct a textual Execution Dependency
tally challenges the attribution of outcomes to spe-        Graph (EDG) G = (V, E), which serves as the
cific decisions (Pignatelli et al., 2024). In Rein-         structural prior for the subsequent phases. Specifi-
forcement Learning, this is traditionally addressed         cally, STRACE parses the agent’s codebase to iden-

                                                        3
Figure 2: Illustration of the STRACE framework. The system optimizes long-horizon agents via four phases: (1)
Structural Modeling, which constructs execution topology; (2) Failure Pattern Mining and Trace Filtering, which
compresses failures into representative traces; (3) Causal Localization, which performs causal context distillation
and root cause isolation; and (4) Inductive Policy Optimization, which injects heuristics into identified root cause
modules.

tify the atomic functional modules (the vertex set           execution signals. To seamlessly adapt to vary-
V). Simultaneously, it infers the textual edges E by         ing agent logging formats, the system dynami-
analyzing the artifacts these modules produce, con-          cally infers a trace schema from a single pilot
sume, or utilize to dictate downstream execution             trace, identifies structural delimiters (e.g., “Ac-
paths.                                                       tion:”, “Observation:”), and compiles a tailored
   This construction yields a faithful, lightweight          parsing script on-the-fly. This parser then traverses
dependency map that captures two dependency                  the full trace set to record both the Global Out-
types among modules: data dependencies, where                come (y ∈ {Success, F ailure}) and the Local
module B consumes artifacts produced by mod-                 Node Status (e.g., whether a specific module threw
ule A (e.g., intermediate plans, retrieved evidence,         a runtime exception).
or execution outputs), and control dependencies,                Upon processing the entire trace corpus, the
where module A governs the downstream execu-                 system evaluates the aggregated dataset across
tion path by deciding whether module B is invoked            two analytical dimensions: (1) Statistical Severity,
or which tool/sub-agent is selected. We provide              which computes the conditional probability of a
the graph extraction procedure and detailed assess-          global task failure given a specific local node error,
ments in Appendix B.2 and Tables 3–4, showing                thereby identifying the most lethal bottlenecks; and
that the extracted graph is effective and remains use-       (2) Structural Path Patterns, which tracks module
ful for STRACE across different optimizer models.            invocation sequences to capture recurring patholog-
                                                             ical topologies. Specifically, this structural track-
3.3   Phase 2: Failure Pattern Mining and                    ing detects anomalous behaviors such as infinite
      Trace Filtering                                        self-loops (e.g., a module repeatedly invoking the
Long-horizon agents often generate massive, het-             same tool without state progression) and dead-end
erogeneous failure traces during rollouts, making            trajectories (e.g., specific calling sequences that
direct optimization inefficient and unstable. In this        consistently lead to an abrupt timeout). The output
phase, STRACE compresses the raw trace set into              is a comprehensive diagnostic summary mapping
a manageable size while rigorously preserving the            these dominant failure patterns across the entire
diversity of failure modes. The pipeline operates            dataset, serving as the quantitative basis for trace
in two steps: global diagnosis summarization fol-            selection (see Appendix B.3 for an example).
lowed by representative trace selection.                     Representative Trace Selection. Because agent
Diagnosis Summarization. Instead of feeding                  failures are heavily repetitive, STRACE applies
raw traces directly to the LLM, STRACE gener-                diversity-based sampling to reduce trace volume.
ates a deterministic Python parser to extract key            Based on the diagnostic summary, the framework

                                                         4
clusters the trace data using both the statistical           ple independent exploration branches. Because di-
severity of the errors and their structural path pat-        vergent reasoning paths are data-independent, an er-
terns. It then selects a minimal exemplar set from           ror manifesting on one specific branch possesses no
each distinct cluster with a predefined size. This           causal link to the others. The backtracking mecha-
guarantees that the optimizer reviews a compact              nism bypasses nodes from those parallel, irrelevant
dataset covering all major failure modes with a              explorations. The resulting high-SNR slice Cslice
controllable size, without being overwhelmed by              removes non-causal noise, capturing only the tra-
redundancy.                                                  jectory of the corrupted information flow.
Fallback Mechanism: In scenarios where the                   Step 2: Root Cause Isolation from the Causal
agent’s trace lacks explicit node-level error signals        Slice. Armed with the noise-free Cslice , STRACE
(i.e., modules fail silently without raising excep-          performs causal deduction to pinpoint where the ex-
tions), STRACE seamlessly adapts. It bypasses                ecution first deviated from the intended logic. The
the local node status and clusters the traces rely-          system traces the flow of corrupted context back-
ing on the global task outcome combined with the             ward from the manifestation node. For instance,
structural path patterns of the module invocations.          while a Code Interpreter (vm ) might manifest the
This ensures the selected exemplar set continues to          error by crashing, semantic reasoning over Cslice
rigorously capture distinct behavioral deviations.           systematically reveals that an upstream Planner
                                                             generated a hallucinated parameter several steps
3.4   Phase 3: Causal Localization                           earlier. Upon locating this originating logical de-
While the filtering phase successfully isolates a            fect, the system formally designates the module as
compact trace set, massive amounts of irrelevant             the true Root Cause Node vr .
information within these individual trajectories still
make it difficult to locate the true root cause node.        3.5    Phase 4: Inductive Policy Optimization
STRACE performs efficient causal localization to             By grouping the highly purified causal slices by
systematically pinpoint the core defect as an op-            their verified root cause nodes (vr ), the final phase
timization target. To achieve this precision, the            transforms episodic errors into persistent policy
framework shifts the analytical focus: instead of            upgrades, executing the actual optimization of the
just locating where an error visibly manifests, it           agent.
extracts what exact context is causally responsi-               For each targeted module vr , STRACE analyzes
ble for it. This naturally leads us to distinguish           the aggregated causal slices to synthesize high-
between the Manifestation Node vm (where the                 order generalized rules. Rather than translating re-
error explicitly surfaces, such as a code interpreter        curring errors into instance-specific failure records
throwing a syntax exception; or the terminal node if         (which risk overfitting), the optimizer performs in-
no explicit error exists) and the Root Cause Node            ductive abstraction to formulate robust, reusable
vr (the module harboring the actual logical defect).         heuristics for future executions. STRACE then
This phase bridges the gap between the two via a             injects these newly discovered rules directly into
two-step process.                                            the textual prompt policy of vr . This guarantees
Step 1: Causal Context Distillation via Back-                that the targeted policy update resolves the exact
ward Slicing. Given a representative trace and its           structural deficiency at its source. The instruction
manifestation node, STRACE extracts a minimal                templates are provided in Appendix B.4, and ex-
Causal Slice containing only the historical steps            amples of synthesized heuristics are provided in
that directly or indirectly influenced the failure.          Appendix D.
STRACE utilizes the EDG to traverse the trace in
reverse. Starting from the failure state at vm , the         4     Experiments
algorithm recursively traces the Data Dependency
and Control Dependency edges backward. By re-                4.1    Experimental Setup
taining only steps that can reach the manifestation          Datasets. We evaluate STRACE on three dis-
node through the dependency closure (→∗ ), the               tinct benchmarks. For general multi-hop reason-
system prunes nodes with no structural influence             ing, we employ HotpotQA (Yang et al., 2018)
on the failure, thereby discarding mere temporal             in the multi-document setting, using a random
antecedents.                                                 150/300 train-test split. For long-horizon agent
   To illustrate, consider an agent executing multi-         optimization, we consider two complementary

                                                         5
Table 1: Performance of STRACE versus baselines on HotpotQA, WebArena, and VeruSAGE-Bench. HotpotQA
is evaluated by Exact Match (EM), while WebArena and VeruSAGE-Bench are evaluated by Success Rate (SR).
Parentheses in ALL indicate absolute gains over the Base Agent. Best results are highlighted in bold. TextGrad is
omitted for VeruSAGE-Bench due to context-budget limits.

Prompt Setting                HotpotQA                                   WebArena (SR)
                                (EM)         Shopping          CMS       Reddit     GitLab             ALL
Base Agent                      37.0%         17.9%            10.8%       4.5%         7.3%            10.8%
Naive Few-shot                  60.0%         23.1%            13.5%       9.1%         7.3%        13.7% (+2.9%)
Failure-Aware RAG               57.7%         23.1%            16.2%       9.1%         7.3%        14.4% (+3.6%)
Summary-based Selection         64.3%         25.6%            10.8%       9.1%        12.2%        15.1% (+4.3%)
Retrieval-based Selection       46.0%         17.9%            13.5%      14.3%        12.2%        14.4% (+3.6%)
TextGrad                        62.0%         30.8%            16.2%       9.1%         9.8%        17.3% (+6.5%)
GEPA                            64.4%         23.1%            10.8%      27.3%         9.8%        16.5% (+5.7%)
STRACE (Ours)                   68.5%         30.8%            16.2%      36.4%        17.1%       23.7% (+12.9%)

Prompt Setting                                             VeruSAGE-Bench (SR)
                            IronKV   Memory Allocator     Node Replication NRKernel      Storage       ALL
Base Agent                  41.6%         66.7%                 80.0%          20.0%     46.2%          42.5%
Naive Few-shot              37.5%         61.1%                 80.0%          24.4%     30.8%      39.6% (-2.9%)
Failure-Aware RAG           37.5%         66.7%                 70.0%          29.3%     38.5%      42.5% (+0.0%)
Summary-based Selection     58.3%         61.1%                 70.0%          29.3%     30.8%      45.3% (+2.8%)
Retrieval-based Selection   37.5%         66.7%                 90.0%          22.0%     38.5%      41.5% (-1.0%)
GEPA                        54.2%         61.1%                 80.0%          29.3%     46.2%      47.2% (+4.7%)
STRACE (Ours)               62.5%         88.9%                100.0%          31.7%     61.5%     58.5% (+16.0%)


benchmarks. WebArena (Zhou et al., 2024) rep-                 Baselines. We compare STRACE against the un-
resents general-purpose web interaction, where                optimized Base Agent, and three categories of op-
agents complete realistic tasks across Shopping,              timization baselines. For static strategies, we uti-
CMS, Reddit, and GitLab tasks. VeruSAGE-                      lize Naive Few-shot (Brown et al., 2020), and a
Bench (Yang et al., 2025) represents domain-                  Failure-Aware RAG baseline (Lewis et al., 2021)
intensive formal verification, consisting of five real-       that retrieves traces via a BM25 index (Robert-
world Rust projects (Lattuada et al., 2024) with              son et al., 2009) and appends them as instruction
extreme context lengths (avg. 947 lines): IronKV,             references. For automated optimizers, we select
Memory Allocator, Node Replication, NRKernel,                 two representative methods. TextGrad (Yuksek-
and Storage. We enforce an 80%/20% split per                  gonul et al., 2024) represents the gradient-based
project to test generalization.                               paradigm, which feeds the full execution trace to
                                                              the optimizer to compute error attributions, and
Base Agent Implementation. The optimiza-                      GEPA (Agrawal et al., 2025) represents the evolu-
tion targets the set of instructions P that gov-              tionary paradigm, which typically applies context
erns the modules in each workflow. For Hot-                   truncation to fit recent history into the optimizer
potQA, we use a DSPy-based (Khattab et al.,                   window. For context management baselines, we in-
2024; Agrawal et al., 2025) four-stage multi-hop              clude two common trace compression strategies for
reasoning workflow with 4 optimizable modules                 handling extremely long traces during optimization:
and GPT-4o (OpenAI, 2024a). For WebArena,                     Summary-based and Retrieval-based optimization.
we use the original Chain-of-Thought (CoT) web-               Both use the same optimizer as STRACE but con-
navigation agent with one tunable instruction and             struct the optimization context without causal lo-
GPT-4o as the backbone. For VeruSAGE-Bench,                   calization: the former summarizes the full trace
we use the hierarchical router-executor multi-agent           before inductive abstraction, while the latter re-
framework (Yang et al., 2025) with 16 optimiz-                trieves the most relevant steps as optimizer input.
able modules and o4-mini (OpenAI, 2025b) as the               Note: TextGrad is excluded from VeruSAGE-Bench
backbone. Each task is solved through an itera-               due to prohibitive context costs (>100k tokens).
tive verification-repair loop that runs for up to 20
repair attempts or 20 minutes. Detailed architec-             Metrics & Configuration. We report Exact Match
tures and optimizable components are provided in              (EM) for HotpotQA and Success Rate (SR) for
Appendix A.                                                   WebArena and VeruSAGE-Bench. Optimization

                                                          6
cost is reported in USD for one full optimization
run, estimated from token usage under API pricing.
For the optimizer, we employ Claude Sonnet 4.5
(temp=1.0) as the meta-controller for all methods to
ensure fairness, with a bottleneck threshold k = 5
and exemplar count s = 5.

4.2   Main Results
Table 1 summarizes the performance of STRACE
across benchmarks that cover both general rea-
soning and complex long-horizon agentic tasks.
Across these settings, STRACE achieves the
strongest overall performance compared to all base-
                                                             Figure 3: Success rate on 50 independent tasks and
lines. The pattern across baseline categories helps
                                                             optimization cost for STRACE, GEPA, and TextGrad
explain where the gains of STRACE come from.                 full-trace prompt optimization, as the number of training
Static strategies can provide additional examples or         cases scales from 1 to 453.
failure cases, but they fail to identify which part of
the current behavior should be revised. Automated
optimizers such as TextGrad and GEPA still rely              strate the effectiveness of STRACE especially in
on provided context quality: using full trajectories         complex agentic settings, where failures may prop-
can exceed the context budget or dilute local sig-           agate across multiple components and require root-
nals, whereas simple truncation or relevance-based           cause localization rather than shallow reuse of prior
slicing may miss the upstream root cause. Context            traces.
management methods attempt to reduce the trace
context, but summaries may discard fine-grained              4.3   Optimization Scalability and Cost
failure signals, while retrieval can be misled by se-              Analysis
mantic similarity. In contrast, STRACE addresses
this context-noise trade-off through a dependency-           Long-horizon prompt optimization must balance
guided optimization framework that provides local-           performance with cost, as naively increasing con-
ized yet context-aware signals, enabling the opti-           text quickly becomes prohibitive. Figure 3 plots
mizer to focus on root causes rather than noisy              the success rate and optimization cost against the
downstream symptoms and thereby achieve the                  number of training trajectories. For a fair com-
strongest overall performance across benchmarks.             parison, all methods are optimized on the same
   Beyond the overall comparison, STRACE also                trajectory subset at each scale point. We include
shows strong adaptability to two optimization                two representative baselines: TextGrad (full-trace
needs in agentic tasks. On WebArena, the key                 optimization) and GEPA (current node slicing and
difference lies in the task-specific demand for op-          batch optimization).
timization signals: Shopping and CMS require                    As the training set scales, STRACE achieves
more workflow guidance, while Reddit and Git-                the most favorable cost–performance trend. While
Lab require more failure-aware rules. In the for-            TextGrad incurs rapidly increasing costs due to full-
mer domains, STRACE remains competitive with                 trace processing and GEPA reduces cost by restrict-
the strongest baselines by preserving useful pro-            ing optimization to local-node batches, STRACE
cedural context. In the latter domains, STRACE               maintains both efficiency and effectiveness. This fa-
achieves clearer improvements, suggesting that               vorable trade-off is enabled by the Statistical Bottle-
STRACE leverages both workflow-level patterns                neck Diagnosis module, which summarizes dataset-
and failure-aware optimization signals. The ad-              level failure patterns and selects only a small set
vantage of STRACE becomes more pronounced                    of representative, high-value exemplars for opti-
on the longer-horizon and more domain-intensive              mization. As a result, even when scaling to the
VeruSAGE-Bench, where STRACE achieves the                    full set of 453 trajectories, STRACE controls con-
highest average success rate of 58.5%, outperform-           text growth while preserving the failure evidence
ing the base agent by +16.0% and the strongest               needed for effective repair, yielding the strongest
baseline, GEPA, by +11.3%. These results demon-              overall cost–performance trend among all methods.

                                                         7
                                                             Table 2: Ablation results with Success Rate and stage-
                                                             wise cost breakdown.

                                                             Ablation Method                  SR     Overall Cost ($)
                                                             STRACE                            56%        2.96
                                                             w/o Structural Modeling           48%        5.10
                                                             w/o Trace Filtering               46%        8.45
                                                             w/o Causal Localization (Current) 54%        2.88
                                                             w/o Causal Localization (Full)    54%        5.93


                                                             an earlier routing error: the upstream controller
                                                             dispatched the task to an unsuitable repair path. By
                                                             repairing this root-cause decision, STRACE breaks
Figure 4: Distinguishing Symptoms from Root                  the loop and enables successful verification.
Causes. Top: Causal localization remaps 25 traces
from 5 manifest nodes to 6 targets, exposing an up-          4.5    Ablation Study
stream source. Bottom: A compute_repair loop is              We ablate STRACE to isolate the contributions of
traced to assertion_reasoning_pipeline, enabling
                                                             structure modeling, trace filtering, and causal lo-
a targeted policy optimization to bypass the recursive
path.                                                        calization. Each variant is optimized under the
                                                             same protocol with the same training traces. Ta-
                                                             ble 2 reports the resulting Success Rate and overall
4.4   Case Study: Tracing Symptoms to Root                   cost. Removing structure modeling leads to lower
      Causes                                                 effectiveness and higher cost, suggesting that the
To empirically validate the distinction between              dependency graph provides a useful prior for or-
symptom (vm ) and cause (vr ), we present two anal-          ganizing trace failures and narrowing the search
yses from the VeruSAGE-Bench optimization pro-               space before optimization. Removing trace filter-
cess in Figure 4. These cases illustrate how root            ing further degrades both performance and effi-
cause isolation redirects optimization from surface-         ciency, as the optimizer must process more redun-
level failures to upstream logical defects.                  dant or low-value traces rather than a compact set
                                                             of representative failures. The causal localization
Re-mapping Target Nodes. As formalized in Sec-
                                                             variants reveal the context-noise dilemma: using
tion 3.4, effective optimization requires targeting
                                                             only the current node may miss upstream causes,
the root-cause node rather than the manifestation
                                                             while using the full trace introduces unnecessary
node. In the 200-case setting, STRACE selects
                                                             noise and cost. In contrast, STRACE combines
5 high-impact manifest modules and 5 represen-
                                                             these components to preserve root-cause evidence
tative traces for each, yielding 25 traces in total.
                                                             while keeping the optimization context bounded.
Without causal localization, these traces would be
                                                             Detailed cost-component analyses are deferred to
attributed to the modules where failures surface
                                                             Appendix C.1.
naturally. However, by applying root cause isola-
tion, 12 of the 25 traces are re-mapped to upstream
                                                             5     Conclusions
root-cause actions, expanding the optimization tar-
gets to 6 distinct nodes, with an additional up-             We introduce a novel method STRACE for long-
stream “assertion_reasoning_pipeline” mod-                   horizon agent optimization under the context-noise
ule. This redistribution confirms that relying solely        trade-off. By combining failure pattern mining
on crash location (vm ) can lead to “optimizing              with causal localization, STRACE breaks this
the wrong target” for a subset of failures, whereas          dilemma, enabling targeted policy optimization
STRACE disperses the diagnosis to the true logical           that is both cost-efficient and high-performing. Re-
origins.                                                     sults on HotpotQA, WebArena, and VeruSAGE-
Breaking the Loop. We further examine a rep-                 Bench show consistent gains in success rate and
resentative IronKV failure. The agent repeatedly             efficiency, outperforming all baselines and demon-
invokes a downstream repair module until timeout,            strating the effectiveness of our method. Ablation
making the visible failure appear local to that mod-         studies and analysis further validate the contribu-
ule. Causal slicing instead traces the loop back to          tion of each phase. Importantly, STRACE can be

                                                         8
readily transferred to harness engineering, where               haria, and Omar Khattab. 2025. GEPA: Reflec-
its localized diagnoses can guide updates to tunable            tive prompt evolution can outperform reinforcement
                                                                learning. Preprint, arXiv:2507.19457.
agent components such as skills, tool-use policies,
and other editable harness elements. This transfer-           Anthropic. 2024a. Developing a computer use model.
ability makes STRACE a flexible framework for                   Anthropic Research Blog.
improving complex long-horizon agents.
                                                              Anthropic. 2024b. Introducing computer use, a new
                                                                Claude 3.5 Sonnet, and Claude 3.5 Haiku. Anthropic
Limitations                                                     Research Blog.
A main limitation of STRACE is that it assumes suf-           Anthropic. 2025a.        Claude Agent SDK.
ficient visibility into the target agent system. The            https://github.com/anthropics/
dependency prior is constructed from codebase-                  claude-agent-sdk-python.    Python SDK for
level or harness-level artifacts, including agent defi-         building agents with Claude Code capabilities.
                                                                Accessed: 2026-05-22.
nitions, tool interfaces, configuration files, prompts,
skills, and execution logs. Therefore, STRACE is              Anthropic. 2025b. Introducing Claude Haiku 4.5. Ac-
most directly applicable to systems where the op-               cessed: 2026-07-07.
timizer can inspect the implementation or harness,
                                                              Anthropic. 2025c. Introducing Claude Sonnet 4.5. Ac-
rather than fully black-box agents with hidden com-             cessed: 2026-07-07.
ponents and control flow. Notably, this does not
require access to model weights, but it does re-              Jose A. Arjona-Medina, Michael Gillhofer, Michael
quire enough system-level visibility to identify the            Widrich, Thomas Unterthiner, Johannes Brandstetter,
                                                                and Sepp Hochreiter. 2019. RUDDER: return decom-
components involved in long-horizon failures. Ex-               position for delayed rewards. Curran Associates Inc.,
tending STRACE to purely trace-only or black-box                Red Hook, NY, USA.
settings remains future work.
                                                              Shraddha Barke, Arnav Goyal, Alind Khare, Avaljot
Ethical considerations                                          Singh, Suman Nath, and Chetan Bansal. 2026. Agen-
                                                                tRx: Diagnosing AI agent failures from execution
In this study, all datasets, models, and software               trajectories. arXiv preprint arXiv:2602.02475.
artifacts used in our experiments are publicly avail-         Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie
able, and we follow their respective licenses or                Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind
terms of use. The use of these resources is strictly            Neelakantan, Pranav Shyam, Girish Sastry, Amanda
confined to academic research and benchmarking                  Askell, Sandhini Agarwal, Ariel Herbert-Voss,
                                                                Gretchen Krueger, Tom Henighan, Rewon Child,
purposes. We do not collect new human-subject                   Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu,
data, and all reported results are presented in ag-             Clemens Winter, and 12 others. 2020.        Lan-
gregate form. While STRACE is designed to im-                   guage models are few-shot learners. Preprint,
prove the efficiency and reliability of long-horizon            arXiv:2005.14165.
agent optimization, we acknowledge that stronger              Mert Cemri, Melissa Z Pan, Shuyi Yang, Lakshya A
agent optimization methods could be misused if                 Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt
applied to unsafe or malicious agent systems. In               Keutzer, Aditya Parameswaran, Dan Klein, Kannan
addition, execution traces collected from real de-             Ramchandran, and 1 others. 2026. Why do multi-
                                                               agent LLM systems fail? Advances in Neural Infor-
ployments may contain sensitive information. For               mation Processing Systems, 38.
practical deployment, we recommend that traces
be anonymized or access-controlled, and that opti-            Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,
mized prompts, skills, or harness components be                Henrique Ponde de Oliveira Pinto, Jared Kaplan,
                                                               Harri Edwards, Yuri Burda, Nicholas Joseph, Greg
reviewed before being applied to high-stakes or                Brockman, Alex Ray, Raul Puri, Gretchen Krueger,
user-facing systems.                                           Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela
                                                               Mishkin, Brooke Chan, Scott Gray, and 39 others.
                                                               2021. Evaluating large language models trained on
References                                                     code. Preprint, arXiv:2107.03374.

Lakshya A Agrawal, Shangyin Tan, Dilara Soylu,                Jie Cheng, Gang Xiong, Ruixi Qiao, Lijun Li, Chao
  Noah Ziems, Rishi Khare, Krista Opsahl-Ong, Ar-                Guo, Junle Wang, Yisheng Lv, and Fei-Yue Wang.
  nav Singhvi, Herumb Shandilya, Michael J Ryan,                 2025. Stop summation: Min-form credit assign-
  Meng Jiang, Christopher Potts, Koushik Sen, Alexan-            ment is all process reward model needs for reasoning.
  dros G. Dimakis, Ion Stoica, Dan Klein, Matei Za-              Preprint, arXiv:2504.15275.


                                                          9
DeepSeek-AI. 2025. DeepSeek-V3.1 release. https:                  Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler
  //api-docs.deepseek.com/news/news250821.                         Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,
  Accessed: 2026-05-20.                                            Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,
                                                                   Shashank Gupta, Bodhisattwa Prasad Majumder,
Qingyan Guo, Rui Wang, Junliang Guo, Bei Li, Kaitao                Katherine Hermann, Sean Welleck, Amir Yazdan-
  Song, Xu Tan, Guoqing Liu, Jiang Bian, and Yu-                   bakhsh, and Peter Clark. 2023. Self-refine: It-
  jiu Yang. 2025. EvoPrompt: Connecting llms with                  erative refinement with self-feedback. Preprint,
  evolutionary algorithms yields powerful prompt opti-             arXiv:2303.17651.
  mizers. Preprint, arXiv:2309.08532.
                                                                  MiniMax. 2026. MiniMax M2.5: Built for real-world
Anna Harutyunyan, Will Dabney, Thomas Mesnard,                      productivity. https://www.minimax.io/models/
  Mohammad Azar, Bilal Piot, Nicolas Heess, Hado                    text. Accessed: 2026-05-20.
  van Hasselt, Greg Wayne, Satinder Singh, Doina Pre-
  cup, and Remi Munos. 2019. Hindsight credit assign-             Nous Research. 2026. Hermes Agent: The agent
  ment. Preprint, arXiv:1912.02503.                                 that grows with you.   https://github.com/
                                                                    NousResearch/hermes-agent. Accessed: 2026-
Shengran Hu, Cong Lu, and Jeff Clune. 2025. Au-                     05-25.
  tomated design of agentic systems.    Preprint,
  arXiv:2408.08435.                                               Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Em-
                                                                    ilien Dupont, Po-Sen Huang, Adam Zsolt Wagner,
Yuhua Jiang, Yuwen Xiong, Yufeng Yuan, Chao Xin,                    Sergey Shirobokov, Borislav Kozlovskii, Francisco
  Wenyuan Xu, Yu Yue, Qianchuan Zhao, and Lin                       J. R. Ruiz, Abbas Mehrabian, M. Pawan Kumar, Abi-
  Yan. 2025. PAG: Multi-turn reinforced LLM self-                   gail See, Swarat Chaudhuri, George Holland, Alex
  correction with policy as generative verifier. Preprint,          Davies, Sebastian Nowozin, Pushmeet Kohli, and
  arXiv:2506.10406.                                                 Matej Balog. 2025. AlphaEvolve: A coding agent
                                                                    for scientific and algorithmic discovery. Preprint,
Carlos E Jimenez, John Yang, Alexander Wettig,
                                                                    arXiv:2506.13131.
  Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R
  Narasimhan. 2024. SWE-bench: Can language mod-                  OpenAI. 2024a. GPT-4o system card.          Preprint,
  els resolve real-world github issues? In The Twelfth              arXiv:2410.21276.
  International Conference on Learning Representa-
  tions.                                                          OpenAI. 2024b. OpenAI o1 system card.
Minki Kang, Wei-Ning Chen, Dongge Han, Huseyin A.                 OpenAI. 2025a. GPT-5 system card. https://openai.
  Inan, Lukas Wutschitz, Yanzhi Chen, Robert Sim,                   com/index/gpt-5-system-card/. Model release:
  and Saravan Rajmohan. 2025. ACON: Optimizing                      August 7, 2025.
  context compression for long-horizon LLM agents.
  Preprint, arXiv:2510.00615.                                     OpenAI. 2025b. OpenAI o3 and o4-mini system card.
                                                                    Accessed: 2026-07-07.
Omar Khattab, Arnav Singhvi, Paridhi Maheshwari,
 Zhiyuan Zhang, Keshav Santhanam, Sri Vard-                       Zehua Pei, Hui-Ling Zhen, Shixiong Kai, Sinno Jialin
 hamanan, Saiful Haq, Ashutosh Sharma, Thomas T.                    Pan, Yunhe Wang, Mingxuan Yuan, and Bei Yu. 2025.
 Joshi, Hanna Moazam, Heather Miller, Matei Zaharia,                Scope: Prompt evolution for enhancing agent effec-
 and Christopher Potts. 2024. DSPy: Compiling                       tiveness. Preprint, arXiv:2512.15374.
 declarative language model calls into self-improving
 pipelines.                                                       Eduardo Pignatelli, Johan Ferret, Matthieu Geist,
                                                                    Thomas Mesnard, Hado van Hasselt, Olivier Pietquin,
Andrea Lattuada, Travis Hance, Jay Bosamiya, Matthias               and Laura Toni. 2024. A survey of temporal credit
  Brun, Chanhee Cho, Hayley LeBlanc, Pranav Srini-                  assignment in deep reinforcement learning. Preprint,
  vasan, Reto Achermann, Tej Chajed, Chris Haw-                     arXiv:2312.01072.
  blitzel, and 1 others. 2024. Verus: A practical foun-
  dation for systems verification. In Proceedings of the          Reid Pryzant, Dan Iter, Jerry Li, Yin Tat Lee, Chen-
  ACM SIGOPS 30th Symposium on Operating Systems                    guang Zhu, and Michael Zeng. 2023. Automatic
  Principles, pages 438–454.                                        prompt optimization with "gradient descent" and
                                                                    beam search. Preprint, arXiv:2305.03495.
Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio
  Petroni, Vladimir Karpukhin, Naman Goyal, Hein-                 Stephen Robertson, Hugo Zaragoza, and 1 others. 2009.
  rich Küttler, Mike Lewis, Wen tau Yih, Tim Rock-                   The probabilistic relevance framework: BM25 and
  täschel, Sebastian Riedel, and Douwe Kiela. 2021.                  beyond. Foundations and trends® in information
  Retrieval-augmented generation for knowledge-                      retrieval, 3(4):333–389.
  intensive NLP tasks. Preprint, arXiv:2005.11401.
                                                                  Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta
Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paran-                Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola
  jape, Michele Bevilacqua, Fabio Petroni, and Percy                Cancedda, and Thomas Scialom. 2023. Toolformer:
  Liang. 2023. Lost in the middle: How language mod-                Language models can teach themselves to use tools.
  els use long contexts. Preprint, arXiv:2307.03172.                Preprint, arXiv:2302.04761.


                                                             10
Asankhaya Sharma. 2025.      OpenEvolve: Open-                Matei Zaharia, Omar Khattab, Lingjiao Chen,
  source implementation of AlphaEvolve. https://               Jared Quincy Davis, Heather Miller, Chris Potts,
  github.com/algorithmicsuperintelligence/                     James Zou, Michael Carbin, Jonathan Fran-
  openevolve. GitHub repository.                               kle, Naveen Rao, and Ali Ghodsi. 2024. The
                                                               shift from models to compound ai systems.
Freda Shi, Xinyun Chen, Kanishka Misra, Nathan                 https://bair.berkeley.edu/blog/2024/02/
  Scales, David Dohan, Ed Chi, Nathanael Schärli, and          18/compound-ai-systems/.
  Denny Zhou. 2023. Large language models can be
  easily distracted by irrelevant context. In Proceed-        Yunpeng Zhai, Shuchang Tao, Cheng Chen, Anni
  ings of the 40th International Conference on Machine          Zou, Ziqian Chen, Qingxu Fu, Shinji Mai, Li Yu,
  Learning, ICML’23. JMLR.org.                                  Jiaji Deng, Zouying Cao, Zhaoyang Liu, Bolin
                                                                Ding, and Jingren Zhou. 2025. AgentEvolver: To-
Noah Shinn, Federico Cassano, Edward Berman, Ash-               wards efficient self-evolving agent system. Preprint,
  win Gopinath, Karthik Narasimhan, and Shunyu Yao.             arXiv:2511.10395.
  2023. Reflexion: Language agents with verbal rein-
  forcement learning. Preprint, arXiv:2303.11366.             Guibin Zhang, Junhao Wang, Junjie Chen, Wangchun-
                                                                shu Zhou, Kun Wang, and Shuicheng Yan. 2025.
Haotian Sun, Yuchen Zhuang, Lingkai Kong, Bo Dai,               AgenTracer: Who is inducing failure in the LLM
  and Chao Zhang. 2023. AdaPlanner: Adaptive plan-              agentic systems? arXiv preprint arXiv:2509.03312.
  ning from feedback with language models. Preprint,
  arXiv:2305.16653.                                           Shuyan Zhou, Frank F Xu, Hao Zhu, Xuhui Zhou,
                                                                Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue
Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao                Ou, Yonatan Bisk, Daniel Fried, and 1 others. 2024.
  Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang,               Webarena: A realistic web environment for build-
  Xu Chen, Yankai Lin, Wayne Xin Zhao, Zhewei Wei,              ing autonomous agents. In International Conference
  and Jirong Wen. 2024. A survey on large language              on Learning Representations, volume 2024, pages
  model based autonomous agents. Frontiers of Com-              15585–15606.
  puter Science, 18(6).
                                                              Yifei Zhou, Sergey Levine, Jason Weston, Xian Li, and
Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yiwen               Sainbayar Sukhbaatar. 2025. Self-challenging lan-
  Ding, Boyang Hong, Ming Zhang, Junzhe Wang, Sen-              guage model agents. Preprint, arXiv:2506.01716.
  jie Jin, Enyu Zhou, Rui Zheng, Xiaoran Fan, Xiao
  Wang, Limao Xiong, Yuhao Zhou, Weiran Wang,                 Yongchao Zhou, Andrei Ioan Muresanu, Ziwen Han,
  Changhao Jiang, Yicheng Zou, Xiangyang Liu, and               Keiran Paster, Silviu Pitis, Harris Chan, and Jimmy
  10 others. 2023. The rise and potential of large              Ba. 2023. Large language models are human-level
  language model based agents: A survey. Preprint,              prompt engineers. Preprint, arXiv:2211.01910.
  arXiv:2309.07864.

Guofu Xie, Yunsheng Shi, Hongtao Tian, Ting Yao,
  and Xiao Zhang. 2025. CAPO: Towards enhancing
  llm reasoning through generative credit assignment.
  Preprint, arXiv:2508.02298.

Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu,
  Quoc V. Le, Denny Zhou, and Xinyun Chen. 2024.
  Large language models as optimizers. Preprint,
  arXiv:2309.03409.

Chenyuan Yang, Natalie Neamtu, Chris Hawblitzel, Ja-
  cob R. Lorch, and Shan Lu. 2025. VeruSAGE: A
  study of agent-based verification for rust systems.
  Preprint, arXiv:2512.18436.

Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio,
  William Cohen, Ruslan Salakhutdinov, and Christo-
  pher D Manning. 2018. HotpotQA: A dataset for
  diverse, explainable multi-hop question answering.
  In Proceedings of the 2018 conference on empiri-
  cal methods in natural language processing, pages
  2369–2380.

Mert Yuksekgonul, Federico Bianchi, Joseph Boen,
 Sheng Liu, Zhi Huang, Carlos Guestrin, and James
 Zou. 2024. Textgrad: Automatic" differentiation" via
 text. arXiv preprint arXiv:2406.07496.


                                                         11
Appendix                                                            representation, exposing interactive elements
                                                                    such as buttons, links, text boxes, and menus.
A       Agent Implementation Details                             2. Reason and Act: Given the task objective and
Here we provide detailed specifications of the base                 the current observation, the Chain-of-Thought
agents used in our experiments, including their ar-                 prompt guides the language model to reason
chitectural workflows and the specific sub-agents                   about the page state and output one concrete
targeted for optimization.                                          action, such as clicking an element, typing
                                                                    into a field, scrolling, navigating to a URL, or
A.1       HotpotQA Agent Workflow                                   stopping with a final answer.
                                                                 3. Execute: The predicted action is executed in
Following the setup in GEPA (Agrawal et al.,
                                                                    the browser environment, producing a new
2025) 1 , our HotpotQA agent consists of four se-
                                                                    webpage state.
quential sub-agents designed to handle multi-hop
                                                                 4. Repeat: The agent repeats this observe–
reasoning. The workflow proceeds as follows:
                                                                    reason–act cycle until it issues a stop action
    1. Summarize1: This module processes the ini-                   or reaches the maximum interaction budget.
       tial question and the paragraphs retrieved in
                                                                 During optimization, STRACE targets the
       the first hop. Its goal is to extract relevant
                                                               prompt of this single WebArena agent. Since the
       information and form a preliminary context.
                                                               baseline does not contain explicit sub-agents, plan-
    2. Create Query Hop2: Based on the initial
                                                               ners, or external memory modules, the optimized
       summary and the original question, this mod-
                                                               component is the agent’s instruction prompt, which
       ule generates a refined search query to retrieve
                                                               defines its action space, reasoning style, and few-
       missing evidence required for the second hop.
                                                               shot behavior examples.
    3. Summarize2: This module integrates the
       newly retrieved passages from the second hop
                                                               A.3    VeruSAGE Agent Workflow
       with the prior context, synthesizing a compre-
       hensive summary that consolidates evidence              For VeruSAGE-Bench, we utilize the VeruSAGE
       from both retrieval rounds.                             framework (Yang et al., 2025) 3 , which employs a
    4. Final Answer: Finally, this module reasons              more complex, iterative multi-agent architecture to
       over the aggregated summaries to produce the            repair verification failures in Rust code.
       final answer string (and supporting facts) for             Iterative Repair Loop.
       the multi-hop question.                                    The agent solves each task through a verification-
  During optimization, STRACE optimizes the                    driven loop. In each iteration:
system prompts for all four modules simultane-                   1. The current code is submitted to the Verus
ously.                                                              verifier.
                                                                 2. If verification fails, the Error Analyzer parses
A.2       WebArena Agent Workflow                                   the error message.
For WebArena, we followed the original We-                       3. A Router (or High-level Planner) selects the
bArena Chain-of-Thought agent design (Zhou                          most appropriate repair action from a pool of
et al., 2024) 2 . WebArena agent is a single prompt-                35 available actions based on the error type
based web navigation agent rather than a multi-                     and code context.
agent system. At each step, the agent observes the               4. The selected Sub-agent (Executor) generates
current webpage through a textual accessibility tree,               a specific patch (e.g., adding a lemma func-
together with the current URL, the user instruction,                tion, enabling a specific prover mode, apply-
and the previous action. A language model then                      ing divide-and-conquer for a specific property
reasons over this information and predicts the next                 to be proved).
browser action.                                                  5. The patch is applied, and the loop repeats.
   The interaction loop proceeds as follows:                   The process terminates when the code verifies suc-
    1. Observe: The browser environment converts               cessfully or when the budget (20 attempts or 20
       the current webpage into an accessibility-tree          minutes) is exhausted.
    1                                                             3
        https://github.com/gepa-ai/gepa-artifact                   https://github.com/microsoft/
    2
        https://github.com/web-arena-x/webarena                verus-proof-synthesis


                                                          12
   Sub-agent Structure. The framework com-                   around the root-cause node. Separating Phase 4
prises 15 specialized sub-agents covering various            from the earlier shared context thus reduces unnec-
aspects of formal verification, including but not            essary context overhead and keeps the final revision
limited to:                                                  step focused and modular.
    • Invariant Manager: For analyzing and fixing
                                                             B.2 Textual Dependency Graph Construction
      loop invariants.
    • Proof Strategy Applicator: For conducting              In our experiments, STRACE instantiates Phase 1
      proof strategies like divide-and-conquer (i.e.,        with an optimizer agent built on the Claude Agent
      case analysis) and induction.                          SDK under a dedicated textual dependency-graph
    • Prover Mode Activator: For enabling special            construction instruction. The agent first inspects
      prover modes, like bit-vector mode, non-linear         the target repository for available background ar-
      arithmetic mode, etc.                                  tifacts, including README files, documentation,
    • Syntax Fixer: For correcting Rust-specific             configuration files, agent definitions, and relevant
      compilation errors.                                    source code. It then identifies the major modules
    • Standard Lemma Guider: For suggesting                  in the system, including active modules (e.g., de-
      what lemmas inside the Verus standard library          cision makers and executors), passive shared-state
      might be useful.                                       modules (e.g., memory or state managers), and the
   Optimization Scope. Due to the domain-                    key artifacts each module produces or consumes.
intensive nature of Verus, generic prompts often             Based on this repository-level inspection, Phase 1
fail to capture the nuances of formal reasoning.             infers two types of dependency priors: data de-
STRACE targets the system prompts of the Router              pendencies and control dependencies. We refer to
and the top-k most frequently triggered Executors,           this textual dependency graph as the dependency
injecting synthesized domain heuristics (e.g., spe-          prior and denote it by G. Notably, the term “graph”
cific strategies for handling "nonlinear arithmetic"         reflects its node–edge structure, but its implemen-
errors) directly into their context windows.                 tation is a text edge list rather than a learned graph
                                                             object or a static-program-analysis graph. Each
B     STRACE Implementation Details                          edge is a textually specified relation between two
                                                             components, together with its dependency type and
B.1    Architecture and Context Management                   brief evidence from repository artifacts. Later diag-
STRACE is implemented on top of the Claude-                  nosis and slicing phases consume this textual graph
Agent-SDK (Anthropic, 2025a) as a four-phase                 as structural guidance.
agent workflow. From an architectural perspective,              This construction is framework-agnostic: the
the system separates the optimization process into           analyzed agent system may be implemented in dif-
four sequential phases, while adopting different             ferent frameworks or coding styles, and STRACE
context management strategies for different stages.          does not require framework-specific APIs for tools
Phases 1–3 are executed within a shared context              or agents. Instead, it recovers dependency priors
window. This design is motivated by the strong con-          from repository-level artifacts such as code, config-
tinuity across these stages: all three phases rely on        uration, and agent definitions.
the same agent background, and they also need to                To further analyze the role of graph quality
share the textual dependency graph inferred during           in STRACE, we report two complementary stud-
structural analysis. As a result, there is a natural         ies: an expert-reviewed comparison of repository-
flow of information across the first three phases,           constructed graphs across models and a graph per-
where intermediate outputs produced in one phase             turbation experiment. These studies address two
directly serve as inputs to the next. In contrast,           questions: whether the dependency prior can be
the Phase 4 is executed in an isolated context win-          reliably constructed by different optimizer models,
dow supported by the reason that STRACE has                  and whether STRACE remains effective when this
already identified the true root-cause node and pro-         prior is noisy.
duced a concise explanation of why this node is                 RQ1: Can different optimizer models construct
the root cause within the slicing chain by the end           a reliable dependency prior from the repository?
of Phase 3. Therefore, Phase 4 no longer needs                  Table 3 answers RQ1 by comparing dependency
access to the full intermediate context from the ear-        graphs constructed from the same repository us-
lier stages. Instead, it only needs the local context        ing different models. The expert review shows

                                                        13
Table 3: Expert-reviewed quality assessment of dependency graphs constructed from the repository by different
models.

 Model (constructed from repository)    Graph Quality Assessment (expert-reviewed)
 Claude Sonnet 4.5 (Anthropic, 2025c)   Highest-quality graph, preserves the core dependency structure with appropriate gran-
                                        ularity.
 Claude Haiku 4.5 (Anthropic, 2025b)    Preserves the core dependency structure, with some additional infrastructure-level
                                        edges.
 GPT-5.1 Codex Mini (OpenAI, 2025a)     Preserves the core dependency structure at a finer granularity.
 DeepSeek-V3.1 (DeepSeek-AI, 2025)      Preserves the core dependency structure, with additional infrastructure-level details.
 MiniMax-M2.5 (MiniMax, 2026)           Preserves the core dependency structure, with about 10% additional noisy edges.



that all models recover the core dependency struc-               Table 4: Impact of dependency-graph perturbations on
ture needed by STRACE. Their differences mainly                  Success Rate.
appear in granularity and the amount of extra
infrastructure-level detail: stronger models pro-                Graph Settings                                          SR
duce cleaner and more appropriately scoped graphs,               Base Agent (No optimization)                           48%
while weaker models may introduce additional                     No dependency graph                                    48%
                                                                 Remove 25% edges                                       54%
noisy edges. Importantly, even the weakest graph                 Add 25% edges                                          56%
still preserves the core dependencies and introduces             Remove 10% edges                                       56%
only about 10% noisy edges, suggesting that the                  Add 10% edges                                          62%
                                                                 STRACE                                                 56%
dependency-prior construction is reasonably stable
across optimizer backbones.
   RQ2: How sensitive is STRACE to noise in the
                                                                 This summary supports trace filtering through two
dependency prior?
                                                                 complementary signals:
   To answer RQ2, we conducted controlled per-
turbation experiments on the dependency prior, as                   • (a) Statistical Severity: The summary es-
shown in Table 4. We randomly add or remove 10%                       timates the conditional failure probability
or 25% of edges between graph nodes to simulate                       P (Task Fail | vi Fail), where vi denotes a lo-
missing dependencies or additional noisy depen-                       cal node error extracted from the structured
dencies. Removing the dependency graph entirely                       trace record. This identifies local failures that
causes performance to fall back to the base-agent                     are strongly associated with global task fail-
level (48%), confirming that the structural prior is                  ure, allowing STRACE to prioritize systemic
essential for effective optimization.                                 bottlenecks over low-impact or stochastic er-
   In contrast, STRACE remains stable when the                        rors.
graph is only partially noisy: removing 25% of                      • (b) Structural Path Patterns: The sum-
edges reduces success rate only slightly from 56%                     mary also tracks module invocation sequences
to 54%, while adding 25% of edges preserves the                       across traces to reveal recurring pathological
same 56% success rate. At the smaller 10% per-                        trajectories. Patterns such as self-loops, oscil-
turbation level, performance is preserved or even                     lations, and dead ends indicate failure modes
improved. These results indicate that STRACE                          that cannot be captured by node-level statis-
benefits substantially from having a dependency                       tics alone, and help select traces that preserve
prior, but does not require this prior to be perfectly                diverse structural failure behaviors.
specified.
                                                                 B.4   Instructions of Phases
B.3   Visualization of Failure Pattern Mining
                                                                 For readability, we present simplified versions of
Figure 5 provides a concrete example of the di-                  the instructions for each phase in this appendix, as
agnostic summary produced by the failure pattern                 shown in Figures 6–9. To support reproducibility
mining stage. Rather than feeding raw traces di-                 and reuse, the GitHub repository includes the full
rectly into the optimizer, STRACE first converts                 instruction templates together with a skill-based
heterogeneous logs into structured records and ag-               version that packages the same workflow for direct
gregates them into dataset-level failure patterns.               plug-in use.

                                                            14
                              Table 5: Ablation results with stage-wise cost breakdown.

                                           Cost at Phase1   Cost at Phase2   Cost at Phase3   Cost at Phase4   Overall Cost
                STRACE                        0.1135           0.1861           0.8515           1.8052          2.9563
         w/o Structural Modeling                 -             1.0099           2.2212           1.8734          5.1045
           w/o Trace Filtering                0.1667              -             0.6802            7.602          8.4489
  w/o Causal Localization (Current Node)      0.2956           0.5320              -             2.0486          2.8762
   w/o Causal Localization (Full Trace)       0.2500           0.3597              -             5.3179          5.9276



C     More Experiments Results                                   more accurate and more efficient.
C.1    Stage-wise Cost Breakdown for the
                                                                 w/o Trace Filtering (removing Phase 2). This
       Ablation Study
                                                                 variant removes Phase 2 and yields an overall
Table 5 reports the stage-wise cost of STRACE in                 cost of 8.4489, where Phase 4 alone increases to
USD. Cost is estimated by tracking the input and                 7.602 (90.0% of the total). In comparison, Phase 1
output tokens consumed by optimizer-side LLM                     (0.1667; 2.0%) and Phase 3 (0.6802; 8.1%) remain
calls and multiplying them by the Claude Son-                    small. The cost inflation is therefore primarily con-
net 4.5 API prices. For stage-wise cost, we ap-                  centrated in Phase 4, consistent with the intuition
ply the same calculation only to LLM calls within                that without diagnosis-driven localization, the sub-
each phase, and the overall cost is the sum across               sequent optimization must operate with less tar-
phases. Phase 1 corresponds to Structural Model-                 geted signals and incurs substantially higher down-
ing, Phase 2 to Failure Pattern Mining and Trace                 stream search/optimization overhead.
Filtering, Phase 3 to Causal Localization, and
Phase 4 to Inductive Policy Optimization. A dash                 w/o Slicing (Current Node) (removing Phase 3).
indicates the corresponding stage is removed in                  With slicing removed, the overall cost becomes
that variant.                                                    2.8762. The cost is still dominated by Phase 4
                                                                 (2.0486; 71.2%), while Phase 1 and Phase 2 in-
STRACE. The overall cost is 2.9563, dominated
                                                                 crease to 0.2956 (10.3%) and 0.5320 (18.5%),
by Phase 4 (1.8052; 61.1%), followed by Phase 3
                                                                 respectively. This suggests that when compact
(0.8515; 28.8%). Phase 1 (0.1135; 3.8%) and
                                                                 dependency-preserving slices are unavailable, more
Phase 2 (0.1861; 6.3%) contribute a relatively small
                                                                 computation shifts to earlier stages (especially di-
fraction, indicating that the main cost driver is the
                                                                 agnosis) and the optimization stage remains the
downstream optimization stage, while diagnosis
                                                                 major cost component.
and slicing introduce only modest overhead.
w/o Structural Modeling (removing Phase 1).                      w/o Slicing (Full Trace) (removing Phase 3).
This variant removes Phase 1 to analyze the cost                 This variant also removes Phase 3 but uses the
and performance impact of the dependency prior.                  complete trajectory as context, resulting in an
Although Phase 1 itself is inexpensive in STRACE                 overall cost of 5.9276. Phase 4 rises sharply to
(0.1135, only 3.8% of the total cost), removing                  5.3179 (89.7%), while Phase 1 and Phase 2 are
it produces the largest performance degradation                  0.2500 (4.2%) and 0.3597 (6.1%). Compared
in the ablation study, reducing success rate from                to STRACE, the increase is almost entirely at-
56% to 48%. At the same time, the overall cost                   tributable to Phase 4, consistent with token/turn
increases from 2.9563 to 5.1045, an increase of                  blow-up when long-horizon, unfiltered traces are
about 2.15. This indicates that without the depen-               directly used in downstream prompt optimization.
dency prior, the optimizer must spend substantially
more effort inferring relationships among differ-                Summary. Across variants, the largest cost vari-
ent components from traces alone, inspecting more                ations are concentrated in Phase 4. Phase 2 (trace
trajectory context to reason about possible causal               filtering) primarily reduces downstream optimiza-
paths. Moreover, this inference is less reliable and             tion overhead by localizing failures, while Phase 3
can lead to incorrect failure paths. Thus, Phase 1               (causal localization) avoids shifting costs to Phase 4
has low direct cost but plays an important role in               by providing compact, dependency-preserving con-
making subsequent localization and repair both                   text in place of full-trace inputs.

                                                            15
                             Table 6: Average Turns of STRACE and VeruSAGE.


              Method                IronKV    Memory Allocator           Node Replication       NRKernel     Storage
     VeruSAGE (Base Agent)           12.04              9.17                    7.80              14.83      13.00
  VeruSAGE (STRACE-enhanced)          8.42              7.39                    4.00               8.20       8.31


             Table 7: Performance on VeruSAGE-Bench of STRACE and other hands-off models.

              SR                IronKV   Memory Allocator          Node Replication    NRKernel    Storage   Overall
             GPT-5              75.0%          55.6%                    90.0%           31.7%       23.1%     50.0%
  o4-mini (STRACE-enhanced)     62.5%          88.9%                   100.0%           31.7%       61.5%     58.5%
        Claude Sonnet 4         79.2%          66.7%                    70.0%           46.3%       46.2%     59.4%



C.2   Average Turns of VeruSAGE                              while the remaining categories also exhibit steady
      (STRACE-enhanced) Compared to the                      decreases. Overall, these results suggest that
      Base Agent                                             STRACE-enhanced prompting improves per-turn
                                                             decision quality and action effectiveness within
In VeruSAGE, a turn is the atomic unit of a
                                                             VeruSAGE, thereby reaching a valid repair with
repair attempt in the outer interaction loop, re-
                                                             fewer interaction rounds and lower iterative over-
flecting how many iterations are needed before
                                                             head under the same stopping criteria.
the system succeeds or terminates. For most
failure types, invoking a single sub-agent to
                                                             C.3    STRACE Performance on
propose and apply a fix counts as one turn.
                                                                    VeruSAGE-Bench Compared with
For assertion failures, VeruSAGE first triggers
                                                                    Hands-off Agents
an assertion_reasoning_pipeline sub-agent
that analyzes the error and selects a special-               We additionally compare STRACE with hands-off
ized downstream sub-agent; in this case, the                 agents reported in VeruSAGE. In VeruSAGE, the
assertion_reasoning_pipeline together with                   hands-off approach instantiates a generic coding
its selected sub-agent are treated as one turn, since        agent (a CLI agent) with a lightweight prompt
they form a coupled decision–execution step within           that primarily enforces anti-cheating constraints,
the same outer-loop attempt.                                 while granting the model direct tool access to (i)
   Average Turns complements Success Rate by                 running Verus, (ii) running a cheat checker, and
characterizing efficiency among successful (and              (iii) inspecting the Verus standard library (vstd)
attempted) repairs. Fewer turns indicate faster con-         as needed. This setting intentionally provides lit-
vergence with fewer outer-loop iterations, which             tle verification-specific tutoring, and relies on the
typically corresponds to fewer LLM calls, lower              underlying coding capability of frontier models to-
latency, and reduced interaction overhead under              gether with tool feedback from the verifier. (Yang
the same stopping criteria (i.e., stopping early upon        et al., 2025)
success or terminating at the maximum allowed                   We report two hands-off baselines based on
attempts). For each task instance, the number of             frontier models: GPT-5 and Claude Sonnet 4.
turns is counted until success. If the agent fails to        Their hands-off numbers are collected from the
solve within the allowed attempts, the maximum-              VeruSAGE study and used as reference results un-
turn cutoff is recorded. The reported value is then          der the same VeruSAGE-Bench suite and evalua-
averaged across the evaluation set.                          tion protocol. STRACE is evaluated on the same
   As shown in Table 6, VeruSAGE (STRACE-                    benchmark split and compared against these hands-
enhanced) consistently requires fewer turns                  off agents accordingly.
than the VeruSAGE base agent across all five                    As shown in Table 7, STRACE optimized
VeruSAGE-Bench categories, indicating faster con-            VeruSAGE achieves an overall success rate that
vergence in the outer repair loop. The reduc-                is competitive with strong hands-off agents. In par-
tion is most pronounced on the more challeng-                ticular, STRACE outperforms the hands-off GPT-5
ing benchmarks (e.g., IronKV and NRKernel),                  baseline in overall SR, and reaches a comparable

                                                        16
overall level to Claude Sonnet 4 (58.5% vs 59.4%),                  the current goal structure.
despite using a substantially smaller model o4-mini.             • USELEMMA: Identify specific helper
The gains are most evident on Memory Allocator,                     lemmas/proof functions available in the
Node Replication, and Storage, indicating that our                  file and state what each lemma estab-
learned, task-specific guidance can substantially                   lishes. Do not select USELEMMA
improve repair reliability in several benchmark                     if no relevant lemmas exist; prefer ac-
categories. Meanwhile, the gap on IronKV and                        tions that construct the proof directly
NRKernel suggests that some failure modes still                     (e.g., CASE_ANALYSIS, INDUCTION,
benefit from stronger general reasoning and long-                   COMPUTE).
horizon robustness. These results demonstrate that               • CASE_ANALYSIS: Specify the exact
STRACE can meaningfully close the performance                       variable or expression to split on and
gap between lightweight models and frontier hands-                  what each branch should establish (e.g.,
off agents on VeruSAGE-Bench.                                       which inequality or domain condition is
                                                                    proven in each case).
D     Evolution Examples in VeruSAGE Task                        • INDUCTION: State the inductive struc-
In this section, we present the actual general-                     ture (base case and inductive hypothesis)
ized rules synthesized from the VeruSAGE bench-                     and how the hypothesis connects to the
mark for the assertion_reasoning_pipeline                           current goal.
module. Crucially, STRACE de-contextualizes spe-                 • EXTENSIONAL_EQUALITY: Indi-
cific trace observations (e.g., "Sub-agent A failed                 cate which collection equality/property
on input X") into transferable heuristics reusable                  requires element-wise reasoning and
across varying proof states. In particular, the re-                 what domain/length conditions need to
vised prompt distills three types of reusable rules:                be established.
                                                                 • SEQSETMAP: List the 2–3 most rel-
    1. Failure-aware stopping condition and ac-
                                                                    evant Seq/Set/Map lemmas to invoke;
       tion switching.
                                                                    avoid invoking an overly broad lemma
          • Track repeated failures: Maintain                       set to prevent timeouts.
            awareness of how many times each ac-
                                                             3. Multi-round planning strategy.
            tion type has been attempted and rejected
                                                                 • Build on progress: Explicitly reference
            under the current proof context.
                                                                    what has been established by previously
          • Stopping condition: If an action has
                                                                    accepted fixes and explain how the next
            been attempted 2–3 times and is consis-
                                                                    action extends that progress.
            tently rejected (especially due to syntax
                                                                 • Develop a short proof plan: For com-
            errors or does not fix the target asser-
                                                                    plex goals, outline a minimal multi-step
            tion), do not select that action again in
                                                                    plan (e.g., establish a key auxiliary fact,
            the same context.
                                                                    prove the main implication, connect to
          • Action switching: Instead, switch to a
                                                                    the final goal).
            different secondary action from the can-
                                                                 • Avoid random exploration: Do not
            didate set; if all reasonable options are
                                                                    switch between unrelated actions with-
            exhausted, explicitly mark the issue as
                                                                    out a clear logical progression; each ac-
            requiring human intervention.
                                                                    tion should advance the proof toward the
          • Example: If INDUCTION fails three
                                                                    current failing goal.
            times with syntax errors, switch to
            alternatives such as USELEMMA or
            CASE_ANALYSIS rather than retrying
            INDUCTION again.
    2. Sub-agent-selection boundaries and action-
       able guidance.
          • General requirement: The guidance
            field must be specific and actionable
            (avoid generic suggestions); include con-
            crete anchors from the visible code and

                                                        17
Figure 5: Visualization of a Failure Summarization Map generated during the optimization of the IronKV project.
STRACE first parses raw traces into structured execution records containing the global task outcome, local node
status, and module invocation sequence. The map then summarizes the trace corpus along two analytical dimensions:
Statistical Severity, which estimates the conditional probability of global failure given each local node error, and
Structural Path Patterns, which identifies recurring pathological trajectories such as self-loops, oscillations, and
dead ends. These aggregated diagnostics serve as the quantitative basis for selecting high-value traces for causal
localization.



                                                        18
Figure 6: Instruction for Phase 1–Structural Modeling.




                         19
Figure 7: Instruction for Phase 2 – Failure Pattern Mining and Trace Filtering.




                                      20
Figure 8: Instruction for Phase 3 – Causal Localization.




                          21
Figure 9: Instruction for Phase 4 – Inductive Policy Optimization.




                               22
