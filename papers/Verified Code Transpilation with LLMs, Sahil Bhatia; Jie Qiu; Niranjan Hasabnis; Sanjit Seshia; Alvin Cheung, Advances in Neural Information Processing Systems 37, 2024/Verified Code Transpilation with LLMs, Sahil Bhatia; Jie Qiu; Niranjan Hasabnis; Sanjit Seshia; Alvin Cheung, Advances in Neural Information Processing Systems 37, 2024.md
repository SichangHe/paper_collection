                                                      Verified Code Transpilation with LLMs


                                                   Sahil Bhatia                     Jie Qiu                    Niranjan Hasabnis
                                                   UC Berkeley                      Duolingo                       Intel Labs
                                            sahilbhatia@berkeley.edu           jieq@berkeley.edu          niranjan.hasabnis@intel.com

                                                           Sanjit A. Seshia                               Alvin Cheung
arXiv:2406.03003v1 [cs.PL] 5 Jun 2024




                                                             UC Berkeley                                  UC Berkeley
                                                        sseshia@berkeley.edu                         akcheung@berkeley.edu



                                                                                      Abstract
                                                 Domain-specific languages (DSLs) are integral to various software workflows.
                                                 Such languages offer domain-specific optimizations and abstractions that improve
                                                 code readability and maintainability. However, leveraging these languages requires
                                                 developers to rewrite existing code using the specific DSL’s API. While large
                                                 language models (LLMs) have shown some success in automatic code transpilation,
                                                 none of them provide any functional correctness guarantees on the transpiled
                                                 code. Another approach for automating this task is verified lifting, which relies
                                                 on program synthesis to find programs in the target language that are functionally
                                                 equivalent to the source language program. While several verified lifting tools have
                                                 been developed for various application domains, they are specialized for specific
                                                 source-target languages or require significant expertise in domain knowledge to
                                                 make the search efficient. In this paper, leveraging recent advances in LLMs, we
                                                 propose an LLM-based approach (LLML IFT) to building verified lifting tools. We
                                                 use the LLM’s capabilities to reason about programs to translate a given program
                                                 into its corresponding equivalent in the target language. Additionally, we use LLMs
                                                 to generate proofs for functional equivalence. We develop lifting-based compilers
                                                 for four different DSLs targeting different application domains. Our approach not
                                                 only outperforms previous symbolic-based tools in both the number of benchmarks
                                                 transpiled and transpilation time, but also requires significantly less effort to build.


                                        1    Introduction
                                        Domain-specific languages (DSLs) have gained popularity due to their ability to provide optimiza-
                                        tions and abstractions that enhance code readability and improve performance in specific domains.
                                        Examples of recent DSLs include Spark (distributed computing), NumPy (array processing), TACO
                                        (tensor processing), and P4 (network packet processing). With new DSLs emerging for diverse appli-
                                        cation domains and programming languages, developers often face the task of manually rewriting
                                        existing code to incorporate these languages into their existing workflows. This manual rewriting
                                        process can be tedious, may introduce bugs into the code, and may fail to preserve the semantics of
                                        the starting code. This problem of transforming and compiling code from one programming language
                                        to another is called transpilation. The question we address in this paper is: can large language models
                                        (LLMs) correctly and automatically perform code transpilation?
                                        A particularly useful form of code transpilation, termed lifting, involves translating code in a somewhat
                                        lower-level, general-purpose language to equivalent code in a DSL. Lifting allows developers to
                                        port code to DSLs from which efficient code can be generated for special-purpose hardware, such
                                        as GPUs, machine learning accelerators, or network processors. Therefore, significant effort has
                                        been dedicated to developing tools aimed at automating the task of lifting. Rule-based approaches

                                        Preprint. Under review.
rely on traditional pattern-matching techniques Radoi et al. [2014]; however, describing these rules
can be a complex, human-intensive task. An alternative are search-based techniques that leverage
advances in program synthesis (e.g., see Solar-Lezama et al. [2006], Jha et al. [2010], Gulwani et al.
[2017]) and formal verification over the last two decades. The use of verified program synthesis for
lifting, termed verified lifting, involves searching for a program in the DSL and subsequently formally
verifying its semantic equivalence to the source program. Verified lifting has been successfully
applied in building compilers [Ahmad and Cheung, 2018, Magalhães et al., 2023, Cheung et al.,
2013, Ahmad et al., 2019] for DSLs like Spark, SQL, Halide, and TACO. Contemporary program
synthesis approaches can be broadly classified into two categories: symbolic and neural. Traditionally,
symbolic techniques such as enumerative, deductive, and constraint-based synthesis strategies have
been used for implementing the search. More recently, neural networks Mariano et al. [2022] have
been trained and leveraged to accelerate the search process. Despite their successes, both symbolic
and neural approaches have common drawbacks: 1) The synthesizer is customized for each DSL,
making them challenging to adapt for new DSLs, and 2) Significant effort is required to design
the synthesizer, including domain-specific heuristics for symbolic approaches and the generation of
parallel corpora ⟨source, target⟩ for ML-based approaches, to enable generalization and scalability
for the target DSL.
Large Language Models (LLMs) Devlin et al. [2019], Brown et al. [2020] have emerged as a promising
approach for tackling complex programming tasks, including code generation, repair, and testing.
However, generating reliable code with formal correctness guarantees with LLMs remains challenging.
Most work on LLMs either focuses on generating code without correctness guarantees [Li et al.,
2023, 2022, Rozière et al., 2024] or separately on producing proof annotations (such as invariants) for
given code Pei et al. [2023], Chakraborty et al. [2023]. Additionally, formal verification tools often
have their own specialized languages (e.g., SMT-LIB, Dafny) for encoding verification problems and
specifications. These languages are typically low-resource in the training datasets of LLMs, making
it challenging for the models to generate code in these formal verification languages directly. To
leverage LLMs for building VL compilers, we must address two key constraints: generalization to
new DSLs and providing correctness guarantees for the generated code.
In this work, we investigate the use of LLMs for verified lifting (VL). Our approach, called LLML IFT,
takes inspiration from the core technique of VL, which involves translating the source program to
a higher-level intermediate representation (IR) that describes the semantics of the DSL operators.
Once the synthesized code is verified, it is then translated to the concrete syntax of the DSL using
rewrite rules. We leverage the reasoning capabilities of LLMs to translate code from context to an IR.
We instruct the model via a prompt to generate code using the operators of the DSL, with Python
serving as the IR to encode the semantics of these operators. Python’s significant representation in
the training datasets of LLMs makes it a suitable choice for this purpose. In addition to generating
the DSL program, we also prompt the model to generate a proof of correctness for the program. To
the best of our knowledge, our approach is the first to leverage LLMs to generate both code and
proof annotations together. To verify the functional equivalence of the generated program to the
given source program for all program states, we translate both the generated program and the proof
to the syntax of an automated theorem prover. This step ensures that the synthesized code is formally
verified and can be trusted to be correct. Our evaluation (section Sec. 3) shows that LLML IFT
has significant advantages over traditional search-based symbolic VL-based tools. It solves 7 more
benchmarks, requires substantially less effort in terms of LoC (1000×), and is faster in generating
verified code and proofs (6× on average) .
In summary, this paper makes the following novel contributions
1. We introduce the first technique for formally-verified code transpilation using LLMs.
2. Our approach uses Python as an IR for code generation, thus eliminating the need for specialized
   DSL-specific training data or fine-tuning of LLMs.
