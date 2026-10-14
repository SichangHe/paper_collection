                                                              Enhancing Large Language Models in Coding
                                                               Through Multi-Perspective Self-Consistency
                                                   Baizhou Huang 1,2,∗ Shuai Lu 3,† Weizhu Chen 3 Xiaojun Wan 1,2 Nan Duan 3
                                                          1
                                                            Wangxuan Institute of Computer Technology, Peking University
                                                 2
                                                   State Key Laboratory of Media Convergence Production Technology and Systems
                                                                             3
                                                                               Microsoft Research Asia
                                                {hbz19,wanxiaojun}@pku.edu.cn, {shuailu,wzchen,nanduan}@microsoft.com


                                                              Abstract                                                       75


                                                                                                                             70
                                            Large language models (LLMs) have exhibited
                                                                                                                             65
                                            remarkable ability in code generation. How-
                                                                                                                             60
                                            ever, generating the correct solution in a sin-
                                            gle attempt still remains a challenge. Prior
arXiv:2309.17272v3 [cs.CL] 2 Jul 2024




                                                                                                         75   70   65   60   0    70   75   80   85

                                                                                                                             5
                                            works utilize verification properties in soft-
                                                                                                                             10
                                            ware engineering to verify and re-rank solu-
                                                                                                                             15
                                            tions in a majority voting manner. But the
                                                                                                                             20
                                            assumption behind them that generated veri-
                                            fication properties have better qualities than
                                            solutions may not always hold. In this paper,         Figure 1: Pass@1 of MPSC. With ChatGPT as the
                                            we treat them equally as different perspectives       foundation model, MPSC even surpasses GPT-4 and
                                            of LLMs’ reasoning processes. We propose the          achieves SOTA performance on all four benchmarks.
                                            Multi-Perspective Self-Consistency (MPSC)
                                            framework incorporating both inter- and intra-
                                            consistency across outputs from multiple per-         models to generate source codes from provided nat-
                                            spectives. Specifically, we prompt LLMs to            ural language intents. Many foundation models
                                            generate diverse outputs from three perspec-          have exhibited remarkable zero-shot performance
                                            tives, Solution, Specification and Test case, con-
                                                                                                  in code generation, such as ChatGPT and GPT4
                                            structing a 3-partite graph. With two mea-
                                            sure functions of consistency, we embed both          (OpenAI, 2023), with successful deployments in
                                            inter- and intra-consistency information into         real-world applications like Github Copilot.
                                            the graph. The optimal choice of solutions               Despite the remarkable abilities, LLMs often
                                            is then determined based on analysis in the           struggle to generate the correct code in a single
                                            graph. MPSC significantly boosts performance          attempt. Therefore, previous works sample diverse
                                            of foundation models (ChatGPT in this paper)
                                                                                                  codes from LLMs and re-rank them by introduc-
                                            on various benchmarks, including HumanEval
                                            (+15.91%), MBPP (+6.43%) and CodeContests             ing verification properties from software engineer-
                                            (+9.37%), even surpassing GPT-4.1                     ing. For example, CodeT (Chen et al., 2022) gen-
                                                                                                  erates test cases as a verification property, while
                                        1   Introduction                                          ALGO (Zhang et al., 2023) generates oracles, the
                                                                                                  brute-force version of desired algorithms, as a ver-
                                        In recent years, pre-trained large language models
                                                                                                  ification property. These methods are essentially
                                        (LLMs) have demonstrated unprecedented profi-
                                                                                                  variants of majority voting, making the assumption
                                        ciency in understanding, generating, and reasoning
                                                                                                  that the correctness of experts (i.e. the verifica-
                                        with human language (Brown et al., 2020; Chowd-
                                                                                                  tion properties) is better than that of choices (i.e.
                                        hery et al., 2022; OpenAI, 2023; Touvron et al.,
                                                                                                  the desired code outputs). However, both verifica-
                                        2023). Among the diverse applications of LLMs,
                                                                                                  tion properties and desired code outputs are usually
                                        code generation stands out as pivotal task and
                                                                                                  generated by the identical model with respect to
                                        has been acknowledged as a fundamental task for
                                                                                                  the same question, and hence the preference over
                                        benchmarking (Liang et al., 2023). This task entails
                                                                                                  verification properties is not always correct.
                                            ∗
                                             Work done during internship at Microsoft.
                                            †                                                        Instead, we believe that both desired code out-
                                             Corresponding author.
                                           1
                                             The code is available at https://github.com/skpig/   puts and verification properties should be treated
                                        MPSC.                                                     equally, since they are different perspectives of
LLM’s deliberate thinking process in face of iden-        2     Multi-Perspective Self-Consistency
tical questions. Aggregating various outputs from
different perspectives can lead to a more credible        A single perspective can often lead to an incomplete
result. To achieve this, we propose the Multi-            understanding of a problem, akin to the parable of
Perspective Self-Consistency (MPSC) framework             “blind men describing an elephant". The reasoning
that incorporates both inter-consistency across mul-      process of LLMs follows a similar pattern. LLMs
tiple perspectives and intra-consistency within a         generally cannot guarantee the correctness of gen-
single perspective. In this way, MPSC can fully           erated output in a single attempt, especially in code
leverage the consistency information within LLMs          generation, which necessitates proficient natural
and select the model output with the most consis-         language understanding, deliberate reasoning and
tent functionality as the final answer.                   rigorous controllability.
                                                             However, a key aspect of human intelligence is
                                                          the ability to think from multiple perspectives, re-
   In our framework, various verification tech-           sulting in a more comprehensive understanding of
niques from software engineering can be included          situations and more accurate solutions to problems.
as extended perspectives for better reasoning.            Inspired by the human cognition process, we pro-
Specifically, we prompt the LLM to simultane-             pose a novel code generation method by reasoning
ously generate diverse outputs from three well-           from three well-established perspectives, solutions,
established perspectives in software engineering,         specifications and test cases. Although noisy out-
namely Solution, Specification and Test case (Abra-       puts may inevitably be included in the generated
hamsson et al., 2017). Solutions implement the            outputs of every perspective, we can leverage both
desired functionality, specifications demonstrate         intra-consistency and inter-consistency among the
the intended properties in formal language, while         diverse outputs to distinguish the best ones from
test cases outline the expected behavior for some         the noise. An overview of our proposed MPSC
specific inputs. Then, we treat these model outputs       method is illustrated in Figure 2.
as vertices in a graph, and establish connections (i.e.
edges) based on the pairwise agreement of vertices        2.1    Solution, Specification and Test Case
from different perspectives. Our goal is to iden-
                                                          Given a user intent in natural language, we intro-
tify the most reliable output using a score function,
                                                          duce solution, specification and test case as three
which evaluates all vertices by considering both
                                                          perspectives to describe the desired functionality.
intra- and inter-consistency information encoded in
                                                          A solution is the source code implementing the
the graph. Specifically, the intra-consistency infor-
                                                          functionality denoted as g : X → Y, which is
mation guides the function to favor the most inter-
                                                          also the target of code generation. A test case is
nally consistent output within a single perspective,
                                                          a pair of valid input and output satisfying the re-
while inter-consistency ensures that the scores for
                                                          quired functionality denoted as (x, y) ∈ X × Y.
two outputs from different perspectives are similar
                                                          Specification draws inspiration from Formal Veri-
if they reach a consensus. We formalize the learn-
                                                          fication in software engineering, which mathemat-
ing process of the score function as an optimization
                                                          ically proves the correctness of one program by
problem adhering to these two consistency criteria
                                                          ensuring its satisfaction of some certain formal
and leverage an iterative algorithm proposed by
                                                          specifications. In the context of software engineer-
Zhou et al. (2003b) to achieve this goal.
                                                          ing, formal verification is usually written in formal
                                                          programming languages, e.g. Coq (Team, 2023)
   We evaluate MPSC on four widely used code              and Dafny (Leino, 2010), and conducted by accom-
