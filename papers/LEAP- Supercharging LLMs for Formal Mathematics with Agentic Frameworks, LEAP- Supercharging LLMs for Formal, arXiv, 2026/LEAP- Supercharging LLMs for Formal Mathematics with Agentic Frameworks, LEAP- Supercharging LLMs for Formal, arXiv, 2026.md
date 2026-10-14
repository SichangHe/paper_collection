                                                                                                                                             2026-06-01



                                        LEAP: Supercharging LLMs for Formal
                                        Mathematics with Agentic Frameworks
                                        Po-Nien Kung1 , Linfeng Song2 , Dawsen Hwang3 , Jinsung Yoon1 , Chun-Liang Li1 , Simone Severini2 , Mirek
                                        Olšák3 , Edward Lockhart3 , Quoc V Le3 , Burak Gokturk1 , Thang Luong3 , Tomas Pfister1 and Nanyun Peng1
                                        1 Google Cloud AI Research, 2 Google Cloud, 3 Google DeepMind




                                        Large Language Models (LLMs) exhibit strong informal mathematical reasoning but struggle to generate
                                        mechanically verifiable proofs in formal languages like Lean. We present LEAP (LLM-in-Lean Environ-
                                        ment Agentic Prover), an agentic framework that enables general-purpose foundation models to achieve
                                        state-of-the-art performance on automated formal theorem proving. LEAP leverages foundation model
arXiv:2606.03303v2 [cs.AI] 3 Jun 2026




                                        capabilities, such as informal reasoning, instruction following, and iterative self-refinement. By decom-
                                        posing complex problems into smaller units, the system bridges formal proof construction with informal
                                        blueprints through continuous interaction with the Lean compiler. To provide a rigorous evaluation be-
                                        yond increasingly saturated benchmarks, we introduce Lean-IMO-Bench, a benchmark of IMO-style prob-
                                        lems formalized in Lean, with short statements yet highly non-routine and multi-step proofs across a wide
                                        range of difficulty levels. Empirically, on the latest 2025 Putnam Competition, an annual mathematics
                                        competition for undergraduate students in North America, LEAP solves all 12 problems, matching recent
                                        breakthroughs by frontier formal mathematical models; On Lean-IMO-Bench, LEAP boosts the one-shot
                                        formal solve rate of general-purpose LLMs from below 10% to 70%, notably surpassing the 48% bench-
                                        mark set by a specialized, gold-medal-caliber IMO system. Furthermore, we demonstrate LEAP’s research-
                                        level utility by autonomously formalizing complex proofs for open combinatorial challenges, including a
                                        verified proof for a key subproblem in Knuth’s Hamiltonian decomposition of even-order Cayley graphs.


                                        1. Introduction
                                        Large Language Models (LLMs) have made impressive progress on mathematical reasoning with
                                        natural language, also known as “informal math reasoning”, demonstrating strong capabilities in
                                        complex reasoning and problem-solving for both math competitions and research level maths (Feng
                                        et al., 2026a,b,c; Huang and Yang, 2025; Luong and Lockhart, 2025). However, as discussed in recent
                                        works like Hilbert (Varambally et al., 2025) and Goedel-Prover-V2 (Lin et al., 2026), solutions in
                                        natural language frequently suffer from logical fallacies and hallucinations, and they are hard to
                                        automatically verify. This difficulty in verification is not merely a limitation of automated systems;
                                        even for human mathematicians, verifying complex proofs is a notoriously time-consuming process
                                        requiring scarce expert labor (Greiffenhagen, 2024). A famous example is the proof of the Kepler
                                        conjecture (Hales, 2005), which required four years of peer review before the referees could only
                                        claim to be “99% certain” of its correctness,1 eventually necessitating a decade-long formal verification
                                        effort (Hales et al., 2017). This verification bottleneck underscores that assessing correctness is a
                                        hard task in natural language, motivating the exploration of formal mathematics, where proofs are
                                        written in a machine-checkable language and verified by a rigorous kernel like in Lean (Moura and
                                        Ullrich, 2021), Isabelle (Nipkow et al., 2002), Coq (Huet et al., 1997), HOL Light (Harrison, 2009),
                                        offers automated verification with guaranteed accuracy. Yet, bridging the gap to formal theorem
                                        proving remains a significant challenge, and the performance of automated formal provers currently
                                        lags substantially behind that of general-purpose LLMs operating in natural language.
                                           1 https://en.wikipedia.org/wiki/Kepler_conjecture




                                        Corresponding author(s): ponienkung@google.com
                                        © 2026 Google. All rights reserved
                         LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



    To bridge this gap, recent efforts in the research community predominantly fine-tunes specialized
prover models (e.g., AlphaProof (Hubert et al., 2026), DeepSeek Prover V2 (Ren et al., 2025), Seed
Prover (Chen et al., 2025b), Goedel Prover V2 (Lin et al., 2026)) on formal corpora, with the
assumption that general LLMs are ineffective for rigorous formal tasks without specialization. Indeed,
according to the FormalProof Bench (Ravi et al., 2026)2 and TaoBench (Taylor et al., 2026), general
LLMs often underperform compared to specialized prover models.
    While some recent works explored agentic or inference-time search, they still depend on specialized
models. For instance, Hilbert (Varambally et al., 2025), AlphaProof Nexus (Tsoukalas et al., 2026),
Aristotle (Achim et al., 2025), and Seed Prover V1.5 (Chen et al., 2025a) use general LLMs for
informal reasoning but rely on specialized models for Lean proving steps. Axiom3 and Numina4 claim
strong results on Putnam 2025 while remained closed source without public access, making them
scientifically unverifiable.
    In this paper, we show that while general LLMs remain limited in one-shot theorem proving, the
bottleneck is not language comprehension but generating long, complex, correct proofs in one attempt.
General LLMs offer complementary skills to specialized models: strong informal reasoning, instruction
following, tool use, and self-refinement. These make them ideal for agentic ATP frameworks, where
proof construction is decomposed and iteratively improved. To this end, we introduce LEAP (LLM-
in-Lean Environment Agentic Prover), an agentic framework using only general LLMs for formal
math. Inspired by human workflow, LEAP generates a high-level blueprint forming a directed acyclic
graph (DAG), then generates the Lean proof, iteratively correcting errors via compiler feedback.
    To evaluate progress beyond saturated benchmarks such as MiniF2F (Zheng et al., 2022) and
PutnamBench (Tsoukalas et al., 2024), we introduce Lean-IMO-Bench, formalizing the challenging
informal math benchmark IMO-Bench (Luong et al., 2025) problem statements into Lean. In contrast
to existing benchmarks, which either focus on shorter problems or emphasize broad undergraduate
coverage, Lean-IMO-Bench targets the complementary regime of elementary statements whose solu-
tions often hinge on highly non-routine insights and unfold through long, multi-step, and structurally
intricate proofs, providing a sharper test of formal theorem proving.
    Empirically, on the latest 2025 Putnam Competition, a challenging annual undergraduate mathe-
matics competition in North America whose 2025 top score was 110 out of 120 while the median
was only 2, LEAP solves all 12 problems in Lean, achieving perfect performance. This matches
recent breakthrough results from frontier formal mathematical reasoning models such as Axiom3 and
Numina4 . On Lean-IMO-Bench, LEAP substantially improves general LLMs’ solve rate from under
10% to 70%, surpassing specialized ATP models (5%) and Aristotle (48%), a strong system with
specialized ATP components that earned the score for Gold medal at IMO 2025. The contribution of
the paper is three-fold:

   • Workflow-Inspired Agentic Design We introduce LEAP, an agentic framework that codifies
     the human mathematical workflow – combining high-level blueprint sketching with low-level
     formal proof generation and iterative compiler feedback. Crucially, LEAP demonstrates that
     state-of-the-art formal theorem proving can be achieved using only general-purpose LLMs,
     challenging the belief that specialized fine-tuning is indispensable.
   • Lean-IMO-Bench Dataset: To evaluate progress beyond saturated benchmarks such as MiniF2F
     and PutnamBench, we introduce Lean-IMO-Bench, a new challenging dataset that translates
   2 The paper is associated with a private dataset with a live leaderboard https://www.vals.ai/benchmarks/proof

_bench. We contacted them several times to participate on the leaderboard without receiving a response.
  3 https://github.com/AxiomMath/putnam2025
  4 https://github.com/project-numina/Numina-Putnam2025




                                                                                                              2
                                LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



     informal problem statements from IMO-Bench into formal Lean statements. Resources are
     available at https://imobench.github.io.
   • Strong Empirical Results and Insights: LEAP solves all 12 problems on Putnam 2025
     and achieves a large improvement over prior baselines on Lean-IMO-Bench. Our analy-
     sis suggests that the primary bottleneck in formal mathematics for general-purpose LLMs
     is not formal language comprehension alone, but the lack of structured, iterative interac-
     tion with the proof environment. The Lean solutions generated by LEAP are available at
     https://github.com/google-deepmind/superhuman/tree/main/leap.


2. LEAP: Blueprint-Driven Automated Theorem Proving

2.1. Formalizing Proofs with Blueprints

Formalizing mathematical proofs is rarely a one-shot task: it requires a structured plan for progressively
translating a high-level argument into Lean. To manage this complexity, recent formalization efforts
often use the Lean Blueprint tool 5 , which let mathematicians write a human-readable proof roadmap
linked to Lean code and visualized as a directed acyclic graph (DAG), where each node represents a
proof obligation. This workflow has been instrumental in coordinating large-scale projects such as
the formalization roadmap for Fermat’s Last Theorem 6 , where a multi-year proof effort is organized
through an explicit dependency graph.
    Inspired by this workflow, we introduce LEAP, an agent for automated theorem proving with
hierarchical decomposition and planning. Rather than synthesizing a complete proof in a single pass,
LEAP incrementally drafts blueprints, decomposes Lean goals into supporting lemmas, and maintains
the evolving proof plan as an AND-OR DAG.


  PROBLEM        STATE READER              DIRECT FORMALIZATION                            BLUEPRINT GENERATION

                                          NL PROVER             FORMAL PROVER        BLUEPRINT GEN.        SKETCH GEN.
         AND-OR DAG
                                                                                                                            REWRITE
                                            INFORMAL                  FORMAL             INFORMAL             FORMAL
                                            PROOF                     PROOF              BLUEPRINT            SKETCH
            OR     AND




                                        Lean        VERIFIER (LEAN)                  REVIEWER (LLM)       VERIFIER (LEAN)
                                        Search
                                                                         FAILED                                              Lean
                                                 PROVED                               FAILED (MSG)                           Search
                                                                      → DECOMPOSE         SUCCESS
            ACCEPT       REJECT                                                     (SKETCH, SUBGOALS)
                                       REWRITE            REVISER                                             REVISER
                 STATE WRITER
     T



