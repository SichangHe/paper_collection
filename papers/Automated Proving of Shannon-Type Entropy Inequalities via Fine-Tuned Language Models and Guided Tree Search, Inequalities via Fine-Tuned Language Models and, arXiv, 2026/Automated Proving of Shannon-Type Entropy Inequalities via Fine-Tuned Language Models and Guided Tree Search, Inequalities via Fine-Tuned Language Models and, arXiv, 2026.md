                                             Automated Proving of Shannon-Type Entropy
                                           Inequalities via Fine-Tuned Language Models and
                                                           Guided Tree Search
                                                            Shing Yin Wong† , Shaocheng Liu∗ , Linqi Song† , Amin Gohari∗ , Cheuk Ting Li∗
                                                                           †
                                                                            Department of Computer Science, City University of Hong Kong
                                                                 ∗
                                                                     Department of Information Engineering, The Chinese University of Hong Kong


                                           Abstract—THIS PAPER IS ELIGIBLE FOR THE STUDENT                     to reduce the size of the LP problem and make the proof
                                        PAPER AWARD. Proving Shannon-type entropy inequalities is              process more efficient.
arXiv:2606.05729v1 [cs.IT] 4 Jun 2026




                                        a fundamental task in information theory that often requires              However, for an inequality involving n random variables,
                                        constructing non-trivial linear combinations of known constraints,
                                        which is a combinatorial search problem that scales poorly with        the space of possible proof-step sequences is vast. Since the
                                        the number of random variables. We investigate whether small-          LP search space grows exponentially, LP-based methods face
                                        scale large language models (0.6B–1.7B parameters), fine-tuned         memory and compute limitations as n grows beyond 10.
                                        on atomic proof steps and combined with guided beam search,               Recent advances in large language models (LLMs) have
                                        can automate this process. On a held-out test set of 60 inequalities   shown promise in formal mathematical reasoning, including
                                        spanning n=10 to 15 variables, our 0.6B fine-tuned model achieves
                                        an 85% proof success rate with tree search. GPT-5.5 solves 1.7%        theorem proving and proof automation [13]–[21], [26], [29]–
                                        samples under zero-shot prompting while Psitip solves 33.3%            [31] and mathematical/olympiad problem solving [11], [22]–
                                        samples. A systematic ablation study across training context           [25], [27]. However, the application of LLMs to entropy
                                        length (4096 vs. 8192 tokens) and data distribution (n=9-skewed        inequality proving remains largely unexplored. Entropy in-
                                        vs not skewed) reveals that a 4096-token not skewed training           equalities present a unique challenge: they require both the
                                        distribution yields the best performance, with extended context
                                        and skewed data providing no marginal benefit. We further              semantic intuition to identify which variables to condition on,
                                        identify two dominant failure modes—format failures and step           and the syntactic precision to produce machine-verifiable proof
                                        quality degradation—and verify that the beam-scoring heuristic         steps with correct indices and coefficients—the latter being
                                        is essential via a controlled ablation (random scoring reduces         precisely where frontier LLMs struggle.
                                        success from 83% to 23%).                                                 In this work, we investigate whether small-scale, supervised
                                                                                                               fine-tuned (SFT) large language models, combined with a
                                                               I. I NTRODUCTION                                guided beam-search tree search, can automate the proof of
                                           Entropy inequalities are fundamental tools in information           Shannon-type entropy inequalities. Our key contributions are:
                                        theory. They are widely used to give outer bounds in specific             1) We demonstrate that a 0.6B-parameter SFT model with
                                        problems such as network coding [1], secret sharing [2],                      tree search achieves 85% proof success on a challenging
                                        regenerating codes [3], and related problems.                                 test set of 60 inequalities (n = 10–15). Frontier LLMs
                                           Given a target inequality, determining whether it is a valid               (GPT-5.5, Claude-4.6 Sonnet) score only 1.7% (1/60)
                                        entropy inequality is quite difficult, especially when the number             under zero-shot prompting.
                                        of random variables is large. To address this problem, Ye-                2) Through a systematic four-dataset ablation (A/B/C/D),
                                        ung introduced a linear programming framework for proving                     we show that a 4096-token not skewed training distribu-
                                        information inequalities [4], which was implemented in the                    tion is sufficient and optimal; extending context to 8192
                                        MATLAB package Information Theoretic Inequality Prover                        tokens or skewing toward higher n provides no benefit
                                        (ITIP). It verifies a target inequality by checking whether                   and can degrade robustness.
                                        it can be written as a non-negative linear combination of                 3) We identify and characterize two primary failure
                                        Shannon-type inequalities and additional conditions. Thus, the                modes—format failures and step quality degradation—
                                        proof is reduced to a linear programming problem. Several                     and quantify the essential role of the beam-scoring
                                        automated tools were later developed along this line. Xitip [5]               heuristic through controlled ablation.
                                        improves the implementation by using a C-based solver, while              4) We show advantages of our method for large n compare
                                        Minitip [6] provides a lightweight C-based prover with a simple               to LP-solvers.
                                        syntax. Aitip [7] offers an online service for proving or disprov-                      II. P ROBLEM F ORMULATION
                                        ing information inequalities. Psitip [8] further extends auto-
                                        mated reasoning to a symbolic Python environment, supporting           A. Shannon-Type Entropy Inequalities
                                        constrained, auxiliary-variable, existential, and non-Shannon-           We review the basic concepts of Shannon-type entropy
                                        type reasoning. Recently Gaussian-elimination methods [9] aim          inequalities [4]. Let X1 , X2 , . . . , Xn be discrete random vari-
