                                        SpecAgent: Empowering Program Verification with Agentic
                                        Synthesis of Formal Program Specifications
                                        LEZHI MA, Nanjing University, China
                                        HAN WANG, Nanjing University, China
                                        SHANGQING LIU, Nanjing University, China
                                        JIAWAN WANG, Nanjing University, China
                                        LEI BU, Nanjing University, China
arXiv:2610.05132v1 [cs.SE] 4 Oct 2026




                                        Formal specifications are essential for deductive program verification, as they provide semantic abstractions
                                        that enable compositional verification on complex software systems. The difficulties in manually constructing
                                        such specifications gave birth to automated specification synthesis, and recent advances in relevant approaches
                                        based on large language models (LLMs) have shown promising capabilities. Nevertheless, existing approaches
                                        often follow a forward-only synthesis workflow and rely on localized repair strategies, which limit their
                                        effectiveness on real-world programs with complex dependencies among functions and loops. In such scenarios,
                                        verification failures may originate from previously generated specifications rather than the immediate failure
                                        locations, leading to cascading failures that cannot be effectively addressed by local refinement.
                                           In this paper, we present SpecAgent, an agentic framework for synthesizing high-quality ACSL specifications
                                        for real-world C programs. SpecAgent integrates four complementary components into a unified workflow: it
                                        analyzes program structures and dependencies to plan specification targets, leverages retrieval-augmented
                                        generation with a specification knowledge base to provide LLMs with relevant specification patterns and
                                        program context, employs agentic repairing to diagnose specification defects and revisit previously generated
                                        specifications when verification failures are traced to their dependencies, and applies an agentic critique
                                        mechanism to assess and refine semantic strength beyond proof success. We extensively evaluate SpecAgent
                                        on both specification synthesis and program verification tasks. On a benchmark consisting of 50 programs
                                        from 14 real-world repositories, SpecAgent with DeepSeek-V4 achieves 96.82% precision and 88.95% recall
                                        in synthesizing correct yet strong specifications, substantially outperforming all baselines including Codex
                                        equipped with GPT-5.6. We further evaluate SpecAgent on 811 real-world verification targets, where SpecAgent
                                        successfully discharges 604 targets, surpassing existing baselines. The results show that SpecAgent can
                                        effectively synthesize high-quality specifications and facilitate verification of real-world software.


                                        1   Introduction
                                        Program verification [25] is an essential technique for software reliability assurance, which can
                                        provide rigorous guarantees by proving consistency between the target program and given proper-
                                        ties (including functional correctness and runtime safety constraints), complementing conventional
                                        techniques such as software testing [27]. However, automatically verifying complex programs
                                        against high-level properties is fundamentally challenging, as the general program verification
                                        problem is undecidable [35] due to the potential unbounded behaviors produced by intricate pro-
                                        gram structures such as loops and function calls. One typical approach to achieving deductive
                                        verification is based on auxiliary specifications [20], which are expressed in parsable, unambiguous
                                        formal languages and can abstract the behaviors of individual program structures. Specifically,
                                        loop invariants summarize the properties preserved across loop iterations, while function contracts
                                        (typically including preconditions and postconditions) characterize the behavioral guarantees of
                                        function calls. These specifications provide the semantic abstractions needed by the verifier to

                                        Authors’ Contact Information: Lezhi Ma, Nanjing University, Nanjing, China, lezhima@hotmail.com; Han Wang, Nanjing
                                        University, Nanjing, China, wh66638@outlook.com; Shangqing Liu, Nanjing University, Nanjing, China, shangqingliu@nju.
                                        edu.cn; Jiawan Wang, Nanjing University, Nanjing, China, wjwnju@nju.edu.cn; Lei Bu, Nanjing University, Nanjing, China,
                                        bulei@nju.edu.cn.


                                                                                                         , Vol. 1, No. 1, Article . Publication date: October 2026.
2                                                            Lezhi Ma, Han Wang, Shangqing Liu, Jiawan Wang, and Lei Bu


construct local proof obligations and facilitate compositional proof construction, thereby enabling
the verification of high-level target properties of the overall program [20, 24].
   However, manually crafting formal program specifications remains labor-intensive and expertise-
demanding [46, 49], particularly for real-world software with complicated control flows and intricate
data dependencies. This challenge has motivated substantial research into automated specification
synthesis. Early approaches in this direction typically rely on heuristic rules [18, 19, 37] or machine
learning techniques [31, 45, 47]. Recently, large language models (LLMs) [22, 23, 32, 38, 39, 55] have
demonstrated promising capabilities in program comprehension and code summarization, bringing
new light on automated program specification synthesis. A series of LLM-based approaches [11,
33, 42, 53, 54] have been explored to generate function contracts and loop invariants, often in
conjunction with formal verification tools to validate and refine the generated specifications.
   Despite this progress, synthesizing high-quality specifications for complex real-world programs
remains challenging due to fundamental limitations of existing approaches. First, they typically
follow a forward-only workflow, in which a specification is considered finalized once successfully
generated and is not revisited in subsequent stages. Second, their repair process is predominantly
localized: when verification fails, they locate and repair errors solely based on the locations indicated
by the verifier, without considering specifications at other program points. These design choices
become problematic in complex real-world programs, where intricate dependencies widely exist
among program structures including loops and function calls, and consequently among the specifi-
cations that abstract their behaviors. Due to these dependencies, verification failure in downstream
specifications may stem from semantic correctness/strength issues in other upstream specifications
on which they depend. Such issues can propagate along dependency chains, triggering cascad-
ing verification failures. However, the forward-only workflow prevents existing approaches from
revisiting upstream specifications, while localized repair confines their efforts to the immediate
failure site. Consequently, they may repeatedly attempt ineffective local repairs without addressing
the root cause, compromising the correctness and strength of the synthesized specifications and
ultimately limiting their ability to support the verification of target properties.
   Addressing this limitation presents several challenges. First, specification synthesis must account
for dependencies induced by program structure. Real-world programs involve intricate relationships
among functions, loops, and data structures, making it difficult to identify the specification synthesis
order and the underlying specifications responsible for verification failures. Second, verification
feedback does not directly identify the root causes of specification defects. A failed proof may
result from an incorrect or insufficient specification, a runtime safety violation, or limitations of
the underlying verification process. Distinguishing these causes and determining the appropriate
scope of refinement require reasoning over both verification evidence and program context. Third,
proof success alone is insufficient to establish specification quality. Weak or vacuous specifications
may be readily verified while failing to capture meaningful program behavior or provide useful
guarantees to callers. Therefore, an effective synthesis approach must not only produce verifiable
specifications but also assess their semantic adequacy and refine them when necessary.
   These challenges call for a shift from localized specification generation and repair toward agentic
specification synthesis, where specifications are generated and refined through agentic dependency-
aware decision-making. Instead of treating generated specifications as immutable artifacts, such a
process can trace root causes across specification dependencies, revisit and improve defective spec-
ifications, and ensure that the resulting specifications provide meaningful behavioral abstractions
beyond merely passing verification. To realize this vision, we propose SpecAgent, an agentic frame-
work for synthesizing formal specifications in ACSL for real-world C programs. SpecAgent first
employs dependency-aware planning to identify specification targets and organize their synthesis
according to program structure and verification objectives. It then leverages agentic generation,

, Vol. 1, No. 1, Article . Publication date: October 2026.
SpecAgent : Empowering Program Verification with Agentic Synthesis of Formal Program Specifications                    3


augmented with relevant specification knowledge and program context, to construct auxiliary
specifications, which are subsequently checked by formal verification tools, guiding the system
in diagnosing failures and determining appropriate repair actions. Unlike workflows restricted
to localized repair, SpecAgent utilizes agentic repairing that can trace verification issues across
program dependencies and revisit previously generated specifications when they are identified
as potential root causes. In addition, a specification critique mechanism evaluates the semantic
strength of verified specifications, helping identify cases in which proof success does not translate
into sufficiently informative behavioral guarantees. By integrating these capabilities into a unified
workflow, SpecAgent aims to improve both the correctness and quality of specifications while
reducing the manual effort required for verifying real-world software.
   We evaluate SpecAgent through extensive experiments from two complementary perspectives:
quality of synthesized specifications and ability to support program verification. For the specifica-
tion synthesis task, we conduct experiments on a benchmark comprising 50 sizable programs from
14 real-world C repositories, where SpecAgent achieves 96.82% precision and 88.95% recall, sub-
stantially outperforming existing approaches (including Codex with gpt-5.6-sol) in generating
correct and sufficiently complete specifications. We further evaluate the ability of SpecAgent-
generated specifications to support real-world verification tasks on 811 verification targets from
two established benchmarks, covering both runtime-safety and reachability-oriented verification
tasks. SpecAgent successfully discharges 604 out of 811 verification targets, substantially surpassing
the best-performing existing baseline (yielding 523). These results provide empirical evidence that
the specifications synthesized by SpecAgent are not only semantically accurate but also practically
effective in facilitating the verification of high-level target properties.
   To conclude, the main contributions of this paper include:
• SpecAgent, an agentic framework integrating dependency-aware planning, retrieval-augmented
  specification generation, formal verification, and agentic repair and refinement to synthesize
  ACSL specifications for real-world C program verification tasks.
• An agentic specification repair and refinement workflow that leverages agentic decisions to
  diagnose specification defects (in terms of both semantic correctness and strength), enabling
  effective revisiting and refinement of previously generated specifications.
• Extensive experiments on 14 repositories and 811 real-world verification targets, comparing
  SpecAgent with 5 state-of-the-art baselines to investigate its effectiveness, component contribu-
  tions, and practical applicability.

