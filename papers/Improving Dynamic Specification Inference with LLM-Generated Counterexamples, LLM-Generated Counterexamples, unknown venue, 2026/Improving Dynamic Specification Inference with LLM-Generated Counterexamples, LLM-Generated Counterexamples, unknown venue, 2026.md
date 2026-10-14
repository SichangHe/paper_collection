                                             Improving Dynamic Specification Inference with
                                                    LLM-Generated Counterexamples
                                                                         Agustı́n Balestra∗ , Agustı́n Nolasco∗¶ , Facundo Molina† ,
                                                                   Diego Garbervetsky‡¶∥ , Renzo Degiovanni§ , and Nazareno Aguirre∗¶∥
                                                    ∗ University of Rio Cuarto, Rio Cuarto, Argentina, {ebalestra, nolasco, naguirre}@dc.exa.unrc.edu.ar
                                                                      † Complutense University of Madrid, Madrid, Spain, facundom@ucm.es
                                                                     ‡ University of Buenos Aires, Buenos Aires, Argentina, diegog@dc.uba.ar
                                                           § Luxembourg Institute of Science and Technology, Luxembourg, renzo.degiovanni@list.lu
                                                                  ¶ National Council for Scientific and Technical Research (CONICET), Argentina
                                                                        ∥ Guangdong Technion-Israel Institute of Technology, Shantou, China
arXiv:2604.10761v1 [cs.SE] 12 Apr 2026




                                            Abstract—Contract assertions, such as preconditions, postcon-        a similar approach: a mechanism is employed for generating
                                         ditions, and invariants, play a crucial role in software develop-       candidate assertions for different program points (precondi-
                                         ment, enabling applications such as program verification, test          tions, postconditions, etc.), which are then assessed against a
                                         generation, and debugging. Despite their benefits, the adoption
                                         of contract assertions is limited, due to the difficulty of manually    given test suite. Failing assertions, i.e., assertions invalidated
                                         producing such assertions. Dynamic analysis-based approaches,           by at least one test case, are discarded, while those assertions
                                         such as Daikon, can aid in this task by inferring expressive asser-     that are found to be valid for the provided suite are likely
                                         tions from execution traces. However, a fundamental weakness            specifications (or likely invariants). Likely invariants are either
                                         of these methods is their reliance on the thoroughness of the test      directly reported back to the user as likely specifications, or
                                         suites used for dynamic analysis. When these test suites do not
                                         contain sufficiently diverse tests, the inferred assertions are often   are the basis of what will be reported, as some tools perform a
                                         not generalizable, leading to a high rate of invalid candidates         posteriori assertion filtering to reduce redundancy [27], [33].
                                         (false positives) that must be manually filtered out.                      All these techniques face a common problem, inherent to
                                            In this paper, we explore the use of large language models           this kind of analysis: the quality of the inferred assertions
                                         (LLMs) to automatically generate tests that attempt to invalidate       greatly depends on the quality of the test suite, and even for
                                         generated assertions. Our results show that state-of-the-art LLMs
                                         can generate effective counterexamples that help to discard up to       thorough and diverse test suites, these techniques typically
                                         11.68% of invalid assertions inferred by SpecFuzzer. Moreover,          report false positives, i.e., spurious or invalid assertions which
                                         when incorporating these LLM-generated counterexamples into             hold at the corresponding program points when observed in
                                         the dynamic analysis process, we observe an improvement of up           executions of the given test suite, but are invalid in the general
                                         to 7% in precision of the inferred specifications, with respect         case [13], [27], [29], [33]. A direct approach to deal with
                                         to the ground-truths gathered from the evaluation benchmarks,
                                         without affecting recall.                                               this issue is to inspect the produced assertions, and manually
                                            Index Terms—Specification inference. Contract assertions.            identify and discard invalid ones, before using the produced
                                         Runtime analysis. Large language models.                                assertions for downstream analyses. However, this is time
                                                                                                                 consuming and error-prone, and is exacerbated as tools for
                                                                I. I NTRODUCTION                                 specification generation grow in specification expressiveness,
                                            Software specifications are abstract descriptions of the in-         and thus in the kinds of specifications they are able to report.
                                         tended behavior of software systems [16]. Software specifi-                In this paper, we assess to what extent Large Language
                                         cations are crucial to relate user needs to software behavior,          Models (LLMs) are effective in automating specification in-
                                         and to perform different software analyses, such as program             validity detection. The motivation is straightforward: if LLMs
                                         verification [23], test generation [7], [10], [24], and program         are effective at detecting invalid assertions, then the burden on
                                         repair [25], [30]. While formal specifications have many ad-            the engineer can be reduced, as the likely specifications to be
                                         vantages and can be exploited for powerful analyses, they are           manually examined can be significantly reduced. To analyze
                                         known to be difficult to produce, in particular due to difficulties     the effectiveness of LLMs for this task, we take a represen-
                                         in formally expressing program intent. Thus, specifications are         tative tool among the above-mentioned techniques, namely
                                         rarely seen in practice, accompanying software.                         SpecFuzzer [27], and introduce an additional stage in the
                                            To address this problem, researchers have developed tech-            standard generate-filter-reduce pipeline of dynamic analysis
                                         niques for automatically inferring specifications from other            specification generation techniques: after filtering assertions
                                         existing software elements. At the level of source code in              via dynamic analysis, we instruct an LLM to decide whether
                                         particular, a family of approaches starting with Daikon [13],           the assertion is valid (i.e., holds at the corresponding program
                                         a foundational tool in this area, generate specifications in            point for every valid run of the software under analysis)
                                         the form of program assertions by resorting to dynamic                  or not. Since this process is likely to be inaccurate and
                                         analysis [13], [27], [29], [33]. All these approaches follow            thus lead us to discard valid assertions, we ask the LLM
to produce, when a likely invariant is deemed invalid, a test        instantiating specification templates with program expressions,
case witnessing the invalidity of the generated assertion. This      obtaining in this way candidate assertions, and then monitoring
approach introduces test generation after the assertions have        program executions at specific program points, such as method
been produced, thus focusing test generation on the task of          entrance and exit points, to assess which candidate expressions
invalidating produced assertions already validated by dynamic        hold in all these observations at the considered program points.
analysis. The purpose is to exploit dynamic analysis on the          Daikon reports the properties that were not falsified by any
provided test suite to reliably discard assertions, and thus focus   test, as likely invariants (invariants in the sense that these
the task of the LLM in the more challenging assertions that          were found to invariantly hold at the observed program points).
dynamic analysis already “accepted”. The LLM then acts as            Daikon is very useful and has enabled various other techniques
an automated intelligent oracle, that partially simulates the        for program analysis. However, the technique is known to have
traditionally human task of inspecting produced assertions,          expressiveness limitations, and to have its precision subject to
identifying false positives (spurious assertions), and removing      the thoroughness of the test suite used for inference.
them. By requesting invalidating test cases in our queries to           Various techniques have been proposed to enhance Daikon’s
the LLM, we can verify the invalidity of the assertions by           dynamic analysis based inference, tackling in particular ex-
executing the produced test cases and confirming assertion           pressiveness limitations and the number and quality of the
failure. In this way, we only remove assertions that the LLM         reported likely invariants. GAssert [33] and EvoSpex [29]
deemed invalid and could certify such invalidity via test cases.     employ evolutionary approaches to generate postconditions
   We evaluate this LLM-enhanced technique on a combined             that are validated against a given test suite. SpecFuzzer [27]
benchmark from GAssert [33] and EvoSpex [29]. Our ex-                provides higher flexibility and expressiveness by allowing
periments consider three state-of-the-art LLMs from different        specifications to be generated via grammar-based fuzzing
families, namely, GPT-5.1 from Open AI, Llama 3.3 70B from           from a user-provided grammar, and using dynamic analysis
Meta, and DeepSeek-R1. In order to more reliably assess the          to validate the generated specifications in the style of Daikon
accuracy of the inferred specifications, we employ the curated       and other previous tools. All these tools and techniques make
ground truth statements provided in [27] for the GAssert and         attempts to improve the quality of reported specifications,
EvoSpex benchmarks, to implement automated ground truth              e.g., employing mutation-based filtering or evolution towards
checkers using SMT and SAT solvers. These checkers are used          stronger assertions, to reduce redundancy. Despite differences
to assess accuracy in our experiments.                               in candidate generation strategies, all these techniques funda-
   Our experimental results show that the counterexamples            mentally rely on the strength and thoroughness of the em-
