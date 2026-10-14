                                                        Large Language Models for Validating Network Protocol Parsers

                                                        Mingwei Zheng                                Danning Xie                             Xiangyu Zhang
                                              Department of Computer Science              Department of Computer Science           Department of Computer Science
                                                     Purdue University                           Purdue University                        Purdue University
                                                    West Lafayette, USA                        West Lafayette, USA                      West Lafayette, USA
                                                   zheng618@purdue.edu                          xie342@purdue.edu                       xyzhang@purdue.edu
arXiv:2504.13515v1 [cs.SE] 18 Apr 2025




                                         Abstract—Network protocol parsers are essential for enabling         including memory corruption, information leakage, and
                                         correct and secure communication between devices. Bugs in            denial-of-service attacks. For instance, the Heartbleed [4]
                                         these parsers can introduce critical vulnerabilities, including      vulnerability in OpenSSL [5]’s TLS parser allowed attackers
                                         memory corruption, information leakage, and denial-of-service        to access sensitive user information due to a missing bounds
                                         attacks. An intuitive way to assess parser correctness is to         check. Similarly, CVE-2021-41773 [6] in Apache’s HTTP
                                         compare the implementation with its official protocol standard.      server exposed confidential files through a path traversal flaw
                                         However, this comparison is challenging because protocol             in the request parser.
                                         standards are typically written in natural language, whereas             Validating the correctness of network protocol parsers is
                                         implementations are in source code. Existing methods like model      inherently challenging. A natural approach is to compare the
                                         checking, fuzzing, and differential testing have been used to find   parser implementation against its official protocol standard to
                                         parsing bugs, but they either require significant manual effort      identify inconsistencies. However, this process is complicated
                                         or ignore the protocol standards, limiting their ability to detect   by a fundamental representational gap: protocol standards
                                         semantic violations. To enable more automated validation of          are typically written in natural language (e.g., RFCs), while
                                         parser implementations against protocol standards, we propose        implementations are written in source code. Although both
                                         PARVAL, a multi-agent framework built on large language              aim to specify the same behavior, their different representa-
                                         models (LLMs). PARVAL leverages the capabilities of LLMs to          tions hinder direct comparison, making systematic validation
                                         understand both natural language and code. It transforms both        a significant challenge.
                                         protocol standards and their implementations into a unified              Various techniques have been proposed to address this
                                         intermediate representation, referred to as format specifications,   challenge. Model checking [7]–[9] verifies parser behavior
                                         and performs a differential comparison to uncover inconsis-          against formal protocol models to detect logical errors. While
                                         tencies. We evaluate PARVAL on the Bidirectional Forwarding          effective, it often requires manual construction of formal
                                         Detection (BFD) protocol. Our experiments demonstrate that           models, making it impractical for applying to large and fre-
                                         PARVAL successfully identifies inconsistencies between the           quently evolving protocols. Fuzzing [10], [11] automatically
                                         implementation and its RFC standard, achieving a low false           produces large volumes of test inputs to expose memory-
                                         positive rate of 5.6%. PARVAL uncovers seven unique bugs,            related issues, such as crashes. However, it primarily targets
                                         including five previously unknown issues.                            low-level bugs and fails to assess whether the parser conforms
                                                                                                              to the protocol’s intended semantics, leaving many semantic
                                         Index Terms—Network protocol parsing, format specifications,
                                                                                                              bugs [12]–[15] undetected. Differential analysis [12], [16]
                                         large language models
                                                                                                              identifies inconsistencies by comparing how different imple-
                                                                                                              mentations handle the same input. This approach assumes
                                         1. Introduction                                                      that at least one implementation behaves correctly and may
                                                                                                              miss bugs shared across all versions. While these methods
                                             Network protocols specify the rules that control com-
                                                                                                              are effective in certain situations, they fall short of providing
                                         munication between devices, for example, TLS [1] for
                                                                                                              an efficient way to validate parser implementations against
                                         secure communication, FTP [2] for file transfers, and IP [3]
                                                                                                              official protocol standards written in natural language.
                                         for routing data. Network protocol parsing is a critical
                                         component of protocol implementations, responsible for               Our Approach. We propose PARVAL, an LLM-based
                                         analyzing incoming packets, validating their correctness,            multi-agent framework for validating parser implementa-
                                         and discarding malformed ones. This process protects data            tions against their official protocol standards. PARVAL uses
                                         integrity and enhances system security by preventing the             LLMs to automatically abstract both the natural language
                                         processing of potentially harmful packets.                           documentation and the parser implementation into a unified
                                             Despite their critical role, network protocol parsers are        intermediate representation, called format specifications.
                                         error-prone, which can lead to severe security vulnerabilities,      These specifications capture the expected packet structure
