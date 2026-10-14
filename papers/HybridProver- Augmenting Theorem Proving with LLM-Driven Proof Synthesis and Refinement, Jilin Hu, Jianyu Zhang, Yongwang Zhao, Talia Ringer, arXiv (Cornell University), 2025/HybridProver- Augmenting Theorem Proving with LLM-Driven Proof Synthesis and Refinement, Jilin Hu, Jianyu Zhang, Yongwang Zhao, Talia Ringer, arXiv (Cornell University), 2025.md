                                             HybridProver: Augmenting Theorem Proving with LLM-Driven Proof
                                                                Synthesis and Refinement
                                                         Jilin Hu1,2 , Jianyu Zhang2 , Yongwang Zhao2,3,* , Talia Ringer4
                                                          1
                                                            Shanghai Artificial Intelligence Laboratory, Shanghai, China
                                            2
                                              School of Cyber Science and Technology, College of Computer Science and Technology,
                                                                        Zhejiang University, Hangzhou, China
                                         3
                                           State Key Laboratory of Blockchain and Data Security, Zhejiang University, Hangzhou, China
                                            4
                                              Siebel School of Computing and Data Science, University of Illinois Urbana-Champaign,
                                                                              Champaign, United States
                                                                             *
                                                                                 Corresponding author: zhaoyw@zju.edu.cn
                                                               Abstract                              ing the broader adoption of formal verification. To
                                                                                                     address this challenge, automated theorem proving
                                             Formal methods play a crucial role in ensur-
arXiv:2505.15740v2 [cs.FL] 27 Aug 2026




                                             ing the reliability of critical systems through
                                                                                                     has emerged as a paradigm to streamline formal
                                             rigorous mathematical verification. However,            verification (Barrett et al., 2011; De Moura and
                                             their adoption remains limited due to the labor-        Bjørner, 2008; Riazanov and Voronkov, 2002; Wei-
                                             intensive nature of manual proof construction.          denbach et al., 1996), but its large proof-search
                                             Recent advances in large language models                space and limited adaptability to diverse proof sce-
                                             (LLMs) have opened new opportunities for au-            narios have constrained its practicality.
                                             tomated theorem proving. Two main paradigms                Recent advances in large language models
                                             have emerged: stepwise tactic-based genera-
                                                                                                     (LLMs) have opened new frontiers for automated
                                             tion and whole-proof synthesis. While both
                                             approaches have complementary strengths, ex-            theorem proving. Generating formal proofs can be
                                             isting work largely treats them in isolation. In        viewed as a structured form of code generation, a
                                             this work, we propose HybridProver, a unified           setting in which LLMs have demonstrated strong
                                             framework that integrates whole-proof synthe-           capabilities (Chen et al., 2021; Jiang et al., 2024).
                                             sis and tactic-based generation through proof           Moreover, unlike natural language outputs, formal
                                             sketches as an intermediate representation. This        proofs can be mechanically verified by ITPs, e.g.,
                                             design enables the reuse of partially correct
                                                                                                     Isabelle/HOL (Nipkow et al., 2002), Rocq (Sozeau
                                             proof structures while effectively combining
                                             high-level planning with fine-grained reasoning.
                                                                                                     et al., 2025), and Lean (Moura and Ullrich, 2021),
                                             We implement HybridProver in Isabelle/HOL               providing a principled way to mitigate hallucina-
                                             and post-train two 7B-scale LLMs on our op-             tion through external verification.
                                             timized Isabelle datasets. Experiments on                  Existing LLM-based approaches to automated
                                             the miniF2F Isabelle benchmark achieved a               theorem proving typically fall into two categories:
                                             73.8% success rate and improved upon the                (1) whole-proof synthesis that produces complete
                                             previous state of the art (61.9%), demonstrat-          formal proof attempts in a single pass (Xin et al.,
                                             ing that lightweight models, when combined
                                                                                                     2024; Liang et al., 2025; Wang et al., 2024c), and
                                             with our approach, can effectively generate
                                             Isabelle/HOL proofs without relying on very             (2) tactic-based generation that constructs proofs
                                             large LLMs. Ablation studies further analyze            via stepwise reasoning (Zhao et al., 2024; Jiang
                                             the impact of dataset quality, training configu-        et al., 2023; Xu et al., 2026). Whole-proof synthe-
                                             rations, and sampling strategies on proof gener-        sis excels at high-level planning but is error-prone
                                             ation. All code and datasets are released.              at the level of detail, while tactic-based generation
                                                                                                     does the opposite. This suggests an opportunity to
                                         1    Introduction
                                                                                                     reuse the global structure of failed whole-proof at-
                                         The field of formal methods plays a pivotal role in         tempts while repairing their local errors with tactic-
                                         ensuring the reliability of critical systems across         level refinement.
                                         mathematics, computer science, and engineer-                   In this work, we present HybridProver, an
                                         ing (Bjørner and Havelund, 2014). By constructing           LLM-driven framework that integrates these two
                                         machine-checkable proofs over formal specifica-             paradigms through an intermediate representation
                                         tions, interactive theorem provers (ITPs) provide           in the form of proof sketches. Given a theorem,
                                         strong guarantees of correctness. However, the              HybridProver first generates candidate proofs us-
                                         process of developing formal proofs remains labor-          ing a whole-proof synthesis model. When these
                                         intensive and requires substantial expertise, limit-        candidates are incorrect, HybridProver abstracts
them into proof sketches that retain the high-level           LLM-based automated theorem proving that
structure while omitting low-level details. These             unifies whole-proof synthesis and tactic-based
sketches are then verified and refined using a tactic-        generation. By using proof sketches as inter-
based generation model, together with existing                mediate representations, HybridProver con-
symbolic tools such as hammers (Blanchette et al.,            nects high-level proof planning with low-level
2016), to produce a final whole proof.                        tactic refinement. It also enables imperfect
   This design highlights a general principle for             whole-proof candidates to be reused and re-
LLM-based formal reasoning: separating high-                  fined rather than discarded.
level planning from low-level refinement and bridg-
                                                             • We implement HybridProver in Isabelle/HOL
ing them through verifiable proof sketches. Such
                                                               and construct optimized training datasets. We
sketches can still be checked for structural valid-
                                                               further fine-tune two 7B-scale LLMs for both
ity, enabling tactic-based generation to proceed
                                                               whole-proof synthesis and tactic-based gener-
under a well-formed proof context while reusing
                                                               ation, and enhance them with reinforcement
partially correct whole-proof attempts. As a result,
                                                               learning guided by verification signals.
HybridProver can flexibly compose different mod-
els and tools, combining neural generation with              • HybridProver achieves a 73.8% success rate
symbolic reasoning in a unified framework. More                on miniF2F, improving over prior results for
broadly, HybridProver suggests a general pattern               Isabelle-based systems (61.9%). We demon-
for verifier-guided generation: reuse rejected out-            strate that lightweight models can be effec-
puts as structured intermediates and repair only the           tively adapted to proof generation through
invalid parts. This idea may also apply to structured          high-level planning and low-level tactic re-
reasoning and code generation with verifiers.                  finement. Extensive ablations highlight the
   While the ideas for HybridProver can be imple-              impact of data quality, fine-tuning hyperpa-
mented for many ITPs, we focus on Isabelle/HOL                 rameters, and sampling diversity.
(Nipkow et al., 2002), using Sledgehammer (Paul-
son, 2012) as the hammer. Compared to prior LLM-         2    Background: Why Isabelle?
based theorem-proving systems, which predomi-
                                                         We implement HybridProver in Isabelle/HOL,
nantly focus on Lean, Isabelle presents a comple-
                                                         an interactive theorem prover (ITP) widely used
mentary and relatively underexplored setting. It
                                                         for formal verification and mathematical reason-
poses additional challenges for LLM-based proof
                                                         ing (Nipkow et al., 2002). ITPs such as Isabelle,
generation due to its diverse proof styles and less
                                                         Rocq (Sozeau et al., 2025), and Lean (Moura and
standardized proof patterns, while also offering
                                                         Ullrich, 2021) provide strong correctness guaran-
unique opportunities for constructing high-quality
                                                         tees by checking proofs with small, trusted ker-
training data (see Section 2).
                                                         nels (Nipkow et al., 2002; Pierce et al., 2010). How-
   We evaluate HybridProver on the miniF2F               ever, constructing formal proofs in these systems
