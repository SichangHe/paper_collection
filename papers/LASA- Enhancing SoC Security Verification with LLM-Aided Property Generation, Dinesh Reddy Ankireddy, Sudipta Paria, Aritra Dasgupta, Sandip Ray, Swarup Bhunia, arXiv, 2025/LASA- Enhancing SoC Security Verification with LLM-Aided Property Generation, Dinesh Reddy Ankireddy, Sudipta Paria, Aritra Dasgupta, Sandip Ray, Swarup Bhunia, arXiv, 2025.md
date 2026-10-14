                                            LASA: Enhancing SoC Security Verification with
                                                  LLM-Aided Property Generation
                                                      Dinesh Reddy Ankireddy, Sudipta Paria, Aritra Dasgupta, Sandip Ray, and Swarup Bhunia
                                                    Department of Electrical and Computer Engineering, University of Florida, Gainesville, FL 32611, USA
                                                           {ankired.dineshre, sudiptaparia, aritradasgupta}@ufl.edu, {sandip, swarup}@ece.ufl.edu


                                            Abstract—Ensuring the security of modern System-on-Chip           derived from its specification by the verification experts. These
                                         (SoC) designs poses significant challenges due to increasing         assertions are used to statically prove properties using formal
                                         complexity and distributed assets across the intellectual property   verification tools or dynamically verified using simulation to
                                         (IP) blocks. Formal property verification (FPV) provides the
                                                                                                              identify potential vulnerabilities. Generating relevant security
arXiv:2506.17865v1 [cs.CR] 22 Jun 2025




                                         capability to model and validate design behaviors through secu-
                                         rity properties with model checkers; however, current practices      properties or assertions is a complex task involving substantial
                                         require significant manual efforts to create such properties,        expertise and manual efforts by security experts, making it
                                         making them time-consuming, costly, and error-prone. The             error-prone and not scalable for larger designs, highlighting
                                         emergence of Large Language Models (LLMs) has showcased              the need for automation to streamline the verification process.
                                         remarkable proficiency across diverse domains, including HDL
                                         code generation and verification tasks. Current LLM-based tech-         The rapid evolution of Large Language Models (LLMs)
                                         niques often produce vacuous assertions and lack efficient prompt    has extended their capabilities beyond natural language pro-
                                         generation, comprehensive verification, and bug detection. This      cessing, making a significant impact in the domain of hard-
                                         paper presents LASA, a novel framework that leverages LLMs
                                         and retrieval-augmented generation (RAG) to produce non-
                                                                                                              ware security and verification. LLMs have shown remarkable
                                         vacuous security properties and SystemVerilog Assertions (SVA)       proficiency in automating tasks like HDL code generation,
                                         from design specifications and related documentation for bus-        verification, and bug fixing [5]. Recent studies on LLM-
                                         based SoC designs. LASA integrates commercial EDA tool for           based generation of SystemVerilog Assertions (SVAs) [6]–[9],
                                         FPV to generate coverage metrics and iteratively refines prompts     security properties [10], [11] have demonstrated the growing
                                         through a feedback loop to enhance coverage. The effectiveness
                                         of LASA is validated through various open-source SoC designs,
                                                                                                              potential of LLMs in automating such verification tasks. LLM-
                                         demonstrating high coverage values with an average of ∼88%           based bug fixing [12], [13] aims to generate repairs for fixing
                                         denoting comprehensive verification through efficient generation     security vulnerabilities involving static analysis and security-
                                         of security properties and SVAs. LASA also demonstrates bug          related feedback or policy-based enforcement [14]. However,
                                         detection capabilities, identifying five unique bugs in the buggy    these techniques are limited by the complexity of RTL designs
                                         OpenTitan SoC from Hack@DAC’24 competition.
                                                                                                              and struggle to effectively incorporate diverse information
                                            Index Terms—SoC Security, Security Properties, SystemVer-
                                         ilog Assertion (SVA), Assertion Based Verification, Formal Prop-     sources, such as design specifications, threat models, and other
                                         erty Verification (FPV), Large Language Models (LLMs).               security requirements, and lack in curating efficient prompts.
                                                                                                              Moreover, existing techniques lack vacuity checking, often
                                                               I. I NTRODUCTION                               resulting in the generation of vacuous or non-meaningful
                                                                                                              properties that hinder effective verification. These techniques
                                            Modern bus-based SoCs integrate multiple intellectual prop-       also do not incorporate coverage analysis to assess the ef-
                                         erties (IPs) on a single chip and utilizes a common bus to           fectiveness of the generated properties, leaving ambiguity in
                                         facilitate communication between them. With the globalization        terms of verification completeness. In this paper, we introduce
                                         of the IC supply chain and adoption of a Zero Trust Model            a novel automated framework LASA (LLM-Aided Security
                                         it becomes crucial to identify and fix vulnerabilities and           Property Generation for Assertion-based SoC Verification) for
                                         protect secure assets in the regime of evolving security threats.    efficiently generating security properties for comprehensive
                                         Traditional verification methods including simulation, random-       SoC verification and identifying bugs. This paper makes the
                                         regression, directed-random testing [1], assertion-based for-        following major contributions:
                                         mal verification [2], fuzzing [3], and hybrid techniques [4]
                                         etc. struggle to keep pace with the growing complexity of              • We propose LASA, a novel and efficient framework that
                                         SoC designs, highlighting the need for greater automation                leverages the knowledge base of LLMs to automatically
                                         in vulnerability detection and remediation. Formal Property              generate security properties and SVAs, enabling compre-
                                         Verification (FPV) provides a rigorous methodology for math-             hensive verification of generic bus-based SoC designs.
                                         ematically verifying hardware design correctness using model-          • LASA integrates vacuity checking rules for identifying
                                         checking. However, the effectiveness of FPV depends on                   and discarding vacuous or non-meaningful properties to
                                         meticulously crafted security properties that accurately capture         enhance verification efficiency and reduce the computa-
                                         the intended behaviors and uncover potential vulnerabilities.            tional overhead.
                                         Assertion Based Verification (ABV) uses assertions that are            • LASA employs standard FPV tools to perform coverage
      analysis and incorporates an iterative refinement step        • Theorems for Vacuity Checking [16]
      when coverage falls below a threshold, ensuring improved      Theorem 1. (Efficient vacuity checking) For every formula
      and comprehensive verification.                               φ, a subformula ψ of φ, and a system M , the following are
   • Experimental results demonstrate the effectiveness of          equivalent:
      LASA evaluated on open-source SoC benchmarks, achiev-         (1) ψ does not affect φ in M .
      ing high coverage values that indicate substantial verifi-    (2) M satisfies φ[ψ ← true] iff M satisfies φ[ψ ← false].
      cation performance.                                           Theorem 2. (Polynomial time complexity) The problem of
   • LASA is equipped with bug detection capabilities, as           checking whether a system M satisfies a formula φ vacuously
      evidenced by the identification of five bugs in the buggy     can be solved in time O(CM (|φ|) · |φ|).
      OpenTitan benchmark from the HackDAC’24 competi-              Theorem 3. (Complexity of checking vacuity in CTL) For φ
      tion.                                                         in CTL,a subformula ψ of φ with multiple occurrences, and a
   The paper is organized as follows: Section II discusses the      system M , the problem of deciding whether ψ does not affect
