                                                 RFCAUDIT: AI Agent for Auditing Protocol
                                                 Implementations Against RFC Specifications
                                                Mingwei Zheng1 , Chengpeng Wang1 , Xuwei Liu1 , Jinyao Guo1 , Shiwei Feng1 ,and Xiangyu Zhang1
                                                          1
                                                            Department of Computer Science, Purdue University, West Lafayette, USA
                                                        Email: {zheng618, wang6590, liu2598, guo846, feng292, xyzhang}@purdue.edu

                                           Abstract—Functional correctness is critical for ensuring the         RFC 8966 3.8.2.1. Avoiding Starvation
                                        reliability and security of network protocol implementations.
                                                                                                                  If a Babel node loses all feasible routes to a destination but still has
                                        Functional bugs, instances where implementations diverge from             unexpired unfeasible routes, it must send a sequence number
                                        behaviors specified in RFC documents, can lead to severe                  request (seqno request) to attempt route recovery.
                                        consequences, including faulty routing, authentication bypasses,
                                        and service disruptions. Detecting these bugs requires deep                                           (a) Babel specification
arXiv:2506.00714v2 [cs.SE] 4 Oct 2025




                                        semantic analysis across specification documents and source code,       void route_lost(struct source *src, unsigned oldmetric) {
                                        a task beyond the capabilities of traditional static analysis tools.       new_route = find_best_route(src->prefix, src->plen, 1, NULL);
                                        This paper introduces RFCAUDIT, an autonomous agent that                   if (new_route) { consider_route(new_route); }
                                                                                                                   else {
                                        leverages large language models (LLMs) to detect functional
                                                                                                                -    if (oldmetric < INFINITY) {
                                        bugs by checking conformance between network protocol im-               +      unfeasible = find_best_route(src->prefix, src->plen, 0, NULL);
                                        plementations and their RFC specifications. Inspired by the             +    if (unfeasible && !route_expired(unfeasible))
                                        human auditing procedure, RFCAUDIT comprises two key com-               +      send_request_resend(NULL, src->prefix, src->plen, …);
                                        ponents: an indexing agent and a detection agent. The former            +    else if (oldmetric < INFINITY)
                                        hierarchically summarizes protocol code semantics, generating                   send_update_resend(…); ..
                                                                                                                    } ..
                                        semantic indexes that enable the detection agent to narrow down
                                        the scanning scope. The latter employs demand-driven retrieval                                     (b) The bug fix in FRRouting
                                        to iteratively collect additional relevant data structures and
                                        functions, eventually identifying potential inconsistencies with the    Fig. 1: An example functional bug in Babel and its fix
                                        RFC specifications effectively. We evaluate RFCAUDIT across
                                        six real-world network protocol implementations. RFCAUDIT
                                                                                                               natural language within RFC documents. In contrast to generic
                                        identifies 47 functional bugs with 81.9% precision, of which 20        low-level safety properties [3], which can often be uniformly
                                        bugs have been confirmed or fixed by developers.                       represented using logical constraints, application-specific high-
                                                                                                               level semantic properties [4]–[7] (or semantic properties in this
                                                                I. I NTRODUCTION
                                                                                                               paper), such as those found in network protocols, are consider-
                                           Network protocols are essential to digital communication,           ably more difficult to formalize due to their reliance on domain
                                        establishing standardized rules that govern data exchange be-          knowledge and context-dependent behaviors. As shown in the
                                        tween devices. They specify message formats and sequencing,            example in Figure 1(a), such properties in the RFC document
                                        as well as mechanisms for routing, connection management,              often require reasoning about the states of multiple protocol
                                        and resource allocation. Due to their complexity, implemen-            entities and the complex interactions among them, making
                                        tations of network protocols are susceptible to functional             encoding such properties inherently intricate. Second, the
                                        bugs—logical errors that cause deviations from intended be-            diversity of semantic properties significantly hinders the devel-
                                        haviors, which undermines the reliability and security of net-         opment of effective detection mechanisms. Conventional bug
                                        work infrastructures. For example, the Zerologon vulnerability         detection techniques, such as constraint-based methods (e.g.,
                                        (CVE-2020-1472 [1]) in Microsoft’s Netlogon Remote Proto-              symbolic execution [8]–[12]) and graph-based reasoning ap-
                                        col (MS-NRPC) [2] stemmed from improper initialization of              proaches (e.g., data-flow reachability analysis [13], [14]), are
                                        a cryptographic vector, which allows attackers to impersonate          inadequate for automatically validating the semantic properties
                                        any host, including domain controllers, and gain unauthorized          of network protocols. These methods cannot automatically
                                        domain administrator access. Due to its critical severity, it was      localize the functions relevant to specific properties and verify
                                        assigned a maximum CVSS score of 10.0.                                 their compliance with the specification. For instance, it is
                                           To enhance the reliability and security of network protocols,       challenging to localize the function route_lost shown in
                                        it is essential to identify functional bugs in their implementa-       Figure 1(b) and leverage a uniform reasoning framework to
                                        tions. Manually detecting such bugs is notoriously difficult,          detect violations of the associated semantic property.
                                        as developers have to compare the implementation against
                                        every relevant clause in lengthy RFC documents—a process                  Although recent studies have proposed various techniques
                                        that demands significant human effort and domain expertise.            for bug detection in network protocol implementations, they
                                        However, automating functional bug detection remains a chal-           remain inadequate to effectively identify functional bugs. In
                                        lenging task. First, the semantic properties depicting protocol        general, existing approaches fall into three categories. First,
                                        functionality are highly diverse and expressed informally in           fuzzing techniques aim to uncover bugs by generating crash-
triggering inputs [15]–[17]. However, functional bugs typically          by retrieving callers or callees until a conclusion can be
do not cause crashes or other observable anomalies, making               drawn. The retrieved functions can also support self-critics
them difficult for fuzzing-based methods to detect. Second,              in the detection, during which the detection agent reviews its
differential analysis can reveal behavioral inconsistencies and          own reasoning steps upon the retrieved functions to mitigate
discover potential functional bugs by comparing multiple                 hallucinations and improve the precision of the detection.
independent implementations of the same protocol [18]–[20].               We implement RFCAUDIT as a prototype [23], powered by
Yet, this approach depends on the availability of high-quality        Claude 3.5 Sonnet. We apply RFCAUDIT to the implementa-
alternative implementations and does not guarantee confor-            tions of six widely-used network protocols, including Babel,
mance to the original specification, thereby limiting its recall      DHCP, and IGMP, and assess its ability to detect functional
for functional bug detection. Third, formal verification offers       bugs according to the corresponding RFC documents. It is
strong semantic guarantees but requires rigorous formalization        shown that RFCAUDIT successfully identifies 47 zero-day
of protocol properties and formal reasoning frameworks [21],          functional bugs with a high precision of 81.9%. In comparison,
[22]. These requirements may not be easily achievable for real-       existing advanced agents, such as Copilot powered with three
world protocols due to the informal and diverse specifications        advanced models: Claude 3.7 Sonnet, Claude 3.5 Sonnet, and
highlighted above. These limitations suggest the need for a           GPT-4o, only identify 26 bugs on average, while exhibiting a
new paradigm of bug detection that enables semantic reasoning         substantially higher average false positive rate of 77.5%. We
on both informal specifications and implementation behavior,          further conduct comprehensive ablation studies, which high-
an essential capability for effectively detecting functional bugs.    light the significant precision gains attributed to the designs
   This paper presents RFCAUDIT, the first LLM agent for              of code semantic indexing and retrieval-guided detection. In
detecting functional bugs in network protocol implementa-             summary, our work makes the following contributions:
tions. Our approach is motivated by the observation that              • We propose RFCAUDIT , the first LLM agent that checks the
LLMs exhibit strong capabilities in understanding both natural           compliance of network protocol implementation and RFC
language specifications, such as RFC documents, and the                  documents for functional bug detection.
semantics of code snippets when they are well scoped, such            • We introduce a multi-agent design that summarizes code
as those spanning just a few related functions. Notably, RFC             functionalities as semantic indexes and leverages them for
documents are typically well-structured and articulate protocol          demand-driven code retrieval, facilitating functional bug
specifications clearly in natural language. Meanwhile, protocol          detection with high precision.
implementations often follow intuitive naming conventions             • We evaluate RFCAUDIT on six network protocol implemen-
that reflect the functionality of functions and modules. This            tations and identify 47 functional bugs with 81.9% precision,
suggests a promising opportunity: Given an informal property             outperforming existing LLM-based baselines in both preci-
described in an RFC, we can leverage LLMs to align the                   sion and semantic coverage. 20 of the detected bugs have
natural language description of the property with the code               been confirmed or fixed by the respective developers.
structure. If the functions related to the property can be
precisely identified by further code retrieval (e.g., along calling                           II. OVERVIEW
contexts), LLMs can perform comprehensive and accurate                   In this section, we begin with a real-world functional bug in
reasoning over these functions to discover potential functional       a network protocol implementation and discuss the limitations
inconsistencies, thereby enabling functional bug detection.           of existing approaches (Section II-A). Then we provide the key
Technically, RFCAUDIT consists of two collaborative agents,           ideas of our approach (Section II-B) with illustrative examples.
namely an indexing agent and a detection agent, which
                                                                      A. Motivating Example
perform the following core analyses, respectively.
                                                                         Figure 1 shows a real-world functional bug in FRRout-
• Code Semantic Indexing. To bridge informal properties in            ing, a collaborative project under the Linux Foundation with
  RFC documents with relevant code scope, the indexing                over 400 contributors, powering major open-source large-scale
  agent constructs hierarchical semantic indexes of the pro-          networking platforms like Microsoft’s SONiC and Amazon’s
  tocol implementation using LLMs, which summarizes the               DENT. According to the RFC document shown in Figure 1(a),
  semantics of functions, files, and directories into concise         when a node loses all feasible routes to a destination but
  natural language descriptions. Such semantic indexes allow          still holds unexpired unfeasible routes, it MUST send a
  RFCAUDIT to narrow down the scope of functions relevant             sequence number (seqno) request to trigger route recovery.
  to the target property, significantly reducing token and time       An unfeasible route means a neighbor recently advertised a
  costs during the detection.                                         path that is not currently usable, but might become valid again.
• Retrieval-Guided Detection. To collect sufficient contexts,         Sending a seqno request prompts that neighbor to re-announce
  the detection agent progressively retrieves additional rele-        the route, potentially restoring connectivity. However, the
  vant functions using symbolic tools driven by the LLM. If           original implementation fails to check for unfeasible routes,
  the currently available context suffices to validate or refute      which can leave the router in a starved state with no way
  conformance to the semantic property, RFCAUDIT proceeds             to recover, causing persistent connectivity loss in dynamic
  to the next property. Otherwise, it augments the context            networks. As shown in Figure 1(b), the fix adds an explicit
                                                                                   Detection Agent
                            Indexing Agent
        Code                                                                Localize              Retrieve
                                                     Hierarchical
                                                    Semantic Index
                                                                             Detect                Validate
                                                                                                                        Bug
        RFC
                                               Fig. 2: The workflow of RFCAUDIT

check for unexpired unfeasible routes and issues a seqno                which involves exploring a large codebase without clear
request when such a route is found, ensuring RFC compliance             guidance from the RFC document.
and preventing persistent routing failure. This bug has been         • Even after locating a relevant function, LLMs may still
confirmed and fixed by the developers.                                  struggle to determine whether the implementation satisfies
    However, detecting functional bugs is extremely challeng-           the intended property. Since a semantic requirement is of-
ing [18], [24]. Traditional bug detection methods, such as              ten implemented through multiple interconnected functions
fuzzing [15], [25], [26] and static analysis [27], [28], primarily      spread across files or modules, LLMs typically need addi-
focus on identifying low-level issues like memory corruption.           tional contexts, such as the functions find_best_route
Consequently, these approaches are ineffective against non-             and send_update_resend in Figure 1.
crashing protocol non-compliance, such as the bug illustrated            To tackle these challenges, we draw inspiration from the
in Figure 1. Model checking techniques also encounter sig-           way human developers typically audit functional correctness
nificant difficulties in detecting this bug, primarily due to        against protocol specifications. When verifying whether a
their dependence on explicitly specified and formally defined        particular semantic property is correctly implemented, experi-
properties. For instance, tools such as CMC [22] and UP-             enced developers first perform a preliminary walkthrough of
PAAL [29] efficiently verify high-level behaviors like state         the codebase to become familiar with the roles of different
transitions and message sequencing, while struggling to cap-         functions, files, and modules. They then progressively gather
ture diverse and nuanced semantic properties, exemplified in         additional program constructs, such as related functions or data
Figure 1(a). Moreover, even when semantic properties can be          structures, to reason about the correctness of the implementa-
explicitly specified, model checking requires extensive manual       tion and identify potential violations.
abstraction efforts, which are often labor-intensive and error-          RFCAUDIT mirrors this human auditing process through
prone, constraining their practical applicability. Lastly, recent    two key technical components: code semantic indexing and
studies such as ParDiff [18] and ParCleanse [30] target non-         retrieval-guided detection. The former creates a semantic map
crashing parsing bugs by inferring valid packet formats from         of the codebase by summarizing the functionality of functions,
code or RFCs. Although effective in identifying parser-related       files, and directories in natural language, allowing fast and
issues, these approaches fall short in detecting functional bugs     informed localization of potentially relevant code. The latter
that involve more complex semantic properties in components          incrementally augments the reasoning context with related
beyond network packet parsers.                                       program constructs, enabling the system to validate a property
B. RFCAUDIT in a Nutshell                                            when its implementation spans multiple functions or modules.
    To bridge the gap, we propose RFCAUDIT, an LLM-                  These two techniques are realized through two collaborative
powered autonomous agent that identifies semantic incon-             agents in RFCAUDIT, the indexing agent and the detection
sistencies between source code and RFC documents. Our                agent, whose respective workflows are illustrated in Figure 2.
approach is motivated by the observation that LLMs, having           • Indexing Agent. The indexing agent performs semantic
been pre-trained on vast corpora of natural language and pro-           summarization and generates hierarchical semantic indexes
gramming code, exhibit strong capabilities in understanding             at the directory, file, and function levels. As shown in
both the specification offered by the RFC document and pro-             Figure 3(a), for the Babel protocol, files like route.c
gram semantics in the code. For instance, given the semantic            and message.c, as well as functions like route_lost,
property shown in Figure 1(a) and the buggy implementation              find_best_route, and send_update_resend, are
in Figure 1(b), LLMs can potentially identify the inconsistency         annotated with concise summaries of their functionality.
between the RFC documents and the corresponding imple-                  These semantic descriptions are later utilized by the detec-
mentation logic. However, applying LLMs for functional bug              tion agent to navigate and localize relevant code.
detection in network protocols is far from trivial, requiring us     • Detection Agent. Given a semantic property, the detection
to resolve two critical technical challenges.                           agent uses hierarchical indexes to identify inconsistencies.
• Due to the lack of direct correspondence between RFC                  As shown in Figure 3(b), it proceeds with four actions
   segments and source code, identifying where a high-level             in five steps: (1) Use the semantic indexes to localize
   property is realized in the implementation is quite difficult.       a relevant function, such as route_lost; (2) Detect
   For instance, checking the property in Figure 1(a) requires          inconsistencies based on this context; (3) Retrieve addi-
   finding the related function route_lost in Figure 1(b),              tional relevant functions, such as find_best_route and
             Repo Structure                                                         Hierarchical Semantic Index

         Repo: FRRouting/frr                           babeld/:
                                                        route.c: Manage and maintain routing tables
           babeld/                      Indexing           - route_lost: handle route loss by finding an alternative route or requesting updates
              route.c                    Agent             - find_best_route: search for the best acceptable route
                    route_lost                          message.c: Message handling and communication
                    find_best_route                        - send_update_resend: send an update message for a network prefix and records it
                                                            …
               message.c
                   send_update_resend
                …                                         (a) An example of indexing agent
                                                                               Step 3. Retrieve
         Task Description: Find functional inconsistencies between the
         code and its RFC specification.                                        Q: Based on the previous LLM reasoning chain, retrieves
         - Code: {Hierarchical Semantic Index}                                  additional context using the following tools: Query(name),
         - RFC document: {RFC 8966 Section 3.8.2.1}                             Query_Callee(call), Query_Caller(fun).

                                                                                A: Query_Callee(route_lost)
                                           Detection Agent
        Step 1. Localize                                                       Step 4. Detect
          Q: According to a document section, identify which functions           Q: Given a document section and the source code, determine
          are most relevant to the behavior described in the document            whether the code satisfies the described behavior.
          section.                                                               struct babel_route * find_best_route (..) ..
                                                                                 struct void send_update_resend(..) ..
          A: The function route_lost is the most relevant because it             Return "Yes" if matches, or "No" with the functional bug
          handles route loss.                                                    description, or "Unknown" if need extra contexts.
         Step 2. Detect
                                                                                A: No. I found one functional bug: Missing Check for
          Q: Given a document section and the source code, determine            Unexpired Unfeasible Routes in route_lost.
          whether the code satisfies the described behavior.
          void route_lost (..) ..
          Return "Yes" if matches, or "No" with a brief explanation if         Step 5. Validate
          not, or "Unknown" if need extra contexts.                             Q: Review the functional bug and confirm whether it is a true
                                                                                violation of the specification or a false positive.
          A: Unknown. I cannot make decisions without the definitions
          of find_best_route and send_update_resend.                            A: Yes, I confirm this is a true functional bug because ..

                                                      (b) An example of detection agent
                                   Fig. 3: Illustrative examples of the two agents in RFCAUDIT

  send_update_resend, if the context is insufficient; (4)                      and directories as summaries, as they often suggest the in-
  Draw a conclusion about a potential violation; and (5)                       tended functionality [31], [32]. However, such names are not
  Apply a self-critique strategy to reassess the reasoning for                 always informative enough to capture precise semantics. For
  hallucination mitigation.                                                    example, in the Babel implementation shown in Figure 1,
                                                                               both babeld.c and babel_main.c reside in the same
                        III. O UR A PPROACH                                    directory, yet their names do not clearly reveal their dis-
   RFCAUDIT emulates the reasoning process of human de-                        tinct functionalities. To generate more informative semantic
velopers when auditing for functional bugs and consists of                     indexes, we leverage LLMs to summarize the contents of
two collaborative agents, the indexing agent and the detection                 functions, files, and directories, producing concise natural
agent, which support scalable and effective functional bug                     language descriptions that form a hierarchical semantic view
detection upon network protocol implementations. In what                       of the implementation.
follows, we present more technical details of the two agents                      As shown in Figure 4, the indexing agent constructs hier-
with concrete prompts and illustrative examples.                               archical semantic indexes in a bottom-up manner. It begins at
                                                                               the function level, where each function definition is passed to
A. Phase 1: Code Semantic Indexing                                             the LLM with a prompt, which asks for a concise summary
   To bridge RFC documents with relevant code segments,                        of its semantics. At the file level, summaries of all functions
we follow the behavior of human developers by construct-                       within the same source file are aggregated to prompt the LLM
ing semantic indexes over the protocol implementation. This                    to generate a description of the file’s overall functionality,
approach enables us to capture the semantics of the code                       capturing how individual behaviors contribute to the role of the
in a manner analogous to the way developers form a high-                       file in the protocol implementation. This process continues at
level understanding of the implementation. Basically, a simple                 the directory level, where the agent combines summaries of all
indexing design is to utilize the names of functions, files,                   files and subdirectories to generate a higher-level description
                 Phase 1: Code Semantic Indexing                                                                        LLM Prompts
                                                                                         Function-level Summary
   Repo-level         Directory-level           File-level         Function-level
                                                                                         Summarize the following section from a technical document: { Section }
   Summary              Summary                 Summary              Summary
                                                                                         Write a 1-2 sentence summary of this section.
                                                                        f(x)             File-level Summary
                                                                        g(x)             Here is a list of functions in a file and their summaries: { Function Summaries }
                                                                        h(x)             Write a paragraph summary of this file based on the above functions.
                                                       ...                               Directory-level Summary
                                                                                         Here is a list of files or sub-directories under a directory and their summaries:
                            Bottom-up Summary                                            { File or Sub-directory Summaries }
                                                                                         Write a paragraph summary of this directory based on the summaries above.

                                     Fig. 4: The workflow of code semantic indexing and prompt templates

 Find functions most relevant     Retrieve contexts                                          B. Phase 2: Retrieval-guided Detection
 to the RFC requirements.         using provided tools.

                                                   On-demand             Tools                  As demonstrated in Section III-A, the hierarchical semantic
        Stage 1:                        Stage 3                   o Query(name)
        Localize                        Retrieve                  o Query_Callee(call)
                                                                                             indexes allow us to effectively bridge RFC documents with
                                                      Return
                                                                  o Query_Caller(fun)        their corresponding implementation functions. Similar to how
                                No functional bug detected                                   human developers audit code, the analysis often requires
                                                                                             collecting additional program constructs, such as caller/callee
        Stage 2:                        Stage 4:
                                                                         Done                functions and data structure definitions, to augment the context
         Detect     Functional bug      Validate      Report as TP
                      detected                        or filter as FP                        until a reliable conclusion can be drawn regarding the confor-
 Compare the retrieved           Check the reported                                          mance or violation of a given semantic property. Building on
 contexts with the RFC           functional bugs to filter
 requirements.                   out false positives.                                        this insight, we introduce the detection agent, which performs
                                                                                             retrieval-guided detection to identify inconsistencies between
      Fig. 5: The state machine of the detection agent                                       the RFC specification and the code as functional bugs.
                                                                                                Technically, the retrieval-guided detection begins by pre-
of the directory. Finally, summaries from all directories are ag-
                                                                                             processing the RFC document and segmenting it into sections
gregated into a repository-level summary, which is a top-level
                                                                                             and subsections based on its structural headings. From each
directory summary, reflecting the system’s overall structure
                                                                                             subsection, the LLMs extract mandatory semantic properties,
and responsibilities. This bottom-up indexing process produces
                                                                                             which serve as guides for the detection process. A single
a structured semantic index aligned with the code hierarchy,
                                                                                             subsection may yield multiple properties depending on its
enabling precise and efficient retrieval during detection. The
                                                                                             content. For each semantic property, the detection agent scans
corresponding prompt templates for each indexing level are
                                                                                             the implementation by following a workflow similar to a
shown on the right of Figure 4. Notably, the code semantic
                                                                                             finite state machine, as illustrated in Figure 5. Specifically, it
indexing is one-time effort. When the codebase changes, we
                                                                                             first localizes relevant functions for inspection (Localization),
can incrementally update the indexes. In our evaluation, we
                                                                                             determines whether the implementation satisfies the RFC
choose the Claude 3.5 Sonnet model and the average cost for
                                                                                             requirement (Detection), and, if necessary, retrieves additional
a full repository is $1.89, shown in Table V. We can also
                                                                                             context (Retrieval). When a potential functional bug is found,
consider using cheaper models for indexing as the task is
                                                                                             the detection agent examines the reasoning chain that produces
relatively simple and does not rely on strong reasoning ability.
                                                                                             the reported bug via self-criticism (Validation). In the follow-
                                                                                             ing subsections, we provide further details on each component
Example 1. Consider the repository structure shown on the                                    of the detection workflow shown in Figure 5.
left of Figure 3(a). We first ask the LLMs to summarize
each function. For example, route_lost handles route loss,                                   Localization. Guided by the pre-built hierarchical semantic
find_best_route searches for the best acceptable route,                                      indexes, the detection agent first identifies functions that are
and send_update_resend sends and records update mes-                                         likely responsible for implementing the behavior described
sages. Next, the function-level summaries under the same file                                in a given RFC section. This localization is performed in
are combined to produce a file-level summary that captures                                   a top-down manner. Starting from the root directory of the
the main responsibility of each file. In this case, we can                                   protocol implementation, it navigates through different levels
discover that route.c focuses on route maintenance, and                                      of directories and files by instantiating the prompt template
message.c on inter-node communication. Finally, all file                                     shown in Figure 6(a). At each level, it reviews the semantic
summaries are merged into a directory-level summary for                                      summaries of directories or files, selects those most relevant to
the babeld module. Lastly, we can obtain the hierarchical                                    the RFC section, and descends into the selected entries. Upon
semantic indexes shown on the right of Figure 3(b).                                          reaching a file, it examines the summaries of its functions
                                                                                             and identifies those that align with the described behavior.
 Localization Prompt                                                  Detection Prompt
 According to a document section, identify which entries are most     Given a document section and the source code, determine whether the
 relevant to the behavior described in the document section.          code satisfies the described behavior. { Document Section } { Code }
 { Document Section } { Entry Summaries }                             Return "Yes" if matches, or "No" with a brief explanation if not, or
 Return a list of names: ["file.c", "subdir"] or ["fun1", "fun2"].    "Unknown " if need extra contexts.
                     (a) Prompt used for Localization                                      (b) Prompt used for Detection
 Retrieval Prompt                                                     Validation Prompt
 Based on the previous LLM reasoning chain, retrieves additional      Review the functional bug and confirm whether it is a true violation of
 context using the following tools: Query(name),                      the specification or a false positive.
 Query_Callee(call), Query_Caller(fun).                               { Document Section } { Code } { Functional Bug }
 { LLM Reasoning Chain }                                              If the functional bug is valid, confirm it. If not, explain why.
                       (c) Prompt used for Retrieval                                      (d) Prompt used for Validation

                                       Fig. 6: The prompt templates used in the detection agent

Because this search process is recursive, the final set of                               RFC 8966 3.8.2.1. Avoiding Starvation
relevant functions may span multiple files across the codebase.
                                                                                                              babeld/
Detection. Based on the localized relevant functions, the                                Localize
detection agent attempts to identify inconsistencies between
                                                                          Localize      route.c               message.c       …
the implementation and the RFC. Using the template in
Figure 6(b), it queries the LLM to make one of three decisions,            route_lost             find_best_route         send_update_resend
as shown in Figure 5. Specifically, if the LLM detects a                                           Retrieve               Retrieve
potential functional bug, the agent proceeds to validate it (see
the Validation stage below). If the LLM concludes that the                    Fig. 7: An illustrative example of Phase 2
implementation conforms to the RFC requirement, the agent
terminates the analysis for the current property. Otherwise, the     continued analysis. The LLM prompt is shown in Figure 6(c).
current context is insufficient, the agent initiates an additional   Validation. Due to the potential lengthy detection context, the
retrieval to expand the context (see the Retrieval stage below).     LLMs may hallucinate and report a false positive. To mitigate
Notably, the detection agent resembles the reasoning pattern         hallucination, we employ self-critics [33] in the detection
of human developers, who iteratively gather evidence from the        agent. Specifically, the detection agent reviews all available
program constructs to identify potential bugs or to justify the      information, including the RFC section, the retrieved context,
correctness of an implementation.                                    and earlier reasoning steps, to make a final judgment. If the
Retrieval. To assist the LLM in identifying functional bugs          violation is confirmed, the functional bug is reported as a
or justifying correctness, the detection agent enables demand-       true positive. Otherwise, it is discarded as a false positive. It
driven retrieval of additional program constructs. This is           may also uncover bugs missed during previous detection. The
achieved by equipping the LLM with a set of predefined               prompt is instantiated using the template in Figure 6(d). Our
tools, which it can invoke through function calls as needed.         results in Section IV-E show that the self-critics can reduce
Specifically, the agent provides three types of tools. First,        the false positives by 71.7% (from 63.9% to 18.1%).
Query(name) retrieves the definition of a data structure and         Example 2. Given the RFC section in Figure 1(a) and
a macro. This is useful when the current context references          the semantic indexes in Figure 3(a), the detection agent
symbols whose definitions are not yet available. Second,             identifies the relevant function route_lost in route.c
Query_Callee(call) returns the definition of the callee              (Figure 7). Finding its context insufficient, the agent retrieves
function invoked at the specified call site. This is used when       find_best_route and send_update_resend, which
the current function doesn’t provide enough information to de-       select candidate routes and issue reactive updates, respectively.
termine whether the behavior matches the RFC, and the LLM            Notably, send_update_resend resides in a different file.
suspects that the called function contains important logic. This     With this broader context, the agent observes that only feasible
selective strategy enables the LLM to focus on semantically          routes are searched (flag = 1) and no sequence number
meaningful functions while avoiding unnecessary expansion            request is made in the fallback logic, violating the starvation
of trivial or unrelated calls. Third, Query_Caller(fun)              prevention rule. Retrieval stops here, and the bug is finally
retrieves all callers of the function fun, allowing the LLM          identified as shown in Figure 1. The whole process is detailed
to examine how the function is used, particularly whether            in Figure 3(b).
its preconditions are satisfied by the callers. These retrieval
operations are triggered on demand, guided by the LLM’s                         IV. I MPLEMENTATION AND E VALUATION
reasoning. Benefiting from model’s planning ability, the LLMs          RFCAUDIT is implemented atop AutoGen [34], a multi-
can choose the proper tools for retrieval. The retrieved results     agent framework designed for building LLM applications. To
further augment the analysis context in the Detection stage for      extract functional specifications, we collect RFC documents
          TABLE I: The statistics of evaluation subjects.                                       TABLE II: The statistics of main results.
  Name      Description                                    LoC     Version (#Page)                                                           Unique Bug
                                                                                      Protocols     #Incons.     TP     Precision                             #Total Bug
  Babel     Distance-vector Routing Protocol                9.6K   RFC 8966 (54)                                                         #New      #Old
  BFD       Bidirectional Forwarding Detection Protocol    17.3K   RFC 5880 (49)
  NHRP      NBMA Next Hop Resolution Protocol               9.2K   RFC 2332 (52)      Babel            16    12   75.0%     8                        2           10
  RIPng     Routing Information Protocol Next Generation    9.3K   RFC 2080 (19)      BFD              30    28   93.3%     9                        5           14
  DHCP      Dynamic Host Configuration Protocol             8.6K   RFC 2131 (45)      NHRP             12Functional
                                                                                                             10     Bug Lists
                                                                                                                  83.3%    10                        0           10
  IGMP      Internet Group Management Protocol              5.2K   RFC 2236 (24)
                                                                                      RIPng            3      2   66.7%     2                        0            2
                                                                                      DHCP             12     8   66.7%     4                        0            4
 in plain text format and derive informal functional properties                       IGMP             10     8   80.0%     7                        0            7
 through structured segmentation of the textual content. We                           Total            83         68         81.9%           40      7           47
 employ Claude 3.5 Sonnet [35] as the underlying LLM for
 RFCAUDIT, configured with a temperature of 0.0 to enforce
 greedy decoding. This setting reduces randomness in model re-
                                                                                                               Demultiplex
 sponses, thereby enhancing the consistency and reproducibility                                                   (2)                                 State
 of RFCAUDIT. To facilitate the indexing and detection agents,
                                                                                                                                     State            Routing
 we implement analysis tools using Tree-sitter [36], a parsing                                     Parsing
                                                                                                    (11)                              (15)            Timer
 library for different programming languages. In particular, we
 construct call graphs by leveraging function names and the                                                                                           Config
 numbers of their associated parameters or arguments. The                                                                                             Err Handle
                                                                                              Err Handle
 output generated by the indexing agent is stored in a JSON file,                                 (2) Config                                          Parsing
 enabling incremental analysis as the protocol implementation                                          (3)                   Routing                  Demultiplex
                                                                                                               Timer           (7)
 evolves. This design avoids redundant processing by skipping
                                                                                                                 (7)
 the analysis of unchanged functions, files, and modules.
    To assess the performance of RFCAUDIT, we conduct
 experiments to address the following research questions:
                                                                                          Fig. 8: Distribution of functional bug categories.
• RQ1: How effective does RFCAUDIT identify functional
  bugs in real-world network protocol implementations?                               reported issue, we manually verify whether it represents a real
• RQ2: How does RFCAUDIT compare to existing approaches?                             violation, and record the counts of true and false positives
• RQ3: What are the runtime and token costs of RFCAUDIT ?                            to compute precision. Since a single underlying issue may
• RQ4: How do the two agents contribute to performance?                              result in multiple reported bugs (e.g., when the same property
 A. Dataset                                                                          is described across multiple sections of the RFC), we group
                                                                                     relevant reports into unique bugs. For each unique bug, we
    We evaluate RFCAUDIT on six protocol implementations
                                                                                     check the project’s issue tracker and pull requests to determine
 from two widely-used, open-source network stacks: FRRout-
                                                                                     whether it is a previously unreported bug (i.e., new) or a known
 ing [37] and lwIP [38]. FRRouting (FRR) is an Internet
                                                                                     issue (i.e., old) that has not yet been fixed in the latest version.
 routing protocol suite for Linux and Unix platforms, with
 over 3.6K stars on GitHub. It is deployed in production by                             Results. As shown in Table II, RFCAUDIT generates a total
 major infrastructure providers such as NVIDIA and Orange,                           of 83 bug reports across six protocols, of which 68 are true
 and is distributed through mainstream Linux repositories in-                        positives, yielding an overall precision of 81.9%. Grouping
 cluding Debian and Fedora. lwIP is a lightweight TCP/IP stack                       related bug reports, we uncovered 47 unique bugs, including
 designed for resource-constrained environments, with over                           40 new bugs and 7 already reported ones. To date, 20 out of 47
 1.3K stars on GitHub. It is widely integrated into embedded                         unique bugs have been confirmed or their patches have been
 systems, IoT platforms, and real-time applications, and has                         approved or merged by the developers. Overall, these results
 been adopted by vendors like Intel, Xilinx, and Freescale.                          demonstrate that RFCAUDIT is effective in identifying bugs
 Overall, both FRRouting and lwIP are actively maintained                            across diverse protocols. To better understand the diversity
 and widely used in practice, making them ideal subjects for                         of functional bugs detected by RFCAUDIT, we categorize
 assessing RFCAUDIT across diverse deployment contexts. For                          the 47 unique bugs into seven categories, namely Parsing,
 each protocol, we collect the corresponding RFC that the                            Config, Routing, Err Handle, State, Timer, and Demultiplex.
 implementation is based on as the reference. The protocol                           As shown in Figure 8, most bugs fall under State (15/47) and
 implementation sizes range from 5.2 KLoC to 17.3 KLoC,                              Parsing (11/47), reflecting common pitfalls in protocol state
 whereas the corresponding RFC documents span between 19                             management and input validation. RFCAUDIT also uncovered
 and 54 pages. The detailed information is shown in Table I.                         Timer misconfiguration (e.g., incorrect IGMP delays), Demul-
                                                                                     tiplexing issues (e.g., incorrect BFD session lookup), and Err
 B. RQ1: Effectiveness of RFCAUDIT                                                   Handle gaps (e.g., miss error-on-error prevention). This variety
    1) The Effectiveness of Bug Detection: To answer RQ1,                            highlights the ability of RFCAUDIT to detect diverse semantic
 we apply RFCAUDIT to each protocol implementation and                               violations specified by the RFCs. Full bug details are available
 its corresponding RFC to detect inconsistencies. For every                          in our artifact [23].
            TABLE III: The precision, recall and F1 score of context retrieval. NA indicates that the divisor is 0.
                                               After Localization                                              After Retrieval
 Protocol    Properties                                                                                                                                    #Miss
                           Function (%)             Type (%)         Macro (%)         Function (%)             Type (%)               Macro (%)
 Babel          15        50.0 / 91.7 / 64.7      NA / 0.0 / NA     NA / 0.0 / NA     50.0 / 91.7 / 64.7   100.0 / 100.0 / 100.0   100.0 / 100.0 / 100.0    1
 BFD            22        57.1 / 66.7 / 61.5      NA / 0.0 / NA     NA / 0.0 / NA    72.7 / 100.0 / 84.2    66.7 / 100.0 / 80.0    100.0 / 100.0 / 100.0    0
 NHRP           15        71.4 / 85.7 / 77.9      NA / 0.0 / NA     NA / 0.0 / NA     76.9 / 95.2 / 85.1   100.0 / 100.0 / 100.0   100.0 / 100.0 / 100.0    0
 RIPng          24        60.7 / 70.8 / 65.4      NA / 0.0 / NA     NA / 0.0 / NA    37.3 / 100.0 / 54.3    100.0 / 33.3 / 50.0       NA / 0.0 / NA         0
 DHCP           34        60.7 / 68.0 / 64.1      NA / NA / NA      NA / NA / NA      65.3 / 94.0 / 77.1      NA / NA / NA            NA / NA / NA          0
 IGMP           21        52.9 / 75.0 / 62.0      NA / NA / NA       NA / 0.0 /           / 100.0 /           NA / NA / NA         100.0 / 100.0 / 100.0    0
 Total          131       59.3 / 71.3 / 65.6      NA / 0.0 / NA     NA / 0.0 / NA    56.0 / 95.1 / 70.5     87.5 / 77.8 / 82.4     100.0 / 75.0 / 100.0     1


   2) The Effectiveness of Context Retrieval: To assess context                     function, type or macro definitions are not retrieved; (ii) RFC
retrieval accuracy, we manually construct ground-truth map-                         misinterpretation (6 cases), where RFCAUDIT mistakenly
pings for each RFC property. Each property is annotated with                        treats optional or incorrect properties as mandatory require-
the minimal set of functions, types, and macros required to                         ments; (iii) code misinterpretation (5 cases), where RFCAU -
capture its semantics. Since this annotation is labor-intensive,                    DIT retrieves the correct context but fails to correctly interpret
we sample 30 RFC subsections (5 per protocol) from our                              the code’s control flow or semantics; and (iv) intentional
datasets, covering a total of 131 properties across six protocols.                  implementation choice (1 case), where the observed behavior
For each property, we compare the elements retrieved by                             is a deliberate deviation from the RFC. The most common
RFCAUDIT against the ground truth and measure precision,                            root cause is RFC misinterpretation, including 4 cases where
recall, and F1 score after two stages: (i) localization and (ii)                    the LLM extracts incorrect properties and 2 cases where the
retrieval. We then compute average recall across all sampled                        LLM treats optional clauses as mandatory. Such errors may
properties to assess how effectively RFCAUDIT collects the                          be mitigated by fine-tuning the LLM on RFC texts to improve
necessary context for inconsistency detection. Since both the                       its ability to extract correct mandatory requirements.
retrieved element count and ground truth element count can
be zero for types and macros, making recall undefined, we                           C. RQ2: Baseline Comparison
use “NA” to indicate these cases. Finally, we examine missed                           We compare RFCAUDIT with GitHub Copilot and LTL-
bugs and identify those caused by incomplete retrieval.                             Fuzzer [4]. We do not compare with other network protocol
   Results. Table III reports the context retrieval accuracy                        bug detection tools, as they either cannot detect functional
across protocols. In the localization stage, RFCAUDIT re-                           bugs (e.g., ChatAFL [15], NetLifter [26]), or target narrow
trieves 172 functions, of which 102 are true positives, yielding                    scope like parsing (e.g., ParCleanse [30], ParVAL [39]).
59.3% precision and 71.3% recall (102 of 143 ground-truth                              1) Comparison with GitHub Copilot: We compare RF-
functions). This stage is limited to function retrieval and, by                     CAUDIT with GitHub Copilot using three LLMs: Claude 3.7
design, does not include types or macros. After the retrieval                       Sonnet (Thinking Mode), Claude 3.5 Sonnet, and GPT-4o.
stage, precision is 56.0% for functions (136 of 243), 87.5%                         All are accessed via Copilot’s Workspace Chat interface in
for types (7 of 8), and 100.0% for macros (7 of 7). More                            VS Code, which supports repository-level queries. To match
importantly, recall improves significantly—95.1% (136 of 143)                       RFCAUDIT’s design, we provide Copilot with one RFC
for functions, 77.8% (7 of 9) for types, and 75.0% (6 of 8)                         section per prompt and ask it to identify deviations from im-
for macros—with only one bug missed overall, caused by                              plementations. For Claude 3.7 Sonnet, we manually examine
code misinterpretation rather than missing context. In this                         all generated bug reports. However, Claude 3.5 Sonnet and
task, recall is more critical than precision. Low precision                         GPT-4o produce hundreds of candidates, making full manual
only means that unnecessary elements are retrieved, causing                         validation impractical. To avoid over-reporting and minimize
additional overhead, while low recall means the needed context                      false positives, we instruct each LLM baseline to only report
is completely missed, preventing the detection of true incon-                       bugs with 100% confidence. To enable a fair and scalable
sistencies. Note that achieving high precision is challenging                       evaluation, we adopt a sampling-based evaluation. For each
for two reasons: (1) some functions are semantically close                          protocol, we randomly sample up to twice the number of
to the target property but not truly relevant, making them                          bug reports identified by RFCAUDIT (e.g., since RFCAUDIT
difficult to filter out, and (2) a single RFC property is often                     generates 16 bug reports for Babel, we sample 32). If the
distributed across multiple functions or files, so aggressive fil-                  model produces fewer than that, we evaluate all of them. Each
tering risks discarding essential information. For these reasons,                   sampled case is manually reviewed by a domain expert.
our retrieval design explicitly prioritizes recall, even at the                        Results. Table IV shows the performance of GitHub Copilot
cost of including borderline or loosely related items. Precision-                   under three model configurations. With Claude 3.7 Sonnet
oriented refinements are left for future work.                                      (no sampling), it generated 215 bug reports, of which 78
   3) False Positive Analysis: We analyze the 15 false posi-                        were true positives (36.3% precision), uncovering 37 unique
