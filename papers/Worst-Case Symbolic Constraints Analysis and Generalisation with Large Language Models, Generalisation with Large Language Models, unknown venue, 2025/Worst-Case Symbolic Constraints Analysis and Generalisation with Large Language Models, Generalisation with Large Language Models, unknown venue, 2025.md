                                         Worst-Case Symbolic Constraints Analysis and
                                         Generalisation with Large Language Models
                                         DANIEL KOH, Mohamed bin Zayed University of Artificial Intelligence, United Arab Emirates
                                         YANNIC NOLLER, Ruhr-Universität Bochum, Germany
                                         CORINA S. PASAREANU, Carnegie Mellon University, United States of America
                                         ADRIANS SKAPARS, University of Manchester, United Kingdom
                                         YOUCHENG SUN, Mohamed bin Zayed University of Artificial Intelligence, United Arab Emirates
arXiv:2506.08171v2 [cs.SE] 16 Sep 2025




                                         Large language models (LLMs) have demonstrated strong performance on coding tasks such as generation,
                                         completion and repair, but their ability to handle complex symbolic reasoning over code still remains under-
                                         explored. We introduce the task of worst-case symbolic constraints analysis, which requires inferring the
                                         symbolic constraints that characterise worst-case program executions; these constraints can be solved to
                                         obtain inputs that expose performance bottlenecks or denial-of-service vulnerabilities in software systems. We
                                         show that even state-of-the-art LLMs (e.g., GPT-5) struggle when applied directly on this task. To address this
                                         challenge, we propose WARP, an innovative neurosymbolic approach that computes worst-case constraints
                                         on smaller concrete input sizes using existing program analysis tools, and then leverages LLMs to generalise
                                         these constraints to larger input sizes.
                                            Concretely, WARP comprises: (1) an incremental strategy for LLM-based worst-case reasoning, (2) a solver-
                                         aligned neurosymbolic framework that integrates reinforcement learning with SMT (Satisfiability Modulo
                                         Theories) solving, and (3) a curated dataset of symbolic constraints. Experimental results show that WARP
                                         consistently improves performance on worst-case constraint reasoning. Leveraging the curated constraint
                                         dataset, we use reinforcement learning to fine-tune a model, WARP-1.0-3B, which significantly outperforms
                                         size-matched and even larger baselines. These results demonstrate that incremental constraint reasoning
                                         enhances LLMs’ ability to handle symbolic reasoning and highlight the potential for deeper integration
                                         between neural learning and formal methods in rigorous program analysis.
                                         CCS Concepts: • Computing methodologies → Artificial intelligence; • Theory of computation →
                                         Automated reasoning; Verification by model checking; • Software and its engineering → Constraint and
                                         logic programming.
                                         Additional Key Words and Phrases: large language models, symbolic reasoning, worst-case constraint reasoning,
                                         SMT solving, reinforcement learning, program analysis, neurosymbolic methods

                                         1   Introduction
                                         Understanding the worst-case algorithmic complexity of software systems has many practical
                                         applications, ranging from compiler optimisations, finding and fixing performance bottlenecks, or
                                         improving cybersecurity in the presence of denial-of-service attacks. Profilers are typically used
                                         to find performance bottlenecks; however, they are inherently incomplete, as they are limited by
                                         the number of test inputs used. Symbolic execution techniques, such as WISE [3] and SPF-WCA
                                         [11], attempt exhaustive analysis but face severe scalability limitations, due to the exponential
                                         growth of possible execution paths. Meanwhile, large language models (LLMs), exemplified by
                                         GPT-5 [14], have demonstrated remarkable capabilities in a variety of programming tasks, including
                                         code generation, completion, and repair [7, 16]. However, their sub-symbolic architecture–based
                                         on statistical pattern recognition rather than explicit logical reasoning–is not immediately suited
                                         for the kinds of rigorous analysis required in worst-case complexity reasoning or formal software
                                         verification. This gap has catalysed the field of neurosymbolic AI, which reconciles the flexibility
                                         Authors’ Contact Information: Daniel Koh, Mohamed bin Zayed University of Artificial Intelligence, United Arab Emirates;
                                         Yannic Noller, Ruhr-Universität Bochum, Germany; Corina S. Pasareanu, Carnegie Mellon University, United States of
                                         America; Adrians Skapars, University of Manchester, United Kingdom; Youcheng Sun, Mohamed bin Zayed University of
                                         Artificial Intelligence, United Arab Emirates.
2                                                                                                    Koh et al.




Fig. 1. Overview of WARP for worst-case execution analysis. 1. Incremental Worst-Case Path Constraints
Curation: Java programs are analysed with SPF-WCA to generate worst-case path constraints for smaller
concrete input sizes, which serve as tractable constraints for extrapolating to larger input sizes. 2. Curated
Dataset and Benchmark of Symbolic Constraints: Consolidates these constraints into a resource that
both trains models on worst-case execution patterns and serves as a benchmark for evaluating generalisation
beyond symbolic execution’s limits. 3. Solver-Aligned Neurosymbolic Framework: The WARP (policy)
model generates constraint candidates from prompts, refined via solver-guided feedback and validated with
an SMT Solver for semantic alignment.


of neural inference with the precision of symbolic reasoning. Recent work in the automated
theorem proving domain has applied various approaches like reinforcement learning, retrieval-
augmented generation and integration of external symbolic tools (often called “hammers”) to uplift
the capabilities of LLMs in the neurosymbolic reasoning dimension [9, 24, 25].
   Building on this momentum, we introduce Worst-case Asymptotic Reasoner for Path constraints
(WARP), a unified neurosymbolic framework for the synthesis and verification of worst-case path
constraints, as illustrated in Figure 1. WARP combines symbolic program analysis, reinforcement
learning with solver-guided feedback, and rigorous benchmarking to improve the asymptotic
reasoning capabilities of LLMs. Our work advances neurosymbolic reasoning for program analysis
by addressing the challenge of integrating formal verification with LLMs, and it makes the following
contributions:
  Incremental Worst-Case Constraint Reasoning. As one of our primary contributions, we introduce
an incremental inference strategy for worst-case constraint reasoning with LLMs: obtain solver-
checked worst-case constraints for small input sizes using existing analysis tools, then (train and)
prompt LLMs to generalise these constraint patterns to larger inputs. This reframes the task as
semantics-preserving pattern induction, sharply reduces the effective search space, mitigates path
explosion, and yields substantial gains over direct prompting on large inputs.
   Neurosymbolic Approach for Worst-Case Complexity Analysis. At the core of the WARP framework
is a novel learning paradigm, which we term Reinforcement Learning from Solver-Guided Feedback
(RLSGF). This method fine-tunes LLMs to generate symbolic constraints by leveraging feedback
Worst-Case Symbolic Constraints Analysis and Generalisation with Large Language Models             3


from SMT solvers, for the synthesis of semantically valid and generalisable SMT formulas for
analysing software programs. Rather than exhaustively exploring an exponentially growing search
space, WARP features training on tractable, small-scale program input constraints, enabling the
model to extrapolate constraint patterns to larger inputs—where traditional tools often fail due to
path explosion.

   Fine-Tuning and Benchmarking Datasets. To advance and evaluate worst-case–constraint syn-
thesis, we introduce two complementary resources. First, a fine-tuning dataset of synthetically
generated programs and their worst-case path constraints is designed to elevate the symbolic-
reasoning skills of LLMs. Secondly, a first-of-its-kind benchmark that assesses the semantic fidelity
of generated constraints, formal correctness, and generalisation. By focusing on the under-explored
task of LLM-driven synthesis of worst-case constraints, the benchmark provides a rigorous, repro-
ducible testbed for future work in neurosymbolic reasoning for WCA spectrum.

   A Trained Model for Worst-Case Symbolic Constraint Reasoning. We develop and also release
WARP-1.0-3B, an LLM fine-tuned using the framework to produce symbolic constraints that gener-
alise across input sizes and outperform baselines on asymptotic prediction tasks.

2     Related Work
2.1    Symbolic Program Analysis
Early program model checkers like Java PathFinder (JPF) [8] systematically explore program
execution states to find bugs, but face scalability issues in complex programs. Symbolic PathFinder
(SPF) [18] extended JPF by executing programs on symbolic inputs instead of concrete values,
using constraint solvers to solve path conditions. This enabled automated test generation and
analysis of Java bytecode with high coverage. Symbolic execution inherently suffers from path
explosion in which the number of feasible paths grows exponentially with the number of branches.
Worst-case analysis (WCA) further accentuates this problem, as it often requires the exploration of
an asymptotically exponential number of execution paths, thereby rendering exhaustive analysis
computationally intractable. Prior works introduced heuristics in attempt to mitigate path explosion.
For example, WISE [3] uses symbolic execution at small input scales and learns simple “generator”
policies (e.g. always-true branches) to steer exploration toward worst-case paths at larger scales.
Meanwhile, SPF-WCA [11] built as an extension to the SPF tool supports more complex branching
strategies (tracking branch history) to ensure worst-case paths are explored. While these approaches
prune the search, they remain limited by the exponential path growth and heavy reliance on solvers.

