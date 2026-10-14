                                                       Understanding the Usability of Cryptographic Verification Tools

                                                       Tarikul Islam                                                    Yasin Islam
                                              Samsung R&D Institute Bangladesh                      Bangladesh University of Engineering and Technology
                                                                 Khandakar Ashrafi Akbar                              Imtiaz Karim
                                                                    Towson University                        The University of Texas at Dallas
arXiv:2609.16323v1 [cs.CR] 14 Sep 2026




                                                                   Abstract                                      post-compromise security, ratcheting, and stateful hardware
                                                                                                                 components, the practical demand for rigorous, tool-assisted
                                         Cryptographic protocol verification tools are widely used to
                                                                                                                 verification continues to grow.
                                         analyze the security of complex protocols, yet how users inter-
                                         act with these tools remains comparatively understudied. We                Yet the effectiveness of a verification tool depends not only
                                         present an exploratory human-centered study of experienced              on its theoretical expressiveness but on whether its intended
                                         users of Tamarin, ProVerif, and related protocol verifiers. Our         users can actually apply it correctly. A protocol verifier that
                                         survey included researchers, graduate students, and practi-             can, in principle, establish strong security guarantees is of lim-
                                         tioners with hands-on experience using Tamarin, ProVerif, or            ited value if practitioners cannot construct a faithful model of
                                         related tools. The findings reveal usability barriers across the        the protocol, cannot understand why a proof fails to terminate,
                                         verification workflow, including difficulties debugging non-            or cannot distinguish a genuine attack from an artifact of an
                                         termination and performance issues and the lack of systematic           overly coarse abstraction. Usable security research has long
                                         methods for validating formal models against real protocols.            shown that this kind of gap between theoretical capability and
                                         When proofs fail without concrete attacks, users commonly               practical usability is a recurring source of real-world secu-
                                         simplify models, add helper lemmas, and revisit modeling ab-            rity failure: studies of cryptographic APIs, for instance, have
                                         stractions. Participants also called for actionable diagnostics,        found that developers can produce code they believe is se-
                                         clearer explanations of results, visualization, and automation          cure while violating basic security requirements, not because
                                         for recurring proof tasks. Our findings suggest that persistent         the underlying primitives are flawed, but because the tools
                                         usability challenges arise from the gap between protocol-level          and interfaces around them are hard to use correctly [3, 35].
                                         reasoning and the verifier’s formal model, proof procedures,            Adjacent classes of security tooling, including constant-time
                                         and diagnostic output. We derive concrete design priorities             analysis tools and fuzzers, exhibit similar patterns: usability
                                         for improving the accessibility, interpretability, and usability        shortcomings around installation, documentation, and output
                                         of cryptographic protocol verification tools.                           interpretation measurably suppress adoption even when the
                                                                                                                 underlying technique is mature and effective [18, 52].
                                                                                                                    Despite this, the usability of cryptographic protocol ver-
                                         1   Introduction                                                        ification tools themselves has received comparatively little
                                                                                                                 systematic attention. Prior work on Tamarin and ProVerif
                                         Formal verification has become a cornerstone of modern pro-             overwhelmingly focuses on their formal expressiveness and
                                         tocol security engineering. Tools such as ProVerif [9, 10] and          analytical power, for example comparing which tool can de-
                                         the Tamarin Prover [5, 31] allow researchers and practitioners          tect which class of attack on a shared benchmark of proto-
                                         to symbolically model cryptographic protocols, specify adver-           cols [26]. This line of work is valuable for understanding what
                                         sarial capabilities, and either prove that a protocol satisfies a       these tools can prove, but it says little about how real users,
                                         given security property for an unbounded number of sessions             ranging from graduate students encountering formal methods
                                         or produce a concrete attack trace that violates it. These tools        for the first time to expert researchers modeling novel pro-
                                         have moved well beyond academic exercises: Tamarin was                  tocols, actually experience the process of learning the tool,
                                         used in the design and analysis of Apple’s iMessage PQ3 pro-            constructing a model they trust, and interpreting the tool’s
                                         tocol [4] and helped uncover a security flaw in an early draft          output. The formal methods community has itself begun to
                                         of TLS 1.3 [15], while ProVerif has been applied to widely de-          recognize this gap: recent position papers call explicitly for
                                         ployed protocols including TLS 1.3 [6] and Signal [8, 29]. As           more human-centered study of formal verification tools, argu-
                                         protocols grow more complex, incorporating features such as             ing that questions of learnability, mental models, and practical


                                                                                                             1
impact remain underexplored relative to the pace of technical           messages, interactive debugging and visualization support,
advances in the tools themselves [12, 30]. Industrial user stud-        and automation for common but tedious tasks such as helper-
ies of verification engineers echo this concern, finding that           lemma generation.
the interpretability of verification results, rather than the un-         This paper makes the following contributions:
derlying formal guarantees, is often what determines whether
engineers trust and adopt a tool [28].                                      • We present an exploratory human-centered study focused
   We address this gap and present a survey-based empiri-                     specifically on the end-to-end experiences of 16 expe-
cal study of 16 experienced users of cryptographic protocol                   rienced users of Tamarin, ProVerif, and related crypto-
verification tools. The users had direct, hands-on experience                 graphic protocol verifiers.
using Tamarin, ProVerif, or related tools in academic or indus-
                                                                            • We identify and characterize usability barriers spanning
try settings, recruited through academic publications, open-
                                                                              the full verification workflow, from learnability through
source contributions, community outreach, and snowball sam-
                                                                              modeling, proof debugging, and result interpretation, and
pling. The survey combined closed- and open-ended ques-
                                                                              show that these barriers are shared across tools despite
tions across five sections, covering participant background,
                                                                              their differing theoretical foundations.
tool learnability, the end-to-end modeling and verification
workflow, and tool-specific usability issues unique to Tamarin              • We analyze the extent to which programming and
and ProVerif respectively. Guided by this study, we investigate               general-purpose model-checking experience transfers to
three research questions:                                                     cryptographic protocol verification, providing evidence
                                                                              for where existing user knowledge helps and where it
   • RQ1: What usability barriers do users encounter when                     falls short.
     applying cryptographic protocol verification tools such
     as Tamarin and ProVerif?                                               • We distill participants’ feedback into concrete, priori-
                                                                              tized recommendations for improving the usability, di-
   • RQ2: How do users perceive the transfer of prior pro-                    agnostics, and automation support of cryptographic ver-
     gramming and general purpose model-checking experi-                      ification tools, informing both future tool design and
     ence to learning and using cryptographic protocol verifi-                the development of educational and documentation re-
     cation tools?                                                            sources.
   • RQ3: What improvements do users believe would make
     these tools more accessible and effective?                         2    Background
   Our findings show that usability barriers are distributed            Cryptographic protocol verification tools analyze formal
across the entire verification workflow rather than concen-             models of protocols under explicitly defined adversarial
trated at any single stage. While learning a tool’s syntax and          capabilities. Many such tools adopt the symbolic, or Dolev–
underlying formal theory poses an initial hurdle, participants          Yao, model [16], in which cryptographic operations such
consistently identified the most persistent difficulties else-          as encryption and signatures are represented as symbolic
where: validating that a formal model faithfully captures the           functions rather than concrete bit-level computations.
real protocol, debugging proofs that fail to terminate or fail          Cryptographic primitives are assumed to behave ideally: for
without a concrete counterexample, and interpreting sparse              example, an adversary can decrypt an encrypted message
or non-actionable error messages and progress output. We                only when it possesses the required key. Verification therefore
find that programming experience transfers partially, supply-           reasons about which symbolic terms an adversary can derive
ing useful problem-solving strategies such as algorithmic               from its initial knowledge and from messages observed
thinking and case analysis, but does not substitute for the             or generated during protocol execution. This abstraction
domain-specific reasoning that symbolic protocol verifica-              enables automated reasoning about protocols with potentially
tion demands, and that prior exposure to general-purpose                unbounded executions while separating protocol-level
model checkers, while helpful, is not a prerequisite that most          reasoning from computational properties of the underlying
users bring with them. Tool-specific findings further show that         cryptographic primitives. ProVerif and Tamarin are among
Tamarin users frequently rely on manually constructed helper            the most widely adopted tools for performing this type of
lemmas and interactive proof inspection to manage scalabil-             symbolic security protocol analysis.
ity, while ProVerif users report persistent friction modeling           Tamarin [5, 31] models protocol behavior using multiset
stateful protocols, complex algebraic theories, and advanced            rewriting rules and expresses security properties using
properties such as post-compromise security. Across both                first-order logic. Its symbolic reasoning supports equational
tools, participants converge on a consistent set of desired im-         theories and protocols involving mutable state and temporal
provements: mechanisms for validating models against the                relationships between events. Tamarin provides both auto-
protocols they represent, more actionable and localized error           mated and interactive verification. Automated proof search


                                                                    2
can either establish a property or produce a counterexample           inadequate explanations, and weak workflow integration
trace, but termination is not guaranteed. In interactive mode,        as barriers to effective use [14, 27, 36, 43]. Developers also
users can inspect intermediate proof states and dependency            need warnings that explain the cause, security relevance, and
graphs and manually guide the search, including through               possible remediation of a reported problem [46, 47]. Usability
auxiliary or helper lemmas. These characteristics make proof          evaluations consequently report difficulties with navigation,
guidance, non-termination, trace interpretation, and stateful         scalability, alert interpretation, prioritization, and remediation,
modeling particularly relevant to Tamarin’s usability.                while warning presentation and specificity can influence
ProVerif [7, 9, 10] is an automated symbolic protocol verifier        developers’ ability to understand and act on results [34,45,48].
based on the applied pi calculus [1, 2]. It translates protocol       Comparable difficulties have been reported for fuzzing,
models into an abstraction that enables reasoning about an            including setup, configuration, workflow integration, progress
unbounded number of protocol sessions and an unbounded                interpretation, and failure diagnosis [40, 41, 52], and for
message space. The tool supports a range of cryptographic             constant-time analysis tools, where installation, documen-
operations through equational and functional theories and             tation, and output interpretation can hinder routine use [18].
can analyze properties including secrecy, authentication,             Broader studies of developer security practices likewise
and forms of equivalence. ProVerif’s verification engine              emphasize the importance of usable feedback and support for
primarily emphasizes automated analysis. Although it also             recovering from security-relevant mistakes [23, 50]. These
provides an interactive process simulator, this differs from          findings suggest that cryptographic protocol verifiers may face
Tamarin’s workflow for interactively inspecting and guiding           related challenges, compounded by the additional demands of
proof search. Its abstractions can make verification highly           formal modeling, proof construction, and result interpretation.
scalable, but the modeling of features such as mutable state,         Usability and Human Factors in Formal Verification.
complex algebraic properties, equivalence properties, and             Usability concerns have also been identified specifically
state-evolving security guarantees may require additional             in formal security-protocol verification. Garcia and Mod-
modeling choices or workarounds.                                      esti [20] observed that specialized specification languages and
   These differences are important for our study. Both tools          fragmented workflows make protocol-analysis tools difficult
require users to translate an informal protocol into a sym-           to use and proposed an IDE integrating higher-level protocol
bolic representation and interpret the resulting verification         modeling with OFMC and ProVerif. Their subsequent
outcome, but they expose different modeling formalisms and            evaluation found that integrated tooling and abstractions can
proof workflows. We therefore examine both usability chal-            assist users with limited formal-methods or cryptography
lenges shared across cryptographic verifiers and tool-specific        backgrounds, while complexity, training, integration, and
issues arising from Tamarin’s interactive proof process and           interpretation of verification results remain important
ProVerif’s automated abstraction-based analysis.                      obstacles [21]. Braghin et al. [11] similarly identify the
                                                                      specialized languages of tools such as Tamarin and ProVerif
3   Related Work                                                      as an expertise barrier and propose higher-level textual and
                                                                      graphical representations for these verification back ends.
