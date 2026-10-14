                                                Symbolic Search Is Not Exhausted: Persistent
                                                    Proof-Space Exploration in Lean4


                                                                                       Ruoran Xu
                                                                           Xi’an Jiaotong-Liverpool University
                                                                         ruoran.xu24@student.xjtlu.edu.cn
arXiv:2610.04275v1 [cs.LO] 3 Oct 2026




                                                                                           Abstract

                                                  Formal theorem proving increasingly combines learned semantic guidance with
                                                  verified symbolic execution. The quality of the symbolic search substrate therefore
                                                  determines how much useful mathematical structure can be accumulated, reused,
                                                  and exposed under a finite inference budget. We introduce V IA L EAN, a Lean4
                                                  prover that organizes symbolic reasoning as bounded exploration of a persistent
                                                  proof-state graph. Its search preserves coverage across complementary reasoning
                                                  modes, merges semantically equivalent goals, retains verified intermediate structure,
                                                  and observes short symbolic futures before committing to a transition. On the
                                                  complete miniF2F test split, the model-free configuration solves 122/244 problems
                                                  (50.0% pass@1). Historical and recent symbolic reference points range from
                                                  Lean’s earlier tidy search to modern grind and SMT-backed verification, showing
                                                  that proof-space organization remains a substantial source of capability. The same
                                                  persistent state also provides a natural interface for neural–symbolic agents: neural
                                                  reasoning can operate over verified regions and intermediate objects while Lean
                                                  continuously expands and validates the local proof space.


                                        1    Introduction

                                        Formal theorem proving has entered a regime in which specialized language models can generate
                                        complete Lean proofs, synthesize formal data, and improve through proof-assistant feedback and
                                        reinforcement learning [Wang et al., 2024, Xin et al., 2024, 2025, Lin et al., 2025a, Li et al., 2024,
                                        Lin et al., 2025b, Leang et al., 2026]. These systems place increasingly strong semantic priors over
                                        formal reasoning. Their proposals still enter a symbolic environment whose search state, reusable
                                        consequences, tactic scheduling, and verification procedures determine how efficiently finite inference
                                        is converted into a completed proof.
                                        This observation separates two complementary sources of capability. Semantic guidance supplies
                                        mathematical jumps such as a useful lemma, witness, decomposition, or representation change.
                                        Proof-space organization determines how verified local consequences are retained, which reasoning
                                        modes remain represented, when equivalent goals are merged, and how far symbolic structure is
                                        explored before the prover commits to a branch. The first source has advanced rapidly through
                                        learned provers. The second remains an algorithmic design space inside the proof assistant.
                                        miniF2F [Zheng et al., 2022] provides a useful trace of this symbolic design space. Its original
                                        deterministic Lean tidy baseline solves 18.0% of the test split at pass@1. Recent evaluation reports
                                        79/244 problems (32.4%) for model-free Lean grind, while SMT-backed Dafny automation verifies
                                        95/244 translated test problems (38.9%) with an empty proof body [Baksys et al., 2026]. Isabelle
                                        Sledgehammer reaches 10.4% on miniF2F-test in its proof environment [Böhme and Nipkow, 2010,
                                        Jiang et al., 2022]. The systems use different languages, libraries, and automation stacks, yet the


                                        40th Conference on Neural Information Processing Systems (NeurIPS 2026). Workshop: The 6th Workshop on Mathematical
                                        Reasoning and AI.
Figure 1: Persistent proof-space exploration in V IA L EAN. A Lean goal is canonicalized into a
semantic state, expanded through a diversity-balanced symbolic frontier, accumulated in a persistent
Proof Atlas, and closed through bounded verified solvers. The Atlas also forms a shared state for
optional neural guidance over regions, intermediate objects, and future symbolic expansion.


progression makes one point clear: stronger symbolic organization continues to expand the set of
formal problems reachable before learned proof generation is invoked.
V IA L EAN develops this direction inside Lean 4. A proof attempt is represented as a bounded graph of
semantic proof states and typed transitions. Candidate generation is partitioned into complementary
symbolic perspectives so a high-volume operator family cannot monopolize the frontier. Equivalent
proof states are merged and their verified structure persists across later visits. Bounded future graphs
expose multi-step local consequences under saved metavariable state, and local synthesis continuously
materializes exact inhabitants and useful partial applications. The resulting model-free configuration
solves 122/244 = 50.0% of miniF2F-test at pass@1.
The system supports a broader agentic view of formal reasoning. The persistent graph can be rendered
as a compact verified workspace in which a model chooses regions, proposes typed intermediate
objects, or requests additional expansion. Symbolic search then converts these interventions into
explicit goals, transitions, and validated consequences. This shared state connects high-level semantic
reasoning to dense low-level proof development.
Our contributions are threefold. First, we formulate finite-budget Lean search as persistent proof-
space exploration with explicit coverage across symbolic reasoning modes. Second, we instantiate
this view in a kernel-checked prover that combines semantic state merging, bounded symbolic
lookahead, continuous local synthesis, and budget-aware scheduling. Third, we report a 50.0%
model-free pass@1 result on the complete miniF2F test split and describe how the same proof
state can support deeper neural–symbolic co-search. The implementation is available at https:
//github.com/RuoranXu/ViaLean.