2     Background and Motivation
2.1    Program Verification and Formal Specification Synthesis
Program verification [25] aims to establish whether a program satisfies desired properties, such as
functional correctness and runtime safety constraints, by formally proving the consistency between
program behaviors and given specifications. However, directly verifying high-level properties of
complex programs is challenging due to the unbounded behaviors introduced by intricate control-
flow structures, such as loops and function calls [35]. To enable effective verification, deductive
verification commonly relies on auxiliary specifications [20], which describe the behaviors of
individual program structures in precise and unambiguous formal languages. These specifications
serve as semantic abstractions that allow verifiers to encode program behaviors compositionally.
For example, function contracts summarize the assumptions and guarantees of function invocations,
while loop invariants characterize properties preserved across loop iterations. By providing such
abstractions, auxiliary specifications enable verifiers to construct local verification obligations and
combine them to establish the proof for high-level properties of the overall program.

                                                               , Vol. 1, No. 1, Article . Publication date: October 2026.
4                                                            Lezhi Ma, Han Wang, Shangqing Liu, Jiawan Wang, and Lei Bu


   In this work, we focus on the ANSI/ISO C Specification Language (ACSL) [7], a formal spec-
ification language for annotating C programs. ACSL provides various constructs for describing
program behaviors, among which function contracts and loop invariants are particularly important
for deductive verification. Specifically, requires statements define preconditions that must hold
before function execution, ensures statements specify postconditions guaranteed after execution,
and loop invariant statements describe properties maintained throughout loop iterations. These
annotations provide formal behavioral summaries of program structures, which can be leveraged by
verification frameworks such as Frama-C/WP [5] to generate verification conditions and discharge
them using automated theorem proving and SMT solving [4, 13, 14].
   Despite their importance, constructing effective auxiliary specifications remains challenging.
Writing formal specifications requires developers to not only understand the intended behaviors
of programs but also identify appropriate abstractions and express them in a rigorous formal
language [46]. For real-world software with entangled data dependencies and numerous interacting
components, manually designing sufficiently precise specifications can be labor-intensive and error-
prone. This has motivated extensive research on automated specification synthesis. Traditional
specification synthesis approaches range from rule-based techniques [18, 19, 37] to learning-
based methods [31, 45, 47]. More recently, the rapid development of Large Language Models
(LLMs) [3, 22, 23, 32, 38, 39] has brought new opportunities for program specification generation
by leveraging their strong capabilities in code understanding and summarization, giving rise to a
series of LLM-based approaches [33, 34, 53, 54].

2.2    Motivation
Real-world programs rarely consist of independent components. Functions interact through calls
and shared data, data structures are constrained by the operations that manipulate them, and loops
and their surrounding code jointly determine program states and invariants. Consequently, the
specifications of individual program components are often semantically interdependent: a specifi-
cation for one component often relies on preconditions, postconditions, invariants, or behavioral
properties established by another. Effective specification synthesis therefore needs to account for
such dependencies and propagate sufficient semantic information across them.
   Existing specification synthesis approaches, such as Preguss [53] and SpecSyn [34], have been
aware of the phenomenon and choose to generate specifications incrementally according to the
dependency relations among program components. Nevertheless, they largely follow a forward-only
process: once a specification has been generated and satisfies the verification checks available at that
stage, it is typically treated as finalized and will never be revisited. This creates a potential problem
when an upstream specification is locally acceptable but insufficiently strong for its downstream
dependents. For example, as illustrated in Figure 1, a weak but verifiable postcondition S1 (line 1)
may provide insufficient semantic information for synthesizing S2 (line 4), causing semantic validity
issues in the latter as well. The resulting deficiency can thus propagate along the specification
dependency chain and eventually manifest as verification failures of the target properties.
   Confronted with such downstream failures, existing approaches typically rely on localized repair,
i,e., modifying the specification at or around the observed failure location, since they are typically
forward-only and cannot revisit finalized specifications. However, the observed failure does not
necessarily indicate the actual location of the underlying defect. In the example above, repeatedly
repairing S2 cannot resolve a deficiency originating from the already-finalized S1. The synthesis
process may therefore become trapped in a failure loop: downstream failures trigger repeated local
repairs while the upstream root cause remains untouched, and the verification feedback obtained
at later stages cannot be utilized to revise earlier synthesis decisions.

, Vol. 1, No. 1, Article . Publication date: October 2026.
SpecAgent : Empowering Program Verification with Agentic Synthesis of Formal Program Specifications                                        5

                          Deficiency propagation issue due to specification interdependencies




                                                                                                                              Rejected
                                                                                                                             by verifier

      Potential deficiency in previously generated specifications       Downstream specifications fail to establish verification
                  Agentic Specification Synthesis                                    Existing Approaches
                                                                                                                             Unchanged




                                                         Successfully
                                                           verified!
                                                                                                                              Rejected
                                                                                                                             by verifier

      Locate actual deficiency and perform targeted refinement          Repeat the futile loop of superficial localized repairing

Fig. 1. Illustration of specification deficiency propagation. Since func2 invokes func1, its postcondition S2
also depends on the postcondition S1 of func1, and they are typically processed sequentially. Semantic
deficiencies in S1 will result in verification failures of S2, where existing approaches repeatedly perform
ineffective localized repairs on S2 due to their forward-only practice. In contrast, agentic synthesis can reason
about the root cause to effectively revisit and refine the responsible upstream specification S1.


   Motivated by these observations, we aim to propose an agentic specification synthesis paradigm,
where specification synthesis is treated as an iterative decision-making process rather than a strictly
forward, one-pass pipeline. Unlike conventional approaches that finalize a specification once its
processing is complete, an agent can continuously reason over the evolving set of specifications
and the verification feedback obtained from downstream components. When a downstream failure
suggests that an upstream specification may be insufficient, the agent can trace the specification
dependencies, revisit the previously generated specification, refine it, and propagate the resulting
changes to its dependents. In this sense, agentic synthesis naturally tackles the aforementioned
deficiency propagation problem by enabling the agent to reconsider its previous decisions in light
of newly acquired evidence and iteratively improve the specification set.

3     Methodology
Overview. SpecAgent consists of four successive stages, as illustrated in Fig. 2. Given a target C
program, the Planning Agent first identifies required specifications, their semantics, and depen-
dencies. The Generation Agent then constructs ACSL annotations with support from structurally
relevant examples retrieved from a dedicated knowledge base. Generated candidates are checked
by Frama-C/WP, and failed candidates are diagnosed and repaired by the Repairing Agent until
they pass verification. Verified specifications are further assessed by the Critique Agent, which
triggers refinement when insufficient properties are identified. Through collaboration among spe-
cialized agents, SpecAgent enables flexible specification synthesis by leveraging evolving contextual
information and external verification feedback.

3.1      Specification Synthesis Task Planning
Directly generating complete specifications requires an LLM to simultaneously identify relevant
program properties, determine their dependencies, and express them in ACSL. Such responsibilities
can become entangled for complex real-world programs, necessitating an explicit planning stage
that separates specification-level reasoning from specific annotation construction. To this end, the

                                                                           , Vol. 1, No. 1, Article . Publication date: October 2026.
6                                                              Lezhi Ma, Han Wang, Shangqing Liu, Jiawan Wang, and Lei Bu




    Input       Program       Planning    Generation   Candidate    Verification    Failure      Verified       Critique        Proof
    Code        Context        Agent        Agent        Specs         Gate         Report      Candidates       Agent




Verification      Syntax      Synthesis   Knowledge    Knowledge    Repairing      Analysis    Completeness       Final        Verifier
  Targets        Analysis       Plan       Retriever     Base         Agent         Tools         Probe       Specifications
                Synthesis Task Planning   Candidate Generation     Verification and Repairing Strength Critique/Refinement

                                Fig. 2. Overview of the proposed framework, SpecAgent.

planning Agent is designed to determine what should be specified and where to specify them before
concrete ACSL annotations are generated.
   Upon receiving the target C program, SpecAgent uses syntax analysis to summarize relevant
structural information into a deterministic program context, including function signatures, caller-
callee relations, and loop statement positions, before invoking the planning agent. Based on this
context and direct inspection of the source code, the planning agent identifies the functions and
loops that require specification instrumentation and determines the properties that should be
addressed, including functional contracts and runtime safety constraints, according to the target
code snippets and relevant caller/callee context. The output of the Planning Agent is a specification
synthesis plan in natural language. The plan describes the intended specification targets, their
designed semantics, interdependencies, and processing order. It therefore serves as an intermediate
reasoning artifact for subsequent processes.

3.2         Retrieval-Augmented Candidate Specification Generation
3.2.1 Candidate Specification Generation. After the planning stage, SpecAgent transforms the
specification synthesis plan into concrete ACSL specifications by employing the Generation Agent.
Given the target program and the current planning context, the Generation Agent constructs
specifications for relevant functions and loops, including preconditions (requires), postconditions
(ensures), frame conditions (assigns), loop invariants, and predicates when necessary. The gener-
ated annotations are intended to capture the behavioral and safety properties identified during the
planning stage. The Generation Agent can perform search-and-replace edits [21] to instrument can-
didate specifications into the target code, but is constrained by the framework to specification-level
modification: the agent is only allowed to add or modify ACSL annotations, without permission to
modify any code implementation itself, therefore preserving the implementation semantics of the
input program. The instrumented candidate specifications are then deterministically checked for
syntactic validity and conformance to ACSL standards by invoking the Frama-C tool.
3.2.2 Knowledge Base Construction and Knowledge Retrieval. To further improve the quality of the
generated candidates, SpecAgent additionally retrieves from a meticulously constructed knowledge
base a series of structurally similar code snippets with verifiable ACSL specifications instrumented,
which are presented to the Generation Agent in the prompts as reference examples.
Knowledge Collection. To obtain specification examples grounded in reliable ACSL usage, we
construct a dedicated knowledge base from the official ACSL tutorial [6]. We first collect the
annotated C code snippets distributed throughout the tutorial and organize them into function-
level knowledge units, yielding 184 units in total. Each unit consists of a C function together with
annotated specifications, preserving the original consistency between code and specification.
Structural Fingerprint of Knowledge Units. For each knowledge unit, we perform syntax
analysis and regex matching to extract the program’s structural features. The extracted information

, Vol. 1, No. 1, Article . Publication date: October 2026.
SpecAgent : Empowering Program Verification with Agentic Synthesis of Formal Program Specifications                    7




                  Fig. 3. Illustration for the 32-bit encoding of program structural features.