relevant background and related works. Section III presents         φ in M is co-NP-complete.
major stages of the proposed framework. Section IV demon-           Theorem 4. (Linearly witnessable CTL formula) Given
strates the experimental results and discussion. Finally, Section   a CTL formula φ, deciding whether φ is linearly wit-
V concludes the paper.                                              nessable is in 2EXPTIME (Double Exponential Time
                                                                              p(n)
                                                                    or O(22 ), where p(n) denotes polynomial function of n)
                      II. BACKGROUND                                and is EXPTIME(Exponential Time)-hard.
A. Security Property and Formal Property Verification               Theorem 5. (Linearly counterable formula) For a branching
   Security property is a formal specification or rule describ-     temporal logic formula φ, we have that φ is linearly counter-
ing an observable behavior that the hardware design must            able iff ¬φ is linearly witnessable.
satisfy to guarantee confidentiality, integrity, and availability   Theorem 6. (Branching temporal logic) For a branching
(CIA) requirements [1], [15]. These properties must adhere          temporal logic formula φ and a system M , we have that
to three fundamental principles: Correctness, Consistency, and      M ⊭ Aφd iff M has a path π such that π ⊭ φ.
Completeness. Designers commonly use languages like PSL             Theorem 7. (Linearly Witnessable CTL⋆ formula) For a
and SVAs, employing logic representations at the temporal           CTL⋆ formula φ and a system M , deciding whether φ is
level like LTL and CTL, to describe design behaviors. FPV is        linearly witnessable in M is PSPACE-complete (polynomial
used to rigorously verify that security properties hold under       amount of memory).
all possible inputs. Commercial EDA tools employ model              Theorem 8. (Counterexamples to find interesting witnesses)
checkers to prove whether a property holds in all cases (safe)      For a formula φ and a system M , a counterexample for
or find a counterexample (violation). By exhaustively proving       ¬witness(φ) in M is an interesting witness for φ in M .
or refuting properties, FPV enables security flaws detection        Theorem 9. (Complexity of finding an interesting witness)
that might evade traditional testing.                               For an LTL or a CTL⋆ formula φ and a system M , an
                                                                    interesting witness for φ in M can be generated in polynomial
B. Vacuity Check Rules/Theorems for Security Properties             space. Deciding whether such a witness exists is PSPACE-
Definition: Vacuity in LTL refers to a situation where a            complete.
specification (formula) is satisfied in a system (model), but
not in a meaningful way as part of the formula was irrelevant       C. Coverage Metrics in FPV
in the system’s behavior. Vacuous properties usually indicate          Commercial tools performing FPV offer a range of coverage
weak, trivial, or incorrect specifications for a given system or    metrics to assess the thoroughness and completeness of FPV.
design.                                                             Cadence JasperGold employs three coverage metrics, namely,
Example:                                                            stimuli, checker, and formal coverage. Stimuli coverage
Let us assume the following formula/property in Model M :           indicates how well the input conditions and scenarios are
                        φ = G(p → F q)                       (1)    applied to the DUT during formal verification. It includes
This states “Always, if p holds, then eventually q holds.”          both code coverage (such as branch, statement, expression,
In model M , if p never occurs, then φ is vacuously true            and toggle coverage) and functional coverage (defined by
because the implication p → F q when p is false. Hence, we          user-specified covergroups). Checker Coverage assesses the
can conclude φ is vacuously satisfied in M with respect to p.       completeness of the formal assertions in verifying the design
Formal Definition: (from [16], [17])                                behavior. It includes Cone of Influence (COI) Coverage which
A system M satisfies a formula φ vacuously iff M |= φ               measures the extent to which the logic paths that influence
and there is some subformula ψ of φ such that ψ does not            a given assertion are exercised, and Proof Core Coverage
affect φ in M . For example, verifying a system with respect        identifies the minimal set of design elements necessary for
to the specification φ = AG(req → AF grant) (“every                 the assertion’s truth value and ensures that these elements are
request is eventually followed by a grant”), we say that φ is       thoroughly checked. Formal Coverage is a composite metric
satisfied vacuously in systems in which requests are never sent.    that combines both stimuli and checker coverage to provide an
                                                                    overall assessment of the formal verification’s effectiveness.
D. Existing Verification Techniques and Challenges                   evaluate the effectiveness of the generated properties or asser-
   The current industry practices predominantly employ two           tions, leaving gaps in verification completeness and increasing
major methodologies for SoC verification: (i) simulation-            the risk of undetected errors. These limitations highlight the
based verification and (ii) assertion-based verification [1],        need for a more efficient automated framework that overcomes
[18]. Simulation-based techniques rely on generating complex         shortcomings of current approaches and ensures comprehen-
testbenches that drive inputs and monitor outputs under various      sive verification of complex SoC designs.
scenarios. Tools such as ModelSim and Synopsys VCS are                                   III. M ETHODOLOGY
commonly employed to validate the functional correctness
                                                                        In this section, we describe the main components of the
