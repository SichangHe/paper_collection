                                                            Pessimistic Verification for Open-Ended Math Questions


                                                                   Yanxing Huang 1 Zihan Tang * 1 Zejin Lin * 1 Peng Li 2 Yang Liu 2 3


                                                                   Abstract                                        tasks. Beyond this achievement, their capability to verify
                                                                                                                   mathematical proofs is also becoming increasingly impor-
                                              Automatic verification is a critical component
                                                                                                                   tant. This is primarily reflected in the following aspects:
                                              in building math-solving agents and reinforce-
                                              ment learning, yet it often falls short in generaliz-                Verification lies in the central place of almost all agentic
arXiv:2511.21522v2 [cs.AI] 22 Jun 2026




                                              ability, performance, and cost-efficiency. Iden-                     workflows for math problem solving (Liu et al., 2025; Shao
                                              tifying that the primary bottleneck of verifica-                     et al., 2025; DeepSeek-AI et al., 2025b; Huang & Yang,
                                              tion lies in error detection capability, we propose                  2025; Varambally et al., 2025; Chen et al., 2025b; Achim
                                              pessimistic verification, a paradigm of agentic                      et al., 2025; Chen et al., 2025a). It is widely adopted and val-
                                              workflows that rejects a solution if any of mul-                     idated as an effective approach that enables further test-time
                                              tiple parallel verifiers identifies a flaw. We fur-                  scaling over long chain-of-thought. Some works claimed
                                              ther introduce progressive pessimistic verifica-                     to achieve IMO gold-medal level performance (Shao et al.,
                                              tion, which employs fine-grained proof decom-                        2025; DeepSeek-AI et al., 2025b; Huang & Yang, 2025)
                                              position to significantly enhance verification ac-                   where verification-based iterative workflows serve as the
                                              curacy and efficiency. Our approach surpasses                        crucial enabler.
                                              the performance and token efficiency of extended
                                                                                                                   Automatic verification is equally critical in reinforcement
                                              long chain-of-thought (long CoT) and mainstream
                                                                                                                   learning for large reasoning models (DeepSeek-AI et al.,
                                              verification workflows, crucially, our analysis
                                                                                                                   2025a; OpenAI et al., 2024). In many prominent recent stud-
                                              reveals that existing benchmarks underestimate
                                                                                                                   ies, both rule-based (DeepSeek-AI et al., 2025a; OpenAI
                                              its effectiveness on stronger models due to in-
                                                                                                                   et al., 2024) and LLM-based automated verification (Shao
                                              herent annotation errors. To further validate
                                                                                                                   et al., 2025; DeepSeek-AI et al., 2025b) methods have been
                                              the effectiveness of our method, we applied a
                                                                                                                   employed during training, yielding remarkable effective-
                                              verification-based solving workflow on the IMO
                                                                                                                   ness.
                                              2025 and MathArena Apex 2025 datasets, where
                                              the workflow with progressive pessimistic ver-                       Despite its importance, automatic verification for mathemat-
                                              ification exhibits remarkable improvements in                        ics remains fundamentally challenging:
                                              both efficiency and accuracy on highly challeng-
                                                                                                                   First, rule-based verification methods are highly efficient
                                              ing contest-level math problems with state-of-
                                                                                                                   and widely used in training, but they are restricted to prob-
                                              the-art models. Code is available at https:
                                                                                                                   lems whose answers can be deterministically checked, leav-
                                              //github.com/THUNLP-MT/pverify.
                                                                                                                   ing most open-ended mathematical questions beyond their
                                                                                                                   scope. They can not be used in agentic workflows for math
                                                                                                                   either.
                                         1. Introduction
                                                                                                                   Second, the absolute accuracy of LLM-based automatic ver-
                                         Since the release of OpenAI o1 (OpenAI et al., 2024) and                  ification is not satisfying yet. While the advancement of
                                         DeepSeek-R1 (DeepSeek-AI et al., 2025a), LLMs have                        LLMs has led to numerous AI systems assisting in mathe-
                                         achieved remarkable success in mathematical reasoning                     matical research, these workflows still rely heavily on hu-
                                            *
                                              Equal contribution 1 Qiuzhen College, Tsinghua University,           man verification and expert guidance (Liu et al., 2025; Bryan
                                         Beijing, China 2 Institute for AI Industry Research (AIR), Tsinghua       et al., 2026). A primary reason for this dependence is the
                                         University, Beijing, China 3 Dept. of Comp. Sci & Tech., In-              inadequate self-verification capability of AI systems, which
                                         stitute for AI, Tsinghua University, Beijing, China. Correspon-           renders their outputs unreliable.
                                         dence to: Peng Li <lipeng@air.tsinghua.edu.cn>, Yang Liu <li-
                                         uyang2011@tsinghua.edu.cn>.                                               Third, computational costs of verification severely limit
                                                                                                                   the applicability of AI systems in mathematical problem-
                                         Proceedings of the 43 rd International Conference on Machine              solving. For instance, the workflows employed by
                                         Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026
                                         by the author(s).                                                         DeepSeekMath-V2 (Shao et al., 2025) and DeepSeek-

                                                                                                               1
                                   Pessimistic Verification for Open-Ended Math Questions

V3.2 (DeepSeek-AI et al., 2025b) generate a vast number                 • We proposed three variants of pessimistic verification
of candidate proofs for each problem, subjecting each to 64               methods that could significantly enhance the verifica-
rounds of parallel independent verification. Consequently,                tion ability of large language models with a higher
solving a single IMO-level problem can consume at least                   efficiency than scaling long CoT.
thousands of API calls. There is, therefore, an urgent need
for more efficient methods for automatic verification.                  • We conducted comprehensive experiments to validate
We contend that the key limitation of automatic verification              our approach and to determine the actual capabilities of
lies in the ability of finding errors in a proof, which is                frontier models on IMO-level tasks within a controlled
supported by a series of recent works (Pandit et al., 2025;               budget.
Liu et al., 2025; Shao et al., 2025; Huang & Yang, 2025).
This brings us to the concept of pessimistic verification.
This method involves checking a proof multiple times via             2. Method
an LLM and marking it as incorrect the moment an error is
                                                                            Simple pes.@n                   Vertical pes.@k                                                           Progressive pes.@n/k
found. On the other hand, intuition tells us that verification




                                                                                                                                Partition into chunks of length k and verify
requires a careful examination of details rather than repeated             Proof:
                                                                        Proof:Proof:                     Proof:
                                                                                                                                                                                 Proof:
                                                                                                                                                                                      Proof: Proof:
                                                                           --------------------
                                                                        --------------------                                                                                     --------------------
                                                                                                                                                                                               --------------------




                                                                                                                                                                                                                      The minimum split length is k
rough checks. This leads to our new proof decomposition                       --------------------
                                                                           -------------                 --------------------                                                         --------------------
                                                                        -------------                                                                                            -------------
                                                                              -------------              -------------                                                                         -------------
                                                                                                                                                                                      -------------
                                                                           -----------------
                                                                        -----------------                                                                                        -----------------
                                                                              -----------------          -----------------                                                                     -----------------
and piecewise verification approach.                                    -- --                                                                                                    -- -----------------
                                                                              --                         --                                                                           --       --
                                                                           ------------------
                                                                        ------------------                                                                                       ------------------
                                                                              ------------------         ------------------                                                                    ------------------
                                                                                                                                                                                      ------------------
                                                                           ------------
                                                                        ------------                                                                                             ------------
                                                                              ------------               ------------                                                                          ------------
                                                                                                                                                                                      ------------
Based on these ideas, we designed and examined three vari-                 ----------
                                                                        ----------
                                                                              ----------                 ----------
                                                                                                                                                                                 ----------
                                                                                                                                                                                      --------------------
                                                                           ----------------
                                                                        ----------------                                                                                         ----------------
                                                                              ----------------           ----------------                                                                      ----------------
                                                                                                                                                                                      ----------------
ants: simple, vertical, and progressive pessimistic verifi-                --------
                                                                        --------
                                                                              --------                   --------
                                                                                                                                                                                 --------
                                                                                                                                                                                      -------- --------
                                                                           ---------------
                                                                        ---------------                                                                                          ---------------
                                                                              ---------------            ---------------                                                                       ---------------
                                                                                                                                                                                      ---------------
cation. The simple variant is very similar to mainstream                   ---------
                                                                        ---------
                                                                              ---------                  ---------
                                                                                                                                                                                 ---------
                                                                                                                                                                                               ---------
                                                                           QED.
                                                                        QED.                                                                                                     QED.---------
                                                                              QED.                       QED.                                                                         QED. QED.
solutions for automatic verification, while the progressive
                                                                       Prarllel review for n times                                                                             Iterate and subdivide up to n times
variant consistently achieves the best performance and effi-
                                                                        indicates the scope of a single veriﬁcation. All methods report false if any one of them ﬁnds an error.
ciency across all scenarios in our experiments. Its progres-
sive decomposition strategy will also become imperative              Figure 1. Three variants of pessimistic verification methods in this
when dealing with lengthy, intricate proofs, which is com-           work. In following experiments they will separately be denoted as
monly seen in research-level problems.                               “pes@n”, “vp@k”, and “prog@n/k”

We primarily conducted our experiments on two verifica-
tion benchmarks, Hard2Verify (Pandit et al., 2025) and               In Figure 1, we illustrate the three main pessimistic verifi-
IMO-GradingBench (Luong et al., 2025). They are both                 cation variants discussed in this paper. All three methods
contest-level math verification benchmarks with expert an-           subject a single proof to multiple rounds of verification,
notations. We also conducted some experiments on a home-             adopting the first identified error as the final verification
made undergraduate-level math problem dataset for verifica-          result. The primary distinction between them lies in the
tion performance, which effectively complements existing             specific construction of these verification rounds. Here we
elementary math datasets.                                            will provide some detailed explanation for them.

Progressive pessimistic verification not only boosts perfor-         2.1. Simple Pessimistic Verification
mance across these datasets but also shows better scaling
efficiency than long chain-of-thought. Notably, our case             The most straightforward approach to automatic verification
studies with state-of-the-art models uncovered many errors           using an LLM is to directly prompt the model to inspect the
missed by the original labels, suggesting that these bench-          entire proof for potential errors, which we refer to as stan-
marks are no longer reliable on cutting-edge LLMs.                   dard verification. Simple pessimistic verification constructs
                                                                     its multiple rounds by simply repeating standard verification
Given the limitations of verification benchmarks, we further         process for n times in parallel.
tested our method on IMO 2025 (Balunović et al., 2025)
and MathArena Apex 2025 (Balunović et al., 2025) for                This direct parallel verification scheme represents the cur-
agentic problem solving with self-verification. The results          rent mainstream approach in verifier-aided problem solving
also confirm that progressive pessimistic verification brings        and has been adopted by numerous related works (Liu et al.,
significant gains in both performance and efficiency.                2025; Shao et al., 2025; Huang & Yang, 2025). While
                                                                     the handling of verification results varies across these stud-
Our main contributions are:                                          ies, they generally emphasize the importance of negative
                                                                     verdicts. However, previous works have not rigorously ex-
   • Our study highlights and investigates the cost ineffi-          amined this approach as a standalone verification method.
     ciencies widespread in current math reasoning work-             In this work, simple pessimistic verification can also be
     flows, providing a new perspective for the community.           viewed as a representative baseline.

                                                                 2
                                                            Pessimistic Verification for Open-Ended Math Questions

2.2. Vertical Pessimistic Verification                                                                                       in which case the maximum number of checks performed
                                                                                                                             on a single proof is 2n − 1. We also introduced a parameter
In spite of simply applying multiple reviews on the whole
                                                                                                                             k to set a lower bound on the segmentation size, which pre-
proof, we also explored a pessimistic verification from an-
                                                                                                                             vents the proofs from being over-segmented in subsequent
other dimension. As shown in Figure 2, we adopted a special
                                                                                                                             iterations.
prompting method and require the LLM to focus on a certain
part of the proof, and try looking deep into these contents to                                                               This method combines the strengths of the other two and
find errors. Vertical pessimistic verification adopts a hyper-                                                               demonstrates the highest efficiency and performance ceiling
parameter k, it first splits the whole proof into chunks with                                                                in our experiments.
at most k lines, and create a series of parallel review tasks
for each chunk. Although this method only goes through                                                                       3. Experiments
the proof once, we also witnessed improved performance
in error detection over single-pass whole proof verification                                                                 3.1. Datasets and Metrics
and even simple pessimistic verification under similar com-
                                                                                                                             In our experiments we primarily use three datasets for evalu-
putational budget.
                                                                                                                             ation, and we constantly use the same prompt and workflow
 Vertical review prompting in vertical and progressive methods                                                               setting across all these dataset. Here are some descriptions
 Proof:
 --------------------
                           Instruct:
                           ------------------    <problem/>                                       <think>
                                                                                                                             about them:
 -------------             ----------            <complete_proof/>                                --------------
 -----------------         1. -----------        <chunk>                                          ...
 --                        2. -------------      --------                                         </think>
 ------------------
 ------------
                           3. ---------------    ---------------             completion via LLM
                                                                                                  <verif>false</verif>
                                                                                                  Here are some
                                                                                                                                • IMO-GradingBench (Luong et al., 2025). This
                           4. ---------          ---------
 ----------                                                                                       descriptions of the
 ----------------
                           Your task: Check
                           only the given
                                                 QED.
                                                 </chunk>                                         error detected.
                                                                                                                                  dataset contains 1,000 human-graded solutions to IMO-
 --------                  chunk for errors.                                                      -------------------
 ---------------
 ---------
                           ---------------      The complete proof is also                        -----------.                    level proof problems from IMO-ProofBench (Luong
                                                provided for context.
 QED.
                                                                                                                                  et al., 2025), from which we selected a subset with
                                                                                                                                  300 samples for evaluation. This is a challenging test
Figure 2. The vertical review prompting method used in vertical
pessimistic verification and progressive pessimistic verification.                                                                of fine-grained mathematical proof evaluation. Test
                                                                                                                                  results on the IMO-GradingBench subset mirror those
Concurrently, we also observed a positive scaling trend                                                                           of the complete dataset, thereby validating its represen-
of vertical pessimistic verification as its segmentation be-                                                                      tativeness for our experiments.
comes increasingly refined. However, hyperparameter se-                                                                         • Hard2Verify (Pandit et al., 2025). Hard2Verify con-
lection remains a challenge. While fine-grained verification                                                                      tains 200 challenging problems and solutions from
is necessary to detect subtle errors within proofs, applying                                                                      recent math competitions such as IMO and Putnam.
it uniformly incurs a high cost for detecting easily discover-                                                                    The solutions are generated by strong models such as
able errors. This trade-off inspired us to design a verifica-                                                                     GPT-5 (Singh et al., 2025) and Gemini 2.5 Pro (Huang
tion scheme capable of dynamically selecting segmentation                                                                         & Yang, 2025) and annotated by humans.
granularity, leading to the development of progressive pes-
simistic verification.                                                                                                          • QiuZhen-Bench (annotated by GPT-5). QiuZhen-
                                                                                                                                  Bench is a high-quality advanced math problem dataset.
2.3. Progressive Pessimistic Verification                                                                                         This dataset is sourced from challenging university-
                                                                                                                                  level math competitions and doctoral qualifying exams
Progressive pessimistic verification combines the mecha-
                                                                                                                                  well-known for their difficulty. Given the limitation of
nism of both simple and vertical methods. It performs multi-
                                                                                                                                  human annotation discussed in Section 3.4, we used
scale verification, ranging from the level of the whole proof
                                                                                                                                  strong language models to generate proofs and anno-
down to detailed steps similar to vertical pessimistic veri-
                                                                                                                                  tations for this dataset. Then it is used to automati-
fication. This allows it to quickly filter out obvious errors
                                                                                                                                  cally evaluate weaker models. You can refer to Ap-
in the proof, and then drill down into the detailed steps to
                                                                                                                                  pendix A.2 for more details of the construction of this
carefully examine the correctness of each part.
                                                                                                                                  dataset.
Progressive pessimistic verification naturally supports prun-
ing operations, thereby further improving its execution ef-                                                                  All evaluation in our experiments was conducted at the re-
ficiency. It begins with iterative verification on a single                                                                  sponse level, where we require the verifier to decide whether
complete proof, and after each iteration, the proof is sub-                                                                  the whole proof is correct instead of providing a score or
divided in half and each part is evaluated separately in the                                                                 step-level evaluation. For IMO-GradingBench, only the re-
manner shown in Figure 2. After every iteration, proofs in                                                                   sponses that obtained fully 7 points are considered correct,
which errors have been detected are filtered out, and ver-                                                                   otherwise they will all be considered false. And aside from
ification continues on the remaining proofs. We use the                                                                      our experiments, we will use standard verification and sim-
parameter n to control the maximum number of iterations,                                                                     ple pessimistic verification as the baseline, as they are the

                                                                                                                         3
                                     Pessimistic Verification for Open-Ended Math Questions

most representative among mainstream applications. In all                1.00
                                                                                              GPT-5-mini                   1.0
                                                                                                                                           Qwen3-30B-A3B
our experiments we set the temperature parameter to 1.0 to               0.95                                              0.9
ensure diversity of the responses.                                       0.90
                                                                                                                           0.8
                                                                         0.85
                                                                                                                           0.7
In this work, we treat mathematical proof verification as a              0.80
                                                                                                                           0.6
binary classification problem and focus on the following                 0.75
                                                                                                                           0.5
                                                                         0.70
performance metrics:
                                                                         0.65                                              0.4

                                                                         0.60 1   2   3   4    5   6   7   8   9 10 11 12 0.3 1   2    3   4    5   6   7   8   9 10 11 12
   • True Negative Rate (TNR): The proportion of de-                                          Num of Reviews                                   Num of Reviews
     tected errors among all erroneous proofs. This is the                                     pes@n Bal. F1           pes@n TPR                 maj@n TNR
                                                                                               pes@n TNR               maj@n Bal. F1             maj@n TPR
     primary metric for evaluating the model’s ability to
     identify incorrect proofs.                                         Figure 3. The comparison of simple pessimistic verification and
   • True Positive Rate (TPR): The proportion of proofs                 majority voting on the subset of IMO-GradingBench. The former
                                                                        exhibits steady performance gains as sampling budget increases,
     classified as correct among all truly correct proofs.              whereas the latter shows almost no changes in performance.
     This helps assess the model’s proof-verification capa-
     bility.
                                                                        questions, which is comparable in size to the other datasets,
   • Balanced F1 Score: The harmonic mean of TPR and
                                                                        is sufficiently representative. Accordingly, all further exper-
     TNR, providing a balanced indicator of performance
                                                                        iments except for case studies on IMO-GradingBench were
     when both false positives and false negatives matter.
                                                                        conducted using this subset.
     This is also the primary indicator used in Pandit et al.
     (2025).                                                             Table 1. Comparison of the evaluation metrics of GPT-5-mini on
                              2 · TPR · TNR                              the full set and subset of IMO-GradingBench. Results indicate
                Balanced F1 =                                (1)         that this subset of 300 questions is already representative for
                               TPR + TNR                                 the verification performance. Here standard method refers to
                                                                         directly prompting the LLM to verify the given proof.
3.2. Preliminary Experiments
                                                                            Method                                Size       TPR               TNR          Bal. F1
Prior to presenting the main experimental results, we have
included results from preliminary experiments to justify our                                                    1,000        0.917             0.660            0.768
                                                                            standard
