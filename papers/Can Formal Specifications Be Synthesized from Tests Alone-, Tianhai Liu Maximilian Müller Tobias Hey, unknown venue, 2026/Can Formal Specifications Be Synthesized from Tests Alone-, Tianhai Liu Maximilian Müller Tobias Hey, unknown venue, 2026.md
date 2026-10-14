                                              Can Formal Specifications Be Synthesized from Tests Alone?
                                                              Tianhai Liu                                         Maximilian Müller                                   Tobias Hey
                                                Karlsruhe Institute of Technology                       Karlsruhe Institute of Technology                 Karlsruhe Institute of Technology
                                                       Karlsruhe, Germany                                      Karlsruhe, Germany                                Karlsruhe, Germany
                                                       tianhai.liu@kit.edu                             maximilian.mueller7@student.kit.edu                          hey@kit.edu

                                                            Vitus Lüntzel                                       Muhammad Minhas                                     Anne Koziolek
                                                Karlsruhe Institute of Technology                        Karlsruhe Institute of Technology                Karlsruhe Institute of Technology
                                                       Karlsruhe, Germany                                       Karlsruhe, Germany                               Karlsruhe, Germany
                                                        luentzel@kit.edu                                         minhas@kit.edu                                   koziolek@kit.edu

                                                                                                                  Bernhard Beckert
                                                                                                         Karlsruhe Institute of Technology
                                                                                                                Karlsruhe, Germany
                                                                                                                 beckert@kit.edu
                                         Abstract                                                                                1   Introduction
arXiv:2608.13240v1 [cs.SE] 13 Aug 2026




                                         Formal specifications offer strong guarantees, but remain costly to                     Unit test suites are the backbone of industrial regression testing,
                                         write manually. Recent LLM-based approaches automate this by in-                        yet they inherently capture only concrete executions. As systems
                                         ferring specifications from source code, yet their reliance on white-                   evolve, this granularity gap allows silent semantic regressions to
                                         box access poses barriers to industrial adoption due to intellectual                    remain undetected. While formal specifications (e.g., pre- and post-
                                         property risks and deployment costs. Our approach uses LLMs to                          conditions) could bridge this gap by enabling broader behavioral
                                         infer candidate specifications solely from test code and dynamic                        reasoning, they are rarely available in practice due to the manual
                                         execution traces: the LLM observes only the program interface, se-                      effort and expert knowledge required to construct them.
                                         lected inputs, and corresponding outputs or state changes, while the                       Recent efforts to automate specification synthesis have predom-
                                         implementation internals remain hidden. Candidate specifications                        inantly leveraged Large Language Models (LLMs) in a white-box
                                         are validated locally using bounded model checking, with feedback                       setting, inferring properties directly from source code [4, 6, 9, 14, 22,
                                         guiding iterative refinement. Initial results on the SpecGenBench                       29, 30]. While effective, this approach may face practical barriers
                                         benchmark suggest that tests can guide LLMs towards meaning-                            in industrial contexts. Our motivation stems from observations of
                                         ful Java Modeling Language specifications, while also highlighting                      long-lived industrial systems, such as those maintained by small
                                         checker compatibility and diagnostic feedback as key challenges                         and medium-sized enterprises (SMEs), where proprietary technol-
                                         for reliable refinement.                                                                ogy is central to their market differentiation. For such systems,
                                                                                                                                 maintaining test cases as the software evolves is increasingly chal-
                                         CCS Concepts                                                                            lenging, and formal specifications could provide a more durable
                                                                                                                                 basis for capturing and checking behavioral expectations. How-
                                         • Software and its engineering → Formal software verifica-
                                                                                                                                 ever, adopting white-box LLM inference must be balanced against
                                         tion; Software testing and debugging.
                                                                                                                                 the need to protect confidential implementation knowledge and
                                                                                                                                 preserve long-term competitiveness. Moreover, source code may
                                         Keywords                                                                                be unavailable to the specification-inference process altogether:
                                         Test-Derived Formal Specifications, LLM, BMC                                            security policies may restrict source code access to isolated envi-
                                                                                                                                 ronments, third-party components or remote services may expose
                                         ACM Reference Format:                                                                   only APIs, and obsolete or legacy systems may survive as binaries
                                         Tianhai Liu, Maximilian Müller, Tobias Hey, Vitus Lüntzel, Muhammad                     after build environments or original source repositories have been
                                         Minhas, Anne Koziolek, and Bernhard Beckert. 2026. Can Formal Specifica-
                                                                                                                                 lost. Exposing implementations to external LLMs may be unaccept-
                                         tions Be Synthesized from Tests Alone?. In Proceedings of the 41st IEEE/ACM
                                                                                                                                 able, even under contractual safeguards, while maintaining local,
                                         International Conference on Automated Software Engineering (ASE ’26), Oc-
                                         tober 12–16, 2026, Munich, Germany. ACM, New York, NY, USA, 5 pages.                    state-of-the-art infrastructure is often impractical for SMEs.
                                         https://doi.org/10.1145/3832783.3834549                                                    These constraints lead us to the research question: Can formal
                                                                                                                                 specifications be synthesized from tests and their execution observa-
                                                                                                                                 tions? We assume that such long-lived system implementations are
                                                                                                                                 trusted as the reference behavior. As a first step, we study whether
                                                                                                                                 the behavioral knowledge encoded in test code and execution traces
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.   can guide LLMs towards meaningful formal specifications without
                                         ASE ’26, Munich, Germany
                                         © 2026 Copyright held by the owner/author(s).
                                                                                                                                 exposing implementation code to the LLM.
                                         ACM ISBN 979-8-4007-2882-2/2026/10
                                         https://doi.org/10.1145/3832783.3834549
