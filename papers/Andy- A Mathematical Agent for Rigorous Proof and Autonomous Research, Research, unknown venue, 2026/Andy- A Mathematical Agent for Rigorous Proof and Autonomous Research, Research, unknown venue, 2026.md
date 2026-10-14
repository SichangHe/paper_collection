                           Andy: A Mathematical Agent for Rigorous Proof and Autonomous
                           Research
                           Global Exponential Leader-Follower Synchronization of Delayed Heterogeneous Networks via
                           Switching Hybrid Control

                           Zi’an Wanga,b
                           a School of Mathematical Sciences, Tongji University, Shanghai 200092, China
                           b Key Laboratory of Intelligent Computing and Applications (Tongji University), Ministry of Education, Shanghai 200092, China

                           Project homepage and source code: https://github.com/mowaiwaim/Andy
arXiv:2608.15052v2 [cs.AI] 20 Aug 2026




                           ARTICLE INFO                                     ABSTRACT
                           Keywords:                                        Andy is an autonomous mathematical research agent that turns a mathematical problem into
                           Autonomous mathematical research                 a traceable proof. It solves or verifies a submitted problem, formulates a literature-grounded
                           agent                                            new problem through a research-value gate, and carries it through proof construction and final
                           Executable proof DAG                             verification. It organizes proof steps in an executable DAG, verifies each step independently
                           Local verification                               and binds the result to a certificate, retains verified work whose interfaces remain unchanged
                           Incremental repair                               during local repair, and records the full path from problem formulation to final proof. The system
                           Hybrid control                                   separates proof generation from correctness evaluation and can acquire, retain, retrieve, and
                           Exponential synchronization                      reuse knowledge from existing results. Starting from a self-triggered impulsive consensus result
                                                                            [1], Andy formulates a global exponential leader-follower synchronization problem for delayed
                                                                            heterogeneous networks with switching communication topologies. The proposed hybrid control
                                                                            combines self-triggered impulses with execution delay and continuous feedback over a recovery
                                                                            window. After each delayed impulse, the feedback cancels the delayed error channel until the
                                                                            pre-impulse history leaves the active delay interval. Sufficient conditions for global exponential
                                                                            synchronization are established, Zeno behavior is excluded for both timing sequences, and a
                                                                            numerical example illustrates the result.




                           1. Introduction
                                Large language models and mathematical reasoning systems can solve increasingly difficult fixed problems.
                           Mathematical research requires a broader workflow. A research system must identify a meaningful question, ground
                           it in relevant literature, construct a long proof, distinguish generation from correctness evaluation, and revise local
                           failures without discarding verified work. These capabilities are often studied separately, so it remains unclear whether
                           a mathematical agent can carry a research task from a verified starting point to a traceable theorem, proof, and numerical
                           certificate.
                                Related systems provide useful context for this objective. FunSearch pairs programs proposed by a pretrained
                           large language model with a problem-specific systematic evaluator. AlphaGeometry uses a neural model to generate
                           auxiliary constructions and a symbolic engine to complete geometry proofs [2, 3]. These systems demonstrate how
                           learned generation can be combined with an explicit external evaluation or deduction mechanism.
                                Recent mathematical research agents move beyond fixed benchmark problems. Moonshine extracts structure from
                           classical problems, formulates conjectures, builds connections, and identifies obstacles [4]. Research Math Agents
                           (RMA) targets long-horizon research problems through literature grounding, structured knowledge, iterative proof
                           refinement, and coordinated proposer and verifier roles [5]. QED organizes multiple agents around failure modes
                           observed in open-problem proving and emphasizes structured verification and expert assessment of generated proofs
                           [6].
                                Recent systems distribute the research cycle differently. ProofCouncil uses an author–critic loop implemented by
                           a conditional workflow-DAG library [7]. Danus coordinates parallel workers through a verifier-gated fact graph that
                           stores proofs and logical dependencies and supports transitive revocation [8]. Rethlas and Archon couple informal
                           research reasoning with Lean formalization [9], while MMAT combines natural-language and formal-language provers
                                         wza1012@tongji.edu.cn (Z. Wang)


                           Zi’an Wang                                                                                                                        Page 1 of 20
                           Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

with a knowledge-base manager in a full-cycle co-pilot architecture [10]. Table 1 compares mechanisms explicitly
documented in the primary reports.

Table 1
Capabilities reported by representative mathematical research systems.
                                                                                    New       Proof      Indep.    Long-term    Formal       Local
 System               Primary research object                                     problem    decomp.     check      memory       proof    revocation
 Moonshine [4]        Conjecture generation and theory exploration                   E         NR          P           E          NR          NR
 RMA [5]              Literature-grounded long-horizon proofs                       NR          E          E           P          NR          NR
 QED [6]              Natural-language proofs for open problems                     NR          E          E           P          NR           P
 ProofCouncil         Author–critic open-problem solving                            NR          P          E           P           P          NR
 [7]
 Danus [8]            Verifier-gated fact-graph proof search                        NR          E           E          E          NR          E
 Rethlas–             Informal reasoning followed by Lean formalization             NR          E           E          E           E          P
 Archon [9]
 MMAT [10]            Natural- and formal-language research co-pilot                 P          E           E          E           E          P
 Andy                 Value-gated problem formulation and incremental proof          E          E           E          E          NR          E
E denotes an explicitly implemented or reported capability. P denotes partial, case-specific, run-local, or architecturally non-equivalent support. NR
records only a lack of reporting in the cited primary source and leaves possible implementations unassessed.


    Together, these developments motivate mathematical agents whose research objects, proof dependencies, and
evaluations remain explicit and auditable.
    To address this gap, we developed Andy, a verification-centered autonomous mathematical research agent. Andy
combines solver and evaluator separation, literature-grounded problem generation, a research-value gate, DAG-based
proof execution, independent verification, targeted repair, and reusable memory in one auditable workflow. The case
study in this paper examines whether this workflow can transform a verified control-theoretic result into a technically
meaningful new problem and complete the corresponding theorem, proof, and numerical verification.
    The main contributions of Andy are summarized as follows.
 (1) We define an executable, version-bound proof DAG. Each node is a five-part research object consisting of a
     statement, assumptions, dependencies, a proof, and a verification certificate. The certificate is tied to the exact
     node version that it verifies. This representation converts a proof outline into an executable dependency structure
     with explicit admissibility and audit conditions.
 (2) We implement a verification-controlled DAG executor. A node becomes available only after all its predecessors
     have been certified. The executor performs topological execution, freezes certified nodes, compares node
     interfaces after revision, propagates invalidation only when an interface changes, activates backup routes when a
     branch fails, and re-verifies the assembled proof. Local repair therefore retains certified work whose dependencies
     remain valid.
 (3) We provide an end-to-end control-theoretic case study with a complete audit trail. Starting from a verified self-
     triggered impulsive consensus result, Andy revised the proposed problem eight times across nine versions and
     explored seven proof routes. It ultimately produced a recovery-window synchronization theorem for delayed
     heterogeneous networks under switching hybrid control, a complete proof, and a numerical illustration. The
     recorded trace identifies failed routes, preserved nodes, and the reason for selecting the final route.
    The remainder of this paper is organized as follows. Section 2 presents the Andy agent architecture. Section 3 gives
the control-theoretic case study. Section 4 concludes the paper.


2. Andy Agent Architecture
   Andy organizes problem solving, problem generation, proof construction, and verification as a single revisable
process. Figure 1 summarizes the complete workflow, and the following subsections describe its main components.

2.1. Solver–Evaluator Separation
   Andy uses a dual-model architecture that separates the roles of solver and evaluator. The main solver uses DeepSeek
V4 Pro. It is responsible for solving the original problem, generating proofs, generating new problems, and revising
proofs. The mathematical correctness evaluator uses Claude Sonnet 5. It reviews answers and proofs along three

Zi’an Wang                                                                                                                             Page 2 of 20
                       Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

                                                                                       repair if needed




            Submitted problem                              Solve the problem or                      Independent correctness check:
           and optional solution                        verify the supplied solution                 premises, calculations, and logic


                                        re-evaluate


           Targeted revision until                    Evaluate importance, originality,                     Literature-grounded
        the selected threshold is met                    feasibility, and coherence                       new-problem formulation


                                                                            repair affected node and descendants


          Explore proof routes and                       Build a lemma DAG with                             Execute, verify, freeze,
         select a promising strategy                      explicit dependencies                           or locally repair each node




                                                        Deliver the proof, certificates,              Assemble the complete proof
                                                      literature links, and research log              and perform final verification

                                            Figure 1: The research workflow of Andy.



dimensions: use of premises, correctness of calculations, and logical completeness. The evaluator cannot directly
modify a proof. It can only provide structured verification conclusions, error locations, and revision suggestions. The
main solver then completes the revisions. This separation of roles prevents the solver model from approving its own
answer without external review.
    To use Andy, the user must first provide a problem. If no answer is provided, Andy independently constructs a
solution or proof and submits it to the correctness evaluator for review. If an answer is provided, Andy directly verifies
that answer without solving the problem independently again.

Remark 2.1. During this study, Codex running GPT-5.6 Sol was placed outside Andy and used as a simulated
human monitor. It inspected the exposed intermediate reasoning, identified mathematical and strategic errors, and
returned targeted guidance. The external monitor supplied the guidance, and Andy’s solver retained responsibility for
implementing every revision. This setup shows that the current workflow can still benefit from external oversight when
deep reasoning errors are difficult for the internal roles to detect.

2.2. Literature-grounded Problem Generation
    After the original problem and its proof pass verification, Andy proposes a new research problem. Before a task
begins, the user can separately specify the direction for generating the problem or upload reference papers. This
guidance is used only during the generation, evaluation, and revision of the new problem. It does not affect the solution
and verification of the original problem.
    Andy analyzes the common features, differences, complementary relations, and research gaps among the papers.
In the new problem, it explains which papers were used, which conditions or methods were inherited, and which
substantive modifications were made. When the available materials are insufficient to assess originality, related work,
or proof tools, Andy can use Tavily to search for related literature as needed.

2.3. Research-value Gate
   The basic evaluation of a new problem covers four dimensions: importance, originality, feasibility, and coherence.
Importance measures whether solving the problem could advance a theory, method, or application. Originality checks
whether the problem only renames, rewrites, or directly restates an existing problem. Feasibility examines whether

Zi’an Wang                                                                                                                       Page 3 of 20
                      Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

there is a concrete proof strategy, usable tools, and a reasonable point of entry for the research. Coherence examines
whether the new problem follows naturally from the original problem or the references and whether it has one clear
research objective. It also checks that the problem is not a simple combination of several small problems. If the user
provides reference papers, the evaluation system adds a literature support dimension. This dimension checks whether
the new problem has traceable links to the papers and contains substantive modifications.
    The user can specify the target difficulty of the new problem. Every dimension is scored on a ten-point scale. An
easy problem requires a total score of at least 6.0 and a score of at least 4.5 in every dimension. A standard problem
requires a total score of at least 7.0 and a score of at least 5.5 in every dimension. A research-level problem requires a
total score of at least 7.5 and a score of at least 6.0 in every dimension. A pure rewriting of an existing problem triggers
a hard gate. A simple combination of several conclusions, the lack of a concrete feasible method, or the inclusion of
several parallel subproblems also triggers a hard gate. Such a problem does not pass verification. The user’s choice
of difficulty changes only the threshold for research value and the research cost. It does not reduce the correctness
requirements for the final proof.
    If a problem does not pass the evaluation, the evaluation stage explains the reason for each score deduction. It