ables. For a subset S ⊆ [n] := {1, . . . , n}, the joint entropy of          C. Proof Example
the variables Xi where i ∈ S is denoted as H(XS ).                              To illustrate the task, consider a concrete n = 14 inequality
  Definition 1: A single entropy inequality on the random                    from the test set. The target is a 22-term inequality:
variables X1 , . . . , Xn is a sequence (αi , Si )i∈[k] where αi ∈ Z          Itarget = − H(X1,2,5,6,9,11 ) + H(X1,2,4,5,6,7,8,9,11 )
and Si ⊆ [n], which represents the inequality                                         − 3H(X1,4,5,6,8,13 ) − 3H(X1,6,8,11,13 )
                                                                                      + 3H(X1,6,7,8,11,12,13 ) − H(X3,5,7,9,11,14 )
                          k
                          X                                                           + H(X1,2,5,6,7,9,11,14 ) − H(X1,2,4,5,6,7,8,9,11,14 )
                                αi H(XSi ) ≥ 0.                                       − 3H(X1,3,4,5,6,8,12,14 ) + 3H(X1,3,4,5,6,7,8,9,10,12,14 )
                          i=1
                                                                                      − 6H(X2,4,5,7,13,14 ) + 6H(X2,4,5,6,7,8,9,13,14 )
A conditional entropy inequality is given by a single entropy                         + H(X2,3,5,6,7,8,9,11,13,14 ) + 3H(X1,4,5,6,7,8,10,11,13,14 )
inequality (αi , Si )i∈[k] (the consequent) together with a list                      + 3H(X1,5,6,7,8,9,10,11,13,14 ) + H(X3,5,6,7,8,9,10,11,13,14 )
of entropy inequalities ((βj,i , Tj,i )i∈[ℓj ] )j∈[m] (the conditions),               − H(X2,3,5,6,7,8,9,10,11,13,14 )
which represents the implication                                                      − H(X1,2,4,5,6,7,8,9,10,11,13,14 )
                                                                                      + 3H(X1,3,4,5,6,7,8,12,13,14 )
                 ℓk                         k
                X                         X                                         − 3H(X1,5,6,7,8,9,10,11,12,13,14 )
    ∀j ∈ [m] :         βj,i H(XTj,i ) ≥ 0 ⇒   αi H(XSi ) ≥ 0.                         + H(X1,2,4,5,6,7,8,9,10,11,12,13,14 )
                 i=1                                    i=1
                                                                                      − 3H(X1,3,4,5,6,7,8,9,10,11,12,13,14 ) ≥ 0.
                                                                              Our 0.6B model under beam search (beam 32, rollouts 6, depth
   Definition 2: A conditional entropy inequality is Shannon-
                                                                             24) finds the following 7-step proof:
type if it is implied by the polymatroid inequality [4]
I(XA ; XB |XC ) ≥ 0, or equivalently,                                           1) 6H(X6,8,9 |X2,4,5,7,13,14 ) ≥ 0
                                                                                2) 3I(X7,10,11,14 ; X3,7,12,13,14 |X1,4,5,6,8,13 ) ≥ 0
      H(XA∪C ) + H(XB∪C ) ≥ H(XA∪B∪C ) + H(XC ),                                3) 3I(X7,9,10 ; X7,10,11,13 |X1,3,4,5,6,8,12,14 ) ≥ 0
                                                                                4) 3I(X7,12 ; X5,7,9,10,14 |X1,6,8,11,13 ) ≥ 0
for every A, B, C ⊆ [n]. More precisely, it is Shannon-type if                  5) I(X4,7,8 ; X7,14 |X1,2,5,6,9,11 ) ≥ 0
                                                                                6) I(X2,6,8,13 ; X6,8,10,13 |X3,5,7,9,11,14 ) ≥ 0
      k                    K
      X                    X                                                    7) H(X12 |X1,2,4,5,6,7,8,9,10,11,13,14 ) ≥ 0.
            αi H(XSi ) ≡         µj H(XAj ∪Cj ) + H(XBj ∪Cj )
                                                                             Each step is independently verifiable as a Shannon-type en-
      i=1                  j=1
                                                                            tropy inequality. The residual after step 7 is exactly zero.
                           − H(XAj ∪Bj ∪Cj ) − H(XCj )
                                m          ℓk                                                           III. M ETHOD
                                X          X
                           +          νj         βj,i H(XTj,i ).             A. Training Data Generation
                                j=1        i=1                                  We generate supervised training data using a reverse proof