generated by GPT-5.1 help us to discard a total of 1,877 invalid     ployed test suites for dynamic analysis, to reduce the number
specifications inferred by SpecFuzzer, while Llama 3.3 70B           of invalid assertions generated. All these dynamic analysis
discards 1,048 invalid assertions, and DeepSeek-R1 discards          based techniques suffer from the problem of generating false
2,173. This LLM-based filtering reduces in 10.09%, 5.63%,            positives due to the inherently partial nature of test suites as
and 11.68%, respectively, the noise in the inferred specifica-       behavior specifications.
tions, which otherwise would have required additional manual            Recently, various specification inference techniques have
inspection and validation. In terms of accuracy, we observe          been proposed that directly incorporate LLMs in the specifica-
that SpecFuzzer+GPT-5.1 obtains 74.17% precision, 54.57%             tion generation process [12], [17], [22], [28], or use LLMs to
recall, and 53.94% F1-score, with respect to the ground-             generate other forms of specifications, such as test assertions
truths gathered from the benchmarks that we implemented in           or metamorphic relations [32], [38]. Unlike these techniques,
automated SAT/SMT checkers, a ∼7% precision improvement              our approach does not modify the invariant generation or
with respect to SpecFuzzer. Moreover, Llama 3.3 70B and              validation mechanisms themselves. Instead, it introduces a
DeepSeek-R1 also improve SpecFuzzer’s precision by ∼3.5%             supplementary post-processing step that actively targets invalid
and ∼8%, respectively. These encouraging results suggest that        assertions (false positives) by generating focused counterexam-
LLMs have a significant potential in improving specification         ples, guided by an LLM, after candidate postconditions have
inference accuracy, thus reducing the engineering effort of the      already been inferred.
manual examination of generated specifications.
                                                                     B. Oracle Assessment
          II. BACKGROUND AND R ELATED W ORK                             The problem of assessing and improving test oracles has
  This work regards various different research areas, most           been widely studied in software testing research [19], [21],
notably dynamic specification inference, oracle assessment,          [26]. OASIs [21] systematically detects these deficiencies
and the use of LLMs in test generation and program analysis.         using evolutionary search. False positives are revealed by
                                                                     generating test cases that violate the oracle, while false neg-
A. Dynamic specification inference                                   atives are identified via mutation analysis. OASIs [21] has
  Dynamic specification inference aims at automatically pro-         been used both as a quality metric and as a support tool
ducing program properties from execution scenarios. A re-            for oracle refinement in several studies. Previous research has
markable contribution to this area, and a seminal technique          also focused on oracle quality, with techniques and tools such
and tool, is Daikon [13]. Daikon infers likely invariants by         as OraclePolish [19], which employs dynamic taint analysis
to detect unused inputs and brittle assertions (assertions that        public class QueueAr {
depend on uncontrolled inputs and thus may be invalidated).              private Object [] theArray;
                                                                         private int currentSize, front, back;
   Our work is conceptually aligned with OASIs and Ora-
clePolish in that we aim to generate counterexamples that                  /**
expose false positives in inferred specifications. However, we             * Get the least recently inserted item in the queue.
                                                                           * Does not alter the queue.
differ substantially in methodology: rather than relying on                */
evolutionary search or dynamic taint analysis, we leverage the             public Object getFront() {
reasoning and code generation capabilities of LLMs to directly                Object result;
                                                                              if(isEmpty()) {
synthesize counterexamples. Moreover, our approach is specif-                   result = null;
ically tailored to dynamically inferred assertions and integrates             } else {
seamlessly with existing specification inference pipelines.                     result = theArray[front];
                                                                              }
C. Large Language Models for Software Testing and Analysis                    return result;
                                                                           }
   Recent years have seen growing interest in leveraging LLMs              ...
                                                                       }
for software engineering, including their application in tasks
such as code generation, program repair, and test genera-                                      (a) Target method.
tion [18]. LLMs have been shown to be effective at various
                                                                       // Postcondition: (currentSize == front implies front < 1)
complex software engineering tasks, including generating unit          assert (this.currentSize != this.front || this.front < 1)
tests, understanding program semantics, and reasoning about
program behavior from source code [34]. In particular, various                      (b) Postcondition inferred by SpecFuzzer.
studies have explored the use of LLMs to generate test                 @Test
cases with the aim of improving code coverage or exposing              public void testGetFront_1() throws Throwable {
bugs [8], [9], [14], [31], [35], [37]. Additional recent work              // Spec: (currentSize = front) implies (front < 1)
                                                                           QueueAr queue = new QueueAr(10);
investigates the effectiveness of LLMs for extracting software
specifications from software documentation [36].                             queue.enqueue("Item 1");
   Our work differs from prior LLM-based testing and test gen-               queue.dequeue(); // This makes the queue empty again
eration methodologies in two fundamental ways. First, rather                 // Check the postcondition when the queue is empty
than employing LLMs for the general problem of generating                    assertTrue(queue.getFront() == null);
test cases, we leverage them to produce tests that serve as
                                                                             queue.enqueue("Item 2");
targeted counterexamples to falsify specific inferred specifica-             // Test that getFront() returns the correct item when
tions, such as candidate program postconditions. Second, we                   the queue is not empty
constrain the model to output executable code that serves as                 assertTrue(queue.getFront().equals("Item 2"));
                                                                       }
a concrete witness of incorrectness, as opposed to providing
unstructured natural language assessments of specification va-                         (c) LLM-generated counterexample.
lidity. This design philosophy enables the automated validation
of LLM-generated responses and ensures that the resulting              Fig. 1: Situation where an LLM-generated counterexample
artifacts are executable. This implies that these responses can        contradicts the inferred postcondition. Figure a) shows the
eventually be integrated into a dynamic loop to refine and             target method under analysis. Figure b) shows an incorrect
improve an underlying specification inference process.                 postcondition inferred by SpecFuzzer for this method. Figure
                                                                       c) shows a test case generated by an LLM that contradicts the
                III. I LLUSTRATIVE E XAMPLE                            inferred postcondition, thus showing it is a false positive.
   This section presents an illustrative example to demonstrate
how LLMs can enhance dynamic specification inference.
Specifically, we show how LLMs can identify false positives,           of the queue is returned, otherwise null is returned. Besides,
incorrect assertions that despite being valid in the observations      the queue’s observable state after the call must be identical to
considered by the dynamic analysis (restricted to the test             its state before the call (also part of the postcondition). The
suite being considered), are invalid in the general case. As           implementation logic is straightforward: it first checks if the
mentioned previously, the LLMs will be instructed to provide           queue is empty, in which case it returns null; otherwise, it
test cases that confirm the invalidity of the identified assertions.   accesses and returns the element stored at the front index of
   As a simple example, consider an array-based implemen-              the underlying array, without modifying any structural fields.
tation of a queue data structure, which includes a method                 To illustrate the automated specification inference, consider
named getFront (see Figure 1(a)). The method’s intended                the application of SpecFuzzer [27] to infer postconditions
behavior is to return the least recently inserted element—the          for the getFront method of our QueueAr example. Given
item at the logical front of the queue—while preserving the            a representative test suite, the tool generates a substantial set
queue’s state. Formally, this constitutes a postcondition: for         of 260 candidate postconditions. One such candidate, shown in
any execution of getFront, if the queue is not empty, the front        Figure 1(b), asserts a relationship between internal fields: if the
queue is empty (currentSize == front), then front < 1.              using large language models (LLMs) to improve dynamic
Although this candidate postcondition may not be considered         specification inference. Our example demonstrates that LLMs
a direct characterization of the method’s intended behavior, it     can effectively identify and invalidate such flawed specifi-
definitely provides relevant information regarding the internal     cations. In the next section, we present an empirical study
implementation of the data structure, observable at the exit        to systematically evaluate the effectiveness of LLMs in this
point of the method under analysis.                                 concrete role.
   While the inferred postcondition is indeed informative, it