3. Our method eliminates the need for manual encoding of domain-specific heuristics, thus simplify-
   ing the process of verified lifting by reducing the human effort required in traditional techniques.
4. We propose an approach to generate not only the lifted code but also a proof of correctness for the
   generated code. This integration of LLMs with verification oracles guarantees the correctness of
   the generated code, a crucial aspect that sets our approach apart from other work on LLM-based
   code generation.




                                                  2
                                                          1   def map(data,f):
                                                          2     if len(data) == 0: return []
 1   public class ConditionalSum {                        3     else:
 2     public static int sumList(List<Integer> data) {    4       return [f(data[0])] + map(data[1:], f)
 3       int sum = 0;                                     5
 4       for (int i = 0; i < data.size(); i++) {          6   def reduce(data,f):
 5         int var = data.get(i);                         7     if len(data) == 0: return 0
 6         if (var < 100)                                 8     else:
 7           sum += var;                                  9       return f(data[0], reduce(data[1:], f))
 8       }                                               10
 9       return sum;                                     11   def ite(a, b, cond):
10     }                                                 12     if cond: return a
11   }                                                   13     else: return b


                   (a) Source Code (S)                         (b) Target Language (Tlang )
                  Figure 1: Sequential source code in Java and semantics of DSL in IR

5. We show the effectiveness of our approach (Sec. 4) by constructing compilers for four DSLs
   spanning various application domains. In terms of accuracy, our LLM-based compilers achieve
   comparable performance to existing tools and, in some domains, outperforms the prior approaches.

2     Background

We now give an overview and an end-to-end example of verified lifting (VL) where we use program
synthesis to build a compiler. Given a program (S) in the source language (Slang ), VL uses a search
procedure to find a program (T) in the target language (Tlang ) that can be proved to be functionally
equivalent to the given source program.
VL comprises of three phases: 1) Search, 2) Verification, and 3) Code generation. The key behind
VL is to first transpile S to an user-defined intermediate representation (IR) of the operators in the
target language before generating executable code. The IR serves as a functional description of
Tlang and ignores any implementation details. Hence, during search phase, S is lifted to a sequence
of operators expressed using the IR. This expression serves as the program summary (PS) which
summarizes S using the IR. Subsequently, PS is verified using a theorem prover to check for semantic
equivalence with S for all program inputs. If verification succeeds, PS is then translated into the
concrete syntax of the target language using simple pattern-matching rules provided by the user to
generate executable code. These rules are notably simpler to write compared to a rule-based translator
that directly compiles from Slang to Tlang , as the PS is already expressed using the operators in the
target language.
We demonstrate an example of transpiling a sequential Java program to Spark using VL. Spark
provides a high-level API for large-scale distributed data computation. Two key higher-order functions
in Spark’s API are map and reduce: map applies a given function to each element of a distributed
dataset and creates a new dataset, while reduce combines the elements of a dataset using a specified
associative binary operator, such as summing across the entire dataset.
Fig. 1a shows a sequential source program (S). The given S takes a list of integers as input and
calculates the sum of all integers in the list that are less than 100. In Fig. 1b, we define the semantics
of the map and reduce operators from Spark in Python (the IR). These functions abstract the
implementation details of the operators while only capturing the high-level semantics of the operators.
Our goal is to find an IR expression sequence of map and reduce such that it is semantically equivalent
to S. Traditional approaches to solving this search problem in VL involve framing it as SyGuS Alur
et al. [2013] problem. SyGuS is an approach for solving program synthesis problems by specifying
constraints and searching for solutions within a defined space. Specifically, a SyGuS problem involves
defining a search space that syntactically restricts the space of possible solutions, thereby making the
search tractable. Formally, this objective can be stated as ∃ T ∈ Tlang | ∀ σ. S(σ) = T (σ), where
T is a program in the target language. For our program in Fig. 1a, the synthesis phase would return
the following PS (i.e., T ):
     reduce(map(data, lambda i : ite(i < 100, i, 0)), lambda a, b: a + b)

The expression initially maps each element in data to either i or 0 based on whether the element i
is less than 100 or not. Next, it reduces the resulting list by summing up all the elements to return


                                                         3
Figure 2: A high-level overview of our LLML IFT framework for building verified lifting-based tools.


the sum of elements less than 100. Since S contains a loop, proving equivalence with the generated
program requires another predicate called the “loop invariant.” A loop invariant is a logical statement
that must hold before and after each iteration of a loop. Intuitively, it captures the essential properties
that are preserved while the loop executes. During VL’s synthesis phase, we generate both the
program summary and any required loop invariant for verification. Verification is done by sending the
program summary and loop invariant(s) to a theorem prover. Verifier checks the semantic equivalence
between S and the generated program program summaries.
VL currently uses cvc5 and z3 for this purpose.
Once verified, we translate the generated program summary to the concrete syntax of the DSL (Spark)
using simple pattern-matching rules, resulting in the following executable code:
      map(lambda i: i if i < 100 else 0).reduce(lambda a, b: a + b)

We next describe our LLM-based approach can improve the efficiency and scalability of VL’s
synthesis problem.

3     LLM-Based Verified Lifting
We now describe our LLM-based approach for verified lifting. We begin by formalizing VL. Then
we give details of how we use LLMs to improve over the classical verified lifting approach.

3.1    Problem Formulation

VL’s search problem is characterized by three components:
1. Specification (ϕ): The specification (ϕ) defines the property that the target program (T) should
   satisfy. For VL considered in this paper, source and target programs are side-effect free functions
   of their inputs. Thus, ϕ encodes the semantic equivalence of T to the source program (S) for each
   program input state σ. The overall correctness condition is:
                                                    .
                                    ∀σ ϕ(σ, T, S) = ∀ σ. S(σ) = T(σ)                                  (1)
2. Program Space (G): The program space outlines the set of potential solutions, typically expressed
   as a context-free grammar G. The language of G includes all sequences of operators ops ∈ Tlang
   applied recursively to terms starting with input variables σ. A target program T as a program
   summary PS that is a composition of operators ops. An example involving the map and reduce
   operators is provided in the previous section. In other words, all values returned by S must be
   expressed using a combination of operators (ops) from Tlang .
3. Search Algorithm (A): This refers to the algorithm used to solve the synthesis problem. Tra-
   ditional symbolic program synthesis solvers utilize enumerative search, deductive search, and
   constraint-based approaches Gulwani et al. [2017]. Part of the synthesis problem is to generate
   the invariants Inv that a verifier can use to prove that ϕ holds. Synthesis tools typically also use a
   grammar GI to constrain the space of possible invariants to search over.
