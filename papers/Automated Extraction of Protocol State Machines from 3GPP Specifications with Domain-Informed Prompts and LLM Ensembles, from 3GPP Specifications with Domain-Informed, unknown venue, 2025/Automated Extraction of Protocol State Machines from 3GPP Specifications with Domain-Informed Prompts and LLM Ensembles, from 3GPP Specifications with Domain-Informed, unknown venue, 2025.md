                                            Automated Extraction of Protocol State Machines
                                            from 3GPP Specifications with Domain-Informed
                                                    Prompts and LLM Ensembles
                                                       Miao Zhang1 , Runhan Feng2 , Hongbo Tang1 , Yu Zhao1 , Jie Yang1 , Hang Qiu1 , Qi Liu2
                                                                                     1
                                                                               Information Engineering University, China
                                                                                 2
                                                                                   Purple Mountain Laboratories, China
                                                       Email: 1152461073@qq.com, fengrunhan@pmlabs.com.cn, tahobo@sina.com, itsyz@foxmail.com
                                                                     yj csu@126.com, qiuhang ndsc@163.com, liuqi@pmlabs.com.cn
arXiv:2510.14348v1 [cs.NI] 16 Oct 2025




                                            Abstract—Mobile telecommunication networks are founda-            of protocol designs [3]–[7], while software testing techniques
                                         tional to global infrastructure and increasingly support critical    such as fuzz testing are applied to uncover vulnerabilities in
                                         sectors such as manufacturing, transportation, and healthcare.       protocol implementations [8]–[13]. The vast majority of these
                                         The security and reliability of these networks are essential, yet
                                         depend heavily on accurate modeling of underlying protocols          approaches, either directly or indirectly, rely on protocol state
                                         through state machines. While most prior work constructs such        machines, which serve as a common modeling framework for
                                         models manually from 3GPP specifications, this process is labor-     representing and analyzing protocol workflows.
                                         intensive, error-prone, and difficult to maintain due to the            However, obtaining state machine models for telecommu-
                                         complexity and frequent updates of the specifications. Recent        nication network protocols is a non-trivial task. Specifically,
                                         efforts using natural language processing have shown promise,
                                         but remain limited in handling the scale and intricacy of cellular   these protocols are designed and maintained by the 3rd Gen-
                                         protocols. In this work, we propose SpecGPT, a novel framework       eration Partnership Project (3GPP), a global consortium com-
                                         that leverages large language models (LLMs) to automatically         prising network operators, equipment vendors, and researchers
                                         extract protocol state machines from 3GPP documents. SpecGPT         [14]. The standardized protocol details are documented in
                                         segments technical specifications into meaningful paragraphs, ap-    technical specifications written in semi-structured natural lan-
                                         plies domain-informed prompting with chain-of-thought reason-
                                         ing, and employs ensemble methods to enhance output reliability.     guage intended for domain experts. Due to the involvement
                                         We evaluate SpecGPT on three representative 5G protocols (NAS,       of a wide range of cellular stakeholders and network entities,
                                         NGAP, and PFCP) using manually annotated ground truth, and           the diversity of use cases, and strict backward compatibility
                                         show that it outperforms existing approaches, demonstrating the      requirements, 3GPP protocol standards are typically complex
                                         effectiveness of LLMs for protocol modeling at scale.                and verbose. They are distributed across multiple specification
                                            Index Terms—Large Language Models, State Machine, 3GPP
                                         Standards                                                            documents, each focusing on specific layers, procedures, or
                                                                                                              architectural components of the protocol, and often span
                                                                                                              hundreds or even thousands of pages. Since 3GPP does
                                                               I. I NTRODUCTION
                                                                                                              not provide formal models of the protocols, existing work
                                            Mobile telecommunication networks constitute a fundamen-          typically relies on domain experts to manually interpret the
                                         tal pillar of global communication infrastructure. According         specifications and construct corresponding state machines.
                                         to the GSMA Mobile Economy Report [1], the number of                 This process is labor-intensive, time-consuming, and prone to
                                         unique mobile subscribers worldwide surpassed 5.8 billion in         human error. The accuracy and level of abstraction of such
                                         2024. Beyond personal communication, mobile networks are             hand-crafted models significantly influence the effectiveness of
                                         increasingly integrated into critical sectors such as industrial     downstream tasks such as protocol verification. Furthermore,
                                         manufacturing, transportation, and healthcare, rendering them        3GPP specifications undergo frequent updates—typically five
                                         an indispensable component of modern society. As such, their         to six times per year. Keeping pace with these changes is
                                         failure can lead to far-reaching and severe consequences.            essential for assessing the security of the most recent protocol
                                         Ensuring the reliability and security of telecommunication           versions. However, due to the high time and labor costs
                                         networks have therefore become more crucial than ever [2].           involved, regularly updating manually constructed models is
                                            Network protocols specify the rules for information ex-           not feasible. In this work, we aim to automatically extract
                                         change between entities in a network and serve as the foun-          protocol state machines from 3GPP specifications.
                                         dation of telecommunication systems. To improve the overall             In recent years, researchers have explored the use of natu-
                                         security of telecommunication networks, researchers have pro-        ral language processing (NLP) techniques for the automated
                                         posed various approaches to evaluate protocol security from          analysis of protocol documents [15]–[17]. Pacheco et al.
                                         both design and implementation perspectives. For instance,           [18] proposed RFCNLP which is capable of extracting finite
                                         formal methods are employed to verify the security properties        state machines (FSMs) from Request for Comments (RFC)
documents. However, compared to the relatively small-scale                struction.
protocols defined in RFCs, cellular network protocols are               • We implement our technique in a tool called SpecGPT
significantly more complex, involving a larger number of state            and applied it to real-world 3GPP protocol specification
transitions, detailed protocol field descriptions, and intricate          documents for comprehensive evaluation. Experimental
cross-layer interactions, which render RFCNLP ineffective. To             results show that our approach can accurately construct
address these challenges, Ishtiaq et al. [19] introduced Hermes,          protocol state machine models and outperforms existing
which leverages a deep-learning-based neural parsing model to             state-of-the-art solutions.
perform constituency parsing of 3GPP documents and employs              The rest of the paper is organized as follows. We first
a domain-specific language to generate the final FSMs. Nev-          introduce the background and research scope in Section II.
ertheless, while Hermes incorporates domain-specific design          We then describe the design of SpecGPT in Section III. The
elements, its effectiveness is still constrained by the inherent     evaluation results are presented in Section IV, followed by a
complexity of the task.                                              discussion in Section V. We introduce related work in Section
   Since the release of ChatGPT in late 2022 [20], large lan-        VI and conclude our paper in Section VII.