benchmark (Zheng et al., 2022). Our approach im-         remains labor-intensive and requires significant ex-
proves proof success rates over prior Isabelle-based     pertise (Klein et al., 2009; Gu et al., 2016; Leroy
systems. We further show that combining whole-           et al., 2016). Our choice of Isabelle as a target ITP
proof synthesis with tactic-based generation yields      addresses its unique challenges while also taking
consistent performance gains, and that integrating       advantage of its unique benefits.
symbolic tools such as Sledgehammer yields addi-
tional improvements. Beyond overall performance,         Challenges of targeting Isabelle: broad use cases.
our ablation studies highlight the importance of         Compared to prior LLM-based theorem proving
dataset quality, fine-tuning hyperparameters, and        systems, which predominantly focus on Lean, Is-
sampling diversity in LLM-based proof generation.        abelle remains relatively underexplored. This dif-
To facilitate future research, we release our datasets   ference is partly due to the nature of existing bench-
and the code of HybridProver.1                           marks such as miniF2F, which are mathematical
                                                         and better aligned with Lean’s mathlib (Moura and
Contributions:                                           Ullrich, 2021). In contrast, Isabelle is more widely
                                                         used in system verification, where proofs vary sig-
   • We propose HybridProver, a framework for
                                                         nificantly across domains and specifications. While
   1
       https://github.com/JilinHu/HybridProver           Isabelle provides a large and diverse corpus of
                                                                                       HybridProver

     Input & Prompt
                                                                                                                                             Prover Output
                                                      Whole-proof
                                                                                          Proof Filter
       Theorem                                      Synthesis Model
       list_reverse:
                                                                                                                       Checker         Yes
       "rev (rev xs) = xs"                                 post
                                            optimized    training                                                        check with
                                             dataset                                                                     Isabelle
       Prompt Template
       Generate Isabelle
       proof based on                      lightweight              Generate initial      Remove invalid or                                  Final Whole Proof
                                               LLM
       the theorem....                                          candidate proofs          redundant proofs                   No              verified by Isabelle


       High-Level Planning (Whole-proof Synthesis)


                                                                                                                                             Prover Output
  Sketch Builder                                           Tactic-based                     Sketch Refiner                                      proof (induction xs)
                             Example Sketch
                                                         Generation Model                                                                         case Nil
                                                                                                                                                  then show ?case
                             proof (induction xs)                                                                       Checker                      by simp
                               case Nil                                                                                                Yes        next
                               then show ?case                                                                            check with              case (Cons a xs)
                                  sorry                                                                                                           then show ?case
                               next                                                                                       Isabelle
                                                                                                                                                     by simp
                               case (Cons a xs)                                                                                                 qed
                               then show ?case
   Construct a proof                                      Generate tactics for
                                  sorry                                                    Iteratively refine proof
     sketch with             qed                          each subgoal with                                                                  Final Whole Proof
                                                                                             sketch with tactics                             verified by Isabelle
     placeholders                                          Sledgehammer                                                       No

   Low-level Refinement (Tactic-based Generation)



                                                         Figure 1: HybridProver Framework Overview


formal proofs (over 200K theorems, compared to                                                      expose the high-level structure.
Lean’s 140K and Rocq’s 71K (Drori et al., 2025;                                                        Importantly, these two styles are complemen-
Reichel et al., 2023)). This diversity makes it chal-                                               tary: Isar can serve as a high-level proof sketch,
lenging for LLMs to learn consistent proof patterns                                                 while apply-style tactics can discharge low-level
across domains.                                                                                     subgoals. This observation motivates our de-
                                                                                                    sign, where we treat Isar-style proofs as structured
Advantages of targeting Isabelle: two proof                                                         sketches and use tactic-based generation to refine
styles. A distinctive feature of Isabelle is the                                                    them. By leveraging both styles, we construct a
coexistence of two proof styles: apply-style                                                        unified framework that bridges high-level planning
proofs (Wenzel, 2025) and Isar proofs (Wenzel and                                                   and low-level reasoning, and enables more effec-
Team, 2025). Apply-style proofs construct deriva-                                                   tive proof generation.
tions through stepwise tactic application, where a
tactic is a primitive proof step that refines the cur-                                               3       HybridProver
rent proof state to an updated state. In contrast, Isar
                                                                                                     3.1        Framework Overview
proofs provide structured, human-readable proof
scripts that resemble mathematical reasoning.                                                       Our framework is depicted in Figure 1. The work-
                                                                                                    flow can be divided into the following steps:
 Listing 1: Isar and apply-style proof example                                                         Step 1: Prompt Construction. HybridProver
 theorem list_reverse: "rev (rev xs) = xs"                                                          takes as input a formal theorem statement in Is-
 Isar proof:             |apply-style proof:                                                        abelle syntax. The statement is concatenated with
 proof(induction xs)     |apply(induction xs)
 case Nil                | apply auto                                                               a structured prompt template (Listing 2) that speci-
 then show ?case by simp | done                                                                     fies the task and output format, and is then fed into a
 next case (Cons a xs)   |                                                                          post-trained whole-proof synthesis model. Trained
 then show ?case by simp |
 qed                     |                                                                          on optimized Isabelle proof data, the model gener-
                                                                                                    ates candidate proofs by capturing common proof
  Listing 1 illustrates these two styles on the same                                                patterns and basic reasoning structures.
theorem, which states that reversing a list twice                                                      Step 2: Whole-Proof Synthesis and Filtering.
does not change the list. Apply-style proofs are                                                    The whole-proof synthesis model generates n can-
concise but opaque, requiring inspection of inter-                                                  didate proofs (we set n = 128 following prior
mediate proof states, whereas Isar proofs explicitly                                                work) in parallel to explore diverse proof paths. A
lightweight proof filter is then applied to remove       Algorithm 1 HybridProver workflow
invalid or redundant outputs, reducing the cost of       Require: Theorem L, prompt template T
subsequent verification. The filter enforces basic       Ensure: Valid Isabelle proof or failure
                                                          1: P ← LLMwhole (L, T ) // Step 1: whole-proof synthesis
syntactic constraints on Isabelle proofs. Outputs         2: Psyntax ← proof _filter (P)              // Step 2: filtering
that do not conform to the required JSON format           3: Pvalid ← ∅
or do not start with valid Isabelle keywords (e.g.,       4: parallel for p ∈ Psyntax do
                                                          5: if check(p, L) then
proof, apply, or by) are discarded. The remaining         6:     Pvalid ← Pvalid ∪ {p}
candidates are passed to the Isabelle checker for         7: end if end parallel
                                                          8: if Pvalid ̸= ∅ then
formal verification, noting that syntactic validity       9:     return any p ∈ Pvalid
does not guarantee correctness.                          10: end if
   With concurrent verification, multiple candidates     11: S ← {replaceSorry(p) | p ∈ P}               // Step 3: sketch
                                                             construction
can be checked simultaneously. If any candidate          12: Svalid ← {s ∈ S | check(s, L)}
passes verification, the system returns the corre-       13: parallel for s ∈ Svalid do        // Steps 4–5: refinement
sponding proof and terminates early. Otherwise,                      . , Gn ← parseSubgoals(s)
                                                         14: G1 , . .S
                                                         15: T ← n
                                                                                                                     
                                                                        i=1 LLMstep (Gi ) ∪ Sledgehammer(Gi )
the valid candidates are forwarded to the next stage     16: prefined ← substituteSorry(s, T )
for further processing.                                  17: if IsabelleVerify(prefined , L) then
   Step 3: Proof Sketch Construction. If none            18:      return prefined
                                                         19: end if end parallel
of the n candidate proofs passes the checker, the        20: return failure
system invokes a sketch builder to transform syntac-
tically valid candidates into proof sketches, rather
than discarding them. The key idea is to lift detailed   the Isabelle checker. These two components are
proof attempts to a higher-level representation that     complementary, as each can solve subgoals that
preserves global structure while abstracting away        the other fails to prove. In contrast to whole-proof
low-level tactic details.                                synthesis, which focuses on high-level structure
   Unlike prior work (Jiang et al., 2023), we con-       and premise selection, this stage operates on lo-
struct proof sketches directly from LLM-generated        calized subgoals and concrete proof steps. In our
candidate proofs. The sketch builder validates each      framework, premise selection is incorporated into
subgoal proof independently: when checking one           the training of the whole-proof synthesis model,
subgoal, it replaces the proofs of the remaining         allowing the refinement stage to leverage richer
subgoals with sorry, allowing Isabelle to verify the     contextual information for subgoal solving.
current proof step under assumed completion of the          Step 5: Proof Refinement. In the final stage,
others. Correct subgoal proofs are preserved, while      the sketch refiner replaces the sorry placeholders
failed ones are replaced with sorry. The resulting       in the proof sketch with the corresponding proof
sketch is therefore a partially verified intermediate    steps generated in Step 4, yielding a complete Is-
representation that reuses correct local proof steps     abelle proof. The refined proof is then submitted
and leaves only unresolved subgoals for refinement.      to the Isabelle checker for final verification. If ver-
The resulting sketches are then validated by the Is-     ification fails, the system performs backtracking
abelle checker to remove structurally invalid cases,     by substituting alternative tactics for unresolved
such as incorrect proof methods or missing lemmas.       subgoals and re-verifying the reconstructed proof.
Since low-level details are abstracted away, most        This process repeats until a valid proof is found or
sketches pass this stage. With concurrent verifica-      all candidates are exhausted. If successful, the sys-
tion, this process remains efficient.                    tem returns the verified proof; otherwise, it reports
   Step 4: Subgoal Refinement and Tactic Gener-          failure. This iterative refinement process bridges
ation. Given a proof sketch, we refine each subgoal      the gap between abstract proof sketches and com-
marked with sorry into a verifiable proof step us-       plete proof code.
ing a tactic-based generation model. This model             The overall workflow of HybridProver is sum-
combines a post-trained LLM for tactic generation        marized in Algorithm 1. Given a theorem L and
with the Isabelle tool Sledgehammer.                     a prompt template T , the whole-proof synthesis
   For each unresolved subgoal, the LLM generates        model generates candidate proofs, which are fil-