Figure 1 | LEAP workflow. LEAP first attempts direct formalization with compiler-feedback revision
and LeanSearch(Gao et al., 2024) retrieval. If this fails, it generates an informal blueprint and formal
proof sketch, adding verified subgoals back to the DAG only when dependencies remain acyclic.

  5 https://github.com/PatrickMassot/leanblueprint
  6 https://leanprover-community.github.io/blog/posts/FLT-announcement/




                                                                                                                                      3
                        LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



2.2. Overview

Figure 1 illustrates the workflow of LEAP. Given an input theorem, LEAP registers its Lean statement
as the root goal, 7 represented as an OR node in the AND-OR DAG. To process an open goal, a state
reader retrieves its statement, dependencies, and related lemmas. LEAP then first attempts a direct
proof by generating an informal proof, translating it into Lean code, and checking the candidate with
the Lean compiler.
    If direct proving fails, LEAP shifts to decomposition. It first drafts an informal blueprint that
proposes intermediate lemmas, then translates the blueprint into a Lean proof sketch. The sketch
proves the current goal assuming only the proposed lemmas: the main theorem body is sorry-free,
while sorry placeholders are permitted only in the newly proposed lemma statements. If the sketch
is accepted by the Lean compiler, it is added as an AND node, and the proposed lemmas are added as
child OR nodes. This ensures that once all child subgoals are proved, the parent goal is also proved.
The verified sketch is then passed to the state writer, which checks that the update preserves acyclicity
before committing it to the DAG. The agent then recursively processes the newly created subgoals.
    This workflow relies on three tightly coupled design choices: DAG-based hierarchical memoiza-
tion, which preserves progress and reuses lemmas across branches; interleaved informal-formal plan-
ning, which connects natural-language strategies with executable Lean code; and verification-guided
proof search, which uses compiler feedback and LLM-based review to accept, revise, decompose,
or abandon candidate branches.


2.3. Hierarchical Memoization via DAG

LEAP uses the AND-OR DAG not only to record proof progress, but also to structure hierarchical
memoization. OR nodes represent open goals or lemma statements, each of which may be resolved
by any valid proof strategy, while AND nodes represent candidate decompositions whose success
depends on proving all constituent subgoals. Figure 2 illustrates this structure.
    The DAG provides two central advantages. First, monotone refinement: once a goal is decom-
posed into supporting subgoals, subsequent search can focus on expanding and resolving these
descendants without restructuring the established dependency order. This separates local proof
exploration from global proof organization: individual proof attempts may be revised, expanded, or
abandoned, while the DAG preserves the stable dependency structure of the overall proof plan. Second,
lemma memoization: intermediate lemma statements are stored as shared proof nodes and can be
reused whenever the same subproblem arises in different branches. This also supports anticipatory
lemma planning: during blueprint generation, LEAP may propose auxiliary lemma statements that are
not immediately required by the current sketch but could support later proof steps. Such prospective
lemmas remain available in the graph memory without being necessary for resolving the current AND
node. Together, these properties allow independent proof plans to converge on common dependencies
while reducing redundant derivations.
   The resulting dependency structure also improves transparency: it exposes which goals remain
open, which lemmas have been resolved, and which nodes block downstream progress. This helps
LEAP identify where additional lemmas, revised decompositions, or stronger assumptions may be
needed, while providing an interpretable blueprint-style workspace for human-AI collaboration.
  7 A goal is any theorem or lemma statement to be proved; decomposition introduces subgoals. See Appendix C.




                                                                                                                4
                      LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



2.4. Interleaved Informal–Formal Planning

As shown in Figure 1, both the direct proof path and the blueprint decomposition path in LEAP pass
through an informal proof sketch. This reflects the complementary strengths of LLMs and Lean: LLMs
are effective at informal reasoning, strategy generation, and refinement, while Lean provides strict
machine-checkable verification.
     In direct proving, LEAP first generates an informal argument for the current goal before translating
it into a candidate Lean proof. In decomposition, it drafts an informal blueprint explaining how
the goal can be reduced to supporting subgoals, then converts this plan into a Lean sketch that
records the proposed dependencies. In both cases, the informal sketch provides a planning space
before formalization, making proof construction less brittle than direct code generation alone (see
Appendix C for examples of informal proofs and blueprints).
    This interleaving also makes proof progress more interpretable: each formal attempt is paired
with an informal rationale, allowing users to inspect why a proof step or decomposition was proposed
rather than only reading Lean code or compiler feedback.


2.5. Verification-Guided Proof Search

As shown in Figure 1, LEAP uses verification at two levels. First, the Lean compiler formally checks
candidate proofs and sketches, ensuring that accepted code is syntactically valid and type-correct.
For proof sketches, LEAP only permits sorry placeholders for the proposed subgoals (lemmas). This
preserves the AND-OR semantics of the proof DAG: once all referenced subgoals are proved, the parent
goal is also proved. Second, after a blueprint proposes new subgoals, an LLM reviewer assesses the
quality of the decomposition: whether the subgoals are relevant to the parent goal, make the problem
easier, and offer a plausible route to completing the proof. This planning-level review is crucial for
complex goals, where a Lean sketch can be syntactically valid while introducing subgoals that are
ill-posed or no simpler than the original statement. Without this filter, the agent may repeatedly
expand weak blueprints, spending search budget on branches that do not make real progress. We
study this failure mode through an ablation without the LLM reviewer in subsection 5.3.
    The LLM reviewer therefore acts as a search filter: it identifies unpromising decompositions,
triggers backtracking, and encourages exploration of alternative strategies. Currently, LEAP uses a
simple DFS over the DAG with backtracking. The effectiveness of this reviewer suggests a broader
future direction: LLMs may also serve as heuristic evaluators for guiding search in formal proof spaces.




Figure 2 | DAG example for Putnam 2025 Problem A6. LEAP decomposes the theorem into a proof
sketch and supporting lemmas. Through anticipatory lemma planning, the agent may also propose
auxiliary lemma statements that are not immediately required but could be useful later; these are
shown with dashed edges and are not needed to prove the main theorem. Green nodes are proven
nodes, and brown blocks denote definitions, structures, or variables introduced at a node.



                                                                                                       5
                     LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



3. Lean-IMO-Bench: Formalizing IMO Problems in Lean

Table 1 | Baseline performance on Lean-IMO-Bench across three evaluation tasks. Natural Language
Proof performance is based on human expert review.

      Task                         Model (Metric)                     Basic Set (%)      Advanced Set (%)
      Natural Language Proof       Gemini 2.5 Pro (Pass@1)                 55.2                17.6
      Formal Theorem Proving       Gemini 3.1 Pro (Pass@128)               20.0                3.3
                                   Gemini 3.1 Pro (Avg.@128)               4.6                 0.2
      Formal Proof Translation     Gemini 3.1 Pro (Pass@128)               20.0                3.3
                                   Gemini 3.1 Pro (Avg.@128)               4.6                 0.8



3.1. Lean-IMO-Bench

We introduce Lean-IMO-Bench, a curated collection of 60 problems building upon the foundational
work of Luong et al. (2025). Luong et al. (2025) introduced IMO-ProofBench, a rigorous suite
vetted by an expert panel of mathematicians and IMO medalists. The benchmark contains 60 problems
split evenly into a Basic set and an Advanced set of 30 problems each. The Basic set spans pre-IMO to
IMO-Medium difficulty and includes 8 algebra, 8 combinatorics, 8 number theory, and 6 geometry
problems. The Advanced set includes novel problems up to IMO-Hard difficulty, with 8 algebra, 8
combinatorics, 6 number theory, and 8 geometry problems. Overall, the benchmark is approximately
balanced across algebra, combinatorics, geometry, and number theory.
    To ensure the highest level of accuracy in Lean-IMO-Bench, Lean experts manually formalized
and verified all 60 problem statements. Because these problems are at the IMO level, the required
mathematical background is elementary. Consequently, we expect the corresponding Lean solutions
to be concise, deliberately removing the overhead associated with formalizing complex, modern
mathematical theories.
    The dataset can be used to evaluate models across three distinct tasks: Natural Language Proof,
Formal Theorem Proving, and Formal Proof Translation, while we focus on formal theorem proving
in this paper. The baseline performance on Lean-IMO-Bench is summarized in Table 1. For the
Natural Language Proof task, we cite Luong et al. (2025) as reference: Gemini 2.5 Pro shows strong
informal reasoning performance. However, as shown in Table 1, this does not directly translate to
formal theorem proving: Gemini 3.1 Pro performs substantially worse on Formal Theorem Proving,
especially on the Advanced set. Providing a correct informal proof in the Formal Proof Translation task
also yields little improvement, with Pass@128 unchanged and only a marginal gain in Average@128.
   Table 1 demonstrates a stark gap in the models’ Lean capabilities. Because the model can already
successfully solve these problems in natural language, mathematical reasoning is not the bottleneck,
thus reliably generating valid Lean code remains the primary challenge.


4. Experimental Results
We evaluate LEAP with Gemini-3.1-pro as the backend large language model and compare it against
four baselines: Gemini-3.1-pro, which tests one-shot proof generation by a strong general-purpose
model; Goedel-Prover-V2-32B (Lin et al., 2026), a state-of-the-art open-source ATP model specialized
for Lean; Hilbert (Varambally et al., 2025), an agentic Lean formalization framework that combines
Goedel-Prover-V2-32B with Gemini-3.1-pro; and Aristotle (Achim et al., 2025), a specialized au-

                                                                                                            6
                          LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



tomated theorem-proving system with dedicated ATP components that achieved gold-medal-level
performance at the 2025 IMO.
    We evaluate formal proving ability on two datasets: Putnam 2025 and our proposed Lean-IMO-
Bench. Putnam 2025 contains twelve undergraduate-level problems from the 86th William Lowell
Putnam Mathematical Competition,8 a highly challenging North American mathematics competition.
In the 2025 competition, the top score was 110 out of 120, the average score was approximately 10,
and the median score was 2.


4.1. Results on Putnam 2025

Table 2 presents the evaluation results on the Putnam 2025 benchmark. Under a Pass@128 setting, the
direct formalization baselines (Gemini-3.1-pro and Goedel-Prover-V2-32B) fail to solve any problems,
indicating that single-pass generation is insufficient for the logical complexity of this dataset.

Table 2 | Putnam 2025 results. Green checkmarks (✓) indicate successfully solved problems, while red
crosses (×) indicate failures. Evaluation settings: ⋄ indicates pass@128, while † indicates rollout=2.

 Method                        a1    a2    a3    a4    a5     a6    b1    b2    b3    b4    b5      b6   Solve Rate (%)
 Gemini-3.1-pro⋄               ×     ×     ×      ×      ×    ×     ×     ×     ×      ×     ×      ×           0.0
 Goedel-Prover-V2-32B⋄         ×     ×     ×      ×      ×    ×     ×     ×     ×      ×     ×      ×           0.0
 Hilbert†                      ×     ✓     ✓      ✓      ×    ×     ×     ×     ×      ×     ×      ✓          33.3
 Aristotle†                    ✓     ✓     ✓      ✓      ×    ✓     ✓     ✓     ✓      ✓     ×      ×          75.0
 LEAP†                         ✓     ✓     ✓      ✓      ✓    ✓     ✓     ✓     ✓      ✓     ✓      ✓         100.0

    The open-source agentic framework Hilbert improves upon direct generation, solving 4 out of 12
