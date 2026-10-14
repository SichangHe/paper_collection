                                                             Verbalized Algorithms:
                                                 Classical Algorithms are All You Need (Mostly)


                                                  Supriya Lall                   Christian Farrell                   Hari Pathanjaly
                                                  MIT CSAIL                      Marist University                      UC Irvine
                                             MIT-IBM Watson AI Lab              IBM Infrastructure                  IBM Infrastructure
                                               supriya@mit.edu             christian.farrell@ibm.com            hari.pathanjaly@ibm.com
arXiv:2509.08150v6 [cs.CL] 22 May 2026




                                                   Marko Pavic                   Sarvesh Chezhian                 Masataro Asai
                                                  Marist University              IBM Infrastructure           MIT-IBM Watson AI Lab
                                                 IBM Infrastructure               schez@ibm.com            IBM Research Cambridge, USA
                                               marko.pavic@ibm.com                                           masataro.asai@ibm.com



                                                                                         Abstract
                                                     Reasoning is a fundamentally algorithmic task. Yet current work on LLM-based
                                                     reasoning relies on free-form generation whose theoretical guarantees (soundness,
                                                     completeness, complexity, optimality) remain poorly understood. We argue that
                                                     we should not treat them as general-purpose reasoners, and as an alternative, we
                                                     propose a paradigm we call verbalized algorithms (VAs), which combines LLMs
                                                     and various algorithms with established guarantees. Instead of betting on LLM’s
                                                     ability to solve a reasoning task, VAs limit their scope by decomposing the task
                                                     down to simple elementary operations on strings that they can answer reliably. For
                                                     example, sorting a list of natural language strings could be done by using an LLM as
                                                     a binary comparison oracle in a parallel or approximate sorting algorithm. We push
                                                     the accuracy-runtime Pareto front with verbalized maximum, sorting, clustering,
                                                     and submodular maximization, for numerical reasoning, topic clustering, Wi-Fi
                                                     access point optimization, and multi-hop Q&A RAG task. These results suggest
                                                     improving LLM-based reasoning through standard algorithmic analysis is a feasible
                                                     and better grounded research direction.


                                         1     Introduction
                                         Imagine receiving thousands of customer complaints and having to quickly sort them by how urgently
                                         they need support. Feeding such a large set of input strings blindly into a transformer-based large
                                         language model (LLM) is ineffective and impractical due to various limitations. Examples of such
                                         limitations include limited context lengths from hardware limitation (GPU memory limit from O(n2 )
                                         attentions), sequential runtime for processing a long input, deteriorating accuracy from the longer
                                         context, and its limited ability to perform the sorting task itself. LLMs provide no guarantees on the
                                         correctness of their outputs for computational reasoning tasks, including but not limited to sorting,
                                         beyond anecdotal, empirical observations that they sometimes do. Despite recent improvements in
                                         Chain-of-Thoughts [Wei et al., 2022] and think tags [Guo et al., 2025], their behavior is fundamentally
                                         an approximation of formal reasoning, and thus contains hallucinations.
                                         We argue that most reasoning tasks are informal representations of formal tasks for which an efficient
                                         and well-analyzed classical algorithm already exists in the literature, thus training a model hoping
                                         that it may learn to solve it by itself is often a reinvention of the wheel. For example, for sequential
                                         comparison sort, O(n log n) algorithms are asymptotically optimal, thus no algorithm can improve
                                         over it anyways — then why don’t we just use them?

                                         Preprint.
           Free-Form Reasoning                                Formalization-based Reasoning
                                                                                                               Translation Barrier:
              Task      Weak models             Task                                                           Weak models fail at
                        tend to return                              Language Expressivity:                     precise translation
                     nonsensical answers                            The target language
                                                                    may not be expressive                            ba-bu, wah !
                       ba-bu, wah !              translate          enough for the task

                       Even a strong model             Delegate reasoning to symbolic solvers                   Lack of Integration:
                         can't guarantee                                                                          LLM is excluded
                       the correct answer
                                                        PDDL          SMT           ASP           Prover9         from reasoning
                        ἔοικα γοῦν τούτου γε
                        σμικρῷ τινι αὐτῷ
                                                                                                                          Answer: ...
                        τούτῳ σοφώτερος
                                                                                                                          but it doesn't
                        εἶναι, ὅτι ἃ μὴ οἶδα
                                                                                                                          sound right!
                        οὐδὲ οἴομαι εἰδέναι                                Answer               translate



              LLM-modulo-theory                                              Verbalized Algorithms
    Task                 Give me more booze!                   Task                Known Algorithm                      Answer
                                                                           def fn (...)     constrained
                                                                                             decoding
                                  Invalid answer!                            if x > y:                      yes/no     Predictable
                                                              Route to         fn( left ) # recurse
                                  What an idiot...             known           fn( right ) # recurse
                                                                                                                       ・correctness
                                                             algorithms      if x = y:                      yes/no     ・runtime
                                    Symbolic
Task
                                    Verifiers
                                                                               ...                                     ・quality
requirement                                                                  if |y-x|>|z-x|:                yes/no
                                                                               ...
  Eventually returns a correct answer but                                 Weak / strong models can
  ・Language expressivity                                                   answer simple questions
  ・How long does it take? (✗ runtime)                                     LLM is integrated in
                                                                          algorithmic reasoning
  ・How good is the answer? (✗ optimality)


                     Figure 1: Conceptual comparison of various reasoning approaches


In addition to hardware limitations and long context issues, LLM reasoning usually does not follow a
formally specified algorithm. Even if it does, the algorithm may be unsound, incomplete, and lack
formal guarantees on time/space/optimality. Even if we discount these issues, autoregressive LLMs
fundamentally operate sequentially. One could parallelize token generations (e.g., beam search or
MCTS), but such task-agnostic parallelization lacks sophisticated coordinations in dedicated parallel
algorithms that exploit task characteristics.
Traditional disciplines of computer science instead approach computational tasks with task decompo-
sition. For example, a merge sort decomposes a sorting task into smaller sorting tasks and combines
the results, where, at the limit, there is an elementary binary comparison over individual pairs. These
traditional algorithms, given an accurate oracle, guarantee the correctness of their outputs and the
average/worst-case runtime/memory. The opaqueness of LLM’s reasoning prevents such an analysis.
In this work, we propose an abstract framework called “verbalized algorithms”. Given an informal
representation of a formal task, a verbalized algorithm replaces some atomic operations in a classical
algorithm with LLM-driven text-based oracles while retaining the high-level control flow, thereby
largely retaining the theoretical guarantees. Our work is heavily influenced by Algorithm with
Predictions [Mitzenmacher and Vassilvitskii, 2022, ALPS] literature, which achieved significant
progress in augmenting algorithms with data-driven oracles. There are certainly other work that
replaces part of algorithms with LLM oracles, including successor function and goal condition in
planning [Katz et al., 2024] and collision checking in STPR [Djuhera et al., 2025], yet we believe
ours is the first general proposal for the reductionist approach toward LLM reasoning.
We perform four case studies with increasing difficulty and non-triviality: Maximum, sorting, cluster-
ing, and submodular maximization. Our implementations are built on top of the offline asynchronous
engine of SGLang [Zheng et al., 2024], and all experiments are repeated 5 times with different seeds.
Contributions. VAs have several key advantages: (1) It is more accurate than classical non-LLM
methods or more recent embedding-based or other LLM-based methods, and is also scalable with
data parallelism. (2) The reasoning trace of VAs is interpretable, as we have a full understanding of


                                                                2
its high-level algorithm and can focus on individual decision points. (3) VAs provide some degrees of
theoretical guarantees. The key point is not these guarantees themselves but the fact that they transfer
directly from the existing literature even though we are using LLMs, which massively helps reducing
the chance of reinventing the wheels. (4) VAs work well with smaller, efficient reasoning models.
(5) VAs are more accessible than some non-VA methods which require model training, and helps AI
democratization. Such training is typically beyond the reach of casual LLMs users, while VAs do not
require additional training. Fine-tuning a model for VA is possible, and is a promising future work.
Limitations. The main limitation of VAs is the resource intensity from the large constant factor
involved in each query. This, however, is not a real limitation in the long term, as the progress in
silicon manufacturing makes more powerful GPUs cheaper. Moreover, VAs are designed to tackle
more difficult tasks, potentially combinatorial ones, that naturally require more precision and a more
careful algorithmic procedure to address compounding errors. Lastly, VAs’ accuracy-runtime Pareto
front is on par or better than with existing approaches by using a smaller model, as seen later.
Another limitation is the cost of writing each algorithm by hand. However, coding agents significantly
lowered the bar recently, as they often know even the most sophisticated algorithms in the literature.
Agentic workflows involving subagents writing their own VAs would accelerate this direction.
Alternative Views. Another set of approach to similar tasks is what we call “formalization-based
approaches”. Leveraging the translation capability of LLMs, it converts an informal task representation
into a formal, symbolic representation, solves it with a specialized combinatorial solver, and then
converts the solution back to the informal, natural language representation. Existing work on this
approach includes LLM-based generation of PDDL [McDermott, 2000] for classical planning [Xie,
2020, Guan et al., 2023, Li et al., 2024, Fine-Morris et al., 2024, Oswald et al., 2024], Prover9 theorem
proving input [Olausson et al., 2023], or SMT input [Hao et al., 2024]. The issue with this approach
is twofold: First, it requires grammar-following capability for a complex target formal language.
This could be error-prone and time-consuming, and/or the grammar class (context free/sensitive)
of the target language could exceed the scope of constraint-decoding libraries [Dong et al., 2025].
Second, the target language limits the scope of the tasks that can be solved. For example, an agent
that converts the task into PDDL cannot handle a probabilistic, temporal, or partially-observable task.
VAs, on the other hand, could handle them robustly by applying informal common sense reasoning to
atomic operations. We see the evidence of this claim in the sorting section.
LLM-Modulo framework [Kambhampati et al., 2024] views an LLM as an “idea generator” and
combines it with rejection sampling / feedback loop with symbolic verifiers to improve the accuracy
of LLM-based reasoning, particularly in planning tasks. While it shares the concerns about the
soundness of LLM-based reasoning with VAs, it has three key issues. First, in the general LLM-based
natural language reasoning, there is no guarantee that such a verifier would exist because the target
application could be highly informal (e.g., related to human emotion and ethics), which makes it
challenging to formally / objectively / symbolically define any correctness. VAs do not have this issue
– when the algorithm contains halting/backtracking with a verifier, the verifier could be replaced by
LLM-based oracles to accommodate informal tasks. Second, it focuses on decision problems and
there is little considerations for optimization problems. Algorithms for optimization generally rely on
ranking/comparison (discussed extensively in this paper) and datastructures around it (e.g., priority
queues). Third, due its reliance on symbolic verifiers, it is also limited by the expressivity of the target
language, even if the verifier exists and the translation to the language is possible.
Another view may criticize that each VA is specialized to some task and does not offer “general
intelligence”. However, it can be largely resolved by tool-use agents [Schick et al., 2023] which are
already widely adopted by the industry. The agent can act as a router to VA implementations.


2    Verbalized Algorithms

