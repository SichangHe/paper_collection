                                                 Multiple Analyses, Requirements Once:
                                                          simplifying testing & verification
                                                      in automotive model-based development

                                             Philipp Berger1 , Johanna Nellen1 , Joost-Pieter Katoen1 , Erika Ábrahám1
                                                          Md Tawhid Bin Waez2 , and Thomas Rambow2
arXiv:1906.07083v1 [cs.LO] 17 Jun 2019




                                                                 1
                                                                 RWTH Aachen University, Germany
                                                  {berger, johanna.nellen, katoen, abraham}@cs.rwth-aachen.de
                                                                2
                                                                     Ford Motor Company, USA/Germany
                                                                        {mwaez, trambow}@ford.com



                                                Abstract. In industrial model-based development (MBD) frameworks,
                                                requirements are typically specified informally using textual descriptions.
                                                To enable the application of formal methods, these specifications need
                                                to be formalized in the input languages of all formal tools that should
                                                be applied to analyse the models at different development levels. In this
                                                paper we propose a unified approach for the computer-assisted formal
                                                specification of requirements and their fully automated translation into
                                                the specification languages of different verification tools. We consider a
                                                two-stage MBD scenario where first Simulink models are developed from
                                                which executable code is generated automatically. We (i) propose a spec-
                                                ification language and a prototypical tool for the formal but still textual
                                                specification of requirements, (ii) show how these requirements can be
                                                translated automatically into the input languages of Simulink Design
                                                Verifier for verification of Simulink models and BTC EmbeddedValida-
                                                tor for source code verification, and (iii) show how our unified framework
                                                enables besides automated formal verification also the automated gener-
                                                ation of test cases.


                                         1    Introduction

                                         In the automotive industry, software units for controllers are often implemen-
                                         ted using model-based development (MBD). The industry standard ISO26262
                                         recommends formal verification to ensure that such safety-critical software is
                                         implemented in accordance with the functional requirements. The work of our
                                         previous two papers [19,2] and this paper not only applies to safety critical
                                         automotive software but also to quality management (QM) or non-safety critical
                                         automotive software. In fact, we worked only on Ford QM software features
                                         in our papers. To optimally exploit recent academic developments as well as
                                         the capabilities of state-of-the-art verification tools, Ford Motor Company and
                                         RWTH Aachen University initiated an alliance research project to analyze how
                                         formal verification techniques for discrete-time systems can be embedded into
2      P. Berger et al.

Ford’s model-based controller development framework, and to experimentally
test their feasibility for industrial-scale C code controllers for mass production.
    In our previous works [19,2], we considered an MBD process starting with
the development of Simulink controller models and using Simulink’s code gener-
ation functionality to derive C code for software units. For formal verification,
we analyzed the feasibility of both Simulink Design Verifier (SLDV ) for Simulink
models as well as BTC EmbeddedPlatform verification tool for the generated C
code. Our papers [19,2] present our observations and give recommendations for
requirement engineers, model developers and tool vendors how they can con-
tribute to a formal verification process that can be smoothly integrated into
MBD.
    The most serious pragmatic obstacles that we identified for the integration
of formal methods are related to the requirement specifications. The requirement
specifications were given informally in natural language. All the considered nat-
ural language requirements described time-bounded linear temporal logic (LTL)
properties, which we manually formalized for both the SLDV and the BTC verifi-
cation tools. During the formalization we detected ambiguity, incompleteness or
inconsistency for roughly half of the textual requirements.
    The manual formalizations needed discussions with requirement engineers
to clarify and correct these flaws. However, a high degree of automation is a
prerequisite for mass production and the integration of formal methods into
the established MBD process at Ford. Automation allows the usage of formal
verification within a development team of engineers with little knowledge of for-
mal verification. Ideally, verification is automatically triggered whenever changes
have been made to either the requirements, the Simulink model, or the used veri-
fication tools. Verification results can then be stored and compared with previous
runs, making deviations from previous results easily detectable. All deviations
can then be reported to a person with a strong background in formal methods
for thorough investigation.
    We also encountered problems rooted in the fact that the formalizations for
the two different formal tools were done independently due to syntactic differ-
ences: in Simulink, requirements are themselves Simulink models that need to
be embedded into the models that should satisfy them, whereas in BTC the re-
quirements can be specified either using a graphical interface for pattern-based
specification or directly in an XML-based file input format.
    The independence of multiple requirement formalizations has several disad-
vantages. First and foremost, basically the same work is done multiple times,
using different input languages. In addition, the formalizations have the risk
to be slightly different. This may result in potentially incompatible analysis re-
sults requiring a deep and time-consuming analysis. When the formalizations are
done independently, they cost additional resources in time and expert knowledge,
raising development cost.
    In addition, typically several programming and modeling languages are used
within a company such as Ford. The preference of these languages changes over
time and each language has its own analyses tools. Different teams within a
                                      Multiple Analyses, Requirements Once                3

company like Ford may use different tools for the same purpose. The fact that
almost every formal verification tool has its unique input language is a big obsta-
cle to introduce formal methods into versatile companies like Ford. A common
requirement language for all formal verification tools may help to take advantage
of the strengths of different tools.
    To diminish these problems, this paper presents a common formal require-
ment specification framework . We focus on Simulink and C code verification in
the automotive domain, but our framework is naturally extensible to further lan-
guages and tools. Concretely, the paper makes the following main contributions:
 1. We identify a small fragment of LTL as a formal specification language that is
    expressive enough for the formalization of typical requirements in the context
    of MBD in the automotive sector .
 2. We describe our tool that was designed as a prototype for use inside this
    research project as a proof of concept. Similar to BTC EmbeddedSpecifier it
    assists users who are not experts in formal methods to specify unambiguous
    and complete formal requirements using textual descriptions according to a
    pattern-based syntax.
 3. We propose an approach for the fully automated translation of the above-
    specified formal requirements into Simulink models that can be embedded in
    SLDV verification processes.
 4. We describe how to automatically generate BTC models from those formal
    requirements for source code verification.
 5. We show how to automatically generate test objectives from formal require-
    ments that can be used for automated test-case generation.
    Our framework is illus-                                       Specification
trated in Fig. 1. While compu-                                    Textual output
ter-assisted approaches for for-                                  of requirements
mal requirement specification
have been proposed (see Sec.               Requirements
                                                             Verification
2), we believe that our ap-         Pattern-based
                                                             - Simulink verification
proach supporting direct anal-       specification
                                                             - Source code verification
                                         tool
ysis using multiple tools at
different development levels                Model data
                                            (optional)         Testing
is novel, especially the auto-
                                                               Test case generation
mated specification export to
                                                               within Simulink
Simulink and the generation of
test-cases.
                                   Fig. 1: The structure of our unified specification
                                   and analysis framework.
2   Related Work
Patterns for specifying properties in formal verification were introduced by Dwyer
et al. [7]. Cheng et al. has extended this work to real-time properties [14] and
Grunske introduced a pattern system for probabilistic properties [10]. Autili et
al. [1] recently presented a unified pattern catalog that combines known patterns
4       P. Berger et al.

for qualitative, real-time and probabilistic properties. Then the work has been
extended by some new patterns. Our works relies on the pattern catalogs from
[7,1]. Inspired by our experience with Ford [19,2], we selected a set of patterns
that covers more than 90% of our investigated automotive requirements.
    Several tools are available for pattern-based specifications. The PSPWizard