problems. However, during evaluation, we observed that Hilbert’s recursive search design leads to an
exponential time complexity of O (( 𝑛 · 𝑏) 𝑑 ), where 𝑛 is the number of lemma retries, 𝑏 is the average
branching factor, and 𝑑 = 10 is the maximum proof depth. Due to the high volume of redundant LLM
calls required by this approach, we bounded each Hilbert rollout to a 7-day time limit. For context
against state-of-the-art proprietary systems, we also report the performance of Aristotle. While the
system is closed-source, it serves as a strong baseline, solving 9 out of 12 problems given two rollouts.9
    LEAP successfully solves all 12 Putnam 2025 problems, improving the benchmark solve rate from
0% via direct formalization to 100% with our agentic framework. This performance directly results
from the LEAP’s blueprint-inspired AND-OR DAG architecture, which resolves the search bottlenecks
observed in standard recursive frameworks like Hilbert. By supporting hierarchical memoization,
LEAP allows independent proof branches to reuse shared intermediate lemmas, significantly mitigating
exponential search complexity and allow LEAP to solve problems efficiently. For a detailed, problem-
level breakdown of the computational cost and search efficiency required to achieve these results,
See Table 3 for runtime and efficiency statistics.


4.2. Results on Lean-IMO-Bench

Table 4 presents evaluation results on Lean-IMO-Bench. We include this dataset to test model
robustness across a broader spectrum of mathematical disciplines and distinct complexity tiers,
providing a complementary challenge to the Putnam benchmark.
   8 Mathematical Association of America, Results of the 86th William Lowell Putnam Mathematical Competition.
   9 An unofficial report indicates Aristotle solved 10 out of 12 problems on this benchmark; however, neither that reported

run nor our evaluation successfully solved problem A5.


                                                                                                                          7
                         LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



Table 3 | Runtime and search efficiency of LEAP on Putnam 2025. For each problem, we report
the computational cost (total LLM calls for a verified proof), the search space explored (active DAG
nodes/lemmas), and the final Lean proof line count.

 Metric            a1       a2       a3      a4        a5      a6       b1       b2       b3       b4    b5       b6
 LLM Calls          71     304      963     1.4k       3.0k   1.0k     116       46      98         87   239      161
 Active Nodes        8      26       55     105        170     62       12        8       10         9   211       24
 Proof Length      405     591      713     1.0k       2.0k   581      752      300      326       556   1.9k     848


     Direct formalization baselines (Gemini-3.1-Pro and Goedel-Prover-V2-32B) and the open-source
Hilbert framework struggle significantly on this dataset, exhibiting severe performance degradation
on the Advanced set. While the proprietary Aristotle system resolves a majority of the Basic problems,
its effectiveness drops sharply as complexity increases. Notably, across all evaluated methods, perfor-
mance in the Geometry category remains near zero. This aligns with the well-established difficulty
of formalizing olympiad-level geometry in Lean without the aid of supplementary, domain-specific
frameworks. We retain this category strictly to evaluate general-purpose reasoning under extreme
formalization constraints.
    Against these baselines, LEAP achieves the highest overall solve rates, scoring 83.3% on the Basic
set and 56.7% on the Advanced set. By effectively leveraging its DAG-based architecture, LEAP
demonstrates strong domain generalization, maintaining a 100% solve rate in both Algebra and
Number Theory regardless of the difficulty tier.

Table 4 | Results on Lean-IMO-Bench. We report the solve rate (%) across different mathematical
categories for the Basic and Advanced sets separately. Evaluation settings: ⋄ indicates pass@128,
while † indicates rollout=2. Best results in each section are in bold.

 Method                   Algebra              Comb.           Num. Theory            Geometry           Overall
                                                    Basic Set (%)
 Gemini-3.1-Pro⋄            37.5                12.5                 25.0                 0                20.0
 Goedel-V2-32B⋄             37.5                  0                   0                   0                10.0
 Hilbert†                   62.5                 25                   50                  0                36.6
 Aristotle†                  75                 100                  100                 16.7              76.7
 LEAP†                      100                 100                  100                 16.7              83.3
                                                  Advanced Set (%)
 Gemini-3.1-Pro⋄             0                  12.5                  0                   0                 3.3
 Goedel-V2-32B⋄              0                    0                   0                   0                  0
 Hilbert†                   12.5                  0                  16.6                 0                 6.6
 Aristotle†                 37.5                12.5                 33.3                 0                20.0
 LEAP†                      100                  25                  100                 12.5              56.7



5. Discussion

5.1. Beyond One-Shot Formalization

A central motivation of LEAP is that general foundation models can be effective iterative formalizers,
even when they are not specialized Lean provers. While specialized provers are trained for formal proof
synthesis, general models offer complementary capabilities such as instruction following, long-context
reasoning, informal planning, tool use, and feedback-based revision.

                                                                                                                        8
                      LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



    To isolate this effect, we evaluate the Direct Formalization component labeled in Figure 1 under two
settings. In the one-shot setting, each model is evaluated with Pass@128 over independently sampled
proof attempts. In the iterative setting, each model receives a single initial attempt and up to 20
compiler-feedback revision steps, yielding a Pass@1 result under a smaller sampling budget. As shown
in Table 5, Goedel-Prover-V2-32B does not benefit from this feedback loop, while Gemini-3.1-pro
improves substantially from 20.0% to 36.6%.
    This suggests that iterative formalization depends on capabilities beyond local Lean proof synthesis.
Interpreting compiler errors, maintaining context, and revising proof attempts over multiple steps can
be as important as one-shot formal proving accuracy. These results support using a general foundation
model as the reasoning backbone of LEAP, while leaving open the possibility of combining it with
specialized provers for local proof generation.

Table 5 | One-shot vs. iterative formalization performance on Lean-IMO-Bench Basic set.

                  Model                       One-shot (Pass@128)             Iterative (Pass@1)
                  Goedel-Prover-V2-32B                    10.0                       6.6
                  Gemini-3.1-Pro                          20.0                      36.6



5.2. Effect of DAG-Based Memoization

LEAP maintains proof progress as a DAG-based memory rather than an isolated decomposition tree.
This allows intermediate lemmas to be stored as shared nodes and reused across branches, while
exposing graph context such as existing goals, dependencies, and previously proposed lemmas.
    To evaluate this design, we compare LEAP with a tree-structured variant that follows the same
workflow but removes global lemma sharing. As shown in Table 6, the tree variant already substantially
outperforms Hilbert (Varambally et al., 2025), which achieves 36.6% and 6.6% on the Basic and
Advanced sets, respectively (Table 4). This indicates that interleaved informal–formal planning and
verification-guided search are effective even without DAG-based memoization. The full DAG version
further improves performance from 73.3% to 83.3% on the Basic set and from 40.0% to 56.7% on
the Advanced set, showing the benefit of global proof memory.
    The improvement is especially pronounced on harder categories, such as Advanced Algebra and
Advanced Number Theory, where shared lemmas and graph context are more likely to matter. We
attribute this gain to two effects. First, the DAG supports anticipatory lemma planning: auxiliary
lemmas proposed at higher-level nodes can later be reused by downstream subgoals (Figure 2).
Second, repeated subproblems can be shared across branches, avoiding the need to rediscover or
reprove the same lemma multiple times. Together, these properties reduce redundant derivations and
improve proof search efficiency.

Table 6 | DAG memoization ablation. Solve rate (%) by category on Lean-IMO-Bench Basic
(B)/Advanced (A) sets.

                                           Alg.      Comb.           NT          Geo.      Overall
               Config.
                                          B     A     B     A    B        A     B    A     B       A
               w/o DAG (Naive Tree) 100 75 75 25 100 66.6 0      0 73.3 40.0
               Full DAG             100 100 100 25 100 100 16.7 12.5 83.3 56.7




                                                                                                       9
                     LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



-- Grandparent goal
theorem perms_a_equiv_b_card
  (m : ℕ) (s : Fin (m + 1) → ℤ× ) (k : Fin (m + 2)) :
  Nat.card (PermsA m s k) = Nat.card (PermsB m s k) := by
  rw [← card_perms_a_eq m s k, ← card_perms_b_eq m s k]
  exact valid_perms_end_eq_sigma_card m s k

-- Intermediate lemma (unfolding the definitions)
lemma valid_perms_end_eq_sigma_card
  (m : ℕ) (s : Fin (m + 1) → ℤ× ) (k : Fin (m + 2)) :
  (ValidPermsEnd (m + 1) s k).card = (Finset.sigma ...).card := by
  rw [card_perms_a_eq m s k, card_perms_b_eq m s k]
  exact card_perms_a_eq_card_perms_b m s k

-- Proposed subgoal (syntactically identical to the grandparent goal)
lemma card_perms_a_eq_card_perms_b
  (m : ℕ) (s : Fin (m + 1) → ℤ× ) (k : Fin (m + 2)) :
  Nat.card (PermsA m s k) = Nat.card (PermsB m s k) := by sorry

Figure 3 | Unproductive decomposition without LLM review. The proposed subgoal restates the
grandparent goal, so the decomposition is formally admissible but does not simplify proof search.

5.3. Toward LLM-Guided Proof Search

Compiler verification checks whether a proof sketch is formally well-typed, but not whether its
decomposition is useful. A sketch may prove the parent goal from proposed lemmas that are unhelpful,
overly difficult, or nearly equivalent to the original goal. In LEAP, the LLM reviewer acts as a local
search heuristic: it filters candidate decompositions by judging whether they meaningfully simplify
the parent goal before they are committed to the DAG.
     We focus this ablation on Putnam 2025 Problem A5 because it is one of the most challenging cases
in our evaluation, requiring the longest runtime and two rollouts for LEAP to formalize the proof
successfully. Removing the LLM-based decomposition reviewer causes the agent to fail even after
eight rollout attempts. This contrast suggests that local LLM review provides a useful search signal:
it rejects weak decompositions early, triggers backtracking, and prevents the agent from spending
rollouts on branches that do not make substantive progress. We further inspect decomposition traces
from the ablated setting; a representative failure case is shown in Figure 3. The decomposition
is formally admissible but does not simplify the mathematical state. The agent first unfolds the
definitions in the grandparent goal to create an intermediate lemma, then folds them back into a
proposed subgoal that is syntactically identical to the original statement. Without semantic review,
this duplicate lemma is treated as a new step, causing the agent to repeat the same unproductive
decomposition until its search budget is exhausted. This failure highlights the potential of LLM-guided
proof search: a reviewer can assess whether a proposed lemma actually advances the proof, prune
cyclic or non-simplifying branches, and direct compute toward more promising paths.


5.4. Perspective: General LLMs as Formal Provers: From Zero to Hero

