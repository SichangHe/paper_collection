                                                             Verifying LLM-Generated Code in the Context of
                                                                  Software Verification with Ada/SPARK

                                                                            Marcos Cramer1        a
                                                                                                      and Lucian McIntyre2       b
                                                                              1 secunet Security Networks AG, Dresden, Germany
                                                           2 International Center for Computational Logic, Technical University Dresden, Germany

                                                                         marcos.cramer@secunet.com, lucianmcintyre@mailbox.org




                                         Keywords:       Software Verification, LLM, Code Generation, Proof Generation, Ada/SPARK
arXiv:2502.07728v1 [cs.SE] 11 Feb 2025




                                         Abstract:       Large language models (LLMs) have demonstrated remarkable code generation capabilities, but the correct-
                                                         ness of the generated code cannot be inherently trusted. This paper explores the feasibility of using formal
                                                         software verification, specifically the SPARK framework for Ada, to ensure the reliability of LLM-generated
                                                         code. We present Marmaragan, a tool that leverages an LLM in order to generate SPARK annotations for ex-
                                                         isting programs, enabling formal verification of the code. The tool is benchmarked on a curated set of SPARK
                                                         programs, with annotations selectively removed to test specific capabilities. The performance of Marmaragan
                                                         with GPT-4o on the benchmark is promising, with correct annotations having been generated for 50.7% of the
                                                         benchmark cases. The results establish a foundation for future work on combining the power of LLMs with
                                                         the reliability of formal software verification.



                                         1       INTRODUCTION                                             standard of code quality and safety.
                                                                                                              The current paper is motivated by the need to
                                         Large language models (LLMs) have attracted signifi-             bridge the gap between the creative potential of LLMs
                                         cant attention within both the AI research community             and the necessity for reliable, error-free code. By
                                         and the general public due to their generative capa-             leveraging formal verification techniques, specifically
                                         bilities. Tools such as ChatGPT have demonstrated                through the SPARK programming language, we aim
                                         the potential of LLMs to automate and accelerate pro-            to explore the feasibility of combining LLMs with
                                         cesses in diverse fields, with software development              formal verification to produce code that is both inno-
                                         benefiting particularly from their ability to generate           vative and provably correct. This study investigates
                                         code. However, while LLMs showcase impressive                    whether LLMs can generate annotations for SPARK
                                         creativity and adaptability, they also present risks. As         programs, facilitating formal verification of the result-
                                         these models operate as black boxes, the code they               ing code.
                                         generate cannot inherently be trusted to be correct or               For this purpose, we have implemented Marmara-
                                         error-free, posing challenges for real-world applica-            gan, a tool that leverages an LLM in order to generate
                                         tions where reliability and safety are essential.                SPARK annotations for existing programs, enabling
                                             To address the uncertainties associated with LLM-            formal verification of the code using the GNATprove
                                         generated code, formal verification techniques offer             tool. Marmaragan can be viewed as a prototype for
                                         a promising solution. Formal software verification               the backend of an AI-powered annotation generator
                                         employs rigorous mathematical methods to prove the               that could run in the background of a SPARK editor. It
                                         correctness of code against a specified set of proper-           incorporates features such as generating multiple so-
                                         ties, which can help ensure that software meets its in-          lution attempts, retrying with additional context from
                                         tended specifications reliably. Integrating formal ver-          GNATprove, and providing pre-compiled error mes-
                                         ification with LLM-generated code has the potential              sages to improve performance. Marmaragan can cur-
                                         to mitigate risks, making it possible to harness the             rently be combined with any LLM in the OpenAI API
                                         creative benefits of LLMs while maintaining a high               and has been most throughly tested with GPT-4o. It
                                                                                                          has parameters for the number of solutions generated
                                             a    https://orcid.org/0000-0002-9461-1245                   in parallel, for the number of retries that Marmara-
                                             b    https://orcid.org/0009-0008-0408-4340                   gan attempts before giving up as well as for toggling
a special chain-of-thought mode.                           “formal verification” as a shorthand for “formal soft-
     In order to evaluate how well Marmaragan per-         ware verification”.
forms depending on the value of its parameters, we             There are different methodological approaches to
created a benchmark based on a curated set of SPARK        formal verification. For this paper, we don’t need to
programs, from which annotations were selectively          consider model checking and instead focus on deduc-
removed following various removal schemata. Ex-            tive verification, which is “the process of turning the
periments on the benchmark demonstrate Marmara-            correctness of a program into a mathematical state-
gan’s competence in generating annotations: Over-          ment and then proving it” (Filliâtre, 2011). In deduc-
all, it generates correct annotations for 50.7% of the     tive verification, the desired behaviour of the program
benchmark programs. Furthermore, the experiments           needs to be specified in a formal language. The task
shed light on what is the optimal balance between par-     is then to prove that the program actually satisfies the
allel solution attempts and retries in the light of lim-   specification for all possible inputs.
ited computational resources.                                  At the level of single functions in the program, this
     By successfully generating correct annotations,       is realized through pre- and postconditions, which are
we establish a foundation for future work: In the near     assertions on values of variables that enter and exit
to medium-term future, this research could contribute      given functions within our program, specifying prop-
to making applications of formal verification of code      erties and relationships (Hoare, 1969). A precondi-
reliability and safety more efficient. In the long term    tion defines the conditions that must be met, so that a
it could contribute a building block towards a hybrid      given function can be executed. Analogously, a post-
tool that combines the power of LLMs with the re-          condition defines the conditions that must be met di-
liability of software verification for generating fully    rectly subsequent to function execution. For example,
verified programs.                                         a function computing F(x, y) = x − y could have the
     In Section 2, we discuss the preliminaries of this    precondition x > y for ensuring that one stays in the