[17] and the SESAMM Specifier [8] provide for a given pattern library export
functionalities to a formal logic or to a textual representation. The SESAMM
specifier has been integrated into an industrial toolchain in the automotive do-
main. The tool PASS (Property ASSistant) [20] guides the user by a set of ques-
tions towards a suitable pattern from which a µ-calculus formula and a UML
sequence diagram can be generated. The tool PROPEL [21] represents patterns
in natural language and by finite-state automata. The COMPASS toolset [6]
supports the original patterns by Dwyer, real-time- and probabilistic patterns.
While the previous mentioned tools use the pattern catalog from [1,7,6], the work
[16] presents different patterns and a tool for the requirement specification and
automated translation to a formal language. The tool DDPSL [11] goes a step
further by allowing the user to fill the templates in a pattern with assumptions
on the variables using a defined set of logical and temporal operators. The ReSA
Tool allows an automated consistency check of requirements on multiple abstrac-
tion levels using SAT checking. The commercial tool BTC EmbeddedPlatform3
also offers the possibility to formalize textual requirements in a pattern-based
language. Former versions of the tool support a pattern catalog but the latest
release uses the universal pattern [22] that offers a graphical specification for
trigger-action based requirements. Our tool focuses on the key patterns but al-
lows for automated generation of test cases, as well as properties for Simulink
model and source code verification.
    Besides the tools for pattern-based specifications, several experience reports
on using specification patterns have been published. In [4], a case study in the
field of service-based applications is presented. [23] reports on an approach using
pattern-based specifications in the area of work flow modeling. Bosch company
investigated the suitability of the pattern catalog from [14] for 289 informal
behavioral requirements from their automotive projects. A report on the inte-
gration of a pattern-based specification tool in an industrial (automotive) tool
chain is given in [8,9]. A restricted set of patterns was used for the formal spec-
ifications within the PICASSOS project [5]. A system for modeling and testing
flight critical software was presented in [18], but their focus lies on test-case
generation and modeling structural aspects of the software system, whereas our
focus is on the automated translation of requirements.


3     Pattern-Based Requirement Specification Language

Requirement documents are commonplace in the automotive industry and are
usually written in natural language by a large number of stakeholders. These
3
    https://www.btc-es.de/en/products/btc-embeddedplatform/
                                        Multiple Analyses, Requirements Once          5


        Table 1: Pattern distributions for three different controller models.
       Pattern                                 LSC          DSR        ECC
       Invariant                             35 85.4%     50 92.6%     80 97.6%
       Time-bounded response (exact bound)   5 12.2%       4 7.4%       2 2.4%
       Event-bounded response                1 2.4%        0 0.0%       0 0.0%



can include engineers and other people without a strong background in formal
methods, which may lead to ambiguous requirements. Specification patterns may
assist engineers in writing complete and unambiguous textual requirements. A
pattern defines the behavior that is described by a requirement and uses tem-
plates for additional information like the specification of events and durations.
In contrast to most existing approaches, events are specified by a constrained
grammar, and higher-order operators, e.g. hysteresis4 , are supported to enable
specifying new operations on events.
Goals. The pattern-based specification language should produce human read-
able specifications. A formal semantics avoids ambiguities and allows the auto-
mated generation of tool-specific requirement specifications. Our aim is to keep
the pattern language simple such that no expert knowledge is needed and the
learning curve for requirement engineers is low. We believe that a limited number
of simple patterns reduces incorrect choices of patterns or scopes when writing
requirements while still covering a high percentage of requirements.
Why yet another specification language? Tools like BTC EmbeddedPlatform
come with their own, existing, pattern-based specification language and there
are existing tools for pattern-based specification. Nonetheless we decided that
creating our own language and tool was the better choice. A key difference from
many established pattern-based specification languages is that we also require
the events to be specified using a constrained grammar, enforcing the events to
be formalizable properties. This, in turn, allows us to immediately export the
entire property to a supported format without the need for any further user
interaction.
    Adding new features or constructs like higher-order operators (e.g. hysteresis)
is easy to achieve, requiring only very modular changes to the grammar and
the back-end exporter classes. We want to be able to create our own pool of
higher-order operators for event specification that can be used to ease the burden
of formalization for the engineers. Our own language allowed us to do rapid
prototyping while coming up with new ideas, without the burden of getting all
stakeholders of an established language on board beforehand.
Syntax. We used [1,7,14] as a starting point to design our pattern-based re-
quirement specification language L, whose grammar is shown in Fig. 2; for more
details see also Appendix A.
4
    Hysteresis is a functionality often used to prevent rapid toggling when observing an
    input signal against some threshold by introducing an upper and a lower delta.
6       P. Berger et al.

    specification: scope pattern;
    scope:         initially | globally;
    pattern:       invariant | response;
    initially:     ’At system start, ’;
    globally:      ’At each time step, ’;
    invariant:     ’[ ’ event ’] holds. ’;
    response:      ’if [ ’ event ’] has been valid for [ ’ duration ’], ’
                   ’then in response, after a delay of [ ’ duration ’], ’
                   ’[ ’ event ’] is valid for [ ’ duration ’]. ’;
    event:         identifier | event AND event | ...| term ≤ term | ...
    term:          identifier | term + term |...
    duration:      uint unit;
    uint:          [1..9] [0..9]*;
    unit:          ’simulation steps ’ | ’milliseconds ’ | ’seconds ’
                   | ’minutes ’ | ’hours ’;


     Fig. 2: Syntax of our pattern-based requirement specification language.


    Requirement specifications consist of a scope followed by a pattern. We start
with a limited set of scopes and patterns that can be extended later to cover fur-
ther specification types. However, these limited sets were sufficient to formalize
more than 90% of the requirements in all three case studies (Low Speed Con-
trol for Parking (LSC), Driveline State Request (DSR) and E-Clutch Control
(ECC)) we considered in [2,19] (see Table 1). Other internal case studies from
Ford show similar results.
    Currently two scopes are supported: the initially scope is used to express
that a property should hold at system start, i.e. at time step 0 of a simulation
before any operations have been performed, while the globally scope expresses
that a property should hold at each time step of an execution, but starting after
the first execution. In [1,7,14] there are further scopes like before R, after
Q, between Q and R and after Q until R that can be considered for future
inclusion.
    We support two patterns for defining which property is required to hold for
a given scope. The invariant pattern allows to state that a certain event holds
(at each time step within the specified scope), and covers both the absence
and the universality patterns from [7] if the negation of events is supported.
The response pattern specifies causalities between two events: the continuous
validity of a trigger event for a given trigger duration implies that after a fixed
separative duration the response event holds continuously for a given response
duration.
    The events in the above patterns are built from identifiers (signals, con-
stants and (calibration) parameters) using a set of functions and operators.
We support those operators and functions that were used in our case studies,
including the Boolean operators AND, OR, NOT and IMPLIES, the relational
operators <, ≤, >, ≥ and =, the arithmetic operators +, −, · and /, absolute
                                        Multiple Analyses, Requirements Once            7

scopes:     Jinitially patternK = JpatternK
            Jglobally patternK =      JpatternK
patterns: J[e] holds.K              = JeK
          Jif [eP ] has been valid for [dP ], then in response, after a delay of [d],
           [eQ ] is valid for [dQ ].K                                           
                                  = [≤JdP K] JeP K → ♦[=JdP K+JdK] [≤JdQ K] JeQ K
events:    JidentifierK           = identifier . . .
           Je1 AND e2 K           = Je1 K ∧ Je2 K . . .
           Jt1 ≤ t2 K             = Jt1 K ≤ Jt2 K . . .
durations: Jn secondsK            = 1000·n
                                     DStep
                                               ...


    Fig. 3: Semantics of our pattern-based requirement specification language.


value, minimum, maximum, functions for bit extraction (bit x of variable y) and
time delays (value of x n steps ago). The complete ANTLR grammar for events is
presented in Appendix A. We plan in future work to incorporate more advanced
operators like state change (“the value of [param] transitions from [const1] to
[const2]”), different variants of hysteresis functions, saturation, rate limiter and
ramping up functions and lookup tables. Note that though custom operators and
functions allow users a more efficient specification, special operators (e.g. lookup
tables) might not be realizable in all specification languages for which export is
provided.
Semantics. We define the semantics of requirement specifications using linear
temporal logic with quantitative temporal operators to express time durations,
that is MTL [15]. The main semantical components are shown in Fig. 3 using
only future temporal modalities (straightforward and therefore not listed in Fig.
3 are the semantics for events and durations, see Appendix A for a complete
definition). We use DStep to denote the step-size, here in milliseconds. We sup-
port durations that are multiples of DStep . An equivalent semantics using past
temporal modalities is given in Appendix A. The difference in terms of a time-
shift between the formulations using past (resp. future) operators is illustrated
in Fig. 4. The two equivalent semantics support the export of a pattern-based
specification into different specification languages. For example the specification
language of the analysis tool SLDV only supports past temporal operators.