2   Related Work and Empirical Context
Symbolic proof automation. Interactive theorem provers have long used symbolic automation to
compress routine proof development. Isabelle’s Sledgehammer connects proof states to first-order
and SMT solvers [Böhme and Nipkow, 2010]; Lean’s mathlib provides a large formal library together
with tactic-level automation [The mathlib Community, 2020]. Aesop develops configurable white-box
best-first proof search in Lean [Limperg and From, 2023], and Canonical studies automated proof
construction through type inhabitation and term synthesis [Norman and Avigad, 2025]. Across
these lines, the effective search space depends on the representation of states, the scheduling of
heterogeneous operators, and the amount of verified structure that survives across local attempts.
The model-free miniF2F reference points in Table 1 capture several generations and proof envi-
ronments. Lean tidy provides an early deterministic tactic-search baseline [Zheng et al., 2022];
Sledgehammer contributes mature ATP-backed automation in Isabelle [Jiang et al., 2022]; and recent


                                                   2
measurements of Lean grind and Dafny illustrate the reach of modern native and SMT-backed
procedures [Baksys et al., 2026, Leino, 2010]. We use these values as contextual reference points for
symbolic reach, with each row retaining its original proof environment and evaluation setting.

Learned Lean provers. Learned systems have expanded the semantic range of formal proof
search. TheoremLlama specializes a general language model for Lean proof generation [Wang
et al., 2024]. DeepSeek-Prover and DeepSeek-Prover-V1.5 combine synthetic formal data, verifier
feedback, reinforcement learning, and search [Xin et al., 2024, 2025]. Goedel-Prover uses iterative
data synthesis and reports 57.6% pass@32 on miniF2F [Lin et al., 2025a]; HunyuanProver reports
68.4% with guided tree search [Li et al., 2024]; Goedel-Prover-V2 and Pythagoras-Prover further
raise learned proving performance with stronger models and inference procedures [Lin et al., 2025b,
Leang et al., 2026]. These systems motivate a symbolic substrate that exposes richer verified state
than a terminal accept/reject signal, especially when models reason over several proof decisions.

3     Persistent Proof-Space Exploration
Let a Lean proof state be s = (Γ ⊢ g). A symbolic operation may close g or produce a set of
successor obligations, yielding an AND/OR transition structure. V IA L EAN organizes this structure
as a bounded Atlas A = (V, E) whose vertices are semantic proof states and whose edges are typed,
replayable transitions. Four mechanisms determine how this Atlas grows.

3.1   Perspective-balanced symbolic frontier

A local proof state usually admits heterogeneous operations with very different branching factors.
Rewriting and local application can generate many candidates, while constructor reasoning, contradic-
tion, equality transport, or bounded forward closure may produce only a few. Ranking all candidates
in one pool makes the candidate count of an operator family interact directly with global coverage.
V IA L EAN partitions generation by symbolic perspective: normalization, contradiction, rewriting,
elimination, construction, backward application, typed forward closure, equality reasoning, and
bounded future exploration. If Cp (s) denotes candidates from perspective p, q is a per-perspective
cap, and B is the global frontier budget, the merge operator is
                                                                  
                             FB (s) = TakeB RRp∈P Takeq Cp (s) ,                                (1)
where RR is round-robin interleaving. When B covers the active perspectives, each active perspective
contributes one candidate before a second candidate is drawn from any perspective. This gives a
simple deterministic coverage guarantee under a fixed frontier budget and keeps multiple modes of
local mathematical reasoning available to the scheduler.

3.2   Persistent semantic states and transpositions

Tactic histories frequently converge to the same mathematical obligation. V IA L EAN assigns each
state a strict semantic identity derived from the target and ordered local context, with local names
alpha-normalized and hash matches structurally confirmed. Reaching an existing identity reuses
the corresponding Atlas vertex. Its outgoing transitions, failures, synthesized objects, and verified
descendants remain available to subsequent search.
This transposition structure changes the unit of accounting from a path prefix to a proof state.
Repeated symbolic routes can therefore share downstream work, and verified intermediate structure
becomes persistent memory within the proof attempt. The Atlas remains finite through explicit
bounds on vertices, transitions, work units, meta-level operations, rendering, and wall-clock time. A
single global deadline is propagated across symbolic expansion, leaf solving, recursive subgoals, and
optional model interaction.

3.3   Bounded future observation

Many useful local transformations reveal their value after several verified steps. A rewrite may
expose a normal form; an introduction may reveal a reusable local implication; a constructor can
create arithmetic obligations that close immediately. V IA L EAN explores such local futures under


                                                 3
Table 1: Selected miniF2F reference points. The symbolic rows retain their reported proof environ-
ments and evaluation settings; learned rows illustrate the higher ceiling obtained with trained prover
models and larger inference budgets.
                      System                       Regime          Test   Setting
                      Lean tidy [Zheng et al.,     symbolic       18.0%   pass@1, deterministic
                      2022]
                      Sledgehammer [Jiang          symbolic       10.4%   Isabelle miniF2F
                      et al., 2022]
                      Lean grind [Baksys           symbolic       32.4%   79/244, no model
                      et al., 2026]
                      Dafny verifier [Baksys       symbolic       38.9%   95/244, empty proof
                      et al., 2026]
                      V IA L EAN (ours)            symbolic       50.0%   122/244, pass@1
                      DeepSeek-V1.5-RL [Lin        learned        50.0%   whole-proof pass@32
                      et al., 2025a, Xin et al.,
                      2025]
                      Goedel-Prover-SFT [Lin       learned        57.6%   pass@32
                      et al., 2025a]