is not a valid postcondition assertion for getFront, despite                         IV. R ESEARCH Q UESTIONS
being valid for all program executions corresponding to the            Our evaluation assesses the effectiveness of LLMs in im-
test suite employed for dynamic analysis. Since this is not         proving dynamic specification inference. We begin by inves-
self-evident, let us analyze the implementation of the dequeue      tigating whether LLM-generated tests enhance the quality of
method, a method that updates the front index, and therefore        inferred specifications, posing the following research question:
indirectly affects the possible states after executing getFront.
                                                                    RQ1 Does LLM-based counterexample generation improve
As this is a circular array-based implementation of a queue,
                                                                          dynamic specification inference?
the dequeue operation does not reset the front index to 0,
but rather increments it circularly:                                To answer this question, we first prompt the LLM to judge
                                                                    the validity of a given postcondition for a target method; if
public Object dequeue() {
  if(isEmpty()) return null;
                                                                    deemed invalid, we ask the LLM to generate a test case as a
  currentSize--;                                                    counterexample. This counterexample is then integrated into
  Object frontItem = theArray[front];                               the dynamic specification inference process to measure its
  theArray[front] = null;
  if (++front == theArray.length)
                                                                    impact on the accuracy relative to the benchmark’s ground-
    front = 0;                                                      truth specifications.
  return frontItem;                                                    Since LLMs can make mistakes or produce tests irrespective
}
                                                                    of their relevance, accuracy improvement may be coincidental.
This circular increment has a direct implication: each dequeue      Therefore, we shift our focus to directly evaluating the quality
operation advances front by one (modulo capacity). Consider         of the LLMs’ outputs. Specifically, we assess their ability to (i)
the following execution trace, starting from an initial empty       correctly identify spurious assertions from dynamic inference
state where currentSize = 0 and front = 0:                          output, and (ii) generate valid counterexamples that invalidate
                                                                    them. This leads to the following questions:
  1) Enqueue an item: currentSize becomes 1; front re-
      mains 0.                                                      RQ2 How effective are LLMs in identifying spurious asser-
  2) Dequeue the item: currentSize returns to 0; front is                 tions inferred by dynamic analysis?
      incremented to 1.                                             RQ3 How effective are LLMs in generating counterexamples
                                                                          that invalidate the identified spurious assertions?
The queue is now logically empty (currentSize = 0), but
front = 1. Now, perform another enqueue:                            To address RQ2, we investigate the LLMs’ ability to ac-
                                                                    curately identify spurious assertions that are invalid for the
  3) Enqueue a second item: currentSize becomes 1; front
                                                                    corresponding target method. For precise verification, we use
      remains 1.
                                                                    constraint solving to determine the correctness of each inferred
In this final state, we have currentSize == front == 1.             postcondition relative to the ground truth. For RQ3, we focus
This invalidates the candidate postcondition, which states that     on the LLMs’ capacity to generate valid counterexamples that
when currentSize == front, front must be less than 1,               demonstrate assertion invalidity. Here, we verify whether the
providing a concrete counterexample.                                generated counterexamples successfully lead to the removal of
   Figure 1(c) presents a test case generated by a large lan-       the spurious assertions during the dynamic filtering stage.
guage model (LLM) that encodes precisely the sequence of
operations described in the previous analysis. Consequently,                     V. E MPIRICAL S TUDY W ORKFLOW
this test case acts as a verifiable counterexample, demonstrat-
ing the invalidity of the spurious postcondition. The generation    A. Overview
process involved providing GPT-5.1 with three key inputs: the          We now provide a detailed overview of our empirical study
complete source code of the QueueAr class, the specific imple-      workflow. As illustrated in Figure 2, our process evaluates
mentation of the getFront method, and the target candidate          the LLMs’ potential to enhance specification inference. The
postcondition. We then prompted the model to first evaluate the     workflow begins with a target Java class, aiming to infer its
logical validity of the postcondition and, upon determining it to   method postconditions as executable contract assertions. For
be false, to synthesize an executable JUnit test case that serves   initial inference, we employ SpecFuzzer [27], a state-of-the-art
as a concrete counterexample. The specific prompt structure         dynamic specification inference tool.
and reasoning guidelines are detailed in Section V-C.                  Our process continues with a target method and the set of
   The difficulty of automatically detecting spurious assertions    likely postconditions dynamically inferred by SpecFuzzer. For
and generating counterexamples highlights the potential of          each candidate postcondition, we query an LLM to perform a
                                       Fig. 2: Overview of our empirical study workflow.


validity analysis. Specifically, we construct a prompt contain-        You are an expert in program verification and testing. You are given a Java
                                                                       method and a postcondition assertion for that method. Based on the method
ing the source code of the enclosing class, the implementation         behavior, you will need to confirm that the method meets the postcondition. If
of the target method, and the postcondition under scrutiny. The        indeed the method meets the postcondition, you MUST output ”OK”. If, on the
                                                                       other hand, you determine that the method does NOT meet the postcondition,
LLM is instructed to first reason about the postcondition’s cor-       you MUST output a counterexample, in the form of a jUnit test case. The
rectness. If it judges the postcondition to be invalid, the model      counterexample test case MUST demonstrate the violation of the postcondition,
                                                                       using input values for the method that, after the execution of the method, make
must then generate a concrete, executable counterexample in            the postcondition invalid. You may provide the reasoning behind your output.
the form of a JUnit test case that demonstrates the violation.         ⃝ 1
                                                                       You will receive the input in the following way:
If the postcondition is deemed valid, the process proceeds             - The source code of the class comes first, after a line containing the text
without test generation. All LLM-generated counterexample              [[CODE]]
                                                                       - The method under test, that the postcondition refers to, comes after the code,
