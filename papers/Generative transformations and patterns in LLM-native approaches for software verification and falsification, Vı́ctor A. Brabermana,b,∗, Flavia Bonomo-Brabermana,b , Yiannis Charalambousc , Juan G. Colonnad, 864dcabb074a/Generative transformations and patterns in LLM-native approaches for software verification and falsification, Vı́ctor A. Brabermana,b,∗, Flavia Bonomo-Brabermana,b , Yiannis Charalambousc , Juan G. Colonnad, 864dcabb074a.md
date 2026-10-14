                                        Generative transformations and patterns in LLM-native approaches for software verification
                                                                             and falsification

                                             Vı́ctor A. Brabermana,b,∗, Flavia Bonomo-Brabermana,b , Yiannis Charalambousc , Juan G. Colonnad , Lucas C. Cordeiroc,d ,
                                                                                             Rosiane de Freitasd
                                                                         a Departamento de Computación, FCEyN, Universidad de Buenos Aires, Buenos Aires, Argentina
                                                                   b Instituto de Investigación en Ciencias de la Computación (ICC), CONICET-UBA, Buenos Aires, Argentina
                                                                               c Department of Computer Science, The University of Manchester, Manchester, UK
                                                                   d Instituto de Computação (ICOMP-UFAM), Universidade Federal do Amazonas, Manaus, Amazonas, Brazil
arXiv:2404.09384v3 [cs.SE] 6 Oct 2025




                                        Abstract
                                        The emergence of prompting as the dominant paradigm for leveraging Large Language Models (LLMs) has led to a proliferation of
                                        LLM-native software, where application behavior arises from complex, stochastic data transformations. However, the engineering of
                                        such systems remains largely exploratory and ad-hoc, hampered by the absence of conceptual frameworks, ex-ante methodologies,
                                        design guidelines, and specialized benchmarks. We argue that a foundational step towards a more disciplined engineering practice is a
                                        systematic understanding of the core functional units–generative transformations–and their compositional patterns within LLM-native
                                        applications.
                                           Focusing on the rich domain of software verification and falsification, we conduct a secondary study of over 100 research proposals
                                        to address this gap. We first present a fine-grained taxonomy of generative transformations, abstracting prompt-based interactions into
                                        conceptual signatures. This taxonomy serves as a scaffolding to identify recurrent transformation relationship patterns–analogous to
                                        software design patterns–that characterize solution approaches in the literature. Our analysis not only validates the utility of the
                                        taxonomy but also surfaces strategic gaps and cross-dimensional relationships, offering a structured foundation for future research in
                                        modular and compositional LLM application design, benchmarking, and the development of reliable LLM-native systems.
                                        Keywords: generative transformation, LLM-native software, design patterns, downstream task, large language models, LLM4SE,
                                        prompt engineering, software engineering, software testing, software verification, taxonomy.


                                        1. Introduction                                                                     We posit that a more principled engineering approach requires
                                                                                                                         a shift in perspective: from a low-level view of prompts as data,
                                           The emergence of prompting as the dominant paradigm for                       to a view of LLM interactions as generative transformations.
                                        interacting with large language models (LLMs) has unlocked                       These are discrete, prompt-induced, LLM-mechanized opera-
                                        new capabilities across diverse domains [251]. Seminal work                      tions that convert stochastically input data into output data. As
                                        demonstrated that strategically structured prompts—whether                       a concrete example, Figure 1 illustrates how the meso-level
                                        through detailed instructions or few-shot demonstrations—can                     view and concepts proposed in this paper could be used to pre-
                                        elicit sophisticated reasoning and task performance without the                  cisely and uniformly describe a representative execution –in
                                        need for model fine-tuning [27, 180, 252]. This has led to the                   this case, a solution proposal within scope, ChatTester [284].
                                        rapid proliferation of LLM-native software, where core func-                     This transformation-oriented viewpoint resonates with emerging
                                        tionality is achieved by orchestrating LLMs through prompts,                     modular and declarative frameworks (e.g., [21, 59, 127]) and we
                                        often within complex chains of generative processing alongside                   argue it can bring the construction of LLM-native software closer
                                        conventional code [83, 127, 227].                                                to the cognitive way we design traditional systems–reasoning
                                           However, the engineering discipline for constructing such sys-                about system behavior through the composition of “functional
                                        tems remains in its infancy [16, 83]. As a widely cited industry                 units”.
                                        maxim captures, “Experimenting with LLMs is the only way
                                        to build LLM-native apps” [15]. We argue this trial-and-error                       This work serves to demonstrate the viability and utility of
                                        paradigm persists due to a critical gap: the absence of conceptual               the transformation-oriented viewpoint. Through a systematic
                                        frameworks to reason about LLM-native software and ex-ante                       analysis of the literature, we develop an initial catalog of genera-
                                        engineering methodologies.                                                       tive transformations and their composition patterns. We argue
                                                                                                                         this catalog provides immediate value for practitioners while
                                           ∗ Corresponding author. Departamento de Computación, FCEyN, Univer-
                                                                                                                         establishing the foundational layer for a more disciplined engi-
                                        sidad de Buenos Aires. Ciudad Universitaria, Pabellón 0+∞. Pres. Dr. Raúl
                                                                                                                         neering paradigm–one capable of high-level, abstract reasoning
                                        Alfonsı́n s/n, (1428) Buenos Aires, Argentina.                                   about system behavior. By providing this structured vocabulary,
                                             Email address: vbraber@dc.uba.ar (Vı́ctor A. Braberman)                     the catalog enables future research directions, such as: (1) spe-
                                        Preprint submitted to Elsevier                                                                                                        October 8, 2025
cialized benchmarks and theoretical models, (2) transformation-
                                                                                       Focal
specialized LLMs, and (3) ex-ante methodologies for reliable                                                 Intent            CodeCorresponding-Intent-Verbalization
                                                                                      Method
LLM-native systems design.
   To ground our investigation, we focus on the domain of soft-
ware verification and falsification. This domain is ideal for our
                                                                                                              Unit
study as it represents a critical, rapidly evolving area of software                  Signature                                 IntentCorresponding-Test-Generation
                                                                                                             Test (0)
engineering [99, 246] with inherent diversity–encompassing
fuzzing, formal verification, and test generation. This diversity
suggests that LLM-native solutions here are likely to be sophisti-
cated, featuring a rich variety of generative transformations and                     Compilation
                                                                                        Errors
compositions.
   Thus, we first address the following research question:


    RQ 1.      Can prompt-based interactions with LLMs                                             Unit
                                                                                                  Test (1)
                                                                                                                        ErrorAware-Test-Correction

    be abstractly described as the execution of generative
    transformations with conceptual signatures? What dif-
    ferent types of transformations emerge from an analysis                Figure 1: An abstract execution of ChatTESTER [284] modeled using our
    of LLM-based software verification proposals?                          conceptual framework. This Bayesian network depicts data flow through the
                                                                           system, where variables represent either inputs (FocalMethod) or outputs
                                                                           from transformations. Generative transformations (labeled with types like
                                                                           IntentCorresponding-Test-Generation) produce stochastic variables through
   To address RQ1, we conducted a systematic analysis of over
                                                                           LLM-mechanized processes, while algorithmic transformations produce de-
100 papers, characterizing prompt-based interactions as data               terministic variables (double-circled, e.g., CompilationErrors). Edges
transformations. The diversity of observed transformations mo-             denote the conceptual input signature of each transformation; for instance,
tivated us to develop a structured taxonomy and a mapping.                 UnitTest(0) depends on Signature and Intent according to the distribu-
                                                                           tion of an IntentCorresponding-Test-Generation transformation. The model
                                                                           reveals two key inter-transformation patterns: Use Verbalized SW Entity
                                                                           (reasoning via intent rather than code) and Generate & Fix (iterative correc-
    RQ 2.       Can the identified transformation types be                 tion using compilation errors).
    organized and mapped into a taxonomy that captures
    their shared characteristics and key differentiators?
                                                                           model and compiler for optimizing the prompts that implement
                                                                           such transformations, our work aims to establish a foundational
   A primary utility of this taxonomy is its ability to scaffold the       conceptual taxonomy of the transformations themselves. We
identification of recurring solution approaches, which we term             seek to answer: What are the fundamental types of generative
Inter-Transformation Patterns (by analogy to software design               operations being composed? By systematically cataloging these
patterns [70]).                                                            functional units and their interconnection patterns, we provide a
                                                                           semantic grounding that can inform the design of future program-
    RQ 3. To what extent can our taxonomy, combined                        ming models, compilers, and evaluation benchmarks. In essence,
    with manual dataflow analysis, systematically surface                  if DSPy offers a “how” for building LLM-native software more
    recurrent solution patterns in existing LLM-native pro-                robustly, our taxonomy provides a “what”–a vocabulary for the
    posals?                                                                core stochastic functionalities that such systems are built upon.
                                                                              Unlike existing taxonomies that focus on broad Natural Lan-
                                                                           guage Processing (NLP) tasks, our work uncovers the actual
   Addressing RQ3 helps validate the utility of our taxonomy               transformations requested in prompt-based interactions. Ex-
while uncovering practical insights for modular LLM application            isting surveys do not discuss the details of decomposition of
design. To our knowledge, this is the first comprehensive effort           solutions into transformations and the abstraction level of their
to catalog both the transformation space and its associated design         summarized information is not adequate to answer our ques-
patterns.                                                                  tions. We are not aware of any taxonomy that would serve
   Finally, we employ our integrated artifacts—the taxonomy,               the preceding purposes. NLP and cognitive tasks appearing
patterns, and their mappings—to conduct a cross-analysis. This             in benchmarks like [89, 149, 221, 234] partially cover some
analysis aims to identify significant relationships and highlight          of the transformations encountered, but most identified trans-
strategic gaps, thereby revealing current limitations and inform-          formations are novel. Traditionally, tasks in the NLP commu-
ing valuable future research directions.                                   nity have been identified and typically classified in benchmarks
                                                                           (e.g. [89, 149, 214, 221, 234]). However, these benchmarks are
1.1. Related Work                                                          neither necessarily focused on software engineering problems
   This transformation-oriented viewpoint aligns with and com-             nor particularly designed to identify transformations that actu-
plements emerging frameworks for structuring LLM applica-                  ally appear in the field. This has been partially recognized in
tions, such as DSPy [127]. While DSPy provides a programming               some benchmarking papers [107, 123, 198, 270, 276]. How-
                                                                       2
ever, in this paper, we pinpoint some overlaps with our proposed           maintenance. Some SE problems overlap with the scope of our
taxonomy. Recently, [115] proposes SWE-bench as an evalu-                  mapping. More precisely, fault localization, vulnerability detec-
ation framework consisting of software engineering problems                tion, unit test generation, assertion generation, fuzzing, failure-
drawn from real GitHub issues. Some of the difficulties may                inducing testing, penetration testing, property-based testing, mu-
partially overlap with the problems addressed in the scope of              tation testing, GUI testing, bug report detection, bug reproduc-
this mapping. However, the focus on GitHub issues implies                  tion, and bug replay. They report on representative code-related
that problems are closer to the area of software corrective and            LLMs and, related to our paper, they identify 11 classes of tasks
evolutive maintenance than the area of verification/falsification.         across four categories defined according to the input/output
More importantly, this is an evaluation framework and thus                 data type: Code-Code: code translation, code refinement, cloze
no transformation elicited by potential solution proposals are             test, mutant generation, assertion generation; Text-Code: code
presented.                                                                 generation, code search; Code-Text: code summarization; and
   Several surveys have also been conducted on the use of LLMs             Code-Label: code classification, clone detection, defect detec-
in Software Engineering papers (e.g., [85, 62, 92, 99, 300]).              tion. Almost all the tasks classes are included in our taxonomy.
Although, to the best of our knowledge, none of the existing               Moreover, their way of classifying tasks/transformations is or-
surveys performs concrete LLMs transformations identification              thogonal to ours, and we make an explicit sub-classification
and mapping, they are relevant related work with some elements             according to type of input-output of the task for some of the
in common with this work.                                                  categories.
   A systematic review of the literature on the use of LLM in                 Our pattern identification and mapping effort focuses on so-
SE (LLM4SE) between 2017 and January 2024 is presented                     lutions that can be expressed as the interrelationship of trans-
in [92]. Key applications of LLM4SE described encompass a                  formations, including the mediation of symbolic computation.
diverse range of 55 specific SE problems, grouped into six core            This leads to a rather systematic exploration and identification of
SE activities. Problems in the quality assurance category overlap          solution patterns in solution proposals and exemplars. Although
with those in the scope of our study. There is no report on how            our work is inspired by the design patterns of [70], we deliber-
proposals structure solutions into LLM-enabled transformations.            ately deviate from their full documentation style. To maintain a
   Within our area of interest, test generation, test adequacy, test       strong, verifiable connection to the recovered transformations
minimization, test oracle problem, and test flakiness are prob-            and studies in scope, we focus our documentation on the core
lems covered by [62]. Unlike this work, the focus is on compar-            elements of name, intent, motivation, and examples. We omit
ing the effectiveness reported by each approach. Again, there              traditional sections like “Consequences” as their speculative
is neither identification nor categorization of concrete LLMs              pros and cons would be premature for the patterns identified in
transformations in proposals that use prompts.                             our nascent and rapidly evolving domain.
   LLM-based fuzzers are analyzed in [99]. The focus is on                    Our transformation-centric approach provides a distinct ana-
how LLMs are used for fuzzing tests and on comparing LLM-                  lytical lens compared to existing pattern catalogs in academy1 .
based fuzzers with traditional fuzzers. Although extra detail is           For instance, [256] presents a “Prompt Pattern Catalog” that
given for LLM-based approaches, neither systematic mapping                 structures 16 effective interaction strategies for humans to in-
nor taxonomy is proposed.                                                  teract conversationally with LLMs like ChatGPT. That is, their
   A survey on testing problems, which also includes debugging             catalog is not focused on the use of prompts in the context of
and repair proposals, is conducted in [246]; 52 papers on testing          LLM-native software broadly speaking. Having said that, links
are covered (33 published since 2022), of which approximately              with our work can be unveiled when one think on the transfor-
one-third concerned test-based LLM fine-tuning, while the re-              mations necessary for implementing an LLM-native application
mainder rely upon prompt engineering. The survey analyzes the              that enables user intervention. For instance, the “flipped in-
papers from both the software testing and LLM perspectives. It             teraction pattern” can be implemented in LLM-native UI by a
presents a detailed discussion of the software testing problems            combination of our patterns, namely, Reactively Consume
for which LLMs are used, including unit test case generation,              Input (in this case, whatever the human has to utter) together
test oracle generation, system test input generation, bug anal-            with the Enrich with Precisions pattern application for the
ysis, and features on how these tasks are solved with the help             human task in question.
of LLMs. In particular, it describes the commonly used LLMs,                  Other related work includes [259], which proposes “Cognitive
their input, the types of prompt engineering employed, and the             Design Patterns” drawn from established cognitive architectures
techniques that form the concrete cognitive architecture of these          (e.g., SOAR, ACT-R) and maps them to capabilities in agentic
proposals (e.g., pure LLMs, LLM + statistical analysis, LLM                LLM systems. Their work demonstrates how high-level cogni-
+ program analysis, LLM + mutation testing, LLM + syntactic                tive functions, such as “Observe-Decide-Act” or “Episodic Mem-
checking, LLM + differential testing). Yet, there is no focus on           ory”, are instantiated in LLM-native designs. Separately, [153]
which concrete types of transformations are actually elicited.             presents an “Agent Design Pattern Catalogue” comprising 18
   In [294], a systematic survey on LLM-based approaches for
SE problems, including empirical evaluations, is presented. It                 1 Practitioner guidance for building LLM-enabled applications are typically
includes 155 studies for 43 specific code-related tasks across             focused in agents and patterns are either higher-level architectural ones or prompt
four phases within the SE workflow: software requirements &                (or context) guidance (e.g. Open AI’s “A practical guide to building agents” or
design, software development, software testing and software                Anthropic’s “Effective context engineering for AI agents”).

                                                                       3
architectural patterns and a decision process that address chal-             candidate locations in the source code that could be claimed
lenges in foundation model-based agent design. Also, it is worth             as likely faulty [187, 258]. A related defect localization prob-
mentioning [216] aimed at providing an architectural description             lem is that of Root Cause Analysis (RCA) when system-wide
language able to contextualize LLM agent research proposals.                 anomalous behavior is found in production (e.g., [110, 213]).
   However, our methodology and results differ fundamentally                 The main challenge in diagnosing the root cause of systems is
in both granularity, scope and analytical approach. While [259]              the interconnected dependence between different services that
analyzes systems from a top-down, architecturally-derived per-               could be internal or third-party.
spective, and [153] catalogs architectural patterns at different                Bug reproduction is one of software development’s first stages
levels of abstraction and generality (e.g., agent adapters, reflec-          of bug fixing when a bug is reported by software users. It
tion, agent goal creation, etc.) that are of interest for a particular       involves reproducing the bug on the developer’s system so that
application domain, we, instead, adopt a bottom-up, domain-                  it can be further analyzed [175]. An associated challenge is
agnostic approach focused on the interrelationship of generative             managing multiple reports regarding the same bug, which can
transformations. That is, our transformation-centric analysis                slow down the bug-fixing process, as it requires resolving all
captures the emergent behavioral patterns that arise from how                duplicate entries before attempting to fix the bug itself [5, 55,
operations are sequenced and composed regardless of the appli-               86, 108].
cation domain.                                                                  There is a wide spectrum of problems derived from the
   This transformation composition focus is a rather unique fea-             goal of analyzing code without executing it. Static analy-
ture that enables a more systematic exploration of the LLM-                  sis [178], generally speaking, encompasses a variety of prob-
native design space. It enables the (re)discovery of existing                lems and approaches ranging from detecting potential vulner-
strategies–such as those encapsulated in the prompt pattern                  abilities or misuses in source code syntactic structures or ML-
catalog–and, crucially, the identification of detailed composi-              representations [10, 93, 141, 143, 202] to sound(y) [157] com-
tional patterns that were previously uncataloged. This is pre-               putation of collecting semantics [40, 44, 165]. Traditional in-
cisely because it operates at a more granular level than architec-           termediate abstractions like control-flow graphs [6] play central
tural component patterns and is not constrained by pre-existing              roles in many analyses. Static analysis is not limited to checking
taxonomies of high-level cognitive functions. By examining                   for a given property. Well-established research topics include
how transformations interact behaviorally rather than how com-               statically built multipurpose program abstractions or extractions.
ponents are structured architecturally, our approach captures the            For example, static slicing [254] addresses the problem of iden-
emergent solution structures that arise from the unique possibili-           tifying statically a set of relevant lines for the computation of a
ties of composing LLM-based and symbolic transformations.                    value in a given program location.
                                                                                Program verification [87] is an area with a well established
                                                                             tradition and that has covered different classes of programs and
2. Background                                                                properties. Software model checking [14, 43, 112] and deductive
                                                                             software verification [134, 135] are among the main trends for
2.1. Verification and falsification problems                                 sequential software correctness verification. In many of those
   Testing is a classical and arguably the most popular approach             approaches, invariant generation [45] is a key challenge for
to gaining confidence in software systems before release [11, 19].           effective automation.
When emphasizing that testing should be regarded as a way                       Recently, some novel application areas and technologies be-
to falsify software and not a way to verify it [57] it becomes               come relevant targets of mentioned verification and testing
clear how research in testing has evolved by focusing on failure             approaches. Among them: GUI-based/mobile applications
detection ability of test suites (automatic) generation propos-              (e.g., [164]), RESTfull services [74], smart contracts [239],
als [185]. Several approaches to test suite generation have been             and Machine-Learning systems, software and applications
proposed [12]. Among others, symbolic and random approaches                  (e.g., [26, 102, 224, 291, 292]). These areas are covered by
(potentially combined) [28, 72, 186], mutation-based ones [113],             the studies in scope.
and search-based approaches [67]. A particular technique of
testing is fuzzing [169], which typically involves adaptively gen-           2.2. Large language models
erating a series of inputs –usually by mutating some input seeds–               Pre-trained Large Language Models (LLMs) (e.g., [56, 299])
to cause the Program under Test (PuT) to crash or enter a defec-             are a type of Generative AI based on Deep Neural Networks [75].
tive state. It does so by repeatedly stimulating the program and             Initially, these models utilized a Transformer encoder-decoder
observing its behavior in a sort of feedback loop [24, 304]. A               architecture with cross-attention mechanisms [237]. However,
typical problem when testing or fuzzing and looking for evidence             many modern LLMs now employ a decoder-only architecture
of (functional) falsification beyond crash or memory corruption              with self-attention layers, which is sufficient for generating out-
is known as the oracle problem. That is, determining, either for a           put from a given input prompt [27].
set of inputs or in general terms, the correct behavior that should             Among the most well-established prompting methods used
be exhibited by the program [18]. Metamorphic relation identifi-             are: Zero-Shot [130], Few-Shot [27], Chain-of-Thought [252],
cation has been a way to partially circumvent the oracle prob-               Tree-of-Thoughts [280], Retrieve Augmented Generation [137]
lem [36]. Once a failure is detected, fault localization is typically        and Reasoning and Acting [281]. Zero-Shot [130] learning in-
the next problem to be solved. Fault localization aims at listing            volves prompting an LLM to perform a specific task without
                                                                         4
providing examples or demonstrations. Few-Shot [27] learning             observed interrelationships. Due to the research questions, in-
includes examples of the task within the prompt. These examples          depth analysis of papers and taxonomy and patterns definitions
serve as demonstrations that condition the model, enabling it to         played a central role that surpassed other typical aspects of
generate sometimes more accurate responses for similar tasks.            systematic mappings such as demographics on areas, topics
Chain-of-Thought (CoT) is an orthogonal prompt approach that             or venues. Given the application focus (software testing and
proposes to generate a logical, linear flow of ideas and reason-         verification), we went through abstracts of papers published or
ing [252]. Thanks to the autoregressive nature of LLMs, they             announced in Software Engineering venues (ICSE, FSE, ASE,
end up (auto)conditioning themselves by verbalizing utterances           ISSTA, ICST, MSR, SANER, ICSME, ICPC, GECCO, TOSEM,
that hopefully correspond to steps of an effective reasoning pro-        TSE, ESE, JSS, STVR, SPE, IST, etc). The same was done
cess. While CoT is an advanced technique that improves LLM               for Programming Language and Formal Verification venues
answers, its fundamental concept relies on a linear reasoning pro-       (e.g., PLDI, POPL, OOSPLA, ECOOP FM/FV: CAV, TACAS,
cess. It does not allow for divergent thoughts. Tree-of-Thought          VMCAI, FM, FMCAD), Operating Systems and Security venues
(ToT) [280] was created to overcome this limitation with the             (USENIX, IEEE SSP), and also major AI venues (AAAI, IJCAI,
intuition of aggregating different “points-of-view” during the           ICML, ICLR, NeurIPS). Arguably, arXiv was a major source of
reasoning process. In ToT, a query to an LLM can generate sev-           papers. We performed searches using technology keywords such
eral different answers, some better than others. These answers,          as “LLM”, “language”, “ChatGPT”, “context”, “prompt” and
in turn, can each generate more than one response, forming a             application related keywords such as “testing”, “verification”,
tree of thoughts that helps reasoning through different paths.           “formal”, “check”, “static”, “fuzzing”, “debugging”, etc. (see
In this tree, the initial query generates the root, and the leaves       SE Problems in Figure 2). We mainly found validation research
of each node are the intermediate thoughts. Thus, to form the            and solution proposal papers [189]. From the SE-related surveys
final response, intermediate prompts corresponding to some path          on using LLMs, we snowballed one level and added missing
within this tree must be used. The final performance of ToT              papers. The time scope for the first collection was essentially
depends largely on the path-selection strategy. While the men-           from 2022 until February 2024 (later expanded to June 2024 and
tioned techniques improve the generated answers, they depend             tested with late October 2024’s conference papers, as mentioned
exclusively on the information in the prompt or the knowledge            below). Then, we carefully analyzed papers by reading both
in the LLM itself. RAG [137] overcomes this limitation by en-            abstract and content, discarding those that did not use prompts
abling access to the latest information for generating reliable          or deal with different SE problems (approx. 140 papers were
outputs via retrieval-based generation. In RAG, an augmented             discarded, and 75 remained).
prompt with contextual information from an additional database              We first read the papers to identify the tool/approach name
helps reduce hallucinations. It makes the LLM adaptive to sit-           given and the actual SE problem solved. Those identified prob-
uations where facts evolve over time by simply updating the              lems were classified into the SE problems taxonomy, and papers
knowledge in this database. This approach also avoids the need           were mapped into it as shown in Figure 22 . This SE problems
for LLM fine-tuning, reducing computational demands. RAG                 taxonomy is similar to other taxonomies found in the literature
can also be combined with other prompting techniques, such as            for the overlapped categories (e.g. [294])3 . From there, as the
CoT, to condition the reasoning process on the given context. For        figure shows, by reading each paper, we performed the labo-
tasks like code generation, the database can be enhanced with            rious identification of transformations, their conceptual intent
examples of code or test cases, further improving the accuracy           and signatures and integration/orchestration notes (Tables 1–5
and reliability of the newly generated codes.                            in v2 of this preprint [25]). Subsection 3.1 further explains our
   ReAct [281] combines reasoning and acting in an interleaved           viewpoint for identification.
manner, where the performed reasoning steps can ask an LLM to               The initial list of transformations (200 approx. with repeti-
perform some tasks, usually involving the operation of external          tions) was then clustered into categories explained in section 5.
tools, and then reason again about the retrieved output from such        Variation points and hierarchy decisions lead to the trees seen
tools. This allows dynamic reasoning and planning, like an AI            (Figs. 5–8 and Figs. A.11–A.29 in Appendix). Another author, in
agent, by interacting with external environments and incorpo-            a “tabula rasa” modality (i.e., no expertise in topics and without
rating the additional information from those environments into           reading previously the papers nor elaborated tables or taxon-
the context prompt. In the context of code generation, this could        omy), was able to map the 200 transformations recovered into
allow executing some code snippets or using verification tools,          the hierarchy to validate that both the table and the taxonomy
observing the output, and planning the next reasoning step until         were “natural” and easy to understand resources. Interestingly,
generating the final answer. For an extensive survey on prompt           during the final steps of this elaboration, we updated the list to
methods the reader can refer to [147].                                   beginning of June 2024 with the more recent papers (36 papers)
                                                                         that were not in the original table. We were able to seamlessly
3. Methodology                                                           add them (and map their 83 transformations) albeit we decided
                                                                         to change some names of transformations and internal structure
   A method that is partially inspired on those of systematic
mapping [189] was followed as a way to come up with the main                2 Some papers were mapped into more than one SE problem when adequate.
contributions of this work, namely: transformation identification,          3 Due to the exclusion criteria, automated program repair is not shown as a

transformations type taxonomy, interconnection patterns, and             debugging subproblem.

                                                                     5
SE Problems
                                                                                            not featured by any of the approaches. A version of this work
   Testing                                                                                  was uploaded on September 8th, 2024, as a technical report [25].
      Unit Test Generation: TestGen-LLM [8], FSML [17], ChatGPTTests [22],                  A couple of weeks later, we performed the identification of trans-
      CodeT [33], ChatUniTest [39], CodeCoT [97], AgentCoder [98],
                                                                                            formations of solution proposals appearing in papers that had
      CodaMOSA [136], TestChain [139], CoverUp [192], TestPilot [204],
      EASEeval [212], HITS [249], TELPA [272], LLM-UTG [277], ChatTester [284]              just been announced as accepted to ASE 2024 and mapped them
      Failure-Inducing Test Generation: DiffPrompt [140], AID [145], secTests [298]         into the baselined taxonomy trees to double check whether types
      Regression Testing: SymPrompt [201]
      Input Generation: DirInput [114], RESTGPT [128], InputBlaster [156],
                                                                                            were already seen or the versatility of trees to accommodate
      PBT-GPT [240], mrDetector [263]                                                       novel variants. That mapping is highlighted using, in the trees of
      DataSet/Mutant Generation: FSML [17], MuTAP [47], BugFarm [105],                      the paper and the ones of Appendix A, squared boxes around the
      µBERT [124], CHEMFUZZ [196], FormAI [229]
      Fuzzing
                                                                                            names of the ASE 2024 tools that were not previously analyzed
           General Fuzzing: OSS-Fuzz [76], ChatFuzz [94], Fuzz4All [268], UGCTX [286]       as arXiv preprints.
           Kernel Fuzzing: KernelGPT [275]                                                     After this, we updated the publication venues of all the papers
           Compiler/Simulator Fuzzing: SearchGEM5 [46], WhiteFox [274]
           Protocol/Parser Fuzzing: FuzzingParsers [1], ChatAFL [168]
                                                                                            that were originally retrieved from arXiv4 . That step included
           DL-Libraries Fuzzing: TitanFuzz [53], FuzzGPT [54], Magneto [303]                changing some of the tool names when they were modified in
      GUI Testing: QTypist [154], GPTDroid [155], AXNav [222]
                                                                                            the published version.
      Functional Testing: TARGET [52], ScenicNL [60], SoVAR [78],
      LLMeDiff [106], SysKG-UTF [215], LeGEND [225]                                            Finally, by analyzing how different types of transformations
      Penetration Testing: PentestGPT [51], Pwn’d [82], AdvSCanner [265]                    were interconnected in each solution proposal (within the subset
      Oracle Problem: FSML [17], SELF-DEBUGGING [37],
      nl2postcondition [61], TOGLL [90], Eywa [117], PropertyGPT [151],
                                                                                            of peer-reviewed papers), we identified a set of recurrent patterns,
      ClarifyGPT [173], CEDAR [176], PROSPER [207], EMR [210],                              which we termed Inter-Transformation Patterns. We further
      GameBugDescriptions [223], MetaMorph [231], ALGO [293]                                conjectured which limitations of LLMs are addressed by each
   Debugging
      Bug Reproduction: AdbGPT [64], CrashTranslator [104], LIBRO [122],
                                                                                            of these patterns, and then examined the relationships between
      SemSlicer [273]                                                                       patterns and transformation categories.
      Bug Report Analysis: FAIL [13], Cupid [295]
      Fault Localization: SELF-DEBUGGING [37], AutoFL [120], AutoSD [121],
      LLM4CBI [232], ChatGPT-4(Log) [266]                                                   3.1. Inclusion and exclusion criteria
      Root Cause Analysis: RCACopilot [38], x-lifecycle [73], LasRCA [79],
      RCAAgents [199], LM-PACE [288], inContextRCA [296]                                       As said, our technological focus is on using LLMs that employ
   Vulnerability/Misuse/Malware/Fault Detection
      Vulnerability Detection: ChatGPT4vul [69], VulBench [71], NLBSE24 [111],
                                                                                            prompts. This excludes proposals that are based primarily on
      VulDetect [125], GRACE [158], VSP [181], AIagent [208], VFFinder [267],               either fine-tuning LLMs (see for instance [179]) or general trans-
      DLAP [278], MultiTask [283], PromptEnhanced [287], VulAdvisor [290],                  former architectures (e.g., [7, 41, 54, 58, 66, 68, 77, 80, 96, 126,
       RustC4 [297], ChatGPT(Plus) [301]
      Line-Level/Edit-Time Fault/API Misuse Prediction: FLAG [3], EditTime [30],            172, 177, 182, 188, 197, 209, 218, 233, 238, 289, 305], etc.), or
      WitheredLeaf [35], LLMAPIDet [253]                                                    leverage embeddings of underlying transformers (e.g. [91, 271],
      Vulnerability Detection for Smart Contracts: ChatGPTSCV [34], SmartAudit [48],
                                                                                            etc.). Selected Software Engineering topics are by no means
      GPTLens [95], GPTScan [220], LLM4Vuln [219], Skyeye [245], Sleuth [260]
      Vulnerability Detection for Packages: SpiderScan [103]                                all areas addressed by LLM-enabled in-context/prompting ap-
   Static Analysis                                                                          proaches. Yet, they currently constitute a significant amount
      Call-Graph/CFG Construction: CFG-Chain [100]
      Use Before Initialize: LLift [138]
                                                                                            of works in SE venues5 . As a notable excluded topic, we do
      Resource Leak: SkipAnalyzer [171], InferROI [244]                                     not cover papers whose main SE goal was program genera-
      Data-Flow Analysis: LLMDFA [243]                                                      tion/synthesis or program repair, which are allegedly “natural”
      Taint Analysis: E&V [81], LATTE [148]
      Static Slicing: SimulinkSlicer [160]
                                                                                            areas of application of generative AI [62, 92, 242, 269, 294].
      Fix Acceptance Check: CORE [241]                                                      The other excluded topic is code reviews. Yet, there are two
      Toxicity Analysis: ToxicDetector [152]                                                important caveats regarding exclusions. On the one hand, some
   Program Verification
      Program Verification: AlloyRepair [4], ChatInv [109], Loopy [119],                    approaches studied elicit code generation or repair transforma-
      SpecGen [161], Dafny-Synth [170], ESBMCibmc [191], Clover [217],                      tions to achieve testing, fault localization or verification goals
      AutoSpec [255], Lam4Inv [261], Lemur [262], RustProof [279]
                                                                                            and we, consequently, do report and analyze those papers. On
                                                                                            the other hand, we also report papers whose primary goal is
Figure 2: Overview of the SE problems considered in this paper, and the tools               program generation, debugging with repair, or code review but
corresponding to each of them. Framed tools are the ASE’24 ones, that were
added at the validation step.                                                               they prompt testing, verification or fault localization tasks to
                                                                                            achieve their end-to-end goals. Thus, the exclusion is limited to
                                                                                            works whose primary SE goal is out of scope and do not prompt
of taxonomy trees to adhere to traditional terminology in those                             LLMs to solve Software Engineering problems within the scope.
areas in which certain types of transformations already exist                               The other important exclusion criterion is the date: this paper
(e.g., classification tasks). This update thus served as another                            version covers papers that appeared in journals, conferences,
validation step. After that, we went through tables, trees, and
the mapping matrix (Table 2) and validated that taxonomy at
                                                                                               4 This is why some papers of very recent conference editions and journal
least helped detect and exhibit some known and potentially un-
                                                                                            volumes appear as part of the papers in scope while not necessarily all papers of
known patterns of LLM usage. Finally, we also check that NLP                                those venues that satisfied the criteria were analyzed.
tasks [221, 236] (e.g. relation extraction [221, 282]) relevant to                             5 For instance, they made up approximately 40% of LLM-enabled prompt-

the surveyed works were either included into the taxonomy or                                based approaches of FSE 2024 main track papers.

                                                                                        6
or arXiv up to the first week of June 2024, and papers already              4. naming those transformations in a way to convey expected
announced in conferences up to July 2024.                                       “functionality”.
   We are aware of other comparative analyses that we do not              This analysis presented several challenges we overcome. First,
