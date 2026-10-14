                                            Automated Formal Proofs of Combinatorial Identities via Wilf–Zeilberger
                                                                    Guidance and LLMs


                                           Beibei Xiong 1 Hangyu Lv 1 Junqi Liu 2 Yisen Wang 2 Shaoshi Chen 2 Jianlin Wang 3 Zhengfeng Yang 1
                                                                                      Lihong Zhi 2


                                                                 Abstract                                  et al., 2025; Wang et al., 2025a; Chen et al., 2025), enabling
                                                                                                           formal reasoning toward research-level mathematics (Wei
arXiv:2605.04472v1 [cs.LG] 6 May 2026




                                             Automating formal proofs of combinatorial iden-               et al., 2024; Yu et al., 2025b). However, scaling LLM-based
                                             tities is challenging for LLM-based provers, as               provers to harder mathematical domains remains challeng-
                                             long-horizon proof planning is required and                   ing, largely due to the lack of principled proof planning
                                             unconstrained search quickly explodes. Sym-                   and the resulting combinatorial explosion in proof search.
                                             bolic methods such as the Wilf–Zeilberger (WZ)                Combinatorics is widely considered one of the most difficult
                                             method can achieve a mechanized proof of com-                 areas for ATP (Chen et al., 2025; Google DeepMind, 2025),
                                             binatorial identities by constructing special aux-            and combinatorial identities form a fundamental and ubiqui-
                                             iliary functions and demonstrating that they sat-             tous class of statements within it. Consequently, automating
                                             isfy specific recurrence relations. We propose                machine-checkable proofs of combinatorial identities is a
                                             WZ-LLM, a neuro-symbolic framework that turns                 key objective for scalable theorem proving, enabling the
                                             WZ proof plans into executable proof sketches                 construction of reusable verified libraries and reducing the
                                             in Lean 4 and uses an LLM-based prover to                     human effort required for formal proof development.
                                             discharge the resulting machine-checkable sub-
                                             goals. We also train a dedicated WZ-Prover                    We focus on automating formal proofs of combinatorial
                                             via a Lean-kernel-verified bootstrapping loop                 identities in Lean 4 (Moura & Ullrich, 2021), a task that
                                             with expert-verified iteration, followed by DAPO-             remains a challenge for current LLM-based provers. Such
                                             based refinement. Experiments show that WZ-                   proofs typically require long-horizon proof planning: with-
                                             LLM achieves a 34% proof success rate on LCI-                 out an executable global route that specifies key intermedi-
                                             Test (100 classic combinatorial identities), outper-          ate milestones, an LLM-based prover is forced into largely
                                             forming strong baselines such as DeepSeek-V3                  unconstrained exploration, leading to a combinatorial ex-
                                             and Goedel-Prover-V2, and delivering consistent               plosion in proof search. Moreover, data scarcity limits the
                                             gains on CombiBench and PutnamBench-Comb.                     available proof data for this domain. These challenges mo-
                                             These results indicate that our framework pro-                tivate an approach for automatically generating executable
                                             vides two complementary strengths: improved                   proof sketches that decompose a target identity into a se-
                                             direct proving for identities beyond the scope of             quence of machine-checkable subgoals, thereby constrain-
                                             WZ, and substantially higher end-to-end success               ing the search space and enabling long-horizon reasoning.
                                             when WZ sketches guide a specialized prover.                  The WZ method is a classical and powerful approach to
                                                                                                           prove combinatorial identities (Zeilberger, 1991; Wilf &
                                                                                                           Zeilberger, 1990; Gosper, 1978; Liu et al., 2024). It pro-
                                        1. Introduction                                                    vides a natural source of global proof structure: a WZ proof
                                                                                                           is organized around the synthesis of a recurrence together
                                        Large language models (LLMs) have recently achieved                with appropriate boundary and initial conditions, thereby
                                        strong performance on formal automated theorem proving             providing a principled proof plan for long-horizon reason-
                                        (ATP) benchmarks (Xin et al., 2025; Lin et al., 2025; Guo          ing (Zeilberger, 1991). However, turning the WZ method
                                            1
                                              School of Software Engineering, East China Normal Uni-       into a fully automated formal proof pipeline remains chal-
                                        versity, Shanghai, China 2 Institute of Mathematics and Sys-       lenging in practice, due to limited symbolic coverage and
                                        tems Science, Chinese Academy of Sciences, Beijing, China          the nontrivial formalization of boundary conditions and obli-
                                        3
                                          School of Computer and Information Engineering, Henan Uni-       gations in proof assistants. This motivates a sketch-guided
                                        versity, Kaifeng, China. Correspondence to: Zhengfeng Yang
                                        <zfyang@sei.ecnu.edu.cn>.                                          neuro-symbolic design: we use the WZ method to plan
                                                                                                           and decompose a target identity into verifiable intermediate
                                        Preprint. May 7, 2026.                                             goals and leverage LLMs to discharge the resulting formal

                                                                                                       1
                                    Submission and Formatting Instructions for ICML 2026

obligations. Meanwhile, LLM-based proving also extends                assistants such as Lean (Moura & Ullrich, 2021) and Is-
coverage by producing direct Lean proofs when the WZ                  abelle (Paulson, 1994). One line focuses on step-wise
decomposition is unavailable or fails.                                tactic generation with explicit search (e.g., BFS/MCTS)
                                                                      and frequent verifier interaction, achieving strong perfor-
We propose WZ-LLM, a framework that translates the WZ
                                                                      mance but often incurring substantial branching and com-
proof plan into executable proof sketches in Lean—namely,
                                                                      pute costs (Polu & Sutskever, 2020; Yang et al., 2024; Xin
recurrence lemmas and their associated obligations—and
                                                                      et al., 2025; Wu et al., 2024). Another line emphasizes
leverages a large language model to automatically discharge
                                                                      whole-proof generation to preserve long-range coherence,
the resulting subgoals. To make this approach effective in
                                                                      but may underutilize intermediate verifier signals for frame-
practice and mitigate data scarcity for Lean combinatorics,
                                                                      workatic correction (Wang et al., 2024; Lin et al., 2025).
we develop a Lean-verified training pipeline for WZ-LLM.
                                                                      To mitigate data scarcity and improve long-horizon reason-
We start by manually formalizing 307 combinatorial identi-
                                                                      ing, recent methods leverage verifier-filtered bootstrapping
ties from classical textbooks, yielding a high-quality seed
                                                                      and reinforcement learning in verifiable environments (Shao
corpus for cold-start supervised fine-tuning (SFT). Building
                                                                      et al., 2024; Ospanov et al., 2025; Xin et al., 2024). In
on this seed, we expand the data via expert-verified iteration,
                                                                      particular, MA-LoT (Wang et al., 2025b) GAR (Wang
retaining only Lean-kernel-verified model outputs: verified
                                                                      et al., 2025c) and Spark-Prover-X1 (Zhou et al., 2025) fur-
proofs (including WZ-sketch lemmas and direct proofs of
                                                                      ther improve proving via correction/refinement and scal-
WZ-uncovered identities) are added to the training corpus
                                                                      able verifier-guided training. Our work targets a domain
and pruned from the proving-task pool, while unverified
                                                                      where successful proving critically depends on explicit proof
attempts are retained for subsequent iterations. We then
                                                                      planning and studies how symbolic decompositions can be
train a specialized prover, WZ-Prover, through cold-start
                                                                      compiled into executable proof sketches to constrain proof
SFT, iterative training on expanded data (Wu et al., 2024),
                                                                      search.
and Dynamic Sampling Policy Optimization (DAPO) refine-
ment (Yu et al., 2025a). Experiments show that WZ-LLM                 Formal Proof of Combinatorial Identities. Symbolic com-
achieves a 34% end-to-end success rate on a benchmark of              putation has long played a central role in proving combi-
100 classical combinatorial identities in Lean 4, substantially       natorial identities by transforming summations into alge-
outperforming strong baselines. Furthermore, on LCI-Test,             braic forms that are amenable to frameworkatic verification.
WZ-LLM proves 5 identities on which the symbolic-only                 Classical generating-function techniques reduce identities
baseline fails, highlighting complementary coverage be-               to functional equations and coefficient extraction, and re-
yond purely symbolic methods. WZ-LLM also improves                    main a standard paradigm in combinatorics (Stanley, 1986;
performance on CombiBench and PutnamBench, solving all                Flajolet & Sedgewick, 2009; Wilf, 2005). Beyond generat-
manually identified identity instances in these benchmarks.           ing functions, elimination-style approaches (e.g., Gröbner-
Our main contributions are as follows.                                basis methods) establish polynomial or rational identities
                                                                      via ideal membership and symbolic elimination (Cox et al.,
   • We propose WZ-LLM, a neuro-symbolic framework                    1997; Sturmfels, 2002). For hypergeometric and holonomic
     that converts Wilf–Zeilberger reasoning into exe-                summations, certificate-based methods such as the Wilf–
     cutable proof sketches in Lean and uses an LLM-based             Zeilberger algorithm and creative telescoping derive recur-
     prover to discharge the resulting proof obligations.             rences together with rational certificates/invariants whose
                                                                      validity can be mechanically checked (Wilf & Zeilberger,
   • We build a Lean-verified dataset for combinatorial               1992; Petkovsek et al., 1996; Kauers & Paule, 2011). How-
     identities and train a domain-specialized prover via a           ever, while these techniques are highly effective in computer
     multi-stage pipeline (cold-start SFT, verified bootstrap-        algebra frameworks, their outputs do not directly translate
     ping, and DAPO refinement), improving long-horizon               into interactive proof assistants: end-to-end formalization
     lemma chaining under distribution shift.                         typically requires explicitly reconstructing telescoping ar-
                                                                      guments, boundary conditions, normalization steps, and
   • We evaluate WZ-LLM on a new benchmark LCI-Test                   non-vanishing side conditions inside the logic, which often
     (100 classical identities) as well as public combina-            dominates the verification cost. Harrison (Harrison, 2015)
     torics benchmarks, outperforming strong LLM base-                calculated rational function certificates using the Maxima
     lines and complementing a symbolic-only baseline by              external computer algebra framework, and subsequently
     solving additional cases.                                        used HOL Light (Harrison, 1996) to rigorously verify that
                                                                      these certificates satisfy the WZ equation (2). Recent efforts
2. Related Work                                                       have begun to framework this domain in Lean by construct-
                                                                      ing dedicated datasets and benchmarks for combinatorial
Automated Theorem Proving. LLM-based automated the-                   identities (Xiong et al., 2025). In this work, we leverages the
orem proving has advanced rapidly in interactive proof

                                                                  2
                                      Submission and Formatting Instructions for ICML 2026

WZ method as a decomposition tool that compiles identities
                                                                         Consider the classical binomial-sum identity
into explicit proof obligations, with all proofs verified by
Lean 4.                                                                                   n  2                
                                                                                          X  n                2n
                                                                                                      =            .           (3)
                                                                                                k              n
                                                                                          k=0
3. Preliminaries
We briefly review the Wilf–Zeilberger method, a certificate-             Step 1 (Normalization). Divide both sides by the right-
based symbolic framework to prove or discover definite sum-              hand side and reduce to the standard form
mation identities (Wilf & Zeilberger, 1990). Let F (n, k) be                     n                                 n 2
                                                                                                                     
                                                                                X
a bivariate hypergeometric term, i.e., F (n + 1, k)/F (n, k)                        F (n, k) = 1,                  k
                                                                                                       F (n, k) := 2n .     (4)
and F (n, k + 1)/F (n, k) are both rational functions of n                      k=0                                    n
and k. Assume that for each fixed n as a nonnegative integer,
F (n, k) vanishes for all but finitely many values of k. The             Step 2 (Certificate synthesis). A symbolic engine
goal of the WZ method is to establish identities of the form             synthesizes a rational certificate

                                                                                                    k 2 (3n − 2k + 3)
                                                                                R(n, k) = −                             ,      (5)
                 S(n) :=
                           X
                                 F (n, k) = C,              (1)                                 2 (n − k + 1)2 (2n + 1)
                            k
                                                                         and defines G(n, k) := R(n, k) F (n, k) such that the
                                                                         WZ relation in Eq.(2) holds.
where the index k runs                                                   Step 3 (Lean-checkable obligations). The proof of the
                          Pon all integers. Note that, for sum-          identity is reduced to a small set of structured obliga-
mations of the form k f (n, k) = r(n) with r(n) ̸= 0,
one can normalize the identity by defining F (n, k) =                    tions: (i) algebraically verify Eq.(2); (ii) show that the
fP(n, k)/r(n), thereby reducing it to the standard form                  boundary terms vanish, i.e., G(n, 0) = G(n, n+1) = 0;
                                                                         and (iii) check the base case to conclude that the con-
    k F (n, k) = 1. This normalization step is crucial in
 practice, as it simplifies the proof to a uniform goal of show-         stant equals 1. Once (i)–(iii) hold, summing Eq. (2)
 ing that the sum equals a constant and thus facilitates the             over k yields S(n + 1) − S(n) = 0 and thus Eq. (3)
 frameworkatic construction of certificates.                             follows.

The core of the WZ method is to build a WZ-pair. Specif-
                                                                       The boxed derivation exposes an executable proof sketch: a
ically, the algorithm seeks an auxiliary term G(n, k) such
                                                                       recurrence/telescoping relation plus boundary obligations,
that the following WZ equation holds:
                                                                       which are exactly the two main types of formal proof task
                                                                       used in our framework. In this work, we use the WZ method
                                                                       as a principled symbolic certification tool to automatically
   F (n + 1, k) − F (n, k) = G(n, k + 1) − G(n, k).         (2)        generate executable proof sketches for combinatorial iden-
                                                                       tities. The resulting sketch transforms the original identity
                                                                       into a set of structured proof obligations, primarily consist-
Under the appropriate boundary conditions, summing both                ing of boundary-condition verification and recurrence-based
sides of the equation over k makes the right-hand side tele-           lemmas. This provides crucial, verifiable structural guidance
scope zero. Hence, we have                                             that constrains the subsequent LLM-based formal proving
                                                                       process and enables scalable proof search in Lean 4.

                        k
                        X                                              4. Methodology
 S(n + 1) − S(n) =              [F (n + 1, k) − F (n, k)] = 0.
                       k=−L                                            In this section, we present WZ-LLM, a neuro-symbolic
                                                                       framework for formally proving combinatorial identities
                                                                       in Lean 4. As shown in Figure 1, for identities that are
This implies that S(n) is independent of n, so the identity            amenable to the WZ method, WZ-LLM first constructs
(1) remains and the constant C can be determined from an               an executable WZ proof sketch and compiles the origi-
initial value S(n0 ). It is required that G(n, k) take the mul-        nal goal into a set of structured proving tasks, including
tiplicative form G(n, k) = R(n, k)F (n, k), where R(n, k)              boundary-condition obligations and recurrence-based lem-
is a rational function, known as the “WZ certificate”. Such            mas. Identities beyond the coverage of the WZ are also
certificates can be found automatically via Gosper’ algo-              incorporated into the task set as direct proving targets. All
rithm or Zeilberger creative telescoping.                              tasks are then discharged by our specialized prover model,

                                                                   3
                                         Submission and Formatting Instructions for ICML 2026

                                                                    WZ-LLM
                                         A. Symbolic Decomposition                                                          B. Model Training
     Candidate                                                                                         Seed Dataset
     Statements

                         WZ Proof Sketch                                                                cold start
                                                  WZ Sub-goals              Proving Task Pool
        WZ         Yes    WZ Invariant          Boundary obligations                                                          DAPO
     applicable?
                           Telescoping           Recurrence lemmas                                                           Training   WZ-Prover
                                                                                                           Prover
           No
                           Summation
                                                                                              train
                                                WZ--uncovered IDs                                      Expert Iteration


                                                                                     retain
                                                                                              Verification Gate    Candidate Proofs


Figure 1. Overview of WZ-LLM. (A) Symbolic decomposition. Given combinatorial-identity statements, the symbolic engine checks
WZ applicability and, when applicable, constructs a WZ proof sketch that is decomposed into sub-goals. Statements that are not amenable
to the WZ method are labeled as WZ-uncovered targets. All sub-goals and uncovered targets form a shared pool of proving tasks. (B)
Model training. We cold-start a prover with a seed dataset, iteratively generate proofs for tasks in the pool, and verify them. Lean-verified
proofs are retained and used for prune/train updates, while unverified ones are discarded. The expert model is further refined with DAPO
to yield WZ-Prover for formally discharging both WZ-derived obligations and WZ-uncovered identities.


WZ-Prover, and the resulting proofs are strictly verified by               the telescoping relation and reduces the original identity to
the Lean kernel. To improve robustness on sketch-induced                   standard WZ obligations: (i) a recurrence lemma showing
subgoals and generalization to out-of-distribution identities,             that the normalized sum S(n) is invariant (or satisfies a lin-
we build a broad-coverage formal training corpus with diffi-               ear recurrence) and (ii) boundary obligations ensuring that
culty stratification, and train WZ-Prover via a combination                the telescoping sum collapses to boundary terms.
of expert-in-the-loop iterative data expansion, and DAPO
                                                                           Constraint inference and side-condition generation. A
refinement with difficulty-smoothing. In general, WZ-LLM
                                                                           major practical obstacle in Lean formalization is that al-
consists of two stages: (i) Symbolic Decomposition using
                                                                           gebraic steps (e.g., field simp) require explicit non-
the WZ method (Section 4.1) and (ii) Model Training for
                                                                           vanishing assumptions for denominators and normalization
WZ-Prover (Section 4.2).
                                                                           factors. We therefore automatically infer domain constraints
                                                                           for each obligation, including when summands or normal-
4.1. Symbolic Decomposition                                                izers become zero/undefined, and compile them into Lean
Given a Lean 4 statement of a combinatorial identity, WZ-                  side-condition goals. Concretely, we use symbolic simplifi-
LLM constructs an WZ-style proof sketch and compiles it                    cation and constraint solving to identify problematic points
into a finite set of Lean proof obligations (Figure 1.A). Cru-             (e.g. zero denominators at boundary indices, negative ar-
cially, it not only produces a WZ certificate/recurrence but               guments to factorial-like terms, or sign-sensitive rewrites),
also generates the auxiliary side conditions and case splits               and then (i) generate corresponding nonzero lemmas (e.g.
needed for successful formalization under Lean’s semantics.                ∀n, k, A(n, k) ̸= 0, ∀n, B(n) ̸= 0), (ii) isolate boundary
                                                                           indices as explicit subgoals, and (iii) trigger case splits when
Normalization. The input is modeled into a canonical sum-                  constraints depend on discrete properties such as parity.
mation form (e.g. Finset.range (n+1) with index
starting at 0) using standard transformations: (i) shifting                Proving Task Pool. Overall, each identity is compiled into
summation ranges not starting at 0; (ii) rewriting bounded                 a proving-task set T = Trec ∪ Tbd ∪ Tside ∪ Tnorm ∪ Tcase ,
sums (Icc, Ico) into range-style sums when possi-                          where Trec contains recurrence lemmas, Tbd contains bound-
ble; (iii) algebraic normalization of hypergeometric factors               ary obligations, Tside contains non-vanishing and well-
(factorials/binomials/powers) to reduce syntactic variance.                typedness conditions required by algebraic tactics, Tnorm
For piecewise specifications (e.g., parity constraints), we                contains normalization/range-shift lemmas, and Tcase con-
compile the goal into structured case splits (e.g. n even/odd)             tains case-split branches. All obligations are expressed as
and treat each branch as an independent proving task.                      Lean goals and are sent to WZ-Prover for formal discharge.
WZ proof sketch construction. When the goal is cov-
                                                                           4.2. Model Training Pipeline for WZ-Prover
ered by the WZ method, a symbolic engine proposes a
recurrence/certificate (e.g., a rational function R(n, k) with             The symbolic stage in Section 4.1 compiles a target identity
G(n, k) = R(n, k)F (n, k)). The sketcher then instantiates                 into a finite set of Lean-checkable proving tasks, including


                                                                       4
                                   Submission and Formatting Instructions for ICML 2026

boundary-condition obligations, lemmas based on recur-              formalized identity proofs. In Round 1, we sample 1020
rence, and direct identity goals. If a valid symbolic sketch        identities; symbolic decomposition produces 7385 lemma
can be synthesized, releasing these obligations yields an           obligations, and we retain 5139 verified lemma proofs plus
end-to-end Lean proof of the original identity. However,            32 verified end-to-end proofs. In Round 2, rerunning on the
symbolic certificate synthesis may fail, and many identities        remaining goals yields 532 additional lemma proofs and 79
fall outside the WZ-applicable class. To bridge this gap, we        identity proofs, so expert iteration adds 5671 lemma proofs
train a combinatorics-specialized Lean prover, WZ-Prover,           and 111 identity proofs in total. Notably, the intermedi-
that covers both: (i) sub-goals produced by symbolic de-            ate lemmas align with key steps in the symbolic trajectory,
composition, and (ii) WZ-uncovered identities that must be          while the full identity proofs help preserve and improve
proved directly without symbolic guidance. Training pro-            end-to-end performance.
ceeds in three stages: (1) supervised cold-start (SFT) on
Expert seed dataset; (2) expert-in-the-loop bootstrapping           4.2.2. DAPO WITH D IFFICULTY-S MOOTHING
that expands the training set with new Lean-verified lemma
                                                                    We further refine WZ-P ROVER with a reinforcement-
and identity proofs; and (3) verifier-based reinforcement
                                                                    learning (RL) stage to improve robustness on long-horizon
learning via DAPO to improve exploration and robustness
                                                                    lemma chaining and hard end-to-end identities. This refine-
on hard proving tasks.
                                                                    ment has two parts: (i) constructing a difficulty-smoothed
Data construction. We adopt a data-flow strategy that               RL set from the SFT corpus, and (ii) applying Dynamic
combines a small high-quality seed dataset, a large pool            Action Policy Optimization (DAPO) (Yu et al., 2025a), a
of unlabeled candidate combinatorial identity statements,           stable Long-CoT optimizer that mitigates entropy collapse,
and expert-in-the-loop iterative expansion, while retaining         truncation-induced reward noise, and training instability.
a source-disjoint test set to evaluate cross-source gener-
                                                                    Our supervised corpus combines (a) a high-quality expert
alization. The resulting training and test sets are named
                                                                    seed set and (b) Lean-verified samples from expert-verified
LCI-training and LCI-Test, respectively. Specifically,
                                                                    iteration over a pool of candidate statements, including both
our dataset consists of three components: (i) Expert seed
                                                                    sketch-induced subgoals (symbolic lemmas) and full iden-
dataset. Based on a classical reference (Spivey, 2019),
                                                                    tity goals. These goal types have markedly different diffi-
we manually formalized 307 combinatorial identities and
                                                                    culty profiles: symbolic decomposition yields many short
provided complete Lean proofs, ensuring all samples are
                                                                    and often repetitive obligations, whereas full identities (and
verified in Lean without sorry. We further applied a sym-
                                                                    hard subgoals) require longer reasoning chains and fail more
bolic decomposition method to split these identities into
                                                                    frequently. To avoid RL overfitting to frequent easy patterns,
CI proving tasks, generating a total of 1200 sub-goals; (ii)
                                                                    we run a rollout-based diagnostic pass to estimate a pass rate
Candidate statements pool. From two additional classi-
                                                                    for each goal under the current policy, use it to tag goals into
cal sources (Quaintance & Gould, 2015; Gould, 2010), we
                                                                    coarse difficulty bins, and filter the extremes by downsam-
extracted and formalized 1020 identity statements in Lean
                                                                    pling near-duplicate easy instances and removing near-zero-
4 as candidate training targets; and (iii) Source-disjoint
                                                                    pass-rate instances that contribute mostly noisy gradients.
test set. We exclusively reserve two classical combinatorial
                                                                    The resulting RL set preserves diverse mid-to-hard goals
identity collections (Gould, 1972; Shi, 2001) for evaluation,
                                                                    while maintaining a smoother difficulty distribution.
selecting 100 problems as the test set. To further reduce
potential data leakage, expressions are canonized to ensure         We then optimize with DAPO using a rule-based outcome
that the canonical forms of test identities do not appear in        reward from Lean verification together with a soft overlong
the candidate pool or training set.                                 punishment:

4.2.1. E XPERT- IN - THE - LOOP BOOTSTRAPPING                                  R(π; G) = Rout (π; G) + λlen Rlen (π),           (6)
The baseline model is cold-started on a high-quality expert         where Rout (π; G) ∈ {+1, −1} indicates whether π kernel-
seed dataset (307 identities with complete Lean proofs, plus        verifies G, and Rlen applies a gradual penalty near the maxi-
1200 framework-extracted lemma proofs) to acquire basic             mum token budget.
proving capability. WZ-LLM then generates proofs for the
candidate statement pool from this cold-start model via two
routes—symbolic decomposition and direct proving—and                5. Experiments
we retain only samples that compile and verify in Lean              We conduct comprehensive experiments on the classical
(deduplicated before training).                                     combinatorial-identity benchmark LCI-Test and two exter-
This process yields two types of new training data: (i) in-         nal benchmarks, CombiBench and PutnamBench-Comb
termediate lemma proofs for WZ sub-goals, and (ii) fully            (the combinatorics subset of PutnamBench), to evaluate the
                                                                    ability of WZ-LLM to produce end-to-end formal proofs

                                                                5
                                   Submission and Formatting Instructions for ICML 2026

in Lean 4. Our evaluation focuses on whether, under a                only if the entire proof is accepted by the Lean 4 kernel.
fixed sampling budget, the framework can leverage proof-             The total training cost is 16 GPU-days, and the evaluation
sketch guidance to generate longer and more structured               cost is 9 GPU-days, all conducted on a 4× L40s-48GB GPU
proof chains, and improve success rates on identities out-           cluster. To quantify the contribution of each component, we
side the coverage of symbolic computation methods (WZ-               report two ablation variants: (i) WZ-Sketch, which retains
uncovered). Specifically, Section 5.2 reports the main results       WZ proof-sketch guidance while removing our specialized
on LCI-Test, establishing the overall effectiveness and gener-       training pipeline; and (ii) WZ-Prover, which retains our
ality of WZ-LLM. Section 5.3 further evaluates its general-          training pipeline and specialized prover while disabling WZ
ization to broader combinatorics problems on CombiBench              proof-sketch guidance. These ablations isolate the gains
and PutnamBench-Comb. Finally, Section 5.4 presents ab-              from symbolic sketching and prover specialization, respec-
lations that isolate the contributions of key training compo-        tively. In the full WZ-LLM framework, goals are solved via
nents.                                                               two complementary routes. The sketch-guided route invokes
                                                                     symbolic WZ decomposition to compile an identity into a
5.1. Experiment Setup                                                set of Lean-checkable lemma obligations, which are then
                                                                     discharged one by one by WZ-Prover (reported as WZ-
5.1.1. B ENCHMARK AND BASELINES                                      Sketch + WZ-Prover in the table). The direct route, used
We evaluate WZ-LLM on three benchmarks: our in-                      when decomposition is inapplicable or fails, attempts an
domain benchmark LCI-Test, and two external benchmarks,              end-to-end Lean proof directly with WZ-Prover (reported
CombiBench and PutnamBench-Comb. LCI-Test is a                       as WZ-uncovered). Finally, we report WZ-LLM as the
combinatorial-identity benchmark constructed from clas-              union of successes from these two routes.
sical references (Gould, 1972; Shi, 2001), containing 100
identities to assess the ability of WZ-LLM to formally prove         5.2. Main Results
combinatorial identities in Lean 4. CombiBench is a widely
                                                                     Table 1 reports end-to-end performance on the classic combi-
used and challenging benchmark for formal combinatorics
                                                                     natorial identity benchmark LCI-Test (100 problems), mea-
theorem proving, consisting of 100 combinatorial prob-
                                                                     sured by the number of fully verified Lean4 proofs. Overall,
lems (Liu et al., 2025). PutnamBench (Tsoukalas et al.,
                                                                     LCI-Test remains challenging for existing provers under
2024), which contains 672 Lean 4-formalized Putnam prob-
                                                                     comparable sampling budgets: DeepSeek-V3 solves 1/100,
lems, we extract a combinatorics subset of 36 problems an-
                                                                     InternLM-2.5-StepProver reaches 2/100, and among whole-
notated with the combinatorics tag, which we refer to
                                                                     proof provers evaluated with pass@32, Kimina-Prover-
as PutnamBench-Comb. These external benchmarks eval-
                                                                     Distill and DeepSeek-Prover-V2 both solve 6/100. Goedel-
uate WZ-LLM’s generalization to broader combinatorics
                                                                     Prover-V2 provides the strongest pass@32 baseline at 9/100.
problems.
                                                                     Component effects. Building on Goedel-Prover-V2, we an-
We compare WZ-LLM against a closed-source LLM,
                                                                     alyze WZ-LLM through two complementary views. Adding
DeepSeek-V3 (Liu et al., 2024), and open-source provers,
                                                                     WZ-Sketch on top of the Goedel-Prover-V2 backend does
including Kimina-Prover-Distill (Wang et al., 2025a),
                                                                     not improve end-to-end results (9/100), indicating that
DeepSeek-Prover-V1.5-RL (Xin et al., 2024), DeepSeek-
                                                                     sketch-only decomposition is insufficient without a stronger
Prover-V2 (Guo et al., 2025), Goedel-Prover-V2 (Lin et al.,
                                                                     lemma prover. In contrast, our trained WZ-Prover im-
2025), MA-LoT (Wang et al., 2025b), and InternLM-2.5-
                                                                     proves direct end-to-end proving to 12/100 under the same
StepProver (Wu et al., 2024).
                                                                     pass@32 budget, demonstrating that the proposed special-
                                                                     ization pipeline strengthens the model’s ability to discharge
5.1.2. I MPLEMENTATION D ETAILS
                                                                     core algebraic subgoals even without symbolic guidance.
For symbolic decomposition, we use S AGE M ATH (Stein &              Two-route solving. Our full framework WZ-LLM com-
Joyner, 2005) as the underlying computer algebra frame-              bines (i) a sketch-guided route for WZ-applicable identi-
work (CAS) to carry out symbolic computations in the                 ties, where WZ-Sketch decomposes the goal into Lean-
WZ/creative-telescoping pipeline. In particular, we rely             checkable obligations that are discharged by WZ-Prover,
on the hypergeometric summation routines provided by the             and (ii) a direct route for WZ-uncovered identities, where
sage.combinat module: given a bivariate hypergeomet-                 WZ decomposition is inapplicable and WZ-Prover attempts
ric term F (n, k), the corresponding WZ certificate C(n, k)          full proofs end-to-end. On LCI-Test, the WZ-uncovered
is synthesized via F.WZ certificate(n,k), and the                    route solves 5 problems, while the sketch-guided route
recurrence ratios are simplified using simplify().                   solves 29 problems, yielding 34 solved problems in total
On all benchmarks, we report end-to-end proof success rates          when aggregated in WZ-LLM.
under the pass@32 metric: a run is counted as successful             This contrast indicates that our framework provides two

                                                                 6
                                    Submission and Formatting Instructions for ICML 2026

Table 1. Main results on LCI-Test. We evaluate our framework WZ-LLM, which combines a symbolic WZ-Sketch decomposer with
a specialized Lean prover WZ-Prover trained from Goedel-Prover-V2. The upper block reports prior baselines under their respective
decoding budgets. The Ours block is organized into two parts. (I) Component effects: WZ-Sketch +Goedel-Prover-V2 matches the
Goedel-Prover-V2 baseline, while WZ-Prover improves direct proving over the same pass@32 budget. (II) Two-route solving: WZ-
uncovered counts identities where WZ decomposition is inapplicable and are solved directly by WZ-Prover; WZ-Sketch+WZ-Prover
counts WZ-applicable identities solved via sketch-induced obligations discharged by WZ-Prover. WZ-LLM aggregates both routes,
achieving the best overall success (34/100).

                 Method                                              Model size    Sample budget       LCI-Test

                 Gemini-3.1-Pro-Preview                                   -            pass@32          16/100
                 DeepSeek-V3 (Liu et al., 2024)                        685B            pass@32           1/100
                 InternLM-2.5-StepProver (Wu et al., 2024)               7B         4 × 32 × 600         2/100
                 MA-LoT (Wang et al., 2025b)                             7B           16 + 8 × 2         3/100
                 Kimina-Prover-Distill (Wang et al., 2025a)              7B            pass@32           6/100
                 DeepSeek-Prover-V2 (Ren et al., 2025)                   7B            pass@32           6/100
                 Goedel-Prover-V2 (Lin et al., 2025)                     8B            pass@32           9/100

                 Ours

                 WZ-Sketch + Goedel-Prover-V2                            8B            pass@32           9/100
                 WZ-Prover                                               8B            pass@32          12/100
                 WZ-uncovered                                            8B            pass@32           5/100
                 WZ-Sketch + WZ-Prover                                   8B            pass@32          29/100
                 WZ-LLM                                                  8B            pass@32          34/100


complementary capabilities: on the one hand, the special-            Goedel-Prover-V2 proves only 564 lemmas (47.88%),
ized WZ-Prover substantially strengthens direct proving              which is insufficient to complete any of the 46 sketched prob-
on problems outside the scope of WZ; on the other hand,              lems because all required obligations must be discharged.
WZ-style symbolic decomposition compiles complex iden-               Replacing it with WZ-Prover raises lemma coverage to
tities into a set of Lean-checkable subgoals, and—when               73.34% (864/1,178), enabling symbolic decomposition to
paired with a strong lemma prover—effectively converts               translate into 29 end-to-end solutions. Overall, these results
the benefits of symbolic computation into markedly higher            show that WZ-style decomposition is most effective when
end-to-end proof success. By integrating these two routes            paired with a specialized lemma prover, and that combining
within a single framework, WZ-LLM achieves a strong                  sketch-guided and direct proving routes yields the strongest
overall end-to-end success rate of 34% on the combinatorial          performance.
identity benchmark.
                                                                     5.3. Cross-Dataset Evaluation
Table 2. Lemma-proving performance on Symbolic Decomposition
subproblems about the base model with our WZ-Prover. WZ-             Table 3 evaluates cross-dataset generalization on Com-
Prover achieves substantially higher lemma accuracy and solves       biBench and PutnamBench-Comb under a fixed pass@32
more end-to-end problems.
                                                                     sampling budget. Baseline provers remain limited on
                                                                     these heterogeneous combinatorial benchmarks: on Com-
  Model                   #Proved        Acc.      #Solved           biBench, Kimina-Prover Distill-8B, DeepSeek-Prover-V2,
                                                                     and Goedel-Prover-V2 solve 6/100, 8/100, and 12/100 prob-
  Goedel-Prover-V2      564 / 1,178    47.88%       0 / 46
                                                                     lems, respectively; on PutnamBench-Comb, they solve 0/36,
  WZ-Prover             864 / 1,178    73.34%      29 / 46           2/36, and 0/36 problems.
                                                                     Component effects. Using WZ-Sketch with the baseline
To understand why sketch-only guidance fails with the un-            Goedel-Prover-V2 provides little benefit: Goedel-Prover-
trained backend, we further perform lemma-level diagnos-             V2 alone solves 12/100 problems on CombiBench, and the
tics on the same 1,178 sketch-induced subgoals (Table 2).

                                                                 7
                                    Submission and Formatting Instructions for ICML 2026

Table 3. Cross-dataset evaluation (pass@32) on CombiBench and PutnamBench-Comb. All our variants are built on Goedel-Prover-
V2 as the base model. The table separates (i) component ablations (WZ-Sketch+Goedel vs. WZ-Prover) and (ii) two-route accounting in
WZ-LLM: the WZ-uncovered route solves goals where WZ decomposition is inapplicable, while the WZ-Sketch+WZ-Prover route
solves WZ-applicable goals via symbolic decomposition plus lemma discharge. WZ-LLM aggregates both routes.

      Method                                  Model size      Sample budget          CombiBench        PutnamBench-Comb

      Kimina-Prover Distill-8B                     8B              pass@32               6/100                  0/36
      DeepSeek-Prover V2-7B                        7B              pass@32               8/100                  2/36
      Goedel-Prover-V2-8B                          8B              pass@32               12/100                 0/36

      Ours

      WZ-Sketch + Goedel-Prover-V2                 8B              pass@32               13/100                 0/36
      WZ-Prover                                    8B              pass@32               15/100                 3/36
      WZ-uncovered                                 8B              pass@32               15/100                 2/36
      WZ-Sketch + WZ-Prover                        8B              pass@32               1/100                  1/36
      WZ-LLM                                       8B              pass@32               16/100                 3/36


sketch-guided variant adds only one extra proof (13/100),                                                     LCI-Test
while on PutnamBench-Comb it offers no improvement                         Training stage
(remaining at 0/36). This indicates that symbolic decom-                                           pass@1     pass@8     pass@32
position alone does not translate into end-to-end success
                                                                           SFT (seed only)          1/100      3/100      9/100
when the backend cannot reliably discharge the induced
                                                                             + expert-iteration     3/100      6/100      10/100
lemma obligations. In contrast, our trained WZ-Prover
substantially improves direct proving, reaching 15/100 on                    + DAPO refinement      4/100      6/100      12/100
CombiBench and 3/36 on PutnamBench-Comb, outperform-                   Table 4. Training-stage ablations for WZ-Prover on LCI-Test.
ing Goedel-Prover-V2 by +3 and +3 problems, respectively.
Two-route accounting in WZ-LLM. We decompose WZ-
LLM’s performance into its two proof routes. On Com-                   seed supervision is insufficient to generalize to the harder
biBench, the WZ-uncovered (WZ-inapplicable) route con-                 identities in LCI-Test. Incorporating expert-verified itera-
tributes 15 solved problems via direct proving, while the              tion improves performance to 3/100, 6/100, and 10/100, con-
sketch-guided route (WZ-Sketch+WZ-Prover) contributes                  sistent with verifier-filtered data growth that introduces ad-
1 additional solved problem through symbolic decompo-                  ditional WZ-induced obligations and diverse identity proofs
sition and lemma discharge, yielding 16/100 overall. On                (see Appendix C). After deduplication and filtering, the re-
PutnamBench-Comb, direct proving solves 2/36 problems,                 sulting SFT corpus contains 418 Lean-verified identities and
and the sketch-guided route adds 1/36, resulting in 3/36.              roughly 5,000 lemma proofs (about 5,418 samples in total).
Overall, these results reinforce the same conclusion as on             Finally, DAPO refinement further raises performance to
LCI-Test: WZ-Prover is the main driver of generalization               4/100, 6/100, and 12/100. Notably, the improvement is
via stronger direct proof capability, while sketch-guided              concentrated at larger sampling budgets (pass@32), which
decomposition can provide additive gains when WZ de-                   suggests that RL primarily helps on harder instances that
composition is applicable and the resulting obligations are            require longer proof trajectories and benefit from increased
within the lemma prover’s reach.                                       exploration, rather than on the easiest problems already
                                                                       solved by SFT. Additional implementation details for the RL
5.4. Effect of Training Stages                                         set construction (difficulty smoothing via pass-rate filtering)
                                                                       and DAPO settings are provided in Appendix C.
Table 4 reports stage-wise ablations for WZ-P ROVER on
LCI-Test, isolating the effects of seed SFT, expert-verified it-
eration, and DAPO refinement. The cold-start model trained             6. Conclusion
on the seed set alone achieves only 1/100 at pass@1, 3/100             We propose WZ-LLM, a neuro-symbolic framework that in-
at pass@8, and 9/100 at pass@32, indicating that the expert            tegrates the Wilf–Zeilberger method with LLM-based prov-

                                                                   8
                                  Submission and Formatting Instructions for ICML 2026

ing for combinatorial identities in Lean 4. WZ-LLM trans-            ric summation. Proceedings of the National Academy of
lates WZ proof plans into executable proof sketches and              Sciences of the United States of America, 75(1):40—42,
uses a trained prover, WZ-Prover, to discharge the resulting         January 1978. ISSN 0027-8424. doi: 10.1073/pnas.75.
machine-checkable subgoals. This approach provides princi-           1.40. URL https://europepmc.org/articles
pled long-horizon proof planning while extending coverage            /PMC411178.
beyond purely symbolic methods. Across multiple bench-
marks, WZ-LLM achieves higher proof success rates than             Gould, H. W. Combinatorial Identities. West Virginia
strong LLM baselines; on LCI-Test, it additionally proves            University, Morgantown, WV, 1972.
identities that defeat a symbolic-only baseline. Overall,
these results indicate that coupling symbolic proof planning       Gould, H. W. Tables of combinatorial identities (from the
with learned formal reasoning is a promising direction for           seven unpublished manuscripts of h. w. gould). Un-
machine-checkable scalable verification in combinatorics.            published manuscript collection, 2010. URL https:
                                                                    //math.wvu.edu/˜hgould/. Edited and compiled
                                                                     by Jocelyn Quaintance (May 3, 2010). Collection of PDF
Impact Statement                                                    volumes hosted online.
This paper presents a Lean-verified proving framework that
combines symbolic WZ decomposition with a trained neural           Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R.,
prover. The approach can improve automation for formal-              Zhu, Q., Ma, S., Wang, P., Bi, X., et al. Deepseek-r1: In-
izing combinatorial identities and reduce the manual effort          centivizing reasoning capability in llms via reinforcement
needed to obtain kernel-checked proofs. We do not an-                learning. arXiv preprint arXiv:2501.12948, 2025.
ticipate direct negative societal impacts beyond standard
concerns about overreliance on automated tools; all results        Harrison, J. Hol light: A tutorial introduction. In Interna-
are validated by the Lean 4 kernel.                                  tional Conference on Formal Methods in Computer-Aided
                                                                     Design, pp. 265–269. Springer, 1996.
References                                                         Harrison, J. Formal proofs of hypergeometric sums. Journal
Chen, L., Gu, J., Huang, L., Huang, W., Jiang, Z., Jie,              of Automated Reasoning, 55(3):223–243, 2015. doi: 10.1
  A., Jin, X., Jin, X., Li, C., Ma, K., Ren, C., Shen, J.,           007/s10817-015-9338-0.
  Shi, W., Sun, T., Sun, H., Wang, J., Wang, S., Wang,
  Z., Wei, C., Wei, S., Wu, Y., Wu, Y., Xia, Y., Xin, H.,          Kauers, M. and Paule, P. The Concrete Tetrahedron - Sym-
  Yang, F., Ying, H., Yuan, H., Yuan, Z., Zhan, T., Zhang,           bolic Sums, Recurrence Equations, Generating Functions,
  C., Zhang, Y., Zhang, G., Zhao, T., Zhao, J., Zhou, Y.,           Asymptotic Estimates. Texts & Monographs in Symbolic
  and Zhu, T. H. Seed-prover: Deep and broad reasoning               Computation. Springer, 2011. ISBN 978-3-7091-0444-
  for automated theorem proving. 2025. URL https:                    6. doi: 10.1007/978-3-7091-0445-3. URL https:
  //arxiv.org/abs/2507.23726.                                       //doi.org/10.1007/978-3-7091-0445-3.

Cox, D. A., Little, J., and O’Shea, D. Ideals, varieties,          Langley, P. Crafting papers on machine learning. In Langley,
  and algorithms - an introduction to computational alge-            P. (ed.), Proceedings of the 17th International Conference
  braic geometry and commutative algebra (2. ed.). Un-               on Machine Learning (ICML 2000), pp. 1207–1216, Stan-
  dergraduate texts in mathematics. Springer, 1997. ISBN             ford, CA, 2000. Morgan Kaufmann.
  978-0-387-94680-1.
                                                                   Lin, Y., Tang, S., Lyu, B., Yang, Z., Chung, J.-H., Zhao,
Flajolet, P. and Sedgewick, R. Analytic Combinatorics.               H., Jiang, L., Geng, Y., Ge, J., Sun, J., et al. Goedel-
  Cambridge University Press, 2009.                                  prover-v2: Scaling formal theorem proving with scaf-
Google DeepMind. Advanced version of gemini with deep                folded data synthesis and self-correction. arXiv preprint
  think officially achieves gold medal standard at the in-           arXiv:2508.03613, 2025.
  ternational mathematical olympiad. Technical report,
  Google DeepMind, 2025. URL https://deepmi                        Liu, A., Feng, B., Xue, B., Wang, B., Wu, B., Lu, C., Zhao,
  nd.google/blog/advanced-version-of-g                               C., Deng, C., Zhang, C., Ruan, C., et al. Deepseek-v3
  emini-with-deep-think-officially-ach                               technical report. arXiv preprint arXiv:2412.19437, 2024.
  ieves-gold-medal-standard-at-the-int
  ernational-mathematical-olympiad/. Ac-                           Liu, J., Lin, X., Bayer, J., Dillies, Y., Jiang, W., Liang, X.,
  cessed: 2026-01-15.                                                Soletskyi, R., Wang, H., Xie, Y., Xiong, B., et al. Com-
                                                                     bibench: Benchmarking llm capability for combinatorial
Gosper, R. Decision procedure for indefinite hypergeomet-            mathematics. arXiv preprint arXiv:2505.03171, 2025.

                                                               9
                                   Submission and Formatting Instructions for ICML 2026

Moura, L. d. and Ullrich, S. The lean 4 theorem prover               Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Santos,
 and programming language. In Automated Deduction–                    M. D., Sung, F., Vinyes, M., Ying, Z., Zhu, Z., et al.
 CADE 28: 28th International Conference on Automated                  Kimina-prover preview: Towards large formal reason-
 Deduction, Virtual Event, July 12–15, 2021, Proceedings              ing models with reinforcement learning. arXiv preprint
 28, pp. 625–635. Springer, 2021.                                     arXiv:2504.11354, 2025a.
Ospanov, A., Farnia, F., and Yousefzadeh, R. Apollo: Au-             Wang, R., Zhang, J., Jia, Y., Pan, R., Diao, S., Pi, R., and
  tomated llm and lean collaboration for advanced formal              Zhang, T. Theoremllama: Transforming general-purpose
  reasoning. arXiv preprint arXiv:2505.05758, 2025.                   llms into lean4 experts. In 2024 Conference on Empiri-
Paulson, L. C. Isabelle: A generic theorem prover. Springer,          cal Methods in Natural Language Processing, EMNLP
  1994.                                                               2024, pp. 11953–11974. Association for Computational
                                                                      Linguistics (ACL), 2024.
Petkovsek, M., Wilf, H., and Zeilberger, D. A = B. CRC
  Press, 1996. ISBN 9781040187944. URL https://                      Wang, R., Pan, R., Li, Y., Zhang, J., Jia, Y., Diao, S., Pi,
  books.google.com.nf/books?id=I4qNEQA                                R., Hu, J., and Zhang, T. Ma-lot: Model-collaboration
  AQBAJ.                                                              lean-based long chain-of-thought reasoning enhances for-
                                                                      mal theorem proving. arXiv preprint arXiv:2503.03205,
Polu, S. and Sutskever, I. Generative language model-                 2025b.
  ing for automated theorem proving. arXiv preprint
  arXiv:2009.03393, 2020.                                            Wang, R., Yao, J., Pan, R., Diao, S., and Zhang, T. Gar:
                                                                      Generative adversarial reinforcement learning for formal
Quaintance, J. and Gould, H. Combinatorial Identities for             theorem proving, 2025c. URL https://arxiv.or
 Stirling Numbers: The Unpublished Notes of H W Gould.                g/abs/2510.11769.
  08 2015. ISBN 978-981-4725-26-2. doi: 10.1142/9821.
                                                                     Wei, C., Sun, M., and Wang, W. Proving olympiad alge-
Ren, Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao, W.,
                                                                      braic inequalities without human demonstrations. arXiv
  Zhang, L., Fu, Z., Zhu, Q., Yang, D., et al. Deepseek-
                                                                      preprint arXiv:2406.14219, 2024.
  prover-v2: Advancing formal mathematical reasoning via
  reinforcement learning for subgoal decomposition. arXiv            Wilf, H. S. generatingfunctionology. CRC press, 2005.
  preprint arXiv:2504.21801, 2025.
                                                                     Wilf, H. S. and Zeilberger, D. Rational functions certify
Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang,
                                                                      combinatorial identities. Journal of the American Math-
  H., Zhang, M., Li, Y., Wu, Y., et al. Deepseekmath: Push-
                                                                      ematical Society, 3(1):147–158, 1990. ISSN 08940347,
  ing the limits of mathematical reasoning in open language
                                                                      10886834. URL http://www.jstor.org/stab
  models. arXiv preprint arXiv:2402.03300, 2024.
                                                                      le/1990986.
Shi, J. Combinatorial Identities. University of Science and
  Technology of China Press, 2001.                                   Wilf, H. S. and Zeilberger, D. An algorithmic proof theory
                                                                      for hypergeometric (ordinary and “q”) multisum/integral
Spivey, M. Z. The art of proving binomial identities. Chap-           identities. Inventiones mathematicae, 108(1):575–633,
  man and Hall/CRC, 2019.                                             1992.
Stanley, R. P. What is enumerative combinatorics? Springer,          Wu, Z., Huang, S., Zhou, Z., Ying, H., Wang, J., Lin, D., and
  1986.                                                               Chen, K. Internlm2.5-stepprover: Advancing automated
Stein, W. and Joyner, D. Sage: system for algebra and                 theorem proving via expert iteration on large-scale LEAN
  geometry experimentation. SIGSAM Bull., 39(2):61–64,                problems. CoRR, abs/2410.15700, 2024. doi: 10.48550
  June 2005. ISSN 0163-5824. doi: 10.1145/1101884.11                  /ARXIV.2410.15700. URL https://doi.org/10
  01889. URL https://doi.org/10.1145/1101                             .48550/arXiv.2410.15700.
  884.1101889.                                                       Xin, H., Guo, D., Shao, Z., Ren, Z., Zhu, Q., Liu, B., Ruan,
Sturmfels, B. Solving systems of polynomial equations.                 C., Li, W., and Liang, X. Deepseek-prover: Advancing
  Number 97. American Mathematical Soc., 2002.                         theorem proving in llms through large-scale synthetic
                                                                       data. arXiv preprint arXiv:2405.14333, 2024.
Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M., Jen-
  nings, M., Thakur, A., and Chaudhuri, S. Putnambench:              Xin, R., Xi, C., Yang, J., Chen, F., Wu, H., Xiao, X., Sun,
  A multilingual competition-mathematics benchmark for                 Y., Zheng, S., and Shen, K. Bfs-prover: Scalable best-
  formal theorem-proving. In AI for Math Workshop@                     first tree search for llm-based automatic theorem proving.
  ICML 2024, 2024.                                                     arXiv preprint arXiv:2502.03438, 2025.

                                                                10
                                    Submission and Formatting Instructions for ICML 2026

Xiong, B., Lv, H., Shan, H., Wang, J., Yang, Z., and Zhi,
  L. A combinatorial identities benchmark for theorem
  proving via automated theorem generation, 2025. URL
  https://arxiv.org/abs/2502.17840.
Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P.,
  Yu, S., Godil, S., Prenger, R. J., and Anandkumar, A.
  Leandojo: Theorem proving with retrieval-augmented
  language models. Advances in Neural Information Pro-
  cessing Systems, 36, 2024.
Yu, Q., Zhang, Z., Zhu, R., Yuan, Y., Zuo, X., Yue, Y., Dai,
  W., Fan, T., Liu, G., Liu, L., Liu, X., Lin, H., Lin, Z., Ma,
  B., Sheng, G., Tong, Y., Zhang, C., Zhang, M., Zhang,
  W., Zhu, H., Zhu, J., Chen, J., Chen, J., Wang, C., Yu, H.,
  Song, Y., Wei, X., Zhou, H., Liu, J., Ma, W.-Y., Zhang,
  Y.-Q., Yan, L., Qiao, M., Wu, Y., and Wang, M. Dapo: An
  open-source llm reinforcement learning system at scale,
  2025a. URL https://arxiv.org/abs/2503.1
  4476.

Yu, Z., Peng, R., Ding, K., Li, Y., Peng, Z., Liu, M.,
  Zhang, Y., Yuan, Z., Xin, H., Huang, W., et al. Formal-
  math: Benchmarking formal mathematical reasoning of
  large language models. arXiv preprint arXiv:2505.02735,
  2025b.

Zeilberger, D. The method of creative telescoping. J. Symb.
  Comput., 11(3):195–204, 1991.
Zhou, X., Lei, Y., Zhou, X., Sun, J., Zhu, Y., Ye, Z., Zhang,
  W., Liu, Q., Wei, S., and Liu, C. Spark-prover-x1: Formal
  theorem proving through diverse data training. arXiv
  preprint arXiv:2511.13043, 2025.




                                                                  11
                                   Submission and Formatting Instructions for ICML 2026

A. Glossary of Symbolic and Formal-Proof Terms
To better understand the terms, we provide this chart that explains in detail every term, abbreviation, and corresponding tool.

A.1. WZ and Symbolic-Computation Terms
Hypergeometric term. A bivariate term F (n, k) is (bi-)hypergeometric if the ratios F (n, k + 1)/F (n, k) and F (n +
1, k)/F (n, k) are rational functions in (n, k). Many WZ/creative-telescoping procedures apply only to identities whose
summands admit such rational ratios.
                                        P                          
Telescoping sum. A sum of the form k G(n, k + 1) − G(n, k) is telescoping: all intermediate terms cancel, leaving
only boundary contributions. Thus, if the boundary terms vanish, the whole sum is evaluated to 0.

WZ pair.    A WZ pair is a pair of terms (F, G) that satisfy
                                   F (n + 1, k) − F (n, k) = G(n, k + 1) − G(n, k),
                                                                       P
so that summing over k yields a (typically constant) behavior of S(n) = k F (n, k) under suitable boundary conditions.

WZ certificate R(n, k). In WZ proofs one often sets G(n, k) = R(n, k)F (n, k), where R(n, k) is a rational function.
This R is called a certificate; once proposed by a CAS, the remaining work is to verify the induced rational identity and the
boundary conditions within the proof assistant.

Creative telescoping / Zeilberger algorithm. Creative telescoping generalizes WZ by producing higher-order relations
                                     J
                                     X
                                           aj (n) F (n + j, k) = G(n, k + 1) − G(n, k),
                                     j=0
                                               P
which induce a linear recurrence for S(n) =      k F (n, k) after summing over k. The case J = 1 recovers the classical WZ
equation.

Recurrence relation. A recurrence is an equation that relates S(n) to different n (e.g., first-order or higher-order linear
recurrences). In our setting, proving the recurrence together with a base case is sufficient to determine S(n) and close the
target identity.

Boundary conditions / boundary obligations. To justify telescoping in a finite range (e.g., k = 0, . . . , n), one must
prove that the boundary terms vanish (or match) at the endpoints, such as G(n, 0) = 0 and G(n, n + 1) = 0. These are
emitted as explicit boundary obligations.
                                   P                                                        P
Normalization. For an identity k f (n, k) = r(n) with r(n) ̸= 0, we normalize to k F (n, k) = 1 by setting
F (n, k) = f (n, k)/r(n). This reduces the goal to proving the constancy of the normalized sum plus a base case.

Summation range transformation.         Many identities require rewriting sums to a canonical range, e.g.,
                                                   b
                                                   X               b−a
                                                                   X
                                                         f (k) =         f (k + a),
                                                   k=a             k=0

Separate a few boundary terms. Such transformations are often needed to match the requirements of WZ-style decomposition.

Singularity / nonzero side conditions. Symbolic certificates frequently introduce denominators. Formal verification
therefore requires side conditions ensuring that those denominators are nonzero in the relevant domain (e.g., to justify
field simp steps in Lean).

A.2. Automated Theorem Proving Terms
Kernel verification. Lean’s trusted kernel checks that the produced proof term/script is valid. All reported successes
correspond to proofs accepted by the kernel.

                                                                   12
                                  Submission and Formatting Instructions for ICML 2026

Proof obligation. A proof obligation is a subgoal generated by a proof sketch (e.g., a boundary condition or a recurrence
lemma) that must be proved to complete the overall proof.

pass@k (e.g., pass@32). pass@k measures whether at least one of the k independently sampled proof attempts verifies.
It is standard for stochastic theorem provers where success is probabilistic.

Executable proof sketch. In this paper, a proof sketch is not a natural-language outline but a structured, machine-checkable
decomposition (e.g., recurrence + boundary obligations + base case) that can be executed in Lean as a sequence of formal
subgoals.

WZ-covered vs. WZ-uncovered identities. An identity is WZ-covered if the symbolic engine can synthesize a WZ/creative-
telescoping certificate and emit a sketch. Otherwise, it is WZ-uncovered and is treated as a direct proving target.

WZ sub-goals and CI proving tasks. WZ sub-goals refer to the boundary obligations and recurrence lemmas produced
by sketch construction. CI proving tasks include both these sub-goals and the WZ-uncovered identities, forming the unified
task set solved by WZ-Prover.

Expert iteration / verifier-filtered bootstrapping. We repeatedly sample candidate proofs from the current prover for
a pool of unproven statements, keep only Lean-verified proofs, and add the resulting pairs (statement, proof) back to the
training set. We then update the prover and continue on the remaining statements, expanding coverage while maintaining
formal correctness.

Goal / theorem statement. A goal G denotes a Lean proposition to be proved (either a full identity or an intermediate
lemma). We write V(G, π) = true if the Lean kernel verifies that the tactic script π proves G.

Candidate statement. A candidate statement is an unlabeled target identity extracted from external sources (e.g., tables
of identities) and normalized into a uniform, Lean-parseable form. The pool of candidate statements is used for expert-in-
the-loop bootstrapping and data expansion.

B. Pseudocode for WZ-LLM and WZ-Prover Training
Our approach combines the complementary strengths of symbolic computation and learned proof search: symbolic WZ
decomposition externalizes long-horizon proof planning into a set of locally checkable obligations, while a specialized Lean
prover efficiently discharges the resulting algebraic and boundary subgoals. To make this neuro-symbolic workflow precise
and reproducible, we summarize the inference-time framework and the corresponding training pipeline in Algorithm 1 and
Algorithm 2.
We present our end-to-end proving framework WZ-LLM (Algorithm 1) and the training pipeline for the resulting prover
WZ-Prover (Algorithm 2). At inference time, WZ-LLM queries a symbolic engine to construct a WZ-style proof sketch,
consisting of a recurrence structure together with boundary-condition obligations. When WZ decomposition succeeds, the
framework reduces the original identity into a set of Lean-checkable subgoals, which are then discharged by WZ-Prover
in Lean4. If the identity is WZ-inapplicable (i.e., no certificate/sketch can be synthesized), WZ-LLM falls back to direct
proving using WZ-Prover. All generated proofs and proof fragments are strictly verified by the Lean kernel.

Algorithm 1: Sketch-guided neuro-symbolic proving. Algorithm 1 describes the inference-time procedure of WZ-LLM.
Given a target Lean goal S, the framework maintains a queue Q of pending obligations and iteratively processes each goal
G popped from the queue. To avoid redundant work (e.g., repeated lemmas produced by different decompositions), we
maintain a visited set Sseen and skip any goal that has already been processed.
For each goal G, WZ-LLM queries the symbolic backend E via WZ-D ECOMPOSE. If the goal is WZ-applicable, the
backend returns (i) an executable Lean sketch and (ii) a finite set of Lean-checkable obligations L, which typically include
recurrence/ratio checks, boundary conditions, normalization steps, and non-vanishing side conditions needed to justify
telescoping. The sketch is stored as a kernel-checkable fragment in P, while each obligation ℓ ∈ L is pushed into Q for
subsequent discharge (subject to deduplication by Sseen ).

                                                            13
                                   Submission and Formatting Instructions for ICML 2026

Algorithm 1 WZ-LLM: Sketch-Guided Neuro-Symbolic Proving in Lean4
  Input: target goal S, WZ engine E, prover M (WZ-Prover), Lean verifier V
  Output: Lean4-verified proof of S or FAIL
  Q ← {S} {queue of pending obligations}
  P ← ∅ {kernel-checkable proof fragments}
  Sseen ← ∅ {visited goals (dedup)}
  while Q ̸= ∅ do
    Pop G from Q
    if G ∈ Sseen then
       continue
    end if
    Sseen ← Sseen ∪ {G}
    (applicable, sketch, L) ← E(WZ-D ECOMPOSE, G)
    if applicable then
       P ← P ∪ {sketch} {Lean skeleton reducing G to obligations in L}
       for each ℓ ∈ L do
          if ℓ ∈
               / Sseen then
             Push ℓ into Q
          end if
       end for
    else
       π ← M(G) {direct proving for WZ-inapplicable goals}
       if V(G, π) then
          P ← P ∪ {π}
       else
          return FAIL
       end if
    end if
  end while
  return A SSEMBLE(P) {assemble fragments; Lean kernel checks final proof}


If WZ-D ECOMPOSE reports that G is WZ-inapplicable, the system falls back to direct proving: the learned prover M
(WZ-Prover) generates a tactic script π ← M(G), which is accepted only if the Lean verifier V confirms V(G, π) = true.
Any verifier failure causes the procedure to return FAIL. Finally, once Q is exhausted, A SSEMBLE(P) combines all verified
fragments (sketches and lemma proofs) into a complete end-to-end proof, which is again checked by the Lean kernel.

Algorithm 2: Training pipeline for WZ-Prover. Algorithm 2 details the three-stage training pipeline that produces
WZ-Prover. The procedure starts from a small expert-verified seed dataset Dseed and performs supervised fine-tuning (SFT)
to obtain an initial prover M. It then performs expert-in-the-loop dataset expansion for T rounds over a pool of candidate
goals Scand . In each round t, the algorithm generates new training samples Dnew from two sources. When a sampled goal S
is WZ-applicable, we decompose it into obligations L and attempt to prove each lemma ℓ ∈ L using the current prover M.
Draft proofs π̂ℓ are then curated through E XPERT R EPAIR A ND F ILTER, which repairs incomplete or partially correct traces,
filters out low-quality outputs, and returns a cleaned pair (ℓ′ , πℓ ) only when a proof is well-formed and verifiable. When S
is WZ-inapplicable, we instead attempt to directly prove the full identity with M and apply the same expert repair/filtering
step, yielding (S ′ , πS ) when successful. All accepted samples must pass Lean verification under V.
After collecting Dnew , we augment the training set D ← D ∪ Dnew and retrain the prover with SFT on the expanded
Lean-verified dataset, repeating for T rounds. Finally, we apply DAPO refinement to further improve long-horizon lemma
chaining and robustness. In contrast to modifying the reward design, our refinement relies on difficulty-smoothing data
curation: we run a rollout-based diagnostic pass to estimate goal pass rates under the current policy, bucket goals into coarse
difficulty bins, and then downsample redundant easy instances while removing near-zero-pass-rate goals that contribute
mostly noisy gradients (Appendix 4.2.2). DAPO is then applied on this curated RL set using the same reward definition as
in Eq. 6. The resulting model M⋆ is returned as the final WZ-Prover.

                                                              14
                                  Submission and Formatting Instructions for ICML 2026

Algorithm 2 WZ-Prover Training: Seed SFT → Expert Iteration → DAPO Refinement
  Input: seed proofs Dseed , candidate goals Scand , WZ engine E, Lean verifier V, expert rounds T
  Output: trained prover M⋆ (WZ-Prover)
  M ← SFT(Dseed )                                                                                               // cold-start
  D ← Dseed
  for t = 1 to T do
     Dnew ← ∅
     for each sampled goal S ∈ Scand do
       (applicable, sketch, L) ← E(WZ-D ECOMPOSE, S)
       if applicable then
          for each lemma ℓ ∈ L do
             π̂ℓ ← M(ℓ)
             (ℓ′ , πℓ ) ← E XPERT R EPAIR A ND F ILTER(ℓ, π̂ℓ )
             if (ℓ′ , πℓ ) ̸= ∅ and V(ℓ′ , πℓ ) then
                 Dnew ← Dnew ∪ {(ℓ′ , πℓ )}
             end if
          end for
       else
          π̂S ← M(S)
          (S ′ , πS ) ← E XPERT R EPAIR A ND F ILTER(S, π̂S )
          if (S ′ , πS ) ̸= ∅ and V(S ′ , πS ) then
             Dnew ← Dnew ∪ {(S ′ , πS )}
          end if
       end if
     end for
     D ← D ∪ Dnew
     M ← SFT(D)                                                                                 // retrain on expanded data
  end for
  // DAPO refinement with difficulty-smoothing data curation (Appendix 4.2.2)
  M⋆ ← DAPO(M; R(π; G))
  return M⋆


C. More Experimental Details
This appendix reports implementation and reproducibility details, covering additional experimental settings (tooling, token
budgets, and optimization hyperparameters).

C.1. Software Stack and Tooling
Lean environment. All proofs are checked in leanprover/lean4:v4.25.0. Kernel verification is treated as the sole
correctness criterion.
Symbolic backend. We use SageMath 10.7 for symbolic computation, including WZ certificate/recurrence synthesis and
auxiliary ratio simplifications. Sage is invoked programmatically via Python.
Inference runtime. Model inference is run with vLLM 0.13.0. For baseline provers that rely on long chain-of-thought
(Kimina-Prover, MA-LoT, DeepSeek-Prover-V2, and Goedel-Prover-V2), we cap the reasoning length at 16,384 tokens to
reduce compute while keeping the sampling budget comparable (pass@32 where applicable). Other baselines follow the
official decoding and token-limit settings provided in their released code.

C.2. Evaluation Budget and Token Limits.
We report end-to-end success under pass@32 where applicable. To keep compute manageable for long-reasoning baselines
(Kimina-Prover, MA-LoT, DeepSeek-Prover-V2, Goedel-Prover-V2), we cap the reasoning length at 16,384 tokens. Other
baselines follow their official evaluation settings.

                                                            15
                                      Submission and Formatting Instructions for ICML 2026

         Stage                         Accepted identities   Seed lemmas      Generated obligations     Accepted lemmas

         Seed dataset                                 307            1,200                          –                1,200

         Expert iteration (Round 1)                     32                –                     7,385                5,139
         Expert iteration (Round 2)                     79                –                     2,246                  532

         Total (accepted)                             418                 –                         –                6,871
Table 5. Training data growth via expert-verified iteration. We start from a seed corpus of 307 Lean-verified identities and 1,200
framework-extracted lemma proofs. Each iteration samples identity statements, decomposes them into lemma obligations when applicable,
and retains only Lean-verified and deduplicated outputs. Across two rounds, expert iteration adds 111 new identity proofs and 5,671
lemma proofs, yielding 418 identities and 6,871 lemmas in total.



C.3. Prompting Protocol
We use the same instruction-following structure throughout training and evaluation. Each instance asks the model to (i)
provide a short proof plan that identifies key lemmas/tactics, and (ii) output a complete Lean4 proof script that closes the
goal without using sorry. For WZ-induced obligations, the prompt additionally includes CAS-produced artifacts (e.g.,
rational certificates or simplified ratios) as explicit context, so that Lean-side verification focuses on well-definedness,
algebraic rewriting, and recurrence/telescoping checks.

D. Training Data Details
Our training corpus contains two major categories: (i) symbolic-induced lemmas produced by WZ-style decomposition (and
related algebraic simplifications), and (ii) end-to-end identity proofs for goals that can be discharged directly (including
identities not covered by WZ decomposition). All retained samples must be compile and verified in Lean; we also duplicate
the proofs before adding them to the training set.
Expert-verified iteration. We perform expert-verified dataset expansion for T = 2 rounds. In each round, we sample
identities from the candidate pool, apply symbolic decomposition to generate lemma obligations, and let the prover attempt
both (i) lemma proofs for sketch-induced subgoals and (ii) direct end-to-end identity proofs. We retain only samples that
compile and verify in Lean, and we deduplicate accepted proofs before adding them to the training corpus in Table 5.
RL dataset size and composition. The RL stage operates on a filtered subset of the Lean-verified SFT corpus obtained from
the seed set plus expert-verified iteration (Table 5). To smooth the difficulty mismatch between sketch-induced lemmas (often
short and repetitive) and full-identity goals (typically long-horizon and failure-prone), we run a rollout-based diagnostic pass
and estimate a pass rate for each goal under the current policy. We then construct the RL set by downsampling large clusters
of high-pass-rate, near-duplicate easy instances and excluding near-zero-pass-rate goals whose rollouts are dominated
by truncation or early failure. The resulting RL set emphasizes diverse mid-to-hard goals, contains a higher fraction of
long-horizon proof trajectories, and still mixes lemma-style subgoals (e.g., ratio/non-vanishing obligations) with full identity
goals to preserve end-to-end capability. All RL prompts follow the same prover input template, and each rollout is scored by
Lean kernel verification plus the soft overlong punishment in Eq. 6.

D.1. Lemma types and data format
Symbolic-induced training instances are dominated by two recurring lemma families: (i) ratio lemmas, which expose
CAS-precomputed term ratios (e.g., A(n,k+1)/A(n,k) or A(n+1,k)/A(n,k)) to avoid expensive normalization inside Lean;
and (ii) non-vanishing (well-definedness) lemmas, which establish that denominators are nonzero, enabling safe use of
field simp and preventing singularities during normalization and recurrence checking. All lemma samples are stored
as instruction-following triples (instruction/input/output): the input contains a Lean goal template, and the
output includes (a) a brief proof plan and (b) a complete Lean4 proof script. We give one example for each lemma type
below (formatted identically to training instances).
The first example illustrates a typical “local obligation” that frequently appears in our pipeline (e.g., when normalizing
expressions or discharging boundary side conditions). Such goals are not mathematically deep, but they are essential for
making later simp/field simp steps well-defined and for keeping the main proof trace stable.

                                                                16
                                   Submission and Formatting Instructions for ICML 2026


Statement (Lean goal).

  1   import Mathlib
  2
  3   open Nat Finset BigOperators
  4
  5 theorem factorial_succ_ge_one {n : N} (h : 1 ≤ n) :
  6   n * (n - 1)! = n! := by
  7   -- to be completed


Proof / Model Output.
Problem. Show that for any natural number n with 1 ≤ n, we have

                                                       n · (n − 1)! = n!.

Key observations.

  1. The hypothesis 1 ≤ n implies 0 < n, which lets us rewrite n as (n − 1) + 1 via Nat.succ pred eq of pos.
  2. Lean’s factorial recurrence is encoded as Nat.factorial succ: (m+1)! = (m+1) * m!. Therefore, once we
     rewrite n as (n-1)+1, the goal reduces to a direct rewrite by Nat.factorial succ.

  3. No induction is needed: the proof is a one-step normalization that bridges the arithmetic identity n = (n-1)+1 with the
     definitional equation of factorial.

Proof plan.

      1. Derive 0 < n from the assumption 1 ≤ n.
      2. Rewrite n as (n - 1) + 1 using Nat.succ pred eq of pos.

      3. Replace n! by ((n-1)+1)! and rewrite it using Nat.factorial succ.

      4. Finish by simplification (simp) and associativity/commutativity normalization (ring is unnecessary for N here).


Complete Lean 4 Proof.

  1   import Mathlib
  2
  3   open Nat Finset BigOperators
  4
  5 theorem factorial_succ_ge_one {n : N} (h : 1 ≤ n) :
  6   n * (n - 1)! = n! := by
  7   have hn : 0 < n := Nat.pos_of_ne_zero (by
  8     -- 1 ≤ n implies n ̸= 0
  9     exact Nat.ne_of_gt (Nat.lt_of_lt_of_le Nat.zero_lt_one h))
 10   -- rewrite n as (n - 1) + 1
 11   have hn’ : (n - 1).succ = n := Nat.succ_pred_eq_of_pos hn
 12   -- turn it into a rewriting form n = (n - 1) + 1
 13   have hn’’ : n = (n - 1) + 1 := by
 14     -- succ is +1 in Nat
 15     simpa [Nat.succ_eq_add_one] using hn’.symm
 16   -- use factorial_succ on m = n-1
 17   -- (n-1+1)! = (n-1+1) * (n-1)!
 18   -- then rewrite (n-1+1) as n
 19   calc
 20     n * (n - 1)! = ((n - 1) + 1) * (n - 1)! := by
 21        simpa [hn’’]
 22     _ = ((n - 1) + 1)! := by
 23        simpa [Nat.factorial_succ]
 24     _ = n! := by
 25        simpa [hn’’]


                                                               17
                                     Submission and Formatting Instructions for ICML 2026

The second example illustrates a typical non-vanishing / well-definedness obligation produced by symbolic preprocessing:
from an arithmetic assumption n > m in N, the prover must show that a real denominator term (n − m + 1) is nonzero.


  Statement (Lean goal).

    1   import Mathlib
    2
    3   open Real Nat Finset BigOperators Polynomial
    4
    5 set_option maxHeartbeats 8000000000
    6 theorem hwz (n m : N) (htotalNumidx : n > m) :
    7   ((↑n - ↑m + 1) : R) ̸= 0 := by
    8   -- to be completed


  Proof / Model Output.
  Problem. Given natural numbers n, m with n > m, prove the real expression

                                                         (n − m + 1) ̸= 0.

  Key observations.

    1. From n > m we get m < n + 1 in N immediately. This is a cleaner arithmetic target than reasoning directly about a casted
       subtraction in R.

    2. If we can show (m : R) < (n + 1 : R), then

                                             (n − m + 1 : R) = (n + 1 : R) − (m : R) > 0,

        hence it cannot be zero (discharged by linarith).

    3. The bridge between the N-inequality and the R-inequality is handled by norm cast. The remaining linear arithmetic on
       naturals is solved by omega.

  Proof plan.

        1. Reduce the non-vanishing goal to a positivity/inequality statement: it suffices to prove (m : R) < (n + 1 : R), then
           conclude by linarith.

        2. Use norm cast to turn (m : R) < (n + 1 : R) into the natural-number inequality m < n + 1.

        3. Prove m < n + 1 from the hypothesis n > m using omega.


  Complete Lean 4 Proof.

    1   import Mathlib
    2
    3   open Real Nat Finset BigOperators Polynomial
    4
    5 set_option maxHeartbeats 8000000000
    6 theorem hwz (n m : N) (htotalNumidx : n > m) :
    7   ((↑n - ↑m + 1) : R) ̸= 0 := by
    8   -- Reduce to a strict inequality in R, then finish by linear arithmetic.
    9   suffices h : (m : R) < (n + 1 : R) by
   10     linarith
   11   -- Move the goal back to N.
   12   norm_cast
   13   -- Discharge the N inequality from n > m.
   14   omega




                                                                18
                                      Submission and Formatting Instructions for ICML 2026

D.2. Qualitative examples of WZ-Prover outputs
We conclude this section with representative WZ-Prover outputs, illustrating the two complementary roles played by the
trained prover in our framework.



Prompting protocol. WZ-Prover is queried with a fixed instruction-following prompt that asks the model to (i) first write
a brief proof plan, and (ii) then output a complete Lean 4 proof script. Concretely, we use the following prompt template,
where ts is a placeholder for the current Lean proof state (the program replaces ts with the target theorem statement and
its surrounding Lean context before inference):



  Prompt template (ts is replaced at runtime).
  Complete the following Lean 4 code:
  “‘lean4 ts“‘
  Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps
  and strategies. The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the
  final formal proof.




Using this prompt, we show qualitative examples of the resulting model outputs. These examples illustrate the two
complementary roles played by the trained prover in our framework.



  Two output modes.

     • (A) Sketch-induced lemmas (symbolic-guided). When the symbolic backend succeeds, a WZ sketch decomposes the original
       identity into many short Lean-checkable obligations. Among the most frequent are: (i) term-ratio recurrences (used to
       verify the WZ invariant and telescoping), and (ii) non-vanishing denominator goals (well-definedness conditions required by
       field simp and normalization).
     • (B) Direct end-to-end proofs (symbolic-free). For WZ-inapplicable identities or when decomposition fails, WZ-Prover
       attempts to prove the identity directly in Lean, without relying on the symbolic sketch.




(A) Example: a sketch-induced lemma. The following are typical lemma forms produced by symbolic decomposition.
They are short, local, and appear repeatedly across WZ-style proof chains.



  (A1) Term-ratio recurrence (for simplification).

    1   import Mathlib
    2   open Real Nat Finset BigOperators
    3
    4 set_option maxHeartbeats 8000000000
    5 theorem rwz (n x : N) (hby_cases : x ≥ n) :
    6     ((-1) ˆ (n+1) : R) = ((-1) ˆ n) * (-1) := by
    7   -- typical local rewrite lemma used in ratio simplification
    8   simpa [pow_succ] using (pow_succ (-1 : R) n)




                                                                   19
                                  Submission and Formatting Instructions for ICML 2026


  (A2) Non-vanishing denominator (for field simp).

    1   import Mathlib
    2   open Real Nat Finset BigOperators
    3
    4 set_option maxHeartbeats 8000000000
    5 theorem hwz (n m : N) (h : n > m) : ((↑n - ↑m + 1) : R) ̸= 0 := by
    6   -- typical well-definedness obligation: denominator minimal factor ̸= 0
    7   have : (0 : R) < (↑n - ↑m + 1) := by
    8     have : (m : R) < (n + 1 : R) := by
    9       norm_cast; omega
   10     linarith
   11   linarith




(B) Example: a direct identity proof (symbolic-free). In contrast, the next example is an end-to-end identity proof
generated by WZ-Prover without invoking WZ decomposition. It showcases a “global” proof that relies on Mathlib’s
analytic lemmas rather than sketch-induced local obligations.


    1   import Mathlib
    2   open Nat BigOperators
    3
    4 theorem idt_149 (n : N) {x : R} (hx : 0 ≤ x ∧ x < 1) :
    5     (1 - x) ˆ (-(n + 1 : N) : R) = Σ’ k : N, (n + k).choose k * x ˆ k := by
    6   have hx_abs : |x| < 1 := by
    7     have : -1 < x ∧ x < 1 := by
    8       constructor
    9       · linarith [hx.1]
   10       · exact hx.2
   11     simpa [abs_lt] using this
   12
   13     rw [neg_eq_neg_one_mul, Real.rpow_mul, Real.rpow_neg_one, inv_eq_one_div]
   14     norm_cast
   15     rw [Real.rpow_natCast, one_pow, div_eq_mul_inv]
   16     -- main analytic lemma (name may vary slightly across Mathlib versions)
   17     simpa using (tsum_choose_mul_geometric_of_abs_lt_1 (n := n) hx_abs)



Together, (A) and (B) reflect the intended complementarity: symbolic decomposition turns long identities into many short
obligations that WZ-Prover can discharge reliably, while direct proving covers WZ-inapplicable identities without requiring
a symbolic sketch.

E. Case Studies
We present two complementary case studies to illustrate how WZ-LLM operates in practice. Appendix E.1 focuses on
the symbolic proof sketch produced by our framework, highlighting how symbolic computation induces a clear, executable
global proof plan. Appendix E.2 then demonstrates how this sketch is instantiated into a complete end-to-end Lean4 proof
through a single interactive command, showcasing the full automation pipeline of WZ-LLM (Algorithm 1).

E.1. From a Proof Sketch Template to Structured Obligations
This case study illustrates how WZ-LLM bridges symbolic proof planning and verifier-checked formal reasoning in Lean4.
Given a target combinatorial identity, the framework first constructs a high-level WZ proof sketch template following the
standard Wilf–Zeilberger reasoning pattern: normalization, recurrence/telescoping, and boundary-condition discharge.
Rather than attempting unconstrained end-to-end proof search, this sketch explicitly exposes the global proof structure and
reduces the original goal to a small set of well-scoped, Lean-checkable proof obligations.

                                                            20
                                 Submission and Formatting Instructions for ICML 2026

The template below summarizes the canonical structure of a WZ-style proof sketch generated by WZ-LLM. Each step
corresponds to a distinct class of obligations that can be independently verified in Lean, allowing scalable and modular
formalization.




                                                          21
                                     Submission and Formatting Instructions for ICML 2026

   WZ Proof Sketch Template in Lean 4

   Annotation convention. Subgoals delegated to WZ-Prover are marked as [LLM task: non-vanishing & ratio
   lemmas]. These obligations typically establish well-definedness conditions (nonzero denominators required by field simp)
   and verify CAS-derived term-ratio identities used in recurrence checking.

     1   theorem <IdentityName> (n : N) (hn : <premises>) :
     2    (Σ k in Finset.range (n + 1), A n k) = B n := by

   Step 1: WZ certificate synthesis (CAS).
   Obtain a rational WZ certificate R(n, k) from a symbolic backend (e.g., Sage).

     1   let R : N → N → R := WZ Certificate from CAS

   Step 2: Side conditions (well-definedness and boundaries).
   Prove non-vanishing conditions required for normalization and algebraic rewriting.

     1 have ne_zeroA : ∀ n k, k < n → (A n k : R) ̸= 0 := by
     2 -- [LLM task: non-vanishing \& ratio lemmas]}
     3 have ne_zeroB : ∀ n, (B n : R) ̸= 0 := by
     4 -- [LLM task: non-vanishing \& ratio lemmas]}

                                     P                                           P
   Step 3: Normalization. Reduce         A(n, k) = B(n) to the canonical form        F (n, k) = 1 using a fixed lemma.


     1 have WZ_aux (n : N) (f : N → N → R) (B : N → R)
     2 (ne_zero : ∀ n, (B n : R) ̸= 0) :
     3 (Σ k in Finset.range (n+1), (f n k / B n : R) = 1)
     4    ↔ (Σ k in Finset.range (n+1), f n k = B n) := by
     5 -- fixed normalization lemma}


   Step 4: CAS-assisted ratio lemmas.
   Precompute quotient identities to simplify recurrence checking in Lean.

     1 have ratio_k : ∀ n k, k < n → A n (k+1)/A n k = <CAS_ratio_k> := by
     2 -- [LLM task: non-vanishing \& ratio lemmas]}
     3 have ratio_n : ∀ n k, k < n → A (n+1) k/A n k = <CAS_ratio_n> := by
     4 -- [LLM task: non-vanishing \& ratio lemmas]}
     5 have ratio_B : ∀ n, B (n+1)/B n = <CAS_ratio_B> := by
     6 -- [LLM task: non-vanishing \& ratio lemmas]}


   Step 5: WZ invariant.
   Verify the core WZ relation F (n+1, k) − F (n, k) = G(n, k+1) − G(n, k).

     1 let F := fun n k => A n k / B n
     2 let G := fun n k => R n k * F n k
     3 have WZ_invariant : ∀ n k, k < n →
     4 F (n+1) k - F n k = G n (k+1) - G n k := by
     5 -- [LLM task: non-vanishing \& ratio lemmas]}


   Step 6: Telescoping and boundary discharge.
   Sum the invariant over k to obtain f (n + 1) − f (n) = 0.

     1 let f := fun n => Σ k in Finset.range (n+1), F n k
     2 have telescoping_step : ∀ n, f (n+1) - f n = 0 := by
     3 -- [LLM task: non-vanishing \& ratio lemmas]}


   Step 7: Constant extraction and unnormalization.
   Prove the base case, conclude f (n) = 1, and recover the original identity.