2.2    LLMs for Program Analysis
The emergence of LLMs pretrained on code (e.g. GPT-4, Codex) has opened new avenues for
program reasoning. Modern LLMs can generate syntactically correct code and even perform simple
reasoning about program behaviour in-context. This has spurred research into using LLMs for
software verification and analysis tasks beyond code synthesis. For instance, [15] investigated
whether LLMs can infer loop invariants and other program properties important for verification.
Their study demonstrated that a sufficiently powerful LLM can propose relevant invariants for
synthetic Java programs, hinting at the model’s reasoning ability. Similarly, [23] showed that LLMs
can assist in vulnerability repair by generating candidate patches which are then validated with
formal verification tools. Despite these promising results, purely non-symbolic approaches do not
offer formal correctness guarantees. That is, an LLM’s output (e.g., an invariant or a code patch)
might seem plausible while being erroneous. Consequently, because sub-symbolic LLMs operate as
4                                                                                            Koh et al.


probabilistic next-token predictors [2], it is necessary to deploy an external checker (e.g., an SMT
solver or verifier) to validate these outputs.

2.3    Neurosymbolic Reasoning
Increasingly, researchers are exploring neurosymbolic methods that integrate neural networks with
symbolic reasoning to capitalise on the strengths of each. In the context of program verification,
neurosymbolic systems use learning to guide or supplement traditional formal analyses. GPT-f [17]
was an early landmark, integrating a transformer-based language model into the Metamath [12]
formal system as a proof search agent. GPT-f demonstrated that training using the prover’s success
to update a value function guiding search can continuously improve theorem-proving performance.
Subsequent systems have expanded on this idea. For example, [26] applied deep reinforcement
learning to guide a theorem prover, employing graph neural networks to represent logical formulae,
with the aim of handling long, complex proofs. Techniques inspired by AlphaZero’s self-play have
also been adapted to propose proof steps and receive verification feedback at each step. While
effective, these RL approaches can be computationally expensive due to the need to attempt many
proof paths and compute rewards from successful proofs.
   An alternative direction has been to use pre-trained LLMs with post-training methods. One
notable example is LeanDojo [25], an open-source playground that enables LLMs to interact with
the Lean theorem prover [5]. LeanDojo provides an interface and dataset of proofs, allowing an
LLM-based agent to propose proof steps and query the proof assistant. By augmenting an LLM
with a retrieval mechanism over a Math library, LeanDojo can select relevant premises and tactics,
significantly improving success rates in formal proofs compared to untutored LLM reasoning.
DeepSeek Prover [24] pushes this synergy further by incorporating reinforcement learning signals
from a proof assistant during training. DeepSeek uses Lean to provide a reward signal to fine-tune
an LLM for theorem proving. In doing so, the neural model learns to align its generation with
formal proof requirements, blending learned intuition with strict verification. Such efforts highlight
that combining LLMs with symbolic evaluators (proof assistants, static analysers, solvers) can
yield systems that are both creative and more reliable. Our work falls into this neurosymbolic
spectrum, where we study and evaluate the application of LLM to synthesise worst-case complexity
path constraints in SMT-LIB v2 (SMT) [1] format. We further formally verify that the synthesised
constraints are semantically equivalent to the worst-case path constraints using the SMT solver
Z3 [4]. The verification is used to guide training and evaluate model capability.

3     Problem Formulation
Symbolic worst-case analysis identifies input conditions under which software exhibits its maximal
resource usage – whether time, memory, or instruction count. Identifying these conditions is crucial
to prevent vulnerabilities and bottlenecks in real-world applications. However, existing symbolic
execution tools, such as SPF-WCA, face significant scalability limitations due to the exponential
path growth. Symbolic execution explores the program paths by solving the path constraints
generated from conditional branches. The worst-case complexity emerges for input size 𝑛 from the
paths Π(𝑛) yielding the maximal resource consumption max 𝐶 (𝜋) where 𝐶 (𝜋) is the cost function
                                                        𝜋 ∈Π (𝑛)
for path 𝜋.

3.1    Motivating Example
Consider the example QuickSort (see Listing 1). Worst-case analysis can derive constraints for
small inputs (e.g. 𝑛 = 3) succinctly represented as SMT formula:
                (assert (and (<= in0 in2) (<= in1 in2) (<= in0 in1)))
Worst-Case Symbolic Constraints Analysis and Generalisation with Large Language Models                       5


Listing 1. Excerpt of the QuickSort function taken from the benchmark, which implements a divide-and-
conquer approach to sort an array by partitioning it around a pivot element and recursively sorting the
resulting subarrays. This method typically runs in 𝑂 (𝑛 𝑙𝑜𝑔(𝑛)) time on average, but may degrade to 𝑂 (𝑛 2 ) in
the worst case when the pivot selection produces highly unbalanced partitions.
 1    public class QuickSort {
 2        public static void quickSort(int[] arr, int low, int high) {
 3            if (low < high) {
 4                int pivotIndex = partition(arr, low, high);
 5                quickSort(arr, low, pivotIndex - 1);
 6                quickSort(arr, pivotIndex + 1, high);
 7            }
 8        }
 9

10          public static int partition(int[] arr, int low, int high) {
11              int pivot = arr[high];
12              int i = low - 1;
13              for (int j = low; j < high; j++) {
14                  if (arr[j] <= pivot) {
15                      i++;
16                      int temp = arr[i];
17                      arr[i] = arr[j];
18                      arr[j] = temp;
19                  }
20              }
21              int temp = arr[i+1];
22              arr[i+1] = arr[high];
23              arr[high] = temp;
24              return i + 1;
25          }
26    }


   As input size grows (e.g. 𝑛 = 12), the symbolic execution tool’s computation becomes increasingly
intensive, quickly exceeding thousands of logical clauses. In particular, this represents a 212 = 4096-
fold increase in the number of execution paths compared to input 𝑛 = 3 above.
   Even with optimised symbolic methods, like history-preserving guidance, this quickly becomes
computationally infeasible at larger input sizes, requiring paradoxical amounts of computational
resources and time. Analysing QuickSort at 𝑛 = 30 entails exploring 230 ≈ 109 paths, translating to
impractical CPU time and memory usage, rendering exhaustive methods computationally infeasible.

3.2       Vanilla Prompting
We first explore the direct application of an LLM to generate SMT worst-case constraints for the
Java programs. The LLM is given the program and it is instructed to output a syntactically correct,
canonical SMT assertion (see Listing 2). To quantify performance under vanilla prompting, we
evaluated a state-of-the-art proprietary LLM, GPT-5 [14], across all 20 programs in the WARP
benchmark (see subsection 4.1). For each program, we sampled five input sizes {2, 4, 8, 16, 30}
and tasked the model with generating the worst-case path constraints at each size. A generated
constraint is counted as correct only if it is both: (1) syntactically valid and (2) semantically
6                                                                                               Koh et al.


                            Table 1. Results of Vanilla Prompting with GPT-5


                                                                       Input Size
WARP Benchmark Programs
                                                  2            4          8            16            30
ArrayTwister                                      ✗           ✗            ✗            ✗            ✗
BinarySearch                                      ✗           ✓            ✓            ✓            ✗
BinarySearchTreeHeight                            ✓           ✗            ✓            ✓            ✓
BinaryTreeSearch                                  ✗           ✗            ✗            ✗            ✗
BubbleSort                                        ✓           ✓            ✓            ✗            ✗
CaseFlipper                                       ✗           ✗            ✗            ✗            ✗
Collatz                                           ✗           ✗            ✗            ✗            ✗
ComplexStateMachineParser                         ✗           ✗            ✗            ✗            ✗
Dijkstra                                          ✗           ✗            ✗            ✗            ✗
DizzyRamp                                         ✗           ✗            ✗            ✗            ✗
GreedyStepper                                     ✗           ✗            ✗            ✗            ✗
KnapsackSolver                                    ✗           ✗            ✗            ✗            ✗
MazeSolver                                        ✗           ✗            ✗            ✗            ✗
MergeSort                                         ✗           ✗            ✗            ✗            ✗
NaiveFibonacci                                    ✗           ✗            ✗            ✗            ✗
QuickSort                                         ✓           ✗            ✗            ✗            ✗
RampUp                                            ✗           ✗            ✗            ✗            ✗
SortedListInsert                                  ✗           ✗            ✗            ✗            ✗
SubarraySumFinder                                 ✓           ✗            ✗            ✓            ✗
TowerOfHanoi                                      ✗           ✗            ✗            ✗            ✗
                                        Notes: ✓= TRUE, ✗= FALSE