saved metavariable state and records a bounded future graph containing goals, operator paths, and
qualitative signals. Observation is transactional: the previewed metavariable state is restored after
inspection, and a chosen transition is replayed on a fresh goal before its subgoals are solved.
The future graph is controlled independently by depth, width, node, character, and work budgets.
These limits make short symbolic foresight compatible with a strict global budget. The scheduler
can therefore compare nearby proof regions using their verified local structure while maintaining a
compact persistent workspace.

3.4   Continuous local synthesis and verified closure

At each visited state, a local synthesizer enumerates multiple exact inhabitants together with partial
applications and their typed gaps. These objects are inserted into the same search process as
tactic-generated transitions, allowing intermediate terms to reshape subsequent reachability. Shared
generators also produce kernel-typed facts such as equality transport so native rewriting and model-
facing state views refer to the same verified objects.
Local closure is supplied by bounded mathlib automation, including normalization, rewriting, arith-
metic procedures, and general tactic search [The mathlib Community, 2020, Limperg and From,
2023]. Every successful branch is elaborated into an ordinary Lean term and checked against the
requested target by Lean 4 [de Moura and Ullrich, 2021]. The proof returned to the caller is therefore
the endpoint of the same typed transition system stored in the Atlas.

4     Model-Free Evaluation on miniF2F
Protocol. We evaluate all 244 problems in the miniF2F test split [Zheng et al., 2022]. The theorem-
answer declarations are excluded from the evaluation environment, and target-theorem retrieval is
disabled. The evaluated configuration uses the symbolic engine, local synthesis, Atlas persistence,
bounded future exploration, and mathlib leaf closure with the external model interface disabled. A
case is solved when Lean constructs a complete proof term for the target. The resulting system solves
122/244 problems (50.0% pass@1).

Empirical context. The symbolic rows show how much verified search can be obtained from
different automation stacks before learned proof generation contributes semantic proposals. ViaLean’s
50.0% result extends this sequence within Lean by combining diverse local expansion, persistent
state reuse, bounded future observation, and continuous term synthesis in one search process. The
learned rows occupy a different inference regime and indicate the semantic headroom available when
trained priors and multiple generations are added. Table 1 therefore separates two axes of progress:
stronger proof-space organization and stronger learned semantic guidance.
The reported score is a system-level measurement of the complete model-free configuration. Ap-
pendix L specifies a matched-compute decomposition for isolating perspective balancing, Atlas


                                                              4
persistence, future observation, and local synthesis under common budgets. Appendix N records the
evaluation boundary and implementation controls used to keep search, rendering, and provider work
explicitly bounded.

5     The Proof Atlas as an Agentic Interface
A persistent proof graph creates a direct interface between symbolic search and a higher-level
mathematical agent. The Atlas exposes verified states, typed transitions, synthesized objects, explored
regions, and structured failures. A model can therefore condition directly on an evolving mathematical
workspace whose vertices and edges summarize the verified search history.
The implementation exposes three interfaces over the same Atlas. A planner reasons over compressed
regions and can request expansion or propose typed terms, helper cuts, bridges, and witnesses;
an interactive mode receives symbolic futures and structured feedback; and a policy mode scores
existing actions. Lean elaborates proposed objects before recording their typed consequences. This
gives a clean division of work: neural computation selects semantically expensive regions or objects,
while symbolic search performs normalization, rewriting, elimination, construction, forward closure,
synthesis, and leaf solving. Each accepted intervention updates the Atlas for the next model decision.

5.1   Stateful neural epochs over verified search

The interaction can be written as a sequence of stateful neural epochs. At epoch t, the model receives
a bounded compression ot = Compress(At ) containing selected Atlas regions, visible local facts,
candidate transitions, future summaries, and recent structured outcomes. It returns an intervention ut
drawn from a small semantic action space: prioritize a region, request expansion, propose a typed cut
or bridge, supply a witness, or submit a complete candidate. Lean elaboration maps the proposal to a
verified object u
                bt when possible, after which the symbolic controller continues bounded search:
                                    At+1 = Search(At , u
                                                       bt ; Bt ) ,                                  (2)
where Bt denotes the remaining node, transition, meta-operation, rendering, provider, and wall-clock
budgets. The next observation is generated from the updated Atlas. Equation (2) makes the proof
assistant’s verified state the persistent carrier of information across model calls.
This interface supports long-horizon reasoning with sparse neural intervention. One model call can
introduce a high-level mathematical object while the symbolic engine develops its local consequences,
merges repeated states, closes tractable obligations, and returns a compact account of the updated
proof region. The next neural epoch therefore receives both newly verified structure and precise
information about unresolved obligations.

5.2   Process-level supervision from Atlas deltas

The Atlas supplies a concrete unit for process-level supervision. For an intervention ut , the system
can record the verified delta ∆At = At+1 \ At together with cost and closure events: newly reached
states, proved intermediate facts, discharged obligations, transposition reuse, downstream proof depth,
and symbolic work. These quantities can supervise region selection, value estimation, or proposal
quality while remaining attached to kernel-checked events. Symbolic and neural improvements
therefore compose through the same persistent state: stronger search develops each intervention more
deeply, and stronger guidance places higher-value objects into the Atlas.

6     Conclusion
ViaLean organizes finite-budget theorem proving around a persistent proof-state graph with
perspective-balanced expansion, semantic state reuse, bounded futures, and local synthesis. The
reported model-free configuration reaches 50.0% pass@1 on miniF2F-test. The same Atlas provides
a shared verified workspace for neural–symbolic agents. Together, these mechanisms make symbolic
search an active reasoning substrate with explicit state, memory, foresight, and validation. Learned
configurations can use this state to carry semantic proposals and process-level feedback across model
calls within one kernel-checked search trajectory.


                                                  5