4    Pattern-Based Requirement Specification Tool

We have implemented a pattern-based specification tool as a prototype for use
inside this research project to support requirement engineers in writing unam-
biguous and complete textual requirements. Our focus was to create a modular
tool that is easy to learn and extendible, if in the future a larger set of scopes,
patterns or operators needs to be supported.
8      P. Berger et al.

                  past temporal operators


           Trigger P      Delay      Response Q       + time-shift by dP + d + dQ
              dP           d             dQ




                                                  Trigger P      Delay       Response Q
                                                     dP           d              dQ



                                                        future temporal operators


Fig. 4: Evaluation of a response pattern with past or future operators. The
present is represented by the red tick on the timeline.




          Fig. 5: User interface of our pattern-based specification tool.



    A user can either import signals, calibratables and constants from a file,
or create, change and delete them manually. Calibratable parameters remain
constant during software execution but can be adjusted before the execution for
tuning or selecting the possible functionalities. Captured data includes a name,
description, minimum and maximum values, dimensions, a value, the data type
and the variable type (signal, calibratable or constant). With the information of
available variables readily available, the tool checks specified events for whether
all referenced variables actually exist.
    The current version of the tool provides export functionality for a selected
requirement or for all of them. Export formats are textual (.txt), SLDV (.m),
BTC (.spec) and C (.c) specifications. The last one is compatible with the SV-
COMP standard [3] and can be used for formal verification with e.g. the Ultimate
Automizer [12].
                                     Multiple Analyses, Requirements Once         9

    The requirement specification panel in Fig. 5 is the main panel of our tool.
A scope and a pattern must be selected for the requirement. A textual transla-
tion of the scope and pattern is given as well as a visualization that shows the
time steps where the chosen pattern is evaluated, see Fig. 5. Events are built us-
ing operators, functions, signals, constants and calibration parameters. For each
event, a duration and a time unit can be specified. Additionally, for patterns
with more than one event, a time delay between events can be specified, again
together with a time unit.
    If the pattern-based specification is incomplete or if it contains specification
errors, the lower part of the specification panel provides the list of errors and
warnings. When all issues are resolved, a textual formal specification is generated
from the specification. The modular set-up of the tool allows to add further
exporters, e.g. to generate specification in a logic like MTL in a straightforward
manner.
    Our prototypical implementation supports the functions abs(param),
min(param1, param2), max(param1, param2), last(param),
last(param, steps) and extractBit(index, param). For an explanation see
Appendix A. Parenthesis expressions can be built using (param) and the basic
boolean operators not, and, or and implication are provided.


5     Requirement Specification Export to Verification Tools

5.1   Export to SLDV

A formal pattern specification is exported to Simulink in the form of a Matlab
script. This script generates a specification block inside a model on the currently
selected hierarchy level. For verification on model-level, the topmost level of a
model should be selected, whereas for verification on subsystem-level the topmost
level of the subsystem should be selected. To implement the semantics of L in
Simulink, we use a custom-build, modular and interchangeable block library and
existing Simulink logic blocks.
    The following requirement is used as a running example to illustrate the
various steps:
Example 1. At each time step if [(((signal A is equal to TRUE) and ((not signal B)
is equal to constant A)) and ((the absolute value of signal C) is greater than
constant B)) and (signal D is less than constant C)] has been valid for [50
milliseconds], then in response, after a delay of [0 steps], [signal E is equal to
TRUE] is valid for [1 step].
    To support the requirement specification for SLDV, we implemented a Simulink
library with building blocks for all elements of our requirement specification lan-
guage. The library provides sub-libraries for the specification of scopes, patterns
and events.
Verification subsystem. Fig. 6 shows the topmost generated block, a verifi-
cation subsystem. Its input are all input and output signals of the Simulink model
10       P. Berger et al.

                 [signal A]                         signal A


                 [signal B]                         signal B

                                                                       ×
                 [signal C]                         signal C
                                                                              X

                 [signal D]                         signal D


                 [signal E]                         signal E

                                                               Verification Subsystem


                           Fig. 6: A sample verification subsystem block.



that are used by the generated requirement specification. The content of veri-
fication subsystems is considered during formal verification but ignored during
code generation and is not part of the generated code. The top-level verification
subsystem contains a separate verification subsystem for each requirement.
    The verification subsystem subsumes the implementation of the actual re-
quirements, i.e. encoding the expected functional behavior, by separating it into
parts: Transformations on inputs, and implementing timed behavioral aspects.
A requirement specification consists of three parts: a set of events, a pattern and
a scope; each is represented by distinct blocks in the library. Fig. 7 shows an ex-
ample requirement specification that consists of a globally scope, a response
pattern and two events.
Scopes. A scope block defines the time steps during which a pattern needs to
be evaluated. The pattern result is a Boolean input parameter. At each simu-
lation step, either the pattern result or true (if the pattern result needs not to
be evaluated at the current time step) is the input of a proof objective. During
formal verification, SLDV analyzes this proof objective. A requirement is violated
if the input of a proof objective can be false at any simulation step.
    The initially scope evaluates the pattern result only at system start, while
the globally scope evaluates the pattern result at each time step. Fig. 8b and
8a show the implementations of scopes globally and initially, respectively.
The delay block is initialized with the value 1, while all subsequent output values
will be 0. The time shift (see Section 3) is realized by the Detector block.


              [signal A]               signal A
                                                                  Trigger P
              [signal B]               signal B
                                                                                              Result   Pattern
              [signal C]               signal C
                                                                  Response Q                           Globally

              [signal D]               signal D
                                                                           Response Pattern
                                                  Trigger



              [signal E]               signal E

                                                  Response



     Fig. 7: The responseTbEb pattern of the verification subsystem in Fig. 6.
                                                          Multiple Analyses, Requirements Once              11


     0              Z−1        In         Out        A
  Constant      Signal Delay
                                    Detector               A⇒B                P
                                                                                          1          P
      1                                              B
   Pattern                                                                           (b) Scope globally
                                                         Implies

                          (a) Scope initially

         Fig. 8: Proof objectives for the scopes initially and globally.


Patterns. A pattern receives the Boolean signals from the events as inputs
along with the time duration and delays between events specified as mask pa-
rameters of the pattern. A pattern block ensures the correct order of events and
handles timing aspects like event durations and delays between events. Simulink
blocks for time durations and delays are provided by our Simulink specification
library. The output of a pattern block is again a Boolean signal. In Fig. 7, the
blocks Trigger and Response contain the part of signal transformation, whereas
the block labeled Response Pattern represents the details of the duration- and
delay checks, as shown in Fig. 9. Inside this subsystem block, the event order
(trigger before response) is established together with the specified time delay
between the two events. In our example, the trigger has to be true for 50 mil-




                  1         Event      Timed Event            Event    Timed Event   A
              Trigger P
                               Duration Check                         Delay
                                                                                           A⇒B       1
                                                                                                   Result

                 2          Event      Timed Event                                   B
             Response Q
                               Duration Check
                                                                                         Implies


              Fig. 9: The implementation of the Trigger/Response pattern.


liseconds. This duration is checked by the Duration Check block which returns
a Boolean true iff its input evaluated to true for a given number of time steps.
A delay block is then used to account for the response duration and a possible
fixed delay between trigger and response.
Events. Each event is specified in its subsystem. The event subsystems are
connected with the input signals of the verification subsystem using From blocks.
An event is built using the blocks provided by our Simulink specification library.
These building blocks must be connected in accordance with the rules of our
event grammar. The output of an event specification is a Boolean signal. Fig.
12      P. Berger et al.

              [signal A]             a
                                         a == b
                TRUE                 b
                                         Equal           AND
              [signal B]       NOT   a
                                         a == b        And
                               Not
              constant A             b                               AND
                                         Equal
              [signal C]             a abs(a)                       And
                                                  a
                                         Abs            a>b
                                                  b                         AND   1
              constant B
                                                      Greater
                                                                           And
              [signal D]                                        a
                                                                     a<b
              constant C                                        b
                                                                    Less



      Fig. 10: The logic of the trigger condition of the example requirement.