tests are subsequently aggregated and added to the original            preceded by text [[METHOD]]
test suite. SpecFuzzer is then re-executed using this augmented        - The postcondition follows after the method, and is preceded by text [[POST-
                                                                       CONDITION]] (note: postconditions may include quantifiers like size(X) –
suite to produce a refined—and ideally more accurate and re-           returns the size of the collection X; pairwiseEqual(seq1, seq2) - True iff seq1
duced—set of inferred postconditions. The subsequent sections          and seq2 have the same length, and every seq1[i] == seq2[i]; isReverse(seq1,
                                                                       seq2) - True iff seq1 is the reverse of seq2, typeArray(X) – returns the type of
detail the implementation and rationale for each of these steps.       the array X; getElement(X, i) – returns the i-th element of the array X; old(X)
                                                                       – returns the value of X before executing the method under test;             ⃝2
B. Dynamic Specification Inference                                     The output must be produced as follows:
                                                                       - After text [[VERDICT]], you will output “OK” if no counterexample for the
   We use SpecFuzzer [27] to infer postconditions for target           method and postcondition exist, and “FAILED” otherwise.
Java methods. The tool operates in two phases. First, it               - If verdict was “[[FAILED]]”, output the counterexample after the verdict,
                                                                       preceded by text “[[TEST]]”, in JUnit format.                                ⃝3
employs grammar-based fuzzing to generate candidate post-              Here are some examples of inputs and corresponding outputs:
conditions and validates them against an existing test suite.          [[CODE]]:
                                                                           {sample class 1}
Second, it performs a mutation-based filtering step to refine          [[METHOD]]:
the candidates. During this latter phase, postconditions are               {sample method 1}
                                                                       [[POSTCONDITION]]:
grouped into clusters based on the mutants they kill. Finally,             {sample postcondition 1}
only a single representative postcondition is selected from each       [[VERDICT]]:
                                                                           {sample verdict 1}
cluster, to form the final reported specification.                     [[TEST]]:
                                                                           {sample test 1}
C. LLM-based Counterexample Generation                                 ...                                                                          ⃝4
                                                                       [[CODE]]:
   To identify spurious inferred assertions and generate coun-             {target class}
                                                                       [[METHOD]]:
terexamples that discard them, we employ state-of-the-art                  {target method}
LLMs, with strong capabilities in code understanding and               [[POSTCONDITION]]:
                                                                           {target postcondition}                                                   ⃝5
generation. To interact with the LLMs, we use a carefully
designed prompt template, shown in Figure 3. The prompt             Fig. 3: Prompt template used for the LLM-based counterex-
aims at guiding the LLM towards determining the validity of         ample generation.
a given postcondition for a given method, and to generate
a counterexample test case evidencing the violation of the
postcondition, if applicable. The prompt is composed of a           and postcondition will be provided, while part ⃝3 outlines how

system prompt and a user prompt. The texts labeled with ⃝,    1     the LLM should structure its output, indicating that a test case
⃝,
 2  ⃝,
     3    and ⃝4 form the system prompt. Part ⃝  1 sets the role    should be provided only if the postcondition is violated, in the
of the LLM as an expert in program verification and testing,        JUnit format.
and describes the overall task of determining the validity of          Part ⃝4  provides examples of inputs and corresponding
a postcondition and generating counterexamples, if needed.          outputs, to illustrate the expected behavior of the LLM. For
Parts ⃝ 2   and ⃝3  provide detailed instructions on the input      space reasons, we do not show here the complete examples,
format and the expected output format, respectively. Part ⃝     2   although they are available in our replication package [5].
specifies the order in which the class code, method under test,        Finally, part ⃝5  forms the user prompt, consisting of the
actual class code, method under test, and postcondition to be      and SpecFuzzer+GPT using standard performance metrics:
analyzed by the LLM.                                               precision, recall, and F1-score. These metrics are computed
                                                                   by comparing the inferred assertions against the ground truth
D. Counterexample Validation                                       specifications. While in previous studies these metrics were
   The last step in our workflow validates the test cases          partially computed manually [27], in our study we fully
generated by the LLM. Essentially, each generated test case        automate this process by formally specifying the ground truth
is validated simply by compiling it. If the LLM-generated test     assertions. For subjects with numeric or boolean assertions, we
does not compile, we instruct the LLM to fix it, with up to        use the Z3 SMT solver [11], available in [6]. For more com-
three attempts. If after three attempts the test case still does   plex cases involving data structure implementations, we use
not compile, we discard it. At this point, we do not execute       the Alloy Analyzer [1], the automated specification analysis
the generated test cases, as they will be executed at a later      tool for the Alloy specification language [20].
stage by SpecFuzzer.                                                  Given a set G of ground truth postcondition assertions for
   Once we have validated the generated test cases, we in-         a subject method, we compute the precision of a set A of
corporate all compiling test cases into the test suite used by     inferred assertions as follows:
SpecFuzzer. Then, we execute SpecFuzzer again to obtain a
new set of postconditions. In this paper, we only perform                                        |{a ∈ A : G |= a}|
                                                                                   Precision =
one SpecFuzzer re-execution, after counterexample tests have                                              |A|
been added, we do not iterate the process. Multiple inference      That is, precision is the ratio of inferred assertions that are
iterations until convergence is a research direction we plan to    implied by the ground truth. To compute recall, we discard
explore in future work.                                            the set of invalid assertions I ⊆ A, the assertions in A that
                                                                   are not implied by the ground truth G, and compute recall as
                   VI. E MPIRICAL S ETUP                           follows:
A. Subjects                                                                                 |{g ∈ G : (A \ I) |= g}|
                                                                                  Recall =
                                                                                                        |G|
   We consider a set of 43 Java methods that were part of
the evaluation of SpecFuzzer [27], and have also been used         Thus, recall is the ratio of ground truth assertions that are
in several related works on specification inference [13], [15],    implied by the valid inferred assertions (i.e., those in A \ I).
[29], [33]. This set includes methods from array-based imple-      Finally, F1-score is computed as the harmonic mean of preci-
mentations of stack and queue data structures, methods from        sion and recall.
popular Java libraries like Apache Commons Math, Apache               In RQ2 and RQ3, we evaluate the quality and consistency
Commons Lang, and Google Guava, and JTS Topology Suite,            of the LLM’s outputs (see Figure 3 for further details on
and methods from classes using or implementing data struc-         the labels below). For RQ2, we measure the accuracy of the
tures including linked lists, n-ary trees, and heaps. We select    [[VERDICT]] provided by the LLM. Using the correct asser-
these subjects because the ground truth of postconditions for      tions identified in RQ1 as ground truth, we report precision
these methods is already available, which we use as a basis        and recall. We consider a true positive an assertion where the
to assess the correctness of the inferred postconditions. We       [[VERDICT]] was FAILED and the dynamic analysis correctly
implemented ground truth checkers for these cases using SAT        discarded it; otherwise, it is a false positive. A true negative is
and SMT Solving. The ground truths we use are publicly             an assertion where the [[VERDICT]] was OK and the dynamic
available in our replication package [5].                          analysis retained it; otherwise, it is a false negative.
                                                                      In RQ3, we go one step further: for each case where
B. Large Language Models (LLMs)                                    the LLM’s [[VERDICT]] was FAILED and it generated a
   Our empirical evaluation considers three state-of-the-art       [[TEST]], we measure whether that counterexample indeed
LLMs from different families: GPT-5.1 [3] from Open AI,            discards the judged invalid assertion. This allows us to assess
Llama 3.3 70B [4] from Meta, and DeepSeek-R1 [2]. These            the reasoning abilities of the LLMs and to determine whether
LLMs have shown great reasoning skills, adaptability to var-       some incorrect assertions were discarded collaterally by other
ious tasks (Mixture-of-Experts) and good computational effi-       tests rather than by the generated counterexamples.
ciency, making them promising candidates for our purposes.         D. Implementation
C. Evaluation Metrics                                                 To run our experiments, we implemented the workflow in
                                                                   Figure 2 as a Python prototype on top of SpecFuzzer [27],
   In RQ1, we investigate whether augmenting dynamic spec-         adding an LLM-based counterexample generation stage af-
ification inference with LLM-generated counterexamples im-         ter Specfuzzer’s standard generate-filter-reduce pipeline. All
proves the overall quality of the inferred specifications. To      scripts and data are in our replication package [5].
this end, we infer postcondition assertions for each method
in our subject set using both the original SpecFuzzer tool                          VII. E XPERIMENTAL R ESULTS
and our extended SpecFuzzer implementation that incorpo-              In this section we present the results obtained when running
rates LLM-based counterexample generation, referred to as          the GPT-5.1 LLM, and later in Section VIII-A we discuss the
SpecFuzzer+GPT. We compare the performance of SpecFuzzer           results with Llama 3.3 70B and DeepSeek-R1.
A. RQ1: Specification Inference Improvement                         public int abs(final int x) {
                                                                      final int i = x >>> 31;
   Table I summarizes the accuracy of the inferred post-              int result = (xˆ(∼i + 1)) + i;
conditions, with respect to the ground-truth, when the LLM-           assert (result >= 0); // Inferred postcondition
                                                                      return result;
generated test cases (counterexamples) are used or not in           }
the dynamic specification inference process. For SpecFuzzer
and SpecFuzzer+GPT, we report the number of ground truth            (a) SimpleMethods.abs method and a postcondition inferred by
postconditions (#GT) for each method, the number of tests           SpecFuzzer.
used by each approach, and the performance in terms of              @Test
precision, recall, and F1-score.                                    public void testAbs_NegativeReturn() throws Throwable {
                                                                      examples.SimpleMethods sm = new examples.SimpleMethods();
   Precision: Notably, when incorporating the LLM-generated           int x = Integer.MIN_VALUE; // -2147483648
counterexamples, we observe a significant improvement in              int result = sm.abs(x);
                                                                    }
precision across most subjects, increasing from an aver-
age of 67.83% with SpecFuzzer to 74.17% with Spec-                  (b) Counterexample test case generated by GPT-5.1, invalidating the
Fuzzer+GPT. More precisely, we observe that the increase in         inferred postcondition.
precision can be up to 54.52% for certain methods, such as
Polyupdate sm, with an average increase of ∼7% across all           Fig. 4: A target method with a postcondition inferred by
methods. In total, the LLM-generated counterexamples allow          SpecFuzzer and a counterexample generated by GPT-5.1.
to increase precision for 48.84% of the methods (21 out of 43
methods), while remaining the same for the rest.
                                                                    dynamic analysis tools like SpecFuzzer.
   This increase in precision comes from the quality of the
                                                                       Recall: Given our designed workflow, in every method we
counterexamples generated by the LLM, which effectively in-
                                                                    analyze, the recall will necessarily remain the same when
validate spurious postcondition assertions that would otherwise
                                                                    using SpecFuzzer alone, compared to using SpecFuzzer+GPT.
be retained by SpecFuzzer. These are test cases that, when
                                                                    This is due to the fact that SpecFuzzer+GPT can only con-
incorporated into the test suite and executed, lead SpecFuzzer’s
                                                                    tribute additional test cases. Thus, this can only make the
dynamic analysis to discard a greater number of invalid
                                                                    dynamic analysis stronger, discarding candidate assertions that
assertions. In Table II, we show, for each subject method, the
                                                                    were wrongly accepted by a less thorough initial test suite.
number of new test cases generated by GPT-5.1, the number
                                                                    This behavior is expected, as we do not rely on the LLM
of inferred assertions before and after incorporating the LLM-
                                                                    to decide whether an assertion has been invalidated, but on
generated tests, and the percentage of discarded assertions.
                                                                    SpecFuzzer’s dynamic analysis stage, which runs each test to
   Notably, the 1,009 new counterexample test cases generated       check assertion validity.
by GPT-5.1 allow us to invalidate and eliminate a total of             Notice also that SpecFuzzer+GPT’s recall is limited by
1,877 invalid postcondition assertions inferred by SpecFuzzer.      SpecFuzzer’s specification language and inference capabilities.
This represents a total reduction of 10.09% of the inferred         Thus, any valid assertion that is not produced by SpecFuzzer,
assertions, which directly contributes to the observed increase     will not be captured by SpecFuzzer+GPT either. Extending
in precision. On average, GPT generated 53 new test cases           SpecFuzzer’s recall capabilities would require proposing new
per method, and discarded 13% of the inferred assertions.           candidate assertions, which is not supported by our designed
Some subjects experienced a significant reduction, such as          workflow.
eiffel.RingBuffer and cozy.Polyupdate, where 44.06%                    Finally, considering both precision and recall, we observe
and 64.42% of the assertions were discarded, respectively.          an overall improvement in F1-score, as it positively affected
   As an example of the counterexamples that LLMs can               by the increase in precision.
generate, consider the method SimpleMethods.abs, which
computes the absolute value of an integer. Figure 4(a) shows          RQ1 Answer. Incorporating LLM-generated counterex-
the method code along with a postcondition inferred by Spec-          amples significantly improves the precision of the inferred
Fuzzer, stating that the return value result is always non-           postconditions by effectively invalidating spurious asser-
negative. While this postcondition seems correct at first glance,     tions. The recall remains unchanged, confirming that no
and holds for most integer inputs, it fails for the specific          valid postconditions are discarded. The overall F1-score
input Integer.MIN VALUE (-2147483648) due to integer                  improves as a direct result of the increased precision.
overflow: in this case, this method’s implementation returns
Integer.MIN VALUE. Figure 4(b) shows a counterexample               B. RQ2: Invalid Postcondition Identification Effectiveness
test case generated by GPT-5.1 that demonstrates this viola-           Table III summarizes GPT-5.1’s performance in identifying
tion. When this test case is executed, it produces a negative       invalid postconditions. We observe that GPT-5.1 correctly
result value, thereby invalidating the inferred postcondition.      judged as invalid 90% of the invalid postconditions (recall),
This example illustrates how LLMs can effectively reason            although only 55% of those judged invalid were indeed invalid
about subtle edge cases in program behavior, and generate           (precision). Improving precision is a challenge to address in
test cases that expose flaws in the specifications inferred by      future LLM-based counterexample generation approaches.
TABLE I: Specification inference performance of SpecFuzzer and SpecFuzzer+GPT, our SpecFuzzer extension augmented with
LLM-based counterexample generation using the GPT-5.1 model.

                                                        #Tests                   Precision(%)                     Recall(%)                    F1-Score
     Subject                         #GT
                                           SpecFuzzer SpecFuzzer+GPT      SpecFuzzer SpecFuzzer+GPT      SpecFuzzer SpecFuzzer+GPT     SpecFuzzer SpecFuzzer+GPT

     SimpleMethods addElementToSet     1         313               315        100.00            100.00       100.00           100.00        100.0          100.0
     SimpleMethods abs                 3         281               351         74.70             96.88         0.00             0.00          0.0            0.0
     SimpleMethods getMin              3         277               277        100.00            100.00        66.67            66.67         80.0           80.0
     SimpleMethods incrementAt         2         343               344         96.49             96.49         0.00             0.00          0.0            0.0
     StackAr makeEmpty                 3         241               251         57.81             58.62       100.00           100.00        73.26          73.91
     StackAr topAndPop                 5         264               289         69.86             72.30        40.00            40.00        50.87          51.51
     StackAr pop                       4         259               266         70.89             71.63        50.00            50.00        58.64          58.89
     StackAr push                      4         264               280         89.19             89.19        50.00            50.00        64.07          64.07
     StackAr top                       4         259               261         79.66             79.66        50.00            50.00        61.44          61.44
     QueueAr enqueue                   5         241               294         80.97             83.30        80.00            80.00        80.48          81.62
     QueueAr getFront                  5         241               249         76.47             74.59        80.00            80.00         78.2           77.2
     QueueAr dequeue                   5         241               260         65.93             65.93        20.00            20.00        30.69          30.69
     QueueAr dequeueAll                5         241               260         80.05             79.95        80.00            80.00        80.02          79.97
     QueueAr makeEmpty                 5         264               328         85.01             86.15        60.00            60.00        70.35          70.74
     ArithmeticUtils subAndCheck       1         271               275        100.00            100.00       100.00           100.00        100.0          100.0
     FastMathNew floor                 1         286               348         40.54             93.75         0.00             0.00          0.0            0.0
     MathUtilsNew copySignInt          4         499               501        100.00            100.00         0.00             0.00          0.0            0.0
     BooleanUtils toBoolean            1         499               501        100.00            100.00       100.00           100.00        100.0          100.0
     BooleanUtils compare              3         273               291         82.35             82.35       100.00           100.00        90.32          90.32
     IntMath mod                       1         328               360          1.64              1.67         0.00             0.00          0.0            0.0
.    Angle getTurn                     4         499               501        100.00            100.00        25.00            25.00         40.0           40.0
     MathUtil clamp                    3         499               523        100.00            100.00        33.33            33.33         50.0           50.0
     Envelope maxExtent                4         273               275          9.02             13.30         0.00             0.00          0.0            0.0
     Composite addChild                5         299               312         21.39             22.10         0.00             0.00          0.0            0.0
     DLLN remove                       1         316               318        100.00            100.00       100.00           100.00        100.0          100.0
     DLLN insertRight                  4         316               322         83.87             82.35        25.00            25.00        38.52          38.36
     Map count                         4         307               309         85.19             85.19       100.00           100.00         92.0           92.0
     Map remove                        5         307               309         61.70             63.04        20.00            20.00        30.21          30.37
     Map extend                        4         307               329         63.79             67.27        25.00            25.00        35.92          36.45
     RingBuffer extend                 4         287               326         38.00             71.51        25.00            25.00        30.16          37.05
     RingBuffer item                   3         287               293         44.94             65.87        66.67            66.67        53.69          66.26
     RingBuffer remove                 3         287               311         39.22             59.45       100.00           100.00        56.34          74.57
     RingBuffer count                  3         287               375         58.28             91.40         0.00             0.00          0.0            0.0
     RingBuffer wipeOut                3         287               302         53.25             63.58       100.00           100.00         69.5          77.74
     Polyupdate a1                     2         271               489          1.52              4.46        50.00            50.00         2.95            8.2
     Polyupdate sm                     1         271               315         21.09             75.61       100.00           100.00        34.83          86.11
     Structure foo                     1         265               265         50.00             50.00       100.00           100.00        66.67          66.67
     Structure setX                    1         265               289         80.39             85.82       100.00           100.00        89.13          92.37
     ListComp02 insert r               3         259               261         94.12             96.77       100.00           100.00        96.97          98.36
     ListComp02 insert s               3         259               259         93.75             93.75       100.00           100.00        96.77          96.77
     MaxBag remove                     4         256               258         41.67             41.67         0.00             0.00          0.0            0.0
     MaxBag getMax                     3         256               282        100.00            100.00        66.67            66.67         80.0           80.0
     MaxBag add                        3         256               260         23.81             23.81        33.33            33.33        27.78          27.78

     AVG                                       297.70            320.56        67.83             74.17        54.57            54.57        51.39          53.94




    RQ2 Answer. GPT-5.1 demonstrates a very high capabil-                          the counterexamples managed to invalidate at least one of
    ity to correctly identify invalid postconditions, achieving                    the targeted candidate postconditions, discarding on average
    high precision and recall in its judgments. When it labels                     47.76% of the assertions judged invalid.
    a postcondition as invalid, the prediction is highly reliable.                    It is worth remarking that some of the counterexamples
                                                                                   produced by GPT-5.1 were very useful for identifying weak-
C. RQ3: Counter-example Generation Effectiveness                                   nesses in our ground-truth, and consequently improving it. For
   RQ3 concerns the effectiveness of GPT-5.1 in generating                         instance, the counterexample shown in Figure 4 for method
counter-examples for assertions judged as invalid. We observe                      abs, was initially considered a false positive, since we believed
that the LLM judged at least one candidate postcondition as                        that the assertion result >= 0 was correct. However, GPT-
invalid in 40 out of the 43 analyzed subjects. For each of                         5.1 realized that for that specific implementation, the assertion
the 40 subjects, GPT-5.1 successfully generated at least one                       does not hold for Integer.MIN VALUE (actually, it is the
compilable counterexample, where on average, 87.2% of the                          only value for which it does not hold). In this case, the ground-
generated tests compiled correctly. In 27 out of the 40 cases,                     truth was revised to match this behavior.
TABLE II: Counterexample test cases generated by GPT-5.1                                        VIII. D ISCUSSION
and their impact on the invariants inferred by SpecFuzzer in
terms of discarded assertions.                                             A. Generalization to other LLMs
                                                                              To assess whether our findings generalize beyond the pri-
     Subject             #M
                              SpecFuzzer    SpecFuzzer+GPT (one iter.)     mary model under evaluation, we replicated our experiments
                                #Invs      #New Tests   #Invs Red. ⇓
                                                                           using two additional LLMs: Llama 3.3 70B and DeepSeek-R1.
     SimpleMethods        4          213           79     190      10.8%   Notice that the same requests were made for each model to
     StackAr              5         1702           87    1675      1.59%
     QueueAr              5         4221          156    4062      3.77%   mitigate any coincidental result. These models were selected
     ArithmeticUtils      1            4            4       4         0%   because they belong to different model families, are open-
     FastMath             1           50           62      18        64%
     MathUtils            1           18            2      17      5.56%   weights, and are representative of models with state-of-the-art
     BooleanUtils         2           60           20      59      1.67%   capabilities in problem solving and large-scale code genera-
     IntMath              1          323           32     318      1.55%
     Angle                1            4            2       3        25%   tion.
     MathUtil             1           19           24      18      5.26%      Table IV summarizes the number of LLM-generated coun-
     Envelope             1          694            2     646      6.92%
     Composite            1         7623           13    7378      3.21%   terexamples, the number of invalid postconditions that were
     DLLN                 2          162            8     160      1.23%   discarded (and the corresponding percentages), as well as the
     Map                  3          141           26     137      2.84%
     RingBuffer           5         2281          172    1276     44.06%   precision, recall and F1-score obtained after adding the cor-
     Polyupdate           2          430          262     153     64.42%   responding tests to the suites used by SpecFuzzer’s dynamic
     Structure            2          156           24     145      7.05%
     ListComp02           2           68            2      65      4.41%   analysis. First, we observe that Llama 3.3 70B generated 430
     MaxBag               3          436           32     404      7.34%   compilable counterexamples for the subjects, while GPT-5.1
     TOTAL               43       18,605        1,009   16,728    10.09%
                                                                           generated 982 compilable tests (128% more). Llama’s coun-
                                                                           terexamples discarded a total of 1,048 invalid postconditions,
                                                                           a 5.63% reduction of the inferred specifications, in contrast
                                                                           to the 1,877 discarded by GPT-5.1 (79% more than Llama).
TABLE III: GPT-5.1 accuracy in identifying invalid postcon-                Llama allowed us to obtain a precision of 71.13%, a recall of
ditions.                                                                   51.47%, and an F1-score of 50.31%, lower than the metrics
                                                                           obtained with GPT-5.1. These observations, given that the
               Subject                     Precision     Recall            same number and same requests were made with these models,
               Angle getTurn                    100         100            suggest that GPT-5.1 is more cost-effective than Llama 3.3
               BooleanUtils toBoolean          100          100            70B, to generate counterexamples for invalid postconditions.
               Composite addChild             27.27         100
               Envelope maxExtent               100         100               Second, in the case of the DeepSeek-R1 model, it generated
               FastMathNew floor                 64         100            3,684 compilable counterexamples (275% more than GPT-5.1)
               IntMath mod                     8.33       33.33
               ListComp02 insert r             100          100            that discarded a total of 2,173 invalid postconditions (almost
               Map extend                     27.27         100            16% more than GPT-5.1). DeepSeek-R1 was more effective
               MathUtil clamp                  12.5         100
               MaxBag getMax                  81.25       92.86            than GPT-5.1 in generating compilable counterexamples, but
               Polyupdate a1                  85.39          95            it obtains a precision of 75.62%, a recall of 51.47%, and an
               Polyupdate sm                   91.3        91.3
               QueueAr dequeueAll                25         100            F1-score of 52.04%, a slightly lower performance than that
               QueueAr enqueue                62.16       85.19            obtained by GPT-5.1, suggesting that GPT-5.1 was the most
               QueueAr getFront                  80         100
               QueueAr makeEmpty              33.33       66.67            cost-effective LLM for the task under study.
               RingBuffer count               94.92       96.55               Our results show that open-weights LLMs obtain a per-
               RingBuffer extend              75.76         100
               RingBuffer item                   50       57.14            formance comparable to the commercial one, being effective
               RingBuffer remove              22.22         100            at identifying incorrect postconditions and generating valid
               RingBuffer wipeOut             55.56        62.5
               SimpleMethods abs              33.33        100             counterexamples.
               StackAr makeEmpty                 20          50
               StackAr pop                    33.33         100            B. Towards ‘static’ LLM-based specification inference
               StackAr push                      25         100
               StackAr topAndPop              57.14         100               Our experiments provided concrete evidence that modern
               Structure setX                 23.08         100
                                                                           LLMs have strong reasoning skills that allow them to statically
               AVG                            55.12       90.02
                                                                           determine whether a given postcondition is valid or not, for a
                                                                           given method under analysis. Then, it is rather straightforward
                                                                           to devise a (static) mechanism to determine the validity or
                                                                           invalidity of a candidate postcondition, by directly using the
                                                                           LLM [[VERDICT]] response. This may be considered an
  RQ3 Answer. GPT-5.1 successfully generates compilable                    instance of the LLM-as-a-Judge strategy [39].
  counterexample test cases for a large majority of the sub-                  To further explore this possibility, we replicated the ex-
  jects. These counterexamples are effective at invalidating               periments with GPT-5.1, but restricted the number of tests
  targeted, spurious postcondition assertions. In some cases,              generated by SpecFuzzer during the dynamic analysis to just
  inaccuracies in the ground-truth are revealed.                           50 tests, approximately 15% of the number of tests used in
                                        TABLE IV: Comparison between different LLMs

   Model                #Tests      #Removed Assertions              Red. (% ⇓)       Precision(%)       Recall(%)       F1-score
   GPT-5.1                 982                         1,877             10.09%             74.17%           54.57%        53.94%
   Llama 3.3 70B           430                         1,048              5.63%             71.13%           54.57%        50.31%
   Deepseek-R1           3,684                         2,173             11.68%             75.62%           54.57%        52.04%


RQ1 (see Table II). This reduces SpecFuzzer’s capabilities            inference process. We specifically instructed three state-of-the-
to discard invalid postconditions, so the LLM has more                art LLMs, namely GPT-5.1, Llama 3.3 70B, and DeepSeek-
invalid assertions to evaluate and discard. Our experiments           R1, to determine whether a candidate assertion is a valid
show that, after analyzing 15,491 assertions, GPT-5.1 managed         postcondition for the method under test, and to generate a
to eliminate 5,140 invalid postconditions. Overall, with this         counterexample in the form of a JUnit test if it is judged in-
simple LLM-as-a-Judge approach [39], GPT-5.1 obtained a               valid. These counterexamples can then be used to augment the
precision of 64.21%, a recall of 83.08, and an F1-score of            test suites employed by SpecFuzzer during dynamic analysis,
72.44%. These results are very promising and consistent with          helping it to discard invalid postconditions.
our previous observations, encouraging researchers to explore            Our empirical evaluation on a diverse benchmark of Java
the direct use of LLMs for candidate specification assessment         methods showed that incorporating LLM-generated counterex-
in future specification inference tools.                              amples leads to a substantial improvement in specification
                                                                      quality. In particular, GPT-5.1 led to an average increase of
                 IX. T HREATS TO VALIDITY
                                                                      approximately 7 percentage points in precision, while recall
      a) External validity: A potential threat to the validity        remained effectively unchanged. This result indicates that
of this study concerns the specification inference tools and          GPT-5.1 can successfully eliminate invalid assertions without
LLMs used for the analysis. To mitigate this risk, we relied          discarding valid properties from the ground truth. Conse-
on SpecFuzzer, one of the state-of-the-art tools for dynamic          quently, the overall quality of inferred specifications improved,
specification inference, that has been more effective than            as reflected by higher F1-scores across most subjects. We
related tools like Daikon [13], GAssert [33] and EvoSpex [29].        also showed that this observation generalizes to other LLMs.
In addition, we evaluated multiple LLMs from different model          Llama 3.3 70B discarded 5.63% of the assertions deemed
families to ensure that our findings are consistent and gener-        invalid, as it generated fewer compilable counterexamples
alizable.                                                             than GPT-5.1. DeepSeek-R1 generated the highest number
      b) Internal validity: The performance of our empirical          of compilable counterexamples (275% more than GPT-5.1),