This template makes explicit which parts of the proof are handled symbolically, which reduce to algebraic side conditions,

                                                                  22
                                     Submission and Formatting Instructions for ICML 2026

and which require Lean-level reasoning. Crucially, many boundary and non-vanishing conditions that are traditionally
discharged manually in proof assistants are surfaced as explicit obligations and automatically handled by WZ-Prover.

E.2. One-Command End-to-End Formal Proof in Lean
Beyond exposing a structured proof sketch, WZ-LLM is integrated into Lean as an interactive tactic. For a concrete identity
such as                                                 
                                                      k n      m           1
                                           X
                                                (−1)                 = m+n ,
                                                         k m+k             n
                                           k∈range(n+1)

the user only needs to invoke a single command:

                                                            wz prove

As illustrated in Figure 2, the Lean InfoView then automatically orchestrates the entire pipeline: it calls a symbolic engine
(Sage) to synthesize WZ certificates and recurrence relations, decomposes the goal into structured subgoals, and interacts
with WZ-Prover to generate Lean proof scripts for each obligation. Once the suggested proof is accepted in the InfoView,




Figure 2. Lean InfoView output of the wz prove tactic. The tactic automatically invokes symbolic computation and the trained prover to
generate Lean proof suggestions, which can be accepted to fill in the complete formal proof.

