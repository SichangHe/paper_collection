                                                         Propose, Solve, Verify: Self-Play Through Formal Verification


                                                                             Alex Wilf 1 Pranjal Aggarwal 1 Bryan Parno 1
                                                                 Daniel Fried Louis-Philippe Morency 1 Paul Pu Liang 2 Sean Welleck 1
                                                                                1




                                                                    Abstract
                                                Training models through self-play alone (without
                                                any human data) has been a longstanding goal in
arXiv:2512.18160v1 [cs.AI] 20 Dec 2025




                                                AI, but its effectiveness for training large language
                                                models remains unclear, particularly in code gen-
                                                eration where rewards based on unit tests are brit-
                                                tle and prone to error propagation. We study self-
                                                play in the verified code generation setting, where           Figure 1: Propose, Solve, Verify (PSV) uses a formal veri-
                                                formal verification provides reliable correctness             fier to enable a self-play loop. We use PSV to train PSV-
                                                signals. We introduce P ROPOSE , S OLVE , V ER -              V ERUS, which starts from the same translated seed corpus
                                                IFY (PSV), a simple self-play framework where                 as AlphaVerus (Aggarwal et al., 2024) but expands it by
                                                formal verification signals are used to create a pro-         proposing new problem specifications and training on veri-
                                                poser capable of generating challenging synthetic             fied solutions. PSV-V ERUS improves across self-play itera-
                                                problems and a solver trained via expert iteration.           tions, opening a substantial gap over AlphaVerus or training
                                                We use PSV to train PSV-V ERUS, which across                  on the seed corpus alone (RFT).
                                                three benchmarks improves pass@1 by up to 9.6×
                                                over inference-only and expert-iteration baselines.
                                                We show that performance scales with the number               self-play is verification. An imperfect verifier can be ex-
                                                of generated questions and training iterations, and           ploited by the solver, and hence corrupt the solver’s training
                                                through ablations identify formal verification and            and any curricula that depend on the solver’s performance.
                                                difficulty-aware proposal as essential ingredients            Indeed, successful early attempts have come in easy-to-
                                                for successful self-play.                                     verify domains such as formal theorem proving (Dong &
                                                                                                              Ma, 2025) or easy-to-check synthetic tasks (Haluptzok et al.,
                                                                                                              2023; Dong et al., 2025; Zhao et al., 2025), leaving self-
                                         1. Introduction                                                      play’s scope of impact for LLMs unclear.
                                         A longstanding goal of AI research is to enable self-play, in        We study self-play for code generation, a domain where
                                         which a system learns by creating its own curriculum with-           verification typically relies on unit tests (Liu et al., 2023). A
                                         out human supervision (Silver et al., 2017; Sukhbaatar et al.,       fundamental limitation is that unit tests only cover a limited
                                         2018). In the context of large language models (LLMs), an            set of cases, so programs can pass them and still be incor-
                                         emerging family of proposer-solver algorithms holds the              rect (Xin & Reiss, 2017; Liu et al., 2023; Yuan et al., 2024).
                                         promise of improving LLMs through self-play (Haluptzok               This can lead the solver to optimize for passing tests rather
                                         et al., 2023; Zhao et al., 2025). In this setup, a proposer          than solving the underlying task, and errors can propagate
                                         model generates problems for a solver model to train on, and         across iterations (Lin et al., 2025; Baker et al., 2025). Hence
                                         the solver’s capabilities inform the proposer’s curriculum.          self-play in code generation remains an open problem.
                                         If one can reliably judge whether the solver’s outputs are
                                         correct, one can train the solver with reinforcement learning        We introduce P ROPOSE , S OLVE , V ERIFY (PSV), which
                                         and successfully design curricula that adapt to the solver’s         uses formal verification to unlock a new paradigm for self-
                                         capabilities.                                                        play in code generation. The core idea is for a proposer
                                                                                                              to generate problems in the form of formal specifications—
                                         Thus a fundamental challenge in realizing proposer-solver            statements that mathematically describe all possible permit-
                                              1                                                               ted inputs plus the desired output behavior of a program
                                                Carnegie Mellon University, School of Computer Science
                                         2
                                             MIT. Correspondence to: Alex Wilf <awilf@cs.cmu.edu>.            with respect to those inputs—-and for a solver to try to gen-
                                                                                                              erate programs that meet the specifications. The key benefit
                                         Preprint. Under Review. Copyright 2025 by the author(s).             is that formal verification provides a sound reward signal: if

                                                                                                          1
                                  Propose, Solve, Verify: Self-Play Through Formal Verification

      Python: Traditional Unit Tests                                              Verus: Formally Verified Code
Signature             def sort(arr):                         Spec       fn sort(s: &Vec<i32>) -> (ret: Vec<i32>)
                                                                                 ensures
                                                                                     forall|i: int, j: int| 0 <= i < j < ret@.len() ==>
                          for i in range(len(arr)):