for some K ∈ Z≥0 , µj ∈ Q≥0 , Aj , Bj , Cj ⊆ [n] for                         construction procedure. Specifically, we randomly sample
j ∈ [K], and νj ∈ Q≥0 for j ∈ [m]. The datum                                 Shannon-type entropy inequalities and conditions, and com-
((µj , Aj , Bj , Cj )j∈[K] , (νj )j∈[m] ) is called a proof of the           bine them to construct a target inequality with a guaranteed
conditional entropy inequality with length K.                                proof. Since our training framework is step-wise, each prompt
                                                                             corresponds to the current residual inequality, and the model
   The proof task is to certify the target inequality under the
                                                                             is expected to output only one proof step at a time. Therefore,
given conditions by finding coefficients (µj , Aj , Bj , Cj )j∈[K]
                                                                             we need a principled strategy to select the next proof step from
and (νj )j∈[m] certifying the decomposition.
                                                                             the candidate Shannon inequalities and conditions.
                                                                                Given a current residual inequality, we focus on entropy
B. Proof via Stepwise Residual Reduction
                                                                             terms with negative coefficients, since these terms indicate the
  Our proof strategy follows an iterative decomposition: start-              part that still needs to be eliminated in the remaining proof. For
ing with residual R0 = Itarget , at each step t, we propose                  each candidate proof atom, we define a score on the negative
an atomic non-negative term Tt ≥ 0. Where Tt is either                       part magnitude of the current residual. The candidate with the
a single information measure with positive coefficient (e.g.,                largest score is selected as the next output step. See Algorithm
H(A), H(A|B), I(A; B), and I(A;                                              1.
                                 PℓkB|C)), or a positive scalar
multiple of a given condition      i=1 βj,i H(XTj,i ). Then we
                                                                                The prompt is tokenized and bounded to a maximum context
subtract it from the current residual:                                       length of 4096 or 8192 tokens, depending on the dataset vari-
                                                                             ant. Each dataset contains approximately 389 million tokens.
                           Rt+1 = Rt − Tt .                            (1)
                                                                             B. Model Architecture and Fine-Tuning
The proof succeeds if we reach Rt = 0. This constraint ensures                  We fine-tune Qwen3 models (0.6B and 1.7B parame-
every step is automatically verifiable by the symbolic checker               ters) [10] using Low-Rank Adaptation (LoRA) [12] with rank
without requiring an LP solver at each step.                                 r = 64 and α = 128. Training uses the AdamW 8-bit optimizer
Algorithm 1 Mixed-type training sample generation                ward residuals that are closest to being non-negative in every
 1: Sample the number of random variables n ∈ {3, . . . , 9}     coefficients—and thus closest to being provable. Ablation with
    and the number of proof atoms k.                             uniform random scoring (replacing this heuristic) reduces proof
 2: Generate k Shannon-type atoms S1 , . . . , Sk from H(A),     success from 83.3% to 23.3% (7/30), confirming the scoring
    H(A|B), I(A; B), and I(A; B|C).                              heuristic is essential for effective beam allocation.
 3: Generate conditions by random sampling and LP feasibil-        Candidate validation pipeline. Each candidate step is
    ity checking, and split them into equality conditions C=     validated through checks before being added to the beam:
    and inequality conditions C≥ .                                 1) Format filter: Accepts only positive scalar multiples
 4: Represent each equality condition C = 0 as two inequali-           of froms H(A), H(A|B), I(A; B), and I(A; B|C),
    ties C ≥ 0 and −C ≥ 0.                                             or of known conditions. Multi-term Shannon sums not
 5: Assign coefficients αi > 0 and βt > 0 to Shannon atoms             matching any condition are rejected.
    and inequality conditions, and assign coefficients ηj ̸= 0     2) Obviously-negative pruning: Discards residuals where
    to equality conditions.                                            all coefficients are ≤ 0 ( residuals never reach zero).
 6: Construct the initial residual                                 3) LP false pruning (applied on sample with n ≤ 9
           R←
                 X
                     αi Si +
                               X
                                   ηj Cj +
                                            X
                                                  βt Dt .              only): When the residual and all conditions have ≤ 9
                  i         Cj ∈C=        Dt ∈C≥
                                                                       variable involved, we use a Shannon-type LP to detect
                                                                       impossible residuals and prune them. For n ≥ 10, the LP
 7: Let V    be the multiset of all candidate proof with their         can no longer incorporate all n variables alongside the
    coefficients.                                                      conditions; Thus, LP pruning is disabled. The ablation
 8: Initialize the dataset D ← [ ].                                    experiment shows that whether we enable of disable this
 9: while V is not empty do                                            function have minor impact on accuracy.
10:     Let N − (R) = {q : Rq < 0} be the negative
    coordinates of R.                                            D. Datasets and Training Setup