In summary, with the target program T represented as the combination (PS,Inv), we define the search
problem in VL as:
                             ∃ PS ∈ G ∃Inv ∈ GI ∀σ . ϕ(σ, PS,Inv, S)                               (2)
This states that we aim to find a program summary (PS) and invariants (Inv) from the defined search
space G, GI , using the search algorithm A, such that the given specification (functional equivalence
with S) holds for all possible program states.


                                                    4
      Figure 3: End-to-End Lifting Example                                Figure 4: Prompt Structure


3.2    LLM-based Verified Lifting

Traditional approaches to solving the VL search problem rely on symbolic search and manually
designed heuristics to make the search effective. Unfortunately doing so is resource intensive and
requires domain-specific knowledge. We explore a new approach by leveraging LLMs.
A naive approach to building a VL-based compiler using LLMs would be to prompt LLMs to translate
Slang programs directly into Tlang . However, this approach has the following shortcomings:
1. VL-based compilers require that the Tlang candidates generated during the search phase be
   functionally equivalent to the input Slang program. This is a strong requirement that current LLMs
   are unable to satisfy.
2. Contarary to general purpose languages (such as Python), domain-specific languages (DSLs) are
   not widely used. Unsurprisingly, we find that LLMs struggle to generate code in languages that
   are insufficiently represented in their training data.
Fig. 3 shows an example of instructing GPT-3.5 to translate code in an end-to-end manner. We
instruct the model to translate a C++ function to TACO (a tensor processing DSL) Kjolstad et al.
[2017], and the model fails to generated the expected einsum representation. Instead, the model
outputs a completely incorrect solution by hallucinating non-existent TACO functions. This problem
is even more prominent for new DSLs that the model might have never seen in the training dataset.
To address these challenges, we leverage VL’s key idea of transpiling to an IR rather than directly
to the concrete syntax of Tlang . Specifically, we observe that Python is one of the well-represented
programming languages in the training dataset of popular LLMs Li et al. [2023], and, consequentially,
these LLMs understand semantics of Python programs well. We exploit these observations by
leveraging Python as the IR to define semantics of DSL operators, an example is shown in Fig. 1b.
In Fig. 2, we show our LLM-based approach where we apply LLMs to generate the program
summaries and invariants in the IR. Each generated summary is then checked for correctness using a
program verifier. After verification, we convert the program summaries into the concrete syntax of
Tlang through simple pattern-matching rules as in traditional VL. Our approach uses LLMs with a
few-shot learning framework that we describe next.

3.3    Few-Shot Learning Approach

LLMs have demonstrated few-shot reasoning capabilities Brown et al. [2020]. Few-shot reasoning
allows LLMs to generalize their understanding to new tasks by leveraging a small set of similar
examples. This allows them to extend their reasoning capabilities to tasks without requiring explicit
training or fine-tuning for those specific tasks. We propose leveraging the few-shot reasoning
capabilities of LLMs for verified lifting as fine-tuning existing LLMs for each new DSL is often
infeasible due to the lack of extensive training data and the rapid pace at which new DSLs are
developed. The effort required to collect, annotate, and preprocess DSL-specific training data for
fine-tuning can be substantial, making it impractical to adapt LLMs to each new DSL.
As described in Sec. 2, VL generates candidates in an IR that abstracts away low-level implementation
details of the operators in Tlang . The objective, as defined in Eq. (2), is to find PS and Inv expressed
using operators from Tlang such that ϕ holds. We leverage the few-shot reasoning capability by
providing the models with the semantics of operators from the target language (Tlang ) using an IR.
By exposing the LLMs to these semantics, we enable them to use their reasoning capabilities over
code to generate both the PS and invariants in the IR.


                                                   5
In Fig. 4, we illustrate the high-level prompt structure we use to generate the PS and Invs. The prompt
consists of the following components:
1. Task Instruction. We instruct the model using a natural language to translate S using only the
   specified DSL operators.
2. DSL Operators. We specify the semantics of all operators from Tlang using Python and include
   it in the prompt. Python is chosen as our IR due to (a) its widespread use across domains, (b) its
   concise and expressive nature, making the representation readable and straightforward and, (c) its
   significant representation in code datasets used for training LLMs Li et al. [2023].
3. Specification. While symbolic techniques often rely on approaches like test cases, bounded
   model checking, and Hoare logic Hoare [1969] for defining specifications, the natural language
   interface of LLMs offers flexibility in using various specifications and combining different forms.
   Given that LLMs are primarily trained on raw source code and may not have encountered other
   forms of specification during training, we directly use the source program (S) as the specification
   in our prompt.
We split the generation of PS and Inv into a two-phase process by first asking the LLM to generate
the PS and then inferring invariants corresponding to it. For generating PS we use zero-shot setting
while for Inv(s) we use one-shot prompt.Due to space constraints, we show an instantiation of the
prompt structure shown in Fig. 4 in Appendix B. When prompted, the model generates the following
PS for our example code shown in Fig. 1a:

   reduce(map(data, lambda i : ite(i < 100, i, 0)), lambda a, b: a + b)

To ensure that the generated candidates follow the DSL operators defined in the prompt, we use a
parser to reject candidates which do not satisfy this constraint.
Next, if S contains loops, establishing the functional equivalence of the generated PS for all program
states with S requires loop invariants. In VL, loop invariants typically follow a templated structure:

                                      Inv ≜ f (i) ∧ e(Tlang )                                       (3)

where f (i) denotes an expression over loop indexes and e(Tlang ) represents an expression recursively
constructed using operators from Tlang . This structured nature simplifies the invariant generation
process compared to solving general loop invariant synthesis problems. To facilitate the generation
of loop invariants, we use 1-shot learning to familiarize the model with the concept and structure
of invariants in the VL context (due to space constraints we illustrate in Appendix B). The prompt
for invariant generation closely resembles that used for generating program summaries, including S
with an additional assertion stating the equality of the return variable with the previously generated
PS. This instruction guides the model to produce an invariant corresponding to the generated PS.
The invariants are generated as Boolean expressions in Python rather than SMT-LIB, as we found
that LLMs encounter difficulties in generating SMT-LIB (standard format for SMT-based theorem
provers) code due to its limited representation in training datasets. When prompted, model generates
the following invariant for the code shown in Fig. 1a:

   def invariant(data, i):
     return i >= 0 and i <= len(data) and
           sum = reduce(map(data[:i], lambda i : ite(i < 100, i, 0)),
                        lambda a, b: a + b)


The loop invariant states that the loop index i remains within the bounds of the data array (0 ≤ i ≤
len(data)). Additionally, the invariant expresses sum as the MapReduce expression over the first i
elements of the data array, which helps prove that the invariant holds in each iteration of the loop.
Both the program summaries and invariants are expressed in Python. We use simple pattern-matching
rewrite rules to translate the expressions to the syntax compatible with the verification oracle used
to check for functional equivalence. Once verified, the PS is similarly translated to the concrete
syntax of Tlang using straightforward rewrite rules, leveraging the syntactic nature of Python. The
translation process is simplified due to Python’s highly structured syntax. We present our complete
algorithm for generating PS and Inv in Appendix A.


                                                  6