evaluation depends on the underlying tooling and LLMs.                discarding 11.68% of invalid assertions (a 16% improvement
Consequently, a potential threat to internal validity arises          over GPT-5.1), although at a higher computational cost.
from variations in model capability as well as from the                  We also observed that LLMs can effectively identify invalid
nondeterministic nature of LLM outputs. To mitigate these             postconditions, achieving 90% recall. However, precision re-
threats, we evaluated multiple models from different families,        mains at only 55%, meaning that nearly half of the assertions
reducing the risk that our findings are specific to a specific        flagged as invalid are actually valid. This leads to wasted
model. Additionally, to limit nondeterminism, we configured           resources, as the LLMs attempt to generate counterexamples
all models with a low temperature setting (0.1), aiming to            for correct postconditions. Thus, while LLMs show promise
make the generation process as deterministic as possible.             in detecting actual issues, further improvements are needed to
      c) Construct validity: A potential threat to validity is        reduce false positives and make the process more efficient.
data leakage, i.e., whether the LLMs have already seen our               Overall, this work demonstrates that LLM-based counterex-
evaluation set during training. However, the risk is low for          ample generation is a practical and effective mechanism for
two reasons. First, the candidate specifications are generated at     improving dynamic specification inference.
runtime by SpecFuzzer using fuzzing, so the specific assertions
                                                                                         ACKNOWLEDGMENTS
