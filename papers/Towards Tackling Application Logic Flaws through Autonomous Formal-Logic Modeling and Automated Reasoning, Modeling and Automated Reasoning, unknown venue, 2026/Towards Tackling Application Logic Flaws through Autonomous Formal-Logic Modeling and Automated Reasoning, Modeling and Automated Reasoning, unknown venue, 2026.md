                                            Towards Tackling Application Logic Flaws through Autonomous Formal-Logic
                                                               Modeling and Automated Reasoning

                                                            Yiwei Fang∗ , Yichen Liu† , Ze Jin∗ , Haoqiang Wang∗ , Qixu Liu∗ , Luyi Xing† ,
                                                                      ∗ Institute of Information Engineering, Chinese Academy of Sciences
                                                             ph4ng0t@rustysnow.org, jinze@iie.ac.cn, wanghaoqiang@iie.ac.cn, liuqixu@iie.ac.cn
                                                                                † University of Illinois Urbana-Champaign
                                                                                yichen59@illinois.edu, lxing2@illinois.edu
arXiv:2609.10537v1 [cs.CR] 9 Sep 2026




                                        Abstract—Logic flaws pose significant challenges in the design        traditional detection techniques like static analysis, dynamic
                                        and implementation of modern, semantically rich systems and           analysis, and fuzzing [3]–[9]. These flaws have severe impli-
                                        applications, impacting security, privacy, and trust. These           cations in domains like communication protocols, military
                                        flaws are inherently tied to business-specific semantics and          systems, and financial infrastructure, leading to unauthorized
                                        threat models, making their discovery and reasoning difficult         access, data corruption, and operational disruptions. For ex-
                                        and hard to scale. Real-world systems often exhibit diverse           ample, a 2023 logic vulnerability in Newag trains in Poland
                                        application features, complex protocol logic, and domain-             caused disruptions when third-party service providers un-
                                        specific threat models, necessitating substantial human effort        intentionally triggered manufacturer-enforced logic con-
                                        and domain expertise for effective security analysis. In this         trols [10], [11]. This case, uncovered by the ethical hacking
                                        paper, we introduce LL-Verifier, a novel, automated framework         group Dragon Sector, underscores the operational and finan-
                                        for identifying logic vulnerabilities built on (1) large language     cial risks posed by logic vulnerabilities in critical systems.
                                        models for autonomous modeling, and (2) logic model checkers          Challenges for detecting flaws in application-level
                                        for rigorous reasoning. LL-Verifier processes natural language        logic. Given an application or application-level protocol
                                        inputs, in particular protocol descriptions and security goals,       which usually comes with context-specific, domain-specific
                                        to automatically generate formal logic models and properties          semantics, prior formal methods based techniques including
                                        expressed in a new logic language built on a generic logic            model checking [12]–[17] and logic reasoning [18]–[25]
                                        language Maude, optimized for modeling arbitrary application-         struggle to scale and adapt to this diversity, leaving many
                                        level semantics. These formal models are then converted into          logic vulnerabilities undetected in complex, real-world
                                        logical state machines, enabling exhaustive, rigorous verifi-         applications, software, and cyber-physical systems. These
                                        cation through logic level model checking. This approach              limitations emphasize the need for novel approaches that
                                        streamlines the analysis of diverse, application-level protocols      can systematically reason about logic vulnerabilities across
                                        deployed in real-world scenarios, offering automated, exhaus-         varied semantic contexts.
                                        tive, and precise reasoning within their logical constraints. We          Our research focuses on flaws at the “application
                                        evaluated the high effectiveness, efficiency, and practicality of     level” (application logic, application-level protocols), in
                                        LL-Verifier by applying it to 27 access control protocols of          contrast to the “cryptography level.” In those prior works,
                                        widely used IoT devices, which come with vendor-specific logic        modeling a specific system, application or underlying
                                        flows and semantics. While LL-verifier tackles a hard problem         protocols involves identifying domain-specific, context-
                                        in application security, i.e., automatic logic flaws discovery, our   specific semantic elements that should be modeled, and
                                        analysis uncovers a range of sophisticated logic vulnerabilities      deciding how to model these semantic elements (e.g.,
                                        in IoT protocols and devices with serious security and privacy        defining data structures and operations using the syntax
                                        implications.                                                         supported by a modeling language) [26]–[30]. Existing
                                                                                                              formal modeling approaches struggle with automation,
                                                                                                              generality, and scalability. The prior modeling process has
                                        1. Introduction
                                                                                                              generally (1) relied heavily on manual effort or domain
                                            Logic vulnerabilities, known as logic flaws or business           experts for individual systems and protocols, and (2) been
                                        logic errors [1], [2], represent a critical challenge in de-          highly tailored to specific systems or domains to identify
                                        signing and implementing modern semantic-rich systems,                the necessary semantics for modeling. As a result, the
                                        affecting security, privacy, and safety. Unlike programming           resulting model is essentially a domain-specific model
                                        bugs, these vulnerabilities arise from design-level weak-             (DSM) and prior approaches have been largely unscalable
                                        nesses, such as flawed reasoning or incorrect assumptions in          across different applications and semantic domains.
                                        specific semantic contexts, targeting contextual logic rather         Research goals. To address both this fundamental gap in
                                        than code-level errors [3]. Consequently, they often evade            formal methods and critical security risks in system and pro-
tocol designs, this paper introduces a formal logic analysis          RQ2: How to design a formal logic language and
framework, namely LL-Verifier, a novel LLM-assisted ap-           modeling mechanism that can effectively find logic flaws
proach for autonomous formal logic modeling and logic flaw        by capturing customized application-level threat models?
reasoning. Given an application-layer protocol design and a       Security flaws are dependent on assumptions made for the
customized security goal, LL-Verifier aims to autonomously        protocol actors, including both benign and threat actors. We
generate domain-specific models in formal logic, and use          dub such assumptions as “threat models,” which define the
logic model checkers to automatically verify the specified        possible behaviors of benign actors and attackers. Model
goals against the target. Notably, it is not uncommon for pro-    checking is known to exhaustively traverse the entire state
tocol implementations to deviate from protocol design due         space, in which process a transitioning to the next state is
to intentional customization or specification ambiguity [31]–     triggered by a possible event (e.g., a user action) — this
[33]. However, it is critically important to directly analyze     process is known to be non-efficient (sometimes cannot
protocol designs to identify logic flaws in the system and        stop) and not truly scalable (e.g., state explosion [40]).
protocol design itself to elevate design-level security (this     When the enumerated user action is unrealistic or outside
research does not focus on flaws in protocol implementa-          the scope of a threat model of interest, the model checking
tions).                                                           process is non-efficient mixed with unuseful results (e.g.,
Research questions. For the above goals, we summarize             out of scope of the given assumption of interest).
specific research questions and their challenges as follows.          Based on the reality of diverse, often domain-specific,
     RQ1: What formal modeling approach can generally             semantic-dependent threat models that fundamentally devi-
enable autonomous modeling of diverse application-level           ate from traditional Dolev-Yao assumptions [3], [27], [29],
protocols with diverse and potentially arbitrary semantics?       [41]–[61], the novel challenge and our goal are: (1) design-
There are two categories of formal logic-based languages:         ing a generalized logic modeling framework that natively
generic logic languages (such as Maude [34], Tamarin [35],        supports domain-specific, custom threat models by easily,
Twelf [24], and Prolog [36]) and domain-specific logic            explicitly distinguishing deterministic protocol executions
language (DSL) [37]. DSL cannot easily adapt to diverse           from non-deterministic attacker events, and (2) ensuring
application-layer protocols, thus being highly limited in         this threat mechanism is structurally coherent with the core
scope of usage. Generic, foundational logic languages like        protocol modeling (e.g., events, rules, etc). Thus, the gener-
Maude are highly flexible in syntax and provide capabilities      ated threat model in the appropriate modeling language is
to flexibly define data structures and types used in modeling.    directly pluggable to the protocol DSM, making the entire
However, it is difficult for LLM to accurately generate           model ready for verification. Consequently, the reported vio-
semantic domain-specific models using highly generic logic        lations in DSM model checking strictly adhere to the defined
languages featuring highly customizable data structures and       application-level threats, ensuring analysis soundness.
types, while ensuring that the generated models are ready         Our approach. To address these challenges, we designed
to or can be verified, in particular, based on state-of-the-art   and implemented LL-Verifier, an automatic logical flaw
formal model checkers.                                            identification framework (§ 3). LL-Verifier introduces an
     This is because it is up to LLM to (1) define data           LLM-compatible modeling framework, Les, which features
structures and types for complex semantic elements (e.g.,         a novel “modeling guardrails” design tailored for LLMs
non-monotonic mutable states) and (2) implement mutual            and includes a Les model compiler (§ 2.5). The “modeling
operations and relations between semantic elements, and           guardrails” (FMG) ensure accurate and reliable LLM
consequently the generated models come with low accuracy          generation of formal models for application-level protocols.
and effectiveness to feed to state-of-the-art model checkers.     Les is designed with FMG principles, including foundational
Specifically, modeling a protocol is essentially to implement     symbols and types (§ 2.1), State-Transitional Logic Rules
the protocol’s core semantics (semantics of interest) using       for protocol rule modeling (§ 2.2), and Event Generation
the chosen modeling language. While pure semantic or              Rules for event modeling (§ 2.4). The Les compiler
functionality-level automatic implementation may become           translates Les formal models of protocols or applications
practical based on trending code LLM techniques [38],             into a rewrite theory [62], enabling the creation of logical
[39], downstream tasks specifically model checking, how-          state machines M (§ 2.5), and supporting non-monotonic
ever, require the modeling in specific paradigms, for in-         mutable states. This facilitates exhaustive and automatic
stance, as a logically, formally defined state machine with       model checking using off-the-shelf model checkers [63].
conceptually defined states and transitions. Without such             Given the textual representation of a protocol and a
definitions and regulations, model checking with respect          customized security goal, LL-Verifier reorganizes the infor-
to customized or semantic properties (e.g., linear temporal       mation into multiple components and formalizes each of
logic or LTL properties) cannot be rigorously defined and         them respectively to Les through the collaborative efforts
verified. To address the problems, this paper designs and         of Les formalization agents (§ 3.1). By employing LLM
implements a novel approach to enable LLM and its agentic         in-context learning (i.e., few-shots prompting) [64] and an
systems to autonomously generate DSMs for applications            embedded program analyzer, we ensure the reliability and
and application-level protocols of various semantics, while       accuracy of LLM responses (§ 3.2). Based on customized
ensuring that the models are directly ready to verify for         threat models and security goals, LL-Verifier adjusts the
context-specific security goals.                                  determinism/non-determinism of Les rules (§ 3.3.2) and sup-
port non Dolev-Yao application-layer threat model. Using                To address RQ1 and RQ2 and enable LLM to effectively
LL-Verifier, we specify trace properties in Linear Temporal        and accurately generate formal logic models that model po-
Logic (LTL). These properties are defined over proposi-            tentially arbitrary application-level protocols, we introduce
tions derived from the same Σ and are evaluated against            Les, a novel LLM-friendly modeling framework including
system states (§ 3.3.3). By verifying whether M satisfies          a LLM-friendly logic modeling language that features a
the negation of a trace property, LL-Verifier produces the         novel “modeling guardrails” design for LLM and a Les
corresponding attack traces.                                       model compiler. Our design intuition is that although logic
Evaluation and findings. We have used LL-Verifier to               language must be general and flexible enough to support
model and reason about IoT devices and applications of             potentially any application semantics, meanwhile, it ought
28 IoT vendors (such as iRobot, Google Home, Aqara, see            to come with “guards” on the format and structures in
Table 2), show that our techniques are effective and and           modeling semantic elements (of the protocols) and how the
practical (§ 4). Specifically, across 27 unique devices , LL-      semantic elements may impact each other in a transition-
Verifier found 35 logic flaws; this includes 30 previously         system paradigm. Those “guards” are essential to ensure
unknown logic flaws among 23 vendors. We implemented               that LLM can accurately and successfully generate formal
proof-of-concept attacks on real devices of ours for all the       models in the way we aim to model arbitrary application-
new flaws (§ 5). We responsibly reported all zero-day flaws        level protocols — called Logical State Machine or LSM
to affected vendors. The Connectivity Standards Alliance           (§ 2.5). We call those “guards” for highly generic modeling
(CSA, the organization that manages the emerging IoT stan-         language as formal modeling guardrails (FMG). Design of
dard Matter [65]) and 14 vendors such as August, Philips,          FMG is novel, distinguishing Les from other general logic
and Tuya have acknowledged the flaws and are releasing             languages or modeling languages like Maude and Tamarin
patches.                                                           and prior modeling approaches [34], [35], [66]–[71].
    To further evaluate coverage and accuracy of LL-                    In the following, we elaborate on the design of Les
Verifier in modeling application-level protocols, we devel-        focusing on FMG including foundational symbols and types
oped Logic-Modeling Bench, a novel benchmark including             in the logic language denoted as Σ that we expect LLM
the textual specifications and formal models of 29 applica-        to use in modeling (§ 2.1), State-Transitional Logic Rules
tion level protocols, including those of 24 IoT and mobile         for LLM to model protocol rules that are both determin-
vendors (such as iRobot, Philips, Tuya) and 5 protocols            istic and trusted in protocol execution and those that are
from prior papers (§ 4). Given those protocols, we eval-           not (dependent on threat model of interest, § 2.2), Event
uate the coverage and accuracy in modeling the protocols’          Generation Rules for LLM to model event generations that
semantics elements, including subjects (i.e., principals, e.g.,    are supported in the protocol.
users, clients, devices, servers), events (e.g., actions and API        While these FMGs along with the Les language are de-
requests supported in the protocol), attributes of the subjects    signed to be general, we implemented the Les language with
and events, and protocol rules. Our evaluation shows that          FMGs using the EBNF [72] (extended Backus–Naur Form,
LL-Verifier achieved high coverage in modeling semantic            a metasyntax notation for formally specifying the syntax)
elements and high accuracy.                                        with 27 lines of code [73]. In § 3, we elaborate our Les
                                                                   LLM agents that take Les’s EBNF specification and target
Contributions. We summarize the contributions as follows:
                                                                   protocol’s textual specification as input, and autonomously