tives reported by RFCAUDIT to understand their root causes.                         bugs (29 new, 8 old). Claude 3.5 Sonnet achieved 19.9%
Based on this analysis, we classify them into four categories:                      precision over 538 inconsistencies and found 26 bugs. GPT-4o
(i) incomplete context retrieval (3 cases), where necessary                         returned the most bug reports (1,315) but the lowest precision
                                 TABLE IV: Baseline comparison across three model configurations.
                     Copilot + Claude 3.7 Sonnet           Copilot + Claude 3.5 Sonnet (With Sample)               Copilot + GPT-4o (With Sample)
 Protocols
             #Incons.   #TP    Precision   #New    #Old   #Incons.   #Sample   Precision   #New    #Old    #Incons.   #Sample    Precision   #New        #Old
 Babel         76        16     21.1%       7       3       173        32       12.5%       3          1     493         32       3.1%        1           0
 BFD           45        37     82.2%       5       5       115        60       23.3%       7          4     244         60       20.0%       6           3
 NHRP          27        10     37.0%       9       0        89        24       20.8%       4          0     204         24       16.7%       4           0
 RIPng          6         1     16.7%       1       0        45         6       16.7%       1          0     84          6        0.0%        0           0
 DHCP          32        9      28.1%       4       0        64        24       25.0%       4          0     188         24       42.0%       1           0
 IGMP          29        5      17.2%       3       0        52        20       15.0%       2          0     102         20       5.0%        1           0
 Total         215       78     36.3%       29      8       538        166      19.9%       21         5    1315        166       11.4%       13          3

   TABLE V: Token usage (In: input tokens, Out: output tokens), financial cost, and execution time per protocol.
                Phase 1: Code Semantic Indexing                Phase 2: Retrieval-guided Detection                              Total
 Protocol
             Tokens (In/Out)  Cost ($)  Time (min)           Tokens (In/Out)   Cost ($)   Time (min)        Tokens (In/Out)      Cost ($)    Time (min)
 Babel         261K / 71K           1.85           44          1340K / 41K        4.63            39         1061K / 112K         6.48              83
 BFD           449K / 119K          3.13           71          1086K / 30K        3.71            52         1535K / 149K         6.84             123
 NHRP          319K / 81K           2.17           49           960K / 25K        3.26            56         1279K / 106K         5.43             105
 RIPng         197K / 52K           1.37           31           429K / 9K         1.42            23          626K / 61K          2.79             54
 DHCP           248K /44K           1.40           28          1353K / 24K        4.42            47         1601K / 68K          5.82             75
 IGMP          248K / 28K           1.40           28           390K / 16K        1.41            20          638K / 44K          2.81             48
 Average        287K / 66K          1.89           42          926K / 24K         3.14            39          1123K / 90K         5.03             81