include here because their prompts are based on literature already        the LLMs manifest a great versatility observed in a wide vari-
reported in our work, for example [226]. Last but not least, it can       ability of questions, instructions, directions, and example-based
be noticed that some traditional SE falsification and verification        elicitation across the literature. Second, solution proposals exhib-
areas like run-time verification, symbolic execution and (some)           ited significant heterogeneity in their presentation, with diverse
model checking challenges are not covered: under the defined              prompting strategies and, often, incomplete descriptions in pa-
LLM and timeline related criteria, no studies were found that             pers of key aspects. That is, while prompts being first-class
could directly be mapped as addressing those topics as their              concepts are typically sketched, their abstract description of
primary contribution focus.                                               functional units we seek is either missing or imprecise and ter-
                                                                          minology varies substantially between studies. Thirdly, there is
                                                                          a wide variety of ways to build prompts and elicit generations
4. Conceptual decomposition of studies into transformations               during inference time. Moreover, prompts and transformations
                                                                          are not necessarily related 1-to-16 . In fact, a statically or pro-
4.1. Extraction process
                                                                          gramatically built prompt prefix might lead to the generation of
   LLM-enabled application proposals can be abstractly charac-            chained transformations during inference-time (and, also, we
terized as software that interacts with LLMs to generate inter-           needed to elucidate actual conceptual signatures embedded into
mediate data or final results. This does not preclude integration         the context). Last but not least, the autoregressive nature of
with classical software tools (compilers, static analyzers, ad-hoc        LLMs–including their potential for step-by-step, inference-time
Deep Learning models, vector databases, etc.) as noted by other           reasoning generation, as demonstrated by Chain-of-Thought ap-
surveys [99].                                                             proaches [252]–may lead to self-generated transformative stages
   We claim that (1) all those LLM based interactions can be un-          that cannot be statically recovered7 . Those transformations are
derstood as a set of “transformations” from some (intermediate)           auto-elicited during runtime to serve higher-level transforma-
inputs to some (intermediate) output, (2) those transformation            tions designed by tool developer– which are the recovering
types, while very rich, can be categorized, and (3) the same can          effort focus. Interestingly, [23] proposes a categorization of sen-
be said about patterns of how transformations are related to solve        tences in CoT trajectories (Problem Setup, Plan Generation, Fact
problems in contemporary literature.                                      Retrieval, Active Computation, Uncertainty Management, Re-
    Figure 1 and Figure 10 exhibit transformations and                    sult Consolidation, Self Checking, and Final Answer Emission)
their interrelationships.       In particular, they depict, as            which could complement our catalog of higher-level developers-
Bayesian Networks [131], the (causal) dependencies of (ran-               guided transformations. As said, there are many means in which
dom/deterministic) conceptual variables in representative ab-             those prompts are built and, potentially, some details might even
stract runs of a couple of solution proposals. The (conditional)          be defined with the help of LLM-based/optimization mecha-
probability distribution of generated data is actually governed           nisms before applications runtime [65, 84, 127, 142, 302]8 .
by either LLM-mechanized or algorithmic “transformations”.                   As said input and output conceptual types were elucidated and
Such a graphical representation serves as a framework guiding             annotated. For reactive transformations (e.g., [281]), the nature
the extraction, identification, and categorization of transforma-         of interactions with the environment (that involve further input
tions –treated as a phenomenon of interest–, particularly those           and output) was also recovered. Input signature was identified
mechanized by LLMs. That is, our first step was to conceptually           by reflecting and discussing carefully about conceptual data that
decompose each solution proposal in the literature in scope by            would be necessary to perform the intended transformation. This
identifying the typology of generative transformations and their          work is relatively easy when prompts sent to LLMs relate 1-to-1
conceptual signatures that the solution leverages. For such aim,          to transformations. As said, when prompts accumulate conver-
we manually analyzed relevant papers and associated reposito-             sation history comprising several transformations this signature
ries to elucidate such discrete functional units. This was done           elucidation is harder: we need to reflect on which data on the
by reading paper descriptions, prompts and algorithms and then            prefix the transformation (conceptually) should be function of.
performing:                                                               That is, in probabilistic terms, output should be conditionally
  1. detection of all potential intermediate and final results that       independent [131]–given the identified input signature–with re-
      would computed by algorithmic manipulation or filled in             spect to the rest of data conveyed in the prompt. Of course,
      by LLMs utterances in representative schematic runs of the          LLM’s mechanisms are opaque, and it could be the case that
      solution proposal (the data variables);                             even conceptually irrelevant data in context, due to the attention
  2. identification of all the elicitation elements (e.g., instruc-
      tions, examples, prefixes, etc.) in prompts that indicate               6 Some role-based agentic presentations or declarative frameworks like [127]

      what is expected as utterances for such intermediate/final          might ease the identification of transformations and signatures, in general, this
      results -our granularity aim;                                       is not trivial.
                                                                              7Yet we do capture transformations suggested by tool developers for the
  3. elucidation of the input signature of such transformations           elicited CoT–a pretty usual practice in papers in scope (e.g., “think step by step,
      in terms of involved data variables that would condition the        first summarize API usage, then ...”).
      generation of utterances;                                               8 Very few were encountered in the literature under review.


                                                                      7
                                       Number of Transformation Types Involved                This sort of descriptors helped us to cluster and categorize
                                  1      2      3     4      5     6     7       8         transformations based on shared functional characteristics. No-
 Testing/Fuzzing                 39%    31%    11%   13%     3%    2%            2%        tation also simplified the elaboration of the taxonomy’s dimen-
 Debugging/Root Cause Analysis   15%    62%    15%     8%                                  sions. It was also key to achieve inter-annotator agreement by
 Vulnerability Detection         61%    15%    15%           6%    3%                      resolving disagreements and inconsistencies via discussion and
 Static Analysis                 33%    11%    11%   22%    22%
                                                                                           refinement.
 Program Verification            20%    50%                 20%                  10%
 Total                           40%    30%    12%     9%    6%    2%            2%        4.2. Results
                                                                                              The following is an illustrative example of transformations
                                                                                           recovered from a couple of solution proposals from different SE
Table 1: Number of transformation types involved in each solution approach.
The analysis is performed for each type of software engineering problem, and               problems: unit test generation [284], fuzzing [268], penetration
the entries of the table express the percentage of solution proposals of that type         testing [51], and vulnerability detection for smart contracts [95].
that feature that number of different types of transformations. When a paper
proposes more than one approach for the same problem, these are considered                  ChatTester [284]:
individually, counting the number of types of transformations involved in each              1. focal meth code → ⟨CodeCorresponding-Intent-Verbalization⟩ → intent
of the approaches.                                                                          2. focal meth sig + intent → ⟨IntentCorresponding-Test-Generation⟩ → unit tests
                                                                                            3. unit test + error msgs → ⟨ErrorAware-Test-Correction⟩ → unit test
                                                                                            Fuzz4All [268]:
                                                                                            1. doc + (examp)∗ + (specs)∗ → ⟨Usage-Summarization⟩ → distilled usage/funct
                                                                                            2. usage/funct → ⟨UsageSastifying-Input-Generation⟩ → fuzz inputs
mechanisms, generates an internal representation that acts as a                             3. usage/funct + fuzz input → ⟨Input-Variation-Generation⟩ → fuzz input
latent variable which might affect the transformation’s distribu-                           PentestGPT [51]:
                                                                                            1. user-intents → ⟨IntentCorresponding-Plan-Generation⟩ → penetration task tree
tion on outputs beyond identified natural signature data. Yet,                                 (ptt)
we believe this identification is crucial since it is worth under-                          2. testing results + ptt → ⟨Elements-Update⟩ → ptt
                                                                                            3. ptt + updated ptt → ⟨Validity-Transition-Analysis⟩ → result
standing, in the future, if those latent variables help or hurt or                          4. ptt → ⟨RulesSatisfying-Information-Extraction⟩ → (potential next task)+
are neutral to the quality of implemented transformations.                                  5. ptt + tasks → ⟨MostPromising-NextTask-Selection⟩ → sugg next task
                                                                                            6. sub-task + avail tools → ⟨ToolsConstrained-Plan-Generation⟩ → seq of steps
   Through this analysis, we systematically identified and, in                                 [CoT]
many cases, defined transformation types as a way to abstractly                             7. step → ⟨Plan-Refinement⟩ → cmd [CoT]
                                                                                            8. raw user intent — test outp → ⟨Summarization⟩ → condensed info
describe what was instructed in prompts found in the literature.                            GPTLens [95]:
Our naming conventions for transformation types were designed                               1. src-code       →       ⟨Rationalized-VulnerabilityProneness-Code-MultiLabel-
                                                                                               Classification⟩ → (vul + funct name + reason)∗ (auditor)
to accurately reflect their fundamental functional nature and                               2. src-code + vul + funct name + reason → ⟨Audits-Qlty(Correctness, Severity,
capture their distinguishing characteristics.                                                  Profitability)-Assessment⟩ → score + explan (critic)

   We abstracted away low-level implementation details (e.g.,
decoding strategies, prompt engineering specifics like word-                                  Colors are indicative of the transformation category as it will
ing [159], etc.) to focus on generalizable transformative in-                              be explained in the next sections. Numbers are later used as sub-
tents and transformations elicited by LLM prompts, enabling a                              indexes when mapping transformations into dimensions choices
clearer identification of commonalities and “functional” varia-                            when taxonomy is presented.
tion points.                                                                                  The outcome of this extraction and naming process for the
                                                                                           initial set of literature in scope can be found in Tables 1–5 in the
   We use a structured naming convention for transforma-
                                                                                           v2 of this preprint [25].
tions. Two parts were mandatory: [Property/Criterion]-
                                                                                              Despite the richness and variety of approaches, we recovered
[Action/transformation type]. The [Action/Transformation] type
                                                                                           from the initial set of 111 reported papers their underlying trans-
describes the fundamental abstract operation being performed
                                                                                           formations (284 in total)9 and presented them homogeneously,
(e.g., Generation, Mutation, OneClass-Classification). [Prop-
                                                                                           no matter sophistication of proposal or how it was reported.
erty/Criterion] describes the conditions, constraints, or goals
                                                                                           Thus, this work provides some evidence that transformation
that are the guiding principles of the transformation. This sets
                                                                                           types, currently, constitute a natural blueprint of what cognitive
the rationale or intended effect (e.g., IntentCorresponding in
                                                                                           capabilities are being leveraged in an LLM-enabled approach,
IntentCorresponding-Code-Generation, CoverageAugmenting
                                                                                           at least for contemporary solution proposals for software testing
in CoverageAugmenting-Test-Generation, VulnerabilityProne-
                                                                                           and verification problems.
ness in VulnerabilityProneness-Code-OneClass-Classification,
                                                                                              Table 1 summarizes the distribution of problem decomposi-
etc.). In most cases, we also added as an additional descriptor
                                                                                           tion complexity of solution proposals measured as the number
the type of artifact being produced, modified or analyzed. This
                                                                                           of different types of transformations elicited per proposal. So-
artifact could refer to the type of object that the transforma-
                                                                                           lution proposals are grouped according to software engineering
tion yields as a way to subtype generative actions (e.g. Test
                                                                                           problem addressed. A paper might propose more than one solu-
in CoverageAugmenting-Test-Generation, Invariant-Lemma in
                                                                                           tion. This is particularly the case of seminal exploratory works
Invariant-Lemma-Generation) or the type of object subject to
                                                                                           which analyze the proficiency of models when prompted for
the transformation (e.g.Code in VulnerabilityProneness-Code-
                                                                                           a studied SE task. That explains the higher concentration of
OneClass-Classification) according to what we believe was more
relevant to make the transformation description more informa-
tive.                                                                                         9 Some recurring ones.


                                                                                       8
1-transformation approaches particularly in unit test generation
and vulnerability proneness classification, SE categories that en-
compass several validation research papers. Having said that, we
can see that the majority of LLM-enabled solution proposals re-              Transformation Taxonomy

quire two or more types of transformation, typically interrelated.              Generative
Inter-transformation patterns in section 7 many times explain                      Code Generation
the reasons for the existence of designs featuring more than one                       General-Code Generation (Figure A.11)
                                                                                       E.g. IntentCorresponding-Code-Generation
transformation type in solution proposals. For instance, a large                       Domain-Specific-Code Generation (Figure A.12)
number of the 2-transformation approaches actually feature a                           E.g. InputGenerator-Generation, DriverCode-Generation/Correction
                                                                                       Test Generation (Figure 5)
generative transformation followed by a corrective stage (see
                                                                                       E.g. Basic&Edge-TestCase-Generation, CoverageAugmenting-Test-Generation
Generate and Fix). Also, approaches for SE problems differ                         Annotation Generation (Figure A.13)
in complexity. For instance, while testing and fuzzing exhibit a                   E.g. Assertion-Generation, Invariant-Lemma-Generation
                                                                                   Data Generation (Figure A.14)
similar distribution of the entire population, static analysis pro-                E.g. ConstraintSatisfying-Input-Generation, Basic&Edge-TestInput-Generation
posals seem to require a larger number of transformations. That                 Evaluative
is, even if many approaches leverage in low-level transforma-                      SW-Entity Analysis
                                                                                       Behavior Analysis (Figure A.15)
tions dynamically elicited during thought trajectories, non-trivial                    E.g. RootCause-Analysis, Behavior-Anomaly-Detection
problem decomposition into two or more transformations and                             Code Analysis
architecture is statically identifiable. That is, for many SE prob-                          Code Classification
                                                                                               Direct Code-Classification (Figure A.18)
lems covered by this report, it seems that ingenious problem                                   E.g. VulnerabilityProneness-Code-OneClass-Classification
decomposition and some degree of tool orchestration is currently                               Rationalized Code-Classification (Figure 6)
                                                                                               E.g. Rationalized-VulnerabilityProneness-Code-MultiLabel-Classification
necessary, possibly because it has not been observed yet break-                            Code Scaling (Figure A.17)
through behavior [214] that would enable solving the actually                              E.g. CVSS-Scoring, VulnerabilityProneness-Code-MultiLabel-Soft-Classification
required end-to-end transformation as a single one. This phe-                              Line Code-Ranking (Figure A.16)
                                                                                           E.g. FaultProneness-CodeLines-Ranking
nomenon has been also dubbed “the compositional gap” in the                            Task-Solution Analysis (Figure A.19)
NLP literature [195] . This topic is revisited in detail in section 7.                 E.g. Self-Validation, Answer-Quality-Assessment
                                                                                   Text Analysis (Figure A.20)
In a few words, the number of transformations involved is the                      E.g. Docstrings-Equivalence-Checking, Ambiguity-Analysis, EvidenceSupport-Judgment
result of two antagonist forces: the sophistication of the goals of             Extractive
LLM-native applications and the ability of LLM to proficiently                     SW-Entity Extraction
                                                                                       Code-Elements Identification & Extraction (Figure A.21)
solve higher-level transformations with a single instruction.                          E.g. CodeElements-Identification, CodeBlocks-Extraction, Model-Slicing
   Identified transformations are rich in nature and functional                    Text-Elements Identification & Extraction (Figure A.22)
features and, to the best of our knowledge, most of them were                      E.g. VariableNames-Identification, StructureCompliant-Information-Extraction
                                                                                Abstractive
not previously contained in existing taxonomies or benchmarks.                     SW-Entity to NL
They possibly fall somewhere in between open-ended and di-                            SW-Entity Verbalization (Figure 7)
                                                                                      E.g. CodeCorresponding-Intent-Verbalization, Summarization
rected generation tasks [88]. Next section will provide an                         NL to SW-Entity
overview of type categories by means of the taxonomy we elab-                         Formalization (Figure A.24)
orated.                                                                               E.g. PostCondition-Formalization
                                                                                   SW-Entity to NL / NL to NL
                                                                                       SW-Entity-Property Identification & Characterization (Figure A.23)
                                                                                       E.g. VariablesSameValue-Identification, TaintFlow-Identification
5. Transformation taxonomy
                                                                                   NL to NL
                                                                                       Focused-Abstractive Summarization (Figure A.25)
   The proposed taxonomy results from our initial best effort to                       E.g. RootCauseOriented-Summarization, Assessment-Yes/No-Summarization
cluster, brand, and rationalize transformation types implemented                Executive
                                                                                   Planning
by prompts and conversations reported in the reviewed literature.
                                                                                      Plan Generation (Figure 8)
Our taxonomy is organized hierarchically: a directed tree of                          E.g. ScenarioCorresponding-Plan-Generation, Plan-Refinement
transformation classes, being the types closer to the root the                     Decision Making
                                                                                       What-to-do-Next Generation (Figure A.26)
most general ones (Transformation Categories). Specificity is                          E.g. ReachabilityOriented-NextAction-Generation
expressed in two different ways: either by “subtyping” using di-                   High-level Instruction Following
rected edges in top levels of the taxonomy (see Figure 3) and, for                     Execution (Figure A.27)
                                                                                       E.g. Step-Computation, Trace-Execution
more concrete levels of the taxonomy (Transformation Classes),                         Textual Data Manipulation (Figure A.28)
types came up as combinations of choices of the identified di-                         E.g. CFG-Fusion, InListCloseMeaning-Elements-Replacement
                                                                                Consultative
mensions (that is, externally-visible variation points) as a way                   Knowledge Distillation (Figure A.29)
to capture the specificity of the transformation being proposed                    E.g. Example-Recall, Definition-Recall, ProtocolGrammar-Recall
by the analyzed studies (Figs. 5–8 and A.11–A.29).
   The initial rationale for the taxonomy is to highlight com-               Figure 3: Taxonomy based on the transformation types found in the reported
monalities between transformations requested by prompts while                papers.
preserving the richness of some relevant details. Taxonomy is
also meant to be “useful” in helping identify some patterns of
use of LLMs and prompting and also making explicit some less
                                                                         9
explored (or unexplored) transformation types. Ultimately, tax-                                                                                                                           The classification criterion is that the main generated output
onomy might also help to understand how to leverage warnings                                                                                                                              must be a software entity (SW-entity). This category is subdi-
and advances of the natural language generation community                                                                                                                                 vided by artifact type: code (Figs .A.11, A.12), tests (Figure 5),
(e.g., [162]) to build LLM-enabled applications in a principled                                                                                                                           code annotations (Figure A.13), and data (Figure A.14). Code
way (see section 10).                                                                                                                                                                     generation is further distinguished by whether the functional-
                                                                                                                                                                                          ity is predetermined (domain-specific, e.g., fuzzing drivers) or
     Knowledge Distillation       1                       5
                                                                                                                                                                    ReAct
                                                                                                                                                                                          emergent from input parameters (general).
 Textual Data Manipulation        1                   4                                                                                                             FS+ReAct
                 Execution        1               3                                                                                                                 RAG
     What-to-do-Next Gen          1                   4                                                                                                             FS+RAG                Evaluative. Evaluative transformations analyze properties of
                                                                                                                                                                    Few-Shot
                  Plan Gen            2               2                   3                           4                           5
                                                                                                                                                                    FS+CoT
                                                                                                                                                                                          input software entities, producing judgments, scores, or qual-
 Focused-Abstractive Summ         1       1       1                                   8

 SW-Entity Prop Id & Char                         5                               3               1                 4
                                                                                                                                                                    CoT
                                                                                                                                                                    ToT
                                                                                                                                                                                          itative assessments. The classification criterion requires the
            Formalization
   SW-Entity Verbalization
                                  1

                                              4
                                                  3

                                                                                                                        15
                                                                                                                                                                    CoT+ReAct
                                                                                                                                                                    FS+CoT+ReAct
                                                                                                                                                                                          output to be conceptually analytical rather than generative. Sub-
   Text-Elements Id & Extr                3               1       1           2                                                                                     RAG+CoT+ReAct         categories are defined by output characteristics: direct classi-
  Code-Elements Id & Extr             2               2                   3               1       1             3                                                   None
            Text Analysis             2           1                       5                                                                                                               fication (categorical labels without justification, akin classical
     Task-Solution Analysis
        Line Code-Ranking
                                  1

                                      2
                                          1

                                                  1
                                                                          7
                                                                                                                                                                                          discriminative ML tasks [144, 29], Figure A.18), rationalized
              Code Scaling                3                                                                                                                                               classification (judgments with natural language explanations,
  Rationalized Code-Classif       1                       5                                   4                         3                             8

        Direct Code-Classif       1       1           2           1           2                                              11
                                                                                                                                                                                          Figure 6), scaling/ranking (numerical or ordinal assessments,
         Behavior Analysis            2           1       1       1                                   8
                                                                                                                                                                                          Figs. A.17, A.16), behavior analysis (assessment of satisfac-
                 Data Gen                                 7                               1                                       11

           Annotation Gen             2           1                   4                   1       1                                    10                                                 tion of dynamic properties from behavioral descriptions, Fig-
                  Test Gen
 Domain-Specific-Code Gen         1
                                              4

                                                  3
                                                                  1

                                                                                                          11
                                                                                                                                                 22
                                                                                                                                                                                          ure A.15), task-solution analysis (evaluation of other transfor-
         General-Code Gen         1           2                                                                                             24
                                                                                                                                                                                          mations’ outputs, Figure A.19), and text analysis (general NL
                              0               2               4               6               8            10               12
                                                                                                      Number of Downstream Tasks
                                                                                                                                      14         16       18   20     22   24   26
                                                                                                                                                                                          assessment, Figure A.20).

                                                                                                                                                                                          Extractive. Extractive transformations identify and retrieve spe-
                                                                                                                                                                                          cific elements from larger contexts without significant abstrac-
Figure 4: Number of transformations using each prompting technique or combi-
                                                                                                                                                                                          tion or reformulation. The classification criterion is verifiable
nation of prompting techniques, aggregated by transformation category.
                                                                                                                                                                                          by checking whether output elements exist verbatim or near-
                                                                                                                                                                                          verbatim within the input. This category includes code ele-
   Our taxonomy was deliberately designed to be extensible
                                                                                                                                                                                          ment identification (Figure A.21) and text extraction operations
along two complementary dimensions. First, intra-category
                                                                                                                                                                                          (Figure A.22), where the transformation performs location and
extensibility: within each category of transformations, new prop-
                                                                                                                                                                                          retrieval rather than synthesis.
erties and options can be incorporated to capture emerging types
of generative transformations without disrupting the existing                                                                                                                             Abstractive. Abstractive transformations construct higher-level
structure. This ensures that the taxonomy can evolve as LLM-                                                                                                                              representations through synthesis, summarization, or formaliza-
native practices diversify. Second, cross-domain extensibility:                                                                                                                           tion. The classification criterion requires that outputs cannot be
while this work focuses on software entities in the domain of                                                                                                                             found verbatim in inputs and represent conceptual abstractions.
verification and falsification, the same organizing principles can                                                                                                                        Subcategories include verbalization (converting SW-entities to
accommodate new categories of transformations in other do-                                                                                                                                natural language descriptions, Figure 7), formalization (produc-
mains (e.g., legal document generation, scientific writing). We                                                                                                                           ing formal specifications, Figure A.24), property characteriza-
thus view the taxonomy not as a fixed classification, but as a                                                                                                                            tion (identifying abstract properties, Figure A.23), and focused
scaffold for reasoning, intended to adapt and expand as new                                                                                                                               abstractive summarization (NL summarization tasks [200], Fig-
classes of transformations and patterns are observed.                                                                                                                                     ure A.25).
   The top-level branching in the taxonomy responds to identify-
ing different high-level conceptual operations being performed.                                                                                                                           Executive. Executive transformations produce operational in-
Those actions typically require, for humans, different cognitive                                                                                                                          structions for goal-directed behavior. The classification criterion
abilities and, for the “pre-LLMs era”, have involved different re-                                                                                                                        is met when outputs specify actions, plans, or state transitions
search communities and used quite different theories, algorithms,                                                                                                                         rather than static artifacts. This encompasses plan generation
and/or training approaches. For instance, distinguishing gener-                                                                                                                           (creating operational sequences, Figure 8), decision-making
ation vs. evaluation of a software entity–although being both                                                                                                                             (selecting next actions, Figure A.26), and instruction follow-
solved by generative utterances–is in line with the perception of                                                                                                                         ing [101] (executing imperative operations, Figs. A.27, A.28).
two different human tasks, problem hardness, different perfor-
mance evaluation methods, and different existing SE-tool cate-                                                                                                                            Consultative. Consultative transformations retrieve and present
gories. As we will show later, categories were initially leveraged                                                                                                                        information from the model’s pre-trained parameters on a given
to detect design patterns, pinpoint opportunities, and to highlight                                                                                                                       subject without relying on provided context [236]. The classi-
commonalities and differences between SE approaches.                                                                                                                                      fication criterion requires that the prompt segment eliciting the
                                                                                                                                                                                          transformation does not contain the answer at all nor an input
Generative. Generative transformations are defined by their pri-                                                                                                                          to process, necessitating recall of compressed knowledge like
mary function: creating or modifying existing software artifacts.                                                                                                                         definitions, specifications, or guidance (Figure A.29).
                                                                                                                                                                                     10
                                                                                                       Rationalized Code-Classification
    Figure 4 indicates both the number of transformations
mapped into each category and some proxy indication on how                                                Analysis criteria
challenging was for authors to implement the expected behavior                                               Vulnerability proneness: EditTime3 [30], EditTime4 [30], SmartAudit2 [48], SmartAudit3 [48],
                                                                                                                                      VulBench [71], GPTLens1 [95], VulDetect1 [125], VulDetect2 [125],
by indicating the used prompting strategy/strategies.                                                                                 LATTE4 [148], VSP1 [181], VSP2 [181], LLM4Vuln3 [219],
                                                                                                                                      LLM4Vuln3w/PreCoT [219], LLM4Vuln3w/PostCoT [219], DLAP3 [278]
                                                                                                                 Null-dereference: SkipAnalyzer1 [171]
5.1. Dimensions of transformation classes                                                                        Leak presence: SkipAnalyzer2 [171]
   Figures 5–8 provide examples of how transformation subtypes                                                   Data-flow CWI: VulDetect3 [125]
                                                                                                                 Entity inconsistency: WitheredLeaf 1 [35]
for a specific category are defined using property dimensions and                                            Malware proneness: Sleuth2 [260]
choices. They also show how the relevant studies are mapped                                                  Fixability analysis
                                                                                                                 Rename: WitheredLeaf 3 [35]
onto these choices, which are represented as the leaves of the                                            Nature of classification
decision trees. The featured choices are those actually observed                                              Multiplicity
                                                                                                                 OneClass (Binary): EditTime3 [30], EditTime4 [30], WitheredLeaf 1 [35],
in our analysis; however, for some dimensions, more choices                                                                         WitheredLeaf 3 [35], SkipAnalyzer1 [171], SkipAnalyzer2 [171],
are naturally possible. This potential for unobserved choices is                                                                    VSP2 [181], Sleuth2 [260], DLAP3 [278]
                                                                                                                 MultiLabel
a key feature of this representational method.                                                                        Open-ended: SmartAudit2 [48], SmartAudit3 [48], GPTLens1 [95],
                                                                                                                      Close-ended: ChatGPTSCV1 [34], VulBench [71], VulDetect1 [125], VulDetect2 [125],
Test Generation                                                                                                                      VulDetect3 [125], LATTE4 [148], VSP1 [181],
                                                                                                                           In-context defined classes: LLM4Vuln3 [219], LLM4Vuln3w/PreCoT [219],
   Generation criteria                                                                                                                                 LLM4Vuln3w/PostCoT [219]
      Differential: MuTAP3 [47]                                                                           Analysis granularity
      Natural: FSMLUTG [17], ChatGPTTests1 [22], ChatUniTest1 [39], MuTAP1 [47],                              Snippet: EditTime3 [30], EditTime4 [30], ChatGPTSCV1 [34], SmartAudit2 [48],
                  DiffPrompt3 [140], TestPilot [204], EASEeval [212], LLM-UTG [277]                                     SmartAudit3 [48], VulBench [71], GPTLens1 [95], VulDetect1 [125],
             Bug revealing: FuzzGPT4 [54]                                                                               VulDetect2 [125], VulDetect3 [125], LATTE4 [148], SkipAnalyzer1 [171],
        Coverage improving: TestGen-LLM [8], ChatGPTTests2 [22], CoverUp1 [192],                                        SkipAnalyzer2 [171], VSP1 [181], VSP2 [181], LLM4Vuln3 [219],
                              CoverUp2 [192], TELPA [272]                                                               LLM4Vuln3w/PreCoT [219], LLM4Vuln3w/PostCoT [219], DLAP3 [278]
        Targeted: CodaMOSA [136]                                                                              Line: WitheredLeaf 1 [35], WitheredLeaf 3 [35]
        Intent corresponding: CodeT [33], CodeCoT [97], AgentCoder [98], ChatTester2 [284]                Extra input
        Parameterized: PBT-GPT3 [240]                                                                         Code intent: SmartAudit3 [48], LLM4Vuln3w/PreCoT [219], Sleuth2 [260]
        Property based: PBT-GPT4 [240]                                                                        Taint-info: LATTE4 [148]
        Similarity inspired: FuzzGPT3 [54]                                                                    Review guidance: DLAP3 [278]
        Mimicking test: secTests [298]                                                                    Corrective mode
        Bug reproducing: LIBRO [122]                                                                          Self-validation: VulDetect3 [125]
   In-filling context                                                                                     Reactivity
        Given prefix: FuzzGPT4 [54]                                                                           Request further information: LLM4Vuln3 [219], LLM4Vuln3w/PreCoT [219],
   Corrective mode                                                                                                                          LLM4Vuln3w/PostCoT [219]
       Feedback based                                                                                     Rationalization
           Compilation errors: ChatUniTest2 [39], MuTAP2 [47], CoverUp2 [192], TestPilot [204],               Assessment/description: ChatGPTSCV1 [34], VulDetect1 [125], VulDetect2 [125],
                               ChatTester3 [284]                                                                                       VulDetect3 [125], LATTE4 [148], SkipAnalyzer1 [171],
           Assertion failure: ChatUniTest2 [39], TestPilot [204], ChatTester3 [284]                                                    SkipAnalyzer2 [171], VSP2 [181]
           Examples to augment: TELPA [272]                                                                   Thought step by step: ChatGPTSCV1 [34], VulBench [71], SkipAnalyzer1 [171],
           Coverage info: CoverUp1 [192], CoverUp2 [192]                                                                              SkipAnalyzer2 [171], VSP1 [181], VSP2 [181], Sleuth2 [260]
   Rationalization                                                                                            Reason: GPTLens1 [95], VulDetect1 [125], VulDetect2 [125], VulDetect3 [125],
       Bug description: FuzzGPT3 [54]                                                                                   LLM4Vuln3 [219], LLM4Vuln3w/PreCoT [219], LLM4Vuln3w/PostCoT [219],
                                                                                                                        DLAP3 [278]
                                                                                                              Fix: WitheredLeaf 3 [35], (SmartAudit3 [48]), LLM4Vuln3w/PostCoT [219]
                             Figure 5: Test Generation. .                                                     Exploit: LLM4Vuln3w/PostCoT [219]


   Transformation types (or subclasses) are defined by means of                                                            Figure 6: Rationalized Code-Classification.