n candidate tactics in parallel, while Sledgeham-        tered and verified in parallel. If a valid proof is
mer independently attempts to discharge the same         found, the system terminates early. Otherwise,
subgoal. The resulting candidates are validated by       syntactically valid candidates are converted into
proof sketches and validated. For each valid sketch,           Table 1: Dataset Sources and Configurations
subgoals are extracted and solved using a tactic-
                                                             Data Source      Purpose      Proof Style Samples
based generation model together with Sledgeham-                                            apply-style 116,308
                                                                            Train (95%)
mer. The resulting tactics are used to refine the                                           Isar-style  35,803
                                                                AFP
sketch into a complete proof, which is then veri-                             Test (4%)         –       6,400
fied by Isabelle. This process iterates until a valid                      Validation (1%)      –        1,600
                                                                                           apply-style 36,038
proof is found or all candidates are exhausted. An              STD         Train (100%)
                                                                                            Isar-style  9,018
Isabelle running example is shown in Section A.3.

3.2   Dataset optimization                                  After supervised fine-tuning, we further optimize
We construct our Isabelle dataset from the Stan-         the model using reinforcement learning. We adopt
dard Library (STD) and the Archive of Formal             Group Relative Policy Optimization (GRPO) (Shao
Proofs (AFP) using PISA (Jiang et al., 2021). To         et al., 2024), where Isabelle serves as the reward
reduce noise in raw formalization data, we apply         provider. The training data consist of a randomly
a cleaning pipeline that extracts theorem–proof          sampled 1% subset of the optimized dataset. A
pairs, removes formatting artifacts (e.g., redundant     key advantage of theorem proving is that generated
whitespace), eliminates comments, and normalizes         proofs are formally verifiable, making Isabelle an
symbols. Each proof is then converted into a struc-      accurate and reliable reward signal. Specifically,
tured format, {Isabelle_proof: proof code}, to stan-     proofs that pass verification receive the highest re-
dardize the target output. We further partition the      ward, partially correct but invalid proofs receive a
dataset according to Isabelle’s two proof styles:        lower reward, and syntactically invalid or rejected
Isar and apply-style proofs. This distinction aligns     outputs receive no reward. We additionally intro-
with our two-stage framework: Isar proofs capture        duce penalties to discourage degenerate behaviors,
high-level structure, while apply-style proofs focus     such as generating placeholders (e.g., sorry) or
on tactic-level reasoning.                               trivial outputs. The final reward combines verifica-
   To improve training efficiency and data quality,      tion feedback with these structural penalties. This
we filter examples based on proof length. Apply-         design encourages the model to generate complete,
style proofs in raw data are typically short (1–5        verifiable proofs while avoiding shortcuts that by-
steps), so we retain only concise instances to en-       pass actual reasoning.
courage precise tactic generation. Isar proofs are
longer (typically 11–30 steps), and we remove            4     Experiments
overly short or excessively long examples (outside
                                                         4.1    Setup
5–50 steps) to balance structural richness and learn-
ability. The resulting dataset provides a cleaner        Dataset. We construct the training dataset from
and more structured training signal for both global      the Isabelle Standard Library (STD) and the
proof generation and local tactic refinement.            Archive of Formal Proofs (AFP) using PISA (Jiang
                                                         et al., 2021), following the preprocessing described
3.3   Model Training                                     in Section 3.2. AFP is split into 95%/1%/4% for
We first fine-tune two models corresponding to the       training/validation/test following prior work (Jiang
two stages of HybridProver. The whole-proof syn-         et al., 2022, 2023), while STD is used entirely for
thesis model is trained on the Isar dataset to capture   training due to its dependency on AFP. The dataset
high-level proof structure, while the tactic-based       statistics are summarized in Table 1. For evaluation,
generation model is trained on the apply-style           we use the miniF2F benchmark (Zheng et al., 2022),
dataset to generate fine-grained proof steps. Both       a widely used dataset consisting of 488 mathemat-
models are obtained via supervised fine-tuning           ical problems. Following prior work, we report
of pretrained models. To improve training effi-          results on the 244 test problems. miniF2F is used
ciency and reduce memory consumption, we adopt           exclusively for evaluation in our pipeline and is
LoRA (Hu et al., 2021), which freezes the base           not included in either SFT or GRPO data; all post-
model and introduces low-rank trainable adapters.        training examples are drawn from AFP and STD.
This allows us to scale to larger models while main-     The evaluation inputs provide theorem statements
taining performance comparable to full fine-tuning       rather than target proofs, which substantially limits
under limited computational resources.                   direct proof-target leakage.
Experimental setup. In initial small-model ex-                To analyze the contribution of each component,
periments, we generated proofs using more than 15          we evaluate several variants of HybridProver (Ta-
different open-source models. In the end, we chose         ble 3). The whole-proof synthesis model alone
Qwen-Coder-7B as our base model for further train-         achieves 45.9%, while the tactic-based generation
ing because it had the highest proof success rate.         model achieves 39.3%. A simple combination of
For LLM fine-tuning and reinforcement learning             the two models (taking the union of their results)
(RL), we use 8 NVIDIA A40 GPUs. Fine-tuning                improves the success rate to 49.6%. In miniF2F,
our models with LoRA on the whole optimized Is-            some theorems are simple and require only a small
abelle dataset and 3 epochs takes around 200 GPU           number of proof steps. In such cases, the whole-
hours, while RL with GRPO takes around 100 GPU             proof synthesis model tends to generate verbose
hours. The cost of ablation studies for other LLMs         and often incorrect Isar proofs, while the tactic-
and configurations is not included. Detailed train-        based generation model is more effective at pro-
ing configurations can be found in Section A.5. For        ducing concise solutions. This explains the com-
evaluation, we use a 128-core Intel CPU with 256           plementary behavior of the two models. Integrat-
GB of RAM while setting the concurrent processes           ing Sledgehammer with heuristics further improves
to 64. The full evaluation required nearly 10,000          performance by approximately 2%, suggesting that
CPU hours. At inference time, computation is di-           the tactic-based LLM already covers most subgoals
vided among whole-proof sampling and checking,             that can be solved by symbolic tools.
independent subproof and sketch validation, tactic
generation, Sledgehammer, and repeated verifica-               Table 3: Ablation results on Isabelle miniF2F
tion during backtracking.
                                                              Variant                                 Test (%)
4.2   Results and Analysis                                    Whole-proof synthesis model                 45.9
                                                              Tactic-based generation model               39.3
We evaluate HybridProver on the Isabelle miniF2F              Whole-proof + tactic generation             49.6
test set, using Sledgehammer as the baseline. Fol-            Tactic generation + sketch refinement       71.3
lowing prior work, we use a sampling size of 128              HybridProver                                73.8
when generating candidate proofs. The results are
shown in Table 2. Sledgehammer with heuristics
                                                              Combining tactic-based generation with proof
achieves a 20.9% success rate without LLM as-
                                                           sketch refinement significantly boosts performance
sistance. Recent LLM-based approaches signifi-
                                                           to 71.3%, demonstrating the effectiveness of
cantly improve over this baseline, reaching 30%–
                                                           reusing partially correct proofs. Interestingly, most
50% success rates. With the integration of whole-
                                                           sketches constructed from the whole-proof synthe-
proof synthesis and tactic-based generation, Hy-
                                                           sis model are structurally correct: when evaluated
bridProver achieves a success rate of 73.8%, out-
                                                           without detailed tactics, sketches achieve up to
performing prior Isabelle-based systems and im-
                                                           90% success rate. This indicates that high-level
proving over the previous best result of 61.9% from
                                                           proof structure is often captured correctly even
ProofAug (Liu et al., 2025) by 11.9%.
                                                           when local reasoning fails. Finally, HybridProver
 Table 2: Proof success rates on the Isabelle miniF2F      achieves a 73.8% success rate, showing that com-
                                                           bining whole-proof synthesis with tactic-based re-
 Method (using Isabelle)       Base Model       Test (%)   finement leads to substantial improvements, while
 Sledgehammer                       –             10.4     symbolic tools provide additional, though smaller,
 Sledgehammer + heuristics          –             20.9     gains. Besides, lightweight models can effectively
 Thor                               –             29.9     generate Isabelle/HOL proofs when combined with
 Thor + expert iteration            –             35.2     our approach without relying on very large LLMs.
 DSP                              Codex           39.3     Qualitatively, remaining failures can arise from
 POETRY                       ProofGPT(1.3B)      42.2     malformed or unparseable Isar structure, halluci-
 Subgoal-Prover                GPT-3.5-Turbo      45.5
 LEGO-Prover                   GPT-3.5-Turbo      50.0     nated or missing premises, unsuitable local tactics
 Lyra                             GPT-4           51.2     and exhaustion of retained tactic combinations in
 SubgoalXL                      Llama3-8B         56.1     multi-subgoal sketches.
 ProofAug                    Deepseek-math-7B     61.9
                                                              In our pipeline, SFT adapts the models to the Is-
 HybridProver                Qwen-Coder-7B        73.8
                                                           abelle output format and the Isar/apply-style proof
patterns, while GRPO subsequently optimizes them
                                                           RA1: Data quality and training hyperparam-
using Isabelle-derived verification rewards. How-
                                                           eters (e.g., learning rate and epochs) signifi-
ever, the current ablations do not hold all other fac-
                                                           cantly affect performance, while LoRA rank
tors fixed to isolate the individual gains from SFT
                                                           has limited impact.