ASE ’26, October 12–16, 2026, Munich, Germany                                                                                      Tianhai Liu et al.


   In our approach, the program is treated as a black box from the          as a specification that admits the observed test behaviors and is
external LLM’s perspective: the model is given the program inter-           consistent with the implementation within the analyzed bounds.
face, selected inputs, and observed return values or state changes,
but not the implementation internals. Test code is provided to the
                                                                            3.1    Test Execution Observation
model, enabling it to exploit oracle assertions, method-call context,
and other test-level cues during specification inference. To comple-        We execute selected unit tests for the method under test to obtain
ment this static test-side information, executions of the selected          concrete execution traces. These traces complement test code by
tests are encoded as structured observation traces that capture             making observed input-output and state-transition relations ex-
program states before and after the method call under test, includ-         plicit, which can refine specifications beyond assertions alone and
ing state changes that may not be explicit in the test code. The            provide behavioral cues when interface names are anonymized. Test
resulting candidates are then iteratively validated and refined in a        selection may be guided by domain expertise, coverage goals, and
counterexample-guided loop using bounded model checking (BMC),              operational constraints. For each selected test, engineers specify
where the program is locally analyzed in a white-box manner.                which objects and fields should be recorded immediately before and
   This work presents an initial investigation into the feasibility         after the method call. This defines a user-controlled projection of
of LLM-based formal specification synthesis from tests alone. Our           the observable program state, which can be implemented through
contributions are: (1) An exploration of the feasibility of decou-          logging or bytecode instrumentation. In the motivating example
pling specification inference from source code access, utilizing only       (Figure 1), we use logging statements for ease of presentation. Tests
test artifacts and execution traces, (2) a proposed approach that           that expose sensitive information through their code, inputs, or
combines oracle information from test code with behavioral obser-           recorded execution data are excluded.
vations from test execution, validating candidates via BMC, (3) a              From each execution trace, we extract a test execution observa-
preliminary evaluation on the SpecGenBench benchmark.                       tion that makes the behavioral evidence explicit and reusable for
                                                                            prompting, observation-coverage checking, and refinement (Sec-
2    Motivating Example                                                     tion 3.2–3.3). Each observation corresponds to one method invoca-
                                                                            tion and is represented as 𝑜𝑏𝑠 = ⟨𝑎𝑟𝑔𝑠, 𝑝𝑟𝑒, 𝑝𝑜𝑠𝑡, 𝑜𝑢𝑡𝑐𝑜𝑚𝑒⟩. The
   Figure 1 illustrates the setting for a simplified deposit method.
                                                                            𝑎𝑟𝑔𝑠 records the receiver-construction arguments and method-call
The implementation updates balance and an internal checksum,
                                                                            arguments, including parameters of parameterized tests. The 𝑝𝑟𝑒
