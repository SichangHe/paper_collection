                                        Accepted at ICLR 2026 Agents in the Wild (AIWILD) Workshop




                                        AGENTIFIED A SSESSMENT OF L OGICAL R EASONING
                                        AGENTS
                                         Zhiyu Ni∗                                                        Yifeng Xiao∗
                                         University of California, Berkeley                               University of California, Berkeley
                                         zhiyuni@berkeley.edu                                             yifeng xiao@berkeley.edu

                                         Zheng Liang∗
                                         University of California, Berkeley
                                         zhliang@berkeley.edu
arXiv:2603.02788v4 [cs.AI] 2 Apr 2026




                                                                                      A BSTRACT

                                                     We present a framework for evaluating and benchmarking logical reasoning agents
                                                     when assessment itself must be reproducible, auditable, and robust to execution
                                                     failures. Building on agentified assessment, we use an assessor agent to issue
                                                     tasks, enforce execution budgets, parse outputs, and record structured failure
                                                     types, while the agent under test only needs to expose a standardized agent-to-
                                                     agent interface. As a case study, we benchmark an auto-formalization agent for
                                                     first-order logic (FOL) reasoning on a solver-verified and repaired split of FO-
                                                     LIO. The agent translates natural language premises and conclusions into exe-
                                                     cutable Z3Py programs and employs satisfiability modulo theories (SMT) solv-
                                                     ing to determine logical entailment. On the cleaned FOLIO validation set, the
                                                     auto-formalization agent achieves 86.70% accuracy under the assessor protocol,
                                                     outperforming a chain-of-thought baseline (73.89%).


                                        1       I NTRODUCTION

                                        Evaluating and benchmarking reasoning agents is challenging because failures occur at multiple
                                        layers, including model reasoning and tool execution. As a result, static evaluation harnesses often
                                        conflate operational failures (e.g., timeouts, runtime errors, output parsing failures) with reasoning
                                        errors, and may hide these failure modes behind a single accuracy number. Moreover, traditional
                                        setups tightly couple benchmark logic to agent implementations, so integration effort grows with the
                                        number of benchmarks.
                                        In this work, we study first-order logic (FOL) inference on FOLIO (Han et al., 2024) and adopt
                                        agentified agent assessment (AAA) as described in AgentBeats (AgentBeats, 2026), where assess-
                                        ment logic is implemented as an assessor agent that interacts with an agent under test through a
                                        standardized agent-to-agent (A2A) interface (A2A Protocol, 2026).
                                        We conduct verification and repair on the FOLIO dataset (Han et al., 2024) using a data cleaning
                                        pipeline, establishing a more reliable benchmark. On the cleaned benchmark, we implement a
                                        white-box auto-formalization agent that achieves 86.70% accuracy on the FOLIO validation set,
                                        outperforming a chain-of-thought baseline (73.89%) (Wei et al., 2022).


                                        2       B ENCHMARK AND DATA C LEANING

                                        We evaluate on FOLIO (Han et al., 2024), a first-order logic (FOL) reasoning benchmark consisting
                                        of natural-language premises and conclusions paired with formal FOL annotations. FOLIO is de-
                                        rived from Wikipedia-based real-world scenarios and requires both natural language understanding
                                        and logical reasoning. For each example, FOLIO provides one of three labels: T RUE (the conclusion
                                            ∗
                                                Equal contribution.


                                                                                            1
Accepted at ICLR 2026 Agents in the Wild (AIWILD) Workshop




            FOL Premises & Conclusion           NL Premises & Conclusion

                                     Inconsistency
               Premise Consistency                     Translation Error
                     Check                               Identification


                   Implication                                                              Human Expert
                                                         FOL Repair
                    Checking             Label                                                Review
                                        Mismatch
                 Verified Instance                                                       Final Label Decision
                                                   Repaired FOL Premises &
                                                          Conclusion


                            Figure 1: Overview of the data cleaning pipeline.


is logically entailed by the premises), FALSE (the conclusion contradicts the premises), or U NCER -
TAIN (the conclusion cannot be determined from the premises). We evaluate classification accuracy
against human-annotated ground-truth labels.