and GRPO. We therefore attribute the observed im-
provements to the post-training pipeline as a whole
rather than to either stage separately.                  RQ2: Does sampling diversity impact the re-
                                                         sults? We vary sampling parameters during in-
                                                         ference, including temperature T and sampling
                                                         rate. While proof generation requires stable outputs
4.3   Additional Ablation Studies                        to ensure syntactic correctness, prior work adopts
                                                         higher temperatures combined with multiple sam-
                                                         ples to improve success rates (e.g., T =1.0 in LISA
RQ1: How do data quality and training param-             and T =1.2 in Thor). In our setting, we evaluate the
eters affect fine-tuning performance? We use             trained Qwen-Coder-7B model for whole proofs
the original Qwen-Coder-7B model as a baseline.          with T ∈ [0.3, 1.2] and sampling rates from @32
Since it is only generically pretrained, it struggles    to @128 (Figure 2). We observe that moderate tem-
to follow our task-specific instructions. To mitigate    peratures (0.6–0.9) achieve the best performance,
this, we prompt the model with a structured format       while both lower and higher values degrade success
(Listing 2) and enforce constrained outputs.             rates. Error analysis shows that excessively high
                                                         T leads to frequent hallucination of non-existent
   We then fine-tune the whole-proof model on vari-      facts, causing verification failures in Isabelle. We
ants of our optimized Isabelle dataset under dif-        also find that increasing the sampling rate improves
ferent hyperparameter settings, including learning       performance, indicating the benefit of broader ex-
rate, LoRA rank, and number of training epochs.          ploration during inference.
Our results show that data quality, learning rate,
and training duration have a significant impact on
                                                           RA2: Sampling diversity influences results:
performance. In particular, training on raw data
                                                           moderate temperature works best, and higher
leads to noisy outputs with redundant tokens and
                                                           sampling rates improve success rates.
formatting artifacts, which degrades proof genera-
tion quality. After applying the data cleaning pro-
cedure described in Section 3.2, the success rate        RQ3: Does providing premises, few-shot exam-
on miniF2F improves by at least 10% across all           ples, and labels help with proving? Many Is-
training settings, highlighting the importance of        abelle theorems rely on auxiliary premises. We
dataset quality.                                         therefore include premises in the training data and
                                                         train the model to both select relevant premises
   The ablation results for training parameters are      and construct proofs accordingly. This reduces
shown in Figure 2. For training epochs, we find          undefined fact errors by around 50%, indicat-
that 3 epochs yield the best performance, while          ing that the model learns to avoid hallucinating
longer training leads to overfitting. This is partly     nonexistent premises. However, this improve-
due to the mismatch between the training data (cov-      ment does not translate into better performance
ering mathematics, software, and systems) and the        on miniF2F, where most theorems do not require
evaluation benchmark (miniF2F, which is purely           external premises.
mathematical). For the learning rate, we experi-            For few-shot prompting, we add three represen-
ment with values ranging from 10−4 to 5 × 10−7           tative examples (Listing 3) to the prompt, cover-
using a warm-up and cosine decay schedule, and           ing simple apply-style proofs, induction proofs,
find that 10−5 yields the best performance. Fi-          and Isar proofs. We observe no performance gain
nally, we evaluate different LoRA ranks (8–256)          for either the trained Qwen-Coder-7B or the base
and observe that the rank has minimal effect on          model, suggesting that the model already captures
performance, despite changing the number of train-       the required syntax and proof patterns. We fur-
able parameters. These findings provide practical        ther augment each theorem with its source file path
guidance for fine-tuning LLMs in theorem proving         as a label, aiming to provide coarse-grained con-
tasks.                                                   textual information for premise selection. While
                                                                                   44




                  Accuracy (%)




                                                                    Accuracy (%)
                                 40                                                42
                                                                                   40
                                 30
                                                                                   38
                                 20                                                36
                                      e−4 5e−5 e−5 5e−6 e−6 5e−7                        8       16    32    64         128     256
                                          (a) Learning Rate                                     (b) LoRA Rank
                                 45                                                40
                 Accuracy (%)




                                                                   Accuracy (%)
                                                                                   35
                                 40
                                                                                   30
                                                                                                       @32      @128
                                 35
                                                                                   25
                                       1    3         6     10                              0.3       0.6     0.9            1.2
                                            (c) Epoch                                       (d) Sampling Temperature

                 Figure 2: Ablation results under different training and sampling configurations.


this reduces the search space in principle (e.g., en-                      Prior work on LLM-based proof generation also
couraging the model to retrieve premises from the                       varies by what the LLM is used for and by its in-
corresponding theory file), it again yields negli-                      put context. Some work (Yang et al., 2023; Zhao
gible improvements on miniF2F, likely due to its                        et al., 2024; Polu and Sutskever, 2020; Lin et al.,
homogeneous mathematical domain.                                        2024; Liang et al., 2025; Wang et al., 2024a; Achim
                                                                        et al., 2025) uses LLMs to generate tactic-based
    RA3: Additional signals such as premises,                           proofs step by step. Other work (Xin et al., 2024;
    few-shot examples, and labels provide limited                       First et al., 2023; Wang et al., 2024c; Ren et al.,
    gains on miniF2F.                                                   2025; Shao et al., 2025; Wang et al., 2025; Lin
                                                                        et al., 2025; Chen et al., 2025; Xu et al., 2026)
                                                                        uses LLMs to generate the whole proof at once.
5    Related Work                                                       For example, Polu (Polu and Sutskever, 2020) and
                                                                        FVEL (Lin et al., 2024) ask LLM to generate the
The use of LLMs to automate theorem proving                             next tactic based on the current proof state. Baldur
was pioneered by Polu and Sutskever (Polu and                           (First et al., 2023) makes LLMs generate whole
Sutskever, 2020). Subsequent work has focused                           proofs based on the input theorem. HybridProver
on improving the reasoning capabilities of LLM-                         organically combines these two approaches and
based systems. Open-source interactive environ-                         gets a better proof quality. After the proof gener-
ments like Leandojo (Yang et al., 2023) for Lean,                       ation, some works also focus on proof search that
and PISA (Jiang et al., 2021) and Isabelle-client                       chooses appropriate generated responses with dif-
(Koepke et al., 2022) for Isabelle, make it eas-                        ferent algorithms, such as best-first search (Polu
ier to build LLM-based tools for automated the-                         and Sutskever, 2020; Han et al., 2022; Yang et al.,
orem proving. Likewise, open-source datasets and                        2023; Xin et al., 2025), and Monte Carlo tree search
benchmarks like miniF2F (Zheng et al., 2022) and                        (Wang et al., 2023; Lample et al., 2022; Xin et al.,
Proofnet (Azerbayev et al., 2023) provide the basis                     2024). Despite the improvement, these search al-
for evaluation. Automation often uses premise se-                       gorithms often require additional computational
lection prior to proof generation to find relevant                      resources that are non-trivial. Besides, a few works
premises (Yang et al., 2023; Jiang et al., 2022;                        try to integrate hammers and sketches to improve
Wang et al., 2024b; Mikuła et al., 2023). For exam-                     the performance (Jiang et al., 2022, 2023; Mikuła
ple, LEGO (Wang et al., 2024b) builds a growing                         et al., 2023; Zhao et al., 2024; Yang et al., 2023; Liu
library and retrieves premises from it, while Thor                      et al., 2025). For instance, DSP (Jiang et al., 2023)
(Jiang et al., 2022) delegates premise selection to                     generates proof sketches with subgoals and uses
hammers during the proving process. In Hybrid-                          hammers to boost the proof success rate. Recent
Prover, we ask both the trained LLM and Sledge-                         work (Ospanov et al., 2025; Ding et al., 2026) has
hammer in Isabelle to perform premise selection.
also explored agent-based approaches to enhance         that the model is trained on existing proof corpora,
the reasoning capabilities of LLMs.                     which may bias it toward familiar proof patterns.
   HybridProver differs from them in three aspects.     As a result, its ability to generalize to novel or sig-
First, most prior work focuses on Lean, while we        nificantly different proof structures remains limited.
study another important ITP called Isabelle. Sec-       In addition, our empirical conclusions are limited to
ond, we not only integrate hammers but also post-       miniF2F and do not establish generalization across
train LLMs based on our optimized dataset to im-        broader Isabelle/HOL domains.
prove the performance. Third, we build the proof
sketch mechanically from the whole proof, which
bridges the gap between whole-proof synthesis and       References
tactic-based generation, while other work, such         Tudor Achim, Alex Best, Alberto Bietti, Kevin Der,
as DSP, builds sketches from informal proofs by           Mathïs Fédérico, Sergei Gukov, Daniel Halpern-
prompting another LLM.                                    Leistner, Kirsten Henningsgard, Yury Kudryashov,
                                                          Alexander Meiburg, Martin Michelsen, Riley Pat-
                                                          terson, Eric Rodriguez, Laura Scharff, Vikram
6   Conclusion and Future Work                            Shanker, Vladmir Sicca, Hari Sowrirajan, Aidan
                                                          Swope, Matyas Tamas, and 4 others. 2025. Aristo-
We introduced HybridProver, an LLM-driven                 tle: Imo-level automated theorem proving. Preprint,
framework for automated theorem proving that uni-         arXiv:2510.01346.
fies whole-proof synthesis and tactic-based gen-
eration through proof sketches as an intermediate       Sidney Amani, Alex Hixon, Zilin Chen, Christine
                                                          Rizkallah, Peter Chubb, Liam O’Connor, Joel
