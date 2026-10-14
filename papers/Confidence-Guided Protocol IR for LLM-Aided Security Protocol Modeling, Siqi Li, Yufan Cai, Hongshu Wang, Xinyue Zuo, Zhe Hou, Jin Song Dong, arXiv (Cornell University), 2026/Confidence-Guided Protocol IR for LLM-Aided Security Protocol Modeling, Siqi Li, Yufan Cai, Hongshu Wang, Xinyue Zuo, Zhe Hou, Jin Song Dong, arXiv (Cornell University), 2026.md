                                             Confidence-Guided Protocol IR for LLM-Aided
                                                      Security Protocol Modeling

                                             Siqi Li1,2[0009−0001−9896−243X] , Yufan Cai1[0009−0008−7579−0824] , Hongshu
                                                Wang1[0009−0006−0198−148X] , Xinyue Zuo1[0009−0008−4411−3054] , Zhe
                                                Hou3[0000−0001−7164−0580] , and Jin Song Dong1[0000−0002−6512−8326]
                                                             1
                                                              National University of Singapore, Singapore
arXiv:2609.37396v1 [cs.CR] 29 Sep 2026




                                                        2
                                                         Beijing Normal-Hong Kong Baptist University, China
                                                                        3
                                                                          Griffith University
                                                                   t330013016@mail.bnbu.edu.cn
                                                        {caiyf, hongshu.wang, zuoxy, dcsdjs}@nus.edu.sg
                                                                      z.hou@griffith.edu.au



                                                Abstract. Large language models offer a promising interface for trans-
                                                lating natural-language protocol descriptions into formal security mod-
                                                els, but their outputs remain difficult to trust without expert validation.
                                                In this paper, we present a human-in-the-loop framework for generating
                                                Tamarin-verifiable formal models of security protocols. Our key obser-
                                                vation is that the main correctness bottleneck is the semantic accuracy
                                                rather than the syntactic validity of the intermediate protocol represen-
                                                tation. To address this problem, we introduce a protocol intermediate
                                                representation (IR) that serves as a human-auditable semantic check-
                                                point between natural-language parsing and formal model generation.
                                                The IR explicitly captures protocol participants, message flows, value
                                                provenance, cryptographic operations, proof targets, and compromise
                                                assumptions. We further design an interactive interface that highlights
                                                uncertain fields and guides users to inspect the most critical semantic de-
                                                cisions based on model confidence before model generation. Rather than
                                                replacing formal-methods experts, our approach uses LLMs to produce
                                                auditable semantic drafts while leveraging verification tools to check the
                                                resulting formal models.

                                                Keywords: Security Protocol Verification · Large Language Models ·
                                                Human-in-the-loop Verification · Protocol Intermediate Representation


                                         1    Introduction
                                         Security protocols are communication workflows that allow distributed parties
                                         to exchange information securely over untrusted networks. They are the foun-
                                         dation of modern digital systems, including online finance, e-commerce, cloud
                                         services, blockchains, and decentralized applications. Since these protocols are
                                         deployed in adversarial environments, even small design flaws may lead to severe
                                         security breaches and financial losses. A notable example is the 2016 DAO attack
                                         on Ethereum, where a re-entrancy vulnerability in a smart contract resulted in
2       S. Li et al.

a loss of approximately $60 million [10]. Consequently, informal reasoning and
testing are often insufficient for establishing deployable security guarantees, es-
pecially for blockchain protocols and smart contracts that are difficult or impos-
sible to patch after deployment. Formal verification is therefore desirable because
it provides a rigorous way to analyze protocol behavior and establish correct-
ness and security guarantees [12]. Formal verification tools such as Tamarin [9],
ProVerif [1], and SAPIC+ [3] provide strong support for symbolic protocol anal-
ysis. They can verify secrecy, authentication, and correspondence properties, and
they can generate counterexamples when these properties do not hold. However,
the reliability of these results depends critically on the correctness of the under-
lying formal model, which is typically constructed manually by a human expert.
Automatically constructing such models from informal protocol requirements, in-
cluding natural-language descriptions, message diagrams, standards documents,
and research papers, remains challenging. A model may be syntactically valid
and verified, while still encoding the wrong protocol semantics.
    Recent work has explored the integration of large language models with for-
mal methods for tasks such as formal specification development, model construc-
tion, verification-guided repair, and trustworthy agent development [5,14,13,11,2].
Motivated by this broader trend, LLMs offer a promising way to reduce the bur-
den of security protocol modeling [8]. Given a natural-language protocol descrip-
tion, an LLM can generate structured summaries, infer message flows, and even
produce candidate SAPIC+ models. However, directly generating Tamarin code
from natural language remains unreliable. The core difficulty is not merely syn-
tactic generation, but semantic faithfulness: the generated model may compile
and verify while still misrepresenting the intended protocol. Once the relevant
protocol semantics are correctly captured, generating a formal model can be
made largely systematic. Fresh values can be translated into declarations, long-
term state into setup processes, messages into input/output actions, checks into
conditional tests, events into symbolic annotations, and proof targets into lem-
mas. The difficult part is ensuring that these objects faithfully represent the
intended protocol before they are translated into a formal model.
    To address this challenge, we propose a confidence-guided, human-auditable
Protocol Intermediate Representation, called Protocol IR, for LLM-aided model-
ing of security protocols. Instead of treating the LLM output as the final formal
model, our framework treats it as a structured semantic draft. The Protocol
IR records the modeling decisions that determine the meaning of the generated
formal model, including value provenance, initial knowledge, message structure,
cryptographic checks, event placement, proof intent, compromise assumptions,
and expected counterexamples. In this way, the IR serves as a semantic check-
point between informal protocol descriptions and the generation of trustworthy
formal models. The proposed framework aims to reduce the effort and exper-
tise required for formal modeling while still allowing users to intervene in the
modeling process. An interface displays the auditable semantic draft together
with confidence information for its components. Our framework makes this trust
boundary explicit: the initial IR is untrusted, but the reviewed IR becomes the
    Confidence-Guided Protocol IR for LLM-Aided Security Protocol Modeling       3

trusted source for model generation. To reduce the cost of human review, we in-
troduce confidence-guided inspection. Each IR field is annotated with confidence
information based on evidence support, consistency with other IR entries, and
semantic risk. For example, a field directly supported by a source sentence may
receive high confidence, while a value used before generation, an event placed
before a check, or a receiver assumed to know an underivable term should be
highlighted as risky. Since not all fields are equally important, low confidence in
proof targets, checks, events, or compromise assumptions is prioritized over low
confidence in descriptive fields. The interface uses these signals to guide users
toward the IR fields most likely to affect verification correctness.
    In summary, this paper makes the following contributions:

 – We propose a confidence-guided Protocol IR that exposes security-critical
   modeling decisions, including value provenance, initial knowledge, message
   structure, cryptographic checks, event placement, proof intent, compromise
   assumptions, and expected counterexamples.
 – We implement an end-to-end framework that translates natural-language
   protocol descriptions into Protocol IR, supports interactive human review
   through a user interface, automatically generates formal models from the
   reviewed IR, and invokes backend verification and repair.
 – We evaluate the framework on representative security protocol modeling
   tasks and non-standard cases, studying the correctness of generated IR fields,
   the effectiveness of confidence-guided review, and the quality of the resulting
   formal models and verification outcomes.

     The implementation is available on GitHub.4