also gives revision instructions that include the specific defect, the mathematical modification, and the acceptance
criterion after modification. The generator then revises the same problem draft in a targeted manner and returns it to
the evaluation stage for another review. By default, the system automatically enters the proof stage after the problem
reaches the threshold. The user can also choose to pause after the evaluation and intervene manually. Algorithm 1
summarizes this formulation, evaluation, and targeted-revision loop.

Algorithm 1 Problem formulation and quality gating
Require: Verified starting result 𝑅, literature 𝐿, user direction 𝑈 , and target thresholds 𝜃
Ensure: Accepted problem 𝑄⋆ and audit record 
 1: 𝑄0 ← F ORMULATE (𝑅, 𝐿, 𝑈 ) and initialize 
 2: for 𝑗 = 0, 1, … do
 3:     (𝐬𝑗 , 𝐠𝑗 ) ← E VALUATE(𝑄𝑗 , 𝐿, 𝜃)
 4:     Append 𝑄𝑗 , dimension scores 𝐬𝑗 , and gate verdicts 𝐠𝑗 to 
 5:     if all score thresholds and hard gates pass then
 6:           𝑄⋆ ← 𝑄𝑗 ; return (𝑄⋆ , )
 7:     end if
 8:     Δ𝑗 ← TARGETEDR EVISION(𝑄𝑗 , 𝐬𝑗 , 𝐠𝑗 )
 9:     𝑄𝑗+1 ← R EVISE(𝑄𝑗 , Δ𝑗 )
10: end for



2.4. DAG Proof Execution
    For the proof of a new problem, Andy provides two routes: a rigorous DAG proof route and a deep research route.
A directed acyclic graph (DAG) is a directed graph with no directed cycles and therefore admits a topological ordering.
In artificial intelligence, DAGs are widely used to encode conditional-dependence structures and organize probabilistic
inference [11].
    Andy adapts this dependency structure to proof construction. The rigorous DAG proof route first generates only a
proof outline, necessary definitions, and lemmas. Andy then represents the proof as a directed acyclic graph. Each node
corresponds to a lemma or proof step with explicit inputs, assumptions, and a conclusion. Directed edges represent
logical dependencies between nodes. The system first checks node identifiers, dependency relations, and reachability
of the target. It then executes the nodes one by one in topological order.
    DAG mode starts a main proof branch. If the main branch cannot be completed mathematically, Andy activates an
alternative branch. If the new DAG executor and the alternative branch both fail, the system can also use a multibranch
proof chain as a fallback and try several proof routes.
    For a research-level problem, the deep research route can be selected. This route first explores several proof
strategies at low cost. It compares only the key construction, required lemmas, main risks, and likelihood of completion
for each route. After selecting the most promising route, the system converts it into a DAG. It then completes the proof
rigorously through node-by-node execution, local verification, freezing, and final overall verification. For a difficult


Zi’an Wang                                                                                                    Page 4 of 20
                      Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

and open-ended problem, this route first obtains the necessary breadth of exploration at low cost. It then concentrates
most of the computational effort on the most promising route.
    For execution, a node version is recorded as 𝑣 = (𝑆𝑣 , 𝐴𝑣 , 𝐷𝑣 , Π𝑣 , 𝐶𝑣 ), where 𝑆𝑣 , 𝐴𝑣 , 𝐷𝑣 , Π𝑣 , and 𝐶𝑣 are its
statement, assumptions, dependency set, proof, and verification certificate, respectively. Its dependency interface is
𝐼𝑣 = (𝑆𝑣 , 𝐴𝑣 , 𝐷𝑣 ), and ℎ𝑣 = 𝐻(𝐼𝑣 ) is the corresponding interface fingerprint. The certificate is bound to the exact
node version and its execution metadata. Algorithm 2 gives the corresponding topological execution and verification
procedure.

Algorithm 2 Proof-DAG execution
Require: Accepted problem 𝑄⋆ and planned main and backup routes
Ensure: A frozen target node or a certified failure record
 1: Build a versioned DAG 𝐺 and reject cycles, missing dependencies, or an unreachable target
 2: while the target node is not frozen do
 3:    Select a ready node 𝑣 in topological order; every node in 𝐷𝑣 must be frozen
 4:    Π𝑣 ← E XECUTE(𝑆𝑣 , 𝐴𝑣 , 𝐷𝑣 )
 5:    𝐶𝑣 ← INDEPENDENTV ERIFY(𝑆𝑣 , 𝐴𝑣 , 𝐷𝑣 , Π𝑣 )
 6:    if 𝐶𝑣 passes then
 7:         Bind 𝐶𝑣 to the node version and execution metadata; FREEZE(𝑣)
 8:    else
 9:         Repair 𝑣, recompute ℎ𝑣 , and apply Algorithm 3
10:    end if
11:    if the active route is mathematically infeasible then
12:         Activate the highest-ranked unused backup route
13:    end if
14: end while
15: Assemble the proof from frozen nodes and perform an independent final verification



Remark 2.2. The present evaluation is preliminary and focuses on the efficiency of DAG execution in one
representative task. The main purpose of the DAG is to freeze the parts that have been confirmed as correct and
confine errors to local regions. This reduces repeated generation and repeated verification of the entire proof.
    We used Andy twice to process the problem “Study the zeros and monotonicity of the function 𝑥3 −𝑥.” An ordinary
proof attempt and verification process serves as the baseline. It took 1 hour, 22 minutes, and 12 seconds. The DAG
process took approximately 37 minutes and 59.7 seconds. The time decreased by approximately 53.8%.
    The new research problems generated by Andy in the two runs were not identical because of the randomness of
the LLM. The experiment shows that the DAG avoided unnecessary execution of complete branches and substantially
reduced the running time in this case. The entire time difference cannot be attributed to the DAG.

2.5. Verification and Targeted Repair
    When a node is executed, the solver can use only the available materials and dependency nodes that have passed
verification. After each new node is completed, it undergoes a separate local verification of premises, calculations, and
logic. A node is frozen after it passes verification. If a node fails, Andy repairs only that node and the descendants
affected by it. Unrelated sibling nodes are not regenerated. If a revision changes only the proof text and leaves
the proposition, assumptions, and dependency interface of the node unchanged, verified downstream results can
be retained. After all necessary nodes pass, the system assembles the complete proof and performs a unified final
verification. If the assembly stage requires a new bridging result, that result must first become a new node and pass a
separate verification. Let Desc𝐺 (𝑣) denote the direct and transitive descendants of node 𝑣 in 𝐺. Algorithm 3 makes the
repair and assembly contract explicit.




Zi’an Wang                                                                                                  Page 5 of 20
                       Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

Algorithm 3 Invalidation and final assembly
Require: Proof DAG 𝐺, revised node 𝑣, and old and new interface fingerprints ℎold       new
                                                                                   𝑣 , ℎ𝑣