the LLMs must assess are unlikely to appear in any training
corpus. While ground truth assertions exist, we use constraint           We thank the anonymous reviewers for their valuable
solving to check semantic consistency since the syntactic             feedback. This work has been partially supported by Lux-
form may differ substantially from any seen example. Second,          embourg’s Ministry of Economy through RDI Law project
the LLMs are instructed to generate novel test cases that             “Innovations for 21st Century Assessment Authoring”, by the
invalidate candidate postconditions, requiring reasoning and          Luxembourg National Research Fund (FNR) PEARL program
creating tests likely not existing for the project under analysis.    (grant agreement 16544475), by Argentina’s ANPCyT through
                                                                      grant 2021-4862, by China’s State Administration of Foreign
                      X. C ONCLUSIONS                                 Experts Affairs through project “Trustworthy Evolution of
  In this paper, we empirically evaluated whether the test            LLM-generated Models”, and by EU’s Marie Sklodowska-
generation capabilities of LLMs can improve the specification         Curie grant No. 101008233 (MISSION).
                             R EFERENCES                                        [20] Daniel Jackson. Alloy: a language and tool for exploring software
                                                                                     designs. Commun. ACM, 62(9):66–76, 2019.
 [1] Alloy analyzer. https://alloytools.org/, 2026.                             [21] Gunel Jahangirova, David Clark, Mark Harman, and Paolo Tonella.
 [2] Deepseek-r1. https://github.com/deepseek-ai/DeepSeek-R1, 2026.                  Test oracle assessment and improvement. In Andreas Zeller and
 [3] Gpt-5.1. https://openai.com/index/gpt-5-1/, 2026.                               Abhik Roychoudhury, editors, Proceedings of the 25th International
 [4] Llama           3.3.                        https://www.llama.com/docs/         Symposium on Software Testing and Analysis, ISSTA 2016, Saarbrücken,
     model-cards-and-prompt-formats/llama3 3/, 2026.                                 Germany, July 18-20, 2016, pages 247–258. ACM, 2016.
 [5] Replication package of our study. https://zenodo.org/records/18899070,     [22] Michael Konstantinou, Renzo Degiovanni, and Mike Papadakis. Do llms
     2026.                                                                           generate test oracles that capture the actual or the expected program
 [6] Z3. https://github.com/Z3Prover/z3, 2026.                                       behaviour?, 2024.
 [7] Pablo Abad, Nazareno Aguirre, Valeria S. Bengolea, Daniel Alfredo          [23] Gary T. Leavens, Yoonsik Cheon, Curtis Clifton, Clyde Ruby, and
     Ciolek, Marcelo F. Frias, Juan P. Galeotti, Tom Maibaum, Mariano M.             David R. Cok. How the design of JML accommodates both runtime
     Moscato, Nicolás Rosner, and Ignacio Vissani. Improving test generation        assertion checking and formal verification. Sci. Comput. Program., 55(1-
     under rich contracts by tight bounds and incremental SAT solving. In            3):185–208, 2005.
     Sixth IEEE International Conference on Software Testing, Verification      [24] Lisa (Ling) Liu, Bertrand Meyer, and Bernd Schoeller. Using contracts
     and Validation, ICST 2013, Luxembourg, Luxembourg, March 18-22,                 and boolean queries to improve the quality of automatic test generation.
     2013, pages 21–30. IEEE Computer Society, 2013.                                 In Yuri Gurevich and Bertrand Meyer, editors, Tests and Proofs - 1st
 [8] Nadia Alshahwan, Jubin Chheda, Anastasia Finegenova, Mark Harman,               International Conference, TAP 2007, Zurich, Switzerland, February 12-
     Alexandru Marginean, Shubho Sengupta, and Eddy Wang. Automated                  13, 2007. Revised Papers, volume 4454 of Lecture Notes in Computer
     unit test improvement using Large Language Models at Meta. In ACM               Science, pages 114–130. Springer, 2007.
     International Conference on the Foundations of Software Engineering        [25] Francesco Logozzo and Thomas Ball. Modular and verified automatic
     (FSE 2024), July 2024.                                                          program repair. In Gary T. Leavens and Matthew B. Dwyer, editors,
 [9] Yinghao Chen, Zehao Hu, Chen Zhi, Junxiao Han, Shuiguang Deng, and              Proceedings of the 27th Annual ACM SIGPLAN Conference on Object-
     Jianwei Yin. Chatunitest: A framework for llm-based test generation.            Oriented Programming, Systems, Languages, and Applications, OOP-
     In Companion Proceedings of the 32nd ACM International Conference               SLA 2012, part of SPLASH 2012, Tucson, AZ, USA, October 21-25,
     on the Foundations of Software Engineering, FSE 2024, page 572–576,             2012, pages 133–146. ACM, 2012.
     New York, NY, USA, 2024. Association for Computing Machinery.              [26] Facundo Molina, Nazareno Aguirre, and Alessandra Gorla. State field