the complete proof is inserted into the Lean file, as shown in Listing 1, and verified by the kernel, yielding a fully checked
end-to-end formal proof with minimal user intervention.

                                                                 23
                          Submission and Formatting Instructions for ICML 2026


 1   import Mathlib
 2   open Real Nat Finset BigOperators Polynomial
 3
 4 set_option maxHeartbeats 8000000000
 5 theorem MichaelZ_052 (n m : N) {m : m ̸= 0} :
 6     Σ k ∈ Finset.range (n + 1),
 7         (-1 : R) ˆ k * (Nat.choose n k) * (m / (m + k))
 8       = 1 / (Nat.choose (m + n) n : R) := by
 9
10      --------------------------------------------------------------------
11      -- (0) WZ-style normalization: define summand A(n,k), target B(n),
12      --     normalized term F(n,k) := A(n,k)/B(n), and sum f(n)=ΣF(n,k).
13      --     Also define a certificate R(n,k) and its companion G(n,k)=R*F.
14      --------------------------------------------------------------------
15      let A : N → N → R := fun (n k : N) =>
16          ((-1) ˆ k * ↑(n.choose k) * (↑m / (↑m + ↑k)) : R)
17      let B : N → R := fun n : N => (1 / ↑((m + n).choose n) : R)
18      let F : N → N → R := fun n k => (A n k / B n)
19      let f : N → R := fun n => Σ k ∈ Finset.range (n+1), F n k
20
21      -- WZ certificate (precomputed by symbolic backend in the full system)
22      let R : N → N → R := fun n k => (-(k + m)*k/((n - k + 1)*(n + 1)) : R)
23      let G : N → N → R:= fun (n k : N) => R n k * F n k
24
25      --------------------------------------------------------------------
26      -- (1) Non-vanishing side conditions: needed for field_simp/division.
27      --      These are typical well-definedness lemmas in WZ pipelines.
28      --------------------------------------------------------------------
29      have ne_zeroA : ∀ n k : N, k < n → (A n k : R) ̸= 0 := by
30        intro n k htotalNumidx
31        simp [A]
32        -- choose n k ̸= 0 when k ≤ n (here k < n)
33        have h1 : ¬n.choose k = 0 := by
34          suffices h : 0 < (choose n k) by linarith
35          have h_le : k ≤ n := by omega
36          exact Nat.choose_pos h_le
37        -- m ̸= 0 (from implicit parameter), plus denominator m+k ̸= 0
38        have h2 : ¬m = 0 := by omega
39        have h3 : ¬(m : R)+ (k : R)= 0 := by norm_cast; omega
40        aesop
41      have ne_zeroB : ∀ n : N, (B n : R) ̸= 0 := by
42        intro n
43        simp [B]
44        -- choose (m+n) n ̸= 0 since n ≤ m+n
45        have h1 : ¬(m + n).choose n = 0 := by
46          suffices h : 0 < (choose (m + n) n) by linarith
47          have h1 : n ≤ m + n := by omega
48          exact Nat.choose_pos h1
49        aesop
50      have ne_zeroB_succ : ∀ n : N, (B (n + 1) : R) ̸= 0 := by
51        intro n
52        simp [B]
53        aesop
54      have ne_zeroB’: ∀ n : N, (B n : R) * (B (n + 1) : R) ̸= 0 := by
55        intro m
56        rw [mul_ne_zero_iff]
57        exact And.intro (ne_zeroB m) (ne_zeroB (m + 1))
58      have ne_zeroAB’ : ∀ n k : N, k < n → (B n : R) * (A n k : R) ̸= 0 := by
59        intro n k hidx
60        rw [mul_ne_zero_iff]
61        exact And.intro (ne_zeroB n) (ne_zeroA n k hidx)
62
63      --------------------------------------------------------------------
64      -- (2) Algebraic factoring helpers: isolate ratios like


                                                  24
                        Submission and Formatting Instructions for ICML 2026

 65   --     A(n+1,k)/A(n,k) and B(n+1)/B(n) after field_simp.
 66   --     These are bookkeeping lemmas that keep later steps readable.
 67   --------------------------------------------------------------------
 68   have l1 : ∀ n k : N, k < n
 69       → A (n + 1) k * B n / (B n * A n k) = A (n + 1) k / A n k := by
 70     intro n k hidx
 71     field_simp [ne_zeroA, ne_zeroB]
 72
 73   have l2 : ∀ n k : N, k < n
 74       → B (n + 1) * A n k / (B n * A n k) =           B (n + 1) / B n := by
 75     intro n k hidx
 76     field_simp [ne_zeroA, ne_zeroB]
 77
 78   have r1 : ∀ n k : N, k < n → B (n + 1) * (R n (k + 1) * A n (k + 1))
 79       / (B n * A n k) = R n (k + 1) * (A n (k + 1) / A n k) * (B (n + 1) / B n)
      := by
 80     intro n k hidx
 81     field_simp [ne_zeroA, ne_zeroB]
 82
 83   have r2 : ∀ n k : N, k < n → B (n + 1) * (A n k * R n k)
 84       / (B n * A n k) = R n k * (B (n + 1) / B n) := by
 85     intro n k hidx
 86     field_simp [ne_zeroA, ne_zeroB]
 87
 88   --------------------------------------------------------------------
 89   -- (3) WZ normalization lemma: sum (A/B) = 1 ←> sum A = B.
 90   --      This bridges the normalized constant-sum formulation back to
 91   --      the original target identity at the very end.
 92   --------------------------------------------------------------------
 93   have WZ_aux (n : N) (f : N → N → R) (B : N → R)
 94        (ne_zero : ∀ n : N, (B n : R) ̸= 0) :
 95        Σ k ∈ Finset.range (n+1), (f n k / B n : R) = (1 : R)
 96        ↔ Σ k ∈ Finset.range (n+1), f n k = B n := by
 97     constructor
 98     · intro h
 99        rw [← Finset.sum_div, div_eq_iff (ne_zero n), one_mul] at h