(11.4%) and the fewest bugs (16). Overall, all three baselines                 reported separately for Phase 1 (Code Semantic Indexing) and
suffer from low precision and high validation overhead. In                     Phase 2 (Retrieval-guided Detection). Although Claude 3.5
contrast, RFCAUDIT achieves 81.9% precision and discovers                      is used for both phases in our evaluation, Phase 1 primarily
47 bugs in total (40 new) with far less manual effort (Table                   involves lightweight summarization. Since it does not require
II). RFCAUDIT consistently reports the lowest false-positive                   complex reasoning, it could be replaced by smaller or less
rates and the highest bug counts across all protocols. Notably,                expensive LLMs with minimal impact on performance.
RFCAUDIT ’s use of Claude 3.5 (a non-reasoning model) still                       Results. As shown in Table V, RFCAUDIT uses an average
outperforms Claude 3.7 (a reasoning model).                                    of 1123K input and 90K output tokens, costs $5.03, and
   2) Comparison with LTL-Fuzzer: We compare RFCAUDIT                          completes each protocol analysis in 81 minutes. Since the
with LTL-Fuzzer [4], which checks protocol implementations                     analysis has a complete summarization of the whole code base
against LTL properties via instrumentation and fuzzing. Set-                   and compares code against the full RFC, input token usage and
ting up LTL-Fuzzer requires substantial manual efforts: trans-                 cost largely depend on the code base size and RFC length.
lating informal specifications into LTL formulas and mapping                   Overall, RFCAUDIT is efficient for functional bug detection.
each atomic predicate to code locations. Consequently, it
                                                                               E. RQ4: Ablation Studies
