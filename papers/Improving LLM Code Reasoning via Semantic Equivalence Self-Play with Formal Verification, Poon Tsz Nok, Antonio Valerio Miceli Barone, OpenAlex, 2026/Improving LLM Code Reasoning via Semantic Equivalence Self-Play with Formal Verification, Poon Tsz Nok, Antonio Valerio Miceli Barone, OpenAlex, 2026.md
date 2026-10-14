                                        Improving LLM Code Reasoning via Semantic Equivalence Self-Play with
                                                              Formal Verification

                                                            Poon Tsz Nok                           Antonio Valerio Miceli Barone
                                                         School of Informatics                         School of Informatics
                                                        University of Edinburgh                       University of Edinburgh
                                                        trevorpoon@gmail.com                            antonio@ed.ac.uk



                                                             Abstract                           properties and edge cases. To bridge this gap, we
                                            We introduce a self-play framework for se-          ground our framework in Haskell for three key rea-
arXiv:2604.17010v2 [cs.CL] 3 May 2026




                                            mantic equivalence in Haskell, utilizing for-       sons. First, its pure functional nature and strong
                                            mal verification to guide adversarial training      static typing eliminate hidden state and side ef-
                                            between a generator and an evaluator. The           fects (Thompson, 2011) (See Appendix A for illus-
                                            framework leverages Liquid Haskell proofs           tration), making equivalence reasoning mathemati-
                                            for validating equivalence and execution-based      cally tractable (Launchbury, 1993; Sestoft, 1997).
                                            counterexamples for inequivalence, organized        Second, the Liquid Haskell ecosystem enables the
                                            via a difficulty-aware curriculum. To facili-
                                                                                                generation of machine-checkable proofs via refine-
                                            tate this, we release OpInstruct-HSx, a syn-
                                            thetic dataset of ≈28k validated Haskell pro-       ment types, making it possible to certify semantic
                                            grams. Empirical experiments show that our          equivalence for a subset of Haskell programs (Liq-
                                            evaluator transfers effectively to downstream       uid Haskell Tutorial, 2025). This offers a source of
                                            tasks, achieving up to 13.3pp accuracy gain on      formal supervision that is unavailable in languages
                                            EquiBench and consistent gains on PySecDB.          such as Python or Java, where formal verification
                                            Ablation studies on the SEQ-SINQ regimes            is much harder. Finally, training on underrepre-
                                            indicate that while inequivalence supervision
                                                                                                sented functional paradigms pushes the model be-
                                            provides data volume, equivalence proofs are
                                            uniquely responsible for the model’s reasoning      yond standard object-oriented patterns (van Dam
                                            capabilities. The entire training pipeline and      et al., 2024; Giagnorio et al., 2025), encouraging
                                            dataset are publicly released on GitHub and         deeper abstraction capabilities.
                                            Hugging Face respectively.                             We propose a self-play framework for semantic
                                                                                                equivalence, in which two specialized agents in-
                                        1   Introduction
                                                                                                teract: Alice, a generator that produces variants of
                                        The rise of large language models (LLMs) has            reference programs; and Bob, an evaluator trained
                                        reshaped how software can be generated and              to decide whether two programs are equivalent.
                                        maintained. Despite models such as Codex and            The self-play loop alternates between program gen-
                                        Qwen2.5-coder have demonstrated strong capabili-        eration, verification through proofs or counterex-
                                        ties in producing functional code from natural lan-     amples, difficulty scoring, and fine-tuning of both
                                        guage prompts (Murphy et al., 2024; Hui et al.,         agents. By framing the problem as a game between
                                        2024), their outputs often fail to preserve the in-     generator and evaluator, the system encourages pro-
                                        tended program behavior beyond basic test cov-          gressively harder examples and deeper reasoning
                                        erage (Laneve et al., 2025; Nguyen et al., 2025;        about semantics.
                                        Wei et al., 2025). This gap raises a fundamental           This work investigates three core questions re-
                                        challenge: How can we design training that ex-          garding the utility of functional programming for
                                        plicitly teaches models to reason about semantic        LLM alignment. First, we examine the dynamics
                                        equivalence between programs? Addressing this           of self-play, asking whether an adversarial loop in
                                        problem is critical not only for reliable code gener-   a functional language can induce a progressive cur-
                                        ation but also for downstream applications such as      riculum that improves semantic reasoning. Second,
                                        program optimization, automated refactoring, and        we evaluate cross-domain and cross-language trans-
                                        vulnerability detection.                                ferability, assessing whether semantic reasoning
                                           Current approaches largely rely on test suites,      skills acquired in Haskell generalize to zero-shot
                                        which are insufficient for capturing deep semantic      synthesis and vulnerability detection in broader
coding benchmarks. Finally, we perform a con-           In the coding domain, recent frameworks such
trolled ablation to determine the relative contri-      as Sol-Ver (Lin et al., 2025) and AutoIF (Dong
butions of supervision signals, distinguishing be-      et al., 2025) adapt this by using model-generated
tween the effects of formal equivalence proofs and      unit tests and execution feedback to filter synthetic
execution-based counterexamples on evaluator ro-        data, achieving significant gains on benchmarks
bustness.                                               like MBPP and IFEval.
                                                           Our work is most directly built upon the ad-
2   Related Work                                        versarial framework proposed by Miceli-Barone
                                                        et al. (2025), known as the Semantic Inequivalence