representation. This design enables effective inter-      Beeren, Yutaka Nagashima, Japheth Lim, Thomas
action between global planning and local reason-          Sewell, and 1 others. 2016. Cogent: Verifying
ing, further enhanced by automated tools such as          high-assurance file system implementations. ACM
hammers. In addition, we construct optimized Is-          SIGARCH Computer Architecture News, 44(2):175–
                                                          188.
abelle datasets and train LLMs via both supervised
fine-tuning and reinforcement learning guided by        Zhangir Azerbayev, Bartosz Piotrowski, Hailey
formal verification signals. Our implementation of        Schoelkopf, Edward W Ayers, Dragomir Radev, and
HybridProver in Isabelle achieves a proof success         Jeremy Avigad. 2023. Proofnet: Autoformalizing
                                                          and formally proving undergraduate-level mathemat-
rate of 73.8% on miniF2F under our evaluation             ics. arXiv preprint arXiv:2302.12433.
setting.
   In future work, we plan to integrate more ad-        Clark Barrett, Christopher L Conway, Morgan Deters,
vanced proof search techniques into the tactic-           Liana Hadarean, Dejan Jovanović, Tim King, Andrew
                                                          Reynolds, and Cesare Tinelli. 2011. cvc4. In Com-
based generation process to improve efficiency. Be-       puter Aided Verification: 23rd International Confer-
yond miniF2F, we plan to evaluate HybridProver            ence, CAV 2011, Snowbird, UT, USA, July 14-20,
on broader Isabelle/HOL domains using carefully           2011. Proceedings 23, pages 171–177. Springer.
defined AFP-based evaluation sets. We also plan
                                                        Dines Bjørner and Klaus Havelund. 2014. 40 years
to develop a more user-friendly integrated system         of formal methods. In FM 2014: Formal Methods,
to facilitate practical adoption.                         pages 42–61, Cham. Springer International Publish-
                                                          ing.
Limitations
                                                        Jasmin Christian Blanchette, Cezary Kaliszyk,
One limitation of HybridProver lies in its rela-           Lawrence C Paulson, and Josef Urban. 2016.
                                                           Hammering towards qed. Journal of Formalized
tively simple proof search strategy during the proof       Reasoning, 9(1):101–148.
sketch refinement stage. As the number of sub-
goals increases, the refinement and evaluation pro-     Tej Chajed, Joseph Tassarotti, M Frans Kaashoek, and
cess becomes increasingly inefficient, leading to         Nickolai Zeldovich. 2019. Verifying concurrent,
                                                          crash-safe systems with perennial. In Proceedings
substantial computational overhead. Moreover, Hy-         of the 27th ACM symposium on operating systems
bridProver relies heavily on the underlying theo-         principles, pages 243–258.
rem prover (e.g., Isabelle) as a verification oracle.
While this provides accurate and reliable feedback,     Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao
                                                          Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing
it also introduces a bottleneck in terms of latency       Jin, Chenggang Li, Kaijing Ma, Cheng Ren, Jiawei
and scalability, especially when evaluating a large       Shen, Wenlei Shi, Tong Sun, He Sun, Jiahui Wang,
number of candidate proofs. Another limitation is         Siran Wang, Zhihong Wang, Chenrui Wei, and 17
  others. 2025. Seed-prover: Deep and broad rea-              Costanzo, and Tahina Ramananandro. 2018. Certi-
  soning for automated theorem proving. Preprint,             fied concurrent abstraction layers. ACM SIGPLAN
  arXiv:2507.23726.                                           Notices, 53(4):646–661.

Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,           Christopher Hahn, Frederik Schmitt, Julia J Tillman,
 Henrique Ponde de Oliveira Pinto, Jared Kaplan,              Niklas Metzger, Julian Siber, and Bernd Finkbeiner.
 Harri Edwards, Yuri Burda, Nicholas Joseph, Greg             2022. Formal specifications from natural language.
 Brockman, Alex Ray, Raul Puri, Gretchen Krueger,             arXiv preprint arXiv:2206.01962.
 Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela
 Mishkin, Brooke Chan, Scott Gray, and 39 others.           Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W
 2021. Evaluating large language models trained on             Ayers, and Stanislas Polu. 2022. Proof artifact co-
 code. Preprint, arXiv:2107.03374.                             training for theorem proving with language models.
                                                               In International Conference on Learning Representa-
Yongchao Chen, Rujul Gandhi, Yang Zhang, and                   tions.
  Chuchu Fan. 2023. Nl2tl: Transforming natural
  languages to temporal logics using large language         Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan
  models. arXiv preprint arXiv:2305.07766.                    Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and
                                                              Weizhu Chen. 2021. Lora: Low-rank adaptation of
Matthias Cosler, Christopher Hahn, Daniel Men-                large language models. Preprint, arXiv:2106.09685.
 doza, Frederik Schmitt, and Caroline Trippel. 2023.
 nl2spec: Interactively translating unstructured natu-      Jilin Hu, Fanlang Zeng, Yongwang Zhao, Zhuoruo
 ral language to temporal logics with large language           Zhang, Leping Zhang, Jianhong Zhao, Rui Chang,
 models. In International Conference on Computer               and Kui Ren. 2024. ProveriT: A Parameterized,
 Aided Verification, pages 383–396. Springer.                  Composable, and Verified Model of TEE Protection
                                                               Profile . IEEE Transactions on Dependable and Se-
Leonardo De Moura and Nikolaj Bjørner. 2008. Z3:               cure Computing, 21(06):5341–5358.
  An efficient smt solver. In International conference
  on Tools and Algorithms for the Construction and          Jilin Hu, Yongwang Zhao, Shuangquan Pan, Zuohua
  Analysis of Systems, pages 337–340. Springer.                Ding, and Kui Ren. 2025. Tacco: A framework for
                                                               ensuring the security of real-world tees via formal
Haoran Ding, Zhaoguo Wang, and Haibo Chen. 2026.
                                                               verification. IEEE Transactions on Dependable and
  Fm-agent: Scaling formal methods to large sys-
                                                               Secure Computing, 22(6):6983–6997.
  tems via llm-based hoare-style reasoning. Preprint,
  arXiv:2604.11556.
                                                            Albert Qiaochu Jiang, Wenda Li, Jesse Michael Han,
Iddo Drori, Gaston Longhitano, Mao Mao, Seunghwan             and Yuhuai Wu. 2021. Lisa: Language models of
   Hyun, Yuke Zhang, Sungjun Park, Zachary Meeks,             isabelle proofs. In 6th Conference on Artificial Intel-
  Xin-Yu Zhang, Ben Segev, Howard Yong, Nakul                 ligence and Theorem Proving, pages 378–392.
  Verma, Avi Shporer, Alon Amit, and Madeleine
   Udell. 2025. Diverse inference and verification for      Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski,
   advanced reasoning. Preprint, arXiv:2502.09955.            Konrad Czechowski, Tomasz Odrzygóźdź, Piotr
                                                              Miłoś, Yuhuai Wu, and Mateja Jamnik. 2022. Thor:
Emily First, Markus N Rabe, Talia Ringer, and Yuriy           Wielding hammers to integrate language models and
  Brun. 2023. Baldur: Whole-proof generation and              automated theorem provers. Advances in Neural In-
  repair with large language models. In Proceedings of        formation Processing Systems, 35:8360–8373.
  the 31st ACM Joint European Software Engineering
  Conference and Symposium on the Foundations of            Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou,
  Software Engineering, pages 1229–1241.                      Timothee Lacroix, Jiacheng Liu, Wenda Li, Mateja
                                                              Jamnik, Guillaume Lample, and Yuhuai Wu. 2023.
Ronghui Gu, Jérémie Koenig, Tahina Ramananan-                 Draft, sketch, and prove: Guiding formal theorem
  dro, Zhong Shao, Xiongnan Wu, Shu-Chun Weng,                provers with informal proofs. In The Eleventh Inter-
  Haozhong Zhang, and Yu Guo. 2015. Deep specifica-           national Conference on Learning Representations.
  tions and certified abstraction layers. ACM SIGPLAN
  Notices, 50(1):595–608.                                   Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim,
                                                              and Sunghun Kim. 2024. A survey on large
Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan New-               language models for code generation. Preprint,
  man Wu, Jieung Kim, Vilhelm Sjöberg, and David              arXiv:2406.00515.
  Costanzo. 2016. {CertiKOS}: An extensible archi-
  tecture for building certified concurrent {OS} kernels.   Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June
  In 12th USENIX Symposium on Operating Systems               Andronick, David Cock, Philip Derrin, Dhammika
  Design and Implementation (OSDI 16), pages 653–             Elkaduwe, Kai Engelhardt, Rafal Kolanski, Michael
  669.                                                        Norrish, and 1 others. 2009. sel4: Formal verification
                                                              of an os kernel. In Proceedings of the ACM SIGOPS
Ronghui Gu, Zhong Shao, Jieung Kim, Xiongnan Wu,              22nd symposium on Operating systems principles,
  Jérémie Koenig, Vilhelm Sjöberg, Hao Chen, David            pages 207–220.