2     Approach

Figure 1 shows the overall workflow of our approach. Given a natural-language
protocol description, the system first invokes an LLM to extract protocol seman-
tics into a structured Protocol IR. The IR captures security-critical modeling de-
cisions, including fresh values, long-term state, message structure, checks, event
placement, proof targets, and compromise assumptions. Each generated IR field
is associated with provenance information and confidence signals, which are later
used to guide human review. The user then inspects the generated IR through
a review interface. Instead of requiring the user to read low-level SAPIC+ code
line by line, the interface exposes high-level protocol concepts and highlights un-
certain or semantically risky fields. After the user confirms or edits the IR, the
reviewed IR becomes the trusted semantic source for automatic SAPIC+ gen-
eration. The generated model is then checked by Tamarin. When syntactic or
backend-specific errors are detected, the system attempts repair while preserving
the reviewed protocol semantics.
4
    https://github.com/laplace1002/TamarinAgent.git
4      S. Li et al.




Fig. 1: Overview of the proposed workflow. The Protocol IR serves as a semantic
checkpoint between unreliable natural-language interpretation and formal model
generation.


2.1   Protocol IR
The Protocol IR operationalizes the semantic checkpoint in our workflow. It or-
ganizes protocol semantics into structured components that are both reviewable
by humans and usable for downstream SAPIC+ generation. Unlike raw natural-
language descriptions, the IR makes modeling choices explicit: which values are
fresh, which values belong to long-term setup, how messages are constructed,
which checks are performed, where security events are placed, what properties
should be proved, and what compromise assumptions are allowed.

Fresh values. The IR records values generated during protocol execution, such
as nonces, random challenges, ephemeral keys, and session keys. For each fresh
value, the IR records its symbolic name, owner, and purpose. The symbolic name
is used later in message terms and proof events. The owner records which role
generates the value, while the purpose explains why the value exists, such as
freshness, challenge generation, or session-key establishment. A key distinction
is whether a value is generated freshly during protocol execution or belongs to
setup or long-term state. Confusing these two cases can substantially change the
security meaning of the generated model.

Cryptographic declarations. The IR records the cryptographic vocabulary re-
quired by the protocol, including built-in theories such as asymmetric encryp-
tion, hashing, or symmetric encryption, as well as protocol-specific functions,
equations, and assumptions when needed. These declarations determine which
symbolic operations are available when generating SAPIC+ code.

Long-term state and setup assumptions. The IR records long-term secrets, public
keys, shared keys, role identities, and setup-generated state. For each value, it
specifies which role owns it, whether it has a corresponding public term, and
whether it may be compromised. This component is essential for constructing a
faithful attacker model, since changing a setup assumption may alter whether
an attack is possible.

Messages. The IR describes each protocol message using a structured represen-
tation of sender, receiver, message fields, protection mode, and symbolic term.
The protection mode records whether the message is public, encrypted, signed,
  Confidence-Guided Protocol IR for LLM-Aided Security Protocol Modeling          5

authenticated by a MAC, or unknown. The symbolic term is used by downstream
SAPIC+ generation, while the natural-language meaning records the intended
interpretation of the message. The IR also stores derived provenance informa-
tion, such as which values the sender must know to construct the message and
which values the receiver is expected to derive after parsing it.

Actions. The IR contains role-local protocol transitions that map message-level
descriptions to role processes. An action records the executing role, generated val-
ues, incoming and outgoing messages, checks performed by the role, and events
emitted after the transition. These actions provide the bridge between protocol-
level descriptions and the process structure later emitted as code.

Checks and Events. The IR explicitly represents verification operations, includ-
ing equality checks, hash comparisons, MAC verification, signature verification,
decryption success, and reconstruction checks. Each check records the role that
performs it, the condition being checked, the source message providing the rel-
evant evidence, and the associated role-local action. Checks are security-critical
because symbolic events should usually be placed only after the relevant checks
have succeeded. The IR records symbolic events used by security lemmas, such
as Running, Commit, Accept, Secret, and Reveal. Each event records its name,
role, arguments, and intended placement. Together with surrounding actions and
checks, these fields make event placement auditable. For example, an authenti-
cation event should not be triggered immediately after receiving a message if the
role has not yet verified its contents.

Proof targets. The IR records the intended verification goals, including lemma
names, goal types, trace kinds, related events, secrecy targets, authentication
targets, expected verification results, and expected counterexamples. Proof tar-
gets are among the most important fields for human review.

Compromise assumptions and attack surface. The IR records attacker capabili-
ties, reveal rules, compromise assumptions, and expected attacks. This prevents
the repair process from accidentally removing an intended attack or weakening
the Dolev–Yao adversary simply to make a proof succeed.

Review Interface The review interface presents the reviewable IR as editable
structured sections. Its purpose is not to expose all low-level model-generation
details, but to help the user inspect the semantic choices that determine the
correctness of the final SAPIC+ model. The same IR components introduced
in §2.1 are rendered as review pages, including fresh values, setup and long-
term state, messages, checks, events, proof targets, compromise assumptions,
and expected attack surfaces. The left sidebar shows the current protocol name,
a color legend for field review status, and navigation groups for the workflow.
These groups include a start page for natural-language input, review pages for
editable IR sections, and generation pages for SAPIC+ output and Tamarin
results. Each navigation item may display a workflow status badge, such as
current, pending, or done, as well as the number of unresolved review cells.
6              S. Li et al.

{                                                                    "messages":[
    "schema":"protocol_ir_v1",                                        {
    "protocol_name":"Example",                                          "label":"M1",
    "roles":["C","S"],                                                  "from":"C",
    "crypto":{                                                          "to":"S",
     "builtins":[                                                       "protection":"asymmetric-encryption",
       "asymmetric-encryption",                                         "term":"aenc(~k, pk(ltkS))",
       "hashing",                                                       "meaning":"C sends a fresh key encrypted for S",
       "symmetric-encryption"                                           "_hidden_or_derived":{
     ],                                                                   "sender_knows":["~k","pk(ltkS)"],
     "functions":[],                                                      "receiver_can_decrypt":true
     "equations":[],                                                    }
     "assumptions":[                                                  }
       "Use the standard Dolev-Yao adversarial network model."       ],
     ]                                                               ...
    },                                                               "field_evidence":[
    "fresh_terms":[                                                   {
     {"name":"~k","owner":"C",                                          "field_path":"messages.0.protection",
       "purpose":"fresh symmetric session key"}                         "source_quote":"encrypts it with the public key pkS",
    ],                                                                  "evidence_kind":"direct",
    "long_term_keys":[                                                  "priority_llm":0.3,
     {"name":"ltkS","owner":"S",                                        "evidence_confidence_score":1.0,
       "public_term":"pk(ltkS)",                                        "consistency_confidence_score":1.0,
       "policy":"server private key is not revealed"}                   "semantic_impact_score":0.9
    ],                                                                }
    ...                                                              ]
                                                                 }