covers a wide spectrum of aspects, including parameter types, pointer and array usage, branch
and loop statements, memory accesses, function calls, return value types, and complex ACSL
constructs involved. These features provide a structural description of each example and are later
used to identify examples structurally compatible with the target code given. To enable efficient
structural matching during retrieval, we further encode the extracted features into a compact 32-bit
bitvector representation, referred to as the structural fingerprint. Figure 3 details the complete
encoding scheme. Each bit corresponds to an aforementioned structural feature and is set when the
corresponding property is present in the code snippet. The reserved bits are kept to 0 under our
settings. The bitwise fingerprint enables efficient computation of the structural overlap between a
target function and knowledge units.
Knowledge Retrieval Based on Structural Similarity. Given a target function, SpecAgent
retrieves annotated code snippets from the knowledge base according to their structural similarity
to the target. The retrieval process uses a two-stage filtering and ranking procedure, progressively
narrowing the candidate space from coarse structural compatibility to fine-grained similarity. This
design allows the retrieved examples to share critical program characteristics with the target while
avoiding unnecessary comparisons against structurally unrelated functions.
• SpecAgent first performs a coarse-grained structural filtering using indexed attributes in the
  knowledge base. Specifically, functions in candidate knowledge units are required to have com-
  patible loop structures and return types. Knowledge units that violate this criterion are excluded
  from subsequent computations.
• The remaining candidates are further ranked according to their Jaccard Similarity towards the
  target function. Denote the fingerprint of candidate function f as 𝐹 f , its Jaccard Similarity towards
  target function g is calculated by
                       𝑆 𝐽 (𝐹 f, 𝐹 g ) = popcount(𝐹 f & 𝐹 g )/popcount(𝐹 f | 𝐹 g )
                         Í31
  where popcount(𝐹 ) = 𝑖=0       𝐹 [𝑖] denotes the number of bits set to 1 in fingerprint 𝐹 . Eventually,
  up to three highest-ranked examples are selected to inject into the prompt.

3.3   Candidate Verification and Agentic Repairing
3.3.1 Verification Gate. Specification synthesis is not necessarily a one-shot process, since LLM-
generated specifications can be incomplete or incorrect, hindering their ability to support program
verification. In SpecAgent, each synthesized specification is subjected to a verification gate before
being committed to the final set of output specifications. The verification gate encapsulates Frama-
C/WP [5], the verifier for ACSL, able to determine whether the candidate is syntactically valid,
successfully parsed, and verifiable by the underlying verification tool. It also categorizes verification
goals and outcomes reported by Frama-C/WP, including successes, syntax errors, proof failures,
and timeouts, into a structured report in JSON representation, providing concrete evidence for
subsequent repair. In particular, for each failure reported by the verifier, the gate maps the failure
back to the source code, recovers the failure context including caller, callee, and exact source line,

                                                               , Vol. 1, No. 1, Article . Publication date: October 2026.
8                                                            Lezhi Ma, Han Wang, Shangqing Liu, Jiawan Wang, and Lei Bu


and reports them to the agent in detail. This turns opaque verifier-produced information into
provenance-aware repair evidence, alleviating the agent’s burden concerning error comprehension
and root-cause reasoning.

3.3.2 Repairing Agent. When verification fails, a Repairing Agent is invoked to diagnose and
repair the current set of candidate specifications. Given the source code and the verification
report produced by the verification gate, the agent reasons about the root cause of failure and
performs corresponding repair through search-and-replace edits. Typical repairs include rectifying
specifications with syntax errors or non-conformance to ACSL standards, correcting inconsistent
specification semantics with the target program, and strengthening the upstream specifications
with weak semantic validity. During diagnosis, the agent can also invoke Frama-C/WP and Frama-
C/Eva [10] to obtain additional verification and value-analysis evidence, facilitating the root-cause
reasoning process. After the repairing agent finishes its job, the modified candidate is submitted
to the Verification Gate again. This process iterates until the candidate passes the gate or the
invocation budget for the repairing agent runs out, ensuring that all committed specifications have
undergone a rigorous verification process to guarantee their correctness.

3.4    Specification Strength Critique and Refinement
3.4.1 Quality Gate and Critique Agent. Verification success only establishes the consistency be-
tween the program and specifications, without guarantee that the specification is sufficiently strong
or complete. SpecAgent therefore introduces a quality gate after successful verification to assess the
semantic strength of the verified specifications. Only the verified set of specifications is subjected to
this assessment, since strength is meaningful only for specifications that are correct and verifiable.
   The Quality Gate invokes a Critique Agent to perform the semantic assessment. Given the origi-
nal program, synthesis plan, set of verified specifications, and relevant editing history, the agent
identifies potentially weak or missing behavioral properties, including incomplete postconditions,
overly restrictive preconditions, and trivial contracts. Additionally, the agent can invoke a Postcon-
dition Completeness Probe (detailed in Section 3.4.2) to test whether the specification sufficiently
characterizes the output of a function. Based on these observations, the agent eventually produces
one of the following diagnosis results:
• ACCEPT: The semantic strength of current candidates is acceptable, and the framework can finish
  with these specifications as final output.
• IMPROVE: The specification exhibits localized strength deficiencies that do not involve interpro-
  cedural dependencies. The diagnosis report is thereby fed back to the Generation Agent for
  targeted regeneration.
• REPLAN: The specification exhibits structural deficiencies that involve interprocedural depen-
  dencies and may subsequently trigger cascading strength issues. Such issues are reported to the
  Planning Agent, which reinitiates the synthesis process anew from the planning stage.

3.4.2 Postcondition Completeness Probe. Relying solely on LLM-based reasoning to assess whether
a specification sufficiently constrains program behavior can lead to inconsistent judgments. To
support the Critique Agent in assessing specification strength, we introduce the Postcondition
Completeness Probe as a static analysis tool that provides stable evidence to facilitate the agent’s
judgment. The majority of existing approaches for specification completeness measurement are
conducted through input-output pair modification [36] or non-equivalent program mutation [17, 30],
which heavily rely on the availability of representative test suites or dedicated mutation operators.
Instead, we exploit a method based on the over-approximation feature of specifications [48].

, Vol. 1, No. 1, Article . Publication date: October 2026.
SpecAgent : Empowering Program Verification with Agentic Synthesis of Formal Program Specifications                      9


                            Table 1. Descriptions on all available tools in SpecAgent.
        Tool                                   Description                                    Applicable Agent(s)
        read            Read input code or documents produced by other agents                     All agents
        edit   Edit candidate specifications or the document to be produced by the agent          All agents
      retrieve Retrieve similar code and specification snippets from the knowledge base          Generation
        check   Check the specifications’ syntactical conformance to Frama-C standards       Generation, Repairing
          wp      Invoke Frama-C/WP for verification on the candidate specifications              Repairing
         eva     Invoke Frama-C/Eva for auxiliary value-analysis results as reference         Repairing, Critique
        probe                Invoke the Postcondition Completeness Probe                           Critique

   The strength of a postcondition can be understood from the set of behaviors that it permits. Given
a program 𝑓 with input space I, let B𝑓 = {(𝑖, 𝑜) | 𝑜 = 𝑓 (𝑖), 𝑖 ∈ I} denote its behavior set, where 𝑖
denotes the input program state and 𝑜 denotes the observable outcome, respectively. Given a set
of postconditions 𝑆, we similarly define its permitted behavior set as B𝑆 = {(𝑖, 𝑜) | 𝑆 (𝑖, 𝑜) = true},
i.e., input-output pairs that satisfy 𝑆. A correct postcondition must admit all behaviors of the
implementation, i.e., B𝑓 ⊆ B𝑆 . Since 𝑆 may permit behaviors that are not actually exhibited by 𝑓 ,
B𝑆 is an over-approximation of B𝑓 . A stronger postcondition constrains this over-approximation
more tightly by excluding behaviors that are not permitted by the specification. In the ideal case, 𝑆
precisely characterizes the function behavior (B𝑓 = B𝑆 ), yielding the strongest postconditions. In
this case, because a deterministic function 𝑓 maps each admissible input to a unique output, such a
postcondition also uniquely determines the output for every admissible input.
   The completeness probe checks this return-value determinacy directly through formal verifica-
tion. Given a verified contract for a target function 𝑓 , it constructs a temporary verification harness
that invokes 𝑓 twice with identical arguments, and asserts that the two return values are equal, i.e.:
                               𝑚 := 𝑓 (𝑥),        𝑛 := 𝑓 (𝑥),       assert 𝑚 = 𝑛.
The verifier will attempt to discharge the assertion using the target function’s contract. If the verifier
proves 𝑚 = 𝑛, the contract is strong enough to uniquely determine the return value for each input,
since the verifier cannot find another distinct output for the same input. Conversely, if both calls
satisfy the contract’s preconditions but the equality cannot be proved, the postcondition admits
insufficiently constrained return behavior, providing evidence of a weak return-value specification.
   Unlike prior works [17, 30, 36, 48, 59] that primarily stop upon a mere strength assessment result,
our probe is further integrated into the agent’s iterative synthesis process through counterexample-
guided refinement. When the aforementioned harness fails verification, the verifier-produced
counterexamples and failed proof obligations are retained as part of the probe result and exposed to
the Critique Agent. These artifacts provide concrete evidence about how the current specification
fails to constrain the program behavior, facilitating the agent’s root-cause reasoning (e.g., insufficient
preconditions or under-constrained return-value characterization). The Critique Agent can thereby
utilize this evidence to formulate a targeted refinement rather than merely receiving a binary
judgment result. In this way, the probe serves not only as a static assessment mechanism, but also
as a source of counterexample-guided evidence for specification refinement.

3.5    Agent Infrastructure
Agent Behavioral Paradigm. All agents in SpecAgent operate under the ReAct paradigm [58].
Specifically, each agent iteratively performs the thought-action-observation loop: in each iteration,
it reasons over the currently available information, selects an appropriate action (typically a tool
call), observes its outcome, and uses the obtained feedback to determine the next action. This
design allows the agents to adapt their behavior (e.g., decide where to instrument specifications and
what to specify) to intermediate status and results, rather than following a predefined sequential

                                                                 , Vol. 1, No. 1, Article . Publication date: October 2026.