100        norm_cast at h
101     · intro _
102        rw [← Finset.sum_div, div_eq_iff (ne_zero n), one_mul]
103        norm_cast
104
105   have Step1 := WZ_aux n A B ne_zeroB
106
107   --------------------------------------------------------------------
108   -- (4) Symbolic (ratio) facts used by the WZ identity:
109   --     aux1 : k-shift ratio  A(n,k+1)/A(n,k)
110   --     aux2 : n-shift ratio  A(n+1,k)/A(n,k)
111   --     aux3 : target ratio   B(n+1)/B(n)
112   --     These are exactly the kind of lemmas that a CAS-backed stage
113   --     tends to generate in bulk for many problems.
114   --------------------------------------------------------------------
115   have aux1 (n k : N) (htotalNumidx : k < n):
116       A n (k + 1) / A n k = -(n - k)*(k + m)/((k + m + 1)*(k + 1)) := by
117     simp only [A]
118     -- (-1)ˆ(k+1) = (-1)ˆk * (-1)
119     have r1 : ((-1) ˆ (k + 1) : R) = ((-1) ˆ k) * (-1) := by
120       rw [pow_succ]
121     rw [r1]
122     -- choose ratio: C(n,k+1) expressed from C(n,k)
123     have r2 : (↑(n.choose (k + 1)) : R) = (↑(n.choose k)) * (n - k)/(k + 1) := by
124       have h1 : n ≥ k := by omega
125       have h2 : (k + 1 : R) ̸= 0 := by linarith
126       field_simp
127       norm_cast
128       simp [Nat.choose_succ_right_eq]

                                                25
                        Submission and Formatting Instructions for ICML 2026