Listing 1.1: Partial raw Protocol IR for the “Example” protocol. The left column
shows protocol-level declarations and setup information, while the right column
shows message-level fields and LLM-provided field evidence. Ellipses indicate
omitted IR sections such as checks, events, actions, proof targets, compromise
assumptions, and semantic constraints.



Natural-language input. The first interface page allows the user to create a Pro-
tocol IR directly from a natural-language description. It contains fields for the
protocol name, difficulty label, protocol description, assumptions, and verifica-
tion goals. The protocol description is the only required input. Optional as-
sumptions can specify attacker-model or setup information, such as Dolev–Yao
network control or trusted public-key setup. Optional goals can specify target
lemma names, goal types, trace kinds, and expected results. If goals are omitted,
the planner infers candidate proof targets from the protocol description.
    After the user presses “Generate IR / Contract”, the system invokes the
planner to produce a Protocol IR candidate. It then validates the IR, derives
field-level review metadata, and constructs the reviewable modeling contract.
The validation pass checks for semantic risks such as missing required proof
events, events emitted before the corresponding check or decryption, conflicting
value classes, and derivability problems. These diagnostics can force a field into
“needs review” even when the LLM-provided confidence is high.

Prepared workflow and IR review pages. This page is used in the experimen-
tal workflow to load an already prepared protocol case from the local workflow
library. It allows the same review and generation pipeline to be applied consis-
tently across benchmark protocols. The review pages render the editable cells
of each IR component. For example, the message page exposes the reviewable
message fields defined in §2.1, as shown in Figures 2 and 3. The user can confirm
a generated field, edit it, or mark it as an intentional modeling assumption.
  Confidence-Guided Protocol IR for LLM-Aided Security Protocol Modeling          7




Fig. 2: Message header and protection cell in the review interface. The
message page exposes editable cells for the reviewable message fields. Clicking
“Review details” expands field-level diagnostic metadata used for confidence-
guided review, including confidence scores, review priority, recommended action,
and source evidence.


Per-cell review details. Every visible editable cell contains a “Review details”
panel. This panel displays the field-level confidence signals, review priority, val-
idation diagnostics, recommended reviewer action, and source evidence when
available. If no direct source span is found, the panel explicitly reports that the
field is inferred or assumed. The “Confirm” button marks the cell as manually
validated, while the “Assumed” button records that the user intentionally accepts
the value as a modeling assumption.

SAPIC+ generation and Tamarin results. After review, the user saves the edited
modeling contract. The system then materializes the reviewed contract back
into a reviewed Protocol IR and uses it for SAPIC+ generation. The SAPIC+
page provides controls to generate the model, run a repair-and-verify loop, and
invoke Tamarin proofs. The Tamarin results page displays compile status, proof
status, warnings, mismatched expected results, and the generated Tamarin code.
These outputs allow the user to check whether a Tamarin-clean model has been
generated and whether the expected proof outcomes are obtained.


2.2   LLM-Based IR Construction

Given a natural-language protocol description, the LLM is prompted to gener-
ate a Protocol IR rather than SAPIC+ code directly. This design deliberately
separates semantic interpretation from formal code generation. The LLM is re-
sponsible for extracting a structured candidate interpretation of the protocol,
including roles, values, messages, checks, events, proof targets, and compromise
8       S. Li et al.




Fig. 3: Message term and meaning review details. This view continues the
review of message M1, where role C sends the fresh key ~k to role S. The term cell
contains the symbolic message used by SAPIC+ generation, while the meaning
cell records the corresponding natural-language interpretation.


assumptions. For each generated IR field, the system asks the LLM to provide
supporting evidence from the source description when possible. For example,
if the LLM claims that a nonce is freshly generated by the initiator, it should
identify the corresponding textual evidence. If the field is inferred rather than
explicitly stated, the IR marks the field as inferred. If no direct evidence exists,
the field is marked as an assumption. This evidence-aware construction makes
the IR auditable. The user does not need to treat the LLM output as an opaque
answer. Instead, the user can inspect both the generated field and the reason
why the system believes the field is correct.

2.3   Confidence-Guided Human Review
A complete Protocol IR may contain many fields. Exhaustively reviewing every
field can be expensive, especially for complex protocols. To reduce review effort,
our framework assigns confidence and review priority to IR fields. The review
priority is derived from three kinds of signals.

Evidence confidence. Evidence confidence measures whether a field is directly
supported by the source description. A field receives high evidence confidence
if it is supported by an explicit source span, medium confidence if it is inferred
from nearby context, and low confidence if it has no direct textual support.

Consistency confidence. Consistency confidence measures whether a field is com-
patible with other IR entries. Examples of low consistency include a value used
  Confidence-Guided Protocol IR for LLM-Aided Security Protocol Modeling           9

before it is generated, a role verifying a term it cannot derive, an event placed
before the corresponding check, or a value classified both as a per-session nonce
and a long-term secret.

Semantic impact. Semantic impact measures how much an error in a field may
affect the meaning of the final verification result. Errors in proof targets, event
placement, checks, or compromise assumptions can make the final verification
result meaningless. Therefore, even a moderately uncertain field should receive
high review priority if its semantic impact is large.

Review priority. Conceptually, the review priority of a field is computed as
priority(f ) = max(1 − evidence(f ), 1 − consistency(f )) × impact(f ). This score is
used to guide attention. Fields with high priority are highlighted in the interface
and should be inspected first.

2.4   Formal Model Generation from Reviewed IR
After human review, the confirmed IR is used as the semantic source for SAPIC+
generation. Because the IR is structured around protocol concepts, the trans-
lation can be performed systematically. Fresh values are translated into new
declarations. Long-term state and setup assumptions are translated into setup
processes, persistent facts, or role parameters. Message entries are translated
into input and output actions. Cryptographic checks are translated into let,
equality, or conditional checks. Events are translated into SAPIC+ event anno-
tations. Proof targets are translated into Tamarin lemmas. Compromise assump-
tions are translated into reveal rules and attacker-knowledge declarations. For
medium and hard cases, the user can optionally enable abstraction hints as proof-
engineering assistance. Once enabled, the backend retrieves matching hints from
a predefined hint library using the reviewed IR and proof targets. These hints
describe modeling patterns such as compact event payloads, bounded role topol-
ogy, transcript summaries, and source lemma shapes. The generation prompt is
designed to preserve the reviewed IR semantics. In particular, it should not intro-
duce additional checks, remove attacker capabilities, or change event placement
unless such changes are reflected in the IR and confirmed by the user.