Peter Koepke, Anton Lorenzen, and Boris Shminke.           Azim Ospanov, Farzan Farnia, and Roozbeh Mohit.
  2022. Cicm’22 system entries. In Intelligent Com-          2025. Apollo: Automated llm and lean collabora-
  puter Mathematics, pages 344–348, Cham. Springer           tion for advanced formal reasoning. In Advances in
  International Publishing.                                  Neural Information Processing Systems, volume 38,
                                                             pages 41599–41633. Curran Associates, Inc.
Guillaume Lample, Timothee Lacroix, Marie-Anne
  Lachaux, Aurelien Rodriguez, Amaury Hayat,               Lawrence Paulson. 2012. Three years of experience
  Thibaut Lavril, Gabriel Ebner, and Xavier Martinet.        with sledgehammer, a practical link between auto-
  2022. Hypertree proof search for neural theorem            matic and interactive theorem provers. In PAAR-
  proving. Advances in neural information processing         2010: Proceedings of the 2nd Workshop on Practical
  systems, 35:26337–26349.                                   Aspects of Automated Reasoning, volume 9 of EPiC
                                                             Series in Computing, pages 1–10. EasyChair.
Xavier Leroy, Sandrine Blazy, Daniel Kästner, Bernhard
  Schommer, Markus Pister, and Christian Ferdinand.        Benjamin C Pierce, Chris Casinghino, Marco Gaboardi,
  2016. Compcert-a formally verified optimizing com-         Michael Greenberg, Cătălin Hriţcu, Vilhelm Sjöberg,
  piler. In ERTS 2016: Embedded Real Time Software           and Brent Yorgey. 2010. Software foundations. Web-
  and Systems, 8th European Congress.                        page: http://www. cis. upenn. edu/bcpierce/sf/curren-
                                                             t/index. html, 16.
Zhenwen Liang, Linfeng Song, Yang Li, TAO YANG,            Stanislas Polu and Ilya Sutskever. 2020. Generative
  Haitao Mi, and Dong Yu. 2025. Mps-prover: Advanc-           language modeling for automated theorem proving.
  ing stepwise theorem proving by multi-perspective           arXiv preprint arXiv:2009.03393.
  search and data curation. In Advances in Neural
  Information Processing Systems, volume 38, pages         Tom Reichel, R. Wesley Henderson, Andrew Touchet,
  137891–137916. Curran Associates, Inc.                     Andrew Gardner, and Talia Ringer. 2023. Proof Re-
                                                             pair Infrastructure for Supervised Models: Build-
Xiaohan Lin, Qingxing Cao, Yinya Huang, Haiming              ing a Large Proof Repair Dataset. In 14th Interna-
  Wang, Jianqiao Lu, Zhengying Liu, Linqi Song, and          tional Conference on Interactive Theorem Proving
  Xiaodan Liang. 2024. Fvel: Interactive formal verifi-      (ITP 2023), volume 268 of Leibniz International Pro-
  cation environment with large language models via          ceedings in Informatics (LIPIcs), pages 26:1–26:20,
  theorem proving. Advances in Neural Information            Dagstuhl, Germany. Schloss Dagstuhl – Leibniz-
  Processing Systems, 37:54932–54946.                        Zentrum für Informatik.

Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu,               Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin,
  Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou                  Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu,
  Xia, Danqi Chen, Sanjeev Arora, and Chi Jin.                Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shi-
  2025. Goedel-prover: A frontier model for open-             rong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun Gao,
  source automated theorem proving.     Preprint,             Daya Guo, and Chong Ruan. 2025. Deepseek-prover-
  arXiv:2502.07640.                                           v2: Advancing formal mathematical reasoning via
                                                              reinforcement learning for subgoal decomposition.
Haoxiong Liu, Jiacheng Sun, Zhenguo Li, and An-               Preprint, arXiv:2504.21801.
  drew C Yao. 2025. Proofaug: efficient neural theo-
  rem proving via fine-grained proof structure analysis.   Alexandre Riazanov and Andrei Voronkov. 2002. The
  In Proceedings of the 42nd International Conference        design and implementation of vampire. AI Commun.,
  on Machine Learning, ICML’25. JMLR.org.                    15(2,3):91–110.

                                                           Zhihong Shao, Yuxiang Luo, Chengda Lu, Z. Z. Ren,
Maciej Mikuła, Szymon Tworkowski, Szymon Anto-               Jiewen Hu, Tian Ye, Zhibin Gou, Shirong Ma, and
 niak, Bartosz Piotrowski, Albert Q Jiang, Jin Peng          Xiaokang Zhang. 2025. Deepseekmath-v2: Towards
 Zhou, Christian Szegedy, Łukasz Kuciński, Piotr            self-verifiable mathematical reasoning. Preprint,
 Miłoś, and Yuhuai Wu. 2023. Magnushammer: A                arXiv:2511.22570.
 transformer-based approach to premise selection. In
 The Twelfth International Conference on Learning          Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,
 Representations.                                            Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan
                                                             Zhang, Y. K. Li, Y. Wu, and Daya Guo. 2024.
Leonardo de Moura and Sebastian Ullrich. 2021. The           Deepseekmath: Pushing the limits of mathemati-
  lean 4 theorem prover and programming language. In         cal reasoning in open language models. Preprint,
  Automated Deduction–CADE 28: 28th International            arXiv:2402.03300.
  Conference on Automated Deduction, Virtual Event,
  July 12–15, 2021, Proceedings 28, pages 625–635.         Shweta Shinde, Shengyi Wang, Pinghai Yuan, Aquinas
  Springer.                                                  Hobor, Abhik Roychoudhury, and Prateek Saxena.
                                                             2020. {BesFS}: A {POSIX} filesystem for enclaves
Tobias Nipkow, Markus Wenzel, and Lawrence C Paul-           with a mechanized safety proof. In 29th USENIX
  son. 2002. Isabelle/HOL: a proof assistant for             Security Symposium (USENIX Security 20), pages
  higher-order logic. Springer.                              523–540.
Xujie Si, Hanjun Dai, Mukund Raghothaman, Mayur          Haiming Wang, Ye Yuan, Zhengying Liu, Jianhao Shen,
  Naik, and Le Song. 2018. Learning loop invariants        Yichun Yin, Jing Xiong, Enze Xie, Han Shi, Yujun
  for program verification. Advances in Neural Infor-      Li, Lin Li, and 1 others. 2023. Dt-solver: Automated
  mation Processing Systems, 31.                           theorem proving with dynamic-tree sampling guided
                                                           by proof-level value function. In Proceedings of the
Xujie Si, Aaditya Naik, Hanjun Dai, Mayur Naik, and        61st Annual Meeting of the Association for Compu-
  Le Song. 2020. Code2inv: A deep learning frame-          tational Linguistics (Volume 1: Long Papers), pages
  work for program verification. In Computer Aided         12632–12646.
  Verification: 32nd International Conference, CAV
  2020, Los Angeles, CA, USA, July 21–24, 2020, Pro-     Qingxiang Wang, Cezary Kaliszyk, and Josef Urban.
  ceedings, Part II 32, pages 151–164. Springer.           2018. First experiments with neural translation of
                                                           informal to formal mathematics. In Intelligent Com-
Helgi Sigurbjarnarson, James Bornholt, Emina Torlak,       puter Mathematics: 11th International Conference,
  and Xi Wang. 2016. {Push-Button} verification of         CICM 2018, Hagenberg, Austria, August 13-17, 2018,
  file systems via crash refinement. In 12th USENIX        Proceedings 11, pages 255–270. Springer.
  Symposium on Operating Systems Design and Imple-
  mentation (OSDI 16), pages 1–16.                       Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe
                                                           Diao, Renjie Pi, and Tong Zhang. 2024c. Theoreml-
Matthieu Sozeau, Yannick Forster, Meven Lennon-            lama: Transforming general-purpose llms into lean4
 Bertrand, Jakob Nielsen, Nicolas Tabareau, and Théo       experts. arXiv preprint arXiv:2407.03203.
 Winterhalter. 2025. Correct and complete type check-
                                                         Christoph Weidenbach, Bernd Gaede, and Georg Rock.
 ing and certified erasure for coq, in coq. Journal of
                                                           1996. Spass & flotter version 0.42. In Automated
 the ACM, 72(1):1–74.
                                                           Deduction—Cade-13: 13th International Conference
Freek Verbeek, Oto Havle, Julien Schmaltz, Sergey          on Automated Deduction New Brunswick, NJ, USA,
  Tverdyshev, Holger Blasum, Bruno Langenstein,            July 30–August 3, 1996 Proceedings 13, pages 141–
  Werner Stephan, Burkhart Wolff, and Yakoub               145. Springer.
  Nemouchi. 2015. Formal api specification of the        Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao
  pikeos separation kernel. In NASA Formal Methods:        Qin, Mengda He, Haokun Li, Shing-Chi Cheung,
  7th International Symposium, NFM 2015, Pasadena,         and Cong Tian. 2024. Enchanting program specifica-
  CA, USA, April 27-29, 2015, Proceedings 7, pages         tion synthesis by large language models using static
  375–389. Springer.                                       analysis and program verification. In International
                                                           Conference on Computer Aided Verification, pages