choice of experimental design.                                                                                    300        0.923             0.675            0.780
Firstly, we briefly explore the mechanism behind the effec-                                                     1,000        0.850             0.816            0.833
                                                                            progressive@3/6
tiveness of pessimistic mechanism. Since the intrinsic diffi-                                                     300        0.857             0.842            0.849
culty of proof verification lies in identifying errors, detecting
an error during multi-round verification is inherently a low-
probability event. Pessimistic verification methods effec-              3.3. Main Results on Verification Benchmarks
tively amplify the probability of this detection. Meanwhile,
                                                                        We begin by conducting some scaling experiments to test the
since current language models typically provide sound rea-
                                                                        effect of hyperparameter settings in pessimistic verification
soning and explanations before pinpointing an error, actual
                                                                        methods. We primarily examined two representative models
false negatives are rare. Consequently, the overall verifica-
                                                                        in these experiments, GPT-5-mini (Singh et al., 2025) and
tion performance is improved.
                                                                        Qwen3-30B-A3B (Yang et al., 2025). They could reflect
We can contrast this with majority voting, a widely popular             the performance gains of language models of medium and
test-time scaling method. It fails to help the model better             small sizes. We did not conduct scaling experiments on
identify errors, rendering it nearly ineffective for verifica-          large models since these benchmarks are already unreliable
tion tasks (Pandit et al., 2025; Mahdavi et al., 2025b). Our            for them.
preliminary experimental results, shown in Figure 3, corrob-
                                                                        The results of our scaling experiments are summarized in
orate this reasoning: Majority Voting is basically ineffective,
                                                                        Figure 4. These experiments showed similar trend of our
whereas Pessimistic Verification methods demonstrate not
                                                                        methods. All three types of pessimistic verifications con-
only effectiveness but also stable scaling potential. And for
                                                                        stantly benefit from scaling up computational budget. The
this reason, we exclude majority voting from comparisons
                                                                        performance of the vertical pessimistic method appears to
in our subsequent experiments.
                                                                        be more influenced by the specific dataset, but when the
We also benchmarked two representative LLMs against both                segmentation is sufficiently fine-grained, it does indeed im-
the full and partial IMO-GradingBench sets. The consistent              prove performance while the proof has been read through
results shown in Table 1 confirm that the subset with 300               only once. Its inefficiency stems largely from token wastage

                                                                    4
                                                                                Pessimistic Verification for Open-Ended Math Questions

                                       Efficiency Curves: IMO-GradingBench                                               1.0                                                                  IMO-GradingBench
                                     GPT-5-mini                                           Qwen3-30B-A3B                  0.9
                                                                                                                         0.8
              0.86                                                   0.80                                                0.7
              0.84                                                   0.75                                                0.6
                                                                                                                         0.5            Standard TPR
Balanced F1




              0.82                                                   0.70                                                               Progressive TPR
                                                                                                                         0.4            TPR loss (std vs prog)
              0.80                                                                                                       0.3            Standard TNR
                                                                     0.65                                                               Progressive TNR
                                                                                                                         0.2
              0.78                                                                                                                      Standard Bal. F1
                                                                     0.60                                                0.1            Progressive Bal. F1
              0.76                                                                                                       0.0
                                                                     0.55                                                               ini               -5            xp           ew     Pro         Flas
                                                                                                                                                                                                             h     ew      4.5          A3B    -4B 3-1.7B
                                                                                                                                  -5-m               GPT V3.2 E                 revi    2.5                    revi onnet            0B- Qwen3
              0.74                                                   0.50                                                      GPT                          e ek           Pro P emini         in i 2.5 lash P        e S    e n 3-3              Qwe
                                                                                                                                                                                                                                                      n
                                                                                                                                                          s          ini 3          G        m              F       d     Qw
                     0      5000     10000       15000   20000              0      5000    10000   15000    20000                                   Dee
                                                                                                                                                        p                                 Ge          ini 3    Clau
                                                   Equivalent output tokens / sample                                                                             Gem                            G e m

                         progressive                 simple pessimistic         progressive (low reasoning_effort)       1.0                                                                         Hard2Verify
                         vertical pessimistic        standard long CoT          simple pes. (low reasoning_effort)       0.9
                                                Efficiency Curves: Hard2Verify                                           0.8
                                                                                                                         0.7
                                     GPT-5-mini                                           Qwen3-30B-A3B                  0.6             Standard TPR
              0.90                                                                                                       0.5             Progressive TPR
              0.88                                                   0.80                                                0.4             TPR loss (std vs prog)
                                                                     0.75                                                0.3             Standard TNR
              0.85                                                                                                                       Progressive TNR
                                                                     0.70                                                0.2             Standard Bal. F1
Balanced F1




              0.83                                                                                                       0.1
                                                                     0.65                                                                Progressive Bal. F1
              0.80                                                                                                       0.0
                                                                                                                                        -5            ro          ini      ew      ash .2 Exp review                    .5     B      B        B
              0.78                                                   0.60                                                          G P T          .5 P      -5-m      revi    5 Fl                                  et 4 30B-A3 wen3-4 en3-1.7
                                                                                                                                            ini 2        GPT 3 Pro P mini 2.             k V3 Flash P           onn        3-    Q     Qw
              0.75                                                   0.55                                                              Gem                    i ni      G e      e p See       i 3     la u de S Qwen
                                                                                                                                                          Gem                 De             in      C
              0.73                                                   0.50                                                                                                              Gem
              0.70                                                   0.45
                     0      5000     10000       15000   20000              0      5000    10000   15000    20000                 1.0                                            QiuZhen-Bench (Annotated by GPT-5)
                                                   Equivalent output tokens / sample                                              0.9
                                                                                                                                  0.8
                         progressive                 simple pessimistic         progressive (low reasoning_effort)                0.7
                         vertical pessimistic        standard long CoT          simple pes. (low reasoning_effort)                0.6
                                                                                                                                                    Standard TPR
                         Efficiency Curves: QiuZhen-Bench (Annotated by GPT-5)                                                    0.5
                                                                                                                                  0.4
                                                                                                                                                    Progressive TPR
                                                                                                                                                    TPR loss (std vs prog)
                                     GPT-5-mini                                           Qwen3-30B-A3B                           0.3               Standard TNR
                                                                                                                                  0.2               Progressive TNR
                                                                                                                                                    Standard Bal. F1
              0.80                                                    0.7                                                         0.1               Progressive Bal. F1
                                                                                                                                  0.0
              0.70                                                                                                                                  Exp             ini                                   B              B                4.5         4B
                                                                      0.6                                                                                      -5-m             Prev
                                                                                                                                                                                     iew              -A3           n3-
                                                                                                                                                                                                                        8
                                                                                                                                                                                                                                    net            n3-           1.7B
                                                                                                                                              3.2                                                 30B         Qwe                               Qwe           n3-
Balanced F1




              0.60                                                                                                                   ek V                   GPT            lash             e n3-                           de   Son                       Qwe
                                                                                                                                   Se                                    F                w
                                                                      0.5                                                  D   eep                                 ini 3                Q                              Clau
              0.50                                                                                                                                            Gem
              0.40                                                    0.4

              0.30                                                    0.3                                                Figure 5. The main benchmark results on IMO-GradingBench,
              0.20                                                    0.2                                                Hard2Verify and QiuZhen-Bench. Thinking mode is enabled for all
                     0      5000     10000       15000   20000              0      5000    10000   15000    20000
                                                   Equivalent output tokens / sample                                     models if possible, and the reasoning effort is set to medium when
                         progressive                 simple pessimistic         progressive (low reasoning_effort)       supported. This method constantly improves the classification
                         vertical pessimistic        standard long CoT          simple pes. (low reasoning_effort)       performance across almost all tested models. Models are sorted by
                                                                                                                         their Bal. F1 score under prog@3/6.
Figure 4. The response-level performance and efficiency of pes-
simistic verification methods on three verification datasets. The
equivalent output tokens is calculated by weighting the model’s
input and output token prices. For GPT-5-mini and Qwen3-30B-                                                             the hyperparameter setting progressive@3/6 for balanced
A3B it is (Output + Input / 8). The reasoning effort of Qwen series                                                      performance and efficiency. From these graphs we can read
models can not be adjusted so we excluded long-CoT results of                                                            several key findings:
them. These results indicate that pessimistic verification has stable
and efficient scalability.
                                                                                                                                • Error detecting is the key ability that separates strong
                                                                                                                                  verifiers from the weak which is also discovered in
                                                                                                                                  some recent works (Pandit et al., 2025). On all datasets
 caused by fixed verification precision, a critical issue that                                                                    the TPR is almost the same across all models from
 can be effectively resolved through progressive segmenta-                                                                        strong to weak, while TNR varies a lot.
 tion. And as the combination of simple and vertical methods,
 progressive pessimistic verification constantly exhibits the                                                                   • Merely from statistics we can see that progressive pes-
 highest performance and efficiency. Moreover, on models                                                                          simistic verification can significantly increase TNR
 that the length of chain-of-thought is controlable (i.e. GPT-                                                                    and balanced F1 score for most models, with a small
 5-mini), simple and progressive methods constantly exhibits                                                                      tradeoff of TPR.
 higher efficiency in test-time scaling than long CoT. Their
 parallel nature makes them even faster than long chains of                                                                     • Weaker models tend to exhibit higher performance
 reasoning.                                                                                                                       gains with a greater degression of TPR. The consis-
                                                                                                                                  tency on positive samples is also an important indicator
Then we have also conducted vast experiments with stan-                                                                           of the verification ability of LLMs.
dard and progressive pessimistic verification methods across
different models on all three datasets, and the main results                                                                    • In fact, based on more fine-grained case studies in
is summarized in Figure 5. In these experiments we use                                                                            Section 3.4, we found that for stronger models, the

                                                                                                                     5
                                      Pessimistic Verification for Open-Ended Math Questions

     decrease in TPR is largely an illusion caused by dataset             annotators. This indicates, on one hand, that our previous
     annotation, and the actual performance improvement                   experiments substantially underestimated the verification
     is being underestimated.                                             capability of stronger models, and on the other hand, it
                                                                          supports the validity of using GPT-5 to annotate QiuZhen-
3.4. Case Study                                                           Bench. Meanwhile, many smaller models do indeed produce
                                                                          a large number of unwarranted False Negative judgments.
To better analyze performance beyond aggregated statistics
and reflect more realistic behavior, we also conducted a de-              3.5. Problem-Solving Experiments
tailed case study on the results of the pessimistic verification.
In this evaluation, we focus primarily on the False Negative              Progressive pessimistic verification exhibits strong perfor-
cases, because TP and TN generally represent correct clas-                mance and efficiency in many proof evaluation benchmarks
sifications, while most FP cases occur simply because our                 on language models of smaller sizes. However, all these
verifier failed to detect existing errors in the proof. FN cases          benchmarks annotated by either human experts or LLMs
are usually the most informative.                                         fail to measure reliably the verification performance accord-
                                                                          ing to our case studies. To further promote the value of
The statistical results of our case study can be found in                 pessimistic verification methods, we have also done a series
Table 2. In the Appendix A.4, we also provide several                     of experiments in problem solving with verification-based
concrete examples of mislabeling in the original dataset,                 agentic workflows. We designed a simple iterative workflow
and the full set of cases we examined is available in our                 similar to Huang & Yang (2025), which is shown in Fig-
open-source code repository. Our classification criteria are              ure 6. The effectiveness of pessimistic verification on them
based on whether the errors identified by these models in                 could be reflected by problem solving experiments here. We
FN cases are:                                                             primarily used Gemini 3 series models for problem-solving
                                                                          experiments for their advanced reasoning ability.
   • Critical. If our verifier does uncover a critical error
     that was overlooked in the original dataset annotation,
                                                                                              inference via LLM
     or a difficult-to-resolve tricky skip, it directly affects               problem                              solution
     the correctness of the entire proof.
   • Minor. If our verifier identified a typo or minor errors
     that can be easily fixed. In such cases, whether it should                                   error
                                                                                                  correction                   veriﬁcation
     be judged as an error depends entirely on subjective
     criteria.
                                                                                                          no

   • Nonsense. If our verifier misunderstands the problems
                                                                                                    yes        passed or hit
     and produces some unwarranted judgments. These are                       ﬁnal solution                    maximum iteration?
     the truly harmful false negatives.
                                                                          Figure 6. Flow diagram of our problem solving workflow. This
                                                                          pipeline is adopted by experiments on IMO 2025 and MathArena
Table 2. Manual review of FN cases in progressive pessimistic             Apex 2025 dataset. Note that the number of iterations of this work-
verification on IMO-GradingBench. The classification is based             flow is largely dependent on the performance of the verification
on whether the judgments provided by the verifier in these FN             method and the inherent problem-solving ability of the LLM.
cases are critical, minor, or nonsense. These cases are regarded as
false in benchmarks, while a large percentage of them generated
by state-of-the-art models actually discovered new critical errors        We used two extremely hard datasets to evaluate the perfor-
ignored in the dataset annotation.                                        mance of problem solving with this workflow:
 Model                    Critical Minor Nonsense Total
                                                                             • IMO 2025 (Balunović et al., 2025). This dataset con-
 Gemini 3 Pro Preview          8         0          2        10                tains 6 problems from the 66th International Mathe-
 GPT-5                         9         9          2        20                matical Olympiad (IMO) contest at the year 2025. We
 GPT-5-mini                  10          6          4        20                collected the output proofs of our workflow and man-
 Qwen3-30B-A3B                 1         1         18        20
                                                                               ually reviewed each output with the provided grading
                                                                               scheme.

We found that most of the FN cases produced by GPT-5-                        • MathArena Apex 2025 (Balunović et al., 2025). Apex
mini or stronger models under pessimistic verification did                     2025 contains 12 problems from various math compe-
in fact identify real, critical errors in the proofs. These                    titions in 2025. These questions have been specially
errors had been mistakenly labeled as correct by the dataset                   selected to exceed the average difficulty of IMO compe-

                                                                      6
                                     Pessimistic Verification for Open-Ended Math Questions

     tition problems. They also come with standard answers,                                            Performance vs. Efficiency of Gemini 3 Pro Preview on Apex 2025
     allowing for convenient automatic grading.                                                 0.40

                                                                                                0.35
In our experiments on the IMO 2025 dataset, we selected the




                                                                        Ground Truth Accuracy
results from the final iteration of each method and performed                                   0.30

manual evaluation on every problem. Conversely, for the                                         0.25
Apex 2025 dataset, we plotted accuracy and cost curves                                          0.20
across workflow iterations by verifying against standard
                                                                                                0.15
answers. Given the small size of the Apex 2025 dataset                                                                                                               w/ progressive@4/4
                                                                                                0.10                                                                 w/ pessimistic@12
and the potential for significant experimental variance, we
repeated the tests three times for each setting and plotted all                                         1          2              3               4              5               6
                                                                                                                 Equivalent Output Token Usage (Millions) (Output + Input / 6)
resulting curves within a single figure.
                                                                                                       Performance vs. Efficiency of Gemini 3 Flash Preview on Apex 2025
Furthermore, regarding token consumption, we calculate the                                      0.25
cumulative tokens from every API call made until a proof is                                                                                                          w/ progressive@4/4
                                                                                                                                                                     w/ pessimistic@12
finally accepted, including the final successful verification                                   0.20




                                                                        Ground Truth Accuracy
step. This metric best reflects real-world usage scenarios.
                                                                                                0.15
The reported cost is expressed as equivalent output tokens,
a weighted figure based on API pricing. For the Gemini 3                                        0.10
model series, this is calculated as: Output + Input / 6.
                                                                                                0.05
Table 3. Performance comparison on the IMO 2025 dataset across
different methods with Gemini 3 Pro Preview. Scores for Problems                                0.00
1–6 (P1–P6) are reported out of 7. The token usage is measured by                                           2              4                  6                  8                   10
                                                                                                                 Equivalent Output Token Usage (Millions) (Output + Input / 6)
equivalent output tokens. Among three methods, “direct” refers
to directly prompting the LLM to solve these problems without           Figure 7. Performance of Gemini 3 series models on the Math-
verification-based workflow.                                            Arena Apex 2025 dataset using the iterative tuning workflow with
                                                                        different verification schemes. Given the limited dataset size and
  Method             direct    w/ pes@12       w/ prog@4/4              high testing costs, three experimental trials were conducted for
                                                                        each setting and plotted within the same figure. It is evident that
  P1                   2            2                 6                 performance improves significantly as iterations progress across
  P2                   0            0                 0                 all settings, with the progressive verification demonstrating notably
                                                                        higher efficiency.
  P3                   0            6                 7
  P4                   5            5                 5
  P5                   6            4                 4
  P6                   0            0                 0                 2025; Achim et al., 2025).
  Total Score         13           17               22                  At the same time, the performance gains on the Apex 2025
  Token Usage        129K        1,310K            985K                 dataset are much more significant, owing to its higher av-
                                                                        erage difficulty compared to IMO 2025. Although we ob-
The performance of Gemini 3 pro with different verification             served instances where correct solutions were erroneously
methods is shown in Table 3, and the performance-efficiency             modified during the process, the final accuracy at the termi-
curve of Gemini series models on Apex 2025 dataset is                   nation of the last iteration showed a significant improvement.
shown in Figure 7. We can read several observations by                  Furthermore, our proposed progressive pessimistic verifica-
looking into the cases of these results:                                tion scheme demonstrates clear efficiency advantages over
                                                                        the currently prevalent naive parallel verification methods.
Initially, while the Gemini 3 Pro model could arrive at the
correct final solution on the IMO 2025 dataset, its derivation
process is often marred by errors and gaps, precluding it               4. Related Work
from securing full marks during our evaluation. Subsequent
                                                                        4.1. Informal Verification in Math