[10] Marcelo d’Amorim, Carlos Pacheco, Tao Xie, Darko Marinov, and                   coverage: A metric for oracle quality. In 40th IEEE/ACM International
     Michael D. Ernst. An empirical comparison of automated generation               Conference on Automated Software Engineering, ASE 2025, Seoul,
     and classification techniques for object-oriented unit testing. In 21st         Korea, Republic of, November 16-20, 2025, pages 2707–2719. IEEE,
     IEEE/ACM International Conference on Automated Software Engineer-               2025.
     ing (ASE 2006), 18-22 September 2006, Tokyo, Japan, pages 59–68.
                                                                                [27] Facundo Molina, Marcelo d’Amorim, and Nazareno Aguirre. Fuzzing
     IEEE Computer Society, 2006.
                                                                                     class specifications. In 44th IEEE/ACM 44th International Conference
[11] Leonardo Mendonça de Moura and Nikolaj S. Bjørner. Z3: an efficient            on Software Engineering, ICSE 2022, Pittsburgh, PA, USA, May 25-27,
     SMT solver. In C. R. Ramakrishnan and Jakob Rehof, editors, Tools               2022, pages 1008–1020. ACM, 2022.
     and Algorithms for the Construction and Analysis of Systems, 14th
                                                                                [28] Facundo Molina, Alessandra Gorla, and Marcelo d’Amorim. Test oracle
     International Conference, TACAS 2008, Held as Part of the Joint
                                                                                     automation in the era of llms. ACM Trans. Softw. Eng. Methodol.,
     European Conferences on Theory and Practice of Software, ETAPS
                                                                                     34(5):150:1–150:24, 2025.
     2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings, volume
     4963 of Lecture Notes in Computer Science, pages 337–340. Springer,        [29] Facundo Molina, Pablo Ponzio, Nazareno Aguirre, and Marcelo F. Frias.
     2008.                                                                           Evospex: An evolutionary algorithm for learning postconditions. In 43rd