Leandro von Werra, Younes Belkada, Lewis Tunstall,         302–328. Springer.
  Edward Beeching, Tristan Thrush, Nathan Lambert,
  Shengyi Huang, Kashif Rasul, and Quentin Gal-          Makarius Wenzel. 2021. The isabelle system manual.
  louédec. 2020. TRL: Transformers Reinforcement
  Learning.                                              Makarius Wenzel. 2025. Isabelle/HOL: A Proof Assis-
                                                          tant for Higher-Order Logic (Tutorial). Technische
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas             Universität München.
  Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
  Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jian-          Makarius Wenzel and Isabelle Development Team. 2025.
  qiao Lu, Hugues de Saxcé, Bolton Bailey, Chen-          The Isabelle/Isar Reference Manual. Technische Uni-
  dong Song, Chenjun Xiao, Dehao Zhang, Ebony             versität München.
  Zhang, Frederick Pu, Han Zhu, and 21 others. 2025.     Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus
  Kimina-prover preview: Towards large formal rea-         Rabe, Charles Staats, Mateja Jamnik, and Christian
  soning models with reinforcement learning. Preprint,     Szegedy. 2022. Autoformalization with large lan-
  arXiv:2504.11354.                                        guage models. Advances in Neural Information Pro-
                                                           cessing Systems, 35:32353–32368.
Haiming Wang, Huajian Xin, Zhengying Liu, Wenda Li,
  Yinya Huang, Jianqiao Lu, Zhicheng Yang, Jing Tang,    Huajian Xin, ZZ Ren, Junxiao Song, Zhihong Shao,
  Jian Yin, Zhenguo Li, and Xiaodan Liang. 2024a.          Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
  Proving theorems recursively. In Proceedings of the      Xuan Lu, Qiushi Du, and 1 others. 2024. Deepseek-
  38th International Conference on Neural Information      prover-v1. 5: Harnessing proof assistant feedback for
  Processing Systems, NIPS ’24, Red Hook, NY, USA.         reinforcement learning and monte-carlo tree search.
  Curran Associates Inc.                                   CoRR.
Haiming Wang, Huajian Xin, Chuanyang Zheng,              Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang
  Zhengying Liu, Qingxing Cao, Yinya Huang, Jing           Wu, Xia Xiao, Yifan Sun, Shen Zheng, and Ming
  Xiong, Han Shi, Enze Xie, Jian Yin, and 1 others.        Ding. 2025. BFS-prover: Scalable best-first tree
  2024b. Lego-prover: Neural theorem proving with          search for LLM-based automatic theorem proving.
  growing libraries. In 12th International Conference      In Proceedings of the 63rd Annual Meeting of the
  on Learning Representations (ICLR 2024). Inter-          Association for Computational Linguistics (Volume 1:
  national Conference on Learning Representations,         Long Papers), pages 32588–32599, Vienna, Austria.
  ICLR.                                                    Association for Computational Linguistics.
Qiyuan Xu, Renxi Wang, Peixin Wang, Haonan Li, and      users can call Sledgehammer directly to finish the
  Conrad Watt. 2026. A minimalist proof language for    proof. Sledgehammer is good at generating short
  neural theorem proving over isabelle/hol. Proc. ACM
                                                        proofs (Paulson, 2012). Thus, if users also pro-
  Program. Lang., 10(OOPSLA1).
                                                        vide a proof sketch with some subgoals introduc-
Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chala-          ing how the proof might be done, Sledgehammer
  mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J    will find proofs for each subgoal and construct the
  Prenger, and Animashree Anandkumar. 2023. Le-
  andojo: Theorem proving with retrieval-augmented      whole proof more easily. It is worth mentioning
  language models. Advances in Neural Information       that Sledgehammer does not do induction very well.
  Processing Systems, 36:21573–21612.                   LLMs might help with theorems that require induc-
Xueliang Zhao, Lin Zheng, Haige Bo, Changran Hu, Ur-    tion proofs.
  mish Thakker, and Lingpeng Kong. 2024. Subgoalxl:
  Subgoal-based expert learning for theorem proving.    A.2             Explanation of Isabelle Code
  arXiv preprint arXiv:2408.11172.                      Listing 1 shows two Isabelle proofs of the same
Yongwang Zhao, David Sanán, Fuyuan Zhang, and           theorem, which states that reversing a list twice
  Yang Liu. 2017. Refinement-based specification        does not change the list. In the apply-style proof
  and security analysis of separation kernels. IEEE     (right), we first apply induction on the list xs, then
  Transactions on Dependable and Secure Computing,      we use a tactic auto in Isabelle to finish the proof.
  16(1):127–141.
                                                        The keyword done marks the end of the proof. This
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.    proof style is concise, but to understand what these
  2022. minif2f: a cross-system benchmark for formal    tactics are doing, we need to check the proof state
  olympiad-level mathematics. In ICLR.
                                                        of each step in Isabelle. In the Isar proof (left), we
A     Technical Appendices and                          first apply induction on list xs that clearly splits the
      Supplementary Material                            goals into two cases, i.e., case Nil and case Cons a
                                                        xs. Here Nil means the empty list, and Cons means
A.1    Hammers                                          appending an element a to the front of the original
We integrate hammers in our framework to                list xs.
augment theorem proving. Blanchette et al.                 Note that these two styles of proofs can be com-
(Blanchette et al., 2016) define hammers as meth-       bined, with Isar sketching the final proof while
ods that “automate reasoning over large libraries       apply-style tactics discharge the remaining sub-
developed with formal proof assistants.” Most ITPs      goals to fill in the sketch. For example, for the
have their own hammers, e.g., Coqhammer in Rocq         proof in Listing 1, a user could write a proof sketch
and Sledgehammer in Isabelle. Sledgehammer in           in Isar by writing sorry instead of by simp—telling
Isabelle is the most powerful one (Paulson, 2012).      Isabelle to assume the subgoal is correct. Then,
Providing the input theorem, Sledgehammer first         after using Isabelle to check that the proof sketch
finds relevant premises using machine learning and      is sufficient, users can fill in the details to finish the
a traditional filtering algorithm (Paulson, 2012).      proof.
Then it translates the input theorem together with a
heuristic selection of hundreds of premises into        A.3             A Running Example of HybridProver
goals that external ATPs can recognize. Then,
                                                                                       Step 1                               Step 2
                                                                                                    Whole-proof
ATPs solve these problems and return the results to      User input: theorem
                                                          theorem list_reverse:
                                                                                                  synthesis model
                                                                                                                                     Proof filter

                                                            "rev (rev xs) = xs"
Sledgehammer. Sledgehammer thus gets the use-                                                    Initial candidate proof
                                                                                                proof (induction xs)
                                                                                                case Nil
ful premises and finally reconstructs proofs for the       Prompt template
                                                         Generate Isabelle proof
                                                                                                then show ?case
                                                                                                      by presburger
                                                                                                                                      Checker:
                                                                                                                                      Isabelle
                                                                                                                                                      Yes
                                                                                                                                                            Prover output: Proof
                                                         based on the input theorem.            next case (Cons a xs)
Isabelle trusted kernel to check. Every ITP has a        Make sure .....
                                                                                                then show ?case
                                                                                                      by simp
                                                                                                                               Step 3       no
                                                                                                qed
trusted kernel, a minimal and rigorously verified
                                                            Tactic-based                                                         Sketch builder
core that checks manually constructed proofs fol-         generation model                            no
                                                                                                                                   Proof sketch
                                                                LLM for                                                                                        Final whole proof
                                                                                                                              proof (induction xs)
lowing mathematical logic rules (Nipkow et al.,                proofsteps               Step 4
                                                                                                     Checker:                 case Nil
                                                                                                                              then show ?case
                                                                                                                                                            proof (induction xs)
                                                                                                                                                            case Nil
                                                            Sledgehammer                   yes        Isabelle
                                                                                                                                   sorry                    then show ?case
2002; Pierce et al., 2010). Since the kernel checks         with heuristics                                                   next case (Cons a xs)              by simp
                                                                                                                                                            next case (Cons a xs)
                                                                                                                              then show ?case
                                                                                                                                                            then show ?case
these proofs, it is unnecessary for the user to worry                                                                  no
                                                                                                                              qed
                                                                                                                                   by simp

                                                                                                                                                            qed
                                                                                                                                                                 by simp
                                                                              Step 5
about the correctness of the generated proof.                                 Sketch refiner
                                                                                                                 Checker:
                                                                                                                                                            Prover output: Proof
                                                                                                                  Isabelle      yes
   Sledgehammer makes writing proofs convenient.
Isabelle users only need to write the assumptions
and the final goal that they want to prove. Then                 Figure 3: A running example of HybridProver
   As a running example in Figure 3, we use the          proof construction by human experts, a process
Isabelle theorem list_reverse, which states that re-     that is labor-intensive and time-consuming. For
versing a list twice yields the original list: rev       example, the seL4 team (Klein et al., 2009) takes
(rev xs) = xs. The initial candidate proof gener-        30 person-years to verify a general-purpose micro-
ated by the whole-proof synthesis model follows an       kernel with 8700 lines of C code in Isabelle. The
Isar-style induction structure. It starts with proof     CertiKOS team (Gu et al., 2016) verifies a concur-
(induction xs), which splits the theorem into the        rent OS through deep abstraction layers in Rocq
base case Nil and the inductive case Cons a xs.          (Gu et al., 2015, 2018). They take 3 person-years to
In the candidate proof, the base case is discharged      prove 6500 lines of C and x86 assembly. CompCert
by by presburger, while the inductive case is            (Leroy et al., 2016) is the first formally verified C
discharged by by simp.                                   compiler to be exempt from miscompilation. Six
   However, this candidate proof does not pass the       person-years are taken in Rocq to construct proofs.