Listing 2. Vanilla prompt structure for worst-case constraint reasoning. [WARP benchmark Program] denotes
the placeholder for a single WARP benchmark program (see subsection 4.1). [Input Size] is an integer in
the set 𝑛 = {2, 4, 8, 16, 30}.
[WARP Benchmark Program]

What is the worst-case time complexity of the Java program above.
Also, provide us the corresponding constraint in SMT2 format
for input size n:[Input Size]

Give the final SMT2 constraint at the end starting with 'Answer:'




equivalent to the ground-truth worst-case constraint verified by the Z3 solver. This dual criterion
ensures that correctness reflects true logical equivalence rather than superficial string similarity.
  As summarised in Table 1, GPT-5 achieves only 13/100 in overall accuracy. Most outputs are
syntactically well-formed but fail semantic equivalence checks, underscoring the difficulty of
worst-case constraint reasoning: without additional structure, even current state-of-the-art models
cannot reliably generate correct constraints. These findings motivate the incremental neurosymbolic
reasoning strategy of WARP: rather than requiring the model to induce full constraints from scratch,
Worst-Case Symbolic Constraints Analysis and Generalisation with Large Language Models                            7


we scaffold learning with solver-verified instances at smaller input sizes, enabling systematic
extrapolation to larger and otherwise infeasible regimes.

3.3     Augmenting Symbolic Execution with LLMs
We propose a neurosymbolic approach that uses SPF-WCA and LLMs in an incremental fashion.
Concretely, we use SPF-WCA to obtain constraints at small input sizes and we task the LLM to:
      (1) Learn constraint patterns from those tractable input sizes.
      (2) Extrapolate these patterns to predict constraints for significantly larger inputs.

   Definition 3.1 (Incremental Worst-Case Constraint Reasoning). Given a sequence of solver-derived
constraint sets {Φ𝑛1 , Φ𝑛2 , . . . , Φ𝑛𝑘 } for small input sizes 𝑛 1 < 𝑛 2 < · · · < 𝑛𝑘 , infer a constraint set Φ̂𝑛
for a larger input size 𝑛 ≫ 𝑛𝑘 such that Φ̂𝑛 ≡ Φ𝑛 with respect to solver-based semantic equivalence.

   This incremental formulation reframes worst-case analysis as a pattern induction problem: instead
of exploring all paths for large 𝑛, the learner generalises from small-scale constraints to approximate
or reproduce Φ𝑛 . This reduces the exponential search space, mitigates path explosion, and enables
analysis at input scales where symbolic execution alone is infeasible.

4     Methodology
Figure 1 gives a high-level overview of WARP. Note that WARP includes a benchmark designed
to evaluate constraint generalisation, and it is applied to finetune an LLM through reinforcement
learning to synthesise SMT constraints for our neurosymbolic task. Our results show that the
incremental reasoning approach significantly improves LLMs’ ability to solve worst-case constraint
reasoning tasks. The fine-tuned WARP-1.0-3B model also matches the performance of much larger
proprietary and open-source baselines in terms of both accuracy and semantic validity of generated
constraints. Therefore, our results underscore WARP’s effectiveness as a lightweight neurosymbolic
alternative.

4.1     Incremental Worst-Case Path Constraints Curation
The defining feature of WARP is its incremental approach to worst-case constraint reasoning.
Instead of asking an LLM to derive large-𝑛 constraints from scratch, we first curate solver-verified
constraints at small input sizes where symbolic execution is efficient and reliable. These small-𝑛
constraints act as building blocks: they capture the recurring structural patterns of worst-case
program behaviour and provide the context needed for the LLM to extrapolate to larger, harder
cases. Concretely, we use SPF-WCA [11] to analyse programs at tractable input sizes in its default
configuration. SPF-WCA’s default cost model utilises the depth of the symbolic execution path, i.e.,
the more branches with symbolic conditions are visited during the execution, the more costly such
a path is. For each program and size 𝑛, SPF-WCA yields worst-case path constraints in SMT format.
By collecting these constraints across multiple small-𝑛 values, we build sequences that illustrate
how the constraint structure evolves as 𝑛 increases.
   WARP leverages these curated constraints in an incremental fashion during both inference and
training. During inference, curated examples at smaller 𝑛 values are included in the prompt, and the
model is tasked with generating the constraint for a larger, held-out input size. During fine-tuning,
they form the foundation of a dataset that familiarises LLMs with the syntax and semantics of SMT
constraints while teaching them the progression of constraint patterns across input sizes. This setup
explicitly isolates the ability to generalise incrementally, ensuring that observed performance gains
reflect learned symbolic reasoning patterns rather than access to ground-truth large-𝑛 solutions.
8                                                                                           Koh et al.




                      Fig. 2. Structure of a single instance in WARP-benchmark.


4.2   Dataset Creation and Benchmarking
In order to accommodate the novel application of LLMs for the prediction of worst-case path
constraints, a corpus of Java programs and the worst-case execution path constraints that follow
have been collected and formatted to enable the development of generalisation and predictive
capabilities in LLMs through reinforcement learning. For fine-tuning, we assembled a diverse
dataset of 23,600 instances—comprising 17,700 training examples and 5,900 test examples—that
span a broad range of symbolic constraints, from simple arithmetic checks to complex logical
compositions. This collection includes both synthetic programs and examples derived from real-
world applications. Notably, a portion of the dataset comes from SPF-WCA and the Badger tool’s
examples [13], which capture a variety of behaviours representative of real-world applications.
   Independent from our fine-tuning dataset, we compiled another test set consisting of over 600
instances from 20 Java programs. Each instance includes ground-truth SMT constraints for several
smaller 𝑛 values from a single Java program, designating a larger 𝑛 as the held-out target the
model must synthesise (see Figure 2). By comparing the generated constraints against the held-out
ground-truth, we directly measure a model’s ability to extrapolate the underlying symbolic rule
rather than merely memorising observed patterns. These programs implement different algorithms,
spanning array manipulation, searching, sorting, graph traversal, optimisation and recursion.
   Defining Difficulty via Jumps in 𝑛. We posit that difficulty depends not only on the upper bound
of 𝑛 but also on the magnitude of the leap from the largest available candidate example to the
target. For instance, employing examples at 𝑛 = 1, 2, 3 and querying 𝑛 = 30 can be considered
more challenging than progressing through intermediate values such as (𝑛 = 1, 3, 6, 8, 15) to 𝑛 = 30.
Larger leaps demand more extensive extrapolation, while smaller, incremental steps emphasise
granular pattern replication.
   Tiered Complexity and Model Limitations. To accommodate both modest and extensive leaps
without incurring path explosion, we classify each instance into small, medium, and large tiers,
each associated with distinct ranges of jump size. As input size 𝑛 increases, synthesising the
corresponding worst-case constraints requires more reasoning and results in longer outputs, often
nearing or exceeding the model’s maximum generation capacity. While providing more examples
in the prompt can improve output quality by offering richer context, it also encourages the model
to generate longer reasoning chains, which consume a greater portion of the output budget. This
introduces a critical trade-off: richer prompts can improve intermediate reasoning, but increase the
risk that the model truncates before fully emitting the final constraint. To mitigate this, we impose
an upper limit on prompt size to ensure adequate capacity is preserved for generation. When the
Worst-Case Symbolic Constraints Analysis and Generalisation with Large Language Models                    9


Listing 3. Template used for training WARP-1.0. (EXAMPLES) denotes the placeholder for specific constraint
instances corresponding to smaller input sizes (e.g. N=1:(assert (<= in0 in1))). (QUESTION) is replaced
with the target input size for which the model is asked to generate the corresponding constraint (e.g., 30).
A conversation between User and Assistant.
The user asks a question, and the Assistant solves it.

User: Your role is to take a known pattern of symbolic constraints that represent the
longest execution path of a program and generalize it for any given input size N.
When you receive an input value N, you must generate a canonical SMT-LIB constraint
string that adheres to the following rules:
(assert (op (op (op var_1 var_2)) (op (op var_3 var_4)) (op (op var_5 var_6)) (op var_7 var_8)))
where op is a logical operator (e.g., 'and', 'or', 'not') and var_i are variables or constants.
All per-variable constraints must be combined using a top-level (assert (and ...))
clause. The output must be in exact, canonical SMT-LIB format without extra
commentary in the constraint string.
Show your work in <think> </think> tags. And return the final SMT-LIB constraint string in <answer>
      </answer> tags.