[12] Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, and Shuvendu K.            IEEE/ACM International Conference on Software Engineering, ICSE
     Lahiri. Can large language models transform natural language intent into        2021, Madrid, Spain, 22-30 May 2021, pages 1223–1235. IEEE, 2021.
     formal method postconditions? Proc. ACM Softw. Eng., 1(FSE):1889–          [30] Yu Pei, Carlo A. Furia, Martin Nordio, Yi Wei, Bertrand Meyer, and
     1912, 2024.                                                                     Andreas Zeller. Automated fixing of programs with contracts. IEEE
[13] Michael D. Ernst, Jeff H. Perkins, Philip J. Guo, Stephen McCamant,             Trans. Software Eng., 40(5):427–449, 2014.
     Carlos Pacheco, Matthew S. Tschantz, and Chen Xiao. The daikon sys-        [31] Gabriel Ryan, Siddhartha Jain, Mingyue Shang, Shiqi Wang, Xiaofei
     tem for dynamic detection of likely invariants. Sci. Comput. Program.,          Ma, Murali Krishna Ramanathan, and Baishakhi Ray. Code-aware
     69(1-3):35–45, 2007.                                                            prompting: A study of coverage-guided test generation in regression
[14] Christopher Foster, Abhishek Gulati, Mark Harman, Inna Harper,                  setting using llm. Proc. ACM Softw. Eng., 1(FSE), July 2024.
     Ke Mao, Jillian Ritchey, Hervé Robert, and Shubho Sengupta. Mutation-     [32] Seung Yeob Shin, Fabrizio Pastore, Domenico Bianculli, and Alexandra
     guided llm-based test generation at meta. In 2025 ACM Conference on             Baicoianu. Towards generating executable metamorphic relations using
     Foundations of Software Engineering (FSE 2025). ACM, 2025. Also                 large language models. In Antonia Bertolino, João Pascoal Faria, Patricia
     available as arXiv preprint arXiv:2501.12862.                                   Lago, and Laura Semini, editors, Quality of Information and Communi-
[15] Aayush Garg, Renzo Degiovanni, Facundo Molina, Maxime Cordy,                    cations Technology, pages 126–141. Springer Nature Switzerland, 2024.
     Nazareno Aguirre, Mike Papadakis, and Yves Le Traon. Enabling              [33] Valerio Terragni, Gunel Jahangirova, Paolo Tonella, and Mauro Pezzè.
     efficient assertion inference. In 34th IEEE International Symposium on          Evolutionary improvement of assertion oracles. In Proceedings of the
     Software Reliability Engineering, ISSRE 2023, Florence, Italy, October          28th ACM Joint Meeting on European Software Engineering Conference
     9-12, 2023, pages 623–634. IEEE, 2023.                                          and Symposium on the Foundations of Software Engineering, ESEC/FSE
[16] Carlo Ghezzi, Mehdi Jazayeri, and Dino Mandrioli. Fundamentals of               2020, page 1178–1189, New York, NY, USA, 2020. Association for
     Software Engineering. Prentice Hall PTR, Upper Saddle River, NJ, USA,           Computing Machinery.
     2nd edition, 2002.                                                         [34] Junjie Wang, Yuchao Huang, Chunyang Chen, Zhe Liu, Song Wang,
[17] Soneya Binta Hossain and Matthew Dwyer. Togll: Correct and strong               and Qing Wang. Software testing with large language models: Survey,
     test oracle generation with llms, 2024.                                         landscape, and vision. IEEE Trans. Softw. Eng., 50(4):911–936, February
[18] Xinyi Hou, Yanjie Zhao, Yue Liu, Zhou Yang, Kailong Wang, Li Li,                2024.
     Xiapu Luo, David Lo, John Grundy, and Haoyu Wang. Large language           [35] Zejun Wang, Kaibo Liu, Ge Li, and Zhi Jin. HITS: high-coverage
     models for software engineering: A systematic literature review. ACM            llm-based unit test generation via method slicing. In Vladimir Filkov,
     Trans. Softw. Eng. Methodol., September 2024. Just Accepted.                    Baishakhi Ray, and Minghui Zhou, editors, Proceedings of the 39th
[19] Chen Huo and James Clause. Improving oracle quality by detecting                IEEE/ACM International Conference on Automated Software Engineer-
     brittle assertions and unused inputs in tests. In Shing-Chi Cheung,             ing, ASE 2024, Sacramento, CA, USA, October 27 - November 1, 2024,
     Alessandro Orso, and Margaret-Anne D. Storey, editors, Proceedings              pages 1258–1268. ACM, 2024.
     of the 22nd ACM SIGSOFT International Symposium on Foundations             [36] Danning Xie, Byoungwoo Yoo, Nan Jiang, Mijung Kim, Lin Tan,
     of Software Engineering, (FSE-22), Hong Kong, China, November 16 -              Xiangyu Zhang, and Judy S. Lee. How effective are large language
     22, 2014, pages 621–631. ACM, 2014.                                             models in generating software specifications? In 2025 IEEE Interna-
     tional Conference on Software Analysis, Evolution and Reengineering
     (SANER), pages 1–12, 2025.
[37] Zhiqiang Yuan, Mingwei Liu, Shiji Ding, Kaixin Wang, Yixuan Chen,
     Xin Peng, and Yiling Lou. Evaluating and improving chatgpt for unit
     test generation. Proc. ACM Softw. Eng., 1(FSE), July 2024.
[38] Yifan Zhang, Dave Towey, and Matthew Pike. Automated metamorphic-
     relation generation with chatgpt: An experience report. In Hossain
     Shahriar, Yuuichi Teranishi, Alfredo Cuzzocrea, Moushumi Sharmin,
     Dave Towey, A. K. M. Jahangir Alam Majumder, Hiroki Kashiwazaki,
     Ji-Jiang Yang, Michiharu Takemoto, Nazmus Sakib, Ryohei Banno, and
     Sheikh Iqbal Ahamed, editors, 47th IEEE Annual Computers, Software,
     and Applications Conference, COMPSAC 2023, Torino, Italy, June 26-
     30, 2023, pages 1780–1785. IEEE, 2023.
[39] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhang-
     hao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P.
     Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica. Judging LLM-as-
     a-judge with MT-bench and Chatbot Arena. In Proceedings of the 37th
     International Conference on Neural Information Processing Systems,
     Red Hook, NY, USA, 2023. Curran Associates Inc.