mainly captures event-ordering temporal properties but cannot
naturally express data-format checks, arithmetic constraints,                     Ablation Study 1: Without Code Semantic Indexing. To
or timing requirements. We applied RFCAUDIT to the 15                          evaluate the impact of code semantic indexing, we disable
zero-day bugs reported in LTL-Fuzzer’s evaluation and also                     semantic summarization in Phase 1. The agent still follows the
examined whether the 47 violated properties from our dataset                   directory structure and explores the codebase hierarchically but
could be encoded for LTL-Fuzzer properties.                                    no longer uses LLM-generated summaries. Instead, it relies
   Results. RFCAUDIT successfully detected 12 of the 15                        solely on directory and file names plus function signatures.
zero-days originally reported by LTL-Fuzzer, without requir-                   This setup follows the same design of AGENTLESS [32] and
ing manual property construction or predicate-to-location map-                 LocAgent [31], which uses code structures without semantic
ping. These included 7 in TinyDTLS and 5 in Contiki-Telnet.                    summaries. As shown in Table VI, removing semantic index-
In contrast, when we attempted to encode the 47 violated                       ing drops precision from 81.9% to 51.4% and reduces detected
properties from our dataset as LTL-Fuzzer properties, only                     bugs from 47 to 26. To explain this drop, we analyze each
11 could be expressed; the remaining 36 required constraints                   false positive and classify its root cause according to the four
beyond plain LTL or lacked precise predicate locations. These                  categories in Section IV-B3. We observe that false positives
results indicate that RFCAUDIT is effective in automatically                   due to (i) incomplete context retrieval rise significantly (from
detecting temporal property violations while extending to a                    3 to 14), making it the main source of false positives in
broader range of functional inconsistencies.                                   this setting. Without semantic summaries, the agent confuses
                                                                               similarly named helper functions across modules—for ex-