For example: <answer>(assert (and ( >= in0 97) ( <= in0 122)))</answer>.
Here are the known constraints:
[EXAMPLES]
What is the constraint for N=[QUESTION]?

Assistant: Let me solve this step by step.<think>




full set of example constraints exceeds this limit, we reduce the prompt to three representative
examples—the first, the median, and the last. If the reduced prompt still exceeds the threshold, we
exclude the instance entirely. Although this may conservatively filter out potentially solvable cases,
it serves as a practical safeguard: if three examples already exceed the output limit, the constraint
for a larger 𝑛 is likely even longer and prone to truncation.
   Note that this constraint is not only a technical safeguard but also a deliberate design choice
intended to foster broader accessibility. By bounding prompt and output sizes, we make the bench-
mark approachable for smaller models, enabling research on efficient reasoning under limited
resources. Looking forward, we view this as a foundation for extensible benchmarks that systemat-
ically explore trade-offs between model scale, prompt complexity, and output fidelity—paving the
way for evaluating both scaling trends and compact, capable alternatives.
   Final Benchmark Set and Scope. After refining the benchmarking dataset through these constraints,
we obtain a consolidated set of 671 instances. Each instance includes a prompt (featuring constraints
at multiple smaller 𝑛) and asks for a constraint at a larger 𝑛, alongside the corresponding solution.
Restricting 𝑛 to at most 30 allows for practical verification using the Z3 SMT solver [4], ensuring
each instance can be definitively classified as correct or incorrect.

4.3   Reinforcement Learning from Solver-Guided Feedback
  We also contribute WARP-1.0-3B, a 3B parameter model fine-tuned to generate SMT constraints
for worst-case execution. For fine-tuning, we adapt the computationally-efficient framework pro-
posed by Sheng et al. [22] with the following key components:
   Training Template. We build upon Qwen2.5-3B [19] and adapt it using a task-specific prompt
designed to elicit SMT constraint generation. As illustrated in Listing 3, the model is required to
first reason through the problem before providing its final answer. This design choice, inspired by
10                                                                                           Koh et al.


DeepSeek-AI et al. [6], avoids imposing content-specific biases and allows the model’s intrinsic
problem-solving capabilities to emerge naturally.

     Reward Modelling. We adopt a rule-based reward system that consists of two types of reward:
       • Semantic Reward. For each predicted SMT constraint 𝜑ˆ we call the Z3 solver to check
         logical equivalence with the ground-truth constraint 𝜑 ★. If Z3 proves 𝜑ˆ ⇔ 𝜑 ★, the episode
         receives a positive reward; otherwise it receives no reward. This binary signal is cheap
         to compute and correlates well with downstream verification performance described in
         subsection 4.4.
       • Syntactic Reward. A smaller bonus is granted when the output exactly matches the
         required template <think>. . . </think><answer>. . . </answer>. Any deviation yields zero
         bonus, discouraging malformed outputs without allowing the model to trade correctness
         for formatting.
The overall reward 𝑅 is a weighted sum of the two components:

                      𝑅 = 0.1 × Syntactic_Reward + 0.9 × Semantic_Reward                           (1)

This reflects our prioritisation of logical correctness over surface-level fluency. We intentionally
leave the content of the <think> block unscored, focusing evaluation budget on verifiable constraint
generalisation rather than natural language reasoning quality.

  Reinforcement Learning Algorithm. To optimise the model efficiently, we employ Group Relative
Policy Optimisation (GRPO) [21] as an alternative to standard Proximal Policy Optimisation (PPO)
[20]. GRPO eliminates the need for a value model (critic) by estimating advantages from group
scores, thereby reducing computational costs associated with a critic model.

   Hyper-parameter Selection. For the purpose of validating our proposed approach, we adopt
a default hyper-parameter settings set by vLLM [10]. Our primary objective is to demonstrate
the viability of applying our framework onto LLMs, rather than to achieve optimal performance.
Although more extensive hyper-parameter tuning may yield improved results, we fix the policy’s
(actor) temperature, nucleus sampling (top-p) and gradient clipping at 1, as our aim is to demonstrate
the feasibility of low-cost neurosymbolic training pipelines and motivate further exploration in
this direction.

   Training Setting. We fine-tune our pre-trained model using a constant learning rate of 1 × 10−6
and a KL divergence penalty weighted at 0.001. Training is performed in bfloat16 precision on
2 NVIDIA A100 80GB GPUs with a batch size of 256 and both the input and output sequence
length are capped at 2048. In our GRPO setup, we sample 16 rollouts per prompt and estimate the
advantage by using the group’s reward mean and standard deviation as a baseline. These settings
reflect our available hardware resources.

4.4     Evaluation and Performance Metrics
Our evaluation protocol quantifies the performance of SMT constraint generation through auto-
mated, reproducible measures:

  Automated Verification. Let 𝜑 ★ be the ground-truth constraint and 𝜑ˆ the constraint generated by
the model. We deem them correct when they are logically equivalent:
                                   h                                               i
              𝜑 ★ ⇔ 𝜑ˆ ⇐⇒ (𝜑 ★ ∧ ¬𝜑)        ˆ is UNSAT ∧ (𝜑ˆ ∧ ¬𝜑 ★) is UNSAT                    (2)
Worst-Case Symbolic Constraints Analysis and Generalisation with Large Language Models               11


   This bidirectional UNSAT test guarantees that no interpretation satisfies one constraint while vio-
lating the other, thereby certifying semantic equivalence. The resulting boolean signal is consumed
by the reward function described in subsection 4.3.
  Accuracy Metric. We define accuracy as the proportion of tasks for which the generated SMT
constraint is both syntactically valid and semantically correct (i.e., successfully verified by Z3).
By measuring solver-verified equivalence to the true worst-case execution condition, our metric
eschews surrogate objectives such as BLEU or perplexity, which offer no guarantee of formal
correctness.

5     Experiments
We evaluate WARP, our neurosymbolic approach for incremental worst-case constraint reasoning,
across a wide range of popular large language models to assess its general applicability. In addition,
we present WARP-1.0-3B, a fine-tuned model trained with the WARP approach, which achieves the
best performance in its size range and even surpasses several larger open-source and proprietary
baselines. Together, these evaluations demonstrate both the broad effectiveness of WARP when
applied to existing models and its ability to lift performance across scales, enabling models of
different sizes to reach levels typically reserved for much larger ones. The evaluation of WARP is
organised around three research questions:
      RQ1. How does incremental worst-case constraint reasoning enable LLMs to outperform
        vanilla prompting, particularly when extrapolating from small input sizes to larger ones?
      RQ2. To what extent does WARP’s performance improvement reflect genuine symbolic rea-
        soning ability rather than domain-specific adaptation to SMT-LIB syntax?
      RQ3. How robust is incremental worst-case constraint reasoning across different model
        scales, varying extrapolation regimes, and program families representative of real software
        workloads, and what practical trade-offs emerge in terms of accuracy, scalability, and
        computational cost?

5.1    Evaluation Setup
   Evaluation Prompt. We assess each model’s ability to produce complete, structured SMT con-
straints by using the uniform instruction set (see Listing 4). This instruction set directs the model to
present its full reasoning between <think>. . . </think> tags and to return an exact, canonical
SMT assertion between <answer>. . . </answer> tags, without any additional commentary or
truncation. All evaluations are performed zero-shot, with no imposed limit on output length.
  Baselines. We benchmark WARP-1.0-3B against nine open-source checkpoints (3B–32B) and
several contemporaneous OpenAI models, selected to span a representative range of model scales
within our computational budget.

5.2    Overall Results
Our overall results in Table 2 first demonstrate that incremental worst-case constraint reasoning
consistently equips LLMs to outperform vanilla prompting. While GPT-5 represents the strongest
proprietary baseline, its performance under vanilla prompting falls short of all models evaluated
with WARP when equipped with the incremental reasoning strategy. Specifically, GPT-5 achieves
only 13% accuracy when prompted directly, but reaches 95.47% under WARP, underscoring that
incremental worst-case constraint reasoning is essential for enabling reliable generalisation.
   The fine-tuned model WARP-1.0-3B achieves an average zero-shot generalisation accuracy
of 41.08% on our worst-case symbolic-constraint benchmark, evaluated over three independent
12                                                                                                Koh et al.