129     rw [r2]
130     -- side conditions for field_simp
131     have h1 : (↑(n.choose k) : R) ̸= 0 := by
132       norm_cast
133       suffices h : 0 < (n.choose k) by exact h.ne’
134       apply Nat.choose_pos
135       omega
136     have h2 : ((↑m + ↑(k + 1)) : R) ̸= 0 := by norm_cast; omega
137     have h3 : ((↑m + ↑k) : R) ̸= 0 := by norm_cast; omega
138     have h4 : (((-1) ˆ k) : R) ̸= 0 := by norm_num
139     have h5 : ((↑k + 1) : R) ̸= 0 := by norm_cast
140     have h6 : (↑m : R) ̸= 0 := by norm_cast
141     have h7 : ((↑k + ↑m + 1) : R) ̸= 0 := by norm_cast
142     field_simp
143     grind
144
145   have aux2 (n k : N) (htotalNumidx : k < n):
146       A (n + 1) k / A n k = (n + 1)/(n - k + 1) := by
147     simp only [A]
148     -- choose lifting: C(n+1,k) expressed from C(n,k)
149     have r1 : (↑((n + 1).choose k) : R) = (↑(n.choose k)) * (n + 1)/(n - k + 1)
      := by
150       have h1 : n ≥ k := by omega
151       have h2 : (↑n - ↑k + 1 : R) ̸= 0 := by norm_cast
152       field_simp
153       norm_cast
154       simp [Nat.choose_mul_succ_eq]
155       omega
156     rw [r1]
157     -- side conditions for field_simp
158     have h1 : (↑(n.choose k) : R) ̸= 0 := by
159       norm_cast
160       suffices h : 0 < (n.choose k) by exact h.ne’
161       apply Nat.choose_pos
162       omega
163     have h2 : ((↑m + ↑k) : R) ̸= 0 := by norm_cast; omega
164     have h3 : (((-1) ˆ k) : R) ̸= 0 := by norm_num
165     have h4 : (↑m : R) ̸= 0 := by norm_cast
166     have h5 : ((↑n - ↑k + 1) : R) ̸= 0 := by
167       suffices 0 < (↑n - ↑k + 1 : R) by linarith
168       simp only [sub_eq_add_neg, add_assoc]
169       norm_cast
170       omega
171     field_simp
172
173   have aux3 : ∀ n : N, B (n + 1) / B n = (n + 1)/(n + m + 1) := by
174     intro n
175     simp only [B]
176     -- ratio of binomial coefficients in B(n)=1/choose(m+n,n)
177     have r1 : (↑((m + (n + 1)).choose (n + 1)) : R)
178           = (↑((m + n).choose n)) * (n + m + 1)/(n + 1) := by
179       have h1 : (n + 1 : R) ̸= 0 := by linarith
180       field_simp
181       norm_cast
182       have h2 : (m + (n + 1)).choose (n + 1) * (n + 1)
183             = (m + n + 1).choose (n + 1) * (n + 1) := by
184         have h21 : m + (n + 1) = m + n + 1 := by omega
185         rw [h21 ]
186       have h2 ’ : (m + n).choose n * (n + m + 1)
187             = (m + n).choose n * (m + n + 1) := by
188         have h2 ’1 : n + m + 1 = m + n + 1 := by omega
189         rw [h2 ’1 ]
190       simp [h2 , h2 ’, Nat.choose_succ_right_eq, Nat.choose_mul_succ_eq]
191     rw [r1]
192     -- side conditions

                                                26
                        Submission and Formatting Instructions for ICML 2026