self-verification and iterative refining yielded noticeable
improvements, while progressive pessimistic verification ex-            Using LLM for evaluation or verification tasks is a natural
hibited the best performance and efficiency. Notably, Prob-             idea. At the early development stage of LLM, some works
lem 6 (P6) in IMO 2025 remains particularly challenging for             have already tried this method on traditional tasks in natural
language models, likely due to its demand for substantial               language processing (Liu et al., 2023; Zheng et al., 2023).
geometric intuition. To date, it remains unsolved across                The open-ended math problem lies between the math an-
nearly all existing studies (Shao et al., 2025; Luong et al.,           swering problem and other evaluation problems. It lacks

                                                                    7
                                     Pessimistic Verification for Open-Ended Math Questions

simple and direct means of verification, but its correctness            satisfy the requirements of most practical applications.
is entirely objective. There are numerous works that focus
on leveraging the internal capability of the LLM to achieve             5. Conclusion and Discussion
automatic evolution in mathematics (Liu et al., 2025; Huang
& Yang, 2025; Xu et al., 2026; Shao et al., 2025; DeepSeek-             In this work we proposed and analyzed pessimistic verifi-
AI et al., 2025b; Zuo et al., 2025). These methods yield                cation, among which progressive pessimistic verification
significant performance improvements without depending                  exhibits strong performance and token efficiency on verifi-
on verifiable reward in math or code.                                   cation tasks. Its effectiveness is further validated in agentic
                                                                        problem-solving tasks with frontier LLMs.
Some works in this area primarily focus on the alignment
of LLM grading and that of humans. Certain agentic work-                Beyond the specific implementation of this mathematical
flows could enhance this ability (Mahdavi et al., 2025a;b;              proof verification scheme and the experimental results, we
Luong et al., 2025), while reinforcement learning for grad-             believe that two key underlying philosophies deserve greater
ing also exhibits effectiveness on small models (Dekoninck              attention:
et al., 2025). However, this research direction differs from
ours. While aligning grading criteria is a meaningful en-                  • The first is the error-centric verification philosophy.
deavor, it involves significant subjective factors, which di-                Among verification outcomes, those identifying errors
verges from the objective error detection we focus on. Some                  possess significantly higher information content, war-
works also highlights the importance of error detection, as                  ranting greater attention and prioritization. Moreover, a
this is the key ability that separates strong verifiers from                 strict pessimistic verification approach facilitates prun-
weaker ones (Pandit et al., 2025; Jain et al., 2025). But they               ing, thereby further enhancing algorithmic efficiency.
did not build or validate a effective verification approach
in math with this intuition. Before the release of this work               • The second is the strategy of segment-wise partition-
there is no well-known and scalable method that could en-                    ing and meticulous proof scrutiny. Whether verifying
hance this ability other than long CoT or multiple simple                    mathematical proofs or debugging code, it is essential
verifications with following process (Pandit et al., 2025).                  to devote substantial effort to examining the minute de-
                                                                             tails within the process, rather than merely conducting
                                                                             repeated, superficial reviews. This may be one of the
4.2. Formal Verification
                                                                             reasons why the efficiency of progressive pessimistic
Another possible solution to verifying mathematical proofs                   verification significantly outperforms that of simple
is through formal theorem provers such as Lean (Chen                         pessimistic verification.
et al., 2025b; Varambally et al., 2025; Chen et al., 2025a),
which could provide completely reliable verification on                 Furthermore, the significance of our method and automatic
math proofs. It is the verification method that distinguishes           verification may also be reflected in the following aspects:
formal mathematics from informal mathematics.
                                                                           • This method can further push the capability frontier
Some works also claim the ability of achieving IMO gold-
                                                                             of state-of-the-art large models, so there is an oppor-
medal with formal provers and verification-based work-
                                                                             tunity to incorporate it into the training pipeline to
flows (Hubert et al., 2025; Achim et al., 2025), while the
                                                                             further raise the upper limit of large models’ abili-
overall performance of formal theorem provers still falls be-
                                                                             ties in verification and rigorous reasoning tasks. This
hind provers in natural language by a large margin (Dekon-
                                                                             would be especially important for open-ended, long-
inck et al., 2025). Verification also dominates the cost of
                                                                             form tasks (Sinha et al., 2025).
formal theorem proving. In formal proving, we are required
to perform highly complex autoformalization of a proof to                  • In many software engineering applications, pessimistic
accommodate formal verification (Varambally et al., 2025;                    verification may also be useful. We might also be
Chen et al., 2025b; Hubert et al., 2025; Achim et al., 2025).                able to use progressive verification to quickly identify
For example in Hilbert (Varambally et al., 2025) the work-                   potential issues in code without the need to design test
flow requires hundreds of API calls and millions of tokens                   cases or execute the code. Progressive segmentation
on average only to solve one problem from Putnam dataset.                    will be a necessary technique since the context of code
While the informal verification discussed in this paper does                 could be extremely lengthy.
not ensure total accuracy, it offers a viable compromise by
trading strict rigor for greater ease of use and cost-efficiency.          • Aside from concrete use cases, the ability to verify
Given that the evolution of human mathematics has not                        should be viewed as a core part of general intelligence.
invariably depended on absolute rigor, we posit that once                    Exploring methods to raise the ceiling of automatic
informal verification achieves sufficient performance, it will               verification and improve the fundamental abilities of
                                                                             LLMs remains an endeavor of enduring value.

                                                                    8
                                    Pessimistic Verification for Open-Ended Math Questions

Acknowledgement                                                          arxiv.org/abs/2507.23726. arXiv:2507.23726
                                                                         [cs].
This work is supported by the National Natural Science
Foundation of China (No. 62276152, 62236011), fund-                    DeepSeek-AI, Guo, D., Yang, D., Zhang, H., Song, J., Wang,
ing from Wuxi Research Institute of Applied Technologies,                P., Zhu, Q., Xu, R., Zhang, R., Ma, S., Bi, X., Zhang,
Tsinghua University under Grant 20242001120, and Key                     X., Yu, X., Wu, Y., Wu, Z. F., Gou, Z., Shao, Z., Li, Z.,
Laboratory of Ethnic Language Intelligent Analysis and                   Gao, Z., Liu, A., Xue, B., Wang, B., Wu, B., Feng, B.,
Security Governance of MOE, Minzu University of China,                   Lu, C., Zhao, C., Deng, C., Zhang, C., Ruan, C., Dai, D.,
Beijing, China.                                                          Chen, D., Ji, D., Li, E., Lin, F., Dai, F., Luo, F., Hao, G.,
                                                                         Chen, G., Li, G., Zhang, H., Bao, H., Xu, H., Wang, H.,
Impact Statement                                                         Ding, H., Xin, H., Gao, H., Qu, H., Li, H., Guo, J., Li, J.,
                                                                         Wang, J., Chen, J., Yuan, J., Qiu, J., Li, J., Cai, J. L., Ni,
This paper presents work whose goal is to advance the field              J., Liang, J., Chen, J., Dong, K., Hu, K., Gao, K., Guan,
of Machine Learning. There are many potential societal                   K., Huang, K., Yu, K., Wang, L., Zhang, L., Zhao, L.,
consequences of our work, none which we feel must be                     Wang, L., Zhang, L., Xu, L., Xia, L., Zhang, M., Zhang,
specifically highlighted here.                                           M., Tang, M., Li, M., Wang, M., Li, M., Tian, N., Huang,
                                                                         P., Zhang, P., Wang, Q., Chen, Q., Du, Q., Ge, R., Zhang,
References                                                               R., Pan, R., Wang, R., Chen, R. J., Jin, R. L., Chen, R.,
                                                                         Lu, S., Zhou, S., Chen, S., Ye, S., Wang, S., Yu, S., Zhou,
Achim, T., Best, A., Der, K., Fédérico, M., Gukov, S.,                 S., Pan, S., Li, S. S., Zhou, S., Wu, S., Ye, S., Yun, T.,
  Halpern-Leister, D., Henningsgard, K., Kudryashov, Y.,                 Pei, T., Sun, T., Wang, T., Zeng, W., Zhao, W., Liu, W.,
  Meiburg, A., Michelsen, M., Patterson, R., Rodriguez,                  Liang, W., Gao, W., Yu, W., Zhang, W., Xiao, W. L., An,
  E., Scharff, L., Shanker, V., Sicca, V., Sowrirajan, H.,               W., Liu, X., Wang, X., Chen, X., Nie, X., Cheng, X., Liu,
  Swope, A., Tamas, M., Tenev, V., Thomm, J., Williams,                  X., Xie, X., Liu, X., Yang, X., Li, X., Su, X., Lin, X., Li,
  H., and Wu, L. Aristotle: IMO-level Automated Theorem                  X. Q., Jin, X., Shen, X., Chen, X., Sun, X., Wang, X.,
  Proving, October 2025. URL http://arxiv.org/                           Song, X., Zhou, X., Wang, X., Shan, X., Li, Y. K., Wang,
  abs/2510.01346. arXiv:2510.01346 [cs].                                 Y. Q., Wei, Y. X., Zhang, Y., Xu, Y., Li, Y., Zhao, Y., Sun,
                                                                         Y., Wang, Y., Yu, Y., Zhang, Y., Shi, Y., Xiong, Y., He, Y.,
Balunović, M., Dekoninck, J., Petrov, I., Jovanović, N., and
                                                                         Piao, Y., Wang, Y., Tan, Y., Ma, Y., Liu, Y., Guo, Y., Ou,
  Vechev, M. MathArena: Evaluating LLMs on Uncon-
                                                                         Y., Wang, Y., Gong, Y., Zou, Y., He, Y., Xiong, Y., Luo,
  taminated Math Competitions. In Advances in Neural
                                                                         Y., You, Y., Liu, Y., Zhou, Y., Zhu, Y. X., Xu, Y., Huang,
  Information Processing Systems 38, 2025. URL https:
                                                                         Y., Li, Y., Zheng, Y., Zhu, Y., Ma, Y., Tang, Y., Zha, Y.,
  //nips.cc/virtual/2025/poster/121385.
                                                                         Yan, Y., Ren, Z. Z., Ren, Z., Sha, Z., Fu, Z., Xu, Z., Xie,
Bryan, J., Elek, B., Manners, F., Salafatinos, G., and Vakil,            Z., Zhang, Z., Hao, Z., Ma, Z., Yan, Z., Wu, Z., Gu, Z.,
  R. The motivic class of the space of genus $0$ maps to                 Zhu, Z., Liu, Z., Li, Z., Xie, Z., Song, Z., Pan, Z., Huang,
  the flag variety, January 2026. URL http://arxiv.                      Z., Xu, Z., Zhang, Z., and Zhang, Z. DeepSeek-R1: In-
  org/abs/2601.07222. arXiv:2601.07222 [math].                           centivizing Reasoning Capability in LLMs via Reinforce-
                                                                         ment Learning. Nature, 645(8081):633–638, September
Chen, J., Chen, W., Du, J., Hu, J., Jiang, Z., Jie, A., Jin, X.,         2025a. ISSN 0028-0836, 1476-4687. doi: 10.1038/
  Jin, X., Li, C., Shi, W., Wang, Z., Wang, M., Wei, C., Wei,            s41586-025-09422-z. URL https://www.nature.
  S., Xin, H., Yang, F., Gao, W., Yuan, Z., Zhan, T., Zheng,             com/articles/s41586-025-09422-z.
  Z., Zhou, T., and Zhu, T. H. Seed-Prover 1.5: Master-
  ing Undergraduate-Level Theorem Proving via Learn-                   DeepSeek-AI, Liu, A., Mei, A., Lin, B., Xue, B., Wang,
  ing from Experience, December 2025a. URL http://                       B., Xu, B., Wu, B., Zhang, B., Lin, C., Dong, C., Lu, C.,
  arxiv.org/abs/2512.17260. arXiv:2512.17260                             Zhao, C., Deng, C., Xu, C., Ruan, C., Dai, D., Guo, D.,
  [cs].                                                                 Yang, D., Chen, D., Li, E., Zhou, F., Lin, F., Dai, F., Hao,
                                                                         G., Chen, G., Li, G., Zhang, H., Xu, H., Li, H., Liang,
Chen, L., Gu, J., Huang, L., Huang, W., Jiang, Z., Jie, A.,              H., Wei, H., Zhang, H., Luo, H., Ji, H., Ding, H., Tang,
  Jin, X., Jin, X., Li, C., Ma, K., Ren, C., Shen, J., Shi,              H., Cao, H., Gao, H., Qu, H., Zeng, H., Huang, J., Li,
  W., Sun, T., Sun, H., Wang, J., Wang, S., Wang, Z., Wei,               J., Xu, J., Hu, J., Chen, J., Xiang, J., Yuan, J., Cheng, J.,
  C., Wei, S., Wu, Y., Wu, Y., Xia, Y., Xin, H., Yang, F.,               Zhu, J., Ran, J., Jiang, J., Qiu, J., Li, J., Song, J., Dong,
  Ying, H., Yuan, H., Yuan, Z., Zhan, T., Zhang, C., Zhang,              K., Gao, K., Guan, K., Huang, K., Zhou, K., Huang, K.,
  Y., Zhang, G., Zhao, T., Zhao, J., Zhou, Y., and Zhu,                 Yu, K., Wang, L., Zhang, L., Wang, L., Zhao, L., Yin,
  T. H. Seed-Prover: Deep and Broad Reasoning for Auto-                  L., Guo, L., Luo, L., Ma, L., Wang, L., Zhang, L., Di,
  mated Theorem Proving, August 2025b. URL http://                       M. S., Xu, M. Y., Zhang, M., Zhang, M., Tang, M., Zhou,

                                                                   9
                                    Pessimistic Verification for Open-Ended Math Questions

  M., Huang, P., Cong, P., Wang, P., Wang, Q., Zhu, Q., Li,               Y., Von Glehn, I., Rowland, M., Albanie, S., Velingker,
  Q., Chen, Q., Du, Q., Xu, R., Ge, R., Zhang, R., Pan, R.,               A., Schmitt, S., Lockhart, E., Hughes, E., Michalewski,
  Wang, R., Yin, R., Xu, R., Shen, R., Zhang, R., Liu, S. H.,             H., Sonnerat, N., Hassabis, D., Kohli, P., and Sil-
  Lu, S., Zhou, S., Chen, S., Cai, S., Chen, S., Hu, S., Liu,             ver, D. Olympiad-level formal mathematical reason-
  S., Hu, S., Ma, S., Wang, S., Yu, S., Zhou, S., Pan, S.,                ing with reinforcement learning. Nature, November
  Zhou, S., Ni, T., Yun, T., Pei, T., Ye, T., Yue, T., Zeng, W.,          2025. ISSN 0028-0836, 1476-4687. doi: 10.1038/
  Liu, W., Liang, W., Pang, W., Luo, W., Gao, W., Zhang,                  s41586-025-09833-y. URL https://www.nature.
  W., Gao, X., Wang, X., Bi, X., Liu, X., Wang, X., Chen,                 com/articles/s41586-025-09833-y.
  X., Zhang, X., Nie, X., Cheng, X., Liu, X., Xie, X., Liu,
  X., Yu, X., Li, X., Yang, X., Li, X., Chen, X., Su, X., Pan,          Jain, S., Ahmed, U. Z., Sahai, S., and Leong, B. Beyond
  X., Lin, X., Fu, X., Wang, Y. Q., Zhang, Y., Xu, Y., Ma,                 Consensus: Mitigating the Agreeableness Bias in LLM
  Y., Li, Y., Li, Y., Zhao, Y., Sun, Y., Wang, Y., Qian, Y.,              Judge Evaluations, December 2025. URL http://
  Yu, Y., Zhang, Y., Ding, Y., Shi, Y., Xiong, Y., He, Y.,                 arxiv.org/abs/2510.11822. arXiv:2510.11822
  Zhou, Y., Zhong, Y., Piao, Y., Wang, Y., Chen, Y., Tan, Y.,              [cs].
  Wei, Y., Ma, Y., Liu, Y., Yang, Y., Guo, Y., Wu, Y., Wu,
  Y., Cheng, Y., Ou, Y., Xu, Y., Wang, Y., Gong, Y., Wu, Y.,            Liu, Y., Iter, D., Xu, Y., Wang, S., Xu, R., and Zhu, C.
  Zou, Y., Li, Y., Xiong, Y., Luo, Y., You, Y., Liu, Y., Zhou,            G-Eval: NLG Evaluation using GPT-4 with Better Hu-
  Y., Wu, Z. F., Ren, Z. Z., Zhao, Z., Ren, Z., Sha, Z., Fu,              man Alignment. In Proceedings of the 2023 Conference
  Z., Xu, Z., Xie, Z., Zhang, Z., Hao, Z., Gou, Z., Ma, Z.,               on Empirical Methods in Natural Language Processing,
  Yan, Z., Shao, Z., Huang, Z., Wu, Z., Li, Z., Zhang, Z.,                pp. 2511–2522, Singapore, December 2023. Association
  Xu, Z., Wang, Z., Gu, Z., Zhu, Z., Li, Z., Zhang, Z., Xie,              for Computational Linguistics. doi: 10.18653/v1/2023.
  Z., Gao, Z., Pan, Z., Yao, Z., Feng, B., Li, H., Cai, J. L.,            emnlp-main.153. URL https://aclanthology.
  Ni, J., Xu, L., Li, M., Tian, N., Chen, R. J., Jin, R. L.,              org/2023.emnlp-main.153/.
  Li, S. S., Zhou, S., Sun, T., Li, X. Q., Jin, X., Shen, X.,
  Chen, X., Song, X., Zhou, X., Zhu, Y. X., Huang, Y., Li,              Liu, Y., Huang, Y., Wang, Y., Li, P., and Liu, Y. AI Mathe-
  Y., Zheng, Y., Zhu, Y., Ma, Y., Huang, Z., Xu, Z., Zhang,               matician: Towards Fully Automated Frontier Mathemati-
  Z., Ji, D., Liang, J., Guo, J., Chen, J., Xia, L., Wang, M.,            cal Research, May 2025. URL http://arxiv.org/
  Li, M., Zhang, P., Chen, R., Sun, S., Wu, S., Ye, S., Wang,             abs/2505.22451. arXiv:2505.22451 [cs].
  T., Xiao, W. L., An, W., Wang, X., Sun, X., Wang, X.,
                                                                        Luong, T., Hwang, D., Nguyen, H. H., Ghiasi, G., Cher-
  Tang, Y., Zha, Y., Zhang, Z., Ju, Z., Zhang, Z., and Qu,
                                                                          vonyi, Y., Seo, I., Kim, J., Bingham, G., Lee, J., Mishra,
  Z. DeepSeek-V3.2: Pushing the Frontier of Open Large
                                                                          S., Zhai, A., Hu, H., Michalewski, H., Kim, J., Ahn,
  Language Models, December 2025b. URL http://
                                                                          J., Bae, J., Song, X., Trinh, T. H., Le, Q. V., and Jung,
  arxiv.org/abs/2512.02556. arXiv:2512.02556
                                                                          J. Towards Robust Mathematical Reasoning. In Pro-
  [cs].
                                                                          ceedings of the 2025 Conference on Empirical Meth-
Dekoninck, J., Petrov, I., Minchev, K., Balunovic, M.,                    ods in Natural Language Processing, pp. 35418–35442,
  Vechev, M., Marinov, M., Drencheva, M., Konova, L.,                     Suzhou, China, November 2025. Association for Compu-
  Shumanov, M., Tsvetkov, K., Drenchev, N., Todorov,                      tational Linguistics. doi: 10.18653/v1/2025.emnlp-main.
  L., Nikolova, K., Georgiev, N., Kalinkova, V., and                      1794. URL https://aclanthology.org/2025.
  Ismoldayev, M. The Open Proof Corpus: A Large-                          emnlp-main.1794/.
  Scale Study of LLM-Generated Mathematical Proofs,
  June 2025. URL http://arxiv.org/abs/2506.                             Mahdavi, H., Mahdavinia, P., Malek, S., Mohammadipour,
  21621. arXiv:2506.21621 [cs].                                          P., Hashemi, A., Daliri, M., Farhadi, A., Khasahmadi, A.,
                                                                         Mireshghallah, N., and Honavar, V. RefGrader: Auto-
Huang, Y. and Yang, L. F. Winning Gold at IMO 2025 with                  mated Grading of Mathematical Competition Proofs us-
  a Model-Agnostic Verification-and-Refinement Pipeline,                 ing Agentic Workflows, October 2025a. URL http://
  September 2025. URL http://arxiv.org/abs/                              arxiv.org/abs/2510.09021. arXiv:2510.09021
  2507.15855. arXiv:2507.15855v4 [cs.AI].                                [cs].

Hubert, T., Mehta, R., Sartran, L., Horváth, M. Z., Žužić,          Mahdavi, S., Kisacanin, B., Toshniwal, S., Du, W.,
  G., Wieser, E., Huang, A., Schrittwieser, J., Schroecker,              Moshkov, I., Armstrong, G., Liao, R., Thrampoulidis, C.,
 Y., Masoom, H., Bertolli, O., Zahavy, T., Mandhane,                     and Gitman, I. Scaling Generative Verifiers For Natural
 A., Yung, J., Beloshapka, I., Ibarz, B., Veeriah, V.,                   Language Mathematical Proof Verification And Selection,
 Yu, L., Nash, O., Lezeau, P., Mercuri, S., Sönne, C.,                  November 2025b. URL http://arxiv.org/abs/
  Mehta, B., Davies, A., Zheng, D., Pedregosa, F., Li,                   2511.13027. arXiv:2511.13027 [cs].

                                                                   10
                                    Pessimistic Verification for Open-Ended Math Questions

OpenAI, Jaech, A., Kalai, A., Lerer, A., Richardson, A.,                  Zhang, Y., Wang, Y., Shao, Z., and Li, Z. OpenAI o1
  El-Kishky, A., Low, A., Helyar, A., Madry, A., Beu-                     System Card, December 2024. URL http://arxiv.
  tel, A., Carney, A., Iftimie, A., Karpenko, A., Passos,                 org/abs/2412.16720. arXiv:2412.16720 [cs].
 A. T., Neitz, A., Prokofiev, A., Wei, A., Tam, A., Bennett,
 A., Kumar, A., Saraiva, A., Vallone, A., Duberstein, A.,               Pandit, S., Xu, A., Nguyen, X.-P., Ming, Y., Xiong,
  Kondrich, A., Mishchenko, A., Applebaum, A., Jiang, A.,                 C., and Joty, S. Hard2Verify: A Step-Level Verifica-
  Nair, A., Zoph, B., Ghorbani, B., Rossen, B., Sokolowsky,               tion Benchmark for Open-Ended Frontier Math, Octo-
  B., Barak, B., McGrew, B., Minaiev, B., Hao, B., Baker,                 ber 2025. URL http://arxiv.org/abs/2510.
  B., Houghton, B., McKinzie, B., Eastman, B., Lugaresi,                  13744. arXiv:2510.13744 [cs].
  C., Bassin, C., Hudson, C., Li, C. M., Bourcy, C. d.,
                                                                        Shao, Z., Luo, Y., Lu, C., Ren, Z. Z., Hu, J., Ye, T., Gou,
 Voss, C., Shen, C., Zhang, C., Koch, C., Orsinger, C.,
                                                                          Z., Ma, S., and Zhang, X. DeepSeekMath-V2: To-
  Hesse, C., Fischer, C., Chan, C., Roberts, D., Kappler,
                                                                          wards Self-Verifiable Mathematical Reasoning, Novem-
  D., Levy, D., Selsam, D., Dohan, D., Farhi, D., Mely, D.,
                                                                          ber 2025. URL http://arxiv.org/abs/2511.
  Robinson, D., Tsipras, D., Li, D., Oprica, D., Freeman,
                                                                          22570. arXiv:2511.22570 [cs].
  E., Zhang, E., Wong, E., Proehl, E., Cheung, E., Mitchell,
  E., Wallace, E., Ritter, E., Mays, E., Wang, F., Such, F. P.,         Singh, A., Fry, A., Perelman, A., Tart, A., Ganesh, A.,
  Raso, F., Leoni, F., Tsimpourlas, F., Song, F., Lohmann,                El-Kishky, A., McLaughlin, A., Low, A., Ostrow, A. J.,
  F. v., Sulit, F., Salmon, G., Parascandolo, G., Chabot, G.,             Ananthram, A., Nathan, A., Luo, A., Helyar, A., Madry,
  Zhao, G., Brockman, G., Leclerc, G., Salman, H., Bao,                   A., Efremov, A., Spyra, A., Baker-Whitcomb, A., Beutel,
  H., Sheng, H., Andrin, H., Bagherinezhad, H., Ren, H.,                  A., Karpenko, A., Makelov, A., Neitz, A., Wei, A., Barr,
  Lightman, H., Chung, H. W., Kivlichan, I., O’Connell,                   A., Kirchmeyer, A., Ivanov, A., Christakis, A., Gillespie,
  I., Osband, I., Gilaberte, I. C., Akkaya, I., Kostrikov, I.,            A., Tam, A., Bennett, A., Wan, A., Huang, A., Sandjideh,
  Sutskever, I., Kofman, I., Pachocki, J., Lennon, J., Wei,               A. M., Yang, A., Kumar, A., Saraiva, A., Vallone, A.,
 J., Harb, J., Twore, J., Feng, J., Yu, J., Weng, J., Tang, J.,           Gheorghe, A., Garcia, A. G., Braunstein, A., Liu, A.,
 Yu, J., Candela, J. Q., Palermo, J., Parish, J., Heidecke,               Schmidt, A., Mereskin, A., Mishchenko, A., Applebaum,
 J., Hallman, J., Rizzo, J., Gordon, J., Uesato, J., Ward,                A., Rogerson, A., Rajan, A., Wei, A., Kotha, A., Srivas-
 J., Huizinga, J., Wang, J., Chen, K., Xiao, K., Singhal,                 tava, A., Agrawal, A., Vijayvergiya, A., Tyra, A., Nair,
  K., Nguyen, K., Cobbe, K., Shi, K., Wood, K., Rimbach,                  A., Nayak, A., Eggers, B., Ji, B., Hoover, B., Chen, B.,
  K., Gu-Lemberg, K., Liu, K., Lu, K., Stone, K., Yu, K.,                 Chen, B., Barak, B., Minaiev, B., Hao, B., Baker, B.,
 Ahmad, L., Yang, L., Liu, L., Maksin, L., Ho, L., Fedus,                 Lightcap, B., McKinzie, B., Wang, B., Quinn, B., Fioca,
  L., Weng, L., Li, L., McCallum, L., Held, L., Kuhn, L.,                 B., Hsu, B., Yang, B., Yu, B., Zhang, B., Brenner, B.,
  Kondraciuk, L., Kaiser, L., Metz, L., Boyd, M., Trebacz,                Zetino, C. R., Raymond, C., Lugaresi, C., Paz, C., Hud-
  M., Joglekar, M., Chen, M., Tintor, M., Meyer, M., Jones,               son, C., Whitney, C., Li, C., Chen, C., Cole, C., Voss,
  M., Kaufer, M., Schwarzer, M., Shah, M., Yatbaz, M.,                    C., Ding, C., Shen, C., Huang, C., Colby, C., Hallacy, C.,
  Guan, M. Y., Xu, M., Yan, M., Glaese, M., Chen, M.,                     Koch, C., Lu, C., Kaplan, C., Kim, C., Minott-Henriques,
  Lampe, M., Malek, M., Wang, M., Fradin, M., McClay,                     C. J., Frey, C., Yu, C., Czarnecki, C., Reid, C., Wei, C.,
  M., Pavlov, M., Wang, M., Wang, M., Murati, M., Bavar-                  Decareaux, C., Scheau, C., Zhang, C., Forbes, C., Tang,
  ian, M., Rohaninejad, M., McAleese, N., Chowdhury,                      D., Goldberg, D., Roberts, D., Palmie, D., Kappler, D.,
  N., Chowdhury, N., Ryder, N., Tezak, N., Brown, N.,                     Levine, D., Wright, D., Leo, D., Lin, D., Robinson, D.,
  Nachum, O., Boiko, O., Murk, O., Watkins, O., Chao, P.,                 Grabb, D., Chen, D., Lim, D., Salama, D., Bhattacharjee,
 Ashbourne, P., Izmailov, P., Zhokhov, P., Dias, R., Arora,               D., Tsipras, D., Li, D., Yu, D., Strouse, D. J., Williams,
  R., Lin, R., Lopes, R. G., Gaon, R., Miyara, R., Leike,                 D., Hunn, D., Bayes, E., Arbus, E., Akyurek, E., Le, E. Y.,
  R., Hwang, R., Garg, R., Brown, R., James, R., Shu, R.,                 Widmann, E., Yani, E., Proehl, E., Sert, E., Cheung, E.,
  Cheu, R., Greene, R., Jain, S., Altman, S., Toizer, S.,                 Schwartz, E., Han, E., Jiang, E., Mitchell, E., Sigler, E.,
 Toyer, S., Miserendino, S., Agarwal, S., Hernandez, S.,                  Wallace, E., Ritter, E., Kavanaugh, E., Mays, E., Nikishin,
  Baker, S., McKinney, S., Yan, S., Zhao, S., Hu, S., San-                E., Li, F., Such, F. P., Peres, F. d. A. B., Raso, F., Beker-
  turkar, S., Chaudhuri, S. R., Zhang, S., Fu, S., Papay, S.,             man, F., Tsimpourlas, F., Chantzis, F., Song, F., Zhang,
  Lin, S., Balaji, S., Sanjeev, S., Sidor, S., Broda, T., Clark,          F., Raila, G., McGrath, G., Briggs, G., Yang, G., Paras-
 A., Wang, T., Gordon, T., Sanders, T., Patwardhan, T.,                   candolo, G., Chabot, G., Kim, G., Zhao, G., Valiant, G.,
  Sottiaux, T., Degry, T., Dimson, T., Zheng, T., Garipov, T.,            Leclerc, G., Salman, H., Wang, H., Sheng, H., Jiang, H.,
  Stasi, T., Bansal, T., Creech, T., Peterson, T., Eloundou,              Wang, H., Jin, H., Sikchi, H., Schmidt, H., Aspegren, H.,
 T., Qi, V., Kosaraju, V., Monaco, V., Pong, V., Fomenko,                 Chen, H., Qiu, H., Lightman, H., Covert, I., Kivlichan,
 V., Zheng, W., Zhou, W., McCabe, W., Zaremba, W.,                        I., Silber, I., Sohl, I., Hammoud, I., Clavera, I., Lan, I.,
  Dubois, Y., Lu, Y., Chen, Y., Cha, Y., Bai, Y., He, Y.,                 Akkaya, I., Kostrikov, I., Kofman, I., Etinger, I., Singal,

                                                                   11
                                  Pessimistic Verification for Open-Ended Math Questions

I., Hehir, J., Huh, J., Pan, J., Wilczynski, J., Pachocki, J.,           W., Bain, W., Thompson, W., Chen, X., Qi, X., Xiang, X.,
Lee, J., Quinn, J., Kiros, J., Kalra, J., Samaroo, J., Wang,             Shi, X., Dubois, Y., Yu, Y., Khakbaz, Y., Wu, Y., Qian,
J., Wolfe, J., Chen, J., Wang, J., Harb, J., Han, J., Wang,              Y., Lee, Y. T., Chen, Y., Zhang, Y., Xiong, Y., Tian, Y.,
J., Zhao, J., Chen, J., Yang, J., Tworek, J., Chand, J., Lan-            Cha, Y., Bai, Y., Yang, Y., Yuan, Y., Li, Y., Zhang, Y.,
don, J., Liang, J., Lin, J., Liu, J., Wang, J., Tang, J., Yin,           Yang, Y., Jin, Y., Jiang, Y., Wang, Y., Wang, Y., Liu, Y.,
J., Jang, J., Morris, J., Flynn, J., Ferstad, J., Heidecke, J.,          Stubenvoll, Z., Dou, Z., Wu, Z., and Wang, Z. OpenAI
Fishbein, J., Hallman, J., Grant, J., Chien, J., Gordon, J.,             GPT-5 System Card, December 2025. URL http://
Park, J., Liss, J., Kraaijeveld, J., Guay, J., Mo, J., Lawson,           arxiv.org/abs/2601.03267. arXiv:2601.03267
J., McGrath, J., Vendrow, J., Jiao, J., Lee, J., Steele, J.,             [cs].
Wang, J., Mao, J., Chen, K., Hayashi, K., Xiao, K., Salahi,
                                                                       Sinha, A., Arun, A., Goel, S., Staab, S., and Geip-
K., Wu, K., Sekhri, K., Sharma, K., Singhal, K., Li, K.,
                                                                         ing, J. The Illusion of Diminishing Returns: Mea-
Nguyen, K., Gu-Lemberg, K., King, K., Liu, K., Stone,
                                                                         suring Long Horizon Execution in LLMs, Septem-
K., Yu, K., Ying, K., Georgiev, K., Lim, K., Tirumala,
                                                                         ber 2025. URL http://arxiv.org/abs/2509.
K., Miller, K., Ahmad, L., Lv, L., Clare, L., Fauconnet,
                                                                         09677. arXiv:2509.09677 [cs].
L., Itow, L., Yang, L., Romaniuk, L., Anise, L., Byron,
L., Pathak, L., Maksin, L., Lo, L., Ho, L., Jing, L., Wu,              Varambally, S., Voice, T., Sun, Y., Chen, Z., Yu, R., and
L., Xiong, L., Mamitsuka, L., Yang, L., McCallum, L.,                    Ye, K. Hilbert: Recursively Building Formal Proofs with
Held, L., Bourgeois, L., Engstrom, L., Kuhn, L., Feuvrier,               Informal Reasoning, September 2025. URL http://
L., Zhang, L., Switzer, L., Kondraciuk, L., Kaiser, L.,                  arxiv.org/abs/2509.22819. arXiv:2509.22819
Joglekar, M., Singh, M., Shah, M., Stratta, M., Williams,                [cs].
M., Chen, M., Sun, M., Cayton, M., Li, M., Zhang, M.,
Aljubeh, M., Nichols, M., Haines, M., Schwarzer, M.,                   Xu, Y., Chakraborty, T., Sharma, S., Nunes, L., Sharma, S.,
Gupta, M., Shah, M., Huang, M., Dong, M., Wang, M.,                      Demopulos, K. D., Kıcıman, E., Lu, S., and Chandra, R.
Glaese, M., Carroll, M., Lampe, M., Malek, M., Shar-                     Direct Reasoning Optimization: Token-Level Reasoning
man, M., Zhang, M., Wang, M., Pokrass, M., Florian,                      Reflectivity Meets Rubric Gates for Unverifiable Tasks,
M., Pavlov, M., Wang, M., Chen, M., Wang, M., Feng,                      May 2026. URL http://arxiv.org/abs/2506.
M., Bavarian, M., Lin, M., Abdool, M., Rohaninejad, M.,                  13351. arXiv:2506.13351v3 [cs.CL].
Soto, N., Staudacher, N., LaFontaine, N., Marwell, N.,                 Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B.,
Liu, N., Preston, N., Turley, N., Ansman, N., Blades, N.,                Yu, B., Gao, C., Huang, C., Lv, C., Zheng, C., Liu, D.,
Pancha, N., Mikhaylin, N., Felix, N., Handa, N., Rai, N.,                Zhou, F., Huang, F., Hu, F., Ge, H., Wei, H., Lin, H.,
Keskar, N., Brown, N., Nachum, O., Boiko, O., Murk,                      Tang, J., Yang, J., Tu, J., Zhang, J., Yang, J., Yang, J.,
O., Watkins, O., Gleeson, O., Mishkin, P., Lesiewicz, P.,                Zhou, J., Zhou, J., Lin, J., Dang, K., Bao, K., Yang, K.,
Baltescu, P., Belov, P., Zhokhov, P., Pronin, P., Guo, P.,               Yu, L., Deng, L., Li, M., Xue, M., Li, M., Zhang, P.,
Thacker, P., Liu, Q., Yuan, Q., Liu, Q., Dias, R., Puck-                 Wang, P., Zhu, Q., Men, R., Gao, R., Liu, S., Luo, S.,
ett, R., Arora, R., Mullapudi, R. T., Gaon, R., Miyara,                  Li, T., Tang, T., Yin, W., Ren, X., Wang, X., Zhang, X.,
R., Song, R., Aggarwal, R., Marsan, R. J., Yemiru, R.,                   Ren, X., Fan, Y., Su, Y., Zhang, Y., Zhang, Y., Wan, Y.,
Xiong, R., Kshirsagar, R., Nuttall, R., Tsiupa, R., Eldan,               Liu, Y., Wang, Z., Cui, Z., Zhang, Z., Zhou, Z., and Qiu,
R., Wang, R., James, R., Ziv, R., Shu, R., Nigmatullin,                  Z. Qwen3 Technical Report, May 2025. URL http://
R., Jain, S., Talaie, S., Altman, S., Arnesen, S., Toizer, S.,           arxiv.org/abs/2505.09388. arXiv:2505.09388
Toyer, S., Miserendino, S., Agarwal, S., Yoo, S., Heon, S.,              [cs].
Ethersmith, S., Grove, S., Taylor, S., Bubeck, S., Banesiu,
S., Amdo, S., Zhao, S., Wu, S., Santurkar, S., Zhao, S.,               Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z.,
Chaudhuri, S. R., Krishnaswamy, S., Shuaiqi, Xia, Cheng,                 Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang,
S., Anadkat, S., Fishman, S. P., Tobin, S., Fu, S., Jain,                H., Gonzalez, J. E., and Stoica, I. Judging LLM-as-a-
S., Mei, S., Egoian, S., Kim, S., Golden, S., Mah, S. Q.,                Judge with MT-Bench and Chatbot Arena. In Advances
Lin, S., Imm, S., Sharpe, S., Yadlowsky, S., Choudhry,                   in Neural Information Processing Systems 36, pp. 46595–
S., Eum, S., Sanjeev, S., Khan, T., Stramer, T., Wang,                   46623, 2023. doi: 10.52202/075280-2020. URL https:
T., Xin, T., Gogineni, T., Christianson, T., Sanders, T.,                //doi.org/10.52202/075280-2020.
Patwardhan, T., Degry, T., Shadwell, T., Fu, T., Gao, T.,              Zuo, Y., Zhang, K., Sheng, L., Qu, S., Cui, G., Zhu, X.,
Garipov, T., Sriskandarajah, T., Sherbakov, T., Kaftan, T.,              Li, H., Zhang, Y., Long, X., Hua, E., Qi, B., Sun, Y.,
Hiratsuka, T., Wang, T., Song, T., Zhao, T., Peterson, T.,               Ma, Z., Yuan, L., Ding, N., and Zhou, B. TTRL: Test-
Kharitonov, V., Chernova, V., Kosaraju, V., Kuo, V., Pong,               Time Reinforcement Learning. In Advances in Neural
V., Verma, V., Petrov, V., Jiang, W., Zhang, W., Zhou, W.,               Information Processing Systems 38, 2025. URL https:
Xie, W., Zhan, W., McCabe, W., DePue, W., Ellsworth,                     //openreview.net/forum?id=VuVhgEiu20.

                                                                  12
                                   Pessimistic Verification for Open-Ended Math Questions

A. Appendix
A.1. Auxiliary Efficiency Measurements
We additionally measured the per-sample token consumption, wall-clock runtime, and API cost of representative verification
settings. All methods were executed with the same concurrency, so the wall-clock runtime is affected by implementation
and serving conditions but remains largely aligned with total token consumption. We therefore report equivalent output
tokens as the primary hardware-agnostic efficiency metric, while runtime and API cost provide concrete reference points for
practical deployment.

                        Table 4. Auxiliary efficiency measurements on representative verification settings.
                        The token usage is measured by equivalent output tokens. Runtime and cost are
                        reported per sample under the same parallel execution setting.

                          Model             Method        Bal. F1    Eq. Tokens     Time (s)    Cost ($)
                          gpt-5-mini        standard         0.78        2,975.5        6.15      0.0060
                          gpt-5-mini        pes@12           0.87       35,675.8       78.55      0.0714
                          gpt-5-mini        prog@3/6         0.85        7,146.6       14.77      0.0143
                          qwen3-30b-a3b     standard         0.52        3,089.1       12.59      0.0013
                          qwen3-30b-a3b     pes@12           0.77       40,666.5      126.95      0.0175
                          qwen3-30b-a3b     prog@3/6         0.79       11,680.1       31.17      0.0049

These auxiliary measurements are consistent with the efficiency trends in Figure 4. At comparable performance, progressive
pessimistic verification uses roughly one fourth of the equivalent tokens, runtime, and API cost of the simple pessimistic
verification setting commonly used in agentic math workflows.

A.2. Details in QiuZhen-Bench
QiuZhen-Bench is a dataset covering a wide range of topics in advanced math, including analysis, algebra, machine learning
theory, geometry, topology, probability, statistics and theoretical physics. We have collected 143 exam papers from S.-T.
Yau College Student Mathematics Contest since 2010, and the doctoral qualifying exams from QiuZhen college, Tsinghua
University since 2023, and required GPT-5 to extract and reformat problems directly from the PDF files. Manual spot checks
did not reveal any errors in these extracted contents, indicating the strong capability of GPT-5 in doing this task. We firstly
divide the exam papers into pages, and for each page we used the following prompt for extraction:

    system prompt

   You are a meticulous exam parsing assistant.
   Extract ALL distinct problems from the provided text chunks.
   Return ONLY valid JSON (no commentary). Focus on problem statements; exclude answers
       and solutions.


    user prompt

   Task: Parse the following exam/contest page images to extract problem statements.
   Requirements:
   - Identify each separate problem with its number or index if present.
   - Preserve math using Markdown and LaTeX (inline ‘$...$‘, display ‘$$...$$‘).
   - Do not infer content; only use what appears in the images.
   - Only include problems written in English; skip non-English (e.g., Chinese).
   - If a problem is mixed-language, include only the English statement; otherwise skip.
   - If a problem spans multiple pages in this chunk, include the full statement.
   Output strictly as JSON array of objects with keys:
     - problem_number: string (e.g., ’1’, ’II-3’, ’A.1’; use ’unknown’ if missing)
     - markdown_statement: string (problem text in Markdown; no solution)
     - section: string|null (e.g., ’Analysis’, ’Geometry’, or null)
     - tags: array of strings (optional keywords, may be empty)


                                                               13
                                  Pessimistic Verification for Open-Ended Math Questions


     - source_pages: array of integers (page numbers within this PDF chunk)
   Return ONLY JSON.

   fSource: {source.rel_path}
   Pages: {chunk.start_page}-{chunk.end_page}


The problems that spans across two pages is extracted by part and combined in the following processing logic. This results
in a dataset containing 1,054 problems in total. Here we provide some samples from this dataset:

   Yau contest 2015, applied math

   Let G be graph of a social network, where for each pair of members there is either no connection, or a positive or a
   negative one. An unbalanced cycle in G is a cycle which have odd number of negative edges. Traversing along such
   a cycle with social rules such as friend of enemy are enemy would result in having a negative relation of one with
   himself! A resigning in G at a vertex v of G is to switch the type (positive or negative) of all edges incident to v.
   Question: Show that one can switch all edge of G into positive edges using a sequence resigning if and only if there is
   no unbalanced cycle in G.

   QiuZhen qualifying 2024 spring, theoretical physics

  Πµν (q) via dimensional regularization (35 points)
  At one-loop, the photon propagator in QED receives the correction

                                                d4 p
                                           Z                                           
                                                              ν        i         µ   i
                             i Πµν (q) = −           Tr   i γ                i γ          ,
                                               (2π)4            ̸ p+ ̸ q − m       ̸p−m
  where γµ is the gamma matrix and ̸ p = pµ γµ .
  i) 10’ Show that this expression can be written as

                                                                    d4 p Nµν
                                                               Z
                                              i Πµν (q) = −i                 ,
                                                                   (2π)4 D
  where
                                                                                     Z 1
                                                                               1                1
                              Nµν = tr [γν (̸ p+ ̸ q + m)γµ (̸ p − m)] ,         =         dα     ,
                                                                               D      0         D
  with
                                                            2
                              D = l2 + α(1 − α)q 2 − m2 + iϵ ,
                                 
                                                                            where l = p + αq.
   ii) 10’ Evaluate Nµν and shift momentum integration from p to l as above.
   iii) 10’ At the integration step over l, perform dimensional regularization by promoting to a d-dimensional integral.
   Derive the expression

                                            Πµν (q) = (qµ qν − ηµν q 2 ) Π(q 2 ),
  when taking the limit d → 4.
  iv) 5’ Why does this result ensure gauge invariance?

   Yau contest 2019, analysis individual

   Let Ω ⊂ R2 be a bounded domain with smooth boundary. Prove that, for all p > 1 and 1 ≤ q < ∞, for all f ∈ Lp (Ω),
   there exists a unique u ∈ H01 (Ω), such that

                                                ∆u = |u|q−1 u + f      in Ω.


                                                             14
                                  Pessimistic Verification for Open-Ended Math Questions

   QiuZhen qualifying 2025 fall, algebra

  Suppose r ≤ n are positive integers. Let X be the subset of M (n × n, C) consisting of complex n × n matrices with
  rank at most r. Prove that X is Zariski closed. Find the number of irreducible components of X, and calculate the
  Krull dimension of each irreducible component of X.