guage models (LLMs) have demonstrated remarkable natural
language comprehension capabilities, leading to groundbreak-                                    II. BACKGROUND
ing progress in a wide range of NLP tasks, including document        A. Cellular network
summarization and structured data extraction [21]–[25]. In this
work, we propose leveraging large language models (LLMs)                Cellular networks have undergone a continuous evolution
to automatically extract protocol state machines from 3GPP           from 1G to 5G, transitioning from voice-centric systems to
specifications. However, the application of LLMs to highly           advanced, data-driven architectures capable of supporting high
technical, domain-specific protocol specifications remains rel-      data rates, ultra-low latency, and massive machine-type con-
atively unexplored. Applying LLM to infer protocol FSM               nectivity. A canonical cellular network architecture comprises
from 3GPP specifications encounters several challenges. On           two principal components: the Radio Access Network (RAN)
the one hand, as is mentioned before, the 3GPP specifications        and the Core Network (CN). Driven by increasing demands
as well as the protocols are highly complex. On the other            for service agility, flexibility, and scalability, network functions
hand, despite their strong language comprehension, LLMs are          have been progressively decoupled from dedicated hardware,
prone to hallucinations, especially when dealing with complex        fostering the adoption of modular, service-based architectures.
or ambiguous input [26]–[28].                                           As illustrated in Figure 1, the 5G CN is logically decom-
   To overcome these challenges and unlock the full potential        posed into a set of independent network functions (NFs), each
of large language models, we introduce SpecGPT, a novel              designed to fulfill a specific operational role. These NFs com-
framework designed to automatically extract protocol FSMs            municate with one another through standardized interfaces,
from complex technical documents. The framework first seg-           each associated with a dedicated protocol stack that supports
ments 3GPP specifications into semantically meaningful para-         various control- and user-plane operations. For example, the
graphs. It then constructs domain-informed prompts to guide          NGAP facilitates control-plane signaling between the RAN
the model toward accurate interpretations. Finally, ensemble         and the Access and Mobility Management Function (AMF);
methods are applied across multiple LLMs to aggregate and            the NAS protocol enables mobility management and session
refine the results, enhancing both reliability and performance.      control between the User Equipment (UE) and the AMF; and
We conduct a comprehensive evaluation of SpecGPT on 3GPP             the PFCP allows the Session Management Function (SMF)
specifications, targeting three representative protocols: 5G         to govern user-plane behavior and enforce traffic handling
NAS (Non-Access Stratum) [29], NGAP (Next Generation Ap-             policies on the User Plane Function (UPF).
plication Protocol) [30], and PFCP (Packet Forwarding Control
Protocol) [31]. Due to the absence of publicly available                                        5G Control plane
ground truth for their complete state machines, we construct                                    Service-Based Interface

manually annotated references. Experimental results indicate                             AMF                              SMF
that SpecGPT achieves an F1-score of up to 91.14% in the task                                                                   PFCP

of state transition extraction, outperforming the state-of-the-art        NAS                  NRF      PCF        UDM

method.                                                                               NGAP
                                                                                                       GTP
   In summary, we make the following major contributions in
this work:                                                                                                                       UPF   DN
                                                                     UE         RAN
   • We designed a novel technique that can automatically
      extract protocol state machines from 3GPP specifica-                                     Fig. 1. 5G Architecture.
      tion documents. Our approach leverages large language
      models to understand the natural language in the spec-
      ifications, incorporates domain knowledge to construct         B. 3GPP Specifications
      prompts, and employs model ensemble techniques to               3GPP is a collaborative standards organization comprising
      further improve the performance of state machine con-          multiple regional telecommunications standards development
organizations, dedicated to the development of globally appli-         •   Final State (qf ): The set of final states, which is a subset
cable technical specifications and technical reports for mobile            of Q (qf ∈ Q), indicating the terminal states when the
communication systems. By defining standardized interface                  protocol has completed its transitions.
protocols, 3GPP ensures interoperability among equipment
from different vendors, significantly promoting the develop-         B. Overview
ment and standardization of the global mobile communications
                                                                        We propose a framework named SpecGPT for automatically
industry.
                                                                     extracting state machines from 3GPP protocol specifications
   3GPP has developed a comprehensive suite of technical
                                                                     using LLMs. As illustrated in Figure 2, the framework consists
specifications that span multiple layers of the cellular network
                                                                     of three main components. In the preprocessing stage, we
architecture, including the RAN, CN, and UE. The volume
                                                                     first perform text cleaning on the original 3GPP documents.
of released specifications is substantial, and the standards are
                                                                     We then merge related sections to restructure the content,
continuously refined to accommodate emerging technologies
                                                                     enabling the documents to be segmented into smaller, coherent
and evolving use cases. For instance, in the context of 5G,
                                                                     chunks suitable as inputs for the LLMs. This mitigates issues
since the introduction of 5G New Radio in Release 15, the
                                                                     such as input truncation due to sequence length limitations.
specifications have evolved through successive releases up
                                                                     The preprocessing procedure is described in detail in Section
to Release 19. Each new release introduces enhancements
                                                                     III-C. In the prompt engineering stage, we design Chain-
over its predecessor and extends support for novel application
                                                                     of-Thought [32] prompts to guide the automatic extraction of
scenarios, such as integrated sensing and communication.
                                                                     protocol state machines. Additionally, we incorporate domain-
   Notably, each technical specification often spans hundreds
                                                                     specific knowledge to comprehensively refine and optimize the
of pages, addressing a wide range of deployment scenarios
                                                                     prompts, thereby improving their effectiveness. Further details
and operational conditions in mobile networks. This extensive
                                                                     are presented in Section III-D. In the model ensembling
and ever-growing body of documentation makes it increasingly
                                                                     stage, we utilize multiple LLMs in parallel to analyze the
inefficient and time-consuming for engineers and researchers
                                                                     protocol specifications. Their outputs are then aggregated
to manually understand and interpret the standards. Therefore,
                                                                     using a majority voting strategy to construct the final finite
there is a pressing need to explore automated approaches
                                                                     state machine. The ensembling process is detailed in Section
for the efficient parsing and application of these technical
                                                                     III-E.
specifications.
                          III. D ESIGN                               Algorithm 1 Section-level Paragraph Window Merging
                                                                     Require: Protocol document D
   Automatically extracting protocol state machines from              1: sections ← extract section numbers(D)
3GPP specifications is a highly non-trivial task. In this section,    2: paragraph to section ← map paragraphs to sections(D, sections)
                                                                      3: section tree ← build section tree(sections)
we present the design of SpecGPT, our proposed framework              4: for node ∈ get leaf nodes(section tree) do
for this challenge. We employ large language models (LLMs)            5: parent ← get parent(node, section tree)
to assist in interpreting the specifications written in natural       6: if all children merged(parent) == False then
                                                                      7:     content ← merge content(get children(parent))
language. Furthermore, we incorporate domain knowledge into           8:     assign content(parent, content)
prompt design and adopt an ensemble of LLMs to enhance                9:     set all children merged(parent) ← True
overall performance and robustness.                                  10: end if
                                                                     11: end for
A. FSM Statement                                                     12: merged windows ← get parent nodes with content(section tree)
                                                                         return merged windows
  The specification of a cellular network state machine is