Ensure: Updated
             { valid DAG and a final verification record
               {𝑣},               ℎold
                                   𝑣 = ℎ𝑣 ,
                                           new
 1: (𝑣) ←
                                   old
               {𝑣} ∪ Desc𝐺 (𝑣), ℎ𝑣 ≠ ℎnew  𝑣
 2: for all 𝑤 ∈ (𝑣) do
 3:     Revoke the frozen state and certificate of 𝑤
 4: end for
 5: Re-execute affected nodes in topological order under Algorithm 2
 6: Assemble the final proof using frozen nodes only
 7: if assembly introduces a new bridging proposition then
 8:     Create a new node for that proposition and verify it before continuing
 9: end if
10: Independently verify the assembled proof and bind the final record to all cited node versions



    The executor maintains four system invariants.
 (1) Dependencies must consist exclusively of verified nodes.
 (2) Each certificate is strictly bound to a specific statement, proof, context, model, prompt, and code version.
 (3) Any bridging proposition introduced during assembly must be represented and verified as a new node.
 (4) The final proof must not cite any invalidated node.

2.6. Memory and Knowledge Acquisition
    Andy is designed for long-term use and debugging by researchers. It therefore also has a memory function. Andy
manages logs and long-term memory separately. The logs provide complete records of problem versions, model rounds,
reasoning content returned by model interfaces, tool calls, search results, evaluation reasons, verification certificates,
DAG node revisions, frozen and invalidated states, causes of errors, and task checkpoints. These materials are saved
as session records and written to the project-level research log. A failed or interrupted task can therefore resume from
the corresponding stage.
    Long-term memory contains selected reusable research information. Andy can store proof-method preferences and
evaluation preferences explicitly stated by the researcher. Examples include “Prefer the Lyapunov method for problems
of this type in the future” and “A rewriting that only changes notation should not receive a high originality score.” It also
stores verified conclusions, successful proof patterns, failed routes, key difficulties, and connections among papers. A
new task retrieves only a small amount of memory relevant to the current problem. Failure records help avoid repeating
unsuccessful routes and are stored separately from mathematical evidence.
    Andy organizes its data around a runtime home directory. This directory contains configurations and credentials,
project workspaces, session logs, a session database, a knowledge base, long-term memory, Agent definitions, Skills,
Tools, runtime logs, and MCP server description files. During a research task, Andy can independently select memory
retrieval, knowledge-base queries, literature searches, and verification tools according to the current stage. It updates
the research state through a cycle of planning, execution, verification, and local revision.
    We also designed a research front end to make the system easier to use and review. The front end integrates
the creation of a research task, a real-time research workspace, and the final report into a complete workflow.
Users can upload materials for the main problem and reference papers. They can separately enter the research
requirements for the original problem and the direction for generating a new problem. They can also select the
target difficulty and proof mode. During execution, users can view stable stage progress, total running time, the
actual reasoning_content returned by the model interface, the verification process, evaluation reasons, literature
connections, and the dependencies, revisions, frozen states, and certificate states of DAG nodes. If users find an error
in the model’s reasoning, they can append a prompt to correct the research direction. This provides an interface for
human intervention. After the task is complete, users can directly download research outputs at different levels from
the front end.

Zi’an Wang                                                                                                     Page 6 of 20
                         Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

   Andy can ultimately deliver the original problem and its verification conclusion or complete solution, the new
problem generated by Andy, itemized scores and revision records, the complete proof of the new problem, and
connections to reference papers and retrieved literature. If the proof fails, it returns the reason for failure and subsequent
reduced-scope problems. The system can export Markdown, structured JSON, and both complete and concise PDF
reports. The complete report retains scores, tools, certificates, versions, and the research process for review and
auditing. The concise report retains only the original problem and its complete solution, together with the problem
generated by Andy and its complete proof. It is suitable for direct reading and communication.


3. Case Study
3.1. Source Problem
   The verified source problem is the self-triggered impulsive consensus problem of Hong and Zhang [1]. It studies
switched delay multi-agent systems under self-triggered impulsive control. Andy uses this result as a starting point and
asks how its scheduling and impulsive-control structure can be extended to a heterogeneous leader-follower network
with switching topology and impulse execution delay.

3.2. Problem Proposed by Andy
    We made only minor formatting adjustments to the model and theorem proposed by Andy. The result is presented
below.
    This case study considers a class of leader-follower heterogeneous networks with switching communication
topologies, time-varying delays, and impulse execution delays. The aim is to establish sufficient conditions for
synchronization under the joint action of continuous and impulsive control. The model and its regularity assumptions
are introduced first.
    Let 𝑁 and 𝑛 be positive integers. Throughout this section, 𝐼𝑚 denotes the 𝑚 × 𝑚 identity matrix, ⊗ denotes the
Kronecker product, and ‖ ⋅ ‖ denotes the Euclidean vector norm or its induced matrix norm. For symmetric matrices,
𝑋 ⪯ 𝑌 means that 𝑌 − 𝑋 is positive semidefinite.
    Let {𝑠𝑘 }𝑘≥0 be the sampling instants determined by the self-triggered algorithm introduced below. Let 𝜏 > 0 be
the known impulse execution delay, and define the corresponding impulse execution instants by 𝑡𝑘 ∶= 𝑠𝑘 + 𝜏. All state
trajectories are taken to be right-continuous at the impulse execution instants.
    Let ℎ̄ > 0, let ℎ ∶ [𝑠0 , ∞) → ℝ be a time-varying delay, and let 𝑓 , 𝑔 ∶ ℝ𝑛 → ℝ𝑛 be nonlinear functions.
    Consider the following 𝑛-dimensional leader:

       ̇ = −𝐶𝑠(𝑡) + 𝐴𝑓 (𝑠(𝑡)) + 𝐵𝑔(𝑠(𝑡 − ℎ(𝑡))),
       𝑠(𝑡)                                                                                                               (1)

where 𝐶, 𝐴, 𝐵 ∈ ℝ𝑛×𝑛 .
   The 𝑖th follower, 𝑖 = 1, … , 𝑁, satisfies the hybrid dynamics
     {                                                 (             )
           𝑥̇ 𝑖 (𝑡) = −𝐶𝑖 𝑥𝑖 (𝑡) + 𝐴𝑖 𝑓 (𝑥𝑖 (𝑡)) + 𝐵𝑖 𝑔 𝑥𝑖 (𝑡 − ℎ(𝑡)) + 𝑢𝑐𝑖 (𝑡),   𝑡 ≠ 𝑡𝑘 ,
                                              𝑝                                                                           (2)
          Δ𝑥𝑖 (𝑡𝑘 ) ∶= 𝑥𝑖 (𝑡+
                            𝑘
                              ) − 𝑥𝑖 (𝑡−
                                       𝑘 ) = 𝑢𝑖 (𝑡𝑘 ),                             𝑡 = 𝑡𝑘 ,

where 𝐶𝑖 , 𝐴𝑖 , 𝐵𝑖 ∈ ℝ𝑛×𝑛 may differ among the nodes. The terms 𝑢𝑐𝑖 (𝑡) and 𝑢𝑝𝑖 (𝑡𝑘 ) denote the continuous and impulsive
control inputs, respectively. The communication topology among the network nodes can switch and will be introduced
below.
Assumption 3.1. The time-varying delay ℎ is absolutely continuous and satisfies 0 ≤ ℎ(𝑡) ≤ ℎ,   ̄ ℎ(𝑡)
                                                                                                   ̇   ≤ 𝛿 < 1 a.e.
    The nonlinear functions 𝑓 and 𝑔 are globally Lipschitz continuous. Namely, there exist 𝑙𝑓 , 𝑙𝑔 > 0 such that, for any
𝑥, 𝑦 ∈ ℝ𝑛 ,

       ‖𝑓 (𝑥) − 𝑓 (𝑦)‖ ≤ 𝑙𝑓 ‖𝑥 − 𝑦‖,            ‖𝑔(𝑥) − 𝑔(𝑦)‖ ≤ 𝑙𝑔 ‖𝑥 − 𝑦‖.                                               (3)

3.3. Key Idea: Recovery Window
     Andy adopts the following hybrid control idea. The network error is sampled, and impulsive control is applied after
a prescribed execution delay. A recovery window whose length equals the upper bound on the time-varying state delay
is then introduced. During this window, the continuous controller temporarily cancels the delay channel in the error

Zi’an Wang                                                                                                      Page 7 of 20
                       Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

system. When the window ends, the pre-impulse history has left the active delay interval. The delayed error channel
is then reactivated, and the stability analysis resumes with the complete Lyapunov-Krasovskii functional.
     The continuous controller is designed as

      𝑢𝑐𝑖 (𝑡) = (𝐶𝑖 − 𝐶)𝑠(𝑡) + (𝐴 − 𝐴𝑖 )𝑓 (𝑠(𝑡)) + (𝐵 − 𝐵𝑖 )𝑔(𝑠(𝑡 − ℎ(𝑡)))
                     (             )               [                                ]
                 − 𝐾𝑖 𝑥𝑖 (𝑡) − 𝑠(𝑡) − (1 − 𝑞(𝑡))𝐵𝑖 𝑔(𝑥𝑖 (𝑡 − ℎ(𝑡))) − 𝑔(𝑠(𝑡 − ℎ(𝑡))) ,                                   (4)

where 𝐾𝑖 ∈ ℝ𝑛×𝑛 is the feedback gain. The phase indicator 𝑞(𝑡) ∈ {0, 1} is right-continuous, distinguishes the recovery
phase from the normal-flow phase, and is coordinated with the impulse instants. Specifically, (i) choose the initial
sampling instant 𝑠0 such that 𝑞(𝑠− 0
                                     ) = 1, and set 𝑞(𝑡) = 1 on the initial interval [𝑠0 , 𝑡0 ). (ii) Set 𝑞(𝑡𝑘 ) = 𝑞(𝑡+
                                                                                                                      𝑘
                                                                                                                        ) = 0
                                                                     ̄                               ̄
whenever 𝑡 = 𝑡𝑘 . (iii) Keep 𝑞 = 0 in the recovery window [𝑡𝑘 , 𝑡𝑘 + ℎ), and set 𝑞 = 1 on [𝑡𝑘 + ℎ, 𝑡𝑘+1 ). (iv) A topology
switch that does not coincide with an impulse does not reset 𝑞.
    We next introduce impulsive control with a switching communication topology. First, consider the switching
graphs. Let 𝑙 be a positive integer, and let 𝜎(𝑡) ∈  ∶= {1, … , 𝑙} be a left-continuous, piecewise constant switching
signal. In mode 𝑟 ∈ , the communication graph 𝑟 is a connected undirected graph. Its Laplacian matrix is denoted
by 𝐿𝑟 = (𝓁𝑖𝑗𝑟 )𝑁×𝑁 .
    Let 𝑎𝑟𝑖𝑗 denote the communication weight between nodes 𝑖 and 𝑗 in mode 𝑟. Then

            ⎧−𝑎𝑟 ,       𝑖 ≠ 𝑗,
            ⎪ 𝑖𝑗
      𝓁𝑖𝑗 = ⎨∑ 𝑎𝑟 ,
       𝑟
                         𝑖 = 𝑗.
            ⎪𝑚≠𝑖 𝑖𝑚
            ⎩

    Let 𝑁𝜎 (𝑡, 𝑢) denote the number of topology switches in the interval [𝑢, 𝑡), and assume that
                    𝑡−𝑢
      𝑁𝜎 (𝑡, 𝑢) ≤       + 𝑁0 ,       𝑡 ≥ 𝑢 ≥ 𝑠0 ,                                                                        (5)
                     𝑇𝑎

where 𝑇𝑎 > 0 is the average dwell time and 𝑁0 ≥ 0 is the chatter bound.

Assumption 3.2. The mode schedule satisfies

      𝜎(𝑡) = 𝑟𝑘 ∶= 𝜎(𝑠−
                      𝑘 ),
                                                ̄
                                  𝑠𝑘 ≤ 𝑡 ≤ 𝑡𝑘 + ℎ,      𝑘 ≥ 0.                                                           (6)

It also satisfies
         (          )
       𝜎 (𝑡𝑘 + ℎ)̄ + = 𝑟𝑘 ,       𝑘 ≥ 0.                                                                                 (7)

Thus, the topology mode remains 𝑟𝑘 from each sampling instant 𝑠𝑘 to the end of the corresponding recovery window.
Its right limit at the endpoint of the recovery window is also 𝑟𝑘 . In particular, no topology switching is allowed in
           ̄ including at 𝑡𝑘 . An immediate switch to the right of the endpoint of the recovery window is also excluded.
[𝑠𝑘 , 𝑡𝑘 + ℎ],
    Choose the pinning matrix 𝐷 = diag(𝑑1 , … , 𝑑𝑁 ), 𝑑𝑖 ≥ 0, where 𝑑𝑖 > 0 means that the 𝑖th follower has an additional
leader-pinning channel in the impulsive coupling. When 𝑑𝑖 = 0, the node receives the leader’s influence only indirectly
through its neighbors in the(impulsive topology.
                                        )        Given the impulse gain 𝜇𝑘 > 0, define the topology-dependent impulse
mapping matrix 𝑀𝑘 ∶= 𝜇𝑘 𝐿𝜎(𝑠− ) +𝐷 , where the active topology immediately before the sampling instant 𝑠𝑘 is used.
                                 𝑘
The mode-scheduling assumption in (6) and (7) avoids a mismatch between the sampling topology and the impulse
execution topology.

Remark 3.3. The impulsive control law selects the corresponding Laplacian matrix according to the active commu-
nication topology at the sampling instant. It is therefore a topology-dependent switching impulsive controller. This
design can describe practical situations such as changes in adjacency relations caused by moving nodes, failures and
recovery of communication links, and time-sharing schedules for wireless channels. The controller can then implement
impulsive corrections according to the communication relations available at the sampling instant.



Zi’an Wang                                                                                                     Page 8 of 20
                         Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

     Define the synchronization errors by 𝑒𝑖 (𝑡) ∶= 𝑥𝑖 (𝑡) − 𝑠(𝑡), 𝑒(𝑡) ∶= col(𝑒1 (𝑡), … , 𝑒𝑁 (𝑡)).
     Assume that the leader and follower state histories are continuous on [𝑠0 − ℎ,    ̄ 𝑠0 ]. Define the initial error segment
by
       𝑒𝑠0 (𝜃) ∶= 𝑒(𝑠0 + 𝜃),              ̄ 0],
                                    𝜃 ∈ [−ℎ,
             ̄ 0], ℝ𝑁𝑛 ), where  denotes the space of continuous functions. Define its norm by