paper in the areas of logic, formal software verifica-     realm of positive numbers. In this case, a sensible
tion (with a focus on SPARK 2014) and large lan-           postcondition would be F(x, y) > 0, as this postcon-
guage models. The implementation of Marmaragan is          dition logically follows from the precondition and the
presented in Section 3. In Section 4, we describe the      definition of the function F(x, y). This kind of logi-
methodology that we applied to create a benchmark          cal entailment needs to hold for every postcondition
for evaluating Marmaragan. The results of running          of a function, and this needs to be established through
Maramaragan with varying parameters on the bench-          a formal proof. We say that there is proof obligation
mark are presented in Section 5, and in Section 6 we       for deriving the postcondition.
discuss these results. Section 7 presents related work.
In section 8, we discuss future work before conclud-       2.2    SPARK 2014
ing in Section 9.
                                                           SPARK 2014 (Moi, 2013) is a formally defined subset
                                                           of the Ada programming language (AdaCore, 1980),
2     PRELIMINARIES                                        designed to support the development of reliable and
                                                           provably correct software (Barnes, 2012). Its un-
This section discusses the foundations the work is set     ambiguous semantics ensures that programs behave
upon and the work it relates to and is inspired by.        consistently and predictably. SPARK allows only
                                                           specific constructs from Ada, ensuring compatibility
                                                           with formal verification methods. Programs written
2.1    Formal Software Verification
                                                           in SPARK can be annotated with assertions, including
Formal software verification is the process of proving     preconditions and postconditions, to support modular
the correctness of a software program with respect to      deductive verification (Hoare, 1969).
a specified formal specification or property, using for-       SPARK has found application in multiple areas,
mal mathematical methods. It ensures that the soft-        including train control systems and space transporta-
ware behaves as intended in all possible scenarios. In     tion (Dross et al., 2014), commercial aviation (Moy
contrast with common non-formal testing techniques,        et al., 2013), air traffic management (Chapman and
which always cover only a limited number of scenar-        Schanda, 2014) and GPU design (Chapman et al.,
ios and are thus vulnerable to having missed out on a      2024).
                                                               Some annotations in SPARK take the form of
scenario in which a bug takes effect, formal software
                                                           pragma statements, such as:
verification covers all potential runs of the program.
From now on, we will often use the equivalent term         pragma Assertion ( condition );
    These include constructs like Assert,
                                                          Listing 1: Example of loop invariants for a SPARK function
Loop Invariant (see section 2.2.1 below), and             that doubles a number.
Loop Variant, which facilitate detailed specification
                                                          procedure Double_Number (X : in Natural ; Result :
and verification. Additionally, SPARK ensures the              out Natural ) is
absence of runtime errors, such as array bounds              Count : Natural := 0;
violations or division by zero, by verifying adherence    begin
to defined rules.                                            Result := 0;
    In SPARK, code is organized into two types of            while Count < X loop
files: .ads and .adb. The .ads files, known as                  pragma Loop_Invariant ( Result = Count * 2) ;
                                                                pragma Loop_Invariant ( Count < X);
specification files, define the interface of modules,
                                                                Result := Result + 2;
including function and procedure declarations along             Count := Count + 1;
with their associated preconditions and postcondi-           end loop ;
tions. In contrast, the .adb files, or implementa-        end Double_Number ;
tion files, contain the executable code and additional
annotations such as Assert, Loop Invariant, and
Loop Variant pragmas. This separation supports a          2.3    Large Language Models and
clear distinction between the specification and imple-           Transformers
mentation, facilitating modular reasoning and verifi-
cation of SPARK programs.                                 The development of large language models (LLMs)
    The GNATprove toolchain is the primary mecha-         has been a significant leap forward for AI develop-
nism for verifying SPARK programs. It operates in         ment, spurred by the introduction of the transformer
three stages:                                             architecture by Vaswani et al. in “Attention Is All You
 • Check: Ensures SPARK compatibility.                    Need” (Vaswani et al., 2017).
                                                              LLMs, which are specialized neural models with
 • Flow: Analyzes data and information flow.              billions of parameters, excel at capturing patterns in
 • Proof: Verifies code against assertions and con-       text data to perform a variety of language tasks. These
   ditions using third-party theorem provers via          models evolved from earlier statistical language mod-
   Why3 (Filliâtre and Paskevich, 2013).                 els that relied on n-gram techniques to predict word
    GNATprove translates SPARK code into proof            sequences but struggled with long-range dependen-
obligations, resolving them using automated provers.      cies. Innovations like Word2Vec (Mikolov et al.,
This ensures compliance with user-defined and             2013) and GloVe (Pennington et al., 2014), combined
language-level constraints, making SPARK programs         with the transformer’s attention mechanisms, enabled
highly reliable.                                          the modeling of complex relationships between words
    GNATprove provides feedback in the form of er-        (or rather between tokens), addressing the limitations