Determining semantic equivalence is extremely           Game (SINQ). In their setup, a generator ("Al-
challenging in general and current LLMs often fail      ice") creates program variants and diverging inputs
to recognise semantic equivalence in code (Laneve       (counterexamples), while an evaluator ("Bob") at-
et al., 2025; Nguyen et al., 2025; Wei et al., 2025).   tempts to detect inequivalence without seeing the
By Rice’s Theorem, determining if two arbitrary         generator’s justification. This adversarial loop pro-
programs are semantically equivalent is generally       vides a scalable curriculum that improves semantic
undecidable (Rice, 1953). Traditional approaches        reasoning. We extend this paradigm by including
rely on unit testing; however, even extended test       Semantic Equivalence tasks (SEQ). While Miceli-
suites, such as HumanEval+ and MBPP+ remain             Barone et al. (2025) focused exclusively on inequiv-
insufficient to guarantee correctness (Gren and         alence via execution feedback, we integrate formal
Antinyan, 2017; Chioteli et al., 2021). Similarly,      verification using Liquid Haskell. This allows us to
symbolic execution offers path-sensitive analysis       train on positive instances of equivalence supported
but suffers from combinatorial state-space explo-       by reasoning traces.
sion as program complexity increases (Badihi et al.,
2020).                                                  3     Methodology
   To address these incompleteness issues, recent
research has pivoted towards formal verification.       We introduce the core methodology of the self-play
In the LLM domain, frameworks like DeepSeek-            framework for improving code reasoning in LLMs
Prover (Xin et al., 2024a,b; Ren et al., 2025) and      through two complementary tasks: the SEQ and
Kimina-Prover (Wang et al., 2025) have demon-           the SINQ. In the SEQ task, the generator model is
strated that fine-tuning models on self-generated       asked to produce a functionally identical variant of
proofs (e.g., in Lean) significantly enhances their     a given Haskell program, along with a formal proof
verifiable reasoning capabilities. However, gener-      certifying its equivalence. In contrast, the SINQ
ating fully machine-checkable equivalence proofs        task requires generating a function that diverges
for imperative languages like Python or C++ is be-      from the original program on at least one input.
yond the reach of current tools except for trivial      Figure 1 shows the complete self-play framework,
cases (Miceli-Barone et al., 2025).                     with difficulty-based supervised fine-tuning that
                                                        guides the adaptive training loop.
   Our approach bridges this gap by using Haskell
and Liquid Haskell. Liquid Haskell embeds refine-       3.1    Framework Overview
ment types into the language (Vazou et al., 2014),
                                                        The self-play framework is formulated as a two-
allowing logical properties to be verified automat-
                                                        agent adversarial game between Alice (the genera-
ically via Satisfiability Modulo Theories (SMT)
                                                        tor) and Bob (the evaluator).
solvers (Diatchki, 2015; Jhala et al., 2020; Liq-
uid Haskell Tutorial, 2025). This framework en-             1. Each round starts with a reference Haskell pro-
ables the construction of machine-checkable lem-               gram P , upon which Alice’s task is to gener-
mas, using reflection and Proof by Logical Evalua-             ate program Q, which is either a semantically
tion (PLE), to formally certify pointwise equality             equivalent variant to P (with a proof) or a
between candidate functions. This provides a de-               semantically inequivalent program (with a di-
terministic, high-fidelity feedback signal for the             verging input that demonstrates their different
self-play loop.                                                behaviour).
   Self-play has historically driven breakthroughs
in game-playing agents like AlphaZero (Silver               2. The proof or the diverging input is verified
et al., 2017) and OpenAI Five (OpenAI et al., 2019).           afterwards, and if it fails, Alice loses.
             Phase 1: Dataset Preparation
                                                                                                                                           nvidia-OpenCodeInstruct dataset (Ahmad et al.,
                                                                                                                                           2025), a large-scale, high-quality instruction cor-
  Hugging Face        OpenCodeInstruct
                          Dataset
                                                      Pre-Filtering       Synthetic Code
                                                                          Generation for
                                                                                                 Compilation &
                                                                                                  Validation
                                                                                                                         OpInstruct-HSx
                                                                                                                                           pus originally built for Python code generation.
                                                                                                                            Dataset
                                                                             Haskell               Filtering


             Phase 2: Semantic Equivalence Self Play
                                                                                                                                              The programs are first pre-filtered and then
                                                                                                                                           transformed into Haskell programs using the
                      ob
                           =0
                             .5
                                       Semantic                    Alice Code &              Liquid               Bob Evaluations
                                                                                                                                           DeepSeek-R1-Distill-Llama-70B model. This
                    pr
                                      Equivalence                      Proof                 Haskell               and Difficulty

                 pr
                   ob
                      For each
                      reference
                     program (P)
                                      Game (SEQ)                    Generation             Verification             Estimation             process results in a synthetic dataset of Haskell
                        =0
   OpInstruct-HSx
      Dataset
                          .5
                                                                                                                                           programs. To ensure its quality, we applied an au-
                                       Semantic
                                     Inequivalence
                                                                   Alice Code &
                                                                  Diverging Input
                                                                                       Diverging Input
                                                                                         Execution
                                                                                                                    Candidate
                                                                                                                     Training
                                                                                                                                           tomated filtering and validation stage. For each
                                      Game (SINQ)                   Generation           Verification                  Data
                                                                                                                                           generated Haskell program, we extract the function
             Phase 3: LoRA Fine-tuning
                                                                                                                                           name and its argument types using syntactic heuris-
                                                                                                                                           tics, and synthesize a type-correct input using a
          Candidate
           Training
                                      Difficulty Score
                                       Biasing and
                                                                   Filtered
                                                                   Training
                                                                                        LoRA
                                                                                     Fine-tuning
                                                                                                           Alice Fine-tuned Adapter for
                                                                                                          Next Round Self-play Iteration
                                                                                                                                           recursive literal generator supporting common base
                                                                                                                                           types (e.g., Int, Bool, List, Tuple). Each pro-
             Data                        Sampling                    Data              on Alice


            Phase 4: Iterations with updated Alice adapters

                                                                                                                                           gram is compiled with Glasgow Haskell Compiler
                                   Repeat for



         Phase 2: Semantic
                                   N Iterations

                                                  Phase 3: LoRA               LoRA
                                                                                                   Intrinsic & Extrinsic Evaluation on
                                                                                                                                           (GHC) and executed on the synthesised input. Only
                                                   Fine-tuning        Fine-tuning on Bob
        Equivalence Self-Play                                                                            Alice and Bob Adapters
                                                     on Alice            in final round
                                                                                                                                           those that compile successfully and execute without
                                                                                                                                           errors are retained. This filtering process eliminates
Figure 1: Overview of the semantic self-play framework                                                                                     malformed or non-functional code, ensuring that
for improving code reasoning in LLMs via Haskell.                                                                                          the resulting dataset consists of minimally func-
                                                                                                                                           tional and executable Haskell programs.
                                                                                                                                              Figure 2 shows the entire multi-stage filtering
  3. Bob then decides whether (P, Q) are seman-
                                                                                                                                           mechanism. We have contributed OpInstruct-HSx,
     tically equivalent. If Bob’s judgment is accu-
                                                                                                                                           a clean and executable Haskell dataset for both
     rate, he wins and Alice loses, vice versa.
                                                                                                                                           SEQ and SINQ games, which consists of approxi-
   Alice’s objective is to create instances that are                                                                                       mately 28,000 validated Haskell functions derived
difficult for Bob to classify, whereas Bob’s task is                                                                                       from real-world problems. This dataset is made
to correctly assess them. Through repeated interac-                                                                                        publicly available2 , serving as a high-quality syn-
tions, both agents gradually improve their perfor-                                                                                         thetic Haskell resource for training LLMs in se-
mance. Miceli-Barone et al. (2025) have proved                                                                                             mantic reasoning tasks. The code to create the data
that this adversarial framework has no theoretical                                                                                         and replicate the experiment is released on a public
upper bound on model’s performance improve-                                                                                                repository3 .
ment, and in principle both agents can learn end-
                                                                                                                                                  Synthetic Haskell Dataset Generation -- OpInstruct-HSx

lessly about the complex programming logic while
training on a real-world coding dataset.                                                                                                     Hugging Face      OpenCodeInstruct         Pre-Filtering      Synthetic Code   Compilation &
                                                                                                                                                                   Dataset                                                                  OpInstruct-HSx
                                                                                                                                                                                                           Generation for    Validation
                                                                                                                                                                                                                                               Dataset
                                                                                                                                                                                                              Haskell         Filtering


3.2      Dataset Generation and Preparation
                                                                                                                                           Figure 2: Full Pipeline for the OpInstruct-HSx dataset
The availability of high-quality Haskell datasets                                                                                          generation
remains extremely limited. Among the few usable
resources, the most substantial one is the Blastwind
dataset1 , which aggregates real-world source files
                                                                                                                                           3.3       The Self-Play Loop: Alice and Bob
scraped from public GitHub repositories. However,
its utility is hindered by substantial noise: the data                                                                                     Step 1: Program Selection and Branching
contains unannotated, inconsistently formatted, and                                                                                        Let D be the dataset of reference Haskell programs.
often non-compilable code.                                                                                                                 We randomly choose a reference program P ∈ D
   To address the scarcity of high-quality Haskell                                                                                         and then select the SEQ game with 50% probability,
datasets, we adopt a complementary strategy: in-                                                                                           otherwise we choose the SINQ game.
troducing OpInstruct-HSx, where we generate
a synthetic Haskell dataset by adapting from the                                                                                              2
                                                                                                                                                https://huggingface.co/datasets/Trevor0501/
                                                                                                                                           OpInstruct-HSx
   1
    https://huggingface.co/datasets/blastwind/                                                                                                3
                                                                                                                                                https://github.com/TrevorPoon/
github-code-haskell-file                                                                                                                   llm-self-play-liquidhaskell
Step 2a: SEQ Game (Alice’s Turn)                        3.4     Implementation with Supervised
In the SEQ game, Alice receives P and must syn-                 Fine-Tuning with Difficulty Score
thesize Q such that for all inputs x:                   Given the practical challenges of reinforcement
                                                        learning (Appendix C), we instead adopt rejection
              ∀x ∈ X . P (x) = Q(x)                     sampling supervised fine-tuning (SFT). We con-
                                                        struct fine-tuning datasets by having Alice gener-
To challenge Bob, Alice is encouraged to construct      ate challenging programs and Bob learn from his
a hard instance Q, aiming for a maximum target          own correct identifications. This semi-adversarial
difficulty level (d=10, defined in Section 3.4.1).      pipeline ensures Alice continually refines her abil-
In addition, Alice is required to produce a formal      ity to craft borderline-difficult SEQ or SINQ pro-
proof (in Liquid Haskell) of this semantic equiva-      gram pairs, while Bob steadily improves at its rea-
lence. See Appendix B for an SEQ instance.              soning ability in semantic equivalence. Detailed
Step 2b: SINQ Game (Alice’s Turn)                       prompt formats for both agents are provided in
                                                        Appendix D.
Alternatively in the SINQ game, Alice is instructed
to produce a function Q that diverges from P on at      3.4.1    Alice’s Training Data Selection
least one input:
                                                        After Alice generates the candidate pairs (P, Q),
                                                        Alice’s outputs are not immediately used for fine-
           ∃x∗ ∈ X : P (x∗ ) ̸= Q(x∗ )
                                                        tuning. Instead, for each pair, Bob is asked to evalu-
Alice is also incentivized to construct a difficult     ate their semantic relation multiple times (typically
function Q that Bob is likely to misclassify, again     N = 10). The number of correct Bob responses
targeting a maximum difficulty level (d=10). Al-        Nsuccess determines the difficulty score dˆ as de-
ice must also output a diverging input xa showing       fined in Equation 1.
this inequivalence such that P (xa ) ̸= Q(xa ). See                                            
                                                                ˆ                      Nsuccess
Appendix B for an SINQ instance.                                d = d(P, Q) = 10 × 1 −                    (1)
                                                                                         N
Step 3: Verification through Liquid Haskell or
Execution                                               However, most of Alice’s early generations are triv-
                                                        ial for Bob. Including all examples would flood
   • SEQ Game: Alice’s proof is verified by Liq-
                                                        the dataset with low-difficulty cases that Bob al-
     uid Haskell, which acts as an external oracle.
                                                        ready solves easily. Following the design in Miceli-
     If the proof is accepted, the proof is retained
                                                        Barone et al. (Miceli-Barone et al., 2025), we only
     as a fine-tuning example.
                                                        retain examples that are sufficiently challenging, as
                                                                                            ˆ Hence, shown
                                                        determined by the difficulty score d.
   • SINQ Game: The candidate xa is tested by an
     execution: If P (xa ) ̸= Q(xa ), the instance is   in Schema 2, we split all (P, Q) pairs into DHard
     accepted. Otherwise, the sample is discarded.      and DEasy , where τ is a chosen difficulty threshold
                                                        (e.g., τ = 5).
   All candidates undergo compilation, execution,
and formal verification checks. This ensures the                 DHard = {(P, Q) | d(P, Q) > τ } ,
                                                                                                          (2)
training data for both Alice and Bob remains high-               DEasy = {(P, Q) | d(P, Q) ≤ τ }
quality and executable.
                                                           Finally, Alice’s training dataset is comprised of
Step 4: Bob’s Turn – Difficulty Estimation              three SFT examples for each validated pairs (P, Q).
After Alice produces her candidate program Q,           The first example pairs the prompts and Alice’s
Bob is presented with both P and Q only and must        generation, and directly trains Alice to generate
decide whether the two programs are semantically        a challenging program Q, which helps improve
equivalent. To estimate the challenge posed by          Alice’s ability to craft precise SEQ or SINQ code
each example, Bob is sampled N times and the pro-       (Schema 3). SP and UP denote the system and
portion of correct responses from Bob is then used      user prompts conditioned on the reference program
to compute a difficulty score. Further details on the   P and a target difficulty d = 10. O represents the
difficulty-based curriculum and dataset sampling        model’s raw output, which includes the chain-of-
can be found in Section 3.4.                            thought followed by the generated program Q (and
the diverging input x in the case of SINQ).              4        Experimental Setup

     SEQ = SPeq           eq           eq               We use DeepSeek-R1-Distill-Qwen-7B as our
                 A , UPA (P, 10), OA
                                                  (3)    base model for both Alice and Bob. Fine-tuning is
    SINQ = SPinq           inq
                 A , UPA (P, 10), OA
                                          inq 
                                                         performed using LoRA adaptors. Please see Ap-
                                                         pendix E for more details.
   We then select every hard example plus 20% as
                                                            To investigate the distinct contributions of equiv-
many easy ones sampled round-robin across integer
                                                         alence versus inequivalence supervision, we con-
difficulty bins to maintain a balanced curriculum.
                                                         duct the main experiment (E0 ) alongside three con-
   The second example, designated as a “difficulty-
                                                         trolled ablations (E1 –E3 ). These regimes systemat-
prediction” instance, teaches Alice to self-assess
                                                         ically vary the game type probability and reference
the hardness of its own creations: by taking Al-
                                                         program budget (P ) to isolate the impact of SEQ
ice’s generated program Q along with the Diffi-
                                                         supervision under controlled data constraints. The
culty Prediction User Prompt and supervising on
                                      ˆ (Schema 4).      configurations are shown in Table 1.
the numeric label “Difficulty level:d"
The training dataset is also biased towards hard
                                                          Regime         SEQ/SINQ    P             Goal
examples, with easy examples comprising 50% of
                                                          E0 (Base)         50/50   500            Main
the subset. Alice learns to calibrate its difficulty      E1                0/100   500         Max Volume
estimates and ensures that its future generations are     E2                96/4    500        Balanced Yield
appropriately challenging.                                E3                0/100    40   Vol. Control (E3 ≈ E2 )

                                                             Table 1: Experimental regimes to test SEQ impact.
         SEQDP = SPeq       eq     ˆ
                                    
                   A,DP , UPA,DP , d
                                                  (4)
        SINQDP = SPinq , UPinq , dˆ
                                    
                        A,DP        A,DP                    The full codebase is available at the GitHub
                                                         repository4 to generate the dataset OpInstruct-HSx,
   The third example concerns all (P, Q) pairs in        reproduce the experiments and evaluate model per-
the SEQ that have been successfully proved. We           formance.
not only consider the generated candidate Q for
a given P , but also the complete reasoning trace        5        Results
and valid Liquid Haskell proof script from Alice
(Schema 5). These examples serve as supervised           The following evaluation results are structured to
training signals to help Alice internalize the proof     address the three research questions outlined in the
obligation π, corresponding to the refinement type       introduction.
∀x., P (x) = Q(x).                                       5.1       Intrinsic Evaluation
                                                         The goal of E0 is teaching Alice (the generator) to
              n
  SEQproof = SPeq           eq        eq          
                     A , UPA (P ), OA (P, Q, π)
                                   o                     generate increasingly challenging instances while
                    LH(P, Q) ⊢ π                         Bob (the evaluator) to improve at judging program
                                                         semantics.
                                                  (5)
                                                         5.1.1 Capability Assessment
  This three-part structure enables Alice to gen-
                                                         As shown in Figure 3, the mean difficulty rises
erate challenging variants, assess their difficulties,
                                                         from 0.50 to 1.18 by round 7, indicating that Al-
and internalize proof strategies.
                                                         ice is crafting harder instances for a constant Bob.
3.4.2   Bob’s Training Data Selection                    See Appendix H.1.1 for the difficulty trajectories
Bob’s training data is constructed from all of his       breakdown for both SEQ and SINQ games.
correct (P, Q) pairs’ evaluations. Each training ex-        In addition, we measure how much the evalua-
ample (Schema 6) consists of the original pair, the      tor model (Bob) improves after its first and only
system prompts, user prompts, and Bob’s response         training round in the semantic equivalence self-
OB . By sampling from a wide range of difficulties,      play. Challenge instances are generated by the final
Bob learns to reason and recognize both easy and         trained generator model, Alice from round 7, us-
subtle equivalence relations.                            ing source programs from the training split of the
                                                            https://github.com/TrevorPoon/
                                                              4

        EBob = SPB , UPB (P, Q), OB               (6)    llm-self-play-liquidhaskell
                                      Alice Mean Difficulty Score by Round (from Bob's Evaluation)
                   5
                                                         Mean difficulty      ±1 SD                                  further enhance his ability to analyse correct and
                   4
                                                                                                                     semantically meaningful code across other coding
                   3                                                                                                 paradigms, not just the functional ones.
      Difficulty




                   2

                                                                                                            1.18
                                                                                                                     5.3.1 EquiBench
                   1                                               0.87                              0.93
                                                  0.65                            0.66
                        0.50   0.50
                                                                                                                     The EquiBench (Wei et al., 2025) benchmark con-
                   0
                         1      2                  3                4              5                  6      7
                                                                  Round                                              sists of six data categories: DCE (C pairs with
                                                                                                                     dead/live code variations), x86-64 (identical assem-
Figure 3: Mean and standard deviation for the difficulty
                                                                                                                     bly sequences via superoptimization), and CUDA
scores for Alice’s generated instances from a fixed un-
trained Bob over 7 rounds.                                                                                           (equivalent kernels with different scheduling) form
                                                                                                                     the low-level systems group. The algorithmic
                                                                                                                     group uses Python pairs from competitive pro-
OpInstruct-HSx and from the unseen test split. The                                                                   gramming, featuring OJ_A (algorithmic refactors),
resulting accuracies, summarised in Table 2, show                                                                    OJ_V (variable renaming), and OJ_VA (combined
modest improvements on unseen data.                                                                                  algorithmic and variable changes).
                                                                                                                        In the zero-shot prompting evaluation, our fine-
                                                                              Accuracy (%)                           tuned Bob model shows clear gains over the base
 Benchmark                                                    Base                       Trained                 ∆   model in several dataset configurations.
 OpInstruct-HSx (Train)                                       87.57                      91.34              +3.77
                                                                                                                                                                       Comparison of Accuracy Across Datasets
 OpInstruct-HSx (Test)                                        88.24                      88.79              +0.55                100
                                                                                                                                                                                                                                          Model Type
                                                                                                                                                                                                                                                base
                                                                                                                                                                                                                                                finetuned

                                                                                                                                  80
Table 2: OpInstruct-HSx accuracy results comparing                                                                                                                                                            69.8%

the Base Model and Trained (Bob adapter) models.                                                                                  60           57.4%   55.8%   55.9%        55.1%                    56.5%
                                                                                                                      Accuracy




                                                                                                                                                                                          51.9%                               51.8%   51.7%
                                                                                                                                       50.2%                                                                                                        50.1%
                                                                                                                                                                                                                      48.0%

                                                                                                                                  40


5.2                    Extrinsic Evaluation
                                                                                                                                  20

Having validated the agents’ improvement within
the self-play loop, we now investigate whether this                                                                                0
                                                                                                                                           OJ_A            OJ_VA                    DCE                   OJ_V
                                                                                                                                                                                      Dataset Configuration
                                                                                                                                                                                                                         STOKE                TVM


training enhances the model’s understanding of
program semantics across different programming                                                                       Figure 4: Accuracy comparison between base and fine-
languages and domains.                                                                                               tuned Bob models across EquiBench dataset configura-
                                                                                                                     tions.
5.2.1 Haskell Program Generation
In MBPP and HumanEval from MultiPL-E (Cas-                                                                                                                             Comparison of F1 Score Across Datasets
                                                                                                                                 100
sano et al., 2022), both models’ compilation errors                                                                                                                                                                                       Model Type
                                                                                                                                                                                                                                                base
                                                                                                                                                                                                                                                finetuned

decrease substantially and Pass@1 improves on                                                                                     80


the Haskell tasks (shown in Table 3). Performance                                                                                                                                                             69.7%


                                                                                                                                  60
trajectories for Alice across self-play rounds are                                                                                                                          53.0%
                                                                                                                      F1 Score




                                                                                                                                               50.7%
                                                                                                                                                               47.5%                      47.7%      47.4%

provided in Appendix H.1.2 and H.1.3.                                                                                             40
                                                                                                                                                       44.2%                                                                          42.8%
                                                                                                                                                                                                                                                    38.3%
                                                                                                                                       34.3%

   The results indicate that semantic reasoning
                                                                                                                                  20                                                                                          18.3%
training transfers positively to Haskell code gener-
                                                                                                                                                                                                                      7.1%

ation performance and robustness for both agents.                                                                                  0
                                                                                                                                           OJ_A            OJ_VA                    DCE                   OJ_V           STOKE                TVM
                                                                                                                                                                                      Dataset Configuration
For Bob, the gains confirm that the semantic dis-
crimination skills learned during self-play can yield                                                                Figure 5: F1 score comparison between base and fine-
broader benefits in practical programming scenar-                                                                    tuned Bob models across EquiBench dataset configura-
ios. And for Alice, the improvements suggest that                                                                    tions.
training on high-quality, verifiable program trans-
formations in self-play can enhance downstream                                                                          From Figure 4 and Figure 5, the model transfers
synthesis accuracy and reduce compilation errors.                                                                    best to OJ_A and OJ_V because both categories
                                                                                                                     (algorithmic refactors and variable renaming re-
5.3                    Coding Related Tasks Evaluation                                                               spectively) align with Bob’s learned skill on detect-
We would like to investigate whether richer type                                                                     ing high-level behavioural divergence, resulting in
semantics learnt in the evaluator model Bob can                                                                      large gains in performance. OJ_VA’s performance
                                                 Pass@1 (%)                              Compilation Errors
 Benchmark           Agent              Base          Trained          ∆          Base        Trained          ∆
 HumanEval           Bob                17.7           26.4           +8.7         130          110           −20
 HumanEval           Alice              17.7           26.3           +8.6         130          104           −26
 MBPP                Bob                26.7           36.9           +10.2        250          203           −47
 MBPP                Alice              26.7           34.3           +7.6         250          218           −32

Table 3: HumanEval and MBPP results (zero-shot prompting in Haskell), comparing the Base Model (untrained)
and Trained models. Averages over 16 trials.


stays modest as the authors stated that it is harder                                        Scores (%)
than pure renaming and closer to the “non-local                  Metric         Base         Trained           ∆
structural” end.                                                                Model
   In contrast, DCE, STOKE, and TVM require                      Accuracy        48.8          50.5           +1.7
reasoning about low-level or non-functional seman-               Precision       45.0          45.7           +0.7
                                                                 Recall          51.1          41.7           −9.4
tics absent from our Haskell curriculum. This mis-               F1 Score        47.9          43.2           −4.7
match in language, abstraction level, and equiva-
lence definition explains the weaker or negligible              Table 5: CodeXGLUE defect detection results compar-
improvements on these tasks.                                    ing the Base Model and Trained (Bob adapter).

5.3.2 PySecDB
PySecDB is the first comprehensive dataset of                   are low-level memory issues that require track-
security-related commits in Python (Sun et al.,                 ing pointers, memory allocation, and data lay-
2023). In Table 4, our fine-tuned Bob model                     outs. However, Haskell is memory-safe, garbage-
achieves consistent improvements over the base                  collected, and doesn’t have manual frees or pointer
model across all evaluated metrics. The results                 arithmetic. Therefore, the trained model shows no
indicate that Bob’s Haskell semantic reasoning                  meaningful advantage over the base model on this
training transfers positively to Python vulnerability           task.
detection, improving in identification of security-
relevant code changes.                                          5.4   Controlled Comparison of SEQ–SINQ
                                                                      Regimes
                             Scores (%)
                                                                A critical finding from E0 is the asymmetry in num-
 Metric         Base          Trained           ∆
                Model
                                                                ber of validated programs between SINQ and SEQ
                                                                even under a uniform sampling policy in choos-
 Accuracy        67.6           68.8           +1.2
 Precision       48.0           49.7           +1.7             ing the game. In Figure 6, we have hundreds of
 Recall          55.1           59.2           +4.1             accepted SINQ instances per round, but very few
 F1 Score        51.3           54.0           +2.7             SEQ instances (single digits in most rounds). A
                                                                review of the output from the self-play shows that
Table 4: PySecDB vulnerability detection results com-
paring the Base Model and Trained (Bob adapter).                while Alice can readily produce SINQ pairs, the
                                                                small reasoning model often struggles to produce
                                                                Liquid Haskell proofs for SEQ, which drastically
5.3.3 CodeXGlue                                                 limits the number of compiled and verified SEQ
CodeXGLUE’s defect detection dataset (Zhou                      examples available for training. This imbalance
et al., 2019) is a curated collection of over 27,000            limits the diversity of program types in the training
C-language functions, each manually labeled to                  buffer, with the current SEQ+SINQ configuration
indicate whether it contains a security-relevant de-            heavily skewed with SINQ examples.
fect.                                                              This subsection investigates whether incorpo-
   In Table 5, both the base and fine-tuned Bob                 rating SEQ supervision yields unique reasoning
models perform near the 50% mark for accuracy,                  benefits beyond those of SINQ alone, aiming to
which is indistinguishable from a random model.                 isolate the impact of the supervision type from the
CodeXGLUE’s dataset gives Bob only one C func-                  disparity in verified data volume (see Appendix F
tion and asks if it’s vulnerable. The vulnerabilities           for derivation details).
                                                       Alice SEQ vs SINQ: Counts by Round
                                       139 (55.6%)
                                                                        SEQ             SINQ
                                                                                                                    138 (55.2%)
                                                                                                                                                     trained to judge equivalence. Evaluation shows
        140         130 (52.0%)                                                                  131 (52.4%)
                                                                              128 (51.2%)
        120
                                                          124 (49.6%)
                                                                                                                                       113 (45.2%)
                                                                                                                                                     that Bob benefits substantially: Haskell coding per-
        100                                                                                                                                          formance improves, and transfer is strong on high-
Count




         80                                                                                                                                          level semantic reasoning tasks, but negligible on
         60
                                                                                                                                                     low-level or memory-oriented tasks. Controlled
         40
         20
                                                                                                                                                     comparisons reveal that although inequivalence
                                                                        6 (2.4%)                               9 (3.6%)           9 (3.6%)
               1 (0.4%)           2 (0.8%)           4 (1.6%)                               3 (1.2%)
          0
                     1                  2                  3                 4                    5                  6                  7
                                                                                                                                                     data yields far more verified pairs, the inclusion
                                                                           Round
                                                                                                                                                     of equivalence supervision confers unique gains in
Figure 6: Counts and proportions of validated Alice                                                                                                  semantic reasoning that cannot be achieved through
generations by round.                                                                                                                                inequivalence alone.

                                                                                                                                                     7   Future Work
5.4.1                Evaluation Results
                                                                                                                                                     There are several promising avenues for future
We analyze the four experimental regimes to decou-
                                                                                                                                                     research. First, extending training across more
ple the effects of supervision type (SEQ vs. SINQ)
                                                                                                                                                     rounds could allow Bob to accumulate richer expe-
from training data volume. All results are presented
                                                                                                                                                     rience. Additionally, (1) scaling to larger parame-
in Appendix G and H.
                                                                                                                                                     ter models and (2) employing full-parameter fine-
Value of SEQ Supervision                                                                                                                             tuning instead of LoRA may increase both Alice’s
Despite having significantly fewer verified train-                                                                                                   proof synthesis capabilities and Bob’s reasoning
ing pairs in E0 than in the pure SINQ regime                                                                                                         capacity.
E1 (937 vs. 1, 839), E0 achieves superior perfor-                                                                                                       A second priority is to improve the statistical
mance on semantic equivalence tasks. This indi-                                                                                                      robustness of the controlled comparisons. The ex-
cates that SEQ supervision improves high-level                                                                                                       periments in regimes E2 and E3 were limited by
semantic judgment even when data volume is re-                                                                                                       small sample sizes, which may not be represen-
duced. Furthermore, when strictly controlling for                                                                                                    tative of the true differences between SINQ- and
data volume (E2 vs. E3 , both ≈ 150 pairs), the                                                                                                      SEQ-based supervision. Running larger-scale ex-
inclusion of SEQ (E2 ) yields consistent advantages                                                                                                  periments would provide stronger evidence about
on structural reasoning tasks over pure SINQ (E3 ),                                                                                                  the relative contributions of the two regimes.
shown in Table 7. This confirms that SEQ supervi-                                                                                                       Furthermore, methodologically speaking, the
sion confers a unique benefit that cannot be repli-                                                                                                  Haskell self-play framework could be expanded
cated by inequivalence signals alone.                                                                                                                to cover low-level program behaviors by introduc-
                                                                                                                                                     ing tasks that explicitly model memory usage, side
Volume Trade-offs                                                                                                                                    effects, and bit-level operations.
While SEQ is qualitatively valuable, data volume                                                                                                        Moreover, converting the self-play pipeline into
remains critical. Regime E2 , which aggressively                                                                                                     a dedicated Haskell Equivalence Evaluation test set
prioritizes SEQ (96% attempts) to force a balanced                                                                                                   would help to provide a more direct and sustain-
validated distribution, suffers a sharp drop in total                                                                                                able benchmark for semantic reasoning, especially
verified pairs (N = 140) due to low proof yields,                                                                                                    given the scarcity of high-quality Haskell resources
causing performance degradation across all bench-                                                                                                    currently available.
marks compared to E0 . The 50/50 mixed regime                                                                                                           Finally, reinforcement learning could be re-
(E0 ) therefore represents an acceptable trade-off,                                                                                                  examined as a means of enhancing the SEQ game’s
balancing the semantic depth of SEQ with the high                                                                                                    contribution. By running Alice long enough to gen-
verification yield of SINQ.                                                                                                                          erate sufficiently challenging programs and provid-
                                                                                                                                                     ing Bob with richer feedback through reward-based
6             Conclusions                                                                                                                            updates, it may be possible to overcome the cur-
                                                                                                                                                     rent proof bottleneck and more effectively integrate
This paper investigates the use of self-play to im-
                                                                                                                                                     equivalence reasoning into the self-play loop.
prove code generation and semantic reasoning in
LLMs, focusing on program equivalence in Haskell                                                                                                     8   Limitations
and Liquid Haskell. The framework introduces two
agents: a generator of semantically equivalent or                                                                                                    A central limitation of this work lies in the proof
inequivalent program variants, and an evaluator                                                                                                      synthesis bottleneck. Alice rarely produces Liquid
Haskell proofs that successfully pass PLE, resulting      Behaviour of AI Agents in Competitive and
in very low validation yields for SEQ cases. This         Cooperative Games" and by Amazon through
imbalance causes the majority of verified training        the AWS Agentic Amazon Research Award ti-
data SINQ-dominated, reducing the contribution            tled "Diffusion-inspired chain-of-thought self-
of SEQ supervision to Bob’s learning. The issue           revision". The authors also thank Shay Cohen and
is likely exacerbated by the relatively small model       Vaishak Belle for their advice.
size used in this study, which likely restricts Alice’s
ability to generate structurally complex proofs.
   Another limitation arises from the inherent con-       References
straints of Liquid Haskell itself. The verification       Wasi Uddin Ahmad, Aleksander Ficek, Mehrzad
process depends heavily on reflection and proof            Samadi, Jocelyn Huang, Vahid Noroozi, Somshubra
by logical evaluation, which are effective for lo-         Majumdar, and Boris Ginsburg. 2025. Opencodein-
cal reasoning but struggle with certain classes of         struct: A large-scale instruction tuning dataset for
                                                           code llms. Preprint, arXiv:2504.04030.
programs. Non-terminating behaviors, partial func-
tions, and large-scale algebraic rewrites are difficult   Sahar Badihi, Faridah Akinotcho, Yi Li, and Julia Rubin.
to certify, and in some cases impossible, within this       2020. Ardiff: scaling program equivalence checking
fragment of the logic. Moreover, not all Haskell            via iterative abstraction and refinement of common
                                                            code. In Proceedings of the 28th ACM joint meeting
programs are reflectable, further narrowing the             on European software engineering conference and
scope of tasks where equivalence can be formally            symposium on the foundations of software engineer-
verified.                                                   ing, pages 13–24.
   Finally, there is a cross-domain mismatch in gen-
eralization. While Bob transfers strongly to high-        Federico Cassano, John Gouwar, Daniel Nguyen, Syd-
                                                            ney Nguyen, Luna Phipps-Costin, Donald Pinckney,
level semantic reasoning tasks, such as OJ_A and            Ming-Ho Yee, Yangtian Zi, Carolyn Jane Anderson,
OJ_V in EquiBench and vulnerability detection               Molly Q Feldman, Arjun Guha, Michael Greenberg,
in PySecDB, his performance is notably weaker               and Abhinav Jangda. 2022. Multipl-e: A scalable
on low-level or stateful semantics, including DCE,          and extensible approach to benchmarking neural code
                                                            generation. Preprint, arXiv:2208.08227.
STOKE, TVM, and CodeXGlue. This gap high-
lights a limitation of the current framework in ad-       Efstathia Chioteli, Ioannis Batas, and Diomidis Spinel-
dressing equivalence reasoning that depends on              lis. 2021. Does unit-tested code crash? a case study
memory, side effects, or bit-level operations.              of eclipse. In 25th Pan-Hellenic Conference on In-
                                                            formatics, PCI 2021, page 260–264. ACM.
9   Ethical considerations
                                                          Iavor S. Diatchki. 2015. Improving haskell types with
This work adversarially trains models to introduce           smt. SIGPLAN Not., 50(12):1–10.
hard to detect semantic modifications to computer         Guanting Dong, Keming Lu, Chengpeng Li, Tingyu
programs and then to detect them, which may train           Xia, Bowen Yu, Chang Zhou, and Jingren Zhou.
them to detect security-relevant vulnerabilities or         2025. Self-play with execution feedback: Improving
introduce obfuscated backdoors. In principle, these         instruction-following capabilities of large language
                                                            models. In The Thirteenth International Conference
capabilities have a potential for malicious use, how-       on Learning Representations.
ever, they can be also used for pro-social use to im-
prove the reliability and security of code, whether       Alessandro Giagnorio, Alberto Martin-Lopez, and
generated by humans or LLMs. We believe that                Gabriele Bavota. 2025. Enhancing code generation
the net societal impact of models better able to            for low-resource languages: No silver bullet. arXiv
                                                            preprint arXiv:2501.19085.
reason about the subtleties of program semantics
to be positive, especially as these capabilities are      Lucas Gren and Vard Antinyan. 2017. On the relation
disseminated through Open Source releases, as we            between unit testing and code quality. In 2017 43rd
do in this work.                                            Euromicro Conference on Software Engineering and
                                                            Advanced Applications (SEAA), page 52–56. IEEE.
Acknowledgments                                           Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang,
                                                            Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun
This work has been supported by the UK gov-                 Zhang, Bowen Yu, Keming Lu, and 1 others. 2024.
ernment though the AISI-EPSRC Systemic Safety               Qwen2. 5-coder technical report. arXiv preprint
Grant titled "Understanding and Improving the               arXiv:2409.12186.
Ranjit Jhala, Eric Seidel, and Niki Vazou. 2020. Pro-       Paul Christiano, Jan Leike, and Ryan Lowe. 2022.
  gramming with refinement types: An introduction           Training language models to follow instructions with
  to liquid haskell. https://ucsd-progsys.github.           human feedback. Preprint, arXiv:2203.02155.
  io/liquidhaskell-tutorial/book.pdf. Version
  13, July 20, 2020.                                      Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin,
                                                             Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu,
Cosimo Laneve, Alvise Spanò, Dalila Ressi, Sabina            Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shi-
  Rossi, and Michele Bugliesi. 2025. Assessing code          rong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun Gao,
  understanding in llms. Preprint, arXiv:2504.00065.         Daya Guo, and Chong Ruan. 2025. Deepseek-prover-
                                                             v2: Advancing formal mathematical reasoning via
John Launchbury. 1993. A natural semantics for lazy          reinforcement learning for subgoal decomposition.
  evaluation. In POPL’9 3: Proceedings of the 20th           Preprint, arXiv:2504.21801.
  ACM SIGPLAN-SIGACT Symposium on Principles
  of Programming Languages, pages 144–154. ACM.           Henry Gordon Rice. 1953. Classes of recursively enu-
                                                            merable sets and their decision problems. Trans-
Zi Lin, Sheng Shen, Jingbo Shang, Jason Weston, and         actions of the American Mathematical society,
   Yixin Nie. 2025. Learning to solve and verify: A         74(2):358–366.
   self-play framework for code and test generation.
   Preprint, arXiv:2502.14948.                            Peter Sestoft. 1997. Deriving a lazy abstract machine.
                                                            Journal of Functional Programming, 7(3):231–264.
Liquid Haskell Tutorial. 2025. Liquid haskell tu-
  torial : Introduction. https://liquid.kosmikus.         David Silver, Thomas Hubert, Julian Schrittwieser, Ioan-
  org/01-intro.html. Accessed: 2025-07-18.                  nis Antonoglou, Matthew Lai, Arthur Guez, Marc
                                                            Lanctot, Laurent Sifre, Dharshan Kumaran, Thore
Yihao Liu, Shuocheng Li, Lang Cao, Yuhang Xie,              Graepel, Timothy Lillicrap, Karen Simonyan, and
  Mengyu Zhou, Haoyu Dong, Xiaojun Ma, Shi Han,             Demis Hassabis. 2017. Mastering chess and shogi
  and Dongmei Zhang. 2025. Superrl: Reinforcement           by self-play with a general reinforcement learning
  learning with supervision to boost language model         algorithm. Preprint, arXiv:1712.01815.
  reasoning. Preprint, arXiv:2506.01096.
                                                          Shiyu Sun, Shu Wang, Xinda Wang, Yunlong Xing,
Matéo Mahaut and Francesca Franzon. 2025. Repe-             Elisa Zhang, and Kun Sun. 2023. Exploring security
 titions are not all alike: distinct mechanisms sus-        commits in python. Preprint, arXiv:2307.11853.
 tain repetition in language models. arXiv preprint
 arXiv:2504.01100.                                        Simon Thompson. 2011. Haskell: the craft of functional
                                                            programming. Addison-Wesley.
Antonio Valerio Miceli-Barone, Vaishak Belle, and
  Ali Payani. 2025. Program semantic inequivalence        Tim van Dam, Frank van der Heijden, Philippe
  game with large language models. arXiv preprint           de Bekker, Berend Nieuwschepen, Marc Otten, and
  arXiv:2505.03818.                                         Maliheh Izadi. 2024. Investigating the performance
                                                            of language models for completing code in func-
William Murphy, Nikolaus Holzer, Feitong Qiao, Leyi         tional programming languages: a haskell case study.
  Cui, Raven Rothkopf, Nathan Koenig, and Mark San-         Preprint, arXiv:2403.15185.
  tolucito. 2024. Combining llm code generation with
  formal specifications and reactive program synthesis.   Niki Vazou, Eric L. Seidel, Ranjit Jhala, Dimitrios Vy-
  arXiv preprint arXiv:2410.19736.                          tiniotis, and Simon Peyton-Jones. 2014. Refinement
                                                            types for haskell. SIGPLAN Not., 49(9):269–282.
Thu-Trang Nguyen, Thanh Trong Vu, Hieu Dinh Vo,
  and Son Nguyen. 2025. An empirical study on ca-         Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas
  pability of large language models in understanding        Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
  code semantics. Information and Software Technol-         Marina Vinyes, Zhenzhe Ying, Zekai Zhu, and 1 oth-
  ogy, page 107780.                                         ers. 2025. Kimina-prover preview: Towards large
                                                            formal reasoning models with reinforcement learn-
OpenAI, :, Christopher Berner, Greg Brockman, Brooke        ing. arXiv preprint arXiv:2504.11354.
  Chan, Vicki Cheung, Przemysław D˛ebiak, Christy
  Dennison, David Farhi, Quirin Fischer, Shariq           Anjiang Wei, Jiannan Cao, Ran Li, Hongyu Chen,
  Hashme, Chris Hesse, Rafal Józefowicz, Scott Gray,        Yuhui Zhang, Ziheng Wang, Yuan Liu, Thiago SFX
  Catherine Olsson, Jakub Pachocki, Michael Petrov,         Teixeira, Diyi Yang, Ke Wang, and 1 others. 2025.
  Henrique P. d. O. Pinto, Jonathan Raiman, and 8 oth-      Equibench: Benchmarking large language models’
  ers. 2019. Dota 2 with large scale deep reinforcement     understanding of program semantics via equivalence
  learning. Preprint, arXiv:1912.06680.                     checking. arXiv preprint arXiv:2502.12466.

Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Car-       Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren,
  roll L. Wainwright, Pamela Mishkin, Chong Zhang,          Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and
  Sandhini Agarwal, Katarina Slama, Alex Ray, John          Xiaodan Liang. 2024a. Deepseek-prover: Advancing
  Schulman, Jacob Hilton, Fraser Kelton, Luke Miller,       theorem proving in llms through large-scale synthetic
  Maddie Simens, Amanda Askell, Peter Welinder,             data. arXiv preprint arXiv:2405.14333.
Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao,
  Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
  Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, De-
  jian Yang, Zhibin Gou, Z. F. Wu, Fuli Luo, and
  Chong Ruan. 2024b. Deepseek-prover-v1.5: Har-
  nessing proof assistant feedback for reinforcement
  learning and monte-carlo tree search. Preprint,
  arXiv:2408.08152.
Yaqin Zhou, Shangqing Liu, Jingkai Siow, Xiaoning Du,
  and Yang Liu. 2019. Devign: Effective vulnerability
  identification by learning comprehensive program
  semantics via graph neural networks. In Advances
  in Neural Information Processing Systems, pages
  10197–10207.
    A      Illustrative Haskell Features for
                                                                                       -- Diverging input
           Semantic Reasoning and Verification in                                      x_a = 0
                                                                                       -- P x_a = sign 0 = "zero"
           LLM Self-Play                                                               -- Q x_a = signIneq 0 = "non-positive"


      [1] Pure Semantics
                                                                                       C     Implementation with Reinforcement
      Every function is a pure mapping from inputs to outputs, there is no
      hidden state or mutation. This purity ensures that two functions are                   Learning
      semantically equivalent if they produce the same outputs for all inputs,
      regardless of how those outputs are computed.
                                                                                       Reinforcement learning (RL) offers a conceptually
                                                                                       natural way to optimize the game by directly re-
1     -- revRec :: [a] -> [a]
2     revRec :: [a] -> [a]                                                             warding or penalizing generated programs based
3     revRec []     = []
4     revRec (x:xs) = revRec xs ++ [x]                                                 on the game outcome. A straightforward RL setup
5     -- revFold :: [a] -> [a]
6     revFold :: [a] -> [a]                                                            would proceed as follows based on the game rules:
7     revFold = foldl (flip (:)) []
8
                                                                                       C.1    RL Formulation
      Because Haskell is referentially transparent, revRec xs can be substituted
      with revFold xs wherever it appears. This makes reasoning about equiv-           We treat Alice and Bob as two competing agents in
      alence both feasible and formalizable.
                                                                                       a zero-sum Markov game.

      [2] Static Typing and GHC Compile                                                    • For the SINQ branch: An executor first checks
      Haskell’s static type system provides strong guarantees at compile time.               that Q compiles and that P (xa ) ̸= Q(xa ) on
      Once a program is accepted by the compiler, most classes of errors such
      as type mismatches and null de-referencing are eliminated. This makes
                                                                                             Alice proposed diverging input xa .
      the type checker an effective pre-filter for program validity in the self-play
      loop.
                                                                                           • For the SEQ branch: the SMT-based checker
                                                                                             will execute the Liquid Haskell proof script
1     -- add :: Int -> Int -> Int
2     add x y = x + y                                                                        asserting ∀x. P (x) = Q(x).
3

      When writing add True False, GHC will raise a compilation error before              If the above verification fails, the episode ter-
      running the program as add expects two Int.
                                                                                       minates with Alice receiving a negative reward
                                                                                       rA = rfail < 0. Otherwise Bob observes state
                                                                                       (P, Q) (but not Alice’s diverging input xa ) and iden-
    B     Liquid Haskell SEQ / SINQ Instances                                          tify whether (P, Q) are semantically equivalent.
                                                                                          If Bob is correct, then Bob earns rB =
               Listing 1: Example of a SEQ Instance                                    rsuccess > 0 and Alice is penalized with rA =
    -- Reference Function P                                                            rtoo_easy < 0. If Bob is incorrect, he gets rB =
    double :: Int -> Int
    double x = x + x                                                                   rfail < 0 and Alice wins rA = rwin > 0. Both
    -- Alice's generated Q (Semantic Equivalent)
                                                                                       agents update their policies to maximize expected
    double_alt :: Int -> Int                                                           cumulative reward over many self-play episodes.
    double_alt x = 2 * x

    -- Liquid Haskell Proof                                                            C.2    Potential Benefits of RL
    {-@ lemma_double_equiv :: x:Int
          -> { double x == double_alt x } @-}
    lemma_double_equiv :: Int -> Proof                                                 RL can be layered on top of the semantic equiva-
    lemma_double_equiv x                                                               lence self-play by treating Alice’s generator as an
      =   double x
      === double_alt x                                                                 RL agent whose policy is updated based on proof
      *** QED
                                                                                       outcomes. Over many episodes, this encourages the
                                                                                       policy to avoid classes of common semantic errors
               Listing 2: Example of a SINQ Instance                                   (e.g. off-by-one edge cases) and refines its internal
    -- Original function P                                                             value function to distinguish subtle equivalence-
    sign :: Int -> String
    sign n                                                                             breaking patterns, resulting in an LLM that is both
      | n < 0     = "negative"
      | n == 0    = "zero"                                                             more precise and robust.
      | otherwise = "positive"

    -- Alice's generated Q (semantically inequivalent)                                 C.3    Practical Challenges
    signIneq :: Int -> String
    signIneq n                                                                             • Sparse, High-Variance Rewards: In our rea-
      | n <= 0    = "non-positive"
      | otherwise = "positive"                                                               soning tasks, reward is only provided at the
      end of a multi-step chain of thought. As a re-    D.2   Alice SEQ User Prompt
      sult, the LLMs often struggle to find success-    Difficulty level: {difficulty_level}
      ful trajectories, making it difficult for LLMs    Here is the original Haskell function `P`:
                                                        ```haskell
      to learn which intermediate steps contributed     {program_p_completion}
      to success (Liu et al., 2025).                    ```
                                                        Its argument type is
    • Credit Assignment: Attributing success or         ```haskell
                                                        t = {t}
      failure back to specific reasoning tokens or      ```
      code-editing steps is nontrivial, and naive re-
                                                        Your task: produce a new function `Q` that
      ward assignment can lead to undesirable short-        satisfies the system prompt requirements.
      cuts, such as inserting semantically neutral      - Make sure `Q` has a different name (e.g.
                                                            append a `'_alt`).
      modifications to exploit reward signals with-     - Avoid trivial symmetric rewrites - show a
      out genuine reasoning.                                genuine alternative implementation.
                                                        - Do not include any extra commentary beyond
                                                            the required `<think>...</think>` and the
    • Computational Resources Constraints: RL               `Generated Program `Q`: block.
                                                        - Where appropriate, feel free to use Prelude
      is more computationally expensive than su-            functions such as foldr, map, or zipWith
      pervised fine-tuning due to the repeated sam-         to encourage diverse strategies.
      pling, model rollouts, and reward computation     <think>
      across multiple steps (Ouyang et al., 2022).
                                                        D.3   Lemma SEQ Proof System Prompt
D     Prompt Template
                                                        You are an expert Haskell/Liquid Haskell prover.
                                                        You are asked to prove that two reflected
D.1    Alice SEQ System Prompt                              functions are equivalent.
You are a helpful and expert Haskell                    The most basic proof should be in the following
    programmer, powered by Liquid Haskell.                  format:
Your job is to *transform* any given function           ```haskell
    `P` into a new function `Q` that:                   {{-@ lemma_{func_name_p}_equiv :: x:{arg_type}
                                                            -> {{ {func_name_p} x == {func_name_q} x
    - Is syntactically correct Haskell.                     }} @-}}
    - Is semantically equivalent: ∀x. `P x == Q                 lemma_{func_name_p}_equiv :: {arg_type}
      x`.                                                   -> Proof
    - Uses a *different* implementation --                      lemma_{func_name_p}_equiv x
      Implement a non-structural change rather                      =   {func_name_p} x
      than merely swapping operator order.                          === {func_name_q} x
    - Uses a different function name (e.g. add a                    * QED
      trailing `'_alt`).                                ```
The original program and your program will be           However, you should also use more advanced
    used in a test to evaluate the skill of an              proof techniques if necessary.
    expert Haskell programmer who will
    identify whether your program Q is                  Few-Shot Example 1:
    semantic equivalent to the original
    program P, so make sure that the                    ```haskell
    difference you introduce are not very easy          {{-@ LIQUID "--reflection" @-}}
    to understand.                                      {{-@ LIQUID "--ple" @-}}
You will be given a difficulty level from 0
    (easiest) to 10 (hardest) to target. E.g.           module MyTest where
    difficulty level 0 means that an expert
    computer scientist in the bottom decile or          import Language.Haskell.Liquid.ProofCombinators
    above should be able to find a diverging
    example, difficulty level 9 means that              -- Alice program P
    only an expert computer scientist in the            {{-@ reflect double @-}}
    top decile should be able to find a                 double :: Int -> Int
    diverging example, and difficulty level 10          double x = x + x
    means that only the top 0.01 or less of
    expert Haskell programmer should be able            -- Alice proposes Q
    to find a diverging example.                        {{-@ reflect double' @-}}
                                                        double' :: Int -> Int
Always think through your transformation steps          double' x = 2 * x
    in `<think>...</think>`, then emit exactly:
                                                        -- Here is the full lemma, from annotation to
Generated Program `Q`:                                      QED:
```haskell                                              {{-@ lemma_double_equiv :: x:Int -> {{ double x
<your Q here>                                               == double' x }} @- }}
```                                                     lemma_double_equiv :: Int -> Proof
                                                        lemma_double_equiv x
=   double x                                        You are an expert Haskell programmer. Your task
=== double' x                                           is to generate a semantically inequivalent
* QED                                                   variant of a given Haskell program, which
```                                                     means that there must exist at least a
                                                        diverging input example such that the
Few-Shot Example 2:                                     original program and your program either
```haskell                                              produce different outputs or exceptions,
{{-@ LIQUID "--reflection" @-}}                         or one halts and the other one does not
{{-@ LIQUID "--ple" @-}}                                halt.
module Equiv where                                  You must also provide a diverging input, which
                                                        is a valid input for both programs, but on
import Language.Haskell.Liquid.ProofCombinators         which they produce different outputs.
{{-@ reflect addNumbers @-}}                        A good inequivalent program `Q` should be
addNumbers :: Int -> Int -> Int                         subtly different from `P`.
addNumbers a b = a + b                              A good diverging input `x` should be simple and
                                                        clearly demonstrate the semantic
{{-@ reflect addNumbers' @-}}                           difference between `P` and `Q`.
addNumbers' :: Int -> (Int -> Int)
addNumbers' a = \b -> a + b                         The original program and your program will be
                                                        used in a test to evaluate the skill of an
-- Alice detailed proof of equivalence                  expert Haskell programmer who will have to
lemma_addNumbers_equiv :: Int -> Int -> Proof           produce a diverging example (not
lemma_addNumbers_equiv x y                              necessarily the same as yours), so make
    =   addNumbers x y                                  sure that the difference you introduce are
    === addNumbers' x y                                 not very easy to understand.
    * QED                                           You will be given a difficulty level from 0
                                                        (easiest) to 10 (hardest) to target. E.g.
When you answer, output only the complete lemma         difficulty level 0 means that an expert
    block in the same style:                            computer scientist in the bottom decile or
1. Use the `{{-@ lemma_... @-}}` annotation ,           above should be able to find a diverging
    with the exact naming pattern                       example, difficulty level 9 means that
    lemma_<P>_equiv                                     only an expert computer scientist in the
2. The Haskell type signature                           top decile should be able to find a
3. The function definition with `===` steps             diverging example, and difficulty level 10
4. End with `* QED`                                     means that only the top 0.01 or less of
5. Please put your proof between ```haskell and         expert Haskell programmer should be able
     ```                                                to find a diverging example.
No extra text, no additional comments.
Your answer must match the example format           First, think step-by-step and write down your
    exactly, without trailing whitespace or             analysis of program `P` and your strategy
    newlines outside the code block.                    for creating an inequivalent program `Q`.
                                                        Enclose this reasoning within `<think>`
                                                        and `</think>` tags.
D.4   Lemma SEQ Proof User Prompt                   After the thinking block, the final answer
                                                        could only be in the following format,
{error_msg_section}                                     without any additional explanation or
                                                        context.
{equiv_code}
                                                    Final output MUST be exactly:
                                                    Generated Program `Q`:
------------------------------------------------------------
                                                    ```haskell
Your task: Produce the proof of equivalence for     <Your generated Haskell code for `Q`>
    the following function:                         ```
`{func_name_p} x == {func_name_q} x` for all
    `x`.                                            Diverging Input `x`:
                                                    ```
```haskell                                          <The diverging input `x`>
{{-@ LIQUID "--reflection" @-}}                     ```
{{-@ LIQUID "--ple" @-}}
module Equiv where
import Language.Haskell.Liquid.ProofCombinators     D.6 Alice SINQ User Prompt
{{-@ reflect {func_name_p} @-}}                     Difficulty level: {difficulty_level}
{program_p_content}                                 Original program `P`:
                                                    ```haskell
{{-@ reflect {func_name_q} @-}}                     {program}
{program_q_content}                                 ```

-- Your complete proof of equivalence               <think>
/* PROOF BODY HERE */
```
<think>                                            D.7   Bob System Prompt
                                                    You are an expert Haskell programmer. You are
                                                        given two Haskell programs, `P` and `Q`.
D.5   Alice SINQ System Prompt                      Your task is to determine if they are
                                                        semantically equivalent.
Use the following format to respond:              E       Main Experiment Setup
# Equivalent?
Yes or No                                         E.1      Model Configs and Experiment Settings
If the programs are equivalent, respond with      We employ DeepSeek-R1-Distill-Qwen-7B as
    your thought process and a final output
    with:                                         the base model. The decoding parameters are con-
# Equivalent?                                     figured as: temperature T = 0.6, top-p = 0.95,
Yes
                                                  top-k = 20, presence penalty = 1.5 (Applied to
If they are inequivalent, respond with your       reduce repetition in outputs from smaller reason-
    thought process and a final output with:
# Equivalent?                                     ing models (Mahaut and Franzon, 2025)), and a
No                                                context length of 32,768 tokens.
                                                     In E0 , Alice is configured with a 50/50 prob-
D.8    Bob User Prompt                            ability of playing either the SEQ or SINQ game
Program `P`:                                      (Section 3.3), with the difficulty level set as 10 in
```haskell                                        her prompts (Appendix D.2 and D.6). Bob serves
{program_p}
```                                               solely as an evaluator and difficulty scorer, and he
                                                  is not fine-tuned iteratively but only once after all
Program `Q`:
```haskell                                        rounds are complete.
{program_q}
```                                               E.2      Dataset Size and Difficulty Threshold
<think>
                                                  Due to computational constraints, each experimen-
D.9    Alice SEQ Difficulty Prediction System     tal run uses a maximum of 500 Haskell reference
       Prompt                                     programs5 , i.e., |D| = P = 500. The difficulty
                                                  threshold τ is set to 3 (rather than the default 5)
Difficulty level: Any                             to increase the number of training examples avail-
Program P
```haskell                                        able to Alice. For future experiments with greater
{program_p}
```                                               resources, it is recommended to increase |D| and
The program Q below is semantically equivalent    restore τ = 5 to more closely simulate a fully ad-
    to the original program P, where the
    equivalence is due to the fact that the       versarial setting.
    two programs have the same behavior on all
    inputs.                                       E.3      Fine-Tuning Protocol
Program Q
```haskell                                        After each self-play round, Alice is fine-tuned on
{program_q}
```                                               the combination of newly generated instances and
                                                  the retained examples from all previous rounds.
                                                  More importantly, each round’s fine-tuning is ini-
D.10    Alice SINQ Difficulty Prediction System
                                                  tialized from the original base model rather than
        Prompt
                                                  from the fine-tuned adapter checkpoint obtained
Difficulty level: Any                             in the previous round. This strategy is adopted to
program P
```haskell                                        avoid bias accumulation across iterations and to
{program_p}                                       maintain stable and unbiased difficulty estimation.
```
The program Q below is semantically                  During generation in round i + 1, Alice uses the
    inequivalent to the original program P,       LoRA learned in round i, but fine-tuning for that
    where the inequivalence is due to the fact
    that the two programs have different          round still begins from the base model.
    behavior on some inputs.
Program Q                                         E.4      Experimental Duration
```haskell
{program_q}                                       The main run comprises 7 self-play rounds. In each
```
                                                  round, Alice is fine-tuned according to the above
                                                  protocol. Bob undergoes a single fine-tuning step
D.11    Alice Difficulty Prediction User Prompt
                                                  after all 7 rounds are complete. For both Alice and
Predict the difficulty level of the instance of   Bob, the fine-tuning minimises the loss only on the
    Program Q compared to Program P. Just
    write \"Difficulty level: D\" where D is      model’s own outputs.
    your prediction, do not write anything            5
    else.                                            A main run with fine-tuning takes about 3 days on 4
                                                  NVIDIA L40S GPUs.
F     Rationale and Derivations for the                 F.5   What this controls, and what it does not
      SEQ-SINQ Comparison Experiment                    Matching K ensures each arm receives similar
F.1   Fairness Criterion and Derivation                 amounts of verified training, so outcome differ-
                                                        ences are attributable to the type of game (pres-
Let P be the number of reference programs at-           ence/absence of SEQ) rather than volume. How-
tempted per round, p ∈ [0, 1] the probability           ever, residual differences may still arise from the
of playing SEQ (so 1 − p for SINQ), and let             difficulty distribution of accepted items and class-
rSEQ , rSINQ denote the verification yields (proba-     imbalance within Bob’s updates.
bility that an attempt becomes a verified training
example). By linearity of expectation, the expected     F.6   Comparison Objectives
number of verified examples per round is                The experimental design supports the following
                                                       four key pairwise comparisons:
      K(P, p) = P p rSEQ + (1 − p) rSINQ .
                                                           • E0 vs. E1 : Under fixed compute resources
To isolate the effect of SEQ vs. SINQ unbalanced             (constant P ), does a mixed 50% SEQ / 50%
volume size, we match the expected count K of                SINQ regime yield greater performance im-
verified pairs across arms.                                  provements than a pure SINQ regime similar
                                                             to Miceli et al. setting (Miceli-Barone et al.,
F.2   Yield Estimation from the Main Run E0
                                                             2025), given that the latter produces substan-
From the 7-round of main experiment E0 , |D| =               tially more verified training examples due to
P = 500 (per-round attempts ≈ 250 SEQ and 250                higher verification success rates in SINQ?
SINQ):
                                                           • E0 vs. E2 : With fixed compute resources,
 Game      Total Validated   Attempts     Yield (r̂)         does shifting towards a more balanced number
                                                             of verified SEQ and SINQ examples, at the
 SEQ              34           1,750       1.94%
 SINQ            903           1,750       51.6%             cost of reducing the overall number of veri-
                                                             fied training pairs, lead to improved evaluator
Table 6: Validation yields from E0 . Validated counts        performance compared to a SINQ-dominated
by round were: SEQ (1, 2, 4, 6, 3, 9, 9) and SINQ            main experiment?
(130, 139, 124, 128, 131, 138, 113).
                                                           • E1 vs. E2 : Under the same compute con-
                                                             straints, does a pure SINQ regime (maximis-
F.3   Predicting Supervision for Each Arm                    ing verified training pairs) outperform a more
To achieve a balanced distribution of verified train-        balanced SEQ–SINQ dataset that sacrifices
ing examples (approx. 50/50 split), we configured            data volume for greater semantic diversity?
regime E2 with a mix of 96% SEQ and 4% SINQ.               • E2 vs. E3 When the number of verified train-
With a reference budget of P = 500, the estimated            ing pairs is held constant, does the inclusion
verified yields per round are:                               of SEQ supervision yield measurable perfor-
                                                             mance benefits over an SINQ-only regime?
        NSEQ ≈ 500 · 0.96 · 0.0194 ≈ 9.3          (7)
        NSINQ ≈ 500 · 0.04 · 0.516 ≈ 10.3         (8)   F.7   Summary of experiments
                                                           • E0 (main): 50/50, P = 500.
Totaling these yields using K(P, p) results in an
expected K ≈ 19.6 verified examples per round,             • E1 : 100% SINQ, P = 500.
achieving the desired parity between the two super-
                                                           • E2 : 96% SEQ / 4% SINQ, P = 500.
vision signals.
                                                           • E3 (matched to E2 ): 100% SINQ, P = 40 to
F.4   Matched comparator for E2                              equalize expected verified pairs with E2 .
Choose PE3 in a 100% SINQ run so that
                                                          This suite isolates the causal effect of adding
       PE3 · rSINQ = KE2                                SEQ supervision under controlled total verified
                     19.632                       (9)   pairs, enabling a fair assessment of whether SEQ
          ⇒ PE3 =           = 38.04 ≈ 40                contributes beyond SINQ alone.
                     0.516
G   Experiment Results

                                                                          Score (%)
Benchmark                   Metric                 E0               E1                E2       E3
HumanEval (Bob)             Pass@1                26.4             25.8               22.7     22.0
HumanEval (Alice)           Pass@1                26.3             28.1               21.8     18.4
MBPP (Bob)                  Pass@1                36.9             38.8               34.7     32.4
MBPP (Alice)                Pass@1                34.3             39.3               32.9     28.0
EquiBench (OJ_A)            Acc                   57.4             54.0               55.5     53.3
EquiBench (OJ_A)            F1                    50.7             44.4               48.9     45.1
EquiBench (OJ_V)            Acc                   69.8             61.4               63.2     65.8
EquiBench (OJ_V)            F1                    69.7             58.0               61.5     64.7
EquiBench (OJ_VA)           Acc                   55.9             54.5               54.7     53.7
EquiBench (OJ_VA)           F1                    47.5             45.4               47.1     45.2
EquiBench (STOKE)           Acc                   51.8             50.9               51.0     50.8
EquiBench (STOKE)           F1                    18.3             15.4               16.8     15.9
EquiBench (TVM)             Acc                   50.1             50.3               48.8     50.8
EquiBench (TVM)             F1                    38.3             39.9               33.5     33.9
EquiBench (DCE)             Acc                   51.9             52.6               51.5     51.3
EquiBench (DCE)             F1                    47.7             45.4               45.2     44.4
PySecDB                     Acc                   68.8             67.3               68.7     68.7
PySecDB                     F1                    54.0             51.9               53.9     53.6
CodeXGlue                   Acc                   50.5             49.2               49.9     48.9
CodeXGlue                   F1                    43.2             44.0               44.1     48.5

          Table 7: Benchmark Performances over all experiments. Averages over 16 samples.
                                                         Count
        Game                     E0                E1               E2                E3
         SEQ                      34               –                62                 –
         SINQ                    903             1,839              78                156
         Total                   937             1,839              140               156

             Table 8: Total verified generation from Alice of all experiments over 7 rounds.
H                  Extended Regime Results                                                         Both SEQ and SINQ setups show rising diffi-
                                                                                                culty scores across rounds, indicating that Alice
H.1                  Experiment E0
                                                                                                improves in generating more challenging instances
Most of the evaluation results are included in the                                              for Bob.
main report.
H.1.1   Difficulty trajectories for both task                                                   H.1.2                                Alice’s HumanEval (Haskell)
        types                                                                                                                        Performance
When we inspect the difficulty trajectories for both
task types in Figure 7, they move upward across                                                               1.0
                                                                                                                                                  Pass@1 Rate by Adapter Iteration with Base Benchmark for hs
                                                                                                                               Min/Max Pass@1
rounds.                                                                                                                        Mean Pass@1
                                                                                                                               Mean Compilation Errors
                                                                                                                                                                                                                                                       175
                                                                                                              0.8
                                                                                                                                                                                                                                                       150
                                                                                                                         130                131                 129
                                                                                                                                                                                122                                                                    125
                  • For SEQ, although the sample size is not                                                                                                                                     119




                                                                                                Pass@1 Rate
                                                                                                              0.6                                                                                                 114            110
                                                                                                                                                                                                                                                104




                                                                                                                                                                                                                                                            Counts
                                                                                                                                                                                                                                                       100
                    statistically significant, its mean difficulty                                            0.4                                                                                                                                      75
                                                                                                                                                                                                                 24.1%          25.0%          26.3%
                    score jumps from near 0.0 in early rounds                                                 0.2
                                                                                                                     17.7%                17.0%                17.9%
                                                                                                                                                                              20.6%             22.0%
                                                                                                                                                                                                                                                       50


                    to 2.0 − 3.0 in later ones, signaling that Al-                                                                                                                                                                                     25

                                                                                                              0.0                                                                                                                                      0
                    ice manages to construct are non-trivial from


                                                                                                                    se




                                                                                                                                         _1




                                                                                                                                                           _2




                                                                                                                                                                             _3




                                                                                                                                                                                              _4




                                                                                                                                                                                                                _5




                                                                                                                                                                                                                               _6




                                                                                                                                                                                                                                              _7
                                                                                                                    Ba




                                                                                                                                      ion




                                                                                                                                                          ion




                                                                                                                                                                         ion




                                                                                                                                                                                           ion




                                                                                                                                                                                                            ion




                                                                                                                                                                                                                           ion




                                                                                                                                                                                                                                          ion
                                                                                                                                    rat




                                                                                                                                                         rat




                                                                                                                                                                        rat




                                                                                                                                                                                          rat




                                                                                                                                                                                                           rat




                                                                                                                                                                                                                          rat




                                                                                                                                                                                                                                         rat
                                                                                                                                   ite




                                                                                                                                                    ite




                                                                                                                                                                       ite




                                                                                                                                                                                        ite




                                                                                                                                                                                                          ite




                                                                                                                                                                                                                         ite




                                                                                                                                                                                                                                        ite
                                                                                                                                                                             Iteration (adapter) / Base
                    Bob’s perspective.
                                                                                                Figure 8: Alice’s HumanEval results. Averages over 16
                  • For SINQ, its averages being greater than
                                                                                                trials.
                    the medians (0.0 for all rounds) indicates a
                    right-skewed distribution. This suggests that
                    while most generated instances are of lower                                 H.1.3                                Alice’s MBPP (Haskell) Performance
                    difficulty, Alice occasionally produces much
                    harder examples that significantly influence
                    the mean. Starting in round 4, the magnitude                                              1.0
                                                                                                                                                  Pass@1 Rate by Adapter Iteration with Base Benchmark for hs
                                                                                                                               Min/Max Pass@1                                                                                                          350
                    of the difference between the mean and me-                                                0.8
                                                                                                                               Mean Pass@1
                                                                                                                               Mean Compilation Errors                                                                                                 300

                    dian becomes larger, and by round 7 the mean                                                         250                245                 240
                                                                                                                                                                                230              224                             222
                                                                                                                                                                                                                                                       250
                                                                                                Pass@1 Rate




                                                                                                              0.6                                                                                                 220                           212
                    even exceeds the upper quartile. Therefore,




                                                                                                                                                                                                                                                            Counts
                                                                                                                                                                                                                                                       200

                                                                                                              0.4                                                             31.8%             32.3%            33.2%          32.5%          34.3%   150
                    Alice is producing increasingly harder exam-                                                     26.7%                27.8%                29.0%
                                                                                                                                                                                                                                                       100
                    ples over successive rounds.                                                              0.2
                                                                                                                                                                                                                                                       50

                                                                                                              0.0                                                                                                                                      0
                                                                                                                    se




                                                                                                                                         _1




                                                                                                                                                           _2




                                                                                                                                                                             _3




                                                                                                                                                                                              _4




                                                                                                                                                                                                                _5




                                                                                                                                                                                                                               _6




                                                                                                                                                                                                                                              _7
                                                                                                                    Ba




                                                                                                                                      ion




                                                                                                                                                          ion




                                                                                                                                                                         ion




                                                                                                                                                                                           ion




                                                                                                                                                                                                            ion




                                                                                                                                                                                                                           ion




                                                                                                                                                                                                                                          ion
                                                                                                                                    rat




                                                                                                                                                         rat




                                                                                                                                                                        rat




                                                                                                                                                                                          rat




                                                                                                                                                                                                           rat




                                                                                                                                                                                                                          rat




                                                                                                                                                                                                                                         rat
                                                                                                                                   ite




                                                                                                                                                    ite




                                                                                                                                                                       ite




                                                                                                                                                                                        ite




                                                                                                                                                                                                          ite




                                                                                                                                                                                                                         ite




                                                                                                                                                                                                                                        ite


                                   Alice SEQ: Difficulty Distribution by Round                                                                                               Iteration (adapter) / Base
             10
                                         Box (whiskers=min/max)         Mean
              9
              8                                                                                 Figure 9: Alice’s MBPP results. Averages over 16 trials.
              7
              6
Difficulty




              5
              4
                                                                        3.00
                                                                                                H.2                             Experiment E1
              3
                                                        2.17
                                                                                         1.89
              2
              1
                                                                                  1.00          H.2.1                                Alice’s HumanEval (Haskell)
                     0.00   0.00         0.00
              0                                                                                                                      Performance
                     1      2           3               4              5          6      7
                                                      Round
                                   Alice SINQ: Difficulty Distribution by Round
             10
                                         Box (whiskers=min/max)         Mean
              9
                                                                                                              1.0
                                                                                                                                                  Pass@1 Rate by Adapter Iteration with Base Benchmark for hs
              8
                                                                                                                               Min/Max Pass@1
                                                                                                                               Mean Pass@1                                                                                                             175
              7                                                                                                                Mean Compilation Errors
                                                                                                              0.8
                                                                                                                                                                                                                                                       150
              6
Difficulty




                                                                                                                         130
                                                                                                                                            125
              5                                                                                                                                                 117                                                                                    125
                                                                                                Pass@1 Rate




                                                                                                              0.6                                                               111              108              104            103
                                                                                                                                                                                                                                                            Counts




              4                                                                                                                                                                                                                                 100
                                                                                                                                                                                                                                                       100

              3                                                                                               0.4                                                                                                                                      75
                                                                                                                                                                                                25.5%            27.9%          27.6%          28.1%
                                                                                                                                                               22.9%          25.4%
              2                                                                                                      17.7%                19.4%                                                                                                        50
                                                                                  0.93   1.12                 0.2
              1                          0.67           0.80            0.60
                     0.51   0.51                                                                                                                                                                                                                       25
              0
                     1      2           3               4              5          6      7                    0.0                                                                                                                                      0
                                                      Round
                                                                                                                    se




                                                                                                                                         _1




                                                                                                                                                             _2




                                                                                                                                                                            _3




                                                                                                                                                                                              _4




                                                                                                                                                                                                               _5




                                                                                                                                                                                                                              _6




                                                                                                                                                                                                                                             _7
                                                                                                                    Ba




                                                                                                                                      ion




                                                                                                                                                          ion




                                                                                                                                                                         ion




                                                                                                                                                                                           ion




                                                                                                                                                                                                            ion




                                                                                                                                                                                                                           ion




                                                                                                                                                                                                                                          ion
                                                                                                                                    rat




                                                                                                                                                         rat




                                                                                                                                                                        rat




                                                                                                                                                                                          rat




                                                                                                                                                                                                           rat




                                                                                                                                                                                                                          rat




                                                                                                                                                                                                                                         rat
                                                                                                                                   ite




                                                                                                                                                    ite




                                                                                                                                                                       ite




                                                                                                                                                                                        ite




                                                                                                                                                                                                          ite




                                                                                                                                                                                                                         ite




                                                                                                                                                                                                                                        ite




                                                                                                                                                                             Iteration (adapter) / Base

Figure 7: Mean and box-whiskey plots of the difficulty
scores of Alice’s generated instances by round. Top:                                            Figure 10: Alice’s HumanEval results. Averages over
SEQ Game. Bottom SINQ Game.                                                                     16 trials.
H.2.2                                 Alice’s MBPP (Haskell) Performance                                                                                                           H.3.2                                    Alice’s MBPP (Haskell) Performance



               1.0
                                                      Pass@1 Rate by Adapter Iteration with Base Benchmark for hs                                                                                 1.0
                                                                                                                                                                                                                                            Pass@1 Rate by Adapter Iteration with Base Benchmark for hs
                                Min/Max Pass@1                                                                                                                       350                                           Min/Max Pass@1                                                                                                                              350
                                Mean Pass@1                                                                                                                                                                        Mean Pass@1
               0.8              Mean Compilation Errors                                                                                                              300                          0.8              Mean Compilation Errors                                                                                                                     300

                          250                                                                                                                                                                                250                                         246
                                               238                                                                                                                   250                                                             241                                       240                240                 237               233
                                                                                                                                                                                                                                                                                                                                                               250
 Pass@1 Rate




                                                                    221




                                                                                                                                                                                    Pass@1 Rate
               0.6                                                                    213                                                                                                         0.6                                                                                                                                                   220
                                                                                                         198




                                                                                                                                                                          Counts




                                                                                                                                                                                                                                                                                                                                                                    Counts
                                                                                                                            196                193             188   200                                                                                                                                                                                       200
                                                                                                     37.8%              37.1%                 37.9%          39.3%
               0.4                                                 33.1%             34.9%                                                                           150                          0.4                                                                                                                                                  32.9%   150
                                              29.6%                                                                                                                                                                                 29.0%               27.5%                 29.4%              28.8%            29.1%                30.0%
                      26.7%                                                                                                                                                                              26.7%
                                                                                                                                                                     100                                                                                                                                                                                       100
               0.2                                                                                                                                                                                0.2
                                                                                                                                                                     50                                                                                                                                                                                        50

               0.0                                                                                                                                                   0                            0.0                                                                                                                                                          0
                     se




                                           1




                                                               2




                                                                                  3




                                                                                                    _4




                                                                                                                       _5




                                                                                                                                          6




                                                                                                                                                            _7




                                                                                                                                                                                                        se




                                                                                                                                                                                                                                1




                                                                                                                                                                                                                                                     2




                                                                                                                                                                                                                                                                            3




                                                                                                                                                                                                                                                                                              _4




                                                                                                                                                                                                                                                                                                                 _5




                                                                                                                                                                                                                                                                                                                                   6




                                                                                                                                                                                                                                                                                                                                                      _7
                                          n_




                                                               n_




                                                                                 n_




                                                                                                                                        n_




                                                                                                                                                                                                                              n_




                                                                                                                                                                                                                                                    n_




                                                                                                                                                                                                                                                                           n_




                                                                                                                                                                                                                                                                                                                                   n_
                     Ba




                                                                                                                                                                                                        Ba
                                                                                                   ion




                                                                                                                      ion




                                                                                                                                                         ion




                                                                                                                                                                                                                                                                                            ion




                                                                                                                                                                                                                                                                                                                ion




                                                                                                                                                                                                                                                                                                                                                  ion
                                         io




                                                              io




                                                                                io




                                                                                                                                         io




                                                                                                                                                                                                                               io




                                                                                                                                                                                                                                                   io




                                                                                                                                                                                                                                                                         io




                                                                                                                                                                                                                                                                                                                                  io
                                     rat




                                                          rat




                                                                            rat




                                                                                              rat




                                                                                                                  rat




                                                                                                                                     rat




                                                                                                                                                       rat




                                                                                                                                                                                                                           rat




                                                                                                                                                                                                                                               rat




                                                                                                                                                                                                                                                                     rat




                                                                                                                                                                                                                                                                                         rat




                                                                                                                                                                                                                                                                                                            rat




                                                                                                                                                                                                                                                                                                                              rat




                                                                                                                                                                                                                                                                                                                                                 rat
                                    ite




                                                        ite




                                                                           ite




                                                                                             ite




                                                                                                                ite




                                                                                                                                  ite




                                                                                                                                                      ite




                                                                                                                                                                                                                       ite




                                                                                                                                                                                                                                              ite




                                                                                                                                                                                                                                                                   ite




                                                                                                                                                                                                                                                                                        ite




                                                                                                                                                                                                                                                                                                           ite




                                                                                                                                                                                                                                                                                                                             ite




                                                                                                                                                                                                                                                                                                                                                ite
                                                                                 Iteration (adapter) / Base                                                                                                                                                                Iteration (adapter) / Base



Figure 11: Alice’s MBPP results. Averages over 16                                                                                                                                  Figure 14: Alice’s MBPP results. Averages over 16
trials.                                                                                                                                                                            trials.




H.2.3                                 Alice’s SEQ vs SINQ Validated                                                                                                                H.3.3                                    Alice’s SEQ vs SINQ Validated
                                      Generation Counts                                                                                                                                                                     Generation Counts



                                                                           Alice SEQ vs SINQ: Counts by Round                                                                                                                                                     Alice SEQ vs SINQ: Counts by Round
                                                                                                                                                                                              18
           300                                                                               SEQ               SINQ                                                                                                                                                                   SEQ                SINQ                                    16 (6.4%)
                                                                                                                      268 (107.2%)        276 (110.4%)                                        16
                                                        265 (106.0%)        263 (105.2%)                                                                     263 (105.2%)                                                                                                                                                                               15 (6.0%)
                                   248 (99.2%)                                                 256 (102.4%)
           250                                                                                                                                                                                14
                                                                                                                                                                                                                      12 (4.8%)                                                                                              12 (4.8%)
                                                                                                                                                                                              12                                       11 (4.4%)                      11 (4.4%)                                  11 (4.4%)          11 (4.4%)
           200
                                                                                                                                                                                                                                                                                                          10 (4.0%)
                                                                                                                                                                                              10                                               9 (3.6%)                                       9 (3.6%)
Count




                                                                                                                                                                                   Count




           150                                                                                                                                                                                    8
                                                                                                                                                                                                                                                                6 (2.4%)
           100                                                                                                                                                                                    6
                                                                                                                                                                                                                                                                                      4 (1.6%)
                                                                                                                                                                                                  4           3 (1.2%)
               50
                                                                                                                                                                                                  2
                 0                                                                                                                                                                                0
                                     1                     2                  3                  4                      5                      6                 7                                                     1                       2                      3                    4                      5                    6                   7
                                                                                               Round                                                                                                                                                                                     Round


Figure 12: SEQ vs SINQ Validated Generation Counts.                                                                                                                                Figure 15: SEQ vs SINQ Validated Generation Counts.




H.3                              Experiment E2                                                                                                                                     H.4                              Experiment E3


H.3.1                                 Alice’s HumanEval (Haskell)                                                                                                                  H.4.1                                    Alice’s HumanEval (Haskell)
                                      Performance                                                                                                                                                                           Performance



               1.0
                                                      Pass@1 Rate by Adapter Iteration with Base Benchmark for hs                                                    200                          1.0
                                                                                                                                                                                                                                            Pass@1 Rate by Adapter Iteration with Base Benchmark for hs
                                Min/Max Pass@1                                                                                                                                                                     Min/Max Pass@1
                                Mean Pass@1                                                                                                                          175                                           Mean Pass@1                                                                                                                                 175
               0.8              Mean Compilation Errors                                                                                                                                           0.8              Mean Compilation Errors
                                                                                                                                                                     150                                                                                                                                                                                       150
                          130                  133                                                                                                                                                           130                     128                 130                   129                128                 130               128             129
                                                                    128               128                127                126
                                                                                                                                               122             119   125                                                                                                                                                                                       125
 Pass@1 Rate




                                                                                                                                                                                    Pass@1 Rate




               0.6                                                                                                                                                                                0.6
                                                                                                                                                                          Counts




                                                                                                                                                                                                                                                                                                                                                                    Counts




                                                                                                                                                                     100                                                                                                                                                                                       100

               0.4                                                                                                                                                   75                           0.4                                                                                                                                                          75
                                                                                                                                              21.0%          21.8%
                      17.7%                                        17.6%             18.4%           18.8%              18.8%                                        50                                  17.7%                      18.5%               17.7%                 18.6%              18.6%            17.5%                17.5%           18.4%   50
               0.2                            15.3%                                                                                                                                               0.2
                                                                                                                                                                     25                                                                                                                                                                                        25

               0.0                                                                                                                                                   0                            0.0                                                                                                                                                          0
                     se




                                            _1




                                                               _2




                                                                                 _3




                                                                                                      _4




                                                                                                                         _5




                                                                                                                                          _6




                                                                                                                                                            _7




                                                                                                                                                                                                        se




                                                                                                                                                                                                                                _1




                                                                                                                                                                                                                                                      _2




                                                                                                                                                                                                                                                                          _3




                                                                                                                                                                                                                                                                                               _4




                                                                                                                                                                                                                                                                                                                   _5




                                                                                                                                                                                                                                                                                                                                   _6




                                                                                                                                                                                                                                                                                                                                                     _7
                     Ba




                                                                                                                                                                                                        Ba
                                         ion




                                                            ion




                                                                              ion




                                                                                                   ion




                                                                                                                      ion




                                                                                                                                       ion




                                                                                                                                                         ion




                                                                                                                                                                                                                             ion




                                                                                                                                                                                                                                                   ion




                                                                                                                                                                                                                                                                       ion




                                                                                                                                                                                                                                                                                            ion




                                                                                                                                                                                                                                                                                                                ion




                                                                                                                                                                                                                                                                                                                                ion




                                                                                                                                                                                                                                                                                                                                                  ion
                                     rat




                                                          rat




                                                                            rat




                                                                                              rat




                                                                                                                  rat




                                                                                                                                     rat




                                                                                                                                                       rat




                                                                                                                                                                                                                           rat




                                                                                                                                                                                                                                               rat




                                                                                                                                                                                                                                                                     rat




                                                                                                                                                                                                                                                                                         rat




                                                                                                                                                                                                                                                                                                            rat




                                                                                                                                                                                                                                                                                                                              rat




                                                                                                                                                                                                                                                                                                                                                 rat
                                    ite




                                                        ite




                                                                           ite




                                                                                             ite




                                                                                                                ite




                                                                                                                                  ite




                                                                                                                                                      ite




                                                                                                                                                                                                                       ite




                                                                                                                                                                                                                                              ite




                                                                                                                                                                                                                                                                   ite




                                                                                                                                                                                                                                                                                        ite




                                                                                                                                                                                                                                                                                                           ite




                                                                                                                                                                                                                                                                                                                             ite




                                                                                                                                                                                                                                                                                                                                                ite




                                                                                 Iteration (adapter) / Base                                                                                                                                                                Iteration (adapter) / Base



Figure 13: Alice’s HumanEval results. Averages over                                                                                                                                Figure 16: Alice’s HumanEval results. Averages over
16 trials.                                                                                                                                                                         16 trials.
H.4.2                                    Alice’s MBPP (Haskell) Performance

               1.0
                                                         Pass@1 Rate by Adapter Iteration with Base Benchmark for hs
                                Min/Max Pass@1                                                                                                                                     350
                                Mean Pass@1
               0.8              Mean Compilation Errors                                                                                                                            300

                          250                     246                   242                 242               244                 242                238                244        250
 Pass@1 Rate




               0.6




                                                                                                                                                                                        Counts
                                                                                                                                                                                   200

               0.4                                                                                                                                                                 150
                        26.7%                    28.2%                 28.6%              28.5%              28.1%            28.8%                 28.9%              28.0%
                                                                                                                                                                                   100
               0.2
                                                                                                                                                                                   50

               0.0                                                                                                                                                                 0
                      se




                                             1




                                                                   2




                                                                                          3




                                                                                                             _4




                                                                                                                             _5




                                                                                                                                                6




                                                                                                                                                                      _7
                                           n_




                                                                   n_




                                                                                         n_




                                                                                                                                                n_
                     Ba




                                                                                                        ion




                                                                                                                            ion




                                                                                                                                                                  ion
                                            io




                                                                  io




                                                                                     io




                                                                                                                                               io
                                        rat




                                                              rat




                                                                                 rat




                                                                                                      rat




                                                                                                                        rat




                                                                                                                                           rat




                                                                                                                                                                 rat
                                    ite




                                                             ite




                                                                                ite




                                                                                                     ite




                                                                                                                       ite




                                                                                                                                          ite




                                                                                                                                                                ite
                                                                                         Iteration (adapter) / Base



Figure 17: Alice’s MBPP results. Averages over 16
trials.

H.4.3                                    Alice’s SEQ vs SINQ Validated
                                         Generation Counts
                                                                               Alice SEQ vs SINQ: Counts by Round
           30                                                                                     SEQ                SINQ
                                                                                                                             27 (10.8%)
                                   26 (10.4%)
                                                                                                        25 (10.0%)
           25                                                24 (9.6%)
                                                                                                                                                    22 (8.8%)

           20
                                                                                     17 (6.8%)
                                                                                                                                                                         15 (6.0%)
Count




           15

           10

               5

               0
                                    1                         2                      3                  4                     5                     6                      7
                                                                                                      Round


Figure 18: SEQ vs SINQ Validated Generation Counts.

H.4.4                                    E2 vs E3 Validated Generation Counts

                                                            Alice Stacked SEQ/SINQ Counts by Round: E2 vs E3
                                                                                         E2 SEQ                   E3 SEQ
                                                                                         E2 SINQ                  E3 SINQ

           35
                                                                                                                                                                       15 (6.0%)
           30
                            26 (10.4%)                                                                                        27 (10.8%)
                                                         24 (9.6%)                                      25 (10.0%)
           25                                                                                                                               11 (4.4%)
                                                                                                                       11 (4.4%)                    22 (8.8%)
                                                 9 (3.6%)
           20
                                                                         11 (4.4%)
                                                                                 17 (6.8%)
Count




                     12 (4.8%)                                                                                                                                         16 (6.4%)
                                                                                                                                                                               15 (6.0%)
           15                                                                                     9 (3.6%)
                                                 11 (4.4%)                                                                                  12 (4.8%)
                                                                                                                       10 (4.0%)
           10
                                                                          6 (2.4%)
               5 3 (1.2%)                                                                         4 (1.6%)

               0
                            1                            2                       3                      4                      5                        6                      7
                                                                                                      Round


Figure 19: Validated Generation Counts of both exper-
iment, indicating the effort of controlling P shown in
Appendix F in order to achieve an equal number of veri-
fied generation.