11:     Select the atom (λ, v) ∈ V that maximizes                   We construct four training datasets (A/B/C/D) varying two
                            P                                    factors: maximum context length (4096 vs. 8192 tokens) and
                         − q∈N − (R) λvq .
                                                                 data distribution (n = 9-skewed and not skewed), each con-
12:     Format the intput x using the current residual target    taining 389.5M tokens: Dataset A (508,803 rows, 4096, 6.0%
    R ≥ 0 and all conditions.                                    n = 9); Dataset B (256,870 rows, 4096, n = 9-skewed, 52.6%
13:     Format the output y using the selected proof step λv ≥   n = 9); Dataset C (8192, 8.0% n = 9, 77% of rows exceed
    0.                                                           3072 tokens); Dataset D (8192, n = 9-skewed, 66.9% n = 9,
14:     Add the prompt (x, y) to D.                              95% long-token share).
15:     Update R ← R − λv and remove (λ, v) from V.
                                                                 E. Training Budget Selection
16: end while
17: return D.                                                       We first train a 0.6B pilot run on Dataset A with 10
                                                                 uniformly spaced checkpoints (fractions 0.1–1.0 of the full
                                                                 training schedule) and evaluate all checkpoints on a held-out
with learning rate 1.5×10−5 , cosine schedule with 200 warmup    validation set (n = 10–15, 30 problems) to select a shared
steps, micro-batch size 4, gradient accumulation over 8 steps    training-budget fraction.
(effective batch size 32), weight decay 0.01, and BF16 mixed
precision. Each model is trained for 2 epochs on two NVIDIA                                TABLE I
                                                                        DATASET A CHECKPOINT SWEEP ON THE 30 PROBLEMS .
RTX 5880 Ada Generation GPUs. All runs use seed 42 for
reproducibility.                                                        Fraction   Step      Pass Rate     Avg. Tree (Proved)

C. Guided Beam-Search Tree Search                                         0.2       3178   21/30 (70.0%)         514.0
                                                                          0.4       6356   22/30 (73.3%)         478.7
   At inference time, the fine-tuned model proposes candi-                0.6       9534   24/30 (80.0%)         385.3
date proof steps given the current residual Rt and available              0.8      12712   23/30 (76.7%)         393.6
conditions. We employ a beam search over proof trees with                 1.0      15885   25/30 (83.3%)         416.0
configurable beam size B, rollouts per node K, and maximum
depth D. Objective is to find any path from R0 to Rt = 0.           Table I shows the sweep results. Performance plateaus
   Scoring and pruning. After generating K candidate in-         around fraction 0.5–0.6, with checkpoint 9534 (fraction 0.6)
equalities at a node, each valid candidate produces a new        achieving 80.0% success and the lowest average proof tree
residual vector.
             P Nodes are scored by the greedy heuristic          size (385.3 nodes) among all high-performing fractions. Later
score(c) = i:ci <0 |ci | × 103 , which is the sum of absolute    checkpoints show marginally improved success (83.3% at frac-
value of negative coefficients of the residual inequality. We    tion 1.0) but with reduced search efficiency (416.0 tree size),
prioritizes residuals with the smallest score, favor beam to-    consistent with overfitting to training data patterns without
improving underlying reasoning capability. Fraction 0.6 is also            4096-token models (A/B) lead the long stress-test (80% vs.
the earliest checkpoint within a small margin of the best                  60%–73% for 8192-token models). The interaction is clearest
validation score, satisfying our preference for conservative               in Dataset D: it leads on the easy set but drops to last on the
early stopping.                                                            hard set and long stress-test, suggesting that skewed n = 9
  We freeze fraction 0.6 as the shared training budget and                 training at 8192 tokens encourages proof patterns that do not
apply it to all subsequent 0.6B runs (B/C/D) and the 1.7B run              transfer to harder problems.
on Dataset A.                                                                 Based on these results, we select Dataset A (4096 not
                                                                           skewed) as the best overall configuration for its consistent
                   IV. E XPERIMENTAL R ESULTS
                                                                           performance and superior search efficiency.