typically defined as a quintuple ⟨Q, Σ, q0 , δ, F ⟩. The aim of
SpecGPT is to construct a formal model as follows:
                                                                     C. Preprocess
   • State Set (Q): A finite set of states representing all
     possible conditions that may occur within the protocol.            The input to the preprocessing stage is the raw 3GPP
   • Input Alphabet (Σ): Also referred to as the set of              specification. After text cleaning and section consolidation, the
     input symbols, this includes all possible transitions in        output consists of small segments that remain aligned with the
     the protocol implementation. Each transition represents a       original document structure.
     specific condition or action within the protocol, thereby            a) Document cleaning: The 3GPP specifications are
     triggering state transitions.                                   provided in Word format and contain a significant amount
   • Initial State (q0 ): The set of initial states, which is a      of non-body content, such as tables of contents, headers,
     subset of the state set Q (q0 ∈ Q), indicating the state in     footers, superscripted footnote markers, redundant blank lines,
     which the protocol resides at startup.                          and fragmented or irrelevant chart data. Such noisy text
   • State Transition Function (δ): A rule that defines how to       can hinder the model’s comprehension and reduce reasoning
     transition to the next state based on the current state and     accuracy. To address this, we apply regular expressions to
     input symbol. Formally, this is understood as δ : Q×Σ →         automatically detect and remove residual elements, including
     Q.                                                              tables of contents and headers.
                                                                                                                     Model Ensembling
                                                    Chain of Thought Prompting

          3GPP                                                     Condition
      Specifications                             State                                  Post
                                                                   and Action
                                               Extraction                            Processing
                                Paragraph                          Extraction
                                   Text

                                                              Enhance
                                                                                                                          Majority
      Document                                                                                                             Voting
       Cleaning                                        Prompt Optimization

                                    Collaborative              Implicit              Cross-
                                     Contextual             Information            Reference
     Text Splitting                  Reasoning               Integration           Handling



     Preprocessing                          Domain-Informed Prompt Engineering                                       Finite State Machine

                                                            Fig. 2. Overview of SpecGPT



     b) Text Splitting: Due to the context length limitations                    design and descriptive style in the specifications. Based on
of large language models, it is necessary to segment the                         our in-depth analysis of the 3GPP protocol specifications, we
document content before processing. Traditional strategies                       categorize them into two types: state-oriented and procedure-
typically adopt either fixed-size sliding windows or paragraph-                  oriented protocols.
based splitting. However, the former may lead to context                            State-oriented protocols are those in which transition nodes
loss due to truncation, while the latter often results in overly                 have clearly defined states, while procedure-oriented protocols
fine-grained segments, causing a large number of ineffective                     feature transition nodes described in terms of procedural steps.
queries (e.g., some paragraphs in 3GPP documents contain                         Based on this classification, we divided prompts into state
only one or two sentences). To address this, we perform                          prompts and process prompts during state extraction. For state-
section consolidation leveraging the hierarchical section struc-                 oriented protocols (e.g., NAS), state names are explicit— for
ture of 3GPP specifications to produce semantically coherent                     example, “5GMM-REGISTERED” indicates that the UE has
input chunks. Specifically, we define a hierarchical relationship                successfully registered with the core network, representing a
between sections as parent–child (also referred to as parent                     clear state. Here, the prompt can be formulated as “extract
and leaf nodes in our algorithm). As shown in Algorithm                          the states mentioned in the text.” In contrast, for procedure-
1, the proposed approach first parses section numbers and                        oriented protocols (e.g., PFCP), states typically refer to nodes
formatted markers to accurately extract and map section nodes                    within a procedure, such as “Established connection with
to their corresponding paragraphs. Furthermore, a section tree                   SMF.” In such cases, we focus on whether a specific procedure
is constructed based on section numbering, clarifying the hier-                  has been completed, and treat this as a state node.
archical and parent–child relationships across various section                      Unfortunately, the extraction of state tuples is often non-
levels. On this basis, for the lowest-level leaf nodes of the                    trivial. A major challenge arises from the presence of ambigu-
section tree, a bottom-up merging strategy is applied: all leaf                  ous or incomplete state names in the specifications themselves.
node contents under the same parent are merged recursively                       For instance, in the NAS specification, the documents may
into their parent node, thereby achieving hierarchical content                   describe states using vague terms such as “any state” or “some
aggregation across the document.                                                 state,” which lack precise definitions. Additionally, due to
                                                                                 the absence of clear state matching, large language models
D. Prompt Engineering                                                            may further generate so-called pseudo-states like “Unknown”
   In this stage, we integrate domain knowledge with chain-of-                   or “Undefined” during the extraction process. Traditional
thought prompt engineering to decompose the FSM extraction                       extraction approaches—primarily based on keyword matching
task into manageable sub-tasks. We further design targeted                       (e.g., detecting the word “state” preceding a potential state
prompt optimization strategies to maximize the potential of                      name)—are insufficient to handle such ambiguities and the
large language models.                                                           diverse expressions commonly found in protocol documents.
      a) Chain-of-Thought Prompting: The finite state ma-                        To mitigate these issues, we incorporate explicit instructions
chine extraction task is divided into three main stages: state                   into the prompt design to guide accurate state extraction, as
extraction, transition extraction, and post-processing. In our                   illustrated in Figure 3. Specifically, the model is instructed to
formulation, each transition is characterized by an associated                   extract only standardized state names defined in the protocol,
action and condition. The details of each step are presented in                  such as “5GMM-REGISTERED,” and to ignore non-standard
the following subsections.                                                       or descriptive phrases that could introduce noise into the state
   State Extraction. As shown in Figure 1, the 3GPP spec-                        set. Moreover, some states are presented in abbreviated forms,