while auditKey and calls to AuditService represent confidential
                                                                            and 𝑝𝑜𝑠𝑡 components record the selected program state immedi-
security or business logic that must not be disclosed. The test checks
                                                                            ately before and after the invocation, respectively. The 𝑜𝑢𝑡𝑐𝑜𝑚𝑒
only that the balance increases, whereas the engineer-controlled
                                                                            component records either normal termination, including the return
observations record selected non-sensitive state changes before and
                                                                            value, or an exception. Objects in 𝑝𝑟𝑒 and 𝑝𝑜𝑠𝑡 are represented by
after the call, e.g., sensitive fields auditKey are excluded.
                                                                            an identifier, a class name, and field-value mappings.
   Using test code and observations, our approach prompts an LLM
to synthesize a candidate Java Modeling Language (JML) [10] con-
tract. In this example, the model produces the candidate contract           3.2    Specification Inference
shown in Figure 1c1 . The candidate specification is then checked           We employ an LLM to synthesize a method-level JML specifica-
locally using BMC against the implementation via a consistency              tion from the method signature, the tests that invoke the method,
check and against the observations via a coverage check (see Sec-           and the corresponding observations. The zero-shot prompt follows
tion 3.3). Both checks pass, indicating that the candidate is con-          a two-stage structure. First, the model infers an initial contract
sistent with the implementation within the analyzed bounds and              from the test code, using test inputs and assertions as evidence for
admits the recorded observations. Importantly, the inferred con-            candidate preconditions, postconditions, exceptional behavior, and
tract can capture behaviors not explicitly asserted by the tests but        assignable locations. Second, the model refines this contract using
visible in the observations. For instance, the tests assert only the        the observations, in particular repeated pre/post-state relations and
updated balance, whereas the observations also expose the change            observed return or exception outcomes. To reduce unsupported
to checksum. Consequently, if the statement updating checksum is            generalization, the prompt enforces three rules. First, clauses should
removed, the inferred specification detects the violation, although         generalize beyond individual tests only when supported by test
the original test assertions would not.                                     assertions, repeated observations, or validation feedback. Second,
                                                                            unsupported domain assumptions should be reported as hypotheses
3    Proposed Approach                                                      rather than encoded directly as JML clauses. Third, the final output
Our approach infers specifications from test code and execution             should contain non-vacuous, syntactically valid JML clauses.
observations. As shown in Figure 2, tests are first executed to pro-
duce test execution observations, which make relevant pre- and              3.3    Specification Validation
post-state explicit. An LLM then uses the tests and observations to
                                                                            Given a candidate specification inferred from test code and ob-
synthesize a candidate JML specification. The candidate is validated
                                                                            servations, we validate it using two complementary checks. The
locally with BMC against the implementation and the recorded
                                                                            consistency check detects candidate specifications that are con-
observations. If validation fails, the counterexample is fed back
                                                                            tradicted by the implementation within the analyzed bounds. The
to the LLM for refinement. Otherwise, the candidate is returned
                                                                            observation-coverage check ensures that the inferred specification
1 Results may vary across runs and models; this example uses ChatGPT 5.4.   does not exclude any observed test behavior.
Can Formal Specifications Be Synthesized from Tests Alone?                                                      ASE ’26, October 12–16, 2026, Munich, Germany



           (a) Implementation                       (b) Simplified test code and observations               (c) Refined candidate specification