Usability in Cryptographic Software and APIs. Prior                      Broader formal-methods research reinforces these concerns.
work has shown that API design, abstraction, documenta-               Surveys of researchers and practitioners identify ease of use,
tion, defaults, examples, and required security knowledge             training, skills, scalability, tool maturity, and workflow integra-
affect developers’ ability to use cryptographic software se-          tion as persistent adoption challenges [19, 22]. Krishnamurthi
curely [3, 32, 35, 38]. Controlled studies further show that          and Nelson [30] argue for greater attention to the humans
interface design can materially affect security and functional        interacting with formal methods, while Carreira et al. [12]
correctness, while programming experience alone does not              call for research into users’ mental models and understanding
prevent security-relevant API blind spots [3, 37]. Accordingly,       of formal-verification guarantees. Empirical studies also high-
researchers have advocated developer-centered APIs, safer             light difficulties interpreting formal notation and verification
defaults, higher-level abstractions, and contextual guidance          outcomes, debugging failed proofs, and maintaining proofs
that reduce the amount of cryptographic reasoning required            over time; explanatory support can improve users’ understand-
from users [17,23–25]. Similar abstraction and usability prob-        ing and acceptance of verification results [28, 33]. Ter Beek
lems have been observed in Ethereum cryptographic APIs                and Ferrari [49] further note that empirical evaluations of
and in the design and use of cryptographic libraries more             formal-method tools remain comparatively rare and advocate
broadly [39, 44, 51]. Systematization work, however, suggests         greater use of usability and human-subject studies.
that many proposed security-API usability recommendations                Taken together, prior work establishes that effective
still lack extensive empirical validation [38].                       security and formal-verification tools depend not only on
Usability of Security Analysis Tools. Adjacent security-              analytical capability, but also on learnability, appropriate
analysis tools exhibit similar problems. Studies of static            abstractions, actionable feedback, debugging support, and
analysis identify false positives, poor warning prioritization,       alignment with users’ workflows. Existing work has recog-


                                                                  3
nized usability barriers in security-protocol verification and         4.2    Recruitment and Eligibility Criteria
proposed interfaces intended to reduce them, but systematic
empirical evidence about how experienced users interact                We used purposive recruitment to reach participants with
with cryptographic protocol verifiers such as Tamarin and              hands-on experience using cryptographic protocol verifica-
ProVerif remains limited. In particular, little is known about         tion tools in academic or professional settings. Because these
how users learn these tools, how prior programming and                 tools serve a relatively small and specialized community, we
model-checking knowledge transfers to them, how they                   recruited through four complementary channels: academic
assess model fidelity, and how they diagnose and recover from          publications involving protocol verification, public technical
unsuccessful or non-terminating verification attempts. Our             contributions such as protocol models and tool-related reposi-
study addresses these gaps by examining users’ experiences             tories, relevant online research communities, and professional
across the end-to-end verification workflow.                           referrals and snowball sampling. Authors and contributors
                                                                       were identified as potential participants based on evidence of
                                                                       relevant tool use rather than assumed expertise. Recruitment
                                                                       was conducted from May to July 2026. We sent approximately
4     Methodology                                                      100 recruitment invitations by email to potential participants
                                                                       identified through the recruitment channels described above.
                                                                       The invitations included a link to the Qualtrics survey, and
In this section, we provide an overview of the methodology
                                                                       follow-up reminder emails were sent during the recruitment
used in our questionnaire-based survey study. We also discuss
                                                                       period. In total, 24 individuals started the survey. Of these, 16
recruitment and screening procedures, participant eligibility
                                                                       completed the survey and were retained for analysis, while
criteria, and data analysis. To examine the usability of crypto-
                                                                       eight incomplete responses were excluded. Thus, our final
graphic verification tools, we conducted an online survey with
                                                                       sample consisted of 16 participants. Eligibility was based on
participants who had practical experience using these tools
                                                                       self-reported prior experience with cryptographic protocol ver-
in academic or professional contexts. Our goal was to under-
                                                                       ification tools. On the consent page, prospective participants
stand how users interact with cryptographic verification tools,
                                                                       were informed that the study was intended for individuals
the challenges they face during modeling and verification
                                                                       with experience using such tools and were asked to confirm
tasks, and the improvements they believe would make these
                                                                       that they met this requirement before proceeding. Participants
tools more usable. For reference, the survey questionnaire is
                                                                       also reported the specific tools they had used and their level
included in the Appendix A.
                                                                       of experience in the demographic portion of the survey.


4.1    Study Design                                                    4.3    Study Structure
                                                                       We conducted the study using an online survey implemented
We designed the study as an online questionnaire-based sur-            in Qualtrics [42]. The survey was organized into five sections:
vey focused on user experiences with cryptographic verifi-             consent, participant background and tool experience, learn-
cation tools. Because these tools are highly specialized and           ability, modeling and verification, and tool-specific usability
require substantial technical knowledge, we targeted partic-           questions. Conditional display logic was used so that partic-
ipants with direct hands-on experience rather than general             ipants were shown Tamarin and ProVerif specific questions
familiarity with formal methods or security protocols.                 only when they reported prior experience with the correspond-
   The survey was intended to capture both closed-ended and            ing tool. Appendix Figure 3 shows the complete survey flow.
open-ended responses. Closed-ended questions were used to              Consent. The participants were first presented with a consent
collect information about the background of the participants,          page describing the purpose of the study, the procedure, the
tool usage and common usability challenges. Open-ended                 potential risks and benefits, and the participation requirements.
questions allowed participants to describe their experiences in        Only participants who selected “I agree” were allowed to
more detail, including difficulties they encountered, strategies       continue.
they used to overcome those difficulties, and suggestions for          Participant background. Participants reported their current
improving cryptographic verification tools.                            role, experience with cryptographic verification tools, self-
   The study focused on practical usability rather than theoret-       rated expertise, and the specific tools they had used. Their
ical robustness of the tools. In particular, we were interested        tool selections determined which tool-specific sections were
in users’ experiences with learning the tools, writing protocol        subsequently displayed.
models, understanding tool syntax and semantics, interpreting          Learnability. This section examined how participants
error messages or verification results, debugging failed proofs        learned cryptographic verification tools and the difficulties
or models, and integrating these tools into broader research           they encountered. Questions covered learning resources,
or development workflows.                                              prior knowledge, the steepest parts of the learning curve,


                                                                   4
transferable programming concepts, and previous experience               Table 1: Summary of the survey instrument. See Appendix A
with general-purpose model checkers.                                     for the complete questionnaire.
Modeling and verification. Participants were asked about
their confidence in model fidelity, factors limiting that                Section (# Questions)     Sample Questions
confidence, strategies for handling unsuccessful proofs,
                                                                         Demographic (4)           Which of the following verification tools have
communication during slow or non-terminating verification,                                         you used?
and shortcomings in error messages.
Tool-specific usability. Participants with Tamarin experience            Learnability (4)          What resources did you rely on when learning
                                                                                                   the tool? (select all that apply)
received questions concerning counterexample analysis,
scalability, helper lemmas, dependency-graph visualization,              Modeling & Verification   How confident are you that your formal model
modeling difficulty, and desired improvements. Participants              (5)                       accurately reflects the real-world protocol you
with ProVerif experience received questions concerning ob-                                         intend to verify?
servational equivalence, algebraic properties, state-dependent           Tamarin (6)               What is the most important usability
protocols, forward secrecy, post-compromise security, and                                          improvement you would like to see in Tamarin
desired improvements.                                                                              Prover?
   The survey included both closed- and open-ended ques-                 ProVerif (6)              How adequate is ProVerif’s current support for
tions, allowing participants to report specific difficulties, de-                                  reasoning about complex algebraic properties
scribe strategies or workarounds, and suggest improvements.                                        (e.g., Diffie–Hellman, XOR, group equations)?
Table 1 summarizes the survey structure, while Appendix A                                          Please explain your reasoning for your choice.
provides the complete questionnaire.

                                                                         or formalism-level gap rather than a modeling inconvenience),
4.4    Data Analysis                                                     and Not Sure (no opinion expressed). This shared scale al-
We analyzed closed-ended and open-ended survey responses                 lowed us to aggregate and compare adequacy ratings across
using complementary quantitative and qualitative approaches.             properties with different underlying codes, and underlies the
Quantitative analysis. For closed-ended and multiple-choice              response distributions reported in Appendix Tables 2–6.
items, we report descriptive statistics (counts and percentages)            Finally, we conducted a lightweight axial coding pass
across respondents. Because Qualtrics’ conditional display               across the justifications for all five questions to identify cross-
logic showed tool-specific question blocks only to participants          cutting themes that recurred across multiple properties rather
who reported experience with the corresponding tool, and                 than being specific to any single one, such as the manual ef-
because not all participants answered every item, we report              fort required by workarounds, recurring termination concerns,
the applicable n for each question alongside its results.                and comparisons participants drew to Tamarin’s support for
Qualitative coding of open-ended justifications. Several                 algebraic reasoning. These cross-cutting themes inform the
survey items (e.g., Q20–Q24 in the ProVerif block) asked                 synthesis presented alongside individual question results in
participants to rate the adequacy of ProVerif’s support for              Section Results and the discussion in Section RQ3.
a specific security property or protocol feature and to justify          Coding limitations. Open-ended responses were coded by a
that rating in free text. To analyze these justifications system-        single researcher; we did not compute inter-rater reliability,
atically, we developed a codebook through an inductive, data-            and a second coder did not independently verify the coding.
driven process. One researcher read all open-ended responses             Given the relatively small number of free-text responses per
for a given question and derived a set of codes capturing the            question (n = 13 per property) and the exploratory goals of
distinct concerns, caveats, or justifications participants raised,       the study, we treat the resulting codes and themes as a struc-
iteratively refining code definitions and splitting or merging           tured, transparent summary of participants’ stated reasoning
codes as needed until they stably captured the range of                  rather than as a statistically validated coding scheme. The full
responses. Each code was documented with a definition and                codebook, including per-question code definitions, severity-
one or more representative (de-identified) response excerpts,            band mappings, and cross-cutting themes, is included in our
and annotated with the number of respondents assigned to it.             open-science artifacts (see Open Science).
   To enable comparison of perceived adequacy across the