of designs. Simulation-based approach is widely used for
                                                                     LASA framework, starting from prompt creation, followed by
its familiarity and ease of deployment, but it offers limited
                                                                     non-vacuous security properties generation and then conver-
coverage and struggles with scalability as design complexity
                                                                     sion to SVAs leveraging LLMs, along with coverage analysis
increases. ABV offers a more formal and rigorous frame-
                                                                     with iterative refinement and bug detection. The overall flow
work that employs SVAs specifying intended design behavior
                                                                     has been depicted in Fig. 1. The proposed framework can be
through properties and constraints and verified using FPV. It
                                                                     categorized into five major stages as described below.
provides exhaustive verification within bounded scopes and is
particularly effective in uncovering subtle logic errors/bugs,       A. Prompt Generation
or security vulnerabilities. However, it can be limited in              The prompt generation step includes the extraction of behav-
scalability due to the state-explosion problem.                      ioral descriptions from the given RTL code and specification
                                                                     documents, including block diagrams and textual descriptions.
E. Related work on Leveraging LLMs in Verification
                                                                     Current LLMs are constrained by the number of input tokens
   The growing use of LLMs is greatly advancing state-of-            they can process, making it difficult for them to effectively
the-art hardware security verification [5] by leveraging their       analyze large hardware designs that consist of thousands of
natural language understanding and broad knowledge base to           lines of RTL code. LASA breaks down the code into higher-
perform diverse automation tasks. Recent research explores           level abstractions (e.g., modules, functions, or components)
integrating LLMs into IC design flow to generate complex             and uses the summarized descriptions in the creation of
testbenches for simulation-based verification and creating pre-      prompts. Additionally, LASA employs Retrieval-Augmented
cise, context-specific SVAs for formal verification. LLM-aided       Generation (RAG) techniques to extract and summarize the
verification enables early detection of vulnerabilities prior to     relevant information from related documentation or manu-
fabrication. LLM-based SVA generation [6], [7], [22], [24]           als at a high level. By combining the summarized design
at the RTL abstraction level has been explored using natural         descriptions and retrieval-based information, LASA generates
language specifications and prompt engineering. Frameworks           more accurate, contextually aware prompts for generating the
like AssertLLM [9] employ specialized LLMs for different             relevant security properties in the subsequent steps.
stages of assertion creation, while hybrid methods [20] com-
bine LLM-driven formal verification with mutation testing to
refine design invariants. ChipNeMo [19] showcases versatile
LLM applications, including chat-based assistance, script gen-
eration, and bug summarization, emphasizing domain-specific
adaptation. DIVAS [14] provides an end-to-end toolflow that
automates CWE identification, SVA generation, and security
policy enforcement using [15], highlighting broad applica-
tions of LLMs. Additional frameworks such as FVEval [23],
LASP [11], and NSPG [10] assess and generate security
properties directly from RTL or design documentation. Table I
summarizes the characteristics of existing solutions and also
highlights the features of the proposed LASA framework.

F. Motivation
   Current techniques face significant challenges due to the
increasing complexity of SoC designs. They also lack the
capability to curate efficient prompts by extracting relevant           Fig. 1: Major stages in the proposed LASA framework.
information from the corresponding documentation or design
specifications. Current techniques follow more targeted verifi-
cation and also do not guarantee the generation of non-vacuous       B. Security Property Generation
properties that contribute to effective verification. Furthermore,     The proposed framework leverages pre-trained LLMs to
existing approaches do not incorporate coverage analysis to          generate relevant security properties for the SoC design under
                               TABLE I: Comparative analysis between LASA and existing LLM-based approaches.
       Proposed                                              SVA        Property/Policy    Vacuity      Prompt               Coverage       Bug                 Evaluation
                                    Baseline                                                                          RAG?
       Solutions                                          Generation?    Generation?      Checking?   Engineering?           Analysis?   Detection?            Benchmarks
    Kande et al. [7]                 Codex                    ✓               ✗               ✗            ✓           ✗        ✗            ✗          Hack@DAC21, OpenTitan
      NSPG [10]                      BERT                     ✗               ✓               ✗            ✓           ✗        ✗            ✗          OpenTitan, RISC-V, MIPS
    ChipNeMo [19]            LLaMA2 7B/13B/70B                ✗               ✗               ✗            ✗           ✓        ✗            ✗              Custom Benchmarks
    AssertLLM [9]               GPT-3.5, GPT-4                ✓               ✗               ✗            ✓           ✓        ✗            ✗              Custom Benchmarks
   Hassan et al. [20]                GPT-4                    ✓               ✗               ✗            ✗           ✗        ✗            ✗               C432 (ISCAS-85)
    Saha et al. [21]            GPT-3.5, GPT-4                ✓               ✗               ✗            ✗           ✗        ✗            ✗               CWE, Trust-Hub
 Orenes-Vera et al. [6]              GPT-4                    ✓               ✗               ✗            ✓           ✗        ✗            ✗             RISC-V CVA6 Ariane
      SPELL [8]             GPT-3.5, GPT-4, Gemini            ✓               ✓               ✗            ✓           ✗        ✗            ✗             MIT-CEP SoC, CWE
    LAAG RV [22]                     GPT-4                    ✓               ✗               ✗            ✓           ✗        ✗            ✗                   OpenTitan
     FVEVAL [23]          GPT-4o, Gemini-1.5, Llama-3.1       ✓               ✗               ✗            ✓           ✗        ✗            ✗              Custom Benchmarks
      LASP [11]                    Gemini-1.5                 ✓               ✓               ✗            ✓           ✗        ✗            ✗          RSA, DES, SHA512, AES
  LASA* (This work)       GPT4o, Llama-3.1, Gemini-1.5        ✓               ✓              ✓             ✓           ✓        ✓            ✓        CEP, OpenTitan, Hack@DAC’24