10                                                           Lezhi Ma, Han Wang, Shangqing Liu, Jiawan Wang, and Lei Bu


procedure (which is the common practice of existing approaches [34, 53, 54]). The loop terminates
when the agent determines that the overall objective assigned to it has been satisfied.
Tool Settings. All agents interact with the outer environment through tool calling. We encapsulate
all necessary interactions into various tools, including file reading and writing, knowledge base
query, and verifier invocation. Agents with different roles have different sets of available tools, as
detailed in Table 1. The tools are invoked during the action step of ReAct loops through structured
queries, and the corresponding outcomes are fed back to the agent as the observation step.
Agent Orchestrator. The agents are coordinated by a centralized orchestrator rather than agent-
authored control flow to ensure the reliability of the overall framework. The orchestrator manages
the workflow progress and agent invocations through a deterministic state machine following the
logic shown in Fig. 2. Agents therefore operate within explicitly defined roles and responsibilities,
without the capability to directly interfere with the overall workflow. The orchestrator is also re-
sponsible for controlling the computational budget. Each agent invocation is subject to a predefined
maximum number of iterations 𝑁𝑠𝑡𝑒𝑝 , beyond which the invocation is forcibly terminated. Also,
the framework will be enforced to terminate and output current intermediate candidates as final
results after the total number of agent invocations reaches a predefined parameter 𝑁𝑖𝑛𝑣𝑜𝑘𝑒 .
Inter-agent Communication. SpecAgent sets explicit memory boundaries between agent invo-
cations, sharing no mutable runtime state or conversation history. Instead, agents communicate
exclusively through a shared workspace. Each agent invocation can access the workspace, including
current specifications, verification results, and documents produced by other agents, and can in
turn update relevant workspace contents that serve as inputs to subsequent agents. Consequently,
agent collaboration is achieved through successive operations on this shared intermediate context.

4     Experimental Setup
We aim to answer the following research questions (RQs) through experiments:

• RQ1: How is the general quality of the specifications generated by SpecAgent?
• RQ2: How does each main component of SpecAgent contributes to its performance?
• RQ3: How does SpecAgent-generated specifications evolve with increasing agent interactions?
• RQ4: Can SpecAgent-generated specifications facilitate real-world program verification tasks?

4.1    Implementation
We implement SpecAgent as a prototype tool in Python for convenient access to LLM interfaces and
agent development frameworks. Concerning the hyperparameters mentioned in Section 3.5, 𝑁𝑠𝑡𝑒𝑝
is set to 10 for Planning and Critique agents, while being 30 for Generation and Repairing agents;
the overall invocation limit 𝑁𝑖𝑛𝑣𝑜𝑘𝑒 is set to 10. Frama-C version 32.0 is adopted in the prototype
and metric calculation. In the experiments, SpecAgent and all other baselines are executed on an
Ubuntu 22.04 LTS server with an Intel® Core™ Ultra 9 275HX (2.70 GHz) 24-core processor and
16GB RAM.

4.2    Baselines
We adopt the following LLM-based approaches for ACSL specification synthesis as baselines:

• AutoSpec [54]: One of the first specification generation approaches based on LLMs.
• SpecGen [33]: An approach combining LLM conversation and mutation-based repairing.
• Preguss [53]: An approach targeting the verification of runtime error freeness properties.
• SpecSyn [34]: An approach utilizing program mutation to enhance specification strength.

, Vol. 1, No. 1, Article . Publication date: October 2026.
SpecAgent : Empowering Program Verification with Agentic Synthesis of Formal Program Specifications                   11


• Codex [40]: A general coding agent developed by OpenAI. In the experiments, Codex is assigned
  permission to read/write workspace files and invoke Frama-C, while being kept from web
  searching.
All baselines are backed up by two different underlying models: deepseek-v4-pro-0813 [55] and
gpt-5-2025-08-07 [39]. Codex is additionally equipped with gpt-5.6-sol [41]. All parameter
configurations remain the same with default settings, since the adopted models do not support
custom temperature settings. Note that Ma et al. [34] have evaluated the performance of these
baselines on GPT-5, and we directly adopt the corresponding statistics reported in their study.

4.3    Benchmark
RQ1&2&3. We adopt the benchmark collected by Ma et al. [34] to assess the general quality of
the specifications produced by baselines. The benchmark contains 50 programs collected from 14
real-world repositories, all paired with verifiable ground-truth specifications to facilitate strength
assessment. Programs in this benchmark yield 456.44 LoC on average, with 7 programs exceeding
1,000 LoC. Taking into consideration that the average program size in other ACSL datasets [1, 2, 11] is
typically below 50 LoC, the substantial difference in program scale makes the benchmark particularly
suitable for assessing the performance of baselines on real-world programs.
RQ4. Evaluation on program verification tasks necessitates explicit target properties serving as
verification goals. Following the settings of Ma et al. [34], we adopt two established datasets.
• Three real-world programs, collected from open-source repositories including Atomthreads [29],
   Contiki [43], and X509-parser [16]. These programs were originally collected by Wang et al. [53]
   to evaluate the performance of Preguss, with target properties concerning RTE-freeness instru-
   mented as ACSL assertions.
• The C category of the SV-COMP [8] benchmark. Specifically, we adopt the 213 programs in the
   reachability track summarized by Cao et al. [11], who translated the corresponding assertion
   targets into ACSL with other code semantics unchanged, yielding 269 targets in total.
All the aforementioned programs are directly retrieved from the artifact of Ma et al. [34].

4.4    Metrics
Following the settings of prior works [34, 59], we adopt two distinct metrics: precision and recall
to comprehensively evaluate different aspects of specification quality. Precision measures the
correctness of the generated specifications, calculated as the percentage of correct specifications over
all generated specifications. Recall assesses the strength of the generated specifications, measured by
the percentage of ground-truth specifications covered (i.e., there exists one generated specification
that is as strong as this ground-truth) over all ground-truth specifications. We inherit the script
utilized by Ma et al. [34] for metric calculation, which identifies equivalence between ground-
truth and generated specifications by constructing a conjunctive specification that connects the
two specifications with a bidirectional implication operator and verifying its correctness with
Frama-C/WP. Similar practices are widely adopted in existing works [48, 59].

5     Experimental Results
5.1    RQ1: General Quality of Generated Specifications
Table 2 demonstrates the quality (correctness measured by precision, strength measured by recall)
of specifications generated by all baselines.
Overall Quality. SpecAgent achieves consistently high precision while maintaining substantially
higher recall than existing approaches. Under DeepSeek-V4, SpecAgent attains an average precision
of 96.82% and recall of 88.95%, compared with 84.07%/61.61% for SpecSyn, 95.17%/74.47% for SpecGen,

                                                               , Vol. 1, No. 1, Article . Publication date: October 2026.
12                                                                                  Lezhi Ma, Han Wang, Shangqing Liu, Jiawan Wang, and Lei Bu


Table 2. Precision (Prec.) and recall (Rec.) of the specifications generated by each baseline, in percentages.
             Repository            X509     Java-JML    UAV     voronoi   hypatia    sokol     cgl      par     Maratis   Punity   ccan    clib     zpl     stb
                                                                                                                                                                    Avg.
       Average LoC per File          95       207       1741     348       1323       553      350      358      732       550     632     551     524      299
                           Prec.   97.04     99.20     89.14    100.00    100.00     96.88    100.00   100.00   80.37     100.00   97.89   97.82 97.13     100.00   96.82
                 DS-V4
                           Rec.    89.50     95.42     98.37     88.53     90.66     73.47     83.33    95.70   86.25     89.47    89.78   89.37 89.94     85.50    88.95
 SpecAgent
                           Prec.   100.00    100.00    76.95    97.26     100.00     99.30    100.00   100.00    81.39    100.00   99.25   96.73   97.69   96.88    96.10
                 GPT-5
                           Rec.     86.43     93.61    88.58    92.38     96.50      63.38    83.33    79.13     79.32    85.96    86.45   89.24   81.82   52.65    82.77
                           Prec.   83.81     91.10     99.59     96.28     87.54     60.68    100.00   90.01     60.58    100.00   79.17   76.10   58.78   93.40    84.07
                 DS-V4
                           Rec.    59.08     67.98     69.00     88.99     66.93     50.19    79.17    43.07     33.91    75.44    52.81   57.01   49.94   68.99    61.61
  SpecSyn
                           Prec.   95.66     97.80     97.57     99.39     97.24     93.42    100.00   98.18     99.13    98.77    99.24   90.94   86.88   99.31    96.68
                 GPT-5
                           Rec.    85.30     82.27     41.96     86.83     95.67     76.77    95.83    73.09     84.53    47.37    80.58   77.43   73.48   61.62    75.91
                           Prec.   83.33     81.96     100.00   100.00    100.00     100.00   100.00   100.00   100.00    100.00   90.35   98.61   74.36   83.34    93.71
                 DS-V4
                           Rec.    55.58     35.83      17.72   35.46      0.39       6.72    16.67    13.34     14.75    17.54    19.17   13.46   20.30   16.67    20.26
 AutoSpec
                           Prec.   33.33     84.72     100.00    80.00     95.24     81.25    42.86    85.40     16.67    90.00    66.67   79.39   81.67    0.00    66.94
                 GPT-5
                           Rec.    9.52      28.21     15.85     31.62     1.57      6.72     66.67    10.31     0.84     14.04    11.98   21.56   11.87    0.00    16.48
                           Prec.   100.00    99.35     65.64     94.79    100.00     97.37    100.00   100.00    84.62    100.00   99.60   94.77   98.68   97.62    95.17
                 DS-V4
                           Rec.    86.62     93.61     69.23     50.00     68.09     40.54    83.33    93.34     77.00    89.47    64.09   74.15   81.20   71.88    74.47
  SpecGen
                           Prec.   75.97     76.50     53.85    100.00     69.67     91.89    100.00   90.58     97.67    93.85    69.84   78.63   80.05   88.71    83.37
                 GPT-5
                           Rec.    43.46     68.20     15.38    77.12      51.97     81.80    100.00   79.73     58.06    68.42    44.19   50.45   61.24   43.19    60.23
                           Prec.   66.67     87.50     97.86    100.00    100.00     100.00   100.00   100.00    90.00    100.00   83.33   87.14   99.89   91.18    93.11
                 DS-V4
                           Rec.    22.93     29.76     60.14    34.42      15.18     12.50    16.67    17.12     27.26    24.56    32.84   28.87   46.28   26.61    28.22
     Preguss
                           Prec.   66.67     95.78     99.54    100.00     99.13     99.00    90.00    100.00    97.38    97.96    81.98   96.56   89.73   98.15    93.70
                 GPT-5
                           Rec.    10.27     29.15     35.43    36.11      53.15     13.85    33.33    21.17     32.76    24.56    36.42   38.68   36.44   28.69    30.72
                           Prec.   95.56     100.00    69.71     74.00    100.00     93.89    100.00   100.00    86.37    100.00   99.07   92.78   84.37   87.93    91.69
                 DS-V4
                           Rec.    76.87     89.35     87.18     92.38     80.93     61.16    83.33    92.26     81.29    82.46    94.20   85.76   85.31   61.38    82.42
     Codex                 Prec.   100.00    100.00    83.63     95.33    100.00     98.84    100.00   99.00     89.62    100.00   99.49   97.34   93.25   89.39    96.14
                 GPT-5.6
                           Rec.    90.65     94.00     85.78     91.53     90.66     62.47    79.17    71.93     81.85    84.21    82.69   87.70   83.58   67.23    82.39
                           Prec.   85.61     98.31     56.30     93.05     84.28     95.84    100.00   99.45     85.20    86.54    95.54   90.79   72.20   87.50    87.90
                 GPT-5
                           Rec.    58.16     92.90     25.41     85.60     67.70     64.70    83.33    69.78     72.35    73.68    73.68   86.59   54.72   44.07    68.05