As demonstrated by LEAP, the seemingly insurmountable gap between the poor one-shot theorem
proving performance of general LLMs and state-of-the-art results can be effectively bridged by a well-
designed agentic framework. By shifting the paradigm away from relying solely on small specialized
LLMs, we show that the extensive knowledge, instruction following, and self-correction capabilities of
foundation models are more than sufficient. When scaffolded correctly, these foundation models can
progress from near zero formal math performance to solving highly complex problems.


                                                                                                    10
                       LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



    While small specialized LLMs lack the overarching agentic capabilities of their foundation coun-
terparts, we acknowledge that they still hold value. A hybrid architecture combining the high-level,
structural reasoning of a foundation model with the focused, formal step generation of a fine-tuned
specialized model could be a highly effective design pattern. However, exploring this hybrid approach
remains outside the scope of this paper, as our primary goal is to highlight the standalone power of
general purpose LLMs in an agentic workflow.


6. Case Studies: Formalizing Open Problems in Combinatorics
Hamiltonian Decomposition of Directed Cayley Graphs. To evaluate LEAP on a highly complex
mathematical task, we targeted a recently solved open problem in combinatorics: the Hamiltonian
decomposition of the directed Cayley graph Γ𝑚 = 𝐶𝑎𝑦 (ℤ3𝑚 , { 𝑒1 , 𝑒2 , 𝑒3 }) for even 𝑚. Originally posed by
Donald Knuth, the problem asks whether the graph’s directed arcs can be partitioned into exactly three
distinct, spanning Hamiltonian cycles . The informal mathematical proof for the even-case construction
is exceptionally intricate, relying on heavy combinatorial analysis and localized defect routing across
different layers of the graph. We focused our formalization efforts on a critical subproblem: rigorously
verifying that the 2D planar projection of a single color class’s routing dynamics forms an unbroken
mathematical cycle of length 𝑚2 . The informal arguments for this specific dynamic span roughly 20
pages of dense piecewise maps, parity-dependent intervals, and complex cross-row transitions. To
tackle a formal verification of this magnitude, we deployed LEAP, which successfully decomposed
the monolithic informal proof into a granular, highly structured proof graph. By autonomously and
systematically resolving the interdependent nodes of this graph, LEAP managed to fully verify the
complex cycle-merging dynamics, ultimately synthesizing over 5000 lines of rigorous Lean 4 code to
complete the formal proof for this subproblem. Full problem descriptions and informal proofs are
available at https://github.com/dpwoodru/knuthCycles/tree/main.


Formalizing Erdős Problem 457. We further tested LEAP on Erdős Problem 457, a classic graph
theory problem concerning the density of triangle-free graphs. Although this problem is already
resolved, it served as an ideal benchmark to assess LEAP’s ability to autonomously reconstruct and
verify established mathematical results. Tasked with deriving the known proof from first principles in
Lean 4, LEAP effectively navigated the combinatorial constraints to confirm the theorem’s validity.
This successful reproduction demonstrates LEAP’s capability to reliably translate complex, existing
literature into high-assurance formal proofs without human intervention.
   Formal statements and detailed problem descriptions are provided in Appendix B.


7. Conclusion and Future Work
The success of LEAP suggests that modern general-purpose LLMs possess substantial reasoning ca-
pabilities for rigorous domain-specific tasks, provided they are coupled with appropriate structural
scaffolding. In formal mathematics, this scaffolding naturally takes the form of proof decomposition
and verifier-guided refinement: the model decomposes complex theorems into smaller subgoals, while
the Lean compiler checks each formal step. This design provides a structured mechanism for translat-
ing informal reasoning into mechanically verified proofs. A central challenge for future work is how
to navigate the resulting proof trees efficiently. As decomposition produces increasingly fine-grained
subgoals, the search space can grow rapidly. Future systems should therefore improve branch prioriti-
zation, decomposition strategies, and compute allocation across large proof searches. Such advances
will be critical for scaling agentic formal proving systems to more complex mathematical problems.


                                                                                                         11
                        LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



Acknowledgements
We thank Michael P. Brenner, Honghao Lin, David Woodruff, Vahab Mirrokni for providing the informal
proof of the even-case of Knuth’s Cycles problem. We would also like to thank Ashley Aragorn Khoo,
Paul Lezeau, Calle Sönne, and Moritz Firsching for formalizing the Lean problem statements in
Lean-IMO-Bench.


References
T. Achim, A. Best, A. Bietti, K. Der, M. Fédérico, S. Gukov, D. Halpern-Leistner, K. Henningsgard,
  Y. Kudryashov, A. Meiburg, M. Michelsen, R. Patterson, E. Rodriguez, L. Scharff, V. Shanker, V. Sicca,
   H. Sowrirajan, A. Swope, M. Tamas, V. Tenev, J. Thomm, H. Williams, and L. Wu. Aristotle: Imo-level
   automated theorem proving, 2025. URL https://arxiv.org/abs/2510.01346.

M. Carneiro. Metamath zero: The cartesian theorem prover, 2020. URL https://arxiv.org/ab
 s/1910.10703.
J. Chen, W. Chen, J. Du, J. Hu, Z. Jiang, A. Jie, X. Jin, X. Jin, C. Li, W. Shi, Z. Wang, M. Wang, C. Wei,
   S. Wei, H. Xin, F. Yang, W. Gao, Z. Yuan, T. Zhan, Z. Zheng, T. Zhou, and T. H. Zhu. Seed-prover
   1.5: Mastering undergraduate-level theorem proving via learning from experience, 2025a. URL
   https://arxiv.org/abs/2512.17260.
L. Chen, J. Gu, L. Huang, W. Huang, Z. Jiang, A. Jie, X. Jin, X. Jin, C. Li, K. Ma, C. Ren, J. Shen, W. Shi,
   T. Sun, H. Sun, J. Wang, S. Wang, Z. Wang, C. Wei, S. Wei, Y. Wu, Y. Wu, Y. Xia, H. Xin, F. Yang,
   H. Ying, H. Yuan, Z. Yuan, T. Zhan, C. Zhang, Y. Zhang, G. Zhang, T. Zhao, J. Zhao, Y. Zhou, and
   T. H. Zhu. Seed-prover: Deep and broad reasoning for automated theorem proving, 2025b. URL
   https://arxiv.org/abs/2507.23726.
T. Feng, J. Jung, S. hyun Kim, C. Pagano, S. Gukov, C.-C. Tsai, D. Woodruff, A. Javanmard, A. Mokhtari,
   D. Hwang, Y. Chervonyi, J. N. Lee, G. Bingham, T. H. Trinh, V. Mirrokni, Q. V. Le, and T. Luong.
   Aletheia tackles firstproof autonomously, 2026a. URL https://arxiv.org/abs/2602.21201.

T. Feng, T. Trinh, G. Bingham, J. Kang, S. Zhang, S. hyun Kim, K. Barreto, C. Schildkraut, J. Jung, J. Seo,
   C. Pagano, Y. Chervonyi, D. Hwang, K. Hou, S. Gukov, C.-C. Tsai, H. Choi, Y. Jin, W.-Y. Li, H.-A. Wu, R.-
   A. Shiu, Y.-S. Shih, Q. V. Le, and T. Luong. Semi-autonomous mathematics discovery with gemini: A
   case study on the erdős problems, 2026b, 2026b. URL https://arxiv.org/abs/2601.22401.

T. Feng, T. H. Trinh, G. Bingham, D. Hwang, Y. Chervonyi, J. Jung, J. Lee, C. Pagano, S. hyun Kim,
   F. Pasqualotto, S. Gukov, J. N. Lee, J. Kim, K. Hou, G. Ghiasi, Y. Tay, Y. Li, C. Kuang, Y. Liu, H. Lin, E. Z.
   Liu, N. Nayakanti, X. Yang, H.-T. Cheng, D. Hassabis, K. Kavukcuoglu, Q. V. Le, and T. Luong. Towards
   autonomous mathematics research, 2026c. URL https://arxiv.org/abs/2602.10177.

E. First, M. N. Rabe, T. Ringer, and Y. Brun. Baldur: Whole-proof generation and repair with large
  language models. In Proceedings of the 31st ACM Joint European Software Engineering Conference
  and Symposium on the Foundations of Software Engineering, pages 1229–1241, 2023.

G. Gao, H. Ju, J. Jiang, Z. Qin, and B. Dong. A semantic search engine for mathlib4. In Y. Al-Onaizan,
  M. Bansal, and Y.-N. Chen, editors, Findings of the Association for Computational Linguistics: EMNLP
  2024, pages 8001–8013, Miami, Florida, USA, Nov. 2024. Association for Computational Linguistics.
  doi: 10.18653/v1/2024.findings-emnlp.470. URL https://aclanthology.org/2024.find
  ings-emnlp.470/.


                                                                                                              12
                      LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



C. Greiffenhagen. Checking correctness in mathematical peer review. Social studies of science, 54(2):
  184–209, 2024.

D. Guo, D. Yang, H. Zhang, J. Song, P. Wang, Q. Zhu, R. Xu, R. Zhang, S. Ma, X. Bi, et al.
  Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint
  arXiv:2501.12948, 2025.

T. Hales, M. Adams, G. Bauer, D. T. Dang, J. Harrison, T. L. Hoang, C. Kaliszyk, V. Magron, S. McLaugh-
   lin, T. T. Nguyen, T. Q. Nguyen, T. Nipkow, S. Obua, J. Pleso, J. Rute, A. Solovyev, A. H. T. Ta, T. N.
   Tran, D. T. Trieu, J. Urban, K. K. Vu, and R. Zumkeller. A formal proof of the kepler conjecture.
   Forum of mathematics, Pi, 5, 2017.

T. C. Hales. A proof of the kepler conjecture. Annals of mathematics, 162(3):1065–1185, 2005.

J. Harrison. Hol light: An overview. In International Conference on Theorem Proving in Higher Order
   Logics, pages 60–66. Springer, 2009.

Y. Huang and L. F. Yang. Winning gold at IMO 2025 with a model-agnostic verification-and-refinement
   pipeline. In The 5th Workshop on Mathematical Reasoning and AI at NeurIPS 2025, 2025. URL
   https://openreview.net/forum?id=svz4xDjRC1.
T. Hubert, R. Mehta, L. Sartran, M. Z. Horváth, G. Žužić, E. Wieser, A. Huang, J. Schrittwieser,
  Y. Schroecker, H. Masoom, O. Bertolli, T. Zahavy, A. Mandhane, J. Yung, I. Beloshapka, B. Ibarz,
  V. Veeriah, L. Yu, O. Nash, P. Lezeau, S. Mercuri, C. Sönne, B. Mehta, A. Davies, D. Zheng,
  F. Pedregosa, Y. Li, I. von Glehn, M. Rowland, S. Albanie, A. Velingker, S. Schmitt, E. Lockhart,
  E. Hughes, H. Michalewski, N. Sonnerat, D. Hassabis, P. Kohli, and D. Silver. Olympiad-level formal
  mathematical reasoning with reinforcement learning. Nature, 651:607–613, 2026. doi: 10.1038/
  s41586-025-09833-y. URL https://www.nature.com/articles/s41586-025-09833-y.