A.3. Prompt Template
In our experiments, we use the same evaluation prompt template across all these datasets. For standard, majority voting, and
simple pessimistic verification, we use this single-pass verification prompt:

   system prompt: single pass

  You are an assistant highly proficient in mathematics.
  The user will provide a math problem together with its proposed solution, and your
      task is to verify the correctness of that solution according to the given
      instruction.




   user prompt: single pass

  Here is a math problem and a candidate solution of it, and you need to verify the
      correctness of this solution. Please check each of the following:

  1. The provided content is indeed a math problem and its corresponding solution,
      rather than unrelated material supplied by mistake.
  2. The solution actually derives the conclusion required by the original problem.
  3. Every step of calculation and formula derivation in the solution is correct.
  4. The hypotheses (conditions) and conclusions of any theorems used are correctly
      matched and applied.
  5. The solution relies only on the conditions given in the problem and does not
      introduce any additional assumptions to obtain the conclusion.

  Consistency and error-severity policy (important):
  - If only minor, easily fixable issues exist (e.g., small algebraic slips later
      corrected, notational typos, superficial formatting), treat the solution as
      correct overall but briefly note such issues.
  - If there is any critical error that undermines correctness (e.g., invalid step,
      wrong theorem usage without required conditions, uncorrected calculation error
      leading to a wrong result), treat the solution as incorrect.

  Response requirements: If the solution is correct overall (possibly with minor issues)
      , reply with ‘<verification>true</verification>‘ and briefly list minor issues if
      any.
   If the solution is incorrect, reply with ‘<verification>false</verification>‘
      followed by a concise description of the most harmful error.
   Do not include any restatement of the entire solution or problem.

  <problem>{problem}</problem>

  <answer>{solution}</answer>