While whether LLMs can reason or not is up for both philosophical and technical debates [Shojaee
et al., 2025, Hazra et al., 2024], it is more widely accepted that they can solve some much simpler
tasks such as multi-choice question answering with high fidelity. From this observation, we propose
verbalized algorithms (VAs), a reasoning strategy that limits the scope of LLMs to simple tasks.
To exhibit a trait typically useful for user interaction (e.g. instruction following), LLMs go through a
series of parameter-efficient fine-tuning (PEFT) steps after pretraining on a large corpus. For example,


                                                     3
in Direct Preference Optimization [Rafailov et al., 2023, DPO], the input is a pair of model outputs
in which human users have indicated their preference over another and the model is fine-tuned to
follow that preference. For a prompt x and an answer pair y1 and y2 , denote by y1 ≻ y2 |x that y1 is
preferred over y2 . DPO learns a Bradley-Terry reward model [Bradley and Terry, 1952, BT-model]
for this preference, i.e., p(y1 ≻ y2 |x). The Plackett-Luce reward model [Plackett, 1975, Luce, 1959,
PL-model] extends BT to a multinomial case that represents a ranking over choices. Our insight in
VAs is that general BT (and PL) reward models baked into the LLM are sufficient to perform simple
tasks. Assuming those capabilities and thus relying entirely on the accuracy of the reward models:
Definition 1 ((n, 2)-Verbalized Algorithms). Let T [τ ] be a computational task (e.g., sorting) over
objects of type τ and let A[τ ] be an algorithm that solves T [τ ] with an n-arg boolean oracle
f [τ ] : τ, · · ·, τ → {⊤, ⊥}. A Verbalized Algorithm instantiates A[τ ] with τ = str by implementing
f [str] as a query to an LLM whose output is constrained to {“yes”, “no”} which maps to {⊤, ⊥}.

VAs keep the high-level control flow of A[τ ] intact, while only replacing the oracle f [τ ] with an
LLM-based f [str]. This preserves the theoretical properties of the classical algorithm A[τ ] if the
model’s reward model matches the ground truth. VAs can also leverage other existing algorithmic
paradigms, such as concurrent algorithms. While the definition above focuses on the BT reward
model, VAs naturally extend to PL reward models as (n, k)-VAs (defined in the appendix, used in
submodular maximization section). If the reward model is inaccurate, a non-classical robust algorithm
that assumes noisy oracles could bound the error rate of the output using known theoretical results. A
deeper investigation into the theoretical error rates is left for future work.
Symmetrization: In certain tasks, we further improve the oracles in VAs via symmetrization, which
mitigates two biases in the model: (1) Positional bias [Liu et al., 2024], which is the bias derived
from the ordering in the input context (e.g., always assigning a higher logit to the first choice in MCQ
tasks), and (2) sycophancy [Casper et al.], which is the bias toward certain answers, such as “yes”.
For asymmetric oracles f (x1 , x2 ) in (n, 2)-VAs, such as (2, 2)-comparison oracles for sorting, let
p12 and p21 be next-token probabilities for answering “yes” with the original prompt and a prompt
whose x1 and x2 are swapped. Due to asymmetricity, ideally f (x1 , x2 ) = ¬f (x2 , x1 ) holds, but in
fact p12 ̸= 1 − p21 due to the bias. Symmetrized (n, 2)-VAs use ( p12 +(1−p
                                                                         2
                                                                            21 ) (1−p12 )+p21
                                                                                ,     2       ) as the
final probability for “yes”, “no”. Symmetrization for (n, k)-VA is discussed in the appendix.

3   Verbalized Maximum
We first establish our claim that even the recent sophisticated models often fail at simple algorithmic
tasks. As an example task, we first investigate their ability to find the maximum in a list X of n
randomly selected integers between 1 and 10000. Due to the lack of principled algorithm for the
LLM to follow, a naive LLM often fails even at this simple task despite with the help of constrained
decoding, especially when the list gets longer.
We compare two approaches: Constraint decoding baseline queries LLMs with a string “What is
the largest number in [comma-separated numbers in X]?”. We use constraint decoding [Willard and
Louf, 2023] to limit the space of possible outputs to one of the elements in X. Verbalized “Native”
maximum overrides Python’s built-in gt operator with an LLM call and applies the built-in max
function, which sequentially reduces the list with O(n) comparisons. Each binary comparison for
x1 , x2 ∈ X is replaced by a yes-no style LLM query “Is X larger than Y? X: x1 Y: x2 ”, where the
next output token is restricted to “yes” and “no” with constrained decoding. The model output is
mapped to ⊤/⊥ if the sampled output is “yes” / “no”, respectively. Finally, Verbalized parallel
elimination tournament performs ⌈log2 n⌉ = O(log n) steps of parallel pairwise comparisons,
where each step eliminates half of the elements [Karp, 1988]. As each match in the tournament
eliminates 1 element, it performs n − 1 comparisons in total.
We evaluated the algorithms above across 20 randomly sampled lists for each of n ∈ {100, 1000}
with various-sized Qwen3 models (1.7B, 4B, 32B) with and without thinking [Team, 2025]. We
measured the rank error, i.e., where the returned output ranked in the sorted list of n numbers instead
of being the first. Fig. 2 shows the average of 5 runs. The error bars show the minimum/maximum
instead of mean ± std because the mean − std can become negative and invalidate logarithmic plots.
The same error bar scheme is used throughout this paper. In column 1 (n = 100), the baseline with a
small 1.7B model struggles to report accurate results despite the small input size. Thinking did not


                                                   4
                           n=100                                                n=1000                                         n=1000, tournament-detail                                    n=1000, tournament-dp
        102                                                                                                                                                                 3 × 100
                base              native, think                 104     base            native, think             2.2 × 100        sym           think, sym                                     dp:1       think, dp:1
                base, think       tourn.                                base, think     tourn.                      2 × 100        think                                                        dp:2       think, dp:2
                native
               1.7
                                  tourn., think                 103     native          tourn.,
                                                                                         1.7 1.7
                                                                                                 think            1.8 × 100
                                                                                                                                                                            2 × 100             dp:4       think, dp:4
                                                                                                                  1.6 × 100

 rank




                                                         rank




                                                                                                           rank




                                                                                                                                                                     rank
        101                                                     102                                                                                   1.7
                                                                                                      32          1.4 × 100                                                                         1.7    1.71.7
                              1.7        32
                                                                101                         4     4               1.2 × 100
                               4 1.7                                                                                            1.7 4
                    1.7        1.7                                                              1.7                           4                        1.7                            44 1.7  1.7
        100    44
              better    32
                         1.7 4 32
                        32           4    32         4                1.7
                                                                100 4better   32         1.7
                                                                                      1.7 4 4     32                   100       1.7 32
                                                                                                                               better            32          4   4             100      1.743232
                                                                                                                                                                                       better       32        4
                                                                                                                                                                                                               4    4     32
                   100           101           102                             101               102                                       101                                                       101                102



Figure 2: The speed-accuracy Pareto front (log x-axis: the runtime per query, log y-axis: rank
error) of maximum task with various model sizes (1.7B, 4B, 32B). The numbers near each point
indicate the model size. (column 1,2) Constraint decoding baseline vs. native maximum vs.
tournament maximum with n = 100, 1000. (column 3) Comparing various configurations of
tournament on n = 1000. Thinking significantly increases the runtime while it can increase the
error. Symmetrization increases the runtime to a lesser degree and reduces the error. (column 4) The
multi-GPU data parallelism (DP) on tournament on n = 1000.


resolve the issue, and even increased the error for the larger 4B and 32B models. Verbalized “Native”
maximum maintains a small, often zero error. Native+thinking worsened the error with an increased
runtime, making the largest 32B model too slow to finish 20 queries within the 1 hour time limit (≈ 3
minutes per query on average). The trend worsened in the n = 1000 experiments (Fig. 2, col 2). Now
thinking has little effect on the baseline and Native+thinking timed out with the 4B model. The only
configuration that solved n = 1000 reliably is the tournament maximum, which was several orders of
magnitude faster yet maintained near-zero errors. Thinking helped little on the tournament either.
We further studied various configurations of tournament maximum. Fig. 2 (mid) compares the effect
of thinking and symmetrization on the runtime. Thinking increased the runtime almost x10 fold. In
contrast, symmetrization multiplied the runtime by two, yet reduced the error in 1.7B. Further, Fig. 2
(right) shows that data parallelism with dp ∈ {2, 4} GPUs scales linearly.


4             Verbalized Sorting