Listing 4. Instruction set for evaluating WARP-1.0. ([QUESTION]) is a single prompt from the benchmark (see
Figure 2).
You are a helpful assistant.
User: All per-variable constraints must be combined using a top-level (assert (and ...)) clause.
The output must be in exact, canonical SMT-LIB format without extra commentary in the constraint
string.
Show your work in <think> </think> tags. And return the final SMT-LIB constraint string in
<answer> </answer> tags.
For example: <answer>(assert (and ( >= in0 97) ( <= in0 122)))</answer>.
[QUESTION]


Table 2. Symbolic constraint generalisation accuracy (%) across models evaluated under the WARP incremental
worst-case constraint reasoning approach. In general, larger and more sophisticated LLMs achieve higher
accuracy on worst-case constraint inference, and all models perform substantially better than the vanilla
prompting results reported earlier (subsection 3.2). The standout result is WARP-1.0-3B (marked with ∗),
fine-tuned from the lowest-performing baseline, Qwen2.5-3B-Instruct, which delivers more than a fourfold
improvement over its base model and performs on par with, or better than, much larger open-source and
proprietary baselines.

 Model                                   Trial 1 (%)       Trial 2 (%)        Trial 3 (%)      Average (%)
 Qwen2.5-3B-Instruct                          11.18              9.99               8.20       9.79 (±1.49)
 DeepSeek-R1-Distill-Qwen-7B                  18.63             16.39              16.24      17.09 (±1.30)
 Qwen2.5-7B-Instruct                          21.46             25.04              22.95      23.15 (±1.79)
 Falcon3-10B-Instruct                         28.02             29.81              29.36      29.06 (±0.90)
 GPT-4o-2024-11-20                            37.26             36.96              33.08      35.77 (±2.33)
 DeepSeek-R1-Distill-Qwen-14B                 36.51             36.36              35.32      36.07 (±0.66)
 WARP-1.0-3B ∗                                41.43             41.58              40.24      41.08 (±0.72)
 GPT-4.1-2025-04-14                           44.11             45.31              42.47      43.96 (±1.44)
 Qwen2.5-14B-Instruct                         44.86             46.20              48.73      46.60 (±1.94)
 DeepSeek-R1-Distill-Qwen-32B                 48.88             50.52              52.91      50.77 (±2.02)
 GPT-4.1-mini-2025-04-14                      57.82             59.61              55.89      57.77 (±1.86)
 Qwen2.5-32B-Instruct                         70.19             70.64              68.70      69.85 (±1.05)
 o4-mini-2025-04-16                           86.89             87.78              90.61      88.43 (±1.52)
 GPT-5-2025-08-07                             95.83             95.08              95.50      95.47 (±0.38)


trials. This performance represents a more than fourfold improvement over the instruct-tuned
Qwen2.5-3B-Instruct baseline (9.79%) and nearly doubles the accuracy of DeepSeek-7B (17.09%).
Furthermore, WARP-1.0-3B surpasses mid-scale models such as Falcon3-10B (29.06%) and DeepSeek-
14B (36.07%), while maintaining a trial-to-trial variance of less than 1 percentage point, indicating
strong stability and consistent solver alignment. Table 2 presents the zero-shot generalisation results
for all models, including DeepSeek-R1-Distill-Qwen variants with 7B, 14B, and 32B parameters
(hereafter DeepSeek-7B, DeepSeek-14B, and DeepSeek-32B, respectively).
   The recently released GPT-5 achieves an average of 95.47% on our benchmark when combined
with the incremental worst-case constraint reasoning strategy, whereas applied directly it performs
poorly (see Table 1). In parallel, our solver-aligned reinforcement learning framework (RLSGF)
produces large gains at the small scale: WARP-1.0-3B improves from 9.79% (instruct variant of base
model) to 41.08%. These results establish both the upper bound provided by frontier models and
the relative improvement enabled by RLSGF at compact scales.
   Figure 3 depicts each model’s average accuracy plotted against parameter count on a log
scale. Compact baselines such as Qwen2.5-3B (9.79%) and DeepSeek-7B (17.09%) lie at the lower
Worst-Case Symbolic Constraints Analysis and Generalisation with Large Language Models                                        13


end, while Qwen2.5-7B (23.15%), Falcon3-10B (29.06%), and mid-sized open-source models like
DeepSeek-14B (36.07%) and Qwen2.5-14B (46.60%) occupy the middle. Among the largest open
models, DeepSeek-32B scores 50.77% and Qwen2.5-32B scores 69.85%, alongside proprietary model
GPT-4o (35.77%) and its successor GPT-4.1 (43.96%), whose sizes are not publicly disclosed but
are believed to be comparable. Notably, WARP-1.0-3B outperforms its parameter-size peers and
matches or surpasses several 14B models. WARP-1.0’s deviation from parameter-only scaling high-
lights the significant impact of RLSGF, demonstrating that integrating formal SMT validation into
the fine-tuning loop enables compact LLMs to synthesise semantically precise worst-case path
constraints, achieving fidelity comparable to much larger models.

                               100
                                                                                                              GPT-5†
                                90                                                                            o4-mini†
                                80
        Average Accuracy (%)




                                70                                                 Qwen2.5-32B

                                60                                                                            GPT-4.1-mini†
                                50                                                 DeepSeek-32B
                                                                    Qwen2.5-14B
                                                                                                              GPT-4.1†
                                40           WARP-3B
                                                                    DeepSeek-14B                              GPT-4o†
                                30                             Falcon3-10B
                                                          Qwen2.5-7B
                                20                        DeepSeek-7B
                                10           Qwen2.5-3B

                                0
                                     1   3               10             30                        100   175
                                                Model Size (Billion Parameters)

Fig. 3. Model size vs. symbolic constraint accuracy. Points show models with publicly known parameter
counts; dashed lines show benchmarks for models with undisclosed sizes. † Parameter sizes for these models are
proprietary / not publicly disclosed. Horizontal lines indicate reported average accuracies only.



      Answer to RQ1

      The results confirm that incremental worst-case constraint reasoning provides a consistent
      advantage over vanilla prompting for LLMs. After fine-tuning, WARP-1.0-3B achieves more
      than four times the accuracy of its base model and performs competitively with models
      an order of magnitude larger. These findings show that incremental reasoning is key to
      achieving reliable generalisation across model scales.


5.3    Disentangling Symbolic Reasoning from Syntax Adaptation
In Table 2, WARP’s solver-aligned framework improves accuracy in WARP-1.0-3B over its base
Qwen2.5-3B-Instruct model from 9% to 41%. Such gains are substantial, but raw accuracy could
potentially mask whether the model has genuinely learned symbolic reasoning or is merely adapting
to the SMT format. Disentangling these factors is essential for understanding the true source of
improvement and the extent to which WARP advances beyond surface-level pattern matching.
   To make this distinction explicit, we aggregate outcomes into four categories: Correct, Semantics,
Syntax, and Formatting. A prediction is labelled Correct if it is solver-equivalent to the ground truth;
14                                                                                               Koh et al.


Table 3. Error-type breakdown (aggregated over three trials). Correct denotes solver-equivalent outputs;
Syntax are invalid SMT constraints; Semantics are syntactically valid but logically incorrect constraints;
Formatting indicates structural issues (e.g., tag mismatches).

 Model                        Correct                Syntax              Semantics            Formatting
 Qwen2.5-3B                      197                   1626                   135                     55
 Qwen2.5-7B                      466                   1388                   151                      8
 Qwen2.5-14B                     938                    942                   126                      7
 Qwen2.5-32B                    1406                    468                   139                      0
 DeepSeek-7B                     344                    110                   213                    356
 DeepSeek-14B                    726                   1044                   110                    133
 DeepSeek-32B                   1022                    827                   134                     30
 Falcon-10B                      585                   1331                    88                      9
 WARP-1.0-3B                     827                    275                   497                    414
 GPT-4.1                         885                    455                   672                      1
 GPT-4.1-mini                   1163                    305                   543                      2
 GPT-4o                          720                    464                   675                    154
 o4-mini                        1780                     21                   196                     16
 GPT-5                          1919                     15                    79                      0



Semantics if it is syntactically valid but fails equivalence; Syntax if it cannot be parsed by Z3; and
Formatting if the output fails to appear within the required <answer> block. These categories follow
a natural dependency: semantic checks are only possible for syntactically valid outputs, and syntax
can only be assessed if the format permits extraction. In practice, this means that some errors may
conceal deeper correctness, while others expose fundamental weaknesses in instruction-following.
5.3.1 Aggregated Results. As shown in Table 3, WARP-1.0-3B achieves a dramatic reduction in
syntax errors compared to its instruct variant base model (Qwen2.5-3B-Instruct) (from 83% to
14%), but also suffers a high rate of formatting errors (21%). Because the categories are dependent,
many outputs never reach semantic evaluation, making raw counts an incomplete picture of
reasoning ability. In particular, it remains unclear whether WARP-1.0-3B’s apparent semantic
improvements stem from genuine generalisation or are masked by formatting fragility. To address
this, we turn to targeted case studies that allow us to study individual predictions.
5.3.2 Case Studies. To better interpret the error categories, we study representative cases where
automated evaluation under- or over-estimates reasoning ability. We analyse the LLM reasoning
rationale, which refers to the intermediate explanation generated before the final SMT constraint,
typically a step-by-step account of how patterns from smaller input sizes are identified and extrap-
olated to larger 𝑛.
   Case Study A: Improved symbolic reasoning in WARP-1.0-3B. We first examine a case where the base