ifications define a wide range of protocols, each designed                       such as “PLMN-SEARCH,” whereas the full qualified state
for different usage scenarios. As a result, they vary in both                    should be “5GMM-REGISTERED.PLMN-SEARCH.” To han-
                                                                   while an action represents the behavior executed once the
              Overall design prompt template
                                                                   condition is satisfied. To further improve accuracy, we include
    Extract state machine information from the combined            few-shot examples [33] to help the model learn and internalize
    content of these two parts (context + current).                this logical separation.
                                                                      Post-Processing. In the prompt design stage, we incorporate
    Context paragraph:[prev_paragraph]                             specific restrictive instructions to guide the behavior of the
    Current paragraph:[paragraph]                                  large language models. However, due to the inherent limita-
                                                                   tions of these models, the generated outputs may occasionally
    Instruction:                                                   deviate from the expected format or content. To address this,
    1.Covering (a) explicitly stated information and (b)           we introduce an auxiliary validation process to ensure output
    partially described information that requires logical
                                                                   reliability. During this stage, we first perform structural vali-
    inference.However, the reasoning must be based on the
                                                                   dation by checking the correctness of the JSON format during
    original text.
                                                                   parsing. Any outputs that fail to meet the required specification
                                                                   are automatically flagged and reported. In addition, we apply
    2.State names must correspond to official protocol state
    machine nodes (e.g., "5GMM-DEREGISTERED").
                                                                   a series of post-processing measures, including removal of
                                                                   pseudo-states and empty states. These steps are implemented
    3.For each transition, "condition" and "action" fields         through predefined rules, enabling the system to effectively
    must be distinguished, with content quoted verbatim            identify and eliminate undesired or noisy content.
    from the original text.                                              b) Prompt Optimization: SpecGPT aims to construct
    ...                                                            a holistic and comprehensive state machine representation.
                                                                   However, extracting the state machine based on individual text
    Note:                                                          segments may lead to information loss, as certain transitions
    For every complete transformation, a recheck of its            can span across segment boundaries. To address this limitation,
    rationality must be conducted.                                 we further develop prompt optimization strategies that leverage
    ...                                                            broader contextual information, enabling the model to infer
                                                                   and recover implicit state transitions.
    Desired format:                                                   Collaborative Contextual Reasoning. The large scale of
    {"states": ["STATE1", ...],                                    3GPP protocol specifications necessitates segmented process-
    "transitions": [ {"from": "STATE1", "to": "STATE2",            ing, which makes the recognition window of large language
    "condition": "...", "action": "..."},]}                        models a critical factor influencing extraction performance.
                                                                   Although preprocessing merges content across segment bound-
                                                                   aries, it does not fully achieve the construction of a coherent
            Fig. 3. A unified basic prompt model for FSM           global state machine. To address this issue, SpecGPT incor-
                                                                   porates a collaborative contextual reasoning mechanism. As
                                                                   illustrated in Figure 3, the prompt is explicitly designed to
dle such cases, SpecGPT employs an associated search and           include relevant historical context alongside the current text
multi-level joint reasoning strategy. During state extraction,     segment, enabling the model to continuously capture proto-
it analyzes the semantic relationships among the target state,     col behavior across segments. This approach supports more
its surrounding context, and adjacent states to infer and re-      accurate and consistent extraction of state machine elements
construct the complete state representation, thereby ensuring      by grounding the model’s reasoning in an extended context
consistency and correctness.                                       window.
   Transition Extraction. Conditions and actions define the           Integration of Explicit and Implicit Information. Con-
transitions in a state machine. Ideally, these elements are        ventional structured parsing methods [19] primarily focus
clearly stated in the specification. For example, a condition      on the accurate extraction of explicitly stated information in
may be expressed as “No 5GMM context has been estab-               protocol specifications, but often struggle to identify or capture
lished,” with the corresponding action being “The UE shall         deeper, latent logical relationships embedded within 3GPP
start the initial registration procedure.” However, in practice,   texts. To address this limitation, we design prompt strategies
conditions and actions in 3GPP documents often appear within       that integrate explicit extraction with implicit reasoning, as
the same sentence, and their boundaries are not always well        illustrated in Figure 3. This approach not only enables the pre-
defined. This ambiguity often leads to confusion during ex-        cise identification of clearly defined state machine elements,
traction by large language models, mainly due to difficulties      but also supports the inference of logically implied transitions
in understanding the logical relationship between the two          that are not directly expressed in the text. To minimize the
components. To address this issue, as illustrated in Figure 3,     risk of hallucinations, our prompts enforce strict grounding in
we explicitly highlight the distinction between conditions and     the original document content and require all inferred results
actions in our prompt design. A condition provides the premise     to undergo a subsequent plausibility verification process.
for deciding whether a specific response should be triggered,         Cross-Reference Handling. Cross-references are pervasive
in 3GPP protocol specifications. If the content being refer-             Two transitions Ti and Tj are considered aligned if and only
enced is not explicitly provided, it can result in contextual loss,   if all of the following hold:
as large language models are unable to access or retrieve the                             init
referenced material independently. To mitigate this issue, we                            
                                                                                          Si = Sjinit ,
                                                                                         S next = S next ,
                                                                                         
design a simplified retrieval-augmented generation (RAG) [34]                               i       j
mechanism. Specifically, we allow multiple protocol texts to                             
                                                                                         
                                                                                          Overlap(A  i , Aj ) ≥ θ,
be input simultaneously and use the original document section                            
                                                                                           Overlap(Ci , Cj ) ≥ θ.
numbers as prefixes to construct an integrated chapter-level
mapping. This design supports retrieval-based input, ensuring           Based on the aforementioned algorithm, we align the out-
that cross-referenced content is accurately located and incorpo-      puts from different models and apply a majority voting strategy
rated into the prompt, thereby improving the completeness and         to integrate them, thereby obtaining the final finite state
reliability of extracted information. Compared to conventional        machine.
RAG frameworks, our approach is lightweight, incurs minimal
                                                                                             IV. E VALUATION
computational overhead, and requires no external knowledge
base or embedding storage.                                               We evaluate SpecGPT on different settings and address the
                                                                      following three research questions:
E. Ensembling                                                            • RQ1: How effective is our multi-model ensemble frame-
   Despite the carefully crafted prompts informed by domain                work in extracting protocol semantics from real-world
knowledge, the performance of large language models remains                3GPP documents?
inherently constrained by limitations such as hallucination. To          • RQ2: How does our approach compare to state-of-the-art
further enhance overall reliability and accuracy, we adopt a               protocol analysis tools?
model ensemble strategy that aggregates outputs from mul-                • RQ3: What is the practical cost and generalization ability
tiple LLMs, thereby mitigating individual model biases and                 of deploying our framework in real-world settings?
improving extraction robustness. Specifically, we select several
mainstream LLMs from different providers, including GPT 4o            A. Settings
and Gemini 2.5 Pro etc. For the same input task, we generate             We selected five advanced models from different vendors,
candidate outputs with identical prompts and standardized pa-         namely GPT 4o [20], DeepSeek V3 [35], Qwen Turbo [36],
rameters (e.g., temperature settings). Due to architectural and       Claude Sonnet 4 [37], and Gemini 2.5 Pro [38]. These models
behavioral differences among models, their interpretations and        represent the most advanced open-source and proprietary large
outputs may vary, necessitating manual alignment to remove            language models available today [39]. The parameter sizes
obvious inconsistencies, such as omissions in state transitions.      of these models range from tens to hundreds of billions.
Additionally, since actions and conditions are extracted as           According to widely accepted recommendations for generating
original text spans from the source, different models may             factual responses, we set the temperature parameter to 0.2 [40].
select different fragments. To address these discrepancies, we        All experiments were conducted on a machine equipped with
introduce a consensus mechanism based on the principle of             32GB RAM and Intel Core i7-14700 CPU.
state transition completeness, utilizing a correlation matching            a) Groundtruth Construction: Currently, there is still a
algorithm defined as follows.                                         lack of a comprehensive and authoritative ground truth dataset
   Let Ti = (Siinit , Ai , Ci , Sinext ) denote a state transition    for 3GPP protocols. Existing datasets from prior work often