D. RQ3: Efficiency of RFCAUDIT                                                 ample, retrieving parse_update_subtlv instead of the
  Setup and Metrics. To quantify the efficiency of RFCAU -                     correct parse_packet when validating Babel update TLVs.
DIT, we measure input/output token usage, financial cost, and                  This highlights the importance of semantic summarization for
execution time for analyzing each repository. The results are                  accurate context retrieval and reduced false positives.
                      TABLE VI: Ablation Studies.                                           void handle_request(struct neighbour *neigh, const unsigned char
                                                                                            *prefix, unsigned char plen, unsigned char hop_count, ..) {
               Ablation Study 1          Ablation Study 2             Ablation Study 3         ..
 Protocol
             Precision #New #Old     Precision #New #Old           Precision #New #Old         if (hop_count <= 1) return;
 Babel        52.6%     5     3          48.0%    9        3         35.2%     11    3      - other_route = find_best_route(prefix, plen, 0, neigh);
 BFD          68.8%     8     5          70.6%    5        5         67.9%     10    5      + other_route = find_best_route(prefix, plen, 1, neigh);
 NHRP         20.0%     2     0          45.0%    6        2         20.4%      7    0      + if (!other_route || route_metric(other_route) >= INFINITY) {
 RIPng         NA       0     0          25.0%    1        0          5.9%      1    0      +      /* If no feasible route found, try non-feasible routes */
 DHCP          0%       0     0          50.0%    3        0         30.0%      4    0
                                                                                            +      other_route = find_best_route(prefix, plen, 0, neigh);
 IGMP         57.1%     3     0          18.2%    2        0         29.6%      4    0
                                                                                               }
 Total        51.4%     18    8       47.1%       26       10        36.1%     37    8
                                                                                                          (a) Bug #1: Incorrect Request Forwarding
TABLE VII: Impact of Removing Single Retrieval Tool.                                        static void nhrp_peer_forward(struct nhrp_peer *p,
                                                                                                                           struct nhrp_packet_parser *pp){
         w/o Query                w/o Query_Callee                w/o Query_Caller             type = htons(ext->type) & ~NHRP_EXTENSION_FLAG_COMPULSORY;
 Precision   #New     #Old   Precision     #New    #Old         Precision    #New   #Old       switch (type) {
  50.0%        31      10     47.7%         37         8         47.3%        31     8         case NHRP_EXTENSION_RESPONDER_ADDRESS:
                                                                                            +   if (hdr->type == NHRP_PACKET_RESOLUTION_REPLY) {
                                                                                            +     cie = nhrp_cie_pull(.., &cie_protocol);
   Ablation Study 2: Detection Without Retrieval. To eval-                                  +     if(cie && sockunion_same(&cie_protocol, &pp->if_ad->addr)){
uate the impact of the Retrieval stage, we disable all code                                 +        nhrp_packet_send_error(pp, NHRP_ERROR_LOOP_DETECTED, 0);
                                                                                            +        goto err;
retrieval tools (Query, Query_Callee, Query_Caller).                                        +     }
The detection agent must make decisions using only the ini-                                 +   }
tially retrieved function(s), without fetching additional context.                               ..

As shown in Table VI, this results in a sharp drop in precision                                (b) Bug #35: Miss Loop Detection for Responder Address Extension
(from 81.9% to 47.1%) and fewer detected bugs (from 47 to                                                        Fig. 9: Case Studies.
36). This shows that retrieval is important for reducing false
                                                                                           G. Threats to Validity.
positives and improving detection quality. To assess the impact
of each retrieval tool, we disable each tool individually. As                                 Several threats may affect the validity of our findings. First,
shown in Table VII, removing any single tool sharply reduces                               we adopt Claude 3.5 Sonnet as our language model with a
precision from 81.9% with full retrieval to about 47–50%,                                  temperature setting of 0.0 for stable analysis results, thereby
with little difference across tools. However, the number of                                enhancing the reproducibility of RFCAUDIT. Nevertheless,
detected bugs varies, with the largest drop occurring when                                 alternative models or configurations may yield variations in
Query_Caller is removed (from 47 to 39), suggesting it                                     performance [40]–[42]. So we ran controlled experiments
contributes the most to overall bug coverage.                                              using two additional general-purpose API models: GPT-4o and
   Ablation Study 3: Detection Without Self-critics. To eval-                              DeepSeek-V3, to analyze the BFD protocol in FRRouting,
uate the impact of self-critics, we disable it during detection.                           where RFCAUDIT discovered the most bugs. RFCAUDIT
This leads to a higher false positive rate (18.1% to 63.9%)                                detected 11 and 13 true bugs with the precision of 71.4% and
and fewer bugs (47 to 45), emphasizing its crucial role in                                 70.3%, respectively, demonstrating the effectiveness across
enhancing detection precision and finding overlooked bugs.                                 models. Second, our manual classification of true positives
                                                                                           and false positives may introduce subjective bias. To mitigate
F. Case Studies                                                                            this risk, two authors independently reviewed each reported
   We present two representative case studies:                                             functional bug and resolved any disagreements through discus-
   Bug #1: Incorrect request forwarding. RFC 8966 specifies                                sion [41], [43]. We further validated our results by reporting
an ordered forwarding rule: when hop count is 2 or more,                                   newly discovered bugs to protocol developers, where all bug
a node must first attempt to forward via a feasible route                                  reports that received a response have been confirmed as true
(excluding the requester); only if no such route exists should                             positives. Third, our method relies on high-quality and well-
it fall back to a non-feasible one. As shown in Figure 9(a),                               structured documentation such as RFCs. Ambiguous or poorly
FRRouting ignored this ordering and always chose a non-                                    maintained documentation might hinder semantic understand-
feasible route. This misbehavior could cause forwarding loops                              ing, potentially threatening the effectiveness of our technique.
or prevent requests from reaching valid next hops, under-
mining routing convergence. We submitted a fix to prioritize                               H. Evaluation on Industry-Scale Protocol Stacks
feasible routes, which has been merged by the developers.                                     We further applied RFCAUDIT to two large protocol stacks:
   Bug #35: Miss loop detection. RFC 2332 specifies that if                                aws-c-http, a 74K LoC HTTP library in the AWS Common
an NHS forwards an NHRP Resolution Reply that lists its own                                Runtime, and the Linux TCP/IP stack, about 190K LoC in
protocol address in the Responder Address Extension, it must                               the kernel implementing core transport and network protocols.
discard the packet and generate an NHRP Error Indication of                                We evaluated aws-c-http against RFC 7230 (HTTP/1.1), and
type “Loop Detected”. As shown in Figure 9(b), FRRouting                                   Linux against RFC 793 (TCP), RFC 768 (UDP), and RFC 791
omitted this check, allowing persistent forwarding loops that                              (IP). On aws-c-http, RFCAUDIT detected 18 inconsistencies,
consume resources and delay address resolution. The bug was                                of which 12 were confirmed as true positives, yielding 12
confirmed by the developers.                                                               unique bugs. On the Linux TCP/IP stack, it flagged 3 incon-
sistencies, with 1 true positive. These results demonstrate that   of the protocol implementation, facilitating the functional bug
RFCAUDIT scales to industry-scale codebases and can expose         detection with high precision and efficiency.
real specification violations with high precision.
                                                                   B. LLM-aided Static Bug Detection
            V. D ISCUSSION AND F UTURE W ORK
                                                                      LLM-aided static bug detection has advanced rapidly [48]–
   While our current evaluation targets network protocols,         [54], typically following two directions. One uses LLMs to
RFCAudit is not limited to this domain. The key requirement is     supply domain knowledge like function specifications [48]–
the availability of specification documents that define expected   [50] and bug definitions [51], to assist symbolic approaches
functionality and constraints. In domains such as system li-       in analyzing the program for bug detection. For example, IRIS
braries, cloud APIs, or security-critical frameworks, specifica-   leverages LLM-inferred sources and sinks to detect taint-style
tions are often available as API references, design guidelines,    vulnerabilities [50], while KNighter synthesizes static analyz-
or standards documents. RFCAUDIT can be adapted to align           ers from bug patches for kernel bug detection [51]. The other
such specifications with code and flag inconsistencies as poten-   direction adopts agent-centric solutions that reason over source
tial bugs. We choose network protocols for evaluation because      code directly without compilation [52]–[54]. Techniques such
RFCs are detailed and publicly accessible, but extending           as LLMSAN [52] and LLMDFA [53] combine LLMs with
RFCAudit to other domains is a promising next step to further      SMT solvers and parsing-based analyzers, while LLift uses
demonstrate its generality and effectiveness.                      progressive prompting to find kernel vulnerabilities [54]. More
                    VI. R ELATED W ORK                             recently, RepoAudit extends these efforts to detect multiple
                                                                   types of data-flow bugs [55]. In contrast, our work targets
A. Bug Detection in Network Protocol Implementation
                                                                   functional bugs, where bug specifications often lack clear
   The correctness of network protocol implementations is          formalization. The diverse nature of functional properties also
critical for ensuring secure and reliable digital communication.   prevents the application of standard static analysis frameworks.
Existing bug detection techniques for protocol implemen-           Nonetheless, our retrieval-based approach draws inspiration
tations can be broadly categorized into three approaches.          from traditional bug detection methodologies, enabling local-
First, fuzzing-based techniques—such as BooFuzz [44] and           izing code segments relevant to targeted functional properties,
SAGE [45]—primarily identify bugs by triggering crashes            facilitating effective subsequent detection.
during execution. Netlifter [26] and ChatAFL [15] improve
fuzzing coverage by using static analysis or LLMs to infer                              VII. C ONCLUSION
packet formats and generate valid inputs, but still rely on
crashes, overlooking subtle semantic issues. LLMIF [46] and           This paper presents RFCAUDIT, an LLM agent designed
mGPTFuzz [16] extract formats or FSMs from specifications          for detecting functional bugs in network protocol implemen-
using LLMs to uncover semantic bugs, but focus narrowly            tations by identifying semantic inconsistencies between the
on state transition or input validation violations and are         code and RFC documents. Specifically, RFCAUDIT comprises
limited to specific IoT devices, hard to generalize to broader     two complementary agents: an indexing agent responsible
protocol testing. LTL-Fuzzer [4] uses LTL formulas to guide        for semantic indexing of source code, and a detection agent
fuzzing and detect event-ordering violations, but demands          performing retrieval-guided inconsistency detection. In our
significant manual effort for formula crafting and predicate-      evaluation, RFCAUDIT successfully uncovered 47 functional
to-code mapping, and is limited to temporal property viola-        bugs across six different protocols, of which 20 have been
tions. Second, differential analysis techniques [18]–[20] detect   acknowledged or fixed by the original developers. As the first
bugs by comparing the behaviors of multiple independent            LLM-based approach explicitly targeting functional bug detec-
implementations of the same protocol. These approaches can         tion in network protocols, our work offers valuable insights
uncover semantic discrepancies that fuzzing may miss. How-         into future research on functional bug detection in domain-
ever, they are inherently limited to scenarios where multiple      specific software systems, demonstrating the significant poten-
protocol implementations are available for comparison. Third,      tial of leveraging LLM capabilities in security auditing tasks.
formal verification-based techniques rigorously check protocol
                                                                                       ACKNOWLEDGMENT
implementations against formally specified properties. While
powerful in reasoning about semantic correctness, they require        We thank all the anonymous reviewers for the insightful
substantial manual effort to construct, maintain, and validate     and constructive feedback. We are grateful to the Center for
formal models, posing significant barriers to practical de-        AI Safety for providing computational resources. This work
ployment. Beyond the three categories, EBugDec [47] targets        was funded in part by the National Science Foundation (NSF)
inconsistencies between RFC evolution and protocol imple-          Awards SHF-1901242, SHF-1910300, Proto-OKN 2333736,
mentations. However, its scope is limited to RFC-evolutionary      IIS-2416835, DARPA VSPELLS - HR001120S0058, ONR
bugs, primarily focusing on packet parsing issues. In contrast     N00014-23-1-2081, and Amazon. Any opinions, findings and
to these prior efforts, our proposed technique, RFCAUDIT,          conclusions or recommendations expressed in this material are
addresses functional correctness by bridging the informal          those of the authors and do not necessarily reflect the views
specifications in RFC documents with the program semantics         of the sponsors.
                               R EFERENCES                                               matter iot devices,” in 33rd USENIX Security Symposium, USENIX
                                                                                         Security 2024, Philadelphia, PA, USA, August 14-16, 2024, D. Balzarotti
 [1] MITRE, “Cve-2020-1472,” https://nvd.nist.gov/vuln/detail/CVE-2020-                  and W. Xu, Eds. USENIX Association, 2024. [Online]. Available: https:
     1472, 2020.                                                                         //www.usenix.org/conference/usenixsecurity24/presentation/ma-xiaoyue
 [2] Microsoft, “Netlogon remote protocol,” https://learn.microsoft.com/en-         [17] X. Liu, W. You, Y. Ye, Z. Zhang, J. Huang, and X. Zhang, “Fuzzinmem:
     us/openspecs/windows protocols/ms-nrpc/ff8f970f-3e37-40f7-bd4b-                     Fuzzing programs via in-memory structures,” in Proceedings of the
     af7336e4792f, 2024.                                                                 IEEE/ACM 46th International Conference on Software Engineering, ser.
 [3] A. A. de Amorim, C. Hritcu, and B. C. Pierce, “The meaning of                       ICSE ’24. New York, NY, USA: Association for Computing Machinery,
     memory safety,” CoRR, vol. abs/1705.07354, 2017. [Online]. Available:               2024. [Online]. Available: https://doi.org/10.1145/3597503.3639172
     http://arxiv.org/abs/1705.07354                                                [18] M. Zheng, Q. Shi, X. Liu, X. Xu, L. Yu, C. Liu, G. Wei, and X. Zhang,
 [4] R. Meng, Z. Dong, J. Li, I. Beschastnikh, and A. Roychoudhury, “Linear-             “Pardiff: Practical static differential analysis of network protocol
     time temporal logic guided greybox fuzzing,” in 44th IEEE/ACM                       parsers,” Proc. ACM Program. Lang., vol. 8, no. OOPSLA1, pp.
     44th International Conference on Software Engineering, ICSE 2022,                   1208–1234, 2024. [Online]. Available: https://doi.org/10.1145/3649854
     Pittsburgh, PA, USA, May 25-27, 2022. ACM, 2022, pp. 1343–1355.                [19] R. Rutledge and A. Orso, “Automating differential testing with
     [Online]. Available: https://doi.org/10.1145/3510003.3510082                        overapproximate symbolic execution,” in 15th IEEE Conference on
 [5] S. Feng, Y. Ye, Q. Shi, Z. Cheng, X. Xu, S. Cheng, H. Choi,                         Software Testing, Verification and Validation, ICST 2022, Valencia,
     and X. Zhang, “ROCAS: root cause analysis of autonomous driving                     Spain, April 4-14, 2022. IEEE, 2022, pp. 256–266. [Online]. Available:
     accidents via cyber-physical co-mutation,” in Proceedings of the                    https://doi.org/10.1109/ICST53961.2022.00035
     39th IEEE/ACM International Conference on Automated Software                   [20] G. S. Reen and C. Rossow, “Dpifuzz: A differential fuzzing framework
     Engineering, ASE 2024, Sacramento, CA, USA, October 27 - November                   to detect DPI elusion strategies for QUIC,” in ACSAC ’20: Annual
     1, 2024, V. Filkov, B. Ray, and M. Zhou, Eds. ACM, 2024, pp. 1620–                  Computer Security Applications Conference, Virtual Event / Austin,
     1632. [Online]. Available: https://doi.org/10.1145/3691620.3695530                  TX, USA, 7-11 December, 2020. ACM, 2020, pp. 332–344. [Online].
 [6] S. Feng, X. Xu, X. Chen, K. Zhang, S. Y. Ahmed, Z. Su, M. Zheng,                    Available: https://doi.org/10.1145/3427228.3427662
     and X. Zhang, “Intentest: Stress testing for intent integrity in api-calling   [21] O. Udrea and C. Lumezanu, “Rule-based static analysis of network
     LLM agents,” CoRR, vol. abs/2506.07524, 2025. [Online]. Available:                  protocol implementations,” in Proceedings of the 15th USENIX
     https://doi.org/10.48550/arXiv.2506.07524                                           Security Symposium, Vancouver, BC, Canada, July 31 - August
 [7] S. Kate, Y. Gao, S. Feng, and X. Zhang, “Roscallbax: Statically                     4, 2006, A. D. Keromytis, Ed. USENIX Association, 2006.
     detecting inconsistencies in callback function setup of robotic systems,”           [Online]. Available: https://www.usenix.org/conference/15th-usenix-
     Proc. ACM Softw. Eng., vol. 2, no. FSE, pp. 668–689, 2025. [Online].                security-symposium/rule-based-static-analysis-network-protocol
     Available: https://doi.org/10.1145/3715748                                     [22] M. Musuvathi and D. R. Engler, “Model checking large network
 [8] C. Cadar, D. Dunbar, and D. R. Engler, “Klee: Unassisted                            protocol implementations,” in 1st Symposium on Networked Systems
     and automatic generation of high-coverage tests for complex                         Design and Implementation (NSDI 2004), March 29-31, 2004, San
     systems programs,” in Proceedings of the 8th USENIX                                 Francisco, California, USA, Proceedings, R. Morris and S. Savage,
     Symposium on Operating Systems Design and Implementation,                           Eds. USENIX, 2004, pp. 155–168. [Online]. Available: http:
     ser. OSDI ’08.           USENIX, 2008, pp. 209–224. [Online].                       //www.usenix.org/events/nsdi04/tech/musuvathi.html
     Available: https://www.usenix.org/conference/osdi-08/klee-unassisted-          [23] “The artifact of RFCAudit,” https://github.com/zmw12306/RFCAudit,
     and-automatic-generation-high-coverage-tests-complex-systems                        2025.
 [9] S. Poeplau and A. Francillon, “Symbolic execution with SymCC:                  [24] C. Liu, S. Gong, and P. Fonseca, “KIT: testing os-level virtualization
     Don’t interpret, compile!” in 29th USENIX Security Symposium                        for functional interference bugs,” in Proceedings of the 28th ACM
     (USENIX Security 20). USENIX Association, Aug. 2020, pp.                            International Conference on Architectural Support for Programming
     181–198. [Online]. Available: https://www.usenix.org/conference/                    Languages and Operating Systems, Volume 2, ASPLOS 2023, Vancouver,
     usenixsecurity20/presentation/poeplau                                               BC, Canada, March 25-29, 2023, T. M. Aamodt, N. D. E. Jerger, and
[10] I. Yun, S. Lee, M. Xu, Y. Jang, and T. Kim, “QSYM : A                               M. M. Swift, Eds. ACM, 2023, pp. 427–441. [Online]. Available:
     practical concolic execution engine tailored for hybrid fuzzing,” in 27th           https://doi.org/10.1145/3575693.3575731
     USENIX Security Symposium (USENIX Security 18). Baltimore, MD:                 [25] V. Pham, M. Böhme, and A. Roychoudhury, “AFLNET: A greybox
     USENIX Association, Aug. 2018, pp. 745–761. [Online]. Available:                    fuzzer for network protocols,” in 13th IEEE International Conference
     https://www.usenix.org/conference/usenixsecurity18/presentation/yun                 on Software Testing, Validation and Verification, ICST 2020, Porto,
[11] J. Jiang, M. Zheng, Q. Shi, and X. Z. Zhang, “SFA-Miner: Mining path-               Portugal, October 24-28, 2020. IEEE, 2020, pp. 460–465. [Online].
     sensitive api usage patterns via symbolic finite automata,” in The IEEE             Available: https://doi.org/10.1109/ICST46399.2020.00062
     Symposium on Security and Privacy, ser. S&P 2026, 2026.                        [26] Q. Shi, J. Shao, Y. Ye, M. Zheng, and X. Zhang, “Lifting network
[12] X. Liu, W. You, Z. Zhang, and X. Zhang, “Tensilefuzz: facilitating                  protocol implementation to precise format specification with security
     seed input generation in fuzzing via string constraint solving,” in                 applications,” in Proceedings of the 2023 ACM SIGSAC Conference
     Proceedings of the 31st ACM SIGSOFT International Symposium on                      on Computer and Communications Security, CCS 2023, Copenhagen,
     Software Testing and Analysis, ser. ISSTA 2022. New York, NY, USA:                  Denmark, November 26-30, 2023, W. Meng, C. D. Jensen, C. Cremers,
     Association for Computing Machinery, 2022, p. 391–403. [Online].                    and E. Kirda, Eds. ACM, 2023, pp. 1287–1301. [Online]. Available:
     Available: https://doi.org/10.1145/3533767.3534403                                  https://doi.org/10.1145/3576915.3616614
[13] P. Yao, J. Zhou, X. Xiao, Q. Shi, R. Wu, and C. Zhang, “Falcon:                [27] Q. Shi, X. Xiao, R. Wu, J. Zhou, G. Fan, and C. Zhang, “Pinpoint:
     A fused approach to path-sensitive sparse data dependence analysis,”                fast and precise sparse value flow analysis for million lines of
     Proc. ACM Program. Lang., vol. 8, no. PLDI, Jun. 2024. [Online].                    code,” in Proceedings of the 39th ACM SIGPLAN Conference on
     Available: https://doi.org/10.1145/3656400                                          Programming Language Design and Implementation, PLDI 2018,
[14] H. Yan, Y. Sui, S. Chen, and J. Xue, “Spatio-temporal context reduction:            Philadelphia, PA, USA, June 18-22, 2018, J. S. Foster and
     a pointer-analysis-based static approach for detecting use-after-free               D. Grossman, Eds. ACM, 2018, pp. 693–706. [Online]. Available:
     vulnerabilities,” in Proceedings of the 40th International Conference               https://doi.org/10.1145/3192366.3192418
     on Software Engineering, ser. ICSE ’18. New York, NY, USA:                     [28] Y. Sui and J. Xue, “SVF: interprocedural static value-flow analysis
     Association for Computing Machinery, 2018, p. 327–337. [Online].                    in LLVM,” in Proceedings of the 25th International Conference on
     Available: https://doi.org/10.1145/3180155.3180178                                  Compiler Construction, CC 2016, Barcelona, Spain, March 12-18,
[15] R. Meng, M. Mirchev, M. Böhme, and A. Roychoudhury, “Large                         2016, A. Zaks and M. V. Hermenegildo, Eds. ACM, 2016, pp.
     language model guided protocol fuzzing,” in 31st Annual Network                     265–266. [Online]. Available: https://doi.org/10.1145/2892208.2892235
     and Distributed System Security Symposium, NDSS 2024, San Diego,               [29] G. Dı́az, F. Cuartero, V. V. Ruiz, and F. L. Pelayo, “Automatic
     California, USA, February 26 - March 1, 2024. The Internet                          verification of the TLS handshake protocol,” in Proceedings of the
     Society, 2024. [Online]. Available: https://www.ndss-symposium.org/                 2004 ACM Symposium on Applied Computing (SAC), Nicosia, Cyprus,
     ndss-paper/large-language-model-guided-protocol-fuzzing/                            March 14-17, 2004, H. Haddad, A. Omicini, R. L. Wainwright, and
[16] X. Ma, L. Luo, and Q. Zeng, “From one thousand pages of specification               L. M. Liebrock, Eds. ACM, 2004, pp. 789–794. [Online]. Available:
     to unveiling hidden bugs: Large language model assisted fuzzing of                  https://doi.org/10.1145/967900.968063
[30] M. Zheng, D. Xie, Q. Shi, C. Wang, and X. Zhang, “Validating network            optimization,” Proc. ACM Softw. Eng., vol. 1, no. FSE, pp. 2469–2492,
     protocol parsers with traceable RFC document interpretation,” Proc.             2024. [Online]. Available: https://doi.org/10.1145/3660816
     ACM Softw. Eng., vol. 2, no. ISSTA, pp. 1772–1794, 2025. [Online].         [49] C. Ye, Y. Cai, and C. Zhang, “When threads meet interrupts:
     Available: https://doi.org/10.1145/3728955                                      Effective static detection of interrupt-based deadlocks in linux,”
[31] Z. Chen, R. Tang, G. Deng, F. Wu, J. Wu, Z. Jiang, V. K. Prasanna,              in 33rd USENIX Security Symposium, USENIX Security 2024,
     A. Cohan, and X. Wang, “Locagent: Graph-guided LLM agents for                   Philadelphia, PA, USA, August 14-16, 2024, D. Balzarotti and
     code localization,” in Proceedings of the 63rd Annual Meeting of the            W. Xu, Eds. USENIX Association, 2024. [Online]. Available:
     Association for Computational Linguistics (Volume 1: Long Papers),              https://www.usenix.org/conference/usenixsecurity24/presentation/ye
     ACL 2025, Vienna, Austria, July 27 - August 1, 2025, W. Che,               [50] Z. Li, S. Dutta, and M. Naik, “Llm-assisted static analysis for detecting
     J. Nabende, E. Shutova, and M. T. Pilehvar, Eds. Association for                security vulnerabilities,” CoRR, vol. abs/2405.17238, 2024. [Online].
     Computational Linguistics, 2025, pp. 8697–8727. [Online]. Available:            Available: https://doi.org/10.48550/arXiv.2405.17238
     https://aclanthology.org/2025.acl-long.426/                                [51] C. Yang, Z. Zhao, Z. Xie, H. Li, and L. Zhang, “Knighter:
[32] C. S. Xia, Y. Deng, S. Dunn, and L. Zhang, “Demystifying llm-based              Transforming static analysis with llm-synthesized checkers,” CoRR, vol.
     software engineering agents,” Proc. ACM Softw. Eng., vol. 2, no. FSE,           abs/2503.09002, 2025. [Online]. Available: https://doi.org/10.48550/
     pp. 801–824, 2025. [Online]. Available: https://doi.org/10.1145/3715754         arXiv.2503.09002
[33] Z. Lin, Z. Gou, T. Liang, R. Luo, H. Liu, and Y. Yang, “CriticBench:       [52] C. Wang, W. Zhang, Z. Su, X. Xu, and X. Zhang, “Sanitizing large
     Benchmarking LLMs for critique-correct reasoning,” in Findings of               language models in bug detection with data-flow,” in Findings of
     the Association for Computational Linguistics: ACL 2024, L.-W. Ku,              the Association for Computational Linguistics: EMNLP 2024, Miami,
     A. Martins, and V. Srikumar, Eds. Bangkok, Thailand: Association                Florida, USA, November 12-16, 2024, Y. Al-Onaizan, M. Bansal, and
     for Computational Linguistics, Aug. 2024, pp. 1552–1587. [Online].              Y. Chen, Eds. Association for Computational Linguistics, 2024, pp.
     Available: https://aclanthology.org/2024.findings-acl.91/                       3790–3805. [Online]. Available: https://aclanthology.org/2024.findings-
[34] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang,                     emnlp.217
     X. Zhang, S. Zhang, J. Liu, A. H. Awadallah, R. W. White,                  [53] C. Wang, W. Zhang, Z. Su, X. Xu, X. Xie, and X. Zhang, “LLMDFA:
     D. Burger, and C. Wang, “Autogen: Enabling next-gen LLM                         analyzing dataflow in code with large language models,” in Advances
     applications via multi-agent conversation,” in ICLR 2024 Workshop               in Neural Information Processing Systems 38: Annual Conference on
     on Large Language Model (LLM) Agents, 2024. [Online]. Available:                Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver,
     https://openreview.net/forum?id=uAjxFFing2                                      BC, Canada, December 10 - 15, 2024, A. Globersons, L. Mackey,
[35] Anthropic, “Claude 3.5 sonnet,” https://www.anthropic.com/claude/               D. Belgrave, A. Fan, U. Paquet, J. M. Tomczak, and C. Zhang, Eds.,
     sonnet, 2025.                                                                   2024. [Online]. Available: http://papers.nips.cc/paper files/paper/2024/
[36] “Tree-sitter,” https://tree-sitter.github.io/tree-sitter/.                      hash/ed9dcde1eb9c597f68c1d375bbecf3fc-Abstract-Conference.html
[37] F. community, “The frrouting protocol suite,” https://github.com/          [54] H. Li, Y. Hao, Y. Zhai, and Z. Qian, “Enhancing static analysis
     FRRouting/frr, 2024.                                                            for practical bug detection: An llm-integrated approach,” Proc. ACM
[38] “lwip - a lightweight tcp/ip stack,” https://github.com/lwip-tcpip/lwip,        Program. Lang., vol. 8, no. OOPSLA1, Apr. 2024. [Online]. Available:
     2025.                                                                           https://doi.org/10.1145/3649828
[39] M. Zheng, D. Xie, and X. Zhang, “Large language models for validating      [55] J. Guo, C. Wang, X. Xu, Z. Su, and X. Zhang, “Repoaudit: An
     network protocol parsers,” in 2025 IEEE Security and Privacy, SP 2025           autonomous llm-agent for repository-level code auditing,” CoRR, vol.
     - Workshops, San Francisco, CA, USA, May 15, 2025, M. Blanton,                  abs/2501.18160, 2025. [Online]. Available: https://doi.org/10.48550/
     W. Enck, and C. Nita-Rotaru, Eds. IEEE, 2025, pp. 56–64. [Online].              arXiv.2501.18160
     Available: https://doi.org/10.1109/SPW67851.2025.00009
[40] X. Deng, J. Da, E. Pan, Y. Y. He, C. Ide, K. Garg, N. Lauffer, A. Park,
     N. Pasari, C. Rane et al., “Swe-bench pro: Can ai agents solve long-
     horizon software engineering tasks?” arXiv preprint arXiv:2509.16941,
     2025. [Online]. Available: https://arxiv.org/abs/2509.16941
[41] D. Xie, B. Yoo, N. Jiang, M. Kim, L. Tan, X. Zhang, and
     J. S. Lee, “Impact of large language models on generating software
     specifications,” CoRR, vol. abs/2306.03324, 2023. [Online]. Available:
     https://doi.org/10.48550/arXiv.2306.03324
[42] D. Xie, M. Zheng, X. Liu, J. Wang, C. Wang, L. Tan, and X. Zhang,
     “Core: Benchmarking LLMs’ code reasoning capabilities through static
     analysis tasks,” in The Thirty-ninth Annual Conference on Neural
     Information Processing Systems Datasets and Benchmarks Track, 2025.
     [Online]. Available: https://openreview.net/forum?id=WJIDorHiuZ
[43] M. Zheng, J. Yang, M. Wen, H. Zhu, Y. Liu, and H. Jin,
     “Why do developers remove lambda expressions in java?” in
     36th IEEE/ACM International Conference on Automated Software
     Engineering, ASE 2021, Melbourne, Australia, November 15-19, 2021.
     IEEE, 2021, pp. 67–78. [Online]. Available: https://doi.org/10.1109/
     ASE51524.2021.9678600
[44] J. Pereyda, “Boofuzz,” https://github.com/jtpereyda/boofuzz, 2023.
[45] P. Godefroid, M. Y. Levin, and D. A. Molnar, “SAGE: whitebox
     fuzzing for security testing,” Commun. ACM, vol. 55, no. 3, pp. 40–44,
     2012. [Online]. Available: https://doi.org/10.1145/2093548.2093564
[46] J. Wang, L. Yu, and X. Luo, “LLMIF: augmented large language model
     for fuzzing iot devices,” in IEEE Symposium on Security and Privacy, SP
     2024, San Francisco, CA, USA, May 19-23, 2024. IEEE, 2024, pp. 881–
     896. [Online]. Available: https://doi.org/10.1109/SP54263.2024.00211
[47] J. Chen, F. Li, Q. Chen, P. Li, L. Xu, and W. Huo, “Ebugdec:
     Detecting inconsistency bugs caused by RFC evolution in protocol
     implementations,” in Proceedings of the 26th International Symposium
     on Research in Attacks, Intrusions and Defenses, RAID 2023, Hong
     Kong, China, October 16-18, 2023. ACM, 2023, pp. 412–425.
     [Online]. Available: https://doi.org/10.1145/3607199.3607222
[48] C. Wang, J. Zhang, R. Wu, and C. Zhang, “Dainfer: Inferring API
     aliasing specifications from library documentation via neurosymbolic