class Account {                                 @ParameterizedTest                                  /*@ public normal_behavior
 int balance, checksum;                         @CsvSource({"10,5", "20,3", "0,7"})                   @ requires
 String auditKey; // sensitive                  void testDeposit(int initial, int amount) {           @     balance <= Integer.MAX_VALUE - amount
 Account(int balance) {                           Account a = new Account(initial);                   @ && amount <= Integer.MAX_VALUE/31
   this.balance = balance;                        // log pre: initial,amount,a.balance,a.checksum     @ && checksum <= Integer.MAX_VALUE - 31*amount;
   this.checksum = 7;                             a.deposit(amount);                                  @
   this.auditKey = AuditSer.issueKey();           // log post: a.balance, a.checksum                  @ ensures balance == \old(balance) + amount;
 }                                                assertEquals(initial + amount, a.balance);          @ ensures checksum == \old(checksum)+ 31*amount;
 void deposit(int amount) {                     }                                                     @
   AuditSer.authorize(auditKey, amount);                                                              @ assignable balance, checksum;
                                                (10,5): (10,7) -> (15,162)
   balance += amount;                                                                                 @*/
                                                (20,3): (20,7) -> (23,100)
   checksum += 31 * amount;                                                                         void deposit(int amount);
                                                (0,7): (0,7) -> (7,224)
}}
                                    Figure 1: Motivating example: inferring a JML specification from tests.

                                                                                   Table 1: Preliminary results on the 22 SpecGenBench tasks.
                Tests
                                                                                   Task                History Result    Task                History Result
                     Test execution observation
                                                                                   abs                    11   Success   binarySearch         00   Error
            Observations                                                           biggest                11   Success   bubbleSortDesc       00   Error
                                                                                   calculate              11   Success   arrcmp               00   Error
            LLM Specification inference                                            canWinNim              11   Success   containsDuplicate    00   Error
                                                                                   conjunctOf             11   Success   convertToFahrenheit 00    Error
             Candidate                                                             disjunctOf             11   Success   convertToKelvin      00   Error
            specification           LLM Refinement                                 divisorGame            11   Success   convertToTitle       00   Error
                                                                                   addLoop              01,11 Success    copyArray            00   Error
         JJBMC Specification validation                                            checkString          01,11 Success    digitRoot            00   Error
                                                        (next iter.)               computeOverlapArea 01,11 Success      bubbleSort        00,00,00 Fail
                                   no                                              convertTemperature 10,10,11 Success   changeCase        10,10,10 Fail
                Valid?                       Counterexample
                                                                                      We encode observations as JML-annotated harness specifications
                     yes                                (max iter.)
                                                                                   that fix observed pre-states and require the corresponding post-
             Validated                                                             states. The target method is interpreted contractually rather than
                                               Not validated
            specification
                                                                                   inlined, making the check independent of the BMC loop-unrolling
 Figure 2: Overview of the specification inference pipeline.                       bound. A counterexample 𝑏 ∈ 𝐵𝑡𝑒𝑠𝑡 \ 𝐵𝑠𝑝𝑒𝑐 means that the contract
                                                                                   excludes an observed behavior and guides refinement. For example,
                                                                                   an observation 𝑏𝑎𝑙𝑎𝑛𝑐𝑒 : 10 ↦→ 15 under 𝑎𝑚𝑜𝑢𝑛𝑡 = 5 means that the
    We consider three behavior sets: (i) 𝐵𝑐𝑜𝑑𝑒 , behaviors exhibited               contract allows a call starting from 𝑎.𝑏𝑎𝑙𝑎𝑛𝑐𝑒 = 10 with 𝑎𝑚𝑜𝑢𝑛𝑡 = 5
by the implementation, (ii) 𝐵𝑡𝑒𝑠𝑡 , the subset exercised by the se-                and ending in 𝑎.𝑏𝑎𝑙𝑎𝑛𝑐𝑒 = 15. A candidate with requires amount
lected unit tests, and (iii) 𝐵𝑠𝑝𝑒𝑐 , behaviors admitted by the candidate           > 10 rejects this call and therefore fails the coverage check.
specification, with 𝐵𝑡𝑒𝑠𝑡 ⊆ 𝐵𝑐𝑜𝑑𝑒 by construction. A behavior 𝑏 cor-                  A candidate that passes both checks is treated as a validated
responds to a pre- and post-state pair of a method execution.                      candidate, not as a complete specification. The checks rule out two
    Consistency check. We treat the implementation as the local be-                concrete failure modes: contradicting the implementation within