4         Experiments
To evaluate the effectiveness of LLML IFT, we evaluate across four distinct DSLs1 , each targeting
diverse application domains:
1. Distributed Computing: We transpile sequential Java programs into MapReduce implementa-
   tions written using the Apache Spark Zaharia et al. [2012] API. Spark, an open-source distributed
   computing framework, provides an interface for programming multiple clusters which for data
   parallelism which helps in large-scale data processing.
2. Network Packet Processing: We transpile sequential network processing algorithms in C to
   the operators of programmable switch devices Sivaraman et al. [2016] with its own ISA. This
   translation enables the exploration of novel algorithms, such as congestion control and load
   balancing, on programmable switch devices.
3. TACO: We transpile sequential C++ programs into TACO Kjolstad et al. [2017]’s API. Taco is
   a tensor processing compiler for generating highly optimized GPU code for performing tensor
   computations.
4. Tensor Processing. We transpile sequential C++ programs to a tensor processing IR recently
   introduced by Qiu et al. [2024]. The tensor processing IR consists of common tensor operations
   such as element wise arithmetic operators, reduction operators and traspose, among others. This
   IR facilitates translation of unoptimized sequential code to tensor operations which can be then
   executed on 6 different software and hardware backends.
Model: In all experiments, we use GPT-4 via their APIs to generate candidates. We set the temperature
to 0.7 for all the experiments. For program summary and invariant generation across all domains, we
use the same zero-shot PS prompt in Fig. 5 and one-shot prompt in Fig. 6, respectively. We keep a
budget of 50 queries for the PS and a budget of 10 queries for each PS.
We present the results in the sections below and defer the error analysis to Appendix D.

4.1       Distributed Computing

MapReduce, a programming model for parallel processing of large datasets across distributed clusters,
simplifies parallel computation by abstracting away distributed system complexities. It comprises two
phases: 1. Map: Input data is partitioned into smaller chunks, each processed by a mapper function to
generate key-value pairs. 2. Reduce: Intermediate key-value pairs are shuffled, sorted based on keys,
and then processed by reducer functions to aggregate associated values.
LLML IFT implementation. We compare the performance of LLML IFT against MetaLift Bhatia
et al. [2023]2 . MetaLift uses a symbolic solver (Rosette Torlak and Bodik [2013]) to perform the
search. We evaluate on the same 45 benchmarks as MetaLift. All the benchmarks have loops and
require loop invariants to prove the functional equivalence of the source and the generated program.
MetaLift solves 40 out of 45 with a timeout of 1 hour. LLML IFT is able to solve 44, i.e., generate
the correct translation as well as the required invariants to prove the correctness. LLML IFT solves
4 additional benchmarks on which MetaLift times out. In addition to solving more benchmarks,
LLML IFT solves them much faster. It takes less than 1 minute on average to solve each benchmark
when MetaLift has to take an average of 3 minutes to solve. The amount of effort required to build
LLML IFT is alo significantly less than MetaLift as it does not require the developers to provide any
search-space description for PS and invariants. Metalift requires over ≈ 1000 LoC for the description
of these search-space.

4.2       Network Packet Processing

Network packet processing hardware, such as routers and switches, lacks flexibility post-development,
preventing experimentation with new data-plane algorithms. Recently, a verified lifting approach
Sivaraman et al. [2016] was introduced to simplify this process. This compiler offers the developers
with two constructs: 1. a packet transaction language (subset of the C language) to express the
semantics of these data-plane algorithms 2. a compiler Sivaraman et al. [2016] that translates the
      1
     All the benchmarks used for evaluation can be found at: https://drive.google.com/drive/folders/1vyxlREe8-
gJ1BJviDN5tqMectwYMmcOr?usp=sharing
   2
     Casper Ahmad and Cheung [2018] is not functional and Mold Radoi et al. [2014] is not open-sourced


                                                      7
packet processing algorithms to the instruction set of programmable switch devices. Atoms are
introduced as an instruction set of the hardware to represent the atomic operations supported by the
hardware. Compiler translates the packet transaction algorithm to a sequence of atoms resulting in a
different programmable switch configuration.
LLML IFT implementation. We implement the Domino compiler using LLML IFT by defining the
semantics of the atoms in the prompt. We compare the performance of our implementation against
MetaLift’s implementation. All benchmarks in Domino are imperative C programs without any loop
constructs, so no loop invariants are required for these benchmarks. The generated PS are verified
using a SMT solver. MetaLift solves all the 10 benchmarks with an average time of 6 seconds.
LLML IFT is also able to transpile all the 10 benchmarks but with an average time of only 2 seconds.
Similar to the Spark case study, we do not require developers to specify the search-space for PS while
Metalift requires over ≈ 1100 LoC to describe this search-space. In summary, LLML IFT shows
similar performance to the existing compiler but can be built using much less effort.

4.3        TACO

Tensors form the key construct in machine learning and tensor compilers play an important role
in optimizing these operations. TACO Kjolstad et al. [2017] is one such compiler which can
automatically generate highly optimized code tailored to CPUs and GPUs. TACO’s language
represents the operations in a concise Einsum like notation. Recently, C2TACO Magalhães et al.
[2023] a search-based lifting tool was proposed to automate the translation of C++ code to TACO.
LLML IFT implementation. In Tab. 1, we compare the performance of C2TACO and LLML IFT for
all the benchmarks. We use the same 90 mins timeout for each benchmark that was used in the original
C2TACO evaluation Magalhães et al. [2023]. C2TACO solves 57 out of the total 60 benchmarks,
while LLML IFT successfully solves all 60 benchmarks. The 3 benchmarks that C2TACO fails
to solve require expressions of depth greater than 4. Due to its enumerative approach, C2TACO
struggles to find solutions for these cases. We attempted to run these 3 challenging benchmarks
with an extended timeout of 1 day, but the C2TACO solver was still unable to find a solution.
C2TACO uses over 1000 LoC for implementing the heuristics to scale the symbolic search. In
contrast, LLML IFT relies on a simple 100 lines of prompt (task instruction + DSL semantics) to
achieve better performance than C2TACO. C2TACO takes an average of 41 seconds while LLML IFT
average solving time is 2 seconds. We also perform an experiment to test the scalability of C2TACO
enumerate apporach with more complex benchmarks than the ones used in the original evaluation.
We include the results in Appendix C.

4.4        Tensor Processing