G. Huet, G. Kahn, and C. Paulin-Mohring. The coq proof assistant a tutorial. Rapport Technique, 178:
  113, 1997.

A. Jaech, A. Kalai, A. Lerer, A. Richardson, A. El-Kishky, A. Low, A. Helyar, A. Madry, A. Beutel,
  A. Carney, et al. Openai o1 system card. arXiv preprint arXiv:2412.16720, 2024.

A. Q. Jiang, S. Welleck, J. P. Zhou, T. Lacroix, J. Liu, W. Li, M. Jamnik, G. Lample, and Y. Wu.
  Draft, sketch, and prove: Guiding formal theorem provers with informal proofs. In The Eleventh
  International Conference on Learning Representations, 2023. URL https://openreview.net/f
  orum?id=SMa9EAovKMC.
G. Lample, T. Lacroix, M.-A. Lachaux, A. Rodriguez, A. Hayat, T. Lavril, G. Ebner, and X. Martinet.
  Hypertree proof search for neural theorem proving. In S. Koyejo, S. Mohamed, A. Agarwal, D. Bel-
  grave, K. Cho, and A. Oh, editors, Advances in Neural Information Processing Systems, volume 35,
  pages 26337–26349. Curran Associates, Inc., 2022. URL https://proceedings.neurips.cc
  /paper_files/paper/2022/file/a8901c5e85fb8e1823bbf0f755053672-Paper-Con
  ference.pdf.
H. Lin, Z. Sun, S. Welleck, and Y. Yang. Lean-STar: Learning to interleave thinking and proving. In
  The Thirteenth International Conference on Learning Representations, 2025. URL https://openre
  view.net/forum?id=SOWZ59UyNc.
Y. Lin, S. Tang, B. Lyu, Z. Yang, J.-H. Chung, H. Zhao, L. Jiang, Y. Geng, J. Ge, J. Sun, J. Wu, J. Gesi,
   X. Lu, D. Acuna, K. Yang, H. Lin, Y. Choi, D. Chen, S. Arora, and C. Jin. Goedel-prover-v2: Scaling
   formal theorem proving with scaffolded data synthesis and self-correction. In The Fourteenth

                                                                                                       13
                      LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



  International Conference on Learning Representations, 2026. URL https://openreview.net/f
  orum?id=j4C0nALrgK.
P. Lu, R. Gong, S. Jiang, L. Qiu, S. Huang, X. Liang, and S.-C. Zhu. Inter-GPS: Interpretable geometry
   problem solving with formal language and symbolic reasoning. In C. Zong, F. Xia, W. Li, and
   R. Navigli, editors, Proceedings of the 59th Annual Meeting of the Association for Computational
   Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1:
   Long Papers), pages 6774–6786, Online, Aug. 2021. Association for Computational Linguistics. doi:
   10.18653/v1/2021.acl-long.528. URL https://aclanthology.org/2021.acl-long.528/.

T. Luong and E. Lockhart. Advanced version of gemini with deep think officially achieves gold-medal
   standard at the international mathematical olympiad. Google DeepMind Blog, July 2025. URL
 https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think
 -officially-achieves-gold-medal-standard-at-the-international-mathemati
 cal-olympiad/. Accessed: 2026-05-02.
T. Luong, D. Hwang, H. H. Nguyen, G. Ghiasi, Y. Chervonyi, I. Seo, J. Kim, G. Bingham, J. Lee,
  S. Mishra, A. Zhai, H. Hu, H. Michalewski, J. Kim, J. Ahn, J. Bae, X. Song, T. H. Trinh, Q. V. Le,
  and J. Jung. Towards robust mathematical reasoning. In C. Christodoulopoulos, T. Chakraborty,
  C. Rose, and V. Peng, editors, Proceedings of the 2025 Conference on Empirical Methods in Natural
  Language Processing, pages 35418–35442, Suzhou, China, Nov. 2025. Association for Computational
  Linguistics. ISBN 979-8-89176-332-6. doi: 10.18653/v1/2025.emnlp-main.1794. URL https:
  //aclanthology.org/2025.emnlp-main.1794/.
T. mathlib Community. The lean mathematical library. In Proceedings of the 9th ACM SIGPLAN
  International Conference on Certified Programs and Proofs, POPL ’20, page 367–381. ACM, Jan. 2020.
  doi: 10.1145/3372885.3373824. URL http://dx.doi.org/10.1145/3372885.3373824.

L. d. Moura and S. Ullrich. The lean 4 theorem prover and programming language. In International
   Conference on Automated Deduction, pages 625–635. Springer, 2021.

T. Nipkow, M. Wenzel, and L. C. Paulson. Isabelle/HOL: a proof assistant for higher-order logic. Springer,
   2002.

S. Polu and I. Sutskever. Generative language modeling for automated theorem proving. arXiv preprint
   arXiv:2009.03393, 2020.

N. Ravi, K. Ying, V. Nesterov, R. Krishnan, E. Uskuplu, B. Xia, J. Aswedige, and L. Nashold. For-
  malproofbench: Can models write graduate level math proofs that are formally verified? In
  ICLR 2026 Workshop: VerifAI-2: The Second Workshop on AI Verification in the Wild, 2026. URL
  https://openreview.net/forum?id=1LdnVndCEG.
Z. Z. Ren, Z. Shao, J. Song, H. Xin, H. Wang, W. Zhao, L. Zhang, Z. Fu, Q. Zhu, D. Yang, Z. F. Wu,
  Z. Gou, S. Ma, H. Tang, Y. Liu, W. Gao, D. Guo, and C. Ruan. Deepseek-prover-v2: Advancing
  formal mathematical reasoning via reinforcement learning for subgoal decomposition, 2025. URL
  https://arxiv.org/abs/2504.21801.
A. K. Taylor, J. Zhang, E. Ji, V. Sahai, H. Deng, Y. Chen, Y. Yuan, D. Wu, J.-C. Gu, K.-W. Chang, N. Peng,
  A. Sahai, and W. Wang. Taobench: Do automated theorem prover llms generalize beyond mathlib?,
  2026. URL https://arxiv.org/abs/2603.12744.

G. Tsoukalas, J. Lee, J. Jennings, J. Xin, M. Ding, M. Jennings, A. Thakur, and S. Chaudhuri. Put-
  nambench: Evaluating neural theorem-provers on the putnam mathematical competition. In


                                                                                                       14
                      LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



  A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, Advances
  in Neural Information Processing Systems, volume 37, pages 11545–11569. Curran Associates, Inc.,
  2024. doi: 10.52202/079017-0368. URL https://proceedings.neurips.cc/paper_files
  /paper/2024/file/1582eaf9e0cf349e1e5a6ee453100aa1-Paper-Datasets_and_Be
  nchmarks_Track.pdf.
G. Tsoukalas, A. Kovsharov, S. Shirobokov, A. Surina, M. Firsching, G. Bérczi, F. J. Ruiz, A. Suggala,
  A. Z. Wagner, E. Wieser, et al. Advancing mathematics research with ai-driven formal proof search.
  arXiv preprint arXiv:2605.22763, 2026.

S. Varambally, T. Voice, Y. Sun, Z. Chen, R. Yu, and K. Ye. Hilbert: Recursively building formal proofs
   with informal reasoning. In The 5th Workshop on Mathematical Reasoning and AI at NeurIPS 2025,
   2025. URL https://openreview.net/forum?id=ljAHonPrs1.

H. Wang, M. Unsal, X. Lin, M. Baksys, J. Liu, M. D. Santos, F. Sung, M. Vinyes, Z. Ying, Z. Zhu,
  J. Lu, H. de Saxcé, B. Bailey, C. Song, C. Xiao, D. Zhang, E. Zhang, F. Pu, H. Zhu, J. Liu, J. Bayer,
  J. Michel, L. Yu, L. Dreyfus-Schmidt, L. Tunstall, L. Pagani, M. Machado, P. Bourigault, R. Wang,
  S. Polu, T. Barroyer, W.-D. Li, Y. Niu, Y. Fleureau, Y. Hu, Z. Yu, Z. Wang, Z. Yang, Z. Liu, and J. Li.
  Kimina-prover preview: Towards large formal reasoning models with reinforcement learning, 2025.
  URL https://arxiv.org/abs/2504.11354.

Y. Wu, A. Q. Jiang, W. Li, M. Rabe, C. Staats, M. Jamnik, and C. Szegedy. Autoformalization with
   large language models. Advances in neural information processing systems, 35:32353–32368, 2022.

H. Xin, Z. Ren, J. Song, Z. Shao, W. Zhao, H. Wang, B. Liu, L. Zhang, X. Lu, Q. Du, W. Gao, H. Zhang,
  Q. Zhu, D. Yang, Z. Gou, Z. Wu, F. Luo, and C. Ruan. Deepseek-prover-v1.5: Harnessing proof
  assistant feedback for reinforcement learning and monte-carlo tree search. In The Thirteenth
  International Conference on Learning Representations, 2025a. URL https://openreview.net/f
  orum?id=I4YAIwrsXa.
R. Xin, C. Xi, J. Yang, F. Chen, H. Wu, X. Xiao, Y. Sun, S. Zheng, and M. Ding. BFS-prover: Scalable best-
  first tree search for LLM-based automatic theorem proving. In W. Che, J. Nabende, E. Shutova, and
  M. T. Pilehvar, editors, Proceedings of the 63rd Annual Meeting of the Association for Computational
  Linguistics (Volume 1: Long Papers), pages 32588–32599, Vienna, Austria, July 2025b. Association
  for Computational Linguistics. ISBN 979-8-89176-251-0. doi: 10.18653/v1/2025.acl-long.1565.
  URL https://aclanthology.org/2025.acl-long.1565/.

K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil, R. J. Prenger, and A. Anandkumar.
  Leandojo: Theorem proving with retrieval-augmented language models. In A. Oh, T. Naumann,
  A. Globerson, K. Saenko, M. Hardt, and S. Levine, editors, Advances in Neural Information Processing
  Systems, volume 36, pages 21573–21612. Curran Associates, Inc., 2023. URL https://procee
  dings.neurips.cc/paper_files/paper/2023/file/4441469427094f8873d0fecb0c4
  e1cee-Paper-Datasets_and_Benchmarks.pdf.
K. Zheng, J. M. Han, and S. Polu. minif2f: a cross-system benchmark for formal olympiad-level
  mathematics. In International Conference on Learning Representations, 2022. URL https://open
  review.net/forum?id=9ZPegFuFTFv.




                                                                                                       15
                      LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