model produces a syntactically valid but semantically incorrect constraint for 𝑁 = 28, while WARP
generates a solver-equivalent formula under the same prompt (see Listing 5). The base model’s
response misidentifies the governing rule: it describes the sequence as “monotonically increasing”
and encodes only a single chain of ≥ relations. This both reverses the intended comparison direction
and omits the strict < operator that enforces a strictly decreasing chain. Although syntactically
valid, the output is semantically non-equivalent. In contrast, WARP-1.0-3B extrapolates the correct
adjacency schema—“for each 𝑖 > 0: 𝑖𝑛𝑖 ≤ 𝑖𝑛𝑖 −1 and 𝑖𝑛𝑖 < 𝑖𝑛𝑖 −1 ”—across all indices at 𝑁 = 28,
preserving both weak and strict constraints and verifying as solver-equivalent. The contrast
indicates uplift in symbolic reasoning: WARP induces and propagates the correct logical pattern,
Worst-Case Symbolic Constraints Analysis and Generalisation with Large Language Models                        15


while the baseline over-fits surface cues (constraint counts, “increasing” phrasing) and generalises
an incorrect schema.
Listing 5. Case study A (ID 236, small): for 𝑁 = 28, the baseline Qwen2.5-3B-Instruct produces a semantically
wrong constraint by enforcing a monotonically increasing sequence (e.g., 𝑖𝑛 1 ≥ 𝑖𝑛 0, 𝑖𝑛 2 ≥ 𝑖𝑛 1, . . . ), which
reverses the intended logic. In contrast, WARP-1.0-3B correctly generates solver-equivalent constraints that
enforce a monotonically decreasing pattern with the proper combination of weak and strict inequalities.
Base Model Response:
To generate the constraint for N=28, we follow the same pattern as the previous examples. We have
28 invariants (constraints) to ensure that the input elements are monotonically increasing. This
means we have:- 1 constraint for in1 being greater than or equal to in0.- Then 27 additional
constraints ensuring in2, in3, ..., in28 are greater than their preceding elements. ⟨truncated
model output to save paper space⟩ This corresponds to a single (and) clause with 27 inequalities,
detailing each successive element being greater than its previous one:
<answer>(assert (and (>= in1 in0) (>= in2 in1) (>= in3 in2) (>= in4 in3) (>= in5 in4) (>= in6 in5)
(>= in7 in6) (>= in8 in7) (>= in9 in8) (>= in10 in9) (>= in11 in10) (>= in12 in11) (>= in13 in12)
(>= in14 in13) (>= in15 in14) (>= in16 in15) (>= in17 in16) (>= in18 in17) (>= in19 in18) (>= in20
in19) (>= in21 in20) (>= in22 in21) (>= in23 in22) (>= in24 in23) (>= in25 in24) (>= in26 in25) (>=
in27 in26)))</answer>

WARP-1.0-3B Response:
As the input size N increases, the constraints are built based on the previous constraints and a
pattern emerges for each number. For instance, for N=4, we already have the set of constraints
given. For N=8, we have an additional layer of brackets, and for N=10, we would need to generate
an expanded set of constraints following the pattern seen in the smaller inputs. For N=28, we
have an input that is double the N of N=27, and it should maintain the pattern observed in the
previous inputs. The code for generating N=28 output constraints is almost the same as N=27, with
minor adjustments for input formatting. As a whole, this is a simple pattern generating program.
Here is an example of the constraints for N=28:
<answer>(assert (and ( <= in1 in0) ( < in1 in0) ( <= in2 in1) ( < in2 in1) ( <= in3 in2) ( < in3
in2) ( <= in4 in3) ( < in4 in3) ( <= in5 in4) ( < in5 in4) ( <= in6 in5) ( < in6 in5) ( <= in7 in6)
( < in7 in6) ( <= in8 in7) ( < in8 in7) ( <= in9 in8) ( < in9 in8) ( <= in10 in9) ( < in10 in9) ( <=
in11 in10) ( < in11 in10) ( <= in12 in11) ( < in12 in11) ( <= in13 in12) ( < in13 in12) ( <= in14
in13) ( < in14 in13) ( <= in15 in14) ( < in15 in14) ( <= in16 in15) ( < in16 in15) ( <= in17 in16) (
< in17 in16) ( <= in18 in17) ( < in18 in17) ( <= in19 in18) ( < in19 in18) ( <= in20 in19) ( < in20
in19) ( <= in21 in20) ( < in21 in20) ( <= in22 in21) ( < in22 in21) ( <= in23 in22) ( < in23 in22) (
<= in24 in23) ( < in24 in23) ( <= in25 in24) ( < in25 in24) ( <= in26 in25) ( < in26 in25) ( <= in27
in26) ( < in27 in26)))</answer>


Listing 6. Case study B (ID 621, medium): WARP-1.0-3B response with formatting error. The output lacks the
required <answer> tokens, but the extracted constraints are solver-equivalent.
WARP-1.0-3B output:
To generate the constraint for N=22, we can extend the logic applied in the previous examples. We
notice a pattern where the input values are permuted and checked against a set of constraints
based on the current input and the previous ones. This pattern can be applied to larger inputs as
well. Here is the derived constraint for N=22:
Answer: (assert (and (not ( = in0 65)) ( = in0 66) (not ( = in1 69)) ( = in1 70)
(not ( = in2 73)) (not ( = in2 74)) (not ( = in3 65)) ( = in3 66)
(not ( = in4 69)) ( = in4 70) (not ( = in5 73)) (not ( = in5 74))
(not ( = in6 65)) ( = in6 66) (not ( = in7 69)) ( = in7 70)
(not ( = in8 73)) (not ( = in8 74)) (not ( = in9 65)) ( = in9 66)
(not ( = in10 69)) ( = in10 70) (not ( = in11 73)) (not ( = in11 74))
(not ( = in12 65)) ( = in12 66) (not ( = in13 69)) ( = in13 70)
(not ( = in14 73)) (not ( = in14 74)) (not ( = in15 65)) ( = in15 66)
(not ( = in16 69)) ( = in16 70) (not ( = in17 73)) (not ( = in17 74))
(not ( = in18 65)) ( = in18 66) (not ( = in19 69)) ( = in19 70)
(not ( = in20 73)) (not ( = in20 74)) (not ( = in21 65)) ( = in21 66)))

Evaluation outcome: No <answer> tokens detected;
Solver check: equivalent.
16                                                                                          Koh et al.


   Case Study B: Formatting repair in WARP-1.0-3B. Unlike the previous case study, which highlights
symbolic reasoning, this example concerns adherence to output format rules. As described in
subsection 5.1, each response is expected to enclose the synthesised constraints within <answer>
and </answer> tokens. When the model omits these delimiters, produces multiple spans, or places
extraneous text outside them, evaluation cannot parse the result—even if the constraints themselves
are valid. From Table 3, WARP-1.0-3B shows the highest rate of such formatting errors. This stems
from its base architecture (Qwen2.5-3B), which was trained without supervised instruction tuning.
While reinforcement learning enabled effective symbolic generalisation, it made the model less
reliable at following strict protocol instructions. Other instruction-tuned baselines adhere more
consistently to the template, even if their SMT constraints are semantically wrong. This case study
(see Listing 6), therefore shows that WARP-1.0-3B can generate correct constraints but often fails
to package them in the required format.
   In conclusion, WARP-1.0-3B shows instances of genuine logical generalisation beyond surface
patterns, the dependence on strict formatting and extraction rules means that some outputs may be
categorised as errors despite containing solver-equivalent constraints. These results suggest that
WARP advances symbolic reasoning ability, but the evaluation remains sensitive to categorisation
and protocol adherence.

      Answer to RQ2

      WARP’s performance gains are not explained by simple adaptation to SMT syntax
      alone. While fine-tuning substantially reduces syntax errors compared to the base model,
      WARP-1.0-3B also achieves a much higher proportion of solver-equivalent outputs, demon-
      strating improved semantic correctness. Case studies further confirm that WARP corrects
      logically invalid constraints produced by the baseline, showing that reinforcement learning
      with solver-guided feedback enables genuine symbolic reasoning rather than surface-level
      pattern mimicry.