Many domains, such as image processing, signal processing, and deep learning, have legacy code
written in high-level languages that operate on individual values of the input and perform specific
operations. To leverage the optimizations provided by deep learning frameworks or hardware
backends like GPUs, this code needs to be lifted to the operators supported by these languages. Prior
work by Qiu et al. [2024] introduced a common tensor IR that can translate sequential programs to
six different hardware and software backends automatically using a verified lifting approach.
LLML IFT implementation. We evaluate LLML IFT against Tenspiler Qiu et al. [2024] on the
23 benchmarks from the image processing and ML kernel domain3 . Tenspiler is able to solve all
23 benchmarks. LLML IFT also successfully solves all 23 benchmarks (including generating the
correct proofs). However, it is important to note that Tenspiler’s synthesis algorithm relies on three
domain-specific optimizations to achieve scalability. These optimizations require significant effort
to implement, with over ≈ 1200 LoC written by a domain expert. In contrast, LLML IFT solves
these benchmarks without relying on any user-defined heuristics, showcasing its ability to generate
correct solutions without the need for domain-specific optimizations. To check the scalability of
Tenspiler’s symblioc approach, we remove all the optimizations. Tenspiler without the optimizations
can only solve 5 out of the 23 benchmarks with a timeout of 1 hour, highlighting the importance of the
domain-specific optimizations for its performance. These results highlight the ability of LLML IFT
to solve complex benchmarks without relying on domain-specific heuristics. Moreover, LLML IFT
      3
          We refer the readers to the paper Qiu et al. [2024] for more details on these benchmarks.


                                                            8
      Tool      BLAS    DSP      DSPStone     makespeare    mathfu    simpl_array    UTDSP     darknet
    C2TACO      100%    100%      100%          100%        91.6%         90%         100%     92.8%
    LLML IFT    100%    100%      100%          100%        100%         100%         100%     100%
               Table 1: Accuracy on various benchmarks for tensor processing domain.



solves these benchmarks faster than Tenspiler with all its optimizations enabled. LLML IFT takes an
average time of 95.89 seconds to solve each benchmark, whereas Tenspiler takes 115.14 seconds.

4.5    Two-phase Approach for LLML IFT

In this section, we evaluate an alternative approach to the two-phase method described in Sec. 3,
where we generate the Inv(s) and the PS together in a single step. To test this, we prompt the model
in a one-shot setting, providing an example that demonstrates generating the PS and the Inv(s)
simultaneously. We merge the prompts described in Fig. 5 and Fig. 6 to create a unified prompt for
this experiment.
Due to budget constraints, we limit this experiment to the tensor processing domain, which represents
our most complex DSL with 37 operators. We use the same query budget as the two-phase approach.
When prompted to generate the invariant and PS together, LLML IFT successfully solves 20 out
of the total 23 benchmarks. In contrast, the two-phase approach described in Sec. 3 solves all 23
benchmarks. We hypothesize that the reduced performance of the single-phase approach may be
attributed to the increased complexity of generating both the PS and the Inv(s) simultaneously.
Moreover, the two-phase approach enables the model to leverage the generated PS when constructing
the invariant. By having access to the PS, the model can more effectively reason about the necessary
conditions and constraints required for the invariant to hold.

5     Related Work
Code Transpilation. Several approaches have been proposed for automating the task of translating
legacy or unoptimized code to DSLs. These range from symbolic rule-based approaches Radoi et al.
[2014] to search-based verified lifting approaches [Ahmad and Cheung, 2018, Ahmad et al., 2019,
Bhatia et al., 2023, Magalhães et al., 2023] and neural approaches Mariano et al. [2022], Roziere et al.
[2020]. Most of these tools are either optimized for a specific domain or require domain expertise to
scale. In contrast, LLML IFT simplifies the process of building lifting tools by leveraging LLMs. The
closest work to ours is Roziere et al. [2020] which uses a sequence-to-sequence model to translate
code between C++, Java, and Python; our work differs in two key respects: we target lifting to DSLs,
and our LLM based approach produces formally verified code.
LLMs for Code. LLMs are trained on massive amounts of code from various sources, leading to
impressive performance on programming tasks such as code generation [Li et al., 2023, 2022], repair,
testing, and transpilation. Furthermore, LLMs have been successfully employed to aid in certain
formal methods tasks, including generating proofs and specifications [Wu et al., 2023, Pei et al., 2023,
Chakraborty et al., 2023]. However, generating reliable code from LLMs remains challenging due to
the stochastic nature of these models and the lack of an external verification oracle. With LLML IFT,
we demonstrate a novel approach to generating and verifying the generated code using LLMs.

6     Conclusion
We presented a principled approach to leverage LLMs for code transpilation. Unlike prior LLM-based
transpilers, our transpiled code is provably equivalent to the input, while also takes significantly less
time to generate as compared to prior non LLM-based approaches with correctness guarantee, as
demonstrated in transpiling to 4 real-world DSLs.

References
Cosmin Radoi, Stephen J. Fink, Rodric Rabbah, and Manu Sridharan. Translating imperative code
  to mapreduce. In Proceedings of the 2014 ACM International Conference on Object Oriented


                                                   9
  Programming Systems Languages & Applications, OOPSLA ’14, pages 909–927, New York, NY,
  USA, 2014. ACM. ISBN 978-1-4503-2585-1. doi: 10.1145/2660193.2660228.
Armando Solar-Lezama, Liviu Tancau, Rastislav Bodík, Sanjit A. Seshia, and Vijay A. Saraswat.
  Combinatorial sketching for finite programs. In Proceedings of the 12th International Conference
  on Architectural Support for Programming Languages and Operating Systems (ASPLOS), pages
  404–415. ACM Press, October 2006.
Susmit Jha, Sumit Gulwani, Sanjit A. Seshia, and Ashish Tiwari. Oracle-guided component-based
  program synthesis. In Proceedings of the 32nd ACM/IEEE International Conference on Software
  Engineering (ICSE), pages 215–224, May 2010.
Sumit Gulwani, Oleksandr Polozov, and Rishabh Singh. Program synthesis. Found. Trends Program.
  Lang., 4(1-2):1–119, 2017.
Maaz Bin Safeer Ahmad and Alvin Cheung. Automatically leveraging mapreduce frameworks for
 data-intensive applications. In Gautam Das, Christopher M. Jermaine, and Philip A. Bernstein,
 editors, Proceedings of the 2018 International Conference on Management of Data, SIGMOD
 Conference 2018, Houston, TX, USA, June 10-15, 2018, pages 1205–1220. ACM, 2018.
José Wesley de Souza Magalhães, Jackson Woodruff, Elizabeth Polgreen, and Michael F. P. O’Boyle.
  C2taco: Lifting tensor code to taco. In Proceedings of the 22nd ACM SIGPLAN International
  Conference on Generative Programming: Concepts and Experiences, GPCE 2023, page 42–56,
  New York, NY, USA, 2023. Association for Computing Machinery. ISBN 9798400704062. doi:
  10.1145/3624007.3624053. URL https://doi.org/10.1145/3624007.3624053.
Alvin Cheung, Armando Solar-Lezama, and Samuel Madden. Optimizing database-backed applica-
  tions with query synthesis. ACM SIGPLAN Notices, 48(6):3–14, 2013.
Maaz Bin Safeer Ahmad, Jonathan Ragan-Kelley, Alvin Cheung, and Shoaib Kamil. Automatically
 translating image processing libraries to halide. ACM Transactions on Graphics (TOG), 38(6):
 1–13, 2019.