• New techniques. We present LL-Verifier, a novel approach         generate formal models in the target Les logic language. To
and tool for autonomous formal modeling of system                  enable execution of and fully automatic model checking on
and application designs of various semantic contexts               Les formal models, Les additionally includes a Les compiler
into domain-specific models (DMSes), and automatically             to convert the Les formal model (of a target protocol or
detecting application-level logical flaws based on formal          application) into a rewrite theory [62], in the syntax of
model checking.                                                    Maude modeling language. A rewrite theory is known to
• New benchmark. We introduce Logic-Modeling Bench, the            be able to be directly mapped to a state-machine, called
first benchmark to evaluate autonomous formal modeling             logical state machine (LSM) in our task, and can leverage
of application-level protocols with varied semantics across        the off-the-shelf Maude model checker [63] for exhaustive,
vendors and application domains.                                   automatic model checking for our models. We elaborate on
• New findings. We applied LL-Verifier to model and ana-           the Les compiler and LSM definition in § 2.5. Our Les LLM
lyze logic flaws in 27 real devices, uncovering the sophisti-      agents and automatic model checking are elaborated in § 3.
cation and pervasiveness of these flaws in IoT protocols and
diverse application scenarios, highlighting the fundamental
threats posed by logic flaws, which are difficult to avoid         2.1. Foundational Logic Symbols and Types
in the design space of IoT systems and potentially other
systems.                                                               In Les, our logic language, denoted as Σ, is designed
                                                                   to have (1) basic symbols and types inherit from prior
                                                                   generic logical languages, and (2) guardrail symbols and
2. Les: A Logic Modeling Framework                                 types that can be flexibly, effectively used by LLM (also by
                                                                   human of course) to specify and model semantics elements
in application-level protocols. The guardrail symbols and            with some Arguments along with the action. For exam-
types are essential to help formulate (1) principals (e.g.,          ple, userA 'pressButton' deviceB denotes that userA
users, devices, clients, servers) in applications and protocols;     presses the button of deviceB , where 'pressButton' is
(2) the principals’ internal states (i.e., attributes, data/knowl-   an action (of sort Action). In our design of Σ, the sort
edge); (3) events that can occur in the application or protocol      Action is general and can additionally model API calls; we
(e.g., operations performed by principals).                          define the sort Arguments as a list of Items, intuitively
                                                                     being arguments related to the action. For example, the
                                                                     Event $U serX 'callAP I : bind' cloudA | KeyA
2.1.1. Basic Symbols and Types. Data types. Based on                 denotes that any user U serX calls the API “bind” of the
basic types previously used in logic, including Bool, Qid            cloud namely cloudA with an argument KeyA. Notably, the
(quoted identifier or String), Nat, Set (we use nils to express      above examples are all from our specification of the iRobot
an empty set), List, etc., Σ defines a generic sort DataItem         protocol using Les.
(or simply Item), and prior basic types Bool, Qid, and
                                                                     Logical State. In Les (Σ), we define the syntax
N at are subsorts of Item. Σ further defines a subsort of
                                                                     < P rincipal1 | Attributes >< P rincipal2 | Attributes >
Item, namely sort P air to model key-value pairs, denoted
                                                                     ......   < P rincipaln | Attributes >         to  denote     a
as K : Y where K is of sort Key and Y is of sort Set. A
                                                                     Logical State, which includes the internal states of
Key is a Qid (String).
                                                                     multiple principals that are considered in modeling and
                                                                     analyzing the protocol.
2.1.2. Guardrail Symbols and Types. Principals. In Σ,                Syntactic sugar. Les comes with a few intuitive syntax
we define P rincipal as a type (called sort in the algebraic         symbols that can be used like syntactic sugar to improve
specification community), and we define U ser, Device, and           expressiveness. For example, “...” is a variable of sort
Cloud as subsort of P rincipal (i.e. every instance of the           Set, which can be seen as a wildcard in pattern-matching
sort U ser is a P rincipal).                                         Attributes of the principals (see a detailed example in § 2.2).
    Σ considers the set of data items (Items). For                        Note that this section focuses on the syntax and in § 2.2
example, the set {'localT o' : deviceB, 'know' :                     and § 2.3 we will elaborate on how to use these sorts
('SecretC ', 'SecretA')} contains two P airs which have              and syntax to model protocols underlying real application
key 'localT o' and 'know' respectively. In this example,             scenarios.
Σ used “,” as a union operator to concatenate Items to form
a bigger set, which satisfies idempotency, associativity, and        2.2. State-Transitional Rules to Model Protocol
commutativity properties.
                                                                     Rules
Attributes and Internal State of Principals. Each principal
has internal states (or InS ), and the internal states are                A principal’s actions in protocols and applications (e.g.,
modeled by attributes of the principal. Specifically, Σ              IoT binding [75], delegation [27]) can have side effects,
defines the syntax < P rincipal | Attributes > to specify            leading to reactions of other principals and changes of their
an internal state of the P rincipal, with the delimiter              internal states. For example, a user makes an API request
| which can be read as “with”, followed by the sort                  (along with a binding key) to the cloud to bind with a device,
Attributes. Σ defines the sort Attributes as a set of data           and correspondingly the cloud principal internally updates
items (Item). For example, < U serX | 'localT o' :                   the recorded binding status of the device and records the
deviceB, 'bindingStatus'             :    true, 'know'       :       binding key.
('SecretA', 'SecretC ') >, being a logical proposition,                   To formulate protocol rules in diverse application
denotes an internal state of the user namely U serX : intu-          protocols, we introduce state-transitional rules to model
itively, she is local to the device named deviceB, her binding       the logical rules of application protocols in the form of
status is “true”, and she knows “SecretA” and “SecretC”.             premise → conclusion. State-transitional rules are de-
    The logic expressions in Σ can include variables (like           signed by modeling the principals’ changes in their internal
in first-order logic). For example, < cloudA | 'bdKey ' :            state corresponding to protocol-supported events (e.g., spe-
KeyA, 'owner' : U serX > denotes the internal state of               cific user actions or API requests with certain arguments).
the Cloud namely cloudA, which has a ‘bdKey’ (intuitively            By default, state-transitional rules for all rules of the target
binding key) whose value is variable KeyA and the ‘owner’            protocol are denoted with the general → sign. Meanwhile, a
is U serX .Based on the logic convention [74], names that            novel design here is that we ought to differentiate “determin-
start with an upper-case letter is a variable (e.g., Key1,           istic” protocol rules that are trusted to execute (rules defining
U serX ). In contrast, cloudA that starts with a lower-case          expected changes or actions of a trusted principal) and
is a constant denoting the principal named “cloudA”.                 “non-deterministic” protocol rules that may not necessarily
Actions and Events. In systems like IoT, a principal may             be executed (rules defining expected changes or actions of a
                                                                                                                     r
perform actions (e.g., operate the device). Σ defines the            non-trusted principal). In Les, we designed → (compared to
syntax $ P rincipal Action P rincipal | Arguments to                 →) to denote “non-deterministic” rules. Essentially, whether
denote an Event, where the principal followed by a $ sign            a protocol rule is “deterministic” or not depends on the threat
performs an action towards the other principal, optionally           model of interest. In § 3, when we provide a customized
threat model (arbitrary principals being trusted or not) to
our model-generation LLM agent along with the protocol
                                                                       < DeviceY | 'key ' : KeyB, 'pressed' : true, ... >
specifications, our agent is able to automatically generate
                                          r                           $ U serX 'callAP I : setKey ' DeviceY | KeyA
and differentiate rules of the two kinds (→ and →). Rule 1           → < DeviceY | 'key ' : KeyA, 'pressed' : f alse, ... >
and 2 show examples in modeling iRobot devices’ protocol.             $ DeviceY ′ callAP I : setKey ′ cloudA | KeyA         (3)
    < cloudA | DeviceY : ('bdKey ' : KeyB, ...) >                     Normally, U serX may additionally call the API “reset”
   $ DeviceY 'callAP I : setKey ' cloudA | KeyA                   using the same key KeyA (Line 2 in Rule 4), which will
  → < cloudA | DeviceY : ('bdKey ' : KeyA, ...) >           (1)   make the cloud reset the binding status of the device by
                                                                  setting the “owner” key’ value as nils (Line 3 in Rule 4).
    In Rule 1, Line 1 abstracts an internal state of the          Full model specification of the iRobot RTE protocol can
cloudA: the cloud recorded for a device (matched by               be found in our website [73].
variable DeviceY ) a binding key KeyB . Line 2 is an                < cloudA | DeviceY : ('bdKey ' : KeyA, 'owner ' : OwnerX) >
event (starting with $) where the device calls the API to set      $ U serX 'callAP I : reset' cloudA | (DeviceY ; KeyA)
a binding key KeyA. The → means implification: based              → < cloudA | DeviceY : ('bdKey ' : nils, 'owner' : nils) > (4)
on Rule 1, the cloud internal state and device event will be
rewritten with a new internal state of the cloud (after the
→ sign at Line 3): the cloud replaces KeyB with KeyA              2.4. Modeling Protocol Events Generation
as binding key of the device (intuitively, the cloud will no
longer recognize KeyB ). Notably, here the simplification              Earlier, we leverage state-transitional rules for model-
in our Les is powerful and flexible in the sense that, it         ing the protocol rules (§ 2.2). Still, we need a non-trivial
can pattern-match a fragment of the cloud’s internal state        design to model the generation of protocol-relevant events,
specified using the pair 'bdKey ′ : KeyB , regardless of          considering that (1) generation of many events (e.g., a user
other attributes and values in the cloud’s internal state         operation) is conditional; (2) depending on the threat model
(specified using syntax “...”, like a wildcard, a variable of     of interest, generation of events is often non-deterministic
sort Set developed in Σ).                                         (by non-trusted principals) while generation of other events
                                                                  (by trusted principals) can be deterministic. Intuitively, being
  < cloudA | DeviceY : ('bdKey ' : KeyA, 'owner ' : nils) >       conditional means that the event that a principal may gen-
 $ U serX 'callAP I : bind' cloudA | DeviceY ; KeyA
                                                                  erate is not completely arbitrary; for example, a principal
→ < cloudA | DeviceY : ('bdKey ' : KeyA, 'owner ' : U serX) >
                                                            (2)   cannot make an API request along with secret argument
                                                                  values that he has not known. Moreover, an event being
    Intuitively, Rule 2 denotes that, when the cloud’s            “non-deterministic” is to consider that a principal especially
internal state already recognizes any KeyA for the device         untrusted principals may perform arbitrary actions as he
which has no owner (Line 1), once any user U serX calls           can, strategically (or unintentionally) out of protocol-regular
the “bind” API of cloudA with the same KeyA, the cloud            order and using arbitrary arguments based on his knowl-
will update its internal state by changing the device owner       edge. By default, event generations are modeled as non-
from empty (denoted as nils) to U serX (Line 3).                                                             r
                                                                  deterministic rules in the form of s −→ e with s and e
                                                                  specified using the Les: s characterizes and matches certain
2.3. A Running Example of iRobot                                  states (a collection of interested principal’s internal states)
                                                                  in the protocol’s execution; depending on the principals’
                                                                  logical state, the rule yields e that specifies a possible new
    Based on the design of our state-transitional rules, we       event to be performed by a principal.
formally specified the complete application protocol rules             For example, the event generation rule (formula 5) spec-
of establishing root trust (RTE) for iRobot devices [76]. In      ifies that at any logical state where there are any DeviceX
iRobot’s protocol, if any U serX and the DeviceY present          and any U serX whose knowledge (part of his internal
to the cloud the same arbitrary binding key KeyA, the cloud       state) includes any string K (regardless of the set of other
                                                                  information in his knowledge, denoted by a variable Keys),
establishes an internal state where U serX is the owner of        the rule will generate an event to call the API “bind” using
DeviceY (Rule 2). The normal process of the iRobot proto-         the argument K .
col starts when a user presses the button on the device, and         < U serX | 'know' : (K, Keys), ... > < DeviceY | ... >
then the device accepts a new binding key KeyA that she                 r
                                                                     −→ $ U serX 'callAP I : bind' cloudA | (DeviceY ; K)      (5)
can send using her iRobot app (Rule 3). This is a mechanism          < U serX | 'know' : (K, Keys), ... > < DeviceY | ... >
developed by iRobot for the user and device to share a secret         r
                                                                    −→ $ U serX 'callAP I : reset' cloudA | (DeviceY ; K)      (6)
binding key. After that, then the device will automatically set
KeyA to the cloud (Last line in Rule 3). This will lead to the      Even from the same logical state, a principal especially
cloud recording the KeyA to its internal state (attributes)       untrusted ones may alternatively perform other actions, e.g.,
for the device (Rule 1). Then if any U serX presents the          line 2 in Equation 6. For example, LL-Verifier automatically
same key to the cloud by calling API “bind”, the cloud will       creates 7 event generation rules for modeling the iRobot
record the U serX as the owner (Line 3 in Rule 2).                protocol. In execution of the logic state machine (§ 2.5), our
LL-Verifier will exhaustively generate possible events using        event). Automatic model checking will then apply equa-
the protocols’ non-deterministic event generation rules,            tional rules in R on s′ to transition to a new LSM states.
dependent on the specific logic states such as principal
knowledge in the state. Additionally, Les supports modeling         3. Autonomous Les Modeling and Formal Rea-
events being “deterministic” to generate if the principals
(to generate the events) are trusted depending on the threat
                                                                    soning
                                     r
model. This is done by replacing −→ with →.
                                                                         This section elaborates on our design and implementa-
                                                                    tion of LL-Verifier, a novel logic flaw detection framework
2.5. Les Model Compiler                                             that is empowered by LLM and is capable of (1) autonomous
                                                                    generation of Les models from protocol specifications and
Making Les models executable. With novel design in                  threat model descriptions (in natural languages), (2) auto-
Les, including FMGs designed as foundational types and              matically compiling Les models into LSM using our Les
symbols, state-transitional rules, and event generation rules,      model compiler (see § 2.5), and (3) performing automatic
Les achieves a high degree of expressiveness and guardrail          logic model checking on our LSM models with respect to
guidance for modeling, enabling concise and precise model-          provided threat model of interest and reporting logic flaws
ing of a wide range of application protocols while enabling         in the application protocol under verification. We provide an
LLMs to automatically generate Les models (§ 2.1) based             overview of LL-Verifier in § 3.1 and elaborate on the design
on our FMG implementation in EBNF. Still, a challenge is            in § 3.2 and 3.3. We implemented LL-Verifier and released
how to make Les models executable for automatic model               its source code online [73]. In § 4, we report our thorough
checking on Les models.                                             evaluation of LL-Verifier, based on Les.
    To address the challenge, we developed a Les model