rors and mediums. Errors typically indicate issues        of traditional approaches.
such as syntax or type errors that prevent the program        The transformer architecture, central to LLMs,
from being executed. Mediums, on the other hand,          employs a multi-layer encoder-decoder struc-
result from proof obligations that could not be dis-      ture (Vaswani et al., 2017). Its core innovation, the
charged, either because the statement being proved is     self-attention mechanism, calculates the importance
false or due to missing annotations. When a statement     of tokens relative to one another, enhancing the
is false, these mediums may include counterexamples       model’s ability to understand context. Multi-head
generated by the tool to help identify the source of      attention further improves performance by allowing
the issue.                                                the model to focus on different aspects of input simul-
                                                          taneously. The final stages of transformers generate
2.2.1   Loop Invariants                                   predictions through a combination of linear layers
                                                          and softmax functions, transforming embeddings into
A loop invariant is a property that holds during each     meaningful output. These advancements, coupled
loop iteration. It can be viewed as the induction hy-     with significant increases in model scale and training
pothesis in an inductive proof over the number of loop    data, underpin the capabilities of state-of-the-art (as
iterations. Consider the example in Listing 1.            of 2024) LLMs like OpenAI’s GPT-4 and GPT-4o
    Here, the invariants state that the Result is twice   models, which are the basis of this thesis.
the Count and that the loop counter does not exceed X.
2.3.1   Chain-of-thought prompting                         3.2     Proof of Concept
LLM performance has been shown to depend on                The aim was to develop a proof of concept for au-
the formulation of the prompt that is given to the         tomatic annotation generation in SPARK. This con-
LLM. One prompting technique that is relevant to our       cept stemmed from the hypothesis that generating for-
work is chain-of-thought-prompting (Jason Wei et al.,      mally verified code with an LLM circumvents the typ-
2023), whose applicability to generating SPARK an-         ical problems encountered with LLM-generated code.
notations we have studied (see Section 3). This                Although LLMs are showing great ability in the
prompting technique enhances reasoning by guiding          area of code generation, the code they create cannot
LLMs through a series of intermediate natural lan-         be assumed to be free of faults or bugs. By gener-
guage steps before generating the final output. For        ating formally verifiable code, it is possible to elim-
this, the prompt is extended by a note about the in-       inate these types of errors. Marmaragan is a step in
tended structure of the response, e.g. “Let’s think step   this direction. By showing that it is possible to gener-
by step”. This technique has been shown to sig-            ate SPARK 2014 annotations for a given program, we
nificantly improve model performance on reasoning-         show that one of the main difficulties of generating
heavy tasks, both for few-shot prompting (Jason Wei        formally verifiable code can be overcome.
et al., 2023) and for zero-shot prompting (Kojima
et al., 2023).                                             3.3     Environment Emulation
                                                           Marmaragan is designed to emulate a tool which runs
3     IMPLEMENTATION                                       in the background of a SPARK 2014 editor, such as
                                                           GNAT Studio (Brosgol, 2019). With this setup, a user
This section provides a detailed description of Mar-       may send requests to the tool, such that annotations
maragan, a tool that leverages an LLM in order to          are generated for their SPARK code.
generate SPARK annotations for existing programs,              As Marmaragan is a proof of concept, the idea was
enabling formal verification of the code.                  to design a tool which, given existing SPARK code,
                                                           is capable of generating annotations. The resulting
3.1     Marmaragan                                         added annotations should lead to GNATprove running
                                                           free of errors and mediums. Given this premise, the
Marmaragan [GitHub] is a tool, developed in Python,        prompting strategy and setup of Marmaragan is de-
designed for the SPARK 2014 language. The tool             veloped in such a way as to optimally emulate these
implements a hybrid AI approach that combines the          conditions.
power of LLMs with the trustworthiness of logic-
based reasoning to generate annotations required for       3.4     Implementation Details
formal verification within SPARK 2014 programs.
    Use is made of the LangChain (Chase, 2022) Li-         Here we deal with the implementation details of Mar-
brary to handle the calls to the OpenAI API and make       maragan. Figure 1 provides an overview
LLM interaction seamless.
    Marmaragan takes as input an existing Spark            3.4.1   Marmaragan as a Benchmarking Tool
project consisting of the specification and implemen-
                                                           Marmaragan is developed as a proof of concept, im-
tation files as well as any dependencies. Using this, it
                                                           plemented as a benchmarking application in order to
queries an LLM to generate missing pragma state-
                                                           evaluate its functionality and performance. It works
ments and then allows GNATprove to compile and
                                                           by taking a benchmark as input, then iterating over
verify the resulting code. The tool incorporates a
                                                           each of the files. For each task, it attempts to generate
range of strategies to assist in generating correct pro-
                                                           all required annotations, such that the code runs error-
grams, including features for retrying with GNAT-
                                                           and medium-free. This procedure may be configured
prove errors and mediums as well as post-processing
                                                           in multiple ways, by modifying the prompt to provide
of LLM output.
                                                           more context to the LLM and changing how solutions
    In the following, we describe the motivation and
                                                           are generated.
concepts behind Maramaragan. We survey the fea-
tures of the tool and discuss each of the steps that are   3.4.2   Prompting in Marmaragan
taken to transform input into output.
                                                           As described in Figure 1, an important step of the
                                                           workflow in Marmaragan is prompting the LLM. A
Figure 1: Overview of the control flow in Marmaragan. Stage 1 initializes input parameters and generates the SPARK
directory. Stage 2 begins the iteration over each of the files in the benchmark, formatting the prompt and invoking the LLM.
Stage 3 is output processing, in Stage 4 GNATprove is run and mediums are extracted. Processes in Stage 5 only run if
enabled: the prompt is reformatted with the previous incorrect solution and GNATprove medium(s) are also included.