Benjamin Mariano, Yanju Chen, Yu Feng, Greg Durrett, and Işil Dillig. Automated transpilation of
  imperative to functional code using neural-guided program synthesis. Proc. ACM Program. Lang.,
  6(OOPSLA1), April 2022. doi: 10.1145/3527315. URL https://doi.org/10.1145/3527315.
Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidi-
  rectional transformers for language understanding. In North American Chapter of the Association
  for Computational Linguistics, 2019. URL https://api.semanticscholar.org/CorpusID:
  52967399.
Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal,
  Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel
  Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler,
  Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott
  Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya
  Sutskever, and Dario Amodei. Language models are few-shot learners. In Proceedings of the 34th
  International Conference on Neural Information Processing Systems, NIPS’20, Red Hook, NY,
  USA, 2020. Curran Associates Inc. ISBN 9781713829546.
Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennighoff, Denis Kocetkov, Chenghao Mou,
  Marc Marone, Christopher Akiki, Jia Li, Jenny Chim, Qian Liu, Evgenii Zheltonozhskii, Terry Yue
  Zhuo, Thomas Wang, Olivier Dehaene, Mishig Davaadorj, Joel Lamy-Poirier, João Monteiro,
  Oleh Shliazhko, Nicolas Gontier, Nicholas Meade, Armel Zebaze, Ming-Ho Yee, Logesh Kumar
  Umapathi, Jian Zhu, Benjamin Lipkin, Muhtasham Oblokulov, Zhiruo Wang, Rudra Murthy, Jason
  Stillerman, Siva Sankalp Patel, Dmitry Abulkhanov, Marco Zocca, Manan Dey, Zhihan Zhang,
  Nour Fahmy, Urvashi Bhattacharyya, Wenhao Yu, Swayam Singh, Sasha Luccioni, Paulo Villegas,
  Maxim Kunakov, Fedor Zhdanov, Manuel Romero, Tony Lee, Nadav Timor, Jennifer Ding, Claire
  Schlesinger, Hailey Schoelkopf, Jan Ebert, Tri Dao, Mayank Mishra, Alex Gu, Jennifer Robinson,
  Carolyn Jane Anderson, Brendan Dolan-Gavitt, Danish Contractor, Siva Reddy, Daniel Fried,
  Dzmitry Bahdanau, Yacine Jernite, Carlos Muñoz Ferrandis, Sean Hughes, Thomas Wolf, Arjun
  Guha, Leandro von Werra, and Harm de Vries. Starcoder: may the source be with you!, 2023.


                                               10
Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom
  Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien
  de Masson d’Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven
  Gowal, Alexey Cherepanov, James Molloy, Daniel J. Mankowitz, Esme Sutherland Robson,
  Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals. Competition-level
  code generation with alphacode. Science, 378(6624):1092–1097, December 2022. ISSN 1095-9203.
  doi: 10.1126/science.abq1158. URL http://dx.doi.org/10.1126/science.abq1158.
Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi
  Adi, Jingyu Liu, Romain Sauvestre, Tal Remez, Jérémy Rapin, Artyom Kozhevnikov, Ivan Evtimov,
  Joanna Bitton, Manish Bhatt, Cristian Canton Ferrer, Aaron Grattafiori, Wenhan Xiong, Alexandre
  Défossez, Jade Copet, Faisal Azhar, Hugo Touvron, Louis Martin, Nicolas Usunier, Thomas
  Scialom, and Gabriel Synnaeve. Code llama: Open foundation models for code, 2024.
Kexin Pei, David Bieber, Kensen Shi, Charles Sutton, and Pengcheng Yin. Can large language models
  reason about program invariants? In Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara
  Engelhardt, Sivan Sabato, and Jonathan Scarlett, editors, Proceedings of the 40th International
  Conference on Machine Learning, volume 202 of Proceedings of Machine Learning Research,
  pages 27496–27520. PMLR, 23–29 Jul 2023. URL https://proceedings.mlr.press/v202/
  pei23a.html.
Saikat Chakraborty, Shuvendu K Lahiri, Sarah Fakhoury, Madanlal Musuvathi, Akash Lal, Aseem
  Rastogi, Aditya Senthilnathan, Rahul Sharma, and Nikhil Swamy. Ranking llm-generated loop
  invariants for program verification. arXiv preprint arXiv:2310.09342, 2023.
Rajeev Alur, Rastislav Bodik, Garvit Juniwal, Milo M. K. Martin, Mukund Raghothaman, Sanjit A.
  Seshia, Rishabh Singh, Armando Solar-Lezama, Emina Torlak, and Abhishek Udupa. Syntax-
  guided synthesis. In 2013 Formal Methods in Computer-Aided Design, pages 1–8, 2013. doi:
  10.1109/FMCAD.2013.6679385.
Fredrik Kjolstad, Shoaib Kamil, Stephen Chou, David Lugato, and Saman Amarasinghe. The tensor
  algebra compiler. Proc. ACM Program. Lang., 1(OOPSLA):77:1–77:29, October 2017. ISSN
  2475-1421. doi: 10.1145/3133901. URL http://doi.acm.org/10.1145/3133901.
C. A. R. Hoare. An axiomatic basis for computer programming. Commun. ACM, 12(10):576–580,
  1969.
Matei Zaharia, Mosharaf Chowdhury, Tathagata Das, Ankur Dave, Justin Ma, Murphy McCauley,
 Michael J. Franklin, Scott Shenker, and Ion Stoica. Resilient distributed datasets: A fault-tolerant
 abstraction for in-memory cluster computing. In Proceedings of the 9th USENIX Conference on
 Networked Systems Design and Implementation, NSDI’12, 2012.
Anirudh Sivaraman, Alvin Cheung, Mihai Budiu, Changhoon Kim, Mohammad Alizadeh, Hari
  Balakrishnan, George Varghese, Nick McKeown, and Steve Licking. Packet transactions: High-
  level programming for line-rate switches. In Proceedings of the ACM SIGCOMM 2016 Conference,
 Florianopolis, Brazil, August 22-26, 2016, pages 15–28, 2016.
Jie Qiu, Colin Cai, Sahil Bhatia, Niranjan Hasabnis, Sanjit A. Seshia, and Alvin Cheung. Tenspiler:
   A verified lifting-based compiler for tensor operations, 2024.
Sahil Bhatia, Sumer Kohli, Sanjit A. Seshia, and Alvin Cheung. Building Code Transpilers for
  Domain-Specific Languages Using Program Synthesis. In Karim Ali and Guido Salvaneschi,
  editors, 37th European Conference on Object-Oriented Programming (ECOOP 2023), volume 263
  of Leibniz International Proceedings in Informatics (LIPIcs), pages 38:1–38:30, Dagstuhl, Ger-
  many, 2023. Schloss Dagstuhl – Leibniz-Zentrum für Informatik. ISBN 978-3-95977-281-5. doi:
  10.4230/LIPIcs.ECOOP.2023.38. URL https://drops.dagstuhl.de/entities/document/10.
  4230/LIPIcs.ECOOP.2023.38.