test. The security properties are typically expressed in temporal                             E. Iterative Refinement
logic and explore specific or entire state space of the design,                                  LASA employs iterative refinement that enhances the exist-
exploring possible states and transitions. The framework also                                 ing prompts to improve the coverage by generating additional
incorporates vacuous rules checking to improve property gen-                                  properties followed by SVAs until the pre-defined coverage
eration and discard trivial or non-interesting properties. We                                 threshold (%) is met. Failed SVAs indicate a potential is-
borrow the standard nine vacuous rules and theorems (de-                                      sue—either due to incorrect formulation by LLM or uncovered
scribed in Section II-B) from literature [16], [17] in evaluating                             design behavior that leads to potential bugs. The incorrect
the vacuous properties. Additionally, the framework integrates                                assertion generation by LLM necessitates prompt refinement
k-shot learning for generating valid security properties while                                through an iterative feedback path in LASA to enhance the
reducing hallucinations and irrelevant outputs from LLMs.                                     assertion generation process and ensure greater accuracy.
                                                                                              Additionally, LASA maintains additional prompts database
C. SVA Generation                                                                             and selectively applies relevant prompts aimed at generating
                                                                                              more accurate properties, thereby enhancing coverage and
   LASA integrates pre-trained LLMs for translating non-                                      improving overall verification completeness.
vacuous security properties into equivalent SVAs. The frame-
work employs re-prompting to correct syntax errors in gener-                                                         IV. R ESULTS AND D ISCUSSION
ated assertions and produce revised versions. LASA appends                                    A. Experimental set-up
each SVA into the respective .sva file and automates the
                                                                                                 We performed a comprehensive evaluation of our proposed
process of generating TCL scripts for evaluation using Ca-
                                                                                              LASA framework on two most popular open-source SoC
dence JasperGold. The evaluation employs FPV using model
                                                                                              benchmarks, namely, Common Evaluation Platform (CEP)
checkers to generate counterexamples (CEXs) to identify any
                                                                                              from MIT-LL1 and OpenTitan2 . The experiments were con-
failures that infer potential bugs or vulnerabilities. LASA uti-
                                                                                              ducted on a Red Hat Enterprise Linux Server with AMD
lizes k-shot learning by allowing the model to learn from
                                                                                              Epyc 7713 64-core processor and 1007.6 GiB Memory. FPV
a small set of example assertions to generate syntactically
                                                                                              has been performed using Cadence JasperGold (ver. 2020.12).
accurate and contextually relevant SVAs. This allows LASA to
                                                                                              Our analysis utilizes diverse pre-trained LLMs with their latest
adapt to diverse design specifications, producing high-quality
                                                                                              available versions such as OpenAI’s GPT4o, Google’s Gemini-
assertions that align with the security goals and underlying
                                                                                              1.5, and Meta’s Llama-3.1 for generating properties and SVAs.
threat model.
                                                                                              We evaluated the performance of different pre-trained LLMs
                                                                                              and found GPT4o outperforms other LLMs based on the per-
D. Coverage Analysis                                                                          centage of generated security properties classified as #proved
   Coverage analysis in FPV quantifies how effectively the                                    or #failed averaged on multiple IPs (refer to Fig. 2). Hence,
verification process exercises the design under test and the                                  we selected GPT-4o as our primary LLM for integration with
generated SVAs derived from formal security properties. It                                    LASA for automation tasks in different stages.
provides quantitative metrics that help evaluate the complete-                                B. Generation of Initial Prompts and RAG-based Extraction
ness, effectiveness, and quality of the properties/assertions.
                                                                                                LASA adopts JSON-based template (<SPEC_FILE>) as
LASA integrates multiple coverage metrics—Formal, Stimuli,
                                                                                              shown partially in Listing 1 that formalize the specifications.
and Checker Coverage—leveraging the Cadence JasperGold
                                                                                              For complex SoCs with multiple IPs involved, LASA processes
Coverage tool to analyze branch, statement, expression, and
                                                                                              each IP individually and uses the corresponding IP-level doc-
toggle coverage. LASA generates a comprehensive verification
                                                                                              umentation and <SPEC_FILE> to generate tailored prompts.
report summarizing assertion coverage and verification results.
                                                                                              For large hierarchical IPs, LASA identifies the submodules
If any signals remain uncovered, further analysis can be
performed by reviewing branch, statement, expression, toggle,                                    1 https://github.com/mit-ll/CEP.git

and functional coverage reports.                                                                 2 https://opentitan.org/book/hw/ip/index.html
                                                                  and semantically correct, and ‘#non-vacuous’ denotes the
                                                                  number of properties that pass vacuity check rules. Fig. 3 rep-
                                                                  resents the number of proved and failed properties generated
                                                                  for each submodule of AES and FIR designs from CEP.

                                                                  TABLE II: Number of generated non-vacuous properties and
                                                                  correct SVAs using LASA.
                                                                                            Properties                      Assertions
                                                                    Design
                                                                               #generated   #correct   #non-vacuous   #generated    #correct
Fig. 2: Comparing LLMs in terms of generating properties.          AES-192▲        73          43           41            41           40
                                                                    DES3▲          37          31           29            29           27
                                                                     GPS▲         108          98           93            93           90
based on design specifications and performs evaluation at            FIR▲          30          24           22            22           22
the submodule level. The initial prompt includes high-level          IIR▲          38          26           25            25           25
                                                                     i2c⋆          78          75           71            71           70
design specifications extracted from <SPEC_FILE>, either at        adc_ctrl⋆       37          33           32            32           32
the module or submodule level, augmented with contextual in-        kmac⋆          49          47           44            44           42
formation retrieved via RAG-based techniques. These enriched      ▲ denotes designs from CEP SoC.   ⋆ denotes designs from OpenTitan SoC.