References
Mantas Baksys, Stefan Zetzsche, Olivier Bouissou, and Sean B. Holden. Minif2f-dafny: Llm-guided
 mathematical theorem proving via auto-active verification. arXiv preprint arXiv:2512.10187, 2026.

Sascha Böhme and Tobias Nipkow. Sledgehammer: Judgement day. In Automated Reasoning –
  IJCAR 2010, volume 6173 of Lecture Notes in Computer Science, pages 107–121. Springer, 2010.
  doi: 10.1007/978-3-642-14203-1_9.

Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language.
  In Automated Deduction – CADE 28, volume 12699 of Lecture Notes in Computer Science, pages
  625–635. Springer, 2021. doi: 10.1007/978-3-030-79876-5_37.

Albert Q. Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski, Tomasz Odrzygozdz, Piotr
  Milos, Yuhuai Wu, and Mateja Jamnik. Thor: Wielding hammers to integrate language models and
  automated theorem provers. In Advances in Neural Information Processing Systems, volume 35,
  2022.

Joshua Ong Jun Leang, Zheng Zhao, Mihaela Catalina Stoian, Qiyuan Xu, Haonan Li, Wenda Li,
  Shay B. Cohen, and Eleonora Giunchiglia. Pythagoras-prover: Advancing efficient formal proving
  via augmented lean formalisation. arXiv preprint arXiv:2606.12594, 2026.

K. Rustan M. Leino. Dafny: An automatic program verifier for functional correctness. In Logic for
  Programming, Artificial Intelligence, and Reasoning – LPAR-16, volume 6355 of Lecture Notes in
  Computer Science, pages 348–370. Springer, 2010. doi: 10.1007/978-3-642-17511-4_20.

Yang Li, Dong Du, Linfeng Song, Chen Li, Weikang Wang, Tao Yang, and Haitao Mi. Hunyuanprover:
  A scalable data synthesis framework and guided tree search for automated theorem proving. arXiv
  preprint arXiv:2412.20735, 2024.

Jannis Limperg and Asta Halkjær From. Aesop: White-box best-first proof search for lean. In
  Proceedings of the 12th ACM SIGPLAN International Conference on Certified Programs and
  Proofs, pages 253–266, 2023. doi: 10.1145/3573105.3575671.

Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu, Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
  Xia, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-prover: A frontier model for open-source
  automated theorem proving. arXiv preprint arXiv:2502.07640, 2025a.

Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,
  Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing Lu, David Acuna, Kaiyu Yang, Hongzhou Lin,
  Yejin Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-prover-v2: Scaling formal theorem
  proving with scaffolded data synthesis and self-correction. arXiv preprint arXiv:2508.03613,
  2025b.

Chase Norman and Jeremy Avigad. Canonical for automated theorem proving in lean. In 16th
  International Conference on Interactive Theorem Proving (ITP 2025), volume 352 of Leibniz
  International Proceedings in Informatics, pages 14:1–14:20. Schloss Dagstuhl – Leibniz-Zentrum
  für Informatik, 2025. doi: 10.4230/LIPIcs.ITP.2025.14.

The mathlib Community. The lean mathematical library. In Proceedings of the 9th ACM SIGPLAN
  International Conference on Certified Programs and Proofs, CPP 2020, pages 367–381. ACM,
  2020. doi: 10.1145/3372885.3373824.

Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe Diao, Renjie Pi, and Tong Zhang. The-
  oremllama: Transforming general-purpose llms into lean4 experts. In Proceedings of the 2024
  Conference on Empirical Methods in Natural Language Processing, pages 11953–11974, 2024.
  doi: 10.18653/v1/2024.emnlp-main.667.

Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li,
  and Xiaodan Liang. Deepseek-prover: Advancing theorem proving in llms through large-scale
  synthetic data. arXiv preprint arXiv:2405.14333, 2024.


                                                6
Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue
  Zhang, Xuan Lu, Qiushi Du, Wenjun Gao, Haowei Zhang, Qihao Zhu, Dejian Yang, Zhibin Gou,
  Z. F. Wu, Fuli Luo, and Chong Ruan. Deepseek-prover-v1.5: Harnessing proof assistant feedback
  for reinforcement learning and monte-carlo tree search. In International Conference on Learning
  Representations, 2025.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark for
  formal olympiad-level mathematics. In International Conference on Learning Representations,
  2022.




                                               7
A    Semantic Proof-State Identity and Transpositions

The persistent search graph relies on a proof-state identity that is stricter than a rendered goal string.
Let a Lean state be
                                s = (Γ ⊢ g),       Γ = (d1 , . . . , dn ),
where each declaration di is either a local assumption or a local let-binding. The implementation
constructs a semantic key
                                                                  n 
                          K(s) = ϕΓ (g), (κi , ϕ<i (τi ), ϕ<i (vi )) i=1 ,                     (3)

where κi ∈ {local, letDecl} records the declaration kind, τi is its type, vi is its optional let-value,
and ϕ replaces free-variable identities by position-stable bound variables and erases binder names.
The order of the local context is retained. Implementation-detail declarations are omitted, while
let-values remain semantic content.
This construction has two practical consequences. First, alpha-renaming of user-facing binders does
not create a new search state. Second, states that agree only textually are not merged when their local
declaration structure, declaration kind, type, or let-value differs. The resulting key is used throughout
cycle detection, bounded-future exploration, and Atlas transposition detection.