and parsing logic, enabling direct comparison between the          1    void bfd_recv_cb (struct thread *t)
                                                                   2    {
protocol documentation and its implementation.                     3             …
    LLMs have demonstrated strong capabilities in extracting       4          if (sd == bvrf->bg_shop || sd == bvrf->bg_mhop) {
format specifications from natural language [15], [17], but        5             mlen = bfd_recv_ipv4(sd, msgbuf, sizeof(msgbuf), …);
applying them to source code remains challenging. In real-         6          } else if (sd == bvrf->bg_shop6 || sd == bvrf->bg_mhop6) {
                                                                   7             mlen = bfd_recv_ipv6(sd, msgbuf, sizeof(msgbuf), …);
world codebases, parsing logic is often scattered across           8          }
multiple files and functions [11], [12], making it difficult       9
to gather the full context needed for accurate format ex-          10        if (mlen < BFD_PKT_LEN) {
traction. Moreover, LLMs are prone to generating incorrect         11           cp_debug("too small (%ld bytes)", mlen);
                                                                   12           return;
or incomplete outputs (hallucinations), so validating and
                                                                   13        }
refining the extracted formats is essential. This typically        14        /* Parse the control header for inconsistencies:
relies on unit tests to check whether the extracted format         15        struct bfd_pkt *cp = (struct bfd_pkt *)(msgbuf);
matches the implementation behavior. However, without a            16        if (BFD_GETVER(cp->diag) != BFD_VERSION) {
well-isolated parsing module, generating and executing such        17           cp_debug("bad version %d", BFD_GETVER(cp->diag));
                                                                   18           return;
tests is difficult. Consequently, errors in the extracted format   19        }
specifications may go unnoticed, undermining the reliability       20           …
of comparing the format specifications extracted from the          21   }
parser implementation and the protocol standard.
                                                                   Figure 1: Entry Parsing Function in BFD Implementation
    To tackle the challenge of retrieving parsing-relevant con-
text from large codebases, PARVAL introduces a Retrieval-              improve the accuracy of format specification extraction
Augmented Program Analysis Agent to automatically extract              and mitigates the impact of LLM hallucination. We
code segments directly related to protocol parsing while               compare the extracted format specification against a
excluding irrelevant ones. This agent uses a dependency-               manually annotated ground truth and find that PARVAL
aware retrieval mechanism, beginning from the entry parsing            successfully extract the full parsing logic.
function and recursively using LLMs to analyze data depen-           • We implement the proposed approach in PARVAL . We
                                                                                                                           1
dencies, control flow, and function calls. It incrementally            have evaluated PARVAL on the Bidirectional Forwarding
collects parsing relevant segments until the complete parsing          Detection (BFD) protocol to validate its parser implemen-
logic is isolated.                                                     tation against the corresponding RFC standard. PARVAL
    To reduce LLM hallucinations in LLM-generated format               successfully identifies seven unique bugs, including five
specifications, PARVAL isolates the extracted parsing logic            previously undiscovered.
into a standalone, executable module. This module takes a          Organization. Section 2 presents a motivation example to
buffer and its length as input and returns a boolean value         illustrate the challenges and our solutions. Section 3 details
indicating whether parsing succeeds. PARVAL then extracts          our design. Section 4 evaluates the effectiveness of our tool.
a format specification from this module and generates unit         Section 5 discusses limitations and future work. Section 6
tests to check whether the module’s behavior matches the           reviews related work. Section 7 concludes the paper.
extracted format specification. Any discrepancies identified
through testing are used as feedback to iteratively refine the
format, improving its accuracy over time.                          2. Motivating Example
Contributions. This paper explores the potential of LLMs               Figure 1 shows a simplified version of the entry pars-
to validate parser implementations against natural language        ing function in the BFD implementation. The function
protocol standards. While our approach does not guarantee          bfd_recv_cb handles incoming BFD packets. It begins
soundness or completeness, our evaluation on a real-world          by determining the socket type (sd) and invokes either
protocol demonstrates its practical effectiveness, providing a     bfd_recv_ipv4 or bfd_recv_ipv6 to read the mes-
strong starting point for further investigation. In summary,       sage into msgbuf (lines 4 - 8). It then validates the message
our main contributions are:                                        length mlen (lines 10 - 13) and proceeds to parse the control
 • We introduce PARVAL, a multi-agent framework that uses          header (lines 14 - 20).
   LLMs to extract parsing behaviors from both source code             To validate the parser implementation, we leverage large
   and protocol standards. These behaviors are represented         language models (LLMs) to extract format specifications
   in a unified intermediate representation, called format         from the source code and the RFC document. By trans-
   specifications, to enable direct comparison.                    lating both into a unified representation, we enable direct
 • PARVAL introduces a dependency-aware retrieval mech-            comparison and systematic validation. However, accurately
   anism that automatically identifies and extracts relevant       extracting protocol formats from source code presents two
   parsing logic by analyzing data flow, control flow, and         key challenges.
   function dependencies throughout the codebase.                  Challenge 1: Retrieving Parsing-Related Context. LLMs
 • PARVAL isolates parsing logic into a standalone, exe-           require complete parsing contexts to accurately extract
   cutable module, enabling test case generation to validate
   and refine the extracted format specifications. This helps        1. PARVAL is available at: https://github.com/zmw12306/PARVAL
protocol formats. However, in real-world codebases, parsing-                                                   1 Parser Isolation
relevant logic is often spread across multiple functions,                             Retrieval-Augmented
files, and Retrieval-Augmented
           directories, making it challenging           to automatically                                                       Read
                                                                                     Program Analysis Agent
                                           read
identify and
           Programextract    all relevant code. For example, in
                    Analysis Agent
Figure 1, struct bfd_pkt (line 15) and BFD_GETVER
(line 16) are defined in separate write      files. Without retrieving                                                         Write                  Protocol
                                                                                      Module Isolation Agent
these dependencies,
              Coder Agent LLMs     cannot   fully  interpret  theCode
                                                         Protocol   parsing
                                                                        Base                                                 Execute                 Code Base
logic. Since feeding the entire codebase execute    exceeds the context
window of LLMs, a selective context retrieval strategy is                                      2   Spec. Extraction from Code                            4
necessary.                                                                                                                                        Parser Validation
               module                             spec                             Isolated Parsing Module                     CodeSpec
Our Solution: We design          Spec
                                     a dependency-aware retrieval
mechanism that guides LLMs       Agent to selectively collect parsing-                                       SpecAgent
relevant code. Starting from the entry parsing function,              bug it
                         syntax/semantics                                                           Syntax & Semantics Check
traces input buffer usage       throughcheck
                                           data and control dependen-
                                                                differential
cies, as well doc
               as function calls, to collect essential
                                                  spec
                                                            context
                                                                analysissuch
                                                                                                                                                    Differential
                                                                                              3 Spec. Extraction from Doc.                           Analysis
as structs, macros, and helper functions. This dependency
                                Spec                                                 Document                                   DocSpec
analysis guides LLMs to Agent    retrieve only the necessary context
to accurately extract protocol formats.                                                                      SpecAgent
                            syntax check
Challenge 2: LLM Hallucinations in Extracted Formats.                                                    Syntax Check
LLMs may generate inaccurate format specifications that
deviate from actual parser behavior, such as involving                                      Figure 2: The Overview of PARVAL
incorrect field types, lengths, or ordering. To correct these
hallucinations, it is essential to test the consistency between
the extracted format specification and the original parser,                       Task Description: Refactor the given protocol implementation to isolate input
using the test results to guide iterative refinement. However,                    parsing logic into a new parser function. This function should:
                                                                                  • Take only two parameters: the input buffer and its length.
this feedback loop becomes unreliable when the parsing logic                      • Return True if the input is valid, False otherwise.
is tightly coupled with other parsing unrelated operations.                       • Exclude checks unrelated to the input buffer or its length.
For instance, in Figure 1, the function bfd_recv_cb                               Iteratively call 'query_name' to retrieve definition from the codebase. Please
expects a thread structure containing socket state and                            output complete function content for each newly added or modified function.
runtime configuration. Before any parsing occurs, the func-
                                                                                  Example: [example]
tion performs socket-related checks. In contrast, test inputs                     Entry parsing function: [function]
generated from the extracted format consist solely of raw
packet data and cannot be passed directly to bfd_recv_cb.
To run a test, each packet data must be wrapped in a                            Figure 3: LLM Task Description for Parser Isolation
correctly initialized thread structure. This additional setup
introduces complexity and obscures whether test failures                       and the Module Isolation Agent collaborate to extract an
stem from the format itself, incorrect thread initialization,                  Isolated Parsing Module from the protocol codebase. In
or buggy socket handling. This undermines the reliability of                   Stage 2 Spec. Extraction from Code (Section 3.2) and
test-based feedback, making it difficult to detect and correct                 Stage 3 Spec. Extraction from Doc. (Section 3.3), the
LLM hallucinations in the extracted format.                                    Spec Agent extracts format specifications from the Isolated
                                                                               Parsing Module and protocol standards, producing CodeSpec
Our Solution: To reduce LLM hallucinations, PARVAL                             and DocSpec, respectively. In Stage 4 Parser Validation
extracts the parsing logic into a standalone, executable                       (Section 3.4), the two format specifications are compared
module that focuses only on packet parsing. This module                        to identify inconsistencies, which may point to bugs in the
takes a raw buffer and its length as input and returns a                       implementation or missing details in the protocol standard.
boolean indicating whether parsing succeeds. Valid and                         The following sections describe each stage in detail.
invalid test packets generated from the extracted format
specification are directly passed to this module. If the module
rejects valid packets or accepts invalid ones, this indicates a                3.1. Stage 1: Parser Isolation
mismatch between the LLM extracted format specification
and the actual parsing behavior. Such mismatches are used to
iteratively refine the extracted format, improving its accuracy.                   In this stage, we isolate the parsing logic from the
                                                                               protocol codebase using an LLM-based multi-agent frame-
3. Approach                                                                    work that integrates dependency-aware retrieval mechanism
                                                                               and parser module construction. As shown in Figure 2,
    Figure 2 presents an overview of our approach, which                       the framework consists of two LLM agents: the Retrieval-
consists of four stages. In Stage 1 Parser Isolation (Sec-                     augmented Program Analysis Agent and the Module Isolation
tion 3.1), the Retrieval-Augmented Program Analysis Agent                      Agent, augmented by tools to interact (i.e., read, write, or
execute) with the protocol codebase. The task description           1    bool parse_bfd_packet (uint8_t *msgbuf, size_t mlen)
for this multi-agent system is shown in Figure 3.                   2    {
                                                                    3          if (mlen < BFD_PKT_LEN) {
     The Retrieval-augmented Program Analysis Agent uses            4             cp_debug("too small (%ld bytes)", mlen);
an LLM to iteratively analyze code and retrieve relevant            5             return false;
context through a dependency-aware retrieval mechanism.             6          }
Starting from the entry parsing function, it traces input           7          /* Parse the control header for inconsistencies:
buffer usage via data and control dependencies, as well as          8          struct bfd_pkt *cp = (struct bfd_pkt *)(msgbuf);
function calls, to identify macros, types, and helper functions     9          if (BFD_GETVER(cp->diag) != BFD_VERSION) {
critical to parsing. It then employs an AST-based retrieval         10            cp_debug("bad version %d", BFD_GETVER(cp->diag));
                                                                    11            return false;
tool, built on Tree-sitter [18], to extract the corresponding
                                                                    12         }
definitions from the source code (read). In parallel, the                        … // other parsing logic
                                                                    13
Module Isolation Agent utilizes the retrieved context to            14         return true;
construct an isolated parsing module. It iteratively writes         15   }
identified parsing logic into a standalone, executable module
and executes it, continuously refining the module based on                 Figure 4: Isolated Parsing Module Example
build results and error feedback. When additional definitions
or clarifications are needed, it collaborates with the Retrieval-   Syntax Check. To ensure syntactic correctness, SpecAgent
augmented Program Analysis Agent to retrieve more contexts.         uses the DSL’s grammar to generate an initial CodeSpec from
The final output is a fully isolated parsing module that            the isolated parsing module. It then iteratively validates and
takes an input buffer and its length as input and returns           refines the specification until it conforms to the DSL rules.
a boolean indicating parsing success. Unlike the original           Semantic Check. Beyond syntactic correctness, CodeSpec
codebase, which often mixes parsing with other processing           must match the semantic behavior of the isolated parsing
logic, this isolated module contains only the parsing logic         module. We verify this by generating symbolic test cases from
and is independently testable.                                      CodeSpec—positive cases that conform to the format and
                                                                    negative ones that violate it. These are run against the isolated
Example. For the entry parsing function shown in Fig-
                                                                    parsing module to check whether valid inputs are accepted
ure 1, isolating the parsing logic requires understand-
                                                                    and malformed ones are rejected. If a positive case fails
ing the behavior of its callee functions, as additional
                                                                    or a negative case passes, it indicates a semantic mismatch.
parsing logic may reside within them. To achieve this,
                                                                    To resolve such discrepancies, SpecAgent iteratively refines
LLMs must retrieve relevant context, just as a human
                                                                    CodeSpec based on the test outcomes. Specifically, when
would when analyzing the code. Hence, the Retrieval-
                                                                    a positive case fails, we instrument the parser to capture
augmented Program Analysis Agent retrieves the definition of
                                                                    its execution trace, which is then provided to SpecAgent
bfd_recv_ipv4, bfd_recv_ipv6, and BFD_GETVER
                                                                    to guide the correction. In contrast, if a negative case is
to determine whether they contain parsing-related operations.
                                                                    incorrectly accepted, SpecAgent analyzes how the input
The agent identifies msgbuf and mlen as the received BFD
                                                                    violates CodeSpec and adjusts the format to enforce the
packet and its length. Therefore, determining whether a piece
                                                                    intended parsing behavior.
of code contributes to BFD parsing involves analyzing its
dependencies on msgbuf and mlen. For example, at line
15 in Figure 1, msgbuf is cast into a bfd_pkt, making cp            3.3. Stage 3: Specification Extraction from Doc.
directly data-dependent on msgbuf. The if condition at line
16 operates on a field of cp and performs input validation,             In this stage, SpecAgent analyzes protocol standards (e.g.,
making it directly relevant to BFD packet parsing. In contrast,     RFCs) to extract a structured format specification, DocSpec,
the if conditions at lines 4 and 6 check the socket types           using the same DSL as in Stage 2. This transforms the
rather than BFD packet fields, hence irrelevant to BFD packet       natural language description of the message format—such as
parsing. The resulting Isolated Parsing Module generated by         field definitions, length constraints, and value ranges—into
the Module Isolation Agent is shown in Figure 4.                    a formal representation. Using a unified DSL enables direct,
                                                                    systematic comparison between DocSpec and the code-
                                                                    derived CodeSpec.
3.2. Stage 2: Specification Extraction from Code
                                                                    3.4. Stage 4: Parser Validation
    In this stage, we employ SpecAgent to transform the
isolated parsing module into a formal representation of the             In the final stage, we validate the parser implementation
input format. This representation, called CodeSpec, is written      by comparing the protocol specifications extracted from code
in a domain-specific language (DSL) for describing protocol         (CodeSpec, from Stage 2) and protocol standards (DocSpec,
formats. SpecAgent performs this translation automatically          from Stage 3). Using Differential Analysis, we identify
by analyzing the parsing logic and iteratively refining the         discrepancies such as mismatched fields or constraints. Each
resulting specification based on feedback from both syntax          inconsistency is manually examined to determine whether it
and semantic checks.                                                is a false positive or a true semantic mismatch. Confirmed
mismatches are then classified as either parser bugs or issues      TABLE 1: Precision and Recall for Format Specification
in the protocol standard.                                           Extraction from the Isolated Parsing Module
                                                                              Metric                  PARVAL     Precision     Recall
4. Evaluation                                                                 Field Name                11        100.0%      100.0%
                                                                              Field Type                11        100.0%      100.0%
    Our tool is built on top of AutoGen [19], a multi-agent                   Field Constraint           4        100.0%      100.0%
framework for developing LLM applications. We use Claude-
3.5 Sonnet [20] as the LLM API with a temperature of                and precision and recall are used to measure the correctness
0 to reduce randomness and enhance reproducibility. For             and completeness of the extracted specification.
repository interaction, we build our tool using Tree-sitter [18],   Results. As shown in Table 1, PARVAL correctly extracts
an AST-based parser to analyze and manipulate source code.          all 11 field names, 11 field types, and 4 field constraints
For protocol format extraction (Section 3.2 and Section 3.3),       with perfect precision and recall. Since the isolated parser
we use 3D language [21] as the DSL and EverParse [22]               fully encapsulates the original parsing logic, the extracted
as the syntax checker. We evaluate the effectiveness of our         CodeSpec is both accurate and complete for this target.
approach by addressing the following research questions:
                                                                    4.2.3. Stage 3: Specification Extraction from Doc. We
  • RQ1: How effective are the four stages of PARVAL?
                                                                    evaluate DocSpec, the format extracted from the RFC,
  • RQ2: How well does the LLM extract format specifica-
                                                                    by comparing it against a manually constructed ground
    tions from code compared to a baseline?
                                                                    truth, using precision and recall to assess accuracy and
  • RQ3: What are the root causes of the discrepancies
                                                                    completeness.
    between the implementation and the RFC?
  • RQ4: How much manual effort does PARVAL require?                TABLE 2: Precision and Recall for Format Specification
                                                                    Extraction from RFC Document
4.1. Dataset
                                                                              Metric                  PARVAL     Precision     Recall

    We evaluate PARVAL on the BFD protocol using the C-                       Field Name                37        100.0%      100.0%
                                                                              Field Type                37         97.3%       97.7%
based implementation from FRRouting [23] (stable/8.4), and                    Field Constraint          15        100.0%       58.3%
RFC 5880 [24] as the official protocol standard. PARVAL is
then applied to validate the implementation against the RFC.
                                                                    Results. As shown in Table 2, PARVAL extracts 37 field
                                                                    names, 37 field types, and 15 field constraints from the RFC
4.2. RQ1: Effectiveness of Each Stage in PARVAL                     document. Field names and types are extracted with near-
                                                                    perfect precision and recall, as they are explicitly defined.
4.2.1. Stage 1: Parser Isolation. We evaluate parser isola-         Constraint extraction is more difficult. While the precision
tion by measuring the precision and recall of the resulting         remains 100%, recall drops to 58.3%, this is because many
isolated parsing module. Precision reflects the correctness         constraints are implied rather than explicitly stated in the
of extracted parsing logic, while recall indicates how much         RFC documents. Despite some missing constraints, the high
of the original logic is preserved. Ground truth is estab-          precision indicates that those extracted constraints are reliable
lished by manually annotating the original parser, aided by         and useful for validation. In particular, if an implementation
NetLifter [11], which uses LLVM-based static analysis to            fails to enforce a constraint specified in DocSpec, it is highly
identify parsing-relevant IR instructions.                          likely to indicate a true implementation bug.
Results. The isolated parsing module achieves 100% preci-
sion and recall, showing that all validation logic is correctly     4.2.4. Stage 4: Parser Validation. We validate the parser by
extracted and preserved. This demonstrates PARVAL ’s                comparing CodeSpec and DocSpec, focusing on field type and
ability to isolate complete and accurate parsing logic. We          constraint differences, as field names do not affect behavior.
also assess whether isolation alters parser behavior. In the        Discrepancies are identified by mismatches between the two
BFD case, packet parsing does not depend on runtime context         specifications, and then traced back to source code and the
(e.g., socket type or protocol version), so the isolated module     RFC to determine whether they represent true inconsistencies.
maintains the intended input structure. However, for protocols      TABLE 3: Differential Analysis Results: CodeSpec vs.
influenced by configuration or negotiation state, isolation may     DocSpec
unintentionally broaden or restrict accepted inputs—requiring
additional control flow modeling to preserve these semantics.        Discrepancy Type    Total Inconsis.     True Inconsis.   Extraction Error
                                                                     Field Type                  21               21                 0
                                                                     Field Constraint            15               13                 2
4.2.2. Stage 2: Specification Extraction from Code.
We evaluate PARVAL ’s accuracy in generating CodeSpec,               Total                       36               34                 2
the format specification extracted from the isolated parsing
module, consisting of field names, types, and constraints. A        Results. As shown in Table 3, PARVAL reports 36 discrep-
ground truth is manually constructed from the module’s logic,       ancies between CodeSpec and DocSpec, including 21 type
and 15 constraint mismatches. Among the 36 discrepancies,                TABLE 6: The Detected Implementation Bugs
34 are confirmed as true inconsistencies, and only two are        No.    Bug Description                                                                     New
false positives caused by LLM hallucination, yielding a            1     Flag M should always be 0.                                                          ✗
                                                                   2     Miss check Authentication Present (A) to handle optional Authentication Section.    ✗
low 5.6% false positive rate. This demonstrates PARVAL’s           3     Miss validation for Simple Password Authentication Section format.                  ✓
effectiveness in detecting real mismatches between parser          4
                                                                   5
                                                                         Miss validation for Keyed MD5 Authentication Section format.
                                                                         Miss validation for Meticulous Keyed MD5 Authentication Section format.
                                                                                                                                                             ✓
                                                                                                                                                             ✓
implementation and its protocol standard.                          6     Miss validation for Keyed SHA1 Authentication Section Format.                       ✓
                                                                   7     Miss validation for Meticulous Keyed SHA1 Authentication Section format.            ✓


                                                                        TABLE 7: The Detected RFC Document Issues
4.3. RQ2: Baseline Comparison
                                                                   No.     RFC Document Issues                                                              New
                                                                    1      Miss explicitly mention that Detect Mult should not be 0.                        ✓
Setup and Metrics. To assess PARVAL’s end-to-end ef-                2      Miss explicitly mention that Length should be at least 24.                       ✓
fectiveness in extracting format specification from source
code (including both parser isolation (Stage 1) and specifi-     4.5. RQ4: Estimation of Manual Effort
cation extraction (Stage 2)), we compare CodeSpec against
a manually constructed ground truth based on the full                We assess the manual effort involved in each stage of
BFD implementation, not just the isolated parsing module.        PARVAL. Stage 1 requires manually identifying the entry
Precision and recall are used to measure how well PARVAL         parsing function, which takes approximately 10 minutes.
captures field names, types, and constraints.                    Stages 2 and 3 are fully automated and require no human
Results. As shown in Table 4, PARVAL achieves 100% pre-          intervention. Stage 4, which involves comparing CodeSpec
cision and recall, confirming its accuracy and completeness      and DocSpec and analyzing inconsistencies, is currently
against the full implementation.                                 manual and takes about 20 minutes.
TABLE 4: Precision and Recall for Format Specification
Extraction from the Full BFD Implementation                      5. Discussion

          Metric             PARVAL    Precision    Recall           This work explores the potential of LLMs to validate
          Field Name           11          100.0%   100.0%
                                                                 network protocol parsers by extracting and comparing pro-
          Field Type           11          100.0%   100.0%       tocol format specifications from source code and natural
          Field Constraint      4          100.0%   100.0%       language documents. Rather than providing a fully verified
                                                                 or complete solution, PARVAL demonstrates how LLMs can
                                                                 assist in a domain traditionally dominated by static analysis
                                                                 and formal methods. While promising, PARVAL does not
4.4. RQ3: Root Cause of Identified Discrepancies                 provide formal soundness or completeness guarantees. Both
                                                                 CodeSpec and DocSpec are LLM-generated and may contain
                                                                 inaccuracies, requiring manual inspection to distinguish true
Setup and Metrics. To identify the root causes of true
                                                                 inconsistencies from extraction errors.
discrepancies, we manually analyze each true inconsistency
                                                                     Given these limitations, PARVAL is best viewed as a
and classify it as either an implementation bug or an RFC
                                                                 practical assistant that complements formal techniques. Its
issue such as unclear, inaccurate, or missing descriptions.
                                                                 effectiveness must be evaluated empirically. Although we
For implementation bugs, we check existing bug reports
                                                                 demonstrate its utility on BFD, broader validation across
to determine whether they are newly discovered. For RFC
                                                                 diverse protocols and implementations is needed to assess
issues, we carefully examine the RFC descriptions to assess
                                                                 generality and robustness. Future work includes extending
their root causes.
                                                                 support to parsers written in other programming languages,
 TABLE 5: Root Causes of Identified Inconsistencies              further automating the validation process, and integrating
                                                                 PARVAL into existing protocol testing frameworks.
  Discrepancy Type           Implementation Bug      RFC Issue
  Field Type Mismatch                 21                     0   6. Related Work
  Constraint Mismatch                 11                     2
  Total                               32                     2   6.1. Techniques for Protocol Parser Validation

Results. As shown in Table 5, 32 of 34 true inconsistencies      Model Checking. Model checking-based methods [7]–[9]
are implementation bugs, while two stem from RFC issues.         formally verifies protocol implementations against their
To avoid redundancy in reporting, we group inconsistencies       specifications. However, constructing formal models often
with the same root cause and identify seven unique bugs,         requires significant manual effort, limiting its applicability
five of which are newly detected by PARVAL, detailed in          to practical validation tasks.
Table 6. The two RFC-related issues are also previously          Conventional Fuzzing. Fuzzing is a widely used approach
undocumented and detailed in Table 7.                            for testing protocol implementations by generating test cases
and executing them to trigger unexpected behavior, particu-        standards. By leveraging LLMs, PARVAL offers a flexible,
larly crashes. Mutation-based fuzzing, such as AFLNET [10],        language-agnostic approach to protocol format lifting.
creates test inputs by mutating existing valid or semi-valid
inputs. While it requires little knowledge of the protocol
format, its effectiveness relies heavily on the quality of seed    6.3. Large Language Models for Coding Tasks
inputs and often struggles to reach deep execution paths when
parsing conditions are complex. In contrast, generation-based          Large Language Models (LLMs) have been widely used
fuzzing, like BooFuzz [25], generates inputs using predefined      for various coding tasks, such as code generation [28]–[31],
grammars, improving coverage but requiring additional              program testing [32]–[35], static bug detection [36]–[41], re-
effort to define these grammars. NetLifter [11] automates          verse engineering [42]–[44], and automated repair [45]–[47].
grammar construction through static analysis to extract path       These models leverage extensive code repositories, natural
conditions, but it still focuses only on low level bugs such as    language data, and domain-specific knowledge to tackle tasks
crashes. However, many protocol implementation bugs are            that once demanded substantial human expertise [31], [48]–
semantic bugs that do not cause crashes but violate protocol       [51]. However, LLM-based approaches also face challenges
specifications, which conventional fuzzing fails to detect.        such as hallucination [52], [53] and incapabilities in reasoning
Differential Analysis. Differential analysis identifies in-        about complex program behaviors [54], [55]. To overcome
consistencies by comparing multiple implementations of             these challenges, recent research has explored techniques
the same protocol. Static tools like ParDiff [12] extract          such as chain-of-thought prompting [56], retrieval-augmented
state machines from different protocol implementations to          generation [57], and the incorporation of symbolic reason-
detect deviations. Dynamic differential testing tools, like DPI-   ing [37]–[39], aiming to enhance both the reliability and
Fuzz [16] and Prognosis [26], generate test cases to execute       transparency of model outputs. PARVAL builds on these
across multiple implementations and compare their runtime          advancements by leveraging retrieval-augmented-LLMs for
behaviors. While these approaches can uncover semantic             protocol format extraction and using symbolic test case
bugs (i.e., silent violations of protocol rules), they rely on     generation for refinement, thereby reducing hallucinations
the availability of multiple independent implementations,          and enhancing correctness.
which is not always feasible. They also fail to detect bugs
shared across all implementations, limiting their effectiveness    7. Conclusion
in certain scenarios.
                                                                       This paper presents PARVAL, a multi-agent framework
6.2. Protocol Format Lifting
                                                                   that leverages LLMs to validate network protocol parsers
                                                                   against protocol standards. By extracting format specifica-
    Previous work has focused on extracting protocol formats
                                                                   tions from both source code and natural language docu-
from either source code or protocol standards to support
                                                                   mentation, PARVAL enables direct comparison to uncover
validation and testing.
                                                                   inconsistencies between implementations and standards. We
Format Extraction from Source Code. Tools like                     evaluate PARVAL on the BFD protocol and demonstrate its
Netlifter [11] and ParDiff [12] use static analysis to extract     effectiveness in identifying mismatches with high precision,
protocol formats from source code. These methods often             uncovering seven unique implementations bugs, five of which
struggle with loops, either relying on imprecise heuristics        were previously unknown. While PARVAL does not offer
for loop summarization, or bounded loop unrolling, leading         formal guarantees, it illustrates the practical utility of LLMs
to incomplete or inaccurate format extraction. Additionally,       in improving protocol correctness. Our results underscore
these tools are typically language-specific and require signif-    the potential of LLM-assisted validation as a complement
icant effort to support new languages. PARVAL overcomes            to traditional static analysis and formal methods, offering a
these limitations by leveraging LLMs for flexible, language-       more scalable approach to protocol verification.
agnostic format extraction. It summarizes loop behavior and
validates the extracted logic through test case execution.
Format Extraction from Protocol Standards. Recent                  Acknowledgment
works [15], [17], [27] highlight the potential of LLMs
for extracting format specifications from protocol standards.          We thank all the anonymous reviewers and our shepherd,
3DGen [17] and ParCleanse [15] apply LLMs to transform             Nathan Dautenhahn, for the insightful feedback and guidance.
unstructured protocol descriptions into structured formats. In     We are grateful to the Center for AI Safety for providing
contrast, ChatAFL [27] avoids feeding RFCs to the model            computational resources. This work was funded in part by the
and instead relies on pre-trained models like GPT-3.5, which       National Science Foundation (NSF) Awards SHF-1901242,
have been trained on RFCs and are able to answer format-           SHF-1910300, Proto-OKN 2333736, IIS-2416835, DARPA
related queries directly.                                          VSPELLS - HR001120S0058, and ONR N00014-23-1-2081.
    PARVAL combines both source code and document-                 Any opinions, findings and conclusions or recommendations
based format extraction, enabling cross-validation to identify     expressed in this material are those of the authors and do
inconsistencies between implementations and their protocol         not necessarily reflect the views of the sponsors.
References                                                                           [21] “3d: Dependent data descriptions for verified validation,” https:
                                                                                          //project-everest.github.io/everparse/3d.html.
[1]   “The transport layer security (tls) protocol,” https://datatracker.ietf.org/   [22] “Everparse,” https://project-everest.github.io/everparse/3d-lang.html.
      doc/html/rfc5246.
                                                                                     [23] F. community, “The frrouting protocol suite,” https://github.com/
[2]   “File transfer protocol (ftp),” https://datatracker.ietf.org/doc/html/              FRRouting/frr, 2024.
      rfc959.
[3]   “Internet protocol (ip),” https://datatracker.ietf.org/doc/html/rfc791.        [24] “Bidirectional forwarding detection (bfd),” https://datatracker.ietf.org/
                                                                                          doc/html/rfc5880.
[4]   Heartbleed, “The heartbleed bug,” https://heartbleed.com, 2020.
                                                                                     [25] J. Pereyda, “Boofuzz,” https://github.com/jtpereyda/boofuzz, 2023.
[5]   “Openssl,” https://www.openssl.org.
                                                                                     [26] T. Ferreira, H. Brewton, L. D’Antoni, and A. Silva, “Prognosis: closed-
[6]   “Cve-2021-41773,” https://cve.mitre.org/cgi-bin/cvename.cgi?name=
                                                                                          box analysis of network protocol implementations,” in Proceedings of
      CVE-2021-41773.
                                                                                          the 2021 ACM SIGCOMM 2021 Conference, 2021, pp. 762–774.
[7]   M. Musuvathi and D. R. Engler, “Model checking large network
      protocol implementations,” in NSDI. USENIX, 2004, pp. 155–168.                 [27] R. Meng, M. Mirchev, M. Böhme, and A. Roychoudhury, “Large
                                                                                          language model guided protocol fuzzing,” in Proceedings of the 31st
[8]   G. Díaz, F. Cuartero, V. V. Ruiz, and F. L. Pelayo, “Automatic                      Annual Network and Distributed System Security Symposium (NDSS),
      verification of the TLS handshake protocol,” in SAC. ACM, 2004,                     ser. NDSS ’24. The Internet Society, 2024.
      pp. 789–794.
                                                                                     [28] R. Li, L. B. Allal, Y. Zi, N. Muennighoff, D. Kocetkov, C. Mou,
[9]   S. Chaki, E. M. Clarke, A. Groce, S. Jha, and H. Veith, “Modular                    M. Marone, C. Akiki, J. Li, J. Chim et al., “Starcoder: may the source
      verification of software components in C,” in ICSE. IEEE Computer                   be with you!” arXiv preprint arXiv:2305.06161, 2023.
      Society, 2003, pp. 385–395.
[10] V.-T. Pham, M. Böhme, and A. Roychoudhury, “Aflnet: a greybox                   [29] Y. Ding, M. J. Min, G. Kaiser, and B. Ray, “Cycle: Learning to self-
     fuzzer for network protocols,” in 2020 IEEE 13th International                       refine the code generation,” Proceedings of the ACM on Programming
     Conference on Software Testing, Validation and Verification (ICST).                  Languages, vol. 8, no. OOPSLA1, pp. 392–418, 2024.
     IEEE, 2020, pp. 460–465.                                                        [30] J. Liu, S. Xie, J. Wang, Y. Wei, Y. Ding, and L. Zhang,
[11] Q. Shi, J. Shao, Y. Ye, M. Zheng, and X. Zhang, “Lifting network                     “Evaluating language models for efficient code generation,” in
     protocol implementation to precise format specification with security                First Conference on Language Modeling, 2024. [Online]. Available:
     applications,” in Proceedings of the 2023 ACM SIGSAC Conference                      https://openreview.net/forum?id=IBCBMeAhmC
     on Computer and Communications Security, ser. CCS ’23. ACM,
                                                                                     [31] Q. Zhu, D. Guo, Z. Shao, D. Yang, P. Wang, R. Xu, Y. Wu,
     2023, p. 1287–1301.
                                                                                          Y. Li, H. Gao, S. Ma et al., “Deepseek-coder-v2: Breaking the
[12] M. Zheng, Q. Shi, X. Liu, X. Xu, L. Yu, C. Liu, G. Wei, and                          barrier of closed-source models in code intelligence,” arXiv preprint
     X. Zhang, “Pardiff: Practical static differential analysis of network                arXiv:2406.11931, 2024.
     protocol parsers,” in Proc. ACM Program. Lang., ser. OOPSLA ’24.
     ACM, 2024, pp. 1208–1234.                                                       [32] Y. Deng, C. S. Xia, H. Peng, C. Yang, and L. Zhang, “Large language
                                                                                          models are zero-shot fuzzers: Fuzzing deep-learning libraries via
[13] C. Liu, S. Gong, and P. Fonseca, “Kit: Testing os-level                              large language models,” in Proceedings of the 32nd ACM SIGSOFT
     virtualization for functional interference bugs,” in Proceedings of                  international symposium on software testing and analysis, 2023, pp.
     the 28th ACM International Conference on Architectural Support                       423–435.
     for Programming Languages and Operating Systems, Volume 2,
     ser. ASPLOS 2023. New York, NY, USA: Association for                            [33] S. Kang, J. Yoon, and S. Yoo, “Large language models are few-
     Computing Machinery, 2023, p. 427–441. [Online]. Available:                          shot testers: Exploring llm-based general bug reproduction,” in 2023
     https://doi.org/10.1145/3575693.3575731                                              IEEE/ACM 45th International Conference on Software Engineering
                                                                                          (ICSE). IEEE, 2023, pp. 2312–2323.
[14] M. Zheng, J. Yang, M. Wen, H. Zhu, Y. Liu, and H. Jin, “Why do de-
     velopers remove lambda expressions in java?” in 2021 36th IEEE/ACM              [34] C. Yang, Y. Deng, R. Lu, J. Yao, J. Liu, R. Jabbarvand, and L. Zhang,
     International Conference on Automated Software Engineering (ASE),                    “Whitefox: White-box compiler fuzzing empowered by large language
     2021, pp. 67–78.                                                                     models,” arXiv preprint arXiv:2310.15991, 2023.
[15] M. Zheng, D. Xie, Q. Shi, C. Wang, and X. Zhang, “Validating                    [35] G. Ryan, S. Jain, M. Shang, S. Wang, X. Ma, M. K. Ramanathan,
     network protocol parsers with traceable rfc document interpretation,”                and B. Ray, “Code-aware prompting: A study of coverage-guided test
     in Proceedings of the 34th ACM SIGSOFT International Symposium                       generation in regression setting using llm,” vol. 1, no. FSE, Jul. 2024.
     on Software Testing and Analysis, ser. ISSTA 2025.                                   [Online]. Available: https://doi.org/10.1145/3643769
[16] G. S. Reen and C. Rossow, “Dpifuzz: a differential fuzzing framework
     to detect dpi elusion strategies for quic,” in Proceedings of the 36th          [36] B. Steenhoek, M. M. Rahman, R. Jiles, and W. Le, “An empirical
     Annual Computer Security Applications Conference, ser. ACSAC ’20.                    study of deep learning models for vulnerability detection,” in 2023
     ACM, 2020, pp. 332–344.                                                              IEEE/ACM 45th International Conference on Software Engineering
                                                                                          (ICSE), 2023, pp. 2237–2248.
[17] S. Fakhoury, M. Kuppe, S. K. Lahiri, T. Ramananandro, and N. Swamy,
     “3dgen: Ai-assisted generation of provably correct binary format                [37] H. Li, Y. Hao, Y. Zhai, and Z. Qian, “Enhancing static analysis for
     parsers,” arXiv preprint arXiv:2404.10362, 2024.                                     practical bug detection: An llm-integrated approach,” Proceedings
                                                                                          of the ACM on Programming Languages, vol. 8, no. OOPSLA1, pp.
[18] “Tree-sitter,” https://tree-sitter.github.io/tree-sitter/.                           474–499, 2024.
[19] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang,
                                                                                     [38] C. Wang, W. Zhang, Z. Su, X. Xu, and X. Zhang, “Sanitizing
     X. Zhang, S. Zhang, J. Liu, A. H. Awadallah, R. W. White,
                                                                                          large language models in bug detection with data-flow,” in
     D. Burger, and C. Wang, “Autogen: Enabling next-gen LLM
                                                                                          Findings of the Association for Computational Linguistics: EMNLP
     applications via multi-agent conversation,” in ICLR 2024 Workshop
                                                                                          2024, Miami, Florida, USA, November 12-16, 2024, Y. Al-
     on Large Language Model (LLM) Agents, 2024. [Online]. Available:
                                                                                          Onaizan, M. Bansal, and Y. Chen, Eds. Association for
     https://openreview.net/forum?id=uAjxFFing2
                                                                                          Computational Linguistics, 2024, pp. 3790–3805. [Online]. Available:
[20] “Claude 3.5 sonnet,” https://www.anthropic.com/claude/sonnet.                        https://aclanthology.org/2024.findings-emnlp.217
[39] C. Wang, W. Zhang, Z. Su, X. Xu, X. Xie, and X. Zhang,                     [55] C. Liu, S. D. Zhang, A. R. Ibrahimzada, and R. Jabbarvand, “Code-
     “LLMDFA: analyzing dataflow in code with large language                         mind: A framework to challenge large language models for code
     models,” in Advances in Neural Information Processing Systems                   reasoning,” arXiv preprint arXiv:2402.09664, 2024.
     38: Annual Conference on Neural Information Processing Systems
                                                                                [56] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V.
     2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 -
                                                                                     Le, D. Zhou et al., “Chain-of-thought prompting elicits reasoning in
     15, 2024, A. Globersons, L. Mackey, D. Belgrave, A. Fan,
                                                                                     large language models,” Advances in neural information processing
     U. Paquet, J. M. Tomczak, and C. Zhang, Eds., 2024.
                                                                                     systems, vol. 35, pp. 24 824–24 837, 2022.
     [Online]. Available: http://papers.nips.cc/paper_files/paper/2024/hash/
     ed9dcde1eb9c597f68c1d375bbecf3fc-Abstract-Conference.html                  [57] M. Minor and E. Kaucher, “Retrieval augmented generation with llms
                                                                                     for explaining business process models,” in International Conference
[40] J. Guo, C. Wang, X. Xu, Z. Su, and X. Zhang, “Repoaudit: An
                                                                                     on Case-Based Reasoning. Springer, 2024, pp. 175–190.
     autonomous llm-agent for repository-level code auditing,” arXiv
     preprint arXiv:2501.18160, 2025.
[41] Z. Li, S. Dutta, and M. Naik, “Llm-assisted static analysis for
     detecting security vulnerabilities,” CoRR, vol. abs/2405.17238, 2024.
     [Online]. Available: https://doi.org/10.48550/arXiv.2405.17238
[42] D. Xie, Z. Zhang, N. Jiang, X. Xu, L. Tan, and X. Zhang, “Resym:
     Harnessing llms to recover variable and data structure symbols from
     stripped binaries,” in Proceedings of the 2024 on ACM SIGSAC
     Conference on Computer and Communications Security, 2024, pp.
     4554–4568.
[43] X. Xu, Z. Zhang, Z. Su, Z. Huang, S. Feng, Y. Ye, N. Jiang, D. Xie,
     S. Cheng, L. Tan et al., “Leveraging generative models to recover
     variable names from stripped binary,” arXiv preprint arXiv:2306.02546,
     2023.
[44] H. Tan, Q. Luo, J. Li, and Y. Zhang, “Llm4decompile: Decom-
     piling binary code with large language models,” arXiv preprint
     arXiv:2403.05286, 2024.
[45] N. Jiang, K. Liu, T. Lutellier, and L. Tan, “Impact of code language
     models on automated program repair,” in 2023 IEEE/ACM 45th
     International Conference on Software Engineering (ICSE). IEEE,
     2023, pp. 1430–1442.
[46] Y. Zhang, H. Ruan, Z. Fan, and A. Roychoudhury, “Autocoderover:
     Autonomous program improvement,” in Proceedings of the 33rd ACM
     SIGSOFT International Symposium on Software Testing and Analysis,
     2024, pp. 1592–1604.
[47] Y. Wu, N. Jiang, H. V. Pham, T. Lutellier, J. Davis, L. Tan,
     P. Babkin, and S. Shah, “How effective are neural networks
     for fixing security vulnerabilities,” in Proceedings of the 32nd
     ACM SIGSOFT International Symposium on Software Testing and
     Analysis, ser. ISSTA 2023. New York, NY, USA: Association for
     Computing Machinery, 2023, p. 1282–1294. [Online]. Available:
     https://doi.org/10.1145/3597926.3598135
[48] A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle, A. Letman,
     A. Mathur, A. Schelten, A. Yang, A. Fan et al., “The llama 3 herd of
     models,” arXiv preprint arXiv:2407.21783, 2024.
[49] A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng,
     C. Zhang, C. Ruan et al., “Deepseek-v3 technical report,” arXiv
     preprint arXiv:2412.19437, 2024.
[50] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal,
     A. Neelakantan, P. Shyam, G. Sastry, A. Askell et al., “Language mod-
     els are few-shot learners,” Advances in neural information processing
     systems, vol. 33, pp. 1877–1901, 2020.
[51] D. Xie, B. Yoo, N. Jiang, M. Kim, L. Tan, X. Zhang, and J. S. Lee,
     “Impact of large language models on generating software specifications,”
     arXiv preprint arXiv:2306.03324, 2023.
[52] S. Wang, Z. Li, H. Qian, C. Yang, Z. Wang, M. Shang, V. Kumar,
     S. Tan, B. Ray, P. Bhatia et al., “Recode: Robustness evaluation of
     code generation models,” arXiv preprint arXiv:2212.10264, 2022.
[53] F. Liu, Y. Liu, L. Shi, H. Huang, R. Wang, Z. Yang, L. Zhang, Z. Li,
     and Y. Ma, “Exploring and evaluating hallucinations in llm-powered
     code generation,” arXiv preprint arXiv:2404.00971, 2024.
[54] J. Chen, Z. Pan, X. Hu, Z. Li, G. Li, and X. Xia, “Reasoning runtime
     behavior of a program with llm: How far are we?” arXiv preprint
     cs.SE/2403.16437, 2024.