Isabelle checker, because by presburger is not a         Additionally, most theorem-proving works in other
suitable tactic for proving the Nil case of this list    operating systems take more than 1 person-year
theorem. Although the overall proof structure is         (Sigurbjarnarson et al., 2016; Shinde et al., 2020;
reasonable—it correctly uses induction and intro-        Chajed et al., 2019; Zhao et al., 2017; Amani et al.,
duces the two standard list cases—one of its local       2016; Hu et al., 2024; Verbeek et al., 2015; Hu et al.,
proof steps is incorrect. This example illustrates       2025). Automated theorem provers (ATPs) such as
why directly discarding the whole candidate proof        Z3 and CVC4 offer full automation (Barrett et al.,
would waste useful structure.                            2011; De Moura and Bjørner, 2008; Riazanov and
   HybridProver therefore constructs a proof sketch      Voronkov, 2002; Weidenbach et al., 1996), but are
from this failed candidate. In the sketch shown          typically limited to first-order logic and suffer from
in Figure 3, the concrete tactics by presburger          search-space explosion. This motivates the use of
are replaced with sorry, while the correct subgoal       LLMs to improve the usability of ITPs without
proof and surrounding Isar structure is preserved:       sacrificing their expressiveness and scalability.
proof (induction xs), case Nil, next case
                                                         Autoformalization. In this work, we focus on
(Cons a xs), and qed remain unchanged. The
                                                         theorem proving where a formal specification al-
resulting sketch keeps the high-level induction ar-
                                                         ready exists. Another interesting area is autofor-
gument but leaves the local proof obligations unre-
                                                         malization, where researchers translate natural lan-
solved.
                                                         guage texts into formal specifications and proofs
   During refinement, the tactic-based generation
                                                         (Azerbayev et al., 2023; Wang et al., 2018; Cosler
model and Sledgehammer search for concrete tac-
                                                         et al., 2023; Hahn et al., 2022; Wu et al., 2022;
tics to replace the sorry placeholders. For this
                                                         Chen et al., 2023). The amount of natural lan-
example, the first subgoal can be solved by by
                                                         guage texts and mathematical proofs is far greater
simp. After substitution, the final proof replaces
                                                         than formal texts. Therefore, autoformalization cre-
each sorry with by simp, producing a complete
                                                         ates a lot of high-quality data used for model train-
Isabelle proof that passes verification: the base case
                                                         ing, which solves the data scarcity problem. Other
Nil is proved by simplification, and the inductive
                                                         works also try to generate specifications based on
case Cons a xs is also discharged by simplifica-
                                                         code (Wen et al., 2024; Cosler et al., 2023; Si et al.,
tion.
                                                         2018, 2020).
   This example shows that the initial whole-proof
candidate already contains a useful high-level struc-    Premise Selection. Premises refer to the auxil-
ture, even though one local tactic is wrong. By          iary lemmas, as well as datatype and function def-
preserving the Isar structure and refining only the      initions, that are referenced to establish the target
unresolved proof steps, HybridProver converts the        theorem. Existing studies on premise selection
failed candidate into a verified proof.                  mainly follow two technical routes. One line of
                                                         work builds an external premise retrieval library
A.4   Additional Related Work                            and retrieves relevant premises according to seman-
Interactive theorem proving. Theorem proving             tic similarity or symbolic matching with the input
is widely used for ensuring the safety and security      theorem (Wang et al., 2024b; Yang et al., 2023).
of critical software and systems. Most work in in-       The other incorporates premise usage into model
teractive theorem proving involves some manual           training, enabling the model to memorize common
premises and their contexts and to invoke them au-        with a 32 sampling rate for one LLM. Thus, we
tomatically when proving similar theorems (First          do ablation studies with a relatively low sampling
et al., 2023). We adopt the latter approach by inte-      rate and small timeout. To set up Sledgehammer,
grating premise selection into the training objective     we follow the default Isabelle2021 configuration
of the whole-proof synthesis model. As a result,          (Jiang et al., 2021), where the Sledgehammer time-
the model is encouraged to identify and insert nec-       out limit is 30s, with the on-machine five default
essary premises during proof generation, thereby          ATPs (E, SPASS, Vampire, Z3, and CVC4). We
providing richer contextual support for the subse-        also complement Sledgehammer with 11 heuristics
quent strategy generation stage and improving the         for proofs: [’by auto’, ’by simp’, ’by blast’, ’by
accuracy of subgoal solving.                              fastforce’, ’by force’, ’by eval’, ’by presburger’,
                                                         ’by sos’, ’by arith’, ’by linarith’, ’by (auto simp:
A.5   Additional Setup                                    field_simps)’].
Dataset. PISA includes the STD and AFP with
version 2021-10-22. The former is more founda-
tional, with around 70K theorems. The latter is          Training Configurations. For fine-tuning, we
a proof library contributed by most Isabelle re-         use LoRA (Hu et al., 2021) to train around 1% of
searchers, with around 170K theorems. It diverges        all parameters with a lora_rank 32 and all target
from mathematical problems to formal verification        layers open for adjustment. In the first 10% of
of software and hardware.                                steps, the learning rate warms up linearly from 0
                                                         to the maximum value e−5 . Then it decays to 0
   MiniF2F (Zheng et al., 2022) is used in many re-
                                                         following a cosine schedule. The context length
search studies (Yang et al., 2023; Jiang et al., 2023;
                                                         for the training data is 2048 tokens, and the total
Zhao et al., 2024). It is an open-source collection
                                                         batch size is 64.
containing 488 high school math competition prob-
lems. These problems are divided into two groups:           We implement reinforcement learning using the
244 for validation and 244 for final testing. All        GRPO trainer from the TRL framework (von Werra
problems have been translated into 4 proof assis-        et al., 2020). For each input theorem, we sample
tant languages: Lean, HOL light, Metamath, and           16 candidate proofs in parallel. The reward func-
Isabelle.                                                tion combines two components: (1) a verification
                                                         reward obtained from Isabelle, and (2) a penalty for
Isabelle Interactive environment. We interact            undesirable patterns. Concretely, proofs that pass
with Isabelle using Isabelle-client (Koepke et al.,      Isabelle checking receive a reward of 1.0, proofs
2022), which provides detailed developer documen-        that are syntactically valid but fail verification re-
tation and Isabelle interface descriptions, making       ceive 0.2, and invalid outputs receive 0.0. Addition-
it easy to use and maintain. It is a Python client       ally, outputs containing tokens such as sorry or
library that strictly follows the Isabelle system man-   malformed proof patterns are assigned a negative
ual (Wenzel, 2021). To improve system throughput         penalty (-0.2), discouraging trivial or incomplete
and efficiency, we employ a concurrent architec-         proofs. We train the model for 3 epochs with a
ture based on a single server, a single client, and      learning rate of 2 × 10−5 , using a per-device batch
multiple sessions. Our experiments show that using       size of 2.
multiple Isabelle server processes leads to resource
contention. By contrast, multiple independent ses-
sions can load different Isabelle theory libraries       A.6   Prompt template and few-shot examples
separately, thereby supporting the verification of
different theorems in the evaluation dataset. In ad-       Listing 2: Prompt template
dition, we found that a multi-client single-session
                                                           Generate proof code in Isabelle/HOL
setting is error-prone and incurs high resource con-
                                                           based on the input Isabelle/HOL
sumption, and therefore it is not adopted in our
                                                           theorem. Make sure that the
system.
                                                           generated proof can be verified by
   watchdog_timeout is set to 30s for evaluation.
                                                           Isabelle/HOL. Do not generate extra
Evaluation in Isabelle is time-consuming even for a
                                                           natural language descriptions.
small sampling rate and a small dataset. It costs 300
                                                           **Input theorem:**
CPU hours to evaluate 244 theorems in miniF2F
 Listing 3: Few-shot examples
 Input theorem 1:
 theorem app_Nil: "[] @ xs = (xs :: '
 a list)"
 Isabelle proof 1:
 {Isabelle proof: by simp}

 Input theorem 2:
 theorem list_reverse: "rev (rev xs)
 = xs"
 Isabelle proof 2:
 {Isabelle proof: apply (induct xs)
 apply simp apply simp done}

 Input theorem 3:
 theorem append_assoc: "(xs @ ys) @
 zs = xs @ (ys @ zs)"
 Isabelle proof 3:
 {Isabelle proof: proof (induct xs)
 case Nil then show ?case by simp
 next case (Cons x xs) then show ?
 case by simp qed}

A.7   Additional ablation results
RQ4: Is the proof pattern similarity equal to
the proof quality? During the fine-tuning stage,
we try to feed the model enough theorem-proof
pairs. The LLM learns to generate proof patterns
similar to the training data. But is the proof pattern
similarity equal to the quality? Thus, we not only
test the success rate of the miniF2F dataset, but also
record all responses from the sampling during the
whole evaluation. We make a comparison between
them and find that generally, the higher the total
correct response is, the higher the success rate for
all theorems is. It demonstrates that proof pattern
similarity is strongly relevant to the proof quality,
reflecting the improvement from training.

  RA4: The more similar an LLM-generated
  proof pattern is to the training data, the higher
  the quality of the proof.