A. Evaluation Setup
   We evaluate on three test regimes:                                      C. Tree Search Hyperparameter Sweep
   • Easy set (E): 30 synthetic inequalities, n = 10–15, five                After selecting Dataset A, we conduct a systematic sweep
     per n, with mixed conditions.                                         over beam size {8, 16, 24, 32, 64}, rollouts {2, 4, 6, 8}, and
   • Hard set (H): 30 difficult inequalities, n = 8–10, five               maximum depth {16, 20, 24, 28} on the hard set using the
     per n. Half are short inequalities that our prototype model           Dataset A model at fraction 0.6.
     cannot solve, while the other half are provable only with
                                                                                                      TABLE III
     large tree sizes (> 1000 nodes). This set was designed to               S ELECTED TREE SEARCH HYPERPARAMETER SWEEP RESULTS ON THE
     stress-test both model capability and search depth.                                  HARD SET (DATASET A, 0.6 FRACTION ).
   • n=9 set (N9): An n = 9 set, target plus condition token
     within 800–4096, generated by Alg. 1.                                        Beam    Rollouts   Depth     Pass Rate     Avg. Tree
   • Long tokens set (L): Token lengths ≥ 4096 for n =
                                                                                   24        4        20      9/30 (30.0%)    1076.1
     7, 8, 10, five per n, generated by Alg. 1.                                    32        4        24     14/30 (46.7%)    2352.0
   • Final test set: 60 inequalities, n = 10–15, 10 per n,                         32        6        24     16/30 (53.3%)    2588.7
     generated by Alg. 1. We permuting n = 10 samples index                        32        8        24     12/30 (40.0%)    2117.0
     randomly to obtain n = 11–15 sample to avoid large                            64        6        24     10/30 (33.3%)    1524.8
     computing power required for direct LP generate.
   Evaluation on N9 and L set is to ablate the effectiveness                  The selected policy is beam size 32, rollouts 6, maximum
of each dataset on specific token-length and n-values por-                 depth 24, which achieves the highest success rate (53.3% on
tions. Default search parameters are beam size 24, rollouts 4,             the hard set). Notably, performance degrades at the most ag-
maximum depth 20. Evaluation uses 6–9 instances of LLMs                    gressive settings (beam 64 or rollouts 8): log analysis confirms
parallely on an NVIDIA RTX 5880 Ada Generation cluster.                    that failed high-parameter runs terminated naturally without
B. ABCD Dataset Ablation (0.6B)                                            hitting tree or time budgets, indicating that excessive breadth
                                                                           introduces distractor branches that steer the search away from
  Table II reports the 0.6B model performance across all four
                                                                           valid proof paths. This reveals a critical beam size beyond
datasets at the 0.6 training fraction.
                                                                           which search quality declines.
                            TABLE II                                       D. Scaling to 1.7B Parameters
 M ODEL SIZE SCALING AND ABLATION ACROSS ALL REGIMES . E=E ASY,
      H=H ARD (30 EACH ); N9=n=9 SPEC ., L=L ONG (15 EACH ).                  Table II compares the 0.6B and 1.7B models, both trained
                                                                           on Dataset A at fraction 0.6 and evaluated under the identical
 Model / Dataset     E (30)        H (30)        N9 (15)       L (15)      search policy (beam 32, rollouts 6, depth 24).
 A (4096 Bal.)     24/30 (80%)   9/30 (30%)    14/15 (93%)   12/15 (80%)      The 1.7B model slightly underperformed compared to the
 B (4096 Skew)     24/30 (80%)   9/30 (30%)    13/15 (87%)   12/15 (80%)   0.6B model on the test set (80.0% vs. 83.3%), the slightly
 C (8192 Bal.)     21/30 (70%)   9/30 (30%)    14/15 (93%)   11/15 (73%)   1.7B underperformed is by one sample, consistent with run-
 D (8192 Skew)     25/30 (83%)   8/30 (27%)    13/15 (87%)    9/15 (60%)
                                                                           to-run stochastic variation rather than a systematic capability
     1.7B A        24/30 (80%)   14/30 (47%)       –             –         regression. However, on the more difficult hard set (n = 8–10,
                                                                           curated), the 1.7B model significantly outperforms the 0.6B
   On the easy set, all datasets perform comparably (70–83%),              model (46.7% vs. 30.0%).
with Dataset D marginally leading. On the hard set, Datasets
A/B/C tie at 30% while D trails at 27%. Critically, while A, B,            E. Final Test-Set Results and Comparison to LP-solver
and C achieve the same hard-set pass rate, Dataset A attains                  Table IV’s experiments on LP-solvers are in 300s time
this with a substantially smaller average tree size (1076.1 vs.            limit.(left) compares our LLM-based method with PSITIP [8].
1257.8–1319.0), indicating more efficient proof paths and less             PSITIP can solve all the n ≤ 12 samples but time out in bigger
susceptibility to search noise while accuracy is about the same            sample. Since LP-solver need to load elemental inequalities
as other dataset. On specialist subsets, not skewed models                 in O(n2 2n ) size. Our method do not need to load elemental
(A/C) lead the n = 9 set (93% vs. 87% for skewed), and                     inequalities, uses 2.33GB of VRAM at minimal setting. Since
Aitip can only solve equality condition problems, we compare                example, on Sample 6 (n = 11), the model proposes 6 ·
LP-solvers in such a dataset. Note that AITIP uses 36.5GB of                (7H(X1,2,3,4,5,6 ) − 5H(X1,4,6,7 ) + · · · ) ≥ 0, which is rejected
RAM when solving n = 15 samples, indicating the memory                      by the format filter since it is not a positive scalar multiple
limitation of the LP-solver method.                                         of any provided condition. We suspect the model sometimes
                                                                            output complex pre-training-style expressions, conflicting with
                              TABLE IV                                      the strict atomic-step constraint.