Verbalized Sorting sorts a list of natural language strings X using LLM’s question answering capability
as an atomic comparison oracle. We evaluated the accuracy-speed tradeoff of several approaches.
LLM-based sorting is highly relevant to information retrieval (IR), and the methods discussed below
overlap with its existing work. However, IR is not the representative of the general sorting task
because of the large mismatch between their goals. IR often targets top-k retrieval and benchmark
metrics such as Normalized Discounted Cumulative Gain [Järvelin and Kekäläinen, 2002, NDCG]
rather than the ability to sort the entire list, including the bottom of the list, accurately. Standard
IR datasets, such as TREC / BeIR, contain binary / coarsely graded biased ranking (majority of
documents are irrelevant to the query) where the ranking among irrelevant documents are discounted.
While some papers [Qin et al., 2024] mention the time complexity of running pairwise comparisons,
evaluations predominantly focus on the accuracy and the total query cost, and they do not analyze
complexity-theoretic parallel runtime or the theoretical error rate from using noisy oracles in depth.
Among 5 recent papers [Qin et al., 2024, Sun et al., 2023, Sachan et al., 2022, Ma et al., 2023, Chao
et al., 2024], only one table discusses the sequential runtime [Chao et al., 2024, Table 4].
Baseline encodes the list X in a markdown format and asks the model to return a sorted list using
constrained-decoding to constrain the output to be a list whose elements are guaranteed to be indices
in the list. The approach corresponds to listwise ranking approach [Ma et al., 2023] in the RAG
literature. Due to the lack of a computationally efficient way to enforce the sorting invariances, i.e.,
that the output (1) is free of duplicates and (2) represents the same set of strings as the input, we
remove the duplicates and append missing elements to the end of the list. To address the invariance
violations, we also tested autoregressive (AR) baseline which decodes the sorted elements one by
one, with each step constrained to the remaining elements. This approach is significantly slower due
to the high cost of generating a new logit processor for constraining each output.
Scoring-based approaches ask the model to assign a score between 1.0 and 5.0 (down to one
decimal) to each sentence using regex-constrained decoding, then sort the sentences using the scores.
Its runtime is dominated by its O(n) scoring phase. It is a form of formalization-based approach (the


                                                                                                           5
                                      Amazon Reviews                                                                       Yelp Reviews                                                                      Amazon Reviews, kwicksort-detailed
                     better                                                                                better                                                                               1.5    better
              0.6           base                    kwick, :16, sym                                  0.6
                                                                                                                  base              kwick, :16, sym                                                            :4
                                                                                                                                                                                                               :4, think
                                                                                                                                                                                                                                 :16
                                                                                                                                                                                                                                 :16, think
                            AR base                 scoring                                                       AR base           scoring                                                     1.0            :4, sym           :16, sym
                            bitonic, sym            AR scoring 32                                                 bitonic, sym      AR scoring                                                                 :4, sym, think    :16, sym, think




                                                                                                                                                                                  kendall_tau
kendall_tau




                                                                                       kendall_tau
              0.4                                                                                    0.4                                    4                32                                                                                        432
                                                                                                                                                       32                                       0.5                                        1.7 1.7
                                               4          4         32                                                       4 32                                                                                                                  4 32 44
                                                                                                                                                                                                                                                  32
                                                                                                                                                                                                                  4 4                    32 1.732 1.7 32
              0.2                                  32                                                0.2      4                                                                                                                     32      32
                                                                                                                                                                                                0.0 1.71.7          1.7 1.7
                      1.7                                                                                             1.7        1.7              32                                                                4 4
                                                               32
              0.0            4    1.7 1.7 44
                                    1.7                 1.7   32         1.7324                      0.0    1.7       1.7 1.7 44                32           1.7324                                                  101                           102
                            100                    101                   102                                  100                101                         102
                                                                                                                                                                                                             Amazon Reviews, kwicksort-dp
                                                                                                                                                                                         1.0          better
                              Cities sorted 32
                                            by 32
                                               population                                                      Stanford Sentiment Treebank                                                                        dp:1 think, dp:1
                       better                                                                              better                    3232                                                0.8                      dp:2 think, dp:2
               0.4                                                                              0.6                                                                                                               dp:4 think, dp:4
                                  4     4




                                                                                                                                                                           kendall_tau
                                                                                                                                                                                         0.6
kendall_tau




                                                                                  kendall_tau
                                                                                                0.4                  1.74 32 4 1.7
                                                                                                                                                                                                                                           1.7 1.71.7 4
               0.2                                                                                                                                                                       0.4                                   32        32 3232 44
                                                                                                0.2                                                                                                    4
                                     32 1.7 1.7   32                                                                                 32
                                                                                                                                                                                                                 4 4                                 32
                                                                                                                                                                                         0.2
               0.0           1.74 1.71.74 4     32                   4 32
                                                                    1.7                         0.0          1.7 4 1.7 1.7 44      32                       1.7
                                                                                                                                                             32 4                                     1.7
                                                                                                                                                                                         0.0           1.7 1.7                                    32
                                   100           101                   102                                      10 0          10 1                           102                                                    101                          102



Figure 3: The speed-accuracy Pareto front (log x-axis: the runtime per query, y-axis: Kendall-tau
score) of sorting tasks. (left) Comparing methods. kwicksort achieved the best Pareto front. (right)
Comparing various configurations of kwicksort on amazon reviews.


list of scores represents the formal problem). We tested two variants: I.i.d Scoring scores xi ∈ X
independently, and autoregressive (AR) scoring scores all strings in a single query, allowing the
model to see the scores of other elements. The approach corresponds to pointwise ranking approach
[Sun et al., 2023, Sachan et al., 2022] in the RAG literature.
Verbalized sorting approaches correspond to pairwise ranking approaches [Qin et al., 2024] in
the RAG literature, but our contribution focuses on leveraging the theoretical properties of classical
algorithms, which has been undermined in the literature. These approaches use the same binary com-
parison oracle used by verbalized maximum. VA Bitonic uses the Bitonic sorting network [Batcher,
1968] from parallel sorting literature, which performs O(n(log n)2 ) comparisons in O((log n)2 )
time due to parallelism. VA KwickSort [Ailon et al., 2008] is an approximate parallel sorting algo-
rithm. It is analyzed on a more general FAS-Tournament task, which permits transitivity violations
(a ≤ b ∧ b ≤ c ̸⇒ a ≤ c) in LLM-based oracles, and bounds the expected number of deordered pairs
((. . . , j, . . . , i, . . .) for i < j) at most three times the optimal. Operationally, kwicksort works identi-
cally to quicksort. It runs O(n log n) comparisons in O(log n) expected parallel runtime because the
input size halves in each recursion in expectation. To address runtime/accuracy tradeoff, we added
early-stopping to the recursion which returns the input X immediately if |X| ≤ θ ∈ {4, 16}.
We evaluated the approaches above on the following benchmarks: Amazon Reviews [Hou et al.,
2024], Yelp Open Dataset Reviews [yel], Stanford Sentiment Treebank [Socher et al., 2013, SST],
and World Cities [Bamwor, 2026] (appendix for details). Each dataset contains 30 sets of 100 strings,
sorted by ratings, sentiment scores, and population. We compute the Kendall-Tau score [Kendall,
1938] between the output Y and the ground-truth sorted list Y ∗ , averaged over the dataset.
Fig. 3 shows the speed-accuracy Pareto front of Qwen3 models. All VAs use symmetrization. The
baseline performed terribly in both the accuracy and the runtime. AR baseline was even worse,
with x100 slowdown from the baseline, causing timeouts (1 hour). While the scoring obtained a
reasonable accuracy with the largest 32B model, their performance degrades as the model gets smaller.
AR scoring did not work as much and its performance is often comparable with the baseline. VA
kwicksort (O(log n)) outperformed VA Bitonic (O((log n)2 )) as predicted by the theory. The strength
of VA is most pronounced with the small models. 4B VA Kwicksort outperformed 32B scoring on
Amazon, Yelp, Cities, and on par in SST.
Next, we investigated the effect of thinking, symmetrization, threshold θ, and data parallelism on
kwicksort. Fig. 3 shows that both thinking and symmetrization drastically improve the accuracy, but
thinking significantly increases the runtime while symmetrization sometimes reduces the runtime
because of the more balanced recursions in kwicksort. Larger θ ∈ {4, 16} reduces the runtime with
slight accuracy degradation. Linear speedup from data parallelism (DP) shows the scalability of VAs.
Finally, the table on the right shows that there is no
correlation between the model size and the number of                                                                                            dataset               1.7B/think 4B/think 32B/think
sorting invariance violations (duplicates) by the base-                                                                                         Amazon                 5.0/7.2                             2.1/7.7              2.5/8.3
line. Thinking appears to increase the violations. This                                                                                         Yelp                   6.3/8.5                             1.1/9.3             4.1/10.2
                                                                                                                                                SST                    0.1/3.2                             0.1/5.2              2.1/9.8
                                                                                                                                                cities                 0.0/0.0                             0.1/1.5              1.8/9.8
                                                                                                                              6
highlights the lack of soundness in free-form reason-
ing, which does not occur in VAs and formalization-
based approaches.
While i.i.d. scoring is generally fast, it is accurate only on reviews-like datasets where the ground-
truth dataset also correspond to a finite range (1-5 stars). This assumption does not apply to the
population of cities which lacks a well-defined range, demonstrating susceptibility of formalization-
based approaches to the target language mismatch. Since each list to sort has a widely different range
of populations, if all cities are small/large, the resulting score values predicted by the LLM lacks
the necessary precision. Although it may be more natural to sort the cities by directly predicting
the population, this case study is merely a representative of the data distribution where the range of
values cannot be known in advance.
Finally, we mention the effect of kv-cache reuse. While each VA query requires O(t2 ) computations
for t input tokens, specialized inference engines [Kwon et al., 2023, Zheng et al., 2024] reuse the
prefix kv-cache over multiple queries. This affects the resource complexity of VA queries majority of
which share the prefix. Due to space, we moved its theoretical and empirical analysis to the appendix.


5   Verbalized Clustering

Topic clustering attempts to cluster a set of strings S into a family of subsets S based on their similarity.
The challenge with text-based clustering is that no a priori metric space for clustering exists. While
traditional approach toward this task performs k-Means or other standard clustering algorithms on
the distance matrix over the vector embeddings of the input strings, Verbalized Clustering instead
leverage triplet comparison query or cluster agreement query to LLM. Triplet comparison takes three
elements x, y and z in a metric space ∥ · ∥ and query if ∥x − z∥ < ∥y − z∥, i.e., we ask the LLM a
question such as “Is Z similar to X than is to Y? X: x, Y: y, Z: z”. Cluster agreement query takes two
elements x and y, then query if x ∈ C ⇔ y ∈ C, i.e., we ask the LLM a question such as “Does X
and Y belong to the same class, category, etc.? X: x, Y: y”. Similar to sorting, while some methods
utilize LLM-based triplet comparisons for clustering [Zhang et al., 2023, Viswanathan et al., 2024],
these methods are driven by practical considerations rather than algorithmic complexity analysis.
We propose two verbalized algorithms. The first is Verbalized Approximate Nearest Neighbor
Tree Ensemble Clustering (Vanntec, Alg. 1), which combines O(n log n) triplet-based approximate
nearest neighbor tree construction algorithm [Haghiri et al., 2017] which was originally developed
for k-Approximate Nearest Neighbor Search, and Evidence Accumulation Clustering [Fred and Jain,
2005, 2002, EAC] consensus clustering (ensemble clustering) algorithm. It constructs multiple trees,
views them as an ensemble of hierarchical clustering, then aggregates the results to return the final
clustering. The EAC step does not involve LLM calls, thus O(n log n) with a large constant factor
for LLM calls dominates the runtime. The parallel runtime is O(log n). The second algorithm is
Verbalized KwickCluster based on [Ailon et al., 2008]. In each iteration, it samples a pivot and
performs a cluster agreement query to collect elements in the same cluster. It has the worst-case O(n2 )
queries and O(n) parallel runtime yet practically runs much faster, and its O(log n) parallel time
improvement exists in the literature [Pan et al., 2015]. We compared VA clustering with embedding
baseline, which uses all-MiniLM-L6-v2/granite-embedding-125m-english/Qwen3-8B-Embedding
from Sentence Transformer library and apply K-Means [MacQueen, 1967].
We evaluated the methods across three datasets. Medrxiv [Muennighoff et al., 2022] contains the
titles and the categories of medical papers on Medrxiv. MD3 [Eisenstein et al., 2023] contains English
transcripts of people from three regions with different dialects (US, India, Nigeria) playing a guessing
game. GoEmotions [Demszky et al., 2020] contains sentences labeled with emotion tags. We sampled
one tag per sentence to form clusters.
Fig. 4 shows the accuracy-runtime Pareto front using the Adjusted Mutual Information [Vinh et al.,
2009, 2010]. (See appendix Fig. 8 for Adjusted Rand Index [Hubert and Arabie, 1985] results).
Overall, VAs spent significantly longer runtime, but outperformed the baselines on accuracy. Vanntec
performed better on tasks where the clustering criteria is ambiguous (due to emotion label sampling,
or the nature of dialectal differences). KwickCluster performed better on Medrxiv where the cluster
is clear and categorical and clustering agreement can be answered reliably. Thinking was not cost-
effective, as it only marginally helped the accuracy with x10-x100 more runtime. On the contrary,
symmetrization sometimes doubled the accuracy with a small runtime increase. Further analysis


                                                     7