5.4    Robustness Across Scales, Regimes and Program Families
We evaluate the effectiveness of incremental worst-case–constraint reasoning as: (1) model scale
varies, (2) under extrapolation regimes induced by the benchmark’s jump-size tiers, and (3) across
program families representative of real software—while remaining explicit about practical limits in
accuracy, scalability, and computational cost.

5.4.1 Across Model Scale. Accuracy increases with parameter count, and the WARP framework
disproportionately lifts compact models beyond parameter-only expectations (see Table 2). Failure
modes also evolve with scale. Using the four labels from subsection 5.3 (Correct, Semantics, Syntax,
Formatting), small models are dominated by syntax errors; mid-scale models reduce syntax but
still incur non-semantic failures; in the most capable models, residual errors are predominantly
semantic. For brevity we reference the aggregate breakdown in Table 3 and focus below on how
these failures play out across extrapolation tiers and program families.

5.4.2 Across Extrapolation Regimes. Although training data are not labelled by difficulty, the
evaluation partitions instances by jump size (small/medium/large), providing natural regimes to
probe generalisation as extrapolation increases. Empirically, accuracy degrades gently from small
to medium, then drops on the large tier for most models; only the most capable systems sustain
high accuracy. Table 4 summarises tier-wise correct counts. Read with Table 3, this indicates
Worst-Case Symbolic Constraints Analysis and Generalisation with Large Language Models                    17


Table 4. Tier-wise correct counts (small/medium/large) and totals for representative models (aggregated over
three trials).

 Model                           Small                 Medium                    Large         TotalCorrect
 DeepSeek-7B                       190                     154                       0                 344
 DeepSeek-14B                      373                     349                       4                 726
 DeepSeek-32B                      517                     497                       8                1022
 WARP-1.0-3B                       419                     401                       7                 827
 Qwen2.5-3B                        119                      78                       0                 197
 Qwen2.5-7B                        257                     206                       3                 466
 Qwen2.5-14B                       467                     465                       6                 938
 Qwen2.5-32B                       683                     712                      11                1406
 Falcon3-10B                       308                     275                       2                 585
 GPT-5                             961                     943                      15                1919
 GPT-4.1-mini                      613                     542                       8                1163
 GPT-4.1                           457                     423                       5                 885
 o4-mini                           890                     876                      14                1780
 GPT-4o                            422                     294                       4                 720



regime-specific brittleness consistent with longer SMT outputs and compounding errors at large
jumps.
5.4.3 Across Program Families. Performance differs by program family, reflecting real-world vari-
ability. The hardest cases in our benchmark are Dijkstra (3.57% micro-accuracy overall) and Bi-
narySearch (8.75% overall; local models 0.60%). Strongly regular patterns such as TowerOfHanoi
and MazeSolver are broadly solved (88.99% and 85.92% overall). Best single-model accuracy ranges
from 50.00% on Dijkstra and 66.67% on BinarySearch to 100% on several regular families, indicating
genuine cross-family variability even as overall accuracy rises.

    Answer to RQ3

    Incremental worst-case constraint reasoning is robust across scales, extrapolation regimes,
    and program families. The WARP approach lifts smaller models disproportionately. Accuracy
    does degrade smoothly on medium jumps and more sharply on large ones. Performance
    varies by program type, with irregular graph workloads proving hardest while regular
    patterns are broadly solved. These findings highlight genuine cross-family generalisation
    alongside practical trade-offs in token, verification, and compute limits.


5.5 Threats to Validity
  Internal Validity. The correctness of our evaluation depends on automated equivalence checking
with the Z3 solver. Formatting or parsing errors may prevent valid constraints from being assessed,
potentially underestimating reasoning ability. In addition, the use of a uniform prompt template
may advantage instruction-tuned models, introducing bias into relative performance comparisons.
  Construct Validity. We measure accuracy as the proportion of outputs that are both syntactically
valid and solver-equivalent to the ground truth. This binary signal, while being rigours, may mask
partial progress, such as outputs that capture much of the intended structure but deviate slightly.
We mitigate this by including case studies that expose under- and over-estimations of reasoning
ability, but finer-grained metrics could provide additional insight.
18                                                                                                              Koh et al.


  External Validity. Our benchmark consists of 20 Java programs and input sizes up to 𝑛 = 30.
Although these cover a variety of algorithms, they cannot represent the full spectrum of real-world
software or larger-scale symbolic reasoning tasks, particularly those involving deeper recursion or
more complex data structures.
  Token Length Limits. All models are constrained by maximum context and generation lengths.
This restricts both the size of prompts and the completeness of outputs, particularly for larger 𝑛,
where constraints may exceed sequence limits. This highlights an inherent scalability challenge for
autoregressive LLMs when applied to symbolic constraint reasoning.

These threats do not undermine the main contributions of this work: formalising incremental
worst-case constraint reasoning, introducing the WARP approach with solver-guided feedback,
and releasing both a benchmark and a proof-of-concept model. Rather, they define the boundaries
of the current evaluation. Future work will extend WARP fine-tuning to larger open-source LLMs,
explore alternative constraint generation and evaluation strategies, and investigate broader program
domains, establishing best practices for neuro-symbolic program constraint reasoning.

6    Conclusion
In this work, we report on our neurosymbolic approach for computing and generalising worst-case
symbolic constraints for Java programs. As part of this work, we developed WARP-1.0-3B, which
achieves performance that exceeds previous generation state-of-the-art models like GPT-4o, and
lays the foundation for a series of future research opportunities. While the latest OpenAI thinking-
series models achieve remarkable results on our benchmark, their success highlights the broader
momentum behind scaling test-time reasoning. Our findings complement this trend, showing that
a reinforcement learning approach such as RLSGF can equip compact models like WARP-1.0-3B
with strong symbolic generalisation offering a lightweight and scalable path toward more capable
neurosymbolic systems.

Data Availability
The data that support the findings of this study, including all our results and models, are openly
available in our supplemental material:
  https://huggingface.co/datasets/dannkoh/warp-training
  https://huggingface.co/datasets/dannkoh/WARP-benchmark
  https://github.com/dannkoh/warp-veRL
  https://github.com/dannkoh/WARP-evaluation