A. Related Work
Neural Theorem Proving Early work in neural theorem proving mainly utilize in-house symbolic
engines, such as Metamath (Polu and Sutskever, 2020), MM0 (Carneiro, 2020) or some dedicated
formal language for geometry problems (Lu et al., 2021). Later work such as mathlib (mathlib
Community, 2020), LeanDojo (Yang et al., 2023) and MiniF2F (Zheng et al., 2022) pioneered the
use of LLMs for generative theorem proving in Lean. They serve as pillar that provide a rich library of
known theorems, an interactive environment for step-level search and a descent-level of difficulty
evaluation set. To manage the large search space, HyperTree Proof Search (Lample et al., 2022) and
related Monte Carlo tree search methods (Lin et al., 2025; Xin et al., 2025b) have been explored.
While search-based methods operate at the tactic level, Baldur (First et al., 2023) and DeepSeek-
prover-v1.5 (Xin et al., 2025a) explored whole-proof generation, attempting to produce a complete
proof in a single step. Another promising direction is guiding formal proof search with informal
proofs or sketches. The “draft, sketch, and prove” methodology (Jiang et al., 2023) demonstrated that
using an informal proof as a blueprint can significantly guide and improve formal theorem proving.
Our work, LEAP, builds on this intuition by utilizing general LLMs to generate informal blueprints
and iteratively refine formal proofs based on compiler feedback, but without relying on specialized
fine-tuned models for the formalization step.


Specialized Prover Models Recent breakthroughs have often relied on extensive fine-tuning of
large models on formal mathematical corpora. Representative works include AlphaProof (Hubert
et al., 2026), DeepSeek Prover V2 (Ren et al., 2025), Seed Prover (Chen et al., 2025b), Kimina Prover
(Wang et al., 2025) and Goedel Prover V2 (Lin et al., 2026). These models achieve state-of-the-art
performance by scaling up training and search on formal systems. However, they require substantial
computational resources for training and are highly specialized for specific formal languages. In
contrast, LEAP demonstrates that general-purpose LLMs, when placed in a proper agentic environment,
can achieve competitive performance without such specialized fine-tuning.


Auto-Formalization Auto-formalization, the task of translating natural language mathematics into
formal statements and proofs, is a critical bridge between informal and formal reasoning. Early work
relied on neural machine translation techniques (Wu et al., 2022). More recently, LLMs have been used
to generate formal statements for training provers at scale, as seen in the auto-formalization pipeline
of AlphaProof (Hubert et al., 2026). LEAP utilizes the strong auto-formalization capabilities of general
LLMs within its agentic harness to bridge the gap between informal blueprints and formal proofs.


Mathematical Reasoning with LLMs Large Language Models have shown impressive progress
in solving natural-language mathematical problems, demonstrating strong capabilities in complex
reasoning. Recent advancements, such as OpenAI o1 (Jaech et al., 2024) and DeepSeek R1 (Guo
et al., 2025), have demonstrated the effectiveness of scaling reinforcement learning for complex
mathematical tasks, achieving high scores on competitive benchmarks like AIME. However, direct
evaluation of these models on formal theorem proving benchmarks often yields low solve rates,
highlighting the gap between informal reasoning and formal verification. LEAP addresses this by
leveraging the strong informal reasoning and instruction-following capabilities of general LLMs within
an agentic harness, enabling them to interact with the Lean compiler and iteratively self-correct, thus
bridging the formalization gap without specialized fine-tuning.




                                                                                                     16
                       LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



B. Problem Statements
We present the LEAN statements of the open problems that we tested with LEAP.


Hamiltonian Decomposition of Directed Cayley Graphs The Hamiltonian decomposition problem
for the directed Cayley graph Γ𝑚 = 𝐶𝑎𝑦 (ℤ3𝑚 , { 𝑒1 , 𝑒2 , 𝑒3 }) asks whether its edges can be partitioned into
three distinct directed Hamiltonian cycles. For the even-case construction (𝑚 = 2ℎ ≥ 10), the 3D
routing dynamics of individual color classes can be analytically projected onto a 2D planar “round
map” defined on a ℤ𝑚 × ℤ𝑚 grid. The formal statement below encodes the exact operational semantics
for the Color 2 subgraph—including its parity-dependent structural defects, coordinate shifts, and
piecewise transitions—and asserts that its round map forms a single, unbroken cycle of length 𝑚2 .

   Lean Statement for the Hamiltonian Decomposition of Directed Cayley Graphs

   import Mathlib

   set_option autoImplicit false

   variable (h : ℕ) (hh : 5 ≤ h)

   abbrev Fiber2 (h : ℕ) := Fin (2 * h) × Fin (2 * h)

   -- 1. Base Coordinate Definitions
   def one2 : Fin (2 * h) := ⟨1, by omega⟩
   def mMinusOne2 : Fin (2 * h) := ⟨2 * h - 1, by omega⟩
   def mMinusTwo2 : Fin (2 * h) := ⟨2 * h - 2, by omega⟩

   def succ2c (x : Fin (2 * h)) : Fin (2 * h) := x + one2 h hh
   def pred2c (x : Fin (2 * h)) : Fin (2 * h) := x - one2 h hh

   -- 2. Exceptional Set Logic (Defects)
   def y2SwitchRow (x : Fin (2 * h)) : Prop :=
     x.val = h + 1 ∨ x.val = h + 2 ∨ x.val = h + 3

   instance (x : Fin (2 * h)) : Decidable (y2SwitchRow h x) := by
     unfold y2SwitchRow
     infer_instance

   def y2star (x : Fin (2 * h)) : Fin (2 * h) :=
     if y2SwitchRow h x then
       if h % 2 = 0 then mMinusTwo2 h hh else mMinusOne2 h hh
     else
       ⟨2 * h - 1 - x.val, by omega⟩

   def A2 (x : Fin (2 * h)) : Fin (2 * h) :=
     succ2c h hh (y2star h hh x)

   def activeB2 (x y : Fin (2 * h)) : Prop :=
     if h % 2 = 0 then
       (x.val = h + 1 ∧ y.val ≤ h - 1) ∨
         (x.val = h + 4 ∧ h - 3 ≤ y.val ∧ y.val ≤ 2 * h - 2)
     else
       (x.val = h + 1 ∧ 1 ≤ y.val ∧ y.val ≤ h - 1) ∨
         (x.val = h + 4 ∧ h - 3 ≤ y.val)

   instance (x y : Fin (2 * h)) : Decidable (activeB2 h x y) := by



                                                                                                           17
                     LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks




     unfold activeB2
     infer_instance

   -- 3. The Round Map
   def r2Map (p : Fiber2 h) : Fiber2 h :=
     let x := p.1
     let u := pred2c h hh p.2
     if u = A2 h hh x then
       (succ2c h hh x,
         if x.val = h + 1 ∨ x.val = h + 2 then u else pred2c h hh u)
     else if activeB2 h x u then
       (x, pred2c h hh u)
     else
       (x, u)

   -- 4. The Self-Contained Goal
   /-- The unrolled Hamiltonicity goal for the Color 2 round map. -/
   theorem color2_singleCycle_unrolled (h6 : 6 ≤ h) :
       (∀ p : Fin (2 * h) × Fin (2 * h), (r2Map h hh)^[(2 * h) * (2 * h)] p = p) ∧
       (∀ (p : Fin (2 * h) × Fin (2 * h)) (k : ℕ), 0 < k → k < (2 * h) * (2 * h) → (
       r2Map h hh)^[k] p ≠ p) := by
     sorry




Erdős 457 Erdős Problem 457 is a number theory challenge concerning the prime divisors of
consecutive integers. Specifically, it conjectures the existence of a real number 𝜀 > 0 such that for
infinitely many integers 𝑛, every prime number 𝑝 ≤ (2 + 𝜀) log 𝑛 divides the product of the ⌊log 𝑛⌋
consecutive integers starting from 𝑛 + 1. The Lean formalization below captures this exact asymptotic
prime divisibility condition.

   Lean Statement for Erdős Problem 457


   import Mathlib

   theorem erdos_457 : ∃ 𝜀 > (0 : ℝ),
       { (n :Îℕ) | ∀ (p : ℕ), p ≤ (2 + 𝜀) * Real.log n → p.Prime →
         p |   i ∈ Finset.Icc 1 ⌊Real.log n⌋ + , (n + i) }.Infinite := by
     sorry




                                                                                                   18
                      LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



C. Proof Contexts and Artifacts
This section describes the formal and informal artifacts used by LEAP during proof planning. Formal
artifacts correspond to Lean-level objects that are checked by the compiler or represented in the proof
DAG, while informal artifacts correspond to natural-language planning objects used to guide direct
proving and decomposition.


Formal context. A proof goal is a Lean theorem or lemma statement that remains to be proved. The
original input theorem is the root proof goal, while lemma statements introduced by decomposition
become subgoals in the proof DAG. A formal proof is a complete Lean proof of the current proof goal
that does not rely on newly proposed unproven lemmas; once accepted by the Lean compiler, the
corresponding goal is marked as resolved. A proof sketch is a Lean artifact that proves the current goal
assuming a set of proposed lemmas. In LEAP, a proof sketch may contain sorry placeholders only
for these explicitly proposed lemmas. Thus, a verified proof sketch defines a valid decomposition:
once all referenced proposed lemmas are later proved, the current goal is also proved. We present
examples of these context using Lean-IMO-Bench Problem 001 and 009 in the Basic Set. All artifacts,
except for the Proof Goal of the root problem, are created by LEAP automatically.)

   Example Proof Goal (Lean-IMO-Bench, Basic 001)

   theorem PBBasic001 : {f : ℤ → ℤ | ∀ x y, f (2 * x) + 2 * f y = f (f (x + y))}
         = {0} ∪ {(fun x ↦→ 2 * x + c)| (c : ℤ)} :=
   by sorry


   Example Formal Proof (Lean-IMO-Bench, Basic 001)

   import Mathlib

   theorem PBBasic001 : {f : ℤ → ℤ | ∀ x y, f (2 * x) + 2 * f y = f (f (x + y))}
           = {0} ∪ {(fun x ↦→ 2 * x + c)| (c : ℤ)} :=
   by
     ext f
     simp only [Set.mem_setOf_eq, Set.mem_union, Set.mem_singleton_iff, Set.mem_range]
     constructor
      · intro h
         have h1 : ∀ y, f (f y) = 2 * f y + f 0 := by
           -- [Proof details omitted for brevity]
         have h2 : ∀ x, f (2 * x) = 2 * f x - f 0 := by
           -- [Proof details omitted]
         have h3 : ∀ x y, f (x + y) = f x + f y - f 0 := by
           -- [Proof details omitted]

        have hc : ∃ c, c = f 0 := ⟨f 0, rfl⟩
        rcases hc with ⟨c, hc_eq⟩
        have hk : ∃ k, k = f 1 - c := ⟨f 1 - c, rfl⟩
        rcases hk with ⟨k, hk_eq⟩

        -- ... [Induction steps for h4 omitted] ...

        have h5 : ∀ x : ℤ, f x = k * x + c := by
          -- ... [Negative cases to prove linear form omitted] ...




                                                                                                     19
                  LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks




   have eq_all : ∀ x y : ℤ, k * (2 * x) + c + 2 * (k * y + c) = k * (k * (x + y) +
   c) + c := by
     intro x y
     have h_orig := h x y
     simp only [h5] at h_orig
     exact h_orig

   have hk_eq : k * (k - 2) = 0 := by
     -- [Algebraic simplification using eq_all 1 0 and eq_all 0 0 omitted]

   have hk2 : k = 0 ∨ k = 2 := by
     cases mul_eq_zero.mp hk_eq with
     | inl h1 => left; exact h1
     | inr h2 => right; omega

   rcases hk2 with hk0 | hk2
   · left
      have eq00 := eq_all 0 0
      rw [hk0] at eq00
      have hc0 : c = 0 := by linarith [eq00]
      ext x
      simp only [Pi.zero_apply]
      have hfx := h5 x
      rw [hk0, hc0] at hfx
      omega
   · right
      use c
      ext x
      have hfx := h5 x
      rw [hk2] at hfx
      omega

 -- Prove that the derived candidates are indeed solutions mappings
 · rintro (rfl | ⟨c, rfl⟩ )
    · intro x y
       simp only [Pi.zero_apply, mul_zero, add_zero]
    · intro x y
       dsimp only
       ring