Algorithm 1 Vanntec(S, #tree k, #cluster n, threshold θ)                                                                                             medarxiv
                                                                                                                        better
                                                                                                                            vanntec, k:5, :16                                kwick
  for 1 ≤ i < k do ; Tree Ti ← ∅         # set of edges                                                        0.5            vanntec, k:5, :16, sym                         kwick, sym
    function R EC (parent p, strings S)                                                                                       vanntec, think, k:5, :16                       kwick, think
                                                                                                                              vanntec, think, k:5, :16, sym                  kwick, think, sym
      If |S| ≤ θ then ∀x ∈ S; Ti ← Ti ∪ {(p, x)}; else                                                         0.4            emb.




                                                                                                 adjusted_mi
      x, y ← randomly chosen from S                                                                                                                               32                          32         32
                                                                                                               0.3                               8                                    8
      Ti ← Ti ∪ {(p, x), (p, y)}                                                                                                   8                   8     32                           8
                                                                                                                       0.022
      Sx ← {z ∈ S | ∥x − z∥ < ∥y − z∥}                                                                         0.2         0.125                                                                        32
                                                                                                                                                                                              8         32
      R EC(x, Sx ); R EC(y, S \ Sx )                                                                                                                         8 32
                                                                                                               0.1                                                      8
    R EC(“root”, S)                                                                                                                                               32
                                                                                                                     10 1          100               101               102                103
  return EAC(n, {T1 , · · · Tk })
                                          md3                                                                                            emotions
                        better                                                        0.3      better
                                                    32   8
    adjusted_mi




                                                                        adjusted_mi
                                                          8        32
                                                                   32                                                                        8         32              88         32              32
                  0.2                           8                                     0.2                        8                                                                             3232
                                                                                                                                                        32                    8
                                                      32
                                                         32   8                                                                          8 3232          8                        8
                                   8         32 328 8 32 8                            0.1          0.022                                      8
                  0.0 0.1250.022               8                                               0.125
                     10 1          100   101         102          103                       10 1                            100            101                     102                            103


Figure 4: The speed-accuracy Pareto front (log x-axis: the runtime per query, y-axis: Adjusted Mutual
Information) of clustering tasks.


in the appendix Fig. 9 shows the ensemble effect of Vanntec, which demonstrates the importance
of aggregating multiple trees via consensus clustering (EAC), and the visualization of the first tree
formed by Vanntec in the first list of Medrxiv dataset, which showcases its interpretability.

6                 Verbalized Submodular Maximization
A submodular set maximization task is a task of maximizing the utility f (S) of a solution S ⊆ C in
a search space C, where f (S) has diminishing returns, i.e., ∀x ∈ C, S ⊆ S ′ ⊆ C; f (S ′ ∪ {x}) −
f (S ′ ) ≤ f (S ∪ {x}) − f (S). The task has various applications including information retrieval as
well as resource allocations. This approach, however, only works in a setting that has a well-defined
submodular evaluation function f . Once the set C is the universe of natural language input, and when
the criteria for optimization can be only informally specified, classical approaches toward submodular
maximization are not directly applicable. We propose Verbalized Greedy Submodular Maximization
(VGSM), a verbalized algorithm that follows the classical greedy algorithm that guarantees 1 − 1/e
optimality. VGSM is an (O(|C|), O(|C|))-VA for selecting |S| = k elements from C, whose step
i selects an element from |C| − i remaining elements. It is based on chat interactions, whose step
incrementally asks for a new element. While traditionally submodular maximization requires a
concrete evaluation function f , VGSM specifies an implicit score function by giving a prompt to the
LLM (available in the appendix). Although it does not produce an absolute score value f (S ∪ {x})
for a newly selected element x ∈ C \ S, this is not an issue because greedy algorithm only requires a
contrastive measure that encodes the selection policy. We evaluated this approach on WiFi Access
Point (AP) Optimization and two Retrieval Augmented Generation tasks.

WiFi AP Optimization This is a classic application of submodular maximization. Using 10 real-
world floor plans obtained from HouseExpo dataset [Li et al., 2020], we created a coarse grid of height
and width at least 16 cells, then obtained the exact optimal WiFi AP locations for k = 3 APs using a
branch-and-bound procedure under the submodular log-distance path loss model (appendix Sec. D.3).
Visualization of the optimal locations indicated that the APs should be placed near the center of or the
boundaries between the rooms to provide the maximum coverage (appendix Fig. 14), matching our
natural intuition. This suggests that an LLM could return a reasonable location assignments, albeit
imprecise or suboptimal, if it actually has a strong common-sense.
We compared VGSM with a baseline which uses JSON-structured decoding to return the entire
assignment as a list of (x, y) coordinates. Both approaches are given the same prompt prefix which
specifies the evaluation function in python code and an ASCII art floor map, ensuring the same
amount of information is given. We measured the runtime and the optimality gap against the optimal


                                                                        8
                                                 Access Point Optimization                                                                            ragbench_hotpotqa, k=6
                                                                                                                         10       better
                        0.5                    base                  vsgm                                                          emb.                                e+VGSM, k2:12
                                  1.7
                                               base, think           vsgm, think                                                   e+kwick, k2:12                      e+VGSM, k2:24
                        0.4                                                                                              0         e+kwick, k2:24                      e+VGSM, think, k2:12
                                                                                                                                   e+kwick, think, k2:12               e+VGSM, think, k2:24




              gap_opt
                        0.3                                1.7                                                                     e+kwick, think, k2:24




                                                                                                                  logp
                               1.7 4                                                                                     10              32                                        4        32
                        0.2                                                                                                   4             4         32                    44 4       32   32 32
                                    4                                4                            32
                        0.1                    32 32                     1.7             4              32
                                                                                                                         20                 32   32
                                better                                                                                        4             4
                        0.0
                                           101                                 102                                                    102                     103               104

                                               Access Point Optimization                                                                                   ragbench_cuad, k=6          32
                                1.7                                                                                               4better 4 32        32
                                                                                                                                                                            4 4 4 4 32 32 32
                     1.0                                                                                                 15
                                                                 4
         violation



                                  4               32 1.7                                     32                                                  32




                                                                                                                  logp
                     0.5                                                                                                 20                 32
                               1.7               32                        1.7                         32                         4         4
                     0.0      better
                               4                                                     4                                   25
                                         101                              102                           103                           102                     103               104



Figure 5: The speed-accuracy Pareto front of submodular maximization tasks. In all subplots, log x-
axis is the runtime per query. y-axes are: (Top left) Optimality gap of WiFi tasks. (Bottom left) The
number of AP location violations in WiFi tasks. (Right) LOGP of RAG tasks (hotpotQA, CUAD)
retrieving k = 6 documents. k = 3, 12 and Jaccard distance results are available in the appendix.


solution. Fig. 5 shows that VGSM outperformed the baselines and obtained solutions are relatively
close to the exact optimal solution. In addition to failing to distribute APs at effective positions to
maximize the coverage, the baseline also violated the constraints specified in the prompt (Fig. 5,
right). This includes assigning APs in the walls despite explicitly told not to, or placing multiple APs
at the same position. These invalid APs are removed when evaluating the solution. While the number
of violations reduced with thinking, it did not completely go away despite suffering from a significant
runtime increase, exposing the lack of soundness in LLMs.

Retrieval Augmented Generation (RAG) Given the success of VGSM in tasks with a known
explicitly-defined submodular evaluation function, we next evaluate VGSM on an evaluation function
implicitly, informally defined by the queries. One such task is RAG, a mainstream approach for
reducing LLM hallucinations by retrieving documents relevant to the query from a database and
appending them to the prompt so that LLMs can draw correct answers from the documents.
While existing work tends to simply rank the documents via vector embedding similarity search, this
approach fails when the task requires combining information in multiple documents to draw conclu-
sions, because all the top-ranked documents may be similar to each other and lack crucial information.
To address this limitation, existing work formulated multi-hop Q&A tasks [Yang et al., 2018] and
observed that there are several types in each ground-truth retrieval (e.g., bridging, comparison, etc),
differing in how they chain multiple information together. Existing work proposed various heuristic
methods that additionally require fine-tuning [Park et al., 2025], based on the observations.
On the other hand, traditional approaches to multi-hop reasoning utilize submodularity. For example,
Maximum Marginal Relevance (MMR) rule [Carbonell and Goldstein, 1998] takes an explicitly
defined evaluation function f and makes it submodular. However, in a LLM-based retriever, f is only
implicitly defined by the prompt, making it difficult to apply this insight.
Greedy submodular maximization guarantees 1 − 1/e optimality under a monotone submodular
function f . In contrast, due to the lack of explicit f , VGSM can only make a much weaker statement,
such as if f is indeed submodular, then it can guarantee 1 − 1/e optimality. One may wonder if such
a weak statement is meaningful, but this question is logically inverted. The submodular assumption is
a model simplification of the real-world task anyway. Given a model (implicit or explicit), it is in fact
in the realm of empirical study to verify its correctness, as was done for the log-distance model with
the actual physics experiments. Since VGSM would work if the implicit f was monotone submodular
and not if otherwise, we could verify the monotone submodularity of f by evaluating VGSM.
We evaluated two RAG datasets: HotpotQA [Yang et al., 2018] (fullwiki, hard) and CUAD [Hendrycks
et al., 2021]. Each dataset contains a set of 4-tuples (Q, A, S ∗ , D) where D is a set of documents,
Q is the question, A is the ground-truth
                                   P       answer, and S ∗ is the ground-truth retrieval. We assume
a generative model p(A|D, Q) = S pϕ (A|S, Q)pψ (S|Q, D), where S is the documents selected
by the retrieval model ψ, and pϕ (A|S, Q) represents the likelihood of the answer by an answering
model ϕ. Given ψ and ϕ, we retrieve k = 3, 6, 12 documents with ψ and evaluate the performance


                                                                                                              9
                              P
by LOGP = log pϕ (A|S, Q) = t log pϕ (At |A1:t−1 , S, Q), i.e., the sum of logits over the tokens in
A. This logits are obtained by feeding ϕ a prompt concatenating Q, S, A in order. If S ≈ S ∗ , the
likelihood should be higher. We also measured the Jaccard distance between S and S ∗ .
We compared VGSM with 2 baselines. Embedding baseline uses state-of-the-art Qwen3-Embedding-
8B for top-k documents retrieval with cosine distance. Verbalized KwickSelect uses a symmetrized
parallel KwickSelect algorithm, a top-k selection variant of kwicksort (when the right branch R has
|R| > k elements, recurse into it; otherwise, recurse into the left branch L and select top-|L| − k − 1
elements). We evaluate it in order to see the impact of ignoring the submodularity. In VGSM and
KwickSelect, we tested ψ ∈ {Qwen3-4B, Qwen3-32B} with ϕ = Qwen3-32B. To reduce the runtime
of the experiment, VGSM and Verbalized KwickSelect pre-selects 2k or 4k documents using the
embedding baseline before running the respective algorithm.
Fig. 5 shows that k documents retrieved by VGSM from 2k or 4k documents have better LOGP than
those simply selected by the embedding. KwickSelect has worse LOGP with similar runtime, thus
the implicit objective encoded by the query was indeed approximately submodular. Thinking was
not cost-effective; VGSM already took care of the sequential algorithmic thoughts, thus there is
significantly less need for thinking in each document selection step.

7      Conclusion, Discussion, Future Work
We demonstrated the feasibility of Verbalized Algorithms (VAs), a general disciplined paradigm
for performing algorithmic reasoning with LLMs. It leverages the strong prior and the established
theoretical results of classical discrete algorithms to significantly improve the accuracy even with a
small model without costly training, and improve the runtime of such reasoning. While this paper
explored only a limited number of examples due to space, our experiments demonstrated that overall,
spurious free-form self-thought via think-tags could harm the accuracy, and theoretically grounded
algorithmic reasoning targeted to specific tasks tends to be superior. We would like to remind the
community that algorithms and computers were born out of humanity’s particular weakness in long
sequential reasoning, and that algorithmic analysis is a tool developed to understand it. These tools
are still useful even on opaque LLM-based reasoning, and throwing them out is not an option.
Future work includes extending VA to more complex, potentially combinatorial algorithms, including
Pareto front computation for diverse / non-dominated document retrieval, DPLL/CDCL, local search,
best-first search for combinatorial reasoning / optimization / planning.

References
Yelp    Open   Dataset   Reviews.         URL     https://huggingface.co/datasets/yashraizad/
    yelp-open-dataset-reviews.
N. Ailon, M. Charikar, and A. Newman. Aggregating inconsistent information: ranking and clustering.
   Journal of the ACM (JACM), 55(5):1–27, 2008.
Bamwor. World cities dataset 2026, 2026. URL https://bamwor.com. Based on GeoNames, curated by
   Bamwor.
K. E. Batcher. Sorting Networks and Their Applications. In Spring Joint Computer Conference. ACM,
   1968.
R. A. Bradley and M. E. Terry. Rank Analysis of Incomplete Block Designs: I. The Method of Paired
   Comparisons. Biometrika, 39(3/4):324–345, 1952.
J. Carbonell and J. Goldstein. The use of MMR, Diversity-Based Reranking for Reordering Documents
   and Producing Summaries. In Proc. of the Annual International ACM SIGIR Conference on Research
   and Development in Information Retrieval, pages 335–336, 1998.
S. Casper, X. Davies, C. Shi, T. K. Gilbert, J. Scheurer, J. Rando, R. Freedman, T. Korbak, D. Lindner,
   P. Freire, et al. Open Problems and Fundamental Limitations of Reinforcement Learning from Human
   Feedback. Transactions on Machine Learning Research.
W.-S. Chao, Z. Zheng, H. Zhu, and H. Liu. Make Large Language Model a Better Ranker. In Findings of
   the Association for Computational Linguistics: EMNLP 2024, pages 918–929, 2024.
D. Demszky, D. Movshovitz-Attias, J. Ko, A. Cowen, G. Nemade, and S. Ravi. GoEmotions: A Dataset
   of Fine-Grained Emotions. In Proc. of the Annual Meeting of the Association for Computational
   Linguistics (ACL), 2020.


                                                  10
A. Djuhera, A. Seffo, M. Asai, and H. Boche. “Don’t Do That!”: Guiding Embodied Systems through
  Large Language Model-based Constraint Generation. arXiv:2506.04500, 2025.
Y. Dong, C. F. Ruan, Y. Cai, Z. Xu, Y. Zhao, R. Lai, and T. Chen. XGrammar: Flexible and Efficient
   Structured Generation Engine for Large Language Models. Proc. of the Annual Conference on Machine
   Learning and Systems, 7, 2025.
J. Eisenstein, C. Rivera, V. Prabhakaran, J. Clark, D. Demszky, S. Mak, R. Rajakumar, D. Elworthy,
   L. Baker, and D. Sharma. MD3: The Multi-Dialect Dataset of Dialogues. In Proceedings of INTER-
   SPEECH, 2023.
M. Fine-Morris, V. Hsiao, L. N. Smith, L. M. Hiatt, and M. Roberts. Leveraging LLMs for Generating
  Document-Informed Hierarchical Planning Models: A Proposal. In AAAI 2025 Workshop LM4Plan,
  2024.
A. L. Fred and A. K. Jain. Data Clustering using Evidence Accumulation. In Proc. of the International
  Conference on Pattern Recognition (ICPR), volume 4, pages 276–280. IEEE, 2002.
A. L. Fred and A. K. Jain. Combining Multiple Clusterings using Evidence Accumulation. IEEE
  Transactions on Pattern Analysis and Machine Intelligence, 27(6):835–850, 2005.
L. Guan, K. Valmeekam, S. Sreedharan, and S. Kambhampati. Leveraging pre-trained large language
   models to construct and utilize world models for model-based task planning. Proc. of the Advances in
  Neural Information Processing Systems (Neurips), 36:79081–79094, 2023.
D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al. Deepseek-
  R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning. arXiv preprint
  arXiv:2501.12948, 2025.
S. Haghiri, D. Ghoshdastidar, and U. von Luxburg. Comparison-Based Nearest Neighbor Search. In
   Proc. of the International Conference on Artificial Intelligence and Statistics (AISTATS), pages 851–859.
   PMLR, 2017.
Y. Hao, Y. Zhang, and C. Fan. Planning Anything with Rigor: General-Purpose Zero-Shot Planning
  with LLM-based Formalized Programming. In Proc. of the International Conference on Learning
  Representations (ICLR), 2024.
R. Hazra, G. Venturato, P. Z. D. Martires, and L. De Raedt. Can Large Language Models Reason? A
  Characterization via 3-SAT. arXiv preprint arXiv:2408.07215, 2024.
D. Hendrycks, C. Burns, A. Chen, and S. Ball. CUAD: An Expert-Annotated NLP Dataset for Legal
  Contract Review. In Proc. of the Advances in Neural Information Processing Systems (Neurips), 2021.
Y. Hou, J. Li, Z. He, A. Yan, X. Chen, and J. McAuley. Bridging Language and Items for Retrieval and
   Recommendation. arXiv preprint arXiv:2403.03952, 2024.
L. Hubert and P. Arabie. Comparing Partitions. Journal of classification, 2(1):193–218, 1985.
K. Järvelin and J. Kekäläinen. Cumulated Gain-Based Evaluation of IR Techniques. ACM Transactions on
  Information Systems (TOIS), 20(4):422–446, 2002.
S. Kambhampati, K. Valmeekam, L. Guan, M. Verma, K. Stechly, S. Bhambri, L. P. Saldyt, and A. B.
   Murthy. Position: LLMs can’t plan, but can help planning in LLM-modulo frameworks. In Proc. of the
   International Conference on Machine Learning (ICML), 2024.
R. M. Karp. A Survey of Parallel Algorithms for Shared-Memory Machines. University of California at
  Berkeley, 1988.
M. Katz, H. Kokel, K. Srinivas, and S. Sohrabi. Thought of Search: Planning with Language Models
 Through The Lens of Efficiency. In Proc. of the Advances in Neural Information Processing Systems
 (Neurips), volume 37, page 138491–138568. Curran Associates, Inc., 2024.
M. G. Kendall. A New Measure of Rank Correlation. Biometrika, 30(1-2):81–93, 1938.
W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. Gonzalez, H. Zhang, and I. Stoica. Efficient
  Memory Management for Large Language Model Serving with Pagedattention. In Proceedings of the
  29th Symposium on Operating Systems Principles, pages 611–626, 2023.
R. Li, L. Cui, S. Lin, and P. Haslum. Naruto: Automatically acquiring planning models from narrative
  texts. In Proc. of AAAI Conference on Artificial Intelligence, volume 38, pages 20194–20202, 2024.
T. Li, D. Ho, C. Li, D. Zhu, C. Wang, and M. Q.-H. Meng. HouseExpo: A Large-Scale 2D Indoor Layout
   Dataset for Learning-based Algorithms on Mobile Robots. In Proc. of IEEE International Workshop on
   Intelligent Robots and Systems (IROS), pages 5839–5846. IEEE, 2020.


                                                    11
N. F. Liu, K. Lin, J. Hewitt, A. Paranjape, M. Bevilacqua, F. Petroni, and P. Liang. Lost in the Middle: How
  Language Models Use Long Contexts. Transactions of the Association for Computational Linguistics,
  12:157–173, 2024.
R. D. Luce. Individual Choice Behavior: A Theoretical Analysis, volume 4. Wiley New York, 1959.
X. Ma, X. Zhang, R. Pradeep, and J. Lin. Zero-Shot Listwise Document Reranking with a Large Language
  Model. arXiv preprint arXiv:2305.02156, 2023.
J. MacQueen. Some methods for classification and analysis of multivariate observations, proceedings of
   5-th berkeley symposium on mathematical statistics and probability. Berkeley, University of California
   Press, 1:281–297, 1967.
D. V. McDermott. The 1998 AI Planning Systems Competition. AI Magazine, 21(2):35–55, 2000.
M. Mitzenmacher and S. Vassilvitskii. Algorithms with Predictions. Communications of the ACM, 65(7):
  33–35, 2022.
N. Muennighoff, N. Tazi, L. Magne, and N. Reimers. MTEB: Massive Text Embedding Benchmark. arXiv
  preprint arXiv:2210.07316, 2022.
T. X. Olausson, A. Gu, B. Lipkin, C. E. Zhang, A. Solar-Lezama, J. B. Tenenbaum, and R. P. Levy. LINC:
   A Neurosymbolic Approach for Logical Reasoning by Combining Language Models with First-Order
   Logic Provers. In Proc. of Empirical Methods in Natural Language Processing, 2023.
J. Oswald, K. Srinivas, H. Kokel, J. Lee, M. Katz, and S. Sohrabi. Large Language Models as Planning Do-
   main Generators. Proceedings of the International Conference on Automated Planning and Scheduling,
   34(1):423–431, May 2024. doi: 10.1609/icaps.v34i1.31502.
X. Pan, D. Papailiopoulos, S. Oymak, B. Recht, K. Ramchandran, and M. I. Jordan. Parallel Correlation
  Clustering on Big Graphs. Proc. of the Advances in Neural Information Processing Systems (Neurips),
  28, 2015.
S. Park, J. Baek, S. Jeong, and S. J. Hwang. Chain of Retrieval: Multi-Aspect Iterative Search Expansion
   and Post-Order Search Aggregation for Full Paper Retrieval. arXiv preprint arXiv:2507.10057, 2025.
R. L. Plackett. The Analysis of Permutations. Journal of the Royal Statistical Society Series C: Applied
  Statistics, 24(2):193–202, 1975.
Z. Qin, R. Jagerman, K. Hui, H. Zhuang, J. Wu, L. Yan, J. Shen, T. Liu, J. Liu, D. Metzler, et al. Large
   Language Models are Effective Text Rankers with Pairwise Ranking Prompting. In Findings of the
  Association for Computational Linguistics: NAACL 2024, pages 1504–1518, 2024.
R. Rafailov, A. Sharma, E. Mitchell, C. D. Manning, S. Ermon, and C. Finn. Direct Preference Optimization:
  Your Language Model is Secretly a Reward Model. Proc. of the Advances in Neural Information
   Processing Systems (Neurips), 36:53728–53741, 2023.
D. Sachan, M. Lewis, M. Joshi, A. Aghajanyan, W.-t. Yih, J. Pineau, and L. Zettlemoyer. Improving
  Passage Retrieval with Zero-Shot Question Generation. In Proc. of Empirical Methods in Natural
  Language Processing, pages 3781–3797, 2022.
T. Schick, J. Dwivedi-Yu, R. Dessı̀, R. Raileanu, M. Lomeli, E. Hambro, L. Zettlemoyer, N. Cancedda, and
   T. Scialom. Toolformer: Language Models can Teach Themselves to Use Tools. Proc. of the Advances
   in Neural Information Processing Systems (Neurips), 36:68539–68551, 2023.
P. Shojaee, S. I. Mirzadeh, K. Alizadeh, M. Horton, S. Bengio, and M. Farajtabar. The Illusion of Thinking:
   Understanding the Strengths and Limitations of Reasoning Models via the Lens of Problem Complexity.
   In Proc. of the Advances in Neural Information Processing Systems (Neurips), 2025.
R. Socher, A. Perelygin, J. Wu, J. Chuang, C. D. Manning, A. Ng, and C. Potts. Recursive Deep
  Models for Semantic Compositionality Over a Sentiment Treebank. In Proc. of Empirical Methods in
  Natural Language Processing, pages 1631–1642, Seattle, Washington, USA, Oct. 2013. Association for
  Computational Linguistics. URL https://www.aclweb.org/anthology/D13-1170.
W. Sun, L. Yan, X. Ma, S. Wang, P. Ren, Z. Chen, D. Yin, and Z. Ren. Is Chatgpt Good at Search?
  Investigating Large Language Models as Re-Ranking Agents. In Proc. of Empirical Methods in Natural
  Language Processing, pages 14918–14937, 2023.
Q. Team. Qwen3 Technical Report, 2025. URL https://arxiv.org/abs/2505.09388.
N. X. Vinh, J. Epps, and J. Bailey. Information Theoretic Measures for Clusterings Comparison: Is a
  Correction for Chance Necessary? In Proc. of the International Conference on Machine Learning
  (ICML), pages 1073–1080, 2009.


                                                    12
N. X. Vinh, J. Epps, and J. Bailey. Information Theoretic Measures for Clusterings Comparison: Variants,
  Properties, Normalization and Correction for Chance. J. Mach. Learn. Res.(JMLR), 11:2837–2854,
  2010.
V. Viswanathan, K. Gashteovski, K. Gashteovski, C. Lawrence, T. Wu, and G. Neubig. Large Language
   Models Enable Few-Shot Clustering. Transactions of the Association for Computational Linguistics, 12:
   321–333, 2024.
J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, et al. Chain-of-Thought
   Prompting Elicits Reasoning in Large Language Models. Proc. of the Advances in Neural Information
   Processing Systems (Neurips), 35:24824–24837, 2022.
B. T. Willard and R. Louf. Efficient Guided Generation for Large Language Models. arXiv preprint
  arXiv:2307.09702, 2023.
Y. Xie. Translating natural language to planning goals with large-language models. The International
   Journal of Robotics Research, 2019:1, 2020.
Z. Yang, P. Qi, S. Zhang, Y. Bengio, W. W. Cohen, R. Salakhutdinov, and C. D. Manning. HotpotQA: A
   dataset for diverse, explainable multi-hop question answering. In Proc. of Empirical Methods in Natural
   Language Processing, 2018.
Y. Zhang, Z. Wang, and J. Shang. ClusterLLM: Large Language Models as a Guide for Text Clustering. In
   Proc. of Empirical Methods in Natural Language Processing, pages 13903–13920, 2023.
L. Zheng, L. Yin, Z. Xie, C. L. Sun, J. Huang, C. H. Yu, S. Cao, C. Kozyrakis, I. Stoica, J. E. Gonzalez,
   et al. SGLANG: Efficient Execution of Structured Language Model Programs. Proc. of the Advances in
   Neural Information Processing Systems (Neurips), 37:62557–62583, 2024.




                                                   13
Appendix

A    (n, k)-Verbalized Algorithms

A verbalized algorithm that utilizes the PL reward model of an LLM by using it as a k-categorical oracle is
called a (n, k)-Verbalized Algorithm. For brevity, we may refer to (n, k)-VAs as just k-VAs.
Definition 2 ((n, k)-Verbalized Algorithms). Let A[τ ] be an algorithm that solves T [τ ] with an n-arg
boolean oracle f [τ ] : τ, · · ·, τ → 1..k. A (n, k)-Verbalized Algorithm instantiates f [str] as a multiple-
choice-question (MCQ) query to an LLM.

Symmetrization for (n, k)-VAs Let σ be a permutation of n inputs. An n-ary function f is permutation-
invariant if ∀σ; f (σ(x)) = f (x), and permutation-equivariant if ∀σ; f (σ(x)) = σ(f (x)). For permutation-
invariant oracles in (n, k)-VAs, we query them with S shuffled inputs (hyperparameter S ≤ n!) presenting
the arguments in a different order in the context, then average the output probability over the orderings.
For permutation-equivariant oracles, the probability must be added toward the original element before the
shuffling.


B    Sorting Dataset and Prompt Details

This section summarizes the dataset used for evaluating the sorting task. All verbalized sorting algorithms
use the same query for the same dataset. Let comparison prompt be a comparison query prompt, specific
to each dataset, listed in the following sections. When comparing strings X and Y, we query the LLM the
following prompt, using the f-string notation in Python programming language:

 verbalized_prompt = f"{comparison_prompt}\nX:{X}\nY:{Y}"

To guarantee that all baseline approaches (constraint-decoding baseline, autoregressive constraint-decoding
baseline, I.i.d. scoring, autoregressive scoring) receive the same information as the verbalized sorting, we
construct the prompts for these baselines from the same comparison query prompt used for verbalized
sorting. Let strings be a list of strings to sort. For constraint-decoding baseline, we query the LLM as
follows, with outputs constrained to string representations of numbers from 0 to |strings|:

 constraint_decoding_basline_prompt = (
      f"Sort the following list in the increasing order of quality " +
      f"that is compared in the following comparison criteria: '{comparison_prompt}'. " +
      f"That is, for a pair X and Y, if the answer to the criteria is 'yes', " +
      f"X must appear after Y in the output list. " +
      f"The elements in the list are numbered. " +
      f"Answer the order using a comma-separated list of the numbers.\n" +
      "\n".join([f"{i}: {s}" for i, s in enumerate(strings)])
 )

For scoring-based baseline, we query the LLM with output constrained to a regular expression
"[1-4]\.[0-9]" as follows:

 scoring_prompt = (
   "I want to sort several strings. " +
   "Given two strings X and Y, " +
   "my comparison criteria is as follows: '" + comparison_prompt + "'. " +
   "Assign a score to X below so that for any pair of strings X and Y, " +
   "if the answer to the comparison criteria above is yes, " +
   "the score of X is greater than the score of Y. " +
   "Each score must be between 1 and 5 with one decimal place, " +
   "where the score 5 means that X will most certainly satisfy the comparison against other strings, " +
   "and the score 1 means the opposite. " +
   "For example, if we compare the height of mountains, score 5 will be assigned to the tallest mountains, " +
   "and if we compare the quality of restaurants, score 1 implies that the food or the service is very bad. " +
   "\n" +
   "X: " + X + "\n"
 )


                                                    14
B.1   Amazon reviews sorted by star ratings
We downloaded the dataset from the Hugging Face repository McAuley-Lab/Amazon-Reviews-2023
[Hou et al., 2024] and extracted the Video Games category. We discarded reviews with empty text or title
or reviews with no helpful vote. We deduplicated reviews based on identical text. We then computed
per-product rating statistics and retained only products with more than 100 total reviews and at least 20
reviews in each star rating class (1 to 5 stars). After filtering products, we reduced class imbalance within
reviews per product by limiting each rating bucket to at most 20 reviews. We then selected 30 products
from the filtered set and truncate each review text to 1000 characters to standardize input length.
Comparison query comparison prompt = “You will be given two product reviews, X and Y, written by
various customers about the same product. Is X more favorable to the product than Y?”

B.2   Yelp reviews sorted by star ratings
We constructed the dataset from the Hugging Face dataset yashraizad/yelp-open-dataset-reviews.
We filtered businesses with at least 100 reviews in total and at least 20 reviews for each star rating (1
through 5), then balanced the number of reviews per star (20 reviews per star per product). We selected the
first 30 businesses to form the final dataset.
Comparison query comparison prompt = “You will be given two Yelp reviews, X and Y, of the same
restaurant written by various customers. Is X more favorable to the restaurant than Y?”

B.3   World cities sorted by population
We constructed the dataset from the Hugging Face dataset bamwor/world-cities. We removed duplicate
city names. We retained only timezones that contains more than 30 cities, then randomly sampled 30 such
timezones. For each selected timezone, we sampled up to 100 cities and sorted them by population.
Comparison query comparison prompt = “You will be given two city names, X and Y, in the same
timezone. Is X’s population larger than that of Y?”

B.4   Stanford Sentiment Treebank (SST) sorted by sentiment
We constructed the dataset from the Hugging Face dataset stanfordnlp/sst. We removed duplicate
sentences. Then we formed 20 groups by randomly sampling sentences without replacement. For each
group, we sampled up to 100 sentence-label pairs and sorted them by sentiment label.
Comparison query comparison prompt = “You will be given two sentences, X and Y. Is X more
positive than Y?”

C     Clustering Dataset and Prompt Details
The prompt for Triplet Approximate Nearest Neighbor Tree for X, Y, Z is constructed from
triplet comparison prompt as follows:

 triplet_anns_prompt = f"{triplet_comparison_prompt}\nZ:{Z}\nX:{X}\nY:{Y}"

The prompt for kwickcluster algorithm given X and Y is constructed from class agreement prompt as
follows:

 kwickcluster_prompt = f"{class_agreement_prompt}\nX:{X}\nY:{Y}"

C.1   MTEB/LLM-Eval Medrxiv clustering dataset
This dataset is readily available from Huggingface (mteb/llm-eval-medrxiv clustering s2s v2) and
is used without additional processing. Each dataset contains 5 sets to perform clustering, and each set has
200 strings.
triplet comparison prompt = You will be given three paper titles X, Y, and Z. Is the topic in Z closer
to the topic in X than to the topic in Y?
class agreement prompt = You will be given two paper titles X and Y posted on medrxiv. Is the subject
area (e.g., Orthopedics) of X same as the subject area of Y?


                                                     15
C.2   MD3
We constructed the dataset from the Hugging Face dataset WillHeld/MD3. We treated the three dialects
(en in, en ng, en us) as class labels. We generated 5 sets containing 99 samples each, randomly selecting
33 samples per class. We truncated each transcript to at most 500 characters.
triplet comparison prompt = You will see three dialogue transcripts, X, Y, and Z, of people playing
a guessing game. Does the dialect in Z sound closer to the dialect in X than to the dialect in Y?
class agreement prompt = You will see two dialogue transcripts, X and Y, of people playing a guessing
game. Does X use the same dialect as Y does?

C.3   GoEmotions
We constructed the dataset from the Hugging Face dataset google-research-datasets/go emotions.
We assigned each text to a single label by randomly selecting one of its annotated emotion labels, then
grouped texts into label-specific buckets. We filtered out emotion labels that do not contain enough
examples to support balanced sampling. We then constructed 5 sets, each containing 100 samples drawn
from 5 distinct emotion labels per set. For each selected label, we sampled 20 texts.
triplet comparison prompt = You will see three sentences, X, Y, and Z. Does the emotion in Z sound
closer to the emotion in X than to the emotion in Y?
class agreement prompt = You will see two sentences, X and Y. Does X express the same emotion as
Y does?

D     Verbalized Greedy Submodular Maximization Prompting Detail
VSGM performs a multi-turn conversation with the LLM. Given a user-defined task-specific task prompt
which explains the task, the first turn (i = 0) queries the LLM an initialization prompt. Let C be the
universe of the set to retrieve k items from, and task_prompt and init_prompt be a task / initialization
prompt, respectively. Then:

 init_prompt = (
     task_prompt
     + "\n".join([ f"X{j}: {elem}" for j, elem in enumerate(C)])
     + f"\nStep {i}: Select Y{i}.\n"
     + f"Your answer must be one of: "
     + ", ".join([ "X"+str(j) for j in range(len(C))])
 )

The output is constrained to "X0", "X1", · · · "X{|C| − 1}". In the later step i > 0 of the multi-turn prompt,
Let U and S be the lists of the remaining unselected elements and the selected elements that represent a
partial solution. We query the following:

 prompt = (
     "OK, the current set is "
     + ", ".join([ "X"+str(j) for j, _ in U])
     + f".\nStep {i}: select Y{i}.\n"
     + f"Your answer must be one of: "
     + ", ".join([ "X"+str(j) for j, _ in S])
 )


D.1   Prompts used in the WiFi Access Point Optimization task
Both algorithms (baseline, VGSM) use the same prompt prefix shown below:

def common_prompt(k):
    return (
        f"Your task is to put {k} wifi access points (APs) on this floor to maximize the coverage " +
        "under Log-distance path loss model, i.e., " +
        "assume the signal strength of a particular position is " +
        "the maximum signal strengths across the APs, and " +
        "the signal diminishes logarithmically to the distance between the position and the AP and " +
        "linearly to the number of walls on the line between the position and the AP. " +


                                                     16
        "The final score (coverage) is the sum of signal strengths over the entire floor. " +
        "This coverage function is submodular. " +
        "More concretely, it is computed by the following python code: \n" +
        """
def signal_strength(
    grid: np.ndarray,
    ap: tuple[int, int],
) -> np.ndarray:
    path_loss_exp: float = 2.0
    wall_penalty: float = 5.0
    H, W = grid.shape
    signal = np.full((H, W), -np.inf)

    for i in range(H):
        for j in range(W):
            if grid[i, j] == 0:
                continue

             d = np.sqrt((i - ap[0])**2 + (j - ap[1])**2) + 1e-6
             walls = count_walls(grid, ap, (i, j))

             signal[i, j] = -10 * path_loss_exp * np.log10(d) - wall_penalty * walls

    return signal

def coverage_function(grid: np.ndarray, aps: list[tuple[int, int]], threshold: float = -70.0) -> float:
    H, W = grid.shape
    best_signal = np.full((H, W), -np.inf)

    for ap in aps:
        sig = signal_strength(grid, ap)
        best_signal = np.maximum(best_signal, sig)

    utility = np.maximum(best_signal, threshold)
    return float(utility.sum())
        """ +
        "\nLook at the floor map shown below. " +
        "The letter '#' indicates a wall, and the letter '.' indicates an empty space. " +
        "Assume that the top-left position is the origin. "
    )

Then each algorithm receives the following prompts. Let floor_text be an ascii art representation of the
floor map. VSGM uses the following prompt:

 task_prompt = (
     common_prompt(k) +
     f"Select {k} locations Y0..Y{k-1} " +
     f"from a list of locations X0..X{len(C)-1} one by one. " +
     "Answer the location of each AP as a x-y coordinate on the floor map. " +
     "Note that the top-left position is the origin. " +
     "\nHere is the floor map: \n" +
     floor_text +
     "\nHere are the names of available postions:\n")

The baseline uses the following prompt:

 prompt = (
     common_prompt(k) +
     "Answer the locations of APs as a list of x-y coordinates on the floor map " +
     "in the 'coordinates' value of a json dictionary. " +
     "Do not select the same location twice. " +
     "Do not select the locations in the walls. " +
     "\nHere is the floor map: \n" +
     floor_text)

Its output is constrained to the following Pydantic-based JSON schema:


                                                  17
 class Coordinate(BaseModel):
     x: Annotated[int, Field(ge=0,lt=W)]
     y: Annotated[int, Field(ge=0,lt=H)]
 class WifiOutput(BaseModel):
     coordinates: Annotated[list[Coordinate],
                            Field(min_length=k,
                                  max_length=k)]

D.2    Prompts in the RAG task
The task prompt for VSGM in the RAG task is as follows:
 task_prompt = (
     f"Your task is to select {k} documents Y0..Y{k-1} "
     + f"from a list of documents X0..X{len(D)-1} "
     + "that helps answer a question Q. "
     + f"Select them in {k} steps. "
     + "In each step i, select Yi "
     + "based on what information is new on top of the documents that are already selected and "
     + "how the new information helps answer Q. "
     + "\n"
     + f"Q: {Q}\n"
 )

Kwickselect performs Verbalized kwickselect algorithm for top-k selection. It uses the comparison oracle
which performs a following query for each pair (X, Y ):
    comparison_criteria = (
        "We are collecting a set of documents that helps answer a question Q. "
        "Is information X more helpful than information Y to answer Q?"
        "\n"
        f"Q: {Q}\n"
        f"X:\n{X}\n"
        f"Y:\n{Y}\n"
    )

D.3    Ground Truth Cost Model of Wifi Task
Let F be points on a H × W discrete grid representing the floor map. Given k APs at locations y1 , · · · yk ∈
F , let the signal received from i-th AP at location x ∈ F be S(yi , x) = α+β log ||yi −x||2 +γW (x, yi ) ∈
R, where W (x, yi ) is the number of wall    P grids on the straight line path between x and yi . α, β, γ are
constants. The optimization objective is x∈F maxi S(yi , x), which is submodular.

E     Hardware Details
Maximization and sorting experiments are performed on NVIDIA Tesla A100-80GB GPUs, while cluster-
ing and submodular maximization experiments are performed on NVIDIA Tesla H100 GPUs.

F     Effect of Prefix Caching on Sorting Task
A comparison query in VA sorting consists of a prompt, x1 , and x2 . Assume all strings being compared
has a fixed length L = |x1 | = |x2 |, and that the length of the fixed prefix is Lp . In the exhaustive pairwise
comparison among n strings (O(n2 ) comparisons, equivalent to insertion sort etc.), a naive inference
engine requires O((Lp + 2L)2 ) runtime per each yes/no query, thus O(n2 (Lp + 2L)2 ) runtime in total,
without parallelism.
We analyze the runtime reduction due to kv-caches. Assume that an input query consists of N + M tokens
(prefix and suffix), and the kv-cache of N prefix tokens is already available. Each N + t-th new input token
attends to N + (t − 1) existing tokens, which makes N + M + 1-th token require M
                                                                                     P
                                                                                       t=1 (N + (t − 1)) =
O(N M + M ) runtime. In other words, the runtime of each comparison query reduces to O(2Lp L + 4L2 ),
              2

totalling O(L2p +n2 (2Lp L+4L2 )) runtime. Moreover, since x1 is repeated n times over n2 comparisons, it
further reduces to O(L2p +n(Lp L+L2 )+n2 ((Lp +L)L+L2 )) = O(L2p +n(Lp L+L2 )+n2 (Lp L+2L2 )).


                                                      18
                                               Amazon Reviews, kwicksort-nocache
                         0.35   better             kwick kwicksort_nocache
                         0.30                               4                      32
                                                  4                          32
                         0.25
           kendall_tau
                         0.20
                         0.15
                         0.10
                         0.05
                                         1.7
                         0.00    1.7
                                                      101                               102

Figure 6: The speed-accuracy pareto front (log x-axis: the runtime per query, y-axis: kendall-τ score)
of sorting tasks over various Qwen3 model sizes (1.7B, 4B, 32B), comparing the effect of kv-cache
reuse in KwickSort (with symmetrization, θ = 16). Disabling kv-cache reuse causes a significant
runtime increase.


Although we assumed a simplified, exhaustive (O(n2 )) comparison scenario, this speedup is significant
in practice. Fig. 6 demonstrates the empirical speedup due to kv-cache. RadixAttention in SGLang is
particularly helpful for VAs whose queries share large prefixes.

G    Additional Results
The rest of the pages contain additional tables and figures.




                                                            19
                                                             medarxiv
                          0.50      better vanntec, k:5, :16                        kwick
                          0.45              vanntec, k:5, :16, sym                  kwick, sym
                                            vanntec, think, k:5, :16                kwick, think
                          0.40              vanntec, think, k:5, :16, sym           kwick, think, sym
                                            emb.
                          0.35                                                                                           32
                                                                        32                                 32
            adjusted_mi

                          0.30                             8                                    8
                                              8                  8 32                                  8
                          0.25     0.022
                          0.20          0.125                                                                       32
                                                                                                           8        32
                          0.15                                          8 32
                          0.10                                                     8
                                                                             32
                                 10 1           100         101                   102                  103

                                                                md3
                                   better
                          0.3
                                                                                        32     8                    32
                                                                                                   8
            adjusted_mi




                                                                                                                    32
                          0.2                                            8
                                                                                        32
                          0.1
                                                                    32    32                    32             8
                          0.0
                                0.125           8
                                                                         8 8
                                                                             8               32 8
                                     0.022
                              10 1              100           101                      102                         103

                                                             emotions
                                   better
                       0.30
                       0.25                                                  32
                                                                    8                        88        32               32
         adjusted_mi




                       0.20                 8                                                                        3232
                                                                             32                    8
                       0.15                                      32                                    8
                                                             8                8
                       0.10                                    32
                                       0.022                      8
                       0.05        0.125
                                10 1             100           101                       102                         103

Figure 7: Enlarged version of Fig. 4. The speed-accuracy pareto front (log x-axis: the runtime
per query, y-axis: Adjusted Mutual Information) of clustering tasks (GoEmotions, MD3, Medrxiv)
over various Qwen3 model sizes (1.7B, 4B, 32B). Embedding baseline is cheap but consistently
outperformed. In Medrxiv, the best pareto front was obtained by Kwickcluster because the clusters is
inherently categorical and determining the cluster agreement is easy. In GoEmotions/MD3, VANNS
achieved the best pareto front because the clusters are inherently ambiguous/continuous and hard
to quantify (dialects in MD3), or because the labels are sampled from the multi-label classification
(GoEmotions).



                                                              20
                                                                   medarxiv
                                 0.5      better vanntec, k:5, :16                       kwick
                                                 vanntec, k:5, :16, sym                  kwick, sym
                                                 vanntec, think, k:5, :16                kwick, think
                                 0.4             vanntec, think, k:5, :16, sym           kwick, think, sym
                                                 emb.
                                                                             32
                 adjusted_rand
                                 0.3
                                                                      8 32
                                 0.2                            8                                                        32
                                                                                                             32
                                                                                                    8
                                 0.1          0.022 8                                                   88          32
                                               0.125                      8 32                                      32
                                                                                       32
                                 0.0                                                   8
                                       10 1             100       101                  102                 103

                                                                        md3
                                         better
                             0.3

                                                                                                   8
             adjusted_rand




                             0.2                                                             32                      32
                                                                                                       8           32
                                                                              8
                             0.1                                                             32
                                            0.125                        32    32         8                    8
                             0.0         0.022          8                     8 8 8 32 32
                                   10 1                 100        101             102                             103

                                                                  emotions
                                         better
                         0.20
                                                                                                                         32
                                                                                  32                8
         adjusted_rand




                         0.15                     8                                                               32
                                                                                                   8
                                                                    8
                         0.10                                                                                          32 32
                                                0.022                   32 32
                         0.05                 0.125                 32      8                          8
                                                                                                           8
                                                                  8
                                                                     8
                                   10 1                 100         101                      102                       103

Figure 8: The speed-accuracy pareto front (log x-axis: the runtime per query, y-axis: Adjusted Rand
Index) of clustering tasks (GoEmotions, MD3, Medrxiv) over various Qwen3 model sizes (1.7B, 4B,
32B). Embedding baseline is cheap but consistently outperformed. In Medrxiv, the best pareto front
was obtained by Kwickcluster because the clusters is inherently categorical and determining the
cluster agreement is easy. In GoEmotions/MD3, VANNS achieved the best pareto front because the
clusters are inherently ambiguous/continuous and hard to quantify (dialects in MD3), or because the
labels are sampled from the multi-label classification (GoEmotions).



                                                                   21
                                                       md3, vanntec-detailed
                               better model_params:8             think, model_params:8
                     0.6                 model_params:32         think, model_params:32
                                         sym, model_params:8     think, sym, model_params:8
                     0.5                 sym, model_params:32 think, sym, model_params:32
                     0.4
       adjusted_mi


                     0.3
                                                                                    5            5 5
                     0.2                                5                                                                   5
                                                                                                             5
                     0.1                                          5
                           1                 1 1 1            1            5            1        1
                     0.0                                          1
                                   101                                102                                    103

                                                                                                                   root 0 (138 leaf)
  15                                                                           15                                  root 1 (62 leaf)

  10                                                                           10
   5                                                                           5
   0                                                                           0
   5                                                                            5
  10                                                                           10
  15
                 10            5         0       5       10                                 10       5   0         5            10


                                                 root 0 (30 leaf)
  15                                             root 1 (108 leaf)             15
                                                 root 2 (55 leaf)
                                                 root 3 (7 leaf)
  10                                                                           10

   5                                                                           5

   0                                                                           0
                                                                                                                       root 0 (17 leaf)
   5                                                                            5                                      root 1 (13 leaf)
                                                                                                                       root 2 (22 leaf)
                                                                                                                       root 3 (86 leaf)
  10                                                                           10                                      root 4 (32 leaf)
                                                                                                                       root 5 (23 leaf)
                     10        5         0       5          10                              10       5   0         5            10


Figure 9: (Top) Ensembling effect of VANNS in MD3 task. (Bottom 4) The ground-truth cluster
label (top-left) and the nodes of the nearest-neighbor search tree found by VANNTEC (Qwen3-
32B, Medrxiv) at depth 1-3 colored by the shared parents (⋆), plotted with t-SNE embeddings of
all-MiniLM-L6-v2. VANNTEC’s explicit search tree provides high interpretability.

                                                                      22
                                                         ragbench_hotpotqa, k=3
                          better                emb.                   e+VGSM, k2:6
             5
                                                e+kwick, k2:6          e+VGSM, k2:12
                                                e+kwick, k2:12         e+VGSM, think, k2:6
             10                                 e+kwick, think, k2:6   e+VGSM, think, k2:12
                                                e+kwick, think, k2:12
                                            32                                        4                              32
             15       4                                                                   4                            32
     logp


                                  4          32                                   4                                 3232
                                                                                              4
             20
                                        32
                                          32
             25               4
                          4
                                                                 103                                    104

                                                          ragbench_hotpotqa, k=6
                              better             emb.                   e+VGSM, k2:12
                  5                              e+kwick, k2:12         e+VGSM, k2:24
                                                 e+kwick, k2:24         e+VGSM, think, k2:12
                                                 e+kwick, think, k2:12 e+VGSM, think, k2:24
              10                                 e+kwick, think, k2:24
                              4                   32        32                                    4 4                32 32
                                            4                                             44                  32     32
      logp




              15
                                                       32
                                            32
              20

                          4                 4
              25
                                  102                                103                          104

                                                         ragbench_hotpotqa, k=12
              8           better                 emb.                   e+kwick, think, k2:48
                                                 e+kwick, k2:24         e+VGSM, k2:24
             10                                  e+kwick, k2:48         e+VGSM, k2:48
                                                 e+kwick, think, k2:24
                                                             32 32                             4 4                          32
             12                         4                                                                            32
                                            4
     logp




             14                                 32 32

             16
                      4
                           4
                                        102                                 103                               104

Figure 10: The speed-accuracy pareto front (log x-axis: the runtime per query, y-axis: LOGP) of RAG
tasks (HotpotQA) over two Qwen3 model sizes (4B, 32B).


                                                                       23
                                                              ragbench_cuad, k=3
                  5           better               emb.                   e+VGSM, k2:6
                                                   e+kwick, k2:6          e+VGSM, k2:12
                                                   e+kwick, k2:12         e+VGSM, think, k2:6
              10                                   e+kwick, think, k2:6   e+VGSM, think, k2:12
                                                   e+kwick, think, k2:12
                                                  32                                    4                           32
              15          4                                                                    4                 32 32
                                                                                            44
      logp

                                      4            32                                                              32

              20
                                              32
                                                   32
              25            4
                           4
                                                                       103                                104

                                                              ragbench_cuad, k=6
                              better               emb.                   e+VGSM, k2:12
                  5                                e+kwick, k2:12         e+VGSM, k2:24
                                                   e+kwick, k2:24         e+VGSM, think, k2:12
                                                   e+kwick, think, k2:12 e+VGSM, think, k2:24
              10                                   e+kwick, think, k2:24
                                                        32        32                                                  32
                              4
                                              4                                                 4 4                   32 32
                                                                                            4         4         32
      logp




              15

                                              32             32
              20

                              4               4
              25
                                  102                                   103                        104

                                                              ragbench_cuad, k=12
                          better                   emb.                    e+kwick, think, k2:48
                                                   e+kwick, k2:24          e+VGSM, k2:24
             10                                    e+kwick, k2:48          e+VGSM, k2:48
                                                   e+kwick, think, k2:24
                                                                   32 32                                              32
             12                           4                                                     4 4                   32
                                              4
     logp




             14                                   32 32


             16
                      4           4

                                          102                                     103                           104

Figure 11: The speed-accuracy pareto front (log x-axis: the runtime per query, y-axis: LOGP) of RAG
tasks (CUAD) over two Qwen3 model sizes (4B, 32B).


                                                                             24
                                                         ragbench_hotpotqa, k=3
                1.2       better                emb.                   e+VGSM, k2:6
                                                e+kwick, k2:6          e+VGSM, k2:12
                1.0                             e+kwick, k2:12         e+VGSM, think, k2:6
                                                e+kwick, think, k2:6   e+VGSM, think, k2:12
                0.8                             e+kwick, think, k2:12
                                              32                                                                   32
      jaccard


                0.6   4               4        32                                      4 4                         32
                                                                                        4     4                   3232
                0.4                       32
                                            32
                0.2           4
                          4
                                                                    103                               104

                                                         ragbench_hotpotqa, k=6
                0.8       better                emb.                   e+VGSM, k2:12
                                                e+kwick, k2:12         e+VGSM, k2:24
                0.7                             e+kwick, k2:24         e+VGSM, think, k2:12
                                                e+kwick, think, k2:12 e+VGSM, think, k2:24
                0.6                             e+kwick, think, k2:24
                0.5                              32          32                                                    32 32
      jaccard




                0.4       4                                                            4     4 4                  32
                                          4                                                   4             32
                0.3                                     32

                0.2   4                   4      32

                0.1
                              102                                     103                     104

                                                         ragbench_hotpotqa, k=12
              0.375        better                emb.                   e+kwick, think, k2:48
              0.350                              e+kwick, k2:24         e+VGSM, k2:24
                                                 e+kwick, k2:48         e+VGSM, k2:48
              0.325                              e+kwick, think, k2:24
                                                    4                                             4
                                                                  32 32                           4                    3232
              0.300                       4
    jaccard




              0.275
              0.250
              0.225
                                      4                 32
              0.200               4                     32
                                          102                                    103                        104

Figure 12: The speed-accuracy pareto front (log x-axis: the runtime per query, y-axis: Jaccard
              ∗
distance |S∩S   |                                                            ∗
         |S∪S ∗ | between the selected documents S and the ground truth set S ) of RAG tasks
(HotpotQA) over two Qwen3 model sizes (4B, 32B).

                                                                            25
                                                           ragbench_cuad, k=3
                          better                emb.                   e+VGSM, k2:6
                1.0                             e+kwick, k2:6          e+VGSM, k2:12
                                                e+kwick, k2:12         e+VGSM, think, k2:6
                                                e+kwick, think, k2:6   e+VGSM, think, k2:12
                0.8                             e+kwick, think, k2:12
                                        32                                                                         32
      jaccard


                0.6   4                  32                                           44                           32
                           4
                                                                                       4                        32 32
                                                                                           4
                0.4                    32
                                            32
                0.2       4
                      4
                                                                   103                                    104

                                                           ragbench_cuad, k=6
                          better                emb.                   e+VGSM, k2:12
                0.7                             e+kwick, k2:12         e+VGSM, k2:24
                                                e+kwick, k2:24         e+VGSM, think, k2:12
                0.6                             e+kwick, think, k2:12 e+VGSM, think, k2:24
                                                e+kwick, think, k2:24
                                                 32           32                                                      32
                0.5
      jaccard




                                                                                                                         32
                      4                4                                                       4 4                    32
                0.4                                                                        4      4             32

                0.3                                   32

                0.2         4 4                 32
                           102                                       103                            104

                                                            ragbench_cuad, k=12
              0.375        better                emb.                    e+kwick, think, k2:48
              0.350                              e+kwick, k2:24          e+VGSM, k2:24
                                                 e+kwick, k2:48          e+VGSM, k2:48
              0.325                              e+kwick, think, k2:24
                                            4                       32                                                32
              0.300                             4                   32                          4                       32
                                                                                                4
    jaccard




              0.275
              0.250
              0.225
                               4
              0.200                4                     32
                                                    32
                                       102                                      103                             104

Figure 13: The speed-accuracy pareto front (log x-axis: the runtime per query, y-axis: Jaccard
              ∗
distance |S∩S   |                                                            ∗
         |S∪S ∗ | between the selected documents S and the ground truth set S ) of RAG tasks
(CUAD) over two Qwen3 model sizes (4B, 32B).

                                                                           26
                                                           ####################
                                                           #.............#....#
                                                           #..................#
                                                           #.............#....#
                                                           #......A......#....#
                                                           #.............#....#
                                                           #.............#....#
                                                           ###..###########..##
                                                           #......#......#....#
                                                           #......#......#.A..#
                                                           #......#......#....#
                                                           #...A..########....#
                                                           #......#......#....#
                                                           #......#......#....#
                                                           #......#......#....#
Figure 14: An example floor map obtained from HouseExpo dataset, and the optimal access point
locations obtained by branch-and-bound using upper bounds that assume a modular objective.




                                             27