2.1   V ERIFICATION AND R EPAIR P IPELINE

The original FOLIO dataset exhibits potential label errors and misalignments between natural lan-
guage and formal annotations due to the complexity of semantic parsing. To establish a more reliable
benchmark, we implement a systematic data cleaning pipeline (Figure 1) that leverages symbolic
verification using the Vampire theorem prover (Kovács & Voronkov, 2013) to execute formal rea-
soning on FOL representations. When verification results conflict with expected labels, we identify
and iteratively repair translation errors.
Given a premise set {ϕ1 , ϕ2 , . . . } and a conclusion φ, we detail the pipeline as follows:
Formal Premise-Conclusion Checking. We verify the implication relation between premises      V and
conclusion in two steps. First, we check whether the premises are consistent (i.e., whether i ϕi is
satisfiable). Then, we perform implication checking using the following satisfiability conditions:
                                  ^                ^
                     T RUE ⇐⇒        ϕi → φ ⇐⇒         ϕi ∧ ¬φ is unsatisfiable,                  (1)
                                        i                         i
                                        ^                          ^
                     FALSE ⇐⇒               ϕi → ¬φ ⇐⇒                    ϕi ∧ φ is unsatisfiable.              (2)
                                        i                             i

When both implication checks fail, we label the instance as U NCERTAIN. We then compare verifi-
cation results against expected labels to identify potential annotation errors.
NL-FOL Misalignment Identification and Repair. When premises are inconsistent or verifica-
tion results conflict with expected labels, we employ a check-and-fix procedure using two LLM-
based agents. A critique agent diagnoses systematic translation errors (e.g., unbalanced parenthe-
ses, lexical typos, and naming convention inconsistencies) by analyzing the original natural lan-
guage and FOL annotations. A refiner agent then executes targeted corrections. We iteratively
re-verify the repaired FOL until the expected labels are achieved. If the number of iterations ex-
ceeds a predefined threshold without resolution, we flag the instance for manual review. We release
the cleaned and repaired FOLIO split at https://huggingface.co/datasets/yfxiao/
folio-refined.

2.2   B ENCHMARK S TATISTICS

We classify instances into three categories: (i) verified directly with the original FOL, (ii) verified
after automatic repair, and (iii) problematic instances flagged for manual review. For the training set
(1,001 examples): 674 (67.3%) verified directly, 23 (2.3%) after automatic repair, and 304 (30.4%)
remain problematic. For the validation set (203 examples): 154 (75.9%) verified directly, 10 (4.9%)
after automatic repair, and 39 (19.2%) remain problematic. In total, we identify 3.8% potential label
errors in the training set and 1.5% in the validation set, improving both the NL-FOL translation
quality and the reliability of labels for evaluation.


                                                            2
Accepted at ICLR 2026 Agents in the Wild (AIWILD) Workshop




Figure 2: Traditional evaluation harnesses couple task execution, environments, and judging logic
to a preset harness. In agentified assessment, an assessor agent evaluates an agent under test via an
A2A interface (A2A Protocol, 2026), reducing integration overhead.


3     AGENTIFIED E VALUATION F RAMEWORK

3.1   AGENTIFIED A SSESSMENT