Implementation            ...
                                                                                     ret@[i] <= ret@[j],
                                                                                     ...
                                                                        {

                      assert sort([1,2,3])==[1,2,3]
Unit Tests            assert sort([])==[]                    Implementation               let mut sorted = s.clone();
                                                                                          ...
                      assert sort([3,2,2,1])==[1,2,2,3]                                   proof { assert(old_sorted.to_multiset() =~= sorted@.to_multiset());}

                      ...
                                                             & proof                      ...




Figure 2: Test cases vs. formal verification. On the right, given any input that satisfies the specification’s preconditions
(here, just the type constraint of s), a program that meets the specification according to the formal verifier is guaranteed to
produce an output that satisfies the postcondition (here, the ensures clause saying that the vector is sorted). In self-play with
verified code generation, a proposer produces the function spec (including pre- and postconditions) and the solver produces
the program and proofs given a specification. This guarantee stands in contrast to supervision based on LLM-generated unit
tests (shown on the left), which can be incomplete (Yang et al., 2025b) and reward hackable (Baker et al., 2025).


the verifier accepts the program, then the program is guar-                 2. We train PSV-V ERUS, which outperforms the previous
anteed to satisfy its specification for all inputs. Thus unlike                state-of-the art AlphaVerus (Aggarwal et al., 2024) and
unit tests, formal verification prevents incorrect solutions                   Expert Iteration (Singh et al., 2024) on verified Rust
from entering the self-play loop.                                              programming.
We apply PSV to Verus (Lattuada et al., 2023), a frame-                     3. We show that performance scales with question bud-
work that enables formal verification of Rust programs                         get and iterations, and identify proposal coverage and
and has attracted recent interest for LLM code generation                      difficulty as factors driving self-play.
(e.g., Yang et al. (2025a); Aggarwal et al. (2024)). We de-
sign a difficulty-aware proposer that adapts the difficulty of              4. We release our code and models.1
proposed specifications based on the solver’s current pass
rates. We initialize self-play from the same translated corpus
used by AlphaVerus (Aggarwal et al., 2024), which orig-                 2. Related Work
inates from human-written problems. PSV then expands
this corpus by alternating between proposing new specifi-               Verified code generation. Verified code generation asks
cations, training the solver on verified solutions, and using           solver models to generate both programs and machine-
the solver’s performance to guide the next round of problem             checkable proofs that verifiers can deterministically and
proposal. As shown in Figure 1, the PSV self-play loop                  mechanically check against a specification. For example in
yields substantial gains: our model, PSV-V ERUS, improves               Figure 2, the implementation and proof must satisfy the post-
across iterations and substantially outperforms both training           conditions described in the ensures block of the spec over
on the seed corpus alone (RFT) and AlphaVerus, which                    all possible inputs and outputs to the function. Unlike unit-
relies on the same seed corpus but without self-play.                   tests, which are hard for LLMs to generate and vulnerable
                                                                        to reward hacking (Yang et al., 2025a; Baker et al., 2025),
We show that PSV-V ERUS’s performance scales with the
                                                                        formal verification provides a binary guarantee of correct-
number of iterations and generated questions, and empiri-
                                                                        ness. This makes the setting attractive for safety-critical
cally identify that verification of solutions and the difficulty-
                                                                        domains (Klein et al., 2014) and for self-improving AI that
awareness and diversity of the proposal are key factors for
                                                                        requires verification of novel questions. Recently devel-
self-play. Coupled with recent successes in formal theorem
                                                                        oped formal verification languages such as Verus (Lattuada
proving (Dong & Ma, 2025), our work points to formal
                                                                        et al., 2023) bring SMT-backed proofs into mainstream sys-
verification as a promising frontier for LLM self-play. In
                                                                        tems languages such as Rust, making formal verification
summary, our contributions are as follows:
                                                                        possible in real world, modern programming domains. A
                                                                        key obstacle to model performance on these tasks is data
                                                                        scarcity (Aggarwal et al., 2024), which makes synthetic
  1. We introduce P ROPOSE , S OLVE , V ERIFY (PSV), a                  corpus generation under formal verifier feedback especially
     self-play algorithm for code generation that leverages             promising.
     formal verification, and propose a difficulty-aware pro-
                                                                             1
     poser based on in-context learning.                                         https://github.com/abwilf/psv

                                                                    2
                                     Propose, Solve, Verify: Self-Play Through Formal Verification


                          fn has_z(...                                                                     ✅✅✅❌              Easy
                                                                       for i...


       Propose            fn is_odd(...            Solve               let m...
                                                                                          Verify          ✅❌✅❌               Medium

                          fn mod(...                                                                       ✅❌❌❌              Hard
                                                                       if a...
                               ...                                       ...                                         ...



Figure 3: P ROPOSE , S OLVE , V ERIFY (PSV) is an iterative self-play approach for formally verified code generation. At
each iteration t, the solver Sθt attempts to solve the current set of specifications xi,t , producing candidate solutions that are
checked using formal verification, which mathematically guarantees their correctness. Verified solutions are used to update
the solver via rejection fine-tuning (RFT), while a proposer Pϕ,t generates new, challenging specifications using the pass
rate (how many candidate solutions passed verification for each problem) as a proxy for what kinds of problems the solver
Sθt finds difficult.


Self-improving AI systems. Self-play game playing al-                   3. P ROPOSE , S OLVE , V ERIFY (PSV)
gorithms such as AlphaZero have shown that AI systems
can surpass human performance without human labels (Sil-                P ROPOSE , S OLVE , V ERIFY (PSV) leverages a formal ver-
ver et al., 2017). Yet porting this paradigm to language, in            ifier to enable a self-play loop. The core idea is to iterate
particular reasoning, has been challenging: the action space            between proposing specifications, attempting to solve the
is vast and verifiers are often weak instead of determinis-             specifications, and using the formal verifier’s feedback to
tic (e.g., the rules of the game define a win/loss). Recent             improve the solver and inform the next round of problem
work has made progress on self-improving language mod-                  proposal. Over time the solver trains with an evolving pool
els with rejection-finetuning (Singh et al., 2024; Zelikman             of challenging and diverse problems, yielding improvements
et al., 2022) and reinforcement learning from verifiable re-            in the solver’s capabilities. We describe each component in
wards (RLVR) (Shao et al., 2024; DeepSeek-AI et al., 2025;              detail below.
Wen et al., 2025) on fixed human-generated datasets. Yet
human-generated reasoning datasets are limited and diffi-
cult to scale (Liu et al., 2025), motivating the creation of            Problem setting. We consider the problem of verified
synthetic data for training reasoning capabilities.                     code generation. In this problem, the input is a formal spec-
                                                                        ification x ∈ X , and the output is code y ∈ Y. A verifier
                                                                        v(x, y) → {0, 1} checks whether the code meets the formal
                                                                        specification. If so, the verifier returns 1 and otherwise it re-
                                                                        turns 0. The specification and code are written in a language
Self-play reasoning systems Self-play systems leverage                  that supports verification, such as Verus (Lattuada et al.,
an intuition that there is a “gap” between what AI can solve            2023) which supports verification for a subset of Rust code,
and verify (Song et al., 2024), meaning that systems could              or Dafny (Leino, 2010). The code y contains an implemen-
self-improve by proposing novel problems and verifiers                  tation and any additional proof code (e.g., “loop invariants”)
and training a “solver” model on verified solutions. This               that is necessary for the program to pass the verifier. Given
has been applied to reasoning games (Cheng et al., 2025b),              a specification x, the goal is to produce code y that passes
code (Rozière et al., 2023; Wei et al., 2024; Haluptzok et al.,        the verifier, v(x, y) = 1. The key property that we leverage
2023), and math (Shah et al., 2024). A recent line of work              is that the Verus verifier is sound with respect to specifi-
has also proposed recursively self-improving, by training               cations, i.e., if v(x, y) = 1 then the program y meets the
the question proposer as well to output difficult problems              specification x. See Appendix F for additional background.
for the current solver (Li et al., 2024; Huang et al., 2025).           While we consider formally verified code generation here,
This has been applied to formal math (Dong & Ma, 2025),                 in principle our methods apply to any problem with a sound
coding (Zhao et al., 2025; Lin et al., 2025), tool use (Zhou            verifier, i.e., if the verifier v(x, y) returns 1, then y is a
et al., 2025), alignment (Cheng et al., 2025a; Zhu et al.,              correct output for problem x. Applying PSV to other such
2025), and general language tasks (Kuba et al., 2025). As               problems is left for future work.
strong verifiers are important to self-play (yet often limited
in applicability) (Saad-Falcon et al., 2025), we investigate
                                                                        3.1. P ROPOSE , S OLVE , V ERIFY (PSV)
the verified coding domain in Verus (Lattuada et al., 2023)
where SMT-backed verification provides a sound guarantee                PSV is an algorithm that runs for iterations t ∈ {1 . . . T }
over a Turing-complete language (Rust).                                 and consists of a proposer model Pϕt and a solver model

                                                                   3
                                    Propose, Solve, Verify: Self-Play Through Formal Verification

Sθt , working together to generate and solve new problems,                 We then trim Dt∗ to keep a maximum of one solution to each
                                                                                                                             j
supervised with help from the verifier.                                    problem i if there are multiple values of j s.t. vi,t = 1. The
                                                                           solver is then updated by minimizing the cross-entropy loss:
At the first iteration (t = 0), PSV receives a set of seed prob-
lem specifications Xt = {x1 , x2 , . . . , xN0 }, and the solver
                                                                                                            j
attempts to solve them. That is, given a specification xi                                                 |yi |
                                                                                     1           X        X
the solver produces candidate outputs yi,t 1            ktrn
                                             , . . . , yi,t  , where        L(θ) = − ∗                            log pθ (yij [k] | xi , yij [< k])
                                                                                    |Dt |
ktrn is a hyperparameter governing the number of solver                                      (xi ,yij )∈Dt∗ k=1
attempts per specification. Each output has an associated
                          j
verification outcome vi,t    ∈ {0, 1} obtained by running the
                    j
                                                                           where θ is initialized from θ0 , yij [k] is the k-th token of
verifier on xi , yi,t . Over all specifications x ∈ Xt , this              solution yij , and yij [< k] denotes all preceding tokens.
yields a data pool Dt = (Xt , Yt , Vt ).                                   Iteratively training on verified solutions in this way can
The solver is then trained using the data pool, yielding a                 be seen as an offline RL algorithm based on expectation-
new solver Sθt+1 . Finally, the proposer Pϕt is updated                    maximization (Singh et al., 2024). Further details about
using the data pool and is used to generate a new set of                   SFT training can be found in Appendix E.
B specifications that are added to the existing set, so that               In principle, different reinforcement learning algorithms
Xt+1 = Xt ∪ {xNt +1 , xNt +2 , . . . , xNt +B }. The process               could have been used, such as GRPO (Shao et al., 2024).
iterates for a fixed number of iterations T .                              We use RFT because the Verus verifier is guaranteed to be
Next, we describe the specific design choices for the solver,              sound but not complete, meaning that advantage-weighted
learning algorithm, and proposer that we use in our experi-                algorithms could incorrectly punish models for correct so-
ments, including our difficulty-aware proposer. We summa-                  lutions that were judged to be incorrect. Future work on
rize PSV in Algorithm 1.                                                   on-policy RL algorithms for formally verified self-play may
                                                                           investigate more performant RL algorithms in this setting.
Algorithm 1 P ROPOSE , S OLVE , V ERIFY (PSV)
Require: Seed specifications X0 , solver Sθ0 , proposer Pϕ0 ,              Proposing. At iteration t, proposer Pϕ,t generates B new
  question budget B, verifier V , number of iterations T                   problem specs at target difficulty levels by conditioning on
  for t = 0 to T − 1 do                                                    problems and associated difficulty labels. We estimate the
    {Yt , Vt } ← S OLVE(Sθt , Xt , V )                                     difficulty of question xi at iteration t by the current solver’s
    Dt ← (Xt , Yt , Vt )                                                   pass rate on that problem:
    Sθt+1 ← T RAIN(Sθ0 , Dt )
    Pϕt+1 ← U PDATE(Pϕ0 , Dt )                                                                               ktrn
    Xt+1 ← Xt ∪ P ROPOSE(Pϕt+1 , Dt )                                                                      1 X          j
                                                                                                ri,t =                 vi,t
  end for                                                                                                ktrn j=1


Solving. At each iteration t, PSV produces candidate so-                   We categorize problems into one of four classes based on
lutions for each xi ∈ Xt by sampling from the solver model                 ri,t : E ASY, M EDIUM, H ARD, and I MPOSSIBLE:
Sθt with temperature 0.8, yielding ktrn candidate solutions
            1             ktrn
for each: yi,t , . . . , yi,t  , along with binary verification out-                              
                       ktrn
                                                                                                    E ASY                 if ri,t ≥ τE
         1
                                                                                                  
comes vi,t , . . . , vi,t . We follow AlphaVerus’s few shot
                                                                                                  
                                                                                                  
                                                                                                  M EDIUM                if τM ≤ ri,t < τE
prompting setup (Aggarwal et al., 2024) with a 1-shot exam-                  difficulty(xi , t) =
ple. We found that while increasing the number of few-shot
                                                                                                  
                                                                                                  
                                                                                                   H ARD                 if 0 < ri,t < τM
                                                                                                                          if ri,t = 0,
                                                                                                  
examples improved performance, it also increased runtime                                            I MPOSSIBLE
substantially because solving is the most computationally
intensive part of the pipeline, and the method was improving               where the thresholds τE and τM are hyperparameters for
without more few-shot examples.                                            our method.

Rejection-Finetuning. The solver is updated through re-                    We then sample kprop problems from Dt to use as exam-
jection fine-tuning (RFT) (Singh et al., 2024), where the                  ples and ask the proposer to output a question at a target
base model is fine-tuned only on verified solutions. For-                  difficulty level. A simplified version of our prompt is below,
mally, we construct the training data for a single iteration of            and the complete prompt is in Appendix A. This mechanism
RFT as                                                                     continually refreshes the prompt distribution, updating the
                  n                              o                         proposer to Pϕ,t+1 through in-context learning and expand-
                          j                j
           Dt∗ ← (xi , yi,t  ) : i ∈ Dt , vi,t =1                          ing the problem frontier in a difficulty-controlled manner.

                                                                       4
                                Propose, Solve, Verify: Self-Play Through Formal Verification

Table 1: Test-Time Training and Transfer Learning Results. Values show mean pass@k rates with standard errors as
subscripts across 5 random seeds. Best results (statistically significant via paired t-test, p < 0.05) are bolded.

                            Dafny2Verus                              MBPP                                  HumanEval
 Method          pass@1       pass@5    pass@10       pass@1         pass@5       pass@10      pass@1       pass@5   pass@10
 Inference Only
 AlphaVerus     24.060.16    52.420.21   63.440.29    6.480.29       18.360.72    24.571.02    7.240.10     15.380.36    18.020.54
 Transfer Learning
 RFT               —             —           —        10.991.10      26.031.05    31.190.79    10.990.45    18.070.50    20.020.54
 PSV-V ERUS        —             —           —        25.252.24      38.321.80    41.511.60    16.181.30    21.611.50    23.132.06
 Test-Time Training
 RFT            34.462.29    57.121.86   63.401.06    3.830.19       14.560.60    22.641.04     5.560.41    12.460.35    14.800.34
 PSV-V ERUS 65.631.70        78.042.31   80.062.35    36.782.45      51.221.65    53.671.49    19.071.02    23.421.20    25.161.47


    Proposer In-Context Learning                                    dependencies are preserved. All datasets require generating
                                                                    Rust+Verus code that passes the Verus verifier (Lattuada
    I would like you to output a problem that is                    et al., 2023). We will omit the *-Verified from the names
    of {difficulty} level. Here are some examples
                                                                    for brevity throughout the rest of the paper. We adopt the
    of problems and how difficult they were for
    the model.                                                      widely used Pass@k metric (Chen et al., 2021): for n sam-
                                                                    ples and c verified successes, pass@k = 1 − n−c          n
                                                                                                                               
                                                                                                                       k / k .
    Problem 1: EASY
                                                                    We measure Pass@1, 5, and 10, and run our final evaluation
    {problem spec}
    Problem 2: HARD                                                 with n = 100 to provide a strong unbiased estimate of the
    {problem spec}                                                  evaluation metrics.
    ...
    Now it’s your turn! Please describe your                        Settings. We study our method’s performance in two set-
    reasoning, then output a new problem that is                    tings. In a setting we refer to as transfer learning we set
    {difficulty}.                                                   X0 to the set of questions in Dafny2Verus and report perfor-
                                                                    mance on MBPP and HumanEval as a held out test set. In a
After inference, specifications are parsed, deduplicated, and       setting that we refer to as test-time training (TTT) (Sun et al.,
filtered through a spec verifier which ensures that the spec        2020), we set X0 to the set of questions in each dataset, and
defines a valid set of mathematical pre- and post-conditions.       run our method on that dataset alone. It is worth noting that
This uses a form of Verus that ignores the implementation           human-written solutions are never trained on.
body – details are in Appendix D.
                                                                    Baselines. We compare to AlphaVerus (Aggarwal et al.,
4. Experiments                                                      2024) (no treefinement version), which is the previous SOTA
                                                                    method for verified code generation based on prompting
We study self-play verified code generation in the Verus            with 50 in-domain exemplars. We also compare to iterative
language (Lattuada et al., 2023).                                   RFT (Yuan et al., 2023; Singh et al., 2024), which performs
                                                                    expert iteration without proposing new problems. We train
Datasets and evaluation. We evaluate our approach                   and evaluate RFT with the same parameters as our method,
using three Verus datasets. Dafny2Verus (274 prob-                  excluding any parameters related to question proposal.
lems) is a translation-derived corpus adapted from the Al-
phaVerus (Aggarwal et al., 2024) pipeline, providing a di-          Hyperparameters and design choices. Our hyperparam-
verse set of formally verified Dafny problems translated into       eters and design choices were selected to provide a proof
Verus. MBPP-Verified (78 problems) is based on the MBPP             of concept of our idea at minimal compute scale. In the
dataset (Austin et al., 2021), following the verified adapta-       current setting, the main experiment (Table 1) takes around
tion process described in (Yang et al., 2025a; Misu et al.,         24 hours on a single machine with 8xL40s GPUs. We use
2024), where each task includes executable Rust+Verus               the Qwen2.5-Coder-3B-Instruct model as our base because
specifications and proofs. HumanEval-Verified (85 func-             it was the strongest open-weight code model at the 3B size.
tions across 49 original programs) is drawn from an open-           We use SGLang (Zheng et al., 2024) with dp-size=8 and
source HumanEval-Verus effort (Contributors, 2024), which           temperature 0.8 for all inference sampling because SGLang
translates Python HumanEval tasks (Chen et al., 2021) into          has large efficiency gains for inference time sampling and
Verus. Each multi-function program is decomposed into               can parallelize over multiple GPUs on the same machine
independently verifiable functions, ensuring all necessary          easily. We set τM to 0.2, similar to Dong & Ma (2025) (who

                                                                5
                                Propose, Solve, Verify: Self-Play Through Formal Verification




Figure 4: PSV-V ERUS performance across three test-time training tasks, plotting Pass@1, 5, and 10 across iterations of the
algorithm, with clouds representing ± 1 standard deviation across 5 random seeds.


used 0.25), and set τE to 0.8. We set ktrn to 10 to balance         metrics, PSV-V ERUS obtains 48.12%, compared to 25.43%
having enough breadth in our search to enable performance           for RFT and 25.55% for AlphaVerus, representing mean im-
improvements and not so much that the computational re-             provements of 1.89× and 1.88×, respectively. Performance
quirements would become unreasonable to reproduce. We               graphs for each task are in Figure 4, where the trends of
use kprop = 12 and use uniform input and output targets,            improving over iterations become clear.
meaning that we populate the proposer prompt with 3 prob-
lems for each difficulty class, and ask for B/4 problems of         6. Analyses and Ablations
each difficulty class as the output. We justify the choice of
uniform input/targets in Appendix B, and vary the number            In the sections that follow, we investigate how our method
of iterations T and proposer budget B in our analysis (§ 6).        scales with the number of generated questions (§6.1) and
                                                                    iterations of the algorithm when the number of proposed
5. Results                                                          questions is held constant (§6.2) – experiments that artic-
                                                                    ulate the scaling properties of our method with respect to
We investigate PSV-V ERUS’s performance on our two ex-              increasing compute. We also analyze the importance of for-
perimental settings: transfer learning and test-time train-         mal verification and factors impacting the effectiveness of
ing. Table 1 presents our main results on three benchmarks:         the question proposal through ablation experiments in §6.3
Dafny2Verus, MBPP-Verified, and HumanEval-Verified.                 to better understand their impact on self-play performance.
PSV-V ERUS consistently outperforms both the AlphaVerus
and the RFT baselines across all metrics.                           6.1. Scaling with Questions Per Iteration
                                                                    The first scaling factor we consider is the number of ques-
Transfer learning PSV-V ERUS achieves strong cross-                 tions per iteration B, because it can be scaled in parallel
domain generalization, scoring 25.25% pass@1 on MBPP                across many machines simultaneously without any blocking
and 16.18% on HumanEval, outperforming AlphaVerus                   factors. Results for the test-time training setting are shown
(6.48%, 7.24%) and RFT (10.99%, 10.99%) by 3.90× and                in Figure 5.
2.30× on MBPP and 2.24× and 1.47× on HumanEval,
respectively. These results demonstrate that training on            On Dafny2Verus, scaling from 4k to 32k questions per itera-
Dafny2Verus generalizes robustly across domains, yielding           tion yields consistent improvements: pass@1 increases from
substantial gains on realistic natural-language programming         59.5% to 74.3% (+25% relative), pass@5 from 73.8% to
benchmarks.                                                         82.6% (+12%), and pass@10 from 75.8% to 83.6% (+10%).
                                                                    On MBPP, scaling from 1k to 32k questions yields pass@1
                                                                    improvements from 22.3% to 44.3% (+98%), pass@5 from
Test-time training On Dafny2Verus pass@1, PSV-                      39.7% to 57.8% (+46%), and pass@10 from 44.8% to
V ERUS achieves 65.63%, compared to AlphaVerus’s 24.06%             61.1% (+36%). HumanEval shows similar gains: pass@1
(a 2.73× improvement) and RFT’s 34.46% (a 1.90× im-                 from 13.9% to 26.3% (+89%), pass@5 from 16.4% to
provement). On MBPP pass@1, PSV-V ERUS reaches                      32.6% (+99%), and pass@10 from 17.9% to 34.5% (+93%).
36.78%, outperforming AlphaVerus’s 6.48% (5.68×) and                We also observe positive scaling behavior for transferring
RFT’s 3.83% (9.61×), and on HumanEval pass@1, PSV-                  from Dafny2Verus to MBPP, though more modest gains for
V ERUS achieves 19.07%, compared to AlphaVerus’s 7.24%              transferring to HumanEval; see Appendix C.
(2.63×) and RFT’s 5.56% (3.43×). On Dafny2Verus
pass@10, PSV-V ERUS outperforms RFT by 1.26× and
AlphaVerus by 1.26×. Averaged across all benchmarks and

                                                                6
                                 Propose, Solve, Verify: Self-Play Through Formal Verification




 Figure 5: Test-time training performance scales with the number of questions per iteration across all three benchmarks.


                                                                      at 4k, from 28.0% to 46.9% (+68%). This effect extends
                                                                      beyond pass@1: at the 4k budget level, pass@5 improves
                                                                      from 50.6% to 62.9% (+24%), and pass@10 improves from
                                                                      60.0% to 66.7% (+11%). In summary, holding the number
                                                                      of proposed specifications constant, increasing the num-
                                                                      ber of iterations boosts success rates, showing that iterative
                                                                      training drives performance improvements in our method.

                                                                      6.3. Ablations
                                                                      Our self-play algorithm PSV-V ERUS has three key compo-
                                                                      nents worth examining through ablation analyses – a verifier
                                                                      that determines whether specs and solutions are correct, and
                                                                      a proposer that outputs diverse solutions by sampling ques-
                                                                      tions to put in the proposer prompt from the ever-growing
Figure 6: Given a fixed total question budget (1, 2, or 4k            dataset and that outputs questions of target difficulty by
questions) spread across differing numbers of iterations,             computing and including labels of how difficult questions
we find that running PSV-V ERUS with more iterations im-              included in the prompt were for the most recent solver. We
proves performance. This plot depicts the final Dafny2Verus           decided to ablate each of these components and observe
pass@1 result for different question budgets across number            their effect on performance in the transfer learning setting.
of total iterations used. For example, the 1k line at the first       Our results are in Table 2 and described below in detail.
tick mark on the x-axis means that 1000 questions were
generated then trained on once, whereas at the last tick mark
200 questions were generated per iteration, separated by              Verification The Verus verifier is used primarily in our
updating the solver and proposer.                                     algorithm to check whether solutions are valid for a given
                                                                      spec before training on them. We analyze the impact of this
                                                                      by ablating this step and training on all generated solutions,
6.2. Iterative Training                                               ignoring the verification signal. Our results are shown in
                                                                      Table 2 under (-Verification). We find that removing solu-
Next, we are interested in whether the proposer’s budget of
                                                                      tion verification hurts performance significantly, leading to
generated specifications (i.e., the question budget) should
                                                                      relative drops in performance of 51.5% pass@1 and 29.3%
be allocated towards increasing the number of iterations of
                                                                      pass@5 for Dafny2Verus, 55.2% and 35.7% for MBPP,
the method or increasing the number of generated specifica-
                                                                      and 52.1% and 33.5% for HumanEval.
tions per iteration. We fix the question budget and vary the
number of iterations. Figure 6 illustrates a smooth, mono-            In addition to performance gains, we also find that verifica-
tonic improvement as the number of iterations increase.               tion can be useful for efficiency. We also use verification
That is, distributing a fixed question budget across multi-           to filter out candidate specs to make sure they are syntacti-
ple of iterations proposing, solving, and updating yields             cally compilable before attempting inference on them. This
better results than a single large iteration. For example, in         impacts efficiency only, not performance, because the syn-
the test-time-training setting on Dafny2Verus at a 1k bud-            tactically invalid specs are 100% not solvable, therefore
get, increasing iterations from 1 to 5 boosts pass@1 from             no solution can impact training. We ablated this step and
21.0% to 42.3% (+102%). The pattern holds at higher bud-              found that the efficiency hit from removing spec verification
gets: at 2k, pass@1 rises from 26.3% to 44.3% (+68%);                 is substantial: only 47.7% of unique specs were valid on

                                                                  7
                                 Propose, Solve, Verify: Self-Play Through Formal Verification

Table 2: Ablation Study. We find that verification of the solution, difficulty-aware proposal prompting, and diversity through
proposal context sampling are important to self-play performance. These results report mean pass@k with standard deviation
subscripts across 5 seeds.

                        Dafny2Verus                      MBPP                        HumanEval
                 pass@1 pass@5 pass@10 pass@1 pass@5 pass@10 pass@1 pass@5 pass@10 Avg
PSV-V ERUS 65.631.70 78.042.31 80.062.35 25.252.24 38.321.80 41.511.60 16.181.30 21.611.50 23.132.06 43.31
  -Verification 31.821.42 55.211.26 60.691.52 11.311.46 24.661.86 28.862.44 7.750.71 14.380.72 16.390.92 27.90
  -Difficulty 60.162.67 74.983.66 77.733.45 23.031.51 36.251.56 39.731.55 13.831.12 20.171.08 21.921.14 40.87
  -Diversity    54.951.43 71.461.15 74.190.86 20.281.04 34.132.16 37.662.04 14.250.82 20.040.74 21.400.93 38.71


average, so removing spec verification meant that we had               ple diversity: PSV-V ERUS achieves a higher uniqueness
to perform pass@10 inference on the remaining 52.3% of                 rate on average (45.3% vs 29.3%), which leads to 2.48×
specs that were not solvable, a 2.1x increase in inference             more unique questions, and 2.26× more solvable questions
compute with no resulting performance improvement.                     used for training the solver, enabling the model to learn
                                                                       from a broader distribution of verified solutions.
Difficulty-awareness We experiment with removing the
difficulty awareness of our proposer by removing the la-               7. Conclusion
bels for the sampled questions in the proposer prompt. The
prompt form is detailed in Appendix G. We found that                   This work set out to investigate a central obstacle to
this -Difficulty ablation causes an average drop of 5.6%               proposer-solver self-play algorithms for language models:
across all metrics. Table 2 shows per-dataset comparisons:             obtaining a reliable reward signal that prevents error propa-
the drop is statistically significant for 6 of 9 dataset/metric        gation and reward hacking. While prior self-play successes
combinations (paired t-test, p < 0.05). Notably, all three             have largely been confined to domains with trivial or limited-
Dafny2Verus metrics show significant drops, while some                 applicability verifiers, we showed that formal verification
HumanEval and MBPP comparisons do not reach signifi-                   in a Turing-complete coding language enables self-play in
cance (MBPP pass@1, HumanEval pass@5,10).                              a realistic code-generation setting by providing a sound,
                                                                       non-exploitable training signal. By introducing PSV and
To understand why, we analyze whether the proposer suc-                applying it successfully to verified Rust programming, we
cessfully generates questions at the target difficulty. For            demonstrated that a model can autonomously expand its
PSV-V ERUS, easy-targeted questions have mean pass rate                training curriculum beyond human-written data and steadily
0.55 (std 0.47), medium-targeted questions have mean 0.45              improve its capabilities without human supervision. We
(std 0.42), and hard-targeted questions have mean 0.36 (std            show that our algorithm displays smooth scaling behavior
0.39). The different means but substantial overlap between             with respect to the number of generated questions (§6.1)
distributions indicates that difficulty prompting provides             and iterations (§6.2), making it an exciting first step in un-
partial but incomplete control over generated question                 derstanding the limits of scaling for self-play reasoning
difficulty. It seems that difficulty-aware prompting provides          training. In analyzing key components of our algorithm’s
a modest benefit despite its imperfect control over gener-             design, we observe the importance of formal verification
ated question difficulty – an area that future work may find           and difficulty-aware and diverse question proposal (§6.3) in
fruitful to improve upon.                                              making self-play performant.

Diversity We experiment with limiting the diversity of the             Acknowledgments
generated questions by ablating the constantly refreshing
proposer prompt with a fixed proposer prompt. We construct             This work was also supported in part by the National
this by sampling only once from the seed dataset to get                Science Foundation under Grant Nos. DMS-2434614 and
our in-context examples, similar to the fixed prompt in self-          DMS2502281, the Future Enterprise Security initiative at
instruct pipelines such as Rozière et al. (2023). This ablation       Carnegie Mellon CyLab (FutureEnterprise@CyLab), and
causes an average drop of 10.6% across all metrics. Table 2            AFRL and DARPA under Agreement FA8750-24-9-1000,
show the full results: all Dafny2Verus and MBPP metrics                and by gifts from Amazon, Convergent Research, Microsoft,
show significant drops (pass@1 drops of 16.3% and 19.7%                VMware, and the Beneficial AI Foundation.
respectively), while HumanEval pass@5 and pass@10 are
lower but do not reach significance.
The mechanism behind this improvement is increased sam-

                                                                   8
                                Propose, Solve, Verify: Self-Play Through Formal Verification

Impact Statement                                                    Contributors, T. H.-V. Humaneval-verus: Hand-written
                                                                      examples of verified verus code derived from humaneval.
We believe this work could help usher in a future of self-            https://github.com/secure-foundations/
improving models through self-play. This comes with ethi-             human-eval-verus.git, 2024.
cal concerns, but so too does it have the potential to enable
a more equitable future where reasoning can emerge in               DeepSeek-AI, Guo, D., Yang, D., Zhang, H., Song, J.,
many domains—more dependent on the properties of the                  Zhang, R., Xu, R., Zhu, Q., Ma, S., Wang, P., Bi, X.,
generation-verification gap in that domain than on the capa-          Zhang, X., Yu, X., Wu, Y., Wu, Z. F., Gou, Z., Shao, Z.,
bility to collect costly human reasoning traces (a capability         Li, Z., Gao, Z., Liu, A., Xue, B., Wang, B., Wu, B., Feng,
usually only the highly resourced possess).                           B., Lu, C., Zhao, C., Deng, C., Zhang, C., Ruan, C., Dai,
                                                                      D., Chen, D., Ji, D., Li, E., Lin, F., Dai, F., Luo, F., Hao,
                                                                      G., Chen, G., Li, G., Zhang, H., Bao, H., Xu, H., Wang,
References
                                                                      H., Ding, H., Xin, H., Gao, H., Qu, H., Li, H., Guo, J.,
Aggarwal, P., Parno, B., and Welleck, S. AlphaVerus: Boot-            Li, J., Wang, J., Chen, J., Yuan, J., Qiu, J., Li, J., Cai,
  strapping Formally Verified Code Generation through                 J. L., Ni, J., Liang, J., Chen, J., Dong, K., Hu, K., Gao,
  Self-Improving Translation and Treefinement, December               K., Guan, K., Huang, K., Yu, K., Wang, L., Zhang, L.,
  2024. URL https://arxiv.org/abs/2412.06176v1.                       Zhao, L., Wang, L., Zhang, L., Xu, L., Xia, L., Zhang,
                                                                      M., Zhang, M., Tang, M., Li, M., Wang, M., Li, M., Tian,
Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski,               N., Huang, P., Zhang, P., Wang, Q., Chen, Q., Du, Q., Ge,
  H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q., and           R., Zhang, R., Pan, R., Wang, R., Chen, R. J., Jin, R. L.,
  Sutton, C. Program synthesis with large language models,            Chen, R., Lu, S., Zhou, S., Chen, S., Ye, S., Wang, S., Yu,
  2021. URL https://arxiv.org/abs/2108.07732.                         S., Zhou, S., Pan, S., Li, S. S., Zhou, S., Wu, S., Ye, S.,
                                                                     Yun, T., Pei, T., Sun, T., Wang, T., Zeng, W., Zhao, W.,
Baker, B., Huizinga, J., Gao, L., Dou, Z., Guan, M. Y.,
                                                                      Liu, W., Liang, W., Gao, W., Yu, W., Zhang, W., Xiao,
  Madry, A., Zaremba, W., Pachocki, J., and Farhi, D.
                                                                     W. L., An, W., Liu, X., Wang, X., Chen, X., Nie, X.,
  Monitoring reasoning models for misbehavior and the
                                                                      Cheng, X., Liu, X., Xie, X., Liu, X., Yang, X., Li, X., Su,
  risks of promoting obfuscation, 2025. URL https:
                                                                      X., Lin, X., Li, X. Q., Jin, X., Shen, X., Chen, X., Sun,
  //arxiv.org/abs/2503.11926.
                                                                      X., Wang, X., Song, X., Zhou, X., Wang, X., Shan, X.,
Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. d. O.,          Li, Y. K., Wang, Y. Q., Wei, Y. X., Zhang, Y., Xu, Y., Li,
  Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brock-             Y., Zhao, Y., Sun, Y., Wang, Y., Yu, Y., Zhang, Y., Shi,
  man, G., Ray, A., Puri, R., Krueger, G., Petrov, M.,               Y., Xiong, Y., He, Y., Piao, Y., Wang, Y., Tan, Y., Ma,
  Khlaaf, H., Sastry, G., Mishkin, P., Chan, B., Gray, S.,           Y., Liu, Y., Guo, Y., Ou, Y., Wang, Y., Gong, Y., Zou,
  Ryder, N., Pavlov, M., Power, A., Kaiser, L., Bavarian,            Y., He, Y., Xiong, Y., Luo, Y., You, Y., Liu, Y., Zhou, Y.,
  M., Winter, C., Tillet, P., Such, F. P., Cummings, D.,              Zhu, Y. X., Xu, Y., Huang, Y., Li, Y., Zheng, Y., Zhu,
  Plappert, M., Chantzis, F., Barnes, E., Herbert-Voss, A.,          Y., Ma, Y., Tang, Y., Zha, Y., Yan, Y., Ren, Z. Z., Ren,
  Guss, W. H., Nichol, A., Paino, A., Tezak, N., Tang,                Z., Sha, Z., Fu, Z., Xu, Z., Xie, Z., Zhang, Z., Hao, Z.,
  J., Babuschkin, I., Balaji, S., Jain, S., Saunders, W.,             Ma, Z., Yan, Z., Wu, Z., Gu, Z., Zhu, Z., Liu, Z., Li, Z.,
  Hesse, C., Carr, A. N., Leike, J., Achiam, J., Misra,               Xie, Z., Song, Z., Pan, Z., Huang, Z., Xu, Z., Zhang, Z.,
  V., Morikawa, E., Radford, A., Knight, M., Brundage,                and Zhang, Z. DeepSeek-R1: Incentivizing Reasoning
  M., Murati, M., Mayer, K., Welinder, P., McGrew, B.,                Capability in LLMs via Reinforcement Learning, Jan-
  Amodei, D., McCandlish, S., Sutskever, I., and Zaremba,             uary 2025. URL http://arxiv.org/abs/2501.12948.
  W. Evaluating Large Language Models Trained on Code,                arXiv:2501.12948 [cs].
  July 2021. URL http://arxiv.org/abs/2107.03374.                   Dong, G., Lu, K., Li, C., Xia, T., Yu, B., Zhou, C.,
  arXiv:2107.03374 [cs].                                              and Zhou, J. Self-play with execution feedback: Im-
Cheng, J., Liu, X., Wang, C., Gu, X., Lu, Y., Zhang, D.,              proving instruction-following capabilities of large lan-
  Dong, Y., Tang, J., Wang, H., and Huang, M. Spar: Self-             guage models. In The Thirteenth International Confer-
  play with tree-search refinement to improve instruction-            ence on Learning Representations, 2025. URL https:
  following in large language models, 2025a. URL https:              //openreview.net/forum?id=cRR0oDFEBC.
  //arxiv.org/abs/2412.11605.                                       Dong, K. and Ma, T. STP: Self-play LLM Theorem Provers
                                                                      with Iterative Conjecturing and Proving, January 2025.
Cheng, P., Hu, T., Xu, H., Zhang, Z., Yuan, Z., Dai, Y.,              URL https://arxiv.org/abs/2502.00212v4.
  Han, L., Du, N., and Li, X. Self-playing adversarial
  language game enhances llm reasoning, 2025b. URL                  Haluptzok, P., Bowers, M., and Kalai, A. T. Language
  https://arxiv.org/abs/2404.10642.                                   models can teach themselves to program better. In The

                                                                9
                               Propose, Solve, Verify: Self-Play Through Formal Verification

  Eleventh International Conference on Learning Represen-          Luo, Z., Xu, C., Zhao, P., Sun, Q., Geng, X., Hu, W., Tao, C.,
  tations, 2023. URL https://openreview.net/forum?                   Ma, J., Lin, Q., and Jiang, D. WizardCoder: Empowering
  id=SaRj2ka1XZ3.                                                    Code Large Language Models with Evol-Instruct, June
                                                                     2023. URL https://arxiv.org/abs/2306.08568v2.
Huang, C., Yu, W., Wang, X., Zhang, H., Li, Z., Li, R.,
  Huang, J., Mi, H., and Yu, D. R-Zero: Self-Evolving Rea-         Misu, M. R. H., Lopes, C. V., Ma, I., and Noble, J. To-
  soning LLM from Zero Data, August 2025. URL http:                 wards ai-assisted synthesis of verified dafny methods.
 //arxiv.org/abs/2508.05004. arXiv:2508.05004 [cs].                 Proc. ACM Softw. Eng., 1(FSE), July 2024. doi: 10.1145/
                                                                    3643763. URL https://doi.org/10.1145/3643763.
Klein, G., Andronick, J., Elphinstone, K., Murray, T.,
                                                                   Rice, H. G. Classes of recursively enumerable sets and
  Sewell, T., Kolanski, R., and Heiser, G. Comprehen-
                                                                     their decision problems. Transactions of the American
  sive formal verification of an OS microkernel. ACM
                                                                     Mathematical Society, 74(2):358–366, 1953. doi: 10.
  Trans. Comput. Syst., 32(1):2:1–2:70, February 2014.
                                                                     1090/S0002-9947-1953-0053041-6.
  ISSN 0734-2071. doi: 10.1145/2560537. URL https:
  //dl.acm.org/doi/10.1145/2560537.                                Rozière, B., Gehring, J., Gloeckle, F., Sootla, S., Gat, I.,
                                                                     Tan, X. E., Adi, Y., Liu, J., Sauvestre, R., Remez, T.,
Kuba, J. G., Gu, M., Ma, Q., Tian, Y., and Mohan, V.                 Rapin, J., Kozhevnikov, A., Evtimov, I., Bitton, J., Bhatt,
  Language Self-Play For Data-Free Training, Septem-                 M., Ferrer, C. C., Grattafiori, A., Xiong, W., Défossez,
  ber 2025. URL http://arxiv.org/abs/2509.07414.                     A., Copet, J., Azhar, F., Touvron, H., Martin, L., Usunier,
  arXiv:2509.07414 [cs].                                             N., Scialom, T., and Synnaeve, G. Code Llama: Open
                                                                     Foundation Models for Code, August 2023. URL https:
Lattuada, A., Hance, T., Cho, C., Brun, M., Subasinghe,              //arxiv.org/abs/2308.12950v3.
  I., Zhou, Y., Howell, J., Parno, B., and Hawblitzel, C.
  Verus: Verifying rust programs using linear ghost types.         Saad-Falcon, J., Buchanan, E. K., Chen, M. F., Huang, T.-H.,
  Proceedings of the ACM on Programming Languages, 7                 McLaughlin, B., Bhathal, T., Zhu, S., Athiwaratkun, B.,
  (OOPSLA1):286–315, 2023.                                           Sala, F., Linderman, S., et al. Shrinking the generation-
                                                                     verification gap with weak verifiers. arXiv preprint
Leino, K. R. M. Dafny: An automatic program verifier for             arXiv:2506.18203, 2025.
  functional correctness. In Proceedings of the Conference
  on Logic for Programming, Artificial Intelligence, and           Shah, V., Yu, D., Lyu, K., Park, S., Yu, J., He, Y., Ke, N. R.,
  Reasoning (LPAR), 2010.                                            Mozer, M., Bengio, Y., Arora, S., and Goyal, A. AI-
                                                                     Assisted Generation of Difficult Math Questions, July
Li, Q., Gao, J., Wang, S., Pi, R., Zhao, X., Wu, C., Jiang,          2024. URL https://arxiv.org/abs/2407.21009v4.
  X., Li, Z., and Kong, L. Forewarned is Forearmed: Lever-
                                                                   Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang,
  aging LLMs for Data Synthesis through Failure-Inducing
                                                                     H., Zhang, M., Li, Y. K., Wu, Y., and Guo, D. DeepSeek-
  Exploration, October 2024. URL https://arxiv.org/
                                                                     Math: Pushing the Limits of Mathematical Reasoning
  abs/2410.16736v1.
                                                                     in Open Language Models, April 2024. URL http:
                                                                     //arxiv.org/abs/2402.03300. arXiv:2402.03300 [cs].
Lin, Z., Shen, S., Shang, J., Weston, J. E., and Nie, Y.
  Learning to solve and verify: A self-play framework              Silver, D., Hubert, T., Schrittwieser, J., Antonoglou, I.,
  for mutually improving code and test generation. In                 Lai, M., Guez, A., Lanctot, M., Sifre, L., Kumaran,
  NeurIPS 2025 Fourth Workshop on Deep Learning for                   D., Graepel, T., Lillicrap, T., Simonyan, K., and Has-
  Code, 2025. URL https://openreview.net/forum?                       sabis, D. Mastering Chess and Shogi by Self-Play with
  id=j6tMZaPWWF.                                                      a General Reinforcement Learning Algorithm, Decem-
                                                                      ber 2017. URL http://arxiv.org/abs/1712.01815.
Liu, J., Xia, C. S., Wang, Y., and Zhang, L. Is your code             arXiv:1712.01815 [cs].
  generated by chatgpt really correct? rigorous evaluation
  of large language models for code generation, 2023. URL          Singh, A., Co-Reyes, J. D., Agarwal, R., Anand, A., Patil,
  https://arxiv.org/abs/2305.01210.                                  P., Garcia, X., Liu, P. J., Harrison, J., Lee, J., Xu,
                                                                     K., Parisi, A., Kumar, A., Alemi, A., Rizkowsky, A.,
Liu, Y., Zhang, L. L., Zhu, Y., Dong, B., Zhou, X., Shang,           Nova, A., Adlam, B., Bohnet, B., Elsayed, G., Sedghi,
  N., Yang, F., and Yang, M. rStar-Coder: Scaling Compet-            H., Mordatch, I., Simpson, I., Gur, I., Snoek, J., Pen-
  itive Code Reasoning with a Large-Scale Verified Dataset,          nington, J., Hron, J., Kenealy, K., Swersky, K., Ma-
  May 2025. URL http://arxiv.org/abs/2505.21297.                     hajan, K., Culp, L., Xiao, L., Bileschi, M. L., Con-
  arXiv:2505.21297 [cs].                                             stant, N., Novak, R., Liu, R., Warkentin, T., Qian, Y.,

                                                              10
                                Propose, Solve, Verify: Self-Play Through Formal Verification

  Bansal, Y., Dyer, E., Neyshabur, B., Sohl-Dickstein,               Yang, Z., Kuang, Z., Xia, X., and Zhao, Y. Can LLMs
  J., and Fiedel, N. Beyond Human Data: Scaling Self-                  Generate High-Quality Test Cases for Algorithm Prob-
  Training for Problem-Solving with Language Models,                   lems? TestCase-Eval: A Systematic Evaluation of Fault
  April 2024. URL http://arxiv.org/abs/2312.06585.                     Coverage and Exposure, June 2025b. URL https:
  arXiv:2312.06585 [cs].                                               //arxiv.org/abs/2506.12278v1.

Song, Y., Zhang, H., Eisenach, C., Kakade, S., Foster,               Yuan, Z., Yuan, H., Li, C., Dong, G., Lu, K., Tan, C., Zhou,
  D., and Ghai, U. Mind the Gap: Examining the Self-                   C., and Zhou, J. Scaling relationship on learning math-
  Improvement Capabilities of Large Language Models,                   ematical reasoning with large language models, 2023.
  December 2024. URL https://arxiv.org/abs/2412.                       URL https://arxiv.org/abs/2308.01825.
  02674v2.
                                                                     Yuan, Z., Lou, Y., Liu, M., Ding, S., Wang, K., Chen, Y.,
Sukhbaatar, S., Lin, Z., Kostrikov, I., Synnaeve, G., Szlam,           and Peng, X. No more manual tests? evaluating and
  A., and Fergus, R. Intrinsic motivation and automatic                improving chatgpt for unit test generation, 2024. URL
  curricula via asymmetric self-play. In International                 https://arxiv.org/abs/2305.04207.
  Conference on Learning Representations, 2018. URL
                                                                     Zelikman, E., Wu, Y., Mu, J., and Goodman, N. D. STaR:
  https://openreview.net/forum?id=SkT5Yg-RZ.
                                                                       Bootstrapping Reasoning With Reasoning, March 2022.
Sun, Y., Wang, X., Liu, Z., Miller, J., Efros, A., and Hardt,          URL https://arxiv.org/abs/2203.14465v2.
  M. Test-Time Training with Self-Supervision for Gener-             Zhao, A., Wu, Y., Yue, Y., Wu, T., Xu, Q., Yue, Y., Lin,
  alization under Distribution Shifts. In Proceedings of the           M., Wang, S., Wu, Q., Zheng, Z., and Huang, G. Abso-
  37th International Conference on Machine Learning, pp.               lute Zero: Reinforced Self-play Reasoning with Zero
  9229–9248. PMLR, November 2020. URL https://                         Data, October 2025. URL http://arxiv.org/abs/
  proceedings.mlr.press/v119/sun20b.html. ISSN:                        2505.03335. arXiv:2505.03335 [cs].
  2640-3498.
                                                                     Zheng, L., Yin, L., Xie, Z., Sun, C., Huang, J., Yu, C. H.,
Wei, Y., Cassano, F., Liu, J., Ding, Y., Jain, N., Mueller,            Cao, S., Kozyrakis, C., Stoica, I., Gonzalez, J. E., Bar-
 Z., de Vries, H., von Werra, L., Guha, A., and Zhang,                 rett, C., and Sheng, Y. Sglang: Efficient execution
 L. SelfCodeAlign: Self-Alignment for Code Genera-                     of structured language model programs, 2024. URL
 tion, October 2024. URL https://arxiv.org/abs/                        https://arxiv.org/abs/2312.07104.
 2410.24198v2.
                                                                     Zhou, Y., Levine, S., Weston, J., Li, X., and Sukhbaatar,
Wen, X., Liu, Z., Zheng, S., Ye, S., Wu, Z., Wang, Y., Xu,             S. Self-Challenging Language Model Agents, June
 Z., Liang, X., Li, J., Miao, Z., Bian, J., and Yang, M.               2025.     URL http://arxiv.org/abs/2506.01716.
 Reinforcement Learning with Verifiable Rewards Implic-                arXiv:2506.01716 [cs].
 itly Incentivizes Correct Reasoning in Base LLMs, Oc-
 tober 2025. URL http://arxiv.org/abs/2506.14245.                    Zhu, R., Wang, Y., Jiang, T., Liang, J., and Wang, T. Self-
 arXiv:2506.14245 [cs].                                                improving model steering, 2025. URL https://arxiv.
                                                                       org/abs/2507.08967.
Xin, Q. and Reiss, S. P. Identifying test-suite-overfitted
  patches through test case generation. In Proceedings
  of the 26th ACM SIGSOFT International Symposium
  on Software Testing and Analysis, ISSTA 2017, pp.
  226–236, New York, NY, USA, 2017. Association for
  Computing Machinery. ISBN 9781450350761. doi:
  10.1145/3092703.3092718. URL https://doi.org/10.
  1145/3092703.3092718.

Yang, C., Li, X., Misu, M. R. H., Yao, J., Cui, W.,
  Gong, Y., Hawblitzel, C., Lahiri, S., Lorch, J. R., Lu,
  S., Yang, F., Zhou, Z., and Lu, S. AutoVerus: Auto-
  mated Proof Generation for Rust Code. Artifact of ”Au-
  toVerus: Automated Proof Generation for Rust Code”, 9
  (OOPSLA2):396:3454–396:3482, October 2025a. doi:
  10.1145/3763174. URL https://dl.acm.org/doi/10.
  1145/3763174.

                                                                11
                                 Propose, Solve, Verify: Self-Play Through Formal Verification

A. Full Proposer Prompt
    Proposer In-Context Learning

    I would like you to output a function spec in Verus (Rust) that is of difficulty {difficulty}. A spec
    defines a function’s inputs, outputs, and returns, and may define preconditions (requires) and
    postconditions (ensures) as well as any helpers necessary for defining these attributes.
    First you should reason about your answer, then you should output the problem descriptions for each
    problem within ```rust ``` tags, so that it can be parsed.
    Your solution will take the form:
    # Reasoning
    < your observations about what makes the example problems easy or hard, and ideas about how to propose
    a new problem >
    ```rust
    <function spec you propose>
    ```
    Here are some examples of specs and their difficulties.
    {examples}
    Now it’s your turn! Please output a problem that is **{difficulty}** for the model by either making
    problems that are not challenging enough harder, or making problems that are too challenging easier,
    or both, in some creative combination. Please enclose your function spec in ```rust ``` tags, so that
    it can be parsed. DO NOT copy any of the examples, and DO NOT include any function implementations.
    You should END your target function with an open curly brace {{.



B. Input & Target Proposal Settings

Table 3: Input/Target Proposal Settings. Mean pass@k with standard errors across 5 seeds. A=All, E=Easy, H=Hard,
U=Uniform.

                     Dafny2Verus                                   MBPP                               HumanEval
             pass@1 pass@5 pass@10                    pass@1       pass@5     pass@10      pass@1       pass@5 pass@10        Avg
 PSV-V ERUS 65.631.70 78.042.31 80.062.35            25.252.24    38.321.80   41.511.60   16.181.30    21.611.50 23.132.06   43.31
 A→H        64.501.31 77.972.18 79.782.34            21.731.40    35.851.80   39.431.64   13.601.17    20.140.57 21.940.57   41.66
 E→H        54.291.70 70.861.39 73.591.54            16.951.58    32.981.25   37.281.01   14.830.81    20.420.42 21.750.60   38.10
 A→E        58.701.35 73.121.37 75.351.54            21.260.81    34.661.25   37.701.37   15.870.96    21.510.70 23.000.60   40.13

We investigated different input and target proposal settings – e.g., using all problem types as the input to the proposer, asking
for Uniform problem types as output target, or perhaps asking for only one class of problems as output (e.g., Easy, Hard).
We tested three alternatives to our method: All → Hard, Easy → Hard (motivated by Luo et al. (2023)), and All → Easy. We
found that our model’s setting worked the best (All input problem types → Uniform output targets). This may be partially
explained by the ablation in §6.3, where we found that removing sampling of the inputs in the proposer hurt performance.
Our results suggest that taking in as much of the seed dataset as possible (not limiting input problems to a specific difficulty
type) and using that to generate as diverse a sampling of problems as possible is the best approach.

C. Transfer Learning Scaling Results
We also evaluate how PSV-V ERUS scales in the transfer learning setting, where we train on Dafny2Verus and evaluate on
MBPP and HumanEval. On MBPP, scaling from 4k to 32k questions per iteration yields consistent improvements: pass@1
increases from 21.8% to 32.0% (+47%), pass@5 from 34.4% to 42.6% (+24%), and pass@10 from 37.3% to 44.5%
(+19%). In contrast, HumanEval shows minimal scaling effects: pass@1 remains essentially flat (14.4% to 14.3%, -1%),
while pass@5 and pass@10 show marginal gains (+4% and +3%, respectively). This is supported by prior work (Aggarwal
et al., 2024) which found limited transfer between Dafny2Verus and HumanEval-Verified.

                                                                 12
                                Propose, Solve, Verify: Self-Play Through Formal Verification

D. Spec Compilation
In Verus, specifications define the contract a function must satisfy—preconditions (requires) and postconditions
(ensures). To test whether a specification is well-formed without requiring a correct implementation, we use the
#[verifier::external body] attribute. This tells Verus to trust the function signature and specification without verifying
the implementation body.

Example: Finding the Maximum Element

       Specification Only (with external body stub)

   1     use vstd :: prelude ::*;
   2
   3     verus ! {
   4
   5     #[ verifier :: external_body ]
   6     fn max_element (a: & Vec < i32 >) -> ( max : i32 )
   7        requires
   8            a . len () > 0,
   9        ensures
  10            forall |i: int | 0 <= i < a. len () == > a[i] <= max ,
  11            exists |i: int | 0 <= i < a. len () && a[i] == max ,
  12     {
  13        assume ( false );
  14        arbitrary ()
  15     }
  16
  17     } // verus !




The external body stub uses assume(false); arbitrary() to satisfy Verus’s type checker without a real implementation.
This allows us to verify that the specification itself is syntactically valid and logically consistent, independent of any
implementation.

                                                             13
                               Propose, Solve, Verify: Self-Play Through Formal Verification

       Complete Verified Implementation

   1     use vstd :: prelude ::*;
   2
   3     verus ! {
   4
   5     fn max_element (a: & Vec < i32 >) -> ( max : i32 )
   6         requires
   7             a. len () > 0,
   8         ensures
   9             forall |i: int | 0 <= i < a. len () == > a[i] <= max ,
  10             exists |i: int | 0 <= i < a. len () && a[i] == max ,
  11     {
  12         let mut max = a [0];
  13         for i in 1.. a. len ()
  14             invariant
  15                  forall |j: int | 0 <= j < i == > a[j] <= max ,
  16                  exists |j: int | 0 <= j < i && a[j] == max ,
  17         {
  18             if a[i] > max {
  19                  max = a[i ];
  20             }
  21         }
  22         max
  23     }
  24
  25     } // verus !




The verified implementation includes loop invariants that mirror the postconditions, allowing Verus to prove the implementa-
tion satisfies the specification. The invariants maintain that:

 1. All elements seen so far are ≤ max

 2. The current max value exists somewhere in the portion of the array already traversed

E. Supervised Fine-Tuning (SFT) Training Details
We perform all supervised fine-tuning (SFT) using the SFTTrainer implementation from the Hugging Face trl library.2
The training setup mirrors standard LoRA-based fine-tuning for decoder-only models, with lightweight adaptation for
efficiency on a single GPU. All experiments are conducted using accelerate to scale to distributed configurations, though
all runs reported in the main results with the Qwen2.5-3B-Coder model use a single NVIDIA A6000 GPU (no DDP).

                Table 4: Model Configuration                                     Table 5: Training Setup

 Parameter                       Value                                    Parameter                        Value
 max seq length                  2048                                     learning rate                    2e-4
 lora r                          16                                       num train epochs                 3
 use quantization                False                                    gradient accumulation steps      8
 use gradient checkpointing      True                                     eval strategy                    no
 per device train batch size     1                                        use peft                         True
 gradient accumulation steps     8                                        lora alpha                       32
 lora target modules             q proj, k proj, v proj, o proj,          bf16                             True
                                 gate proj, up proj, down proj            save total limit                 1
   2
       https://huggingface.co/docs/trl/en/sft trainer

                                                             14
                                 Propose, Solve, Verify: Self-Play Through Formal Verification

Each run takes approximately 20 minutes at the final iteration of the main experiments (with the most sft data). Checkpoints
are saved every 5 steps, retaining only the latest one to minimize storage.

Reproducibility. All code for SFT training, including configuration files and launcher scripts, is available in the project
repository for full reproducibility, and is run automatically as a subprocess during the main entrypoint script.

F. Verification Background
Denote a problem as x ∈ X , and its associated set of acceptable programs as Yx ⊆ Y. Here X is a problem domain and Y
is the set of possible programs. Intuitively, the term acceptable corresponds to the notion of a “correct solution”.
Let Zxv ⊆ Y be the set of programs for which a binary verifier v returns 1 for problem x, i.e.

                                                 Zxv = {y ∈ Y | v(x, y) = 1}.                                                  (1)

We say that program y is verified according to v when y ∈ Zxv .
We refer to Zxv as an accepted set (for verifier v, on problem x; we occasionally do not state these distinctions for brevity).
By soundness we mean that every program verified according to v is an acceptable program:

                                                            Zxv ⊆ Yx .                                                         (2)

Namely, we say that verifier v is sound for problem x if the relationship above holds, and unsound for problem x if the
relationship above does not hold. We say that the verifier is sound if it is sound for all problems x ∈ X . We say that the
verifier is unsound if it is unsound for at least one problem x ∈ X .
By completeness we mean that every acceptable program is verified according to v:

                                                            Yx ⊆ Zxv .                                                         (3)

We say that verifier v is complete for problem x if the relationship above holds, and incomplete if the relationship does not
hold. We say that the verifier is complete if it is complete for all problems x ∈ X . We say that the verifier is incomplete if it
is incomplete for at least one problem x ∈ X .

Test-case verification is unsound. A test suite can be seen as a verifier vT that returns 1 when a program passes all tests
in the suite T , and 0 otherwise. It induces a subset of programs that pass all tests in T , ZxvT = {y ∈ Y | y passes T}.
When we say that test case verification is unsound, we mean that for some problem x, there exists a program y that passes
the test cases but is not actually correct:

                                                     ∃x ∈ X s.t. ZxvT ̸⊆ Yx .                                                  (4)

It is easy to construct such an example. For instance, consider the problem of writing a program to check whether an input
integer is prime, and a single test that checks if the program returns True for input 3. Then a program return n == 3 would
pass the tests, but it is clearly not an acceptable program for the problem. In practice, unsoundness of test-case verification
is widely observed in the context of LLM code generation and evaluation (e.g., (Liu et al., 2023)).

Formal verification is sound with respect to the specification. In this setting, we take X to be the set of specifications
in a formal verification language such as Verus or Dafny. In our setting, x is a specification (e.g., preconditions and
postconditions), Yx is the set of programs that satisfy x, and vF is the Verus verification procedure. Verus is an SMT-based
verifier: it translates a program and specification into verification conditions and discharges them with an SMT solver. When
Verus verifies a program, the result is sound with respect to the specification, up to the trusted computing base (Lattuada
et al., 2023):

                                                     y ∈ ZxvF =⇒ y ∈ Yx .                                                      (5)

That is, if vF (x, y) = 1 then y satisfies the specification x.

                                                                  15
                               Propose, Solve, Verify: Self-Play Through Formal Verification

However, formal verification tools like Verus or Dafny are incomplete. This is fundamental: no (general-purpose) program
analysis for Turing-complete languages can be both sound and complete (Rice, 1953). Hence, for a problem x, it may
be the case that ZxvF ⊂ Yx (note the strict subset), meaning that there are acceptable programs that the verifier rejects.
This fundamental incompleteness explains why proof annotations are needed; we can think of adding such annotations as
converting a program p ∈ Yx \ ZxvF into a program p′ ∈ ZxvF .

G. Difficulty Unaware Ablation
   Proposer In-Context Learning

   I would like you to output a problem that is of {difficulty} level. Here are some examples of problems
   and how difficult they were for the model.
   Problem 1
   {problem spec}
   Problem 2
   {problem spec}
   ...
   Now it’s your turn! Please describe your reasoning, then output a new problem that is {difficulty}.




                                                            16