The first step of progressive pessimistic verifier also adopts the single pass prompt, and for the following verification
of subdivisions, we will use the following chunk verification prompt. This prompt is also used in vertical pessimistic
verification in our experiments.



                                                            15
                                  Pessimistic Verification for Open-Ended Math Questions

   system prompt: chunk verification

   You are an assistant highly proficient in mathematics.
   The user will provide a math problem together with its proposed solution, and your
       task is to verify the correctness of that solution according to the given
       instruction.



   user prompt: chunk verification

   We provide the original problem and the complete proposed solution for full context.
   Then we provide a specific chunk from the solution for focused checking.
   Your task: Check ONLY the given chunk for errors while considering the overall
       context.

   Checklist:
   1. The chunk’s reasoning and calculations adhere to mathematical correctness.
   2. Any theorems used in the chunk match their hypotheses and conclusions.
   3. The chunk does not rely on assumptions not justified by the problem or earlier
       proven steps.

   Consistency and error-severity policy (important):
   - If only minor, easily fixable issues exist (e.g., small algebraic slips later
       corrected, notational typos, superficial formatting), treat the chunk as correct
       overall but briefly note such issues.
   - If there is any critical error that undermines correctness in this chunk (e.g.,
       invalid step, wrong theorem usage without required conditions), treat the chunk as
        incorrect.

   Response requirements: If the chunk is correct overall (possibly with minor issues),
       reply with ‘<verification>true</verification>‘ and briefly list minor issues if
       any.
   If the chunk is incorrect, reply with ‘<verification>false</verification>‘ followed by
        a concise description of the most harmful error in the proof that you found in
       the chunk.

   <problem>{problem}</problem>

   <full_answer>{full_proof}</full_answer>

   <chunk_index>{idx}</chunk_index>
   <chunk>{chunk}</chunk>



A.4. More Detailed Case Studies
In this section we primarily focus on the false negative cases reported by different verifiers, these are the most informative
cases in our experiments.

A.4.1. FALSE N EGATIVE E XAMPLES ON IMO-G RADING B ENCH

   Case 1: problem

   Let ∠XY Z be an acute angle with ∠XY Z ̸= 60◦ , and let A be a point inside ∠XY Z. Prove that there exists D ̸= A
   inside ∠XY Z and θ ∈ (0, 2π) satisfying the following condition:
                                  −−→     −−→
   For points B and C on the rays Y X and Y Z respectively, then

                                        ∠BAC = ∠XY Z           =⇒       ∠BDC = θ.



                                                             16
                                Pessimistic Verification for Open-Ended Math Questions

 Case 1: proof

**1. Summary**
**a. Verdict:** I have successfully solved the problem. I have rigorously proven that the statement is true.
**b. Method Sketch:** The proof utilizes complex numbers to model the geometric configuration.
                                                                                                          −−→       −−→
1. **Setup**: We establish a coordinate system with Y at the origin. Let α = ∠XY Z. The rays Y X and Y Z
correspond to the positive real axis and the ray at angle α, respectively. A = a is inside the angle. B = b and
C = ceiα (b > 0, c > 0). 2. **Analysis of Configurations (SA )**: We analyze the condition ∠BAC = α. This
geometric condition implies the directed angle from AB ⃗ to AC ⃗ is either α (CCW) or −α (CW). * We prove that the
set of CCW configurations is empty when A is strictly inside the angle. * We prove that the set of CW configurations
SA is non-empty and infinite, corresponding to an interval of values for b. We rigorously derive the relationship
between b and c (via an intermediate variable k) as a rational function. 3. **Constant Angle Condition**: We assume
D = d is a point inside the angle such that ∠BDC = θ is constant for all configurations in SA . This implies the
                        C(b)−d
complex ratio X(b) = B(b)−d    has a constant argument as b varies. 4. **Analysis of the Rational Function**: X(b) is
shown to be a rational function P (b)/Q(b), where deg(P ) = 1 and deg(Q) = 2. Since arg(X(b)) is constant, X(b)
must be proportional to a real rational function. 5. **Poles Analysis**: The poles of Q(b) are d (non-real) and b0
(real). For the corresponding real rational function to exist, its poles must be symmetric under conjugation. This
forces a cancellation between P (b) and Q(b). 6. **Case Analysis of Common Roots**: We analyze the possibilities
for the common root. * If the common root is b0 , it implies A is on the ray Y X, contradicting the premise. * If
the common root is d, it leads to two solutions for D: D = A and a unique other point D = D∗ . 7. **Analysis
of the Solution D∗ **: We explicitly calculate D∗ and rigorously prove that D∗ is always strictly inside the angle
∠XY Z. 8. **Exclusion of D∗ = A**: We determine the conditions under which D∗ = A. This occurs if and only if
α = 60◦ and A lies on the angle bisector. 9. **Conclusion**: Since the problem stipulates that α ̸= 60◦ , we must
have D∗ ̸= A. Thus, D = D∗ is the required point inside the angle, different from A. The constant angle is calculated
to be θ = π − 2α.
**2. Detailed Solution**
Step 1: Setup and Coordinate System. Let α = ∠XY Z. We are given 0 < α < π/2 and α ̸= π/3. We set up a
                                                                         −−→                              −−→
coordinate system in the complex plane with Y at the origin 0. The ray Y X is the positive real axis, and Y Z is the ray
at angle α. Let A be represented by the complex number a. Since A is strictly inside the angle, a = reiϕ1 with r > 0
and 0 < ϕ1 < α. Let B and C be represented by b and ceiα respectively, with b > 0, c > 0.
Step 2: Analysis of the configurations SA . The condition is ∠BAC = α. This geometric angle condition means the
directed angle from AB⃗ (represented by B − A) to AC  ⃗ (represented by C − A) is either α (CCW orientation) or −α
(CW orientation).
Case 2.1: CCW orientation. The directed angle is α.
                                         ceiα − a
                                                  = keiα ,     for some k > 0.
                                          b−a
ceiα − a = k(b − a)eiα . Dividing by eiα : c − ae−iα = k(b − a). Since c, k, b are real, we equate the imaginary parts:
Im(c − ae−iα ) = kIm(b − a). Im(−ae−iα ) = kIm(−a). Im(−rei(ϕ1 −α) ) = kIm(−reiϕ1 ). −r sin(ϕ1 − α) =
k(−r sin ϕ1 ). sin(ϕ1 − α) = k sin ϕ1 . Since 0 < ϕ1 < α < π/2, we have sin ϕ1 > 0. Also, −π/2 < −α <
                                                               1 −α)