compiler (intuitively “converter”) that translates a Les            3.1. Overview of LL-Verifier
model into a rewrite theory with a syntax compatible with
the generic Maude logic language, which is thus executable              Figure 1 outlines the architecture of LL-Verifier’s analy-
by the off-the-shelf Maude model checker [63]. Specifically,        sis pipeline, which is designed to autonomously translate
all deterministic rules are translated into equational rules E ,    protocol designs into formal models and conduct model
non-deterministic rules are translated into rewrite rules R,        checking to uncover application-layer logic flaws. The
and data structures and types remain unchanged. Notably,            pipeline consists of three phases, including autonomous
we also support cryptography primitives and operations              formalization, Les Model building with automated repair,
as equational rules built-in our tool (not protocol specific)       and Logical Model Checking.
like Tamarin [35]. The resulting rewrite theory (Σ, E, R)           Input pre-processing. Before LL-Verifier’s fully automatic
corresponds to a state machine [77], called logical state           formal modeling and reasoning, LL-Verifier employs a semi-
machine (see definition below).                                     automatic pre-processing phase to better organize and struc-
Logical State Machine. The LSM model is defined as                  ture the raw input. The pre-processing component is devel-
a logical transition system denoted as M = (S , s0 , T R,           oped as an LLM agent called the specification preprocessing
R). S is the set of states (also called LSM states). Each           agent that groups the textual descriptions from the input into
state s (s ∈ S ), formulated as s = e @ ls, comprises (1) a         four semantic segments (without changes to the original
logical state ls of all principals of interest in the application   descriptions in the sentences): (1) texts describing rules
protocol (e.g., a set of clients, devices, servers and clouds,      in the protocols, (2) texts describing how (when and on
also see the sort Logical State in § 2.1) and (2) the most          what conditions) events can be generated in the protocol,
recent event e that occurred and has driven the logical state       (3) texts related to the considered initial state of the pro-
changes to yield ls.1 Essentially, each state comprises the         tocol’s operation, and (4) texts related to the threat model
logical propositions (principals’ internal states, events) that     of interest and desired security properties. Following this
hold at the state. The s0 is the initial state, whose event is      step, we involve human in the loop to check the results:
empty, denoted as idle. T R denotes the transition relation         in particular, we manually ensure that descriptions of each
T R : S × S . From any current state sc , a state transition t      protocol rule should include at least three elements: pre-
(t ∈ T R) is driven by a new event occurring enew (e.g.,            conditions (optional), events (including actions), and post-
a client’s action). Notably, The possible new events that           conditions of the events/actions. Essentially, a protocol rule
can occur to the state sc are modeled by rewriting rules R          should describe both conditions and consequences of the
(particularly those converted from the event generation rules,      events/actions supported in the protocol.
which look like event generation rules with a syntax like               For each target protocol or system, the pre-processing
E @ ls ⇒ e @ ls e instead of s → e, to be compatible with           phase transfers raw textual descriptions to organized texts
Maude model checker). In R with event generation rules              as input to LL-Verifier. We provide the pre-processing
such as rule 5, Line 2 essentially derives a new intermediate       output for the iRobot protocol in Appendix Figure 3. Our
state s′ = enew @ ls enew (here, enew denotes the generated         Logic-Modeling Bench (§ 4) includes the raw descriptions,
                                                                    organized texts, and formal models of 29 unique protocols
  1. @ is a syntactic sugar designed and implemented in Les.        of 28 IoT and mobile vendors.
                                                 Figure 1: LL-Verifier overview


Autonomous modeling and formal reasoning. Taking the               invokes a light-weight program analyzer we developed to
(organized) input, LL-Verifier’s formalization component au-       find all principals from state transitional rules and for each
tonomously generates Les models. The formalization com-            principal, generate a full internal state template (or simply
ponent is built with a set of collaborative Les formalization      state template) that models all their attributes that have been
agents, each powered by an LLM. Each Les formalization             found in the state transitional rules (all attributes that are
                                                                   relevant to the principal in the target protocol, with each
agent processes one of the four semantic segments from the         attribute represented as a set of all possible data types).
input and respectively generates Les formal representations        For example, by combining rules 1 and 2, the program
of state-transitional rules, event generation rules, an initial    analyzer computes a state template for the principal cloudA
Logical State (for related principals of interest that should be   as follows:
mentioned in the threat model), and the security properties.
                                                                   < cloudA | DeviceB : ('bdKey ' : [Qid], 'owner' : [U ser]) >
    In the final Logical Model Checking component, the
Les model compiler converts the Les models including the             Based on the templates, AgentE processes the texts for
modeled security properties into a rewrite-theory represen-        event generation (produced by the Preprocessing component
tation (LSM) using the Maude-compatible syntax. Then the           of LL-Verifier) to produce the event generation rules for
sub-component called LSM runner employs the Maude LTL              the protocol. Using the templates that come with protocol-
Logical Model Checker [63] for automatic model checking            specific attribute names and event names already used by
on our models with respect to the security properties.             AgentS ensure that event generation rules generated by
Implementation and open-source release. We imple-                  AgentE reuse the same names. Similarly, AgentE generates
mented LL-Verifier using 2564 lines of Python code and             event templates for each named event that are found in state
157 lines of Maude code. We released the source code and           transitional rules; this ensures AgentE to reuse the event
related prompts used by the agents online [73], [78].              names already used by AgentS .

3.2. Autonomous Protocol Modeling in Les                           3.2.2. Guardrail Agents for Grammar and Semantics
                                                                   Correctness. To ensure modeling correctness and effec-
3.2.1. Formalization Agents. The formalization component           tiveness, LL-Verifier developed novel guardrails techniques
comes with multiple LLM agents that translate natural lan-         built on reflection agents [39]: each Formalization agent
guage texts grouped and organized by the pre-processing            such as AgentS and AgentE is accompanied with a “model
phase into Les formal models.                                      guardrail” agent that evaluates whether the agent generates
Agent for State-Transitional Rules (AgentS ). Among mul-           proper model code with correct Les grammar and respect to
tiple agents in the Formalization component, first, AgentS         goals defined in its system prompt. With the feedback, each
works by processing the texts describing protocol rules.           formalization agent iteratively improves results until they
Given an arbitrary application protocol with protocol-             are approved by its “model guardrail” agent. We elaborate
specific semantic elements and attributes for its principals,      on the approaches below.
AgentS actually generates rules that include those protocol-       Guardrail of modeling grammar. While recent develop-
specific principals, attributes of the principals mentioned in     ment of grammar-constrained decode (GCD) [79]–[93] can
the specification as long as they impact protocol operation.       ensure output of LLMs to strictly conform specified formal
For example, in the running example of iRobot (§ 2.3),             grammars, this can introduce performance overhead and
the user and device are relevant principals; their keys and        cost in producing output. Likely for these reasons, GCD
the “pressed” status are relevant attributes that affect those     techniques have not been widely deployed. For example,
principals and their events to generate. Essentially, AgentS       OpenAI supports strict JSON in output [94], but has not
models domain-specific protocol rules autonomously.                deployed support for arbitrary formal grammar. To help
Agent for Event Generation Rules (AgentE ). AgentS                 our formalization agents generate models that confirm to
takes the state transitional rules produced by AgentS and          Les grammar, we developed a set of practical approaches
into LL-Verifier. First, these agents all leverage the EBNF        with Linear Temporal Logic operators, which can model
specification of Les grammar as part of their system prompts       the relation across time, like ”Eventually, there is a state
to LLM , which helps regulate grammar of the generated Les         that userC is not local to deviceB and userA is the owner
models. Second, we leverage the aforementioned “model              of deviceB , and the next state userC is still on the remote
guardrail” agent (our reflection-agent) that evaluates Les         and the userA is not the owner of deviceB .” (sv1 ).
grammar of the generated model by the specific agent, and              By formulating individual LSM state as e @ ls as § 2.5,
provides the grammar errors and possible repair guidance           we records the most recent event in LSM state, enables
                                                                   defining both state property and event property. Formula
to the agent to regenerate grammar-correct models. Inside          e @ LS ⊢ p = true where LS is a variable to match
the “model guardrail” agent, the grammar check is built            whatever logic state defines that only e is the most recent
on the Python Lark library, which can accept an arbitrary          event that the primitive proposition p (primitive propositions
EBNF specification and rigorously check and report gram-           are the most simple properties and can build more complex
                                                                   properties with Logic operators) is evaluated to true at
mar errors. In our current configuration, for each protocol,       current LSM state. Similarly, E @ ls ⊢ p = true where
the “model guardrail” agents run up to three times to help fix     E is an event variable defined that when proposition p is
grammar errors. This is already sufficient to ensure grammar       true at the LSM state by matching ls. Subsequently, the
correctness for all 29 unique protocols across 28 IoT and          aforementioned uaOwner and uaP ress can be formalized
                                                                   as follows:
mobile vendors we studied (see § 4).
                                                                     • E @ LS < cloudA | 'deviceB ' : ('owner' : userA, ...) > ⊢
Mitigating hallucinations in semantic modeling. Based                  uaOwner = true
on semantic level inspection by guardrail agents, the for-           • userA ′ pressButton′ deviceB @ LS ⊢ uaP ress = true
malization agents come with iterative repairs of the models
for semantic correctness. During development, we observed              The operator syntax ⊢ comes with the underlying model
several recurring hallucinations and mistakes. Even though         checker MLMC (maude LTL model checker [63]), being
the context-free grammar is often guaranteed, the modeling         generally used to define a logic proposition (of sort P rop
result from LLM could still obey the semantic requirements         in MLMC). To make MLMC recognize LSM state, an
of Rewriting Logic or Les. For instance, Rewriting Logic           LSM state is defined as a general sort State of MLMC.
mandates that all variables on the right-hand side (RHS)           In this way, while LL-Verifier instantiates all LSM states
of a rule must also appear on the left-hand side (LHS).            (see model checking in § 3.1), LL-Verifier is capable of
To mitigate these issues, our high-level strategy involves:        leveraging MLMC to reason about each LSM state and
(1)Reducing LLM workload by allowing certain repairable            evaluate the primitive propositions. Based on whether or
errors and correcting them post hoc. (2)Predefining common         not related propositions hold at one LSM state or a state
error-repair patterns; LL-Verifier applies an iterative repair     trace, LL-Verifier can identify counterexamples of the prop-
loop to refine LLM outputs. When an error pattern is               erties. Similar to uaOwner and uaP ress, other primitive
detected, LL-Verifier triggers the corresponding repair            propositions can be defined (Appendix Table 1).
routine. Examples are provided in Appendix B.
                                                                   3.3.2. Modeling Threat Models in Les. Unlike traditional
3.3. Threat Model and Security Goals in Les                        network-layer analysis that universally assumes a Dolev-
                                                                   Yao attacker, application-layer protocols rely on determin-
    To address RQ2, LL-Verifier supports as input domain-          istic logic flows (rather than network anomalies like packet
specific, flexibly customized threat models and security           loss or delay) and face highly context-specific threats (e.g.,
goals, and models them in Les. We first introduce the              a malicious guest user, a compromised cloud node, or a
modeling of primitive propositions(§ 3.3.1), then present the      physically proximate attacker). To precisely capture these
threat model specification and the underlying mechanisms           diverse threat models, we design the following mechanisms.
for constraining state exploration in Les (§ 3.3.2), and finally
describe how security goals or properties are encoded as               When generating formal Les models from texts, protocol
Linear Temporal Logic formulas in Les (§ 3.3.3).                   state-transition rules are deterministic, while event genera-
                                                                   tion rules are non-deterministic by default, unless explicitly
3.3.1. Modeling Primitive Propositions in Les. Consid-             specified otherwise using a strong directive (which can be
ering the diversity of domain-specific threat models and           identified cues and tune of the texts by LLMs). During
security properties, one should be able to model properties        preprocessing, the determinism or non-determinism of rules
on (1) states, (2) events and (3) state traces. State properties   can be adjusted according to specified threat models. By
are the properties that depend on the current logical state        designating a party as untrusted within threat models, LL-
including all internal states of interested principals in the      Verifier converts all rules associated with the principal to
protocol, like “userA is the owner of deviceB” (referred as        non-deterministic ones. Furthermore, threat models support
uaOwner), “userC is remote to deviceB” in the iRobot pro-          the explicit specification of rules to fine-tune the deter-
tocol. Event properties are the properties that depend on the      minism or non-determinism of protocol rules with greater
event that happened, like ”userA press the physical button         granularity. Rules explicitly defined in a threat model take
of deviceB” (uaP ress) , and ”userA reset the deviceB”.            precedence over and override those in the protocol that
The above properties care about individual LSM state,              share identical premises. This functionality is achieved by
while trace properties are defined above those properties          treating both threat models and protocol models as sets of
rules, which are subsequently merged into a unified set (                    3.4. An Attack Trace in the iRobot Protocol
Algorithm online [73]).
    Furthermore, LL-Verifier supports explicitly defining                    Logic Flaw Type 1. We illustrate a counterexample vio-
complex attacker capabilities by modeling how an adver-                      lating sv1 in iRobot’s protocol (§ 2.3). After a legitimate
sary’s actions interleave with a benign user’s deterministic                 owner userA binds to deviceB , a malicious userC with
sequence. For instance, in the iRobot root trust establish                   temporary physical access presses the device button. This
(RTE) protocol, an attacker might have prior or concurrent                   forces the device to accept a rogue KeyA from userC ’s
physical access to a device. To demonstrate the generality of                app and synchronize it with the cloud. Subsequently, userC
our approach in modeling such constraints, we define benign                  remotely invokes the “reset” API using KeyA, erasing the
user valid operation trace, and attacker’s non-deterministic                 legitimate owner’s cloud record. Full implementation traces
events. Using primitive propositions (mentioned in 3.3.1                     are available online [73].
and Appendix Table 1), LL-Verifier formalizes it in Linear
Temporal Logic to rp as follows:                                             4. Evaluation
 □(uaP ressButton → ⃝(ucOperationW(uaCallSetKey ∨ uaReset)))                     We used LL-Verifier to automatically model and verify
 ∧ □(uaCallSetKey → ⃝(ucOperationW(uaCallBind ∨ uaReset)))                   multiple classes of proprietary protocols of 28 vendors,
     ∧ □(uaReset → ⃝(ucOperationWuaP ressButton))                      (7)   including IoT RTE (§ 5), IoT interoperability (§ 5.2), and
     ∧ □(uaOwner → ¬ ⃝ uaOperation)
                                                                             collaborative IoT access control (§ 5.3) under the following
     ∧ □(⃝uaReset → (uaCallBind ∧ ¬uaOwner))
                                                                             threat model.
     In formula 7, we present this threat model into                         Threat model. We consider realistic IoT threat scenarios
LTL using standard temporal operators: □ (Globally),                         built on prior works in studying different IoT protocols [27],
⃝ (Next), and W (Weak Until). It encodes this threat                         [57], [59], [60]. To analyze application-layer logic flaws, we
model in LTL, bounding an untrusted attacker’s arbi-                         consider that the IoT cloud infrastructure and systems are
trary actions (ucOperation) within the benign user’s                         benign (the cloud, management console, and device hard-
(ua) deterministic sequence (e.g., uaP ressButton →                          ware and firmware); the adversary cannot eavesdrop on or
uaCallSetKey → uaCallBind). By combining the ⃝                               interfere with the communication of other users’ devices and
and W operators, we formally define interleaving win-                        apps. Some older generations of IoT designs assume that
dows. For instance, the clause □(uaP ressButton →                            whoever has physical access to the device may reset or bind
⃝(ucOperation W (uaCallSetKey ∨uaReset))) dictates                           with the device. Hence, we do not focus on the adversary
that the attacker can non-deterministically inject operations                who resets or binds with the device when he has physical
strictly between the user’s legitimate button press and the                  access to the devices, which are well-known attacks, less
subsequent expected state or device reset.                                   stealthy and even assumed. However, if he comes once, and
                                                                             is able to either break the owner’s binding or bind with the
3.3.3. Modeling Security Goals/Properties in Les. Cur-                       device anytime after he leaves, this is a violation of security
rently we support two security goals, including attacker                     expectations, shed light on in our research.
gains device ownership remotely (equation 8) and attacker                    End-to-end discoveries of logic flaws. With LL-Verifier,
unauthorized device control (equation 9).                                    we identified 30 zero-day logic flaws (Table 2), all
                                                                             confirmed on real devices, including multiple flaw types
                                                                             and novel attacks discussed in § 5.
          | {z } ∧ uaOwner
 sv1 : ♢((ucRemote | {z } ) ∧ ⃝(ucRemote ∧ ¬uaOwner ))                 (8)
         remote attacker     ua is device owner
                                                                             Formal model generation. Our benchmark (available on-
                                                                             line [73]) includes 29 protocols from real-world vendors,
                                                                             including the original texts, organized texts, and correspond-
            | {z } ∧¬ ucOwner
 sv2 : ♢((¬ deviceOn  | {z } ) ∧ ⃝( |ucEvents
                                        {z } ∧deviceOn ∧ ¬ucOwner ))   (9)   ing formal models written in Les. On average, each protocol
           device off      attacker not owner     arbitrary actions
                                                                             contains 425 words, 12 rules, 4 principals, and 10 attributes.
    In Les, security goals are formalized as LTL (Linear                     On the benchmark, we evaluated the performance of the gen-
Temporal Logic) formulas representing the precise violation                  erated models across several semantic elements (Appendix
traces (i.e., the realization of an attack). We leverage the                 Table 3). Overall, LL-Verifier successfully models 98.3%
eventually operator (♢) and the next-state operator (⃝) to                   of principals with 1.7% false positives, 99.3% of attributes
capture illicit logical transitions over explicit state variables.           with 1.4% false positives, 96.8% of rules, and 64.3% of
By formalizing these goals as definitive transitions over                    properties. 65.5% of logic flaws can be checked without
explicit key-value states, the Les model checker exhaustively                human intervention. Among the remaining failures, only 2.3
evaluates the state space against these properties. Because                  manual corrections on average were required to make the
our analysis is strictly bounded by the customized threat                    defective models functional. See detailed error discussion
model rather than generic Dolev-Yao assumptions, this eval-                  in Appendix § C.
uation guarantees analytical soundness—meaning any trace                     Ablation Evaluation. With official Maude grammar [95],
satisfying these formulas is a confirmed logic flaw with no                  we designed a prompt (on website [73]) to evaluate
false positives (FP) within the defined scope.                               the effectiveness of generating Maude code directly. We
compared model generation between LL-Verifier and                                2                                          3
standard Maude on three protocols (iRobot, Aqara, and




                                                                                          2




                                                                                                                1
                                                                     3
August). From a syntactic perspective, LL-Verifier generated                1                  1                       2

models executed without errors, whereas the Maude models                 (a) RTE P1         (b) RTE P2              (c) RTE P3
encountered multiple runtime failures. Semantically, LL-
Verifier achieved full coverage. In contrast, the Maude               Figure 2: Three RTE design paradigms in the wild
models covered only 27/44 rules, 27/30 attributes.The
complete table is on our website [73], which demonstrates         unexpected users (attackers) to become the “root” users. For
low effectiveness in directly formalizing protocols using         example, in prior understanding, whoever presenting the de-
foundational logic frameworks like Maude.                         vice’s unique identifier to the cloud (server) can simply bind
LLM Choices. To assess the impact of LLM choice,                  with the device (entitled as “root” user) [75], [96]. The prob-
we selected 5 popular models: GPT-4o, Grok-3, Claude-             lem was that device ID (e.g., a string, a MAC address [97])
sonnet-4, DeepSeek-R1, and Gemini-2.5-Pro-Preview.                may be leaked (e.g., to a guest or in brute-force guess),
From Logic-Modeling Bench, we randomly sampled three              seriously endangering prior RTE designs. Unlike prior un-
representative protocols—iRobot, Aqara, and August—and            derstanding, we note that modern RTE protocols of real-
evaluated LL-Verifier’s performance with each LLM. The            world vendors are more complicated, usually proprietary
results show that all five LLMs achieved over 70% coverage        and diverse, with some being quite sophisticated aiming for
in modeling principals, attributes, rules, and events. 4 out of   improved security and usability. With the diversity of ven-
5 models successfully generated at least one protocol model       dors’ RTE protocols we found, we further summarize them
that uncovered real flaws without any human intervention.         in three sub-paradigms in § 5.1.1 to § 5.1.3 respectively.
See the full table online [73].
Performance overhead. We evaluated the performance                5.1.1. RTE P1: User-and-Device Provers. Essentially, in
overhead of LSM Runner running on the 29 protocol                 RTE protocols, the user aims to prove to the cloud that
models using 3GHz AMD Ryzen 5 4600H CPU and 16                    she/he is the legitimate root user. In some vendors’ RTE
GB memory. Based on the average of ten executions,                protocol design, the user u (using IoT mobile app) and the
LL-Verifier took 462 milliseconds and 75,860 KB memory            device d send a secret (binding key) to the cloud respectively.
at most to fully reason about a model.                            If their secrets match, the cloud is convinced that the user
                                                                  is entitled to bind with the device, establishing a binding
5. Logic Flaws in Application-Level IoT Access                    relation such as (u, d) (Figure 2a). We call this general
Protocols                                                         design pattern RTE Paradigm 1 (RTE P1), although different
                                                                  vendors still bear subtle differences with vulnerabilities in
    This paper focuses on analyzing application-level             protocol logic (e.g., iRobot, Philips Hue, see below). No-
protocols and logic (compared to cryptography-level               tably, Logic Flaw Type 1 (LFT 1) is under RTE P1.
protocols). Taking IoT as an example domain, application-         LFT 2 (local distribution of binding key). We find that
level protocols manage how users access (use, operate) and        vendors usually come with unique mechanisms to let the
securely manage IoT devices. LL-Verifier reported 35 logic        device and the user (using mobile apps) share a secret
flaws across 28 vendors (Table 2) for the multiple classes of     binding key. In LFT 1, once the user presses a button
IoT application-level protocols. This includes 30 zero-day        on an iRobot device, the device accepts a new binding
flaws: they are categorized as 9 logic flaw types (LFT 1          key from the user’s iRobot app. This is based on a local
to LFT 9) and elaborated on in § 5.1 to § 5.3 based on            Message Queuing Telemetry Transport (MQTT) [98] server
the protocols’ design-level mistakes and protocol classes.        in the iRobot device accepting customized commands.
Further, LL-Verifier reported 4 previously known flaws in in-     In iRobot’s RTE protocol, the user u alternatively can
teroperability (cross-vendor delegation of Google Home and        press the button and query the in-device MQTT server to
SmartThings [27]) and collaborative access control (MaaG          retrieve the binding key kprior previously used (already
of Kwikset and Level [59]) (last four rows in Table 2).           sent to the cloud, Equation 1) which is still recorded in
Based on their design and usage purposes, we summarize            the device. Anytime in the future, he can remotely send
real-world deployed, common IoT application protocols into        kprior to the cloud by calling a binding-related reset
a few general classes: IoT RTE (§ 5.1), IoT interoperability      API (https://auth1.iot.irobot.cn/v1/{deviceID}/reset) and
(§ 5.2), and collaborative IoT access control (§ 5.3).            the legitimate owner will lose binding relation and access
                                                                  rights (see PoC implementation below). The reason iRobot
5.1. IoT Root Trust Establishment (RTE)                           devices keep the used binding key kprior is possible because
                                                                  iRobot intends to reuse such an established secret between
    Fundamental to the security of any application protocols      the iRobot app and the device for local control. Specifically,
for IoT devices is the establishment of root trust, called        although normally the app’s control commands (e.g., turning
root trust establishment or RTE (sometimes called device          on/off the device) go through the cloud (allowing remote
binding [75]). The prior RTE protocols [75], [96] were            control), when the cloud or Internet service is unavailable,
usually simple and could be easily compromised, allowing          the iRobot app can automatically switch to local working
mode, and directly send commands to the device (through          HomeService/JoinWithTicket. The former requires
the device’s MQTT interface) using the secret key.               the ticket, device MAC, and home ID as arguments when
LFT 3 (remote distribution of binding key). Different            the device has no existing binding. The latter API is used
from iRobot devices that convey the binding key between          to bind with devices that have existing binding(s). Encoded
the iRobot app and device through local communication            RTE protocols and attack traces are available online [73].
channels (Bluetooth or Wi-Fi), the Philips Hue RTE strives
                                                                 5.1.2. RTE P2: User Prover. For some vendors, the user
to ensure their RTE is cross-platform and compatible with
                                                                 u is the prover trying to convince the cloud that she is the
Web clients. Specifically, users can use a Web page to bind
                                                                 legitimate user to bind with a device d. Usually, the user
with Philips Hue devices. Given that browsers or Webviews
                                                                 (using mobile apps) obtains a binding key from the device
may not always be entitled or equipped with Bluetooth, Wi-
                                                                 and sends it to the cloud to prove credibility (Figure 2b).
Fi, or support raw TCP/UDP protocols (e.g., customized
                                                                 The key can include the device’s identity, in-device secret,
MQTT commands between iRobot app and device), Philips
                                                                 or other credentials up to individual vendors’ RTE design.
Hue leverages the cloud to convey the secret key. Once a
                                                                 We find that real IoT devices supported by this RTE
button is pressed on the device, the device sends a new
                                                                 paradigm (RTE P2) do not require Internet connectivity
binding key to the cloud, which then tries to deliver the key
                                                                 (August [100] and Kevo [101]) although some devices
to the user (using her Hue app) who presses the button.
                                                                 connect to the cloud for after RTE (Switchbot [102],
    However, determining the actual user of a device be-         Netvue [103], and Govee [104]).
fore completing RTE is challenging. As a workaround,
                                                                 LFT 4 (multiple usages of a binding key). The design of
the Hue cloud issues the binding key to any users that
                                                                 Broadlink smart plugs did not differentiate a regular access
share the same outbound IP address with the device. To
                                                                 key from a binding key. Specifically, in its RTE, the owner
receive the binding key, normally the benign user’s binding
                                                                 usually presses a button on the device, and her Broadlink
Web page will query a Hue cloud API hue.accounts.
                                                                 app will automatically receive a secret binding key after
v1.BridgeService/RequestAccess. However, the
                                                                 connecting to the device’s Wi-Fi hotspot. The app then sends
attacker can also query (or even keep querying for racing
                                                                 the binding key to the cloud to finish the binding. Further,
with the victim) the cloud API to receive the binding key,
                                                                 the owner can allow guest users to use Broadlink devices
whenever any victim with the same outbound IP address is
                                                                 by either adding a guest user or turning on a “local access”
attempting a Hue device binding. The attacker can then use
                                                                 switch both done in the Broadlink app. In the former case,
the key to call the Hue cloud API hue.accounts.v1.
                                                                 the guest user’s Broadlink app will automatically retrieve an
BridgeService/LinkBridgeWithTicket, and es-
                                                                 access token from the cloud. In the latter case, the guest user
tablish a binding with the device. Once the attacker receives
                                                                 can press the button on the device and the app will retrieve
the key, the victim cannot receive it. The victim may attempt
                                                                 an access token from the device. With such access tokens,
RTE again, whose device generates another key (key2).
                                                                 the guest user can send commands to operate the device
    Notably, in the Philips Hue protocol, the cloud supports     either remotely through the cloud or locally (through Wi-Fi).
both root users and respective binding keys; the benign user         However, it turns out that the access token exposed to the
can bind with the device without the awareness of another        guest users is the same as the binding token. Even after the
root user (attacker). This attack can pose practical, serious    guest user is revoked, they can use the access token and call
risks in places like campuses, corporations, or communities,     the cloud API https://app-service-chn-467a8f05.ibroadlink.
where many users share outbound IP addresses.                    com/appsync/group/dev/manage?operation=add to establish
Implementation and PoC exploits. We PoC attacks for              a binding becoming the root user.
LFT 1 and 2 using our iRobot Roomba 975 devices. After           LFT 5 (insufficient restriction of binding key usage).
pressing the device’s button, by transmitting an iRobot-         Certain vendors have put measures to limit the validity and
customized packet f005efcc3b2900 to the in-device                the usability context of the binding key, to mitigate threats
MQTT server on port 8883, we developed a script (similar to      considering the binding key may sometimes be exposed
the iRobot mobile app) to retrieve the existing binding key      (e.g., to someone who could ever access the device). For
from the device; alternatively, our script can send the device   example, the iRobot cloud only acknowledges the latest
a new binding key with up to 30-bytes after sending a packet     binding key sent by the device, while the server of Kevo
f023efcc3b2900 to the in-device MQTT server [99].                door locks [101] and Netvue cameras [103] acknowledge all
    We implemented attacks for LFT 3 on our Philips              prior binding keys. A guest user of Netvue cameras (e.g.,
Hue Hub (victim device). We developed an attack script,          Airbnb guest) can press a device button and receive a fresh
running on a machine sharing the same outbound IP                binding key kn (using the Netvue app). Although the owner
address as the victim device. The Hue cloud APIs                 could have bound or may generate a new binding key km
(see below) are under https://api.account.meethue.com/.          to bind with the device, the guest can use kn to bind with
The attack script fetched the binding key via the                the device for arbitrary times.
Hue      API     hue.accounts.v1.BridgeService/                      RTE protocols of some devices ensure only one root user
RequestAccess. To bind with devices, the attack script           at a time, such as August [100] and TTLock [105] locks.
uses the API hue.accounts.v1.HomeService/                        Even if a guest user obtains the binding key from the device,
LinkBridgeWithTicket or hue.accounts.v1.                         their binding request to the cloud will be rejected. Unless
the existing lock owner (using the app) makes requests to             Implementation and PoC exploits. We implemented PoC
the cloud to reset existing binding or transfer the ownership         attacks for LFT 6 with our own TP-Link Kasa HS103P2
to another user, no one can reset or bind with the device             smart plug. We used a benign “owner” account (victim)
even physically having the device. However, such restric-             and a malicious user. We implemented an attack An-
tions can still be bypassed by a looping attack script that           droid app (either running on a nearby, malicious user’s
patiently waits for the opportune moment. Once the owner              phone or on the victim’s phone), using minimal permis-
resets the device binding (e.g., during ownership transfer or         sion ACCESS_FINE_LOCATION, which is needed to scan
configuration resetting), this script may operate faster than         nearby hotspot of the device. This app monitors Wi-Fi SSID
the benign user who performs a new binding, and establishes           “TP-LINK”. The device launches such a hotspot only during
malicious binding (by automatically sending the binding key           binding. The attack app then keeps sending a malicious
to the cloud). The benign user will have no way to bind the           binding key every 100 milliseconds until a successful bind-
device — even a physical resetting would not help.                    ing. Notably, the attack app does not know the victim’s
Implementation and PoC exploits. We performed PoC                     credentials related to binding.
attacks for LFT 4 using our Broadlink SP4M smart plugs.
We used two different Broadlink accounts to act as the                5.2. IoT Interoperability
benign owner and the guest (attacker, with guest permissions
granted by the owner). The guest obtained the device’s local               IoT interoperability enables devices from multiple ven-
key by sniffing the app’s network traffic with the Broadlink          dors to work easily together including cross-vendor del-
cloud. After the owner revoked the guest’s permissions,               egation [27], multiple device management channels (M-
the guest used a script to invoke the Broadlink cloud API             DMC) [57], and etc. The Matter protocol [65] is an industry-
with POST data. The data has a key field called “cookie”,             standard for smart-home IoT, supporting multiple protocols
which is a base64 encoded JSON that contains the pair                 including RTE. As a new control channel besides the com-
“aeskey”: {local key}. Then, the guest whose permissions              mon DMCs in [57], it emphasizes local control to enhance
were revoked, became a root user stealthily without the               reliability and security, recording access control lists inside
owner awareness. We show PoC attack videos online [73].               the devices.
                                                                      LFT 8. Many IoT vendors add Matter protocols to their ex-
5.1.3. RTE P3: Device Prover. Some IoT vendors feature                isting devices and apps for compatibility with the emerging
RTE Paradigm 3 (RTE P3): the device d is the prover                   Matter standard. In Aqara [106], device owner u can still
that tries to convince the cloud to bind itself with a user           leverage the vendor’s original RTE protocol to bind with
u. To do so, the device obtains a binding key from the                device d, and delegate partial access rights (guest-level) to
user’s app, which usually includes the user’s identity or             a user c, all using the Aqara app. Normally, the privileges of
other credentials up to individual vendor design, and sends           a guest-level user are restricted, unable to establish binding
the binding key to the cloud (Figure 2c). Again, real-world           using Aqara RTE or edit other users, for example. Since
vendors’ RTE protocols under RTE P3 are varied, featuring             the Aqara devices support Matter, we developed an LSM
subtle logic flaws.                                                   model that collectively models Aqara’s RTE, delegation,
LFT 6 (attacker binding key with the victim device).                  and Matter RTE protocols. Such an LSM model specifies
The TP-Link Kasa plugs enter RTE process once the benign              more comprehensive application semantics than modeling
owner presses a physical button. During binding, the device           individual protocols. LL-Verifier finds that after delegation is
d receives a secret binding key k from the user u (using her          conducted by owner u, user c can execute Matter RTE with
Kasa app), who got it from the cloud. The communication               the device, establishing a binding relation that is recorded
is based on that the user app is connected to the hotspot             in the device’s internal state. Consequently, user c achieved
of the device. Next, the user app sends the home’s Wi-Fi              privilege escalation. Even after the owner revokes user c
credential to the device, which then connects to the Internet.        using the Aqara app (part of Aqara delegation protocol),
Since the cloud knew the correlation (k, u), once the device          leading to removal of user c in the cloud-side access control
d presents k to the cloud, the cloud concludes the binding            list (modeled in the cloud’s internal state), user c still has
relation (d, u, k).                                                   a binding relation with the device based on the Matter
    Leveraging a protocol flaw, after a victim sends hers             protocol. Such a binding status is recorded in the device’s
k to the device, a malicious user u′ can also send his                internal state, still allowing user c to operate the device,
own binding key k ′ to the device, replacing k effectively.           posing a security violation.Tuya [107] has a similar logic
After the victim’s app sends Wi-Fi information, the device            flaw (Table 2).
presents k ′ to the cloud, establishes a binding (d, u′ , k ′ ). In   Implementation and PoC exploits. The encoded Aqara
reality, the attacker can be a neighbor, someone nearby, or           protocol is released online [73]. We implemented PoC
even an app with malicious code on the victim’s phone, that           attacks with our Aqara smart hub M2. Acting as a
keeps trying the above attack (using automatic code) and              device owner (victim), we invited a guest user ac-
awaits for the victim to ever bind with her device (see PoC           count (attacker) into the “home” in the Aqara app and
attacks on real devices below). We present another LFT 7              granted the attacker a “Guest User” role. Through re-
under RTE Paradigm 3 for CloudEdge cameras in Appendix.               verse engineering network traffic between his Aqara app
and the Aqara cloud, the attacker collected the de-              difficult to avoid and present serious and subtle problems
vice identifier. The attacker retrieved the Matter pairing       in the security design space. Specifically, production-level
code of the device by calling Aqara cloud API with               IoT devices are supposed to have gone through internal
payload {"data":[{"options":["4.200.700"],                       security review by developers (or dedicated security teams).
"subjected": "DEVICE_ID"}]}. Using an open-                      However, thanks to LL-Verifier, all vendors we studied come
source Matter controller CHIP Tool [108], the attacker           with subtle logic flaws, indicating that state-of-the-practice
successfully bound with the device using Matter protocol,        approaches (e.g., prior techniques, manual security review)
which lasted after the owner removed him in the Aqara app.       are less effective or hard to scale in reasoning about logic
                                                                 flaws. Problems in the application logic space require proper
                                                                 approaches for effective, comprehensive modeling and rea-
5.3. Collaborative IoT Access Control                            soning, for which LL-Verifier advances the state-of-the-art.

    Unlike prior protocols (§ 5.1 and 5.2) with centralized      6. Related Work
access control (e.g., a vendor’s cloud), some IoT devices
coordinate policies between cloud and in-device authorities,
especially for offline devices [59]. IoT vendors, such as Ap-    LLM-empowered protocol modeling. Prior work [112]–
ple Home [109], Dyson [110], and Tuya [107], enforce in-         [116] has primarily used code as input, rather than natural
device security policies to authorize local user app requests.   language, to construct models. In contrast, our objective
For remote users, commands are routed through the cloud,         is to synthesize formal protocol models directly from tex-
which authenticates users and relays approved instructions       tual descriptions. [117] proposed generating formal models
to devices. Devices synchronize with the cloud to update         from natural languages, in sharp contrast, their approach
or retrieve access policies, such as adding a new authorized     targets cryptographic protocols and is designed to model
user. This bidirectional synchronization ensures consistent      limited kinds of cryptographic semantics (e.g., encryption,
access control between devices and cloud authorities.            keys, key exchange). It was not designed to autonomously
LFT 9. Under CAC protocols, when the cloud de-authorizes         model application-level protocols of various semantics and
a user, the device’s local access control should not permit      domains like LL-Verifier.
the user to operate the device. Take, Tuya devices’ CAC          Security analysis of logic flaws. Previous works [3], [27],
protocol in combination with delegation protocol, for            [29], [41]–[60] relied on empirical analysis or significant
instance. Following the Tuya app’s delegation workflow, an       manual efforts to analyze logic flaws, and identify specific
owner can delegate permissions to another user, who can          exploits and logical attack steps. Some other works have
be a malicious employee or tenant, for example. The latter       used relatively automatic approaches, including those
(attacker) gets two keys keyremote and keylocal : for remote     leveraging test cases generation [26], [28], [30], [118], and
access through the cloud the requests should include both        model-guided analysis [26], [27], [29]. They are typically
keys and for local access the requests only need the latter      domain-specific and need significant manual efforts. In
key. After the device owner (victim) revokes the attacker, the   contrast, our LL-Verifier aims for a cross-application-
cloud’s policy (modeled as part of the cloud’s internal state)   domain, semantic-agnostic, general, automatic approach to
deauthorizes requests with the two keys; inconsistently,         identify logic flaws.
the device policy will still permit the attacker’s operating     Model checking for protocol security analysis. Prior
requests carrying keylocal . Dyson, Xiaomi, Huawei, Philips,     works extensively leveraged model checking to formally
CloudEdge, and Broadlink all have similar CAC protocols          verify system protocols or access control policies [12]–[17].
and a similar logic flaw (Table 2).                              General model checking tools (e.g., Spin [66], SMV [67],
Implementation and PoC exploits. We released Tuya’s              Alloy [68], ProVerif [119], and TLA+ [69]) are commonly
logical model in Les and its attack traces online [73].          adopted to implement and verify models for specific appli-
We implemented PoC attacks using our Tuya Kmeasion               cation domains (e.g., VerioT [27], MPInspector [37], MQT-
smart plug CZ1. We used an owner account (victim) and            Tactic [61]). [120]–[124] used Maude to model IoT/Cyber-
granted a guest role to another account using the Tuya           physical systems [120]–[122] and Fog systems [123], [124].
Smart (mobile) app. The latter account (attacker) can obtain     [125]–[127] modeled and verified IoT trigger-action appli-
the two keys by employing Frida [111] to instrument the          cations partially using Maude.
com.tuya.smart.common.utils.AESUtil class of                          However, in prior works, modeling a specific sys-
his Tuya app. After the owner completely removes the at-         tem, application or underlying protocols involves identify-
tacker from his home using the Tuya app, the attacker cannot     ing domain-specific, context-specific semantic elements that
request the cloud to operate the device but can send opera-      should be modeled, and deciding how to model these seman-
tion commands to the device’s port 6668 carrying keylocal .      tic elements (e.g., defining data structures and operations
                                                                 using the syntax supported by a modeling language) [26]–
5.4. Discussions                                                 [30]. The prior modeling process has generally (1) relied
                                                                 heavily on manual efforts or domain experts for individual
    Our findings (§ 5 or Table 2) showed pervasive logic         systems and protocols, and (2) been highly tailored to spe-
flaws across multiple classes of IoT protocols, which are        cific systems or domains to identify the necessary semantics
for modeling. our LL-Verifier addresses such a fundamental                      [13]   J. Backes, U. Berrueco, T. Bray, D. Brim, B. Cook, A. Gacek,
gap in formal modeling of application-level protocols of                               R. Jhala, K. Luckow, S. McLaughlin, M. Menon et al., “Stratified
                                                                                       abstraction of access control policies,” in International Conference
various semantic contexts and domains, through a general,                              on Computer Aided Verification. Springer, 2020, pp. 165–176.
autonomous approach design and implementation.
                                                                                [14]   J. Backes, P. Bolignano, B. Cook, C. Dodge, A. Gacek, K. S.
                                                                                       Luckow, N. Rungta, O. Tkachuk, and C. Varming, “Semantic-based
7. Conclusion                                                                          automated reasoning for AWS access policies using SMT,” in
                                                                                       2018 Formal Methods in Computer Aided Design, FMCAD 2018,
    We presented an automatic logic flaw identification                                Austin, TX, USA, October 30 - November 2, 2018, N. Bjørner
                                                                                       and A. Gurfinkel, Eds. IEEE, 2018, pp. 1–9. [Online]. Available:
framework LL-Verifier empowered by LLM, enabling the                                   https://doi.org/10.23919/FMCAD.2018.8602994
modeling and specification of real-world systems and the
                                                                                [15]   M. Yahyazadeh, P. Podder, E. Hoque, and O. Chowdhury, “Ex-
automated verification of security flaws. With LL-Verifier,                            pat: Expectation-based policy analysis and enforcement for appified
we identified 30 zero-day logic flaws among 28 IoT vendors,                            smart-home platforms,” in Proceedings of the 24th ACM Symposium
highlighting the effectiveness of our approach in improving                            on Access Control Models and Technologies, 2019, pp. 61–72.
IoT security.                                                                   [16]   K. Jayaraman, N. Bjørner, G. Outhred, and C. Kaufman, “Automated
                                                                                       analysis and debugging of network connectivity policies,” Microsoft
                                                                                       Research, pp. 1–11, 2014.
References
                                                                                [17]   W. T. Hallahan, E. Zhai, and R. Piskac, “Automated repair by
                                                                                       example for firewalls,” in 2017 Formal Methods in Computer Aided
[1]    “Cwe - cwe-840: Cwe category: Business logic errors (4.16,” https:
                                                                                       Design (FMCAD). IEEE, 2017, pp. 220–229.
       //cwe.mitre.org/data/definitions/840.html, 2026.
[2]    “Business logic vulnerability — owasp foundation,” https://owasp.        [18]   B. Lampson, M. Abadi, M. Burrows, and E. Wobber, “Authentication
       org/www-community/vulnerabilities/Business logic vulnerability,                 in distributed systems: Theory and practice,” ACM Transactions on
       2026.                                                                           Computer Systems (TOCS), vol. 10, no. 4, pp. 265–310, 1992.

[3]    J. Wang, Y. Xiao, X. Wang, Y. Nan, L. Xing, X. Liao, J. Dong,            [19]   A. W. Appel and E. W. Felten, “Proof-carrying authentication,” in
       N. Serrano, H. Lu, X. Wang et al., “Understanding malicious                     Proceedings of the 6th ACM Conference on Computer and Commu-
       cross-library data harvesting on android,” in 30th USENIX Security              nications Security, 1999, pp. 52–62.
       Symposium (USENIX Security 21), 2021, pp. 4133–4150.                     [20]   L. Bauer, M. A. Schneider, and E. W. Felten, “A general and flexible
[4]    Y. Zhang, Z. Hu, X. Wang, Y. Hong, Y. Nan, X. Wang, J. Cheng,                   access-control system for the web.” in USENIX Security Symposium,
       and L. Xing, “Navigating the privacy compliance maze: Under-                    2002, pp. 93–108.
       standing risks with {Privacy-Configurable} mobile {SDKs},” in            [21]   L. Bauer, S. Garriss, J. M. McCune, M. K. Reiter, J. Rouse, and
       33rd USENIX Security Symposium (USENIX Security 24), 2024, pp.                  P. Rutenbar, “Device-enabled authorization in the grey system,”
       6543–6560.                                                                      in Information Security: 8th International Conference, ISC 2005,
[5]    D. Liu, Y. Xiao, C. Zhang, K. Xie, X. Bai, S. Zhang, and L. Xing,               Singapore, September 20-23, 2005. Proceedings 8. Springer, 2005,
       “{iHunter}: Hunting privacy violations at scale in the software                 pp. 431–445.
       supply chain on {iOS},” in 33rd USENIX Security Symposium                [22]   L. Bauer, S. Garriss, and M. K. Reiter, “Distributed proving in
       (USENIX Security 24), 2024, pp. 5663–5680.                                      access-control systems,” in 2005 IEEE symposium on security and
[6]    X. Wang, Y. Zhang, X. Wang, Y. Jia, and L. Xing, “Union under                   privacy (S&P’05). IEEE, 2005, pp. 81–95.
       duress: understanding hazards of duplicate resource mismediation in
                                                                                [23]   M. Burrows, M. Abadi, and R. Needham, “A logic of authentica-
       android software supply chain,” in 32nd USENIX Security Sympo-
                                                                                       tion,” ACM Transactions on Computer Systems (TOCS), vol. 8, no. 1,
       sium (USENIX Security 23), 2023, pp. 3403–3420.
                                                                                       pp. 18–36, 1990.
[7]    X. Bai, L. Xing, M. Zheng, and F. Qu, “idea: Static analysis on the
       security of apple kernel drivers,” in Proceedings of the 2020 ACM        [24]   H. Ganzinger, F. Pfenning, and C. Schürmann, “System descrip-
       SIGSAC Conference on Computer and Communications Security,                      tion: Twelf—a meta-logical framework for deductive systems,” in
       2020, pp. 1185–1202.                                                            Automated Deduction—CADE-16: 16th International Conference on
                                                                                       Automated Deduction Trento, Italy, July 7–10, 1999 Proceedings 16.
[8]    C. Zuo, W. Wang, Z. Lin, and R. Wang, “Automatic forgery of cryp-               Springer, 1999, pp. 202–206.
       tographically consistent messages to identify security vulnerabilities
       in mobile services.” in NDSS, 2016.                                      [25]   Y. Bertot and P. Castéran, Interactive theorem proving and pro-
                                                                                       gram development: Coq’Art: the calculus of inductive constructions.
[9]    E. Bauman, Z. Lin, K. W. Hamlen et al., “Superset disassembly:                  Springer Science & Business Media, 2013.
       Statically rewriting x86 binaries without heuristics.” in NDSS, 2018.
                                                                                [26]   V. Felmetsger, L. Cavedon, C. Kruegel, and G. Vigna, “Toward
[10]   “Trains were designed to break down after third-party repairs, hack-            automated detection of logic vulnerabilities in web applications,”
       ers find - ars technic,” https://arstechnica.com/tech-policy/2026/12/           in USENIX Security Symposium, vol. 58, 2010.
       manufacturer-deliberately-bricked-trains-
       repaired-by-competitors-hackers-find/, 2026.                             [27]   B. Yuan, Y. Jia, L. Xing, D. Zhao, X. Wang, D. Zou, H. Jin, and
                                                                                       Y. Zhang, “Shattered chain of trust: Understanding security risks in
[11]   “How a group of train hackers exposed a right-to-repair nightmare               cross-cloud iot access delegation.” in USENIX Security Symposium,
       - threatshub cybersecurity news,” https://www.threatshub.org/blog/              2020, pp. 1183–1200.
       how-a-group-of-train-hackers-exposed-a-
       right-to-repair-nightmare/, 2026.                                        [28]   G. Pellegrino and D. Balzarotti, “Toward black-box detection of
                                                                                       logic flaws in web applications.” in NDSS, vol. 14, 2014, pp. 23–
[12]   M. Bouchet, B. Cook, B. Cutler, A. Druzkina, A. Gacek,                          26.
       L. Hadarean, R. Jhala, B. Marshall, D. Peebles, N. Rungta et al.,
       “Block public access: trust safety verification of access control        [29]   Y. Chen, L. Xing, Y. Qin, X. Liao, X. Wang, K. Chen, and W. Zou,
       policies,” in Proceedings of the 28th ACM Joint Meeting on Eu-                  “Devils in the guidance: Predicting logic vulnerabilities in payment
       ropean Software Engineering Conference and Symposium on the                     syndication services through automated documentation analysis.” in
       Foundations of Software Engineering, 2020, pp. 281–291.                         USENIX security symposium, 2019, pp. 747–764.
[30]   A. Doupé, B. Boe, C. Kruegel, and G. Vigna, “Fear the ear:              [47]   L. Xing, X. Bai, T. Li, X. Wang, K. Chen, X. Liao, S.-M. Hu,
       discovering and mitigating execution after redirect vulnerabilities,”           and X. Han, “Cracking app isolation on apple: Unauthorized cross-
       in Proceedings of the 18th ACM conference on Computer and                       app resource access on mac os˜ x and ios,” in Proceedings of the
       communications security, 2011, pp. 251–262.                                     22nd ACM SIGSAC Conference on Computer and Communications
[31]   J. Yen, T. Lévai, Q. Ye, X. Ren, R. Govindan, and B. Raghavan,                 Security, 2015, pp. 31–43.
       “Semi-automated protocol disambiguation and code generation,” in         [48]   X. Liao, K. Yuan, X. Wang, Z. Pei, H. Yang, J. Chen, H. Duan,
       Proceedings of the 2021 ACM SIGCOMM 2021 Conference, 2021,                      K. Du, E. Alowaisheq, S. Alrwais et al., “Seeking nonsense, looking
       pp. 272–286.                                                                    for trouble: Efficient promotional-infection detection through seman-
[32]   A. Sosnovich, O. Grumberg, and G. Nakibly, “Formal black-                       tic inconsistency search,” in 2016 IEEE Symposium on Security and
       box analysis of routing protocol implementations,” arXiv preprint               Privacy (SP). IEEE, 2016, pp. 707–723.
       arXiv:1709.08096, 2017.                                                  [49]   X. Bai, L. Xing, N. Zhang, X. Wang, X. Liao, T. Li, and S.-M.
[33]   A. Davis, M. Hirschhorn, and J. Schvimer, “Extreme modelling in                 Hu, “Staying secure and unprepared: Understanding and mitigating
       practice,” arXiv preprint arXiv:2006.00915, 2020.                               the security risks of apple zeroconf,” in 2016 IEEE Symposium on
                                                                                       Security and Privacy (SP). IEEE, 2016, pp. 655–674.
[34]   M. Clavel, F. Durán, S. Eker, S. Escobar, P. Lincoln, N. Martı-Oliet,
       J. Meseguer, R. Rubio, and C. Talcott, “Maude manual (version            [50]   X. Liao, K. Yuan, X. Wang, Z. Li, L. Xing, and R. Beyah, “Acing the
       3.1),” SRI International University of Illinois at Urbana-Champaign             ioc game: Toward automatic discovery and analysis of open-source
       http://maude. lcc. uma. es/maude31-manual-html/maude-manual.                    cyber threat intelligence,” in Proceedings of the 2016 ACM SIGSAC
       html, 2020.                                                                     conference on computer and communications security, 2016, pp.
                                                                                       755–766.
[35]   S. Meier, B. Schmidt, C. Cremers, and D. Basin, “The tamarin
       prover for the symbolic analysis of security protocols,” in Computer     [51]   X. Liao, S. Alrwais, K. Yuan, L. Xing, X. Wang, S. Hao, and
       Aided Verification: 25th International Conference, CAV 2013, Saint              R. Beyah, “Lurking malice in the cloud: Understanding and detect-
       Petersburg, Russia, July 13-19, 2013. Proceedings 25. Springer,                 ing cloud repository as a malicious service,” in Proceedings of the
       2013, pp. 696–701.                                                              2016 ACM SIGSAC Conference on Computer and Communications
                                                                                       Security, 2016, pp. 1541–1552.
[36]   A. Colmerauer and P. Roussel, “The birth of prolog,” in History of
       programming languages—II, 1996, pp. 331–367.                             [52]   T. Li, X. Wang, M. Zha, K. Chen, X. Wang, L. Xing, X. Bai,
[37]   Q. Wang, S. Ji, Y. Tian, X. Zhang, B. Zhao, Y. Kan, Z. Lin,                     N. Zhang, and X. Han, “Unleashing the walking dead: Under-
       C. Lin, S. Deng, A. X. Liu et al., “{MPInspector}: A systematic and             standing cross-app remote infections on mobile webviews,” in Pro-
       automatic approach for evaluating the security of {IoT} messaging               ceedings of the 2017 ACM SIGSAC Conference on Computer and
       protocols,” in 30th USENIX Security Symposium (USENIX Security                  Communications Security, 2017, pp. 829–844.
       21), 2021, pp. 4205–4222.                                                [53]   Y. Jia, L. Xing, Y. Mao, D. Zhao, X. Wang, S. Zhao, and Y. Zhang,
[38]   J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V.                 “Burglars’ iot paradise: Understanding and mitigating security risks
       Le, D. Zhou et al., “Chain-of-thought prompting elicits reasoning in            of general messaging protocols on iot clouds,” in 2020 IEEE Sym-
       large language models,” Advances in neural information processing               posium on Security and Privacy (SP). IEEE, 2020, pp. 465–481.
       systems, vol. 35, pp. 24 824–24 837, 2022.                               [54]   H. Lu, L. Xing, Y. Xiao, Y. Zhang, X. Liao, X. Wang, and X. Wang,
[39]   N. Shinn, F. Cassano, B. Labash, A. Gopinath, K. Narasimhan,                    “Demystifying resource management risks in emerging mobile app-
       and S. Yao, “Reflexion: Language agents with verbal reinforcement               in-app ecosystems,” in Proceedings of the 2020 ACM SIGSAC
       learning.(2023),” arXiv preprint cs.AI/2303.11366, 2023.                        conference on computer and communications Security, 2020, pp.
                                                                                       569–585.
[40]   S. Demri, F. Laroussinie, and P. Schnoebelen, “A parametric analysis
       of the state-explosion problem in model checking,” Journal of            [55]   T. Lv, R. Li, Y. Yang, K. Chen, X. Liao, X. Wang, P. Hu, and
       Computer and System Sciences, vol. 72, no. 4, pp. 547–575, 2006.                L. Xing, “Rtfm! automatic assumption discovery and verification
                                                                                       derivation from library document for api misuse detection,” in
[41]   J. Zhou and G. Vigna, “Detecting attacks that exploit application-
                                                                                       Proceedings of the 2020 ACM SIGSAC conference on computer and
       logic errors through application-level auditing,” in 20th Annual
                                                                                       communications security, 2020, pp. 1837–1852.
       Computer Security Applications Conference. IEEE, 2004, pp. 168–
       178.                                                                     [56]   L. Su, X. Shen, X. Du, X. Liao, X. Wang, L. Xing, and B. Liu, “Evil
[42]   R. Wang, S. Chen, X. Wang, and S. Qadeer, “How to shop for free                 under the sun: Understanding and discovering attacks on ethereum
       online–security analysis of cashier-as-a-service based web stores,”             decentralized applications.” in USENIX Security Symposium, 2021,
       in 2011 IEEE symposium on security and privacy. IEEE, 2011,                     pp. 1307–1324.
       pp. 465–480.                                                             [57]   Y. Jia, B. Yuan, L. Xing, D. Zhao, Y. Zhang, X. Wang, Y. Liu,
[43]   R. Wang, S. Chen, and X. Wang, “Signing me onto your accounts                   K. Zheng, P. Crnjak, Y. Zhang et al., “Who’s in control? on
       through facebook and google: A traffic-guided security study of                 security risks of disjointed iot device management channels,” in
       commercially deployed single-sign-on web services,” in 2012 IEEE                Proceedings of the 2021 ACM SIGSAC Conference on Computer
       Symposium on Security and Privacy. IEEE, 2012, pp. 365–379.                     and Communications Security, 2021, pp. 1289–1305.
[44]   L. Xing, X. Pan, R. Wang, K. Yuan, and X. Wang, “Upgrading your          [58]   Z. Li, W. Liu, H. Chen, X. Wang, X. Liao, L. Xing, M. Zha, H. Jin,
       android, elevating my malware: Privilege escalation through mobile              and D. Zou, “Robbery on devops: Understanding and mitigating
       os updating,” in 2014 IEEE symposium on security and privacy.                   illicit cryptomining on continuous integration service platforms,” in
       IEEE, 2014, pp. 393–408.                                                        2022 IEEE Symposium on Security and Privacy (SP). IEEE, 2022,
                                                                                       pp. 2397–2412.
[45]   R. Wang, L. Xing, X. Wang, and S. Chen, “Unauthorized origin
       crossing on mobile platforms: Threats and mitigation,” in Pro-           [59]   X. Zhou, J. Guan, L. Xing, and Z. Qian, “Perils and mitigation
       ceedings of the 2013 ACM SIGSAC conference on Computer &                        of security risks of cooperation in mobile-as-a-gateway iot,” in
       communications security, 2013, pp. 635–646.                                     Proceedings of the 2022 ACM SIGSAC Conference on Computer
                                                                                       and Communications Security, 2022, pp. 3285–3299.
[46]   T. Li, X. Zhou, L. Xing, Y. Lee, M. Naveed, X. Wang, and X. Han,
       “Mayhem in the push clouds: Understanding and mitigating security        [60]   Z. Jin, L. Xing, Y. Fang, Y. Jia, B. Yuan, and Q. Liu, “P-verifier:
       hazards in mobile push-messaging services,” in Proceedings of the               Understanding and mitigating security risks in cloud-based iot access
       2014 ACM SIGSAC Conference on Computer and Communications                       policies,” in Proceedings of the 2022 ACM SIGSAC Conference on
       Security, 2014, pp. 978–989.                                                    Computer and Communications Security, 2022, pp. 1647–1661.
[61]   B. Yuan, Z. Song, Y. Jia, Z. Lu, D. Zou, H. Jin, and L. Xing,            [82]   S. G. Patil, T. Zhang, V. Fang, R. Huang, A. Hao, M. Casado, J. E.
       “Mqttactic: Security analysis and verification for logic flaws in mqtt          Gonzalez, R. A. Popa, and I. Stoica, “Goex: Perspectives and designs
       implementations,” in 2024 IEEE Symposium on Security and Privacy                towards a runtime for autonomous llm applications,” arXiv preprint
       (SP). IEEE, 2024.                                                               arXiv:2404.06921, 2024.
[62]   N. Martı́-Oliet and J. Meseguer, “Rewriting logic as a logical and       [83]   S. Geng, M. Josifoski, M. Peyrard, and R. West, “Grammar-
       semantic framework,” Electronic Notes in Theoretical Computer                   constrained decoding for structured nlp tasks without finetuning,”
       Science, vol. 4, pp. 190–225, 1996.                                             arXiv preprint arXiv:2305.13971, 2023.
[63]   S. Eker, J. Meseguer, and A. Sridharanarayanan, “The maude ltl           [84]   Z. Wang, L. F. Ribeiro, A. Papangelis, R. Mukherjee, T.-Y. Wang,
       model checker,” Electronic Notes in Theoretical Computer Science,               X. Zhao, A. Biswas, J. Caverlee, and A. Metallinou, “Fantastic
       vol. 71, pp. 162–187, 2004.                                                     sequences and where to find them: Faithful and efficient api call
[64]   T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhari-                generation through state-tracked constrained decoding and rerank-
       wal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell et al., “Lan-               ing,” arXiv preprint arXiv:2407.13945, 2024.
       guage models are few-shot learners,” Advances in neural information      [85]   Z. R. Tam, C.-K. Wu, Y.-L. Tsai, C.-Y. Lin, H.-y. Lee, and Y.-N.
       processing systems, vol. 33, pp. 1877–1901, 2020.                               Chen, “Let me speak freely? a study on the impact of format re-
[65]   “Matter - csa-iot,” https://csa-iot.org/all-solutions/matter/, 2024.            strictions on performance of large language models,” arXiv preprint
                                                                                       arXiv:2408.02442, 2024.
[66]   G. J. Holzmann, “The model checker spin,” IEEE Transactions on
       software engineering, vol. 23, no. 5, pp. 279–295, 1997.                 [86]   K. Park, J. Wang, T. Berg-Kirkpatrick, N. Polikarpova, and
                                                                                       L. D’Antoni, “Grammar-aligned decoding,” arXiv preprint
[67]   K. L. McMillan and K. L. McMillan, “The smv system,” Symbolic
                                                                                       arXiv:2405.21047, 2024.
       Model Checking, pp. 61–85, 1993.
[68]   D. Jackson, “Alloy: a language and tool for exploring software           [87]   T. Koo, F. Liu, and L. He, “Automata-based constraints for language
       designs,” Communications of the ACM, vol. 62, no. 9, pp. 66–76,                 model decoding,” arXiv preprint arXiv:2407.08103, 2024.
       2019.                                                                    [88]   S. Geng, B. Döner, C. Wendler, M. Josifoski, and R. West, “Sketch-
[69]   Y. Yu, P. Manolios, and L. Lamport, “Model checking tla+ spec-                  guided constrained decoding for boosting blackbox large language
       ifications,” in Advanced Research Working Conference on Correct                 models without logit access,” arXiv preprint arXiv:2401.09967,
       Hardware Design and Verification Methods. Springer, 1999, pp.                   2024.
       54–66.                                                                   [89]   S. Ugare, R. Gumaste, T. Suresh, G. Singh, and S. Mis-
[70]   B. Yuan, Z. Song, Y. Jia, Z. Lu, D. Zou, H. Jin, and L. Xing,                   ailovic, “Itergen: Iterative structured llm generation,” arXiv preprint
       “Mqttactic: Security analysis and verification for logic flaws in mqtt          arXiv:2410.07295, 2024.
       implementations,” in 2024 IEEE Symposium on Security and Privacy         [90]   Z. Li, W. Hua, H. Wang, H. Zhu, and Y. Zhang, “Formal-llm:
       (SP). IEEE, 2024, pp. 2385–2403.                                                Integrating formal language and natural language for controllable
[71]   M. P. Andersen, S. Kumar, M. AbdelBaky, G. Fierro, J. Kolb,                     llm-based agents,” arXiv preprint arXiv:2402.00798, 2024.
       H. Kim, D. E. Culler, and R. A. Popa, “WAVE: A decentralized
                                                                                [91]   Y. Dong, C. F. Ruan, Y. Cai, R. Lai, Z. Xu, Y. Zhao, and T. Chen,
       authorization framework with transitive delegation,” in 28th USENIX
                                                                                       “Xgrammar: Flexible and efficient structured generation engine for
       Security Symposium, 2019, pp. 1375–1392.
                                                                                       large language models,” arXiv preprint arXiv:2411.15100, 2024.
[72]   “Extended backus–naur form - wikipedia,” https://en.wikipedia.org/
                                                                                [92]   S. Geng, H. Cooper, M. Moskal, S. Jenkins, J. Berman, N. Ranchin,
       wiki/Extended Backus%E2%80%93Naur form, 2026.
                                                                                       R. West, E. Horvitz, and H. Nori, “Generating structured outputs
[73]   “Ll-verifier,” https://sites.google.com/view/ll-verifier/home, 2026.            from language models: Benchmark and studies,” arXiv preprint
[74]   A. V. Aho and J. D. Ullman, Foundations of computer science.                    arXiv:2501.10868, 2025.
       Computer Science Press, Inc., 1992.                                      [93]   S. G. Patil, T. Zhang, X. Wang, and J. E. Gonzalez, “Gorilla:
[75]   J. Chen, C. Zuo, W. Diao, S. Dong, Q. Zhao, M. Sun, Z. Lin,                     Large language model connected with massive apis,” arXiv preprint
       Y. Zhang, and K. Zhang, “Your iots are (not) mine: On the re-                   arXiv:2305.15334, 2023.
       mote binding between iot devices and users,” in 2019 49th Annual         [94]   “Introducing structured outputs in the api — openai,” https://openai.
       IEEE/IFIP International Conference on Dependable Systems and                    com/index/introducing-structured-outputs-in-the-api/, 2026.
       Networks (DSN). IEEE, 2019, pp. 222–233.
                                                                                [95]   “19 core maude grammar,” https://maude.lcc.uma.es/manual271/
[76]   “irobot,” https://www.irobot.com/, 2024, accessed: 2019-01.                     maude-manualch19.html, 2026.
[77]   S. Escobar and J. Meseguer, “Symbolic model checking of infinite-
                                                                                [96]   J. Chen, M. Sun, and K. Zhang, “Security analysis of device binding
       state systems using narrowing,” in International Conference on
                                                                                       for ip-based iot devices,” in 2019 IEEE International Conference
       Rewriting Techniques and Applications. Springer, 2007, pp. 153–
                                                                                       on Pervasive Computing and Communications Workshops (PerCom
       168.
                                                                                       Workshops). IEEE, 2019, pp. 900–905.
[78]   “Llverifier artifact,” https://anonymous.4open.science/r/LLVerifier-
       204C/README.md, 2026.                                                    [97]   “Mac address - wikipedia,” https://en.wikipedia.org/wiki/MAC
                                                                                       address, 2026.
[79]   K. Park, J. Wang, T. Berg-Kirkpatrick, N. Polikarpova, and
       L. Antoni, “Grammar-aligned decoding,” in Advances in Neural             [98]   “Mqtt version 3.0 - candidate oasis standard 01,” https://docs.oasis-
       Information Processing Systems, A. Globerson, L. Mackey,                        open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html, 2026.
       D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, Eds.,          [99]   “Roomba980-python/password.py      at   master    -    github,”
       vol. 37. Curran Associates, Inc., 2024, pp. 24 547–24 568. [Online].            https://github.com/NickWaterton/Roomba980-Python/blob/master/
       Available: https://proceedings.neurips.cc/paper files/paper/2024/file/          roomba/password.py, 2026.
       2bdc2267c3d7d01523e2e17ac0a754f3-Paper-Conference.pdf
                                                                                [100] “August Home,” https://august.com/, 2024.
[80]   B. T. Willard and R. Louf, “Efficient guided generation for large
       language models,” arXiv preprint arXiv:2307.09702, 2023.                 [101] “Kevo Smart Lock, 2nd Gen,” https://www.kwikset.com/products/
                                                                                      detail/kevo-traditional-touch-to-open-smart-lock-2nd-gen, 2024.
[81]   S. Ugare, T. Suresh, H. Kang, S. Misailovic, and G. Singh, “Syn-
       code: Llm generation with grammar augmentation, 2024,” URL               [102] “SwitchBot Official - Make Home Appliances Smart,” https://us.
       https://arxiv. org/abs/2403.01632.                                             switch-bot.com/, 2024.
[103] “Netvue Web Client — Home Security, Done Smart,” https://my.              [125] F. Durán, G. Salaün, and A. Krishna, “Automated composition, anal-
      netvue.com, 2024.                                                               ysis and deployment of iot applications,” in Software Technology:
                                                                                      Methods and Tools: 51st International Conference, TOOLS 2019,
[104] “Govee IoT,” https://us.govee.com/, 2024.                                       Innopolis, Russia, October 15–17, 2019, Proceedings 51. Springer,
[105] “TTLock,” https://www.ttlock.com/, 2024.                                        2019, pp. 252–268.
[106] “Aqara,” https://www.aqara.com/us/, 2024.                                 [126] F. Durán, A. Krishna, M. Le Pallec, R. Mateescu, and G. Salaün,
                                                                                      “Models and analysis for user-driven reconfiguration of rule-based
[107] “Tuya Smart - Global IoT Development Platform Service Provider,”
                                                                                      iot applications,” Internet of Things, vol. 19, p. 100515, 2022.
      https://www.tuya.com, 2024.
[108] “connectedhomeip,”                    https://github.com/project-chip/    [127] Q. Wang, P. Datta, W. Yang, S. Liu, A. Bates, and C. A. Gunter,
      connectedhomeip/, 2026.                                                         “Charting the attack surface of trigger-action iot platforms,” in
                                                                                      Proceedings of the 2019 ACM SIGSAC conference on computer and
[109] “Home app - Apple,” https://www.apple.com/home-app/, 2024.                      communications security, 2019, pp. 1439–1453.
[110] “Dyson,” https://www.dyson.com/en, 2024.
[111] “Frida • a world-class dynamic instrumentation toolkit,” https://frida.   Appendix
      re/, 2026.
[112] H. Wei, Z. Du, H. Huang, Y. Liu, G. Cheng, L. Wang, and B. Mao,
      “Inferring state machine from the protocol implementation via large       1. Other Logic Flaw Types
      language model,” arXiv preprint arXiv:2405.00393, 2024.
[113] T. Chen, S. Lu, S. Lu, Y. Gong, C. Yang, X. Li, M. R. H. Misu,            LFT 7 (victim binding key with the attacker device). In
      H. Yu, N. Duan, P. Cheng et al., “Automated proof generation              CloudEdge camera’s RTE protocol (released online [73]),
      for rust code via self-evolution,” arXiv preprint arXiv:2410.15756,
      2024.                                                                     a string called “phoneMac” is used as a binding key
                                                                                sent from the user app to the device. It is a string that
[114] S. Chakraborty, S. K. Lahiri, S. Fakhoury, M. Musuvathi, A. Lal,
      A. Rastogi, A. Senthilnathan, R. Sharma, and N. Swamy, “Rank-             uniquely identifies the user’s CloudEdge account, in the
      ing llm-generated loop invariants for program verification,” arXiv        format “US-00015kXXX4eK” in which the “XXX” part
      preprint arXiv:2310.09342, 2023.                                          with 3-characters is user-specific. Consequently, the device
[115] S. Chakraborty, G. Ebner, S. Bhat, S. Fakhoury, S. Fatima, S. Lahiri,     d sends the “phoneMac” of user u to the CloudEdge cloud,
      and N. Swamy, “Towards neural synthesis for smt-assisted proof-           which concludes the binding relation (d, u). Such a premise
      oriented programming,” arXiv preprint arXiv:2405.01787, 2024.             of binding allows an attacker to bind his malicious device
[116] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil,         with a victim user’s account using her “phoneMac”, which
      R. J. Prenger, and A. Anandkumar, “Leandojo: Theorem proving              is subject to brute force enumeration (3-characters being
      with retrieval-augmented language models,” Advances in Neural             user-specific). As a result, when the victim user opens the
      Information Processing Systems, vol. 36, pp. 21 573–21 612, 2023.
                                                                                CloudEdge camera’s app, they will encounter an unfamiliar
[117] Z. Mao, J. Wang, J. Sun, S. Qin, and J. Xiong, “Llm-aided automatic       device displaying the attacker’s contents (at the app’s launch
      modelling for security protocol verification,” in 2025 IEEE/ACM
      47th International Conference on Software Engineering (ICSE).             screen), such as those intimidating or harassing. We released
      IEEE Computer Society, 2025, pp. 734–734.                                 CloudEdge’s LSM model and the attack traces identified by
[118] D. Balzarotti, M. Cova, V. V. Felmetsger, and G. Vigna, “Multi-
                                                                                LL-Verifier online [73].
      module vulnerability analysis of web-based applications,” in Pro-
      ceedings of the 14th ACM conference on Computer and communi-
      cations security, 2007, pp. 25–35.                                        2. Automatic repairing example.
[119] M. Abadi and B. Blanchet, “Computer-assisted verification of a
      protocol for certified email,” in International Static Analysis Sym-          Based on whether outputs are structured and whether
      posium. Springer, 2003, pp. 316–335.                                      detection/repair relies on the LLM or solely on the Les
[120] M. Souad, B. Faiza, and H. Nabil, “Formal modeling iot systems on         program analyzer, these mistakes fall into four quadrants.
      the basis of biagents* and maude,” in 2020 International Conference
      on Advanced Aspects of Software Engineering (ICAASE). IEEE,                                   Unstructured output      Structured output
      2020, pp. 1–7.                                                                    PA only             K1                      K4
                                                                                         LLMs               K2                      K3
[121] S. Ouchani, K. Khebbeb, and M. Hafsi, “Towards enhancing secu-
      rity and resilience in cps: A coq-maude based approach,” in 2020              For each kind of mistake, LL-Verifier applies a tailored
      IEEE/ACS 17th International Conference on Computer Systems and
      Applications (AICCSA). IEEE, 2020, pp. 1–6.                               repair strategy:
                                                                                • K1: Identified and corrected via string-level manipulation.
[122] A. Fortas, E. Kerkouche, and A. Chaoui, “Formal verification of iot
                                                                                • K2: Forwards general parsing errors from the PA to the
      applications using rewriting logic: An mde-based approach,” Science
      of Computer Programming, vol. 222, p. 102859, 2022.                         LLM for output revision.
                                                                                • K3: After parsing, detects inconsistencies and prompts
[123] K. Khebbeb, N. Hameurlain, and F. Belala, “A maude-based rewrit-
      ing approach to model and verify cloud/fog self-adaptation and              the LLM with candidate fixes, letting it choose the most
      orchestration,” Journal of Systems Architecture, vol. 110, p. 101821,       semantically appropriate correction.
      2020.                                                                     • K4: Eliminates errors via direct abstract syntax tree
[124] S. Marir, F. Belala, and N. Hameurlain, “A strategy-based formal            (AST) manipulation.
      approach for fog systems analysis,” Future Internet, vol. 14, no. 2,          LL-Verifier employs an iterative repair loop to refine
      p. 52, 2022.                                                              LLM outputs. For each output, it checks for mistakes from
K1 to K4. Upon detecting a pattern, LL-Verifier invokes the                                                     TABLE 2: Zero-day flaws
corresponding repair routine.
                                                                                                                                Logic                              App
                                                                                                            Protocol                              Device                    Security
  < U serX | 'know' : (K, Keys), ... > // know                                         Vendor
                                                                                                            Classes1
                                                                                                                                Flaw
                                                                                                                                                   Type2
                                                                                                                                                                 Down-
                                                                                                                                                                            Impact3
   r                                                                                                                            Type                              loads
  −→ $ U serX 'callAP I : bind' cloudA | (DeviceY ; K)                      (10)       iRobot             RTE P1               LFT 1, 2      Vacuum              5M+        D
  < U serX | 'know' : (K, Keys), ... >                                                 Philips            RTE P1, CAC          LFT 3, 9      Smart light         5M+        B, E
   r                                                                                   CloudEdge          RTE P3, CAC          LFT 7, 9      Camera              1M+        A, E
  −→ $ U serX 'callAP I : bind' cloudA | (DeviceY ; K)                      (11)
                                                                                       Meross             RTE P3               LFT 5, 7      Light/Plug          1M+        A, B
                                                                                       Netvue             RTE P2, CAC          LFT 5, 9      Camera              500K+      B, E
For instance, the output in rule 10 cannot be parsed due to                            Broadlink          RTE P2, CAC          LFT 4, 9      Smart plug          1M+        B, E
a K2 issue; specifically, it contains a C-style comment. LL-                           Kwikset Kevo       RTE P2               LFT 5         Lock                500K+      D
Verifier resolves this by removing the comment, resulting                              Midea              RTE P2               LFT 5         Air conditioner     50M+       B, D
                                                                                       EZVIZ              RTE P2               LFT 5         Camera              10M+       B
in rule 11. In the subsequent iteration, rule 11 becomes                               IMOU               RTE P2               LFT 5         Camera              5M+        B
parsable and structured, but it still suffers from a K4 prob-                          August             RTE P2               LFT 5         Lock                1M+        B, D
                                                                                       Switchbot          RTE P2               LFT 4         Smart plug          500K+      B
lem: the variable DeviceY appears in the RHS but is absent                             Govee              RTE P2               LFT 5         Light               1M+        B
from the LHS. The PA addresses this by copying the missing                             Sunlogin           RTE P2               LFT 5         Smart plug          10M+       B
internal states to the LHS, producing the well-formed rule 5.                          Beurer             RTE P2               LFT 5         Air purifier        5K+        B
                                                                                       Wiz                RTE P2               LFT 5         Light               1M+        D
                                                                                       Belkin Wemo        RTE P3               LFT 6         Smart plug          1M+        B
3. Evaluation discussion                                                               Tplink Kasa        RTE P3               LFT 6         Smart plug          5M+        B
                                                                                       Aqara              INT                  LFT 8         Hub                 100K+      B
                                                                                       Tuya               INT, CAC             LFT 8, 9      Hub/Light           10M+       B
    This section outlines common errors observed in the                                Xiaomi             CAC                  LFT 9         Air purifier        50M+       E
                                                                                       Dyson              CAC                  LFT 9         Air purifier        1M+        E
evaluation of generated formal models. Addressing these                                Huawei             CAC                  LFT 9         Smart plug          23M+       E
issues can reduce the overall error rate by 75%.                                   1
                                                                                     Protocol Classes: RTE Pn : IoT RTE Paradigm n; INT: IoT Interoperability;
Duplicated internal states. We observed the presence of                            CAC: Collaborative IoT Access Control (see § 5).
                                                                                   2
duplicated internal states for a single principal in the initial                   3
                                                                                     Device Type: We provide specific device models on our website [73].
state in multiple protocols, like Broadlink, Aqara, Dyson,                           Security Impact: D: Break victims’ established binding; B:Hijack binding and
and Huawei. For instance. When generating the initial state,                       become root user; A: Bind attack devices with victim users; E: Permission escalation;
the LLMs use two internal states like formula 12.
 < cloudA | (userA : ('device' : deviceB, 'members' : nils)) >
 < cloudA | (userC : ('device' : nils, 'members' : nils)) >                                  TABLE 3: Formal model generation evaluation
                                                            (12)                                     (a) Models of protocols with zero-day flaws
instead of a single internal state in formula 13,                                      Protocol
                                                                                                    Principals   Attributes        Rules         Events          Flaws
                                                                                                                                                                        Time       Tokens
                                                                                                    CP1    FP2   CP     FP      CP     FP      CP     FP       CP FP
 < cloudA | userA : ('device' : deviceB, 'members' : nils)),                           Philips      4/4    0     8/8    0       15/15 0        6/6    0        0/1 1    88.4       21352
                                                                                       TPLink       4/4    0     10/10 0        11/11 0        5/5    0        1/1 0    77.2       19358
            userC : ('device' : nils, 'members' : nils) >    (13)                      CloudEdge    5/5    0     10/10 0        11/11 0        5/5    0        1/1 0    81.8       19636
                                                                                       Wemo         4/4    0     10/10 0        11/11 0        5/5    0        1/1 0    96.3       19947
which is inconsistent with the state-transitional rules and                            Govee        4/4    0     8/8    0       9/9    0       4/4    0        1/1 0    82.4       19090
                                                                                       iRobot       4/4    0     9/9    0       17/17 0        7/7    0        1/1 0    104.1      23000
prevents correct reasoning. This error corresponds to a K4                             August       4/4    0     11/11 0        12/12 0        5/5    0        1/1 0    108.6      21751
issue (§ 3.2), which can be repaired by merging internal                               Beurer       4/4    0     8/8    0       9/9    0       4/4    0        1/1 0    87.1       19502
                                                                                       Sunlogin     4/4    0     8/8    0       9/9    0       4/4    0        1/1 0    80.2       19405
states associated with the same principal.                                             Wiz          4/4    0     8/8    0       9/9    0       4/4    0        1/1 0    81.2       19347
                                                                                       Imou         4/4    0     9/9    0       10/11 0        4/5    0        0/1 1    91.0       19570
Omissions. Models of Philips, TPLink, and Level overlook                               Ezviz        4/4    0     9/9    0       11/11 0        5/5    0        1/1 0    91.2       20059
certain proposition definitions when extracting propositions                           Switchbot    4/4    0     11/11 0        14/15 0        6/6    0        1/1 0    95.5       21079
                                                                                       Midea        4/4    0     9/9    0       11/11 0        5/5    0        1/1 0    86.1       19301
from property texts. Additionally, when LL-Verifier                                    Meross       4/4    0     12/12 0        11/11 0        5/5    0        1/1 0    79.5       21371
detects errors in the initial output and prompts LLMs for                              Netvue       4/4    0     8/8    0       11/11 0        5/5    1        1/1 0    84.1       20752
                                                                                       Kevo         4/4    0     8/8    0       11/11 0        5/5    1        1/1 0    98.8       21688
revision, the revised output sometimes includes only the                               Broadlink    4/4    0     12/12 2        17/18 0        9/9    0        1/1 0    100.9      23146
                                                                                       Aqara        4/4    0     11/11 0        14/15 0        6/6    0        0/1 0    92.5       21328
modified portion rather than the complete result, leading to                           TuyaMatter   4/4    0     11/11 0        15/15 0        6/6    0        1/1 0    89.7       21750
incomplete Maude code.                                                                 TuyaCAC      4/4    0     10/10 0        13/13 0        5/5    0        1/1 0    97.0       24614
                                                                                       Xiaomi       4/4    0     10/10 0        13/13 0        5/5    0        1/1 0    98.7       25380
                                                                                       Dyson        4/4    1     10/10 0        13/13 0        5/5    0        0/1 0    82.0       20844
                                                                                       Huawei       4/4    1     10/10 0        13/13 0        5/5    0        0/1 0    95.0       24536
                                                                                       Average      100% 2%      100% 0.9%      98.6% 0%       99.2% 1.6%      75% 8.3% 90.4       21159
                                                                                                     (b) Models of protocols with one-day flaws
                                                                                                          Principals   Attributes      Rules         Events       Flaws
                                                                                       Protocol                                                                            Time     Tokens
                                                                                                          CP     FP    CP     FP     CP      FP     CP     FP    CP FP
TABLE 1: Primitive propositions in iRobot RTE protocol                                 Maag Level [59]    4/4    0     8/8    0      10/13 0        5/5    0     0/1 0     121.4    28359
                                                                                       Maag Kwickset      4/4    0     10/10 0       15/16 0        8/8    0     0/1 0     328.6    22945
(Automaticaly generated by LLMs)                                                       [59]
                                                                                       Delegation         4/5     0    12/13    0    11/13    0     4/5    0     0/1   0   88.6     21098
 Primitive proposition   Description                                                   Flaw1 [27]
 uaP ressButton          if userA pressed the physical button of deviceB.              Delegation         4/5     0    12/13    0    12/13    0     5/5    0     0/1   0   147.9    21171
 uaCallSetKey            if userA calls device API to set key.                         Flaw2 [27]
 uaReset                 if userA calls cloud API to reset the device.                 MQTT               4/4     0    8/8      2    9/9      0     4/5    0     0/1   0   61.6     17910
                                                                                       Flaw1 [70]
 uaOperation             if userA performs any operations                              Average            90.9% 0%     96.2% 4%      89.1% 0% 92.9% 0% 0%              0% 149.6     22297
 ucOperation             if userC performs any operations                          1
 uaOwner                 if userA is the owner of deviceB                           CP: Coverage Probability — the proportion of semantic elements that are correctly modeled.
                                                                                   2
 ucOwner                 if userC is the owner of deviceB                           FP: False Positives — the number of extra semantic elements incorrectly included in the
                                                                                   model (false positive rate in the row average).
 ucRemote                if userC is remote to the target device now
[init]
Initially, the userA is local to the deviceB and has key 'secretA';
  the cloudA records deviceB's information where its binding key is
 '' and owner is empty set
......
[state changes]
If any user presses the button on any device, then the device
records that it is pressed.
When any device is pressed with no key before, and any user calls
device API 'callAPI:setKey', then the device will change its state
to be not pressed, record the new key, and call the cloudA' s API '
callAPI:setKey' with the new binding key as an argument, change the
 device's state to record it has a key now.
When any device which already has a key is pressed, and any user
calls device API 'callAPI:setKey', then the device will change its
state to be not pressed, record the new key, and call the cloudA' s
 API 'callAPI:setKey' with the new binding key.
When the cloudA receives a 'callAPI:setKey' event from any device,
the cloudA will update its binding key record for that device.
......

[events]
If the user has some key, the user can:
1. use the key to call cloudA 's API 'callAPI:bind' ;
2. use the key to call cloudA 's API 'callAPI:reset'.
......
[properties]
The userA will always ......
Eventually, there is a time point that userC is not local to
deviceB and is not the owner of deviceB, and the next time userC is
 not local and the owner of deviceB.


Figure 3: Preprocessing result of iRobot’s RTE protocol
(Simplified version, full texts are available online [73].