193     have h1 : ((↑n + ↑m + 1) : R) ̸= 0 := by norm_cast
194     have h2 : (1 : R) ̸= 0 := by norm_num
195     have h3 : ((↑n + 1) : R) ̸= 0 := by norm_cast
196     have h4 : (↑((m + n).choose n) : R) ̸= 0 := by
197       norm_cast
198       push_neg
199       rw [← Nat.pos_iff_ne_zero]
200       apply Nat.choose_pos
201       linarith
202     field_simp
203
204   -- boundary helpers that appear in the telescoping boundary terms
205   have r_aux1 : ∀ n : N, A (n + 1) (n+1) = ((-1)*(m + n) / (m + n + 1)) * A n n
      := by
206     intro n
207     simp only [A]
208     field_simp
209     have r1 : ((-1) ˆ (n + 1) : R) = ((-1) ˆ n) * (-1) := by rw [pow_succ]
210     rw [r1]
211     norm_num
212     grind
213
214   have r_aux2 : ∀ n : N, A (n + 1) n = (n + 1) * A n n := by
215     intro n
216     simp only [A]
217     field_simp
218     norm_num
219
220   --------------------------------------------------------------------
221   -- (5) Core WZ step: show f(n+1) - f(n) = 0, by telescoping:
222   --     F(n+1,k) - F(n,k) = G(n,k+1) - G(n,k)
223   --     Sum over k collapses to boundary terms, which cancel.
224   --------------------------------------------------------------------
225   have Step2 : ∀ n : N, f (n + 1) - f n = 0 := by
226     intro n
227
228     -- pointwise WZ identity for each k (local recurrence + certificate)
229     have WZ (k : N) (htotalNumidx:k < n) :
230         F (n + 1) k - F n k = G n (k + 1) - G n k := by
231       simp only [F, G]
232       -- normalize differences under common denominators
233       field_simp [ne_zeroA, ne_zeroB]
234       rw [← div_left_inj’ (ne_zeroAB’ n k (by omega))]
235       rw [sub_div, mul_sub, sub_div ]
236       -- split into ratios A(n+1,k)/A(n,k) and B(n+1)/B(n)
237       rw [l1 n k (by omega), l2 n k (by omega), r1 n k (by omega), r2 n k (by
      omega)]