extracted by model i, where Siinit and Sinext represent the           suffer from limited protocol coverage and only capture explicit
initial and resulting states, Ai is the action text span, and Ci      states or behaviors. To address this gap, we manually con-
is the condition text span.                                           structed a detailed ground truth state machine dataset for three
   Two states Si and Sj are considered matching if                    widely used 5G core network protocols—NAS, NGAP, and
                                                                      PFCP. All protocols are based on Release 17 specifications.
                            Si = Sj .
                                                                      This effort involved over 210 person-hours of work by multiple
  For actions and conditions, let span(X) denote the text span        domain experts, including cross-validation and iterative peer
of X measured in words. The overlap between two spans is              review to ensure protocol type coverage, state completeness,
defined as                                                            and strict compliance with 3GPP specifications. Our ground
                           |span(Ai ) ∩ span(Aj )|                    truth dataset significantly improves state transition coverage
   Overlap(Ai , Aj ) =                               ≥ θ,            across mainstream protocols, providing a robust foundation for
                       min |span(Ai )|, |span(Aj )|
                                                                      future research in protocol modeling, analysis, and verification.
where θ is a predefined threshold indicating sufficient overlap.           b) Evaluation Metrics: We employ three widely used
We set θ as 0.75 in practice, which yielded the best perfor-          and objective measures: Precision, Recall, and F1-Score. Fol-
mance in our evaluation.                                              lowing standard definitions, precision is defined as T PT+F P
                                                                                                                                     P,
  Similarly, for conditions,                                                                    TP
                                                                      Recall is given by T P +F N , the F1-Score is calculated as
                           |span(Ci ) ∩ span(Cj )|                    2 × Precision×Recall
                                                                            Precision+Recall . Here, T P denotes the number of true
   Overlap(Ci , Cj ) =                                ≥ θ.
                         min |span(Ci )|, |span(Cj )|                 positives, F P denotes false positives (i.e., the number of
instances incorrectly predicted as positive), and F N denotes                                   TABLE I
false negatives (i.e., actual positive instances missed by the            C OMPARISON OF THE THREE INDICATORS OF VARIOUS LLM S
model). It should be emphasized that the F1-Score takes                      Model          Precision (%)   Recall (%)   F1-score (%)
into account both F P and F N , thereby serving as a crucial             Claude Sonnet 4        80.39         87.23         83.67
indicator for the overall performance of the model in this study.         DeepSeek V3           68.70         84.04         75.60
                                                                         Gemini 2.5 Pro         70.00         89.36         78.50
                                                                             GPT 4o             79.09         92.55         85.29
B. RQ1: End-to-End Performance                                             Qwen Turbo           61.71         77.66         68.77
                                                                            Ensemble            91.86         90.43         91.14
   We apply SpecGPT to extract state machines from the three
protocols included in our ground truth dataset, namely the                                        TABLE II
Release 17 versions of NAS, NGAP, and PFCP, in order                    I NDICATOR DATA AT DIFFERENT LEVELS OF DIFFERENT PROTOCOLS
to conduct a systematic evaluation of SpecGPT. Since the                    Protocol        Precision (%)   Recall (%)   F1-score (%)
model outputs for conditions and actions are directly extracted             PFCP-all            85.71         90.00         87.80
from the source documents, their spans may not perfectly                 PFCP-asscoiation       85.71         84.04         80.00
                                                                          PFCP-session          92.30         92.30         92.30
correspond to those in the ground truth. Therefore, we adopt                NGAP-all            70.71         67.96         69.31
an alignment strategy similar to that used in the ensembling               NGAP-NCG             91.67         71.43         80.29
process (Section III-E). Specifically, a state machine transition          NGAP-PSR             72.92         68.63         70.71
                                                                           NGAP-UCM             57.43         64.89         60.93
is considered correct only if the states match exactly, and
both the condition and action spans overlap beyond a specified
threshold, which we set as 0.75 in experiments.
                                                                           c) Performance of Transition Extraction on PFCP and
     a) Performance of State Extraction on NAS: The NAS              NGAP: Table II summarizes the performance of SpecGPT in
ground truth we annotated includes a total of 18 distinct states     extracting state transitions within the PFCP and NGAP proto-
and 179 transitions. All five models successfully and precisely      cols. To enable a more detailed evaluation of SpecGPT’s capa-
extracted all these states within the NAS protocol, resulting in     bilities, both protocols were further subdivided for fine-grained
an F1-score of 100%. This achievement highlights both the            assessment across distinct protocol components. Specifically,
advanced understanding ability of large language models and          for the PFCP protocol, we separated the association estab-
the effectiveness of our specialized state extraction design.        lishment and maintenance functions (association layer) from
     b) Performance of Transition Extraction on NAS:                 session management and forwarding rule control (session
Table I presents the extraction performance of various large         layer), treating them as two independent layers. For the NGAP
language models on state transitions within the NAS protocol.        protocol, the subdivision was based on functional granularity
The row labeled ”Ensemble” shows the aggregated results              and control scope, resulting in three hierarchical layers from
from the five models, reflecting SpecGPT’s overall perfor-           the network to the service bearer level: the Next-Generation
mance in extracting state transitions. The effectiveness of          Core (NGC) Connection Global layer, describing the global
transition extraction demonstrates SpecGPT’s comprehensive           state of the NGC interface; the UE Context Main (UCM)
capability in the state machine extraction task. As indicated        layer, responsible for signaling and state management at
in the table, extraction performance varies among models             the UE level; and the PDU (Protocol Data Unit) Session
despite using identical prompt configurations. Specifically, the     Resource layer, focusing on PDU session resources for each
models exhibit relatively low precision, ranging from 61.71%         UE. Experimental results demonstrate that SpecGPT achieves
to 80.39%, while recall remains comparatively high, between          excellent extraction performance on the PFCP protocol both
77.66% and 92.55%. This discrepancy is primarily due to              overall and within each individual layer, with particularly
the hallucination problem. Large language models tend to             precise recognition in the association and session layers. In
generate significantly more transition tuples than actually exist,   contrast, the NGAP protocol is more complex and exhibits
leading to a higher false positive rate and consequently lower       certain ambiguities in its specification, increasing the difficulty
precision. However, this hallucination does not markedly affect      of automatic extraction. Nonetheless, its overall extraction
the coverage of correct transitions, resulting in consistently       performance still satisfies the basic requirements for practical
high recall. Furthermore, when ensemble decision strategies          application.
are applied across multiple models, the F1-score improves
substantially, ranging from 5.85% to 22.37%. This improve-           C. RQ2: Comparison with the SOTA
ment is attributed to the ensemble method’s ability to remove          To evaluate the effectiveness of SpecGPT, we further con-
incorrect transitions caused by hallucinations in individual         duct a comparative evaluation against Hermes [19], the SOTA
models, thereby boosting overall extraction performance.             tool designed to automatically extract protocol finite state
   Large language models were trained using 3GPP specifica-          machines (FSMs) from 3GPP specification documents.