Collision-safe lookup. The key has a 64-bit hash bucket for fast indexing, but hash equality is not
treated as semantic equality. Membership first selects a bucket and then checks full structural equality
of the key. Thus the hash is an acceleration structure rather than the proof-state identity itself. If
h(K1 ) = h(K2 ) while K1 ̸= K2 , the states remain distinct.

Transposition insertion. When a newly observed goal has a key already represented in the Atlas,
the existing node is reused and the transposition counter is incremented. Otherwise a new node
is allocated if the node budget remains available. Consequently the graph can represent several
proof paths entering the same semantic goal without duplicating the state itself. This is especially
useful after rewriting, constructor decomposition, or helper-lemma introduction, where different local
histories can converge to the same residual obligation.


B    Proof Atlas Data Model

The Atlas is a typed graph with explicit evidence and bounded metadata. A node stores
                                   v = (id, K(s), ssnap , d, p, σ, c),                                (4)
where d is search depth, p indicates whether the node was created by preview, σ contains symbolic
signals, and c is a local difficulty estimate. Preview nodes additionally store a durable rendered goal
because the Lean metavariable state used to create them is later rolled back. A transition stores
                                     e = (id, vsrc , a, {vj }, x, z, ϵ),                              (5)
with symbolic candidate a, child nodes {vj }, executability flag x, coupling flag z, and transition evi-
dence ϵ. Evidence records one of untried, expanded, solved, failed, timedOut, or rejected,
together with elapsed time and an optional failure class.
The symbolic candidate itself is separated into three layers:
 1. a concrete operation, such as local application, constructor, cases, induction, rewrite, bridge,
    witness, cut, leaf solver, or exact term;
 2. a coarse strategy family used by scheduling and region aggregation;
 3. metadata consisting of prior, estimated cost, origin, and a stable fingerprint.
The strategy families are normalization, contradiction, equality, elimination, construction, backward,
forward, witness, cut, structural, leaf, and mixed. The same vocabulary is shared by symbolic
producers, the Atlas, the scheduler, and the planner interface.


                                                     8
B.1   Transition uniqueness and evidence updates

For a fixed parent node, a transition fingerprint acts as the identity of a candidate edge. Offering an
already present fingerprint returns the existing transition. A new edge is inserted only while both the
transition-count budget and the work-unit budget remain open. Successful child attachment marks
the transition as expanded; a solved edge records a terminal positive outcome; failed or rejected
outcomes mark its knowledge status as refuted. These status updates affect search memory and
planner observations, not Lean’s proof-theoretic acceptance criterion.

B.2   Structural transition potential

For previews with children, the implementation computes a bounded structural value from parent and
child difficulty estimates. Let cp be the parent cost, c1 , . . . , cm the child costs, and
                                       m
                                    1 X
                             c̄ =         cj ,       b(m) = 0.20(m − 1).
                                    m j=1

Then an expanded transition receives
                                                             cp
                           Vsym (e) = clip[0,1]                            ,                        (6)
                                                  max{0.1, cp + c̄ + b(m)}
while a solved edge has value 1 and an unexpanded edge has no structural value. The branch
penalty prevents a decomposition into many individually small children from appearing automatically
preferable. This quantity is a search signal; it is never used as evidence that a proposition is true.

B.3   Coarse proof regions

The Atlas can be compressed into proof regions indexed by strategy family. For each family, the
region stores its entry nodes, a small set of depth-ordered representatives, size, depth range, and
aggregate signals such as solved edges, failed edges, and nodes admitting an exact local inhabitant.
Region compression provides a stable intermediate granularity between a single tactic action and the
entire proof graph. Planner mode operates primarily at this granularity, while the underlying nodes
and transitions remain available when additional detail is needed.

C     Perspective-Balanced Frontier Construction
At a state s, each symbolic perspective p ∈ P independently emits an ordered sequence
                                       Cp (s) = (ap,1 , ap,2 , . . .).
The current implementation covers normalization, contradiction, equality/rewrite, elimination, con-
struction, backward application, forward reasoning, and multi-step symbolic futures, together with
other proposal families from the main search controller. Let q denote the per-perspective cap and B
the visible frontier budget. Define
                                     C
                                     ep (s) = Cp (s)1:min(q,|C (s)|) .
                                                              p

The global frontier is formed by round-robin interleaving of the capped sequences and truncation to
B items, as stated in Eq. (1).

First-round coverage property. Let A(s) = {p : Cp (s) ̸= ∅} be the active perspectives. If q ≥ 1
and B ≥ |A(s)|, the merged frontier contains at least one candidate from every active perspective
before any perspective contributes its second candidate. This follows because the first interleaving
round visits each active sequence once. Candidate multiplicity inside one family therefore cannot
remove all first-round representation from a lower-cardinality family.

Why the cap is separate from the global budget. The per-perspective cap controls domination by
a prolific producer; the global budget controls the visible action set. Keeping them separate allows
a family to remain represented without forcing the total action set to scale with the raw number of
rewrites, local applications, or retrieved premises.


                                                     9