havioral reference, reflecting our target setting of mature industrial             the analyzed bounds and excluding recorded test behaviors. They do
software that has evolved over the years and is already supported                  not establish that all unobserved behaviors are specified precisely;
by regression tests. A candidate specification should therefore not                specification strength is therefore assessed separately.
exclude behaviors that the implementation can exhibit within the
bounds of analysis. We use BMC to check, within a given bound,                     4    Preliminary Results
whether the precondition and program semantics admit an exe-                       We conducted an initial feasibility study on SpecGenBench [14].
cution that violates the postcondition. If such an execution exists,               SpecGenBench was originally designed for specification inference
BMC reports it as a counterexample 𝑏 ∈ 𝐵𝑐𝑜𝑑𝑒 \ 𝐵𝑠𝑝𝑒𝑐 , showing                     from source code, where multiple implementations of the same API
that the specification excludes an implementation behavior and                     provide complementary evidence about the intended behavior. In
is therefore inconsistent. We convert the counterexample into an                   contrast, our approach infers specifications from tests and execution
additional observation and feed it back to the LLM for refinement.                 observations without exposing the implementation source code.
    Observation-coverage check. The consistency check ensures                      We therefore evaluate our approach at the API level, treating each
that the candidate specification admits all implementation behav-                  API as a separate target-specification task.
iors within the analyzed bound, e.g., bounded loop unrollings. If                     For each API, we use gpt-oss-120b [18] to generate JUnit tests.
this bound is sufficient, the observed execution behaviors would                   Across the evaluated tasks, these tests achieve an average instruc-
already be admitted by the specification. However, tests may exer-                 tion coverage of 76.9%, providing a coarse sanity check that the
cise behaviors outside the BMC search space. We therefore perform                  inferred specifications are not based solely on trivial executions.
an observation-coverage check that directly checks whether each                    We use GPT-5.4 [17] to infer and refine candidate JML specifica-
recorded test behavior is admitted by the candidate specification.                 tions. Each candidate is checked with JJBMC [2] using its default
ASE ’26, October 12–16, 2026, Munich, Germany                                                                                  Tianhai Liu et al.


loop-unrolling bound of 5 against two criteria: implementation           the approach on proprietary industrial software whose implemen-
consistency and observation admission. Such bounds are a known           tations and intended specifications are not publicly available, and
source of precision concerns in bounded verification [13]. Failed        by anonymizing the method and test code in SpecGenBench.
candidates are refined using validation feedback for up to 3 iter-
ations per task. We evaluate our prototype on 22 SpecGenBench            5   Related Work
APIs compatible with JJBMC. Their implementations use Booleans,          Dynamic specification inference derives likely properties from ob-
integers, floating-point values, arrays, and loops. We exclude tasks     served executions. Daikon [5] pioneered this line by mining in-
that require features JJBMC doesn’t support, such as strings or          variants from instrumented runs, while later work on specification
reachability-style heap properties.                                      mining inferred temporal rules, API protocols, behavioral patterns,
   Table 1 shows the evaluation results. We classify the outcomes        and algebraic specifications from execution traces and program
as follows: Success means that the final candidate passes both the       interactions [1, 8]. Subsequent approaches extended the predicate
consistency and observation-coverage checks; Error means that            space with quantified properties, implication-style specifications,
the generated JML is not supported by JJBMC; and Fail means              or evolutionary search [15, 16, 27]. These techniques are related
that the refinement iteration bound is reached without obtaining         to our use of observations, but they typically rely on predefined
a candidate that passes both checks. In the history column, each         templates, handcrafted predicates, or trace mining rather than ex-
iteration is encoded as a two-bit outcome: the first bit denotes         ploiting test-code oracle structure and LLM-based generalization.
the consistency check, and the second denotes the observation-              Specification synthesis approaches such as AutoSpec [29], Spec-
coverage check; 1 indicates success and 0 indicates failure. For         Gen [14], and Allo2JML [7], as well as works on loop invariant
example, 01, 11 means that consistency fails but coverage passes in      generation [3, 4, 21, 25] and class invariant generation [24], demon-
the first iteration, while both checks pass in the second.               strate the potential of automated specification synthesis.
   The prototype succeeds on 11 of the 22 tasks. Among these, 7             Granberry et al. [6] further enrich prompts with generated tests