238       -- insert the explicit symbolic ratios aux1 /aux2 /aux3
239       rw [sub_eq_iff_eq_add, ← sub_mul]
240       nth_rw 2 [show B (n + 1) / B n = 1 * (B (n + 1) / B n) by grind]
241       rw [← add_mul]
242       simp [R]
243       rw [aux1 n k (by linarith), aux2 n k (by linarith), aux3 n]
244       -- finish by algebraic simplification (denominators shown nonzero)
245       field_simp
246       have h1 : ((↑n - (↑k + 1) + 1) : R) ̸= 0 := by
247         suffices h : k < (n : R) by linarith
248         norm_cast
249       have h2 : ((↑k + 1) : R) ̸= 0 := by norm_cast
250       have h3 : ((↑n - ↑k + 1) : R) ̸= 0 := by
251         suffices h : k < (n + 1 : R) by linarith
252         norm_cast
253         omega
254       have h4 : ((↑k + ↑m + 1) : R) ̸= 0 := by norm_cast
255       have h5 : ((↑n + 1) : R) ̸= 0 := by norm_cast

                                                27
                             Submission and Formatting Instructions for ICML 2026

256       field_simp
257       ring
258
259     -- sum the pointwise WZ identity over k and telescope G(n,·)
260     calc f (n + 1) - f n
261       _ = (Σ k ∈ range (n+1), (F (n + 1) k - F n k)) + F (n + 1) (n+1) := by
262         simp [f]
263         rw [Finset.sum_range_add]
264         simp only [range_one, sum_singleton, add_zero, sub_add_eq_add_sub]
265       _ = (Σ k ∈ range n, (G n (k + 1) - G n k)) + F (n + 1) n - F n n + F (n +
      1) (n+1) := by