2.5   Repair and Verification
The generated SAPIC+ model is submitted to Tamarin for parsing and verifica-
tion. Some generated models may require repair due to syntactic errors, backend-
specific restrictions, Tamarin well-formedness warnings, or proof-lint issues. Our
framework allows automatic repair at this stage, but restricts the repair scope
to preserve the reviewed semantics. We distinguish two kinds of repair. Syntac-
tic repair fixes malformed SAPIC+ constructs, incorrect declarations, backend
compatibility issues, or translation-level inconsistencies in events, checks, and
lemmas when the fix is supported by the reviewed IR. Semantic repair changes
the protocol meaning, such as moving events, adding checks, changing attacker
10      S. Li et al.

capabilities, or modifying proof targets. Syntactic repair can be automated safely
because it does not alter the intended protocol semantics. Semantic repair re-
quires returning to the IR and asking the user to review the affected field. This
distinction prevents the system from optimizing for proof success at the cost of
model faithfulness. If Tamarin finds a counterexample, the system does not au-
tomatically treat it as a modeling bug. Instead, the counterexample is compared
against the expected attacks and compromise assumptions recorded in the IR.


3    Evaluation
In this section, we evaluate whether our framework can help users construct
trustworthy formal protocol models from natural-language descriptions. Follow-
ing the evaluation structure of prior work on LLM-aided automatic symbolic
modeling [8], we evaluate our approach at multiple levels: the quality of the gen-
erated protocol IR, the effectiveness of confidence-guided human review, and the
correctness of the generated SAPIC+ models.
   Our evaluation is designed to answer the following research questions:
RQ1: IR Extraction Quality. How accurately can the LLM extract a proto-
  col IR from a natural-language protocol description?
RQ2: End-to-End Model Generation. Given a reviewed protocol IR, can
  our framework generate SAPIC+ models that are accepted by Tamarin?
RQ3: Generated versus Manual Models. How do generated models differ
  from manually developed Tamarin models and what do these differences
  reveal about the limits of LLM-assisted modeling?
RQ4: Cost Analysis. What is the cost of introducing the Protocol IR and
  confidence-guided review into the modeling workflow?

Implementation. We implemented our framework as an interactive modeling
assistant. All experiments are conducted on a MacBook Pro equipped with an
Apple M5 Pro chip, a 15-core CPU, a 16-core integrated GPU, 24 GB of RAM,
and macOS 26.5 (Build 25F71). For LLM calls, we use provider-hosted chat-
completion APIs as served during June 7–8, 2026. We evaluate our system using
the following LLMs: DeepSeek V4 Pro [4], GPT-4o [7], GPT-5.5 [7], and Llama-
3.3-70b-instruct [6]. All generated SAPIC+ models are checked using Tamarin
version1.12.0 with Maude version 3.5.1.