tion documents. We attempted to directly prompt these models           Since the Hermes paper only reports experimental results on
to output state machines for different protocols, but the result-    the 5G NAS and RRC protocols, we restrict our comparison
ing F1-score was only 14.87%. This outcome demonstrates              with Hermes to the 5G NAS protocol. The main limitation
the necessity of our carefully designed in-context prompts.          of Hermes lies in its explicit extraction, which is restricted
to fully articulated transitions explicitly stated in protocol
                                                                            96
specification texts, and does not sufficiently account for the                                                                          <state>
semantic logic and implicit information inherent in the natural                                                                         <contion>
                                                                            91                                                          <action>
language formation of specifications. In contrast, SpecGPT is                                                                           all
capable of capturing implicit state transitions embedded in the             86
protocol specifications. Hermes does not provide the actual
state machines it constructed. According to the evaluation                  81

results reported in its paper, Hermes achieves an accuracy of       100
                                                                     80
81.39% for actions and 86.40% for conditions on the 5G NAS           60
protocol. In comparison, SpecGPT achieves higher accuracies          40
of 86.41% and 92.94%, respectively. It is worth noting that          20
                                                                      0
the ground truth used by SpecGPT is more comprehensive in                 Claude Sonnet 4 DeepSeek V3   Gemini 2.5 Pro   GPT 4o      Qwen Turbo
terms of both the number of states and transitions. Therefore,
SpecGPT demonstrates superior overall performance on the                    Fig. 4. The effectiveness of each model in labeling the tags
5G NAS protocol compared to Hermes.

                            TABLE III                              comparable usage across the evaluated models. Based on the
        T HE EFFECTS OF DIFFERENT TOOLS IN LABELING TAGS           respective API pricing, we estimate the cost per run to be
        Tools          Precision (%)   Recall (%)   F1-score (%)   approximately $2.7 for NAS, $1.6 for NGAP, and $1.5 for
   NEUTREX-Labeled         64.30         66.13         65.20       PFCP. In terms of runtime efficiency, the primary influence is
  NEUTREX-Unlabeled        66.88         68.79         67.82       the type of LLM employed. Through optimized input window
        LLM                87.46         90.40         88.90
                                                                   scheduling and segmentation strategies, we have significantly
   In addition, Hermes introduces a dedicated neural con-          reduced the processing time for a single document from
stituency parser, NEUTREX, to annotate transition compo-           several hours to mere minutes. Additionally, preprocessing
nents such as states, conditions, and actions in 3GPP specifica-   and comparative testing typically require less than one minute.
tion documents. To assess the effectiveness of large language      Detailed performance metrics are also presented in Table IV.
models (LLMs) on the same task, we use the ground truth            Considering that protocol state machine extraction is usually
provided by Hermes, which includes human-annotated transi-         performed only once per document, the overall time cost is
tion components extracted from the specifications. Using this      acceptable in practical scenarios. With ongoing advancements
dataset, we apply LLMs to perform the annotation task without      in foundation models, we expect both monetary costs and
any task-specific training. The results are shown in Table         processing time to further decrease.
III. In this table, NEUTREX-Unlabeled denotes NEUTREX’s
                                                                                               TABLE IV
performance on the detected spans without any consideration        T HE COSTS AND EFFICIENCIES OF EACH MODEL UNDER EACH PROTOCOL
of the labels assigned to them, while NEUTREX-Labeled take
into consideration the labels assigned. Overall, LLMs outper-                                           # Input      # Output
                                                                    Protocol           Model                                      Time (minute)
                                                                                                        Tokens        Tokens
form NEUTREX on this task. These findings underscore the                          Claude Sonnet 4       221,829       50,347           32
advantages of our end-to-end approach, which achieves higher                       DeepSeek V3          233,517       75,239          117
accuracy without relying on a dedicated parser or training           NAS          Gemini 2.5 Pro        236,751       74,985          202
                                                                                      GPT 4o            235,984       94,202           20
process. Figure 4 presents a breakdown of the performance                           Qwen Turbo          234,894       97,863           57
of different large language models on each type of transition                     Claude Sonnet 4       130,490       29,358           20
component in this task. All five models demonstrate strong                         DeepSeek V3          136,578       43,857           69
                                                                     NGAP         Gemini 2.5 Pro        136,875       43,221          119
performance across the annotation of individual components.                           GPT 4o            136,560       55,461           12
This also highlights the potential of LLMs to simplify and                          Qwen Turbo          136,423       57,400           35
enhance automated protocol analysis by eliminating the need                       Claude Sonnet 4       118,904       26,721           18
                                                                                   DeepSeek V3          124,551       39,826           61
for complex intermediate models.                                     PFCP         Gemini 2.5 Pro        124,686       39,801          113
                                                                                      GPT 4o            124,558       49,577           10
D. RQ3: Cost and Generalization Ability                                             Qwen Turbo          124,496       51,996           31
     a) Cost: We assess the practical cost of our approach
from two perspectives: monetary expense and runtime effi-                b) Generalization Ability: We further assess the gen-
ciency. Specifically, we measure the number of tokens con-         eralization ability of SpecGPT on a different version of
sumed and the processing time required by SpecGPT when             the specifications, as real-world applications typically require
invoking large language models and executing subsequent            re-extracting state machine models following specification
processing pipelines. Regarding monetary cost, token usage         updates. Specifically, the evaluation is performed using the
is the main factor, which largely depends on the length            Release 15 (R15) version of the NAS protocol specification.
of the 3GPP specification documents. Table IV summarizes           SpecGPT successfully extracted 142 state transitions from the
the detailed token consumption for each model, showing             Release 15 (R15) version of the specification, representing
a reduction of approximately 20% compared to Release 17                  b) Enrichment of 3GPP specifications: The main reason
(R17). Notably, the total number of states remained largely        researchers have to manually construct state machine models
unchanged. This outcome is consistent with expectations, as        is that the 3GPP, as the maintainer of protocol specifications,
R15 serves as the initial 3GPP standard defining 5G NR             provides the standards only in natural language, rather than
and 5GC, whereas R17 introduces subsequent enhancements,           in more structured forms such as state machines, which are
including new features, commercial deployment scenarios, and       better suited for a wide range of downstream tasks. This
expanded network capabilities, which collectively contribute       choice is influenced by various factors, but a major con-
to increased complexity in the protocol’s state machine. The       straint is the substantial manual effort required to create and
results of the experiment validate the generalization ability      maintain such formal representations. Our tool addresses this
of our tool, indicating its effectiveness in handling multiple     gap by automatically extracting protocol state machines from
versions of the protocol specifications.                           the specifications, significantly reducing human workload and
                                                                   enabling structured, machine-readable representations that can
                        V. D ISCUSSION                             greatly support tasks such as verification, testing, and protocol
                                                                   evolution.
A. Limitations and Future Work
   Although SpecGPT achieved an F1-score of 91.14% in                                   VI. R ELATED W ORK
extracting protocol state machines from 3GPP documents
                                                                   A. Cellular Security