and 93.71%/28.22% for Preguss. Notably, Codex with GPT-5.6-sol achieves 96.14% precision and
82.39% recall, still underperforming SpecAgent with DeepSeek-V4. The same trend holds for GPT-5:
SpecAgent achieves 96.10% precision and 82.77% recall, surpassing all baselines. These results
indicate that SpecAgent can generate specifications that are not only predominantly correct but
also substantially stronger than those produced by most existing approaches.
Trade-off between Correctness and Strength. The results further reveal a clear trade-off faced
by existing methods. AutoSpec and Preguss, for example, often achieve high precision on individual
repositories, but their recalls remain low, with average recall as low as 20.26% and 28.22% under
DeepSeek-V4, respectively. This suggests that their high precision is frequently accompanied
by limited specification coverage. In contrast, SpecAgent maintains precision above 96% while
reaching nearly 89% recall with DeepSeek-V4. This trend is even more clearly illustrated in Fig. 4.
Across all baselines, the majority of data points lie in the upper region of the grid, indicating that
existing approaches generally achieve high precision. However, the points of Preguss and AutoSpec
are predominantly concentrated toward the upper-left corner, whereas those of SpecAgent are
substantially more clustered around the upper-right corner, highlighting the pronounced gap in
recall across different approaches. This result is particularly notable because attempting to enhance
specification strength introduces additional risk of incorrect or unverifiable assertions. The ability
of SpecAgent to improve recall without a corresponding substantial loss in precision suggests that
its agentic synthesis process can exploit verification feedback to effectively enrich specification
semantics while preserving correctness.
Robustness across repositories. SpecAgent also demonstrates relatively stable performance
across projects with substantially different program sizes. The benchmark ranges from relatively
small programs such as those from X509-parser (95 LoC per file) to substantially larger ones such as
UAV (1,741 LoC) and hypatia (1,323 LoC). Despite this variation, SpecAgent maintains precision close
to or above 90% on most repositories and achieves high recall on both small and large programs. For
example, on UAV, the largest repository in the benchmark, SpecAgent obtains 89.14% precision and

, Vol. 1, No. 1, Article . Publication date: October 2026.
SpecAgent : Empowering Program Verification with Agentic Synthesis of Formal Program Specifications                   13




Fig. 4. Per-program specification quality of each baseline (using DeepSeek-V4) shown by scatter points. The
coordinates of each point represent the precision and recall achieved on one specific program.

98.37% recall with DeepSeek-V4, and 76.95% precision and 88.58% recall with GPT-5. This suggests
that the approach is not limited to short or structurally simple programs and can retain substantial
specification strength as program complexity increases.
Effect of the Underlying LLM. Changing the underlying LLM affects the absolute performance
of all approaches, but does not alter the relative advantage of SpecAgent. Replacing DeepSeek-V4
with GPT-5 slightly decreases average recall of SpecAgent from 88.95% to 82.77%, while precision
remains comparably high (96.82% vs. 96.10%). In contrast, several baselines exhibit much larger
degradations in recall when switching models. e.g., SpecGen from 74.47% to 60.23%. It is noteworthy
that recall of Codex drops from 82.42% to 68.05% (-16.37%), whereas SpecAgent’s recall decreases
by only 6.18%, despite both Codex and SpecAgent adopting agentic workflows. This comparison
suggests that SpecAgent’s explicit verification-guided state transitions and iterative refinement
make specification synthesis less sensitive to the underlying LLM’s agentic capabilities.

 Answer to RQ1: SpecAgent consistently generates specifications with high correctness and
 strength across repositories, achieving an average precision of 96.82% and recall of 88.95% with
 DeepSeek-V4, and 96.10% and 82.77% with GPT-5. Compared with existing approaches, SpecAgent
 better balances specification correctness and strength, avoiding the weak specifications often
 produced by methods that prioritize precision. Moreover, SpecAgent exhibits relatively stable
 performance across different underlying LLMs, suggesting that its verification-guided agentic
 workflow reduces the dependence of specification quality on the underlying model.


5.2   RQ2: Ablation Study on Main Components
We construct 4 variants of SpecAgent by progressively augmenting a basic candidate generation
process (Section 3.2) with additional agentic components. Specifically, G-only represents the basic
generation process, followed by P+G that augments it with the Planning stage (Section 3.1), P+G+R
further with Verification and Agentic Repairing (Section 3.3), and finally the complete SpecAgent
configuration with Strength Critique and Refinement (Section 3.4).
   Table 3 reports the ablation results on DeepSeek-V4 and GPT-5. Overall, the results show that
the individual components provide complementary benefits, while their combination is essential
for achieving consistently strong performance. Using Generation alone (G only) already achieves
relatively high precision, with average precision of 89.78% and 88.66% for DeepSeek-V4 and GPT-5,
respectively, but its recall remains limited to 80.93% and 72.14%. Adding Planning (P+G) does not
yield a consistent improvement: although recall increases slightly for DeepSeek-V4 to 83.99%, it
slightly decreases for GPT-5 to 71.51%, suggesting that planning alone cannot reliably address
synthesis failures. In contrast, incorporating Repairing (P+G+R) substantially improves precision,
reaching 94.79% and 94.34% on average for DeepSeek-V4 and GPT-5, respectively, while also
recovering recall to 82.08% and 76.21%. Finally, the complete SpecAgent configuration achieves the
strongest overall performance, with average precision/recall of 96.82%/88.95% for DeepSeek-V4 and
96.10%/82.77% for GPT-5. Notably, the gain in recall over Generation-only is particularly pronounced

                                                               , Vol. 1, No. 1, Article . Publication date: October 2026.
14                                                                       Lezhi Ma, Han Wang, Shangqing Liu, Jiawan Wang, and Lei Bu


Table 3. Performance of all ablation variants of SpecAgent. All statistics are reported in percentages. P:
synthesis task Planning, G: candidate Generation, R: agentic Repairing, C: strength Critique and refinement.
Model   Variant   Metric   X509     Java-JML   UAV     voronoi hypatia   sokol    cgl      par     Maratis   Punity   ccan    clib     zpl     stb     Avg.
                  Prec.    95.24     91.25     66.55    64.70   86.40    98.15   100.00   98.99    91.67     92.68    99.48   74.80   97.06   100.00   89.78
        G only
                  Rec.     83.21     94.06     82.28    88.14   90.66    68.65    83.33   94.16    47.46     78.95    81.61   70.86   84.10   85.50    80.93
                  Prec.    94.67     90.38     66.18   66.60    90.47    97.29   96.76    95.40     86.37    95.78    96.25   99.04   91.83   95.65    90.19
         P+G
DS-V4             Rec.     86.43     95.92     79.72   91.53    90.66    52.14   83.33    98.98     86.25    89.47    81.25   82.47   88.94   68.83    83.99
                  Prec.    100.00    100.00    73.97    94.16   100.00   95.00   100.00   100.00    83.85    100.00   99.59   87.30   93.18   100.00   94.79
        P+G+R
                  Rec.      84.10     84.33    88.67    77.24   87.93    64.25   77.50    89.41     87.33    83.21    85.42   80.13   80.04   79.52    82.08
                  Prec.    97.04     99.20     89.14   100.00   100.00   96.88   100.00   100.00   80.37     100.00   97.89   97.82 97.13 100.00       96.82
         Full
                  Rec.     89.50     95.42     98.37    88.53   90.66    73.47   83.33     95.70   86.25     89.47    89.78   89.37 89.94 85.50        88.95
                  Prec.    91.67     97.53     72.46    70.33   86.44    86.26   100.00   96.07    81.49     98.48    93.82   95.54   88.41   82.69    88.66
        G only
                  Rec.     64.03     86.82     71.33    88.14   67.70    56.80    83.33   74.04    71.51     78.95    69.74   74.13   80.48   43.03    72.14
                  Prec.    89.93     98.69     73.98    60.45   61.26    89.91   100.00   100.00    87.73    94.59    94.17   97.09   90.91   86.45    87.51
         P+G