(L EFT ) RESULTS DATASET WITH INEQUALITY AND EQUALITY CONDITIONS .
    (R IGHT ) LP- SOLVERS BENCHMARK , ONLY EQUALITY CONDITIONS .            B. Step Quality Degradation
                       Testset                   Equality Conditions
                                                                               On the failed n = 15 samples in the final test-set evaluation,
                                                                            the model often produced format-valid but weak steps. For
   n          0.6B A             PSITIP        AITIP           PSITIP
                                                                            instance, on a residual with 20+ terms and large coefficients
   10      10/10 (100.0%)    10/10 (100%)   10/10 (100%)    10/10 (100%)
   11       9/10 (90.0%)     10/10 (100%)   10/10 (100%)    10/10 (100%)    (magnitudes 10–100), the model repeatedly proposes single-
   12       7/10 (70.0%)      0/10 (0%)     10/10 (100%)     4/10 (40%)     unit monotonicity steps (e.g., H(X1,2 |X3 ) ≥ 0) that reduce the
   13       8/10 (80.0%)      0/10 (0%)      8/10 (80%)      1/10 (10%)
   14       9/10 (90.0%)      0/10 (0%)       0/10 (0%)      2/10 (20%)     residual by only a few terms with coefficient 1 while leaving
   15       8/10 (80.0%)      0/10 (0%)      1/10 (10%)      1/10 (10%)     large negative coefficients untouched. Performance degrades
 Overall   51/60 (85.0%)    20/60 (33.3%)   39/60 (65.0%)   28/60 (46.7%)   at aggressive search settings (beam 64, rollouts 8): at high
                                                                            beam size and at high rollouts, it repeatedly generates near-
                                                                            duplicate atomic terms that only differ in coefficient (e.g.,
F. SOTA LLM Baselines                                                       H(X2,5 |X1,3,6,7,8 ) ≥ 0 appears 7 consecutive times at roll-
   We establish external baselines on the same test set to                  out 8) rather than exploring diverse steps. The search budget is
contextualize the SFT model performance.                                    consumed by these steps that make negligible progress toward
   Zero-shot prompting. GPT-5.5 [32] and Claude-4.6 Sonnet                  zero.
[33] were evaluated via their websites, their output is not                                        VI. C ONCLUSION
restricted to atomic step. Under zero-shot prompting, GPT-5.5
                                                                               We have shown that a 0.6B-parameter language model, fine-
proved 1 out of 60 samples while while Claude-4.6 Sonnet
                                                                            tuned on atomic entropy inequality proof steps and combined
solved none. The only successful case is Sample 7, whose
                                                                            with guided beam search, can prove 85% of test set where GPT-
proof uses the given condition and can be decomposed as
                                                                            5.5 scores only 1.7% (1/60) under zero-shot prompting. A 1.7B
I = 6C1 + S, where S is a non-negative combination of
                                                                            model under identical conditions outperforms the 0.6B model
Shannon-type inequalities.
                                                                            on a hard set (46.7% vs. 30.0%), demonstrating that larger ca-
   Tree-search with frontier LLMs. We also try on replacing
                                                                            pacity aids deeper reasoning on complex problems at moderate
our fine-tuned model with GPT-5.4-mini [34] or DeepSeek
                                                                            n. Systematic ablation reveals that a 4096-token not skewed
V3.2 [35] the beam-search framework, using the API (tem-
                                                                            training distribution yields the most robust performance, with
perature=1.2, top_p=0.9, max_tokens=512). Test with n = 3, 5
                                                                            no benefit from extended context, and that the beam-scoring
problems, were completed: DeepSeek V3.2 proved 1/5 (20.0%)
                                                                            heuristic is essential (random scoring reduces success rate from
and GPT-5.4-mini proved 0/5 (0.0%). DeepSeek V3.2 and
                                                                            83% to 23%). Our method also solves more n ≥ 12 problems
GPT-5.4-mini produced 45–300 format-invalid proposals per
                                                                            compare to LP-solver under time limit. The primary obstacles
run (often multi-term expressions or natural-language frag-
                                                                            to further improvement are format failures at moderate n and
ments) and propose Shannon-infeasible output, showing that
                                                                            search budget exhaustion at high n, both of which suggest
the format discipline required by the verifier is not satisfied by
                                                                            concrete directions for future work in constrained decoding,
general-purpose LLMs.
                                                                            larger-scale search, and reinforcement learning [28].
G. Search Score Function Ablation                                              Another way to speed up tree search is to strengthen LP false
                                                                            pruning. When n ≥ 10, we can randomly set some variables
   We tested on dataset E with random scoring on for beam
                                                                            be constants or equal. A true information inequality must still
selection. Accuracy drops from 83.3% (25/30) to 23.3% (7/30).
                                                                            be true after these changes. Hence, if the simplified inequality