are solved in the first iteration, while 4 require refinement. The       and static analysis results. In contrast, our work explores a com-
convertTemperature case is representative of the refinement. The         plementary setting in which the LLM receives controlled test code
initial specification expressed the expected conversion results as       and sanitized observations, while implementation code is excluded
postcondition result[0] = celsius + 273.15, where celsius is             from the prompt and used only for local validation.
the parameter of the tested method. During refinement, JJBMC                Test- and oracle-based techniques infer executable assertions
reported a consistency violation caused by unsafe JML expressions,       or postconditions from generated executions or transformation
such as dereferencing \result or accessing array elements without        traces [31]. Like our approach, they treat executions as evidence of
guards. Using this feedback, the LLM added well-definedness guards       intended behavior. However, they usually aim to strengthen test
\result != null && \result.length >= 1 ⇒ \result[0] ==                   oracles or learn assertions, rather than to synthesize JML method
celsius + 273.15. Such guards avoid null dereferences and out-           contracts. Our approach uses test code structure and heap observa-
of-bounds accesses during JML evaluation.                                tions as evidence for LLM-based generalization, followed by local
   The dominant limitation is compatibility with the JML fragment        JML validation.
supported by JJBMC. Among the 22 tasks, 9 terminate with an Error
because the generated specifications contain constructs outside the
                                                                         6   Conclusion and Future Work
fragment supported by JJBMC, such as \num_of, ghost or model
fields, and arithmetic expressions over quantified variables. Since      We investigated whether LLMs can synthesize formal specifications
these constructs are valid in standard JML but cannot be validated       from tests alone. Our framework extracts structured execution ob-
by the current toolchain, we treat these cases primarily as checker-     servations, combines them with test-oracle information to generate
compatibility failures rather than semantic failures of the inferred     candidate JML specifications, and validates them through BMC-
specifications after closer manual investigation.                        based counterexample-guided refinement. This behavior-oriented
   Checker interaction also explains the two fail cases. These tasks     approach avoids reliance on source-code structure. On 22 SpecGen-
reach the refinement bound without obtaining a candidate that            Bench API-level tasks, our prototype automatically generated and
is both consistent with the implementation and covers the obser-         validated specifications for 11 using JJBMC.
vations. In these cases, JJBMC reports failed checks but does not           Test-level evidence provides partial behavioral coverage. To off-
provide an informative counterexample, returning only an asser-          set missing source-code context, we plan to incorporate public doc-
tion failure with an empty concrete example. Consequently, the           umentation [32], API specifications [19], and usage examples [23]
LLM receives little actionable feedback and can only guess how to        to capture intent and resolve behavior under-specified by tests.
refine the candidate specification.                                         We will also address scalability by summarising large traces
   The results provide early evidence for the feasibility of inferring   into representative behavioral patterns before inference. To mit-
JML specifications from test code and observations, while identi-        igate BMC state-space explosion, we plan to combine bounded
fying checker-aware specification generation as the main current         validation with program slicing [26, 28] and incremental symbolic
challenge. Future work will therefore provide checker-aware pre-         execution [11, 20].
checking and a repair layer, and improve JJBMC.
   A threat to validity is the potential leakage of benchmark data.      Acknowledgements
SpecGenBench tasks or similar code fragments may have appeared           This work was supported by the German Research Foundation
in LLM pre-training data. We plan to mitigate this risk by evaluating    (DFG) – SFB 1608 – 501798263.
Can Formal Specifications Be Synthesized from Tests Alone?                                                                      ASE ’26, October 12–16, 2026, Munich, Germany


Data Availability Statement                                                                 [15] Bertrand Meyer, Ilinca Ciupa, Andreas Leitner, and Lisa Ling Liu. 2007. Automatic
                                                                                                 Testing of Object-Oriented Software. In International Conference on Current Trends
All benchmark, evaluation data, and prototype artifacts are publicly                             in Theory and Practice of Computer Science. Springer, 114–129. doi:10.1007/978-3-
available at [12].                                                                               540-69507-3_9
                                                                                            [16] Facundo Molina, Pablo Ponzio, Nazareno Aguirre, and Marcelo Frias. 2021.
                                                                                                 EvoSpex: An Evolutionary Algorithm for Learning Postconditions. In Inter-