GPT-5             Rec.     63.65     87.88     51.98    88.14   59.14    58.52    83.33   73.56     72.23    82.46    66.44   81.22   77.11   55.53    71.51
                  Prec.    100.00    100.00    68.82    71.67   100.00   96.38   100.00   100.00    85.50    100.00   100.00 99.76 98.69 100.00        94.34
        P+G+R
                  Rec.      75.94     88.86    82.28    85.14   87.94    56.80    83.33    71.70    75.76     80.70    69.22 80.69 69.19 59.38         76.21
                  Prec.    100.00    100.00    76.95   97.26    100.00   99.30 100.00     100.00   81.39     100.00   99.25   96.73 97.69     96.88    96.10
         Full
                  Rec.      86.43     93.61    88.58   92.38    96.50    63.38 83.33       79.13   79.32      85.96   86.45   89.24 81.82     52.65    82.77


for SpecAgent, reaching +8.02% and +10.63% for DeepSeek-V4 and GPT-5, respectively. These results
indicate that the key advantage of SpecAgent does not stem from any single component, but from
their interaction: Planning provides dependency-aware guidance, Repairing resolves invalid or
unverifiable specifications, and the complete workflow enables these decisions to be iteratively
informed by verification feedback.

  Answer to RQ2: The ablation study shows that the components of SpecAgent provide com-
  plementary benefits, with performance improving as the synthesis process is progressively
  augmented with planning, repairing, and critique. In particular, repairing substantially improves
  precision, while the complete workflow further improves recall by leveraging the feedback
  from strength Critique. Overall, the results demonstrate the importance of integrating these
  components into an agentic synthesis process rather than relying on a single agent.


5.3 RQ3: Specification Quality Evolution over Agent Invocations
To investigate how specification quality evolves as agent interactions accumulate, we analyze all
specification evolution trajectories at increasing numbers of agent invocations. Specifically, we
vary the number of agent invocations from 2 to 10 (1 excluded since the generation stage has not
yet begun) and track four metrics at each invocation count: the fraction of trajectories that have
passed the verification gate, the average number of generated specifications, precision, and recall.
The first metric captures how quickly trajectories reach a verification-accepted state, while the
latter three characterize the quantity and quality of the resulting specifications. This analysis allows
us to examine how additional agent interactions contribute to specification synthesis and whether
their benefits diminish as the invocation count increases.
   Fig. 5 demonstrates the trend of candidate specification quality evolution as the number of agent
invocations increases. As the number of agent invocations increases, candidate specification quality
generally improves, but the gains gradually diminish. The most substantial improvement occurs in
the early invocations: from 2 to 6 invocations, the mean precision increases from 93.11% to 96.32%,
while the mean recall rises from 87.22% to 90.01%. Meanwhile, the average number of generated
specifications increases from 79.79 to 90.70, indicating that additional agent interactions progres-
sively expand the set of candidate specifications while maintaining or improving their quality.
Most notably, the fraction of trajectories passing the verification gate also increases from 36% at 2
invocations to 62% at 6 invocations, suggesting that 2–6 is the golden interval where the majority

, Vol. 1, No. 1, Article . Publication date: October 2026.
SpecAgent : Empowering Program Verification with Agentic Synthesis of Formal Program Specifications                   15




 Fig. 5. Evolution of SpecAgent-generated specification quality as agent invocations increase from 2 to 10.

of trajectories reach verifiable states. Beyond 6–8 invocations, however, the improvements become
marginal: precision remains around 97%, recall fluctuates around 90%, and the verification-gate
pass rate oscillates between 60% and 64%. These results suggest that agentic specification synthesis
benefits substantially from a limited number of iterative interactions, after which additional invo-
cations yield diminishing returns rather than continuously improving specification quality. This
diminishing-return trend also justifies our choice of 10 as the maximum agent invocation budget,
as further interactions are unlikely to yield substantial improvements in specification quality.

 Answer to RQ3: Agentic specification synthesis exhibits clear diminishing returns with increas-
 ing invocation budgets. Most improvements occur within the first 6–8 invocations, after which
 these metrics largely stabilize around 97% precision, 90% recall, and 60–64% verification-gate
 pass rate. This indicates that a moderate invocation budget is sufficient for the agent to capture
 most of the attainable specification quality.


5.4   RQ4: Performance on Real-world Program Verification Tasks
To assess the practical effectiveness of the evaluated baselines on real-world software verification
tasks, we evaluate all approaches on two types of real-world verification tasks. Table 4 demonstrates
the number of verification targets successfully discharged by all baseline methods using DeepSeek-
V4, the best-performing underlying LLM in RQ1. Overall, SpecAgent successfully supports the
verification of 604 out of 811 targets (74.5%), compared with 523 for Codex, 512 for Preguss, and
435 for SpecSyn. This result shows that SpecAgent can effectively translate program context into
specifications strong enough to discharge a large fraction of verification targets. The following
analysis further examines this performance across the two types of real-world verification tasks.
X509-parser, Contiki, and Atomthreads. The programs are extracted from real-world reposito-
ries, with ACSL assertions on runtime error (RTE) freeness instrumented as verification targets.
For these programs, SpecAgent consistently enables the successful verification of a large fraction of
the target properties. Notably, on X509-parser, SpecAgent successfully discharges all 140 targets,
compared with 128 and 126 for Preguss and SpecSyn, respectively. On Contiki, SpecAgent verifies
137 out of 163 targets, again exceeding Preguss (133) and SpecSyn (92). On the more challenging
Atomthreads project, SpecAgent successfully verifies 109 of 239 targets, slightly below Preguss (112)
but above SpecSyn (85), AutoSpec (99), and Codex (101). As described in Section 4.3, the programs
were originally intended to evaluate Preguss, an approach focusing on excluding potential RTEs.
The relatively stable performance of Preguss across these programs suggests its effectiveness on
verification targets concerning RTE-freeness. Codex provides a relatively competitive baseline, but
its performance remains below SpecAgent and Preguss, indicating that a general-purpose agent
alone may not consistently produce specifications sufficient for verification. It is worth noting that
SpecGen verifies none of the targets on X509 and only a small fraction on Contiki and Atomthreads.
This is primarily due to its generation strategy, which requires the LLM to reproduce the input

                                                               , Vol. 1, No. 1, Article . Publication date: October 2026.
16                                                             Lezhi Ma, Han Wang, Shangqing Liu, Jiawan Wang, and Lei Bu


              Table 4. Number of Verified Targets yielded by each baseline (using DeepSeek-V4).
                Repository   Avg. LoC Target Num.     SpecAgent    Preguss   SpecSyn   SpecGen   AutoSpec   Codex
               X509-parser     1199         140          140        128        126        0         83       113
                 Contiki       544          163          137        133        92         6         93       105
               Atomthreads     1451         239          109        112        85        101        22       99
                SV-COMP        27.79        269          218        139        132       195       165       206
                  Total          -          811          604        512        435       312       363       523

program while inserting ACSL annotations into the output, introducing the risk of unintended
source-code modifications. In our experiments, SpecGen modified the source code of both Contiki
and Atomthreads during generation, rendering the corresponding verification targets invalid.
SV-COMP. The programs retrieved from the SV-COMP benchmark are mainly toy examples (av-
erage LoC being 27.79), on which the verification tasks primarily focus on the synthesis of loop
invariants. Among 269 targets, SpecAgent successfully verifies 218, substantially outperforming
SpecSyn (132), Preguss (139), and AutoSpec (165), while remaining competitive with Codex (206),
indicating that SpecAgent possesses a strong capability to reason about iterative program behavior
and synthesize inductive invariants that capture non-trivial loop semantics. In contrast, Preguss
and SpecSyn, which perform relatively competitively on some real-world repositories, show sub-
stantially lower coverage on SV-COMP, suggesting that their strengths on real-world RTE-oriented
properties may not transfer equally well to loop-invariant synthesis. Codex, in contrast, achieves
206 successful verifications and remains close to SpecAgent, indicating that its general-purpose
code reasoning capability is particularly effective on the relatively small SV-COMP programs.
Interestingly, SpecGen and AutoSpec exhibit a noticeable recovery on SV-COMP compared with
the real-world programs. This can be attributed to the relatively small size of SV-COMP programs,
which reduces the challenges for baselines that do not employ a divide-and-conquer mechanism.
Nevertheless, SpecAgent still successfully verifies the largest number of targets, demonstrating its
effectiveness across both smaller programs and larger real-world codebases.

    Answer to RQ4. SpecAgent achieves the highest overall verification coverage, successfully
    discharging 604 out of the 811 verification targets and consistently performing strongly across
    real-world projects and SV-COMP tasks. The results demonstrate that SpecAgent can synthe-
    size sufficiently strong specifications for both large-scale real-world code and loop-intensive
    verification tasks, indicating its ability to adapt the synthesis procedure of different types of
    specifications to diverse verification requirements.


6     Discussion
6.1     Cost Analysis
We further analyze the computational and monetary overhead of the evaluated approaches in terms
of wall-clock time, Frama-C invocations, LLM calls, and API cost. As shown in Table 5, SpecAgent
requires 1,684.49 seconds and 25.58 Frama-C calls per program, far more efficient than verification-
intensive approaches (Preguss and SpecSyn). Although the wall-time overhead over lightweight
approaches (AutoSpec and SpecGen) is non-negligible, it remains substantially lower than the
human effort required for real-world verification projects (e.g., developing ACSL specifications and
completing the verification of X509-parser required five calendar months of manual effort [16]).
Moreover, SpecAgent requires 99.40 LLM calls, slightly fewer than Preguss (107.30), with monetary
cost being $0.6228, lower than Preguss ($0.7210) and Codex ($0.7100) while comparable to SpecSyn
($0.6243). Among the baselines, AutoSpec achieves the lowest overhead across all metrics. However,
this efficiency is accompanied by substantially weaker effectiveness in specification generation

, Vol. 1, No. 1, Article . Publication date: October 2026.
SpecAgent : Empowering Program Verification with Agentic Synthesis of Formal Program Specifications                      17