10 shows the necessary signal transformations for the trigger of the example
requirement.
Connection to the Simulink model. After the automated insertion of the
verification subsystem at a user-chosen level in the model, the inputs of the
verification system need to be connected to the corresponding signals in the
model. Because of possible data dependency issues, we use global data store
blocks for accessing the signals. For selecting the source signal, we traverse the
model in a hierarchical approach and try to find the first match of a named signal
matching the one being looked for. A data store write is then inserted into the
model at the matched location, allowing us to generate the corresponding global
data store read block next to our verification subsystem.

5.2    Export to BTC EmbeddedPlatform
We support the export of formalized requirements to BTC’s input format, so-
called SPEC files. They contain an XML-based structured representation of the
requirements and their patterns. Small transformations are applied during export
to match BTC’s pattern semantics. We consider the time step 0 to be the first time
step in the initially scope. This means that we start to evaluate the pattern
directly after initialization, i.e. before the first computation step. In contrast,
BTC starts the evaluation after the first computation step. It is not possible to
check initial variable valuations in BTC, therefore, an error is presented when
exporting a requirement with scope initially to BTC. The generated SPEC files
can then be imported into BTC EmbeddedPlatform and used for verification.

5.3    Export to Textual Requirements
Formally specified requirements can easily be exported to textual form. As many
engineers and stakeholders without a solid background in formal methods are
involved in the design, testing and implementation of the defined software com-
ponents, it is vital to present the agreed-upon requirements in a textual repre-
sentation, which is easy to understand, distribute and review. Our export feature
                                     Multiple Analyses, Requirements Once       13

for textual requirements additionally supports automatically introducing paren-
thesis around all non-trivial arguments used in the specification to prohibit mis-
interpretations or misunderstandings of the written specification—a problem we
encountered several times in [2,19].


5.4   Export to SV-Comp-style C code

To enable the use of state-of-the-art academic C code model checkers, we ex-
plicitly encode our pattern semantics in C code. This enables to embed all as-
sumptions and behavior directly in the code, instead of going around it with
LTL specifications or similar, as supported by some tools. We built a boiler-
plate framework for initializing parameters and calibratables (enabling verifying
with varying calibrations) and updating input variables after every step. We
decided to use the established VERIFIER error(); functionality for encoding
violations of the behavior allowed by the patterns as supported by many code
verifiers such as more than 20 tools participating in the SV-comp.


6     Requirement-Based Test Vector Generation

The automated generation of an SLDV specification can be reused for automated
requirement-based test vector generation. The Automotive Functional Safety
standard ISO26262 [13] recommends to identify missing test vectors and un-
intended behavior of the implemented model by: “For each requirement, a set
of test vectors should be generated. Afterwards, the structural coverage of the
requirement-based test vectors shall be measured according to a suitable cov-
erage metrics. The industry norm recommends different coverage metrics de-
pending on the ASIL-level of the model. In case the coverage metrics reveals
uncovered parts of the model, a further analysis is needed: either test vectors
are missing or unintended functionality in the model has been detected.”
    If requirements are verified using formal verification and the implemented
requirement is shown to be valid, additional, manual creation of test vectors
should not be necessary. Manual creation of test vectors is a tedious work and
should be limited to those requirements that are not tested using formal ver-
ification. We propose to reuse the automated generation of SLDV requirement
specification for generating test vectors for these same requirements. For this
purpose, we annotate the generated specification with so-called test objectives
(see Fig. 11) automatically. The test objectives specify the signal valuations that
must be considered during test-vector generation.
    The set of requirement-based test vectors depends on the chosen coverage
metric. For condition coverage, a set of test vectors is required such that each
condition takes every possible value, while for decision coverage a set of test
vectors must generate every possible outcome for each decision. Decision cover-
age is closely related to branch coverage, where conditional and unconditional
branches are considered. According to ISO26262, branch coverage is suitable
for requirement coverage at software unit-level for ASIL A to C. However, for
14      P. Berger et al.

                           {true, false}
                   1            O               {true, false}

                           {true, false}   OR        O          1

                   2            O

                                           or

             Fig. 11: A logic OR block with test objectives attached.



ASIL D, modified condition/decision coverage (MC/DC) is highly recommended.
Additionally, it is required that all conditions contributing to a decision must
independently affect the outcome of the decision.
   To achieve condition coverage, test objectives must be added to all Boolean
input signals. For decision coverage, test objectives are needed for all Boolean
output signals. If test objectives are added to all Boolean output signals and
to all Boolean input signals of blocks with more than one input parameter,
condition/decision coverage is achieved, which guarantees both condition and
decision coverage. For MC/DC coverage, test objectives are hard to generate
and currently out of scope of our project. One way to at least partly cover
MC/DC would be to generate test objectives for all Boolean combinations of
possible input signals. For an OR block, we currently generate vectors for both
outcomes, but ”true” could be generated by inputs 01, 10 or 11—by adding
additional logic we can enforce all combinations to be generated.
    Alternatively, we propose to use the built-in function of SLDV to compute
a set of test vectors for MC/DC coverage. Unfortunately, this functionality is
currently only available on model-level. To get requirement-based test vectors
for the model, MC/DC must be checked at requirement (i.e. subsystem) level
while test vectors must be generated for the complete model.
    To automate the requirement-based test vector generation, we added test
objectives for condition/decision coverage to all blocks in our Simulink formal
specification library. The relational operators compute Boolean output signals
that also must be annotated with test objectives. Additional test objectives are
necessary for all temporal operators to assure the correct length of generated
test cases. Since we handle Boolean signals only, all test objectives can take the
values true and false. Fig. 11 presents the implementation of the annotated
Boolean Or operator from our specification library.
    Annotating the specification library allows the flexibility of adding/removing
test objectives without adapting the source code of the specification tool. This
enables the user to maintain a set of specification libraries for different coverage
metrics or to create a library without any test objective annotations.
                                       Multiple Analyses, Requirements Once          15

7   Conclusion and Future Work

In this paper we presented a prototypical pattern-based specification tool to-
gether with automated translations to SLDV and BTC EmbeddedPlatform together
with an adaption of the SLDV input for automated test-case generation. This cor-
responds to the vision of enabling engineers to specify requirements with formal
semantics once and then applying the requirements in multiple analyses. The
tool was designed as a prototype for use inside this research project as a proof
of concept.
    Although a big step towards a highly automated automotive verification pro-
cess has been made within this project and investigations by Ford have been
producing encouraging results, this is only a proof-of-concept and many open
problems still need to be resolved.
    As future work we plan the extension of our pattern set with a few further
relevant elements like time- and event-bounded response patterns. We plan to
tackle the automated translation of textual legacy requirements into formal nota-
tion. Scripts are needed to further automate verification at different development
levels with suitable configuration parameters, and to trigger the verification pro-
cess if changes are applied to the model or the requirements. Another module
should monitor the verification results and automatically report conspicuous
behavior if the comparison with previous results reveals deviations. In case of
invalid verification results, counterexamples should be analyzed.
    We plan to use the export of formalized requirements to SV-COMP like
C-code patterns in order to benchmark academic C-code model checkers on
industrial examples against commercial tools.