good prompt is key to generating useful LLM re-                  dependencies of a Spark2014 / ADA project :
sponses, thus we delve into the details of this step.
    In Marmaragan prompting works by inserting the               { dependencies }

given SPARK 2014 files into the prompt, format-
                                                                 This is the package body ( implementation ):
ting and subsequently invoking the LLM. The prompt
used for all queries can be found below in listing 2.            { package_body }

      Listing 2: The base prompt used to query the LLM           Add one or multiple pragma statements
Try to solve the following problem logically and                 (e.g. pragma Loop_Invariant , pragma Assert ) to the
step by step . The final answer should then be                   package body , so that the code runs error and
delimited in the following way :                                 medium free .


‘‘‘ ada                                                          Make use of the mediums provided in the prompt to
                                                                 guide your solution .
code here
                                                                 You must not modify the code in any other way ,
‘‘‘                                                              except to add " for " loops and " if " statements that
                                                                 enclose only pragma statements .
The following are the specifications and
Do not modify the functionality in any way . Return      2023) is a strategy that helps to increase the perfor-
the entire implementation file with the required         mance of LLMs on complex reasoning tasks. To
additions .                                              gain some insight into the effectiveness of different
    The prompt is designed to be as general as pos-      prompting techniques, a chain-of-thought prompt was
sible, in order to adhere to the goal of emulation, as   developed, which deviates from the standard prompt
described in section [3.3]. Therefore, no direct spec-   only in the first section:
ification is given as to which pragma statements to
generate.                                                Listing 4: The beginning of Marmaragan’s chain-of-thought
                                                         prompt
    It also includes the request that the code not be
                                                         Try to solve the following problem by first
modified in any way, other than to add pragma state-
                                                         explaining in natural language what the underlying
ments and possibly include structures such as “for”      problem , leading to the medium , might be and how
loops and “if” statements.                               it could be solved .
    Additionally, when prompting LLMs with                                        ...
LangChain, it is possible to provide a system mes-
sage. The system message conveys to the LLM its              Based on the results of the papers presented in
context and which role it should take within the given   2.3.1, this prompt aims to make the LLM explain,
context. As the system message for OpenAI GPT            in natural language, how it will go about proving the
models is capped at 512 characters, the message          code. The hope is that this approach forces the model
chosen sticks to the key points the model should         to reason more soundly. After explaining how it will
adhere to. The system message used is displayed          solve the given program, it is then tasked with imple-
below, in listing [3].                                   menting this solution, all in one step, similar to the
                                                         Zero-Shot Chain-of-Thought approach (Kojima et al.,
    Listing 3: The system message passed to the LLM      2023).
You are a Spark2014 / ADA programmer with
strong logical reasoning abilities .                     3.4.5   N-Solutions

You will be given an Implementation of a program ,       The N-Solutions and Retries parameters are funda-
a specification of the program and the mediums           mental instruments which can be employed to in-
that GnatProve raised for it .                           crease the benchmarking success rate. N-Solutions
                                                         determines the number of responses an LLM returns,
You must complete the package body of the given
                                                         per individual prompt. At N = 1, the LLM supplies a
program , inserting one or multiple pragma
statements .
                                                         single response to a given prompt, at N = 5 it returns
                                                         five responses. Due to how generation is affected by
You must not modify the code in any other way ,          the temperature parameter, each of the N-Solutions
except to add for loops and if statements that           are in most cases distinct.
enclose only pragma statements , and do not
modify the functionality .                               3.4.6   Retries

3.4.3   Medium in Prompt                                 Setting the Retries parameter to a value graeater than
                                                         0 makes Marmaragan continue with retries after a
Further, the prompt may be enhanced with additional      first failed attempt at generating pragmas that verify
context, by enabling the medium-in-prompt feature.       the code. The Retries mechanism works by provid-
When this feature is enabled, GNATprove compiles         ing the LLM with additional context in the form of
the SPARK project and any mediums from the out-          the previous failed attempt and the medium messages
put are extracted and formatted. In this case, format-   generated by GNATprove in that attempt. This ad-
ting involves taking the line number and extracting      ditional context helps the model to formulate a new
the related line of code (and the one below) from the    solution attempt. Increasing the number of Retries
SPARK file. The line of code and the medium mes-         leads to the additional solution attempts, each con-
sage is then appended to the prompt. Figure 2 gives      taining more context than the last.
an example of this.

3.4.4   Chain-of-Thought Prompt                          4    BENCHMARKING
As discussed in Section 2.3.1, chain-of-thought
                                                         This section discusses the programs selected for