References                                                                                       national Conference on Software Engineering. IEEE, 1223–1235. doi:10.1109/
 [1] Glenn Ammons, Rastislav Bodík, and James R. Larus. 2002. Mining Specifications.             ICSE43902.2021.00112
     ACM SIGPLAN Notices 37, 1 (2002), 4–16. doi:10.1145/565816.503275                      [17] OpenAI. 2026. GPT-5.4 Model. https://developers.openai.com/api/docs/models/
 [2] Bernhard Beckert, Michael Kirsten, Jonas Klamroth, and Mattias Ulbrich. 2020.               gpt-5.4. Accessed: 2026-05-12.
     Modular Verification of JML Contracts Using Bounded Model Checking. In Inter-          [18] OpenAI. 2026. gpt-oss-120b Model. https://developers.openai.com/api/docs/
     national Symposium on Leveraging Applications of Formal Methods, Verification               models/gpt-oss-120b. Accessed: 2026-05-12.
     and Validation, Vol. 12476. Springer, 60–80. doi:10.1007/978-3-030-61362-4_4           [19] Rahul Pandita, Xusheng Xiao, Hao Zhong, Tao Xie, Stephen Oney, and Amit
 [3] Bernhard Beckert, Jonas Klamroth, Wolfram Pfeifer, Patrick Röper, and Samuel                Paradkar. 2012. Inferring Method Specifications from Natural Language API
     Teuber. 2025. Towards Combining the Cognitive Abilities of Large Language                   Descriptions. In International Conference on Software Engineering. IEEE, 815–825.
     Models with the Rigor of Deductive Program Verification. In International Sym-              doi:10.1109/ICSE.2012.6227137
     posium on Leveraging Applications of Formal Methods, Verification and Validation.      [20] Corina S. Păsăreanu and Willem Visser. 2009. A Survey of New Trends in Symbolic
     Springer, 242–257. doi:10.1007/978-3-031-75387-9_15                                         Execution for Software Testing and Analysis. International Journal on Software
 [4] Saikat Chakraborty, Shuvendu Lahiri, Sarah Fakhoury, Akash Lal, Madanlal                    Tools for Technology Transfer 11, 4 (2009), 339–353. doi:10.1007/s10009-009-0118-1
     Musuvathi, Aseem Rastogi, Aditya Senthilnathan, Rahul Sharma, and Nikhil               [21] Muhammad A. A. Pirzada, Giles Reger, Ahmed Bhayat, and Lucas C. Cordeiro.
     Swamy. 2023. Ranking LLM-Generated Loop Invariants for Program Verification.                2024. LLM-Generated Invariants for Bounded Model Checking Without Loop
     In Findings of the Association for Computational Linguistics: The 2023 Conference on        Unrolling. In International Conference on Automated Software Engineering. 1395–
     Empirical Methods in Natural Language Processing. Association for Computational             1407. doi:10.1145/3691620.3695512
     Linguistics, 9164–9175. doi:10.18653/v1/2023.findings-emnlp.614                        [22] Armand Puccetti, Gaël de Chalendar, and Pierre-Yves Gibello. 2021. Combining
 [5] Michael D. Ernst, Jake Cockrell, William G. Griswold, and David Notkin. 1999.               Formal and Machine Learning Techniques for the Generation of JML Specifica-
     Dynamically Discovering Likely Program Invariants to Support Program Evo-                   tions. In Workshop on Formal Techniques for Java-like Programs. ACM, 59–64.
     lution. In International Conference on Software Engineering. ACM, 213–224.                  doi:10.1145/3464971.3468425
     doi:10.1145/302405.302467                                                              [23] Veselin Raychev, Martin Vechev, and Eran Yahav. 2014. Code Completion with
 [6] George Granberry, Wolfgang Ahrendt, and Moa Johansson. 2025. Specify What?                  Statistical Language Models. ACM SIGPLAN Notices 49, 6 (2014), 419–428. doi:10.
     Enhancing Neural Specification Synthesis by Symbolic Methods. In Integrated                 1145/2666356.2594321
     Formal Methods. Springer, 307–325. doi:10.1007/978-3-031-76554-4_19                    [24] Chuyue Sun, Viraj Agashe, Saikat Chakraborty, Jubi Taneja, Clark Barrett, David
 [7] Daniel Grunwald, Christoph Gladisch, Tianhai Liu, Mana Taghdiri, and Shmuel S.              Dill, Xiaokang Qiu, and Shuvendu K. Lahiri. 2026. ClassInvGen: Class Invariant
     Tyszberowicz. 2014. Generating JML Specifications from Alloy Expressions. In                Synthesis Using Large Language Models. In AI Verification. Springer, 64–96.
     Haifa Verification Conference. Springer, 99–115. doi:10.1007/978-3-319-13338-6_9            doi:10.1007/978-3-031-99991-8_4
 [8] Johannes Henkel and Amer Diwan. 2003. Discovering Algebraic Specifications             [25] Samuel Teuber and Bernhard Beckert. 2025. Next Steps in LLM-Supported Java
     from Java Classes. In European Conference on Object-Oriented Programming.                   Verification. In International Workshop on Next-Generation Software Engineering.
     Springer, 431–456. doi:10.1007/978-3-540-45070-2_19                                         IEEE, 1–4. doi:10.1109/NSE66660.2025.00007
 [9] Thanh Le-Cong, Bach Le, and Toby Murray. 2025. Can LLMs Reason About Pro-              [26] Frank Tip. 1995. A Survey of Program Slicing Techniques. Journal of Programming
     gram Semantics? A Comprehensive Evaluation of LLMs on Formal Specification                  Languages 3, 3 (1995), 121–189.
     Inference. In Annual Meeting of the Association for Computational Linguistics. As-     [27] Yi Wei, Carlo A. Furia, Nikolay Kazmin, and Bertrand Meyer. 2011. Inferring
     sociation for Computational Linguistics, 21991–22014. doi:10.18653/v1/2025.acl-             Better Contracts. In International Conference on Software Engineering. ACM, 191–
     long.1068                                                                                   200. doi:10.1145/1985793.1985820