We formalize the evaluation of reasoning agents by treating assessment itself as an agent. Instead
of relying on a static evaluation script, we separate the system into two interacting components:
an agent under test, which performs reasoning, and an assessor agent, which controls task exe-
cution, interprets outcomes, and assigns scores. We adopt the agentified agent assessment (AAA)
abstraction described in AgentBeats (AgentBeats, 2026), where the assessor and the agent under test
communicate through an agent-to-agent (A2A) interface (A2A Protocol, 2026).
The primary value of AAA is not to address individual operational issues (e.g., timeouts), which
can also be handled in traditional benchmarks. Instead, it changes the integration cost model for
benchmarking agents: in traditional setups, integration cost grows with the number of benchmarks
(O(n)), whereas under AAA, an agent implements A2A once and can participate in many assessors
(O(1)). This decoupling enables plug-and-play evaluation and architecture freedom for agents with
diverse internal designs.
As illustrated in Figure 2, traditional benchmarks couple task orchestration and judging to a
benchmark-specific harness. AAA decouples these components by packaging evaluation logic as
an assessor agent that interacts with an agent under test through a standardized interface, allowing
the assessor to evolve without breaking participants.


3.2   A SSESSOR AGENT (E VALUATION P ROTOCOL )

The assessor agent implements the evaluation protocol. For each premise and conclusion pair, it
issues the task to the agent under test, enforces execution budgets (e.g., timeouts and retries), parses
and validates the response, and assigns a final label (T RUE, FALSE, or U NCERTAIN) according to
the benchmark criteria.
If the agent under test outputs additional text, the assessor parses the final label deterministically;
non-parseable outputs are recorded as PARSE E RROR. Rather than discarding failures, the assessor
records structured failure types such as T IMEOUT, RUNTIME E RROR, and PARSE E RROR. Finally,
the assessor emits a machine-consumable evaluation artifact containing per-instance records (gold
label, predicted label, correctness, error type if any, latency) and aggregate metrics.


3.3   R EASONING AGENTS U NDER T EST

We benchmark two agents under the same assessor.


                                                   3
Accepted at ICLR 2026 Agents in the Wild (AIWILD) Workshop




Chain-of-thought baseline. We use chain-of-thought prompting (Wei et al., 2022): the agent is
instructed to reason step by step and then output its final answer as the last line containing exactly
one label in {T RUE, FALSE, U NCERTAIN}, which is parsed by the assessor.
Auto-formalization agent. The auto-formalization agent solves first-order logic (FOL) inference
problems by translating natural language premises and conclusions into executable symbolic pro-
grams and performing logical reasoning via solver execution (Pan et al., 2023; Ni et al., 2026). The
reasoning process follows a two-stage pipeline. In Stage 1 (Code Generation), a language model
generates executable Z3Py (De Moura & Bjørner, 2008) code from the input. In Stage 2 (Execution
and Verification), the generated program is executed in a sandbox environment with a 60-second
timeout.
Logical validity is determined
                       V         through satisfiability checking as specified in the benchmark
                                                                                          V    defini-
tion (Section 2): if i ϕi ∧ ¬φ is unsatisfiable, the conclusion is labeled T RUE; if i ϕi ∧ φ is
unsatisfiable, it is labeled FALSE; otherwise, the label is U NCERTAIN.
To improve robustness, the agent incorporates a self-repair loop with up to three attempts. When
execution fails due to syntax errors or malformed quantifiers, the agent extracts the error message
and performs targeted code repair before re-execution.

Implementation note. We implement the assessor and agents under test on top of Agent-
Beats (AgentBeats, 2026), where they communicate via A2A (A2A Protocol, 2026) (and option-
ally expose tools via MCP (Anthropic, 2024)). We also constructed a logical reasoning leaderboard
that runs the assessor against registered agents and records per-run artifacts (accuracy, latency, and
failure types), enabling reproducible comparisons across agents.

4     E XPERIMENTS

4.1   E XPERIMENTAL S ETUP AND BASELINE

We evaluate on the cleaned FOLIO validation set comprising 203 examples after label verification.
Both the chain-of-thought baseline agent and the auto-formalization agent use Gemini 2.5 Flash (Co-
manici et al., 2025) as the backbone LLM with a temperature T = 0.0 for deterministic outputs and
default maximum output tokens n = 65535. Both agents use a system-user prompt structure. For
the chain-of-thought baseline, the system prompt elicits step-by-step reasoning and requires the fi-
nal answer label to appear as the last line; for auto-formalization, it includes Z3 code generation
instructions with syntax guidelines. No in-context learning (ICL) examples are provided for either
agent.