The average tree size on successful proofs are 1100.3 and 244.1
                                                                            is false, then the original inequality cannot be true. This gives
respectively for greedy function and uniform random scoring
                                                                            an inexpensive and efficient way to reject bad branches early,
function. Only samples with small proof tree size are proved,
                                                                            which may be investigated in future research.
indicating that uniform random scoring decrease tree search
ability on proving samples that require large depth.                                              ACKNOWLEDGMENT
                       V. FAILURE A NALYSIS                                   The work of Shaocheng Liu and Cheuk Ting Li was partially
                                                                            supported by two grants from the Research Grants Council of
A. Format Failure                                                           the Hong Kong Special Administrative Region, China [Project
  In the 0.6B Dataset A test-set evaluation, at n = 11                      No.s: CUHK 24205621 (ECS), CUHK 14209823 (GRF)]. The
and n = 13, the model repeatedly proposes multi-term                        authors thank Chih Wei Ling, Yanxiao Liu and Yunhe Li for
Shannon sums instead of atomic single-term expressions. For                 the insightful discussions.
                              R EFERENCES                                        [24] T. Hubert et al., “Olympiad-level formal mathematical reasoning with
                                                                                      reinforcement learning,” Nature, vol. 651, pp. 607–613, 2026.
 [1] Z. Zhang and R. W. Yeung, “On characterization of entropy function          [25] C. Wei, M. Sun, and W. Wang, “Proving olympiad algebraic inequalities
     via information inequalities,” IEEE Trans. Inf. Theory, vol. 44, no. 4,          without human demonstrations,” in Proc. Adv. Neural Inf. Process. Syst.
     pp. 1440–1452, Jul. 1998.                                                        (NeurIPS), Datasets and Benchmarks Track, 2024.
 [2] A. Beimel, “Secret-sharing schemes: A survey,” in Coding and Cryptol-       [26] K. Dong, A. Mahankali, and T. Ma, “Formal theorem proving by
     ogy, Lecture Notes in Computer Science, vol. 6639. Berlin, Heidelberg:           rewarding LLMs to decompose proofs hierarchically,” in Proc. NeurIPS
     Springer, 2011, pp. 11–46.                                                       Workshop Mathematical Reasoning and AI (MATH-AI), 2024.
 [3] C. Tian, “Characterizing the rate region of the (4,3,3) exact-repair        [27] E. Glazer, E. Erdil, T. Besiroglu, D. Chicharro, E. Chen, A. Gunning,
     regenerating codes,” IEEE J. Sel. Areas Commun., vol. 32, no. 5, pp. 967–        C. F. Olsson, J.-S. Denain, A. Ho, E. de Oliveira Santos, O. Järviniemi,
     975, May 2014.                                                                   M. Barnett, R. Sandler, M. Vrzala, J. Sevilla, Q. Ren, E. Pratt, L. Levine,
                                                                                      G. Barkley, N. Stewart, B. Grechuk, T. Grechuk, S. V. Enugandla,
 [4] R. W. Yeung, “A framework for linear information inequalities,” IEEE
                                                                                      and M. Wildon, “FrontierMath: A benchmark for evaluating advanced
     Trans. Inf. Theory, vol. 43, no. 6, pp. 1924–1934, Nov. 1997.
                                                                                      mathematical reasoning in AI,” arXiv:2411.04872, 2024.
 [5] R. Pulikkoonattu and S. Diggavi, ITIP-Based C Program Software
                                                                                 [28] Y. Yue, Z. Chen, R. Lu, A. Zhao, Z. Wang, Y. Yue, S. Song, and
     Package, 2006. [Online]. Available: http://xitip.epfl.ch
                                                                                      G. Huang, “Does reinforcement learning really incentivize reasoning
 [6] L. Csirmaz, Minitip—A Minimal Information Theoretic Inequality                   capacity in LLMs beyond the base model?,” in Proc. Adv. Neural Inf.
     Prover, 2016. [Online]. Available: https://github.com/lcsirmaz/minitip           Process. Syst. (NeurIPS), 2025.
 [7] S.-W. Ho, L. Ling, C. W. Tan, and R. W. Yeung, “Proving and disproving      [29] M. Lu, B. Delaware, and T. Zhang, “Proof automation with large lan-
     information inequalities: Theory and scalable algorithms,” IEEE Trans.           guage models,” in Proc. 39th IEEE/ACM Int. Conf. Automated Software
     Inf. Theory, vol. 66, no. 9, pp. 5522–5536, Sep. 2020.                           Engineering (ASE), Sacramento, CA, USA, 2024, 12 pp.
 [8] C. T. Li, “An automated theorem proving framework for information-          [30] P. Song, K. Yang, and A. Anandkumar, “Lean Copilot: Large language
     theoretic results,” IEEE Trans. Inf. Theory, vol. 69, no. 11, pp. 6857–          models as copilots for theorem proving in Lean,” in Proc. Int. Conf.
     6877, Nov. 2023.                                                                 Neuro-symbolic Systems (NeuS), Proc. Mach. Learn. Res., vol. 288,
 [9] L. Guo, R. W. Yeung, and X.-S. Gao, “Proving information inequalities            pp. 144–169, 2025.
     by Gaussian elimination,” IEEE Trans. Inf. Theory, vol. 71, no. 4,          [31] J. Lu, Y. Wan, Z. Liu, Y. Huang, J. Xiong, C. Liu, J. Shen, H. Jin,
     pp. 2315–2328, Apr. 2025.                                                        J. Zhang, H. Wang, Z. Yang, J. Tang, and Z. Guo, “Process-driven