Metrics We follow prior work’s exact-coverage, boundedness-check, and property-
success evaluation style [8], but adapt the counting unit to our UI-visible IR
review cells. For RQ1, Table 1 reports exact-match rate (EMR), semantic accu-
racy (SA), well-formedness rate (WFR), and semantic repair count (#ϵ). EMR
adapts exact coverage to UI-visible IR cells: EMR = Nmatch /Ncell , where Ncell
is the number of evaluated UI-visible cells. SA is also cell-level and treats ex-
act and semantically acceptable labeled cells as positive: SA = (Ncorrect +
Nacceptable )/Nlabeled-cell , where Nlabeled-cell excludes unlabeled or invalid rows.
WFR instead performs a role-local provenance check over symbolic-value uses:
  Confidence-Guided Protocol IR for LLM-Aided Security Protocol Modeling          11

WFR = Nprovenance-ok /Nprovenance . It therefore has a different denominator and
measures neither global semantic correctness nor SAPIC+ syntactic acceptance.
Finally, #ϵ = Nlabeled-cell − Ncorrect − Nacceptable counts existing UI-visible cells
that require semantic repair. Because the number of emitted cells and provenance
uses depends on the generated IR, these RQ1 measures are output-conditioned
diagnostics rather than recall over a fixed set of reference obligations. For RQ2,
Table 2 summarizes SAPIC+ acceptance and verification success as case-level
ratios in the totals. For RQ3, we compare GPT-5.5-generated models with man-
ual models using the structural alignment metrics defined below. For this com-
parison, comments and lemmas are removed, identifiers and constants are alpha-
normalized, and equivalent cryptographic aliases are normalized. We apply these
metrics to four dimensions corresponding to explicit modeling decisions, includ-
ing value provenance and setup, message payload structure, cryptographic de-
pendencies, and verification checks. Each dimension is represented as a multiset
of structural atoms. For generated atoms G and reference atoms R, the matched
atoms are M = G ∩ R. We report Precision = |M |/|G|, Recall = |M |/|R|,
F1 = 2P R/(P + R). Precision penalizes unsupported additions, while recall cap-
tures details omitted from the generated model. For RQ4, we report UI-visible
manual edit counts and runtime overhead for SAPIC+ generation and Tamarin
verification.


3.1   RQ1: IR Extraction Quality

For each protocol description, we prompt the LLM to generate a protocol IR.
We compare the generated IR against the manually reviewed reference IR. We
evaluate both exact field-level matching and semantic correctness. Unlike direct
SAPIC+ generation, the IR is designed to expose semantic information that is
important for formal modeling, including value provenance, verification targets,
role-local knowledge, and compromise assumptions.
    Table 1 reports the IR extraction results. We observe that exact match for
each IR field remains challenging because the average EMR is mostly under
55.0%, even for strong models. However, semantic accuracy is higher, especially
for GPT-5.5, indicating that many emitted cells that do not exactly match the
reference are still semantically acceptable. This does not account for reference
details that the model fails to emit. GPT-4o achieves the best average EMR
(51.9%) and the fewest ϵ among the non-GPT-5.5 models. DeepSeek V4 Pro has
slightly higher semantic accuracy than GPT-4o and Llama, but requires more
missing-cell corrections. GPT-5.5 achieves near-perfect semantic accuracy on the
annotated UI cells, suggesting that it often captures protocol meaning. Its lower
average WFR (44.8%) captures a different issue. WFR checks whether every
role-local value use has an explicit source. For example, a cell may correctly
state that a server computes its response from a nonce n and therefore receive
an acceptable SA label. If the server role does not explicitly obtain n through an
in action or carry it in local state, the corresponding use fails the WFR check.
12         S. Li et al.


               Table 1: IR extraction quality at the UI-visible cell level.
                  DeepSeek V4 Pro                  GPT-4o            Llama-3.3-70b-instruct            GPT-5.5

Protocol      EMR      SA    WFR #ϵ EMR            SA   WFR #ϵ EMR            SA    WFR       #ϵ EMR        SA WFR #ϵ

Example     50.6% 94.8% 100.0%          4 62.3% 93.4% 100.0%        4 60.7% 93.4% 100.0%       4 52.0% 100.0% 52.9%    0
NSPK        52.3% 80.2% 85.7%          17 56.0% 75.0% 100.0%       21 54.2% 75.0% 76.9%       18 35.9% 100.0% 65.7%    0
Naxos       32.6% 85.7% 55.6%           7 49.0% 89.8% 100.0%        5 47.5% 74.6% 100.0%      15 44.2% 100.0% 44.4%    0
Toy         35.3% 95.3% 95.8%           4 49.0% 82.3% 100.0%        9 43.7% 76.1% 100.0%      17 30.4% 100.0% 55.6%    0
Woo and Lam 53.4% 84.1% 100.0%         14 55.1% 73.1% 89.5%        21 57.7% 73.1% 88.2%       21 38.9% 100.0% 51.1%    0
Sigfox      44.6% 78.5% 83.3%          14 47.3% 90.9% 88.9%         5 43.9% 70.2% 100.0%      17 27.4% 100.0% 82.6%    0

X509.1       43.3% 55.7%     61.1%     43 52.7% 80.0% 71.4%        11 53.2% 79.0%   77.8%     13 39.0% 99.2% 34.6%     1
DenningSacco 45.0% 93.6%     90.9%      7 53.7% 88.1% 100.0%        8 53.5% 85.9%   83.3%     10 39.5% 100.0% 95.1%    0
Kao Chow     63.5% 87.3%     53.8%     16 61.5% 79.2% 66.7%        20 56.2% 77.1%   68.8%     22 44.4% 100.0% 40.0%    0
NSSK         51.8% 82.9%     90.0%     28 67.0% 76.0% 100.0%       24 64.6% 79.2%   86.4%     20 55.3% 100.0% 35.1%    0
Stubblebine  45.3% 57.9%     66.7%     67 49.2% 63.3% 69.0%        47 38.8% 70.9%   70.3%     48 34.2% 100.0% 25.0%    0
Otway Rees   60.2% 93.2%     94.3%     11 67.0% 77.0% 66.7%        23 61.0% 68.0%   73.3%     32 46.1% 100.0% 38.5%    0
Yahalom      58.2% 81.8%     73.9%     20 62.2% 79.6% 68.4%        20 63.9% 80.2%   85.7%     17 40.1% 100.0% 50.9%    0

EDHOC         27.9% 78.9%    73.4%     62 39.5% 73.7%   73.7%      30 44.4% 60.2%   93.3%     43 32.4% 100.0% 23.8%    0
KEMTLS        16.9% 74.3%    92.6%     87 34.8% 64.0%   59.1%      32 36.1% 54.2%   66.7%     38 19.1% 100.0% 32.6%    0
LAKE          40.5% 87.8%    41.2%      9 35.7% 72.9%   85.7%      19 40.3% 75.8%   75.0%     15 27.1% 100.0% 37.1%    0
SPLICE        48.2% 59.7%    85.7%     56 50.0% 57.6%   75.0%      39 47.1% 63.7%   88.2%     37 24.4% 100.0% 40.0%    0
SSH           37.7% 45.5%    52.9%     42 42.0% 76.8%   64.3%      16 47.4% 77.2%   75.0%     13 19.9% 100.0% 1.6%     0

Average       44.9% 78.7%    77.6% 28.2 51.9% 77.4%     82.1% 19.7 50.8% 74.1%      83.8% 22.2 36.1% 99.96% 44.8% 0.1




 Table 2: End-to-end model generation and verification results for one round.
Protocol          DeepSeek                    GPT-4o                      Llama                      GPT-5.5

           Mod. Ver.   Time Edits Mod. Ver. Time Edits Mod. Ver.              Time Edits Mod.        Ver.   Time Edits

Example       ✓    ✓    103.0    15       ×    ×     77.8    16      ×    ×    428.4     15      ✓     ✓     155.9    0
NSPK          ✓    ×   2512.1    80       ×    ×     91.0    81      ×    ×   1048.3     93      ✓     ✓    2008.4    0
Naxos         ✓    ✓    264.7    47       ×    ×     52.6    43      ×    ×    435.5     49      ✓     ✓     958.8    0
Toy           ✓    ✓     40.5    11       ✓    ✓     29.2    40      ×    ×   1559.9     28      ✓     ✓     164.0    0
Woo&Lam       ✓    ×   4340.2    85       ×    ×     68.2    97      ×    ×   1272.4     97      ✓     ✓    965.47    0
Sigfox        ✓    ×   1476.7    44       ×    ×     51.4    44      ×    ×   1546.2     50      ✓     ✓     241.5    0

X509.1        ✓    ✓    668.3    36       ×    ×     65.0    39      ×    ×   1024.2     39      ✓     ✓   414.3      1
Denning       ✓    ✓   5015.8    49       ×    ×     68.7    69      ×    ×   1356.0     69      ✓     ✓ 2206.9       0
KaoChow       ✓    ✓   3888.8    75       ×    ×    202.8   102      ×    ×   2401.1    104      ✓     × 4484.61      0
NSSK          ✓    ✓   1588.9    74       ×    ×    100.3    97      ×    ×   2647.2     97      ✓     ✓ 2286.0       0
Stubblebine   ✓    ×   4201.0   115       ×    ×     97.4   114      ×    ×    601.1    118      ✓     × 5482.6       0
OtwayRees     ✓    ×   5125.7     9       ×    ×    112.6   102      ×    ×   2321.1    111      ✓     × 6652.18      0
Yahalom       ✓    ×   1468.3    93       ×    ×    154.4   101      ×    ×   1798.0    102      ✓     × 4014.83      0

EDHOC         ✓    ×   5161.6   102       ×    ×     72.6   130      ×    ×   1462.2    126      ✓     ✓    2360.2     0
KEMTLS        ✓    ✓   3771.8    88       ×    ×     67.9   127      ×    ×    543.5    128      ✓     ✓    2065.8    11
LAKE          ✓    ✓   3262.5    67       ×    ×     63.5    79      ×    ×   1598.6     78      ✓     ✓    2125.2     0
SPLICE        ✓    ×   5606.9   182       ×    ×    102.9   187      ×    ×   1949.3    187      ✓     ✓     802.5     0
SSH           ✓    ×   5401.4   130       ×    ×     71.4   125      ×    ×   1133.7    130      ✓     ✓    2287.0     0

Total      18/18 9/18 53898.2   1302   1/18 1/18 1549.7     1593   0/18 0/18 25126.7   1621 18/18 14/18 39676.2       12




3.2     RQ2: End-to-End SAPIC+ Model Generation


After user inspection and repair, we translate the reviewed protocol IR into
SAPIC+. We then run Tamarin on the generated model and check the tar-
get security properties. A case is considered successful if the generated model
is accepted by Tamarin and all target properties are verified or produce ex-
pected attacks. Table 2 reports the end-to-end results. DeepSeek provides the
strongest compile-success baseline, with all 18 generated models accepted by
Tamarin, although only 9 of them satisfy the expected verification outcomes. In
contrast, GPT-4o and Llama struggle in downstream SAPIC+ generation. GPT-
5.5 achieves the highest verification success so far, with 14 out of 18 cases verified,
suggesting that stronger models can improve the generation performance.
  Confidence-Guided Protocol IR for LLM-Aided Security Protocol Modeling         13


Table 3: Quantitative comparison between 18 GPT-5.5-generated and manual
SAPIC+ models.
              Modeling dimension           Precision Recall          F1
              Value provenance and setup         0.824     0.682   0.714
              Message structure                  0.555     0.586   0.560
              Cryptographic dependencies         0.652     0.704   0.656
              Verification checks                0.516     0.488   0.478



Table 4: Per-protocol F1 scores for four modeling dimensions. Each entry is the
F1 of the generated model against the manual SAPIC+ reference.
             Protocol             Provenance   Message   Crypto    Checks
             CCITT-X509                 0.62      0.39     0.79      0.56
             Denning–Sacco              0.71      0.60     1.00      0.33
             EDHOC                      0.47      0.30     0.18      0.50
             Example                    0.67      1.00     0.67      0.57
             KEMTLS                     0.50      0.42     0.25      0.38
             Kao–Chow                   0.71      0.51     0.75      0.39
             LAK06                      0.75      0.30     0.36      0.22
             NSPK                       0.78      0.73     1.00      0.48
             NSSK                       0.71      0.51     0.68      0.45
             Naxos                      0.67      0.47     0.62      1.00
             Neuman–Stubblebine         0.71      0.40     0.84      0.16
             Otway–Rees                 0.71      0.53     0.33      0.28
             SPLICE                     0.70      0.38     0.62      0.41
             SSH                        0.62      0.42     0.18      0.36
             Toy                        1.00      0.83     1.00      1.00
             Woo–Lam                    0.80      0.68     0.69      0.48
             Yahalom                    0.71      0.65     0.94      0.41
             Sigfox                     1.00      0.96     0.90      0.62




3.3   RQ3: Generated versus Manual Models

We compare the 18 GPT-5.5-generated SAPIC+ models with the correspond-
ing manual models from prior work [8]. This comparison is performed at the
SAPIC+ level to avoid mixing modeling choices with artifacts introduced by
compiler expansion into multiset-rewriting models.
    Table 3 shows that setup and value provenance are the best-aligned dimension
(F1 = 0.714), followed by cryptographic dependencies (F1 = 0.656). Alignment is
weaker for message structure (F1 = 0.560) and verification checks (F1 = 0.478).
Thus, generated models more often retain the protocol’s cryptographic vocabu-
lary than the exact conditions under which a received value may be trusted.
    We selected representative cases from Table 4 to illustrate three distinct
outcomes: (i) close agreement on the protocol body under different threat or
session assumptions, (ii) over-modeling reflected in low precision, and (iii) causal
errors that are not captured by a bag of structural atoms.
    (i) NSPK and Example show that agreement on the protocol body can co-
exist with differences in threat and session modeling. For NSPK, cryptographic-
dependency F1 is 1.00 and message-structure F1 is 0.73, reflecting the preser-
14      S. Li et al.

vation of the three encrypted messages. The manual model includes replicated
honest principals and an explicit compromise interface. However, the generated
model publishes one attacker-controlled private key and does not reproduce
the same replicated-principal structure. Example makes this distinction even
sharper. Its message-structure F1 is 1.00, showing that client request, server de-
cryption, and hash response have the same symbolic shape in both models. But
its provenance F1 drops to 0.67 because generated model omits the replicated
client/server sessions and explicit long-term-key reveal branches present in the
manual model. These differences matter because the same protocol body can be
analyzed under different assumptions about principals, compromise, and session
replication.

    (ii) LAK06 and Woo–Lam illustrate how precision and recall expose dif-
ferent kinds of disagreement. LAK06 achieves provenance F1 of 0.75, but its
message-structure and cryptographic-dependency precision are only 0.30 and
0.36. The generated model introduces separate reader and backend branches, a
prior-transcript role, additional forwarding steps, and duplicated outputs, while
the manual model uses a compact synchronized-key protocol. The issue is there-
fore not omission but addition. Woo–Lam falls between the closely aligned and
heavily over-modeled cases, with provenance, message, crypto, and checks F1 val-
ues of 0.80, 0.68, 0.69, and 0.48. It retains the broad message and cryptographic
structure but differs more substantially in validation logic and adversarial events.

    (iii) EDHOC and SSH expose a different problem. EDHOC has message-
structure and cryptographic-dependency F1 values of 0.300 and 0.18, but the
more important issue is that a single HonestEDHOC process constructs both ini-
tiator and responder messages sequentially. After sending the first message, it
constructs the response locally and verifies its own locally generated signature
without an intervening network input. The manual model instead separates ini-
tiator and responder processes with explicit out/in boundaries. SSH shows the
same causal problem. Its cryptographic-dependency F1 is only 0.18, but the
more important issue is that the generated model does not preserve the distinc-
tion between locally generated and peer-provided values. Server values created
locally are later treated as if they had been received from the peer. The model
also omits the encrypted user-authentication request, acknowledgement, signed
response, and final server verification present in the manual model.

    Overall, the GPT-5.5-generated models match the manual references more
closely on the protocol body than on security assumptions. Therefore, generated
models are useful as semantic drafts, but not as direct replacements for manually
developed models. Human review is still needed to check assumptions about the
attacker, session state, role ownership, and when inputs are accepted. In several
cases, the generated model simplified or omitted details that affect which traces
are reachable. As a result, a model may verify successfully while still representing
a weaker or different threat model from the manual reference.
    Confidence-Guided Protocol IR for LLM-Aided Security Protocol Modeling         15

3.4     RQ4: Cost Analysis
RQ4 evaluates the cost of introducing Protocol IR and confidence-guided re-
view. Compared with direct LLM-to-SAPIC+ generation, our framework adds
an explicit semantic checkpoint that makes modeling decisions inspectable but
requires additional human effort. We evaluate workflow cost in terms of cell-level
edits, human inspection and repair effort, and model generation overhead. The
"Edits" column in Table 2 counts UI-level corrections to the generated IR before
SAPIC+ generation, including fixes to message fields, value provenance, role-
local knowledge, verification targets, and compromise assumptions. DeepSeek,
GPT-4o, and Llama require 72.3, 88.5, and 90.1 edits per protocol on average,
respectively, while GPT-5.5 averages only 0.7 edits and reaches highest proof
verification success. Smaller protocols such as Example, Toy, and Otway Rees
require relatively few edits, whereas larger and more complex protocols such as
KEMTLS, SPLICE, and SSH require substantially more corrections. This sug-
gests that model ability and protocol complexity directly affect the amount of
human repair needed at the IR level.
    We also report model generation and verification time in Table 2. We also
report model generation and verification time in Table 2. These measurements
record the observed end-to-end wall-clock time for translating the reviewed IR
into SAPIC+ and running Tamarin. However, the times are outcome-conditioned.
Failed runs may terminate before proof search, whereas accepted models may go
through the full verification process. The totals should therefore not be used to
directly compare efficiency across models. Together with the manual edit counts,
these results characterize the main trade-off of our framework: the Protocol IR
introduces an additional review step, but this step makes the modeling process
more transparent, repairable, and trustworthy.


4     Case Study
We further present a case study on KEMTLS, a protocol whose natural-language
description is difficult to translate directly into a formal model because sev-
eral protocol steps are described as phases and flights rather than as individual
messages. In particular, the input states:

      "In the same server-to-client flight as ServerHello, the server also sends
      a certificate containing its long-term KEM public key."

    This sentence is easy for an LLM to misinterpret. The initial LLM-generated
IR treated the server’s long-term KEM public key as if it were directly included
in the unprotected ServerHello message. As shown in Figure 4, the raw IR mod-
els the server response as a single plaintext M2 row, ⟨kem_encaps(pk(ske),˜ r̃e ),
pk(ltkS), rs⟩,
            ˜ thereby placing the KEM encapsulation, the server long-term
public key, and the server nonce in the same unprotected message. This loses an
important semantic distinction because ServerHello establishes the first shared
secret, whereas the server certificate is a later handshake item protected by the
16     S. Li et al.




Fig. 4: Raw IR fields for the partial KEMTLS review example. The raw IR
represents server flight as a single plaintext message row M2.



derived server handshake traffic secret. The review UI makes this error visible at
the IR level, but not by simply marking the raw M2 term as unsupported. The
cells of this row, such as ServerHello, the KEM encapsulation, the server public
key, and the nonce, are all mentioned in the source text. Thus, the Term and
Meaning cells receive strong evidence confidence. The ambiguity instead appears
in how those cells are assigned to protocol steps. In the raw IR, the "Checks"
field is marked as high priority: the "role" and "source message" cells for the
early KEMTLS checks are "must review", with review priority 100%, evidence
confidence 0%, and semantic impact 100%. During review, the user can repair
this by splitting the server flight into separate steps. The reviewed excerpt sepa-
rates M2, a plaintext ServerHello, from M3, an encrypted ServerCert protected
under SHTS. The reviewed IR therefore models M 2 = ⟨SERVERHello, cte, rs⟩ and
then M 3 = senc(⟨ServerCert, cert(pkS)⟩, SHT S).
    This repair also affects the later checks. The reviewed IR explicitly records
that the client first derives CHTS and SHTS from ServerHello, then decrypts
ServerCert, recovers the server KEM public key, and only then sends the client
KEM ciphertext and finished messages. These UI-visible edits prevent SAPIC+
generator from proving properties over a model in which the server authenti-
cation key is available at the wrong protocol point. After review, the gener-
ated SAPIC+ model compiles cleanly and Tamarin matches all five reviewed
KEMTLS target outcomes. This case illustrates why the IR layer is necessary.
Tamarin can verify a formal model against formal lemmas, but it cannot decide
whether a phrase such as "same flight" has been translated into the needed mes-
sage structure. The IR therefore acts as a human-auditable checkpoint between
natural language and formal verification.
    Confidence-Guided Protocol IR for LLM-Aided Security Protocol Modeling        17

5     Discussion
5.1     Non-standard Cases
To examine whether the workflow remains usable beyond textbook protocols, we
applied it to three additional security scenarios: MCP session hijacking, GitHub
Actions artifact provenance, and AWS external-ID delegation 5 Because unlike
benchmark protocols, these cases are described mainly through platform docu-
mentation, attacks, and mitigations rather than complete message sequences.

MCP session hijacking. The MCP case shows how the workflow converts a real
attack scenario into a model that can be checked automatically. The model cap-
tures both session-hijacking methods described in the source, including injecting
messages into a shared session queue and directly impersonating another session.
Tamarin reproduces both attacks and shows why they are possible. A request is
accepted when its session identifier matches, without first checking whether the
sender is authorized to use that session.


rule MCP_Receive:
 [ St_MCP(sid), In(call(sid_call, request)) ]
 -->
 [ St_MCP_Check(sid, sid_call, request) ]

rule MCP_CheckSession:
 [ St_MCP_Check(sid, sid_call, request) ]
 --[ Pred_Eq(sid_call, sid) ]->
 [ St_MCP_Accept(sid, request) ]

rule MCP_Accept:
 [ St_MCP_Accept(sid, request) ]
 --[ CallAcceptedAsSession(
       ’MCPServer’,’Attacker’,’Client’,sid,request) ]->
 [ ]


             Fig. 5: Tamarin MSR rules for MCP session acceptance.


    Figure 5 6 shows the key modeling choice of this attack. The received session
identifier is checked against the stored identifier, and the compiler-generated
predicate_eq gives this comparison its equality semantics. However, the autho-
rization lemma requires an earlier AuthorizedInboundRequest event, which is
absent from the acceptance path. The counterexample therefore shows that a
valid session identifier is sufficient to associate a request with a session, but not
to authenticate the sender.
    The verification results also need to be read according to the type of property
being checked. Tamarin verifies the two reachability lemmas because it finds the
5
  The implementation, reviewed inputs, generated models, and proof summaries are
  available at https://github.com/laplace1002/TamarinAgent.
6
  For readability, we alpha-rename only compiler-generated state facts and omit state
  arguments that do not participate in the illustrated decision
18      S. Li et al.

expected attack traces, while the authorization lemma is falsified by a coun-
terexample. Thus, the model captures both the intended attack paths and the
missing authorization check.

GitHub Actions artifact provenance. The GitHub Actions case compares three
artifact-selection policies. Selecting an artifact only by name allows an artifact
from another run to be substituted. Binding the artifact to the triggering run
prevents this cross-run substitution, but it does not guarantee that the run itself
came from a trusted source because a fork run can still be the triggering run.
The stronger trusted_origin policy therefore also checks repository and branch
metadata.


rule RunBound_Select:
 [ St_RunBound(producing_run, trigger_run,
               artifact, repo, branch) ]
 --[ Pred_Eq(producing_run, trigger_run),
     ArtifactSelected(’run_bound’, trigger_run,
                      artifact, trigger_run, repo, branch) ]->
 [ ]

rule TrustedOrigin_Select:
 [ St_Trusted(producing_run, trigger_run,
              artifact, repo, branch) ]
 --[ Pred_Eq(producing_run, trigger_run),
     Pred_Eq(repo, ’protected_repo’),
     Pred_Eq(branch, ’protected_branch’),
     ArtifactSelected(’trusted_origin’, trigger_run,
                      artifact, trigger_run,
                      ’protected_repo’,’protected_branch’) ]->
 [ ]


Fig. 6: Tamarin MSR rules for run-bound and trusted-origin artifact selection.



    Figure 6 highlights this distinction. The run identifier establishes which ex-
ecution produced the artifact, while the repository and branch checks establish
whether that execution came from an allowed source. As a result, run_bound
satisfies the run-provenance property but still admits a fork trace, whereas
trusted_origin blocks that trace. An executability lemma also confirms that
the stronger policy still allows a legitimate protected-branch deployment, rather
than achieving security by rejecting all deployments.
    Our workflow automatically identifies nine verification targets covering three
questions. Theses are whether a fork artifact can reach privileged use, whether
the selected artifact belongs to the triggering run, and whether that run has
a trusted origin. All nine results match the expected outcomes. Assuming that
the metadata used for these checks is authentic, the case shows that binding an
artifact to the correct producer run is not sufficient to establish that the run
originated from an authorized source.
    These non-standard cases highlight a different strength of the workflow from
the benchmark evaluation. Even without a complete reference model, it can
    Confidence-Guided Protocol IR for LLM-Aided Security Protocol Modeling           19

turn security assumptions described in natural language into explicit policy vari-
ants and verification targets. This makes differences such as session identity ver-
sus sender authorization, and artifact provenance versus trusted origin directly
testable. By checking attack reachability, safety, and legitimate execution sepa-
rately, the workflow also makes clear why a policy succeeds or fails rather than
reducing the result to a single verification outcome.

5.2     Limitations and Future Work
Our approach does not fully solve the problem of interpreting natural-language
protocol descriptions. If the source description omits important details, the sys-
tem may still require the user to supply missing assumptions. Moreover, the
quality of the generated IR depends on the ability of the LLM to identify rele-
vant protocol concepts and provide useful evidence. The confidence mechanism
can help expose uncertainty, but it cannot guarantee that all semantic errors
will be found. Finally, the current framework focuses on improving the modeling
workflow rather than proving the correctness of the IR-to-SAPIC+ translator.
A stronger implementation would require a more formal definition of the IR
semantics and a verified or systematically validated translation procedure.
    As future work, we plan to add a lightweight review step that compares
the generated model with the original description. LLM would check whether
the model captures the messages, checks, events, and compromise assumptions
stated in the description, and whether it introduces any behavior or assumptions
that the description does not support. It would also flag missing steps or changes
in their order. This could help users identify potential modeling errors.


6     Conclusion
This paper presented a confidence-guided Protocol IR for LLM-aided security
protocol modeling. By introducing an explicit semantic checkpoint between natural-
language interpretation and formal model generation, our approach makes criti-
cal modeling decisions inspectable, correctable, and auditable before formal ver-
ification. The confidence-guided interface further helps users focus on uncertain
and high-risk fields. Overall, the proposed trust boundary provides a practical
foundation for trustworthy LLM-assisted security protocol verification.


References
 1. Blanchet, B., Smyth, B., Cheval, V., Sylvestre, M.: Proverif 2.00: automatic crypto-
    graphic protocol verifier, user manual and tutorial. Version from 16, 05–16 (2018)
 2. Chen, Z., Cao, J., Xu, C., Cheung, S.C.: Modelwisdom: An integrated toolkit for
    tla+ model visualization, digest and repair (short tool paper). In: International
    Symposium on Formal Methods. pp. 211–219. Springer (2026)
 3. Cheval, V., Jacomme, C., Kremer, S., Künnemann, R.: {SAPIC+}: protocol veri-
    fiers of the world, unite! In: 31st USENIX Security Symposium (USENIX Security
    22). pp. 3935–3952 (2022)
20      S. Li et al.

 4. DeepSeek-AI: Deepseek-v4: Towards highly efficient million-token context intelli-
    gence (2026), https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro
 5. Fuggitti, F., Chakraborti, T.: Nl2ltl–a python package for converting natural lan-
    guage (nl) instructions to linear temporal logic (ltl) formulas. In: Proceedings of
    the AAAI Conference on Artificial Intelligence. vol. 37, pp. 16428–16430 (2023).
    https://doi.org/https://doi.org/10.1609/aaai.v37i13.27068
 6. Grattafiori, A., Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Let-
    man, A., Mathur, A., Schelten, A., Vaughan, A., et al.: The llama 3 herd of models.
    arXiv preprint arXiv:2407.21783 (2024)
 7. Hurst, A., Lerer, A., Goucher, A.P., Perelman, A., Ramesh, A., Clark, A., Os-
    trow, A., Welihinda, A., Hayes, A., Radford, A., et al.: Gpt-4o system card. arXiv
    preprint arXiv:2410.21276 (2024)
 8. Mao, Z., Wang, J., Sun, J., Qin, S., Xiong, J.: Llm-aided automatic modeling for
    security protocol verification. In: 2025 IEEE/ACM 47th International Conference
    on Software Engineering (ICSE). pp. 642–654 (2025). https://doi.org/10.1109/
    ICSE55347.2025.00197
 9. Meier, S., Schmidt, B., Cremers, C., Basin, D.: The tamarin prover for the sym-
    bolic analysis of security protocols. In: International conference on computer aided
    verification. pp. 696–701. Springer (2013)
10. Praitheeshan, P., Pan, L., Yu, J., Liu, J., Doss, R.: Security analysis methods on
    ethereum smart contract vulnerabilities: A survey. arXiv preprint arXiv:1908.08605
    (2019)
11. Wang, H., Zuo, X., Sun, Y., Li, Q., Ameur, Y.A., Dong, J.S.: Event-b agent:
    Towards llm agent for formal model synthesis and repair. arXiv preprint
    arXiv:2605.17475 (2026)
12. Yu, Y., Hou, Z., Dong, N., Dong, J.S.: Model checking nondeterministic be-
    haviours in the tendermint byzantine fault tolerant blockchain consensus pro-
    tocol. In: Zhou, Y., Teo, S.G., Xie, X., Ding, Z., Liu, Y. (eds.) Engineering
    of Complex Computer Systems - 29th International Conference, ICECCS 2025,
    Hangzhou, China, July 2-4, 2025, Proceedings. pp. 379–400. Lecture Notes in Com-
    puter Science, Springer (2025). https://doi.org/10.1007/978-3-032-00828-2_
    21, https://doi.org/10.1007/978-3-032-00828-2_21
13. Zhang, Y., Cai, Y., Zuo, X., Luan, X., Wang, K., Hou, Z., Zhang, Y., Wei, Z., Sun,
    M., Sun, J., et al.: Position: Trustworthy ai agents require the integration of large
    language models and formal methods. In: Forty-second International Conference
    on Machine Learning Position Paper Track (2025)
14. Zuo, X., Zhang, Y., Wang, H., Cai, Y., Hou, Z., Sun, J., Dong, J.S.: Pat-agent: Aut-
    oformalization for model checking. In: 2025 40th IEEE/ACM International Con-
    ference on Automated Software Engineering (ASE). pp. 2122–2133. IEEE (2025)