Emina Torlak and Rastislav Bodik. Growing solver-aided languages with rosette. In Proceedings
 of the 2013 ACM International Symposium on New Ideas, New Paradigms, and Reflections on
 Programming & Software, Onward! 2013, pages 135–152, New York, NY, USA, 2013. ACM.
 ISBN 978-1-4503-2472-4. doi: 10.1145/2509578.2509586. URL http://doi.acm.org/10.
 1145/2509578.2509586.


                                                 11
Baptiste Roziere, Marie-Anne Lachaux, Lowik Chanussot, and Guillaume Lample. Unsupervised
  translation of programming languages. Advances in neural information processing systems, 33:
  20601–20611, 2020.
Haoze Wu, Clark Barrett, and Nina Narodytska. Lemur: Integrating large language models in
  automated program verification. arXiv preprint arXiv:2310.04870, 2023.




                                             12
Appendix

A    Algorithm

The transpile_code algorithm translates the source code of a program into a target language using
LLM. The source_code parameter represents the code to be transpiled, and num_iters and n specify
the number of iterations and the number of PS and Invs to generate in each iteration, respectively.
The algorithm maintains two sets: incorrect_ps_sols and seen_ps_sols (lines 2, 3). The
incorrect_ps_sols set keeps track of PS that are syntactically correct but have been found to
be incorrect during the transpilation process. The seen_ps_sols set keeps track of all PS that have
been processed by the algorithm. The algorithm operates in a loop that runs for num_iters iterations
(line 5). In each iteration, the algorithm calls get_ps_sols to generate n different PS for the given
source_code from LLM, and supply to LLM any PS that have been marked as incorrect as stored
in the incorrect_ps_sols set (line 6). For each generated PS, the algorithm first checks if it has
been seen before by looking it up in the seen_ps_sols set (line 9). If the PS has been encountered
previously, the algorithm skips it to avoid redundant processing. If it is new, the algorithm parses it
to check for syntactic validity using the parse function (line 12). If the summary has invalid syntax,
it is discarded, and the algorithm moves on to the next summary. If the PS is syntactically correct,
the algorithm proceeds to generate Inv for it. It maintains a set called seen_inv_sols_for_ps that
keeps track of invariants that have been processed for the current PS to avoid redundant processing.
It also checks each generated Inv’s syntactic validity and discards it if it is not.
If both the PS and the Invs pass the syntactic validation, the algorithm proceeds to verify their
correctness using the verify function (line 26). If the verification succeeds, the algorithm returns
the PS (ps_sol) as the final transpiled code. If none of the generated Invs for a PS are found to be
valid, the algorithm assumes that the PS itself is incorrect. It adds the PS to the incorrect_ps_sols
set to exclude it from future iterations and adds it to the seen_ps_sols set to mark it as processed.
The algorithm continues this process of generating PS and Invs and verifying their correctness until
a valid solution is found or the maximum number of tries is reached. If no valid solution is found
within the given number of tries, the algorithm returns None, indicating that the transpilation was
unsuccessful.


B    Prompts

In this section, we present an instantiation of the prompt structure shown in Fig. 4. The prompt
shown in Fig. 5 consists of several components designed to guide the language model in generating
semantically equivalent code using a restricted set of functions and constants. The prompt begins
with a clear task description that instructs the model that its goal is to rewrite the given C++ function
using only the provided functions and constants while maintaining semantic equivalence. Next, the
prompt includes a set of instructions. These constraints are designed to make the generated code
easier to parse and translate into a format suitable for theorem provers. The prompt then provides a
set of defined functions in Python. These functions define all DSL operators that the model can use
to rewrite the given C++ function. Finally, the prompt includes the test function in C++ which the
model should rewrite using the provided functions and constants.
In Fig. 6, we present a one-shot prompt designed to guide the language model in generating loop
invariants for the given test function. This prompt is similar in structure to the program summary
guessing prompt: it provides a clear task description, a set of instructions, and examples to guide the
model in generating the desired output. The prompt instructs the model to prove the assertion in the
test function by finding a loop invariant using the defined functions. It includes specific constraints
on the generated loop invariant, such as using only the defined functions, avoiding loops, using a
single return statement, inlining expressions, and generating separate invariants for each loop in the
test function. These constraints are intended to simplify the parsing of the generated invariants into
SMT formulas, making it easier to integrate them into automated theorem provers. Additionally, the
prompt provides a template for the invariant structure, guiding the model in constructing the loop
invariant as a Python function that takes the loop variables and relevant data structures as input and
returns a boolean expression. The invariant should involve comparisons of the loop variables using
operators and expressions, and an equality check for the loop-dependent variable using the defined


                                                   13
 1   def transpile_code(source_code: str, num_iters: int, n: int) -> str:
 2       incorrect_ps_sols: set[str] = set()
 3       seen_ps_sols: set[str] = set()
 4
 5      for _ in range(num_iters):
 6          ps_sols: list[str] = get_ps_sols(n, source_code, incorrect_ps_sols)
 7          for ps_sol in ps_sols:
 8              # We have processed this PS before
 9              if ps_sol in seen_ps_sols:
10                  continue
11              # If this PS has invalid syntax
12              if not parse(ps_sol):
13                  continue
14
15             # Generate invariants for this PS
16             seen_inv_sols_for_ps: set[str] = set()
17             inv_sols: list[str] = get_inv_sols_for_ps(n, ps_sol)
18             for inv_sol in inv_sols:
19                 # We have processed this INV for this PS before
20                 if inv_sol in seen_inv_sols_for_ps:
21                     continue
22                 # If this INV has invalid syntax
23                 if not parse(inv_sol):
24                     continue
25                 # Verify INV and PS.
26                 if verify(inv_sol, ps_sol):
27                     return ps_sol
28                 seen_inv_sols_for_ps.add(inv_sol)
29
30             # At this point, none of the INVs work for this PS. We assume this ps is incorrect.
31             incorrect_ps_sols.add(ps_sol)
32             seen_ps_sols.add(ps_sol)
33
34
35      # No solution has been found.
36      return None




functions. The prompt also includes an example to demonstrate the expected format and structure of
the loop invariant. Example 1 shows a test function that performs element-wise subtraction of two
matrices and provides two loop invariants. Example 2 shows the test function for which we need to
generate the loop invariants.
To avoid regenerating the same incorrect solutions, the prompt also includes all the syntactically
correct solutions that have been generated so far, along with a message saying These generated
programs are incorrect. Do not generate the same. Please generate another program.