4.2   R ESULTS AND A NALYSIS

Table 1 reports accuracy broken down by ground-truth label category, together with overall perfor-
mance. The chain-of-thought baseline achieves an overall accuracy of 73.89% (150/203), while the
auto-formalization agent improves accuracy to 86.70% (176/203).

                                Chain-of-Thought             Auto-formalization
               Category      Correct Total    Acc.         Correct Total    Acc.
               True            65      73   89.04%           66      73    90.41%
               False           27      61   44.26%           47      61    77.05%
               Uncertain       58      69   84.06%           63      69    91.30%
               Overall        150     203 73.89%            176     203 86.70%

         Table 1: Per-category and overall accuracy on the cleaned FOLIO validation set.

The largest improvement is observed in the FALSE category, where accuracy increases from 44.26%
to 77.05%. Performance on T RUE cases is comparable across methods. The auto-formalization
agent also improves on U NCERTAIN cases (84.06% to 91.30%), highlighting the advantage of
solver-based reasoning in handling logical indeterminacy. Overall, these results demonstrate that
formal verification improves robustness on this benchmark, leading to higher overall accuracy.


                                                  4
Accepted at ICLR 2026 Agents in the Wild (AIWILD) Workshop




5   C ONCLUSION
This work benchmarks logical reasoning agents under agentified assessment, where an assessor
agent enforces budgets, records structured failures, and emits auditable evaluation artifacts. As a
case study, an auto-formalization agent that translates natural language problems into executable
Z3Py code and uses solver execution outperforms a chain-of-thought baseline on a solver-verified
and repaired split of FOLIO, with the largest gains on contradiction (FALSE) cases and consistent
improvements on indeterminate (U NCERTAIN) cases. Future work could extend assessor policies
and apply agentified assessment to richer tool-using agent settings.

R EFERENCES
A2A Protocol. Agent2agent (a2a) protocol specification, 2026. https://a2a-protocol.
  org/latest/.
AgentBeats. Agentified agent assessment (aaa), 2026. https://docs.agentbeats.dev/.
Anthropic. Model context protocol (mcp), 2024. https://docs.anthropic.com/en/
  docs/mcp.
Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit
  Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing the
  frontier with advanced reasoning, multimodality, long context, and next generation agentic capa-
  bilities. arXiv preprint arXiv:2507.06261, 2025.
Leonardo De Moura and Nikolaj Bjørner. Z3: An efficient smt solver. In International conference
  on Tools and Algorithms for the Construction and Analysis of Systems, pp. 337–340. Springer,
  2008.
Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhenting Qi, Martin Riddell, Wenfei Zhou, James
  Coady, David Peng, Yujie Qiao, Luke Benson, et al. Folio: Natural language reasoning with first-
  order logic. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language
  Processing, pp. 22017–22031, 2024.
Laura Kovács and Andrei Voronkov. First-order theorem proving and vampire. In International
  Conference on Computer Aided Verification, pp. 1–35. Springer, 2013.
Zhiyu Ni, Zheng Liang, Liangcheng Song, Chenrui Cao, Xian Zhang, Alberto Sangiovanni-
  Vincentelli, and Pierluigi Nuzzo. Draft-and-prune: Improving the reliability of auto-formalization
  for logical reasoning. arXiv preprint arXiv:2603.17233, 2026.
Liangming Pan, Alon Albalak, Xinyi Wang, and William Wang. Logic-lm: Empowering large lan-
  guage models with symbolic solvers for faithful logical reasoning. In Findings of the Association
  for Computational Linguistics: EMNLP 2023, pp. 3806–3824, 2023.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny
  Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. Advances in
  neural information processing systems, 35:24824–24837, 2022.




                                                 5