five properties (Q20–Q24), each per-question code was ad-                5     Results
ditionally mapped onto a shared five-level ordinal severity
scale, ranging from Fully Adequate (no significant caveats               5.1     Participants
reported), through Adequate with Minor Limitations and Ad-
equate but Requires Significant Improvement (verifiable in               Our sample (see Appendix Table 8 for details) was predomi-
principle, but only via substantial manual effort, workarounds,          nantly experienced: 12 of 16 participants were academic re-
or careful nonstandard modeling), to Insufficient (a structural          searchers or faculty, two were graduate students, and two were


                                                                     5
industry professionals. Thirteen participants rated themselves              Combinations of learning resources used by participants
as having Advanced or Deep Expertise, and nine reported
                                                                                                                       3.0 3   3
more than six years of experience with security-protocol veri-
fication tools. Thirteen participants had used ProVerif, while
twelve had used Tamarin, with several reporting experience                                                             2.5




                                                                                                   Intersection size
                                                                                                                       2.0         2   2   2
across multiple verification tools.
   These characteristics indicate that our findings primarily                                                          1.5
reflect the experiences of established users rather than novice                                                        1.0                     1   1   1   1
users. This is important when interpreting the results: diffi-                                                         0.5
culties reported in later sections, particularly around model                                                          0.0
validation, proof debugging, and non-termination, persist even
                                                                                 4         Video lectures
among participants with substantial prior experience.
                                                                             9             Peer guidance
                                                                           10              Public models
5.2    Learnability of Cryptographic Verifiers                            12             Research papers
                                                                        16                Documentation
Before users can effectively apply cryptographic verifiers,
they must learn both the tool-specific modeling language                    10       0
                                                                                         N = 16; participants could select multiple resources.
and the formal reasoning style that underlies the verification
process. In this section, we examine how participants learned
cryptographic verification tools, what resources they relied on,       Figure 1: Combinations of learning resources used by partic-
which parts of the learning process they found most difficult,         ipants. Filled circles identify the resources included in each
and what prior programming knowledge helped them become                combination, while the vertical bars show the number of par-
more effective users. Similar to other specialized security            ticipants reporting that combination.
tools, cryptographic verifiers require users to move beyond
ordinary programming or testing workflows and adopt a more
abstract way of representing protocols, adversarial behavior,          resources. Addressing these problems often requires users
and security properties.                                               to inspect proof states, modify models, introduce helper
Learning Resources. Participants reported relying on a com-            lemmas, and experiment with proof strategies. Understanding
bination of official documentation, research papers, publicly          the underlying formal theory, such as applied pi-calculus or
available models, recorded lectures, and guidance from peers           multiset rewriting, was identified by 4 participants (25.0%).
or supervisors when learning cryptographic verification tools.         Two participants (12.5%) reported that translating informal
Figure 1 shows that all 16 participants (100%) used official           protocol descriptions into the tool’s modeling language was
documentation or tool manuals, making this the most com-               the steepest challenge, while only one participant (6.3%)
mon learning resource. Research papers applying the tools to           selected interpreting verification output and attack traces.
real protocols were used by 12 participants (75.0%), while
10 participants (62.5%) relied on publicly available models,             · Takeaway: Although learning challenges occurred across
such as GitHub repositories. Peer or supervisor guidance was             modeling, theory, and result interpretation, non-termination
reported by 9 participants (56.3%), and 4 participants (25%)             and performance debugging emerged as the most frequently
                                                                         reported steepest part of the learning curve. Becoming pro-
used video lectures or summer-school recordings.
                                                                         ficient with a verifier requires learning not only its language
                                                                         and formal foundations, but also how to diagnose and manage
  · Takeaway: Participants relied on multiple complementary              the behavior of its proof search.
  resources rather than a single learning source (see Figure 1),
  combining official documentation with research papers, public
                                                                       Programming concepts that helped. Participants reported
  models, and interpersonal guidance. It indicates that respon-
                                                                       that several programming concepts helped them use crypto-
  dents commonly supplemented official documentation with
  papers, public models, and interpersonal guidance.                   graphic verification tools more effectively. Step-by-step algo-
                                                                       rithmic thinking was the most commonly selected concept,
Steepest part of the learning curve. When asked about                  reported by 11 of 16 participants (68.8%). Pattern matching
the steepest part of the learning curve, 9 participants (56.3%)        and case analysis were selected by seven participants (43.8%),
selected debugging non-termination and performance issues.             while six participants (37.5%) identified recursion and rea-
This indicates that the most significant difficulty is not             soning through repeated structures as helpful.
limited to learning the tool’s syntax or modeling language,              Control flow, higher-order functions, and debugging
but also involves understanding why proof search becomes               skills were each selected by four participants (25.0%).
slow, fails to terminate, or consumes excessive computational          Three participants (18.8%) reported that immutability was


                                                                   6
useful, while one participant (6.3%) selected error handling.          reasonable degree, a meaningful minority (18.8%) remain
Two participants (12.5%) also mentioned other relevant                 only slightly confident, indicating that confidence in model
experience, including knowledge of multiple programming                fidelity is far from uniform across users of these tools.
languages and logic programming.                                          This pattern is consistent with participants’ explanations of
                                                                       what most limits their confidence. The two most frequently
  · Takeaway: Existing programming knowledge can provide               cited factors were the lack of a systematic methodology to
  useful cognitive scaffolding, but cryptographic verifiers can-       validate the model against the real protocol (8, 50%) and
  not assume a single programming background or rely on con-           difficulty modeling stateful or complex protocol behavior (8,
  ventional programming concepts alone. Learning resources             50%), followed by having no way to cross-check the model
  can therefore connect verifier concepts to familiar reasoning        against the actual implementation (7, 43.8%) and concern that
  patterns while explicitly introducing domain-specific abstrac-
                                                                       the symbolic model’s assumption of perfect cryptography may
  tions that do not transfer directly from prior programming
                                                                       not reflect real-world implementation weaknesses (6, 37.5%).
  experience.
                                                                       Fewer participants (3, 18.75%) cited uncertainty about the
Previous use of general-purpose model checkers: Partic-                realism of the Dolev-Yao attacker model, and one participant
ipants were also asked whether they had previously used                additionally identified limitations inherent to symbolic formal
general-purpose model checkers that helped them understand             verification.
verification concepts. Half of the participants (8, 50.0%) re-
                                                                         · Takeaway: The moderate confidence levels reported in
ported no prior experience with such tools. SPIN was the                 Q9 are driven primarily by structural gaps in the verifica-
most commonly used model checker, selected by 4(25.0%),                  tion workflow, namely the absence of validation methodology
followed by Maude with 3(18.8%) and UPPAAL with two par-                 and cross-checking mechanisms against real implementations,
ticipants (12.5%). NuSMV and PRISM were each reported by                 rather than by fundamental doubts about the symbolic model-
one participant (6.3%). Two participants (12.5%) mentioned               ing paradigm or the underlying attacker model.
other formal reasoning tools, including SMT solvers such
as Z3 and Vampire, and the Isabelle theorem prover. Since              Handling proof failures without a concrete attack trace.
participants could report multiple tools, the percentages do           When a proof failed without producing a concrete attack trace,
not sum to 100%.                                                       participants’ most used strategies were simplifying the model
                                                                       to isolate the source of failure, adding helper or auxiliary
  · Takeaway: Interfaces, documentation, and tutorials cannot          lemmas to guide the proof, and re-examining modeling
  assume that new users already understand concepts such as            decisions and abstractions for potential unsoundness. These
  state exploration, formal properties, or counterexample-based        three approaches were selected at identical rates (11, 68.8%),
  reasoning. Cryptographic verification tools must therefore
                                                                       suggesting that experienced users treat proof failures as a
  remain learnable for users entering from security or program-
                                                                       debugging problem to be decomposed methodically rather
  ming backgrounds without previous model-checking experi-
  ence.                                                                than a signal to abandon or restart the model. Increasing
                                                                       computational resources or adjusting tool parameters was
                                                                       also fairly common (6, 37.5%), while consulting published
5.3    Modeling and Verification                                       models or peers (3, 18.75%) and switching tools to cross-
                                                                       validate results (2, 12.5%) were used less frequently, possibly
After learning the tools’ basic syntax and workflow, partici-          reflecting the relative isolation in which many users work
pants still face difficult modeling decisions. Verification de-        or the limited availability of comparable published models.
pends on whether the formal model accurately captures the              Only one participant reported assuming the model was flawed
protocol, its assumptions, and intended security properties.           and rewriting it from scratch, and one participant stated:
We therefore examine participants’ confidence in model fi-
delity, factors limiting that confidence, and strategies used          “Tweak model to consider a less complex case and see
when verification does not proceed as expected.                         what happens”. – P7
Confidence in model accuracy. When asked how confident
they were that their formal model accurately reflects the real-          · Takeaway: Participants addressed proof failures through
world protocol or implementation, participants leaned toward             iterative, model-focused debugging, such as simplifying mod-
moderate-to-high confidence, though with notable spread. The             els, adding auxiliary lemmas, and revisiting assumptions. This
most common response (7, 43.75%) was "Confident", while                  places substantial diagnostic burden on users, suggesting a
the remaining responses were split evenly (3, 18.75%) across             need for better support in identifying problematic model com-
                                                                         ponents and explaining unsuccessful proof search.
"Slightly confident", "Moderately confident", and "Very con-
fident". This distribution yields a mean confidence rating of
approximately 3.6/5 across the 16 respondents, suggesting
that while a majority of participants trust their models to a


                                                                   7
Communication during slow or non-terminating verifi-                    situations, participants with Tamarin experience were asked
cation. Participants’ experiences with tool communication               whether they had encountered false positive counterexamples
during slow or non-terminating verification runs were                   and how they typically resolved them.
predominantly negative. The most frequently selected                       The responses show that the most common strategy was
response (8, 50%) was that the tool hangs silently with no              manually analyzing the counterexample to confirm that it
output or progress indication, followed by the tool producing           was not a real attack, reported by 10 participants (83.3%).
verbose low-level output that is hard to map back to the                Eight participants (66.7%) refined or corrected the protocol
participant’s model (6, 37.5%) and the tool showing generic             model or specification, indicating that false positives often
progress output but nothing specific to the model (5, 31.25%).          result from mismatches between the intended protocol behav-
Fewer participants (3, 18.75%) reported that the tool at least          ior and its formal representation. Two participants adjusted
indicates which rule or lemma is causing the bottleneck,                assumptions about the adversary or environment, while one
though without offering guidance, and only two partici-                 sought help from peers, supervisors, or online communities.
pants(12.5%) described the tool as clearly communicating                One participant reported another recovery approach.
the source of the problem and how to address it. Overall,
most of the selections described feedback as absent, generic,             · Takeaway: The recovery mainly depends on careful trace
or difficult to map back to the model, whereas only two                   interpretation and iterative model refinement. This process can
selections described the tool as clearly communicating both               require considerable expertise, suggesting a need for clearer
the source of the problem and how to address it.                          counterexample explanations and better diagnostic support in
Shortcomings in error messaging. When asked about the                     Tamarin.
most common shortcomings in the tool’s error messaging,
participants most often pointed to the absence of actionable
guidance, with no suggestion or hint on how to fix the issue
                                                                        5.4.2   Scalability and Practical Limitations
being the top-selected shortcoming (9, 56.25%). This was
followed by error messages that do not pinpoint the exact
                                                                        To examine the practical usability of Tamarin beyond small
location of the problem in the model (8, 50%) and semantic
                                                                        examples, participants were asked about the most common
errors that are silently ignored rather than explicitly reported
                                                                        limiting factors they encountered when running larger or more
(7, 43.75%). A smaller number of participants (5, 31.25%)
                                                                        realistic case studies. The response options included memory
noted that error messages assume too much prior knowledge
                                                                        usage, long or non-terminating execution, manual effort re-
of the underlying formal theory or that errors are too low-
                                                                        quired for interactive tracing, tool crashes or instability, not
level and tied to internal tool mechanics rather than the model
                                                                        running large models, and other factors.
itself (3, 18.75%), while only two participants reported no
shortcoming in the tool’s error messaging at all.                          The responses to this question help capture the scalability-
                                                                        related challenges of using Tamarin in practice. While small
  · Takeaway: Taken together with the findings on Q12, these            protocol models may be easier to construct and verify, larger
  results indicate that error and progress messaging represent a        case studies often introduce additional complexity due to a
  substantial usability gap in current cryptographic verification       larger state space, more protocol rules, richer adversary behav-
  tools: participants are frequently left to diagnose both the          ior, and more complex security properties. As a result, users
  location and the cause of a problem largely on their own,             may face limitations not only from computational resources,
  whether that problem manifests as a stalled verification run or       but also from the amount of manual effort required to guide,
  an unclear error message, with silent failures, either through        inspect, or debug the verification process.
  non-termination or unreported semantic errors, emerging as a
                                                                           Manual effort was the most frequently (8, 66.7%) reported
  recurring theme across both questions.
                                                                        limitation. This indicates that larger models often require sub-
                                                                        stantial interactive tracing, inspection, and debugging. Mem-
5.4     Tamarin specific usability                                      ory usage and long or non-terminating execution were each
                                                                        reported by 7 participants (58.3%), showing that computa-
5.4.1   Recovery from false positive counter-example                    tional resource requirements and verification time are also
                                                                        major scalability concerns. Tool crashes or instability were
Tamarin users may sometimes encounter counterexamples
                                                                        reported by 2 participants (16.7%).
that initially appear to represent valid attacks but are later
determined to be false positives. In this study, we use the
                                                                          · Takeaway: Tamarin’s scalability is limited by both compu-
term false positive to refer to a counterexample that does                tational demands and the human effort required to guide and
not correspond to a realistic attack on the intended protocol,            interpret complex verification tasks. Improved automation,
but rather arises from modeling errors, under-specified as-               resource management, and support for interactive analysis
sumptions, abstraction choices, or misunderstandings of the               could therefore make larger case studies more practical.
verification output. To examine how users recover from such


                                                                    8
                                                                                                                              Difficulty of modeling selected features in Tamarin
5.4.3   Reliance on Helper Lemmas.
                                                                                            Stateful protocols            8%            50%                8%         25%         8%


Helper lemmas are intermediate properties used to guide                               Multi-session scenarios                          8%     17%         25%                33%              17%
Tamarin’s proof search, reduce the search space, and support
                                                                                             Forward secrecy                                  9%          36%                           55%
termination when automated reasoning is insufficient. Among
the 12 participants, five (41.7%) reported that they often                       Complex equational theories
                                                                                   (e.g., Diffie-Hellman, XOR)                              33%           17%                42%              8%

needed to write helper lemmas, while three (25.0%) needed
                                                                         Observational equivalence properties           27%          27%                  45%
them almost always. Another three participants (25.0%) re-
                                                                                                             100   75          50           25             0                25               50     75   100
quired them sometimes, and only one (8.3%) rarely relied on                                                                                      Percentage of responses
                                                                                                                                       Very difficult       Neutral              Very easy
them. Overall, eight participants (66.7%) often or almost al-                                                                          Difficult            Easy

ways needed helper lemmas, while 11 (91.7%) required them
at least sometimes.                                                      Figure 2: Participants’ ratings of the difficulty of modeling
                                                                         selected features in Tamarin. Ratings ranged from 1 (Very
  · Takeaway: These findings indicate that successful verifi-            difficult) to 5 (Very easy). Numbers inside the bars indicate
  cation frequently depends on manually constructed interme-             response percentage.
  diate lemmas, requiring users to understand both the protocol
  model and Tamarin’s proof-search behavior. Better automated
  guidance for generating or recommending helper lemmas                  task as easy. Similarly, (7, 58%) of the ratings for stateful pro-
  could therefore reduce manual effort and improve usability.            tocols indicated difficulty, compared with (4, 33%) indicating
                                                                         easy. 11 participants responded to observational equivalence
                                                                         properties.
5.4.4   Usefulness of dependency graph
                                                                            By contrast, forward secrecy received the most favorable
In Tamarin’s interactive mode, the dependency graph visu-                ratings: (6, 55%) of participants rated it as easy, (4, 36%)
alizes the current proof state by showing rule instances and             were neutral, and only 9% rated it as difficult. Multi-session
the dependencies between their premises and conclusions.                 scenarios also received comparatively positive ratings, with
It helps users examine protocol traces, identify unresolved              50% selecting either Easy or Very easy, 25% selecting Neutral,
constraints, and navigate the proof process.                             and 25% reporting difficulty. For complex equational theories,
   Among the 12 participants, four (33.3%) rated the                     including Diffie–Hellman and XOR, half of the responses
dependency graph as intuitive, while one (8.3%) considered it            indicated ease, while 33% indicated difficulty and 17% were
very intuitive. Four participants (33.3%) found it moderately            neutral.
intuitive, indicating that the graph was readable but required
                                                                            · Takeaway: Participants reported the greatest difficulty
effort. Two participants (16.7%) rated it as unintuitive, and
                                                                            with observational equivalence and stateful protocols. For-
one (8.3%) considered it very unintuitive. In general, five
                                                                            ward secrecy was viewed as the most approachable feature,
participants (41.7%) viewed the visualization positively,                   while ratings for multi-session scenarios and complex equa-
while three (25.0%) found it unintuitive or very unintuitive.               tional theories were comparatively favorable but more varied.

  · Takeaway: Participants’ ratings suggest that Tamarin’s de-
  pendency graph is usable for many users but is not uniformly           5.5          ProVerif specific usability
  intuitive. The graph is intended to help users understand and
  navigate complex proof states; if interpreting the visualization       Ratings and representative concerns for Q20–Q24 were de-
  itself requires substantial experience, some of its diagnostic         rived using the coding procedure described in Section 4.4:
  value is lost precisely for users who need additional guidance.        each open-ended justification was assigned an inductively-
  Clearer visual organization, navigation, and explanations of           derived, question-specific code, which was in turn mapped
  proof-state elements could make interactive analysis more              onto a shared five-level adequacy scale (Fully Adequate, Ade-
  accessible.
                                                                         quate with Minor Limitations, Adequate but Requires Signifi-
                                                                         cant Improvement, Insufficient, Not Sure) to allow comparison
5.4.5   Difficulty of modeling protocol features.                        across properties. This shared scale underlies the response
                                                                         distributions reported details in Appendix Tables 2–6.
Participants rated the difficulty of modeling five protocol fea-
tures on a five-point scale ranging from Very difficult to Very          5.5.1          Adequacy of Observational Equivalence Support
easy. As shown in Figure 2, observational equivalence prop-                             (ProVerif)
erties and stateful protocols received the highest proportions
of difficult ratings. For observational equivalence, (6, 54%)            Participants expressed mixed views on ProVerif’s support
of responses were either Very difficult or Difficult, while the          for observational equivalence (i.e., whether an intruder can
remaining (5, 45%) were neutral; no participants rated this              distinguish between two protocols or scenarios). Appendix Ta-


                                                                     9
ble 6 provides the full response distribution and representative        sidered ProVerif’s algebraic support adequate, responses em-
concerns from participants’ free-text justifications.                   phasized that this adequacy is conditional: users must care-
   When asked how adequate ProVerif’s current support for               fully construct equational theories and explicitly account for
observational equivalence is, responses were fairly evenly dis-         properties such as associativity and commutativity, and one
tributed across the scale, with a slight lean toward perceiving         participant noted that termination behavior in the presence of
limitations: four participants rated it insufficient for modern         such theories is not always predictable.
protocols, three rated it adequate but requiring significant im-
provements, two rated it adequate with only minor limitations,            · Takeaway: Together, these results suggest that algebraic
two rated it fully adequate, and two were not sure. Notably, 7            reasoning, particularly involving DH-type and AC equations,
of the 13 respondents (54%) selected one of the two Insuffi-              remains one of the more technically demanding aspects of
cient or Requires Significant Improvement bands, suggesting               modeling in ProVerif, requiring either specialized expertise
                                                                          or acceptance of reduced expressiveness.
that a majority of participants who ventured an opinion see
room for growth in this area.
   The qualitative comments accompanying these ratings                  5.5.3   Support for State-Dependent Protocols
point to a few recurring themes rather than a single shared
complaint. Several participants raised concerns about the gran-         Responses tended to identify limitations in ProVerif’s sup-
ularity and precision of diff-equivalence, describing it as an          port for state-dependent protocols, particularly for complex
over-approximation that is often too coarse or too strong to            stateful designs. Appendix Table 4 reports the full distribu-
capture properties like anonymity, unlinkability, or processes          tion and representative concerns. Responses to Q22 skewed
that differ in more than simple terms. Others pointed to practi-        toward viewing ProVerif’s support for state-dependent proto-
cal limitations, including termination difficulties and a desire        cols as inadequate: four participants rated it insufficient for
for more specific diagnostic explanations when equivalence              complex stateful designs, three rated it adequate but requiring
checks fail, echoing the broader error-messaging concerns               significant improvements, and only two rated it fully adequate.
raised in Q13. A smaller number of participants noted domain-           Combined, 7 of 13 respondents (54%) selected one of the two
specific gaps, such as applicability to IoT and post-quantum            lowest-rated bands. A recurring theme across responses was
computing contexts, or the desire to reason about more than             the reliance on tables as a workaround for modeling state,
two executions for properties like robust declassification. In-         which multiple participants described as usable but unsatis-
terestingly, even among participants who rated the feature as           factory, requiring substantial manual effort, and of uncertain
adequate, one noted that usability depends heavily on deep              scalability to larger protocols. Several participants pointed
prior knowledge of the tool, reinforcing a theme that surfaces          to concrete domains where this limitation is especially acute,
throughout the survey: ProVerif’s core theoretical machinery            such as protocols involving TPMs or IoT devices, and one
may be sound, but its accessibility and diagnostic transparency         noted having to significantly deviate from the original proto-
remain significant barriers for users.                                  col specification simply to achieve termination. Extensions
                                                                        such as GSVerif were mentioned as a partial mitigation, and
                                                                        debugging stateful models was separately flagged as a source
5.5.2   Support for Complex Algebraic Properties
                                                                        of difficulty even when a workable encoding was found. Sev-
Participants generally viewed ProVerif’s support for com-               eral participants also expressed hope that native support for
plex algebraic properties as limited or dependent on careful            mutable state would appear in future tool versions.
modeling. Appendix Table 5 provides the detailed responses
distribution and representative comments.                                 · Takeaway: Respondents reported burdens when encoding
                                                                          richer state evolution using ProVerif’s available mechanisms.
   Participant ratings of ProVerif’s support for complex al-
gebraic properties were mixed but leaned toward identify-
ing limitations: four participants found support limited for            5.5.4   Adequacy of Support for Perfect Forward Secrecy
algebra-heavy designs, three were not sure, three considered
it adequate with careful modeling, and one each rated it fully          Appendix Table 3 summarizes participant ratings of
adequate, prone to false positives, or insufficient and requir-         ProVerif’s support for verifying Perfect Forward Secrecy
ing redesign. The most consistent theme across responses,               (PFS). For Perfect Forward Secrecy, the dominant response
appearing in both the Limited and Requires Redesign codes,              was uncertainty: seven of 13 participants (54%) selected Not
was ProVerif’s lack of native support for AC (associative-              Sure, considerably more than for any other adequacy question
commutative) operators and Diffie–Hellman-type equations,               in the survey. Among participants who did express an opinion,
which participants noted are common in real-world proto-                responses were generally positive, with three rating ProVerif’s
col designs and are better supported in tools like Tamarin;             support fully adequate and two rating it adequate with only
several participants explicitly benchmarked ProVerif against            minor limitations. The concerns raised by these participants
Tamarin on this point. Even among participants who con-                 were relatively narrow in scope, centering on the need to


                                                                   10
carefully model the notion of a compromised “past” state                earlier in Q11. Termination behavior surfaced as an indepen-
and a suggestion that testing a greater number of sessions              dent source of uncertainty across observational equivalence,
could strengthen confidence in verification results. Only one           algebraic properties, and stateful modeling (Q20–Q22), rein-
participant rated support as requiring significant improvement,         forcing the non-termination concerns raised throughout the
noting that modeling PFS still requires ad hoc tricks. The              broader modeling and verification workflow (Q12). Partici-
high proportion of Not Sure responses suggests that, relative           pants also explicitly benchmarked ProVerif against Tamarin,
to other properties surveyed, participants have comparatively           particularly regarding native support for Diffie–Hellman-type
less direct experience modeling Perfect Forward Secrecy in              and AC-operator reasoning (Q21), and raised domain-specific
ProVerif, which limits how strongly conclusions about its               applicability concerns for IoT, TPM, and post-quantum set-
adequacy can be drawn from this sample.                                 tings (Q20, Q22). Several participants expressed hope for
                                                                        native support of currently unsupported features, such as mu-
                                                                        table global state, in future tool versions (Q22, Q24), while
5.5.5   Support for Post-Compromise Security
                                                                        others pointed to existing published models (e.g., for Signal)
Participant ratings of ProVerif’s support for post-compromise           as evidence that even demanding properties can be verified
security, which requires reasoning about state evolution are            given sufficient effort (Q24).
shown in Appendix Table 2. As with Perfect Forward Secrecy,
uncertainty dominated responses regarding post-compromise                 · Takeaway: Participants’ concerns about ProVerif extend
security, with seven of 13 participants (54%) selecting Not               beyond any single security property to shared structural limita-
Sure. Among the remaining participants, opinions were split               tions, namely termination predictability, native algebraic and
                                                                          state support, and the manual effort required to work around
evenly between viewing ProVerif’s support as workable and
                                                                          their absence.
viewing it as insufficient: two participants rated it adequate
with careful modeling, citing existing models for protocols
such as Signal as evidence of feasibility while explicitly not-         5.5.7   Desired Features and Improvements for ProVerif
ing that such models require substantial manual effort to con-
struct, and two rated it insufficient for modern ratcheting pro-        When asked which features or improvements would most
tocols, with one hoping that related overfitting issues would           increase their productivity with ProVerif, participants most
be addressed in future updates despite acknowledging this               frequently selected a model validation mechanism to check
as a hard problem. Only one participant rated support as fully          whether the formal model matches the intended protocol (n =
adequate, and one rated it adequate but limited specifically for        10), followed by an interactive debugging mode allowing step-
dynamic recovery scenarios, noting that this remains difficult          by-step inspection of the proof state (n = 8) and a graphical in-
to model in a straightforward way. The high rate of uncertainty         terface for model visualization and attack trace exploration (n
for Q24 suggests that many participants had limited direct              = 6). Improved documentation with realistic, well-annotated
experience modeling post-compromise security in ProVerif.               protocol examples was also fairly commonly selected (n =
Participants who did express an opinion frequently empha-               5), while integration with standard development tools such
sized the modeling effort required. These responses should              as IDE plugins or CI/CD pipelines (n = 3) and automated
therefore be interpreted as usability judgments rather than             suggestions for fixing common modeling mistakes (n = 3)
bounds on ProVerif’s technical capabilities. Recent work [13]           were selected less frequently. Two participants used the open-
has demonstrated a highly automated ProVerif-based analysis             ended option to specifically request automated generation of
of Signal’s Double Ratchet that reasons about key compro-               helper lemmas.
mise and proves post-compromise security in the analyzed                   This ranking of desired improvements aligns closely with
model, showing that sophisticated PCS verification is possible          limitations identified elsewhere in the survey. The top-ranked
while potentially requiring specialized modeling expertise.             request, a model validation mechanism, directly mirrors the
                                                                        leading concerns raised in Q10, where the lack of a systematic
5.5.6   Cross-Cutting Themes in ProVerif Adequacy                       methodology to validate the model against the real protocol
                                                                        and the inability to cross-check the model against the actual
Beyond the property-specific concerns above, our axial cod-             implementation were among the most commonly cited lim-
ing pass across Q20–Q24 identified several themes that re-              its on confidence. Similarly, the demand for an interactive
curred across multiple properties rather than being specific            debugging mode and a graphical interface for trace explo-
to any single one. Manual effort was repeatedly cited as the            ration reflects the debugging-heavy troubleshooting strategies
qualifier that separates a nominally adequate feature from              reported in Q11 and the recurring complaints in Q12 and
a practically usable one, appearing in participants’ justifica-         Q13 about silent failures and unhelpful error messages. The
tions for complex algebraic properties (Q21), state-dependent           relatively lower demand for IDE or CI/CD integration and
protocols (Q22), and post-compromise security (Q24), and                automated mistake-fixing suggests that participants’ priorities
echoing the workaround-heavy debugging strategies reported              center less on tooling convenience and more on fundamental


                                                                   11
gaps in validation, transparency, and debuggability.                   guiding proofs, diagnosing non-termination, and interpreting
                                                                       results remain largely the user’s responsibility, so effective
    · Takeaway: Users are less concerned with ProVerif fitting         use depends on substantial formal-methods expertise, which
    into modern development workflows than with being able to          may limit accessibility and wider adoption.
    trust and understand the models and proofs it produces.

                                                                       7   RQ2: Perceived Transfer of Programming
6     RQ1: Usability Barriers in Cryptographic                             and Model-Checking Knowledge
      Protocol Verification Tools                                      Transferable programming strategies. Prior programming
                                                                       experience transfers mainly through general problem-solving
Barriers across the verification workflow. Usability
                                                                       strategies. Participants drew on step-by-step algorithmic
barriers occur throughout the verification workflow rather
                                                                       reasoning, pattern matching, case analysis, recursion, and de-
than at a single stage. Learning specialized syntax and formal
                                                                       bugging when constructing and analyzing models, supporting
theory is challenging, but the more persistent difficulties
                                                                       decomposition, reasoning about alternative execution paths,
arise during model construction, proof management, and
                                                                       and diagnosis. However, no single concept was universally
interpreting outcomes: translating informal protocols into
                                                                       essential, and programming experience does not fully prepare
suitable symbolic abstractions, judging whether those
                                                                       users for symbolic reasoning, unbounded sessions, attacker
abstractions are accurate, and managing proof searches that
                                                                       knowledge, equational theories, or interpreting formal
may stall or fail to terminate.
                                                                       security guarantees, so users must adapt familiar reasoning
Model fidelity and validation. A central barrier is confidence
                                                                       to a substantially different setting.
in model fidelity. Even confident participants reported limited
                                                                       Model checking as a conceptual bridge. Prior experience
support for systematically validating a formal model against
                                                                       with general-purpose model checkers may provide a more
the original protocol or implementation, a gap between
                                                                       direct bridge: familiarity with state exploration, property
verifying a representation and establishing that it faithfully
                                                                       specification, and counterexamples helps users understand
captures the real system. Difficulty representing stateful
                                                                       the broader purpose and behavior of cryptographic verifiers.
and complex behavior widens this uncertainty, particularly
                                                                       However, half of participants had no such experience, so this
when the verifier requires workarounds that diverge from the
                                                                       background is helpful but not a prerequisite, and verifiers
original specification.
                                                                       cannot assume new users already understand these concepts.
Proof debugging and diagnostic feedback. Proof failures
                                                                       Limits of knowledge transfer. Cryptographic verification
impose a substantial manual debugging burden. Users typ-
                                                                       introduces domain-specific concepts not typically found in
ically respond by simplifying models, revisiting assumptions,
                                                                       conventional programming or model checking, including sym-
and introducing helper lemmas, work that requires under-
                                                                       bolic adversary models, cryptographic term algebras, protocol-
standing both the protocol and the verifier’s proof-search
                                                                       specific security properties, and formalisms such as multiset
behavior. Limited progress information and non-actionable
                                                                       rewriting and the applied pi calculus. Prior knowledge may
error messages compound this: silent hangs, low-level
                                                                       clarify the shape of the verification task, but does not eliminate
internal output, or unlocalized errors leave users to diagnose
                                                                       the need to learn these specialized theories and conventions.
problems largely through experimentation and prior expertise.
                                                                       Implications for onboarding. Programming and model-
Tool-specific modeling and proof challenges. Tool-specific             checking knowledge together provide a helpful but
findings reinforce these broader barriers. Tamarin users               incomplete foundation: programming contributes transferable
frequently depend on helper lemmas, interactive proof guid-            reasoning and debugging strategies, while model checking
ance, and manual counterexample analysis; its dependency               provides familiarity with verification concepts and workflows.
graph can support expert analysis but may require substantial          Neither fully addresses the specialized abstractions and
experience to interpret, and modeling stateful protocols or            proof-management demands of cryptographic protocol
observational equivalence remains especially demanding.                analysis, so onboarding materials should explicitly connect
ProVerif participants identified similar difficulties with             familiar concepts to their verification counterparts while
state-dependent protocols, complex algebraic properties, and           supporting users without prior formal-methods experience.
observational equivalence, properties that workarounds can
represent only at the cost of significant manual effort and
reduced fidelity to the original protocol.                             8   RQ3: Usability, Design, and Functional Im-
Gap between protocol reasoning and verifier behavior.                      provements
The main usability challenge is therefore not learning to
operate a verifier, but managing the gap between the user’s            Improving these tools requires more than simplifying syntax
protocol-level reasoning and the tool’s formal representation,         or modernizing interfaces. Participants prioritized reducing
proof procedures, and diagnostic output. Validating models,            uncertainty during model construction, making proof behavior


                                                                  12
transparent, and strengthening support for diagnosing unsuc-            examples across tools for non-termination, false coun-
cessful verification. Across both tools, the most important             terexamples, helper lemmas, and stateful or equivalence
needs concerned model validation, actionable diagnostics,               properties. Tooling support could include syntax-aware
counterexample explanation, interactive debugging, and as-              editors, inline diagnostics, navigation between models and
sistance with complex proof tasks. An overview appears in               counterexample traces, and state-transition visualization.
Appendix Table 7.                                                       IDE and CI/CD integration was a lower priority (three
Model construction and validation support. A model-                     respondents), suggesting adoption is currently constrained
validation mechanism was the most requested ProVerif                    more by validation, interpretability, and debuggability than
improvement, helping users compare formal models with                   by workflow convenience; integration is likely to matter more
protocol descriptions, identify omitted assumptions, and link           once users can trust the verification process.
model elements to implementation behavior. It would not                 Functional support for complex protocols and properties.
guarantee correctness but could reduce mismatches between               Some barriers require changes beyond interfaces or documen-
the verified model and the intended protocol.                           tation. For Tamarin, participants wanted stronger support for
Error feedback and counterexample explanation. For                      stateful protocols, observational equivalence, proof scalability,
Tamarin, error feedback and counterexample explanation                  and interactive analysis; for ProVerif, improvements to
were the top requests (eight responses each). Participants              mutable state, ordered transitions, complex algebraic theories,
wanted diagnostics that identify the relevant rule, lemma,              observational equivalence, and properties involving state
query, or construct and explain possible causes and fixes,              evolution such as post-compromise security. Addressing
with counterexamples summarized at the protocol level so                these may require changes to the underlying frameworks,
genuine attacks can be distinguished from modeling errors               reducing reliance on workarounds that increase manual effort
or abstraction artifacts.                                               and distance the model from the original protocol.
Interactive debugging and visualization. Interactive
debugging and visualization could reduce the manual effort
needed to understand verification behavior. Eight ProVerif
                                                                        9    Acknowledgments
participants wanted step-by-step proof-state inspection,
                                                                        We thank all survey participants for generously contributing
and six wanted a graphical interface for model and trace
                                                                        their time and sharing their experiences and perspectives. We
exploration. Such interfaces should connect internal proof
                                                                        are particularly grateful to Qifan Zhang of Palo Alto Networks
operations to the user’s original protocol representation,
                                                                        and Zilin Shen of Purdue University for participating in the
letting users trace attacker knowledge, identify unresolved
                                                                        pilot survey and providing valuable feedback that informed
branches, and locate where search becomes unmanageable.
                                                                        the refinement and finalization of the questionnaire. Their
For Tamarin, this means clearer dependency-graph layouts,
                                                                        input helped improve the clarity, relevance, and overall quality
better navigation, and stronger interactive/proof-oracle sup-
                                                                        of the survey instrument.
port for case distinctions; for ProVerif, an interactive mode
for examining failed queries and diagnosing non-termination
that is currently hard to infer from static output.                     10    Conclusion
Automation and proof guidance. Tamarin users frequently
depend on manually written helper lemmas and case distinc-              We presented an exploratory survey of 16 experienced
tions, and two ProVerif respondents requested automated                 users of cryptographic protocol verification tools, including
lemma generation. Future tools could analyze recurring                  Tamarin and ProVerif. Participants reported challenges
proof patterns to recommend intermediate lemmas, case                   in validating whether formal models faithfully represent
distinctions, model simplifications, or alternative strategies,         intended protocols, diagnosing slow or non-terminating
and detect modeling mistakes or abstractions that produce               verification, and interpreting unsuccessful proofs and tool
false counterexamples or non-termination. AI-assisted func-             feedback. Prior programming and model-checking experience
tionality could also synthesize counterexamples, summarize              provided useful reasoning strategies but did not replace the
proof states, and explain unresolved branches, but such                 domain-specific knowledge required for symbolic protocol
recommendations should remain transparent and reviewable,               verification. Across tools, participants emphasized the need
supporting rather than obscuring the formal basis of the result.        for better model-validation support, actionable diagnostics,
Documentation and tooling support. Documentation                        clearer explanations of verification outcomes, interactive
and tooling support were each selected by five Tamarin                  debugging, and greater automation of recurring proof tasks.
participants, and five ProVerif respondents wanted improved,               Our findings should be interpreted in light of the study’s
realistic, well-annotated examples. Traditional reference               small, self-selected, and predominantly experienced sample
manuals appear insufficient alone; documentation should                 and its reliance on self-reported rather than observed tool use.
explain modeling choices, rejected alternatives, common                 Overall, improving cryptographic verifiers requires reducing
mistakes, and debugging steps, ideally with comparative                 the gap between users’ protocol-level reasoning and the tools’


                                                                   13
formal representations and proof procedures. Future work               considered re-identification and associated professional
should evaluate these needs through observational studies and          or reputational harm to be the primary risks and therefore
concrete mechanisms for model validation, proof guidance,              limited the disclosure and linkage of participant-specific
and explanation.                                                       information; (2) Tool developers and maintainers: are also
                                                                       affected because our findings identify perceived limitations
                                                                       and recommend changes to existing tools. We therefore
Ethical Considerations
                                                                       distinguish participants’ reported experiences from objective
Human Subjects and Informed Consent. This study                        technical deficiencies and avoid attributing usability problems
involved an online questionnaire with researchers, graduate            or design trade-offs to individual developers; (3) Current and
students, and industry practitioners who had hands-on                  prospective users: may benefit from improved diagnostics,
experience with cryptographic protocol verification tools.             model-validation support, documentation, visualization,
The study was reviewed and approved by the relevant                    and proof guidance, while inaccurate or overly broad
Institutional Review Board (IRB). Before beginning the                 interpretations of our findings could give users misleading
survey, participants were presented with a consent form                expectations about the capabilities or limitations of particular
describing the purpose and scope of the study, the survey              tools; (4) The broader security and formal-methods research
procedure, potential risks and benefits, and other information         community: may use these findings to inform future tool
relevant to participation. Participants could proceed with the         design and human-centered research. Because our evidence is
survey only after explicitly providing consent by selecting            based on a small, specialized, self-selected sample, we avoid
the “I agree” option; participants who selected “I disagree”           claiming that the reported experiences are representative of
were not permitted to continue.                                        all users of cryptographic verification tools.
Participant Privacy and Confidentiality. Because cryp-                 Responsible Characterization of Tools and Findings.
tographic protocol verification is a relatively small and              Our study examines users’ experiences with cryptographic
specialized research community, combinations of profes-                verification tools rather than evaluating the competence or
sional role, experience, tool usage, research activities, or           intentions of their developers. Some challenges reported by
qualitative responses could potentially make individual                participants, including non-termination, limitations in model-
participants identifiable even after direct identifiers are            ing particular protocol features, or difficulties associated with
removed. This creates potential professional or reputational           specific abstractions, may arise from fundamental properties
risks, particularly when participants describe difficulties            or design trade-offs of the underlying verification approaches
they encountered, limitations of particular tools, or their            rather than straightforward software defects. We therefore
own verification practices. To mitigate these risks, we                distinguish between participants’ reported experiences, our
refer to participants using anonymous identifiers, remove              interpretation of those experiences, and objective claims
potentially identifying details from quoted responses, and             about a tool’s technical capabilities. Similarly, difficulty using
avoid reporting project-specific information that could reveal         a verification tool should not be interpreted as evidence of
participant identities. We also avoid unnecessarily linking            insufficient expertise on the part of an individual participant.
qualitative responses with detailed participant characteristics        Our goal is to identify opportunities for improving usability
when such combinations could increase re-identification risk.          and supporting users rather than assigning responsibility for
Data Protection and Reporting. Survey responses were col-              the difficulties reported.
lected through Qualtrics and stored securely for research pur-         Respect for Law and Public Interest. The study consisted of
poses. We report quantitative results primarily in aggregate           a questionnaire about participants’ experiences with crypto-
and use de-identified excerpts when presenting qualitative             graphic protocol verification tools and did not involve probing
responses. Because the participant population is specialized           deployed systems, exploiting vulnerabilities, or interacting
and some combinations of demographic characteristics and               with third-party systems without authorization. The survey
tool experience may be distinctive, we take particular care            focused on participants’ learning experiences, modeling and
when reporting participant-level information. Any materials            verification workflows, difficulties encountered during proof
released alongside the paper will be reviewed to ensure that           construction and debugging, and desired improvements to
they do not expose direct identifiers or combinations of infor-        existing tools. We avoid reporting identifying project details
mation that could reasonably facilitate re-identification.             or other information that could create unnecessary risks to
Affected Stakeholders. We identify the following primary               participants or third parties. The expected public benefit of
stakeholder groups that may be affected by our work: (1)               this research is a better understanding of the usability barriers
Study participants: are the primary stakeholders because               surrounding cryptographic protocol verification and the iden-
they provided potentially sensitive descriptions of their              tification of design priorities that may help researchers and
expertise, workflows, difficulties, and opinions about                 practitioners construct, debug, interpret, and validate formal
particular verification tools. Given the relatively small              protocol models more effectively.
and specialized cryptographic-verification community, we               Responsible Interpretation and Generalization. Partici-


                                                                  14
pants were recruited from a specialized community through                  [3] Yasemin Acar, Michael Backes, Sascha Fahl, Simson
academic publications, open-source contributions, commu-                       Garfinkel, Doowon Kim, Michelle L. Mazurek, and
nity outreach, professional contacts, referrals, and snowball                  Christian Stransky. Comparing the usability of cryp-
sampling. Participation was voluntary, and the recruitment                     tographic apis. In 2017 IEEE Symposium on Secu-
strategy may introduce self-selection bias. The study also                     rity and Privacy (SP), pages 154–171, 2017. doi:
relies on participants’ self-reported experiences rather than                  10.1109/SP.2017.52.
direct observation of their verification activities. We therefore
                                                                           [4] Apple Security Engineering and Architecture (SEAR).
interpret the findings as evidence about the experiences and
                                                                               iMessage with PQ3: The new state of the art in quantum-
practices reported by our participants and do not claim that the
                                                                               secure messaging at scale, February 2024. Accessed:
results are statistically representative of all Tamarin, ProVerif,
                                                                               2026-07-03. URL: https://security.apple.com/
or cryptographic-verification users.
                                                                               blog/imessage-pq3/.
                                                                           [5] David Basin, Cas Cremers, Jannik Dreier, Simon Meier,
Open Science                                                                   Ralf Sasse, and Benedikt Schmidt. Tamarin prover,
                                                                               2026.    Accessed April 2026.      URL: https://
To support transparency, reproducibility, and evaluation
                                                                               tamarin-prover.github.io/.
of our study, we make the study materials and analysis
artifacts publicly available. During the anonymous review                  [6] Karthikeyan Bhargavan, Bruno Blanchet, and Nadim
period, these materials are available through an anonymized                    Kobeissi. Verified models and reference implementa-
repository at https://anonymous.4open.science/r/                               tions for the tls 1.3 standard candidate. In 2017 IEEE
protocol-verifier-usability-artifact-6625/. The                                Symposium on Security and Privacy (SP), pages 483–
research artifacts associated with this study are:                             502, 2017. doi:10.1109/SP.2017.26.

   • Survey questionnaire                                                  [7] B. Blanchet. An efficient cryptographic protocol veri-
                                                                               fier based on prolog rules. In Proceedings. 14th IEEE
   • Consent form                                                              Computer Security Foundations Workshop, 2001., pages
                                                                               82–96, 2001. doi:10.1109/CSFW.2001.930138.
   • Codebook
                                                                           [8] Bruno Blanchet. Automatic verification of security pro-
Materials Shared: We include the complete questionnaire                        tocols in the symbolic model: The verifier proverif. In
used in the study, including the consent information. We also                  International School on Foundations of Security Analy-
share the lightweight codebook used to analyze the explana-                    sis and Design, pages 54–87. Springer, 2012.
tory free-text responses, with codes, definitions, and example             [9] Bruno Blanchet. ProVerif: Cryptographic Protocol Veri-
quotes that we coded for each code.                                            fier in the Formal Model, 2023. Accessed April 2026.
Materials Not Shared: We do not publicly release the raw                       URL: https://bblanche.gitlabpages.inria.fr/
Qualtrics response data. Although the survey did not in-                       proverif/.
tentionally collect direct personally identifiable information,
the cryptographic-verification community is relatively small              [10] Bruno Blanchet, Ben Smyth, and Vincent Cheval.
and specialized, and combinations of response content and                      Proverif 2.05: Automatic cryptographic protocol verifier,
survey metadata could increase the risk of participant re-                     user manual and tutorial, 2026. Accessed April 2026.
identification. To minimize this risk and preserve participant                 URL: https://bblanche.gitlabpages.inria.fr/
anonymity, we share only de-identified, processed, and aggre-                  proverif/manual.pdf.
gated data necessary to support the analyses reported in this             [11] Chiara Braghin, Mario Lilli, and Elvinia Riccobene.
paper, rather than the original Qualtrics export.                              Aprover front-end modelling language for designing se-
                                                                               curity protocols. SN Computer Science, 6(8):992, 2025.
References                                                                [12] Carolina Carreira, Joao F Ferreira, Alexandra Mendes,
                                                                               and Nicolas Christin. Exploring usable security to
 [1] Martín Abadi, Bruno Blanchet, and Cédric Fournet. The                     improve the impact of formal verification: a research
     applied pi calculus: Mobile values, new names, and                        agenda. arXiv preprint arXiv:2111.08209, 2021.
     secure communication. J. ACM, 65(1), 2017. doi:
     10.1145/3127586.                                                     [13] Vincent Cheval, Charlie Jacomme, and Jessica Richards.
                                                                               Automated formal analysis of signal’s double ratchet:
 [2] Martín Abadi and Cédric Fournet. Mobile values, new                       Attacks, fixes and security proofs. In 2026 IEEE Sym-
     names, and secure communication. ACM Sigplan No-                          posium on Security and Privacy (SP), pages 1522–1538,
     tices, 36(3):104–115, 2001.                                               2026. doi:10.1109/SP63933.2026.00120.


                                                                     15
[14] Maria Christakis and Christian Bird. What develop-               [24] Peter Leo Gorski, Luigi Lo Iacono, Dominik Wermke,
     ers want and need from program analysis: an empirical                 Christian Stransky, Sebastian Möller, Yasemin Acar, and
     study. In Proceedings of the 31st IEEE/ACM interna-                   Sascha Fahl. Developers deserve security warnings,
     tional conference on automated software engineering,                  too: On the effect of integrated security advice on cryp-
     pages 332–343, 2016.                                                  tographic API misuse. In Fourteenth Symposium on
                                                                           Usable Privacy and Security (SOUPS 2018), pages 265–
[15] Cas Cremers, Marko Horvat, Sam Scott, and Thyla Van                   281, Baltimore, MD, August 2018. USENIX Associa-
     Der Merwe. Automated analysis and verification of tls                 tion. URL: https://www.usenix.org/conference/
     1.3: 0-rtt, resumption and delayed authentication. In                 soups2018/presentation/gorski.
     2016 IEEE Symposium on Security and Privacy (SP),
     pages 470–485. IEEE, 2016.                                       [25] Matthew Green and Matthew Smith. Developers are not
                                                                           the enemy!: The need for usable security apis. IEEE
[16] Danny Dolev and Andrew Yao. On the security of public                 Security & Privacy, 14(5):40–46, 2016. doi:10.1109/
     key protocols. IEEE Transactions on information theory,               MSP.2016.111.
     29(2):198–208, 1983.
                                                                      [26] A Hassan, I Ishaq, J Munilla, AU Ardelia, CF Fan-
[17] Ehsan Firouzi, Ammar Mansuri, Mohammad Ghafari,                       gasadha, R Widuri, and V Polepally. Evaluating formal
     and Maziar Kaveh. From struggle to simplicity with a                  methods for verifying security protocols: a case study
     usable and secure api for encryption in java. In Proceed-             of tamarin, avispa, and proverif. Journal of Theoreti-
     ings of the 18th ACM/IEEE International Symposium                     cal and Applied Information Technology, 103(5):1597–
     on Empirical Software Engineering and Measurement,                    1614, 2025.
     pages 556–565, 2024.
                                                                      [27] Brittany Johnson, Yoonki Song, Emerson Murphy-Hill,
[18] Marcel Fourné, Daniel De Almeida Braga, Jan Jancar,
                                                                           and Robert Bowdidge. Why don’t software develop-
     Mohamed Sabt, Peter Schwabe, Gilles Barthe, Pierre-
                                                                           ers use static analysis tools to find bugs? In 2013
     Alain Fouque, and Yasemin Acar. " these results must be
                                                                           35th International Conference on Software Engineer-
     false": A usability evaluation of constant-time analysis
                                                                           ing (ICSE), pages 672–681, 2013. doi:10.1109/ICSE.
     tools. In 33rd USENIX Security Symposium (USENIX
                                                                           2013.6606613.
     Security 24), pages 6705–6722, 2024.

[19] Hubert Garavel, Maurice H Ter Beek, and Jaco Van                 [28] Arut Prakash Kaleeswaran, Arne Nordmann, Thomas
     De Pol. The 2020 expert survey on formal methods. In                  Vogel, and Lars Grunske. A user study for evaluation of
     International Conference on Formal Methods for Indus-                 formal verification results and their explanation at bosch.
     trial Critical Systems, pages 3–69. Springer, 2020.                   Empirical Software Engineering, 28(5):125, 2023.

[20] Rémi Garcia and Paolo Modesti. An ide for the design,            [29] Nadim Kobeissi, Karthikeyan Bhargavan, and Bruno
     verification and implementation of security protocols.                Blanchet. Automated verification for secure messag-
     In 2017 IEEE International Symposium on Software Re-                  ing protocols and their implementations: A symbolic
     liability Engineering Workshops (ISSREW), pages 157–                  and computational approach. In 2017 IEEE European
     163. IEEE, 2017.                                                      Symposium on Security and Privacy (EuroS&P), pages
                                                                           435–450, 2017. doi:10.1109/EuroSP.2017.38.
[21] Rémi Garcia and Paolo Modesti. A practical approach
     to formal methods: An eclipse integrated development             [30] Shriram Krishnamurthi and Tim Nelson. The human in
     environment (ide) for security protocols. Electronics,                formal methods. In International Symposium on Formal
     13(23):4660, 2024.                                                    Methods, pages 3–10. Springer, 2019.

[22] Mario Gleirscher and Diego Marmsoler. Formal meth-               [31] Simon Meier, Benedikt Schmidt, Cas Cremers, and
     ods in dependable systems engineering: a survey of                    David Basin. The tamarin prover for the symbolic analy-
     professionals from europe and north america. Empirical                sis of security protocols. In International conference on
     Software Engineering, 25(6):4473–4546, 2020.                          computer aided verification, pages 696–701. Springer,
                                                                           2013.
[23] Peter Leo Gorski, Yasemin Acar, Luigi Lo Iacono, and
     Sascha Fahl. Listen to developers! a participatory design        [32] Kai Mindermann, Philipp Keck, and Stefan Wagner.
     study on security warnings for cryptographic apis. In                 How usable are rust cryptography apis? In 2018 IEEE
     Proceedings of the 2020 CHI Conference on Human                       International Conference on Software Quality, Reliabil-
     Factors in Computing Systems, pages 1–13, 2020.                       ity and Security (QRS), pages 143–154. IEEE, 2018.


                                                                 16
[33] Eric Mugnier, Yuanyuan Zhou, Ranjit Jhala, and Michael           [41] Stephan Plöger, Mischa Meier, and Matthew Smith. A
     Coblenz. On the impact of formal verification on soft-                usability evaluation of afl and libfuzzer with cs students.
     ware development. Proceedings of the ACM on Pro-                      In Proceedings of the 2023 CHI Conference on Human
     gramming Languages, 9(OOPSLA2):3642–3668, 2025.                       Factors in Computing Systems, pages 1–18, 2023.

[34] Marcus Nachtigall, Michael Schlichtig, and Eric Bodden.          [42] Qualtrics. Accessed: 2026-07-29. URL: https://www.
     A large-scale study of usability criteria addressed by                qualtrics.com/.
     static analysis tools. In Proceedings of the 31st ACM            [43] Caitlin Sadowski, Edward Aftandilian, Alex Eagle, Liam
     SIGSOFT International Symposium on Software Testing                   Miller-Cushon, and Ciera Jaspan. Lessons from building
     and Analysis, pages 532–543, 2022.                                    static analysis tools at google. Communications of the
                                                                           ACM, 61(4):58–66, 2018.
[35] Sarah Nadi, Stefan Krüger, Mira Mezini, and Eric Bod-
     den. Jumping through hoops: why do java develop-                 [44] Juliane Schmüser, Philip Klostermeyer, Kay Friedrich,
     ers struggle with cryptography apis? In Proceedings                   and Sascha Fahl. “i’m pretty expert and i still screw it
     of the 38th International Conference on Software En-                  up”: Qualitative insights into experiences and challenges
     gineering, ICSE ’16, page 935–946, New York, NY,                      of designing and implementing cryptographic library
     USA, 2016. Association for Computing Machinery.                       apis. In 2025 IEEE Symposium on Security and Privacy
     doi:10.1145/2884781.2884790.                                          (SP), pages 2322–2340. IEEE, 2025.

[36] Lisa Nguyen Quang Do, James Wright, and Karim Ali.               [45] Justin Smith, Lisa Nguyen Quang Do, and Emerson
     Why do software developers use static analysis tools? a               Murphy-Hill. Why can’t johnny fix vulnerabilities: A
     user-centered study of developer needs and motivations.               usability evaluation of static analysis tools for security.
     IEEE Transactions on Software Engineering, 48:835–                    In Sixteenth Symposium on Usable Privacy and Secu-
     847, 03 2022. doi:10.1109/TSE.2020.3004525.                           rity (SOUPS 2020), pages 221–238. USENIX Associa-
                                                                           tion, August 2020. URL: https://www.usenix.org/
[37] Daniela Seabra Oliveira, Tian Lin, Muhammad Sajidur                   conference/soups2020/presentation/smith.
     Rahman, Rad Akefirad, Donovan Ellis, Eliany Perez,               [46] Justin Smith, Brittany Johnson, Emerson Murphy-Hill,
     Rahul Bobhate, Lois A. DeLong, Justin Cappos, and                     Bill Chu, and Heather Richter Lipford. Questions devel-
     Yuriy Brun. API blindspots: Why experienced develop-                  opers ask while diagnosing potential security vulnera-
     ers write vulnerable code. In Fourteenth Symposium on                 bilities with static analysis. In Proceedings of the 2015
     Usable Privacy and Security (SOUPS 2018), pages 315–                  10th Joint Meeting on Foundations of Software Engi-
     328, Baltimore, MD, August 2018. USENIX Associa-                      neering, ESEC/FSE 2015, page 248–259, New York,
     tion. URL: https://www.usenix.org/conference/                         NY, USA, 2015. Association for Computing Machinery.
     soups2018/presentation/oliveira.                                      doi:10.1145/2786805.2786812.
[38] Nikhil Patnaik, Andrew C Dwyer, Joseph Hallett, and              [47] Justin Smith, Brittany Johnson, Emerson Murphy-Hill,
     Awais Rashid. Don’t forget your classics: Systematizing               Bill Chu, and Heather Richter Lipford. How developers
     45 years of ancestry for security api usability recommen-             diagnose potential security vulnerabilities with a static
     dations. arXiv preprint arXiv:2105.02031, 2021.                       analysis tool. IEEE Transactions on Software Engineer-
                                                                           ing, 45(9):877–897, 2019. doi:10.1109/TSE.2018.
[39] Nikhil Patnaik, Joseph Hallett, and Awais Rashid. Us-                 2810116.
     ability smells: An analysis of Developers’ struggle
     with crypto libraries. In Fifteenth Symposium on Us-             [48] Mohammad Tahaei, Kami Vaniea, Konstantin Beznosov,
     able Privacy and Security (SOUPS 2019), pages 245–                    and Maria K Wolters. Security notifications in static
     257, Santa Clara, CA, August 2019. USENIX Associa-                    analysis tools: Developers’ attitudes, comprehension,
     tion. URL: https://www.usenix.org/conference/                         and ability to act on them. In Proceedings of the 2021
     soups2019/presentation/patnaik.                                       CHI Conference on Human Factors in Computing Sys-
                                                                           tems, pages 1–17, 2021.
[40] Stephan Plöger, Mischa Meier, and Matthew Smith. A               [49] Maurice H ter Beek and Alessio Ferrari. Empirical
     qualitative usability evaluation of the clang static ana-             formal methods: guidelines for performing empirical
     lyzer and libFuzzer with CS students and CTF players.                 studies on formal methods. Software, 1(4), 2022.
     In Seventeenth Symposium on Usable Privacy and Secu-
     rity (SOUPS 2021), pages 553–572. USENIX Associa-                [50] Daniel Votipka, Kelsey R Fulton, James Parker, Matthew
     tion, August 2021. URL: https://www.usenix.org/                       Hou, Michelle L Mazurek, and Michael Hicks. Under-
     conference/soups2021/presentation/ploger.                             standing security mistakes developers make: Qualitative


                                                                 17
      analysis from build it, break it, fix it. In 29th USENIX                         A.2     Block: Learnability
      Security Symposium (USENIX Security 20), pages 109–                              Q5. What resources did you rely on when learning the tool? (select all that
      126, 2020.                                                                           apply)

[51] Jiashuo Zhang, Jiachi Chen, Zhiyuan Wan, Ting Chen,                                       □ Official documentation and tool manual
     Jianbo Gao, and Zhong Chen. When contracts meets                                          □ Research papers applying the tool to real protocols
     crypto: Exploring developers’ struggles with ethereum                                     □ Video lectures or summer school recordings
     cryptographic apis. In Proceedings of the IEEE/ACM                                        □ Publicly available models from other researchers (e.g., GitHub)
     46th International Conference on Software Engineering,                                    □ Peer or supervisor guidance
     pages 1–13, 2024.
                                                                                               □ Other (please specify)
[52] Yunze Zhao, Wentao Guo, Harrison Goldstein, Daniel                                Q6. What was the steepest part of the learning curve? (select one)
     Votipka, Kelsey R Fulton, and Michelle L Mazurek. A
                                                                                                1. Translating informal protocol descriptions into the tool’s mod-
     qualitative analysis of fuzzer usability and challenges.                                      eling language
     In Proceedings of the 2025 ACM SIGSAC Conference on                                        2. Understanding the underlying formal theory (e.g., applied pi-
     Computer and Communications Security, pages 2504–                                             calculus, multiset rewriting)
     2518, 2025.                                                                                3. Interpreting verification output and attack traces
                                                                                                4. Debugging non-termination and performance issues
A     Survey Instruments                                                                        5. Knowing what the proof actually guarantees in practice
                                                                                                6. Other (please specify)
This appendix presents the full text of the survey administered to participants
with experience using cryptographic protocol verification tools (Tamarin               Q7. Which programming concepts from your prior experience helped you
Prover, ProVerif, and other). The survey was organized into five blocks:                   be more effective when learning or using this cryptographic verification
Demographic, Learnability, Modeling & Verification, Tamarin, and ProVerif.                 tool? (select all that apply)
Unless otherwise noted, single-select items are marked (select one) and
multi-select items are marked (select all that apply) or checkbox.                             □ Step-by-step algorithmic thinking
                                                                                               □ Control flow (if/else, loops)
A.1      Block: Demographic                                                                    □ Debugging skills (tracing execution, logging, breakpoints)
Q1. Which of the following verification tools have you used? (select all                       □ Error handling (exceptions, return codes, defensive checks)
    that apply)                                                                                □ Higher-order functions
          □ Tamarin                                                                            □ Immutability (avoiding unintended state changes)
          □ ProVerif                                                                           □ Pattern matching / case analysis
          □ DeepSec
                                                                                               □ Recursion (reasoning via repeated structure)
          □ Other (please specify)
                                                                                               □ Other (please specify)
Q2. How long have you been using formal verification tools for security
    protocols?                                                                         Q8. Have you previously used any general-purpose model checker that
                                                                                           helped you learn or use this cryptographic verification tool?
          1. Less than 1 year
          2. 1–3 years                                                                         □ SPIN
          3. 4–6 years                                                                         □ NuSMV
          4. More than 6 years                                                                 □ UPPAAL
Q3. What is your current role or background?                                                   □ TLA+ (TLC)
          1. Undergraduate student (studying relevant field)                                   □ PRISM
          2. Graduate student (Master’s or PhD)                                                □ Maude
          3. Academic researcher or faculty                                                    □ Other (please specify)
          4. Industry professional (practitioner using formal methods)                         □ None
          5. Other (please specify)
Q4. How would you rate your expertise in formal methods / cryptographic                A.3     Block: Modeling & Verification
    protocol verification?
                                                                                       Q9. How confident are you that your formal model accurately reflects the
          1. Novice: new to formal verification (just learning or only basic
                                                                                           real-world protocol you intend to verify?
             knowledge)
          2. Intermediate: comfortable with core concepts and have used                         1. 1 – Not confident at all
             verification tools on some projects                                                2. 2 – Slightly confident
          3. Advanced: very proficient with formal verification; extensive                      3. 3 – Moderately confident
             experience using these tools
                                                                                                4. 4 – Confident
          4. Deep expertise (e.g., you contribute to tool development or
             advanced research in this area)                                                    5. 5 – Very confident


                                                                                  18
Q10. What most limits your confidence in the accuracy of your model?                 A.4      Block: Tamarin
     (select all that apply)
                                                                                     Q14. Have you ever encountered a counterexample in Tamarin that you later
          □ The symbolic model assumes perfect cryptography, which may                    determined to be a false positive? If so, how did you typically recover
            not reflect actual weaknesses in real-world implementations                   from or resolve it?

          □ Difficulty modeling stateful or complex protocol behavior                          □ Refined or corrected the protocol model/specification
                                                                                               □ Manually analyzed the counterexample to confirm it was not a
          □ Uncertainty about whether the Dolev–Yao attacker model is
                                                                                                 real attack
            realistic enough
                                                                                               □ Consulted documentation, examples, or academic papers
          □ Lack of a systematic methodology to validate the model against
            the real protocol                                                                  □ Asked for help from peers, supervisors, or online communities

          □ No way to cross-check the model against the actual implemen-                       □ Adjusted assumptions about the adversary or environment
            tation                                                                             □ Other (please specify)
          □ Other (please specify)                                                   Q15. When running larger/realistic case studies in Tamarin, what is your
                                                                                          most common limiting factor(s)?
Q11. When a proof fails without a concrete attack trace, what is your typical
     approach? (select all that apply)                                                         □ Memory (RAM)
                                                                                               □ Time (runs too long / non-terminating)
          □ Simplify the model to isolate which part is causing the failure
                                                                                               □ Manual effort (requires deep interactive tracing)
          □ Add helper lemmas or auxiliary lemmas to guide the proof (e.g.,
            in Tamarin)                                                                        □ Tool crashes / instability
                                                                                               □ I don’t run large models
          □ Re-examine modeling decisions and abstractions for potential
            unsoundness                                                                        □ Other (please specify)
          □ Consult related published models or ask peers for guidance               Q16. How often do you need to write helper lemmas to guide Tamarin’s
                                                                                          proof search toward termination?
          □ Switch to a different tool to cross-validate the result
                                                                                               1. Never
          □ Assume the model is flawed and rewrite it from scratch
                                                                                               2. Rarely
          □ Increase computational resources or adjust tool parameters and
            re-run                                                                             3. Sometimes

          □ Other (please specify)                                                             4. Often
                                                                                               5. Almost always
Q12. Which best describes the tool’s communication when verification is
     slow or non-terminating? (select all that apply)                                Q17. How intuitive is the visualization of the dependency graph in Tamarin’s
                                                                                          interactive mode?
          □ The tool hangs silently with no output or progress indication
                                                                                               1. 1 – Very unintuitive: the graph is difficult to read and interpret
          □ The tool shows generic progress output but nothing specific to                     2. 2 – Unintuitive: requires significant experience to navigate
            my model
                                                                                               3. 3 – Moderate: readable with effort but could be clearer
          □ The tool produces verbose low-level output that is hard to map
            back to my model                                                                   4. 4 – Intuitive: the graph is generally easy to read and navigate
                                                                                               5. 5 – Very intuitive: the graph clearly communicates the proof
          □ The tool indicates which rule or lemma is causing the bottleneck
                                                                                                  state
            but offers no guidance
                                                                                     Q18. How difficult is it to model the following in Tamarin? Rate each on a
          □ The tool clearly communicates the source of the problem and
                                                                                          scale from 1 (Very Difficult) to 5 (Very Easy).
            how to address it
                                                                                               □ Stateful protocols
Q13. What best describes the most common shortcoming in the tool’s error
     messaging? (select all that apply)                                                        □ Multi-session scenarios
                                                                                               □ Forward secrecy
          □ Error messages do not pinpoint the exact location of the problem
            in the model                                                                       □ Complex equational theories (e.g., Diffie–Hellman, XOR)
                                                                                               □ Observational equivalence properties
          □ Errors are too low-level and tied to internal tool mechanics
            rather than the model itself                                             Q19. What is the important usability improvement you would like to see in
                                                                                          Tamarin Prover?
          □ Semantic errors are silently ignored rather than explicitly re-
            ported                                                                             □ Modeling support
          □ No suggestion or hint is provided on how to fix the issue                          □ Error feedback
          □ Error messages assume too much prior knowledge of the under-                       □ Counterexample explanation
            lying formal theory                                                                □ Documentation
          □ No shortcoming in the tool’s error messaging                                       □ Tooling support
          □ Other (please specify)                                                             □ Other (please specify)


                                                                                19
A.5      Block: ProVerif                                                                  □ A graphical interface for model visualization and attack trace
                                                                                            exploration
Q20. How adequate is ProVerif’s current support for observational equiva-
     lence (two protocol executions are indistinguishable to any attacker) in             □ Automated suggestions for fixing common modeling mistakes
     analyzing modern privacy-preserving protocols? Please explain your                   □ Improved documentation with realistic, well-annotated protocol
     reasoning for your choice.                                                             examples
          1. Fully adequate                                                               □ Integration with standard development tools (e.g., IDE plugins,
                                                                                            CI/CD pipelines)
          2. Adequate with minor limitations
                                                                                          □ A model validation mechanism to check whether the formal
          3. Adequate but requires significant improvements
                                                                                            model matches the intended protocol
          4. Insufficient for modern protocols
                                                                                          □ Other (please specify)
          5. Not sure
Q21. How adequate is ProVerif’s current support for reasoning about com-
     plex algebraic properties (e.g., Diffie–Hellman, XOR, group equa-               B   Figures
     tions)? Please explain your reasoning for your choice.
          1. Fully adequate for modern protocols
          2. Adequate with careful modeling
          3. Adequate but prone to false positives
          4. Limited for algebra-heavy designs
          5. Insufficient and requires redesign
          6. Not sure
Q22. Considering that ProVerif does not natively support mutable global
     state or ordered transitions, do you believe its current framework is
     fundamentally adequate for verifying stateful protocols (e.g., TPMs,
     IoT devices, e-passports)? Please explain your reasoning for your
     choice.
          1. Fully adequate
          2. Adequate with minor limitations
          3. Adequate but requires significant improvements
          4. Insufficient for complex stateful designs
          5. Not sure
Q23. In your opinion, how adequate is ProVerif’s support for verifying
     Perfect Forward Secrecy (compromise of long-term keys does not
     break past sessions)? Please explain your reasoning for your choice.
          1. Fully adequate
          2. Adequate with minor limitations
          3. Adequate but requires significant improvements
          4. Insufficient for modern protocols
          5. Not sure
Q24. Considering that post-compromise security requires reasoning about
     state evolution, key updates, and temporal ordering (e.g., compromise
     occurs, then secure recovery), do you believe ProVerif’s current Horn-
     clause-based over-approximation is fundamentally adequate for this?
     Please explain your reasoning for your choice.
          1. Fully adequate
          2. Adequate with careful modeling
          3. Adequate but limited for dynamic recovery
          4. Insufficient for modern ratcheting protocols
          5. Not sure
Q25. Which features or improvements would most increase your productivity
     with ProVerif?
          □ An interactive debugging mode allowing step-by-step inspec-
            tion of the proof state


                                                                                20
                   Table 2: Participant ratings of ProVerif’s support for post-compromise security.

Response                                    Representative concerns raised

Not sure (7)                                —

Adequate with careful modeling (2)          • Models exist for protocols such as Signal, but require substantial manual effort
                                            • Reference to a recent Signal ProVerif model (S&P ’26)

Insufficient for modern ratcheting proto-   • Current support described as inadequate
cols (2)                                    • Hope that issues related to overfitting will be addressed in future updates,
                                            despite this being a challenging problem

Fully adequate (1)                          —

Adequate but limited for dynamic recov-     • Not straightforward to model
ery (1)



               Table 3: Participant ratings of ProVerif’s support for verifying Perfect Forward Secrecy.

Response                                    Representative concerns raised

Not sure (7)                                —

Fully adequate (3)                          —

Adequate with minor limitations (2)         • Care is needed in how “past” states are modeled
                                            • Increasing the number of sessions tested may improve confidence in results

Adequate but requires significant im-       • Requires tricks to model correctly
provements (1)



                   Table 4: Participant ratings of ProVerif’s support for state-dependent protocols.

Response                                    Representative concerns raised

Insufficient for complex stateful designs   • Modeling attempts required deviating significantly from the protocol specifica-
(4)                                         tion just to get ProVerif to terminate
                                            • Particularly limiting for stateful devices such as TPMs and IoT devices
                                            • Tables can be used to emulate a notion of state, but this is unsatisfactory and
                                            likely does not scale to large protocols
                                            • Hope for future updates to natively support mutable global state and ordered
                                            transitions

Adequate but requires significant im-       • Workarounds can often be made to work, but require substantial manual effort
provements (3)                              • Reasoning about mutable state is inherently difficult
                                            • Extensions such as GSVerif can help address this gap

Adequate with minor limitations (2)         • Tables can handle state, though not always easily
                                            • Debugging stateful models is difficult

Fully adequate (2)                          —

Not sure (2)                                —



                                                             21
              Table 5: Participant ratings of ProVerif’s support for reasoning about complex algebraic properties.

        Response                                    Representative concerns raised

        Limited for algebra-heavy designs (4)       • Almost no support for Diffie–Hellman (DH)-type equations or theories using
                                                    AC operators, which are common in practice
                                                    • Does not support full DH reasoning the way Tamarin does

        Not sure (3)                                —

        Adequate with careful modeling (3)          • Can handle Diffie–Hellman, but one must be careful about the equations written
                                                    and account for properties like associativity and commutativity
                                                    • Expected to be of comparable quality to Tamarin

        Fully adequate for modern protocols (1)     —

        Adequate but prone to false positives (1)   • Termination is not obvious

        Insufficient and requires redesign (1)      • No support for AC symbols in ProVerif




Table 6: Participant ratings of ProVerif’s support for observational equivalence, with representative open-ended concerns for
each category.

        Response                                    Representative concerns raised

        Insufficient for modern protocols (4)       • Diff-equivalence is too coarse or too strong, limiting precision for properties
                                                    like anonymity or unlinkability
                                                    • Limited to reasoning about processes that differ only by certain terms
                                                    • Gaps in applicability to IoT and post-quantum computing settings

        Adequate but requires significant im-       • Diff-equivalence is an over-approximation that is sometimes hard to overcome
        provements (3)                              • Termination issues
                                                    • Need for more specific explanations of failure causes

        Adequate with minor limitations (2)         • Desire to examine more than two executions (e.g., for robust declassification)
                                                    • Sufficient, but usability requires deep prior knowledge of the tool

        Fully adequate (2)                          —

        Not sure (2)                                —




                                                                     22
                           Table 7: Summary of requested usability, design, and functional improvements.

Improvement Area            Tamarin Evidence                  ProVerif Evidence                Main Implication
Error feedback and          Error feedback: 8(67%)            Automated suggestions for        Errors should identify the relevant model
diagnostics                 responses in Q19                  modeling mistakes (3             element, explain the cause, and recommend
                                                              responses); interactive          possible corrective actions.
                                                              debugging (8 responses)
Counterexample and          Counterexample explanation:       Graphical attack-trace           Verification outcomes should be explained
result explanation          8(67%) responses; high-level      exploration (6 responses)        at the protocol level and connected to
                            AI synthesis requested in                                          assumptions and modeling decisions.
                            open-ended responses
Modeling and                Modeling support: 6(50%)          Model-validation mechanism       Tools should assist model construction and
validation support          responses                         (10 responses)                   help users assess whether the formal model
                                                                                               matches the intended protocol.
Interactive verification    Better interactive verification   Interactive debugging mode (8    Users need step-by-step access to proof
and debugging               and proof-oracle support          responses)                       states, bottlenecks, unresolved branches,
                            requested in open-ended                                            and attacker behavior.
                            responses
Visualization               Improved interactive and          Graphical model and              Visualizations should map internal proof
                            counterexample support            attack-trace interface (6        structures to protocol roles, messages,
                            implied by responses              responses)                       states, and properties.
Documentation and           Documentation: 5(42%)             Improved documentation(5         Documentation should include realistic
examples                    responses                         responses)                       annotated models, modeling rationale,
                                                                                               failure cases, and debugging workflows.
Proof automation and        Better proof oracles and          Helper-lemma generation          Tools could recommend helper lemmas,
guidance                    case-distinction support; AI      requested by 2 respondents       case distinctions, model simplifications,
                            synthesis requested by 2                                           and proof strategies.
                            respondents
Tooling and workflow        Tooling support: 5(42%)           IDE or CI/CD integration (3      Editor and workflow integration is useful,
support                     responses                         responses)                       but currently less important than
                                                                                               interpretability and validation.
Functional and              Greater support needed for        Greater support needed for       Some usability barriers require
expressive support          stateful protocols and            state, algebraic theories,       improvements to the tools’ underlying
                            observational equivalence         observational equivalence, and   verification and modeling capabilities.
                                                              state-evolving properties




                                                                     23
ID               Role                      Experience              Expertise              Tool(s)
P1    Academic Researcher or Faculty        1–3 yrs               Intermediate            ProVerif
P2              Graduate                    1–3 yrs              Deep Expertise      ProVerif, Squirrel
P3    Academic Researcher or Faculty        4–6 yrs              Deep Expertise           Tamarin
                                                                                     Tamarin, ProVerif,
P4    Academic Researcher or Faculty          > 6 yrs            Deep Expertise
                                                                                        CryptoVerif
                                                                                    Tamarin, EasyCrypt,
P5    Academic Researcher or Faculty          4–6 yrs               Advanced
                                                                                         ProofFrog
P6         Industry Professional              > 6 yrs               Advanced      Isabelle/PSPSP, OFMC
                                                                                     Tamarin, ProVerif,
P7    Academic Researcher or Faculty          > 6 yrs            Deep Expertise      OFMC, AVISPA,
                                                                                  AVANTSSAR, SPaCIoS
P8    Academic Researcher or Faculty          > 6 yrs               Advanced         Tamarin, ProVerif
                                                                                     Tamarin, ProVerif,
P9    Academic Researcher or Faculty          > 6 yrs               Advanced
                                                                                          DeepSec
                                                                                     Tamarin, ProVerif,
P10          Graduate student                 1–3 yrs             Intermediate
                                                                                          AVISPA
P11   Academic Researcher or Faculty          1–3 yrs             Intermediate            ProVerif
P12   Academic Researcher or Faculty          > 6 yrs            Deep Expertise      Tamarin, ProVerif
P13       Industry professional               > 6 yrs              Advanced          Tamarin, ProVerif
                                                                                     Tamarin, ProVerif,
P14   Academic Researcher or Faculty          4–6 yrs               Advanced
                                                                                          DeepSec
P15   Academic Researcher or Faculty          > 6 yrs              Advanced          Tamarin, ProVerif
P16   Academic Researcher or Faculty          > 6 yrs            Deep Expertise      Tamarin, ProVerif

                        Table 8: Demographic details of survey participants.




                                                24
     Intro & Consent
     Description of the study and informed
     consent.


     Demographics
     Demographic & users' research
     background questions


     Learnability
     Questions regarding how participants
     learned cryptographic verification and
     the challenges they faced during the
     process.


     Modeling & verification workflow
     Questions about the usability of
     cryptographic verification tools during
     protocol modeling and verification.
       Has tamarin
       experience
                                                   No experience on Tamarin/ProVerif




     Tamarin related usability
     Usability questions based on Tamarin
     verifier.

       Has proVerif
        experience
     ProVerif related usability
     Usability questions based on ProVerif
     verifier.

     End of Survey Confirmation


Figure 3: Overview of the survey flow and conditional tool-
specific branches.




                                                                                       25