D     Bounded Symbolic Future Graph
The future graph is an observation mechanism that expands short symbolic trajectories under saved
Lean metavariable state. The implementation uses breadth-first exploration. Each queue item
contains a goal metavariable, a depth, and an operator path. A node contributes a rendered goal and
qualitative symbolic signals; if it remains within the depth and node budgets, the engine tries at most
one successful successor group from each eligible operator family before further descendants are
expanded.
A compact description is:
 1. initialize the queue with the current goal and insert its semantic key into a strict visited set;
 2. pop queue items in FIFO order until the node cap, work cap, or wall-clock budget closes;
 3. render the current state and attach local signals;
 4. generate bounded successor groups from introduction, rewriting, elimination, induction at the
    root, construction, and backward application;
 5. for each accepted successor group, create a typed preview transition and bounded child states;
 6. deduplicate children using the same strict goal identity and enqueue unseen children while depth
    remains;
 7. restore Lean’s metavariable state after the observation transaction, while retaining the resulting
    durable Atlas records.
The breadth-first policy is important because the future view is itself a scarce observation budget. A
depth-first procedure can spend most of the budget following one operator family. FIFO expansion
instead exposes competing local futures at comparable depths. Within each future node, successor
groups are sorted by estimated symbolic cost with deterministic fingerprint tie-breaking; a requested
strategy family can be moved to the front without discarding the alternatives.

D.1   Preview versus execution

Future expansion and proof execution are intentionally distinct. Preview operations run in a saved
metavariable state and can create durable descriptions of counterfactual states, but they do not commit
a root proof assignment. When the controller selects an executable transition, the operation is replayed
on a fresh goal and its recursive obligations are solved through the ordinary controller. This separation
permits richer observation without making speculative state mutation part of the trusted proof path.

D.2   Finite observation bounds

The future view has independent caps for depth, per-node width, total future nodes, branch fan-out,
rendered characters, and meta-level work. With defaults from the public configuration, these are
depth 3, width 6, at most 24 future nodes, and at most 6 displayed/replayed children per branch.
These are implementation defaults rather than claims about the benchmark configuration; the harness
may override them.

E     Continuous Local Synthesis
Local synthesis runs at visited proof states and exposes complete and partial inhabitants independently
of model guidance. For each local declaration h : τ , the synthesizer first checks whether τ is
definitionally equal to the target g. If so, it emits a zero-cost exact inhabitant. Otherwise it follows a
bounded chain of nondependent arrows in τ and records the resulting domains as obligations. The
candidate is represented as
                                              q = (t, Ω, op, c),
where t is the local term, Ω is the array of missing obligations, op is the corresponding symbolic
operation, and c = |Ω| for partial local applications. A candidate is complete exactly when Ω = ∅.
The current synthesizer also detects reflexive equality goals and the proposition True. For an equality
x = x up to definitional equality it materializes Eq.refl; for True it materializes True.intro.


                                                   10
These small rules matter because complete inhabitants become direct closure opportunities, while
partial inhabitants expose useful typed decompositions to later search.
The synthesis layer is deliberately typed. It does not serialize arbitrary source-level terms as proof
facts. The term and its obligations remain Lean expressions inside the proof process, and any complete
candidate still passes the final validation path before the root proof is returned.

F    Transactional Execution and Meta-State Isolation
Lean metaprogramming manipulates mutable metavariable assignments, so speculative search re-
quires explicit isolation. ViaLean uses a transactional pattern at the operation boundary:
 1. save the complete metavariable state before preview or branch-local experimentation;
 2. execute a bounded transformation under the current local context;
 3. extract only stable information needed by the Atlas, such as rendered child goals, typed transition
    metadata, and structural signals;
 4. restore the saved state after preview, failed execution, or benchmark isolation;
 5. commit the original root assignment only after a complete candidate has been recursively solved
    and validated.
This creates two memory layers. The ephemeral Meta state contains temporary metavariables and
trial assignments. The persistent workspace contains semantic keys, durable node descriptions,
transition evidence, verified objects, structured failures, and version numbers. Rollback therefore
removes speculative Lean assignments without discarding what the search learned about the local
proof space.

Nested model calls. Model-generated subgoals and selected replay operations execute with nested
model queries disabled. This keeps one semantic intervention from recursively spawning uncontrolled
provider interactions and preserves a single accounting path for the outer search episode.

G    Budget Algebra and Operational Boundedness
The search budget is a vector rather than one scalar:
                                 B = (T, N, E, W, M, C, R, D, F, P ),                          (7)
where T is wall-clock time, N Atlas nodes, E Atlas transitions, W work units, M Meta operations,
C rendered characters, R regions, D future depth, F future nodes/width, and P provider/planner
capacity. Different producers debit different coordinates. In particular, increasing the number of
characters shown to a model does not create new symbolic work units, and increasing a displayed
frontier cap does not silently increase the persistent Meta-operation allowance.
The global deadline is installed as a Lean cancellation token over the complete search. The monitor
observes the remaining time and cancels provider, Atlas, retrieval, synthesis, and solver computation
through the same outer boundary. Local timeout cancellation is converted into an ordinary failed
attempt, while an already-set parent cancellation is propagated.

Operational boundedness. At the controller level, all explicit queues and loops have finite count
or work caps, and the full operation is covered by the shared cancellation deadline. Thus the search
cannot expand its own Atlas, future queue, provider loop, or trace stream without bound. This
statement concerns the implementation’s search control; it is distinct from a complexity theorem
about arbitrary Lean elaboration.

H    Planner and Interactive Protocols
The persistent workspace supports three model-facing modes over the same search state.