prompting (Jason Wei et al., 2023; Kojima et al.,
                                                         benchmarking. This includes why the programs were
      Figure 2: Example of Gnatprove precompiled and formatted medium messages, which are added to the prompt


chosen, where they were sourced from and how dif-           errors and medium. By taking programs which are al-
fering benchmarks were assembled from these.                ready verified, we are sure that a correct solution ex-
                                                            ists. Additionally, utilizing existing programs makes
4.1    Programs                                             it possible to better curate which types of annotations
                                                            to generate.
In total, 16 SPARK 2014 programs were selected,
from three differing sources:                               4.3    Five Benchmarks
 • Five programs originate from the Argu Reposi-
   tory, [Link](Cramer, 2023), which is a verified          In total, from the 16 programs, five benchmarks were
   tool written by Marcos Cramer for computing ab-          developed with differing aims. For each benchmark,
   stract argumentation semantics, with a focus on          a separate schema for removing pragma statements
   finding the grounded extension of an argumenta-          from the programs was devised. For some schemas,
   tion framework and proving its uniqueness. It was        it was possible to do this multiple times per program.
   first published after the cutoff dates for the train-    pragma statements are removed only from the imple-
   ing of GPT-4 and GPT-4o, so that unlike for the          mentation file (.adb) of the SPARK project. After re-
   other programs in the benchmark, we can be cer-          moving pragmas from a program, we run GNATprove
   tain that it was not included in the training data of    to check whether any mediums are generated. A pro-
   these LLMs.                                              gram with removed pragmas is only included in the
                                                            benchmark if GNATprove generates mediums for it,
 • The spark tutorial [Link], where the
                                                            because otherwise it can be considered to be already
   linear search and show map programs were
                                                            fully verified, so that Marmaragan has no work to do
   taken from.
                                                            on it.
 • A repository of SPARK 2014 implementations
   of common algorithms, known as spark-by-
   example [Link], where the final 11 programs
   were taken from, including basic implementations
   of copy and f ind algorithms, but also more com-
   plex programs such as search lower bound.

4.2    Determining a Metric for Results
       Evaluation
The choice was made to work with pre-existing, for-
mally verified SPARK 2014 projects, as this made the
task of evaluating the results from the benchmarks
possible.
    Quantifying how close a given solution is to be-
ing formally verified is very challenging. GnatProve
provides no feedback in regards to this, excepting
medium messages. These provide feedback about
                                                            Figure 3: This chart details the distribution of programs
which statements lead to a failure in verification, but
                                                            from each of the three sources across the five benchmarks
the total number of medium messages is not indica-
tive of the closeness to a completed verification. A        All Pragmas
manual analysis is also not feasible, given the num-
ber of benchmark programs and the total number of             • All    pragma statements of             the form
solutions generated.                                            Loop Invariant, Loop Variant,          and Assert
    Thus, it is only possible to evaluate correctness by        are removed.
checking whether the program is completely free of            • 14 programs total
Last Invariant All Loops                                   devised. The aim was to derive the effectiveness of
 • The last pragma Loop Invariant is removed from          the N-Solutions and Retries parameters. Various com-
   each loop in the file. If multiple loops occur in the   binations of each of the parameters were conceived to
   same file, then multiple statements are removed.        test this. A central goal of these tests was to determine
                                                           what balance between n (N-Solutions) and r (Retries)
 • 12 programs total                                       was ideal in order to get the best results given a fixed
All Pragmas One Loop                                       amount of computational resources available for com-
 • All pragma statements are removed from a single         pleting the verification of a program.
    loop, only for loops with two or more loop invari-         Given the values n and r for the N-Solutions and
    ant statements.                                        Retries parameters, the number of solutions generated
                                                           by the program is limited to a maximum of n(r + 1),
 • 16 programs total
                                                           because n solutions are generated for the first attempt
Last Invariant One Loop                                    and n further ones for each of the r retries. The total
 • The last pragma Loop Invariant is removed from          number of solutions to be generated per benchmark
   a single loop.                                          program was set to 12, as this made various combina-
 • 22 programs total                                       tions of n and r possible, while keeping costs within
                                                           the limits set. The resulting combinations were the
One Assert                                                 following:
 • A single Assert is removed.                             (n , r) combinations :
 • 7 programs total                                            (12 , 0) , (6 , 1) ,   (4 , 2) ,   (3 , 3) ,   (2 , 5)


   Figure [3] displays a bar for each of the bench-
marks, detailing the distribution of the source pro-       5.3    Experiment Results
grams.
                                                           Table 1 details the results of each of the five experi-
                                                           ments on each of the five benchmarks.
                                                                In total 36 programs out of 71 were solved across
5     RESULTS                                              all five benchmarks, meaning a solution was found for
                                                           50.7% of all benchmark problems.
This section presents the findings from experiments
                                                                Figure 4 is a graphical interpretation of Table 1.
with Marmaragan. The aim was to evaluate Mar-
maragan’s performance across various benchmarks,
while varying the individual parameters of the tool.
Through a series of experiments, we attempt to mea-
sure the effectiveness of the tool and extract how
the parameter N-Solutions and Retries interact with
each other.

5.1    GPT-4o Release
Early experiments conducted on the benchmark with
vanilla GPT-4 demonstrated promising, albeit not
entirely satisfying, results. However, shortly after
these initial trials, GPT-4o was released. Not only
did small scale experiments indicate that this new
model was more successful overall, importantly, they
also demonstrated that GPT-4o was far more cost-
effective. This made larger experiments feasible. The
main experiments were performed with the model
gpt-4o-2024-05-13.                                         Figure 4: Comparison of the number of programs solved per
                                                           experiment. The bar is composed of the stacked number of
                                                           solutions per benchmark.
5.2    Experiment Setup
                                                              A further graphical representation of the data is
Adjusting for these new possibilities, a large scale ex-   Figure 5. The number of successfully solved pro-
periment to test the capabilities of Marmaragan was        grams, compared to the total number of programs in
Table 1: The results of five experiments with unique combinations of N-Solutions and retries, over five different benchmarks.
The final column displays the total number of programs solved across all benchmarks.
                       All pragmas   Last invariant all loops   One assert       All pragmas one loop   Last invariant one loop   Sum

           n=12, r=0       3                    4                   5                     2                        6              20
           n=6, r=1        2                    3                   6                     1                       12              24
           n=4, r=2        3                    4                   7                     3                        7              24
           n=3, r=3        2                    4                   7                     0                        7              20
           n=2, r=5        2                    4                   6                     0                        6              18




the benchmark, is depicted through a 100% bar chart,                         rerun were more successful than the initial runs, lead-
to contrast performance on each of the benchmarks,                           ing to a total of 25/71 successfully solved programs
per experiment.                                                              for n = 4, r = 2 and 26/71 for n = 6, r = 1.
    Figures 6 and 7 contrast the effectiveness of suc-
cessive retries and N-Solutions. Important to note                           5.6       Chain of Thought Experiment
here is that while one parameter is varied, the other
is kept constant. In essence, each of the selected ex-                       The Chain-of-Thought experiment refers to a fur-
periments was analyzed and the number of successful                          ther experiment conducted, which differentiates itself
solutions was counted at each step, keeping one of the                       from the main experiment in its prompting strategy.
two parameters constant.                                                     See section 3.4.4 for an explanation.
                                                                                 Using the set of parameters with the highest rate
5.4    Argu Results                                                          of successfully generated solutions: n = 6, r = 1, the
                                                                             experiment was conducted. In total, 25/71 programs
The programs that originate from Argu (see Sec-                              were solved, equaling the average of the success rates
tion 4.1) are of high significance, as the programs                          from the original experiment and the verification run.
cannot be part of GPT-4o’s training data1 . Thus, this
makes it a notable benchmark, as the solutions could
not have been learned, but had to be produced by                             6      DISCUSSION
the LLM without having seen the full program dur-
ing pre-training.                                                            This section analyses the results of the experiments
    Along with the programs being completely new                             conducted with Marmaragan.
for the LLM, the subject matter of the programs is
also niche. Abstract argumentation theory is likely
not among the major fields of academic research, and                         6.1       General observations
literature surrounding this topic is likewise uncom-
mon. This makes the programs from the Argu repos-                            Experiments on the benchmark demonstrate Mar-
itory potentially the most challenging in the bench-                         maragan’s competence in generating annotations,
mark. With these premises in place, the results                              both in the case of Assert statements and in the
achieved by Marmaragan are surprising. Argu pro-                             case of loop invariants, with a higher level of compe-
grams comprised just over half of the programs in the                        tence for Assert statements than for loop invariants.
benchmark, totaling 36 out of 71. Out of these 36                            Overall, it generated correct annotations for 36 out
programs, 16 were solved.                                                    of 71 (50.7%) of the benchmark cases. These results
                                                                             highlight the potential for integrating formal verifica-
                                                                             tion into AI-assisted development, paving the way for
5.5    Verification of Results                                               safer and more reliable AI-generated software.
Despite additional API costs, a replication of the two
most successful experiments was conducted to at-                             6.2       N-Solutions and Retries Parameters
tempt to show reproducibility. The two most success-
ful runs were n = 6, r = 1 and n = 4, r = 2, each                            Increasing the N-Solutions parameter, which deter-
reaching 24/71 solutions. These two were rerun, in                           mines the number of initial solution attempts, gener-
order to check reproducibility. The results from this                        ally led to improved success rates in solving bench-
                                                                             mark problems. The retry mechanism, which allows
    1 If we take the statistics from Open AI’s website to be                 Marmaragan to attempt corrections based on error
up-to-date, at the time of writing, and provided the informa-                feedback, also proved to be an effective strategy. In
tion is reliable.
Table 2: Breakdown of the number of programs solved in total, for each benchmark. The bottom row is the number of
programs in the benchmark.
                          All pragmas   Last invariant all loops   One assert   All pragmas one loop   Last invariant one loop   Sum

     Total solved              5                   6                   7                 4                       14              36
     Total in benchmark       14                  12                   7                16                       22              71




Figure 5: Summary of the total amount of programs solved, per benchmark, across all five experiments. The chart is a 100%
bar chart, thus the y-axis represents the amount of programs that were solved, as a percentage of the total number of programs
in the benchmark.




Figure 6: An overview of the efficacy of N-Solutions, be-                   Figure 7: An overview of the efficacy of successive retries,
tween n=1 and n=6. The retries parameter is kept constant                   between r=0 and r=5 (N-Solution parameter constant).

many cases, experiments that incorporated retries out-                      n = 6, r = 1 and n = 4, r = 2 yielded the best results,
performed those that relied solely on generating new                        solving 24 out of 71 programs each. This suggests
solutions. This suggests that the model can effectively                     that a balance between initial solution attempts and
use error information to refine its approach.                               correction opportunities is more effective than relying
    The experiments reveal a complex interplay be-                          on either approach alone.
tween N-Solutions and retries. The combinations of                              As can be seen in Figures 6 and 7, higher values
of the N-Solutions end Retries parameters have demi-       enhances results, solving 65.7% of PISA problems,
nishing returns. This is not surprising, as the model      showcasing complementary strengths.
exhausts its most promising approaches in the first            The Draft-Sketch-Prove (DSP) approach (Jiang
few attempts, with subsequent attempts becoming less       et al., 2023b) addresses autoformalization by trans-
likely to yield new solutions.                             forming informal mathematical proofs into verified
                                                           formal proofs through three steps: drafting informal
                                                           proofs, generating formal sketches, and completing
7    RELATED WORK                                          gaps using automated provers. Using human-written
                                                           and LLM-generated informal proofs, DSP achieves
We are not aware of any work that brings LLMs and          state-of-the-art performance on the MiniF2F bench-
formal software verification together in the same way      mark, solving 42.6% and 40.6% of validation prob-
as we have proposed in this paper. But there is related    lems, respectively. Ablation studies highlight the im-
work on leveraging LLMs for theorem proving and            portance of comments, multi-step reasoning, and in-
autoformalization in mathematics, from which valu-         tegrating ATP tools like Sledgehammer.
                                                               Magnushammer (Mikuła et al., 2024) uses a
able insights can be drawn for applying these tech-
                                                           transformer-based architecture to address premise se-
niques to the verification of software. This section
                                                           lection, bypassing the need for extensive engineering.
reviews key works that inform our approach. These
                                                           By training on premise selection datasets, it combines
studies provide context for the capabilities and limita-
                                                           SELECT and RERANK algorithms to embed proof
tions of LLMs in formal reasoning, which Marmara-
                                                           states and premises into a shared latent space, en-
gan seeks to extend to software verification.
                                                           abling relevance scoring. Magnushammer achieves
    Thor (Jiang et al., 2023a) combines language
models (LMs) with automated theorem proving sys-           state-of-the-art results on PISA, solving 59.5% of
tems using hammers to improve formal proof gen-            problems, and boosts Thor’s performance to a 71%
eration. Hammers are tools that bridge the gap be-         success rate when replacing Sledgehammer as the
tween Interactive Theorem Provers (ITPs), which as-        premise selection tool.
sist users in formulating proofs, and Automated The-
orem Provers (ATPs), which independently verify
conjectures. They achieve this by translating proof        8    FUTURE WORK
steps into ATP-compatible formats, selecting relevant
premises, and integrating the ATP’s solutions back         Marmaragan demonstrates the feasibility of an AI-
into the ITP, enabling automated reasoning for indi-       powered annotation generator for SPARK 2014, but
vidual proof steps (Blanchette et al., 2016). Sledge-      there remain several opportunities for further research
hammer (Paulson, 2012) is a hammer for the Is-             and development.
abelle (Paulson, 1994) ITP. Thor functions as follows:         One potential direction is enabling the generation
given a theorem and assumptions, it proves the con-        of pre- and postconditions by the LLM itself. Devel-
jecture by first allowing the LM to devise the proof       opers could define contracts for high-level functions,
steps, then appending < hammer > annotations to            while the AI refines contracts for the invoked lower-
individual sections, allowing Sledgehammer to com-         level functions to preserve program correctness.
plete the rest of the proof. Tested on the PISA and            Testing Marmaragan on a benchmark of 16 pro-
MiniF2F benchmarks, Thor demonstrated higher suc-          grams yielded initial results, but validating its robust-
cess rates than individual components like Sledge-         ness and generalizability requires a larger dataset. Fu-
hammer, solving 57% of PISA benchmark problems.            ture benchmarks should include diverse SPARK pro-
Despite its innovative approach, subsequent methods        grams spanning various domains and complexities.
like Baldur have surpassed Thor’s results, utilizing           Long-term goals include evolving Marmaragan
newer LLM technologies.                                    into an industrial-grade tool, akin to how Copilot in-
    Baldur (First et al., 2023) generates entire for-      tegrates into IDEs, by providing real-time annotation
mal proofs from theorem statements using LLMs and          suggestions during SPARK code development.
features a proof-repair mechanism that utilizes error          Finally, an exciting avenue for long-term research
messages to refine failed proofs. Unlike step-by-step      based on the ideas in this paper would be to explore
proof generation, Baldur constructs full proofs and as-    the possibility of employing LLMs to generate entire
sesses their validity. It achieves a 47.9% success rate    formally verified programs based on a conversation
on the PISA benchmark and demonstrates the effec-          between a human project manager and an LLM about
tiveness of proof repair and additional context for im-    the intended behavior of the program.
proving performance. Combining Baldur with Thor
9    CONCLUSION                                               Chapman, R., Dross, C., Matthews, S., and Moy, Y. (2024).
                                                                     Co-developing programs and their proof of correct-
This paper introduced Marmaragan, a proof-of-                        ness. Commun. ACM, 67(3):84–94.
concept tool for generating SPARK 2014 annota-                Chapman, R. and Schanda, F. (2014). Are we there yet?
tions using LLMs. It integrates GNATprove to check                   20 years of industrial theorem proving with SPARK.
                                                                     In Klein, G. and Gamboa, R., editors, Interactive The-
whether the annotations complete the verification of                 orem Proving, pages 17–26, Cham. Springer Interna-
the code. Marmaragan is thus a hybrid AI system that                 tional Publishing.
combines the power of LLMs with the trustworthiness           Chase, H. (2022).               LangChain Python Library.
of logic-based reasoning tools. Key techniques in the                https://github.com/langchain-ai/langchain.
implementation of Marmaragan include utilizing pre-           Cramer,             M.        (2023).                    argu.
compiled GNATprove mediums, generating multiple                      https://github.com/marcoscramer/argu.
solutions, retrying with additional context, and op-          Dross, C., Efstathopoulos, P., Lesens, D., Mentr, D., and
tional chain-of-thought prompting.                                   Moy, Y. (2014). Rail, space, security: Three case stud-
    Benchmarking on 16 curated SPARK programs                        ies for SPARK 2014.
demonstrated Marmaragan’s capabilities, particularly          Filliâtre, J.-C. and Paskevich, A. (2013). Why3 — where
in generating Assert statements. The tool was able                   programs meet provers. In Felleisen, M. and Gard-
to solve 36 out of 71 benchmark cases.                               ner, P., editors, Programming Languages and Systems,
                                                                     pages 125–128, Berlin, Heidelberg. Springer Berlin
    This work highlights the potential for integrat-                 Heidelberg.
ing formal verification into AI-assisted development,
                                                              Filliâtre, J.-C. (2011). Deductive software verification. In-
paving the way for safer and more reliable AI-                       ternational Journal on Software Tools for Technology
generated software.                                                  Transfer, 13:397–403.
                                                              First, E., Rabe, M. N., Ringer, T., and Brun, Y. (2023).
                                                                     Baldur: Whole-proof generation and repair with large
ACKNOWLEDGEMENTS                                                     language models.
                                                              Hoare, C. A. R. (1969). An Axiomatic Basis for Computer
                                                                     Programming. Communications of the ACM.
We would like to acknowledge the work done by Em-
                                                              Jason Wei, X. W., Schuurmans, D., Bosma, M., Ichter, B.,
manuel Debanne. Based on ideas of the first co-
                                                                     Xia, F., Chi, E., Le, Q., and Zhou, D. (2023). Chain-
author of this paper, Emmanuel developed Sparkilo, a                 of-thought prompting elicits reasoning in large lan-
closed-source tool similar to Marmaragan for generat-                guage models.
ing annotations for SPARK 2014 programs, including            Jiang, A. Q., Li, W., Tworkowski, S., Czechowski, K.,
features such as retries and chain of thought prompt-                Odrzygóźdź, T., Miłoś, P., Wu, Y., and Jamnik, M.
ing. Sparkilo provided a great foundation for the ideas              (2023a). Thor: Wielding hammers to integrate lan-
presented in this paper and laid out the groundwork                  guage models and automated theorem provers. Jour-
for many of the features implemented in Marmaragan.                  nal of Formal Methods.
Two functions authored by Emmanuel were included              Jiang, A. Q., Welleck, S., Zhou, J. P., Li, W., Liu, J., Jam-
in Marmaragan.                                                       nik, M., Lacroix, T., Wu, Y., and Lample, G. (2023b).
                                                                     Draft, sketch, and prove: Guiding formal theorem
    Additionally, we would like to acknowledge the                   provers with informal proofs.
support of Tobias Philipp from secunet Security Net-          Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., and Iwasawa,
works AG, who supported the two co-authors of this                   Y. (2023). Large language models are zero-shot rea-
paper in the development of Marmaragan through his                   soners.
expertise in SPARK 2014.                                      Mikolov, T., Chen, K., Corrado, G., and Dean, J. (2013).
                                                                     Efficient estimation of word representations in vector
                                                                     space.
REFERENCES                                                    Mikuła, M., Tworkowski, S., Antoniak, S., Piotrowski,
                                                                     B., Jiang, A. Q., Zhou, J. P., Szegedy, C., Łukasz
                                                                     Kuciński, Miłoś, P., and Wu, Y. (2024). Magnusham-
AdaCore (1980). Ada programming language. https://ada-               mer: A transformer-based approach to premise selec-
     lang.io/.                                                       tion.
Barnes, J. (2012). High Integrity Software: The SPARK
                                                              Moi, Y. (2013). SPARK 2014 rationale. Ada User Journal,
     Approach to Safety and Security. Addison-Wesley.
                                                                     34(4):243–254.
Blanchette, J. C., Kaliszyk, C., Paulson, L. C., and Urban,
                                                              Moy, Y., Ledinot, E., Delseny, H., Wiels, V., and Monate,
     J. (2016). Hammering towards QED. Journal of For-
                                                                     B. (2013). Testing or formal verification: DO-178C
     malized Reasoning, 9(1):101–148.
                                                                     alternatives and industrial experience. IEEE Software,
Brosgol, B. M. (2019). How to succeed in the software busi-          30(3):50–57.
     ness while giving away the source code: The AdaCore
     experience. IEEE Software, 36(6):17–22.
Paulson, L. (2012). Three years of experience with sledge-
     hammer, a practical link between automatic and inter-
     active theorem provers. In Schmidt, R. A., Schulz, S.,
     and Konev, B., editors, PAAR-2010: Proceedings of
     the 2nd Workshop on Practical Aspects of Automated
     Reasoning, volume 9 of EPiC Series in Computing,
     pages 1–10. EasyChair.
Paulson, L. C. (1994). Isabelle: A generic theorem prover.
Pennington, J., Socher, R., and Manning, C. D. (2014).
     Glove: Global vectors for word representation. Con-
     ference on Empirical Methods in Natural Language
     Processing (EMNLP), pages 1532–1543.
Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones,
     L., Gomez, A. N., Kaiser, L., and Polosukhin, I.
     (2017). Attention is all you need. Advances in Neu-
     ral Information Processing Systems (NeurIPS), pages
     5998–6008.