[10] Gary T. Leavens, Albert L. Baker, and Clyde Ruby. 2006. Preliminary design of          [28] Mark Weiser. 1984. Program Slicing. IEEE Transactions on Software Engineering
     JML: a behavioral interface specification language for Java. SIGSOFT Softw. Eng.            SE-10, 4 (1984), 352–357.
     Notes 31, 3 (May 2006), 1–38. doi:10.1145/1127878.1127884                              [29] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun
[11] Tianhai Liu, Mateus Araújo, Marcelo d’Amorim, and Mana Taghdiri. 2014. A                    Li, Shing-Chi Cheung, and Cong Tian. 2024. Enchanting Program Specification
     Comparative Study of Incremental Constraint Solving Approaches in Symbolic                  Synthesis by Large Language Models Using Static Analysis and Program Ver-
     Execution. In Haifa Verification Conference, Vol. 8855. Springer, 284–299. doi:10.          ification. In International Conference on Computer Aided Verification. Springer,
     1007/978-3-319-13338-6_21                                                                   302–328. doi:10.1007/978-3-031-65630-9_16
[12] Tianhai Liu, Maximilian Müller, Tobias Hey, Muhammad Minhas, Vitus Lüntzel,            [30] Guangyuan Wu, Weining Cao, Yuan Yao, Hengfeng Wei, Taolue Chen, and
     Anne Koziolek, and Bernhard Beckert. 2026. Dataset and Artifacts for Can Formal             Xiaoxing Ma. 2024. LLM Meets Bounded Model Checking: Neuro-symbolic
     Specifications Be Synthesized from Tests Alone? doi:10.5281/zenodo.21249653                 Loop Invariant Inference. In International Conference on Automated Software
[13] Tianhai Liu, Shmuel S. Tyszberowicz, Bernhard Beckert, and Mana Taghdiri.                   Engineering. ACM, 406–417. doi:10.1145/3691620.3695014
     2017. Computing Exact Loop Bounds for Bounded Program Verification. In                 [31] Tao Xie. 2006. Augmenting Automatically Generated Unit-Test Suites with
     International Symposium on Theoretical Aspects of Software Engineering. Springer,           Regression Oracle Checking. In ECOOP 2006 – Object-Oriented Programming.
     147–163. doi:10.1007/978-3-319-69483-2_9                                                    Springer, 380–403. doi:10.1007/11785477_23
[14] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. 2025. SpecGen: Auto-          [32] Hao Zhong, Lu Zhang, Tao Xie, and Hong Mei. 2011. Inferring Specifications
     mated Generation of Formal Program Specifications via Large Language Models.                for Resources from Natural Language API Documentation. Automated Software
     In International Conference on Software Engineering. IEEE, 16–28. doi:10.1109/              Engineering 18 (2011), 227–261. doi:10.1007/s10515-011-0082-3
     ICSE55347.2025.00129
                                                                                            Received 2026-05-12; accepted 2026-07-02