Policy mode. A model receives a set of kernel-checkable actions and returns bounded scalar signals.
These signals modify ranking only. They cannot close a goal or create a verified proposition.


                                                  11
      Configuration field                Default   Role
      timeoutSec                             10    shared wall-clock deadline
      maxDepth                                2    controller recursion depth
      maxActionsPerNode                      32    executable action cap
      frontierMaxProbes                      32    visible frontier probes
      frontierMaxPerPerspective               4    per-perspective visibility cap
      frontierFutureDepth                     3    symbolic future depth
      frontierFutureWidth                     6    successor groups per future node
      frontierFutureNodes                    24    total future-view nodes
      atlasMaxNodes                          96    persistent semantic states
      atlasMaxTransitions                   160    persistent typed transitions
      atlasMaxWorkUnits                     256    Atlas transition work cap
      atlasMaxMetaOps                       256    shared Meta-operation cap
      atlasMaxRenderedChars               16000    persistent rendering budget
      atlasMaxRegions                        12    compressed planner regions
      plannerMaxCalls                         4    planner calls in one search
      plannerMaxPayloadChars              16000    serialized planner payload cap
Table 2: Selected public defaults from the implementation. Benchmark or application configurations
may override these values.


Interactive mode. The request contains the current goal shape, local context summaries, actions,
symbolic frontier probes, bounded future views, and structured feedback from previous non-model
search events. A continuation may select actions or probes and may include Lean candidates.
Feedback records action family, outcome, elapsed time, and a bounded detail string.

Planner mode. The planner receives a compressed workspace containing a root view, proof
regions, selected nodes, typed transitions, recent observations, verified/speculative objects, remaining
wall-clock time, and remaining Atlas work. Its response can include region preferences, transition
policy/value/confidence values, a multi-family strategy, expansion requests, typed thought objects,
and Lean candidates.
One planner epoch can be written as
                              (πt , ρt , Ut ) = Plan(Compress(At ), Bt ),                           (8)
where πt contains transition-level signals, ρt contains region-level or expansion decisions, and Ut
contains proposed intermediate objects. The controller validates Ut , performs bounded symbolic
work, and produces an updated workspace version. The next request includes the corresponding Atlas
delta and observations.

H.1     Deterministic payload degradation

Both interactive and planner requests have absolute character caps. When a request exceeds the cap,
the serializer applies a deterministic degradation schedule rather than relying on provider truncation.
Planner requests first remove older observations, then reduce object, node, transition, and region
collections, and finally shorten the rendered root goal. If the minimal request still does not fit, the
payload becomes an empty JSON object. This keeps provider work explicitly bounded and makes
truncation behavior reproducible.

I     Typed Proposal Validation
Model outputs and internally generated bridges cross a narrow validation boundary before they can
become verified workspace objects. The common validator instantiates metavariables and rejects
an expression if it still contains unresolved metavariables, contains a loose bound variable, exceeds
the configured proposal-size cap, or fails type inference. Specialized validators then enforce the
target-dependent typing relation.
Validation does not by itself prove a helper proposition. A well-typed cut remains an obligation
until its proof is constructed. Likewise, a witness merely instantiates an existential and leaves the


                                                   12
    Proposal type             Validation condition
    Helper cut                candidate is a well-typed sort; by default it must be a proposition; it differs
                              definitionally from the target, True, and existing local assumptions
    Equality midpoint         target has form x = y over carrier τ ; candidate has type τ and differs
                              definitionally from both endpoints
    Iff midpoint              target has form P ↔ Q; candidate is a proposition and differs definitionally
                              from P and Q
    Existential witness       target has form ∃x : τ, P (x); candidate has type τ
    Raw Lean candidate        accepted only through the explicitly enabled experimental path, with indepen-
                              dent candidate count, source-size, syntax, and heartbeat limits
        Table 3: Target-specific proposal checks before an object can influence verified search.


instantiated proposition as a proof obligation. The trust boundary is therefore defined by Lean
elaboration and final kernel checking, not by model confidence or proposal syntax.

J     Knowledge Objects and Workspace Deltas
In addition to proof states, the workspace stores typed intermediate objects. An object records an
identifier, conjecture kind, expression, optional type, blockers, utility, dependencies, knowledge
status, origin, and display text. Supported kinds include helper lemma, equality bridge, iff bridge,
witness, invariant, generalization, and term. Status is one of verified, pending, speculative, refuted, or
dominated.
A planner thought batch enters the workspace as speculative objects. Each thought is absorbed
independently so one malformed or later-refuted object does not invalidate unrelated proposals.
After elaboration or proof construction, the object’s status can be upgraded to verified or changed to
refuted. Duplicate objects are merged by kind, expression, and optional type, preserving the stronger
knowledge status.
The workspace is versioned. A delta between versions can list newly added nodes, transitions,
verified/refuted objects, and structured observations. This versioning provides a natural event
boundary for sparse neural intervention: the planner does not need the full historical token sequence
to know what changed since its previous call.

K      Failure Taxonomy and Structured Feedback
Failed search is represented explicitly. The current failure classes include type mismatch, unification
failure, no progress, branch growth, branch explosion, timeout, unsafe syntax, rewrite mismatch,
premise mismatch, open goals, invalid planner selection, budget denial, internal failure, and an
unknown fallback. A structured observation links the failure class to an optional transition, transition
outcome, newly reached nodes, elapsed time, and a bounded debug field.
This distinction matters for both scheduling and training data. A timeout indicates that an operation
exceeded a resource boundary; a type mismatch indicates semantic incompatibility; branch explosion
indicates unfavorable search geometry; and budget denial means the proposal was never executed.
Collapsing all four into a single negative reward would erase information that can guide later region
selection or curriculum construction.