and significantly outperformed the existing SOTA tool, it
still suffers from false positives and false negatives due to         The complexity and continuous evolution of cellular net-
inherent limitations such as hallucinations in large language      work protocols have driven growing interest in automated
models. This challenge is common across many LLM-based             security analysis and verification approaches [3]–[6], [8]–[12],
approaches [26], [27]. Addressing this issue requires progress     [42]. Karim et al. [8] introduced ProChecker, a framework
in two key directions. The first is the continual improvement      that combines dynamic testing with static instrumentation to
of foundation model capabilities. The second involves the in-      detect logical flaws in 4G LTE protocol implementations.
tegration of emerging techniques such as retrieval-augmented       Akon et al. [3] proposed CoreScan, a decomposition-based
generation [34] and self-consistency [41] to reduce hallucina-     framework with assume-guarantee reasoning to verify 5G
tions and improve the reliability of model outputs. As large       access control, uncovering five new privilege escalation vul-
language model technologies continue to evolve rapidly, our        nerabilities. Dong et al. [9] proposed CoreCrisis, a stateful
extensible multi-model ensemble framework is well positioned       fuzzing framework that learns an FSM to guide state-aware
to benefit from these advancements. This will enable contin-       mutation for testing 5G core implementations. It discovered 7
uous improvement in state machine extraction and ultimately        specification deviations and 13 critical vulnerabilities. While
support the goal of generating complete and accurate protocol      existing works have advanced automated security analysis of
state machines. In addition, this work focuses exclusively         cellular protocols, automation in state machine modeling re-
on protocol state machines. However, protocol specification        mains limited—especially for the complex, dynamic interfaces
documents contain a wealth of other valuable information,          in 5G and beyond.
such as protocol fields and potential security hazards, which
play a critical role in various security-related tasks. We leave   B. Machine Learning Based Document Analysis
the extraction and utilization of such information to future
work.                                                                 Machine learning, particularly NLP, is increasingly used
                                                                   to extract structured protocol specifications from documents
B. Utility of SpecGPT                                              and code, supporting automated protocol parsing and state
                                                                   modeling [15], [16], [18], [19], [43], [44], [45]. Chen et al.
   This work focuses on the automatic extraction of protocol       [16] introduced CREEK, which uses a fine-tuned BERT model
state machines from 3GPP specifications. The proposed frame-       and Positive-Unlabeled learning to classify security-relevant
work can facilitate a variety of downstream tasks, especially      3GPP Change Requests, and successfully uncovered multiple
in protocol verification and testing, and the enrichment of        exploitable security vulnerabilities. Ishtiaq et al. [19] proposed
technical specifications.                                          Hermes, which combines a neural parser, a domain-specific
      a) Protocol verification and testing: Most existing tools    language for intermediate representation, and logic-driven
for protocol verification and testing rely on hand-crafted state   FSM generation to automatically extract state machines from
machines, which are time-consuming to build, error-prone,          3GPP specifications using NLP. Rahman et al. [44] applied
and difficult to maintain. With frequent updates to protocol       NLP to identify design-level inconsistencies in specification
specifications, manually constructed models often become           documents and assessed their potential impact on implemen-
outdated quickly. SpecGPT can automatically extract state          tation choices. However, prior methods rely on annotated
machine models from the specifications, significantly reducing     data and domain-specific training. Whether the capabilities of
the manual effort required and improving the maintainability       large language models can be leveraged for efficient protocol
and accuracy of existing protocol analysis research.               recognition is the focus of this work.
                           VII. C ONCLUSION                                        [16] Y. Chen and e. a. Tang, “Seeing the forest for the trees: Understanding
                                                                                        security hazards in the 3gpp ecosystem through intelligent analysis
   In this work, we present SpecGPT, a novel framework                                  on change requests,” in Proceedings of the 31st USENIX Security
                                                                                        Symposium (Security 2022), 2022, pp. 2713–2730.
for automatically extracting protocol state machines from                          [17] H.-T. Nguyen, N.-Q. Nguyen, N. K. Dao et al., “When 5g security
3GPP specifications using large language models. By com-                                meets natural language processing: Challenges and future pathways,” in
bining domain-informed prompt engineering, chain-of-thought                             Proceedings of the 2024 IEEE Conference on Antenna Measurements
                                                                                        and Applications (CAMA), 2024.
reasoning, and ensemble techniques, SpecGPT effectively                            [18] M. L. Pacheco, M. von Hippel, B. Weintraub, D. Goldwasser, and
addresses the complexity, scale, and ambiguity inherent in                              C. Nita-Rotaru, “Automated attack synthesis by extracting finite state
cellular protocol documents. Our evaluation on NAS, NGAP,                               machines from protocol specification documents,” in 2022 IEEE Sym-
                                                                                        posium on Security and Privacy (SP). IEEE, 2022, pp. 51–68.
and PFCP protocols demonstrates that SpecGPT achieves                              [19] A. Al Ishtiaq, S. S. S. Das, S. M. M. Rashid, A. Ranjbar, K. Tu, T. Wu,
higher accuracy compared to prior approaches, highlighting                              Z. Song, W. Wang, M. Akon, R. Zhang et al., “Hermes: unlocking
the potential of LLMs in automating protocol analysis. The                              security analysis of cellular network protocols by synthesizing finite
                                                                                        state machines from natural language specifications,” in 33rd USENIX
state machines extracted by our framework serve as structured,                          Security Symposium (USENIX Security 24), 2024, pp. 4445–4462.
interpretable representations of protocol behavior, which can                      [20] “ChatGPT,” https://chatgpt.com/, 2025.
further facilitate downstream tasks such as automated testing                      [21] M. Zheng, D. Xie, and X. Zhang, “Large language models for validating
and formal verification, ultimately enhancing the robustness                            network protocol parsers,” IEEE Transactions on Network and Service
                                                                                        Management, 2025.