generation benchmarks, including HumanEval                panying verification tools. For the generalization of
(Chen et al., 2021), HumanEval+ (Liu et al., 2023),       the proposed method in different program language
MBPP (Austin et al., 2021) and CodeContests (Li           scenarios, we adopt the idea of formal verification
et al., 2022). Experimental results show that our         and limit the specifications within pre-conditions
method boosts the performance of ChatGPT by a             and post-conditions, which can be written as func-
large margin, 15.91% in HumanEval, 15.64% in              tions in the same programming language like so-
HumanEval+, 6.43% in MBPP and 9.37% in Code-              lutions, without struggling with formal languages.
Contests. Our framework even surpasses GPT-4              Specifically, a pre-condition constrains the require-
(OpenAI, 2023) as shown in Figure 1.                      ments that a valid input should satisfy, while a
  User Instruction
 ""”
 Given a list l, return median of elements in the list.                     𝑣!()*%
 >>> median([3, 1, 2, 4, 5])
     3                                                                                                            Confident Score
 >>> median([-7, 4, 6, 100, 10, 20])                               "#$%
     15.0                                                         𝑣!
 """

                                                                             ()*%
                                                                            𝑣&                             high             ()*%
                                                                                                                    "#$%
                                                                                                                   𝑣!      𝑣!      𝑣&+*(+
                                                                   "#$%
                                                                 𝑣&                    𝑣!+*(+
  Solution
   Solution                                                                                                         "#$%    ()*%
 def Solution
      median(l: list):
                                                                             ()*%                                  𝑣&      𝑣'      𝑣'+*(+
   defl median(l:
     def
        = sorted(l)
          median(l:
                    list):                                                  𝑣'
      ifl len(l)  % 2 list):
           = sorted(l) == 1:
        iflreturn
             = sorted(l)
            len(l)  % 2 == 1:
                   l[len(l)//2]
          if return
      else:   len(l) l[len(l)//2]
                      % 2 == 1:
                                                                   "#$%
        else:  return
           return      l[len(l)//2]
                   (l[len(l)//2  - 1] + l[len(l)//2]) / 2.0      𝑣'                    𝑣&+*(+                       "#$%
                                                                                                                   𝑣'
                                                                                                                            ()*%
                                                                                                                           𝑣&      𝑣!+*(+
          else:
             return (l[len(l)//2 - 1] + l[len(l)//2]) / 2.0
               return (l[len(l)//2 - 1] + l[len(l)//2]) / 2.0



  Specification
   Specification                                                                                           low
     Specification
 def preconditions(l):
     assert isinstance(l, list)                                                        𝑣'+*(+
     assert all([isinstance(i, (int, float)) for i in l])

 def postconditions(l, output):
     assert isinstance(output, (int, float))
     num_greater = sum([1 for i in l if i >= output])
     num_less = sum([1 for i in l if i <= output])
     assert num_greater == num_less
                                                                          Inter-consistency Measure
                                                                          over Edges                         Optimization
                                                                                                                          !
                                                                                                              Objectives
  Test case
    Test case
                                                                          Intra-consistency Measure
     Testmedian([-10,
  assert  case        4, 6, 1000, 10, 20]) == 8.0
   assert median([-10, 4, 6, 1000, 10, 20]) == 8.0
                                                                          over Vertices
    assert median([-10, 4, 6, 1000, 10, 20]) == 8.0




                   Stage 1.                                                    Stage 2.                                Stage 3.
         Multi-Perspectives Generation                          Multi-Perspective Consistency Measures             Output Reranking



Figure 2: Overview of our MPSC code generation method. (a) Stage 1: we require a LLM to generate diverse
solutions, specifications and test cases. A detailed example of the three perspectives of function median(l) from
HumanEval is presented. (b) Stage 2: we construct a 3-partite graph based on the generated outputs and then
calculate both inter- and intra-consistency measures over edges and vertices respectively. The magnitudes of
measurements are demonstrated by the shade of colors. (c) Stage 3: Incorporating the multi-perspective consistency
information, we then learn a score function to re-rank outputs within each perspective.


post-condition constrains the relationships that a                          2.3      Inter-Consistency between Different
pair of valid inputs and outputs should satisfy. We                                  Perspectives
denote them as hpre : X → {F alse, T rue} and
                                                                            We distinguish between two kinds of consis-
hpost : X × Y → {F alse, T rue}. Detailed exam-
                                                                            tency based on the perspectives involved. Intra-
ples of outputs are shown in Figure 2.
                                                                            consistency is defined as the degree to which a
                                                                            given output aligns with others within the same per-
2.2      Graph Construction                                                 spective, following the original definition in Wang
                                                                            et al. (2022). Conversely, inter-consistency is de-
We require LLMs to generate diverse outputs from                            fined as the degree of consensus between a pair of
all three perspectives. We employ an 3-partite                              outputs from two different perspectives.
graph representation to capture the relationships
                                                                               With the well-established definitions of these
among these generated outputs. Specifically, we
                                                                            three perspectives in software engineering, each
represent the generated solutions {g1 , g2 , ..., gI }
                                                                            output implicitly describes a latent functionality
with a vertex set V f unc , the specification set
                                                                            regardless of whether it is a solution, a specifica-
{(hpre    post        pre post
    1 , h1 ), ..., (hJ , hJ )} with V
                                             spec , the
                                                                            tion or a test case. Consequently, we define the
test case set {(x1 , y1 ), ..., (xK , yK )} with V test ,
                                                                            inter-consistency between two vertices from dif-
and hence construct a vertex set V = V f unc ∪
                                                                            ferent perspectives as the alignment of their latent
V spec ∪ V test . With edges connecting each pair
                                                                            functionalities. And the most appealing aspect is
of vertices from two distinct sets, we construct
                                                                            that we can quantify the alignments with a code
an undirected 3-partite graph G = (V, E). Our
                                                                            interpreter in a deterministic manner2 . We for-
goal is to leverage the graph to encode the multi-
                                                                            malize the inter-consistency as a measure function
perspective consistency information, and then learn
                                                                            ω(·, ·) : V × V → R (also the adjacency matrix
a score function f : V → R (also a vector
f , fi = f (vi )) from it to choose the most reliable                           2
                                                                                  We provide the Python code snippets implementing the
output among all.                                                           verification in Appendix B.
W , where Wi,j = ω(vi , vj )) to weight different                                 BLEU metrics (Papineni et al., 2002) as the loss
edges in different ways as shown in Table 1.                                      function L aiming at lexical similarity and assume
                                                                                  the hypothesis distribution is uniform, i.e.
          Vertex Types                    Expression of ω(vi , vj )                                       X
   vi   ∈ V f unc , v   j   ∈ V spec   Ex∈X [1hpre (x)→hpost (x,gi (x)) ]                 φ(vi ) = C ·           BLEU(vi , vj )
                                                  j          j
   vi ∈ V f unc , vj ∈ V test          1gi (xj )=yj                                                       vj ∈K(vi )
   vi ∈ V spec , vj ∈ V test           1hpre (xj )∧hpost (xj ,yj )
                                         i          i
   otherwise                           0                                          , where C is the normalizing constant so that mea-
                                                                                  sures of outputs in one perspective sum up to 1,
Table 1: Mathematical expressions of different inter-                             K(vi ) represents the other outputs within the same
consistency measures ω(·, ·).                                                     perspective as vi .
  We then derive an optimization objective based
                                                                                  Semantic intra-consistency by structural equiv-
on inter-consistency measurements,
                                                                                  alence. In the realm of graph theory, two vertices
  Linter =
                  X
                               Wi,j (f (vi ) − f (vj ))2 = f T Lf           (1)
                                                                                  are deemed structurally equivalent if they share
               (vi ,vj )∈E                                                        identical weighted connections with the same third-
                                                                                  party vertices. Utilizing this equivalence relation,
   , where L = D − W is the laplacian matrix                                      we delineate V f unc , V spec , and V test into their
of the graph G 3 . The loss function is the weighted                              respective structural equivalence classes. Noted
sum of the local variation of each edge on the graph.                             that the weights assigned to edges reflect the align-
An underlying assumption is that a pair of outputs                                ments of latent functionalities associated with the
exhibiting consistency are either both correct or                                 vertices, and hence outputs within each equivalence
both incorrect. Therefore, the difference between                                 class can be regarded as exhibiting consistent func-
scores of two connected vertices should be con-                                   tional behavior. Therefore, we define the intra-
strained by the penalty corresponding to the degree                               consistency measure based on the structural equiv-
of consistency, i.e. edge weight.                                                 alence classes within each perspective. Suppose
                                                                                  vi belongs to the solution set V f unc . The struc-
2.4     Intra-Consistency within the Same                                         tural equivalence class of vi is denoted as S(vi ) ⊂
        Perspective                                                               V f unc , and neighbor sets of vi can be partitioned
Following Wang et al. (2022), we define the intra-                                into two subsets {Nt (vi )|t ∈ {spec, test}} de-
consistency of one generated output as its similarity                             pending on the perspective they belong to. Overall,
to others within the same perspective, which is                                   the lexical intra-consistency measure is defined as
denoted as a function φ(·) : V → R (also a vector                                 the multiplication of these three sets, i.e.
y, yi = φ(vi )).                                                                                                     Y
   Wang et al. (2022) limits the consistency to mere                                         φ(vi ) = C · |S(vi )| ·   |Nt (vi )|
equalities in final answers, thereby lacking efficacy                                                                  t
when applied to open-form tasks. In the scenario                                  , where C is the normalizing constant. The notation
of code generation, we extend the scope of intra-                                 is similar when vi belongs to other perspectives.
consistency to lexical and semantic similarities.                                    Intra-consistency is in fact an estimate of the
                                                                                  LLM’s uncertainty (Kuhn et al., 2023; Xiong et al.,
Lexical intra-consistency by Bayes risk. Min-
                                                                                  2023b) and reflects the confidence of the model
imum Bayes risk decoding (Kumar and Byrne,
                                                                                  on one specific output. Therefore, we can utilize
2004) selects the hypothesis h ∈ H that minimizes
                                                                                  the intra-consistency information as a supervision
the expected loss R(h) = Ey∼P (y) [L(y, h)] over
                                                                                  signal by ensuring the closeness between the score
the distribution of label y. Because of the unavail-
                                                                                  function f and the intra-consistency measure φ
ability of P (y), P (h) is usually used as a proxy
                                                                                  with Mean Squared Error (MSE),
distribution in practice.
                      P Then the′ Bayes risk can be
                                           ′
rewritten as R(h) = h′ ∈H L(h , h) · P (h ), which                                              1 X                         1
                                                                                     Lintra =          |f (vi ) − φ(vi )|2 = ||f − y||2   (2)
is in fact measure the consistency of h over the                                                2 v ∈V                      2
                                                                                                  i
hypothesis space. Specifically, we utilize negative
   3
                                                                                  2.5   Optimization Formulation
    In our experiment, we use the symmetric normalized
                        1      1
Laplacian Lsym = D − 2 LD − 2 for more robust perfor-                             After all, following the criteria of inter- and intra-
mance.                                                                            consistency, we can then formulate the learning
process of f as an optimization problem that com-           the baseline without any prior intra-consistency
bines both Linter (Eq. 1) and Lintra (Eq. 2):               information and treats every vertex equally, i.e.
                                                            φ(vi ) = C. (2) MPSC-Label includes the public
               min {α · Linter + (1 − α) · Lintra }   (3)
              f :V →R                                       example test cases in docstrings as silver labels, i.e.
                                                            φ(vi ) = C · 1vi is label 5 . Further details regarding
   To solve this optimization problem on the graph,         the implementation of our method and baselines
we adopt the iterative algorithm proposed by Zhou           are provided in Appendix E.
et al. (2003b). The details of the algorithm can be
found in Appendix A.                                        3.2   Main Results
3       Experiment                                          The experimental results on the four benchmarks
                                                            are presented in Table 2. We observe that MPSC
3.1       Experiment Settings
                                                            consistently enhances the code generation capa-
Dataset and metrics. We conduct experiments                 bilities of the foundation model (i.e. GPT-3.5-
on four widely used Python code generation                  Turbo) across all benchmarks with a remarkable
benchmarks, including HumanEval, HumanEval+,                margin of improvement. Particularly, when k is
MBPP and CodeContests. HumanEval (Chen et al.,              set to 1, which is the most prevalent scenario
2021) and MBPP (Austin et al., 2021) are two                in real-world applications, the performance im-
hand-written Python programming problems. Hu-               provement is notably significant (+15.91% on Hu-
manEval+ (Liu et al., 2023) adds more unit tests            manEval, +15.64% on HumanEval+, +6.43% on
based on HumanEval. CodeContests (Li et al.,                MBPP and +9.37% on CodeContests). With the
2022) is a much more challenging dataset consist-           foundation model GPT-3.5-Turbo, our MPSC can
ing of competition problems from the Codeforces             even outperform GPT-4 in Pass@1 across all bench-
platform. The evaluation metric is Pass@k (Chen             marks. Compared to other post-hoc augmenta-
et al., 2021), which is an unbiased estimator of the        tion approaches, even though they utilize more test
probability that at least one out of the k solutions        cases, our MPSC still shows consistent advantages
generated by the model passes unit tests. Details           in all benchmarks, excluding the Pass@5 score in
about the metric can be found in Appendix C.                MBPP benchmark. MPSC-Uniform serves as the
                                                            bottom line of MPSC framework and still achieves
Implementation and baselines. We compare
                                                            great gains for the foundation model, which demon-
several baselines from different LLMs for code like
                                                            strates that relying on inter-consistency proves to be
ChatGPT4 (i.e. GPT-3.5-Turbo), GPT-4 (OpenAI,
                                                            entirely effective. Moreover, incorporating various
2023), Code Llama (Rozière et al., 2024), Wiz-
                                                            types of intra-consistency information leads to fur-
ardCoder (Luo et al., 2023) and Deepseek Coder
                                                            ther improvements. Specifically, MPSC-Label and
(Guo et al., 2024), to other post-hoc approaches
                                                            MPSC-Semantic exhibit particularly strong results.
enhancing LLMs during inference, including Self-
                                                            They are two representative approaches leverag-
consistency (Wang et al., 2022), MBR- EXEC (Shi
                                                            ing the external supervision signals or the internal
et al., 2022), CodeT (Chen et al., 2022) and Self-
                                                            consistency information respectively. Surprisingly,
collaboration (Dong et al., 2023). For both MPSC
                                                            MPSC-Semantic can match or even surpass MPSC-
and other post-hoc augmentation approaches, we
                                                            Label in some benchmarks, which further high-
employ GPT-3.5-Turbo as the foundation model to
                                                            lights the significance of consistency information
generate 200 solutions. MPSC additionally gener-
                                                            in LLMs. Besides, we also note that the perfor-
ates 50 specifications and 100 test cases for each
                                                            mance of MPSC-Semantic and MPSC-Lexical re-
problem. Following the original setting in Chen
                                                            mains largely unchanged as k increases. This phe-
et al. (2022), we additionally generate 500 test
                                                            nomenon aligns with the nature of MPSC, which
cases for other baselines.
                                                            assesses solutions based on their consistency within
Variants of MPSC. As shown in Eq.2, the intra-              the foundation model. It implies that top-ranked
consistency measure φ(·) is essentially used as a           solutions exhibit semantic similarity and are con-
supervision signal without leveraging the seman-            sistently either correct or incorrect. This reaffirms
tics of “consistency". Therefore, we include two            the capability of our proposed MPSC to effectively
variants in our experiments: (1) MPSC-Uniform is
                                                               5
                                                                 The number of example test cases is two in average.
    4
        https://chat.openai.com/                            Noted that MBPP doesn’t provide test cases in docstrings.
                  Benchmark                         HumanEval                                 HumanEval+
                    Metric            Pass@1         Pass@2        Pass@5       Pass@1         Pass@2        Pass@5
               GPT4                   81.48          86.31         90.46        70.52          75.48         79.54
               GPT-3.5-Turbo          68.38          76.24         83.15        58.75          66.58         73.96
               DeepSeekCoder          79.30          -             -            -              -             -
               WizardCoder            73.20          -             -            -              -             -
               Code Llama             62.20          -             -            -              -             -
               Self-consistency       73.86+5.48     73.93-2.31    74.10-9.05   63.50+4.75     64.70-1.88    65.67-8.29
               MBR- EXEC              72.96+4.58     76.47+0.23    79.00-4.15   62.12+3.37     67.08+0.50    71.38-2.58
               CodeT                  78.05+9.67     78.05+1.81    78.30-4.85   67.87+9.12     68.75+2.17    69.65-4.31
               Self-collaboration     74.40+6.02     -             -            -              -             -
               MPSC-Uniform           74.17+5.79     77.02+0.78    78.53-4.62   65.05+6.30     69.76+3.18    71.72-2.24
               MPSC-Lexical           82.32+13.94    84.76+8.52    86.48+3.33   74.39+15.64    75.00+8.42    77.24+3.28
               MPSC-Semantic          83.38+15.00    84.25+8.01    84.45+1.30   73.54+14.79    74.46+7.88    75.26+1.30
               MPSC-Label             84.29+15.91    86.79+10.55   87.13+3.98   73.47+14.72    76.66+10.08   77.25+3.29

                  Benchmark                           MBPP                                    CodeContests
                    Metric            Pass@1         Pass@2        Pass@5       Pass@1         Pass@2        Pass@5
               GPT-4                  71.26          74.27         76.99        6.1            8.28          11.72
               GPT-3.5-Turbo          66.80          72.34         76.60        2.57           4.22          7.16
               DeepseekCoder          70.00          -             -            -              -             -
               WizardCoder            61.20          -             -            2.15           3.40          5.37
               Code Llama             61.20          -             -            -              -             -
               Self-consistency       71.70+4.90     71.73-0.61    71.82-4.78   8.10+5.53      8.42+4.20     8.48+1.32
               MBR- EXEC              70.79+3.99     73.14+0.80    74.85-1.75   8.25+5.68      8.87+4.65     9.08+1.92
               CodeT                  71.90+5.10     71.95-0.39    72.02-4.58   9.92+7.35      10.18+5.96    10.30+3.14
               Self-collaboration     68.20+1.40     -             -            -              -             -
               MPSC-Uniform           69.34+2.54     70.06-2.28    71.85-4.75   4.71+2.14      6.65+2.43     8.31+1.15
               MPSC-Lexical           68.38+1.58     70.26-2.08    71.43-5.17   5.45+2.88      5.45+1.23     6.06-1.10
               MPSC-Semantic          73.23+6.43     73.29+0.95    73.55-3.05   10.09+7.52     10.29+6.07    10.30+3.14
               MPSC-Label             -              -             -            11.94+9.37     15.55+11.33   18.20+11.04

Table 2: The results on four code generation benchmarks. The foundation model for MPSC, Self-consistency,
MBR- EXEC, CodeT, Self-collaboration are all GPT-3.5-Turbo. The improvements are calculated between methods
and GPT-3.5-Turbo. The best and second best performance for each dataset are shown in bold and underline.

aggregate consistency information within LLMs,                        test cases in Table 5. The quality of all three per-
thereby selecting the most consistent answers. We                     spectives is insufficient individually. Indeed, the
have a more detailed discussion about this phe-                       generated verification properties (i.e. specifications
nomenon in Appendix C.                                                and test cases) are even poorer than the generated
                                                                      solutions. It implies that prior works (Zhang et al.,
3.3      Further Analysis                                             2023; Chen et al., 2022) relying on generated veri-
Ablation study. We conduct an ablation study                          fication properties as experts for majority voting on
to examine the impact of different perspectives on                    solutions may fail, as these experts perform worse
MPSC. The results are presented in Table 4. Evi-                      than the choices (i.e. solutions) themselves. Ad-
dently, both the specification and test case perspec-                 ditionally, it indicates that the significant improve-
tives play crucial roles in our framework. Addition-                  ments brought by MPSC do not solely depend on
ally, test cases contribute more to the improvements                  the high quality of verification properties. The
than specifications. We attribute the observation                     improvements come from the consistency informa-
to the better quality of test cases, as generating an                 tion within LLMs, which helps to distinguish noise
accurate test case is considerably simpler than ab-                   from high-quality solutions.
stracting a comprehensive and sound specification.
                                                                      Generalization over different LLMs. MPSC
Qualities of three perspectives. We present the
                                                                      is designed as a model-agnostic framework that
accuracy6 of generated solutions, specifications and
                                                                      assumes black-box access to the underlying foun-
   6
       Accuracy is equal to pass@1.                                   dation model. In assessing the extent of MPSC’s
                       Benchmark                            HumanEval                                                                    HumanEval+
                        Metric                Pass@1          Pass@2        Pass@5                             Pass@1                          Pass@2                         Pass@5
              GPT-4 (gpt4-0614)               81.48           86.31         90.46                              70.52                           75.48                          79.54
                           +MPSC              92.15+10.67     91.62+5.31    91.80+1.34                         81.72+11.2                      81.77+6.29                     82.12+2.58
              WizzardCoder-34B†               67.84           72.12         75.98                              58.70                           62.88                          66.88
                         +MPSC                74.06+6.22      75.00+2.88    75.07-0.91                         65.45+6.75                      65.71+2.83                     66.19-0.69
              Code Llama-34B                  51.78           59.24         67.07                              41.49                           48.30                          55.93
                          +MPSC               70.97+19.19     70.55+11.31   71.36+4.29                         58.44+16.95                     59.00+10.70                    60.02+4.09
              WizzardCoder-13B                60.35           66.10         72.01                              50.25                           56.00                          61.98
                         +MPSC                73.60+13.25     74.96+8.86    74.57+2.56                         61.33+11.08                     62.99+6.99                     62.67+0.69
              Code Llama-13B                  44.63           50.99         57.86                              35.93                           41.71                          48.19
                          +MPSC               62.94+18.31     64.93+13.94   64.66+6.80                         50.04+14.11                     51.24+9.53                     51.36+3.17
              WizzardCoder-7B                 53.81           59.62         66.06                              45.06                           50.83                          57.69
                         +MPSC                63.85+10.04     64.04+4.42    67.32+1.26                         53.69+8.63                      55.07+4.24                     59.45+1.76
              Code Llama-7B                   39.38           45.18         52.79                              34.33                           39.18                          45.25
                          +MPSC               58.54+19.16     57.83+12.65   59.31+6.52                         49.04+14.71                     49.96+10.78                    50.46+5.21
              Deepseek Coder-6.7B             71.73           80.92         86.73                              61.72                           71.42                          78.54
                          +MPSC               82.38+10.65     83.92+3.00    84.71-2.02                         70.04+8.32                      72.12+0.70                     73.96-4.58

Table 3: The performance of MPSC-Semantic with different foundation models. † : We use nucleus sampling with
temperature as 0.2 instead of greedy generation in this experiment. The best performance is shown in bold.

     Benchmark          HumanEval   HumanEval+     MBPP     CodeContests
                                                                                                1.0
 Ours                     83.38       73.54        73.23       10.09
                                                                              Ratio of Pass@1=100




   w/o Specification      82.32       73.52        70.18        9.17
   w/o Test case          78.30       68.49        72.00        8.71                            0.8
   w/o Both               68.38       58.75        66.80        2.57
                                                                                                0.6

Table 4: The ablation study results (Pass@1) on four                                            0.4                                                                                            CodeContests
benchmarks.                                                                                                                                                                                    HumanEval
                                                                                                                                                                                               MBPP
                                                                                                0.2

    Perspective         Solution     Specification         Test Case                            0.0
                                                                                                             4k)          8k)          12k
                                                                                                                                          )          6k)          0k)          4k)          8k)          2k)          6k)
                                                                                                      [0k,         [4k,         [8k,          [12
                                                                                                                                                 k, 1
                                                                                                                                                           [16
                                                                                                                                                              k, 2
                                                                                                                                                                        [20
                                                                                                                                                                           k, 2
                                                                                                                                                                                     [24
                                                                                                                                                                                        k, 2
                                                                                                                                                                                                  [28
                                                                                                                                                                                                     k, 3
                                                                                                                                                                                                               [32
                                                                                                                                                                                                                  k, 3
   HumanEval              68.38          45.93              63.82
     MBPP                 66.80          53.70              34.64                                                                       Sum of Edge Weights
                                                                             Figure 3: The correlation between the performance of
Table 5: Accuracy of solutions, specifications and test
                                                                             MPSC and the edge density.
cases generated by GPT-3-Turbo.

                                                                            sity on the framework’s efficacy. To address this,
generalization, we employ many other LLMs in                                we categorize all queries in the dataset into dis-
addition to ChatGPT as foundation models. In spe-                           tinct bins based on the total edge weights in their
cific, we consider the strongest model, GPT4, and                           corresponding graphs and compute the perfect per-
three highly proficient open-source coding LLMs,                            formance ratio (i.e. Pass@1=100) for each bin. In
Code Llama, WizardCoder and DeepSeek Coder                                  this experiment, we employ the MPSC-Uniform
in Python. The experimental results presented in                            configuration7 . Figure 3 illustrates the correlation
Table 3 show that MPSC consistently yields sig-                             between edge density and performance. The results
nificant improvements across all models, which                              clearly demonstrate a positive correlation between
demonstrates the robust generalization capabilities                         the number of edges and the overall performance
embedded in our proposed framework.                                         of our framework.

                                                                             Impact of sampling number. To examine the
Impact of edge sparsity. Our framework signif-
                                                                             effect of the sampling number of different perspec-
icantly depends on the inter-consistency informa-
                                                                             tives, we conduct an analysis experiment by vary-
tion between model outputs, which is represented
as edges within the constructed graph. A critical                                7
                                                                                   The Uniform configuration is utilized to eliminate the
question arises concerning the impact of edge spar-                          influence of intra-consistency information.
                                              #Test Case
 #Specification                                                                         referring to the consistency within the same LLM,
                      10            20            50           100           200
       10         78.93+10.55   80.08+11.7    83.82+15.44   83.96+15.58   84.17+15.79
                                                                                        they focus to tackle the inter-inconsistency prob-
       20
       50
                  77.17+8.79
                  80.23+11.85
                                80.13+11.75
                                80.24+11.86
                                              83.82+15.44
                                              82.24+13.86
                                                            83.42+15.04
                                                            83.38+15.00
                                                                          85.44+17.06
                                                                          83.57+15.19
                                                                                        lem between different models with a formal debate
      100         80.39+12.01   80.9+12.52    80.92+12.54   81.55+13.17   84.17+15.79   framework.
Table 6: Pass@1 of MPSC-Semantic with different sam-                                    LLM for code. LLMs pretrained on large-scale
pling numbers on HumanEval.                                                             code data have demonstrated strong capabilities in
                                                                                        the field of code generation, such as Codex (Chen
                                                                                        et al., 2021), AlphaCode (Li et al., 2022), Code-
ing the numbers of generated specifications and
                                                                                        Gen (Nijkamp et al., 2023), InCoder (Fried et al.,
test cases. As shown in Table 6, MPSC constantly
                                                                                        2022), StarCoder (Li et al., 2023), Code Llama
brings significant performance gains with varied
                                                                                        (Rozière et al., 2023), WizardCoder (Luo et al.,
specifications and test cases. We note that MPSC
                                                                                        2023), DeepSeekCoder (Guo et al., 2024). How-
generally suffers a slight degradation in perfor-
                                                                                        ever, they remain unreliable, particularly in sce-
mance when fewer specifications or test cases are
                                                                                        narios involving complex input-output mappings.
used, which is consistent with our intuition. But the
                                                                                        Because of the low tolerance of compilers and oper-
performance decline is relatively small (about 4%
                                                                                        ating systems for bugs, the instability makes LLMs
with only 10% of specifications and test cases re-
                                                                                        hard to deploy into real-world applications. Sev-
tained). The observation indicts the remarkable per-
                                                                                        eral methods have been proposed to mitigate the
formance and efficiency of MPSC, suggesting the
                                                                                        phenomenon (Shi et al., 2022; Chen et al., 2022;
potential for real-world application with reduced
                                                                                        Zhang et al., 2022; Key et al., 2022; Ni et al., 2023;
computational costs.
                                                                                        Dong et al., 2023; Olausson et al., 2023; Chen et al.,
                                                                                        2023b; Zhang et al., 2023). The line of work with
4    Related Work
                                                                                        the most direct relevance to ours is to re-rank gener-
Prompting techniques on consistency. Based                                              ated solutions in a post-hoc manner. For example,
on Chain-of-thought mechanism (Wei et al., 2022),                                       Shi et al. (2022) matches the execution results of
previous works have adopted various prompting                                           generated solutions for minimum Bayes risk selec-
techniques and decoding strategies to reveal the                                        tion. Zhang et al. (2022) prompts another model as
consistency of LLM outputs and further enhance                                          a reviewer to check whether generated programs
the capabilities of LLMs. One line of approaches                                        satisfy the given language instruction by measuring
decodes multiple times from the same perspective                                        p(instruction|program). CodeT (Chen et al., 2022)
and aggregate the results (Wang et al., 2022; Zhou                                      additionally generates test cases to verify the gen-
et al., 2022; Jung et al., 2022; Sun et al., 2022; Chen                                 erated solutions. Similarly, ALGO (Zhang et al.,
et al., 2023a). For example, Wang et al. (2022) tar-                                    2023) additionally generates exhaustive search al-
gets tasks with fixed answer sets and scores each                                       gorithms as oracle programs to generate high qual-
answer based on the output frequency. Building                                          ity test cases for verification.
on this, Sun et al. (2022) introduces recitation as
                                                                                        Ranking on graph. In our framework, the final
context for augmentation. While Jung et al. (2022)
                                                                                        stage is in fact a ranking problem in graph. There
focus on the two-value entailment relations (True or
                                                                                        exists some renowned graph ranking algorithms
False) between statements and explanations. They
                                                                                        like PageRank (Page et al., 1998) and HITS (Klein-
treat the inference process as a weighted MAX-
                                                                                        berg, 1999). While our approach is inspired by
SAT problem and utilize a logistic solver to solve it.
                                                                                        manifold ranking (Zhou et al., 2003b), which is
Another line draws inspiration from the “Dual Pro-
                                                                                        built upon a regularization framework on discrete
cess" in cognitive science, which posits that human
                                                                                        spaces (i.e. graphs in this scenario) (Zhou et al.,
reasoning is dominated by System 1 and System 2
                                                                                        2003a; Zhou and Schölkopf, 2004, 2005).
(Daniel, 2017; Sloman, 1996). As a result, these ap-
proaches require LLMs to play different roles like                                      5   Conclusion
generator (i.e. System 1) and verifier (i.e. System
2), and optimize the result iteratively by a conversa-                                  In this paper, we present a novel code genera-
tional way (Madaan et al., 2023; Shinn et al., 2023;                                    tion method, Multi-Perspective Self-Consistency
Zhu et al., 2023). Xiong et al. (2023a) also pro-                                       (MPSC), aimed at enhancing the performance of
poses the concept of "inter-consistency". Instead of                                    LLMs in complex code generation tasks where a
single attempt may not suffice to ensure the ac-         References
curacy of the output. Our proposed MPSC strat-           Pekka Abrahamsson, Outi Salo, Jussi Ronkainen, and
egy capitalizes on both intra- and inter-consistency       Juhani Warsta. 2017. Agile software development
across three perspectives, solutions, specifications       methods: Review and analysis.
and test cases, to identify the most reliable an-
                                                         Jacob Austin, Augustus Odena, Maxwell Nye, Maarten
swer. We systematically validate the effectiveness          Bosma, Henryk Michalewski, David Dohan, Ellen
of MPSC through comprehensive experiments con-              Jiang, Carrie Cai, Michael Terry, Quoc Le, and
ducted on four widely used code generation bench-           Charles Sutton. 2021. Program Synthesis with Large
marks. The evaluation results demonstrate that              Language Models.
MPSC outperforms existing methods and achieves           Tom Brown, Benjamin Mann, Nick Ryder, Melanie
the state-of-the-art performance on all of them.           Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind
                                                           Neelakantan, Pranav Shyam, Girish Sastry, Amanda
Limitations                                                Askell, et al. 2020. Language models are few-shot
                                                           learners. Advances in neural information processing
Evaluation in the wild. Even though MPSC has               systems, 33:1877–1901.
shown remarkable performance on most widely
used code generation benchmarks, its effectiveness       Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan,
                                                           Zeqi Lin, Jian-Guang Lou, and Weizhu Chen. 2022.
in real-world scenarios remains largely unexplored.        CodeT: Code Generation with Generated Tests.
Existing code generation benchmarks often present
simplified code generation tasks compared to the in-     Mark Chen, Jerry Tworek, Heewoo Jun, Qiming
                                                          Yuan, Henrique Ponde de Oliveira Pinto, Jared Ka-
tricacies encountered in actual code developments,        plan, Harri Edwards, Yuri Burda, Nicholas Joseph,
where user intents are harder to understand and the       Greg Brockman, Alex Ray, Raul Puri, Gretchen
desired functionalities are more complex.                 Krueger, Michael Petrov, Heidy Khlaaf, Girish Sas-
                                                          try, Pamela Mishkin, Brooke Chan, Scott Gray,
Generalization to other tasks. Since our pro-             Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz
posed MPSC framework is designed to be model-             Kaiser, Mohammad Bavarian, Clemens Winter,
agnostic and task-agnostic. We only conduct ex-           Philippe Tillet, Felipe Petroski Such, Dave Cum-
                                                          mings, Matthias Plappert, Fotios Chantzis, Eliza-
periments in the code generation task in this paper.      beth Barnes, Ariel Herbert-Voss, William Hebgen
Actually, MPSC can be applied to other textual            Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie
generation tasks like math problem solving and            Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain,
question answering. However, unlike code gen-             William Saunders, Christopher Hesse, Andrew N.
                                                          Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan
eration, where code interpreter can measure the
                                                          Morikawa, Alec Radford, Matthew Knight, Miles
agreement between outputs in a deterministic way,         Brundage, Mira Murati, Katie Mayer, Peter Welinder,
assessing the agreement between natural language          Bob McGrew, Dario Amodei, Sam McCandlish, Ilya
outputs is non-trivial. A general task-agnostic inter-    Sutskever, and Wojciech Zaremba. 2021. Evaluating
consistency measure is to solely rely on LLMs,            Large Language Models Trained on Code.
whose evaluation ability for arbitrary textual inputs    Xinyun Chen, Renat Aksitov, Uri Alon, Jie Ren, Ke-
has been demonstrated recently. We leave it for            fan Xiao, Pengcheng Yin, Sushant Prakash, Charles
future works to discuss.                                   Sutton, Xuezhi Wang, and Denny Zhou. 2023a. Uni-
                                                           versal self-consistency for large language model gen-
Acknowledgments                                            eration.

This work was supported by National Key                  Xinyun Chen, Maxwell Lin, Nathanael Schärli, and
                                                           Denny Zhou. 2023b. Teaching Large Language Mod-
R&D Program of China (2021YFF0901502),                     els to Self-Debug.
Beijing Science and Technology Program
(Z231100007423011) and Key Laboratory of                 Aakanksha Chowdhery, Sharan Narang, Jacob Devlin,
Science, Technology and Standard in Press                  Maarten Bosma, Gaurav Mishra, Adam Roberts,
                                                           Paul Barham, Hyung Won Chung, Charles Sutton,
Industry (Key Laboratory of Intelligent Press              Sebastian Gehrmann, Parker Schuh, Kensen Shi,
Media Technology). We sincerely thank Xinyu                Sasha Tsvyashchenko, Joshua Maynez, Abhishek
Hu, Mingqi Gao, Xiao Pu and Xiang Chen for                 Rao, Parker Barnes, Yi Tay, Noam Shazeer, Vin-
providing insightful advice about this work. We            odkumar Prabhakaran, Emily Reif, Nan Du, Ben
                                                           Hutchinson, Reiner Pope, James Bradbury, Jacob
also appreciate the anonymous reviewers for their          Austin, Michael Isard, Guy Gur-Ari, Pengcheng Yin,
helpful comments.                                          Toju Duke, Anselm Levskaya, Sanjay Ghemawat,
                                                           Sunipa Dev, Henryk Michalewski, Xavier Garcia,
  Vedant Misra, Kevin Robinson, Liam Fedus, Denny            2023. Starcoder: may the source be with you! arXiv
  Zhou, Daphne Ippolito, David Luan, Hyeontaek Lim,          preprint arXiv:2305.06161.
  Barret Zoph, Alexander Spiridonov, Ryan Sepassi,
  David Dohan, Shivani Agrawal, Mark Omernick, An-         Yujia Li, David Choi, Junyoung Chung, Nate Kush-
  drew M. Dai, Thanumalayan Sankaranarayana Pil-             man, Julian Schrittwieser, Rémi Leblond, Tom Ec-
  lai, Marie Pellat, Aitor Lewkowycz, Erica Moreira,         cles, James Keeling, Felix Gimeno, Agustin Dal
  Rewon Child, Oleksandr Polozov, Katherine Lee,             Lago, Thomas Hubert, Peter Choy, Cyprien de Mas-
  Zongwei Zhou, Xuezhi Wang, Brennan Saeta, Mark             son d’Autume, Igor Babuschkin, Xinyun Chen, Po-
  Diaz, Orhan Firat, Michele Catasta, Jason Wei, Kathy       Sen Huang, Johannes Welbl, Sven Gowal, Alexey
  Meier-Hellstern, Douglas Eck, Jeff Dean, Slav Petrov,      Cherepanov, James Molloy, Daniel J. Mankowitz,
  and Noah Fiedel. 2022. PaLM: Scaling Language              Esme Sutherland Robson, Pushmeet Kohli, Nando
  Modeling with Pathways.                                    de Freitas, Koray Kavukcuoglu, and Oriol Vinyals.
                                                             2022. Competition-Level Code Generation with Al-
Kahneman Daniel. 2017. Thinking, fast and slow.              phaCode. Science, 378(6624):1092–1097.
Yihong Dong, Xue Jiang, Zhi Jin, and Ge Li. 2023.          Percy Liang, Rishi Bommasani, Tony Lee, Dimitris
  Self-collaboration Code Generation via ChatGPT.            Tsipras, Dilara Soylu, Michihiro Yasunaga, Yian
                                                             Zhang, Deepak Narayanan, Yuhuai Wu, Ananya Ku-
Daniel Fried, Armen Aghajanyan, Jessy Lin, Sida Wang,
                                                             mar, Benjamin Newman, Binhang Yuan, Bobby Yan,
  Eric Wallace, Freda Shi, Ruiqi Zhong, Wen-tau Yih,
                                                             Ce Zhang, Christian Cosgrove, Christopher D. Man-
  Luke Zettlemoyer, and Mike Lewis. 2022. Incoder:
                                                             ning, Christopher Ré, Diana Acosta-Navas, Drew A.
  A generative model for code infilling and synthesis.
                                                             Hudson, Eric Zelikman, Esin Durmus, Faisal Lad-
  arXiv preprint arXiv:2204.05999.
                                                             hak, Frieda Rong, Hongyu Ren, Huaxiu Yao, Jue
Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai            Wang, Keshav Santhanam, Laurel Orr, Lucia Zheng,
  Dong, Wentao Zhang, Guanting Chen, Xiao Bi,                Mert Yuksekgonul, Mirac Suzgun, Nathan Kim,
  Y. Wu, Y. K. Li, Fuli Luo, Yingfei Xiong, and Wen-         Neel Guha, Niladri Chatterji, Omar Khattab, Peter
  feng Liang. 2024. Deepseek-coder: When the large           Henderson, Qian Huang, Ryan Chi, Sang Michael
  language model meets programming – the rise of             Xie, Shibani Santurkar, Surya Ganguli, Tatsunori
  code intelligence.                                         Hashimoto, Thomas Icard, Tianyi Zhang, Vishrav
                                                             Chaudhary, William Wang, Xuechen Li, Yifan Mai,
Jaehun Jung, Lianhui Qin, Sean Welleck, Faeze Brah-          Yuhui Zhang, and Yuta Koreeda. 2023. Holistic eval-
   man, Chandra Bhagavatula, Ronan Le Bras, and              uation of language models.
  Yejin Choi. 2022. Maieutic prompting: Logically
   consistent reasoning with recursive explanations.       Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Ling-
   arXiv preprint arXiv:2205.11822.                           ming Zhang. 2023. Is your code generated by chat-
                                                              gpt really correct? rigorous evaluation of large lan-
Darren Key, Wen-Ding Li, and Kevin Ellis. 2022. I             guage models for code generation. arXiv preprint
  Speak, You Verify: Toward Trustworthy Neural Pro-           arXiv:2305.01210.
  gram Synthesis.
                                                           Ziyang Luo, Can Xu, Pu Zhao, Qingfeng Sun, Xi-
Jon M. Kleinberg. 1999. Authoritative sources in a           ubo Geng, Wenxiang Hu, Chongyang Tao, Jing Ma,
  hyperlinked environment. J. ACM, 46(5):604–632.            Qingwei Lin, and Daxin Jiang. 2023. Wizardcoder:
                                                             Empowering code large language models with evol-
Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. 2023.
                                                             instruct. arXiv preprint arXiv:2306.08568.
  Semantic uncertainty: Linguistic invariances for un-
  certainty estimation in natural language generation.
                                                           Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler
Shankar Kumar and William Byrne. 2004. Minimum              Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,
  Bayes-Risk Decoding for Statistical Machine Trans-        Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,
  lation. In Proceedings of the Human Language Tech-        Shashank Gupta, Bodhisattwa Prasad Majumder,
  nology Conference of the North American Chapter           Katherine Hermann, Sean Welleck, Amir Yazdan-
  of the Association for Computational Linguistics:         bakhsh, and Peter Clark. 2023. Self-Refine: Iterative
  HLT-NAACL 2004, pages 169–176, Boston, Mas-               Refinement with Self-Feedback.
  sachusetts, USA. Association for Computational Lin-
  guistics.                                                Ansong Ni, Srini Iyer, Dragomir Radev, Veselin Stoy-
                                                             anov, Wen-tau Yih, Sida Wang, and Xi Victoria Lin.
K. Rustan M. Leino. 2010. Dafny: An automatic pro-           2023. Lever: Learning to verify language-to-code
  gram verifier for functional correctness. In Logic for     generation with execution. In International Con-
  Programming, Artificial Intelligence, and Reasoning,       ference on Machine Learning, pages 26106–26128.
  pages 348–370, Berlin, Heidelberg. Springer Berlin         PMLR.
  Heidelberg.
                                                           Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan
Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas            Wang, Yingbo Zhou, Silvio Savarese, and Caiming
  Muennighoff, Denis Kocetkov, Chenghao Mou, Marc            Xiong. 2023. CodeGen: An Open Large Language
  Marone, Christopher Akiki, Jia Li, Jenny Chim, et al.       Model for Code with Multi-Turn Program Synthesis.
Theo X. Olausson, Jeevana Priya Inala, Chenglong          Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc
  Wang, Jianfeng Gao, and Armando Solar-Lezama.             Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery,
  2023. Demystifying GPT Self-Repair for Code Gen-          and Denny Zhou. 2022. Self-Consistency Improves
  eration.                                                  Chain of Thought Reasoning in Language Models.
R OpenAI. 2023. Gpt-4 technical report. arXiv, pages      Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
  2303–08774.                                                Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,
                                                             et al. 2022. Chain-of-thought prompting elicits rea-
Lawrence Page, Sergey Brin, Rajeev Motwani, and              soning in large language models. Advances in Neural
  Terry Winograd. 1998. The PageRank Citation Rank-          Information Processing Systems, 35:24824–24837.
  ing: Bringing Order to the Web. Technical report,
  Stanford Digital Library Technologies Project.          Kai Xiong, Xiao Ding, Yixin Cao, Ting Liu, and Bing
                                                            Qin. 2023a. Examining the Inter-Consistency of
Kishore Papineni, Salim Roukos, Todd Ward, and Wei-         Large Language Models: An In-depth Analysis via
  Jing Zhu. 2002. Bleu: a method for automatic evalu-       Debate.
  ation of machine translation. In Proceedings of the
  40th Annual Meeting of the Association for Compu-       Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie
  tational Linguistics, pages 311–318, Philadelphia,        Fu, Junxian He, and Bryan Hooi. 2023b. Can llms
  Pennsylvania, USA. Association for Computational          express their uncertainty? an empirical evaluation of
  Linguistics.                                              confidence elicitation in llms.

Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten    Kexun Zhang, Danqing Wang, Jingtao Xia,
  Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi,          William Yang Wang, and Lei Li. 2023. ALGO:
  Jingyu Liu, Tal Remez, Jérémy Rapin, et al. 2023.         Synthesizing Algorithmic Programs with Generated
  Code llama: Open foundation models for code. arXiv        Oracle Verifiers.
  preprint arXiv:2308.12950.
                                                          Tianyi Zhang, Tao Yu, Tatsunori B. Hashimoto, Mike
Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten      Lewis, Wen-tau Yih, Daniel Fried, and Sida I. Wang.
  Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi,          2022. Coder Reviewer Reranking for Code Genera-
  Jingyu Liu, Romain Sauvestre, Tal Remez, Jérémy           tion.
  Rapin, Artyom Kozhevnikov, Ivan Evtimov, Joanna         D. Zhou and B. Schölkopf. 2004. A Regularization
  Bitton, Manish Bhatt, Cristian Canton Ferrer, Aaron       Framework for Learning from Graph Data. In ICML
  Grattafiori, Wenhan Xiong, Alexandre Défossez,            2004 Workshop on Statistical Relational Learning
  Jade Copet, Faisal Azhar, Hugo Touvron, Louis Mar-        and Its Connections to Other Fields (SRL 2004),
  tin, Nicolas Usunier, Thomas Scialom, and Gabriel         pages 132–137.
  Synnaeve. 2024. Code llama: Open foundation mod-
  els for code.                                           Dengyong Zhou, Olivier Bousquet, Thomas Lal, Jason
                                                            Weston, and Bernhard Schölkopf. 2003a. Learning
Freda Shi, Daniel Fried, Marjan Ghazvininejad, Luke         with Local and Global Consistency. In Advances in
  Zettlemoyer, and Sida I. Wang. 2022. Natural Lan-         Neural Information Processing Systems, volume 16.
  guage to Code Translation with Execution. In Pro-         MIT Press.
  ceedings of the 2022 Conference on Empirical Meth-
  ods in Natural Language Processing, pages 3533–         Dengyong Zhou and Bernhard Schölkopf. 2005. Regu-
  3546, Abu Dhabi, United Arab Emirates. Association        larization on Discrete Spaces. In Pattern Recognition,
  for Computational Linguistics.                            Lecture Notes in Computer Science, pages 361–368,
                                                            Berlin, Heidelberg. Springer.
Noah Shinn, Beck Labash, and Ashwin Gopinath. 2023.
  Reflexion: An autonomous agent with dynamic mem-        Dengyong Zhou, Jason Weston, Arthur Gretton, Olivier
  ory and self-reflection.                                  Bousquet, and Bernhard Schölkopf. 2003b. Ranking
                                                            on Data Manifolds. In Advances in Neural Informa-
Steven A Sloman. 1996. The empirical case for two sys-      tion Processing Systems, volume 16. MIT Press.
   tems of reasoning. Psychological bulletin, 119(1):3.
                                                          Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei,
Zhiqing Sun, Xuezhi Wang, Yi Tay, Yiming Yang, and          Nathan Scales, Xuezhi Wang, Dale Schuurmans,
  Denny Zhou. 2022. Recitation-Augmented Lan-               Claire Cui, Olivier Bousquet, Quoc Le, et al. 2022.
  guage Models. In The Eleventh International Confer-       Least-to-most prompting enables complex reason-
  ence on Learning Representations.                         ing in large language models. arXiv preprint
                                                            arXiv:2205.10625.
The Coq Development Team. 2023. The coq proof
  assistant.                                              Xinyu Zhu, Junjie Wang, Lin Zhang, Yuxiang Zhang,
                                                            Yongfeng Huang, Ruyi Gan, Jiaxing Zhang, and Yu-
Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier
                                                            jiu Yang. 2023. Solving Math Word Problems via
  Martinet, Marie-Anne Lachaux, Timothée Lacroix,
                                                            Cooperative Reasoning induced Language Models.
  Baptiste Rozière, Naman Goyal, Eric Hambro,
                                                            In Proceedings of the 61st Annual Meeting of the
  Faisal Azhar, et al. 2023. Llama: Open and effi-
                                                            Association for Computational Linguistics (Volume
  cient foundation language models. arXiv preprint
                                                            1: Long Papers), pages 4471–4485.
  arXiv:2302.13971.
A    Details of the Iterative Algorithm                     Differentiate F with respect to f , we have
Description of algorithm. The iterative algo-                   ∂F
rithm is shown in Algorithm 1.                                     = α(I − T )f + (1 − α)(f − y)
                                                                ∂f

 Algorithm 1: Iterative Optimization                         Let the derivatives to 0, the solution f ′ =
  Input: degree matrix                                    (1 − α)(I − αT )−1 y = f ∗ . Therefore, the itera-
         D = diag(d1 , ..., dN ), initialization          tive algorithm is actually optimizing the objective
         score vector y, weighted adjacency               function.
         matrix W , threshold ϵ                           Results of closed-form solution. Despite the ex-
  Output: optimal confidence score vector                 istence of a closed-form solution for the optimiza-
           f∗                                             tion problem, the required matrix inversion opera-
  begin                                                   tion is computationally expensive. Conversely, the
     f (0) ←− y                                           iterative algorithm exhibits rapid convergence and
                     1          1
       T ←− D − 2 W D − 2                                 demonstrates strong empirical performance. Con-
       i ←− 0                                             sequently, we employ the iterative algorithm in our
       Do                                                 experiments. Additionally, we provide the perfor-
           f (i+1) ←− αT f (i) + (1 − α)y                 mance of the closed-form solution in Table 7. Our
           i ←− i + 1                                     results indicate that the iterative algorithm achieves
       While ||f (i) − f (i−1) || ≤ ϵ                     a performance on par with that of the direct com-
       f ∗ ←− f (i)                                       putation of the closed-form solution.
       return f ∗
                                                                Metric         Pass@1       Pass@2        Pass@5
                                                                                 HumanEval
Proof of Convergence We first expand the ex-               MPSC-Lexical      82.32/82.32   84.76/84.76   86.48/86.59
                                                           MPSC-Semantic     83.38/83.46   84.25/84.15   84.45/84.45
pression of f (n) according to the recursive formula
                                                                                HumanEval+
    f (n) = αT f (n−1) + (1 − α)y                          MPSC-Lexical      74.39/74.39   75.00/75.00   77.24/77.34
                                        n−1
                                        X                  MPSC-Semantic     73.54/73.97   74.46/75.04   75.26/75.96
        = (αT )n−1 f (0) + (1 − α)             (αT )i y                         CodeContests
                                         i=0
                                                           MPSC-Lexical       5.45/5.45     5.45/5.45     6.06/6.06
                                                           MPSC-Semantic     10.09/10.26   10.29/10.30   10.30/10.30
                                                                                    MBPP
Notice that T is similar to a stochastic ma-
                       1      1       1     1              MPSC-Lexical      68.38/68.38   70.26/70.26   71.43/71.43
trix W D −1 = D 2 (D − 2 W D − 2 )D − 2 =
   1      1                                                MPSC-Semantic     73.23/73.27   73.29/73.55   73.55/73.56
D 2 T D − 2 . Therefore the eigenvalues of αT are
in [−α, α]. With α ∈ (0, 1), we have                      Table 7: Performance of MPSC optimized by the it-
                                                          erative algorithm or calculating closed-form solution
                  lim (αT )n = 0                          directly. The results are presented in form of (iterative
              n→∞
               n−1
               X                                           algorithm / closed-form solution).
            lim          (αT )i = (I − αT )−1
          n→∞
                   i=0

Therefore

     f ∗ = lim f (n) = (1 − α)(1 − αT )−1 y
            n→∞

Proof of Equivalence           Denote the optimization
function as
                          1      1     (1 − α)
F = αf T (I − D − 2 W D 2 )f +                 (f − y)2
                                          2
                              (1 − α)
    = αf T (I − T )f +                (f − y)2
                                 2
     B    Implementation of Inter-Consistency                  29   final_result = check ()
                                                                    Listing 2: Inter-consistency between solutions and
     We present the code snippets measuring the inter- specifications.
     consistency between each pair of perspectives in
     Listing 1, 2, 3. After execution with Python inter- 1 """ Generated solutions """
     preter, the final_result is acquired as ω(vi , vj ). 2 def entry_point ( input ):
                                                                3   ...
 1 """ Generated specifications """                             4

 2 # Pre - conditions                                           5 """ Generated test cases """
 3 def preconditions ( input ):
                                                                6 test_case = { ' input ': ... ,
 4 ...
                                                                7               ' output ': ...}
                                                                8
 5
 6 # Post - conditions                                          9 """ Check inter - consistency """
 7 def postconditions ( input , output ):
                                                               10 def check () :
 8 ...
                                                               11      try :
 9
                                                               12            output = entry_point ( test_case [ '
10 """ Generated test cases """                                        input ' ])
11 test_case = { ' input ': ... ,                              13            pass_result = ( output ==
12               ' output ': ...}                                      test_case [ ' output ' ])
13
                                                               14      except Exception as e:
14 """ Check inter - consistency """                           15            pass_result = False
15 def check () :                                              16      return pass_result
                                                               17 global final_result
16      pass_result = None
                                                               18 final_result = check ()
17      try :
18            preconditions ( test_case [ ' input '                 Listing 3: Inter-consistency between solutions and test
        ])                                                          cases.
19            postconditions ( test_case [ ' input '
        ] , test_case [ ' output ' ])
20            pass_result = True
21      except Exception as e:
22            pass_result = False
23      return pass_result
24 global final_result
25 final_result = check ()

     Listing 1: Inter-consistency between specifications and
     test cases.


 1 """ Generated solutions """
 2 def entry_point ( input ):
 3 ...
 4
 5 """ Generated specifications """
 6 # Pre - conditions
 7 def preconditions ( input ):
 8 ...
 9
10 # Post - conditions
11 def postconditions ( input , output ):
12 ...
13
14   """ Generated casual inputs """
15   casual_inputs = [...]
16
17 """ Check inter - consistency """
18 def check () :
19      pass_result = []
20      for ci in casual_inputs :
21          try :
22                output = entry_point ( ci )
23                postconditions (ci , output )
24                pass_result . append ( True )
25          except Exception as e:
26                pass_result . append ( False )
27      return sum ( pass_result ) / len (
        pass_result )
28 global final_result
C     Discussion about Pass@k                                   For a the first category of methods, n̂ equals n
In this section, we discuss the flaws of Pass@k              since it treats each solution equally. As a result,
in Chen et al. (2021) and propose a variant for              our implementation of Pass@k is identical to the
evaluating methods involved selection and filtering.         original implementation in Chen et al. (2021).
   Chen et al. (2021) propose an unbiased estimator
called Pass@k, which estimates the probability of a          Pass@k of MPSC when k is large As shown in
model passing unit tests within k attempts. In spe-          Table 2, the performance of MPSC-Semantic and
cific, Chen et al. (2021) first samples a total of n         MPSC-Lexical remains largely unchanged as k in-
solutions with c of them are correct, randomly sam-          creases. This phenomenon aligns with the nature
ples k solutions for testing, and use the probability        of MPSC, which assesses solutions based on their
of passing tests for estimation,                             consistency, hence assigning similar scores to so-
                                     n−c
                                                            lutions with similar semantics. Consequently, all
                                      k
                 Pass@k = 1 −         n                      solutions will aggregate into many clusters depend-
                                      k                      ing on whether the assigned scores are identical,
   Although their implementation serves as an ef-            resulting in a lack of diversity within each clus-
fective measure of the code generation ability of            ter. Therefore, the pass rate of solutions selected
different foundation models (referred to as the first        by MPSC will remains constant even in more at-
category of methods in the following), it is not             tempts (i.e. varying k), if the number of attempts is
suitable to evaluate methods involving filtering or          still less than the top-ranked cluster size. A trivial
selection during the inference stage (Li et al., 2022;       method to address the problem is to increase the di-
Chen et al., 2022) (referred to as the second cate-          versity by adopting a round-robin selection from all
gory of methods in the following), as the n gener-           clusters, rather than selecting solutions according
ated solutions are identical.                                to scores from highest to lowest. The correspond-
   To address the limitation, we implement a vari-           ing results are presented in Table 8. We can see
ant of Pass@k. We assume each method provides                the performance of Pass@5 is improved compared
a score function over the n generated solutions,             with that of Table 2.
which provides a unified view for the two method
categories and hence enables a fair comparison.                  Method            Pass@1     Pass@2    Pass@5
The first category can be regarded as assigning                                   HumanEval
an identical score to each solution. Similar to                  GPT-3.5-Turbo      68.38       76.24   83.15
the original definition of Pass@k, we evaluate the               MPSC-Lexical       82.32       84.76   86.59
                                                                 MPSC-Semantic      83.35       86.08   89.75
method by testing the top-k solutions with the high-
est scores. As the score function may assign the                                 HumanEval+
same score to multiple solutions, the test result of             GPT-3.5-Turbo      58.75       66.58   73.96
the top-k is not deterministic but an expected value.            MPSC-Lexical       74.39        75.0   77.44
                                                                 MPSC-Semantic      73.08       77.89   83.20
   Mathematically, let’s assume that a method se-
                                                                                    MBPP
quentially arranges outputs into an ordered list
{s1 , ..., sn }, such that ∀i > j, si ⪯ sj accord-               GPT-3.5-Turbo      66.80       72.34   76.60
                                                                 MPSC-Lexical       68.38       70.26   71.43
ing to their scores. We define a set of solutions                MPSC-Semantic      73.24       74.46   78.01
Sk = {si |sk ⪯ si }, which represents the solution                               CodeContests
set selected by the method. Suppose the cardinalily
                                                                 GPT-3.5-Turbo       2.57        4.22    7.16
of Sk is n̂, the number of correct solutions within              MPSC-Lexical        5.45        5.45    6.06
Sk is ĉ. Noted that n̂ ≥ k, and thus we uniformly               MPSC-Semantic      10.07       10.18   11.39
sample k solutions {s′1 , ..., s′k } from Sk for estima-
tion,                                                        Table 8: Performance of MPSC evaluated by the Pass@k
                                                             metric in a round-robin way.
    Pass@k (Ours) = Es′1 ,...,s′k [1∪k    ′              ]
                                     i=1 si is correct

                     = Pr(∪ki=1 s′i is correct)
                     = 1 − Pr(∩ki=1 s′i is incorrect)
                            n̂−ĉ
                                  
                               k
                     =1−       n̂
                                 
                               k
          Method           Pass@1      Pass@2   Pass@5           Metric          Pass@1        Pass@2        Pass@5
                          HumanEval                                                HumanEval
      MPSC                  74.17      77.02    78.53     WizzardCoder-34B       66.04±1.27    70.95±0.84    75.51±0.43
        + 1 test case       85.37      86.59    85.13              +MPSC         76.32±1.82    76.50±1.20    75.93±0.68
        + 2 test cases      85.98      86.18    85.36
        + 5 test cases      88.41      89.23    88.69     WizzardCoder-13B       58.62±1.23    65.05±0.75    71.81±0.14
        + 10 test cases     89.02      90.24    88.81              +MPSC         74.96±0.96    75.51±0.44    75.33±0.57

                          HumanEval+                      WizzardCoder-7B        52.20±2.17    58.16±1.94    64.73±1.68
                                                                   +MPSC         65.09±1.83    65.54±1.38    66.51±0.83
      MPSC                  65.05      69.76    71.72
        + 1 test case       85.37      86.59    85.13                             HumanEval+
        + 2 test cases      85.98      86.18    85.36     WizzardCoder-34B       56.12±1.83    60.54±1.66    64.67±1.56
        + 5 test cases      88.41      89.23    88.69              +MPSC         65.21±0.20    64.85±1.10    64.74±1.36
        + 10 test cases     89.02      90.24    88.81
                                                          WizzardCoder-13B       49.42±0.59    54.91±0.77    60.81±0.83
                            MBPP                                   +MPSC         63.12±1.35    63.68±0.63    63.77±0.94
      MPSC                  69.34      70.06    71.85     WizzardCoder-7B        43.74±2.34    49.48±2.37    56.26±2.30
        + 1 test case       69.85      71.99    72.69              +MPSC         54.64±1.21    56.55±1.05    58.21±0.88
        + 2 test cases      70.78      72.46    73.04
        + 5 test cases      71.25      72.93    73.47
        + 10 test cases     71.72       73.4    73.27    Table 10: The average performance of MPSC with
                                                         three sample sets under different random seeds. We
Table 9: Performance of MPSC with different numbers      use MPSC-Semantic configuration in this experiment.
of golden test cases.

                                                         dataset 8 and present the results in Table 9. The
                                                         substantial performance enhancements achieved
C.1     Analysis of Other Perspectives                   with the inclusion of merely five golden test cases
                                                         underscore the feasibility of implementing MPSC
MPSC not only selects the optimal output from the
                                                         in user-interactive application scenarios.
target perspective but also chooses outputs from
auxiliary perspectives, thereby generating corre-        D.2    Time Overhead
sponding by-products. In the context of code gen-
                                                         The additional time overhead imposed by MPSC
eration, which is the primary focus of this paper,
                                                         mainly comes from inter-consistency measure-
MPSC can additionally identify more reliable test
                                                         ments and the iterative algorithm (Alg. 1). For the
cases and specifications. We evaluate the quality
                                                         former, we need to process a total of (200 × 50 +
of these by-products and present the results in Ta-
                                                         50 × 100 + 100 × 200) = 35000 edges with a time
ble 11. The experimental results demonstrate that
                                                         limit of 0.001 seconds per edge. In contrast, CodeT
MPSC is proficient in selecting high-quality out-
                                                         (Chen et al., 2022), the strongest baseline, requires
puts across all relevant perspectives.
                                                         to process a total of 200 × 500 = 100000 edges.
                                                         Moreover, this process can be fully parallelized.
D     More Analysis                                      For the latter, the iterative algorithm converges
                                                         rapidly, typically within an average of about 50
D.1     MPSC with User-provided Test Cases               rounds, requiring less than 0.1 second. Overall, the
In practical applications of code generation, users      time overhead of MPSC is acceptable in most code
often provide a limited number of test cases to out-     development scenarios, laying the groundwork for
line the desired functionality, thereby assisting the    real-world deployments.
model in generating code that aligns with the re-        D.3    Stability of MPSC
quirements. In Table 2, MPSC-Label has shown
remarkable performance. In this study, we investi-       We explore the stability of MPSC with respect to
gate the potential performance improvements of the       the sampling process. We conduct the sampling
method in such scenarios by incorporating various        process of WizardCoder with three random seeds
quantities of golden test cases. These golden test       and then assess the performance of MPSC on the
cases are generated and then validated using canon-      generated solutions. The average results are shown
ical solutions provided in the benchmarks. We con-           8
                                                               CodeContests doesn’t provide canonical solutions. There-
duct experiments on the HumanEval and MBPP               fore, we cannot conduct evaluation of test cases.
                          Benchmark                HumanEval                            MBPP
                           Metric       Pass@1       Pass@2     Pass@5       Pass@1     Pass@2      Pass@5
                                                                  Specification
                       GPT-3.5-Turbo      45.93       58.76     72.26         53.7       62.37       70.60
                          MPSC            73.58       73.59     74.38        71.86       71.38       73.40
                                                                     Test case
                       GPT-3.5-Turbo      63.83       80.71     93.23        34.64       44.32       53.19
                          MPSC            96.95       96.95     96.95        55.72       55.95       57.18

Table 11: The quality of specifications and test cases selected by MPSC. They can also be evaluated in Pass@k. We
use MPSC-Semantic configuration in this experiment.

               Benchmark                       HumanEval                                       HumanEval+
                 Metric          Pass@1           Pass@2        Pass@5           Pass@1          Pass@2        Pass@5
                             †
           WizzardCoder-34B      67.84            72.12         75.98            58.70           62.88         66.88
                     +CodeT      73.17+5.33       73.17+1.05    72.03-3.95       64.21+5.51      64.36+1.48    63.41-3.47
                     +MPSC       74.06+6.22       75.00+2.88    75.07-0.91       65.45+6.75      65.71+2.83    66.19-0.69
           Code Llama-34B        51.78            59.24         67.07            41.49           48.30         55.93
                     +CodeT      67.99+16.21      68.17+8.93    68.28+1.21       55.26+13.77     56.70+8.4     57.90+1.97
                     +MPSC       70.97+19.19      70.55+11.31   71.36+4.29       58.44+16.95     59.00+10.70   60.02+4.09
           WizzardCoder-13B      60.35            66.10         72.01            50.25           56.00         61.98
                     +CodeT      66.86+6.51       67.18+1.08    67.93-4.08       58.23+7.98      58.72+2.72    58.99-2.99
                     +MPSC       73.60+13.25      74.96+8.86    74.57+2.56       61.33+11.08     62.99+6.99    62.67+0.69
           Code Llama-13B        44.63            50.99         57.86            35.93           41.71         48.19
                     +CodeT      57.99+13.36      58.25+7.26    57.91+0.05       50.03+14.1      50.46+8.75    50.48+2.29
                     +MPSC       62.94+18.31      64.93+13.94   64.66+6.80       50.04+14.11     51.24+9.53    51.36+3.17
           WizzardCoder-7B       53.81            59.62         66.06            45.06           50.83         57.69
                     +CodeT      63.17+9.36       63.36+3.74    63.41-2.65       54.13+9.07      55.05+4.22    55.74-1.95
                     +MPSC       63.85+10.04      64.04+4.42    67.32+1.26       53.69+8.63      55.07+4.24    59.45+1.76
           Code Llama-7B         39.38            45.18         52.79            34.33           39.18         45.25
                     +CodeT      51.68+12.30      51.83+6.65    51.90-0.89       44.06+9.73      44.47+5.29    44.71-0.54
                     +MPSC       58.54+19.16      57.83+12.65   59.31+6.52       49.04+14.71     49.96+10.78   50.46+5.21

Table 12: The performance of MPSC-Semantic with different foundation models. † : We use nucleus sampling with
temperature as 0.2 instead of greedy generation in this experiment. The best performance is shown in bold.

in Table 10. It is evident that the improvement                  E       Experiment Settings and Baselines
brought by MPSC is very stable.
                                                                 We incorporate various baselines in code gen-
D.4   MPSC with Limited API Calls                                eration. First of all, we include many strong
                                                                 large language models like ChatGPT (gpt-3.5-
We here discuss another setting, where MPSC uti-                 turbo 0614 version), GPT-4 (gpt4-0614 version),
lizes 100 solutions, 50 specifications and 50 test               Code Llama-Instruct-34B, WizardCoder-Python-
cases, requiring identical API calls to the founda-              34B and DeepSeekCoder-7B-Instruct. The spe-
tion model baselines. The results shown in Table                 cific hyper-parameters for inference of ChatGPT
13 again prove the supreme performance of MPSC                   and GPT4 are shown in Table 14. MPSC requires
over baselines under fair comparison.                            an additional hyper-parameter α, which controls
                                                                 the balance between inter-consistency and intra-
D.5 Comparison on Other Foundation Models                        consistency in the algorithm. Given that the quality
Table 3 demonstrates the generalization of MPSC                  of inter-consistency significantly depends on the
on other foundation models. We also conduct an                   edge density of the graph, we utilize the mean edge
experiment to compare MPSC with CodeT, the                       weight to determine the value of α. Empirically,
strongest baseline, under this setting. The results              we assign a relatively small value of α (0.01) when
are presented in Table 12.                                       the edges are sparse on the graph, indicated by the
    Benchmark               HumanEval                     HumanEval+                    MBPP                       CodeContest
      Metric       Pass@1    Pass@2     Pass@5   Pass@1     Pass@2   Pass@5    Pass@1   Pass@2   Pass@5   Pass@1     Pass@2      Pass@5
   GPT-3.5-Turbo   68.38      76.24     83.15     58.75     66.58      73.96   66.80    72.34    76.60     2.57        4.22       7.16
      GPT-4        81.48      86.31     90.46     70.52     75.48      79.54   71.26    74.27    76.99     6.1        8.28       11.72
      MPSC          81.5       83.7     91.05     72.18      75.2      81.22   72.78    74.24    78.25    10.77       12.64      13.84


           Table 13: The performance of MPSC with 100 solutions, 50 specifications and 50 test cases


mean edge weight less than 0.16. Other, we as-                          oracle programs until they pass all public example
sign a large value of α (0.95) otherwise to better                      test cases, whose complexity is unlimited.
leverage inter-consistency.

                  Temperature              0.8
                     Top P                 0.95
               Frequency Penalty            0
                Presence Penalty            0

 Table 14: The Inference hyper-parameters of LLMs.

   We also include several baselines like Self-
Consistency MBR- EXEC, CodeT and Self-
collaboration, which enhance the inference capa-
bility of LLMs in a post-hoc manner.
  • CodeT: This baseline first uses generated test
    cases to verify each solution by code execution.
    Then it utilizes RANSAC algorithm to create
    consensus sets based on execution results. The
    size of consensus set is then used to rank so-
    lutions. We generate 500 test cases for CodeT
    following the original implementation in Chen
    et al. (2022).
 • Self-Consistency: We implement this baseline
   following Chen et al. (2022). If two solution
   pass the same set of generated test cases and
   specifications, we regard them “consistent”.
   Then we take a majority voting to rank solu-
   tions following Wang et al. (2022).
  • MBR- EXEC: This baseline ranks solutions by
    minimum Bayes risk decoding based on the ex-
    ecution results in the 500 generated test cases.
   For a fair comparison between our proposed
MPSC and these baselines, we employ the same
solutions generated by ChatGPT for them to rerank.
In specific, we sample 200 solutions following the
conventional setting. Since some methods leverage
generated test cases and specifications as well, we
use the same set of test cases and specifications
generated by ChatGPT for both MPSC and these
baselines.
   We don’t include ALGO (Zhang et al., 2023)
as baseline, because it requires to keep generating
F    Prompt for MPSC                                    Prompt for Generating Test Cases

    Prompt for Generating Specifications                ```Python
                                                        # Given a docstring, continue to write the
    I want you to act as a python programmer.           following code with 10 valid assertion
    Given a docstring about a python method,            statements to check the correctness of the
    you need to write its pre-conditions in one         function. Provide diverse test cases.
    test function “def preconditions(input)"            {Docstrings}
    and post-conditions in another test function        pass
    “def postconditions(input, output):". You
    should ensure invalid input or output of            # check the correctness of with 10
    the method will raise error in the two test         different valid assertion statements in the
    functions.                                          form of “assert {entry point}(...) == ..."
                                                        assert
    ```Python
    {Demonstration Docstrings 1}
    pass
    #Pre-conditions
                                                    G    Case Study
    {Demonstration Preconditions 1}
    #Post-conditions                                We present some cases from HumanEval, MBPP,
    {Demonstration Postconditions 1}                CodeContests in the following pages.
    ```


    ```Python
    {Demonstration Docstrings 2}
    pass
    #Pre-conditions
    {Demonstration Preconditions 2}
    #Post-conditions
    {Demonstration Postconditions 2}
    ```


    ```Python
    {Docstrings}
    pass




    Prompt for Generating Solutions

    I want you to act like a Python programmer.
    I will give you the declaration of a function
    and comments about its property. You need
    to implement the body of the function in
    the code block. Do not modify any code I
    provide. Do not provide any explanations.

    Here is the question.
    ```Python
    {Docstrings}
    ```
 1 """ User Intent """
 2 def get_row ( lst , x):
 3      """
 4      You are given a 2 dimensional data , as a nested lists ,
 5      which is similar to matrix , however , unlike matrices ,
 6      each row may contain a different number of columns .
 7      Given lst , and integer x , find integers x in the list ,
 8      and return list of tuples , [( x1 , y1 ) , (x2 , y2 ) ...] such that
 9      each tuple is a coordinate - ( row , columns ) , starting with 0.