References

 1. Autili, M., Grunske, L., Lumpe, M., Pelliccione, P., Tang, A.: Aligning qualitative,
    real-time, and probabilistic property specification patterns using a structured en-
    glish grammar. IEEE Transactions on Software Engineering 41(7), 620–638 (2015).
    https://doi.org/10.1109/TSE.2015.2398877
 2. Berger, P., Katoen, J.P., Ábrahám, E., Waez, M.T.B., Rambow, T.: Verifying
    auto-generated c code from simulink. In: Formal Methods. pp. 312–328. Springer
    International Publishing (2018). https://doi.org/10.1007/978-3-319-95582-7 18
 3. Beyer, D.: Software verification with validation of results - (report on SV-
    COMP 2017). In: Legay, A., Margaria, T. (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems - 23rd International Conference, TACAS
    2017, Held as Part of the European Joint Conferences on Theory and Prac-
    tice of Software, ETAPS 2017, Uppsala, Sweden, April 22-29, 2017, Proceed-
    ings, Part II. Lecture Notes in Computer Science, vol. 10206, pp. 331–349 (2017).
    https://doi.org/10.1007/978-3-662-54580-5 20
 4. Bianculli, D., Ghezzi, C., Pautasso, C., Senti, P.: Specification patterns from re-
    search to industry: A case study in service-based applications. In: Proc. of ICSE.
    pp. 968–976. IEEE (2012). https://doi.org/10.1109/ICSE.2012.6227125
16      P. Berger et al.

 5. Botham, J., Dhadyalla, G., Powell, A., Miller, P., Haas, O., McGeoch, D.,
    Rao, A.C., O’Halloran, C., Kiec, J., Farooq, A., Poushpas, S., Tudor, N.: PI-
    CASSOS – Practical applications of automated formal methods to safety re-
    lated automotive systems. In: SAE Technical Paper. SAE International (2017).
    https://doi.org/10.4271/2017-01-0063
 6. Bozzano, M., Cimatti, A., Katoen, J., Nguyen, V.Y., Noll, T., Roveri, M.: Safety,
    dependability and performance analysis of extended AADL models. Comput. J.
    54(5), 754–775 (2011). https://doi.org/10.1093/comjnl/bxq024
 7. Dwyer, M.B., Avrunin, G.S., Corbett, J.C.: Patterns in property specifica-
    tions for finite-state verification. In: Proc. of ICSE. pp. 411–420. ACM (1999).
    https://doi.org/10.1145/302405.302672
 8. Filipovikj, P., Jagerfield, T., Nyberg, M., Rodriguez-Navas, G., Seceleanu,
    C.: Integrating pattern-based formal requirements specification in an in-
    dustrial tool-chain. In: Proc. of COMPSAC. pp. 167–173. IEEE (2016).
    https://doi.org/10.1109/COMPSAC.2016.140
 9. Filipovikj, P., Nyberg, M., Rodriguez-Navas, G.: Reassessing the pattern-based
    approach for formalizing requirements in the automotive domain. In: Proc. of RE.
    pp. 444–450. IEEE (2014). https://doi.org/10.1109/RE.2014.6912296
10. Grunske, L.: Specification patterns for probabilistic quality properties. In: Proc. of
    ICSE. pp. 31–40. ACM (2008). https://doi.org/10.1145/1368088.1368094
11. Guglielmo, L.D., Fummi, F., Orlandi, N., Pravadelli, G.: DDPSL: An easy
    way of defining properties. In: Proc. of ICCD. pp. 468–473. IEEE (2010).
    https://doi.org/10.1109/ICCD.2010.5647654
12. Heizmann, M., Hoenicke, J., Podelski, A.: Software model checking for people who
    love automata. In: Sharygina, N., Veith, H. (eds.) Computer Aided Verification
    - 25th International Conference, CAV 2013, Saint Petersburg, Russia, July 13-
    19, 2013. Proceedings. Lecture Notes in Computer Science, vol. 8044, pp. 36–52.
    Springer (2013). https://doi.org/10.1007/978-3-642-39799-8 2
13. ISO Central Secretary: Road vehicles Functional safety. Standard ISO 26262-
    1:2011, International Organization for Standardization, Geneva, CH (2011), https:
    //www.iso.org/standard/62711.html
14. Konrad, S., Cheng, B.H.C.: Real-time specification patterns. In: Proc. of ICSE.
    pp. 372–381. ACM (2005). https://doi.org/10.1145/1062455.1062526
15. Koymans, R.: Specifying real-time properties with metric temporal logic. Real-
    Time Systems 2(4), 255–299 (1990). https://doi.org/10.1007/BF01995674
16. Liu, S., Wang, X., Miao, W.: Supporting requirements analysis using pattern-based
    formal specification construction. In: Proc. of ICFEM. pp. 100–115. Springer (2015)
17. Lumpe, M., Meedeniya, I., Grunske, L.: PSPWizard: Machine-assisted definition of
    temporal logical properties with specification patterns. In: Proc. of SIGSOFT/FSE.
    pp. 468–471. ACM (2011). https://doi.org/10.1145/2025113.2025193
18. Moitra, A., Siu, K., Crapo, A.W., Chamarthi, H.R., Durling, M., Li, M., Yu, H.,
    Manolios, P., Meiners, M.: Towards development of complete and conflict-free re-
    quirements. In: RE. pp. 286–296. IEEE Computer Society (2018)
19. Nellen, J., Rambow, T., Waez, M.T.B., Ábrahám, E., Katoen, J.P.: Formal veri-
    fication of automotive simulink controller models: Empirical technical challenges,
    evaluation and recommendations. In: Formal Methods. pp. 382–398. Springer In-
    ternational Publishing (2018). https://doi.org/10.1007/978-3-319-95582-7 23
20. Remenska, D., Willemse, T.A.C., Templon, J., Verstoep, K., Bal, H.: Property
    specification made easy: Harnessing the power of model checking in UML designs.
    In: Formal Techniques for Distributed Objects, Components, and Systems. pp.
    17–32. Springer (2014)
                                        Multiple Analyses, Requirements Once           17

21. Smith, R.L., Avrunin, G.S., Clarke, L.A., Osterweil, L.J.: PROPEL: An approach
    supporting property elucidation. In: Proc. of ICSE. pp. 11–21. IEEE (2002).
    https://doi.org/10.1109/ICSE.2002.1007952
22. Teige, T., Bienmller, T., Holberg, H.J.: Universal pattern – Formalization, testing,
    coverage, verification, and test case generation for safety-critical requirements. In:
    Proc. of MBMV (2016)
23. Wong, P.Y.H., Gibbons, J.: Property specifications for workflow modelling. In:
    Proc. of IFM. pp. 56–71. Springer (2009)
18     P. Berger et al.

A    Appendix

Syntax In the following we present the formal grammar for the specification of
events.

grammar EventGrammar;

//////////////////////////////
//GRAMMAR RULES (Parser)    //
//////////////////////////////
//////////////////////////////
// EVENT (Start rule)       //
//////////////////////////////
event : expr=booleanExpression EOF;

//////////////////////////////
// BOOLEAN EXPRESSIONS //
//////////////////////////////
booleanExpression : booleanTerm (booleanImplication booleanTerm)*;
booleanTerm : booleanFactor (booleanAddition booleanFactor)*;
booleanFactor : booleanEqualityTerm (booleanMultiplication booleanEqualityTerm)*;
booleanEqualityTerm : booleanBaseTerm (booleanEquality booleanBaseTerm)*;
booleanBaseTerm
  : booleanAtom
  | booleanNotExpression
  | booleanParExpression
  | relationalExpression
  | booleanFunctionExpression
booleanNotExpression : booleanNot booleanBaseTerm;
booleanParExpression : leftPar booleanExpression rightPar;
relationalExpression : arithmeticExpression relationalOperator arithmeticExpression;
booleanFunctionExpression : booleanBinaryFunctionExpression;
booleanBinaryFunctionExpression
  : BIT_EXTRACTION_TEXTUAL arithmeticExpression OF arithmeticExpression
  | booleanBinaryFunction leftPar arithmeticExpression
     comma arithmeticExpression rightPar;

//////////////////////////////
// ARITHMETIC EXPRESSIONS    //
//////////////////////////////
arithmeticExpression : arithmeticFactor (arithmeticAddition arithmeticFactor)*;
arithmeticFactor : arithmeticBaseTerm (arithmeticMultiplication arithmeticBaseTerm)*;
arithmeticBaseTerm
  : arithmeticAtom
  | arithmeticParExpression
  | arithmeticSignExpression
                             Multiple Analyses, Requirements Once   19

  | arithmeticFunction
arithmeticParExpression : leftPar arithmeticExpression rightPar;
arithmeticSignExpression : arithmeticSign arithmeticBaseTerm;
//Functions
arithmeticFunction
  : arithmeticUnaryFunctionExpression
  | arithmeticBinaryFunctionExpression
  | temporalUnaryFunctionExpression
  | temporalBinaryFunctionExpression;
arithmeticUnaryFunctionExpression
  : arithmeticUnaryFunction leftPar arithmeticExpression rightPar
  | arithmeticUnaryFunctionTextual arithmeticExpression;
arithmeticBinaryFunctionExpression
  : arithmeticBinaryFunction leftPar arithmeticExpression
     comma arithmeticExpression rightPar
  | arithemticBinaryFunctionTextual arithmeticExpression
     AND arithmeticExpression;
temporalUnaryFunctionExpression
  : temporalUnaryFunction leftPar arithmeticExpression rightPar
  | temporalUnaryFunctionTextual arithmeticExpression;
temporalBinaryFunctionExpression
  : temporalBinaryFunction leftPar arithmeticExpression
     comma arithmeticBaseTerm rightPar
  | LAST_BINARY_TEXTUAL_0 arithmeticExpression
     arithmeticBaseTerm LAST_BINARY_TEXTUAL_1;

///////////////
//Operators //
///////////////
booleanNot : NOT;
booleanAddition : OR;
booleanMultiplication : AND;
booleanImplication : IMPLICATION;
booleanEquality : EQ;
relationalOperator
  : EQ
  | GT
  | GTEQ
  | LT
  | LTEQ;
arithmeticAddition
  : PLUS
  | MINUS;
arithmeticMultiplication
  : TIMES
20    P. Berger et al.

  | DIV;
arithmeticSign
  : PLUS
  | MINUS;

///////////////
//Functions //
///////////////
booleanBinaryFunction : BIT_EXTRACTION_FUNCTION;
arithmeticUnaryFunction : ABS_FUNCTION;
arithmeticUnaryFunctionTextual : ABS_TEXTUAL;
arithmeticBinaryFunction
  : MIN_FUNCTION
  | MAX_FUNCTION;
arithemticBinaryFunctionTextual
  : MIN_TEXTUAL
  | MAX_TEXTUAL;

//temporal
temporalUnaryFunction : LAST_UNARY_FUNCTION;
temporalUnaryFunctionTextual : LAST_UNARY_TEXTUAL;
temporalBinaryFunction : LAST_BINARY_FUNCTION;

/////////////////
//Parentheses //
/////////////////
leftPar : LPAR;
rightPar : RPAR;

/////////////////
//Other        //
/////////////////
comma : COMMA;

/////////////////////////////////
//Identifiers and Constants    //
/////////////////////////////////
booleanAtom
  : booleanConstant
  | booleanIdentifier;
arithmeticAtom
  : arithmeticConstant
  | arithmeticIdentifier;
booleanConstant
  : TRUE
                             Multiple Analyses, Requirements Once   21

  | FALSE;
arithmeticConstant
  : INTEGER
  | FLOATINGPOINT;
booleanIdentifier : IDENTIFIER;
arithmeticIdentifier : IDENTIFIER;

//////////////////////////////
//TOKENS (Lexer rules)      //
//////////////////////////////
/////////////////
//Constants    //
/////////////////
TRUE
  : ’TRUE’
  | ’True’
  | ’true’;
FALSE
  : ’FALSE’
  | ’False’
  | ’false’;

/////////////////
//Operators    //
/////////////////
//boolean
OR
  : ’|’
  | ’or’;
AND
  : ’&’
  | ’and’;
NOT
  : ’!’
  | ’not’;
IMPLICATION
  : ’=>’
  | ’implies’;
//arithmetic
PLUS
  : ’+’
  | ’plus’;
MINUS
  : ’-’
  | ’minus’;
22    P. Berger et al.

TIMES
  : ’*’
  | ’multiplied with’;
DIV
  : ’/’
  | ’divided by’;
//relational
GT
  : ’>’
  | ’is greater than’;
GTEQ
  : ’>=’
  | ’is greater or equal to’;
LT
  : ’<’
  | ’is less than’;
LTEQ
  : ’<=’
  | ’is less or equal to’;
EQ
  : ’=’
  | ’is equal to’;

/////////////////
//Parentheses //
/////////////////
LPAR
  : ’(’
  | ’left parenthesis’;
RPAR
  : ’)’
  | ’right parenthesis’;

/////////////////
//Other        //
/////////////////
OF : ’of’;
COMMA : ’,’;

/////////////////
//Functions    //
/////////////////
BIT_EXTRACTION_TEXTUAL : ’bit’;
BIT_EXTRACTION_FUNCTION : ’extractBit’;
ABS_FUNCTION : ’abs’;
                                            Multiple Analyses, Requirements Once            23

ABS_TEXTUAL : ’the absolute value of’;
MIN_FUNCTION : ’min’;
MIN_TEXTUAL : ’the minimum of’;
MAX_FUNCTION : ’max’;
MAX_TEXTUAL : ’the maximum of’;
LAST_UNARY_FUNCTION : ’last’;
LAST_UNARY_TEXTUAL : ’the previous value of’ ;
LAST_BINARY_FUNCTION : ’last’;
LAST_BINARY_TEXTUAL_0 : ’the value of’;
LAST_BINARY_TEXTUAL_1 : ’steps ago’ ;

/////////////////
//Identifiers //
/////////////////
IDENTIFIER : CHAR (CHAR | SPECIAL_CHAR | DIGIT)*;
CHAR
 : (’a’..’z’)
 | (’A’..’Z’);
SPECIAL_CHAR : ’_’;

/////////////////
//Numbers      //
/////////////////
INTEGER : DIGIT+;
FLOATINGPOINT : DIGIT+ ’.’ DIGIT+;
DIGIT :(’0’..’9’);

/////////////////
//White spaces //
/////////////////
WS : [ \r\t\n] + -> skip // skip spaces, tabs, newlines;

Semantics The semantics of w for temporal operators that reach to the past
is given by the following MTL formulas:


1. P ,
   if s = initially, p = invariant and E = (P ),


2. [0,∞] P ,
   if s = globally, p = invariant and E = (P ),

                                                                                            
3. ♦[tp +td +tq ,tp +td +tq ]   [−td −tq ,td −tq ] (P S[tp ,tp ] true) → (Q S[tq ,tq ] true) ,
24      P. Berger et al.

     if s = initially, p = responseTbEb and E = (P, Q)
     (Note, that a time shift of tp + td + tq is needed for this scope/pattern com-
     bination.),

                                                                                      
4. [tp +td +tq ,∞]       [−td −tq ,−td −tq ] (P S[tp ,tp ] true) → (Q S[tq ,tq ] true) ,
     if s = globally, p = responseTbEb and E = (P, Q)
     (Note, that a time shift of tp + td + tq is needed for this scope/pattern com-
     bination.).




Supported Functions

Operator                 Meaning
abs(param)               Absolute value of param.
min(param1, param2)      The minimum of param1 and param2.
max(param1, param2)      The maximum of param1 and param2.
last(param)              The value of param one step ago.
last(param, steps)       The value of param steps step ago.
extractBit(index, param) The bit at position index of param.
                                     Multiple Analyses, Requirements Once      25

B     Appendix




In this appendix, we present the Simulink library for the formal specification
of properties for SLDV. We defined sub-libraries for the specification of scopes,
patterns, and events (see Figure 12). Additionally, the library contains a set of
auxiliary scripts that can be called to create a specification.




Fig. 12: Simulink library with sub-libraries for the specification of scopes, pat-
terns and events.




B.1   Scopes




Our specification library supports the set S = {initially, globally} of scopes.
A scope defines the time steps in which a pattern is evaluated.
26       P. Berger et al.


     initially (Category: Scope)

     At system start, [Pattern].
     Interface




     Parameters:
      – Input parameter “Pattern”: The pattern that is evaluated at system
        start.
     Implementation




     Comments

      – No scope shift is performed. For more information on the time shift,
        we refer to Section 3.
      – Delay mask parameter “Delay length”: 1
      – Delay mask parameter “Initial condition”: 1
                               Multiple Analyses, Requirements Once      27


initially (Category: Scope)

At system start, [Pattern].
Interface




Parameters:
 – Input parameter “Pattern”: The pattern that is evaluated at system
   start.
Implementation




Comments

 – A scope shift is performed. For more information on the time shift,
   we refer to Section 3.
 – Mask parameter “Time shift”: The time step to which the scope must
   be shifted.
 – Delay mask parameter “Delay length”: 1
 – Delay mask parameter “Initial condition”: 1
 – Detector mask parameter “Step for input detection”: 1
 – Detector mask parameter “Time steps for delay”: d − 1
 – Detector mask parameter “Time steps for output duration”: 1
28       P. Berger et al.


     globally (Category: Scope)

     At each time step, [Pattern].
     Interface




     Parameters:
      – Input parameter “Pattern”: The pattern that is evaluated at each
        time step.

     Implementation




     Comments

      – No scope shift is performed. For more information on the time shift,
        we refer to Section 3.
                                   Multiple Analyses, Requirements Once      29

B.2    Patterns




The Simulink library for formal specification supports the set P = {invariant, responseTbEb}
of patterns and offers Simulink blocks for durations and delays. A pattern is a
template for the definition of properties. A set of events with time durations and
delays between events must be specified.




   invariant (Category: Pattern)

   [P] holds.
   Interface




   Parameters:
      – Input parameter “P”: The invariant event.
      – Output parameter “Result”: The invariant pattern result (Boolean).

   Implementation




   Comments
      – –
30       P. Berger et al.


     responseTbEb (Category: Pattern)

     If [P] has been valid for [Trigger duration], then in response, after a delay
     of [Delay] , [Q] is valid for [Response duration].
     Interface




     Parameters:
      – Input parameter “Trigger P”/“Response Q”: The trigger/response
        event.
      – Output parameter “Result”: The response pattern result (Boolean).
      – Mask parameter “Delay”: The delay between the trigger and the re-
        sponse event.
      – Mask parameter: “Trigger duration”/“Response duration”: The du-
        ration of the trigger/response event.

     Implementation




                            Subsystem implementation:




     Comments

      – Duration/Duration1 mask parameter: Trigger/Response duration
      – Delay mask parameter: Delay + Response duration
                                Multiple Analyses, Requirements Once        31


duration (Category: Pattern)

[Event is valid for] Time duration simulation steps.
Interface




Parameters:
 – Input parameter “Event”: The event for which a duration is specified.
 – Output parameter “Timed event”: The timed event result (Boolean).
 – Mask parameter “Time duration”: The duration of the event in sim-
   ulation steps.

Implementation




Comments

 – Detector mask parameter “External reset”: No
 – Detector mask parameter “Time steps for input detection”: time Du-
   ration
 – Detector mask parameter “Time steps for delay (optional)”: 0
 – Detector mask parameter “Time steps for output duration”: 1
 – A test objective is added to ensure generated test vectors of the cor-
   rect length.
32       P. Berger et al.


     delay (Category: Pattern)

     after a delay of Time duration simulation steps, [Event is valid].
     Interface




     Parameters:
      – Input parameter “Event”: The event which is delayed.
      – Output parameter “Delayed event”: The delayed event result
        (Boolean).
      – Mask parameter “Time Delay”: The delay of the event in simulation
        steps.

     Implementation




     Comments

      – Detector mask parameter “External reset”: No
      – Detector mask parameter “Time steps for input detection”: 1
      – Detector mask parameter “Time steps for delay (optional)”: time
        Duration
      – Detector mask parameter “Time steps for output duration”: 1
      – A test objective is added to ensure generated test vectors of the cor-
        rect length.
                                    Multiple Analyses, Requirements Once      33

B.3   Events




Events are specified in a subsystem using building blocks from the specification
library for signals, constants, calibration parameters, operators and functions.
For each input signal of the event, a “signal in” block is used and its output is
connected to the input of a “signal goto” block. This provides the interface and
allows to access the signal using a “signal from” block during event specifica-
tion. Our event library contains sub-libraries for signals and parameters and for
operators and funcations (see Figure 13).




Fig. 13: Simulink library for events with sub-libraries for the specification of
signals and parameters and for operators and functions.




Signals, Constants and Calibration Parameters
34         P. Berger et al.


     input/output signal (Category: Event – Signals and Parameters)
     –
     Interface




     Parameters:
         – Mask parameter “Port number”: The number of the corresponding
           input/output port.

     Implementation
                                           –

     Comments

         – Used to define the interface for (verification) subsystems.
                                Multiple Analyses, Requirements Once         35


signal (Category: Event – Signals and Parameters)

signal name, e.g. signal A
Interface




Parameters:
 – Mask parameter “Goto Tag”: The tag of the corresponding signal
   goto block.

Implementation
                                    –

Comments

 – Each signal in block is connected with a signal goto block to make
   the signal accessible during event specification.
 – Signal from blocks are used for the specification of signals inside the
   event specification.
36       P. Berger et al.


     constant (Category: Event – Signals and Parameters)

     constant name, e.g. constant A
     Interface




     Parameters:

      – Mask parameter “Constant value”: The numerical value of the con-
        stant.
     Implementation




     Comments
      – –
                                     Multiple Analyses, Requirements Once      37


   calibration parameter (Category: Event – Signals and Parameters)

   signal name, e.g. calibration A
   Interface




   Parameters:

     – Mask parameter “Calibration parameter”: The name of the corre-
       sponding calibration parameter.

   Implementation




   Comments
     – –




Operators and Functions The sub-library for operators and functions is fur-
ther divided into sub-libraries for Boolean operators, arithmetic operators, rela-
tional operators, functions and parentheses (see Figure 14).
38       P. Berger et al.




Fig. 14: Simulink library for events with sub-libraries for the specification of
signals and parameters and for operators and functions.


     not (Category: Event – Operators and Functions – Boolean Operators)

     not [In1]
     Interface




     Parameters:
      – Input parameter “In1”: input that is negated.
      – Output parameter “Out1”: negation of the input.

     Implementation




     Comments

      – A test objective is added for the generation of test vectors for true/-
        false result.
                                Multiple Analyses, Requirements Once         39


and (Category: Event – Operators and Functions – Boolean Operators)

[In1] and [In2]
Interface




Parameters:
 – Input parameter “In1”/“In2”: The inputs to which the and operator
   is applied.
 – Output parameter “Out1”: The logical and of the two input param-
   eters.
Implementation




Comments

 – Test objectives are added for the generation of test vectors for all
   possible input combinations.
 – A test objective is added for the generation of test vectors for true/-
   false result.
40       P. Berger et al.


     or (Category: Event – Operators and Functions – Boolean Operators)

     [In1] or [In2]
     Interface




     Parameters:

      – Input parameter “In1”/“In2”: The inputs to which the or operator
        is applied.
      – Output parameter “Out1”: The logical or of the two input parame-
        ters.
     Implementation




     Comments

      – Test objectives are added for the generation of test vectors for all
        possible input combinations.
      – A test objective is added for the generation of test vectors for true/-
        false result.
                                Multiple Analyses, Requirements Once         41


implies (Category: Event – Operators and Functions – Boolean Opera-
tors)

[A] implies [B]
Interface




Parameters:
 – Input parameter “A”/“B”: The inputs to which the implication op-
   erator is applied.
 – Output parameter “A ⇒ B”: The logical implication of the two input
   parameters.

Implementation




Comments

 – Test objectives are added for the generation of test vectors for all
   possible input combinations.
 – A test objective is added for the generation of test vectors for true/-
   false result.
42       P. Berger et al.


     plus (Category: Event – Operators and Functions – Arithmetic Opera-
     tors)

     [a] plus [b]
     Interface




     Parameters:
      – Input parameter “a”/“b”: The inputs to which the addition operator
        is applied.
      – Output parameter “a+b”: The addition of the two input parameters.

     Implementation




     Comments
      – –
                              Multiple Analyses, Requirements Once     43


minus (Category: Event – Operators and Functions – Arithmetic Opera-
tors)

[a] minus [b]
Interface




Parameters:
 – Input parameter “In1”/“In2”: The inputs to which the subtraction
   operator is applied.
 – Output parameter “a-b”: The subtraction of the two input parame-
   ters.
Implementation




Comments
 – –
44       P. Berger et al.


     multiplication (Category: Event – Operators and Functions – Arith-
     metic Operators)

     [a] multiplied with [b]
     Interface




     Parameters:
      – Input parameter “a”/“b”: The inputs to which the multiplication
        operator is applied.
      – Output parameter “a*b”: The multiplication of the two input param-
        eters.
      – Mask parameter “Number of inputs”: “2”.
      – Mask parameter “Multiplication”: Element-wise(.*).

     Implementation


     Comments
      – –
                              Multiple Analyses, Requirements Once      45


division (Category: Event – Operators and Functions – Arithmetic Op-
erators)

[a] divided by [b]
Interface




Parameters:

 – Input parameter “a”/“b”: The inputs to which the division operator
   is applied.
 – Output parameter “a/b”: The division of the two input parameters.
 – Mask parameter “Number of inputs”: “*/”.
 – Mask parameter “Multiplication”: Element-wise(.*).

Implementation


Comments
 – –
46       P. Berger et al.


     plus sign (Category: Event – Operators and Functions – Arithmetic
     Operators)

     plus [a]
     Interface




     Parameters:
      – Input parameter “a”: The inputs to which the positive sign is applied.
      – Output parameter “+a”: The computation result.

     Implementation




     Comments
      – –
                                Multiple Analyses, Requirements Once        47


minus sign (Category: Event – Operators and Functions – Arithmetic
Operators)

minus [a]
Interface




Parameters:
 – Input parameter “a”: The inputs to which the negative sign is applied.
 – Output parameter “-a”: The computation result.

Implementation




Comments
 – –
48       P. Berger et al.


     less (Category: Event – Operators and Functions – Relational Opera-
     tors)

     [a] is less than [b]
     Interface




     Parameters:

      – Input parameter “a”/“b”: The inputs which are compared using the
        less operator.
      – Output parameter “a<b”: The comparison result.

     Implementation




     Comments

      – A test objective is added for the generation of test vectors for true/-
        false result.
                                Multiple Analyses, Requirements Once         49


less or equal (Category: Event – Operators and Functions – Relational
Operators)

[a] is less or equal to [b]
Interface




Parameters:
 – Input parameter “a”/“b”: The inputs which are compared using the
   less or equal operator.
 – Output parameter “a≤b”: The comparison result.

Implementation




Comments

 – A test objective is added for the generation of test vectors for true/-
   false result.
50       P. Berger et al.


     greater (Category: Event – Operators and Functions – Relational Op-
     erators)

     [a] is greater than [b]
     Interface




     Parameters:

      – Input parameter “a”/“b”: The inputs which are compared using the
        greater operator.
      – Output parameter “a>b”: The comparison result.

     Implementation




     Comments

      – A test objective is added for the generation of test vectors for true/-
        false result.
                                 Multiple Analyses, Requirements Once        51


greater or equal (Category: Event – Operators and Functions – Rela-
tional Operators)

[a] is greater or equal to [b]
Interface




Parameters:
 – Input parameter “a”/“b”: The inputs which are compared using the
   greater or equal operator.
 – Output parameter “a≥b”: The comparison result.

Implementation




Comments

 – A test objective is added for the generation of test vectors for true/-
   false result.
52       P. Berger et al.


     equal (Category: Event – Operators and Functions – Relational Opera-
     tors)

     [a] is equal to [b]
     Interface




     Parameters:
      – Input parameter “a”/“b”: The inputs which are compared using the
        equal operator.
      – Output parameter “a==b”: The comparison result.

     Implementation




     Comments

      – A test objective is added for the generation of test vectors for true/-
        false result.
                              Multiple Analyses, Requirements Once   53


min (Category: Event – Operators and Functions – Functions)

the minimum of [a] and [b]
Interface




Parameters:
 – Input parameter “a”/“b”: The inputs from which the minimum is
   selected.
 – Output parameter “min(a,b)”: The minimum of the two inputs.
 – Mask parameter “Function”: min.
 – Mask parameter “Number of input ports”: 2.

Implementation


Comments
 – –
54       P. Berger et al.


     max (Category: Event – Operators and Functions – Functions)

     the maximum of [a] and [b]
     Interface




     Parameters:
      – Input parameter “a”/“b”: The inputs from which the maximum is
        selected.
      – Output parameter “max(a,b)”: The maximum of the two inputs.
      – Mask parameter “Function”: max.
      – Mask parameter “Number of input ports”: 2.

     Implementation


     Comments
      – –
                               Multiple Analyses, Requirements Once       55


abs (Category: Event – Operators and Functions – Functions)

the absolute value of [a]
Interface




Parameters:

 – Input parameter “a”: The inputs for which the absolute value is com-
   puted.
 – Output parameter “abs(a)”: The absolute value of the input.

Implementation


Comments
 – –
56       P. Berger et al.


     last (Category: Event – Operators and Functions – Functions)

     the value of [a] [delay] simulation steps ago
     Interface




     Parameters:
      – Input parameter “a”: The input for which the past value is computed.
      – Output parameter “last(a,delay)”: The value of the input a delay
        simulation steps ago.
      – Mask parameter “Time delay”: The number of steps the last operator
        reaches.
     Implementation




     Comments

      – Mask parameter “Delay length” of Delay block: Source= Dialog,
        Value = delay.
      – A test objective is added to ensure generated test vectors of the cor-
        rect length.
                               Multiple Analyses, Requirements Once       57


extractBit (Category: Event – Operators and Functions – Functions)

bit [bit] of [a]
Interface




Parameters:
 – Input parameter “a”: The input from which a bit is extracted.
 – Output parameter “extractBit(a,bit)”: The value of bit “bit” of the
   input a.
 – Mask parameter “Bit”: The number of the bit that is to be extracted.

Implementation




Comments

 – Mask parameter “Bits to extract” of Extract Bits block: Range of
   bits.
 – Mask parameter “Bit indices” of Extract Bits block: [bit, bit].
58       P. Berger et al.


     parenthesis (Category: Event – Operators and Functions – Functions)

     ([In1])
     Interface




     Parameters:
      – Input parameter “In1”: The input that should be surrounded by a
        parenthesis.
      – Output parameter “Out1”: The computed parenthesis expression.

     Implementation




     Comments
      – –




B.4     Scripts




Currently, the library is shipped with a single script that defines a matlab func-
tion to connect the inputs of a specification block with matching signals in the
Simulink model.
                                Multiple Analyses, Requirements Once        59

addSubsystemConnection

Parameters:

 – Input parameter “systempath”: The path to the top-level verification
   subsystem of the specification.
 – Input parameter “blockName”: The name of the top-level verification
   subsystem of the specification.
 – Input parameter “signalNames”: A list of strings that contains the
   names of the input signals of the top-level specification block.

Description
This function connects the inports of a verification subsystem with the
matching signals in the selected (sub)model. For each input signal in
the list of signal names, a search for a matching signal is started. In a
first step, the input and output signals of the selected (sub)system are
searched. If no matching signal name is found, all nested subsystems
are searched, starting with the innermost subsystem. If the search is
successful, a Data Store Write block is attached to the signal source.
Additionally, a corresponding Date Store block is added to the selected
(sub)system and the corresponding inport is connected with the output of
a Data Store Read block. If no matching signal is found, an error message
is printed.