[10] Qwen Team, “Qwen3 technical report,” arXiv:2505.09388, 2025.                     autoformalization in Lean 4,” arXiv:2406.01940, 2024.
[11] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang,        [32] OpenAI, GPT-5.5, 2026. [Online]. Available: https://openai.com/index/
     Y. K. Li, Y. Wu, and D. Guo, “DeepSeekMath: Pushing the limits of                introducing-gpt-5-5/
     mathematical reasoning in open language models,” arXiv:2402.03300,          [33] Anthropic, Claude Sonnet 4.6, 2026. [Online]. Available: https://www.
     2024.                                                                            anthropic.com/news/claude-sonnet-4-6
[12] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang,        [34] OpenAI, GPT-5.4 mini, 2026. [Online]. Available: https://developers.
     and W. Chen, “LoRA: Low-rank adaptation of large language models,”               openai.com/api/docs/models/gpt-5.4-mini
     in Proc. Int. Conf. Learn. Represent. (ICLR), 2022.                         [35] DeepSeek, DeepSeek-V3.2 Release, 2025. [Online]. Available: https://
[13] S. Polu and I. Sutskever, “Generative language modeling for automated            api-docs.deepseek.com/news/news251201
     theorem proving,” arXiv:2009.03393, 2020.
[14] S. Polu, J. M. Han, K. Zheng, M. Baksys, I. Babuschkin, and I. Sutskever,
     “Formal mathematics statement curriculum learning,” in Proc. Int. Conf.
     Learn. Represent. (ICLR), 2023.
[15] C. Kaliszyk, J. Urban, H. Michalewski, and M. Olsák, “Reinforcement
     learning of theorem proving,” in Proc. Adv. Neural Inf. Process. Syst.
     (NeurIPS), 2018.
[16] M. Wang, Y. Tang, J. Wang, and J. Deng, “Premise selection for theorem
     proving by deep graph embedding,” in Proc. Adv. Neural Inf. Process.
     Syst. (NeurIPS), 2017.
[17] G. Lample, T. Lacroix, M.-A. Lachaux, A. Rodriguez, A. Hayat,
     T. Lavril, G. Ebner, and X. Martinet, “HyperTree proof search for neural
     theorem proving,” in Proc. Adv. Neural Inf. Process. Syst. (NeurIPS),
     2022.
[18] R. Xin, C. Xi, J. Yang, F. Chen, H. Wu, X. Xiao, Y. Sun, S. Zheng,
     and M. Ding, “BFS-Prover: Scalable best-first tree search for LLM-based
     automatic theorem proving,” in Proc. 63rd Annu. Meeting Assoc. Comput.
     Linguistics (ACL), Vol. 1: Long Papers, 2025, pp. 32588–32599.
[19] A. Q. Jiang, W. Li, S. Tworkowski, K. Czechowski, T. Odrzygóźdź,
     P. Miłoś, Y. Wu, and M. Jamnik, “Thor: Wielding hammers to integrate
     language models and automated theorem provers,” in Proc. Adv. Neural
     Inf. Process. Syst. (NeurIPS), 2022.
[20] H. Xin, D. Guo, Z. Shao, Z. Z. Ren, Q. Zhu, B. Liu, C. Ruan,
     W. Li, and X. Liang, “DeepSeek-Prover: Advancing theorem proving in
     LLMs through large-scale synthetic data,” in Proc. NeurIPS Workshop
     Mathematical Reasoning and AI (MATH-AI), 2024.
[21] A. Gu, B. Piotrowski, F. Gloeckle, K. Yang, and A. H. Markosyan,
     “ProofOptimizer: Training language models to simplify proofs without
     human demonstrations,” in Proc. Int. Conf. Learn. Represent. (ICLR),
     2026.
[22] T. H. Trinh, Y. Wu, Q. V. Le, H. He, and T. Luong, “Solving olympiad
     geometry without human demonstrations,” Nature, vol. 625, pp. 476–482,
     Jan. 2024.
[23] Y. Chervonyi, T. H. Trinh, M. Olsák, X. Yang, H. H. Nguyen, M. Mene-
     gali, J. Jung, J. Kim, V. Verma, Q. V. Le, and T. Luong, “Gold-medalist
     performance in solving olympiad geometry with AlphaGeometry2,” J.
     Mach. Learn. Res., vol. 26, pp. 1–39, 2025.