Example Proof Sketch (Lean-IMO-Bench, Basic 006)

import Mathlib

open Polynomial

-- Shared Definitions from the file environment
def K (c : ℕ → ℤ) : ℤ := (c 1)^2 - (2 : ℤ) * (c 0) * (c 2)

def k_target (c : ℕ → ℤ) : ℕ := max 2 (Int.toNat (K c + (1 : ℤ)))

def esymm_one_target (s : Multiset ℝ) : ℕ → ℝ
  | 0 => 0
  | k + 1 => s.esymm k

def esymm_two_target (s : Multiset ℝ) : ℕ → ℝ
  | 0 => 0



                                                                                            20
                            LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks




     | 1 => 0
     | k + 2 => s.esymm k

   -- Supporting Lemmas (with sorry)
   lemma root_count_bound_implies_eq
                         Í
                                      (c : ℕ → ℤ) (hc : c 0 ≠ 0) (k : ℕ)
     (h_not_less : ¬ ((( i ∈ Finset.Icc 0 k, monomial i (c i)).rootSet ℝ).ncard < k))
       :Í
     ((
      Í
          i ∈ Finset.Icc 0 k, monomial i (c i)).rootSet ℝ).ncard = k ∧
     ( i ∈ Finset.Icc 0 k, monomial i (c i)).natDegree = k := by
     sorry

   lemma k_le_K_of_eq
               Í
                      (c : ℕ → ℤ) (hc : c 0 ≠ 0) (k : ℕ) (hk : (2 : ℕ) ≤ k)
     (h_eq : ((Í i ∈ Finset.Icc 0 k, monomial i (c i)).rootSet ℝ).ncard = k)
     (h_deg : ( i ∈ Finset.Icc 0 k, monomial i (c i)).natDegree = k) :
     (k : ℤ) ≤ K c := by
     sorry

   lemma k_target_ge_two (c : ℕ → ℤ) : (2 : ℕ) ≤ k_target c := by
     sorry

   lemma k_target_gt_K (c : ℕ → ℤ) : K c < (k_target c : ℤ) := by
     sorry

   -- Main Theorem
   theorem PBBasic006
            Í
                      (c : ℕ → ℤ) (hc : c 0 ≠ 0) :
     ∃ k, (( i ∈ Finset.Icc 0 k, monomial i (c i)).rootSet ℝ).ncard < k := by
     use k_target c
     by_contra h
     have h1 := root_count_bound_implies_eq c hc (k_target c) h
     have h2 := k_le_K_of_eq c hc (k_target c) (k_target_ge_two c) h1.1 h1.2
     have h3 := k_target_gt_K c
     linarith




Informal context. An informal proof is a natural-language plan for proving the current goal directly,
without introducing a decomposition into new subgoals. It guides the generation of a complete formal
proof. An informal blueprint is a higher-level natural-language plan that explains how the current
goal can be reduced to useful supporting lemmas. Unlike an informal proof, an informal blueprint
may introduce proposed lemmas that are not immediately proved and may include auxiliary lemmas
for later proof steps. These proposed lemmas are then translated into formal subgoals and organized
in the proof DAG. Examples are shown below:

   Example Informal Proof (Lean-IMO-Bench, Basic 001)

   Let 𝑆 = { 𝑓 : ℤ → ℤ | ∀𝑥, 𝑦 ∈ ℤ, 𝑓 (2𝑥 ) + 2 𝑓 ( 𝑦 ) = 𝑓 ( 𝑓 ( 𝑥 + 𝑦 ))} and 𝑇 = {0} ∪ { 𝑥 ↦→ 2𝑥 + 𝑐 | 𝑐 ∈ ℤ}. We want to show
   that 𝑆 = 𝑇 .

   Part 1: Proof that 𝑇 ⊆ 𝑆

   Suppose 𝑓 ∈ 𝑇 . Then either 𝑓 is the constant zero function ( 𝑓 = 0) or 𝑓 ( 𝑥 ) = 2𝑥 + 𝑐 for some 𝑐 ∈ ℤ.

       • Case 1: If 𝑓 = 0, then for any 𝑥, 𝑦 ∈ ℤ, the left-hand side is 𝑓 (2𝑥 ) + 2 𝑓 ( 𝑦 ) = 0 + 2(0) = 0. The right-hand
         side is 𝑓 ( 𝑓 ( 𝑥 + 𝑦 )) = 𝑓 (0) = 0. The two sides match, so 𝑓 ∈ 𝑆.
       • Case 2: If 𝑓 ( 𝑥 ) = 2 𝑥 + 𝑐 for some 𝑐 ∈ ℤ, then for any 𝑥, 𝑦 ∈ ℤ, the left-hand side is: 𝑓 (2 𝑥 ) +2 𝑓 ( 𝑦 ) = (2(2 𝑥 ) + 𝑐) +
         2(2 𝑦 + 𝑐) = 4 𝑥 + 4 𝑦 + 3𝑐. The right-hand side is: 𝑓 ( 𝑓 ( 𝑥 + 𝑦 )) = 𝑓 (2( 𝑥 + 𝑦 ) + 𝑐) = 2(2𝑥 + 2 𝑦 + 𝑐) + 𝑐 = 4 𝑥 + 4 𝑦 + 3𝑐.
         The two sides are equal, so 𝑓 ∈ 𝑆.



                                                                                                                                              21
                        LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



This proves 𝑇 ⊆ 𝑆.

Part 2: Proof that 𝑆 ⊆ 𝑇

Let 𝑓 ∈ 𝑆. Then for all 𝑥, 𝑦 ∈ ℤ, we have:
(1) 𝑓 (2𝑥 ) + 2 𝑓 ( 𝑦 ) = 𝑓 ( 𝑓 ( 𝑥 + 𝑦 )).

Substitute 𝑥 = 0 into Eq. (1):
 𝑓 (0) + 2 𝑓 ( 𝑦 ) = 𝑓 ( 𝑓 ( 𝑦 )).
Let 𝑐 = 𝑓 (0). Then for all 𝑦 ∈ ℤ, we have:
(2) 𝑓 ( 𝑓 ( 𝑦 )) = 2 𝑓 ( 𝑦 ) + 𝑐.

Using Eq. (2) on the right-hand side of Eq. (1) (since it holds for any input, including 𝑥 + 𝑦 ), we ob-
tain:
(3) 𝑓 (2𝑥 ) + 2 𝑓 ( 𝑦 ) = 2 𝑓 ( 𝑥 + 𝑦 ) + 𝑐.

Substitute 𝑦 = 0 into Eq. (3):
 𝑓 (2 𝑥 ) + 2 𝑓 (0) = 2 𝑓 ( 𝑥 ) + 𝑐.
Since 𝑓 (0) = 𝑐, this becomes 𝑓 (2𝑥 ) + 2𝑐 = 2 𝑓 ( 𝑥 ) + 𝑐, which yields:
(4) 𝑓 (2𝑥 ) = 2 𝑓 ( 𝑥 ) − 𝑐.

Now, substitute Eq. (4) back into the left-hand side of Eq. (3):
(2 𝑓 ( 𝑥 ) − 𝑐) + 2 𝑓 ( 𝑦 ) = 2 𝑓 ( 𝑥 + 𝑦 ) + 𝑐.
Rearranging the terms gives:
2 𝑓 ( 𝑥 + 𝑦 ) = 2 𝑓 ( 𝑥 ) + 2 𝑓 ( 𝑦 ) − 2𝑐.
Because the codomain is ℤ, we can divide both sides by 2 to obtain:
(5) 𝑓 ( 𝑥 + 𝑦 ) = 𝑓 ( 𝑥 ) + 𝑓 ( 𝑦 ) − 𝑐.

Define a new function 𝑔 : ℤ → ℤ by 𝑔 ( 𝑥 ) = 𝑓 ( 𝑥 ) − 𝑐. Then we can rewrite Eq. (5) as:
𝑔 ( 𝑥 + 𝑦 ) + 𝑐 = ( 𝑔 ( 𝑥 ) + 𝑐) + ( 𝑔 ( 𝑦 ) + 𝑐) − 𝑐.
Simplifying this yields Cauchy’s functional equation:
𝑔 ( 𝑥 + 𝑦 ) = 𝑔 ( 𝑥 ) + 𝑔 ( 𝑦 ) for all 𝑥, 𝑦 ∈ ℤ.

Since 𝑔 satisfies 𝑔 ( 𝑥 + 𝑦 ) = 𝑔 ( 𝑥 ) + 𝑔 ( 𝑦 ) over integers, it must be a linear function. Let 𝑘 = 𝑔 (1) ∈ ℤ.
By standard induction, we have 𝑔 ( 𝑥 ) = 𝑘𝑥 for all integers 𝑥 ≥ 0 (with 𝑔 (0) = 0). For negative integers,
0 = 𝑔 (0) = 𝑔 ( 𝑥 + (−𝑥 )) = 𝑔 ( 𝑥 ) + 𝑔 (−𝑥 ), meaning 𝑔 ( 𝑥 ) = −𝑔 (−𝑥 ) = −(−𝑘𝑥 ) = 𝑘𝑥 . Thus 𝑔 ( 𝑥 ) = 𝑘𝑥 for all 𝑥 ∈ ℤ.
As a result, we have 𝑓 ( 𝑥 ) = 𝑘𝑥 + 𝑐 for all 𝑥 ∈ ℤ.