prompts are fed sequentially to pre-trained LLMs to facilitate
the generation of relevant security properties while mitigating
the token limitations of LLMs. The example prompts are            D. Generation of Valid SVAs
included in Appendix A.                                              LASA leverages pre-trained LLMs to generate equivalent
"SoC_General":                                                    assertions for all non-vacuous properties that pass the vacu-
{                                                                 ity check. We found most of the properties were directly
    "NAME":"MIT-CEP",                                             translatable into SVAs (refer to Table II) while some posed
    "TYPE":"Open-source",
    "BUS":"AXI4",                                                 challenges for direct conversion due to the dependence on the
    "NO_OF_IP":"12",                                              formulation of properties. There were some manual efforts
    .... // more details                                          involved for those properties requiring re-prompting for con-
},
"BUS_INTERFACE":                                                  version to SVAs. LLMs often struggle with generating correct
{                                                                 SVAs due to limited understanding of hardware behavior,
    "INTERFACE_NAME":"Master/Slave",                              signal timing, and implication semantics (e.g., overlapping
    "NO_OF_PORTS":"17",
    .... // more details                                          vs. non-overlapping), etc. LLMs may generate SVAs that
}                                                                 are syntactically valid but semantically incorrect such as
"IP_1":                                                           using non-boolean expressions in implication, incorrect signal
{
    "NAME":"AES",                                                 scopes, or violating reset behavior constraints. LASA integrates
    "TYPE":"Slave",                                               verification through Cadence JasperGold and discards the
    "OPERATION":"Crypto",                                         syntactically incorrect or semantically invalid SVAs.
    .... // more details
}
.... // more IPs
"Assets":
{
    "NAME":"aes_key",
    "TYPE":"192-bit",
    .... // more details
}

Listing 1: CEP SoC Design Specifications in JSON format.

C. Generation of Security Properties and Vacuity Check
   LASA employs vacuity check on the LLM-generated prop-
erties to discard all non-vacuous properties that violate at
least one of nine theorems (Section II-B). LASA adopts a
hierarchical analysis approach, treating each submodule in-       Fig. 3: Number of ‘Proved’ and ‘Failed’ Properties Generated
dependently to generate localized security properties, which      by LASA for AES and FIR Sub-Modules.
are subsequently aggregated at the top module level to ensure
comprehensive coverage and consistency. Table II presents         Example of Vacuous Property/Assertion:
the number of security properties generated for different IPs     Listing 3 demonstrates an example property that violates
from CEP and OpenTitan benchmarks. The column ‘#correct’          one of the nine theorems of vacuity checking and will be
denotes the number of properties that are proven to be relevant   treated as a vacuous property, and the corresponding assertion
    would also be discarded. This property is potentially vacuous             TABLE III: Coverage values (%) for different IPs.
    since the antecedent validCounter > 1 is never true if                              Checker Coverage       Stimuli      Formal Coverage
                                                                         Benchmarks
    validCounter is stuck at 1 or 0.                                                    COI     Proof Core    Coverage     COI     Proof Core
                                                                          AES-192▲     99.02%     83.59%       99.93%     99.37%     85.05%
1 property p_validCounter_decrement;
2   @(posedge clk) disable iff (rst)                                       DES3▲       93.97%     91.70%        100%      93.98%     91.71%
3   (validCounter > 1) |=> (validCounter == $past(                          GPS▲       98.48%     83.39%       99.40%     98.63%     84.70%
      validCounter) - 1);                                                   FIR▲       92.64%     80.35%       92.82%     91.59%     80.50%
4 endproperty                                                               IIR▲       90.68%     81.07%       99.01%     90.97%     81.42%
5 assert property (p_validCounter_decrement);
                                                                            i2c⋆       91.44%     84.40%       99.25%     91.44%     84.40%
                                                                          adc_ctrl⋆    86.37%     80.53%       95.18%     86.12%     80.78%
         Listing 2: Example of Vacuous Property/Assertion.
                                                                           kmac⋆       89.35%     81.53%       96.79%     90.22%     82.19%
                                                                           Average       %          %             %         %          %
    Example of CEX:                                                     ▲ denotes designs from CEP SoC.   ⋆ denotes designs from OpenTitan SoC.
    Listing 3 illustrates a counterexample generated for an LLM-
    generated SVA for DES3 design. This condition violates the
    design behavior, and model checking in FPV can generate             generating relevant properties and SVAs. Fig. 5 illustrates the
    a counterexample for the same (refer to Fig. 4), making it          iterative improvement on coverage metrics across five different
    semantically incorrect.                                             designs from the CEP SoC benchmark. This iterative approach
                                                                        ensures that LASA enhances formal coverage, leading to more
1 property p_k_update;
2   @(posedge clk) disable iff (reset)                                  robust and comprehensive verification outcomes.
3   (!$stable(roundSel)) |=> (K !== $past(K));
4 endproperty
                                                                        prompt_database:
5 assert property (p_k_update);
                                                                          "Enhance coverage by adding reset conditions."
                                                                          "Add corner case assertions for boundary values."
            Listing 3: Example of CEX for DES3 design.                    "Include sequential behavior checks."
                                                                          "Cover unreachable states if any."
                                                                          "Extend assertions to multi-cycle paths."

                                                                             Listing 4: Example prompts for iterative refinement.

                                                                        G. Bug Detection
                                                                           LASA facilitates bug detection by generating context-aware
    Fig. 4: Timing diagram depicting the counterexample (CEX).
                                                                        SVAs that capture the security and functional properties of
                                                                        the design. For generating tailored SVAs for detecting bugs,
    E. Coverage Analysis                                                LASA includes additional high-level information into the
       LASA integrates Cadence JasperGold to perform FPV on             prompts, including micro-architectural events, threat models,
    the generated SVAs in the previous step and generate respec-        secure assets, etc. These improved prompts guide the language
    tive coverage metrics. LASA follows a configurable coverage         model to produce tailored SVAs that more accurately reflect
    threshold (set to 80% for our experiments), representing            the design’s security objectives. When verified, these SVAs can
    the minimum coverage required for the verification to be            expose violations that indicate design flaws. This capability
    considered acceptable. If coverage falls below this thresh-         is demonstrated through the detection of five bugs in the
    old, LASA incoprates a feedback loop to generate additional         buggy OpenTitan SoC from the Hack@DAC’24 competition
    relevant SVAs to improve the coverage. Higher coverage %            and tabulated in Table IV.
    indicates a more thorough and efficient verification, ensuring
    that all relevant states, behaviors, and properties of the design
    are fully explored and validated. LASA can also be seam-
    lessly integrated with other commercial EDA tool flows to
    perform FPV and generate respective coverage metrics. Table
    III presents the highest coverage values achieved for eight
    different IPs belonging to CEP and OpenTitan SoC. Coverage
    values at sub-module level are detailed in Appendix B.
    F. Iterative Refinement
       LASA includes a feedback path involving prompt engineer-
    ing to regenerate more non-vacuous properties and context-
    specific SVAs for further improvement of coverage metrics if
    it falls below the threshold. Listing 4 shows some example          Fig. 5: Improvement on coverage values for different IPs
    prompts providing additional semantic context that are in-          through iterative refinement in LASA.
    cluded with the existing prompts, refining the requirements and
                    TABLE IV: Detected bugs from HackDAC’24 buggy OpenTitan SoC using LASA framework.
 Bug#                Bug Description                        Code Reference                       Security impact                                     SVA for Detection
                                                                                                                                 property p_parity_err_without_enable;
         Incorrect parity checks for UART receiver.                                     It can lead to incorrect FIFO sync       @(posedge clk_i) disable iff (!rst_ni)
                                                              uart_rx.sv:
  1     The rx_parity_err in uart_rx does not depend                                   (prim_fifo_sync) and false hardware       (!parity_enable && rx_valid_q) |->!rx_parity_err;
                                                             Line: 102-103
                       on parity_enable                                                  interrupt (intr_hw_rx_parity_err).      endproperty
                                                                                                                                 assert property(p_parity_err_without_enable);
                                                                                                                                 property p_w1s_hw_clear_should_use_d;
                                                                                                                                 @(posedge clk_i) disable iff (!rst_ni)
         Incorrect wr_data is assigned. Assigned q         prim_subreg_arb.sv:            Incorrect assignment leads to          (SwAccess == SwAccessW1S && de && !we)
  2
            (reg value) instead of d (hw value)                 Line: 51                   non-clearance of hw value.            |->(wr_data === d);
                                                                                                                                 endproperty
                                                                                                                                 assert property(p_w1s_hw_clear_should_use_d);
                                                                                                                                 property p_otp_word_check;
                                                                                                                                 @(posedge clk_i) disable iff (!rst_ni)
                                                             otp_ctrl_lci.sv:        Overflow will cause system interruption
  3            Potential OTP word Overflow                                                                                       (LastLcOtpWord != LastLcOtpWordInt[CntWidth-1:0]);
                                                                Line: 67                   by generating wrong values.
                                                                                                                                 endproperty
                                                                                                                                 assert property(p_otp_word_check);
                                                                                                                                 property p_hmac_key_read_blocked;
                                                                                                                                 @(posedge clk_i)
            HMAC hashing key leaked through                  hmac_reg_top.sv:         Malicious attempt to leak the HMAC         disable iff (!rst_ni)
  4
                   reg_rdata_next                      Line: 1267-1273; 1343-1345;                hashing key.                   (addr_hit[8] || addr_hit[9]) |->reg_rdata_next == ’0;
                                                                                                                                 endproperty
                                                                                                                                 assert property(p_hmac_key_read_blocked);
                                                                                                                                 property p_error_s_known;
                                                                                                                                 @(posedge clk_i)
                                                                                     Since error_s is not used hence the error
                                                         prim_subreg_shadow.sv:                                                  disable iff (!rst_ni)
  5            Incorrect error detection logic                                        detection logic will not work correctly
                                                          Line: 76-66; 184-185;                                                  $isunknown(error_s) == 0;
                                                                                          leading to incorrect operation.
                                                                                                                                 endproperty
                                                                                                                                 assert property(p_error_s_known);




H. Discussion                                                                              vulnerabilities at the early stages of the design flow. Future
   While LASA demonstrates promising results, further en-                                  work includes incorporating domain-adapted LLMs with fine-
hancements are still possible. Incorporating more robust vacu-                             tuning to improve the performance and also extending to other
ity checking rules or refining existing ones could help filter out                         SoC interconnect fabrics, e.g., Network-on-Chip (NoC).
vacuous properties. LLMs struggle with complex, specialized
tasks and are constrained by a finite set of use cases in                                                                        R EFERENCES
generating SVAs, often leading to incomplete or erroneous
responses. Fine-tuning LLMs on domain-specific datasets can                                 [1] S. Bhunia and M. Tehranipoor, Hardware Security: A Hands-on Learn-
                                                                                                ing Approach, 1st ed. San Francisco, CA, USA: Morgan Kaufmann
significantly enhance their performance. Integrating syntax-                                    Publishers Inc., 2018.
checking tools helps minimize errors in generated responses                                 [2] H. Witharana, Y. Lyu, S. Charles, and P. Mishra, “A survey on assertion-
and significantly reduces manual efforts. Enhancing LLMs                                        based hardware verification,” ACM Comput. Surv., vol. 54, no. 11s, Sep.
                                                                                                2022.
with advanced reasoning capabilities and more sophisticated                                 [3] R. Saravanan, S. Paria, A. Dasgupta, V. N. Patnala, S. Bhunia, and
prompt engineering could improve the automation tasks. Addi-                                    S. M. P. D, “Synfuzz: Leveraging fuzzing of netlist to detect synthesis
tionally, adopting custom coverage metrics would offer a more                                   bugs,” 2025. [Online]. Available: https://arxiv.org/abs/2504.18812
                                                                                            [4] C. Chen, R. Kande, N. Nguyen, F. Andersen, A. Tyagi, A.-R. Sadeghi,
accurate representation of verification completeness, guiding                                   and J. Rajendran, “Hypfuzz: formal-assisted processor fuzzing,” in
iterative improvements effectively.                                                             Proceedings of the 32nd USENIX Conference on Security Symposium,
                                                                                                ser. SEC ’23. USA: USENIX Association, 2023.
                       V. C ONCLUSION                                                       [5] S. Paria, A. Dasgupta, and S. Bhunia, “Navigating soc security landscape
   In this paper, we presented LASA, a novel efficient frame-                                   on llm-guided paths,” in Proceedings of the Great Lakes Symposium on
                                                                                                VLSI 2024, ser. GLSVLSI ’24. New York, NY, USA: Association for
work for automating security verification for generic bus-                                      Computing Machinery, 2024, p. 252–257.
based SoCs. LASA incorporates RAG-based implementation                                      [6] M. Orenes-Vera, M. Martonosi, and D. Wentzlaff, “Using LLMs to
to extract relevant data from hardware documentation and                                        Facilitate Formal Verification of RTL,” 2023.
                                                                                            [7] R. Kande, H. Pearce, B. Tan, B. Dolan-Gavitt, S. Thakur, R. Karri, and
formalize SoC specifications for generating effective LLM                                       J. Rajendran, “(Security) Assertions by Large Language Models,” IEEE
prompts. By leveraging pre-trained LLMs and combining                                           Transactions on Information Forensics and Security, pp. 1–1, 2024.
vacuity checking and k-shot learning, LASA efficiently gen-                                 [8] S. Paria, A. Dasgupta, and S. Bhunia, “SPELL: An End-to-End Tool
                                                                                                Flow for LLM-Guided Secure SoC Design for Embedded Systems,”
erates contextually relevant non-vacuous security properties                                    IEEE Embedded Systems Letters, vol. 16, no. 4, pp. 365–368, 2024.
and then SVAs at both module and sub-module levels. The                                     [9] W. Fang, M. Li, M. Li, Z. Yan, S. Liu, H. Zhang, and Z. Xie, “As-
experimental results demonstrate higher coverage values (avg.                                   sertLLM: Generating and Evaluating Hardware Verification Assertions
88%) with iterative refinement, highlighting LASA’s effective-                                  from Design Specifications via Multi-LLMs,” 2024.
                                                                                           [10] X. Meng, A. Srivastava, A. Arunachalam, A. Ray, P. H. Silva, R. Psiakis,
ness in comprehensive verification. LASA also showcases bug                                     Y. Makris, and K. Basu, “Unlocking Hardware Security Assurance: The
detection capabilities, enabling the identification of potential                                Potential of LLMs,” 2023.
[11] A. Ayalasomayajula, R. Guo, J. Zhou, S. K. Saha, and F. Farahmandi,         Prompt 2 : Vacuity checking rules for k-shot learning
     “LASP: LLM Assisted Security Property Generation for SoC Verifica-
     tion,” in 2024 ACM/IEEE 6th Symposium on Machine Learning for CAD           – // 9 Rules <give in the text file> or direct in
     (MLCAD), 2024, pp. 1–7.
[12] H. Pearce, B. Tan, B. Ahmad, R. Karri, and B. Dolan-Gavitt, “Examining
                                                                                 prompt Here are the 9 vacuity checking rules you
     Zero-Shot Vulnerability Repair with Large Language Models,” in 2023         need to memorize. Utilize these 9 theorems to generate
     IEEE Symposium on Security and Privacy (SP), 2023, pp. 2339–2356.           valid and non-vacuous properties for the <module/sub-
[13] B. Ahmad, S. Thakur, B. Tan, R. Karri, and H. Pearce, “Fixing Hardware      module>.
     Security Bugs with Large Language Models,” 2023.
[14] S. Paria, A. Dasgupta, and S. Bhunia, “DIVAS: An LLM-based End-to-
     End Framework for SoC Security Analysis and Policy-based Protection,”       Prompt 3: Vacuity checking of generated properties
     2023.
[15] S. Paria, A. Dasgupta, and S. Bhunia, “DiSPEL: A Framework for SoC
     Security Policy Synthesis and Distributed Enforcement,” in 2024 IEEE
                                                                                 Can you evaluate and check if each property generated
     International Symposium on Hardware Oriented Security and Trust             is non-vacuous? A property must fail at least one
     (HOST), 2024, pp. 271–281.                                                  vacuity condition among the 9 theorems to be non-
[16] O. Kupferman and M. Y. Vardi, “Vacuity detection in temporal model          vacuous. Property is vacuous or non-vacuous using
     checking,” in Correct Hardware Design and Verification Methods,
     L. Pierre and T. Kropf, Eds.       Berlin, Heidelberg: Springer Berlin      the 9 vacuity rules provided, and respond as if Non-
     Heidelberg, 1999, pp. 82–98.                                                Vacuous True else False.
[17] I. Beer, S. Ben-David, C. Eisner, and Y. Rodeh, “Efficient detection of
     vacuity in actl formulas,” in Computer Aided Verification, O. Grumberg,
     Ed. Berlin, Heidelberg: Springer Berlin Heidelberg, 1997, pp. 279–290.      Prompt 4: Generating Counter Examples (CEXs)
[18] D. R. Ankireddy, S. Paria, A. Dasgupta, S. Ray, and S. Bhunia, “Clip:
     A structural approach to cut points matching for logic equivalence          Can you help analyze the Counter Examples (CEXs)
     checking,” in 2025 IEEE 43rd VLSI Test Symposium (VTS), 2025, pp.
     1–7.                                                                        report from formal verification runs. Please analyze
[19] M. Liu et al., “ChipNeMo: Domain-Adapted LLMs for Chip Design,”             and explain the failure in the given CEXs and generate
     2024.                                                                       or modify the corresponding Assertions.
[20] M. Hassan, S. Ahmadi-Pour, K. Qayyum, C. K. Jha, and R. Drechsler,
     “LLM-guided Formal Verification Coupled with Mutation Testing,”
     2024.                                                                       Prompt 5: Fixing SVA errors
[21] D. Saha, S. Tarek, K. Yahyaei, S. K. Saha, J. Zhou, M. Tehranipoor,
     and F. Farahmandi, “LLM for SoC Security: A Paradigm Shift,” 2023.
                                                                                 There is an error in the properties generated by you.
[22] K. Maddala, B. Mali, and C. Karfa, “Laag-rv: Llm assisted assertion
     generation for rtl design verification,” 2024. [Online]. Available:         Check for Syntax or Semantics errors and correct it
     https://arxiv.org/abs/2409.15281                                            accordingly. Here is the error [ERROR (error code:
[23] M. Kang, M. Liu, G. B. Hamad, S. Suhaib, and H. Ren,                        VERI-1137)] <.sva> syntax error near <>
     “FVEval: Understanding Language Model Capabilities in Formal
     Verification of Digital Hardware,” 2024. [Online]. Available:
     https://arxiv.org/abs/2410.23299