Table 5. Average execution overhead per program for each baseline on DeepSeek-V4. We calculate the
monetary costs from the figures reported by the official DeepSeek API platform [15].
                      Metrics      Preguss   SpecGen   SpecSyn     AutoSpec      Codex    SpecAgent
                   Wall Time (s)   7750.77    898.88   10305.96      582.46     1717.72     1684.49
                   Frama-C Calls    351.22     5.04     369.33        3.76        2.28        25.58
                     LLM Calls      107.30     4.46      74.82        3.43       120.02       99.40
                    Cost (USD)      0.7210    0.3852    0.6243       0.0341     0.7100       0.6228




and program verification. SpecGen also maintains low computational overhead but exhibits high
instability on verification tasks (Section 5.4). In contrast, Preguss and SpecSyn incur considerably
higher verification overhead, with 351.22 and 369.33 Frama-C calls, respectively, resulting in
substantially longer wall time as well. Overall, SpecAgent achieves a practical balance between
verification effectiveness and resource consumption, introducing moderate overhead to enable
dependency-aware, verification-guided, and iterative specification synthesis.

6.2   Threats to Validity
Internal Threats. First, LLM-based agents may produce different outputs across runs due to
the stochastic nature of generation, introducing potential variance into specification qualities.
We mitigate this threat by fixing the model configurations across experiments and reporting
aggregate results over a series of evaluated tasks. Second, our ablation study incrementally adds
major components to the basic candidate-generation workflow, but adding a component may
also change the subsequent execution trajectory and the number of agent interactions, making
it difficult to completely isolate its individual contribution. We therefore interpret the ablation
results as measuring the contribution of each component within the overall workflow rather than
as strictly independent causal effects. Finally, the effectiveness of SpecAgent may be sensitive to
agent budget configurations, e.g., the maximum number of agent invocations. Concerning this
threat, our additional study on specification quality evolution shows that specification quality
improves noticeably within the first 6–8 agent invocations, after which it tends to plateau, indicating
that insufficient budgets can noticeably degrade specification quality, while larger budgets yield
diminishing returns. The analysis provides empirical insights into the sensitivity of SpecAgent to
agent budget and how to configure the budget in practical scenarios.
External Threats. The main external threat lies in the benchmark adopted for experiments. Al-
though the benchmark programs come from real-world open-source repositories, the number
of programs in the adopted benchmark is still limited. We mitigate this threat by evaluating the
baselines across multiple repositories and complementing the experiments with real-world verifica-
tion tasks. Further evaluation on larger and more diverse software systems is left for future work.
Another threat concerns the language scope, as our evaluation focuses on C programs specified
in ACSL and verified with the Frama-C/WP ecosystem. The effectiveness of the proposed agentic
workflow may depend on the characteristics of this programming language and formal verification
ecosystem, and therefore our findings may not directly generalize to other specification languages
and programming languages. Lastly, our evaluation relies on Frama-C/WP to assess specification
correctness and strength. The verification tool is inherently incomplete, and a valid specification
may fail to be proved due to limitations of the underlying solver, leading to potential false negatives
in our evaluation. Nevertheless, we employ the same Frama-C/WP version, verification config-
uration, and underlying solver environment across all experiments and baselines, ensuring the
consistency and fairness of the comparisons.

                                                                  , Vol. 1, No. 1, Article . Publication date: October 2026.
18                                                           Lezhi Ma, Han Wang, Shangqing Liu, Jiawan Wang, and Lei Bu


7    Related Works
LLM-based Agent for Software Engineering. Recent advances in LLMs have shifted software
engineering automation from mere LLM queries toward autonomous agents that iteratively interact
with software environments. Early efforts such as MetaGPT [26] and ChatDev [44] focus on code
generation by organizing software development as collaboration among role-specialized agents
through predefined workflows for design, coding, and testing. As agentic capabilities evolve, recent
works extend to repository-level tasks involving existing software. SWE-agent [57] addresses
real-world GitHub issues by enabling agents to navigate repositories, edit files, and execute tests
through a specialized interface. AutoCodeRover [60] incorporates program structures and iterative
code search for issue localization and program repair. RepairAgent [9] enables autonomous defect
repair by allowing LLMs to gather information, generate patches, invoke validation tools, and adapt
actions based on feedback. OpenHands [52] further explores general-purpose software engineering
agents that interact with code, command-line tools, and development environments. Despite this
progress, agentic approaches for formal methods remain relatively nascent. Tu et al. [51] introduce
AutoRocq, an LLM agent that performs program verification in the Rocq prover by iteratively
refining proofs based on prover feedback. Sun et al. [50] employ LLM agents to orchestrate model
checking tasks by selecting strategies, analyzing counterexamples, and refining decisions based on
checker feedback. Compared to these works, SpecAgent treats formal specification synthesis as the
primary task, perform agentic generation, repair, and refinement on formal specifications.
LLM-based Program Specification Synthesis. The emergence of LLMs has enabled specification
synthesis beyond conventional rule-based and analysis-based approaches. AutoSpec [54] pioneers
LLM-based specification generation by leveraging static analysis to expose program hierarchies
and guide synthesis. SpecGen [33] combines conversational generation with heuristic mutation
operators to repair generated specifications, while Preguss [53] employs abstract interpretation to
detect potential runtime errors and guide generation. SpecSyn [34] further utilizes non-equivalent
program mutations to assess and refine the semantic strength of generated specifications. Pei et
al. [42] and Cao et al. [11] improve specification generation by fine-tuning LLMs on specification-
related corpora. Compared to these works, SpecAgent reformulates specification synthesis as
an agentic decision-making process, where specialized agents dynamically determine generation,
repair, and refinement actions based on evolving context. Other works [12, 28, 56, 61] target different
specification languages, such as Verus for Rust. Due to substantial differences in programming
languages and formal verification ecosystems, we do not directly compare SpecAgent with these
approaches. Among them, StarVerus [28], a concurrent work, explores autonomous agents for
synthesizing and repairing formal specifications using verifier feedback. However, its primary
objective is to obtain specifications that pass verification, without explicitly critiquing their strength.
In contrast, SpecAgent treats specification correctness as a prerequisite rather than the endpoint,
explicitly identifying semantic deficiencies in the specifications and refining them when necessary.

8    Conclusion
We present SpecAgent, an agentic framework for automated ACSL specification synthesis that refor-
mulates specification generation as an iterative decision-making process. By integrating planning,
generation, verification-guided repair, and critique-guided refinement, SpecAgent identifies and
revisits specification dependencies rather than following a fixed forward-only workflow. Extensive
evaluation on real-world specification generation and verification tasks demonstrates that SpecA-
gent improves specification completeness while maintaining high precision, effectively supporting
practical software verification. These results highlight the potential of agentic approaches for
reliable and scalable formal specification synthesis.

, Vol. 1, No. 1, Article . Publication date: October 2026.
SpecAgent : Empowering Program Verification with Agentic Synthesis of Formal Program Specifications                        19


References
 [1] GitHub - fraunhoferfokus/acsl-by-example: Public snapshots of "ACSL by Example".                    https://github.com/
     fraunhoferfokus/acsl-by-example, 2026.
 [2] GitHub - manavpatnaik/frama-c-problems: A repository dedicated for problems related to verification of programs
     using the tool frama-c. https://github.com/manavpatnaik/frama-c-problems, 2026.
 [3] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida,
     Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774,
     2023.
 [4] Clark Barrett, Christopher L Conway, Morgan Deters, Liana Hadarean, Dejan Jovanović, Tim King, Andrew Reynolds,
     and Cesare Tinelli. cvc4. In International Conference on Computer Aided Verification, pages 171–177. Springer, 2011.
 [5] Patrick Baudin, François Bobot, Loïc Correnson, Zaynah Dargaye, and Allan Blanchard. WP Plug-in Manual, . URL
     https://frama-c.com/download/frama-c-wp-manual.pdf.
 [6] Patrick Baudin, Jean-Christophe Filliâtre, Claude Marché, Benjamin Monate, Yannick Moy, and Virgile Prevosto. ACSL:
     ANSI/ISO C Specification Language, . URL https://frama-c.com/download/acsl.pdf.
 [7] Patrick Baudin, Jean-Christophe Filliâtre, Claude Marché, Benjamin Monate, Yannick Moy, and Virgile Prevosto. Acsl:
     Ansi c specification language. CEA-LIST, Saclay, France, Tech. Rep. v1, 2:79, 2008.
 [8] Dirk Beyer and Jan Strejček. Evaluating software verifiers for c, java, and sv-lib: (report on sv-comp 2026). In
     International Conference on Tools and Algorithms for the Construction and Analysis of Systems, pages 461–502. Springer,
     2026.
 [9] Islem Bouzenia, Premkumar Devanbu, and Michael Pradel. Repairagent: An autonomous, llm-based agent for program
     repair. In 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE), pages 2188–2200. IEEE, 2025.
[10] David Bühler, Pascal Cuoq, and Boris Yakobowski. Eva - The Evolved Value Analysis plug-in. URL https://frama-
     c.com/download/frama-c-eva-manual.pdf.
[11] Jialun Cao, Yaojie Lu, Meiziniu Li, Haoyang Ma, Haokun Li, Mengda He, Cheng Wen, Le Sun, Hongyu Zhang, Shengchao
     Qin, et al. From informal to formal–incorporating and evaluating llms on natural language requirements to verifiable
     formal proofs. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1:
     Long Papers), pages 26984–27003, 2025.
[12] Tianyu Chen, Shuai Lu, Shan Lu, Yeyun Gong, Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Hao Yu, Nan
     Duan, Peng Cheng, et al. Automated proof generation for rust code via self-evolution. arXiv preprint arXiv:2410.15756,
     2024.
[13] Sylvain Conchon, Albin Coquereau, Mohamed Iguernlala, and Alain Mebsout. Alt-ergo 2.2. In SMT Workshop:
     International Workshop on Satisfiability Modulo Theories, 2018.
[14] Leonardo De Moura and Nikolaj Bjørner. Z3: An efficient smt solver. In International conference on Tools and Algorithms
     for the Construction and Analysis of Systems, pages 337–340. Springer, 2008.