and security of modern communication protocols.                                    [22] M. Duclos, I. A. Fernandez, K. Moore et al., “Utilizing large language
                                                                                        models to translate rfc protocol specifications to cpsa definitions,” IEEE
                                                                                        Access, 2024.
                               R EFERENCES                                         [23] L. Ma, S. Liu, Y. Li et al., “Specgen: Automated generation of formal
                                                                                        program specifications via large language models,” Proceedings of the
 [1] “The       Mobile       Economy        2025,”     https://www.gsma.com/            ACM on Programming Languages, 2024.
     solutions-and-impact/connectivity-for-good/mobile-economy/, 2025.             [24] Y. Maklad, F. Wael, W. Elsersy et al., “Retrieval augmented generation
 [2] R. Khan, P. Kumar, D. N. K. Jayakody, and M. Liyanage, “A survey                   based llm evaluation for protocol state machine inference with chain-
     on security and privacy of 5g technologies: Potential solutions, recent            of-thought reasoning,” IEEE Transactions on Information Forensics and
     advancements, and future directions,” IEEE Communications Surveys &                Security, 2025.
     Tutorials, vol. 22, no. 1, pp. 196–248, 2019.                                 [25] P. Sharma and V. Yegneswaran, “Prosper: Extracting protocol specifica-
 [3] M. Akon, M. Toufikuzzaman, and S. R. Hussain, “From control to chaos:              tions using large language models,” in Proceedings of the 22nd ACM
     A comprehensive formal analysis of 5g’s access control,” in Proceedings            Workshop on Hot Topics in Networks, 2023, pp. 41–47.
     of the 2025 IEEE Symposium on Security and Privacy (SP), 2025.                [26] L. Huang, W. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen,
 [4] D. Basin, J. Dreier, L. Hirschi, S. Radomirovic, R. Sasse, and V. Stettler,        W. Peng, X. Feng, B. Qin et al., “A survey on hallucination in large
     “A formal analysis of 5g authentication,” in Proceedings of the 2018               language models: Principles, taxonomy, challenges, and open questions,”
     ACM SIGSAC conference on computer and communications security,                     ACM Transactions on Information Systems, vol. 43, no. 2, pp. 1–55,
     2018, pp. 1383–1396.                                                               2025.
 [5] S. R. Hussain and e. a. Echeverria, “5greasoner: A property-directed se-      [27] Z. Xu, S. Jain, and M. Kankanhalli, “Hallucination is inevitable:
     curity and privacy analysis framework for 5g cellular network protocol,”           An innate limitation of large language models,” arXiv preprint
     in Proceedings of the 2019 ACM SIGSAC Conference on Computer and                   arXiv:2401.11817, 2024.
     Communications Security (CCS ’19), 2019, pp. 669–684.                         [28] D. Xie, B. Yoo, N. Jiang et al., “How effective are large language
 [6] S. Hussain, O. Chowdhury, S. Mehnaz, and E. Bertino, “LTEInspector:                models in generating software specifications?” in Proceedings of the
     A systematic approach for adversarial testing of 4g LTE,” in Network               2025 IEEE International Conference on Software Analysis, Evolution
     and Distributed Systems Security (NDSS) Symposium 2018, 2018.                      and Reengineering (SANER), 2025.
 [7] C. Cremers and M. Dehnel-Wild, “Component-based formal analysis of            [29] “Non-Access-Stratum (NAS) protocol for 5G System (5GS); Stage 3,”
     5g-aka: Channel assumptions and session confusion,” in Network and                 https://www.3gpp.org/dynareport/24501.htm, 2025.
     Distributed Systems Security (NDSS) Symposium, 2019.                          [30] “Ng-ran; ng application protocol (ngap),” https://www.3gpp.org/
 [8] I. Karim, S. R. Hussain, and E. Bertino, “Prochecker: An automated                 dynareport/38413.htm, 2025.
     security and privacy analysis framework for 4g lte protocol imple-            [31] “Interface between the control plane and the user plane nodes,” https:
     mentations,” in Proceedings of the IEEE International Conference on                //www.3gpp.org/dynareport/29244.htm, 2025.
     Distributed Computing Systems (ICDCS), 2021, pp. 1158–1168.                   [32] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le,
 [9] Y. Dong, T. Yang, A. Al Ishtiaq, S. M. M. Rashid, A. Ranjbar, K. Tu,               D. Zhou et al., “Chain-of-thought prompting elicits reasoning in large
     T. Wu, M. S. Mahmud, and S. R. Hussain, “Corecrisis: Threat-guided                 language models,” Advances in neural information processing systems,
     and context-aware iterative learning and fuzzing of 5g core networks,”             vol. 35, pp. 24 824–24 837, 2022.
     2025.                                                                         [33] A. Parnami and M. Lee, “Learning from few examples: A summary
[10] T. Yang, S. K S, A. Arumugam, and S. Hussain, “Feedback-guided api                 of approaches to few-shot learning,” arXiv preprint arXiv:2203.04291,
     fuzzing of 5g network,” 2024.                                                      2022.
[11] N. Bennett, W. Zhu, B. Simon, R. Kennedy, W. Enck, P. Traynor, and            [34] Y. Gao, Y. Xiong, X. Gao, K. Jia, J. Pan, Y. Bi, Y. Dai, J. Sun,
     K. R. Butler, “Ransacked: A domain-informed approach for fuzzing                   H. Wang, and H. Wang, “Retrieval-augmented generation for large
     lte and 5g ran-core interfaces,” in Proceedings of the 2024 on ACM                 language models: A survey,” arXiv preprint arXiv:2312.10997, vol. 2,
     SIGSAC Conference on Computer and Communications Security, 2024,                   no. 1, 2023.
     pp. 2027–2041.                                                                [35] “DeepSeek,” https://chat.deepseek.com/, 2025.
[12] H. Kim, J. Lee, E. Lee, and Y. Kim, “Touching the untouchables:               [36] “Qwen,” https://github.com/QwenLM/Qwen, 2025.
     Dynamic security analysis of the lte control plane,” in 2019 IEEE             [37] “Claude,” https://claude.ai/, 2025.
     Symposium on Security and Privacy (SP). IEEE, 2019, pp. 1153–1168.            [38] “Gemini,” https://gemini.google.com/app, 2025.
[13] L. Huang, P. Zhao, H. Chen et al., “Large language models based fuzzing       [39] “Lmarena leaderboad,” https://lmarena.ai/leaderboard, 2025.
     techniques: A survey,” ACM Computing Surveys, 2024.                           [40] M. Peeperkorn, T. Kouwenhoven, D. Brown, and A. Jordanous, “Is
[14] “3GPP Standard,” https://www.3gpp.org/, 2025.                                      temperature the creativity parameter of large language models?” arXiv
[15] Y. Chen, Y. Yao, X. Wang, D. Xu, C. Yue, X. Liu, K. Chen, H. Tang,                 preprint arXiv:2405.00492, 2024.
     and B. Liu, “Bookworm game: Automatic discovery of lte vulnerabilities        [41] X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdh-
     through documentation analysis,” in 2021 IEEE Symposium on Security                ery, and D. Zhou, “Self-consistency improves chain of thought reasoning
     and Privacy (SP). IEEE, 2021, pp. 1197–1214.                                       in language models,” arXiv preprint arXiv:2203.11171, 2022.
[42] A. Shaik, R. Borgaonkar, N. Asokan et al., “Practical attacks against
     privacy and availability in 4g/lte mobile communication systems,” IEEE
     Transactions on Mobile Computing, 2017.
[43] S. M. M. Rashid, T. Wu, K. Tu et al., “State machine mutation-
     based testing framework for wireless communication protocols,” IEEE
     Transactions on Software Engineering, 2024.
[44] M. M. Rahman, I. Karim, and E. Bertino, “CellularLint: A Systematic
     Approach to Identify Inconsistent Behavior in Cellular Network Speci-
     fications,” in 33rd USENIX Security Symposium (USENIX Security 24),
     2024, pp. 5215–5232.
[45] Z. Wang and Y. Wang, “NLP-based Cross-Layer 5G Vulnerability
     Detection via Fuzzing-Generated Run-Time Profiling,” in 2023 IEEE
     12th International Conference on Cloud Networking (CloudNet), 2023,
     pp. 194–202.