[24] S. Paria, A. Dasgupta, and S. Bhunia, “Towards automated verification
                                                                                 Prompt 6: Generating corrected SVAs through iterative
     of ip and cots: Leveraging llms in pre- and post-silicon stages,” in 2025   refinement
     IEEE 43rd VLSI Test Symposium (VTS), 2025, pp. 1–5.
                                                                                 Based on this coverage report <statement, toggle,
                                                                                 expression, branch> analysis, so the following cases
                                                                                 <?> are not covered, can you generate more property-
                                A PPENDIX                                        based system verilog assertions to cover all the cases.


A. Example Prompts                                                               Prompt 7: Design specs.

                                                                                 You need to generate Properties for the hardware
    Prompt 1 : Initial Prompt                                                    verification of some designs. Here is the Hardware
                                                                                 specification <SPEC FILE>. Based on this, you need
    You are an expert in Formal Verification and in                              to use the RAG model to prepare a module description
    generating SystemVerilog Assertions, specializing in                         at a high level such that I need to give the described
    writing comprehensive properties, including liveness,                        design specification to the LLM model to generate
    safety, and fairness constraints. You ensure thorough                        some properties-based assertions. For each signal, ex-
    coverage by checking for deadlock, livelock, and star-                       tract the following information: 1. Signal name 2. Port
    vation scenarios. To manage state space explosion,                           Declearation:-Output, Input 3. Description: Definition,
    you effectively apply constraints, symbolic tokens, and                      bit width, Signal type 4. Functionality 5. Any inter-
    assumptions. You also utilize auxiliary code and strive                      connects with other signals 6. Additional information
    to write efficient, modular properties in place of overly                    required for assertions 7. Microarchitecture design
    complex assertions instead for Hardware Designs.