[15] DeepSeek. Deepseek platform, 2026. https://platform.deepseek.com.
[16] Arnaud Ebalard, Patricia Mouy, and Ryad Benadjila. Journey to a rte-free x. 509 parser. In Symposium sur la sécurité
     des technologies de l’information et des communications (SSTIC 2019), volume 186, pages 1–30, 2019.
[17] Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, and Shuvendu K Lahiri. Can large language models transform
     natural language intent into formal method postconditions? Proceedings of the ACM on Software Engineering, 1(FSE):
     1889–1912, 2024.
[18] Michael D Ernst, Jeff H Perkins, Philip J Guo, Stephen McCamant, Carlos Pacheco, Matthew S Tschantz, and Chen Xiao.
     The daikon system for dynamic detection of likely invariants. Science of computer programming, 69(1-3):35–45, 2007.
[19] Cormac Flanagan and K Rustan M Leino. Houdini, an annotation assistant for esc/java. In International Symposium of
     Formal Methods Europe, pages 500–517. Springer, 2001.
[20] Maria Joao Frade and Jorge Sousa Pinto. Verification conditions for source-level imperative programs. Computer
     Science Review, 5(3):252–277, 2011.
[21] Paul Gauthier et al. Aider: Ai pair programming in your terminal. GitHub Repository, 2024.
[22] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha
     Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd of models. arXiv preprint arXiv:2407.21783,
     2024.
[23] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang,
     Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint
     arXiv:2501.12948, 2025.
[24] Thomas A Henzinger, Shaz Qadeer, and Sriram K Rajamani. You assume, we guarantee: Methodology and case studies.
     In International Conference on Computer Aided Verification, pages 440–451. Springer, 1998.
[25] Charles Antony Richard Hoare. An axiomatic basis for computer programming. Communications of the ACM, 12(10):
     576–580, 1969.


                                                                    , Vol. 1, No. 1, Article . Publication date: October 2026.
20                                                           Lezhi Ma, Han Wang, Shangqing Liu, Jiawan Wang, and Lei Bu


[26] Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Jinlin Wang, Ceyao Zhang, Steven Yau,
     Zijuan Lin, Liyang Zhou, et al. Metagpt: Meta programming for a multi-agent collaborative framework. In International
     Conference on Learning Representations, volume 2024, pages 23247–23275, 2024.
[27] William E. Howden. Program testing versus proofs of correctness. Software Testing, Verification and Reliability, 1(1):
     5–15, 1991. doi: https://doi.org/10.1002/stvr.4370010103. URL https://onlinelibrary.wiley.com/doi/abs/10.1002/stvr.
     4370010103.
[28] Chao Jiang, Ding Wang, Dugang Liu, Zhiwu Xu, Cheng Wen, Zhong Ming, Yuwei Liu, Xinyi Wan, and Lin Huang.
     Starverus: Llm-powered multi-agent collaboration for industrial rust code verification automation. In Proceedings of
     the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 2, pages 7444–7455, 2026.
[29] Kelvin Lawson. Atomthreads. https://github.com/kelvinlawson/atomthreads, 2026.
[30] Thanh Le-Cong, Bach Le, and Toby Murray. Can llms reason about program semantics? a comprehensive evaluation of
     llms on formal specification inference. In Proceedings of the 63rd Annual Meeting of the Association for Computational
     Linguistics (Volume 1: Long Papers), pages 21991–22014, 2025.
[31] Jiaying Li, Jun Sun, Li Li, Quang Loc Le, and Shang-Wei Lin. Automatic loop-invariant generation anc refinement
     through selective sampling. In 2017 32nd IEEE/ACM International Conference on Automated Software Engineering (ASE),
     pages 782–792. IEEE, 2017.
[32] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu
     Zhang, Chong Ruan, et al. Deepseek-v3 technical report. arXiv preprint arXiv:2412.19437, 2024.
[33] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. Specgen: Automated generation of formal program specifications
     via large language models. arXiv preprint arXiv:2401.08807, 2024.
[34] Lezhi Ma, Shangqing Liu, Yi Li, Qiong Wu, Han Wang, and Lei Bu. Specsyn: Llm-based synthesis and refinement of
     formal specifications for real-world program verification. arXiv preprint arXiv:2604.21570, 2026.
[35] Umang Mathur, P Madhusudan, and Mahesh Viswanathan. Decidable verification of uninterpreted programs. Proceed-
     ings of the ACM on Programming Languages, 3(POPL):1–29, 2019.
[36] Md Rakib Hossain Misu, Iris Ma, and Cristina V Lopes. Veriact: Beyond verifiability–agentic synthesis of correct and
     complete formal specifications. arXiv preprint arXiv:2604.00280, 2026.
[37] Facundo Molina, Marcelo d’Amorim, and Nazareno Aguirre. Fuzzing class specifications. In Proceedings of the 44th
     International Conference on Software Engineering, pages 1008–1020, 2022.
[38] OpenAI. Gpt-3.5, 2026. https://platform.openai.com/docs/models/gpt-3-5.
[39] OpenAI. Gpt-5 model, 2026. https://platform.openai.com/docs/models/gpt-5.
[40] OpenAI. Codex - ai coding partner from openai. https://openai.com/codex/, 2026.
[41] OpenAI. Gpt-5.6: Frontier intelligence that scales with your ambition, 2026. https://openai.com/index/gpt-5-6/.
[42] Kexin Pei, David Bieber, Kensen Shi, Charles Sutton, and Pengcheng Yin. Can large language models reason about
     program invariants? In International Conference on Machine Learning, pages 27496–27520. PMLR, 2023.
[43] Alexandre Peyrard, Nikolai Kosmatov, Simon Duquennoy, and Shahid Raza. Towards formal verification of contiki:
     Analysis of the aes–ccm* modules with frama-c. In RED-IOT 2018-Workshop on Recent advances in secure management
     of data and resources in the IoT, 2018.
[44] Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng Su, Xin
     Cong, et al. Chatdev: Communicative agents for software development. In Proceedings of the 62nd annual meeting of
     the association for computational linguistics (volume 1: Long papers), pages 15174–15186, 2024.
[45] Gabriel Ryan, Justin Wong, Jianan Yao, Ronghui Gu, and Suman Jana. Cln2inv: learning loop invariants with continuous
     logic networks. arXiv preprint arXiv:1909.11542, 2019.
[46] Todd W Schiller and Michael D Ernst. Reducing the barriers to writing verified specifications. In Proceedings of the
     ACM international conference on Object oriented programming systems languages and applications, pages 95–112, 2012.
[47] Xujie Si, Hanjun Dai, Mukund Raghothaman, Mayur Naik, and Le Song. Learning loop invariants for program
     verification. Advances in Neural Information Processing Systems, 31, 2018.
[48] Caio Vinícius Pereira Silveira and Mateus Felipe Tymburibá Ferreira. Assessing postcondition completeness in
     auto-generated function contracts for software verification.
[49] Colin Frank Snook. Exploring the barriers to formal specification. PhD thesis, University of Southampton, 2001.
[50] Youcheng Sun, Jiawen Liu, Daniel Kroening, and Jason Xue. Agentic model checking. arXiv preprint arXiv:2605.21434,
     2026.
[51] Haoxin Tu, Huan Zhao, Yahui Song, Mehtab Zafar, Ruijie Meng, and Abhik Roychoudhury. Agentic verification of
     software systems. Proceedings of the ACM on Software Engineering, 3(FSE):3558–3581, 2026.
[52] Xingyao Wang, Boxuan Li, Yufan Song, Frank F Xu, Xiangru Tang, Mingchen Zhuge, Jiayi Pan, Yueqi Song, Bowen Li,
     Jaskirat Singh, et al. Openhands: An open platform for ai software developers as generalist agents. In International
     Conference on Learning Representations, volume 2025, pages 65882–65919, 2025.



, Vol. 1, No. 1, Article . Publication date: October 2026.
SpecAgent : Empowering Program Verification with Agentic Synthesis of Formal Program Specifications                        21


[53] Zhongyi Wang, Tengjie Lin, Mingshuai Chen, Haokun Li, Mingqi Yang, Xiao Yi, Shengchao Qin, Yixing Luo, Xiaofeng
     Li, Bin Gu, et al. A tale of 1001 loc: Potential runtime error-guided specification synthesis for verifying large-scale
     programs. arXiv preprint arXiv:2512.24594, 2025.
[54] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun Li, Shing-Chi Cheung, and Cong Tian.
     Enchanting program specification synthesis by large language models using static analysis and program verification.
     In International Conference on Computer Aided Verification, pages 302–328. Springer, 2024.
[55] Anyi Xu, Bangcai Lin, Bing Xue, Bingxuan Wang, Bingzheng Xu, Bochao Wu, Bowei Zhang, Chaofan Lin, Chen
     Dong, Chenchen Ling, et al. Deepseek-v4: Towards highly efficient million-token context intelligence. arXiv preprint
     arXiv:2606.19348, 2026.
[56] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Weidong Cui, Yeyun Gong, Chris Hawblitzel,
     Shuvendu Lahiri, Jacob R Lorch, Shuai Lu, et al. Autoverus: Automated proof generation for rust code. Proceedings of
     the ACM on Programming Languages, 9(OOPSLA2):3454–3482, 2025.
[57] John Yang, Carlos Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir Press. Swe-
     agent: Agent-computer interfaces enable automated software engineering. Advances in Neural Information Processing
     Systems, 37:50528–50652, 2024.
[58] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing
     reasoning and acting in language models. arXiv preprint arXiv:2210.03629, 2022.
[59] Gehao Zhang and Juan Zhai. Postcondbench: Benchmarking correctness and completeness in formal postcondition
     inference. In Findings of the Association for Computational Linguistics: ACL 2026, pages 35478–35507, 2026.
[60] Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury. Autocoderover: Autonomous program im-
     provement. In Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis, pages
     1592–1604, 2024.
[61] Sicheng Zhong, Jiading Zhu, Yifang Tian, and Xujie Si. Rag-verus: Repository-level program verification with llms
     using retrieval augmented generation. arXiv preprint arXiv:2502.05344, 2025.




                                                                    , Vol. 1, No. 1, Article . Publication date: October 2026.