choices in different dimensions to abstractly capture the func-
tional and externally visible nature of transformations underlying
prompting strategies in an attempt to separate the “what” from                                         Granularity Nature of Classification in evaluative transforma-
the “how”.                                                                                             tions, Nature of Property in Property Identification, etc.), some
   Each class exhibits dimensions (variation points) in which                                          are common to several classes (e.g., Nature of (generated) Entity,
choices define potential subclasses of transformations. Also,                                          (generation/analysis/correctness) Criteria, (problem) Domain),
in each class leaf, we map transformations that appear in solu-                                        and a few are applicable, in principle, to all categories: Rational-
tion proposals that feature the given choice denoted by the leaf.                                      ization, Reactivity, and Corrective feedback. In-filling context
Colors indicate the corresponding SE problem in Figure 2, and                                          stands for a transformation’s assumed precondition regarding
sub-indexes indicate different transformations performed by the                                        to which extent and how the container context of the expected
same solution proposal or exploratory study, ordered as they                                           solution is provided and related to it. Rationalization stands for
appear in Tables 1–5 in v2 of this preprint [25].                                                      the nature of verbalized thoughts/explanations/argumentation
   As it can be observed, choices for correctness or preference                                        the transformation is supposed to generate (many times, in a
criteria are one of the main properties that define the subclass                                       Chain-of-Thought generation stream). Note that we consider
of transformation. This is, naturally, the major variation point                                       CoT not only a way to elicit improved inference but also a po-
in transformation classes. Yet, some other dimensions define                                           tentially externally visible output of transformations. In fact,
crucial details of the nature/properties of transformations. As                                        rationalizations could be consumed by humans or other models
mentioned above, more specific transformation types of a class                                         to assess yielded results. Defining a transformation as reactive
are described employing those, potentially orthogonal, dimen-                                          implies that abstractly may not be simply understood as a simple
sions. While some are specific to a transformation class (e.g.                                         input-output function but as an (adaptive) goal-oriented trajec-
                                                                                                  11
SW-Entity Verbalization                                                                             Plan Generation

   Abstraction criteria                                                                                Generation criteria
      Summary: PentestGPT8 [51], LLM4Vuln1 [219], HITS1 [249]                                             Intent corresponding: PentestGPT1 [51]
      Intent: SmartAudit3(CoT) [48], DiffPrompt1 [140], Clover4 [217], Clover7 [217],                     Scenario corresponding: Pwn’d1 [82]
              LLM4Vuln1 [219], LLM4Vuln3(PreCoT) [219], LLMAPIDet1 [253], LLMAPIDet2 [253],               Achieve goal: AlloyRepair3 [4], TARGET1 [52], TARGET2 [52], LLM4Vuln3(exploit) [219],
              ChatGPT-4(Log)1(CoT) [266], RustProof 1(CoT) [279],                                                         AXNav1 [222]
              ChatTester1 [284], PromptEnhanced1 [287]                                                         Constrained
      Explanation: SELF-DEBUGGINGOP1 [37], SELF-DEBUGGINGOP3 [37], Skyeye2 [245]                                   Available tools: PentestGPT6 [51]
                     Sleuth1 [260], RustProof 1(CoT) [279], RustProof 2(CoT) [279]                         Fusing: SysKG-UTF3 [215]
      Differences: ClarifyGPT3 [173]                                                                       Refinement/Concretization: PentestGPT7 [51], AdbGPT2 [64], SysKG-UTF2 [215],
      Problem solving steps: HITS3 [249]                                                                                               SysKG-UTF4 [215], AXNav2 [222], DLAP2 [278]
   Nature of input entity                                                                              Domain
      Intent: PentestGPT8 [51]                                                                             SW review: DLAP2 [278]
      Code: SELF-DEBUGGINGOP1 [37], SELF-DEBUGGINGOP3 [37],                                                SW-system integration: PentestGPT1 [51], PentestGPT6 [51], PentestGPT7 [51],
              SmartAudit3(CoT) [48], DiffPrompt1 [140], ClarifyGPT3 [173], LLM4Vuln1 [219],                                         AdbGPT2 [64], Pwn’d1 [82], SysKG-UTF2 [215],
              LLM4Vuln3(PreCoT) [219], HITS1 [249], HITS3 [249], Sleuth1 [260],                                                     SysKG-UTF3 [215], SysKG-UTF4 [215], LLM4Vuln3(exploit) [219],
              ChatGPT-4(Log)1(CoT) [266], ChatTester1 [284], PromptEnhanced1 [287]                                                  AXNav1 [222], AXNav2 [222], AXNav4 [222]
           Commit: VulAdvisor [290]                                                                        Repair: AlloyRepair3 [4]
           Annotated: Clover4 [217], RustProof 1(CoT) [279], RustProof 2(CoT) [279]                        Physical: TARGET1 [52], TARGET2 [52]
       Call sequences: Skyeye2 [245]                                                                   Nature of output
       Report: LLM4Vuln1 [219]                                                                             Step-by-step plan: AlloyRepair3 [4], PentestGPT6 [51], TARGET1 [52], TARGET2 [52],
       Testing outputs: PentestGPT8 [51]                                                                                      Pwn’d1 [82], SysKG-UTF2 [215], SysKG-UTF3 [215],
       Assertion: Clover7 [217]                                                                                               SysKG-UTF4 [215], LLM4Vuln3(exploit) [219], AXNav1 [222],
           Precondition: RustProof 1(CoT) [279], RustProof 2(CoT) [279]                                                       AXNav4 [222], DLAP2 [278]
           Postcondition: RustProof 2(CoT) [279]                                                           Hierarchical plan: PentestGPT1 [51]
       Change action: LLMAPIDet1 [253]                                                                     Command/Action: PentestGPT7 [51], AdbGPT2 [64], AXNav2 [222]
   Extra input                                                                                         Corrective mode
       Execution: SELF-DEBUGGINGOP3 [37]                                                                   Feedback based
       Attack type: Skyeye2 [245]                                                                              Outcomes: PentestGPT1 [51], AXNav4 [222]
       Data flow: Sleuth1 [260]                                                                            Rule based: TARGET2 [52]
                                                                                                       Reactivity
                                                                                                           Tool invocation: PentestGPT1 [51], Pwn’d1 [82]
                          Figure 7: SW-Entity Verbalization.                                           Rationalization
                                                                                                           Thought: PentestGPT1 [51], PentestGPT7 [51], AdbGPT2 [64], AXNav1 [222],
                                                                                                                     AXNav2 [222]
                                                                                                           Assessment: SysKG-UTF4 [215]
tory of inputs and outputs. In fact, underlying LLM needs to                                               Pseudo-code guided assessment: SysKG-UTF3 [215]
proficiently interact with its environment to achieve the transfor-
mation’s goal [281, 205]. Thus, Reactivity choices describe how                                                                  Figure 8: Plan Generation.
a transformation is supposed to interact with its environment to
achieve its goal. For instance, reactive behavior allows a sys-
tem to incrementally request missing information. Conversely,                                      That is, they are typically not broken down into several transfor-
using external tools (e.g., symbolic systems) can enhance perfor-                                  mations.
mance by feeding intermediate results back into the step-by-step                                      Input generation approaches use LLMs differently. Typically,
inference process of a transformer model.                                                          they seem to elicit abstractive generation for verbalized charac-
   Finally, Corrective feedback dimension stands for choices                                       terization of desired input. Something similar happens to fuzzing
for transformations that are meant to correct/repair or improve                                    approaches that aim to trigger some specific software behavior.
yielded result based on new evidence (see pattern Generate                                         They do not rely on a single staged transformation to get data or
and Fix). When a transformation is requested with corrective                                       input. Section on patterns digs into more detail on this.
feedback it could be argued it becomes a version of the original                                      On the other hand, functional testing, GUI testing, penetra-
transformation in which the elicited generation is cognitively                                     tion testing and, in general, system-level testing have a strong
closer to fixing a given solution. Nevertheless, at least this                                     usage link with executive transformations (e.g., plan generation,
transformation is considered a version of the original one in                                      decision making, etc.). In fact they would be the main “clients”
which hints/feedback are also given to achieve goals.                                              for language models featuring strong planning abilities.
                                                                                                      Fuzzing, particularly when inputs are programs (e.g., DL-
6. Mapping studies into the taxonomy                                                               fuzzing and compiler fuzzing), is the main “client” of code
                                                                                                   generation transformations. Programs that are requested to be
   The following are conclusions drawn from Tables and Trees,                                      generated are typically small, and that, together with the per-
and from the prompt techniques used by each transformation                                         ceived native ability for such transformations, might explain
class, which are summarized in Figure 4.                                                           why design patterns and prompting strategies to transformation
                                                                                                   elicitation are rather straightforward.
6.1. SE Problems and the use of Transformations                                                       Vulnerability detection constitutes another rather homoge-
   In what follows, we draw preliminary conclusions regarding                                      neous SE problems cluster regarding transformation categories
several aspects of the relationship between SE problem cate-                                       involved (mostly evaluative). Smart contract analysis, which
gories and transformation categories (see Figure 9 and Table 2).                                   often seeks logical vulnerabilities, leverages rationalized clas-
Firstly, unit testing approaches are rather homogeneous regard-                                    sification more frequently than general vulnerability analysis,
ing using generative classes of transformations that are straight-                                 which is more oriented to detect code patterns.
forwardly traceable to the final SE problem being addressed.                                          Oracle problems, debugging, and static analysis are SE prob-
                                                                                              12
                                                                                                                           Table 2: Relation between SE problems and transformation taxonomy.




                                                                                                                                                                                                                                                                                                                                                                                                                                                                           SW-Entity Property Id. & Char.




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        What-to-do-Next Generation
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            Focused-Abstractive Summ.
                                                                             Domain-Specific-Code Gen.




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Textual Data Manipulation
                                                                                                                                                                                                                                    Rationalized Code-Classif.
                                                                                                                                                                                                       Direct Code-Classification




                                                                                                                                                                                                                                                                                                                                                            Code-Elements Id. & Extr.
                                                   General-Code Generation




                                                                                                                                                                                                                                                                                                                                                                                        Text-Elements Id. & Extr.




                                                                                                                                                                                                                                                                                                                                                                                                                                 SW-Entity Verbalization
                                                                                                                            Annotation Generation




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         Knowledge Distillation
                                                                                                                                                                                                                                                                                                    Task-Solution Analysis
                                                                                                                                                                                                                                                                                Line Code-Ranking
                                                                                                                                                                                   Behavior Analysis
                                                                                                                                                    Data Generation




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Plan Generation
                                                                                                         Test Generation




                                                                                                                                                                                                                                                                                                                                                                                                                                                           Formalization
                                                                                                                                                                                                                                                                 Code Scaling




                                                                                                                                                                                                                                                                                                                               Text Analysis




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    Consultative
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        Abstractive
                                                                                                                                                                      Generative




                                                                                                                                                                                                                                                                                                                                               Evaluative




                                                                                                                                                                                                                                                                                                                                                                                                                    Extractive




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     Execution




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             Executive




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Total
Unit Test Generation                                                                                      17                                               1           18                                                                                                                                                                                                                                                                   1                                                                                                1                                                           1                                       1                                                 20
Failure-Inducing Test Generation                              2                          1                      2                                                          5                                                                                                                                                                                                                                                                1                                                                                                1                                                                                                                                                       6
Input Generation                                                                         2                      2                     1                    3               8                                                                                                                                   1                                    1                                                                                                                                     3                                                  3                                                                                                                                                     12
Regression Testing                                                                                                                                         1               1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         1
DataSet/Mutant Generation                                     6                                                 3                                                          9               1                                                                                                                                                        1                                                                                                                                                                                                                                                                                                                                              10
General Fuzzing                                                                          4                                                                 4               8                                                                                                                                                                                                                                                                1                                                                                                1                                                                                                                                                       9
Kernel Fuzzing                                                                                                                        1                                    1                                                                                                                                                                                            4                                                4                                                                                                                                                                                                                                                                           5
Compiler/Simulator Fuzzing                                    1                                                                                            2               3                                                                                                                                                                                                                                                                                                              1                                                  1                                                                                                                                                       4
Protocol/Parser Fuzzing                                                                                                                                    3               3                                                                                                                                                                                                                                                                                                                                                                                                                                                 1                   1                  4                     4          8
DL-Libraries Fuzzing                                          3                                                 2                                                          5                                        1                                                                                                                               1                                                                                                                                                                                                                                                                                                                                                6
GUI Testing                                                                                                                                                2               2               2                                                                                                                                                        2                                                                                                                                                                                                        3                       1                                                           4                                                   8
Functional Testing                                                                       1                                                                 1               2                                                                                                                                                         2              2                                               1                    1                                                                                              1                    1               5                                                               1                   6                                                 12
Penetration Testing                                                                                                                                                                        2                                                                                                                                                        2                                                                                       1                                                                                                1               4                       2                                       2                   8                                                 11
Oracle Problem                                                2                          2                                            6                    2           12                  1                        1                                                                                                                2              4                                               3                    3                  4                    1                        3                             2                10                                                              1                                       1                                                 30
Testing                                              14                        10                         26                          8              19                77                  6                        2                                                                                          1                     4         13                       4                           4                    8                  8                    1                        7                             3                19            12                            3                   2                   4               21                     4                     4        142
Bug Reproduction                                                                                                1                                                          1                                                                                                                                                                                                                        1                    1                                                                                                                                   1                       2                                                           3                                                   5
Duplicate Bug Report Detection                                                                                                                                                                                                                                                                                                                                                                      1                    1                                                                                                                                                                                                                                                                           1
Fault Localization                                            2                                                                                                            2               3                                                                                            2                                            1              6                                                                                       1                                                                           1                    2                                                           1                                       1                                                 11
Root Cause Analysis                                                                                                                                                                        3                                                                                                                   1                     2              6                                               1                    1                                                                                              5                    5                                                                                                                                                     12
Debugging                                                     2                                                 1                                                          3               6                                                                                            2                      1                     3         12                                                   3                    3                  1                                                                           6                    7               1                       2                   1                                       4                                                 29
Vulnerability Detection                                                                                                                                                                                  11                                      7                     3                1                      1                               23                                                                                           1                                                                                                1               1                                                                                   1                                                 25
Line-Level/Edit-Time Fault/API Misuse Prediction              2                                                                                                            2                                        2                            4                                                             1                                    7                                                                                       2                                                                                                2                                                                                                                      2                     2        13
Vulnerability Detection for Smart Contracts                   1                                                                                                            1                                        3                            7                                                             1                               11                       1                                                1                  4                                                                           1                    5               1                                                                                   1                                                 19
Vulnerability/Misuse/Malware/Fault Detection                  3                                                                                                            3                             16                           18                               3                1                      3                               41                       1                                                1                  7                                                                           1                    8               2                                                                                   2                  2                     2        57
Call-Graph/CFG Construction                                                                                                                                                                                                                                                                                                                                             2                                                2                                                                1                                                  1                                                                               1                   1                                                   4
Use Before Initialize                                                                                                                                                                                                                                                                                          2                                    2                   1                                                1                                                                2                                                  2                                                                                                                                                       5
Resource Leak                                                                                                                                                                                                                                    2                                                             1                                    3                   1                                                1                                                                                                                                                                                                                                                                           4
Data-Flow Analysis                                                                       4                                                                                 4                                                                                                                                                                                                                                                                                                              1                                                  1                                                                                                                                                       5
Taint Analysis                                                                                                                                                                             1                                                     1                                                                                                  2                   2                                                2                                                                1                                                  1                                                           1                                       1                                                   6
Static Slicing                                                                                                                                                                                                                                                                                                                                                          1                                                1                                                                                                                                                                                                                                                                           1
Fix Acceptance Check                                                                                                                                                                                                                                                                                           1                                    1                                                                                                                                                                                                                                                                                                                                                1
Static Analysis                                                                          4                                                                                 4               1                                                     3                                                             4                                    8                   7                                                7                                                                5                                                  5                                                           1                   1                   2                                                 26
Program Verification                                          8                          1                                    11                                       20                                                                                                                                                            1              1                                                                                       4                    3                        1                                                  8               1                                                                                   1                                                 30
Program Verification                                          8                          1                                    11                                       20                                                                                                                                                            1              1                                                                                       4                    3                        1                                                  8               1                                                                                   1                                                 30
Total                                                27                        15                         27                  19                     19               107           13                   18                           21                               3                3                      9                     8         75             12                                    7               19             20                            4           13                               10                         47            16                            5                   4                   5               30                     6                     6        284




lems for which existing solutions tend to use a wide spectrum of
transformation categories.
    Extractive transformations such as code element identification                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Generative

are highly linked to static analysis (LLM-enabled) approaches.                                                                                                                                                                                                                                                               Testing

Indeed, the only testing approach that uses such ability is a
kernel-fuzzing approach [275] that uses extractive operations to
fill-in a sort of specification later used for generating relevant
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  Evaluative
system calls. The other exception is [220], which tries to locate                                                                                                                                                                                                                                                            Debugging
code playing a certain role for later static analysis. On the other
hand, extractive operations on Natural Language are elicited by                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Extractive
                                                                                                                                                                                                                                                                                                                             Vulnerability/Misuse/Malware/Fault Detection
approaches addressing debugging, functional testing, and oracle
problems.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Abstractive

    Program verification approaches may blend SW-entities gen-                                                                                                                                                                                                                                                               Static Analysis

erative transformations with verbalization and formalization.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Executive
                                                                                                                                                                                                                                                                                                                             Program Verification
    Unsurprisingly, generative transformations are the most                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        Consultative

elicited, with test generation at the top. Perhaps it is more
interesting to pinpoint that general code generation is utilized in
almost all categories (except for static analysis approaches). In-                                                                                                                                                                                                                                                       Figure 9: Coarse mapping: SE big areas vs. transf. taxonomy main categories.
stead, static analysis approaches like [243] use domain-specific
code generation to get scripts and rules to scan code under analy-
                                                                                                                                                                                                                                                                                                                       proaches except static analysis. Verbalization transformations
sis. Rationalized vulnerability detection is also a quite populated
                                                                                                                                                                                                                                                                                                                       are either requested by instructing them as the expected result
category due to the number of exploratory studies eliciting such
                                                                                                                                                                                                                                                                                                                       or as intermediate suggested steps in a Chain of Thought. We
sort of transformations.
                                                                                                                                                                                                                                                                                                                       conjecture verbalization being a good performance “natural”
    It is worth noting that software-entities verbalization (typi-                                                                                                                                                                                                                                                     task [63] and the generated result is also an effective tool for
cally but not restricted to intent generation from code) is a class                                                                                                                                                                                                                                                    conditioning subsequent transformations (see also Section 7).
of transformations extensively used trough almost all SE ap-
                                                                                                                                                                                                                                                                                              13
                      Table 3: Transformation Categories and Characteristics of Mapped Transformations.

Transformation        Characteristics of Mapped Transformations
Category

Code Generation       The most frequent transformation type is the generation of code that corresponds to a given natural language intent.
                      Contextualized transformations (meaning, transformation stated as a “fill-in” or completing a partial solution) seem to be
                      preferred whenever they make sense for the addressed problem. Implementation notes: in general terms, in this category,
                      transformations seem to be elicited by just conditioning the model with their description/instruction.

Domain-Specific       Frequent code types are fuzzing drivers (i.e., a program that can execute library functions by feeding them with inputs
Code Generation       provided by a fuzzer) or scripts for scanning code. Implementation notes: prompting strategies are similar to those of general
                      code generation. Still, there is a proportionally higher use of the Few-Shot demonstrations as an ICL (In-Context Learning)
                      approach [27] (possibly, given the potentially fewer data points during pre-training). Function calling [190] also seems an
                      alternative to the lack of training data for the domain specific language (DSL).

Test Generation       Types vary greatly on the generation criteria being the “natural” (i.e., no specific criteria beyond being as a “predictable” test
                      accompanying the code in context according to the model) the more frequent one. Implementation notes: test generation is
                      often elicited without using any particular strategy beyond the instruction itself (see [294] for a similar observation). In this
                      case, Few-Shot demos are used to clarify some generation criteria that are not standard or in some studies to evaluate ICL.

Annotation            Some transformations mapped seem to pursue ambitious correctness criteria (e.g., being annotations that enable a symbolic
Generation            proof). Implementation notes: it seems unlikely that LLM has been pre-trained and/or fine-tuned for such tasks, and it seems
                      to require more sophisticated approaches to adequately prompt the model (more than half of transformations require CoT or
                      some guided decomposition).

Data Generation       Transformations are rich in terms of criteria/goal spectrum: from consistency with interactions and environment hints to
                      being variants of some other data exemplar. Implementation notes: Few-Shot seems to be the more common approach after
                      simply instructing to get results.

Behavior Analysis     A typical transformation is root cause analysis which naturally fits as a reactive task that requests/inspects/analyzes
                      information on demand. Transformations in this category sometimes require an extra input to perform the evaluation (code,
                      traces or verbalizations) (see also section 7). Implementation notes: In-Context Learning and rationalization are also present
                      in the analyzed literature.

Direct Code           Security vulnerability proneness is the most frequent analysis domain (e.g., CWE vulnerability presence). In particular, the
Classification        most frequent classification transformation is identifying whether a snippet of code belongs to the vulnerability-prone class.
                      Close-ended classification means the set of labels/classes of interest is predefined (e.g., the target list of CWE vulnerabilities).
                      While some transformations deal with some (pre)fixed concept of vulnerability proneness (e.g., CWE), in some cases,
                      the concept that defines (the) class is actually characterized verbally in-context, that is, transformations are parametric to
                      pieces of information injected and only available at model’s inference time (e.g., brand new definitions of vulnerabilities,
                      a behavioral description, etc.). Implementation notes: many of these transformations are frequently elicited just by using
                      a description of what is desired (labels for vulnerabilities assumed “memorized” and patterns learned either explicitly or
                      implicitly during pre-training). The use of retrieved examples in-context are among the alternatives used by authors when
                      seeking to condition result to what is known about similar cases.

Rationalized          “Nature of classification” alternatives are similar to direct code classification (including also denotation relationship between
Code-Classification   labels and concepts are provided as an actual input parameter of such transformations during inference time). Particular to
                      this category is the variety of types of rationalizations that justify classification: typically an assessment or a reason but also
                      fixes and exploits are possible ways to witness the classification of code into a vulnerability proneness class. Implementation
                      notes: rationalized transformations compared to direct ones use more frequently ICL prompting strategies. It is notable
                      the use of CoT to get the rationalization of the classification. In some works, it likely acts as a way to improve quality of
                      classification by (auto)guidance† .
                      †
                       It is worth noting that from a wider interpretation of what CoT means, CoT usage might be underreported in this category since we typically
                      do not consider as truly “CoT-compliant” prompts that suggest the generation of rationalization after verbalizing the classification outcome
                      nor prompts that explicitly instruct directed/guided steps of thought (we consider that as chained transformations).


Code Scaling          In particular, a couple of works feature transformations that were mapped into Line-code Ranking category. Implementation
                      notes: they are typically straightforwardly elicited by instructions.

Task Solution         Transformations found are meant to perform quality evaluation functions [206] described in prompts and correctness
Analysis              assessment. Implementation notes: they are typically straightforwardly elicited by instructions.

                                                                                                                                        Continued on next page




                                                                     14
                              Table 3: Transformation Categories and Characteristics of Mapped Transformations. (Continued)

Transformation                      Characteristics of Mapped Transformations
Category

Text Analysis                       It includes transformations that resemble those tasks studied and benchmarked by the Natural Language Processing
                                    community (e.g., implicatures, ambiguity detection, etc. [221]). Interestingly, while some transformations are mainly
                                    domain-independent, others are supposed to be solved by recalling some domain expertise to leverage missing tacit
                                    knowledge. Implementation notes: In-Context Learning [27] and debate-based inference [280] are used in a couple of
                                    mapped transformations which, apparently, required certain degree of sophistication to elicit non-erring results.

Code Elements Identification and    Typically transformations mapped into this category are meant to extract elements that fit some given role (some fixed in
Extraction                          tool’s design-time (e.g., [275]) and some configurable during tool’s use (e.g., [220])). One of the salient characteristics
                                    of transformations mapped in this category is their reactive nature [205, 281], in this case, to incrementally explore code
                                    bases. Context-size limitations and attention-mechanism degradation [146] usually motivate the need for such approaches.
                                    Implementation notes: their reported elicitation typically includes In-Context Learning and CoT.

Text Elements Identification and    In the studies under analysis, they are typically used to perform extractive summarization of large NL reports [150].
Extraction                          Implementation notes: Few-Shot and CoT are used and even combined.

SW-entity Verbalization             Comprises a set of elicited transformations to translate code and other software entities into natural language utterances by
                                    instructing them to do so. Intent of code is the most common abstraction goal. Implementation notes: In-Context Learning
                                    seems to have been applied only in cases where the verbalization criteria required further guidance (e.g., verbalization of
                                    differences, line-by-line explanations, etc.).

Formalization                       Transformations found typically convert intents into code’s pre and post conditions. Implementation notes: most cases are
                                    elicited by described instruction and in some cases Few-Shot demonstrations are used.

SW-entity Property Identification   Transformations are quite varied in terms of nature of abstractions uttered (from input validity constraints to static analysis
and Characterization                facts) and input is typically code, but descriptions and runtime information can also be input to the transformation.
                                    Implementation notes: adequate conditioning (e.g., In-Context Learning) is required since those transformations are,
                                    intuitively, far from trained ones.

Focused Abstractive                 Extracting a summary with a conceptual viewpoint is the most common elicited transformation in this category. Implementa-
Summarization                       tion notes: although, in most cases, they seem to be elicited by just instructing the model to perform adequate summarization
                                    (or providing some demonstrations in context), sophisticated (auto)guidance approaches (e.g., [280]) are in place when it is
                                    likely that the model may produce answers not fully aligned with the purpose of the task.

Plan Generation                     For the studies and proposals in scope, transformations deal with either generating or refining operational descriptions meant
                                    to reach goals. Typical domain is that of interacting with a software-enabled system. Implementation notes: the use of CoT
                                    guidance is quite frequent, possibly because LLMs struggle to generate criteria-aligned plans [234, 149].

What-to-do Next Generation          Generally speaking, those transformations are related to interacting with a software-enabled system as the agent’s environ-
                                    ment, given environment and history information. Implementation notes: in most mapped cases, elicitation is done by just
                                    instruction description in prompt.

Execution                           It comprises transformations that deal with program-like instruction(s)/intent computation. This could be either at a level of
                                    single instruction or potentially a code snippet or intent. Implementation notes: mostly straightforwardly elicited, use of CoT
                                    has been observed too.

Textual Data Manipulation           Textual data structures are typically used as intermediate memorization/summarization/scratchpad elements incrementally
                                    manipulated in long inference processes [183]. Implementation notes: mostly elicited by instruction description.

Knowledge Distillation              Unsurprisingly, seem to mainly be used for recalling memorized knowledge related to SW-related domains (e.g., grammar of
                                    a message structure). Implementation notes: mostly elicited by instruction description.




                                                                              15
7. Inter-transformation patterns in solution proposals                                          Optimization      Code under           Expected input
                                                                                                   name            analysis               format
   In the previous section we explain how elicited inferences
associated to the LLM-generated data were grouped into tax-
onomy of transformations. Now, we pursue the goal of finding                                                     Trigger input
                                                                                                                                     CodeReachability-Input-Characterization
behavioral patterns based on transformations, according to the                                                      pattern

studies in scope. That is, we aim at identifying what seem
to be recurrent behavioral design patterns arising from how
LLM-based transformations are related, and the likely problems                                                      Input        ConstraintSatisfying-Input-Generation
addressed by them. By “related” we adopt a broader view, mean-
ing that generated content of one transformation flows to the
                                                                                          Figure 10: An abstract run of WhiteFox [274] exhibiting inter-transformation
input of another one or, broadly speaking, affects the execution                          pattern Build Model.
of another one. That occurs when staging transformations in
a pipeline or chain but also when one transformation prepares
data that is eventually consumed by another one or a transfor-                            transformations for generating SWE. In that group of sin-
mation leads to the invocation of another transformation. The                             gle staged solution proposals there are four evaluative ap-
details on how the composition should be architected is not the                           proaches [111, 220, 283, 301], six extractive transforma-
focus of inter-transformation patterns but the nature and role of                         tions [207, 64, 160, 231, 244, 295], five code-generation/code-
transformations involved. Transformations also include types of                           completion approaches [3, 105, 145, 229, 293], five asser-
algorithmically implemented ones that are instrumental to the                             tion generation approaches [61, 90, 109, 151, 176], one data-
solution, like compilers or vector data bases.                                            generation [154], and one plan-generation [82]. In fact, typically
   Patterns are, as in the case of Design Patterns [70], potentially                      validation studies of evaluative approaches elicit LLMs by a
reusable solutions to commonly occurring problems, in this case,                          single staged approach as mentioned in previous sections.
in many contexts of LLM-native software design. To arrive                                    Patterns are grouped into different thematic areas which
to such a catalog, we group together and abstract aspects seen                            mainly corresponds to coping with compositional gap [195]
as (potentially) recurrent in the generated data dependencies                             and derived topics from broad strategies or other design pat-
arising in the transformations of the analyzed approaches. Phe-                           terns. Dealing with the compositional gap is arguably the most
nomenology introduced by the notion of transformation and their                           populated group given that we are particularly interested in the
taxonomy enables to conceptualize generated and computed data                             composition of transformations as the common way they ap-
dependencies in representative executions of solution proposals                           pear related. In fact, the variety of strategies found serves as
as part of a multivariate probabilistic distribution specification                        an initial evidence that, as we claim, compositional gap phe-
as shown in Figure 1 and Figure 10. Such sort of represen-                                nomenon [195] is the main underlying reason for interaction
tation sketches helped us to elaborate the inter-transformation                           patterns observed when two or more transformations are some-
pattern catalog. For instance, ChatTester (Figure 1) is an ex-                            how staged. Some other groups refine some of the general pat-
ample for the use of two patterns: Use Verbalized SWE and                                 terns presented: Reactive Consumption of Objects, Generating
Generate and Fix, while WhiteFox (Figure 10) features inter-                              Set of Elements, Generating with Corrective Feedback, RAG-
transformation Build Model. Also, taxonomy played a crucial                               support. Groups like Operating on an Environment, Feedback
role for discovering them as it is used to label transformations                          Processing in Reactive Trajectories, Interaction Memory are
and often permeates into the naming, description and grouping                             related to subtopics of LLM-enabled transformations typically
of exemplars found. Given the nature of our work, whether or not                          composed in agentic software. Validation deals with the general
they can be considered best practices that may be used to solve                           problem of trusting results. Finally, Economics addresses prob-
stated problems, their pros and cons, or completeness of catalog,                         lems derived from the cost of using large foundational models.
is out of scope. Instead, here we map works into identified pat-                             Patterns are described in Table 4 and approaches following
terns as a key step forward. That is, we use solution proposals of                        them are mapped together with category of involved transforma-
peer reviewed works10 to analyze data dependencies and come                               tions.
up with likely problem solved and solution pattern. Also, low
level prompting strategies and linguistic ones are not covered                            7.1. Use of patterns in transformation categories
in this catalog either (e.g. ICL strategies) and are considered                              Table 5 highlights how inter-transformation patterns to serve
out-of-scope of this work11 .                                                             to different categories of end-to-end macro transformations. That
   It is worth noting that solution proposals of some peer re-                            is, for each category, we analyze transformations (or staged trans-
viewed papers in scope are not mapped into the pattern ta-                                formations) in solution proposals which transformative purpose
ble. The reason for this is that they feature single staged                               corresponds to that category and then we highlight notable pat-
                                                                                          terns that are either used (or not) in the literature under analysis.
   10We believe the focus only on peer reviewed work does not affect the validity

of found patterns.
   11 ICL strategies were pinpointed just to provide a sense of eliciting hardness

of transformations.

                                                                                     16
             Table 4: Patterns by Topic with References and Observations. Colors of the tools indicate the corresponding SE-problem in Figure 2.

Pattern Name                      Details (Description, Tools, Observations)

Dealing with the Compositional-Gap

LLMs are powerful yet subproblem decomposition might be required for improving performance.

Enhance                           Description: Straightforward use of LLM to solve some code analysis transformations is likely to struggle with inferring the right
                                  semantic facts on executions thus leading to hallucinations (e.g., see program state analysis task discussion [214]). Augmenting
                                  signature with structural or verbalized information of existing inputs to improve evaluative transformations.
                                  Tools/Observations:
                                     • (GRACE, PromptEnhanced): Code control- and/or data-flow structure for evaluative transformation.
                                     • (PromptEnhanced, SmartAudit): SWE verbalization for evaluative transformation.

Enrich with Precisions            Description: Performance of generative transformations might benefit from adding more precise verbalized interpretations of NL
                                  descriptions (even if those interpretations and their likelihood are inferable from crystallized knowledge).
                                  Tools/Observations:
                                     • (ScenicNL): Expert-persona text analysis to derive precise properties of intents before code generation.
                                     • (ClarifyGPT): Guided user disambiguation to enrich given intent before code generation.

Use Verbalized SWE                Description: Leveraging software entities verbalizations (instead of actual SW-entities) as a input of other generative stages
                                  might the right way to break up a transformative problem.
                                  Tools/Observations:
                                     • (Fuzz4All): Usage summarization for data generation stage.
                                     • (ClarifyGPT): Verbalizing differences for text analysis stage.
                                     • (ChatTester): verbalizing intent for test generation stage.

Generate and Fix                  Description: Use correctness feedback when available to fix initial generation. Related topic: Generating with Corrective
                                  Feedback.
                                  Tools/Observations:
                                     • (PropertyGPT, KernelGPT, Clover, SpecGen, AutoSpec, Lemur, Loopy): Annotation generation.
                                     • (Clover, SpecGen, OSS-Fuzz, UGCTX, LLMDFA, AutoSpec, Lemur, Loopy, InputBlaster): Code generation.
                                     • (ChatUniTest, TestPilot, ChatTester): Test generation.
                                     • (AutoSD): Behavior analysis.
                                     • (GPTDroid, AXNav, AdbGPT, Pwn’d): What-to-do-next, planning.

Rationalize then                  Description: Verbose but likely coherent analysis (e.g., rationalized evaluative transformation) is followed by focused summa-
Summarize                         rization to yield the expected concise result.
                                  Tools/Observations:
                                     • (GameBugDescriptions, AutoFL): Behavior analysis followed by focused-abstractive summarization.
                                     • (ChatGPTSCV): Rationalized code-classification postprocessed by focused summarization.
                                     • (LM-PACE): Task-solution analysis (quality assessment) followed by abstractive summarization. Also, text analysis
                                       followed by focused-abstractive summarization to yield verdict.

Verbalize Execution               Description: Executive SWE transformation might help to expose subtle semantic aspects to improve later analysis stage.
                                  Tools/Observations:
                                     • (SELF-DEBUGGINGFeedbackLoop ): SWE execution uttered to serve a difference analysis stage.

Tour d’horizon                    Description: Elicits overview evaluative transformations. The uttered verbalized result conditions later and more detailed stages.
                                  Tools/Observations:
                                     • (ChatGPT4vul): Binary classification preceding code ranking.

Elicit Hidden Variable            Description: Eliciting assumed internal mechanisms for conditioning later verbalized answer.
                                  Tools/Observations:
                                     • (GPTScan): Hidden thoughts for binary classifications.

                                                                                                                                             Continued on next page




                                                                            17
      Table 4: Patterns by Topic with References and Observations. Colors of the tools indicate the corresponding SE-problem in Figure 2. (Continued)

Pattern Name                     Details (Description, Tools, Observations)

Build Model                      Description: Straightforward use of LLM to solve some code analysis transformations is likely to struggle with inferring the right
                                 semantic facts on executions thus leading to hallucinations (e.g., see program state analysis task discussion [214]). Extracting
                                 some useful properties of a SWE-artifact or analyzable models as an initial transformations might be a way to deal with this
                                 challenge.
                                 Tools/Observations:
                                    • (EMR, InputBlaster): Property identification for domain-specific-code generation.
                                    • (WhiteFox, SymPrompt, InputBlaster, RESTGPT): Constraint-based description of input is uttered for data generation
                                      stage.

Transform to Fit                 Description: Transforming input into a more standard problem statement where LLMs might perform better.
                                 Tools/Observations:
                                    • (SearchGEM5): Parameterized snippet generation and then a data generation stage.

Divide, Generate and             Description: Modular generation of components of the expected result are later fused and corrected.
Merge                            Tools/Observations:
                                    • (SysKG-UTF): Plan generation by refinement of subplans and fusion.
                                    • (PBT-GPT): Deterministic (not LLM-based) fusion of independent generative transformations.
                                    • (FuzzingParsers): LLM-based fusing of generated elements.

Extract and Merge                Description: Generation sometimes can be achieved by extracting and building the expected SWE.
                                 Tools/Observations:
                                    • (KernelGPT): SWE-extraction and then algorithmic construction of result.

Extract to Focus                 Description: Using LLM-powered extraction transformations to concentrate the expected transformation on relevant elements of
                                 the input SWE. Related topic: Reactive Consumption of Objects.
                                 Tools/Observations:
                                    • (SysKG-UTF): Extractive tasks for planning input.
                                    • (EMR): Text extraction for property identification.
                                    • (Dafny-Synth): Intent to structured NL before formalization.

Compute Sequence of              Description: Required transformation trajectories can be computed (symbolically or LLM-based) in advance to guide inference
Transformations                  steps.
                                 Tools/Observations:
                                    • (LATTE): Behavior analysis guided by externally fed data-flow steps (symbolically computed).

Orchestrate                      Description: It might be not trivial to statically or algorithmically determine when and how to adequately invoke and use
Transformations and              transformations and tool results. Let LLM orchestrate and instantiate a subset of available transformations (or tools) to achieve
Tools                            some higher-level transformative goal. That could be done reactively according to results. Related topics: Reactive Consumption
                                 of Objects, Operating on an Environment, CoT.
                                 Tools/Observations: Only found for the special case Reactively Consume Input.

Reactively Consume               Description: Large and complex objects (e.g., repositories, models, etc.) are inputs of analysis, generation, or retrieval
Input                            transformations. Bulk treatment might nor work. LLM can guide the exploration and analysis and react to retrieved/queried
                                 information. Related topic: Reactive Consumption of Objects.
                                 Tools/Observations:
                                    • (LLift, KernelGPT): SWE-property identification and SWE-extraction trajectories.
                                    • (AutoFL, RCAAgents): Behavior analysis from information and code.
                                    • (ChatUniTest): Test generation.

Wrapping Input for               Description: An LLM-based transformation might help input consumption by translating requests into lower level operations
Reactive Consumption             and/or concrete answers. Related topic: Reactive Consumption of Objects.
                                 Tools/Observations:
                                    • (RCAAgents, ScenicNL): Text-analysis transformation to answer open queries on textual feedback or summarized text.

                                                                                                                                            Continued on next page




                                                                           18
        Table 4: Patterns by Topic with References and Observations. Colors of the tools indicate the corresponding SE-problem in Figure 2. (Continued)

Pattern Name                         Details (Description, Tools, Observations)

Reactive Consumption of Objects

Analysis or retrieval of relevant information may require dealing with large and complex objects and bulk treatment may not work for several reasons.


Extract Incrementally                Description: Reactive information extraction for a next stage of LLM- or algorithmic-based processing.
                                     Tools/Observations:
                                        • (LLift, KernelGPT): Code-elements identification & extraction trajectories.

Extract & Perform                    Description: Knowing what to extract might require simultaneous incremental analysis.
Incrementally                        Tools/Observations:
                                        • (AutoFL): Code-fetching for behavior analysis.
                                        • (RCAAgents): Information requests (together with question generation) for behavior analysis.

Generating Set of Elements

Objects to be generated sometimes are compound of individual SWE (e.g., a test suite). Also, multiple intermediate variations of artifacts may be useful.


Sequence Elements                    Description: Generating compound SW entities and set of variants simply as a trajectory of SWE elements.
                                     Tools/Observations:
                                        • (DiffPrompt, TestGen-LLM, ChatGPTTests, CodeT, ChatUniTest, CodaMOSA, TestPilot, EASEeval, ChatTester): Test-
                                          generation for test suite construction.
                                        • (Fuzz4All): Data-generation variations from input.
                                        • (µBert): In-filling code-generation.
                                        • (DiffPrompt, ClarifyGPT): Intent-corresponding code-generation variations.
                                        • (FuzzingParsers): Error-triggering variations.

Sequence Elements and                Description: Guided variants generation.
Guiding Utterances                   Tools/Observations:
                                        • (LLMorpheus, CHEMFUZZ): Rationalized code variants.
                                        • (FuzzGPTFewShot ): Diverse code-generation with knowledge distillation transformation to utter hints intermediate.

Generate Element and                 Description: Exemplar-based generation as the first stage of variants generation.
Mutate It                            Tools/Observations:
                                        • (TitanFuzz, ChatAFL):        Exemplar code-generated and then code-generation of variants by masking and in-
                                          filling/completion.

Reactively Sequence                  Description: Feedback-driven solution variation.
Elements                             Tools/Observations:
                                        • (LLM4CBI): Mutation code-generation solutions leveraged by compilation feedback.

Generating with Corrective Feedback

LLMs hallucinate and err; validation signals can feed into corrective generative trajectories.

Fix with Sanity Check                Description: Using sanity check provided by external tool to guide correction trajectory.
Signal                               Tools/Observations:
                                        • (PropertyGPT, KernelGPT, Clover, SpecGen): Error-aware correction for annotation generation.
                                        • (ChatUniTest, ChatTester, TestPilot, CoverUp): Test-generation with compiler feedback.
                                        • (Clover, SpecGen, OSS-Fuzz, UGCTX, LLMDFA): Compiler-checked code generation.

                                                                                                                                              Continued on next page




                                                                                 19
        Table 4: Patterns by Topic with References and Observations. Colors of the tools indicate the corresponding SE-problem in Figure 2. (Continued)

Pattern Name                          Details (Description, Tools, Observations)

Fix with Goal                         Description: Incorporating verification outcomes into generation/correction trajectory.
Satisfaction Signal                   Tools/Observations:
                                         • (CoverUp): Coverage Information.
                                         • (ChatUniTest, TestPilot): Assertion failure.
                                         • (AutoSpec, Lemur, Loopy): Verified annotation generation.
                                         • (Lemur, AutoSpec, Loopy, InputBlaster): Verified code generation. Effectiveness feedback for the case of InputBlaster
                                           (DS-code generation).
                                         • (AutoSD): Reactive trajectory behavior analysis generating hypothesis which are tested.

RAG-Support

Populating DBs for similarity-based information retrieval may leverage LLM-based transformations.

NL Abstractions for                   Description: Improving retrievability through abstraction.
Embeddings                            Tools/Observations:
                                         • (LLMAPIDet, x-lifecycle): Abstractive summarization/verbalization for storing into vectorial DB, later fetched by similar-
                                           ity with verbalized/abstractive summarization of input (LLMAPIDet, RCACopilot).

Classifications for                   Description: Code classification for retrieval enhancement.
Embeddings                            Tools/Observations:
                                         • (FuzzGPTFewShot ): Code classification for ulterior demonstration retrieval.

Validation

Ultimately, results are unreliable.

Vote                                  Description: Using multiple LLM samples to establish consensus through voting mechanisms.
                                      Tools/Observations:
                                         • (LLift): Majority-vote over task solution.
                                         • (LM-PACE): Multiple answer sampling for distribution analysis.

Judge                                 Description: Using LLM-based task evaluation processes to validate outputs.
                                      Tools/Observations:
                                         • (mrDetector): Data generation with task solution analysis as judgment.
                                         • (SkipAnalyzer, GPTLens, VulDetect): Rationalized classifications with task analysis.
                                         • (LLift): SWE-property identification & characterization with task-solution analysis.

Test Symbolically                     Description: Employing symbolic methods to verify LLM outputs.
                                      Tools/Observations:
                                         • (GPTScan): Role-based software identification with symbolic validation.

Cross Check Consistency               Description: Ensuring consistency across multiple representations or modalities.
                                      Tools/Observations:
                                         • (Clover): Functional equivalence analysis of verbalized software entities.

Constrain Generation                  Description: Ensuring adherence to formal rules by constraining next-token generation (e.g. [132]).
                                      Tools/Observations:
                                         • (ScenicNL): DS-code generation.

                                                                                                                                              Continued on next page




                                                                               20
       Table 4: Patterns by Topic with References and Observations. Colors of the tools indicate the corresponding SE-problem in Figure 2. (Continued)

Pattern Name                      Details (Description, Tools, Observations)

Operating on an Environment: Approach

Problem-domain may require interacting by means of actions with complex environments. Agentic systems are typical exemplars. Related topics: Feedback
Processing, Interaction Memory.

Decide Action as You Go           Description: Reactive action decision-making based on status and trajectory.
                                  Tools/Observations:
                                     • (Pwn’d): Reachability-oriented what-to-do-next trajectory.
                                     • (GPTDroid, CrashTranslator): Goal-oriented what-to-do-next reactive trajectories.
                                     • (CrashTranslator): Chained what-to-do-next generation for refining each trajectory step.

Plan, Refine, Act,                Description: Iterative planning with execution feedback.
Update                            Tools/Observations:
                                     • (AXNav): Plan generation, refinement, one step execution, and update based on feedback.

Use Given Plan and                Description: Plan refinement at execution-time.
Refine It                         Tools/Observations:
                                     • (AdbGPT): Dynamic plan-refinement.

Feedback Processing in Reactive Trajectories

Do Bulk Processing                Description: Analyzing feedback with a single staged transformation.
                                  Tools/Observations:
                                     • (AutoSD): Text-analysis-based judgment on feedback.
                                     • (GPTDroid): Behavior analysis for concluding environment state.
                                     • (AXNav): Behavior analysis (anomaly detection).

Process Feedback                  Description: Feedback is further treated as a large and complex feedback. Related topic: Reactive Consumption of Objects.
Reactively                        Related patterns: Reactively Consume Input, Wrapping Input for Reactive Consumption.
                                  Tools/Observations:
                                     • (RCAAgents): Behavior analysis to generate questions and text analysis to generate answers.

Operating on an Environment: Interaction Memory

Exploration may require memory.

Trajectory in Context             Description: Simply maintaining context across interactions acts as history.
                                  Tools/Observations:
                                     • (RCAAgents, CrashTranslator, AdbGPT)

Update ScratchPad                 Description: Context required is not necessarily small or attention mechanism degrades. Scratchpads are manipulated by an
                                  LLM.
                                  Tools/Observations:
                                     • (AXNav): Plan updates based on context.

Algorithmically                   Description: Memory/Scratchpad is updated by an algorithmic mechanism.
Updated ScratchPad                Tools/Observations:
                                     • (GPTDroid): Symbolic context updates.

Economics

Invoking many times a cutting-edge LLM might be too expensive.

Filter before Expensive           Description: Filtering with a cheaper and less capable LLM to get a short list.
Call                              Tools/Observations:
                                     • (GPTScan): Simpler behavior analysis before a more sophisticated one.




                                                                            21
                                   Table 5: Categories of Final Transformative Goals and Observation on Patterns Used.

Category of Final Transforma-      Patterns Observations
tive Goal

Code Generation                    Generate and Fix is the typical pattern followed to improve the performance of code generation by repairing initial
                                   hallucinations. Fix with Sanity Check Signal depends on the sort of transformation category: for code generation
                                   compilation, feedback is the natural option, but other signals are possible (e.g., verifier feedback in [217]).

DS-Code Generation                 Fix with Goal Satisfaction Signal by using execution results is possible as they can be interpreted as a relevant
                                   signal for iterative improvement of transformation results.

Test Generation                    Fix with Sanity Check Signal and Fix with Goal Satisfaction Signal are both used as specializations of
                                   Generate and Fix. A single case of Reactively Consume Input can be found in [39]. Sequence Elements and
                                   Guiding Utterances is used by uttering bug description in [54].

Annotation Generation              Enriching code with annotations uses compilation errors (i.e., Fix with Sanity Check Signal) and verification results
                                   (i.e., Fix with Goal Satisfaction Signal) for patterns that are instances of Generate and Fix. There is no use of
                                   Reactively Consume Input as context is typically feed entirely into transformations instances found.

Data Generation                    Use Verbalized SWE and Build Model patterns are followed. No use of Generate and Fix was found and there
                                   is one case of Judge. No use of Reactively Consume Input as context is bulk processed in the found instances of
                                   data-generation transformations.

Direct Code Classification         Notably, possibly due to the static-analysis nature of classification and the flexibility of class definition, no instances of
                                   Generate and Fix pattern were found. Extra inputs as Enhance (e.g., call graphs, data-flow facts, etc.) are, in some
                                   works, provided to improve the quality of classification.

Rationalized Code Classification   Abstractive transformations (e.g., verbalization of software entities) are requested to be uttered before rationalizations (i.e.,
                                   Enhance). Few use Reactively Consume Input pattern to incrementally explore code base.
                                   Generally, evaluative transformations in-scope do not Generate and Fix. For rationalized transformations, self-
                                   reflection [211] is one of the attempted alternatives to Judge.

Code Scaling                       There are transformations which use Generate and Fix by means of testing feedback. Some follow Use Verbalized
                                   SWE pattern.

Task Solution Analysis             Vote is used to gain some reliability by consensus.

Text Analysis                      No pattern usage was found to improve performance, validate or fix for this category of transformations.

Code Elements Identification and   One of the salient characteristics of its transformations is their reactive nature (i.e., Reactively Consume Input).
Extraction

Text Elements Identification and   No pattern usage was found to improve performance, validate or fix for this category of transformations. Notably, transfor-
Extraction                         mations currently mapped into this category are not designed to be reactive and, thus, they are supposed to work with text
                                   that could fit into the LLMs context.

SWE Verbalization                  No pattern usage was found to improve performance, validate or fix for this category of transformations.

Formalization                      Syntactic corrective feedback (i.e., Fix with Sanity Check Signal) is featured by only one transformation in this
                                   category.

SWE Property Identification and    Only self-validation (e.g., [248, 116]) seems to be the way to obtain signal for correction (i.e., Judge and Vote). This might
Characterization                   be due to difficulties to get or process some effective corrective signals.

Plan Generation                    Divide, Generate and Merge is one pattern observed to get initial plans. Plans might be corrected with feedback, either
                                   new environmental situation or proposed action results, as different instances of Generate and Fix pattern.

What-to-do Next                    Corrective transformations might be feedback with either new environmental situation or proposed action feedback as
                                   different instances of Generate and Fix pattern. No orchestration or enhancement of potential assisting tools (e.g., AI
                                   Planners, World Models, etc.) have been found.

Execution                          Reactivity for using external computation tools is used in this class (Orchestrate Transformations and Tools). No
                                   corrective feedback found.

Textual Data Manipulation          No pattern usage was found to improve performance, validate or fix for this category of transformations.

Knowledge Distillation             No pattern usage was found to improve performance, validate or fix for this category of transformations.




                                                                              22
8. Actionable insights                                                     feedback, external tool integration, specially designed bench-
                                                                           marks (e.g., [115]), evaluation metrics [32], capabilities analy-
   While some observations on gaps have been pinpointed in                 sis [31], and learning-problem hardness [118], etc. are some of
preceding sections (e.g., lack of patterns used for some transfor-         the areas that could be explored taking into account characteris-
mative goals in Table 5) there are some aspects of the current             tics of transformations and patterns12 . For instance, constrained
landscape to which one could add prospective comments and                  generation and constrained decoding (e.g., [2, 21, 50, 132, 194],
avenues for future work from the identified transformations and            etc.) is regarded as a way to build more principled and robust
patterns.                                                                  AI-software [20, 50]. Characteristics of transformations might
                                                                           serve to understand in which extent such ideas could be applied
                                                                           and could be pursued. Just as an example, while results of
Verbalized Abstractions for Enhancement. Getting useful be-
                                                                           classification transformations, extractive transformations, and
havioral abstractions seems an important intermediate step in
                                                                           the generation of formally defined SW-entities (e.g., assertions)
many LLM-enabled transformations chains (e.g., pattern Build
                                                                           could be potentially constrained by syntactic and even seman-
Model). We envision that more research would seek for the ef-
                                                                           tic rules (Constrain Generation pattern), verbalization and
fective construction (or use) of varied language-oriented abstrac-
                                                                           transformations yielding NL abstractions, albeit useful for condi-
tions of SW-entities (e.g., GORE [235] artifacts, abstract behav-
                                                                           tioning, are likely harder to be constrained upfront. Hypothesis
ioral models [49], etc.). Those abstractions should be designed to
                                                                           search [247] combined with certified deductive reasoning [193]
leverage language analytical inference as a way to deal with the
                                                                           might be interesting steps forward for the generation of such sort
combinatorial nature of behavior (in a more historical vein, com-
                                                                           of entities.
positional deductive analysis frameworks (e.g., [87, 133, 163],
etc.) have been helping humans to reason about large state                 Compositionality. It is hard to forecast how future generation
spaces). That would require improving validation and corrective            of LLM-enabled tools will look like. However, we speculate
strategies as well as modular ways to build them. As noted,                some fundamental shortcoming might remain even if models
correction in abstractive transformations seems, in general, an            improve their performance in generative transformations. Break-
area of vacancy when compared with traditional (combinato-                 ing problems into pieces/transformations (either manually or
rial) abstraction construction (e.g. CEGAR [42], where spurious            automatically) before inference time and the use of external
counterexamples are key to interpolation-based refinement), au-            symbolic tools seems to be unavoidable due to phenomena like
tomated error detection (e.g. misalignment) and informative                the compositional gap [195] and “hard to learn” problems [118].
corrective feedback in LLM-based abstractions might be chal-               Modularity based in transformations-like concepts can be seen
lenging. We hypothesize that the ability to perform some execu-            in frameworks like [127, 216, 264] in which solutions are made
tive and data generation transformations might be useful to close          up of some sort of declarative modules which instruct “what”
some feedback loops in static analysis use cases.                          to do and might let prompting and workflow details be modi-
                                                                           fied as part of an optimization process. Yet, modularity does
Reactive Consumption of Models. In reported transformations,               not mean truly compositional analysis on solutions is actually
models either built by LLM-transformations or symbolic com-                enabled. That is, compositional reasoning (e.g., [87]) which is
putation are bulk processed by enhanced transformations. Thus,             formally and informally ubiquitous in old-plain software, seems
one can envision an opportunity to reactively consume models               to be challenging for LLM-based software [16]. In a few words,
when they possess inference capabilities (e.g. probabilistic dis-          compositional treatment of LLM-native software would mean
tribution specifications or programs). Moreover, using LLMs                that local measurable improvements in a constituent transforma-
to build world models as an intermediate to reason about rela-             tion would lead to ex-ante guaranteed end-to-end improvement.
tional systems, physical scenes and plans has been advocated               Catalogs of transformations and pattens of compositions can
by [257] and similar ideas could be empower solutions to sophis-           help to have concrete practical observations to guide approaches
ticated verification and testing problems: world models (built             address such challenges. In a few words, future research on how
using abstractive transformations) could be later act as “external”        to elicit, evaluate, abstractly characterize, and compose transfor-
components which inference capabilities can be thus leveraged              mations in the context of LLM-native software may benefit from
by a reactive transformation to improve their alignment and                identifying recurrent transformations and how they are typically
specificity.                                                               used together in inter-transformation patterns, as done in this
                                                                           work.
Improvement and evaluation of transformations and patterns.
A taxonomy can help focus efforts to improve LLM proficiency               9. Threats to Validity
in classes or instances of transformations that are recurrent and
                                                                             Naturally, due to the youth of the area and the variety of SE
might deserve specific (either existing or novel) strategies to
                                                                           problems and communities, LLM-enabled studies and proposals
analyze and improve LLM-based transformation performance.
Fine-tuning [250], reasoning bootstrapping [285], enhanced ac-               12 Natural Language Generation research has been pinpointing, for instance,
tivation/hallucination detection (e.g. [184, 228]), finer grained          that the nature of NLG-tasks seem to play an important role when analyzing
prompt tuning (e.g., [302]), prefix tuning [142], gisting [174],           quality-probability paradox [166, 167] and ultimately deciding an appropriate
prover-verifier games [129], hypothesis search [247], corrective           decoding strategy.

                                                                      23
are presented very differently from one paper to another. For               10. Conclusion
instance, LLM interaction sometimes might be described in its
low-level raw conversational nature or as just a short hint on how             Both LLMs foundational research and the engineering of soft-
LLM is used. That is, transformations are not always explicitly             ware tools on top of them are areas that are very rapidly evolving.
identified nor functionally described in some presentations. We             This work addresses an initial question on the current nature of
did our best effort in rationalizing (and filling the unknowns)             (human-defined) transformations and their composition in LLM-
in the inner workings of studies in scope. However, many de-                enabled solutions for some areas related to Software Analysis.
tails might have been wrongly captured due to our incorrect                 It does this by detecting and naming them in the extensively
understanding of those studies and proposals.                               reviewed literature and by building a hierarchical taxonomy of
   Also, for the sake of simplicity, some details regarding how             transformation classes that accommodates all instances of trans-
transformations are organized in a conversation or chain might              formations seen. We leverage the mapping to explain some
not, in some cases, be completely or accurately reported. That              existing abstract patterns of transformations relationship in the
is, for instance, there might be some imprecision (or even inac-            design of such solutions.
curacy) regarding whether a prompt for a given transformation                  This report does not try to answer another related question: is
continues a given conversation (that is a consequence of previous           a transformation viewpoint the best conceptual tool (adequate
transformations) or, alternatively, a brand new LLM session is              level of abstraction) for engineering LLM-enabled solutions?
launched and only some verbalized results yielded in the previ-             We believe the answer to this question greatly depends on the fu-
ous conversation are copied into the new context. We are aware              ture development of theory to engineer this sort of systems. The-
that those details might be crucial in practice to achieve good             ory and tools for engineering good LLM-enabled approaches are
task quality performance [159, 203, 299] (see section 10), but we           at their infancy. It is our vision that more compositional and ab-
favor highlighting conceptual characteristics of transformations            stract concepts linked to the idea of transformations are required
elicited by prompts in studied approaches.                                  to actually intellectually control behavior models and probabilis-
   Mapping from prompts to the identified transformations is                tic programs that people are building on top of them [59]. The
not always trivial. This justifies in part this work but, naturally,        need of principled engineering might also apply even if, in the fu-
it also elevates the risk of being inaccurate or too simplistic in          ture, LLMs themselves address problems by –autoregressively–
our description. Thus, although we tried to be as faithful as               proposing and chaining high-level transformations and tools
possible to the actual (but still abstract) prompting architecture,         either as at design time or at inference time.
by design, this traceability should not be taken for granted. Lack
of trivial traceability also occurs when we split transformations           Acknowledgements
instructed by a single prompt to pinpoint the different nature of
those transformations. Of course, we do not preclude that best                 This work was supported by the Coordenação de
quality performance is achieved when a single prompt elicits                Aperfeiçoamento de Pessoal de Nı́vel Superior – Brazil (CAPES-
all transformations in sequence but that is not the focus of this           PROEX), Financing Code 001, and by the Fundação de Amparo
study, as already mentioned.                                                à Pesquisa do Estado do Amazonas – FAPEAM, through the
   In summary, phenomenology based on transformations im-                   POSGRAD 23-24 project. This research was carried out within
plies tacitly adhering to a (virtual) modular and functional view           the SWPERFI UFAM-MOTOROLA RD&I Project “Técnicas
of how LLM-enabled approaches interact with LLMs in terms                   de Inteligência Artificial para Análise e Otimização de Desem-
of task elicitation. This is done “by design”, even though this             penho de Software”. This work was also partially supported by
modularity cannot be taken for granted due to other variables               CONICET PIP 11220200100084CO, ANPCyT PICT 2018-3835
playing a role in the distribution of results. However, we be-              and 2021-I-A-00755, UBACyT Grants 20020220300079BA and
lieve understanding this abstract decomposition provides a first            20020190100126BA, and A-1-2022-1-173516 IDRC-ANII.
glimpse of the strategy followed in problem-solving with LLMs.
   There is a risk of the taxonomy to be overfit to the reported pa-        Declaration of generative AI and AI-assisted technologies in the
pers and unable to fit future LLM-enabled works. Beyond being               manuscript preparation process
a risk for any taxonomy there are a couple of caveats. Firstly, the            During the preparation of this work the authors used
property/choices trees are suitable for adding both novel relevant          DeepSeek and ChatGPT in order to improve grammar and style
properties and new choices. It is also worth noting the scope and           of some sentences. After using this tool/service, the authors
exhaustiveness of SE topics covered: from falsification to formal           reviewed and edited the content as needed and take full respon-
verification ones (a scope that is rarely covered by surveys). This         sibility for the content of the published article.
means that taxonomy as it is was able to classify a rich variety
of approaches for quite different SE problems. All papers satis-
fying the criteria that were mentioned by existing surveys were             References
reported and classified to avoid cherry-picking. Last but not
least, we were able to seamlessly accommodate more than 30%                   [1] Joshua Ackerman and George Cybenko. Large language models for
                                                                                  fuzzing parsers (Registered report). In Marcel Böhme, Yannic Noller,
of papers in this study after having defined the main structure of                Baishakhi Ray, and László Szekeres, editors, FUZZING 2023: 2nd In-
the taxonomy and there was a final validation step in which we                    ternational Fuzzing Workshop, pages 31–38, New York, NY, USA, 2023.
were able to map ASE’24 easily in categories found.                               ACM, doi:10.1145/3605157.3605173.

                                                                       24
 [2] Lakshya A. Agrawal, Aditya Kanade, Navin Goyal, Shuvendu K. Lahiri,                [17] Patrick Bareiß, Beatriz Souza, Marcelo d’Amorim, and Michael Pradel.
     and Sriram K. Rajamani. Monitor-guided decoding of code LMs with                        Code generation tools (almost) for free? A study of few-shot, pre-trained
     static analysis of repository context. In Alice Oh, Tristan Naumann, Amir               language models on code, 2022, arXiv:2206.01335.
     Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine, editors, Ad-              [18] Earl T. Barr, Mark Harman, Phil McMinn, Muzammil Shahbaz, and Shin
     vances in Neural Information Processing Systems 36: Annual Conference                   Yoo. The oracle problem in software testing: A survey. IEEE Trans. Soft-
     on Neural Information Processing Systems 2023, NeurIPS 2023, New                        ware Eng., 41(5):507–525, 2015, doi:10.1109/TSE.2014.2372785.
     Orleans, LA, USA, December 10 - 16, 2023, 2023.                                    [19] Boris Beizer. Software testing techniques (2. ed.). Van Nostrand Reinhold,
 [3] Baleegh Ahmad, Benjamin Tan, Ramesh Karri, and Hammond Pearce.                          1990.
     FLAG: Finding line anomalies (in code) with generative AI, 2023,                   [20] Emery Berger and Ben Zorn. AI software should be more like plain
     arXiv:2306.12643.                                                                       old software. In Dmitry Ponomarev, editor, Computer Architecture
 [4] Mohannad Alhanahnah, Md Rashedul Hasan, Lisong Xu, and Hamid                            Today, ACM Sigarch, 2024.             At https://www.sigarch.org/
     Bagheri. An empirical evaluation of pre-trained large language models for               ai-software-should-be-more-like-plain-old-software/
     repairing declarative formal specifications. Empir. Softw. Eng., 30(5):149,             [accessed July 2024].
     2025, doi:10.1007/S10664-025-10687-1.                                              [21] Luca Beurer-Kellner, Marc Fischer, and Martin T. Vechev. Prompting is
 [5] Anahita Alipour, Abram Hindle, and Eleni Stroulia. A contextual ap-                     programming: A query language for large language models. Proc. ACM
     proach towards more accurate duplicate bug report detection. In Thomas                  Program. Lang., 7(PLDI):1946–1969, 2023, doi:10.1145/3591300.
     Zimmermann, Massimiliano Di Penta, and Sunghun Kim, editors, Pro-                  [22] Shreya Bhatia, Tarushi Gandhi, Dhruv Kumar, and Pankaj Jalote. Unit test
     ceedings of the 10th Working Conference on Mining Software Reposito-                    generation using generative AI: A comparative performance analysis of
     ries, MSR ’13, San Francisco, CA, USA, May 18-19, 2013, pages 183–192.                  autogeneration tools. In LLM4Code’24, April 20, 2024, Lisbon, Portugal,
     IEEE Computer Society, 2013, doi:10.1109/MSR.2013.6624026.                              pages 38:1–38:8. ACM, 2024, doi:10.1145/3643795.3648396.
 [6] Frances E. Allen. Control flow analysis. In Robert S. Northcote, edi-              [23] Paul C. Bogdan, Uzay Macar, Neel Nanda, and Arthur Conmy.
     tor, Proceedings of a Symposium on Compiler Optimization, Urbana-                       Thought anchors: Which LLM reasoning steps matter?, 2025,
     Champaign, Illinois, USA, July 27-28, 1970, pages 1–19. ACM, 1970,                      arXiv:2506.19143.
     doi:10.1145/800028.808479.                                                         [24] Marcel Böhme, Van-Thuan Pham, and Abhik Roychoudhury. Coverage-
 [7] Mansour Alqarni and Akramul Azim. Low level source code vul-                            based greybox fuzzing as markov chain. IEEE Trans. Software Eng.,
     nerability detection using advanced BERT language model.                 In             45(5):489–506, 2019, doi:10.1109/TSE.2017.2785841.
     Iluju Kiringa and Sébastien Gambs, editors, 35th Canadian Confer-                 [25] Vı́ctor A. Braberman, Flavia Bonomo-Braberman, Yiannis Charalam-
     ence on Artificial Intelligence, Toronto, Ontario, Canada, May 30                       bous, Juan G. Colonna, Lucas C. Cordeiro, and Rosiane de Freitas. Tasks
     - June 3, 2022. Canadian Artificial Intelligence Association, 2022,                     people prompt: A taxonomy of LLM downstream tasks in software
     doi:10.21428/594757DB.B85E6625.                                                         verification and falsification approaches, 2024, arXiv:2404.09384.
 [8] Nadia Alshahwan, Jubin Chheda, Anastasia Finogenova, Beliz Gokkaya,                [26] Houssem Ben Braiek and Foutse Khomh.                     On testing ma-
     Mark Harman, Inna Harper, Alexandru Marginean, Shubho Sengupta,                         chine learning programs.          J. Syst. Softw., 164:110542, 2020,
     and Eddy Wang. Automated unit test improvement using large language                     doi:10.1016/J.JSS.2020.110542.
     models at Meta. In Marcelo d’Amorim, editor, Companion Proceed-                    [27] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared
     ings of the 32nd ACM International Conference on the Foundations of                     Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish
     Software Engineering, FSE 2024, Porto de Galinhas, Brazil, July 15-19,                  Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen
     2024, pages 185–196. ACM, 2024, doi:10.1145/3663529.3663839.                            Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M.
 [9] Nadia Alshahwan, Mark Harman, Inna Harper, Alexandru Marginean,                         Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen,
     Shubho Sengupta, and Eddy Wang. Assured LLM-based software engi-                        Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark,
     neering. In 2nd IEEE/ACM International Workshop on Interpretabil-                       Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever,
     ity, Robustness, and Benchmarking in Neural Software Engineering,                       and Dario Amodei. Language models are few-shot learners. In Hugo
     InteNSE@ICSE 2024, Lisbon, Portugal, April 15, 2024, pages 7–12.                        Larochelle, Marc’Aurelio Ranzato, Raia Hadsell, Maria-Florina Balcan,
     ACM/IEEE, 2024, doi:10.1145/3643661.3643953.                                            and Hsuan-Tien Lin, editors, Advances in Neural Information Process-
[10] Sven Amann, Hoan Anh Nguyen, Sarah Nadi, Tien N. Nguyen,                                ing Systems 33: Annual Conference on Neural Information Processing
     and Mira Mezini. A systematic evaluation of static API-misuse                           Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual, 2020.
     detectors. IEEE Trans. Software Eng., 45(12):1170–1188, 2019,                      [28] Cristian Cadar and Koushik Sen. Symbolic execution for software
     doi:10.1109/TSE.2018.2827384.                                                           testing: three decades later. Commun. ACM, 56(2):82–90, 2013,
[11] Paul Ammann and Jeff Offutt. Introduction to Software Testing. Cam-                     doi:10.1145/2408776.2408795.
     bridge University Press, 2008, doi:10.1017/CBO9780511809163.                       [29] Saikat Chakraborty, Rahul Krishna, Yangruibo Ding, and Baishakhi
[12] Saswat Anand, Edmund K. Burke, Tsong Yueh Chen, John A. Clark,                          Ray. Deep learning based vulnerability detection: Are we there
     Myra B. Cohen, Wolfgang Grieskamp, Mark Harman, Mary Jean Har-                          yet?         IEEE Trans. Software Eng., 48(9):3280–3296, 2022,
     rold, and Phil McMinn. An orchestrated survey of methodologies for                      doi:10.1109/TSE.2021.3087402.
     automated software test case generation. J. Syst. Softw., 86(8):1978–2001,         [30] Aaron Chan, Anant Kharkar, Roshanak Zilouchian Moghaddam, Yevhen
     2013, doi:10.1016/J.JSS.2013.02.061.                                                    Mohylevskyy, Alec Helyar, Eslam Kamal, Mohamed Elkamhawy,
[13] Dharun Anandayuvaraj, Matthew Campbell, Arav Tewari, and James C.                       and Neel Sundaresan. Transformer-based vulnerability detection
     Davis. FAIL: analyzing software failures from the news using LLMs. In                   in code at EditTime: Zero-shot, few-shot, or fine-tuning?, 2023,
     Vladimir Filkov, Baishakhi Ray, and Minghui Zhou, editors, Proceedings                  arXiv:2306.01754.
     of the 39th IEEE/ACM International Conference on Automated Software                [31] Tyler A. Chang and Benjamin K. Bergen. Language model behavior:
     Engineering, ASE 2024, Sacramento, CA, USA, October 27 - November 1,                    A comprehensive survey. Comput. Linguistics, 50(1):293–350, 2024,
     2024, pages 506–518. ACM, 2024, doi:10.1145/3691620.3695022.                            doi:10.1162/COLI A 00492.
[14] Christel Baier and Joost-Pieter Katoen. Principles of model checking.              [32] Yupeng Chang, Xu Wang, Jindong Wang, Yuan Wu, Linyi Yang, Kaijie
     MIT Press, 2008.                                                                        Zhu, Hao Chen, Xiaoyuan Yi, Cunxiang Wang, Yidong Wang, Wei Ye,
[15] Almog Baku. Building LLM apps: A clear step-by-step guide, Jun                          Yue Zhang, Yi Chang, Philip S. Yu, Qiang Yang, and Xing Xie. A survey
     2024. Medium TDS Archive, https://medium.com/data-science/                              on evaluation of large language models. ACM Trans. Intell. Syst. Technol.,
     1fe1e6ef60fd [accessed Sept 2025].                                                      15(3):39:1–39:45, 2024, doi:10.1145/3641289.
[16] Juan Manuel Baldonado, Flavia Bonomo-Braberman, and Vı́ctor A.                     [33] Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-
     Braberman. Towards a probabilistic framework for analyzing and im-                      Guang Lou, and Weizhu Chen. CodeT: Code generation with generated
     proving LLM-enabled software. In IEEE International Conference on                       tests. In The Eleventh International Conference on Learning Represen-
     Software Testing, Verification and Validation, ICST 2025 - Workshops,                   tations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023. OpenReview.net,
     Naples, Italy, March 31 - April 4, 2025, pages 418–422. IEEE, 2025,                     2023.
     doi:10.1109/ICSTW64639.2025.10962470.                                              [34] Chong Chen, Jianzhong Su, Jiachi Chen, Tingting Bi, Jianxing Yu,


                                                                                   25
     Yanlin Wang, Xingwei Lin, Ting Chen, and Zibin Zheng. When                            arXiv:2306.12338.
     ChatGPT meets smart contract vulnerability detection: How far are                [49] Guido de Caso, Vı́ctor A. Braberman, Diego Garbervetsky, and Sebastián
     we? ACM Trans. Softw. Eng. Methodol., 34(4):100:1–100:30, 2025,                       Uchitel. Automated abstractions for contract validation. IEEE Trans.
     doi:10.1145/3702973.                                                                  Software Eng., 38(1):141–162, 2012, doi:10.1109/TSE.2010.98.
[35] Hongbo Chen, Yifan Zhang, Xing Han, Huanyao Rong, Yuheng Zhang,                  [50] Jasper Dekoninck, Marc Fischer, Luca Beurer-Kellner, and Martin T.
     Tianhao Mao, Hang Zhang, XiaoFeng Wang, Luyi Xing, and Xun Chen.                      Vechev. Controlled text generation via language model arithmetic. In
     WitheredLeaf: Finding entity-inconsistency bugs with LLMs, 2024,                      The Twelfth International Conference on Learning Representations, ICLR
     arXiv:2405.01668.                                                                     2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024.
[36] Tsong Yueh Chen, Fei-Ching Kuo, Huai Liu, Pak-Lok Poon, Dave Towey,              [51] Gelei Deng, Yi Liu, Vı́ctor Mayoral Vilches, Peng Liu, Yuekang Li, Yuan
     T. H. Tse, and Zhi Quan Zhou. Metamorphic testing: A review of                        Xu, Martin Pinzger, Stefan Rass, Tianwei Zhang, and Yang Liu. Pentest-
     challenges and opportunities. ACM Comput. Surv., 51(1):4:1–4:27, 2018,                GPT: Evaluating and harnessing large language models for automated
     doi:10.1145/3143561.                                                                  penetration testing. In Davide Balzarotti and Wenyuan Xu, editors, 33rd
[37] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. Teach-                  USENIX Security Symposium, USENIX Security 2024, Philadelphia, PA,
     ing large language models to self-debug. In The Twelfth International                 USA, August 14-16, 2024. USENIX Association, 2024.
     Conference on Learning Representations, ICLR 2024, Vienna, Austria,              [52] Yao Deng, Zhi Tu, Jiaohong Yao, Mengshi Zhang, Tianyi Zhang,
     May 7-11, 2024. OpenReview.net, 2024.                                                 and James Xi Zheng.           TARGET: traffic rule-based test genera-
[38] Yinfang Chen, Huaibing Xie, Minghua Ma, Yu Kang, Xin Gao, Liu                         tion for autonomous driving via validated LLM-guided knowledge
     Shi, Yunjie Cao, Xuedong Gao, Hao Fan, Ming Wen, Jun Zeng, Supriyo                    extraction. IEEE Trans. Software Eng., 51(7):1950–1968, 2025,
     Ghosh, Xuchao Zhang, Chaoyun Zhang, Qingwei Lin, Saravan Rajmo-                       doi:10.1109/TSE.2025.3569086.
     han, Dongmei Zhang, and Tianyin Xu. Automatic root cause analy-                  [53] Yinlin Deng, Chunqiu Steven Xia, Haoran Peng, Chenyuan Yang, and
     sis via large language models for cloud incidents. In Proceedings of                  Lingming Zhang. Large language models are zero-shot fuzzers: Fuzzing
     the Nineteenth European Conference on Computer Systems, EuroSys                       deep-learning libraries via large language models. In René Just and
     2024, Athens, Greece, April 22-25, 2024, pages 674–688. ACM, 2024,                    Gordon Fraser, editors, 32nd ACM SIGSOFT International Symposium on
     doi:10.1145/3627703.3629553.                                                          Software Testing and Analysis, ISSTA 2023, Seattle, WA, USA, July 17-21,
[39] Yinghao Chen, Zehao Hu, Chen Zhi, Junxiao Han, Shuiguang Deng, and                    2023, pages 423–435. ACM, 2023, doi:10.1145/3597926.3598067.
     Jianwei Yin. ChatUniTest: A framework for LLM-based test generation.             [54] Yinlin Deng, Chunqiu Steven Xia, Chenyuan Yang, Shizhuo Dylan Zhang,
     In Marcelo d’Amorim, editor, Companion Proceedings of the 32nd ACM                    Shujing Yang, and Lingming Zhang. Large language models are edge-
     International Conference on the Foundations of Software Engineering,                  case generators: Crafting unusual programs for fuzzing deep learning
     FSE 2024, Porto de Galinhas, Brazil, July 15-19, 2024, pages 572–576.                 libraries. In 46th IEEE/ACM International Conference on Software En-
     ACM, 2024, doi:10.1145/3663529.3663801.                                               gineering, ICSE 2024, Lisbon, Portugal, April 14-20, 2024, pages 70:1–
[40] Brian Chess and Gary McGraw. Static analysis for security. IEEE Secur.                70:13. ACM, 2024, doi:10.1145/3597503.3623343.
     Priv., 2(6):76–79, 2004, doi:10.1109/MSP.2004.111.                               [55] Jayati Deshmukh, K. M. Annervaz, Sanjay Podder, Shubhashis Sengupta,
[41] Agnieszka Ciborowska and Kostadin Damevski. Fast changeset-based                      and Neville Dubash. Towards accurate duplicate bug retrieval using
     bug localization with BERT. In 44th IEEE/ACM International Conference                 deep learning techniques. In 2017 IEEE International Conference on
     on Software Engineering, ICSE 2022, Pittsburgh, PA, USA, May 25-27,                   Software Maintenance and Evolution, ICSME 2017, Shanghai, China,
     2022, pages 946–957. ACM, 2022, doi:10.1145/3510003.3510042.                          September 17-22, 2017, pages 115–124. IEEE Computer Society, 2017,
[42] Edmund M. Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Hel-                        doi:10.1109/ICSME.2017.69.
     mut Veith. Counterexample-guided abstraction refinement. In E. Allen             [56] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.
     Emerson and A. Prasad Sistla, editors, Computer Aided Verification, 12th              BERT: pre-training of deep bidirectional transformers for language un-
     International Conference, CAV 2000, Chicago, IL, USA, July 15-19, 2000,               derstanding. In Jill Burstein, Christy Doran, and Thamar Solorio, editors,
     Proceedings, volume 1855 of Lecture Notes in Computer Science, pages                  Proceedings of the 2019 Conference of the North American Chapter of
     154–169. Springer, 2000, doi:10.1007/10722167 15.                                     the Association for Computational Linguistics: Human Language Tech-
[43] Edmund M. Clarke, Orna Grumberg, Daniel Kroening, Doron A. Peled,                     nologies, NAACL-HLT 2019, Minneapolis, MN, USA, June 2-7, 2019,
     and Helmut Veith. Model checking, 2nd Edition. MIT Press, 2018.                       Volume 1 (Long and Short Papers), pages 4171–4186. Association for
[44] Patrick Cousot and Radhia Cousot. Abstract interpretation: A uni-                     Computational Linguistics, 2019, doi:10.18653/V1/N19-1423.
     fied lattice model for static analysis of programs by construction               [57] Edsger W. Dijkstra. Notes on structured programming. Technical Report
     or approximation of fixpoints. In Robert M. Graham, Michael A.                        70-WSK-03, EWD Vol. 249, WSK, Dept. of Mathematics and Computing
     Harrison, and Ravi Sethi, editors, Conference Record of the Fourth                    Science, Technische Hogeschool Eindhoven, 1970.
     ACM Symposium on Principles of Programming Languages, Los An-                    [58] Elizabeth Dinella, Gabriel Ryan, Todd Mytkowicz, and Shuvendu K.
     geles, California, USA, January 1977, pages 238–252. ACM, 1977,                       Lahiri. TOGA: A neural method for test oracle generation. In 44th
     doi:10.1145/512950.512973.                                                            IEEE/ACM International Conference on Software Engineering, ICSE
[45] Patrick Cousot and Nicolas Halbwachs. Automatic discovery of linear                   2022, Pittsburgh, PA, USA, May 25-27, 2022, pages 2130–2141. ACM,
     restraints among variables of a program. In Alfred V. Aho, Stephen N.                 2022, doi:10.1145/3510003.3510141.
     Zilles, and Thomas G. Szymanski, editors, Conference Record of the               [59] David Dohan, Winnie Xu, Aitor Lewkowycz, Jacob Austin, David Bieber,
     Fifth Annual ACM Symposium on Principles of Programming Languages,                    Raphael Gontijo Lopes, Yuhuai Wu, Henryk Michalewski, Rif A. Saurous,
     Tucson, Arizona, USA, January 1978, pages 84–96. ACM Press, 1978,                     Jascha Sohl-dickstein, Kevin Murphy, and Charles Sutton. Language
     doi:10.1145/512760.512770.                                                            model cascades, 2022, arXiv:2207.10342. Presented as spotlight at
[46] Aidan Dakhama, Karine Even-Mendoza, William B. Langdon, Héctor D.                    the Beyond Bases workshop at ICML 2022.
     Menéndez, and Justyna Petke. SearchGEM5: Towards reliable Gem5                  [60] Karim Elmaaroufi, Devan Shanker, Ana Cismaru, Marcell Vazquez-
     with search based software testing and large language models. In Paolo                Chanlatte, Alberto Sangiovanni-Vincentelli, Matei Zaharia, and Sanjit A.
     Arcaini, Tao Yue, and Erik M. Fredericks, editors, Search-Based Soft-                 Seshia. ScenicNL: Generating probabilistic scenario programs from nat-
     ware Engineering - 15th International Symposium, SSBSE 2023, San                      ural language. In First Conference on Language Modeling, COLM 2024,
     Francisco, CA, USA, December 8, 2023, Proceedings, volume 14415                       Philadelphia, Pennsylvania, United States, Oct 7, 2024. OpenReview.net,
     of Lecture Notes in Computer Science, pages 160–166. Springer, 2023,                  2024.
     doi:10.1007/978-3-031-48796-5 14.                                                [61] Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, and Shuvendu K.
[47] Arghavan Moradi Dakhel, Amin Nikanjam, Vahid Majdinasab, Foutse                       Lahiri. Can large language models transform natural language intent into
     Khomh, and Michel C. Desmarais. Effective test generation using pre-                  formal method postconditions? Proc. ACM Softw. Eng., 1(FSE):1889–
     trained large language models and mutation testing. Inf. Softw. Technol.,             1912, 2024, doi:10.1145/3660791.
     171:107468, 2024, doi:10.1016/J.INFSOF.2024.107468.                              [62] Angela Fan, Beliz Gokkaya, Mark Harman, Mitya Lyubarskiy, Shubho
[48] Isaac David, Liyi Zhou, Kaihua Qin, Dawn Song, Lorenzo Cavallaro, and                 Sengupta, Shin Yoo, and Jie M. Zhang. Large language models for soft-
     Arthur Gervais. Do you still need a manual smart contract audit?, 2023,               ware engineering: Survey and open problems. In IEEE/ACM International


                                                                                 26
     Conference on Software Engineering: Future of Software Engineering,             [77] Jiazhen Gu, Xuchuan Luo, Yangfan Zhou, and Xin Wang. Muffin: Test-
     ICSE-FoSE 2023, Melbourne, Australia, May 14-20, 2023, pages 31–53.                  ing deep learning libraries via neural architecture fuzzing. In 44th
     IEEE, 2023, doi:10.1109/ICSE-FOSE59343.2023.00008.                                   IEEE/ACM International Conference on Software Engineering, ICSE
[63] Chongzhou Fang, Ning Miao, Shaurya Srivastav, Jialin Liu, Ruoyu Zhang,               2022, Pittsburgh, PA, USA, May 25-27, 2022, pages 1418–1430. ACM,
     Ruijie Fang, Asmita, Ryan Tsang, Najmeh Nazari, Han Wang, and                        2022, doi:10.1145/3510003.3510092.
     Houman Homayoun. Large language models for code analysis: Do                    [78] An Guo, Yuan Zhou, Haoxiang Tian, Chunrong Fang, Yunjian Sun,
     llms really do their job? In Davide Balzarotti and Wenyuan Xu, editors,              Weisong Sun, Xinyu Gao, Anh Tuan Luu, Yang Liu, and Zhenyu Chen.
     33rd USENIX Security Symposium, USENIX Security 2024, Philadelphia,                  SoVAR: Build generalizable scenarios from accident reports for au-
     PA, USA, August 14-16, 2024. USENIX Association, 2024.                               tonomous driving testing. In Proceedings of the 39th IEEE/ACM In-
[64] Sidong Feng and Chunyang Chen. Prompting is all you need: Au-                        ternational Conference on Automated Software Engineering, ASE 2024,
     tomated android bug replay with large language models. In 46th                       Sacramento, CA, USA, October 27 - November 1, 2024, pages 268–280.
     IEEE/ACM International Conference on Software Engineering, ICSE                      ACM, 2024, doi:10.1145/3691620.3695037.
     2024, Lisbon, Portugal, April 14-20, 2024, pages 67:1–67:13. ACM,               [79] Yongqi Han, Qingfeng Du, Ying Huang, Jiaqi Wu, Fulong Tian, and
     2024, doi:10.1145/3597503.3608137.                                                   Cheng He. The potential of one-shot failure root cause analysis: Col-
[65] Chrisantha Fernando, Dylan Banarse, Henryk Michalewski, Simon                        laboration of the large language model and small classifier. In Vladimir
     Osindero, and Tim Rocktäschel. Promptbreeder: Self-referential self-                Filkov, Baishakhi Ray, and Minghui Zhou, editors, Proceedings of the
     improvement via prompt evolution. In Forty-first International Confer-               39th IEEE/ACM International Conference on Automated Software Engi-
     ence on Machine Learning, ICML 2024, Vienna, Austria, July 21-27,                    neering, ASE 2024, Sacramento, CA, USA, October 27 - November 1,
     2024. OpenReview.net, 2024.                                                          2024, pages 931–943. ACM, 2024, doi:10.1145/3691620.3695475.
[66] Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. Baldur:              [80] Hazim Hanif and Sergio Maffeis. VulBERTa: Simplified source code
     Whole-proof generation and repair with large language models. In                     pre-training for vulnerability detection. In International Joint Conference
     Satish Chandra, Kelly Blincoe, and Paolo Tonella, editors, 31st ACM                  on Neural Networks, IJCNN 2022, Padua, Italy, July 18-23, 2022, pages
     Joint European Software Engineering Conference and Symposium on                      1–8. IEEE, 2022, doi:10.1109/IJCNN55064.2022.9892280.
     the Foundations of Software Engineering, ESEC/FSE 2023, San Fran-               [81] Yu Hao, Weiteng Chen, Ziqiao Zhou, and Weidong Cui. E&V: Prompt-
     cisco, CA, USA, December 3-9, 2023, pages 1229–1241. ACM, 2023,                      ing large language models to perform static analysis by pseudo-code
     doi:10.1145/3611643.3616243.                                                         execution and verification, 2023, arXiv:2312.08477.
[67] Gordon Fraser and Andrea Arcuri. Evosuite: automatic test suite                 [82] Andreas Happe and Jürgen Cito. Getting pwn’d by AI: Penetration testing
     generation for object-oriented software. In Tibor Gyimóthy and An-                  with large language models. In Satish Chandra, Kelly Blincoe, and
     dreas Zeller, editors, SIGSOFT/FSE’11 19th ACM SIGSOFT Sym-                          Paolo Tonella, editors, 31st ACM Joint European Software Engineering
     posium on the Foundations of Software Engineering (FSE-19) and                       Conference and Symposium on the Foundations of Software Engineering,
     ESEC’11: 13th European Software Engineering Conference (ESEC-13),                    ESEC/FSE 2023, San Francisco, CA, USA, December 3-9, 2023, pages
     Szeged, Hungary, September 5-9, 2011, pages 416–419. ACM, 2011,                      2082–2086. ACM, 2023, doi:10.1145/3611643.3613083.
     doi:10.1145/2025113.2025179.                                                    [83] Ahmed E. Hassan, Dayi Lin, Gopi Krishnan Rajbahadur, Keheliya Gal-
[68] Michael Fu and Chakkrit Tantithamthavorn. LineVul: A transformer-                    laba, Filipe Roseiro Côgo, Boyuan Chen, Haoxiang Zhang, Kishanthan
     based line-level vulnerability prediction. In 19th IEEE/ACM Inter-                   Thangarajah, Gustavo Ansaldi Oliva, Jiahuei (Justina) Lin, Wali Mo-
     national Conference on Mining Software Repositories, MSR 2022,                       hammad Abdullah, and Zhen Ming (Jack) Jiang. Rethinking software
     Pittsburgh, PA, USA, May 23-24, 2022, pages 608–620. ACM, 2022,                      engineering in the era of foundation models: A curated catalogue of chal-
     doi:10.1145/3524842.3528452.                                                         lenges in the development of trustworthy FMware. In Marcelo d’Amorim,
[69] Michael Fu, Chakkrit Kla Tantithamthavorn, Van Nguyen, and Trung Le.                 editor, Companion Proceedings of the 32nd ACM International Confer-
     ChatGPT for vulnerability detection, classification, and repair: How far             ence on the Foundations of Software Engineering, FSE 2024, Porto
     are we? In 30th Asia-Pacific Software Engineering Conference, APSEC                  de Galinhas, Brazil, July 15-19, 2024, pages 294–305. ACM, 2024,
     2023, Seoul, Republic of Korea, December 4-7, 2023, pages 632–636.                   doi:10.1145/3663529.3663849.
     IEEE, 2023, doi:10.1109/APSEC60848.2023.00085.                                  [84] Jingxuan He, Mark Vero, Gabriela Krasnopolska, and Martin T. Vechev.
[70] Erich Gamma, Richard Helm, Ralph E. Johnson, and John M. Vlissides.                  Instruction tuning for secure code generation. In Forty-first International
     Design patterns: Abstraction and reuse of object-oriented design. In                 Conference on Machine Learning, ICML 2024, Vienna, Austria, July
     Oscar Nierstrasz, editor, ECOOP’93 - Object-Oriented Programming,                    21-27, 2024. OpenReview.net, 2024.
     7th European Conference, Kaiserslautern, Germany, July 26-30, 1993,             [85] Junda He, Christoph Treude, and David Lo. LLM-based multi-agent
     Proceedings, volume 707 of Lecture Notes in Computer Science, pages                  systems for software engineering: Literature review, vision, and the road
     406–431. Springer, 1993, doi:10.1007/3-540-47910-4 21.                               ahead. ACM Trans. Softw. Eng. Methodol., 34(5):124:1–124:30, 2025,
[71] Zeyu Gao, Hao Wang, Yuchen Zhou, Wenyu Zhu, and Chao Zhang. How                      doi:10.1145/3712003.
     far have we gone in vulnerability detection using large language models,        [86] Abram Hindle, Anahita Alipour, and Eleni Stroulia.                  A con-
     2023, arXiv:2311.12420.                                                              textual approach towards more accurate duplicate bug report de-
[72] Patrice Godefroid, Nils Klarlund, and Koushik Sen. DART: directed                    tection and ranking.       Empir. Softw. Eng., 21(2):368–410, 2016,
     automated random testing. In Vivek Sarkar and Mary W. Hall, editors,                 doi:10.1007/S10664-015-9387-3.
     Proceedings of the ACM SIGPLAN 2005 Conference on Programming                   [87] C. A. R. Hoare. An axiomatic basis for computer programming. Commun.
     Language Design and Implementation, Chicago, IL, USA, June 12-15,                    ACM, 12(10):576–580, 1969, doi:10.1145/363235.363259.
     2005, pages 213–223. ACM, 2005, doi:10.1145/1065010.1065036.                    [88] Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, and Yejin Choi. The
[73] Drishti Goel, Fiza Husain, Aditya Singh, Supriyo Ghosh, Anjaly Parayil,              curious case of neural text degeneration. In 8th International Conference
     Chetan Bansal, Xuchao Zhang, and Saravan Rajmohan. X-lifecycle learn-                on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April
     ing for cloud incident management using LLMs. In Marcelo d’Amorim,                   26-30, 2020. OpenReview.net, 2020.
     editor, Companion Proceedings of the 32nd ACM International Con-                [89] Or Honovich, Uri Shaham, Samuel R. Bowman, and Omer Levy. Instruc-
     ference on the Foundations of Software Engineering, FSE 2024, Porto                  tion induction: From few examples to natural language task descriptions.
     de Galinhas, Brazil, July 15-19, 2024, pages 417–428. ACM, 2024,                     In Anna Rogers, Jordan L. Boyd-Graber, and Naoaki Okazaki, editors,
     doi:10.1145/3663529.3663861.                                                         Proceedings of the 61st Annual Meeting of the Association for Computa-
[74] Amid Golmohammadi, Man Zhang, and Andrea Arcuri. Testing restful                     tional Linguistics (Volume 1: Long Papers), ACL 2023, Toronto, Canada,
     apis: A survey. ACM Trans. Softw. Eng. Methodol., 33(1):27:1–27:41,                  July 9-14, 2023, pages 1935–1952. Association for Computational Lin-
     2024, doi:10.1145/3617175.                                                           guistics, 2023, doi:10.18653/V1/2023.ACL-LONG.108.
[75] Ian J. Goodfellow, Yoshua Bengio, and Aaron C. Courville. Deep Learn-           [90] Soneya Binta Hossain and Matthew B. Dwyer. TOGLL: correct and
     ing. Adaptive computation and machine learning. MIT Press, 2016.                     strong test oracle generation with LLMS. In 47th IEEE/ACM Inter-
[76] Google. AI-powered fuzzing: Breaking the bug hunting barrier, 2023. At               national Conference on Software Engineering, ICSE 2025, Ottawa,
     security.googleblog.com [accessed April 2024].                                       ON, Canada, April 26 - May 6, 2025, pages 1475–1487. IEEE, 2025,


                                                                                27
      doi:10.1109/ICSE55347.2025.00098.                                                  [105] Ali Reza Ibrahimzada, Yang Chen, Ryan Rong, and Reyhaneh Jabbarvand.
 [91] Soneya Binta Hossain, Nan Jiang, Qiang Zhou, Xiaopeng Li, Wen-Hao                        Automated bug generation in the era of large language models, 2023,
      Chiang, Yingjun Lyu, Hoan Nguyen, and Omer Tripp. A deep dive into                       arXiv:2310.02407.
      large language models for automated bug localization and repair. Proc.             [106] Erblin Isaku, Christoph Laaber, Hassan Sartaj, Shaukat Ali, Thomas
      ACM Softw. Eng., 1(FSE):1471–1493, 2024, doi:10.1145/3660773.                            Schwitalla, and Jan F. Nygård. LLMs in the heart of differential
 [92] Xinyi Hou, Yanjie Zhao, Yue Liu, Zhou Yang, Kailong Wang, Li Li,                         testing: A case study on a medical rule engine. In IEEE Confer-
      Xiapu Luo, David Lo, John Grundy, and Haoyu Wang. Large lan-                             ence on Software Testing, Verification and Validation, ICST 2025,
      guage models for software engineering: A systematic literature re-                       Napoli, Italy, March 31 - April 4, 2025, pages 429–440. IEEE, 2025,
      view. ACM Trans. Softw. Eng. Methodol., 33(8):220:1–220:79, 2024,                        doi:10.1109/ICST62969.2025.10989025.
      doi:10.1145/3695988.                                                               [107] Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun
 [93] David Hovemeyer and William W. Pugh.                       Finding bugs                  Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica.
      is easy.        ACM SIGPLAN Notices, 39(12):92–106, 2004,                                LiveCodeBench: Holistic and contamination free evaluation of large
      doi:10.1145/1052883.1052895.                                                             language models for code. In The Thirteenth International Conference
 [94] Jie Hu, Qian Zhang, and Heng Yin. Augmenting greybox fuzzing with                        on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025.
      generative AI, 2023, arXiv:2306.06782.                                                   OpenReview.net, 2025.
 [95] Sihao Hu, Tiansheng Huang, Fatih Ilhan, Selim Furkan Tekin, and Ling               [108] Nicholas Jalbert and Westley Weimer. Automated duplicate detection
      Liu. Large language model-powered smart contract vulnerability detec-                    for bug tracking systems. In The 38th Annual IEEE/IFIP International
      tion: New perspectives. In 5th IEEE International Conference on Trust,                   Conference on Dependable Systems and Networks, DSN 2008, June 24-
      Privacy and Security in Intelligent Systems and Applications, TPS-ISA                    27, 2008, Anchorage, Alaska, USA, Proceedings, pages 52–61. IEEE
      2023, Atlanta, GA, USA, November 1-4, 2023, pages 297–306. IEEE,                         Computer Society, 2008, doi:10.1109/DSN.2008.4630070.
      2023, doi:10.1109/TPS-ISA58951.2023.00044.                                         [109] Christian Janßen, Cedric Richter, and Heike Wehrheim. Can ChatGPT
 [96] Xing Hu, Zhuang Liu, Xin Xia, Zhongxin Liu, Tongtong Xu, and                             support software verification? In Dirk Beyer and Ana Cavalcanti, editors,
      Xiaohu Yang. Identify and update test cases when production code                         Fundamental Approaches to Software Engineering - 27th International
      changes: A transformer-based approach. In 38th IEEE/ACM Inter-                           Conference, FASE 2024, Held as Part of the European Joint Confer-
      national Conference on Automated Software Engineering, ASE 2023,                         ences on Theory and Practice of Software, ETAPS 2024, Luxembourg
      Luxembourg, September 11-15, 2023, pages 1111–1122. IEEE, 2023,                          City, Luxembourg, April 6-11, 2024, Proceedings, volume 14573 of
      doi:10.1109/ASE56229.2023.00165.                                                         Lecture Notes in Computer Science, pages 266–279. Springer, 2024,
 [97] Dong Huang, Qingwen Bu, Yuhao Qing, and Heming Cui. CodeCoT:                             doi:10.1007/978-3-031-57259-3 13.
      Tackling code syntax errors in CoT reasoning for code generation, 2024,            [110] Hiranya Jayathilaka, Chandra Krintz, and Rich Wolski. Performance mon-
      arXiv:2308.08784.                                                                        itoring and root cause analysis for cloud-hosted web applications. In Rick
 [98] Dong Huang, Qingwen Bu, Jie M. Zhang, Michael Luck, and Heming                           Barrett, Rick Cummings, Eugene Agichtein, and Evgeniy Gabrilovich,
      Cui. AgentCoder: Multi-agent-based code generation with iterative                        editors, Proceedings of the 26th International Conference on World Wide
      testing and optimisation, 2024, arXiv:2312.13010.                                        Web, WWW 2017, Perth, Australia, April 3-7, 2017, pages 469–478.
 [99] Linghan Huang, Peizhou Zhao, Lei Ma, and Huaming Chen. On                                ACM, 2017, doi:10.1145/3038912.3052649.
      the challenges of fuzzing techniques via large language models. In                 [111] Rasmus Ingemann Tuffveson Jensen, Vali Tawosi, and Salwa Alamir.
      Rong N. Chang, Carl K. Chang, Jingwei Yang, Nimanthi Atukorala, Dan                      Software vulnerability and functionality assessment using large language
      Chen, Sumi Helal, Sasu Tarkoma, Qiang He, Tevfik Kosar, Claudio A.                       models. In Maliheh Izadi, Andrea Di Sorbo, and Sebastiano Panichella,
      Ardagna, Javier Berrocal, Kaoutar El Maghaouri, and Yanchun Sun, edi-                    editors, Proceedings of the Third ACM/IEEE International Workshop on
      tors, IEEE International Conference on Software Services Engineering,                    NL-based Software Engineering, NLBSE 2024, Lisbon, Portugal, 20 April
      SSE 2025, Helsinki, Finland, July 7-12, 2025, pages 162–171. IEEE,                       2024, pages 25–28. ACM, 2024, doi:10.1145/3643787.3648036.
      2025, doi:10.1109/SSE67621.2025.00028.                                             [112] Ranjit Jhala and Rupak Majumdar. Software model checking. ACM Com-
[100] Qing Huang, Zhou Zou, Zhenchang Xing, Zhenkang Zuo, Xiwei Xu,                            put. Surv., 41(4):21:1–21:54, 2009, doi:10.1145/1592434.1592438.
      and Qinghua Lu. AI chain on large language model for unsupervised                  [113] Yue Jia and Mark Harman. An analysis and survey of the development
      control flow graph generation for statically-typed partial code, 2023,                   of mutation testing. IEEE Trans. Software Eng., 37(5):649–678, 2011,
      arXiv:2306.00757.                                                                        doi:10.1109/TSE.2010.62.
[101] Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch. Lan-               [114] Zongze Jiang, Ming Wen, Jialun Cao, Xuanhua Shi, and Hai Jin. Towards
      guage models as zero-shot planners: Extracting actionable knowledge                      understanding the effectiveness of large language models on directed test
      for embodied agents. In Kamalika Chaudhuri, Stefanie Jegelka, Le Song,                   input generation. In Proceedings of the 39th IEEE/ACM International
      Csaba Szepesvári, Gang Niu, and Sivan Sabato, editors, International                    Conference on Automated Software Engineering, ASE 2024, Sacramento,
      Conference on Machine Learning, ICML 2022, 17-23 July 2022, Balti-                       CA, USA, October 27 - November 1, 2024, pages 1408–1420. ACM,
      more, Maryland, USA, volume 162 of Proceedings of Machine Learning                       2024, doi:10.1145/3691620.3695513.
      Research, pages 9118–9147. PMLR, 2022.                                             [115] Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin
[102] Xiaowei Huang, Daniel Kroening, Wenjie Ruan, James Sharp, Youcheng                       Pei, Ofir Press, and Karthik R. Narasimhan. Swe-bench: Can language
      Sun, Emese Thamo, Min Wu, and Xinping Yi. A survey of safety and                         models resolve real-world github issues? In The Twelfth International
      trustworthiness of deep neural networks: Verification, testing, adversarial              Conference on Learning Representations, ICLR 2024, Vienna, Austria,
      attack and defence, and interpretability. Comput. Sci. Rev., 37:100270,                  May 7-11, 2024. OpenReview.net, 2024.
      2020, doi:10.1016/J.COSREV.2020.100270.                                            [116] Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn
[103] Yiheng Huang, Ruisi Wang, Wen Zheng, Zhuotong Zhou, Susheng Wu,                          Drain, Ethan Perez, Nicholas Schiefer, Zac Hatfield-Dodds, Nova Das-
      Shulin Ke, Bihuan Chen, Shan Gao, and Xin Peng. SpiderScan: Practical                    Sarma, Eli Tran-Johnson, Scott Johnston, Sheer El Showk, Andy Jones,
      detection of malicious NPM packages based on graph-based behavior                        Nelson Elhage, Tristan Hume, Anna Chen, Yuntao Bai, Sam Bowman,
      modeling and matching. In Vladimir Filkov, Baishakhi Ray, and Minghui                    Stanislav Fort, Deep Ganguli, Danny Hernandez, Josh Jacobson, Jackson
      Zhou, editors, Proceedings of the 39th IEEE/ACM International Confer-                    Kernion, Shauna Kravec, Liane Lovitt, Kamal Ndousse, Catherine Olsson,
      ence on Automated Software Engineering, ASE 2024, Sacramento, CA,                        Sam Ringer, Dario Amodei, Tom Brown, Jack Clark, Nicholas Joseph,
      USA, October 27 - November 1, 2024, pages 1146–1158. ACM, 2024,                          Ben Mann, Sam McCandlish, Chris Olah, and Jared Kaplan. Language
      doi:10.1145/3691620.3695492.                                                             models (mostly) know what they know, 2022, arXiv:2207.05221.
[104] Yuchao Huang, Junjie Wang, Zhe Liu, Yawen Wang, Song Wang, Chun-                   [117] Siva Kesava Reddy Kakarla and Ryan Beckett. Oracle-based protocol
      yang Chen, Yuanzhe Hu, and Qing Wang. CrashTranslator: Automatically                     testing with Eywa, 2023, arXiv:2312.06875.
      reproducing mobile application crashes directly from stack trace. In 46th          [118] Adam Tauman Kalai, Ofir Nachum, Santosh S. Vempala, and Edwin
      IEEE/ACM International Conference on Software Engineering, ICSE                          Zhang. Why language models hallucinate, 2025, arXiv:2509.04664.
      2024, Lisbon, Portugal, April 14-20, 2024, pages 18:1–18:13. ACM,                  [119] Adharsh Kamath, Nausheen Mohammed, Aditya Senthilnathan, Saikat
      2024, doi:10.1145/3597503.3623298.                                                       Chakraborty, Pantazis Deligiannis, Shuvendu K. Lahiri, Akash Lal,


                                                                                    28
      Aseem Rastogi, Subhajit Roy, and Rahul Sharma. Leveraging LLMs                        International Conference on Software Engineering, ICSE 2023, Mel-
      for program verification. In Nina Narodytska and Philipp Rümmer,                     bourne, Australia, May 14-20, 2023, pages 919–931. IEEE, 2023,
      editors, Formal Methods in Computer-Aided Design, FMCAD 2024,                         doi:10.1109/ICSE48619.2023.00085.
      Prague, Czech Republic, October 15-18, 2024, pages 107–118. IEEE,               [137] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir
      2024, doi:10.34727/2024/ISBN.978-3-85448-065-5 16.                                    Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau
[120] Sungmin Kang, Gabin An, and Shin Yoo. A quantitative and qualitative                  Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. Retrieval-
      evaluation of LLM-based explainable fault localization. Proc. ACM Softw.              augmented generation for knowledge-intensive NLP tasks. In Proceed-
      Eng., 1(FSE):1424–1446, 2024, doi:10.1145/3660771.                                    ings of the 34th International Conference on Neural Information Process-
[121] Sungmin Kang, Bei Chen, Shin Yoo, and Jian-Guang Lou. Ex-                             ing Systems, NIPS ’20, 2020.
      plainable automated debugging via large language model-driven                   [138] Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian. Enhancing
      scientific debugging.         Empir. Softw. Eng., 30(2):45, 2025,                     static analysis for practical bug detection: An LLM-integrated ap-
      doi:10.1007/S10664-024-10594-X.                                                       proach. Proc. ACM Program. Lang., 8(OOPSLA1):474–499, 2024,
[122] Sungmin Kang, Juyeon Yoon, and Shin Yoo. Large language models                        doi:10.1145/3649828.
      are few-shot testers: Exploring LLM-based general bug reproduction.             [139] Kefan Li and Yuan Yuan. Large language models as test case generators:
      In 45th IEEE/ACM International Conference on Software Engineering,                    Performance evaluation and enhancement, 2024, arXiv:2404.13340.
      ICSE 2023, Melbourne, Australia, May 14-20, 2023, pages 2312–2323.              [140] Tsz-On Li, Wenxi Zong, Yibo Wang, Haoye Tian, Ying Wang, Shing-Chi
      IEEE, 2023, doi:10.1109/ICSE48619.2023.00194.                                         Cheung, and Jeff Kramer. Nuances are the key: Unlocking ChatGPT to
[123] Moe Kayali, Fabian Wenz, Nesime Tatbul, and Çağatay Demiralp. Mind                  find failure-inducing tests with differential prompting. In 38th IEEE/ACM
      the data gap: Bridging LLMs to enterprise data integration, 2024,                     International Conference on Automated Software Engineering, ASE 2023,
      arXiv:2412.20331.                                                                     Kirchberg, Luxembourg, September 11-15, 2023, pages 1:1–1:13. ACM,
[124] Ahmed Khanfir, Renzo Degiovanni, Mike Papadakis, and Yves Le                          2023, doi:10.1145/3551349.3560420.
      Traon. Efficient mutation testing via pre-trained language models, 2023,        [141] Xia Li, Jiajun Jiang, Samuel Benton, Yingfei Xiong, and Lingming
      arXiv:2301.03543.                                                                     Zhang. A large-scale study on API misuses in the wild. In 14th IEEE
[125] Avishree Khare, Saikat Dutta, Ziyang Li, Alaia Solko-Breslin, Ra-                     Conference on Software Testing, Verification and Validation, ICST 2021,
      jeev Alur, and Mayur Naik. Understanding the effectiveness of large                   Porto de Galinhas, Brazil, April 12-16, 2021, pages 241–252. IEEE,
      language models in detecting security vulnerabilities. In IEEE Con-                   2021, doi:10.1109/ICST49551.2021.00034.
      ference on Software Testing, Verification and Validation, ICST 2025,            [142] Xiang Lisa Li and Percy Liang. Prefix-tuning: Optimizing continu-
      Napoli, Italy, March 31 - April 4, 2025, pages 103–114. IEEE, 2025,                   ous prompts for generation. In Chengqing Zong, Fei Xia, Wenjie Li,
      doi:10.1109/ICST62969.2025.10988968.                                                  and Roberto Navigli, editors, Proceedings of the 59th Annual Meeting
[126] Anant Kharkar, Roshanak Zilouchian Moghaddam, Matthew Jin, Xi-                        of the Association for Computational Linguistics and the 11th Interna-
      aoyu Liu, Xin Shi, Colin B. Clement, and Neel Sundaresan. Learning                    tional Joint Conference on Natural Language Processing, ACL/IJCNLP
      to reduce false positives in analytic bug detectors. In 44th IEEE/ACM                 2021, (Volume 1: Long Papers), Virtual Event, August 1-6, 2021,
      International Conference on Software Engineering, ICSE 2022, Pitts-                   pages 4582–4597. Association for Computational Linguistics, 2021,
      burgh, PA, USA, May 25-27, 2022, pages 1307–1316. ACM, 2022,                          doi:10.18653/V1/2021.ACL-LONG.353.
      doi:10.1145/3510003.3510153.                                                    [143] Zhen Li, Deqing Zou, Shouhuai Xu, Xinyu Ou, Hai Jin, Sujuan Wang,
[127] Omar Khattab, Arnav Singhvi, Paridhi Maheshwari, Zhiyuan Zhang,                       Zhijun Deng, and Yuyi Zhong. VulDeePecker: A deep learning-
      Keshav Santhanam, Sri Vardhamanan, Saiful Haq, Ashutosh Sharma,                       based system for vulnerability detection. In 25th Annual Network
      Thomas T. Joshi, Hanna Moazam, Heather Miller, Matei Zaharia, and                     and Distributed System Security Symposium, NDSS 2018, San Diego,
      Christopher Potts. DSPy: Compiling declarative language model calls                   California, USA, February 18-21, 2018. The Internet Society, 2018,
      into state-of-the-art pipelines. In The Twelfth International Conference              doi:10.14722/ndss.2018.23158.
      on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11,              [144] Guanjun Lin, Sheng Wen, Qing-Long Han, Jun Zhang, and
      2024. OpenReview.net, 2024.                                                           Yang Xiang.        Software vulnerability detection using deep neu-
[128] Myeongsoo Kim, Tyler Stennett, Dhruv Shah, Saurabh Sinha, and                         ral networks: A survey. Proc. IEEE, 108(10):1825–1848, 2020,
      Alessandro Orso. Leveraging large language models to improve REST                     doi:10.1109/JPROC.2020.2993293.
      API testing. In Proceedings of the 2024 ACM/IEEE 44th International             [145] Kaibo Liu, Zhenpeng Chen, Yiyang Liu, Jie M. Zhang, Mark Harman,
      Conference on Software Engineering: New Ideas and Emerging Results,                   Yudong Han, Yun Ma, Yihong Dong, Ge Li, and Gang Huang. LLM-
      NIER@ICSE 2024, Lisbon, Portugal, April 14-20, 2024, pages 37–41.                     powered test case generation for detecting bugs in plausible programs.
      ACM, 2024, doi:10.1145/3639476.3639769.                                               In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Moham-
[129] Jan Hendrik Kirchner, Yining Chen, Harri Edwards, Jan Leike, Nat                      mad Taher Pilehvar, editors, Proceedings of the 63rd Annual Meeting of
      McAleese, and Yuri Burda. Prover-verifier games improve legibility of                 the Association for Computational Linguistics (Volume 1: Long Papers),
      LLM outputs, 2024, arXiv:2407.13692.                                                  ACL 2025, Vienna, Austria, July 27 - August 1, 2025, pages 430–440.
[130] Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and                    Association for Computational Linguistics, 2025.
      Yusuke Iwasawa. Large language models are zero-shot reasoners. In               [146] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele
      NeurIPS, 2022.                                                                        Bevilacqua, Fabio Petroni, and Percy Liang. Lost in the middle: How
[131] Daphne Koller and Nir Friedman. Probabilistic Graphical Models -                      language models use long contexts. Trans. Assoc. Comput. Linguistics,
      Principles and Techniques. MIT Press, 2009.                                           12:157–173, 2024, doi:10.1162/TACL A 00638.
[132] Terry Koo, Frederick Liu, and Luheng He. Automata-based constraints             [147] Pengfei Liu, Weizhe Yuan, Jinlan Fu, Zhengbao Jiang, Hiroaki Hayashi,
      for language model decoding, 2024, arXiv:2407.08103.                                  and Graham Neubig. Pre-train, prompt, and predict: A systematic survey
[133] Leslie Lamport. The temporal logic of actions. ACM Trans. Program.                    of prompting methods in natural language processing. ACM Comput.
      Lang. Syst., 16(3):872–923, 1994, doi:10.1145/177492.177726.                          Surv., 55(9):195:1–195:35, 2023, doi:10.1145/3560815.
[134] K. Rustan M. Leino. Dafny: An automatic program verifier for                    [148] Puzhuo Liu, Chengnian Sun, Yaowen Zheng, Xuan Feng, Chuan Qin,
      functional correctness. In Edmund M. Clarke and Andrei Voronkov,                      Yuncheng Wang, Zhenyang Xu, Zhi Li, Peng Di, Yu Jiang, and Limin
      editors, Logic for Programming, Artificial Intelligence, and Reason-                  Sun. LLM-powered static binary taint analysis. ACM Trans. Softw. Eng.
      ing - 16th International Conference, LPAR-16, Dakar, Senegal, April                   Methodol., 34(3):83:1–83:36, 2025, doi:10.1145/3711816.
      25-May 1, 2010, Revised Selected Papers, volume 6355 of Lec-                    [149] Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai,
      ture Notes in Computer Science, pages 348–370. Springer, 2010,                        Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang,
      doi:10.1007/978-3-642-17511-4 20.                                                     Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen,
[135] K. Rustan M. Leino. Program Proofs. MIT Press, 2023.                                  Tianjun Zhang, Yu Su, Huan Sun, Minlie Huang, Yuxiao Dong, and Jie
[136] Caroline Lemieux, Jeevana Priya Inala, Shuvendu K. Lahiri, and Sid-                   Tang. AgentBench: Evaluating LLMs as agents. In The Twelfth Inter-
      dhartha Sen. CodaMOSA: Escaping coverage plateaus in test gen-                        national Conference on Learning Representations, ICLR 2024, Vienna,
      eration with pre-trained large language models. In 45th IEEE/ACM                      Austria, May 7-11, 2024. OpenReview.net, 2024.


                                                                                 29
[150] Yang Liu. Fine-tune BERT for extractive summarization, 2019,                             Res., 2025, 2025.
      arXiv:1903.10318.                                                                  [163] Zohar Manna and Amir Pnueli.                The temporal logic of re-
[151] Ye Liu, Yue Xue, Daoyuan Wu, Yuqiang Sun, Yi Li, Miaolei Shi, and                        active and concurrent systems - specification.          Springer, 1992,
      Yang Liu. PropertyGPT: LLM-driven formal verification of smart con-                      doi:10.1007/978-1-4612-0931-7.
      tracts through retrieval-augmented property generation. In 32nd Annual             [164] Ke Mao, Mark Harman, and Yue Jia. Sapienz: multi-objective
      Network and Distributed System Security Symposium, NDSS 2025, San                        automated testing for android applications.          In Andreas Zeller
      Diego, California, USA, February 24-28, 2025. The Internet Society,                      and Abhik Roychoudhury, editors, Proceedings of the 25th Inter-
      2025.                                                                                    national Symposium on Software Testing and Analysis, ISSTA 2016,
[152] Yi Liu, Junzhe Yu, Huijia Sun, Ling Shi, Gelei Deng, Yuqi Chen,                          Saarbrücken, Germany, July 18-20, 2016, pages 94–105. ACM, 2016,
      and Yang Liu. Efficient detection of toxic prompts in large language                     doi:10.1145/2931037.2931054.
      models. In Vladimir Filkov, Baishakhi Ray, and Minghui Zhou, ed-                   [165] Michael C. Martin, V. Benjamin Livshits, and Monica S. Lam. Find-
      itors, Proceedings of the 39th IEEE/ACM International Conference                         ing application errors and security flaws using PQL: a program query
      on Automated Software Engineering, ASE 2024, Sacramento, CA,                             language. In Ralph E. Johnson and Richard P. Gabriel, editors, Proceed-
      USA, October 27 - November 1, 2024, pages 455–467. ACM, 2024,                            ings of the 20th Annual ACM SIGPLAN Conference on Object-Oriented
      doi:10.1145/3691620.3695018.                                                             Programming, Systems, Languages, and Applications, OOPSLA 2005,
[153] Yue Liu, Sin Kit Lo, Qinghua Lu, Liming Zhu, Dehai Zhao, Xiwei                           October 16-20, 2005, San Diego, CA, USA, pages 365–383. ACM, 2005,
      Xu, Stefan Harrer, and Jon Whittle. Agent design pattern catalogue: A                    doi:10.1145/1094811.1094840.
      collection of architectural patterns for foundation model based agents. J.         [166] Clara Meister, Gian Wiher, and Ryan Cotterell. On decoding strategies for
      Syst. Softw., 220:112278, 2025, doi:10.1016/J.JSS.2024.112278.                           neural text generators. Trans. Assoc. Comput. Linguistics, 10:997–1012,
[154] Zhe Liu, Chunyang Chen, Junjie Wang, Xing Che, Yuekai Huang, Jun                         2022, doi:10.1162/TACL A 00502.
      Hu, and Qing Wang. Fill in the blank: Context-aware automated                      [167] Clara Meister, Gian Wiher, Tiago Pimentel, and Ryan Cotterell. High
      text input generation for mobile GUI testing. In 45th IEEE/ACM                           probability or low information? the probability-quality paradox in lan-
      International Conference on Software Engineering, ICSE 2023, Mel-                        guage generation. In Smaranda Muresan, Preslav Nakov, and Aline Villav-
      bourne, Australia, May 14-20, 2023, pages 1355–1367. IEEE, 2023,                         icencio, editors, Proceedings of the 60th Annual Meeting of the Associa-
      doi:10.1109/ICSE48619.2023.00119.                                                        tion for Computational Linguistics (Volume 2: Short Papers), ACL 2022,
[155] Zhe Liu, Chunyang Chen, Junjie Wang, Mengzhuo Chen, Boyu Wu, Xing                        Dublin, Ireland, May 22-27, 2022, pages 36–45. Association for Compu-
      Che, Dandan Wang, and Qing Wang. Make LLM a testing expert: Bring-                       tational Linguistics, 2022, doi:10.18653/V1/2022.ACL-SHORT.5.
      ing human-like interaction to mobile GUI testing via functionality-aware           [168] Ruijie Meng, Martin Mirchev, Marcel Böhme, and Abhik Roychoudhury.
      decisions. In 46th IEEE/ACM International Conference on Software                         Large language model guided protocol fuzzing. In Network and Dis-
      Engineering, ICSE 2024, Lisbon, Portugal, April 14-20, 2024, pages                       tributed System Security (NDSS) Symposium 2024, 26 February - 1 March
      100:1–100:13. ACM, 2024, doi:10.1145/3597503.3639180.                                    2024, San Diego, CA, USA, 2024, doi:10.14722/ndss.2024.24556.
[156] Zhe Liu, Chunyang Chen, Junjie Wang, Mengzhuo Chen, Boyu Wu,                       [169] Barton P. Miller, Lars Fredriksen, and Bryan So. An empirical study of
      Zhilin Tian, Yuekai Huang, Jun Hu, and Qing Wang. Testing the lim-                       the reliability of UNIX utilities. Commun. ACM, 33(12):32–44, 1990,
      its: Unusual text inputs generation for mobile app crash detection with                  doi:10.1145/96267.96279.
      large language model. In 46th IEEE/ACM International Conference on                 [170] Md Rakib Hossain Misu, Cristina V. Lopes, Iris Ma, and James Noble.
      Software Engineering, ICSE 2024, Lisbon, Portugal, April 14-20, 2024,                    Towards AI-assisted synthesis of verified Dafny methods. Proc. ACM
      pages 137:1–137:12. ACM, 2024, doi:10.1145/3597503.3639118.                              Softw. Eng., 1(FSE):812–835, 2024, doi:10.1145/3643763.
[157] Benjamin Livshits, Manu Sridharan, Yannis Smaragdakis, Ondrej                      [171] Mohammad Mahdi Mohajer, Reem Aleithan, Nima Shiri Harzevili,
      Lhoták, José Nelson Amaral, Bor-Yuh Evan Chang, Samuel Z. Guyer,                       Moshi Wei, Alvine Boaye Belle, Hung Viet Pham, and Song Wang.
      Uday P. Khedker, Anders Møller, and Dimitrios Vardoulakis. In de-                        Effectiveness of ChatGPT for static analysis: How far are we? In Bram
      fense of soundiness: a manifesto. Commun. ACM, 58(2):44–46, 2015,                        Adams, Thomas Zimmermann, Ipek Ozkaya, Dayi Lin, and Jie M. Zhang,
      doi:10.1145/2644805.                                                                     editors, Proceedings of the 1st ACM International Conference on AI-
[158] Guilong Lu, Xiaolin Ju, Xiang Chen, Wenlong Pei, and Zhilong Cai.                        Powered Software, AIware 2024, Porto de Galinhas, Brazil, July 15-16,
      GRACE: Empowering LLM-based software vulnerability detection with                        2024. ACM, 2024, doi:10.1145/3664646.3664777.
      graph structure and in-context learning. J. Syst. Softw., 212:112031, 2024,        [172] Amr Mansour Mohsen, Hesham A. Hassan, Khaled Wassif, Ra-
      doi:10.1016/J.JSS.2024.112031.                                                           madan Moawad, and Soha Makady. Enhancing bug localization us-
[159] Yao Lu, Max Bartolo, Alastair Moore, Sebastian Riedel, and Pontus                        ing phase-based approach. IEEE Access, 11:35901–35913, 2023,
      Stenetorp. Fantastically ordered prompts and where to find them: Over-                   doi:10.1109/ACCESS.2023.3265731.
      coming few-shot prompt order sensitivity. In Smaranda Muresan, Preslav             [173] Fangwen Mu, Lin Shi, Song Wang, Zhuohao Yu, Binquan Zhang,
      Nakov, and Aline Villavicencio, editors, Proceedings of the 60th An-                     Chenxue Wang, Shichao Liu, and Qing Wang. ClarifyGPT: A
      nual Meeting of the Association for Computational Linguistics (Vol-                      framework for enhancing LLM-based code generation via require-
      ume 1: Long Papers), ACL 2022, Dublin, Ireland, May 22-27, 2022,                         ments clarification. Proc. ACM Softw. Eng., 1(FSE):2332–2354, 2024,
      pages 8086–8098. Association for Computational Linguistics, 2022,                        doi:10.1145/3660810.
      doi:10.18653/V1/2022.ACL-LONG.556.                                                 [174] Jesse Mu, Xiang Li, and Noah D. Goodman. Learning to compress
[160] Dipeeka Luitel, Shiva Nejati, and Mehrdad Sabetzadeh. Requirements-                      prompts with gist tokens. In Alice Oh, Tristan Naumann, Amir Globerson,
      driven slicing of Simulink models using LLMs. In 32nd IEEE In-                           Kate Saenko, Moritz Hardt, and Sergey Levine, editors, Advances in
      ternational Requirements Engineering Conference, RE 2024 - Work-                         Neural Information Processing Systems 36: Annual Conference on Neural
      shops, Reykjavik, Iceland, June 24-25, 2024, pages 72–82. IEEE, 2024,                    Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA,
      doi:10.1109/REW61692.2024.00014.                                                         USA, December 10 - 16, 2023, 2023.
[161] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. SpecGen:                  [175] Satish Narayanasamy, Gilles Pokam, and Brad Calder. Bugnet: Continu-
      Automated generation of formal program specifications via large lan-                     ously recording program execution for deterministic replay debugging. In
      guage models. In 47th IEEE/ACM International Conference on Software                      32st International Symposium on Computer Architecture (ISCA 2005), 4-
      Engineering, ICSE 2025, Ottawa, ON, Canada, April 26 - May 6, 2025,                      8 June 2005, Madison, Wisconsin, USA, pages 284–295. IEEE Computer
      pages 16–28. IEEE, 2025, doi:10.1109/ICSE55347.2025.00129.                               Society, 2005, doi:10.1109/ISCA.2005.16.
[162] Laura Manduchi, Clara Meister, Kushagra Pandey, Robert Bamler, Ryan                [176] Noor Nashid, Mifta Sintaha, and Ali Mesbah. Retrieval-based prompt
      Cotterell, Sina Däubener, Sophie Fellenz, Asja Fischer, Thomas Gärtner,                selection for code-related few-shot learning. In 45th IEEE/ACM In-
      Matthias Kirchler, Marius Kloft, Yingzhen Li, Christoph Lippert, Gerard                  ternational Conference on Software Engineering, ICSE 2023, Mel-
      de Melo, Eric T. Nalisnick, Björn Ommer, Rajesh Ranganath, Maja                         bourne, Australia, May 14-20, 2023, pages 2450–2462. IEEE, 2023,
      Rudolph, Karen Ullrich, Guy Van den Broeck, Julia E. Vogt, Yixin Wang,                   doi:10.1109/ICSE48619.2023.00205.
      Florian Wenzel, Frank Wood, Stephan Mandt, and Vincent Fortuin. On                 [177] Ansong Ni, Srini Iyer, Dragomir Radev, Veselin Stoyanov, Wen-Tau Yih,
      the challenges and opportunities in generative AI. Trans. Mach. Learn.                   Sida I. Wang, and Xi Victoria Lin. LEVER: learning to verify language-


                                                                                    30
      to-code generation with execution. In Andreas Krause, Emma Brunskill,                   Cordeiro. LLM-generated invariants for bounded model checking with-
      Kyunghyun Cho, Barbara Engelhardt, Sivan Sabato, and Jonathan Scar-                     out loop unrolling. In Vladimir Filkov, Baishakhi Ray, and Minghui
      lett, editors, International Conference on Machine Learning, ICML 2023,                 Zhou, editors, Proceedings of the 39th IEEE/ACM International Confer-
      23-29 July 2023, Honolulu, Hawaii, USA, volume 202 of Proceedings of                    ence on Automated Software Engineering, ASE 2024, Sacramento, CA,
      Machine Learning Research, pages 26106–26128. PMLR, 2023.                               USA, October 27 - November 1, 2024, pages 1395–1407. ACM, 2024,
[178] Flemming Nielson, Hanne Riis Nielson, and Chris Han-                                    doi:10.1145/3691620.3695512.
      kin.        Principles of program analysis.             Springer, 1999,           [192] Juan Altmayer Pizzorno and Emery D. Berger. CoverUp: Effective high
      doi:10.1007/978-3-662-03811-6.                                                          coverage test generation for python. Proc. ACM Softw. Eng., 2(FSE):2897–
[179] Changan Niu, Chuanyi Li, Bin Luo, and Vincent Ng. Deep learning                         2919, 2025, doi:10.1145/3729398.
      meets software engineering: A survey on pre-trained models of source              [193] Gabriel Poesia, Kanishk Gandhi, Eric Zelikman, and Noah D. Goodman.
      code. In Luc De Raedt, editor, Thirty-First International Joint Conference              Certified deductive reasoning with language models. Trans. Mach. Learn.
      on Artificial Intelligence, IJCAI 2022, Vienna, Austria, 23-29 July 2022,               Res., 2024, 2024.
      pages 5546–5555. ijcai.org, 2022, doi:10.24963/IJCAI.2022/775.                    [194] Gabriel Poesia, Alex Polozov, Vu Le, Ashish Tiwari, Gustavo Soares,
[180] Yu Nong, Mohammed Aldeen, Long Cheng, Hongxin Hu, Feng                                  Christopher Meek, and Sumit Gulwani. Synchromesh: Reliable code
      Chen, and Haipeng Cai. Chain-of-thought prompting of large lan-                         generation from pre-trained language models. In The Tenth International
      guage models for discovering and fixing software vulnerabilities, 2024,                 Conference on Learning Representations, ICLR 2022, Virtual Event, April
      arXiv:2402.17230.                                                                       25-29, 2022. OpenReview.net, 2022.
[181] Yu Nong, Mohammed Aldeen, Long Cheng, Hongxin Hu, Feng                            [195] Ofir Press, Muru Zhang, Sewon Min, Ludwig Schmidt, Noah A.
      Chen, and Haipeng Cai. Chain-of-thought prompting of large lan-                         Smith, and Mike Lewis. Measuring and narrowing the composi-
      guage models for discovering and fixing software vulnerabilities, 2024,                 tionality gap in language models. In Houda Bouamor, Juan Pino,
      arXiv:2402.17230.                                                                       and Kalika Bali, editors, Findings of the Association for Computa-
[182] Yu Nong, Yuzhe Ou, Michael Pradel, Feng Chen, and Haipeng Cai.                          tional Linguistics: EMNLP 2023, Singapore, December 6-10, 2023,
      VULGEN: realistic vulnerability generation via pattern mining and deep                  pages 5687–5711. Association for Computational Linguistics, 2023,
      learning. In 45th IEEE/ACM International Conference on Software En-                     doi:10.18653/V1/2023.FINDINGS-EMNLP.378.
      gineering, ICSE 2023, Melbourne, Australia, May 14-20, 2023, pages                [196] Feng Qiu, Pu Ji, Baojian Hua, and Yang Wang. CHEMFUZZ:
      2527–2539. IEEE, 2023, doi:10.1109/ICSE48619.2023.00211.                                large language models-assisted fuzzing for quantum chemistry soft-
[183] Maxwell Nye, Anders Johan Andreassen, Guy Gur-Ari, Henryk                               ware bug detection. In 23rd IEEE International Conference on Soft-
      Michalewski, Jacob Austin, David Bieber, David Dohan, Aitor                             ware Quality, Reliability, and Security, QRS 2023 Companion, Chi-
      Lewkowycz, Maarten Bosma, David Luan, Charles Sutton, and Augustus                      ang Mai, Thailand, October 22-26, 2023, pages 103–112. IEEE, 2023,
      Odena. Show your work: Scratchpads for intermediate computation with                    doi:10.1109/QRS-C60940.2023.00104.
      language models, 2021, arXiv:2112.00114.                                          [197] Nikitha Rao, Kush Jain, Uri Alon, Claire Le Goues, and Vincent J. Hel-
[184] Oscar Obeso, Andy Arditi, Javier Ferrando, Joshua Freeman, Cameron                      lendoorn. CAT-LM training language models on aligned code and tests.
      Holmes, and Neel Nanda. Real-time detection of hallucinated entities in                 In 38th IEEE/ACM International Conference on Automated Software
      long-form generation, 2025, arXiv:2509.03531.                                           Engineering, ASE 2023, Luxembourg, September 11-15, 2023, pages
[185] Alessandro Orso and Gregg Rothermel. Software testing: a research                       409–420. IEEE, 2023, doi:10.1109/ASE56229.2023.00193.
      travelogue (2000-2014). In James D. Herbsleb and Matthew B. Dwyer,                [198] Adrian Rebmann, Fabian David Schmidt, Goran Glavaš, and Han van der
      editors, Proceedings of the on Future of Software Engineering, FOSE                     Aa. Evaluating the ability of LLMs to solve semantics-aware process
      2014, Hyderabad, India, May 31 - June 7, 2014, pages 117–132. ACM,                      mining tasks. In 6th International Conference on Process Mining, ICPM
      2014, doi:10.1145/2593882.2593885.                                                      2024, Kgs. Lyngby, Denmark, October 14-18, 2024, pages 9–16. IEEE,
[186] Carlos Pacheco, Shuvendu K. Lahiri, Michael D. Ernst, and Thomas                        2024, doi:10.1109/ICPM63005.2024.10680677.
      Ball. Feedback-directed random test generation. In 29th International             [199] Devjeet Roy, Xuchao Zhang, Rashi Bhave, Chetan Bansal, Pedro Hen-
      Conference on Software Engineering (ICSE 2007), Minneapolis, MN,                        rique B. Las-Casas, Rodrigo Fonseca, and Saravan Rajmohan. Explor-
      USA, May 20-26, 2007, pages 75–84. IEEE Computer Society, 2007,                         ing LLM-based agents for root cause analysis. In Marcelo d’Amorim,
      doi:10.1109/ICSE.2007.37.                                                               editor, Companion Proceedings of the 32nd ACM International Con-
[187] Spencer Pearson, José Campos, René Just, Gordon Fraser, Rui Abreu,                    ference on the Foundations of Software Engineering, FSE 2024, Porto
      Michael D. Ernst, Deric Pang, and Benjamin Keller. Evaluating and                       de Galinhas, Brazil, July 15-19, 2024, pages 208–219. ACM, 2024,
      improving fault localization. In Sebastián Uchitel, Alessandro Orso,                   doi:10.1145/3663529.3663841.
      and Martin P. Robillard, editors, Proceedings of the 39th Interna-                [200] Alexander M. Rush, Sumit Chopra, and Jason Weston. A neural attention
      tional Conference on Software Engineering, ICSE 2017, Buenos Aires,                     model for abstractive sentence summarization. In Lluı́s Màrquez, Chris
      Argentina, May 20-28, 2017, pages 609–620. IEEE / ACM, 2017,                            Callison-Burch, Jian Su, Daniele Pighin, and Yuval Marton, editors,
      doi:10.1109/ICSE.2017.62.                                                               Proceedings of the 2015 Conference on Empirical Methods in Natural
[188] Kexin Pei, David Bieber, Kensen Shi, Charles Sutton, and Pengcheng                      Language Processing, EMNLP 2015, Lisbon, Portugal, September 17-21,
      Yin. Can large language models reason about program invariants? In                      2015, pages 379–389. The Association for Computational Linguistics,
      Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara Engelhardt,                      2015, doi:10.18653/V1/D15-1044.
      Sivan Sabato, and Jonathan Scarlett, editors, International Conference            [201] Gabriel Ryan, Siddhartha Jain, Mingyue Shang, Shiqi Wang, Xiaofei
      on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu, Hawaii,                      Ma, Murali Krishna Ramanathan, and Baishakhi Ray. Code-aware
      USA, volume 202 of Proceedings of Machine Learning Research, pages                      prompting: A study of coverage-guided test generation in regression
      27496–27520. PMLR, 2023.                                                                setting using LLM. Proc. ACM Softw. Eng., 1(FSE):951–971, 2024,
[189] Kai Petersen, Robert Feldt, Shahid Mujtaba, and Michael Mattsson. Sys-                  doi:10.1145/3643769.
      tematic mapping studies in software engineering. In Giuseppe Visaggio,            [202] S. C. Johnson. Lint, a C program checker, 1978.
      Maria Teresa Baldassarre, Stephen G. Linkman, and Mark Turner, editors,           [203] Shubhra Kanti Karmaker Santu and Dongji Feng. TELeR: A general
      12th International Conference on Evaluation and Assessment in Software                  taxonomy of LLM prompts for benchmarking complex tasks. In Houda
      Engineering, EASE 2008, University of Bari, Italy, 26-27 June 2008,                     Bouamor, Juan Pino, and Kalika Bali, editors, Findings of the Association
      Workshops in Computing. BCS, 2008.                                                      for Computational Linguistics: EMNLP 2023, Singapore, December 6-10,
[190] Hung Phan, Arushi Sharma, and Ali Jannesari. Generating context-                        2023, pages 14197–14203. Association for Computational Linguistics,
      aware API calls from natural language description using neural embed-                   2023, doi:10.18653/V1/2023.FINDINGS-EMNLP.946.
      dings and machine translation. In 36th IEEE/ACM International Con-                [204] Max Schäfer, Sarah Nadi, Aryaz Eghbali, and Frank Tip. An em-
      ference on Automated Software Engineering, ASE 2021 - Workshops,                        pirical evaluation of using large language models for automated unit
      Melbourne, Australia, November 15-19, 2021, pages 219–226. IEEE,                        test generation. IEEE Trans. Software Eng., 50(1):85–105, 2024,
      2021, doi:10.1109/ASEW52652.2021.00050.                                                 doi:10.1109/TSE.2023.3334955.
[191] Muhammad A. A. Pirzada, Giles Reger, Ahmed Bhayat, and Lucas C.                   [205] Timo Schick, Jane Dwivedi-Yu, Roberto Dessı̀, Roberta Raileanu, Maria


                                                                                   31
      Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola Cancedda, and Thomas                Chandan Singh, Charles Rathkopf, Chenlin Meng, Chitta Baral, Chiyu
      Scialom. Toolformer: Language models can teach themselves to use                  Wu, Chris Callison-Burch, Chris Waites, Christian Voigt, Christopher D.
      tools. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko,                 Manning, Christopher Potts, Cindy Ramirez, Clara E. Rivera, Clemencia
      Moritz Hardt, and Sergey Levine, editors, Advances in Neural Informa-             Siro, Colin Raffel, Courtney Ashcraft, Cristina Garbacea, Damien Sileo,
      tion Processing Systems 36: Annual Conference on Neural Information               Dan Garrette, Dan Hendrycks, Dan Kilman, Dan Roth, Daniel Free-
      Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, De-                  man, Daniel Khashabi, Daniel Levy, Daniel Moseguı́ González, Danielle
      cember 10 - 16, 2023, 2023.                                                       Perszyk, Danny Hernandez, Danqi Chen, Daphne Ippolito, Dar Gilboa,
[206] Shreya Shankar, J. D. Zamfirescu-Pereira, Bjoern Hartmann, Aditya G.              David Dohan, David Drakard, David Jurgens, Debajyoti Datta, Deep
      Parameswaran, and Ian Arawjo. Who validates the validators? aligning              Ganguli, Denis Emelin, Denis Kleyko, Deniz Yuret, Derek Chen, Derek
      LLM-assisted evaluation of LLM outputs with human preferences. In                 Tam, Dieuwke Hupkes, Diganta Misra, Dilyar Buzan, Dimitri Coelho
      Lining Yao, Mayank Goel, Alexandra Ion, and Pedro Lopes, editors, Pro-            Mollo, Diyi Yang, Dong-Ho Lee, Dylan Schrader, Ekaterina Shutova,
      ceedings of the 37th Annual ACM Symposium on User Interface Software              Ekin Dogus Cubuk, Elad Segal, Eleanor Hagerman, Elizabeth Barnes,
      and Technology, UIST 2024, Pittsburgh, PA, USA, October 13-16, 2024,              Elizabeth Donoway, Ellie Pavlick, Emanuele Rodolà, Emma Lam, Eric
      pages 131:1–131:14. ACM, 2024, doi:10.1145/3654777.3676450.                       Chu, Eric Tang, Erkut Erdem, Ernie Chang, Ethan A. Chi, Ethan Dyer,
[207] Prakhar Sharma and Vinod Yegneswaran. PROSPER: Extracting proto-                  Ethan J. Jerzak, Ethan Kim, Eunice Engefu Manyasi, Evgenii Zheltonozh-
      col specifications using large language models. In Proceedings of the             skii, Fanyue Xia, Fatemeh Siar, Fernando Martı́nez-Plumed, Francesca
      22nd ACM Workshop on Hot Topics in Networks, HotNets 2023, Cam-                   Happé, François Chollet, Frieda Rong, Gaurav Mishra, Genta Indra
      bridge, MA, USA, November 28-29, 2023, pages 41–47. ACM, 2023,                    Winata, Gerard de Melo, Germán Kruszewski, Giambattista Parascan-
      doi:10.1145/3626111.3628205.                                                      dolo, Giorgio Mariani, Gloria Wang, Gonzalo Jaimovitch-López, Gregor
[208] Kumar Shashwat, Francis Hahn, Xinming Ou, Dmitry Goldgof, Lawrence                Betz, Guy Gur-Ari, Hana Galijasevic, Hannah Kim, Hannah Rashkin,
      Hall, Jay Ligatti, S. Raj Rajgopalan, and Armin Ziaie Tabari. A prelimi-          Hannaneh Hajishirzi, Harsh Mehta, Hayden Bogar, Henry Shevlin, Hin-
      nary study on using large language models in software pentesting, 2024,           rich Schütze, Hiromu Yakura, Hongming Zhang, Hugh Mee Wong, Ian
      arXiv:2401.17459.                                                                 Ng, Isaac Noble, Jaap Jumelet, Jack Geissinger, Jackson Kernion, Jacob
[209] Jiho Shin, Sepehr Hashtroudi, Hadi Hemmati, and Song Wang. Domain                 Hilton, Jaehoon Lee, Jaime Fernández Fisac, James B. Simon, James
      adaptation for code model-based unit test case generation. In Maria               Koppel, James Zheng, James Zou, Jan Kocon, Jana Thompson, Janelle
      Christakis and Michael Pradel, editors, Proceedings of the 33rd ACM               Wingfield, Jared Kaplan, Jarema Radom, Jascha Sohl-Dickstein, Jason
      SIGSOFT International Symposium on Software Testing and Analysis,                 Phang, Jason Wei, Jason Yosinski, Jekaterina Novikova, Jelle Bosscher,
      ISSTA 2024, Vienna, Austria, September 16-20, 2024, pages 1211–1222.              Jennifer Marsh, Jeremy Kim, Jeroen Taal, Jesse H. Engel, Jesujoba Alabi,
      ACM, 2024, doi:10.1145/3650212.3680354.                                           Jiacheng Xu, Jiaming Song, Jillian Tang, Joan Waweru, John Burden,
[210] Seung Yeob Shin, Fabrizio Pastore, Domenico Bianculli, and Alexandra              John Miller, John U. Balis, Jonathan Batchelder, Jonathan Berant, Jörg
      Baicoianu. Towards generating executable metamorphic relations using              Frohberg, Jos Rozen, José Hernández-Orallo, Joseph Boudeman, Joseph
      large language models. In Antonia Bertolino, João Pascoal Faria, Patricia        Guerr, Joseph Jones, Joshua B. Tenenbaum, Joshua S. Rule, Joyce Chua,
      Lago, and Laura Semini, editors, Quality of Information and Commu-                Kamil Kanclerz, Karen Livescu, Karl Krauth, Karthik Gopalakrishnan,
      nications Technology - 17th International Conference on the Quality of            Katerina Ignatyeva, Katja Markert, Kaustubh D. Dhole, Kevin Gimpel,
      Information and Communications Technology, QUATIC 2024, Pisa, Italy,              Kevin Omondi, Kory Mathewson, Kristen Chiafullo, Ksenia Shkaruta,
      September 11-13, 2024, Proceedings, volume 2178 of Communications                 Kumar Shridhar, Kyle McDonell, Kyle Richardson, Laria Reynolds, Leo
      in Computer and Information Science, pages 126–141. Springer, 2024,               Gao, Li Zhang, Liam Dugan, Lianhui Qin, Lidia Contreras Ochando,
      doi:10.1007/978-3-031-70245-7 9.                                                  Louis-Philippe Morency, Luca Moschella, Lucas Lam, Lucy Noble, Lud-
[211] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan,                wig Schmidt, Luheng He, Luis Oliveros Colón, Luke Metz, Lütfi Kerem
      and Shunyu Yao. Reflexion: language agents with verbal reinforce-                 Senel, Maarten Bosma, Maarten Sap, Maartje ter Hoeve, Maheen Fa-
      ment learning. In Alice Oh, Tristan Naumann, Amir Globerson, Kate                 rooqi, Manaal Faruqui, Mantas Mazeika, Marco Baturan, Marco Marelli,
      Saenko, Moritz Hardt, and Sergey Levine, editors, Advances in Neural              Marco Maru, Marı́a José Ramı́rez-Quintana, Marie Tolkiehn, Mario Giu-
      Information Processing Systems 36: Annual Conference on Neural Infor-             lianelli, Martha Lewis, Martin Potthast, Matthew L. Leavitt, Matthias
      mation Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA,               Hagen, Mátyás Schubert, Medina Baitemirova, Melody Arnaud, Melvin
      December 10 - 16, 2023, 2023.                                                     McElrath, Michael A. Yee, Michael Cohen, Michael Gu, Michael I. Ivan-
[212] Mohammed Latif Siddiq, Joanna Cecilia da Silva Santos, Ridwanul Hasan             itskiy, Michael Starritt, Michael Strube, Michal Swedrowski, Michele
      Tanvir, Noshin Ulfat, Fahmid Al Rifat, and Vinicius Carvalho Lopes. Us-           Bevilacqua, Michihiro Yasunaga, Mihir Kale, Mike Cain, Mimee Xu,
      ing large language models to generate JUnit tests: An empirical study. In         Mirac Suzgun, Mitch Walker, Mo Tiwari, Mohit Bansal, Moin Amin-
      Proceedings of the 28th International Conference on Evaluation and As-            naseri, Mor Geva, Mozhdeh Gheini, Mukund Varma T., Nanyun Peng,
      sessment in Software Engineering, EASE 2024, Salerno, Italy, June 18-21,          Nathan A. Chi, Nayeon Lee, Neta Gur-Ari Krakover, Nicholas Cameron,
      2024, pages 313–322. ACM, 2024, doi:10.1145/3661167.3661216.                      Nicholas Roberts, Nick Doiron, Nicole Martinez, Nikita Nangia, Niklas
[213] Jacopo Soldani and Antonio Brogi. Anomaly detection and failure root              Deckers, Niklas Muennighoff, Nitish Shirish Keskar, Niveditha Iyer,
      cause analysis in (micro) service-based cloud applications: A survey.             Noah Constant, Noah Fiedel, Nuan Wen, Oliver Zhang, Omar Agha,
      ACM Comput. Surv., 55(3):59:1–59:39, 2023, doi:10.1145/3501297.                   Omar Elbaghdadi, Omer Levy, Owain Evans, Pablo Antonio Moreno
[214] Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao, Abu Awal Md Shoeb,              Casares, Parth Doshi, Pascale Fung, Paul Pu Liang, Paul Vicol, Pegah
      Abubakar Abid, Adam Fisch, Adam R. Brown, Adam Santoro, Aditya                    Alipoormolabashi, Peiyuan Liao, Percy Liang, Peter Chang, Peter Ecker-
      Gupta, Adrià Garriga-Alonso, Agnieszka Kluska, Aitor Lewkowycz,                  sley, Phu Mon Htut, Pinyu Hwang, Piotr Milkowski, Piyush Patil, Pouya
      Akshat Agarwal, Alethea Power, Alex Ray, Alex Warstadt, Alexan-                   Pezeshkpour, Priti Oli, Qiaozhu Mei, Qing Lyu, Qinlang Chen, Rabin
      der W. Kocurek, Ali Safaya, Ali Tazarv, Alice Xiang, Alicia Parrish,              Banjade, Rachel Etta Rudolph, Raefer Gabriel, Rahel Habacker, Ramon
      Allen Nie, Aman Hussain, Amanda Askell, Amanda Dsouza, Ambrose                    Risco, Raphaël Millière, Rhythm Garg, Richard Barnes, Rif A. Saurous,
      Slone, Ameet Rahane, Anantharaman S. Iyer, Anders Andreassen, An-                 Riku Arakawa, Robbe Raymaekers, Robert Frank, Rohan Sikand, Roman
      drea Madotto, Andrea Santilli, Andreas Stuhlmüller, Andrew M. Dai,               Novak, Roman Sitelew, Ronan LeBras, Rosanne Liu, Rowan Jacobs,
      Andrew La, Andrew K. Lampinen, Andy Zou, Angela Jiang, Angelica                   Rui Zhang, Ruslan Salakhutdinov, Ryan Chi, Ryan Lee, Ryan Stovall,
      Chen, Anh Vuong, Animesh Gupta, Anna Gottardi, Antonio Norelli, Anu               Ryan Teehan, Rylan Yang, Sahib Singh, Saif M. Mohammad, Sajant
      Venkatesh, Arash Gholamidavoodi, Arfa Tabassum, Arul Menezes, Arun                Anand, Sam Dillavou, Sam Shleifer, Sam Wiseman, Samuel Gruetter,
      Kirubarajan, Asher Mullokandov, Ashish Sabharwal, Austin Herrick,                 Samuel R. Bowman, Samuel S. Schoenholz, Sanghyun Han, Sanjeev
      Avia Efrat, Aykut Erdem, Ayla Karakas, B. Ryan Roberts, Bao Sheng                 Kwatra, Sarah A. Rous, Sarik Ghazarian, Sayan Ghosh, Sean Casey,
      Loe, Barret Zoph, Bartlomiej Bojanowski, Batuhan Özyurt, Behnam                  Sebastian Bischoff, Sebastian Gehrmann, Sebastian Schuster, Sepideh
      Hedayatnia, Behnam Neyshabur, Benjamin Inden, Benno Stein, Berk                   Sadeghi, Shadi Hamdan, Sharon Zhou, Shashank Srivastava, Sherry Shi,
      Ekmekci, Bill Yuchen Lin, Blake Howald, Bryan Orinion, Cameron Diao,              Shikhar Singh, Shima Asaadi, Shixiang Shane Gu, Shubh Pachchigar,
      Cameron Dour, Catherine Stinson, Cedrick Argueta, Cèsar Ferri Ramı́rez,          Shubham Toshniwal, Shyam Upadhyay, Shyamolima (Shammie) Deb-


                                                                                   32
      nath, Siamak Shakeri, Simon Thormeyer, Simone Melzi, Siva Reddy,                       Shuang Liu, Shengjian Guo, Yan-Fu Li, Lei Ma, Yinxing Xue, and Yang
      Sneha Priscilla Makini, Soo-Hwan Lee, Spencer Torene, Sriharsha Hat-                   Liu. A survey on automated driving system testing: Landscapes and
      war, Stanislas Dehaene, Stefan Divic, Stefano Ermon, Stella Biderman,                  trends. ACM Trans. Softw. Eng. Methodol., 32(5):124:1–124:62, 2023,
      Stephanie Lin, Stephen Prasad, Steven T. Piantadosi, Stuart M. Shieber,                doi:10.1145/3579642.
      Summer Misherghi, Svetlana Kiritchenko, Swaroop Mishra, Tal Linzen,              [225] Shuncheng Tang, Zhenya Zhang, Jixiang Zhou, Lei Lei, Yuan Zhou,
      Tal Schuster, Tao Li, Tao Yu, Tariq Ali, Tatsu Hashimoto, Te-Lin Wu,                   and Yinxing Xue. LeGEND: A top-down approach to scenario gen-
      Théo Desbordes, Theodore Rothschild, Thomas Phan, Tianle Wang,                        eration of autonomous driving systems assisted by large language
      Tiberius Nkinyili, Timo Schick, Timofei Kornev, Titus Tunduny, Tobias                  models. In Proceedings of the 39th IEEE/ACM International Confer-
      Gerstenberg, Trenton Chang, Trishala Neeraj, Tushar Khot, Tyler Shultz,                ence on Automated Software Engineering, ASE 2024, Sacramento, CA,
      Uri Shaham, Vedant Misra, Vera Demberg, Victoria Nyamai, Vikas Rau-                    USA, October 27 - November 1, 2024, pages 1497–1508. ACM, 2024,
      nak, Vinay V. Ramasesh, Vinay Uday Prabhu, Vishakh Padmakumar,                         doi:10.1145/3691620.3695520.
      Vivek Srikumar, William Fedus, William Saunders, William Zhang, Wout             [226] Yutian Tang, Zhijie Liu, Zhichao Zhou, and Xiapu Luo. Chat-
      Vossen, Xiang Ren, Xiaoyu Tong, Xinran Zhao, Xinyi Wu, Xudong                          GPT vs SBST: A comparative assessment of unit test suite gen-
      Shen, Yadollah Yaghoobzadeh, Yair Lakretz, Yangqiu Song, Yasaman                       eration.     IEEE Trans. Software Eng., 50(6):1340–1359, 2024,
      Bahri, Yejin Choi, Yichi Yang, Yiding Hao, Yifu Chen, Yonatan Belinkov,                doi:10.1109/TSE.2024.3382365.
      Yu Hou, Yufang Hou, Yuntao Bai, Zachary Seid, Zhuoye Zhao, Zijian                [227] Langchain Team.         LANGCHAIN BLOG: OpenAI’s bet on a
      Wang, Zijie J. Wang, Zirui Wang, and Ziyi Wu. Beyond the imitation                     cognitive architecture, 2023.       https://blog.langchain.dev/
      game: Quantifying and extrapolating the capabilities of language models.               openais-bet-on-a-cognitive-architecture/ [accessed July
      Trans. Mach. Learn. Res., 2023, 2023.                                                  2024].
[215] Yanqi Su, Dianshu Liao, Zhenchang Xing, Qing Huang, Mulong                       [228] Adly Templeton, Tom Conerly, Jonathan Marcus, Jack Lindsey, Trenton
      Xie, Qinghua Lu, and Xiwei Xu. Enhancing exploratory testing                           Bricken, Brian Chen, Adam Pearce, Craig Citro, Emmanuel Ameisen,
      by large language model and knowledge graph. In 46th IEEE/ACM                          Andy Jones, Hoagy Cunningham, Nicholas L Turner, Callum Mc-
      International Conference on Software Engineering, ICSE 2024, Lis-                      Dougall, Monte MacDiarmid, Alex Tamkin, Esin Durmus, Tristan Hume,
      bon, Portugal, April 14-20, 2024, pages 98:1–98:12. ACM, 2024,                         Francesco Mosconi, C. Daniel Freeman, Theodore R. Sumers, Edward
      doi:10.1145/3597503.3639157.                                                           Rees, Joshua Batson, Adam Jermyn, Shan Carter, Chris Olah, and
[216] Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan, and Thomas L.                      Tom Henighan. Scaling monosemanticity: Extracting interpretable
      Griffiths. Cognitive architectures for language agents. Trans. Mach.                   features from Claude 3 Sonnet. https://transformer-circuits.
      Learn. Res., 2024, 2024.                                                               pub/2024/scaling-monosemanticity/index.html, 2024.                    At
[217] Chuyue Sun, Ying Sheng, Oded Padon, and Clark W. Barrett. Clover:                      transformer-circuits.pub [accessed July 2024].
      Closed-loop verifiable code generation. In Guy Avni, Mirco Giacobbe,             [229] Norbert Tihanyi, Tamás Bisztray, Ridhi Jain, Mohamed Amine Ferrag,
      Taylor T. Johnson, Guy Katz, Anna Lukina, Nina Narodytska, and Chris-                  Lucas C. Cordeiro, and Vasileios Mavroeidis. The FormAI dataset:
      tian Schilling, editors, AI Verification - First International Symposium,              Generative AI in software security through the lens of formal verifi-
      SAIV 2024, Montreal, QC, Canada, July 22-23, 2024, Proceedings,                        cation. In Shane McIntosh, Eunjong Choi, and Steffen Herbold, edi-
      volume 14846 of Lecture Notes in Computer Science, pages 134–155.                      tors, Proceedings of the 19th International Conference on Predictive
      Springer, 2024, doi:10.1007/978-3-031-65112-0 7.                                       Models and Data Analytics in Software Engineering, PROMISE 2023,
[218] Maolin Sun, Yibiao Yang, Yang Wang, Ming Wen, Haoxiang Jia,                            San Francisco, CA, USA, 8 December 2023, pages 33–43. ACM, 2023,
      and Yuming Zhou. SMT solver validation empowered by large                              doi:10.1145/3617555.3617874.
      pre-trained language models.          In 38th IEEE/ACM International             [230] Frank Tip, Jonathan Bell, and Max Schäfer. LLMorpheus: Mutation test-
      Conference on Automated Software Engineering, ASE 2023, Lux-                           ing using large language models. IEEE Trans. Software Eng., 51(6):1645–
      embourg, September 11-15, 2023, pages 1288–1300. IEEE, 2023,                           1665, 2025, doi:10.1109/TSE.2025.3562025.
      doi:10.1109/ASE56229.2023.00180.                                                 [231] Christos Tsigkanos, Pooja Rani, Sebastian Müller, and Timo Kehrer.
[219] Yuqiang Sun, Daoyuan Wu, Yue Xue, Han Liu, Wei Ma, Lyuye Zhang,                        Large language models: The next frontier for variable discovery within
      Miaolei Shi, and Yang Liu. LLM4Vuln: A unified evaluation framework                    metamorphic testing? In Tao Zhang, Xin Xia, and Nicole Novielli, editors,
      for decoupling and enhancing LLMs’ vulnerability reasoning, 2024,                      IEEE International Conference on Software Analysis, Evolution and
      arXiv:2401.16185.                                                                      Reengineering, SANER 2023, Taipa, Macao, March 21-24, 2023, pages
[220] Yuqiang Sun, Daoyuan Wu, Yue Xue, Han Liu, Haijun Wang, Zhengzi                        678–682. IEEE, 2023, doi:10.1109/SANER56733.2023.00070.
      Xu, Xiaofei Xie, and Yang Liu. GPTScan: Detecting logic vulnerabilities          [232] Haoxin Tu, Zhide Zhou, He Jiang, Imam Nur Bani Yusuf, Yuxian Li,
      in smart contracts by combining GPT with program analysis. In 46th                     and Lingxiao Jiang. Isolating compiler bugs by generating effective
      IEEE/ACM International Conference on Software Engineering, ICSE                        witness programs with large language models. IEEE Trans. Software
      2024, Lisbon, Portugal, April 14-20, 2024, pages 166:1–166:13. ACM,                    Eng., 50(7):1768–1788, 2024, doi:10.1109/TSE.2024.3397822.
      2024, doi:10.1145/3597503.3639117.                                               [233] Michele Tufano, Dawn Drain, Alexey Svyatkovskiy, Shao Kun Deng,
[221] Mirac Suzgun, Nathan Scales, Nathanael Schärli, Sebastian Gehrmann,                   and Neel Sundaresan. Unit test case generation with transformers and
      Yi Tay, Hyung Won Chung, Aakanksha Chowdhery, Quoc V. Le, Ed H.                        focal context, 2021, arXiv:2009.05617.
      Chi, Denny Zhou, and Jason Wei. Challenging BIG-bench tasks and                  [234] Karthik Valmeekam, Matthew Marquez, Alberto Olmo Hernandez, Sarath
      whether chain-of-thought can solve them. In Anna Rogers, Jordan L.                     Sreedharan, and Subbarao Kambhampati. PlanBench: An extensible
      Boyd-Graber, and Naoaki Okazaki, editors, Findings of the Association                  benchmark for evaluating large language models on planning and reason-
      for Computational Linguistics: ACL 2023, Toronto, Canada, July 9-14,                   ing about change. In Alice Oh, Tristan Naumann, Amir Globerson, Kate
      2023, pages 13003–13051. Association for Computational Linguistics,                    Saenko, Moritz Hardt, and Sergey Levine, editors, Advances in Neural
      2023, doi:10.18653/V1/2023.FINDINGS-ACL.824.                                           Information Processing Systems 36: Annual Conference on Neural Infor-
[222] Maryam Taeb, Amanda Swearngin, Eldon Schoop, Ruijia Cheng, Yue                         mation Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA,
      Jiang, and Jeffrey Nichols. AXNav: Replaying accessibility tests                       December 10 - 16, 2023, 2023.
      from natural language. In Florian ’Floyd’ Mueller, Penny Kyburz,                 [235] Axel van Lamsweerde. Goal-oriented requirements engineering: A
      Julie R. Williamson, Corina Sas, Max L. Wilson, Phoebe O. Toups                        guided tour. In 5th IEEE International Symposium on Requirements
      Dugas, and Irina Shklovski, editors, Proceedings of the CHI Con-                       Engineering (RE 2001), 27-31 August 2001, Toronto, Canada, page 249.
      ference on Human Factors in Computing Systems, CHI 2024, Hon-                          IEEE Computer Society, 2001, doi:10.1109/ISRE.2001.948567.
      olulu, HI, USA, May 11-16, 2024, pages 962:1–962:16. ACM, 2024,                  [236] Rob van Zoest. Periodic table of natural language processing tasks, 2020.
      doi:10.1145/3613904.3642777.                                                           https://www.innerdoc.com/periodic-table-of-nlp-tasks/
[223] Mohammad Reza Taesiri, Finlay Macklon, Yihe Wang, Hengshuo Shen,                       [accessed April 2024].
      and Cor-Paul Bezemer. Large language models are pretty good zero-shot            [237] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion
      video game bug detectors, 2022, arXiv:2210.02506.                                      Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention
[224] Shuncheng Tang, Zhenya Zhang, Yi Zhang, Jixiang Zhou, Yan Guo,                         is all you need. In Isabelle Guyon, Ulrike von Luxburg, Samy Bengio,


                                                                                  33
      Hanna M. Wallach, Rob Fergus, S. V. N. Vishwanathan, and Roman                         Metzler, Ed H. Chi, Tatsunori Hashimoto, Oriol Vinyals, Percy Liang,
      Garnett, editors, Advances in Neural Information Processing Systems                    Jeff Dean, and William Fedus. Emergent abilities of large language
      30: Annual Conference on Neural Information Processing Systems 2017,                   models. Trans. Mach. Learn. Res., pages 209:1–209:30, 2022.
      December 4-9, 2017, Long Beach, CA, USA, pages 5998–6008, 2017.                  [252] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian
[238] Ashwin Prasad Shivarpatna Venkatesh, Samkutty Sabu, Amir M. Mir,                       Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou. Chain-of-
      Sofia Reis, and Eric Bodden. The emergence of large language models in                 thought prompting elicits reasoning in large language models. In Sanmi
      static analysis: A first look through micro-benchmarks. In David Lo, Xin               Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh,
      Xia, Massimiliano Di Penta, and Xing Hu, editors, Proceedings of the                   editors, Advances in Neural Information Processing Systems 35: Annual
      2024 IEEE/ACM First International Conference on AI Foundation Models                   Conference on Neural Information Processing Systems 2022, NeurIPS
      and Software Engineering, FORGE 2024, Lisbon, Portugal, 14 April                       2022, New Orleans, LA, USA, November 28 - December 9, 2022, 2022.
      2024, pages 35–39. ACM, 2024, doi:10.1145/3650105.3652288.                       [253] Moshi Wei, Nima Shiri Harzevili, Yuekai Huang, Jinqiu Yang, Junjie
[239] Fernando Richter Vidal, Naghmeh Ivaki, and Nuno Laranjeiro.                            Wang, and Song Wang. Demystifying and detecting misuses of deep
      Vulnerability detection techniques for smart contracts: A sys-                         learning APIs. In 46th IEEE/ACM International Conference on Software
      tematic literature review.         J. Syst. Softw., 217:112160, 2024,                  Engineering, ICSE 2024, Lisbon, Portugal, April 14-20, 2024, pages
      doi:https://doi.org/10.1016/j.jss.2024.112160.                                         201:1–201:12. ACM, 2024, doi:10.1145/3597503.3639177.
[240] Vasudev Vikram, Caroline Lemieux, and Rohan Padhye.                  Can         [254] Mark D. Weiser. Program slicing. IEEE Trans. Software Eng., 10(4):352–
      large language models write good property-based tests?, 2023,                          357, 1984, doi:10.1109/TSE.1984.5010248.
      arXiv:2307.04346.                                                                [255] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He,
[241] Nalin Wadhwa, Jui Pradhan, Atharv Sonwane, Surya Prakash Sahu,                         Haokun Li, Shing-Chi Cheung, and Cong Tian. Enchanting program
      Nagarajan Natarajan, Aditya Kanade, Suresh Parthasarathy, and Sriram                   specification synthesis by large language models using static analysis
      Rajamani. CORE: Resolving code quality issues using LLMs. Proc.                        and program verification. In Arie Gurfinkel and Vijay Ganesh, editors,
      ACM Softw. Eng., 1(FSE):789–811, 2024, doi:10.1145/3643762.                            Computer Aided Verification - 36th International Conference, CAV 2024,
[242] Zhongwei Wan, Xin Wang, Che Liu, Samiul Alam, Yu Zheng, Jiachen                        Montreal, QC, Canada, July 24-27, 2024, Proceedings, Part II, volume
      Liu, Zhongnan Qu, Shen Yan, Yi Zhu, Quanlu Zhang, Mosharaf Chowd-                      14682 of Lecture Notes in Computer Science, pages 302–328. Springer,
      hury, and Mi Zhang. Efficient large language models: A survey. Trans.                  2024, doi:10.1007/978-3-031-65630-9 16.
      Mach. Learn. Res., 2024, 2024.                                                   [256] Jules White, Quchen Fu, Sam Hays, Michael Sandborn, Carlos Olea,
[243] Chengpeng Wang, Wuqi Zhang, Zian Su, Xiangzhe Xu, Xiaoheng Xie,                        Henry Gilbert, Ashraf Elnashar, Jesse Spencer-Smith, and Douglas C.
      and Xiangyu Zhang. LLMDFA: analyzing dataflow in code with large                       Schmidt. A prompt pattern catalog to enhance prompt engineering with
      language models. In Amir Globersons, Lester Mackey, Danielle Bel-                      ChatGPT, 2023, arXiv:2302.11382.
      grave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang,             [257] Lionel Wong, Gabriel Grand, Alexander K. Lew, Noah D. Goodman,
      editors, Advances in Neural Information Processing Systems 38: Annual                  Vikash K. Mansinghka, Jacob Andreas, and Joshua B. Tenenbaum. From
      Conference on Neural Information Processing Systems 2024, NeurIPS                      word models to world models: Translating from natural language to the
      2024, Vancouver, BC, Canada, December 10 - 15, 2024, 2024.                             probabilistic language of thought, 2023, arXiv:2306.12672.
[244] Chong Wang, Jianan Liu, Xin Peng, Yang Liu, and Yiling Lou. Boosting             [258] W. Eric Wong, Ruizhi Gao, Yihao Li, Rui Abreu, and Franz Wotawa.
      static resource leak detection via LLM-based resource-oriented intention               A survey on software fault localization. IEEE Trans. Software Eng.,
      inference. In 47th IEEE/ACM International Conference on Software Engi-                 42(8):707–740, 2016, doi:10.1109/TSE.2016.2521368.
      neering, ICSE 2025, Ottawa, ON, Canada, April 26 - May 6, 2025, pages            [259] Robert E. Wray, James R. Kirk, and John E. Laird. Applying cog-
      2905–2917. IEEE, 2025, doi:10.1109/ICSE55347.2025.00131.                               nitive design patterns to general LLM agents. In Matthew Iklé, An-
[245] Haijun Wang, Yurui Hu, Hao Wu, Dijun Liu, Chenyang Peng, Yin Wu,                       ton Kolonin, and Michael Bennett, editors, Artificial General Intel-
      Ming Fan, and Ting Liu. Skyeye: Detecting imminent attacks via analyz-                 ligence - 18th International Conference, AGI 2025, Reykjavic, Ice-
      ing adversarial smart contracts. In Vladimir Filkov, Baishakhi Ray, and                land, August 10-13, 2025, Proceedings, Part II, volume 16058 of
      Minghui Zhou, editors, Proceedings of the 39th IEEE/ACM International                  Lecture Notes in Computer Science, pages 312–325. Springer, 2025,
      Conference on Automated Software Engineering, ASE 2024, Sacramento,                    doi:10.1007/978-3-032-00800-8 28.
      CA, USA, October 27 - November 1, 2024, pages 1570–1582. ACM,                    [260] Cong Wu, Jing Chen, Ziwei Wang, Ruichao Liang, and Ruiying Du. Se-
      2024, doi:10.1145/3691620.3695526.                                                     mantic Sleuth: Identifying Ponzi contracts via large language models. In
[246] Junjie Wang, Yuchao Huang, Chunyang Chen, Zhe Liu, Song Wang,                          Vladimir Filkov, Baishakhi Ray, and Minghui Zhou, editors, Proceedings
      and Qing Wang. Software testing with large language model: Survey,                     of the 39th IEEE/ACM International Conference on Automated Software
      landscape, and vision. IEEE Trans. Software Eng., 50:911–936, 2024,                    Engineering, ASE 2024, Sacramento, CA, USA, October 27 - November 1,
      doi:10.1109/TSE.2024.3368208.                                                          2024, pages 582–593. ACM, 2024, doi:10.1145/3691620.3695055.
[247] Ruocheng Wang, Eric Zelikman, Gabriel Poesia, Yewen Pu, Nick Haber,              [261] Guangyuan Wu, Weining Cao, Yuan Yao, Hengfeng Wei, Taolue Chen,
      and Noah D. Goodman. Hypothesis search: Inductive reasoning with                       and Xiaoxing Ma. LLM meets bounded model checking: Neuro-symbolic
      language models. In The Twelfth International Conference on Learning                   loop invariant inference. In Vladimir Filkov, Baishakhi Ray, and Minghui
      Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenRe-                   Zhou, editors, Proceedings of the 39th IEEE/ACM International Con-
      view.net, 2024.                                                                        ference on Automated Software Engineering, ASE 2024, Sacramento,
[248] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V. Le, Ed H. Chi, Sha-                   CA, USA, October 27 - November 1, 2024, pages 406–417. ACM, 2024,
      ran Narang, Aakanksha Chowdhery, and Denny Zhou. Self-consistency                      doi:10.1145/3691620.3695014.
      improves chain of thought reasoning in language models. In The Eleventh          [262] Haoze Wu, Clark Barrett, and Nina Narodytska. Lemur: Integrating large
      International Conference on Learning Representations, ICLR 2023, Ki-                   language models in automated program verification. In The Twelfth Inter-
      gali, Rwanda, May 1-5, 2023. OpenReview.net, 2023.                                     national Conference on Learning Representations, ICLR 2024, Vienna,
[249] Zejun Wang, Kaibo Liu, Ge Li, and Zhi Jin. HITS: High-coverage LLM-                    Austria, May 7-11 2024. OpenReview.net, 2024.
      based unit test generation via method slicing. In Proceedings of the 39th        [263] Shengnan Wu, Yongxiang Hu, Yingchuan Wang, Jiazhen Gu, Jin Meng,
      IEEE/ACM International Conference on Automated Software Engineering,                   Liujie Fan, Zhongshi Luan, Xin Wang, and Yangfan Zhou. Combating
      ASE 2024, Sacramento, CA, USA, October 27 - November 1, 2024, pages                    missed recalls in e-commerce search: A CoT-prompting testing approach.
      1258–1268. ACM, 2024, doi:10.1145/3691620.3695501.                                     In Marcelo d’Amorim, editor, Companion Proceedings of the 32nd ACM
[250] Jason Wei, Maarten Bosma, Vincent Y. Zhao, Kelvin Guu, Adams Wei                       International Conference on the Foundations of Software Engineering,
      Yu, Brian Lester, Nan Du, Andrew M. Dai, and Quoc V. Le. Finetuned                     FSE 2024, Porto de Galinhas, Brazil, July 15-19, 2024, pages 220–231.
      language models are zero-shot learners. In The Tenth International                     ACM, 2024, doi:10.1145/3663529.3663842.
      Conference on Learning Representations, ICLR 2022, Virtual Event,                [264] Tongshuang Wu, Ellen Jiang, Aaron Donsbach, Jeff Gray, Alejandra
      April 25-29, 2022. OpenReview.net, 2022.                                               Molina, Michael Terry, and Carrie J. Cai. Promptchainer: Chaining large
[251] Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebas-                  language model prompts through visual programming. In Simone D. J.
      tian Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald                        Barbosa, Cliff Lampe, Caroline Appert, and David A. Shamma, editors,


                                                                                  34
      CHI ’22: CHI Conference on Human Factors in Computing Systems,                         arXiv:2505.20139.
      New Orleans, LA, USA, 29 April 2022 - 5 May 2022, Extended Abstracts,            [277] Lin Yang, Chen Yang, Shutao Gao, Weijing Wang, Bo Wang, Qihao
      pages 359:1–359:10. ACM, 2022, doi:10.1145/3491101.3519729.                            Zhu, Xiao Chu, Jianyi Zhou, Guangtai Liang, Qianxiang Wang, and
[265] Yin Wu, Xiaofei Xie, Chenyang Peng, Dijun Liu, Hao Wu, Ming Fan,                       Junjie Chen. On the evaluation of large language models in unit test
      Ting Liu, and Haijun Wang. AdvSCanner: Generating adversarial smart                    generation. In Proceedings of the 39th IEEE/ACM International Confer-
      contracts to exploit reentrancy vulnerabilities using LLM and static                   ence on Automated Software Engineering, ASE 2024, Sacramento, CA,
      analysis. In Proceedings of the 39th IEEE/ACM International Confer-                    USA, October 27 - November 1, 2024, pages 1607–1619. ACM, 2024,
      ence on Automated Software Engineering, ASE 2024, Sacramento, CA,                      doi:10.1145/3691620.3695529.
      USA, October 27 - November 1, 2024, pages 1019–1031. ACM, 2024,                  [278] Yanjing Yang, Xin Zhou, Runfeng Mao, Jinwei Xu, Lanxin Yang,
      doi:10.1145/3691620.3695482.                                                           Yu Zhang, Haifeng Shen, and He Zhang. DLAP: A deep learn-
[266] Yonghao Wu, Zheng Li, Jie M. Zhang, Mike Papadakis, Mark Har-                          ing augmented large language model prompting framework for soft-
      man, and Yong Liu. Large language models in fault localisation, 2023,                  ware vulnerability detection. J. Syst. Softw., 219:112234, 2025,
      arXiv:2308.15276.                                                                      doi:10.1016/J.JSS.2024.112234.
[267] Yulun Wu, Ming Wen, Zeliang Yu, Xiaochen Guo, and Hai Jin. Effective             [279] Jianan Yao, Ziqiao Zhou, Weiteng Chen, and Weidong Cui. Leveraging
      vulnerable function identification based on CVE description empowered                  large language models for automated proof synthesis in Rust, 2023,
      by large language models. In Vladimir Filkov, Baishakhi Ray, and                       arXiv:2311.03739.
      Minghui Zhou, editors, Proceedings of the 39th IEEE/ACM International            [280] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan
      Conference on Automated Software Engineering, ASE 2024, Sacramento,                    Cao, and Karthik Narasimhan. Tree of thoughts: Deliberate problem
      CA, USA, October 27 - November 1, 2024, pages 393–405. ACM, 2024,                      solving with large language models. In Advances in Neural Information
      doi:10.1145/3691620.3695013.                                                           Processing Systems, volume 36, pages 11809–11822. Curran Associates,
[268] Chunqiu Steven Xia, Matteo Paltenghi, Jia Le Tian, Michael Pradel, and                 Inc., 2023.
      Lingming Zhang. Fuzz4All: Universal fuzzing with large language mod-             [281] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R.
      els. In 46th IEEE/ACM International Conference on Software Engineer-                   Narasimhan, and Yuan Cao. ReAct: Synergizing reasoning and act-
      ing, ICSE 2024, Lisbon, Portugal, April 14-20, 2024, pages 126:1–126:13.               ing in language models. In The Eleventh International Conference on
      ACM, 2024, doi:10.1145/3597503.3639121.                                                Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023.
[269] Chunqiu Steven Xia, Yuxiang Wei, and Lingming Zhang. Automated                         OpenReview.net, 2023.
      program repair in the era of large pre-trained language models. In 45th          [282] Yuan Yao, Deming Ye, Peng Li, Xu Han, Yankai Lin, Zhenghao Liu,
      IEEE/ACM International Conference on Software Engineering, ICSE                        Zhiyuan Liu, Lixin Huang, Jie Zhou, and Maosong Sun. DocRED: A
      2023, Melbourne, Australia, May 14-20, 2023, pages 1482–1494. IEEE,                    large-scale document-level relation extraction dataset. In Anna Korhonen,
      2023, doi:10.1109/ICSE48619.2023.00129.                                                David R. Traum, and Lluı́s Màrquez, editors, 57th Conference of the As-
[270] Weixiang Yan, Haitian Liu, Yunkun Wang, Yunzhe Li, Qian Chen, Wen                      sociation for Computational Linguistics, ACL 2019, Florence, Italy, July
      Wang, Tingyu Lin, Weishan Zhao, Li Zhu, Hari Sundaram, and Shuiguang                   28- August 2, 2019, Volume 1: Long Papers, pages 764–777. Association
      Deng. CodeScope: An execution-based multilingual multitask multidi-                    for Computational Linguistics, 2019, doi:10.18653/V1/P19-1074.
      mensional benchmark for evaluating LLMs on code understanding and                [283] Xin Yin, Chao Ni, and Shaohua Wang. Multitask-based evaluation of
      generation. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors,                 open-source LLM on software vulnerability. IEEE Trans. Software Eng.,
      Proceedings of the 62nd Annual Meeting of the Association for Com-                     50(11):3071–3087, 2024, doi:10.1109/TSE.2024.3470333.
      putational Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok,               [284] Zhiqiang Yuan, Yiling Lou, Mingwei Liu, Shiji Ding, Kaixin Wang,
      Thailand, August 11-16, 2024, pages 5511–5558. Association for Compu-                  Yixuan Chen, and Xin Peng. Evaluating and improving ChatGPT for
      tational Linguistics, 2024, doi:10.18653/V1/2024.ACL-LONG.301.                         unit test generation. Proc. ACM Softw. Eng., 1(FSE):1703–1726, 2024,
[271] Aidan Z.H. Yang, Ruben Martins, Claire Le Goues, and Vincent J. Hel-                   doi:10.1145/3660783.
      lendoorn. Large language models for test-free fault localization. In 46th        [285] Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah D. Goodman. Star:
      IEEE/ACM International Conference on Software Engineering, ICSE                        Bootstrapping reasoning with reasoning. In Sanmi Koyejo, S. Mohamed,
      2024, Lisbon, Portugal, April 14-20, 2024, pages 17:1–17:12. ACM,                      A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh, editors, Advances in
      2024, doi:10.1145/3597503.3623342.                                                     Neural Information Processing Systems 35: Annual Conference on Neural
[272] Chen Yang, Junjie Chen, Bin Lin, Jianyi Zhou, and Ziqi Wang. Enhanc-                   Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA,
      ing LLM-based test generation for hard-to-cover branches via program                   USA, November 28 - December 9, 2022, 2022.
      analysis, 2024, arXiv:2404.04966.                                                [286] Cen Zhang, Yaowen Zheng, Mingqiang Bai, Yeting Li, Wei Ma, Xiaofei
[273] Chenyang Yang, Yining Hong, Grace A. Lewis, Tongshuang Wu, and                         Xie, Yuekang Li, Limin Sun, and Yang Liu. How effective are they?
      Christian Kästner. What is wrong with my model? identifying systematic                exploring large language model based fuzz driver generation. In Maria
      problems with semantic data slicing. In Vladimir Filkov, Baishakhi                     Christakis and Michael Pradel, editors, Proceedings of the 33rd ACM
      Ray, and Minghui Zhou, editors, Proceedings of the 39th IEEE/ACM                       SIGSOFT International Symposium on Software Testing and Analysis,
      International Conference on Automated Software Engineering, ASE 2024,                  ISSTA 2024, Vienna, Austria, September 16-20, 2024, pages 1223–1235.
      Sacramento, CA, USA, October 27 - November 1, 2024, pages 306–318.                     ACM, 2024, doi:10.1145/3650212.3680355.
      ACM, 2024, doi:10.1145/3691620.3695033.                                          [287] Chenyuan Zhang, Hao Liu, Jiutian Zeng, Kejing Yang, Yuhong Li,
[274] Chenyuan Yang, Yinlin Deng, Runyu Lu, Jiayi Yao, Jiawei Liu, Rey-                      and Hui Li. Prompt-enhanced software vulnerability detection us-
      haneh Jabbarvand, and Lingming Zhang. WhiteFox: White-box compiler                     ing ChatGPT. In 46th IEEE/ACM International Conference on Soft-
      fuzzing empowered by large language models. Proc. ACM Program.                         ware Engineering: Companion Proceedings, ICSE Companion 2024,
      Lang., 8(OOPSLA2):709–735, 2024, doi:10.1145/3689736.                                  Lisbon, Portugal, April 14-20, 2024, pages 276–277. ACM, 2024,
[275] Chenyuan Yang, Zijie Zhao, and Lingming Zhang. KernelGPT: En-                          doi:10.1145/3639478.3643065.
      hanced kernel fuzzing via large language models. In Lieven Eeckhout,             [288] Dylan Zhang, Xuchao Zhang, Chetan Bansal, Pedro Henrique B. Las-
      Georgios Smaragdakis, Katai Liang, Adrian Sampson, Martha A. Kim,                      Casas, Rodrigo Fonseca, and Saravan Rajmohan. LM-PACE: confidence
      and Christopher J. Rossbach, editors, Proceedings of the 30th ACM                      estimation by large language models for effective root causing of cloud
      International Conference on Architectural Support for Programming Lan-                 incidents. In Marcelo d’Amorim, editor, Companion Proceedings of
      guages and Operating Systems, Volume 2, ASPLOS 2025, Rotterdam,                        the 32nd ACM International Conference on the Foundations of Software
      Netherlands, 30 March 2025 - 3 April 2025, pages 560–573. ACM, 2025,                   Engineering, FSE 2024, Porto de Galinhas, Brazil, July 15-19, 2024,
      doi:10.1145/3676641.3716022.                                                           pages 388–398. ACM, 2024, doi:10.1145/3663529.3663858.
[276] Jialin Yang, Dongfu Jiang, Lipeng He, Sherman Siu, Yuxuan Zhang,                 [289] Fengyi Zhang, Bihuan Chen, Yufei Zhao, and Xin Peng. Slice-
      Disen Liao, Zhuofeng Li, Huaye Zeng, Yiming Jia, Haozhe Wang, Ben-                     based code change representation learning. In Tao Zhang, Xin
      jamin Schneider, Chi Ruan, Wentao Ma, Zhiheng Lyu, Yifei Wang, Yi Lu,                  Xia, and Nicole Novielli, editors, IEEE International Conference
      Quy Duc Do, Ziyan Jiang, Ping Nie, and Wenhu Chen. StructEval:                         on Software Analysis, Evolution and Reengineering, SANER 2023,
      Benchmarking LLMs’ capabilities to generate structural outputs, 2025,                  Taipa, Macao, March 21-24, 2023, pages 319–330. IEEE, 2023,


                                                                                  35
      doi:10.1109/SANER56733.2023.00038.                                             [304] Xiaogang Zhu, Sheng Wen, Seyit Camtepe, and Yang Xiang. Fuzzing: A
[290] Jian Zhang, Chong Wang, Anran Li, Wenhan Wang, Tianlin Li, and                       survey for roadmap. ACM Comput. Surv., 54(11s):230:1–230:36, 2022,
      Yang Liu. VulAdvisor: Natural language suggestion generation for                     doi:10.1145/3512345.
      software vulnerability repair. In Vladimir Filkov, Baishakhi Ray, and          [305] Ziye Zhu, Yu Wang, and Yun Li. TroBo: A novel deep transfer model
      Minghui Zhou, editors, Proceedings of the 39th IEEE/ACM International                for enhancing cross-project bug localization. In Han Qiu, Cheng Zhang,
      Conference on Automated Software Engineering, ASE 2024, Sacramento,                  Zongming Fei, Meikang Qiu, and Sun-Yuan Kung, editors, Knowledge
      CA, USA, October 27 - November 1, 2024, pages 1932–1944. ACM,                        Science, Engineering and Management - 14th International Conference,
      2024, doi:10.1145/3691620.3695555.                                                   KSEM 2021, Tokyo, Japan, August 14-16, 2021, Proceedings, Part I,
[291] Jie M. Zhang, Mark Harman, Lei Ma, and Yang Liu. Machine learning                    volume 12815 of Lecture Notes in Computer Science, pages 529–541.
      testing: Survey, landscapes and horizons. IEEE Trans. Software Eng.,                 Springer, 2021, doi:10.1007/978-3-030-82136-4 43.
      48(2):1–36, 2022, doi:10.1109/TSE.2019.2962027.
[292] Jin Zhang and Jingyue Li.           Testing and verification of neural-
      network-based safety-critical control software:          A systematic          Appendix A. Transformations Taxonomy Trees
      literature review.         Inf. Softw. Technol., 123:106296, 2020,
      doi:10.1016/J.INFSOF.2020.106296.                                                We include here the omitted detailed trees of the taxonomy
[293] Kexun Zhang, Danqing Wang, Jingtao Xia, William Yang Wang, and
      Lei Li. ALGO: synthesizing algorithmic programs with generated or-             were we have mapped the transformations from the analyzed
      acle verifiers. In Alice Oh, Tristan Naumann, Amir Globerson, Kate             tools.
      Saenko, Moritz Hardt, and Sergey Levine, editors, Advances in Neural
      Information Processing Systems 36: Annual Conference on Neural Infor-          General-Code Generation
      mation Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA,
                                                                                        Generation criteria
      December 10 - 16, 2023, 2023.                                                        Intent corresponding: TitanFuzz1 [53], AID1 [145], DiffPrompt2 [140], Dafny-Synth1 [170],
[294] Quanjun Zhang, Chunrong Fang, Yang Xie, Yaxin Zhang, Yun Yang,                                            ClarifyGPT1 [173], Clover3 [217], FormAI [229]
      Weisong Sun, Shengcheng Yu, and Zhenyu Chen. A survey on large                          Clarifications
      language models for software engineering, 2023, arXiv:2312.15223.                            Test provided: Dafny-Synth2 [170]
[295] Ting Zhang, Ivana Clairine Irsan, Ferdian Thung, and David Lo. Cupid:                        Signature provided: Dafny-Synth2 [170], Dafny-Synth5 [170]
      Leveraging ChatGPT for more accurate duplicate bug report detection,                         Specification provided: Dafny-Synth5 [170]
                                                                                              Verifiable: Dafny-Synth5 [170]
      2023, arXiv:2308.10022.
                                                                                              Non-functional requirements satisfying
[296] Xuchao Zhang, Supriyo Ghosh, Chetan Bansal, Rujia Wang, Minghua                              Complexity: ALGO [293]
      Ma, Yu Kang, and Saravan Rajmohan. Automated root causing of cloud                           Style: AID1 [145], FormAI [229]
      incidents using in-context learning with GPT-4. In Marcelo d’Amorim,                 Annotation corresponding: Clover1 [217], Clover2 [217]
      editor, Companion Proceedings of the 32nd ACM International Con-                     Repair request corresponding
      ference on the Foundations of Software Engineering, FSE 2024, Porto                     Defect-description repairing: WitheredLeaf 3(CoT) [35], AutoSD3 [121],
                                                                                                                            LLM4Vuln3(patch) [219]
      de Galinhas, Brazil, July 15-19, 2024, pages 266–277. ACM, 2024,
                                                                                              Error-feedback repairing: AlloyRepair1 [4]
      doi:10.1145/3663529.3663846.                                                            Suggestion-based repairing: AlloyRepair2 [4]
[297] Yichi Zhang, Zixi Liu, Yang Feng, and Baowen Xu. Leveraging large                    Examples based
      language model to assist detecting Rust code comment inconsistency. In                   Translation
      Vladimir Filkov, Baishakhi Ray, and Minghui Zhou, editors, Proceedings                       API: FuzzGPT2 [54]
      of the 39th IEEE/ACM International Conference on Automated Software                      Parametrization: SearchGEM51 [46]
                                                                                               Mutation: FSMLDS/MG [17], LLM4CBI [232]
      Engineering, ASE 2024, Sacramento, CA, USA, October 27 - November 1,
                                                                                                    Bug injecting: BugFarm [105]
      2024, pages 356–366. ACM, 2024, doi:10.1145/3691620.3695010.                                  Different behavior: LLMorpheus [230]
[298] Ying Zhang, Wenjia Song, Zhengjie Ji, Danfeng Yao, and Na Meng. How                      Repair: AlloyRepair1 [4], AlloyRepair2 [4], WitheredLeaf 3(CoT) [35], AutoSD3 [121],
      well does LLM generate security tests?, 2023, arXiv:2310.00710.                                   AID1 [145], LLM4Vuln3(patch) [219]
[299] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yu-                       Completion
      peng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong,                              Natural: FLAG [3], TitanFuzz2 [53], µBERT [124], CHEMFUZZ1 [196]
                                                                                        Nature of primary generated entity
      Yifan Du, Chen Yang, Yushuo Chen, Zhipeng Chen, Jinhao Jiang,                        Code: FLAG [3], FSMLDS/MG [17], WitheredLeaf 3(CoT) [35], SearchGEM51 [46],
      Ruiyang Ren, Yifan Li, Xinyu Tang, Zikang Liu, Peiyu Liu, Jian-Yun                          TitanFuzz1 [53], TitanFuzz2 [53], FuzzGPT2 [54], BugFarm [105],
      Nie, and Ji-Rong Wen. A survey of large language models, 2023,                              AutoSD3 [121], µBERT [124], DiffPrompt2 [140], AID1 [145],
      arXiv:2303.18223.                                                                           Dafny-Synth1 [170], Dafny-Synth2 [170], Dafny-Synth5 [170], ClarifyGPT1 [173],
[300] Xin Zhou, Sicong Cao, Xiaobing Sun, and David Lo. Large language                            CHEMFUZZ1 [196], Clover1 [217], Clover2 [217], Clover3 [217],
                                                                                                  LLM4Vuln3(patch) [219], FormAI [229], LLMorpheus [230], LLM4CBI [232],
      model for vulnerability detection and repair: Literature review and the
                                                                                                  ALGO [293]
      road ahead. ACM Trans. Softw. Eng. Methodol., 34(5):145:1–145:31,                    Model: AlloyRepair1 [4], AlloyRepair2 [4]
      2025, doi:10.1145/3708522.                                                        Nature of extra generated entity
[301] Xin Zhou, Ting Zhang, and David Lo. Large language model for vul-                      Annotations
      nerability detection: Emerging results and future directions. In Pro-                       Pre/Postcondition: Dafny-Synth1 [170], Dafny-Synth2 [170]
      ceedings of the 2024 ACM/IEEE 44th International Conference on Soft-                        Loop invariant / Verification annotations: Dafny-Synth5 [170]
                                                                                        In-filling context
      ware Engineering: New Ideas and Emerging Results, NIER@ICSE
                                                                                             Annotated code: Clover1 [217], Clover2 [217], Clover3 [217]
      2024, Lisbon, Portugal, April 14-20, 2024, pages 47–51. ACM, 2024,                     Masked code: FLAG [3], TitanFuzz2 [53], µBERT [124], CHEMFUZZ1 [196],
      doi:10.1145/3639476.3639762.                                                                          LLMorpheus [230]
[302] Yongchao Zhou, Andrei Ioan Muresanu, Ziwen Han, Keiran Paster, Silviu             Corrective mode
      Pitis, Harris Chan, and Jimmy Ba. Large language models are human-                    Feedback based
      level prompt engineers. In The Eleventh International Conference on                       Compiler: Clover2 [217], Clover3 [217]
      Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023.                       Verifier: Clover1 [217]
                                                                                                Validity: AlloyRepair1 [4], CHEMFUZZ1 [196], LLM4CBI [232]
      OpenReview.net, 2023.
                                                                                                Suggested corrections: AlloyRepair2 [4]
[303] Zhuotong Zhou, Yongzhuo Yang, Susheng Wu, Yiheng Huang, Bi-                       Rationalization
      huan Chen, and Xin Peng. Magneto: A step-wise approach to ex-                         Explanation: LLMorpheus [230]
      ploit vulnerabilities in dependent libraries via LLM-empowered directed
      fuzzing. In Proceedings of the 39th IEEE/ACM International Confer-
                                                                                                           Figure A.11: General-Code Generation.
      ence on Automated Software Engineering, ASE 2024, Sacramento, CA,
      USA, October 27 - November 1, 2024, pages 1633–1644. ACM, 2024,
      doi:10.1145/3691620.3695531.


                                                                                36
 Domain-Specific-Code Generation                                                                Data Generation

    Generation criteria                                                                            Generation criteria
       Problem-description corresponding                                                               Context compliant
            DSL-function description: Eywa [117]                                                          Description: RESTGPT2 [128]
            Function intent: Dafny-Synth3 [170]                                                           Usage: Fuzz4All2 [268]
            Object description: LLMDFA4 [243], LLMDFA5 [243]                                              GUI context: QTypist1 [154], QTypist2 [154], InputBlaster2 [156]
            Scenario: ScenicNL4 [60], LeGEND2 [225]                                                       Code + arguments: SearchGEM52 [46]
            Constraint: AID2 [145]                                                                     Constraints based
            Property: EMR3 [210]                                                                          x | P(x): RESTGPT2 [128], InputBlaster2 [156], SymPrompt [201], WhiteFox2 [274]
            Rule: InputBlaster4 [156]
                                                                                                                P ≡ code reachability: DirInput [114], HITS6 [249], Magneto [303]
       Ability to execute code: OSS-Fuzz1 [76], OSS-Fuzz2 [76], PBT-GPT2 [240],                            x | ∃i : x = F(i): SELF-DEBUGGINGOP2 [37]
                                 UGCTX1 [286], UGCTX2 [286]                                                x | i = F(x): mrDetector1 [263]
           Ability to trigger vulnerability: AdvSCanner1 [265]                                                x | i = F(x, j): SemSlicer4 [273]
       High precision & recall: LLMDFA1 [243], LLMDFA2 [243]
                                                                                                              x | ∀y g(i, y)  f (x, y): SemSlicer1 [273], SemSlicer2 [273]
    Nature of domain/entity                                                                               x | exercises (A(x) ⇒ C(x)): LLMeDiff [106]
         Scripting for SW analysis                                                                        x | exercises (Pre(x)& exercises Post(x, R)): TestChain1 [139], ClarifyGPT2 [173]
              Source/Sink identification: LLMDFA1 [243], LLMDFA2 [243]                                 Exemplars compliant
         Metamorphic relation: EMR3 [210]                                                                 Spec-aware edition: ChatAFL2 [168], Fuzz4All3 [268]
         Encoders                                                                                         Variation: ChatFuzz [94], Fuzz4All4 [268]
              Path condition: LLMDFA4 [243], LLMDFA5 [243]                                                       Error triggering: FuzzingParsers4 [1]
         Test drivers                                                                                        Natural completion: ChatAFL3 [168]
              Fuzzing: OSS-Fuzz1 [76], OSS-Fuzz2 [76], UGCTX1 [286], UGCTX2 [286]                  In-filling context
              Input generators: AID2 [145], InputBlaster4 [156], PBT-GPT2 [240]                         Masked data: QTypist2 [154]
         Protocol-related code: Eywa [117]                                                              Data completion: QTypist1 [154], ChatAFL3 [168]
         Word model: ScenicNL4 [60], LeGEND2 [225]                                                 Corrective mode
         Signatures: Dafny-Synth3 [170]                                                                Feedback based
         Adversarial SmartContract: AdvSCanner1 [265]                                                      Execution output: DirInput [114]
    In-filling context                                                                                     Self-refine alternative: SemSlicer2 [273]
         Hint code: LLMDFA1 [243], LLMDFA2 [243]
         Constrained decoding: ScenicNL4 [60]
    Corrective mode                                                                                                         Figure A.14: Data Generation.
       Feedback based
            Compiler: OSS-Fuzz2 [76], LLMDFA2 [243], LLMDFA5 [243], UGCTX2 [286]
            Execution
                Number of positive/negative: LLMDFA2 [243]
                                                                                                   Behavior Analysis
                Results: OSS-Fuzz2 [76], InputBlaster4 [156], UGCTX2 [286]
            Rationalized failure: AdvSCanner1 [265]
                                                                                                       Analysis criteria
    Reactivity
                                                                                                           Anomaly detection
       Function calling: ScenicNL4 [60]
                                                                                                              Open-ended: CHEMFUZZ2 [196]
                                                                                                                   Attack: Skyeye1 [245], Skyeye3 [245]
             Figure A.12: Domain-Specific-Code Generation.                                                         Vulnerability: Pwn’d3 [82]
                                                                                                                   View-point conformance: GameBugDescriptions1 [223]
                                                                                                                   Self-justified: AXNav3 [222]
                                                                                                               Sanity check: PentestGPT3 [51]
Annotation Generation                                                                                             Execution specification conformance: E&V2 [81]
                                                                                                           Root-cause: x-lifecycle2 [73], AutoFL1 [120], AutoSD1 [121], RCAAgents1 [199],

   Generation criteria                                                                                                   inContextRCA2 [296]
      Syntactic: KernelGPT5 [275]                                                                              Differences: SELF-DEBUGGINGFL [37]
                                                                                                           State: GPTDroid2 [155]
      Natural: TOGLL [90], ChatInv [109], PBT-GPT1 [240], AutoSpec [255]
                                                                                                       Extra input
             Demonstration similarity: PropertyGPT1 [151], PropertyGPT2 [151],
                                                                                                           Architecture: x-lifecycle2 [73]
                                       PropertyGPT4 [151], CEDAR [176]
                                                                                                           Code: SELF-DEBUGGINGFL [37], AutoFL1 [120], AutoSD1 [121]
        Natural & Verifiable: SpecGen1 [161]
                                                                                                           Historic incidents: RCAAgents1 [199], inContextRCA2 [296]
        Proof-enabling: Loopy1 [119], Clover5 [217], Lam4Inv [261], Lemur1 [262],
                                                                                                           (hidden) Verbalized call sequence: Skyeye3 [245]
                        RustProof 2 [279]
                                                                                                       Reactivity
   Nature of entity
                                                                                                           Function calls: AutoFL1 [120], RCAAgents1 [199]
        Precondition: PropertyGPT2 [151], SpecGen1 [161], Clover5 [217], AutoSpec [255]
                                                                                                           Questions: RCAAgents1 [199]
        Postcondition: PropertyGPT2 [151], SpecGen1 [161], Clover5 [217], AutoSpec [255]
                                                                                                       Rationalization
        Loop invariant: Loopy1 [119], ESBMCibmc [191], AutoSpec [255], Lam4Inv [261],
                                                                                                           Applied evaluation criteria: AXNav3 [222]
                        RustProof 2 [279]
                                                                                                           Execution: SELF-DEBUGGINGFL [37]
        Assumption: Lemur1 [262]
        Type state: KernelGPT5 [275]
        Assertion: TOGLL [90], PropertyGPT1 [151], CEDAR [176]
                                                                                                                           Figure A.15: Behavior Analysis.
   In-filling context
        Masked assertion: ChatInv [109]
        Annotated code: Loopy1 [119], SpecGen1 [161], CEDAR [176], Clover5 [217],
                         AutoSpec [255], Lemur1 [262], RustProof 2 [279]
        Unit test: TOGLL [90], CEDAR [176]                                                        Line Code-Ranking
   Corrective mode
      Feedback based                                                                                  Analysis criteria
          Compiler failure: PropertyGPT3 [151], ESBMCibmc [191]                                           Fault proneness: ChatGPT4vul2 [69], ChatGPT-4(Log)1 [266], ChatGPT-4(Log)2 [266]
          Verification failure: SpecGen2 [161], ESBMCibmc [191], Lam4Inv [261],                       Extra input
                                Lemur2 [262], RustProof 3 [279]                                           Intent: ChatGPT-4(Log)1 [266], ChatGPT-4(Log)2 [266]
                Inductiveness: Loopy2 [119]                                                           Corrective mode
           Validity checker: PropertyGPT4 [151], KernelGPT5 [275]                                         Test results: ChatGPT-4(Log)2 [266]
   Rationalization                                                                                    Rationalization
       Invariant explanation: RustProof 2 [279]                                                           Intent: ChatGPT-4(Log)1 [266], ChatGPT-4(Log)2 [266]
       Proof explanation: RustProof 2 [279]                                                               Reason: ChatGPT-4(Log)1 [266], ChatGPT-4(Log)2 [266]



            Figure A.13: Code-Given Annotation Generation.                                                                 Figure A.16: Line Code-Ranking.


                                                                                           37
                        Code-Scaling


                            Scale
                                CVSS: ChatGPT4vul4 [69], MultiTask2 [283]
                                Vulnerability probability: DLAP1 [278]
                                                                                                              Text Analysis

                                                                                                                 Analysis type
                                 Figure A.17: Code Scaling.
                                                                                                                     Comparative analysis
                                                                                                                         Functional equivalence: SELF-DEBUGGINGOP6 [37], Clover8 [217]
                                                                                                                         Similarity analysis: FAIL4 [13]
                                                                                                                         Generalized consensus: Skyeye4 [245]
 Direct Code-Classification
                                                                                                                     Ambiguity analysis: ScenicNL2 [60], ClarifyGPT4 [173]
                                                                                                                     Support analysis
    Analysis criteria
                                                                                                                         To conclude: AutoSD2 [121], FAIL9 [13]
       Vulnerability proneness: SmartAudit1 [48], ChatGPT4vul1 [69], ChatGPT4vul3 [69],
                                                                                                                         To perform: LM-PACE1 [288]
                               NLBSE241 [111], GRACE [158], AIagent [208], MultiTask1 [283],
                                                                                                                         To analyze: FAIL2 [13]
                               MultiTask3 [283], MultiTask4 [283], PromptEnhanced2 [287],
                                                                                                                     Closed analysis
                               ChatGPT(Plus) [301]
                                                                                                                         Q&A: LasRCA1 [79]
           Similar to demonstrations: GRACE [158]
                                                                                                                     Open analysis
       Malware proneness: SpiderScan1 [103]
                                                                                                                         Q&A: RCAAgents2 [199]
       Used API: FuzzGPT1 [54], SpiderScan2 [103]
       API Misuse: LLMAPIDet3 [253]                                                                                           Expert completed: ScenicNL3 [60]
                                                                                                                     Classification
       Category of bug: WitheredLeaf 4 [35]
       Adherence to description: NLBSE242 [111], GPTScan1 [220]                                                          Binary: FAIL4 [13]
       Adherence to behavioral description: SELF-DEBUGGINGOP7 [37], GPTScan2 [220]                                            In-context defined class: SemSlicer3 [273]
    Nature of classification                                                                                             Multilabel
        Multiplicity                                                                                                          Close ended: LasRCA2 [79], LasRCA3 [79]
           OneClass (Binary): SmartAudit1 [48], ChatGPT4vul1 [69], SpiderScan1 [103],                                         Open ended: Skyeye4 [245]
                                                                                                                 Rationalization
                               NLBSE241 [111], GRACE [158], MultiTask1 [283],
                                                                                                                     Debate: ScenicNL3 [60]
                               MultiTask3 [283], PromptEnhanced2 [287]
                                                                                                                     Thought step by step: LasRCA2 [79]
               In-context defined class: SELF-DEBUGGINGOP7 [37], NLBSE242 [111],
                                                                                                                     Reasons: LasRCA3 [79]
                                         GPTScan1 [220], GPTScan2 [220],
                                         LLMAPIDet3 [253], ChatGPT(Plus) [301]
            MultiClass/MultiLabel
                 Open-ended: FuzzGPT1 [54]
                                                                                                                                    Figure A.20: Text Analysis.
                 Close-ended: ChatGPT4vul3 [69], SpiderScan2 [103], AIagent [208],
                              MultiTask4 [283]
                 Semi-close-ended: WitheredLeaf 4 [35]
    Analysis granularity
        Snippet: SELF-DEBUGGINGOP7 [37], SmartAudit1 [48], FuzzGPT1 [54],
                  ChatGPT4vul1 [69], ChatGPT4vul3 [69], SpiderScan1 [103], NLBSE241 [111],
                  NLBSE242 [111], GRACE [158], GPTScan1 [220], GPTScan2 [220],
                  LLMAPIDet3 [253], MultiTask1 [283], PromptEnhanced2 [287],
                  ChatGPT(Plus) [301]
        Line: WitheredLeaf 4 [35], AIagent [208], MultiTask3 [283]
    Extra input
        Code property graph: GRACE [158]
                                                                                                               Code-Elements Identification & Extraction
        Intent: PromptEnhanced2 [287]
        Ctrl/Data-flow: PromptEnhanced2 [287]
        Call sequence: PromptEnhanced2 [287]                                                                       Identification criteria
        Bug reason: WitheredLeaf 4 [35]                                                                                Role based
        Assertion: SELF-DEBUGGINGOP7 [37]                                                                                   Specialized
    Rationalization                                                                                                            Command values: KernelGPT2 [275]
        Background: GPTScan1 [220], GPTScan2 [220]                                                                              Definition
        Execution: SELF-DEBUGGINGOP7 [37]                                                                                            Type: KernelGPT4 [275]
                                                                                                                                Type: KernelGPT3 [275]
                                                                                                                                Initializator: LLift1 [138], KernelGPT1 [275]
                       Figure A.18: Direct Code-Classification.                                                                 Leakable parameter: LATTE1 [148]
                                                                                                                                Resource leak-related: InferROI [244]
                                                                                                                                External input: LATTE2 [148]
                                                                                                                                Device name: KernelGPT1 [275]
    Task-Solution Analysis                                                                                                      Settings to run: HITS2 [249]
                                                                                                                                Problem solution steps-related: HITS4 [249]
        Analysis criteria                                                                                                       Used variables & methods: HITS5 [249]
           Correctness of analysis: VulDetect4 [125], LLift2(SelfValid) [138], LLift3(SelfValid) [138]                          Used conditions: HITS5 [249]
               False-positive warning filtering: WitheredLeaf 2 [35], SkipAnalyzer3 [171]                                  Scenario defined: GPTScan3 [220]
            Quality assessment: mrDetector2 [263], LM-PACE3 [288]                                                      Relevance based: SimulinkSlicer [160]
                Scored: GPTLens2 [95], CORE [241]                                                                      Structural
            Reason of failure: AdvSCanner2 [265]                                                                           Blocks of code: CFG-Chain1 [100]
        Domain                                                                                                             Code of blocks: CFG-Chain2 [100]
            Vulnerability analysis: WitheredLeaf 2 [35], GPTLens2 [95]                                             Reactivity
            Root cause analysis: LM-PACE3 [288]                                                                        Request further information: LLift1 [138], KernelGPT2 [275],
            Program analysis: VulDetect4 [125], LLift2(SelfValid) [138], LLift3(SelfValid) [138],                                                      KernelGPT3 [275], KernelGPT4 [275]
                               SkipAnalyzer3 [171]                                                                 Rationalization
            Program repair: CORE [241]                                                                                 Background: GPTScan3 [220]
            Information retrieval: mrDetector2 [263]                                                                   Dependence: SimulinkSlicer [160]
            Exploit generation: AdvSCanner2 [265]
        Rationalization
            Justification: VulDetect4 [125]                                                                     Figure A.21: Code-Elements Identification & Extraction.


Figure A.19: Task-Solution Analysis (some used in the self-reflection frame-
work).


                                                                                                         38
   Text-Elements Identification & Extraction                                                          Focused-Abstractive Summarization

      Extraction criteria                                                                                Abstraction criteria
          Defined role                                                                                       Sign of answer: LM-PACE2 [288]
               Keywords: Cupid [295]                                                                         Scaled assessment: LM-PACE4 [288]
               Variable names: MetaMorph [231]                                                               Concept extraction
               FSM-elements: PROSPER [207]                                                                       Usage: Fuzz4All1 [268], FAIL3 [13]
               Topic related sentences                                                                           Failure described: GameBugDescriptions2 [223]
                   I/O: EMR1 [210]                                                                               Faulty culprit: AutoFL2 [120]
          Best fit                                                                                               Vulnerability described: ChatGPTSCV2 [34]
               Defined structure: FAIL5 [13], AdbGPT1 [64], SysKG-UTF1 [215]                                     Vulnerability mechanism/vector described: LLM4Vuln2 [219], VFFinder1 [267]
               Defined option: FAIL8 [13]                                                                        Incident/Root-cause described: RCACopilot1 [38], x-lifecycle1 [73], VFFinder1 [267],
               Input property                                                                                                                   inContextRCA1 [296]
                   Common root cause: RCACopilot2 [38]                                                           Relevant report elements: ScenicNL1 [60], SoVAR [78], LeGEND1 [225]
      Nature of text                                                                                             Output characterizations: SELF-DEBUGGINGOP4 [37]
          RFC: PROSPER [207]                                                                                     Reason for toxicity: ToxicDetector1 [152]
          Options list: RCACopilot2 [38]                                                                     Timeline: FAIL7 [13]
      Literality                                                                                         Rationalization
          Literal: FAIL5 [13], EMR1 [210], SysKG-UTF1 [215], MetaMorph [231], Cupid [295]                    Thoughts: ChatGPTSCV2 [34]
          Transformative                                                                                     Debate: ScenicNL1 [60]
               Closest meaning: AdbGPT1 [64]

                                                                                                     Figure A.25: Focused-Abstractive Summarization (previous thoughts or ratio-
            Figure A.22: Text-Elements Identification & Extraction.                                  nalizations).

SW-Entity Property Identification & Characterization                                                    What-to-do-Next Generation

   Criteria of characterization                                                                            Generation criteria
       Descriptions & domain corresponding: FSMLOP [17], SELF-DEBUGGINGOP5 [37],                               Most promising: PentestGPT5 [51]
                                              RESTGPT1 [128], Dafny-Synth4a [170], EMR2 [210]                  Coverage oriented: GPTDroid1 [155]
       Code corresponding: CFG-Chain3 [100], LLift2 [138], LLift3 [138], LATTE3 [148],                         Reachability oriented: Pwn’d2 [82], CrashTranslator1 [104], CrashTranslator2 [104]
                              LLMDFA3 [243], WhiteFox1 [274]                                               Domain
       Run-time context corresponding: InputBlaster1 [156], InputBlaster3 [156]                                SW-system integration: PentestGPT5 [51], Pwn’d2 [82], CrashTranslator1 [104],
   Nature of property                                                                                                                  CrashTranslator2 [104], GPTDroid1 [155]
       Input-validity constraint: RESTGPT1 [128], InputBlaster1 [156]                                      Nature of options
       NL-precondition: Dafny-Synth4a [170]                                                                    Open-ended: Pwn’d2 [82], CrashTranslator1 [104], GPTDroid1 [155]
       Precondition constraint to reach code: WhiteFox1 [274]                                                  Close-ended: PentestGPT5 [51], CrashTranslator2 [104]
       NL-postcondition: Dafny-Synth4a [170]                                                               Given context
           Columns of query: SELF-DEBUGGINGOP5 [37]                                                            Enclosing plan: PentestGPT5 [51]
       Qualified post-constraint: LLift2 [138]                                                                 Dynamic annotation: GPTDroid1 [155]
       Code facts                                                                                              GUI context: CrashTranslator1 [104], CrashTranslator2 [104], GPTDroid1 [155]
           Taint-flow: LATTE3 [148]
           Same-value: LLMDFA3 [243]
           Control-flow: CFG-Chain3 [100]                                                                                Figure A.26: What-to-do-Next Generation.
       Summary
           May-must: LLift3 [138]                                                                               Execution
       Metamorphic
           Term equivalence: FSMLOP [17]                                                                            Domain
           NL-relation: EMR2 [210]                                                                                      General code: SELF-DEBUGGINGFL(CoT) [37]
           Bug-revealing mutation: InputBlaster3 [156]                                                                  Pseudocode: E&V1 [81]
   Corrective mode                                                                                                      Intent: TestChain2 [139]
       Self-validation: LLift2 [138], LLift3 [138]                                                                      Assertions: SELF-DEBUGGINGOP7(CoT) [37]
       Feedback based                                                                                               Granularity
           Test results: InputBlaster3 [156]                                                                            Single step: SELF-DEBUGGINGOP7(CoT) [37], E&V1 [81]
   Reactivity                                                                                                           Multiple steps: SELF-DEBUGGINGFL(CoT) [37], TestChain2 [139]
       Requests further info: LLift3 [138]                                                                          Corrective mode
   Rationalization                                                                                                     Feedback based
       Analysis: FSMLOP [17], SELF-DEBUGGINGOP5 [37]                                                                        Verification results: E&V1 [81]
       Thought & assessment: LLMDFA3 [243]                                                                          Reactivity
                                                                                                                       Request further information: E&V1 [81]
                                                                                                                       Request external tool: E&V1 [81], TestChain2 [139]
     Figure A.23: SW-Entity-Property Identification & Characterization.

        Formalization
                                                                                                                                     Figure A.27: Execution.

            Abstraction criteria                                                                                            Textual Data Manipulation
               Intent/Comment corresponding: nl2postcondition [61], Clover6 [217],
                                              RustProof 1 [279], RustC4 [297]                                                  Operation criteria
               Precondition corresponding: RustProof 1 [279]                                                                      Information projection: PentestGPT4 [51]
               Code corresponding: RustProof 1 [279]                                                                              Update: PentestGPT2 [51]
            Nature of formalization                                                                                               Replacement
                 State-predicate                                                                                                       Closest meaning: TARGET3 [52]
                      Postcondition: nl2postcondition [61], Clover6 [217], RustProof 1 [279]                                      Fusion
                      Precondition: Clover6 [217]                                                                                      Control flow graph: CFG-Chain4 [100]
                      Assertion: RustC4 [297]                                                                                          Structure: FuzzingParsers5 [1]
            In-filling context                                                                                                 Nature of structure
                 Annotated code: Clover6 [217], RustProof 1 [279]                                                                 Plan: PentestGPT2 [51], PentestGPT4 [51]
            Corrective mode                                                                                                       Scenario: TARGET3 [52]
                Feedback based                                                                                                    Graph: CFG-Chain4 [100]
                    Compiler: Clover6 [217]                                                                                       String: FuzzingParsers5 [1]



                               Figure A.24: Formalization.                                                                Figure A.28: Textual Data Manipulation.

                                                                                                39
Knowledge Distillation

   Domain
      Vulnerability detection: EditTime1 [30], EditTime2 [30]
      Protocol parsing: ChatAFL1 [168]
      Language parsing: FuzzingParsers1 [1], FuzzingParsers2 [1], FuzzingParsers3 [1]
      Toxicity: ToxicDetector2 [152]
   Nature of knowledge
      Definitions: EditTime1 [30]
          Grammar/Structure: FuzzingParsers1 [1], ChatAFL1 [168]
       Examples: FuzzingParsers2 [1], EditTime2 [30]
           Conceptual: ToxicDetector2 [152]
       Set of items: FuzzingParsers3 [1]



                  Figure A.29: Knowledge Distillation.




                                                                                        40