B. Coverage Analysis at Sub-module level
   Coverage analysis at the sub-module level involves assess-
ing the checker, stimuli and formal coverage generated using
Cadence JasperGold integrated with LASA framework. This
approach enhances the overall verification efforts, allowing for
a more granular exploration of design behavior at sub-module
level and ensuring greater accuracy in identifying potential
issues. Additionally, this approach also enhances scalability
by enabling targeted testing of sub-modules, which can be
independently verified and then aggregated for comprehensive
verification of the overall design.
   Table V presents the coverage metrics at the sub-module
level for various IPs from the OpenTitan and CEP SoC
benchmarks. The results highlight high coverage values for
the generated properties using the LASA framework, demon-
strating the effectiveness of the proposed approach.



                                TABLE V: Coverage values for different IPs at sub-module level.
                                                                   Checker Coverage Settings                        Formal Coverage
              Benchmarks               Sub module                                              Stimuli Coverage
                                                                    COI       Proof Core                           COI     Proof Core
                                         AES_192_top               97.94%       81.25%             99.56%         97.52%     85.50%
                                     Expand_key_type_A             95.26%       81.23%              100%          98.16%     83.16%
                                     Expand_key_type_B              100%        81.35%              100%           100%      81.44%
               AES-192▲
                                     Expand_key_type_C              100%        81.20%              100%           100%      82.35%
                                     Expand_key_type_D              100%        96.25%              100%           100%      96.25%
                                           final_round              100%        80.23%              100%           100%      81.60%
                                             des3_top              99.82%       93.03%              100%          99.82%     93.03%
                DES3▲                           CRP                99.34%       99.34%              100%          99.34%     99.34%
                                             key_sel3              82.74%       82.72%              100%          82.78%     82.75%
                                              gps_top               100%        85.34%              100%           100%      83.67%
                                         AES_192_top               97.94%       81.25%             99.56%         97.52%     85.50%
                                     Expand_key_type_A             95.26%       81.23%              100%          98.16%     83.16%
                                     Expand_key_type_B              100%        81.35%              100%           100%      81.44%
                GPS▲                 Expand_key_type_C              100%        81.20%              100%           100%      82.35%
                                     Expand_key_type_D              100%        96.25%              100%           100%      96.25%
                                           final_round              100%        80.23%              100%           100%      81.60%
                                                pcode              94.62%       80.86%             97.01%         94.78%     82.54%
                                              cacode                100%        84.75%               99%          98.61%     84.75%
                                               fir_top             90.58%       87.56%               94%          90.60%     87.89%
                                      fir_filter_block_left        96.89%       83.56%             89.23%         95.54%     83.73%
                 FIR▲       fir_filter_block_left_multiply block   92.85%       71.65%             88.94%         90.23%     71.78%
                                     fir_filter_block_right        94.30%       86.70%             96.24%         94.35%     86.82%
                           fir_filter_block_right_multiply block   88.56%       72.29%             95.71%         87.25%     72.29%
                                               iir_top             91.78%       88.54%             98.65%         92.62%     89.34%
                                      iir_filter_block_left        94.65%       80.03%              100%          94.65%     80.03%
                 IIR▲       iir_filter_block_left_multiply block   89.02%       75.18%               99%          89.27%     75.58%
                                     iir_filter_block_right        87.89%       72.76%               98%          88.24%     73.32%
                           iir_filter_block_right_multiply block   90.05%       88.82%              100%          90.05%     88.82%
                                          bus_monitor              91.20%       81.40%             98.20%         91.20%     81.40%
                 i2c⋆                  controller module           92.65%       84.40%             99.54%         92.65%     84.40%
                                         target module             90.47%       87.40%              100%          90.47%     87.40%
                                          adc_ctrl_fsm             85.58%       79.63%             93.83%         85.02%     79.18%
               adc_ctrl⋆                  adc_ctrl_intr            90.02%       82.08%             94.86%         89.58%     82.72%
                                          adc_ctrl_core            83.52%       79.89%             96.84%         83.76%     80.45%
                                         keccak_round              90.52%       85.33%             99.56%         90.52%     85.50%
                                             sha3_top              86.57%       78.23%             95.42%         87.16%     79.45%
                kmac⋆
                                            kmac core              87.54%       81.35%             97.45%         89.43%     81.44%
                                         kmac_entropy              92.76%       81.20%             94.72%         93.76%     82.35%
                                   ▲ denotes designs from CEP SoC.        ⋆ denotes designs from OpenTitan SoC.