C     Scalability
In this section, we evaluate the scalability of symbolic solvers in the context of VL-based tools. The
benchmarks used in the evaluation of these tools are often carefully selected and limited in scope,
allowing the tools to perform well within their intended domain. However, in this experiment, we
aim to demonstrate that symbolic tools relying on domain-specific heuristics can be brittle and fail to
scale when the complexity of the benchmarks increases beyond a certain threshold.
We begin by evaluating C2TACO. Upon careful analysis of the benchmarks on which C2TACO
struggles, we observed that the tool often times out when tasked with generating expressions of
length greater than 4 One such example is illustrated in Fig. 7a where the source performs an in-place
operation on an array arr of length n and raises each element of the array to the power of 4. C2TACO
enumerates candidate expressions using tensor operators and index variables in increasing order
of expression length. C2TACO enumerates ≈30k candidates. We illustrate some of the incorrect
expressions in Fig. 7a.
To test the scalability of C2TACO, we randomly generated a set of 10 benchmarks with expressions
of varying lengths, ranging from 5 to 10, incorporating various arithmetic operations (see Fig. 7b for
an example). We used a timeout of 90 minutes for C2TACO, as reported in the original evaluation.
C2TACO was unable to solve any of the 10 benchmarks within the timeout. In contrast, LLML IFT,
was able to solve all 10 benchmarks correctly in less than 2 seconds. This performance can be
attributed to the ability of language models to identify patterns and learn from the context provided in


                                                        14
Figure 5: Program summary guessing prompt




                   15
the source code. To further test the capabilities of LLML IFT, we evaluated it on a variation of the
benchmark shown in Fig. 7a, where each element of the array is raised to the power of 20 instead of
4. Despite the increased complexity of the expression, LLML IFT was able to generate the correct
solution efficiently.

D    Qualitative Analysis of the Errors.
In this section, we provide a qualitative analysis of the mistakes made by LLMs while generating
code and proofs. In LLML IFT, we use Python as the IR and the ps and inv(s) are generated in Python.
The errors encountered can be classified into two categories: syntactic and semantic.
Syntactic errors occur when the generated code constructs are not compatible with the theorem prover.
To mitigate this issue, we use a syntactic parser that translates the generated solutions to the language
supported by the theorem prover. The parser ensures that only supported constructs are present in the
solutions and rejects any candidates that do not comply with the theorem prover’s syntax.
One common source of syntactic errors is the use of Python-specific constructs that are not supported
by SMT solvers. Although we prompt the model to generate solutions using only the constructs
provided in the prompt’s scope, controlling the exact code generated by the model can be challenging.
Fig. 9 illustrates examples of program summaries generated by GPT-4 for the screen blend
benchmark that contain unsupported constructs. For instance, the first solution in Fig. 9 uses a for
loop, which is not supported by SMT solvers. Similarly, the second and third solutions utilize Python’s
list comprehension syntax, which is also not directly supported by SMT solvers. List comprehension
are supported in SMT solvers using empty lists and append functions, such as append(1, []).
Semantic errors occur when the generated code is syntactically correct but is semantically not
equivalent to the given S. In the context of the screen blend benchmark (shown in Fig. 8),
Fig. 10 illustrates two examples of semantically incorrect programs generated by GPT-4. The
first program incorrectly subtracts a term from the base matrix instead of subtracting it from
the sum of base and active matrices. The second program suffers from a similar issue. It
subtracts an incorrect term from the active matrix. Specifically, the term being subtracted
is matrix_elemwise_div(matrix_elemwise_mul(base, active), matrix_scalar_mul(32,
matrix_elemwise_mul(base, active))), which is different from the one in the given program.




                                                  16
                17

Figure 6: Invariant guessing prompt
 1   void fourth_in_place(int* arr, int n)
 2   {
 3     for (int i = 0; i < n; ++i) {
 4       arr[i] = arr[i] * arr[i];
 5       arr[i] = arr[i] * arr[i];
 6     }                                                  1   void test1(int* arr, int n)
 7   }                                                    2   {
 8   //TACO expression                                    3     for (int i = 0; i < n; ++i) {
 9   out[i] = arr[i] * arr[i] * arr[i] * arr[i]           4       arr[i] = arr[i] + arr[i] + arr[i] + arr[i] + arr[i];
10                                                        5     }
11   //Incorrect TACO expressions                         6   }
12   out(i) = arr(i) * arr(i)                             7   //TACO expression
13   out(i) = Cons1 + arr(j,i)                            8   out[i] = arr[i] + arr[i] + arr[i] + arr[i] + arr[i]
14   out(k) = Cons1 * arr(l,k,j)
                                                          (b) Example of synthetic benchmark with expression
        (a) Benchmark on which C2TACO fails.              length = 5.
            Figure 7: Scalability evaluation of symbolic solvers using synthetic benchmarks

 1   vector<vector<int>> screen_blend_8(vector<vector<int>> base, vector<vector<int>> active)
 2   {
 3       vector<vector<int>> out;
 4       int m = base.size();
 5       int n = base[0].size();
 6           for (int row = 0; row < m; row++) {
 7           vector<int> row_vec;
 8                  for (int col = 0; col < n; col++) {
 9                         int pixel = base[row][col] + active[row][col] - (base[row][col] * active[row][col]) / 255;
10                         row_vec.push_back(pixel);
11                  }
12                  out.push_back(row_vec);
13           }
14           return out;
15   }


                              Figure 8: Screen_blend benchmark source code.

 1   def screen_blend_8(base: List[List[int]], active: List[List[int]]) -> List[List[int]]:
 2       return matrix_elemwise_add(
 3           matrix_elemwise_sub(
 4               base,
 5               matrix_elemwise_div(
 6                   matrix_elemwise_mul(base, active),
 7                   vec_scalar_mul(32, [1 for _ in range(len(base[0]))])
 8               )
 9           ),
10           active
11       )

 1   def screen_blend_8(base: List[List[int]], active: List[List[int]]) -> List[List[int]]:
 2       return matrix_elemwise_add(
 3           matrix_elemwise_sub(
 4               base,
 5               matrix_elemwise_div(
 6                   matrix_elemwise_mul(base, active),
 7                   vec_scalar_mul(32, [[1]*len(base[0])]*len(base))
 8               )
 9           ),
10           active
11       )


 1   def screen_blend_8(base: List[List[int]], active: List[List[int]]) -> List[List[int]]:
 2       return matrix_elemwise_add(
 3           matrix_elemwise_sub(
 4               base,
 5               matrix_elemwise_div(
 6                   matrix_elemwise_mul(base, active),
 7                   vec_scalar_mul(32, vec_elemwise_mul([1], [1]))
 8               )
 9           ),
10           active
11       )


                       Figure 9: Programs rejected by LLML IFT’s syntactic parser


                                                        18
 1   def screen_blend_8(base: List[List[int]], active: List[List[int]]) -> List[List[int]]:
 2       return matrix_elemwise_add(
 3           matrix_elemwise_sub(
 4               base,
 5               matrix_elemwise_div(
 6                   matrix_elemwise_mul(base, active),
 7                   scalar_matrix_div(32, base)
 8               )
 9           ),
10           active
11       )

 1   def screen_blend_8(base: List[List[int]], active: List[List[int]]) -> List[List[int]]:
 2       return matrix_elemwise_add(
 3           base,
 4           matrix_elemwise_sub(
 5               active,
 6               matrix_elemwise_div(
 7                   matrix_elemwise_mul(base, active),
 8                   matrix_scalar_mul(32, matrix_elemwise_mul(base, active))
 9               )
10           )
11       )


              Figure 10: Programs rejected by theorem prover for semantic incorrectness




                                                        19