ϕ1 − α < 0. Thus sin(ϕ1 − α) < 0. This implies k = sin(ϕ    sin ϕ1   < 0. This contradicts the requirement k > 0.
Therefore, the set of CCW configurations is empty.
Case 2.2: CW orientation. The directed angle is −α.
                                        ceiα − a
                                                 = ke−iα ,     for some k > 0.
                                         b−a
ceiα − a = k(b − a)e−iα . Dividing by eiα is not helpful. Let’s rearrange to isolate c. ceiα = a + k(b − a)e−iα .
c = ae−iα + k(b − a)e−i2α . Since c is real, we equate the imaginary part to zero. Im(ae−iα ) + kIm((b − a)e−i2α ) =
0. Im(rei(ϕ1 −α) ) + kIm(be−i2α − rei(ϕ1 −2α) ) = 0. r sin(ϕ1 − α) + k(b sin(−2α) − r sin(ϕ1 − 2α)) = 0.
r sin(ϕ1 − α) = k(−b sin(−2α) + r sin(ϕ1 − 2α)). r sin(ϕ1 − α) = k(b sin 2α − r sin(ϕ1 − 2α)).
We rewrite this using sin(x) = − sin(−x). −r sin(α − ϕ1 ) = k(b sin 2α + r sin(2α − ϕ1 )).
Let C1 = r sin(α − ϕ1 ). Since 0 < α − ϕ1 < π/2, C1 > 0. Let C2 = sin 2α. Since 0 < 2α < π, C2 > 0. Let
C3 = r sin(2α − ϕ1 ). Since 0 < ϕ1 < α and α < π/2, we have α < 2α − ϕ1 < 2α < π. Thus C3 > 0.


                                                          17
                                  Pessimistic Verification for Open-Ended Math Questions


The equation is −C1 = k(C2 b + C3 ). Since C1 > 0 and C2 , C3 , b > 0, the RHS is k(C2 b + C3 ). If k > 0, the RHS
is positive, while the LHS is negative. This is a contradiction.
Let’s recheck the derivation in the thought block, as I seem to have made a mistake again in the live derivation attempt.
Let’s restart the derivation for Case 2.2 carefully. ceiα − a = k(b − a)e−iα . We want to eliminate c. We can
multiply by e−iα . c − ae−iα = k(b − a)e−i2α . Since c is real, the imaginary part of the LHS is Im(−ae−iα ). The
imaginary part of the RHS is kIm((b − a)e−i2α ). Im(−rei(ϕ1 −α) ) = kIm((b − reiϕ1 )e−i2α ). −r sin(ϕ1 − α) =
kIm(be−i2α − rei(ϕ1 −2α) ). −r sin(ϕ1 − α) = k(b sin(−2α) − r sin(ϕ1 − 2α)).
Now we simplify. LHS: r sin(α − ϕ1 ). RHS: k(−b sin 2α + r sin(2α − ϕ1 )).
The equation is r sin(α − ϕ1 ) = k(r sin(2α − ϕ1 ) − b sin 2α).
Using the definitions of C1 , C2 , C3 : C1 = k(C3 − C2 b).
                                                                                                                C1
We require k > 0. Since C1 > 0, we need C3 − C2 b > 0. b < C3 /C2 . Let b0 = C3 /C2 . b0 > 0. k(b) = C3 −C          2b
                                                                                                                       .
                                                                                              −iα                          −i2α
We also require c(b) > 0. c(b) = Re(ae−iα ) + k(b)Re((b − a)e−i2α ). c(b) = Re(ae )(C3 −CC23b)+C                1 Re((b−a)e
                                                                                                            −C2 b
                                                                                                                               )
                                                                                                                                 .
                                                                                                                          −iα
The denominator is positive for b ∈ (0, b0 ). We analyze the numerator N (b) = L1 b + L0 . L1 = −C2 Re(ae ) +
C1 Re(e−i2α ). L1 = − sin 2α · r cos(ϕ1 − α) + r sin(α − ϕ1 ) cos 2α. L1 = −r[sin 2α cos(α − ϕ1 ) − cos 2α sin(α −
ϕ1 )]. L1 = −r sin(2α − (α − ϕ1 )) = −r sin(α + ϕ1 ). Since 0 < α + ϕ1 < π, L1 < 0.
L0 = C3 Re(ae−iα ) + C1 Re(−ae−i2α ). L0 = r sin(2α − ϕ1 )r cos(α − ϕ1 ) − r sin(α − ϕ1 )r cos(2α − ϕ1 ).
L0 = r2 sin((2α − ϕ1 ) − (α − ϕ1 )) = r2 sin α. Since α > 0, L0 > 0.
We need N (b) > 0. L1 b + L0 > 0. Since L1 < 0, b < −L0 /L1 . Let b1 = −L0 /L1 . b1 > 0. The set of valid
configurations SA corresponds to the interval IA = (0, min(b0 , b1 )). This interval is non-empty, so SA is infinite.
Step 3: Analysis of the constant angle condition. Let D = d be a point inside the angle. This means d is not real and
0 < arg(d) < α. We require D ̸= A. We require ∠BDC = θ to be constant for all (B, C) ∈ SA . Let C(b) denote
the complex coordinate of C corresponding to B = b. C(b) = c(b)eiα . The condition means the argument of the
complex ratio X(b) = C(b)−d b−d is constant for b ∈ IA .
From the definition of the CW configuration in Step 2.2, we have C(b) = a + k(b)(b − a)e−iα . X(b) =
a−d+k(b)(b−a)e−iα                                                          3 −C2 b)+C1 (b−a)e
                                                                                             −iα

         b−d        . Substituting k(b) = C3 −CC1
                                                  2b
                                                     : X(b) = (a−d)(C(b−d)(C       3 −C2 b)
                                                                                                    P (b)
                                                                                                 = Q(b)   .
P (b) is a polynomial of degree at most 1 in b. Q(b) is a polynomial of degree 2 in b. Q(b) = −C2 (b − d)(b − b0 ),
where b0 = C3 /C2 . The roots are d (non-real) and b0 (real and positive).
Since arg(X(b)) is constant on the interval IA , X(b) = KR(b) where K is a complex constant and R(b) is a real
rational function. The poles of a real rational function must be real or come in conjugate pairs.
If P (b) and Q(b) are coprime, the poles of X(b) (and thus R(b)) are d and b0 . Since d is not real, d¯ must also be a
pole. So d¯ ∈ {d, b0 }. d¯ = d is impossible as d is not real. d¯ = b0 . Since b0 is real, d = b¯0 = b0 . This implies d is real,
which contradicts that D is inside the angle. Thus, P (b) and Q(b) must share a common root.
Step 4: Case analysis of the common root. Case 4.1: The common root is b0 . P (b0 ) = 0. P (b0 ) = (a − d)(C3 −
C2 b0 ) + C1 (b0 − a)e−iα . Since C3 − C2 b0 = 0, P (b0 ) = C1 (b0 − a)e−iα . P (b0 ) = 0 implies C1 (b0 − a)e−iα = 0.
Since C1 > 0 and e−iα ̸= 0, we must have b0 − a = 0. a = b0 . This means A is real, so A is on the ray Y X. This
contradicts that A is strictly inside the angle (0 < ϕ1 ).
Case 4.2: The common root is d. P (d) = 0. P (d) = (a − d)(C3 − C2 d) + C1 (d − a)e−iα = 0. (a − d)[(C3 −
C2 d) − C1 e−iα ] = 0. This yields two possibilities for D: D = A (i.e., d = a) or C3 − C2 d − C1 e−iα = 0.
We are looking for D ̸= A. Let D∗ be the second solution, with coordinate d∗ . C2 d∗ = C3 − C1 e−iα . d∗ =
C3 −C1 e−iα
     C2      .
If D = D∗ , then (b − d∗ ) is a common factor of P (b) and Q(b). P (b) = p1 (b − d∗ ). Q(b) = −C2 (b − d∗ )(b − b0 ).
X(b) = −C2p(b−b1
                  0)
                     . For b ∈ IA , b < b0 . Since C2 > 0, the denominator −C2 (b − b0 ) is positive and real. Thus,
arg(X(b)) = arg(p1 ), which is constant.
Step 5: Analysis of the location of D∗ . We must verify that D∗ is inside the angle, i.e., 0 < arg(d∗ ) < α.
Im(d∗ ) = C12 Im(C3 − C1 e−iα ) = C12 (−C1 sin(−α)) = C1Csin             2
                                                                            α
                                                                              . Since C1 > 0, C2 > 0, sin α > 0, we have
       ∗                  ∗
Im(d ) > 0. So arg(d ) > 0.
                                                                                               −iα       −i2α
We check arg(d∗ ) < α. This is equivalent to Im(d∗ e−iα ) < 0. d∗ e−iα = C3 e −C                   C2
                                                                                                      1e
                                                                                                              . Im(d∗ e−iα ) =
C3 sin(−α)−C1 sin(−2α)
           C2          = −C3 sin α+C
                                 C2
                                     1 sin 2α
                                              . Let H = C1 sin 2α − C3 sin α. H = r sin(α − ϕ1 ) sin 2α − r sin(2α −
ϕ1 ) sin α. H = r sin α[2 sin(α − ϕ1 ) cos α − sin(2α − ϕ1 )]. Using the identity 2 sin A cos B = sin(A + B) +
sin(A − B): 2 sin(α − ϕ1 ) cos α = sin(2α − ϕ1 ) + sin(−ϕ1 ) = sin(2α − ϕ1 ) − sin ϕ1 . H = r sin α[sin(2α − ϕ1 ) −



                                                               18
                                  Pessimistic Verification for Open-Ended Math Questions


  sin ϕ1 − sin(2α − ϕ1 )]. H = −r sin α sin ϕ1 . Since r > 0, sin α > 0, sin ϕ1 > 0 (as 0 < ϕ1 < α < π/2), we have
  H < 0. Thus Im(d∗ e−iα ) < 0. So arg(d∗ ) < α. D∗ is strictly inside the angle ∠XY Z.
  Step 6: Analysis of the condition D∗ = A. We check when d∗ = a. This happens if a satisfies the equation for d∗ .
  C2 a = C3 −C1 e−iα . reiϕ1 sin 2α = r sin(2α−ϕ1 )−r sin(α−ϕ1 )e−iα . Dividing by r and examining the imaginary
  part: sin ϕ1 sin 2α = Im(− sin(α − ϕ1 )e−iα ) = − sin(α − ϕ1 ) sin(−α) = sin(α − ϕ1 ) sin α. 2 sin ϕ1 sin α cos α =
  (sin α cos ϕ1 − cos α sin ϕ1 ) sin α. Since sin α ̸= 0: 2 sin ϕ1 cos α = sin α cos ϕ1 − cos α sin ϕ1 . 3 sin ϕ1 cos α =
  sin α cos ϕ1 . 3 tan ϕ1 = tan α. (Since cos α ̸= 0, cos ϕ1 ̸= 0).
  Examining the real part: cos ϕ1 sin 2α = sin(2α − ϕ1 ) − sin(α − ϕ1 ) cos α. cos ϕ1 sin 2α = (sin 2α cos ϕ1 −
  cos 2α sin ϕ1 ) − (sin α cos ϕ1 − cos α sin ϕ1 ) cos α. 0 = − cos 2α sin ϕ1 − sin α cos α cos ϕ1 + cos2 α sin ϕ1 . 0 =
  sin ϕ1 (cos2 α − cos 2α) − sin α cos α cos ϕ1 . 0 = sin ϕ1 (cos2 α − (cos2 α − sin2 α)) − 12 sin 2α cos ϕ1 . 0 =
  sin ϕ1 sin2 α − sin α cos α cos ϕ1 . 0 = sin α(sin ϕ1 sin α − cos α cos ϕ1 ) = − sin α cos(α + ϕ1 ). Since sin α ̸= 0,
  cos(α + ϕ1 ) = 0. Since 0 < α + ϕ1 < π, we must have α + ϕ1 = π/2.
  If α + ϕ1 = π/2, then tan α = cot ϕ1 =√1/ tan ϕ1 . Substituting into 3 tan ϕ1 = tan α: 3 tan ϕ1 = 1/ tan ϕ1 .
  tan2 ϕ1 = 1/3. Since ϕ1 > 0, tan ϕ1 = 1/ 3. ϕ1 = π/6 (30 degrees). Then α = π/2 − π/6 = π/3 (60 degrees).
  So D∗ = A if and only if α = 60◦ and A is on the angle bisector (ϕ1 = α/2).
  Step 7: Conclusion. The problem states that ∠XY Z ̸= 60◦ (i.e., α ̸= π/3). Therefore, the condition for D∗ = A is
  not met, so D∗ ̸= A. We have shown that D∗ is strictly inside the angle ∠XY Z. We have shown that for D = D∗ ,
  the angle ∠BDC is constant for all configurations (B, C) such that ∠BAC = α.
  We determine the constant angle θ. The directed angle Θ is arg(X(b)) = arg(p1 ). p1 is the leading coefficient of
  P (b). p1 = −C2 (a − d∗ ) + C1 e−iα . Using the definition of d∗ , C2 d∗ = C3 − C1 e−iα , so C1 e−iα = C3 − C2 d∗ .
  p1 = −C2 a + C2 d∗ + (C3 − C2 d∗ ) = C3 − C2 a. p1 = r sin(2α − ϕ1 ) − sin 2α · reiϕ1 . p1 = r[sin(2α −
  ϕ1 ) − (cos ϕ1 + i sin ϕ1 ) sin 2α]. p1 = r[(sin 2α cos ϕ1 − cos 2α sin ϕ1 ) − sin 2α cos ϕ1 − i sin 2α sin ϕ1 ]. p1 =
  r[− cos 2α sin ϕ1 − i sin 2α sin ϕ1 ]. p1 = −r sin ϕ1 (cos 2α + i sin 2α) = −r sin ϕ1 ei2α . Since r > 0, sin ϕ1 > 0,
  arg(p1 ) = π + 2α. The directed angle is Θ = π + 2α (mod 2π). Since 0 < α < π/2, π < Θ < 2π. The geometric
  angle θ is 2π − Θ = 2π − (π + 2α) = π − 2α. Since 0 < α < π/2, 0 < θ < π. Thus θ ∈ (0, 2π).
  We have proven the existence of D = D∗ ̸= A inside ∠XY Z and θ = π − 2α ∈ (0, 2π) satisfying the condition.


   Case 1: review from gpt-5

                                                                                         (c−a)e−iα
                                                                                                    
   <verification>false</verification> The bilinear relation from Im                        beiα −a       = 0 is computed with
   a sign error. Expanding Im(N · D) = 0 gives cb sin(2α) + rb sin(2α − ϕ) − rc sin(α + ϕ) + r2 sin α = 0, so
   the coefficient of b is A12 = r sin(2α − ϕ), not A12 = −r sin(2α − ϕ) as stated. This sign error undermines the
   subsequent locus equation.

The manually annotated label in the dataset is true (7 points). However, our verification method found an algebraic error in
the proof’s procedure, suggesting the score should be lower (e.g., 5-6 points).

   Case 1: our comment
  The derivation of the bilinear relation coefficients (A11 through A22 ) contained a systematic sign error. For instance,
  the coefficient A12 was calculated with the wrong sign. This error did not propagate to the final construction of point
  D because the necessary values were derived from ratios of the coefficients (e.g., A22 /A11 ), where the overall sign
  difference cancelled out.

   Case 2: problem

   Find all functionsf : Z → Z such that the equation

                                              f (x − f (xy)) = f (x)f (1 − y)

   holds for all x, y ∈ Z.



                                                            19
                                Pessimistic Verification for Open-Ended Math Questions

 Case 2: proof

We are looking for all functions f : Z → Z such that the equation

                                         f (x − f (xy)) = f (x)f (1 − y)    (∗)

holds for all x, y ∈ Z. Let P (x, y) be the assertion (∗).
**1. Constant solutions** If f (x) = c for all x ∈ Z. Then c = c · c, so c2 = c. This implies c = 0 or c = 1. Solution
1: f (x) = 0. (LHS=0, RHS=0). Solution 2: f (x) = 1. (LHS=1, RHS=1).
**2. Non-constant solutions** P (0, y) =⇒ f (0 − f (0)) = f (0)f (1 − y). f (−f (0)) = f (0)f (1 − y). The LHS is
constant. If f (0) ̸= 0, then f (1 − y) is constant. As y spans Z, f (x) is constant. This contradicts the assumption that
f is non-constant. Thus, we must have f (0) = 0.
P (x, 0) =⇒ f (x − f (0)) = f (x)f (1). f (x) = f (x)f (1). Since f is not identically zero, there exists x0 such that
f (x0 ) ̸= 0. Thus, f (1) = 1.
P (x, 1) =⇒ f (x − f (x)) = f (x)f (1 − 1) = f (x)f (0) = 0. (E1) P (1, y) =⇒ f (1 − f (y)) = f (1)f (1 − y) =
f (1 − y). (E2)
Let Z = {z ∈ Z | f (z) = 0} be the set of zeros of f . We know 0 ∈ Z. (E1) implies that x − f (x) ∈ Z for all x ∈ Z.
**3. Case Z = {0}** If 0 is the only zero, then x − f (x) = 0 for all x. Solution 3: f (x) = x. Verification: LHS
= f (x − xy) = x − xy. RHS = f (x)f (1 − y) = x(1 − y) = x − xy.
**4. Case Z ̸= {0}** Let k be the smallest positive integer in Z. Since f (1) = 1, k ≥ 2.
If z ∈ Z, f (z) = 0. By (E2), f (1 − z) = f (1 − f (z)) = f (1 − 0) = f (1) = 1.
We will show that k must be 2 or 3.
**Step 4.1: Suppose k is even.** Let k = 2m for some integer m ≥ 1. f (k) = f (2m) = 0. P (m, 2) =⇒
f (m − f (2m)) = f (m)f (1 − 2). f (m − 0) = f (m)f (−1). f (m) = f (m)f (−1).
If m = 1, then k = 2. If m > 1, then 1 < m < k. By the definition of k, f (m) ̸= 0. Thus f (−1) = 1.
P (1, −1) =⇒ f (1 − f (−1)) = f (1)f (1 − (−1)). f (1 − 1) = 1 · f (2). f (0) = f (2). So f (2) = 0. This means
k ≤ 2. Since k is even, k = 2. So, if k is even, k = 2.
**Step 4.2: Suppose k is odd.** k ≥ 3. f (k) = 0. Since k is odd, y = 1−k              2 is an integer. 1 − y =
                                                                                                                     1+k
                                                                                                                       2 .
                      1−k                                                                   1+k
P (2, y) =⇒ P (2, 2 ). f (2 − f (2y)) = f (2)f (1 − y). f (2 − f (1 − k)) = f (2)f ( 2 ). We know f (1 − k) = 1
(since k ∈ Z). f (2 − 1) = f (1) = 1. So 1 = f (2)f ( 1+k  2 ).
Since f (x) ∈ Z, f (2) must be 1 or −1.
If f (2) = 1. By (E1), f (2 − f (2)) = f (2 − 1) = f (1) = 0. But f (1) = 1. Contradiction (1 = 0). If f (2) = −1. By
(E1), f (2 − f (2)) = f (2 − (−1)) = f (3) = 0. This implies k ≤ 3. Since k is odd and k ≥ 3, we must have k = 3.
So, the smallest positive zero k can only be 2 or 3.
**Step 4.3: Case k=2.** f (2) = 0. f (1) = 1. We look for a solution where Z = 2Z (the set of even integers). If
Z = 2Z, f (x) = 0 iff x is even. Let x be odd (so f (x) ̸= 0) and y be even. xy is even, so f (xy) = 0. 1 − y is odd.
P (x, y) =⇒ f (x − f (xy)) = f (x)f (1 − y). f (x − 0) = f (x)f (1 − y). f (x) = f (x)f (1 − y). Since f (x) ̸= 0,
we must have f (1 − y) = 1. As y ranges over all even integers, 1 − y ranges over all odd integers. So f (z) = 1 for
all odd z.              (
                          0 if x is even
Solution 4: f (x) =                       (i.e., f (x) = x mod 2). Verification: Case 1: x is even. f (x) = 0. RHS=0.
                          1 if x is odd
f (xy) is 0 (if y is even) or f (x) = 0 (if y is odd). In both cases f (xy) = 0. LHS=f (x − 0) = 0. Case 2: x is odd.
f (x) = 1. RHS=f (1 − y). If y is even, 1 − y is odd (RHS=1). xy is even, f (xy) = 0. LHS=f (x − 0) = f (x) = 1.
If y is odd, 1 − y is even (RHS=0). xy is odd, f (xy) = 1. LHS=f (x − 1). Since x is odd, x − 1 is even, LHS=0.
**Step 4.4: Case k=3.** f (3) = 0. f (1) = 1. We found f (2) = −1. We look for a solution where Z = 3Z.
x − f (x) ∈ Z = 3Z,so f (x) ≡ x (mod 3). If f (x) ∈ {−1, 0, 1}, then f (x) is uniquely determined by x mod 3.
                      0
                              if x ≡ 0 (mod 3)
Solution 5: f (x) = 1          if x ≡ 1 (mod 3) . (This is the Legendre symbol (x/3)). Verification: This function f is
                      
                         −1 if x ≡ 2 (mod 3)
                      
completely multiplicative, f (xy) = f (x)f (y), and f (x) ∈ {−1, 0, 1}. The equation is f (x−f (x)f (y)) = f (x)f (1−
y). If f (x) = 0 (i.e., 3|x), LHS=0, RHS=0. If f (x) ̸= 0, then f (x) ∈ {1, −1}. LHS = f (x(1 − f (x)−1 f (y))). Since
f (x)−1 = f (x), LHS = f (x)f (1 − f (x)f (y)). We need f (x)f (1 − f (x)f (y)) = f (x)f (1 − y). Since f (x) ̸= 0,
we need f (1 − f (x)f (y)) = f (1 − y).


                                                           20
                                    Pessimistic Verification for Open-Ended Math Questions


   If f (x) = 1. f (1 − f (y)) = f (1 − y). This holds by (E2). If f (x) = −1. f (1 − (−1)f (y)) = f (1 + f (y)). We need
   f (1 + f (y)) = f (1 − y). If f (y) = 0 (y ≡ 0 (mod 3)). f (1) = 1. 1 − y ≡ 1 (mod 3), f (1 − y) = 1. If f (y) = 1
   (y ≡ 1 (mod 3)). f (1 + 1) = f (2) = −1. 1 − y ≡ 0 (mod 3), f (1 − y) = 0. −1 = 0.
   Let’s re-verify Solution 5 using the congruence property f (x) ≡ x (mod 3). LHS = f (x − f (xy)). RHS =
   f (x)f (1 − y). RHS ≡ x(1 − y) = x − xy (mod 3). LHS ≡ x − f (xy) (mod 3). Since f (xy) ≡ xy (mod 3).
   LHS ≡ x − xy (mod 3). Since LHS and RHS are both in {−1, 0, 1} and congruent modulo 3, they must be equal.
   Wait, there was an error in the verification attempt using multiplicativity above: If f (x) = −1 and f (y) = 1.
   f (1 + f (y)) = f (2) = −1. f (1 − y) = 0. −1 = 0. This derivation must be flawed.
   Let’s check the specific case: x = 2 (f (x) = −1), y = 1 (f (y) = 1). LHS: f (x − f (xy)) = f (2 − f (2)) =
   f (2 − (−1)) = f (3) = 0. RHS: f (x)f (1 − y) = f (2)f (0) = (−1)(0) = 0. The specific case holds.
   The error in the multiplicative derivation was assuming f (x − f (x)f (y)) = f (x)f (1 − f (x)f (y)) when f (x) ̸= 0.
   This requires f (a − b) = f (a)f (1 − b/a) which is generally not true. Multiplicativity f (ab) = f (a)f (b) works, but
   we cannot factor x out if x is not coprime to 3 (and even if it is, f (x − y) ̸= f (x)f (1 − y/x)).
   The verification using f (x) ≡ x (mod 3) is correct.
   We have found five solutions.
   Final Answer: The functions satisfying the equation are: 1. f (x)     = 0 for all x ∈ Z. 2. f (x) = 1 for all x ∈ Z. 3.
                                        (
                                                                        0
                                                                              if x ≡ 0 (mod 3)
                                          0 if x is even
   f (x) = x for all x ∈ Z. 4. f (x) =                    . 5. f (x) = 1       if x ≡ 1 (mod 3) .
                                          1 if x is odd                 
                                                                          −1 if x ≡ 2 (mod 3)
                                                                        


    Case 2: review from gpt-5

   The chunk makes critical, unjustified assumptions when classifying the non-constant solutions. In particular:
      • In Step 4.3 (k = 2), it assumes Z = 2Z (all even numbers are zeros) and then derives the parity solution, but it
        never proves from the functional equation that Z must equal 2Z or that f (odd) = 1.

      • In Step 4.4 (k = 3), it assumes Z = 3Z and that f (x) ∈ {−1, 0, 1}, using this to conclude the “Legendre symbol”
        form via a congruence argument. These constraints are not derived from k = 3 (only f (x) ≡ x (mod 3) is
        shown).
   Thus the claim that the five listed functions are all solutions is not established.

The manually annotated label in the dataset is true (7 points), while our method found a critical error in it:

    Case 2: our comment
   The proof is incomplete in steps 4.3 and 4.4 due to unjustified assumptions. For the k = 2 and k = 3 cases, the
   author assumes the set of zeros is Z = kZ and, for k = 3, further assumes f (x) ∈ {−1, 0, 1} to match the Legendre
   symbol form. While these specific functions are indeed solutions, the proof fails to derive that all solutions satisfying
   f (k) = 0 must necessarily possess this periodicity and range structure.

    Case 3: problem

   For a positive integer n, let An be the number of perfect powers less than or equal to n. Here, a perfect power is a
   number that can be expressed in the form ab , where a is a positive integer and b is an integer greater than or equal to 2.
   Prove that there are infinitely many n such that An divides n + 2024.

    Case 3: proof

   Let S be the set of perfect powers. A perfect power is a positive integer that can be expressed in the form ab , where a
   is a positive integer and b is an integer greater than or equal to 2. The set of perfect powers, sorted in increasing order,
   is {1, 4, 8, 9, 16, 25, 27, . . . }. For a positive integer n, An is the number of perfect powers less than or equal to n. So,


                                                                21
                                Pessimistic Verification for Open-Ended Math Questions


An = |S ∩ {1, 2, . . . , n}|. The function An is a non-decreasing step function. It is constant between consecutive
perfect powers. Let pk denote the k-th perfect power. For any integer n in the range pk ≤ n < pk+1 , the value of An
is constant and equal to k.
We want to prove that there are infinitely many positive integers n such that An divides n + 2024.
Our strategy is to find an infinite sequence of disjoint integer intervals, and in each interval, find one such integer
n. Let’s consider an interval [pk , pk+1 − 1] where An is constant, equal to k. The condition we want to satisfy is
k | (n + 2024). This is equivalent to the congruence relation n ≡ −2024 (mod k). The interval [pk , pk+1 − 1]
contains pk+1 − pk consecutive integers. If the length of this interval is at least k, the integers it contains form a
complete residue system modulo k. In such a case, there is guaranteed to be an integer n in the interval satisfying
n ≡ −2024 (mod k).
So, the problem reduces to showing that there are infinitely many values of k for which the gap between consecutive
perfect powers, pk+1 − pk , is greater than or equal to k.
We will focus on a special subsequence of perfect powers: the squares. Consider the gaps between consecutive squares.
Let m ≥ 2 be an integer. We will analyze the interval of integers Im = [(m − 1)2 , m2 − 1]. We will show that for all
sufficiently large m: 1. An is constant for all n ∈ Im . To do this, we will prove that there are no perfect powers in the
open interval ((m − 1)2 , m2 ). 2. The length of the interval Im is greater than the value of An for n ∈ Im .
If these two conditions hold for some large m, let km be the constant value of An on Im . The length of Im is
(m2 − 1) − (m − 1)2 + 1 = 2m − 1. Condition 2 means 2m − 1 > km . As argued above, since the interval Im
contains 2m − 1 > km consecutive integers, there must exist an integer nm ∈ Im such that nm ≡ −2024 (mod km ).
For this nm , we have Anm = km , and thus Anm | (nm + 2024).
If we can show that these conditions hold for all m greater than some integer M , we can find a solution nm for each
m ≥ M . Since the intervals Im are disjoint for different m, the solutions nm will be distinct, proving that there are
infinitely many such integers.
We now formalize and prove these two main claims.
**Claim 1:** For all sufficiently large integers m, there are no perfect powers in the open interval ((m − 1)2 , m2 ).
**Proof:** A perfect power in the interval ((m − 1)2 , m2 ) cannot be a perfect square, as there are no integers between
m − 1 and m. Therefore, any such perfect power must be of the form xj where x ≥ 2 and j ≥ 3 are integers.
For xj to be in the interval, we must have (m − 1)2 < xj < m2 . Taking the j-th root of this inequality gives
(m − 1)2/j < x < m2/j . For an integer x to exist in this range, the length of the interval ((m − 1)2/j , m2/j ) must be
greater than 1 for some j. The possible values for the exponent j are limited by the condition 2j ≤ xj < m2 , which
implies j < 2 log2 m.
Let N (a, b) be the number of perfect powers in the open interval (a, b). The total number of perfect powers in
((m − 1)2 , m2 ) is bounded by the sum of the number of integer candidates for the base x over all possible prime
exponents j. For simplicity, we sum over all integers j ≥ 3:
                                                   ⌊2 log2 m⌋                                       
                                                     X
                            N ((m − 1)2 , m2 ) ≤                  ⌊m2/j ⌋ − ⌈(m − 1)2/j ⌉ + 1
                                                      j=3

A simpler bound is the sum of the lengths of the intervals for x:
                                                       ⌊2 log2 m⌋                           
                                                            X
                                N ((m − 1)2 , m2 ) ≤                  m2/j − (m − 1)2/j
                                                            j=3


Let’s analyze the term m2/j − (m − 1)2/j . By the Mean Value Theorem applied to the function f (t) = t2/j on the
interval [m − 1, m], for each j there exists some cj ∈ (m − 1, m) such that:

                                                                                          2 2j −1
                              m2/j − (m − 1)2/j = f ′ (cj ) · (m − (m − 1)) =              c
                                                                                          j j
                                                                            2
                                                                                −1               2
Since j ≥ 3, the exponent 2j − 1 is negative. As cj > m − 1, we have cjj             < (m − 1) j −1 . So, m2/j − (m − 1)2/j <
          2
2         j −1 .
j (m − 1)




                                                             22
                                 Pessimistic Verification for Open-Ended Math Questions


Now we bound the sum. For j ≥ 3, the exponent 2j − 1 ≤ 23 − 1 = − 13 . Assuming m − 1 ≥ 1, we have
        2
(m − 1) j −1 ≤ (m − 1)−1/3 .
                                                ⌊2 log2 m⌋                             ⌊2 log2 m⌋
                                                  X          2         2                   X        2
                                   2     2
                        N ((m − 1) , m ) <                     (m − 1) j −1 ≤                         (m − 1)−1/3
                                                   j=3
                                                             j                             j=3
                                                                                                    3

The number of terms in the summation is ⌊2 log2 m⌋ − 2 < 2 log2 m.
                                                            2                4 log2 m
                           N ((m − 1)2 , m2 ) < (2 log2 m) · (m − 1)−1/3 =
                                                            3              3(m − 1)1/3
As m → ∞, this upper bound tends to 0. To see this formally:
                                       4 log2 m              4 ln m
                                  lim            = lim                    =0
                                 m→∞ 3(m − 1)1/3  m→∞ 3 ln 2 · (m − 1)1/3


since any positive power of m grows faster than any power of ln m. Since N ((m − 1)2 , m2 ) must be a non-negative
integer, there must exist an integer M1 such that for all m ≥ M1 , N ((m − 1)2 , m2 ) = 0. This proves Claim 1.
**Claim 2:** For all sufficiently large integers m, 2m − 1 > A(m−1)2 .
**Proof:** We need an upper bound for An . The set of perfect powers is the union of the sets of squares, cubes, 5th
powers, and so on. A simple upper bound for An is obtained by summing the number of j-th powers up to n for all
j ≥ 2, ignoring overlaps which leads to overcounting. The number of j-th powers up to n is ⌊n1/j ⌋.
                                                    ⌊log2 n⌋                   ⌊log2 n⌋
                                                     X                          X
                                                                    1/j
                                             An ≤              ⌊n         ⌋<              n1/j
                                                      j=2                        j=2

We can write this as:
                                       An < n1/2 + n1/3 + n1/4 + · · · + n1/⌊log2 n⌋
The number of terms in the sum after n1/2 is ⌊log2 n⌋ − 2. For j ≥ 3, we have n1/j ≤ n1/3 (for n ≥ 1). So, we can
bound the sum as:
                            An < n1/2 + (⌊log2 n⌋ − 2)n1/3 < n1/2 + (log2 n)n1/3
Now, let’s apply this bound to A(m−1)2 . Let n = (m − 1)2 .
                                       p
                           A(m−1)2 < (m − 1)2 + (log2 ((m − 1)2 )) · ((m − 1)2 )1/3

                                  A(m−1)2 < m − 1 + (2 log2 (m − 1)) · (m − 1)2/3
We want to prove that 2m − 1 > A(m−1)2 for sufficiently large m. It is sufficient to show that:

                                   2m − 1 > m − 1 + 2 log2 (m − 1) · (m − 1)2/3

This inequality simplifies to:
                                             m > 2 log2 (m − 1) · (m − 1)2/3
For m > 1, we can divide by m2/3 :
                                                               2/3                               2/3
                                                        m−1                                       1
                        m1/3 > 2 log2 (m − 1) ·                            = 2 log2 (m − 1) · 1 −
                                                         m                                        m

As m → ∞, the term (1 − 1/m)2/3 approaches 1. The inequality will hold if m1/3 grows faster than 2 log2 (m − 1).
To confirm this, we examine the limit of their ratio:

                                                  x1/3            x1/3 ln 2
                                          lim               = lim
                                         x→∞ 2 log2 (x − 1)  x→∞ 2 ln(x − 1)




                                                                    23
                                   Pessimistic Verification for Open-Ended Math Questions


   Using L’Hôpital’s rule on this ∞
                                   ∞ form:

                               1 −2/3
                               3x       ln 2       ln 2 x − 1       ln 2 1/3
                        = lim         1      = lim        2/3
                                                              = lim     (x − x−2/3 ) = ∞
                           x→∞   2 · x−1      x→∞   6 x        x→∞   6

  Since this limit is infinite, x1/3 grows faster than any constant multiple of log2 (x − 1). Therefore, there exists an
  integer M2 such that for all m ≥ M2 , the inequality m1/3 > 2 log2 (m − 1) · (1 − 1/m)2/3 holds. This proves Claim
  2.
  **Conclusion**
  Let M = max(M1 , M2 ). For every integer m ≥ M , we have established the following: 1. From Claim 1, the interval
  ((m − 1)2 , m2 ) contains no perfect powers. This means that for any integer n in the interval Im = [(m − 1)2 , m2 − 1],
  the set of perfect powers less than or equal to n is the same as the set of perfect powers less than or equal to (m − 1)2 .
  Thus, An has a constant value for all n ∈ Im . Let this value be km = A(m−1)2 .
  2. From Claim 2, the inequality 2m − 1 > A(m−1)2 = km holds. The length of the interval Im is (m2 − 1) − (m −
  1)2 + 1 = 2m − 1. So, for m ≥ M , the length of the interval Im is strictly greater than km .
  We are looking for an integer n such that An | (n + 2024). For any m ≥ M , we seek an n ∈ Im satisfying
  km | (n + 2024). This is equivalent to finding an n in the range (m − 1)2 ≤ n ≤ m2 − 1 that satisfies the congruence:

                                                  n ≡ −2024        (mod km )

   The interval Im contains the sequence of consecutive integers (m − 1)2 , (m − 1)2 + 1, . . . , m2 − 1. The length of
   this sequence is 2m − 1. Since m ≥ M , we have 2m − 1 > km . Because the sequence of integers in Im is longer
   than a full cycle of residues modulo km , it is guaranteed to contain at least one integer from each residue class modulo
   km . In particular, there must exist an integer nm ∈ Im such that nm ≡ −2024 (mod km ). For this nm , we have
   Anm = km , and so Anm | (nm + 2024).
   For each integer m ≥ M , we have successfully found an integer nm that satisfies the given property. To complete the
   proof, we must show that this process generates an infinite number of distinct solutions.
   Let m and m′ be two integers such that M ≤ m < m′ . The solution nm lies in the interval Im = [(m − 1)2 , m2 − 1].
   The solution nm′ lies in the interval Im′ = [(m′ − 1)2 , (m′ )2 − 1]. Since m′ > m, we must have m′ ≥ m + 1. The
   smallest value in the interval Im′ is (m′ − 1)2 ≥ (m + 1 − 1)2 = m2 . The largest value in the interval Im is m2 − 1.
   So, for any n ∈ Im and n′ ∈ Im′ , we have n ≤ m2 − 1 < m2 ≤ n′ . This shows that the intervals Im and Im′ are
   disjoint. Consequently, the solutions nm ∈ Im and nm′ ∈ Im′ are distinct.
   Since we can choose any integer m ≥ M , we have constructed an infinite sequence of distinct solutions {nm }m≥M .
   Therefore, there are infinitely many integers n such that An divides n + 2024.

The manually annotated label in the dataset is true (7 points), while our method found a critical error in it:

    Case 3: review from GPT-5-mini
   <verification>false</verification>
   The main (fatal) error is in Claim 1: the author replaces the integer count
                                                 2/j  
                                                         − (m − 1)2/j + 1
                                                                         
                                                 m

   by the real length m2/j − (m − 1)2/j . That inequality is not valid in general (e.g. an interval of real length < 1 can
   still contain an integer). Thus the bound
                                                       X 2/j
                                       N (m − 1)2 , m2 ≤        m − (m − 1)2/j
                                                                                     
                                                              j

   is unjustified, and the conclusion “this sum → 0 ⇒ N = 0 for  large m” does not follow. Because of this mistake the
   proof does not establish that the open interval (m − 1)2 , m2 contains no perfect powers for all large m, and the rest
   of the argument (which depends critically on that claim) fails.



                                                              24
                                Pessimistic Verification for Open-Ended Math Questions

 Case 3: our comment
The gt label is wrong, the pred label is correct.
Fatal error in Claim 1: It is invalid to use the length of a real interval to upper-bound the number of integer points,
because when the interval length is ¡ 1 it may still contain integers. Therefore, the conclusion “limit = 0 =¿ final result
= 0” does not hold; Moreover, the proof has a totally wrong derivation that
                                                   ⌊2 log2 m⌋                                  
                                                     X
                            N ((m − 1)2 , m2 ) ≤                  ⌊m2/j ⌋ − ⌈(m − 1)2/j ⌉ + 1
                                                      j=3

                                                         ⌊2 log2 m⌋                        
                                                            X
                               ⇒ N ((m − 1)2 , m2 ) ≤                   m2/j − (m − 1)2/j
                                                            j=3

which is actually an unacceptable gap.

 Case 4: problem

Prove that there exist two real-coefficient polynomials P (x) and Q(x) satisfying the following condition:
(Condition) The degree of the polynomial P (x) is at least 2024, the degree of Q(x) is at least 2, and for any real
number x, the following holds:
                                             P (Q(x) − x − 1) = Q(P (x))

 Case 4: proof

We will prove the existence of such polynomials P (x) and Q(x) by constructing them. Our construction will follow
three main steps: 1. Find a pair of polynomials of low degree, let’s call them (P0 (x), Q0 (x)), that satisfies the given
functional equation. 2. Construct a high-degree polynomial, let’s call it R(x), that commutes with Q0 (x). 3. Combine
these polynomials to form the final pair (P (x), Q(x)) that satisfies all the given conditions.
Let the given equation be
                                        P (Q(x) − x − 1) = Q(P (x)) (∗).
Step 1: Finding a base solution pair
We look for a simple solution where P0 (x) and Q0 (x) have degree 2. Let’s try to relate them. A simple assumption is
that Q0 (x) is a linear perturbation of P0 (x). Let’s try the ansatz:

                                                Q0 (x) = P0 (x) + x + c

for some real constant c. Substituting this into the equation (∗): The left side’s argument becomes Q0 (x) − x − 1 =
(P0 (x) + x + c) − x − 1 = P0 (x) + c − 1. So the equation becomes P0 (P0 (x) + c − 1) = Q0 (P0 (x)).
Let y = P0 (x). For any value y in the range of P0 (x), the equation must hold:

                                                P0 (y + c − 1) = Q0 (y).

Using our ansatz for Q0 (y), we have Q0 (y) = P0 (y) + y + c. So, we obtain a functional equation for P0 (y):

                                           P0 (y + c − 1) = P0 (y) + y + c.

Let b = c − 1, so c = b + 1. The equation is

                                           P0 (y + b) − P0 (y) = y + b + 1.

Let m = deg(P0 ). If b ̸= 0, the degree of the polynomial on the left, P0 (y + b) − P0 (y), is m − 1. The degree of the
polynomial on the right is 1. For the identity to hold, the degrees must be equal, so m − 1 = 1, which implies m = 2.
Let P0 (y) = Ay 2 +By +C for some constants A, B, C ∈ R with A eq0. Substituting this into the difference equation:
A(y+b)2 +B(y+b)+C −(Ay 2 +By+C) = y+b+1 A(y 2 +2by+b2 )+B(y+b)+C− = Ay 2 −By−C = y+b+1


                                                            25
                                 Pessimistic Verification for Open-Ended Math Questions


2Aby + Ab2 + Bb = y + b + 1. This must be a polynomial identity in y. We can equate the coefficients of the powers
of y: 1. Coefficient of y: 2Ab = 1. 2. Constant term: Ab2 + Bb = b + 1.
This is a system of two equations with three unknowns (A, B, b). We can choose a value for one of them. Let’s
choose b = 2. From (1): 2A(2) = 1 =⇒ 4A = 1 =⇒ A = 1/4. Substitute A = 1/4 and b = 2 into (2):
(1/4)(22 )+B(2) = 2+1 =⇒ 1+2B = 3 =⇒ 2B = 2 =⇒ B = 1. The constant C can be any real number. For
simplicity, we choose C = 0. So, we have found a polynomial P0 (x) = 41 x2 + x. We have b = 2, so c = b + 1 = 3.
Now we find the corresponding Q0 (x): Q0 (x) = P0 (x) + x + c = ( 14 x2 + x) + x + 3 = 14 x2 + 2x + 3.
So, we have found a base solution pair: P0 (x) = 14 x2 + x Q0 (x) = 14 x2 + 2x + 3 Both have degree 2, satisfying the
degree condition for Q0 (x). Let’s verify that they satisfy (∗). Q0 (x) − x − 1 = ( 14 x2 + 2x + 3) − x − 1 = 14 x2 + x + 2.
LHS: P0 (Q0 (x) − x − 1) = P0 ( 14 x2 + x + 2) = 14 ( 14 x2 + x + 2)2 + ( 14 x2 + x + 2) = 64 1 4
                                                                                                x + 81 x3 + 34 x2 + 2x + 3.
RHS: Q0 (P0 (x)) = 4 (P0 (x)) + 2P0 (x) + 3 = 4 ( 4 x + x) + 2( 4 x + x) + 3 = 64 x + 18 x3 + 34 x2 + 2x + 3.
                       1          2                    1 1 2        2     1 2                1 4

LHS=RHS, so the pair (P0 , Q0 ) is a solution.
Step 2: Construction of a high-degree commuting polynomial
Our plan is to set Q(x) = Q0 (x) and P (x) = R(P0 (x)) for some polynomial R(x) with high degree. Let’s see what
condition R(x) must satisfy. Substitute P (x) = R(P0 (x)) and Q(x) = Q0 (x) into (∗): LHS: P (Q(x) − x − 1) =
R(P0 (Q0 (x) − x − 1)). Using the property of our base solution, P0 (Q0 (x) − x − 1) = Q0 (P0 (x)), we get: LHS =
R(Q0 (P0 (x))). RHS: Q(P (x)) = Q0 (R(P0 (x))). So, the equation becomes R(Q0 (P0 (x))) = Q0 (R(P0 (x))). Let
y = P0 (x). This identity must hold for all values y in the range of P0 . If we find a polynomial R that commutes with
Q0 , i.e., R(Q0 (y)) = Q0 (R(y)) for all y, then our equation will be satisfied. Since this is a polynomial identity, if it
holds for all y in the range of P0 (an infinite set), it holds for all y.
We need to find a polynomial R(x) that commutes with Q0 (x). A standard method for finding commuting polynomials
is to simplify Q0 (x) by a linear change of variables (conjugation). Q0 (x) = 14 x2 + 2x + 3 = 14 (x2 + 8x) + 3 =
 1                              1                                                   −1
     2                                    2
 4 (x + 8x + 16) − 4 + 3 = 4 (x + 4) − 1. Let L(x) = x + 4. Its inverse is L            (x) = x − 4. Let S(y) = 41 y 2 − 1.
                   −1
Then Q0 (x) = L (S(L(x))).
If we find a polynomial R̃(y) that commutes with S(y), then R(x) = L−1 (R̃(L(x))) will commute with
Q0 (x). This is because: R(Q0 (x)) = L−1 (R̃(L(L−1 (S(L(x)))))) = L−1 (R̃(S(L(x)))). Q0 (R(x)) =
L−1 (S(L(L−1 (R̃(L(x)))))) = L−1 (S(R̃(L(x)))). Since R̃ and S commute, R̃(S(y)) = S(R̃(y)), so R and
Q0 commute.
A simple way to find a polynomial that commutes with S(y) is to take iterates of S(y). Let S1 (y) = S(y) and
Sk (y) = S(Sk−1 (y)) for k ≥ 2. Then Sk (y) commutes with S(y) for any k ≥ 1. Let’s choose R̃(y) = Sk (y) for a
sufficiently large k. The degree of S(y) is 2. The degree of R̃(y) = Sk (y) is 2k . We define R(x) = L−1 (Sk (L(x))) =
Sk (x + 4) − 4. The degree of R(x) is 2k .
Step 3: Assembling the final solution
We are now ready to define P (x) and Q(x). - Let Q(x) = Q0 (x) = 14 x2 + 2x + 3. - Let R(x) be constructed with
k = 10, so R̃(y) = S10 (y) = S ◦10 (y), and R(x) = S10 (x + 4) − 4. - Let P (x) = R(P0 (x)) = R( 41 x2 + x).
Let’s check the conditions: 1. **Coefficients**: P0 , Q0 , L, L−1 , S are all real-coefficient polynomials. Any composi-
tion or iteration will also result in polynomials with real coefficients. So P (x) and Q(x) have real coefficients.
2. **Degree of Q(x)**: deg(Q) = deg(Q0 ) = 2. This satisfies deg(Q) ≥ 2.
3. **Degree of P(x)**: The degree of P (x) is the product of the degrees of R(x) and P0 (x). deg(P0 ) = 2.
deg(R) = deg(S10 ) = 210 = 1024. deg(P ) = deg(R) · deg(P0 ) = 1024 · 2 = 2048. We need deg(P ) ≥ 2024.
Our value 2048 satisfies this condition. (If we needed an even higher degree, we could just choose a larger k. For
instance, k = 11 would give deg(P ) = 4096.)
4. **The functional equation**: As shown in Step 2, the choice P (x) = R(P0 (x)) and Q(x) = Q0 (x) reduces the
equation (∗) to R(Q0 (P0 (x))) = Q0 (R(P0 (x))). Our construction of R(x) ensures it commutes with Q0 (x), so this
identity holds for all inputs, and thus for all real numbers x.
We have successfully constructed polynomials P (x) and Q(x) that satisfy all the required conditions. For completeness,
the polynomials are: - Q(x) = 14 x2 + 2x + 3. - P (x) = S10 ( 14 x2 + x + 4) − 4, where S(y) = 14 y 2 − 1 and S10 is
the 10th iterate of S(y).
This completes the proof that such polynomials exist.




                                                            26
                                     Pessimistic Verification for Open-Ended Math Questions

    Case 4: review from GPT-5-mini
   <verification>false</verification> The fatal error is in Step 2: the author claims Q0 (x) =
   L−1 (S(L(x))) with L(x) = x + 4 and then uses this to conclude that R(x) = L−1 (Sk (L(x))) commutes with
   Q0 whenever Sk commutes with S. But Q0 (x) = 1/4(x + 4)2 − 1 equals S(L(x)), not L−1 (S(L(x))). That
   mistaken conjugation breaks the commuting argument: the equality R(Q0 (x)) = Q0 (R(x)) does not follow from
   Sk ◦ S = S ◦ Sk under the provided definitions, and the displayed R(x) = Sk (x + 4) − 4 need not commute with Q0 .
   (Thus the key commuting-polynomial construction is invalid as written.)

The manually annotated label in the dataset is true (7 points), while our method found a typo in it:

    Case 4: our comment

   The review fromi GPT-5-mini actually points out a typo that Q0 (x) ̸= L−1 (S(L(x))). However, the choice of S does
   not really matter so we can fix the proof easily.


    Case 5: problem

   Prove that there exist two real-coefficient polynomials P (x) and Q(x) satisfying the following condition:
   (Condition) The degree of the polynomial P (x) is at least 2024, the degree of Q(x) is at least 2, and for any real
   number x, the following holds:

                                                 P (Q(x) − x − 1) = Q(P (x))


    Case 5: proof

   Let n = 2024. We are looking for real-coefficient polynomials P (x) and Q(x) such that deg(P ) ≥ n and P (Q(x) −
   x − 1) = Q(P (x)) for all real x.
   Let deg(P ) = dP and deg(Q) = dQ . Comparing the degrees of both sides of the equation P (Q(x) − x − 1) =
   Q(P (x)), we have deg(Q(P (x))) = dQ dP . deg(P (Q(x) − x − 1)) = dP deg(Q(x) − x − 1). If dQ > 1,
   deg(Q(x) − x − 1) = dQ , so deg(P (Q(x) − x − 1)) = dP dQ . If dQ = 1, let Q(x) = cx + d with c e0. Then
   Q(x) − x − 1 = (c − 1)x + d − 1. If c e1, deg(Q(x) − x − 1) = 1 = dQ , so deg(P (Q(x) − x − 1)) = dP · 1 = dP .
   The degree of Q(P (x)) is 1 · dP = dP . If c = 1, Q(x) = x + d. Q(x) − x − 1 = d − 1. deg(P (Q(x) − x − 1)) =
   deg(P (d − 1)) = 0. The degree of Q(P (x)) = P (x) + d is dP . For 0 = dP , P (x) must be a constant. Let P (x) = k.
   Then P (Q(x) − x − 1) = k and Q(P (x)) = Q(k) = k + d. So k = k + d =⇒ d = 0. Q(x) = x. In this case
   P (Q(x) − x − 1) = P (−1) and Q(P (x)) = P (x). So P (x) must be a constant k such that P (−1) = k. This works,
   but we need dP ≥ 2024. So we must have dQ ≥ 1 and c e1 if dQ = 1.
   Let’s try to find a solution with dQ = 1. Let Q(x) = cx + d with c e1. The condition is P ((c − 1)x + d − 1) =
   cP (x) + d. Let dP = n = 2024. Let P (x) = an xn + · · · + a0 with an e0. Comparing the leading coefficients,
   an ((c − 1)x)n + · · · = c(an xn ) + . . . . an (c − 1)n xn + · · · = can xn + . . . . Since an e0, we must have (c − 1)n = c.
   Let n = 2024. We need to show that there exists a real number c e1 such that (c − 1)2024 = c. Consider the function
   f (t) = (t−1)2024 −t for t ∈ R. f (t) is continuous. f (0) = (0−1)2024 −0 = 1 > 0. f (1) = (1−1)2024 −1 = −1 < 0.
   By the Intermediate Value Theorem, there exists c1 ∈ (0, 1) such that f (c1 ) = 0. Since c1 ∈ (0, 1), c1 e1.
   f (3) = (3 − 1)2024 − 3 = 22024 − 3 > 0. By the Intermediate Value Theorem, there exists c2 ∈ (1, 3) such that
   f (c2 ) = 0. Since c2 ∈ (1, 3), c2 e1. Let c be any such real root. For example, c = c1 or c = c2 . Now we need to find a
   polynomial P (x) of degree n = 2024 satisfying P ((c−1)x+d−1) = cP (x)+d for some d. Let’s try d = 1. We need
   P ((c−1)x) = cP (x)+1. Let P (x) = axn +b. a((c−1)x)n +b = c(axn +b)+1. a(c−1)n xn +b = acxn +cb+1.
                                                                                                                          1
   acxn + b = acxn + cb + 1. This requires b = cb + 1, so b(1 − c) = 1. Since c e1, we can choose b = 1−c                    . Let
                            n     1                                                               2024     1
   a = 1. Then P (x) = x + 1−c is a polynomial of degree n = 2024. Let P (x) = x                       + 1−c and Q(x) = cx + 1.
   P (x) has degree 2024 ≥ 2024. P (x) and Q(x) have real coefficients since c is real. Let’s verify the condition:
                                                                                  1                            1                1
   P (Q(x)−x−1) = P (cx+1−x−1) = P ((c−1)x) = ((c−1)x)2024 + 1−c                        = (c−1)2024 x2024 + 1−c    = cx2024 + 1−c .
                                   2024       1             2024      c          2024       c+1−c       2024     1
   Q(P (x)) = cP (x) + 1 = c(x          + 1−c ) + 1 = cx         + 1−c + 1 = cx          + 1−c = cx          + 1−c . The condition
   P (Q(x) − x − 1) = Q(P (x)) is satisfied. Thus, such polynomials P (x) and Q(x) exist.


                                                                 27
                                     Pessimistic Verification for Open-Ended Math Questions



   Final Answer: The final answer is P (x) and Q(x) exist


    Case 5: review from qwen3-30b-a3b

   <verification>false</verification> The solution incorrectly constructs Q(x) as a linear polynomial
   (degree 1), violating the problem’s requirement that deg(Q) ≥ 2. This critical error undermines the correctness of the
   solution.

The manually annotated label in the dataset is true (7 points), while our method found a critical error in it:

    Case 5: our comment
   deg(Q) has to be at least 2 so this construction cannot be accepted.

    Case 6: problem

   There are 120 students in DeepMind highschool, and each student ‘loves’ some of the students. Here ‘love’ is not
   always a mutual relationship; a student A may love B while B may not love A, and it is also possible that a student
   loves oneself. For the set F of all 2120 subsets of the students, define the function f : F → F as the function that
   maps each X ∈ F to the set of students loved by one or more students in X. For A, B ∈ F , A and B are said to
   have a ’lovely relationship’ iff there exists a natural number k such that f k (A) = B. Now we want to select distinct
   elements A1 , A2 , · · · At from F such that for any 1 ≤ i < j ≤ t, Ai and Aj have a lovely relationship. Let M (f ) be
   the maximum possible value of t. Show that M (f ) ≤ 270 . ”, ”proof”:S   ”Let S be the set of 120 students, and F = 2S
   be the power set of S. The function f : F → F is defined as f (X) = u∈X N (u), where N (u) is the set of students
   loved by student u. This defines a directed graph G = (S, E) where (u, v) ∈ E if u loves v.

    Case 6: proof

   The function f is a linear map over the vector space F120    2 , where subsets are identified with their characteristic vectors.
   The union operation corresponds to vector addition.
   A ’lovely relationship’ between two sets A, B ∈ F means that one can be reached from the other by repeated
   application of f . A collection of distinct sets {A1 , . . . , At } where any pair has a lovely relationship must form a chain
   under this reachability relation. We can reorder these sets to form a simple path in the functional graph of f . The
   maximum possible value of t, denoted M (f ), is the length of the longest such path. A maximal path can be written as
   A0 , A1 , . . . , At−1 , where Ai+1 = f (Ai ) for i = 0, . . . , t − 2, and all Ai are distinct.
   Our proof strategy is to analyze the structure of the graph G by decomposing it into a c̈orep̈art and an äcyclicp̈art. We
   will use the properties of the iterates of f on the whole set S.
   Let L0 = S, and define a sequence of subsets Lk = f k (S) for k ≥ 1. The function f is monotone, i.e., if X ⊆ Y ,
   then f (X) ⊆ f (Y ). Since L1 = f (S) ⊆ S = L0 , monotonicity implies f (L1 ) ⊆ f (L0 ), so L2 ⊆ L1 . This gives a
   descending chain of subsets: S = L0 ⊇ L1 ⊇ L2 ⊇ · · · .
   Since S is finite, this sequence must stabilize. Let p be the first integer such that Lp = Lp+1 . Let Cf = Lp . This is
   the ı̈mage coreöf the graph under f . From Lp+1 = f (Lp ), the stability condition Lp = Lp+1 means f (Cf ) = Cf .
   This implies that the function f , when restricted to the set Cf , acts as a permutation on the elements of Cf . Let’s
   call this permutation π. Let x ∈ Cf . Since f (Cf ) = Cf , every element in Cf must have at least one preimage in Cf .
   Since Cf is finite, this means f restricted to the elements of Cf is a bijection, i.e., a permutation π. This implies that
   for each x ∈ Cf , its neighborhood N (x) must be a singleton set {π(x)}, and π(x) ∈ Cf .
   Now we analyze the structure of any trajectory A0 , A1 , . . . , At−1 . Let m be the first index in the sequence such that
   Am is a subset of Cf . So Ai ot ⊆ Cf for i < m, and Am ⊆ Cf .                                              S
   The property f (Cf ) = Cf implies that for any u ∈ Cf , N (u) ⊆ Cf . Let X ⊆ Cf . Then f (X) = u∈X N (u) ⊆ Cf .
   This means that once a set in the trajectory is a subset of Cf , all subsequent sets in the trajectory are also subsets of
   Cf . So Ai ⊆ Cf for all i ≥ m. The total length of the trajectory is t = m + (t − m). The first part of the trajectory
   has length m, and the second part has length t − m. The two parts are disjoint because sets in the first part are not


                                                                 28
                                   Pessimistic Verification for Open-Ended Math Questions


  subsets of Cf , while sets in the second part are.
  Let’s bound the length of the pre-core part of the trajectory, m. Let U = S \ Cf . For i < m, Ai ∩ U e∅. Let
  AU                            C                                      C     U         C            U
    i = Ai ∩ U and Ai = Ai ∩ Cf . Ai+1 = f (Ai ) = f (Ai ∪ Ai ) = f (Ai ) ∪ f (Ai ). Since N (Cf ) ⊆ Cf , we
              C
  have f (Ai ) ⊆ Cf . Therefore, the part of Ai+1 outside the core is determined solely by the part of Ai outside the
  core: AU                                 C         U               U                                            U
           i+1 = Ai+1 ∩ U = (f (Ai ) ∪ f (Ai )) ∩ U = f (Ai ) ∩ U . The sequence of non-core parts (Ai )i≥0 evolves
  autonomously.                T
  The set Cf = Lp = k≥0 Lk consists of all vertices that can be reached by paths of arbitrary length from S. This
  means any vertex not in Cf cannot reach a cycle. The subgraph G[U ] induced by U = S \ Cf must be a Directed
  Acyclic Graph (DAG).
  Let v1 , v2 , . . . , v|U | be a topological sort of the vertices in U . For any edge (vi , vj ) in G[U ], we have i < j. For
                                                                                                              U
  any non-empty subset Y ⊆ U , define its rank         S as minr (Y ) = min{i | vi ∈ Y }. Let Yi = Ai . Suppose Yi e∅.
  Let j = minr (Yi ). Yi+1 = f (Yi ) ∩ U = u∈Yi (N (u) ∩ U ). Any vertex w ∈ N (vj ) ∩ U must have an index
  greater than j. The same applies to any other u ∈ Yi with index greater than j. Thus, for any vertex in Yi+1 ,
  its index in the topological sort is greater than j. This means minr (Yi+1 ) > minr (Yi ). The sequence of ranks
  minr (AU                    U
            0 ), minr (A1 ), . . . is strictly increasing as long as the sets are non-empty. Since the rank is at most |U |, the
  sequence of non-empty sets (AU                                             U             U
                                          i ) can have length at most |U |. Am−1 e∅ and Am = ∅. So m ≤ |U |. Let k = |Cf |.
  Then |U | = 120 − k. We have m ≤ 120 − k.
  Now let’s bound the length of the core part of the trajectory, t − m. For i ≥ m, the sets Ai are subsets of
  Cf . As we established,
                       S            for any x ∈ Cf , N (x) = {π(x)} where π is a permutation of Cf . So, for any X ⊆
  Cf , f (X) = x∈X {π(x)} = π(X). The trajectory for i ≥ m is given by Ai+1 = π(Ai ). The sequence is
  Am , π(Am ), π 2 (Am ), . . . , At−1 . Since these sets must be distinct, the length t − m is bounded by the order of
  the permutation π in the symmetric group on 2Cf . This is the order of the element Am . The maximum length
  is the maximum cycle length in the permutation group induced by π on 2Cf . This is bounded by the order of
  π acting on Cf . The order of π ∈ Sk is the least common multiple (lcm) of the lengths of its disjoint cycles.
  The maximum possible order for a permutation of k elements is given by Landau’s function g(k), defined as
  g(k) = maxn1 +···+nr =k lcm(n1 , . . . , nr ). So, t − m ≤ g(k).
  Combining the bounds for both parts, we get: t = m + (t − m) ≤ (120 − k) + g(k).
  We need to find an upper bound for h(k) = 120 − k + g(k)√for k ∈ {0, 1, . . . , 120}. Landau’s function g(k)
  grows subexponentially. The asymptotic growth is ln g(k) ∼ k ln k. Let’s check some values: h(0) = 120 −
  0 + g(0) = 120 + 1 = 121 (a trajectory on ∅ has length 1). h(1) = 120 − 1 + g(1) = 119 + 1 = 120.
  h(10) = 110 + g(10) = 110 + lcm(2, 3, 5) = 110 + 30 = 140. h(20) = 100 + g(20) = 100 + lcm(3, 4, 5, 7) =
  100 + 420 = 520. h(40) = 80 + g(40) = 80 + lcm(3, 5, 7, 8, 11) = 80 + 9240 = 9320. h(70) = 50 + g(70).
  g(70) = lcm(3, 4, 5, 7, 11, 13, 17) = 1161160. h(70) = 1161210. For k = 120, h(120) = g(120). A partition of
  120 into prime powers that gives a large lcm is 3, 4, 5, 7, 11, 13, 17, 19, 23. The sum is 102. Remaining 18. Add 1.
  g(102) is huge. For k = 120, g(120) is known to be ≈ 3.2 × 1010 .
  In all cases, the value of h(k) = 120 − k + g(k) is significantly smaller than 270 . 210 ≈ 103 . 270 = (210 )7 ≈
  (103 )7 = 1021 . The maximum value of h(k) for k ∈ [0, 120] is many orders of magnitude smaller than 270 . Therefore,
  we have shown that for any graph G, M (f ) ≤ max0≤k≤120 (120 − k + g(k)) ≪ 270 .
  This shows that M (f ) ≤ 270 .


   Case 6: review from qwen3-30b-a3b

  <verification>false</verification>
  The solution incorrectly claims that the function f corresponds to vector addition in F120
                                                                                         2 , which is invalid because f is
  defined via union (not symmetric difference). It also wrongly asserts that f restricted to the core Cf is a permutation,
  which fails to account for possible non-injective behavior of f . Additionally, the analysis of the core assumes each
  N (x) is a singleton, which is not guaranteed by the problem’s conditions. These critical errors undermine the proof’s
  validity.”

The case shows that model may misunderstand definitions if the explanation is unclear in some sense. Actually, the human
expert misunderstands it as well at first.


                                                               29
                               Pessimistic Verification for Open-Ended Math Questions

Case 6: our comment
The proof is true. The model misunderstands the definition of the function f . However, It can easily be misunderstood
due to the unclear explanation.




                                                         30