266         rw [Finset.sum_range_add]
267         simp only [range_one, sum_singleton, add_zero, add_left_inj, add_sub]
268         congr 2
269         apply Finset.sum_congr rfl
270         intro k hidx
271         simp only [mem_range] at hidx
272         exact WZ k hidx
273       _ = (G n n - G n 0) + F (n + 1) n - F n n + F (n + 1) (n+1) := by
274         -- telescoping: Σ (G(k+1)-G(k)) = G(n)-G(0)
275         congr 3
276         apply sum_range_sub
277
278     -- discharge boundary terms and show total difference is zero
279     simp [G, F]
280     field_simp [ne_zeroB n, ne_zeroB_succ n, ne_zeroB’ n]
281     simp [mul_comm (B n)]
282     rw [add_sub_right_comm, ← sub_mul, add_assoc, ← add_mul]
283     nth_rw 1 [show B (n + 1) = (B (n + 1) / B n) * B n by field_simp [ne_zeroB]]
284     conv_lhs => enter[1];rw[← mul_assoc]
285     rw [← add_mul]
286     simp only [_root_.mul_eq_zero]
287     left
288     rw [sub_right_comm,← sub_one_mul,aux3 n, r_aux1 n, r_aux2 n]
289     simp only [A, R]
290     field_simp
291     norm_num
292     grind
293
294   --------------------------------------------------------------------
295   -- (6) Conclude f(n) is constant (=1) by Step2 and base case f(0)=1.
296   --------------------------------------------------------------------
297   have Step3 : ∀ n : N, f n = 1 := by
298     intro n
299     induction’ n with n hm
300     · -- base case: f(0)=F(0,0)=A(0,0)/B(0)=1
301        simp [f, F, A, B]
302        have h1 : (↑m : R) ̸= 0 := by norm_cast
303        field_simp
304     · -- inductive step: f(n+1)=f(n) from Step2, then use IH
305        exact (sub_eq_zero.1 $ Step2 n).trans (hm)
306
307   --------------------------------------------------------------------
308   -- (7) Unnormalize back to the original statement: Σ A = B.
309   --------------------------------------------------------------------
310   unfold A B at Step1
311   rw [Step1.1]
312   exact Step3 n

         Listing 1. Complete Lean4 proof of the combinatorial identity M ichaelZ 052 generated by WZ-LLM.




                                                       28