L     Matched-Compute Benchmark Instrumentation
The repository contains a matched-compute benchmark interface with eight modes. All modes inherit
the same wall-clock and Atlas work caps from a common base configuration, while the target feature
is toggled:
 1. native-only: bounded native solver without the symbolic frontier or Atlas graph;
 2. symbolic-actions: symbolic actions without frontier or graph persistence;
 3. flat-frontier: frontier exposure with deterministic replay and no Atlas graph;


                                                     13
 4. graph-atlas: model-free frontier plus persistent graph;
 5. atlas-policy: graph plus deterministic policy-style guidance;
 6. atlas-policy-value: planner-style policy/value signal without expansion requests;
 7. planner-expansion: planner-guided region expansion under the same outer budget;
 8. interactive-raw: interactive path with the explicitly enabled raw Lean compatibility gate.
Each case emits a vialean.benchmark.v3 record containing solved status, elapsed milliseconds,
direct and proposal attempts, bridge depth, model calls, replan count, Atlas nodes, Atlas transitions,
and Atlas Meta operations. These measurements make it possible to separate accuracy gains from
simple increases in symbolic work or provider calls.
For the paper-level system analysis, the most informative matched-compute contrasts are flat frontier
versus graph Atlas, and graph Atlas versus full future/synthesis search. Useful secondary statistics
are transposition count, unique semantic states per solved case, successful transition depth, and
time-to-proof quantiles. No additional empirical numbers are inserted here; the reported miniF2F
result in the main text remains the manuscript’s measured result.

M     Training and Analysis Traces
The training trace schema is intentionally different from a raw proof transcript.                    A
vialean.training.v3 event contains a sequence number, event kind, workspace version, and
a JSON payload. The writer is deterministic and caps the number of serialized events. Callers are
expected to record stable identifiers, counts, and scores; raw goals, local names, provider credentials,
and source-level proof text are excluded from this trace format.
This event design supports process analysis without making the trace itself part of the trusted proof
artifact. For example, a training pipeline can correlate a planner intervention with later node growth,
solved transitions, bridge depth, or failure classes while the final proof remains an ordinary Lean
term checked independently of the trace.

N    Reproducibility and Evaluation Boundary
The manuscript’s miniF2F evaluation covers the complete 244-problem test split used in the original
experiment. The theorem-answer declarations are excluded and retrieval of the target theorem is
disabled. Each successful case must terminate in a complete Lean proof term accepted by the kernel.
The reported pass@1 value is therefore 122/244 = 50.0%, exactly as in the original empirical result.
ViaLean’s standalone core uses ordinary Lean 4 metaprogramming APIs. Mathlib support is isolated
in the integration project, which supplies the benchmark adapter and bounded leaf portfolio. The
search controller uses one shared deadline across frontier expansion, local synthesis, leaf solving,
recursive execution, and optional provider interaction. Proof states are keyed by the strict semantic
identity in Appendix A, with structural equality confirmation after hash lookup.

Suggested reproduction record. For each test theorem, a reproducible run should store the
repository revision, Lean and mathlib revisions, complete configuration, timeout, solved status,
elapsed time, Atlas node/transition/Meta-op counts, and the final proof term or replayable proof
script. For any model-enabled variant, the provider/model identifier, decoding parameters, request
cap, model-call count, and replay data should also be retained.

O    Baseline Comparability
Table 1 preserves the settings reported by each source. Lean tidy and ViaLean are pass@1 Lean
searches from different toolchain generations. The reported grind number is a direct Lean tactic
reference point. Sledgehammer is evaluated in Isabelle. Dafny uses an auto-active verifier and SMT
backend over a translated miniF2F benchmark. The learned rows use larger pass@k or search budgets.
The table therefore provides empirical context along symbolic-automation and learned-guidance axes
while retaining the distinctions among proof environments and inference budgets.


                                                  14
P    Implementation Map
The technical components described above correspond directly to modules in the public implementa-
tion:

    Module                             Primary responsibility
    GoalKey.lean                       alpha-stable strict proof-state identity and collision-safe strict
                                       goal set
    Symbolic.lean                      common strategy-family and symbolic-operation intermediate
                                       representation
    Atlas/Types.lean                   nodes, transitions, evidence, regions, limits, transpositions, and
                                       structural potential
    Workspace.lean                     versioned persistent Atlas, typed objects, observations, deltas,
                                       and failure classes
    Frontier.lean                      perspective probes, bounded future graph, breadth-first expansion,
                                       and preview transactions
    Synthesis/Local.lean               exact inhabitants and typed partial local applications
    Model/Protocol.lean                policy, interactive, and planner schemas with deterministic pay-
                                       load caps
    Validate.lean                      common and target-specific validation for cuts, bridges, and wit-
                                       nesses
    Search/Controller.lean             shared cancellation deadline over the complete search
    Benchmark.lean                     matched-compute modes and vialean.benchmark.v3 records
    Trace.lean                         deterministic redacted vialean.training.v3 event stream
               Table 4: Implementation correspondence for the technical appendix.


The central design invariant across these modules is that search memory may be rich, persistent, and
model-facing, while proof acceptance remains narrow: a result is returned only when Lean has a
complete, well-typed term for the original target with no unresolved synthetic metavariables.




                                                  15