To determine the permissible values of 𝑘 and 𝑐, substitute 𝑓 ( 𝑥 ) = 𝑘𝑥 + 𝑐 back into the original Eq. (1):
Left-hand side: 𝑓 (2𝑥 ) + 2 𝑓 ( 𝑦 ) = 𝑘 (2 𝑥 ) + 𝑐 + 2( 𝑘𝑦 + 𝑐) = 2𝑘𝑥 + 2𝑘𝑦 + 3𝑐.
Right-hand side: 𝑓 ( 𝑓 ( 𝑥 + 𝑦 )) = 𝑘 ( 𝑓 ( 𝑥 + 𝑦 )) + 𝑐 = 𝑘 ( 𝑘 ( 𝑥 + 𝑦 ) + 𝑐) + 𝑐 = 𝑘2 𝑥 + 𝑘2 𝑦 + ( 𝑘 + 1) 𝑐.

For the equality 2𝑘𝑥 + 2𝑘𝑦 + 3𝑐 = 𝑘2 𝑥 + 𝑘2 𝑦 + ( 𝑘 + 1) 𝑐 to hold for all 𝑥, 𝑦 ∈ ℤ, the corresponding coeffi-
cients must match.
Setting 𝑥 = 0 and 𝑦 = 0 yields:
(6) 3𝑐 = ( 𝑘 + 1) 𝑐.
Setting 𝑥 = 1 and 𝑦 = 0 yields:
2𝑘 + 3𝑐 = 𝑘2 + ( 𝑘 + 1) 𝑐.
Subtracting Eq. (6) from this gives 2𝑘 = 𝑘2 , which simplifies to 𝑘 ( 𝑘 − 2) = 0. Since 𝑘 ∈ ℤ, the only solutions are
𝑘 = 0 or 𝑘 = 2.

    • Case A: 𝑘 = 0. Substitute 𝑘 = 0 into Eq. (6): 3𝑐 = 𝑐 =⇒ 2𝑐 = 0 =⇒ 𝑐 = 0. Thus, 𝑓 ( 𝑥 ) = 0 𝑥 + 0 = 0, meaning
      𝑓 is the zero function. Hence 𝑓 ∈ {0} ⊆ 𝑇 .
    • Case B: 𝑘 = 2. Substitute 𝑘 = 2 into Eq. (6): 3𝑐 = 3𝑐, which is true for any 𝑐 ∈ ℤ. Thus, 𝑓 ( 𝑥 ) = 2𝑥 + 𝑐 for
      some 𝑐 ∈ ℤ. Hence 𝑓 ∈ { 𝑥 ↦→ 2 𝑥 + 𝑐 | 𝑐 ∈ ℤ} ⊆ 𝑇 .
In all cases, any function 𝑓 ∈ 𝑆 is also in 𝑇 , proving 𝑆 ⊆ 𝑇 .
Since both subset inclusions have been established, 𝑆 = 𝑇 .




                                                                                                                               22
                        LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



Example Informal Blueprint (Lean-IMO-Bench, Basic 006)

High-Level Mathematical Idea
The goal is to prove that 𝑘 ≤ 𝐾 ( 𝑐), where 𝐾 ( 𝑐) = 𝑐12 − 2𝑐0 𝑐2 , given that the polynomial 𝑃 ( 𝑥 ) = 𝑘𝑖=0 𝑐𝑖 𝑥 𝑖 with integer
                                                                                                       Í
coefficients has degree 𝑘 and exactly 𝑘 real roots.
The proof elegantly uses multiset symmetric polynomials and the AM-GM inequality, avoiding rational functions or
polynomial derivatives:
    1. Polynomial Roots and Splitting: Since 𝑃 has natural degree 𝑘 and 𝑘 distinct real roots, it splits completely
       over ℝ, and the multiset of its roots 𝑆 has cardinality 𝑘.
    2. Vieta’s Formulas: Vieta’s formulas express the coefficients 𝑐0 , 𝑐1 , 𝑐2 in terms of the elementary symmetric
       polynomials of 𝑆:
       𝑐0 = 𝑐𝑘 (−1) 𝑘 𝐸 𝑘
       𝑐1 = 𝑐𝑘 (−1) 𝑘 −1 𝐸 𝑘 −1
       𝑐2 = 𝑐𝑘 (−1) 𝑘 −2 𝐸 𝑘 −2
       where 𝐸 𝑖 = esymm𝑖 ( 𝑆).
    3. Multiset Identity: We construct a new multiset 𝑌 by mapping each root 𝑥 ∈ 𝑆 to the product of all other
       roots, ( 𝑆 \ { 𝑥 }).prod. Purely multiset inductive identities show:
       Í
         𝑌 = 𝐸 𝑘 −1
       esymm2 (𝑌 ) = 𝐸 𝑘 𝐸 𝑘 −2
          𝑌 = ( 𝐸 𝑘 ) 𝑘 −1
       Î
    4. Sum of Squares: For the multiset 𝑍 = 𝑐𝑘 𝑌 , we evaluate the sum of its squares 𝑊 = { 𝑧2 | 𝑧 ∈ 𝑍 }.
       By the relation ( 𝑍 ) 2 = ( 𝑍 2 ) + 2esymm2 ( 𝑍 ), we can algebraically compute 𝑊 = 𝑐12 − 2𝑐0 𝑐2 = 𝐾 ( 𝑐).
                            Í      Í                                                     Í
                                                                            𝑘 −1
    5. Integer Product Bound: The product of 𝑍 evaluates to 𝑐𝑘 ((−1) 𝑐0 ) . Since 𝑃 has degree 𝑘 and 𝑐0 ≠ 0, both
                                                                         𝑘

       𝑐0 and 𝑐𝑘 are non-zero integers. Thus, the product of 𝑍 is a non-zero integer, implying 𝑊 = ( 𝑍 ) 2 ≥ 1.
                                                                                                   Î      Î
    6. AM-GM Inequality: Applying the AM-GM inequality to the multiset 𝑊 (which consists of 𝑘 non-negative
                                                           Í
       real numbers whose product is ≥ 1), we obtain 𝑊 ≥ 𝑘 =⇒ 𝐾 ( 𝑐) ≥ 𝑘.

Required Global Definitions, Variables, or Structures
No new definitions, axioms, or structures are needed. We use purely standard Mathlib components (like Multiset,
Polynomial, and esymm).
Smaller Lemmas (Subproblems)
       lemma coeff_of_sum_Icc (c : ℕ → ℤ) (k : ℕ) (hk : (2 : ℕ) ≤ k)
       (i : Íℕ) (hi : i ≤ k) :
           ( j ∈ Finset.Icc 0 k, Polynomial.monomial j (c j)).coeff i =
       c i
Purpose: Simplifies polynomial coefficient extraction from the given sum format.
        lemma card_roots_eq_of_ncard_rootSet {k : ℕ} {P : Polynomial ℝ}
            (h_deg : P.natDegree = k)
            (h_ncard : (P.rootSet ℝ).ncard = k) :
            P.roots.card = k
Purpose: Shows that a polynomial with 𝑘 distinct real roots and degree 𝑘 has exactly 𝑘 roots counting multiplicities.
        lemma multiset_map_erase_prod_sum {R : Type*} [CommRing R] (s :
        Multiset R) :
            (s.map (fun x => (s.erase x).prod)).sum = s.esymm (s.card - 1)
Purpose: Multiset identity relating the sum of element-wise excluded products to 𝐸 𝑘 −1 .
       lemma multiset_map_erase_prod_esymm_two {R : Type*} [CommRing R]
       (s : Multiset R) :
           (s.map (fun x => (s.erase x).prod)).esymm 2 = s.prod * s.esymm
       (s.card - 2)
Purpose: Multiset identity relating the 2nd elementary symmetric polynomial of excluded products to 𝐸 𝑘 𝐸 𝑘 −2 .
        lemma multiset_sum_sq_eq {R : Type*} [CommRing R] (s : Multiset R)
        :
            (s.map (fun x => x^2)).sum = (s.sum)^2 - (2 : R) * s.esymm 2


                                                                                                                                   23
                     LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks



Purpose: Expresses the sum of squares of a multiset in terms of its sum and its 2nd elementary symmetric
polynomial.

      lemma multiset_map_erase_prod_prod {R : Type*} [CommRing R] (s :
      Multiset R) :
          (s.map (fun x => (s.erase x).prod)).prod = s.prod ^ (s.card -
      1)
Purpose: Computes the full product of the excluded products multiset.

      lemma multiset_sum_ge_card_of_prod_ge_one (W : Multiset ℝ) (hw :
      ∀ x ∈ W, 0 ≤ x) (hp : (1 :   ℝ) ≤ W.prod) :
          (W.card : ℝ) ≤ W.sum
Purpose: The AM-GM inequality specialized for a multiset whose product is at least 1, proving that the sum is
bounded below by its cardinality.
Proof Body Outline
                              Í
   1. Define 𝑃 as the sum 𝑖 ∈Finset.Icc 0𝑘 monomial 𝑖 ( 𝑐𝑖 ) and 𝑃 𝑅 as 𝑃.map (algebraMap ℤ ℝ).
   2. Apply coeff_of_sum_Icc to assert 𝑃 𝑅 .coeff 𝑖 = ( 𝑐𝑖 : ℝ) for 𝑖 ∈ {0, 1, 2, 𝑘 }.
   3. Establish 𝑃 𝑅 .roots.card = 𝑘 using card_roots_eq_of_ncard_rootSet and the natural degree injectivity.
   4. Establish that 𝑃 𝑅 .splits (RingHom.id ℝ) follows from Polynomial.splits_iff_card_roots.
   5. Let 𝑠 = 𝑃 𝑅 .roots. Invoke Vieta’s formulas (Polynomial.coeff_eq_esymm_roots_of_splits) to express
      𝑐0 , 𝑐1 , and 𝑐2 in terms of 𝑠.esymm 𝑖.
   6. Define multisets 𝑌 and 𝑍 matching the theoretical blueprint.                     Use multiset_sum_sq_eq,
      multiset_map_erase_prod_sum, and multiset_map_erase_prod_esymm_two to show that the sum
      of the squared elements of 𝑍 expands algebraically to exactly ( 𝑐12 − 2𝑐0 𝑐2 : ℝ) = ( 𝐾 ( 𝑐) : ℝ).
   7. Use multiset_map_erase_prod_prod to find 𝑍.prod = 𝑐𝑘 ((−1) 𝑘 𝑐0 ) 𝑘 −1 .
   8. Observe that since 𝑐0 and 𝑐𝑘 are non-zero integers, their algebraic combination 𝑍.prod represents a non-zero
      integer, so its square (the product of 𝑊 = 𝑍 2 ) is ≥ 1.
   9. Feed 𝑊 to multiset_sum_ge_card_of_prod_ge_one to deduce that 𝑊.sum ≥ 𝑊.card.
  10. Using 𝑊.card = 𝑘 and 𝑊.sum = ( 𝐾 ( 𝑐) : ℝ), deduce ( 𝑘 : ℝ) ≤ ( 𝐾 ( 𝑐) : ℝ). Use norm_cast to translate this
      back to ( 𝑘 : ℤ) ≤ 𝐾 ( 𝑐).




                                                                                                                     24