10      Sort coordinates initially by rows in ascending order .
11      Also , sort coordinates of the row by columns in descending order .
12
13     Examples :
14     get_row ([
15        [1 ,2 ,3 ,4 ,5 ,6] ,
16        [1 ,2 ,3 ,4 ,1 ,6] ,
17        [1 ,2 ,3 ,4 ,5 ,1]
18     ] , 1) == [(0 , 0) , (1 , 4) , (1 , 0) , (2 , 5) , (2 , 0) ]
19     get_row ([] , 1) == []
20     get_row ([[] , [1] , [1 , 2, 3]] , 3) == [(2 , 2) ]
21     """
22
23
24 """ Solution selected by MPSC """
25 def get_row ( lst , x):
26      result = []
27      for row_index , row in enumerate ( lst ):
28          for col_index , val in reversed ( list ( enumerate ( row ))):
29                if val == x:
30                      result . append (( row_index , col_index ))
31      result . sort ( key = lambda x: x [0])
32      return result
33
34
35 """ Solution selected by CodeT """
36 def get_row ( lst , x):
37      result = []
38      for i , row in enumerate ( lst ):
39          if x in row :
40               for j , val in sorted ( enumerate ( row ) , key = lambda x: -x [1]) :
41                    if val == x:
42                         result . append ((i , j))
43      return result
                                     Listing 4: Cases from HumanEval.
 1 """ User Intent """
 2 def count_first_elements ( test_tup ):
 3      '''
 4      Write a function to find the number of elements that occurs before the tuple
        element in the given tuple .
 5      '''
 6
 7
 8 """ Solution selected by MPSC """
 9 def count_first_elements ( test_tup ):
10      count = 0
11      for i in range ( len ( test_tup )):
12          if isinstance ( test_tup [i], tuple ):
13              break
14          count += 1
15      return count
16
17
18 """ Solution selected by CodeT """
19 def count_first_elements ( test_tup ):
20      count = 0
21      for i in range ( len ( test_tup )):
22          if test_tup [i] == test_tup [0]:
23              break
24          count += 1
25      return count
                                     Listing 5: Cases from MBPP.
 1 """ User Intent """
 2 def solution ( inputs : str ) -> str :
 3      '''
 4      You are given an array a of length n.
 5      Let 's define the eversion operation . Let x = a_n . Then array a is partitioned
        into two parts : left and right . The left part contains the elements of a that
        are not greater than x ( <= x). The right part contains the elements of a that
        are strictly greater than x (> x). The order of elements in each part is kept
        the same as before the operation , i. e. the partition is stable . Then the array
        is replaced with the concatenation of the left and the right parts .
 6      For example , if the array a is [2 , 4, 1, 5, 3] , the eversion goes like this : [2 ,
         4 , 1 , 5, 3] -> [2 , 1, 3] , [4 , 5] -> [2 , 1, 3, 4, 5].
 7      We start with the array a and perform eversions on this array . We can prove that
         after several eversions the array a stops changing . Output the minimum number k
         such that the array stops changing after k eversions .
 8
 9     Input :
10     Each test contains multiple test cases . The first line contains the number of
       test cases t (1 <= t <= 100) . Description of the test cases follows .
11     The first line contains a single integer n (1 <= n <= 2 * 10^5) .
12     The second line contains n integers a_1 , a_2 , ... , a_n (1 <= a_i <= 10^9) .
13     It is guaranteed that the sum of n over all test cases does not exceed 2 * 10^5.
14
15      Output :
16      For each test case print a single integer k - the number of eversions after
        which the array stops changing .
17      Example
18      assert solution ( '3\ n5 \ n2 4 1 5 3\ n5 \ n5 3 2 4 1\ n4 \ n1 1 1 1 ') == '1\ n2 \ n0 '
19      '''
20 """ Solution selected by MPSC """
21 def solution ( inputs : str ) -> str :
22      def eversion (a):
23          n = len (a)
24          l , r = [] , []
25          x = a [ -1]
26          for i in range (n - 1) :
27               if a[i] <= x:
28                    l. append (a[i ])
29               else :
30                    r. append (a[i ])
31          return l + [x] + r
32
33     def is_same (a , b):
34         return len (a) == len (b) and all ( ai == bi for ai , bi in zip (a , b))
35
36     res = []
37     inputs = inputs . strip () . split ( '\n ')
38     t = int ( inputs [0])
39     idx = 1
40     for _ in range (t):
41         n = int ( inputs [ idx ])
42         a = list ( map ( int , inputs [ idx +1]. split () ))
43         idx += 2
44         cnt = 0
45         while True :
46               new_a = eversion (a)
47               cnt += 1
48               if is_same (a , new_a ) :
49                   break
50               a = new_a
51         res . append ( str ( cnt - 1) )
52     return '\n '. join ( res )
53 """ Solution selected by CodeT """
54 def solution ( inputs : str ) -> str :
55      # split the input into list of test cases
56      test_cases = inputs . strip () . split ( '\n ') [1:]
57      result = []
58
59     # loop through each test case
60     for i in range (0 , len ( test_cases ) , 2) :
61         n = int ( test_cases [i ])
62         a = list ( map ( int , test_cases [i +1]. split () ))
63         k = 0
64
65          # perform eversion operation until array stops changing
66          while True :
67              x = a [ -1]
68              left , right = [] , []
69              for j in range (n -1) :
70                   if a[j] <= x:
71                        left . append (a[j ])
72                   else :
73                        right . append (a[j ])
74              new_a = left + [x] + right
75              if new_a == a:
76                   break
77              a = new_a
78              k += 1
79
80          result . append ( str (k))
81
82     # join the results and return
83     return '\n '. join ( result )
                                     Listing 6: Cases from CodeContests.