so 𝑒𝑠0 ∈ ([−ℎ,
       ‖𝑒𝑠0 ‖ℎ̄ ∶= sup ‖𝑒(𝑠0 + 𝜃)‖.
                     ̄
                    −ℎ≤𝜃≤0

    Let [𝑧]𝑖 denote the 𝑖th 𝑛-dimensional block of the stacked vector 𝑧 ∈ ℝ𝑁𝑛 . Since the leader state 𝑠(𝑡) is continuous
at the impulse execution instants, the impulsive control input is designed as
                    [                 ]
       𝑢𝑝𝑖 (𝑡𝑘 ) ∶= (𝑀𝑘 ⊗ 𝐼𝑛 )𝑒(𝑠−              −
                                   𝑘 ) 𝑖 − 𝑒𝑖 (𝑡𝑘 )                                                                   (8)
                                  [𝑁                                            ]
                                   ∑ 𝜎(𝑠− ) (                     )
                 = −𝑒𝑖 (𝑡−
                         𝑘 ) + 𝜇𝑘     𝑎𝑖𝑗 𝑘 𝑒𝑖 (𝑠−             −             −
                                                    𝑘 ) − 𝑒𝑗 (𝑠𝑘 ) + 𝑑𝑖 𝑒𝑖 (𝑠𝑘 ) .
                                  𝑗=1

     Since 𝑥𝑖 (𝑡𝑘 ) = 𝑥𝑖 (𝑡−
                           𝑘
                             ) + 𝑢𝑝𝑖 (𝑡𝑘 ), the stacked error after impulse execution is
       𝑒(𝑡𝑘 ) = (𝑀𝑘 ⊗ 𝐼𝑛 )𝑒(𝑠−
                             𝑘 ).                                                                                          (9)
     Substituting (4) into the leader and follower systems in (1) and (2) gives the unified closed-loop error system
       {
           𝑒̇ 𝑖 (𝑡) = −(𝐶𝑖 + 𝐾𝑖 )𝑒𝑖 (𝑡) + 𝐴𝑖 Δ𝑓𝑖 (𝑡) + 𝑞(𝑡)𝐵𝑖 Δ𝑔𝑖 (𝑡 − ℎ(𝑡)), 𝑡 ≠ 𝑡𝑘 ,
                      [                  ]                                                                           (10)
          𝑒𝑖 (𝑡𝑘 ) = (𝑀𝑘 ⊗ 𝐼𝑛 )𝑒(𝑠−   𝑘) 𝑖 ,                                  𝑡 = 𝑡𝑘 ,

where Δ𝑓𝑖 (𝑡) ∶= 𝑓 (𝑥𝑖 (𝑡)) − 𝑓 (𝑠(𝑡)), Δ𝑔𝑖 (𝑡 − ℎ(𝑡)) ∶= 𝑔(𝑥𝑖 (𝑡 − ℎ(𝑡))) − 𝑔(𝑠(𝑡 − ℎ(𝑡))).
     It follows from (10) that the delay channel in the error system is exactly canceled when 𝑞(𝑡) = 0. This delay channel
is reactivated when 𝑞(𝑡) = 1. Furthermore, suppose that the error is identically zero at a given instant and throughout
the required delay-history interval. Then Δ𝑓𝑖 (𝑡) = 0 and Δ𝑔𝑖 (𝑡 − ℎ(𝑡)) = 0, so the continuous flow satisfies 𝑒̇ 𝑖 (𝑡) = 0. If
𝑒(𝑠−𝑘
      ) = 0, the impulse mapping gives 𝑒(𝑡𝑘 ) = (𝑀𝑘 ⊗ 𝐼𝑛 )𝑒(𝑠−    𝑘
                                                                    ) = 0. Therefore, the continuous flow and the impulsive
jumps both preserve the zero-error state. Once the system reaches synchronization, it remains synchronized.
     We next introduce self-triggered impulsive control. Let the triggering parameters be 𝜆̄ ≥ 0 and 𝜌 > 0, and the
parameter sequence be {𝑎𝑘 }𝑘≥0 , where 𝑎𝑘 > 0. Assume additionally that 𝜏 ≥ ℎ.      ̄
     The selected triggering parameter 𝜆̄ will be further constrained in the theorem below by the Lyapunov matrices
and their related constants.
                                                           ̄
     At the computed sampling instant 𝑠𝑘 , set 𝑊𝑘2 ∶= 𝑒𝜆𝜏 and define the self-triggering function for a candidate instant
𝑡 ≥ 𝑡𝑘 as
       Ψ𝑘 (𝑡) ∶= (𝜆̄ + 𝜌)(𝑡 − 𝑡𝑘 ) − 𝑎𝑘 − ln 𝑊𝑘2 .                                                                        (11)

     Since 𝜆̄ + 𝜌 > 0, the function Ψ𝑘 (𝑡) is strictly increasing in 𝑡. Therefore, the next sampling instant is defined as the
first instant at which Ψ𝑘 (𝑡) reaches a nonnegative value. Namely,
                    {                    }
        𝑠𝑘+1 ∶= inf 𝑡 > 𝑡𝑘 ∶ Ψ𝑘 (𝑡) ≥ 0 .                                                                                (12)
     Define the time length from the 𝑘th actual impulse execution instant 𝑡𝑘 to the next sampling instant 𝑠𝑘+1 by
                         𝑎𝑘 + ln 𝑊𝑘2  𝑎 + 𝜆𝜏̄
       Φ𝑘 ∶= 𝑠𝑘+1 − 𝑡𝑘 =             = 𝑘      .                                                                           (13)
                            𝜆̄ + 𝜌     𝜆̄ + 𝜌
    Hence, 𝑠𝑘+1 = 𝑡𝑘 + Φ𝑘 = 𝑠𝑘 + 𝜏 + Φ𝑘 ,
    Therefore, the sampling sequence and the impulse execution sequence are interlaced as 𝑠0 < 𝑡0 < 𝑠1 < 𝑡1 < ⋯ ,
and 𝑡𝑘+1 − 𝑡𝑘 = 𝑠𝑘+1 − 𝑠𝑘 = 𝜏 + Φ𝑘 > 0.
    Both the sampling intervals and the impulse execution intervals have the uniform strict positive lower bound 𝜏.
Thus, any finite time interval contains only finitely many sampling instants and impulse execution instants. Therefore,
neither the self-triggered sampling sequence nor the impulse execution sequence exhibits Zeno behavior.

Zi’an Wang                                                                                                       Page 9 of 20
                          Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

Remark 3.4. The recovery-window feedback in (4) reveals a useful control-design idea. It matches a controller term
with a difficult term in the error dynamics and removes that term during the part of the hybrid evolution in which it is
most troublesome.
    Andy’s construction complements standard delay-analysis methods with a structural heuristic. It first identifies the
term that makes the Lyapunov derivative difficult. The controller and the Lyapunov function are then co-designed so
that this term is canceled or absorbed in a controlled phase. This principle also appears in PD-controlled multi-weighted
networks. A derivative feedback term can be matched with a coupling-weighted quadratic term in the Lyapunov
function so that the corresponding cross-derivative terms cancel pairwise [12, 13]. In PI designs, related weight terms
can be balanced in an augmented Lyapunov functional [12].
    A broader version of this idea appears in recursive adaptive control. Coordinate changes, parameter-update laws,
and the feedback law are constructed step by step, and stability is established through a Lyapunov argument [14]. A
related learning-based approach jointly trains a nonlinear controller and a neural Lyapunov function. An SMT-based
falsification step checks the Lyapunov conditions and returns counterexamples when they fail [15].
    These connections suggest that Andy’s control design can inform the construction of Lyapunov functions and
PID-type controllers for systems with several coupling weights, delayed channels, or derivative couplings.
    Exact delay-channel cancellation in (4) is demanding in practice because it requires accurate knowledge of
the delayed model and online access to the complete delayed states. Mature delay-system methods can retain the
delayed channel and estimate its effect through Lyapunov-Krasovskii functionals, comparison arguments, and delayed
impulsive inequalities [1, 16, 17]. When exact delayed states are unavailable, a natural extension is to use observer-
based or adaptive approximate cancellation and bound the residual mismatch with standard delay-analysis tools.

3.4. Main Theorem
   For any candidate symmetric positive definite matrices 𝑃𝑟 , 𝑆𝑟 , 𝑅𝑟 ∈ ℝ𝑛×𝑛 , constants 𝜆1,𝑟 ≥ 0, and scalars 𝜀𝑖,𝑟 > 0
appearing in condition (i) below, where 𝑟 ∈  and 𝑖 = 1, … , 𝑁, define

         𝑄𝑖,𝑟 ∶= 𝑃𝑟 (𝐶𝑖 + 𝐾𝑖 ) + (𝐶𝑖 + 𝐾𝑖 )𝖳 𝑃𝑟 ,
      Λ(11)
       𝑖,𝑟 ∶= − 𝑄𝑖,𝑟 + 2‖𝑃𝑟 𝐴𝑖 ‖𝑙𝑓 𝐼𝑛 + 𝜀𝑖,𝑟 𝐼𝑛 + 𝜆max (𝑆𝑟 )𝐼𝑛 + ℎ𝜆max (𝑅𝑟 )𝐼𝑛 ,
                                                                 ̄

      Λ(22)    −1          2 2
       𝑖,𝑟 ∶= 𝜀𝑖,𝑟 ‖𝑃𝑟 𝐵𝑖 ‖ 𝑙𝑔 𝐼𝑛 − (1 − 𝛿)𝜆min (𝑆𝑟 )𝐼𝑛 .

   Further define
                  {                           }                     max{0, 𝛽𝑟(0) }
      𝛽𝑟(0) ∶= max −𝜆min (𝑄𝑖,𝑟 ) + 2‖𝑃𝑟 𝐴𝑖 ‖𝑙𝑓 ,            𝛽𝑟 ∶=                  ,
                1≤𝑖≤𝑁                                                𝜆min (𝑃𝑟 )
                  {                          }                     max{0, 𝛾𝑟(0) }
      𝛾𝑟(0) ∶= max 𝜆max (𝑄𝑖,𝑟 ) + 2‖𝑃𝑟 𝐴𝑖 ‖𝑙𝑓 ,         𝛾𝑟 ∶=                     .
                1≤𝑖≤𝑁                                               𝜆min (𝑃𝑟 )
   Let
                                               2
                         ⎛    ̄ max (𝑆𝑟 ) + ℎ̄ 𝜆max (𝑅𝑟 ) ⎞
                              ℎ𝜆
                   (𝛽𝑟 +𝛾𝑟 )ℎ̄ ⎜              2           ⎟,
         𝜒̃𝑟 ∶= 𝑒         1+
                         ⎜            𝜆min (𝑃𝑟 )          ⎟
                         ⎝                                ⎠
      𝜒̃max ∶= max 𝜒̃𝑟 ,     𝛽+ ∶= max 𝛽𝑟 ,       ̄
                                                  𝜆1 ∶= max 𝜆1,𝑟 .
                  𝑟∈                   𝑟∈                  𝑟∈

    For a candidate sequence {𝜂𝑘 }𝑘≥0 ⊂ (0, 1) appearing in condition (ii) below, define the effective contraction over
the 𝑘th impulsive period by

      𝑐̃𝑘 ∶= − ln 𝜂𝑘 − 𝛽+ ℎ̄ − ln 𝜒̃max .                                                                           (14)

   For any 𝛼 > 0, define 𝛼ef f ∶= 𝛼 + 𝜆̄ − 𝜆̄ 1 .
Theorem 3.5. Consider the systems in (1) and (2) under the continuous controller (4), the impulsive controller (8),
and the self-triggering mechanism defined by (11) through (13). Assumption 3.1, the average dwell-time constraint (5),
                                     ̄ and the mode-scheduling assumption in (6) and (7) are imposed throughout.
the execution-delay requirement 𝜏 ≥ ℎ,
If the following conditions hold:

Zi’an Wang                                                                                                 Page 10 of 20
                            Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

    (i) For each switching mode 𝑟 ∈ , there exist symmetric positive definite matrices 𝑃𝑟 , 𝑆𝑟 , 𝑅𝑟 ∈ ℝ𝑛×𝑛 , and a
        constant 𝜆1,𝑟 ≥ 0 that is valid for all nodes. For every 𝑖 = 1, … , 𝑁, there exists 𝜀𝑖,𝑟 > 0 such that
                [                     ]         [           ]
                 Λ(11)
                  𝑖,𝑟           0                𝑃        0
                                          ⪯ 𝜆1,𝑟 𝑟            ,                                                                      (15)
                  0           Λ(22)
                               𝑖,𝑟
                                                  0       0

        In addition, 𝜆̄ ≥ max{𝜆̄ 1 , 𝛽+ }.
   (ii) There exists a sequence {𝜂𝑘 }𝑘≥0 ⊂ (0, 1) such that, for every 𝑘 ≥ 0, the impulsive map satisfies

                𝑀𝑘𝖳 𝑀𝑘 ⪯ 𝜂𝑘 𝐼𝑁 .                                                                                                     (16)

        In addition, there exists a constant 𝜇 ≥ 1 such that, for all 𝑟, 𝑗 ∈ ,

                𝑃𝑟 ⪯ 𝜇𝑃𝑗 ,             𝑆𝑟 ⪯ 𝜇𝑆𝑗 ,             𝑅𝑟 ⪯ 𝜇𝑅𝑗 .                                                             (17)

  (iii) The self-triggering parameters satisfy
                      ̄
                𝑎𝑘 > 𝜌ℎ,              𝑘 ≥ 0.                                                                                         (18)

        There exist constants 𝛼 > 0 and 𝜑 > 0 such that, for all 𝑡 ≥ 𝑢 ≥ 𝑠0 ,
                                           ∑ [                   ]
                ̄ − 𝑢) + ln 𝜇 (𝑡 − 𝑢) +
                𝜆(𝑡                                𝑐𝑘 + (𝜆̄ + 𝜌)𝜏 ≤ −𝛼(𝑡 − 𝑢) + 𝜑.
                                                  −̃
                          𝑇𝑎                                                                                                         (19)
                                        𝑘∶ 𝑢≤𝑡 <𝑡         𝑘


    Then 𝛼ef f ≥ 𝛼 > 0, and the closed-loop system achieves global exponential leader-follower synchronization.
Specifically, there exists a constant 𝐶GE ≥ 1, independent of the initial history, such that every admissible initial
history satisfies
                                       𝛼ef f
      ‖𝑒(𝑡)‖ ≤ 𝐶GE ‖𝑒𝑠0 ‖ℎ̄ 𝑒− 2 (𝑡−𝑠0 ) ,                𝑡 ≥ 𝑠0 ,                                                                   (20)

Proof. The stated regularity and non-Zeno timing assumptions ensure that the closed-loop system admits a unique
global right-continuous solution. It remains to establish the exponential estimate.
   Fix matrices 𝑃𝑟 , 𝑆𝑟 , 𝑅𝑟 and constants 𝜆1,𝑟 , 𝜀𝑖,𝑟 satisfying condition (i). In each recovery window, construct the
quadratic Lyapunov function

      𝑟0 (𝑡) ∶= 𝑒𝖳 (𝑡)(𝐼𝑁 ⊗ 𝑃𝑟 )𝑒(𝑡),                                                                                               (21)

    In each normal phase, construct the Lyapunov-Krasovskii functional
                                                      𝑡                                     0    𝑡
      𝑟1 (𝑡) ∶= 𝑒𝖳 (𝑡)(𝐼𝑁 ⊗ 𝑃𝑟 )𝑒(𝑡) +                       𝑒𝖳 (𝑣)(𝐼𝑁 ⊗ 𝑆𝑟 )𝑒(𝑣) d𝑣 +               𝑒𝖳 (𝑣)(𝐼𝑁 ⊗ 𝑅𝑟 )𝑒(𝑣) d𝑣 d𝜃.    (22)
                                                ∫𝑡−ℎ(𝑡)                                   ∫−ℎ̄ ∫𝑡+𝜃

    In the following, write V (𝑡) = 𝜎(𝑡)0 (𝑡) when 𝑞(𝑡) = 0, and write V (𝑡) =  1 (𝑡) when 𝑞(𝑡) = 1. The initialization of
                                                                                        𝜎(𝑡)
𝑞 gives 𝑞 = 1 at 𝑠−   and throughout    [𝑠 0 , 𝑡0 ). For 𝑘 ≥ 1, the conditions 𝜏 ≥  ̄ and (18) imply that 𝑞 = 1 at each sampling
                                                                                    ℎ
                    0
instant 𝑠𝑘 and each pre-impulse instant 𝑡−       𝑘
                                                   . Thus, V is the full functional at these instants.
    First, consider the continuous flow in a recovery window. When 𝑞 = 0 and the mode is fixed, (10) has no delay
term. Its error trajectory is absolutely continuous. Hence, 𝑟0 is also absolutely continuous. It follows from (21), the
definition of 𝑄𝑖,𝑟 , and (3) that, for almost every 𝑡,

                    ∑
                    𝑁
                      [                                ]        ∑
                                                                𝑁
      ̇ 𝑟0 (𝑡) =         −𝑒𝖳𝑖 𝑄𝑖,𝑟 𝑒𝑖 + 2𝑒𝖳𝑖 𝑃𝑟 𝐴𝑖 Δ𝑓𝑖 ≤ 𝛽𝑟(0)   ‖𝑒𝑖 ‖2 ≤ 𝛽𝑟 𝑟0 (𝑡).                                               (23)
                    𝑖=1                                               𝑖=1



Zi’an Wang                                                                                                                   Page 11 of 20
                            Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

   Similarly,

                           ∑
                           𝑁
      ̇ 𝑟0 (𝑡) ≥ −𝛾𝑟(0)         ‖𝑒𝑖 ‖2 ≥ −𝛾𝑟 𝑟0 (𝑡).                                                                 (24)
                           𝑖=1

    Therefore, in the almost-everywhere sense, −𝛾𝑟 𝑟0 (𝑡) ≤ ̇ 𝑟0 (𝑡) ≤ 𝛽𝑟 𝑟0 (𝑡). Apply the standard Gronwall inequality
to these two differential inequalities. In a recovery window with a fixed mode, for any 𝑡𝑘 ≤ 𝑢 ≤ 𝑣 ≤ 𝑡𝑘 + ℎ,  ̄ this gives

      𝑟0 (𝑣) ≤ 𝑒𝛽𝑟 (𝑣−𝑢) 𝑟0 (𝑢),               𝑟0 (𝑢) ≤ 𝑒𝛾𝑟 (𝑣−𝑢) 𝑟0 (𝑣).                                          (25)

    Next, consider the continuous flow in a normal phase. Let 𝑒𝑖,ℎ ∶= 𝑒𝑖 (𝑡 − ℎ(𝑡)). When 𝑞 = 1, take the Dini derivative
of the quadratic term in (22) along (10). We obtain

        [                    ] ∑𝑁
                                  [ 𝖳                                                      ]
      𝐷+ 𝑒𝖳 (𝑡)(𝐼𝑁 ⊗ 𝑃𝑟 )𝑒(𝑡) =    −𝑒𝑖 𝑄𝑖,𝑟 𝑒𝑖 + 2𝑒𝖳𝑖 𝑃𝑟 𝐴𝑖 Δ𝑓𝑖 + 2𝑒𝖳𝑖 𝑃𝑟 𝐵𝑖 Δ𝑔𝑖 (𝑡 − ℎ(𝑡)) .
                                                 𝑖=1

   The Lipschitz conditions and Young’s inequality give, respectively,

      2𝑒𝖳𝑖 𝑃𝑟 𝐴𝑖 Δ𝑓𝑖 ≤ 2‖𝑃𝑟 𝐴𝑖 ‖𝑙𝑓 ‖𝑒𝑖 ‖2 ,
      2𝑒𝖳𝑖 𝑃𝑟 𝐵𝑖 Δ𝑔𝑖 (𝑡 − ℎ(𝑡)) ≤ 𝜀𝑖,𝑟 ‖𝑒𝑖 ‖2 + 𝜀−1          2 2        2
                                                 𝑖,𝑟 ‖𝑃𝑟 𝐵𝑖 ‖ 𝑙𝑔 ‖𝑒𝑖,ℎ ‖ .

                                                             ̇
   Apply the Leibniz rule to the single-integral term. Using ℎ(𝑡) ≤ 𝛿, we obtain
           [                                 ]
                 𝑡                                         ∑
                                                           𝑁                            ∑
                                                                                        𝑁
      𝐷+              𝑒𝖳 (𝑣)(𝐼𝑁 ⊗ 𝑆𝑟 )𝑒(𝑣) d𝑣 ≤ 𝜆max (𝑆𝑟 )   ‖𝑒𝑖 ‖2 − (1 − 𝛿)𝜆min (𝑆𝑟 )   ‖𝑒𝑖,ℎ ‖2 .
            ∫𝑡−ℎ(𝑡)
                                                                          𝑖=1           𝑖=1

   The Dini derivative of the double-integral term satisfies
        [                                      ]
                 0    𝑡
      𝐷+                   𝑒𝖳 (𝑣)(𝐼𝑁 ⊗ 𝑅𝑟 )𝑒(𝑣) d𝑣 d𝜃
               ∫−ℎ̄ ∫𝑡+𝜃
                                                       𝑡
          = ℎ̄ 𝑒𝖳 (𝑡)(𝐼𝑁 ⊗ 𝑅𝑟 )𝑒(𝑡) −                      𝑒𝖳 (𝑣)(𝐼𝑁 ⊗ 𝑅𝑟 )𝑒(𝑣) d𝑣
                                                   ∫𝑡−ℎ̄
                                ∑
                                𝑁
            ̄ max (𝑅𝑟 )
          ≤ ℎ𝜆                        ‖𝑒𝑖 ‖2 .
                                𝑖=1

   Combining the above estimates gives the following bound for the Dini derivative of the full functional:

                      ∑
                      𝑁
                        [                               ]
      𝐷+ 𝑟1 (𝑡) ≤          𝑒𝖳𝑖 Λ(11)      𝖳    (22)
                                 𝑖,𝑟 𝑒𝑖 + 𝑒𝑖,ℎ Λ𝑖,𝑟 𝑒𝑖,ℎ .
                                                                                                                       (26)
                      𝑖=1

   By (15),

      𝐷+ 𝑟1 (𝑡) ≤ 𝜆1,𝑟 𝑒𝖳 (𝑡)(𝐼𝑁 ⊗ 𝑃𝑟 )𝑒(𝑡) ≤ 𝜆1,𝑟 𝑟1 (𝑡).                                                           (27)

    Suppose that a switch from mode 𝑟 to mode 𝑗 occurs during a normal phase. Applying (17) term by term to (22)
gives

      𝑗1 (𝑡+ ) ≤ 𝜇𝑟1 (𝑡− ).                                                                                          (28)

    We next estimate the functional transition at the end of a recovery window. Let 𝑡⋆      ∶= 𝑡𝑘 + ℎ.̄ Since ℎ(𝑡⋆ ) ≤ ℎ,
                                                                                                                       ̄ all
                                                                                         𝑘                         𝑘
                             ⋆                                    ⋆
history involved in (22) at 𝑡𝑘 lies in the recovery window [𝑡𝑘 , 𝑡𝑘 ]. By (25), every 𝑣 in this interval satisfies
                            ̄
      𝑟0 (𝑣) ≤ 𝑒(𝛽𝑟 +𝛾𝑟 )ℎ 𝑟0 (𝑡⋆
                                  𝑘 −).                                                                                (29)

Zi’an Wang                                                                                                   Page 12 of 20
                                 Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

   Moreover, ‖𝑒(𝑣)‖2 ≤ 𝑟0 (𝑣)∕𝜆min (𝑃𝑟 ). Hence,
              𝑡⋆                                                  ̄
               𝑘                                              ̄ ℎ𝜆max (𝑆𝑟 )
                          𝑒𝖳 (𝑣)(𝐼𝑁 ⊗ 𝑆𝑟 )𝑒(𝑣) d𝑣 ≤ 𝑒(𝛽𝑟 +𝛾𝑟 )ℎ                  𝑟0 (𝑡⋆
                                                                                       𝑘 −),
      ∫𝑡⋆ −ℎ(𝑡⋆ )                                                 𝜆min (𝑃𝑟 )
          𝑘         𝑘
              0      𝑡⋆                                                     ̄2
                      𝑘                                                   ̄ ℎ 𝜆max (𝑅𝑟 )
                           𝑒𝖳 (𝑣)(𝐼𝑁 ⊗ 𝑅𝑟 )𝑒(𝑣) d𝑣 d𝜃 ≤ 𝑒(𝛽𝑟 +𝛾𝑟 )ℎ                        𝑟0 (𝑡⋆
                                                                                                 𝑘 −).
      ∫−ℎ̄ ∫𝑡⋆ +𝜃                                                           2𝜆min (𝑃𝑟 )
                    𝑘

   Therefore, the definition of 𝜒̃𝑟 and (7) yield

      𝑟1 ((𝑡⋆ +
                    ̃𝑟 𝑟0 (𝑡⋆
             𝑘) ) ≤ 𝜒        𝑘 −).                                                                                       (30)

    By (6) and (7), the mode 𝑟𝑘 = 𝜎(𝑠−    ) = 𝜎(𝑡−                                   ̄ Using (9), (16), and the dominance
                                                   ) remains unchanged on [𝑠𝑘 , 𝑡𝑘 + ℎ].
                                        𝑘        𝑘
of the full functional over its current-state quadratic term, we have

      𝑟0 (𝑡+
            𝑘
              ) = 𝑒𝖳 (𝑠−    𝖳              −         𝖳 −                 −         1 −
                       𝑘 )(𝑀𝑘 𝑀𝑘 ⊗ 𝑃𝑟𝑘 )𝑒(𝑠𝑘 ) ≤ 𝜂𝑘 𝑒 (𝑠𝑘 )(𝐼𝑁 ⊗ 𝑃𝑟𝑘 )𝑒(𝑠𝑘 ) ≤ 𝜂𝑘 𝑟 (𝑠𝑘 ).                              (31)
          𝑘                                                                                              𝑘

   Successive application of (23), (30), and (14) gives
                                             ̄
                 ̄ + ) ≤ 𝜒̃max 𝑒𝛽+ ℎ 𝜂𝑘  1 (𝑠− ) = 𝑒−̃𝑐𝑘  1 (𝑠− ).
      𝑟1 ((𝑡𝑘 + ℎ)                      𝑟    𝑘            𝑟    𝑘                                                        (32)
          𝑘                                            𝑘              𝑘

                ̄ and (13),
   By (18), 𝜏 ≥ ℎ,

                           𝑎𝑘 − 𝜌ℎ̄ + 𝜆(𝜏
                                       ̄ − ℎ)
                                           ̄
      Φ𝑘 − ℎ̄ =                               > 0.                                                                       (33)
                                  𝜆̄ + 𝜌
               ̄ 𝑠𝑘+1 ) is a nondegenerate normal phase. Let 𝑁 sw denote the number of switches in this interval.
  Thus, [𝑡𝑘 + ℎ,                                              𝑘
Combining (27), (28), and (32), we obtain
                             ̄      ̄            sw
      V (𝑠−
          𝑘+1
              ) ≤ 𝑒𝜆1 (Φ𝑘 −ℎ)−̃𝑐𝑘 𝜇 𝑁𝑘 V (𝑠−
                                           𝑘 ).                                                                          (34)

    Condition (6) excludes mode switches in all other intervals of the current cycle. Thus, 𝑁𝑘sw is also the total number
                                                 ∑                           ∑𝑘−1 sw 𝑠𝑘 −𝑠0
of switches in [𝑠𝑘 , 𝑠𝑘+1 ). Iterate (34) and use 𝑘−1
                                                   𝑖=0 Φ𝑖 = (𝑠𝑘 − 𝑠0 ) − 𝑘𝜏,  𝑖=0 𝑁𝑖 ≤ 𝑇       + 𝑁0 , to obtain
                                                                                                             𝑎


                                    [                        ∑
                                                          ] 𝑘−1        ln 𝜇
      ln V (𝑠− ) ≤ ln V (𝑠 −
                             ) + ̄ 1 (𝑠𝑘 − 𝑠0 ) − 𝑘𝜏 − 𝑘ℎ̄ −
                                 𝜆                               𝑐̃𝑖 +      (𝑠 − 𝑠0 ) + 𝑁0 ln 𝜇.                         (35)
             𝑘             0
                                                             𝑖=0
                                                                        𝑇𝑎 𝑘

   Set 𝑢 = 𝑠0 and 𝑡 = 𝑠𝑘 in (19). Then

          ∑
          𝑘−1
                           ln 𝜇
      −            𝑐̃𝑖 +                          ̄ 𝑘 − 𝑠0 ) − 𝑘(𝜆̄ + 𝜌)𝜏 + 𝜑.
                                (𝑠 − 𝑠0 ) ≤ −(𝛼 + 𝜆)(𝑠                                                                   (36)
          𝑖=0
                            𝑇𝑎 𝑘

   Substitute (36) into (35) and discard the nonpositive terms involving 𝑘. Let 𝜑ef f ∶= 𝜑 + 𝑁0 ln 𝜇. We obtain

      V (𝑠−
          𝑘) ≤ 𝑒
                𝜑ef f
                      V (𝑠−
                          0
                            )𝑒−𝛼ef f (𝑠𝑘 −𝑠0 ) .                                                                         (37)

   We next estimate a uniform upper bound for the triggering intervals. Fix 𝑘 and take 0 < 𝜀 < Φ𝑘 . Set 𝑢 = 𝑡𝑘 + 𝜀
and 𝑡 = 𝑠𝑘+1 in (19). The interval [𝑡𝑘 + 𝜀, 𝑠𝑘+1 ) contains no impulse and has length Φ𝑘 − 𝜀. Hence,
      (               )
             ̄   ln 𝜇
        𝛼+𝜆+            (Φ𝑘 − 𝜀) ≤ 𝜑.
                  𝑇𝑎
   Letting 𝜀 ↓ 0 gives
                                              𝜑
      0 < Φ𝑘 ≤ Φmax ∶=                                < ∞.                                                               (38)
                                        𝛼 + 𝜆̄ + ln 𝜇 𝑇𝑎

Zi’an Wang                                                                                                       Page 13 of 20
                                Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

   Thus, Φ𝑘 has the uniform upper bound required for the estimate over the entire time domain.
   We now extend the estimate at the sampling instants to all times. If 𝑡 ∈ [𝑠𝑘 , 𝑡𝑘 ), then (27) and (6) give
                    ̄
        V (𝑡) ≤ 𝑒𝜆𝜏 V (𝑠−
                        𝑘 ).

                     ̄ then (23) and (31) give
   If 𝑡 ∈ [𝑡𝑘 , 𝑡𝑘 + ℎ),
                        ̄                ̄̄
        V (𝑡) ≤ 𝑒𝛽+ ℎ V (𝑠−
                          𝑘 ) ≤ 𝑒 V (𝑠𝑘 ).
                                 𝜆ℎ   −


                ̄ 𝑠𝑘+1 ), then (30), (27), (28), (5), and (38) give
   If 𝑡 ∈ [𝑡𝑘 + ℎ,
                                ̄   ̄
        V (𝑡) ≤ 𝜒̃max 𝑒𝛽+ ℎ+𝜆1 Φmax 𝜇𝑁0 +Φmax ∕𝑇𝑎 V (𝑠−
                                                      𝑘 ).

   Therefore, for every 𝑡 ∈ [𝑠𝑘 , 𝑠𝑘+1 ),

        V (𝑡) ≤ 𝐶cyc V (𝑠−
                         𝑘 ),                                                                                          (39)

where
                   { ̄ ̄̄                 ̄ ̄                    }
        𝐶cyc ∶= max 𝑒𝜆𝜏 , 𝑒𝜆ℎ , 𝜒̃max 𝑒𝛽+ ℎ+𝜆1 Φmax 𝜇𝑁0 +Φmax ∕𝑇𝑎 .                                                    (40)

   Moreover, 𝑡 − 𝑠𝑘 < 𝜏 + Φmax . It follows from (37) and (39) that

        V (𝑡) ≤ 𝐶cyc 𝑒𝜑ef f +𝛼ef f (𝜏+Φmax ) V (𝑠−
                                                 0
                                                   )𝑒−𝛼ef f (𝑡−𝑠0 ) .                                                  (41)

   Define

          𝑝 ∶= min 𝜆min (𝑃𝑟 ),
                 𝑟∈
                                                   ℎ̄ 2
        𝐶ℎ ∶= max 𝜆max (𝑃𝑟 ) + ℎ̄ max 𝜆max (𝑆𝑟 ) +      max 𝜆 (𝑅 ).
              𝑟∈                 𝑟∈                2 𝑟∈ max 𝑟
   By (21) and (22),

        V (𝑡) ≥ 𝑝‖𝑒(𝑡)‖2 ,              V (𝑠−
                                            0
                                              ) ≤ 𝐶ℎ ‖𝑒𝑠0 ‖2ℎ̄ .                                                       (42)

   Substituting (42) into (41) gives (20), where we can take
                   (                )1∕2      [                          ]
                        𝐶cyc 𝐶ℎ                𝜑ef f + 𝛼ef f (𝜏 + Φmax )
        𝐶GE ∶=                             exp                             .                                           (43)
                            𝑝                               2

    Since 𝑒𝑖 (𝑡) = 𝑥𝑖 (𝑡) − 𝑠(𝑡), (20) shows that every follower error 𝑒𝑖 (𝑡) converges to zero at an exponential rate of at
least 𝛼ef f ∕2. Therefore, the closed-loop system achieves global exponential leader-follower synchronization.

Remark 3.6. When 𝛾𝑟(0) ≤ 0 holds for every mode, 𝛾𝑟 = 0. The phase-transition factor 𝜒̃𝑟 then automatically reduces
to its original form without the bidirectional growth compensation. This reduction leaves all other conditions of the
theorem and the proof structure unchanged.

3.5. Numerical Verification
Example 3.1. Consider one three-dimensional leader and five three-dimensional heterogeneous followers. The
nonlinear functions are applied componentwise and are chosen as 𝑓 (𝑧) = 𝑔(𝑧) = tanh(𝑧), 𝑙𝑓 = 𝑙𝑔 = 1. The matrices
of the leader system are 𝐶 = diag(0.45, 0.50, 0.55), 𝐵 = diag(0.12, 0.10, 0.09), and

            ⎡ 1.05          −0.25        0.15 ⎤
        𝐴 = ⎢ 0.20          0.95         −0.20⎥ .
            ⎢                                 ⎥
            ⎣−0.15          0.25         1.00 ⎦

Zi’an Wang                                                                                                   Page 14 of 20
                       Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

    The follower matrices are diagonal and are chosen as
      𝐶1 = diag(0.30, 0.36, 0.42),            𝐴1 = diag(1.20, 0.95, 1.05),             𝐵1 = diag(0.15, 0.10, 0.12),
      𝐶2 = diag(0.34, 0.31, 0.46),            𝐴2 = diag(1.10, 1.18, 0.92),             𝐵2 = diag(0.11, 0.14, 0.09),
      𝐶3 = diag(0.38, 0.44, 0.32),            𝐴3 = diag(0.98, 1.08, 1.15),             𝐵3 = diag(0.13, 0.08, 0.15),
      𝐶4 = diag(0.33, 0.48, 0.37),            𝐴4 = diag(1.16, 1.02, 1.10),             𝐵4 = diag(0.10, 0.12, 0.14),
      𝐶5 = diag(0.41, 0.35, 0.50),            𝐴5 = diag(1.05, 1.12, 1.19),             𝐵5 = diag(0.14, 0.15, 0.11).
    The continuous feedback gains are 𝐾𝑖 = 1.20𝐼3 for 𝑖 = 1, … , 5.
    The time-varying delay is ℎ(𝑡) = 0.075 + 0.025 sin(0.8𝑡), so 0.05 ≤ ℎ(𝑡) ≤ ℎ̄ = 0.10 and max𝑡 ℎ(𝑡)̇  = 0.02 < 𝛿 =
0.05 < 1. The two switching topologies are a five-node ring and a star centered at follower 3. Their Laplacian matrices
are
           ⎡2       −1 0  0          −1⎤             ⎡1       0    −1 0        0⎤
           ⎢−1       2 −1 0           0⎥             ⎢0       1    −1 0        0⎥
      𝐿1 = ⎢ 0      −1 2 −1          0 ⎥,       𝐿2 = ⎢−1      −1    4 −1       −1⎥ .
           ⎢                           ⎥             ⎢                           ⎥
           ⎢0       0 −1 2           −1⎥             ⎢0       0    −1 1        0⎥
           ⎣−1       0  0 −1          2⎦             ⎣0       0    −1 0        1⎦
   Only follower 1 has a direct pinning channel, and hence 𝐷 = diag(1, 0, 0, 0, 0).
   For the impulsive controller, choose 𝜇𝑘 = 0.05, 𝜂𝑘 = 0.07, 𝜏 = 1.00, 𝜆̄ = 0, 𝜌 = 0.10, 𝑎𝑘 = 0.10.
   The switch in each cycle is scheduled at 𝑠𝑘 + 1.50 s, after the protected interval ends at 𝑠𝑘 + 𝜏 + ℎ̄ = 𝑠𝑘 + 1.10 s. The
two impulsive topology modes alternate over successive triggering cycles. The switching parameters are 𝑇𝑎 = 2.00
and 𝑁0 = 1. The Lyapunov parameters are selected as 𝑃𝑟 = 𝐼3 , 𝑆𝑟 = 0.25𝐼3 , 𝑅𝑟 = 0.05𝐼3 , 𝜀𝑖,𝑟 = 0.10, for both modes,
with 𝜆1,𝑟 = 0, 𝜇 = 1, 𝛼 = 0.80, 𝜑 = 1.97.
   The initial histories are constant on [−0.10, 0]. They are specified by
                                             ⎡𝑒𝖳1 (𝜃)⎤ ⎡ 5      1 −3⎤
                                             ⎢𝑒𝖳 (𝜃)⎥ ⎢ 4       2 −2⎥
            [                      ]𝖳        ⎢ 2𝖳 ⎥ ⎢
      𝑠(𝜃) = 0.60     −0.40    0.80 ,        ⎢𝑒3 (𝜃)⎥ = ⎢−5     −2 0 ⎥ ,      −0.10 ≤ 𝜃 ≤ 0.
                                             ⎢𝑒𝖳 (𝜃)⎥ ⎢ 1            ⎥
                                                                0 −1⎥
                                             ⎢𝑒4𝖳 (𝜃)⎥ ⎣−7      −3 1 ⎦
                                             ⎣ 5 ⎦
    These values satisfy all conditions of Theorem 3.5. Therefore, the network achieves global exponential leader-
follower synchronization under the proposed hybrid control. Figure 2 shows that all synchronization errors converge
to zero under the hybrid control. The maximum error at 𝑡 = 12 s is 4.3163 × 10−7 . For comparison, all control and
inter-node coupling are removed in Figure 3. The error curves remain separated, and the maximum error at 𝑡 = 12 s is
approximately 8.4527.

4. Conclusion
    Andy provides an end-to-end workflow that turns a mathematical problem into a traceable proof. It organizes proof
steps in an executable DAG, binds each local verification result to a certificate, uses node interfaces to confine repairs to
the affected proof region, and records the complete path from problem formulation to final proof. The system separates
proof generation from correctness evaluation and can acquire, retain, retrieve, and reuse knowledge from existing
results. The case study shows that Andy can develop a technically meaningful problem from an established result and
carry it through theorem construction, proof, and numerical illustration.
    Starting from the self-triggered impulsive consensus result in [1], Andy formulated a global exponential leader-
follower synchronization problem for delayed heterogeneous networks with switching communication topologies. The
control-theoretic contribution is the recovery-window design. After each delayed impulse, model-matching feedback
temporarily removes the delayed error channel until the pre-impulse history leaves the active delay interval. This
separation permits a quadratic Lyapunov estimate during recovery and restores the full Lyapunov-Krasovskii functional
afterward. It brings switching topology, impulse execution delay, and self-triggered updates into one exponential-
synchronization proof. Sufficient conditions were established, Zeno behavior was excluded for both timing sequences,
and the numerical example illustrates the expected synchronization behavior.

Zi’an Wang                                                                                                    Page 15 of 20
                        Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research


               10
                                                                                    Follower 1   Follower 4

                                                                                    Follower 2   Follower 5
                8
                                                                                    Follower 3



                6




                4




                2




                0
                    0             2              4               6              8                 10           12
                                                            Time t (s)

         Figure 2: Synchronization errors ‖𝑥𝑖 (𝑡) − 𝑠(𝑡)‖2 of the five followers under the proposed hybrid control.



               10
                                                                                    Follower 1   Follower 4
                                                                                    Follower 2   Follower 5
                8                                                                   Follower 3




                6




                4




                2




                0
                    0             2              4               6              8                 10           12
                                                            Time t (s)

                    Figure 3: Synchronization errors ‖𝑥𝑖 (𝑡) − 𝑠(𝑡)‖2 of the five followers without control.



    Future work will investigate CrewAI-style role-based multi-agent orchestration in which the solver, evaluator, and
human-like monitor operate as distinct agents. Independent roles can reduce correlated self-evaluation errors and
make disagreements explicit. Parallel exploration can increase proof-route coverage and shorten the time spent on
unsuccessful branches. Role-specific messages and certificates can also improve traceability, while dynamic routing,
escalation, and cross-checking can make the workflow more robust to errors from a single model or reasoning route.



Zi’an Wang                                                                                                          Page 16 of 20
                          Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

References
 [1] S. Hong, Y. Zhang, Consensus of switched delay multi-agent systems via self-triggered impulsive control, International Journal of Control
     95 (12) (2022) 3252–3261. doi:10.1080/00207179.2021.1970815.
 [2] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P. Kumar, E. Dupont, F. J. R. Ruiz, J. S. Ellenberg, P. Wang, O. Fawzi,
     P. Kohli, A. Fawzi, Mathematical discoveries from program search with large language models, Nature 625 (2024) 468–475. doi:
     10.1038/s41586-023-06924-6.
 [3] T. H. Trinh, Y. Wu, Q. V. Le, H. He, T. Luong, Solving olympiad geometry without human demonstrations, Nature 625 (2024) 476–482.
     doi:10.1038/s41586-023-06747-5.
 [4] X. Chen, X. Jiang, Moonshine: An autonomous mathematical research agent centered on conjecture generation (2026). arXiv:2606.10806.
     URL https://arxiv.org/abs/2606.10806
 [5] Z. Zhao, B. Yuan, J. Choi, Y. Chen, RMA: An agentic system for research-level mathematical problems (2026). arXiv:2605.22875.
     URL https://arxiv.org/abs/2605.22875
 [6] C. An, Q. Ye, M. Pan, J. Zhang, QED: An open-source multi-agent system for generating mathematical proofs on open problems (2026).
     arXiv:2604.24021.
     URL https://arxiv.org/abs/2604.24021
 [7] J. Schmitt, T. Gehrunger, J. Dekoninck, G. Bérczi, U. Kreitner, L. Price, D. Holmes, ProofCouncil: An LLM agent for solving open
     mathematical problems (2026). arXiv:2607.09474.
     URL https://arxiv.org/abs/2607.09474
 [8] J. Liu, G. Gao, Z. Sun, B. Wu, S. Liu, J. Jiang, H. Ju, L. Chen, R. Cheng, X. Zhang, B. Dong, Danus: Orchestrating mathematical reasoning
     agents with fact-graph memory (2026). arXiv:2607.06447.
     URL https://arxiv.org/abs/2607.06447
 [9] H. Ju, G. Gao, J. Jiang, B. Wu, Z. Sun, S. Liu, L. Chen, Y. Wang, Y. Wang, Z. Wang, W. He, P. Wu, L. Xiao, R. Liu, B. Dai, B. Dong,
     Automated conjecture resolution with formal verification (2026). arXiv:2604.03789.
     URL https://arxiv.org/abs/2604.03789
[10] Y. Cao, R. Qiu, J. Liu, J. Wang, D. Guo, R. Feng, L. Zhi, X.-S. Gao, Mechmath agent team: LLM driven agents for mathematical research
     (2026). arXiv:2607.04394.
     URL https://arxiv.org/abs/2607.04394
[11] J. Pearl, Probabilistic Reasoning in Intelligent Systems: Networks of Plausible Inference, Morgan Kaufmann, San Mateo, CA, 1988.
[12] J.-L. Wang, L.-H. Zhao, PD and PI control for passivity and synchronization of coupled neural networks with multi-weights, IEEE Transactions
     on Network Science and Engineering 8 (1) (2021) 790–802. doi:10.1109/TNSE.2021.3052889.
[13] J.-L. Wang, L.-H. Zhao, H.-N. Wu, T. Huang, Finite-time passivity and synchronization of multi-weighted complex dynamical networks under
     PD control, IEEE Transactions on Neural Networks and Learning Systems 35 (1) (2024) 507–518. doi:10.1109/TNNLS.2022.3175747.
[14] I. Kanellakopoulos, P. V. Kokotović, A. S. Morse, Systematic design of adaptive controllers for feedback linearizable systems, IEEE
     Transactions on Automatic Control 36 (11) (1991) 1241–1253. doi:10.1109/9.100933.
[15] R. Zhou, T. Quartz, H. De Sterck, J. Liu, Neural Lyapunov control of unknown nonlinear systems with stability guarantees, in: Advances in
     Neural Information Processing Systems, Vol. 35, 2022, pp. 29113–29125. doi:10.52202/068431-2111.
[16] L. Zhang, J. Lu, F. Liu, J. Lou, Synchronization of time-delay coupled neural networks with stabilizing delayed impulsive control, IEEE
     Transactions on Neural Networks and Learning Systems 35 (12) (2024) 18899–18906. doi:10.1109/TNNLS.2023.3320651.
[17] X. Xie, X. Li, S. Song, X. Liu, A self-triggered impulsive approach to group consensus of MASs with sensing/actuation delays, IEEE
     Transactions on Systems, Man, and Cybernetics: Systems 54 (2) (2024) 1168–1179. doi:10.1109/TSMC.2023.3326830.



A. Research Trace of the Case Study
    This appendix records the main research decisions made during the case study. It summarizes the problem-revision
history, the low-cost exploration of proof routes, the construction of the proof dependency graph, and the selection of
the final proof chain.

A.1. Problem Revision and Research-Value Evaluation
     The evaluator recorded nine consecutive versions of the proposed research problem, indexed from 0 to 8. Thus, the
initial proposal was followed by eight revision cycles. Each version was scored for importance, originality, feasibility,
and coherence. Acceptance required a weighted total of at least 7.5, a score of at least 6 in every dimension, and a
single research objective that could be answered by one principal conclusion. Table 2 gives the complete evaluation
trace.
Example A.1. In Version 1, Andy proposed the following problem. Consider a leader and 𝑁 heterogeneous followers
governed by

        ̇ = −𝐶𝑠(𝑡) + 𝐴𝑓 (𝑠(𝑡)) + 𝐵𝑔(𝑠(𝑡 − ℎ(𝑡))),
        𝑠(𝑡)
       𝑥̇ 𝑖 (𝑡) = −𝐶𝑖 𝑥𝑖 (𝑡) + 𝐴𝑖 𝑓 (𝑥𝑖 (𝑡)) + 𝐵𝑖 𝑔(𝑥𝑖 (𝑡 − ℎ(𝑡))) + 𝑢𝑐𝑖 (𝑡) + 𝑢𝑝𝑖 (𝑡),

Zi’an Wang                                                                                                                      Page 17 of 20
                       Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

Table 2
Evaluation trace for the proposed research problem.

                                    Version     Imp.    Orig.    Feas.      Coh.   Total
                                       0        6.5       6        6        5.5     6.07
                                       1         6        5        3         4      4.65
                                       2         7        7        6         7      6.75
                                       3         7        8        6         7      7.05
                                       4         8        8        7         8      7.75
                                       5         8        8        7         8      7.75
                                       6         8        8        7         8      7.75
                                       7         8        8        7         8      7.75
                                       8         8        8        7         8      7.75


with 𝑒𝑖 = 𝑥𝑖 − 𝑠, use the manifold-compensation feedback 𝑢𝑐𝑖 = (𝐶𝑖 − 𝐶)𝑠 + (𝐴 − 𝐴𝑖 )𝑓 (𝑠) + (𝐵 − 𝐵𝑖 )𝑔(𝑠(𝑡 − ℎ(𝑡))) − 𝐾𝑖 𝑒𝑖 .
At each delayed impulse time 𝑡𝑘 = 𝑠𝑘 + 𝜏, impose 𝑒(𝑡+     𝑘
                                                            ) = (𝑀𝑘 ⊗ 𝐼𝑛 )𝑒(𝑠−
                                                                             𝑘
                                                                               ). For the switching quadratic function
𝑉 (𝑡) = 𝑒𝖳 (𝑡)(𝐼𝑁 ⊗ 𝑃𝜎(𝑡) )𝑒(𝑡), introduce the scalar comparison system 𝑊̇ = 𝜆̄ 1 𝑊 + 𝜅 between impulses and
𝑊 (𝑡𝑘 ) = 𝜂𝑘 𝑊 (𝑠−𝑘
                    ) at impulses. Generate the next sampling time from

                {                                        }                              𝑎𝑘 + ln 𝑊𝑘2
      𝑠𝑘+1 = inf 𝑡 > 𝑠𝑘 + 𝜏 ∶ 𝑡 − 𝑠𝑘 − 𝜏 − Φ(𝑘, 𝑊𝑘2 ) ≥ 0 ,              Φ(𝑘, 𝑊𝑘2 ) =               .
                                                                                          𝜆̄ 1 + 𝜌

The task was to select the controller and triggering parameters so that the switching, impulse-contraction, and
cumulative-decay conditions guaranteed global exponential leader-follower synchronization and a uniform positive
lower bound on the intersampling intervals.
    This version received scores of 6, 5, 3, and 4 for importance, originality, feasibility, and coherence, respectively,
with a total score of 4.65. Feasibility was the principal failure. The proposed argument claimed that a fixed constant
𝜅 could absorb the delayed state-dependent term 𝜆2 𝑊 (𝑡 − ℎ(𝑡)). Such a constant cannot dominate that term while the
same comparison system is required to converge to zero. The Halanay-Li comparison bridge therefore did not close.
The impulsive condition also constrained only the instantaneous quadratic term and did not control the history terms
of a complete Lyapunov-Krasovskii functional. Coherence fell below the threshold because the delay, switching, and
impulsive mechanisms were not connected by one valid estimate, and the required condition ℎ(𝑡)     ̇   ≤ 𝛿 < 1 had not
been stated. The originality score was also below the threshold because the claimed integration of the mechanisms
depended on this invalid step and two literature attributions were incomplete.
    The evaluator recommended removing the additive-constant absorption step, constructing an explicit mode-
dependent Lyapunov-Krasovskii functional, adding the delay-derivative assumption, deriving verifiable block matrix
inequalities, and treating the jump of the complete functional at impulsive instants. It also requested a concrete
intermediate lemma that connected the flow, delay, and impulse estimates before the revised problem proceeded to
full proof execution.
     Versions 4 through 7 had already cleared every numerical threshold. They were rejected solely because the proposal
still presented several parallel subquestions as separate targets. The final revision retained the mathematical content
and reorganized these requests into one objective: establish global exponential leader-follower synchronization under
a unified switching hybrid-control theorem.

A.2. Low-Cost Route Exploration and DAG Construction
    The route planner first explored several strategies at low computational cost. The first round considered scalar
comparison domination, direct interval-wise Lyapunov stitching, and a discrete impulse-map approach. The second
round refined the comparison route into a Li-type scalar comparison argument with a cumulative condition and also
considered multiple-Lyapunov stitching, unified growth-rate absorption, and a direct impulsive Gronwall-Halanay
recurrence. These two rounds produced seven route records. The comparison route received the highest feasibility
assessment and became the main route. The strongest structurally different candidates were retained as backups. The
discrete-map and unified-growth approaches were discarded because they either lost essential delay and switching

Zi’an Wang                                                                                                    Page 18 of 20
                       Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

information or introduced excessive conservatism. The seven records therefore represent broad preliminary exploration,
while only three route families were promoted to executable branches.

A.3. Proof-Node Responsibilities and Exact Dependencies
    Here and below, 𝑁𝑖 denotes the 𝑖th proof node in the execution plan. Each proof node is a mathematical work unit
with a specified input, conclusion, dependency set, and verification criterion. The subscript 𝑖 is a stable node identifier;
model iterations, difficulty levels, and branch numbers use different notation. The notation 𝑁𝑖 -𝑟𝑗 denotes the immutable
𝑗th revision of node 𝑁𝑖 . Table 3 defines every node.

Table 3
Proof-node responsibilities, direct dependencies, and final records.
        Node Responsibility                                                Direct predecessors       Record
         𝑁1   Two-stage error system, recovery-window controller, and      None                      Frozen at 𝑟2
              impulsive error map
        𝑁2    Recovery-window quadratic growth bound                       𝑁1                        Frozen at 𝑟1
        𝑁3    Normal-phase LKF Dini-derivative estimate                    𝑁1                        Frozen at 𝑟1
        𝑁4    Impulse jump estimate and effective contraction factor       𝑁1                        Frozen at 𝑟1
        𝑁5    Interface between the recovery and normal phases             𝑁1 , 𝑁2                   Frozen at 𝑟5
        𝑁6    Li-type scalar comparison dominating the full functional     𝑁2 , 𝑁3 , 𝑁4 , 𝑁5         Invalidated
        𝑁7    Cauchy factor and exponential-decay estimate                 𝑁6                        Invalidated
        𝑁8    Main-branch theorem assembly                                 𝑁7                        Invalidated
        𝑁9    Direct interval-wise stitching without a scalar comparator   𝑁2 , 𝑁3 , 𝑁4 , 𝑁5         Failed after 𝑟3
        𝑁10   First backup-theorem assembly                                𝑁9                        Not run; invalidated
        𝑁11   Direct impulsive Gronwall-Halanay cumulative recurrence      𝑁2 , 𝑁3 , 𝑁4 , 𝑁5         Frozen at 𝑟2
        𝑁12   Final synchronization-theorem assembly                       𝑁11                       Frozen at 𝑟4


   The common prefix of the graph contained the system reduction and the four estimates needed by every branch.
The planner then attached three alternative tails to this verified prefix. Figure 4 shows the resulting execution graph.


                                   𝑁2               𝑁5                     𝑁6                  𝑁7             𝑁8



                  𝑁1               𝑁3                                      𝑁9                  𝑁10



                                   𝑁4                                      𝑁11                 𝑁12

Figure 4: Executed proof DAG. Node responsibilities and direct predecessors are listed in Table 3. Green nodes were verified
and frozen, red marks the failed backup node, and gray nodes were invalidated after an upstream change or branch failure.



A.4. Failed Branches and Final Route Selection
    The main branch comprised 𝑁6 , 𝑁7 , and 𝑁8 . During the repair of 𝑁5 , the interface factor was replaced by the
corrected mode-dependent quantity 𝜒̃𝑟 . This change altered the dependency fingerprint of the downstream comparison
construction. The three nodes were therefore invalidated before further execution. Their invalidation records an
upstream interface change and leaves the local validity of individual statements in the abandoned branch undecided.
    The first backup branch failed at 𝑁9 after three revisions. The first revision contained a sign error in the logarithmic
exponent and counted the average-dwell-time chatter term twice. The second introduced an undeclared maximum
interval and omitted a time-dependent switching factor. The third relied on an unavailable growth-rate inequality,
counted the recovery cost twice, and omitted switches between a sampling instant and its delayed impulse. These
failures showed that direct interval stitching was too fragile for the coupled recovery, delay, and switching interfaces.
Consequently, 𝑁10 was never executed.

Zi’an Wang                                                                                                          Page 19 of 20
                      Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

    The second backup branch retained the interval estimates and changed only their assembly mechanism. The first
revision of 𝑁11 omitted the corrected phase condition and did not verify that the normal interval had nonnegative
length. Its second revision used 𝜒̃max , added the required trigger margin, and completed the cumulative recurrence.
The first three revisions of 𝑁12 still exposed mismatches between the theorem statement and the verified proof interface.
Revision 4 made the actual assumptions explicit and passed independent verification.
    The final proof chain was therefore

      𝑁1 -𝑟2 ⟶ {𝑁2 -𝑟1 , 𝑁3 -𝑟1 , 𝑁4 -𝑟1 } ⟶ 𝑁5 -𝑟5 ⟶ 𝑁11 -𝑟2 ⟶ 𝑁12 -𝑟4 .

The braces indicate that 𝑁2 , 𝑁3 , and 𝑁4 were verified in parallel. The dependency of 𝑁5 was limited to 𝑁1 and 𝑁2 ,
while 𝑁11 used all four shared estimates 𝑁2 through 𝑁5 . At the end of the run, seven nodes were frozen, one node had
failed, and four nodes had been invalidated. The graph contained nineteen immutable node revisions, which preserved
the complete repair history while allowing the verified prefix to be reused.




Zi’an Wang                                                                                                 Page 20 of 20