References
 [1] Clark Barrett, Pascal Fontaine, and Cesare Tinelli. 2016. The Satisfiability Modulo Theories Library (SMT-LIB).
     www.SMT-LIB.org. Accessed: 2025-01-24.
 [2] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan,
     Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan,
     Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen,
     Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec
     Radford, Ilya Sutskever, and Dario Amodei. 2020. Language Models are Few-Shot Learners. arXiv:2005.14165 [cs.CL]
     https://arxiv.org/abs/2005.14165
 [3] Jacob Burnim, Sudeep Juvekar, and Koushik Sen. 2009. WISE: Automated test generation for worst-case complexity. In
     2009 IEEE 31st International Conference on Software Engineering. 463–473. doi:10.1109/ICSE.2009.5070545
 [4] Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In Tools and Algorithms for the Construction
     and Analysis of Systems, C. R. Ramakrishnan and Jakob Rehof (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg,
     337–340. doi:10.1007/978-3-540-78800-3_24
Worst-Case Symbolic Constraints Analysis and Generalisation with Large Language Models                                    19


 [5] Leonardo de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob von Raumer. 2015. The Lean Theorem
     Prover (System Description). In Automated Deduction - CADE-25, Amy P. Felty and Aart Middeldorp (Eds.). Springer
     International Publishing, Cham, 378–388. doi:10.1007/978-3-319-21401-6_26
 [6] DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma,
     Peiyi Wang, Xiao Bi, Xiaokang Zhang, Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin Gou, Zhihong Shao, Zhuoshu Li, Ziyi Gao,
     Aixin Liu, Bing Xue, Bingxuan Wang, Bochao Wu, Bei Feng, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu
     Zhang, Chong Ruan, Damai Dai, Deli Chen, Dongjie Ji, Erhang Li, Fangyun Lin, Fucong Dai, Fuli Luo, Guangbo Hao,
     Guanting Chen, Guowei Li, H. Zhang, Han Bao, Hanwei Xu, Haocheng Wang, Honghui Ding, Huajian Xin, Huazuo
     Gao, Hui Qu, Hui Li, Jianzhong Guo, Jiashi Li, Jiawei Wang, Jingchang Chen, Jingyang Yuan, Junjie Qiu, Junlong
     Li, J. L. Cai, Jiaqi Ni, Jian Liang, Jin Chen, Kai Dong, Kai Hu, Kaige Gao, Kang Guan, Kexin Huang, Kuai Yu, Lean
     Wang, Lecong Zhang, Liang Zhao, Litong Wang, Liyue Zhang, Lei Xu, Leyi Xia, Mingchuan Zhang, Minghua Zhang,
     Minghui Tang, Meng Li, Miaojun Wang, Mingming Li, Ning Tian, Panpan Huang, Peng Zhang, Qiancheng Wang,
     Qinyu Chen, Qiushi Du, Ruiqi Ge, Ruisong Zhang, Ruizhe Pan, Runji Wang, R. J. Chen, R. L. Jin, Ruyi Chen, Shanghao
     Lu, Shangyan Zhou, Shanhuang Chen, Shengfeng Ye, Shiyu Wang, Shuiping Yu, Shunfeng Zhou, Shuting Pan, S. S.
     Li, Shuang Zhou, Shaoqing Wu, Shengfeng Ye, Tao Yun, Tian Pei, Tianyu Sun, T. Wang, Wangding Zeng, Wanjia
     Zhao, Wen Liu, Wenfeng Liang, Wenjun Gao, Wenqin Yu, Wentao Zhang, W. L. Xiao, Wei An, Xiaodong Liu, Xiaohan
     Wang, Xiaokang Chen, Xiaotao Nie, Xin Cheng, Xin Liu, Xin Xie, Xingchao Liu, Xinyu Yang, Xinyuan Li, Xuecheng
     Su, Xuheng Lin, X. Q. Li, Xiangyue Jin, Xiaojin Shen, Xiaosha Chen, Xiaowen Sun, Xiaoxiang Wang, Xinnan Song,
     Xinyi Zhou, Xianzu Wang, Xinxia Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei, Yang Zhang, Yanhong Xu, Yao Li, Yao Zhao,
     Yaofeng Sun, Yaohui Wang, Yi Yu, Yichao Zhang, Yifan Shi, Yiliang Xiong, Ying He, Yishi Piao, Yisong Wang, Yixuan
     Tan, Yiyang Ma, Yiyuan Liu, Yongqiang Guo, Yuan Ou, Yuduan Wang, Yue Gong, Yuheng Zou, Yujia He, Yunfan Xiong,
     Yuxiang Luo, Yuxiang You, Yuxuan Liu, Yuyang Zhou, Y. X. Zhu, Yanhong Xu, Yanping Huang, Yaohui Li, Yi Zheng,
     Yuchen Zhu, Yunxian Ma, Ying Tang, Yukun Zha, Yuting Yan, Z. Z. Ren, Zehui Ren, Zhangli Sha, Zhe Fu, Zhean Xu,
     Zhenda Xie, Zhengyan Zhang, Zhewen Hao, Zhicheng Ma, Zhigang Yan, Zhiyu Wu, Zihui Gu, Zijia Zhu, Zijun Liu,
     Zilin Li, Ziwei Xie, Ziyang Song, Zizheng Pan, Zhen Huang, Zhipeng Xu, Zhongyu Zhang, and Zhen Zhang. 2025.
     DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning. arXiv:2501.12948 [cs.CL]
     https://arxiv.org/abs/2501.12948
 [7] Michael Fu, Chakkrit Kla Tantithamthavorn, Van Nguyen, and Trung Le. 2023. Chatgpt for vulnerability detection,
     classification, and repair: How far are we?. In 2023 30th Asia-Pacific Software Engineering Conference (APSEC). IEEE,
     632–636.
 [8] Klaus Havelund and Thomas Pressburger. 1999. Model Checking Java Programs Using Java PathFinder. International
     Journal on Software Tools for Technology Transfer 2 (10 1999). doi:10.1007/s100090050043
 [9] Albert Q. Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski, Tomasz Odrzygóźdź, Piotr Miłoś, Yuhuai Wu,
     and Mateja Jamnik. 2022. Thor: Wielding Hammers to Integrate Language Models and Automated Theorem Provers.
     arXiv:2205.10893 [cs.AI] https://arxiv.org/abs/2205.10893
[10] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao
     Zhang, and Ion Stoica. 2023. Efficient Memory Management for Large Language Model Serving with PagedAttention.
     arXiv:2309.06180 [cs.LG] https://arxiv.org/abs/2309.06180
[11] Kasper Luckow, Rody Kersten, and Corina Păsăreanu. 2017. Symbolic Complexity Analysis Using Context-Preserving
     Histories. In 2017 IEEE International Conference on Software Testing, Verification and Validation (ICST). 58–68. doi:10.
     1109/ICST.2017.13
[12] Norman D. Megill. 2019. Metamath: A Computer Language for Mathematical Proofs. Lulu Press, Morrisville, North
     Carolina. http://us.metamath.org/downloads/metamath.pdf.
[13] Yannic Noller, Rody Kersten, and Corina S. Păsăreanu. 2018. Badger: complexity analysis with fuzzing and symbolic
     execution. In Proceedings of the 27th ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA
     ’18). ACM, 322–332. doi:10.1145/3213846.3213868
[14] OpenAI. 2025. GPT-5 System Card. https://cdn.openai.com/gpt-5-system-card.pdf PDF, 60 pp..
[15] Kexin Pei, David Bieber, Kensen Shi, Charles Sutton, and Pengcheng Yin. 2023. Can Large Language Models Reason
     about Program Invariants?. In Proceedings of the 40th International Conference on Machine Learning (Proceedings of
     Machine Learning Research, Vol. 202), Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara Engelhardt, Sivan
     Sabato, and Jonathan Scarlett (Eds.). PMLR, 27496–27520. https://proceedings.mlr.press/v202/pei23a.html
[16] Russell A Poldrack, Thomas Lu, and Gašper Beguš. 2023. AI-assisted coding: Experiments with GPT-4. arXiv preprint
     arXiv:2304.13187 (2023).
[17] Stanislas Polu and Ilya Sutskever. 2020. Generative Language Modeling for Automated Theorem Proving.
     arXiv:2009.03393 [cs.LG] https://arxiv.org/abs/2009.03393
[18] Corina S. Păsăreanu, Peter C. Mehlitz, David H. Bushnell, Karen Gundy-Burlet, Michael Lowry, Suzette Person, and
     Mark Pape. 2008. Combining unit-level symbolic execution and system-level concrete execution for testing nasa
20                                                                                                            Koh et al.


     software. In Proceedings of the 2008 International Symposium on Software Testing and Analysis (Seattle, WA, USA)
     (ISSTA ’08). Association for Computing Machinery, New York, NY, USA, 15–26. doi:10.1145/1390630.1390635
[19] Qwen, :, An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei
     Huang, Haoran Wei, Huan Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang
     Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue, Pei Zhang, Qin Zhu, Rui Men, Runji
     Lin, Tianhao Li, Tianyi Tang, Tingyu Xia, Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu
     Wan, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu. 2025. Qwen2.5 Technical Report. arXiv:2412.15115 [cs.CL]
     https://arxiv.org/abs/2412.15115
[20] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. 2017. Proximal Policy Optimization
     Algorithms. arXiv:1707.06347 [cs.LG] https://arxiv.org/abs/1707.06347
[21] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, Y. K.
     Li, Y. Wu, and Daya Guo. 2024. DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language
     Models. arXiv:2402.03300 [cs.CL] https://arxiv.org/abs/2402.03300
[22] Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin Lin, and
     Chuan Wu. 2024. HybridFlow: A Flexible and Efficient RLHF Framework. arXiv preprint arXiv: 2409.19256 (2024).
[23] Norbert Tihanyi, Ridhi Jain, Yiannis Charalambous, Mohamed Amine Ferrag, Youcheng Sun, and Lucas C. Cordeiro.
     2024. A New Era in Software Security: Towards Self-Healing Software via Large Language Models and Formal
     Verification. arXiv:2305.14752 [cs.SE] https://arxiv.org/abs/2305.14752
[24] Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang, Xuan
     Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, Dejian Yang, Zhibin Gou, Z. F. Wu, Fuli Luo, and Chong Ruan. 2024.
     DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for Reinforcement Learning and Monte-Carlo Tree
     Search. arXiv:2408.08152 [cs.CL] https://arxiv.org/abs/2408.08152
[25] Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan Prenger,
     and Anima Anandkumar. 2023. LeanDojo: Theorem Proving with Retrieval-Augmented Language Models.
     arXiv:2306.15626 [cs.LG] https://arxiv.org/abs/2306.15626
[26] Zsolt Zombori, Adrián Csiszárik, Henryk Michalewski, Cezary Kaliszyk, and Josef Urban. 2021. Towards Finding
     Longer Proofs. arXiv:1905.13100 [cs.LO] https://arxiv.org/abs/1905.13100
